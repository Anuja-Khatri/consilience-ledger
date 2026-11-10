# DECISIONS

Decisions taken during the build, keyed to the spec's pre-made decisions (D1-D17)
and corner cases. Standing rulings from Anu are in OPEN_QUESTIONS.md.

## Phase 1
- D1: Python 3.15 venv in repo; requirements.txt pinned (pydantic 2.14.3, networkx
  3.7, Pint 0.26.2, PyYAML 6.0.3, pytest 9.2.0).
- D4: determinism split implemented and documented (README, METHODS). Judge records
  carry a content_hash, rules_version, map_version.
- IV.1: Claim Card v2 modelled in pydantic v2; JSON Schema generated from the models
  so the two cannot drift. Conditions is exactly ten keys (extra=forbid).
- IV.2: comparability engine is default-deny with named defects. The vendored matcher
  gained a `conditions_compatible` predicate that delegates to the authoritative
  `labext.comparability`, so there is one source of truth.
- Design: NetworkX DiGraphMatcher accepts only node_match/edge_match, so the
  comparability veto runs as a pre-filter over the pair, not as a third matcher
  callback (recorded in ENGINE_INVENTORY as the Phase 1 design flag).
- CC-06: current_density carries `normalization` (geometric|ecsa|unstated); CR2
  requires it to match.
- CC-12: room_temperature is an enum; room_temperature vs a number is a mismatch.
- CC-14: no conditions veto on non-quantitative (mechanism) pairs; those take the
  structural judge path.
- rules v0 is PROVISIONAL (sources finalized Phase 3). Hash-locked in rules.lock.
