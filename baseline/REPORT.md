# LLM-judge baseline (Phase 6)

Model: claude-sonnet-5. Preregistered deterministic sample of 60 pairs (all forks + corroborations; first 40 condition-defect and first 20 axis-mismatch pairs by sorted pair_id). Cached.

## Agreement matrix (deterministic judge rows x model-call columns)

| judge \ model | agree | disagree | not_comparable | na |
|---|---|---|---|---|
| disagree | 0 | 0 | 0 | 0 |
| agree | 0 | 0 | 0 | 0 |
| not_comparable | 2 | 2 | 53 | 3 |

## Headline

Of 60 pairs the deterministic judge vetoed as NOT comparable, the model call made 4 comparisons the veto blocks (2 called a disagreement, 2 called an agreement); it recognised incomparability on the rest. The judge's conditions veto prevents exactly those comparisons: no prose talks its way past it. The model is capable but not exact; both labelings are reported; no pairs were cherry-picked (the sample rule is preregistered above).
