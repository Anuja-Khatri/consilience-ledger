# K2 harvest preregistration (Gate 3) - written before running

Goal (Anu): 20 open-access acidic-OER papers whose FULL TEXT states an iR-compensation
practice, prioritizing commercial RuO2 / IrO2 baseline measurements in 0.5 M H2SO4 and
0.1 M HClO4. The point is condition-complete claims (iR fraction stated) that CAN fork,
unlike the K40 set where iR was unstated in 71% of claims.

## Europe PMC query (verbatim, run unchanged)
`("oxygen evolution" OR OER) AND (RuO2 OR IrO2 OR "ruthenium oxide" OR "iridium oxide") AND
(acidic OR "H2SO4" OR "HClO4" OR "sulfuric acid" OR "perchloric acid") AND (overpotential) AND
("iR" OR "ohmic" OR "compensation") AND (OPEN_ACCESS:y) AND (HAS_FT:y) AND (IN_EPMC:y)
NOT (PUB_TYPE:"review")`

## Post-filters (full text, deterministic)
1. F2 review detection (article-type + review prose) -> exclude.
2. F1 acid measurement context (named strong acid present) -> exclude alkaline-only.
3. states_ir_practice(full_text) must be TRUE: the text must contain an iR/ohmic-compensation
   PRACTICE statement (a verb/percentage/"not applied"), not merely the token. Papers that only
   mention iR in passing are excluded.
Prioritization within the pass set: papers whose full text also mentions a RuO2/IrO2 baseline
are selected first (mentions_baseline), then the remainder, to maximize the commercial-baseline
cross-paper cluster. Deterministic PMCID-sorted within each priority tier.

## Selection
Up to 20 papers, attempt-capped. No silent shortfall: if fewer than 20 pass, that is reported.
Licenses + SHA-256 recorded in r2_corpus/k2/harvest_manifest.json. Official route only.
