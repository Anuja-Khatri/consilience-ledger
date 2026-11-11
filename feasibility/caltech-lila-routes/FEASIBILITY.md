# FEASIBILITY - three data-route checks against the fixed Section 5 pass rules

Research only. No pipeline changes, no model API calls, no verdicts, nothing
pushed. Pass rules are taken verbatim from
`../consilience-for-lila-data-routes-and-next-move.md` §5 and were not changed.
A borderline number is a FAIL. Every count below carries its n.

## Plain-words summary (read this first)

1. **Check 1 (Caltech database vs Lila screening): FAIL.** Compositions match in
   plenty (7,115 Lila-row/DB-sample pairs at tol 0.05 in identical 1 M H2SO4),
   but **0** pairs can carry the three required facts with strong linkage. NOTE:
   the completed Part A (see "CHECK 1, COMPLETED" below) supersedes the first
   pass's reason - strong linkage IS available (each plate's CaltechDATA record
   declares `IsDocumentedBy` a publication), but that publication, the records,
   and the data all fail to state electrode area, iR status, or measurement
   temperature. Still FAIL (0 < 20).
2. **Check 2 (round-robin, Tesch 2023): central values YES, spread NOT met → the
   §5 spread condition FAILS.** A central value is readable for 9-11 labs, but the
   per-lab error bars at 10 mA cm-2 sit BELOW the raster resolution (marker ≈ 12 mV
   ≈ the bars), so a per-lab spread is NOT readable for ≥5 labs. The first pass
   over-claimed this; see "CORRECTION - Check 2 spread" below and CORRECTIONS.md.
3. **Check 3 (McCrory tables): FAIL.** Of 57 approved claim cards, **0** state
   all required conditions (temperature in 5, protocol tier in 0), so the count
   of McCrory-material claims with every condition stated is 0 (need ≥5).
4. Surprising and load-bearing: the database's "missing" concentration is
   actually recorded (process params: "1.0 M sulfuric acid"); what is truly
   missing is electrode area (0.0), temperature, iR status, and any link to a
   paper.
5. Net: all three checks fail their §5 rule as written. Route 2 is the closest - it
   delivers readable per-lab central values (the inter-lab spread the paper reports),
   but NOT a readable per-lab spread for ≥5 labs, so its §5 condition is not met.

---

## CHECK 1 - Caltech database (mps) versus Lila's screening data → **FAIL**

### 1a. Lila side - screening measurement conditions (verbatim, from Methods)
Source: `corpus_in/text/2609.30133.txt` (Lila paper 2609.30133), lines 180–182
and 253–254, 282–284.

- Electrolyte identity + concentration, current density, hold duration:
  > "OER screening is performed in 1 M H2SO4 in a custom-built scanning
  > electrochemical cell (SEC). Activity is taken as the overpotential at 10
  > mA cm-2 after 10 min."
- iR correction - no standalone sentence names the screening measurement's iR
  status. The nearest verbatim statements, about the lead-catalyst CP hold and
  the long-term test:
  > "During the initial 10 mA cm-2 hold, InMnPdOx held a stable overpotential of
  > 0.45 V (not iR-corrected) ..."
  > "(E) Long-term testing at 10 mA cm-2 after iR correction ... Non iR-corrected
  > data can be found in Fig. S2."
- Temperature: **not stated** anywhere in the retrieved main text for the
  screening measurement.
- Lila screening dataset: `oer_exp_data.csv`, **1,125** rows with valid
  composition; field `overpotential_cp1_600s_mean` = overpotential at 10 min
  (600 s), consistent with the quoted protocol.

### 1b. Database side - the acid-CP overpotential rows (mps adapter's selection)
Selection mirrors `engine/adapters/mps.py`: `r0survey.acid_cp_fom`, `eta_v_ave`
not null, electrolyte in {H2SO4(aq), KH2PO4/K2HPO4(aq)}, comp a json object.
SQL in `feasibility/sql/`.

