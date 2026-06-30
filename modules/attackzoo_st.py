import os
import csv
import ipaddress
import json
import shutil
import signal
import socket
import subprocess
import sys
import time
import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from modules.registry import CATEGORIES, AttackSpec, ParamSpec
from modules.runners import (
    docker_available,
    docker_container_status,
    docker_logs,
    docker_rm_force,
)
from modules.features import (
    FEATURES_DIR,
    TMP_DIR,
    build_feature_paths,
    extract_with_ntlflowlyzer,
    extract_with_tshark,
    extract_with_scapy,
)
from modules.datasets import build_dataset_unsupervised_for_capture

# -----------------------------
# Directories / Paths
# -----------------------------
CAPTURES_DIR = Path("captures")
FEATURES_DIR = Path("features")
DATASETS_DIR = Path("datasets")
TMP_DIR = Path(".tmp")

LOGS_DIR = Path("logs")
BENIGN_CLIENTS_LOG = LOGS_DIR / "benign_clients.log"
ATTACKS_LOG_PATH = LOGS_DIR / "attacks.log"
ATTACKS_LOG = LOGS_DIR / "attacks.log"
_ATTACKS_LOG_LOCK = threading.Lock()

def _ensure_logs_dir() -> None:
    """
    Ensures required directories exist.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def _append_attacks_log_line(line: str) -> None:
    """
    Appends attack logs to the end of logs/attacks.log.

    :param line: Log line
    :type line: str
    """
    _ensure_logs_dir()
    with _ATTACKS_LOG_LOCK:
        with ATTACKS_LOG.open("a", encoding="utf-8") as f:
            f.write(line.rstrip("\n") + "\n")

def _log_attack_event(event: str, **fields: Any) -> None:
    """
    Writes a labeled event to logs/attacks.log.

    :param event: _description_
    :type event: Additional log-line label
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parts: List[str] = []
    for k, v in fields.items():
        if v is None:
            continue
        parts.append(f"{k}={v}")
    _append_attacks_log_line(f"[{ts}] {event} " + " ".join(parts))

