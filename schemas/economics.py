"""
schemas/economics.py — Economics entity model.

Represents economic evidence entries from Part 11 and the economics
data store. Economics entries are organized by pillar (health outcomes,
cost of inaction, construction cost, market value) and serve the
/economics/ URL family.

Per navigation-modes.md §3.2, unified-data-schema Entity 5, and B3.2.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class EconomicsEntry(GuidebookEntity):
    """An economics evidence entry.

    Each entry captures one piece of economic evidence — a cost
    premium study, a health outcome RCT, a retrofit multiplier,
    a grant programme, or a market value finding. Entries are
    grouped by pillar for the economics dashboard.
    """

    # Identity
    entry_id: str  # e.g. "ECON-0001" or sub-type IDs (HO-001, CP-001, etc.)
    pillar: str  # "health", "inaction", "construction", "market"
    entry_type: str  # "cost_premium", "retrofit_multiplier", "grant_programme",
                     # "health_outcome", "market_value", "housing_deficit", "research_gap"

    # Content
    source: str  # Citation reference
    jurisdiction: Optional[str] = None  # ISO country code or "MULTI"
    finding: str  # Key finding text
    study_design: Optional[str] = None  # RCT, systematic review, survey, etc.
    sample: Optional[str] = None  # Sample description

    # Quantitative data (type-dependent)
    value_numeric: Optional[float] = None  # Primary numeric value
    value_unit: Optional[str] = None  # "%", "currency", "ratio", "years"
    currency: Optional[str] = None  # ISO currency code
    bcr: Optional[str] = None  # Benefit-cost ratio if available

    # Classification
    evidence_tier: Optional[int] = None  # 1-6
    confidence: Optional[str] = None  # "HIGH", "MODERATE", "LOW"

    # Relationships
    specification_refs: list[str] = []  # Item codes with cost data
    population_codes: list[str] = []  # Populations affected

    # Metadata
    year: Optional[int] = None  # Publication year
    journal: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("pillar")
    @classmethod
    def valid_pillar(cls, v: str) -> str:
        valid = {"health", "inaction", "construction", "market"}
        if v not in valid:
            raise ValueError(f"pillar must be one of {sorted(valid)}, got: '{v}'")
        return v

    @field_validator("entry_type")
    @classmethod
    def valid_entry_type(cls, v: str) -> str:
        valid = {
            "cost_premium", "retrofit_multiplier", "grant_programme",
            "health_outcome", "market_value", "housing_deficit", "research_gap",
        }
        if v not in valid:
            raise ValueError(f"entry_type must be one of {sorted(valid)}, got: '{v}'")
        return v
