"""Deterministic card generator: a settleable fork compiles into an experiment card.

For an OER quantity fork, the discriminating observable is the fork's axis, measured on
both catalysts under the shared conditions with OERSIM's instrument. No LLM is used;
the card is a pure function of the fork and the two claim cards, so it is deterministic.
"""

from __future__ import annotations

from labext.loop.card import CostTier, DiscriminatingPower, ExperimentCard, ExperimentDesign
from labext.schema import ClaimCard


def generate_card(fork: dict, card_a: ClaimCard, card_b: ClaimCard) -> ExperimentCard:
    axis = fork.get("axis") or "overpotential_at_current_density"
    margin = float(fork.get("margin") or 0.0)
    floor = float(fork.get("floor_applied") or 0.0)
    # strong if the predicted split clears the floor by a comfortable margin (CC-27).
    power = DiscriminatingPower.strong if margin >= 2 * max(floor, 1e-9) else DiscriminatingPower.weak
    instrument = "cp_chronopotentiometry"

    design = ExperimentDesign(
        hypothesis=f"{card_a.subject} and {card_b.subject} differ in {axis} under the shared conditions.",
        manipulated_variable="catalyst identity",
        discriminating_observable=axis,
        instrument=instrument,
        instrument_exists=True,
        instrument_source="lab-gate OERSIM (cp chronopotentiometry); replays the public oer13_cps dataset shipped in helao-async (13 base metals, no palladium)",
        protocol_sketch=(
            f"Measure {axis} for both catalysts at the shared current density and electrolyte, "
            f"compare the difference against the {floor} floor."
        ),
        predicted_outcome_if_match_holds="the two values agree within the floor; the disagreement dissolves",
        predicted_outcome_if_match_fails="the two values differ beyond the floor; the disagreement is real",
        control_conditions="same electrolyte, current density, temperature, and iR-correction as both claims",
    )

    return ExperimentCard(
        experiment_id=f"EXP_{fork['pair_id']}",
        fork_id=fork["pair_id"],
        title=f"Discriminate {axis}: {card_a.subject} vs {card_b.subject}",
        claim_a=card_a.claim_id,
        claim_b=card_b.claim_id,
        claim_a_source_sentence=card_a.source_sentence,
        claim_b_source_sentence=card_b.source_sentence,
        structural_bridge=(
            f"Both claims are {axis} values under comparable conditions; they disagree by {margin}."
        ),
        experiment_design=design,
        falsification=(
            f"If the measured {axis} values agree within the floor, the disagreement is not real."
        ),
        discriminating_power=power,
        who_could_run_this="an acidic-OER electrochemistry lab (RDE or SFC)",
        estimated_cost=CostTier.k10,
        estimated_timeline="days",
        sources_bridged=[card_a.source_document, card_b.source_document],
        value_to_lab="resolves a published disagreement before spending the lab on it",
    )


__all__ = ["generate_card"]
