"""
schemas/item.py — Item entity model.

Represents a physical product, fixture, or assembly that implements
one or more specifications. Items are the Part 4 organizational unit —
each item code (A-01 through K-NN) groups related specifications
under a single design element.

Per D-0139 §3.2 and A3 §1.7.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class Item(GuidebookEntity):
    """An item entity — a physical element that implements specifications.

    Items map to Part 4 item codes. Each item groups one or more
    specifications under a single design element (e.g., E-08 "Corridor
    Clear Width" groups width, passing space, and turning specifications).
    """

    # Identity
    item_id: str  # "ITEM-NNNN" formal ID
    item_code: str  # "E-08" — Part 4 code
    category: str  # Single letter A-K
    category_name: str  # "Circulation" etc.
    name: str  # Human-readable name, e.g. "Corridor Clear Width"

    # Content
    description: Optional[str] = None  # Brief description
    body_md: Optional[str] = None  # Full item specification prose (markdown)

    # Specification linkages (denormalized for convenience; canonical in join table)
    specification_ids: list[str] = []  # SPEC-NNNN references

    # Part 4 structural metadata
    part_section: Optional[str] = None  # e.g. "§4.5"
    bpc_source_slug: Optional[str] = None  # Primary BPC file

    # Status
    status: Optional[str] = None  # draft, active, merged, retired

    # Metadata
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("item_code")
    @classmethod
    def valid_item_code(cls, v: str) -> str:
        if not re.match(r"^[A-K]-\d{2}$", v):
            raise ValueError(
                f"item_code must match [A-K]-NN, got: '{v}'"
            )
        return v

    @field_validator("category")
    @classmethod
    def valid_category(cls, v: str) -> str:
        if not re.match(r"^[A-K]$", v):
            raise ValueError(
                f"category must be single letter A-K, got: '{v}'"
            )
        return v

    @field_validator("specification_ids")
    @classmethod
    def valid_spec_ids(cls, v: list[str]) -> list[str]:
        for sid in v:
            if not re.match(r"^SPEC-\d{4}$", sid):
                raise ValueError(
                    f"specification_id must match SPEC-NNNN, got: '{sid}'"
                )
        return v
