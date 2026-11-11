# B1 OA harvest: preregistered query wording (R0, written before running)

Governs: strategy section 2 (B1), section 6 (R0). Research only; no extraction here, a
census of counts only. Supersession S1 (corpus = the field) takes effect at Gate 1, not
now; this preregistration records the exact wording so the Gate-1 harvest is reproducible.

## Inclusion criteria (fixed before counting)
A record counts if it is a study of the oxygen evolution reaction (OER) in ACIDIC
electrolyte (sulfuric acid, perchloric acid, or stated pH < 3), reporting an overpotential
or a stability metric, on a catalyst whose primary active metal is palladium (Pd),
ruthenium (Ru), or iridium (Ir). Reviews are counted separately (they carry secondary
claims, D8). Counting is at the record level; de-duplication across sources is by DOI.

## Per-source query strings (verbatim, to be run unchanged at Gate 1)
- Europe PMC (REST search API, resultType=lite, synchronous paging):
  `("oxygen evolution" OR OER) AND (acidic OR "sulfuric acid" OR "perchloric acid" OR "0.5 M H2SO4" OR "0.1 M HClO4") AND (overpotential OR "current density" OR stability) AND (palladium OR ruthenium OR iridium OR Pd OR Ru OR Ir)`
  Per-metal refinement: append `AND <metal-term>` for Pd, Ru, Ir separately.
  Accessible-fulltext count = the same query AND `(OPEN_ACCESS:y)`.
- arXiv (export API, search_query):
  `all:"oxygen evolution" AND all:acidic AND (all:palladium OR all:ruthenium OR all:iridium) AND (all:overpotential OR all:electrocatalyst)`
  All arXiv records are open-access full text.
- ChemRxiv (public API, term search):
  term=`acidic oxygen evolution overpotential` filtered client-side to Pd/Ru/Ir in title or
  abstract. All ChemRxiv records are open-access full text.

## Counting method
Report, per source and per metal (Pd, Ru, Ir): total matching records, and the
accessible-fulltext subset. A record matching more than one metal is counted under each
metal but once in the de-duplicated total. Query total cap recorded; searches cached.

## Known limits (honest)
Europe PMC and arXiv keyword search are lexical, not semantic, so counts are upper bounds
(false positives from the keywords) and lower bounds for papers that state conditions only
in the body. These counts size the harvest; they are not the harvested corpus.
