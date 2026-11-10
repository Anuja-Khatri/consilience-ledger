"""D6 pilot GO/NO-GO rule, applied autonomously. Never soften a rule to pass.

Pilot = refs 39, 40, 42 (or the next accessible performance paper if 42 is out).
GO if at least 10 approvable numeric performance/stability claims have exact source
sentences AND at least half of those explicitly state electrolyte identity, current
density, and iR-correction status.
First NO-GO: shrink to the Pd neighborhood (their paper + refs 39, 40, 11, 12) and
re-pilot once. Second NO-GO: their paper + refs 39, 40 only, limitation recorded.
"""

from __future__ import annotations

from labext.schema import ClaimCard, QUANTITY_KINDS, UNSTATED

MIN_CLAIMS = 10


def _has_source_sentence(c: ClaimCard) -> bool:
    return bool(c.source_sentence and c.source_sentence.strip())


def _is_numeric_claim(c: ClaimCard) -> bool:
    return c.claim_kind in QUANTITY_KINDS and c.quantity is not None


def _fully_conditioned(c: ClaimCard) -> bool:
    cond = c.conditions
    electrolyte_ok = cond.electrolyte != UNSTATED and getattr(cond.electrolyte, "identity", None)
    current_ok = cond.current_density != UNSTATED
    ir_ok = cond.ir_correction != UNSTATED  # True or False both count as stated
    return bool(electrolyte_ok and current_ok and ir_ok)


def decide_pilot(approved_cards: list[ClaimCard], attempt: int = 1) -> dict:
    numeric = [c for c in approved_cards if _is_numeric_claim(c) and _has_source_sentence(c)]
    fully = [c for c in numeric if _fully_conditioned(c)]
    n, f = len(numeric), len(fully)
    go = n >= MIN_CLAIMS and f >= (n / 2)

    if go:
        next_action = "proceed to full corpus extraction (Phase 3)"
    elif attempt == 1:
        next_action = "NO-GO: shrink to Pd neighborhood (their paper + refs 39, 40, 11, 12), re-pilot once"
    else:
        next_action = "NO-GO: corpus = their paper + refs 39, 40 only; record the limitation prominently"

    return {
        "decision": "GO" if go else "NO-GO",
        "attempt": attempt,
        "numeric_claims_with_source": n,
        "fully_conditioned": f,
        "min_required": MIN_CLAIMS,
        "half_required": round(n / 2, 1),
        "next_action": next_action,
    }
