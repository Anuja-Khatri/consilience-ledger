# PROVENANCE

Retrieval date for all web sources: **2026-11-11**. Research-only feasibility check.
Every file below was retrieved through an official open route (institutional
open-access repository, DOE OSTI, or publisher open-access page). No paywall,
login, or bot block was worked around. Where a publisher site returned a 403
bot block or paywall, the item was NOT fetched by another path and is listed in
`FOR_ANU.md` instead.

## Retrieved source files (saved under feasibility/sources/)

### Tesch et al. 2023 - round-robin OER (Check 2)
- Citation: M. F. Tesch, S. Neugebauer, P. V. Narangoda, R. Schlögl, A. K.
  Mechler, "The rotating disc electrode: measurement protocols and
  reproducibility in the evaluation of catalysts for the oxygen evolution
  reaction," *Energy Advances*, 2023, **2**, 1823–1830.
- DOI: 10.1039/d3ya00340j
- Retrieved via: Max Planck Society open repository (pure.mpg.de), the
  authors' institutional open-access copy. RSC publisher page
  (pubs.rsc.org/ya/article/2/11/1823-1830/836090) returned HTTP 403 (bot
  block) and was not used.
- URL: https://pure.mpg.de/rest/items/item_3564330_2/component/file_3564833/content?download=true
- Licence as stated on the file: "This article is licensed under a Creative
  Commons Attribution 3.0 Unported Licence." / "© 2023 The Author(s).
  Published by the Royal Society of Chemistry." (Open Access Article.)
- File: feasibility/sources/tesch_2023_energy_advances.pdf
- sha256: 64b8dc389a0eb5e6417e631d2cec78ae17f591da28239e315b8763b8a93a5e9d

### McCrory et al. 2013 - OER benchmarking, Supporting Information (Check 3)
- Citation: C. C. L. McCrory, S. Jung, J. C. Peters, T. F. Jaramillo,
  "Benchmarking Heterogeneous Electrocatalysts for the Oxygen Evolution
  Reaction," *J. Am. Chem. Soc.*, 2013, **135**, 16977–16987.
- DOI: 10.1021/ja407115p
- Retrieved via: CaltechAUTHORS institutional repository (open SI download via
  its own AWS S3 signed link). ACS publisher SI URL returned HTTP 403; the
  Caltech open route was used instead. Main-text PDF is NOT open (rights
  "Other" on the Caltech record); only the Supporting Information is free.
- URL: https://authors.library.caltech.edu/records/smd5n-0aa45 (file ja407115p_si_001.pdf)
- Licence/rights as stated: Caltech record marks the deposit "Other" -
  "No commercial reproduction, distribution, display or performance rights in
  this work are provided." The SI itself is provided free for download.
- File: feasibility/sources/mccrory_2013_si.pdf
- sha256: 1002b96bd2948a22d12ea86f9b5ed4df22dd14d59d2a067995f32b283fb02efa

### McCrory et al. 2015 - OER/HER benchmarking, Supporting Information (Check 3)
- Citation: C. C. L. McCrory, S. Jung, I. M. Ferrer, S. M. Chatman, J. C.
  Peters, T. F. Jaramillo, "Benchmarking Hydrogen Evolving Reaction and Oxygen
  Evolving Reaction Electrocatalysts for Solar Water Splitting Devices,"
  *J. Am. Chem. Soc.*, 2015, **137**, 4347–4357.
- DOI: 10.1021/ja510442p
- Retrieved via: CaltechAUTHORS institutional repository (open SI download).
  ACS publisher SI URL returned HTTP 403; the Caltech open route was used.
  Main-text PDF is NOT open (rights "Other"); only the SI is free.
- URL: https://authors.library.caltech.edu/records/9hdcw-5f261 (file ja510442p_si_001.pdf)
- Licence/rights as stated: "No commercial reproduction, distribution, display
  or performance rights in this work are provided." (record "Other"); SI free.
- File: feasibility/sources/mccrory_2015_si.pdf
- sha256: 4e5763feef7e6fd469437aeda0ecf96357452cf2021be30cc68d34bb65bd570f

