"""
schemas/enums.py — Shared enumerations for the guidebook data layer.

These enums encode doctrinal decisions from project-standards.md.
Changes here require a Change Order (CO) because they affect validation
across all entity types.

Population codes: workplan-orchestrator §Population Codes (canonical).
Evidence tiers: project-standards §Core Doctrine (seven-tier hierarchy).
Jurisdiction codes: jurisdiction-tracker §4.7.3 (24 canonical + meta-codes).
"""

from enum import Enum


class PopulationCode(str, Enum):
    """Canonical population codes per workplan-orchestrator.

    Top-level codes and sub-codes are both valid enum members.
    Sub-code implies parent: MOB_AMB implies MOB.
    VIS, DEAF, DBL are three distinct codes — VIS/DEAF compound is invalid.
    BAR is NOT main taxonomy (Supp. Part 4 only).
    IntD proxied through DEM + NDV per project-standards.
    """

    # Top-level
    MOB = "MOB"
    VIS = "VIS"
    DEAF = "DEAF"
    NEU = "NEU"
    DEM = "DEM"
    NDV = "NDV"
    NDV_MH = "NDV/MH"
    PAIN = "PAIN"
    DBL = "DBL"
    OFS = "OFS"
    IntD = "IntD"
    ALL = "ALL"

    # Sub-codes (MOB)
    MOB_AMB = "MOB/AMB"
    MOB_UPL = "MOB/UPL"

    # Sub-codes (NDV)
    NDV_AUT = "NDV/AUT"
    NDV_ADHD = "NDV/ADHD"
    NDV_SENS = "NDV/SENS"

    # Sub-codes (NEU)
    NEU_PCS = "NEU/PCS"

    # Sub-codes (OFS)
    OFS_ME = "OFS/ME"
    OFS_POTS = "OFS/POTS"
    OFS_MCAS = "OFS/MCAS"

    # Supplementary only (not main taxonomy)
    CHD = "CHD"
    LPA = "LPA"
    EXH = "EXH"
    BAR = "BAR"


class EvidenceTier(int, Enum):
    """Evidence tier per project-standards §Core Doctrine + T-03 resolution.

    Per T-03: tier (1–6) is one dimension; evidence_type (EvidenceType enum)
    is the other. Co-1 and Co-2 are evidence_types, not tiers.
    Co-1 sources carry tier=1 (co-primary). Co-2 sources carry tier=2 (parallel to Tier 2, per T-03).

    Tier 1 = OT intervention-tested clinical research (highest).
    Tier 2 = NGO/DPO/advocacy guidelines.
    Tier 3 = Systematic reviews and meta-analyses (Co-2 CPGs also here).
    Tier 4 = International standards with evidence basis.
    Tier 5 = National beyond-code frameworks.
    Tier 6 = Statutory codes (reference baseline only).
    """

    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3
    TIER_4 = 4
    TIER_5 = 5
    TIER_6 = 6


class ValueType(str, Enum):
    """Specification value types."""
    FIXED = "fixed"
    RANGE = "range"
    QUALITATIVE = "qualitative"  # presence-only, no numeric value


class RecommendationStrength(str, Enum):
    """Recommendation strength per evidence synthesis.

    UNSET: awaiting Opus synthesis.
    STRONG_UNIVERSAL: universal design / code compliance — fixed value.
    CONDITIONAL_POPULATION: population-informed — range with median default.
    CONDITIONAL: context-dependent without mode assignment.
    """
    UNSET = "UNSET"
    STRONG_UNIVERSAL = "STRONG_UNIVERSAL"
    CONDITIONAL_POPULATION = "CONDITIONAL_POPULATION"
    CONDITIONAL = "CONDITIONAL"


class ItemAssignmentStatus(str, Enum):
    """Item code assignment state.

    Replaces sentinel strings [UNASSIGNED] and [CROSS-CUTTING] in spec-db.
    """
    ASSIGNED = "ASSIGNED"
    UNASSIGNED = "UNASSIGNED"
    CROSS_CUTTING = "CROSS_CUTTING"


