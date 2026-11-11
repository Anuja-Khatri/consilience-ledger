# STATE.md

Per CC-32: a fresh session resumes from the repo alone. Updated at the end of each phase.

## STANDING RULES (Anu, 2026-11-10 - override the spec; full text in OPEN_QUESTIONS.md)
- **No date gate (D17 superseded).** Build continuously, Phases 1-12 in order, starting now.
  Never start a phase before the previous phase's acceptance criteria pass.
- **Never ask questions.** Safe default + log in OPEN_QUESTIONS.md + continue. Stop only at
  Checkpoint 1 (after Phase 3), Checkpoint 2 (after Phase 8), or a true block. At any stop: update
  STATE.md and summarize.
- **Never read any `.env` file.** If API keys are absent from the live environment, do the non-API
  parts, log the block, move to unblocked work.
- OQ rulings applied: clone lab-gate@3e0185a and lila_oer_manuscript@HEAD into `upstream/`;
  freeze consilience-verification@275dba8; demo repos are own code (derived work MIT).

## Current state: Phase 0 COMPLETE (2026-11-10)

Phase 0 is read-only ENGINE_INVENTORY. It ran to completion. No file outside
`BUILD_ROOT/lab-extension/` was written; no read-only repo was modified.

### What is done
- Located and identified every source repo on this Mac (see ENGINE_INVENTORY §0). Verified pins:
  theconsilience-engine 71f60a2 ✓, helao-async ba910c4 ✓. lab-gate has no git (OQ-5).
- Answered all III.3 questions for `consilience-demo` (4/4) and `miu-demo` (4/4).
- Mapped the pinned repos' reusable components with exact paths (engine judge, lab-gate gate/sim,
  consilience-verification locks/stability, helao plan models).
- Recorded licenses (CC-28): engine Apache-2.0, lab-gate MIT, consilience-verification MIT,
  helao-async MIT (redistribution OK); consilience-demo and miu-demo have NO license (OQ-4).
- Produced revised sizes for features 6, 17, 23 (ENGINE_INVENTORY §7).
- Verified `BUILD_ROOT/.claude/settings.json` exists and is configured per the II.0 amendment.

