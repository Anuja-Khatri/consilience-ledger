"""Apply the Checkpoint 1 triage (CP1-TRIAGE.md), approved by Anu, to the review queue.

This encodes the section-4 per-file decisions and batch rules BR1-BR7, ticks the verdict
box in each review md, and writes the corrected card (BR2 sentence-evidence strips, BR4
bound/re-type, BR5 range, BR7 axis) into the verdict block. BR1 (id regeneration) is
applied later by apply_review. Decisions are Anu's, drafted by Claude against sentence
evidence; this is the project's disclosed method.

Run: python -m labext.apply_cp1
"""

from __future__ import annotations

import json
import os
import re

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REVIEW = os.path.join(_REPO, "extraction", "review_queue")

THEIR = "2609.30133"
PENG = "ref40_peng2023"

# v = which model card to take (A/B) or reject; optional transforms.
DECISIONS = {
    f"{THEIR}__001": {"v": "B", "retype": {"subject": "NiTaPdOx", "hours": 470, "threshold": 0.5}, "strip": ["electrolyte", "current_density"]},
    f"{THEIR}__002": {"v": "B", "retype": {"subject": "PdOx", "hours": 200, "threshold": 0.5}, "strip": ["electrolyte", "current_density"]},
    f"{THEIR}__003": {"v": "A"},
    f"{THEIR}__004": {"v": "A"},
    f"{THEIR}__005": {"v": "B", "strip": ["electrolyte", "current_density"]},
    f"{THEIR}__006": {"v": "B"},
    f"{THEIR}__007": {"v": "B"},
    f"{THEIR}__008": {"v": "reject"},
    f"{THEIR}__009": {"v": "reject"},
    f"{THEIR}__010": {"v": "B", "strip": ["electrolyte", "current_density"], "bound": "upper"},
    f"{THEIR}__011": {"v": "reject"},
    f"{THEIR}__012": {"v": "B", "strip": ["electrolyte", "current_density"]},
    f"{THEIR}__013": {"v": "B", "strip": ["electrolyte", "current_density"]},
    f"{THEIR}__014": {"v": "B", "strip": ["electrolyte", "current_density"]},
    f"{THEIR}__015": {"v": "reject"},
    f"{THEIR}__016": {"v": "reject"},
    f"{THEIR}__017": {"v": "A", "strip": ["substrate"]},
    f"{THEIR}__018": {"v": "reject"},
    f"{THEIR}__019": {"v": "reject"},
    f"{THEIR}__020": {"v": "B"},
    f"{THEIR}__021": {"v": "B"},
    f"{THEIR}__022": {"v": "reject"},
    f"{THEIR}__023": {"v": "B"},
    f"{THEIR}__024": {"v": "B", "range": {"lo": 0.3, "hi": 0.7, "unit": "umol/cm^2"}},
    f"{THEIR}__025": {"v": "reject"},
    f"{PENG}__001": {"v": "reject"},
    f"{PENG}__002": {"v": "A"},
    f"{PENG}__003": {"v": "reject"},
    f"{PENG}__004": {"v": "A", "strip": ["substrate"]},
    f"{PENG}__005": {"v": "reject"},
    f"{PENG}__006": {"v": "A", "strip": ["substrate"]},
    f"{PENG}__007": {"v": "reject"},
    f"{PENG}__008": {"v": "reject"},
    f"{PENG}__009": {"v": "B", "strip": ["loading", "substrate"]},
    f"{PENG}__010": {"v": "B", "strip": ["loading", "substrate"]},
    f"{PENG}__011": {"v": "A", "strip": ["electrolyte"], "bound": "lower"},
    f"{PENG}__012": {"v": "reject"},
    f"{PENG}__013": {"v": "A", "strip": ["current_density", "electrolyte"]},
    f"{PENG}__014": {"v": "reject"},
    f"{PENG}__015": {"v": "reject"},
    f"{PENG}__016": {"v": "reject"},
    f"{PENG}__017": {"v": "reject"},
    f"{PENG}__018": {"v": "reject"},
    f"{PENG}__019": {"v": "B", "strip": ["electrolyte"]},
    f"{PENG}__020": {"v": "A"},
    f"{PENG}__021": {"v": "A", "bound": "upper"},
    f"{PENG}__022": {"v": "A"},
    f"{PENG}__023": {"v": "reject"},
    f"{PENG}__024": {"v": "reject"},
    f"{PENG}__025": {"v": "A", "strip": ["current_density", "electrolyte"]},
    f"{PENG}__026": {"v": "A", "strip": ["electrolyte"], "axis": "mass_activity"},
    f"{PENG}__027": {"v": "reject"},
    f"{PENG}__028": {"v": "reject"},
    f"{PENG}__029": {"v": "reject"},
    f"{PENG}__030": {"v": "reject"},
    f"{PENG}__031": {"v": "reject"},
    f"{PENG}__032": {"v": "reject"},
    f"{PENG}__033": {"v": "A", "strip": ["electrolyte"]},
    f"{PENG}__034": {"v": "A", "strip": ["electrolyte"]},
    f"{PENG}__035": {"v": "reject"},
    f"{PENG}__036": {"v": "reject"},
    f"{PENG}__037": {"v": "reject"},
    f"{PENG}__038": {"v": "reject"},
    f"{PENG}__039": {"v": "reject"},
    f"{PENG}__040": {"v": "A", "strip": ["electrolyte"]},
    f"{PENG}__041": {"v": "reject"},
    f"{PENG}__042": {"v": "reject"},
    f"{PENG}__043": {"v": "reject"},
    f"{PENG}__044": {"v": "A"},
    f"{PENG}__045": {"v": "A"},
    f"{PENG}__046": {"v": "reject"},
    f"{PENG}__047": {"v": "reject"},
}