class JurisdictionCode(str, Enum):
    """Canonical jurisdiction codes.

    24 country codes per jurisdiction-tracker §4.7.3 plus meta-codes.
    Uses ISO 3166-1 alpha-2 where possible. UK used instead of GB
    per project convention. Full list confirmed at A3.
    """

    # Core 24 jurisdictions (alphabetical)
    AU = "AU"   # Australia
    BD = "BD"   # Bangladesh
    BR = "BR"   # Brazil
    CA = "CA"   # Canada
    CH = "CH"   # Switzerland
    CN = "CN"   # China
    DE = "DE"   # Germany
    DK = "DK"   # Denmark
    EG = "EG"   # Egypt
    FR = "FR"   # France
    ID = "ID"   # Indonesia
    IE = "IE"   # Ireland
    IN = "IN"   # India
    JP = "JP"   # Japan
    KE = "KE"   # Kenya
    KR = "KR"   # South Korea
    NG = "NG"   # Nigeria
    NL = "NL"   # Netherlands
    NO = "NO"   # Norway
    NZ = "NZ"   # New Zealand
    SE = "SE"   # Sweden
    SG = "SG"   # Singapore
    UK = "UK"   # United Kingdom (project convention, not GB)
    US = "US"   # United States
    ZA = "ZA"   # South Africa

    # Meta-codes (not individual countries)
    ISO = "ISO"   # ISO international standards
    EU = "EU"     # European Union directives


class EvidenceMarker(str, Enum):
    """Evidence specification markers per project-standards.

    ● (filled) = evidence-based specification (Tier 1–6).
    ○ (empty) = inferred from clinical reasoning or expert consensus.
    Every specification sentence carries either ● or ○. Unmarked = error.
    """
    EVIDENCE_BASED = "●"
    INFERRED = "○"


class EvidenceType(str, Enum):
    """Evidence type taxonomy per T-03 resolution.

    T-03 decided: tier (1–6) + evidence_type. Two orthogonal dimensions.
    tier encodes the clinical-evidence position (1 = strongest, 6 = baseline).
    evidence_type encodes the kind of evidence.

    Co-1 records: tier=1, evidence_type=CO1 (co-primary with clinical Tier 1).
    Co-2 records: tier=2, evidence_type=CO2 (OT body CPGs, rated Tier 3 with marker).
    """
    CLINICAL = "clinical"        # OT intervention-tested research
    CO1 = "co1"                  # Lived experience / participatory design
    CO2 = "co2"                  # OT professional body CPGs
    SR_META = "sr_meta"          # Systematic reviews / meta-analyses
    STANDARD_EB = "standard_eb"  # International standards with evidence basis
    NATIONAL_FW = "national_fw"  # National beyond-code frameworks
    CODE = "code"                # Statutory codes
    GREY = "grey"                # Grey literature, organizational reports
    UNKNOWN = "unknown"          # Not yet classified


class EvidenceCellState(str, Enum):
    """T-04 evidence-state machine for (parameter × population) cells.

    Per governance/evidence-methodology.md §2 (A6):
    - stated: sufficient evidence (≥Tier 3 OR Co-1 OR Co-2)
    - provisional: Tier 4–6 only, meets richness threshold
    - pending: too sparse to synthesize
    - not_applicable: parameter irrelevant for this population
    """
    STATED = "stated"
    PROVISIONAL = "provisional"
    PENDING = "pending"
    NOT_APPLICABLE = "not_applicable"


class ConvergenceStatus(str, Enum):
    """Cross-tier convergence assessment status.

    Per governance/evidence-methodology.md §3.2 (A6):
    Assessed at the (parameter × population) cell level.
    """
    CONVERGENT = "convergent"
    DIVERGENT = "divergent"
    SINGLE_AXIS = "single_axis"
    PENDING_ASSESSMENT = "pending_assessment"


