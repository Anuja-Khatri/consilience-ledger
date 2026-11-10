# OPEN_QUESTIONS.md

Per II.1: anything the spec does not fully resolve is logged here with a safe default already
applied, and the build continues. Nothing here is interactive. Entries marked **BLOCKS** gate a
later phase and need Anu before that phase runs; the rest are recorded for transparency.
Started Phase 0, 2026-11-10.

---

## Anu's standing rulings (verbatim, received 2026-11-10) - these override the spec where they conflict

> Updates to your instructions, from Anu. These override the spec where they conflict.
>
> 1. D17 is superseded: there is no date gate. Build continuously, phases 1 through 12 in order,
>    starting now. Never start a phase before the previous phase's acceptance criteria pass.
> 2. Never ask me questions. Take safe defaults, log them in OPEN_QUESTIONS.md, continue. Stop only
>    at Checkpoint 1 (after Phase 3), at Checkpoint 2 (after Phase 8), or when work truly cannot
>    proceed without my inputs. At any stop: update STATE.md and summarize.
> 3. Rulings on your OPEN_QUESTIONS: OQ-2 never read any .env file anywhere; if API keys are not in
>    the environment, do every part of Phase 2 that needs no API call, log the block, and move to
>    whatever later work is unblocked. OQ-3 clone github.com/fl97inc/lila_oer_manuscript at HEAD,
>    record the sha, check its license, never commit its data. OQ-4 accepted: own code, derived work
>    MIT. OQ-5 clone lab-gate from github.com/Anuja-Khatri/lab-gate at 3e0185a into upstream/, vendor
>    from that clone. OQ-6 freeze consilience-verification at 275dba8. OQ-7 accepted.
> 4. corpus_in/ is empty for now. When you reach work that needs papers, use the openly accessible
>    ones you can legally download (arXiv, publisher open access, the Lila repo) per the spec's corpus
>    rules, mark paywalled ones excluded_inaccessible, and continue.
> 5. Record this message verbatim in OPEN_QUESTIONS.md as Anu's standing rulings, and reflect point 1
>    in STATE.md, so any future session resumes under these rules without me repeating them.

**How these resolve the OQ entries below:**
- OQ-1 / corpus: ruling 4 applies. Download openly accessible papers when needed; mark paywalled
  `excluded_inaccessible`; continue. No longer a hard stop.
- OQ-2 (API keys): **never read any `.env` file anywhere.** If no key is in the live environment,
  do every non-API part of a phase, log the block, and move to unblocked later work. (Supersedes the
  earlier default that pointed at `~/oii-sprint/.env`.)
- OQ-3 (Lila OER data): clone `github.com/fl97inc/lila_oer_manuscript` at HEAD, record sha, check
  license, never commit its data.
- OQ-4 (demo licenses): accepted - own code, derived work MIT.
- OQ-5 (lab-gate pin): clone `github.com/Anuja-Khatri/lab-gate` at 3e0185a into `upstream/`, vendor
  from that clone.
- OQ-6 (consilience-verification): freeze at 275dba8.
- OQ-7 (`refs_in/`): accepted.

No date gate (ruling 1): Phases 1-12 run continuously now, in order, each gated only on the prior
phase's acceptance criteria. Stops only at Checkpoint 1 (post Phase 3), Checkpoint 2 (post Phase 8),
or a true block.

---

## OQ-1 - `corpus_in/` is empty (no paper PDFs staged)
`BUILD_ROOT/corpus_in/` holds only `.gitkeep`. None of the D5 corpus papers, their paper
(arXiv:2609.30133) + SI, or ESAMP are staged yet.
- **Safe default applied:** Phase 0 proceeds (it needs no papers). Extraction (Phase 2+) will try
  open-access sources per III.4 and apply D16 (`excluded_inaccessible`, access attempt recorded) for
  the rest. Never scrape paywalled content.
- **BLOCKS:** Phase 2 pilot and Phase 3 corpus extraction. The D6 pilot needs refs 39, 40, 42.
- **Needs Anu:** stage every paper she has legitimate access to in `corpus_in/` before 16 Dec
  (the III.5 prelaunch item). This is expected pre-work, not an error.

