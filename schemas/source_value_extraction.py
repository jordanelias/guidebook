"""
schemas/source_value_extraction.py — per-source extracted-value layer.

Mirrors the source_value_extractions SQLite table introduced by
migration 018 per DR-2026-05-28-b. Sits between the bare-link layer
(source_slug_links) and the synthesis-verification layer
(reasoning_doc_citations) in the evidence-curation chain:

    source_slug_links (link)
       ↓
    source_value_extractions (per-source asserted value)  ← this model
       ↓
    reasoning_doc_citations (re-read, value_match verdict — rule #10 gate)
       ↓
    spec_value_probes (PMP walk — rule #8)
       ↓
    items.pmp_* (curated spec value)

An extraction with extraction_status='verified' and a non-null
promoted_to_rdc_id is the bridge: the extraction has graduated to the
synthesis layer and the reasoning-doc cell points back via citation_id.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ClaimType(str, Enum):
    NUMERICAL = "numerical"
    RANGE = "range"
    QUALITATIVE = "qualitative"
    FRAMEWORK = "framework"
    ABSENT = "absent"  # source linked to topic/parameter but asserts no value


class ExtractionMethod(str, Enum):
    SKIM = "skim"
    FULL_READ = "full-read"
    RE_READ = "re-read"
    AUTO_MINED = "auto-mined"


class ExtractionStatus(str, Enum):
    PRELIMINARY = "preliminary"
    REVIEWED = "reviewed"
    VERIFIED = "verified"
    CONTRADICTED = "contradicted"
    ABSENT_CONFIRMED = "absent-confirmed"


class SourceValueExtraction(BaseModel):
    """One per-source asserted-value row.

    Records what a single evidence source asserts for a given parameter,
    population, and jurisdiction — captured during mining, before
    rule #10 re-read verification.
    """

    extraction_id: Optional[int] = None  # autoincrement PK

    # Provenance
    ref_id: str = Field(..., description="FK evidence_sources.ref_id")
    slug: str = Field(..., description="topic; matches source_slug_links.slug")

    # What is being extracted
    parameter: str = Field(..., description='e.g. "RT60", "door clear width"')
    parameter_canonical: Optional[str] = None  # normalized for join (lowercase, hyphens)
    population_code: Optional[str] = None  # FK populations.population_code
    population_label: Optional[str] = None  # free-text qualifier
    jurisdiction: Optional[str] = None  # "UK","US","Multi", or None for clinical

    # The asserted claim
    claim_type: ClaimType
    claimed_value: Optional[str] = None
    claimed_unit: Optional[str] = None
    claim_text: Optional[str] = None  # exact source phrasing
    source_section: Optional[str] = None  # "Table 6, p.33"

    # Provenance of the extraction itself
    extraction_method: ExtractionMethod
    extraction_status: ExtractionStatus = ExtractionStatus.PRELIMINARY

    # Bridge to synthesis layer
    promoted_to_rdc_id: Optional[str] = None  # FK reasoning_doc_citations.citation_id

    notes: Optional[str] = None

    # Audit
    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by_session: Optional[str] = None

    @model_validator(mode="after")
    def _value_consistency(self):
        # Mirror the SQL CHECK: claim_type='absent' ↔ claimed_value IS NULL
        if self.claim_type == ClaimType.ABSENT and self.claimed_value is not None:
            raise ValueError("claim_type='absent' requires claimed_value to be None")
        if self.claim_type != ClaimType.ABSENT and self.claimed_value is None:
            raise ValueError(
                f"claim_type='{self.claim_type.value}' requires claimed_value to be set"
            )
        return self
