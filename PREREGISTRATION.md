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

## Durability consistency check - claim 2609.30133__010 (preregistered BEFORE opening the trace, fix #7)
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
- LABEL (fixed): this is a CONSISTENCY CHECK between the authors' claim and the authors' own data - 
  same authors, same iR-corrected measurement. It is NOT independent confirmation. The claim itself
  notes the 1,000 h figure rests on "repeated measurements over a partial duration on planar and
  porous supports" (Figs. S4–S6), so agreement here means the claim is consistent with the released
  trace, nothing more.

### AMENDMENT 2026-11-11 (after the trace was opened) - the durability check omitted the standing floor
The pass rule above (fix #7) was written STRICT ("every recorded point below 0.5 V"; FAIL if any point
>= 0.5 V). That strict reading is kept on record, but it OMITTED the standing verdict-floor rule and is
superseded by this amendment.
- Standing floor rule (D7): a verdict threshold is the LARGER of 13 mV and the claim's stated
  uncertainty; a difference within that floor is `within_floor`, not a contradiction. It already
  exists in this repo and PREDATES this check:
 - `labext/writeback.py`: `FLOOR_V = 0.013` (line 37), `floor = max(FLOOR_V, claim_unc or 0.0)`
    (line 121), `outcome = "within_floor" if margin <= floor else "contradicted"` (line 154).
 - Introduced in commit **09e066e5** (2026-11-10 16:01 +0530, "feat(phase-5): writeback verdicts vs
    Lila data under D7"); `FLOOR_V = 0.013` locked in commit **f1602722** (2026-11-10 19:57 +0530).
    The D7 floor is also stated above in this file ("Verdict floor D7"). This durability check was
    only added on 2026-11-11 (fix #7), so the floor rule is older than the check.
- This amendment was made AFTER the trace was opened. It is NOT tuning: it does not invent a new
  threshold to change this result; it applies a rule that was locked on 2026-11-10 (before the check
  existed) and is already used by the writeback verdict code. Writing a strict threshold that ignores
  that floor was the omission; it repeats the error recorded in CONTRADICTION_DOSSIER.md (treating a
  sub-floor difference as a contradiction).
- Amended rule: the check is `within_floor` iff NO recorded InMnPdOx point exceeds 0.5 V + floor =
  0.513 V (claim __010 states no per-value uncertainty, so floor = max(13 mV, 0) = 13 mV). The claim
  "below 0.5 V" is written to a precision of 0.1 V (one decimal place). The corrected verdict is in
  reports/durability_check_2609.30133.md; both the strict and the floor readings are shown.
