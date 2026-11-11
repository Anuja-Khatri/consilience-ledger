"""Fix #7 correction: the durability consistency check (claim 2609.30133__010) must apply the
standing verdict floor (D7: max(13 mV, stated uncertainty)), not a strict every-point-below-0.5-V
rule. Skipped if the authors' released trace is not present at runtime (not committed)."""

import csv
import os

import pytest

# the check must use the SAME floor the writeback verdicts use (locked 2026-11-10), not a new one
from labext.writeback import FLOOR_V

_TRACE = os.path.expanduser(
    "~/consilience for lila/upstream/lila_oer_manuscript/data/fig_3e.csv")
if not os.path.exists(_TRACE):
    _TRACE = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "..", "upstream", "lila_oer_manuscript", "data", "fig_3e.csv")

_CLAIM_THRESHOLD_V = 0.5          # the claim's own stated ceiling ("below 0.5 V")
_CLAIM_UNCERTAINTY_V = 0.0        # claim 2609.30133__010 states no per-value uncertainty


def _inmnpdox_overpotentials():
    with open(_TRACE) as fh:
        return [float(r["overpotential_corrected_avg"])
                for r in csv.DictReader(fh) if r["material_system"] == "InMnPdOx"]


@pytest.mark.skipif(not os.path.exists(_TRACE), reason="authors' H-cell trace not present (runtime data)")
def test_durability_check_applies_the_floor():
    assert FLOOR_V == 0.013                                   # the standing floor, imported not re-defined
    floor = max(FLOOR_V, _CLAIM_UNCERTAINTY_V)               # D7: max(13 mV, stated uncertainty)
    threshold = _CLAIM_THRESHOLD_V + floor                   # 0.513 V
    etas = _inmnpdox_overpotentials()
    assert etas, "InMnPdOx trace not found"
    mx = max(etas)
    # the strict reading (one point above 0.500 V) is real...
    assert sum(1 for e in etas if e > _CLAIM_THRESHOLD_V) >= 1
    # ...but under the floor the verdict is within_floor: no point exceeds 0.513 V
    assert sum(1 for e in etas if e > threshold) == 0
    assert mx <= threshold                                   # within_floor -> consistent within +/-13 mV
