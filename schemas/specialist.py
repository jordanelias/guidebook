"""
schemas/specialist.py — Specialist Consultant entity model.

Represents a specialist consultant role from Part 9 (Working with
Specialist Consultants). Each role has appointment triggers, scope
of services by design stage, and links to specifications that
require specialist input.

Per navigation-modes.md §3.2 and B3.2.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class DesignStageScope(GuidebookEntity):
    """Scope of specialist services at a specific design stage."""

    stage: str  # SD, DD, CD, RFO
    scope: str  # What the specialist does at this stage
    deliverables: list[str] = []  # Expected deliverables


class Specialist(GuidebookEntity):
    """A specialist consultant role.

    Part 9 defines the boundary between what the guidebook equips
    a generalist to handle and what requires specialist input.
    Each specialist role has triggers (when to appoint), scope
    (what they do at each design stage), and specification links
    (which items require their input).
    """

    # Identity
    specialist_id: str  # "SPEC-ROLE-NN"
    role: str  # "OT", "dementia-design", "deafspace", etc.
    role_label: str  # Human-readable: "Occupational Therapist"

    # Source
    part_section: Optional[str] = None  # e.g. "§9.2"

    # Content
    role_description: str  # What this specialist does
    appointment_triggers: list[str] = []  # When to appoint
    scope_by_stage: list[DesignStageScope] = []  # Services per design stage

    # Assessment output
    assessment_format: Optional[str] = None  # Report format guidance
    co_design_notes: Optional[str] = None  # CRPD Article 4.3 notes

    # Relationships
    specification_refs: list[str] = []  # Item codes requiring this specialist
    population_codes: list[str] = []  # Populations this specialist serves
    handoff_ids: list[str] = []  # SH-NNNN references from fdr_specialist.py

    # Guidebook relationship
    guidebook_relationship: Optional[str] = None  # How this role relates to the guidebook

    # Metadata
    status: str = "active"
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("specialist_id")
    @classmethod
    def valid_specialist_id(cls, v: str) -> str:
        if not re.match(r"^SPEC-ROLE-\d{2}$", v):
            raise ValueError(f"specialist_id must match SPEC-ROLE-NN, got: '{v}'")
        return v

    @field_validator("role")
    @classmethod
    def valid_role(cls, v: str) -> str:
        known = {
            "OT",
            "dementia-design",
            "deafspace",
            "sensory-design",
            "accessibility-auditor",
            "disability-organisation",
        }
        if v not in known:
            # Extensible — warn but don't reject
            pass
        return v
