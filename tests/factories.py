"""Synthetic claim-card builders for the Phase 1 tests."""

from __future__ import annotations

from labext.schema import ClaimCard, Conditions, Quantity

# A fully-stated, comparable condition set (all four v0-required fields present).
FULL_CONDITIONS = dict(
    electrolyte={"identity": "H2SO4", "concentration": {"value": 0.5, "unit": "mol/L"}},
    current_density={"value": 10.0, "unit": "mA/cm^2", "normalization": "geometric"},
    temperature={"value": 25.0, "unit": "degC"},
    ir_correction=True,
)


def perf_card(claim_id: str, overpotential_v: float, *, uncertainty=None,
              axis="overpotential_at_current_density", conditions=None, document="docP"):
    cond = dict(FULL_CONDITIONS if conditions is None else conditions)
    return ClaimCard(
        claim_id=claim_id,
        claim_kind="performance_value",
        commitment_direction="asserts",
        causal_direction="independent",
        physical_scale="molecular",
        measurability="measurable_now",
        measurable_with="cp_chronopotentiometry",
        subject=f"catalyst_{claim_id}",
        relation="has_overpotential",
        object="overpotential",
        domain="materials_oer",
        source_sentence=f"Catalyst {claim_id} shows {overpotential_v} V overpotential at 10 mA/cm2 in 0.5 M H2SO4.",
        source_document=document,
        provenance_hash=f"hash_{claim_id}",
        axis=axis,
        quantity=Quantity(value=overpotential_v, unit="V", uncertainty=uncertainty,
                          uncertainty_kind="stated_sd" if uncertainty is not None else "none_stated"),
        conditions=Conditions(**cond),
    )


def stability_card(claim_id: str, hours: float, axis="hours_to_threshold", document="docS"):
    return ClaimCard(
        claim_id=claim_id,
        claim_kind="stability_value",
        commitment_direction="asserts",
        causal_direction="independent",
        physical_scale="molecular",
        measurability="measurable_now",
        measurable_with="cp_chronopotentiometry",
        subject=f"catalyst_{claim_id}",
        relation="retains_activity",
        object="activity",
        domain="materials_oer",
        source_sentence=f"Catalyst {claim_id} lasts {hours} h.",
        source_document=document,
        provenance_hash=f"hash_{claim_id}",
        axis=axis,
        quantity=Quantity(value=hours, unit="h"),
        conditions=Conditions(**FULL_CONDITIONS),
    )
