# Verdicts (writeback against Lila's instrument data)

Data loaded at runtime from oer_exp_data.csv (CC-BY, not committed, CC-28), sha `ab33c747883b5dce...`, cited by row index.

Outcomes: {'within_floor': 1, 'not_comparable': 6, 'contradicted': 2}

| verdict | subject | claim V | measured best V | margin | outcome |
|---|---|---|---|---|---|
| V_2609.30133__003 | InMnPdOx | 0.45 | 0.4501 | 0.0001 | within_floor |
| V_2609.30133__004 | RuOx | 0.41 | - | None | not_comparable |
| V_2609.30133__020 | CoFeZrOx | 0.55 | 0.5365 | 0.0135 | contradicted |
| V_2609.30133__021 | CoInZrOx | 0.55 | 0.5323 | 0.0177 | contradicted |
| V_2609.30133__023 | Pd-rich, non-annealed oxide compositions with either In-Mn or Ni-Ta as additives | 0.46 | - | None | not_comparable |
| V_ref40_peng2023__013 | PdCoO2 precursor (without etching) | 0.528 | - | None | not_comparable |
| V_ref40_peng2023__022 | Pd-55 | 0.196 | - | None | not_comparable |
| V_ref40_peng2023__033 | Pd-25 | 0.348 | - | None | not_comparable |
| V_ref40_peng2023__034 | Pd-40 | 0.28 | - | None | not_comparable |

Every not_comparable row is a published veto: Lila has no comparable measurement for that catalyst/condition set. This is expected (CC-21).
