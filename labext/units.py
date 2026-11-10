"""Materials unit canonicalisation, fail-closed.

Reuses the vendored lab-gate boundary parser (``vendor.labgate.units``), which
turns a bare number, a string like "10 mA/cm^2", or a {"value","unit"} mapping
into a pint Quantity and raises ``UnitError`` on anything unparseable. We extend
its canonical-unit map to the OER condition/observable world. Nothing is ever
silently coerced: an unparseable or dimensionally wrong quantity raises
``UnitError`` so the caller fails closed (spec: pint fail-closed; D14/CC-09).
"""

from __future__ import annotations

from vendor.labgate.units import UnitError, _as_quantity

# dimension name -> canonical unit string (pint-parseable)
MATERIALS_CANONICAL = {
    "temperature": "degree_Celsius",
    "current_density": "milliampere / centimeter ** 2",
    "concentration": "mole / liter",
    "loading_molar": "micromole / centimeter ** 2",
    "loading_mass": "milligram / centimeter ** 2",
    "duration": "hour",
    "potential": "volt",
    "overpotential": "volt",
}


def to_canonical(value, dimension: str) -> float:
    """Return ``value`` as a float in the canonical unit of ``dimension``.

    A bare number is assumed already canonical. A quantity with an explicit unit
    is converted; a dimensional mismatch fails closed with ``UnitError``.
    """
    if dimension not in MATERIALS_CANONICAL:
        raise UnitError(f"unknown materials dimension {dimension!r}")
    canon = MATERIALS_CANONICAL[dimension]
    q = _as_quantity(value)

    # bare number -> already in the canonical unit
    if q.dimensionless and not isinstance(value, (str, dict)):
        return float(q.magnitude)

    try:
        return float(q.to(canon).magnitude)
    except Exception as exc:  # pint DimensionalityError, undefined unit, etc.
        raise UnitError(
            f"dimensional mismatch: {value!r} is not a {dimension} "
            f"(expected convertible to {canon}): {exc}"
        ) from None


# Which dimension each quantity-bearing condition canonicalises against.
CONDITION_DIMENSION = {
    "current_density": "current_density",
    "temperature": "temperature",
    "anneal_temperature": "temperature",
    "prior_operation_duration": "duration",
}


def canonical_quantity(value_unit: dict, dimension: str) -> float:
    """Canonicalise a {'value','unit'} mapping to a float, fail-closed."""
    if not isinstance(value_unit, dict) or "value" not in value_unit or "unit" not in value_unit:
        raise UnitError(f"expected a {{'value','unit'}} mapping, got {value_unit!r}")
    return to_canonical({"value": value_unit["value"], "unit": value_unit["unit"]}, dimension)


__all__ = ["UnitError", "to_canonical", "canonical_quantity", "MATERIALS_CANONICAL", "CONDITION_DIMENSION"]
