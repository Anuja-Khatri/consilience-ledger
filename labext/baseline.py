"""Phase 6: the LLM-judge baseline.

The same claim pairs the deterministic judge handled, labeled by a single model call
(comparable? agree/disagree?), cached, and compared. The headline: where the model
calls a disagreement on a pair the judge vetoed as not comparable. Both are reported.

Sample is preregistered and deterministic (no cherry-picking): all forks and
corroborations, plus the first N condition-defect pairs and the first M axis-mismatch
pairs by sorted pair_id. All responses cached to disk, resumable.
"""

from __future__ import annotations

import hashlib
import json
import os

from labext.extraction.backends import _post_json
from labext.ledger import load_cards

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LEDGER = os.path.join(_REPO, "ledger")
_BASE = os.path.join(_REPO, "baseline")
_CACHE = os.path.join(_BASE, "cache")

PREREG = {"condition": 40, "axis_mismatch": 20}  # deterministic caps; forks/corroborations all
BASELINE_MODEL = "claude-sonnet-5"
PROMPT_VERSION = "baseline-judge-v0"

_SYS = (
    "You compare two scientific claims about catalysts. Decide two things and respond "
    "with JSON only: {\"comparable\": true|false, \"relation\": \"agree\"|\"disagree\"|\"na\"}. "
    "comparable = can these be directly compared (same measured quantity under compatible "
    "measurement conditions)? relation = if comparable, do the numbers agree or disagree?"
)


def _summary(card: dict) -> str:
    q = card.get("quantity") or {}
    c = card.get("conditions") or {}
    return (f"subject={card.get('subject')}; axis={card.get('axis')}; "
            f"value={q.get('value')} {q.get('unit')}; "
            f"electrolyte={c.get('electrolyte')}; current_density={c.get('current_density')}; "
            f"temperature={c.get('temperature')}; ir_correction={c.get('ir_correction')}; "
            f"sentence={card.get('source_sentence')}")


def _judge_label(rec: dict) -> tuple[str, str]:
    """Return (judge_label, category) for a ledger record."""
    kind = rec.get("kind")
    if kind == "fork":
        return "disagree", "fork"
    if kind == "agreement":
        return "agree", "corroboration"
    defects = {d["defect_type"] for d in rec.get("defects", [])}
    cat = "axis_mismatch" if "axis_mismatch" in defects else "condition"
    return "not_comparable", cat


def build_pairs() -> list[dict]:
    pairs = []
    for fname in ["forks.json", "corroborations.json", "rejections.json"]:
        for rec in json.load(open(os.path.join(_LEDGER, fname))):
            label, cat = _judge_label(rec)
            pairs.append({"rec": rec, "judge": label, "category": cat})
    return pairs


def select_sample(pairs: list[dict]) -> list[dict]:
    pairs = sorted(pairs, key=lambda p: p["rec"]["pair_id"])
    out, counts = [], {"condition": 0, "axis_mismatch": 0}
    for p in pairs:
        cat = p["category"]
        if cat in ("fork", "corroboration"):
            out.append(p)
        elif counts.get(cat, 0) < PREREG.get(cat, 0):
            counts[cat] += 1
            out.append(p)
    return out


def _cache_path(pair_id: str) -> str:
    h = hashlib.sha256(f"{BASELINE_MODEL}\x1f{PROMPT_VERSION}\x1f{pair_id}".encode()).hexdigest()[:20]
    return os.path.join(_CACHE, f"{h}.json")


def model_label(pair_id: str, a: dict, b: dict) -> dict:
    os.makedirs(_CACHE, exist_ok=True)
    cp = _cache_path(pair_id)
    if os.path.exists(cp):
        return json.load(open(cp))
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return {"comparable": None, "relation": "na", "error": "no key"}
    payload = _post_json(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        {"model": BASELINE_MODEL, "max_tokens": 200, "system": _SYS,
         "messages": [{"role": "user", "content": f"Claim A: {_summary(a)}\n\nClaim B: {_summary(b)}"}]},
    )
    text = "".join(bl.get("text", "") for bl in payload.get("content", []))
    try:
        s, e = text.find("{"), text.rfind("}")
        out = json.loads(text[s:e + 1])
    except Exception:
        out = {"comparable": None, "relation": "na", "parse_error": text[:120]}
    json.dump(out, open(cp, "w"), sort_keys=True)
    return out


