"""Synthetic pairs produce condition_mismatch, condition_unstated, axis_mismatch,
and a true fork (Phase 1 acceptance)."""

from labext.comparability import evaluate_comparability
from labext.judge import compare_pair
from labext.schema import Conditions
from tests.factories import FULL_CONDITIONS, perf_card, stability_card


def _defect_types(record):
    return {d["defect_type"] for d in record["defects"]}


def test_true_fork():
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.40)  # 100 mV apart, well above the 13 mV floor
    rec = compare_pair(a, b)
    assert rec["kind"] == "fork"
    assert rec["outcome"] == "fork"
    assert rec["margin"] > rec["floor_applied"]
    # both source sentences present for side-by-side rendering
    assert rec["claim_a_sentence"] and rec["claim_b_sentence"]


def test_within_floor_is_not_a_fork():
    a = perf_card("A", 0.300)
    b = perf_card("B", 0.305)  # 5 mV apart, below the 13 mV floor
    rec = compare_pair(a, b)
    assert rec["kind"] == "agreement"
    assert rec["outcome"] == "within_floor"


def test_condition_mismatch_on_current_density():
    cond_b = dict(FULL_CONDITIONS)
    cond_b["current_density"] = {"value": 20.0, "unit": "mA/cm^2", "normalization": "geometric"}
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.40, conditions=cond_b)
    rec = compare_pair(a, b)
    assert rec["kind"] == "rejection"
    assert "condition_mismatch" in _defect_types(rec)
    assert any(d["target"] == "CR2" for d in rec["defects"])


def test_condition_mismatch_on_normalization():
    # same magnitude but ECSA vs geometric are not comparable (CC-06)
    cond_b = dict(FULL_CONDITIONS)
    cond_b["current_density"] = {"value": 10.0, "unit": "mA/cm^2", "normalization": "ecsa"}
    rec = compare_pair(perf_card("A", 0.30), perf_card("B", 0.40, conditions=cond_b))
    assert rec["kind"] == "rejection"
    assert any(d["target"] == "CR2" for d in rec["defects"])


def test_condition_unstated_temperature():
    cond_b = dict(FULL_CONDITIONS)
    del cond_b["temperature"]  # leave temperature unstated on B
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.40, conditions=cond_b)
    rec = compare_pair(a, b)
    assert rec["kind"] == "rejection"
    assert "condition_unstated" in _defect_types(rec)
    assert any(d["target"] == "temperature" for d in rec["defects"])


def test_axis_mismatch():
    a = perf_card("A", 0.30)  # overpotential_at_current_density
    b = stability_card("B", 100.0)  # hours_to_threshold
    rec = compare_pair(a, b)
    assert rec["kind"] == "rejection"
    assert rec["outcome"] == "axis_mismatch"
    assert "axis_mismatch" in _defect_types(rec)


def test_room_temperature_vs_number_is_mismatch():
    # CC-12: room_temperature never equals a stated number
    cond_a = dict(FULL_CONDITIONS)
    cond_a["temperature"] = "room_temperature"
    rec = compare_pair(perf_card("A", 0.30, conditions=cond_a), perf_card("B", 0.40))
    assert rec["kind"] == "rejection"
    assert any(d["target"] == "CR3" for d in rec["defects"])


def test_multiple_defects_collected():
    cond_b = dict(FULL_CONDITIONS)
    cond_b["current_density"] = {"value": 20.0, "unit": "mA/cm^2", "normalization": "geometric"}
    del cond_b["ir_correction"]
    defects = evaluate_comparability(Conditions(**FULL_CONDITIONS), Conditions(**cond_b))
    types = {d.defect_type.value for d in defects}
    assert "condition_mismatch" in types  # CR2
    assert "condition_unstated" in types  # ir_correction
