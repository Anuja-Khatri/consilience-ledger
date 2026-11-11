# CHECKPOINT 2 (full, end of Phase 12) - for Anu, batched, non-interactive

The second human checkpoint: publish sign-off. Signed off (name, license) at the end of
Phase 8; this is the full update after the whole build. Publishing is HELD until your push
approval. Nothing has been pushed anywhere.

## 0. Final state (Phase 12)
All phases done and tagged phase-1 through phase-12. Public name: consilience-ledger. The
full build reproduces: `make reproduce` is byte-identical (schemas, rules.lock, ledger,
verdicts). 73 tests green. README carries "Independent work, not affiliated with or
endorsed by Lila Sciences." Stage 3 ran on a clearly-labeled SYNTHETIC simulator-lookup example
(two different materials looked up; not a fork) on the REAL OERSIM over the PUBLIC helao-async
oer13_cps dataset (13 base metals, no palladium; not Lila's data); the discovery report is
labelled NOT YET RUN (the search did not execute meaningfully). The writeback correction
(CONTRADICTION_DOSSIER.md / CORRECTIONS.md) is in place: 0 confirmed, 0 contradicted, 9
not_comparable. No composition is proposed anywhere.

## 1. State of the build
Stage 1 is complete through Phase 8 and reproduces locally. Phase 9 (safety format) is
done. Phases 10-11 scaffolding is in place and tested. Checkpoint 1 is resolved (your
triage decisions applied). Tags: phase-1 … phase-9. `make reproduce` regenerates the
schemas, rules.lock, ledger, and verdicts and the test suite is green.

## 2. What publishing entails (your decisions)
- **Public name.** The working name is `consilience-lab-extension`. The public name is
  your call (II.2).
- **License confirmation.** Code is MIT (`LICENSE`); data and reports are CC-BY-4.0
  (`LICENSE-DATA`) per D2. Confirm or override.
- **Lila's data.** `oer_exp_data.csv` is CC-BY but is NOT committed (your ruling / CC-28);
  it is loaded at runtime and cited by sha + row index. Keep it uncommitted on publish.
- **The two engine fixes** (validation.md wording, README v2 DOI) are your separate manual
  task in theconsilience-engine; this build never touched that repo.

## 3. What is honest to say publicly (numbers locked, II.3)
- The judge agrees exactly with an independent logic program (n=213) and SMT (n=311):
  locked Consilience numbers.
- Over 34 approved claims the ledger found 0 numeric forks and 561 vetoes. Most literature
  pairs are not comparable; the engine is designed to surface that, and the veto table is
  the headline result. This is a valid Stage 1 outcome (CC-22), not a failure.
- Every writeback comparison is a published veto: no claim's conditions were proven
  comparable to Lila's H-cell measurement. Verdicts use the H-cell data; the CP1 600s
  screening data is comparative, not absolute, and is not used to confirm or contradict.
  See CONTRADICTION_DOSSIER.md (the earlier screening-tier verdicts were corrected).
- The LLM-judge baseline made 4 comparisons the veto blocks on 60 sampled pairs.
- Fresh materials extraction-stability is 0.423 (n=52), reported as the materials number,
  distinct from the consciousness-domain 0.25.
- Nothing claims or implies Lila uses, wants, or endorses this work. Dan Guevarra agreed
  the need; he did not endorse. "Designed to," never "shown to," for anything not measured.

## 4. Status note
Checkpoint 1 is resolved, so Stage 1 outputs are APPROVED, not provisional. Stage 3's loop
runs on a clearly-labeled synthetic fork because zero real forks survived (CC-22); that
label must remain on any published Stage 3 artifact.

## 5. Not done (by design or by access)
- Discovery judging (Phase 11) and the full Stage 3 end-to-end are scaffolded; the
  discovery report runs when you want it. The corpus is the minimal accessible slice; most
  D5 references are paywalled (recorded in the manifest).
- STOP: no public publishing until you sign off here.
