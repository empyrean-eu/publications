"""
Experiment 3 - Normalized Metrics Comparison (Big Scale)
4 subplots, one per optimization scenario.
Each subplot: 3 groups (Greedy, SA, Rollout) x 3 bars (Cost, Latency, Security).
Data from results_20260626_150558/150659/150801/150902.json (config_big, 100 apps).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

data = {
    'Cost': {
        'Greedy': [8.5139, 52.3099, 52.2285],
        'SA': [8.6185, 50.9100, 55.5084],
        'Rollout': [7.9003, 45.7212, 58.8001],
    },
    'Latency': {
        'Greedy': [35.3403, 23.1801, 43.0120],
        'SA': [35.8366, 20.3269, 45.1320],
        'Rollout': [35.3227, 16.8431, 52.4185],
    },
    'Security': {
        'Greedy': [24.9712, 53.2379, 84.9191],
        'SA': [25.0461, 52.0706, 86.6335],
        'Rollout': [25.8463, 38.5173, 86.9597],
    },
    'Balanced': {
        'Greedy': [28.9028, 31.5045, 62.3235],
        'SA': [28.6637, 27.9229, 66.7455],
        'Rollout': [21.9581, 27.0535, 72.3813],
    },
}

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']
metrics = ['Cost', 'Latency', 'Security']

greedy_color = '#3498DB'
sa_color = '#A9CCE3'
rollout_color = '#F39C12'

fig, axes = plt.subplots(2, 2, figsize=(15, 11))
axes = axes.flatten()

for idx, sc in enumerate(scenarios):
    ax = axes[idx]
    d = data[sc]

    x = np.arange(len(metrics))
    width = 0.25

    bars1 = ax.bar(x - width, d['Greedy'], width,
                   label='Greedy Best-Fit', color=greedy_color, edgecolor='white', linewidth=0.5, zorder=3)
    bars2 = ax.bar(x, d['SA'], width,
                   label='Simulated Annealing', color=sa_color, edgecolor='white', linewidth=0.5, zorder=3)
    bars3 = ax.bar(x + width, d['Rollout'], width,
                   label='Rollout', color=rollout_color, edgecolor='white', linewidth=0.5, zorder=3)

    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1A5276')
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2471A3')
    for bar in bars3:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f'{h:.1f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#7E5109')

    ax.set_title(f'{sc} Optimization', fontsize=14, fontweight='bold', pad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=12, fontweight='bold')
    ax.tick_params(axis='y', labelsize=11)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    max_val = max(max(d['Greedy']), max(d['SA']), max(d['Rollout']))
    ax.set_ylim(0, max_val * 1.15)

    if idx == 0:
        ax.legend(fontsize=11, loc='upper left', framealpha=0.95)

fig.text(0.01, 0.5, 'Normalized Objective Term Value', va='center', rotation='vertical', fontsize=15, fontweight='bold')

plt.tight_layout(rect=[0.03, 0, 1, 1])

out_path = os.path.join(OUT_DIR, "experiment3_normalized_metrics_v2.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
