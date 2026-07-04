import ipaddress
import pathlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

try:
    from modules.runners import docker_run_detached
except ModuleNotFoundError:  # Compatibility when modules/ is placed directly on sys.path.
    from runners import docker_run_detached

_LOOPBACK_NAMES = {"localhost"}
_TARGET_KNOWN_KEYS = {"target_ip", "target", "target_server", "host"}


def _is_loopback_target(value: Any) -> bool:
    """Check whether a resolved target value refers to the local host."""
    text = str(value).strip().lower()
    if text in _LOOPBACK_NAMES:
        return True
    try:
        return ipaddress.ip_address(text).is_loopback
    except ValueError:
        return False


@dataclass(frozen=True)
class ParamSpec:
    key: str
    label: str
    kind: str  # "ip" | "port" | "cidr" | "text" | "int" | "float"
    placeholder: Optional[str] = None
    default: Optional[Any] = None
    validate: Optional[str] = None  # custom validation regex override
    required: bool = True
    positional: bool = True
    env_var: Optional[str] = None

@dataclass(frozen=True)
class AttackSpec:
    id: str
    name: str
    description: str
    image: str
    container_name: str
    params: List[ParamSpec] = field(default_factory=list)
    no_params_note: Optional[str] = None
    details_warning: Optional[str] = None
    mitre: Optional[Union[str, List[str]]] = None
    tools: Optional[List[Dict[str, str]]] = None
    max_runtime_s: int = 10
    target_mapping: Optional[Dict[str, str]] = None  # example: {"target": "target_ip"}
    docker_network: Optional[str] = None

    def runner(self, resolved_params: Dict[str, Any]) -> Dict[str, Any]:
        """Launch this attack image with resolved positional args and env vars."""
        args = self.positional_args(resolved_params)
        env = self.env_vars(resolved_params)
        return docker_run_detached(
            image=self.image,
            name=self.container_name,
            args=args,
            env=env or None,
            network=self.network_mode(resolved_params),
        )

    def positional_args(self, resolved_params: Dict[str, Any]) -> List[str]:
        """Return resolved parameters that must be passed as container arguments."""
        return [
            str(resolved_params[p.key])
            for p in self.params
            if p.positional and p.key in resolved_params
        ]

    def env_vars(self, resolved_params: Dict[str, Any]) -> Dict[str, str]:
        """Return resolved parameters that should be injected as environment vars."""
        return {
            p.env_var: str(resolved_params[p.key])
            for p in self.params
            if p.env_var and p.key in resolved_params and resolved_params[p.key] is not None
        }

    def network_mode(self, resolved_params: Dict[str, Any]) -> Optional[str]:
        """Select the Docker network mode required for this attack invocation."""
        if self.docker_network:
            return self.docker_network

        target_keys = set(_TARGET_KNOWN_KEYS)
        if self.target_mapping and "target" in self.target_mapping:
            target_keys.add(self.target_mapping["target"])

        has_loopback_target = any(
            p.key in target_keys
            and p.key in resolved_params
            and _is_loopback_target(resolved_params[p.key])
            for p in self.params
        )
        has_port = any(p.kind == "port" and p.key in resolved_params for p in self.params)

        if has_loopback_target and has_port:
            return "host"
        return None

# Load CATEGORIES exclusively from attack.yaml files.
_attacks_dir = pathlib.Path(__file__).parent.parent / "docker" / "attackers"
CATEGORIES: Dict[str, List[AttackSpec]] = {}
try:
    from modules.loader import load_attacks as _la
except ModuleNotFoundError:  # Compatibility when modules/ is placed directly on sys.path.
    from loader import load_attacks as _la

try:
    CATEGORIES = _la(_attacks_dir)
except Exception as _e:
    import warnings
    warnings.warn(f"[registry] Failed to load attacks: {_e}")
