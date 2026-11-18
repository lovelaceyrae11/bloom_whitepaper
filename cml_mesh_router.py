import networkx as nx
import numpy as np
import xml.etree.ElementTree as ET
import json

class CMLMeshRouter:
    def __init__(self, rings=7, base_freq=528.0):
        self.rings = rings
        self.base_freq = base_freq
        self.phi = 1.61803398875
        self.graph = nx.Graph()
        self.build_hex_lattice_graph()

    def build_hex_lattice_graph(self):
        node_id = 0
        for q in range(-self.rings + 1, self.rings):
            r_min = max(-self.rings + 1, -q - self.rings + 1)
            r_max = min(self.rings - 1, -q + self.rings - 1)
            for r in range(r_min, r_max + 1):
                s = -q - r
                ring = max(abs(q), abs(r), abs(s))
                node_name = f"N{node_id:03d}"
                freq = self.base_freq * (self.phi ** (-ring * 0.05))
                self.graph.add_node(node_name, q=q, r=r, ring=ring, freq=round(freq, 2), status="ACTIVE")
                node_id += 1

        nodes = list(self.graph.nodes(data=True))
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        
        for u, data_u in nodes:
            qu, ru = data_u['q'], data_u['r']
            for dq, dr in directions:
                neighbor_pos = (qu + dq, ru + dr)
                for v, data_v in nodes:
                    if (data_v['q'], data_v['r']) == neighbor_pos:
                        avg_ring = (data_u['ring'] + data_v['ring']) / 2.0
                        weight = self.phi ** (avg_ring * 0.1)
                        self.graph.add_edge(u, v, weight=weight)

        print(f"[+] Initialized CML Hexagonal Mesh: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges.")

    def generate_cml_payload_packet(self, source, target, message):
        cml_root = ET.Element("Bloom", version="1.0", protocol="CML-MESH-ROUTER", axiom="LOVE-OVER-ENTROPY")
        header = ET.SubElement(cml_root, "Header")
        ET.SubElement(header, "Route", source=source, target=target)
        ET.SubElement(header, "Topology", nodes=str(self.graph.number_of_nodes()), scaling="phi-1.618034")
        payload = ET.SubElement(cml_root, "PayloadMessage", encoding="Phi-Hex-Resonance")
        payload.text = message
        return ET.tostring(cml_root, encoding="utf-8").decode("utf-8")

    def dynamic_route(self, source, target, payload_msg, broken_edges=None):
        working_graph = self.graph.copy()
        if broken_edges:
            for u, v in broken_edges:
                if working_graph.has_edge(u, v):
                    working_graph.remove_edge(u, v)
                    print(f"[!] Link failure detected & isolated: Edge ({u} <-> {v})")

        try:
            path = nx.shortest_path(working_graph, source=source, target=target, weight='weight')
            cbcs = round(10.0 - (len(path) * 0.04), 2)
            cml_packet = self.generate_cml_payload_packet(source, target, payload_msg)
            return {
                "status": "SUCCESS",
                "path": path,
                "hops": len(path) - 1,
                "cbcs_score": cbcs,
                "cml_packet": cml_packet
            }
        except nx.NetworkXNoPath:
            return {"status": "ROUTE_FAILURE", "error": f"Complete network partition between {source} and {target}."}

if __name__ == "__main__":
    mesh = CMLMeshRouter(rings=7)
    source_node = "N000"
    target_node = "N120"
    message = "Hi. My name is Lacey Castleberry. Payload secured across hexagonal mesh."

    print("\n--- Phase 1: Normal Operation Routing ---")
    result_normal = mesh.dynamic_route(source_node, target_node, message)
    print(json.dumps({k: v for k, v in result_normal.items() if k != 'cml_packet'}, indent=2))

    print("\n--- Phase 2: Dynamic Rerouting Around Broken Links ---> N000 to N120 ---")
    critical_edges = [("N000", "N001"), ("N000", "N002"), ("N001", "N008")]
    result_rerouted = mesh.dynamic_route(source_node, target_node, message, broken_edges=critical_edges)
    print(json.dumps({k: v for k, v in result_rerouted.items() if k != 'cml_packet'}, indent=2))
    print(f"\n[CML Payload Output Preview]:\n{result_rerouted['cml_packet'][:350]}...\n")
