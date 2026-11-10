"""Card -> helao Action/Experiment/Sequence plan (feature 18).

Targets the helao plan shape pinned at ba910c4 (field names verified in Phase 0:
Sequence.sequence_name/sequence_params/planned_experiments;
Experiment.experiment_name/experiment_params/planned_actions;
Action.action_name/action_server/action_params). The full helao models could not be
imported here (they pull numpy and more), so we validate against an embedded minimal
schema for the pinned shape and record the upstream-drift caveat in LIMITATIONS (CC-24).

Only a card whose status is ``ready`` or ``plan_only`` compiles to a plan; a
``not_scientific`` card (falsification NONE) never compiles (CC-26). A ``plan_only``
card produces the plan and stops at the gate, with no OERSIM execution (CC-25).
"""

from __future__ import annotations

from labext.loop.card import ExperimentCard

HELAO_PIN = "ba910c4"


def card_to_sequence(card: ExperimentCard) -> dict:
    status = card.status()
    if status == "not_scientific":
        raise ValueError(f"card {card.experiment_id} is not falsifiable (CC-26); it does not compile")

    action = {
        "action_name": "measure_cp",
        "action_server": {"server_name": "CPSIM", "machine_name": "oersim"},
        "action_params": {
            "fork_id": card.fork_id,
            "observable": card.experiment_design.discriminating_observable,
            "catalyst_a": card.claim_a,
            "catalyst_b": card.claim_b,
        },
    }
    experiment = {
        "experiment_name": "OER_discriminate",
        "experiment_params": {"fork_id": card.fork_id, "status": status},
        "planned_actions": [action],
    }
    sequence = {
        "sequence_name": f"consilience_fork_{card.fork_id}",
        "sequence_params": {
            "fork_id": card.fork_id,
            "helao_pin": HELAO_PIN,
            "status": status,
            "discriminating_power": card.discriminating_power.value,
        },
        "planned_experiments": [
            {"experiment_name": experiment["experiment_name"],
             "experiment_params": experiment["experiment_params"]}
        ],
        "_experiments_full": [experiment],  # actions kept for the gate/OERSIM driver
    }
    return sequence


def validate_sequence(seq: dict) -> list[str]:
    """Return a list of schema errors against the pinned helao shape. Empty == valid."""
    errors = []

    def need(d, key, typ, where):
        if key not in d:
            errors.append(f"{where}: missing {key}")
        elif not isinstance(d[key], typ):
            errors.append(f"{where}: {key} must be {typ.__name__}")

    need(seq, "sequence_name", str, "sequence")
    need(seq, "sequence_params", dict, "sequence")
    need(seq, "planned_experiments", list, "sequence")
    for i, exp in enumerate(seq.get("planned_experiments", [])):
        need(exp, "experiment_name", str, f"experiment[{i}]")
        need(exp, "experiment_params", dict, f"experiment[{i}]")
    for i, exp in enumerate(seq.get("_experiments_full", [])):
        need(exp, "planned_actions", list, f"experiment_full[{i}]")
        for j, act in enumerate(exp.get("planned_actions", [])):
            need(act, "action_name", str, f"action[{i}.{j}]")
            need(act, "action_server", dict, f"action[{i}.{j}]")
            need(act, "action_params", dict, f"action[{i}.{j}]")
    return errors


__all__ = ["card_to_sequence", "validate_sequence", "HELAO_PIN"]
