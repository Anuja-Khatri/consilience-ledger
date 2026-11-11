"""Numbers lock (Phase 7). Ported pattern from consilience-verification.

Any headline number cited in outgoing text must appear in NUMBERS_LOCK.json, each with
its n and qualifier (II.3). `lint_text` scans a piece of text for measured-looking
numbers (decimals, percentages, "n=NN", "NN mV") and returns those not in the registry
and not matching the structural allowlist (phase tags, years, versions, pint exponents).
"""

from __future__ import annotations

import json
import os
import re

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOCK = os.path.join(_REPO, "NUMBERS_LOCK.json")


def registry() -> list[dict]:
    return json.load(open(_LOCK))["numbers"]


def registered_values() -> set:
    return {float(e["value"]) for e in registry()}


def add_number(id: str, value, n=None, qualifier: str = "", source: str = "") -> None:
    data = json.load(open(_LOCK))
    if not any(e["id"] == id for e in data["numbers"]):
        data["numbers"].append({"id": id, "value": value, "n": n, "qualifier": qualifier, "source": source})
        json.dump(data, open(_LOCK, "w"), indent=2)
        open(_LOCK, "a").write("\n")


# structural numbers that are not measured values
_ALLOW = re.compile(r"""
    ^(19|20)\d\d$        # years
  | ^v?\d+(\.\d+)?$      # bare version-like
""", re.VERBOSE)
_NUM = re.compile(r"(?<![\w.])\d+\.\d+(?![\w])|(?<![\w])n=\d+|(?<![\w.])\d+\s*mV")


def _as_floats(text: str) -> list[float]:
    # Extract measured-looking numbers as whole tokens: decimals, n=NN, and an integer
    # directly before mV. The negative lookbehind on the mV match stops a decimal like
    # "90.7 mV" from also yielding a spurious "7" (the ".7" is part of the decimal above).
    out = []
    for m in re.findall(r"(?<![\d.])\d+\.\d+", text):
        out.append(float(m))
    for m in re.findall(r"n=(\d+)", text):
        out.append(float(m))
    for m in re.findall(r"(?<![\d.])(\d+)\s*mV", text):
        out.append(float(m))
    return out


def lint_text(text: str) -> list[float]:
    """Return decimal/n=/mV numbers in text that are not in the registry."""
    allowed = registered_values()
    allowed |= {float(e["n"]) for e in registry() if e.get("n") is not None}  # sample sizes
    allowed |= {4.1, 4.8, 5.0, 3.11, 2.0, 0.1}  # model/version/structural decimals
    bad = []
    for v in _as_floats(text):
        if v not in allowed and not (v.is_integer() and 1900 <= v <= 2100):
            bad.append(v)
    return bad


__all__ = ["registry", "registered_values", "add_number", "lint_text"]
