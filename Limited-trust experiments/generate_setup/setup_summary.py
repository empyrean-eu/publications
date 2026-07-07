"""
Print tables and save summary plots after topology + workload generation.
"""
import os
from typing import List, Optional

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from structs import Topology, Application

TIER_NAMES = {1: 'Near-Edge', 2: 'Far-Edge', 3: 'Cloud'}
SEC_LABELS = ['Tier 0', 'Tier 1', 'Tier 2', 'Tier 3']


def _pct(n, total):
    return 100.0 * n / total if total else 0.0


def _bar_table(headers, rows, col_widths=None):
    if not rows:
        return ''
    if col_widths is None:
        col_widths = [max(len(str(h)), max(len(str(r[i])) for r in rows)) + 2
                      for i, h in enumerate(headers)]
    sep = '|' + '|'.join('-' * w for w in col_widths) + '|'
    lines = ['|' + '|'.join(str(h).center(w) for h, w in zip(headers, col_widths)) + '|', sep]
    for row in rows:
        lines.append('|' + '|'.join(str(v).center(w) for v, w in zip(row, col_widths)) + '|')
    return '\n'.join(lines)


def collect_topology_stats(topo: Topology, num_clusters: int):
    cats = topo.node_categories
    clusters = topo.node_clusters
    machines = topo.machines

    node_rows = []
    for tier in (1, 2, 3):
        mask = cats == tier
        node_rows.append([
            TIER_NAMES[tier],
            int(mask.sum()),
            f"{_pct(mask.sum(), topo.num_nodes):.1f}%",
        ])

    cluster_node_rows = []
    for c in range(num_clusters):
        cmask = clusters == c
        ne = int(np.sum(cmask & (cats == 1)))
        fe = int(np.sum(cmask & (cats == 2)))
        cl = int(np.sum(cmask & (cats == 3)))
        cluster_node_rows.append([c, ne, fe, cl, ne + fe + cl])

    mach_per_node = {}
    for n_id in range(topo.num_nodes):
        mach_per_node[n_id] = int(np.sum(machines[:, topo.NODE_IDX].astype(int) == n_id))

    sec_tiers = machines[:, topo.SEC_IDX].astype(int)
    sec_counts = [int(np.sum(sec_tiers == t)) for t in range(4)]

    cpu_vals = machines[:, topo.CPU_IDX]
    cost_vals = machines[:, topo.COST_IDX]

    mach_tier_rows = []
    for tier in (1, 2, 3):
        node_mask = cats == tier
        node_ids = np.where(node_mask)[0]
        m_count = int(np.sum(np.isin(machines[:, topo.NODE_IDX].astype(int), node_ids)))
        mach_tier_rows.append([TIER_NAMES[tier], m_count, f"{_pct(m_count, len(machines)):.1f}%"])

    return {
        'node_rows': node_rows,
        'cluster_node_rows': cluster_node_rows,
        'mach_tier_rows': mach_tier_rows,
        'sec_counts': sec_counts,
        'mach_per_node': mach_per_node,
        'cpu_min': float(cpu_vals.min()), 'cpu_max': float(cpu_vals.max()), 'cpu_mean': float(cpu_vals.mean()),
        'cost_min': float(cost_vals.min()), 'cost_max': float(cost_vals.max()), 'cost_mean': float(cost_vals.mean()),
        'total_machines': len(machines),
    }


def collect_workload_stats(apps: List[Application], num_clusters: int, include_clusters: bool = False):
    chain_lens = [len(a.microservices) for a in apps]
    total_svc = sum(chain_lens)
    total_links = sum(len(a.mtls_requirements) for a in apps)
    mtls_on = sum(sum(a.mtls_requirements) for a in apps)

    uni = sum(1 for a in apps for ms in a.microservices if ms.max_security == 3)
    heavy = sum(1 for a in apps for ms in a.microservices if ms.cpu_demand >= 1.0)

    min_sec = [ms.min_security for a in apps for ms in a.microservices]
    max_sec = [ms.max_security for a in apps for ms in a.microservices]
    data_sizes = [ms.data_size for a in apps for ms in a.microservices]
    mtls_cpu = [ov for a in apps for ov in a.mtls_overheads]

    apps_per_cluster = {c: 0 for c in range(num_clusters)}
    svc_per_cluster = {c: 0 for c in range(num_clusters)}
    for a in apps:
        c = a.source_cluster
        apps_per_cluster[c] = apps_per_cluster.get(c, 0) + 1
        svc_per_cluster[c] = svc_per_cluster.get(c, 0) + len(a.microservices)

    app_rows = []
    for a in apps[:8]:
        row = [a.id, len(a.microservices), sum(a.mtls_requirements)]
        if include_clusters:
            row = [a.id, a.source_cluster, len(a.microservices), sum(a.mtls_requirements)]
        app_rows.append(row)

    return {
        'chain_lens': chain_lens,
        'total_svc': total_svc,
        'total_links': total_links,
        'mtls_on': mtls_on,
        'uni': uni,
        'heavy': heavy,
        'min_sec': min_sec,
        'max_sec': max_sec,
        'data_sizes': data_sizes,
        'mtls_cpu': mtls_cpu,
        'apps_per_cluster': apps_per_cluster,
        'svc_per_cluster': svc_per_cluster,
        'app_rows': app_rows,
        'num_apps': len(apps),
    }


