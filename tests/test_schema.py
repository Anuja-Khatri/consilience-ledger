"""Claim card v2 schema: parse failures fail closed; JSON Schema is generated."""

import json
import os

import pytest
from pydantic import ValidationError

from labext.schema import ClaimCard, Conditions, Quantity

_SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schema")


def test_performance_value_requires_quantity_and_axis():
    with pytest.raises(ValidationError):
        ClaimCard(
            claim_id="X", claim_kind="performance_value", commitment_direction="asserts",
            causal_direction="independent", physical_scale="molecular",
            measurability="measurable_now", subject="s", relation="has_overpotential",
            object="o", source_sentence="s", source_document="d", provenance_hash="h",
            # no quantity, no axis
        )


def test_conditions_forbid_extra_keys():
    with pytest.raises(ValidationError):
        Conditions(not_a_real_condition="x")


def test_conditions_default_all_unstated():
    c = Conditions()
    d = c.model_dump()
    assert all(d[k] == "unstated" for k in d)


def test_quantity_enum_validated():
    with pytest.raises(ValidationError):
        Quantity(value=1.0, unit="V", bound="sideways")


def test_json_schemas_exist_and_parse():
    for fname in ["claim_card_v2.json", "conditions.json", "quantity.json",
                  "verdict_record.json", "defect.json", "comparability_rules.json"]:
        path = os.path.join(_SCHEMA_DIR, fname)
        assert os.path.exists(path), f"missing {fname} (run python -m labext.gen_schemas)"
        with open(path) as fh:
            schema = json.load(fh)
        assert "properties" in schema or "$defs" in schema


def test_claim_card_schema_has_conditions_and_quantity():
    schema = ClaimCard.model_json_schema()
    assert "conditions" in schema["properties"]
    assert "quantity" in schema["properties"]
    assert "axis" in schema["properties"]
