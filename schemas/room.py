"""
schemas/room.py — Room entity model.

Represents a room type from Parts 6-7 with its item application
matrix, DAR provisions, conflict register, and schematic checklist.
Rooms serve the /rooms/ URL family.

Per navigation-modes.md §3.1, unified-data-schema Entity 3, and B3.2.
Entity E-17 (deferred from A6, now scoped).
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import GuidebookEntity


class RoomItemEntry(GuidebookEntity):
    """An item's application within a specific room type."""

    item_code: str  # e.g. "E-06"
    item_title: Optional[str] = None
    design_stage: Optional[str] = None  # SD, DD, CD, RFO
    must_appear_on: Optional[str] = None  # e.g. "Site plan; floor plan"
    population_applicability: Optional[dict[str, str]] = None  # {code: "primary"/"secondary"/null}
    notes: Optional[str] = None

    @field_validator("item_code")
    @classmethod
    def valid_item_code(cls, v: str) -> str:
        if not re.match(r"^[A-K]-\d{2}$", v):
            raise ValueError(f"item_code must match [A-K]-NN, got: '{v}'")
        return v


class DARProvision(GuidebookEntity):
    """A Design-for-Adaptability-and-Repair provision for a room."""

    description: str
    construction_stage: Optional[str] = None  # CD, RFO
    drawing_reference: Optional[str] = None
    notes: Optional[str] = None


class RoomConflict(GuidebookEntity):
    """A conflict register entry specific to a room context."""

    description: str
    resolution: Optional[str] = None
    conflict_domain: Optional[str] = None  # Links to conflict entity


class Room(GuidebookEntity):
    """A room type entity from the application matrices.

    Each room groups the specifications applicable in that spatial
    context, with population applicability, DAR provisions, conflict
    resolutions, and a schematic checklist.
    """

    # Identity
    room_id: str  # "R-ENT", "R-BA", etc.
    room_label: str  # "Entry", "Bathroom", etc.
    building_type: str  # "residential", "non-residential"

    # Source
    part_source: int  # 6 (residential) or 7 (non-residential)
    section: Optional[str] = None  # e.g. "§6.1"

    # Context
    criticality_note: Optional[str] = None  # Why this room matters
    evidence_density: Optional[str] = None  # ■ Rich / ▓ Moderate / ░ Thin / · Absent

    # Populations
    primary_populations: list[str] = []  # Population codes most relevant

    # Content
    item_matrix: list[RoomItemEntry] = []  # Items applicable in this room
    dar_provisions: list[DARProvision] = []
    conflict_register: list[RoomConflict] = []
    schematic_checklist: list[str] = []  # Checklist items for schematic review

    # Metadata
    status: str = "active"
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("room_id")
    @classmethod
    def valid_room_id(cls, v: str) -> str:
        if not re.match(r"^(R|NR)-[A-Z]{2,4}$", v):
            raise ValueError(f"room_id must match R-XX/NR-XXX, got: '{v}'")
        return v

    @field_validator("building_type")
    @classmethod
    def valid_building_type(cls, v: str) -> str:
        if v not in ("residential", "non-residential"):
            raise ValueError(
                f"building_type must be 'residential' or 'non-residential', got: '{v}'"
            )
        return v

    @field_validator("part_source")
    @classmethod
    def valid_part_source(cls, v: int) -> int:
        if v not in (6, 7):
            raise ValueError(f"part_source must be 6 or 7, got: {v}")
        return v
