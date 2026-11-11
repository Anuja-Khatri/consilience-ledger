# R0_REPORT - consilience-ledger v2, phase R0 (research only)

Date 2026-11-10. Author Claude, from live retrieval. Phase R0 per strategy section 6:
research only, no pipeline code, no change to the consilience-ledger repo, nothing pushed.
All sources are openly licensed public scientific data and open-access papers, retrieved
only through official routes (CaltechDATA download, Europe PMC API, arXiv API). Anything not
openly available is on FOR_ANU.md, never worked around. Gate-1 decisions are Anu's; this
report is the packet for them. Supporting files are all under `BUILD_ROOT/r0/`.

## 0. Deliverables produced (all in r0/)
- PROVENANCE.md - license receipts + SHA-256 for every artifact.
- HARVEST_PREREG.md - preregistered B1 query wording (pre-existing, honored).
- harvest_census.py + harvest/census.json + harvest/cluster_facets.json + harvest/raw/ - B1 census.
- downloads/ - MPS dump + CaltechDATA record metadata.
- MPS_SURVEY.md + sql/mps_survey.sql - the A1 survey (coverage, keys, empirical floor).
- FORK_CENSUS.md - the four (now five) fork sources, candidate clusters, review-load projection.
- CONDITIONS_DELTA.md - the one proposed vector change (ir_correction -> fraction).
- RULES_PROPOSALS.md - page-sourced comparability rules CR-A..CR-E and CR5.
- READING_NOTES.md - v1 reading queue completed (ESAMP, ref 27, B2, B3; refs 4/15/16 excluded).
- OPEN_QUESTIONS.md - OQ-R0-1..8, each with a safe default applied.
- FOR_ANU.md - manual-fetch / manual-action list.
- papers/ - fetched open-access full texts (B2, B3, ESAMP, ref 27).

## 1. Licenses, verified with receipts (PROVENANCE.md)
- A1 MPS CaltechDATA hjfx4-a8r81: CC-BY-4.0. 4,521,364,439-byte archive, size-matched,
  SHA-256 b988d2c4...e668da. Guevarra co-author confirmed (Lila lineage claim holds).
- A2 lila_oer_manuscript: code MIT, data CC-BY-4.0 (local clone; data not committed).
- B2 PMC13707403 cc-by; B3 PMC10576816 cc-by; ESAMP PMC10079965 cc-by;
  ref 27 PMC10012258 cc-by-nc-nd (readable, no redistribution).
- A3 McCrory SI, A4 437-point set, refs 4/15/16, ChemRxiv census: not openly retrievable by an
  automated route -> FOR_ANU.md. No byte of any paywalled source was used.

## 2. Headline findings
1. **MPS loaded and surveyed.** 3.43 GB plain SQL into local PostgreSQL; 12,159,999 samples,
   3,980,832 analyses (2,713,725 FOM-type). Clean load, 0 errors.
2. **Acidic-OER coverage is real but non-noble.** 152,133 acidic CP overpotential measurements
   on 102,148 samples (H2SO4 / pH<3), all earth-abundant metal OXIDES (Co 92.9k, Mn 74.8k, Ta
   66.1k, Sb, Fe, Sn, Ce, Ni ...). **Pd in 8,448 samples store-wide but 0 under acidic
   conditions; Ru 0; Ir 0.** MPS cannot supply Pd/Ru/Ir forks (OQ-R0-4) - a material Gate-1 input.
3. **Empirical replicate floor measured.** Within-lab acidic-OER overpotential reproducibility
   is ~22 mV (strict same-sample repeat) to ~51 mV (same-composition block) median, p90 > 130
   mV - far above the stated 13 mV. First-party evidence for S3.
4. **B1 census.** Europe PMC: 4,182 acidic-OER Pd/Ru/Ir records, 3,478 open-access (Pd 1,436 /
   Ru 1,946 / Ir 2,792 OA). arXiv: ~1 (negligible; arXiv barely covers this field).
   ChemRxiv: blocked (FOR_ANU). Six well-populated candidate clusters (metal x acid x 10 mA/cm2),
   each hundreds of records - the prior against zero forks is strong.
