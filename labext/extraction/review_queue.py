"""Human review queue: one markdown file per contested claim (spec Phase 2).

Each file shows the source sentence, both model outputs, the field-level diff, and
approve/reject checkboxes. Anu edits the file; `apply_review` (Phase 3) reads the
ticked verdicts. The code never judges.
"""

from __future__ import annotations

import json
import os
import re

from labext.extraction.canonicalize import field_diff


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


def _fmt(card) -> str:
    return json.dumps(card.model_dump(mode="json"), indent=2, sort_keys=True) if card else "(no card from this model)"


def write_contested(directory: str, paper_id: str, index: int, item: dict) -> str:
    """item: {key, model_a, card_a, model_b, card_b, reason}. Returns the file path."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{_safe(paper_id)}__{index:03d}.md")
    card_a, card_b = item.get("card_a"), item.get("card_b")
    diff = field_diff(card_a, card_b) if card_a and card_b else ["(only one model produced a card)"]
    sentence = (card_a or card_b).source_sentence if (card_a or card_b) else ""
    lines = [
        f"# Contested claim {paper_id} #{index:03d}",
        "",
        f"Reason: {item.get('reason', 'models disagree')}",
        "",
        "## Source sentence",
        "",
        f"> {sentence}",
        "",
        f"## Differing fields",
        "",
        ", ".join(diff),
        "",
        f"## Model A ({item.get('model_a', '?')})",
        "",
        "```json",
        _fmt(card_a),
        "```",
        "",
        f"## Model B ({item.get('model_b', '?')})",
        "",
        "```json",
        _fmt(card_b),
        "```",
        "",
        "## Verdict (Anu)",
        "",
        "- [ ] approve model A",
        "- [ ] approve model B",
        "- [ ] approve with corrections (write the corrected card below)",
        "- [ ] reject",
        "",
        "```json",
        "",
        "```",
        "",
    ]
    with open(path, "w") as fh:
        fh.write("\n".join(lines))
    return path
