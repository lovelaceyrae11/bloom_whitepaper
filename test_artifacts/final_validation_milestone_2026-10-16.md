# Castleberry Bloom PBFT
## Final Validation Milestone

Date: 2026-10-16

### 1. Hardened Verifier Regression Suite

Verifier:
independent_verifier_v4_viewbound_hardened.py

Result: 7 of 7 tests passed.

Checks covered:
1. Trust anchor and 127 node certificates
2. Pristine isolated test ledger.
3. Conflicting sequence/state root rejection.
4. Public-key substitution rejection.
5. Untrusted quorum value rejection.
6. Duplicate COMMIT voter rejection.
7. PREPARE signature rejection for a different view.

The live output also confirmed rejection of a forged COMMIT signature.

### 2. Experimental Primary Rotation

Provisional rule:
primary(view) = node_order[view % node_count]

Multi-view regression:
8 passed, 0 failed.

Views tested: 0, 1, 2, and 126.

The tested cases accepted the expected primary and rejected an
incorrect primary. Test cases used in-memory data.

Additional negative test:
An incorrect primary for view 0 was rejected as expected.

The rotation rule remains experimental and is not yet adopted
as final protocol policy.

### 3. Saved Ledger Integrity

SHA-256 of pbft_consensus_ledger.jsonl:
ab33dd4d20a60239f981f1a8383b2a9dff41c195df8fd73032939383bce6608a

SHA-256 of pbft_consensus_ledger.final.json:
ab33dd4d20a60239f981f1a8383b2a9dff41c195df8fd73032939383bce6608a

Both files match each other and the previously recorded hash.

This confirms current byte-level consistency with that checkpoint.
It does not establish complete historical integrity.

### 4. Compatibility Issues

The original engine selects nodes[0] and hardcodes view 1.
The provisional rotation rule expects nodes[1] at view 1.

The original engine's PREPARE and COMMIT messages omit the view
number, while the isolated view-bound engine includes it.

These issues require explicit resolution before protocol adoption.

### 5. Scope and Limitations

These results are local verifier and regression tests. They are
not a live distributed 127-node consensus run.

They do not prove complete PBFT safety, liveness, network-wide
consensus, or a complete view-change protocol.

The configured fault bound and quorum are assumptions that need
to be justified against the protocol and threat model.

### 6. Preservation Note

This report records the observed results of the validation milestone.
The original engine, verifier scripts, saved ledgers, and previous
reports were not intended to be modified by creating this file.

No new ledger hash is claimed beyond the measurements recorded above.
