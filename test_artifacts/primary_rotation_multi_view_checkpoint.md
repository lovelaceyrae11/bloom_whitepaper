# Castleberry Bloom PBFT
## Experimental Primary Rotation Multi-View Checkpoint

Date: 2026-10-16

### Test
Script: test_artifacts/test_primary_rotation_multi_view.py
Verifier: independent_verifier_v5_rotation_experimental.py

Rule tested:
primary(view) = node_order[view % node_count]

### Results
Total checks: 8
Passed: 8
Failed: 0

View 0:
- Expected primary node-core-001 accepted.
- Different trusted primary node-core-002 rejected.

View 1:
- Expected primary node-core-002 accepted.
- Different trusted primary node-core-001 rejected.

View 2:
- Expected primary node-core-003 accepted.
- Different trusted primary node-core-001 rejected.

View 126:
- Expected primary node-shell-108 accepted.
- Different trusted primary node-core-001 rejected.

### Preservation Checks

Isolated test ledger SHA-256:
cea0ab06a25b3a00759d488e3835b983fd2d4c1d231ccff506b7d0de61245695

Saved ledger SHA-256:
ab33dd4d20a60239f981f1a8383b2a9dff41c195df8fd73032939383bce6608a

Both hashes matched their recorded values after the experiment.

### Scope and Limitations

The tests used locally generated signatures and in-memory ledger copies.
They were not a distributed 127-node consensus run.

These results establish that the experimental verifier enforced the
provisional primary-rotation rule for the tested cases. They do not
establish full PBFT safety, liveness, or a complete view-change protocol.

The provisional rule still conflicts with the original engine view-1
primary selection. Do not treat the rule as adopted protocol policy
until that compatibility question is resolved.

### Preservation

This checkpoint is a report of the experimental results. The test used
in-memory ledger copies. No changes to the original engine, hardened
verifier, saved ledger, or earlier reports were intended.
