# datasets.py
from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import Iterable, Union, List
import pandas as pd

PathLike = Union[str, Path]
def _ensure_dir(path: PathLike) -> Path:
    """
    Ensure the output directory exists.

    :param path: Relative path.
    :type path: PathLike
    :return: Absolute path for validation and creation, if needed.
    :rtype: Path
    """
    p = Path(path)
    if p.suffix:
        p.parent.mkdir(parents=True, exist_ok=True)
    else:
        p.mkdir(parents=True, exist_ok=True)
    return p

def _detect_source_tool(df: pd.DataFrame, path: Path) -> str:
    """
    

    :param df: Dataframes pandas
    :type df: pd.DataFrame
    :param path: DataFrame path.
    :type path: Path
    :return: Return the likely source tool name.
    :rtype: str
    """
    name = path.name.lower()

    # NTLFlowLyzer (flow-level)
    if "ntlflowlyzer-" in name or "flow_id" in df.columns or "packets_IAT_mean" in df.columns:
        return "ntlflowlyzer"

    # TShark (packet-level) - conforme seu extractor atual
    if "tshark-" in name and "frame.number" in df.columns and "frame.time_epoch" in df.columns:
        return "tshark_packets"

    # Scapy (packet-level) - conforme seu extractor atual
    if "scapy-" in name and "pkt_index" in df.columns and "time_epoch" in df.columns:
        return "scapy_packets"

    return "unknown"

def _normalize_ntlflowlyzer(df: pd.DataFrame) -> pd.DataFrame:
    """
    NTLFlowLyzer normalization.       

    :param df: Dataframe pandas
    :type df: pd.DataFrame
    :return: New normalized DataFrame.
    :rtype: pd.DataFrame
    """
    df = df.copy()

    # standardize minimum column names
    rename_map = {
        "protocol": "proto",
        "duration": "dur",
        "packets_count": "pkts",
    }
    df = df.rename(columns=rename_map)

    # bytes = payload + header
    if "total_payload_bytes" in df.columns and "total_header_bytes" in df.columns:
        df["bytes"] = pd.to_numeric(df["total_payload_bytes"], errors="coerce").fillna(0) + \
                      pd.to_numeric(df["total_header_bytes"], errors="coerce").fillna(0)

    # minimum timestamp
    if "timestamp" in df.columns:
        df["ts"] = pd.to_numeric(df["timestamp"], errors="coerce")
    else:
        df["ts"] = pd.NA

    # rename internal label to avoid labeling at this stage
    if "label" in df.columns:
        df = df.rename(columns={"label": "ntlflow_label"})

    # ensure minimum types
    for col in ["src_port", "dst_port", "proto", "dur", "pkts", "bytes", "ts"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def _normalize_tshark_packets(df: pd.DataFrame) -> pd.DataFrame:
    """
    TShark normalization.       

    :param df: Dataframe pandas
    :type df: pd.DataFrame
    :return: New normalized DataFrame.
    :rtype: pd.DataFrame
    """
    df = df.copy()

    # Campos do extrator:
    # frame.time_epoch, frame.len, ip.src, ip.dst, ip.proto, tcp.srcport, tcp.dstport, udp.srcport, udp.dstport
    df["ts"] = pd.to_numeric(df.get("frame.time_epoch"), errors="coerce")
    df["bytes"] = pd.to_numeric(df.get("frame.len"), errors="coerce")

    df["src_ip"] = df.get("ip.src")
    df["dst_ip"] = df.get("ip.dst")
    df["proto"] = pd.to_numeric(df.get("ip.proto"), errors="coerce")

    # port: try TCP, then UDP
    df["src_port"] = pd.to_numeric(df.get("tcp.srcport"), errors="coerce")
    df["dst_port"] = pd.to_numeric(df.get("tcp.dstport"), errors="coerce")

    df["src_port"] = df["src_port"].fillna(pd.to_numeric(df.get("udp.srcport"), errors="coerce"))
    df["dst_port"] = df["dst_port"].fillna(pd.to_numeric(df.get("udp.dstport"), errors="coerce"))

    # packet-level => pkts = 1
    df["pkts"] = 1

    return df

def _normalize_scapy_packets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Scapy normalization.

    :param df: Dataframe pandas
    :type df: pd.DataFrame
    :return: New normalized DataFrame.
    :rtype: pd.DataFrame
    """
    df = df.copy()

    # Campos do extrator:
    # time_epoch, frame_len, ip_src, ip_dst, ip_proto, src_port, dst_port
    
    df["ts"] = pd.to_numeric(df.get("time_epoch"), errors="coerce")
    df["bytes"] = pd.to_numeric(df.get("frame_len"), errors="coerce")
    df["src_ip"] = df.get("ip_src")
    df["dst_ip"] = df.get("ip_dst")
    df["proto"] = pd.to_numeric(df.get("ip_proto"), errors="coerce")
    df["src_port"] = pd.to_numeric(df.get("src_port"), errors="coerce")
    df["dst_port"] = pd.to_numeric(df.get("dst_port"), errors="coerce")

    df["pkts"] = 1
    return df

def _normalize_common(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    General-purpose normalization.

    :param df: DataFrame.
    :type df: pd.DataFrame
    :param source: DataFrame source.
    :type source: str
    :return: Normalized DataFrame.
    :rtype: pd.DataFrame
    """
    if source == "ntlflowlyzer":
        df = _normalize_ntlflowlyzer(df)
    elif source == "tshark_packets":
        df = _normalize_tshark_packets(df)
    elif source == "scapy_packets":
        df = _normalize_scapy_packets(df)
    else:
        df = df.copy()
        df["ts"] = pd.NA
        df["bytes"] = pd.NA
        df["pkts"] = pd.NA

    df["source_tool"] = source
    return df

def load_features(csv_paths: Union[PathLike, Iterable[PathLike]]) -> pd.DataFrame:
    """
    Load features.

    :param csv_paths: CSV file paths.
    :type csv_paths: Union[PathLike, Iterable[PathLike]]
    :raises FileNotFoundError: Error raised when the file is not found.
    :raises ValueError: Error raised when the file has no workable values.
    :return: Dataframe
    :rtype: pd.DataFrame
    """
    if isinstance(csv_paths, (str, Path)):
        csv_paths = [csv_paths]

    dfs: List[pd.DataFrame] = []
    for path in csv_paths:
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"CSV file not found: {p}")

        df = pd.read_csv(p, engine="python")
        source = _detect_source_tool(df, p)

        df_norm = _normalize_common(df, source)
        df_norm["__source_csv"] = p.name
        dfs.append(df_norm)

    if not dfs:
        raise ValueError("No values provided.")

    return pd.concat(dfs, ignore_index=True)

