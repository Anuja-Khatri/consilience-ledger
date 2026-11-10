"""Human Review Dossier (feature 19): one page per plan.

Prints the two source sentences side by side, the discriminating-power flag prominently
(CC-27), the falsification (NONE printed prominently if so, CC-26), the card status
(ready / plan_only / not_scientific), and the SIM-NOT-CHEMISTRY disclaimer.
"""

from __future__ import annotations

import os

from labext.loop import SIM_NOT_CHEMISTRY
from labext.loop.card import ExperimentCard


def render_dossier(card: ExperimentCard, fork: dict) -> str:
    d = card.experiment_design
    none_flag = "" if card.is_scientific else "\n**FALSIFICATION = NONE: this card is not falsifiable and does not compile to a plan (CC-26).**\n"
    weak_flag = "" if card.discriminating_power.value == "strong" else "\n**WEAK DISCRIMINATING POWER (CC-27): this experiment may not decide the question.**\n"
    lines = [
        f"# Human Review Dossier: {card.title}",
        "",
        f"_{SIM_NOT_CHEMISTRY}_",
        "",
        f"- Fork: `{card.fork_id}`  |  Axis: `{fork.get('axis')}`  |  Status: **{card.status()}**",
        f"- Discriminating power: **{card.discriminating_power.value}**  |  Cost: {card.estimated_cost.value}  |  Timeline: {card.estimated_timeline}",
        f"- Predicted split: {fork.get('margin')} (floor {fork.get('floor_applied')})",
        none_flag,
        weak_flag,
        "## The two claims",
        "",
        f"- A ({card.claim_a}): > {card.claim_a_source_sentence}",
        f"- B ({card.claim_b}): > {card.claim_b_source_sentence}",
        "",
        "## Experiment design",
        "",
        f"- Hypothesis: {d.hypothesis}",
        f"- Manipulated variable: {d.manipulated_variable}",
        f"- Discriminating observable: {d.discriminating_observable}",
        f"- Instrument: {d.instrument} (exists: {d.instrument_exists}; {d.instrument_source})",
        f"- Protocol: {d.protocol_sketch}",
        f"- If match holds: {d.predicted_outcome_if_match_holds}",
        f"- If match fails: {d.predicted_outcome_if_match_fails}",
        f"- Controls: {d.control_conditions}",
        "",
        f"## Falsification",
        "",
        card.falsification,
        "",
        f"Who could run this: {card.who_could_run_this}",
        f"Sources bridged: {', '.join(card.sources_bridged)}",
        "",
    ]
    return "\n".join(line for line in lines if line is not None)


def write_dossier(card: ExperimentCard, fork: dict, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{card.experiment_id}.md")
    with open(path, "w") as fh:
        fh.write(render_dossier(card, fork))
    return path


__all__ = ["render_dossier", "write_dossier"]
