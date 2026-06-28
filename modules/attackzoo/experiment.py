from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from modules.features import build_feature_paths, extract_with_ntlflowlyzer, extract_with_scapy, extract_with_tshark
from modules.attackzoo.attacks import _all_specs
from modules.attackzoo.capture import start_tcpdump
from modules.attackzoo.common import _stop_proc
from modules.attackzoo.probes import SUPPORTED_PROBES, normalize_probe_service, probe_default_port, probe_loop
from modules.attackzoo.reports.availability import generate_reports
from modules.attackzoo.reports.server_stats import generate_server_stats_reports
from modules.attackzoo.reports.stability import generate_reexecution_stability_reports
from modules.attackzoo.telemetry import docker_stats_loop, resource_loop


def _start_hook(cmd_template: str, vars_: Dict[str, Any]) -> Optional[subprocess.Popen]:
    if not cmd_template.strip():
        return None
    cmd = cmd_template.format(**vars_)
    # shell=True allows user-defined redirections and pipes
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)


def _parse_probe_services(raw: str) -> List[str]:
    services: List[str] = []
    for item in (raw or "").split(","):
        token = item.strip().lower()
        if not token or token == "none":
            continue
        if token == "all":
            for svc in SUPPORTED_PROBES:
                if svc not in services:
                    services.append(svc)
            continue
        svc = normalize_probe_service(token)
        if svc not in services:
            services.append(svc)
    return services


def _split_host_port(value: str) -> Dict[str, Any]:
    value = value.strip()
    if not value:
        return {}
    if value.startswith("["):
        host, _, rest = value[1:].partition("]")
        port_s = rest[1:] if rest.startswith(":") else ""
        return {"host": host, "port": int(port_s)} if port_s else {"host": host}
    host, sep, port_s = value.rpartition(":")
    if sep and port_s.isdigit():
        return {"host": host, "port": int(port_s)}
    return {"host": value}


def _parse_probe_endpoints(raw_items: List[str]) -> Dict[str, Dict[str, Any]]:
    endpoints: Dict[str, Dict[str, Any]] = {}
    for raw in raw_items or []:
        if "=" not in raw:
            raise ValueError(f"--probe-endpoint is invalid: {raw!r}; use service=host:port or service=url")
        service_raw, value = raw.split("=", 1)
        svc = normalize_probe_service(service_raw)
        value = value.strip()
        if "://" in value:
            endpoints[svc] = {"url": value}
        else:
            endpoints[svc] = _split_host_port(value)
    return endpoints


def _url_from_endpoint(scheme: str, endpoint: Dict[str, Any], default_url: str) -> str:
    if endpoint.get("url"):
        return str(endpoint["url"])
    if endpoint.get("host"):
        host = str(endpoint["host"])
        port = int(endpoint.get("port") or probe_default_port(scheme))
        return f"{scheme}://{host}:{port}/"
    return default_url


def _probe_endpoint_for(
    *,
    service: str,
    args: argparse.Namespace,
    explicit_endpoints: Dict[str, Dict[str, Any]],
    probe_count: int,
) -> Dict[str, Any]:
    endpoint = dict(explicit_endpoints.get(service, {}))
    if service == "http":
        return {"url": _url_from_endpoint("http", endpoint, args.http_url)}
    if service == "https":
        return {"url": _url_from_endpoint("https", endpoint, args.https_url)}
    if service == "mqtt":
        return {
            "host": str(endpoint.get("host") or args.mqtt_host),
            "port": int(endpoint.get("port") or args.mqtt_port),
        }

    host = str(endpoint.get("host") or args.probe_host or args.host or "127.0.0.1")
    port = int(endpoint.get("port") or args.probe_port or 0)
    if not port and getattr(args, "port", None) is not None and probe_count == 1:
        port = int(args.port)
    if not port:
        port = probe_default_port(service)
    return {"host": host, "port": port}


