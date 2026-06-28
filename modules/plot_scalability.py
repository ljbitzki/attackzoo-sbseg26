#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def p95(x):
    return x.quantile(0.95)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="experiments/scalability/tables/scalability_raw.csv")
    ap.add_argument("--out", default="experiments/scalability")
    args = ap.parse_args()

    out = Path(args.out)
    table_dir = out / "tables"
    fig_dir = out / "figs"
    table_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)

    for col in [
        "orchestrator_cpu_pct",
        "orchestrator_rss_mb",
        "host_cpu_pct",
        "host_mem_used_pct",
        "probe_success_rate",
        "startup_time_s",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    summary = (
        df.groupby(["n_targets", "run_id"])
        .agg(
            orchestrator_cpu_mean_pct=("orchestrator_cpu_pct", "mean"),
            orchestrator_cpu_p95_pct=("orchestrator_cpu_pct", p95),
            orchestrator_cpu_max_pct=("orchestrator_cpu_pct", "max"),
            orchestrator_rss_mean_mb=("orchestrator_rss_mb", "mean"),
            orchestrator_rss_max_mb=("orchestrator_rss_mb", "max"),
            host_cpu_mean_pct=("host_cpu_pct", "mean"),
            host_mem_mean_pct=("host_mem_used_pct", "mean"),
            probe_success_rate_mean=("probe_success_rate", "mean"),
            startup_time_s=("startup_time_s", "max"),
        )
        .reset_index()
    )

    agg = (
        summary.groupby("n_targets")
        .agg(
            runs=("run_id", "count"),
            cpu_mean_pct=("orchestrator_cpu_mean_pct", "mean"),
            cpu_std_pct=("orchestrator_cpu_mean_pct", "std"),
            cpu_p95_mean_pct=("orchestrator_cpu_p95_pct", "mean"),
            rss_mean_mb=("orchestrator_rss_mean_mb", "mean"),
            rss_std_mb=("orchestrator_rss_mean_mb", "std"),
            rss_max_mb=("orchestrator_rss_max_mb", "mean"),
            startup_mean_s=("startup_time_s", "mean"),
            startup_std_s=("startup_time_s", "std"),
            probe_success_rate_mean=("probe_success_rate_mean", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(table_dir / "scalability_by_run.csv", index=False)
    agg.to_csv(table_dir / "scalability_summary.csv", index=False)

    fig, ax = plt.subplots()
    ax.errorbar(
        agg["n_targets"],
        agg["cpu_mean_pct"],
        yerr=agg["cpu_std_pct"],
        marker="o",
        capsize=3,
    )
    ax.set_xlabel("Number of simultaneous attacker containers")
    ax.set_ylabel("Orchestrator CPU usage (%)")
    ax.set_title("Orchestration CPU overhead under increasing attacker scale")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.savefig(fig_dir / "F_scalability_cpu.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots()
    ax.errorbar(
        agg["n_targets"],
        agg["rss_mean_mb"],
        yerr=agg["rss_std_mb"],
        marker="o",
        capsize=3,
    )
    ax.set_xlabel("Number of simultaneous attacker containers")
    ax.set_ylabel("Orchestrator memory footprint (MB)")
    ax.set_title("Orchestration memory overhead under increasing attacker scale")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.savefig(fig_dir / "F_scalability_memory.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(table_dir / "scalability_summary.csv")
    print(fig_dir / "F_scalability_cpu.png")
    print(fig_dir / "F_scalability_memory.png")


if __name__ == "__main__":
    main()
