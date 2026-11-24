# CSV fixture acceptance criteria

The verifier reads the bundled operations in file order and keeps a separate cart for each ID. The following rules describe the behavior exercised by the local fixture.

- A `put` sets the quantity for one lowercase ASCII letter. Quantities are integers from 0 through 9. An invalid item or quantity raises `ValueError` and leaves the cart state intact.
- A `read` returns the stored quantity, including zero, or `None` for an absent item. An exported mapping is independent of the live cart. The `probe_export` operation checks that modifying this mapping leaves the cart intact.
- A `begin` opens an edit. `finish(True)` keeps the innermost edit. `finish(False)` restores the state from before that edit began, even if an inner edit had already been saved. A non-boolean argument raises `TypeError` and leaves the current edit open. Finishing without an open edit raises `RuntimeError`.
- Every operation has one expected result. The verifier compares the state and any return value or exception type for each case, writes the input and source digests, and exits with status 1 when a comparison fails.
