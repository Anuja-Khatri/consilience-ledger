"""Deterministic pairwise judge over APPROVED claim cards (spec D4, IV).

Order of checks for a quantity pair:
  1. axis match           -> else defect ``axis_mismatch`` (CC-13)
  2. conditions veto       -> else defects ``condition_unstated`` / ``condition_mismatch``
                             (gate is the vendored ``conditions_compatible`` predicate)
  3. quantity vs floor     -> ``fork`` if the margin exceeds the floor (D7), else ``within_floor``

Mechanism / non-quantitative pairs take the structural path (vendored VF2 matcher +
equivocation + four-rung ladder); no conditions veto is applied to them (CC-14).

Every record carries a SHA-256 ``content_hash`` (vendored determinism hasher), plus
``rules_version`` and ``map_version`` (spec IV.2/IV.5).
"""

from __future__ import annotations

import functools
import os

import yaml

from labext import CODE_VERSION
from labext.comparability import default_rules, evaluate_comparability
from labext.schema import ClaimCard, QUANTITY_KINDS, ClaimKind
from labext.units import UnitError
from vendor.engine.judge.hash.determinism_check import compute_verdict_hash
from vendor.engine.judge.matching.vf2_typed import (
    conditions_compatible,
    check_subgraph_isomorphism,
)
from vendor.engine.judge.equivocation.lexical_ablation import equivocation_test
from vendor.engine.judge.grading.four_rung_ladder import assign_rung
from vendor.labgate.units import _as_quantity

_AXES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "domainpack",
    "materials_oer",
    "axes.yaml",
)


@functools.lru_cache(maxsize=4)
def _axes_cached(path: str, mtime: float) -> dict:
    with open(path, "r") as fh:
        return yaml.safe_load(fh)


def _axes() -> dict:
    return _axes_cached(_AXES_PATH, os.path.getmtime(_AXES_PATH))


def map_version() -> str:
    return _axes().get("version", "materials_oer-v0")


def _axis_meta(axis_id: str) -> dict:
    return (_axes().get("axes") or {}).get(axis_id, {})


def _convert(value: float, unit: str, target_unit: str) -> float:
    """Convert value[unit] to target_unit via pint, fail-closed."""
    try:
        return float(_as_quantity({"value": value, "unit": unit}).to(target_unit).magnitude)
    except Exception as exc:
        raise UnitError(f"cannot convert {value} {unit} to {target_unit}: {exc}") from None


def _canon(q, target_unit):
    """Return (value, uncertainty) for a Quantity in target_unit (or raw if None)."""
    if target_unit is None:
        return float(q.value), float(q.uncertainty or 0.0)
    val = _convert(q.value, q.unit, target_unit)
    unc = _convert(q.uncertainty, q.unit, target_unit) if q.uncertainty is not None else 0.0
    return val, unc


def _finalise(record: dict) -> dict:
    record["content_hash"] = compute_verdict_hash(
        {k: v for k, v in record.items() if k != "content_hash"}
    )
    return record


def _structural(card_a: ClaimCard, card_b: ClaimCard, base: dict) -> dict:
    """Mechanism / non-quantitative path: vendored structural judge (CC-14)."""
    import networkx as nx

    def graph(card):
        g = nx.DiGraph()
        g.add_node(card.subject, claim_kind=card.claim_kind.value,
                   physical_scale=card.physical_scale, terms=[card.subject])
        g.add_node(card.object, claim_kind=card.claim_kind.value,
                   physical_scale=card.physical_scale, terms=[card.object])
        g.add_edge(card.subject, card.object,
                   relation=card.relation, causal_direction=card.causal_direction.value)
        return g

    ga, gb = graph(card_a), graph(card_b)
    iso = check_subgraph_isomorphism(ga, gb)
    equiv = equivocation_test(ga, gb)
    survived = equiv["overall_verdict"] != "vocabulary_dependent"
    rung = assign_rung(
        is_isomorphic=iso["is_isomorphic"],
        mcs_ratio=1.0 if iso["is_isomorphic"] else 0.0,
        equivocation_survived=survived,
        has_defect_edge=not iso["is_isomorphic"],
    )
    base.update(
        kind="correspondence",
        outcome="structural",
        rung=rung["rung"],
        ceiling=rung["ceiling"],
        equivocation=equiv["overall_verdict"],
    )
    return _finalise(base)