def start_attack_logs_watcher(
    container_ref: str,
    spec: AttackSpec,
    *,
    cmd: Optional[List[str]] = None,
    pcap_path: Optional[str] = None,
    max_runtime_s: Optional[int] = None,
    capture_enabled: bool = False,
) -> None:
    """
    Follows container logs and writes them to the attack log.

    :param container_ref: Container ID
    :type container_ref: str
    :param spec: Container specification
    :type spec: AttackSpec
    :param cmd: Command description, defaults to None
    :type cmd: Optional[List[str]], optional
    :param pcap_path: PCAP storage path, defaults to None
    :type pcap_path: Optional[str], optional
    :param max_runtime_s: Maximum runtime in seconds, defaults to None
    :type max_runtime_s: Optional[int], optional
    :param capture_enabled: Whether packet capture is enabled, defaults to False
    :type capture_enabled: bool, optional
    """

    def _worker() -> None:
        try:
            _log_attack_event(
                "ATTACK_START",
                attack_id=spec.id,
                container=spec.container_name,
                image=spec.image,
                max_runtime_s=max_runtime_s,
                capture=capture_enabled,
                pcap=pcap_path,
            )
            if cmd:
                _append_attacks_log_line(f"[{spec.id}|{spec.container_name}] CMD: " + " ".join(map(str, cmd)))

            p = subprocess.Popen(
                ["docker", "logs", "-f", "--timestamps", container_ref],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if p.stdout:
                for raw in iter(p.stdout.readline, b""):
                    if not raw:
                        break
                    line = raw.decode("utf-8", errors="replace").rstrip("\n")
                    _append_attacks_log_line(f"[{spec.id}|{spec.container_name}] {line}")
            try:
                p.wait(timeout=60 * 60 * 12)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        except Exception as e:
            _append_attacks_log_line(f"[{spec.id}|{spec.container_name}] [logs_watcher_error] {e}")

        exit_code: Optional[int] = None
        rc, out, _ = _run(["docker", "inspect", "-f", "{{.State.ExitCode}}", container_ref])
        if rc == 0:
            out = out.strip()
            if out.isdigit():
                exit_code = int(out)

        _log_attack_event(
            "ATTACK_END",
            attack_id=spec.id,
            container=spec.container_name,
            exit_code=exit_code,
        )
    threading.Thread(target=_worker, daemon=True).start()

def start_attack_timeout_watchdog(container_ref: str, spec: AttackSpec, max_runtime_s: int) -> None:
    """
    After `max_runtime_s`, force-removes the container with `docker rm -f` if it is still running.
    """

    def _worker() -> None:
        try:
            time.sleep(max_runtime_s)
            rc, out, _ = _run(["docker", "inspect", "-f", "{{.State.Running}}", container_ref])
            if rc == 0 and out.strip().lower() == "true":
                _log_attack_event(
                    "ATTACK_TIMEOUT",
                    attack_id=spec.id,
                    container=spec.container_name,
                    max_runtime_s=max_runtime_s,
                )
                rc2, out2, err2 = _run(["docker", "rm", "-f", container_ref])
                _append_attacks_log_line(
                    f"[{spec.id}|{spec.container_name}] [timeout_kill] rc={rc2} out={out2.strip()} err={err2.strip()}"
                )
        except Exception as e:
            _append_attacks_log_line(f"[{spec.id}|{spec.container_name}] [timeout_watchdog_error] {e}")

    if max_runtime_s and max_runtime_s > 0:
        threading.Thread(target=_worker, daemon=True).start()

def build_dataset_path_for_capture(pcap_path: Path) -> Path:
    """
    Maps captures to future dataset generation outputs using the same basename.

    :param pcap_path: Path to the .pcap file
    :type pcap_path: Path
    :return: Full dataset file path
    :rtype: Path
    """
    base = stem_no_ext(pcap_path)
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    return DATASETS_DIR / f"unsupervised-{base}.csv"

def _ensure_dirs() -> None:
    """
    Ensures output directories exist.
    """
    CAPTURES_DIR.mkdir(parents=True, exist_ok=True)
    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

def stem_no_ext(p: Path) -> str:
    """
    Example: recon_arp_scan-20260124_161958 (without .pcap)

    :param p: .pcap file path
    :type p: Path
    :return: .pcap filename without extension
    :rtype: str
    """
    return p.name[:-5] if p.name.lower().endswith(".pcap") else p.stem

def build_feature_paths(pcap_path: Path) -> Dict[str, Path]:
    """
    Maps captures to future feature extraction outputs using the same basename.

    :param pcap_path: Full PCAP path to map to future extraction outputs
    :type pcap_path: Path
    :return: Path dictionary for extraction tools
    :rtype: Dict[str, Path]
    """
    base = stem_no_ext(pcap_path)
    return {
        "ntlflowlyzer": FEATURES_DIR / f"ntlflowlyzer-{base}.csv",
        "tshark": FEATURES_DIR / f"tshark-{base}.csv",
        "scapy": FEATURES_DIR / f"scapy-{base}.csv",
    }

def build_capture_path(attack_id: str) -> Path:
    """
    Standardizes capture output paths.

    :param attack_id: Attack ID from the registry file
    :type attack_id: str
    :return: Full PCAP output path
    :rtype: Path
    """
    _ensure_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return CAPTURES_DIR / f"{attack_id}-{ts}.pcap"

def tool_exists(exe: str) -> bool:
    """
    Checks whether tools exist before they are called.

    :param exe: Binary name to check
    :type exe: str
    :return: True if the tool exists, otherwise False
    :rtype: bool
    """
    return shutil.which(exe) is not None

# -----------------------------------
# Command execution (binary-safe)
# -----------------------------------
def _run(cmd: List[str]) -> Tuple[int, str, str]:
    """
    Runs a command and returns (rc, stdout, stderr) without UnicodeDecodeError.
    Decodes bytes with UTF-8 errors='replace'.

    :param cmd: Command to run
    :type cmd: List[str]
    :return: Standard outputs
    :rtype: Tuple[int, str, str]
    """
    p = subprocess.run(cmd, capture_output=True)  # bytes
    stdout = (p.stdout or b"").decode("utf-8", errors="replace").strip()
    stderr = (p.stderr or b"").decode("utf-8", errors="replace").strip()
    return p.returncode, stdout, stderr

# -----------------------------
# Centralized logs: benign clients
# -----------------------------
_BENIGN_LOG_LOCK = threading.Lock()

def _ensure_logs_dir() -> None:
    """
    Ensures the logs/ directory exists.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def _append_benign_log(line: str) -> None:
    """
    Appends threaded logs to logs/benign_clients.log.

    :param line: Log line
    :type line: str
    """
    _ensure_logs_dir()
    if not line.endswith("\n"):
        line += "\n"
    with _BENIGN_LOG_LOCK:
        with BENIGN_CLIENTS_LOG.open("a", encoding="utf-8", errors="replace") as f:
            f.write(line)

def _log_event(event: str, **fields: Any) -> None:
    """
    Logs a single-line event with a timestamp.

    :param event: Event name
    :type event: str
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    extra = " ".join([f"{k}={v}" for k, v in fields.items() if v is not None and str(v) != ""])
    _append_benign_log(f"[{ts}] {event} {extra}".rstrip())

def tail_text_file(path: Path, n_lines: int = 400, max_bytes: int = 256 * 1024) -> str:
    """
    Reads approximately the last N lines from a text file, with a byte limit.

    :param path: Log file path
    :type path: Path
    :param n_lines: Number of lines to display, defaults to 400
    :type n_lines: int, optional
    :param max_bytes: Maximum bytes to display, defaults to 256*1024
    :type max_bytes: int, optional
    :return: Log text to display
    :rtype: str
    """
    if not path.exists():
        return ""
    try:
        data = path.read_bytes()
        if len(data) > max_bytes:
            data = data[-max_bytes:]
        txt = data.decode("utf-8", errors="replace")
        lines = txt.splitlines()
        return "\n".join(lines[-int(n_lines):])
    except Exception as e:
        return f"[error reading log file] {e}"

def start_benign_logs_watcher(container_ref: str, kind: str, *, container_name: Optional[str] = None, cmd: Optional[List[str]] = None) -> None:
    """
    Follows `docker logs -f --timestamps` and writes to logs/benign_clients.log.
    When it exits, or if it already exited, tries to record the exit_code and remove the container.

    :param container_ref: Container ID
    :type container_ref: str
    :param kind: Client kind
    :type kind: str
    :param container_name: Container name, defaults to None
    :type container_name: Optional[str], optional
    :param cmd: Execution command, defaults to None
    :type cmd: Optional[List[str]], optional
    """
    def _worker() -> None:
        ref = container_ref or (container_name or "")
        name = container_name or container_ref

        _log_event("BENIGN_CLIENT_START", kind=kind, name=name)
        if cmd:
            _append_benign_log(f"[{name}] cmd: {' '.join(cmd)}")

        logs_cmd = ["docker", "logs", "-f", "--timestamps", ref]

        try:
            p = subprocess.Popen(logs_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # stdout stream
            if p.stdout:
                for raw in iter(p.stdout.readline, b""):
                    if not raw:
                        break
                    line = raw.decode("utf-8", errors="replace").rstrip("\n")
                    _append_benign_log(f"[{name}] {line}")

            p.wait()

            err_bytes = b""
            if p.stderr:
                try:
                    err_bytes = p.stderr.read() or b""
                except Exception:
                    err_bytes = b""
            if err_bytes:
                _append_benign_log(f"[{name}] [docker-logs-stderr] {err_bytes.decode('utf-8', errors='replace').strip()}")

        except Exception as e:
            _append_benign_log(f"[{name}] [watcher-error] {e}")

        exit_code: Optional[str] = None
        rc2, out2, _ = _run(["docker", "wait", ref])
        if rc2 == 0 and out2.strip().isdigit():
            exit_code = out2.strip()
        else:
            rc3, out3, _ = _run(["docker", "inspect", "-f", "{{.State.ExitCode}}", ref])
            if rc3 == 0 and out3.strip().isdigit():
                exit_code = out3.strip()

        _log_event("BENIGN_CLIENT_END", kind=kind, name=name, exit_code=exit_code)

        # cleanup
        _run(["docker", "rm", "-f", name])

    threading.Thread(target=_worker, daemon=True).start()

def snapshot_benign_container_logs(names: List[str], kind: str) -> None:
    """
    Captures current logs (non-following) before removing containers.

    :param names: Container names
    :type names: List[str]
    :param kind: Client kind
    :type kind: str
    """
    if not names:
        return
    for name in names:
        _log_event("BENIGN_CLIENT_SNAPSHOT", kind=kind, name=name)
        rc, out, err = _run(["docker", "logs", "--timestamps", name])
        if out:
            for line in out.splitlines():
                _append_benign_log(f"[{name}] {line}")
        if err:
            _append_benign_log(f"[{name}] [docker-logs-stderr] {err}")


# Definitions for spawning benign clients

# RANDOM benign client (starts up to 10 numbered instances)
RANDOM_CLIENT_NAME_RE = re.compile(r"^client-random-?(\d{1,2})$")
RANDOM_CLIENT_IMAGE = "client-random:latest"
RANDOM_CLIENT_NAME_PREFIX = "client-random-"
RANDOM_CLIENT_MAX_RUNNING = 10

# SUPER benign client (parameterized; allows multiple numbered instances)
SUPER_CLIENT_NAME_RE = re.compile(r"^client-super-?(\d{1,2})$")
SUPER_CLIENT_FIXED_NAMES = {"client-super"}  # compatibility
SUPER_CLIENT_IMAGE = "client-super:latest"
SUPER_CLIENT_NAME_PREFIX = "client-super-"
SUPER_CLIENT_MAX_RUNNING = 10

def list_running_benign_clients() -> List[Tuple[str, int]]:
    """
    Returns [(container_name, n)] only for RUNNING containers whose name
    matches client-random-<N>.

    :return: List of running benign client containers
    :rtype: List[Tuple[str, int]]
    """
    if not docker_available():
        return []

    rc, out, _ = _run(["docker", "ps", "--format", "{{.Names}}"])
    if rc != 0:
        return []

    items: List[Tuple[str, int]] = []
    for name in out.splitlines():
        name = name.strip()
        m = RANDOM_CLIENT_NAME_RE.match(name)
        if m:
            items.append((name, int(m.group(1))))
    # Sort the simple list by number.
    items.sort(key=lambda x: x[1])
    return items

def next_benign_client_number(running_clients: List[Tuple[str, int]]) -> int:
    """
    Next number = (largest running number) + 1.
    If none exist, starts at 1.

    :param running_clients: List of running benign client containers
    :type running_clients: List[Tuple[str, int]]
    :return: Next benign client number
    :rtype: int
    """
    if not running_clients:
        return 1
    return max(n for _, n in running_clients) + 1

def remove_all_benign_clients(running_clients: List[Tuple[str, int]]) -> dict:
    """
    Runs docker rm -f for all running containers matching the prefix.
    :param running_clients: List of running benign client containers
    :type running_clients: List[Tuple[str, int]]
    :return: Execution status
    :rtype: dict
    """
    if not docker_available():
        return {"ok": False, "stderr": "Docker unavailable.", "cmd": []}

    if not running_clients:
        return {"ok": True, "stdout": "No clients to remove.", "cmd": []}

    names = [name for name, _ in running_clients]
    # Snapshot logs before removing containers.
    snapshot_benign_container_logs(names, "random")
    cmd = ["docker", "rm", "-f", *names]
    rc, out, err = _run(cmd)
    return {"ok": rc == 0, "stdout": out, "stderr": err, "cmd": cmd, "returncode": rc}

def start_one_benign_client(running_clients: List[Tuple[str, int]]) -> dict:
    """
    Spawns one benign client per button click, up to 10.
    docker run -d --rm --name client-random-1 client-random:latest \
        "<WEB_IP>" "<SSH_IP>" "<SMB_IP>" "<MQTT_IP>" "<COAP_IP>" "<TELNET_IP>" "<SSL_IP>"
    Enable only when count < 10 and all 7 servers are running.

    :param running_clients: List of running benign client containers
    :type running_clients: List[Tuple[str, int]]
    :return: Parameter dictionary for running benign client containers
    :rtype: dict
    """
    if not docker_available():
        return {"ok": False, "stderr": "Docker unavailable.", "cmd": []}

    # Remove benign containers left in Exited/Created/etc states to avoid name conflicts.
    purge_stale_benign_containers()

    if len(running_clients) >= RANDOM_CLIENT_MAX_RUNNING:
        return {"ok": False, "stderr": "The limit of 10 benign clients has already been reached.", "cmd": []}

    server_ips, missing = get_required_server_ips()
    if not server_ips:
        return {
            "ok": False,
            "stderr": f"Cannot start client: server(s) are not running or have no IP: {', '.join(missing)}",
            "cmd": [],
        }

    y = next_benign_client_number(running_clients)
    all_names = _all_container_names()
    name = f"{RANDOM_CLIENT_NAME_PREFIX}{y}"
    while name in all_names:
        y += 1
        name = f"{RANDOM_CLIENT_NAME_PREFIX}{y}"

    # 7 arguments in server order.
    cmd = ["docker", "run", "-d", "--rm", "--name", name, RANDOM_CLIENT_IMAGE, *server_ips]
    rc, out, err = _run(cmd)

    container_id = (out.strip().splitlines()[0] if out else "").strip()
    if rc == 0:
        start_benign_logs_watcher(container_id or name, "random", container_name=name, cmd=cmd)

    return {
        "ok": rc == 0,
        "stdout": out,
        "stderr": err,
        "cmd": cmd,
        "returncode": rc,
        "container_name": name,
        "server_ips": server_ips,
    }

def list_running_super_clients() -> List[Tuple[str, int]]:
    """
    Returns [(container_name, n)] only for RUNNING containers that are
    SUPER benign clients (parameterized).
    Accepts numbered names (client-super-<n> or without the hyphen) and the
    fixed compatibility name client-super.

    :return: List of running SUPER benign client containers
    :rtype: List[Tuple[str, int]]
    """
    if not docker_available():
        return []

    rc, out, _ = _run(["docker", "ps", "--format", "{{.Names}}"])
    if rc != 0:
        return []

    items: List[Tuple[str, int]] = []
    for name in out.splitlines():
        name = name.strip()
        if not name:
            continue
        if name in SUPER_CLIENT_FIXED_NAMES:
            items.append((name, 0))
            continue
        m = SUPER_CLIENT_NAME_RE.match(name)
        if m:
            items.append((name, int(m.group(1))))

    items.sort(key=lambda x: x[1])
    return items

# -----------------------------
# Automatic cleanup of stale benign containers
# -----------------------------
_BENIGN_RANDOM_RE = re.compile(rf"^{re.escape(RANDOM_CLIENT_NAME_PREFIX)}(\d{{1,2}})$")
_BENIGN_SUPER_RE = re.compile(rf"^{re.escape(SUPER_CLIENT_NAME_PREFIX)}(\d{{1,2}})$")

def _list_containers_by_regex(name_re: "re.Pattern") -> List[Tuple[str, str]]:
    """
    Returns [(name, status)] for containers from docker ps -a whose name matches name_re.

    :param name_re: Regular expression used to match names
    :type name_re: re.Pattern
    :return: Matched container list
    :rtype: List[Tuple[str, str]]
    """
    if not docker_available():
        return []
    rc, out, _ = _run(["docker", "ps", "-a", "--format", "{{.Names}}\t{{.Status}}"])
    if rc != 0:
        return []
    rows: List[Tuple[str, str]] = []
    for line in out.splitlines():
        if "\t" not in line:
            continue
        name, status = line.split("\t", 1)
        name = name.strip()
        status = status.strip()
        if name_re.match(name):
            rows.append((name, status))
    return rows

def _is_running_status(status: str) -> bool:
    """
    Checks whether a container status means it is running.

    :param status: status
    :type status: str
    :return: True or False
    :rtype: bool
    """
    s = (status or "").strip().lower()
    return s.startswith("up") or s.startswith("restarting") or s.startswith("paused")

def purge_stale_benign_containers() -> Dict[str, Any]:
    """
    Removes benign containers that are not running (Exited/Created/Dead/etc).
    Avoids name conflicts when the app restarts and old containers remain.

    :return: Dictionary with non-running clients selected for removal
    :rtype: Dict[str, Any]
    """
    removed: List[str] = []
    errors: List[str] = []

    for kind, name_re in [("random", _BENIGN_RANDOM_RE), ("super", _BENIGN_SUPER_RE)]:
        for name, status in _list_containers_by_regex(name_re):
            if _is_running_status(status):
                continue
            rc, out, err = _run(["docker", "rm", "-f", name])
            if rc == 0:
                removed.append(name)
                _log_event("cleanup_stale", kind=kind, container=name, status=status)
            else:
                errors.append(f"{name}: {err or out}".strip())

    return {"ok": len(errors) == 0, "removed": removed, "errors": errors}

def _all_container_names() -> set:
    """
    Returns all containers.

    :return: All container names
    :rtype: set
    """
    if not docker_available():
        return set()
    rc, out, _ = _run(["docker", "ps", "-a", "--format", "{{.Names}}"])
    if rc != 0:
        return set()
    return set(x.strip() for x in out.splitlines() if x.strip())

def next_super_client_number(running_clients: List[Tuple[str, int]]) -> int:
    """
    Next number = (largest running number) + 1.
    If no numbered containers exist, starts at 1.

    :param running_clients: List of running SUPER containers
    :type running_clients: List[Tuple[str, int]]
    :return: Next SUPER client number
    :rtype: int
    """
    nums = [n for _, n in running_clients if n and n > 0]
    return (max(nums) + 1) if nums else 1

def remove_all_super_clients(running_clients: List[Tuple[str, int]]) -> dict:
    """
    Runs docker rm -f for all running SUPER containers.

    :param running_clients: List of running SUPER containers
    :type running_clients: List[Tuple[str, int]]
    :return: Execution status
    :rtype: dict
    """
    if not docker_available():
        return {"ok": False, "stderr": "Docker unavailable.", "cmd": []}

    if not running_clients:
        return {"ok": True, "stdout": "No SUPER clients to remove.", "cmd": []}

    names = [name for name, _ in running_clients]
    # Snapshot logs before removing containers.
    snapshot_benign_container_logs(names, "super")
    cmd = ["docker", "rm", "-f", *names]
    rc, out, err = _run(cmd)
    return {"ok": rc == 0, "stdout": out, "stderr": err, "cmd": cmd, "returncode": rc}

def start_one_super_client(
    service: str,
    target_ip: str,
    target_port: int,
    max_accesses: int,
    interval_s: int,
    max_total_s: int,
    running_clients: Optional[List[Tuple[str, int]]] = None,
) -> dict:
    """
    Spawns a SUPER benign client (parameterized) in detached mode with --rm.

    Example:
      docker run -d --rm --name client-super-1 client-super:latest web 172.17.0.2 443 10 1 15

    :return: Dictionary with status and executed command
    :rtype: dict
    """
    if not docker_available():
        return {"ok": False, "stderr": "Docker unavailable.", "cmd": []}

    # Remove benign containers left in Exited/Created/etc states to avoid name conflicts.
    purge_stale_benign_containers()

    # Recalculate the list after cleanup to avoid stale containers.
    running_clients = list_running_super_clients()
    if len(running_clients) >= SUPER_CLIENT_MAX_RUNNING:
        return {"ok": False, "stderr": "The SUPER client limit has already been reached.", "cmd": []}

    n = next_super_client_number(running_clients)
    all_names = _all_container_names()
    name = f"{SUPER_CLIENT_NAME_PREFIX}{n}"
    while name in all_names:
        n += 1
        name = f"{SUPER_CLIENT_NAME_PREFIX}{n}"

    cmd = [
        "docker", "run", "-d", "--rm",
        "--name", name,
        SUPER_CLIENT_IMAGE,
        str(service).strip(),
        str(target_ip).strip(),
        str(int(target_port)),
        str(int(max_accesses)),
        str(int(interval_s)),
        str(int(max_total_s)),
    ]

    rc, out, err = _run(cmd)
    container_id = (out.strip().splitlines()[0] if out else "").strip()
    if rc == 0:
        start_benign_logs_watcher(container_id or name, "super", container_name=name, cmd=cmd)
    return {
        "ok": rc == 0,
        "stdout": out,
        "stderr": err,
        "cmd": cmd,
        "returncode": rc,
        "container_name": name,
    }

# -------------------------------------------
# Sidebar: Servers and Server Logs
# -------------------------------------------

# Server specifications to display in the sidebar
SERVER_SPECS = [
    ("Web Server", "server-http-server"),
    ("SSH Server", "server-ssh-server"),
    ("SMB Server", "server-smb-server"),
    ("MQTT Broker", "server-mqtt-broker"),
    ("CoAP Server", "server-coap-server"),
    ("XRCE-DDS Agent", "server-xrce-dds-agent"),
    ("Zenoh Router", "server-zenoh-router"),
    ("Telnet Server", "server-telnet-server"),
    ("SSL Heartbleed", "server-ssl-heartbleed"),
]

BENIGN_CLIENT_SERVER_ORDER = [
    ("WEB",    "server-http-server"),
    ("SSH",    "server-ssh-server"),
    ("SMB",    "server-smb-server"),
    ("MQTT",   "server-mqtt-broker"),
    ("COAP",   "server-coap-server"),
    ("TELNET", "server-telnet-server"),
    ("SSL",    "server-ssl-heartbleed"),
]

# Server log specifications
SERVER_LOG_SPECS: Dict[str, Dict[str, Any]] = {
    "server-coap-server": {"mode": "docker_logs"},
    "server-http-server": {"mode": "docker_logs"},
    "server-mqtt-broker": {"mode": "docker_logs"},
    "server-smb-server": {"mode": "exec_sh", "sh": "/var/log/samba/*"},
    "server-ssh-server": {"mode": "exec_sh", "sh": "/var/log/auth.log"},
    "server-ssl-heartbleed": {"mode": "exec_sh", "sh": "/var/log/access.log"},
    "server-xrce-dds-agent": {"mode": "docker_logs"},
    "server-zenoh-router": {"mode": "docker_logs"},
    "server-telnet-server": {
        "mode": "exec_sh",
        "sh": "/var/log/wtmp",
        "binary": True,
        "binary_hint": "The /var/log/wtmp file is binary; Tail raw mode may be unreadable.",
        "alt_label": "Use last",
        "alt_sh": 'command -v last >/dev/null 2>&1 && last -f /var/log/wtmp || echo "The last command is not available in the container."',
    },
}

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="Attack Testbed (Streamlit)", layout="wide")
st.title("Attack Testbed")
st.caption(
    "Select a category and an attack. Fill in the parameters when applicable "
    "and click Start attack to run it through Docker."
)

# Small visual adjustments for the on-screen controls.
st.markdown(
    '''
    <style>
    section[data-testid="stSidebar"] button[kind="secondary"],
    section[data-testid="stSidebar"] button[kind="primary"] {
        padding-top: 0.15rem !important;
        padding-bottom: 0.15rem !important;
        min-height: 1.6rem !important;
        line-height: 1.2rem !important;
        font-size: 0.85rem !important;
    }
    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 0.2rem !important;
    }
    </style>
    ''',
    unsafe_allow_html=True,
)

# Persistent state for the latest attack output
if "last_attack_result" not in st.session_state:
    st.session_state["last_attack_result"] = {}
if "view" not in st.session_state:
    st.session_state["view"] = "main"

# -----------------------------
# Docker helpers (inspect/list)
# -----------------------------

_MITRE_PATH_RE = re.compile(
    r"/(?P<kind>techniques|tactics)/(?P<id>[^/?#]+(?:/[^/?#]+)?)",
    re.IGNORECASE,
)

def normalize_mitre(mitre: Optional[Union[str, List[str]]]) -> List[str]:
    """
    Normalizes MITRE ATT&CK reference links.

    :param mitre: Technique description
    :type mitre: Optional[Union[str, List[str]]]
    :return: Technique list
    :rtype: List[str]
    """
    if not mitre:
        return []
    if isinstance(mitre, str):
        return [mitre]
    return [m for m in mitre if isinstance(m, str) and m.strip()]

def mitre_label_from_url(url: str) -> str:
    """
    Extracts the label after 'techniques/' or 'tactics/'.
    Ex.:
      .../techniques/T1595/003/ -> T1595/003
      .../techniques/T1018/     -> T1018
      .../tactics/TA0007/       -> TA0007
    """
    m = _MITRE_PATH_RE.search(url)
    if not m:
        return url.rstrip("/")

    label = m.group("id").rstrip("/")
    return label

def render_mitre_links(mitre: Optional[Union[str, List[str]]]) -> None:
    """
    Retorna lista de URLs

    :param mitre: Lista de URLs
    :type mitre: Optional[Union[str, List[str]]]
    """
    urls = normalize_mitre(mitre)
    if not urls:
        return

    parts = []
    for u in urls:
        label = mitre_label_from_url(u)
        parts.append(f'<a href="{u}" target="_blank"><code>{label}</code></a>')

    st.markdown("MITRE ATT&CK categories: " + " ".join(parts), unsafe_allow_html=True)

def normalize_tools(tools: Optional[List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """
    Accepts two formats:
    [{"name": "Python", "url": "https://..."}]
    [{"Python": "https://..."}, {"Streamlit": "https://..."}]
    Normalizes to a list of {"name":..., "url":...}.

    :param tools: Tool names and URLs
    :type tools: Optional[List[Dict[str, str]]]
    :return: Data in the format expected by the renderer
    :rtype: List[Dict[str, str]]
    """
    if not tools:
        return []

    norm: List[Dict[str, str]] = []
    for item in tools:
        if not isinstance(item, dict) or not item:
            continue

        if "name" in item and "url" in item:
            name = str(item.get("name", "")).strip()
            url = str(item.get("url", "")).strip()
            if name and url:
                norm.append({"name": name, "url": url})
            continue

        if len(item) == 1:
            name, url = next(iter(item.items()))
            name = str(name).strip()
            url = str(url).strip()
            if name and url:
                norm.append({"name": name, "url": url})
            continue
    return norm

def render_tools_links(tools: Optional[List[Dict[str, str]]]) -> None:
    """
    Renders tool names registered in the specifications.

    :param tools: List of Name : URL dictionaries
    :type tools: Optional[List[Dict[str, str]]]
    """
    items = normalize_tools(tools)
    if not items:
        return

    parts = []
    for it in items:
        name = it["name"]
        url = it["url"]
        parts.append(f'<a href="{url}" target="_blank"><code>{name}</code></a>')

    st.markdown("Tools: " + " ".join(parts), unsafe_allow_html=True)

def _container_ids_by_ancestor(image: str) -> List[str]:
    """
    Finds the actual container ID associated with an image.

    :param image: Image name to search for
    :type image: str
    :return: List of containers associated with the image
    :rtype: List[str]
    """
    rc, out, _ = _run(["docker", "ps", "-a", "-q", "--filter", f"ancestor={image}"])
    ids = [x for x in out.splitlines() if x.strip()] if rc == 0 else []

    if not ids and ":" not in image:
        rc, out, _ = _run(["docker", "ps", "-a", "-q", "--filter", f"ancestor={image}:latest"])
        ids = [x for x in out.splitlines() if x.strip()] if rc == 0 else []
    return ids

def _inspect(cont_id: str) -> Optional[dict]:
    """
    Runs docker container inspect to extract display data.

    :param cont_id: Container ID to inspect
    :type cont_id: str
    :return: Returned parameter dictionary
    :rtype: Optional[dict]
    """
    rc, out, _ = _run(["docker", "inspect", cont_id])
    if rc != 0 or not out:
        return None
    try:
        data = json.loads(out)
        return data[0] if data else None
    except Exception:
        return None

def _extract_ips(inspected: dict) -> Dict[str, str]:
    """
    Parses inspect output to get the container IP.

    :param inspected: Inspection parameter dictionary
    :type inspected: dict
    :return: Dictionary with the container IP(s)
    :rtype: Dict[str, str]
    """
    ips: Dict[str, str] = {}
    nets = (inspected.get("NetworkSettings") or {}).get("Networks") or {}
    for net_name, net_data in nets.items():
        ip = (net_data or {}).get("IPAddress") or ""
        if ip:
            ips[net_name] = ip
    return ips

def _pick_preferred_container(container_ids: List[str]) -> Optional[str]:
    """
    Selects the exact container.

    :param container_ids: Container IDs to select from
    :type container_ids: List[str]
    :return: Container ID real
    :rtype: Optional[str]
    """
    if not container_ids:
        return None
    for cid in container_ids:
        inspected = _inspect(cid)
        if not inspected:
            continue
        status = ((inspected.get("State") or {}).get("Status") or "").lower()
        if status == "running":
            return cid
    return container_ids[0]

def _get_preferred_container_id_by_ancestor(image_base: str) -> Optional[str]:
    """
    Selects the exact container by image name.

    :param image_base: Image name
    :type image_base: str
    :return: Returned container IDs
    :rtype: Optional[str]
    """
    ids = _container_ids_by_ancestor(image_base)
    return _pick_preferred_container(ids)

def get_running_container_id_by_ancestor(image_base: str) -> Optional[str]:
    """
    Returns the container_id for a RUNNING container whose ancestor is image_base or image_base:latest.

    :param image_base: Image name
    :type image_base: str
    :return: Returned container IDs
    :rtype: Optional[str]
    """
    if not docker_available():
        return None

    # 1) Try with :latest.
    rc, out, _ = _run(["docker", "ps", "--filter", f"ancestor={image_base}:latest", "--format", "{{.ID}}"])
    ids = [x.strip() for x in out.splitlines() if x.strip()]
    if rc == 0 and ids:
        return ids[0]

    # 2) Try without :latest.
    rc, out, _ = _run(["docker", "ps", "--filter", f"ancestor={image_base}", "--format", "{{.ID}}"])
    ids = [x.strip() for x in out.splitlines() if x.strip()]
    if rc == 0 and ids:
        return ids[0]

    return None

def get_container_ip_by_id(cid: str) -> Optional[str]:
    """
    Container IP (bridge). If there are multiple networks, returns the first IP found.

    :param cid: ID do container
    :type cid: str
    :return: IP address as a string
    :rtype: Optional[str]
    """
    if not cid:
        return None
    rc, out, err = _run([
        "docker", "inspect",
        "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}",
        cid
    ])
    if rc != 0:
        return None
    ips = [x for x in out.strip().split() if x]
    return ips[0] if ips else None

def get_required_server_ips() -> Tuple[Optional[List[str]], List[str]]:
    """
    Returns (ordered_ips, missing_labels).
    missing_labels contains the "WEB/SSH/..." entries that are not running or have no IP.

    :return: Server IP addresses
    :rtype: Tuple[Optional[List[str]], List[str]]
    """
    missing: List[str] = []
    ips: List[str] = []

    for label, image_base in BENIGN_CLIENT_SERVER_ORDER:
        cid = get_running_container_id_by_ancestor(image_base)
        if not cid:
            missing.append(label)
            continue
        ip = get_container_ip_by_id(cid)
        if not ip:
            missing.append(label)
            continue
        ips.append(ip)

    if missing:
        return None, missing
    return ips, []

# -----------------------------
# Server logs (view)
# -----------------------------
def fetch_server_logs(image_base: str, tail_lines: int = 200, prefer_alt: bool = False) -> Dict[str, Any]:
    """
    Fetches logs from a server.

    :param image_base: Image name
    :type image_base: str
    :param tail_lines: Number of log lines to return, defaults to 200
    :type tail_lines: int, optional
    :param prefer_alt: Alternative method for binary logs, defaults to False
    :type prefer_alt: bool, optional
    :return: Standard log output for display
    :rtype: Dict[str, Any]
    """
    if not docker_available():
        return {"ok": False, "mode": "error", "cmd_display": "", "stdout": "", "stderr": "Docker unavailable.", "returncode": 1}

    cid = _get_preferred_container_id_by_ancestor(image_base)
    if not cid:
        return {"ok": False, "mode": "error", "cmd_display": "", "stdout": "", "stderr": f"Container not found for ancestor={image_base}.", "returncode": 1}

    spec = SERVER_LOG_SPECS.get(image_base, {"mode": "docker_logs"})
    mode = spec.get("mode", "docker_logs")
    tail_lines = max(1, min(int(tail_lines), 5000))

    if mode == "docker_logs":
        cmd = ["docker", "logs", "--tail", str(tail_lines), cid]
        rc, out, err = _run(cmd)
        return {"ok": rc == 0, "mode": mode, "cmd_display": " ".join(cmd), "stdout": out, "stderr": err, "returncode": rc}

    if mode == "exec_sh":
        if prefer_alt and spec.get("alt_sh"):
            sh_cmd = f"{spec['alt_sh']} | head -n {tail_lines}"
            cmd = ["docker", "exec", cid, "sh", "-lc", sh_cmd]
            rc, out, err = _run(cmd)
            return {"ok": True, "mode": mode, "cmd_display": " ".join(cmd), "stdout": out, "stderr": err, "returncode": rc}

        files_expr = spec.get("sh", "")
        sh_cmd = f"tail -n {tail_lines} {files_expr} 2>/dev/null || true"
        cmd = ["docker", "exec", cid, "sh", "-lc", sh_cmd]
        rc, out, err = _run(cmd)
        return {"ok": True, "mode": mode, "cmd_display": " ".join(cmd), "stdout": out, "stderr": err, "returncode": rc}

    return {"ok": False, "mode": "error", "cmd_display": "", "stdout": "", "stderr": f"Unknown log mode: {mode}", "returncode": 1}

def _clip_text(s: str, max_chars: int = 120_000) -> str:
    """
    Defines the maximum text output length.

    :param s: Returned string values
    :type s: str
    :param max_chars: Maximum characters for a single return value, defaults to 120,000 characters
    :type max_chars: int, optional
    :return: Text output truncated at 120,000 characters when needed
    :rtype: str
    """
    if not s:
        return s
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + "\n\n[output truncated: character limit exceeded]"

def render_server_logs_view() -> None:
    """
    Streamlit functions that build the log viewer module.
    """
    label = st.session_state.get("server_logs_label", "")
    image_base = st.session_state.get("server_logs_image_base", "")
    st.subheader(f"Server logs: {label}")

    if "server_logs_tail" not in st.session_state:
        st.session_state["server_logs_tail"] = 200

    spec = SERVER_LOG_SPECS.get(image_base, {})
    has_alt = bool(spec.get("alt_sh"))
    is_binary = bool(spec.get("binary"))

    top = st.columns([1, 1, 2])
    if top[0].button("Back"):
        st.session_state["view"] = "main"
        st.rerun()

    tail_lines = top[2].number_input("Tail (lines)", min_value=1, max_value=5000, value=int(st.session_state["server_logs_tail"]), step=50)
    st.session_state["server_logs_tail"] = int(tail_lines)

    if top[1].button("Refresh logs"):
        st.rerun()

    prefer_alt = False
    if is_binary:
        st.warning(spec.get("binary_hint", "This log may be binary and the output may be unreadable."))
        if has_alt:
            mode_choice = st.radio("Read mode", options=["Tail raw", spec.get("alt_label", "Alternative")], horizontal=True, index=0, key="server_logs_mode_choice")
            prefer_alt = (mode_choice != "Tail raw")
            if not prefer_alt:
                st.error("This log cannot be displayed in Tail raw mode because it is binary. Use the alternative mode.")
                return

    result = fetch_server_logs(image_base, tail_lines=int(tail_lines), prefer_alt=prefer_alt)

    st.caption("Executed command:")
    st.code(result.get("cmd_display", ""), language="bash")

    out = _clip_text(result.get("stdout", ""))
    err = _clip_text(result.get("stderr", ""))

    if out:
        st.code(out, language="text")
    else:
        st.write("No log output.")

    if err:
        with st.expander("stderr", expanded=False):
            st.code(err, language="text")


def render_attacks_logs_view() -> None:
    """
    Renders the attack log view.
    """
    st.subheader("Consolidated attack logs")

    top = st.columns([1, 1, 3])
    if top[0].button("Back"):
        st.session_state["view"] = "main"
        st.rerun()
    if top[1].button("Refresh"):
        st.rerun()

    path = ATTACKS_LOG_PATH
    if not path.exists():
        st.info(f'No log found at "{path}".')
        return

    # logs/attacks.log download button
    with open(path, "rb") as f:
        st.download_button(
            "Download attacks.log",
            data=f,
            file_name=path.name,
            mime="text/plain",
            use_container_width=False,
            key="dl_attacks_log",
        )

    st.divider()

    c1, c2, c3 = st.columns([1.2, 1.2, 2.6], gap="small")
    tail_n = c1.number_input("Last lines", min_value=50, max_value=5000, value=300, step=50, key="att_log_tail_n")
    auto = c2.checkbox("Auto-refresh", value=False, key="att_log_auto")
    query = c3.text_input("Filter (contains)", value="", key="att_log_filter").strip().lower()

    try:
        # Reads the whole file (usually fine), tails it, and filters it.
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()

        # Tail first (faster).
        lines = lines[-int(tail_n):]

        # Filter
        if query:
            lines = [ln for ln in lines if query in ln.lower()]

        st.caption(f"Displaying {len(lines)} line(s).")
        st.text_area("attacks.log", value="\n".join(lines), height=520, key="att_log_text", disabled=True)

    except Exception as e:
        st.error("Failed to read the log file.")
        st.code(str(e), language="text")

    # Simple auto-refresh attempt.
    if auto:
        time.sleep(1)
        st.rerun()

# -----------------------------
# Benign clients (view)
# -----------------------------
def _render_last_client_action() -> None:
    """
    Renders information from the latest execution.
    """
    res = st.session_state.get("last_client_action")
    if not res:
        return
    st.markdown("### Last action")
    if res.get("ok"):
        st.success(res.get("title", "Action completed successfully."))
    else:
        st.error(res.get("title", "Action failed."))
    if res.get("cmd"):
        st.caption("Executed command:")
        st.code(" ".join(res["cmd"]), language="bash")
    if res.get("stdout"):
        with st.expander("stdout", expanded=False):
            st.code(res["stdout"], language="text")
    if res.get("stderr"):
        with st.expander("stderr", expanded=False):
            st.code(res["stderr"], language="text")

def render_benign_clients_view() -> None:
    """
    Renders the benign client control view.
    """
    st.subheader("Benign Client Control")

    top = st.columns([1, 1, 3])
    if top[0].button("Back"):
        st.session_state["view"] = "main"
        st.rerun()
    if top[1].button("Refresh"):
        st.rerun()

    if not docker_available():
        st.error("Docker is unavailable on the Streamlit host.")
        return

    tabs = st.tabs(["Random-access client", "Parameterized client"])

    # -------------------------
    # Random client
    # -------------------------
    with tabs[0]:
        running = list_running_benign_clients()
        x = len(running)

        server_ips, missing = get_required_server_ips()
        servers_ok = (server_ips is not None)

        st.write(f"Running clients (random access): **{x}**")
        if not servers_ok:
            st.warning(
                "Cannot start new random clients: "
                f"server(s) are not running or have no IP: {', '.join(missing)}"
            )

        remove_disabled = (x == 0) or (not docker_available())
        start_disabled = (x >= RANDOM_CLIENT_MAX_RUNNING) or (not docker_available()) or (not servers_ok)

        c1, c2 = st.columns([1, 1], gap="small")
        if c1.button("Remove all clients (random access)", disabled=remove_disabled, type="secondary", use_container_width=True):
            res = remove_all_benign_clients(running)
            res["title"] = "Random clients removed." if res.get("ok") else "Failed to remove random clients."
            st.session_state["last_client_action"] = res
            st.rerun()

        if c2.button("Start one client (random access)", disabled=start_disabled, type="primary", use_container_width=True):
            res = start_one_benign_client(running)
            res["title"] = f"Started: {res.get('container_name')}" if res.get("ok") else "Failed to start random client."
            st.session_state["last_client_action"] = res
            st.rerun()

        if running:
            with st.expander("View running containers (random)", expanded=False):
                st.write(", ".join(name for name, _ in running))
        _render_last_client_action()

        st.divider()
        st.caption("**Random-access client**: Starts a container that makes simple requests to target server services in random order and at a random interval between 1 and 5 seconds.")
        st.caption("**Parameterized client**: Starts a container against a specific target server and generates simple requests at the configured interval for the configured duration.")

    # -------------------------
    # Parameterized client
    # -------------------------
    with tabs[1]:
        running = list_running_super_clients()
        x = len(running)

        st.write(f"Running (parameterized): **{x}**")

        c1, c2 = st.columns([1, 1], gap="small")
        remove_disabled = (x == 0) or (not docker_available())

        if c1.button("Remove all clients (parameterized)", disabled=remove_disabled, type="secondary", use_container_width=True):
            res = remove_all_super_clients(running)
            res["title"] = "Parameterized clients removed." if res.get("ok") else "Failed to remove parameterized clients."
            st.session_state["last_client_action"] = res
            st.rerun()

        # Parameterized client form
        st.markdown("### Run parameterized client")
        rows = get_servers_status()
        ip_map_local = {r["Server"]: r["IP"] for r in rows}

        SUPER_SERVICE_SPECS: Dict[str, Dict[str, Any]] = {
            "web": {
                "label": "WEB (HTTP/HTTPS)",
                "desc": "curl performs a GET against httpx://aaa.bbb.ccc.ddd/ (HTTPS if port=443, otherwise HTTP). Defaults: 80/443.",
                "default_port": 80,
                "server_label": "Web Server",
            },
            "smb": {
                "label": "SMB",
                "desc": "smbclient -L //aaa.bbb.ccc.ddd lists shares while trying random credentials. Default: 445.",
                "default_port": 445,
                "server_label": "SMB Server",
            },
            "ssh": {
                "label": "SSH",
                "desc": "paramiko tries to open an SSH session against aaa.bbb.ccc.ddd with random credentials (1s timeout). Default: 22.",
                "default_port": 22,
                "server_label": "SSH Server",
            },
            "rdp": {
                "label": "RDP",
                "desc": "xfreerdp tries authentication (+auth-only) against aaa.bbb.ccc.ddd with random credentials (1s timeout). Default: 3389.",
                "default_port": 3389,
            },
            "telnet": {
                "label": "TELNET",
                "desc": "TCP connection sending simple random username/password data to aaa.bbb.ccc.ddd. Default: 23.",
                "default_port": 23,
                "server_label": "Telnet Server",
            },
            "smtp": {
                "label": "SMTP",
                "desc": "TCP, EHLO, AUTH LOGIN attempt with random credentials, QUIT. Default: 25.",
                "default_port": 25,
            },
            "imap": {
                "label": "IMAP",
                "desc": "TCP, LOGIN user pass, LOGOUT. Default: 143.",
                "default_port": 143,
            },
            "pop3": {
                "label": "POP3",
                "desc": "TCP, USER/PASS, QUIT. Default: 110.",
                "default_port": 110,
            },
            "ftp": {
                "label": "FTP",
                "desc": "TCP, USER/PASS, QUIT. Default: 21.",
                "default_port": 21,
            },
            "dns": {
                "label": "DNS",
                "desc": "dig @aaa.bbb.ccc.ddd -p PORT example.com A with +time=1 +tries=1. Default: 53.",
                "default_port": 53,
            },
            "snmp": {
                "label": "SNMP",
                "desc": "snmpget v2c on sysUpTime.0 with a random community, -t 1 -r 0. Default: 161.",
                "default_port": 161,
            },
            "sip": {
                "label": "SIP",
                "desc": "Sends OPTIONS over UDP (minimal SIP) and waits up to 1s for a response. Defaults: 5060 (without TLS) and 5061 (TLS).",
                "default_port": 5060,
            },
            "coap": {
                "label": "CoAP",
                "desc": "coap-client -m get coap://aaa.bbb.ccc.ddd:PORT/.well-known/core. Default: 5683.",
                "default_port": 5683,
                "server_label": "CoAP Server",
            },
            "mqtt": {
                "label": "MQTT",
                "desc": "mosquitto_pub publishes to a random topic with random user/pass values. Default: 1883.",
                "default_port": 1883,
                "server_label": "MQTT Broker",
            },
            "zenoh": {
                "label": "Zenoh-Pico (Zenoh)",
                "desc": "Lightweight connectivity attempt (TCP connect; UDP probe fallback). Common TCP: 7447. UDP multicast scouting example: 7446.",
                "default_port": 7447,
                "server_label": "Zenoh Router",
            },
            "xrce-dds": {
                "label": "XRCE-DDS (Micro XRCE-DDS)",
                "desc": "Sends a benign UDP probe datagram to the agent. Common agent port: 8888/UDP.",
                "default_port": 8888,
                "server_label": "XRCE-DDS Agent",
            },
        }

        service_keys = list(SUPER_SERVICE_SPECS.keys())

        from functools import partial

        def _super_apply_defaults(ip_map_local: dict) -> None:
            """
            Applies default values when declared.

            :param ip_map_local: Default-value dictionary
            :type ip_map_local: dict
            """
            svc = st.session_state.get("super_svc")
            if not svc:
                return

            spec = SUPER_SERVICE_SPECS[svc]

            # Update the default port whenever the service changes.
            st.session_state["super_port"] = int(spec["default_port"])

            # Suggest an IP only when a mapped server_label exists.
            server_label = spec.get("server_label", "")
            suggested_ip = ip_map_local.get(server_label, "") or ""
            if suggested_ip == "-":
                suggested_ip = ""
            if suggested_ip and not (st.session_state.get("super_ip") or "").strip():
                st.session_state["super_ip"] = suggested_ip

        svc = st.selectbox(
            "Service",
            service_keys,
            index=0,
            format_func=lambda k: SUPER_SERVICE_SPECS[k]["label"],
            key="super_svc",
            on_change=partial(_super_apply_defaults, ip_map_local),
        )

        st.info(SUPER_SERVICE_SPECS[svc]["desc"])
        if "super_port" not in st.session_state:
            st.session_state["super_port"] = int(SUPER_SERVICE_SPECS[svc]["default_port"])

        with st.form("super_client_form", clear_on_submit=False):
            ip = st.text_input("IP or FQDN", key="super_ip", placeholder="172.17.0.x")
            port = st.number_input("Port", min_value=1, max_value=65535, step=1, key="super_port")

            max_access = st.number_input("Maximum accesses (safeguard if there is no interval between requests)", min_value=1, max_value=10_000_000, value=9999, step=1)
            interval_s = st.number_input("Interval between accesses (s)", min_value=0, max_value=86_400, value=1, step=1)
            max_total_s = st.number_input("Total client runtime (s)", min_value=1, max_value=86_400, value=15, step=1)

            submitted = st.form_submit_button(
                "Start parameterized client",
                type="primary",
                disabled=(x >= SUPER_CLIENT_MAX_RUNNING),
            )

        if submitted:
            errs = []
            if not ip or not validate_ip_or_fqdn(ip, allow_single_label=False):
                errs.append('Invalid "IP" field (IP or FQDN).')
            if not validate_port(int(port)):
                errs.append('Invalid "Port" field (1-65535).')
            if int(max_access) < 1:
                errs.append('Invalid "Maximum accesses" field.')
            if int(interval_s) < 0:
                errs.append('Invalid "Interval" field.')
            if int(max_total_s) < 1:
                errs.append('Invalid "Maximum total runtime" field.')
            if errs:
                for e in errs:
                    st.error(e)
            else:
                res = start_one_super_client(
                    service=svc,
                    target_ip=ip,
                    target_port=int(port),
                    max_accesses=int(max_access),
                    interval_s=int(interval_s),
                    max_total_s=int(max_total_s),
                    running_clients=running,
                )
                res["title"] = f"Started: {res.get('container_name')}" if res.get("ok") else "Failed to start parameterized client."
                st.session_state["last_client_action"] = res
                st.rerun()

        if running:
            with st.expander("View running containers (parameterized)", expanded=False):
                st.write(", ".join(name for name, _ in running))

        _render_last_client_action()

        st.divider()
        st.caption("**Random-access client**: Starts a container that makes simple requests to target server services in random order and at a random interval between 1 and 5 seconds.")
        st.caption("**Parameterized client**: Starts a container against a specific target server and generates simple requests at the configured interval for the configured duration.")

    st.divider()
    st.markdown("### Consolidated benign client logs")

    # Unified log view.
    if "benign_log_tail" not in st.session_state:
        st.session_state["benign_log_tail"] = 400

    c1, c2, c3 = st.columns([1.2, 1.0, 1.8], gap="small")
    tail_n = c1.number_input(
        "Tail (lines)",
        min_value=20,
        max_value=5000,
        value=int(st.session_state["benign_log_tail"]),
        step=20,
        key="benign_log_tail_n",
    )
    st.session_state["benign_log_tail"] = int(tail_n)

    if c2.button("Refresh logs", key="refresh_benign_log"):
        st.rerun()

    if BENIGN_CLIENTS_LOG.exists():
        with BENIGN_CLIENTS_LOG.open("rb") as f:
            c3.download_button(
                "Download benign_clients.log",
                data=f,
                file_name=BENIGN_CLIENTS_LOG.name,
                mime="text/plain",
                key="dl_benign_clients_log",
                use_container_width=True,
            )
        st.code(tail_text_file(BENIGN_CLIENTS_LOG, n_lines=int(tail_n)), language="text")
    else:
        st.info('No log entries yet in "logs/benign_clients.log".')

# -----------------------------
# Captures + Features (views)
# -----------------------------
def list_capture_files() -> List[Path]:
    """
    Lists .pcap files in the captures/ directory.

    :return: List of paths in ascending order
    :rtype: List[Path]
    """
    _ensure_dirs()
    return sorted(CAPTURES_DIR.glob("*.pcap"), key=lambda p: p.stat().st_mtime, reverse=True)

def format_bytes(n: int) -> str:
    """
    Helper function that displays the capture file size on screen.

    :param n: Size in bytes
    :type n: int
    :return: Human-readable conversion
    :rtype: str
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024 or unit == "TB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def render_captures_view() -> None:
    """
    Streamlit functions that build the capture viewer module.
    """
    st.subheader("Completed Captures")
    top = st.columns([1, 1, 3])
    if top[0].button("Back"):
        st.session_state["view"] = "main"
        st.rerun()
    if top[1].button("Refresh list"):
        st.rerun()

    files = list_capture_files()
    if not files:
        st.info('No captures found in "captures/".')
        return

    query = st.text_input("Filter by name (optional)", value="").strip().lower()
    if query:
        files = [p for p in files if query in p.name.lower()]

    st.caption(f'Total: {len(files)} file(s) in "{CAPTURES_DIR}/"')

    # Organize columns to display buttons on the same row.
    h1, h2, h3, h4, h5, h6, h7, h8 = st.columns([4, 1.5, 2, 1.4, 1.6, 1.6, 1.8, 1.8], gap="small")
    h1.write("File")
    h2.write("Size")
    h3.write("Modified at")
    h4.write("Download")
    h5.write("Extract")
    h6.write("View features")
    h7.write("Generate dataset")
    h8.write("View dataset")

    for p in files:
        stat = p.stat()
        size = format_bytes(stat.st_size)
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        # Existing features?
        outs = build_feature_paths(p)
        existing = {tool: path for tool, path in outs.items() if path.exists()}
        has_features = len(existing) > 0

        # Existing dataset?
        dataset_path = build_dataset_path_for_capture(p)
        has_dataset = dataset_path.exists()

        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([4, 1.5, 2, 1.4, 1.6, 1.6, 1.8, 1.8], gap="small")
        c1.write(p.name)
        c2.write(size)
        c3.write(mtime)

        # Download PCAP
        with open(p, "rb") as f:
            c4.download_button(
                "Download",
                data=f,
                file_name=p.name,
                mime="application/vnd.tcpdump.pcap",
                key=f"dl_{p.name}",
                use_container_width=True,
            )

        # Extract features
        if c5.button("Extract", key=f"fx_{p.name}", type="secondary", use_container_width=True):
            st.session_state["selected_pcap"] = str(p)
            st.session_state["view"] = "features"
            st.rerun()

        # View features
        if c6.button("Ver", key=f"vf_{p.name}", type="secondary", use_container_width=True, disabled=not has_features):
            st.session_state["selected_pcap"] = str(p)
            st.session_state["view"] = "view_features"
            st.rerun()

        # Generate dataset (only when features exist)
        if c7.button("Generate", key=f"gd_{p.name}", type="secondary", use_container_width=True, disabled=not has_features):
            try:
                from modules.datasets import build_dataset_unsupervised_for_capture
                out_path = build_dataset_unsupervised_for_capture(
                    p,
                    features_dir=FEATURES_DIR,   # or "features"
                    outdir=DATASETS_DIR,         # or "datasets"
                )
                st.success(f"Dataset generated: {Path(out_path).name}")
            except Exception as e:
                st.error("Failed to generate dataset.")
                st.code(str(e), language="text")
            st.rerun()

        # View dataset (only when it exists)
        if c8.button("Ver", key=f"vd_{p.name}", type="secondary", use_container_width=True, disabled=not has_dataset):
            st.session_state["selected_pcap"] = str(p)
            st.session_state["view"] = "view_dataset"
            st.rerun()

def render_features_view() -> None:
    """
    Streamlit functions that build the extracted-feature selection view.
    """
    st.subheader("Feature Extraction")
    top = st.columns([1, 3])
    if top[0].button("Back"):
        st.session_state["view"] = "captures"
        st.rerun()

    pcap_str = st.session_state.get("selected_pcap", "")
    if not pcap_str:
        st.info("No capture selected.")
        return

    pcap_path = Path(pcap_str)
    if not pcap_path.exists():
        st.error(f"File not found: {pcap_path}")
        return

    _ensure_dirs()
    outs = build_feature_paths(pcap_path)

    st.write("Selected capture:", str(pcap_path))
    st.markdown("### Expected outputs")
    st.code("\n".join([str(outs["ntlflowlyzer"]), str(outs["tshark"]), str(outs["scapy"])]), language="text")

    c1, c2, c3 = st.columns(3)
    run_ntl = c1.checkbox("NTLFlowLyzer", value=True)
    run_tsh = c2.checkbox("TShark", value=True)
    run_scp = c3.checkbox("Scapy", value=True)

    overwrite = st.checkbox("Overwrite existing CSVs if present", value=True)

    if st.button("Extract features", type="primary"):
        results: Dict[str, Any] = {}
        with st.spinner("Running extraction... This action may take several minutes."):
            if run_ntl:
                results["ntlflowlyzer"] = extract_with_ntlflowlyzer(pcap_path, outs["ntlflowlyzer"]) if (overwrite or not outs["ntlflowlyzer"].exists()) else {"ok": True, "output": str(outs["ntlflowlyzer"]), "cmd": ["(skip) already exists"]}
            if run_tsh:
                results["tshark"] = extract_with_tshark(pcap_path, outs["tshark"]) if (overwrite or not outs["tshark"].exists()) else {"ok": True, "output": str(outs["tshark"]), "cmd": ["(skip) already exists"]}
            if run_scp:
                results["scapy"] = extract_with_scapy(pcap_path, outs["scapy"]) if (overwrite or not outs["scapy"].exists()) else {"ok": True, "output": str(outs["scapy"]), "cmd": ["(skip) already exists"]}

        st.markdown("### Results")
        for tool, res in results.items():
            if res.get("ok"):
                st.success(f"{tool}: OK → {res.get('output')}")
            else:
                st.warning("This extractor may have failed for this capture because the .pcap file may be incomplete...")
                if res.get("hint"):
                    st.info(res["hint"])
                if res.get("stderr"):
                    st.code(res["stderr"], language="text")
            if res.get("cmd"):
                st.caption("Command:")
                st.code(" ".join(res["cmd"]), language="bash")

        if st.button("Go to View features", type="secondary"):
            st.session_state["view"] = "view_features"
            st.rerun()

def _preview_csv(path: Path, n_rows: int) -> Any:
    """
    Data handling functions used to display results in Streamlit.

    :param path: CSV file path to display
    :type path: Path
    :param n_rows: Default number of rows to display
    :type n_rows: int
    :return: Formatted data
    :rtype: Any
    """
    try:
        import pandas as pd  # type: ignore
        df = pd.read_csv(path)
        return df.head(n_rows)
    except Exception:
        rows: List[Dict[str, Any]] = []
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= n_rows:
                    break
                rows.append(row)
        return rows

def render_view_dataset_view() -> None:
    """
    Streamlit functions that build the dataset viewer module.
    """
    st.subheader("Dataset (unsupervised)")

    top = st.columns([1, 1, 3])
    if top[0].button("Back"):
        st.session_state["view"] = "captures"
        st.rerun()
    if top[1].button("Refresh"):
        st.rerun()

    pcap_str = st.session_state.get("selected_pcap", "")
    if not pcap_str:
        st.info("No capture selected.")
        return

    pcap_path = Path(pcap_str)
    ds_path = build_dataset_path_for_capture(pcap_path)

    st.write("Capture:", str(pcap_path))
    st.write("Dataset:", str(ds_path))

    if not ds_path.exists():
        st.warning("Dataset not found for this capture.")
        return

    # Download
    with open(ds_path, "rb") as f:
        st.download_button(
            label="Download dataset (CSV)",
            data=f,
            file_name=ds_path.name,
            mime="text/csv",
            use_container_width=False,
        )

    st.divider()

    # View controls
    c1, c2, c3 = st.columns([1.3, 1.3, 2.4], gap="small")
    preview_n = c1.number_input("Preview (rows)", min_value=10, max_value=20000, value=200, step=50)
    max_cols = c2.number_input("Max columns", min_value=10, max_value=300, value=80, step=10)
    search = c3.text_input("Filter (contained in row text)", value="").strip().lower()

    # Load with pandas when possible.
    try:
        import pandas as pd

        # Read only the first N rows to keep it fast.
        df = pd.read_csv(ds_path, nrows=int(preview_n), engine="python")

        # Limit columns because many columns make the view heavy.
        if df.shape[1] > int(max_cols):
            df = df.iloc[:, : int(max_cols)]

        # Simple substring filter over concatenated row values.
        if search:
            mask = df.astype(str).agg(" ".join, axis=1).str.lower().str.contains(search, na=False)
            df = df[mask]

        st.caption(f"Displaying {len(df)} row(s) (up to {preview_n}) and {df.shape[1]} column(s).")
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        # Fallback without pandas.
        st.warning("Pandas is unavailable or failed to read the CSV. Using the simple view.")
        st.code(str(e), language="text")

        import csv

        rows = []
        with ds_path.open("r", encoding="utf-8", errors="replace", newline="") as fp:
            r = csv.reader(fp)
            for i, row in enumerate(r):
                rows.append(row)
                if i >= int(preview_n):
                    break

        if rows:
            # Display as a manual dataframe.
            header = rows[0]
            data = rows[1:]
            # Apply filter when present.
            if search:
                data = [r for r in data if search in " ".join(r).lower()]
            st.caption(f"Displaying {len(data)} row(s) (up to {preview_n})")
            st.dataframe(data, use_container_width=True)  # no header in fallback
        else:
            st.write("Empty file.")

def render_view_features_view() -> None:
    """
    Streamlit functions that build the extracted-feature viewer module.
    """
    st.subheader("Extracted Features")
    top = st.columns([1, 3])
    if top[0].button("Back"):
        st.session_state["view"] = "captures"
        st.rerun()

    pcap_str = st.session_state.get("selected_pcap", "")
    if not pcap_str:
        st.info("No capture selected.")
        return

    pcap_path = Path(pcap_str)
    outs = build_feature_paths(pcap_path)
    existing = {tool: path for tool, path in outs.items() if path.exists()}

    st.write("Capture:", str(pcap_path))

    if not existing:
        st.warning("No feature files found for this capture.")
        if st.button("Extract features now", type="primary"):
            st.session_state["view"] = "features"
            st.rerun()
        return

    st.markdown("### Found files")
    for tool, path in existing.items():
        cols = st.columns([3, 2, 2], gap="small")
        cols[0].write(path.name)
        cols[1].write(tool)
        with open(path, "rb") as f:
            cols[2].download_button("Download CSV", data=f, file_name=path.name, mime="text/csv", key=f"dl_csv_{tool}_{pcap_path.name}", use_container_width=True)

    st.markdown("### Preview")
    tool_list = list(existing.keys())
    tabs = st.tabs(tool_list)
    for tab, tool in zip(tabs, tool_list):
        with tab:
            csv_path = existing[tool]
            n = st.number_input("Rows to preview", min_value=5, max_value=500, value=50, step=5, key=f"preview_n_{tool}_{pcap_path.name}")
            preview = _preview_csv(csv_path, int(n))
            st.dataframe(preview, use_container_width=True)

# -----------------------------
# Host IP and server status
# -----------------------------
def get_host_ip() -> str:
    """
    Returns the actual host IP.

    :return: IP address as a string
    :rtype: str
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "-"

@st.cache_data(ttl=5, show_spinner=False)
def get_servers_status() -> List[dict]:
    """
    Returns server status.

    :return: Server status list
    :rtype: List[dict]
    """
    rows: List[dict] = [{"Server": "This machine", "IP": get_host_ip()}]

    if not docker_available():
        rows.append({"Server": "Docker", "IP": "Docker unavailable (CLI not accessible)."})
        return rows

    for label, image in SERVER_SPECS:
        ids = _container_ids_by_ancestor(image)
        cid = _pick_preferred_container(ids)
        if not cid:
            rows.append({"Server": label, "IP": "-"})
            continue
        inspected = _inspect(cid)
        if not inspected:
            rows.append({"Server": label, "IP": "-"})
            continue
        ips = _extract_ips(inspected)
        ip = ips.get("bridge") or (next(iter(ips.values())) if ips else "-")
        rows.append({"Server": label, "IP": ip})

    return rows

# -----------------------------
# tcpdump capture
# -----------------------------
def _file_size_stable(path: Path, checks: int = 5, sleep_s: float = 0.10) -> bool:
    try:
        last = path.stat().st_size
    except Exception:
        return False

    stable = 0
    for _ in range(checks):
        time.sleep(sleep_s)
        try:
            cur = path.stat().st_size
        except Exception:
            return False
        if cur == last:
            stable += 1
        else:
            stable = 0
            last = cur
    return stable >= checks


def _tshark_rewrite_pcap_if_needed(pcap_path: Path, tmp_dir: Path) -> Tuple[bool, str]:
    p = subprocess.run(["tshark", "-r", str(pcap_path), "-q"], capture_output=True)
    if p.returncode == 0:
        return False, "pcap_ok"

    cleaned = tmp_dir / f"clean-{pcap_path.name}"
    p2 = subprocess.run(["tshark", "-r", str(pcap_path), "-w", str(cleaned), "-F", "pcap"], capture_output=True)
    if p2.returncode == 0 and cleaned.exists() and cleaned.stat().st_size > 24:
        bak = tmp_dir / f"bak-{pcap_path.name}"
        try:
            if bak.exists():
                bak.unlink()
        except Exception:
            pass
        try:
            pcap_path.replace(bak)
        except Exception:
            pass
        cleaned.replace(pcap_path)
        return True, "pcap_rewritten_by_tshark"

    return False, "pcap_invalid_and_rewrite_failed"

def start_tcpdump_capture(pcap_path: Path, iface: str = "docker0") -> Dict[str, Any]:
    _ensure_dirs()

    cmd = ["tcpdump", "-i", iface, "-U", "-s", "0", "-w", str(pcap_path)]

    try:
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,
        )

        time.sleep(0.25)
        if p.poll() is not None:
            out, err = p.communicate(timeout=1)
            return {
                "ok": False,
                "cmd": cmd,
                "popen": None,
                "stderr": (err or b"").decode("utf-8", errors="replace").strip(),
                "stdout": (out or b"").decode("utf-8", errors="replace").strip(),
            }

        return {"ok": True, "cmd": cmd, "popen": p, "stdout": "", "stderr": ""}

    except FileNotFoundError:
        return {"ok": False, "cmd": cmd, "popen": None, "stdout": "", "stderr": "tcpdump not found in PATH."}
    except Exception as e:
        return {"ok": False, "cmd": cmd, "popen": None, "stdout": "", "stderr": str(e)}


def stop_tcpdump_capture(p: subprocess.Popen, pcap_path: Optional[Path] = None, timeout: float = 10.0) -> Dict[str, Any]:
    try:
        if p.poll() is None:
            # graceful: SIGINT
            try:
                os.killpg(p.pid, signal.SIGINT)
            except Exception:
                p.send_signal(signal.SIGINT)

            try:
                p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # SIGTERM
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except Exception:
                    p.terminate()

                try:
                    p.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    # SIGKILL
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except Exception:
                        p.kill()
                    p.wait(timeout=timeout)

        try:
            out, err = p.communicate(timeout=1)
        except Exception:
            out = (p.stdout.read() if p.stdout else b"")
            err = (p.stderr.read() if p.stderr else b"")

        res = {
            "ok": True,
            "stdout": (out or b"").decode("utf-8", errors="replace").strip(),
            "stderr": (err or b"").decode("utf-8", errors="replace").strip(),
        }

        if pcap_path and pcap_path.exists():
            _file_size_stable(pcap_path, checks=5, sleep_s=0.10)

            if tool_exists("tshark"):
                did, msg = _tshark_rewrite_pcap_if_needed(pcap_path, TMP_DIR)
                res["pcap_rewrite"] = msg
                res["pcap_rewritten"] = did

        return res

    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}

# -----------------------------
# Sidebar UI (render)
# -----------------------------
rows = get_servers_status()
ip_map = {r["Server"]: r["IP"] for r in rows}

st.sidebar.header("Stored Data")
if st.sidebar.button("Completed Capture Files", use_container_width=True):
    st.session_state["view"] = "captures"
    st.rerun()
if st.sidebar.button("Completed Attack Logs", use_container_width=True):
    st.session_state["view"] = "attacks_logs"
    st.rerun()

st.sidebar.divider()

h1, h2, h3 = st.sidebar.columns([2, 2, 2])
h1.write("**Server**")
h2.write("**IP**")
h3.write("**Ver logs**")

c1, c2, c3 = st.sidebar.columns([2, 2, 2])
c1.write("This machine")
c2.write(ip_map.get("This machine", "-"))
c3.write("-")

for label, image_base in SERVER_SPECS:
    c1, c2, c3 = st.sidebar.columns([2, 2, 2], gap="small")
    c1.write(label)
    c2.write(ip_map.get(label, "-"))
    if c3.button("Logs", key=f"logs_btn_{image_base}", type="secondary", use_container_width=True):
        st.session_state["view"] = "server_logs"
        st.session_state["server_logs_label"] = label
        st.session_state["server_logs_image_base"] = image_base
        st.rerun()

if st.sidebar.button("Refresh"):
    get_servers_status.clear()

st.sidebar.divider()
st.sidebar.header("Running benign clients:")

# Only status/counters here; controls stay in the "Benign Client Control" screen.
running_random = list_running_benign_clients()
running_super = list_running_super_clients()

st.sidebar.write(f"Random access: **{len(running_random)}**")
st.sidebar.write(f"Parameterized: **{len(running_super)}**")

# Prerequisite info for spawning the random client (depends on the 7 servers).
server_ips, missing_servers = get_required_server_ips()
servers_ok = (server_ips is not None)
if not servers_ok:
    st.sidebar.warning(
        "Servers unavailable (prerequisite for random client): "
        f"{', '.join(missing_servers)}"
    )

with st.sidebar.expander("Details", expanded=False):
    if running_random:
        st.write("Random:", ", ".join(name for name, _ in running_random))
    else:
        st.write("Random: none running.")
    if running_super:
        st.write("Parameterized:", ", ".join(name for name, _ in running_super))
    else:
        st.write("Parameterized: none running.")

if st.sidebar.button("Benign Client Control", use_container_width=True):
    st.session_state["view"] = "benign_clients"
    st.rerun()

st.sidebar.divider()

# -----------------------------
# Attack Run / Stop / Status
# -----------------------------
def run_attack_from_spec(
    spec: AttackSpec,
    resolved_params: Dict[str, Any],
    capture_enabled: bool = True,
    max_runtime_s: int = 15,
) -> Dict[str, Any]:
    """
    Runs attacks and controls their containers.

    - Starts the attack container (docker run -d --rm ...)
    - Optionally starts tcpdump capture on docker0 and stops it automatically when the container exits
    - Stops the container after `max_runtime_s` if it is still running (watchdog)
    - Records logs in logs/attacks.log on a best-effort basis

    :param spec: Attack parameter definition from the registry
    :type spec: AttackSpec
    :param resolved_params: Parameters resolved for execution
    :type resolved_params: Dict[str, Any]
    :param capture_enabled: Whether to start packet capture automatically, defaults to True
    :type capture_enabled: bool, optional
    :param max_runtime_s: Maximum time in seconds before stopping the container if still running
    :type max_runtime_s: int
    :return: Parameter dictionary
    :rtype: Dict[str, Any]
    """
    if not docker_available():
        return {"ok": False, "stderr": "Docker is unavailable on the Streamlit host.", "cmd": [], "returncode": 1}

    # Ensure a reasonable value.
    try:
        max_runtime_s = int(max_runtime_s)
    except Exception:
        max_runtime_s = int(getattr(spec, "max_runtime_s", 15) or 15)
    if max_runtime_s < 1:
        max_runtime_s = 1

    # Capture path when enabled.
    pcap_path = build_capture_path(spec.id) if capture_enabled else None

    def _start_attack_only() -> Dict[str, Any]:
        with st.spinner("Running attack..."):
            result = spec.runner(resolved_params)

        # watchers/logs
        container_ref = result.get("container_id") or spec.container_name
        start_attack_logs_watcher(
            container_ref,
            spec,
            cmd=result.get("cmd"),
            pcap_path=str(pcap_path) if pcap_path else None,
            max_runtime_s=max_runtime_s,
            capture_enabled=capture_enabled,
        )
        start_attack_timeout_watchdog(container_ref, spec, max_runtime_s=max_runtime_s)

        result["max_runtime_s"] = max_runtime_s
        result["capture"] = {"enabled": False}
        return result

    if not capture_enabled:
        return _start_attack_only()

    # Capture enabled.
    cap = start_tcpdump_capture(pcap_path, iface="docker0")
    if not cap.get("ok"):
        return {
            "ok": False,
            "stderr": f"Failed to start capture: {cap.get('stderr') or ''}".strip(),
            "cmd": cap.get("cmd", []),
            "returncode": 1,
            "capture": {"enabled": True, "ok": False, "pcap_path": str(pcap_path), **cap},
        }

    tcpdump_p = cap["popen"]
    with st.spinner("Running attack and capturing traffic..."):
        attack_result = spec.runner(resolved_params)

    # watchers/logs, even on failure.
    container_ref = attack_result.get("container_id") or spec.container_name
    start_attack_logs_watcher(
        container_ref,
        spec,
        cmd=attack_result.get("cmd"),
        pcap_path=str(pcap_path),
        max_runtime_s=max_runtime_s,
        capture_enabled=True,
    )
    start_attack_timeout_watchdog(container_ref, spec, max_runtime_s=max_runtime_s)

    attack_result["max_runtime_s"] = max_runtime_s

    if not attack_result.get("ok"):
        stop_info = stop_tcpdump_capture(cap["popen"], pcap_path=pcap_path, timeout=3.0)
        attack_result["capture"] = {
            "enabled": True,
            "ok": True,
            "pcap_path": str(pcap_path),
            "tcpdump_cmd": cap.get("cmd"),
            "stop": stop_info,
        }
        return attack_result

    container_id = attack_result.get("container_id")
    wait_err = ""
    if container_id:
        rc, out, err = _run(["docker", "wait", container_id])
        if rc != 0:
            wait_err = err or out or "Failed to wait for the container to finish."
    else:
        wait_err = "container_id was not returned; could not wait for completion."

    stop_info = stop_tcpdump_capture(cap["popen"], pcap_path=pcap_path, timeout=3.0)
    attack_result["capture"] = {
        "enabled": True,
        "ok": True,
        "pcap_path": str(pcap_path),
        "tcpdump_cmd": cap.get("cmd"),
        "wait_error": wait_err,
        "stop": stop_info,
    }
    return attack_result

def show_last_attack_result(spec: AttackSpec) -> None:
    """
    Execution session state.

    :param spec: Specification whose latest execution state should be displayed
    :type spec: AttackSpec
    """
    res = st.session_state["last_attack_result"].get(spec.id)
    if not res:
        return

    st.markdown("### Latest execution")

    cap = res.get("capture") or {}
    if cap.get("enabled") is False:
        st.write("Capture:", "disabled")

    pcap = cap.get("pcap_path")
    if pcap:
        st.write("Capture:", pcap)
        if cap.get("tcpdump_cmd"):
            st.caption("tcpdump command:")
            st.code(" ".join(cap["tcpdump_cmd"]), language="bash")
        if cap.get("wait_error"):
            st.warning(f"Note: {cap['wait_error']}")

    if res.get("ok"):
        st.success("Attack started successfully.")
        st.write("Container ID:", res.get("container_id") or "-")
    else:
        st.error("Failed to start attack.")
        st.write("Return code:", res.get("returncode"))
        if res.get("stderr"):
            st.code(res["stderr"], language="text")

    st.caption("Executed command:")
    st.code(" ".join(res.get("cmd", [])), language="bash")

    if st.button("Clear latest output", key=f"clear_last_{spec.id}"):
        st.session_state["last_attack_result"].pop(spec.id, None)
        st.rerun()

def stop_attack(spec: AttackSpec) -> None:
    """
    Manual attack stop control.

    :param spec: Attack specification to stop
    :type spec: AttackSpec
    """
    if not spec.container_name:
        st.warning("This attack has no container_name defined; it cannot be stopped automatically.")
        return
    if not docker_available():
        st.error("Docker is unavailable on the Streamlit host.")
        return
    result = docker_rm_force(spec.container_name)
    if result.get("ok"):
        st.success("Attack container removed.")
    else:
        st.error("Failed to remove the attack container.")
        if result.get("stderr"):
            st.code(result["stderr"], language="text")

def show_attack_runtime(spec: AttackSpec) -> None:
    """
    Displays the running attack.

    :param spec: Attack specification
    :type spec: AttackSpec
    """
    if not spec.container_name:
        st.info("This attack has no container_name defined; status/stop are unavailable.")
        return
    status = docker_container_status(spec.container_name)
    if not status.get("exists"):
        st.write("Attack status:", "**stopped**.")
        return
    st.write("Attack status:", status.get("status", "unknown"))
    st.write("Container:", status.get("id") or "-")
    with st.expander("View logs (tail 200)", expanded=False):
        logs = docker_logs(spec.container_name, tail=200)
        if logs.get("ok") and logs.get("stdout"):
            st.code(logs["stdout"], language="text")
        elif logs.get("stderr"):
            st.code(logs["stderr"], language="text")
        else:
            st.write("No logs available.")

# -----------------------------
# Dynamic schema-based form
# -----------------------------
def validate_ip(value: str) -> bool:
    """
    IP validation function.

    :param value: Address string
    :type value: str
    :return: Whether it is a valid IP address
    :rtype: bool
    """
    try:
        ipaddress.ip_address(value.strip())
        return True
    except Exception:
        return False

def validate_port(value: int) -> bool:
    """
    Port validation.

    :param value: Port as an integer
    :type value: int
    :return: Whether it is a valid port
    :rtype: bool
    """
    return 1 <= int(value) <= 65535

def validate_cidr(value: str) -> bool:
    """
    Network validation.

    :param value: Network string
    :type value: str
    :return: Whether it is a valid network
    :rtype: bool
    """
    try:
        ipaddress.ip_network(value.strip(), strict=False)
        return True
    except Exception:
        return False

_FQDN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}\.?$"
)
_HOST_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.(?!-)[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*\.?$"
)

