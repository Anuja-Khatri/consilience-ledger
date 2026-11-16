"""Input hardening for the comparator and the units layer (WP1).

Each case here was found by probing the code: before this change it either returned
a confident wrong number, or let a meaningless comparison through. Every one must now
be refused with a named reason (fail closed), never coerced.
"""

import math

import pytest

from labext.comparability import evaluate_comparability
from labext.judge import compare_pair
from labext.schema import ClaimCard, Conditions, Quantity
from labext.units import UnitError, as_quantity, normalize_unit, to_canonical
from tests.factories import FULL_CONDITIONS, perf_card


# --------------------------------------------------------------------------- #
# String parsing: misread inputs must be refused with a named reason
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "text, reason",
    [
        ("1 200", "space_separated_digits"),       # was read as 1 * 200 = 200
        ("1 200 mA/cm^2", "space_separated_digits"),
        ("3,14", "ambiguous_separator"),           # was read as 314
        ("1,234 mL", "ambiguous_separator"),       # decimal or thousands comma: ambiguous
        ("5M", "ambiguous_scale_suffix"),          # was read as 5 molar
        ("5k", "ambiguous_scale_suffix"),          # was read as 5 Boltzmann constants
        ("5K", "ambiguous_scale_suffix"),          # was read as 5 kelvin
        ("(1,234)", "parenthesised_number"),       # accounting negative, was +1234
        ("inf", "non_finite"),
        ("-inf", "non_finite"),
        ("nan", "non_finite"),
        ("NaN V", "non_finite"),
        ("1.2.3", "malformed_number"),             # was read as 0.36
        ("5-10", "malformed_number"),              # was read as -5
        ("1/2", "malformed_number"),               # was evaluated as arithmetic
        ("1 h 30 min", "compound_quantity"),       # was 30 hour*minute
        ("", "empty"),
    ],
)
def test_misreadable_strings_are_refused_with_named_reason(text, reason):
    with pytest.raises(UnitError) as exc:
        as_quantity(text)
    assert reason in str(exc.value)


@pytest.mark.parametrize(
    "text, expected, unit",
    [
        ("42", 42.0, "dimensionless"),
        ("3.14", 3.14, "dimensionless"),
        ("1.2e-3", 0.0012, "dimensionless"),
        ("350 degC", 350.0, "degree_Celsius"),
        ("350degC", 350.0, "degree_Celsius"),
        ("10 mA/cm^2", 10.0, "milliampere / centimeter ** 2"),
        ("-0.5 V", -0.5, "volt"),
        ("5 K", 5.0, "kelvin"),                     # spaced: an explicit unit, not a suffix
    ],
)
def test_well_formed_strings_still_parse(text, expected, unit):
    q = as_quantity(text)
    assert q.magnitude == pytest.approx(expected)
    assert str(q.units) == unit


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_numbers_are_refused(bad):
    with pytest.raises(UnitError, match="non_finite"):
        as_quantity(bad)
    with pytest.raises(UnitError, match="non_finite"):
        as_quantity({"value": bad, "unit": "V"})
    with pytest.raises(UnitError, match="non_finite"):
        to_canonical({"value": bad, "unit": "V"}, "overpotential")


# --------------------------------------------------------------------------- #
# Alias lookup must be case-exact; a case variant of a known alias is refused
# --------------------------------------------------------------------------- #
def test_alias_lookup_is_case_exact():
    assert normalize_unit("M") == "mol/L"
    assert normalize_unit("C") == "degC"
    assert normalize_unit("K") == "kelvin"
    # lower-case "m" is metre and "k" is not kelvin: they must not be rewritten
    assert normalize_unit("m") == "m"
    assert normalize_unit("k") == "k"


@pytest.mark.parametrize("unit", ["m", "k", "mv", "ma/cm2", "MV"])
def test_case_variant_of_alias_is_refused_as_ambiguous(unit):
    with pytest.raises(UnitError, match="ambiguous_unit_case"):
        as_quantity({"value": 1.0, "unit": unit})


def test_metre_is_not_silently_molar():
    # before: {"value": 0.5, "unit": "m"} became 0.5 mol/L
    with pytest.raises(UnitError):
        to_canonical({"value": 0.5, "unit": "m"}, "concentration")


def test_lowercase_k_is_not_silently_kelvin():
    # before: {"value": 300, "unit": "k"} became 300 kelvin = 26.85 degC
    with pytest.raises(UnitError):
        to_canonical({"value": 300, "unit": "k"}, "temperature")


# --------------------------------------------------------------------------- #
# Judge: NaN, axes without a canonical unit, unknown axes
# --------------------------------------------------------------------------- #
def _outcome(rec):
    return rec["outcome"], [d["defect_type"] for d in rec["defects"]], " ".join(
        d["target"] for d in rec["defects"])


def test_nan_value_is_not_within_floor():
    a = perf_card("A", float("nan"))
    b = perf_card("B", 0.30)
    outcome, types, targets = _outcome(compare_pair(a, b))
    assert outcome == "not_comparable"
    assert "quantity_refused" in types
    assert "non_finite" in targets


def test_nan_uncertainty_is_refused():
    a = perf_card("A", 0.30, uncertainty=float("nan"))
    b = perf_card("B", 0.90)
    outcome, types, targets = _outcome(compare_pair(a, b))
    assert outcome == "not_comparable"
    assert "non_finite" in targets


def _card_on_axis(claim_id, value, unit, axis):
    return ClaimCard(
        claim_id=claim_id, claim_kind="stability_value", commitment_direction="asserts",
        causal_direction="independent", physical_scale="molecular",
        measurability="measurable_now", subject=f"cat_{claim_id}", relation="retains",
        object="activity", source_sentence="s", source_document="d",
        provenance_hash=f"h_{claim_id}", axis=axis,
        quantity=Quantity(value=value, unit=unit), conditions=Conditions(**FULL_CONDITIONS),
    )


def test_axis_without_canonical_unit_is_refused_not_compared_raw():
    # before: "90 %" vs "0.9" (no unit) on percent_retention returned fork, margin 89.1
    a = _card_on_axis("A", 90.0, "%", "percent_retention")
    b = _card_on_axis("B", 0.9, "dimensionless", "percent_retention")
    outcome, types, targets = _outcome(compare_pair(a, b))
    assert outcome == "not_comparable"
    assert "quantity_refused" in types
    assert "no_canonical_unit" in targets


def test_unknown_axis_is_refused():
    a = _card_on_axis("A", 1.0, "V", "an_axis_not_in_axes_yaml")
    b = _card_on_axis("B", 2.0, "V", "an_axis_not_in_axes_yaml")
    outcome, types, targets = _outcome(compare_pair(a, b))
    assert outcome == "not_comparable"
    assert "unknown_axis" in targets


def test_well_formed_pair_still_compares():
    assert compare_pair(perf_card("A", 0.30), perf_card("B", 0.305))["outcome"] == "within_floor"
    assert compare_pair(perf_card("A", 0.30), perf_card("B", 0.40))["outcome"] == "fork"


def test_nan_in_condition_is_a_mismatch_not_a_pass():
    cond = dict(FULL_CONDITIONS)
    cond["current_density"] = {"value": float("nan"), "unit": "mA/cm^2", "normalization": "geometric"}
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.30, conditions=cond)
    defects = evaluate_comparability(a.conditions, b.conditions)
    assert any(d.target == "CR2" for d in defects)
    assert math.isnan(cond["current_density"]["value"])
