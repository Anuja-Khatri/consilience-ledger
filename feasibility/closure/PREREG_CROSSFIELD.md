# PREREG_CROSSFIELD - Test 2 (feature 23), actually run

Written **2026-11-11, BEFORE running any query.** Locked honesty rails apply (no model API calls;
search APIs and open retrieval are in scope for this test).

## What the earlier attempt did wrong (the exact bug to fix)
It sent **full sentences** to a keyword API, hit rate limits, and returned **particle-physics**
papers; it never truly ran. Fix: **vocabulary-stripping** → SHORT structural queries (2–5 words
each), field-scoped sources, a hard query cap, cached + resumable.

## Target question (from the locked plan)
The **durability of the lead catalyst (InMnPdOx) via its operando-formed needle-like nanostructure**
- i.e. does a structure→durability mechanism of this shape appear in adjacent literature.

## Protocol
- **Vocabulary-stripping**: reduce the mechanism sentence to 2–5 word STRUCTURAL queries (drop
  system-specific nouns like In/Mn/Pd; keep the structural relation, e.g. "needle nanostructure
  stability", "operando nanostructure formation", "morphology durability oxide", "anisotropic
  oxide corrosion").
- **Sources**: arXiv API (categories **cond-mat**, **physics.chem-ph**) and **Semantic Scholar**
  (with a **field-of-study filter**: Materials Science / Chemistry).
- **Cap**: **40 queries total**, across both sources. All responses **cached** to
  `feasibility/closure/cache/`; the run is **resumable** (skip a query whose cache file exists).

## Executed-vs-not criterion (the gate the earlier run failed)
The run **counts as executed only if at least HALF of the retrieved candidates are on-topic by
title** - materials, electrochemistry, degradation, or mechanism-adjacent. If < half are on-topic,
the run is **NOT executed** (same failure class as before) and that is reported as such, not as a
null.

## Grading and valid outcomes
If executed, the **matcher grades every candidate with a rung and a ceiling** (the four-rung
correspondence ladder; ceiling never licenses ontological identity). Valid outcomes, both of which
are results:
- **matches at a stated rung**, reported **with chance context** (how many candidates, how many
  would match by chance at that rung); or
- **nothing above rung 3** → a **true null**.
