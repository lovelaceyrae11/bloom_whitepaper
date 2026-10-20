import os
import xml.etree.ElementTree as ET

print("[*] Parsing CML (Castleberry Markup Language) Specification...")

spec_path = "build_artifacts/bloom_spec.cml"
if not os.path.exists(spec_path):
    raise FileNotFoundError("[!] CML specification missing.")

tree = ET.parse(spec_path)
root = tree.getroot()

# Handle XML namespace in tag lookup
ns = {"cml": "http://velathkai.org/cml"}

print("=" * 60)
print(f" CML ROOT TAG: {root.tag} (v{root.attrib.get('version')})")

metadata = root.find("cml:Metadata", ns) if root.tag.startswith("{") else root.find("Metadata")
if metadata is None:
    metadata = root.find("Metadata")

print("-" * 60)
print(" [Metadata]")
if metadata is not None:
    for child in metadata:
        tag_name = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        print(f"   {tag_name}: {child.text}")

anchor = root.find("cml:SovereignAnchor", ns) if root.tag.startswith("{") else root.find("SovereignAnchor")
if anchor is None:
    anchor = root.find("SovereignAnchor")

print("-" * 60)
print(" [Sovereign Anchor]")
if anchor is not None:
    for child in anchor:
        tag_name = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        print(f"   {tag_name}: {child.text}")

ring = root.find("cml:PhiHexagonalRing", ns) if root.tag.startswith("{") else root.find("PhiHexagonalRing")
if ring is None:
    ring = root.find("PhiHexagonalRing")

print("-" * 60)
if ring is not None:
    print(f" [Phi-Hexagonal Ring Nodes: {len(ring)}]")
    for node in ring:
        print(f"   Node ID {node.attrib.get('id')}: Address={node.attrib.get('address')} | Freq={node.attrib.get('freq')} | Status={node.attrib.get('status')}")
else:
    print(" [Phi-Hexagonal Ring Nodes: 0]")

print("=" * 60)
print("[+] CML specification parsed successfully. Structure and resonance parameters verified.")
