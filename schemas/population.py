"""
schemas/population.py — Population and Sub-population entity model.

Represents a disability population code with its functional profile,
primary barriers, key parameters, conflict domains, and evidence basis.
Implements single-table inheritance via self-referencing parent_code
per schema-spec §3.1 and A7 population-taxonomy.md.

Sub-codes inherit parent properties. Recursive CTE in SQLite resolves
inheritance at query time via the population_resolved view.
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import GuidebookEntity
from schemas.enums import PopulationCode


class Population(GuidebookEntity):
    """A population code entity in the guidebook data layer.

    Each record represents a disability population (top-level) or
    sub-population that inherits from a parent. Population codes
    are the organizing axis for design parameter applicability,
    conflict domain membership, and evidence-state tracking.
    """

    # Identity
    code: str  # PopulationCode value, e.g. "MOB", "MOB/AMB"
    parent_code: Optional[str] = None  # NULL for top-level; e.g. "MOB" for "MOB/AMB"
    label: str  # Human-readable label, e.g. "Mobility and Strength"
    definition: str  # Functional definition

    # Functional profile (from populations.json)
    functional_profile: Optional[str] = None  # prose description
    primary_barriers: list[str] = []  # barrier strings
    key_parameters: list[str] = []  # item codes of key specifications

    # Evidence
    evidence_confidence: Optional[str] = None  # HIGH, MEDIUM, LOW
    evidence_strength: Optional[str] = None  # A6 §6 directional

    # Conflict domains
    conflict_domains: list[str] = []  # conflict domain IDs

    # Co-occurrence
    co_occurrence_notes: Optional[str] = None  # prose on compound profiles

    # ICF mapping (new — AF-5 requirement)
    icf_codes_primary: list[str] = []  # ICF codes, e.g. ["b710", "b730"]

    # Population-level prevalence
    prevalence_band: Optional[str] = None  # 'common', 'less-common', 'rare'

    # Co-1 evidence status
    co1_status: Optional[str] = None  # e.g. "Partial — KR and BR not retrieved"
    co1_gap_note: Optional[str] = None

    # BPC source slugs
    bpc_slugs: list[str] = []  # BPC file slugs covering this population

    # Metadata
    notes: Optional[str] = None
    specification_count: Optional[int] = None

    # --- Validators ---

    @field_validator("code")
    @classmethod
    def valid_code(cls, v: str) -> str:
        """Validate population code format."""
        valid = {e.value for e in PopulationCode}
        if v not in valid:
            raise ValueError(
                f"Unknown population code: '{v}'. "
                f"Valid codes: {sorted(valid)}"
            )
        return v

    @field_validator("parent_code")
    @classmethod
    def valid_parent(cls, v: Optional[str]) -> Optional[str]:
        """Parent code must also be a valid PopulationCode if set."""
        if v is not None:
            valid = {e.value for e in PopulationCode}
            if v not in valid:
                raise ValueError(f"Unknown parent population code: '{v}'")
        return v

    @field_validator("key_parameters")
    @classmethod
    def valid_item_codes(cls, v: list[str]) -> list[str]:
        """Key parameters must be valid item codes."""
        for code in v:
            if not re.match(r"^[A-K]-\d{2}$", code):
                raise ValueError(
                    f"key_parameter must be item code [A-K]-NN, got: '{code}'"
                )
        return v

    @model_validator(mode="after")
    def inheritance_consistency(self) -> "Population":
        """Sub-codes must have a parent; top-level codes must not."""
        if "/" in self.code:
            # Sub-code: must have parent_code
            if self.parent_code is None:
                expected_parent = self.code.split("/")[0]
                raise ValueError(
                    f"Sub-code '{self.code}' must have parent_code "
                    f"(expected '{expected_parent}')"
                )
        return self
