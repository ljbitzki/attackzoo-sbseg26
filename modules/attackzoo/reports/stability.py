from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

def _parse_iso_datetime(value: Any) -> Optional[datetime]:
    """Parses ISO timestamps generated in meta.json, accepting the Z suffix."""
    if not value:
        return None
    try:
        s = str(value).strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)
    except Exception:
        return None

def _csv_data_row_count(path: Path) -> int:
    """Counts CSV data rows, excluding the header."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            n = sum(1 for _ in f)
        return max(0, n - 1)
    except Exception:
        return 0


def _safe_file_size_mb(path: Path) -> float:
    """Return a file size in megabytes, or NaN when it cannot be read."""
    try:
        return path.stat().st_size / (1024.0 * 1024.0)
    except Exception:
        return float("nan")


def _read_meta_json(run_dir: Path) -> Dict[str, Any]:
    """Read a run's meta.json file, returning an empty dict on failure."""
    meta_path = run_dir / "meta.json"
    if not meta_path.exists():
        return {}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _first_existing_path(paths: Iterable[Any]) -> Optional[Path]:
    """Return the first existing path from a loose list of path-like values."""
    for raw in paths:
        if not raw:
            continue
        try:
            p = Path(str(raw))
            if p.exists():
                return p
        except Exception:
            continue
    return None


def _guess_pcap_path(run_dir: Path, meta: Dict[str, Any]) -> Optional[Path]:
    """Locate the PCAP associated with a run using metadata and local files."""
    candidates: List[Any] = []
    candidates.append(meta.get("pcap"))
    candidates.append(meta.get("pcap_path"))
    artifacts = meta.get("artifacts") if isinstance(meta.get("artifacts"), dict) else {}
    candidates.append(artifacts.get("pcap"))
    found = _first_existing_path(candidates)
    if found:
        return found
    pcaps = sorted(run_dir.glob("*.pcap"))
    return pcaps[0] if pcaps else None


def _probe_files_for_run(run_dir: Path, meta: Dict[str, Any]) -> List[Path]:
    """Collect all probe CSV files referenced by or present in a run folder."""
    paths: List[Path] = []
    artifacts = meta.get("artifacts") if isinstance(meta.get("artifacts"), dict) else {}
    for raw in (meta.get("probe_files") or []) + (artifacts.get("probes") or []):
        try:
            pp = Path(str(raw))
            if pp.exists() and pp not in paths:
                paths.append(pp)
        except Exception:
            pass
    for pp in sorted(list(run_dir.glob("probe_*.csv")) + [run_dir / "probe.csv"]):
        if pp.exists() and pp not in paths:
            paths.append(pp)
    return paths


def _feature_status(meta: Dict[str, Any]) -> Tuple[bool, int, int]:
    """Returns (requested, ok_count, total_count) from the features field."""
    requested = bool(meta.get("extract_features"))
    feats = meta.get("features") if isinstance(meta.get("features"), dict) else {}
    if feats:
        requested = True
    ok_count = 0
    total_count = 0
    for _, result in feats.items():
        total_count += 1
        if isinstance(result, dict):
            # Several project modules return {ok: bool, out/output/path: ...}.
            if result.get("ok") is True:
                ok_count += 1
                continue
            for key in ("out", "output", "path", "csv", "file"):
                if result.get(key) and Path(str(result[key])).exists():
                    ok_count += 1
                    break
        elif result:
            try:
                if Path(str(result)).exists():
                    ok_count += 1
            except Exception:
                pass
    return requested, ok_count, total_count


def _dataset_status(meta: Dict[str, Any]) -> Tuple[bool, str, bool, int]:
    """Summarize whether a dataset was requested, exists, and has data rows."""
    requested = bool(meta.get("build_dataset"))
    ds = str(meta.get("dataset") or "")
    if ds:
        requested = True
    exists = bool(ds and Path(ds).exists())
    rows = _csv_data_row_count(Path(ds)) if exists else 0
    return requested, ds, exists, rows


