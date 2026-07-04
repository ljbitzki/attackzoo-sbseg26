from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

from modules.attackzoo.common import _ensure_dir, _phase_of

_re = re


def _read_proc_stat_totals() -> Tuple[int, int]:
    """Return (total_jiffies, idle_jiffies) from /proc/stat."""
    line = Path("/proc/stat").read_text(encoding="utf-8").splitlines()[0]
    parts = [int(x) for x in line.split()[1:]]
    idle = parts[3] + (parts[4] if len(parts) > 4 else 0)
    total = sum(parts)
    return total, idle


def _sample_cpu_percent(prev_total: Optional[int], prev_idle: Optional[int]) -> Tuple[float, int, int]:
    """Compute host CPU usage since the previous procfs sample."""
    total, idle = _read_proc_stat_totals()
    if prev_total is None or prev_idle is None or total <= prev_total:
        return float("nan"), total, idle
    total_d = total - prev_total
    idle_d = idle - prev_idle
    busy = max(0, total_d - idle_d)
    cpu_pct = (100.0 * busy / total_d) if total_d > 0 else float("nan")
    return float(cpu_pct), total, idle


def _read_meminfo() -> Dict[str, float]:
    """Read host memory totals and usage percentages from /proc/meminfo."""
    vals: Dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, rest = line.split(":", 1)
        m = _re.search(r"(\d+)", rest)
        if m:
            vals[key.strip()] = int(m.group(1))

    total_kb = int(vals.get("MemTotal", 0))
    avail_kb = int(vals.get("MemAvailable", vals.get("MemFree", 0)))
    used_kb = max(0, total_kb - avail_kb)
    used_pct = (100.0 * used_kb / total_kb) if total_kb > 0 else float("nan")
    return {
        "mem_total_mb": total_kb / 1024.0,
        "mem_available_mb": avail_kb / 1024.0,
        "mem_used_mb": used_kb / 1024.0,
        "mem_used_pct": float(used_pct),
    }


def _read_loadavg() -> Tuple[float, float, float]:
    """Read 1, 5, and 15 minute host load averages."""
    try:
        a, b, c = os.getloadavg()
        return float(a), float(b), float(c)
    except Exception:
        raw = Path("/proc/loadavg").read_text(encoding="utf-8").split()
        return float(raw[0]), float(raw[1]), float(raw[2])


def resource_loop(
    *,
    out_csv: Path,
    service: str,
    attack_id: str,
    level: str,
    warmup: float,
    attack: float,
    cooldown: float,
    interval: float,
    stop_evt: threading.Event,
) -> None:
    """Collect local CPU usage, load average, and memory throughout the experiment.

    Note: this implementation measures resources on the local host where the CLI is
    running, which works well when the target web server is on the
    same experiment machine (for example, http://127.0.0.1:8080/).
    """
    t_start = time.time()
    _ensure_dir(out_csv.parent)
    prev_total: Optional[int] = None
    prev_idle: Optional[int] = None

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "service",
            "attack_id",
            "level",
            "phase",
            "t_epoch",
            "t_iso",
            "t_rel_s",
            "cpu_pct",
            "load1",
            "load5",
            "load15",
            "mem_used_pct",
            "mem_used_mb",
            "mem_available_mb",
            "mem_total_mb",
        ])
        while not stop_evt.is_set():
            now = time.time()
            t_rel = now - t_start
            ph = _phase_of(t_rel, warmup, attack, cooldown)
            if ph == "done":
                break

            cpu_pct, prev_total, prev_idle = _sample_cpu_percent(prev_total, prev_idle)
            load1, load5, load15 = _read_loadavg()
            mem = _read_meminfo()
            t_iso = datetime.fromtimestamp(now, tz=timezone.utc).isoformat()

            w.writerow([
                service,
                attack_id,
                level,
                ph,
                f"{now:.6f}",
                t_iso,
                f"{t_rel:.3f}",
                f"{cpu_pct:.3f}" if cpu_pct == cpu_pct else "",
                f"{load1:.3f}",
                f"{load5:.3f}",
                f"{load15:.3f}",
                f"{mem['mem_used_pct']:.3f}" if mem['mem_used_pct'] == mem['mem_used_pct'] else "",
                f"{mem['mem_used_mb']:.3f}",
                f"{mem['mem_available_mb']:.3f}",
                f"{mem['mem_total_mb']:.3f}",
            ])
            f.flush()
            time.sleep(interval)


def _parse_docker_bytes_mb(s: str) -> float:
    """Parse a Docker byte string, such as '1.5kB' or '300MiB', to MB."""
    m = _re.match(r"([\d.]+)\s*(B|kB|KiB|MB|MiB|GB|GiB)", s.strip())
    if not m:
        return float("nan")
    val = float(m.group(1))
    unit = m.group(2)
    mult = {
        "B": 1e-6, "kB": 1e-3, "KiB": 1024 / 1e6,
        "MB": 1.0, "MiB": 1048576 / 1e6,
        "GB": 1e3, "GiB": 1073741824 / 1e6,
    }
    return val * mult.get(unit, float("nan"))


def docker_stats_loop(
    *,
    container_name: str,
    out_csv: Path,
    warmup: float,
    attack: float,
    cooldown: float,
    stop_evt: threading.Event,
    poll_interval: float = 1.0,
) -> None:
    """Collect CPU/memory telemetry through `docker stats --no-stream`."""
    t_start = time.time()
    _ensure_dir(out_csv.parent)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "t_epoch", "t_iso", "t_rel_s", "phase",
            "cpu_pct", "mem_usage_mb", "mem_limit_mb", "mem_pct",
            "net_rx_mb", "net_tx_mb",
        ])
        while not stop_evt.is_set():
            now = time.time()
            t_rel = now - t_start
            ph = _phase_of(t_rel, warmup, attack, cooldown)
            if ph == "done":
                break
            try:
                res = subprocess.run(
                    ["docker", "stats", "--no-stream", "--format", "{{json .}}", container_name],
                    capture_output=True, text=True, timeout=5.0,
                )
                if res.returncode == 0 and res.stdout.strip():
                    d = json.loads(res.stdout.strip())
                    cpu_pct = float(d.get("CPUPerc", "0%").rstrip("%") or 0)
                    mem_raw = d.get("MemUsage", "0B / 0B")
                    mem_parts = (mem_raw + " / 0B").split(" / ")[:2]
                    mem_usage_mb = _parse_docker_bytes_mb(mem_parts[0])
                    mem_limit_mb = _parse_docker_bytes_mb(mem_parts[1])
                    mem_pct = float(d.get("MemPerc", "0%").rstrip("%") or 0)
                    net_raw = d.get("NetIO", "0B / 0B")
                    net_parts = (net_raw + " / 0B").split(" / ")[:2]
                    net_rx_mb = _parse_docker_bytes_mb(net_parts[0])
                    net_tx_mb = _parse_docker_bytes_mb(net_parts[1])
                    t_iso = datetime.fromtimestamp(now, tz=timezone.utc).isoformat()
                    w.writerow([
                        f"{now:.6f}", t_iso, f"{t_rel:.3f}", ph,
                        f"{cpu_pct:.2f}", f"{mem_usage_mb:.4f}", f"{mem_limit_mb:.4f}",
                        f"{mem_pct:.2f}", f"{net_rx_mb:.4f}", f"{net_tx_mb:.4f}",
                    ])
                    f.flush()
            except Exception:
                pass
            time.sleep(poll_interval)
