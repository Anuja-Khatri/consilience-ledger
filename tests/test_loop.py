"""Stage 3 loop scaffolding (Phase 10): card, translator, dossier, fork table."""

from labext.judge import compare_pair
from labext.loop.card import DiscriminatingPower
from labext.loop.dossier import render_dossier
from labext.loop.fork_table import rows_from_cards, write_table
from labext.loop.generate import generate_card
from labext.loop.translator import card_to_sequence, validate_sequence
from tests.factories import perf_card


def _fork_and_cards():
    a = perf_card("A", 0.30)
    b = perf_card("B", 0.45)  # 150 mV apart -> fork
    fork = compare_pair(a, b)
    assert fork["kind"] == "fork"
    return fork, a, b


def test_card_generation_and_status_ready():
    fork, a, b = _fork_and_cards()
    card = generate_card(fork, a, b)
    assert card.fork_id == fork["pair_id"]
    assert card.status() == "ready"  # cp_chronopotentiometry is an OERSIM capability
    assert card.discriminating_power == DiscriminatingPower.strong  # 150 mV >> floor


def test_translator_produces_valid_pinned_plan():
    fork, a, b = _fork_and_cards()
    seq = card_to_sequence(generate_card(fork, a, b))
    assert validate_sequence(seq) == []
    assert seq["planned_experiments"][0]["experiment_name"] == "OER_discriminate"


def test_plan_only_for_unsimulated_instrument():
    fork, a, b = _fork_and_cards()
    card = generate_card(fork, a, b)
    card.experiment_design.instrument = "synchrotron_xas"  # not an OERSIM capability
    assert card.status() == "plan_only"  # CC-25
    # a plan_only card still compiles to a plan (stops at the gate), no execution
    assert validate_sequence(card_to_sequence(card)) == []


def test_not_scientific_card_does_not_compile():
    fork, a, b = _fork_and_cards()
    card = generate_card(fork, a, b)
    card.falsification = "NONE"
    assert card.status() == "not_scientific"  # CC-26
    try:
        card_to_sequence(card)
        assert False, "not_scientific card must not compile"
    except ValueError:
        pass


def test_dossier_prominently_flags_weak_and_none(tmp_path):
    fork, a, b = _fork_and_cards()
    card = generate_card(fork, a, b)
    card.discriminating_power = DiscriminatingPower.weak
    text = render_dossier(card, fork)
    assert "WEAK DISCRIMINATING POWER" in text  # CC-27 propagated, never dropped
    assert "SIM-NOT-CHEMISTRY" in text


def test_fork_table_csv_json(tmp_path):
    fork, a, b = _fork_and_cards()
    card = generate_card(fork, a, b)
    rows = rows_from_cards([(fork, card)])
    out = write_table(rows, str(tmp_path))
    assert out["n"] == 1
    assert rows[0]["discriminating_power"] in {"strong", "weak"}
    import csv
    with open(out["csv"]) as fh:
        got = list(csv.DictReader(fh))
    assert got[0]["fork_id"] == card.fork_id
