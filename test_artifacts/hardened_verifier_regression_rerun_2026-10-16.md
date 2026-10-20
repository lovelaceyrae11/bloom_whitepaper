# Castleberry Bloom PBFT
## Hardened Verifier Regression Rerun

Date: 2026-10-16

### Verifier
File: independent_verifier_v4_viewbound_hardened.py
SHA-256: 3f7f0c7d15378bfebb775fe12c909dead69cae779d0e5c71ea315b99448c4071

### Regression Results
Result: 7 of 7 tests passed.

1. Trust anchor and 127 node certificates verified.
2. Pristine isolated test ledger verified.
3. Conflicting sequence/state root rejected.
4. Public-key substitution rejected.
5. Untrusted quorum value rejected.
6. Duplicate COMMIT voter rejected.
7. PREPARE signature from a different view rejected.

### File Fingerprints After the Test
Isolated test ledger:
cea0ab06a25b3a00759d488e3835b983fd2d4c1d231ccff506b7d0de61245695

Saved ledger:
ab33dd4d20a60239f981f1a8383b2a9dff41c195df8fd73032939383bce6608a

The saved ledger hash matches the current hash checkpoint.
The isolated test ledger hash was captured after the regression run.

### Scope and Limitations
These are local verifier regression results. They do not establish
full distributed PBFT safety or liveness, network-wide consensus,
or correct behavior under every view-change scenario.

The historical difference between the saved ledger hash and the
older baseline remains unresolved.

### Preservation
This checkpoint is a new file. The original verifier, saved ledger,
and earlier reports were not intentionally modified by this
checkpoint-creation command.
