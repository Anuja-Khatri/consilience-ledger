"""Split a paper into candidate passages for extraction.

Only passages carrying an OER performance/stability/condition signal are kept, and the
count is capped (recorded). This mirrors the demo's candidate pre-filter: most numeric
claims and their conditions live in a minority of sentences and in tables.
"""

from __future__ import annotations

import re

SIGNAL = re.compile(
    r"overpotential|\bmV\b|mA\s*/?\s*cm|A\s*/?\s*cm|tafel|dissolution|stabilit|"
    r"current density|iR[- ]?correct|H2SO4|HClO4|\bRHE\b|retention|degrad|"
    r"η|eta\b|chronopotentiom|hours|durab",
    re.I,
)


def paper_windows(text: str, size: int = 1600, overlap: int = 200, max_windows: int = 40) -> list[str]:
    """Return up to max_windows signal-bearing passages covering the paper."""
    text = re.sub(r"[ \t]+", " ", text)
    windows = []
    step = max(size - overlap, 1)
    for start in range(0, len(text), step):
        chunk = text[start : start + size].strip()
        if len(chunk) < 120:
            continue
        if SIGNAL.search(chunk):
            windows.append(chunk)
        if len(windows) >= max_windows:
            break
    return windows
