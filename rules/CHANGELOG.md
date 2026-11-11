# Comparability rules changelog

## comparability-v0.1 (2026-11-11) - DOCUMENTATION ONLY (no verdict change)
Ported the page-level citations approved at Gate 1 in ../ledger-v2 (r0/GATE1.md) into the
`source:` field of each rule and into rules/SOURCES.md, matched BY FIELD:
- CR1 electrolyte          <- B2 (PMC13707403, Molecules 2026), abstract ("matched basis (1 M KOH, room temperature)").
- CR2 current_density      <- B2, section 3.2 "The 10 mA cm-2 Benchmark" ("> 150 mV at 100 mA cm-2" vs 10).
- CR3 temperature          <- B2, abstract ("(1 M KOH, room temperature)")  [ledger-v2 numbers this CR4].
- CR4 ir_correction        <- B2, section 3 (RuO2 437 -> 382 mV sliding with compensation)  [ledger-v2 numbers this CR3].

Rule numbering, fields, predicates and tolerances are UNCHANGED from comparability-v0. Only the
`source` metadata changed, so every verdict (0 forks, 561 vetoes, 9 verdicts) is byte-identical;
the ledger DECISIONS do not change. Because `source` is inside the hash-locked rules model, the
`rules.lock` sha and the `ledger.hash` were regenerated (re-locked); the version was bumped v0 ->
v0.1 to mark this documentation-only change. See FIXES_REPORT.md / CORRECTIONS.md for the hashes.

## comparability-v0 (Checkpoint 1, Anu-confirmed)
Initial CR1-CR4 structural rules with canonical maps; citations PROVISIONAL (now ported at v0.1).
