"""
schemas/enums.py — Shared enumerations for the guidebook data layer.

These enums encode doctrinal decisions from project-standards.md.
Changes here require a Change Order (CO) because they affect validation
across all entity types.

Population codes: workplan-orchestrator §Population Codes (canonical).
Evidence tiers: `governance/tier-system.md` §1.
Jurisdiction codes: jurisdiction-tracker §4.7.3 (24 canonical + meta-codes).
"""

from enum import Enum


class LifeStageModifier(str, Enum):
    """Orthogonal life-stage modifiers (DR-2026-07-23).

    Not populations: a child or an older adult can hold any access profile.
    """
    SEN = "SEN"   # older adults
    CHD = "CHD"   # disabled children


class EvidenceTier(int, Enum):
    """Evidence tier per project-standards §Core Doctrine + T-03 resolution.

    Per T-03: tier (1–6) is one dimension; evidence_type (EvidenceType enum)
    is the other. Co-1 and Co-2 are evidence_types, not tiers.
    Co-1 sources carry tier=1 (co-primary). Co-2 sources carry tier=2 (parallel to Tier 2, per T-03).

    Ladder per governance/tier-system.md (OPERATIVE 2026-05-25; T2/T3 reordering
    from the pre-2026-05-25 draft — sr_meta sits at T2, not T3):
    Tier 1 = Primary research with intervention-level or biomechanical control.
    Tier 2 = Systematic reviews / meta-analyses (sr_meta), or named-organisation
      evidence-based standards (standard_eb) -- community-consensus synthesis
      above primary studies but below international standards.
    Tier 3 = Lower-control primary clinical research (cross-sectional,
      observational, qualitative, single-centre) plus grey-literature primary
      research; "rarely the sole basis" (tier-system.md §1).
    Tier 4 = International standards with evidence basis (ISO, IEC, CEN, etc.).
    Tier 5 = National beyond-code frameworks.
    Tier 6 = Statutory codes (reference baseline only; convergence-not-evidence).
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

    The original 24 per jurisdiction-tracker §4.7.3, plus meta-codes, plus those
    admitted 2026-09-18 and 2026-10-01 (below). ISO 3166-1 alpha-2 where possible.
    Count the members rather than trusting a number typed anywhere (CLAUDE.md rule 7a):

        python3 -c "import sys; sys.path.insert(0,'.'); from schemas.enums import JurisdictionCode as J; print(len(list(J)))"

    WRITERS REFUSE WHAT THIS DOES NOT DECLARE (2026-10-01). `dbcore.check_jurisdiction`
    reads this enum and is called by every `db.py` writer of a table the audit below
    gates, so an undeclared code is refused at write time rather than found after it
    lands. Before that the writers checked nothing, and `PT` reached a research
    batch's rows before any gate saw it.

    UK, NOT GB. `governance/jurisdiction-philosophy.md` rules GB rejected at
    ERROR level, and as of 2026-09-18 that is enforced on the DATABASE by
    `scripts/audit/jurisdiction_db_vocabulary.py` -- previously only on files,
    which is how 27 GB rows across five tables went unnoticed.

    DO NOT ADD A CODE BECAUSE IT APPEARS IN A TABLE. Derive what is live before
    proposing one, and note WHICH tables carry it:

        select jurisdiction, count(*) from evidence_sources group by 1;

    The 2026-09-18 five were admitted because they appear in the CORPUS tables --
    evidence_sources, source_value_extractions, search_executions,
    research_code_leads. Roughly twenty further ISO codes are live in
    `lang_jur_map`, which is a language-to-jurisdiction reference map of places
    the project MAY expand into, not evidence it holds; those are the "Phase 3
    expansion" `validate_jurisdiction.py` warns about and they are deliberately
    NOT admitted here. Admitting a code silently converts a candidate
    jurisdiction into a declared one.
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

    # Admitted 2026-09-18 (owner ruling). Each was already live in the corpus
    # tables while absent from this enum, so the declared vocabulary could not be
    # used to gate the column it describes.
    BE = "BE"   # Belgium -- REF-00995 (Flemish decree), REF-00996 (Handboek Toegankelijkheid)
    ES = "ES"   # Spain -- search_executions (CTE DB-SUA line of enquiry)
    HR = "HR"   # Croatia -- REF-01001 (Lepoglavec 2023)
    IT = "IT"   # Italy -- search_executions

    # Admitted 2026-10-01, executing the owner ruling of 2026-09-28 ("jurisdiction
    # scope: buckets 1-2 exhausted before reaching further", references/
    # project-standards.md). PT and FI are named Bucket-2 members and UN a Bucket-1
    # member of that ruling, which calls UN's absence from this enum "a tooling gap
    # (rule 10: fix in its own PR)". Where each is live:
    #     select jurisdiction, count(*) from <table> where jurisdiction in
    #         ('PT','FI','UN','UG') group by 1;
    PT = "PT"   # Portugal -- Bucket 2
    FI = "FI"   # Finland -- Bucket 2
    UN = "UN"   # United Nations -- Bucket 1. A meta-code like ISO and EU, not a country.
    # UG is NOT in either bucket and is admitted by owner decision D2, approved 2026-10-01
    # (references/project-standards.md, grep "plan's decisions D1–D4 approved"): declared
    # for PR #165's rows, which are not unwound; outside research scope by the 2026-09-28
    # ruling. This enum is the declared vocabulary of rows held, not the canonical list --
    # so declaring UG licenses no further Ugandan research; the ruling, not this list,
    # sets research scope.
    UG = "UG"   # Uganda

    # Meta-codes (not individual countries)
    ISO = "ISO"   # ISO international standards
    EU = "EU"     # European Union directives
    INT = "INT"   # International / no single jurisdiction. DISTINCT FROM ISO: ISO
    #               means an ISO-published standard, INT means the work spans
    #               jurisdictions without being one -- REF-00994 (IPC Accessibility
    #               Guide) and REF-00977 (a review searched across three databases).


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
    Co-2 records: tier=2, evidence_type=CO2 (OT body CPGs, parallel to Tier 2 —
    not Tier 3; see governance/tier-system.md's Co-2 row).
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

    Per governance/evidence-methodology.md §2 (A6, amended by the
    tier3-stated-threshold DR, ACCEPTED 2026-07-13):
    - stated: ≥1 anchoring source at Tier 1, Tier 2, Co-1, or Co-2 (Tier 3
      alone never suffices)
    - provisional: T3-clinical-alone, or Tier 4–6 only meeting the richness
      threshold
    - pending: too sparse to synthesize (includes T3-grey-alone)
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
    """Co-1 evidence provenance (co1-operational §3.1).

    D-0178: the Co-1 warrant is the named co-production, which neither value
    states.
    """
    PUBLISHED_CORPUS = "published_corpus"
    PARTICIPATORY_SYNTHESIS = "participatory_synthesis"


class Co1SourceType(str, Enum):
    """Co-1 source type taxonomy per A5 §1.1.

    The live column's values differ from these; RULINGS R11 corrects the enum
    from the column in plan step 3.
    """
    PEER_REVIEWED_LITERATURE = "peer_reviewed_literature"
    DPO_RESEARCH = "dpo_research"
    ADVOCACY_POSITION = "advocacy_position"
    ACADEMIC_NARRATIVE = "academic_narrative"
    VALIDATED_TOOL = "validated_tool"


class VerificationStatus(str, Enum):
    """Whether a source is established. BINARY, per D-0157 (ADOPTED 2026-08-04).

    VERIFIED means the source document itself was obtained and the metadata
    recorded was read from it -- not from a citing bibliography, a search-result
    summary, or a publisher's landing page. For a Co-1 source the artefact is
    the attestation (DR section 3.1); same standard, different artefact, which
    co-primacy with T1 under CRPD Art. 4.3 requires.

    The retired values -- VERIFIED-1, VERIFIED-2, VERIFIED-WITH-CORRECTION,
    UNVERIFIED-1, UNVERIFIED-CLOSED, CLOSED-DELETED, DISPUTED, SUPERSEDED --
    were each one of three orthogonal facts smuggled into the status string.
    They now live in VerificationDisposition (is more effort owed),
    verification_attempt_count (how much was spent), VerificationMethod (how it
    was established) and VerificationClosureReason (why it stopped).
    """
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"


class VerificationDisposition(str, Enum):
    """Is more effort owed on this source? D-0157."""
    OPEN = "OPEN"      # a return pass is owed
    CLOSED = "CLOSED"  # settled -- and for UNVERIFIED, earned against >=2 attempts


class VerificationMethod(str, Enum):
    """How the standing was established. D-0157 section 4.3."""
    DIRECT_RENDER = "direct-render"
    CO1_ATTESTATION = "co1-attestation"
    CORROBORATED_NOT_RETRIEVED = "corroborated-not-retrieved"
    CITING_BIBLIOGRAPHY = "citing-bibliography"
    TOOL = "tool"


class VerificationClosureReason(str, Enum):
    """Why an unverified source stopped being pursued. D-0157 section 4.2."""
    PAYWALLED = "paywalled"
    PRINT_ONLY = "print-only"
    ACCESS_DENIED_PERSISTENT = "access-denied-persistent"
    WITHDRAWN = "withdrawn"
    NOT_FOUND_AFTER_SEARCH = "not-found-after-search"
    DISPUTED_EXISTENCE = "disputed-existence"  # owner ruling: there may be no resolution


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
    Population Mode = Population-Informed Inclusive Design (ranges; median default).
    Person Mode = Person-Specific Co-Design (OT assessment resolves the individual's
        own need, informed by but not bounded by the Population-Mode range).
    DAR mandatory at all modes.

    "Mode P" / "Mode S" are retired spellings (DR-2026-07-12-evidence-architecture-  [RETIRED-VOCAB-OK]
    unification Item V, ratified 2026-07-13): "Tier N" is reserved for the evidence
    ladder, and the design scales are named Universal / Population / Person only.
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
