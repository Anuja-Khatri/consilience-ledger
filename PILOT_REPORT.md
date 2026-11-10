# PILOT_REPORT

Status: **BLOCKED on API keys.** The pilot decision cannot be computed on real data
because no model API key is present in the build environment, and no `.env` file is
read (Anu standing ruling OQ-2). The non-API machinery is complete and tested; the
pilot runs and decides itself the moment a key is exported.

## What is ready (tested with a mock backend, 8 Phase 2 tests green)
- Dual-model extraction harness (`labext/extraction/`), two independent runs, disk
  cache (jsonl per paper per model), resumable (D3). Real backends for Anthropic and
  OpenAI are implemented (stdlib urllib) and raise `MissingKeyError` when their key is
  absent.
- Agreement gate: AGREED-PROVISIONAL = both models produce the identical card,
  field-exact after canonicalisation (`labext/extraction/canonicalize.py`). Quantities
  reduced to pint base units so 0.30 V and 300 mV agree; per-run ids excluded.
- Review queue: one markdown file per contested claim, with the source sentence, both
  model outputs, the field-level diff, and approve/reject checkboxes.
- Parking: unparseable cards are parked, never guessed (CC-11); partial agreement is
  parked, never averaged (CC-15).
- D6 GO/NO-GO rule (`labext/pilot.py`), applied autonomously, never softened.

## The D6 rule, ready to apply
Pilot papers: refs 39, 40, 42 (or the next accessible performance paper if 42 is out).
GO if at least 10 approvable numeric performance/stability claims have exact source
sentences AND at least half explicitly state electrolyte identity, current density, and
iR-correction status. First NO-GO shrinks to the Pd neighborhood and re-pilots once;
second NO-GO uses their paper + refs 39, 40 only, with the limitation recorded.

## Per-field stated-rate table
Pending extraction. Will be filled when a key is available: for each pilot paper, the
count of numeric claims and the fraction stating electrolyte, current density, pH,
temperature, iR-correction, loading, and protocol tier.

## To unblock
Export `ANTHROPIC_API_KEY` (and optionally `OPENAI_API_KEY` for a second family per D3)
into the build session, stage or allow download of the pilot papers, then re-run
Phase 2. The harness will extract, diff, write the review queue, and decide the pilot
by rule.
