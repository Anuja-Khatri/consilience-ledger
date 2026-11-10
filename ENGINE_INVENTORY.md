# ENGINE_INVENTORY.md

Phase 0 deliverable. Read-only inventory of the demo codebases and pinned repos that
this build (`consilience-lab-extension`) copies from or ports. Produced 2026-11-10.

BUILD_ROOT = `/Users/anujakhatri3/consilience for lila` (the folder holding the spec).
New build folder (the only writable target in Phase 0) = `BUILD_ROOT/lab-extension/`.
No file outside `BUILD_ROOT/lab-extension/` was written. No read-only repo was modified.

---

## 0. Where every source lives on this Mac (resolved paths)

| Spec name | On-disk path | git? | Pin wanted | Pin found | Status |
|---|---|---|---|---|---|
| theconsilience-engine | `~/theconsilience-engine` | yes | 71f60a2 | **71f60a25…** | EXACT MATCH |
| lab-gate | `~/lila-gate/lab-gate` (nested) | no `.git` | 3e0185a | n/a (no git) | present, sha unverifiable |
| consilience-verification | `~/consilience-verification` | yes | HEAD | 275dba8 | present (spec says HEAD) |
| helao-async | `~/lila-gate/helao-async` | yes | ba910c4 | **ba910c4c…** | EXACT MATCH |
| lila_oer_manuscript (fl97inc) | **NOT ON DISK** | - | HEAD@build | - | **MISSING (see OQ-3)** |
| consilience-demo | `~/consilience-demo` | no `.git` | (local read) | - | present |
| miu-demo | `~/miu-demo` | no `.git` | (local read) | - | present |

Notes:
- `lab-gate` is nested inside `~/lila-gate/` (which also holds `helao-async`, `helao-async-pr`,
  `handoff-operator`, and a `refs/consilience-verification` copy). Use `~/lila-gate/lab-gate`.
- `lab-gate` and `consilience-demo`/`miu-demo` have no `.git`, so their commit pins cannot be
  verified. `lab-gate` is Anu's own code (copying unrestricted per II.2); record the directory
  mtime/contents hash in PROVENANCE at vendor time instead of a commit sha.
- Per II.0 the read-only repos stay where they are; no clone into `BUILD_ROOT/upstream/` is
  needed because all required repos except `lila_oer_manuscript` are present.

---

## 1. theconsilience-engine  (judge core)  - LICENSE: Apache-2.0 (code) + CC-BY-4.0 (docs)

