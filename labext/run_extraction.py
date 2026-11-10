"""Run real dual-model extraction over a set of papers and (for the pilot) decide D6.

Usage (keys must be sourced into the environment by the caller):
  python -m labext.run_extraction pilot
  python -m labext.run_extraction corpus
"""

from __future__ import annotations

import json
import os
import sys

from labext.extraction.backends import MissingKeyError, select_backends
from labext.extraction.cache import JsonlCache
from labext.extraction.pipeline import run_paper
from labext.extraction.windows import paper_windows
from labext.pilot import decide_pilot
from labext.schema import ClaimCard, QUANTITY_KINDS, UNSTATED

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BUILD_ROOT = os.path.dirname(_REPO)
_CORPUS_TEXT = os.path.join(_BUILD_ROOT, "corpus_in", "text")

_RUNS = os.path.join(_REPO, "extraction", "runs")
_APPROVED = os.path.join(_REPO, "extraction", "approved")
_REVIEW = os.path.join(_REPO, "extraction", "review_queue")

# Accessible papers (text ingested under corpus_in/text). Paywalled refs 39, 42 are
# recorded excluded_inaccessible in the manifest; ref 42 (Science) is substituted by
# their own paper, an accessible performance paper (D6).
PILOT_PAPERS = [
    {"id": "2609.30133", "text": "2609.30133.txt"},        # their paper (mandatory, D5)
    {"id": "ref40_peng2023", "text": "ref40_peng2023.txt"},  # ref 40, OA
]

_COND_FIELDS = ["electrolyte", "ph", "current_density", "temperature", "loading",
                "protocol_tier", "prior_operation_duration", "anneal_temperature", "ir_correction"]


def _stated(card: ClaimCard, field: str) -> bool:
    return getattr(card.conditions, field) != UNSTATED


def run_set(papers, max_windows=30) -> dict:
    backends = select_backends()
    if len(backends) < 2:
        raise MissingKeyError("need two model backends; export ANTHROPIC_API_KEY (and OPENAI_API_KEY)")
    cache = JsonlCache(_RUNS)
    approved: list[ClaimCard] = []
    approvable: list[ClaimCard] = []
    per_paper = []
    for spec in papers:
        with open(os.path.join(_CORPUS_TEXT, spec["text"]), encoding="utf-8") as fh:
            text = fh.read()
        windows = paper_windows(text, max_windows=max_windows)
        res = run_paper(spec["id"], text, backends, cache, _APPROVED, _REVIEW, windows=windows)
        res["counts"]["windows"] = len(windows)
        per_paper.append({"id": spec["id"], **res["counts"]})
        approved.extend(ClaimCard.model_validate(c) for c in res["approved"])
        approvable.extend(ClaimCard.model_validate(c) for c in res["validated_union"])
    return {"approved": approved, "approvable": approvable, "per_paper": per_paper,
            "models": [b.name for b in backends]}


def _stated_rate_table(numeric: list[ClaimCard]) -> dict:
    n = len(numeric) or 1
    return {f: round(sum(_stated(c, f) for c in numeric) / n, 3) for f in _COND_FIELDS}


def run_pilot() -> dict:
    out = run_set(PILOT_PAPERS)
    approvable = out["approvable"]  # D6 "approvable" = all validated candidate claims
    numeric = [c for c in approvable if c.claim_kind in QUANTITY_KINDS and c.quantity]
    decision = decide_pilot(approvable, attempt=1)
    result = {
        "decision": decision,
        "models": out["models"],
        "per_paper": out["per_paper"],
        "total_approvable": len(approvable),
        "auto_agreed": len(out["approved"]),
        "numeric_approvable": len(numeric),
        "stated_rate": _stated_rate_table(numeric),
    }
    with open(os.path.join(_REPO, "extraction", "pilot_result.json"), "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
    return result


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    if mode == "pilot":
        r = run_pilot()
        print(json.dumps({k: v for k, v in r.items() if k != "approved"}, indent=2))
    else:
        print("unknown mode", mode)
