# LIMITATIONS

Known limits, recorded as they arise (spec II.3, Phase 7 formalizes this).

- Figure-only data is not extracted in v1 (D9). Text and tables only.
- Corpus accessibility: paywalled papers are marked `excluded_inaccessible` with the
  access attempt recorded (D16). No paywalled content is ever scraped.
- Comparability rules v0 are PROVISIONAL. The sourced, page-cited rule set is drafted
  in Phase 3 from ESAMP ESI and refs 4, 27, 15, 16.
- Extraction has not run: no API key was present in the build environment (OQ-2).
  All non-API Phase 2 work proceeds first; extraction stability (a materials number)
  is unmeasured until keys are available and is reported fresh when measured (II.3).
- Provisional claims: until Anu's Checkpoint 1 batch returns, downstream outputs run
  on AGREED-PROVISIONAL claims only and are labeled PROVISIONAL.
- Mechanism (non-quantitative) comparison uses the structural judge path only; the
  conditions veto does not apply to it (CC-14).
- Safety seed (Phase 9): the instrument protection bounds use generic public values
  (furnace ceiling, potentiostat compliance, acid budget), not Lila's SI numbers, which
  are not staged. They are source-labeled as public instrument specifications and are
  refined from their SI when it is available. The incompatible-chemical classes are
  standard public general-safety classes. No dual-use content (CC-31), checked by a
  grep-able denylist test.
- OERSIM loop (Phase 10): the loop runs end to end on the REAL OERSIM
  (`vendor/labgate/sim_ext/oersim.py`) replaying Lila's real `oer13_cps` dataset
  (`~/lila-gate/helao-async/.../oer13_cps.pzstd`, HELAO_DATASET). Because zero real forks
  survived (CC-22), the fork is a clearly-labeled SYNTHETIC worked example built from two
  existing addressable points in the dataset (no composition is proposed). Every loop
  artifact is labeled SYNTHETIC and carries the SIM-NOT-CHEMISTRY disclaimer; the outcome
  is a simulation over recorded data, not a new chemical measurement. The gate is the
  Phase 9 safety screen (typed, no text channel). A card whose instrument OERSIM cannot
  run gets status plan_only and stops at plan+gate with no faked result (CC-25). Note the
  oer13_cps composition space is 13 base metals (Ca..Zn), a different space from the
  Pd/In manuscript systems; the loop demonstrates the machinery, not a Pd result.
- Corpus accessibility (real): at launch only openly accessible papers could be
  downloaded. Accessible: their paper (arXiv:2609.30133) and ref 40 (Peng 2023, NSR, via
  Europe PMC). Refs 39 (Cherevko, Wiley), 42 (Chong, Science), 11 (Wan, Nat Catal), 12
  (Cherevko, Curr Opin) are paywalled and `excluded_inaccessible`. The D6 pilot returned
  NO-GO twice, so the corpus is the minimal accessible slice (their paper + ref 40). This
  is recorded prominently per D6.
- iR-correction is stated in ~3% of extracted result sentences (it lives in the Methods,
  not per-claim). Per-sentence extraction does not propagate a paper-global condition to
  each claim. Doing so is a candidate future improvement but was not implemented, to
  avoid inferring unstated conditions (D10) and to avoid softening the pilot (D6). This
  drives most pairs to veto on `condition_unstated`, which is the expected behaviour
  (CC-21).
- Auto-agreement across the two model families on the full card is 0 for the pilot, so
  every extracted claim goes to the review queue for Anu (Checkpoint 1). Agreement is the
  auto-accept signal, not a requirement for a claim to be approvable.
- Writeback (Phase 5): verdicts use the H-cell data (fig_3e.csv). Its electrolyte and
  current density are not in the released file, so they are unstated and every comparison
  vetoes on them (never inferred, D10); the result is 9 published vetoes, 0 confirm/
  contradict. A future improvement is to read Lila's H-cell electrolyte from their Methods
  and treat it as a stated data-side condition. The earlier screening-tier verdicts were a
  bug, corrected before Checkpoint 2 (CORRECTIONS.md, CONTRADICTION_DOSSIER.md).
- Discovery (Phase 11): structure-directed search on their closing mechanism claim
  returned a NULL result (5 candidates, all rung 4 thematic, 0 above rung 3). This is a
  valid outcome. The v0 vocabulary-stripping emits long natural-language queries, which
  arXiv (keyword search) matches poorly, and Semantic Scholar rate-limited (4 queries
  capped), so the candidate pool is small and noisy. A refinement is shorter
  domain-specific keyword queries and deeper paging. The report is rung-graded with
  ceilings and states the null plainly (CC-30); no superlatives.
- Baseline (Phase 6): on a preregistered sample of 60 vetoed pairs, the model call made 4
  comparisons the deterministic veto blocks (2 false disagreements, 2 false agreements) and
  recognised incomparability on the other 56. The model is capable but not exact; the veto
  catches what it misses. Both labelings are reported; no cherry-picking.
- Extraction stability (Phase 7): 0.423 (n=52 distinct claims, K=3 test-retest). The
  (subject, value) of an extracted numeric claim is highly reproducible; the observable
  axis LABEL is not stable run-to-run, so stability is measured on (subject, value-family),
  not on the axis string. This is the materials number, reported fresh with its n; it is not
  the consciousness-domain 0.25 (different domain and metric).
- Ledger (Phase 4): over the 34 approved claims, zero numeric forks survived the
  conditions veto. All 561 pairings are vetoes: 515 axis_mismatch (claims report
  different observables, CC-13), 149 condition_unstated (electrolyte/current-density often
  not in the result sentence), 3 condition_mismatch. This is the expected outcome (CC-21):
  the veto table is the headline result. Per CC-22, this is still a publishable Stage 1
  (ledger, vetoes, corroborations, verdicts, baseline). There are no mechanism claims in
  the approved set, so no mechanism-level fork either; Stage 3 (Phase 10) therefore runs
  on a clearly-labeled synthetic worked example, not a real ledger fork.
