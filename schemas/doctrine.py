"""
schemas/doctrine.py — Doctrine entity model.

Represents a foundational principle or framework from Part 1 that
governs how specifications are authored, applied, and interpreted.
Doctrines are grouped (Core, Evidence, Ethics, Frameworks) and
serve the /foundations/ URL family.

Per navigation-modes.md §3.2 and B3.2.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class Doctrine(GuidebookEntity):
    """A foundational doctrine or framework entry.

    Doctrines are the authoritative principles from Part 1 that
    govern all downstream specification work. Each doctrine has
    a slug for URL routing and a group for index organisation.
    """

    # Identity
    doctrine_id: str  # "DOC-NNNN"
    slug: str  # URL slug, e.g. "design-modes"
    title: str  # e.g. "Design Modes"
    group: str  # "core", "evidence", "ethics", "frameworks"

    # Content
    statement: str  # Authoritative prose (from Part 1)
    implications: Optional[str] = None  # Implications for practice
    body_md: Optional[str] = None  # Full prose (markdown)

    # Relationships
    related_specifications: list[str] = []  # Item codes affected
    related_sections: list[str] = []  # Part/section references, e.g. "§1.2"

    # Source
    part_section: Optional[str] = None  # e.g. "§1.2"
    part_source: int = 1  # Always Part 1

    # Metadata
    status: str = "active"  # active, superseded
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("doctrine_id")
    @classmethod
    def valid_doctrine_id(cls, v: str) -> str:
        if not re.match(r"^DOC-\d{4}$", v):
            raise ValueError(f"doctrine_id must match DOC-NNNN, got: '{v}'")
        return v

    @field_validator("group")
    @classmethod
    def valid_group(cls, v: str) -> str:
        valid = {"core", "evidence", "ethics", "frameworks"}
        if v not in valid:
            raise ValueError(f"group must be one of {sorted(valid)}, got: '{v}'")
        return v

    @field_validator("slug")
    @classmethod
    def valid_slug(cls, v: str) -> str:
        if not re.match(r"^[a-z][a-z0-9-]*$", v):
            raise ValueError(
                f"slug must be lowercase alphanumeric with hyphens, got: '{v}'"
            )
        return v
