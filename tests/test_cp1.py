"""Checkpoint 1 application: electrolyte/unit canonicalization and apply_review."""

import os

from labext.comparability import evaluate_comparability
from labext.extraction.apply_review import apply_review
from labext.judge import compare_pair
from labext.units import normalize_unit, to_canonical
from tests.factories import FULL_CONDITIONS, perf_card


def test_unit_aliases():
    assert normalize_unit("C") == "degC"
    assert normalize_unit("mA cm-2") == "mA/cm^2"
    assert to_canonical({"value": 65, "unit": "C"}, "temperature") == 65.0  # pint would read C as coulomb


def test_electrolyte_identity_canonical_equal():
    # H2SO4 and "sulfuric acid" are the same electrolyte (CR1 canonical list)
    cond_b = dict(FULL_CONDITIONS)
    cond_b["electrolyte"] = {"identity": "sulfuric acid", "concentration": {"value": 0.5, "unit": "mol/L"}}
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.30, conditions=cond_b)
    assert evaluate_comparability(a.conditions, b.conditions) == []  # comparable, not a string accident
    assert compare_pair(a, b)["kind"] == "agreement"


def test_apply_review_corrected_card(tmp_path):
    md = '''# Contested claim demo #007

## Source sentence

> X.

## Model A (m-a)

```json
{"claim_id":"EX1","claim_kind":"performance_value","commitment_direction":"asserts",
"causal_direction":"independent","physical_scale":"molecular","measurability":"measurable_now",
"measurable_with":"cp_chronopotentiometry","subject":"IrO2","relation":"has_overpotential",
"object":"overpotential","domain":"materials_oer","source_sentence":"X.","source_document":"example",
"provenance_hash":"ex1","axis":"overpotential_at_current_density",
"quantity":{"value":0.30,"unit":"V","uncertainty":null,"uncertainty_kind":"none_stated","bound":"exact"},
"conditions":{"electrolyte":"unstated","ph":"unstated","current_density":"unstated","temperature":"unstated",
"loading":"unstated","substrate":"unstated","protocol_tier":"unstated","prior_operation_duration":"unstated",
"anneal_temperature":"unstated","ir_correction":"unstated"}}
```

## Model B (m-b)

```json
(no card from this model)
```

## Verdict (Anu)

- [x] approve model A
- [ ] approve model B
- [ ] approve with corrections (write the corrected card below)
- [ ] reject

```json

```
'''
    d = tmp_path / "review"
    d.mkdir()
    (d / "demo__007.md").write_text(md)
    out = apply_review(str(d), str(tmp_path / "approved_cards.jsonl"))
    assert out["counts"]["approved"] == 1
    card = out["approved"][0]
    assert card["claim_id"] == "demo__007"          # BR1 id regenerated
    assert not card["provenance_hash"].startswith("ex")
    assert os.path.exists(out["out"])
