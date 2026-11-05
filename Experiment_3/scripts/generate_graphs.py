"""
Experiment 3 - Analyze Synchronization Mechanisms in Parallel Programs
Performance Analysis & Visualization Generator

Reads  : ../results/benchmark_results.csv
Writes : ../graphs/*.png

Usage  : python scripts/generate_graphs.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "graphs")
os.makedirs(OUT, exist_ok=True)

# Styling configuration
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.35,
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# Load Data
df = pd.read_csv(os.path.join(RES, "benchmark_results.csv"), keep_default_na=False)

colors = {
    "None": "#EF4444",      # Red
    "Critical": "#F59E0B",  # Amber
    "Atomic": "#10B981",    # Emerald
    "Lock": "#6366F1",      # Indigo
}

markers = {
    "None": "o",
    "Critical": "s",
    "Atomic": "^",
    "Lock": "D",
}

# ------------------------------------------------------------------------------
# Graph 1: Execution Time vs Thread Count (Line Chart)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
for mech in ["None", "Atomic", "Lock", "Critical"]:
    subset = df[df["Mechanism"] == mech]
    ax.plot(
        subset["Threads"],
        subset["Execution_Time_s"],
        label=f"{mech} ({subset['Correctness'].iloc[-1]})",
        color=colors[mech],
        marker=markers[mech],
        linewidth=2.5,
        markersize=8,
    )
    for _, row in subset.iterrows():
        ax.annotate(
            f"{row['Execution_Time_s']:.4f}s",
            (row["Threads"], row["Execution_Time_s"]),
            textcoords="offset points",
            xytext=(0, 9),
            ha="center",
            fontsize=8.5,
            fontweight="bold",
            color=colors[mech],
        )

ax.set_title("Execution Time vs Number of Threads (10,000,000 Incs)")
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Execution Time (seconds)")
ax.set_xticks([1, 2, 4, 8])
ax.legend(title="Synchronization Mechanism", frameon=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "01_execution_time_comparison.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 2: Bar Comparison across Thread Configurations
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
threads = [1, 2, 4, 8]
x = np.arange(len(threads))
width = 0.20

for idx, mech in enumerate(["None", "Atomic", "Lock", "Critical"]):
    times = [df[(df["Mechanism"] == mech) & (df["Threads"] == t)]["Execution_Time_s"].values[0] for t in threads]
    offset = (idx - 1.5) * width
    bars = ax.bar(x + offset, times, width, label=mech, color=colors[mech], alpha=0.9, edgecolor="black", linewidth=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.3f}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, rotation=45)

ax.set_title("Performance Comparison by Thread Count")
ax.set_xlabel("Thread Count")
ax.set_ylabel("Execution Time (seconds)")
ax.set_xticks(x)
ax.set_xticklabels([f"{t} Threads" for t in threads])
ax.legend(title="Mechanism", frameon=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "02_execution_time_grouped_bar.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 3: Race Condition Update Loss (Correctness Analysis)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
none_df = df[df["Mechanism"] == "None"]
expected = 10000000

bars = ax.bar(
    [f"{t} Threads" for t in none_df["Threads"]],
    none_df["Final_Count"] / 1e6,
    color="#EF4444",
    alpha=0.85,
    edgecolor="black",
    width=0.45,
    label="Actual Recorded Count",
)
ax.axhline(expected / 1e6, color="#10B981", linestyle="--", linewidth=2, label="Expected Count (10.0M)")

for bar in bars:
    yval = bar.get_height()
    loss_pct = (1 - (yval * 1e6 / expected)) * 100
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval / 2,
        f"{yval:.2f}M\n(-{loss_pct:.1f}% loss)" if loss_pct > 0 else f"{yval:.2f}M\n(100% correct)",
        ha="center",
        va="center",
        color="white" if loss_pct > 0 else "black",
        fontweight="bold",
        fontsize=10,
    )

ax.set_title("Race Condition: Lost Updates as Thread Contention Increases")
ax.set_xlabel("Thread Configuration")
ax.set_ylabel("Final Counter Value (Millions)")
ax.set_ylim(0, 12)
ax.legend(frameon=True, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03_race_condition_lost_updates.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 4: Scalability / Overhead Factor Relative to 1 Thread
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
for mech in ["Atomic", "Critical", "Lock"]:
    subset = df[df["Mechanism"] == mech]
    t1 = subset[subset["Threads"] == 1]["Execution_Time_s"].values[0]
    slowdown = subset["Execution_Time_s"] / t1
    ax.plot(
        subset["Threads"],
        slowdown,
        label=f"{mech} (T_p / T_1)",
        color=colors[mech],
        marker=markers[mech],
        linewidth=2.5,
        markersize=8,
    )
    for thr, sl in zip(subset["Threads"], slowdown):
        ax.annotate(
            f"{sl:.2f}x",
            (thr, sl),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            fontweight="bold",
            color=colors[mech],
        )

ax.axhline(1.0, color="#6B7280", linestyle=":", linewidth=1.5, label="Ideal Scalability (1.0x)")
ax.set_title("Lock Contention Overhead Factor vs 1 Thread")
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Execution Time Relative to 1 Thread (Slowdown Factor)")
ax.set_xticks([1, 2, 4, 8])
ax.legend(frameon=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "04_scalability_slowdown_factor.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 5: Executive Dashboard (2x2 Multi-Panel)
# ------------------------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Subplot (0,0): Time vs Threads
for mech in ["None", "Atomic", "Lock", "Critical"]:
    sub = df[df["Mechanism"] == mech]
    axs[0, 0].plot(sub["Threads"], sub["Execution_Time_s"], marker=markers[mech], color=colors[mech], label=mech, linewidth=2)
axs[0, 0].set_title("A. Absolute Execution Time", fontweight="bold")
axs[0, 0].set_xlabel("Threads")
axs[0, 0].set_ylabel("Time (s)")
axs[0, 0].set_xticks([1, 2, 4, 8])
axs[0, 0].legend(frameon=True, fontsize=9)

# Subplot (0,1): Atomic vs Critical & Lock
for mech in ["Atomic", "Lock", "Critical"]:
    sub = df[df["Mechanism"] == mech]
    axs[0, 1].plot(sub["Threads"], sub["Execution_Time_s"], marker=markers[mech], color=colors[mech], label=mech, linewidth=2)
axs[0, 1].set_title("B. Synchronized Mechanisms Contention", fontweight="bold")
axs[0, 1].set_xlabel("Threads")
axs[0, 1].set_ylabel("Time (s)")
axs[0, 1].set_xticks([1, 2, 4, 8])
axs[0, 1].legend(frameon=True, fontsize=9)

# Subplot (1,0): Final Count vs Expected
none_sub = df[df["Mechanism"] == "None"]
atomic_sub = df[df["Mechanism"] == "Atomic"]
axs[1, 0].plot(none_sub["Threads"], none_sub["Final_Count"] / 1e6, 'o-', color=colors["None"], label="None (Race)", linewidth=2)
axs[1, 0].plot(atomic_sub["Threads"], atomic_sub["Final_Count"] / 1e6, '^-', color=colors["Atomic"], label="Atomic / Sync", linewidth=2)
axs[1, 0].axhline(10.0, color="gray", linestyle="--", alpha=0.7, label="Expected (10M)")
axs[1, 0].set_title("C. Correctness: Count vs Expected", fontweight="bold")
axs[1, 0].set_xlabel("Threads")
axs[1, 0].set_ylabel("Final Count (Millions)")
axs[1, 0].set_xticks([1, 2, 4, 8])
axs[1, 0].set_ylim(0, 12)
axs[1, 0].legend(frameon=True, fontsize=9)

# Subplot (1,1): Summary Table / Scorecard
axs[1, 1].axis('off')
table_data = [
    ["Mechanism", "Correctness", "1 Thread (s)", "8 Threads (s)", "Scalability"],
    ["None", "INCORRECT", "0.0130 s", "0.0306 s", "Flawed (Race)"],
    ["Atomic", "Correct", "0.1512 s", "0.2273 s", "Excellent (~1.5x)"],
    ["Lock", "Correct", "0.2334 s", "2.2623 s", "Poor (~9.7x slower)"],
    ["Critical", "Correct", "0.2849 s", "2.2584 s", "Poor (~7.9x slower)"],
]
table = axs[1, 1].table(
    cellText=table_data,
    loc='center',
    cellLoc='center',
    colWidths=[0.20, 0.22, 0.20, 0.20, 0.24]
)
table.auto_set_font_size(False)
table.set_fontsize(9.5)
table.scale(1.05, 1.8)
for i in range(5):
    table[(0, i)].set_facecolor("#374151")
    table[(0, i)].set_text_props(color="white", weight="bold")
for row_idx in range(1, 5):
    bg = "#F3F4F6" if row_idx % 2 == 1 else "#FFFFFF"
    for col_idx in range(5):
        table[(row_idx, col_idx)].set_facecolor(bg)

axs[1, 1].set_title("D. Synchronization Benchmark Scorecard", fontweight="bold", pad=20)

fig.suptitle("Experiment 3: Synchronization Mechanisms Comprehensive Dashboard", fontsize=16, fontweight="bold", y=0.98)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig(os.path.join(OUT, "05_synchronization_dashboard.png"))
plt.close(fig)

print("Successfully generated all 5 graphs in", OUT)
