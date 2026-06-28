import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

CSV_PATH = "T3_summary_censored.csv"
OUT_PATH = "fig_t3_l0_l2_comparison.png"

# Read the CSV
df = pd.read_csv(CSV_PATH)

# Basic normalization
df["level"] = df["level"].astype(str)
df["phase"] = pd.Categorical(
    df["phase"],
    categories=["warmup", "attack", "cooldown"],
    ordered=True
)

# Filter levels of interest
df = df[df["level"].isin(["L0", "L2"])].copy()
df = df.sort_values(["phase", "level"])

# Minimum check
required_cols = ["level", "phase", "success_rate", "lat_p95_ms_censored"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Colunas ausentes no CSV: {missing}")

phases = ["warmup", "attack", "cooldown"]
levels = ["L0", "L2"]
x = np.arange(len(phases))
width = 0.35

# Extract values in the correct order
def vals(metric, level):
    sub = df[df["level"] == level].set_index("phase")
    return [sub.loc[p, metric] if p in sub.index else np.nan for p in phases]

success_l0 = vals("success_rate", "L0")
success_l2 = vals("success_rate", "L2")
p95_l0 = vals("lat_p95_ms_censored", "L0")
p95_l2 = vals("lat_p95_ms_censored", "L2")

fig, axes = plt.subplots(2, 1, figsize=(8, 7), constrained_layout=True)

# Painel 1: success rate
ax1 = axes[0]
ax1.bar(x - width/2, success_l0, width, label="L0")
ax1.bar(x + width/2, success_l2, width, label="L2")
ax1.set_xticks(x)
ax1.set_xticklabels(phases)
ax1.set_ylabel("Success rate (%)")
ax1.set_title("Success rate by phase")
ax1.set_ylim(0, 110)
ax1.legend()
ax1.grid(axis="y", alpha=0.3)

# Painel 2: p95 censurado
ax2 = axes[1]
ax2.bar(x - width/2, p95_l0, width, label="L0")
ax2.bar(x + width/2, p95_l2, width, label="L2")
ax2.set_xticks(x)
ax2.set_xticklabels(phases)
ax2.set_ylabel("p95 censurado (ms)")
ax2.set_title("Latency p95 censurada por fase")
ax2.set_yscale("log")
ax2.legend()
ax2.grid(axis="y", alpha=0.3, which="both")

fig.suptitle("Comparison between L0 and L2 from T3_summary_censored.csv")
plt.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
plt.show()

print(f"Figura salva em: {Path(OUT_PATH).resolve()}")

