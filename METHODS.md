# METHODS

## Determinism scope (D4)
Extraction (Phase 2+) uses language models and is not deterministic. It is gated by
dual-model agreement plus a human review queue. From approved claim cards onward the
pipeline is byte-deterministic: `ledger.hash` is a sha256 over canonical-JSON of the
approved cards plus `rules.lock` plus the code version. `make reproduce` regenerates
and must match byte for byte (spec IV.5). We never claim end-to-end determinism.

## Judge (Phase 1)
The structural judge is vendored unchanged from theconsilience-engine @ 71f60a2:
typed VF2 subgraph isomorphism (one mismatched typed edge vetoes), per-instance
lexical ablation (the equivocation test), and the four-rung ladder with explicit
ceilings. The one addition is `conditions_compatible`, a node-level comparability
gate for quantitative claims (see Comparability).

## Comparability veto (IV.2)
Two quantitative claims are compared only after their measurement conditions are
proven comparable. The rule set is default-deny: a pair is comparable only if every
rule's field is stated on both claims and the predicate passes. Any unstated required
field yields `condition_unstated`; any failed predicate yields `condition_mismatch`;
a quantity-axis mismatch yields `axis_mismatch`. The rules are hash-locked
(`rules/rules.lock`); every record carries `rules_version` and `map_version`. The v0
rule set is provisional; the sourced, page-cited set is drafted in Phase 3.

## Units
Conditions and quantities are canonicalized with pint, fail-closed (vendored from
lab-gate @ 3e0185a). An unparseable or dimensionally wrong quantity raises and the
pair fails closed. Unstated conditions are never inferred (D10): no pH from
electrolyte, no temperature from an absent "room temperature".

## Verdict floor (D7) and writeback (Phase 5)
A numeric verdict against Lila's data requires the difference to exceed
max(their stated floor 13 mV, the claim's own stated uncertainty). Below that the
outcome is `within_floor`, not confirmed or contradicted.

Writeback compares each approved overpotential performance claim against Lila's own
instrument data (`oer_exp_data.csv`, `overpotential_cp1_600s_mean`). The data is CC-BY
but is loaded at runtime from a user-provided path (env `LILA_OER_DATA`, else the
upstream checkout) and is never committed (CC-28); verdicts cite the data by sha256 and
by row index, plus the manuscript commit. The comparison point is the best measured
overpotential for the claim's catalyst element system (the optimised composition), with
the spread (mean, n rows) reported; no statistics are recomputed beyond this (CC-19). A
claim whose catalyst system has no Lila measurement (for example the published pure-Pd
claims), or an explicitly long-term claim against the screening-tier data, is a published
veto (`not_comparable`), not a verdict (CC-21). Result over the 34 approved claims: 1
within_floor (their InMnPdOx claim reproduced by their own data to 0.1 mV), 2
contradicted (just over the floor), 6 not_comparable (including every published pure-Pd
claim).

## Extraction models (D3)
Two independent extraction runs. Selection by the keys present in the environment:
- If `OPENAI_API_KEY` is also set: `claude-sonnet-4-6` (Anthropic) + `gpt-4.1` (OpenAI),
  one Anthropic and one non-Anthropic family (preferred).
- Else: `claude-sonnet-4-6` + `claude-haiku-4-5-20251001`, two different Anthropic
  versions (the D3 fallback).
All outputs are cached to disk (jsonl per paper per model) and are resumable. Keys come
from environment variables only (D14); no `.env` is read (Anu ruling). As of the Phase 2
commit no key was present, so extraction has not run; the exact model strings above are
what the harness will use, and the actual run is recorded here when it happens (OQ-2,
PILOT_REPORT.md).

## Agreement gate
AGREED-PROVISIONAL = both models produce the identical card, field-exact after
canonicalisation (text casefolded, quantities reduced to pint base units, per-run ids
excluded). Everything else goes to the review queue as one markdown file per contested
claim. Unparseable cards are parked (CC-11); partial agreement is parked, never averaged
(CC-15).
