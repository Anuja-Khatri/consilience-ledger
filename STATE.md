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

## BUILD PAUSED here: two Anu inputs now gate the remaining work (ruling 2: a true block).
1. API keys (ANTHROPIC_API_KEY, optionally OPENAI_API_KEY). Unblocks Phase 2 real extraction and the
   pilot decision, and therefore all of Stage 1 (Phases 3-8) and the discovery judging in Phase 11.
2. The `oer13_cps` OERSIM dataset (env HELAO_DATASET). Unblocks the Phase 10 loop end-to-end.

Done so far: Phase 0 (inventory), Phase 1 (tagged phase-1), Phase 2 (code-complete, not tagged,
blocked on keys), Phase 9 (tagged phase-9). Tests: 39 green. `make reproduce` green.

## Remaining UNBLOCKED scaffolding that can still be built without those inputs (next, if continued):
- Phase 10 partial: port the experiment-card model from miu-demo EXPERIMENT_SPEC.md into a pydantic
  card (add the explicit `discriminating_power` field, CC-27; check `instrument_exists` vs OERSIM
  capability list, CC-25 -> plan_only); the card->helao Action/Experiment/Sequence translator
  validated against a schema generated from helao models (model_json_schema, pydantic v2); the
  Human Review Dossier renderer; the fork candidate table (csv+json). These build and test on a
  LABELED SYNTHETIC fork (CC-22). Only the gate->OERSIM->verdict execution waits on input 2.
- Phase 11 partial: the vocabulary-stripping + arXiv/Semantic Scholar search harness (D12, CC-29,
  cached, rate-capped) and the Module D reconciliation report template. The judging of found papers
  and the mechanism-claim input wait on Stage 1 (input 1).

## BLOCKED until inputs: Phases 3-8 (ledger, writeback, baseline, discipline, render), Phase 10
end-to-end, Phase 11 discovery judging, Phase 12 final package. Checkpoint 1 (after Phase 3) and
Checkpoint 2 (after Phase 8) are not reachable until input 1 is provided.
