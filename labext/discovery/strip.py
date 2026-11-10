"""Vocabulary stripping (feature 23, ported pattern from miu-demo source-discovery).

Given a claim, discard surface domain vocabulary and emit a domain-neutral structural
pattern plus search queries phrased for other fields. This v0 is deterministic (a token
stoplist + templated queries); an LLM refinement is a later improvement. The point is
the same as miu's: topic search returns near-neighbours, structure search crosses the
vocabulary wall.
"""

from __future__ import annotations

import re

# Surface materials/electrochemistry vocabulary to strip.
STOPWORDS = {
    "palladium", "pd", "iridium", "ir", "ruthenium", "ru", "oxide", "oxides", "catalyst",
    "catalysts", "overpotential", "acidic", "acid", "oer", "electrolyte", "electrode",
    "electrochemical", "water", "oxygen", "evolution", "current", "density", "voltage",
    "potential", "nanostructure", "nanoparticle", "operando", "the", "a", "an", "of", "and",
    "to", "in", "its", "is", "are", "with", "that", "this", "from", "by", "for", "at", "on",
}

TARGET_DOMAINS = [
    "dynamical systems", "self-organization", "developmental biology",
    "fracture mechanics", "glass physics", "network theory",
]


def strip_claim(text: str) -> dict:
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    kept = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    # a domain-neutral paraphrase of the structural shape of a durability-by-reorganization claim
    structural_pattern = (
        "a structure whose stability is produced by a self-reinforcing reorganization under load, "
        "rather than by static composition"
    )
    stems = " ".join(dict.fromkeys(kept))  # dedupe, keep order
    queries = [f"{structural_pattern} in {domain}" for domain in TARGET_DOMAINS]
    queries.append(f"self-stabilizing reorganization under operating stress {stems}".strip())
    return {
        "original_text": text,
        "structural_pattern": structural_pattern,
        "kept_terms": kept,
        "search_queries": queries,
        "target_domains": list(TARGET_DOMAINS),
    }


__all__ = ["strip_claim", "TARGET_DOMAINS", "STOPWORDS"]
