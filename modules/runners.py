import json
import subprocess
from typing import Any, Dict, List, Optional, Tuple

def _run(cmd: List[str]) -> Tuple[int, str, str]:
    """
    Run a command.

    :param cmd: Intended command.
    :type cmd: List[str]
    :return: Return code, stdout, and stderr.
    :rtype: Tuple[int, str, str]
    """
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

def docker_available() -> bool:
    """
    Check whether Docker is available.

    :return: True when Docker is available, otherwise false.
    :rtype: bool
    """
    rc, _, _ = _run(["docker", "version"])
    return rc == 0

def docker_container_id_by_name(name: str) -> Optional[str]:
    """
    Use an exact ^name$ regex to identify a container.

    :param name: Container name.
    :type name: str
    :return: Matching container ID, if found.
    :rtype: Optional[str]
    """
    rc, out, _ = _run(["docker", "ps", "-a", "-q", "--filter", f"name=^{name}$"])
    if rc != 0:
        return None
    cid = out.strip()
    return cid or None

def docker_rm_force(name_or_id: str) -> Dict[str, Any]:
    """
    Force-remove a container.

    :param name_or_id: Input name or ID.
    :type name_or_id: str
    :return: Command execution details.
    :rtype: Dict[str, Any]
    """
    rc, out, err = _run(["docker", "rm", "-f", name_or_id])
    return {
        "ok": rc == 0,
        "cmd": ["docker", "rm", "-f", name_or_id],
        "stdout": out,
        "stderr": err,
        "returncode": rc,
    }

def docker_inspect(name_or_id: str) -> Optional[dict]:
    """
    Inspect a container.

    :param name_or_id: Input name or ID.
    :type name_or_id: str
    :return: Docker inspect payload, if available.
    :rtype: Dict[str, Any]
    """
    rc, out, _ = _run(["docker", "inspect", name_or_id])
    if rc != 0 or not out:
        return None
    try:
        data = json.loads(out)
        return data[0] if data else None
    except Exception:
        return None

def docker_container_status(name: str) -> Dict[str, Any]:
    """
    Get container status.

    :param name_or_id: Input name or ID.
    :type name_or_id: str
    :return: Status details.
    :rtype: Dict[str, Any]
    """
    cid = docker_container_id_by_name(name)
    if not cid:
        return {"exists": False, "name": name, "id": None, "status": "not_found"}

    inspected = docker_inspect(cid)
    if not inspected:
        return {"exists": True, "name": name, "id": cid[:12], "status": "unknown"}

    state = inspected.get("State") or {}
    status = (state.get("Status") or "unknown").lower()
    return {"exists": True, "name": name, "id": cid[:12], "status": status}

def docker_logs(name_or_id: str, tail: int = 200) -> Dict[str, Any]:
    rc, out, err = _run(["docker", "logs", "--tail", str(tail), name_or_id])
    return {
        "ok": rc == 0,
        "cmd": ["docker", "logs", "--tail", str(tail), name_or_id],
        "stdout": out,
        "stderr": err,
        "returncode": rc,
    }

def docker_run_detached(
    *,
    image: str,
    name: str,
    args: List[str],
    env: Optional[Dict[str, str]] = None,
    network: Optional[str] = None,
    remove_if_exists: bool = True,
) -> Dict[str, Any]:
    """
    Run a container in detached mode.

    :param image: Image name.
    :type image: str
    :param name: Container name.
    :type name: str
    :param args: Associated parameters.
    :type args: List[str]
    :param env: Environment variables to inject into the container, for example {"RATE": "500"}.
    :type env: Dict[str, str], optional
    :param remove_if_exists: Remove an existing container with the same name, defaults to true.
    :type remove_if_exists: bool, optional
    :return: Command execution details.
    :rtype: Dict[str, Any]
    """

    if remove_if_exists:
        existing = docker_container_id_by_name(name)
        if existing:
            docker_rm_force(existing)

    env_flags: List[str] = []
    for k, v in (env or {}).items():
        env_flags += ["-e", f"{k}={v}"]

    network_flags = ["--network", network] if network else []

    cmd = ["docker", "run", "--rm", "-d", "--name", name, *network_flags, *env_flags, image, *args]
    rc, out, err = _run(cmd)
    ok = (rc == 0)

    return {
        "ok": ok,
        "cmd": cmd,
        "container_id": out.strip() if ok else None,
        "stdout": out,
        "stderr": err,
        "returncode": rc,
    }
