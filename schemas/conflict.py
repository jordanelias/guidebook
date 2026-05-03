"""
schemas/conflict.py — Conflict entity model.

Represents a conflict domain where two or more populations have
divergent design requirements for the same physical parameter.
Per schema-spec §3.3 and A6 evidence-methodology.md §4.

Conflict resolution follows the harm-asymmetry principle:
where populations have opposing needs on the same parameter,
the default protects the higher-harm population, with supplementary
provision for others. Values-based conflicts (no disproportionate
harm) use the broadest-benefit assessment.
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import GuidebookEntity


class ConflictParty(GuidebookEntity):
    """One side of a conflict — populations and their specification."""

    codes: list[str]  # PopulationCode values
    specification: str  # What this party needs, e.g. "≥30% LRV differential"


class ConflictResolution(GuidebookEntity):
    """Resolution details for a conflict domain."""

    status: str  # RESOLVED-EVIDENCE, RESOLVED-CONSENSUS, UNRESOLVABLE-TIER-2, DEFERRED
    strategy_codes: list[str] = []  # e.g. ["SZ", "PP"] — Sensory Zoning, Parallel Provision
    strategy_labels: list[str] = []  # human-readable strategy names
    description: str  # prose resolution description
    evidence_quality: Optional[str] = None  # ● / ◐ / ○

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        valid = {
            "RESOLVED-EVIDENCE", "RESOLVED-CONSENSUS",
            "UNRESOLVABLE-TIER-2", "DEFERRED", "OPEN",
        }
        if v not in valid:
            raise ValueError(f"Invalid resolution status: '{v}'. Valid: {sorted(valid)}")
        return v


class DecisionTreeNode(GuidebookEntity):
    """A node in the conflict resolution decision tree."""

    question: Optional[str] = None  # Decision question
    yes: Optional[str] = None  # Answer if yes (leaf) or None (branch)
    no: Optional[str] = None  # Answer if no (leaf) or None (branch)
    yes_node: Optional["DecisionTreeNode"] = None  # Sub-tree if yes is a branch
    no_node: Optional["DecisionTreeNode"] = None  # Sub-tree if no is a branch


class ConflictCitation(GuidebookEntity):
    """A citation supporting a conflict analysis."""

    ref: str  # Short reference
    finding: Optional[str] = None  # Key finding from this source


class Conflict(GuidebookEntity):
    """A conflict domain in the guidebook data layer.

    Each record captures where two or more populations have opposing
    design requirements on the same physical parameter, and how the
    conflict is resolved (or declared unresolvable at Tier 2).
    """

    # Identity
    conflict_id: str  # e.g. "COLOUR-CONT", "ACOUSTIC-LVL"
    conflict_label: str  # Human-readable label
    domain: str  # Conflict domain name

    # Parties
    population_a: ConflictParty
    population_b: ConflictParty

    # Resolution
    resolution: ConflictResolution

    # Governing principle
    governing_principle: Optional[str] = None  # e.g. "Safety-critical provisions take priority"

    # Decision tree (for website rendering)
    decision_tree: Optional[DecisionTreeNode] = None

    # Specifications involved
    specifications_involved: list[str] = []  # item codes
    connection_ids: list[str] = []  # CON-NNNN references

    # Unresolvable residual (for UNRESOLVABLE-TIER-2 conflicts)
    unresolvable_residual: Optional[str] = None
    tier_2_trigger: Optional[str] = None
    mitigation: Optional[str] = None
    ot_assessment_mandatory: bool = False

    # Citations
    citations: list[ConflictCitation] = []

    # Metadata
    notes: Optional[str] = None

    # --- Validators ---

    @field_validator("conflict_id")
    @classmethod
    def valid_conflict_id(cls, v: str) -> str:
        """Conflict ID must be uppercase hyphenated."""
        if not re.match(r"^[A-Z][-A-Z0-9]+$", v):
            raise ValueError(
                f"conflict_id must be uppercase hyphenated, got: '{v}'"
            )
        return v

    @field_validator("specifications_involved")
    @classmethod
    def valid_spec_refs(cls, v: list[str]) -> list[str]:
        """Specifications must be valid item codes."""
        for code in v:
            if not re.match(r"^[A-K]-\d{2}$", code):
                raise ValueError(
                    f"specification must be item code [A-K]-NN, got: '{code}'"
                )
        return v

    @model_validator(mode="after")
    def unresolvable_consistency(self) -> "Conflict":
        """UNRESOLVABLE-TIER-2 conflicts must have tier_2_trigger."""
        if self.resolution.status == "UNRESOLVABLE-TIER-2":
            if not self.tier_2_trigger:
                raise ValueError(
                    "UNRESOLVABLE-TIER-2 conflict must specify tier_2_trigger"
                )
        return self
