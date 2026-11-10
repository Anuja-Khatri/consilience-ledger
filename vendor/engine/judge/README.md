# The Deterministic Judge

This directory contains the judge code: the deterministic layer that matches, grades, and assesses testability. No model touches this code's output. Same inputs, same output, content hash verifiable.

## Components

- `schema/` — JSON schemas for typed claim cards, correspondences, rejections, and instrument entries
- `matching/` — VF2 subgraph isomorphism and maximum common subgraph with typed edge constraints
- `grading/` — Four-rung grading ladder with ceiling statements
- `equivocation/` — Lexical ablation test (strip shared terms, check structural survival)
- `testability/` — Versioned instrument capability map lookup
- `hash/` — Content hash verification (run twice, compare hashes)

## What is included

The mechanism code: how matching, grading, equivocation testing, and testability checking work. These implement human-specified rules as deterministic functions.

## What is NOT included

The authored assets: ontology entries (relation types, claim kinds), calibration set (the fakes), instrument capability map data (specific instruments and scales), and extraction prompts. These are the moat. The mechanism is open. The data the mechanism operates on is not published.

## Running the determinism demo

```bash
cd ../examples/determinism-demo
python run_demo.py
```

Run it twice. Compare the hashes. They match.
