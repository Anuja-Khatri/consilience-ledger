"""Consolidation checks (public-record round trees).

1. Every measured-looking number in the new REPORT and SUMMARY files is registered in
   NUMBERS_LOCK.json, where each entry carries its n and qualifier.
2. The superseded median-floor draft fork counts never appear anywhere in the repo
   (consolidation rule 2: they are described in words only, their digits are not printed).
   The banned strings are assembled from fragments so this test file does not match itself.
3. Every JSON file ported into the round and feasibility trees parses.
"""

import glob
import json
import os

from labext.numbers_lock import lint_text

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}


def _report_summary_files():
    files = glob.glob(os.path.join(_REPO, "rounds", "*", "REPORT.md"))
    files += glob.glob(os.path.join(_REPO, "feasibility", "**", "*SUMMARY*.md"), recursive=True)
    return sorted(set(files))


def test_new_reports_exist():
    assert len(_report_summary_files()) >= 4, "expected the round REPORTs and the Route 1 summary"


def test_new_reports_numbers_registered():
    offenders = {}
    for f in _report_summary_files():
        with open(f, encoding="utf-8") as fh:
            bad = sorted(set(lint_text(fh.read())))
        if bad:
            offenders[os.path.relpath(f, _REPO)] = bad
    assert not offenders, f"unregistered numbers (add to NUMBERS_LOCK.json with n): {offenders}"


# superseded median-floor draft fork counts (rule 2); split so this file never matches itself
_BANNED = ["77" + ",523", "6" + ",404"]


def _text_files():
    out = []
    for root, dirs, files in os.walk(_REPO):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
        for fn in files:
            if fn.endswith((".md", ".json", ".py", ".yaml", ".yml", ".txt", ".sql", ".csv")):
                out.append(os.path.join(root, fn))
    return out


def test_banned_superseded_tokens_absent_repo_wide():
    offenders = []
    for f in _text_files():
        try:
            with open(f, encoding="utf-8") as fh:
                t = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        for b in _BANNED:
            if b in t:
                offenders.append((os.path.relpath(f, _REPO), b))
    assert not offenders, f"banned superseded median-floor fork counts found: {offenders}"


def _ported_json_files():
    files = glob.glob(os.path.join(_REPO, "rounds", "**", "*.json"), recursive=True)
    files += glob.glob(os.path.join(_REPO, "feasibility", "**", "*.json"), recursive=True)
    return sorted(set(files))


def test_ported_json_parses():
    bad = []
    for f in _ported_json_files():
        try:
            with open(f, encoding="utf-8") as fh:
                json.load(fh)
        except (json.JSONDecodeError, OSError) as e:
            bad.append((os.path.relpath(f, _REPO), str(e)))
    assert not bad, f"ported JSON failed to parse: {bad}"
    assert _ported_json_files(), "expected ported JSON files under the round/feasibility trees"
