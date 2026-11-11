# PREREG_KNOWN_ANSWER - Test 1 (feature 7), the ref 39 vs ref 40 pair

Written **2026-11-11, BEFORE reading either paper.** Locked honesty rails apply.

## The pair
- **Ref 40** = Peng et al., "Hierarchical palladium catalyst for highly active and stable water
  oxidation in acidic media," *Natl. Sci. Rev.*, DOI 10.1093/nsr/nwac108. Open full text at
  **PMC10035503**.
- **Ref 39** = Cherevko et al., "Dissolution of Noble Metals during Oxygen Evolution in Acidic
  Media," *ChemCatChem* 2014, 6, 2219, DOI 10.1002/cctc.201402194. Access order: (a) free Wiley SI
  PDF; (b) co-author Zeradjanin's Academia.edu; (c) abstract + SI only = **partial**. Never any
  pirate mirror. Access route recorded per paper in the manifest.

## Exactly three outcomes (the only vocabulary allowed in the conclusion)
- **O1** - the judge finds a **fork** on a **shared axis** with **stated conditions on both sides**.
- **O2** - the judge **refuses** the pair and **names the missing or mismatched condition fields**;
  those named fields are the finding.
- **O3** - once typed, the papers **do not disagree**: different axes (e.g. dissolution rate vs
  overpotential or durability) or compatible claims.

## Dated prior (recorded before reading)
The search abstracts suggest **ref 39 reports Pd dissolution as comparatively low among the noble
metals**, so **O3 is a live possibility known before reading** (low Pd dissolution would be
compatible with ref 40's claim of a stable Pd catalyst; and the two likely report different axes -
dissolution rate vs overpotential/durability).

## Method (deterministic rules; locked rail: NO model API calls)
- The pipeline's "dual-model extraction" cannot run - model API calls are barred by the locked
  rails. Honest substitute: a **single manual typed extraction** by the reader, each card carrying
  verbatim source sentences + provenance. This deviation is recorded here and in the manifest;
  nothing is presented as a model-run extraction.
- **Contested cards** (any condition field unclear or one-sided) are routed to the **review queue
  for Anu**, not self-approved.
- The **judge runs on the deterministic rules only** (no model): `engine.verdict.compare_pair` with
  the hash-locked `comparability_rules` (chem **CR1–CR5**, default-deny) and **CR-ID**. Cross-paper
  pairs are cross-source (different `source_id`), so CR-ID does not waive; stated conditions are
  required on both sides (default-deny). Verdict taxonomy: not_comparable / within_floor /
  replicate_inconsistency / **fork** / suspect_transcription / untestable.
- Condition fields the CR predicates check (what O2 would name): **electrolyte identity (+
  concentration), current_density, temperature, iR correction**, plus the **axis** and **same-entity
  (composition)** gates that precede them.
- The conclusion will use **only O1 / O2 / O3**.
