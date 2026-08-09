"""
schemas/reasoning_doc_citation.py — synthesis-verification layer.

Mirrors the `reasoning_doc_citations` SQLite table. Its place in the
evidence-curation chain (see schemas/source_value_extraction.py for the
neighbouring links):

    source_slug_links (link)
       ↓
    source_value_extractions (per-source asserted value)
       ↓
    reasoning_doc_citations (re-read, value_match verdict — rule #10 gate)  ← this model
       ↓
    spec_value_probes (PMP walk — rule #8)
       ↓
    items.pmp_* (curated spec value)

This is the gate where a value asserted by a source is re-read against the
source itself and given a verdict. `value_match` carries that verdict for
quantified claims, `claim_match` for qualitative ones, and the table's compound
CHECK makes the pairing structural rather than conventional: a numerical or
jurisdiction-value claim must carry `claimed_value` + `value_match`, and a
qualitative or definitional claim must carry `claim_text` + `claim_match`. That
CHECK is mirrored below by `_check_claim_pairing`, so the model refuses the same
rows SQLite refuses.

WHY THIS MODEL EXISTS AT ALL
It did not, until 2026-08-09. Migration 053 added sixteen locator columns to
three tables; two had models to mirror them into and this one had none, so a
third of that migration landed in a table mirrored nowhere. The gap was found by
probe D5b (workplan/2026-08-09-locator-hierarchy-and-enforcement-probes.md) and
is the one class of drift `validate_pydantic_schemas` structurally cannot
report: it compares the columns of tables that HAVE models, so a table with no
model is invisible to it rather than failing it.

SCOPE — this mirror is COMPLETE as of schema 53. Every column in the table is
declared here. Stated explicitly, because the sibling model
(source_value_extraction.py) is a deliberate subset and a reader moving between
them should not have to infer which kind each one is.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ClaimType(str, Enum):
    """What kind of assertion the reasoning doc made. Drives which verdict
    column is required — see `_check_claim_pairing`."""
    NUMERICAL_SPEC = "numerical_spec"
    JURISDICTION_VALUE = "jurisdiction_value"
    QUALITATIVE = "qualitative"
    DEFINITIONAL = "definitional"


class ValueMatch(str, Enum):
    """Verdict for a quantified claim re-read against its source.

    PAYWALL and NOT-FOUND are outcomes, not failures to record: an
    unreachable source is a fact about retrieval, and erasing it would
    make the gap invisible.
    """
    EXACT = "EXACT"
    WITHIN_TOLERANCE = "WITHIN-TOLERANCE"
    DIFFERENT = "DIFFERENT"
    NOT_FOUND = "NOT-FOUND"
    PAYWALL = "PAYWALL"
    SUPERSEDED = "SUPERSEDED"


class ClaimMatch(str, Enum):
    """Verdict for a qualitative claim re-read against its source."""
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    NOT_FOUND = "NOT-FOUND"
    PAYWALL = "PAYWALL"
    CONTRADICTED = "CONTRADICTED"


class ReasoningDocCitation(BaseModel):
    """One citation in a reasoning doc, re-read and adjudicated."""

    citation_id: str
    reasoning_doc_slug: str            # FK -> slugs.slug
    parameter: str
    jurisdiction: Optional[str] = None
    population: Optional[str] = None

    claim_type: ClaimType
    claimed_value: Optional[str] = None
    claimed_unit: Optional[str] = None
    claim_text: Optional[str] = None

    source_ref_id: str                 # FK -> evidence_sources.ref_id
    source_section: Optional[str] = None

    value_match: Optional[ValueMatch] = None
    claim_match: Optional[ClaimMatch] = None

    # ── Locator (migration 053) ──────────────────────────────────────────────
    # The pinpoint position inside a document, decomposed. Most rows leave most
    # levels NULL: a level a document does not have is not missing data.
    # `locator_scheme` records which family's naming applies (ISO's top numbered
    # level is a CLAUSE, ADA's is a SECTION), so a reader knows whether to render
    # '§404.2' or 'clause 12.3'. The `_end` companions carry spans -- 'ADA 2010
    # §604-608' is live data. `source_section` above is the undecomposed string
    # and retires only once its values have been decomposed, not before.
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

    # ── Provenance of the verification itself ────────────────────────────────
    verified_at: str
    verified_by_session: str

    paywall_purchase_candidate: int = Field(default=0, ge=0, le=1)
    notes: Optional[str] = None
    setting: Optional[str] = None

    @model_validator(mode="after")
    def _check_claim_pairing(self):
        """Mirror the table's compound CHECK.

        Quantified and qualitative claims are adjudicated by different columns,
        and a row carrying a claim with no verdict is a citation that was never
        actually re-read. SQLite refuses those; so does this.
        """
        quantified = {ClaimType.NUMERICAL_SPEC, ClaimType.JURISDICTION_VALUE}
        if self.claim_type in quantified:
            if self.claimed_value is None or self.value_match is None:
                raise ValueError(
                    f"claim_type={self.claim_type.value} requires claimed_value "
                    f"and value_match (the re-read verdict). A quantified claim "
                    f"with no verdict was never adjudicated.")
        else:
            if self.claim_text is None or self.claim_match is None:
                raise ValueError(
                    f"claim_type={self.claim_type.value} requires claim_text "
                    f"and claim_match (the re-read verdict). A qualitative claim "
                    f"with no verdict was never adjudicated.")
        return self
