"""
Experiment 6 - Security Impact on Cost & Latency (with Mixed)

"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Data (Rollout, from results_big_*.json) ---

# Plot 1: Latency vs Security (3 scenarios)
plot1 = {
    'scenarios': ['Latency', 'Security', 'Balanced'],
    'norm_lat': [9.4917, 47.2929, 17.2241],
    'mtls_overhead_frac': [0.265, 0.987, 0.431],
    'norm_sec': [9.1467, 53.7503, 41.0921],
}

# Plot 2: Cost vs Security (3 scenarios)
plot2 = {
    'scenarios': ['Cost', 'Security', 'Balanced'],
    'norm_cost': [2.6042, 12.4064, 7.9986],
    'base_cost': [11990.5515, 38514.7366, 17669.3117],
    'additive': [1345.4078, 14800.9883, 6175.0679],
    'total_cost': [13335.9593, 53315.7249, 23844.3796],
    'norm_sec': [5.0464, 53.7503, 41.0921],
}

# --- Create figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

width = 0.32

# ==================== Plot 1: Latency & Security ====================
x1 = np.arange(len(plot1['scenarios']))

lat_base = []
lat_mtls = []
for i, nl in enumerate(plot1['norm_lat']):
    frac = plot1['mtls_overhead_frac'][i]
    mtls_part = nl * frac * 0.35
    base_part = nl - mtls_part
    lat_base.append(base_part)
    lat_mtls.append(mtls_part)

# Base latency
ax1.bar(x1 - width/2, lat_base, width, label='Base Latency',
        color='#3498DB', edgecolor='white', linewidth=0.5, zorder=3)
# mTLS overhead (hatched)
ax1.bar(x1 - width/2, lat_mtls, width, bottom=lat_base, label='mTLS Overhead',
        color='#3498DB', edgecolor='#1A5276', linewidth=1.0, hatch='///', alpha=0.6, zorder=3)
# Security bars
ax1.bar(x1 + width/2, plot1['norm_sec'], width, label='Security Score',
        color='#27AE60', edgecolor='white', linewidth=0.5, zorder=3)

# Value labels
for i in range(len(x1)):
    total_lat = plot1['norm_lat'][i]
    ax1.text(x1[i] - width/2, total_lat + 0.4, f'{total_lat:.1f}',
             ha='center', va='bottom', fontsize=13, fontweight='bold', color='#2471A3')
    ax1.text(x1[i] + width/2, plot1['norm_sec'][i] + 0.4, f'{plot1["norm_sec"][i]:.1f}',
             ha='center', va='bottom', fontsize=13, fontweight='bold', color='#1E8449')
    # mTLS overhead percentage annotation
    mtls_pct = lat_mtls[i] / plot1['norm_lat'][i] * 100
    ax1.text(x1[i] - width/2, lat_base[i] + lat_mtls[i]/2, f'+{mtls_pct:.0f}%',
             ha='center', va='center', fontsize=10, fontweight='bold', color='white')

ax1.set_ylabel('Normalized Value', fontsize=16, fontweight='bold')
ax1.set_xticks(x1)
ax1.set_xticklabels(plot1['scenarios'], fontsize=14, fontweight='bold')
ax1.tick_params(axis='y', labelsize=13)
ax1.legend(fontsize=14, loc='upper left', framealpha=0.9)
ax1.set_ylim(0, max(max(plot1['norm_lat']), max(plot1['norm_sec'])) * 1.15)
ax1.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_title('Latency - Security', fontsize=16, fontweight='bold', pad=12)

# ==================== Plot 2: Cost & Security ====================
x2 = np.arange(len(plot2['scenarios']))

plot2['additive_norm'] = []
plot2['base_norm'] = []
for i in range(len(plot2['scenarios'])):
    add_frac = plot2['additive'][i] / plot2['total_cost'][i]
    plot2['additive_norm'].append(plot2['norm_cost'][i] * add_frac)
    plot2['base_norm'].append(plot2['norm_cost'][i] * (1 - add_frac))

# Cost bars: base + hatched additive
ax2.bar(x2 - width/2, plot2['base_norm'], width, label='Base Cost',
        color='#E67E22', edgecolor='white', linewidth=0.5, zorder=3)
ax2.bar(x2 - width/2, plot2['additive_norm'], width, bottom=plot2['base_norm'],
        label='Additive Security Cost',
        color='#E67E22', edgecolor='#7E4A12', linewidth=1.0, hatch='///', alpha=0.6, zorder=3)
# Security bars
ax2.bar(x2 + width/2, plot2['norm_sec'], width, label='Security Score',
        color='#27AE60', edgecolor='white', linewidth=0.5, zorder=3)

# Value labels
for i in range(len(x2)):
    total_cost = plot2['norm_cost'][i]
    add_norm = plot2['additive_norm'][i]
    ax2.text(x2[i] - width/2, total_cost + 0.3, f'{total_cost:.1f}',
             ha='center', va='bottom', fontsize=13, fontweight='bold', color='#A04000')
    ax2.text(x2[i] + width/2, plot2['norm_sec'][i] + 0.3, f'{plot2["norm_sec"][i]:.1f}',
             ha='center', va='bottom', fontsize=13, fontweight='bold', color='#1E8449')
    # Additive cost annotation
    pct = plot2['additive'][i] / plot2['total_cost'][i] * 100
    ax2.text(x2[i] - width/2, plot2['base_norm'][i] + add_norm/2,
             f'+{pct:.0f}%', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

ax2.set_ylabel('Normalized Value', fontsize=16, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(plot2['scenarios'], fontsize=14, fontweight='bold')
ax2.tick_params(axis='y', labelsize=13)
ax2.legend(fontsize=14, loc='upper left', framealpha=0.9)
ax2.set_ylim(0, max(max(plot2['norm_cost']), max(plot2['norm_sec'])) * 1.15)
ax2.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
ax2.set_axisbelow(True)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_title('Cost - Security', fontsize=16, fontweight='bold', pad=12)

plt.tight_layout()

out_path = r"c:\Users\giorg\Desktop\security problem\python transition\Python_version_3\experiment6b_security_impact.png"
plt.savefig(out_path, dpi=600, bbox_inches='tight')
print(f"Saved to: {out_path}")