- **Electrolyte identity × concentration × pH** (concentration and
  solution_description come from `process_detail.parameters`, which the FOM
  view does not expose; row counts after the sp→process join, which fans out):
  - H2SO4(aq), concentration `1` = **"1.0 M sulfuric acid"**, pH 0 - the subset
    comparable to Lila. (This directly contradicts the premise that acid
    strength is unrecorded; see Surprises.)
  - H2SO4(aq) also at 0.35 / 0.6 / 0.1 / 1.5 = "0.1 M sulfuric acid + sodium
    sulfate" mixtures (pH 1–1.4) and "1.0 M sulfuric acid + 0.5 M sodium
    sulfate".
  - KH2PO4/K2HPO4(aq) phosphate buffer, concentration 0.39/0.3/0.1/0.05,
    pH ≈ 2.24–2.92.
- **Distinct H2SO4 1.0 M samples with valid composition: 69,273** (the matchable
  pool). From the FOM selection overall there are ≈99,000 H2SO4 CP rows and
  ≈41,600 phosphate CP rows.
- **Rows per element system:** within the H2SO4 1.0 M pool, **87** distinct
  element systems (database) vs **54** (Lila). Only **6** element sets are
  identical on both sides (see 1c).
- **Anneal temperature recorded?** YES, but not in the FOM view: each sample
  links through `sample_process → process → process_detail` (type `anneal`) to a
  recipe with `max_temperature` (e.g. 350, 450, 500 C) and a `plate_id`. All
  1,881 matched samples (1c) carry an anneal temperature.
- **Fields that link a row to a plate / run / campaign / publication:**
  `sample → collection__sample → collection`, where `collection.label` is the
  plate number and `collection.doi` is a **per-plate CaltechDATA data DOI**
  (`10.25989/...`). There is **no publication DOI anywhere**: every one of the
  3,612 collections is type `JCAP_plate` with a CaltechDATA DOI, and
  `jcap_experiment.doi` is empty. This is decisive for 1d/1e.

### 1c. Composition matching (cation fractions, O excluded, renormalised to 1)
Match = identical element set AND every element fraction within tol t.
Restricted to identical electrolyte identity (H2SO4) AND identical concentration
(1.0 M). Lila n = 1,125 rows; database n = 69,273 samples.

| tol t | Lila rows with ≥1 DB match | total pairs | distinct DB samples |
|------:|---------------------------:|------------:|--------------------:|
| 0.02  | 62 / 1125                  | 5,564       | 1,633               |
| 0.05  | 75 / 1125                  | 7,115       | 1,881               |
| 0.10  | 75 / 1125                  | 9,727       | 2,090               |

Shared element systems (identical set, both sides) and their pair counts at
t=0.05: Mn 4,065; Mn–Sb 1,514; Co–Mn 1,068; Fe 406; Co–Mn–Sn 32; Fe–Sb 30.
(Lila rows per system: Mn–Sb 40, Co–Mn 18, Fe–Sb 6, Mn 5, Co–Mn–Sn 4, Fe 2.)

**Anneal subset (information only, NOT part of the pass rule):** of the 7,115
pairs at t=0.05, 6,579 have an anneal temperature on both sides; **190** have the
two anneal temperatures equal within 50 C.

### 1d. Campaign attribution of the matched samples
The 1,881 matched samples (t=0.05) belong to **34 distinct CaltechDATA plates**
(labels 1472–2975), each with its own data DOI (`10.25989/...`). None of these
is a publication DOI. The Mn–Sb pairs sit in the plate block ≈1472–1713, which
is the chemistry of Zhou et al. 2018 (Mn–Sb–O rutile acid OER) - but that tie is
**element-system identity only**.

Per the rule, "If the only linkage is 'same element system', label the linkage
WEAK and do not count those pairs." The database provides no plate ids, sample
ids, dates, or provenance fields that appear in Zhou 2018 or Gregoire 2013, so
**every** matched pair's linkage to a published campaign is WEAK.

