

## Overview

**This repository contains the experimental artifacts, configuration files, and plotting scripts associated with the manuscript.**

- **Benchmark Methodology**: The methodology and benchmark results used to derive the simulation parameters for the CPU footprints of each security tier are detailed in [`BENCHMARK_METHODOLOGY.md`](BENCHMARK_METHODOLOGY.md).

## Experimental Sections

The repository is organised into folders corresponding to the experimental sections in the manuscript:

- **[`Full-trust experiments/`](Full-trust%20experiments/)**: Contains the setup and results for sections 6.2.1. and 6.2.2. evaluating fully collaborative (full-trust) orchestrator associations.
- **[`Limited-trust experiments/`](Limited-trust%20experiments/)**: Contains the setup and results for the section 6.2.3. evaluating multi-tenant inter-cluster trust (limited-trust) associations.

**Note**: In the code, the notation for near-edge and far-edge is simply edge and fog, respectively.

### Reproducing the experimental setup and the results

Inside each of the experimental folders, you will find:

1. **Configuration Files**: The exact configuration parameters used for the infrastructure and algorithms.
2. **Setup Generator**: A generator script to reproduce the specific experimental setup (topology, workloads, and trust models).
3. **Results & Plotting**: The plotting scripts and the resulting figures exactly as they appear in the manuscript.

Please refer to the individual `README.md` file within each experiment folder for specific instructions on how to generate the setups and reproduce the plots.
