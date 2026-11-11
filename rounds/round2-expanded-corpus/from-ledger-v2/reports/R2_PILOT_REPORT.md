# R2 three-paper extraction pilot - report (stops at the review queue; Gate 2 is Anu's)

Dual independent model families (anthropic claude-sonnet-5, openai gpt-4.1) extracted
overpotential-at-current-density claims from three open-access acidic-OER papers on the
approved clusters. Agreement-v2: a claim auto-accepts only if BOTH families produced a
field-exact match on the judge-relevant fields (material, overpotential mV, current density,
electrolyte identity+concentration). Everything else is contested and triaged to Anu.
Research only; model keys sourced from the environment, never echoed. Caches in
`r2_out/model_cache.jsonl` (rerun is deterministic for seen prompts).

## Corpus (licenses in r2_corpus/PROVENANCE.md)
- PMC12606313 - Nat Commun 2025, CC BY-NC-ND - sulfonic-group IrOx OER catalyst (acidic/PEM).
- PMC13550445 - Nat Commun 2026, CC BY-NC-ND - spinel Mn3O4 site substitution, acidic OER.
- PMC13459051 - Chem Sci 2026, CC BY - Ta-enabled high-entropy acidic OER.

## Results
| paper | anthropic | openai | agreed | contested |
|---|---|---|---|---|
| PMC12606313 | 4 | 4 | 2 | 4 |
| PMC13550445 | 1 | 1 | 0 | 2 |
| PMC13459051 | 1 | 1 | 0 | 2 |
| total | 6 | 6 | **2** | **8** |

- Agreement rate: **0.20** (2 of 10 distinct claims auto-accepted). 0 model/API errors.
- iR-fraction stated rate: **0.60**; current-density stated rate: **1.00**.
- AGREED-PROVISIONAL cards written to `r2_out/agreed_provisional/`; contested items to
  `r2_out/review_queue/` with a triage-ready `INDEX.md`.

## What the agreed cards look like (real)
Example (PMC12606313): *Ir/IrOx~SO3H, overpotential 259 mV at 10 mA/cm2 (geometric) in
0.5 M H2SO4, iR correction = none (stated)*. This is condition-complete on the judge-relevant
fields, so it is immediately blockable and could fork against other literature in the acidic
cluster - unlike the MPS rows, which were unstated on three keys. The literature path is where
round-one forks can actually form.

## What the contested items teach (the review economics)
The 8 contested items are near-misses, not noise: e.g. the two families read the same sentence
as 255 vs 259 mV, or label a catalyst "Ir/IrOx" vs "Ir/IrOx (commercial)" - a material-string
difference that (correctly) fails field-exact match. These are exactly the cases a human should
adjudicate; triage batches them by paper and by disagreeing field so Anu reviews groups.

### Review-load projection from the pilot (for Gate 2)
- Single-axis extraction (overpotential only) yields ~2-3 contested claims per paper, far below
  v1's 36/paper (which extracted every numeric claim). Auto-accept at ~20% on first pass; the
  rest triaged. Scaling the approved OA clusters (Pd/HClO4 121, Co/H2SO4 ~697) at ~2.7
  contested/paper gives a tractable, batchable queue; a second agreement pass (relaxing the
  material-string exactness to a normalized formula) would lift auto-accept and shrink it
  further - a knob for Anu at Gate 2, not changed here.

## D6 / discipline signals (reported, not softened)
iR-fraction stated in only 60% of extracted claims and (from the structured side) 0% in MPS -
the under-reporting thesis holds on live literature. The agreement gate stayed strict
(material-string exactness kept two true-looking 281 mV claims contested); nothing was
auto-accepted on a loose match.

## Stop point
This is the triage-ready package. Gate 2 (Anu) decides: approve/reject each contested claim
(or correct a field); accept the agreed-provisional cards; set the agreement-pass knobs; and
choose the harvest depth K for R2-at-scale. No claim enters the ledger without that.

## Reproducibility
`PYTHONPATH=ledger-v2 python tools/run_pilot.py` after sourcing keys; cached calls make reruns
deterministic. Model ids recorded in `ledgerv2/extraction/extract.py` (MODELS).
