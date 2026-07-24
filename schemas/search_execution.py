"""
schemas/search_execution.py — the coverage-loop logged-search event table
(migration 033). Mirrors the SQLite `search_executions` table; schema<->SQLite
drift is a CI-caught bug.

One row = one executed search. Coverage is DERIVED from these rows via the
v_coverage_jurisdiction / v_coverage_language / v_coverage_branch views, never
hand-written — the un-fakeable substrate the coverage-completion loop
(coverage-completion-loop-methodology §4, search-coverage-completion-workplan §2.2)
requires. `deferred_reason` makes an honest non-search a first-class counted outcome;
`admitted_ref_ids` back-links each admitted source to the exact search that found it
(chain of custody + auditable spillover routing); `backfill=1` isolates the recoverable
historical queries from forward loop rows; `executed_at` is an explicit ISO string so
rebuild is byte-deterministic.

Per DR-2026-07-24-search-executions-substrate (D-SCHEMA / DG-REVIEW, ratified 2026-07-24).
"""

from typing import Optional

from pydantic import BaseModel, Field


class SearchExecution(BaseModel):
    """One executed search — the coverage-loop event log row (migration 033)."""

    exec_id: Optional[int] = None
    slug: str = Field(..., description="FK slugs.slug")
    jurisdiction: Optional[str] = None            # NULL = jurisdiction-agnostic search
    language: str = Field(..., description="ISO; one of the 19 research languages")
    # hierarchy branch the search TARGETED (diffable against what was FOUND):
    target_tier: Optional[int] = Field(None, ge=1, le=6)
    target_evidence_type: Optional[str] = None    # clinical|sr_meta|standard_eb|national_fw|code|co1|co2|grey
    target_scope: Optional[str] = None            # intrinsic|lower_control|high_control|national|international
    # the verbatim, replayable query:
    query_text: str
    terms_used: Optional[str] = None              # JSON array of term ids
    engine: str                                   # pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual
    # depth as real method, not booleans:
    depth_method: str                             # scoping|systematic
    mining_direction: Optional[str] = None        # none|backward|forward|both
    # yield:
    results_found: int = 0
    results_screened: int = 0
    results_admitted: int = 0
    saturation_signal: Optional[str] = None       # none|partial|saturated
    admitted_ref_ids: Optional[str] = None        # JSON array of evidence_sources.ref_id
    deferred_reason: Optional[str] = None          # non-NULL => deliberate no-search for this cell
    backfill: int = 0
    session: str
    executed_at: str                              # explicit ISO timestamp
