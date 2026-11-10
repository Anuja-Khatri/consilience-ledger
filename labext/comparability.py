"""Conditions comparability: default-deny, named defects (spec IV.2).

A pair of claims is comparable only if EVERY rule whose field is required passes,
and no required field is 'unstated' on either side. Any unstated required field
yields a ``condition_unstated`` defect naming the field; any failed predicate
yields a ``condition_mismatch`` defect naming the rule id. This is the published
ancestor of ESAMP's state-equivalency rules, applied as a veto before two claims
may be called a disagreement.

The authoritative engine lives here. The vendored VF2 matcher's
``conditions_compatible`` predicate delegates to ``conditions_compatible_bool``.
"""

from __future__ import annotations

import functools
import os

import yaml

from labext.schema import (
    CONDITION_KEYS,
    UNSTATED,
    ComparabilityRules,
    Defect,
    DefectType,
    Conditions,
)
from labext.units import UnitError, to_canonical

_RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "rules",
    "comparability_rules.yaml",
)


def load_rules(path: str) -> ComparabilityRules:
    with open(path, "r") as fh:
        data = yaml.safe_load(fh)
    return ComparabilityRules.model_validate(data)


@functools.lru_cache(maxsize=4)
def _default_rules_cached(path: str, mtime: float) -> ComparabilityRules:
    return load_rules(path)


def default_rules() -> ComparabilityRules:
    """Load the repo's comparability rules, cached by path + mtime."""
    mtime = os.path.getmtime(_RULES_PATH)
    return _default_rules_cached(_RULES_PATH, mtime)


def _as_dict(conditions) -> dict:
    """Normalise a Conditions model or plain dict to the ten-key dict."""
    if isinstance(conditions, Conditions):
        d = conditions.model_dump()
    elif isinstance(conditions, dict):
        d = dict(conditions)
    else:
        raise TypeError(f"conditions must be Conditions or dict, got {type(conditions)}")
    for key in d:
        if key not in CONDITION_KEYS:
            raise ValueError(f"unknown condition key {key!r}")
    return {k: d.get(k, UNSTATED) for k in CONDITION_KEYS}


# --------------------------------------------------------------------------- #
# Predicates
# --------------------------------------------------------------------------- #
def _norm_text(s) -> str:
    return str(s).strip().casefold()


def _elec_equal(va: dict, vb: dict) -> bool:
    if _norm_text(va.get("identity")) != _norm_text(vb.get("identity")):
        return False
    ca, cb = va.get("concentration"), vb.get("concentration")
    if ca == UNSTATED or cb == UNSTATED or not isinstance(ca, dict) or not isinstance(cb, dict):
        return False  # concentration not stated on both -> not provably comparable
    a = to_canonical({"value": ca["value"], "unit": ca["unit"]}, "concentration")
    b = to_canonical({"value": cb["value"], "unit": cb["unit"]}, "concentration")
    return abs(a - b) <= 0


def _numeric_equal(field: str, va, vb, tol: float) -> bool:
    if field == "current_density":
        if va.get("normalization") != vb.get("normalization"):
            return False  # CC-06: geometric vs ecsa are not comparable
        a = to_canonical({"value": va["value"], "unit": va["unit"]}, "current_density")
        b = to_canonical({"value": vb["value"], "unit": vb["unit"]}, "current_density")
        return abs(a - b) <= tol
    if field == "ph":
        return abs(float(va) - float(vb)) <= tol
    if field == "prior_operation_duration":
        a = to_canonical({"value": va["value"], "unit": va["unit"]}, "duration")
        b = to_canonical({"value": vb["value"], "unit": vb["unit"]}, "duration")
        return abs(a - b) <= tol
    raise ValueError(f"equal_within has no numeric handler for field {field!r}")


def _temp_equal(va, vb, tol: float) -> bool:
    # CC-12: room_temperature == room_temperature passes; room_temperature vs a
    # number is a mismatch unless the paper states the number (not inferred).
    a_rt = va == "room_temperature"
    b_rt = vb == "room_temperature"
    if a_rt or b_rt:
        return a_rt and b_rt
    a = to_canonical({"value": va["value"], "unit": va["unit"]}, "temperature")
    b = to_canonical({"value": vb["value"], "unit": vb["unit"]}, "temperature")
    return abs(a - b) <= tol


def _anneal_equal(va, vb, tol: float) -> bool:
    a_ad = va == "as_deposited"
    b_ad = vb == "as_deposited"
    if a_ad or b_ad:
        return a_ad and b_ad
    a = to_canonical({"value": va["value"], "unit": va["unit"]}, "temperature")
    b = to_canonical({"value": vb["value"], "unit": vb["unit"]}, "temperature")
    return abs(a - b) <= tol


def _predicate_passes(field: str, va, vb, predicate) -> bool:
    name = predicate.name
    params = predicate.params or {}
    tol = float(params.get("tolerance", 0))
    if name == "identity_and_concentration_equal":
        return _elec_equal(va, vb)
    if name == "equal_within":
        return _numeric_equal(field, va, vb, tol)
    if name == "enum_equal":
        return va == vb
    if name == "temperature_equal":
        return _temp_equal(va, vb, tol)
    if name == "anneal_equal":
        return _anneal_equal(va, vb, tol)
    raise ValueError(f"unknown comparability predicate {name!r}")


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def evaluate_comparability(cond_a, cond_b, rules: ComparabilityRules = None) -> list[Defect]:
    """Return the list of comparability defects. Empty list means comparable."""
    if rules is None:
        rules = default_rules()
    a = _as_dict(cond_a)
    b = _as_dict(cond_b)

    defects: list[Defect] = []
    unstated_seen: set[str] = set()

    for rule in rules.rules:
        rule_unstated = False
        for field in rule.fields:
            va, vb = a[field], b[field]
            if va == UNSTATED or vb == UNSTATED:
                rule_unstated = True
                if field not in unstated_seen:
                    unstated_seen.add(field)
                    defects.append(
                        Defect(defect_type=DefectType.condition_unstated, target=field)
                    )
        if rule_unstated:
            continue  # cannot evaluate the predicate with an unstated field
        field = rule.fields[0]
        try:
            ok = _predicate_passes(field, a[field], b[field], rule.predicate)
        except UnitError:
            ok = False  # unparseable quantity fails closed -> not comparable
        if not ok:
            defects.append(
                Defect(defect_type=DefectType.condition_mismatch, target=rule.id)
            )
    return defects


def conditions_compatible_bool(cond_a, cond_b, rules: ComparabilityRules = None) -> bool:
    """True iff the two condition sets are comparable under the rules (no defects)."""
    return len(evaluate_comparability(cond_a, cond_b, rules)) == 0


__all__ = [
    "load_rules",
    "default_rules",
    "evaluate_comparability",
    "conditions_compatible_bool",
]