5. **A fifth fork source found: A1 x A2.** MPS and Lila are both acidic CP-overpotential
   metal-oxide datasets from the same JCAP/Gregoire lineage; MPS has 72,547 Co+Mn acidic oxide
   samples overlapping Lila's Co-Mn chemistry. A structured-only fork path needing zero
   literature extraction and two mapping approvals.
6. **Review economics confirmed at real scale.** ~153,700 structured claims admit for 4 human
   mapping approvals; paper-text review is ~36 contested claims/paper (v1 pilot rate), tamed by
   agreement-v2 + triage + (metal, electrolyte, current-density) blocking.
7. **Reading queue closed; one vector change justified.** ir_correction boolean -> stated
   fraction (B2's RuO2 437->382 mV). Rules CR-A..CR-E and CR5 page-sourced.

## 3. GATE 1 decision packet (Anu only)
Everything R0 was meant to feed, in one place. Detail in the named files.
- **Pick the fork clusters to pursue** (FORK_CENSUS.md): recommended entry = the Ir/0.5 M
  H2SO4/10 mA literature cluster (~597 OA) as the 3-paper pilot, PLUS the A1 x A2 Co-Mn
  structured block in parallel. Decide whether to widen the harvest beyond Pd/Ru/Ir to activate
  A1 x B1 on non-noble oxides.
- **Approve each dataset column-mapping** (one per dataset, S2): A1 MPS, A2 Lila, A3 McCrory
  (after SI fetch), A4 (after id). R0 gives the A1 field->key mapping in MPS_SURVEY.md section 4.
- **Approve the harvest list** (HARVEST_PREREG.md queries, census in harvest/).
- **FREEZE the conditions vector** (locked plan item 3): accept/modify D-1 (ir_correction ->
  fraction); keep the other nine keys. CONDITIONS_DELTA.md.
- **Approve each sourced comparability rule** (locked plan item 4): CR-A electrolyte, CR-B
  current density, CR-C iR fraction, CR-D temperature, CR-E loading, and **decide CR5
  protocol_tier** (five tiers, default-deny on mismatch/unstated). RULES_PROPOSALS.md.
- **Decide the floor policy** (locked plan item 9 / S3): adopt floor = max(stated, 13 mV, MPS
  empirical block floor ~22-51 mV). MPS_SURVEY.md section 3.
- **Sign the three supersessions** (strategy section 8): S1 corpus=field, S2 tiered gate, S3
  empirical floor.

## 4. Deferred to Anu (FOR_ANU.md) - none of these blocked R0
McCrory SI (A3); identify A4's DOI; refs 4/15/16 if their text is wanted; run the ChemRxiv
census in a browser.

## 5. Open questions (OPEN_QUESTIONS.md)
OQ-R0-1 B2 is 2026 not 2025 (same paper). OQ-R0-2 ESAMP 143/25 mV figure not in the OA
descriptor (floor computed from data instead). OQ-R0-3 A4 unidentified. OQ-R0-4 MPS has no
Ru/Ir. OQ-R0-5 McCrory SI deferred. OQ-R0-6 ChemRxiv blocked. OQ-R0-7 MPS scale differs from
the paper headline. OQ-R0-8 MPS current-density needs area->mA/cm2 mapping at R1.

## 6. Reproducibility and hygiene
- MPS: `tar xzOf downloads/public_release_20230228.tar.gz | psql -d mps`; survey via
  sql/mps_survey.sql; no write touched schema public_release; the archive is unchanged.
- Census: `python3 harvest_census.py` (raw responses cached under harvest/raw/).
- Nothing was pushed; the consilience-ledger (v1 lab-extension) repo was not modified; no
  pipeline code was written. R0 stops here for Gate 1.

## 7. Bottom line
The universe the strategy bet on is largely real and now receipted: a field-scale OA
literature pool, a first-party structured dataset with a measured reproducibility floor, and -
unplanned - a second structured dataset (Lila) that forks against the first with no extraction.
The one true gap is that MPS carries no Pd/Ru/Ir, so the noble-metal fork work lives in the
literature and McCrory sources, not in MPS. Everything needed to decide Gate 1 is in r0/.
