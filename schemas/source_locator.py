"""
schemas/source_locator.py — the clue store entity model.

Mirrors `source_locators` as merged by migration 062. It began as
schemas/reference_stub.py, mirroring a table created hours earlier by migration 061 and
dropped by 062 for duplicating this one on the same primary key.

CORRECTION 2026-08-24. An earlier version of this docstring cited an "owner directive 2026-08-23:
anything like citation stored in .md should be recorded in a table". THE OWNER DID NOT GIVE THAT
DIRECTIVE - "that was machine bundled without my notice". Migration 061 was built on an authority
that did not exist, and 061's header still carries the false attribution because migrations are
append-only (CLAUDE.md 0.3); the correction lives in
decisions/DR-2026-08-24-scaffolding-is-phase-specific.md 1.

WHAT THIS TABLE IS. Clues, in the owner's words 2026-08-23: "not stored as usable for any
case unless it is being read by a researcher." A researcher reads a row to decide what to
search for. Nothing joins it, no determination may cite it, and it is NOT evidence —
DR-2026-08-06 demoted this material and ruled that resuming research does not restore it.
`status` defaults to REFERENCE-ONLY and admission runs the full R1-R15 path into
`evidence_sources`.

WHY EVERY FIELD IS OPTIONAL EXCEPT THE KEY. The table is a full outer join of what two
tables held before 062: 344 rows carry identifiers and no bibliography, 32 carry a title
and no identifier, 499 carry both. The table CHECK requires an identifier OR a title, so a
title-only clue is legal — that is the ordinary shape of a standards reference — while a
wholly empty row is not. 061 could not express that, which is why it invented a second
table for the 32.

THE ONE MACHINE USE THAT SURVIVES is duplicate detection: R9a/R9b in
scripts/audit/research_batch_dod.py ask whether an identifier is already held here. That
is a question ABOUT the stash, not a claim made FROM it, and it is what OD-5 existed to
enable. Any wider machine use needs a ruling first.
"""

from typing import Optional

from schemas.base import GuidebookEntity


class SourceLocator(GuidebookEntity):
    """A research clue: a held identifier, a bibliographic stub, or both."""

    ref_id: str
    doi: Optional[str] = None
    url: Optional[str] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None
    isbn: Optional[str] = None
    issn: Optional[str] = None
    standard_number: Optional[str] = None
    doi_resolution_outcome: Optional[str] = None
    url_resolution_outcome: Optional[str] = None
    url_last_fetched: Optional[str] = None
    recovered_from: str
    authors: Optional[str] = None
    pub_year: Optional[str] = None
    title: Optional[str] = None
    tier_claimed: Optional[str] = None
    jurisdiction: Optional[str] = None
    used_in_bpcs: Optional[str] = None
    status: str = "REFERENCE-ONLY"
    notes: Optional[str] = None
