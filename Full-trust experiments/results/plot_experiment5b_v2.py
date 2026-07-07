"""
Experiment 5b - Tier Distribution (stacked) + mTLS Activation (thin bar)
4 objective scenarios, Rollout only.
Data: app_rollout_weights_log.txt (config_big, 100 apps).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PLOTS_DIR = os.path.dirname(os.path.abspath(__file__))

# 570 services, 470 inter-service links (100-app big topology)
TOTAL_SERVICES = 570
TOTAL_LINKS = 470

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']

# Tier counts from log
tiers = {
    'Cost':     [272, 186, 104, 8],
    'Latency':  [271, 145, 103, 41],
    'Security': [0,   27,  435, 108],
    'Balanced': [10,  51,  424, 85],
}

# mTLS links active
mtls_on = {
    'Cost': 122,
    'Latency': 117,
    'Security': 461,
    'Balanced': 226,
}

tier_pct = {sc: [v / TOTAL_SERVICES * 100 for v in tiers[sc]] for sc in scenarios}
mtls_pct = {sc: mtls_on[sc] / TOTAL_LINKS * 100 for sc in scenarios}

fig, ax = plt.subplots(figsize=(10, 7))

t0_color = '#D5D8DC'
t1_color = '#AEB6BF'
t2_color = '#5DADE2'
t3_color = '#2E86C1'
mtls_color = '#E74C3C'

bar_width = 0.45
mtls_width = 0.10

x = np.arange(len(scenarios))
x_mtls = x + bar_width / 2 + mtls_width / 2 + 0.03

t0 = [tier_pct[sc][0] for sc in scenarios]
t1 = [tier_pct[sc][1] for sc in scenarios]
t2 = [tier_pct[sc][2] for sc in scenarios]
t3 = [tier_pct[sc][3] for sc in scenarios]

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
        if val > 8:
            ax.text(x[i], cum + val / 2, f'{val:.0f}%',
                    ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        cum += val

mtls_vals = [mtls_pct[sc] for sc in scenarios]
ax.bar(x_mtls, mtls_vals, mtls_width, label='mTLS (%)', color=mtls_color,
       edgecolor='white', linewidth=0.5, zorder=3, alpha=0.85)

for i, val in enumerate(mtls_vals):
    ax.text(x_mtls[i], val + 1.5, f'{val:.0f}%',
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#C0392B')

ax.set_ylabel('Distribution (%)', fontsize=16, fontweight='bold')
ax.set_ylim(0, 118)
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=15, fontweight='bold')
ax.tick_params(axis='y', labelsize=13)

ax.legend(fontsize=13, loc='upper center', framealpha=0.9, ncol=5,
          bbox_to_anchor=(0.5, 1.0))

ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

out_path = os.path.join(PLOTS_DIR, "experiment5b_tiers_mtls_v2.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
