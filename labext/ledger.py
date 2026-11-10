"""Phase 4: the ledger. Judge every pair of approved claim cards.

Buckets: forks (settleable disagreements that passed the conditions veto), corroborations
(within-floor agreements), graded correspondences (mechanism/structural), and rejections
(every vetoed pairing with its named defect and rule id). Writes ledger/*.json, a
byte-deterministic ledger.hash (approved claims + rules.lock + code version, spec IV.5),
and readable pages into reports/.

Most pairs veto (CC-21): literature conditions are heterogeneous and often unstated, so
the veto table is itself a headline result, framed exactly so.
"""

from __future__ import annotations

import hashlib
import json
import os
from itertools import combinations

from labext import CODE_VERSION
from labext.comparability import default_rules
from labext.judge import compare_pair
from labext.schema import ClaimCard

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LEDGER = os.path.join(_REPO, "ledger")
_REPORTS = os.path.join(_REPO, "reports")
_RULES_LOCK = os.path.join(_REPO, "rules", "rules.lock")


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def build_ledger(cards: list[ClaimCard], rules=None, ledger_dir=_LEDGER, reports_dir=_REPORTS) -> dict:
    if rules is None:
        rules = default_rules()
    forks, corroborations, correspondences, rejections = [], [], [], []
    for a, b in combinations(cards, 2):
        rec = compare_pair(a, b, rules)
        kind = rec["kind"]
        if kind == "fork":
            forks.append(rec)
        elif kind == "agreement":
            corroborations.append(rec)
        elif kind == "correspondence":
            correspondences.append(rec)
        else:
            rejections.append(rec)

    claims = sorted((c.model_dump(mode="json") for c in cards), key=lambda c: c["claim_id"])
    rules_lock = open(_RULES_LOCK).read() if os.path.exists(_RULES_LOCK) else ""
    ledger_hash = hashlib.sha256(
        (_canonical(claims) + "\x1f" + rules_lock + "\x1f" + CODE_VERSION).encode()
    ).hexdigest()

    os.makedirs(ledger_dir, exist_ok=True)
    out = {
        "claims.json": claims,
        "forks.json": sorted(forks, key=lambda r: r["pair_id"]),
        "corroborations.json": sorted(corroborations, key=lambda r: r["pair_id"]),
        "correspondences.json": sorted(correspondences, key=lambda r: r["pair_id"]),
        "rejections.json": sorted(rejections, key=lambda r: r["pair_id"]),
        "verdicts.json": [],  # filled in Phase 5
    }
    for fname, data in out.items():
        with open(os.path.join(ledger_dir, fname), "w") as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
            fh.write("\n")
    with open(os.path.join(ledger_dir, "ledger.hash"), "w") as fh:
        fh.write(ledger_hash + "\n")

    summary = {
        "n_claims": len(claims),
        "n_forks": len(forks),
        "n_corroborations": len(corroborations),
        "n_correspondences": len(correspondences),
        "n_rejections": len(rejections),
        "ledger_hash": ledger_hash,
        "rules_version": rules.version,
    }
    _render(out, summary, reports_dir)
    return summary


def _defect_counts(rejections) -> dict:
    counts: dict = {}
    for r in rejections:
        for d in r.get("defects", []):
            counts[d["defect_type"]] = counts.get(d["defect_type"], 0) + 1
    return counts


def _cond_line(card: dict) -> str:
    c = card.get("conditions", {})
    def s(v):
        return "unstated" if v == "unstated" else json.dumps(v, sort_keys=True)
    return (f"electrolyte={s(c.get('electrolyte'))}, cd={s(c.get('current_density'))}, "
            f"T={s(c.get('temperature'))}, iR={s(c.get('ir_correction'))}")


def _render(out: dict, summary: dict, reports_dir=_REPORTS):
    os.makedirs(reports_dir, exist_ok=True)
    claims_by_id = {c["claim_id"]: c for c in out["claims.json"]}

    lines = ["# Ledger", "",
             f"Rules {summary['rules_version']}. ledger.hash `{summary['ledger_hash'][:16]}...`.", "",
             f"- claims: {summary['n_claims']}",
             f"- forks (settleable disagreements): {summary['n_forks']}",
             f"- corroborations (within floor): {summary['n_corroborations']}",
             f"- correspondences: {summary['n_correspondences']}",
             f"- rejections (vetoed pairings): {summary['n_rejections']}", "",
             "## Defect breakdown (the veto table is a headline result, CC-21)", ""]
    for dt, n in sorted(_defect_counts(out["rejections.json"]).items(), key=lambda x: -x[1]):
        lines.append(f"- {dt}: {n}")
    lines += ["", "## Claims", ""]
    for c in out["claims.json"]:
        q = c.get("quantity") or {}
        lines.append(f"- `{c['claim_id']}` [{c['claim_kind']}/{c.get('axis')}] "
                     f"{c['subject']} {c['relation']} {q.get('value', '')} {q.get('unit', '')}")
        lines.append(f"  - > {c['source_sentence']}")
    with open(os.path.join(reports_dir, "ledger.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    # Spot-check: every fork's two source sentences side by side with conditions.
    fl = ["# Fork spot-check", "",
          "Every fork's two claims, side by side, with the conditions that were proven "
          "comparable before the pair was called a disagreement.", ""]
    for r in out["forks.json"]:
        a, b = claims_by_id.get(r["claim_a_id"], {}), claims_by_id.get(r["claim_b_id"], {})
        fl += [f"## Fork `{r['pair_id']}` (axis {r['axis']}, margin {r.get('margin')} "
               f"{r.get('canonical_unit') or ''}, floor {r.get('floor_applied')})",
               "",
               f"- A `{r['claim_a_id']}`: > {r['claim_a_sentence']}",
               f"  - conditions: {_cond_line(a)}",
               f"- B `{r['claim_b_id']}`: > {r['claim_b_sentence']}",
               f"  - conditions: {_cond_line(b)}", ""]
    if not out["forks.json"]:
        fl += ["(No numeric forks survived the conditions veto. That is a valid Stage 1 "
               "outcome: the ledger, vetoes, and corroborations stand; see LIMITATIONS.)", ""]
    with open(os.path.join(reports_dir, "forks_spotcheck.md"), "w") as fh:
        fh.write("\n".join(fl) + "\n")


def load_cards(path: str) -> list[ClaimCard]:
    with open(path) as fh:
        return [ClaimCard.model_validate(json.loads(line)) for line in fh if line.strip()]


if __name__ == "__main__":
    cards = load_cards(os.path.join(_REPO, "extraction", "approved_cards.jsonl"))
    print(json.dumps(build_ledger(cards), indent=2))
