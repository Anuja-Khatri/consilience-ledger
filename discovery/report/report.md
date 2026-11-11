# Cross-field correspondence report (discovery) - executed run, true null

Status: executed. This run replaces the earlier "not yet run" placeholder. The cross-field
structural search was fixed and actually run, and it returned a true null: nothing rose above
rung 3. The full receipts are in `feasibility/closure/` (CLOSURE_REPORT.md Test 2, PREREG_CROSSFIELD.md,
run_crossfield_search.py, test2_candidates.json).

## What was fixed
The earlier attempt sent full source sentences to a keyword API, hit rate limits, and returned
unrelated particle-physics papers, so it never ran. The fix, preregistered before running, replaces
those with short structural queries (2 to 5 words, vocabulary-stripped) to arXiv (cond-mat and
physics.chem-ph) and Semantic Scholar, capped and cached. The run counts as executed only if at
least half of the retrieved candidates are on-topic by title.

## What the run did
- 20 of 40 query-calls were used.
- 56 of 60 candidates were on-topic by title (93 percent), so the execution gate passed.
- Semantic Scholar was rate-limited to empty responses; arXiv carried the run.

## The result: a true null
The matcher graded each candidate against the target mechanism graph (an operando process forming an
anisotropic nanostructure that yields operational durability). The closest hits are same-field
topical adjacency (structure-to-stability in electrocatalysts), none presenting that mechanism as a
cross-field correspondence with disjoint vocabulary. Nothing rises above rung 3, and 0 of 60 are
isomorphic-mechanism matches.

Chance context: a 93 percent on-topic rate is expected by construction, because the queries were
themselves electrochemistry-structural. Topical overlap of this kind carries no correspondence
signal. The result is therefore a true null: the search ran, returned on-topic materials papers, and
found no genuine cross-field mechanism match.
