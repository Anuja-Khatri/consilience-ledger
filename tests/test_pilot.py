"""D6 pilot GO/NO-GO rule (Phase 2)."""

from labext.pilot import decide_pilot
from labext.schema import Conditions
from tests.factories import FULL_CONDITIONS, perf_card


def _underconditioned(claim_id):
    cond = dict(FULL_CONDITIONS)
    del cond["ir_correction"]  # iR-correction status not stated
    return perf_card(claim_id, 0.30, conditions=cond)


def test_go_when_ten_fully_conditioned():
    cards = [perf_card(f"C{i}", 0.30 + i * 0.001) for i in range(10)]
    d = decide_pilot(cards)
    assert d["decision"] == "GO"
    assert d["numeric_claims_with_source"] == 10
    assert d["fully_conditioned"] == 10


def test_no_go_when_too_few():
    cards = [perf_card(f"C{i}", 0.30) for i in range(9)]
    d = decide_pilot(cards, attempt=1)
    assert d["decision"] == "NO-GO"
    assert "Pd neighborhood" in d["next_action"]


def test_no_go_when_fewer_than_half_conditioned():
    # 12 numeric claims with source sentences, but only 4 fully conditioned (< half).
    cards = [perf_card(f"C{i}", 0.30) for i in range(4)] + [_underconditioned(f"U{i}") for i in range(8)]
    d = decide_pilot(cards)
    assert d["numeric_claims_with_source"] == 12
    assert d["fully_conditioned"] == 4
    assert d["decision"] == "NO-GO"


def test_second_no_go_message():
    cards = [perf_card(f"C{i}", 0.30) for i in range(3)]
    d = decide_pilot(cards, attempt=2)
    assert d["decision"] == "NO-GO"
    assert "refs 39, 40 only" in d["next_action"]
