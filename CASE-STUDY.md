# A fixed acceptance check caught a rollback defect

## Specify the state transition

The requirements define the difference between an absent item and a zero quantity, require independent cart instances and specify what can happen inside nested edits. In the key sequence, saving the inner edit makes it visible during the outer edit. Discarding the outer edit then restores the state from before it began.

The verifier plays the ordered operations in `orders.csv` against the selected draft. It compares the exported cart after each operation and checks expected return values or exception types from `expected.json`. Both drafts use the same operation order, expected outcomes and checker.

## Inspect the first mismatch

The first draft stored the live dictionary as its snapshot. The following edits therefore changed both working state and the object that was meant to restore it. The first mismatch appears at `outer_discard`, with `{"x": 3, "y": 0}` still present where `{"x": 2}` was expected. Several subsequent mismatches reflect that same state error.

The corrected draft uses a shallow copy when an edit opens. The cart stores integers, so copying the outer mapping preserves its previous values. The paired reports record matching input, checker and contract digests. Their 10/18 and 18/18 results describe a regression comparison on this sequence.

## Interpret the check

The input and expected values are available to the candidate author, and Codex wrote the candidates and checker. The bundle models an acceptance workflow with inspectable evidence. A production workflow would need a separate input validation layer and checks for any additional requirements it claims to satisfy.
