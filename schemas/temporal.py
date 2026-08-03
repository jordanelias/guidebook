"""
schemas/temporal.py — Time-model entities per governance/time-model.md (A9).

Five temporal axes: document version, standards edition, project-rule
effective date, source publication/verification, launch phase. Plus the
SupersedenceLink primitive that crosses all five.

Cross-entity relationships:
- GuidebookVersion supersedes GuidebookVersion (chain)
- StandardEdition supersedes StandardEdition (chain)
- ProjectRule supersedes ProjectRule (chain)
- EvidenceSource may supersede EvidenceSource (rare)
- LaunchPhaseRecord is a singleton

Date format convention (Standing Rule 2): YYYY-MM-DD HH:MM via `date -u`.
"""

import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from schemas.base import GuidebookEntity
from schemas.enums import (
    GuidebookVersionStatus,
    LaunchPhase,
    ProjectRuleStatus,
    StandardStatus,
    SupersedenceLinkStatus,
    SupersedenceType,
)

# --- Format patterns ---

DATETIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
DATE_ONLY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PRE_SESSION_LITERAL = "pre-session"
PRE_SESSION_NORMALISED = "2026-03-15 00:00"

VERSION_TAG_PATTERN = re.compile(r"^v(\d+)\.(\d+)$")
VERSION_FILENAME_PATTERN = re.compile(
    r"^Guidebook_for_Accessible_Design_v\d+-\d+(_\d{4}-\d{2}-\d{2})?(-prep)?\.md$"
)

RULE_ID_PATTERN = re.compile(r"^RULE-[a-z0-9-]+-\d+$")
SUPERSEDENCE_ID_PATTERN = re.compile(r"^SUP-[a-z]+-\d{4}$")
SESSION_ID_PATTERN = re.compile(r"^session_\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$")


def _validate_datetime_str(value: str, *, allow_date_only: bool = False) -> str:
    """Shared validator: YYYY-MM-DD HH:MM, optionally YYYY-MM-DD."""
    if value == PRE_SESSION_LITERAL:
        return value
    if DATETIME_PATTERN.match(value):
        return value
    if allow_date_only and DATE_ONLY_PATTERN.match(value):
        return value
    raise ValueError(
        f"date must be YYYY-MM-DD HH:MM"
        f"{' or YYYY-MM-DD' if allow_date_only else ''}"
        f"{', or pre-session' if value == PRE_SESSION_LITERAL else ''}, "
        f"got: '{value}'"
    )


# --- Helper types ---

class VersionTag(BaseModel):
    """Parsed v{MAJOR}.{MINOR} version tag.

    Filesystem-friendly form replaces '.' with '-'.
    """

    model_config = ConfigDict(extra="forbid")

    major: int
    minor: int

    @field_validator("major", "minor")
    @classmethod
    def non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError(f"version component must be ≥0, got: {v}")
        return v

    @classmethod
    def from_string(cls, s: str) -> "VersionTag":
        """Parse 'v9.0' or '9.0' or '8.10' into a VersionTag."""
        s = s.strip()
        if not s.startswith("v"):
            s = "v" + s
        m = VERSION_TAG_PATTERN.match(s)
        if not m:
            raise ValueError(f"invalid version tag: '{s}' (expected vMAJOR.MINOR)")
        return cls(major=int(m.group(1)), minor=int(m.group(2)))

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}"

    def to_filename_component(self) -> str:
        """Filesystem-friendly form: v9.0 → v9-0."""
        return f"v{self.major}-{self.minor}"


