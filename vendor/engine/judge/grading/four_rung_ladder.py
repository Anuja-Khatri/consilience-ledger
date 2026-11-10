"""
Four-Rung Grading Ladder

Converts VF2/MCS matching output into one of four rungs,
each with an explicit ceiling stating what the correspondence
does and does not license.

Pure functions. Deterministic. Same input, same rung.
"""

CEILINGS = {
    1: "Structural identity confirmed. Does NOT license ontological identity. Two theories can be structurally isomorphic and still describe different things.",
    2: "Structural analogy confirmed for the matched subgraph. Does NOT license claims about the non-matching parts. Divergence points are named.",
    3: "Generative analogy only. Suggestive, not evidential. Does NOT license structural claims. May generate hypotheses worth testing.",
    4: "Thematic resonance only (quarantined). Vocabulary match without structural survival. Does NOT license any structural claim."
}


def assign_rung(
    is_isomorphic: bool,
    mcs_ratio: float,
    equivocation_survived: bool,
    has_defect_edge: bool
) -> dict:
    """
    Assign a rung based on matching results.

    Args:
        is_isomorphic: VF2 found a complete subgraph match
        mcs_ratio: Maximum common subgraph ratio (0.0 to 1.0)
        equivocation_survived: Structure survives after shared terms stripped
        has_defect_edge: At least one typed edge mismatch found

    Returns:
        dict with rung (1-4) and ceiling statement
    """
    if has_defect_edge:
        # Newman guard veto: one defect edge drops to lowest supportable rung
        if equivocation_survived:
            return {"rung": 3, "ceiling": CEILINGS[3]}
        else:
            return {"rung": 4, "ceiling": CEILINGS[4]}

    if is_isomorphic and equivocation_survived:
        return {"rung": 1, "ceiling": CEILINGS[1]}

    if mcs_ratio >= 0.5 and equivocation_survived:
        return {"rung": 2, "ceiling": CEILINGS[2]}

    if equivocation_survived:
        return {"rung": 3, "ceiling": CEILINGS[3]}

    return {"rung": 4, "ceiling": CEILINGS[4]}
