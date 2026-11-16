"""`make reproduce` must actually rebuild the ledger, and rebuilding it must not
empty the committed writeback verdicts (found in the WP1 fresh-clone check)."""

import json
import os
import re

from labext.ledger import build_ledger
from tests.factories import perf_card

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _phony_targets():
    with open(os.path.join(_REPO, "Makefile")) as fh:
        text = fh.read()
    phony = set()
    for m in re.finditer(r"^\.PHONY:(.*)$", text, re.MULTILINE):
        phony.update(m.group(1).split())
    targets = set(re.findall(r"^([A-Za-z][\w-]*):", text, re.MULTILINE))
    m = re.search(r"^reproduce:(.*)$", text, re.MULTILINE)
    prereqs = m.group(1).split()
    return phony, targets, prereqs


def test_every_make_target_is_phony():
    # "ledger" shares its name with the ledger/ directory; if it is not phony,
    # make reports it up to date and skips the rebuild.
    phony, targets, _ = _phony_targets()
    assert targets - phony == set(), f"targets missing from .PHONY: {sorted(targets - phony)}"


def test_reproduce_rebuilds_ledger_and_checks_output():
    _, _, prereqs = _phony_targets()
    assert "ledger" in prereqs
    assert "check-unchanged" in prereqs
    assert prereqs.index("ledger") < prereqs.index("check-unchanged")


def test_makefile_names_the_env_var_the_code_reads():
    with open(os.path.join(_REPO, "Makefile")) as fh:
        mk = fh.read()
    with open(os.path.join(_REPO, "labext", "writeback.py")) as fh:
        wb = fh.read()
    assert "LILA_OER_DATA_DIR" in wb
    assert re.search(r"LILA_OER_DATA(?!_DIR)", mk) is None


def test_ledger_rebuild_keeps_existing_verdicts(tmp_path):
    led = tmp_path / "ledger"
    led.mkdir()
    existing = [{"verdict_id": "V_X", "outcome": "not_comparable"}]
    (led / "verdicts.json").write_text(json.dumps(existing))
    build_ledger([perf_card("A", 0.3), perf_card("B", 0.4)], ledger_dir=str(led),
                 reports_dir=str(tmp_path / "reports"))
    assert json.loads((led / "verdicts.json").read_text()) == existing


def test_ledger_rebuild_creates_empty_verdicts_when_absent(tmp_path):
    led = tmp_path / "ledger"
    build_ledger([perf_card("A", 0.3), perf_card("B", 0.4)], ledger_dir=str(led),
                 reports_dir=str(tmp_path / "reports"))
    assert json.loads((led / "verdicts.json").read_text()) == []
