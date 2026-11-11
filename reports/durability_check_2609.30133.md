# Durability consistency check — claim 2609.30133__010 (fix #7)

**This is a CONSISTENCY CHECK between the authors' claim and the authors' OWN released data — same
authors, same iR-corrected measurement. It is NOT independent confirmation.**

## Claim under test
> "InMnPdOx is the most stable, sustaining an overpotential below 0.5 V over 1,000 h" (arXiv:2609.30133,
> claim `2609.30133__010`).

## Pass rule (preregistered BEFORE the trace was opened — see PREREGISTRATION.md)
PASS iff the InMnPdOx iR-corrected overpotential in the released trace is strictly below 0.5 V at
EVERY recorded point; FAIL iff any recorded point is >= 0.5 V; INCONCLUSIVE iff no InMnPdOx system or
no time axis. 0.5 V is the claim's own threshold; no extra floor applied.

## Trace and its conditions (attributed from the authors' own released artifact, quoted)
- File: `upstream/lila_oer_manuscript/data/fig_3e.csv`, sha256 `cac022933ff17b84…`
  (columns: `material_system, plot_x_hr, has_blue_marker, overpotential_corrected_avg`).
- Authors' own description of this trace, quoted verbatim from their figure script
  `upstream/lila_oer_manuscript/scripts/fig_3e.py`:
  > "Fig 3e — iR-corrected long-term HCell OER overpotential vs time, per catalyst."
- Conditions so attributed: **iR-corrected = yes**; measurement = **long-term H-cell OER
  overpotential vs time** (protocol tier long_term). **Electrolyte and current density are NOT
  stated in the released trace or figure script, so they stay unstated (not inferred, D10).** The
  paper's full Methods text is not in the committed corpus, so finer conditions remain unstated.

## Result — FAIL (not strictly consistent)
- InMnPdOx trace: 84 recorded points, time coverage **11.5 h → 999.6 h** (≈ the stated 1,000 h).
- Overpotential range **0.4104 V → 0.5055 V**.
- **Maximum = 0.5055 V at 575.5 h**, which is **≥ 0.5 V** (one point, ~5.5 mV above the ceiling).
- By the preregistered strict rule, the check **FAILS**: the released trace contains a point above
  the claimed 0.5 V ceiling within 1,000 h, so the claim "below 0.5 V over 1,000 h" is **not strictly
  consistent** with the authors' own data. The exceedance is small (~5.5 mV at one point near the
  mid-run), and the claim itself notes the 1,000 h figure rests on "repeated measurements over a
  partial duration on planar and porous supports" (Figs. S4–S6).

**Interpretation:** the authors' own long-term H-cell trace very nearly supports their "below 0.5 V"
durability claim, but grazes just above 0.5 V once (0.5055 V, 575.5 h). This is reported as a
consistency finding against their own data, not as independent confirmation or refutation of the
catalyst's durability.

## Reproduce
```
python - <<'PY'
import csv
rows=list(csv.DictReader(open('upstream/lila_oer_manuscript/data/fig_3e.csv')))
v=[(float(r['plot_x_hr']),float(r['overpotential_corrected_avg'])) for r in rows if r['material_system']=='InMnPdOx']
print('max eta', max(e for _,e in v), 'at', [t for t,e in v if e==max(e for _,e in v)][0],'h; any>=0.5:', any(e>=0.5 for _,e in v))
PY
```
