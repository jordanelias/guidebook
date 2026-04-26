"""
schemas/evidence_source.py — Evidence Source entity model.

Represents a single citable source in the global reference registry.
Per T-03: each source carries both a tier (1–6) and an evidence_type,
encoding the clinical-evidence position and the kind of evidence as
two orthogonal dimensions.

Cross-entity relationships:
- used_in_slugs → links to BPC entries (E-03)
- local_ref_ids → links to per-BPC reference tables
- ref_id → cited by Specification evidence basis
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity
from schemas.enums import EvidenceType


class EvidenceSource(GuidebookEntity):
    """A single citable source in the guidebook evidence base.

    531 records in the global reference registry. Each record is a unique
    publication, standard, guideline, or grey literature source.
    """

    # Identity
    ref_id: str  # REF-NNNNN (global, stable)

    # Bibliographic
    authors: str
    year: Optional[str] = None
    title: str
    doi: Optional[str] = None
    pmid: Optional[str] = None

    # Evidence classification (T-03: two orthogonal dimensions)
    tier: Optional[int] = None  # 1–6 per evidence hierarchy
    evidence_type: EvidenceType = EvidenceType.UNKNOWN

    # Jurisdiction
    jurisdiction: Optional[str] = None  # JurisdictionCode or "INT" for international

    # Cross-references
    used_in_slugs: list[str] = []  # BPC slugs citing this source
    local_ref_ids: list[str] = []  # slug:local_id format

    # Metadata quality
    metadata_quality: Optional[str] = None  # COMPLETE, PMID-ONLY, GREY, AUTHOR-TITLE-ONLY

    # Verification
    verification_status: Optional[str] = None  # VERIFIED, UNVERIFIED, RETRACTED

    # Notes
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("ref_id")
    @classmethod
    def valid_ref_id(cls, v: str) -> str:
        if not re.match(r"^REF-\d{5}$", v):
            raise ValueError(f"ref_id must match REF-NNNNN, got: {v}")
        return v

    @field_validator("tier")
    @classmethod
    def valid_tier(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1 or v > 6):
            raise ValueError(f"tier must be 1–6, got: {v}")
        return v

    @field_validator("doi")
    @classmethod
    def normalize_doi(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if v == "":
                return None
            # Strip common prefixes
            v = re.sub(r"^https?://doi\.org/", "", v)
            v = re.sub(r"^doi:", "", v, flags=re.IGNORECASE)
        return v

    @field_validator("pmid")
    @classmethod
    def normalize_pmid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if v == "":
                return None
        return v

    @field_validator("local_ref_ids")
    @classmethod
    def valid_local_ref_format(cls, v: list[str]) -> list[str]:
        for ref in v:
            if ":" not in ref:
                raise ValueError(
                    f"local_ref_id must be 'slug:local_id' format, got: '{ref}'"
                )
        return v
