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

# The project's one ratified status vocabulary — owner ruling 2026-08-14,
# enforced in SQL by migration 058 and mirrored here. Kept as a literal set
# rather than an import of DecisionStatus so this module stays importable
# standalone, which validate_conflict.py relies on; the two are compared by
# test_db_integrity rather than by trust.
#
# RESOLVED-EVIDENCE and RESOLVED-CONSENSUS are reserved for direct evidence or
# claims directly derived from it. A conflict closed for any other reason —
# infrastructure finished, question withdrawn — is CLOSED.
RATIFIED_STATUSES = frozenset({
    "ACTIVE", "PROPOSED", "DEFERRED", "RESOLVED-EVIDENCE",
    "RESOLVED-CONSENSUS", "UNRESOLVED", "CLOSED", "RETIRED",
})


class ConflictParty(GuidebookEntity):
    """One side of a conflict — populations and their specification."""

    codes: list[str]  # PopulationCode values
    specification: str  # What this party needs, e.g. "≥30% LRV differential"


class ConflictResolution(GuidebookEntity):
    """Resolution details for a conflict domain."""

    status: str  # the ratified vocabulary — see RATIFIED_STATUSES
    strategy_codes: list[str] = []  # e.g. ["SZ", "PP"] — Sensory Zoning, Parallel Provision
    strategy_labels: list[str] = []  # human-readable strategy names
    description: str  # prose resolution description
    evidence_quality: Optional[str] = None  # ● / ◐ / ○

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        if v not in RATIFIED_STATUSES:
            raise ValueError(
                f"Invalid resolution status: '{v}'. Valid: {sorted(RATIFIED_STATUSES)}"
            )
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
    conflict is resolved (or declared unresolvable at Mode S).
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

    # Unresolvable residual (for UNRESOLVED conflicts — the Person-Mode handoff)
    unresolvable_residual: Optional[str] = None
    mode_s_trigger: Optional[str] = None
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
            if not re.match(r"^[A-K]-\d{2}[a-z]?$", code):
                raise ValueError(
                    f"specification must be item code [A-K]-NN[a-z]?, got: '{code}'"
                )
        return v

    @model_validator(mode="after")
    def unresolvable_consistency(self) -> "Conflict":
        """UNRESOLVED conflicts must name the Person-Mode handoff.

        The rule is unchanged; only the status it keys on is. It used to key on
        UNRESOLVABLE-MODE-S, a spelling deprecated on 2026-07-13 when "Mode S"
        became "Person Mode" (Item V of RATIFICATION-PACKAGE-2026-07-12, ratified
        in full per RATIFICATION-RECORD-2026-07-13 A5 — which named the
        conflicts.status CHECK as the one migration it needed, and that migration
        did not run until 058), and retired as a status word by the 2026-08-14
        ruling. A conflict that
        cannot be resolved at population scale still owes the reader what the
        assessment turns on, which is exactly what mode_s_trigger holds.
        """
        if self.resolution.status == "UNRESOLVED":
            if not self.mode_s_trigger:
                raise ValueError(
                    "UNRESOLVED conflict must specify mode_s_trigger "
                    "(the Person-Mode handoff parameter)"
                )
        return self
