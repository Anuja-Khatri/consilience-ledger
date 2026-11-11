# Comparability rule sources

Candidate comparability parameters and tolerances with citations, feeding the
`comparability_rules.yaml` draft. Rules are default-deny: a pair is comparable only if
every rule's field is stated on both claims and the predicate passes (IV.2).

The empirical basis for a conditions veto in acidic OER is ESAMP (Statt, Rohr, Brown,
Guevarra, Hummelshoj, Hung, Anapolsky, Gregoire, Suram; Digital Discovery 2023, 2, 1078):
overpotential prediction error drops from 143 mV to 25 mV when condition parameters enter.
Its state-equivalency rules are the published ancestor of this veto.

## Rule basis (v0.1 - page-level citations ported from ../ledger-v2 r0/GATE1.md, Gate-1 approved)
Citations are matched BY FIELD. Note CR3/CR4 are numbered differently in ledger-v2 (there CR3=iR,
CR4=temperature); this repo keeps its own numbering and predicates. Source "B2" = PMC13707403
(Molecules 2026), the OER-benchmarking comparability review cited throughout GATE1.

| Rule | Field | Predicate | Basis | Page-level citation (ported) |
|---|---|---|---|---|
| CR1 | electrolyte | identity + concentration equal | Electrolyte identity and concentration set the reaction environment. | B2 (PMC13707403, Molecules 2026), **abstract**: comparability asserted only "on a matched basis (1 M KOH, room temperature)". |
| CR2 | current_density | equal within 0, same normalisation | Overpotential is reported at a current density; geometric vs ECSA are not interchangeable (CC-06). | B2, **section 3.2 "The 10 mA cm-2 Benchmark"**: divergence "by more than 150 mV at 100 mA cm-2" relative to 10 mA cm-2. |
| CR3 | temperature | equal (room_temperature enum, CC-12) | Temperature shifts kinetics; room_temperature is an enum, never a number (D10). | B2, **abstract**: the matched basis is explicitly "(1 M KOH, room temperature)" (ledger-v2 numbers this CR4). |
| CR4 | ir_correction | both corrected or both not | iR correction changes the reported overpotential materially. | B2, **section 3**: a RuO2 electrode's overpotential at 25 mA cm-2 "slid continuously from 437 mV uncompensated down to 382 mV at full compensation" (ledger-v2 numbers this CR3; this repo keeps its enum_equal predicate). |

ESAMP (Statt et al., Digital Discovery 2023, 2, 1078) remains the empirical ancestor of the veto
(overpotential error 143 mV -> 25 mV when conditions enter); the per-rule page-level citations above
are the Gate-1-approved sources ported from ledger-v2.

## Accessible sources used so far
- Their paper (arXiv:2609.30133), downloaded and ingested; reports overpotentials at
  stated current densities in acid with iR-correction status, and stability metrics.
- ref 40 Peng 2023 (National Science Review, OA), downloaded and ingested.

## comparability-v0 locked (Checkpoint 1, Anu-confirmed)
- CR1-CR4 confirmed as comparability-v0.
- CR1 uses a canonical electrolyte identity list (H2SO4 = sulfuric_acid; HClO4 =
  perchloric_acid), so identity equality is never a string accident.
- CR2/CR3 units canonicalise through pint after spelling normalisation
  (labext/units.UNIT_ALIASES): "C" -> degC (pint reads bare C as coulomb), mA/cm^2 and
  A/cm^2 variants, umol/cm^2, mg/cm^2, mol/L. These are locked in rules.lock via the
  rules file `canonical` block.

## CR5 (protocol_tier) - v1 CANDIDATE, NOT added in v0
A CR5 that makes a screening tier and a long-term tier never comparable matches Lila's
own "comparative, not absolute" framing. It is NOT added in v0: the stated rate for
protocol_tier is 0.00, so adding CR5 now would make every pair `condition_unstated` and
the ledger 100% veto. Logged here as a sourced candidate for comparability-v1, to be
added once protocol tier is reliably extracted. Source basis: Lila's screening data is
explicitly comparative (arXiv:2609.30133 SI); ESAMP state-equivalency.

## Pending downloads for Phase 3 sourcing (III.4.4)
- ESAMP ESI (RSC, open access) for the state-equivalency parameter list and tolerances.
- refs 4 (Wei 2023 ACS Catal), 27 (Hochfilzer 2023 ACS Energy Lett), 15, 16: attempt OA;
  mark excluded_inaccessible if paywalled (D16). These would FURTHER refine the rule basis;
  the per-rule page-level citations above are already ported (v0.1, from ledger-v2 r0/GATE1.md),
  so the rules are no longer PROVISIONAL on their source.
