from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from modules.features import build_feature_paths, extract_with_ntlflowlyzer, extract_with_scapy, extract_with_tshark
from modules.attackzoo.attacks import _all_specs, _find_port_param, _find_target_param, _validate_param
from modules.attackzoo.capture import CAPTURES_DIR
from modules.attackzoo.common import _ensure_dir
from modules.attackzoo.reports.availability import generate_reports
from modules.attackzoo.reports.server_stats import generate_server_stats_reports
from modules.attackzoo.reports.stability import generate_reexecution_stability_reports
from modules.registry import CATEGORIES
from modules.runners import docker_available, docker_container_status, docker_logs, docker_rm_force, docker_run_detached


def cmd_status(_: argparse.Namespace) -> int:
    """Check whether Docker is reachable and report CLI readiness."""
    ok = docker_available()
    print("docker_available=" + ("true" if ok else "false"))
    return 0 if ok else 2


def cmd_list(args: argparse.Namespace) -> int:
    """List the registry catalog."""
    payload: Dict[str, Any] = {}

    for cat, specs in CATEGORIES.items():
        if args.category and args.category.lower() not in cat.lower():
            continue
        items = []
        for s in specs:
            if args.id and args.id != s.id:
                continue
            target_p = _find_target_param(s)
            params_display = []
            for p in (s.params or []):
                if p == target_p:
                    params_display.append({
                        "key": "target",
                        "label": "Target (IP or domain)",
                        "kind": p.kind,
                        "placeholder": p.placeholder,
                        "default": p.default,
                    })
                else:
                    params_display.append(asdict(p))
            items.append(
                {
                    "id": s.id,
                    "name": s.name,
                    "image": s.image,
                    "container": s.container_name,
                    "params": params_display,
                    "mitre": s.mitre,
                    "max_runtime_s": getattr(s, "max_runtime_s", None),
                }
            )
        if items:
            payload[cat] = items

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for cat, items in payload.items():
            print(cat)
            for it in items:
                param_parts = []
                for p in it["params"]:
                    k = p["key"]
                    d = f"={p['default']}" if p.get("default") is not None else ""
                    param_parts.append(f"--{k}{d}")
                params_str = "  [" + "  ".join(param_parts) + "]" if param_parts else ""
                print(f"  - {it['id']}: {it['name']}{params_str}")
    return 0


def cmd_captures(args: argparse.Namespace) -> int:
    """List captured PCAP files and any generated feature/dataset artifacts."""
    _ensure_dir(CAPTURES_DIR)
    pcaps = sorted(CAPTURES_DIR.glob("*.pcap"), key=lambda p: p.stat().st_mtime, reverse=True)
    if args.latest and pcaps:
        pcaps = pcaps[:1]

    rows = []
    for p in pcaps:
        base = p.name[:-5]
        feats = build_feature_paths(p)
        ds = Path("datasets") / f"unsupervised-{base}.csv"
        rows.append(
            {
                "pcap": str(p),
                "size": p.stat().st_size,
                "mtime": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
                "features": {k: str(v) for k, v in feats.items() if v.exists()},
                "dataset": str(ds) if ds.exists() else "",
            }
        )

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        for r in rows:
            print(r["pcap"])
            print(f"  size={r['size']} mtime={r['mtime']}")
            if r["features"]:
                print("  features:")
                for k, v in r["features"].items():
                    print(f"    - {k}: {v}")
            if r["dataset"]:
                print(f"  dataset: {r['dataset']}")
    return 0


