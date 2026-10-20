# Castleberry Bloom View-Bound Validation Checkpoint

Recorded (UTC): 2026-10-16T05:18:05.988196+00:00

## Environment
- Python: 3.14.6
- Cryptography: 50.0.2

## Configuration
- Configured nodes: 127
- Assumed fault bound: 42
- Required quorum: 85

## Test outcome
- Reported result: all seven verifier tests passed.
- Cross-view PREPARE signature check: passed.
- Scope: local cryptographic and ledger verification tests.
- This does not prove distributed PBFT safety or liveness.

## SHA-256 fingerprints
- `pbft_consensus_engine_v4_viewbound.py`: `8270b591b31db7f7957e93af04ef496a506dc60998b6f4c5658b284c32395af6`
- `independent_verifier_v4_viewbound.py`: `b678c22d7ab1dede11689550ccfc7412bb9cdf6d0d745179fa1727c47ade0750`
- `test_artifacts/pbft_v4_viewbound_test_ledger.json`: `cea0ab06a25b3a00759d488e3835b983fd2d4c1d231ccff506b7d0de61245695`

## Qualification
The test result is recorded from the supplied terminal output. The fingerprints identify the file contents at checkpoint time. The verifier is a local test harness and does not establish independent agreement among 127 separate machines.
