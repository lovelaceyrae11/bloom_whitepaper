# Castleberry Bloom PBFT Primary-Rotation Regression Report

## Test purpose
Determine whether the hardened view-bound verifier enforces a provisional deterministic primary-rotation rule.

## Provisional rule
primary(view) = node_order[view % node_count]

This is a proposed test rule, not yet an established Castleberry Bloom protocol requirement.

## Test configuration
- Topology nodes: 127
- Test view: 0
- Expected primary: node-core-001
- Actual proposal primary: node-core-002
- Proposal and vote signatures: regenerated using the corresponding local test keys
- Ledger hash: recalculated in memory
- Saved test ledger: not modified by the test script

## Observed result
RESULT: ACCEPTED

The hardened verifier accepted a correctly signed proposal from a trusted node that violated the provisional rotation rule.

## Finding
The verifier does not enforce the provisional primary-selection rule tested here.

## Limitations
This result does not establish that the provisional rule is the correct protocol rule. It does not prove that the complete PBFT system is unsafe, nor does it establish distributed safety or liveness.

## Next steps
1. Define the intended primary-selection and view-change rules.
2. Implement a proposed fix in a separate verifier copy.
3. Test both valid and invalid primary selections.
4. Rerun the existing verification and malformed-input tests.
5. Preserve the original engine, verifier, ledger, and previous checkpoints.

