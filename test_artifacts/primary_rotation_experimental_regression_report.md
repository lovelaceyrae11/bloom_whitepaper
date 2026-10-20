# Castleberry Bloom PBFT
## Experimental Primary-Rotation Regression Report

Status: Experimental validation checkpoint

Purpose: Record the two primary-selection tests for the separate experimental verifier.

### 1. Scope

Experimental verifier:
`independent_verifier_v5_rotation_experimental.py`

Copied from:
`independent_verifier_v4_viewbound_hardened.py`

The primary-selection check was added only to the experimental copy.

### 2. Provisional Primary-Rotation Rule

The experimental rule is:

primary(view) = node_order[view % node_count]

The node order comes from cluster_extended.cml through
parse_and_validate_topology().

This rule is provisional. It has not been established as the
formally adopted Castleberry Bloom PBFT protocol rule.

### 3. Negative Test: Incorrect Primary

Test script:
test_artifacts/test_primary_rotation_v5.py

Test view: 0
Expected primary: node-core-001
Supplied primary: node-core-002

The test regenerated signatures in memory and recalculated the
ledger hash for the test proposal.

Observed result:
REJECTED: Primary rotation violation: view 0 requires
node-core-001, not node-core-002.

Outcome: PASS. The experimental verifier rejected the
incorrect primary under the provisional rule.

### 4. Positive Test: Correct Primary

Test script:
test_artifacts/test_primary_rotation_v5_valid.py

Test view: 0
Expected primary: node-core-001
Supplied primary: node-core-001

The test regenerated signatures in memory and recalculated the
ledger hash for the test proposal.

Observed result:
ACCEPTED

Outcome: PASS. The experimental verifier accepted the proposal
using the primary required by the provisional rule.

Note: The positive test script still prints a stale FINDING
message copied from the negative test. Its wording is incorrect.
The actual ACCEPTED result above is the relevant test outcome.

### 5. View-1 Compatibility Conflict

The existing engine uses nodes[0] as primary at view 1.

The provisional rotation rule instead expects nodes[1] at view 1.

These behaviors conflict. The experimental rule must not be
treated as an established protocol requirement until primary
selection, view numbering, and view-change policy are formally
specified.

No change to the original engine is authorized by this report.

### 6. Preservation of Existing Files

The tests constructed their modified proposals, signatures,
and recalculated hashes in memory.

The test scripts reported that the saved ledger was left
unchanged. No intentional changes were made to the original
verifier, original engine, saved ledger, or earlier reports.

This report is a separate experimental record.

### 7. Limitations

These results cover only two targeted primary-selection cases.

They do not establish full distributed PBFT safety or liveness,
correct view-change handling, preservation of prepared state,
network-wide consensus, or correctness of the provisional rule.

All test signatures were generated locally using test inputs
and private keys within one process. This was not a live,
distributed 127-node consensus run.

### 8. Recommended Next Steps

1. Formally define primary selection and view numbering.
2. Resolve the view-1 compatibility conflict before adoption.
3. Add tests for additional views and invalid primary choices.
4. Test view changes and prepared-state preservation separately.
5. Rerun the existing hardened-verifier regression suite without
   modifying its baseline files.

### 9. Conclusion

The experimental verifier passed one negative test by rejecting
an incorrectly selected primary and one positive test by
accepting the expected primary for view 0.

These results support the behavior of the experimental check
in the two tested cases only. The rotation rule remains
provisional and is not yet validated as a complete PBFT policy.


