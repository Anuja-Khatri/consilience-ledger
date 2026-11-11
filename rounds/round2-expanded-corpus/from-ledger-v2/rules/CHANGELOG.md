# Comparability rules changelog - v1 -> v2

v1 (frozen, lab-extension/rules/comparability_rules.yaml, locked at CP1-TRIAGE):
- CR1 canonical electrolyte list; CR2 / CR3 pint unit canonicalisation; CR5 logged as a
  v1 candidate (protocol_tier), not yet active.

v2 (comparability-v2.0, approved at Gate 1, r0/GATE1.md decision 4). The rule IDs are
RENUMBERED; this table is the authoritative mapping so nothing silently moves:

| v2 id | meaning | relation to v1 | source |
|---|---|---|---|
| CR1 | electrolyte identity + concentration must match | tightens v1 "CR1 canonical electrolyte list" from a list to an identity+concentration equality veto | B2 abstract (matched basis) |
| CR2 | current-density value + normalisation must match | NEW as a first-class veto (v1 CR2/CR3 were unit-canonicalisation plumbing, now folded into units.py) | B2 sec. 3.2 |
| CR3 | iR-compensation FRACTION must match | NEW; enabled by conditions delta D-1 (ir_correction boolean -> fraction) | B2 sec. 3 (RuO2 437->382 mV) |
| CR4 | temperature must match | NEW first-class veto | B2 abstract (room temperature) |
| CR5 | protocol_tier must match, binned from duration | ACTIVATES the v1 CR5 candidate with a preregistered duration-to-tier rule | ref 27 + B3 |

Notes:
- v1 unit-canonicalisation (old CR2/CR3) is not deleted; it moved into ledgerv2/units.py and
  is applied by every numeric predicate. Only its rule-ID slots were reused for the new vetoes.
- Duration-to-tier binning (CR5, ledgerv2/tiers.py, preregistered): <1 h ht_screen;
  [1 h, 2 h) medium_term; >=2 h long_term (McCrory 2 h standard boundary). Unstated duration
  -> protocol_tier unstated -> CR5 vetoes.
- Default-deny and named-defect semantics are unchanged from v1.

## Extraction amendments (Gate 2, 2026-11-11) - preregistered before the K=40 harvest
Approved by Anu; agreement knob otherwise unchanged (S2). Implemented in ledgerv2/extraction/.
- A1 (material canonicalization): material names are canonicalized before the agreement check
  (ledgerv2/extraction/materials.py: drop parenthetical qualifiers like "(commercial)", strip
  baseline words, map baseline synonyms), so string variants of ONE material pair instead of
  contesting. Distinct chemistries never merge.
- A2 (durations are claims, not conditions): a stated hold duration measured at a DIFFERENT
  current density, or coupled by phrasing like "together with", becomes its own claim
  (separate_stability metadata), NEVER a condition on the activity card. Only activity_hold_hours
  (the hold of THIS overpotential at THIS current) feeds protocol_tier.
- A3 (electrolyte attribution context): electrolyte Methods attribution is restricted to
  electrochemical-measurement sentences; synthesis and washing sentences never qualify. A claim
  whose electrolyte comes from a non-measurement context has its electrolyte nulled (-> unstated).
- Scope: commercial baseline materials (RuO2, IrO2, Ir/IrOx, Pt, Pt/C) are explicitly in scope
  for extraction as the densest cross-paper cluster.
- Mechanical: a stated ir_correction fraction always carries its quote (filled from the iR
  Methods sentence, else the overpotential source sentence).

## Pipeline fixes + amendments (Gate 3, 2026-11-11) - preregistered before re-extraction and K2
Approved by Anu. Recorded here BEFORE any run.
- F1 (acid-context harvest filter): a harvested paper is kept in an acid cluster only if its
  full text states an acid-electrolyte MEASUREMENT context (H2SO4/HClO4/"acidic", OER test);
  alkaline-only papers are excluded from acid clusters.
