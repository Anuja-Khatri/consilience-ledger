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

## Verdict floor (D7)
A numeric verdict against Lila's data requires the difference to exceed
max(their stated floor 13 mV, the claim's own stated uncertainty). Below that the
outcome is `within_floor`, not confirmed or contradicted. (Wired in Phase 5.)

## Extraction models
Recorded here in Phase 2 (exact model strings). Not yet run: no API key was present
in the build environment (OPEN_QUESTIONS OQ-2); the non-API parts proceed first.
