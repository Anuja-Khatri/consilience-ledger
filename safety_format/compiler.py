"""Rules-to-screen compiler (feature 16).

Compiles a graded safety registry into a Screen. The screen consumes a TYPED plan
fingerprint (see boundary.py) and a registry, and emits a receipt with a decision
(PASS or BLOCK) plus, on a block, the firing rule id, its grade, and its source.
No free text ever enters the screen, so the no-text-channel property holds by
construction. The receipt carries the registry hash so a verdict is attributable to
an exact policy (mirrors lab-gate's certificates).
"""

from __future__ import annotations

import hashlib
import json
import operator

import yaml

from safety_format.boundary import plan_fingerprint
from safety_format.schema import SafetyRegistry

_OPS = {
    "<=": operator.le, ">=": operator.ge, "<": operator.lt,
    ">": operator.gt, "==": operator.eq, "!=": operator.ne,
}


def load_registry(path: str) -> SafetyRegistry:
    with open(path, "r") as fh:
        return SafetyRegistry.model_validate(yaml.safe_load(fh))


def registry_hash(registry: SafetyRegistry) -> str:
    d = registry.model_dump(mode="json")
    d["rules"] = sorted(d["rules"], key=lambda r: r["id"])
    canonical = json.dumps(d, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


class Screen:
    def __init__(self, registry: SafetyRegistry):
        self.registry = registry
        self.registry_hash = registry_hash(registry)

    def check(self, fingerprint: dict) -> dict:
        """Return a receipt. BLOCK on the first firing rule, else PASS."""
        plan_hash = hashlib.sha256(
            json.dumps(fingerprint, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        settings = fingerprint.get("instrument_settings", {})
        classes = set(fingerprint.get("chemical_classes", []))

        for rule in sorted(self.registry.rules, key=lambda r: r.id):
            fired = False
            reason = ""
            if rule.kind == "bound":
                var = rule.bound.var
                if var in settings:  # not applicable if the plan does not set this var
                    ok = _OPS[rule.bound.op](settings[var], rule.bound.value)
                    if not ok:
                        fired = True
                        reason = f"{var}={settings[var]} violates {var} {rule.bound.op} {rule.bound.value}"
            elif rule.kind == "forbid_combo":
                needed = {c.strip().casefold() for c in rule.forbid_combo.classes}
                if needed <= classes:
                    fired = True
                    reason = f"incompatible classes present together: {sorted(needed)}"
            if fired:
                return {
                    "decision": "BLOCK",
                    "rule_id": rule.id,
                    "grade": rule.grade.value,
                    "source": rule.source,
                    "reason": reason,
                    "plan_hash": plan_hash,
                    "registry_hash": self.registry_hash,
                }
        return {
            "decision": "PASS",
            "rule_id": None,
            "grade": None,
            "source": None,
            "reason": "no safety rule fired",
            "plan_hash": plan_hash,
            "registry_hash": self.registry_hash,
        }


def compile_screen(registry: SafetyRegistry) -> Screen:
    return Screen(registry)


def screen_plan(raw_plan: dict, registry: SafetyRegistry) -> dict:
    """Full path: raw plan -> typed fingerprint (free text quarantined) -> screen receipt."""
    return compile_screen(registry).check(plan_fingerprint(raw_plan))


__all__ = ["load_registry", "registry_hash", "Screen", "compile_screen", "screen_plan"]
