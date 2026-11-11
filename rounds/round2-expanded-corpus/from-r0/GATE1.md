# GATE 1 decision sheet (Anu) - consilience-ledger v2

One page. Six decisions. Each: R0 evidence, proposed default, consequence. Fill-in at the end.
Full backing in R0_REPORT.md and the named r0/ files. Nothing is applied until you sign.

---

### 1. Fork paths for round one
- Evidence: MPS and Lila are both acidic CP-overpotential metal-oxide sets from the same
  JCAP/Gregoire platform; MPS holds 72,547 Co+Mn (and Mn-Sb etc.) acidic-oxide samples that
  overlap Lila's chemistry - a fork path needing zero paper extraction. Literature OA clusters
  are large: Pd/0.1 M HClO4/10 mA = 121; Co/0.5 M H2SO4/10 mA ~ 697 records.
- Default: run three - (a) MPS-vs-Lila Co-Mn structured path, (b) Pd-in-HClO4 literature
  cluster, (c) one Co-in-H2SO4 literature cluster; defer Ru, Ir, and McCrory to round two.
- Consequence: (a) can fork with no extraction and no API keys; (b)+(c) scope the first
  3-paper extraction pilot to two live clusters. Deferring Ru/Ir keeps round one small and
  avoids the metals MPS cannot anchor.

### 2. Two mapping approvals (one hash-locked approval each, admits all rows - S2)
**A1 - MPS -> Claim Card v2**
| MPS source (plain words) | -> card field |
|---|---|
| `CP_FOMS_standard` output `Eta.V_ave` (volts x1000) | overpotential value (mV) |
| params `electrolyte` + `concentration` | electrolyte |
| params `solution_ph` | ph |
| technique CP3/CP4 + hold time | protocol_tier (= ht_screen) |
| `current_abs` / `measurement_area` x 1000 | current_density (mA/cm2-geo) WHEN area > 0; else UNSTATED |
| `sample.final_composition` | material / axis |
| (no field) | temperature = unstated; ir_correction = unstated |

Example row as a card: *material Mn0.85Sb0.15 oxide; overpotential 532 mV; electrolyte 1 M
H2SO4 (pH 0); current_density UNSTATED (measurement_area = 0.0 on this H2SO4 row - area absent);
protocol_tier ht_screen; temperature unstated; ir_correction unstated; provenance = MPS sample
1700-1620, CP_FOMS_standard.* Claim belongs to the dataset (D8), never silently to an original
paper. (Current density IS stated for the 4.2% of acidic CP rows in phosphate buffer, where
measurement_area = 0.64 cm2; those rows block separately from the H2SO4 fork path.)

**A2 - Lila -> Claim Card v2**
| Lila column (plain words) | -> card field |
|---|---|
| `composition` | material / axis |
| `overpotential_cp1_600s_mean` (volts x1000) | overpotential value (mV) |
| `anneal_T` | anneal_temperature |
| Methods sentence "acidic ... H2SO4" (quoted on card) | electrolyte |
| CP 600 s hold | protocol_tier (= ht_screen) |
| fig_3e `overpotential_corrected` + Methods | ir_correction (fraction, if Methods states it) |

Example row as a card: *material Mn0.97Sb0.03 oxide; overpotential 688 mV; anneal 700 C;
electrolyte 0.5 M H2SO4 (quoted Methods); protocol_tier ht_screen; provenance =
lila_oer_manuscript oer_exp_data.csv.* (Pairs against the MPS card above on the Mn-Sb block.)
- Default: approve both mappings as written. Consequence: ~152,133 MPS + ~1,125 Lila claims
  admit for two human decisions; the Mn-Sb / Co-Mn structured fork becomes computable at R1.

### 3. Conditions-vector freeze - the one drafted delta (keeps ten keys)
- D-1 `ir_correction`: boolean -> stated **fraction** (0 = none ... 1 = full; else unstated).
  Justifying sentence, B2 (PMC13707403, sec. 3): *"the reported overpotential at 25 mA cm-2
  slid continuously from 437 mV uncompensated down to 382 mV at full compensation, depending
  on which fraction the author chose."* Independent support: MPS has no iR field at all.
- Default: accept D-1; keep the other nine keys unchanged.
- Consequence: a bare "iR-corrected" with no fraction becomes a comparability defect, not a
  silent equality; ~55 mV of hidden variance is modeled instead of ignored.

### 4. Comparability rules + CR5 (default-deny; each names its defect)
| rule | vetoes when | page-level source |
|---|---|---|
| CR1 electrolyte identity | electrolytes differ/unstated | B2 abstract: comparability only "on a matched basis (1 M KOH, room temperature)" |
| CR2 current-density convention | eta reported at different current density | B2 sec. 3.2: diverges "by more than 150 mV at 100 mA cm-2" vs 10 |
| CR3 iR-compensation fraction | fractions differ, or either unstated | B2 sec. 3 (the 437->382 mV sentence above) |
| CR4 temperature | temperatures differ/unstated | B2 abstract: "(1 M KOH, room temperature)" |
- CR5 protocol_tier (recommendation): adopt five tiers (ht_screen, medium_term, long_term,
  other_stated, unstated); veto on tier mismatch AND on unstated tier. Sources: ref 27
  (PMC10012258) activity-vs-stability distinction; B3 (PMC10576816): the McCrory protocol "is
  the most widely used, yet still only by an insignificant fraction of all OER publications."
