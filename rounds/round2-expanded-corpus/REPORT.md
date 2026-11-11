# Round 2: expanded corpus, measured under-reporting, measured floors

This round grows the claim corpus well beyond round 1 and measures, on that larger
corpus, how often the published papers actually state the conditions the comparison
rules require. It also measures an empirical reproducibility floor directly from a
public materials database. Nothing here changes round 1's results or the v1 ledger.

Provenance note (rule 7): the source directories ../ledger-v2 and ../r0 are
unversioned working trees with no commit history. The ported files carry their
file dates, not commit dates. Every ported file is listed with its source path and
sha256 in PROVENANCE.md in this folder.

## Corpus growth
Two open-access harvests were run under the preregistered wording
(`from-ledger-v2/HARVEST_PREREG_K2.md` and the round-2 harvest report):

- A 40-paper harvest: 20 Pd in HClO4 plus 20 Co in H2SO4, open access with
  retrievable Europe PMC full text, reviews excluded, deterministic PMCID-sorted
  selection. The harvest report records an honest shortfall rather than padding:
  only 2 of the 18 lexical "1 M HClO4" Pd hits had retrievable full text, so the
  Pd quota was filled from the broader HClO4 priority. See
  `from-ledger-v2/reports/R2_HARVEST_REPORT.md` and
  `from-ledger-v2/r2_corpus/k40/harvest_manifest.json`.
- A 20-paper harvest targeting papers that state their iR practice (the K2 set),
  to probe the condition gap the first harvest exposed. See
  `from-ledger-v2/HARVEST_PREREG_K2.md` and
  `from-ledger-v2/r2_corpus/k2/harvest_manifest.json`.

## The corpus census
The census of record is over 73 approved cards (receipt:
`from-ledger-v2/reports/K2_CENSUS.md`), with this provenance split: v1 33, pilot 6,
gate3 17, reextract 10, k2 7. The v1 33 are the round-1 cards already in this repo;
the pilot, gate3, reextract, and k2 cards are ported under `from-ledger-v2/cards/`
(the agreed and approved card JSON directories, each card keeping its quoted source
sentence). The reextract directory holds 17 agreed-provisional cards; the census
counts 10 of them as net new in the 73 after provenance dedup against v1 and the
earlier sets.

Census result over the 73 cards and 23 blocks:

- forks: 0
- corroborations within floor: 0
- vetoed pairs: 210

## The measured under-reporting of the field
Every vetoed pair is refused because a required condition is unstated or mismatched
on one side. The per-defect veto table, verbatim from
`from-ledger-v2/reports/K2_CENSUS.md`:

| veto defect | count |
|---|---|
| condition_unstated: temperature | 210 |
| condition_unstated: ir_correction | 188 |
| condition_unstated: protocol_tier | 181 |
| condition_unstated: electrolyte | 65 |
| condition_mismatch: CR2 | 24 |
| condition_mismatch: CR1 | 20 |
| condition_unstated: current_density | 10 |
| condition_mismatch: CR3 | 10 |

This table is the measured under-reporting of the field's papers: it counts how
often the published texts omit or disagree on the conditions needed to compare two
numbers. Temperature is unstated on every one of the 210 vetoed pairs. Each rule
that drives a veto is written down and justified under `from-ledger-v2/rules/` (the
CR comparability rules and their CHANGELOG).

The A4 temperature-recall fix was preregistered in `from-ledger-v2/rules/CHANGELOG.md`
before it ran and operates on the cache only. It raised temperature recall from 6 of
73 to 9 of 73 cards and changed no pair verdict; the census is byte-identical to the
Gate 3 result. Fixing recall recovered only the 3 cards that genuinely stated a
temperature and moved nothing. So the zero forks and the 210 vetoes are a property
of the texts, not an artifact of the extractor. Receipt:
`from-ledger-v2/reports/A4_RECALL_REPORT.md`.

## The measured reproducibility floor
Separately, an empirical reproducibility floor was measured directly on the public
Materials Provenance Store (MPS) acidic-OER data (receipts:
`from-r0/MPS_SURVEY.md` section 3, `from-r0/R0_REPORT.md`, `from-r0/GATE1.md`):

- about 22 mV, strict same-sample repeat (median stddev 22.4 mV, n = 6,249 groups)
- about 51 mV, same-composition block (median stddev 51.1 mV, n = 9,709 blocks)
- p90 above 130 mV in both cases

This is measured on MPS and sits well above Lila's stated reproducibility floor of
13 mV. The floor policy adopted at Gate 1 is the 51 mV same-composition default,
applied as the larger of the stated uncertainty, 13 mV, and 51 mV.

## What this round shows
The comparison instrument is working: when conditions are not stated, it refuses to
compare, and on a 73-card corpus of real OER papers it refuses almost everything,
for a reason it can name on every pair. The refusals are the measurement. The r0
fork census and its projections keep their "projection" labelling
(`from-r0/FORK_CENSUS.md`); no fork is claimed here.
