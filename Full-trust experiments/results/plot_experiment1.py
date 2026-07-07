"""
Experiment 1 - Optimality Gap Bar Chart
Compares Greedy Best-Fit, Simulated Annealing (SA), and Best Rollout optimality gaps relative to ILP.
Data from small_scale3.md (run 2026-06-21- 2026-06-23).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Data ---
scenarios = ['Cost', 'Latency', 'Security', 'Balanced']

greedy_gap  = [20.37, 30.65, 27.54, 33.02]
sa_gap      = [9.20, 13.35, 4.96, 9.82]
rollout_gap = [6.61, 3.55, 2.11, 4.57]

fig, ax = plt.subplots(figsize=(11, 6.5))

x = np.arange(len(scenarios))
width = 0.25

bars1 = ax.bar(x - width, greedy_gap, width,
               label='Greedy Best-Fit', color='#3498DB', edgecolor='white', linewidth=0.8, zorder=3)
bars2 = ax.bar(x, sa_gap, width,
               label='Simulated Annealing', color='#A9CCE3', edgecolor='white', linewidth=0.8, zorder=3)
bars3 = ax.bar(x + width, rollout_gap, width,
               label='Rollout', color='#F39C12', edgecolor='white', linewidth=0.8, zorder=3)

for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}%',
            ha='center', va='bottom', fontsize=13, fontweight='bold', color='#1A5276')

for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}%',
            ha='center', va='bottom', fontsize=13, fontweight='bold', color='#2471A3')

for bar in bars3:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}%',
            ha='center', va='bottom', fontsize=13, fontweight='bold', color='#7E5109')

ax.set_xlabel('Optimization Scenario', fontsize=15, fontweight='bold')
ax.set_ylabel('Optimality Gap (%)', fontsize=15, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=14, fontweight='bold')
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=15, loc='upper left', bbox_to_anchor=(-0.02, 1.0), framealpha=0.95)

ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax.set_axisbelow(True)
ax.set_ylim(0, max(greedy_gap) * 1.15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

out_path = os.path.join(OUT_DIR, "experiment1_optimality_gap3.png")
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Saved to: {out_path}")
