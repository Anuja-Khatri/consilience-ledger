"""Canonical card form for the field-exact agreement diff (Phase 2).

Two model cards are AGREED-PROVISIONAL when they are identical after canonicalisation:
text fields casefolded and stripped, every {value, unit} quantity reduced to pint base
units. Identity fields that differ per extraction run (claim_id, provenance_hash) are
excluded from the comparison; the semantic content is what must agree.
"""

from __future__ import annotations

from labext.schema import ClaimCard
from labext.units import UnitError
from vendor.labgate.units import _as_quantity

# Fields whose agreement defines an identical card. claim_id and provenance_hash are
# per-run identifiers and are deliberately excluded.
SEMANTIC_FIELDS = [
    "claim_kind",
    "commitment_direction",
    "causal_direction",
    "physical_scale",
    "measurability",
    "measurable_with",
    "subject",
    "relation",
    "object",
    "domain",
    "axis",
    "quantity",
    "conditions",
    "source_sentence",
    "source_document",
]


def _canon_value(obj):
    if isinstance(obj, dict):
        if "value" in obj and "unit" in obj:
            try:
                q = _as_quantity({"value": obj["value"], "unit": obj["unit"]}).to_base_units()
                base = [round(float(q.magnitude), 9), str(q.units)]
                extra = {k: _canon_value(v) for k, v in obj.items() if k not in ("value", "unit")}
                return {"__base__": base, **extra}
            except (UnitError, Exception):
                return {k: _canon_value(v) for k, v in sorted(obj.items())}
        return {k: _canon_value(v) for k, v in sorted(obj.items())}
    if isinstance(obj, str):
        return obj.strip().casefold()
    return obj


def canonical_card(card: ClaimCard) -> dict:
    d = card.model_dump(mode="json")
    return {f: _canon_value(d.get(f)) for f in SEMANTIC_FIELDS}


def align_key(card: ClaimCard) -> tuple:
    """Key used to line up the two models' cards for the same underlying claim."""
    return (
        (card.source_document or "").strip().casefold(),
        (card.source_sentence or "").strip().casefold(),
        (card.axis or "").strip().casefold(),
        (card.subject or "").strip().casefold(),
    )


def field_diff(a: ClaimCard, b: ClaimCard) -> list[str]:
    ca, cb = canonical_card(a), canonical_card(b)
    return [f for f in SEMANTIC_FIELDS if ca.get(f) != cb.get(f)]