## Local inputs read (not retrieved; hashed for the record)

- Lila screening data: upstream/lila_oer_manuscript/data/oer_exp_data.csv
  - sha256: ab33c747883b5dce98cc26bd2dee16dd9a12a9703fe3f18450d1490fe3f91d00
  - Licence: the manuscript repo ships its own LICENSE (data/LICENSE). Lila's.
- Lila paper text: corpus_in/text/2609.30133.txt
  - sha256: aaaafb196e6d7d651db5a8c49d38168827291a352283d0705b518dac2e98cda5
- MPS (Caltech) database: local PostgreSQL db `mps` (CaltechDATA hjfx4-a8r81,
  CC-BY-4.0). Read-only SELECT only. Queries saved in feasibility/sql/.
- Simulator dataset: vendor/helao_oersim/oer13_cps.pzstd
  - sha256: b9e23249ec4367e1a729223a584f74cd08bb98a4f738cbe6fb091c345044cbf0
  - Licence: MIT (vendor/helao_oersim/LICENSE.md). Belongs to helao-async
    (Guevarra, Richter, Kan, Lai, Zhou, Stein, Donnelly, Gregoire, Suram).
    NOT Lila's dataset.
- Approved claim cards: lab-extension/ledger/claims.json
  - sha256: 731b730e0b1728222aaa439cdc67e1e0d36aad7d8f662c65f4c9120dd01d97c2
  - plus ledger-v2/r2_out/approved/*.json and ledger-v2/r2_out_k40/approved/*.json

## PART A additions - DOI resolution (retrieved 2026-11-11)

### CaltechDATA plate records (34), via DataCite API
- Source: DataCite REST API, `https://api.datacite.org/dois/<doi>` - the official
  DOI-metadata route for the CaltechDATA records (landing pages at
  `https://data.caltech.edu/records/...`). Retrieved for all 34 matched plate
  DOIs listed in `feasibility/A1_matched_plates.csv`.
- Raw records saved: `feasibility/caltechdata/*.json` (34 files).
- Licence as stated in each record: `cc-by-sa-4.0`
  (http://creativecommons.org/licenses/by-sa/4.0/).
- Summary CSV: `feasibility/A2_caltechdata_summary.csv`
  - sha256: 1f4ad8fc77a088eedc1de2005f0594f3f634ba88d66905ad80770892d0283141
- A1 plate table: `feasibility/A1_matched_plates.csv`
  - sha256: e03d8b00e49d24152508b794ab9d1acf879cf567e9a8b04cd35d84947382aaac
- Combined sha256 over the 34 sorted per-file hashes (stable manifest):
  06ce81eac9de2d0cc23e2731453bb91364e0f668971b5b0a228010e6c329045b
- Every record declares `IsPartOf 10.25989/es8t-kswe` and
  `IsDocumentedBy 10.1038/s41524-019-0216-x`.

### Soedarmadji et al. 2019 - the documenting publication (strong linkage target)
- Citation: E. Soedarmadji, H. S. Stein, S. K. Suram, D. Guevarra, J. M.
  Gregoire, "Tracking materials science data lineage to manage millions of
  materials experiments and analyses," *npj Computational Materials*, 2019,
  **5**, 79. DOI: 10.1038/s41524-019-0216-x.
- Retrieved via: Nature open-access page (npj journals are gold OA, CC BY 4.0).
  The HTML redirects through a cookie-consent step (idp.nature.com); the
  open-access PDF was fetched with a standard cookie jar - a consent banner, not
  a login or paywall. Not in PMC (NCBI id-converter: "not found in PMC"); Europe
  PMC returned no record.
- URL: https://www.nature.com/articles/s41524-019-0216-x
- Licence as stated on the file (verbatim): "Open Access This article is licensed
  under a Creative Commons Attribution 4.0 International License…" "© The
  Author(s) 2019".
- File: feasibility/sources/soedarmadji_2019_npj_mead_lineage.pdf
- sha256: 0612926eeef4e6ed6d11aafde9b961988a0c4aa4e4e0f347e6229b7c7f3d4129
