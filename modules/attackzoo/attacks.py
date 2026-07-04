from __future__ import annotations

import re as _re
from typing import Any, Dict, Optional

from modules.registry import CATEGORIES, AttackSpec


_TARGET_KNOWN_KEYS = {"target_ip", "target_net", "target", "target_server", "host"}


_KIND_PATTERNS = {
    "ip":   _re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^[a-zA-Z0-9._-]+$"),
    "cidr": _re.compile(r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$"),
}


def _all_specs() -> Dict[str, Any]:
    """Flatten the categorized registry into an attack-id lookup table."""
    return {s.id: s for specs in CATEGORIES.values() for s in specs}


_TARGET_KNOWN_KEYS = {"target_ip", "target_net", "target", "target_server", "host"}


def _find_target_param(spec: AttackSpec):
    """Return the primary target ParamSpec (host/network), or None."""
    # Priority 0: declarative target_mapping in YAML
    if spec.target_mapping and "target" in spec.target_mapping:
        mapped_key = spec.target_mapping["target"]
        for p in spec.params:
            if p.key == mapped_key:
                return p
    # Priority 1: known key (heuristic fallback)
    for p in spec.params:
        if p.key in _TARGET_KNOWN_KEYS:
            return p
    # Priority 2: first ip/cidr parameter
    for p in spec.params:
        if p.kind in ("ip", "cidr"):
            return p
    return None


def _find_port_param(spec: AttackSpec):
    """Return the attack port ParamSpec, or None."""
    # Priority 0: declarative target_mapping, "port" key
    if spec.target_mapping and "port" in spec.target_mapping:
        mapped_key = spec.target_mapping["port"]
        for p in spec.params:
            if p.key == mapped_key:
                return p
    # Priority 1: first parameter with kind "port"
    for p in spec.params:
        if p.kind == "port":
            return p
    return None


_KIND_PATTERNS = {
    "ip":   _re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^[a-zA-Z0-9._-]+$"),
    "cidr": _re.compile(r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$"),
}


def _validate_param(p: "ParamSpec", value: str) -> Optional[str]:
    """Return an error message, or None when valid."""
    # Custom YAML regex takes priority
    if p.validate:
        if not _re.match(p.validate, value):
            return f"Value '{value}' is invalid for --{p.key} (expected pattern: {p.validate})"
        return None
    # Kind-based validation
    if p.kind == "port":
        try:
            port = int(value)
            if not (1 <= port <= 65535):
                return f"Port {port} is out of range (1-65535)"
        except ValueError:
            return f"'{value}' is not a valid port"
    elif p.kind == "int":
        try:
            if int(value) < 0:
                return f"'{value}' must be an integer greater than or equal to zero"
        except ValueError:
            return f"'{value}' is not a valid integer"
    elif p.kind == "float":
        try:
            if float(value) < 0:
                return f"'{value}' must be a number greater than or equal to zero"
        except ValueError:
            return f"'{value}' is not a valid number"
    elif p.kind in _KIND_PATTERNS:
        if not _KIND_PATTERNS[p.kind].match(value):
            return f"'{value}' is invalid for {p.kind} parameter '--{p.key}'"
    return None
