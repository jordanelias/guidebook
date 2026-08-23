"""
schemas/reference_stub.py — pre-reset bibliographic record entity model.

Mirrors the `reference_stubs` table created by migration 061. That migration exists
because `references/global-reference-registry.md` opened by declaring itself the
"Single source of truth for all references cited anywhere in the guidebook" — a
markdown file holding the role the database holds. Owner directive 2026-08-23:
anything like citation stored in .md should be recorded in a table.

TWO THINGS THIS MODEL DELIBERATELY DOES NOT HAVE, both load-bearing:

1. No `doi` and no `pmid`. Identifiers are attributes of an identifier and live in
   `source_locators`, keyed on the same `ref_id`. On 2026-08-23 this project measured
   four tables independently storing a DOI as a copied string, 17 duplicated across
   them and four already drifted by case. A fifth copy here would have reproduced
   that defect the day it was written up. Join on `ref_id`.

2. No claim to be evidence. `status` defaults to REFERENCE-ONLY. DR-2026-08-06 reset
   the corpus and ruled that resuming research does not restore the reset rows;
   admission still runs the full R1–R15 path into `evidence_sources`.

`tier_claimed` is TEXT, not an int, and is named `claimed` on purpose: the source
carries values like 'Co-1' alongside numerals, and none of them is a derived tier.
`pub_year` is TEXT because the registry carries 'n.d.' and ranges.
"""

from typing import Optional

from schemas.base import GuidebookEntity


class ReferenceStub(GuidebookEntity):
    """A pre-reset bibliographic record, held for reference and not citable."""

    ref_id: str
    authors: Optional[str] = None
    pub_year: Optional[str] = None
    title: str
    tier_claimed: Optional[str] = None
    jurisdiction: Optional[str] = None
    used_in_bpcs: Optional[str] = None
    metadata_quality: Optional[str] = None
    status: str = "REFERENCE-ONLY"
    recovered_from: str
    notes: Optional[str] = None
