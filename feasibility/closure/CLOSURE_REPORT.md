# CLOSURE_REPORT - two tests

## Test 1 - known-answer pair (feature 7): ref 39 (Cherevko) vs ref 40 (Peng)

**Prereg** (`PREREG_KNOWN_ANSWER.md`, written before reading). Three outcomes: **O1** judge finds a
fork on a shared axis with stated conditions on both sides; **O2** judge refuses and names the
missing/mismatched condition fields; **O3** once typed, the papers do not disagree (different axes -
e.g. dissolution rate vs overpotential/durability - or compatible claims). Dated prior: abstracts
suggested ref 39 reports Pd dissolution comparatively low, so **O3 was flagged a live possibility
before reading**.

**Outcome: O3.** Ref 40 (Peng, PMC10035503, full text) reports Pd on the axis
**overpotential-at-current-density** (196 mV @ 10 mA cm⁻², 1 M HClO₄) and durability (66 µV h⁻¹).
Ref 39 (Cherevko, abstract; SI not retrievable → partial access) reports noble metals on the axis
**dissolution rate**, and states Pd's "dissolution rates are low". The deterministic judge
(`compare_pair`, rules CR1–CR5 + CR-ID) returns **not_comparable / axis_mismatch**
("overpotential_at_current_density vs dissolution_rate"); both cards were contested and routed to the
review queue, so no fork was manufactured. The two papers also agree where they touch (both: Pd
comparatively stable in acid). This is O3.

**Root cause (one sentence):** The pair was never a disagreement - the two papers measure different
things (ref 39 how fast Pd dissolves, ref 40 Pd's overpotential and durability), and where they
overlap they agree that palladium is comparatively stable in acid.

## Test 2 - cross-field search (feature 23), actually run

**Prereg** (`PREREG_CROSSFIELD.md`, written before running). The earlier attempt sent full sentences
to a keyword API, hit rate limits, and returned particle-physics papers - it never ran. Fix:
vocabulary-stripped SHORT structural queries (2–5 words) to arXiv (cond-mat, physics.chem-ph) and
Semantic Scholar (field-of-study filter), cap 40 queries, cached, resumable. Target: the durability
of the lead catalyst via its operando-formed needle-like nanostructure. Executed-only-if **≥ half of
retrieved candidates are on-topic by title**; the matcher then grades each candidate with a rung and
a ceiling; valid outcomes are matches at a stated rung (with chance context) **or** nothing above
rung 3 (a true null).

**Outcome: executed, true null (nothing above rung 3).** 20 of 40 query-calls used; **56 of 60
candidates (93%) on-topic** by title → the run **counts as executed** (the earlier failure is fixed).
Semantic Scholar rate-limited to empty; arXiv carried the run. Grading against the target mechanism
graph (operando process → anisotropic nanostructure → operational durability): the closest hits are
**same-field topical adjacency** (structure→stability in electrocatalysts, e.g. defect partitioning
to stabilise PtAu, operando degradation studies), none presenting the same mechanism as a cross-field
correspondence with disjoint vocabulary. **Nothing rises above rung 3.** Chance context: a 93%
on-topic rate is expected by construction (the queries were electrochemistry-structural), so topical
overlap carries no correspondence signal, and 0 of 60 are isomorphic-mechanism matches.

**Root cause (one sentence):** With the full-sentence queries replaced by short structural ones the
search finally runs and returns on-topic materials papers, but none carries the same operando
nanostructure-to-durability mechanism as a genuine cross-field match, so the result is a true
null.

## Owner review (11 Nov 2026)

Owner review, 11 Nov 2026: both cards corrected on review. On the Peng card the two stated conditions (10 mA cm-2; 1 M) were filled. On the Cherevko card the invented numeric quantity (0.0 ng/cm^2/s) was removed; the abstract states only that dissolution rates are low, so the claim is recorded as a qualitative claim with the authors' hedge 'presumably Pd' noted here. Consequence, stated plainly: the original run's defect label (axis_mismatch) was computed on the pre-review cards; on the corrected cards the judge refuses the pair as type_mismatch, because a quantitative claim and a qualitative claim are different claim types. The top-level verdict is unchanged (not comparable), the cards' axes remain different (dissolution_rate versus overpotential_at_current_density, recorded on the cards), and the preregistered outcome remains O3: the papers do not disagree. Cards APPROVED by the owner.
