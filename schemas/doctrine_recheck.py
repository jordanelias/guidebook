"""
schemas/doctrine_recheck.py — Doctrine recheck records (per governance/doctrine-recheck.md, A13).

- RecheckSession: container record per recheck (RC-NNN)
- RecheckFinding: a single finding within a recheck (RC-NNN-FF)
- ContaminationSample: one sampled BPC per recheck (associated by recheck_id)
- DoctrineSnapshot: point-in-time inventory of CANONICAL governance + RULEs + decisions
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import GuidebookEntity
from schemas.enums import (
    ContaminationDisposition,
    RecheckFindingSeverity,
    RecheckFindingStatus,
    RecheckTrigger,
)
from schemas.temporal import DATETIME_PATTERN, DATE_ONLY_PATTERN

# --- Format patterns ---

RECHECK_ID_PATTERN = re.compile(r"^RC-\d{3,4}$")
FINDING_ID_PATTERN = re.compile(r"^RC-\d{3,4}-\d{2,3}$")


# --- Entities ---

class RecheckFinding(GuidebookEntity):
    """A single finding within a recheck session."""

    finding_id: str  # RC-NNN-FF
    severity: RecheckFindingSeverity
    pass_id: str  # 2.2 / 2.3 / 2.4 / 2.5 / 2.6
    description: str
    affected_artifacts: list[str] = []
    recommended_action: str
    status: RecheckFindingStatus = RecheckFindingStatus.OPEN
    resolution_commit: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("finding_id")
    @classmethod
    def valid_finding_id(cls, v: str) -> str:
        if not FINDING_ID_PATTERN.match(v):
            raise ValueError(f"finding_id must match RC-NNN-FF, got: '{v}'")
        return v

    @field_validator("pass_id")
    @classmethod
    def valid_pass(cls, v: str) -> str:
        if v not in {"2.2", "2.3", "2.4", "2.5", "2.6"}:
            raise ValueError(
                f"pass_id must be one of 2.2–2.6, got: '{v}'"
            )
        return v

    @model_validator(mode="after")
    def resolution_consistency(self) -> "RecheckFinding":
        status_val = (
            self.status if isinstance(self.status, str) else self.status.value
        )
        if status_val == "RESOLVED" and not self.resolution_commit:
            raise ValueError(
                "RESOLVED finding requires resolution_commit"
            )
        if status_val != "RESOLVED" and self.resolution_commit:
            raise ValueError(
                f"resolution_commit only on RESOLVED, got status={status_val}"
            )
        return self


class ContaminationSample(GuidebookEntity):
    """One sampled BPC within a recheck's contamination resampling pass."""

    recheck_id: str
    bpc_path: str
    topic_group: str
    disposition: ContaminationDisposition
    disposition_rationale: str
    reviewer: str
    review_date: str  # YYYY-MM-DD HH:MM

    @field_validator("recheck_id")
    @classmethod
    def valid_recheck_id(cls, v: str) -> str:
        if not RECHECK_ID_PATTERN.match(v):
            raise ValueError(f"recheck_id must match RC-NNN, got: '{v}'")
        return v

    @field_validator("review_date")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"review_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v


class RecheckSession(GuidebookEntity):
    """Container record per recheck session.

    Stored at data/doctrine_recheck/recheck_{YYYY-MM-DD}.yaml.
    """

    recheck_id: str
    trigger: RecheckTrigger
    trigger_detail: str  # session count / stage tag / rule_id
    recheck_date: str
    recheck_by: str
    model_routing: str  # per A12 §4
    passes_run: list[str]  # subset of {"2.2", "2.3", "2.4", "2.5", "2.6"}
    findings: list[RecheckFinding] = []
    contamination_samples: list[ContaminationSample] = []
    drift_summary: dict = {}
    contamination_summary: dict = {}
    next_recheck_due: Optional[str] = None  # trigger condition for next
    notes: Optional[str] = None

    @field_validator("recheck_id")
    @classmethod
    def valid_recheck_id(cls, v: str) -> str:
        if not RECHECK_ID_PATTERN.match(v):
            raise ValueError(f"recheck_id must match RC-NNN, got: '{v}'")
        return v

    @field_validator("recheck_date")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"recheck_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @field_validator("model_routing")
    @classmethod
    def valid_model_routing(cls, v: str) -> str:
        # Match A12 §4 notation
        from schemas.decision import MODEL_ROUTING_PATTERN
        if not MODEL_ROUTING_PATTERN.match(v):
            raise ValueError(
                f"model_routing must match A12 §4 notation, got: '{v}'"
            )
        return v

    @field_validator("passes_run")
    @classmethod
    def valid_passes(cls, v: list[str]) -> list[str]:
        valid = {"2.2", "2.3", "2.4", "2.5", "2.6"}
        for p in v:
            if p not in valid:
                raise ValueError(f"pass_id must be one of {valid}, got: '{p}'")
        if not v:
            raise ValueError("passes_run cannot be empty")
        return v

    @model_validator(mode="after")
    def findings_belong_to_recheck(self) -> "RecheckSession":
        for f in self.findings:
            if not f.finding_id.startswith(self.recheck_id + "-"):
                raise ValueError(
                    f"finding_id '{f.finding_id}' does not belong to "
                    f"recheck '{self.recheck_id}'"
                )
        return self

    @model_validator(mode="after")
    def samples_belong_to_recheck(self) -> "RecheckSession":
        for s in self.contamination_samples:
            if s.recheck_id != self.recheck_id:
                raise ValueError(
                    f"contamination_sample.recheck_id '{s.recheck_id}' does not "
                    f"match recheck_id '{self.recheck_id}'"
                )
        return self

    @model_validator(mode="after")
    def trigger_detail_format(self) -> "RecheckSession":
        """Validate trigger_detail format by trigger type."""
        trigger_val = (
            self.trigger if isinstance(self.trigger, str) else self.trigger.value
        )
        if trigger_val == "PERIODIC":
            # trigger_detail should be a session count (integer string)
            if not self.trigger_detail.strip().isdigit():
                raise ValueError(
                    f"trigger=PERIODIC requires trigger_detail as session count, "
                    f"got: '{self.trigger_detail}'"
                )
        elif trigger_val == "STAGE_TRANSITION":
            # trigger_detail should be a stage transition tag like "A->B"
            if "->" not in self.trigger_detail:
                raise ValueError(
                    f"trigger=STAGE_TRANSITION requires trigger_detail as "
                    f"stage tag (e.g., 'A->B'), got: '{self.trigger_detail}'"
                )
        elif trigger_val == "RULE_REVISION":
            # trigger_detail should reference a rule (RULE-... or section ref)
            if not self.trigger_detail.strip():
                raise ValueError(
                    "trigger=RULE_REVISION requires trigger_detail as rule reference"
                )
        return self


class DoctrineSnapshot(GuidebookEntity):
    """Point-in-time inventory of CANONICAL governance, RULEs, and decisions.

    Stored at data/doctrine_recheck/snapshot_{YYYY-MM-DD}.yaml.
    """

    snapshot_date: str  # YYYY-MM-DD HH:MM
    governance_docs: list[str]  # paths to CANONICAL governance docs
    canonical_rules: list[str]  # one-line summaries of CANONICAL RULEs
    decision_ids: list[str]  # ACTIVE Decision IDs from register
    bpc_count: int  # total BPC files at snapshot time

    @field_validator("snapshot_date")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"snapshot_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @field_validator("bpc_count")
    @classmethod
    def non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError(f"bpc_count must be ≥0, got: {v}")
        return v
