"""
schemas/population_links.py — value-claim population junction tables.

Mirrors the three junction tables added by migration 021 per the owner
directive of 2026-05-28 ("improve schema so that sqlite can accommodate
everything flagged properly"). Each links a value-claim row to one canonical
population code; a claim applying to N populations has N rows.

These extend the project's established population-junction idiom
(item_taxonomy_links, evidence_population_match) to the value-claim tables:

    reasoning_doc_citations  --(citation_population_links)-->  populations
    source_value_extractions --(extraction_population_links)->  populations

The population_code FK to populations(population_code) makes population
validity structurally enforced; compound populations (e.g. NDV + AUT) are
first-class multi-row sets rather than comma-separated strings.

The scalar population / population_code columns on the parent tables are
deprecated transition aliases kept in sync; the junction is authoritative.
population_integrity_audit.py, which enforced scalar<->junction consistency, was
deleted in plan step 1.2; probe_population_links went with spec_value_probes.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CitationPopulationLink(BaseModel):
    """One (reasoning_doc_citation, population) membership row."""

    citation_id: str = Field(..., description="FK reasoning_doc_citations.citation_id")
    population_code: str = Field(..., description="FK populations.population_code")
    notes: Optional[str] = None  # optional per-population qualifier
    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None


class ExtractionPopulationLink(BaseModel):
    """One (source_value_extraction, population) membership row."""

    extraction_id: int = Field(..., description="FK source_value_extractions.extraction_id")
    population_code: str = Field(..., description="FK populations.population_code")
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None
