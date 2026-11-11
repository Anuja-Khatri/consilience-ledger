# FIXES_REPORT.md — correction pass (2026-11-11, local only, not pushed)

Fixes only; no new features; no model API calls. `make reproduce` stays byte-stable (re-locked where
a regenerated file changed a hash, noted below). Test suite green: **73 passed** (unchanged count;
`test_loop_run` assertion updated, `test_safety_format` dual-use test extended to the proposed file).

## Hashes that changed (re-locked; `make reproduce` byte-stable at the new values)
| file | before | after |
|---|---|---|
| rules/rules.lock (sha256) | `cc251d77…43d0d185` | `ba3db7c1…1adf92b7` |
| rules/rules.lock (version) | `comparability-v0` | `comparability-v0.1` (documentation-only) |
| ledger/ledger.hash | `f42d48c1…e7f758fe3` | `a11ee946…abe69bdd` |
| loop/{runs,cards,plans,dossiers}/* | (old wording) | regenerated (wording fix 1/2; not part of `make reproduce`'s locked hashes) |

**No verdict changed:** ledger 0 forks, 561 vetoes; writeback 9 not_comparable — byte-identical
decisions. The rules.lock / ledger.hash moved only because the rule `source` metadata (hashed) gained
its ported citations and the doc-only version bump; the ledger records the new `rules_version` label.

## Fix 1 — dataset misattribution (`oer13_cps` is public helao-async data, not Lila's)
Established from helao-async's own files (`helao/deploy/test/drivers/pstat/cpsim_driver.py`:
"the OER `oer13_cps` dataset … a pickled OER measurement library … replays stored CP traces";
`LICENSE.md`: MIT, High-Throughput-Experimentation) and the dataset itself (13 base metals, no Pd).
- Files: `labext/loop/run_loop.py`, `labext/loop/generate.py`, `labext/loop/__init__.py`,
  `PROVENANCE.md`, `LIMITATIONS.md`, `OPEN_QUESTIONS.md` (OQ-3), `STATE.md`, `CHECKPOINT2.md`;
  regenerated `loop/{runs,cards,plans,dossiers}/*`.

## Fix 2 — synthetic example is a simulator-lookup, not a fork
Two DIFFERENT materials are looked up, so it is not a claim disagreement. Relabelled everywhere;
`fork_confirmed` -> `lookup_two_materials_differ` / `lookup_two_materials_within_floor`.
- Files: `labext/loop/run_loop.py`, `labext/loop/dossier.py`, `tests/test_loop_run.py`,
  `STATE.md`, `CHECKPOINT2.md`, `LIMITATIONS.md`; regenerated loop artifacts.

## Fix 3 — stale text
- `README.md`: removed "Stage 3 scaffolding in place", "Phases 10-11 scaffolding", "Nothing is
  published"; true status stated (Phase 10 ran on public data; Phase 11 NOT YET RUN).
- `LIMITATIONS.md`: removed "Extraction has not run" and "Provisional claims (until Checkpoint 1
  returns)" — both stale (34 real claims extracted; Checkpoint 1 resolved).

## Fix 4 — discovery report honesty (NOT YET RUN)
The search fed long sentences to a keyword engine, was rate-limited to 4 queries, and returned 5
unrelated particle-physics/astrophysics papers; it did not execute meaningfully. Search NOT rerun.
- Files: `discovery/report/report.md` (rewritten), `README.md`, `LIMITATIONS.md`, `STATE.md`,
  `CHECKPOINT2.md`.

## Fix 5 — rule citations ported from ../ledger-v2
Ported the Gate-1-approved page-level citations (r0/GATE1.md, source B2 = PMC13707403, Molecules
2026) by FIELD (CR3/CR4 numbered oppositely in ledger-v2). Numbering, fields, predicates, tolerances
UNCHANGED -> no verdict change. Version bumped documentation-only v0 -> v0.1.
- Files: `rules/SOURCES.md`, `rules/comparability_rules.yaml` (source + version only),
  `rules/CHANGELOG.md` (new), `rules/rules.lock` (re-locked), `ledger/*` + `ledger/ledger.hash`
  (regenerated). See the hash table above.

## Fix 6 — proposed safety seed (not activated)
`safety_format/seed/registry_proposed.yaml` (new): exact public citation per rule (Prudent Practices
in the Laboratory, NRC 2011; OSHA 29 CFR 1910.1450) or explicit `generic` label for instrument
bounds (Lila states operating values, not protection ceilings). Harmless; dual-use denylist scan
passes. `SEED_APPROVAL.md` (new, one row per rule); `safety_format/TIER_POLICY.md` marked AWAITING
ANU'S WORDING. Active `registry.yaml` unchanged.
- Files: `safety_format/seed/registry_proposed.yaml`, `SEED_APPROVAL.md`,
  `safety_format/TIER_POLICY.md`, `tests/test_safety_format.py` (extended dual-use scan).

## Fix 7 — the skipped durability check (claim 2609.30133__010)
Pass rule preregistered in `PREREGISTRATION.md` BEFORE opening the trace. Ran against the authors'
own released H-cell trace `upstream/lila_oer_manuscript/data/fig_3e.csv` (sha `cac02293…`). Result:
**FAIL** of the strict rule — InMnPdOx reaches 0.5055 V at 575.5 h (one point ~5.5 mV above the
claimed 0.5 V ceiling) over 11.5-999.6 h coverage. Reported as a CONSISTENCY CHECK between the
authors' claim and their own data, NOT independent confirmation.
- Files: `PREREGISTRATION.md`, `reports/durability_check_2609.30133.md` (new).

## Fix 8 — this report + CORRECTIONS.md + local commit
`CORRECTIONS.md` updated (2026-11-11 entry). `FIXES_REPORT.md` (this file). Committed locally; **not
pushed**.
