from __future__ import annotations

import os
import signal
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

def _ensure_dir(p: Path) -> None:
    """Create a directory tree when a command needs an output location."""
    p.mkdir(parents=True, exist_ok=True)


def _now_ts() -> str:
    """Return a timestamp string suitable for filenames and run folders."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _run(cmd: List[str]) -> Tuple[int, str, str]:
    """Run a command and return decoded stdout/stderr with its exit code."""
    p = subprocess.run(cmd, capture_output=True)
    out = (p.stdout or b"").decode("utf-8", errors="replace").strip()
    err = (p.stderr or b"").decode("utf-8", errors="replace").strip()
    return p.returncode, out, err


def _stop_proc(p: Optional[subprocess.Popen], timeout: float = 5.0) -> None:
    """Stop a child process group gracefully before falling back to termination."""
    if not p:
        return
    try:
        if p.poll() is None:
            try:
                os.killpg(p.pid, signal.SIGINT)
            except Exception:
                try:
                    p.send_signal(signal.SIGINT)
                except Exception:
                    pass
            try:
                p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except Exception:
                    try:
                        p.terminate()
                    except Exception:
                        pass
                try:
                    p.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except Exception:
                        try:
                            p.kill()
                        except Exception:
                            pass
    except Exception:
        pass


def _phase_of(t_rel: float, warmup: float, attack: float, cooldown: float) -> str:
    """Map elapsed experiment time to warmup, attack, cooldown, or done."""
    if t_rel < warmup:
        return "warmup"
    if t_rel < warmup + attack:
        return "attack"
    if t_rel < warmup + attack + cooldown:
        return "cooldown"
    return "done"
