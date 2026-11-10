"""Dual-model extraction with diffing (Phase 2).

AGREED-PROVISIONAL = both models produced the identical card (field-exact after
canonicalisation). Everything else goes to the review queue as one md file per
contested claim. Unparseable cards are parked, never guessed (CC-11). Partial
agreement (same claim, different reads) is parked, never averaged (CC-15).
"""

from __future__ import annotations

import json
import os
from collections import defaultdict

from pydantic import ValidationError

from labext.extraction.backends import ExtractorBackend, MissingKeyError
from labext.extraction.cache import JsonlCache
from labext.extraction.canonicalize import align_key, canonical_card
from labext.extraction.review_queue import write_contested
from labext.schema import ClaimCard


def _validate(raw_cards: list[dict]):
    cards, parked = [], []
    for raw in raw_cards:
        try:
            cards.append(ClaimCard.model_validate(raw))
        except ValidationError as exc:
            parked.append({"raw": raw, "error": str(exc)})
    return cards, parked


def run_paper(
    paper_id: str,
    paper_text: str,
    backends: list[ExtractorBackend],
    cache: JsonlCache,
    approved_dir: str,
    review_dir: str,
    windows: list[str] | None = None,
) -> dict:
    """Extract a paper with two models and diff. If ``windows`` is given, each model is
    run per window and the cards concatenated; otherwise the whole text is sent once
    (used by the mock tests)."""
    if len(backends) != 2:
        raise ValueError("dual-model extraction requires exactly two backends (D3)")

    per_model_cards: dict[str, list[ClaimCard]] = {}
    parked_all: list[dict] = []
    model_counts: dict[str, int] = {}
    for b in backends:
        raw = cache.load(paper_id, b.name)
        if raw is None:
            if windows is None:
                raw = b.extract(paper_text)  # may raise MissingKeyError
            else:
                raw = []
                for w in windows:
                    try:
                        raw.extend(b.extract(w))
                    except MissingKeyError:
                        raise
                    except Exception as exc:  # window-level failure: record, continue (CC-16)
                        parked_all.append({"window_error": str(exc)[:160], "model": b.name})
            cache.save(paper_id, b.name, raw)
        cards, parked = _validate(raw)
        per_model_cards[b.name] = cards
        parked_all.extend(parked)
        model_counts[b.name] = len(cards)

    (name_a, cards_a), (name_b, cards_b) = per_model_cards.items()
    buckets_a, buckets_b = defaultdict(list), defaultdict(list)
    for c in cards_a:
        buckets_a[align_key(c)].append(c)
    for c in cards_b:
        buckets_b[align_key(c)].append(c)

    approved: list[ClaimCard] = []
    contested: list[dict] = []
    for key in sorted(set(buckets_a) | set(buckets_b)):
        a_list, b_list = buckets_a.get(key, []), buckets_b.get(key, [])
        if len(a_list) == 1 and len(b_list) == 1:
            a, b = a_list[0], b_list[0]
            if canonical_card(a) == canonical_card(b):
                approved.append(a)
            else:
                contested.append({"key": key, "model_a": name_a, "card_a": a,
                                  "model_b": name_b, "card_b": b, "reason": "models disagree on fields"})
        else:
            # zero-on-one-side or a many-to-one collision: park every card involved
            for c in a_list:
                contested.append({"key": key, "model_a": name_a, "card_a": c,
                                  "model_b": name_b, "card_b": (b_list[0] if len(b_list) == 1 else None),
                                  "reason": "no field-exact 1:1 agreement"})
            if not a_list:
                for c in b_list:
                    contested.append({"key": key, "model_a": name_a, "card_a": None,
                                      "model_b": name_b, "card_b": c,
                                      "reason": f"only {name_b} extracted this claim"})

    os.makedirs(approved_dir, exist_ok=True)
    approved_path = os.path.join(approved_dir, f"{paper_id}.jsonl")
    with open(approved_path, "w") as fh:
        for c in approved:
            row = {**c.model_dump(mode="json"), "status": "agreed_provisional",
                   "extractor_models": [name_a, name_b]}
            fh.write(json.dumps(row, sort_keys=True))
            fh.write("\n")

    review_paths = [write_contested(review_dir, paper_id, i + 1, item) for i, item in enumerate(contested)]

    return {
        "paper_id": paper_id,
        "approved": [c.model_dump(mode="json") for c in approved],
        "approved_path": approved_path,
        "counts": {
            "approved": len(approved),
            "contested": len(contested),
            "parked": len(parked_all),
            "models": model_counts,
        },
        "review_paths": review_paths,
        "parked": parked_all,
    }
