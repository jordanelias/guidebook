"""
schemas/bpc_metadata.py — BPC entry metadata entity model.

Represents extracted metadata from a Best Practices Compendium markdown file.
The BPC file itself remains the authoritative source — this entity captures
the structured metadata for validation and cross-referencing.

Sources of metadata within a BPC file:
1. Header line: "**Updated:** ... **Evidence tier range:** ... **Opus synthesis:** ..."
2. YAML block inside ```yaml ... ``` fences (usually under ### Metadata)
3. Key sources table (REF-IDs extracted for cross-system checking)
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class BPCMetadata(GuidebookEntity):
    """Metadata extracted from a BPC markdown file.

    Required fields match validate_bpc.py mandatory keys.
    Optional fields capture the full CO-0006 template when present.
    """

    # Required (per validate_bpc.py)
    slug: str
    population: str  # Comma-separated or single code
    last_updated: str  # YYYY-MM-DD or YYYY-MM-DD HH:MM

    # Location
    topic_directory: str  # e.g., "bathrooms-and-wet-areas"
    file_path: str  # Relative path from repo root

    # Template optional fields
    opus_synthesis: Optional[bool] = None
    opus_session: Optional[str] = None
    status: Optional[str] = None  # ACTIVE, PROVISIONAL, STUB, COMPLETE
    evidence_tier_range: Optional[str] = None  # e.g., "1–6", "Tier 1–5"
    jurisdiction_count: Optional[int] = None
    language_count: Optional[int] = None
    co0006_migration: Optional[bool] = None

    # Extracted from Key sources table
    key_source_ref_ids: list[str] = []  # Local REF-IDs (e.g., "01", "DAB-05")
    key_source_count: int = 0

    # Header-extracted fields
    header_updated: Optional[str] = None  # From header line
    header_opus: Optional[str] = None  # YES/NO from header

    # Frozen flag (top-level population files)
    is_frozen: bool = False

    # --- Validators ---

    @field_validator("slug")
    @classmethod
    def valid_slug(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("slug cannot be empty")
        # slugs are kebab-case
        if not re.match(r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$", v) and len(v) > 1:
            # Allow single-char or non-standard but flag
            pass
        return v.strip()

    @field_validator("population")
    @classmethod
    def valid_population(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("population cannot be empty")
        return v.strip()

    @field_validator("last_updated")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("last_updated cannot be empty")
        # Accept YYYY-MM-DD or YYYY-MM-DD HH:MM
        if not re.match(r"^\d{4}-\d{2}-\d{2}", v.strip()):
            raise ValueError(
                f"last_updated must start with YYYY-MM-DD, got: '{v}'"
            )
        return v.strip()
