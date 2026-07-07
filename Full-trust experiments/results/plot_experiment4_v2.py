"""
Experiment 4 - Layer Placement Stacked Bar Chart (Big Scale)
One plot: 4 scenarios on x-axis, 3 stacked bars per scenario (Greedy, SA, Rollout).
Stacks: Edge / Fog / Cloud percentages.
Data from results_20260626_150558/150659/150801/150902.json (config_big, 100 apps).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

pct = {
    'Cost': {
        'Greedy':  [0.0, 20.5, 79.5],
        'SA':      [0.4, 21.8, 77.9],
        'Rollout': [0.0, 19.3, 80.7],
    },
    'Latency': {
        'Greedy':  [69.1, 26.3, 4.6],
        'SA':      [68.9, 27.9, 3.2],
        'Rollout': [52.3, 40.7, 7.0],
    },
    'Security': {
        'Greedy':  [25.1, 25.4, 49.5],
        'SA':      [26.0, 25.4, 48.6],
        'Rollout': [26.1, 29.8, 44.0],
    },
    'Balanced': {
        'Greedy':  [36.0, 38.8, 25.3],
        'SA':      [38.2, 37.7, 24.0],
        'Rollout': [16.5, 43.2, 40.4],
    },
}

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']
methods = ['Greedy', 'SA', 'Rollout']

fig, ax = plt.subplots(figsize=(14, 7.5))

edge_color = '#7F8C8D'
fog_color = '#27AE60'
cloud_color = '#85C1E9'

bar_width = 0.22
group_gap = 0.05
group_width = 3 * bar_width + 2 * group_gap

x_groups = np.arange(len(scenarios)) * (group_width + 0.6)

for j, method in enumerate(methods):
    x_pos = x_groups + j * (bar_width + group_gap)

    edge_vals = [pct[sc][method][0] for sc in scenarios]
    fog_vals = [pct[sc][method][1] for sc in scenarios]
    cloud_vals = [pct[sc][method][2] for sc in scenarios]

    ax.bar(x_pos, edge_vals, bar_width,
           label='Near-Edge' if j == 0 else '', color=edge_color,
           edgecolor='white', linewidth=0.8, zorder=3)

    ax.bar(x_pos, fog_vals, bar_width, bottom=edge_vals,
           label='Far-Edge' if j == 0 else '', color=fog_color,
           edgecolor='white', linewidth=0.8, zorder=3)

    bottom_cloud = [e + f for e, f in zip(edge_vals, fog_vals)]
    ax.bar(x_pos, cloud_vals, bar_width, bottom=bottom_cloud,
           label='Cloud' if j == 0 else '', color=cloud_color,
           edgecolor='white', linewidth=0.8, zorder=3)

    for i in range(len(scenarios)):
        if edge_vals[i] > 6:
            ax.text(x_pos[i], edge_vals[i] / 2, f'{edge_vals[i]:.0f}%',
                    ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        if fog_vals[i] > 6:
            ax.text(x_pos[i], edge_vals[i] + fog_vals[i] / 2, f'{fog_vals[i]:.0f}%',
                    ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        if cloud_vals[i] > 6:
            ax.text(x_pos[i], bottom_cloud[i] + cloud_vals[i] / 2, f'{cloud_vals[i]:.0f}%',
                    ha='center', va='center', fontsize=9, fontweight='bold', color='white')

for i, sc in enumerate(scenarios):
    for j, method in enumerate(methods):
        x_pos = x_groups[i] + j * (bar_width + group_gap)
        ax.text(x_pos, -5, method, ha='center', va='top', fontsize=11, fontweight='bold', color='#2C3E50')

for i, sc in enumerate(scenarios):
    center = x_groups[i] + bar_width + group_gap
    ax.text(center, -12, sc, ha='center', va='top', fontsize=15, fontweight='bold', color='#1A252F')

ax.set_ylabel('Services Placed (%)', fontsize=15, fontweight='bold')
ax.set_ylim(0, 118)
ax.set_xlim(x_groups[0] - 0.25, x_groups[-1] + 3 * bar_width + 2 * group_gap + 0.05)
ax.tick_params(axis='y', labelsize=12)
ax.set_xticks([])

ax.legend(fontsize=13, loc='upper center', framealpha=0.95, ncol=3,
          bbox_to_anchor=(0.5, 1.0))

ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

plt.subplots_adjust(bottom=0.18)

out_path = os.path.join(OUT_DIR, "experiment4_placement_v2.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
