"""Generate JSON Schema (Part IV) from the pydantic models so the two never drift.

Run: python -m labext.gen_schemas   (writes schema/*.json)
"""

from __future__ import annotations

import json
import os

from labext.schema import (
    ClaimCard,
    Conditions,
    Quantity,
    VerdictRecord,
    Defect,
    ComparabilityRules,
)

_SCHEMA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schema"
)

_MODELS = {
    "claim_card_v2.json": ClaimCard,
    "conditions.json": Conditions,
    "quantity.json": Quantity,
    "verdict_record.json": VerdictRecord,
    "defect.json": Defect,
    "comparability_rules.json": ComparabilityRules,
}


def write_all(schema_dir: str = _SCHEMA_DIR) -> list[str]:
    os.makedirs(schema_dir, exist_ok=True)
    written = []
    for fname, model in _MODELS.items():
        schema = model.model_json_schema()
        path = os.path.join(schema_dir, fname)
        with open(path, "w") as fh:
            json.dump(schema, fh, indent=2, sort_keys=True)
            fh.write("\n")
        written.append(path)
    return written


if __name__ == "__main__":
    for p in write_all():
        print(p)