Retrieval of the two campaign papers through open routes:
- **Zhou et al. 2018** (ACS Catalysis, 10.1021/acscatal.8b02689): main text
  paywalled; CaltechAUTHORS exposes only the SI; LBNL mirror returned 403. The
  Methods sentences on area / iR / temperature could NOT be quoted from an open
  route → recorded in `FOR_ANU.md`.
- **Gregoire et al. 2013** (Rev. Sci. Instrum. 84, 024102): paywalled (AIP). It
  is an instrument paper; a fact from it would be an instrument default, which
  the rule excludes. → `FOR_ANU.md`.

Because no quoted, strongly-linked, campaign-specific facts could be attached to
any pair, the quotation step yields nothing countable regardless of whether the
papers are eventually obtained.

### 1e. Result
Pairs at t=0.05 with identical electrolyte identity + concentration AND all three
missing facts (electrode/contact area, iR-compensation, temperature) quoted from
the published paper for that campaign with STRONG linkage: **0**.

> Pass rule: ≥ 20 → PASS, else FAIL. **0 < 20 → FAIL.**

> SUPERSEDED IN PART: see "CHECK 1, COMPLETED" below. Strong linkage to a
> publication IS available through the CaltechDATA DOI records' `IsDocumentedBy`
> provenance field (not merely same-element-system). The result is unchanged
> (0 < 20 → FAIL) because the linked publication states none of the three facts.
> The paragraph immediately below describes the first-pass reasoning (the mps
> relational tables carry no publication DOI); the DOI *records*, resolved via
> DataCite, do.

The failure is structural, not a matter of effort: the database carries no field
that links a sample to a publication, so strong linkage is impossible from the
data as held, and the three facts (area recorded as 0.0; temperature absent; iR
absent) are not in the database either.

**Simulator addressability (count only) - COMPOSITION coverage, NOT runnability.**
Of the matched compositions at t=0.05 there are **67 distinct compositions**;
**all 67** are element-addressable (their elements ⊆ the oer13_cps 13-element set
{Ca,Ce,Co,Cu,Fe,La,Mg,Mn,Ni,Sb,Sn,Ta,Zn}); **45** are grid-addressable (their
nearest 10-at.% grid point is an actual stored key in the oer13_cps library of
3,823 keys across 2 plates). The oer13_cps dataset is helao-async's (MIT), not
Lila's.

> CORRECTION (electrolyte). These compositions match in **acid** (both Lila and
> the matched MPS rows are 1.0 M H2SO4, pH ~0). The **oer13_cps simulator is
> ALKALINE**: its two plate keys (2750, 3851) were measured, for their CP3
> chronopotentiometry, in NaOH(aq), concentration 0.35, **solution_ph = 13**,
> "0.1 M sodium hydroxide + 0.25 M sodium sulfate" (n = 2,121 and 2,166 samples) -
> the helao electrolyte identifier **OER13**, listed separately from "1MH2SO4"
> and "1MNaOH" (see `feasibility/sql/10_oer13_electrolyte.sql`; helao
> `helao/core/models/electrolyte.py`). So **none of these acid matches can
> actually be RUN on this simulator** - an acid disagreement (pH ~0) cannot be
> settled on an alkaline OER13 replay (pH 13), a ~13-unit pH gap.
> Composition-addressability (67 / 45) is coverage of the composition axis ONLY;
> it does not imply the acid measurement is reproducible here.

---

## CHECK 2 - round-robin study (Tesch et al. 2023) → central values YES; **spread condition NOT met** (corrected)

### 2a. Retrieval and licence
Retrieved the full article via the Max Planck open repository (RSC page was
403-blocked). See PROVENANCE.md. Licence, verbatim:
> "This article is licensed under a Creative Commons Attribution 3.0 Unported
> Licence." - "© 2023 The Author(s). Published by the Royal Society of
> Chemistry."

### 2b. Protocol conditions (verbatim)
- Catalyst + loading:
  > "a commercial nickel–cobalt–oxide (Ni–Co–O) powder-based material of a
  > single batch was distributed among the project partners as a reference
  > catalyst."
  > "The benchmark electrodes were prepared by depositing 100 µg cm−2 Ni–Co–O
  > on a glassy carbon support with Nafion® as binder".
