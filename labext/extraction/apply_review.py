"""Read Anu's ticked review-queue verdicts into approved claim cards (Phase 3).

Each review md carries two model cards, a ticked verdict, and (for an approve-with-
corrections) a corrected card. This reads the ticked box, selects the corrected card
(or model A / model B), applies BR1 (regenerate claim_id and provenance_hash so no
few-shot id survives), validates through the repair + schema gate, and writes the
approved cards. The code never judges; it records the human's decision.
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import re

from pydantic import ValidationError

from labext.extraction.repair import repair_raw_card
from labext.schema import ClaimCard

_FENCE = re.compile(r"```json\n(.*?)```", re.DOTALL)
_IDX = re.compile(r"__(\d+)\.md$")
_CHECK = {
    "A": "approve model A",
    "B": "approve model B",
    "corrected": "approve with corrections",
    "reject": "reject",
}


def _blocks(text: str) -> list:
    out = []
    for m in _FENCE.finditer(text):
        s = m.group(1).strip()
        try:
            out.append(json.loads(s))
        except Exception:
            out.append(None)
    return out


def _verdict(text: str) -> str | None:
    for key, label in _CHECK.items():
        if re.search(r"-\s*\[[xX]\]\s*" + re.escape(label), text):
            return key
    return None


def parse_review(path: str) -> dict:
    text = open(path, encoding="utf-8").read()
    b = _blocks(text)
    return {
        "path": path,
        "card_a": b[0] if len(b) > 0 else None,
        "card_b": b[1] if len(b) > 1 else None,
        "corrected": b[2] if len(b) > 2 else None,
        "verdict": _verdict(text),
    }


def _regen_ids(card: dict, paper: str, idx: str) -> dict:
    card = dict(card)
    card["claim_id"] = f"{paper}__{idx}"  # BR1: deterministic, no EX ids survive
    prov = f"{card.get('source_document', '')}\x1f{card.get('source_sentence', '')}"
    card["provenance_hash"] = hashlib.sha256(prov.encode()).hexdigest()[:16]
    return card


def apply_review(review_dir: str, out_jsonl: str) -> dict:
    approved = []
    counts = {"approved": 0, "rejected": 0, "skipped": 0}
    for path in sorted(glob.glob(os.path.join(review_dir, "*__*.md"))):
        pr = parse_review(path)
        v = pr["verdict"]
        base = os.path.basename(path)
        paper = base.rsplit("__", 1)[0]
        m = _IDX.search(base)
        idx = m.group(1) if m else "000"
        if v == "reject":
            counts["rejected"] += 1
            continue
        if v is None:
            counts["skipped"] += 1
            continue
        card = pr["corrected"] if v == "corrected" else (pr["card_a"] if v == "A" else pr["card_b"])
        if card is None:
            counts["skipped"] += 1
            continue
        card = _regen_ids(card, paper, idx)
        try:
            cc = ClaimCard.model_validate(repair_raw_card(card, paper))
        except ValidationError:
            counts["skipped"] += 1
            continue
        approved.append(cc)
        counts["approved"] += 1

    os.makedirs(os.path.dirname(out_jsonl), exist_ok=True)
    with open(out_jsonl, "w") as fh:
        for c in approved:
            fh.write(json.dumps(c.model_dump(mode="json"), sort_keys=True) + "\n")
    return {"counts": counts, "approved": [c.model_dump(mode="json") for c in approved], "out": out_jsonl}


__all__ = ["parse_review", "apply_review"]
