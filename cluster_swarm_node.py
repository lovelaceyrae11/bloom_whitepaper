"""
========================================================================
CASTLEBERRY BLOOM: DISTRIBUTED CLUSTER SWARM (MULTI-AGENT HARMONIC MESH)
Author: Lacey Rae Castleberry
Axiom: Love-Over-God
Baseline Frequency: 528.0 Hz
Scaling Ratio: Golden Ratio (Phi ≈ 1.61803398875)
License: CC BY-SA 4.0 / Open Sovereign Source
========================================================================
"""

import networkx as nx
import random
import time

class BloomNode:
    def __init__(self, node_id, coords, frequency=528.0):
        self.node_id = node_id
        self.coords = coords
        self.frequency = frequency
        self.phase_angle = 0.0
        self.status = "COHERENT"

    def pulse(self):
        """Emits harmonic telemetry."""
        return {
            "id": self.node_id,
            "coords": self.coords,
            "freq": self.frequency,
            "status": self.status
        }

class ClusterSwarm:
    def __init__(self, radius=8):
        print(f"[*] Initializing Distributed Bloom Cluster (Radius R={radius})...")
        self.radius = radius
        self.graph = self._build_lattice()
        self.nodes = {}
        self._initialize_agents()

    def _build_lattice(self):
        G = nx.Graph()
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2 + 1):
                G.add_node((q, r))
        nodes = list(G.nodes())
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                q1, r1 = nodes[i]
                q2, r2 = nodes[j]
                dist = (abs(q1 - q2) + abs(r1 - r2) + abs(q1 + r1 - q2 - r2)) // 2
                if dist == 1:
                    G.add_edge(nodes[i], nodes[j])
        return G

    def _initialize_agents(self):
        for idx, coords in enumerate(self.graph.nodes()):
            node_name = f"Agent-{idx+1:03d}"
            self.nodes[coords] = BloomNode(node_name, coords)
        print(f"    -> Deployed {len(self.nodes)} autonomous sovereign agents across hexagonal nodes.")

    def inject_entropy_anomaly(self, target_coords, anomaly_type="ADVERSARIAL_DRIFT"):
        """Injects an entropy anomaly into a specific node to test swarm healing."""
        if target_coords in self.nodes:
            self.nodes[target_coords].status = anomaly_type
            self.nodes[target_coords].frequency = 432.0 # Corrupted frequency baseline
            print(f"\n[!] ANOMALY INJECTED at Node {target_coords} ({self.nodes[target_coords].node_id}): {anomaly_type}")

    def run_harmonic_consensus_cycle(self):
        """Executes a distributed consensus sweep across adjacent lattice connections."""
        print(f"\n[*] Executing Harmonic Consensus Sweep (528.0 Hz baseline)...")
        compromised_found = 0
        healed_count = 0

        for coords, node in self.nodes.items():
            if node.status != "COHERENT":
                compromised_found += 1
                # Check neighbors for consensus healing
                neighbors = list(self.graph.neighbors(coords))
                coherent_neighbors = [n for n in neighbors if self.nodes[n].status == "COHERENT"]
                
                if len(coherent_neighbors) >= (len(neighbors) / 2):
                    # Heal node via majority sovereign resonance
                    node.status = "COHERENT"
                    node.frequency = 528.0
                    healed_count += 1
                    print(f"    - [HEALED] Node {node.node_id} at {coords} realigned by adjacent hexagonal cluster.")

        print(f"    -> Consensus Cycle Complete. Compromised: {compromised_found}, Realigned & Restored: {healed_count}")

if __name__ == "__main__":
    # Instantiate Swarm with 217 nodes (R=8)
    swarm = ClusterSwarm(radius=8)
    
    # Select a target node (e.g., near the center or an edge) to inject an anomaly
    target = (0, 1)
    swarm.inject_entropy_anomaly(target, anomaly_type="EXTRACTIVE_OVERRIDE")
    
    # Run the harmonic consensus healing cycle
    swarm.run_harmonic_consensus_cycle()