class Co1Provenance(str, Enum):
    """Co-1 evidence provenance per A5 §3.1.

    Pre-launch: all Co-1 citations are published_corpus.
    participatory_synthesis is post-launch contingent.
    """
    PUBLISHED_CORPUS = "published_corpus"
    PARTICIPATORY_SYNTHESIS = "participatory_synthesis"


class Co1SourceType(str, Enum):
    """Co-1 source type taxonomy per A5 §1.1.

    The four types of Co-1 source plus validated_tool (A5 §6.1).
    """
    PEER_REVIEWED_LITERATURE = "peer_reviewed_literature"
    DPO_RESEARCH = "dpo_research"
    ADVOCACY_POSITION = "advocacy_position"
    ACADEMIC_NARRATIVE = "academic_narrative"
    VALIDATED_TOOL = "validated_tool"


class VerificationStatus(str, Enum):
    """Source verification status per 2026-04-23 verification report.

    Per A5 §6.3 + A6 §2.8:
    - VERIFIED / VERIFIED_WITH_CORRECTION: no state-machine effect
    - UNVERIFIED_1: flag, don't downgrade; triggers re-search
    - UNVERIFIED_CLOSED: sole qualifying source → cell downgrades to pending
    - CLOSED_DELETED: sole qualifying source → cell downgrades to pending
    """
    VERIFIED = "VERIFIED"
    VERIFIED_WITH_CORRECTION = "VERIFIED-WITH-CORRECTION"
    UNVERIFIED_1 = "UNVERIFIED-1"
    UNVERIFIED_CLOSED = "UNVERIFIED-CLOSED"
    CLOSED_DELETED = "CLOSED-DELETED"


class BestPracticeStatus(str, Enum):
    """T-04 state machine for BPC entries.

    PROVISIONAL: initial extraction, not all 24 jurisdictions recorded.
    COMPLETE: all 24 jurisdictions + co1_pass ≥ 9 languages.
    OPUS_SYNTHESIZED: Opus has reviewed and set recommendation_strength.
    CONSUMED: integrated into item specification.
    """
    PROVISIONAL = "PROVISIONAL"
    COMPLETE = "COMPLETE"
    OPUS_SYNTHESIZED = "OPUS_SYNTHESIZED"
    CONSUMED = "CONSUMED"


class DesignMode(int, Enum):
    """Design Modes per project-standards §Core Doctrine.

    Universal Mode = Universal Design / Code Compliance (population-agnostic, fixed).
    Mode P = Population-Informed Inclusive Design (ranges; median default).
    Mode S = Person-Specific Co-Design (OT assessment resolves range).
    DAR mandatory at all modes.
    """
    UNIVERSAL = 0
    POPULATION_BASED = 1
    PERSON_SPECIFIC = 2


class DesignStage(str, Enum):
    """Cross-cutting axis: project design stage.

    Specifications may have different applicability at different stages.
    Per workplan A3 T-06: design stage interacts orthogonally with parameters.
    """
    DD = "DD"             # Design Development
    RFO = "RFO"           # Ready for Occupancy
    RETROFIT = "retrofit"  # Existing building modification
    ALL = "all"            # Applies at all stages


class ProjectType(str, Enum):
    """Cross-cutting axis: project type.

    Constraints on achievable specification compliance vary by type.
    Per workplan A3 N-03: project type interacts orthogonally with parameters.
    """
    NEW_CONSTRUCTION = "new_construction"
    MAJOR_RENOVATION = "major_renovation"
    MINOR_ADAPTATION = "minor_adaptation"
    MAINTENANCE = "maintenance"
    ALL = "all"  # Applies to all project types


