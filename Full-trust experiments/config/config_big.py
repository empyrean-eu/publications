# Simulation Configuration V2

# --- Simulation Parameters ---
SEED = 42
# RUN_ILP = False
# RUN_ROLLOUT = True # Toggle Rollout execution
# RUN_ROLLOUT_NODE_BASED = False # Toggle simplified Node-Based Rollout
# RUN_ROLLOUT_NODE_PARALLEL = False # Toggle parallel Node-Based Rollout
# RUN_FULL_ROLLOUT = False # Toggle Full Lookahead Rollout (inter-app, parallel)
# USE_CP_SAT = False # Use Google OR-Tools CP-SAT (ILP2) instead of PuLP (ILP)
# ILP_MAX_CANDIDATES = 50


# Specific Topology: 60 Edge, 20 Fog, 10 Cloud
NUM_EDGE = 60
NUM_FOG = 20
NUM_CLOUD = 10
NUM_NODES = NUM_EDGE + NUM_FOG + NUM_CLOUD

# --- Cluster/Domain Constants ---
NUM_CLUSTERS = 4
INTRA_CLUSTER_LATENCY_FACTOR = 0.8 # Latency discount for intra-cluster communication

# Machines per Node (Range inclusive)
MACHINES_EDGE = (1, 2)
MACHINES_FOG = (2, 4)
MACHINES_CLOUD = (5, 5)


# Exec Time = Typical Runtime / Speed Coefficient

SPEED_COEFF_EDGE = (0.5, 0.8)
SPEED_COEFF_FOG = (1.0, 1.2)
SPEED_COEFF_CLOUD = (1.4, 2.0)

# Machine Specifications (CPU, COST)

SPECS_EDGE_CPU = (2.0, 4.0)

SPECS_EDGE_COST = (3.0, 5.0)

# Fog (Mid)
SPECS_FOG_CPU = (2.0, 8.0)

SPECS_FOG_COST = (2.0, 3.0)

# Cloud (Economy of Scale)
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
NUM_APPS = 60
MIN_SERVICES = 2
MAX_SERVICES = 10

# # --- Return Path ---
# RETURN_PATH_PROBABILITY = 0.25

# --- Service Generation Parameters ---

# 1. Runtime (ms)

PROB_HEAVY_SERVICE = 0.25
RUNTIME_LIGHT = (5.0, 20.0)
RUNTIME_HEAVY = (100.0, 200.0)

# 2. Resource Demands (CPU)
# Light Services
DEMAND_CPU_LIGHT = (0.2, 1.0)


# Heavy Services
DEMAND_CPU_HEAVY = (1.0, 2.0)


# 3. Security Requirements
MIN_SEC = 0
MAX_SEC = 3

# 4. Data Size (MB)
DATA_SIZE = (0.5, 10.0)

# 5. mTLS
MTLS_PROBABILITY = 0.3
MTLS_CPU_OVERHEAD = 0.2

# mTLS Latency = Base + (Per_MB * Data_Size_MB)
MTLS_LATENCY_FIXED = 5.0    # Base latency 
MTLS_LATENCY_PER_MB = 10.0   # Encryption/Processing delay per MB



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
# We utilize these to normalize objective terms before weighting
MAX_NORM_COST = 5000.0  # Safe upper bound for new high cost edge model
MIN_NORM_COST = 10.0   # Est Min Cost

MAX_NORM_LATENCY = 2000.0 # Est Max Total End-to-End Chain Latency
MIN_NORM_LATENCY = 5.0

MAX_NORM_SEC = 40.0 # Theoretical Max: 10 svc * 3 tier + 9 links * 1 mTLS = 39
MIN_NORM_SEC = 1.0

# --- Weights ---
# w1*NormCost + w2*NormSec + w3*NormLat
W1 = 0.3 # Cost
W2 = 0.2# Security
W3 = 0.4 # Latency

# # --- Heuristics ---
# MAX_WORKERS = 16 # Auto-detect in main recommended, or hardcode
# ROLLOUT_WINDOW_SIZE = 10 # Number of future apps to consider in windowed lookahead
# ROLLOUT_DISCOUNT = 0.95 # Discount factor for future app scores (0=ignore future, 1=full weight)
# FULL_ROLLOUT_TOP_K = 50 # Number of top machines to evaluate per service in Full Rollout
