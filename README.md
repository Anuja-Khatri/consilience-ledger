# Consilience Lab Extension (working name)

Work in progress. Not for publication. The public name and final wording are
decided at Checkpoint 2 (spec II.2, D2).

## What this is
A deterministic, open hypothesis-comparison engine extended to the published
literature of closed-loop autonomous laboratories, with acidic oxygen evolution
(OER) as the concrete instance. A language model extracts claims into typed
fields. A deterministic judge compares them. The judge has no text channel. Before
two quantitative claims may be called a disagreement, their measurement conditions
must be proven comparable; if they are not, the pair is vetoed with a named defect.

## The determinism split (D4, important)
Extraction is NOT claimed deterministic. It is gated by cross-model agreement and a
human review queue. The pipeline from APPROVED CLAIM CARDS onward IS byte
deterministic: the same approved cards plus the same rules version produce an
identical ledger hash. The README and METHODS state this split plainly and never
claim end-to-end determinism (CC-01).

## Status
- Phase 0: engine inventory (ENGINE_INVENTORY.md). Done.
- Phase 1: scaffold, Part IV schemas, vendored judge, pint units (fail-closed),
  the `conditions_compatible` veto beside the matcher, extended defect enums, and
  tests for the three condition defects, a true fork, and determinism. Done.
- Phases 2-12: see STATE.md and the spec.

## Layout
See the spec Part IV. Code lives in `labext/`; vendored upstream code in `vendor/`
with `PROVENANCE.md`; data contracts as JSON Schema in `schema/`; comparability
rules in `rules/`; the materials capability map in `domainpack/materials_oer/`.

## Develop
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    make test          # run the suite
    make schemas       # regenerate JSON Schema from the pydantic models
    make lock          # regenerate rules/rules.lock

## Honesty
Numbers in any outgoing text come only from the locked registry or Lila's own
publications, each with its n and qualifier (II.3). "Designed to," never "shown
to," for anything not measured. Nothing here claims or implies that Lila Sciences
uses, wants, or endorses this work.
