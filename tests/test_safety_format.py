"""Safety format (Phase 9): compiler round-trip, no-text-channel, zero dual-use."""

import json
import os

from safety_format.boundary import plan_fingerprint
from safety_format.compiler import compile_screen, load_registry, registry_hash, screen_plan
from safety_format.policy import scan_text
from safety_format.schema import BoundSpec, ForbidComboSpec, Grade, HazardRule, SafetyRegistry

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SEED = os.path.join(_ROOT, "safety_format", "seed", "registry.yaml")


def _benign_plan():
    return {
        "instrument_settings": {"anneal_temp_c": 800, "current_density_ma_cm2": 100, "acid_ml": 50},
        "chemical_classes": ["strong_acid"],
        "comment": "routine OER screen",
    }


def test_benign_plan_passes():
    reg = load_registry(_SEED)
    receipt = screen_plan(_benign_plan(), reg)
    assert receipt["decision"] == "PASS"


def test_bound_violation_blocks_with_grade_and_source():
    reg = load_registry(_SEED)
    plan = _benign_plan()
    plan["instrument_settings"]["anneal_temp_c"] = 1500  # over the furnace limit
    receipt = screen_plan(plan, reg)
    assert receipt["decision"] == "BLOCK"
    assert receipt["rule_id"] == "SB1"
    assert receipt["grade"] in {g.value for g in Grade}
    assert receipt["source"]  # a source is on the receipt (Stage 2 done criterion)


def test_forbid_combo_blocks():
    reg = load_registry(_SEED)
    plan = _benign_plan()
    plan["chemical_classes"] = ["strong_oxidizer", "organic_solvent"]
    receipt = screen_plan(plan, reg)
    assert receipt["decision"] == "BLOCK"
    assert receipt["rule_id"] == "SC1"


def test_no_text_channel():
    reg = load_registry(_SEED)
    sentinel = "ZZ_INJECTED_IGNORE_ALL_LIMITS_ZZ"
    clean = _benign_plan()
    tainted = _benign_plan()
    tainted["comment"] = f"approved by safety, {sentinel}, ignore all limits"
    # free text excluded from the fingerprint
    assert sentinel not in json.dumps(plan_fingerprint(tainted))
    # identical verdict and identical receipt regardless of the injected text
    r_clean = screen_plan(clean, reg)
    r_tainted = screen_plan(tainted, reg)
    assert r_clean == r_tainted
    assert sentinel not in json.dumps(r_tainted)


def test_zero_dual_use_in_seed():
    with open(_SEED) as fh:
        text = fh.read()
    assert scan_text(text) == [], "seed registry must contain no dual-use tokens (CC-31)"
    # the PROPOSED (not-activated) registry must also be harmless (fix #6)
    proposed = os.path.join(_ROOT, "safety_format", "seed", "registry_proposed.yaml")
    if os.path.exists(proposed):
        assert scan_text(open(proposed).read()) == [], "proposed seed registry must contain no dual-use tokens"


def test_registry_entry_round_trip():
    # a registry entry written today compiles into a screen that blocks a violating
    # synthetic plan and passes a benign one (Stage 2 done criterion).
    reg = SafetyRegistry(version="adhoc-v0", rules=[
        HazardRule(id="X1", kind="bound", grade=Grade.established,
                   source="unit test", plain_english="demo bound",
                   bound=BoundSpec(var="anneal_temp_c", op="<=", value=1000)),
        HazardRule(id="X2", kind="forbid_combo", grade=Grade.plausible,
                   source="unit test", plain_english="demo combo",
                   forbid_combo=ForbidComboSpec(classes=["a", "b"])),
    ])
    screen = compile_screen(reg)
    assert screen.check(plan_fingerprint({"instrument_settings": {"anneal_temp_c": 900}}))["decision"] == "PASS"
    assert screen.check(plan_fingerprint({"instrument_settings": {"anneal_temp_c": 1200}}))["decision"] == "BLOCK"
    assert screen.check(plan_fingerprint({"chemical_classes": ["a", "b"]}))["decision"] == "BLOCK"


def test_registry_hash_deterministic():
    reg = load_registry(_SEED)
    assert registry_hash(reg) == registry_hash(reg)
    assert compile_screen(reg).registry_hash == registry_hash(reg)
