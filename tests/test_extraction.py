"""Dual-model extraction, agreement gate, review queue (Phase 2, mock-driven)."""

import os

from labext.extraction.backends import (
    AnthropicBackend,
    MissingKeyError,
    MockBackend,
    select_backends,
)
from labext.extraction.cache import JsonlCache
from labext.extraction.pipeline import run_paper


def _card(claim_id, subject, overpotential, *, ir_correction=True, cd_value=10.0,
          sentence="RuO2 shows 0.30 V at 10 mA/cm2 in 0.5 M H2SO4 iR-corrected."):
    return {
        "claim_id": claim_id,
        "claim_kind": "performance_value",
        "commitment_direction": "asserts",
        "causal_direction": "independent",
        "physical_scale": "molecular",
        "measurability": "measurable_now",
        "measurable_with": "cp_chronopotentiometry",
        "subject": subject,
        "relation": "has_overpotential",
        "object": "overpotential",
        "domain": "materials_oer",
        "source_sentence": sentence,
        "source_document": "paperP",
        "provenance_hash": f"h_{claim_id}",
        "axis": "overpotential_at_current_density",
        "quantity": {"value": overpotential, "unit": "V", "uncertainty": None,
                     "uncertainty_kind": "none_stated", "bound": "exact"},
        "conditions": {
            "electrolyte": {"identity": "H2SO4", "concentration": {"value": 0.5, "unit": "mol/L"}},
            "ph": "unstated",
            "current_density": {"value": cd_value, "unit": "mA/cm^2", "normalization": "geometric"},
            "temperature": {"value": 25.0, "unit": "degC"},
            "loading": "unstated", "substrate": "unstated", "protocol_tier": "unstated",
            "prior_operation_duration": "unstated", "anneal_temperature": "unstated",
            "ir_correction": ir_correction,
        },
    }


PAPER = "paperP body text"


def _backends():
    # C1 agrees across models (0.30 V); C2 disagrees (ir_correction True vs False).
    a = MockBackend("model-A", {PAPER: [
        _card("A1", "IrO2", 0.30, sentence="IrO2 shows 0.30 V."),
        _card("A2", "RuO2", 0.40, ir_correction=True),
    ]})
    b = MockBackend("model-B", {PAPER: [
        _card("B1", "IrO2", 0.30, sentence="IrO2 shows 0.30 V."),
        _card("B2", "RuO2", 0.40, ir_correction=False),
    ]})
    return a, b


def test_agreement_and_contested(tmp_path):
    a, b = _backends()
    cache = JsonlCache(str(tmp_path / "runs"))
    res = run_paper(PAPER, PAPER, [a, b], cache,
                    str(tmp_path / "approved"), str(tmp_path / "review"))
    assert res["counts"]["approved"] == 1       # the IrO2 claim agreed
    assert res["counts"]["contested"] == 1       # the RuO2 iR-correction disagreement
    assert res["approved"][0]["subject"] == "IrO2"
    assert len(res["review_paths"]) == 1
    assert os.path.exists(res["review_paths"][0])
    assert os.path.exists(res["approved_path"])


def test_cache_is_resumable(tmp_path):
    a, b = _backends()
    cache = JsonlCache(str(tmp_path / "runs"))
    run_paper(PAPER, PAPER, [a, b], cache, str(tmp_path / "ap"), str(tmp_path / "rv"))
    run_paper(PAPER, PAPER, [a, b], cache, str(tmp_path / "ap"), str(tmp_path / "rv"))
    assert a.calls == 1 and b.calls == 1  # second run served from cache


def test_missing_key_raises_and_select_empty(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert select_backends() == []
    try:
        AnthropicBackend("claude-sonnet-4-6").extract("x")
        assert False, "expected MissingKeyError"
    except MissingKeyError:
        pass


def test_parser_salvages_truncated_json():
    from labext.extraction.backends import _parse_cards
    # a reply truncated mid-second-object (max_tokens cutoff) must not raise
    s = '[{"claim_id":"A","x":1}, {"claim_id":"B","source_sentence":"cut off here'
    cards = _parse_cards(s)
    assert [c["claim_id"] for c in cards] == ["A"]
    assert _parse_cards("no json at all") == []
    assert _parse_cards('```json\n[{"claim_id":"C"}]\n```')[0]["claim_id"] == "C"


def test_unparseable_card_is_parked(tmp_path):
    a = MockBackend("model-A", {PAPER: [_card("A1", "IrO2", 0.30), {"garbage": True}]})
    b = MockBackend("model-B", {PAPER: [_card("B1", "IrO2", 0.30)]})
    cache = JsonlCache(str(tmp_path / "runs"))
    res = run_paper(PAPER, PAPER, [a, b], cache, str(tmp_path / "ap"), str(tmp_path / "rv"))
    assert res["counts"]["parked"] == 1
    assert res["counts"]["approved"] == 1
