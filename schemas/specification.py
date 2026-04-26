"""
schemas/specification.py — Specification entity model.

Represents a single measurable design parameter with its evidence basis,
population applicability, and jurisdiction coverage. This is the primary
entity type in the specification database.

Cross-field validation rules (from throughline analysis F-10):
- value_type == FIXED → value_min == value_max == value_median
- value_type == RANGE → value_min < value_max, median between them
- value_type == QUALITATIVE → all value fields None
- item_code present ↔ assignment_status == ASSIGNED
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import ConditionValue, EvidenceTierRange, GuidebookEntity
from schemas.enums import (
    ItemAssignmentStatus,
    PopulationCode,
    RecommendationStrength,
    ValueType,
)


class Specification(GuidebookEntity):
    """A single specification record in the guidebook data layer.

    Each record ties a measurable parameter to its evidence, populations,
    and jurisdictions. The spec_id is the stable identifier; item_code
    is assigned when the specification is integrated into Part 4.
    """

    # Identity
    spec_id: str  # SPEC-NNNN
    slug: str  # BPC source slug
    bpc_source_slug: str  # May differ from slug if restructured

    # Item assignment
    item_code: Optional[str] = None  # e.g. "G-03" — None if unassigned
    assignment_status: ItemAssignmentStatus = ItemAssignmentStatus.UNASSIGNED

    # Parameter
    parameter: str  # snake_case parameter name
    value_type: ValueType
    value_min: Optional[float] = None
    value_max: Optional[float] = None
    value_median: Optional[float] = None
    unit: Optional[str] = None

    # Evidence
    evidence_tier: Optional[EvidenceTierRange] = None
    opus_synthesized: bool = False
    opus_synthesis_date: Optional[str] = None
    recommendation_strength: RecommendationStrength = RecommendationStrength.UNSET
    recommendation_qualifier: Optional[str] = None  # Free-text qualifier

    # Populations
    populations: list[str] = []  # PopulationCode values

    # Jurisdictions
    jurisdictions_supporting: list[str] = []  # JurisdictionCode values
    jurisdictions_divergent: list[str] = []
    divergence_note: Optional[str] = None

    # Tier 2 handoff
    tier_2_note: Optional[str] = None

    # Conditional values
    conditions: list[ConditionValue] = []

    # Metadata
    percentile_basis: Optional[str] = None  # DEPRECATED — vestigial field
    notes: Optional[str] = None
    context_note: Optional[str] = None

    # --- Validators ---

    @field_validator("spec_id")
    @classmethod
    def valid_spec_id(cls, v: str) -> str:
        if not re.match(r"^SPEC-\d{4}$", v):
            raise ValueError(f"spec_id must match SPEC-NNNN, got: {v}")
        return v

    @field_validator("item_code")
    @classmethod
    def valid_item_code(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^[A-K]-\d{2}$", v):
            raise ValueError(
                f"item_code must match [A-K]-NN (bare code, no prefix), got: {v}"
            )
        return v

    @field_validator("parameter")
    @classmethod
    def no_sentinel_parameter(cls, v: str) -> str:
        if v.lower() in ("unclassified", "unknown", "tbd"):
            raise ValueError(
                f"Sentinel parameter name not allowed: '{v}'. "
                "Assign a descriptive snake_case name."
            )
        return v

    @field_validator("populations")
    @classmethod
    def valid_population_codes(cls, v: list[str]) -> list[str]:
        valid = {e.value for e in PopulationCode}
        for code in v:
            if code not in valid:
                raise ValueError(
                    f"Unknown population code: '{code}'. "
                    f"Valid codes: {sorted(valid)}"
                )
        return v

    @model_validator(mode="after")
    def cross_field_validation(self) -> "Specification":
        """Enforce value_type / value / assignment consistency."""

        # Value-type consistency
        if self.value_type == ValueType.FIXED:
            if (
                self.value_min is not None
                and self.value_max is not None
                and self.value_min != self.value_max
            ):
                raise ValueError(
                    f"value_type is FIXED but min ({self.value_min}) != "
                    f"max ({self.value_max})"
                )

        elif self.value_type == ValueType.RANGE:
            if (
                self.value_min is not None
                and self.value_max is not None
                and self.value_min >= self.value_max
            ):
                raise ValueError(
                    f"value_type is RANGE but min ({self.value_min}) >= "
                    f"max ({self.value_max})"
                )
            if (
                self.value_median is not None
                and self.value_min is not None
                and self.value_max is not None
            ):
                if not (self.value_min <= self.value_median <= self.value_max):
                    raise ValueError(
                        f"median ({self.value_median}) not between "
                        f"min ({self.value_min}) and max ({self.value_max})"
                    )

        elif self.value_type == ValueType.QUALITATIVE:
            if any(
                v is not None
                for v in [self.value_min, self.value_max, self.value_median]
            ):
                raise ValueError(
                    "value_type is QUALITATIVE but numeric values are set"
                )

        # Assignment status consistency
        if self.item_code is not None:
            if self.assignment_status != ItemAssignmentStatus.ASSIGNED:
                raise ValueError(
                    f"item_code is set ('{self.item_code}') but "
                    f"assignment_status is {self.assignment_status}"
                )
        else:
            if self.assignment_status == ItemAssignmentStatus.ASSIGNED:
                raise ValueError(
                    "assignment_status is ASSIGNED but item_code is None"
                )

        return self
