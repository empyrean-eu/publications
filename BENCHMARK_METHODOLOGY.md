# Appendix — Benchmark Methodology to Calculate the Resource Overhead of the Examined Deployment Methods

This appendix documents the experimental methodology used to derive the **CPU, memory, and storage overhead multipliers** for each security deployment tier (Tier 0–3) that are used as parameters throughout the simulation experiments.

---

## Benchmark Workloads

Two representative workloads were used to characterise the resource overhead of each deployment approach:

| Workload | Application | Benchmark Tool |
|----------|-------------|---------------|
| Web-server | nginx | [hey](https://github.com/rakyll/hey) |
| Key-value store | redis | redis-benchmark |

---

## Hardware Nodes

Benchmarks were run on two nodes representing different infrastructure layers:

| Resource | x86 (Cloud) | aarch64 (Edge) |
|----------|------------|----------------|
| CPU | 12-core AMD Ryzen 5 2600 | 8-core Arm Cortex-A78AE v8.2 |
| Memory | 64 GB | 16 GB |
| Storage | 1 TB NVMe | 1 TB NVMe |

---

## Software Stack

All nodes run identical software:

- **Container runtime:** containerd v1.7 + nerdctl v1.0
- **Low-level runtimes (one per tier):**

| Tier | Technology | Runtime |
|------|-----------|---------|
| 0 | Bare container (no isolation) | `runc` |
| 1 | Software sandbox | `runsc` (gVisor) |
| 2 | Micro-VM | `kata-containers` (Firecracker) |
| 3 | Unikernel | `urunc` |

---

## Measurement Procedure

For each tier, a single container is spawned with the process **pinned to a single CPU core**. The benchmark tool runs from a **separate core** to avoid interference.

- **CPU throughput:** captured directly from benchmark tool output
- **Memory footprint:** measured as the **Resident Set Size (RSS)** — the portion of memory held in main memory — for *all* processes involved in the container execution (runtime, hypervisor, helper tools, etc.)
- **Storage:** measured for all components in the execution chain:
  - *Bare container (Tier 0):* container runtime binary + container image
  - *Sandboxed (Tier 1, gVisor):* runtime binary + container image
  - *Micro-VM (Tier 2, kata):* runtime binary + Firecracker hypervisor + microVM kernel + rootfs
  - *Unikernel (Tier 3, urunc):* unikernel binary + image

---

## Resource Multiplier Results

All values are normalised to **Tier 0 (bare container = 1.00×)**.

| Workload | Resource | Tier 0 | Tier 1 (sandbox) | Tier 2 (Micro-VM) | Tier 3 (Unikernel) |
|----------|----------|--------|-----------------|-------------------|-------------------|
| **Web-server** | CPU | 1.00 | 1.44 | 1.70 | 0.42 |
| | Memory | 1.00 | 1.07 | 1.66 | 0.66 |
| | Storage | 1.00 | 1.24 | 2.79 | 0.27 |
| **Key-value Store** | CPU | 1.00 | 1.72 | 2.03 | 0.91 |
| | Memory | 1.00 | 1.39 | 1.71 | 0.65 |
| | Storage | 1.00 | 1.22 | 2.64 | 0.21 |

