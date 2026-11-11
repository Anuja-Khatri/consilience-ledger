# R0 PROVENANCE and license receipts

Per strategy section 5: every source gets its license quoted and hashed here before a
byte is used. Retrieved 2026-11-10 by Claude, research only (phase R0), through each
source's official route. SHA-256 is over the exact bytes retrieved and stored under
`r0/`. No raw 1.1 TB Caltech data was ever requested; only the released metadata dump.

## A1 - Materials Provenance Store (MPS)
- Source: CaltechDATA record `hjfx4-a8r81`, DOI 10.22002/hjfx4-a8r81.
- Official route: InvenioRDM REST API `GET /api/records/hjfx4-a8r81` then the file
  content endpoint `/files/public_release_20230228.tar.gz/content` (302 -> OSN S3 store,
  followed with `curl -L`).
- License (quoted from record `metadata.rights`): **"Creative Commons Attribution 4.0
  International"** (CC-BY-4.0).
- Creators (record): Statt, Michael; Rohr, Brian; **Guevarra, Dan**; Suram, Santosh;
  Morrell, Thomas; Gregoire, John. (Guevarra co-author confirms the Lila lineage claim.)
- File: `public_release_20230228.tar.gz`, declared size 4,521,364,439 bytes; downloaded
  size matched exactly. Contains one member: `public_release_20230228.sql` (plain
  PostgreSQL dump, server version 14.6, schema `public_release`, ~3.43 GB uncompressed).
- SHA-256 (archive): `b988d2c428fbe2d29fed1a4aa195aedf4b950972c0b0d3429146550b3abcce9e`
- SHA-256 (record metadata JSON): `1818a873fa683cd0f896915da8be21b21dd24cd9c92413f9c1058d20c8e668da`
- Stored: `r0/downloads/public_release_20230228.tar.gz`, `r0/downloads/mps_record.json`.

## A2 - lila_oer_manuscript
- Already cloned at `upstream/lila_oer_manuscript` (STATE.md: @92a7737).
- License (quoted): code **"MIT License ... Copyright (c) 2026 Lila Sciences"**; data
  **"The data files under `data/` are released under the Creative Commons Attribution"**
  (CC-BY-4.0, per README). Data not committed into any build repo (Anu ruling OQ-3).

## A3 - McCrory JCAP benchmarking set
- Not retrieved in R0. The data tables live in the paper's ACS Supporting Information,
  described as free of charge, but the ACS SI route was not exercised here. Logged on
  FOR_ANU.md for Anu to pull the SI directly, with the exact citation. No value used yet.

## A4 - Curated 437-point OER literature set
- NOT uniquely identified from the strategy description alone. Europe PMC keyword search
  did not pin a single record with 437 points at 1 mA/cm2-geo with pH + composition.
  Logged as OPEN_QUESTION OQ-R0-3 and on FOR_ANU.md; no value used.

## B2 - "What the Overpotential Does Not Tell You..."
- Source: Europe PMC, PMCID **PMC13707403**, DOI 10.3390/molecules31203696.
- Journal/year: *Molecules* (MDPI), **2026** (strategy said 2025 - discrepancy logged OQ-R0-1).
- Official route: Europe PMC REST `/{PMCID}/fullTextXML`.
- License (Europe PMC `license` field): **cc by**. isOpenAccess = Y.
- SHA-256 (full text XML): `3ab71f905ff60aaab05c7de8341d1dedd3408bc8853f47932cfd58151314c104`
- Stored: `r0/papers/PMC13707403_fulltext.xml`, `r0/papers/b2_meta.json`.

## B3 - "Reporting activities for the oxygen evolution reaction"
- Source: Europe PMC, PMCID **PMC10576816**, DOI 10.1038/s42004-023-01024-y.
- Journal/year: *Communications Chemistry* (Nature), **2023**.
- License (Europe PMC): **cc by**. isOpenAccess = Y.
- SHA-256 (full text XML): `6a767b8809f44eaea275b2d542b914cb7698ab00acf32c6bd1a16817140c88d1`
- Stored: `r0/papers/PMC10576816_fulltext.xml`, `r0/papers/b3_meta.json`.

## Reading-queue - ESAMP / MPS descriptor paper
- Source: Europe PMC, PMCID **PMC10079965**, "The Materials Provenance Store", *Sci Data*
  2023. License **cc by**. isOpenAccess = Y.
- SHA-256 (full text XML): `77f8435bed59b8f34664bef45b98231e0cf752e5042be81a9e3cce6b6ea3713b`
- Note: the "143-to-25 mV" replicate figure cited in the strategy was NOT located in this
  Sci Data descriptor (OQ-R0-2). The empirical replicate floor is computed directly from
  the A1 data instead (see MPS_SURVEY.md), which is the stronger, data-derived route.

## Reading-queue - ref 27 (Hochfilzer, Chorkendorff, Kibsgaard)
- "Catalyst Stability Considerations for Electrochemical Energy Conversion", ACS Energy
  Lett 2023. Europe PMC PMCID **PMC10012258**. License **cc by-nc-nd**. isOpenAccess = Y.
  (BY-NC-ND: readable for research; no redistribution/derivatives of the text.)
- SHA-256 (full text XML): `39befbf76d5be144aec7fb00980f28c746285dd2398435eb5e6d460d74a4a064`
- Stored: `r0/papers/PMC10012258_fulltext.xml`, `r0/papers/PMC10012258_meta.json`.

## Reading-queue - refs 4, 15, 16 (excluded_inaccessible)
- ref 4: Wei et al., "Benchmarking Electrocatalyst Stability for Acidic OER: The Crucial
  Role of Dissolved Ion Concentration", ACS Catal. 13, 14058-14069 (2023).
- ref 15: Przybysz, Jenewein, Cherevko, "High-Throughput Electrochemistry Using Scanning
  Electrochemical Cells", ACS Electrochem. 2, 801-824 (2026).
- ref 16: Jenewein, Akkoc, Kormanyos, Cherevko, "Automated high-throughput activity and
  stability screening of electrocatalysts", Chem Catalysis 2, 2778-2794 (2022).
- All three: no OA full text in Europe PMC (publisher paywall). Marked
  **excluded_inaccessible**; listed on FOR_ANU.md. No value used.

## Harvest census (B1)
- Europe PMC REST search API + arXiv export API, preregistered queries (HARVEST_PREREG.md).
- Raw API responses cached under `r0/harvest/raw/`. census SHA-256:
  `321b8b94528adddccda5dd1338edd369d20f7fc4d9ab12161eb7b7649dbe863e`
- ChemRxiv API: BLOCKED by a Cloudflare JS bot-challenge (HTTP 403 to curl and WebFetch).
  Not worked around; exact query on FOR_ANU.md.
