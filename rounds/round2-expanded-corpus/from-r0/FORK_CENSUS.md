# Candidate fork-cluster census and review-load projection (R0)

Research-only sizing. No literature claims are extracted in R0 (that is R2), so the
literature fork counts here are PROJECTIONS from preregistered API census counts plus the
v1 extraction pilot rates, not enumerated forks. Structured-source clusters are counted
directly from the loaded data. A candidate fork cluster = same axis (OER overpotential),
same electrolyte identity, same current-density convention, with 2+ independent sources.

## 1. The four fork sources, with R0 liveness verdicts
Strategy section 4 names four independent fork sources. R0 findings update their status:

1. **Literature x literature within one acid (B1, B2)** - PRIMARY, LIVE, large.
   Six well-populated candidate clusters (OA, electrolyte-matched, 10 mA/cm2;
   `harvest/cluster_facets.json`, upper-bound lexical counts):
   | metal | 0.5 M H2SO4 & 10 mA | 0.1 M HClO4 & 10 mA |
   |---|---|---|
   | Pd | 264 | 121 |
   | Ru | 466 | 207 |
   | Ir | 597 | 253 |
   Each cluster has hundreds of nominal members - orders of magnitude more than the 2+ a
   fork needs. Even after discounting for lexical false positives and for the "insignificant
   fraction" that actually report comparably (B3), every cluster clears the bar. The prior
   against zero forks is strong. Which exact pairs fork is an R2 result.

2. **Literature x McCrory standard set (A3)** - LIVE pending retrieval.
   McCrory = 26 catalysts under one protocol in acid and alkali; the single cleanest anchor.
   A3 data not retrieved in R0 (ACS SI route; FOR_ANU.md item 1). Once in, every acidic
   McCrory catalyst becomes a condition-matched anchor against the B1 clusters above.

3. **Literature x MPS rows (A1)** - LIVE for non-noble oxides only; NULL for Pd/Ru/Ir.
   MPS acidic data is earth-abundant metal OXIDES (Co/Mn/Ta/Sb/Fe/Sn/Ce/Ni...), **zero
   Pd/Ru/Ir** (MPS_SURVEY.md). Under the current Pd/Ru/Ir harvest scope, A1 x B1 does NOT
   overlap on active metal. A1 x B1 becomes live only if Anu widens the harvest to
   non-noble acidic-OER oxides (a Gate-1 scope choice). What A1 adds regardless: the
   empirical floor, and source 5 below.

4. **Claims x Lila's own data (A2)** - LIVE on two axes.
   Lila's paper is *Ir/Ru-free palladium-oxide catalysts for acidic OER*; data are acidic
   CP overpotential (`overpotential_cp1_600s_mean`) on Pd-oxide and earth-abundant oxides
   (Co-Mn-Nb, Ni-Sn-Nb, In-Mn-Pd). A2 x B1 is live on the Pd-in-acid axis (connects to the
   ref 39/40 Peng Pd pair the strategy keeps). A2 also anchors source 5.

5. **(NEW, found in R0) Structured x structured: MPS (A1) x Lila (A2)** - LIVE, large.
   Both are acidic CP-overpotential metal-oxide datasets from the same JCAP/Gregoire HTE
   lineage, so they are condition-comparable by construction. Concrete composition overlap
   in the loaded MPS acidic set (distinct samples):
   Co+Mn **72,547**; Co+Mn+Fe 22,872; Ni+Fe 17,385. (Lila's Nb, In, Sn-pairings are absent
   from MPS acidic: Ni+Sn 0, In 0, Nb 0 - so matches are on the Co-Mn / Ni-Fe backbone, with
   the third element a composition-axis difference the ledger flags, not a fork.) This gives
   a structured-only fork path that needs **zero literature extraction** and only two dataset
   mapping approvals.

## 2. Structured-source candidate blocks counted directly
- MPS-internal condition-matched blocks (same composition 0.05-rounded + electrolyte + CP
  stage, >=3 members): 9,709 blocks. These are the replicate-floor blocks, not forks (one
  source), but they are the denominator for how many A1 blocks a literature or Lila claim
  could match into.
- A1 x A2 Co-Mn-oxide acidic block: ~72k MPS samples available to match Lila's Co-Mn-Nb
  points - the largest single structured fork candidate.

## 3. Review-load projection
Two regimes, per the S2 tiered gate.

### Structured rows: ONE mapping approval per dataset (not per row)
Admitting the entire structured universe costs, in human decisions:
| dataset | rows admitted (approx) | Anu decisions |
|---|---|---|
| A1 MPS acidic CP overpotential | 152,133 | 1 column-mapping approval |
| A2 Lila acidic CP overpotential | ~1,125 screening + H-cell | 1 column-mapping approval |
| A3 McCrory | ~26 (x acid/alkali) | 1 column-mapping approval |
| A4 437-point curated (pending id) | ~437 (SECONDARY) | 1 column-mapping approval |
Total: **~153,700 claims admitted for 4 human approvals.** This is the economic point of the
whole v2 plan (strategy section 3) and it holds up against the real MPS row count.

### Paper-text claims: triaged per-claim review, sized from the v1 pilot
v1 pilot measured (lab-extension PILOT_REPORT): 2 accessible papers -> 70 approvable + 72
contested numeric claims, auto-agreed 0 (field-exact across two model families, strict).
Rates: ~71 numeric claims/paper; ~36 contested/paper pre-triage; agreement-v2 auto-accept
rate still unmeasured at scale (the 3-paper pilot the strategy mandates will set it).
Projection of Anu's contested queue, before triage compression, at three harvest depths:
| papers extracted (K) | raw claims ~71K | contested ~36K to review |
|---|---|---|
| 10 | ~710 | ~360 |
| 50 | ~3,550 | ~1,800 |
| 100 | ~7,100 | ~3,600 |
Triage (agreement-v2 auto-accept + the CP1-triage batching Anu already used, 34/72 approved
in one pass) is what makes these tractable; the pilot must measure the auto-accept rate
before R2 commits to a K. Blocking by (metal, electrolyte, current density) keeps pairwise
judging inside the six clusters above, never all-pairs over 3,478 records.

### Recommended R2 entry point (for Anu to accept/modify at Gate 1)
Start literature extraction on the single best-populated comparable cluster
(Ir / 0.5 M H2SO4 / 10 mA, ~597 OA records) as the 3-paper pilot, because it maximizes the
chance of an early real literature-vs-literature fork; run the structured A1 x A2 Co-Mn block
in parallel as the zero-extraction fork path. Both are live today; neither needs A3 or A4.

## 4. Honesty note
All B1 and cluster counts are lexical upper bounds (keyword search, not semantic; a record
matching the electrolyte string may not report eta at 10 mA/cm2 comparably). They size the
harvest and bound the review load; they are not a claim that N forks exist. The zero-forks
contingency (strategy section 7) remains preregistered.
