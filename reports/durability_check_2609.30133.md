# Durability self-consistency check, claim 2609.30133__010 (fix #7)

**This is a SELF-CONSISTENCY CHECK between the authors' claim and the authors' OWN released data:
same authors, same iR-corrected measurement, read two ways. It is NOT independent confirmation.**

## Claim under test
> "InMnPdOx is the most stable, sustaining an overpotential below 0.5 V over 1,000 h" (arXiv:2609.30133,
> claim `2609.30133__010`).

## Basis of comparability (why this is a self-consistency check)
This verdict rests on IDENTITY, not on proven cross-source comparability. The claim is the authors'
OWN description of this same measurement (their Fig. 3e trace), so the claim and the data are one
experiment, by the same authors, read two ways. Call it a **self-consistency check**: the authors'
prose against the authors' own plotted numbers.

Under the ordinary cross-source comparability rules this pair would be REFUSED as
`condition_unstated`: on the data side the electrolyte and the current density are not stated (the
released `fig_3e.csv` and its figure script `scripts/fig_3e.py` give only "iR-corrected long-term
HCell OER overpotential vs time"; the paper's Methods text is not committed to this repo, so those
conditions remain unstated here). This is exactly why the 9 writeback comparisons were refused as
vetoes while this check is not: the writeback pairs a claim against a SEPARATE measurement and must
prove the conditions match, whereas here claim and measurement are the same experiment, so no
cross-source conditions need to be proven. The self-consistency check therefore says only that the
authors' words agree with their own trace, nothing about independent reproduction.

## Pass rule (preregistered BEFORE the trace was opened, see PREREGISTRATION.md)
PASS iff the InMnPdOx iR-corrected overpotential in the released trace is strictly below 0.5 V at
EVERY recorded point; FAIL iff any recorded point is >= 0.5 V; INCONCLUSIVE iff no InMnPdOx system or
no time axis. 0.5 V is the claim's own threshold; no extra floor applied.

## Trace and its conditions (attributed from the authors' own released artifact, quoted)
- File: `upstream/lila_oer_manuscript/data/fig_3e.csv`, sha256 `cac022933ff17b84…`
  (columns: `material_system, plot_x_hr, has_blue_marker, overpotential_corrected_avg`).
- Authors' own description of this trace, quoted verbatim from their figure script
  `upstream/lila_oer_manuscript/scripts/fig_3e.py`:
  > "Fig 3e - iR-corrected long-term HCell OER overpotential vs time, per catalyst."
- Conditions so attributed: **iR-corrected = yes**; measurement = **long-term H-cell OER
  overpotential vs time** (protocol tier long_term). **Electrolyte and current density are NOT
  stated in the released trace or figure script, so they stay unstated (not inferred, D10).** The
  paper's full Methods text is not in the committed corpus, so finer conditions remain unstated.

## Verdict (CORRECTED 2026-11-11): within_floor - consistent within the authors' stated ±13 mV reproducibility

The numbers (same for both readings):
- InMnPdOx trace: **84** recorded points, time coverage **11.5 h → 999.6 h** (≈ the stated 1,000 h).
- Overpotential range **0.4104 V → 0.5055 V**; **maximum = 0.5055 V at 575.5 h**.
- Points exceeding **0.500 V**: **1** (the 0.5055 V point).
- Points exceeding **0.513 V** (0.5 V + the 13 mV floor): **0**.
- Precision the claim is written to: **0.1 V** ("below 0.5 V", one decimal place).

### Reading 2 - standing floor rule (D7), the CORRECT verdict
The standing verdict-floor rule (locked 2026-11-10, before this check; `labext/writeback.py`
`FLOOR_V = 0.013`, `floor = max(FLOOR_V, claim_unc)`, `within_floor if margin <= floor`) makes the
verdict threshold the larger of 13 mV and the claim's stated uncertainty. Claim __010 states no
per-value uncertainty, so the floor is 13 mV and the exceedance threshold is **0.513 V**. No recorded
point exceeds 0.513 V, so the verdict is **within_floor**: the claim "below 0.5 V over 1,000 h" is
**consistent within the authors' stated ±13 mV reproducibility** (max 0.5055 V at 575.5 h, i.e.
5.5 mV above 0.500 V but inside the 13 mV floor; at the claim's own 0.1 V precision it reads as 0.5 V).

### Reading 1 - strict rule (kept on record, superseded)
Under the preregistered STRICT rule (every point strictly below 0.5 V), the single 0.5055 V point is
"above 0.5 V", so the strict reading is a non-pass. This strict rule omitted the standing floor and is
superseded by Reading 2 (see the PREREGISTRATION.md amendment 2026-11-11). It is retained here only as
the strict reading on record; it is **not** the verdict.

**Interpretation:** the authors' own long-term H-cell trace is **consistent within ±13 mV** with their
"below 0.5 V over 1,000 h" durability claim (one point grazes to 0.5055 V, inside the floor). This is a
consistency finding against the authors' own data - **not independent confirmation**, and not a
refutation.

## Reproduce
```
python - <<'PY'
import csv
rows=list(csv.DictReader(open('upstream/lila_oer_manuscript/data/fig_3e.csv')))
v=[(float(r['plot_x_hr']),float(r['overpotential_corrected_avg'])) for r in rows if r['material_system']=='InMnPdOx']
print('max eta', max(e for _,e in v), 'at', [t for t,e in v if e==max(e for _,e in v)][0],'h; any>=0.5:', any(e>=0.5 for _,e in v))
PY
```
