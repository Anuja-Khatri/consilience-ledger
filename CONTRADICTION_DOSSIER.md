# CONTRADICTION DOSSIER

Written before Checkpoint 2 sign-off to audit the two "contradicted" writeback rows.
Finding: both rested on a screening-tier comparison against unstated conditions and on a
catalyst system with no H-cell data. Per the rules they are reclassified to
`not_comparable` (published vetoes). The writeback was corrected to use the H-cell data
for verdicts and the screening data for veto demonstrations only. Not published.

## Root cause
The verdicts were computed against `oer_exp_data.csv`, column
`overpotential_cp1_600s_mean`. That is the CP1 600-second hold: a SCREENING-tier
measurement (fig_2c/fig_3a in the manuscript scripts), explicitly comparative, not
absolute (II.3). The H-cell verdict data is `fig_3e.csv` ("iR-corrected long-term HCell
OER overpotential", fig_3e.py), which contains only InMnPdOx, NiTaPdOx, PdOx, RuOx. The
ruling is that writeback uses H-cell verdicts plus published vetoes only. Using screening
data to contradict a claim violates both the ruling and the comparative-not-absolute
framing.

Data shas (loaded at runtime, not committed, CC-28):
- screening `oer_exp_data.csv` sha256 `ab33c747883b5dce...`
- H-cell `fig_3e.csv` sha256 `cac022933ff17b84...`
- manuscript commit `92a773790b684786cb8956e3c2cac668043850cb`

---

## Row 1: `V_2609.30133__020` (CoFeZrOx)

**Claim card.** id `2609.30133__020`; kind performance_value; axis
overpotential_at_current_density; subject CoFeZrOx; quantity 0.55 V (bound exact).
Source sentence: "The most active were consistently Co-rich and Zr-containing, clustering
near Co78In12Zr10Ox and Co86Fe7Zr7Ox (CoInZrOx and CoFeZrOx), reaching 0.55 V at 10 mA
cm-2 ...".
Conditions: current_density 10 mA/cm^2 (geometric); electrolyte **unstated**;
ir_correction **unstated**; temperature **unstated**; protocol_tier **unstated**; all
others unstated.

**Matched data row (old, screening).** `oer_exp_data.csv` rows 612-616 for the
`['Co','Fe','Zr']` screening system, sha `ab33c747883b5dce...`, measured best 0.5365 V.
**H-cell data (fig_3e.csv): NONE.** The H-cell set has only InMnPdOx, NiTaPdOx, PdOx,
RuOx. There is no CoFeZr H-cell measurement.

**Protocol tier.** Claim: unstated. Data used (old): screening (CP1 600s). H-cell: not
available. **Floor applied:** 0.013 V (13 mV). Old margin 0.0135 V, which is 0.5 mV over
the floor. A verdict that flips on half a millivolt, drawn from comparative screening
data, is exactly the case the floor and the veto exist to stop.

**Conditions compared.** electrolyte: claim unstated vs data not recorded -> unstated;
current_density: claim 10 vs screening geometric; temperature: unstated both;
ir_correction: claim unstated vs screening not recorded. The electrolyte and
iR-correction are unstated on at least one side.

**Framing check.** Comparative-not-absolute: FAILED (a screening number was used as an
absolute reference to contradict). H-cell-verdicts-only ruling: FAILED (screening data,
not H-cell). Conditions veto: the claim has unstated electrolyte and iR status.

**Reclassification.** `not_comparable`, defect `no_hcell_data: CoFeZr`. Published veto.

---

## Row 2: `V_2609.30133__021` (CoInZrOx)

**Claim card.** id `2609.30133__021`; performance_value;
overpotential_at_current_density; subject CoInZrOx; 0.55 V. Same source sentence as Row 1
(the two catalysts are reported together). Conditions: current_density 10 mA/cm^2
(geometric); electrolyte, ir_correction, temperature, protocol_tier all **unstated**.

**Matched data row (old, screening).** `oer_exp_data.csv` rows 744-748 for
`['Co','In','Zr']`, sha `ab33c747883b5dce...`, measured best 0.5323 V. **H-cell data:
NONE** (no CoInZr H-cell measurement).

**Protocol tier.** Claim unstated; data used (old) screening; H-cell unavailable. **Floor
0.013 V.** Old margin 0.0177 V (4.7 mV over the floor), again off comparative screening
data.

**Conditions compared.** Same as Row 1: electrolyte and iR-correction unstated;
current_density 10 vs screening geometric; temperature unstated.

**Framing check.** Comparative-not-absolute: FAILED. H-cell-verdicts-only: FAILED.
Conditions veto: unstated electrolyte and iR status.

**Reclassification.** `not_comparable`, defect `no_hcell_data: CoInZr`. Published veto.

---

## Consistency: the InMnPdOx row was also reclassified
The former single `within_floor` row (`V_2609.30133__003`, InMnPdOx 0.45 V) had the same
root cause: it matched the claim to the screening best (0.45 V) with margin 0.1 mV. Against
the correct H-cell data it is `not_comparable`: the claim is "not iR-corrected" while the
H-cell data is iR-corrected (defect `condition_mismatch: CR4`), and the H-cell electrolyte
and current density are not in the file so they are unstated (never inferred, D10). It is
now a published veto, consistent with Rows 1 and 2.

## Corrected verdict distribution
Before: 1 within_floor, 2 contradicted, 6 not_comparable.
After: **0 within_floor, 0 contradicted, 9 not_comparable (all published vetoes).** No
approved claim's conditions were proven comparable to an H-cell measurement, so no
confirm/contradict verdict is issued. This respects the comparative-not-absolute framing
and the H-cell-verdicts-only ruling, and it matches the ledger's veto-dominated result
(CC-21). See `ledger/verdicts.json` and `reports/verdicts.md`.

## Exact wording changed
METHODS.md (before):
> Result over the 34 approved claims: 1 within_floor (their InMnPdOx claim reproduced by
> their own data to 0.1 mV), 2 contradicted (just over the floor), 6 not_comparable
> (including every published pure-Pd claim).

METHODS.md (after):
> Result over the 34 approved claims: 0 confirmed, 0 contradicted, 9 not_comparable (all
> published vetoes). Verdicts use the H-cell data (fig_3e.csv, iR-corrected long-term);
> the CP1 600s screening data is comparative, not absolute, and is used only to
> demonstrate vetoes. No claim's conditions were proven comparable to an H-cell
> measurement (no H-cell data for the system, an iR-correction or tier mismatch, or an
> unstated electrolyte), so no claim is confirmed or contradicted.

README.md (before):
> their InMnPdOx claim is reproduced by their own measurement within the floor; the
> published pure-Pd claims have no comparable Lila measurement and are published vetoes.

README.md (after):
> every writeback comparison is a published veto: no claim's conditions were proven
> comparable to Lila's H-cell measurement (the screening data is comparative, not
> absolute, and is not used to confirm or contradict). The published pure-Pd claims are
> among the vetoes.

This correction is recorded in CORRECTIONS.md.
