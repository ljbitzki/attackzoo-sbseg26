"""modules/loader.py — Dynamic attack discovery from attack.yaml files.

Scans docker/attackers/ for subdirectories containing attack.yaml,
builds AttackSpec/ParamSpec objects, and returns a CATEGORIES dict
identical in shape to the one in registry.py.
"""

import pathlib
import yaml


STANDARD_INTENSITY_PARAMS = {
    "duration_s": {
        "label": "Internal attack duration (s)",
        "kind": "int",
        "default": 0,
        "validate": r"^\d+$",
        "env_var": "DURATION_S",
    },
    "count": {
        "label": "Number of packets/requests/attempts",
        "kind": "int",
        "default": 0,
        "validate": r"^\d+$",
        "env_var": "COUNT",
    },
    "rate_pps": {
        "label": "Target rate (packets/requests per second)",
        "kind": "int",
        "default": 0,
        "validate": r"^\d+$",
        "env_var": "RATE_PPS",
    },
    "concurrency": {
        "label": "Maximum concurrency",
        "kind": "int",
        "default": 1,
        "validate": r"^[1-9]\d*$",
        "env_var": "CONCURRENCY",
    },
    "threads": {
        "label": "Number of parallel threads/clients",
        "kind": "int",
        "default": 1,
        "validate": r"^[1-9]\d*$",
        "env_var": "THREADS",
    },
    "delay_ms": {
        "label": "Interval between sends (ms)",
        "kind": "int",
        "default": 0,
        "validate": r"^\d+$",
        "env_var": "DELAY_MS",
    },
    "payload_size": {
        "label": "Payload size (bytes)",
        "kind": "int",
        "default": 0,
        "validate": r"^\d+$",
        "env_var": "PAYLOAD_SIZE",
    },
}


def load_attacks(attacks_dir: pathlib.Path) -> dict:
    """Scan attacks_dir for attack.yaml files and return a CATEGORIES dict."""
    categories: dict = {}
    for folder in sorted(attacks_dir.iterdir()):
        if not folder.is_dir():
            continue
        cfg = folder / "attack.yaml"
        if not cfg.exists():
            continue
        try:
            d = yaml.safe_load(cfg.read_text(encoding="utf-8"))
            spec = _build_spec(d)
            category = d["category"]
        except Exception as e:
            import warnings
            warnings.warn(f"[loader] Skipping {cfg}: {e}")
            continue
        categories.setdefault(category, []).append(spec)
    return dict(sorted(categories.items(), key=lambda item: item[0]))


def _build_spec(d: dict):
    from modules.registry import AttackSpec, ParamSpec

    params = [_param_from_dict(p, ParamSpec) for p in d.get("params", [])]
    params.extend(_build_intensity_params(d.get("intensity_params", []), ParamSpec))
    return AttackSpec(
        id=d["id"],
        name=d["name"],
        description=d.get("description", ""),
        image=d["image"],
        container_name=d["container_name"],
        params=params,
        no_params_note=d.get("no_params_note"),
        details_warning=d.get("details_warning"),
        mitre=d.get("mitre"),
        max_runtime_s=d.get("max_runtime_s", 10),
        target_mapping=d.get("target_mapping"),
        docker_network=d.get("docker_network"),
    )


def _param_from_dict(p: dict, param_cls):
    return param_cls(
        key=p["key"],
        label=p.get("label", p["key"]),
        kind=p["kind"],
        placeholder=p.get("placeholder"),
        default=p.get("default"),
        validate=p.get("validate"),
        required=p.get("required", p.get("default") is None),
        positional=p.get("positional", True),
        env_var=p.get("env_var"),
    )


def _build_intensity_params(items, param_cls):
    params = []
    for item in items or []:
        if isinstance(item, str):
            key = item
            overrides = {}
        else:
            key = item["key"]
            overrides = dict(item)

        if key not in STANDARD_INTENSITY_PARAMS:
            raise ValueError(f"Unknown intensity param: {key}")

        spec = dict(STANDARD_INTENSITY_PARAMS[key])
        spec.update(overrides)
        spec["key"] = key
        spec.setdefault("required", False)
        spec.setdefault("positional", False)
        params.append(_param_from_dict(spec, param_cls))
    return params
