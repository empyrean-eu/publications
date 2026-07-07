# Limited-trust experiments

This folder contains all artifacts for the **experimental section 6.5**, which evaluates the impact of **inter-cluster trust** on microservice placement quality and security decisions in a multi-tenant 10-cluster environment.

---

## Setup


| Parameter    | Value                                                            |
| ------------ | ---------------------------------------------------------------- |
| Topology     | 90 nodes (60 near-edge + 20 far-edge + 10 cloud)                 |
| Clusters     | 10 orchestrator domains (each: 6 near-edge, 2 far-edge, 1 cloud) |
| Applications | 100 total (10 per cluster)                                       |


---

## Config File

`[config/config_collab.py](config/config_collab.py)` — a single configuration file that defines the full 10-cluster infrastructure and the set of trust levels evaluated in the plots (`0, 2, 4, 6, 10`).

---



## Experimental Setup Generator

You can generate and preview the experimental setup (topology, workload, and inter-cluster trust matrix) using the provided generator script.

```bash
python generator.py
```

> **Note:** The generator relies on `config/config_collab.py` and `structs.py` to define the parameters and class structures. You can modify these configuration files to define your custom parameters and then re-run the generator to produce your own experimental setup.

---



## Results



### Objectives vs Trust Level

**Plot:** `[results/plot_objectives_v3.png](results/plot_objectives_v3.png)`
**Script:** `[results/plot_objectives_v3.py](results/plot_objectives_v3.py)`

Rollout average normalised objective (per app) and failed-service rate across Isolated, Zero-Trust, Fed-2, Fed-4, Fed-6, and Full-Trust for Cost, Latency, Security, and Balanced scenarios.

Objectives

---



### Trust-Aware Placement Distribution

**Plot:** `[results/plot_placements_v2.png](results/plot_placements_v2.png)`
**Script:** `[results/plot_placements_v2.py](results/plot_placements_v2.py)`

Percentage of services placed in the origin cluster, trusted region, and untrusted region for each trust level and optimisation scenario.

Placements

---



## How to Reproduce the Plots

```bash
cd results/
python plot_objectives_v3.py
python plot_placements_v2.py
```

> Requires: `matplotlib`, `numpy`

---



## Key Findings

- **Full collaboration** consistently improves objective scores vs. isolated operation — the broader the resource pool, the more the optimizer can match service requirements to the best available tuples [machine, tier, mTLS].
- **Latency & Cost** see the largest gains from collaboration (more near-edge resources from trusted clusters become available).
- **Partial collaboration** (Fed-2 / Fed-4 / Fed-6) achieves most of the gains of full collaboration at a fraction of the coordination overhead.

