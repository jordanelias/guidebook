"""
schemas/evidence_source.py — Evidence Source entity model.

Represents a single citable source in the global reference registry.
Per T-03: each source carries both a tier (1–6) and an evidence_type,
encoding the clinical-evidence position and the kind of evidence as
two orthogonal dimensions.

Cross-entity relationships:
- used_in_slugs → links to BPC entries (ENT-03)
- local_ref_ids → links to per-BPC reference tables
- ref_id → cited by Specification evidence basis
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import GuidebookEntity
from schemas.enums import Co1Provenance, Co1SourceType, EvidenceType, VerificationStatus


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
    verification_status: Optional[VerificationStatus] = None

    # Co-1 fields (A5 §6.1 — required when evidence_type == co1)
    co1_provenance: Optional[Co1Provenance] = None
    co1_source_type: Optional[Co1SourceType] = None
    synthesis_attribution_required: Optional[bool] = None

    # Notes
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("ref_id")
    @classmethod
    def valid_ref_id(cls, v: str) -> str:
        if not re.match(r"^(REF-\d{5}|Co1-\d{2,3})$", v):
            raise ValueError(f"ref_id must match REF-NNNNN or Co1-NN, got: {v}")
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

    @model_validator(mode="after")
    def co1_field_consistency(self) -> "EvidenceSource":
        """Enforce A5 §6.1: Co-1 sources require Co-1-specific fields."""
        et = self.evidence_type
        if isinstance(et, str):
            is_co1 = et == "co1"
        else:
            is_co1 = et == EvidenceType.CO1

        if is_co1:
            if self.tier is not None and self.tier != 1:
                raise ValueError(
                    f"Co-1 source must have tier=1 (co-primary), got tier={self.tier}"
                )
            if self.co1_provenance is None:
                raise ValueError(
                    "Co-1 source requires co1_provenance field (A5 §6.1)"
                )
            if self.co1_source_type is None:
                raise ValueError(
                    "Co-1 source requires co1_source_type field (A5 §6.1)"
                )
        else:
            # Non-Co-1 sources must not carry Co-1-specific fields
            if self.co1_provenance is not None:
                raise ValueError(
                    f"co1_provenance is only valid for Co-1 sources, "
                    f"but evidence_type={et}"
                )
            if self.co1_source_type is not None:
                raise ValueError(
                    f"co1_source_type is only valid for Co-1 sources, "
                    f"but evidence_type={et}"
                )
        return self
