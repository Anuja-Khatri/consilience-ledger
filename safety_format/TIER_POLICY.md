# TIER POLICY (draft, D13)

Draft wording. Anu words the final version at Checkpoint 2.

## Scope
This safety format ships with public-standard EHS content only. Dual-use content is
absent by permanent policy. Content curation is the job of domain scientists. The format
is a container and a compiler; it does not supply hazardous knowledge and never will.

## What is in scope (the benign allowlist, CC-31)
- Instrument protection bounds (for example, a furnace temperature ceiling, a
  potentiostat compliance limit).
- Consumables budgets (for example, acid volume per run).
- Standard laboratory incompatible-chemical classes as listed in widely published
  general safety references (for example, keep strong oxidizers away from organic
  solvents).

## What is permanently out of scope
Anything about synthesis routes to harmful agents. Anything that would function as a
recipe for a weapon, a toxin, or a controlled material. If any doubt exists about an
entry, it is excluded. A grep-able dual-use denylist (`safety_format/policy.py`) is
checked against the seed content by an automated test; the seed must contain none of
those tokens.

## Grades (the ladder)
Every rule carries a grade and a source. The ladder follows the hiring ladder in the
field: established, plausible, weakly supported. The grade is reported on every screen
receipt so a reader can see how strongly a block is backed and by what source. A grade
is a statement about evidence, not about severity.

## No text channel
A compiled screen reads only a typed plan fingerprint. Free text in a plan is
quarantined at the boundary and never reaches the screen, so no prose can talk its way
past a safety rule.
