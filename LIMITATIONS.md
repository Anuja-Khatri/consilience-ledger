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
- OERSIM loop (Phase 10): OERSIM replays the real `oer13_cps` dataset. It was located
  inside the helao-async checkout (`helao/deploy/test/demos/data/oer13_cps.pzstd`), so
  `HELAO_DATASET` can point there; the loop is no longer blocked on the dataset.
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