def validate_fqdn(value: str, *, allow_single_label: bool = False) -> bool:
    """
    Validates hostname/FQDN.
    - allow_single_label=False: requires at least one dot and a TLD (for example, example.com)
    - allow_single_label=True: allows hostnames without dots (for example, "router", "localhost")

    :param value: Value to test
    :type value: str
    :param allow_single_label: Whether simple names are allowed, defaults to False
    :type allow_single_label: bool, optional
    :return: True when valid, otherwise False
    :rtype: bool
    """
    v = value.strip()
    if not v:
        return False
    if " " in v or "://" in v or "/" in v:
        return False

    if re.fullmatch(r"[0-9.]+", v) or ":" in v:
        return False

    if v.lower() == "localhost":
        return True

    if allow_single_label:
        return _HOST_RE.match(v) is not None
    return _FQDN_RE.match(v) is not None

def validate_ip_or_fqdn(value: str, *, allow_single_label: bool = False) -> bool:
    """
    Validates user input as a valid IP or FQDN.

    :param value: Target input
    :type value: str
    :param allow_single_label: Whether simple names are allowed, defaults to False
    :type allow_single_label: bool, optional
    :return: True when valid, otherwise False
    :rtype: bool
    """
    return validate_ip(value) or validate_fqdn(value, allow_single_label=allow_single_label)

