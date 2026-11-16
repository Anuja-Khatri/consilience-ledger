"""Materials unit canonicalisation, fail-closed.

Reuses the vendored lab-gate unit registry (``vendor.labgate.units``) but not its
string parser: ``as_quantity`` reads the number with a fixed grammar and hands only
the unit to pint, so a bare number, a string like "10 mA/cm^2", or a
{"value","unit"} mapping becomes a pint Quantity, and anything ambiguous (space or
comma separators, parentheses, glued scale suffixes, NaN, infinity, a unit that is a
case variant of a known alias) raises ``UnitError`` with a named reason. We extend
the canonical-unit map to the OER condition/observable world. Nothing is ever
silently coerced: an unparseable or dimensionally wrong quantity raises
``UnitError`` so the caller fails closed (spec: pint fail-closed; D14/CC-09).
"""

from __future__ import annotations

import math
import re

from vendor.labgate.units import _UREG, UnitError

# Unit-spelling canonicalisation (CP1 section 5). Real cards use "C" for Celsius (pint
# reads C as coulomb), "mA cm-2" variants, etc. Normalise the spelling before pint.
# Lookup is CASE-EXACT (whitespace is ignored). A spelling that matches a key only when
# case is ignored ("m" vs "M", "k" vs "K", "mv" vs "mV") is refused as ambiguous, because
# in units case carries meaning (m = metre, M = molar; k = kilo/Boltzmann, K = kelvin).
UNIT_ALIASES = {
    "C": "degC", "°C": "degC", "degreeC": "degC", "Celsius": "degC", "celsius": "degC",
    "degC": "degC",
    "K": "kelvin",
    "mA/cm2": "mA/cm^2", "mAcm-2": "mA/cm^2", "mA/cm^2": "mA/cm^2", "mA*cm-2": "mA/cm^2",
    "mA/cm²": "mA/cm^2", "mAcm^-2": "mA/cm^2",
    "A/cm2": "A/cm^2", "Acm-2": "A/cm^2", "A/cm^2": "A/cm^2", "A/cm²": "A/cm^2",
    "umol/cm2": "umol/cm^2", "umol/cm^2": "umol/cm^2", "µmol/cm2": "umol/cm^2",
    "μmol/cm2": "umol/cm^2",
    "mg/cm2": "mg/cm^2", "mg/cm^2": "mg/cm^2",
    "mol/L": "mol/L", "mol/l": "mol/L", "M": "mol/L",
    "mV/dec": "mV/decade", "mV/decade": "mV/decade",
    "mV": "mV", "V": "V", "h": "h", "hour": "h", "hours": "h",
}
_ALIAS_CASEFOLD = {}
for _k in UNIT_ALIASES:
    _ALIAS_CASEFOLD.setdefault(_k.casefold(), set()).add(_k)


def _alias_key(u: str) -> str:
    return u.strip().replace(" ", "")


def normalize_unit(u):
    """Return the canonical spelling of ``u`` if it is a known alias (case-exact)."""
    if not isinstance(u, str):
        return u
    return UNIT_ALIASES.get(_alias_key(u), u.strip())


def _check_unit_case(u: str) -> None:
    """Refuse a unit that is a case variant of a known alias but not the alias itself."""
    key = _alias_key(u)
    if key in UNIT_ALIASES:
        return
    near = _ALIAS_CASEFOLD.get(key.casefold())
    if near:
        raise UnitError(
            f"ambiguous_unit_case: {u!r} differs only in letter case from the known "
            f"unit spelling(s) {sorted(near)}; case carries meaning in units, refusing"
        )


# --------------------------------------------------------------------------- #
# Strict quantity parsing (fail closed, named reasons)
# --------------------------------------------------------------------------- #
_NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")
_NON_FINITE = re.compile(r"(?<![A-Za-z])(nan|inf|infinity)(?![A-Za-z])", re.IGNORECASE)
# A unit glued to the number that reads as a scale word or suffix ("5M", "5k", "5bn").
_SCALE_SUFFIXES = {"k", "K", "M", "m", "B", "b", "G", "T", "bn", "mn"}
_UNIT_START = re.compile(r"[A-Za-z°µμÅΩ%]")