## OQ-2 - API keys are not in the build session environment
No `ANTHROPIC_API_KEY` (or any model key) is exported in the current shell. Keys DO exist in
`~/oii-sprint/.env`: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`.
- **Safe default applied:** Phase 0 needs no model calls, so none were made. D3 is satisfiable
  (one Anthropic + one non-Anthropic family both available), which is the preferred configuration.
- **BLOCKS:** Phase 2+ extraction.
- **Needs Anu:** export the keys into the build session (D14: env-vars only; `.env` gitignored; the
  build fails with a clear message, never reads a key from a file). The ported pipeline reads from
  the environment only (no `~/thoughtlog/.env` path).
- **Phase 2 status (2026-11-10):** confirmed no model key in the live environment. Per Anu ruling,
  the full non-API Phase 2 pipeline was built and mock-tested (8 tests green): dual-model harness,
  resumable disk cache, field-exact agreement gate, one-md-per-claim review queue, and the D6
  GO/NO-GO rule. The real extraction and the pilot DECISION are pending a key (see PILOT_REPORT.md).
  Phase 2 is therefore code-complete but NOT tagged (acceptance needs a real pilot decision). All of
  Stage 1 (Phases 3-8) depends on real extracted claims and is blocked until a key is available.

## OQ-3 - Lila's real OER data is absent from this machine  **(largest gap)**
Three linked artifacts are not present anywhere under `~` (searched to depth 6, Trash/Library
excluded):
  1. the `lila_oer_manuscript` repo (github.com/fl97inc/lila_oer_manuscript),
  2. `oer_exp_data.csv` and the benchmark-curve CSVs (III.2 / Phase 5 writeback inputs),
  3. the `oer13_cps` dataset that `lab-gate/sim_ext/oersim.py` replays via env `HELAO_DATASET`
     (Phase 10 loop - this is the "OERSIM replays Lila's real data" mechanism).
Because the repo is absent, its LICENSE cannot be checked, so CC-28 cannot be resolved yet.
- **Safe default applied:** Phases 1-4 (schema, extraction, ledger) need none of this and proceed.
  At Phase 5, apply CC-28 conservatively by default: treat the data as non-redistributable until a
  permissive license is confirmed - do NOT commit their CSVs; load at runtime from an Anu-provided
  path via a fetch script; verdict records cite rows by index + sha.
- **BLOCKS:** Phase 5 (writeback) and Phase 10 (loop / OERSIM).
- **Needs Anu:** before Phase 5, provide the `lila_oer_manuscript` checkout (record its sha), the
  `oer_exp_data.csv` + benchmark CSVs, and the `oer13_cps` dataset path for `HELAO_DATASET`; and
  confirm the manuscript repo's license for the CC-28 decision.

## OQ-4 - `consilience-demo` and `miu-demo` have no LICENSE file
Phase 0 confirmed neither repo contains a LICENSE/COPYING file. II.2 names only
`theconsilience-engine` and `lab-gate` as "Anu's own code; copying unrestricted." Yet III.3 and
Phases 2/10/11 direct porting from these two demos, and D2 wants our shipped code MIT with a
PROVENANCE license line per vendored file.
- **Safe default applied:** treat both as Anu's own internal code (they are her demo repos).
  When vendoring in Phase 1+, write the PROVENANCE line as "author: Anu Khatri; no LICENSE file in
  source; internal reuse authorized by BUILD-SPEC III.3", and relicense our derived code MIT per D2.
- **Needs Anu:** add a LICENSE to both repos, or confirm these reuse terms at Checkpoint 2.

## OQ-5 - `lab-gate` pin 3e0185a cannot be verified (no git)
`~/lila-gate/lab-gate` has no `.git`, so its commit cannot be confirmed against the pinned 3e0185a.
- **Safe default applied:** it is Anu's own code (copying unrestricted), so this does not block
  anything. At vendor time record a content hash of each copied file + the source directory state in
  PROVENANCE instead of a commit sha.
- **Needs Anu (minor):** confirm this checkout corresponds to 3e0185a, or point to a git checkout,
  so PROVENANCE can cite the exact commit.

## OQ-6 - `consilience-verification` local HEAD is 275dba8 (spec says "HEAD")
III.2 pins this repo to "HEAD", and the local HEAD is `275dba8`. No conflict, but "HEAD" is not a
reproducible pin.
- **Safe default applied:** at vendor time, freeze the exact sha (`275dba8…`) into PROVENANCE so the
  build is reproducible regardless of future upstream movement. No action needed from Anu.

## OQ-7 - `refs_in/` does not exist yet
III.4 says cache downloaded references under `corpus_in/` and `refs_in/`; only `corpus_in/` exists.
- **Safe default applied:** create `refs_in/` in Phase 2 when the first reference is downloaded.
  No action needed now.
