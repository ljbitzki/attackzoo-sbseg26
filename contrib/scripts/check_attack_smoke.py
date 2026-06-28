#!/usr/bin/env python3
"""Smoke test runner for AttackZoo attack containers.

The script starts each attack container with minimal parameters, waits briefly,
collects Docker/app logs, records exit status, and removes the container.

It is intended to find image, entrypoint, argument, YAML/catalog, and obvious
application startup problems after rebuilding attack images.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.attackzoo.attacks import _all_specs, _validate_param  # noqa: E402


ISSUE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\btraceback\b",
        r"\bexception\b",
        r"\bsegmentation fault\b",
        r"\bcommand not found\b",
        r"\bno such file\b",
        r"\bpermission denied\b",
        r"\binvalid\b",
        r"\busage:",
        r"\bfailed\b",
        r"\berror\b",
        r"\bunable\b",
        r"\bcannot\b",
        r"\bcan't\b",
    ]
]


LOCAL_LINK_ATTACKS = {
    "net_arp_spoof",
    "net_cdp_table_flood",
    "net_dhcp_starvation",
    "net_stp_conf_flood",
    "net_stp_tcn_flood",
    "net_ipv6_mld_flood",
    "net_ipv6_ns_flood",
    "net_ipv6_ra_flood",
}


EXPECTED_LOG_PATTERNS = {
    "net_cdp_table_flood": [
        re.compile(r"^Error launching attack 1 \(mode 1\)!!$", re.IGNORECASE),
    ],
    "exf_icmp_tunnel": [
        re.compile(r"^Host key verification failed\.$", re.IGNORECASE),
    ],
    "iot_coap_token_collision": [
        re.compile(r"^Error request \d+: \[Errno 111\] received through errqueue$", re.IGNORECASE),
    ],
}


ATTACK_PARAM_DEFAULTS = {
    attack_id: {"duration_s": 3}
    for attack_id in {
        "iot_xrce_dds_entity_flood",
        "iot_xrce_dds_fragment_abuse",
        "iot_xrce_dds_malformed_inject",
        "iot_xrce_dds_session_hijack",
        "iot_xrce_dds_time_desync",
        "iot_xrce_dds_udp_dos",
    }
}
ATTACK_PARAM_DEFAULTS.update(
    {
        attack_id: {"duration_s": 4}
        for attack_id in {
            "iot_zenoh_pico_fragments_reassembly",
            "iot_zenoh_pico_keepalive_flood",
            "iot_zenoh_pico_memory_exhaustion",
            "iot_zenoh_pico_sequence_exhaustion",
            "iot_zenoh_pico_timestamp_mess",
        }
    }
)


DEFAULT_INTENSITY_DURATION_S = 1


@dataclasses.dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


@dataclasses.dataclass
class SmokeResult:
    attack_id: str
    name: str
    image: str
    category: str
    status: str
    passed: bool
    exit_code: Optional[int]
    issues: List[str]
    command: List[str]
    args: List[str]
    env: Dict[str, str]
    network: Optional[str]
    docker_stdout: str
    docker_stderr: str
    log_file: Optional[str]
    elapsed_s: float


def run_cmd(cmd: List[str], timeout_s: Optional[float] = None) -> CommandResult:
    try:
        proc = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        return CommandResult(proc.returncode, proc.stdout or "", proc.stderr or "")
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            124,
            exc.stdout or "",
            (exc.stderr or "") + f"\nTimeout after {timeout_s}s",
        )


def docker_available() -> bool:
    result = run_cmd(["docker", "version"], timeout_s=10)
    return result.returncode == 0


def docker_rm_force(name: str) -> None:
    run_cmd(["docker", "rm", "-f", name], timeout_s=10)


def docker_logs(name: str, tail: int) -> str:
    result = run_cmd(["docker", "logs", "--tail", str(tail), name], timeout_s=10)
    parts = []
    if result.stdout:
        parts.append(result.stdout)
    if result.stderr:
        parts.append(result.stderr)
    return "\n".join(parts).strip()


def docker_wait(name: str, timeout_s: float) -> Tuple[Optional[int], bool]:
    try:
        proc = subprocess.run(
            ["docker", "wait", name],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        if proc.returncode != 0:
            return None, False
        text = (proc.stdout or "").strip()
        return int(text) if text else None, False
    except subprocess.TimeoutExpired:
        return None, True


def parse_key_value(item: str) -> Tuple[str, str]:
    if "=" not in item:
        raise argparse.ArgumentTypeError(f"Expected KEY=VALUE, got {item!r}")
    key, value = item.split("=", 1)
    key = key.strip().replace("-", "_")
    if not key:
        raise argparse.ArgumentTypeError(f"Missing key in {item!r}")
    return key, value


def parse_attack_key_value(item: str) -> Tuple[str, str, str]:
    if ":" not in item:
        raise argparse.ArgumentTypeError(f"Expected ATTACK_ID:KEY=VALUE, got {item!r}")
    attack_id, rest = item.split(":", 1)
    key, value = parse_key_value(rest)
    return attack_id.strip(), key, value


def default_value_for_param(param: Any, args: argparse.Namespace) -> Any:
    key = param.key

    if key == "duration_s":
        if args.intensity_duration_s is not None:
            return args.intensity_duration_s
        return DEFAULT_INTENSITY_DURATION_S
    if key == "count":
        return args.intensity_count
    if key == "rate_pps":
        return args.intensity_rate_pps
    if key == "concurrency":
        return args.intensity_concurrency
    if key == "threads":
        return args.intensity_threads
    if key == "delay_ms":
        return args.intensity_delay_ms
    if key == "payload_size":
        return args.intensity_payload_size

    if param.default is not None:
        return param.default

    if key == "spoof_gw":
        return args.spoof_gw
    if param.kind == "cidr":
        return args.target_net
    if param.kind == "ip":
        return args.target_ip
    if param.kind == "port":
        return args.target_port
    if param.kind == "int":
        return 1
    if param.kind == "float":
        return 1.0
    return args.text_value


def resolve_params(spec: Any, args: argparse.Namespace) -> Tuple[Dict[str, Any], List[str]]:
    resolved: Dict[str, Any] = {}
    issues: List[str] = []

    global_overrides = dict(args.param or [])
    attack_overrides: Dict[str, Dict[str, str]] = {}
    for attack_id, key, value in args.attack_param or []:
        attack_overrides.setdefault(attack_id, {})[key] = value

    for param in spec.params:
        value = default_value_for_param(param, args)
        if args.intensity_duration_s is None and spec.id in ATTACK_PARAM_DEFAULTS:
            value = ATTACK_PARAM_DEFAULTS[spec.id].get(param.key, value)
        if param.key in global_overrides:
            value = global_overrides[param.key]
        if spec.id in attack_overrides and param.key in attack_overrides[spec.id]:
            value = attack_overrides[spec.id][param.key]

        if value is None and param.required:
            issues.append(f"missing required parameter {param.key}")
            continue
        if value is not None:
            err = _validate_param(param, str(value))
            if err:
                issues.append(err)
            resolved[param.key] = value

    return resolved, issues


def is_expected_log_issue(attack_id: str, line: str) -> bool:
    return any(pattern.search(line) for pattern in EXPECTED_LOG_PATTERNS.get(attack_id, []))


def find_log_issues(text: str, attack_id: str, max_items: int = 8) -> List[str]:
    issues: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if is_expected_log_issue(attack_id, line):
            continue
        if any(pattern.search(line) for pattern in ISSUE_PATTERNS):
            issues.append(line[:240])
            if len(issues) >= max_items:
                break
    return issues


def command_to_text(cmd: Iterable[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in cmd)


def run_smoke_for_attack(
    spec: Any,
    category: str,
    index: int,
    args: argparse.Namespace,
    out_dir: Path,
) -> SmokeResult:
    started = time.monotonic()
    resolved, param_issues = resolve_params(spec, args)
    positional_args = spec.positional_args(resolved)
    env_vars = spec.env_vars(resolved)
    network = spec.network_mode(resolved)

    safe_id = re.sub(r"[^a-zA-Z0-9_.-]", "-", spec.id)[:42]
    container_name = f"AttackZoo-smoke-{index:03d}-{safe_id}"

    env_flags: List[str] = []
    for key, value in sorted(env_vars.items()):
        env_flags.extend(["-e", f"{key}={value}"])

    network_flags = ["--network", network] if network else []
    cmd = ["docker", "run", "-d", "--name", container_name, *network_flags, *env_flags, spec.image, *positional_args]

    if args.dry_run:
        return SmokeResult(
            attack_id=spec.id,
            name=spec.name,
            image=spec.image,
            category=category,
            status="dry_run",
            passed=True,
            exit_code=None,
            issues=param_issues,
            command=cmd,
            args=positional_args,
            env=env_vars,
            network=network,
            docker_stdout="",
            docker_stderr="",
            log_file=None,
            elapsed_s=0,
        )

    docker_rm_force(container_name)
    run_result = run_cmd(cmd, timeout_s=args.docker_run_timeout_s)
    if run_result.returncode != 0:
        return SmokeResult(
            attack_id=spec.id,
            name=spec.name,
            image=spec.image,
            category=category,
            status="docker_run_failed",
            passed=False,
            exit_code=None,
            issues=param_issues + find_log_issues(run_result.stderr, spec.id),
            command=cmd,
            args=positional_args,
            env=env_vars,
            network=network,
            docker_stdout=run_result.stdout.strip(),
            docker_stderr=run_result.stderr.strip(),
            log_file=None,
            elapsed_s=time.monotonic() - started,
        )

    exit_code, timed_out = docker_wait(container_name, timeout_s=args.timeout_s)
    logs = docker_logs(container_name, tail=args.logs_tail)

    log_path = out_dir / "logs" / f"{spec.id}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(logs + ("\n" if logs else ""), encoding="utf-8")

    if timed_out:
        status = "started_and_killed"
        passed = True
    elif exit_code == 0:
        status = "exited_zero"
        passed = True
    else:
        status = "exited_nonzero"
        passed = False

    log_issues = find_log_issues(logs, spec.id)
    if log_issues and passed:
        status = f"{status}_with_log_warnings"
        if args.fail_on_log_warnings:
            passed = False

    if not args.keep_containers:
        docker_rm_force(container_name)

    return SmokeResult(
        attack_id=spec.id,
        name=spec.name,
        image=spec.image,
        category=category,
        status=status,
        passed=passed and not param_issues,
        exit_code=exit_code,
        issues=param_issues + log_issues,
        command=cmd,
        args=positional_args,
        env=env_vars,
        network=network,
        docker_stdout=run_result.stdout.strip(),
        docker_stderr=run_result.stderr.strip(),
        log_file=str(log_path.relative_to(REPO_ROOT)),
        elapsed_s=time.monotonic() - started,
    )


def select_specs(args: argparse.Namespace) -> List[Tuple[str, Any]]:
    selected: List[Tuple[str, Any]] = []
    include_ids = set(args.attack or [])
    skip_ids = set(args.skip or [])
    category_filter = (args.category or "").lower()

    for category, specs in sorted(_categories().items()):
        if category_filter and category_filter not in category.lower():
            continue
        for spec in specs:
            if include_ids and spec.id not in include_ids:
                continue
            if spec.id in skip_ids:
                continue
            if args.skip_local_link and spec.id in LOCAL_LINK_ATTACKS:
                continue
            selected.append((category, spec))
    return selected


def _categories() -> Dict[str, List[Any]]:
    from modules.registry import CATEGORIES

    return CATEGORIES


def write_reports(results: List[SmokeResult], out_dir: Path, args: argparse.Namespace) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "repo": str(REPO_ROOT),
        "options": {
            "timeout_s": args.timeout_s,
            "target_ip": args.target_ip,
            "target_net": args.target_net,
            "skip_local_link": args.skip_local_link,
            "dry_run": args.dry_run,
        },
        "summary": {
            "total": len(results),
            "passed": sum(1 for item in results if item.passed),
            "failed": sum(1 for item in results if not item.passed),
        },
        "results": [dataclasses.asdict(item) for item in results],
    }
    (out_dir / "results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# AttackZoo attack smoke check",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Total: `{payload['summary']['total']}`",
        f"- Passed: `{payload['summary']['passed']}`",
        f"- Failed: `{payload['summary']['failed']}`",
        f"- Timeout per attack: `{args.timeout_s}s`",
        "",
        "| Status | Attack | Exit | Issues | Log |",
        "|---|---|---:|---|---|",
    ]
    for item in results:
        icon = "PASS" if item.passed else "FAIL"
        exit_text = "" if item.exit_code is None else str(item.exit_code)
        issues = "; ".join(item.issues[:2])
        if len(item.issues) > 2:
            issues += f"; +{len(item.issues) - 2} more"
        log_link = item.log_file or ""
        lines.append(
            f"| {icon} `{item.status}` | `{item.attack_id}` | {exit_text} | "
            f"{issues.replace('|', '/')} | `{log_link}` |"
        )

    lines.extend(
        [
            "",
            "## Commands",
            "",
        ]
    )
    for item in results:
        lines.append(f"### `{item.attack_id}`")
        lines.append("")
        lines.append("```bash")
        lines.append(command_to_text(item.command))
        lines.append("```")
        lines.append("")

    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run minimal Docker smoke checks for AttackZoo attack containers.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--attack", action="append", help="Run only this attack id. Repeatable.")
    parser.add_argument("--skip", action="append", help="Skip this attack id. Repeatable.")
    parser.add_argument("--category", help="Run only categories containing this text.")
    parser.add_argument("--skip-local-link", action="store_true", help="Skip ARP/CDP/DHCP/STP/IPv6 local-link attacks.")
    parser.add_argument("--dry-run", action="store_true", help="Resolve parameters and write commands without running Docker.")
    parser.add_argument("--keep-containers", action="store_true", help="Do not remove smoke containers after each run.")
    parser.add_argument("--fail-on-log-warnings", action="store_true", help="Treat error-like log lines as failures.")
    parser.add_argument("--timeout-s", type=float, default=5.0, help="Seconds to wait before force-removing a still-running container.")
    parser.add_argument("--docker-run-timeout-s", type=float, default=20.0, help="Timeout for docker run itself.")
    parser.add_argument("--logs-tail", type=int, default=120, help="Number of log lines to collect per container.")
    parser.add_argument("--target-ip", default="127.0.0.1", help="Fallback value for required IP/FQDN parameters.")
    parser.add_argument("--target-net", default="127.0.0.0/30", help="Fallback value for required CIDR parameters.")
    parser.add_argument("--target-port", default=8080, type=int, help="Fallback value for required port parameters without YAML default.")
    parser.add_argument("--spoof-gw", default="127.0.0.1", help="Fallback value for spoof_gw.")
    parser.add_argument("--text-value", default="smoke", help="Fallback value for text parameters.")
    parser.add_argument(
        "--intensity-duration-s",
        type=int,
        default=None,
        help="Smoke value for duration_s. When omitted, most attacks use 1 and selected attacks use safer per-attack defaults.",
    )
    parser.add_argument("--intensity-count", type=int, default=1, help="Smoke value for count.")
    parser.add_argument("--intensity-rate-pps", type=int, default=1, help="Smoke value for rate_pps.")
    parser.add_argument("--intensity-concurrency", type=int, default=1, help="Smoke value for concurrency.")
    parser.add_argument("--intensity-threads", type=int, default=1, help="Smoke value for threads.")
    parser.add_argument("--intensity-delay-ms", type=int, default=0, help="Smoke value for delay_ms.")
    parser.add_argument("--intensity-payload-size", type=int, default=16, help="Smoke value for payload_size.")
    parser.add_argument(
        "--param",
        action="append",
        type=parse_key_value,
        help="Global parameter override KEY=VALUE. Repeatable.",
    )
    parser.add_argument(
        "--attack-param",
        action="append",
        type=parse_attack_key_value,
        help="Attack-specific override ATTACK_ID:KEY=VALUE. Repeatable.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory. Defaults to contrib/reports/attack-smoke-<timestamp>.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else REPO_ROOT / "contrib" / "reports" / f"attack-smoke-{timestamp}"
    out_dir = out_dir.resolve()

    selected = select_specs(args)
    if not selected:
        print("[ERROR] No attacks selected.", file=sys.stderr)
        return 2

    if not args.dry_run and not docker_available():
        print("[ERROR] Docker is not available to the current user/session.", file=sys.stderr)
        return 2

    if not args.skip_local_link and any(spec.id in LOCAL_LINK_ATTACKS for _, spec in selected):
        print(
            "[WARN] Local-link attacks are included. Use --skip-local-link to skip ARP/CDP/DHCP/STP/IPv6 local-link tests.",
            file=sys.stderr,
        )

    results: List[SmokeResult] = []
    total = len(selected)
    for index, (category, spec) in enumerate(selected, start=1):
        print(f"[{index:03d}/{total:03d}] {spec.id} ...", flush=True)
        result = run_smoke_for_attack(spec, category, index, args, out_dir)
        results.append(result)
        marker = "OK" if result.passed else "FAIL"
        print(f"    {marker}: {result.status} exit={result.exit_code} issues={len(result.issues)}", flush=True)

    write_reports(results, out_dir, args)
    failed = [item for item in results if not item.passed]

    print(f"\nReport: {out_dir / 'summary.md'}")
    print(f"JSON:   {out_dir / 'results.json'}")
    print(f"Passed: {len(results) - len(failed)}/{len(results)}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
