"""
schemas/throughline.py — Throughline entity model.

Represents a cross-cutting pattern identified across multiple
evidence bases and specifications. Throughlines are meta-observations
about how the evidence base behaves — patterns that recur across
populations, parameters, and jurisdictions.

Per navigation-modes.md §3.2 and B3.2.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class ThroughlineInstance(GuidebookEntity):
    """An instance of a throughline in a specific specification context."""

    specification_ref: Optional[str] = None  # Item code
    description: str  # How this throughline manifests here
    population_codes: list[str] = []  # Relevant populations


class Throughline(GuidebookEntity):
    """A throughline — a cross-cutting pattern across evidence bases.

    Throughlines are identified in the throughline analysis and
    represent structural observations about the evidence. They
    are not specifications themselves but inform how specifications
    should be read, applied, and extended.
    """

    # Identity
    throughline_id: str  # "T-NN"
    title: str  # e.g. "Code-as-Floor / Beyond-Code"
    slug: Optional[str] = None  # URL slug

    # Content
    description: str  # What this throughline captures
    implications: Optional[str] = None  # What it means for practice
    body_md: Optional[str] = None  # Full analysis prose (markdown)

    # Instances
    instances: list[ThroughlineInstance] = []  # Where this throughline appears

    # Relationships
    specification_refs: list[str] = []  # Item codes where this applies
    population_codes: list[str] = []  # Populations involved

    # Classification
    category: Optional[str] = None  # "methodological", "clinical", "structural"

    # Metadata
    status: str = "active"
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("throughline_id")
    @classmethod
    def valid_throughline_id(cls, v: str) -> str:
        if not re.match(r"^T-\d{2}$", v):
            raise ValueError(f"throughline_id must match T-NN, got: '{v}'")
        return v
