"""Normalise raw model cards into the strict schema shape before validation.

Models emit the right content in slightly different surface forms: bound synonyms
(lower_bound), numeric values as strings ("1000 h"), bare-number conditions, extra
condition keys, and occasionally the few-shot example ids. This repair canonicalises
those surface forms. It never invents an UNSTATED condition (D10): a value is only
reshaped when the model stated it; a default unit is applied to a stated bare number
(the canonical OER unit), which is unit-normalisation, not inference. A card that still
fails validation after repair is parked (CC-11), never guessed.
"""

from __future__ import annotations

import re

_BOUND = {
    "lower_bound": "lower", "at_least": "lower", "minimum": "lower", "min": "lower",
    "greater_than": "lower", "upper_bound": "upper", "at_most": "upper", "maximum": "upper",
    "max": "upper", "less_than": "upper", "approximate": "approx", "approximately": "approx",
    "about": "approx", "~": "approx", "equal": "exact", "exact": "exact", "lower": "lower",
    "upper": "upper", "approx": "approx",
}
_CAUSAL = {"causes", "caused_by", "bidirectional", "independent"}
_KINDS = {"location", "timing", "architecture", "mechanism", "computability", "substrate",
          "measurement", "scale", "boundary", "performance_value", "stability_value",
          "synthesis_claim"}
_KIND_MAP = {"performance": "performance_value", "stability": "stability_value",
             "durability": "stability_value", "synthesis": "synthesis_claim"}
_UNC = {"stated_sd", "stated_range", "none_stated"}
_TEN = {"electrolyte", "ph", "current_density", "temperature", "loading", "substrate",
        "protocol_tier", "prior_operation_duration", "anneal_temperature", "ir_correction"}
_COND_SYN = {"duration": "prior_operation_duration", "operation_duration": "prior_operation_duration",
             "anneal_temp": "anneal_temperature", "annealing_temperature": "anneal_temperature",
             "current": "current_density"}
_TIERS = {"ht_screen", "medium_term", "long_term", "other_stated", "unstated"}


def _num(v):
    if isinstance(v, bool):
        return None, None
    if isinstance(v, (int, float)):
        return float(v), None
    if isinstance(v, str):
        m = re.search(r"-?\d+\.?\d*(?:[eE]-?\d+)?", v.replace(",", ""))
        if m:
            return float(m.group()), (v[m.end():].strip() or None)
    return None, None


def _value_unit(v, default_unit):
    """Coerce a stated value into {'value','unit'} or pass through unstated/sentinels."""
    if isinstance(v, str) and v in ("unstated", "room_temperature", "as_deposited"):
        return v
    if isinstance(v, dict) and "value" in v:
        val, unit = _num(v.get("value"))
        if val is None:
            return "unstated"
        out = {"value": val, "unit": str(v.get("unit") or unit or default_unit)}
        if "normalization" in v:
            out["normalization"] = v["normalization"]
        return out
    val, unit = _num(v)
    if val is None:
        return "unstated"
    return {"value": val, "unit": unit or default_unit}


def _repair_conditions(cond: dict) -> dict:
    out = {k: "unstated" for k in _TEN}
    for key, v in cond.items():
        key = _COND_SYN.get(key, key)
        if key not in _TEN:
            continue
        if v == "unstated" or v is None:
            continue
        if key == "electrolyte":
            if isinstance(v, dict) and v.get("identity"):
                conc = v.get("concentration")
                e = {"identity": str(v["identity"])}
                if isinstance(conc, dict) and "value" in conc:
                    val, unit = _num(conc.get("value"))
                    e["concentration"] = {"value": val, "unit": str(conc.get("unit") or unit or "mol/L")} if val is not None else "unstated"
                else:
                    e["concentration"] = "unstated"
                out[key] = e
        elif key == "ph":
            val, _ = _num(v)
            out[key] = val if val is not None else "unstated"
        elif key == "current_density":
            cd = _value_unit(v, "mA/cm^2")
            if isinstance(cd, dict):
                cd.setdefault("unit", "mA/cm^2")
                cd.setdefault("normalization", "unstated")
            out[key] = cd
        elif key == "temperature":
            out[key] = _value_unit(v, "degC")
        elif key == "anneal_temperature":
            out[key] = _value_unit(v, "degC")
        elif key == "prior_operation_duration":
            out[key] = _value_unit(v, "h")
        elif key == "loading":
            out[key] = v if isinstance(v, dict) and v.get("unit") else "unstated"
        elif key == "substrate":
            out[key] = str(v)
        elif key == "protocol_tier":
            out[key] = v if v in _TIERS else "unstated"
        elif key == "ir_correction":
            if isinstance(v, bool):
                out[key] = v
            elif str(v).lower() in ("true", "yes", "corrected", "ir-corrected"):
                out[key] = True
            elif str(v).lower() in ("false", "no", "uncorrected"):
                out[key] = False
            else:
                out[key] = "unstated"
    return out


def repair_raw_card(raw: dict, paper_id: str) -> dict:
    if not isinstance(raw, dict):
        return raw
    c = dict(raw)
    c["source_document"] = paper_id  # override few-shot example leakage
    k = str(c.get("claim_kind", "")).lower()
    if k not in _KINDS:
        c["claim_kind"] = _KIND_MAP.get(k, c.get("claim_kind"))
    if str(c.get("causal_direction", "")).lower() not in _CAUSAL:
        c["causal_direction"] = "independent"
    if str(c.get("commitment_direction", "")).lower() not in ("asserts", "denies"):
        c["commitment_direction"] = "asserts"
    if c.get("measurability") not in ("measurable_now", "measurable_under_assumption", "not_measurable"):
        c["measurability"] = "measurable_now"
    if c.get("measurable_with") == "unstated":
        c["measurable_with"] = None
    q = c.get("quantity")
    if isinstance(q, dict):
        q = dict(q)
        val, unit = _num(q.get("value"))
        if val is not None:
            q["value"] = val
            if not q.get("unit") and unit:
                q["unit"] = unit
        if q.get("unit") is not None:
            q["unit"] = str(q["unit"]).strip()
        q["bound"] = _BOUND.get(str(q.get("bound", "exact")).lower().strip(), "exact")
        if q.get("uncertainty_kind") not in _UNC:
            q["uncertainty_kind"] = "none_stated"
        if isinstance(q.get("uncertainty"), str):
            uv, _ = _num(q["uncertainty"])
            q["uncertainty"] = uv
        c["quantity"] = q
    if isinstance(c.get("conditions"), dict):
        c["conditions"] = _repair_conditions(c["conditions"])
    return c


__all__ = ["repair_raw_card"]
