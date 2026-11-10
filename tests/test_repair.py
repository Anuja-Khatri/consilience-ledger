"""Repair layer normalises real model output into the strict schema (Phase 2)."""

from labext.extraction.repair import repair_raw_card
from labext.schema import ClaimCard


def _raw(**over):
    base = {
        "claim_id": "EX1", "claim_kind": "performance", "commitment_direction": "asserts",
        "causal_direction": "weird", "physical_scale": "molecular",
        "measurability": "measurable_now", "measurable_with": "unstated",
        "subject": "IrO2", "relation": "has_overpotential", "object": "overpotential",
        "domain": "materials_oer", "source_sentence": "IrO2 shows 300 mV.",
        "source_document": "example", "provenance_hash": "ex1",
        "axis": "overpotential_at_current_density",
        "quantity": {"value": "300 mV", "unit": "", "uncertainty": None,
                     "uncertainty_kind": "none_stated", "bound": "lower_bound"},
        "conditions": {
            "electrolyte": {"identity": "H2SO4", "concentration": {"value": "0.5", "unit": "mol/L"}},
            "current_density": 10, "temperature": 25, "ir_correction": "yes",
            "duration": {"value": 1000, "unit": "h"},  # synonym for prior_operation_duration
        },
    }
    base.update(over)
    return base


def test_repair_makes_real_output_valid():
    card = ClaimCard.model_validate(repair_raw_card(_raw(), "2609.30133"))
    assert card.claim_kind.value == "performance_value"       # synonym mapped
    assert card.causal_direction.value == "independent"       # invalid -> default
    assert card.quantity.bound == "lower"                      # lower_bound -> lower
    assert card.quantity.value == 300.0 and card.quantity.unit == "mV"  # string+unit parsed
    assert card.source_document == "2609.30133"               # few-shot id overridden
    # bare-number conditions wrapped with canonical units; synonym key mapped
    assert card.conditions.current_density.value == 10.0
    assert card.conditions.temperature.value == 25.0
    assert card.conditions.ir_correction is True
    assert card.conditions.prior_operation_duration.value == 1000.0


def test_repair_drops_unknown_condition_keys():
    raw = _raw()
    raw["conditions"]["not_a_condition"] = 5
    card = ClaimCard.model_validate(repair_raw_card(raw, "p"))
    assert "not_a_condition" not in card.conditions.model_dump()


def test_repair_never_invents_unstated():
    raw = _raw()
    raw["conditions"] = {"electrolyte": "unstated"}
    card = ClaimCard.model_validate(repair_raw_card(raw, "p"))
    d = card.conditions.model_dump()
    assert d["current_density"] == "unstated" and d["ir_correction"] == "unstated"
