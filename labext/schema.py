"""Part IV data contracts as pydantic v2 models.

Claim Card v2 (IV.1) extends the engine v1 card with ``quantity``, a ten-key
``conditions`` block, an ``axis`` id, and the materials ``claim_kind`` additions.
Rejection defects (IV.3), the verdict record (IV.4), and the comparability rules
format (IV.2) are modelled here too. JSON Schema is generated from these models
(see ``labext.gen_schemas``) so the two never drift.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator


# --------------------------------------------------------------------------- #
# Enums
# --------------------------------------------------------------------------- #
class ClaimKind(str, Enum):
    # engine v1 kinds (kept)
    location = "location"
    timing = "timing"
    architecture = "architecture"
    mechanism = "mechanism"
    computability = "computability"
    substrate = "substrate"
    measurement = "measurement"
    scale = "scale"
    boundary = "boundary"
    # materials additions (IV.1)
    performance_value = "performance_value"
    stability_value = "stability_value"
    synthesis_claim = "synthesis_claim"


QUANTITY_KINDS = {ClaimKind.performance_value, ClaimKind.stability_value}


class CommitmentDirection(str, Enum):
    asserts = "asserts"
    denies = "denies"


class CausalDirection(str, Enum):
    causes = "causes"
    caused_by = "caused_by"
    bidirectional = "bidirectional"
    independent = "independent"


class Measurability(str, Enum):
    measurable_now = "measurable_now"
    measurable_under_assumption = "measurable_under_assumption"
    not_measurable = "not_measurable"


class DefectType(str, Enum):
    # engine enum (judge/schema/rejection.json)
    type_mismatch = "type_mismatch"
    direction_mismatch = "direction_mismatch"
    vocabulary_dependence = "vocabulary_dependence"
    provenance_circularity = "provenance_circularity"
    insufficient_coverage = "insufficient_coverage"
    # lab-extension additions (IV.3)
    condition_mismatch = "condition_mismatch"
    condition_unstated = "condition_unstated"
    axis_mismatch = "axis_mismatch"


# --------------------------------------------------------------------------- #
# Quantity + condition value types
# --------------------------------------------------------------------------- #
UNSTATED = "unstated"


class Concentration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float
    unit: str


class Electrolyte(BaseModel):
    model_config = ConfigDict(extra="forbid")
    identity: str
    concentration: Union[Concentration, Literal["unstated"]] = UNSTATED


class CurrentDensity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float
    unit: str = "mA/cm^2"
    # CC-06: ECSA- vs geometric-normalised current density must match to compare.
    normalization: Literal["geometric", "ecsa", "unstated"] = "unstated"


class TempValue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float
    unit: str = "degC"


class Loading(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float
    unit: str  # umol/cm^2 or mg/cm^2


class DurationValue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float
    unit: str = "h"


class AnnealValue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float
    unit: str = "degC"


class Quantity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float
    unit: str
    uncertainty: Optional[float] = None
    uncertainty_kind: Literal["stated_sd", "stated_range", "none_stated"] = "none_stated"
    bound: Literal["exact", "upper", "lower", "approx"] = "exact"


class Conditions(BaseModel):
    """Exactly ten keys (IV.1). Each is a typed value or the literal 'unstated'."""

    model_config = ConfigDict(extra="forbid")

    electrolyte: Union[Electrolyte, Literal["unstated"]] = UNSTATED
    ph: Union[float, Literal["unstated"]] = UNSTATED
    current_density: Union[CurrentDensity, Literal["unstated"]] = UNSTATED
    temperature: Union[TempValue, Literal["room_temperature", "unstated"]] = UNSTATED
    loading: Union[Loading, Literal["unstated"]] = UNSTATED
    substrate: str = UNSTATED  # the string 'unstated' is the sentinel
    protocol_tier: Literal[
        "ht_screen", "medium_term", "long_term", "other_stated", "unstated"
    ] = UNSTATED
    prior_operation_duration: Union[DurationValue, Literal["unstated"]] = UNSTATED
    anneal_temperature: Union[AnnealValue, Literal["as_deposited", "unstated"]] = UNSTATED
    ir_correction: Union[bool, Literal["unstated"]] = UNSTATED


CONDITION_KEYS = [
    "electrolyte",
    "ph",
    "current_density",
    "temperature",
    "loading",
    "substrate",
    "protocol_tier",
    "prior_operation_duration",
    "anneal_temperature",
    "ir_correction",
]


# --------------------------------------------------------------------------- #
# Claim card v2
# --------------------------------------------------------------------------- #
class ClaimCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # engine v1 fields
    claim_id: str
    claim_kind: ClaimKind
    commitment_direction: CommitmentDirection
    causal_direction: CausalDirection
    physical_scale: str
    measurability: Measurability
    measurable_with: Optional[str] = None
    subject: str
    relation: str
    object: str
    domain: Optional[str] = None
    source_sentence: str
    source_document: str
    provenance_hash: str

    # lab-extension additions (IV.1)
    axis: Optional[str] = None
    quantity: Optional[Quantity] = None
    conditions: Conditions = Field(default_factory=Conditions)

    @model_validator(mode="after")
    def _quantity_kinds_need_quantity_and_axis(self) -> "ClaimCard":
        if self.claim_kind in QUANTITY_KINDS:
            if self.quantity is None:
                raise ValueError(
                    f"claim_kind={self.claim_kind.value} requires a 'quantity' block"
                )
            if not self.axis:
                raise ValueError(
                    f"claim_kind={self.claim_kind.value} requires an 'axis' id"
                )
        return self


# --------------------------------------------------------------------------- #
# Comparability rules (IV.2)
# --------------------------------------------------------------------------- #
class Predicate(BaseModel):
    """A predicate name plus optional params. Accepts a bare string or a mapping
    like {name: equal_within, tolerance: 0} in YAML."""

    model_config = ConfigDict(extra="forbid")
    name: str
    params: dict = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _coerce(cls, data):
        if isinstance(data, str):
            return {"name": data, "params": {}}
        if isinstance(data, dict) and "name" not in data:
            # {equal_within: {tolerance: 0}} or {name:..., ...params}
            if len(data) == 1:
                (k, v), = data.items()
                return {"name": k, "params": v if isinstance(v, dict) else {"value": v}}
        return data


class ComparabilityRule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    fields: list[str]
    predicate: Predicate
    plain_english: str
    rationale: str = ""
    source: str = ""


class ComparabilityRules(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    rules: list[ComparabilityRule]
    # CP1 section 5: canonical maps locked as part of comparability-v0.
    canonical: dict = Field(default_factory=dict)


# --------------------------------------------------------------------------- #
# Verdict record (IV.4)
# --------------------------------------------------------------------------- #
class VerdictRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verdict_id: str
    claim_id: str
    data_source: dict  # {file, sha, row_refs}
    comparison: dict
    outcome: Literal["confirmed", "contradicted", "within_floor", "not_comparable"]
    margin: Optional[float]
    floor_applied: float
    rules_version: str
    map_version: str
    computed_at: str


class Defect(BaseModel):
    model_config = ConfigDict(extra="forbid")
    defect_type: DefectType
    target: str  # the condition field name, the rule id, or the axis pair


__all__ = [
    "ClaimKind",
    "QUANTITY_KINDS",
    "CommitmentDirection",
    "CausalDirection",
    "Measurability",
    "DefectType",
    "Concentration",
    "Electrolyte",
    "CurrentDensity",
    "TempValue",
    "Loading",
    "DurationValue",
    "AnnealValue",
    "Quantity",
    "Conditions",
    "CONDITION_KEYS",
    "ClaimCard",
    "Predicate",
    "ComparabilityRule",
    "ComparabilityRules",
    "VerdictRecord",
    "Defect",
    "UNSTATED",
]
