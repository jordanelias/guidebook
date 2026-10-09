"""
schemas/extraction_follow_up.py — an open-until-resolved follow-up on an extraction.

Mirrors `extraction_follow_ups` (migration 105, tooling T1). The owner's answer to D1,
2026-10-09: "D1: yes figure from source filed by another slug allowed. skimmed values are
not publishable", read with the earlier "should be yes, but we still tag it for follow up
later" (catalogue-plan-v2 Addendum 1). A figure read outside the purpose its source was
admitted for may set a published value, tagged for a reviewer to re-check; nothing can
derive that tag (no slug-to-parameter map exists, and one would be curation, CLAUDE.md
rule 8), so it is recorded as a judgement with its warrant.

`reason` is plain str, owned by the table's CHECK (one value today,
`read-outside-admitting-purpose`; a second is a schema change with its ruling). The
resolution triple is all-or-nothing, mirrored below as the table's CHECK is.

WHAT READS THIS MODEL: scripts/audit/validate_pydantic_schemas.py. Writers: `db.py
raise-follow-up` / `resolve-follow-up`. The table's reader is
scripts/audit/extraction_follow_up_audit.py.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator


class ExtractionFollowUp(BaseModel):
    """One follow-up on one extraction. Mirrors `extraction_follow_ups` (105)."""

    model_config = ConfigDict(extra="forbid")

    follow_up_id: Optional[int] = None     # AUTOINCREMENT
    extraction_id: int
    reason: str                            # CHECK-owned vocabulary
    warrant: str
    raised_at: Optional[str] = None
    raised_by_session: Optional[str] = None
    resolved_at: Optional[str] = None
    resolved_by_session: Optional[str] = None
    resolution: Optional[str] = None

    @model_validator(mode="after")
    def shape(self) -> "ExtractionFollowUp":
        """Mirrors the table's CHECKs: a warrant, and an all-or-nothing resolution."""
        if not self.warrant.strip():
            raise ValueError("warrant is blank -- a follow-up that cannot say why "
                             "cannot be acted on")
        resolved = [self.resolved_at, self.resolved_by_session, self.resolution]
        if any(v is not None for v in resolved) and not all(
                v is not None and str(v).strip() for v in resolved):
            raise ValueError("a resolution needs resolved_at, resolved_by_session and a "
                             "non-blank resolution together")
        return self
