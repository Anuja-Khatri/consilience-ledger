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
- OERSIM loop (Phase 10): OERSIM replays the real `oer13_cps` dataset via env
  `HELAO_DATASET`, which is not present on this machine. The loop's end-to-end run is
  blocked until that dataset (or a path to it) is provided.
