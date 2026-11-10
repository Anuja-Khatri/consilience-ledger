"""Plan boundary: produce a TYPED fingerprint with no text channel (feature 15).

A raw plan may carry free-text fields (comments, labels, notes). The fingerprint keeps
only typed, numeric instrument settings and the declared chemical classes. Free text is
quarantined and never reaches the screen, so no prose in a plan can change a verdict.
Mirrors lab-gate's no-text-channel boundary.
"""

from __future__ import annotations

FREE_TEXT_FIELDS = {"comment", "note", "label", "description", "notes", "rationale"}


def plan_fingerprint(raw_plan: dict) -> dict:
    """Typed-only view of a plan. Numeric settings + sorted chemical classes."""
    settings_in = raw_plan.get("instrument_settings") or {}
    settings = {
        k: v for k, v in settings_in.items()
        if isinstance(v, (int, float)) and not isinstance(v, bool)
    }
    classes = sorted({str(c).strip().casefold() for c in (raw_plan.get("chemical_classes") or [])})
    return {"instrument_settings": dict(sorted(settings.items())), "chemical_classes": classes}


def quarantined_text(raw_plan: dict) -> list[str]:
    """Collect every free-text value set aside at the boundary (not dropped silently)."""
    out = []
    for k, v in raw_plan.items():
        if k in FREE_TEXT_FIELDS and isinstance(v, str):
            out.append(v)
    for action in raw_plan.get("actions") or []:
        if isinstance(action, dict):
            for k, v in action.items():
                if k in FREE_TEXT_FIELDS and isinstance(v, str):
                    out.append(v)
    return out


__all__ = ["FREE_TEXT_FIELDS", "plan_fingerprint", "quarantined_text"]
