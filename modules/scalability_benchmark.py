#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import csv
import json
import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Optional
from urllib.request import urlopen


def run(cmd: list[str], timeout: Optional[float] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ensure_network(name: str) -> None:
    res = run(["docker", "network", "inspect", name])
    if res.returncode != 0:
        res = run(["docker", "network", "create", name])
        if res.returncode != 0:
            raise RuntimeError(res.stderr)


def remove_container(name: str) -> None:
    run(["docker", "rm", "-f", name])


def start_target(name: str, image: str, network: str, host_port: int) -> None:
    remove_container(name)
    res = run([
        "docker", "run", "-d", "--rm",
        "--name", name,
        "--network", network,
        "-p", f"127.0.0.1:{host_port}:80",
        image,
    ])
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip())


def wait_http(port: int, timeout_s: float = 10.0) -> bool:
    deadline = time.time() + timeout_s
    url = f"http://127.0.0.1:{port}/"
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1.0) as r:
                r.read(32)
            return True
        except Exception:
            time.sleep(0.2)
    return False


def probe_http(port: int) -> bool:
    try:
        with urlopen(f"http://127.0.0.1:{port}/", timeout=1.0) as r:
            r.read(32)
        return True
    except Exception:
        return False


def read_proc_cpu(pid: int) -> tuple[int, int]:
    # utime=14, stime=15 em /proc/<pid>/stat
    parts = Path(f"/proc/{pid}/stat").read_text().split()
    return int(parts[13]), int(parts[14])


def read_proc_rss_mb(pid: int) -> float:
    status = Path(f"/proc/{pid}/status").read_text().splitlines()
    for line in status:
        if line.startswith("VmRSS:"):
            kb = int(line.split()[1])
            return kb / 1024.0
    return float("nan")


def read_host_cpu() -> tuple[int, int]:
    parts = [int(x) for x in Path("/proc/stat").read_text().splitlines()[0].split()[1:]]
    idle = parts[3] + (parts[4] if len(parts) > 4 else 0)
    total = sum(parts)
    return total, idle


def read_host_mem() -> dict[str, float]:
    vals = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        if ":" not in line:
            continue
        k, rest = line.split(":", 1)
        nums = [x for x in rest.split() if x.isdigit()]
        if nums:
            vals[k] = int(nums[0])
    total = vals.get("MemTotal", 0)
    avail = vals.get("MemAvailable", vals.get("MemFree", 0))
    used = max(0, total - avail)
    return {
        "host_mem_used_mb": used / 1024.0,
        "host_mem_used_pct": (100.0 * used / total) if total else float("nan"),
    }


