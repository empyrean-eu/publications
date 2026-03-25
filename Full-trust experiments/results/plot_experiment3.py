"""
Experiment 3 - Normalized Metrics Comparison (Big Scale)
4 subplots, one per optimization scenario.
Each subplot: 2 groups (Greedy, Rollout) x 3 bars (Cost, Latency, Security).
Data from Tables 1, 3, 4, 5 of experiment_results_big.md
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Data: [Norm Cost, Norm Latency, Norm Security] ---
# Best Rollout: App for Latency/Mixed, Window for Cost/Security

data = {
    'Latency': {
        'weights': 'W₁=0.05, W₂=0.05, W₃=0.90',
        'Greedy':  [22.5050, 12.8685, 27.1078],
        'Rollout': [18.6009, 10.9654, 31.5970],
    },
    'Cost': {
        'weights': 'W₁=0.80, W₂=0.10, W₃=0.10',
        'Greedy':  [5.1035, 28.4213, 30.9159],
        'Rollout': [3.9489, 25.8073, 35.8616],
    },
    'Security': {
        'weights': 'W₁=0.10, W₂=0.80, W₃=0.10',
        'Greedy':  [10.6983, 32.8711, 50.1618],
        'Rollout': [12.6044, 29.1517, 54.4093],
    },
    'Balanced': {
        'weights': 'W₁=0.30, W₂=0.30, W₃=0.40',
        'Greedy':  [16.2231, 21.4112, 35.4274],
        'Rollout': [11.1750, 17.4305, 41.106],
    },
}

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']
metrics = [' Cost', 'Latency', ' Security']

# Colors
greedy_color = '#3498DB'
rollout_color = '#F39C12'

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, sc in enumerate(scenarios):
    ax = axes[idx]
    d = data[sc]
    
    x = np.arange(len(metrics))
    width = 0.32
    
    bars1 = ax.bar(x - width/2, d['Greedy'], width,
                   label='Greedy Best-Fit', color=greedy_color, edgecolor='white', linewidth=0.5, zorder=3)
    bars2 = ax.bar(x + width/2, d['Rollout'], width,
                   label='Rollout', color=rollout_color, edgecolor='white', linewidth=0.5, zorder=3)
    
    # Value labels
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.3, f'{h:.1f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2471A3')
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.3, f'{h:.1f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='#D68910')
    
    ax.set_title(f'{sc} Optimization', fontsize=16, fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=13)
    ax.tick_params(axis='y', labelsize=12)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Set y limit with headroom
    max_val = max(max(d['Greedy']), max(d['Rollout']))
    ax.set_ylim(0, max_val * 1.18)
    
    if idx == 0:
        ax.legend(fontsize=15, loc='upper left', framealpha=0.9)

fig.text(0.02, 0.5, 'Normalized Value', va='center', rotation='vertical', fontsize=16, fontweight='bold')

plt.tight_layout(rect=[0.04, 0, 1, 1])

out_path = r"c:\Users\giorg\Desktop\security problem\python transition\Python_version_3\experiment3_normalized_metrics.png"
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
