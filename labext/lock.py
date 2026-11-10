"""Hash-lock for the comparability rules (spec IV.2: rules.lock).

The hash is taken over the normalised, id-sorted rules (via the pydantic model),
so it is independent of YAML key order and whitespace. Pattern ported from
lab-gate ``gate/registry/lock.py``. No timestamp is stored, so the lock is stable
and ``make reproduce`` stays byte-identical.
"""

from __future__ import annotations

import hashlib
import json
import os

from labext.comparability import load_rules

_RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "rules",
    "comparability_rules.yaml",
)
_LOCK_PATH = os.path.join(os.path.dirname(_RULES_PATH), "rules.lock")


def canonical_rules_dict(rules) -> dict:
    d = rules.model_dump(mode="json")
    d["rules"] = sorted(d["rules"], key=lambda r: r["id"])
    return d


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def rules_hash(path: str = _RULES_PATH) -> str:
    rules = load_rules(path)
    return hashlib.sha256(canonical_json(canonical_rules_dict(rules)).encode()).hexdigest()


def write_lock(rules_path: str = _RULES_PATH, lock_path: str = _LOCK_PATH) -> dict:
    rules = load_rules(rules_path)
    lock = {"version": rules.version, "sha256": rules_hash(rules_path)}
    with open(lock_path, "w") as fh:
        json.dump(lock, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return lock


if __name__ == "__main__":
    print(write_lock())
