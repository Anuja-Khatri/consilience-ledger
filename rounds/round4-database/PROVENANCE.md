# PROVENANCE (round 4 database)

All sources are from operator-v4 at git HEAD 5a1028e
(5a1028e39350981fa48d8c28e133614419256017). The sha256 is of the source file. JSON receipts
are copied verbatim except NUMBERS_LOCK.json, where the two superseded median-floor fork-count
digits were redacted to word-only per consolidation rule 2 (no other bytes changed). METHODS.md
and CORRECTIONS.md are rewritten for this folder from the sources named below, em dashes purged.

| destination | source (operator-v4 @ 5a1028e) | sha256 (source) | modification |
|---|---|---|---|
| lab-extension/rounds/round4-database/NUMBERS_LOCK.json | NUMBERS_LOCK.json | 4d95bd34fd37728cc9490d6f981cfc8751b85507410ef2021a2dc90288b6151f | banned median-floor fork digits redacted per rule 2 |
| lab-extension/rounds/round4-database/compliance_rerun.json | out/compliance_rerun.json | 671b2df2f6ca906a4321fc061e7bbf9bb92249ad13ec79ab3db9cae43b54e980 | none (verbatim) |
| lab-extension/rounds/round4-database/redteam_report.json | out/redteam_report.json | b5c3644605742aa5f045e6425141151cc68bff7fce52562156ba2b6176354108 | none (verbatim) |
| lab-extension/rounds/round4-database/METHODS.md | METHODS.md | 4d3ff46459b0d60440dedcda95cc7861a4aea6bd4500c71f0f874cf6c480bf4f | relevant sections extracted (round-robin and cross-field excluded); em dashes purged |
| lab-extension/rounds/round4-database/CORRECTIONS.md | CORRECTIONS.md | 965af529e8ced123db660eb4e9494325e493018caf53f44c93d6e518267e37ac | C-001 to C-003 and superseded section reworded per rule 2; em dashes purged |
| lab-extension/rounds/round4-database/REPORT.md | (written for this consolidation) | n/a | new document; numbers sourced from the receipts above |