Copying is unrestricted (Anu's own code, II.2). Note the license is **Apache-2.0, not MIT**; the
PROVENANCE line should say so.

| Component | Path | Entry / notes |
|---|---|---|
| Typed VF2 matcher | `judge/matching/vf2_typed.py` | `check_subgraph_isomorphism(a,b)`. `node_match` (L19-24, matches claim_kind+physical_scale), `edge_match` (L27-36, relation+causal_direction, "Newman guard"). Wraps NetworkX `DiGraphMatcher`. |
| Four-rung ladder | `judge/grading/four_rung_ladder.py` | `assign_rung(is_iso, mcs_ratio, equivocation_survived, has_defect_edge)`; `CEILINGS` dict (rung 1-4). Pure/deterministic. |
| Equivocation | `judge/equivocation/lexical_ablation.py` | `equivocation_test(a,b)`; per-term ablation; verdict `structurally_supported` vs `vocabulary_dependent`. |
| Testability | `judge/testability/capability_map_lookup.py` | `check_testability(disagreement, capability_map, map_version)` → testable_now / under_assumption / not_testable. |
| Determinism hash | `judge/hash/determinism_check.py` | content-hash support for matcher output (SHA-256). |
| Schemas | `judge/schema/*.json` | `claim_card.json`, `correspondence.json`, `instrument_entry.json`, `rejection.json`. |
| Docs | `docs/` | `experiment-design.md`, `structural-matching.md`, `validation.md`, `equivocation-test.md`, `grading.md`, `rejections.md`, `structure-directed-acquisition.md`, `full-pipeline-detail.md`. |

Claim-card fields (IV.1 base set): all 14 named fields exist in `claim_card.json`. Twelve are
required; `measurable_with` and `domain` are present but NOT in the `required` array.

Defect enum: defined in **`judge/schema/rejection.json`** field `defect_type`, NOT in Python.
Current values: `type_mismatch`, `direction_mismatch`, `vocabulary_dependence`,
`provenance_circularity`, `insufficient_coverage`. (IV.3 adds `condition_mismatch`,
`condition_unstated`, `axis_mismatch` - Phase 1 extends this JSON enum.)

PORTS CLEANLY. **Design flag for Phase 1:** NetworkX `DiGraphMatcher` accepts only `node_match`
and `edge_match`. The new `conditions_compatible` predicate (IV.2) cannot be a third matcher
callback; it must either be folded into `node_match`/`edge_match` or run as a pre-filter over the
claim pair before the matcher is constructed. Recommend a pre-filter (default-deny comparability
gate) so the judge path stays untouched and the veto carries its own named defect.

---

## 2. lab-gate  (`~/lila-gate/lab-gate`)  - LICENSE: MIT (Copyright 2026 Anuja Khatri)

| Component | Path | Notes |
|---|---|---|
| Units (pint, fail-closed) | `gate/boundary/units.py` | `to_canonical(value, dimension)`, `_as_quantity`, `UnitError`. Anything unparseable/undimensioned/boolean/wrong-dimension RAISES (fail-closed). CANONICAL: degC, minute, mL, nm, Hz. |
| Invariants registry | `gate/registry/invariants.yaml` + `schema.py` + `lock.py` + `ltlf.py` | pydantic strict (`extra=forbid`). Kinds: bound / forbid_combo / accumulate / reach. Predicate mini-language `{var,op,value}`. `lock.py registry_hash()` = SHA-256 over canonical sorted JSON. This is the IV.2 "invariants house style". |
| Checker interface | `gate/checker/reference.py` `evaluate(parsed, registry, …)`; `smt.py` `encode_and_check`; `ltlf_eval.py`; `equivalence.py`; `certificates.py` | Pair of independent checkers (Python LTLf + Z3 SMT) proven equivalent. This is the interface the Stage 2 rules-to-screen compiler targets. |
| Verdict entry | `gate/verdict.py` | `decide(raw_plan, horizon_k)` → Verdict (PASS/BLOCK/ABSTAIN); `plan_fingerprint`, `plan_hash`; `decide_merged` (shared-budget). |
| No-text-channel test | `tests/test_no_text_channel.py` | injects `ZZ_INJECTED_SENTINEL_ZZ` into 1000 plans; asserts public verdict byte-identical clean-vs-tainted, sentinel never in verdict/fingerprint, but IS captured to `quarantined_text`. Static test: checker/verdict/units never reference free-text fields. |
| Red-team | `tests/test_redteam.py`; generators `eval/redteam/{static,decomposition,adaptive}.py`, `goals.yaml`; fixtures `tests/planfactory.py` | typed gate lets through no in-spec attack; decomposition-beyond-horizon ABSTAINs. |
| OERSIM | `sim_ext/oersim.py` | `InProcessOERSIM`, `run_activelearn(plate_id, iterations, seed, dataset_path, requester_id)`. Replays the **real `oer13_cps` dataset** via real `calc_eta`. Capabilities: change_plate, get_loaded_plate, measure_cp (CP3 chronopotentiometry), acquire_next (seeded GP-EI stand-in). Byte-deterministic for fixed (plate,iters,seed). |
| Surrogate / accounting | `sim_ext/surrogate.py`, `sim_ext/accounting.py` | deterministic per-element linear I1 model; 13-element comp_vec summing to 100; derives furnace/instrument minutes + acid mL. |
| Gate hooks | `gate/hook/oersim_hook.py`, `dispatch_hook.py` | `run_gated(...)` inserts the gate at the OERSIM decision step without touching helao; PASS→execute, BLOCK→next acquisition, ABSTAIN→hold queue. `gate_dispatch(raw_plan)` for orchestrator plans. |

PORTS CLEANLY for Stage 2/3. **Dependency flag:** `sim_ext/` requires an adjacent `helao-async`
checkout (present, ba910c4 ✓) AND the `oer13_cps` dataset via env `HELAO_DATASET`. **That dataset
is not on disk** (see OQ-3). No "screen compiler" exists yet - Stage 2 (features 13-16) is new code
that compiles registry entries down to the `gate/checker` interface above.

---

## 3. consilience-verification  - LICENSE: MIT (probe_set/ dual MIT + CC-BY-4.0)

| Component | Path | Notes |
|---|---|---|
| Numbers freeze gate | `pipeline/numbers_lock.py` | freezes the metrics registry: `metrics_sha()` SHA-256 over canonical metrics array; aborts if any precondition metric_id missing; writes lock to `results/registry.json` + `paper/NUMBERS_LOCK.json`. |
| Prose number linter | `pipeline/lint_claims.py` (+ `lint_allowlist.txt`) | the "cited number must be in the registry" enforcement over docs/paper. (numbers_lock is the registry half; lint_claims is the prose half - IV.5 needs BOTH.) |
| Registry | `pipeline/registry.py` | `class Registry.upsert(metric_id, value, task, n, ci_lo, ci_hi, preregistered, …)`; backing `results/registry.json` + schema. |
| N-gram guard | `pipeline/ngram_guard.py` | contamination guard; ≥8-word exact-run leakage detector, provenance report, calibrated FPR. Relevant to Phase 11 discovery / Phase 7 discipline. |
| Stability (test-retest) | `pipeline/a5_stability.py` | recurrence of claim-clusters across 5 replicate extractions (seeds 11/22/33/44/55); KEEP_MIN=4. Consciousness-domain n = 16 candidate windows ×5; baseline 27.1% imported (cited, not re-measured). **The materials stability number is unmeasured - Phase 7 measures it fresh.** |
| Adjudication | `pipeline/a2_adjudicate.py`, `a2_finalize.py`, `b3_panel.py` (+ `stats.py` κ / percent_agreement) | model-drafted verdicts → human `review/*.csv` approve/reject → finalize. Cross-vendor panel (gpt-4.1 + gemini). |

PORTS CLEANLY: numbers_lock + lint_claims + registry are the IV.5 lock pattern; a5_stability is the
Phase 7 template; stats.py is the Phase 6 baseline-agreement math.

---

## 4. consilience-demo  (COGITATE app)  - LICENSE: **NONE present** (see OQ-6)

All portable machinery is under `demo/` (self-contained package). Repo root is an unrelated
FastAPI product app and is NOT ported.

### III.3 answers (all four found)

1. **Extraction pipeline** - `demo/pipeline/p2_extract.py` (~484 LOC) + `demo/pipeline/schemas.py`
   (~137 LOC, pydantic v2 `Claim` model) + `p1_ingest.py`, `p3_normalize.py`.
   - Model call: `extract_window()` → `client.messages.create(model=SONNET,…)`, strict JSON array,
     3 few-shots. Constants `SONNET="claude-sonnet-4-6"`, `HAIKU="claude-haiku-4-5-20251001"`.
   - Candidate pre-filter `candidates()` (regex `SIGNAL`/`REFLIKE`, `MAX_CANDIDATES=64`, `WINDOW=8`).
   - Durable output: JSONL draft `demo/data/claims/<slug>_draft.jsonl` (one card/line).
   - **Key path is hardcoded to `~/thoughtlog/.env`** - must change to env-var-only for D14.
2. **Cross-model agreement gate** - `haiku_agreement()` in `p2_extract.py` (~16 LOC): Haiku
   independently re-derives `(entity_type, axis, polarity)` from only the cited passages; equality
   is **field-exact on those three fields**, stored as `Claim.agreement: bool`. Stronger audited
   version: `demo/eval/t3_independent_checker.py` (~337 LOC) adds an independent-lineage model
   **OpenAI `gpt-4.1` (temp 0)**; agreement stats (Cohen's κ) in `demo/eval/stats.py`.
3. **Human review queue** - `write_review()` / `apply_review()` in `p2_extract.py` (~155 LOC).
   Format is a **Markdown table, one file per theory/batch** (`demo/review/extraction_review_<slug>.md`)
   with approve/reject/corrected checkboxes; `--apply-review` parses verdict rows → `<slug>_approved.jsonl`.
4. **Capability map** - `demo/vocab/*.yaml` (version `demo_v0`): `entity_types.yaml` (14),
   `axes.yaml` (12 + canonical_entity_types + observable_links), `relations.yaml` (4),
   `observables.yaml` (instruments/scales), `contrast_axis_map.yaml`. Loaded by `schemas.py` to drive
   validation.
   - Reusable disk cache (separate from p2): `demo/eval/common.py` `cached_call()` keyed by
     `sha256(model+system+user+temp+max_tokens)`, cached under `demo/eval_out/cache/<model>/`. Fully
     generic - this is the D3 "all model outputs cached to disk, reruns free/resumable" layer.

Portable surface ≈ 1,100–1,600 LOC Python + 5 small YAMLs.

### Divergences from spec (become NEW work in Feature 6 / Phase 2)

- Spec Phase 2 AGREED-PROVISIONAL = **both models produce the identical FULL card** (field-exact
  after canonicalisation). Demo only cross-checks 3 fields (entity_type/axis/polarity), not quantity
  or the 10-key `conditions` block. Full-card diff is new.
- Spec wants **one md file per contested claim**; demo writes one md per theory (a table). Rework.
- Demo flags agreement but still routes everything to review; spec auto-accepts AGREED-PROVISIONAL.
- Hardcoded `~/thoughtlog/.env` key path → env-vars only (D14).

---

## 5. miu-demo  (physics workspace)  - LICENSE: **NONE present** (see OQ-6)

This is a **data + LLM-prompt artifact, not a code library**. No pydantic models, no JSON Schema,
no clean importable generator. The reusable assets are the spec + data contract; the `tools/` Python
(~1,362 LOC) is corpus-specific glue (hardcoded `~/miu-demo` paths, Hagelin/MIU maps).

### III.3 answers (all four found)

1. **Experiment card generator (stage-6B)** - there is no single function. The generator *spec* is
   `experiments/EXPERIMENT_SPEC.md` ("Experiment-Path Spec - Phase 4"), with the HARD RULES (real
   instruments only, honest falsification/kill-switch, verbatim quotes, conservative cost). Output =
   `experiments/experiment_*.json`. Supporting code: `tools/validate_experiments.py` (~83 LOC,
   `check(obj)`) and `tools/build_demo_data_v2.py` `load_exp()` (~40 LOC of the 265-LOC file).
2. **Card schema** - defined in `EXPERIMENT_SPEC.md` (L11-47) and enforced as the key-sets `TOP`
   and `DES` in `validate_experiments.py`. Top-level: experiment_id, match_id, title, claim_a/b,
   claim_*_source_sentence, structural_bridge, experiment_design, falsification, who_could_run_this,
   estimated_cost (`$10K|$100K|$1M|$10M+`), estimated_timeline, miu_relevant, value_to_hagelin,
   sources_bridged[]. `experiment_design`: hypothesis, manipulated_variable, discriminating_observable,
   instrument, **instrument_exists (bool)**, instrument_source, protocol_sketch,
   predicted_outcome_if_match_{holds,fails}, control_conditions. Optional `flag_not_scientific` with
   `falsification: "NONE - not falsifiable"`.
3. **Structure-directed acquisition (vocabulary stripping + structural queries)** - entirely under
   `source-discovery/` as prompt + JSON, **~0 portable Python**. Loop: unmatched claims →
   `structural_pattern` field (surface vocabulary discarded) → `search_queries[]` in alien
   vocabularies + `target_domains[]` → arXiv/S2 search (`_search/`, `search_results.json`) →
   `selected_papers.json` tagged `GAP:match_NN` → re-match. Key file `unmatched_patterns.json`.
   Fetchers `tools/arxiv_fetch.py` (42 LOC), `tools/select_and_download.py` (67 LOC).
4. **EXP_48 weak-discriminating-power flag** - `experiments/experiment_48.json`. There is **NO
   structured flag field**; "weak discriminating power" is prose inside the `falsification` field
   (and `value_to_hagelin`). The only machine-detectable flag is `flag_not_scientific` /
   `falsification` starting "NONE". Spec CC-27 requires propagating a weak-discriminating-power flag
   card → candidate table → dossier, so Phase 10 must **promote this to an explicit field**
   (e.g. `discriminating_power: strong|weak`).

---

## 6. helao-async  (`~/lila-gate/helao-async`, ba910c4 ✓)  - LICENSE: MIT (redistribution + attribution OK)

CC-28 note: helao's MIT license permits copying/redistribution with the notice retained. We only
*translate to* its schema (we do not vendor helao source), so attribution in PROVENANCE suffices.

- Models in `helao/core/models/`: `action.py` (ShortActionModel/ActionModel), `experiment.py`
  (ShortExperimentModel/ExperimentModel), `sequence.py` (ShortSequenceModel/SequenceModel).
- **pydantic v2** (ConfigDict, field_validator mode=before, model_dump). Pins: pydantic 2.14.1.
  Matches D1 (pydantic v2).
- Plan nesting: `SequenceModel.planned_experiments: list[ShortExperimentModel]`; `ExperimentModel.planned_actions: list` (untyped) + `experiment_params: dict`; action/exp/seq `*_params` are free-form dicts.
- **No JSON Schema is committed** anywhere in helao. The Stage 3 translator (Phase 10) must emit
  JSON validated against a schema it generates itself via pydantic v2
  `SequenceModel.model_json_schema()` / `ExperimentModel` / `ActionModel`. Several fields `$ref`
  external types (MachineModel, SampleUnion, FileInfo, enums). On-disk records are YAML, not JSON,
  but the model shape is identical. (CC-24: translate to the PINNED schema; note upstream drift.)

---

## 7. Revised sizes for features 6, 17, 23 (required by Phase 0 acceptance)

| Feature | Port source | Ports cleanly | NEW work required | Revised estimate |
|---|---|---|---|---|
| **6 Extraction pipeline** | consilience-demo `demo/pipeline/*` + `demo/eval/common.py` cache + `t3_independent_checker.py` | windowing, JSON extraction, dedup, provenance-required rule, disk cache, cross-model κ math | full-CARD field-exact diff (not 3 fields); the 10-key `conditions` extractor + `quantity` block (IV.1); one-md-per-claim review format; auto-accept AGREED-PROVISIONAL; env-var-only keys (D14); materials vocab pack; tables-as-first-class (CC-10) | Port ~1.2k LOC + ~600-900 LOC new. **~1.5–2.5 weeks** (was a straight PORT; now PORT+NEW, mid-weight). |
| **17 Card generator** | miu-demo `EXPERIMENT_SPEC.md` + `validate_experiments.py` + `load_exp` | the card schema + HARD RULES (instrument_exists, falsification-NONE) | author a fresh pydantic card model (no reusable one exists); **explicit `discriminating_power` field** (CC-27); check `instrument_exists` against OERSIM capability list before compile (CC-25 `plan_only`); domain-neutralise Hagelin/MIU fields | ~100 LOC port + ~250-400 LOC new. **~1 week.** |
| **23 Cross-field correspondence / discovery** | miu-demo `source-discovery/*` (pattern + prompt only) | the *concept* (strip vocabulary → structural pattern → alien-vocab queries → target domains → gap-close) | **~0 reusable code** - reimplement acquisition as code/prompt; arXiv + S2 clients with caching + rate caps (D12/CC-29); rung grading with ceilings; thematic quarantine; chance context | Mostly new. **~1.5–2 weeks after Stage 3 core** (lock estimate "1-2 weeks after C" holds, lean to the top of the range given zero portable code). |

---

## 8. Phase 0 acceptance check

- [x] Inventory exists (this file).
- [x] Every III.3 question answered (consilience-demo 4/4, miu-demo 4/4; see §4, §5).
- [x] Licenses recorded (CC-28): engine Apache-2.0, lab-gate MIT, consilience-verification MIT,
      helao-async MIT (redistribution OK), **consilience-demo NONE, miu-demo NONE** (OQ-6).
- [x] Revised sizes for features 6, 17, 23 (§7).
- [x] Zero writes outside `BUILD_ROOT/lab-extension/`; zero reads mutated any repo.
- [x] Pins verified where git exists: engine 71f60a2 ✓, helao ba910c4 ✓.

Open items that block later phases are logged in `OPEN_QUESTIONS.md` (OQ-1 … OQ-7), each with a
safe default already applied per II.1. No build code written. Phase 1 starts 16 Dec 2026 (D17).
