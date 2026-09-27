"""
schemas/adversarial.py — the adversarial pass and its findings.

Mirrors migration 097 (RC4, DR-2026-09-26-recurring-defect-shapes-remediation.md section 1).
An `AdversarialPass` is one antagonist run against one subject session's diff; its
`AdversarialFinding` rows are one per lens the reviewer's closing findings block names
(.claude/agents/antagonist.md, "Report shape"). `reviewer_models`/`author_models` are
lists DERIVED by the writer (scripts/db.py record-adversarial-pass) from the two
transcripts' own assistant-turn records — never hand-typed, so independence is computed
rather than asserted (CLAUDE.md rule 8).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AdversarialPass(BaseModel):
    """One antagonist run against one subject session's committed diff."""

    pass_id: Optional[int] = None
    subject_session: str = Field(..., description="bare stem of the session attacked")
    subject_commit: str = Field(..., description="the sha the reviewer read")
    reviewer_transcript: str = Field(..., description="tracked path under transcripts/")
    reviewer_models: list[str] = Field(
        default_factory=list, description="derived from the reviewer transcript's own "
        "assistant-turn model field; never typed by hand")
    author_transcript: str = Field(..., description="tracked path under transcripts/")
    author_models: list[str] = Field(default_factory=list)
    closed_at: Optional[datetime] = None
    created_by_session: Optional[str] = None
    created_at: Optional[datetime] = None


class AdversarialFinding(BaseModel):
    """One lens attacked during a pass, and its disposition."""

    finding_id: Optional[int] = None
    pass_id: int = Field(..., description="FK adversarial_passes.pass_id")
    lens: str = Field(..., description="one of the eight DR-2026-08-19 §7 lenses, or "
                       "S1-harm-reached-row / S2-mismatch-note-vs-payload / S3-containment")
    subject_table: Optional[str] = Field(
        None, description="POINTER to the row attacked (rule 5); never a copy of it")
    subject_key: Optional[str] = None
    claim_attacked: str
    method: str
    artefact: Optional[str] = Field(
        None, description="what the claim was attacked WITH (DR-2026-09-11 clause 2)")
    verdict: str = Field(..., description="SUSTAINED / SURVIVED / NOT-ATTACKED / WITHHELD-FOR-OWNER")
    severity: Optional[str] = Field(
        None, description="CRITICAL / HIGH / MEDIUM / LOW; required iff verdict=SUSTAINED")
    disposition: Optional[str] = Field(
        None, description="REPAIRED / REJECTED / PROVISIONAL-DISPUTED / OWNER-RULED")
    disposition_ref: Optional[str] = Field(
        None, description="a data migration path; a quote-anchored ledger pointer; or the reason")
    disposed_by_session: Optional[str] = None
    disposed_at: Optional[datetime] = None
    created_by_session: Optional[str] = None
    created_at: Optional[datetime] = None