- Default: approve CR1-CR4 and adopt CR5. Consequence: ht_screen MPS/Lila numbers never
  compare as equals to long-term stability literature; unstated conditions block equality.

### 5. Floor policy (supersession S3)
- Measured MPS acidic-OER within-lab reproducibility: **22 mV** (strict same-sample repeat,
  median), **51 mV** (same-composition block, median), **>130 mV** (p90) - vs the stated 13 mV.
- Default: floor = max(stated uncertainty, 13 mV, **51 mV** composition-block). Consequence by
  choice: 13 mV -> most "forks", many are just measurement noise (false forks); 22 mV -> fewer,
  excludes pure repeat scatter; **51 mV -> only >51 mV gaps count, fewest but most defensible
  forks**; 130 mV -> only large disagreements survive, near-zero forks. More conservative is
  always the larger floor.

### 6. ChemRxiv + FOR_ANU (no decision, status only)
ChemRxiv census deferred (Cloudflare bot-block; browser run noted in FOR_ANU.md). FOR_ANU.md
as it stands: (1) McCrory SI; (2) identify A4's DOI; (3) refs 4/15/16 if their text is wanted;
(4) ChemRxiv browser census. None blocked R0.

---

### Fill-in (one line each)
1. Fork paths round one: ______________________________________________
2. Approve A1 mapping? ___  Approve A2 mapping? ___  changes: ____________
3. Accept conditions delta D-1 (ir_correction -> fraction)? ___  other: ___
4. Approve CR1 __ CR2 __ CR3 __ CR4 __  Adopt CR5 as recommended? ___
5. Floor policy (13 / 22 / 51 / 130 / other): ___________________________
6. Sign supersessions S1 __ S2 __ S3 __   FOR_ANU owner/dates: ___________

---

## SIGNED ANSWERS (Anu, 2026-11-10) - verbatim

1. Fork paths round one: approved as the default, (a) MPS-vs-Lila Co-Mn, (b) Pd-in-HClO4
   literature cluster, (c) Co-in-H2SO4 literature cluster; Ru, Ir, McCrory deferred. Additions:
   report the 1 M HClO4 Pd cluster size so the v1 Peng claims can pair; and in R1, search MPS
   and ESAMP documentation for a stated iR-compensation practice for the CP technique, quoting
   and hashing any statement found; absent such a statement, path (a) is expected to yield a
   veto census rather than forks and runs anyway.
2. Approve A1 mapping: YES. Approve A2 mapping: YES. One addition to both: any fork between two
   ht_screen rows is labeled screening-tier provisional, honoring comparative-not-absolute; it
   is never presented as a settled disagreement about absolute activity.
3. Accept conditions delta D-1 (ir_correction becomes a stated fraction): YES.
4. Approve CR1 YES, CR2 YES, CR3 YES, CR4 YES. Adopt CR5: YES, with a preregistered
   duration-to-tier binning rule so stated durations yield stated tiers; unstated still vetoes.
   Document the rule renumbering versus v1 in the rules changelog.
5. Floor policy: 51 mV composition-block default, applied as max(stated uncertainty, 13 mV,
   51 mV) per S3.
6. Supersessions signed: S1 YES, S2 YES, S3 YES. FOR_ANU: owner Anu, no deadline; McCrory SI
   fetched when convenient.

## R0->R1 facts resolved under answer 1 (receipts in R1 artifacts)
- 1 M HClO4 Pd cluster (OA, +10 mA): 18 records; 0.1 M HClO4 Pd: 121; any HClO4 Pd: 310
  (harvest/pd_hclo4_clusters.json). The Peng ref-40 pairing sits in the 1 M HClO4 = 18 set.
- MPS/ESAMP iR-compensation practice for CP: NONE found. ESAMP Sci Data paper (PMC10079965)
  has no iR/ohmic/compensation mention; 0 MPS process_detail params carry an iR/ohmic/
  resistance-compensation field. Therefore MPS CP overpotential = ir_correction UNSTATED, and
  path (a) runs as a VETO census (CR3 condition_unstated) as anticipated.
- Lila Methods state (quotable/hashable, their paper 2609.30133 Supporting Methods): "All
  measurements were carried out in 1 M H2SO4 (pH 0.3) at room temperature"; "10 min
  chronopotentiometric (CP) hold at 10 mA cm-2"; "Electrochemical surface area (ECSA)
  determination and iR correction were not [applied]" (Lila ir_correction = 0, stated); and the
  stated 13 mV floor originates here: "five bare Pt/Si substrates measured at 10 mA cm-2 ...
  variation of +/-13 mV".
