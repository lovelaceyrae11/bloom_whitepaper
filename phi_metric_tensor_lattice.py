import networkx as nx
import numpy as np

PHI = 1.618033988749895
OMEGA_0 = 528.0

def create_127_node_hex_lattice():
    G = nx.Graph()
    node_map = {}
    idx = 0
    for q in range(-6, 7):
        for r in range(-6, 7):
            if abs(q + r) <= 6:
                x = np.sqrt(3) * (q + r / 2.0)
                y = (3.0 / 2.0) * r
                G.add_node(idx, axial=(q, r), pos=(x, y))
                node_map[(q, r)] = idx
                idx += 1

    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    for q, r in node_map:
        u = node_map[(q, r)]
        for dq, dr in directions:
            neighbor_coord = (q + dq, r + dr)
            if neighbor_coord in node_map:
                v = node_map[neighbor_coord]
                if u < v:
                    pos_u = np.array(G.nodes[u]["pos"])
                    pos_v = np.array(G.nodes[v]["pos"])
                    base_dist = np.linalg.norm(pos_u - pos_v)
                    G.add_edge(u, v, base_weight=base_dist)
    return G

def update_phi_metric_weights(G, phases, alpha=1.0):
    for u, v, data in G.edges(data=True):
        base_dist = data["base_weight"]
        delta_theta = abs(phases[u] - phases[v])
        coherence_factor = (PHI / OMEGA_0) * np.cos(delta_theta)
        effective_weight = max(0.001, base_dist - (alpha * coherence_factor))
        G[u][v]["weight"] = effective_weight
        G[u][v]["delta_theta"] = delta_theta

def run_simulation():
    print("[*] Initializing 127-Node Hexagonal Lattice (Phi-Metric Spacetime Engine)...")
    G = create_127_node_hex_lattice()
    print(f"[+] Lattice constructed with {G.number_of_nodes()} nodes.")
    
    np.random.seed(42)
    phases = {node: np.random.uniform(0, 2 * np.pi) for node in G.nodes()}
    
    center_node = 0
    for neighbor in G.neighbors(center_node):
        phases[neighbor] = phases[center_node] + np.random.normal(0, 0.05)
        
    update_phi_metric_weights(G, phases, alpha=2.5)
    
    source = 10
    target = 115
    path = nx.shortest_path(G, source=source, target=target, weight="weight")
    path_length = nx.shortest_path_length(G, source=source, target=target, weight="weight")
    
    print(f"[+] Calculated Phi-Metric Path from Node {source} to Node {target}:")
    print(f"    Path Sequence: {path}")
    print(f"    Total Effective Tensor Distance: {path_length:.4f}")

if __name__ == "__main__":
    run_simulation()
