# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import time
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class CoherenceNode:
    node_id: str
    public_key: str
    role: Literal["core", "shell", "gateway", "sensor"]
    version: str
    status: Literal["healthy", "degraded", "offline"] = "healthy"
    last_heartbeat: float = field(default_factory=time.time)

    def validate_state(self, max_heartbeat_age: float = 30.0) -> bool:
        """Enforces rigorous state, identity, and liveness invariants."""
        now = time.time()
        if not self.node_id or not self.public_key:
            return False
        if (now - self.last_heartbeat) > max_heartbeat_age:
            self.status = "offline"
            return False
        return self.status in {"healthy", "degraded"}

if __name__ == "__main__":
    # Test instance validation
    test_node = CoherenceNode(
        node_id="node-alpha-01",
        public_key="02a1b2c3d4e5...",
        role="core",
        version="1.0.0"
    )
    print(f"[*] Initialized node: {test_node.node_id}")
    print(f"[*] State validation check: {test_node.validate_state()}")