def build_markdown(topo: Topology, apps: List[Application], cfg,
                   trust_level: Optional[int] = None, include_clusters: bool = False) -> str:
    ts = collect_topology_stats(topo, cfg.NUM_CLUSTERS)
    ws = collect_workload_stats(apps, cfg.NUM_CLUSTERS, include_clusters=include_clusters)

    header = f'**Seed:** {cfg.SEED}  |  **Applications:** {ws["num_apps"]}  |  **Services:** {ws["total_svc"]}'
    if include_clusters:
        header = f'**Seed:** {cfg.SEED}  |  **Clusters:** {cfg.NUM_CLUSTERS}  |  **Applications:** {ws["num_apps"]}  |  **Services:** {ws["total_svc"]}'
    if trust_level is not None:
        header += f'  |  **Trust level:** {trust_level}'

    lines = [
        '# Experimental Setup Summary',
        '',
        header,
        '',
        '## Infrastructure — Nodes by Tier',
        '',
        _bar_table(['Tier', 'Nodes', 'Share'], ts['node_rows']),
    ]

    if include_clusters:
        lines += [
            '',
            '## Infrastructure — Nodes per Cluster',
            '',
            _bar_table(['Cluster', 'Near-Edge', 'Far-Edge', 'Cloud', 'Total'], ts['cluster_node_rows']),
        ]

    lines += [
        '',
        '## Infrastructure — Machines',
        '',
        f'- **Total machines:** {ts["total_machines"]}',
        f'- **Per tier:** ' + ', '.join(f'{r[0]}: {r[1]} ({r[2]})' for r in ts['mach_tier_rows']),
        f'- **Security tier on machines:** ' +
        ', '.join(f'{SEC_LABELS[t]}: {ts["sec_counts"][t]} ({_pct(ts["sec_counts"][t], ts["total_machines"]):.1f}%)'
                  for t in range(4)),
        f'- **CPU capacity (cores):** min={ts["cpu_min"]:.2f}, mean={ts["cpu_mean"]:.2f}, max={ts["cpu_max"]:.2f}',
        f'- **Cost rate:** min={ts["cost_min"]:.2f}, mean={ts["cost_mean"]:.2f}, max={ts["cost_max"]:.2f}',
        f'- **Machines per node:** min={min(ts["mach_per_node"].values())}, '
        f'max={max(ts["mach_per_node"].values())}, '
        f'mean={np.mean(list(ts["mach_per_node"].values())):.2f}',
        '',
        '## Workload — Aggregate',
        '',
        f'- **Services per app:** min={min(ws["chain_lens"])}, max={max(ws["chain_lens"])}, '
        f'mean={np.mean(ws["chain_lens"]):.2f}',
        f'- **Unikernel-capable services:** {ws["uni"]} ({_pct(ws["uni"], ws["total_svc"]):.1f}%)',
        f'- **Heavy services (CPU >= 1.0):** {ws["heavy"]} ({_pct(ws["heavy"], ws["total_svc"]):.1f}%)',
        f'- **Inter-service links:** {ws["total_links"]}  |  **mTLS required:** {ws["mtls_on"]} '
        f'({_pct(ws["mtls_on"], ws["total_links"]):.1f}%)',
        f'- **Payload size (MB):** min={min(ws["data_sizes"]):.2f}, mean={np.mean(ws["data_sizes"]):.2f}, '
        f'max={max(ws["data_sizes"]):.2f}',
        f'- **mTLS CPU overhead (cores):** min={min(ws["mtls_cpu"]):.3f}, '
        f'mean={np.mean(ws["mtls_cpu"]):.3f}, max={max(ws["mtls_cpu"]):.3f}',
    ]

    if include_clusters:
        lines += [
            '',
            '## Workload — Apps per Cluster',
            '',
            _bar_table(
                ['Cluster', 'Apps', 'Services'],
                [[c, ws['apps_per_cluster'][c], ws['svc_per_cluster'][c]] for c in range(cfg.NUM_CLUSTERS)],
            ),
        ]

    sample_headers = (['App ID', 'Origin Cluster', 'Chain Len', 'mTLS Links']
                      if include_clusters else ['App ID', 'Chain Len', 'mTLS Links'])
    lines += [
        '',
        '## Sample Applications (first 8)',
        '',
        _bar_table(sample_headers, ws['app_rows']),
    ]
    return '\n'.join(lines)


