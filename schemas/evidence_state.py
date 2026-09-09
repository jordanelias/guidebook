"""
schemas/evidence_state.py — Evidence state model for (parameter × lens) cells.

Per T-04 (Stage 0.5, DECIDED) and governance/evidence-methodology.md §2 (A6):
each cell in the guidebook's specification matrix holds one of four states
(stated, provisional, pending, not_applicable) with an associated
convergence assessment.

DIRECTNESS-AWARE (Stage 2.3, decision D-D; doctrine SHA 373255e). These models
back the `specifications` + `convergence_assessment` tables (migration 024,
closing R2) and carry the scale × directness conditioning of §1.4/§1.6/§1.7:
- the cell records its `design_scale` (universal/population/person), the axis from
  which each source's directness is computed (schemas/directness.scale_directness);
- the convergence assessment records the §1.7 directness conditioning via
  `down_weighted_sources` / `discounted_sources` (grain-mismatched sources that
  count less, or cannot anchor).

CELL IDENTITY — BOTH HALVES ARE RULED; NEITHER IS OPEN.

The SUBJECT is the canonical design parameter (owner 2026-08-26): `parameter_id`
into `base_parameters`, which points at the adjudicated term. It is NOT
`items.item_code` — the item layer was emptied 2026-09-01 and `items` is demoted
to a Part-4 render rollup derived FROM specifications, never keyed by them. Every
`[A-E]-NN` code still on the reading surface is prior-version content.

The LENS is the four browsing taxonomies (owner 2026-08-28, CHECK relaxed by
D-0182): identity / ICF / access-need / medical. `population_code` is retired in
favour of the four, and `populations` is ONLY the identity lens — keying a cell on
it alone is the traversal D-0184 measured and rejected. NULL in a lens means the
determination is not stated in that lens, which is legitimate; NULL in all four is
not, and `at_least_one_lens` below is that CHECK mechanised.

Migration 071 built both halves. This model mirrors the table it built.

Cross-entity relationships:
- One EvidenceStateRecord per (parameter_id × lens) cell
- References EvidenceSource records via the convergence source lists
- Cross-links to the gaps table (gap_id) for pending cells
"""

import re
from typing import Optional

from pydantic import ConfigDict, BaseModel, field_validator, model_validator

from schemas.directness import ALL_SCALES
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
    # Directness conditioning (§1.7): how grain-matching conditioned the source set
    # for this cell's design_scale. Anchoring set = (clinical ∪ co1 ∪ co2) − discounted.
    down_weighted_sources: list[str] = []  # REF-IDs DOWN-WEIGHTED (grain-mismatch; count less)
    discounted_sources: list[str] = []  # REF-IDs DISCOUNTED / NON-ANCHORING (cannot anchor)
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
    """T-04 evidence state for a single (parameter × lens) cell.

    Per governance/evidence-methodology.md §2 (A6):
    - stated: ≥1 anchoring source at Tier 1, Tier 2 (either stream), Co-1, or Co-2
      (T3-alone never suffices: T3-clinical-alone => provisional, T3-grey-alone =>
      pending — DR-2026-07-12-tier3-stated-threshold + unification-DR G7, ACCEPTED)
    - provisional: T3-clinical-alone (no anchoring corroboration), or Tier 4–6 only
      meeting the §2.3 richness threshold
    - pending: too sparse; gap-register link required
    - not_applicable: parameter irrelevant under that lens; rationale required

    Directness-aware (§1.4/§1.6/§1.7): the cell carries its `design_scale`, the
    axis from which each source's directness conditioning is computed.
    """

    model_config = ConfigDict(extra="forbid")

    # Cell identity — THE SUBJECT (owner 2026-08-26): the canonical design
    # parameter, pointed at, never copied (rule 5). base_parameters.parameter_id.
    parameter_id: int

    # Cell identity — THE FOUR LENSES (owner 2026-08-28; CHECK relaxed by D-0182
    # to "at least one"). Each is a code in its own base taxonomy; the codes are
    # NOT validated here, because a vocabulary belongs to the schema's CHECK and
    # its FK, never to a list in Python (CLAUDE.md §4).
    identity_code: Optional[str] = None   # populations.population_code
    icf_code: Optional[str] = None        # axes.axis_code
    needs_code: Optional[str] = None      # access_needs.need_code
    medical_code: Optional[str] = None    # base_taxonomy_medical.medical_code

    # Design scale (§1.4/§1.6) — universal | population | person
    design_scale: Optional[str] = None

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

    @field_validator("design_scale")
    @classmethod
    def valid_design_scale(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ALL_SCALES:
            raise ValueError(f"design_scale must be one of {sorted(ALL_SCALES)}, got: {v}")
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
    def at_least_one_lens(self) -> "EvidenceStateRecord":
        """D-0182, mechanised: absence in a lens is fine, absence in ALL is not.

        This is the Python side of the live table's
        `CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code)
        IS NOT NULL)`. It was "exactly one" under the 2026-08-28 ruling and D-0182
        relaxed it; stating a determination in several lenses at once is the ideal,
        not a violation.
        """
        if (
            self.identity_code is None
            and self.icf_code is None
            and self.needs_code is None
            and self.medical_code is None
        ):
            raise ValueError(
                "A determination must be stated in at least one lens: set one or "
                "more of identity_code / icf_code / needs_code / medical_code "
                "(D-0182). A cell in no lens is a cell about nobody."
            )
        return self

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
