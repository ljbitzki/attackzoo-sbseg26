from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

from modules.attackzoo.common import _ensure_dir, _now_ts


CAPTURES_DIR = Path("captures")


def build_capture_path(prefix: str) -> Path:
    _ensure_dir(CAPTURES_DIR)
    return CAPTURES_DIR / f"{prefix}-{_now_ts()}.pcap"


def start_tcpdump(pcap_path: Path, iface: str, bpf: str = "") -> subprocess.Popen:
    _ensure_dir(pcap_path.parent)
    cmd = ["tcpdump", "-i", iface, "-U", "-s", "0", "-w", str(pcap_path)]
    if bpf.strip():
        cmd += shlex.split(bpf.strip())
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