def save_plots(topo: Topology, apps: List[Application], cfg, out_dir: str,
               trust_level: Optional[int] = None, include_clusters: bool = False):
    os.makedirs(out_dir, exist_ok=True)
    ts = collect_topology_stats(topo, cfg.NUM_CLUSTERS)
    ws = collect_workload_stats(apps, cfg.NUM_CLUSTERS, include_clusters=include_clusters)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.suptitle('Infrastructure Summary', fontsize=14, fontweight='bold')

    ax = axes[0]
    tiers = [TIER_NAMES[t] for t in (1, 2, 3)]
    counts = [int(np.sum(topo.node_categories == t)) for t in (1, 2, 3)]
    ax.bar(tiers, counts, color=['#7F8C8D', '#27AE60', '#85C1E9'], edgecolor='white')
    ax.set_title('Nodes by Tier')
    ax.set_ylabel('Count')
    for i, v in enumerate(counts):
        ax.text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    ax = axes[1]
    ax.bar(SEC_LABELS, ts['sec_counts'], color='#5DADE2', edgecolor='white')
    ax.set_title('Machines by Max Security Tier')
    ax.set_ylabel('Count')
    for i, v in enumerate(ts['sec_counts']):
        ax.text(i, v + 1, str(v), ha='center', fontsize=9, fontweight='bold')

    ax = axes[2]
    if include_clusters:
        clusters = np.arange(cfg.NUM_CLUSTERS)
        ne = [int(np.sum((topo.node_clusters == c) & (topo.node_categories == 1))) for c in clusters]
        fe = [int(np.sum((topo.node_clusters == c) & (topo.node_categories == 2))) for c in clusters]
        cl = [int(np.sum((topo.node_clusters == c) & (topo.node_categories == 3))) for c in clusters]
        ax.bar(clusters, ne, label='Near-Edge', color='#7F8C8D')
        ax.bar(clusters, fe, bottom=ne, label='Far-Edge', color='#27AE60')
        ax.bar(clusters, cl, bottom=np.array(ne) + np.array(fe), label='Cloud', color='#85C1E9')
        ax.set_title('Nodes per Cluster')
        ax.set_xlabel('Cluster ID')
        ax.set_ylabel('Nodes')
        ax.legend(fontsize=8)
    else:
        tier_labels = [r[0] for r in ts['mach_tier_rows']]
        tier_counts = [r[1] for r in ts['mach_tier_rows']]
        ax.bar(tier_labels, tier_counts, color=['#7F8C8D', '#27AE60', '#85C1E9'], edgecolor='white')
        ax.set_title('Machines by Infrastructure Tier')
        ax.set_ylabel('Count')
        for i, v in enumerate(tier_counts):
            ax.text(i, v + 1, str(v), ha='center', fontweight='bold')

    plt.tight_layout()
    p1 = os.path.join(out_dir, 'summary_infrastructure.png')
    fig.savefig(p1, dpi=150, bbox_inches='tight')
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('Workload Summary', fontsize=14, fontweight='bold')

    ax = axes[0, 0]
    ax.hist(ws['chain_lens'], bins=range(cfg.MIN_SERVICES, cfg.MAX_SERVICES + 2),
            color='#3498DB', edgecolor='white', align='left')
    ax.set_title('Services per Application')
    ax.set_xlabel('Chain length')
    ax.set_ylabel('Applications')

    ax = axes[0, 1]
    min_counts = [ws['min_sec'].count(t) for t in range(4)]
    max_counts = [ws['max_sec'].count(t) for t in range(4)]
    x = np.arange(4)
    w = 0.35
    ax.bar(x - w/2, min_counts, w, label='Min required tier', color='#AED6F1')
    ax.bar(x + w/2, max_counts, w, label='Max supported tier', color='#21618C')
    ax.set_xticks(x)
    ax.set_xticklabels(SEC_LABELS)
    ax.set_title('Service Security Tiers')
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    if ws['mtls_cpu'] and ws['data_sizes']:
        link_payloads = []
        link_cpu = []
        for a in apps:
            for j, ov in enumerate(a.mtls_overheads):
                link_payloads.append(a.microservices[j].data_size)
                link_cpu.append(ov)
        ax.scatter(link_payloads, link_cpu, alpha=0.35, s=18, color='#E74C3C')
        ax.set_xlabel('Incoming payload (MB)')
        ax.set_ylabel('mTLS CPU overhead (cores)')
        ax.set_title('mTLS Overhead vs Payload')
    else:
        ax.text(0.5, 0.5, 'No inter-service links', ha='center', va='center', transform=ax.transAxes)

    ax = axes[1, 1]
    if include_clusters:
        clusters = list(ws['apps_per_cluster'].keys())
        ax.bar(clusters, [ws['apps_per_cluster'][c] for c in clusters],
               color='#9B59B6', edgecolor='white', label='Apps')
        ax2 = ax.twinx()
        ax2.plot(clusters, [ws['svc_per_cluster'][c] for c in clusters],
                 color='#E67E22', marker='o', linewidth=2, label='Services')
        ax.set_title('Apps & Services per Cluster')
        ax.set_xlabel('Cluster ID')
        ax.set_ylabel('Applications', color='#9B59B6')
        ax2.set_ylabel('Services', color='#E67E22')
    else:
        ax.hist(ws['data_sizes'], bins=15, color='#1ABC9C', edgecolor='white')
        ax.set_title('Service Payload Size Distribution')
        ax.set_xlabel('Data size (MB)')
        ax.set_ylabel('Services')

    plt.tight_layout()
    p2 = os.path.join(out_dir, 'summary_workload.png')
    fig.savefig(p2, dpi=150, bbox_inches='tight')
    plt.close(fig)

    p3 = None
    if trust_level is not None and topo.trust_matrix is not None:
        fig, ax = plt.subplots(figsize=(7, 6))
        im = ax.imshow(topo.trust_matrix, cmap='Blues', vmin=0, vmax=1)
        ax.set_title(f'Trust Matrix (level={trust_level})')
        ax.set_xlabel('Target cluster')
        ax.set_ylabel('Source cluster')
        ax.set_xticks(range(cfg.NUM_CLUSTERS))
        ax.set_yticks(range(cfg.NUM_CLUSTERS))
        for i in range(cfg.NUM_CLUSTERS):
            for j in range(cfg.NUM_CLUSTERS):
                ax.text(j, i, int(topo.trust_matrix[i, j]), ha='center', va='center',
                        color='white' if topo.trust_matrix[i, j] else 'black', fontsize=8)
        fig.colorbar(im, ax=ax, fraction=0.046)
        plt.tight_layout()
        p3 = os.path.join(out_dir, 'summary_trust_matrix.png')
        fig.savefig(p3, dpi=150, bbox_inches='tight')
        plt.close(fig)

    return p1, p2, p3


def print_console_summary(topo: Topology, apps: List[Application], cfg,
                          trust_level: Optional[int] = None, include_clusters: bool = False):
    md = build_markdown(topo, apps, cfg, trust_level, include_clusters=include_clusters)
    print('\n' + '=' * 72)
    try:
        print(md)
    except UnicodeEncodeError:
        print(md.encode('ascii', errors='replace').decode('ascii'))
    print('=' * 72)


def emit_setup_summary(topo: Topology, apps: List[Application], cfg,
                       out_dir: Optional[str] = None, trust_level: Optional[int] = None,
                       include_clusters: Optional[bool] = None):
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(__file__), 'summary')
    if include_clusters is None:
        include_clusters = trust_level is not None

    md = build_markdown(topo, apps, cfg, trust_level, include_clusters=include_clusters)
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, 'setup_summary.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)

    plots = save_plots(topo, apps, cfg, out_dir, trust_level, include_clusters=include_clusters)
    print_console_summary(topo, apps, cfg, trust_level, include_clusters=include_clusters)

    print(f'\nSaved summary markdown: {md_path}')
    print(f'Saved plots: {plots[0]}, {plots[1]}' + (f', {plots[2]}' if plots[2] else ''))
    return md_path, plots
