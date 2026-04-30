"""
schemas/adversarial_use.py — Misuse vector catalogue + release-review records.

Per governance/adversarial-use-framework.md (A10):
- MisuseVector: a single catalogue entry (named misuse pattern)
- MisuseVectorCatalog: the top-level catalogue (singleton: data/adversarial_use/catalog.yaml)
- MisuseReview: a single (version × vector) review record
- ReleaseOverride: explicit author override of an unresolved ESCALATE review

Vector IDs follow the V-NN convention (V-01, V-02, ...).
Catalogue versioning is integer (1, 2, ...) tracked in MisuseVectorCatalog.version.
"""

import re
from typing import Optional

from pydantic import field_validator, model_validator

from schemas.base import GuidebookEntity
from schemas.enums import (
    MisuseReviewStatus,
    MisuseVectorSeverity,
    MisuseVectorStatus,
)
from schemas.temporal import DATETIME_PATTERN, DATE_ONLY_PATTERN

# --- Format patterns ---

VECTOR_ID_PATTERN = re.compile(r"^V-\d{2,3}$")
VERSION_TAG_PATTERN = re.compile(r"^v\d+\.\d+$")


# --- Entity types ---

class MisuseVector(GuidebookEntity):
    """A single named misuse pattern in the catalogue.

    Each vector declares its mechanism, harm, and the primary mitigations
    that exist in the project's methodology to address it.
    """

    vector_id: str  # V-NN (zero-padded to 2-3 digits)
    name: str  # short human label
    mechanism: str  # how the misuse works (1-3 sentences)
    harm: str  # what harm follows (1-2 sentences)
    severity: MisuseVectorSeverity
    primary_mitigations: list[str]  # references to project methodology
    doctrinal_basis: list[str]  # references that authorise this vector being catalogued
    status: MisuseVectorStatus = MisuseVectorStatus.ACTIVE
    introduced_date: str  # YYYY-MM-DD HH:MM
    retired_date: Optional[str] = None  # populated only when status=RETIRED
    retirement_rationale: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("vector_id")
    @classmethod
    def valid_vector_id(cls, v: str) -> str:
        if not VECTOR_ID_PATTERN.match(v):
            raise ValueError(f"vector_id must match V-NN, got: '{v}'")
        return v

    @field_validator("introduced_date")
    @classmethod
    def valid_intro(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"introduced_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @field_validator("retired_date")
    @classmethod
    def valid_retired(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"retired_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @field_validator("primary_mitigations")
    @classmethod
    def at_least_one_mitigation(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError(
                "MisuseVector must declare at least one primary mitigation. "
                "If no mitigation exists, the vector should be flagged "
                "ESCALATE in its first release-gate review, not catalogued "
                "with empty mitigations."
            )
        return v

    @model_validator(mode="after")
    def retired_consistency(self) -> "MisuseVector":
        """RETIRED vectors must have retired_date and rationale."""
        status_val = (
            self.status if isinstance(self.status, str) else self.status.value
        )
        if status_val == "RETIRED":
            if not self.retired_date:
                raise ValueError("RETIRED vector must have retired_date")
            if not self.retirement_rationale:
                raise ValueError(
                    "RETIRED vector must have retirement_rationale"
                )
        elif status_val == "ACTIVE":
            if self.retired_date or self.retirement_rationale:
                raise ValueError(
                    "ACTIVE vector must not have retired_date or rationale"
                )
        return self


class MisuseVectorCatalog(GuidebookEntity):
    """The top-level catalogue (one per repository).

    Stored at data/adversarial_use/catalog.yaml.
    """

    catalog_version: int  # increments on each material change
    last_updated: str  # YYYY-MM-DD HH:MM
    vectors: list[MisuseVector]

    @field_validator("catalog_version")
    @classmethod
    def positive_version(cls, v: int) -> int:
        if v < 1:
            raise ValueError(f"catalog_version must be ≥1, got: {v}")
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
    def unique_vector_ids(self) -> "MisuseVectorCatalog":
        """Vector IDs must be unique within the catalogue."""
        seen: set[str] = set()
        for v in self.vectors:
            if v.vector_id in seen:
                raise ValueError(
                    f"duplicate vector_id in catalogue: {v.vector_id}"
                )
            seen.add(v.vector_id)
        return self


class MisuseReview(GuidebookEntity):
    """One review record per (guidebook_version × vector) pair.

    A version's complete review_log is a collection of these records,
    typically stored together in data/adversarial_use/review_log/{version_tag}.yaml
    as a list under the key 'reviews'.
    """

    version_tag: str  # vMAJOR.MINOR (links to A9 GuidebookVersion)
    vector_id: str  # V-NN (links to MisuseVector)
    reviewer: str  # 'solo_author_pre_launch' or named reviewer
    date: str  # YYYY-MM-DD HH:MM
    status: MisuseReviewStatus
    notes: Optional[str] = None
    new_exposure_introduced: bool = False
    mitigations_operative: bool = True
    new_mitigations_added: list[str] = []
    weakened_mitigations: list[str] = []
    retroactive: bool = False

    @field_validator("version_tag")
    @classmethod
    def valid_version_tag(cls, v: str) -> str:
        if not VERSION_TAG_PATTERN.match(v):
            raise ValueError(
                f"version_tag must match vMAJOR.MINOR, got: '{v}'"
            )
        return v

    @field_validator("vector_id")
    @classmethod
    def valid_vector_id(cls, v: str) -> str:
        if not VECTOR_ID_PATTERN.match(v):
            raise ValueError(f"vector_id must match V-NN, got: '{v}'")
        return v

    @field_validator("date")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(f"date must be YYYY-MM-DD HH:MM, got: '{v}'")
        return v

    @model_validator(mode="after")
    def status_field_consistency(self) -> "MisuseReview":
        """CLEARED_WITH_NOTES and ESCALATE require notes."""
        status_val = (
            self.status if isinstance(self.status, str) else self.status.value
        )
        if status_val in {"CLEARED_WITH_NOTES", "ESCALATE"} and not self.notes:
            raise ValueError(
                f"MisuseReview with status={status_val} requires notes"
            )
        # If new_exposure introduced or a mitigation weakened, status must be
        # at least CLEARED_WITH_NOTES (not bare CLEARED).
        if (self.new_exposure_introduced or self.weakened_mitigations) and (
            status_val == "CLEARED"
        ):
            raise ValueError(
                "MisuseReview cannot be bare CLEARED when "
                "new_exposure_introduced or weakened_mitigations is set; "
                "use CLEARED_WITH_NOTES or ESCALATE"
            )
        return self


class VersionReviewLog(GuidebookEntity):
    """Container for all reviews on a single guidebook version.

    One file per version: data/adversarial_use/review_log/{version_tag}.yaml.
    """

    version_tag: str
    review_completed_date: str  # YYYY-MM-DD HH:MM (when all reviews on version finished)
    catalog_version_at_review: int  # which catalog version was used
    reviews: list[MisuseReview]

    @field_validator("version_tag")
    @classmethod
    def valid_version_tag(cls, v: str) -> str:
        if not VERSION_TAG_PATTERN.match(v):
            raise ValueError(
                f"version_tag must match vMAJOR.MINOR, got: '{v}'"
            )
        return v

    @field_validator("review_completed_date")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"review_completed_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @model_validator(mode="after")
    def reviews_match_version(self) -> "VersionReviewLog":
        """Every review record's version_tag must match the log's version_tag."""
        for r in self.reviews:
            if r.version_tag != self.version_tag:
                raise ValueError(
                    f"review version_tag '{r.version_tag}' does not match "
                    f"log version_tag '{self.version_tag}'"
                )
        return self


class ReleaseOverride(GuidebookEntity):
    """Explicit override of an ESCALATE review status to permit release.

    Required when a release proceeds despite an ESCALATE review.
    Surfaces in release notes; tracked separately for accountability.
    """

    version_tag: str
    vector_id: str
    escalation_rationale: str  # the original ESCALATE notes
    override_rationale: str  # why release is proceeding
    override_by: str  # reviewer name
    override_date: str  # YYYY-MM-DD HH:MM
    mitigation_plan: Optional[str] = None  # planned remediation, if any

    @field_validator("version_tag")
    @classmethod
    def valid_version_tag(cls, v: str) -> str:
        if not VERSION_TAG_PATTERN.match(v):
            raise ValueError(
                f"version_tag must match vMAJOR.MINOR, got: '{v}'"
            )
        return v

    @field_validator("vector_id")
    @classmethod
    def valid_vector_id(cls, v: str) -> str:
        if not VECTOR_ID_PATTERN.match(v):
            raise ValueError(f"vector_id must match V-NN, got: '{v}'")
        return v

    @field_validator("override_date")
    @classmethod
    def valid_date(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"override_date must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v
