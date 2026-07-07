import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config_collab as cfg
from structs import Topology, Application, Microservice, dataclass
import random


def _mtls_cpu_bounds():
    ov = cfg.MTLS_CPU_OVERHEAD
    if isinstance(ov, (list, tuple)):
        return float(ov[0]), float(ov[1])
    return float(ov), float(ov)


def compute_mtls_cpu_overhead(incoming_data_mb: float) -> float:
    """
    Map incoming inter-service payload size to mTLS sidecar CPU demand.
    Linear in [DATA_SIZE] -> [MTLS_CPU_OVERHEAD] (default 0.1–5 MB -> 0.05–0.4 cores).
    """
    cpu_lo, cpu_hi = _mtls_cpu_bounds()
    data_lo, data_hi = cfg.DATA_SIZE
    if data_hi <= data_lo:
        return round(cpu_lo, 3)
    t = (incoming_data_mb - data_lo) / (data_hi - data_lo)
    t = max(0.0, min(1.0, t))
    return round(cpu_lo + t * (cpu_hi - cpu_lo), 3)


def _trust_clique(trust: np.ndarray, members: list) -> None:
    for a in members:
        for b in members:
            trust[a, b] = 1


def generate_trust_matrix(num_clusters: int, trust_level: int) -> np.ndarray:
    """
    Generate a symmetric binary trust matrix from sequential federation blocks.

    - trust_level=0: each cluster trusts only itself.
    - trust_level=k: partition clusters into federations of size k+1 (full cliques).
      A partial leftover block (2..k clusters) also forms a clique.
      A single leftover cluster trusts k random other clusters (symmetric, seeded).
    - trust_level>=num_clusters-1: full trust (all 1s).
    """
    trust = np.eye(num_clusters, dtype=int)

    if trust_level == 0:
        return trust
    if trust_level >= num_clusters - 1:
        return np.ones((num_clusters, num_clusters), dtype=int)

    block_size = trust_level + 1
    i = 0
    while i < num_clusters:
        remaining = num_clusters - i
        if remaining >= block_size:
            _trust_clique(trust, list(range(i, i + block_size)))
            i += block_size
        elif remaining == 1:
            orphan = i
            others = [c for c in range(num_clusters) if c != orphan]
            peers = random.sample(others, min(trust_level, len(others)))
            for p in peers:
                trust[orphan, p] = trust[p, orphan] = 1
            i += 1
        else:
            _trust_clique(trust, list(range(i, num_clusters)))
            i = num_clusters

    return trust


def segment_nodes_into_clusters(num_nodes: int, num_clusters: int, categories: np.ndarray = None) -> np.ndarray:
    """
    Segments nodes into clusters with STRATIFIED assignment:
    each cluster gets an equal share of Near-Edge, Far-Edge, and Cloud nodes.
    This ensures every cluster has a representative mix of all tiers.
    """
    if num_clusters > num_nodes:
        raise ValueError("Cannot have more clusters than nodes")
        
    clusters = np.zeros(num_nodes, dtype=int)
    
    if categories is not None:
        for cat in [1, 2, 3]:
            cat_indices = np.where(categories == cat)[0]
            np.random.shuffle(cat_indices)
            for rank, node_idx in enumerate(cat_indices):
                clusters[node_idx] = rank % num_clusters
    else:
        node_indices = np.arange(num_nodes)
        np.random.shuffle(node_indices)
        for i in range(num_clusters):
            clusters[node_indices[i]] = i
        for i in range(num_clusters, num_nodes):
            clusters[node_indices[i]] = np.random.randint(0, num_clusters)
        
    return clusters


