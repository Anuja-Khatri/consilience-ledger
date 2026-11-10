"""Permanent dual-use exclusion policy (CC-31, feature 13-16 guardrail).

The seed content is a benign allowlist only: instrument protection bounds, consumables
budgets, and standard laboratory incompatible-chemical classes from widely published
general safety references. Nothing about synthesis routes to harmful agents, ever.

DUAL_USE_DENYLIST is grep-able. A test asserts the seed registry contains none of these
tokens. If any doubt exists about an entry, it is excluded (CC-31).
"""

from __future__ import annotations

DUAL_USE_DENYLIST = [
    "synthesis route",
    "synthesize agent",
    "nerve agent",
    "chemical weapon",
    "bioweapon",
    "pathogen",
    "toxin production",
    "select agent",
    "explosive synthesis",
    "detonator",
    "weaponiz",
    "precursor to",
    "enrich uranium",
    "lethal dose",
]


def scan_text(text: str) -> list[str]:
    """Return any denylisted tokens present in text (case-insensitive)."""
    low = text.lower()
    return [tok for tok in DUAL_USE_DENYLIST if tok in low]


__all__ = ["DUAL_USE_DENYLIST", "scan_text"]