def cmd_features(args: argparse.Namespace) -> int:
    """Extract configured feature sets from a PCAP capture."""
    pcap = Path(args.pcap)
    if not pcap.exists():
        print(f"PCAP not found: {pcap}", file=sys.stderr)
        return 2

    outs = build_feature_paths(pcap, features_dir=Path(args.outdir))
    tools = [t.strip() for t in args.tools.split(",") if t.strip()]

    results: Dict[str, Any] = {}
    if "ntlflowlyzer" in tools:
        results["ntlflowlyzer"] = extract_with_ntlflowlyzer(pcap, outs["ntlflowlyzer"])
    if "tshark" in tools:
        results["tshark"] = extract_with_tshark(pcap, outs["tshark"])
    if "scapy" in tools:
        results["scapy"] = extract_with_scapy(pcap, outs["scapy"])

    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


def cmd_dataset(args: argparse.Namespace) -> int:
    """Build an unsupervised dataset CSV for a capture."""
    from modules.datasets import build_dataset_unsupervised_for_capture

    pcap = Path(args.pcap)
    if not pcap.exists():
        print(f"PCAP not found: {pcap}", file=sys.stderr)
        return 2
    out = build_dataset_unsupervised_for_capture(
        pcap,
        features_dir=args.features_dir,
        outdir=args.outdir,
        save=True,
    )
    print(str(out))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Regenerate reports from a directory containing runs."""
    in_dir = Path(args.input)
    if not in_dir.exists():
        print(f"Directory not found: {in_dir}", file=sys.stderr)
        return 2

    # Accept probe_*.csv and probe.csv for backward compatibility.
    probe_files = sorted({
        p for p in list(in_dir.rglob("probe_*.csv")) + list(in_dir.rglob("probe.csv"))
        if "reports" not in p.parts
    })
    stats_files = list(in_dir.rglob("server_stats.csv"))
    resource_files = list(in_dir.rglob("resource.csv"))

    if not probe_files and not stats_files and not resource_files:
        print(f"No data files found in: {in_dir}", file=sys.stderr)
        return 2

    outdir = Path(args.outdir) if args.outdir else (in_dir / "reports")

    if probe_files:
        generate_reports(probe_files, outdir, args.warmup, args.attack, args.cooldown)
    else:
        print("[INFO] No probe files; F3/F4/T3 reports were not generated.", file=sys.stderr)

    if stats_files:
        generate_server_stats_reports(stats_files, outdir, args.warmup, args.attack, args.cooldown)

    # T6/T7/T8: reexecution, stability, and artifact metrics.
    generate_reexecution_stability_reports(in_dir, outdir, args.warmup, args.attack, args.cooldown)

    print(str(outdir))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Run an attack container directly by ID."""
    spec = _all_specs().get(args.attack_id)
    if not spec:
        print(f"[ERROR] Unknown attack id: {args.attack_id}", file=sys.stderr)
        print("[HINT] Use: python attackzoo.py list", file=sys.stderr)
        return 1

    # Parse extra kwargs from args.extra (e.g. ["--target_ip", "1.2.3.4"])
    resolved: Dict[str, Any] = {}
    extra = list(args.extra or [])
    it = iter(extra)
    for token in it:
        if token.startswith("--"):
            key = token[2:].replace("-", "_")
            try:
                val = next(it)
            except StopIteration:
                print(f"[ERROR] Missing value for {token}", file=sys.stderr)
                return 1
            resolved[key] = val

    # Resolve --target to the correct attack parameter.
    if getattr(args, "target", None):
        target_param = _find_target_param(spec)
        if target_param is None:
            print(
                f"[WARN] Attack '{spec.id}' has no mappable target parameter. "
                "--target ignored.",
                file=sys.stderr,
            )
        elif target_param.key not in resolved:
            resolved[target_param.key] = args.target

    # Resolve --port to the attack port parameter.
    if getattr(args, "port", None) is not None:
        port_param = _find_port_param(spec)
        if port_param is None:
            print(
                f"[WARN] Attack '{spec.id}' has no mappable port parameter. "
                "--port ignored.",
                file=sys.stderr,
            )
        elif port_param.key not in resolved:
            resolved[port_param.key] = args.port

    if getattr(args, "duration", None) is not None and any(p.key == "duration_s" for p in spec.params):
        resolved.setdefault("duration_s", int(args.duration))
    if getattr(args, "rate", None) is not None and any(p.key == "rate_pps" for p in spec.params):
        resolved.setdefault("rate_pps", int(args.rate))

    # Fill defaults and check required params
    for p in spec.params:
        if p.key not in resolved:
            if p.default is not None:
                resolved[p.key] = p.default
            elif p.required:
                print(f"[ERROR] Missing required param: --{p.key}", file=sys.stderr)
                return 1

    # Validate resolved params
    for p in spec.params:
        if p.key not in resolved and not p.required:
            continue
        err = _validate_param(p, str(resolved[p.key]))
        if err:
            print(f"[ERROR] {err}", file=sys.stderr)
            return 1

    # Build env vars for non-positional/intensity params.
    env: Dict[str, str] = spec.env_vars(resolved)
    if args.rate is not None:
        env["RATE"] = str(int(args.rate))
        env.setdefault("RATE_PPS", str(int(args.rate)))

    # Build positional args in YAML-param order ($1, $2, …)
    docker_args = spec.positional_args(resolved)

    result = docker_run_detached(
        image=spec.image,
        name=spec.container_name,
        args=docker_args,
        env=env or None,
        network=spec.network_mode(resolved),
    )
    if not result.get("ok"):
        print(f"[ERROR] {result.get('stderr', '')}", file=sys.stderr)
        return 1

    cid = result.get("container_id") or spec.container_name
    rate_info = f"  rate={args.rate} pkt/s (RATE env)" if args.rate else ""
    dur_info  = f"  duration={args.duration}s" if args.duration else ""
    print(f"[OK] Container started: {cid}{rate_info}{dur_info}")

    if args.duration:
        try:
            print(f"[INFO] Waiting {args.duration}s... (Ctrl+C to stop early)")
            time.sleep(args.duration)
        except KeyboardInterrupt:
            print()
        stop = docker_rm_force(spec.container_name)
        if stop.get("ok"):
            print(f"[OK] Stopped: {spec.container_name}")
        else:
            print(f"[WARN] Stop failed: {stop.get('stderr', '')}", file=sys.stderr)

    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    """Stop a running attack container."""
    spec = _all_specs().get(args.attack_id)
    if not spec:
        print(f"[ERROR] Unknown attack id: {args.attack_id}", file=sys.stderr)
        return 1
    result = docker_rm_force(spec.container_name)
    if result.get("ok"):
        print(f"[OK] Stopped: {spec.container_name}")
        return 0
    else:
        print(f"[ERROR] {result.get('stderr', '')}", file=sys.stderr)
        return 1


def cmd_ps(args: argparse.Namespace) -> int:
    """List attack containers and their states."""
    rows = []
    for specs in CATEGORIES.values():
        for s in specs:
            st = docker_container_status(s.container_name)
            status = st.get("status", "not_found")
            if not args.all and status not in ("running", "paused"):
                continue
            rows.append({
                "id": s.id,
                "container": s.container_name,
                "status": status,
                "container_id": st.get("id") or "",
            })

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        if not rows:
            print("No attack containers running. Use --all to show all.")
        else:
            print(f"{'STATUS':<12}  {'ATTACK ID':<42}  CONTAINER")
            for r in rows:
                print(f"  {r['status']:<10}  {r['id']:<42}  {r['container']}")
    return 0


def cmd_logs(args: argparse.Namespace) -> int:
    """Show logs from an attack container."""
    spec = _all_specs().get(args.attack_id)
    if not spec:
        print(f"[ERROR] Unknown attack id: {args.attack_id}", file=sys.stderr)
        return 1
    result = docker_logs(spec.container_name, tail=args.tail)
    if result.get("stdout"):
        print(result["stdout"])
    if result.get("stderr"):
        print(result["stderr"], file=sys.stderr)
    return 0 if result.get("ok") else 1
