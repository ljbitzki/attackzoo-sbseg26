from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

def generate_reports(probe_csv_files: Iterable[Path], outdir: Path, warmup: float, attack: float, cooldown: float) -> None:
    """
    Generate tables and figures from probe_*.csv or probe.csv files.

    Versions:
      - F3 (v1): latency for successful probes only (compatible with the previous version)
      - F3 (v2): censored latency (failures mapped to timeout) + success_rate (rolling window)
      - F4 (v1): CDF for successful probes only
      - F4 (v2): censored CDF (includes failures as timeout) + failure-rate plot (warmup vs attack)

    Requer: pandas / numpy / matplotlib.
    """
    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"[WARN] Missing pandas/numpy/matplotlib. Could not generate plots. ({e})", file=sys.stderr)
        print("[HINT] pip install pandas numpy matplotlib", file=sys.stderr)
        return

    outdir.mkdir(parents=True, exist_ok=True)
    figs_dir = outdir / "figs"
    tabs_dir = outdir / "tables"
    figs_dir.mkdir(parents=True, exist_ok=True)
    tabs_dir.mkdir(parents=True, exist_ok=True)

    dfs = []
    for f in probe_csv_files:
        df = pd.read_csv(f)
        df["run_id"] = f.parent.name
        df["run_dir"] = str(f.parent)
        dfs.append(df)
    if not dfs:
        print("[WARN] No probe_*.csv/probe.csv found for report generation.", file=sys.stderr)
        return

    data = pd.concat(dfs, ignore_index=True)
    data["t_rel_s"] = pd.to_numeric(data["t_rel_s"], errors="coerce")
    data["ok"] = pd.to_numeric(data["ok"], errors="coerce").fillna(0).astype(int)
    data["latency_ms"] = pd.to_numeric(data["latency_ms"], errors="coerce")

    resource_dfs = []
    for run_dir in {f.parent for f in probe_csv_files}:
        rf = run_dir / "resource.csv"
        if not rf.exists():
            continue
        rdf = pd.read_csv(rf)
        rdf["run_id"] = run_dir.name
        rdf["run_dir"] = str(run_dir)
        resource_dfs.append(rdf)
    resources = pd.concat(resource_dfs, ignore_index=True) if resource_dfs else None
    if resources is not None and len(resources):
        for col in ["t_rel_s", "cpu_pct", "load1", "load5", "load15", "mem_used_pct", "mem_used_mb", "mem_available_mb", "mem_total_mb"]:
            if col in resources.columns:
                resources[col] = pd.to_numeric(resources[col], errors="coerce")

    def pctl(x, q):
        x = np.asarray(x, dtype=float)
        return float(np.percentile(x, q)) if x.size else np.nan

    # ------------------------------------------------------------------
    # T3 (v1): metrics for successful probes only (compatible)
    # ------------------------------------------------------------------
    rows_v1: List[Dict[str, Any]] = []
    for (service, attack_id, level, phase), g in data.groupby(["service", "attack_id", "level", "phase"], dropna=False):
        lat_ok = g.loc[g["ok"] == 1, "latency_ms"].dropna().values
        rows_v1.append(
            {
                "service": service,
                "attack_id": attack_id,
                "level": level,
                "phase": phase,
                "n_samples": int(len(g)),
                "success_rate": float(g["ok"].mean()) if len(g) else np.nan,
                "lat_p50_ms": pctl(lat_ok, 50),
                "lat_p95_ms": pctl(lat_ok, 95),
                "lat_p99_ms": pctl(lat_ok, 99),
            }
        )
    pd.DataFrame(rows_v1).sort_values(["service", "attack_id", "level", "phase"]).to_csv(tabs_dir / "T3_summary.csv", index=False)

    # ------------------------------------------------------------------
    # Helpers for censored versions
    # ------------------------------------------------------------------
    def _read_meta_timeout_ms(run_dir: str, default_timeout_s: float = 2.0) -> float:
        """Try to read meta.json, if present, to obtain probe_timeout_s in the future."""
        try:
            mp = Path(run_dir) / "meta.json"
            if mp.exists():
                meta = json.loads(mp.read_text(encoding="utf-8"))
                t = meta.get("probe_timeout_s", None)
                if isinstance(t, (int, float)) and t > 0:
                    return float(t) * 1000.0
        except Exception:
            pass
        return float(default_timeout_s) * 1000.0

    def _timeout_marker_ms(g: "pd.DataFrame") -> float:
        """
        Value used to censor failures in the chart/CDF.
        Rule:
          1) try meta.json (probe_timeout_s), fallback 2000ms
          2) use the largest observed value as the floor
        """
        base = _read_meta_timeout_ms(str(g["run_dir"].iloc[0])) if "run_dir" in g.columns and len(g) else 2000.0
        observed_max = float(np.nanmax(g["latency_ms"].values)) if len(g) else base
        return max(base, observed_max)

    def _rolling_window_n(g: "pd.DataFrame", window_s: float = 5.0) -> int:
        t = g["t_rel_s"].dropna().values
        if len(t) < 3:
            return 1
        dt = np.median(np.diff(np.sort(t)))
        if not np.isfinite(dt) or dt <= 0:
            return 1
        return max(1, int(round(window_s / dt)))

    # ------------------------------------------------------------------
    # T3 (v2): include failures as timeout (censored) + fail_rate
    # ------------------------------------------------------------------
    rows_v2: List[Dict[str, Any]] = []
    for (service, attack_id, level, phase), g in data.groupby(["service", "attack_id", "level", "phase"], dropna=False):
        tm = _timeout_marker_ms(g)
        lat_cens = g["latency_ms"].copy()
        lat_cens.loc[g["ok"] != 1] = tm
        lat_cens = lat_cens.dropna().values
        rows_v2.append(
            {
                "service": service,
                "attack_id": attack_id,
                "level": level,
                "phase": phase,
                "n_samples": int(len(g)),
                "success_rate": float(g["ok"].mean()) if len(g) else np.nan,
                "fail_rate": float(1.0 - g["ok"].mean()) if len(g) else np.nan,
                "timeout_marker_ms": tm,
                "lat_p50_ms_censored": pctl(lat_cens, 50),
                "lat_p95_ms_censored": pctl(lat_cens, 95),
                "lat_p99_ms_censored": pctl(lat_cens, 99),
            }
        )
    pd.DataFrame(rows_v2).sort_values(["service", "attack_id", "level", "phase"]).to_csv(
        tabs_dir / "T3_summary_censored.csv", index=False
    )

    # ------------------------------------------------------------------
    # F3 (v1): compatible
    # ------------------------------------------------------------------
    v1, v2, v3 = warmup, warmup + attack, warmup + attack + cooldown
    for (service, attack_id, level, run_id), g in data.groupby(["service", "attack_id", "level", "run_id"], dropna=False):
        g = g.sort_values("t_rel_s")
        lat = g["latency_ms"].where(g["ok"] == 1)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(g["t_rel_s"], lat)
        ax.axvline(v1, linestyle="dotted", color="k")
        ax.axvline(v2, linestyle="dotted", color="k")
        ax.axvline(v3, linestyle="dotted", color="k")
        ax.set_title(f"F3 (v1) - Latency | {service} | {attack_id} | {level} | {run_id}")
        ax.set_xlabel("Relative time (s) - Warmup | Attack | Cooldown")
        ax.set_ylabel("Latency (ms) (successful probes only)")
        fig.savefig(figs_dir / f"F3_v1_timeseries_{service}_{attack_id}_{level}_{run_id}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ------------------------------------------------------------------
    # F3 (v2): censored latency + success_rate (rolling window)
    # ------------------------------------------------------------------
    for (service, attack_id, level, run_id), g in data.groupby(["service", "attack_id", "level", "run_id"], dropna=False):
        g = g.sort_values("t_rel_s").reset_index(drop=True)

        tm = _timeout_marker_ms(g)
        lat_cens = g["latency_ms"].copy()
        lat_cens.loc[g["ok"] != 1] = tm

        win_n = _rolling_window_n(g, window_s=5.0)
        sr = g["ok"].rolling(window=win_n, min_periods=1).mean()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(g["t_rel_s"], lat_cens, color="r")
        ax.axvline(v1, linestyle="dotted", color="k")
        ax.axvline(v2, linestyle="dotted", color="k")
        ax.axvline(v3, linestyle="dotted", color="k")
        ax.set_title(f"F3 (v2) - Latency censurada + sucesso | {service} | {attack_id} | {level} | {run_id}")
        ax.set_xlabel("Relative time (s) - Warmup | Attack | Cooldown")
        ax.set_ylabel(f"Latency (ms) (failures={tm:.0f}ms)", color="r")

        ax2 = ax.twinx()
        ax2.plot(g["t_rel_s"], sr, linestyle="dashdot", color="g")
        ax2.set_ylabel(f"Success rate (window ~{win_n} samples)", color='g')

        fig.savefig(figs_dir / f"F3_v2_censored_sr_{service}_{attack_id}_{level}_{run_id}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ------------------------------------------------------------------
    # F4 (v1) — CDF for successful probes only
    # ------------------------------------------------------------------
    def cdf(x):
        x = np.sort(x)
        y = np.arange(1, len(x) + 1) / len(x)
        return x, y

    for (service, attack_id, level), g in data.groupby(["service", "attack_id", "level"], dropna=False):
        warm = g[(g["phase"] == "warmup") & (g["ok"] == 1)]["latency_ms"].dropna().values
        attk = g[(g["phase"] == "attack") & (g["ok"] == 1)]["latency_ms"].dropna().values
        if warm.size < 5 or attk.size < 5:
            continue

        xw, yw = cdf(warm)
        xa, ya = cdf(attk)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(xw, yw, label="warmup (sucessos)")
        ax.plot(xa, ya, label="attack (sucessos)")
        ax.set_title(f"F4 (v1) - CDF Latency (sucessos) | {service} | {attack_id} | {level}")
        ax.set_xlabel("Latency (ms) - Warmup | Attack | Cooldown")
        ax.set_ylabel("CDF")
        ax.legend()
        fig.savefig(figs_dir / f"F4_v1_cdf_success_{service}_{attack_id}_{level}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ------------------------------------------------------------------
    # F4 (v2): censored CDF + failure rate (warmup vs attack)
    # ------------------------------------------------------------------
    for (service, attack_id, level), g in data.groupby(["service", "attack_id", "level"], dropna=False):
        tm = _timeout_marker_ms(g)

        warm_g = g[g["phase"] == "warmup"].copy()
        attk_g = g[g["phase"] == "attack"].copy()
        if len(warm_g) < 5 or len(attk_g) < 5:
            continue

        warm_lat = warm_g["latency_ms"].copy()
        warm_lat.loc[warm_g["ok"] != 1] = tm
        warm_lat = warm_lat.dropna().values

        attk_lat = attk_g["latency_ms"].copy()
        attk_lat.loc[attk_g["ok"] != 1] = tm
        attk_lat = attk_lat.dropna().values

        if warm_lat.size < 5 or attk_lat.size < 5:
            continue

        xw, yw = cdf(warm_lat)
        xa, ya = cdf(attk_lat)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(xw, yw, label="warmup (censurado)")
        ax.plot(xa, ya, label="attack (censurado)")
        ax.set_title(f"F4 (v2) - CDF Latency (censurada) | {service} | {attack_id} | {level}")
        ax.set_xlabel("Latency (ms) - Warmup | Attack | Cooldown")
        ax.set_ylabel("CDF")
        ax.legend()
        fig.savefig(figs_dir / f"F4_v2_cdf_censored_{service}_{attack_id}_{level}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

        warm_fail = float((1 - warm_g["ok"]).mean()) if len(warm_g) else np.nan
        attk_fail = float((1 - attk_g["ok"]).mean()) if len(attk_g) else np.nan

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(["warmup", "attack"], [warm_fail, attk_fail])
        ax.set_title(f"F4 (v2) - Failure rate | {service} | {attack_id} | {level}")
        ax.set_xlabel("Fase")
        ax.set_ylabel("Fail rate")
        fig.savefig(figs_dir / f"F4_v2_failrate_{service}_{attack_id}_{level}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ------------------------------------------------------------------
    # T5/F5: target host resources (CPU / load / memory)
    # ------------------------------------------------------------------
    if resources is not None and len(resources):
        rows_res: List[Dict[str, Any]] = []
        for (service, attack_id, level, phase), g in resources.groupby(["service", "attack_id", "level", "phase"], dropna=False):
            rows_res.append(
                {
                    "service": service,
                    "attack_id": attack_id,
                    "level": level,
                    "phase": phase,
                    "n_samples": int(len(g)),
                    "cpu_mean_pct": float(g["cpu_pct"].mean()) if "cpu_pct" in g else np.nan,
                    "cpu_max_pct": float(g["cpu_pct"].max()) if "cpu_pct" in g else np.nan,
                    "load1_mean": float(g["load1"].mean()) if "load1" in g else np.nan,
                    "load1_max": float(g["load1"].max()) if "load1" in g else np.nan,
                    "mem_mean_pct": float(g["mem_used_pct"].mean()) if "mem_used_pct" in g else np.nan,
                    "mem_max_pct": float(g["mem_used_pct"].max()) if "mem_used_pct" in g else np.nan,
                    "mem_used_mean_mb": float(g["mem_used_mb"].mean()) if "mem_used_mb" in g else np.nan,
                }
            )
        pd.DataFrame(rows_res).sort_values(["service", "attack_id", "level", "phase"]).to_csv(
            tabs_dir / "T5_resource_summary.csv", index=False
        )

        for (service, attack_id, level, run_id), g in resources.groupby(["service", "attack_id", "level", "run_id"], dropna=False):
            g = g.sort_values("t_rel_s").reset_index(drop=True)
            fig, axes = plt.subplots(3, 1, sharex=True, figsize=(11, 8))

            axes[0].plot(g["t_rel_s"], g["cpu_pct"])
            axes[0].set_ylabel("CPU (%)")
            axes[0].set_title(f"F5 - Recursos do host | {service} | {attack_id} | {level} | {run_id}")

            axes[1].plot(g["t_rel_s"], g["load1"], label="load1")
            if "load5" in g.columns:
                axes[1].plot(g["t_rel_s"], g["load5"], label="load5")
            if "load15" in g.columns:
                axes[1].plot(g["t_rel_s"], g["load15"], label="load15")
            axes[1].set_ylabel("Load")
            axes[1].legend()

            axes[2].plot(g["t_rel_s"], g["mem_used_pct"])
            axes[2].set_ylabel("Memory (%)")
            axes[2].set_xlabel("Relative time (s) - Warmup | Attack | Cooldown")

            for ax in axes:
                ax.axvline(v1, linestyle="--")
                ax.axvline(v2, linestyle="--")
                ax.axvline(v3, linestyle="--")

            fig.savefig(figs_dir / f"F5_resources_{service}_{attack_id}_{level}_{run_id}.png", dpi=150, bbox_inches="tight")
            plt.close(fig)