def _phase_counts(df: "pd.DataFrame") -> Dict[str, int]:  # type: ignore[name-defined]
    """Count probe rows per experiment phase."""
    out = {"warmup": 0, "attack": 0, "cooldown": 0}
    if "phase" not in df.columns:
        return out
    vc = df["phase"].astype(str).value_counts().to_dict()
    for k in out:
        out[k] = int(vc.get(k, 0))
    return out


def _latency_censored_values(g: "pd.DataFrame", timeout_marker_ms: float) -> Any:  # type: ignore[name-defined]
    """Replace failed probe latencies with a timeout marker for statistics."""
    lat = g["latency_ms"].copy()
    lat.loc[g["ok"] != 1] = timeout_marker_ms
    return lat.dropna().values


def _read_timeseries_phase_summary(path: Path, value_cols: List[str]) -> Dict[str, float]:
    """Summarizes resource.csv/server_stats.csv by phase to enrich the run table."""
    try:
        import pandas as pd
    except Exception:
        return {}
    if not path.exists():
        return {}
    try:
        df = pd.read_csv(path)
    except Exception:
        return {}
    if df.empty or "phase" not in df.columns:
        return {}
    out: Dict[str, float] = {}
    for col in value_cols:
        if col not in df.columns:
            continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
        for phase, g in df.groupby("phase", dropna=False):
            phase_s = str(phase)
            out[f"{col}_{phase_s}_mean"] = float(g[col].mean()) if len(g) else float("nan")
            out[f"{col}_{phase_s}_max"] = float(g[col].max()) if len(g) else float("nan")
    return out


def _write_latex_table_from_csv(csv_path: Path, tex_path: Path, caption: str, label: str, max_rows: int = 30) -> None:
    """Exports a simple LaTeX version of the main tables when pandas is available."""
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        if len(df) > max_rows:
            df = df.head(max_rows)
        tex = df.to_latex(index=False, escape=True, longtable=False, caption=caption, label=label)
        tex_path.write_text(tex, encoding="utf-8")
    except Exception:
        pass


