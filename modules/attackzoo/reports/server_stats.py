from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

def generate_server_stats_reports(
    stats_csv_files: Iterable[Path],
    outdir: Path,
    warmup: float,
    attack: float,
    cooldown: float,
) -> None:
    """Generates F6 (CPU time series), F7 (memory), and T4 from server_stats.csv.

    Robust version: if `server_stats.csv` exists with only a header, or if
    `docker stats` did not produce valid samples (for example, because the
    container name passed in --server is incorrect), processing emits WARN and continues without
    interrupting generation of the remaining reports.
    """
    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"[WARN] pandas/numpy/matplotlib unavailable. Could not generate stats charts. ({e})", file=sys.stderr)
        print("[HINT] pip install pandas numpy matplotlib", file=sys.stderr)
        return

    outdir.mkdir(parents=True, exist_ok=True)
    figs_dir = outdir / "figs"
    tabs_dir = outdir / "tables"
    figs_dir.mkdir(parents=True, exist_ok=True)
    tabs_dir.mkdir(parents=True, exist_ok=True)

    dfs = []
    skipped_empty = 0
    skipped_invalid = 0

    for f in stats_csv_files:
        try:
            df = pd.read_csv(f)
        except Exception:
            skipped_invalid += 1
            continue

        # Common case when --server was provided, but `docker stats` did not
        # obtain samples: the file exists but contains only a header.
        if df.empty:
            skipped_empty += 1
            continue

        df["run_id"] = f.parent.name
        # Expected structure: .../experiments/<out>/<attack_id>/<level>/run<N>/server_stats.csv
        parts = list(f.parts)
        if len(parts) >= 4:
            df["level"] = parts[-3]
            df["attack_id"] = parts[-4]
        else:
            df["level"] = "unknown"
            df["attack_id"] = "unknown"
        dfs.append(df)

    if not dfs:
        msg = "[WARN] No server_stats.csv with valid samples found; F6/F7/T4 will not be generated."
        if skipped_empty:
            msg += f" Empty/header-only files: {skipped_empty}."
        if skipped_invalid:
            msg += f" Invalid files: {skipped_invalid}."
        print(msg, file=sys.stderr)
        return

    data = pd.concat(dfs, ignore_index=True)
    if data.empty:
        print("[WARN] server_stats.csv has no data rows; F6/F7/T4 will not be generated.", file=sys.stderr)
        return

    # Ensure minimum columns to avoid KeyError on partial datasets.
    for col in ["attack_id", "level", "run_id", "phase"]:
        if col not in data.columns:
            data[col] = "unknown"
        data[col] = data[col].fillna("unknown").astype(str)

    numeric_cols = ["t_rel_s", "cpu_pct", "mem_usage_mb", "mem_limit_mb", "mem_pct", "net_rx_mb", "net_tx_mb"]
    for col in numeric_cols:
        if col not in data.columns:
            data[col] = np.nan
        data[col] = pd.to_numeric(data[col], errors="coerce")

    # Remove rows without a time axis or any useful telemetry.
    data = data.dropna(subset=["t_rel_s"], how="any")
    useful = ["cpu_pct", "mem_usage_mb", "mem_pct", "net_rx_mb", "net_tx_mb"]
    data = data.dropna(subset=useful, how="all")
    if data.empty:
        print("[WARN] server_stats.csv has no useful numeric samples; F6/F7/T4 will not be generated.", file=sys.stderr)
        return

    v1, v2, v3 = warmup, warmup + attack, warmup + attack + cooldown

    # F6 - CPU time series (target container)
    for (attack_id, level, run_id), g in data.groupby(["attack_id", "level", "run_id"], dropna=False):
        g = g.sort_values("t_rel_s")
        if g.empty:
            continue
        fig, ax = plt.subplots()
        ax.plot(g["t_rel_s"], g["cpu_pct"])
        ax.axvline(v1, linestyle="dotted", color="k")
        ax.axvline(v2, linestyle="dotted", color="k")
        ax.axvline(v3, linestyle="dotted", color="k")
        ax.set_title(f"F6 - CPU container | {attack_id} | {level} | {run_id}")
        ax.set_xlabel("Relative time (s) - Warmup | Attack | Cooldown")
        ax.set_ylabel("CPU (%)")
        fig.savefig(figs_dir / f"F6_cpu_{attack_id}_{level}_{run_id}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # F7 - Memory (MB on left axis, percent on right axis)
    for (attack_id, level, run_id), g in data.groupby(["attack_id", "level", "run_id"], dropna=False):
        g = g.sort_values("t_rel_s")
        if g.empty:
            continue
        fig, ax = plt.subplots()
        ax.plot(g["t_rel_s"], g["mem_usage_mb"], color="b")
        ax.axvline(v1, linestyle="dotted", color="k")
        ax.axvline(v2, linestyle="dotted", color="k")
        ax.axvline(v3, linestyle="dotted", color="k")
        ax.set_title(f"F7 - Memory container | {attack_id} | {level} | {run_id}")
        ax.set_xlabel("Relative time (s) - Warmup | Attack | Cooldown")
        ax.set_ylabel("Memory (MB)", color="b")
        ax2 = ax.twinx()
        ax2.plot(g["t_rel_s"], g["mem_pct"], color="r", linestyle="dashdot")
        ax2.set_ylabel("Memory (%)", color="r")
        fig.savefig(figs_dir / f"F7_mem_{attack_id}_{level}_{run_id}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # T4 - mean/max summary by (attack_id, level, run_id, phase)
    rows: List[Dict[str, Any]] = []
    for (attack_id, level, run_id, phase), g in data.groupby(
        ["attack_id", "level", "run_id", "phase"], dropna=False
    ):
        if g.empty:
            continue
        rows.append({
            "attack_id": attack_id,
            "level": level,
            "run_id": run_id,
            "phase": phase,
            "cpu_pct_mean": float(g["cpu_pct"].mean()) if len(g) else float("nan"),
            "cpu_pct_max": float(g["cpu_pct"].max()) if len(g) else float("nan"),
            "mem_usage_mb_mean": float(g["mem_usage_mb"].mean()) if len(g) else float("nan"),
            "mem_usage_mb_max": float(g["mem_usage_mb"].max()) if len(g) else float("nan"),
        })

    t4_cols = [
        "attack_id", "level", "run_id", "phase",
        "cpu_pct_mean", "cpu_pct_max", "mem_usage_mb_mean", "mem_usage_mb_max",
    ]
    t4 = pd.DataFrame(rows, columns=t4_cols)
    if t4.empty:
        print("[WARN] No aggregate row could be produced for T4_server_stats.csv.", file=sys.stderr)
        t4.to_csv(tabs_dir / "T4_server_stats.csv", index=False)
        return

    t4.sort_values(["attack_id", "level", "run_id", "phase"]).to_csv(
        tabs_dir / "T4_server_stats.csv", index=False
    )
