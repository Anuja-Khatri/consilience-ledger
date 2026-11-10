"""Report templates: Module D reconciliation (feature 21) and the discovery report.

Discovery results are reported modestly (II.3): every match carries a rung and its
ceiling, chance context is given, and "found nothing above rung 3" is a valid published
outcome. No README superlatives (CC-30).
"""

from __future__ import annotations

import os

from vendor.engine.judge.grading.four_rung_ladder import CEILINGS


def reconciliation_report(summary: dict) -> str:
    """Module D: reconcile the ledger against a partner's literature. `summary` carries
    counts and lists; this renders the template."""
    lines = [
        "# Reconciliation report (Module D)",
        "",
        f"- Claims compared: {summary.get('n_claims', 0)}",
        f"- Forks (settleable disagreements): {summary.get('n_forks', 0)}",
        f"- Vetoed pairings (not comparable): {summary.get('n_vetoes', 0)}",
        f"- Verdicts against instrument data: {summary.get('n_verdicts', 0)}",
        "",
        "## Agreements and disagreements",
        "",
        summary.get("narrative", "(filled from the ledger in Stage 1)"),
        "",
        "Every disagreement here passed the conditions veto: the two claims were proven "
        "comparable before being called a disagreement. Pairings that failed the veto are "
        "listed as vetoes with their named defect, not as disagreements.",
        "",
    ]
    return "\n".join(lines)


def discovery_report(matches: list[dict], chance_context: str) -> str:
    """matches: list of {title, rung, source_domain, note}. A rung-graded, modest report."""
    lines = [
        "# Cross-field correspondence report (discovery)",
        "",
        "Structure-directed search across other fields for the durability mechanism. Results "
        "are hypothesis-generating, not evidential. Rung ceilings are stated for every match.",
        "",
        f"Chance context: {chance_context}",
        "",
    ]
    above_3 = [m for m in matches if int(m.get("rung", 4)) <= 2]
    if not matches:
        lines += ["## Result", "", "No cross-field correspondences were found. This is a valid "
                  "outcome and is reported as such."]
        return "\n".join(lines)
    if not above_3:
        lines += ["## Result", "", "Found nothing above rung 3. This is a valid outcome: the "
                  "mechanism question has no structural cross-field match at this corpus and "
                  "search depth. Rung-3 and rung-4 candidates are listed below as suggestions only."]
    lines += ["", "## Candidates", ""]
    for m in matches:
        rung = int(m.get("rung", 4))
        lines.append(f"- **{m.get('title', '(untitled)')}** "
                     f"[{m.get('source_domain', '?')}] rung {rung}")
        lines.append(f"  - ceiling: {CEILINGS.get(rung, '')}")
        if m.get("note"):
            lines.append(f"  - note: {m['note']}")
    lines.append("")
    return "\n".join(lines)


def write_report(text: str, path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)
    return path


__all__ = ["reconciliation_report", "discovery_report", "write_report"]
