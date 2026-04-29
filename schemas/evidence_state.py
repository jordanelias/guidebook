"""
schemas/evidence_state.py — Evidence state model for (parameter × population) cells.

Per T-04 (Stage 0.5, DECIDED) and governance/evidence-methodology.md §2 (A6):
each cell in the guidebook's specification matrix holds one of four states
(stated, provisional, pending, not_applicable) with an associated
convergence assessment.

Cross-entity relationships:
- Attaches to Specification records (one EvidenceStateRecord per spec)
- References EvidenceSource records via source lists
- Cross-links to gap_register.md for pending cells
"""

import re
from typing import Optional

from pydantic import ConfigDict, BaseModel, field_validator, model_validator

from schemas.enums import (
    ConvergenceStatus,
    EvidenceCellState,
    VerificationStatus,
)


class ProvisionalConfidenceFlag(BaseModel):
    """Structured confidence flag for provisional cells.

    Per governance/evidence-methodology.md §2.3: every provisional cell
    carries a flag naming the evidence dimensions present and absent.
    """

    model_config = ConfigDict(extra="forbid")

    dimensions_present: list[str]  # e.g. ["Tier 4–5 international standards"]
    dimensions_absent: list[str]  # e.g. ["No Tier 1–3 clinical", "No Co-1"]
    synthesis_basis: str  # e.g. "Value derived from ISO 21542 + BS 8300-2 convergence"


class ConvergenceAssessment(BaseModel):
    """Cross-tier convergence assessment for a (parameter × population) cell.

    Per governance/evidence-methodology.md §3.2 (A6 Q2 resolution):
    convergence is a property of the synthesis, assessed at the cell level.
    """

    model_config = ConfigDict(extra="forbid")

    status: ConvergenceStatus
    clinical_sources: list[str] = []  # REF-IDs of Tier 1–3 sources
    co1_sources: list[str] = []  # REF-IDs of Co-1 sources
    co2_sources: list[str] = []  # REF-IDs of Co-2 sources
    rationale: Optional[str] = None  # Required for divergent and single_axis
    synthesis_approach: Optional[str] = None  # Required for divergent

    @model_validator(mode="after")
    def check_rationale_requirements(self) -> "ConvergenceAssessment":
        """Enforce rationale requirements per convergence status."""
        status = self.status
        if isinstance(status, str):
            is_divergent = status == "divergent"
            is_single = status == "single_axis"
        else:
            is_divergent = status == ConvergenceStatus.DIVERGENT
            is_single = status == ConvergenceStatus.SINGLE_AXIS

        if is_divergent:
            if not self.rationale:
                raise ValueError(
                    "Divergent convergence assessment requires rationale"
                )
            if not self.synthesis_approach:
                raise ValueError(
                    "Divergent convergence assessment requires synthesis_approach"
                )
        if is_single and not self.rationale:
            raise ValueError(
                "Single-axis convergence assessment requires rationale "
                "(name the axis present)"
            )
        return self


class EvidenceStateRecord(BaseModel):
    """T-04 evidence state for a single (parameter × population) cell.

    Per governance/evidence-methodology.md §2 (A6):
    - stated: ≥1 source at Tier 1–3, Co-1, or Co-2
    - provisional: Tier 4–6 only, meets richness threshold
    - pending: too sparse; gap-register link required
    - not_applicable: parameter irrelevant for population; rationale required
    """

    model_config = ConfigDict(extra="forbid")

    # Cell identity
    spec_id: str  # Links to Specification.spec_id
    population: str  # PopulationCode value

    # State
    state: EvidenceCellState

    # Convergence (required for stated and provisional; None for pending/n_a)
    convergence: Optional[ConvergenceAssessment] = None

    # Provisional confidence flag (required when state == provisional)
    confidence_flag: Optional[ProvisionalConfidenceFlag] = None

    # Pending gap link (required when state == pending)
    gap_register_id: Optional[str] = None  # GAP-NNN format

    # Not-applicable rationale (required when state == not_applicable)
    not_applicable_rationale: Optional[str] = None

    # Source quality flags
    has_unverified_sources: bool = False  # Any UNVERIFIED-1 sources in basis
    all_sources_disqualified: bool = False  # All qualifying sources CLOSED

    # --- Validators ---

    @field_validator("spec_id")
    @classmethod
    def valid_spec_id(cls, v: str) -> str:
        if not re.match(r"^SPEC-\d{4}$", v):
            raise ValueError(f"spec_id must match SPEC-NNNN, got: {v}")
        return v

    @field_validator("gap_register_id")
    @classmethod
    def valid_gap_id(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^GAP-\d{3,4}$", v):
            raise ValueError(
                f"gap_register_id must match GAP-NNN or GAP-NNNN, got: {v}"
            )
        return v

    @model_validator(mode="after")
    def state_field_consistency(self) -> "EvidenceStateRecord":
        """Enforce state-dependent field requirements per A6 §2."""
        state = self.state
        if isinstance(state, str):
            state_val = state
        else:
            state_val = state.value

        if state_val == "pending":
            if not self.gap_register_id:
                raise ValueError(
                    "State 'pending' requires gap_register_id "
                    "(cross-link to gap_register.md)"
                )

        elif state_val == "provisional":
            if self.confidence_flag is None:
                raise ValueError(
                    "State 'provisional' requires confidence_flag "
                    "(name evidence dimensions present and absent)"
                )

        elif state_val == "not_applicable":
            if not self.not_applicable_rationale:
                raise ValueError(
                    "State 'not_applicable' requires not_applicable_rationale"
                )

        elif state_val == "stated":
            # stated cells should have convergence assessment
            # (pending_assessment is acceptable during migration)
            pass

        return self
