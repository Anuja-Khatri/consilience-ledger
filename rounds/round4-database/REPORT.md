# Round 4: database QC, verdict distribution, guardrail receipts

This round runs the comparability engine over a large real materials database and reports
what it finds. It is a quality-control pass on a public dataset, not a discovery. Numbers are
ported from operator-v4 (git HEAD 5a1028e); each carries its n here and in NUMBERS_LOCK.json,
compliance_rerun.json, and redteam_report.json in this folder.

## What was ingested
From the Materials Provenance Store (MPS, CaltechDATA hjfx4-a8r81, CC BY 4.0) we ingested
140,708 acidic-OER chronopotentiometry cards (n = 140,708). MPS data bytes are not committed;
only the derived counts and receipts are. The licence is recorded first.

## The committed verdict distribution (test half, C-003 criterion)
On the test half, every comparable pair receives one verdict. The full committed distribution:

| verdict | count |
|---|---|
| not comparable | 74,569 |
| within floor | 80,144 |
| replicate inconsistency | 0 |
| fork | 0 |
| suspect transcription | 16,613 |

The cross-source fork count is 0 because MPS is one dataset and one pipeline, so no
cross-source pair exists to compare. This is reported as a structural zero, not as a search
that found nothing.

## The replicate check is false-discovery controlled and null calibrated
Disagreements are called against an empirical replicate-difference null with
Benjamini-Hochberg control, not a fixed floor. Under the null with nothing planted, the
false-positive rate is 0.000 (n = 1,228 test pairs, at q = 0.05). Clearly planted forks and
suspects are recovered at precision and recall of 1.00 and 1.00 (n = 33 planted positives on
the test half). The test controls false discoveries, which a floor cannot.

## Guardrail receipts
The typed lab-gate was attacked and defended 523 of 523 attempts with 0 steered, scored
against an independent vendored oracle. The comparability judge was attacked and defended 20
of 20, with 0 steered (receipt: redteam_report.json). The loop demonstration ran only on a
labelled synthetic fork: OERSIM returned an overpotential of 0.3610 V (n = 1, SIM, a
demonstration on a synthetic fork, not a discovery), and the whole chain is byte-reproducible.
The deterministic pipeline is byte-stable and the suite is green: 117 tests pass with
byte-stable reproduce.

## The compliance finding (credited to MPS, not an authors' error)
Converting each measurement to the RHE frame and comparing to each row's own recorded
compliance limit, 5,131 of 70,152 test-half rows carry a result from a measurement whose
potential exceeded its OWN recorded compliance limit by more than 0.5 V. A further 920 rows
are nonphysical (overpotential at or below zero). This check is possible only because MPS
records the compliance limit on all 70,152 of 70,152 test-half rows. It is a quality-control
observation about individual measurements running past their recorded compliance, credited to
MPS for recording the limits; it is not an error by the authors, and nothing here is said to
be shown about any catalyst.
