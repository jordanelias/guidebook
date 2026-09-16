"""
schemas/slug.py — Research slug entity model.

A slug is a research unit — a single topic that has both a search log
and a BPC entry. The slug registry maps slugs to their file paths
and topic directories.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class Slug(GuidebookEntity):
    """A research slug in the slug registry."""

    slug: str
    topic_directory: str
    sl_path: str  # Search log file path
    bpc_path: str  # BPC file path
    status: str  # ACTIVE, MERGED, STUB

    # Merge target (if MERGED)
    merged_into: Optional[str] = None

    @field_validator("slug")
    @classmethod
    def valid_slug(cls, v: str) -> str:
        if not v or not re.match(r"^[a-z0-9][a-z0-9\-]*$", v):
            raise ValueError(f"Invalid slug format: '{v}'")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        valid = {"ACTIVE", "MERGED", "STUB", "PROVISIONAL"}
        if v not in valid:
            raise ValueError(f"Invalid status: '{v}'. Must be one of {valid}")
        return v
