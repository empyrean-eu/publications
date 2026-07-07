# Experimental Setup Summary

**Seed:** 42  |  **Clusters:** 10  |  **Applications:** 100  |  **Services:** 634  |  **Trust level:** 3

## Infrastructure — Nodes by Tier

|    Tier   | Nodes | Share |
|-----------|-------|-------|
| Near-Edge |   60  | 66.7% |
|  Far-Edge |   20  | 22.2% |
|   Cloud   |   10  | 11.1% |

## Infrastructure — Nodes per Cluster

| Cluster | Near-Edge | Far-Edge | Cloud | Total |
|---------|-----------|----------|-------|-------|
|    0    |     6     |    2     |   1   |   9   |
|    1    |     6     |    2     |   1   |   9   |
|    2    |     6     |    2     |   1   |   9   |
|    3    |     6     |    2     |   1   |   9   |
|    4    |     6     |    2     |   1   |   9   |
|    5    |     6     |    2     |   1   |   9   |
|    6    |     6     |    2     |   1   |   9   |
|    7    |     6     |    2     |   1   |   9   |
|    8    |     6     |    2     |   1   |   9   |
|    9    |     6     |    2     |   1   |   9   |

## Infrastructure — Machines

- **Total machines:** 255
- **Per tier:** Near-Edge: 93 (36.5%), Far-Edge: 62 (24.3%), Cloud: 100 (39.2%)
- **Security tier on machines:** Tier 0: 78 (30.6%), Tier 1: 69 (27.1%), Tier 2: 52 (20.4%), Tier 3: 56 (22.0%)
- **CPU capacity (cores):** min=2.03, mean=6.05, max=15.92
- **Cost rate:** min=0.95, mean=2.62, max=5.20
- **Machines per node:** min=1, max=10, mean=2.83

## Workload — Aggregate

- **Services per app:** min=2, max=10, mean=6.34
- **Unikernel-capable services:** 134 (21.1%)
- **Heavy services (CPU >= 1.0):** 115 (18.1%)
- **Inter-service links:** 534  |  **mTLS required:** 129 (24.2%)
- **Payload size (MB):** min=0.10, mean=2.42, max=4.99
- **mTLS CPU overhead (cores):** min=0.050, mean=0.217, max=0.399

## Workload — Apps per Cluster

| Cluster | Apps | Services |
|---------|------|----------|
|    0    |  10  |    61    |
|    1    |  10  |    67    |
|    2    |  10  |    46    |
|    3    |  10  |    59    |
|    4    |  10  |    77    |
|    5    |  10  |    64    |
|    6    |  10  |    71    |
|    7    |  10  |    68    |
|    8    |  10  |    62    |
|    9    |  10  |    59    |

## Sample Applications (first 8)

| App ID | Origin Cluster | Chain Len | mTLS Links |
|--------|----------------|-----------|------------|
|   0    |       0        |     2     |     0      |
|   1    |       0        |     10    |     3      |
|   2    |       0        |     2     |     1      |
|   3    |       0        |     3     |     0      |
|   4    |       0        |     7     |     0      |
|   5    |       0        |     7     |     3      |
|   6    |       0        |     6     |     0      |
|   7    |       0        |     9     |     3      |