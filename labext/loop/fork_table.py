"""Machine-readable fork candidate table (feature 22): csv + json.

Columns: fork_id, axis, discriminating_power, predicted_split, instrument, cost_tier.
The weak-discriminating-power flag is propagated here from the card, never dropped
(CC-27). The csv loads in pandas.
"""

from __future__ import annotations

import csv
import json
import os

COLUMNS = ["fork_id", "axis", "discriminating_power", "predicted_split", "instrument", "cost_tier"]


def rows_from_cards(cards) -> list[dict]:
    """cards: list of (fork_record, ExperimentCard)."""
    rows = []
    for fork, card in cards:
        rows.append({
            "fork_id": card.fork_id,
            "axis": fork.get("axis"),
            "discriminating_power": card.discriminating_power.value,
            "predicted_split": fork.get("margin"),
            "instrument": card.experiment_design.instrument,
            "cost_tier": card.estimated_cost.value,
        })
    return rows


def write_table(rows: list[dict], out_dir: str, stem: str = "fork_candidates") -> dict:
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, stem + ".csv")
    json_path = os.path.join(out_dir, stem + ".json")
    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in COLUMNS})
    with open(json_path, "w") as fh:
        json.dump(rows, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return {"csv": csv_path, "json": json_path, "n": len(rows)}


__all__ = ["COLUMNS", "rows_from_cards", "write_table"]