def _refuse(reason: str, value, detail: str = "") -> UnitError:
    return UnitError(f"{reason}: {value!r}" + (f" ({detail})" if detail else ""))


def _finite(x: float, value) -> float:
    if not math.isfinite(x):
        raise _refuse("non_finite", value, "NaN and infinity are not measurements")
    return x


def _parse_string(text: str):
    """Split ``text`` into (number, unit-or-None) under a strict grammar, else refuse."""
    s = text.strip()
    if not s:
        raise _refuse("empty", text)
    if _NON_FINITE.search(s):
        raise _refuse("non_finite", text, "NaN and infinity are not measurements")
    if s.startswith("("):
        raise _refuse("parenthesised_number", text, "accounting negative or grouping is ambiguous")
    if "," in s:
        raise _refuse("ambiguous_separator", text, "a comma may be a decimal or a thousands separator")
    m = _NUMBER.match(s)
    if not m:
        raise _refuse("malformed_number", text, "no leading number")
    number = float(m.group())
    rest = s[m.end():]
    unit = rest.strip()
    if not unit:
        return number, None
    if rest[0].isspace() and (unit[0].isdigit() or unit[0] in "+-."):
        raise _refuse("space_separated_digits", text, "digits separated by a space are ambiguous")
    if not _UNIT_START.match(unit):
        raise _refuse("malformed_number", text, f"unexpected {unit[0]!r} after the number")
    if re.search(r"\s[+-]?\d", unit):
        raise _refuse("compound_quantity", text, "more than one number in one quantity")
    if not rest[0].isspace() and unit in _SCALE_SUFFIXES:
        raise _refuse("ambiguous_scale_suffix", text, f"{unit!r} may be a unit or a scale word")
    return number, unit


def _build(number: float, unit, value):
    _finite(number, value)
    if unit is None:
        return _UREG.Quantity(number)
    if not isinstance(unit, str):
        raise _refuse("unparseable_unit", value, "unit must be a string")
    _check_unit_case(unit)
    unit = normalize_unit(unit)
    try:
        return _UREG.Quantity(number, unit)
    except Exception as exc:  # undefined unit, parse error
        raise UnitError(f"unparseable_unit: {value!r}: {exc}") from None


def as_quantity(value):
    """Build a pint Quantity from number | str | {'value','unit'}, fail closed.

    Stricter than the vendored parser: the number is read by a fixed grammar, never by
    pint's expression evaluator, so spaces, commas, parentheses, ranges, arithmetic,
    glued scale suffixes, NaN and infinity are refused with a named reason.
    """
    if isinstance(value, bool):
        raise _refuse("not_a_quantity", value, "boolean")
    if isinstance(value, (int, float)):
        return _build(float(value), None, value)
    if isinstance(value, str):
        number, unit = _parse_string(value)
        return _build(number, unit, value)
    if isinstance(value, dict):
        if "value" not in value or "unit" not in value:
            raise UnitError(f"quantity mapping needs 'value' and 'unit': {value!r}")
        v = value["value"]
        if isinstance(v, bool):
            raise _refuse("not_a_quantity", value, "boolean value")
        if isinstance(v, str):
            number, inline_unit = _parse_string(v)
            if inline_unit is not None:
                raise _refuse("malformed_number", value, "unit inside the value field")
        elif isinstance(v, (int, float)):
            number = float(v)
        else:
            raise _refuse("not_a_quantity", value, f"value of type {type(v).__name__}")
        return _build(number, value["unit"], value)
    raise UnitError(f"unsupported quantity type {type(value).__name__}: {value!r}")


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
    q = as_quantity(value)

    # bare number -> already in the canonical unit
    if q.dimensionless and not isinstance(value, (str, dict)):
        return float(q.magnitude)

    try:
        out = float(q.to(canon).magnitude)
    except Exception as exc:  # pint DimensionalityError, undefined unit, etc.
        raise UnitError(
            f"dimensional mismatch: {value!r} is not a {dimension} "
            f"(expected convertible to {canon}): {exc}"
        ) from None
    return _finite(out, value)


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


__all__ = ["UnitError", "as_quantity", "normalize_unit", "to_canonical", "canonical_quantity", "MATERIALS_CANONICAL", "CONDITION_DIMENSION"]
