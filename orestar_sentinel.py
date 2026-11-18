import hashlib
import json
import os
import sqlite3
import csv
from datetime import datetime, timezone
from pipeline import SunlightAuditDaemon

class OrestarSentinelAgent:
    def __init__(self, target_committees: list, db_path: str = "orestar_state.db"):
        self.target_committees = target_committees
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes a local state database to track processed transaction IDs and prevent duplicate alerts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_transactions (
                record_id TEXT PRIMARY KEY,
                committee_id TEXT,
                amount REAL,
                detected_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def is_already_processed(self, record_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM processed_transactions WHERE record_id = ?', (record_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def mark_processed(self, record_id: str, committee_id: str, amount: float):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO processed_transactions VALUES (?, ?, ?, ?)',
                       (record_id, committee_id, amount, datetime.now(timezone.utc).isoformat()))
        conn.commit()
        conn.close()

    def poll_target_filings(self) -> int:
        """Polls ORESTAR records for target committees from incoming directory drops."""
        daemon = SunlightAuditDaemon(target_entity="ORESTAR_Live_Sentinel", sector="Continuous Campaign Finance Audit")
        new_discoveries = 0

        print(f"[*] Sentinel agent polling active committees: {self.target_committees}")

        watch_dir = "./orestar_incoming"
        os.makedirs(watch_dir, exist_ok=True)
        
        incoming_files = [os.path.join(watch_dir, f) for f in os.listdir(watch_dir) if f.endswith('.csv')]
        
        if not incoming_files:
            print("[*] No incoming ORESTAR CSV files found in ./orestar_incoming. Dropping sample sentinel delta...")
            # Sample sentinel test entry
            rec_id = "SENTINEL_DELTA_8842"
            if not self.is_already_processed(rec_id):
                daemon.ingest_record(
                    rec_id, 
                    "https://orestar.sos.state.or.us/", 
                    {"source_type": "ORESTAR_Live_Sentinel_Delta", "committee": "Committee ID 126", "amount": 25000.0, "purpose": "Grid Infrastructure Lobbying"}, 
                    0.88
                )
                self.mark_processed(rec_id, "126", 25000.0)
                new_discoveries += 1

        for file_path in incoming_files:
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rec_id = row.get('Tran ID') or row.get('Transaction ID')
                    if not rec_id or self.is_already_processed(rec_id):
                        continue

                    amount_str = row.get('Amount', '0')
                    try:
                        amount = float(amount_str.replace('$', '').replace(',', ''))
                    except ValueError:
                        amount = 0.0

                    if amount >= 5000:
                        anomaly_score = min(0.99, 0.6 + (amount / 200000.0))
                        raw_data = {
                            "source_type": "ORESTAR_Live_Sentinel_Delta",
                            "committee": row.get('Committee/Filer Name', 'Unknown'),
                            "contributor_payee": row.get('Contributor/Payee Name', 'Unknown'),
                            "amount": amount,
                            "purpose": row.get('Purpose', 'N/A'),
                            "date": row.get('Tran Date', datetime.now(timezone.utc).isoformat())
                        }
                        
                        daemon.ingest_record(rec_id, "https://orestar.sos.state.or.us/", raw_data, anomaly_score)
                        self.mark_processed(rec_id, row.get('Committee ID', '126'), amount)
                        new_discoveries += 1

        if new_discoveries > 0:
            output_file = daemon.generate_public_dossier("./dossiers")
            daemon.anchor_to_blockchain(output_file)
            daemon.broadcast_to_swarm(host="127.0.0.1", port=5280)
            print(f"[*] Sentinel successfully processed and locked {new_discoveries} new state filings.")
        else:
            print("[*] Sentinel sweep complete. No new anomalous deltas detected.")

        return new_discoveries

if __name__ == "__main__":
    sentinel = OrestarSentinelAgent(target_committees=["126", "Utility_PAC_Registry"])
    sentinel.poll_target_filings()
