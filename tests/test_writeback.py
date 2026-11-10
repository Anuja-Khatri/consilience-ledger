"""Phase 5 writeback: verdicts use H-cell data; screening-tier/unstated -> published veto."""

from labext.writeback import compute_verdicts, parse_elements
from tests.factories import FULL_CONDITIONS, perf_card

_HCELL = (  # fig_3e.csv: iR-corrected long-term H-cell overpotential (InMnPdOx only)
    "material_system,plot_x_hr,has_blue_marker,overpotential_corrected_avg\n"
    "InMnPdOx,1.0,False,0.410\nInMnPdOx,2.0,False,0.420\n"
)
_SCREEN = (  # oer_exp_data.csv: CP1 600s screening (has the Co-Fe-Zr system)
    "composition,target_elements,anneal_T,overpotential_cp1_600s_mean,xrf_total_molar_change\n"
    "\"{'Co':0.8,'Fe':0.1,'Zr':0.1}\",\"['Co', 'Fe', 'Zr']\",400.0,0.537,0.1\n"
)


def _dir(tmp_path):
    (tmp_path / "fig_3e.csv").write_text(_HCELL)
    (tmp_path / "oer_exp_data.csv").write_text(_SCREEN)
    return str(tmp_path)


def test_parse_elements():
    assert parse_elements("InMnPdOx") == frozenset({"In", "Mn", "Pd"})
    assert parse_elements("Pd-55") == frozenset({"Pd"})


def test_cofezr_has_no_hcell_data_is_veto(tmp_path):
    card = perf_card("2609.30133__020", 0.55)
    card.subject = "CoFeZrOx"
    v = compute_verdicts([card], _dir(tmp_path))["verdicts"][0]
    assert v["outcome"] == "not_comparable"             # reclassified from the screening-tier contradiction
    assert v["defects"][0]["defect_type"] == "no_hcell_data"
    assert v["data_source"]["screening_row_refs"]        # the screening basis is recorded, not used as a verdict


def test_hcell_system_vetoes_on_unstated_electrolyte(tmp_path):
    # even with H-cell data for the system, the H-cell electrolyte is not in the file
    card = perf_card("2609.30133__003", 0.45)
    card.subject = "InMnPdOx"  # FULL_CONDITIONS states electrolyte/cd/temp; H-cell has none
    v = compute_verdicts([card], _dir(tmp_path))["verdicts"][0]
    assert v["outcome"] == "not_comparable"
    types = {d["defect_type"] for d in v["defects"]}
    assert "condition_unstated" in types                 # electrolyte/cd not in the H-cell file (never inferred)


def test_ir_mismatch_is_veto(tmp_path):
    cond = dict(FULL_CONDITIONS)
    cond["ir_correction"] = False  # claim not iR-corrected; H-cell is iR-corrected
    card = perf_card("x", 0.41, conditions=cond)
    card.subject = "InMnPdOx"
    v = compute_verdicts([card], _dir(tmp_path))["verdicts"][0]
    assert v["outcome"] == "not_comparable"
    assert any(d["defect_type"] == "condition_mismatch" and d["target"] == "CR4" for d in v["defects"])


def test_no_confirm_or_contradict_from_screening(tmp_path):
    # no verdict is ever confirmed/contradicted off the screening data
    cards = [perf_card("c", 0.55, conditions={**FULL_CONDITIONS, "ir_correction": False})]
    cards[0].subject = "CoFeZrOx"
    outs = {v["outcome"] for v in compute_verdicts(cards, _dir(tmp_path))["verdicts"]}
    assert outs <= {"not_comparable"}
