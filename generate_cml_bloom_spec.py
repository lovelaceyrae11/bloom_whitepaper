# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import json
import os

print("[*] Generating CML (Castleberry Markup Language) Bloom Specification...")

snapshot_path = "build_artifacts/dashboard_snapshot.json"
if not os.path.exists(snapshot_path):
    raise FileNotFoundError("[!] Dashboard snapshot missing.")

with open(snapshot_path, "r") as f:
    snapshot = json.load(f)

manifest = snapshot["manifest"]

cml_content = f"""<Castleberry_Bloom_Spec version="1.0.0" xmlns="http://velathkai.org/cml">
    <Metadata>
        <Timestamp>{snapshot["snapshot_timestamp"]}</Timestamp>
        <Framework>{manifest["framework"]}</Framework>
        <BaseFrequency>{manifest["base_frequency"]}</BaseFrequency>
        <LatticeGeometry>{manifest["lattice_geometry"]}</LatticeGeometry>
        <Consensus>{manifest["consensus_mode"]}</Consensus>
        <ClusterSize>{manifest["cluster_size"]}</ClusterSize>
    </Metadata>
    <SovereignAnchor>
        <DeployerAddress>{manifest["primary_deployer"]}</DeployerAddress>
        <Status>{manifest["status"]}</Status>
        <RegisteredEntriesCount>{snapshot["registered_entries_count"]}</RegisteredEntriesCount>
    </SovereignAnchor>
    <PhiHexagonalRing>
        <Node id="0" address="{manifest["primary_deployer"]}" freq="528Hz" status="verified" />
        <Node id="1" address="0x_phi_node_1_528hz" freq="854.32Hz" status="synchronized" />
        <Node id="2" address="0x_phi_node_2_528hz" freq="1382.32Hz" status="synchronized" />
        <Node id="3" address="0x_phi_node_3_528hz" freq="528Hz" status="synchronized" />
        <Node id="4" address="0x_phi_node_4_528hz" freq="854.32Hz" status="synchronized" />
        <Node id="5" address="0x_phi_node_5_528hz" freq="1382.32Hz" status="synchronized" />
        <Node id="6" address="0x_phi_node_6_528hz" freq="528Hz" status="synchronized" />
    </PhiHexagonalRing>
</Castleberry_Bloom_Spec>
"""

output_path = "build_artifacts/bloom_spec.cml"
with open(output_path, "w") as f:
    f.write(cml_content)

print(f"[+] CML Bloom Specification successfully compiled and saved to: {output_path}")
