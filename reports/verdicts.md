# Verdicts (writeback against Lila's H-cell instrument data)

Verdicts use fig_3e.csv (iR-corrected long-term H-cell overpotential; CC-BY, not committed, CC-28), sha `cac022933ff17b84...`, cited by row index. The CP1 600s screening data is comparative, not absolute, and is used only to demonstrate vetoes, never to confirm or contradict a claim.

Outcomes: {'not_comparable': 9}

| verdict | subject | claim V | measured best V | outcome | why |
|---|---|---|---|---|---|
| V_2609.30133__003 | InMnPdOx | 0.45 | - | not_comparable | condition_unstated:electrolyte; condition_unstated:current_density; condition_unstated:temperature; condition_mismatch:CR4 |
| V_2609.30133__004 | RuOx | 0.41 | - | not_comparable | condition_unstated:electrolyte; condition_unstated:current_density; condition_unstated:temperature; condition_mismatch:CR4 |
| V_2609.30133__020 | CoFeZrOx | 0.55 | - | not_comparable | no_hcell_data:CoFeZr |
| V_2609.30133__021 | CoInZrOx | 0.55 | - | not_comparable | no_hcell_data:CoInZr |
| V_2609.30133__023 | Pd-rich, non-annealed  | 0.46 | - | not_comparable | no_hcell_data:InMnNiPdTa |
| V_ref40_peng2023__013 | PdCoO2 precursor (with | 0.528 | - | not_comparable | no_hcell_data:CoPd |
| V_ref40_peng2023__022 | Pd-55 | 0.196 | - | not_comparable | condition_unstated:electrolyte; condition_unstated:current_density; condition_unstated:temperature; condition_unstated:ir_correction |
| V_ref40_peng2023__033 | Pd-25 | 0.348 | - | not_comparable | condition_unstated:electrolyte; condition_unstated:current_density; condition_unstated:temperature; condition_unstated:ir_correction |
| V_ref40_peng2023__034 | Pd-40 | 0.28 | - | not_comparable | condition_unstated:electrolyte; condition_unstated:current_density; condition_unstated:temperature; condition_unstated:ir_correction |

Every not_comparable row is a published veto: the claim's conditions were not proven comparable to an H-cell measurement (no H-cell data for the system, a tier or iR-correction mismatch, or an unstated electrolyte). This respects the comparative, not absolute framing (II.3) and the H-cell-verdicts-only ruling. Expected (CC-21).
