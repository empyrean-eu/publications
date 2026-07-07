# Initial Experiments

This folder contains all artifacts for **experimental sections 6.2**, 6.3 and 6.4  which evaluate security-aware microservice placement under a **fully collaborative Association** (all orchestration clusters mutually trust each other, i.e., `t_{o,o'} = 1 ∀ o, o'`). Cross-cluster placements therefore do not trigger additional security constraints, enabling a clean evaluation of algorithm performance and security trade-offs.

---

## Config Files

| File | Topology |
| `[config/config.py](config/config.py)` | Basic (22 nodes)
| `[config/config_big.py](config/config_big.py)` | Extended (90 nodes)

---



## Experimental Setup Generator

You can generate and preview the experimental setup (topology and workload) using the provided generator script. This script reads the configuration and outputs a summary of the generated infrastructure nodes, clusters, applications, and microservices.

```bash
python generator.py
```

Running the generator prints summary **tables** to the console and writes artifacts under `generate_setup/summary/`:

- `setup_summary.md` — markdown tables (nodes, machines, clusters, workload stats, sample apps)
- `summary_infrastructure.png` — node tiers, machine security tiers, cluster layout, machines/node histogram
- `summary_workload.png` — chain lengths, security tiers, mTLS vs payload, apps/services per cluster
- `summary_trust_matrix.png` — trust matrix heatmap *(Limited-trust only)*

> **Note:** The generator relies on the config files in the `config/` directory and `structs.py` to define the parameters and class structures. You can modify these configuration files to define your custom parameters and then re-run the generator to produce your own experimental setup.

---



## Experiments



### Experiment 1 — Optimality Gap Analysis

**Topology:** Basic | **Config:** `config.py`

Compares the normalised objective scores of Greedy best-fit, Simulated Annealing, and the multi-agent Rollout against the optimal ILP (CP-SAT) solution across four optimisation scenarios (cost, latency, security, balanced).

**Plot:** `[results/experiment1_optimality_gap3.png](results/experiment1_optimality_gap3.png)`
**Script:** `[results/plot_experiment1.py](results/plot_experiment1.py)`

Experiment 1

---



### Experiment 3 — Normalised Metrics Comparison (Extended Scale)

**Topology:** Extended | **Config:** `config_big.py`

Compares Greedy, Simulated Annealing, and Rollout across all three normalised objectives (cost, latency, security) on the large topology. No ILP baseline (intractable at this scale).

**Plot:** `[results/experiment3_normalized_metrics_v2.png](results/experiment3_normalized_metrics_v2.png)`
**Script:** `[results/plot_experiment3_v2.py](results/plot_experiment3_v2.py)`

Experiment 3

---



### Experiment 4 — Layer Placement Distribution (Extended Scale)

**Topology:** Extended | **Config:** `config_big.py`

Analyses where microservices are placed (near-edge / far-edge / cloud) for each optimisation scenario, revealing how objective weights shape placement across the continuum.

**Plot:** `[results/experiment4_placement_v2.png](results/experiment4_placement_v2.png)`
**Script:** `[results/plot_experiment4_v2.py](results/plot_experiment4_v2.py)`

Experiment 4

---



### Experiment 5 — Security Tier & mTLS Distribution (Extended Scale)

**Topology:** Extended | **Config:** `config_big.py`

Examines the distribution of assigned security tiers (Tier 0–3) and mTLS link activation across scenarios. Security-optimised placement activates mTLS on ~98% of eligible links.

**Plots:** `[results/experiment5b_tiers_mtls_v2.png](results/experiment5b_tiers_mtls_v2.png)`, `[results/experiment5b_spi_tiers_mtls_v3.png](results/experiment5b_spi_tiers_mtls_v3.png)`
**Scripts:** `[results/plot_experiment5b_v2.py](results/plot_experiment5b_v2.py)`, `[results/plot_experiment5b_spi_v3.py](results/plot_experiment5b_spi_v3.py)`

Experiment 5b — tiers & mTLSExperiment 5b — SPI variants

---



### Experiment 6 — Security Impact on Cost & Latency (Extended Scale)

**Topology:** Extended | **Config:** `config_big.py`

Quantifies the cost and latency penalty incurred by selecting higher security tiers and enabling mTLS, comparing latency-optimised vs security-optimised placements, and cost-optimised vs security-optimised placements, along with the balanced approach where all objectives contribute equally.

**Plot:** `[results/experiment6_security_impact_v2.png](results/experiment6_security_impact_v2.png)`
**Script:** `[results/plot_experiment6_v2.py](results/plot_experiment6_v2.py)`

Experiment 6

---



### Scalability & mTLS Sensitivity (Extended Scale)

**Topology:** Extended | **Config:** `config_big.py`

Rollout execution time vs infrastructure size, workload size, and chain depth; mTLS overhead sensitivity under the balanced objective.


| Plot                                                                                           | Script                                                                       |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `[scalability_infrastructure_v2.png](results/scalability_infrastructure_v2.png)`               | `[plot_scalability_v2.py](results/plot_scalability_v2.py)`                   |
| `[scalability_workload_v2.png](results/scalability_workload_v2.png)`                           | `[plot_scalability_v2.py](results/plot_scalability_v2.py)`                   |
| `[scalability_services_v2.png](results/scalability_services_v2.png)`                           | `[plot_scalability_services_v2.py](results/plot_scalability_services_v2.py)` |
| `[balanced_activation_latency_lines_v3.png](results/balanced_activation_latency_lines_v3.png)` | `[plot_balanced_mtls_v2.py](results/plot_balanced_mtls_v2.py)`               |


Scalability — infrastructuremTLS sensitivity

---



## How to Reproduce the Plots

```bash
cd results/
python plot_experiment1.py
python plot_experiment3_v2.py
python plot_experiment4_v2.py
python plot_experiment5b_v2.py
python plot_experiment5b_spi_v3.py
python plot_experiment6_v2.py
python plot_scalability_v2.py
python plot_scalability_services_v2.py
python plot_balanced_mtls_v2.py
```

> Requires: `matplotlib`, `numpy`

