"""
Experiment 6 - Security Impact on Cost & Latency (Rollout)
Three scenarios per panel: objective-opt, Security-opt, Balanced (0.33/0.33/0.33).
Layout matches security_impact_metrics_v2.png.
Data: app_rollout_weights_log.txt (config_big, 100 apps).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PLOTS_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH = 0.32

# norm = normalized objective value (bar height)
# sec_impact = % attributable to security overhead (hatched segment)
# norm_sec = normalized security score
LATENCY = [
    # scenario     norm      sec_impact  norm_sec
    ('Latency',  14.9218,   12.73,      13.0145),
    ('Security', 71.0674,   27.22,      88.6076),
    ('Balanced', 27.0535,   14.31,      72.3813),
]

COST = [
    # scenario     norm      sec_impact  norm_sec
    ('Cost',     3.9270,    12.01,      6.6561),
    ('Security', 27.9538,   29.48,      88.6076),
    ('Balanced', 21.9581,   24.22,      72.3813),
]


def draw_panel(ax, rows, obj_label, sec_label, obj_color, obj_edge, title):
    scenarios = [r[0] for r in rows]
    norm = np.array([r[1] for r in rows])
    sec_pct = np.array([r[2] for r in rows])
    norm_sec = np.array([r[3] for r in rows])

    sec_part = norm * sec_pct / 100.0
    base_part = norm - sec_part

    x = np.arange(len(scenarios))

    ax.bar(x - WIDTH / 2, base_part, WIDTH, label=obj_label,
           color=obj_color, edgecolor='white', linewidth=0.5, zorder=3)
    ax.bar(x - WIDTH / 2, sec_part, WIDTH, bottom=base_part,
           label=sec_label, color=obj_color, edgecolor=obj_edge,
           linewidth=1.0, hatch='///', alpha=0.6, zorder=3)
    ax.bar(x + WIDTH / 2, norm_sec, WIDTH, label='Security Score',
           color='#27AE60', edgecolor='white', linewidth=0.5, zorder=3)

    for i in range(len(scenarios)):
        ax.text(x[i] - WIDTH / 2, norm[i] + 0.4, f'{norm[i]:.1f}',
                ha='center', va='bottom', fontsize=13, fontweight='bold', color=obj_edge)
        ax.text(x[i] + WIDTH / 2, norm_sec[i] + 0.4, f'{norm_sec[i]:.1f}',
                ha='center', va='bottom', fontsize=13, fontweight='bold', color='#1E8449')
        if sec_part[i] > 0.3:
            ax.text(x[i] - WIDTH / 2, base_part[i] + sec_part[i] / 2,
                    f'+{sec_pct[i]:.0f}%',
                    ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    ax.set_ylabel('Normalized Value', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=14, fontweight='bold')
    ax.tick_params(axis='y', labelsize=13)
    ax.legend(fontsize=13, loc='upper left', framealpha=0.9)
    ax.set_ylim(0, max(norm.max(), norm_sec.max()) * 1.15)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=12)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

draw_panel(ax1, LATENCY,
           obj_label='Base Latency',
           sec_label='mTLS Overhead',
           obj_color='#3498DB', obj_edge='#2471A3',
           title='Latency - Security')

draw_panel(ax2, COST,
           obj_label='Base Cost',
           sec_label='Additive Security Cost',
           obj_color='#E67E22', obj_edge='#A04000',
           title='Cost - Security')

plt.tight_layout()

out_path = os.path.join(PLOTS_DIR, "experiment6_security_impact_v2.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
