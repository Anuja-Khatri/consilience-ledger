# Human Review Dossier: Discriminate overpotential_at_current_density: SYN:Ni100 vs SYN:Co10Fe40La50

_SIM-NOT-CHEMISTRY: OERSIM replays the public oer13_cps dataset shipped in helao-async (13 base metals, no palladium); not Lila's data. A simulated outcome is not a chemical measurement and licenses no chemical claim._

- Synthetic simulator-lookup example (two different materials; NOT a fork/disagreement): `SYN2|Ni100|Co10Fe40La50`  |  Axis: `overpotential_at_current_density`  |  Status: **ready**
- Discriminating power: **weak**  |  Cost: $10K  |  Timeline: days
- Lookup margin: 0.0109 (floor 0.013)


**WEAK DISCRIMINATING POWER (CC-27): this experiment may not decide the question.**

## The two claims

- A (SYN2A): > SYNTHETIC simulator-lookup example: SYN:Ni100 shows 0.3696 V overpotential in the public oer13_cps dataset.
- B (SYN2B): > SYNTHETIC simulator-lookup example: SYN:Co10Fe40La50 shows 0.3805 V overpotential in the public oer13_cps dataset.

## Experiment design

- Hypothesis: SYN:Ni100 and SYN:Co10Fe40La50 differ in overpotential_at_current_density under the shared conditions.
- Manipulated variable: catalyst identity
- Discriminating observable: overpotential_at_current_density
- Instrument: cp_chronopotentiometry (exists: True; lab-gate OERSIM (cp chronopotentiometry); replays the public oer13_cps dataset shipped in helao-async (13 base metals, no palladium))
- Protocol: Measure overpotential_at_current_density for both catalysts at the shared current density and electrolyte, compare the difference against the 0.013 floor.
- If match holds: the two values agree within the floor; the disagreement dissolves
- If match fails: the two values differ beyond the floor; the disagreement is real
- Controls: same electrolyte, current density, temperature, and iR-correction as both claims

## Falsification

If the measured overpotential_at_current_density values agree within the floor, the disagreement is not real.

Who could run this: an acidic-OER electrochemistry lab (RDE or SFC)
Sources bridged: SYNTHETIC, SYNTHETIC
