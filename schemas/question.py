"""
schemas/question.py — Question entity model (stub).

Represents a question in the questions-led teaching mode (DC-6).
Each question maps to one or more specifications that answer it.

STUB: This schema is specified in D-0139 §3.4 for storage-form
completeness. Full question entity specification is a B3 deliverable
(B3.2 website entity specification + B3.3 template specification).

The question_heading field on the specification table (D-0139 Amendment 1)
holds the per-spec question form; the Question entity here is the
standalone question object for the questions-led navigation mode.
"""

import re
from typing import Optional

from pydantic import field_validator

from schemas.base import GuidebookEntity


class Question(GuidebookEntity):
    """A question entity for the questions-led navigation mode.

    Questions are the primary entry surface for the questions-led
    teaching mode. Each question maps to specifications that answer it,
    with an answer_role indicating whether the spec is primary, partial,
    or related.

    B3 will specify: question taxonomy, question-to-audience mapping,
    question ordering per design stage, and question-mode page template.
    """

    # Identity
    question_id: str  # "Q-NNNN"
    question_text: str  # The question, e.g. "Can two power wheelchairs pass?"

    # Classification
    applies_to_population: Optional[str] = None  # PopulationCode or None (universal)
    parameter_class: Optional[str] = None  # A3 §1.4 hierarchical class
    design_stage: Optional[str] = None  # When in design this question arises

    # Status
    status: str = "DRAFT"  # DRAFT, ACTIVE, RETIRED

    # Metadata
    created_at: Optional[str] = None
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("question_id")
    @classmethod
    def valid_question_id(cls, v: str) -> str:
        if not re.match(r"^Q-\d{4}$", v):
            raise ValueError(f"question_id must match Q-NNNN, got: '{v}'")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        if v not in ("DRAFT", "ACTIVE", "RETIRED"):
            raise ValueError(f"status must be DRAFT/ACTIVE/RETIRED, got: '{v}'")
        return v


class QuestionSpecification(GuidebookEntity):
    """Link between a question and a specification that answers it."""

    question_id: str
    spec_id: str
    answer_role: Optional[str] = None  # 'primary', 'partial', 'related'

    @field_validator("answer_role")
    @classmethod
    def valid_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ('primary', 'partial', 'related'):
            raise ValueError(f"answer_role must be primary/partial/related, got: '{v}'")
        return v
