"""
Castleberry Bloom Sovereign Systems — Zero-Burn Agent Wrapper (Pro Kit)
Deterministic Step-0 Circuit Breaker & Token Quota Guardrail for CrewAI / LangGraph / AutoGen
"""
import hashlib
import json
import time
from functools import wraps

class SovereignCircuitBreaker:
    def __init__(self, max_steps=12, max_budget_usd=2.50, cost_per_1k_tokens=0.015):
        self.max_steps = max_steps
        self.max_budget_usd = max_budget_usd
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.current_steps = 0
        self.estimated_spend = 0.0
        self.state_hashes = set()
        self.ledger = []

    def verify_step_zero(self, prompt_payload: str, estimated_tokens: int = 800):
        self.current_steps += 1
        step_cost = (estimated_tokens / 1000.0) * self.cost_per_1k_tokens
        self.estimated_spend += step_cost

        payload_hash = hashlib.sha256(prompt_payload.encode("utf-8")).hexdigest()

        # 1. Recursive Loop Detection (Exact state repetition)
        if payload_hash in self.state_hashes:
            raise RuntimeError(f"[GUARDRAIL HALT] Recursive agent loop detected at Step {self.current_steps}. SHA-256: {payload_hash[:16]}")
        self.state_hashes.add(payload_hash)

        # 2. Step Ceiling Enforcement
        if self.current_steps > self.max_steps:
            raise RuntimeError(f"[GUARDRAIL HALT] Max execution steps ({self.max_steps}) exceeded. Preventing runaway execution.")

        # 3. Hard USD Budget Ceiling
        if self.estimated_spend > self.max_budget_usd:
            raise RuntimeError(f"[GUARDRAIL HALT] Token budget cap (${self.max_budget_usd:.2f}) reached (Current:${self.estimated_spend:.4f}).")

        entry = {
            "step": self.current_steps,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "sha256": payload_hash,
            "cumulative_spend_usd": round(self.estimated_spend, 4),
            "status": "CLEARED"
        }
        self.ledger.append(entry)
        return entry

    def export_client_audit_seal(self, filepath="client_compliance_seal.json"):
        manifest = {
            "framework": "Castleberry Guardrail Pro v1.0",
            "total_steps_executed": self.current_steps,
            "total_estimated_spend_usd": round(self.estimated_spend, 4),
            "budget_ceiling_usd": self.max_budget_usd,
            "ledger_entries": self.ledger,
            "final_seal_sha256": hashlib.sha256(json.dumps(self.ledger).encode("utf-8")).hexdigest()
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        return manifest
