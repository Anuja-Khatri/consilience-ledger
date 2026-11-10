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
