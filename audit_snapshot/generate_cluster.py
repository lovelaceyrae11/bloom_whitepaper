import os
import json
import datetime
import xml.etree.ElementTree as ET
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID

def generate_pki_cluster():
    print("[*] Initializing Cluster Root Certificate Authority (CA)...")
    ca_priv_key = ed25519.Ed25519PrivateKey.generate()
    ca_pub_key = ca_priv_key.public_key()
    
    ca_subject = ca_issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Castleberry Bloom Grid"),
        x509.NameAttribute(NameOID.COMMON_NAME, "CORE-127 Root CA"),
    ])
    
    ca_cert = x509.CertificateBuilder().subject_name(
        ca_subject
    ).issuer_name(
        ca_issuer
    ).public_key(
        ca_pub_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).sign(ca_priv_key, None)
    
    ca_cert_pem = ca_cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')

    root = ET.Element("Bloom", attrib={
        "cluster_id": "CORE-127",
        "geometry": "phi-hexagonal",
        "total_nodes": "127",
        "crypto_standard": "Ed25519-PKI",
        "root_ca_pem": ca_cert_pem.replace("\n", "\\n")
    })
    
    node_secrets = {}

    # Tier 1: Core Ring (19 nodes @ 528.0 Hz)
    core_tier = ET.SubElement(root, "Tier", attrib={"level": "core", "frequency": "528.0"})
    for i in range(1, 20):
        node_id = f"node-core-{i:03d}"
        node_priv = ed25519.Ed25519PrivateKey.generate()
        node_pub = node_priv.public_key()
        
        node_pub_hex = node_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()
        
        node_priv_hex = node_priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ).hex()
        
        node_secrets[node_id] = node_priv_hex
        
        node_subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, node_id),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Core-Tier"),
        ])
        node_cert = x509.CertificateBuilder().subject_name(
            node_subject
        ).issuer_name(
            ca_subject
        ).public_key(
            node_pub
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        ).sign(ca_priv_key, None)
        
        node_cert_pem = node_cert.public_bytes(serialization.Encoding.PEM).decode('utf-8').replace("\n", "\\n")
        
        ET.SubElement(core_tier, "Node", attrib={
            "node_id": node_id,
            "public_key": node_pub_hex,
            "ek_certificate": node_cert_pem,
            "role": "core-validator",
            "endpoint": f"127.0.0.1:{8000 + i}"
        })

    # Tier 2: Shell Ring (108 nodes @ 639.0 Hz)
    shell_tier = ET.SubElement(root, "Tier", attrib={"level": "shell", "frequency": "639.0"})
    for i in range(1, 109):
        node_id = f"node-shell-{i:03d}"
        node_priv = ed25519.Ed25519PrivateKey.generate()
        node_pub = node_priv.public_key()
        
        node_pub_hex = node_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()
        
        node_priv_hex = node_priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ).hex()
        
        node_secrets[node_id] = node_priv_hex
        
        node_subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, node_id),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Shell-Tier"),
        ])
        node_cert = x509.CertificateBuilder().subject_name(
            node_subject
        ).issuer_name(
            ca_subject
        ).public_key(
            node_pub
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        ).sign(ca_priv_key, None)
        
        node_cert_pem = node_cert.public_bytes(serialization.Encoding.PEM).decode('utf-8').replace("\n", "\\n")
        
        ET.SubElement(shell_tier, "Node", attrib={
            "node_id": node_id,
            "public_key": node_pub_hex,
            "ek_certificate": node_cert_pem,
            "role": "shell-edge",
            "endpoint": f"127.0.0.1:{9000 + i}"
        })

    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ", level=0)
    tree.write("cluster_extended.cml", encoding="utf-8", xml_declaration=True)
    
    with open("node_secrets.json", "w") as f:
        json.dump(node_secrets, f, indent=2)
        
    print(f"[*] Generated 127 PKI-backed nodes with Root CA certificates in 'cluster_extended.cml'.")

if __name__ == "__main__":
    generate_pki_cluster()
