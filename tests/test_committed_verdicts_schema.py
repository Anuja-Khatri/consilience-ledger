"""Every committed verdict file validates against the repository's own JSON Schema.

Found in the WP1 readiness review: the nine committed writeback verdicts did not
validate against schema/verdict_record.json (the schema described a planned record
shape that writeback never wrote), and the pair verdicts had no schema at all.
"""

import glob
import json
import os

import jsonschema
import pytest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _schema(name):
    with open(os.path.join(_REPO, "schema", name)) as fh:
        return json.load(fh)


def _records(path):
    with open(path) as fh:
        return json.load(fh)


PAIR_FILES = ["rejections.json", "forks.json", "corroborations.json", "correspondences.json"]


def test_writeback_verdicts_validate():
    schema = _schema("verdict_record.json")
    records = _records(os.path.join(_REPO, "ledger", "verdicts.json"))
    assert records, "committed verdicts.json is empty"
    for r in records:
        jsonschema.validate(r, schema)


@pytest.mark.parametrize("fname", PAIR_FILES)
def test_pair_verdicts_validate(fname):
    schema = _schema("pair_verdict_record.json")
    for r in _records(os.path.join(_REPO, "ledger", fname)):
        jsonschema.validate(r, schema)


def test_every_committed_ledger_record_file_is_covered():
    covered = set(PAIR_FILES) | {"verdicts.json", "claims.json"}
    on_disk = {os.path.basename(p) for p in glob.glob(os.path.join(_REPO, "ledger", "*.json"))}
    assert on_disk <= covered, f"ledger files with no schema test: {sorted(on_disk - covered)}"


def test_claims_validate():
    schema = _schema("claim_card_v2.json")
    for r in _records(os.path.join(_REPO, "ledger", "claims.json")):
        jsonschema.validate(r, schema)


def test_schema_rejects_an_extra_field():
    schema = _schema("verdict_record.json")
    rec = dict(_records(os.path.join(_REPO, "ledger", "verdicts.json"))[0])
    rec["unexpected"] = 1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(rec, schema)


def test_freshly_judged_records_of_every_kind_validate():
    from labext.judge import compare_pair
    from tests.factories import perf_card, stability_card

    schema = _schema("pair_verdict_record.json")
    recs = [
        compare_pair(perf_card("A", 0.30), perf_card("B", 0.45)),             # fork
        compare_pair(perf_card("A", 0.30), perf_card("B", 0.305)),            # within_floor
        compare_pair(perf_card("A", 0.30), stability_card("S", 100.0)),       # axis_mismatch
        compare_pair(perf_card("A", float("nan")), perf_card("B", 0.30)),     # quantity_refused
    ]
    assert {r["outcome"] for r in recs} >= {"fork", "within_floor", "axis_mismatch", "not_comparable"}
    for r in recs:
        jsonschema.validate(r, schema)
