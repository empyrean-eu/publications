# Multi-Tenancy Trust Region Experiment - Configuration

# --- Simulation Parameters ---
SEED = 42
# RUN_ILP = False
# RUN_ROLLOUT = True
# RUN_ROLLOUT_NODE_BASED = False
# RUN_ROLLOUT_NODE_PARALLEL = False
# RUN_FULL_ROLLOUT = False
# USE_CP_SAT = False
# ILP_MAX_CANDIDATES = 50

NUM_NEAR_EDGE = 60
NUM_FAR_EDGE = 20
NUM_CLOUD = 10
NUM_EDGE = NUM_NEAR_EDGE   # Alias for backward compat with heuristics.py
NUM_FOG = NUM_FAR_EDGE     # Alias for backward compat with heuristics.py
NUM_NODES = NUM_NEAR_EDGE + NUM_FAR_EDGE + NUM_CLOUD

# --- Cluster/Domain Constants ---
NUM_CLUSTERS = 10
INTRA_CLUSTER_LATENCY_FACTOR = 0.8

# --- Trust Configuration ---
# 0  = each cluster trusts only itself (isolated)
# 3  = each cluster trusts 3 additional clusters (partial collaboration)
# 10 = full trust (all clusters trust all others)
TRUST_LEVELS = [0, 3, 10]

# Machines per Node
MACHINES_EDGE = (1, 2)
MACHINES_FOG = (2, 4)
MACHINES_CLOUD = (5, 5)

SPEED_COEFF_EDGE = (0.5, 0.8)
SPEED_COEFF_FOG = (1.0, 1.2)
SPEED_COEFF_CLOUD = (1.4, 2.0)

# Machine Specifications (CPU, COST)
SPECS_EDGE_CPU = (2.0, 4.0)
SPECS_EDGE_COST = (3.0, 5.0)

SPECS_FOG_CPU = (2.0, 8.0)
SPECS_FOG_COST = (2.0, 3.0)

SPECS_CLOUD_CPU = (4.0, 16.0)
SPECS_CLOUD_COST = (1.0, 2.0)

# --- Latency Constants (ms) ---
INTRA_MACHINE_LATENCY = 2.0
INTRA_NODE_LATENCY = 5.0

# Network latencies (ms) ranges by tier pair
DELAY_EDGE_EDGE = (20.0, 40.0)
DELAY_EDGE_FOG = (60.0, 150.0)
DELAY_EDGE_CLOUD = (350.0, 500.0)
DELAY_FOG_FOG = (60.0, 150.0)
DELAY_FOG_CLOUD = (220.0, 350.0)
DELAY_CLOUD_CLOUD = (250.0, 400.0)

# User (Data Source) to Node Latencies
DELAY_USER_EDGE = (20.0, 40.0)
DELAY_USER_FOG = (100.0, 150.0)
DELAY_USER_CLOUD = (400.0, 500.0)

# --- Application Constants ---
NUM_APPS = 100           # 10 apps per cluster
MIN_SERVICES = 2
MAX_SERVICES = 10

# # --- Return Path ---
# RETURN_PATH_PROBABILITY = 0.25

# --- Service Generation Parameters ---
PROB_HEAVY_SERVICE = 0.25
RUNTIME_LIGHT = (5.0, 20.0)
RUNTIME_HEAVY = (100.0, 200.0)

DEMAND_CPU_LIGHT = (0.2, 1.0)
DEMAND_CPU_HEAVY = (1.0, 2.0)

# 3. Security Requirements
MIN_SEC = 0
MAX_SEC = 3

# 4. Data Size (MB)
DATA_SIZE = (0.5, 10.0)

# 5. mTLS
MTLS_PROBABILITY = 0.2
MTLS_CPU_OVERHEAD = 0.2
MTLS_LATENCY_FIXED = 5.0
MTLS_LATENCY_PER_MB = 10.0

# --- Resource Overheads (Security Tiers) ---
# Tiers: 0, 1, 2, 3
import numpy as np
OVERHEAD_CPU_BASE = np.array([1.0, 1.74, 1.36, 0.67])
# OVERHEAD_RAM = np.array([1.0, 1.23, 1.34, 0.66])
# OVERHEAD_STORAGE = np.array([1.0, 1.23, 2.71, 0.24])

# Cost Multipliers per Security Tier (multiplicative on base cost)
COST_MULT_EDGE = np.array([1.0, 1.1, 1.25, 1.5])
COST_MULT_FOG = np.array([1.0, 1.1, 1.25, 1.5])
COST_MULT_CLOUD = np.array([1.0, 1.1, 1.25, 1.5])

# Node Capability Distributions (Security Tier Probabilities 0-3)
PROB_EDGE = [0.40, 0.20, 0.20, 0.20]
PROB_FOG = [0.30, 0.20, 0.30, 0.20]
PROB_CLOUD = [0.20, 0.25, 0.25, 0.30]

# --- Normalization Bounds (Estimated) ---
# Used for Max-Min Normalization [0, 1]
MAX_NORM_COST = 5000.0
MIN_NORM_COST = 10.0
MAX_NORM_LATENCY = 2000.0
MIN_NORM_LATENCY = 5.0
MAX_NORM_SEC = 40.0
MIN_NORM_SEC = 1.0

# --- Weights ---
# w1*NormCost + w2*NormSec + w3*NormLat
W1 = 0.35  # Cost
W2 = 0.2   # Security
W3 = 0.45  # Latency

# # --- Heuristics ---
# MAX_WORKERS = 16
# ROLLOUT_WINDOW_SIZE = 10
# ROLLOUT_DISCOUNT = 0.95
# FULL_ROLLOUT_TOP_K = 50
