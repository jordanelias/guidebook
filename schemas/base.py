"""
schemas/base.py — Base model for all guidebook entities.

Provides shared configuration: YAML serialization defaults,
validation settings, and common fields (timestamps, IDs).
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class GuidebookEntity(BaseModel):
    """Base class for all guidebook data entities.

    Config:
    - Extra fields forbidden (catches typos and schema drift).
    - Enum values serialized by value (not name) for YAML readability.
    - Validation runs on assignment (not just construction).
    """

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    @classmethod
    def from_yaml(cls, path: str) -> "GuidebookEntity":
        """Load entity from a YAML file."""
        import yaml

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)

    def to_yaml(self, path: str) -> None:
        """Write entity to a YAML file."""
        import yaml

        data = self.model_dump(mode="json", exclude_none=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(
                data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            )

    def to_dict(self) -> dict:
        """Serialize to dict, excluding None values."""
        return self.model_dump(mode="json", exclude_none=True)


class EvidenceTierRange(BaseModel):
    """Structured representation of an evidence tier range.

    Replaces compound strings like "Tier 4-5" or "Co-1/Tier 3".
    floor and ceiling define the tier range (1–6) of supporting evidence.
    evidence_types_present lists the kinds of evidence found (per T-03).

    Per T-03: tier is one dimension (1–6), evidence_type is the other.
    Co-1 is not a tier — it's an evidence_type with tier=1 (co-primary).
    """

    model_config = ConfigDict(extra="forbid")

    floor: int  # Strongest evidence tier (1–6)
    ceiling: int  # Weakest evidence tier (1–6)
    evidence_types_present: list[str] = []  # EvidenceType values found

    @field_validator("floor")
    @classmethod
    def valid_floor(cls, v: int) -> int:
        if v < 1 or v > 6:
            raise ValueError(f"floor must be 1–6, got {v}")
        return v

    @field_validator("ceiling")
    @classmethod
    def ceiling_gte_floor(cls, v: int, info) -> int:
        if v < 1 or v > 6:
            raise ValueError(f"ceiling must be 1–6, got {v}")
        floor = info.data.get("floor")
        if floor is not None and v < floor:
            raise ValueError(
                f"ceiling ({v}) cannot be stronger than floor ({floor})"
            )
        return v


class ConditionValue(BaseModel):
    """Population-dependent conditional value per CO-0006 §C3.

    Example: corridor width varies by single wheelchair vs two passing.
    """

    model_config = ConfigDict(extra="forbid")

    condition: str
    value_min: Optional[float] = None
    value_max: Optional[float] = None
    unit: Optional[str] = None
    populations: list[str] = []
