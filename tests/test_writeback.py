"""Phase 5 writeback: verdicts under D7; screening-tier/no-data failures are vetoes."""

from labext.schema import Conditions, Quantity
from labext.writeback import compute_verdicts, parse_elements
from tests.factories import FULL_CONDITIONS, perf_card

_CSV = (
    "composition,target_elements,anneal_T,overpotential_cp1_600s_mean,xrf_total_molar_change\n"
    "\"{'In':0.3,'Mn':0.3,'Pd':0.4}\",\"['In', 'Mn', 'Pd']\",400.0,0.450,0.1\n"
    "\"{'In':0.2,'Mn':0.3,'Pd':0.5}\",\"['In', 'Mn', 'Pd']\",400.0,0.470,0.1\n"
)


def _data(tmp_path):
    p = tmp_path / "oer_exp_data.csv"
    p.write_text(_CSV)
    return str(p)


def test_parse_elements():
    assert parse_elements("InMnPdOx") == frozenset({"In", "Mn", "Pd"})
    assert parse_elements("Pd-55") == frozenset({"Pd"})


def test_inmnpdox_within_floor(tmp_path):
    card = perf_card("2609.30133__003", 0.45)
    card.subject = "InMnPdOx"
    v = compute_verdicts([card], _data(tmp_path))["verdicts"]
    assert len(v) == 1
    assert v[0]["outcome"] == "within_floor"   # 0.45 vs measured best 0.45
    assert v[0]["data_source"]["sha256"]
    assert v[0]["data_source"]["row_refs"]       # cited by row index (CC-28)


def test_published_pure_pd_is_not_comparable(tmp_path):
    card = perf_card("ref40_022", 0.196)
    card.subject = "Pd-55"
    v = compute_verdicts([card], _data(tmp_path))["verdicts"]
    assert v[0]["outcome"] == "not_comparable"   # no pure-Pd rows -> published veto
    assert v[0]["data_source"]["row_refs"] == []


def test_contradicted_when_over_floor(tmp_path):
    card = perf_card("x", 0.52)  # 70 mV above measured best 0.45
    card.subject = "InMnPdOx"
    v = compute_verdicts([card], _data(tmp_path))["verdicts"]
    assert v[0]["outcome"] == "contradicted"