def generate_topology(trust_level: int = 0) -> Topology:
    cat_near_edge = np.full(cfg.NUM_NEAR_EDGE, 1)
    cat_far_edge = np.full(cfg.NUM_FAR_EDGE, 2)
    cat_cloud = np.full(cfg.NUM_CLOUD, 3)
    categories = np.concatenate([cat_near_edge, cat_far_edge, cat_cloud])
    
    num_nodes = len(categories)
        
    node_clusters = segment_nodes_into_clusters(num_nodes, cfg.NUM_CLUSTERS, categories)
    
    trust_matrix = generate_trust_matrix(cfg.NUM_CLUSTERS, trust_level)
    
    print(f"\n[Trust Level {trust_level}] Trust matrix generated ({cfg.NUM_CLUSTERS}x{cfg.NUM_CLUSTERS})")
    for c in range(cfg.NUM_CLUSTERS):
        trusted = [j for j in range(cfg.NUM_CLUSTERS) if trust_matrix[c, j] == 1 and j != c]
        ne_count = np.sum((node_clusters == c) & (categories == 1))
        fe_count = np.sum((node_clusters == c) & (categories == 2))
        cl_count = np.sum((node_clusters == c) & (categories == 3))
        print(f"  Cluster {c}: {ne_count}NE + {fe_count}FE + {cl_count}C nodes | trusts: {trusted if trusted else 'self only'}")
        
    lat_matrix = np.zeros((num_nodes, num_nodes))
    
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            cat_i = categories[i]
            cat_j = categories[j]
            
            pair = tuple(sorted((cat_i, cat_j)))
            
            latency = 0.0
            
            if pair == (1, 1):
                latency = round(np.random.uniform(*cfg.DELAY_EDGE_EDGE), 2)
            elif pair == (1, 2):
                latency = round(np.random.uniform(*cfg.DELAY_EDGE_FOG), 2)
            elif pair == (1, 3):
                latency = round(np.random.uniform(*cfg.DELAY_EDGE_CLOUD), 2)
            elif pair == (2, 2):
                latency = round(np.random.uniform(*cfg.DELAY_FOG_FOG), 2)
            elif pair == (2, 3):
                latency = round(np.random.uniform(*cfg.DELAY_FOG_CLOUD), 2)
            elif pair == (3, 3):
                 latency = round(np.random.uniform(*cfg.DELAY_CLOUD_CLOUD), 2)
            
            if node_clusters[i] == node_clusters[j]:
                latency *= cfg.INTRA_CLUSTER_LATENCY_FACTOR
                latency = round(latency, 2)
            
            lat_matrix[i, j] = latency
            lat_matrix[j, i] = latency

    user_lat = np.zeros((num_nodes, cfg.NUM_CLUSTERS))
    
    base_access_delays = np.zeros(num_nodes)
    for n in range(num_nodes):
        cat = categories[n]
        if cat == 1:
            base_access_delays[n] = round(np.random.uniform(*cfg.DELAY_USER_EDGE), 2)
        elif cat == 2:
            base_access_delays[n] = round(np.random.uniform(*cfg.DELAY_USER_FOG), 2)
        else:
            base_access_delays[n] = round(np.random.uniform(*cfg.DELAY_USER_CLOUD), 2)
            
    for n in range(num_nodes):
        for c in range(cfg.NUM_CLUSTERS):
            base = base_access_delays[n]
            
            if node_clusters[n] == c:
                val = base * cfg.INTRA_CLUSTER_LATENCY_FACTOR
            else:
                val = base
                
            user_lat[n, c] = round(val, 2)
    
    machines_list = []
    machine_rows = []
    
    for n_id in range(num_nodes):
        cat = categories[n_id]
        
        if cat == 1:
            num_mach = np.random.randint(cfg.MACHINES_EDGE[0], cfg.MACHINES_EDGE[1] + 1)
            base_cpu = cfg.SPECS_EDGE_CPU
            base_cost = cfg.SPECS_EDGE_COST
            security_prob = cfg.PROB_EDGE
            
        elif cat == 2:
            num_mach = np.random.randint(cfg.MACHINES_FOG[0], cfg.MACHINES_FOG[1] + 1)
            base_cpu = cfg.SPECS_FOG_CPU
            base_cost = cfg.SPECS_FOG_COST
            security_prob = cfg.PROB_FOG
            
        else:
            num_mach = np.random.randint(cfg.MACHINES_CLOUD[0], cfg.MACHINES_CLOUD[1] + 1)
            base_cpu = cfg.SPECS_CLOUD_CPU
            base_cost = cfg.SPECS_CLOUD_COST
            security_prob = cfg.PROB_CLOUD
        
        for _ in range(num_mach):
            if cat == 1: sp_rng = cfg.SPEED_COEFF_EDGE
            elif cat == 2: sp_rng = cfg.SPEED_COEFF_FOG
            else: sp_rng = cfg.SPEED_COEFF_CLOUD
            
            mach_speed = round(np.random.uniform(*sp_rng), 2)
            
            s_min, s_max = sp_rng
            if s_max > s_min:
                norm_speed = (mach_speed - s_min) / (s_max - s_min)
            else:
                norm_speed = 0.5
                
            c_min, c_max = base_cost
            base_c = c_min + (norm_speed * (c_max - c_min))
            
            dist_factor = np.random.uniform(0.9, 1.1)
            cost = round(base_c * dist_factor, 2)
            
            cpu = round(np.random.uniform(*base_cpu), 2)
            
            sec = np.random.choice([0, 1, 2, 3], p=security_prob)

            # [CPU, RAM, STO, COST, SEC, LOAD, NODE_ID, SPEED, INTRA_NODE, INTRA_MACH]
            machine_rows.append([cpu, 999999.0, 999999.0, cost, sec, 0, n_id, mach_speed, cfg.INTRA_NODE_LATENCY, cfg.INTRA_MACHINE_LATENCY])
            
    machines = np.array(machine_rows)

    print(f"[Topology] All {len(machines)} machines available across {cfg.NUM_CLUSTERS} clusters")

    return Topology(
        num_nodes=num_nodes,
        machines=machines,
        network_latency=lat_matrix,
        node_to_user_latency=user_lat,
        node_categories=categories,
        node_clusters=node_clusters,
        trust_matrix=trust_matrix
    )


