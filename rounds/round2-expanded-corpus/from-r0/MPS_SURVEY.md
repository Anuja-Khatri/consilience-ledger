# MPS survey (A1) - acidic-OER coverage, condition keys, replicate floor

Source: CaltechDATA `hjfx4-a8r81`, CC-BY-4.0 (receipt in PROVENANCE.md). Loaded into local
PostgreSQL 16, database `mps`, schema `public_release` (dump server version 14.6). Survey
tables built in schema `r0survey`. All numbers below are queries over the loaded data on
2026-11-10; the exact SQL is reproduced in this file and in `r0/sql/`. Research only.

## 0. Scale as loaded (actual, not the paper headline)
- `sample`: 12,159,999 rows   `analysis`: 3,980,832 rows   FOM-type analysis: 2,713,725.
- The ESAMP paper headline (>6M measurements / 1.5M samples) describes a different cut;
  R0 reports the loaded counts (OQ-R0-7).
- `process_detail` eche defs: 6,168; of these 5,640 carry the OER redox couple (O2/H2O).
  9 distinct electrolytes store-wide.

## 1. Core UNKNOWN resolved: how much ACIDIC OER data, and on what
"Acidic" defined before counting as: eche process whose `electrolyte` matches
H2SO4/HClO4/H3PO4 OR whose `solution_ph` < 3. OER = O2/H2O couple (the eche default here).

- Acidic eche process definitions: 584;  acidic eche processes: 1,075.
- Acidic sample-process measurements: **163,846**, across **103,483 distinct samples**
  (each acidic process runs over a full combinatorial plate).
- Acidic overpotential VALUES successfully linked to FOMs:
  - **152,133 CP (chronopotentiometry) overpotential rows** (`CP_FOMS_standard.Eta.V_ave`),
    across **102,148 distinct samples** -- the bulk of the acidic-OER activity data.
  - 634 CV "specific-toggle" rows giving eta at a defined current threshold
    (451 at ithresh 3e-5 A, 183 at 1e-4 A) -- the cleanest "eta at a fixed current" analog.
- Electrolyte split of the acidic measurements: H2SO4(aq) 118,553 sp / 85,735 samples;
  a pH~2.9 phosphate set 44,227 sp / 17,570 samples; "other" 1,066.
- pH split: pH 0 (H2SO4) 103,924 sp; pH 2.8-2.92 ~44k; pH 1-1.4 ~16k.

### Metal coverage -- the decisive result for fork-source A1
- Across ALL 12.16M samples: **Pd in 8,448 samples, Ru in 0, Ir in 0.**
- Among the 103,483 ACIDIC samples: **Pd 0, Ru 0, Ir 0.** The 8,448 Pd samples are all
  measured under non-acidic (alkaline/neutral) conditions.
- The acidic-OER samples are earth-abundant transition-metal OXIDE combinatorial libraries.
  Element frequency among acidic samples (distinct samples):
  Co 92,853; Mn 74,764; Ta 66,096; Sb 59,170; Fe 35,426; Sn 33,105; Ce 24,178; Ni 21,742;
  La 10,651; Cu 6,520; Zn 4,071; W 3,878; Mg 2,172; Sr 21; V 6.

**Implication (Gate-1 input, not a Claude decision):** MPS (A1) is a rich acidic-OER source
on non-noble metal-oxide compositions (Co/Mn/Ta/Sb/Fe...), matched by electrolyte and current
convention. It cannot supply Pd/Ru/Ir matches -- the B1 literature harvest is Pd/Ru/Ir-focused,
so A1 x B1 forks will NOT overlap on active metal. A1's live roles are (a) within-acid,
same-composition comparisons and (b) the empirical replicate floor below. See FORK_CENSUS.md.

## 2. Overpotential distribution (sanity; acidic CP, mV)
p01 257 | p25 581 | p50 **642** | p75 810 | p99 1163. A ~642 mV median is physically sensible
for earth-abundant oxides in acid (noble-metal-free OER in acid is intrinsically high-eta).
Values used only in range [0,2] V to drop obvious artifacts.

## 3. Empirical replicate floor (the S3 result)
Three nested definitions of "replicate", most-to-least strict:
- **Floor-A, same physical sample + same CP stage, repeated** (pure measurement repeatability):
  6,249 groups, median stddev **22.4 mV**, median range 45.8 mV, p90 stddev 129 mV.
- Same physical sample, across CP stages: 38,375 groups, median stddev 57.5 mV, range 117.8 mV.
- **Floor-B, same composition (fractions rounded 0.05) + electrolyte + stage, across library
  samples** (sample-to-sample + measurement -- the relevant floor when matching a literature
  claim to a dataset row): 9,709 blocks (avg 6.6 members), median stddev **51.1 mV**,
  median range 132.3 mV, p90 stddev 131.8 mV, p90 range 392.1 mV.

**Reading:** the data-derived within-lab reproducibility floor for acidic-OER overpotential in
MPS is ~22 mV (strict repeat) to ~51 mV (composition-matched), with heavy tails above 100 mV --
far above the stated 13 mV floor. This is first-party evidence for the S3 floor policy
(floor = max(stated uncertainty, 13 mV, empirical block floor for the matching condition
block)). It does not depend on the ESAMP paper's own number (OQ-R0-2).

## 4. The ten condition keys, surveyed against MPS fields
How well each locked condition key can be populated from MPS structured fields:
| key | MPS source | availability |
|---|---|---|
| electrolyte | `electrolyte` + `solution_description` + `concentration` (all 1075 acidic defs) | FULL |
| ph | `solution_ph` (all) | FULL |
| current_density | `current_abs` (A) / `measurement_area` (cm2) x 1000 | STATED for only 6,388 / 152,133 acidic CP rows (4.2%), all phosphate buffer at 0.05-0.16 mA/cm2; `measurement_area = 0.0` on ALL 118,553 H2SO4 rows so it is ABSENT there (data absence, not derivation choice) |
| protocol_tier | CP stage (CP3/CP4) + `acquisition_time` hold duration | DERIVABLE |
| anneal_temperature | separate `anneal` process in the sample's process chain (sample_process) | DERIVABLE via chain |
| loading | `jcap_loading` table + inkjet/platemap loading on `sample` | PARTIAL |
| substrate | plate/electrode implied by platemap; not an explicit field | PARTIAL |
| prior_operation_duration | prior CA/CP steps + `acquisition_time` | PARTIAL |
| temperature | no temperature field in eche params | UNSTATED (absent) |
| ir_correction | `reference_vrhe`/`potential_vref` are RHE referencing, NOT iR compensation; no iR fraction field | UNSTATED (absent) |

**Note for the conditions-vector delta:** even this richest structured dataset leaves
`temperature` and `ir_correction` unstated. The absence of an iR-compensation field here, next
to B2's RuO2 437->382 mV example, is independent support for refining the `ir_correction` key
(see CONDITIONS_DELTA.md).

## 5. Reproducibility of this survey
Dump restored with `tar xzOf public_release_20230228.tar.gz | psql -d mps`. Survey tables:
`r0survey.acid_proc` (acidic processes), `r0survey.acid_sp` (acidic sample-processes with
composition), `r0survey.acid_cp_fom` (acidic CP overpotential values). SQL saved under
`r0/sql/mps_survey.sql`. No write touched `public_release`; the raw dump archive is unchanged.
