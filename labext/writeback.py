"""Phase 5: writeback. Compute verdicts of published claims against Lila's own
instrument data (oer_exp_data.csv), under D7.

The data is CC-BY but is NOT committed (Anu ruling / CC-28): it is loaded at runtime
from a user-provided path (env LILA_OER_DATA, else the upstream checkout) and verdicts
cite rows by index + sha. D7: a numeric verdict requires the difference to exceed
max(13 mV floor, the claim's own uncertainty); below that the outcome is within_floor.
Every screening-tier pairing that fails comparability appears as a published veto
(not_comparable), not a verdict (CC-21).
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import os

from labext.ledger import load_cards
from labext.schema import ClaimCard
from labext.units import UnitError, to_canonical

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_DATA = os.path.join(
    os.path.dirname(_REPO), "upstream", "lila_oer_manuscript", "data", "oer_exp_data.csv"
)
_MANUSCRIPT_SHA = "92a773790b684786cb8956e3c2cac668043850cb"
FLOOR_V = 0.013  # Lila's stated reproducibility floor, +/-13 mV

_ELEMENTS = ["In", "Mn", "Pd", "Ni", "Ta", "Ru", "Co", "Fe", "Zr", "Sn", "Nb", "Ti",
             "Sb", "Zn", "Mo", "Hf", "Ag", "Al", "Bi", "Cu", "Cr", "Pb", "Ge", "Si", "Ir", "W", "V"]


def parse_elements(subject: str) -> frozenset:
    found = set()
    s = subject
    for el in sorted(_ELEMENTS, key=len, reverse=True):
        if el in s:
            found.add(el)
    return frozenset(found)


def _file_sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_data(path: str):
    rows = list(csv.DictReader(open(path)))
    by_system: dict = {}
    for i, r in enumerate(rows):
        try:
            elems = frozenset(ast.literal_eval(r["target_elements"]))
            eta = float(r["overpotential_cp1_600s_mean"])
        except Exception:
            continue
        by_system.setdefault(elems, []).append((i, eta))
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


def compute_verdicts(cards: list[ClaimCard], data_path: str = None) -> dict:
    data_path = data_path or os.environ.get("LILA_OER_DATA", _DEFAULT_DATA)
    if not os.path.exists(data_path):
        return {"error": f"data not found at {data_path}; set LILA_OER_DATA", "verdicts": []}
    sha = _file_sha(data_path)
    by_system = load_data(data_path)

    verdicts = []
    for c in cards:
        if c.claim_kind.value != "performance_value" or c.axis != "overpotential_at_current_density":
            continue  # verdicts are computed for overpotential performance claims
        claim_v, claim_unc = _claim_eta_volts(c)
        if claim_v is None:
            continue
        elems = parse_elements(c.subject)
        rows = by_system.get(elems)
        base = {
            "verdict_id": f"V_{c.claim_id}",
            "claim_id": c.claim_id,
            "claim_subject": c.subject,
            "claim_value_V": round(claim_v, 4),
            "rules_version": "comparability-v0",
            "map_version": "materials_oer-v0",
            "floor_applied": max(FLOOR_V, claim_unc or 0.0),
        }
        if not elems or rows is None:
            # no Lila measurement for this catalyst system (e.g. pure Pd): a published veto
            verdicts.append({**base, "outcome": "not_comparable", "margin": None,
                             "data_source": {"file": "oer_exp_data.csv", "sha256": sha,
                                             "manuscript_commit": _MANUSCRIPT_SHA, "row_refs": [],
                                             "note": "no Lila screening data for this catalyst system"}})
            continue
        # screening tier vs an explicitly long-term claim is not comparable (comparative, not absolute)
        if c.conditions.protocol_tier == "long_term":
            verdicts.append({**base, "outcome": "not_comparable", "margin": None,
                             "data_source": {"file": "oer_exp_data.csv", "sha256": sha,
                                             "manuscript_commit": _MANUSCRIPT_SHA,
                                             "row_refs": [i for i, _ in rows[:5]],
                                             "note": "screening-tier data vs long-term claim; not comparable"}})
            continue
        etas = [e for _, e in rows]
        best = min(etas)
        mean = sum(etas) / len(etas)
        margin = abs(claim_v - best)
        floor = base["floor_applied"]
        outcome = "within_floor" if margin <= floor else "contradicted"
        verdicts.append({**base, "outcome": outcome, "margin": round(margin, 4),
                         "measured_best_V": round(best, 4), "measured_mean_V": round(mean, 4),
                         "n_rows": len(rows),
                         "data_source": {"file": "oer_exp_data.csv", "sha256": sha,
                                         "manuscript_commit": _MANUSCRIPT_SHA,
                                         "row_refs": [i for i, _ in rows[:10]]}})
    return {"verdicts": sorted(verdicts, key=lambda v: v["verdict_id"]), "data_sha": sha}


def write_verdicts(cards: list[ClaimCard], data_path: str = None) -> dict:
    result = compute_verdicts(cards, data_path)
    verdicts = result.get("verdicts", [])
    with open(os.path.join(_REPO, "ledger", "verdicts.json"), "w") as fh:
        json.dump(verdicts, fh, indent=2, sort_keys=True)
        fh.write("\n")
    # render
    from collections import Counter
    oc = Counter(v["outcome"] for v in verdicts)
    lines = ["# Verdicts (writeback against Lila's instrument data)", "",
             "Data loaded at runtime from oer_exp_data.csv (CC-BY, not committed, CC-28), "
             f"sha `{result.get('data_sha', '')[:16]}...`, cited by row index.", "",
             f"Outcomes: {dict(oc)}", "",
             "| verdict | subject | claim V | measured best V | margin | outcome |",
             "|---|---|---|---|---|---|"]
    for v in verdicts:
        lines.append(f"| {v['verdict_id']} | {v['claim_subject']} | {v['claim_value_V']} | "
                     f"{v.get('measured_best_V', '-')} | {v.get('margin', '-')} | {v['outcome']} |")
    lines += ["", "Every not_comparable row is a published veto: Lila has no comparable "
              "measurement for that catalyst/condition set. This is expected (CC-21)."]
    with open(os.path.join(_REPO, "reports", "verdicts.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"n": len(verdicts), "outcomes": dict(oc)}


if __name__ == "__main__":
    cards = load_cards(os.path.join(_REPO, "extraction", "approved_cards.jsonl"))
    print(json.dumps(write_verdicts(cards), indent=2))
