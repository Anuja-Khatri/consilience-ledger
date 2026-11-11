# Gate 3 execution report - rules hardened, re-extracted, full census, K2. Stops at K2 review queue.

All Gate-3 decisions applied in order: preregister F1-F4/A4/A5 -> implement -> re-extract -> fold
the 17 approvals -> full census -> K2 harvest/extraction/census. Research only; keys sourced,
never echoed; everything cached and deterministic. 15 tests green.

## 1. Adjudication + rule changes (reports/GATE3_DECISIONS.md, rules/CHANGELOG.md)
- 17 approved K40 cards built (r2_out_k40/approved/); 34 rejected with reasons. PMC10035503
  deduped vs the (empty) v1 ref40 set as the canonical card.
- Preregistered and implemented: F1 acid-context harvest filter; F2 review detection; F3
  reagent/supplier electrolyte exclusion; F4 computed_not_stated rejection; A4 temperature
  attribution (room_temperature enum, quoted); A5 technique-to-tier (sweeps -> other_stated).

## 2. Re-extraction under the new rules (validation) - r2_out_k40_v2/
- F1/F2 filtered 4 of 40 papers (3 reviews + 1 no-acid). F4 dropped 5 computed-not-stated values.
- 17 new agreed-provisional cards, materially richer: electrolyte 17/17, protocol_tier
  other_stated 15/17 (A5), temperature 5/17, iR fraction 7/17 with real values (0.0, 0.85, 1.0).
- Validation of the filters against Anu's manual rejects: F2 auto-catches the reviews
  (PMC11935124/862, PMC11936017); F4 the computed values (PMC5684209) and unevidenced value
  (PMC7379386); F3 the reagent-purchase electrolyte. Honest limit: F1 does NOT auto-catch
  acid-mentioning-but-alkaline-measured papers (PMC10209667 etc.) - those are correctly resolved
  at the CLAIM level by electrolyte-context attribution, as Anu did (OQ-V2-2).

## 3. Full fork + correspondence census (reports/FULL_CENSUS.md)
Over 66 approved cards (v1 33, pilot 6, gate3 17, reextract 10; deduped). 22 blocks:
**0 forks, 0 corroborations, 172 vetoed.** Top blocker: temperature unstated (172/172), then
protocol_tier (155), ir_correction (152); plus real CR1/CR2/CR3 mismatches (20/22/8).

## 4. K2 round-two (reports/K2_CENSUS.md; r2_out_k2/)
- Preregistered selection (HARVEST_PREREG_K2.md): 20 OA acidic papers whose full text STATES an
  iR-compensation practice, all RuO2/IrO2-baseline, in H2SO4/HClO4. Licenses: 17 CC BY, 2 CC
  BY-NC, 1 CC BY-NC-ND.
- Extraction (A4/A5/F3/F4): 7 agreed-provisional, 17 contested -> triage-ready review queue
  (r2_out_k2/review_queue/INDEX.md).
- Census over 73 cards (adds k2 7): **0 forks, 0 corroborations, 210 vetoed.** CR3 (iR-fraction
  mismatch) now fires 10x - the ledger correctly rules pairs non-comparable because they used
  DIFFERENT iR compensation (0.0 vs 0.85 vs 1.0). That is the comparability engine working as
  designed on a corpus chosen for stated iR practice.

## 5. The finding - and the one caveat surfaced honestly
Across every corpus now measured - MPS structured, K40, and the iR-selected K2 - cross-source
forks do not form, and every blocked pair is named with a specific defect. The dominant blocker
is temperature (100% of K2 cross-pairs). **Caveat (OQ-V2-1):** this over-states temperature as a
field gap, because A4 under-recalls stated measurement temperatures - PMC10005387 states "in
0.5 M H2SO4 at room temperature" yet its card reads temperature=unstated. The 0-fork result is a
mix of real under-reporting (iR, tier, often temperature) and an A4 recall gap on temperature.
The remedy is a temperature-recall fix, not loosening the gate.

## 6. Stop point (next gate is Anu's)
Adjudicate the 17 K2 contested claims; fix A4 temperature recall and re-census; the CR1/CR2/CR3
near-miss pairs are the candidate forks once their last unstated condition is filled at review.
Nothing enters the ledger without that.

## Reproducibility
rules.lock / mappings.lock unchanged (rule YAML untouched; the fixes live in code + prereg
changelog). Re-run: tools/run_reextract.py, run_full_census.py, k2_harvest.py, run_k2.py with
keys sourced; model calls cached.
