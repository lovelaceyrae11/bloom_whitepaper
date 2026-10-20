# Castleberry Bloom PBFT
## Primary Rotation Experimental Test Checkpoint

Date: 2026-10-16

### Purpose

Record the primary-rotation experiments and the corrected test outputs.
The rotation rule remains provisional and is not yet adopted protocol policy.

### Provisional Rule

primary(view) = node_order[view % node_count]

### Positive Test

Script:
test_artifacts/test_primary_rotation_v5_valid_reportfix.py

View: 0
Expected primary: node-core-001
Observed result: ACCEPTED

Finding: The experimental verifier accepted the correctly selected primary.

### Negative Test

Script:
test_artifacts/test_primary_rotation_v5_reportfix.py

View: 0
Expected primary: node-core-001
Supplied primary: node-core-002
Observed result: REJECTED

Verifier message:
Primary rotation violation: view 0 requires node-core-001, not node-core-002.

Finding: The experimental verifier rejected the incorrectly selected primary.

### Multi-View Test

Script:
test_artifacts/test_primary_rotation_multi_view.py

Total checks: 8
Passed: 8
Failed: 0

Tested views: 0, 1, 2, and 126.

The cases tested expected-primary acceptance and wrong-primary rejection.
Test signatures and modified ledger data were generated in memory.

### Hardened Verifier Comparison

The existing hardened v4 verifier accepted a re-signed proposal
that violated the proposed rotation rule. This demonstrates that v4 does not enforce
that proposed rotation rule.

### Compatibility Issue

The original engine selects nodes[0] and hardcodes view 1.
The experimental rotation rule expects nodes[1] at view 1.
This conflict must be resolved before the rule is adopted.

The original engine's PREPARE and COMMIT messages also omit the view
number, while the isolated view-bound engine includes it.

### Scope and Limitations

These are local verifier tests using locally available keys and
in-memory test data. They are not a distributed 127-node consensus run.

The results support enforcement of the provisional primary-rotation
rule in the tested cases. They do not prove complete PBFT safety,
liveness, or a complete view-change protocol.

### Preservation

This checkpoint records observed test results. The original engine,
hardened verifier, saved ledger, existing test scripts, and previous
reports were not intended to be modified by creating this report.

No ledger hash is asserted here as a new measurement. Verify current
hashes separately if a fresh integrity check is required.
