"""
plot_balanced_mtls_v2.py

Balanced scenario, Rollout — mTLS overhead sensitivity (config_big, 100 apps).
Results from mtls_sensitivity_results.json (run 2026-06-26, 470 links).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

multipliers = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
labels = ['0.25x', '0.5x', '0.75x', '1.0x', '1.25x', '1.5x', '2.0x']

activation_pct = [86.81, 69.57, 54.26, 48.09, 43.62, 40.43, 37.45]
lat_pct        = [10.35, 14.65, 15.44, 17.31, 18.88, 20.23, 22.51]
norm_add_lat   = [2.8607, 4.5345, 4.9248, 5.8505, 6.4663, 7.0753, 8.8904]
cpu_cores      = [51.32, 83.054, 96.444, 113.314, 129.522, 142.79, 176.23]
norm_sec       = [81.6512, 79.4375, 74.944, 72.3813, 71.2295, 68.6322, 67.9451]
norm_lat_tot   = [23.6971, 25.9526, 26.5132, 27.0535, 27.6777, 27.427, 28.9351]

color_lat = '#D35400'
color_cpu = '#27AE60'
color_norm = '#8E44AD'
color_bar = '#2E86C1'
color_sec = '#27AE60'

LEGEND_KW = dict(loc='upper center', fontsize=12, framealpha=0.92)


def _dual_axis_plot(ax_left, y_left, y_right,
                    ylab_left, ylab_right,
                    label_left, label_right,
                    ylim_left=(0, 100), ylim_sec_pad=0.4,
                    legend_kw=None):
    ax_left.set_xlabel('mTLS Overhead Multiplier', fontsize=16, fontweight='bold')
    ax_left.set_ylabel(ylab_left, fontsize=16, fontweight='bold', color=color_bar)
    l_left = ax_left.plot(multipliers, y_left, marker='s', markersize=9, linewidth=2.8,
                          color=color_bar, label=label_left)
    ax_left.tick_params(axis='y', labelcolor=color_bar, labelsize=14)
    ax_left.tick_params(axis='x', labelsize=14)
    ax_left.set_xticks(multipliers)
    ax_left.set_xticklabels(labels)
    ax_left.set_ylim(*ylim_left)

    ax_right = ax_left.twinx()
    ax_right.set_ylabel(ylab_right, fontsize=16, fontweight='bold', color=color_sec)
    l_right = ax_right.plot(multipliers, y_right, marker='^', markersize=9, linewidth=2.8,
                            color=color_sec, label=label_right)
    ax_right.tick_params(axis='y', labelcolor=color_sec, labelsize=14)
    sec_lo, sec_hi = min(y_right), max(y_right)
    sec_pad = (sec_hi - sec_lo) * ylim_sec_pad
    ax_right.set_ylim(sec_lo - sec_pad, sec_hi + sec_pad)

    lines = l_left + l_right
    ax_left.legend(lines, [l.get_label() for l in lines], **(legend_kw or LEGEND_KW))
    ax_left.grid(True, linestyle='--', alpha=0.5)
    return ax_left


def _triple_axis_plot(ax_left, y_left, y_mid, y_right,
                      ylab_left, ylab_mid, ylab_right,
                      label_left, label_mid, label_right,
                      color_mid, ylim_left=(0, 100), ylim_mid_pad=0.25, ylim_sec_pad=0.4):
    ax_left.set_xlabel('mTLS Overhead Multiplier', fontsize=16, fontweight='bold')
    ax_left.set_ylabel(ylab_left, fontsize=16, fontweight='bold', color=color_bar)
    l_left = ax_left.plot(multipliers, y_left, marker='s', markersize=9, linewidth=2.8,
                          color=color_bar, label=label_left)
    ax_left.tick_params(axis='y', labelcolor=color_bar, labelsize=14)
    ax_left.tick_params(axis='x', labelsize=14)
    ax_left.set_xticks(multipliers)
    ax_left.set_xticklabels(labels)
    ax_left.set_ylim(*ylim_left)

    ax_mid = ax_left.twinx()
    ax_mid.set_ylabel(ylab_mid, fontsize=16, fontweight='bold', color=color_mid)
    l_mid = ax_mid.plot(multipliers, y_mid, marker='o', markersize=9, linewidth=2.8,
                        color=color_mid, label=label_mid)
    ax_mid.tick_params(axis='y', labelcolor=color_mid, labelsize=14)
    mid_lo, mid_hi = min(y_mid), max(y_mid)
    mid_pad = (mid_hi - mid_lo) * ylim_mid_pad if mid_hi > mid_lo else mid_hi * 0.1
    ax_mid.set_ylim(max(0, mid_lo - mid_pad), mid_hi + mid_pad)

    ax_right = ax_left.twinx()
    ax_right.spines['right'].set_position(('outward', 65))
    ax_right.set_ylabel(ylab_right, fontsize=16, fontweight='bold', color=color_sec)
    l_right = ax_right.plot(multipliers, y_right, marker='^', markersize=9, linewidth=2.8,
                            color=color_sec, label=label_right)
    ax_right.tick_params(axis='y', labelcolor=color_sec, labelsize=14)
    sec_lo, sec_hi = min(y_right), max(y_right)
    sec_pad = (sec_hi - sec_lo) * ylim_sec_pad
    ax_right.set_ylim(sec_lo - sec_pad, sec_hi + sec_pad)

    lines = l_left + l_mid + l_right
    ax_left.legend(lines, [l.get_label() for l in lines], **LEGEND_KW)
    ax_left.grid(True, linestyle='--', alpha=0.5)
    return ax_left


# --- Plot: activation + normalized security (no latency) ---
fig5, ax5 = plt.subplots(figsize=(7.5, 6))
_dual_axis_plot(
    ax5, activation_pct, norm_sec,
    ylab_left='Activated mTLS Links (%)',
    ylab_right='Normalized Security',
    label_left='Activated mTLS Links (%)',
    label_right='Normalized Security',
    legend_kw=dict(loc='upper center', fontsize=16, framealpha=0.92,
                   handlelength=2.4, handleheight=1.4, labelspacing=0.6),
)
plt.tight_layout()
out5 = os.path.join(OUT_DIR, "balanced_activation_latency_lines_v3.png")
fig5.savefig(out5, dpi=300, bbox_inches='tight')
print(f"Saved: {out5}")
