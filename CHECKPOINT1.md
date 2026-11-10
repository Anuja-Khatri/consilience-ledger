# CHECKPOINT 1 (end of Phase 3) - for Anu, batched, non-interactive

This is the first of the two human checkpoints (II.1). It is the product's advertised
integrity mechanism, not an interruption. Review in one sitting; downstream phases wait
on your batch. Everything below is PROVISIONAL until you approve.

## 1. What happened (honest summary)
- Keys were sourced into the environment (never read into output); real extraction ran
  with `claude-sonnet-5` + `gpt-4.1` (D3 preferred: one Anthropic + one non-Anthropic).
- Corpus accessibility was the binding reality. Openly accessible and downloaded: their
  paper (arXiv:2609.30133) and ref 40 (Peng 2023, NSR, via Europe PMC). Paywalled and
  `excluded_inaccessible` (no scraping): refs 39 (Cherevko, Wiley), 42 (Chong, Science),
  11 (Wan, Nat Catal), 12 (Cherevko, Curr Opin).
- The D6 pilot returned NO-GO twice and was never softened. The binding constraint:
  iR-correction is stated in ~3% of result sentences (it lives in Methods), so fewer than
  half of the numeric claims state electrolyte + current density + iR-correction together.
  Per the D6 ladder the corpus is now the minimal accessible slice: their paper + ref 40.
- This NO-GO is itself the product thesis in miniature: literature conditions are
  heterogeneous and under-stated, so most pairs will veto on `condition_unstated` rather
  than be called disagreements (CC-21).

## 2. Counts (honest)
| quantity | value |
|---|---|
| papers accessible / excluded | 2 / 4 |
| approvable numeric claims extracted | 70 |
| AGREED-PROVISIONAL (auto-agreed, both models identical card) | 0 |
| contested -> review queue (await your approve/reject) | 72 |
| parked (unparseable/invalid after repair) | 49 |

Because auto-agreement is 0, there are no AGREED-PROVISIONAL claims to carry into Phase 4
yet. The build correctly stops here until your batch returns.

## 3. The review queue (your approve/reject)
- Index: `extraction/review_queue/INDEX.md` (72 rows: file, source sentence, differing
  fields). One markdown file per contested claim, each with the source sentence, both
  model outputs, the field-level diff, and approve/reject checkboxes.
- Tick a box per claim (or edit a corrected card inline). Phase 3's `apply_review` reads
  your ticked verdicts into approved claim cards.

## 4. Drafted comparability rules (your confirmation)
- `rules/comparability_rules.yaml` (version comparability-v0), hash-locked in
  `rules/rules.lock`. Four default-deny rules: CR1 electrolyte (identity + concentration),
  CR2 current density (equal, same normalisation), CR3 temperature, CR4 iR-correction.
- Sources and rationale in `rules/SOURCES.md`. The empirical ancestor is ESAMP
  (Digital Discovery 2023, 2, 1078). Page-level citations for ESAMP ESI and refs 4/27
  are PENDING (those sources are not yet downloaded); the rules are labeled PROVISIONAL
  until the page-level cites are added. Please confirm the rule set or adjust the fields.

## 5. Exactly what your batch unlocks
- Approving claims -> approved claim cards -> Phase 4 builds the ledger over them: forks
  (settleable disagreements that passed the conditions veto), graded correspondences,
  and every vetoed pairing with its named defect and rule id.
- Confirming the rules -> the rules version is locked for the ledger; every fork,
  correspondence, and verdict record carries `rules_version` and `map_version`.
- Until then, every output is labeled PROVISIONAL and nothing is published (Checkpoint 2
  gates publishing).

## 6. What is already built and waiting (so Phase 4+ runs the moment you return)
- The deterministic judge + conditions veto (Phase 1), the extraction/agreement/review
  pipeline (Phase 2), the safety format (Phase 9), and the Stage 3 loop + discovery
  scaffolding (Phases 10-11) are built and tested (54 tests green, `make reproduce` green).
- OERSIM's dataset was located in the helao checkout, so the Phase 10 loop is unblocked.
