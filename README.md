## Overview

**This repository contains the experimental artifacts, configuration files, and plotting scripts associated with the manuscript.**

- **Benchmark Methodology**: The methodology and benchmark results used to derive the simulation parameters for the CPU footprints of each security tier are detailed in `[BENCHMARK_METHODOLOGY.md](BENCHMARK_METHODOLOGY.md)`.

## Experimental Sections

The repository is organised into folders corresponding to the experimental sections in the manuscript:

- `[Full-trust experiments/](Full-trust%20experiments/)`: Contains the setup and results for sections 6.2.1. and 6.2.2. evaluating fully collaborative (full-trust) orchestrator associations.
- `[Limited-trust experiments/](Limited-trust%20experiments/)`: Contains the setup and results for the section 6.2.3. evaluating multi-tenant inter-cluster trust (limited-trust) associations.

**Note**: In the code, the notation for near-edge and far-edge is simply edge and fog, respectively.

### Reproducing the experimental setup and the results

Inside each of the experimental folders, you will find:

1. **Configuration Files**: The configuration parameters used for the infrastructure and algorithms.
2. **Setup Generator**: A generator script to reproduce the specific experimental setup (topology, workloads, and trust models).
3. **Results & Plotting**: The plotting scripts and the resulting figures exactly as they appear in the manuscript.

Please refer to the individual `README.md` file within each experiment folder for specific instructions on how to generate the setups and reproduce the plots.

### Setup summary statistics and visuals

Running `python generator.py` inside each folder's `generate_setup/` directory prints summary tables to the console and writes artifacts under `generate_setup/summary/`. 

#### Full-trust experiments

**Command** (from `Full-trust experiments/generate_setup/`):

```bash
python generator.py
```

**Markdown report** — `generate_setup/summary/setup_summary.md`:

- Header:  application count, service count
- **Infrastructure**: nodes by tier (near-edge / far-edge / cloud); machine totals, tier distribution, security-tier mix, CPU/cost ranges, machines-per-node stats
- **Workload**: services per app, unikernel-capable and heavy services, inter-service links and mTLS rate, payload sizes, mTLS CPU overhead
- **Sample applications** (first 8): app ID, chain length, mTLS links

**Figures**:


| File                         | Panels                                                                                                             |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `summary_infrastructure.png` | Nodes by tier · Machines by max security tier · Machines by infrastructure tier                                    |
| `summary_workload.png`       | Services per application · Service security tiers (min/max) · mTLS overhead vs payload · Payload size distribution |


#### Limited-trust experiments

**Command** (from `Limited-trust experiments/generate_setup/`):

```bash
python generator.py
```

**Markdown report** — `generate_setup/summary/setup_summary.md`:

- Header: cluster count, application count, service count, trust level used for the preview
- **Infrastructure**: nodes by tier; **nodes per cluster** (near-edge / far-edge / cloud breakdown); machine totals and stats (as above)
- **Workload**: aggregate stats (as above); **apps and services per cluster**
- **Sample applications** (first 8): app ID, origin cluster, chain length, mTLS links



**Figures**:


| File                         | Panels                                                                                                               |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `summary_infrastructure.png` | Nodes by tier · Machines by max security tier · Nodes per cluster (stacked by tier)                                  |
| `summary_workload.png`       | Services per application · Service security tiers (min/max) · mTLS overhead vs payload · Apps & services per cluster |
| `summary_trust_matrix.png`   | Binary trust matrix heatmap for the preview trust level                                                              |


> **Note:** Both generators use `setup_summary.py` and read from the respective `config/` files and `structs.py`. Modify those parameters and re-run the generator to produce an updated summary.

