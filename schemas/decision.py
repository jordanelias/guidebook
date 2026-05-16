"""
schemas/decision.py — Decision protocol (per governance/decision-protocol.md, A12).

- Decision: a single decision record (D-NNNN)
- DecisionRegister: the singleton register at data/decisions/decision_register.yaml

Decision IDs follow the D-NNNN convention (zero-padded to 4 digits).
The model_routing field follows the §4.4 standardised notation that resolves L-05.
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import GuidebookEntity
from schemas.enums import (
    DecisionCategory,
    DecisionReviewStatus,
    DecisionStatus,
    DelegationCategory,
)
from schemas.temporal import DATETIME_PATTERN

# --- Format patterns ---

DECISION_ID_PATTERN = re.compile(r"^D-\d{4,5}$")

# Per governance/decision-protocol.md §4.4
MODEL_ROUTING_PATTERN = re.compile(
    r"^(opus|sonnet|haiku|human|legacy)/(200|150|125|100|75|50|none)/"
    r"(synth|arbitrate|extract|format|route|none)$"
)

VALID_EFFORT_LEVELS = {200, 150, 125, 100, 75, 50}


# --- Entity ---

class Decision(GuidebookEntity):
    """A single decision record per governance/decision-protocol.md §3.2."""

    decision_id: str  # D-NNNN
    category: DecisionCategory
    delegation: DelegationCategory
    delegation_rationale: Optional[str] = None
    summary: str
    outcome: str
    rationale: str
    alternatives_considered: list[str] = []
    decision_date: str  # YYYY-MM-DD HH:MM
    decided_by: str
    model_routing: str  # see §4.4
    effort_level: int  # one of VALID_EFFORT_LEVELS or 0 (=none)
    decision_artifacts: list[str] = []
    predecessors: list[str] = []
    supersedes: list[str] = []
    status: DecisionStatus = DecisionStatus.ACTIVE
    review_status: DecisionReviewStatus
    notes: Optional[str] = None

    @field_validator("decision_id")
    @classmethod
    def valid_decision_id(cls, v: str) -> str:
        if not DECISION_ID_PATTERN.match(v):
            raise ValueError(f"decision_id must match D-NNNN, got: '{v}'")
        return v

    @field_validator("decision_date")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"decision_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @field_validator("model_routing")
    @classmethod
    def valid_model_routing(cls, v: str) -> str:
        if not MODEL_ROUTING_PATTERN.match(v):
            raise ValueError(
                f"model_routing must match {{opus|sonnet|haiku|human|legacy}}/"
                f"{{200|150|125|100|75|50|none}}/{{synth|arbitrate|extract|format|"
                f"route|none}}, got: '{v}'"
            )
        return v

    @field_validator("effort_level")
    @classmethod
    def valid_effort(cls, v: int) -> int:
        if v != 0 and v not in VALID_EFFORT_LEVELS:
            raise ValueError(
                f"effort_level must be one of {VALID_EFFORT_LEVELS} or 0 (=none), "
                f"got: {v}"
            )
        return v

    @field_validator("predecessors", "supersedes")
    @classmethod
    def valid_id_refs(cls, v: list[str]) -> list[str]:
        for ref in v:
            if not DECISION_ID_PATTERN.match(ref):
                raise ValueError(
                    f"decision_id reference must match D-NNNN, got: '{ref}'"
                )
        return v

    @model_validator(mode="after")
    def review_status_consistent(self) -> "Decision":
        """DG-NON and DG-AUTO -> review_status=NA; DG-REVIEW -> PENDING/CONFIRMED."""
        deleg_val = (
            self.delegation
            if isinstance(self.delegation, str)
            else self.delegation.value
        )
        review_val = (
            self.review_status
            if isinstance(self.review_status, str)
            else self.review_status.value
        )
        if deleg_val in {"DG-NON", "DG-AUTO"} and review_val != "NA":
            raise ValueError(
                f"delegation={deleg_val} requires review_status=NA, "
                f"got: {review_val}"
            )
        if deleg_val == "DG-REVIEW" and review_val == "NA":
            raise ValueError(
                "delegation=DG-REVIEW requires review_status=PENDING or CONFIRMED, "
                "not NA"
            )
        return self

    @model_validator(mode="after")
    def alternatives_required_for_doctrinal(self) -> "Decision":
        """Per §3.2: alternatives_considered required for D-DOCT and D-METH."""
        cat_val = (
            self.category if isinstance(self.category, str) else self.category.value
        )
        # D-METH for new methodology requires alternatives; for application of existing,
        # not necessarily. We make the strict check on D-DOCT only; D-METH validation
        # is C3-rationale-length warning territory at the validator script.
        if cat_val == "D-DOCT" and not self.alternatives_considered:
            raise ValueError(
                "category=D-DOCT requires alternatives_considered (per §3.2)"
            )
        return self

    @model_validator(mode="after")
    def delegation_rationale_required_on_departure(self) -> "Decision":
        """Per §2.3: departure from default delegation requires rationale."""
        # We cannot mechanically determine "default" delegation without knowing
        # the §2.2 table here at field-validator time. The validator script (C8)
        # checks this cross-reference. At schema-time, we only require that
        # delegation_rationale is non-empty when present, and that DG-AUTO
        # decisions in D-DOCT/D-METH categories provide a rationale (clear
        # default departure).
        cat_val = (
            self.category if isinstance(self.category, str) else self.category.value
        )
        deleg_val = (
            self.delegation if isinstance(self.delegation, str) else self.delegation.value
        )
        if cat_val in {"D-DOCT", "D-METH"} and deleg_val == "DG-AUTO":
            if not self.delegation_rationale:
                raise ValueError(
                    f"category={cat_val} with delegation=DG-AUTO is a default "
                    f"departure (default is DG-NON); delegation_rationale required."
                )
        return self


class DecisionRegister(GuidebookEntity):
    """The singleton decision register.

    Stored at data/decisions/decision_register.yaml.
    """

    register_version: int
    last_updated: str  # YYYY-MM-DD HH:MM
    decisions: list[Decision]

    @field_validator("register_version")
    @classmethod
    def positive_version(cls, v: int) -> int:
        if v < 1:
            raise ValueError(f"register_version must be ≥1, got: {v}")
        return v

    @field_validator("last_updated")
    @classmethod
    def valid_last_updated(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"last_updated must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @model_validator(mode="after")
    def unique_decision_ids(self) -> "DecisionRegister":
        """No duplicate decision_ids."""
        seen: set[str] = set()
        for d in self.decisions:
            if d.decision_id in seen:
                raise ValueError(f"duplicate decision_id: {d.decision_id}")
            seen.add(d.decision_id)
        return self

    @model_validator(mode="after")
    def supersedes_resolves(self) -> "DecisionRegister":
        """Every supersedes ref must resolve to a record in the register; the
        referenced record must have status=SUPERSEDED."""
        ids = {d.decision_id: d for d in self.decisions}
        for d in self.decisions:
            for sup_id in d.supersedes:
                if sup_id not in ids:
                    raise ValueError(
                        f"{d.decision_id}.supersedes references {sup_id}, "
                        f"which is not in the register"
                    )
                target = ids[sup_id]
                target_status = (
                    target.status
                    if isinstance(target.status, str)
                    else target.status.value
                )
                if target_status != "SUPERSEDED":
                    raise ValueError(
                        f"{d.decision_id}.supersedes references {sup_id}, "
                        f"but {sup_id} has status={target_status} (expected SUPERSEDED)"
                    )
        return self

    @model_validator(mode="after")
    def predecessors_resolve(self) -> "DecisionRegister":
        """Every predecessor ref must resolve to a record in the register."""
        ids = {d.decision_id for d in self.decisions}
        for d in self.decisions:
            for pred_id in d.predecessors:
                if pred_id not in ids:
                    raise ValueError(
                        f"{d.decision_id}.predecessors references {pred_id}, "
                        f"which is not in the register"
                    )
        return self
