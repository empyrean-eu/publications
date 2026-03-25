from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np

@dataclass
class Microservice:
    id: int
    app_id: int
    
    cpu_demand: float
    ram_demand: float
    storage_demand: float
    
    min_security: int
    max_security: int 
    
    typical_runtime: float  # ms on standard CPU
    
    data_size: float  # MB (Data output to next service)
    
    # CPU multiplier per security tier [0, 1, 2, 3]
    security_overheads: List[float] = field(default_factory=lambda: [1.0, 1.0, 1.0, 1.0])
    
    assigned_machine_id: int = -1
    assigned_node_id: int = -1
    assigned_tier: int = 0
    assigned_obj_cost: float = 0.0
    rflag: bool = False

@dataclass
class Application:
    id: int
    microservices: List[Microservice]
    
    gen_point: int  # Cluster ID (0..NUM_CLUSTERS-1) where request originates
    source_cluster: int = -1
    
    # index i corresponds to link MS[i] -> MS[i+1], length = len(microservices) - 1
    mtls_requirements: List[bool] = field(default_factory=list)
    mtls_decisions: List[bool] = field(default_factory=list)
    
    return_to_ue: bool = False  # If True, last service sends data back to UE

@dataclass
class Topology:
    num_nodes: int
    machines: np.ndarray 
    # Machine Matrix Columns:
    # 0: CPU, 1: RAM, 2: STORAGE, 3: COST, 4: SEC_LEVEL, 
    # 5: LOAD, 6: NODE_ID, 7: SPEED_COEFF, 8: INTRA_NODE_LAT, 9: INTRA_MACH_LAT
    
    node_categories: np.ndarray  # 1: Near-Edge, 2: Far-Edge, 3: Cloud
    node_clusters: np.ndarray    # Cluster ID (0..NUM_CLUSTERS-1) for each node
    
    node_to_user_latency: np.ndarray  # (NumNodes x NumClusters)
    network_latency: np.ndarray       # (NumNodes x NumNodes)
    
    trust_matrix: np.ndarray = None   # (NUM_CLUSTERS x NUM_CLUSTERS) binary trust matrix

    # Column Constants
    CPU_IDX = 0
    RAM_IDX = 1
    STR_IDX = 2
    COST_IDX = 3
    SEC_IDX = 4
    LOAD_IDX = 5
    NODE_IDX = 6
    SPEED_IDX = 7
    INODE_LAT_IDX = 8  # Intra-Node
    IMACH_LAT_IDX = 9  # Intra-Machine