- F2 (review detection): exclude reviews by article-type metadata AND by the attribution pattern
  of predominantly citing other groups' materials; reviews carry only secondary claims (D8).
- F3 (A3 extension): the non-measurement electrolyte-context exclusions now include
  reagent-purchase / supplier sentences (e.g. "purchased from", "Sigma-Aldrich", "99.9%").
- F4 (computed_not_stated): a quantity VALUE must be stated verbatim; a value computed from a
  potential (via an assumed 1.23 V), from a percentage, or otherwise derived is rejected with a
  new `computed_not_stated` class. The model must return the number as it appears in the sentence.
- A4 (temperature attribution): temperature is taken only from a quoted Methods measurement
  sentence; "room temperature"/"ambient"/"25 C" map to the room_temperature enum with the quote;
  no temperature is inferred.
- A5 (technique-to-tier mapping, preregistered): protocol_tier is set from the measurement
  technique when a hold duration is absent - chronopotentiometry/chronoamperometry holds bin by
  duration (CR5); LSV/CV/polarization sweeps bin to `other_stated` carrying the technique quote;
  an unstated technique stays unstated (vetoes).

## A4 temperature-recall fix (Gate 4, 2026-11-11) - preregistered BEFORE re-extraction and re-census
Approved standing-default; recorded here BEFORE any run. Surfaced by OQ-V2-1: A4 as shipped at
Gate 3 attributed temperature only when the extraction model populated the dedicated
`temperature` field AND a non-empty `temperature_methods_quote`. When the model left `temperature`
null but the stated measurement temperature sat inside the overpotential sentence itself
("...curves in 0.5 M H2SO4 at room temperature...", PMC10005387) or inside the quoted electrolyte
measurement sentence, the card recorded temperature=unstated. That under-counted stated
temperatures and OVER-stated temperature as a field-level under-reporting gap in the census.
- A4-recall (this change): temperature attribution is a deterministic pass over the cached model
  output. It captures BOTH an in-sentence statement (the overpotential `source_sentence`) AND a
  Methods statement (`temperature_methods_quote`, and the measurement-context `electrolyte_methods_quote`),
  quoted either way. Only these three MEASUREMENT-context quoted fields are scanned - never a
  synthesis/washing/drying sentence - so the correct Gate-3 behaviour (do NOT attribute a
  "dried at room temperature" synthesis step, PMC10154325) is preserved structurally.
- Extended pattern set: `room temperature` / `room-temperature`, `ambient` (+ "ambient
  temperature/conditions"), `RT` / `R.T.` (standalone, guarded against acronyms like RT-PCR), and
  numeric Celsius variants (`25 °C`, `25°C`, `25 ◦C`, `25 degrees C`, `25 deg C`, `25 Celsius`,
  `80 centigrade`). A bare number with no degree marker and no Celsius word (e.g. "25C", "10 C")
  is intentionally NOT matched - ambiguous with coulombs / C-rate - and stays unstated (safe default).
- Typing is unchanged: a room-temperature phrase maps to the `room_temperature` ENUM; a numeric
  Celsius reading stays a NUMBER (TempValue, degC). Numeric is preferred over the enum within a
  sentence ("room temperature (25 °C)" -> 25). Nothing is inferred: attribution fires only on a
  literal pattern present in a measurement-context quote.
- Monotonic / no regression: if no pattern matches but the model itself set `temperature`
  (number or room_temperature) with a non-empty `temperature_methods_quote`, that stated value is
  kept (backward-compatible with every Gate-3 card). The change is recall-only; it never drops a
  previously attributed temperature.
- Cache discipline: the extraction SYSTEM/INSTRUCTION prompt strings are UNCHANGED, so every
  cache key is preserved and re-extraction runs entirely from cache (no API calls). The recall
  improvement is enforced at card-build time (review_queue._conditions_from_claim), which is why
  it applies to already-cached model outputs.
- Regression test: tests/test_ledgerv2.py adds the PMC10005387 sentence that exposed the gap plus
  numeric-Celsius / RT / ambient positives and a synthesis-step negative.
