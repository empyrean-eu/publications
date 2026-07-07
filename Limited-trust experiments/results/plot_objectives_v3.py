import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']

# Hardcoded from results_jsons5.md — Rollout avg_score (per successful application)
avg_iso  = [0.0698, 0.2028, 0.1624, 0.2534]
avg_t0   = [0.0624, 0.2013, 0.1725, 0.2490]
avg_t2   = [0.0524, 0.1879, 0.1717, 0.2477]
avg_t4   = [0.0509, 0.1896, 0.1729, 0.2455]
avg_t6   = [0.0507, 0.1859, 0.1712, 0.2430]
avg_t10  = [0.0504, 0.1828, 0.1704, 0.2361]

sub_bars = [avg_iso, avg_t0, avg_t2, avg_t4, avg_t6, avg_t10]
labels = ["Isolated", "Zero-Trust", "Fed-2", "Fed-4", "Fed-6", "Full-Trust"]

# Rollout failed services (%)
fail_iso = [2.70,  3.40, 14.91, 6.28]
fail_t0  = [0.00,  0.00,  3.80, 0.00]
fail_t2  = [0.00,  0.00,  2.33, 0.00]
fail_t4  = [0.00,  0.00,  1.33, 0.00]
fail_t6  = [0.00,  0.00,  0.33, 0.00]
fail_t10 = [0.00,  0.00,  0.00, 0.00]

fails = [fail_iso, fail_t0, fail_t2, fail_t4, fail_t6, fail_t10]

fig, ax1 = plt.subplots(figsize=(16, 6))
fig.patch.set_facecolor('#FFFFFF')
ax1.set_facecolor('#F8F9F9')
ax2 = ax1.twinx()

width = 0.11
thin_width = 0.025
offset = 0.008
group_spacing = 1.15

x = np.arange(len(scenarios)) * group_spacing
x_offsets = np.linspace(-0.40, 0.40, 6)

colors = ['#D6EAF8', '#AED6F1', '#85C1E9', '#5DADE2', '#3498DB', '#21618C']
color_fail = '#C0392B'

y_max = max(max(b) for b in sub_bars)
text_pad = y_max * 0.03

for i in range(6):
    xs = x + x_offsets[i]
    ax1.bar(
        xs, sub_bars[i], width, label=labels[i],
        color=colors[i], edgecolor='white', linewidth=1, zorder=3,
    )

    for j, val in enumerate(sub_bars[i]):
        ax1.text(
            xs[j], val + text_pad, f'{val:.4f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold',
            color='black', rotation=90,
        )

    xs_thin = xs + (width / 2) + (thin_width / 2) + offset
    ax2.bar(
        xs_thin, fails[i], thin_width,
        label='Failed Services (%)' if i == 0 else "",
        color=color_fail, edgecolor='white', linewidth=0.5, alpha=0.9, zorder=4,
    )

    for j, val in enumerate(fails[i]):
        if val > 0:
            ax2.text(
                xs_thin[j], val + 0.4, f'{val:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold',
                color='#922B21', rotation=90,
            )

ax1.set_ylabel('Avg Normalized Objective (per app)', fontsize=15, fontweight='bold')
ax2.set_ylabel('Failed Services (%)', fontsize=15, fontweight='bold', color=color_fail)

ax1.set_xticks(x)
ax1.set_xticklabels(scenarios, fontsize=15, fontweight='bold')
ax1.tick_params(axis='y', labelsize=13)
ax2.tick_params(axis='y', labelsize=13)

ax1.set_ylim(0, y_max * 1.35)
ax2.set_ylim(0, max(max(f) for f in fails) * 1.45)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(
    lines1 + lines2, labels1 + labels2,
    loc='upper center', bbox_to_anchor=(0.5, 1.18), ncol=7, fontsize=12, framealpha=0.9,
)

ax1.yaxis.grid(True, linestyle='-', alpha=0.4, color='#95A5A6', zorder=0)
ax1.set_axisbelow(True)

ax1.spines['top'].set_visible(False)
ax1.spines['left'].set_color('#BDC3C7')
ax1.spines['bottom'].set_color('#BDC3C7')

ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['right'].set_color('#BDC3C7')
ax2.spines['bottom'].set_color('#BDC3C7')

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "plot_objectives_v3.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved objective plot to: {out_path}")