def resolve_placeholder(p: ParamSpec, host_ip: str) -> str:
    """
    Defines placeholders (input suggestions) based on registry specifications.

    :param p: Parameter type
    :type p: ParamSpec
    :param host_ip: Suggested IP
    :type host_ip: str
    :return: Suggested IP placeholder
    :rtype: str
    """
    ph = getattr(p, "placeholder", None)
    if not ph:
        return ""
    return host_ip if ph == "__HOST_IP__" else str(ph)

def render_params_form(spec: AttackSpec, host_ip: str) -> Tuple[bool, Dict[str, Any], bool, int]:
    """
    Renders the parameter form for a selected attack.

    Returns (submitted, resolved_params, capture_enabled, max_runtime_s).

    :param spec: Parameter type
    :type spec: AttackSpec
    :param host_ip: Suggested IP
    :type host_ip: str
    :return: Suggested parameter values for each attack type
    :rtype: Tuple[bool, Dict[str, Any], bool, int]
    """
    resolved: Dict[str, Any] = {}
    runtime_default = int(getattr(spec, "max_runtime_s", 15) or 15)

    if spec.no_params_note:
        st.info(spec.no_params_note)

    if not spec.params:
        max_runtime_s = int(
            st.number_input(
                "Maximum runtime (s)",
                min_value=1,
                max_value=86400,
                value=runtime_default,
                step=1,
                key=f"maxrt_{spec.id}",
            )
        )

        c1, c2 = st.columns([3, 2])
        capture_enabled = c2.toggle(
            "Start packet capture with the attack",
            value=True,
            key=f"cap_toggle_{spec.id}",
        )
        submitted = c1.button("Start attack", key=f"start_noparams_{spec.id}")
        return submitted, resolved, capture_enabled, max_runtime_s

    with st.form(f"form_{spec.id}", clear_on_submit=False):
        for p in spec.params:
            ph = resolve_placeholder(p, host_ip)
            if p.kind == "port":
                default_port = int(p.default) if p.default is not None else (int(ph) if ph.isdigit() else 1)
                value = st.number_input(
                    p.label,
                    min_value=1,
                    max_value=65535,
                    value=default_port,
                    step=1,
                    key=f"{spec.id}_{p.key}",
                )
                resolved[p.key] = int(value)
            elif p.kind == "int":
                default_int = int(p.default) if p.default is not None else 0
                value = st.number_input(
                    p.label,
                    min_value=0,
                    max_value=10_000_000_000,
                    value=default_int,
                    step=1,
                    key=f"{spec.id}_{p.key}",
                )
                resolved[p.key] = int(value)
            elif p.kind == "float":
                default_float = float(p.default) if p.default is not None else 0.0
                value = st.number_input(
                    p.label,
                    min_value=0.0,
                    value=default_float,
                    step=0.1,
                    key=f"{spec.id}_{p.key}",
                )
                resolved[p.key] = float(value)
            else:
                value = st.text_input(
                    p.label,
                    placeholder=ph if ph else None,
                    value="" if p.default is None else str(p.default),
                    key=f"{spec.id}_{p.key}",
                ).strip()
                if not value and ph:
                    value = ph
                    st.caption(f'Field "{p.label}" is empty; using suggested value: {ph}')
                resolved[p.key] = value

        max_runtime_s = int(
            st.number_input(
                "Maximum runtime (s)",
                min_value=1,
                max_value=86400,
                value=runtime_default,
                step=1,
                key=f"maxrt_{spec.id}",
            )
        )

        c1, c2 = st.columns([3, 2])
        submitted = c1.form_submit_button("Start attack")
        capture_enabled = c2.toggle(
            "Start packet capture with the attack",
            value=True,
            key=f"cap_toggle_{spec.id}",
        )

    return submitted, resolved, capture_enabled, max_runtime_s

