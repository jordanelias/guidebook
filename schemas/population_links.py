"""
schemas/population_links.py — value-claim population junction tables.

Mirrors the three junction tables added by migration 021 per the owner
directive of 2026-05-28 ("improve schema so that sqlite can accommodate
everything flagged properly"). Each links a value-claim row to one canonical
population code; a claim applying to N populations has N rows.

These extend the project's established population-junction idiom
(item_population_links, evidence_population_match) to the value-claim tables:

    reasoning_doc_citations  --(citation_population_links)-->  populations
    spec_value_probes        --(probe_population_links)----->  populations
    source_value_extractions --(extraction_population_links)->  populations

The population_code FK to populations(population_code) makes population
validity structurally enforced; compound populations (e.g. NDV + AUT) are
first-class multi-row sets rather than comma-separated strings.

The scalar population / population_code columns on the parent tables are
deprecated transition aliases kept in sync; the junction is authoritative.
scripts/audit/population_integrity_audit.py enforces scalar<->junction
consistency (Level 2).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CitationPopulationLink(BaseModel):
    """One (reasoning_doc_citation, population) membership row."""

    citation_id: str = Field(..., description="FK reasoning_doc_citations.citation_id")
    population_code: str = Field(..., description="FK populations.population_code")
    note: Optional[str] = None  # optional per-population qualifier
    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None


class ProbePopulationLink(BaseModel):
    """One (spec_value_probe, population) membership row."""

    probe_id: str = Field(..., description="FK spec_value_probes.probe_id")
    population_code: str = Field(..., description="FK populations.population_code")
    note: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None


class ExtractionPopulationLink(BaseModel):
    """One (source_value_extraction, population) membership row."""

    extraction_id: int = Field(..., description="FK source_value_extractions.extraction_id")
    population_code: str = Field(..., description="FK populations.population_code")
    note: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by_session: Optional[str] = None
