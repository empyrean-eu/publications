import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']
methods = ['Isolated', 'Zero-Trust', 'Federated', 'Full-Trust']

# Data for 4 scenarios. Inside each scenario: 4 methods (Iso, T0, T3, T10).
# For each method: [Origin, Trusted, Untrusted]
data_cost = {
    'Origin': [611, 324, 63, 52],
    'Trusted': [0, 0, 467, 582],
    'Untrusted': [0, 310, 104, 0]
}

data_latency = {
    'Origin': [611, 584, 185, 224],
    'Trusted': [0, 0, 444, 410],
    'Untrusted': [0, 50, 5, 0]
}

data_sec = {
    'Origin': [530, 86, 89, 104],
    'Trusted': [0, 0, 329, 506],
    'Untrusted': [0, 521, 192, 0]
}

data_bal = {
    'Origin': [585, 382, 166, 193],
    'Trusted': [0, 0, 346, 441],
    'Untrusted': [0, 252, 122, 0]
}

all_data = [data_cost, data_latency, data_sec, data_bal]

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.patch.set_facecolor('#FFFFFF')
axes = axes.flatten()

colors = ['#D6EAF8', '#21618C', '#C0392B'] # Isolated Blue (Origin), Trust 10 Blue (Trusted), Red (Untrusted)
labels = ['Origin Cluster', 'Trusted Region', 'Untrusted Region']

for i, ax in enumerate(axes):
    scenario_data = all_data[i]
    
    # Extract
    origin = np.array(scenario_data['Origin'])
    trusted = np.array(scenario_data['Trusted'])
    untrusted = np.array(scenario_data['Untrusted'])
    
    # Calculate totals and percentages
    total = origin + trusted + untrusted
    origin_pct = origin / total * 100
    trusted_pct = trusted / total * 100
    untrusted_pct = untrusted / total * 100
    
    ax.set_facecolor('#F8F9F9')
    x = np.arange(len(methods))
    
    ax.bar(x, origin_pct, label=labels[0], color=colors[0], edgecolor='#BDC3C7', linewidth=1, zorder=3)
    ax.bar(x, trusted_pct, bottom=origin_pct, label=labels[1], color=colors[1], edgecolor='white', linewidth=1, zorder=3)
    ax.bar(x, untrusted_pct, bottom=origin_pct + trusted_pct, label=labels[2], color=colors[2], edgecolor='white', linewidth=1, zorder=3)
    
    ax.set_title(f'{scenarios[i]} Optimization', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=14, fontweight='bold')
    
    if i % 2 == 0:
        ax.set_ylabel('Placed Services (%)', fontsize=14, fontweight='bold')
        
    ax.set_ylim(0, 100)
    ax.tick_params(axis='y', labelsize=14)
    
    ax.yaxis.grid(True, linestyle='-', alpha=0.4, color='#95A5A6', zorder=0)
    ax.set_axisbelow(True)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    
    # Add percentage text
    for j in range(len(methods)):
        if origin_pct[j] > 5:
             ax.text(x[j], origin_pct[j]/2, f"{origin_pct[j]:.1f}%", ha='center', va='center', color='black', fontweight='bold', fontsize=12)
        if trusted_pct[j] > 5:
             ax.text(x[j], origin_pct[j] + trusted_pct[j]/2, f"{trusted_pct[j]:.1f}%", ha='center', va='center', color='black', fontweight='bold', fontsize=12)
        if untrusted_pct[j] > 5:
             ax.text(x[j], origin_pct[j] + trusted_pct[j] + untrusted_pct[j]/2, f"{untrusted_pct[j]:.1f}%", ha='center', va='center', color='black', fontweight='bold', fontsize=12)

handles, legend_labels = ax.get_legend_handles_labels()
fig.legend(handles, legend_labels, loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=3, fontsize=16, framealpha=0.9)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "plot_placements.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved placements plot to: {out_path}")
