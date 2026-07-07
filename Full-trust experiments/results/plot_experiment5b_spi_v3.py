"""
SPI experiment — tier placement (%), mTLS link activation (%), and normalized security.
5 SPI weight profiles, Balanced objective (0.33/0.33/0.33), Rollout only.
Data: spi_impact_20260626_161926.json (config_big, 100 apps).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PLOTS_DIR = os.path.dirname(os.path.abspath(__file__))

# scenario       T0%    T1%    T2%    T3%    mTLS%   norm_sec
DATA = [
    ('Balanced\nSPI',  1.75,  8.95, 74.39, 14.91, 48.09, 72.3813),
    ('mTLS\nx3',       5.79, 11.93, 69.12, 13.16, 64.26, 68.2455),
    ('Tier\nx3',       0.53,  5.26, 77.54, 16.67, 35.11, 82.4871),
    ('mTLS\nx5',       8.07, 12.11, 68.25, 11.58, 71.28, 72.9805),
    ('Tier\nx5',       0.35,  3.68, 77.77, 18.19, 30.21, 86.9132),
]

scenarios = [r[0] for r in DATA]
t0 = [r[1] for r in DATA]
t1 = [r[2] for r in DATA]
t2 = [r[3] for r in DATA]
t3 = [r[4] for r in DATA]
mtls = [r[5] for r in DATA]
norm_sec = [r[6] for r in DATA]

fig, ax = plt.subplots(figsize=(11, 7))
ax2 = ax.twinx()

t0_color = '#D5D8DC'
t1_color = '#AEB6BF'
t2_color = '#5DADE2'
t3_color = '#2E86C1'
mtls_color = '#E74C3C'
sec_color = '#27AE60'

bar_width = 0.45
thin_width = 0.10
gap = 0.03
x = np.arange(len(scenarios))
x_mtls = x + bar_width / 2 + thin_width / 2 + gap
x_sec = x_mtls + thin_width + gap

ax.bar(x, t0, bar_width, label='Tier 0', color=t0_color, edgecolor='white', linewidth=0.5, zorder=3)
bot1 = t0
ax.bar(x, t1, bar_width, bottom=bot1, label='Tier 1', color=t1_color, edgecolor='white', linewidth=0.5, zorder=3)
bot2 = [a + b for a, b in zip(bot1, t1)]
ax.bar(x, t2, bar_width, bottom=bot2, label='Tier 2', color=t2_color, edgecolor='white', linewidth=0.5, zorder=3)
bot3 = [a + b for a, b in zip(bot2, t2)]
ax.bar(x, t3, bar_width, bottom=bot3, label='Tier 3', color=t3_color, edgecolor='white', linewidth=0.5, zorder=3)

for i in range(len(scenarios)):
    cum = 0
    for val in [t0[i], t1[i], t2[i], t3[i]]:
        if val > 5:
            ax.text(x[i], cum + val / 2, f'{val:.0f}%',
                    ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        cum += val

ax.bar(x_mtls, mtls, thin_width, label='mTLS (%)', color=mtls_color,
       edgecolor='white', linewidth=0.5, zorder=3, alpha=0.85)

for i, val in enumerate(mtls):
    ax.text(x_mtls[i], val + 1.5, f'{val:.0f}%',
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#C0392B')

ax2.bar(x_sec, norm_sec, thin_width, label='Norm. Security',
        color=sec_color, edgecolor='white', linewidth=0.5, zorder=3, alpha=0.85)

for i, val in enumerate(norm_sec):
    ax2.text(x_sec[i], val + 0.8, f'{val:.1f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold', color='#1E8449')

ax.set_ylabel('Distribution (%)', fontsize=16, fontweight='bold')
ax2.set_ylabel('Normalized Security', fontsize=16, fontweight='bold', color=sec_color)
ax2.tick_params(axis='y', labelsize=13, colors=sec_color)

ax.set_ylim(0, 118)
sec_lo = min(norm_sec) - 8
sec_hi = max(norm_sec) + 8
ax2.set_ylim(sec_lo, sec_hi)

ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=15, fontweight='bold')
ax.tick_params(axis='y', labelsize=13)

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=12, loc='upper center',
          framealpha=0.9, ncol=6, bbox_to_anchor=(0.5, 1.0))

ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2.spines['right'].set_color(sec_color)

plt.tight_layout()

out_path = os.path.join(PLOTS_DIR, "experiment5b_spi_tiers_mtls_v3.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