class EffectiveDateRange(BaseModel):
    """Closed or open-ended date range.

    until_date=None means open-ended (still in effect).
    """

    model_config = ConfigDict(extra="forbid")

    from_date: str  # YYYY-MM-DD HH:MM or YYYY-MM-DD
    until_date: Optional[str] = None

    @field_validator("from_date")
    @classmethod
    def valid_from(cls, v: str) -> str:
        return _validate_datetime_str(v, allow_date_only=True)

    @field_validator("until_date")
    @classmethod
    def valid_until(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return _validate_datetime_str(v, allow_date_only=True)

    @model_validator(mode="after")
    def until_after_from(self) -> "EffectiveDateRange":
        if self.until_date is not None:
            # Lexical comparison works because YYYY-MM-DD format is sortable
            if self.until_date < self.from_date:
                raise ValueError(
                    f"until_date ({self.until_date}) must be ≥ "
                    f"from_date ({self.from_date})"
                )
        return self


# --- Entity types ---

class GuidebookVersion(GuidebookEntity):
    """A released or in-prep version of the guidebook itself."""

    version_tag: str  # canonical form: vMAJOR.MINOR
    effective_date: Optional[str] = None  # YYYY-MM-DD; null for prep
    file_path: str  # versions/{folder}/Guidebook_for_Accessible_Design_*.md
    status: GuidebookVersionStatus
    supersedes: Optional[str] = None  # prior version_tag
    notes: Optional[str] = None

    @field_validator("version_tag")
    @classmethod
    def valid_tag(cls, v: str) -> str:
        if not VERSION_TAG_PATTERN.match(v):
            raise ValueError(
                f"version_tag must match v{{MAJOR}}.{{MINOR}}, got: '{v}'"
            )
        return v

    @field_validator("effective_date")
    @classmethod
    def valid_effective(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not DATE_ONLY_PATTERN.match(v):
            raise ValueError(
                f"effective_date must be YYYY-MM-DD, got: '{v}'"
            )
        return v

    @model_validator(mode="after")
    def status_field_consistency(self) -> "GuidebookVersion":
        """ACTIVE/ARCHIVED require effective_date; IN_PREP may omit."""
        status_val = (
            self.status if isinstance(self.status, str) else self.status.value
        )
        if status_val in {"ACTIVE", "ARCHIVED"} and not self.effective_date:
            raise ValueError(
                f"GuidebookVersion with status={status_val} requires effective_date"
            )
        if self.supersedes and self.supersedes == self.version_tag:
            raise ValueError("version cannot supersede itself")
        return self


class StandardEdition(GuidebookEntity):
    """A specific edition of a standard family.

    Family: long-lived identifier (e.g., 'AS 1428.1', 'NEN 9120').
    Edition: dated release of that family (e.g., 'AS 1428.1:2021').
    """

    jurisdiction: str  # JurisdictionCode
    standard_family: str  # 'AS 1428.1'
    edition: str  # 'AS 1428.1:2021'
    publication_date: Optional[str] = None  # YYYY-MM-DD or YYYY-MM
    status: StandardStatus
    supersedes_edition: Optional[str] = None  # prior edition string
    transition_until_date: Optional[str] = None  # YYYY-MM-DD
    last_checked: Optional[str] = None  # YYYY-MM-DD HH:MM
    notes: Optional[str] = None

    @field_validator("publication_date")
    @classmethod
    def valid_pub_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        # Accept YYYY-MM-DD or YYYY-MM
        if DATE_ONLY_PATTERN.match(v):
            return v
        if re.match(r"^\d{4}-\d{2}$", v):
            return v
        raise ValueError(
            f"publication_date must be YYYY-MM-DD or YYYY-MM, got: '{v}'"
        )

    @field_validator("transition_until_date")
    @classmethod
    def valid_transition(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not DATE_ONLY_PATTERN.match(v):
            raise ValueError(
                f"transition_until_date must be YYYY-MM-DD, got: '{v}'"
            )
        return v

    @field_validator("last_checked")
    @classmethod
    def valid_checked(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return _validate_datetime_str(v)


class ProjectRule(GuidebookEntity):
    """A single RULE block extracted from project-standards.md."""

    rule_id: str  # RULE-{section_slug}-{seq}
    rule_text: str
    condition: Optional[str] = None
    action: Optional[str] = None
    effective_date: str  # original string from DATE: line
    effective_date_normalized: str  # YYYY-MM-DD HH:MM
    section: str  # H2/H3 heading
    supersedes: list[str] = []
    superseded_by: Optional[str] = None
    status: ProjectRuleStatus = ProjectRuleStatus.ACTIVE
    source_file: str = "references/project-standards.md"
    source_line: Optional[int] = None

    @field_validator("rule_id")
    @classmethod
    def valid_rule_id(cls, v: str) -> str:
        if not RULE_ID_PATTERN.match(v):
            raise ValueError(
                f"rule_id must match RULE-{{section-slug}}-{{seq}}, got: '{v}'"
            )
        return v

    @field_validator("effective_date")
    @classmethod
    def valid_effective(cls, v: str) -> str:
        return _validate_datetime_str(v, allow_date_only=True)

    @field_validator("effective_date_normalized")
    @classmethod
    def valid_normalised(cls, v: str) -> str:
        if not DATETIME_PATTERN.match(v):
            raise ValueError(
                f"effective_date_normalized must be YYYY-MM-DD HH:MM, got: '{v}'"
            )
        return v

    @model_validator(mode="after")
    def normalisation_consistency(self) -> "ProjectRule":
        """Pre-session normalises to anchor; canonical formats round-trip."""
        if self.effective_date == PRE_SESSION_LITERAL:
            if self.effective_date_normalized != PRE_SESSION_NORMALISED:
                raise ValueError(
                    f"pre-session must normalise to '{PRE_SESSION_NORMALISED}', "
                    f"got: '{self.effective_date_normalized}'"
                )
        elif DATETIME_PATTERN.match(self.effective_date):
            if self.effective_date_normalized != self.effective_date:
                raise ValueError(
                    f"effective_date_normalized must match effective_date when "
                    f"already in canonical form: '{self.effective_date}' vs "
                    f"'{self.effective_date_normalized}'"
                )
        elif DATE_ONLY_PATTERN.match(self.effective_date):
            expected = f"{self.effective_date} 00:00"
            if self.effective_date_normalized != expected:
                raise ValueError(
                    f"date-only effective_date '{self.effective_date}' must "
                    f"normalise to '{expected}', got "
                    f"'{self.effective_date_normalized}'"
                )

        # Self-supersedence check
        if self.rule_id in self.supersedes:
            raise ValueError(f"rule cannot supersede itself: {self.rule_id}")
        if self.superseded_by == self.rule_id:
            raise ValueError(f"rule cannot be superseded by itself: {self.rule_id}")
        return self


class SupersedenceLink(GuidebookEntity):
    """A directional supersedence relationship between two entities.

    Five link types: rule, standard, version, decision, source. The
    from_id and to_id resolve to records of the matching link_type.
    """

    link_id: str  # SUP-{type}-NNNN
    link_type: SupersedenceType
    from_id: str  # the thing being superseded
    to_id: str  # the thing that supersedes it
    effective_date: str  # YYYY-MM-DD HH:MM or YYYY-MM-DD
    transition_until_date: Optional[str] = None
    rationale: Optional[str] = None
    status: SupersedenceLinkStatus = SupersedenceLinkStatus.ACTIVE
    source: Optional[str] = None  # how detected (manual, registry, textual_cue)

    @field_validator("link_id")
    @classmethod
    def valid_link_id(cls, v: str) -> str:
        if not SUPERSEDENCE_ID_PATTERN.match(v):
            raise ValueError(
                f"link_id must match SUP-{{type}}-NNNN, got: '{v}'"
            )
        return v

    @field_validator("effective_date")
    @classmethod
    def valid_effective(cls, v: str) -> str:
        return _validate_datetime_str(v, allow_date_only=True)

    @field_validator("transition_until_date")
    @classmethod
    def valid_transition(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return _validate_datetime_str(v, allow_date_only=True)

    @model_validator(mode="after")
    def no_self_supersedence(self) -> "SupersedenceLink":
        if self.from_id == self.to_id:
            raise ValueError(
                f"SupersedenceLink cannot link entity to itself: {self.from_id}"
            )
        # link_id type prefix should match link_type
        link_type_val = (
            self.link_type if isinstance(self.link_type, str)
            else self.link_type.value
        )
        expected_prefix = f"SUP-{link_type_val}-"
        if not self.link_id.startswith(expected_prefix):
            raise ValueError(
                f"link_id prefix '{self.link_id}' does not match "
                f"link_type '{link_type_val}' (expected start: '{expected_prefix}')"
            )
        return self


class LaunchPhaseRecord(GuidebookEntity):
    """Singleton: the current launch phase of the project.

    Pre-launch is the current state per A5 RULE 2026-04-26.
    Transition to launched requires three triggers (see governance §5).
    """

    phase: LaunchPhase
    since: str  # YYYY-MM-DD HH:MM
    triggers_met: dict[str, bool] = {
        "launch_event": False,
        "resources_available": False,
        "co_designed_recruitment_spec": False,
    }
    history: list[dict] = []  # prior transitions

    @field_validator("since")
    @classmethod
    def valid_since(cls, v: str) -> str:
        return _validate_datetime_str(v)

    @model_validator(mode="after")
    def phase_trigger_consistency(self) -> "LaunchPhaseRecord":
        """Launched/maintained require all three triggers met."""
        phase_val = self.phase if isinstance(self.phase, str) else self.phase.value
        if phase_val in {"launched", "maintained"}:
            if not all(self.triggers_met.values()):
                raise ValueError(
                    f"phase={phase_val} requires all three triggers met, "
                    f"got: {self.triggers_met}"
                )
        return self


# --- Module-level constants ---

# Freshness windows per §4.3 of governance/time-model.md.
# (tier, evidence_type) → suggested_window_years (None = edition-driven).
FRESHNESS_WINDOWS: dict[tuple[int, str], Optional[int]] = {
    (1, "clinical"): 7,
    (1, "co1"): 5,
    (2, "standard_eb"): 5,
    (2, "co2"): 6,  # midpoint of 5–7
    (3, "sr_meta"): 5,
    (4, "standard_eb"): None,  # edition-driven
    (5, "national_fw"): None,
    (6, "code"): None,
}


def freshness_window_years(tier: int, evidence_type: str) -> Optional[int]:
    """Return suggested freshness window for a (tier, evidence_type) pair.

    None means edition-driven (re-verify at edition release, not on a clock).
    """
    return FRESHNESS_WINDOWS.get((tier, evidence_type))
