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

SCOPE — this model is a DELIBERATE SUBSET, not a complete mirror.
The SQLite table has 33 columns; this model declares 22. Missing, all added
by later migrations that never reached here: root_id, root_type, root_ref_id,
root_population_note, root_classification_basis, echo_of, measurement_paradigm,
device_class, contested, file_anchor, setting. Those carry the value-genealogy
and independence-scoring layer, and mirroring them means mirroring three CHECK
vocabularies — real work with its own review surface, tracked as F5 in
workplan/2026-08-03-fork-cut-walkable-graph-execution-plan.md. `item_code`
(migration 052) IS declared below, because it is the hop-4 edge itself and a
model silently missing it would misrepresent the chain this docstring draws.
Stated here rather than left implicit: a reader should not infer from one
added field that the mirror is whole.
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
    item_code: Optional[str] = Field(
        None,
        description="FK items.item_code (migration 052). NULL means the item was "
                    "not established at extraction — `parameter` alone cannot "
                    "resolve it (A-18 and A-10b are both RT60).",
    )
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

    # ── Pinpoint locator (schema 053) ────────────────────────────────────────
    # A code or standard is cited at a hierarchical position inside it. These
    # mirror the DB columns 1:1; most are NULL on most rows, because a level a
    # document does not have is not missing data. `locator_scheme` records which
    # family's naming applies (ISO's top numbered level is a CLAUSE, ADA's is a
    # SECTION), so a reader knows whether to render '§404.2' or 'clause 12.3'.
    # The `_end` companions carry spans -- 'ADA 2010 §604-608' is live data.
    locator_scheme: Optional[str] = None
    loc_division: Optional[str] = None
    loc_part: Optional[str] = None
    loc_section: Optional[str] = None
    loc_subsection: Optional[str] = None
    loc_paragraph: Optional[str] = None
    loc_clause: Optional[str] = None
    loc_subclause: Optional[str] = None
    loc_division_end: Optional[str] = None
    loc_part_end: Optional[str] = None
    loc_section_end: Optional[str] = None
    loc_subsection_end: Optional[str] = None
    loc_paragraph_end: Optional[str] = None
    loc_clause_end: Optional[str] = None
    loc_subclause_end: Optional[str] = None
    loc_note: Optional[str] = None


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
