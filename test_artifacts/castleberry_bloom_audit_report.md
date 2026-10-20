# Castleberry Bloom PBFT Prototype Audit Report

## 1. Baseline Verification

Result: PASS

Verifier: independent_verifier_v2.py

Expected node count: 127
Required quorum: 85

Unique node certificates checked: 127
PRE-PREPARE signature: Valid
PREPARE votes: 127 unique valid signatures
COMMIT votes: 127 unique valid signatures

Pinned root certificate SHA-256:
9745b5840660bb48166ff142968fa90469df9606e1836e3255ac3d51bef8bea9

Verified ledger SHA-256:
e66251c3935df2f3a85a0daf69c2a8c24163500c8e261a24acfaffc6767e584b

## 2. Negative Tests

1. PREPARE signature alteration
   Result: PASS
   Observed: Invalid PREPARE signature rejected.

2. Insufficient quorum
   Result: PASS
   Test input: 84 PREPARE votes; required quorum 85.
   Observed: PREPARE quorum not met.

3. Duplicate vote
   Result: PASS
   Test input: 128 vote entries, 127 unique voters.
   Observed: Duplicate PREPARE vote from node-core-001 rejected.

4. Proposal state-root alteration
   Result: PASS
   Observed: Invalid PRE-PREPARE signature rejected.

## 3. Scope and Limitations

These tests demonstrate specific signature-validation,
quorum-enforcement, duplicate-vote, and proposal-integrity
checks in the local verifier.

They do not establish independent multi-machine consensus,
Byzantine fault tolerance, network security, or production
readiness.

The prototype generates votes locally using keys held in
node_secrets.json. Independent participation by 127 machines
has not been demonstrated by these tests.

The pinned root fingerprint identifies the expected root
certificate but does not, by itself, establish an external
trusted identity for that certificate.

## 4. Preservation

The negative tests used separate files under test_artifacts.
The original ledger passed verification again after testing.

This report records observed terminal results; it is not an
independent third-party security audit.

## Independent Verifier V3 Results

Date: 2026-10-15

V3 passed verification of the preserved prototype ledger.

- Root certificate fingerprint, validity, and self-signature checked.
- 127 unique node certificates and public-key matches checked.
- Expected primary, view, sequence, and proposal structure checked.
- PRE-PREPARE signature verified.
- 127 unique PREPARE votes and 127 unique COMMIT votes verified.
- Configured quorum of 85 met for both phases.
- Ledger hash matched the previously recorded value:

  `e66251c3935df2f3a85a0daf69c2a8c24163500c8e261a24acfaffc6767e584b`

V3 negative tests rejected all four test fixtures:

- Tampered PREPARE signature.
- PREPARE quorum reduced to 84.
- Duplicate PREPARE voter.
- Modified proposal contents.

Scope limitation:

These tests establish specific integrity-checking behaviors for a local prototype. They do not demonstrate independent multi-machine consensus, production Byzantine fault tolerance, or external trust establishment. Existing PREPARE and COMMIT signatures do not include the view number.

The original ledger was not intentionally modified during these tests.
