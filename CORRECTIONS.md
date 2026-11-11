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
   CHECKPOINT2 to status "NOT YET RUN" - not a NULL result, not a result about durability. Search
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
   trace (upstream/lila_oer_manuscript/data/fig_3e.csv, sha cac02293…). InMnPdOx: 84 points, max
   0.5055 V at 575.5 h, coverage 11.5-999.6 h. **Verdict (corrected 2026-11-11, see below): within_floor**
 - the first rule was written strict and omitted the standing 13 mV floor; under the floor, 0 points
   exceed 0.513 V so the claim is consistent within ±13 mV. CONSISTENCY CHECK vs the authors' own data,
   NOT independent confirmation (reports/durability_check_2609.30133.md).

## 2026-11-11: durability check (fix #7) omitted the standing floor - verdict corrected to within_floor
- What was wrong: the pass rule for the claim-2609.30133__010 durability consistency check was written
  STRICT (every trace point below 0.5 V; "FAIL" if any point >= 0.5 V). It omitted the standing
  verdict-floor rule (D7: threshold = max(13 mV, the claim's stated uncertainty)), which was locked on
  2026-11-10 - before this check existed - in `labext/writeback.py` (`FLOOR_V = 0.013`,
  `floor = max(FLOOR_V, claim_unc)`, `within_floor if margin <= floor`; commits 09e066e5 2026-11-10
  16:01 and f1602722 2026-11-10 19:57) and is already used by the writeback verdict code. A strict
  threshold contradicts that floor and repeats the error recorded in CONTRADICTION_DOSSIER.md
  (treating a sub-floor difference as a contradiction).
- Correction: amended the preregistration (dated 2026-11-11, after the trace was opened; not tuning - 
  it applies a rule locked earlier) and recomputed under the floor. InMnPdOx max = 0.5055 V at 575.5 h;
  1 point exceeds 0.500 V; **0 points exceed 0.513 V** (0.5 V + 13 mV floor); coverage 11.5-999.6 h;
  claim written to 0.1 V precision. **Verdict: within_floor - consistent within the authors' stated
  ±13 mV reproducibility.** The strict reading is kept on record but superseded. The word "FAIL" for
  this check was replaced in reports/durability_check_2609.30133.md and FIXES_REPORT.md; the label
  (consistency check vs the authors' own data, not independent confirmation) is unchanged.
- Repo sweep: searched for any wording that a Lila claim fails / is contradicted / is wrong. The only
  unsupported hits were this check's "FAIL" (now corrected). Other hits are correct: "0 contradicted"
  verdicts; the CONTRADICTION_DOSSIER "FAILED" framing-checks (the ENGINE's prior behavior, already
  corrected, not a claim); and the verbatim paper quote "both failed medium-term acidic stability
  screening" (the authors' own words, left as-is).
- Test: `tests/test_durability_floor.py` asserts the check applies the 13 mV floor (within_floor at
  0.5055 V) and that no InMnPdOx point exceeds 0.513 V.

## 2026-11-11: follow-up corrections (self-consistency label, public repo, stale status, em dashes)
- Durability report (reports/durability_check_2609.30133.md): added a "Basis of comparability" section
  stating the verdict rests on IDENTITY (the claim is the authors' own description of the same Fig. 3e
  measurement, so claim and data are one experiment); labelled it a "self-consistency check". Noted
  that under the ordinary cross-source rules this pair would be refused as condition_unstated
  (electrolyte and current density unstated on the data side), which is why the 9 writeback comparisons
  were refused while this check is not. The paper's long-term-test Methods text is not committed, so
  those conditions remain unstated here.
- README.md: removed "publishing is not performed here"; stated the repo is public
  (github.com/Anuja-Khatri/consilience-ledger). Added a one-line durability self-consistency check to
  Results (max 0.5055 V at 575.5 h, 0 of 84 points above 0.513 V, within_floor, consistent within
  +/- 13 mV). Registered those numbers in NUMBERS_LOCK.json with n and qualifier so the numbers linter
  passes (README lints clean).
- STATE.md: replaced the stale "Phases 10-11 scaffolding" line with the true status (Phase 10 ran on
  public data; Phase 11 NOT YET RUN). CHECKPOINT2.md: added a top banner marking it a historical record,
  superseded by README and CORRECTIONS.md where they conflict.
- Em dashes: replaced every em dash (U+2014) with plain punctuation in README, FIXES_REPORT,
  CORRECTIONS, the durability report, discovery/report/report.md, and (for the test scope) OPEN_QUESTIONS,
  PREREGISTRATION, SEED_APPROVAL, STATE. Added tests/test_no_em_dash.py, which fails if an em dash appears
  in any top-level .md file or under reports/ or discovery/report/.
- No verdict or hash changed: ledger.hash and rules.lock are unchanged (docs + tests only). 75 tests
  green; make reproduce byte-stable.

## 2026-11-11: database and round-robin corrections (C-001 to C-007), merged for the public record
These corrections come from the later database and round-robin rounds; full detail is in
`rounds/round4-database/CORRECTIONS.md` and `rounds/round5-roundrobin/REPORT.md`. Reworded here per
consolidation rule 2: the superseded median-floor fork counts are described in words only and their
digits are not printed anywhere in this repo.

- A superseded intermediate database round used a median-floor fork rule that did not control false
  discoveries and did not separate same-source replicate inconsistency from cross-source forks. Its
  draft fork counts are superseded and are not quoted; the corrected finding is that MPS is a single
  dataset and pipeline (cross-source fork count is zero) and the enzyme sets are untestable, never
  "zero forks".
- C-001 (2026-11-11): the physical ceiling on suspect measurements was too tight and wrongly flagged
  real but poor catalysts; the bound was raised (values confirmed to be in volts, so a bound error,
  not a units error).
- C-002 (2026-11-11): the raised ceiling was still too permissive; every apparent replicate
  inconsistency under it was a normal value paired with a lone compliance-rail value, so the ceiling
  was lowered and no genuine replicate inconsistency survived the false-discovery control.
- C-003 (2026-11-11): the eye-chosen ceiling was replaced by each row's own recorded instrument
  compliance limit; on the MPS test half this gives not comparable 74,569, within floor 80,144,
  replicate inconsistency 0, fork 0, suspect transcription 16,613.
- C-004 (2026-11-11): the vendored OERSIM was mislabelled acidic; it is alkaline (OER13, pH 13), so
  an acid disagreement cannot be settled on it and the round-robin fork in 1 M KOH stays plan_only.
- C-005 (2026-11-11): an earlier pass marked the per-lab spread condition as met; the machine read
  shows the per-lab error bars are at or below the raster resolution, so the condition is not met and
  the round-robin spread sweep values are not pre-registered.
- C-006 (2026-11-11): the round-robin forks at the headline setting are fragile to the per-lab spread
  assumption; a single noisy laboratory at 30 mV erases all of them.
- C-007 (2026-11-11): the round-robin headline was corrected to "0 to 4 forks at s = 15 mV" with its
  full qualifier, and the result to lead with is the robust inter-lab central range of 90.7 mV
  (n = 9). No computed number moved; only the presentation changed.
- C-008 (2026-11-11): on a clone without the never-committed H-cell data (CC-28), `make reproduce`
  ran writeback, which overwrote the committed `ledger/verdicts.json` with an empty list and shrank
  `reports/verdicts.md`, breaking the published fresh-clone byte-stability for exactly the reader the
  front page invites to clone and check; no drift occurred with the data present, which is why earlier
  checks passed. Found by the post-push fresh-clone verification. Writeback now skips without writing
  when the data is absent, mirroring the two tests that already skip for the same reason; verified
  byte-stable on a dataless fresh clone.