- Electrolyte: "1 M KOH" (Fig. 2 caption; Abstract: "in 1 M KOH"). Conditioning
  "100 mV s−1 in stagnant electrolyte".
- Rotation rate: "Scans are performed at a rotation speed of 1600 rpm."
- Current densities: "geometric current density of 10 mA cm−2 ... the potentials
  needed to drive geometric current densities of 2 mA cm−2 and 5 mA cm−2 are
  also included". Normalisation "with respect to the geometric area".
- iR compensation:
  > "To be able to compensate for the Ohmic drop, both activity and stability
  > measurement is preceded by a measurement of the open circuit potential and
  > electrochemical impedance spectroscopy at open circuit potential."
  (uncompensated resistance R_u is measured and reported; Fig. 3.)
- Stability: CP "the current is ramped up to 10 mA cm−2 (geometric area)" or CA
  at 1.8 V_RHE, 1600 rpm, "carried out for two hours".
- Temperature: **not stated** (the paper notes humidity/temperature as
  uncontrolled sources of variation but gives no controlled value).
- Number of labs: "measured by 11 project partners at different institutions";
  Fig. 3/4 captions: "11 different laboratories/experimenters".

### 2c. The per-lab figures at 10 mA cm-2
Both figures show the 10 mA cm−2 result; both are **raster** images embedded in
the PDF (300 ppi, ~982 px wide - values are NOT vector-recoverable; pixel
reading only). Y-axis minor ticks = 5 mV; practical reading precision ≈ **5 mV**.

- **Fig. 4** (KPIs for 2, 5, 10 mA cm−2): one column of individual diamond
  markers color-coded by lab, plus a box plot (median red line, star = mean,
  whiskers = min/max within 1.5·IQR). At 10 mA cm−2 there are ~18–20 points
  across ~10 distinguishable colours; markers overlap, so per-lab assignment
  here is error-prone.
- **Fig. 5** (the clean per-lab figure): "Average KPI obtained by the individual
  experimenters (open symbols ...). The error bars indicate the full range of
  the potentials ... across all measurements performed by an individual
  experimenter. In case of the half filled symbols only a single data point was
  provided." At 10 mA cm−2, counting symbols:

| per-lab readout at 10 mA cm-2 (Fig. 5) | count | notes |
|---|---|---|
| central value (one coloured symbol per lab) | ~11 | colours well separated in Fig. 5 |
| spread readable (open symbol with error bar = full range) | ~8 | these labs provided >1 measurement |
| spread NOT readable (filled/half-filled = single data point) | ~3 | e.g. black, dark-green, red |

Text corroboration: "For the data obtained by a single experimenter, in all
except one case, the spread is below 15 mV at 10 mA cm−2."

### 2d. Per-lab values in a table or data file?
**No per-lab numeric table in the main text.** Table 1 reports only the aggregate
box-plot statistics (min, 25th/median/75th percentiles, max, mean, IQR, full
range) at 2/5/10 mA cm−2 - not per lab. Per-lab values exist only as the plotted
points in Fig. 3/4/5. The ESI (same DOI) was not retrievable (RSC 403) and is
listed in FOR_ANU.md; the main-text figures already decide the check.

### 2e. Result - CORRECTED
Central value readable for ≥ 8 of 11 labs: **YES** (9 machine-read reliably; grey
and black are not colour-separable from chart furniture). Per-lab spread readable
for ≥ 5 labs: **NO**.

> Pass rule: central value ≥ 8 labs AND spread ≥ 5 labs. The spread half is **NOT
> MET**, so the check does **not** pass as its §5 rule requires.

