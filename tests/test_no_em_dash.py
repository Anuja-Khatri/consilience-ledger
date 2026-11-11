"""Follow-up correction: no em dash (U+2014) may appear in any top-level .md file, nor under
reports/ or discovery/report/. Plain punctuation only in outgoing docs."""

import glob
import os

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EM_DASH = "—"


def _scoped_md_files():
    files = glob.glob(os.path.join(_REPO, "*.md"))
    files += glob.glob(os.path.join(_REPO, "reports", "*.md"))
    files += glob.glob(os.path.join(_REPO, "discovery", "report", "*.md"))
    return sorted(set(files))


def test_no_em_dash_in_docs():
    offenders = []
    for f in _scoped_md_files():
        with open(f, encoding="utf-8") as fh:
            if _EM_DASH in fh.read():
                offenders.append(os.path.relpath(f, _REPO))
    assert not offenders, f"em dash (U+2014) found in: {offenders}; use plain punctuation"
