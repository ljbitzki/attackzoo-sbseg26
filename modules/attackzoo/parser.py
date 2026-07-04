from __future__ import annotations

import argparse
import sys

from modules.features import FEATURES_DIR
from modules.attackzoo.commands import (
    cmd_captures,
    cmd_dataset,
    cmd_features,
    cmd_list,
    cmd_logs,
    cmd_ps,
    cmd_report,
    cmd_run,
    cmd_status,
    cmd_stop,
)
from modules.attackzoo.experiment import cmd_experiment
from modules.attackzoo.probes import SUPPORTED_PROBES


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level AttackZoo CLI parser and all subcommands."""
    p = argparse.ArgumentParser(prog="attackzoo.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Check prerequisites (Docker).")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("list", help="List registry attacks/categories.")
    s.add_argument("--category", default="")
    s.add_argument("--id", default="")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("captures", help="List captures in captures/*.pcap")
    s.add_argument("--latest", action="store_true")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_captures)

    s = sub.add_parser("features", help="Extract features from a PCAP.")
    s.add_argument("--pcap", required=True)
    s.add_argument("--tools", default="ntlflowlyzer,tshark,scapy")
    s.add_argument("--outdir", default=str(FEATURES_DIR))
    s.set_defaults(func=cmd_features)

    s = sub.add_parser("dataset", help="Generate an unsupervised dataset from a capture.")
    s.add_argument("--pcap", required=True)
    s.add_argument("--features-dir", default="features")
    s.add_argument("--outdir", default="datasets")
    s.set_defaults(func=cmd_dataset)


    s = sub.add_parser("report", help="Generate/regenerate reports (T3/F3/F4/T5/T6/T7/T8) from an experiment directory")
    s.add_argument("--input", required=True, help="Experiment base directory containing subdirectories with probe_*.csv or probe.csv")
    s.add_argument("--outdir", default="", help="Output directory (default: <input>/reports)")
    s.add_argument("--warmup", type=float, required=True)
    s.add_argument("--attack", type=float, required=True)
    s.add_argument("--cooldown", type=float, required=True)
    s.set_defaults(func=cmd_report)

    s = sub.add_parser(
        "experiment",
        help="Run an automated experiment with simultaneous probes, PCAP capture, and T3-T8 reports.",
        description=(
            "Runs warmup/attack/cooldown batches for a single attack across multiple levels.\n"
            "Results are saved in experiments/<out>/<attack_id>/<level>/run<N>/.\n"
            "L0 = baseline without attack (hooks are not called)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    def _exp_error(message, _s=s):
        """Print experiment-specific parser errors with the subcommand usage."""
        _s.print_usage(sys.stderr)
        _s.exit(2, f"\nexperiment: error: {message}\n")
    s.error = _exp_error  # type: ignore[method-assign]

    # Experiment identity
    s.add_argument("--attack-id", required=True,
                   help="Attack ID to run (for example: iot_mqtt_publisher). See: python attackzoo.py list")
    s.add_argument("--out", required=True,
                   help="Subdirectory under experiments/ where results are saved.")
    s.add_argument("--service", default="",
                   help="Service label for hook substitution ({service}). Default: --out value.")

    # Timing
    s.add_argument("--runs", type=int, default=10,
                   help="Number of runs per level (default: 10).")
    s.add_argument("--warmup", type=float, default=60,
                   help="Warmup phase duration in seconds (default: 60).")
    s.add_argument("--attack", type=float, default=120,
                   help="Attack window duration in seconds (default: 120).")
    s.add_argument("--cooldown", type=float, default=60,
                   help="Cooldown phase duration in seconds (default: 60).")
    s.add_argument("--interval", type=float, default=0.5,
                   help="Interval between probes in seconds (default: 0.5).")
    s.add_argument("--probe-timeout", type=float, default=2.0,
                   help="Per-probe timeout in seconds (default: 2.0).")

    # Capture and levels
    s.add_argument("--levels", default="L0,L1,L2,L3",
                   help="Comma-separated intensity levels (default: L0,L1,L2,L3).")
    s.add_argument("--iface", default="lo",
                   help="Network interface for tcpdump (default: lo).")
    s.add_argument("--bpf", default="tcp port 8080 or tcp port 1883",
                   help="BPF filter for tcpdump (default: 'tcp port 8080 or tcp port 1883').")

    # Probe endpoints
    s.add_argument("--probes", default="http,mqtt",
                   help=(
                       "Probe services to run, comma-separated: "
                       f"{', '.join(SUPPORTED_PROBES)} or all "
                       "(default: 'http,mqtt'). Use 'none' to capture traffic without availability probes."
                   ))
    s.add_argument("--http-url", default="http://127.0.0.1:8080/",
                   help="URL for HTTP probe (default: http://127.0.0.1:8080/).")
    s.add_argument("--https-url", default="https://127.0.0.1:8443/",
                   help="URL for HTTPS probe (default: https://127.0.0.1:8443/).")
    s.add_argument("--mqtt-host", default="127.0.0.1",
                   help="Host for MQTT probe (default: 127.0.0.1).")
    s.add_argument("--mqtt-port", type=int, default=1883,
                   help="Port for MQTT probe (default: 1883).")
    s.add_argument("--probe-host", default="",
                   help="Default host for probes without a specific endpoint (fallback: --host).")
    s.add_argument("--probe-port", type=int, default=0,
                   help="Default port for probes without a specific endpoint (0 uses the service default port).")
    s.add_argument("--probe-endpoint", action="append", default=[],
                   help=(
                       "Specific probe endpoint, repeatable: service=host:port or service=url. "
                       "Ex: --probe-endpoint ssh=172.17.0.3:22 --probe-endpoint https=https://127.0.0.1:8443/"
                   ))

    # Target for hooks
    s.add_argument("--host", default="127.0.0.1",
                   help="Target host injected as {host} in hook templates (default: 127.0.0.1).")
    s.add_argument("--port", type=int, default=None,
                   help="Target port injected as {port} in hook templates (default: 1883).")

    # Local host telemetry (/proc)
    s.add_argument("--collect-resources", action="store_true",
                   help="Collect local host CPU/load/memory through /proc and generate F5/T5 (resource.csv).")
    s.add_argument("--resource-interval", type=float, default=1.0,
                   help="Local host resource collection interval in seconds (default: 1.0).")

    # Target container telemetry (docker stats)
    s.add_argument("--server", default="",
                   help="Docker container name to monitor through 'docker stats' (for example: SBSeg26-server-mqtt-broker).")

    # Hooks
    s.add_argument("--attack-start-hook", default="",
                   help=(
                       "Command template called at the start of the attack window (only for levels != L0). "
                       "Available variables: {service} {attack_id} {level} {host} {port} {duration_s} {run_dir}"
                   ))
    s.add_argument("--attack-stop-hook", default="",
                   help="Command template called at the end of the attack window (only for levels != L0).")

    # Post-processing
    s.add_argument("--extract-features", action="store_true",
                   help="Extract features from the PCAP after each run.")
    s.add_argument("--build-dataset", action="store_true",
                   help="Build an unsupervised dataset after each run.")
    s.add_argument("--features-dir", default="features",
                   help="Output directory for features (default: features).")
    s.add_argument("--dataset-dir", default="datasets",
                   help="Output directory for datasets (default: datasets).")
    s.add_argument("--tools-ntl", action="store_true", help="Use ntlflowlyzer for feature extraction.")
    s.add_argument("--tools-tshark", action="store_true", help="Use tshark for feature extraction.")
    s.add_argument("--tools-scapy", action="store_true", help="Use scapy for feature extraction.")

    s.set_defaults(func=cmd_experiment)

    s = sub.add_parser("run", help="Run an attack container directly by ID.")
    s.add_argument("attack_id", help="Attack ID (see: list)")
    s.add_argument(
        "--duration", type=float, default=None, metavar="SECONDS",
        help="Automatically stop the container after N seconds (blocks until done).",
    )
    s.add_argument(
        "--rate", type=float, default=None, metavar="PPS",
        help="Packet/request rate per second. Injected as env var RATE=<N> "
             "in the container. The attack entrypoint.sh must support $RATE.",
    )
    s.add_argument(
        "--target", metavar="IP_OR_HOST", default=None,
        help=(
            "Target IP address or domain. Automatically mapped to the "
            "correct attack parameter (target_ip, target_net, etc.). "
            "Equivalent to --target_ip for most attacks."
        ),
    )
    s.add_argument(
        "--port", type=int, default=None, metavar="PORT",
        help=(
            "Target port. Automatically mapped to the attack port "
            "parameter (target_port, etc.). Equivalent to --target_port for "
            "most attacks."
        ),
    )
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("stop", help="Stop a running attack container.")
    s.add_argument("attack_id", help="Attack ID (see: list)")
    s.set_defaults(func=cmd_stop)

    s = sub.add_parser("ps", help="List attack containers and their states.")
    s.add_argument("--all", action="store_true", help="Show all states (default: only running/paused).")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_ps)

    s = sub.add_parser("logs", help="Show logs from an attack container.")
    s.add_argument("attack_id", help="Attack ID (see: list)")
    s.add_argument("--tail", type=int, default=200, metavar="N", help="Number of trailing lines (default: 200).")
    s.set_defaults(func=cmd_logs)

    return p
