# Full fork + correspondence census - all approved claims

Over 66 approved cards (by source: {'v1': 33, 'pilot': 6, 'gate3': 17, 'reextract': 10}), deduped by provenance (PMC10035503 vs v1 ref40 collapses here). Blocked by axis + electrolyte identity + protocol tier; every cross-source pair judged with CR1-CR5 + the S3 floor.

- blocks: 22
- **fork candidates: 0** (0 screening-tier provisional)
- **corroborations (agree within floor): 0**
- vetoed (not comparable): 172

## Top veto defects (why pairs are not comparable)
- condition_unstated:temperature: 172
- condition_unstated:protocol_tier: 155
- condition_unstated:ir_correction: 152
- condition_unstated:electrolyte: 53
- condition_mismatch:CR2: 22
- condition_mismatch:CR1: 20
- condition_unstated:current_density: 9
- condition_mismatch:CR3: 8

No forks or corroborations survived the default-deny gate: comparable pairs require electrolyte + current density + iR fraction + temperature + tier all stated on both sides, which the approved claims rarely satisfy. The defect table above names the missing conditions. K2 (iR-practice-stated papers) targets this gap.
