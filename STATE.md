# STATE.md

Per CC-32: a fresh session resumes from the repo alone. Updated at the end of each phase.

## STANDING RULES (Anu, 2026-11-10 — override the spec; full text in OPEN_QUESTIONS.md)
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
- `ENGINE_INVENTORY.md` — the full inventory (this phase's required output).
- `OPEN_QUESTIONS.md` — OQ-1 … OQ-7, each with a safe default applied.
- `PRELAUNCH_CHECKLIST.md` — III.5 verification.
- `STATE.md` — this file.

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
- Phase 5 + Phase 10 need the Lila OER data + `oer13_cps` dataset + manuscript license (OQ-3).

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

## Next: Phase 2 (extraction pipeline + pilot).
Blocked part: dual-model extraction needs API keys, absent from the environment (OQ-2; Anu ruling:
never read .env). Do every non-API part first: port the extraction, diff, and review-queue
structure from consilience-demo `demo/pipeline/` (one md file per contested claim, not per theory),
the disk cache from `demo/eval/common.py`, author the materials extraction prompt and the
AGREED-PROVISIONAL full-card diff, and download openly accessible pilot papers (refs 39, 40, 42)
per Anu ruling 4. Log the API block, run the D6 pilot rule when keys exist, else proceed to
unblocked later-phase work.
