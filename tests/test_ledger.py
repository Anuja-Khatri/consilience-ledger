"""Phase 4 ledger: forks, vetoes, byte-deterministic hash, rendered pages."""

import os

from labext.ledger import build_ledger
from labext.schema import Conditions
from tests.factories import FULL_CONDITIONS, perf_card, stability_card


def _cards():
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.45)  # fork with A (same conditions, 150 mV apart)
    stripped = dict(FULL_CONDITIONS)
    del stripped["electrolyte"]
    c = perf_card("C", 0.30, conditions=stripped)  # veto vs A/B (condition_unstated)
    s = stability_card("S", 100.0)  # axis_mismatch vs the overpotential claims
    return [a, b, c, s]


def test_ledger_buckets_and_reports(tmp_path):
    led = str(tmp_path / "ledger")
    rep = str(tmp_path / "reports")
    summary = build_ledger(_cards(), ledger_dir=led, reports_dir=rep)
    assert summary["n_claims"] == 4
    assert summary["n_forks"] >= 1          # A vs B
    assert summary["n_rejections"] >= 3     # vetoes incl axis_mismatch + condition_unstated
    assert os.path.exists(os.path.join(led, "ledger.hash"))
    assert os.path.exists(os.path.join(rep, "ledger.md"))
    assert os.path.exists(os.path.join(rep, "forks_spotcheck.md"))


def test_ledger_hash_deterministic(tmp_path):
    cards = _cards()
    h1 = build_ledger(cards, ledger_dir=str(tmp_path / "a"), reports_dir=str(tmp_path / "ra"))["ledger_hash"]
    h2 = build_ledger(cards, ledger_dir=str(tmp_path / "b"), reports_dir=str(tmp_path / "rb"))["ledger_hash"]
    assert h1 == h2


def test_real_ledger_present():
    # the committed real ledger exists and is veto-dominated (CC-21/CC-22)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert os.path.exists(os.path.join(repo, "ledger", "ledger.hash"))
    assert os.path.exists(os.path.join(repo, "ledger", "rejections.json"))
