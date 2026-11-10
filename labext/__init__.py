"""Consilience Lab Extension: materials-OER claim comparison on the deterministic judge.

The pipeline from APPROVED CLAIM CARDS onward is byte-deterministic (spec D4).
Extraction (Phase 2+) is NOT claimed deterministic; it is gated.
"""

CODE_VERSION = "lab-extension-0.1.0"
"""Bumped when judge/comparability logic changes. Enters ledger.hash (spec IV.5)."""