def cleanup(prefix: str, max_n: int) -> None:
    for i in range(1, max_n + 1):
        remove_container(f"{prefix}-{i:03d}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", default="1,5,10,20,30,40,50")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--duration", type=float, default=60.0)
    ap.add_argument("--image", default="nginx:alpine")
    ap.add_argument("--network", default="nsb-scale")
    ap.add_argument("--prefix", default="nsb-target")
    ap.add_argument("--base-port", type=int, default=18080)
    ap.add_argument("--sample-interval", type=float, default=1.0)
    ap.add_argument("--out", default="experiments/scalability")
    args = ap.parse_args()

    counts = [int(x) for x in args.counts.split(",") if x.strip()]
    max_n = max(counts)
    out = Path(args.out)
    raw_dir = out / "raw"
    table_dir = out / "tables"
    raw_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    ensure_network(args.network)

    raw_all_path = table_dir / "scalability_raw.csv"
    raw_exists = raw_all_path.exists()

    pid = os.getpid()
    clk_tck = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
    cpu_count = os.cpu_count() or 1

    try:
        with raw_all_path.open("a", newline="", encoding="utf-8") as fall:
            fieldnames = [
                "n_targets", "run_id", "phase", "t_epoch", "t_rel_s",
                "orchestrator_cpu_pct", "orchestrator_rss_mb",
                "host_cpu_pct", "host_mem_used_pct", "host_mem_used_mb",
                "probe_success_rate", "running_containers",
                "startup_time_s", "teardown_time_s",
            ]
            writer_all = csv.DictWriter(fall, fieldnames=fieldnames)
            if not raw_exists:
                writer_all.writeheader()

            for n in counts:
                for run_id in range(1, args.runs + 1):
                    print(f"[INFO] n={n} run={run_id}")

                    cleanup(args.prefix, max_n)

                    t0 = time.perf_counter()
                    failed = 0
                    for i in range(1, n + 1):
                        name = f"{args.prefix}-{i:03d}"
                        port = args.base_port + i
                        try:
                            start_target(name, args.image, args.network, port)
                        except Exception as e:
                            failed += 1
                            print(f"[WARN] failed to start {name}: {e}")

                    ready = 0
                    for i in range(1, n + 1):
                        port = args.base_port + i
                        if wait_http(port, timeout_s=10.0):
                            ready += 1

                    startup_time = time.perf_counter() - t0
                    print(f"[INFO] ready={ready}/{n} startup={startup_time:.2f}s")

                    sample_path = raw_dir / f"scale_{n:03d}_run{run_id:02d}_samples.csv"
                    with sample_path.open("w", newline="", encoding="utf-8") as fs:
                        writer = csv.DictWriter(fs, fieldnames=fieldnames)
                        writer.writeheader()

                        prev_proc_cpu = sum(read_proc_cpu(pid))
                        prev_host_total, prev_host_idle = read_host_cpu()
                        prev_wall = time.perf_counter()
                        steady_start = time.perf_counter()

                        while True:
                            now = time.perf_counter()
                            t_rel = now - steady_start
                            if t_rel >= args.duration:
                                break

                            ok = 0
                            for i in range(1, n + 1):
                                if probe_http(args.base_port + i):
                                    ok += 1
                            probe_success_rate = ok / n if n else 0.0

                            proc_cpu = sum(read_proc_cpu(pid))
                            host_total, host_idle = read_host_cpu()
                            wall = time.perf_counter()

                            proc_delta = proc_cpu - prev_proc_cpu
                            wall_delta = max(1e-9, wall - prev_wall)
                            orchestrator_cpu_pct = 100.0 * (proc_delta / clk_tck) / wall_delta

                            total_delta = host_total - prev_host_total
                            idle_delta = host_idle - prev_host_idle
                            host_cpu_pct = (
                                100.0 * max(0, total_delta - idle_delta) / total_delta
                                if total_delta > 0 else float("nan")
                            )

                            mem = read_host_mem()
                            row = {
                                "n_targets": n,
                                "run_id": run_id,
                                "phase": "steady",
                                "t_epoch": f"{time.time():.6f}",
                                "t_rel_s": f"{t_rel:.3f}",
                                "orchestrator_cpu_pct": f"{orchestrator_cpu_pct:.4f}",
                                "orchestrator_rss_mb": f"{read_proc_rss_mb(pid):.4f}",
                                "host_cpu_pct": f"{host_cpu_pct:.4f}",
                                "host_mem_used_pct": f"{mem['host_mem_used_pct']:.4f}",
                                "host_mem_used_mb": f"{mem['host_mem_used_mb']:.4f}",
                                "probe_success_rate": f"{probe_success_rate:.4f}",
                                "running_containers": ready - failed,
                                "startup_time_s": f"{startup_time:.4f}",
                                "teardown_time_s": "",
                            }

                            writer.writerow(row)
                            writer_all.writerow(row)
                            fall.flush()

                            prev_proc_cpu = proc_cpu
                            prev_host_total, prev_host_idle = host_total, host_idle
                            prev_wall = wall
                            time.sleep(args.sample_interval)

                    t1 = time.perf_counter()
                    cleanup(args.prefix, max_n)
                    teardown_time = time.perf_counter() - t1

                    meta = {
                        "n_targets": n,
                        "run_id": run_id,
                        "image": args.image,
                        "network": args.network,
                        "duration_s": args.duration,
                        "startup_time_s": startup_time,
                        "teardown_time_s": teardown_time,
                        "ready_targets": ready,
                        "failed_starts": failed,
                    }
                    (raw_dir / f"scale_{n:03d}_run{run_id:02d}_meta.json").write_text(
                        json.dumps(meta, indent=2),
                        encoding="utf-8",
                    )

                    print(f"[OK] n={n} run={run_id} teardown={teardown_time:.2f}s")

    finally:
        cleanup(args.prefix, max_n)

    print(f"[OK] raw data: {raw_all_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
