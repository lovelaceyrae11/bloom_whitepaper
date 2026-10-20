# Castleberry Bloom: Hardened Verifier Regression Checkpoint

Recorded UTC: 2026-10-16T05:34:09.950899+00:00

## Verifier
File: independent_verifier_v4_viewbound_hardened.py
SHA-256: 3f7f0c7d15378bfebb775fe12c909dead69cae779d0e5c71ea315b99448c4071

## Existing verification suite
Result: 7 of 7 tests passed on the hardened verifier copy.

## Malformed sequence regression tests
- Boolean True: rejected by sequence validation.
- Negative integer -1: rejected by sequence validation.
- Numeric string "1001": rejected by sequence validation.
- Floating-point value 1001.0: rejected by sequence validation.
Result: 4 of 4 malformed sequence tests passed.

## Scope limitation
These results cover local verifier tests. They do not establish full distributed PBFT safety or liveness.

## Preservation
This report is separate from the original verifier and earlier checkpoints. The original verifier, ledger, and previous reports were not modified by this report-creation command.
