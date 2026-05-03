"""
schemas/fdr_specialist.py — FDR Scenario and Specialist Handoff models.

FDR (Failure-Demand-Recovery) scenarios capture resilience analysis:
what happens when a design element fails, when demand exceeds capacity,
or when recovery from a failure event is needed.

Specialist handoffs capture the points where specialist consultation
(OT, PT, accessibility consultant, etc.) is required — the boundary
between what the guidebook equips a generalist to handle and what
requires specialist input.

Per D-0139 §3.5 and A3 §§1.9-1.10.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity
from schemas.enums import PopulationCode


class FDRScenario(GuidebookEntity):
    """A Failure-Demand-Recovery scenario.

    Each scenario documents what happens when a design parameter
    fails to meet its specification, when demand exceeds the designed
    capacity, or when recovery from a failure event is needed.

    FDR scenarios are linked to populations (who is affected) and
    specifications (which parameters are involved).
    """

    # Identity
    scenario_id: str  # "FDR-NNNN"
    scenario_type: str  # 'failure', 'demand-spike', 'recovery', 'compound'

    # Content
    description: str  # What happens in this scenario
    trigger: Optional[str] = None  # What triggers the scenario
    consequence: Optional[str] = None  # What the consequence is
    mitigation: Optional[str] = None  # How to mitigate

    # Affected populations
    affected_populations: list[str] = []  # PopulationCode values

    # Linked specifications
    specification_refs: list[str] = []  # Item codes (A-01 format)

    # Severity
    severity: Optional[str] = None  # 'critical', 'major', 'minor'

    # Source
    source_slug: Optional[str] = None  # FDR slug from fdr-slug-registry-v2.md

    # Metadata
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("scenario_id")
    @classmethod
    def valid_scenario_id(cls, v: str) -> str:
        if not re.match(r"^FDR-[\w-]+$", v):
            raise ValueError(f"scenario_id must match FDR-*, got: '{v}'")
        return v

    @field_validator("scenario_type")
    @classmethod
    def valid_type(cls, v: str) -> str:
        valid = {'failure', 'demand-spike', 'recovery', 'compound'}
        if v not in valid:
            raise ValueError(f"scenario_type must be one of {valid}, got: '{v}'")
        return v

    @field_validator("affected_populations")
    @classmethod
    def valid_populations(cls, v: list[str]) -> list[str]:
        valid = {e.value for e in PopulationCode}
        for code in v:
            if code not in valid:
                raise ValueError(f"Unknown population code: '{code}'")
        return v

    @field_validator("specification_refs")
    @classmethod
    def valid_spec_refs(cls, v: list[str]) -> list[str]:
        for ref in v:
            if not re.match(r"^[A-K]-\d{2}$", ref):
                raise ValueError(f"spec ref must be item code [A-K]-NN, got: '{ref}'")
        return v


class SpecialistHandoff(GuidebookEntity):
    """A specialist handoff point.

    Documents where the guidebook reaches the boundary of what a
    generalist professional can handle and specialist input is required.
    Per A3 §1.10 and Part 9 (Working with Specialist Consultants).
    """

    # Identity
    handoff_id: str  # "SH-NNNN"

    # Specialist
    specialist_role: str  # 'OT', 'PT', 'accessibility-consultant', etc.
    specialist_detail: Optional[str] = None  # More specific role description

    # Trigger
    triggering_condition: str  # When this handoff is needed
    design_stage: Optional[str] = None  # At which design stage

    # Linked specifications
    specification_refs: list[str] = []  # Item codes

    # Population context
    populations: list[str] = []  # Which populations trigger this handoff

    # Metadata
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("handoff_id")
    @classmethod
    def valid_handoff_id(cls, v: str) -> str:
        if not re.match(r"^SH-\d{4}$", v):
            raise ValueError(f"handoff_id must match SH-NNNN, got: '{v}'")
        return v

    @field_validator("specialist_role")
    @classmethod
    def valid_role(cls, v: str) -> str:
        valid = {
            'OT', 'PT', 'accessibility-consultant', 'acoustic-consultant',
            'lighting-consultant', 'disability-studies', 'wayfinding-specialist',
        }
        if v not in valid:
            # Allow unlisted roles but warn
            pass  # Extensible — new specialist roles may be added
        return v
