# PROVENANCE (feasibility: caltech-lila routes)

All files are ported from operator-v4/feasibility at git HEAD 5a1028e (5a1028e39350981fa48d8c28e133614419256017). The sha256 is of the source file. Markdown, SQL, and Python files had the em dash character (U+2014) replaced with a hyphen where flagged `purged`; CSV tables are byte-identical. No MPS data bytes and no paper full text are included (rule 5): only the SQL that reads the read-only database, the derived receipt tables, and the report markdown. The McCrory Supporting Information carries restrictive rights and is not included; only its derived count appears.

The source directory's own provenance record is preserved verbatim (em dashes purged) as SOURCE_PROVENANCE.md. ROUTE1_SUMMARY.md is written for this consolidation; its numbers are reproduced from the committed route1_receipts tables.

| destination (repo-relative) | source (operator-v4 @ 5a1028e) | sha256 (source) | em-dash purged |
|---|---|---|---|
| feasibility/caltech-lila-routes/FEASIBILITY.md | feasibility/operator-v4/feasibility/FEASIBILITY.md | c934dc29e74fdb9eef5df91c2a1c44ca3f9dbafc526192392a56dfead5f85bba | yes |
| feasibility/caltech-lila-routes/SOURCE_PROVENANCE.md | feasibility/operator-v4/feasibility/PROVENANCE.md | 1e66e096af34064deca732c83636ba2890269e49dcecf9b0260236ecf14300d3 | yes |
| feasibility/caltech-lila-routes/route1_receipts/RECEIPTS.md | feasibility/operator-v4/feasibility/route1_receipts/RECEIPTS.md | 2205b92fa669098a5418e9efa8ee233c5286b87298a99aa473a5505c88ef8d44 | yes |
| feasibility/caltech-lila-routes/route1_receipts/route1_match.py | feasibility/operator-v4/feasibility/route1_receipts/route1_match.py | cac82e8590e7f9efe88bdd151299200d8867bae1bed97d0b8659e28bf4e3ad2b | yes |
| feasibility/caltech-lila-routes/route1_receipts/route1_subset_counts.py | feasibility/operator-v4/feasibility/route1_receipts/route1_subset_counts.py | 5245cbf222f9a1496d16cc6ac964097f21e88ab89e1ae012a0e2e4fdd8f65387 | yes |
| feasibility/caltech-lila-routes/route1_receipts/table_a_technique_current.csv | feasibility/operator-v4/feasibility/route1_receipts/table_a_technique_current.csv | 1bdf1bfbf7a396e1cfc9701895ff591ea25092b5ee35f8718896083970e77994 | no |
| feasibility/caltech-lila-routes/route1_receipts/table_b_acquisition_time.csv | feasibility/operator-v4/feasibility/route1_receipts/table_b_acquisition_time.csv | a23a005412596489a4ebfcfe398b039db541162ca42e793bad148b963d51866c | no |
| feasibility/caltech-lila-routes/route1_receipts/table_c_anneal.csv | feasibility/operator-v4/feasibility/route1_receipts/table_c_anneal.csv | 82375e8a37a598f0499b93a8b0a2bfbf38d3420b0da4d997f36ebe5c8fe8213d | no |
| feasibility/caltech-lila-routes/route1_receipts/table_c_fabrication.csv | feasibility/operator-v4/feasibility/route1_receipts/table_c_fabrication.csv | 7ae5ce01cfd0a248b67377f096572603c0dd8ca648890da1b7978e553307b355 | no |
| feasibility/caltech-lila-routes/route1_receipts/table_c_substrate.csv | feasibility/operator-v4/feasibility/route1_receipts/table_c_substrate.csv | 384451a1de932c0b01018dab62478852c6a60cd41972d3661d6c6094e81848d0 | no |
| feasibility/caltech-lila-routes/route1_receipts/table_d_cp4_100ua.csv | feasibility/operator-v4/feasibility/route1_receipts/table_d_cp4_100ua.csv | 31c394a1815a350dbad5e934138913f6f98728fb6e905b8d794679ac9ec240b5 | no |
| feasibility/caltech-lila-routes/sql/01_electrolyte_ph_technique.sql | feasibility/operator-v4/feasibility/sql/01_electrolyte_ph_technique.sql | 5a25d5a957acdb1175f9dbde3d58a6e028504b1c2e2c87961bcd1dfcb3bca237 | no |
| feasibility/caltech-lila-routes/sql/02_process_detail_params.sql | feasibility/operator-v4/feasibility/sql/02_process_detail_params.sql | 07c0154c15f071da7155681d5a18988b36fc828da24899fba976cdb207d59633 | no |
| feasibility/caltech-lila-routes/sql/03_acid_cp_conditions.sql | feasibility/operator-v4/feasibility/sql/03_acid_cp_conditions.sql | 377a3581d4273b5f2dca8b04169412d06f421445df66a3879e68d8f860b8eb6c | no |
| feasibility/caltech-lila-routes/sql/04_export_h2so4_1M_samples.sql | feasibility/operator-v4/feasibility/sql/04_export_h2so4_1M_samples.sql | e0db9d7a27d404fdb825aa3d1899930a7d5913a8e185ffc4eed05886d1ba9a99 | no |
| feasibility/caltech-lila-routes/sql/05_export_enriched.sql | feasibility/operator-v4/feasibility/sql/05_export_enriched.sql | f016b43bdfbca0f210f55502c4827fe1731c9a81b649065d66df9d9a552d6e63 | no |
| feasibility/caltech-lila-routes/sql/06_matched_campaigns.sql | feasibility/operator-v4/feasibility/sql/06_matched_campaigns.sql | 8f2abed0f1c1f78b5db66afb6ee6bd17e3c1d8d19a22d3e9ba835c268bcbb42d | no |
| feasibility/caltech-lila-routes/sql/07_plate_count.sql | feasibility/operator-v4/feasibility/sql/07_plate_count.sql | 7f0a9a7aa2eaa3447ffce1b38e8c7e2611b13c7497830241bec37f93773ad7ce | no |
| feasibility/caltech-lila-routes/sql/08_matched_anneal.sql | feasibility/operator-v4/feasibility/sql/08_matched_anneal.sql | e6b85c87353d0d3bbf6771dc710886089a12d97ea21ed0926f05bf82babaa00f | no |
| feasibility/caltech-lila-routes/sql/09_matched_sample_plate_doi.sql | feasibility/operator-v4/feasibility/sql/09_matched_sample_plate_doi.sql | cb4d4e7944d409a438540763eacc6db1754f37d95b8cb0358cace26029282b78 | no |
| feasibility/caltech-lila-routes/sql/10_oer13_electrolyte.sql | feasibility/operator-v4/feasibility/sql/10_oer13_electrolyte.sql | 65a432270b7d209b05f544f36e707af2365e4f68a542bdf39d2e23aeb1198dbe | no |
| feasibility/caltech-lila-routes/ROUTE1_SUMMARY.md | (written for this consolidation) | n/a | no |
