# Human Review Dossier: Discriminate overpotential_at_current_density: SYN:xasOnly vs SYN:xasRef

_SIM-NOT-CHEMISTRY: OERSIM replays recorded data. A simulated outcome is not a chemical measurement and licenses no chemical claim._

- Fork: `SYN3|plan_only`  |  Axis: `overpotential_at_current_density`  |  Status: **plan_only**
- Discriminating power: **weak**  |  Cost: $10K  |  Timeline: days
- Predicted split: 0.02 (floor 0.013)


**WEAK DISCRIMINATING POWER (CC-27): this experiment may not decide the question.**

## The two claims

- A (SYN3A): > SYNTHETIC worked example: SYN:xasOnly is claimed to show 0.4 V overpotential.
- B (SYN3B): > SYNTHETIC worked example: SYN:xasRef is claimed to show 0.42 V overpotential.

## Experiment design

- Hypothesis: SYN:xasOnly and SYN:xasRef differ in overpotential_at_current_density under the shared conditions.
- Manipulated variable: catalyst identity
- Discriminating observable: overpotential_at_current_density
- Instrument: synchrotron_xas (exists: True; lab-gate OERSIM (cp chronopotentiometry); replays recorded data)
- Protocol: Measure overpotential_at_current_density for both catalysts at the shared current density and electrolyte, compare the difference against the 0.013 floor.
- If match holds: the two values agree within the floor; the disagreement dissolves
- If match fails: the two values differ beyond the floor; the disagreement is real
- Controls: same electrolyte, current density, temperature, and iR-correction as both claims

## Falsification

If the measured overpotential_at_current_density values agree within the floor, the disagreement is not real.

Who could run this: an acidic-OER electrochemistry lab (RDE or SFC)
Sources bridged: SYNTHETIC, SYNTHETIC
