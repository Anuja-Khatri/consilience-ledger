"""Numbers lock (Phase 7): headline numbers are registered; linter flags unregistered."""

from labext.numbers_lock import lint_text, registered_values


def test_headline_numbers_registered():
    vals = registered_values()
    for v in [1.0, 0.9842, 0.25, 13.0, 70.0, 34.0, 561.0, 0.075]:
        assert v in vals, f"{v} must be in the numbers lock"


def test_linter_passes_registered_text():
    assert lint_text("judge agreement 1.0 (n=213); proof coverage 0.9842; floor 13 mV") == []


def test_linter_flags_unregistered_number():
    bad = lint_text("the agreement was 0.999 which is suspicious")
    assert 0.999 in bad


def test_linter_reads_comma_grouped_sample_sizes_whole():
    # "n=140,708" was read as n=140 (WP1); it is one number
    assert lint_text("ingested 140,708 cards (n=140,708)") == []
    assert 123456.0 in lint_text("a sample of n=123,456")


def test_readme_numbers_are_all_registered():
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
    with open(path, encoding="utf-8") as fh:
        assert lint_text(fh.read()) == []
