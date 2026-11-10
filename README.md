# consilience-ledger

**Independent work, not affiliated with or endorsed by Lila Sciences.**

Signed off at Checkpoint 2. License: code MIT (`LICENSE`); data and reports CC-BY-4.0
(`LICENSE-DATA`). Lila's instrument data is not committed; it is loaded at runtime and
cited by sha256 and row index (CC-28).

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

## Status (Stage 1 complete through Checkpoint 2; Stage 3 scaffolding in place)
- Phase 0 inventory; Phase 1 judge + conditions veto; Phase 2 real dual-model extraction
  + D6 pilot; Phase 3 Checkpoint 1 (Anu's batch applied); Phase 4 ledger; Phase 5
  writeback; Phase 6 LLM-judge baseline; Phase 7 evaluation discipline; Phase 8 browser +
  this finalisation. Phase 9 safety format. Phases 10-11 scaffolding. Done.
- The two human checkpoints are the advertised integrity mechanism. Checkpoint 1 is
  resolved (Anu's decisions applied). Checkpoint 2 signed off; publishing is held until the full build is done. Nothing
  is published.

## Results (numbers from NUMBERS_LOCK.json, each with its n and qualifier, II.3)
- Judge: 1.0 agreement vs an independent logic program (n=213) and vs SMT (n=311); these
  are locked Consilience numbers, cited as such.
- Corpus (real): two accessible papers (their paper and ref 40); the rest paywalled and
  excluded. The D6 pilot returned NO-GO twice (iR-correction is stated in few result
  sentences), so the corpus is the minimal accessible slice.
- Ledger over 34 approved claims: 0 numeric forks, 561 vetoes (515 axis_mismatch, 149
  condition_unstated, 3 condition_mismatch). The veto table is the headline result: most
  literature pairs are not comparable, so they are not called disagreements. This is
  designed to surface exactly that, and it does.
- Writeback vs Lila's own H-cell data (loaded at runtime, not committed): every comparison
  is a published veto. No claim's conditions were proven comparable to an H-cell
  measurement (the CP1 600s screening data is comparative, not absolute, and is not used to
  confirm or contradict). The published pure-Pd claims are among the vetoes. See
  CONTRADICTION_DOSSIER.md.
- LLM-judge baseline: on a preregistered sample of 60 vetoed pairs, a model call made 4
  comparisons the deterministic veto blocks.
- Fresh materials extraction-stability: 0.423 (n=52, test-retest). This is the materials
  number, reported fresh; it is not the consciousness-domain 0.25 (different domain and
  metric).

## Browse
Open `browser/index.html` from any local file server (it reads `ledger/*.json` by relative
fetch). Phases and the full method are in STATE.md, METHODS.md, and the spec.

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
