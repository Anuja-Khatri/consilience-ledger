# Gate 2 decisions (Anu, 2026-11-11) - transcribed

Applied by tools/apply_gate2.py -> r2_out/approved/ (6 cards), r2_out/gate2_decisions.json.

## Pilot adjudications
- Agreed cards: ACCEPT both (PMC12606313 agreed0/agreed1). Mechanical correction applied: a
  stated ir_correction.fraction always carries its quote; source_quote filled from the source
  sentence where the model left it empty.
- PMC12606313_contested_2, _3: APPROVE, material corrected to "Ir/IrOx (commercial)" on both.
- PMC12606313_contested_0, _1: REJECT (twins of _2/_3).
- PMC13459051_contested_0: APPROVE, activity_hold_hours set to null (the 500 h is a separate
  stability claim at a different current, not a condition of the 196 mV measurement).
- PMC13459051_contested_1: REJECT - electrolyte falsely attributed from a synthesis-washing
  Methods sentence, which is never a measurement-electrolyte source.
- PMC13550445_contested_0: APPROVE, activity_hold_hours set to null (650 h is at 100 mA/cm2, a
  separate claim).
- PMC13550445_contested_1: REJECT (twin of _0).
Result: 6 approved seed cards (2 agreed + 4 approved contested).

## Standing decisions for the K=40 harvest
- Agreement knob: UNCHANGED (as signed under S2).
- Harvest depth K = 40: 20 papers in Pd-HClO4 (including all 18 at 1 M HClO4) + 20 in Co-H2SO4.
- Three preregistered extraction amendments (recorded in rules/CHANGELOG.md): A1 material-name
  canonicalization before agreement; A2 a duration at a different current density or coupled by
  "together with" becomes its own claim, never a condition; A3 electrolyte Methods attribution
  restricted to electrochemical-measurement context. Commercial baselines (RuO2, IrO2, Ir/IrOx,
  Pt) explicitly in scope.

Each of the four contested approvals above is exactly what amendments A1-A3 now automate: the
Ir/IrOx-vs-"Ir/IrOx (commercial)" split (A1), the 500 h / 650 h durations wrongly attached (A2),
and the synthesis-washing electrolyte (A3). The amendments are validated against Anu's hand
decisions before the harvest runs.
