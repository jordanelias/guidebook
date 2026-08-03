"""
schemas/connection.py — Connection entity model.

Represents a cross-item integration instruction from the connection register.
Connections link items to each other with explanatory context — they are
instructions for synthesis: "when writing spec X, also consider spec Y."

Per CO-0006: master index at references/connections/_index.md + per-topic files.
CON-ID format: CON-NNNN (4-digit zero-padded per project-standards).
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class Connection(GuidebookEntity):
    """A single connection register entry."""

    # Identity
    con_id: str  # CON-NNNN

    # Status
    status: str  # CONSUMED, CONSUMED-DEFERRED, PENDING

    # Cross-references
    primary_target: str  # Item codes or descriptions
    filed_in: str  # Topic directory name

    # Assessment
    confidence: str  # HIGH, MODERATE, SPECULATIVE
    opus_reviewed: bool = False

    # Application
    session_applied: Optional[str] = None

    # Type (per project-standards — connection_scout entry schema)
    connection_type: Optional[str] = None  # CROSS-POPULATION, CROSS-ITEM, COMPOUND-INTERACTION, METHODOLOGY

    # --- Validators ---

    @field_validator("con_id")
    @classmethod
    def valid_con_id(cls, v: str) -> str:
        if not re.match(r"^CON-\d{4}$", v):
            raise ValueError(f"con_id must match CON-NNNN (4-digit), got: {v}")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        valid = {"CONSUMED", "CONSUMED-DEFERRED", "PENDING", "CLOSED"}
        if v not in valid:
            raise ValueError(f"Invalid status: '{v}'. Must be one of {valid}")
        return v

    @field_validator("confidence")
    @classmethod
    def valid_confidence(cls, v: str) -> str:
        # Normalize MEDIUM → MODERATE
        if v == "MEDIUM":
            v = "MODERATE"
        valid = {"HIGH", "MODERATE", "SPECULATIVE"}
        if v not in valid:
            raise ValueError(f"Invalid confidence: '{v}'. Must be one of {valid}")
        return v
