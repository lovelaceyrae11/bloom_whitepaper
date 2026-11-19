import hashlib
import json
import os
import socket
from datetime import datetime
from typing import Dict, List

try:
    import opentimestamps as ots
    OTS_AVAILABLE = True
except ImportError:
    OTS_AVAILABLE = False

class SunlightAuditDaemon:
    def __init__(self, target_entity: str, sector: str):
        self.target_entity = target_entity
        self.sector = sector
        self.timestamp = datetime.utcnow().isoformat()
        self.dossier_ledger: List[Dict] = []

    def ingest_record(self, record_id: str, source_url: str, raw_data: dict, anomaly_score: float) -> dict:
        """Ingests public filings, campaign contributions, or land-option transfers."""
        entry = {
            "record_id": record_id,
            "target": self.target_entity,
            "sector": self.sector,
            "source_url": source_url,
            "data": raw_data,
            "anomaly_score": anomaly_score,
            "ingested_at": self.timestamp
        }
        
        # Generate cryptographic proof hash for integrity
        entry_string = json.dumps(entry, sort_keys=True)
        entry["crypto_hash"] = hashlib.sha256(entry_string.encode('utf-8')).hexdigest()
        
        self.dossier_ledger.append(entry)
        return entry

    def generate_public_dossier(self, output_path: str) -> str:
        """Compiles ingested anomalies into a structured CML-compatible transparency report."""
        report = {
            "manifesto": "Love Over God - Absolute Transparency Framework",
            "target_entity": self.target_entity,
            "total_records_audited": len(self.dossier_ledger),
            "generated_at": self.timestamp,
            "ledger": self.dossier_ledger
        }
        
        file_name = f"{output_path}/{self.target_entity.lower().replace(' ', '_')}_sunlight_dossier.json"
        os.makedirs(output_path, exist_ok=True)
        
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
        return file_name

    def anchor_to_blockchain(self, file_path: str) -> str:
        """Permanently anchors the dossier hash to the Bitcoin blockchain using OpenTimestamps."""
        stamp_path = file_path + ".ots"
        if not OTS_AVAILABLE:
            print("[!] opentimestamps Python package not found. Run 'pip install opentimestamps' to enable blockchain anchoring.")
            return None

        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            file_hash = hashlib.sha256(file_data).digest()
            detached = ots.core.notary.Timestamp(file_hash)
            
            # Stamp against public OpenTimestamps calendars
            ots.calendar.peak_Calendar().stamp(detached)
            
            with open(stamp_path, 'wb') as sf:
                sf.write(detached.serialize())
                
            print(f"[*] Immutable Bitcoin blockchain proof anchored and saved to: {stamp_path}")
            return stamp_path
        except Exception as e:
            print(f"[!] Blockchain anchoring deferred / offline: {e}")
            return None

    def broadcast_to_swarm(self, host: str = "127.0.0.1", port: int = 5280) -> None:
        """Broadcasts the compiled dossier packet over UDP port 5280 to the active CML socket swarm."""
        report = {
            "manifesto": "Love Over God - Absolute Transparency Framework",
            "target_entity": self.target_entity,
            "total_records_audited": len(self.dossier_ledger),
            "generated_at": self.timestamp,
            "ledger": self.dossier_ledger
        }
        
        payload = json.dumps({
            "protocol": "CML_MYCELIAL_BROADCAST",
            "axiom": "Love Over God",
            "node_target": self.target_entity,
            "payload": report
        }).encode('utf-8')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(payload, (host, port))
            print(f"[*] Broadcasted CML dossier packet to active mesh swarm at {host}:{port}")
        except Exception as e:
            print(f"[!] Broadcast failed: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    daemon = SunlightAuditDaemon(target_entity="Pacific_Energy_DataCorp_Node", sector="Grid & Water Infrastructure")
    
    # Ingesting anomalous land-option and untracked power/water allocations
    daemon.ingest_record(
        record_id="ORESTAR_REF_99482",
        source_url="https://orestar.sos.state.or.us/",
        raw_data={"transfer_amount": 60000, "recipient_PAC": "Utility_Capture_Fund_A", "water_rights_mgd": 4.2},
        anomaly_score=0.94
    )
    
    output_file = daemon.generate_public_dossier("./dossiers")
    print(f"[*] Immutable transparency dossier compiled and locked at: {output_file}")
    
    # Anchor proof to Bitcoin blockchain
    daemon.anchor_to_blockchain(output_file)
    
    # Broadcast across UDP 5280 to the CML socket swarm
    daemon.broadcast_to_swarm(host="127.0.0.1", port=5280)
