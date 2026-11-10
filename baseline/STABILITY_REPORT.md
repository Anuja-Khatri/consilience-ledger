# Materials extraction-stability (fresh, Phase 7)

Model claude-sonnet-5, test-retest K=3 on identical passages (20 passages).

- stability = **0.423** (n = 52 distinct claims)
- stable (recurs in >= 2 of 3 runs): 22

Clustering: a claim is (normalised subject, rounded value, normalised unit). The axis label is excluded from the key: the model relabels the observable run-to-run (time_to_threshold vs duration_below) even when the subject and number are identical, so keying on the axis string would report labeling noise as instability. The (subject, value) of an extracted numeric claim is highly reproducible; the observable LABEL is not.

This is the materials number, reported fresh with its n. It is NOT the consciousness-domain 0.25 (that is a different domain and metric, cited separately with its own n=88).
Caveat: temperature default (API rejects temperature 0 for this model family).
