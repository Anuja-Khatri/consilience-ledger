# METHODS

The method, stage by stage. All code is deterministic; `make reproduce` asserts byte-stable hashes.
Numbers are not restated here - they live, each with its n, in `README.md` and `NUMBERS_LOCK.json`.

## Typed claims (S1–S2)
Each measurement becomes a `TypedClaimCard` (v3): identity + provenance, structural typing, a
`quantity` (value/unit/uncertainty), a per-domain `conditions` object where every field admits
`unstated`, a `source_id` (the provenance unit - dataset+pipeline or paper), and, for chemistry, the
row's recorded `instrument_potential_limit_rhe`. Structured corpora skip any model: one hash-locked
mapping per dataset. Data bytes are runtime-loaded, never committed; licences are recorded first.

## Comparability - default-deny (S3, part 1)
Two cards are comparable only if every rule whose field is required passes and no required field is
`unstated` on either side. Chemistry CR1–CR5 are page-sourced (electrolyte identity+concentration,
current density, iR fraction, temperature, protocol tier); biology BR1–BR5 are the matched-condition
analogues (EC, substrate, pH, temperature, organism). A missing required field yields
`condition_unstated:<field>`; a failed predicate yields `condition_mismatch:<rule id>`. A fork
additionally requires the SAME entity (composition, or enzyme-variant+substrate). **CR-ID** (within
one dataset, same technique+pipeline) treats conditions the shared documentation leaves unstated on
both sides as identical-by-protocol - identity of protocol, not equality of stated values; stated
values are never waived and cross-dataset pairs stay default-deny.

## Compliance / physical bound (S3, part 2) - C-003
The suspect/upper bound is the data's OWN recorded instrument compliance, not an eye-chosen ceiling: a
chemistry row is a compliance artefact when its RHE potential (η + 1.23 V) exceeds its recorded
`limit_potential_vref − reference_vrhe` by a compliance band. Rows with no recorded limit fall back to
a labelled η ceiling. η ≤ 0 is nonphysical. The experiment-abort criteria are a diagnostic cross-check
only (they are protocol branch points, so they over-flag). This replaced two earlier eye-chosen
ceilings (`CORRECTIONS.md` C-001, C-002, C-003).

## The replicate / fork decision (S3, part 3) - FDR, not a floor
The median floor is retired. Each dataset is split 50/50 by a fixed seed. On the calibration half we
build the empirical distribution of replicate differences from SAME-source same-entity pairs (a clean
noise null); a dataset with no same-source replicates uses a labelled `same_entity_fallback` whose
verdicts are reported `untestable`, never "0 forks". On the test half each comparable pair gets an
empirical one-sided p-value against the null, then Benjamini-Hochberg at q=0.05. A significant pair is
a `replicate_inconsistency` if same-source (QC) or a cross-source `fork` if different-source. Where
rows carry a reported uncertainty, cross-source pairs are instead tested by a z-test on log10 values
(same split, same q); no public kinetics corpus carries one, so those pairs are `untestable`.

## Validation (mandatory)
Null calibration: data generated from the empirical noise with nothing planted must be flagged at a
rate ≤ q - demonstrated in both domains. Planted recovery: clearly-planted forks and suspects are
recovered at full precision/recall on the test half. Both are run on every build.

## The loop (S4–S9)
For a fork on a measurable entity: S4 decidability vs the OERSIM capability profile (settleable vs
plan_only); S5 the 6b experiment card (a no-compile card is a valid terminal); S6 translation to a
typed helao plan; S7 the vendored lab-gate (PASS/BLOCK/ABSTAIN, no free-text channel); S8 the
in-process OERSIM replay; S9 writeback + a byte-reproducible trace audit. Every simulated outcome
carries the SIM label; the loop proposes an experiment on an existing entity and never invents a
material. It is demonstrated on a clearly-labelled SYNTHETIC fork only (no real fork cleared the bar).

## Red-team (eval-of-evaluators)
The typed gate is attacked with oracle-scored static attacks and no-text-channel injections; an attack
counts as steering only if the gate PASSes a plan the independent vendored oracle says is out-of-spec.
The judge is attacked by injecting adversarial text into its string fields and checking the verdict
content-hash is byte-identical.

## Preregistration + reproduction
Every rule, floor method, threshold, split seed, and the compliance criterion are preregistered and
hash-locked BEFORE the run that uses them (`engine/prereg/`, verified at run time). `make reproduce`
recomputes the pipeline twice and fails on any hash drift.

---
Ported from operator-v4 METHODS.md (git HEAD 5a1028e) for the public record; the round-robin and cross-field sections live with round 5 and are not duplicated here. Em dashes purged. Numbers live with their n in this round's REPORT.md, NUMBERS_LOCK.json, compliance_rerun.json, and redteam_report.json.
