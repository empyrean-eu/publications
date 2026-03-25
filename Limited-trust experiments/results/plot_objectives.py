import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

scenarios = ['Cost', 'Latency', 'Security', 'Balanced']

# Main Objective Values
obj_iso = [7.815, 19.762, 14.998, 28.855]
obj_t0 = [8.136, 21.098, 18.574, 26.126]
obj_t3 = [6.521, 19.596, 19.125, 25.819]
obj_t10 = [5.834, 18.967, 19.636, 24.186]

sub_bars = [obj_iso, obj_t0, obj_t3, obj_t10]
labels = ["Isolated", "Zero-Trust", "Federated", "Full-Trust"]

# Failed Services % (Failures / 634 * 100)
fail_iso = [23/634*100, 30/634*100, 104/634*100, 49/634*100]
fail_t0 = [0, 0, 27/634*100, 0]
fail_t3 = [0, 0, 10/634*100, 0]
fail_t10 = [0, 0, 0/634*100, 0]

fails = [fail_iso, fail_t0, fail_t3, fail_t10]

fig, ax1 = plt.subplots(figsize=(14, 5.5))
fig.patch.set_facecolor('#FFFFFF')
ax1.set_facecolor('#F8F9F9')
ax2 = ax1.twinx()

width = 0.14
thin_width = 0.03
offset = 0.01
group_spacing = 0.95

x = np.arange(len(scenarios)) * group_spacing
# Offsets for the 4 methods
x_offsets = [-0.32, -0.12, 0.08, 0.28]

colors = ['#D6EAF8', '#85C1E9', '#3498DB', '#21618C']
color_fail = '#C0392B'

for i in range(4):
    xs = x + x_offsets[i]
    ax1.bar(xs, sub_bars[i], width, label=labels[i], color=colors[i], edgecolor='white', linewidth=1, zorder=3)
    
    # Add text to the main bars
    for j, val in enumerate(sub_bars[i]):
        ax1.text(xs[j], val + 0.5, f'{val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold', color='black', rotation=90)
    
    # Thin bars for failures
    xs_thin = xs + (width/2) + (thin_width/2) + offset
    ax2.bar(xs_thin, fails[i], thin_width, label='Failed Services (%)' if i == 0 else "", color=color_fail, edgecolor='white', linewidth=0.5, alpha=0.9, zorder=4)

    # Add text to thin bars if fail > 0
    for j, val in enumerate(fails[i]):
        if val > 0:
            ax2.text(xs_thin[j], val + 0.5, f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#922B21', rotation=90)


ax1.set_ylabel('Normalized Objective Value', fontsize=16, fontweight='bold')
ax2.set_ylabel('Failed Services (%)', fontsize=16, fontweight='bold', color=color_fail)

ax1.set_xticks(x)
ax1.set_xticklabels(scenarios, fontsize=16, fontweight='bold')
ax1.tick_params(axis='y', labelsize=14)
ax2.tick_params(axis='y', labelsize=14)

ax1.set_ylim(0, max([max(b) for b in sub_bars]) * 1.3)
ax2.set_ylim(0, max([max(f) for f in fails]) * 1.5)

# Legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 1.22), ncol=5, fontsize=14, framealpha=0.9)

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
out_path = os.path.join(os.path.dirname(__file__), "plot_objectives.png")
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved objective plot to: {out_path}")
