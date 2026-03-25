"""
Experiment 1 - Optimality Gap Bar Chart
Compares Greedy Best-Fit vs Best Rollout optimality gap relative to ILP.
Data from Tables 2, 4, 5, 6 of experiment_results.md
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Data ---
scenarios = ['Cost', 'Latency', 'Security', 'Balanced']

# Objective scores from tables
ilp_scores    = [1.9336, 3.8543, 2.3054, 3.5030]
greedy_scores = [2.3790, 4.6266, 2.9769, 4.9565]
# Best rollout: Window for Cost/Security/Balanced, App for Latency
best_rollout  = [2.0765, 4.0021, 2.4192, 3.6432]

# Optimality gaps (%)
greedy_gap  = [(g - i) / i * 100 for g, i in zip(greedy_scores, ilp_scores)]
rollout_gap = [(r - i) / i * 100 for r, i in zip(best_rollout, ilp_scores)]

print("Greedy gaps:", [f"{g:.2f}%" for g in greedy_gap])
print("Rollout gaps:", [f"{r:.2f}%" for r in rollout_gap])

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(scenarios))
width = 0.32

bars1 = ax.bar(x - width/2, greedy_gap, width, 
               label='Greedy Best-Fit', color='#3498DB', edgecolor='white', linewidth=0.8, zorder=3)
bars2 = ax.bar(x + width/2, rollout_gap, width,
               label='Rollout', color='#F39C12', edgecolor='white', linewidth=0.8, zorder=3)

# Value labels on bars
for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}%',
            ha='center', va='bottom', fontsize=14, fontweight='bold', color='#2471A3')

for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}%',
            ha='center', va='bottom', fontsize=14, fontweight='bold', color='#D68910')

# Styling
ax.set_xlabel('Optimization Scenario', fontsize=16, fontweight='bold')
ax.set_ylabel('Optimality Gap (%)', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=15)
ax.tick_params(axis='y', labelsize=13)
ax.legend(fontsize=16, loc='upper left', framealpha=0.9)

# Grid
ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax.set_axisbelow(True)

# Y-axis limit with some headroom
ax.set_ylim(0, max(greedy_gap) * 1.15)

# Clean spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

out_path = r"c:\Users\giorg\Desktop\security problem\python transition\Python_version_3\experiment1_optimality_gap.png"
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"\nSaved to: {out_path}")
