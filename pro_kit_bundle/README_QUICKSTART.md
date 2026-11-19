# Zero-Burn Agent Wrapper & Client Compliance Kit ($49 Pro Edition)

## 1. Quick Integration (CrewAI / LangChain / Custom Agents)
Wrap any agent task or LLM call with `SovereignCircuitBreaker` to immediately block infinite loops, enforce a hard dollar cap per run, and generate a cryptographic SHA-256 audit log for your clients.

```python
from zero_burn_wrapper import SovereignCircuitBreaker

guard = SovereignCircuitBreaker(max_steps=10, max_budget_usd=1.50)

def run_agent_step(prompt_text):
    # Pre-execution Step-0 check before spending API credits
    guard.verify_step_zero(prompt_text, estimated_tokens=1200)
    # Proceed with LLM / CrewAI execution...
    return "Agent Output"

# Export verifiable JSON/PDF-ready compliance seal for client handoff
seal = guard.export_client_audit_seal()
print("Client Seal Generated:", seal["final_seal_sha256"])
