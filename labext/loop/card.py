"""Experiment card (feature 17), ported from miu-demo EXPERIMENT_SPEC.md.

Hard rules kept: real instruments only, falsification or explicit NONE, cost tier,
timeline, weak-discriminating-power flag. Fixes over the miu version:
- ``discriminating_power`` is an explicit enum field (CC-27), not prose in falsification.
- ``instrument_exists`` is checked against the OERSIM capability list before compilation;
  a card needing an unsimulated instrument stops at plan+gate with status ``plan_only``
  (CC-25). A card with falsification NONE is ``not_scientific`` and never compiles (CC-26).
"""

from __future__ import annotations

from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, model_validator

# Instruments OERSIM can simulate (from lab-gate sim_ext/oersim.py capability list).
OERSIM_CAPABILITIES = {"cp_chronopotentiometry", "chronopotentiometry", "oersim"}


class CostTier(str, Enum):
    k10 = "$10K"
    k100 = "$100K"
    m1 = "$1M"
    m10 = "$10M+"


class DiscriminatingPower(str, Enum):
    strong = "strong"
    weak = "weak"


class ExperimentDesign(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hypothesis: str
    manipulated_variable: str
    discriminating_observable: str
    instrument: str
    instrument_exists: bool
    instrument_source: str
    protocol_sketch: str
    predicted_outcome_if_match_holds: str
    predicted_outcome_if_match_fails: str
    control_conditions: str


class ExperimentCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str
    fork_id: str
    title: str
    claim_a: str
    claim_b: str
    claim_a_source_sentence: str
    claim_b_source_sentence: str
    structural_bridge: str
    experiment_design: ExperimentDesign
    falsification: str  # a concrete falsifier, or the literal "NONE" (CC-26)
    discriminating_power: DiscriminatingPower  # explicit (CC-27)
    who_could_run_this: str
    estimated_cost: CostTier
    estimated_timeline: str
    sources_bridged: list[str]
    value_to_lab: str

    @model_validator(mode="after")
    def _hard_rules(self) -> "ExperimentCard":
        if not self.falsification.strip():
            raise ValueError("falsification must be a concrete falsifier or the literal NONE")
        return self

    @property
    def is_scientific(self) -> bool:
        return self.falsification.strip().upper() != "NONE"

    def status(self) -> str:
        """ready (compiles), plan_only (unsimulated instrument, CC-25), or not_scientific (CC-26)."""
        if not self.is_scientific:
            return "not_scientific"
        instr = self.experiment_design.instrument.strip().casefold()
        if not self.experiment_design.instrument_exists or instr not in OERSIM_CAPABILITIES:
            return "plan_only"
        return "ready"


__all__ = ["CostTier", "DiscriminatingPower", "ExperimentDesign", "ExperimentCard",
           "OERSIM_CAPABILITIES"]
