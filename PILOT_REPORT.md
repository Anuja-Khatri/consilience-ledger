# PILOT_REPORT

Real dual-model extraction, run 2026-11-10. Models: `claude-sonnet-5` and `gpt-4.1`
(one Anthropic + one non-Anthropic family, D3 preferred). All outputs cached to disk
(jsonl per paper per model), resumable. No key value was ever printed, logged, or
committed.

## Decision: NO-GO (twice) -> minimal corpus. The rule was never softened (D6).

- Attempt 1 (pilot = refs 39, 40, 42; accessible: their paper 2609.30133 + ref 40 Peng;
  refs 39 and 42 are paywalled and excluded; ref 42 substituted by their own paper):
  **NO-GO**. 70 approvable numeric claims, but ~0 state all three of electrolyte
  identity, current density, and iR-correction, so fewer than half are fully
  conditioned.
- Shrink to the Pd neighborhood (their paper + refs 39, 40, 11, 12): refs 11 (Wan 2024,
  Nat Catal) and 12 (Cherevko 2023, Curr Opin) are review papers and paywalled; their
  primary numeric claims are few (reviews restate others' numbers, excluded by D8). The
  accessible shrunk set equals the current set, so the re-pilot is identical.
- Attempt 2: **NO-GO**. Corpus set to their paper + refs 39, 40 only (accessible slice:
  their paper + ref 40). Limitation recorded below.

## Yield and per-field stated-rate table (70 approvable numeric claims)
| field | stated rate |
|---|---|
| electrolyte identity | 0.53 |
| current_density | 0.63 |
| prior_operation_duration | 0.26 |
| temperature | 0.06 |
| anneal_temperature | 0.06 |
| loading | 0.03 |
| iR_correction | 0.03 |
| pH | 0.00 |
| protocol_tier | 0.00 |

Per paper: their paper 25 approvable (sonnet 6, gpt 20; 29 parked); ref 40 Peng 45
approvable (sonnet 26, gpt 25; 20 parked). Auto-agreed (field-exact on both models): 0;
every claim therefore goes to the review queue for Anu (72 contested files). This is
expected for full-card field-exact agreement across two model families; agreement is
the auto-accept signal, not a requirement for a claim to be approvable.

## The finding behind the NO-GO (why this is a result, not a failure)
iR-correction is explicitly stated in only 3% of result sentences. In the OER
literature it is stated once in the Methods, not in each result sentence, so
per-sentence extraction rarely carries it. This is exactly the heterogeneous,
under-stated-conditions problem the conditions veto addresses (CC-21): most literature
pairs will veto on `condition_unstated` rather than being called disagreements. The
NO-GO and the minimal corpus are the honest, spec-compliant outcome of the D6 ladder.

A legitimate future extraction improvement is to attribute a paper-globally-stated
condition (for example "all overpotentials are iR-corrected") to each claim that leaves
it unstated. That was NOT done here: it was out of scope for v1 and would risk the
exact unstated-condition inference the project forbids (D10). It is recorded in
ROADMAP/LIMITATIONS, not used to move the pilot to GO.
