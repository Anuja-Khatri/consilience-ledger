"""
Determinism Verification

Run the same comparison twice and verify that the content hashes match.
This is the single most persuasive artifact in the repo.
"""

import hashlib
import json


def compute_verdict_hash(verdict: dict) -> str:
    """Compute SHA256 hash of a verdict dict."""
    canonical = json.dumps(verdict, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


def verify_determinism(verdict_1: dict, verdict_2: dict) -> dict:
    """
    Verify that two verdicts from the same inputs are identical.

    Returns:
        dict with hash_1, hash_2, and match (bool)
    """
    hash_1 = compute_verdict_hash(verdict_1)
    hash_2 = compute_verdict_hash(verdict_2)

    return {
        "hash_1": hash_1,
        "hash_2": hash_2,
        "match": hash_1 == hash_2,
        "message": (
            "DETERMINISM VERIFIED: same inputs, same output"
            if hash_1 == hash_2
            else "DETERMINISM FAILED: outputs differ"
        )
    }
