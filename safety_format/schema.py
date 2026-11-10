"""Graded, claims-backed safety registry format (features 13-14).

Mirrors the lab-gate invariants house style (bound / forbid_combo with a typed spec),
and adds a grade and a source to every rule. The grade ladder is their own job ads'
ladder: established, plausible, weakly supported.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, model_validator


class Grade(str, Enum):
    established = "established"
    plausible = "plausible"
    weakly_supported = "weakly_supported"


class BoundSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    var: str  # a fingerprint variable, e.g. anneal_temp_c
    op: Literal["<=", ">=", "<", ">", "==", "!="]
    value: float


class ForbidComboSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    classes: list[str]  # block if ALL of these chemical classes are present together


class HazardRule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    kind: Literal["bound", "forbid_combo"]
    grade: Grade
    source: str
    plain_english: str
    bound: Optional[BoundSpec] = None
    forbid_combo: Optional[ForbidComboSpec] = None

    @model_validator(mode="after")
    def _spec_matches_kind(self) -> "HazardRule":
        if self.kind == "bound" and self.bound is None:
            raise ValueError(f"rule {self.id}: kind=bound requires a 'bound' spec")
        if self.kind == "forbid_combo" and self.forbid_combo is None:
            raise ValueError(f"rule {self.id}: kind=forbid_combo requires a 'forbid_combo' spec")
        return self


class SafetyRegistry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    rules: list[HazardRule]


__all__ = ["Grade", "BoundSpec", "ForbidComboSpec", "HazardRule", "SafetyRegistry"]
