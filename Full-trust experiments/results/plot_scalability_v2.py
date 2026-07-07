"""
plot_scalability_v2.py

Rollout scalability plots (results from rollout_scalability_*_results.json).
1. Execution Time vs Total Machines (Infrastructure Scale)
2. Execution Time vs Total Services (Workload Scale)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
ROLLOUT_COLOR = '#F39C12'

INFRASTRUCTURE = [
    {"target_machines": 25, "total_nodes": 10, "edge": 7, "fog": 2, "cloud": 1,
     "total_machines": 23, "num_apps": 50, "total_services": 299,
     "time_rollout": 1.5951, "rollout_heuristic_calls": 3158},
    {"target_machines": 50, "total_nodes": 23, "edge": 16, "fog": 5, "cloud": 2,
     "total_machines": 50, "num_apps": 50, "total_services": 296,
     "time_rollout": 3.2855, "rollout_heuristic_calls": 19430},
    {"target_machines": 150, "total_nodes": 68, "edge": 48, "fog": 14, "cloud": 6,
     "total_machines": 150, "num_apps": 50, "total_services": 270,
     "time_rollout": 7.1867, "rollout_heuristic_calls": 80067},
    {"target_machines": 200, "total_nodes": 94, "edge": 66, "fog": 19, "cloud": 9,
     "total_machines": 197, "num_apps": 50, "total_services": 310,
     "time_rollout": 13.1938, "rollout_heuristic_calls": 134054},
    {"target_machines": 250, "total_nodes": 116, "edge": 81, "fog": 23, "cloud": 12,
     "total_machines": 249, "num_apps": 50, "total_services": 271,
     "time_rollout": 15.6373, "rollout_heuristic_calls": 139669},
    {"target_machines": 300, "total_nodes": 138, "edge": 97, "fog": 28, "cloud": 13,
     "total_machines": 301, "num_apps": 50, "total_services": 268,
     "time_rollout": 17.574, "rollout_heuristic_calls": 180663},
    {"target_machines": 350, "total_nodes": 167, "edge": 117, "fog": 33, "cloud": 17,
     "total_machines": 349, "num_apps": 50, "total_services": 293,
     "time_rollout": 22.3355, "rollout_heuristic_calls": 227887},
    {"target_machines": 400, "total_nodes": 186, "edge": 130, "fog": 37, "cloud": 19,
     "total_machines": 402, "num_apps": 50, "total_services": 309,
     "time_rollout": 25.482, "rollout_heuristic_calls": 291577},
    {"target_machines": 450, "total_nodes": 214, "edge": 150, "fog": 43, "cloud": 21,
     "total_machines": 450, "num_apps": 50, "total_services": 280,
     "time_rollout": 31.8401, "rollout_heuristic_calls": 301507},
    {"target_machines": 500, "total_nodes": 232, "edge": 162, "fog": 46, "cloud": 24,
     "total_machines": 499, "num_apps": 50, "total_services": 301,
     "time_rollout": 36.1154, "rollout_heuristic_calls": 357395},
]

WORKLOAD = [
    {"target_total_services": 100, "total_machines": 197, "num_apps": 17,
     "total_services": 108, "time_rollout": 5.6087, "rollout_heuristic_calls": 53429},
    {"target_total_services": 200, "total_machines": 197, "num_apps": 33,
     "total_services": 213, "time_rollout": 10.0437, "rollout_heuristic_calls": 96245},
    {"target_total_services": 300, "total_machines": 197, "num_apps": 50,
     "total_services": 310, "time_rollout": 12.9927, "rollout_heuristic_calls": 134054},
    {"target_total_services": 400, "total_machines": 197, "num_apps": 67,
     "total_services": 395, "time_rollout": 15.8536, "rollout_heuristic_calls": 166121},
    {"target_total_services": 500, "total_machines": 197, "num_apps": 83,
     "total_services": 491, "time_rollout": 18.5699, "rollout_heuristic_calls": 195414},
    {"target_total_services": 600, "total_machines": 197, "num_apps": 100,
     "total_services": 598, "time_rollout": 22.1364, "rollout_heuristic_calls": 221975},
    {"target_total_services": 700, "total_machines": 197, "num_apps": 117,
     "total_services": 694, "time_rollout": 24.6501, "rollout_heuristic_calls": 242788},
    {"target_total_services": 800, "total_machines": 197, "num_apps": 133,
     "total_services": 799, "time_rollout": 27.4662, "rollout_heuristic_calls": 262651},
    {"target_total_services": 900, "total_machines": 197, "num_apps": 150,
     "total_services": 921, "time_rollout": 29.2511, "rollout_heuristic_calls": 265195},
    {"target_total_services": 1000, "total_machines": 197, "num_apps": 167,
     "total_services": 1037, "time_rollout": 31.5541, "rollout_heuristic_calls": 286367},
]


def _style_axis(ax):
    ax.tick_params(axis='both', labelsize=16)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, zorder=0)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def main():
    machines = [r["total_machines"] for r in INFRASTRUCTURE]
    infra_time = [r["time_rollout"] for r in INFRASTRUCTURE]

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(machines, infra_time, marker='s', linestyle='-', linewidth=2,
             color=ROLLOUT_COLOR, label='App Rollout', zorder=3)
    ax1.set_xlabel("Number of Machines ($M$)", fontsize=20, fontweight='bold')
    ax1.set_ylabel("Execution time (seconds)", fontsize=20, fontweight='bold')
    _style_axis(ax1)
    plt.tight_layout()
    out1 = os.path.join(OUT_DIR, "scalability_infrastructure_v2.png")
    fig1.savefig(out1, dpi=300, bbox_inches='tight')
    print(f"Saved: {out1}")

    services = [r["total_services"] for r in WORKLOAD]
    work_time = [r["time_rollout"] for r in WORKLOAD]

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(services, work_time, marker='s', linestyle='-', linewidth=2,
             color=ROLLOUT_COLOR, label='App Rollout', zorder=3)
    ax2.set_xlabel("Number of Services", fontsize=20, fontweight='bold')
    ax2.set_ylabel("Execution time (seconds)", fontsize=20, fontweight='bold')
    _style_axis(ax2)
    plt.tight_layout()
    out2 = os.path.join(OUT_DIR, "scalability_workload_v2.png")
    fig2.savefig(out2, dpi=300, bbox_inches='tight')
    print(f"Saved: {out2}")


if __name__ == "__main__":
    main()
