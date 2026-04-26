"""
schemas/gap.py — Gap register entry entity model.

Gaps track identified issues, missing content, and research needs.
The gap register enforces a priority/status state machine.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class Gap(GuidebookEntity):
    """A gap register entry."""

    gap_id: str  # GAP-NNN or GAP-XX-NN
    category: str  # RP, SW, CR, ST, MX, CD, EC, EG
    priority: str  # P1, P2, P3
    status: str  # OPEN, OPEN-PARTIAL, CLOSED-*
    skill: str  # Originating skill
    section: str  # Affected section
    description: str
    date: str  # YYYY-MM-DD or YYYY-MM-DD HH:MM

    @field_validator("gap_id")
    @classmethod
    def valid_gap_id(cls, v: str) -> str:
        if not re.match(r"^GAP-", v):
            raise ValueError(f"gap_id must start with GAP-, got: '{v}'")
        return v

    @field_validator("category")
    @classmethod
    def valid_category(cls, v: str) -> str:
        valid = {"RP", "SW", "CR", "ST", "MX", "CD", "EC", "EG"}
        if v not in valid:
            raise ValueError(f"Invalid category: '{v}'. Must be one of {valid}")
        return v

    @field_validator("priority")
    @classmethod
    def valid_priority(cls, v: str) -> str:
        valid = {"P1", "P2", "P3"}
        if v not in valid:
            raise ValueError(f"Invalid priority: '{v}'. Must be one of {valid}")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        valid_prefixes = {"OPEN", "CLOSED"}
        prefix = v.split("-")[0] if "-" in v else v
        if prefix not in valid_prefixes:
            raise ValueError(f"Invalid status: '{v}'. Must start with OPEN or CLOSED")
        return v