def generate_reexecution_stability_reports(
    experiment_dir: Path,
    outdir: Path,
    warmup: float,
    attack: float,
    cooldown: float,
) -> None:
    """Generates tables for Section 5.2: reexecution, stability, and artifact validity.

    Main outputs in <outdir>/tables/:
      - T6_run_metrics.csv: one row per service/level/run.
      - T6_reexecution_stability.csv: mean, standard deviation, CV, and range by metric.
      - T7_artifact_validation.csv: acceptance criteria by run.
      - T8_artifact_summary.csv: summarized artifact inventory by run.

    This function is intentionally independent of a single service: it scans
    probe_*.csv and probe.csv under the experiment directory.
    """
    try:
        import numpy as np
        import pandas as pd
    except Exception as e:
        print(f"[WARN] pandas/numpy unavailable. Could not generate T6/T7/T8. ({e})", file=sys.stderr)
        print("[HINT] pip install pandas numpy", file=sys.stderr)
        return

    outdir.mkdir(parents=True, exist_ok=True)
    tabs_dir = outdir / "tables"
    tabs_dir.mkdir(parents=True, exist_ok=True)

    probe_files = sorted({
        p for p in list(experiment_dir.rglob("probe_*.csv")) + list(experiment_dir.rglob("probe.csv"))
        if "reports" not in p.parts
    })
    if not probe_files:
        print(f"[WARN] No probe CSV found for T6/T7/T8 in: {experiment_dir}", file=sys.stderr)
        return

    def pctl(x: Any, q: float) -> float:
        """Return a percentile value for a numeric sequence."""
        arr = np.asarray(x, dtype=float)
        return float(np.percentile(arr, q)) if arr.size else float("nan")

    run_rows: List[Dict[str, Any]] = []
    validation_by_run: Dict[str, Dict[str, Any]] = {}
    artifact_by_run: Dict[str, Dict[str, Any]] = {}

    for probe_file in sorted(probe_files):
        run_dir = probe_file.parent
        meta = _read_meta_json(run_dir)
        pcap_path = _guess_pcap_path(run_dir, meta)
        pcap_exists = bool(pcap_path and pcap_path.exists())
        pcap_size_mb = _safe_file_size_mb(pcap_path) if pcap_path else float("nan")
        pcap_nonempty = bool(pcap_exists and pcap_path and pcap_path.stat().st_size > 24)

        try:
            df = pd.read_csv(probe_file)
        except Exception:
            continue
        if df.empty:
            continue
        for col in ["t_rel_s", "ok", "latency_ms"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "ok" not in df.columns:
            df["ok"] = 0
        df["ok"] = df["ok"].fillna(0).astype(int)
        if "latency_ms" not in df.columns:
            df["latency_ms"] = np.nan
        if "phase" not in df.columns:
            df["phase"] = "unknown"

        service = str(df["service"].dropna().iloc[0]) if "service" in df.columns and df["service"].notna().any() else str(meta.get("service") or probe_file.stem.replace("probe_", ""))
        attack_id = str(df["attack_id"].dropna().iloc[0]) if "attack_id" in df.columns and df["attack_id"].notna().any() else str(meta.get("attack_id") or run_dir.parent.parent.name)
        level = str(df["level"].dropna().iloc[0]) if "level" in df.columns and df["level"].notna().any() else str(meta.get("level") or run_dir.parent.name)
        run_id = str(meta.get("run_id") or run_dir.name)

        timeout_marker_ms = float(meta.get("probe_timeout_s") or 2.0) * 1000.0
        try:
            observed_max = float(np.nanmax(df["latency_ms"].values))
            if np.isfinite(observed_max):
                timeout_marker_ms = max(timeout_marker_ms, observed_max)
        except Exception:
            pass

        row: Dict[str, Any] = {
            "service": service,
            "attack_id": attack_id,
            "level": level,
            "run_id": run_id,
            "probe_file": str(probe_file),
            "run_dir": str(run_dir),
            "timeout_marker_ms": timeout_marker_ms,
            "pcap_exists": int(pcap_exists),
            "pcap_nonempty": int(pcap_nonempty),
            "pcap_size_mb": pcap_size_mb,
        }

        counts = _phase_counts(df)
        for phase in ["warmup", "attack", "cooldown"]:
            g = df[df["phase"].astype(str) == phase].copy()
            lat_ok = g.loc[g["ok"] == 1, "latency_ms"].dropna().values
            lat_cens = _latency_censored_values(g, timeout_marker_ms) if len(g) else []
            row[f"samples_{phase}"] = int(counts.get(phase, 0))
            row[f"success_rate_{phase}_pct"] = float(g["ok"].mean() * 100.0) if len(g) else float("nan")
            row[f"fail_rate_{phase}_pct"] = float((1.0 - g["ok"].mean()) * 100.0) if len(g) else float("nan")
            row[f"lat_p50_{phase}_ms"] = pctl(lat_ok, 50)
            row[f"lat_p95_{phase}_ms"] = pctl(lat_ok, 95)
            row[f"lat_p99_{phase}_ms"] = pctl(lat_ok, 99)
            row[f"lat_p50_{phase}_censored_ms"] = pctl(lat_cens, 50)
            row[f"lat_p95_{phase}_censored_ms"] = pctl(lat_cens, 95)
            row[f"lat_p99_{phase}_censored_ms"] = pctl(lat_cens, 99)

        started = _parse_iso_datetime(meta.get("started_at_utc"))
        finished = _parse_iso_datetime(meta.get("finished_at_utc"))
        if started and finished:
            row["execution_time_s"] = max(0.0, (finished - started).total_seconds())
        else:
            row["execution_time_s"] = float("nan")

        # Artefatos derivados
        features_requested, feature_ok_count, feature_total_count = _feature_status(meta)
        dataset_requested, dataset_path, dataset_exists, dataset_rows = _dataset_status(meta)
        row["features_requested"] = int(features_requested)
        row["feature_extractors_total"] = int(feature_total_count)
        row["feature_extractors_ok"] = int(feature_ok_count)
        row["dataset_requested"] = int(dataset_requested)
        row["dataset_exists"] = int(dataset_exists)
        row["dataset_rows"] = int(dataset_rows)

        resource_csv = run_dir / "resource.csv"
        server_stats_csv = run_dir / "server_stats.csv"
        row["resource_csv_exists"] = int(resource_csv.exists())
        row["server_stats_csv_exists"] = int(server_stats_csv.exists())
        row.update(_read_timeseries_phase_summary(resource_csv, ["cpu_pct", "load1", "mem_used_pct", "mem_used_mb"]))
        row.update(_read_timeseries_phase_summary(server_stats_csv, ["cpu_pct", "mem_usage_mb", "mem_pct", "net_rx_mb", "net_tx_mb"]))

        run_rows.append(row)

        run_key = str(run_dir)
        if run_key not in validation_by_run:
            probe_paths = _probe_files_for_run(run_dir, meta)
            probe_phase_ok = True
            probe_rows_total = 0
            for pf in probe_paths:
                try:
                    pdf = pd.read_csv(pf)
                    probe_rows_total += len(pdf)
                    pc = _phase_counts(pdf)
                    probe_phase_ok = probe_phase_ok and all(pc.get(ph, 0) > 0 for ph in ["warmup", "attack", "cooldown"])
                except Exception:
                    probe_phase_ok = False

            metadata_exists = (run_dir / "meta.json").exists()
            metadata_traceable = bool(metadata_exists and meta.get("attack_id") and meta.get("level") and meta.get("run_id") and meta.get("started_at_utc") and meta.get("finished_at_utc"))
            feature_ok = (not features_requested) or (feature_total_count > 0 and feature_ok_count > 0)
            dataset_ok = (not dataset_requested) or bool(dataset_exists and dataset_rows > 0)
            resource_ok = (not bool(meta.get("collect_resources"))) or resource_csv.exists()
            server_stats_requested = bool(str(meta.get("server") or "").strip())
            server_stats_ok = (not server_stats_requested) or server_stats_csv.exists()

            criteria = {
                "capture_valid": pcap_nonempty,
                "probe_complete": bool(probe_paths and probe_rows_total > 0 and probe_phase_ok),
                "metadata_traceable": metadata_traceable,
                "features_valid_if_requested": feature_ok,
                "dataset_valid_if_requested": dataset_ok,
                "resources_valid_if_requested": resource_ok,
                "server_stats_valid_if_requested": server_stats_ok,
            }
            failed = [k for k, v in criteria.items() if not v]
            validation_by_run[run_key] = {
                "attack_id": attack_id,
                "level": level,
                "run_id": run_id,
                "run_dir": str(run_dir),
                **{k: int(v) for k, v in criteria.items()},
                "acceptance_pass": int(len(failed) == 0),
                "failed_criteria": ",".join(failed),
            }
            artifact_by_run[run_key] = {
                "attack_id": attack_id,
                "level": level,
                "run_id": run_id,
                "run_dir": str(run_dir),
                "pcap_path": str(pcap_path or ""),
                "pcap_size_mb": pcap_size_mb,
                "probe_files": ";".join(str(x) for x in probe_paths),
                "probe_rows_total": int(probe_rows_total),
                "meta_path": str(run_dir / "meta.json") if metadata_exists else "",
                "feature_extractors_total": int(feature_total_count),
                "feature_extractors_ok": int(feature_ok_count),
                "dataset_path": dataset_path,
                "dataset_rows": int(dataset_rows),
                "resource_csv": str(resource_csv) if resource_csv.exists() else "",
                "server_stats_csv": str(server_stats_csv) if server_stats_csv.exists() else "",
            }

    if not run_rows:
        print("[WARN] No run metric could be generated for T6.", file=sys.stderr)
        return

    run_df = pd.DataFrame(run_rows).sort_values(["service", "attack_id", "level", "run_id"])
    run_csv = tabs_dir / "T6_run_metrics.csv"
    run_df.to_csv(run_csv, index=False)

    metric_candidates = [
        "success_rate_warmup_pct",
        "success_rate_attack_pct",
        "success_rate_cooldown_pct",
        "fail_rate_attack_pct",
        "lat_p50_attack_censored_ms",
        "lat_p95_attack_censored_ms",
        "lat_p99_attack_censored_ms",
        "pcap_size_mb",
        "dataset_rows",
        "execution_time_s",
        "cpu_pct_attack_mean",
        "cpu_pct_attack_max",
        "mem_used_pct_attack_mean",
        "mem_used_pct_attack_max",
        "mem_usage_mb_attack_mean",
        "mem_usage_mb_attack_max",
    ]
    stability_rows: List[Dict[str, Any]] = []
    for (service, attack_id, level), g in run_df.groupby(["service", "attack_id", "level"], dropna=False):
        for metric in metric_candidates:
            if metric not in g.columns:
                continue
            vals = pd.to_numeric(g[metric], errors="coerce").dropna()
            if len(vals) == 0:
                continue
            mean = float(vals.mean())
            std = float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
            cv = float((std / abs(mean)) * 100.0) if mean not in (0.0, -0.0) and np.isfinite(mean) else float("nan")
            stability_rows.append({
                "service": service,
                "attack_id": attack_id,
                "level": level,
                "metric": metric,
                "n_runs": int(len(vals)),
                "mean": mean,
                "std_dev": std,
                "cv_pct": cv,
                "min": float(vals.min()),
                "max": float(vals.max()),
                "range": float(vals.max() - vals.min()),
            })
    stability_df = pd.DataFrame(stability_rows)
    stability_csv = tabs_dir / "T6_reexecution_stability.csv"
    if not stability_df.empty:
        stability_df.sort_values(["service", "attack_id", "level", "metric"]).to_csv(stability_csv, index=False)

    validation_df = pd.DataFrame(validation_by_run.values()).sort_values(["attack_id", "level", "run_id"])
    validation_csv = tabs_dir / "T7_artifact_validation.csv"
    validation_df.to_csv(validation_csv, index=False)

    artifact_df = pd.DataFrame(artifact_by_run.values()).sort_values(["attack_id", "level", "run_id"])
    artifact_csv = tabs_dir / "T8_artifact_summary.csv"
    artifact_df.to_csv(artifact_csv, index=False)

    # Quick LaTeX versions for pasting into the paper, keeping full CSVs as the source.
    _write_latex_table_from_csv(
        stability_csv,
        tabs_dir / "T6_reexecution_stability.tex",
        caption="Re-execution stability metrics across repeated AttackZoo runs.",
        label="tab:reexecution_stability",
        max_rows=40,
    )
    _write_latex_table_from_csv(
        validation_csv,
        tabs_dir / "T7_artifact_validation.tex",
        caption="Artifact validation and experimental acceptance criteria per run.",
        label="tab:artifact_validation",
        max_rows=40,
    )

    # Small JSON manifest to make produced artifacts easier to audit.
    manifest = {
        "experiment_dir": str(experiment_dir),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "tables": {
            "run_metrics": str(run_csv),
            "reexecution_stability": str(stability_csv),
            "artifact_validation": str(validation_csv),
            "artifact_summary": str(artifact_csv),
        },
        "timing": {"warmup_s": warmup, "attack_s": attack, "cooldown_s": cooldown},
    }
    (outdir / "metrics_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