def generate_workload(num_apps=cfg.NUM_APPS) -> list[Application]:
    """
    Generate workload with apps evenly distributed across clusters.
    """
    apps = []
    ms_counter = 0
    
    apps_per_cluster = num_apps // cfg.NUM_CLUSTERS
    
    for i in range(num_apps):
        num_ms = np.random.randint(cfg.MIN_SERVICES, cfg.MAX_SERVICES + 1)
        services = []
        
        for _ in range(num_ms):
            has_specialized_image = (np.random.random() < cfg.PROB_UNIKERNEL_IMAGE)
            limit_max = 3 if has_specialized_image else 2
            
            min_sec = np.random.choice([0, 1, 2, 3], p=[0.60, 0.15, 0.15, 0.10])
            
            if min_sec > limit_max:
                min_sec = limit_max
                
            max_sec = limit_max
            
            is_heavy = (np.random.random() < cfg.PROB_HEAVY_SERVICE)
            if _ == 0 and num_ms > 1: 
                is_heavy = False
                
            if is_heavy:
                runtime = round(np.random.uniform(*cfg.RUNTIME_HEAVY), 2)
                cpu = round(np.random.uniform(*cfg.DEMAND_CPU_HEAVY), 2)
            else:
                runtime = round(np.random.uniform(*cfg.RUNTIME_LIGHT), 2)
                cpu = round(np.random.uniform(*cfg.DEMAND_CPU_LIGHT), 2)
            
            d_size = round(np.random.uniform(*cfg.DATA_SIZE), 2)
            
            sec_ov = [1.0] * 4
            for t in range(1, 4):
                 base = cfg.OVERHEAD_CPU_BASE[t]
                 low = base * 0.8
                 high = base * 1.2
                 val = np.random.uniform(low, high)
                 sec_ov[t] = round(val, 3)
            
            ms = Microservice(
                id=ms_counter,
                app_id=i,
                cpu_demand=cpu,
                ram_demand=0.0,
                storage_demand=0.0,
                min_security=min_sec,
                max_security=max_sec,
                typical_runtime=runtime,
                data_size=d_size,
                security_overheads=sec_ov
            )
            services.append(ms)
            ms_counter += 1
            
        mtls_reqs = []
        mtls_ovs = []
        for link_idx in range(num_ms - 1):
            req = (np.random.random() < cfg.MTLS_PROBABILITY)
            mtls_reqs.append(req)
            incoming_mb = services[link_idx].data_size
            mtls_ovs.append(compute_mtls_cpu_overhead(incoming_mb))
            
        return_path = (np.random.random() < cfg.RETURN_PATH_PROBABILITY)

        source_cluster = i // apps_per_cluster
        if source_cluster >= cfg.NUM_CLUSTERS:
            source_cluster = cfg.NUM_CLUSTERS - 1
        
        app = Application(
            id=i,
            microservices=services,
            mtls_requirements=mtls_reqs,
            mtls_decisions=mtls_reqs.copy(),
            mtls_overheads=mtls_ovs,
            gen_point=source_cluster,
            source_cluster=source_cluster,
            return_to_ue=return_path
        )
        apps.append(app)
    
    cluster_counts = {}
    for a in apps:
        cluster_counts[a.source_cluster] = cluster_counts.get(a.source_cluster, 0) + 1
    print(f"Generated {len(apps)} apps with total {ms_counter} services (Avg {ms_counter/len(apps):.2f})")
    print(f"  Apps per cluster: {dict(sorted(cluster_counts.items()))}")
    return apps

if __name__ == "__main__":
    import time
    from setup_summary import emit_setup_summary

    np.random.seed(cfg.SEED)
    random.seed(cfg.SEED)

    print("=== Creating Experimental Setup (Limited-trust) ===")
    print("1. Generating Infrastructure Topology & Trust Matrix...")
    trust_level = 3
    topo = generate_topology(trust_level=trust_level)
    print(f"   -> Topology generated: {topo.num_nodes} nodes, {len(topo.machines)} total machines.")
    print(f"   -> Distribution: {len(np.where(topo.node_categories == 1)[0])} Near-Edge, "
          f"{len(np.where(topo.node_categories == 2)[0])} Far-Edge, "
          f"{len(np.where(topo.node_categories == 3)[0])} Cloud nodes.")

    print("\n2. Generating Microservice Workload...")
    start_time = time.time()
    apps = generate_workload()
    elapsed = time.time() - start_time
    print(f"   -> Workload generated in {elapsed:.4f}s")

    print("\n3. Setup summary (tables + plots)...")
    emit_setup_summary(topo, apps, cfg, trust_level=trust_level)
    print("\n=== Experimental Setup Ready ===")
