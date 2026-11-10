# PRELAUNCH_CHECKLIST.md

Per III.5: verify at startup, list anything missing, continue. Checked 2026-11-10 (Phase 0).
Legend: [x] present / ready, [ ] missing or not yet ready.

## III.5 prelaunch items
- [ ] **`corpus_in/` with paper PDFs** — empty (only `.gitkeep`). See OQ-1. Needed before Phase 2.
- [ ] **API keys in environment** — not exported in the build session; available in
      `~/oii-sprint/.env` (ANTHROPIC + OPENAI + GEMINI). See OQ-2. Needed before Phase 2.
- [x] **Handoff / context documents (III.1)** — all 9 present in BUILD_ROOT:
      lock-candidate, learnings, 1-lila-operator-today, 2-consilience-offer-for-lila,
      strategy, modules, project-log, lila-native-blueprint, lila-hiring-research.
- [ ] **Confirmation Phases 1+ may start** — NOT yet. Today is 2026-11-10; D17 sets Phase 1 to
      16 Dec 2026. Phase 0 (read-only) is explicitly allowed now and is what ran.

## Repos / inputs (III.2, III.3)
- [x] theconsilience-engine `~/theconsilience-engine` @ 71f60a2 (exact pin match).
- [x] lab-gate `~/lila-gate/lab-gate` (present; no git, pin unverifiable — OQ-5).
- [x] consilience-verification `~/consilience-verification` @ 275dba8 (spec says HEAD — OQ-6).
- [x] helao-async `~/lila-gate/helao-async` @ ba910c4 (exact pin match), MIT license.
- [x] consilience-demo `~/consilience-demo` (present; no LICENSE — OQ-4).
- [x] miu-demo `~/miu-demo` (present; no LICENSE — OQ-4).
- [ ] lila_oer_manuscript + oer_exp_data.csv + oer13_cps dataset — absent (OQ-3). Needed Phase 5/10.

## Environment / harness (II.0 amendment)
- [x] **`BUILD_ROOT/.claude/settings.json`** present (created 10 Nov, 12:34). Auto-approves reads,
      in-folder edits, and routine commands; keeps `git push` and `rm` on ask; hard-denies
      Write/Edit under `~/oii-sprint` and `~/lila-gate`; denies reading `./.env`. This matches the
      spec and should stop the repeated permission prompts. Per II.0, if prompts still recur the
      session predates the file — report to Anu, do not work around it, never loosen the deny rules.
- [x] Python available for Phase 1 (D1: Python 3.11+, venv in repo) — to be set up at Phase 1, not now.

## Bottom line
Phase 0 (read-only inventory) had everything it needed and is complete. Four prelaunch items remain
for Anu before Phase 1 on 16 Dec: stage `corpus_in/`, export API keys, provide the Lila OER
data/dataset (OQ-3), and confirm the 16 Dec start. None block Phase 0.