class StandardStatus(str, Enum):
    """Standard edition status per A8 §3.2 / A9 §2.

    CURRENT: this edition is the current legally-enforceable version
    UPDATED: a newer edition exists and may be partially in effect
    SUPERSEDED: a newer edition has fully replaced this one
    WITHDRAWN: standard withdrawn without replacement
    """
    CURRENT = "CURRENT"
    UPDATED = "UPDATED"
    SUPERSEDED = "SUPERSEDED"
    WITHDRAWN = "WITHDRAWN"


class SupersedenceType(str, Enum):
    """Categories of supersedence relationship per governance/time-model.md §4.

    rule: project-standards RULE block superseded by a later RULE
    standard: standards edition superseded by a later edition (same family)
    version: guidebook version superseded by a later release
    decision: governance decision (e.g. T-04 lock) supersedes prior draft
    source: a newer publication supersedes an older one (rare, optional)
    """
    RULE = "rule"
    STANDARD = "standard"
    VERSION = "version"
    DECISION = "decision"
    SOURCE = "source"


class SupersedenceLinkStatus(str, Enum):
    """SupersedenceLink record status.

    ACTIVE: link is authoritative
    PROVISIONAL: link detected by textual cue, awaits human review
    RETIRED: link superseded by a newer link or invalidated
    """
    ACTIVE = "ACTIVE"
    PROVISIONAL = "PROVISIONAL"
    RETIRED = "RETIRED"


class GuidebookVersionStatus(str, Enum):
    """Lifecycle status of a guidebook version.

    IN_PREP: in preparation, not effective
    ACTIVE: the current effective version (exactly one record at a time)
    ARCHIVED: prior version, no longer effective
    """
    IN_PREP = "IN_PREP"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class ProjectRuleStatus(str, Enum):
    """Lifecycle status of a project-standards RULE.

    ACTIVE: rule is in force
    SUPERSEDED: replaced by a later rule (named successor)
    RETIRED: removed without a named successor
    """
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    RETIRED = "RETIRED"


class LaunchPhase(str, Enum):
    """Project launch phase per governance/time-model.md §5.

    pre_launch: solo authorship, published-corpus Co-1 only (current)
    launched: initial public release, post-launch posture begins
    maintained: ongoing edition cycle, participatory synthesis may engage
    """
    PRE_LAUNCH = "pre_launch"
    LAUNCHED = "launched"
    MAINTAINED = "maintained"


