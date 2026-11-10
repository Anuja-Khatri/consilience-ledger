"""The judge is byte-deterministic from approved cards onward (spec D4, IV.5)."""

from labext.judge import compare_pair
from tests.factories import perf_card
from vendor.engine.judge.hash.determinism_check import verify_determinism


def test_same_inputs_same_hash():
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.40)
    r1 = compare_pair(a, b)
    r2 = compare_pair(a, b)
    v = verify_determinism(r1, r2)
    assert v["match"], v["message"]
    assert r1["content_hash"] == r2["content_hash"]


def test_order_independent():
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.40)
    assert compare_pair(a, b)["content_hash"] == compare_pair(b, a)["content_hash"]


def test_rejection_is_deterministic():
    from tests.factories import FULL_CONDITIONS
    cond_b = dict(FULL_CONDITIONS)
    cond_b["current_density"] = {"value": 20.0, "unit": "mA/cm^2", "normalization": "geometric"}
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.40, conditions=cond_b)
    assert compare_pair(a, b)["content_hash"] == compare_pair(a, b)["content_hash"]