def validate_params(spec: AttackSpec, params: Dict[str, Any]) -> List[str]:
    """
    Validates inserted parameters.

    :param spec: Parameter type
    :type spec: AttackSpec
    :param params: Dictionary of possible values
    :type params: Dict[str, Any]
    :return: Validation error list
    :rtype: List[str]
    """
    errors: List[str] = []
    for p in spec.params:
        v = params.get(p.key, "")
        if p.kind == "ip":
            if not v or not validate_ip_or_fqdn(str(v), allow_single_label=False):
                errors.append(f'Field "{p.label}" is invalid.')
        elif p.kind == "cidr":
            if not v or not validate_cidr(str(v)):
                errors.append(f'Field "{p.label}" is invalid (for example, 192.168.0.0/24).')
        elif p.kind == "port":
            try:
                pv = int(v)
                if not validate_port(pv):
                    errors.append(f'Field "{p.label}" is invalid (1-65535).')
            except Exception:
                errors.append(f'Field "{p.label}" is invalid (1-65535).')
        elif p.kind == "int":
            try:
                if int(v) < 0:
                    errors.append(f'Field "{p.label}" is invalid (integer >= 0).')
            except Exception:
                errors.append(f'Field "{p.label}" is invalid (integer >= 0).')
        elif p.kind == "float":
            try:
                if float(v) < 0:
                    errors.append(f'Field "{p.label}" is invalid (number >= 0).')
            except Exception:
                errors.append(f'Field "{p.label}" is invalid (number >= 0).')
        else:
            if v is None:
                errors.append(f'Field "{p.label}" is invalid.')
    return errors

