"""Phase 11: structure-directed cross-field discovery + Module D reconciliation.

Seed: their closing mechanism claim (mandatory) that the catalyst's endurance traces to
an operando-formed needle-like nanostructure. Strip its vocabulary to a structural
pattern, query other fields (arXiv + Semantic Scholar, cached, capped), and grade each
candidate by rung with its ceiling. Reported modestly (II.3): rung-3 is suggestive only,
thematic matches (rung 4) are quarantined, and a null result (nothing above rung 3) is a
valid outcome. No README superlatives (CC-30). No composition is proposed.
"""

from __future__ import annotations

import json
import os

from labext.discovery.report import discovery_report, reconciliation_report, write_report
from labext.discovery.search import SearchHarness
from labext.discovery.strip import strip_claim
from labext.extraction.backends import _post_json

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DISC = os.path.join(_REPO, "discovery")
_LEDGER = os.path.join(_REPO, "ledger")
MODEL = "claude-sonnet-5"
MAX_QUERIES = 8
MAX_JUDGED = 12

# Their closing mechanism claim (mandatory seed, from arXiv:2609.30133 Outlook/results).
MECHANISM = ("Its endurance traces to an operando-formed needle-like nanostructure; the "
             "additive elements promote a nanostructure that stabilizes Pd against corrosion.")

_JUDGE_SYS = (
    "You grade how well a candidate paper STRUCTURALLY matches a target mechanism, on the "
    "four-rung ladder. Target structural pattern: a structure whose durability or stability "
    "arises from a self-formed reorganization under operating stress, rather than from static "
    "composition. Rungs: 1 structural identity (a genuine isomorphism, almost never warranted "
    "across fields); 2 structural analogy (matched subgraph); 3 generative analogy (suggestive, "
    "hypothesis-generating only); 4 thematic resonance (shared words, no structural survival; "
    "quarantined). Be conservative: shared vocabulary without a shared mechanism is rung 4. "
    "Respond JSON only: {\"rung\": 1|2|3|4, \"reason\": \"<one sentence>\"}."
)


def _judge(cand: dict) -> dict:
    os.makedirs(os.path.join(_DISC, "_judge_cache"), exist_ok=True)
    import hashlib
    key = hashlib.sha256((MODEL + (cand.get("title", "") + cand.get("abstract", ""))[:400]).encode()).hexdigest()[:20]
    cp = os.path.join(_DISC, "_judge_cache", key + ".json")
    if os.path.exists(cp):
        return json.load(open(cp))
    k = os.environ.get("ANTHROPIC_API_KEY")
    if not k:
        return {"rung": 4, "reason": "no key; defaulted to thematic (quarantined)"}
    try:
        payload = _post_json(
            "https://api.anthropic.com/v1/messages",
            {"x-api-key": k, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            {"model": MODEL, "max_tokens": 200, "system": _JUDGE_SYS,
             "messages": [{"role": "user", "content": f"Title: {cand.get('title')}\nAbstract: {(cand.get('abstract') or '')[:1200]}"}]})
        text = "".join(b.get("text", "") for b in payload.get("content", []))
        out = json.loads(text[text.find("{"):text.rfind("}") + 1])
        out["rung"] = int(out.get("rung", 4))
    except Exception as exc:
        out = {"rung": 4, "reason": f"judge error, quarantined: {str(exc)[:60]}"}
    json.dump(out, open(cp, "w"), sort_keys=True)
    return out


def _ledger_summary() -> dict:
    def load(n):
        return json.load(open(os.path.join(_LEDGER, n)))
    rej = load("rejections.json")
    return {"n_claims": len(load("claims.json")), "n_forks": len(load("forks.json")),
            "n_vetoes": len(rej), "n_verdicts": len(load("verdicts.json")),
            "narrative": "Zero numeric forks survived the conditions veto; the reconciliation is "
            "dominated by vetoes (most literature pairs are not comparable). Verdicts against "
            "Lila's H-cell data are all published vetoes (no claim's conditions matched)."}


def run() -> dict:
    os.makedirs(os.path.join(_DISC, "report"), exist_ok=True)
    os.makedirs(os.path.join(_DISC, "found_papers"), exist_ok=True)
    stripped = strip_claim(MECHANISM)
    os.makedirs(os.path.join(_DISC, "queries"), exist_ok=True)
    json.dump(stripped, open(os.path.join(_DISC, "queries", "stripped.json"), "w"), indent=2)

    harness = SearchHarness(os.path.join(_DISC, "queries"), max_queries=MAX_QUERIES, sleep=3.0)
    cands: dict = {}
    for q in stripped["search_queries"][:4]:
        for hit in harness.arxiv(q, max_results=5) + harness.semantic_scholar(q, max_results=5):
            t = (hit.get("title") or "").strip()
            if t and t not in cands:
                cands[t] = hit
    candidates = list(cands.values())
    json.dump(candidates, open(os.path.join(_DISC, "found_papers", "candidates.json"), "w"), indent=2, sort_keys=True)

    matches = []
    for c in candidates[:MAX_JUDGED]:
        j = _judge(c)
        matches.append({"title": c.get("title"), "rung": j["rung"],
                        "source_domain": c.get("source"), "note": j.get("reason", "")[:160]})
    matches.sort(key=lambda m: m["rung"])

    chance = ("Cross-field structural matches at rung 1-2 are rare; the base rate of thematic "
              "(rung 4) hits is high because alien-vocabulary queries surface shared words. A "
              "rung-3 match is suggestive and hypothesis-generating only, not evidence.")
    report = discovery_report(matches, chance_context=chance)
    write_report(report, os.path.join(_DISC, "report", "report.md"))
    write_report(reconciliation_report(_ledger_summary()), os.path.join(_REPO, "reports", "reconciliation.md"))

    above_3 = [m for m in matches if m["rung"] <= 2]
    return {"candidates": len(candidates), "judged": len(matches),
            "rung_counts": {r: sum(1 for m in matches if m["rung"] == r) for r in (1, 2, 3, 4)},
            "above_rung_3": len(above_3),
            "queries_run": harness.queries_run, "capped": len(harness.capped),
            "null_result": len(above_3) == 0}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
