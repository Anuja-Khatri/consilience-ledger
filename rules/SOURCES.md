# Comparability rule sources

Candidate comparability parameters and tolerances with citations, feeding the
`comparability_rules.yaml` draft. Rules are default-deny: a pair is comparable only if
every rule's field is stated on both claims and the predicate passes (IV.2).

The empirical basis for a conditions veto in acidic OER is ESAMP (Statt, Rohr, Brown,
Guevarra, Hummelshoj, Hung, Anapolsky, Gregoire, Suram; Digital Discovery 2023, 2, 1078):
overpotential prediction error drops from 143 mV to 25 mV when condition parameters enter.
Its state-equivalency rules are the published ancestor of this veto.

## Rule basis (v0)
| Rule | Field | Predicate | Basis | Citation status |
|---|---|---|---|---|
| CR1 | electrolyte | identity + concentration equal | Electrolyte identity and concentration set the reaction environment; ESAMP groups states by them. | ESAMP (Digital Discovery 2023, 2, 1078); page-level cite PENDING (ESAMP ESI not yet downloaded). |
| CR2 | current_density | equal within 0, same normalisation | Overpotential is reported at a current density; geometric vs ECSA are not interchangeable (CC-06). | ESAMP overpotential-at-current-density definition; page-level cite PENDING. |
| CR3 | temperature | equal (room_temperature enum, CC-12) | Temperature shifts kinetics; room_temperature is an enum, never a number (D10). | General electrochemistry; page-level cite PENDING. |
| CR4 | ir_correction | both corrected or both not | iR correction changes the reported overpotential materially. | ref 27 (Hochfilzer 2023, ACS Energy Lett) protocol discussion; PDF PENDING (paywalled check). |

## Accessible sources used so far
- Their paper (arXiv:2609.30133), downloaded and ingested; reports overpotentials at
  stated current densities in acid with iR-correction status, and stability metrics.
- ref 40 Peng 2023 (National Science Review, OA), downloaded and ingested.

## Pending downloads for Phase 3 sourcing (III.4.4)
- ESAMP ESI (RSC, open access) for the state-equivalency parameter list and tolerances.
- refs 4 (Wei 2023 ACS Catal), 27 (Hochfilzer 2023 ACS Energy Lett), 15, 16: attempt OA;
  mark excluded_inaccessible if paywalled (D16). Page-level citations are added when the
  source text is in hand; until then the rules are PROVISIONAL and labeled so.