#### CORRECTION - Check 2 spread
The first pass claimed "spread readable for ~8 labs" by eye. The build-side
machine read (Part B; `engine/round_robin.py`, Fig. 5 @ 10 mA cm⁻² extracted to a
PPM at 300 ppi) shows this was wrong: the marker diamond is ≈ 12 mV tall and the
per-lab error bars are at or below that, and similar colours cross-contaminate, so
**no per-lab error bar is reliably readable** (0 labs, not ≥ 5). The only lab with
an unambiguously large bar (grey) is itself not colour-separable. The paper's own
text is consistent - the single-experimenter spread is "below 15 mV at 10 mA
cm⁻²", i.e. at or under the figure's reading resolution. So Check 2 delivers the
central values but **does not meet the spread-readable-for-≥5 condition**. Recorded
here and in `../CORRECTIONS.md`.

---

## CHECK 3 - McCrory benchmark tables → **FAIL**

### 3a. Retrieval
The ACS SI URLs returned HTTP 403, but both Supporting Information PDFs were then
retrieved through an official open route - **CaltechAUTHORS** (see PROVENANCE).
Check 3 is therefore RUN (not NOT RUN; see OPEN_QUESTIONS #6). The two main texts
(which carry the iR-compensation sentence) remain paywalled → FOR_ANU.md.

### 3b. Catalysts and stated conditions
- **McCrory 2013** (SI, open) - 10 OER catalysts benchmarked: IrOx, CoOx (Co-a),
  CoOx-b (CoPi), CoFeOx, NiOx, NiCeOx, NiCoOx, NiCuOx, NiFeOx, NiLaOx.
  Conditions, verbatim (Fig. S16/S17 captions):
  > "A representative rotating disk voltammogram of the oxygen evolution reaction
  > at an electrodeposited CoOx-(a) catalyst at 0.01 V/s scan rate and 1600 rpm
  > in 1 M NaOH."
  > "The horizontal dashed line at 10 mA cm−2 per geometric area is the current
  > density expected for a 10% efficient solar water-splitting device."
  > "The inset is a representative 2-h controlled-current electrolysis at 10 mA
  > cm−2 per geometric area."
- **McCrory 2015** (SI, open) - "26 electrocatalysts for the oxygen evolution
  reaction (OER)". Table S2 (electrodeposited OER) lists: Co-(b), Co/B, Co/P-(a),
  Co/P-(b), CoFe, Cu, Fe-(b), FeMn, Ni-(b), Ni/B, NiCe, NiCo-(b), NiCo-(c), NiCr,
  NiCu, NiFe-(b), NiFe-(c), NiLa, NiMoFe(b), NiSn(b), NiZn(b), Ru-(a) - plus IrOx
  and further reference oxides to total 26. Materials list names the electrolytes
  used: "98% sulfuric acid (H2SO4)", "sodium hydroxide (NaOH)", "potassium
  hydroxide (KOH)". Current-density basis is 10 mA cm−2 per geometric area;
  rotation 1600 rpm; stability 2 h; scan rate 0.01 V/s (same protocol as 2013).
  (iR-compensation statement is in the main text, not the SI.)

So McCrory's OER set is Ru-based (Ru-(a)) + Ir-based (IrOx) + earth-abundant Co/
Ni/Fe/Cu/Mn oxides.

### 3c. Approved claim cards on McCrory materials with every condition stated
Pool: **57 approved claim cards** = 34 in `lab-extension/ledger/claims.json`
(all from the Lila paper 2609.30133) + 23 in ledger-v2 approved folders
(`r2_out_k40/approved` 17, `r2_out/approved` 6). Material names canonicalised.

A card is "condition-complete" iff it states ALL of: electrolyte identity +
concentration; current density with basis; iR fraction; temperature; protocol
tier. Per-field tallies across the 57 cards:

| field stated | count / 57 |
|---|---|
| current density + basis | 38 |
| electrolyte identity + concentration | 22 |
| iR fraction (ir_correction) | 14 |
| temperature | 5 |
| protocol tier | 0 |
| **ALL five together** | **0** |

Material overlap with McCrory's catalysts does exist among the approved cards
(RuO2 / RuOx ↔ McCrory Ru-(a); IrOx / IrO2 ↔ McCrory IrOx - a handful of cards),
but **none** of those cards - indeed none of the 57 - states every condition.
`protocol_tier` is "unstated" on all 57, and temperature on all but 5, so the
intersection (McCrory-material ∧ condition-complete) is 0.

### 3d. Result
Approved claims on a McCrory material with every condition stated: **0**.

> Pass rule: ≥ 5 → PASS, else FAIL. **0 < 5 → FAIL.**

---

## Surprises that bear on the data routes

1. **The database's "missing" acid strength is not missing.** The headline
   premise for Route 1 (area, iR, temperature unrecorded per row) is only
   two-thirds right. Electrolyte CONCENTRATION *is* recorded - in
   `process_detail.parameters` the H2SO4 rows read `concentration = 1`,
   `solution_description = "1.0 M sulfuric acid"`, which matches Lila's 1 M
   H2SO4 exactly. Also recorded there: `current_abs` (30/100/300 µA),
   `acquisition_time`, `solution_ph`, `ref_electrode_type` (uAg/AgCl). The mps
   adapter emits all of these as UNSTATED only because its FOM view drops them;
   the base tables have them. What is genuinely absent is `measurement_area`
   (0.0 for the sulfuric rows → current density not computable), any temperature
   field, and any iR field.

2. **The database hold is not a 10-minute hold.** Lila's screening overpotential
   is "after 10 min" (600 s). The database's acid CP techniques are short:
   `acquisition_time` is overwhelmingly 15 s (CP3) or 10–20 s, with only a
   handful of rows at 600 s. So even where compositions and electrolyte match,
   the measurement protocol (hold duration) does not - a comparability gap the
   pass rule does not test but which matters for any later build.

3. **There is no paper link anywhere in the database.** Every DOI in mps is a
   per-plate CaltechDATA *data* DOI; `jcap_experiment.doi` is empty. This is the
   single fact that kills Route 1 under the stated rule: campaign-to-publication
   attribution can only ever be "same element system" = WEAK.

4. **Composition overlap is real and sizeable** (7,115 pairs, 1 M H2SO4, tol
   0.05), concentrated in Mn, Mn–Sb and Co–Mn - exactly Lila's earth-abundant
   comparators, and exactly the chemistry of the Caltech Mn–Sb–O acid-OER work.
   The route fails on provenance and stated conditions, not on chemistry.

5. **The ledger cannot currently feed Check 3 (or any condition-matched fork).**
   Across 57 approved cards, `protocol_tier` is never stated and temperature is
   stated 5 times. This is the same scarcity Route 4 describes, now measured on
   the approved set: condition-complete yield is effectively zero.

6. **Only Route 2 is live.** Of the three checks, the round-robin is the one with
   a readable known-answer test (central values for ~11 labs, spreads for ~8, at
   ~5 mV off raster figures). It is alkaline Ni–Co oxide, not Lila's chemistry -
   a demonstration of the detector, not a result in Lila's space.

---

## CHECK 1, COMPLETED - DOI resolution and strong-linkage recount (Part A)

The first pass concluded the only tie from a matched sample to a published
campaign was "same element system" = WEAK. That was incomplete: the CaltechDATA
DOI records carry a provenance field that supplies strong linkage. Resolving it
changes the *reason* for the result but not the result.

### A1. Plates behind the 7,115 matched pairs (n = 34 plates)
All 7,115 pairs (t=0.05, identical electrolyte identity + 1.0 M concentration)
attribute to **34 distinct CaltechDATA plates**, each with its own data DOI.
Full table: `feasibility/A1_matched_plates.csv` (plate, DOI, matched samples,
matched pairs, element systems). Largest: plate 1486 (DOI 10.25989/w228-8r45,
255 pairs); the pairs span element systems Mn, Mn–Sb, Co–Mn, Co–Mn–Sn, Fe,
Fe–Sb, consistent with the Mn-rich acid-OER chemistry.

### A2. DOI resolution (DataCite API, official open route, retrieved 2026-11-11)
Each DOI resolved through `https://api.datacite.org/dois/<doi>`; the 34 raw
records are saved in `feasibility/caltechdata/`, summarised in
`feasibility/A2_caltechdata_summary.csv`. For every record:
- **Rights:** `cc-by-sa-4.0` (all 34).
- **Creators:** Soedarmadji, Gregoire (+ contributors Guevarra, Haber, Jones,
  Kan, Lai, …), Caltech JCAP High Throughput Experimentation Project.
- **Title** encodes synthesis provenance tied to the plate id, e.g.:
  > "Materials Experiment and Analysis Database: Material library with
  > Mn,Sn,Sb,Fe,Co deposited by INKJET on 2014-03-13 from Plate 00014869
  > annealed at 350.0C to add O on 2014-03-14"
  (anneal temperature and deposition dates are in the record; these are
  synthesis conditions, NOT the three measurement facts the rule requires).
- **IsPartOf:** `10.25989/es8t-kswe` ("Materials Experiment and Analysis
  Database", the parent dataset) - all 34.
- **IsDocumentedBy (the strong link):** `10.1038/s41524-019-0216-x` - all 34.

### A3. Strong linkage and the three facts
`IsDocumentedBy` is a database provenance field that ties each plate id to a
specific publication, so it meets the rule's strong-linkage bar (not "same
element system"). The publication is:

> Soedarmadji, Stein, Suram, Guevarra, Gregoire, "Tracking materials science
> data lineage to manage millions of materials experiments and analyses," *npj
> Computational Materials*, 2019, **5**, 79. DOI 10.1038/s41524-019-0216-x.
> Licence (verbatim): "Open Access This article is licensed under a Creative
> Commons Attribution 4.0 International License…" "© The Author(s) 2019".
> Retrieved 2026-11-11 from the Nature open-access page (CC BY).

Read in full. It is a data-lineage / database-infrastructure paper. On the
measurement it says only, verbatim:
> "Photoelectrochemical performance is assessed via a series of specialized
> scanning droplet cells.44,45"

It states **none** of the three required facts:
- electrode / contact area - **NOT stated** (no area anywhere; refs 44,45 are
  the instrument papers, which the rule excludes as instrument defaults);
- iR-compensation - **NOT stated** (the words iR / ohmic / compensation do not
  appear);
- measurement temperature - **NOT stated** (the only "temperature" is an
  example of a data-file field, not the OER measurement).

The DOI'd records themselves (the other route the rule allows) supply only the
anneal temperature and synthesis dates - not area, iR, or measurement
temperature. And the underlying MEAD data for these plates carries
`measurement_area = 0.0`, no temperature field, and no iR field (Check 1b). So
under both permitted routes - the linked publication and the DOI'd record - the
three facts are unavailable for every plate.

Per-campaign (all 34 plates identical on this point):

| fact | found? | where it would be / why not |
|---|---|---|
| electrode / contact area | NO | not in record; linked paper gives none; MEAD stores 0.0 |
| iR-compensated? | NO | not in record; linked paper never mentions iR |
| temperature (measurement) | NO | not in record; linked paper gives none; no DB field |
| (anneal temperature) | yes | in the DOI title (e.g. 350.0C) - but excluded by the rule |

### A4. Recount under the unchanged Section 5 rule
Pairs at t=0.05, each element within 0.05, identical electrolyte identity and
concentration (1.0 M H2SO4), with all three facts quoted with STRONG linkage:
**0**.

> Pass rule: ≥ 20 → PASS, else FAIL. **0 < 20 → FAIL.**

What changed from the first pass: strong linkage is **available** for all 7,115
pairs (plate id → CaltechDATA record → the documenting publication, via the
`IsDocumentedBy` field - CC BY-SA 4.0 records, CC BY 4.0 paper, both retrieved
by open routes). The check still FAILS, now for a sharper reason: the single
publication that the records declare as documenting these plates does not report
electrode area, iR status, or measurement temperature, and neither do the
records or the data. The missing facts are missing at the source, not merely
unlinked. No matched plate links to Zhou 2018 or Gregoire 2013, so conditions
quoted from those papers would not be strongly linked and cannot be counted.