def cmd_experiment(args: argparse.Namespace) -> int:
    """Run warmup/attack/cooldown batches with simultaneous probes, PCAP capture, and reports."""
    # Validate attack_id
    spec = _all_specs().get(args.attack_id)
    if spec is None:
        print(f"[ERROR] Attack id '{args.attack_id}' not found.", file=sys.stderr)
        print("[HINT]  Run: python attackzoo.py list", file=sys.stderr)
        return 1

    base_dir = Path("experiments") / args.out
    base_dir.mkdir(parents=True, exist_ok=True)

    levels = [x.strip() for x in args.levels.split(",") if x.strip()]
    service_label = args.service or args.out
    try:
        probe_services = _parse_probe_services(args.probes)
        explicit_endpoints = _parse_probe_endpoints(args.probe_endpoint)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 2

    probe_files: List[Path] = []
    stats_csv_files: List[Path] = []

    for level in levels:
        for run_num in range(1, args.runs + 1):
            run_id = f"run{run_num:02d}"
            run_dir = base_dir / args.attack_id / level / run_id
            run_dir.mkdir(parents=True, exist_ok=True)

            pcap_label = service_label
            pcap_path = run_dir / f"{pcap_label}-{args.attack_id}-{level}-{run_id}.pcap"
            resource_csv = run_dir / "resource.csv"
            stats_csv = run_dir / "server_stats.csv"
            meta_path = run_dir / "meta.json"

            stop_evt = threading.Event()

            probe_threads: List[threading.Thread] = []
            run_probe_files: List[Path] = []
            probe_endpoints: Dict[str, Dict[str, Any]] = {}
            for probe_service in probe_services:
                endpoint = _probe_endpoint_for(
                    service=probe_service,
                    args=args,
                    explicit_endpoints=explicit_endpoints,
                    probe_count=len(probe_services),
                )
                probe_csv = run_dir / f"probe_{probe_service}.csv"
                probe_endpoints[probe_service] = endpoint
                run_probe_files.append(probe_csv)
                probe_threads.append(threading.Thread(
                    target=probe_loop,
                    kwargs={
                        "out_csv": probe_csv,
                        "service": probe_service,
                        "endpoint": endpoint,
                        "attack_id": args.attack_id,
                        "level": level,
                        "warmup": args.warmup,
                        "attack": args.attack,
                        "cooldown": args.cooldown,
                        "interval": args.interval,
                        "timeout_s": args.probe_timeout,
                        "stop_evt": stop_evt,
                    },
                    daemon=True,
                ))

            # Optional local host resource collection thread
            thr_res: Optional[threading.Thread] = None
            if args.collect_resources:
                thr_res = threading.Thread(
                    target=resource_loop,
                    kwargs={
                        "out_csv": resource_csv,
                        "service": service_label,
                        "attack_id": args.attack_id,
                        "level": level,
                        "warmup": args.warmup,
                        "attack": args.attack,
                        "cooldown": args.cooldown,
                        "interval": args.resource_interval,
                        "stop_evt": stop_evt,
                    },
                    daemon=True,
                )

            # Optional docker stats thread for the target container
            thr_stats: Optional[threading.Thread] = None
            if args.server.strip():
                thr_stats = threading.Thread(
                    target=docker_stats_loop,
                    kwargs={
                        "container_name": args.server,
                        "out_csv": stats_csv,
                        "warmup": args.warmup,
                        "attack": args.attack,
                        "cooldown": args.cooldown,
                        "stop_evt": stop_evt,
                    },
                    daemon=True,
                )

            for thr_probe in probe_threads:
                thr_probe.start()
            if thr_res:
                thr_res.start()
            if thr_stats:
                thr_stats.start()

            tcp = None
            try:
                tcp = start_tcpdump(pcap_path, iface=args.iface, bpf=args.bpf)
            except FileNotFoundError:
                print("[WARN] tcpdump not found; PCAP capture will be skipped.", file=sys.stderr)

            started_at = datetime.now(timezone.utc).isoformat()

            # Warmup
            time.sleep(args.warmup)

            # Attack-start hook (not called for L0)
            hook_p: Optional[subprocess.Popen] = None
            hook_vars = {
                "service": service_label,
                "attack_id": args.attack_id,
                "level": level,
                "host": args.host,
                "port": int(args.port) if args.port is not None else 1883,
                "duration_s": args.attack,
                "run_dir": str(run_dir),
            }
            if level != "L0" and args.attack_start_hook.strip():
                hook_p = _start_hook(args.attack_start_hook, hook_vars)

            time.sleep(args.attack)

            # Attack-stop hook (not called for L0)
            if level != "L0" and args.attack_stop_hook.strip():
                _start_hook(args.attack_stop_hook, hook_vars)
            _stop_proc(hook_p, timeout=2.0)

            # Cooldown
            time.sleep(args.cooldown)

            stop_evt.set()
            for thr_probe in probe_threads:
                thr_probe.join(timeout=5.0)
            if thr_res:
                thr_res.join(timeout=5.0)
            if thr_stats:
                thr_stats.join(timeout=5.0)
            _stop_proc(tcp, timeout=3.0)

            # Optional feature extraction
            feature_results: Dict[str, Any] = {}
            dataset_path = ""
            if args.extract_features:
                use_ntl = args.tools_ntl
                use_tshark = args.tools_tshark
                use_scapy = args.tools_scapy
                if not (use_ntl or use_tshark or use_scapy):
                    use_ntl = use_tshark = use_scapy = True
                feat_paths = build_feature_paths(pcap_path, features_dir=Path(args.features_dir))
                if use_ntl:
                    feature_results["ntlflowlyzer"] = extract_with_ntlflowlyzer(pcap_path, feat_paths["ntlflowlyzer"])
                if use_tshark:
                    feature_results["tshark"] = extract_with_tshark(pcap_path, feat_paths["tshark"])
                if use_scapy:
                    feature_results["scapy"] = extract_with_scapy(pcap_path, feat_paths["scapy"])

            if args.build_dataset:
                from modules.datasets import build_dataset_unsupervised_for_capture

                dataset_path = str(
                    build_dataset_unsupervised_for_capture(
                        pcap_path,
                        features_dir=args.features_dir,
                        outdir=args.dataset_dir,
                        save=True,
                    )
                )

            meta = {
                "service": service_label,
                "attack_id": args.attack_id,
                "level": level,
                "run_id": run_id,
                "started_at_utc": started_at,
                "finished_at_utc": datetime.now(timezone.utc).isoformat(),
                "warmup_s": args.warmup,
                "attack_s": args.attack,
                "cooldown_s": args.cooldown,
                "pcap": str(pcap_path),
                "probe_files": [str(p) for p in run_probe_files],
                "resource_csv": str(resource_csv) if args.collect_resources else "",
                "server_stats_csv": str(stats_csv) if args.server.strip() else "",
                "probe_services": list(probe_services),
                "probe_endpoints": probe_endpoints,
                "probe_timeout_s": args.probe_timeout,
                "iface": args.iface,
                "bpf": args.bpf,
                "http_url": args.http_url,
                "https_url": args.https_url,
                "mqtt_host": args.mqtt_host,
                "mqtt_port": int(args.mqtt_port),
                "server": args.server,
                "collect_resources": args.collect_resources,
                "resource_interval_s": args.resource_interval,
                "attack_start_hook": args.attack_start_hook,
                "attack_stop_hook": args.attack_stop_hook,
                "extract_features": bool(args.extract_features),
                "build_dataset": bool(args.build_dataset),
                "features_dir": args.features_dir,
                "dataset_dir": args.dataset_dir,
                "features": feature_results,
                "dataset": dataset_path,
                "artifacts": {
                    "pcap": str(pcap_path),
                    "probes": [str(p) for p in run_probe_files],
                    "resource_csv": str(resource_csv) if args.collect_resources else "",
                    "server_stats_csv": str(stats_csv) if args.server.strip() else "",
                    "dataset": dataset_path,
                },
            }
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

            probe_files.extend(run_probe_files)
            if args.server.strip() and stats_csv.exists():
                stats_csv_files.append(stats_csv)

            print(f"[OK] {args.attack_id} {level} {run_id}")

    # Reports
    rep_dir = base_dir / "reports"
    generate_reports(probe_files, rep_dir, args.warmup, args.attack, args.cooldown)
    if stats_csv_files:
        generate_server_stats_reports(stats_csv_files, rep_dir, args.warmup, args.attack, args.cooldown)
    # T6/T7/T8: reexecution, stability, and artifact-validity metrics.
    generate_reexecution_stability_reports(base_dir, rep_dir, args.warmup, args.attack, args.cooldown)
    print(str(rep_dir))
    return 0
