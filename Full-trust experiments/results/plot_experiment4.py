"""
Experiment 4 - Layer Placement Stacked Bar Chart (Big Scale)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Data: [Edge, Fog, Cloud] raw counts, total = 373 ---
total = 373

data = {
    'Cost': {
        'Greedy':  [3, 144, 226],
        'Rollout': [0, 112, 261],
    },
    'Latency': {
        'Greedy':  [264, 109, 0],
        'Rollout': [202, 152, 19],
    },
    'Security': {
        'Greedy':  [144, 99, 130],
        'Rollout': [118, 109, 146],
    },
    'Balanced': {
        'Greedy':  [163, 135, 75],
        'Rollout': [65, 134, 174],
    },
}

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']
methods = ['Greedy', 'Rollout']

# Convert to percentages
pct = {}
for sc in scenarios:
    pct[sc] = {}
    for m in methods:
        vals = data[sc][m]
        pct[sc][m] = [v / total * 100 for v in vals]

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 6.5))

# Colors for layers
edge_color  = '#7F8C8D'  # gray (near-edge)
fog_color   = '#27AE60'  # green (far-edge)
cloud_color = '#85C1E9'  # light blue (cloud)

bar_width = 0.30
group_gap = 0.08
group_width = 2 * bar_width + group_gap

x_groups = np.arange(len(scenarios)) * (group_width + 0.5)

for j, method in enumerate(methods):
    x_pos = x_groups + j * (bar_width + group_gap)
    
    edge_vals  = [pct[sc][method][0] for sc in scenarios]
    fog_vals   = [pct[sc][method][1] for sc in scenarios]
    cloud_vals = [pct[sc][method][2] for sc in scenarios]
    
    # Stack: Edge at bottom, Fog in middle, Cloud on top
    b1 = ax.bar(x_pos, edge_vals, bar_width,
                label='Near-Edge' if j == 0 else '', color=edge_color,
                edgecolor='white', linewidth=0.8, zorder=3)
    
    b2 = ax.bar(x_pos, fog_vals, bar_width, bottom=edge_vals,
                label='Far-Edge' if j == 0 else '', color=fog_color,
                edgecolor='white', linewidth=0.8, zorder=3)
    
    bottom_cloud = [e + f for e, f in zip(edge_vals, fog_vals)]
    b3 = ax.bar(x_pos, cloud_vals, bar_width, bottom=bottom_cloud,
                label='Cloud' if j == 0 else '', color=cloud_color,
                edgecolor='white', linewidth=0.8, zorder=3)
    
    # Add percentage labels inside segments (only if > 8%)
    for i in range(len(scenarios)):
        # Edge
        if edge_vals[i] > 8:
            ax.text(x_pos[i], edge_vals[i] / 2, f'{edge_vals[i]:.0f}%',
                    ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        # Fog
        if fog_vals[i] > 8:
            ax.text(x_pos[i], edge_vals[i] + fog_vals[i] / 2, f'{fog_vals[i]:.0f}%',
                    ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        # Cloud
        if cloud_vals[i] > 8:
            ax.text(x_pos[i], bottom_cloud[i] + cloud_vals[i] / 2, f'{cloud_vals[i]:.0f}%',
                    ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# Method labels under each bar
for i, sc in enumerate(scenarios):
    for j, method in enumerate(methods):
        x_pos = x_groups[i] + j * (bar_width + group_gap)
        ax.text(x_pos, -5, method, ha='center', va='top', fontsize=12, fontweight='bold')

# Scenario labels
for i, sc in enumerate(scenarios):
    center = x_groups[i] + (bar_width + group_gap) / 2
    ax.text(center, -12, sc, ha='center', va='top', fontsize=16, fontweight='bold')

# Styling
ax.set_ylabel('Services Placed (%)', fontsize=16, fontweight='bold')
ax.set_ylim(0, 118)
ax.set_xlim(x_groups[0] - 0.35, x_groups[-1] + 2 * (bar_width + group_gap) + 0.15)
ax.tick_params(axis='y', labelsize=13)
ax.set_xticks([])

# Legend
ax.legend(fontsize=14, loc='upper center', framealpha=0.9, ncol=3,
          bbox_to_anchor=(0.5, 1.0))

# Grid
ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax.set_axisbelow(True)

# Clean spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

plt.subplots_adjust(bottom=0.18)

out_path = r"c:\Users\giorg\Desktop\security problem\python transition\Python_version_3\experiment4_placement.png"
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
