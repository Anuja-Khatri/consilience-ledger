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

## 2026-11-11: correction pass (fixes 1-7; local only, not pushed)
Full per-fix detail in FIXES_REPORT.md. Summary of material corrections:

1. **Dataset misattribution.** Six+ files said the simulator replays "Lila's real recorded data".
   Established from helao-async's own files (cpsim_driver.py: "the OER `oer13_cps` dataset ... a
   pickled OER measurement library ... replays stored CP traces"; LICENSE.md: MIT,
   High-Throughput-Experimentation) that `oer13_cps` is the PUBLIC dataset shipped in helao-async,
   a combinatorial OER CP library over **13 base metals** (Ca,Ce,Co,Cu,Fe,La,Mg,Mn,Ni,Sb,Sn,Ta,Zn;
   **no palladium**), present on this machine. Corrected run_loop.py, generate.py, loop/__init__.py,
   PROVENANCE.md, LIMITATIONS.md, OPEN_QUESTIONS.md (OQ-3), STATE.md, CHECKPOINT2.md, and
   regenerated loop/{runs,cards,plans,dossiers}. Net effect on OQ-3: Phase 10 is NOT blocked by the
   missing-Lila-data gap (it runs on public data); only Phase 5 is.
2. **Synthetic example wording.** The loop pairs two DIFFERENT materials, so it is not a
   claim-vs-claim disagreement. Relabelled everywhere as a "synthetic simulator-lookup example";
   the outcome label `fork_confirmed` is replaced by `lookup_two_materials_differ` /
   `lookup_two_materials_within_floor` (no fork claim). test_loop_run.py updated to match.
3. **Stale text.** README: removed "Stage 3 scaffolding in place", "Phases 10-11 scaffolding",
   "Nothing is published"; status now states Phase 10 ran on public data and Phase 11 is NOT YET RUN.
   LIMITATIONS.md: removed the stale "Extraction has not run" and "Provisional claims (until
   Checkpoint 1 returns)" lines (extraction DID run: 34 real claims; Checkpoint 1 is resolved).
4. **Discovery report.** The Phase 11 search fed long sentences into a keyword engine, was
   rate-limited to 4 queries, and returned 5 unrelated particle-physics/astrophysics papers; it did
   not execute meaningfully. Rewrote discovery/report/report.md, README, LIMITATIONS, STATE,
   CHECKPOINT2 to status "NOT YET RUN" — not a NULL result, not a result about durability. Search
   NOT rerun.
5. **Rule citations.** Ported the Gate-1-approved page-level citations from ../ledger-v2
   (r0/GATE1.md, source B2 = PMC13707403, Molecules 2026) into rules/SOURCES.md and the yaml
   `source` fields, matched BY FIELD (note CR3/CR4 are numbered oppositely in ledger-v2). Numbering,
   fields, predicates, tolerances UNCHANGED, so **no verdict changed** (0 forks, 561 vetoes, 9
   verdicts byte-identical). Because `source` is inside the hash-locked rules model, version was
   bumped documentation-only **comparability-v0 -> v0.1** (rules/CHANGELOG.md); the regenerated
   hashes are **rules.lock sha cc251d77… -> ba3db7c1…** and **ledger.hash f42d48c1… -> a11ee946…**
   (re-locked; `make reproduce` byte-stable at the new values).
6. **Safety seed.** Wrote PROPOSED (not activated) safety_format/seed/registry_proposed.yaml with
   an exact public citation per rule (Prudent Practices in the Laboratory, NRC 2011; OSHA 29 CFR
   1910.1450) or an explicit `generic` label for instrument bounds (Lila's paper states operating
   VALUES, not protection ceilings). Harmless; the dual-use denylist scan passes (test extended to
   cover the proposed file). SEED_APPROVAL.md written (one row per rule); safety_format/TIER_POLICY.md
   marked AWAITING ANU'S WORDING. Active registry.yaml unchanged.
7. **Skipped durability check (claim 2609.30133__010).** Preregistered the pass rule in
   PREREGISTRATION.md BEFORE opening the trace, then ran it against the authors' own released H-cell
   trace (upstream/lila_oer_manuscript/data/fig_3e.csv, sha cac02293…). Result: **FAIL** of the
   strict rule — InMnPdOx grazes 0.5055 V at 575.5 h (one point ~5.5 mV above the claimed 0.5 V
   ceiling) over 11.5-999.6 h coverage. Reported as a CONSISTENCY CHECK between the authors' claim
   and their own data, NOT independent confirmation (reports/durability_check_2609.30133.md).
