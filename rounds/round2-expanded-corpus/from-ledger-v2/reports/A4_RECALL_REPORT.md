# A4 temperature-recall fix - report (stops at the fresh K2 review queue)

Preregistered in `rules/CHANGELOG.md` ("A4 temperature-recall fix (Gate 4)") BEFORE any run.
Resolves OQ-V2-1. 23 tests green. No API calls: re-extraction ran entirely from cache (the
extraction prompt strings are unchanged, so every cache key was preserved).

## What changed (code)
- `ledgerv2/extraction/temperature.py` (new): `attribute_temperature(claim)` - a deterministic
  pass over the cached model claim. Temperature is read from a quoted MEASUREMENT-context sentence,
  captured **both** in-sentence (the overpotential `source_sentence`) **and** from a Methods
  statement (`temperature_methods_quote` + the measurement `electrolyte_methods_quote`), quoted
  either way. Only those three measurement fields are scanned - never a synthesis/washing/drying
  sentence - so the correct Gate-3 behaviour (do NOT attribute a "dried at room temperature"
  synthesis step) is preserved structurally.
- Pattern set extended: `room temperature` / `room-temperature`, `ambient` (+ ambient
  temperature/conditions), `RT` / `R.T.` (standalone, guarded against RT-PCR-type acronyms), and
  numeric Celsius variants (`25 °C`, `25°C`, `25 ◦C`, `25 degrees C`, `25 deg C`, `25 Celsius`,
  `80 centigrade`). A bare `25C`/`10 C` with no degree marker is deliberately NOT matched
  (ambiguous with coulombs / C-rate) and stays unstated - the safe default.
- Typing unchanged: a room-temperature phrase → the `room_temperature` ENUM; a numeric reading
  stays a NUMBER (`TempValue` degC); numeric wins over the enum inside one sentence. Nothing is
  inferred. Monotonic: if nothing parses but the model itself stated a temperature with a quote,
  that value is kept - the change is recall-only and never drops a previously-attributed temperature.
- Wired into `ledgerv2/extraction/review_queue._conditions_from_claim`, so it flows through every
  card builder (`card_from_agreed`, `apply_gate2`, `apply_gate3`, reextract, K2).
- Regression test `tests/test_ledgerv2.py`: the PMC10005387 sentence that exposed the gap, plus
  numeric-Celsius / RT / ambient positives, a numeric-preferred-over-enum case, a no-false-positive
  case (bare `10 C`, `RT-PCR`), a synthesis-step negative, and a monotonic back-compat case.

## 1. Corrected temperature-stated rate
Genuine A4 recoveries (old logic = unstated → now stated), measured on the identical cached
claims: **3 cards** - `PMC10289644:g3_0/1/2` (all `room_temperature`), recovered from the Methods
measurement sentence *"All OER measurements were performed in a three-electrode configuration
using 0.1 M HClO4 … at room temperature"*. The model had left its `temperature` field null while
stating it in the measurement sentence; the old quote-gated rule therefore missed it.

The other temperature-stated cards (PMC10005387 ×2, the reextract/K2 RuIr-baseline papers, the v1
peng2023 65 °C cards) were already captured under the old logic and are unchanged.

| census | before fix | after fix |
|---|---|---|
| Full census (66 approved cards) | 4/66 = 6.1 % | **7/66 = 10.6 %** |
| K2 census (73 cards) | 6/73 = 8.2 % | **9/73 = 12.3 %** |

## 2. New veto distribution
Byte-identical to Gate 3 - the recall fix did **not** change a single pair outcome (explained in §3).

Full census - 66 cards, 22 blocks, **172 vetoed pairs**, 0 forks, 0 corroborations:
| defect | pairs |
|---|---|
| condition_unstated:temperature | 172 |
| condition_unstated:protocol_tier | 155 |
| condition_unstated:ir_correction | 152 |
| condition_unstated:electrolyte | 53 |
| condition_mismatch:CR2 | 22 |
| condition_mismatch:CR1 | 20 |
| condition_unstated:current_density | 9 |
| condition_mismatch:CR3 | 8 |

K2 census - 73 cards, 23 blocks, **210 vetoed pairs**, 0 forks, 0 corroborations:
| defect | pairs |
|---|---|
| condition_unstated:temperature | 210 |
| condition_unstated:ir_correction | 188 |
| condition_unstated:protocol_tier | 181 |
| condition_unstated:electrolyte | 65 |
| condition_mismatch:CR2 | 24 |
| condition_mismatch:CR1 | 20 |
| condition_unstated:current_density | 10 |
| condition_mismatch:CR3 | 10 |

## 3. Forks or corroborations that now clear
**None.** 0 forks and 0 corroborations in both censuses, unchanged.

Why the recovery clears nothing: a `temperature` defect fires when **either** side of a pair is
unstated. Every temperature-stated card sits in a block whose stated-temperature cards all come
from a **single source** (PMC10289644 ×3 in `hclo4/unstated`; PMC10005387 ×2 in
`hclo4/other_stated`; peng2023 ×2 in `unstated/unstated`). Same-source pairs are excluded, so **no
cross-source pair has a stated temperature on both sides** - the temperature defect still fires on
all 172 / 210 pairs. The 3 recovered cards also still veto on other unstated conditions.

