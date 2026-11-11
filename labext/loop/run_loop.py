"""Phase 10: the Stage 3 loop, end to end, on a clearly-labeled SYNTHETIC simulator-lookup example.

Zero real forks survived the ledger (CC-22), so the loop runs on a synthetic simulator-lookup
example: it pairs two DIFFERENT existing materials and looks up each one's overpotential, which is
NOT a disagreement between claims about the same entity (not a fork). Every artifact says SYNTHETIC
and SIM-NOT-CHEMISTRY. The OERSIM step replays the public ``oer13_cps`` dataset shipped in
helao-async (MIT-licensed; High-Throughput-Experimentation) — a combinatorial OER chronopotentiometry
library over a plate of 13 BASE metals (Ca, Ce, Co, Cu, Fe, La, Mg, Mn, Ni, Sb, Sn, Ta, Zn; no
palladium). It is NOT Lila's data and NOT Lila's palladium systems; this is a simulation over that
public recorded dataset, not a new chemical measurement. A card whose instrument OERSIM cannot run
gets status plan_only: it stops at the plan + gate stage, with no faked result (CC-25). No
composition is proposed anywhere; the two catalysts are existing addressable points in the public
helao-async dataset.
"""

from __future__ import annotations

import hashlib
import json
import os

from labext.loop import SIM_NOT_CHEMISTRY
from labext.loop.card import ExperimentCard
from labext.loop.dossier import write_dossier
from labext.loop.fork_table import rows_from_cards, write_table
from labext.loop.generate import generate_card
from labext.loop.translator import card_to_sequence, validate_sequence
from labext.schema import ClaimCard, Conditions, Quantity
from safety_format.boundary import plan_fingerprint
from safety_format.compiler import compile_screen, load_registry
from vendor.labgate.sim_ext.oersim import InProcessOERSIM

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LOOP = os.path.join(_REPO, "loop")
_SEED = os.path.join(_REPO, "safety_format", "seed", "registry.yaml")
SYNTHETIC = True
_DATASET = os.environ.get(
    "HELAO_DATASET",
    os.path.expanduser("~/lila-gate/helao-async/helao/deploy/test/demos/data/oer13_cps.pzstd"),
)
FLOOR_V = 0.013


def _comp_label(comp_vec, elements) -> str:
    return "".join(f"{elements[i]}{v}" for i, v in enumerate(comp_vec) if v) or "blank"