### Deliverables written (all under `BUILD_ROOT/lab-extension/`)
- `ENGINE_INVENTORY.md` - the full inventory (this phase's required output).
- `OPEN_QUESTIONS.md` - OQ-1 … OQ-7, each with a safe default applied.
- `PRELAUNCH_CHECKLIST.md` - III.5 verification.
- `STATE.md` - this file.

### Key paths (for the next session)
- Spec: `BUILD_ROOT/BUILD-SPEC-consilience-lab-extension.md`
- Build repo root (to be `git init`-ed in Phase 1): `BUILD_ROOT/lab-extension/`
- Engine judge: `~/theconsilience-engine/judge/` (matcher at `judge/matching/vf2_typed.py`)
- Gate: `~/lila-gate/lab-gate/gate/` + `sim_ext/` (OERSIM) + `tests/test_no_text_channel.py`
- Locks/stability: `~/consilience-verification/pipeline/{numbers_lock,lint_claims,registry,ngram_guard,a5_stability}.py`
- helao models: `~/lila-gate/helao-async/helao/core/models/{action,experiment,sequence}.py` (pydantic v2)
- Extraction to port: `~/consilience-demo/demo/pipeline/` + `demo/eval/common.py` (cache) + `demo/vocab/`
- Card gen / acquisition to port: `~/miu-demo/experiments/EXPERIMENT_SPEC.md`, `~/miu-demo/source-discovery/`

### Blockers carried into later phases (from OPEN_QUESTIONS.md)
- Phase 2 needs `corpus_in/` papers (OQ-1) and exported API keys (OQ-2).
- Phase 5 needs the Lila OER manuscript data + manuscript license (OQ-3). Phase 10 uses the PUBLIC
  helao-async `oer13_cps` dataset (present), not Lila's data - it is not blocked by OQ-3.

## Phase 1 COMPLETE (2026-11-10). Acceptance: pytest green (24 passed), tagged phase-1.

What shipped:
- git repo at `BUILD_ROOT/lab-extension/`, Part IV layout, venv, pinned requirements.
- Upstream clones in `BUILD_ROOT/upstream/`: lab-gate@3e0185a (verified), lila_oer_manuscript@92a7737.
  Manuscript license checked: data CC-BY-4.0, code MIT; data NOT committed (Anu ruling OQ-3).
- Vendored with PROVENANCE: engine judge tree (unchanged except the added `conditions_compatible`
  in vendor/engine/judge/matching/vf2_typed.py), lab-gate units.py.
- `labext/`: schema.py (Claim Card v2, Conditions 10-key, Quantity, defects, verdict, rules),
  units.py (pint fail-closed), comparability.py (default-deny, named defects), judge.py (axis
  check, conditions veto, quantity-floor fork, determinism hash), lock.py, gen_schemas.py.
- `schema/*.json` generated from the models. `rules/comparability_rules.yaml` (v0, provisional)
  plus `rules/rules.lock`. `domainpack/materials_oer/*.yaml`.
- Tests (24): units fail-closed; condition_mismatch, condition_unstated, axis_mismatch, true fork,
  within-floor; schema parse-failures; determinism (same hash, order-independent).
- `make reproduce` regenerates schemas and lock and runs the suite green. The venv has a `.pth`
  pointing at the repo root so `python -m labext.*` works from any cwd.

Design note: NetworkX DiGraphMatcher accepts only node_match and edge_match, so the comparability
veto runs as a pre-filter over the pair, not as a third matcher callback. The vendored
`conditions_compatible` predicate delegates to the authoritative `labext.comparability`.

## Phase 2 CODE-COMPLETE, pilot BLOCKED on API keys (2026-11-10). NOT tagged.
Confirmed no model key in the live environment (OQ-2; Anu ruling: never read .env). Built and
mock-tested the full non-API pipeline (`labext/extraction/` + `labext/pilot.py`, 8 tests green,
32 total):
- Dual-model harness with resumable jsonl disk cache; real Anthropic + OpenAI backends via stdlib
  urllib (raise MissingKeyError without a key); MockBackend for tests.
- Field-exact agreement gate (canonicalize.py: quantities to pint base units, per-run ids excluded);
  AGREED-PROVISIONAL = identical card from both models.
- Review queue: one md per contested claim, with source sentence, both outputs, field diff,
  approve/reject checkboxes. Parking for unparseable (CC-11) and partial agreement (CC-15).
- D6 GO/NO-GO rule, applied autonomously, never softened.
- Extraction prompt + few-shots; model strings recorded in METHODS.md. PILOT_REPORT.md written.
What is blocked: the REAL extraction and the pilot DECISION need a key. All of Stage 1 (Phases 3-8)
depends on real extracted claims and is blocked until a key is exported. To unblock: export
ANTHROPIC_API_KEY (and optionally OPENAI_API_KEY per D3), then re-run Phase 2.

## Phase 9 COMPLETE (2026-11-10), built out of order as unblocked work. Tagged phase-9.
`safety_format/`: graded hazard registry (schema.py: bound / forbid_combo, grade ladder
established|plausible|weakly_supported, source per rule); typed plan boundary with no text channel
(boundary.py); rules-to-screen compiler with grade+source on every receipt and a registry hash
(compiler.py, shaped like lab-gate's checker/certificates); benign EHS seed (seed/registry.yaml:
furnace/potentiostat/acid bounds + standard incompatible-chemical classes, all source-labeled);
permanent dual-use denylist (policy.py); TIER_POLICY.md draft (D13). Acceptance met: 7 tests green
(round-trip block/pass, bound + forbid_combo blocks with grade+source, no-text-channel sentinel test,
zero dual-use grep, deterministic registry hash). Safe default logged: seed bounds use generic public
values pending their SI (LIMITATIONS.md).

## BOTH earlier blockers RESOLVED (2026-11-10)
- API keys: available via sourcing `$HOME/oii-sprint/.env` (ruling 1 pattern). Never read into output.
- OERSIM dataset: `oer13_cps.pzstd` found in the helao checkout
  (`~/lila-gate/helao-async/helao/deploy/test/demos/data/oer13_cps.pzstd`); set HELAO_DATASET there.

## Phase 2 COMPLETE, tagged phase-2 (2026-11-10). Real extraction + D6 pilot.
- Models claude-sonnet-5 + gpt-4.1. Accessible papers: their paper 2609.30133 + ref 40 Peng (OA).
  Refs 39/42/11/12 paywalled -> excluded_inaccessible. Added a repair layer (labext/extraction/repair.py)
  so real model output validates; 70 approvable numeric claims; 72 contested -> review queue; auto-agreed 0.
- D6 applied, never softened: NO-GO twice (iR-correction stated in ~3% of result sentences, Methods-only),
  -> minimal corpus (their paper + ref 40). PILOT_REPORT.md has the per-field stated-rate table.

## Phase 3 COMPLETE -> CHECKPOINT 1 REACHED, tagged phase-3 (2026-11-10). BUILD STOPPED here (ruling 5).
- Full corpus == minimal accessible corpus (already extracted). Comparability rules v0 drafted with
  sources (rules/SOURCES.md, rules.lock). CHECKPOINT1.md written for Anu: review-queue index
  (extraction/review_queue/INDEX.md, 72 items), drafted rules, corpus manifest, honest counts, and
  exactly what her batch unlocks. Auto-agreed = 0, so there are no AGREED-PROVISIONAL claims to carry
  into Phase 4; the build correctly waits for her batch.

## CHECKPOINT 1 RESOLVED, then Phases 4-8 run; CHECKPOINT 2 REACHED (2026-11-10). BUILD STOPPED (ruling 5).

Anu's Checkpoint 1 triage (CP1-TRIAGE.md) was applied: 34 approved, 38 rejected; comparability-v0
locked (CR1 canonical electrolyte list, CR2/CR3 pint unit canonicalisation); CR5 logged as v1 candidate.

Phases completed this run:
- Phase 4 ledger (tag phase-4): 34 approved claims judged pairwise; 0 forks, 561 vetoes (515
  axis_mismatch, 149 condition_unstated, 3 condition_mismatch). Byte-deterministic ledger.hash;
  reports/ledger.md + forks_spotcheck.md. Zero forks is valid Stage 1 (CC-22).
- Phase 5 writeback (tag phase-5): verdicts vs oer_exp_data.csv (loaded at runtime, NOT committed,
  cited by sha+row). Corrected to use the H-cell data fig_3e.csv for verdicts (screening CSV is
  veto-only): 0 confirmed, 0 contradicted, 9 not_comparable (all published vetoes). See
  CONTRADICTION_DOSSIER.md / CORRECTIONS.md.
- Phase 6 baseline (tag phase-6): 60-pair preregistered sample; model made 4 comparisons the veto blocks.
- Phase 7 discipline (tag phase-7): PREREGISTRATION, numbers lock (NUMBERS_LOCK.json + linter),
  fresh materials extraction-stability 0.423 (n=52), red-team no-text-channel tests.
- Phase 8 (tag phase-8): static browser (browser/index.html), README/METHODS finalized under II.3
  (numbers lint clean), CHECKPOINT2.md. make reproduce is byte-identical (git status clean after).

Also done earlier: Phase 9 safety (tag phase-9); Phase 10 loop RAN end to end on the public
helao-async oer13_cps dataset (synthetic simulator-lookup example, not a fork); Phase 11 discovery
NOT YET RUN (the search did not execute meaningfully; see discovery/report/report.md, CORRECTIONS.md).

## BUILD COMPLETE through Phase 12. Checkpoint 2 signed off (name, license). PUBLISHING HELD for push approval.

Phases 10-12 done after sign-off:
- Phase 10 (tag phase-10): Stage 3 loop end-to-end on the REAL OERSIM (vendored sim_ext, PUBLIC
  helao-async oer13_cps dataset; 13 base metals, no palladium; not Lila's data). Two clearly-labeled
  SYNTHETIC simulator-lookup examples (two DIFFERENT materials each; not forks) drive card -> plan ->
  gate -> OERSIM -> writeback (SYN1 lookup_two_materials_differ, SYN2 lookup_two_materials_within_floor);
  SYN3 plan_only (CC-25). One-page dossiers, candidate table, SIM-NOT-CHEMISTRY on every artifact. No
  composition proposed.
- Phase 11 (tag phase-11): structure-directed discovery on their closing mechanism claim ->
  NOT YET RUN. The search did not execute meaningfully (long sentences into a keyword search,
  rate-limited to 4 queries, returned 5 unrelated particle-physics/astrophysics papers), so it is
  not a NULL result and says nothing about the durability question (discovery/report/report.md;
  CORRECTIONS.md). Module D reconciliation report over the ledger is unaffected.
- Phase 12 (tag phase-12): final verification. make reproduce byte-identical; 73 tests green;
  numbers lint clean; no retracted number outside CORRECTIONS/DOSSIER; no em dashes in docs (II.3);
  README has the affiliation disclaimer; name consilience-ledger.

Writeback correction standing: 0 confirmed, 0 contradicted, 9 not_comparable (CONTRADICTION_DOSSIER.md,
CORRECTIONS.md). Checkpoint 1 resolved (Anu triage applied).

## STOP POINT: full build done. PUBLISHING HELD pending Anu's push approval. No remote exists yet;
the repo is local-only. Exact push commands are in the final summary; do not push without approval
(D15: never push unless asked). Runtime inputs for a fresh session: source $HOME/oii-sprint/.env for
keys; HELAO_DATASET + LILA_OER_DATA_DIR point at the helao checkout and upstream/lila_oer_manuscript/data.

## Status tags: phase-1 .. phase-12 all tagged. Tests 73 green. make reproduce byte-identical.