Decisive consequence for OQ-V2-1: the 210/210 temperature vetoes were **not** an A4 extraction
artifact. Fixing recall recovered only what was genuinely stated (3 cards) and moved nothing. The
remaining temperature-unstated cards genuinely do not state a measurement temperature. Temperature
under-reporting is real - and, per §4, it is never the *sole* missing condition.

## 4. Near-miss table - pairs one condition short of comparable
**Exactly one condition short: ZERO pairs**, in both the full and the K2 census. No pair is a
single stated condition away from comparable.

Distribution of how far each K2 cross-source pair is from comparable:
| conditions short | pairs |
|---|---|
| 2 | 31 |
| 3 | 80 |
| 4 | 89 |
| 5 | 10 |

The closest tier is **two conditions short (19 unique pairs after deduping the PMC10005387
reextract/K2 double-listing)**, and **every one of them includes temperature as one of its two
missing conditions** - i.e. if temperature were universally stated, each would collapse to exactly
one condition short (the named partner). The partner condition is ir_correction (15),
protocol_tier (2), or a CR3 iR-fraction mismatch (2, genuinely incomparable - not fillable).

| missing conditions | A (mV, paper) | B (mV, paper) | \|Δ\| mV | block |
|---|---|---|---|---|
| CR3 + temperature | SrIrO3 256 (PMC10005387) | porous Pt layer 140 (PMC5684209) | 116 | hclo4/other_stated |
| CR3 + temperature | SrFe0.1Ir0.9O3 238 (PMC10005387) | porous Pt layer 140 (PMC5684209) | 98 | hclo4/other_stated |
| ir_correction + temperature | Pd/C 465 (PMC11077676) | porous Pt layer 140 (PMC5684209) | 325 | hclo4/other_stated |
| ir_correction + temperature | SrFe0.1Ir0.9O3 238 (PMC10005387) | Pd/C 465 (PMC11077676) | 227 | hclo4/other_stated |
| ir_correction + temperature | PdCu/C 354 (PMC11077676) | porous Pt layer 140 (PMC5684209) | 214 | hclo4/other_stated |
| ir_correction + temperature | Pd/C 465 (PMC11077676) | SrIrO3 256 (PMC10005387) | 209 | hclo4/other_stated |
| ir_correction + temperature | Ir/C 301 (PMC11077676) | porous Pt layer 140 (PMC5684209) | 161 | hclo4/other_stated |
| ir_correction + temperature | PdCu/C 354 (PMC11077676) | SrFe0.1Ir0.9O3 238 (PMC10005387) | 116 | hclo4/other_stated |
| ir_correction + temperature | PdCuIr/C 247 (PMC11077676) | porous Pt layer 140 (PMC5684209) | 107 | hclo4/other_stated |
| ir_correction + temperature | PdCu/C 354 (PMC11077676) | SrIrO3 256 (PMC10005387) | 98 | hclo4/other_stated |
| ir_correction + temperature | PdCuIrCo/C 221 (PMC11077676) | porous Pt layer 140 (PMC5684209) | 81 | hclo4/other_stated |
| ir_correction + temperature | Ir/C 301 (PMC11077676) | SrFe0.1Ir0.9O3 238 (PMC10005387) | 63 | hclo4/other_stated |
| ir_correction + temperature | Ir/C 301 (PMC11077676) | SrIrO3 256 (PMC10005387) | 45 | hclo4/other_stated |
| ir_correction + temperature | PdCuIrCo/C 221 (PMC11077676) | SrIrO3 256 (PMC10005387) | 35 | hclo4/other_stated |
| ir_correction + temperature | SrFe0.1Ir0.9O3 238 (PMC10005387) | PdCuIrCo/C 221 (PMC11077676) | 17 | hclo4/other_stated |
| ir_correction + temperature | PdCuIr/C 247 (PMC11077676) | SrFe0.1Ir0.9O3 238 (PMC10005387) | 9 | hclo4/other_stated |
| ir_correction + temperature | PdCuIr/C 247 (PMC11077676) | SrIrO3 256 (PMC10005387) | 9 | hclo4/other_stated |
| protocol_tier + temperature | Ir/IrOx (commercial) 255 (PMC12606313) | py-RuO2:Zn 173 (PMC10154325) | 82 | h2so4/unstated |
| protocol_tier + temperature | Ir/IrOx~SO3H 233 (PMC12606313) | py-RuO2:Zn 173 (PMC10154325) | 60 | h2so4/unstated |

Reading: the HClO4 `other_stated` block (PMC11077676 Pd/Pt-group multimetallics, PMC10005387
SrIr-oxides, PMC5684209 Pt) is the densest pocket of near-comparable acidic-OER claims. Each pair
there needs its iR practice stated on both sides (and temperature on the non-RT side) before the
judge can call a fork or a corroboration. The 2 CR3 pairs are a genuine iR-fraction *mismatch*, not
a missing value - they stay incomparable even if temperature is filled.

## Stop point
Stopped at the fresh K2 review queue (`r2_out_k2/review_queue/INDEX.md`): 20 papers, 7
agreed-provisional, 17 contested - regenerated under the fix so Anu never adjudicates stale cards.
Reports regenerated: `reports/FULL_CENSUS.md`, `reports/K2_CENSUS.md`, this file, and
`reports/a4_nearmiss_table.json`. Next gate is Anu's: adjudicate the 17 K2 contested, and fill
ir_correction / protocol_tier on the §4 near pairs to convert them into candidate forks.