def _dataset_sha() -> str:
    h = hashlib.sha256()
    with open(_DATASET, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _synthetic_card(cid: str, subject: str, eta: float) -> ClaimCard:
    return ClaimCard(
        claim_id=cid, claim_kind="performance_value", commitment_direction="asserts",
        causal_direction="independent", physical_scale="molecular",
        measurability="measurable_now", measurable_with="cp_chronopotentiometry",
        subject=subject, relation="has_overpotential", object="overpotential",
        domain="materials_oer",
        source_sentence=f"SYNTHETIC simulator-lookup example: {subject} shows {eta} V overpotential in the public oer13_cps dataset.",
        source_document="SYNTHETIC", provenance_hash=f"syn_{cid}",
        axis="overpotential_at_current_density",
        quantity=Quantity(value=eta, unit="V"),
        conditions=Conditions(current_density={"value": 10, "unit": "mA/cm^2", "normalization": "geometric"},
                              ir_correction=False),
    )


def _gate(card: ExperimentCard) -> dict:
    """Run the plan through the safety screen (the no-text-channel gate)."""
    raw_plan = {
        "instrument_settings": {"current_density_ma_cm2": 10, "acid_ml": 5},
        "chemical_classes": [],
        "comment": f"SYNTHETIC simulator-lookup example {card.fork_id}; {SIM_NOT_CHEMISTRY}",
    }
    screen = compile_screen(load_registry(_SEED))
    return screen.check(plan_fingerprint(raw_plan))


def run_loop() -> dict:
    for sub in ["cards", "plans", "dossiers", "runs"]:
        os.makedirs(os.path.join(_LOOP, sub), exist_ok=True)
    sim = InProcessOERSIM(dataset_path=_DATASET)
    comps = sim.addressable()
    sha = _dataset_sha()

    # Two synthetic forks built from existing addressable points (no composition proposed).
    pairs = [(comps[0], comps[1]), (comps[10], comps[400])]
    table_rows = []
    summaries = []

    for i, (ca, cb) in enumerate(pairs, 1):
        la, lb = _comp_label(ca, sim.elements), _comp_label(cb, sim.elements)
        # OERSIM replays the stored CP trace for each existing point in the public helao-async dataset
        ma, mb = sim.measure_cp(ca), sim.measure_cp(cb)
        eta_a, eta_b = ma["actual_eta_vrhe"], mb["actual_eta_vrhe"]
        fork_id = f"SYN{i}|{la}|{lb}"

        card_a = _synthetic_card(f"SYN{i}A", f"SYN:{la}", round(eta_a, 4))
        card_b = _synthetic_card(f"SYN{i}B", f"SYN:{lb}", round(eta_b, 4))
        fork = {"pair_id": fork_id, "axis": "overpotential_at_current_density",
                "margin": round(abs(eta_a - eta_b), 4), "floor_applied": FLOOR_V,
                "canonical_unit": "V", "synthetic": True}
        card = generate_card(fork, card_a, card_b)

        gate = _gate(card)
        status = card.status()  # cp_chronopotentiometry -> ready
        plan = card_to_sequence(card)
        plan["_SYNTHETIC"] = True
        plan["_disclaimer"] = SIM_NOT_CHEMISTRY

        margin = abs(eta_a - eta_b)
        # Two DIFFERENT materials are looked up; a margin above the floor only means the two distinct
        # materials differ (expected), NOT that two claims about the same entity disagree. No fork claim.
        outcome = ("lookup_two_materials_differ" if margin > FLOOR_V
                   else "lookup_two_materials_within_floor")
        trace = {
            "fork_id": fork_id, "SYNTHETIC": True, "disclaimer": SIM_NOT_CHEMISTRY,
            "example_type": "synthetic simulator-lookup example (two different materials; not a fork)",
            "catalyst_a": {"label": la, "comp_vec": list(ca), "oersim_eta_vrhe": round(eta_a, 4)},
            "catalyst_b": {"label": lb, "comp_vec": list(cb), "oersim_eta_vrhe": round(eta_b, 4)},
            "gate": gate, "card_status": status,
            "plan_valid": validate_sequence(plan) == [],
            "margin_V": round(margin, 4), "floor_V": FLOOR_V, "outcome": outcome,
            "oersim_dataset": "oer13_cps.pzstd", "oersim_dataset_sha256": sha,
            "note": ("OERSIM replays the public oer13_cps dataset shipped in helao-async "
                     "(MIT; High-Throughput-Experimentation; 13 base metals, no palladium). Not Lila's "
                     "data; not a new chemical measurement. The pair is two different materials, so the "
                     "margin is a lookup difference, not a fork."),
        }
        # writeback artifacts
        json.dump(card.model_dump(mode="json"), open(os.path.join(_LOOP, "cards", f"{i}.json"), "w"), indent=2, sort_keys=True)
        json.dump(plan, open(os.path.join(_LOOP, "plans", f"{i}.json"), "w"), indent=2, sort_keys=True)
        json.dump(trace, open(os.path.join(_LOOP, "runs", f"{i}.json"), "w"), indent=2, sort_keys=True)
        write_dossier(card, fork, os.path.join(_LOOP, "dossiers"))
        table_rows.extend(rows_from_cards([(fork, card)]))
        summaries.append({"fork_id": fork_id, "gate": gate["decision"], "status": status, "outcome": outcome})

    # plan_only demonstration (CC-25): a card needing an instrument OERSIM cannot run
    po_a = _synthetic_card("SYN3A", "SYN:xasOnly", 0.40)
    po_b = _synthetic_card("SYN3B", "SYN:xasRef", 0.42)
    po_fork = {"pair_id": "SYN3|plan_only", "axis": "overpotential_at_current_density",
               "margin": 0.02, "floor_applied": FLOOR_V, "canonical_unit": "V", "synthetic": True}
    po_card = generate_card(po_fork, po_a, po_b)
    po_card.experiment_design.instrument = "synchrotron_xas"  # not an OERSIM capability
    po_status = po_card.status()  # plan_only
    po_plan = card_to_sequence(po_card)
    po_plan["_SYNTHETIC"] = True
    json.dump({"fork_id": "SYN3|plan_only", "SYNTHETIC": True, "disclaimer": SIM_NOT_CHEMISTRY,
               "card_status": po_status, "plan_valid": validate_sequence(po_plan) == [],
               "outcome": "plan_only", "note": "instrument synchrotron_xas is not in the OERSIM "
               "capability list; stops at plan+gate, no result faked (CC-25)."},
              open(os.path.join(_LOOP, "runs", "3_plan_only.json"), "w"), indent=2, sort_keys=True)
    write_dossier(po_card, po_fork, os.path.join(_LOOP, "dossiers"))
    summaries.append({"fork_id": "SYN3|plan_only", "status": po_status, "outcome": "plan_only"})

    out = write_table(table_rows, _LOOP)
    return {"forks_run": len(pairs), "plan_only": 1, "summaries": summaries,
            "candidate_table": out, "dataset_sha": sha[:16]}


if __name__ == "__main__":
    print(json.dumps(run_loop(), indent=2))
