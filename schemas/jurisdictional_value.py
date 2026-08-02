"""
schemas/jurisdictional_value.py — Jurisdiction-specific code/standard values.

A jurisdictional value is a *code floor* — what a named jurisdiction's standard
requires for a given item — and is deliberately NOT a best-practice claim.
migration 026 gave these their own table precisely so that a jurisdiction-specific
minimum could never be conflated with the jurisdiction-agnostic best practice; see
that migration's header and governance/tier-system.md on the corridor-width case.

WHY THIS MODEL EXISTS. `data/jurisdictional_values/*.yaml` is the only entity
corpus on disk with a real DB counterpart (`jurisdictional_values`, 109 rows) and
no validator of any kind. scripts/validate_schema.py — a BLOCKING check — named
six subdirectories that have never existed (`specifications`, `sources`,
`bpc-metadata`, `connections`, `slugs`, `gaps`), so it found zero files and
exited 0 on every run it has ever made. Repointing it at this corpus is what
makes that gate assert something.

Shape note: each YAML file is a *section wrapper* carrying several records, not a
single entity, so the file-level model is JurisdictionalValueFile and the row-level
model is JurisdictionalValueRecord. The record fields mirror the DB table's
columns, minus the provenance quartet (created_at/created_by_session/updated_at/
updated_by_session), which the migration sets and the YAML does not carry.
"""

from typing import List, Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class JurisdictionalValueRecord(GuidebookEntity):
    """One (item × jurisdiction) code value. Mirrors a `jurisdictional_values` row."""

    # Nullability mirrors the DB exactly, checked against PRAGMA table_info:
    # item_code and jurisdiction are NOT NULL (they are the identity of a code
    # value); spec_id and standard_name are nullable and 83 of 109 rows carry a
    # NULL spec_id. A first draft of this model made both required, which would
    # have turned a gate that checked nothing into a gate that failed on correct
    # data — the same defect wearing the opposite sign.
    item_code: str
    jurisdiction: str
    spec_id: Optional[str] = None
    standard_name: Optional[str] = None
    value_text: Optional[str] = None
    value_numeric: Optional[float] = None
    unit: Optional[str] = None
    # SQLite has no boolean type; the table stores 0/1 INTEGER.
    is_code_minimum: Optional[int] = None
    evidence_tier: Optional[int] = None
    source_section: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("evidence_tier")
    @classmethod
    def tier_in_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not 1 <= v <= 6:
            raise ValueError(f"evidence_tier {v} outside the 1-6 ladder (governance/tier-system.md)")
        return v

    @field_validator("is_code_minimum")
    @classmethod
    def flag_is_zero_or_one(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v not in (0, 1):
            raise ValueError(f"is_code_minimum must be 0 or 1, got {v!r}")
        return v


class JurisdictionalValueFile(GuidebookEntity):
    """One `data/jurisdictional_values/*.yaml` file: a section wrapper plus its records."""

    section: str
    title: str
    item_code: str
    spec_id: Optional[str] = None
    records: List[JurisdictionalValueRecord]

    @field_validator("records")
    @classmethod
    def non_empty(cls, v: List[JurisdictionalValueRecord]) -> List[JurisdictionalValueRecord]:
        # A file with no records would validate vacuously — the failure mode this
        # whole corpus was wired up to end.
        if not v:
            raise ValueError("file declares no records")
        return v
