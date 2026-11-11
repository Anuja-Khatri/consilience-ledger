# PREREGISTRATION

Written to fix methods before computing headline numbers where feasible (Phase 7). Where
a number already exists from an earlier phase, that is stated plainly rather than claimed
as preregistered.

## Scope of the determinism claim (D4)
Extraction is not deterministic and is not claimed to be. From approved claim cards
onward the pipeline is byte-deterministic: `make reproduce` regenerates the identical
ledger hash. This split is stated in README and METHODS.

## Preregistered decision rules (fixed before the data was seen)
- D6 pilot GO/NO-GO rule: coded in `labext/pilot.py` before extraction ran. Applied
  autonomously, never softened. Outcome: NO-GO twice (Phase 2).
- Baseline sample: preregistered in `labext/baseline.py` as a deterministic selection
  (all forks and corroborations, plus the first 40 condition-defect and first 20
  axis-mismatch pairs by sorted pair_id). No pairs are cherry-picked.
- Verdict floor D7: difference must exceed max(13 mV, the claim's own uncertainty) for a
  confirmed/contradicted verdict; otherwise within_floor.

## Materials extraction-stability measurement (preregistered here, before running)
- Protocol: test-retest on identical passages. Re-run extraction on the SAME passages
  K=3 times with the same model and prompt (temperature left at the API default; the
  API does not accept temperature 0 for this model family, recorded as a caveat). A claim
  is counted stable if its (subject, axis, quantity-family) recurs in at least 2 of 3
  runs. Stability = stable claims / distinct claims.
- n is reported as the number of distinct claims over the sampled passages.
- The materials number is unknown until measured in this build and is reported fresh with
  its n (II.3). It is NOT compared to the consciousness-domain 0.25 as if the same metric;
  the consciousness number is cited separately with its own n and domain.

## Numbers already computed (descriptive outcomes, not preregistered hypotheses)
Pilot yield (70 approvable, Phase 2), approved claims (34, Checkpoint 1), ledger counts
(0 forks, 561 vetoes, Phase 4), verdicts (0 confirmed, 0 contradicted, 9 not_comparable,
Phase 5, corrected per CORRECTIONS.md). These are descriptive results of fixed rules,
reported with their provenance, not headline hypothesis tests.

## Durability consistency check — claim 2609.30133__010 (preregistered BEFORE opening the trace, fix #7)
- Claim under test: "InMnPdOx is the most stable, sustaining an overpotential below 0.5 V over
  1,000 h" (arXiv:2609.30133, claim 2609.30133__010).
- Data used: the authors' OWN released H-cell trace, `upstream/lila_oer_manuscript/data/fig_3e.csv`
  (iR-corrected overpotential per material system; cited by sha256 + rows).
- PASS rule (fixed before any value in fig_3e.csv was read): the check PASSES iff the InMnPdOx
  system's iR-corrected overpotential in the released trace is strictly below 0.5 V at EVERY
  recorded point for that system. It FAILS iff any recorded InMnPdOx point is >= 0.5 V. It is
  INCONCLUSIVE iff the trace contains no InMnPdOx system, or carries no per-point time axis to
  bound the stated 1,000 h duration (in which case only the "below 0.5 V" magnitude is testable and
  the 1,000 h duration is reported as not-verifiable-from-this-file).
- Threshold handling: 0.5 V is the claim's own stated threshold; no extra floor is applied (this is
  a threshold-crossing check, not a fork). Values are read in volts as released.
- LABEL (fixed): this is a CONSISTENCY CHECK between the authors' claim and the authors' own data —
  same authors, same iR-corrected measurement. It is NOT independent confirmation. The claim itself
  notes the 1,000 h figure rests on "repeated measurements over a partial duration on planar and
  porous supports" (Figs. S4–S6), so agreement here means the claim is consistent with the released
  trace, nothing more.
