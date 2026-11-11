# CHECKPOINT: consolidation into the public consilience-ledger

This records the consolidation that brought the later rounds (round 2 expanded corpus, the
database round, the round-robin round, the feasibility routes, and the closure) into this public
repository, with provenance. It started from HEAD 41b68b7 (clean tree). Nothing in round 1, the v1
ledger hash, the rules.lock, or the v1 `make reproduce` was changed. Nothing is pushed.

## Ground rules honored
- Only receipted numbers entered, each with its n and qualifier from the source lock or committed
  output. No number was deferred to OPEN_QUESTIONS.md, because every number used had a committed
  receipt.
- The superseded median-floor draft fork counts are described in words only; their digits appear
  nowhere in this repo. A repo-wide test enforces this (tests/test_consolidation.py).
- The round-robin is stated only as "0 to 4 forks at s = 15 mV" with its full qualifier, and led by
  the robust inter-lab central range of 90.7 mV (n = 9).
- No goal, hiring, outreach, or strategy language. No person names except publication authors and
  dataset maintainers. Lila Sciences appears only as cited publications at their stated values.
- No full-text paper files committed. MPS and paper data bytes are not committed; only derived
  tables and receipts, with CC BY 4.0 (CaltechDATA hjfx4-a8r81) and Tesch CC BY 3.0 attributions.
- Every ported or new document is free of the em dash (U+2014); the em-dash test now covers the new
  trees. SEED_APPROVAL.md and TIER_POLICY.md were not touched; they await the owner.

## Commits (local only, in order)
| stage | commit | message | files |
|---|---|---|---|
| A | e41b7e2 | round 2: expanded corpus, measured under-reporting, floors (ported with provenance) | 76 |
| B | 6635ad4 | round 4: database QC, verdict distribution, guardrail receipts | 7 |
| C | e14ee64 | round 5: round-robin known-answer run, corrected headline | 3 |
| D | d6f4cb1 | feasibility: data routes with Route 1 receipts | 23 |
| E | 944ffb4 | closure round ported; discovery replaced by the executed run (true null) | 13 |
| F | 35f1c94 | program history, merged corrections, limitations, checks extended | 9 |
| G | (this commit) | consolidation checkpoint | 1 |

## New and changed files by stage

### Stage A: rounds/round2-expanded-corpus/ (commit e41b7e2)
New: REPORT.md (written), PROVENANCE.md (written). Ported from ../ledger-v2 (unversioned, dates are
file dates): reports/ (K2_CENSUS, R2_PILOT_REPORT, R2_HARVEST_REPORT, R2_GATE3_REPORT,
GATE2_DECISIONS, GATE3_DECISIONS, FULL_CENSUS, A4_RECALL_REPORT), HARVEST_PREREG_K2.md, rules/
(comparability_rules_v2.yaml, rules.lock, CHANGELOG.md), r2_corpus/ (k2 and k40 harvest_manifest.json,
PROVENANCE.md), and the approved claim cards under cards/ (pilot 6, gate3 17, k2 7, reextract 17 of
which the census counts 10 as net new). Ported from ../r0 (unversioned): R0_REPORT.md, MPS_SURVEY.md,
GATE1.md, HARVEST_PREREG.md, FORK_CENSUS.md, RULES_PROPOSALS.md, CONDITIONS_DELTA.md, PROVENANCE.md,
sql/mps_survey.sql, harvest_census.py, harvest/ (census.json, cluster_facets.json). A4_RECALL_REPORT.md
had em dashes purged.

### Stage B: rounds/round4-database/ (commit 6635ad4)
New: REPORT.md (written), PROVENANCE.md (written). Ported from operator-v4 @ 5a1028e: NUMBERS_LOCK.json
(banned median-floor fork digits redacted to word-only per rule 2), compliance_rerun.json,
redteam_report.json (both verbatim), METHODS.md (relevant sections extracted, round-robin and
cross-field excluded, em dashes purged), CORRECTIONS.md (C-001 to C-003 and the superseded section
reworded per rule 2). In Stage F the ported NUMBERS_LOCK.json key honest_nulls was renamed to
stated_nulls.

### Stage C: rounds/round5-roundrobin/ (commit e14ee64)
New: REPORT.md (written; merges RRR_REPORT.md and CHECKPOINT_RR.md content, reworded per rule 2),
PROVENANCE.md (written). Ported from operator-v4 @ 5a1028e: rr_tesch_result.json (verbatim). In Stage
F one line was reworded to use the locked fragility bound 16.0 to 24.5 mV.

### Stage D: feasibility/caltech-lila-routes/ (commit d6f4cb1)
New: ROUTE1_SUMMARY.md (written), PROVENANCE.md (written port record). Ported from operator-v4 @
5a1028e: FEASIBILITY.md (purged), SOURCE_PROVENANCE.md (their provenance, purged), sql/ (10 files),
route1_receipts/ (RECEIPTS.md and two scripts purged; five CSV tables verbatim).

### Stage E: feasibility/closure/ and the discovery replacement (commit 944ffb4)
New closure files ported from operator-v4 @ 5a1028e: PREREG_CROSSFIELD.md, PREREG_KNOWN_ANSWER.md,
run_crossfield_search.py, test1_cards_and_verdict.json, test2_candidates.json (verbatim), CLOSURE_REPORT.md
(purged; null worded as a true null), MANIFEST.md (purged; consolidation notes appended), PROVENANCE.md
(written). The Test 2 cache stays local, re-derivable by the committed script. Rewritten:
discovery/report/report.md (now the executed run, a true null). Updated echoes: README.md, STATE.md,
LIMITATIONS.md, CHECKPOINT2.md (each now points at the executed run).

### Stage F: top-level documents and checks (commit 35f1c94)
Changed: README.md (Program history section), CORRECTIONS.md (merged C-001 to C-007 with dates and the
superseded-round line, reworded per rule 2; existing v1 corrections unchanged), LIMITATIONS.md (biology
untestable, ref 39 partial access, round 2 has no commit history, the measured ceiling), NUMBERS_LOCK.json
(13 new entries, each with n and qualifier), labext/numbers_lock.py (cleaner number tokenizer).
Tests: tests/test_consolidation.py (new: new-report numbers registered, banned tokens absent repo-wide,
ported JSON parses), tests/test_no_em_dash.py (extended to the round and feasibility trees).

## Test results
- Full suite: 79 passed (75 prior plus 4 new consolidation tests).
- make reproduce: byte-stable (schemas, rules.lock, ledger, verdicts regenerated; writeback 9
  not_comparable; suite green).
- v1 integrity: ledger/, schema/, and rules/ are byte-identical after reproduce (no drift).

## Open questions
Nothing was deferred to OPEN_QUESTIONS.md: every number used carried a committed receipt. Three items
are flagged for the owner's review and are recorded in feasibility/closure/MANIFEST.md, not as number
conflicts: the two closure Test 1 claim cards await review, so the O3 verdict is provisional; ref 39
(Cherevko) was abstract-level access only (recorded as partial); and the reextract card directory holds
17 agreed-provisional cards of which the census of record counts 10 as net new after provenance dedup.

Nothing is pushed; the owner reviews this diff, resolves open questions, and pushes.
