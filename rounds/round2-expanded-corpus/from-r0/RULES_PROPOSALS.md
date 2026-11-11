# Comparability-rule proposals with page-level sources - for Gate 1 per-rule approval

Each rule below is a PROPOSAL. Anu approves or rejects each one individually at Gate 1, with
its source cite (locked plan item 4's letter and strategy section 6). All rules are
default-deny: two claims are non-comparable unless every applicable key matches; every veto
names its rule and the defect. Sources are open-access papers retrieved in R0 (PROVENANCE.md);
quotes are copied from the fetched full-text XML and carry their section.

Carried from v1 (already locked at CP1-TRIAGE): CR1 canonical electrolyte list, CR2/CR3 pint
unit canonicalisation. The proposals below are the sourced additions/refinements R0 justifies.

## CR-A  Electrolyte identity must match
- Rule: claims in different electrolyte identities (e.g. 0.5 M H2SO4 vs 0.1 M HClO4 vs 1 M
  KOH) are non-comparable; defect `condition_mismatch(electrolyte)`.
- Source: B2 (PMC13707403), Abstract/intro: comparability is asserted only "on a matched
  basis (1 M KOH, room temperature)"; the matched basis explicitly includes the electrolyte.
- Status: refines v1 CR1 from a canonical list to an identity-match veto.

## CR-B  Current-density convention must match
- Rule: an overpotential reported at one current density is non-comparable to one at another
  (eta@10 vs eta@1 vs eta@100 mA/cm2-geo); defect `condition_mismatch(current_density)`.
- Source: B2, section 3.2 ("The 10 mA cm-2 Benchmark: Origin ...") and section 3 generally,
  which documents divergence "by more than 150 mV at 100 mA cm-2" relative to 10 mA cm-2.
- Note: the current density must be geometric-area-normalized before matching (MPS adapter,
  OQ-R0-8).

## CR-C  iR-compensation fraction must match or be flagged
- Rule: two claims whose stated iR-compensation fractions differ are non-comparable; if either
  is unstated, the pair carries defect `condition_unstated(ir_correction)` and cannot be an
  equality. Depends on conditions-delta D-1 (CONDITIONS_DELTA.md).
- Source: B2, section 3: "the reported overpotential at 25 mA cm-2 slid continuously from 437
  mV uncompensated down to 382 mV at full compensation, depending on which fraction the author
  chose [8]" and "the percentage of ohmic (iR) drop compensation ... often left unstated, has
  an outsized effect on the resulting overpotential."

## CR-D  Temperature must match
- Rule: claims at differing (or unstated) temperature are non-comparable; defect
  `condition_mismatch(temperature)` or `condition_unstated(temperature)`.
- Source: B2 matched-basis clause "(1 M KOH, room temperature)" - temperature is part of match.

## CR-E  Loading / geometric-vs-intrinsic activity must match
- Rule: overpotentials at materially different catalyst loadings are non-comparable on a
  geometric basis; defect `condition_mismatch(loading)`.
- Source: B2, section 3.3 ("The Loading Artefact and Three-Dimensional ...") documenting that
  loading shifts geometric-current activity independent of intrinsic activity.

## CR5  Protocol-tier must match  (the decision the strategy asks Anu to make)
- Proposed tiers (already in the v1 vector's `protocol_tier` enum):
  `ht_screen` (seconds-to-minutes HT screen), `medium_term`, `long_term` (e.g. 2 h+ stability),
  `other_stated`, `unstated`.
- Rule: an activity number from a short HT screen is non-comparable to one from a long-term
  stability protocol; defect `condition_mismatch(protocol_tier)`. Unstated tier is a defect,
  not a wildcard.
- Sources:
  - ref 27 (PMC10012258, Hochfilzer/Chorkendorff/Kibsgaard, ACS Energy Lett 2023,
    CC BY-NC-ND): catalyst-stability considerations - activity and stability are distinct
    regimes and must not be conflated.
  - B3 (PMC10576816, Comms Chem 2023): the McCrory protocol (which fixes a 2 h / 10 mA cm-2
    stability step) "is the most widely used, yet still only by an insignificant fraction of
    all OER publications" - so protocol tier is usually unstated and must be modeled explicitly.
  - MPS evidence: MPS acidic data is `ht_screen` (CP3/CP4 short holds); mixing its numbers
    with literature long-term stability numbers would be a tier mismatch by construction.
- CR5 decision for Anu: (i) adopt the five tiers as above; (ii) set the default-deny veto on
  tier mismatch and on unstated tier; (iii) map MPS CP-stage FOMs to `ht_screen` and Lila's
  600 s CP to `ht_screen`/`medium_term` as the adapters see the hold time. Anu picks the letter.

## Empirical-floor rule (feeds the S3 decision, not a comparability veto)
- Proposal: the comparability floor for an acidic-OER overpotential block =
  max(stated uncertainty, 13 mV, the MPS empirical replicate floor for the matching condition
  block). R0 measured that empirical floor at ~22 mV (strict same-sample repeat) to ~51 mV
  (same-composition-block), median, with p90 > 130 mV (MPS_SURVEY.md section 3). Direction is
  always the more conservative (larger) floor. This is supersession S3; Anu signs it at Gate 1.

## What is NOT proposed (held to locked rails)
No derived conditions, no composition proposing, no rule without a quoted source on the card.
Every rule above vetoes by default and names its defect; none infers a missing value.
