"""Phase 10: the loop runs end to end on real OERSIM (skipped if the dataset is absent)."""

import glob
import json
import os

import pytest

_DS = os.environ.get(
    "HELAO_DATASET",
    os.path.expanduser("~/lila-gate/helao-async/helao/deploy/test/demos/data/oer13_cps.pzstd"),
)
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.skipif(not os.path.exists(_DS), reason="oer13_cps dataset not present")
def test_loop_end_to_end():
    from labext.loop.run_loop import run_loop
    r = run_loop()
    assert r["forks_run"] == 2 and r["plan_only"] == 1
    outcomes = {s["outcome"] for s in r["summaries"]}
    assert "fork_confirmed" in outcomes  # at least one fork resolved by OERSIM
    assert "plan_only" in outcomes       # CC-25 honored
    # every committed run trace is labeled SYNTHETIC with the SIM-NOT-CHEMISTRY disclaimer
    traces = glob.glob(os.path.join(_REPO, "loop", "runs", "*.json"))
    assert traces
    for f in traces:
        t = json.load(open(f))
        assert t.get("SYNTHETIC") is True
        assert "SIM-NOT-CHEMISTRY" in t.get("disclaimer", "")


def test_card_status_plan_only_and_not_scientific_unit():
    # unit coverage that does not need the dataset
    from labext.loop.card import DiscriminatingPower
    from labext.loop.generate import generate_card
    from tests.factories import perf_card
    from labext.judge import compare_pair
    a, b = perf_card("A", 0.30), perf_card("B", 0.50)
    fork = compare_pair(a, b)
    card = generate_card(fork, a, b)
    card.experiment_design.instrument = "tem"  # not OERSIM
    assert card.status() == "plan_only"
