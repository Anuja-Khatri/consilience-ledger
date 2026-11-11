# consilience-ledger

Operating or building an autonomous lab? Start with [FOR_AUTONOMOUS_LABS.md](FOR_AUTONOMOUS_LABS.md).

**Independent work, not affiliated with or endorsed by Lila Sciences.**

## In plain words

I built a system that compares scientific claims carefully. A language model reads a sentence
from a paper or a database and turns it into a card: what material, what was measured, what
number, under what conditions. The judge, a second part, is plain code with no AI inside: it
compares two cards, gives the same answer every time, and refuses the comparison when the
conditions do not match, naming the reason. A third part checks a lab plan against safety
rules before the plan runs.

This repository is one arm of The Consilience, an instrument I build for comparing
scientific claims across fields that do not share a vocabulary. The core engine and its
validation are described in the paper: Consilience: Deterministic Cross-Theory Claim
Comparison (Zenodo, DOI 10.5281/zenodo.23672883). This repository extends that engine to
the literature and data of autonomous laboratories.

The main finding so far is honest and useful: most published results cannot fairly be compared
at all, because papers do not state the conditions. Where I planted real disagreements as a
test, the system found all of them, and on clean data it invented none. The exact numbers,
each with its sample size, are on the front page and in `NUMBERS_LOCK.json`.

One rule governs this repository: every public number carries its sample size, tests fail the
build if a number drifts, and my mistakes are listed in `CORRECTIONS.md`. Code is MIT
licensed; text and data are CC BY 4.0.

To check it yourself:

    git clone https://github.com/Anuja-Khatri/consilience-ledger.git
    cd consilience-ledger && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    make reproduce

It rebuilds byte for byte and the tests pass, including two that openly skip because the data
they need is deliberately never committed.

A live, read-only browser over the round 1 ledger is served from this repository by GitHub
Pages: https://anuja-khatri.github.io/consilience-ledger/browser/

### Map of this repository

Start with `FOR_AUTONOMOUS_LABS.md` and this README. The results live in `ledger/`, `rounds/`,
`feasibility/` and `reports/`. The receipts live in `NUMBERS_LOCK.json`, `CORRECTIONS.md`,
`PREREGISTRATION.md`, the CHECKPOINT files, `DECISIONS.md` and `STATE.md`. The code is
`labext/` with `tests/` and the Makefile; `vendor/` holds upstream code with its provenance;
`schema/` and `rules/` hold the data contracts and the comparison rules. Everything else is
the working record of how this was built, kept public on purpose: in a repository about
verifiable claims, the process files are part of the evidence.

## The technical record

Everything below is the precise record, kept in the project's internal vocabulary for people
verifying the work. Codes such as D4, CC-28 or II.3 are internal decision references; the
checkpoint files and `DECISIONS.md` define them.

Signed off at Checkpoint 2. License: code MIT (`LICENSE`); data and reports CC-BY-4.0
(`LICENSE-DATA`). Lila's instrument data is not committed; it is loaded at runtime and
cited by sha256 and row index (CC-28).

## What this is
A deterministic, open hypothesis-comparison engine extended to the published
literature of closed-loop autonomous laboratories, with acidic oxygen evolution
(OER) as the concrete instance. A language model extracts claims into typed
fields. A deterministic judge compares them. The judge has no text channel. Before
two quantitative claims may be called a disagreement, their measurement conditions
must be proven comparable; if they are not, the pair is vetoed with a named defect.

## The determinism split (D4, important)
Extraction is NOT claimed deterministic. It is gated by cross-model agreement and a
human review queue. The pipeline from APPROVED CLAIM CARDS onward IS byte
deterministic: the same approved cards plus the same rules version produce an
identical ledger hash. The README and METHODS state this split plainly and never
claim end-to-end determinism (CC-01).

