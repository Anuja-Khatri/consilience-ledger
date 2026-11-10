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

## Checkpoint 1 (human gate, resolved 2026-11-10)
- The 72-claim review queue and the comparability rules were decided by Anu via a
  Claude-drafted triage (`CP1-TRIAGE.md`, copied into the repo). The recommendations were
  drafted by Claude against sentence-level evidence; the decisions and any overrides are
  Anu's. This is the project's disclosed method (the human gate is the advertised
  integrity mechanism), applied here. Overrides at approval: NONE (the three scope calls
  2609_022, ref40_030, ref40_031 default to reject per the triage).
- Applied autonomously: `labext/apply_cp1.py` ticked each verdict box and wrote corrected
  cards per batch rules BR1-BR7; `labext/extraction/apply_review.py` read the ticked
  verdicts into 34 approved claim cards (BR1 regenerated every id; no few-shot id survives)
  at `extraction/approved_cards.jsonl`. 38 claims rejected.
- comparability-v0 locked (section 5): CR1 canonical electrolyte list, CR2/CR3 pint unit
  canonicalisation (C -> degC, mA/cm^2 variants). CR5 (protocol_tier) logged as a v1
  candidate only (adding it in v0 would make the ledger 100% veto; stated rate 0.00).
