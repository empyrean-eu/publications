# Experimental Setup Summary

**Seed:** 42  |  **Applications:** 100  |  **Services:** 613

## Infrastructure — Nodes by Tier

|    Tier   | Nodes | Share |
|-----------|-------|-------|
| Near-Edge |   60  | 66.7% |
|  Far-Edge |   20  | 22.2% |
|   Cloud   |   10  | 11.1% |

## Infrastructure — Machines

- **Total machines:** 247
- **Per tier:** Near-Edge: 90 (36.4%), Far-Edge: 57 (23.1%), Cloud: 100 (40.5%)
- **Security tier on machines:** Tier 0: 91 (36.8%), Tier 1: 53 (21.5%), Tier 2: 47 (19.0%), Tier 3: 56 (22.7%)
- **CPU capacity (cores):** min=1.04, mean=9.79, max=31.48
- **Cost rate:** min=0.92, mean=2.62, max=5.24
- **Machines per node:** min=1, max=10, mean=2.74

## Workload — Aggregate

- **Services per app:** min=2, max=10, mean=6.13
- **Unikernel-capable services:** 121 (19.7%)
- **Heavy services (CPU >= 1.0):** 98 (16.0%)
- **Inter-service links:** 513  |  **mTLS required:** 109 (21.2%)
- **Payload size (MB):** min=0.10, mean=2.57, max=4.98
- **mTLS CPU overhead (cores):** min=0.050, mean=0.227, max=0.399

## Sample Applications (first 8)

| App ID | Chain Len | mTLS Links |
|--------|-----------|------------|
|   0    |     9     |     0      |
|   1    |     5     |     1      |
|   2    |     8     |     2      |
|   3    |     10    |     1      |
|   4    |     2     |     0      |
|   5    |     3     |     1      |
|   6    |     9     |     1      |
|   7    |     5     |     0      |