## Status (Stage 1 complete through Checkpoint 2; Stage 3 loop ran on public data)
- Phase 0 inventory; Phase 1 judge + conditions veto; Phase 2 real dual-model extraction
  + D6 pilot; Phase 3 Checkpoint 1 (Anu's batch applied); Phase 4 ledger; Phase 5
  writeback; Phase 6 LLM-judge baseline; Phase 7 evaluation discipline; Phase 8 browser +
  this finalisation. Phase 9 safety format. **Phase 10 loop ran end to end** on the PUBLIC
  helao-async `oer13_cps` dataset (13 base metals, no palladium; not Lila's data), on a
  clearly-labeled SYNTHETIC simulator-lookup example (two different materials; not a fork).
  **Phase 11 discovery: executed, true null** - the structure-directed search was fixed and
  run (short structural queries), and nothing rose above rung 3 (see
  discovery/report/report.md and feasibility/closure/CLOSURE_REPORT.md).
- The two human checkpoints are the advertised integrity mechanism. Checkpoint 1 is
  resolved (Anu's decisions applied). Checkpoint 2 is signed off. This repository is public
  (github.com/Anuja-Khatri/consilience-ledger).

## Results (numbers from NUMBERS_LOCK.json, each with its n and qualifier, II.3)
- Judge: 1.0 agreement vs an independent logic program (n=213) and vs SMT (n=311); these
  are locked Consilience numbers, cited as such.
- Corpus (real): two accessible papers (their paper and ref 40); the rest paywalled and
  excluded. The D6 pilot returned NO-GO twice (iR-correction is stated in few result
  sentences), so the corpus is the minimal accessible slice.
- Ledger over 34 approved claims: 0 numeric forks, 561 vetoes (515 axis_mismatch, 149
  condition_unstated, 3 condition_mismatch). The veto table is the headline result: most
  literature pairs are not comparable, so they are not called disagreements. This is
  designed to surface exactly that, and it does.
- Writeback vs Lila's own H-cell data (loaded at runtime, not committed): every comparison
  is a published veto. No claim's conditions were proven comparable to an H-cell
  measurement (the CP1 600s screening data is comparative, not absolute, and is not used to
  confirm or contradict). The published pure-Pd claims are among the vetoes. See
  CONTRADICTION_DOSSIER.md.
- Durability self-consistency check (InMnPdOx, the authors' own Fig. 3e trace): max 0.5055 V
  at 575.5 h, 0 of 84 points above the 0.513 V threshold (the claim's 0.5 V ceiling plus the
  standing 13 mV floor), so within_floor, consistent within +/- 13 mV. A self-consistency check
  (the authors' claim vs the authors' own data), not independent confirmation. See
  reports/durability_check_2609.30133.md.
- LLM-judge baseline: on a preregistered sample of 60 vetoed pairs, a model call made 4
  comparisons the deterministic veto blocks.
- Fresh materials extraction-stability: 0.423 (n=52, test-retest). This is the materials
  number, reported fresh; it is not the consciousness-domain 0.25 (different domain and
  metric).

## Program history
The public record spans several rounds. Each line links its tree.

- Round 1 (this root): 34 approved claims, 561 refused pairs each with a recorded reason, 0
  forks, and the durability self-consistency check within floor. See `ledger/` and
  CONTRADICTION_DOSSIER.md.
- Round 2 (`rounds/round2-expanded-corpus/`): 73 approved cards, 210 vetoed pairs, the measured
  under-reporting table, and 0 forks. A reproducibility floor is also measured on MPS.
- A superseded intermediate database round existed and was replaced; the superseded fork counts
  are described in words only, see CORRECTIONS.md.
- Round 4 (`rounds/round4-database/`): the database quality-control pass and the full committed
  verdict distribution.
- Round 5 (`rounds/round5-roundrobin/`): the round-robin known-answer run, led by the robust
  inter-lab central range.
- The closure (`feasibility/closure/`): the known-answer pair (O3) and the executed cross-field
  search (a true null).

## Browse
Open `browser/index.html` from any local file server (it reads `ledger/*.json` by relative
fetch). Phases and the full method are in STATE.md, METHODS.md, and the spec.

## Layout
See the spec Part IV. Code lives in `labext/`; vendored upstream code in `vendor/`
with `PROVENANCE.md`; data contracts as JSON Schema in `schema/`; comparability
rules in `rules/`; the materials capability map in `domainpack/materials_oer/`.

## Develop
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    make test          # run the suite
    make schemas       # regenerate JSON Schema from the pydantic models
    make lock          # regenerate rules/rules.lock

## Honesty
Numbers in any outgoing text come only from the locked registry or Lila's own
publications, each with its n and qualifier (II.3). "Designed to," never "shown
to," for anything not measured. Nothing here claims or implies that Lila Sciences
uses, wants, or endorses this work.