# -----------------------------
# Category tab UI
# -----------------------------
def category_tab_ui(category_name: str, attacks: List[AttackSpec]) -> None:
    """
    Renders attack category tabs.

    :param category_name: Categories specified in the registry
    :type category_name: str
    :param attacks: Specific parameters for the attack selected in a tab
    :type attacks: List[AttackSpec]
    """
    st.subheader(category_name)

    attack_name_to_spec = {a.name: a for a in attacks}
    attack_name = st.selectbox("Attack", list(attack_name_to_spec.keys()), key=f"attack_select_{category_name}")
    spec = attack_name_to_spec[attack_name]

    left, right = st.columns([2, 3], gap="large")
    host_ip = get_host_ip()

    with left:
        st.markdown("### Attack Details")
        st.markdown(f"ID: `{spec.id}`")
        st.markdown(f"Name: {spec.name}")
        st.markdown(f"Description: {spec.description}")
        render_tools_links(getattr(spec, "tools", None))
        with st.expander("Container Details", expanded=False):
            st.markdown(f"Image: `{spec.image}`")
            st.markdown(f"Name: `{spec.container_name}`")
        render_mitre_links(getattr(spec, "mitre", None))
        if getattr(spec, "details_warning", None):
            st.warning(spec.details_warning)
        st.markdown("### Execution")
        show_attack_runtime(spec)

        col1, col2 = st.columns([1, 1])
        if col1.button("Refresh status", key=f"refresh_status_{spec.id}"):
            st.rerun()
        if col2.button("Stop attack", key=f"stop_{spec.id}"):
            stop_attack(spec)
            st.rerun()

    with right:
        st.markdown("### Parameters")
        submitted, resolved, capture_enabled, max_runtime_s = render_params_form(spec, host_ip)
        show_last_attack_result(spec)

        if submitted:
            errors = validate_params(spec, resolved)
            if errors:
                for e in errors:
                    st.error(e)
            else:
                result = run_attack_from_spec(spec, resolved, capture_enabled=capture_enabled, max_runtime_s=max_runtime_s)
                st.session_state["last_attack_result"][spec.id] = result
                st.rerun()

