# Gate 3 decisions (Anu, 2026-11-11) - transcribed

Adjudication of the 51 K=40 contested items (r2_out_k40/review_queue). Applied by
tools/apply_gate3.py -> r2_out_k40/approved/ ; record in r2_out_k40/gate3_decisions.json.

## APPROVE (17)
PMC10015077_0; PMC10015899_0; PMC10016623_0, _1; PMC10035503_0 (dedupe by provenance vs the v1
ref40 cards - one canonical set per paper; v1 ref40 approved set is empty, so this is the
canonical card); PMC10154325_0, _1, _2; PMC10161032_0, _1, _2; PMC10289644_0, _1, _2;
PMC11775546_0; PMC12537992_0, _1.

## REJECT (34) with reasons
- PMC10015899_1 - electrolyte attributed from a reagent-purchase sentence (F3).
- PMC10035503_1 - twin of _0.
- PMC10209667 _0.._7 (all 8) - alkaline, out of acid-cluster scope (F1).
- PMC10254529_0 - alkaline, out of scope (F1).
- PMC10357413_0, _1 - alkaline, out of scope (F1).
- PMC10475099_0 - false electrolyte identity: quote states NaCl/NaClO4, not HClO4; value a
  converted approximation (F4).
- PMC11935124 _0.._6 (all 7) - review paper, secondary per D8 (F2).
- PMC11936017 _0.._2 (all 3) - review and alkaline (F1/F2).
- PMC11935862 _0.._3 (all 4) - review pattern; verify article type, resubmit only if primary (F2).
- PMC5684209 _0.._2 (all 3) - values computed from potentials via an assumed 1.23 V;
  computed is not stated (F4).
- PMC7379386_0 - value not evidenced in any quote (F4).
- PMC12606313_0, _1 - duplicates of the Gate-2 approved pilot set.

## Pipeline fixes + amendments approved (preregistered in rules/CHANGELOG.md BEFORE any run)
F1 acid-context harvest filter; F2 review detection; F3 reagent/supplier electrolyte exclusion;
F4 computed_not_stated rejection class; A4 temperature Methods attribution (room_temperature
enum, quoted); A5 technique-to-tier mapping (sweeps -> other_stated with the technique quote).

## Validation note
Each rejection class maps to a now-automated filter: F1 would auto-exclude the alkaline papers
(PMC10209667, PMC10254529, PMC10357413, PMC11936017); F2 the reviews (PMC11935124, PMC11935862,
PMC11936017); F3 the reagent-purchase electrolyte (PMC10015899_1); F4 the computed values
(PMC5684209, PMC10475099_0) and the unevidenced value (PMC7379386_0). The re-extraction pass
measures how many of Anu's 34 manual rejects the filters reproduce automatically.