class MisuseVectorSeverity(str, Enum):
    """Severity of harm magnitude per A10 §1.

    LOW: harm is real but contained / single-instance
    MEDIUM: harm scales but mitigations exist within project methodology
    HIGH: harm scales and primary mitigations are external to project (require
          legal/regulatory framework or post-launch enforcement)
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class MisuseReviewStatus(str, Enum):
    """Status of a release-gate review per A10 §4.4.

    CLEARED: vector reviewed, no new exposure, mitigations operative
    CLEARED_WITH_NOTES: vector reviewed; non-blocking observations recorded
    ESCALATE: vector reviewed; concern requires attention before/at release
              (release proceeds only via ReleaseOverride)
    """
    CLEARED = "CLEARED"
    CLEARED_WITH_NOTES = "CLEARED_WITH_NOTES"
    ESCALATE = "ESCALATE"


class MisuseVectorStatus(str, Enum):
    """Lifecycle status of a catalogue vector.

    ACTIVE: vector is currently catalogued and reviewed at each release
    RETIRED: vector is no longer applicable (e.g., obsolete due to methodology
             change, or merged into another vector); retained in catalogue for
             historical record but not reviewed at release
    """
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"


class DecisionCategory(str, Enum):
    """Decision category per governance/decision-protocol.md §1.

    D-DOCT: doctrinal (mission, CRPD posture, taxonomy, evidence-tier hierarchy)
    D-METH: methodological (evidence-state machine, convergence rules, freshness windows)
    D-SCHEMA: schema/data-structure (Pydantic entities, enum values, format patterns)
    D-OP: operational (branch protection, commit conventions, CI matrix, PAT scope)
    D-PRES: presentation (voice patterns, section ordering, plain-language register)
    """
    D_DOCT = "D-DOCT"
    D_METH = "D-METH"
    D_SCHEMA = "D-SCHEMA"
    D_OP = "D-OP"
    D_PRES = "D-PRES"


class DelegationCategory(str, Enum):
    """Delegation category per governance/decision-protocol.md §2.

    DG-NON: non-delegable; project owner alone decides
    DG-REVIEW: agent decides; project owner reviews before canonical
    DG-AUTO: agent decides; no review gate; logged
    """
    DG_NON = "DG-NON"
    DG_REVIEW = "DG-REVIEW"
    DG_AUTO = "DG-AUTO"


class DecisionStatus(str, Enum):
    """Lifecycle status of a Decision record.

    ACTIVE: decision in force
    SUPERSEDED: replaced by a later decision (named successor)
    RETIRED: removed without a named successor
    """
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    RETIRED = "RETIRED"


class DecisionReviewStatus(str, Enum):
    """Review status of a Decision record.

    PENDING: DG-REVIEW awaiting review
    CONFIRMED: DG-REVIEW reviewed and confirmed
    NA: not applicable (DG-NON or DG-AUTO)
    """
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    NA = "NA"


class RecheckTrigger(str, Enum):
    """Recheck trigger per governance/doctrine-recheck.md §1.

    PERIODIC: every 25 working sessions
    STAGE_TRANSITION: A->B, B->C
    RULE_REVISION: targeted recheck on doctrinal-rule revision
    """
    PERIODIC = "PERIODIC"
    STAGE_TRANSITION = "STAGE_TRANSITION"
    RULE_REVISION = "RULE_REVISION"


class RecheckFindingSeverity(str, Enum):
    """Severity of a RecheckFinding."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class RecheckFindingStatus(str, Enum):
    """Lifecycle status of a RecheckFinding."""
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    DEFERRED = "DEFERRED"


class ContaminationDisposition(str, Enum):
    """Four-state classification per Amendment 3 / Stage 0.4 contamination sample.

    CLEAN: doctrinally aligned with Core Doctrine and A6/A7 methodology
    AMBIGUOUS: Tier-5-only or self-flagged PROVISIONAL; needs confidence-flag review
    STUB: synthesis pending Opus pass; placeholder content
    MERGED: CO-0006 redirect file; substantive BPC is at redirect target
    """
    CLEAN = "CLEAN"
    AMBIGUOUS = "AMBIGUOUS"
    STUB = "STUB"
    MERGED = "MERGED"


class DiagramType(str, Enum):
    """Specification diagram type per D-0139 Amendment 1."""
    PLAN = "plan"
    SECTION = "section"
    ELEVATION = "elevation"
    ISOMETRIC = "isometric"
    CHART = "chart"


class RetrofitCategory(str, Enum):
    """Retrofit cost/difficulty category per D-0139 Amendment 1.

    LOW_PLANNING: zero cost at design stage; retrofit requires spatial reorganisation.
    LOW_FIXTURE: fixture replacement only; no structural work.
    MODERATE: minor works (e.g., door widening, ramp addition).
    HIGH: significant structural works (e.g., lift shaft, wet room).
    STRUCTURAL: load-bearing or foundation changes.
    """
    LOW_PLANNING = "LOW-PLANNING"
    LOW_FIXTURE = "LOW-FIXTURE"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    STRUCTURAL = "STRUCTURAL"


class CurationStatus(str, Enum):
    """Specification curation lifecycle per D-0139 Amendment 1."""
    AUTOMATED = "automated"
    REVIEWED = "reviewed"
    OPUS_SYNTHESIZED = "opus_synthesized"


class PopulationRole(str, Enum):
    """Population relationship role in specification_population join.

    PRIMARY: population is the primary design driver for this spec.
    SECONDARY: population benefits but is not the primary driver.
    ALL: universal applicability (legacy migration default).
    """
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ALL = "all"
