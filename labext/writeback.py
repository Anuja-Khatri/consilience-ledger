"""Phase 5: writeback. Compute verdicts of published claims against Lila's own H-CELL
instrument data, under D7.

Verdicts use the H-cell data (fig_3e.csv: iR-corrected long-term H-cell overpotential).
The CP1 600s screening data (oer_exp_data.csv) is SCREENING tier and is used only to
demonstrate vetoes: it is comparative, not absolute (II.3), and never yields a
confirm/contradict verdict. This follows the ruling that writeback uses H-cell verdicts
plus published vetoes only.

A verdict is computed only when the claim's conditions are proven comparable to the
H-cell measurement (same conditions veto as the ledger). The H-cell data is iR-corrected
and long-term; its electrolyte is not recorded in the file, so it is treated as unstated
(never inferred, D10). Any pairing that fails comparability is a published veto
(not_comparable). D7: a confirm/contradict verdict requires the difference to exceed
max(13 mV, the claim's uncertainty).

Data is CC-BY but NOT committed (CC-28 / Anu ruling); it is loaded at runtime (env
LILA_OER_DATA_DIR or the upstream checkout) and cited by sha + row.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import os

from labext.comparability import evaluate_comparability
from labext.ledger import load_cards
from labext.schema import ClaimCard, Conditions
from labext.units import UnitError, to_canonical

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_DIR = os.path.join(os.path.dirname(_REPO), "upstream", "lila_oer_manuscript", "data")
_MANUSCRIPT_SHA = "92a773790b684786cb8956e3c2cac668043850cb"
FLOOR_V = 0.013

_ELEMENTS = ["In", "Mn", "Pd", "Ni", "Ta", "Ru", "Co", "Fe", "Zr", "Sn", "Nb", "Ti",
             "Sb", "Zn", "Mo", "Hf", "Ag", "Al", "Bi", "Cu", "Cr", "Pb", "Ge", "Si", "Ir", "W", "V"]

# The H-cell measurement's own conditions: iR-corrected, long-term tier. Electrolyte and
# current density are NOT in fig_3e.csv, so they stay unstated (never inferred, D10).
HCELL_CONDITIONS = Conditions(ir_correction=True, protocol_tier="long_term")


def parse_elements(subject: str) -> frozenset:
    return frozenset(el for el in sorted(_ELEMENTS, key=len, reverse=True) if el in subject)


def _file_sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_hcell(path: str) -> dict:
    rows = list(csv.DictReader(open(path)))
    by_system: dict = {}
    for i, r in enumerate(rows):
        try:
            elems = parse_elements(r["material_system"])
            eta = float(r["overpotential_corrected_avg"])
        except Exception:
            continue
        by_system.setdefault(elems, {"rows": [], "eta": []})
        by_system[elems]["rows"].append(i)
        by_system[elems]["eta"].append(eta)
    return by_system


def load_screening(path: str) -> dict:
    rows = list(csv.DictReader(open(path)))
    by_system: dict = {}
    for i, r in enumerate(rows):
        try:
            elems = frozenset(ast.literal_eval(r["target_elements"]))
        except Exception:
            continue
        by_system.setdefault(elems, []).append(i)
    return by_system


def _claim_eta_volts(card: ClaimCard):
    q = card.quantity
    if q is None:
        return None, None
    try:
        v = to_canonical({"value": q.value, "unit": q.unit}, "overpotential")
    except UnitError:
        return None, None
    unc = None
    if q.uncertainty is not None:
        try:
            unc = to_canonical({"value": q.uncertainty, "unit": q.unit}, "overpotential")
        except UnitError:
            unc = None
    return v, unc


def compute_verdicts(cards: list[ClaimCard], data_dir: str = None) -> dict:
    data_dir = data_dir or os.environ.get("LILA_OER_DATA_DIR", _DEFAULT_DIR)
    hcell_path = os.path.join(data_dir, "fig_3e.csv")
    screen_path = os.path.join(data_dir, "oer_exp_data.csv")
    if not os.path.exists(hcell_path):
        return {"error": f"H-cell data not found at {hcell_path}; set LILA_OER_DATA_DIR", "verdicts": []}
    hcell_sha = _file_sha(hcell_path)
    hcell = load_hcell(hcell_path)
    screen = load_screening(screen_path) if os.path.exists(screen_path) else {}

    verdicts = []
    for c in cards:
        if c.claim_kind.value != "performance_value" or c.axis != "overpotential_at_current_density":
            continue
        claim_v, claim_unc = _claim_eta_volts(c)
        if claim_v is None:
            continue
        elems = parse_elements(c.subject)
        floor = max(FLOOR_V, claim_unc or 0.0)
        base = {
            "verdict_id": f"V_{c.claim_id}", "claim_id": c.claim_id, "claim_subject": c.subject,
            "claim_value_V": round(claim_v, 4), "rules_version": "comparability-v0",
            "map_version": "materials_oer-v0", "floor_applied": floor,
            "claim_protocol_tier": c.conditions.protocol_tier,
            "claim_ir_correction": c.conditions.ir_correction,
        }
        ds = {"hcell_file": "fig_3e.csv", "hcell_sha256": hcell_sha,
              "manuscript_commit": _MANUSCRIPT_SHA,
              "screening_file": "oer_exp_data.csv (CP1 600s, screening tier, comparative not absolute)",
              "screening_row_refs": (screen.get(elems, [])[:5] if elems else [])}

        if not elems or elems not in hcell:
            verdicts.append({**base, "outcome": "not_comparable", "margin": None,
                             "defects": [{"defect_type": "no_hcell_data",
                                          "target": "".join(sorted(elems)) or "unknown_system"}],
                             "data_source": ds})
            continue

        # conditions veto: is the claim comparable to the H-cell measurement?
        defects = evaluate_comparability(c.conditions, HCELL_CONDITIONS)
        rows = hcell[elems]["rows"]
        ds["hcell_row_refs"] = rows[:10]
        ds["hcell_material_match"] = sorted(elems)
        if defects:
            verdicts.append({**base, "outcome": "not_comparable", "margin": None,
                             "defects": [d.model_dump(mode="json") for d in defects],
                             "data_source": ds})
            continue
        best = min(hcell[elems]["eta"])
        mean = sum(hcell[elems]["eta"]) / len(hcell[elems]["eta"])
        margin = abs(claim_v - best)
        outcome = "within_floor" if margin <= floor else "contradicted"
        verdicts.append({**base, "outcome": outcome, "margin": round(margin, 4),
                         "measured_best_V": round(best, 4), "measured_mean_V": round(mean, 4),
                         "n_hcell_rows": len(rows), "defects": [], "data_source": ds})
    return {"verdicts": sorted(verdicts, key=lambda v: v["verdict_id"]), "hcell_sha": hcell_sha}


def write_verdicts(cards: list[ClaimCard], data_dir: str = None) -> dict:
    result = compute_verdicts(cards, data_dir)
    verdicts = result.get("verdicts", [])
    with open(os.path.join(_REPO, "ledger", "verdicts.json"), "w") as fh:
        json.dump(verdicts, fh, indent=2, sort_keys=True)
        fh.write("\n")
    from collections import Counter
    oc = Counter(v["outcome"] for v in verdicts)
    lines = ["# Verdicts (writeback against Lila's H-cell instrument data)", "",
             "Verdicts use fig_3e.csv (iR-corrected long-term H-cell overpotential; CC-BY, not "
             f"committed, CC-28), sha `{result.get('hcell_sha', '')[:16]}...`, cited by row index. "
             "The CP1 600s screening data is comparative, not absolute, and is used only to "
             "demonstrate vetoes, never to confirm or contradict a claim.", "",
             f"Outcomes: {dict(oc)}", "",
             "| verdict | subject | claim V | measured best V | outcome | why |",
             "|---|---|---|---|---|---|"]
    for v in verdicts:
        why = "; ".join(f"{d['defect_type']}:{d['target']}" for d in v.get("defects", [])) or "comparable"
        lines.append(f"| {v['verdict_id']} | {v['claim_subject'][:22]} | {v['claim_value_V']} | "
                     f"{v.get('measured_best_V', '-')} | {v['outcome']} | {why} |")
    lines += ["", "Every not_comparable row is a published veto: the claim's conditions were not "
              "proven comparable to an H-cell measurement (no H-cell data for the system, a tier or "
              "iR-correction mismatch, or an unstated electrolyte). This respects the comparative, "
              "not absolute framing (II.3) and the H-cell-verdicts-only ruling. Expected (CC-21)."]
    with open(os.path.join(_REPO, "reports", "verdicts.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"n": len(verdicts), "outcomes": dict(oc)}


if __name__ == "__main__":
    cards = load_cards(os.path.join(_REPO, "extraction", "approved_cards.jsonl"))
    print(json.dumps(write_verdicts(cards), indent=2))
