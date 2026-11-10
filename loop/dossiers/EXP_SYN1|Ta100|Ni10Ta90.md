# Human Review Dossier: Discriminate overpotential_at_current_density: SYN:Ta100 vs SYN:Ni10Ta90

_SIM-NOT-CHEMISTRY: OERSIM replays recorded data. A simulated outcome is not a chemical measurement and licenses no chemical claim._

- Fork: `SYN1|Ta100|Ni10Ta90`  |  Axis: `overpotential_at_current_density`  |  Status: **ready**
- Discriminating power: **strong**  |  Cost: $10K  |  Timeline: days
- Predicted split: 0.0281 (floor 0.013)


## The two claims

- A (SYN1A): > SYNTHETIC worked example: SYN:Ta100 is claimed to show 0.4054 V overpotential.
- B (SYN1B): > SYNTHETIC worked example: SYN:Ni10Ta90 is claimed to show 0.3773 V overpotential.

## Experiment design

- Hypothesis: SYN:Ta100 and SYN:Ni10Ta90 differ in overpotential_at_current_density under the shared conditions.
- Manipulated variable: catalyst identity
- Discriminating observable: overpotential_at_current_density
- Instrument: cp_chronopotentiometry (exists: True; lab-gate OERSIM (cp chronopotentiometry); replays recorded data)
- Protocol: Measure overpotential_at_current_density for both catalysts at the shared current density and electrolyte, compare the difference against the 0.013 floor.
- If match holds: the two values agree within the floor; the disagreement dissolves
- If match fails: the two values differ beyond the floor; the disagreement is real
- Controls: same electrolyte, current density, temperature, and iR-correction as both claims

## Falsification

If the measured overpotential_at_current_density values agree within the floor, the disagreement is not real.

Who could run this: an acidic-OER electrochemistry lab (RDE or SFC)
Sources bridged: SYNTHETIC, SYNTHETIC