def compare_pair(card_a: ClaimCard, card_b: ClaimCard, rules=None, overpotential_floor_v=0.013) -> dict:
    """Compare two approved claim cards. Returns a deterministic JSON-able record."""
    if rules is None:
        rules = default_rules()

    # order-independent pair identity for determinism across argument order
    if card_a.claim_id > card_b.claim_id:
        card_a, card_b = card_b, card_a

    base = {
        "pair_id": f"{card_a.claim_id}|{card_b.claim_id}",
        "claim_a_id": card_a.claim_id,
        "claim_b_id": card_b.claim_id,
        "claim_a_sentence": card_a.source_sentence,
        "claim_b_sentence": card_b.source_sentence,
        "axis": None,
        "defects": [],
        "margin": None,
        "floor_applied": None,
        "canonical_unit": None,
        "rules_version": rules.version,
        "map_version": map_version(),
        "code_version": CODE_VERSION,
    }

    both_quantity = card_a.claim_kind in QUANTITY_KINDS and card_b.claim_kind in QUANTITY_KINDS
    if not both_quantity:
        if card_a.claim_kind == ClaimKind.mechanism and card_b.claim_kind == ClaimKind.mechanism:
            return _structural(card_a, card_b, base)
        base.update(kind="rejection", outcome="not_comparable",
                    defects=[{"defect_type": "type_mismatch",
                              "target": f"{card_a.claim_kind.value} vs {card_b.claim_kind.value}"}])
        return _finalise(base)

    base["axis"] = card_a.axis

    # 1. axis match
    if card_a.axis != card_b.axis:
        base.update(kind="rejection", outcome="axis_mismatch",
                    defects=[{"defect_type": "axis_mismatch",
                              "target": f"{card_a.axis} vs {card_b.axis}"}])
        return _finalise(base)

    # 2. conditions veto (gate = vendored predicate; defects = authoritative engine)
    na = {"conditions": card_a.conditions.model_dump()}
    nb = {"conditions": card_b.conditions.model_dump()}
    if not conditions_compatible(na, nb):
        defects = evaluate_comparability(card_a.conditions, card_b.conditions, rules)
        base.update(kind="rejection", outcome="not_comparable",
                    defects=[d.model_dump(mode="json") for d in defects])
        return _finalise(base)

    # 3. quantity vs floor (D7)
    meta = _axis_meta(card_a.axis)
    target_unit = meta.get("canonical_unit")
    axis_floor = meta.get("floor")
    if axis_floor is None and card_a.axis == "overpotential_at_current_density":
        axis_floor = overpotential_floor_v
    try:
        a_val, a_unc = _canon(card_a.quantity, target_unit)
        b_val, b_unc = _canon(card_b.quantity, target_unit)
    except UnitError as exc:
        base.update(kind="rejection", outcome="not_comparable",
                    defects=[{"defect_type": "condition_mismatch",
                              "target": f"unparseable_quantity: {exc}"}])
        return _finalise(base)

    margin = abs(a_val - b_val)
    floor_applied = max(axis_floor or 0.0, a_unc, b_unc)
    base["margin"] = margin
    base["floor_applied"] = floor_applied
    base["canonical_unit"] = target_unit
    if margin > floor_applied:
        base.update(kind="fork", outcome="fork")
    else:
        base.update(kind="agreement", outcome="within_floor")
    return _finalise(base)


__all__ = ["compare_pair", "map_version"]
