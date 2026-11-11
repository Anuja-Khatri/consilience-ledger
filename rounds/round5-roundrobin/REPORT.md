# Round 5: round-robin known-answer run, corrected headline

This round is a build-side known-answer test, not a discovery. It reads a published
inter-laboratory round-robin and asks whether the comparability engine recovers a spread the
paper itself already reported. Content is merged from operator-v4 RRR_REPORT.md and
CHECKPOINT_RR.md (git HEAD 5a1028e), em dashes purged; the machine-readable result is in
rr_tesch_result.json in this folder.

## The robust result (lead with this)
The durable finding is the inter-lab central-value range: 90.7 mV (n = 9), read from Fig. 5 of
Tesch et al., Energy Advances 2023, 2, 1823 (CC BY 3.0). The figure is a raster image, so 9 of
the 11 laboratories are machine-read (two similar colours are not separable from chart
furniture). This is a spread the paper itself reports. It is not a new finding, and no
laboratory is said to have erred. The catalyst is a single shared batch of alkaline
nickel-cobalt oxide under one written protocol, not Lila's chemistry.

## The fork finding, with its full qualifier
Running every laboratory pair through the hash-locked prereg gives:

0 to 4 forks at s = 15 mV. The paper reports one experimenter above 15 mV without naming which
or by how much (its own words: "in all except one case, the spread is below 15 mV at 10 mA per
cm2"). The 4 forks tolerate a single-lab spread of only 16.0 to 24.5 mV, and one laboratory
appears in 3 of the 4, so none survive if any single laboratory's spread reaches 30 mV. Across
the sweep the counts are 4 / 15 / 20 / 23 forks at s = 15 / 10 / 7.5 / 5 mV, over 36 testable
laboratory pairs. The spread threshold was chosen after seeing the data, because the per-lab
error bars sit at or below the raster reading resolution and are not machine-readable; the
sweep values are therefore not in the hash-locked prereg. The fork count is not robust; the
central range above is the durable result.

Before the real data, a null calibration (false-fork rate below q = 0.05) and a planted
recovery both passed (receipt: rr_tesch_result.json). The most significant fork is run through
the loop, which terminates at plan_only: the discriminating measurement is in 1 M KOH while the
public OERSIM electrolyte is OER13 (0.1 M NaOH plus 0.25 M Na2SO4, alkaline, pH 13), a different
electrolyte, so no run is faked.

## Correction history (reworded)
- C-004: the vendored OERSIM was mislabelled acidic; it is alkaline (OER13, pH 13). An acid
  disagreement cannot be settled on this simulator, and the round-robin fork in 1 M KOH is also
  a different electrolyte, so it stays plan_only.
- C-005: an earlier pass marked the per-lab spread condition as met; the machine read shows the
  per-lab error bars are at or below the raster resolution, so a per-lab spread is readable for
  0 laboratories and the spread condition is not met. The central values stand (9 machine-read).
  The sweep spread values were chosen after the figure was read and are not pre-registered.
- C-006: the forks at the headline setting are fragile to the per-lab spread assumption. Each
  fork breaks once one of its own laboratories exceeds roughly 16 to 26 mV, and a single
  genuinely noisy laboratory at 30 mV erases all of them.
- C-007: an earlier headline over-stated a fragile count of forks as if it were firm. The
  corrected, mandatory headline is 0 to 4 forks at s = 15 mV with the qualifier above, and the
  result to lead with is the robust inter-lab central range of 90.7 mV (n = 9). No computed
  number moved; only the presentation changed.
