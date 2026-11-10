"""Units fail closed (spec: pint fail-closed; Phase 1 acceptance)."""

import pytest

from labext.units import UnitError, to_canonical


def test_bare_number_is_canonical():
    assert to_canonical(10.0, "current_density") == 10.0


def test_string_quantity_converts():
    assert to_canonical("10 mA/cm^2", "current_density") == pytest.approx(10.0)


def test_mapping_quantity_converts_units():
    # 1 A/cm^2 == 1000 mA/cm^2
    assert to_canonical({"value": 1.0, "unit": "A/cm^2"}, "current_density") == pytest.approx(1000.0)


def test_unknown_dimension_fails_closed():
    with pytest.raises(UnitError):
        to_canonical(1.0, "flux_capacitance")


def test_unparseable_quantity_fails_closed():
    with pytest.raises(UnitError):
        to_canonical("banana", "current_density")


def test_dimensional_mismatch_fails_closed():
    # a temperature supplied where a current density is expected
    with pytest.raises(UnitError):
        to_canonical("25 degC", "current_density")


def test_boolean_is_not_a_quantity():
    with pytest.raises(UnitError):
        to_canonical(True, "current_density")
