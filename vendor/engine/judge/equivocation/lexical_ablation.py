"""
Equivocation Removal Test (Per-Instance Lexical Ablation)

For any correspondence resting on a shared term, strip the term
and re-derive edges from typed graphs alone. Check whether
structure survives without the shared vocabulary.

Named for Newman's 1928 objection that untyped structural claims
are trivially satisfiable. This test enforces typing at inference time.
"""

import networkx as nx


def find_shared_terms(graph_a: nx.DiGraph, graph_b: nx.DiGraph) -> set:
    """Find terms that appear in both graphs' node labels."""
    terms_a = set()
    terms_b = set()
    for _, data in graph_a.nodes(data=True):
        terms_a.update(data.get("terms", []))
    for _, data in graph_b.nodes(data=True):
        terms_b.update(data.get("terms", []))
    return terms_a & terms_b


def strip_term_and_check(
    graph_a: nx.DiGraph,
    graph_b: nx.DiGraph,
    term: str
) -> dict:
    """
    Strip a shared term from both graphs and check if any
    structural edges survive without it.

    Returns:
        dict with:
          - term: the stripped term
          - surviving_edges: number of edges that survive
          - verdict: "structurally_supported" or "vocabulary_dependent"
    """
    # Remove nodes containing the term
    stripped_a = graph_a.copy()
    stripped_b = graph_b.copy()

    nodes_to_remove_a = [
        n for n, d in stripped_a.nodes(data=True)
        if term.lower() in [t.lower() for t in d.get("terms", [])]
    ]
    nodes_to_remove_b = [
        n for n, d in stripped_b.nodes(data=True)
        if term.lower() in [t.lower() for t in d.get("terms", [])]
    ]

    stripped_a.remove_nodes_from(nodes_to_remove_a)
    stripped_b.remove_nodes_from(nodes_to_remove_b)

    # Count surviving cross-side edges (edges that could still match)
    surviving_edges = min(stripped_a.number_of_edges(), stripped_b.number_of_edges())

    return {
        "term": term,
        "surviving_edges": surviving_edges,
        "verdict": (
            "structurally_supported" if surviving_edges > 0
            else "vocabulary_dependent"
        )
    }


def equivocation_test(
    graph_a: nx.DiGraph, graph_b: nx.DiGraph
) -> dict:
    """
    Run the full equivocation test on a pair of graphs.

    For every shared term, strip it and check survival.
    If ANY shared term has zero surviving edges, the
    correspondence is vocabulary-dependent (Newman veto).
    """
    shared_terms = find_shared_terms(graph_a, graph_b)

    if not shared_terms:
        return {
            "shared_terms": [],
            "overall_verdict": "no_shared_terms",
            "results": []
        }

    results = []
    vocabulary_dependent = False

    for term in shared_terms:
        result = strip_term_and_check(graph_a, graph_b, term)
        results.append(result)
        if result["verdict"] == "vocabulary_dependent":
            vocabulary_dependent = True

    return {
        "shared_terms": list(shared_terms),
        "overall_verdict": (
            "vocabulary_dependent" if vocabulary_dependent
            else "structurally_supported"
        ),
        "results": results
    }
