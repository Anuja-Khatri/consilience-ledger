# Route 1 receipts - matched-sample conditions reproduced from the pipeline

Route 1 = composition match of Lila's acid-OER screening rows against the
Materials Provenance Store (MPS) at tolerance **t = 0.05** in identical
**1.0 M H₂SO₄**. These receipts turn the session-reported Route-1 numbers into
committed, re-derivable tables.

## Provenance / inputs
- **Lila screening rows** - `upstream/lila_oer_manuscript/data/oer_exp_data.csv`
  (committed clone). 1,125 rows with valid composition.
- **MPS** - local read-only PostgreSQL database `mps` (CaltechDATA record
  `hjfx4-a8r81`, CC-BY-4.0). No MPS data bytes are committed; the queries that
  read it are in `feasibility/sql/` and in the scripts here.
- Matchable DB subset: `r0survey.acid_cp_fom` rows with `eta_v_ave` not null,
  `electrolyte='H2SO4(aq)'`, `comp` a json object, and process
  `concentration='1'` (= "1.0 M sulfuric acid"). Export query:
  `feasibility/sql/04_export_h2so4_1M_samples.sql`.

## Reproduction
```
psql -d mps --csv -f feasibility/sql/04_export_h2so4_1M_samples.sql > db_h2so4_1M.csv
python3 route1_match.py \
   ../../upstream/.../oer_exp_data.csv  db_h2so4_1M.csv  .
# -> pairs_t05.csv, matched_db_ids.txt ; prints the baseline below
```
The per-condition tables (a–c) are produced by grouping the matched sample set
against `process_detail.parameters` (see the SQL header comments in each file);
the (d) subset counts by `route1_subset_counts.py`.

## Baseline (independent re-derivation of the matched set)
| quantity | value |
|---|---|
| Lila rows (valid comp) | 1,125 |
| DB samples, H₂SO₄ 1.0 M (valid comp) | 69,273 |
| matched Lila-row / DB-sample pairs (t=0.05) | **7,115** |
| distinct matched DB samples | **1,881** |

Matches the session figures exactly. (The raw DB export carries 69,278 sample
rows; 5 drop on composition normalisation, leaving 69,273 - the number the
pipeline actually matches against.)

## (a) Technique and recorded current per row - `table_a_technique_current.csv`
CP rows of the 1,881 matched samples, by technique and `current_abs` (amperes).
| technique | current_abs (A) | current | n_rows | n_samples |
|---|---|---|---|---|
| CP3 | 0.00003 | +30 µA | 1,849 | 1,828 |
| CP4 | 0.0001 | **+100 µA** | 297 | 297 |
| CP4 | 0.0003 | +300 µA | 273 | 261 |
| CP4 | -0.0001 | −100 µA | 53 | 53 |

Note the sign: a separate CP4 group runs at **−**100 µA (0.0001 A), distinct
from the +100 µA subset in (d).

## (b) Acquisition-time distribution - `table_b_acquisition_time.csv`
| technique | acquisition_time (s) | n_rows | n_samples |
|---|---|---|---|
| CP3 | 15.0 | 1,787 | 1,766 |
| CP4 | 15.0 | 561 | 549 |
| CP3 | 10.0 | 62 | 62 |
| CP4 | 10.0 | 62 | 62 |

Hold windows are 10–15 s - i.e. short screening holds, not Lila's 10-minute
activity point (see (e)).

## (c) Substrate, fabrication method, anneal temperature - matched samples
`table_c_substrate.csv`, `table_c_fabrication.csv`, `table_c_anneal.csv`
(counts over the 1,881 matched samples).

Substrate (plate-level, `collection.details->>'substrate'`):
| substrate | n_samples |
|---|---|
| Glass FTO Tec 15 | 928 |
| Glass FTO Tec 7 | 900 |
| Round glass Molybdenum | 53 |

Fabrication method (`print.parameters->>'method'`): **INKJET - 1,881 / 1,881**
(100 %).

Anneal max temperature (°C, via `sample_process → process_detail type=anneal`):
| anneal max T (°C) | n_samples |
|---|---|
| 350 | 1,603 |
| 450 | 171 |
| 300 | 53 |
| 605 | 27 |
| 600 | 27 |

All 1,881 matched samples carry an anneal temperature (no "(no anneal)" row).

## (d) CP4 @ +100 µA subset - `table_d_cp4_100ua.csv`
Independent recompute vs. the session-reported figures:
| metric | recomputed | session-reported | match |
|---|---|---|---|
| CP4 @ +100 µA matched samples | **297** | 297 | ✅ |
| of the 7,115 pairs, those involving ≥1 such sample | **1,041** | 1,041 | ✅ |
| distinct matched compositions | **58** | 58 | ✅ |

All three reproduce exactly. "distinct matched compositions" is read as the
distinct **Lila-side** normalised compositions participating in the 1,041 pairs
(= 58). For reference, the same subset has 32 distinct DB-side compositions and
5 distinct element systems; these are not the reported figure.

## (e) Lila Methods hold-duration quote
> "OER screening is performed in 1 M H₂SO₄ in a custom-built scanning
> electrochemical cell (SEC). Activity is taken as the overpotential at 10
> mA cm⁻² **after 10 min**."

Source: Lila paper 2609.30133, Methods - cited in `feasibility/FEASIBILITY.md`
§1a as `corpus_in/text/2609.30133.txt` lines 180–182 (also 253–254, 282–284).
The 600 s hold matches the dataset field `overpotential_cp1_600s_mean`. (The
`corpus_in/` paper text is not committed - see `feasibility/PROVENANCE.md`.)
