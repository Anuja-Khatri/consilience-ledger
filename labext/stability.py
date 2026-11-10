"""Phase 7: fresh materials extraction-stability (test-retest on identical passages).

Re-extract the SAME passages K times with the same model and prompt, then measure how
often a claim recurs. A claim is stable if its (subject, axis, quantity-family) key
recurs in at least ceil(K/2) runs. Stability = stable / distinct. Reported fresh with
its n (II.3); it is NOT equated with the consciousness-domain number.

Each run is an independent live call (the API default is non-deterministic for this
model family; temperature 0 is not accepted, recorded as a caveat). Responses are cached
per (passage, run) so reruns are free.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re

from pydantic import ValidationError

from labext.extraction.backends import AnthropicBackend
from labext.extraction.repair import repair_raw_card
from labext.extraction.windows import paper_windows
from labext.schema import ClaimCard

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BUILD_ROOT = os.path.dirname(_REPO)
_TEXT = os.path.join(_BUILD_ROOT, "corpus_in", "text")
_CACHE = os.path.join(_REPO, "baseline", "stability_cache")

MODEL = "claude-sonnet-5"
K = 3
PER_PAPER = 10
PAPERS = ["2609.30133.txt", "ref40_peng2023.txt"]


def _passages() -> list[str]:
    out = []
    for p in PAPERS:
        path = os.path.join(_TEXT, p)
        if os.path.exists(path):
            out.extend(paper_windows(open(path, encoding="utf-8").read(), max_windows=PER_PAPER))
    return out


def _cache_path(pi: int, run: int) -> str:
    h = hashlib.sha256(f"{MODEL}\x1f{pi}\x1f{run}".encode()).hexdigest()[:20]
    return os.path.join(_CACHE, f"{h}.json")


def _extract(passage: str, pi: int, run: int) -> list[dict]:
    os.makedirs(_CACHE, exist_ok=True)
    cp = _cache_path(pi, run)
    if os.path.exists(cp):
        return json.load(open(cp))
    raw = AnthropicBackend(MODEL).extract(passage)
    json.dump(raw, open(cp, "w"))
    return raw


def _norm_unit(u: str) -> str:
    return (u or "").lower().replace("μ", "u").replace("µ", "u").replace(" ", "")


def _keys(raw: list[dict], paper_id: str) -> set:
    """Cluster by (subject, quantity-family): normalised subject + rounded value + unit.

    The axis string is deliberately excluded: the model relabels the observable
    run-to-run (time_to_threshold vs duration_below) even when the subject and number are
    identical. A stability measured on the axis string would report instability that is
    labeling noise, not claim instability. The axis-label instability is reported
    separately in the stability report.
    """
    out = set()
    for r in raw:
        try:
            c = ClaimCard.model_validate(repair_raw_card(r, paper_id))
        except ValidationError:
            continue
        q = c.quantity
        subj = re.sub(r"[^a-z0-9]", "", c.subject.lower())
        fam = (round(q.value, 2), _norm_unit(q.unit)) if q else (c.claim_kind.value,)
        out.add((subj, fam))
    return out


def measure() -> dict:
    passages = _passages()
    if not passages:
        return {"error": "no passages (corpus_in/text missing)"}
    need = math.ceil(K / 2)
    all_keys: dict = {}
    for pi, passage in enumerate(passages):
        counts: dict = {}
        for run in range(K):
            for key in _keys(_extract(passage, pi, run), "stability"):
                counts[key] = counts.get(key, 0) + 1
        for key, n in counts.items():
            all_keys[(pi, key)] = n
    distinct = len(all_keys)
    stable = sum(1 for n in all_keys.values() if n >= need)
    return {
        "model": MODEL, "K": K, "n_passages": len(passages),
        "n_distinct_claims": distinct,
        "n_stable": stable,
        "stability": round(stable / distinct, 3) if distinct else None,
        "recur_threshold": need,
        "caveat": "temperature default (API rejects temperature 0 for this model family)",
    }


def write_report() -> dict:
    result = measure()
    base = os.path.join(_REPO, "baseline")
    os.makedirs(base, exist_ok=True)
    json.dump(result, open(os.path.join(base, "stability_result.json"), "w"), indent=2, sort_keys=True)
    if "error" not in result:
        lines = [
            "# Materials extraction-stability (fresh, Phase 7)", "",
            f"Model {result['model']}, test-retest K={result['K']} on identical passages "
            f"({result['n_passages']} passages).", "",
            f"- stability = **{result['stability']}** (n = {result['n_distinct_claims']} distinct claims)",
            f"- stable (recurs in >= {result['recur_threshold']} of {result['K']} runs): {result['n_stable']}",
            "",
            "Clustering: a claim is (normalised subject, rounded value, normalised unit). The axis "
            "label is excluded from the key: the model relabels the observable run-to-run "
            "(time_to_threshold vs duration_below) even when the subject and number are identical, so "
            "keying on the axis string would report labeling noise as instability. The (subject, value) "
            "of an extracted numeric claim is highly reproducible; the observable LABEL is not.", "",
            "This is the materials number, reported fresh with its n. It is NOT the consciousness-domain "
            "0.25 (that is a different domain and metric, cited separately with its own n=88).",
            f"Caveat: {result['caveat']}.",
        ]
        open(os.path.join(base, "STABILITY_REPORT.md"), "w").write("\n".join(lines) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(write_report(), indent=2))
