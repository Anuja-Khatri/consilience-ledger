# Corrections C-001 to C-003 (database round)

Reworded for the public record from operator-v4 CORRECTIONS.md (git HEAD 5a1028e). Per
consolidation rule 2, the superseded draft fork counts from the median-floor error are
described in words only; their digits are not printed. The corrected, locked numbers are
in REPORT.md and NUMBERS_LOCK.json, each with its n.

## C-001: the physical ceiling on suspect measurements was too tight
The first physical-bound rule flagged any overpotential outside 0 to 1.0 V as a suspect
transcription. An audit showed this mixed two populations: genuine artefacts (negative
overpotentials and extreme values) and real but poor catalysts with high overpotentials
near 1.0 V that were wrongly flagged. The values were confirmed to be in volts, so this was
a bound error, not a units error. The ceiling was raised so that a real poor catalyst is
not called an artefact.

## C-002: the ceiling was still too permissive
A follow-up audit enumerated every apparent replicate inconsistency under the raised
ceiling and found each one was a normal value paired with a lone compliance-rail value, not
a genuine disagreement. The dense real overpotential population ends well below the raised
ceiling. The ceiling was lowered again, after which no genuine replicate inconsistency
survived the false-discovery control. No real on-plate discrepancy remained to settle, so
the loop test stayed on a clearly labelled synthetic fork only.

## C-003: the eye-chosen ceiling is replaced by the data's own recorded compliance
Both earlier ceilings were read off the overpotential histogram by eye. C-003 replaces them
with an independent, per-row instrument criterion: a chemistry row is a compliance artefact
when its RHE potential exceeds its own recorded instrument compliance limit by more than
0.5 V. Overpotential at or below zero is nonphysical regardless. Rows with no recorded limit
fall back to the earlier labelled ceiling; on MPS every row carries a recorded limit, so the
fallback never fires.

Rerun on the MPS test half (70,152 cards, preregistered compliance criterion locked before
the run):

| route | rows flagged (test half) |
|---|---|
| recorded compliance limit exceeded by more than 0.5 V | 5,131 |
| nonphysical (overpotential at or below zero) | 920 |
| fallback ceiling (no recorded limit) | 0 (every MPS row carries a recorded limit) |

Verdict on the test half under C-003: not comparable 74,569, within floor 80,144, replicate
inconsistency 0, fork 0, suspect transcription 16,613. The headline null is unchanged: zero
genuine MPS replicate inconsistencies. The former artefacts are now excluded by each row's
own recorded compliance, not by an eye-chosen ceiling.

## Superseded numbers, do not quote (reworded per rule 2)
An earlier database pass used a median-floor fork rule that did not control false
discoveries and did not separate same-source replicate inconsistency from cross-source
forks. Under that retired rule, the pipeline reported large median-floor "fork" counts for
MPS and for the CatLog enzyme set. Those counts are superseded and are described here in
words only; their digits are not printed anywhere in this repo. The corrected findings are:
MPS is a single dataset and pipeline, so no cross-source pair exists and the cross-source
fork count is zero; the enzyme sets carry no per-row uncertainty and no same-source
replicate null, so their cross-source pairs are untestable, never "zero forks". The median
floor is retired for verdict purposes.
