#!/usr/bin/env python3
"""Build traffic statistics and plots for an AttackZoo campaign."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CAMPAIGN_DIR = REPO_ROOT / "experiments" / "60att_5runs_l0l1l2l3"
DEFAULT_REPORTS_ROOT = REPO_ROOT / "contrib" / "reports"

TSHARK_FIELDS = (
    "frame.time_epoch",
    "frame.len",
    "ip.proto",
    "ipv6.nxt",
    "tcp.srcport",
    "tcp.dstport",
    "udp.srcport",
    "udp.dstport",
    "sctp.srcport",
    "sctp.dstport",
    "icmp.type",
    "icmpv6.type",
    "_ws.col.protocol",
)

FEATURE_FIELD_ALIASES = {
    "time_epoch": ("frame.time_epoch",),
    "frame_len": ("frame.len",),
    "ip_proto": ("ip.proto",),
    "ipv6_nxt": ("ipv6.nxt",),
    "tcp_srcport": ("tcp.srcport",),
    "tcp_dstport": ("tcp.dstport",),
    "udp_srcport": ("udp.srcport",),
    "udp_dstport": ("udp.dstport",),
    "sctp_srcport": ("sctp.srcport",),
    "sctp_dstport": ("sctp.dstport",),
    "icmp_type": ("icmp.type",),
    "icmpv6_type": ("icmpv6.type",),
    "ws_protocol": ("_ws.col.protocol", "_ws.col.Protocol"),
}

IP_PROTOCOLS = {
    "1": "ICMP",
    "2": "IGMP",
    "6": "TCP",
    "17": "UDP",
    "47": "GRE",
    "50": "ESP",
    "51": "AH",
    "58": "ICMPv6",
    "89": "OSPF",
    "132": "SCTP",
}

LEVEL_ORDER = ("L0", "L1", "L2", "L3")
LEVEL_COLORS = {
    "L0": "#1f77b4",
    "L1": "#ff7f0e",
    "L2": "#2ca02c",
    "L3": "#d62728",
}


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate packet/port/protocol/pps/Bps statistics from campaign PCAPs.",
    )
    parser.add_argument(
        "--campaign-dir",
        type=Path,
        default=DEFAULT_CAMPAIGN_DIR,
        help=f"Campaign directory. Default: {DEFAULT_CAMPAIGN_DIR}",
    )
    parser.add_argument(
        "--reports-root",
        type=Path,
        default=DEFAULT_REPORTS_ROOT,
        help=f"Root directory for reports. Default: {DEFAULT_REPORTS_ROOT}",
    )
    parser.add_argument(
        "--campaign-name",
        default=None,
        help="Report directory name. Default: basename of --campaign-dir.",
    )
    parser.add_argument(
        "--source",
        choices=("auto", "features", "pcap"),
        default="auto",
        help="Read existing tshark feature CSVs, PCAPs via tshark, or auto fallback. Default: auto.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocess all PCAPs instead of reusing file_summaries cache.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Process only the first N PCAPs; useful for smoke tests.",
    )
    parser.add_argument(
        "--top-ports",
        type=int,
        default=30,
        help="Number of ports shown in the port plot. CSVs include all ports.",
    )
    parser.add_argument(
        "--top-protocols",
        type=int,
        default=20,
        help="Number of protocols shown in the protocol plot. CSV includes all protocols.",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Only write CSV/JSON outputs, without PNG plots.",
    )
    parser.add_argument(
        "--progress-interval",
        type=int,
        default=25,
        help="Print progress every N processed PCAPs. Use 0 to disable.",
    )
    return parser.parse_args(argv)


def read_json(path: Path) -> Optional[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def sha1_text(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def find_pcaps(campaign_dir: Path) -> list[Path]:
    return sorted(
        path for path in campaign_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pcap"
    )


def parse_pcap_identity(campaign_dir: Path, pcap: Path) -> dict[str, Any]:
    rel = pcap.relative_to(campaign_dir)
    parts = rel.parts
    attack_id = parts[0] if parts else ""
    level = next((part for part in parts if part in LEVEL_ORDER), "")
    run_id = next((part for part in parts if part.startswith("run")), "")
    service = pcap.name.split("-", 1)[0] if "-" in pcap.name else ""
    meta = read_json(pcap.with_name("meta.json")) or {}
    return {
        "campaign_relative_path": str(rel),
        "attack_id": meta.get("attack_id") or attack_id,
        "level": meta.get("level") or level,
        "run_id": meta.get("run_id") or run_id,
        "service": meta.get("service") or service,
        "started_at_utc": meta.get("started_at_utc"),
        "finished_at_utc": meta.get("finished_at_utc"),
    }


def feature_csv_for_pcap(campaign_dir: Path, pcap: Path) -> Path:
    rel = pcap.relative_to(campaign_dir)
    attack_id = rel.parts[0]
    return campaign_dir / attack_id / "features" / f"tshark-{pcap.stem}.csv"


def summary_path_for_pcap(summary_dir: Path, campaign_dir: Path, pcap: Path) -> Path:
    rel = str(pcap.relative_to(campaign_dir))
    return summary_dir / f"{sha1_text(rel)}.json"


def first_value(value: str) -> str:
    # Tshark can emit multiple occurrences; occurrence=f should avoid this, but keep the parser defensive.
    if not value:
        return ""
    return value.split(",", 1)[0].strip().strip('"')


def to_int(value: str) -> Optional[int]:
    value = first_value(value)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return int(float(value))
        except ValueError:
            return None


def to_float(value: str) -> Optional[float]:
    value = first_value(value)
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def normalize_ws_protocol(value: str) -> str:
    value = first_value(value).strip()
    if not value:
        return "OTHER"
    upper = value.upper()
    if upper in {"TCP", "UDP", "ICMP", "ICMPV6", "ARP", "SCTP"}:
        return "ICMPv6" if upper == "ICMPV6" else upper
    if "ICMPV6" in upper or "ICMPV6" in upper.replace("-", ""):
        return "ICMPv6"
    if "ICMP" in upper:
        return "ICMP"
    if "TCP" in upper:
        return "TCP"
    if "UDP" in upper:
        return "UDP"
    if "ARP" in upper:
        return "ARP"
    return upper


def protocol_name(ip_proto: str, ipv6_nxt: str, ws_protocol: str, icmpv6_type: str) -> str:
    proto = first_value(ip_proto) or first_value(ipv6_nxt)
    if proto in IP_PROTOCOLS:
        return IP_PROTOCOLS[proto]
    if icmpv6_type:
        return "ICMPv6"
    return normalize_ws_protocol(ws_protocol)


def service_port(src: Optional[int], dst: Optional[int]) -> Optional[int]:
    ports = [port for port in (src, dst) if port is not None and port >= 0]
    if not ports:
        return None
    if len(ports) == 1:
        return ports[0]
    # For request and response packets this usually maps traffic back to the server-side port
    # instead of scattering counts across ephemeral client ports.
    return min(ports)


def packet_port(protocol: str, row: dict[str, str]) -> Optional[tuple[str, int]]:
    if protocol == "TCP":
        port = service_port(to_int(row.get("tcp_srcport", "")), to_int(row.get("tcp_dstport", "")))
        return ("TCP", port) if port is not None else None
    if protocol == "UDP":
        port = service_port(to_int(row.get("udp_srcport", "")), to_int(row.get("udp_dstport", "")))
        return ("UDP", port) if port is not None else None
    if protocol == "SCTP":
        port = service_port(to_int(row.get("sctp_srcport", "")), to_int(row.get("sctp_dstport", "")))
        return ("SCTP", port) if port is not None else None
    return None


def empty_summary(campaign_dir: Path, pcap: Path, source_path: Path, source_kind: str) -> dict[str, Any]:
    identity = parse_pcap_identity(campaign_dir, pcap)
    stat = pcap.stat()
    return {
        "schema_version": 1,
        "ok": True,
        "error": "",
        "source_kind": source_kind,
        "source_path": str(source_path),
        "pcap_path": str(pcap),
        "pcap_mtime_ns": stat.st_mtime_ns,
        "pcap_size_bytes": stat.st_size,
        **identity,
        "packet_count": 0,
        "byte_count": 0,
        "first_epoch": None,
        "last_epoch": None,
        "protocol_counts": {},
        "protocol_bytes": {},
        "port_counts": {},
        "port_bytes": {},
        "second_packet_counts": {},
        "second_byte_counts": {},
    }


def update_summary(summary: dict[str, Any], row: dict[str, str]) -> None:
    epoch = to_float(row.get("time_epoch", ""))
    frame_len = to_int(row.get("frame_len", "")) or 0
    protocol = protocol_name(
        row.get("ip_proto", ""),
        row.get("ipv6_nxt", ""),
        row.get("ws_protocol", ""),
        row.get("icmpv6_type", ""),
    )

    summary["packet_count"] += 1
    summary["byte_count"] += frame_len
    summary["protocol_counts"][protocol] = summary["protocol_counts"].get(protocol, 0) + 1
    summary["protocol_bytes"][protocol] = summary["protocol_bytes"].get(protocol, 0) + frame_len

    port_key = packet_port(protocol, row)
    if port_key is not None:
        key = f"{port_key[0]}/{port_key[1]}"
        summary["port_counts"][key] = summary["port_counts"].get(key, 0) + 1
        summary["port_bytes"][key] = summary["port_bytes"].get(key, 0) + frame_len

    if epoch is not None and math.isfinite(epoch):
        second = int(math.floor(epoch))
        second_key = str(second)
        summary["second_packet_counts"][second_key] = summary["second_packet_counts"].get(second_key, 0) + 1
        summary["second_byte_counts"][second_key] = summary["second_byte_counts"].get(second_key, 0) + frame_len
        if summary["first_epoch"] is None or epoch < summary["first_epoch"]:
            summary["first_epoch"] = epoch
        if summary["last_epoch"] is None or epoch > summary["last_epoch"]:
            summary["last_epoch"] = epoch


def read_feature_rows(path: Path) -> Iterable[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        indexes = {}
        for logical_name, aliases in FEATURE_FIELD_ALIASES.items():
            for alias in aliases:
                if alias in header:
                    indexes[logical_name] = header.index(alias)
                    break
        for row in reader:
            yield {
                logical_name: row[index] if index < len(row) else ""
                for logical_name, index in indexes.items()
            }


def read_tshark_rows(pcap: Path) -> Iterable[dict[str, str]]:
    tshark = shutil.which("tshark")
    if not tshark:
        raise RuntimeError("tshark not found in PATH")
    cmd = [
        tshark,
        "-r",
        str(pcap),
        "-T",
        "fields",
        "-E",
        "separator=,",
        "-E",
        "occurrence=f",
    ]
    for field in TSHARK_FIELDS:
        cmd.extend(["-e", field])
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        newline="",
    )
    assert proc.stdout is not None
    reader = csv.reader(proc.stdout)
    try:
        for row in reader:
            padded = row + [""] * (len(TSHARK_FIELDS) - len(row))
            yield {
                "time_epoch": padded[0],
                "frame_len": padded[1],
                "ip_proto": padded[2],
                "ipv6_nxt": padded[3],
                "tcp_srcport": padded[4],
                "tcp_dstport": padded[5],
                "udp_srcport": padded[6],
                "udp_dstport": padded[7],
                "sctp_srcport": padded[8],
                "sctp_dstport": padded[9],
                "icmp_type": padded[10],
                "icmpv6_type": padded[11],
                "ws_protocol": padded[12],
            }
    finally:
        stderr = proc.stderr.read() if proc.stderr is not None else ""
        returncode = proc.wait()
        if returncode != 0:
            raise RuntimeError(f"tshark exited with status {returncode}: {stderr.strip()}")


def process_pcap(campaign_dir: Path, pcap: Path, source: str) -> dict[str, Any]:
    feature_csv = feature_csv_for_pcap(campaign_dir, pcap)
    if source in {"auto", "features"} and feature_csv.exists():
        source_path = feature_csv
        source_kind = "features"
        rows = read_feature_rows(source_path)
    elif source == "features":
        raise FileNotFoundError(f"tshark feature CSV not found for {pcap}: {feature_csv}")
    else:
        source_path = pcap
        source_kind = "pcap"
        rows = read_tshark_rows(pcap)

    summary = empty_summary(campaign_dir, pcap, source_path, source_kind)
    for row in rows:
        update_summary(summary, row)
    return summary


def cached_summary_is_valid(summary: dict[str, Any], pcap: Path) -> bool:
    try:
        stat = pcap.stat()
    except OSError:
        return False
    return (
        summary.get("schema_version") == 1
        and summary.get("pcap_mtime_ns") == stat.st_mtime_ns
        and summary.get("pcap_size_bytes") == stat.st_size
    )


def load_or_process_summary(
    campaign_dir: Path,
    pcap: Path,
    summary_path: Path,
    source: str,
    force: bool,
) -> dict[str, Any]:
    if not force and summary_path.exists():
        cached = read_json(summary_path)
        if cached and cached_summary_is_valid(cached, pcap):
            return cached
    try:
        summary = process_pcap(campaign_dir, pcap, source)
    except Exception as exc:
        summary = empty_summary(campaign_dir, pcap, pcap, "error")
        summary["ok"] = False
        summary["error"] = str(exc)
    write_json(summary_path, summary)
    return summary


def add_counter(counter: Counter[str], payload: dict[str, int]) -> None:
    for key, value in payload.items():
        counter[key] += int(value)


def write_csv(path: Path, header: Sequence[str], rows: Iterable[Sequence[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def split_port_key(key: str) -> tuple[str, int]:
    protocol, port = key.split("/", 1)
    return protocol, int(port)


def aggregate_summaries(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    protocol_counts: Counter[str] = Counter()
    protocol_bytes: Counter[str] = Counter()
    port_counts: Counter[str] = Counter()
    port_bytes: Counter[str] = Counter()
    level_second_packets: Counter[tuple[str, int]] = Counter()
    level_second_bytes: Counter[tuple[str, int]] = Counter()
    first_second: Optional[int] = None
    last_second: Optional[int] = None

    for summary in summaries:
        if not summary.get("ok", False):
            continue
        add_counter(protocol_counts, summary.get("protocol_counts", {}))
        add_counter(protocol_bytes, summary.get("protocol_bytes", {}))
        add_counter(port_counts, summary.get("port_counts", {}))
        add_counter(port_bytes, summary.get("port_bytes", {}))
        level = summary.get("level") or "UNKNOWN"
        for second_text, count in summary.get("second_packet_counts", {}).items():
            second = int(second_text)
            level_second_packets[(level, second)] += int(count)
            if first_second is None or second < first_second:
                first_second = second
            if last_second is None or second > last_second:
                last_second = second
        for second_text, byte_count in summary.get("second_byte_counts", {}).items():
            level_second_bytes[(level, int(second_text))] += int(byte_count)

    return {
        "protocol_counts": protocol_counts,
        "protocol_bytes": protocol_bytes,
        "port_counts": port_counts,
        "port_bytes": port_bytes,
        "level_second_packets": level_second_packets,
        "level_second_bytes": level_second_bytes,
        "first_second": first_second,
        "last_second": last_second,
    }


def write_outputs(report_dir: Path, summaries: list[dict[str, Any]], aggregate: dict[str, Any]) -> dict[str, Path]:
    data_dir = report_dir / "data"
    protocol_counts: Counter[str] = aggregate["protocol_counts"]
    protocol_bytes: Counter[str] = aggregate["protocol_bytes"]
    port_counts: Counter[str] = aggregate["port_counts"]
    port_bytes: Counter[str] = aggregate["port_bytes"]
    total_packets = sum(protocol_counts.values())
    total_bytes = sum(protocol_bytes.values())

    protocol_rows = []
    for protocol, packet_count in protocol_counts.most_common():
        byte_count = protocol_bytes[protocol]
        protocol_rows.append(
            (
                protocol,
                packet_count,
                byte_count,
                packet_count / total_packets if total_packets else 0.0,
                byte_count / total_bytes if total_bytes else 0.0,
            )
        )
    protocol_csv = data_dir / "protocol_packet_counts.csv"
    write_csv(
        protocol_csv,
        ("protocol", "packet_count", "byte_count", "packet_fraction", "byte_fraction"),
        protocol_rows,
    )

    port_rows = []
    by_port_counts: Counter[str] = Counter()
    by_port_bytes: Counter[str] = Counter()
    for key, packet_count in port_counts.most_common():
        protocol, port = split_port_key(key)
        byte_count = port_bytes[key]
        by_port_counts[str(port)] += packet_count
        by_port_bytes[str(port)] += byte_count
        port_rows.append(
            (
                protocol,
                port,
                f"{protocol}/{port}",
                packet_count,
                byte_count,
                packet_count / total_packets if total_packets else 0.0,
                byte_count / total_bytes if total_bytes else 0.0,
            )
        )
    port_csv = data_dir / "port_packet_counts.csv"
    write_csv(
        port_csv,
        ("transport", "port", "port_label", "packet_count", "byte_count", "packet_fraction", "byte_fraction"),
        port_rows,
    )

    by_port_rows = [
        (
            int(port),
            packet_count,
            by_port_bytes[port],
            packet_count / total_packets if total_packets else 0.0,
            by_port_bytes[port] / total_bytes if total_bytes else 0.0,
        )
        for port, packet_count in by_port_counts.most_common()
    ]
    port_aggregate_csv = data_dir / "port_packet_counts_by_port.csv"
    write_csv(
        port_aggregate_csv,
        ("port", "packet_count", "byte_count", "packet_fraction", "byte_fraction"),
        by_port_rows,
    )

    first_second = aggregate["first_second"]
    level_rows = []
    for (level, epoch_second), packet_count in sorted(aggregate["level_second_packets"].items()):
        byte_count = aggregate["level_second_bytes"].get((level, epoch_second), 0)
        campaign_second = epoch_second - first_second if first_second is not None else 0
        level_rows.append((level, campaign_second, epoch_second, packet_count, byte_count, packet_count, byte_count))
    level_csv = data_dir / "level_second_rates.csv"
    write_csv(
        level_csv,
        ("level", "campaign_second", "epoch_second", "packet_count", "byte_count", "pps", "Bps"),
        level_rows,
    )

    file_rows = []
    for summary in summaries:
        file_rows.append(
            (
                summary.get("ok"),
                summary.get("level"),
                summary.get("attack_id"),
                summary.get("run_id"),
                summary.get("service"),
                summary.get("packet_count"),
                summary.get("byte_count"),
                summary.get("first_epoch"),
                summary.get("last_epoch"),
                summary.get("source_kind"),
                summary.get("campaign_relative_path"),
                summary.get("error"),
            )
        )
    file_csv = data_dir / "pcap_file_summaries.csv"
    write_csv(
        file_csv,
        (
            "ok",
            "level",
            "attack_id",
            "run_id",
            "service",
            "packet_count",
            "byte_count",
            "first_epoch",
            "last_epoch",
            "source_kind",
            "campaign_relative_path",
            "error",
        ),
        file_rows,
    )

    return {
        "protocol_csv": protocol_csv,
        "port_csv": port_csv,
        "port_aggregate_csv": port_aggregate_csv,
        "level_csv": level_csv,
        "file_csv": file_csv,
    }


def import_plotting():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    return plt, pd


def plot_outputs(report_dir: Path, csv_paths: dict[str, Path], top_ports: int, top_protocols: int) -> dict[str, Path]:
    plt, pd = import_plotting()
    figures_dir = report_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}

    protocol_df = pd.read_csv(csv_paths["protocol_csv"]).head(top_protocols)
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    colors = plt.get_cmap("tab20").colors
    ax.bar(protocol_df["protocol"], protocol_df["packet_count"], color=colors[: len(protocol_df)])
    ax.set_title("Packet Count by Protocol")
    ax.set_xlabel("Protocol")
    ax.set_ylabel("Packet count")
    ax.ticklabel_format(axis="y", style="plain")
    ax.grid(axis="y", alpha=0.25)
    ax.tick_params(axis="x", rotation=35)
    path = figures_dir / "01_protocol_packet_counts.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    outputs["protocol_plot"] = path

    port_df = pd.read_csv(csv_paths["port_csv"]).head(top_ports)
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    ax.bar(port_df["port_label"], port_df["packet_count"], color=colors[: len(port_df)])
    ax.set_title("Packet Count by Port")
    ax.set_xlabel("Port")
    ax.set_ylabel("Packet count")
    ax.ticklabel_format(axis="y", style="plain")
    ax.grid(axis="y", alpha=0.25)
    ax.tick_params(axis="x", rotation=45)
    path = figures_dir / "02_port_packet_counts.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    outputs["port_plot"] = path

    rates_df = pd.read_csv(csv_paths["level_csv"])
    for metric, ylabel, filename, title in (
        ("pps", "Packets per second (pps)", "03_pps_by_level_over_campaign_seconds.png", "PPS by Level over Campaign Seconds"),
        ("Bps", "Bytes per second (Bps)", "04_Bps_by_level_over_campaign_seconds.png", "Bps by Level over Campaign Seconds"),
    ):
        fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
        for level in LEVEL_ORDER:
            sub = rates_df[rates_df["level"] == level].sort_values("campaign_second")
            if sub.empty:
                continue
            ax.plot(
                sub["campaign_second"],
                sub[metric],
                label=level,
                color=LEVEL_COLORS.get(level),
                linewidth=1.2,
                alpha=0.85,
            )
        ax.set_title(title)
        ax.set_xlabel("Campaign second")
        ax.set_ylabel(ylabel)
        ax.ticklabel_format(axis="y", style="plain")
        ax.grid(alpha=0.25)
        ax.legend(title="Level")
        path = figures_dir / filename
        fig.savefig(path, dpi=180, bbox_inches="tight")
        plt.close(fig)
        outputs[f"{metric}_plot"] = path

    return outputs


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    campaign_dir = args.campaign_dir.resolve()
    if not campaign_dir.is_dir():
        print(f"[ERROR] Campaign directory not found: {campaign_dir}", file=sys.stderr)
        return 2

    report_name = args.campaign_name or campaign_dir.name
    report_dir = (args.reports_root.resolve() / report_name)
    summary_dir = report_dir / "file_summaries"
    report_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    pcaps = find_pcaps(campaign_dir)
    if args.max_files is not None:
        pcaps = pcaps[: args.max_files]
    if not pcaps:
        print(f"[ERROR] No PCAP files found under {campaign_dir}", file=sys.stderr)
        return 2

    summaries: list[dict[str, Any]] = []
    for index, pcap in enumerate(pcaps, start=1):
        summary_path = summary_path_for_pcap(summary_dir, campaign_dir, pcap)
        summary = load_or_process_summary(campaign_dir, pcap, summary_path, args.source, args.force)
        summaries.append(summary)
        if args.progress_interval > 0 and (index % args.progress_interval == 0 or index == len(pcaps)):
            status = "ok" if summary.get("ok") else "error"
            print(f"[progress] {index}/{len(pcaps)} {status} {pcap.relative_to(campaign_dir)}", file=sys.stderr)

    aggregate = aggregate_summaries(summaries)
    csv_paths = write_outputs(report_dir, summaries, aggregate)
    plot_paths: dict[str, Path] = {}
    plot_error = ""
    if not args.no_plots:
        try:
            plot_paths = plot_outputs(report_dir, csv_paths, args.top_ports, args.top_protocols)
        except ModuleNotFoundError as exc:
            plot_error = f"plot dependencies missing: {exc}"
            print(f"[WARN] {plot_error}; CSV outputs were still written.", file=sys.stderr)

    ok_count = sum(1 for summary in summaries if summary.get("ok"))
    packet_total = sum(aggregate["protocol_counts"].values())
    byte_total = sum(aggregate["protocol_bytes"].values())
    manifest = {
        "generated_at_utc": utc_now(),
        "campaign_dir": str(campaign_dir),
        "report_dir": str(report_dir),
        "source": args.source,
        "processed_pcap_count": len(summaries),
        "ok_pcap_count": ok_count,
        "error_pcap_count": len(summaries) - ok_count,
        "packet_total": packet_total,
        "byte_total": byte_total,
        "first_epoch_second": aggregate["first_second"],
        "last_epoch_second": aggregate["last_second"],
        "csv_outputs": {key: str(value) for key, value in csv_paths.items()},
        "plot_outputs": {key: str(value) for key, value in plot_paths.items()},
        "plot_error": plot_error,
    }
    write_json(report_dir / "manifest.json", manifest)

    print("Traffic statistics")
    print(f"- Report dir: {report_dir}")
    print(f"- PCAPs processed: {ok_count}/{len(summaries)}")
    print(f"- Packets counted: {packet_total}")
    print(f"- Bytes counted: {byte_total}")
    print(f"- CSV outputs: {report_dir / 'data'}")
    if plot_paths:
        print(f"- Plot outputs: {report_dir / 'figures'}")
    return 0 if ok_count == len(summaries) else 1


if __name__ == "__main__":
    raise SystemExit(main())