_FENCE = re.compile(r"```json\n(.*?)```", re.DOTALL)
_BOXES = [
    ("A", "approve model A"),
    ("B", "approve model B"),
    ("corrected", "approve with corrections (write the corrected card below)"),
    ("reject", "reject"),
]


def _parse_cards(text):
    out = []
    for m in _FENCE.finditer(text):
        try:
            out.append(json.loads(m.group(1).strip()))
        except Exception:
            out.append(None)
    return out


def _transform(base: dict, dec: dict) -> dict:
    c = json.loads(json.dumps(base))
    if "retype" in dec:  # BR4: re-type to a stability lifetime claim
        rt = dec["retype"]
        c["claim_kind"] = "stability_value"
        c["axis"] = "hours_to_threshold"
        c["quantity"] = {"value": rt["hours"], "unit": "h", "uncertainty": None,
                         "uncertainty_kind": "none_stated", "bound": "approx"}
        c["relation"] = "retains_activity"
        c["object"] = f"time_to_{rt['threshold']}V_threshold"
        c["subject"] = rt["subject"]
    if "range" in dec:  # BR5: carry a stated range, not a point
        r = dec["range"]
        mid = (r["lo"] + r["hi"]) / 2
        half = (r["hi"] - r["lo"]) / 2
        c["quantity"] = {"value": mid, "unit": r["unit"], "uncertainty": half,
                         "uncertainty_kind": "stated_range", "bound": "approx"}
    if "bound" in dec:  # BR4
        c.setdefault("quantity", {})
        c["quantity"]["bound"] = dec["bound"]
    if "axis" in dec:  # BR7
        c["axis"] = dec["axis"]
    for f in dec.get("strip", []):  # BR2: strip conditions not in the sentence
        if isinstance(c.get("conditions"), dict):
            c["conditions"][f] = "unstated"
    return c


def _has_corrections(dec: dict) -> bool:
    return any(k in dec for k in ("retype", "range", "bound", "axis", "strip"))


def _rewrite(path: str, choice: str, corrected: dict | None):
    text = open(path, encoding="utf-8").read()
    head = text.split("## Verdict (Anu)")[0].rstrip()
    vl = ["## Verdict (Anu)", "",
          "Decision: Anu, via the Checkpoint 1 triage (CP1-TRIAGE.md); batch rules BR1-BR7 applied.", ""]
    for key, label in _BOXES:
        vl.append(f"- [{'x' if key == choice else ' '}] {label}")
    vl += ["", "```json", json.dumps(corrected, indent=2, sort_keys=True) if corrected else "", "```", ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + "\n\n" + "\n".join(vl) + "\n")


def main() -> dict:
    counts = {"approved": 0, "rejected": 0, "corrected": 0, "missing": 0}
    for key, dec in DECISIONS.items():
        path = os.path.join(_REVIEW, key + ".md")
        if not os.path.exists(path):
            counts["missing"] += 1
            continue
        if dec["v"] == "reject":
            _rewrite(path, "reject", None)
            counts["rejected"] += 1
            continue
        cards = _parse_cards(open(path, encoding="utf-8").read())
        base = (cards[0] if dec["v"] == "A" else cards[1]) if len(cards) > 1 else None
        if base is None:
            counts["missing"] += 1
            continue
        if _has_corrections(dec):
            _rewrite(path, "corrected", _transform(base, dec))
            counts["corrected"] += 1
        else:
            _rewrite(path, dec["v"], None)
        counts["approved"] += 1
    return counts


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
