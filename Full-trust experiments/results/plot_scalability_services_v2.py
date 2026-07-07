"""
plot_scalability_services_v2.py

Rollout scalability vs services per application ( from
rollout_scalability_services_per_app_results.json).
Execution Time vs Services per Application.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
ROLLOUT_COLOR = '#F39C12'

SERVICES_PER_APP = [
    {"services_per_app": 1, "total_machines": 197, "num_apps": 50, "total_services": 50,
     "time_rollout": 0.9976, "rollout_heuristic_calls": 14919},
    {"services_per_app": 2, "total_machines": 197, "num_apps": 50, "total_services": 100,
     "time_rollout": 1.735, "rollout_heuristic_calls": 42294},
    {"services_per_app": 3, "total_machines": 197, "num_apps": 50, "total_services": 150,
     "time_rollout": 3.1149, "rollout_heuristic_calls": 65848},
    {"services_per_app": 4, "total_machines": 197, "num_apps": 50, "total_services": 200,
     "time_rollout": 4.9738, "rollout_heuristic_calls": 85771},
    {"services_per_app": 5, "total_machines": 197, "num_apps": 50, "total_services": 250,
     "time_rollout": 7.4594, "rollout_heuristic_calls": 108837},
    {"services_per_app": 6, "total_machines": 197, "num_apps": 50, "total_services": 300,
     "time_rollout": 11.0476, "rollout_heuristic_calls": 129388},
    {"services_per_app": 7, "total_machines": 197, "num_apps": 50, "total_services": 350,
     "time_rollout": 15.1756, "rollout_heuristic_calls": 154593},
    {"services_per_app": 8, "total_machines": 197, "num_apps": 50, "total_services": 400,
     "time_rollout": 18.0779, "rollout_heuristic_calls": 168010},
    {"services_per_app": 9, "total_machines": 197, "num_apps": 50, "total_services": 450,
     "time_rollout": 24.215, "rollout_heuristic_calls": 193525},
    {"services_per_app": 10, "total_machines": 197, "num_apps": 50, "total_services": 500,
     "time_rollout": 26.4711, "rollout_heuristic_calls": 194705},
    {"services_per_app": 11, "total_machines": 197, "num_apps": 50, "total_services": 550,
     "time_rollout": 34.6495, "rollout_heuristic_calls": 231492},
    {"services_per_app": 12, "total_machines": 197, "num_apps": 50, "total_services": 600,
     "time_rollout": 42.3666, "rollout_heuristic_calls": 250069},
    {"services_per_app": 13, "total_machines": 197, "num_apps": 50, "total_services": 650,
     "time_rollout": 48.0581, "rollout_heuristic_calls": 263895},
    {"services_per_app": 14, "total_machines": 197, "num_apps": 50, "total_services": 700,
     "time_rollout": 58.4701, "rollout_heuristic_calls": 291203},
    {"services_per_app": 15, "total_machines": 197, "num_apps": 50, "total_services": 750,
     "time_rollout": 59.2764, "rollout_heuristic_calls": 289663},
    {"services_per_app": 16, "total_machines": 197, "num_apps": 50, "total_services": 800,
     "time_rollout": 68.2765, "rollout_heuristic_calls": 303152},
    {"services_per_app": 17, "total_machines": 197, "num_apps": 50, "total_services": 850,
     "time_rollout": 73.852, "rollout_heuristic_calls": 311180},
    {"services_per_app": 18, "total_machines": 197, "num_apps": 50, "total_services": 900,
     "time_rollout": 82.2072, "rollout_heuristic_calls": 330839},
    {"services_per_app": 19, "total_machines": 197, "num_apps": 50, "total_services": 950,
     "time_rollout": 89.8578, "rollout_heuristic_calls": 337671},
    {"services_per_app": 20, "total_machines": 197, "num_apps": 50, "total_services": 1000,
     "time_rollout": 98.1901, "rollout_heuristic_calls": 347423},
]


def _style_axis(ax):
    ax.tick_params(axis='both', labelsize=16)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, zorder=0)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def main():
    svc_per_app = [r["services_per_app"] for r in SERVICES_PER_APP]
    t_rollout = [r["time_rollout"] for r in SERVICES_PER_APP]

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(svc_per_app, t_rollout, marker='s', linestyle='-', linewidth=2,
             color=ROLLOUT_COLOR, label='App Rollout', zorder=3)
    ax1.set_xlabel("Services per Application ($I_c$)", fontsize=20, fontweight='bold')
    ax1.set_ylabel("Execution time (seconds)", fontsize=20, fontweight='bold')
    _style_axis(ax1)
    plt.tight_layout()
    out1 = os.path.join(OUT_DIR, "scalability_services_v2.png")
    fig1.savefig(out1, dpi=300, bbox_inches='tight')
    print(f"Saved: {out1}")


if __name__ == "__main__":
    main()