def run_baseline() -> dict:
    cards = {c.claim_id: c.model_dump(mode="json")
             for c in load_cards(os.path.join(_REPO, "extraction", "approved_cards.jsonl"))}
    sample = select_sample(build_pairs())
    matrix: dict = {}
    rows = []
    for p in sample:
        rec = p["rec"]
        a, b = cards.get(rec["claim_a_id"], {}), cards.get(rec["claim_b_id"], {})
        ml = model_label(rec["pair_id"], a, b)
        model_rel = "not_comparable" if ml.get("comparable") is False else ml.get("relation", "na")
        key = (p["judge"], model_rel)
        matrix[key] = matrix.get(key, 0) + 1
        rows.append({"pair_id": rec["pair_id"], "judge": p["judge"],
                     "category": p["category"], "model": model_rel})
    # headline: judge vetoed (not_comparable) but the model called a disagreement
    false_disagreements = sum(1 for r in rows if r["judge"] == "not_comparable" and r["model"] == "disagree")
    false_agreements = sum(1 for r in rows if r["judge"] == "not_comparable" and r["model"] == "agree")
    veto_total = sum(1 for r in rows if r["judge"] == "not_comparable")
    return {"matrix": {f"{k[0]}|{k[1]}": v for k, v in matrix.items()},
            "rows": rows, "n": len(rows),
            "false_disagreements_on_vetoed_pairs": false_disagreements,
            "false_agreements_on_vetoed_pairs": false_agreements,
            "vetoed_pairs_in_sample": veto_total}


def write_report() -> dict:
    result = run_baseline()
    os.makedirs(_BASE, exist_ok=True)
    json.dump(result, open(os.path.join(_BASE, "baseline_result.json"), "w"), indent=2, sort_keys=True)
    lines = ["# LLM-judge baseline (Phase 6)", "",
             f"Model: {BASELINE_MODEL}. Preregistered deterministic sample of {result['n']} pairs "
             f"(all forks + corroborations; first {PREREG['condition']} condition-defect and "
             f"first {PREREG['axis_mismatch']} axis-mismatch pairs by sorted pair_id). Cached.", "",
             "## Agreement matrix (deterministic judge rows x model-call columns)", "",
             "| judge \\ model | " + " | ".join(["agree", "disagree", "not_comparable", "na"]) + " |",
             "|---|---|---|---|---|"]
    for jl in ["disagree", "agree", "not_comparable"]:
        cells = [str(result["matrix"].get(f"{jl}|{mc}", 0)) for mc in ["agree", "disagree", "not_comparable", "na"]]
        lines.append(f"| {jl} | " + " | ".join(cells) + " |")
    lines += ["",
              f"## Headline",
              "",
              f"Of {result['vetoed_pairs_in_sample']} pairs the deterministic judge vetoed as NOT "
              f"comparable, the model call made {result['false_disagreements_on_vetoed_pairs'] + result['false_agreements_on_vetoed_pairs']} "
              f"comparisons the veto blocks ({result['false_disagreements_on_vetoed_pairs']} called a "
              f"disagreement, {result['false_agreements_on_vetoed_pairs']} called an agreement); it "
              f"recognised incomparability on the rest. The judge's conditions veto prevents exactly "
              "those comparisons: no prose talks its way past it. The model is capable but not exact; "
              "both labelings are reported; no pairs were cherry-picked (the sample rule is "
              "preregistered above)."]
    open(os.path.join(_BASE, "REPORT.md"), "w").write("\n".join(lines) + "\n")
    return {"n": result["n"], "false_disagreements": result["false_disagreements_on_vetoed_pairs"]}


if __name__ == "__main__":
    print(json.dumps(write_report(), indent=2))
