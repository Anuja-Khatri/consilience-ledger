# MANIFEST - closure round (access routes + receipts)

Retrieval 2026-11-11. Locked rails: no model API calls (dual-model extraction replaced by a single
manual typed extraction; the judge is the deterministic engine, no model). No pirate mirrors.

## Test 1 - access route per paper
- **Ref 40 (Peng, PMC10035503)**: FULL TEXT via **Europe PMC REST** (official open route),
  `/webservices/rest/PMC10035503/fullTextXML` (86 KB). Open access.
  - Extracted: electrolyte **1 M HClO4 (pH 0)**; **overpotential 196 mV @ 10 mA cm-2**; mass activity
    407.2 A/g @ 1.53 V_RHE; **degradation 66 µV h-1**; Ag/AgCl ref, Pt counter, 10 mV/s, glassy
    carbon; "at different temperatures" (25/40/55 °C); entity = hierarchical nanostructured Pd (~2.8 nm).
  - Note: Peng's own dissolution test states "Pd is extremely stable at low pH under steady-state".
- **Ref 39 (Cherevko, 10.1002/cctc.201402194)**: access order attempted -
  (a) Wiley SI page → **HTTP 403** (bot block; not evaded);
  (b) Zeradjanin **Academia.edu** copy (/25083585/) → **HTTP 403** (login/bot wall; not evaded);
  (c) → **ABSTRACT via Crossref** (official metadata route). **ACCESS = PARTIAL** (abstract only; SI
    not retrieved).
  - Extracted (abstract): axis = **dissolution rate** (transient + steady-state) and Tafel slope;
    entity = **polycrystalline** noble metals; key: "on metals for which oxygen evolves directly from
    adsorbed water, such as Pt and presumably **Pd, the Tafel slopes are high and the dissolution
    rates are low**." Numeric dissolution value sits in the unretrieved SI.

## Test 1 - receipts
- Typed cards + deterministic verdict: `test1_cards_and_verdict.json`.
- Judge (engine.verdict.compare_pair, rules CR1-CR5 + CR-ID, hash-locked): **not_comparable**,
  defect **axis_mismatch** ("overpotential_at_current_density vs dissolution_rate"). Cross-source
  (different source_id); same composition entity (Pd=1.0) but the axis gate precedes entity/CR.
- Both cards CONTESTED (ref39 number in unretrieved SI; ref40 OER measurement temperature ambiguous)
  → routed to the review queue for Anu, NOT self-approved; no fork manufactured.

## Test 2 - route + receipts
- Sources: **arXiv API** (cat cond-mat.mtrl-sci OR physics.chem-ph) and **Semantic Scholar** (FoS
  Materials Science/Chemistry). 10 structural queries (2-5 words, vocabulary-stripped). **20 of 40**
  query-calls used. Cached + resumable: `cache/` (10 arxiv + 10 s2).
- **arXiv**: 60 candidates, **56/60 = 93% on-topic** by title.
- **Semantic Scholar**: all 10 responses **EMPTY** (shared-pool rate-limit); contributed 0. arXiv
  carried the executed run.
- Candidates: `test2_candidates.json`. Runner: `run_crossfield_search.py`.

## Owner review (11 Nov 2026)

Owner review, 11 Nov 2026: both cards corrected on review. On the Peng card the two stated conditions (10 mA cm-2; 1 M) were filled. On the Cherevko card the invented numeric quantity (0.0 ng/cm^2/s) was removed; the abstract states only that dissolution rates are low, so the claim is recorded as a qualitative claim with the authors' hedge 'presumably Pd' noted here. Consequence, stated plainly: the original run's defect label (axis_mismatch) was computed on the pre-review cards; on the corrected cards the judge refuses the pair as type_mismatch, because a quantitative claim and a qualitative claim are different claim types. The top-level verdict is unchanged (not comparable), the cards' axes remain different (dissolution_rate versus overpotential_at_current_density, recorded on the cards), and the preregistered outcome remains O3: the papers do not disagree. Cards APPROVED by the owner.

## Owner-review items (consolidation record)
- Ref 39 (Cherevko) access: abstract-level only; the full text and SI routes were refused (HTTP 403), so its access is recorded as partial.
- O3 and the two cards: on owner review (11 Nov 2026) the two Test 1 claim cards were corrected and approved (see Owner review above); the preregistered outcome O3 stands.
- reextract 17-vs-10 dedup: the reextract card directory holds 17 agreed-provisional cards of which the census of record counts 10 as net new after provenance dedup.

## Consolidation provenance notes (added for the public record)
- The preregistrations and the results were committed together in the source repo in a single commit; precedence rests on the in-file dating and the preregistration text, written before reading (Test 1) and before running (Test 2).
- Test 1's claim cards came from a single manual typed extraction by the reader, because model API calls were barred by the locked rails; disclosed as a deviation from the dual-model extraction used elsewhere.
- The Test 2 cache (arXiv and Semantic Scholar responses) is not committed; it stays local and is re-derivable by the committed script run_crossfield_search.py.
