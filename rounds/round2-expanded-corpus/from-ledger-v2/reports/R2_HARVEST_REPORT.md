# R2-at-scale (K=40) harvest + extraction - report. Stops at the review queue (Gate 3 is Anu's).

Dual independent model families (claude-sonnet-5, gpt-4.1) extracted overpotential-at-current-
density claims from a 40-paper OA corpus on the two approved clusters, under agreement-v2 with
Gate-2 amendments A1-A3. Research only; keys sourced from the environment, never echoed; model
calls cached (`r2_out_k40/model_cache.jsonl`, deterministic on rerun). Outputs in
`ledger-v2/r2_out_k40/`.

## Harvest (tools/harvest.py; manifest in r2_corpus/k40/)
- **40 papers: 20 Pd-HClO4 + 20 Co-H2SO4**, OA with retrievable Europe PMC full text, reviews
  excluded, deterministic PMCID-sorted selection. Licenses: 30 CC BY, 6 CC BY-NC, 3 CC BY-NC-ND,
  1 unspecified (facts/short Methods quotes only; full text not redistributed).
- **Honest shortfall (no silent padding):** only **2 of the 18** lexical "1 M HClO4" Pd hits had
  retrievable EPMC full-text XML (the rest are abstract-only in EPMC or review-typed). The
  Pd-HClO4 quota of 20 was filled from the 0.1 M / broad-HClO4 priority. The 18-count was a
  lexical hitCount, not 18 full-text papers; this is the gap between "records" and "retrievable
  full text" the R0 census flagged.

## Extraction (agreement-v2 + amendments A1-A3)
| | value |
|---|---|
| agreed-provisional (auto-accepted) | **12** |
| contested (-> Anu) | **51** (Pd-HClO4 28, Co-H2SO4 23) |
| agreement rate | 0.19 |
| iR-fraction stated rate | **0.286** |
| model parse errors (parked, not dropped) | 2 (anthropic unparseable JSON on PMC11935124, PMC10161032) |
- Amendments validated against Anu's pilot hand-decisions now run automatically: material-name
  canonicalization (A1) paired baseline-string variants; durations at a different current were
  kept off the activity card (A2); non-measurement electrolyte sentences were nulled (A3);
  commercial baselines (RuO2, IrO2, Ir/IrOx, Pt) were extracted as intended.
- Review queue: `r2_out_k40/review_queue/` (one md per contested claim, both model outputs,
  field diff, approve/reject/correct boxes) with a triage-ready `INDEX.md` batched by cluster.

## Fork-candidate preview (FORK_PREVIEW.md) - from auto-accepts only
Blocked the 12 agreed-provisional cards + the 6 Gate-2-approved pilot cards (18 total) and judged
every cross-paper pair inside a block with CR1-CR5 + the S3 floor.
- 3 blocks (hclo4/unstated 8, h2so4/unstated 9, unstated/unstated 1); 38 cross-paper pairs.
- **0 fork candidates, 0 within-floor, 38 vetoed.** Every veto is on the SAME three fields:
  `condition_unstated: ir_correction` x38, `: temperature` x38, `: protocol_tier` x38.

## The finding, now measured on two independent corpora
The literature auto-accepts do NOT fork - not because the numbers agree, but because the papers
leave iR compensation, temperature, and protocol tier unstated, so comparability is vetoed before
a disagreement can be read. This is the SAME cause that produced the MPS structured veto census
(reports/structured_fork_census.md). The "overpotential does not tell you" thesis holds across
both a flagship structured dataset AND a 40-paper literature sample: eta at 10 mA/cm2 is rarely
comparable across sources, and the defect is named every time. iR fraction is stated in only 28.6%
of extracted literature claims (0% in MPS).

## Where round-one forks will come from
Not from the strict auto-accept set. The 51 contested claims are where condition-complete pairs
emerge: during review Anu confirms/fills the conditions a model left contested, and two claims
that then share electrolyte + current density + iR fraction + temperature + tier can fork. The
fork preview is deliberately built only from auto-accepts (the defensible floor); the real fork
census runs after Gate 3 over the approved set.

## Review-load projection (for Gate 3)
51 contested over 40 papers = ~1.3 contested/paper on the single overpotential axis (vs the v1
all-numeric 36/paper), triaged by cluster. A second agreement pass relaxing the
material-string tie (already partly addressed by A1) would raise auto-accept further. Scaling the
clusters is linear and batchable.

## Honest limits
- Lexical harvest: the corpus is what the preregistered queries returned; some tangential/near-
  review papers slipped the filter. The extractor's "overpotential + measurement-electrolyte"
  requirement discards most of their noise, but Anu should spot-check cluster fit at review.
- 2 papers lost one model's output to unparseable JSON; those papers ran single-family (their
  claims are all contested by construction - never auto-accepted on one family).
- The fork preview excludes contested claims by design; 0 forks here is a floor, not the final
  fork count.

## Stop point
Gate 3 (Anu): adjudicate the 51 contested claims, accept the 12 agreed cards, then the fork
census + loop run over the approved set. Nothing enters the ledger without that.
