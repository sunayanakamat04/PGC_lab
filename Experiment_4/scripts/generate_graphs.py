"""
Experiment 4 - Analyze Cache Coherence (MSI, MESI, MOESI) and NUMA Performance
Visualization & Analysis Graph Generator
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

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.35,
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# ------------------------------------------------------------------------------
# Graph 1: Simulation Bus Traffic (MSI vs MESI vs MOESI)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5))
protos = ["MSI", "MESI", "MOESI"]
bus_tx_adj = [4000, 3999, 3999]
bus_tx_pad = [4, 2, 2]

x = np.arange(len(protos))
width = 0.35

bars1 = ax.bar(x - width/2, bus_tx_adj, width, label="Adjacent (False Sharing)", color="#EF4444", edgecolor="black", alpha=0.9)
bars2 = ax.bar(x + width/2, bus_tx_pad, width, label="Padded (Private Lines)", color="#10B981", edgecolor="black", alpha=0.9)

for bar in bars1:
    h = bar.get_height()
    ax.annotate(f"{int(h)}", xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9)

for bar in bars2:
    h = bar.get_height()
    ax.annotate(f"{int(h)}", xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9)

ax.set_title("Coherence Protocol Bus Transactions (1000 Iterations / 4000 Ops)")
ax.set_xlabel("Coherence Protocol")
ax.set_ylabel("Total Bus Transactions (BusRd + RdX + Upgr)")
ax.set_xticks(x)
ax.set_xticklabels(protos)
ax.set_yscale('log')
ax.set_ylim(1, 10000)
ax.legend(frameon=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "01_coherence_bus_transactions.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 2: False Sharing Hardware Execution Time (Adjacent vs Padded)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.2))
threads = [1, 2, 4]
adj_times = [0.0387, 0.0219, 0.0185]
pad_times = [0.0354, 0.0184, 0.0175]

ax.plot(threads, adj_times, 'o-', color='#EF4444', linewidth=2.5, markersize=8, label="Adjacent (False Sharing)")
ax.plot(threads, pad_times, 's-', color='#10B981', linewidth=2.5, markersize=8, label="Padded (No False Sharing)")

for t, a, p in zip(threads, adj_times, pad_times):
    ax.annotate(f"{a:.4f}s", (t, a), textcoords="offset points", xytext=(0, 8), ha='center', color='#EF4444', fontweight='bold')
    ax.annotate(f"{p:.4f}s", (t, p), textcoords="offset points", xytext=(0, -14), ha='center', color='#10B981', fontweight='bold')

ax.set_title("Hardware Execution Time vs Thread Count (100M Incs)")
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Execution Time (seconds)")
ax.set_xticks(threads)
ax.legend(frameon=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "02_false_sharing_execution_time.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 3: Physical Core Pinning (Taskset Effect)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5))
labels = ["Default Scheduler\n(2 Threads)", "Pinned Cores 0, 2\n(Physical Cores)"]
t_adj = [0.0219, 0.0266]
t_pad = [0.0184, 0.0191]

x = np.arange(len(labels))
width = 0.35
b1 = ax.bar(x - width/2, t_adj, width, label="Adjacent (Shared Line)", color="#EF4444", edgecolor="black")
b2 = ax.bar(x + width/2, t_pad, width, label="Padded (Distinct Lines)", color="#10B981", edgecolor="black")

for bar in b1:
    h = bar.get_height()
    ax.annotate(f"{h:.4f}s", (bar.get_x() + bar.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha='center', va='bottom', fontsize=9, fontweight='bold')

for bar in b2:
    h = bar.get_height()
    ax.annotate(f"{h:.4f}s", (bar.get_x() + bar.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha='center', va='bottom', fontsize=9, fontweight='bold')

overhead_pct = ((t_adj[1] - t_pad[1]) / t_pad[1]) * 100
ax.annotate(f"+{overhead_pct:.1f}% Cache Contention\nOverhead", xy=(1 - width/2, t_adj[1]), xytext=(0.7, 0.031),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5), fontsize=9.5, fontweight='bold', color="#DC2626")

ax.set_title("Cache Line Bouncing across Physical Cores (L1/L2 Invalidation)")
ax.set_ylabel("Execution Time (seconds)")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(0, 0.035)
ax.legend(frameon=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03_physical_core_pinning_overhead.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 4: Memory Sweep Execution Time (512 MB Buffer, 4 Passes)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
threads = ["1 Thread", "2 Threads"]
t_default = [0.1313, 0.0806]
t_numa = [0.1866, 0.0847]

x = np.arange(len(threads))
width = 0.35
b1 = ax.bar(x - width/2, t_default, width, label="Default Linux Allocation", color="#3B82F6", edgecolor="black")
b2 = ax.bar(x + width/2, t_numa, width, label="numactl Node 0 Bound", color="#8B5CF6", edgecolor="black")

for bar in b1:
    h = bar.get_height()
    ax.annotate(f"{h:.4f}s", (bar.get_x() + bar.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha='center', va='bottom', fontsize=9, fontweight='bold')

for bar in b2:
    h = bar.get_height()
    ax.annotate(f"{h:.4f}s", (bar.get_x() + bar.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_title("Memory Sweep Execution Time (512 MB Buffer, 4 Passes)")
ax.set_ylabel("Execution Time (seconds)")
ax.set_xticks(x)
ax.set_xticklabels(threads)
ax.legend(frameon=True)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "04_memory_sweep_latency.png"))
plt.close(fig)

# ------------------------------------------------------------------------------
# Graph 5: Executive Dashboard (2x2 Multi-Panel)
# ------------------------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Subplot (0,0): Bus Transactions
axs[0, 0].bar(x - width/2, bus_tx_adj[:2], width, label="Adjacent", color="#EF4444", edgecolor="black")
axs[0, 0].bar(x + width/2, bus_tx_pad[:2], width, label="Padded", color="#10B981", edgecolor="black")
axs[0, 0].set_title("A. Simulated Bus Transactions (Log Scale)", fontweight="bold")
axs[0, 0].set_xticks(x)
axs[0, 0].set_xticklabels(["MSI", "MESI"])
axs[0, 0].set_yscale('log')
axs[0, 0].set_ylabel("Transactions")
axs[0, 0].legend(frameon=True, fontsize=9)

# Subplot (0,1): Memory Writebacks vs Cache-to-Cache Transfers
ops = ["Writeback (Memory)", "Cache-to-Cache (C2C)"]
mesi_vals = [1999, 0]
moesi_vals = [0, 1999]
x_ops = np.arange(len(ops))
axs[0, 1].bar(x_ops - width/2, mesi_vals, width, label="MESI (Writeback to RAM)", color="#F59E0B", edgecolor="black")
axs[0, 1].bar(x_ops + width/2, moesi_vals, width, label="MOESI (Direct C2C)", color="#10B981", edgecolor="black")
axs[0, 1].set_title("B. MOESI Owned State Advantage on Shared Line", fontweight="bold")
axs[0, 1].set_xticks(x_ops)
axs[0, 1].set_xticklabels(ops)
axs[0, 1].set_ylabel("Total Operations (1000 Iters)")
axs[0, 1].legend(frameon=True, fontsize=9)

# Subplot (1,0): False Sharing Hardware Time
axs[1, 0].plot([1, 2, 4], adj_times, 'o-', color='#EF4444', label="Adjacent (False Sharing)", linewidth=2)
axs[1, 0].plot([1, 2, 4], pad_times, 's-', color='#10B981', label="Padded (Aligned)", linewidth=2)
axs[1, 0].set_title("C. Multi-Core Execution Time (Hardware)", fontweight="bold")
axs[1, 0].set_xlabel("Threads")
axs[1, 0].set_ylabel("Time (s)")
axs[1, 0].set_xticks([1, 2, 4])
axs[1, 0].legend(frameon=True, fontsize=9)

# Subplot (1,1): Summary Scorecard Table
axs[1, 1].axis('off')
table_data = [
    ["Mechanism / Case", "Correctness", "Relative Performance", "Scalability"],
    ["MSI (Simulated)", "Correct", "High Bus Traffic (4000 tx)", "Poor on Shared Lines"],
    ["MESI (Simulated)", "Correct", "Silent E->M (Private Lines)", "Good for Private Data"],
    ["MOESI (Simulated)", "Correct", "1999 C2C Transfers (0 WB)", "Best Memory Traffic"],
    ["Adjacent (Hardware)", "Correct", "Cache Line Bouncing (+40%)", "Degraded Scalability"],
    ["Padded (Hardware)", "Correct", "Fastest (~0.017s @ 4T)", "Optimal Scaling"],
]
table = axs[1, 1].table(
    cellText=table_data,
    loc='center',
    cellLoc='center',
    colWidths=[0.28, 0.18, 0.30, 0.24]
)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.05, 1.7)
for i in range(4):
    table[(0, i)].set_facecolor("#374151")
    table[(0, i)].set_text_props(color="white", weight="bold")
for r in range(1, 6):
    bg = "#F3F4F6" if r % 2 == 1 else "#FFFFFF"
    for c in range(4):
        table[(r, c)].set_facecolor(bg)

axs[1, 1].set_title("D. Coherence & NUMA Evaluation Scorecard", fontweight="bold", pad=20)

fig.suptitle("Experiment 4: Cache Coherence & NUMA Access Comprehensive Dashboard", fontsize=15, fontweight="bold", y=0.98)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig(os.path.join(OUT, "05_cache_coherence_dashboard.png"))
plt.close(fig)

print("Generated all 5 graphs in", OUT)