# -----------------------------
# View router
# -----------------------------
if st.session_state["view"] == "benign_clients":
    render_benign_clients_view()
    st.stop()
if st.session_state["view"] == "server_logs":
    render_server_logs_view()
    st.stop()
if st.session_state.get("view") == "attacks_logs":
    render_attacks_logs_view()
    st.stop()
if st.session_state["view"] == "captures":
    render_captures_view()
    st.stop()
if st.session_state["view"] == "features":
    render_features_view()
    st.stop()
if st.session_state["view"] == "view_features":
    render_view_features_view()
    st.stop()
if st.session_state["view"] == "view_dataset":
    render_view_dataset_view()
    st.stop()

# -----------------------------
# Main screen: tabs
# -----------------------------
category_names = list(CATEGORIES.keys())
if not category_names:
    st.error("No attacks were loaded from the Docker attack catalog.")
    st.caption("Expected catalog location: docker/attackers/*/attack.yaml")
    st.stop()

tabs = st.tabs(category_names)
for tab, category_name in zip(tabs, category_names):
    with tab:
        category_tab_ui(category_name, CATEGORIES[category_name])

st.divider()
st.caption("26th Brazilian Symposium on Cybersecurity (SBSeg) 2026 - SF.")
st.caption(
    "This tool is intended for educational use and must not be used to attack addresses outside the experiment. "
    "For demonstrations, use this machine's own IP as the attack target for attacks aimed directly at an IP address. "
    "For network-level attacks, use the Docker network (172.17.0.0/16) or your local network."
)
