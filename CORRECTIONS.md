# CORRECTIONS

Material corrections to published numbers or claims, with dates and reasons.

## 2026-11-10: writeback used screening data instead of H-cell data (corrected before Checkpoint 2)
- What was wrong: Phase 5 writeback computed verdicts against `oer_exp_data.csv`
  (`overpotential_cp1_600s_mean`), which is the CP1 600-second hold, a SCREENING-tier
  measurement that is comparative, not absolute (II.3). This produced 1 within_floor and
  2 contradicted verdicts (CoFeZrOx, CoInZrOx), both just over the 13 mV floor.
- Why it was wrong: the ruling is that writeback uses H-cell verdicts plus published vetoes
  only. The H-cell data is `fig_3e.csv` (iR-corrected long-term H-cell overpotential). Using
  screening data to contradict a claim violates the ruling and the comparative-not-absolute
  framing. The two contradicted systems have no H-cell data at all, and their claims leave
  electrolyte and iR-correction unstated.
- Correction: writeback now uses `fig_3e.csv` for verdicts and treats the screening CSV as
  veto-demonstration only. A verdict is issued only when the claim's conditions are proven
  comparable to the H-cell measurement. Result: 0 confirmed, 0 contradicted, 9
  not_comparable (all published vetoes). The two contradictions are reclassified to
  `not_comparable` (`no_hcell_data`); the InMnPdOx within_floor is reclassified to
  `not_comparable` (iR-correction mismatch and unstated electrolyte). Full audit in
  CONTRADICTION_DOSSIER.md. METHODS, README, LIMITATIONS, and NUMBERS_LOCK updated.
