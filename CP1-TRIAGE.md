# Checkpoint 1 triage (drafted by Claude for Anu's decision, 10 Nov 2026)

Drafted from the review-queue files only (source sentences + both cards). I did not
re-read the full papers; every recommendation is judged against the quoted sentence,
which is the card's own evidence. You decide; override any row.

## 1. Headline

- 72 files, but only ~34 distinct claims. The rest are twin files of the same claim
  (pairing failed on exact fields, so each model's card got its own file), repeated
  facts from near-duplicate sentences, and 2 cards with invented values.
- Recommend: approve 34 (about 20 with batch corrections), reject 38.
- Four systemic patterns (S1-S4) are best fixed as batch rules (BR1-BR7), not hand-edits.

## 2. Systemic findings

- S1 LEAKED IDS (all 72): every card carries few-shot ids (claim_id EX1..EX9,
  provenance_hash ex2a..). Cosmetic. Fix mechanically at apply time (BR1).
- S2 CONDITIONS NOT IN SENTENCE (worst issue, ~30 cards): cards state electrolyte
  (1 M H2SO4 / 1 M HClO4), current density, loading, or substrate that the quoted
  sentence does not contain. This is the unstated-condition inference D10 forbids,
  arriving through extraction. Fix: BR2 strips them to "unstated". This is conservative,
  it strengthens the condition_unstated thesis result, and the roadmap item
  (paper-global condition attribution) stays a future, disclosed improvement.
- S3 INVENTED VALUES (2 cards): ref40_003 (66 uV/h) and ref40_032 (500 h) attach
  numbers to sentences that contain no number. Reject; the same facts are properly
  carded elsewhere.
- S4 DUPLICATES: twin files (same claim, one per model) and repeated facts from
  near-duplicate sentences (e.g. 196 mV appears in 6 files). One canonical card per
  fact (BR3), rejects marked "dup".

## 3. Batch rules for apply_review (Claude Code implements; your approval of this
## document is the authorization)

- BR1 Regenerate claim_id and provenance_hash for every approved card; no EX/ex ids survive.
- BR2 Sentence-evidence rule: any condition value not present in the card's
  source_sentence is reset to "unstated". No exceptions in v1.
- BR3 Dedup: approve only the canonical file per distinct claim (table below); twins
  and repeated facts are rejected as "dup".
- BR4 Bound fixes from sentence language: "below/under/up to" -> upper;
  "exceeded/more than/>" -> lower; "~/about" -> approx. Specific re-typings:
  2609_001/002 become stability_lifetime claims (time to exceed the 0.5 V threshold:
  NiTaPdOx ~470 h, PdOx ~200 h, bound approx), mirroring the lifetime form of 2609_006/007.
  ref40_021: durability "up to 500 h" -> bound upper, not exact.
- BR5 Ranges (CC-01): 2609_024 molar loss is 0.3-0.7 umol/cm2, carded as a range,
  not 0.5 approx.
- BR6 Reject class "value not in sentence": ref40_003, ref40_032.
- BR7 Axis unification: one mass_activity axis (replace *_at_overpotential /
  *_at_potential variants). physical_scale and measurable_with disagreements are
  vocabulary noise, not veto fields; normalize gently, never block on them.

## 4. Per-file decisions (A = claude-sonnet-5 card, B = gpt-4.1 card; c = with corrections)

### Their paper (2609.30133)
| file | rec | reason |
|---|---|---|
| 001 | APPROVE B c | re-type per BR4: NiTaPdOx lifetime ~470 h to 0.5 V; strip electrolyte+cd (BR2) |
| 002 | APPROVE B c | same, PdOx ~200 h |
| 003 | APPROVE A | cd + iR both in sentence; B adds H2SO4 not in sentence |
| 004 | APPROVE A | RuOx 0.41 V, cd + iR in sentence |
| 005 | APPROVE B c | 96% Pd after 1000 h, XRF; strip electrolyte+cd (BR2) |
| 006 | APPROVE B | CoFeZrOx lifetime <4 h, bound upper correct; subject from adjacent sentence (standard antecedent resolution, fine) |
| 007 | APPROVE B | CoInZrOx, same |
| 008 | REJECT | dup of 023 built on a fragment sentence with inferred subjects |
| 009 | REJECT | dup, same |
| 010 | APPROVE B c | InMnPdOx <0.5 V over 1000 h, bound upper; strip electrolyte+cd |
| 011 | REJECT | same fact as 010 from a near-duplicate sentence; bound also wrong |
| 012 | APPROVE B c | NiTaPdOx 88% after 575 h; strip electrolyte+cd, keep duration |
| 013 | APPROVE B c | PdOx 87% after 828 h; same strip |
| 014 | APPROVE B c | RuOx 59% after 661 h; same strip |
| 015 | REJECT | dup of 013; mw icp_ms contradicts the paper's XRF |
| 016 | REJECT | dup of 014; same mw problem |
| 017 | APPROVE A c | SEC reproduces within 15 mV; strip substrate (not in sentence) |
| 018 | REJECT | summary restatement of 010 (platform-level), subject inferred |
| 019 | REJECT | same summary sentence |
| 020 | APPROVE B | CoFeZrOx 0.55 V at 10 mA/cm2; cd in sentence |
| 021 | APPROVE B | CoInZrOx, same |
| 022 | REJECT (your scope call) | >90% automation: real claim, never OER-comparable; approve only if you want platform claims in the ledger |
| 023 | APPROVE B | Pd-rich In-Mn/Ni-Ta systems <0.46 V at 10; cd in sentence |
| 024 | APPROVE B c | molar loss as RANGE 0.3-0.7 umol/cm2 (BR5) |
| 025 | REJECT | automation dup of 022 with fabricated electrolyte+cd conditions |

### ref 40 (Peng 2023)
| file | rec | reason |
|---|---|---|
| 001 | REJECT | fragment; fact carded fully in 010 |
| 002 | APPROVE A | Pd-55 500 h at 10 mA/cm2 in 1 M HClO4; all conditions in sentence |
| 003 | REJECT | BR6: 66 uV/h not in this sentence |
| 004 | APPROVE A c | dG2 0.13 eV DFT; strip substrate Pd(111) if not in sentence |
| 005 | REJECT | 407.2 fact canonical in 026 (which carries the 1.53 VRHE context) |
| 006 | APPROVE A c | dG3 2.79 eV; same substrate strip |
| 007 | REJECT | twin of 009 |
| 008 | REJECT | twin of 010 |
| 009 | APPROVE B c | 1.664 V at 1 A/cm2, 65 C; strip loading+substrate (not in sentence); mw polarization_curve matches sentence |
| 010 | APPROVE B c | 1.771 V at 2 A/cm2, 65 C; same strip |
| 011 | APPROVE A c | >40 h at 100 mA/cm2, bound lower; strip electrolyte |
| 012 | REJECT | twin of 011 |
| 013 | APPROVE A c | PdCoO2 528 mV; strip cd+electrolyte (neither in sentence) |
| 014 | REJECT | twin of 013 |
| 015 | REJECT | electrode-fabrication statement, not a performance claim |
| 016 | REJECT | fragment; 66 uV/h canonical in 040 |
| 017 | REJECT | fragment twin |
| 018 | REJECT | twin of 019 (which captures anneal 55 C stated in sentence) |
| 019 | APPROVE B c | Tafel 51.3 mV/dec, anneal 55 C in sentence; strip electrolyte |
| 020 | APPROVE A | Pd-25 MA 3.7 A/g; A's mw sensible, B's EIS wrong |
| 021 | APPROVE A c | durability up to 500 h -> bound upper (BR4) |
| 022 | APPROVE A | Pd-55 196 mV at 10 in 1 M HClO4; ALL conditions in sentence; canonical 196 card |
| 023 | REJECT | near-duplicate sentence, same two facts |
| 024 | REJECT | same |
| 025 | APPROVE A c | dissolution 0.14 ng/cm2/s; strip cd+electrolyte, keep 500 h |
| 026 | APPROVE A c | MA 407.2 at 1.53 VRHE; strip electrolyte; axis per BR7 |
| 027 | REJECT | twin of 026 |
| 028 | REJECT | 196 dup (canonical 022) |
| 029 | REJECT | 196 dup |
| 030 | REJECT (scope) | HER claim, outside the OER ledger; approve only if you want HER background |
| 031 | REJECT (scope) | HER twin |
| 032 | REJECT | BR6: 500 h not in this sentence |
| 033 | APPROVE A c | Pd-25 348 mV at 10; strip electrolyte |
| 034 | APPROVE A c | Pd-40 280 mV at 10; strip electrolyte |
| 035 | REJECT | 196 dup (canonical 022) |
| 036 | REJECT | twin of 033 with anneal temp derived from the material name |
| 037 | REJECT | twin of 034, same |
| 038 | REJECT | 196 dup, same |
| 039 | REJECT | fragment inverse of 010 |
| 040 | APPROVE A c | 66 uV/h at 10 for 500 h, canonical; strip electrolyte |
| 041 | REJECT | twin of 040 |
| 042 | REJECT | twin of 044 |
| 043 | REJECT | twin of 044 |
| 044 | APPROVE A | MA 34.6 A/g (~5.4 nm); A's scale+mw sensible |
| 045 | APPROVE A | particle size ~3 nm TEM; empty conditions, honest |
| 046 | REJECT | twin of 045 with electrolyte absurdly attached to a TEM claim |
| 047 | REJECT | 66 uV/h dup from the comparative sentence |

Approve 34, reject 38 (3 rows are your scope calls: 2609_022, ref40_030, ref40_031).

## 5. Comparability rules (your confirmation)

CR1-CR4 are sound and match their stated sources; confirm as comparability-v0 with two
notes for Claude Code:
- CR1 needs a canonical electrolyte identity list (H2SO4 = sulfuric acid; HClO4 =
  perchloric acid) so identity equality is never a string accident.
- CR3/CR2 unit spellings (degC vs C; mA/cm^2 variants) must canonicalize through pint
  before the predicate runs.

One open option, your call, consequence stated plainly: a CR5 on protocol_tier
(screening-tier vs long-term tier never comparable) matches Lila's own "comparative not
absolute" framing, but the stated rate for tier is 0.00, so adding it now makes every
pair condition_unstated and the ledger 100% veto. Recommend: log CR5 as a sourced
candidate for v1, do not add in v0.

## 6. Honesty line for the record

These recommendations were drafted by Claude against sentence-level evidence and
decided by Anu; decisions and all overrides are Anu's. That is the same disclosed
method as the rest of the project.