def build_dataset_unsupervised_for_capture(
    capture_pcap: PathLike,
    *,
    features_dir: PathLike = "features",
    outdir: PathLike = "datasets",
    save: bool = True,
) -> Path:
    """
    Build the unsupervised dataset for a single capture.
    Automatically looks for ntlflowlyzer-<base>.csv, tshark-<base>.csv, and scapy-<base>.csv.
    Saves datasets/unsupervised-<base>.csv.

    :param capture_pcap: Capture file.
    :type capture_pcap: PathLike
    :param features_dir: Feature directory, defaults to "features/".
    :type features_dir: PathLike, optional
    :param outdir: Dataset directory, defaults to "datasets/".
    :type outdir: PathLike, optional
    :param save: Boolean that controls whether to save to disk, defaults to True.
    :type save: bool, optional
    :raises FileNotFoundError: Error raised when the file is not found.
    :return: Full saved dataset path.
    :rtype: Path
    """
    capture_pcap = Path(capture_pcap)
    base = capture_pcap.name[:-5] if capture_pcap.name.lower().endswith(".pcap") else capture_pcap.stem

    feats_dir = Path(features_dir)
    candidates = [
        feats_dir / f"ntlflowlyzer-{base}.csv",
        feats_dir / f"tshark-{base}.csv",
        feats_dir / f"scapy-{base}.csv",
    ]
    csvs = [p for p in candidates if p.exists()]
    if not csvs:
        raise FileNotFoundError(f"No feature CSV found for {base} in {feats_dir}")

    df = load_features(csvs)

    if save:
        _ensure_dir(outdir)
        out_path = Path(outdir) / f"unsupervised-{base}.csv"
        df.to_csv(out_path, index=False)
        return out_path

    return Path(outdir) / f"unsupervised-{base}.csv"
