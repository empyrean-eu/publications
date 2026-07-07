import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# Hardcoded from results_jsons5.md — Rollout trust placement (%)
scenarios = ['Cost', 'Latency', 'Security', 'Balanced']
methods = ['Isolated', 'Zero-Trust', 'Fed-2', 'Fed-4', 'Fed-6', 'Full-Trust']

data_cost = {
    'Origin':    [100.0, 55.9, 29.2, 11.2, 10.0, 12.7],
    'Trusted':   [0.0,   0.0,  47.7, 69.8, 73.6, 87.3],
    'Untrusted': [0.0,  44.1,  23.1, 18.9,  16.4,  0.0],
}

data_latency = {
    'Origin':    [100.0, 91.9, 43.3, 31.1, 32.9, 32.8],
    'Trusted':   [0.0,   0.0,  54.7, 66.9, 66.2, 67.2],
    'Untrusted': [0.0,   8.1,   2.0,  2.0,  0.9,  0.0],
}

data_sec = {
    'Origin':    [100.0, 16.4, 18.6, 20.3, 20.6, 20.2],
    'Trusted':   [0.0,   0.0,  26.4, 42.3, 45.3, 79.8],
    'Untrusted': [0.0,  83.6,  55.0, 37.5, 34.1,  0.0],
}

data_bal = {
    'Origin':    [100.0, 40.5, 29.5, 30.6, 30.6, 35.3],
    'Trusted':   [0.0,   0.0,  30.6, 45.8, 44.4, 64.7],
    'Untrusted': [0.0,  59.5,  40.0, 24.6, 25.0,  0.0],
}

all_data = [data_cost, data_latency, data_sec, data_bal]

SEGMENT_COLORS = ['#D6EAF8', '#21618C', '#C0392B']
SEGMENT_LABELS = ['Origin Cluster', 'Trusted Region', 'Untrusted Region']
TEXT_COLORS = ['#1A1A1A', '#FFFFFF', '#FFFFFF']
MIN_INSIDE_PCT = 11.0
LABEL_FONTSIZE = 14
SMALL_LABEL_FONTSIZE = 11


def annotate_segment(ax, xpos, bottom, height, text, text_color):
    """Place percentage inside the bar when tall enough, else just above the segment."""
    if height <= 0:
        return
    label = f"{text:.1f}%"
    mid_y = bottom + height / 2
    if height >= MIN_INSIDE_PCT:
        ax.text(
            xpos, mid_y, label,
            ha='center', va='center', color=text_color,
            fontweight='bold', fontsize=LABEL_FONTSIZE, zorder=5,
        )
    elif height >= 1.0:
        ax.text(
            xpos, bottom + height + 1.2, label,
            ha='center', va='bottom', color='#922B21' if text_color == '#FFFFFF' else '#1A1A1A',
            fontweight='bold', fontsize=SMALL_LABEL_FONTSIZE, zorder=5,
        )


fig, axes = plt.subplots(2, 2, figsize=(20, 11))
fig.patch.set_facecolor('#FFFFFF')
axes = axes.flatten()

bar_width = 0.72

for i, ax in enumerate(axes):
    scenario_data = all_data[i]
    origin_pct = np.array(scenario_data['Origin'])
    trusted_pct = np.array(scenario_data['Trusted'])
    untrusted_pct = np.array(scenario_data['Untrusted'])

    ax.set_facecolor('#F8F9F9')
    x = np.arange(len(methods))

    ax.bar(
        x, origin_pct, bar_width, label=SEGMENT_LABELS[0],
        color=SEGMENT_COLORS[0], edgecolor='#BDC3C7', linewidth=1.2, zorder=3,
    )
    ax.bar(
        x, trusted_pct, bar_width, bottom=origin_pct, label=SEGMENT_LABELS[1],
        color=SEGMENT_COLORS[1], edgecolor='white', linewidth=1.2, zorder=3,
    )
    ax.bar(
        x, untrusted_pct, bar_width, bottom=origin_pct + trusted_pct,
        label=SEGMENT_LABELS[2], color=SEGMENT_COLORS[2], edgecolor='white', linewidth=1.2, zorder=3,
    )

    ax.set_title(f'{scenarios[i]} Optimization', fontsize=18, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=14, fontweight='bold', rotation=0, ha='center')

    if i % 2 == 0:
        ax.set_ylabel('Placed Services (%)', fontsize=16, fontweight='bold')

    ax.set_ylim(0, 108)
    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', pad=8)

    ax.yaxis.grid(True, linestyle='-', alpha=0.4, color='#95A5A6', zorder=0)
    ax.set_axisbelow(True)

    for spine in ('top', 'right'):
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')

    for j in range(len(methods)):
        annotate_segment(ax, x[j], 0, origin_pct[j], origin_pct[j], TEXT_COLORS[0])
        annotate_segment(
            ax, x[j], origin_pct[j], trusted_pct[j], trusted_pct[j], TEXT_COLORS[1],
        )
        annotate_segment(
            ax, x[j], origin_pct[j] + trusted_pct[j], untrusted_pct[j],
            untrusted_pct[j], TEXT_COLORS[2],
        )

handles, legend_labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles, legend_labels,
    loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3,
    fontsize=20, framealpha=0.95, edgecolor='#BDC3C7',
    handlelength=2.2, handleheight=1.4, labelspacing=0.6,
)

fig.subplots_adjust(left=0.07, right=0.98, top=0.90, bottom=0.10, hspace=0.38, wspace=0.22)

out_path = os.path.join(os.path.dirname(__file__), "plot_placements_v2.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight', facecolor='white')
print(f"Saved placements plot to: {out_path}")
