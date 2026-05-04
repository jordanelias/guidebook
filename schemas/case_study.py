"""
schemas/case_study.py — Case Study entity model.

Represents a documented accessible built environment from Part 12.
Each case study captures a real building with verified design
strategies, outcomes, and (where available) cost data.

Per navigation-modes.md §3.2, unified-data-schema Entity 6, and B3.2.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class CaseStudyOutcome(GuidebookEntity):
    """A verified outcome from a case study."""

    metric: str  # What was measured
    value: Optional[str] = None  # The measured value
    source: Optional[str] = None  # How it was verified
    tier: Optional[int] = None  # Evidence quality tier (1-3 per Part 12)


class CaseStudy(GuidebookEntity):
    """A case study entry from Part 12.

    Each case study documents a real building with independently
    verified outcomes. The evidence quality tier reflects the
    verification method, not the building quality.
    """

    # Identity
    case_study_id: str  # "CS-NNNN"
    slug: str  # URL slug
    title: str  # e.g. "Maggie's Centre, Inverness"

    # Building information
    building_type: str  # "cancer support centre", "university campus", etc.
    location: str  # City, Country
    architect: Optional[str] = None
    year: Optional[int] = None  # Completion year
    setting: Optional[str] = None  # e.g. "NHS Highland, Scotland, UK"

    # Populations
    primary_populations: list[str] = []  # Population codes
    population_description: Optional[str] = None  # Prose description

    # Design strategies
    design_strategies: list[str] = []  # Prose descriptions
    specification_refs: list[str] = []  # Item codes demonstrated

    # Outcomes
    outcomes: list[CaseStudyOutcome] = []
    evidence_quality_tier: Optional[int] = None  # 1-3 per Part 12 methodology

    # Cost data
    cost_data: Optional[str] = None  # Cost information (if available)
    cost_data_quality: Optional[str] = None  # VERIFIED, PROVISIONAL, GREY

    # Source
    part_section: Optional[str] = None  # e.g. "§12.01"

    # Limitations
    limitations: Optional[str] = None

    # Metadata
    status: str = "active"
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("case_study_id")
    @classmethod
    def valid_case_study_id(cls, v: str) -> str:
        if not re.match(r"^CS-\d{4}$", v):
            raise ValueError(f"case_study_id must match CS-NNNN, got: '{v}'")
        return v

    @field_validator("slug")
    @classmethod
    def valid_slug(cls, v: str) -> str:
        if not re.match(r"^[a-z][a-z0-9-]*$", v):
            raise ValueError(
                f"slug must be lowercase alphanumeric with hyphens, got: '{v}'"
            )
        return v

    @field_validator("evidence_quality_tier")
    @classmethod
    def valid_tier(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v not in (1, 2, 3):
            raise ValueError(f"evidence_quality_tier must be 1-3, got: {v}")
        return v

    @field_validator("cost_data_quality")
    @classmethod
    def valid_cost_quality(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("VERIFIED", "PROVISIONAL", "GREY"):
            raise ValueError(
                f"cost_data_quality must be VERIFIED/PROVISIONAL/GREY, got: '{v}'"
            )
        return v
