# Limited-trust experiments

This folder contains all artifacts for the **experimental section 6.2.3.**, which evaluates the impact of **inter-cluster trust** on microservice placement quality and security decisions in a multi-tenant 10-cluster environment.

---

## Setup

| Parameter | Value |
|-----------|-------|
| Topology | 90 nodes (60 near-edge + 20 far-edge + 10 cloud) |
| Clusters | 10 orchestrator domains (each: 6 near-edge, 2 far-edge, 1 cloud) |
| Applications | 100 total (10 per cluster) |

---


## Config File

[`config/config_collab.py`](config/config_collab.py) — a single configuration file that defines the full 10-cluster infrastructure and the set of trust levels to sweep over (`TRUST_LEVELS = [0, 3, 10]`).


---

## Experimental Setup Generator

You can generate and preview the experimental setup (topology, workload, and inter-cluster trust matrix) using the provided generator script.

```bash
python generator.py
```

> **Note:** The generator relies on `config/config_collab.py` and `structs.py` to define the parameters and class structures. You can modify these configuration files to define your custom parameters and then re-run the generator to produce your own experimental setup.

---

## How to Reproduce the Plots

```bash
cd results/
python plot_objectives.py       
python plot_placements.py       
python plot_tiers.py            
python plot_final_experiment.py 
```

> Requires: `matplotlib`, `numpy`

---

## Key Findings

- **Full collaboration** consistently improves objective scores vs. isolated operation — the broader the resource pool, the more the optimizer can match service requirements to the best available nodes.
- **Latency** sees the largest gains from collaboration (more near-edge resources from trusted clusters become available).
- **Security tier distribution** shifts toward higher tiers with increasing trust, as cross-cluster placements trigger stricter requirements.
- **Partial collaboration** (trust = 3) achieves most of the gains of full collaboration at a fraction of the coordination overhead.
