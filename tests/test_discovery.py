"""Phase 11 discovery scaffolding: strip, search (cached/capped), report templates."""

from labext.discovery.report import discovery_report, reconciliation_report
from labext.discovery.search import SearchHarness
from labext.discovery.strip import strip_claim


def test_strip_is_deterministic_and_drops_vocabulary():
    text = "The palladium oxide catalyst's durability arises from an operando nanostructure."
    a = strip_claim(text)
    b = strip_claim(text)
    assert a == b
    assert "palladium" not in a["kept_terms"]  # surface vocabulary stripped
    assert a["search_queries"] and a["target_domains"]


_FAKE_ARXIV = (
    b'<feed xmlns="http://www.w3.org/2005/Atom"><entry>'
    b"<id>http://arxiv.org/abs/0000.00001</id><title>Self-stabilizing networks</title>"
    b"<summary>A structure that reorganizes under load.</summary></entry></feed>"
)


def test_search_caches_and_caps(tmp_path):
    calls = {"n": 0}

    def fake_fetch(url):
        calls["n"] += 1
        return _FAKE_ARXIV

    h = SearchHarness(str(tmp_path), max_queries=1, sleep=0, fetch=fake_fetch)
    r1 = h.arxiv("query one")
    assert r1[0]["title"] == "Self-stabilizing networks"
    # second distinct query exceeds the cap and is recorded, not fetched
    r2 = h.arxiv("query two")
    assert r2 == []
    assert h.capped and h.capped[0]["query"] == "query two"
    # repeating the first query is served from cache (no new fetch)
    h.arxiv("query one")
    assert calls["n"] == 1


def test_discovery_report_null_result():
    text = discovery_report([], chance_context="random cross-field hit rate not yet calibrated")
    assert "No cross-field correspondences were found" in text


def test_discovery_report_nothing_above_rung_3():
    matches = [{"title": "X", "rung": 3, "source_domain": "dynamical systems"}]
    text = discovery_report(matches, chance_context="context")
    assert "Found nothing above rung 3" in text
    assert "ceiling:" in text


def test_reconciliation_template():
    text = reconciliation_report({"n_claims": 5, "n_forks": 1, "n_vetoes": 3, "n_verdicts": 2})
    assert "Reconciliation report (Module D)" in text
    assert "passed the conditions veto" in text
