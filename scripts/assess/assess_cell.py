#!/usr/bin/env python3
"""
scripts/assess/assess_cell.py — the determination engine (rule_version "pilot-2").

THE STATE IS COMPUTED. Owner ruling 2026-09-09 (references/project-standards.md):
*"you have to compute it. I can't handle this load manually."* That supersedes
DR-2026-08-19 §12.5's "permanently manual" clause as it applies to `specifications`,
on contact (CLAUDE.md rule 0). Two sessions had read §12.5 as retiring this engine;
that reading is closed. What §12.5 still governs is untouched: the reasoning doc, the
Opus floor on best_practice_synthesis, the B-before-E gate — and this engine still
REFUSES data/guidebook.db outright and emits SQL for replay through
emit_data_migration.py → migrate_db.py. Computing the state is not licence to write
the canonical blob.

RE-KEYED 2026-09-09 by migration 071. The cell was (item_code × population_code) and
is now (parameter_id × lens). The item layer was emptied 2026-09-01 and the seven
hardcoded PILOT_CELLS this engine used to walk — E-08, E-12, G-03, C-02, E-06, B-10 —
were prior-version containers whose names stated their answers. They are gone with the
driver that held them; the engine now takes its cell on the command line.

RE-KEYED AGAIN 2026-09-10, AND THIS TIME AT THE POINT WHERE IT DECIDES. 071 re-keyed the
cell's IDENTITY; the engine still gathered its EVIDENCE by slug, so `parameter_id` reached
sha(), the report and validate_parameter() and never reached the evidence. `param 1 × MOB
→ stated basis=T1+CO1+T2` therefore meant "everything admitted to
accessible-circulation-geometry" — 10 sources, 8 of them flagged `tier_inconsistent` by
this engine's own report, all 10 DOWN-WEIGHTED. Two changes close it:

  B4c  gather_sources() takes a parameter_id and returns the sources holding an
       EXTRACTION for it, joined on (ref_id, parameter_id). Migration 073 made
       `source_value_extractions.parameter_id` NOT NULL and `db.py add-extraction` —
       the writer that table shipped without — creates the edge this joins on.
  B5a  a source whose tier is not derivable from its own (evidence_type, scope) is
       NON-ANCHORING and cannot reach a `stated` determination. A parameter with no
       qualifying extraction is `pending` with a gap, which is what it always was.

`--slug` survives as the topic a determination is RECORDED under. It no longer selects
evidence, and every sentence this engine emits that mentions it has been re-derived to
say so.

Implements the pure determination function of workplan/best-practices-assessment-system.md
§3 under the doctrine of governance/evidence-architecture.md, with the G1/G2/G3/G6
fixes active, tagged rule_version="pilot-2". G2, G3 and G6 are RATIFIED
(RATIFICATION-PACKAGE-2026-07-12, owner directive 2026-07-13).

PROMOTED 2026-09-10 (register item Q4). G3 and G6 used to be implemented ONLY in
this engine's own `source_grain()`, while schemas/directness.py's
`GRAIN_FROM_EVIDENCE_TYPE` mapped `co1 -> specific` and `standard_eb -> code`
unconditionally — two implementations of one ratified rule, disagreeing, which is
a rule that attests nothing. `schemas.directness.grain_for()` is now the single
home; `source_grain()` is deleted from this module and `GRAIN_FROM_EVIDENCE_TYPE`
is unchanged, kept as the default map `grain_for()` falls back to. Equivalence
was checked by enumeration over every (evidence_type, tier, co1_source_type)
triple the live schema admits, not by reading: 0 of 336 triples differ, including
REF-00978's live (co1, 1, 'dpo_annual_survey') — the corpus's only Co-1 source,
whose co1_source_type is not in schemas.enums.Co1SourceType and which both the
old and new implementation grain SPECIFIC via the same unrecognised-value
fallback. G2's NOT_ASSESSED moved the same way, into schemas.directness, so it
is a first-class shared grade rather than an engine-local string.

Determinism: same evidence + same rule_version ⇒ same state + same derivation_sha.
Timestamps come from --stamp, not wall-clock reads, so a re-run is byte-identical and
the double-run determinism check (evidence-architecture.md §10, check 2) is meaningful.

Module roster (PILOT-MANIFEST.md §4 — no silent omissions):
  schemas.directness          grain-matching (grain_for, G3/G6 — promoted 2026-09-10),
                              scale-directness, consolidation, NOT_ASSESSED (G2 —
                              promoted 2026-09-10). Co1SourceType is consulted inside
                              grain_for() itself, not imported here directly.
  schemas.tier_derivation     tier/evidence_type/scope consistency audit per source
  schemas.evidence_state      EvidenceStateRecord / ConvergenceAssessment /
                              ProvisionalConfidenceFlag — every row validated
                              against the pydantic model BEFORE insert
  schemas.enums               PopulationCode / EvidenceCellState / ConvergenceStatus /
                              VerificationStatus vocabularies
  schemas.evidence_source     (via enums + verification gates below)
  schemas.source_value_extraction  the JUDGMENT item (D-0168) — what gather_sources
                              now joins on. The VALUE dimension stays NOT_ASSESSED,
                              and the reason is not emptiness: no value-directness
                              grading rule exists in this repository and inventing
                              one is stop condition 4 (G2; never silently EXACT)
  schemas.population, schemas.population_links, schemas.slug, schemas.bpc_metadata,
  schemas.gap                 identity/attribution semantics (lens codes validated
                              against their own live base tables)

G-fixes (evidence-architecture.md §4, DR-2026-07-12-evidence-architecture-unification):
  G1  T4–6-only basis ⇒ regulatory-stratum determination: design_scale='universal',
      never 'stated', code_floor_only=1 iff T6-only; T4/T5 keep GRAIN_CODE (no pilot
      source has documented T1/T2 traceability, so no re-graining is claimed).
      Engine-side (regulatory_richness(), below) — not a directness-model rule.
  G2  A directness dimension that APPLIES but has never been assessed is NOT_ASSESSED,
      not None ("not applicable"): it caps consolidation at DOWN-WEIGHTED via
      consolidate()'s existing partial-dimension path, and the source is flagged.
      schemas.directness.NOT_ASSESSED (promoted 2026-09-10; was engine-local).
  G3  Co-1 grain follows co1_source_type (dpo_research/advocacy_position → aggregate;
      academic_narrative → specific; others, including an unrecognised
      co1_source_type → specific, noted).
      schemas.directness.grain_for() (promoted 2026-09-10; was source_grain() here).
  G6  standard_eb grain follows (type × tier): T2 → aggregate; T4/T5 → code.
      schemas.directness.grain_for() (promoted 2026-09-10; was source_grain() here).
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
# EXACT, NEVER FLOAT. The ruling of 2026-09-17 turns on 1:20 being exactly 5%, and
# on 1:12 being exactly 100/12 rather than 8.33. Fraction is what makes "exact" a
# property this code can test rather than a word in a comment.
from fractions import Fraction

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

from schemas.directness import (  # noqa: E402
    GRAIN_AGGREGATE, NOT_ASSESSED, SCALE_POPULATION, SCALE_UNIVERSAL,
    SD_NON_ANCHORING,
    COND_DIRECT, COND_DOWN_WEIGHTED, COND_DISCOUNTED, COND_NON_ANCHORING,
    consolidate, grain_for, population_directness_from_match_grade, scale_directness,
)
from schemas.tier_derivation import check_tier_consistency  # noqa: E402
from schemas.enums import (  # noqa: E402
    ConvergenceStatus, EvidenceCellState, PopulationCode,
    VerificationStatus,
)
from schemas.evidence_state import (  # noqa: E402
    ConvergenceAssessment, EvidenceStateRecord, ProvisionalConfidenceFlag,
)

RULE_VERSION = "pilot-3"  # 077: derivation_sha hashes the GRADED LINK SET, not the
#   governing ref list plus an unfiltered extraction count. Bumped from pilot-2 because
#   the sha PAYLOAD FORMAT changed: `rule_version` is what tells a verifier which format
#   to recompute, so K01 dispatches on it and pilot-2 rows replayed from migration
#   history still verify against the old format. Nothing else about the rule changed.
#   The predicate that made this necessary: since 075 only figure_role IN
#   ('claim','derived') governs, so re-grading a row flipped a cell's STATE while
#   leaving the old payload byte-identical -- a BLOCKING check (K01) reporting CLEAN
#   over a determination whose inputs had changed.
#
# pilot-1 + adversarial-review corrections (see PILOT-MANIFEST §7):
#   tier_basis now describes the GOVERNING set only (supporting strata listed separately);
#   derivation_sha includes cell identity (pending cells no longer share one constant sha);
#   has_unverified_sources / all_sources_disqualified implemented per §2.8;
#   population-match rows attributed to the cell's population or treated NOT_ASSESSED;
#   §2.3 richness checks T6 jurisdiction distinctness and names its unchecked clause;
#   jurisdiction distinctness is now NORMALISED before counting (2026-09-10, audit
#   Task 4): stripped, casefolded, empty/None dropped — ("US", None) is one
#   jurisdiction, not two, and ("US","us","US ") is one, not three;
#   G2/G3/G6 grain rules promoted into schemas.directness (2026-09-10, register
#   item Q4): source_grain() deleted from this module, grain_for() is the one home;
#   gap descriptions are PARAMETER-scoped as of 2026-09-10 (they were slug-scoped, and
#   said so, back when the gather was too — absence of an extraction for the parameter
#   is not corpus-level absence, and is not the same absence a missing slug-link is);
#   ~~the SQL artifact amends v_best_practice to exclude regulatory-stratum-only rows
#   (interim, marker-based; migration 027 adds the real column).~~ WITHDRAWN
#   2026-08-22 (BRK-26): the column exists and migration 029 superseded the
#   exclusion under ratified DR-2026-07-21. See the note at the emit site.
# Run-supplied, not wall-clock: --session and --stamp. Determinism is the point
# (evidence-architecture.md §10 check 2: the engine run twice must produce a
# byte-identical derivation_sha), so the stamp is an INPUT, never `now()`.
SESSION = None
STAMP = None

# G2: "dimension applies but was never assessed" is imported from
# schemas.directness, not redefined here. PROMOTED 2026-09-10: it used to be
# engine-local, exactly the "additive rule, not touching schemas.directness"
# posture G3/G6 were also under before that promotion left one ratified rule
# with two disagreeing implementations. Passing it to consolidate() still makes
# pop_full/val_full False -> caps at DOWN-WEIGHTED — that mechanism is
# unchanged; only its home moved.

# Verification gates (evidence-methodology.md §2.2 cond. 2 / §2.8)
# D-0157: the standing is binary, so the sound set is a single value. The old
# set also admitted VERIFIED-WITH-CORRECTION, which described an event during
# verification rather than a different standing -- "it's merely verified".
VERIFIED_OK = {VerificationStatus.VERIFIED.value}
# Disqualification is now a disposition, not a status: effort spent and nothing
# found. Callers pass the disposition alongside the status; a plain UNVERIFIED
# row is not disqualified, because a return pass is still owed on it.
DISQUALIFIED_DISPOSITION = {"CLOSED"}
# Legacy statuses kept ONLY so that a fixture or an un-migrated DB still
# disqualifies correctly; live rows are disqualified by disposition.
DISQUALIFIED = {"UNVERIFIED-CLOSED", "CLOSED-DELETED"}


def _is_disqualified(rec) -> bool:
    """Effort was spent and nothing was found.

    D-0157: a plain UNVERIFIED source is NOT disqualified -- a return pass is
    still owed on it, which is what OPEN means. Disqualification is the CLOSED
    disposition on a non-VERIFIED row, the thing the old UNVERIFIED-CLOSED and
    CLOSED-DELETED values were each spelling out.
    """
    status = rec.get("verification_status") or ""
    if status in DISQUALIFIED:
        return True
    return status != "VERIFIED" and (rec.get("verification_disposition") or "") in DISQUALIFIED_DISPOSITION

# THE FOUR LENSES (owner 2026-08-28; CHECK relaxed to "at least one" by D-0182).
# Each column, the base table its real FK points into, and that table's key. Derived
# from the schema rather than restated as a vocabulary in code — the tables ARE the
# vocabulary (CLAUDE.md §4).
LENS_COLUMNS = {
    "identity_code": ("populations", "population_code"),
    # RE-POINTED 2026-09-13 (owner ruling; migration 081). Was ("axes", "axis_code"),
    # i.e. the ICF lens resolving to an AX- demand code -- the state the same day's
    # ruling bans. db._LENS_COLUMNS carries the identical pair; the extraction and the
    # determination it feeds must name the lens the same way.
    "icf_code": ("base_icf", "icf_code"),
    "needs_code": ("access_needs", "need_code"),
    "medical_code": ("base_taxonomy_medical", "medical_code"),
}
# COALESCE order, matching the table's own CHECK and test_db_integrity K01's sha payload.
LENS_ORDER = ("identity_code", "icf_code", "needs_code", "medical_code")


def lens_key(lens):
    """The single lens value a cell is identified by — COALESCE over the four.

    K01 hashes this, and the D-0182 CHECK guarantees it is never None for a row that
    reached the table. A cell may be stated in several lenses at once; the KEY is the
    first present in COALESCE order, which is what the database's own COALESCE returns.
    """
    for col in LENS_ORDER:
        if lens.get(col):
            return lens[col]
    return None


def gather_sources(conn, parameter_id):
    """The sources holding an EXTRACTION FOR THIS PARAMETER. Not the slug's sources.

    THE DEFECT THIS CLOSES, measured 2026-09-10. This function took a `slug` and
    joined `source_slug_links`, so the governing set was "everything admitted to this
    topic". `parameter_id` was carried through determine()'s signature, sha(), the
    report dict and validate_parameter() and never reached the evidence at all -- the
    071 re-key was cosmetic at the exact point where the engine decides. The visible
    result was `param 1 x MOB -> stated basis=T1+CO1+T2` anchored on all 10 sources
    linked to `accessible-circulation-geometry`, 8 of which the engine's own report
    flagged `tier_inconsistent`, and every one of the 10 DOWN-WEIGHTED.

    The cause was one absent table-writer, not a bad query: `db.py` held ZERO
    references to `source_value_extractions`, so no parameter->evidence edge existed
    and the slug was the only join available. `db.py add-extraction` (migration 073,
    same change as this) creates the edge; this query uses it.

    DISTINCT IS LOAD-BEARING, not tidiness. Evidence to judgment is 1:N (D-0168): one
    code document yields many clause-level extractions for one parameter. Without
    DISTINCT, NBC 3.8's clauses would each add a copy of the same source to the
    governing set, and a single document would look like corroboration of itself --
    the independence failure `v_value_independence` exists to detect, manufactured
    inside the engine.

    A CONSEQUENCE WORTH STATING, because it is stop condition 6 of the operative
    plan ("any `stated` cell whose governing set includes a source with no extraction
    for that parameter -- do not merge the migration"): after this change that cell is
    not merely forbidden, it is unconstructible. Every ref_id in the governing set
    came out of this query, and this query returns only sources that hold an
    extraction for the parameter being determined.

    ONLY VALUE-SUPPLYING ROWS GOVERN (added 2026-09-13, migration 075's whole point).
    Holding an extraction for the parameter was never enough. Measured on the live
    corpus the day the grading landed: specification 1 was `stated` at T1 -- the
    strongest claim this project makes -- on four rows of which TWO WERE CONDITIONS
    (the slopes a treadmill was set to; the ADA range a study tested) and two were
    findings, one of them `claim_type='absent'`, asserting nothing whatever. Not one
    governing row was a claim. Specification 2 was the same shape.

    So the predicate is `figure_role IN ('claim','derived')`:

      claim     -- the row states a value for the parameter. Governs.
      derived   -- the row's value was computed from other rows. Governs; its band
                   is the floored mean of its inputs' (owner ruling 2026-09-13).
      finding   -- the row reports something ABOUT the parameter without asserting a
                   value: "code-compliant width fails 10-100% of users". Supplies
                   DIRECTION, never value (owner ruling 2026-09-13). Not gathered here.
      condition -- a rig setting or a limit the value is conditioned by. Never anchors.
      NULL      -- ungraded. Not a value-supplier: a row nobody has stated the kind of
                   cannot be read as a claim, which is exactly how a tested slope came
                   to govern a `stated` cell.

    A cell whose value-supplying set is empty now comes out `pending`, which for both
    live cells is the truth -- not one retrieved source states a corridor width or a
    ramp gradient value. Gathering `finding` rows for direction, and the `confirms`
    edge that upgrades a code value, build ON this predicate and are not required by
    it.
    """
    # verification_disposition arrived with migration 049 (D-0157). This script
    # is run against scratch and fixture databases as well as the canonical one
    # -- it refuses the canonical DB by design -- so the column is selected only
    # when it exists. A pre-049 database still disqualifies correctly through
    # the legacy status values in DISQUALIFIED.
    has_disp = any(r[1] == "verification_disposition"
                   for r in conn.execute("PRAGMA table_info(evidence_sources)"))
    disp_col = "e.verification_disposition" if has_disp else "NULL"
    q = f"""SELECT DISTINCT e.ref_id, e.tier, e.evidence_type, e.co1_source_type,
                   e.verification_status, {disp_col}, e.scope, e.jurisdiction
            FROM source_value_extractions x
            JOIN evidence_sources e ON e.ref_id = x.ref_id
            WHERE x.parameter_id = ? AND e.superseded_by_ref_id IS NULL
              AND x.figure_role IN ('claim', 'derived')
            ORDER BY e.ref_id"""
    return [dict(zip(("ref_id", "tier", "evidence_type", "co1_source_type",
                      "verification_status", "verification_disposition",
                      "scope", "jurisdiction"), r))
            for r in conn.execute(q, (parameter_id,))]


#: Which figure_role values supply a value to a determination. ONE HOME (migration 077).
#: `gather_sources` filters on it, `gather_extraction_links` grades on it, and K01
#: recomputes the sha from the links this produces -- so the three cannot disagree.
#: Before 077 the predicate lived only inside gather_sources' SQL while the sha hashed an
#: UNFILTERED count, which is how re-grading a row could flip a cell from `stated` to
#: `pending` without moving its attestation.
VALUE_SUPPLYING_ROLES = ("claim", "derived")
CONDITIONING_ROLES = ("condition",)
#: Rows that report something ABOUT the parameter without asserting a value for it.
#: They supply DIRECTION, never value (owner ruling 2026-09-13), and since the owner
#: statement of 2026-09-16 they may also carry a determination as a PROXY -- see
#: `gather_findings` and the proxy branch in `determine()`.
DIRECTION_SUPPLYING_ROLES = ("finding",)


def gather_findings(conn, parameter_id):
    """The sources holding a FINDING for this parameter. Direction, never value.

    WHY THIS EXISTS, and it is not symmetry with `gather_sources`. Owner statement
    2026-09-16: "even if they aren't asserting a gradient, they are examining the
    impacts of gradients ... adjudication will be able to reason that whatever range
    of gradients corresponds to the best outcomes is the best range of gradient." Its
    ACTION (2) names this function's absence as the defect: "`assess_cell` must be
    able to reach a determination from findings plus a threshold, not only from
    `claim` rows -- today it cannot, and that is why batch 08 reads `refs=0`."

    WHAT THAT LOOKED LIKE. Batch 08 admitted two studies measuring articular
    discomfort rising 14->36% and pushrim force more than doubling across gradient,
    and the engine returned `pending` with `refs=0` -- which renders as "no evidence"
    over two studies that measured the thing. The rows were there; `gather_sources`
    filters `figure_role IN ('claim','derived')` and a `finding` contributed nothing
    however much it had measured.

    WHAT THIS DOES NOT DO. It does not make a finding a value-supplier. `governing`
    still means "supplied the value" and still comes from `gather_sources` alone --
    stop condition 6 of the operative plan turns on that, and migration 075 exists
    because two conditions and two findings once governed a `stated` cell. A finding
    reaching a determination through this function lands in `supporting`, and the
    determination is marked `rests_on_proxy_inference` so the book can tell an
    inference from a citation.
    """
    has_disp = any(r[1] == "verification_disposition"
                   for r in conn.execute("PRAGMA table_info(evidence_sources)"))
    disp_col = "e.verification_disposition" if has_disp else "NULL"
    q = f"""SELECT DISTINCT e.ref_id, e.tier, e.evidence_type, e.co1_source_type,
                   e.verification_status, {disp_col}, e.scope, e.jurisdiction
            FROM source_value_extractions x
            JOIN evidence_sources e ON e.ref_id = x.ref_id
            WHERE x.parameter_id = ? AND e.superseded_by_ref_id IS NULL
              AND x.figure_role IN ({",".join("?" * len(DIRECTION_SUPPLYING_ROLES))})
            ORDER BY e.ref_id"""
    return [dict(zip(("ref_id", "tier", "evidence_type", "co1_source_type",
                      "verification_status", "verification_disposition",
                      "scope", "jurisdiction"), r))
            for r in conn.execute(q, (parameter_id,) + DIRECTION_SUPPLYING_ROLES)]


def gather_extraction_links(conn, parameter_id, governing_refs):
    """Every extraction for this parameter, graded by the part it played.

    THE BACKWARD WALK STARTS HERE (migration 077). `gather_sources` returns SOURCES and
    its DISTINCT is load-bearing -- collapsing the 1:N fan-out is what stops one document
    corroborating itself -- so it cannot also tell us WHICH rows governed. This does, and
    the two are deliberately separate functions rather than one that returns both: the
    first answers "how many independent sources", the second "which sentences", and
    conflating them is how the fan-out collapse would leak into the provenance record.

    Returns one dict per extraction, with `role` in:

      governing     figure_role supplies a value AND the row's source survived the tier,
                    verification and supersession gates -- i.e. its ref_id is in the
                    governing set this determination actually used.
      conditioning  figure_role='condition'. Qualifies a governing row. Carried onto the
                    determination so a slope arrives with its run length attached.
      excluded      everything else, with a MANDATORY reason. This is the row that makes
                    a `pending` cell legible: "examined, and here is why it did not
                    answer" reads differently from silence, and the two were previously
                    indistinguishable to everything except a hash collision.

    `governing_refs` is passed in rather than re-derived because the caller has already
    applied the tier/verification/supersession gates; re-deriving them here would be a
    second implementation of the anchoring rule, free to drift from the first.
    """
    # Positional, not by name: this module's connection carries no row_factory, and
    # assuming one made the first cut of this function raise `tuple indices must be
    # integers`. The column order here is the SELECT's, which is the only contract.
    rows = conn.execute(
        "SELECT extraction_id, ref_id, figure_role, claim_type FROM "
        "source_value_extractions WHERE parameter_id = ? ORDER BY extraction_id",
        (parameter_id,)).fetchall()
    gov = set(governing_refs or ())
    out = []
    for eid, ref, frole, ctype in rows:
        if frole in VALUE_SUPPLYING_ROLES and ref in gov:
            role, why = "governing", None
        elif frole in CONDITIONING_ROLES:
            role, why = "conditioning", None
        elif frole in VALUE_SUPPLYING_ROLES:
            # Value-supplying, but its source did not survive the anchoring gates.
            role, why = "excluded", (
                f"figure_role={frole!r} supplies a value, but {ref} is not in the "
                f"governing set: it was disqualified on tier, verification or "
                f"supersession before the value was reached")
        elif frole is None:
            role, why = "excluded", (
                "figure_role IS NULL -- ungraded, so nothing states whether this row "
                "asserts a value, reports a finding, or states a condition")
        else:
            role, why = "excluded", (
                f"figure_role={frole!r} reports something ABOUT the parameter without "
                f"asserting a value for it"
                + (f" (claim_type={ctype!r})" if ctype == "absent" else ""))
        out.append({"extraction_id": eid, "ref_id": ref, "figure_role": frole,
                    "role": role, "exclusion_reason": why})
    return out


#: NOTATIONS OF ONE QUANTITY, and the arithmetic that relates them. Owner ruling
#: 2026-09-17: "Present both -- don't choose between ratio or percentage."
#:
#: THIS IS A DEFINITION, NOT A CURATED FACT, which is why it is a literal here and
#: not derived from the corpus (CLAUDE.md rule 8 asks for derivation of facts the
#: machine can compute; the relation between `1:20` and `5 %` is mathematics and
#: there is nothing in the database to read it off).
#:
#: A FAMILY IS NOT A UNIT. Members are two ways of WRITING one dimensionless
#: quantity. Millimetres and degrees are different units, and the ruling says so in
#: its own ACTION (4): composing across THEM stays refused. Adding a member here is
#: a claim that two notations denote the same quantity exactly, which is a
#: mathematical claim and should be made deliberately.
NOTATION_FAMILIES = {
    "gradient": ("%", "rise:run ratio"),
}
#: Every family member MUST appear here, and the guard below refuses one that does
#: not. Without it, adding a notation to the tuple above and forgetting the
#: arithmetic makes `to_canonical` fall through to `Fraction(text)` and read the
#: number AS IF it were already canonical -- `5` degrees silently becoming `5 %`.
#: That is the shape a reviewer of the 2026-09-17 ruling flagged: `degrees` is the
#: ARCTANGENT of the ratio, not a rescaling of it, so it is not a notation of this
#: quantity at all and belongs to a family of its own or to none. Membership is a
#: mathematical claim; this makes forgetting to back it up an error rather than a
#: wrong answer.
_CONVERTIBLE = {"%", "rise:run ratio"}
_RATIO_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\s*$")


def notation_family(unit):
    """Which family a stated unit belongs to, or None if it stands alone."""
    for fam, members in NOTATION_FAMILIES.items():
        if (unit or "").strip() in members:
            return fam
    return None


def to_canonical(raw, unit):
    """One stated value -> an exact Fraction on its family's canonical scale.

    The canonical scale is the family's FIRST member -- percent for gradient -- and
    the conversion is exact because it is done in Fraction, never float: `1:12` is
    100/12, which is 8.333... and is never rounded here. Rounding happens once, at
    render, and is marked inexact when it happens.
    """
    txt = (raw or "").strip()
    if not txt:
        return None
    fam = notation_family(unit)
    if fam and (unit or "").strip() not in _CONVERTIBLE:
        raise NotImplementedError(
            "%r is listed in NOTATION_FAMILIES[%r] but no conversion is defined for "
            "it. A family member is a claim that two notations denote ONE quantity "
            "exactly; back it with arithmetic in to_canonical/from_canonical, or "
            "remove it. Falling through here would read the number as if it were "
            "already canonical." % (unit, fam))
    m = _RATIO_RE.match(txt)
    if m and fam:
        rise, run = Fraction(m.group(1)), Fraction(m.group(2))
        if run == 0:
            return None
        return rise / run * 100                      # rise:run -> percent, exactly
    try:
        return Fraction(txt)
    except (TypeError, ValueError):
        return None


def from_canonical(value, notation):
    """A canonical Fraction -> (text, exact) in one notation of its family.

    `exact` is False when the notation cannot hold the value without rounding --
    8.333...% is the case this project actually has -- and the caller MARKS it,
    because ACTION (3) of the ruling forbids a rounded figure standing where a
    source's own figure would.
    """
    if value is None:
        return None, True
    if notation == "%":
        as_float = float(value)
        text = ("%g" % as_float)
        return text, Fraction(text) == value
    if notation not in _CONVERTIBLE:
        raise NotImplementedError(
            "no rendering defined for notation %r; see _CONVERTIBLE" % (notation,))
    if notation == "rise:run ratio":
        if value == 0:
            return "0", True
        run = Fraction(100) / value                  # percent -> 1:n, exactly
        text = "1:%g" % float(run)
        return text, Fraction(1, 1) / Fraction(text.split(":")[1]) * 100 == value
    return None, True


def bound_on_scale(claimed_value, unit, comparator, claim_type):
    """One governing claim -> (lo, hi) as exact Fractions on its family's scale.

    The same comparator rules as `parse_bound` -- the comparator IS the bound -- but
    the NUMBER goes through `to_canonical`, so `1:20` and `5 %` land on one scale and
    can be compared. `parse_bound` is left exactly as it was: it answers "what bound
    does this claim state, in its own notation", which is still what the docstring
    below promises and what other callers want. This answers the different question
    the owner ruling of 2026-09-17 requires, which is "where does this claim sit
    relative to one written the other way".
    """
    raw = (claimed_value or "").strip()
    if not raw:
        return None
    cmp_ = (comparator or "").strip()
    if cmp_ == "between" or claim_type == "range":
        parts = re.split(r"\s+to\s+", raw)
        if len(parts) == 2:
            lo, hi = to_canonical(parts[0], unit), to_canonical(parts[1], unit)
            if lo is not None and hi is not None:
                return (min(lo, hi), max(lo, hi))
        return None
    v = to_canonical(raw, unit)
    if v is None:
        return None
    if cmp_ in (">=", ">"):
        return (v, None)
    if cmp_ in ("<=", "<"):
        return (None, v)
    return (v, v)


def parse_bound(claimed_value, comparator, claim_type):
    """One governing claim -> (lo, hi) in its own unit, or None if it states no number.

    The comparator IS the bound, which is why migration 075 added it: "more than thirty
    centimetres" stored as a bare 30 turns a floor into a point, and a determination built
    from points is a determination that has quietly dropped every inequality its sources
    stated.

      =, approx, or no comparator on a numerical claim -> a point:   (v, v)
      >=, >                                            -> a floor:   (v, None)
      <=, <                                            -> a ceiling: (None, v)
      between, or a range claim written "a to b"       -> (a, b)

    STRICTNESS IS NOT MODELLED, deliberately. `>` and `>=` both land as (v, None): the
    columns are REAL and carry no open/closed flag, and inventing one here would put a
    distinction in the determination that no render surface can show and no source states
    precisely enough to defend. The comparator stays on the extraction, which is where a
    reader can see it.

    Returns None for anything that is not a number -- a qualitative claim, a ratio like
    '1:12', a value with words in it. Those govern the STATE of a cell (they are still
    `figure_role='claim'`) without contributing a numeric bound, and the caller says so
    rather than silently treating them as zero.
    """
    raw = (claimed_value or "").strip()
    if not raw:
        return None
    cmp_ = (comparator or "").strip()

    def num(tok):
        try:
            return float(tok)
        except (TypeError, ValueError):
            return None

    if cmp_ == "between" or claim_type == "range":
        parts = re.split(r"\s+to\s+|\s*-\s*|\s*–\s*", raw)
        if len(parts) == 2:
            lo, hi = num(parts[0]), num(parts[1])
            if lo is not None and hi is not None:
                return (min(lo, hi), max(lo, hi))
        return None
    v = num(raw)
    if v is None:
        return None
    if cmp_ in (">=", ">"):
        return (v, None)
    if cmp_ in ("<=", "<"):
        return (None, v)
    return (v, v)


def derivation_handshake(conn, parameter_id, lens, sources):
    """H2/H3/H4 — which paths this value was derived along, and what gates it.

    THE RULE (DR-2026-07-13, ratified; evidence-architecture.md section 5.5). The corpus
    derives values along two paths that have never been required to meet: TOP-DOWN from
    population and community, BOTTOM-UP from function (the ICF-indexed references/fdr/
    corpus, population-blind at collection). "No mechanism requires the paths to agree
    before a value ships, and dual derivation is undetectable by query."

    BOTH PATHS ARE DERIVED, NOT ASKED FOR (CLAUDE.md rule 8). The population path is present
    when governing evidence exists -- that is what the rest of this engine computes. The
    function path is present when the cell's identity lens has rows in `population_icf_links`
    -- migration 080's promotion of the functional-deficit-auditor's mapping out of skill
    prose. So `functional_basis` is READ from that table rather than typed onto the
    determination, and `derivation_paths` follows from the pair. Nothing here is a judgment
    a session could get wrong by assertion.

    THE CULTURAL/DIGNITY PROTECTION, and it is the reason this function is careful rather
    than clever. Claims whose normative force is community-rooted remain FULLY ASSERTABLE as
    `population_only`; no functional derivation may flatten, reduce or override a community
    claim; THERE IS NO BOTTOM-UP OVERRIDE OF Co-1. "A signing-space corridor width is not a
    wheelchair-envelope calculation that came out wrong; it is a different claim, held by the
    community whose language it serves."

    So the absence of a function path NEVER downgrades a cell here, and a culturally
    anchored population_only cell owes no rationale. The anchor is checked, not asserted:
    per the ratified boundary criterion, "community-rooted" means anchored by
    Co-1/participatory provenance per `co1_source_type`, and a population_only claim without
    such an anchor "is simply a single-path claim owing the standard named-path rationale;
    it gains no cultural exemption by assertion". That criterion "exists so the protection
    cannot become a route around the mechanism requirement".

    H4 GATES, with the deadlock discipline doctrine specifies:
      * they bind ONLY where a check has actually run -- so this reads gate ROWS, and no
        rows means no gating, which is the correct reading of "no silent pretence of
        coverage" rather than a gap;
      * a gate forces `provisional`, NEVER `stated`, and never below that;
      * the ladder cannot be inverted: a gate binds only when its trigger is at least as
        strong as the cell's best anchor, so "a grey-tier CONTRADICTS cannot pin a
        T1-anchored cell indefinitely".

    Returns (functional_basis_json, derivation_paths, rationale, cultural_anchor_json, gates).
    """
    identity = lens.get("identity_code")

    # --- the function path: the promoted population<->ICF map -------------------
    fb_rows = []
    if identity and _table_exists(conn, "population_icf_links"):
        fb_rows = conn.execute(
            "SELECT icf_code, mechanism, mapping_confidence, provenance "
            "FROM population_icf_links WHERE population_code = ? ORDER BY icf_code",
            (identity,)).fetchall()
    functional_basis = json.dumps(
        [{"icf_code": r[0], "mechanism": r[1], "mapping_confidence": r[2],
          "provenance": r[3]} for r in fb_rows]) if fb_rows else None

    # --- the population path ----------------------------------------------------
    has_population = bool(sources)
    has_function = bool(fb_rows)

    # --- the cultural anchor, and it is G3's predicate rather than a new one -----
    #
    # THE RATIFIED BOUNDARY CRITERION (evidence-architecture.md section 6.2, "the
    # protection is anchored, not self-declared"): "community-rooted" means anchored by
    # Co-1/participatory provenance per `co1_source_type` -- `dpo_research`,
    # `advocacy_position`, participatory peer-reviewed work -- or an equivalent
    # documented community process.
    #
    # THAT SET IS ALREADY IMPLEMENTED, ONCE, and it is not re-typed here. G3 grades
    # `dpo_research` and `advocacy_position` as population-grain COMMUNITY CONSENSUS and
    # everything else Co-1 as individual-grain, and `schemas/directness.grain_for()` is
    # that rule's ONE home -- its own comment says so, in the change that closed a
    # finding about two implementations of it disagreeing. Restating the tuple here
    # would reopen exactly that (CLAUDE.md rule 5).
    #
    # WHERE THIS IS NARROWER THAN THE DOCTRINE, STATED RATHER THAN SMOOTHED OVER.
    # "Participatory peer-reviewed work" anchors under the criterion, but nothing in the
    # schema distinguishes a participatory peer-reviewed Co-1 source from any other:
    # `co1_source_type` carries one value, `peer_reviewed_literature`, for both, and it
    # has no CHECK to widen. So such a source does NOT anchor here and owes the standard
    # named-path rationale instead. That is the conservative direction on purpose. The
    # cost is a sentence on a claim that would have been exempt; the cost of erring the
    # other way is every Co-1 claim inheriting the exemption by tier alone, which is the
    # "route around the mechanism requirement" the criterion was written to close. When a
    # participatory flag exists, widen HERE and record it.
    anchors = sorted({r["ref_id"] for r in sources
                      if r.get("evidence_type") == "co1"
                      and grain_for("co1", r.get("tier"),
                                    r.get("co1_source_type"))[0] == GRAIN_AGGREGATE})
    cultural_anchor = json.dumps(anchors) if anchors else None

    if has_population and has_function:
        paths, rationale = "dual", None
    elif has_population:
        paths = "population_only"
        rationale = None if cultural_anchor else (
            "no population_icf_links row characterises %s, so no function path exists to "
            "meet the population path; recorded as a single-path determination per H2. "
            "This is NOT a downgrade: the absence of a functional derivation never reduces "
            "a population-derived claim (DR-2026-07-13, the cultural-claim protection)."
            % (identity or "this lens"))
    elif has_function:
        paths = "function_only"
        rationale = ("no governing population evidence for this cell; the determination "
                     "rests on the functional mapping alone")
    else:
        return functional_basis, None, None, cultural_anchor, []

    # --- H4 ---------------------------------------------------------------------
    gates = []
    if _table_exists(conn, "determination_gates"):
        best = min((r["tier"] for r in sources if r.get("tier")), default=6)
        for g in conn.execute(
                "SELECT gate_id, verdict, trigger_tier, trigger_evidence_type, "
                "trigger_ref_id, detail, identity_code FROM v_open_determination_gates "
                "WHERE parameter_id = ?", (parameter_id,)):
            if g[6] and identity and g[6] != identity:
                continue                      # a gate on another lens
            if g[2] > best:
                # LADDER-INVERSION GUARD. The trigger is weaker than the cell's best
                # anchor; recorded as not-binding rather than dropped, so a reader can
                # see the gate exists and why it did not bite.
                gates.append({"gate_id": g[0], "verdict": g[1], "trigger_tier": g[2],
                              "binds": False,
                              "why": "trigger is T%d against a T%d anchor -- binding it "
                                     "would invert the ladder" % (g[2], best)})
                continue
            gates.append({"gate_id": g[0], "verdict": g[1], "trigger_tier": g[2],
                          "binds": True, "why": g[5]})
    return functional_basis, paths, rationale, cultural_anchor, gates


def _table_exists(conn, name):
    """Fixture tolerance, as everywhere else in this engine."""
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type IN ('table','view') AND name = ?",
        (name,)).fetchone() is not None


def compose_value(conn, links, direction):
    """The determination's value, selected MOST-ACCOMMODATINGLY (owner, 2026-07-21).

    Ratified rule, `governance/evidence-architecture.md`: a determination anchors on "the
    MOST ACCOMMODATING available value, read per the parameter's accessibility direction --
    best-for-the-user, not largest-number: the widest minimum corridor, but the LOWEST
    maximum threshold height and the GENTLEST maximum ramp slope." That bullet has carried
    an `[ENGINE-LAG -> DR-2026-07-21 section 5]` marker since it was written, and this
    function is the half that removes it: every `specifications.value_min/value_max/
    value_unit` since the 057 baseline has been NULL because the engine passed literal None
    into those three slots, having no rule it could apply.

    Returns (value_min, value_max, value_unit, note). A NULL triple always arrives with a
    note saying WHY, because "no value" and "no rule to pick one" are different facts and a
    determination that cannot tell them apart is the pending-versus-never-read collision
    again, one column along.

    THE FOUR WAYS IT DECLINES, each reported rather than defaulted:
      * no governing claim states a number (every one is qualitative or a ratio);
      * the governing claims are in DIFFERENT UNITS, so there is no common interval and
        converting them here would invent a figure no source stated;
      * `direction` is NULL -- nobody has recorded which way is better for a disabled
        person on this parameter, so "most accommodating" has no meaning yet
        (`db.py set-parameter-direction` is the remedy, and the note says so);
      * `direction` is `contested` -- DR-2026-07-21 section 5: where the direction is
        population-contested, most-accommodating selection is INAPPLICABLE, no single value
        is anchored, and the spread is rendered with each population's direction stated.
        Anchoring one number here would silently pick a winner between two groups of
        disabled people, which is the whole thing that safeguard exists to prevent.

    SCOPE, STATED BECAUSE IT IS AN EXTENSION. The owner's wording is about jurisdictions'
    CODE FLOORS differing. This applies the same selection to any divergent governing set,
    because it is the only composition rule this project has ruled and the alternative is
    no value at all. Recorded here rather than assumed so it can be vetoed.
    """
    gov = [l for l in links if l["role"] == "governing"]
    if not gov:
        return None, None, None, None, None    # `pending` already says this

    ids = [l["extraction_id"] for l in gov]
    # Same fixture tolerance as the direction lookup: the pilot test builds a synthetic
    # source_value_extractions with only the columns its own assertions need. A fixture
    # that cannot state a value is a fixture with no value to compose, which is a true
    # answer rather than a crash.
    _cols = {r[1] for r in conn.execute("PRAGMA table_info(source_value_extractions)")}
    if not {"claimed_value", "claimed_unit", "comparator", "claim_type"} <= _cols:
        return None, None, None, (
            "this database's source_value_extractions carries no value columns, so no "
            "interval can be composed from it"), None
    rows = conn.execute(
        "SELECT extraction_id, claimed_value, claimed_unit, comparator, claim_type "
        "FROM source_value_extractions WHERE extraction_id IN (%s)"
        % ",".join("?" * len(ids)), ids).fetchall()

    # ── COMPOSE ACROSS NOTATIONS, NEVER WITHIN ONE (owner ruling 2026-09-17) ──
    # Each governing bound is placed on a COMMON SCALE. For a value written in a
    # notation family -- `1:12` and `5 %` are two notations of one dimensionless
    # gradient -- the scale is the family's canonical member and the conversion is
    # exact, in Fraction. For anything else the scale IS the stated unit, and two
    # different ones still refuse to compose: millimetres and degrees are units, not
    # notations, and the ruling's ACTION (4) leaves that refusal alone.
    bounds, scales, stated_notations, unparsed = [], set(), set(), []
    for _eid, val, unit, cmp_, ctype in rows:
        fam = notation_family(unit)
        b = bound_on_scale(val, unit, cmp_, ctype)
        if b is None:
            # Still reported, still not silently dropped (086). What changes since the
            # ruling is that a RATIO is no longer in this bucket -- it is a notation
            # this engine can now read, and the 2-of-7 composition that motivated the
            # ruling was exactly these rows going unread.
            unparsed.append((val, unit))
            continue
        bounds.append((b, (unit or "").strip()))
        scales.add(fam or (unit or "").strip())
        if fam:
            stated_notations.add((unit or "").strip())
    if not bounds:
        return None, None, None, (
            "no governing claim states a numeric value (all are qualitative, or a "
            "notation this engine does not read into a bound)"), None
    if len(scales) > 1:
        return None, None, None, (
            "governing claims are stated in different units (%s); composing an interval "
            "would require a conversion no source stated"
            % ", ".join(sorted(repr(u) for u in scales))), None
    scale = next(iter(scales))
    family = scale if scale in NOTATION_FAMILIES else None
    unit = (NOTATION_FAMILIES[family][0] if family
            else (next(iter({u for _b, u in bounds})) or None))

    if direction is None:
        return None, None, unit, (
            "no accessibility_direction recorded for this parameter, so the "
            "most-accommodating rule (owner 2026-07-21) has nothing to read: record it "
            "with db.py set-parameter-direction"), None
    if direction == "contested":
        return None, None, unit, (
            "accessibility_direction is CONTESTED -- most-accommodating selection is "
            "inapplicable (DR-2026-07-21 section 5) and no single value is anchored; the "
            "spread is rendered with each population's direction stated"), None

    caveat = None
    if unparsed:
        _shown = ", ".join(sorted({repr(v) for v, _u in unparsed}))
        caveat = (f"composed from {len(bounds)} of {len(bounds) + len(unparsed)} governing "
                  f"claims: {len(unparsed)} state no parsable numeric bound ({_shown}) and "
                  f"contribute to the cell's STATE but not to this interval")

    los = [b[0] for b, _u in bounds if b[0] is not None]
    his = [b[1] for b, _u in bounds if b[1] is not None]
    if direction == "higher_is_better":
        # The widest minimum: the most demanding floor is the one that serves most people.
        vmin = max(los) if los else None
        vmax = max(his) if his else None
    else:                                        # lower_is_better
        # The gentlest maximum, the lowest ceiling.
        vmin = min(los) if los else None
        vmax = min(his) if his else None

    # ── AN INCOHERENT INTERVAL IS A DEFECT, NOT A VALUE ───────────────────────────
    # vmin > vmax cannot describe anything. It arises when a claim carries NO
    # comparator: `parse_bound`'s own docstring says the comparator IS the bound, and
    # a bare number is read as a POINT, so a ceiling stored without `<=` contributes
    # a floor as well. Before the 2026-09-17 ruling this was unreachable on parameter
    # 3 by luck -- the offending row was written as a ratio and the engine could not
    # read ratios, so it never reached the selection at all. Reading it exposed the
    # row. Refusing here rather than emitting means a missing comparator surfaces as
    # a named defect instead of a nonsense interval on a published determination.
    if vmin is not None and vmax is not None and vmin > vmax:
        _pointy = sorted({repr(u) for b, u in bounds
                          if b[0] is not None and b[0] == b[1]})
        return None, None, unit, (
            "INCOHERENT INTERVAL: the most-accommodating selection gives a minimum "
            "above its maximum, which describes nothing. The usual cause is a "
            "governing claim stored with NO comparator, which is read as a point "
            "value and so contributes a floor as well as a ceiling"
            + (" — point-valued claims are in %s" % ", ".join(_pointy) if _pointy else "")
            + ". Fix the comparator on the extraction (`db.py amend-extraction "
              "--field comparator`), do not widen the interval here"), None

    # ── PRESENT BOTH ──────────────────────────────────────────────────────────────
    # Every notation the governing set states, carrying the SELECTED bound. A notation
    # is `stated` when some governing claim wrote this very bound that way, and
    # `derived` when the engine rendered it -- and a derived rendering that does not
    # terminate is marked inexact, because ACTION (3) forbids a rounded figure standing
    # where a source's own figure would. 1:12 is 8.333...% and this says so.
    notations = None
    if family:
        _written = {u for b, u in bounds
                    if (vmax is not None and b[1] == vmax)
                    or (vmin is not None and b[0] == vmin)}
        notations = []
        for member in NOTATION_FAMILIES[family]:
            if member not in stated_notations:
                continue                      # the governing set never used it
            lo_txt, lo_exact = from_canonical(vmin, member)
            hi_txt, hi_exact = from_canonical(vmax, member)
            notations.append({
                "notation": member,
                "min": lo_txt, "max": hi_txt,
                "stated": member in _written,
                "exact": bool(lo_exact and hi_exact),
            })
        if len(notations) > 1:
            caveat = ((caveat + "; ") if caveat else "") + (
                "value presented in %d notations of one quantity (owner ruling "
                "2026-09-17: present both, never choose)" % len(notations))

    return (float(vmin) if vmin is not None else None,
            float(vmax) if vmax is not None else None,
            unit, caveat, notations)


def link_payload(links):
    """The governing set as `derivation_sha` hashes it, and as K01 recomputes it.

    ONE STRING, ONE FORMAT, TWO CALLERS -- this module and test_db_integrity's K01. The
    previous payload used the governing REF list plus an unfiltered extraction COUNT, and
    the count was there (per sha()'s own docstring) because the ref list alone could not
    distinguish a parameter never read from one read and rejected. Storing the graded
    links makes the real set recomputable in one query, which is the thing that docstring
    wanted and ruled out only because nothing stored it.

    Role is inside the hash, not just the id: a row moving excluded -> governing is
    EXACTLY the change that must move the attestation, and it moves no id.
    """
    return "|".join(sorted(f"{l['role']}:{l['extraction_id']}" for l in links))


def count_extractions(conn, parameter_id):
    """How many extraction rows this parameter holds, across all sources.

    Reported alongside the source count so a reader can see the 1:N fan-out rather
    than infer it: 2 sources and 9 extractions is a normal, ruled shape (D-0168), and
    a report showing only "2 sources" hides which of the two carried the clauses.
    """
    return conn.execute(
        "SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id = ?",
        (parameter_id,)).fetchone()[0]


def population_match(conn, ref_id, population):
    """Return a match_grade ONLY when a row is attributable to THIS population.
    target_population is free text, so attribution is conservative: the row must
    name the population code as a word (case-insensitive). Rows that exist but
    cannot be attributed to this population are NOT evidence of directness for
    it — the dimension stays NOT_ASSESSED (G2; a grade assessed against another
    population must never condition this cell)."""
    if not population:
        # No identity lens on this cell — a determination stated only in ICF, access-need
        # or medical terms has no population to attribute a match row TO. The dimension is
        # then unassessed rather than absent, which is G2 exactly: consolidation caps at
        # DOWN-WEIGHTED and the source is flagged. Never silently EXACT.
        return None
    rows = conn.execute(
        "SELECT match_grade, target_population FROM evidence_population_match "
        "WHERE ref_id = ? ORDER BY match_id", (ref_id,)).fetchall()
    import re as _re
    for grade, target in rows:
        if target and _re.search(rf"\b{_re.escape(population)}\b", target, _re.I):
            return grade
    return None


def assess_source(conn, src, claim_scale, population):
    """Per-source directness record under pilot rules (G2/G3/G6 active)."""
    grain, grain_why = grain_for(src["evidence_type"], src["tier"], src["co1_source_type"])
    sd = scale_directness(grain, claim_scale)
    mg = population_match(conn, src["ref_id"], population)
    if mg is not None:
        pop = population_directness_from_match_grade(mg)
    else:
        pop = NOT_ASSESSED  # G2: applies but unassessed — never graded as EXACT
    # VALUE DIMENSION: NOT_ASSESSED, and it stays that way.
    #
    # The reason is not that the table is empty — it is writable from 2026-09-10 and
    # this engine now gathers BY its rows. The reason is that NO VALUE-DIRECTNESS
    # GRADING RULE EXISTS IN THIS REPOSITORY. Grading "how directly does this
    # source's stated value bear on this cell" is a judgment act with doctrine behind
    # it, and inventing one here — at the point where it is least visible and most
    # load-bearing — is stop condition 4 of the operative plan: "Any step needing a
    # value-directness grading rule. None exists. Do not invent one."
    #
    # This comment previously read that the table "holds 8 rows as of migration 052
    # and, since that migration, an item_code to join them on". Both halves are now
    # false: the item layer was emptied 2026-09-01 and migration 073 retired
    # `item_code` from this table outright. Corrected rather than deleted, because
    # the SUBSTANTIVE claim — G2 stands, applies but unassessed, never silently
    # full-match — never depended on either.
    val = NOT_ASSESSED
    cond = consolidate(pop, val, sd)
    tier_ok = check_tier_consistency(src["evidence_type"], src["scope"], src["tier"])
    # THE TIER GATE (B5a). A source whose stored tier is not derivable from its own
    # (evidence_type, scope) CANNOT ANCHOR. `tier_basis` is the sentence a `stated`
    # determination offers as its warrant — "T1+CO1+T2" — so anchoring on a source
    # whose tier the repository cannot re-derive is asserting a warrant out of an
    # input the engine's OWN report flags as underivable. That is not a marginal
    # case: on the 2026-09-10 walk, 8 of the 10 sources in the governing set were
    # flagged `tier_inconsistent` and the cell still came out `stated`.
    #
    # Implemented as CONDITIONING rather than as a separate filter, deliberately.
    # `anchoring()` is the single function that decides what may anchor (§1.7), and
    # routing the gate through it means the exclusion propagates everywhere anchoring
    # is consulted — the T1/Co-1/T2/Co-2 set AND the T3-clinical set — instead of
    # being applied in one branch and forgotten in another. NON-ANCHORING also lands
    # the ref in `discounted_sources`, whose own definition is "cannot anchor", so
    # the convergence record says what happened rather than hiding it.
    #
    # WHAT THIS DOES NOT DO, stated so silence is not read as oversight: it does not
    # touch the G1 regulatory branch, which reads `b["t45"] + b["t6"]` unfiltered.
    # That branch never emits `stated` — it emits a Universal-Mode floor claim at
    # provisional, whose §2.3 richness test is about jurisdictional breadth. Widening
    # the gate to cover it is a doctrinal call about what an underivable tier means
    # for a code floor, and it is left open rather than decided here.
    #
    # The pre-gate grade is kept so the report shows both: a reader can see that a
    # source was DOWN-WEIGHTED on directness AND non-anchoring on tier, rather than
    # seeing one verdict and guessing which rule produced it.
    cond_before_tier_gate = cond
    if not tier_ok:
        cond = COND_NON_ANCHORING
    return {
        "ref_id": src["ref_id"], "tier": src["tier"], "evidence_type": src["evidence_type"],
        "grain": grain, "grain_why": grain_why, "scale_directness": sd,
        "population_directness": pop, "value_directness": val, "conditioning": cond,
        "conditioning_before_tier_gate": cond_before_tier_gate,
        "needs_population_assessment": pop == NOT_ASSESSED,
        "tier_consistent": tier_ok,
        "verification_status": src["verification_status"],
        "verification_disposition": src.get("verification_disposition"),
        "jurisdiction": src["jurisdiction"],  # richness §2.3 jurisdiction distinctness
    }


def classify(recs):
    """Bucket assessed sources into doctrinal strata (disqualified sources excluded)."""
    live = [r for r in recs if not _is_disqualified(r)]
    b = {"t1": [], "co1": [], "t2": [], "co2": [], "t3c": [], "t3g": [], "t45": [], "t6": []}
    for r in live:
        t, ty = r["tier"], r["evidence_type"]
        if ty == "co1":
            # §2.2 cond. 2: Co-1 counts toward `stated` only when VERIFIED
            if (r["verification_status"] or "") in VERIFIED_OK:
                b["co1"].append(r)
            else:
                b.setdefault("co1_unverified", []).append(r)
        elif ty == "co2":
            b["co2"].append(r)
        elif t == 1 and ty == "clinical":
            b["t1"].append(r)
        elif t == 2 and ty in ("sr_meta", "standard_eb"):
            b["t2"].append(r)
        elif t == 3 and ty == "clinical":
            b["t3c"].append(r)
        elif t == 3:
            b["t3g"].append(r)
        elif t in (4, 5):
            b["t45"].append(r)
        elif t == 6:
            b["t6"].append(r)
        else:
            b.setdefault("other", []).append(r)
    return b


def anchoring(recs):
    """A source anchors only if its conditioning permits (§1.7): never NON-ANCHORING/DISCOUNTED."""
    return [r for r in recs if r["conditioning"] not in (COND_NON_ANCHORING, COND_DISCOUNTED)]


def _distinct_jurisdictions(recs):
    """The set of distinct jurisdictions among `recs`, normalised.

    §2.3's "different jurisdictions" test is a count over this set's SIZE, so
    what counts as one distinct value matters. Strip whitespace, casefold, and
    drop empty/None — a source with no recorded jurisdiction contributes
    nothing to distinctness (it is not "one more jurisdiction"), and
    "US" / "us" / "US " are the same jurisdiction, not three.
    """
    out = set()
    for r in recs:
        j = r.get("jurisdiction")
        if j is None:
            continue
        j = j.strip().casefold()
        if j:
            out.add(j)
    return out


def regulatory_richness(t45, t6):
    """§2.3 richness for a T4–6-only provisional (else pending).

    Honestly-partial implementation, named as such in the rationale it emits:
    §2.3's T4 clause requires "an evidence-based value directly addressing the
    parameter" — the T4 branch checks presence only and SAYS SO. (This has now
    carried two wrong reasons in turn: first "not mechanically checkable while
    source_value_extractions is empty", then "the table now has 8 rows and, per
    migration 052, an item_code to address the parameter with" — the table holds 0
    rows and migration 073 retired `item_code` from it. The branch is unchanged
    under either, because the join was never what was missing: deciding what counts
    as "directly addressing" is a judgment call, and the rule for making it does not
    exist.) The T6 clause
    requires convergence "on the same value or range" — likewise unverifiable;
    jurisdiction distinctness IS checkable and is enforced.

    NORMALISED before counting (fixed 2026-09-10; audit Task 4). §2.3 requires
    sources "from different jurisdictions" — an untrimmed, un-casefolded set
    counted `("US", None)` as two distinct jurisdictions and `("US","us","US ")`
    as three, because `{r.get("jurisdiction") for r in recs}` is a set over raw
    strings, and a source with NO recorded jurisdiction was being counted as
    ONE. `_distinct_jurisdictions()` strips, casefolds, and drops empty/None
    before the set is built, in both the T4-5 and T6 branches."""
    jur45 = _distinct_jurisdictions(t45)
    if len([r for r in t45 if r["tier"] == 4]) >= 1:
        return True, (">=1 T4 international standard present (§2.3; the clause's "
                      "'value directly addressing the parameter' is unverified — "
                      "value extraction pending)")
    if len(t45) >= 2 and len(jur45) >= 2:
        return True, ">=2 T4-5 sources, distinct jurisdictions (§2.3)"
    jur6 = _distinct_jurisdictions(t6)
    if len(t6) >= 3 and len(jur6) >= 3:
        return True, (f">=3 T6 codes from {len(jur6)} distinct jurisdictions (§2.3; "
                      "value-level convergence unverified — extraction pending)")
    return False, "below §2.3 richness"


def sha(parameter_id, lens, links):
    """Cell-scoped derivation sha: identity + governing set + EVIDENCE READ + rule
    version, so pending cells do not all share one constant hash (staleness stays
    checkable).

    The payload is byte-for-byte what test_db_integrity K01 recomputes when it verifies
    a stored sha, and K01 was re-keyed to (parameter_id × lens) by migration 071. Two
    implementations of one hash that disagree is a hash that attests nothing, so this
    one and K01's move together or not at all. `lens` is the COALESCE value, not the
    whole dict — see lens_key().

    WHY `n_extractions` IS IN THE PAYLOAD (added 2026-09-10). Without it, two
    materially different cells hash IDENTICALLY, because both have an empty governing
    set:

        (a) a parameter NEVER READ            — 0 sources, 0 extractions
        (b) a parameter READ AND REJECTED     — 2 sources, 2 extractions, both
                                                non-anchoring on tier (B5a)

    Reproduced 2026-09-10: both produced f6c0126a5726af3c…. Their gap DESCRIPTIONS
    differ; the attestation did not. B5a creates a new route into that collision class
    and, on today's corpus — where every source's tier is underivable from its own
    (evidence_type, scope) — the universal one. So the sha failed to move across
    exactly the transition this change exists to make visible: somebody reading the
    parameter for the first time.

    WHY THE COUNT AND NOT THE SORTED GATHERED-REF SET, which is the other candidate
    and carries strictly more information (it would also move when one rejected source
    is swapped for another). K01 must recompute this payload from the database, and
    `specifications` stores neither quantity. A count is recomputable there in one
    line — `SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id = ?`,
    the whole of `count_extractions()`. The gathered set is not: reproducing it means
    reproducing gather_sources()' DISTINCT and its `superseded_by_ref_id IS NULL`
    filter inside the check, i.e. a SECOND HOME for the gather rule, free to drift
    from the engine's. A hash whose two implementations can silently disagree attests
    nothing, which is the exact failure this docstring already warns about. The count
    is the largest payload term that keeps one home.

    CONSEQUENCE, stated because it widens K01: the sha now moves when EVIDENCE for the
    parameter is added, not only when the stored row is edited. That is the doctrine
    it was built for — evidence-architecture §10 mechanical check 2, "same evidence +
    same rule_version ⇒ same state + same derivation_sha". A determination stamped
    before an extraction arrived IS stale, and K01 saying so is the check working.
    """
    payload = f"{parameter_id}|{lens}|" + link_payload(links) + "::" + RULE_VERSION
    return hashlib.sha256(payload.encode()).hexdigest()


def determine(conn, parameter_id, lens, slug, note):
    """The pure determination function. Returns (record dicts for insert, log).

    `lens` is the four-column dict; at least one value is non-None (D-0182). Only the
    identity lens conditions population-directness, because that is the only one
    evidence_population_match.target_population is written in — a cell in ICF or
    access-need terms alone leaves the dimension NOT_ASSESSED, which caps it at
    DOWN-WEIGHTED under G2 rather than pretending to a match.
    """
    identity = lens.get("identity_code")
    # THE SUBJECT, not the topic. Sources are gathered by the extractions they hold
    # for THIS parameter (B4c); `slug` no longer selects evidence and is carried only
    # as the topic the determination was recorded under.
    sources = gather_sources(conn, parameter_id)
    n_extractions = count_extractions(conn, parameter_id)
    recs = [assess_source(conn, s, SCALE_POPULATION, identity) for s in sources]
    b = classify(recs)
    # THE DIRECTION SET (owner 2026-09-16, ACTION 2). Sources holding a `finding` for
    # this parameter: they measured an effect without stating a value. Assessed through
    # exactly the same gates as the value-supplying set -- tier consistency,
    # disqualification, population directness -- because a finding that cannot anchor
    # for one of those reasons cannot carry a proxy inference either.
    finding_sources = gather_findings(conn, parameter_id)
    finding_recs = [assess_source(conn, s, SCALE_POPULATION, identity)
                    for s in finding_sources]
    fb = classify(finding_recs)
    finding_anchors = (anchoring(fb["t1"]) + anchoring(fb["co1"])
                       + anchoring(fb["t2"]) + anchoring(fb["co2"]))
    # §2.8 verification-status machinery
    live = [r for r in recs if not _is_disqualified(r)]
    has_unverified = any((r["verification_status"] or "") == "UNVERIFIED" for r in live)
    all_disqualified = bool(recs) and not live
    anchors = anchoring(b["t1"]) + anchoring(b["co1"]) + anchoring(b["t2"]) + anchoring(b["co2"])
    t3c = anchoring(b["t3c"])
    regulatory = b["t45"] + b["t6"]
    down_weighted = [r["ref_id"] for r in recs if r["conditioning"] == COND_DOWN_WEIGHTED]
    discounted = [r["ref_id"] for r in recs
                  if r["conditioning"] in (COND_DISCOUNTED, COND_NON_ANCHORING)]

    axes_clinical = [r["ref_id"] for r in anchors + t3c if r["evidence_type"] not in ("co1", "co2")]
    axes_co1 = [r["ref_id"] for r in anchors if r["evidence_type"] == "co1"]
    axes_co2 = [r["ref_id"] for r in anchors if r["evidence_type"] == "co2"]
    n_axes = sum(1 for a in (axes_clinical, axes_co1, axes_co2) if a)

    conv = None
    state, design_scale = None, SCALE_POPULATION
    tier_basis, governing, conf, gap_needed = None, [], None, False
    code_floor_only, regulatory_stratum_only = 0, 0
    rests_on_proxy_inference = 0
    falsification = None

    supporting = []
    if anchors:
        state = "stated"
        governing = sorted(r["ref_id"] for r in anchors)
        # tier_basis describes the GOVERNING set only (adversarial finding 8);
        # supporting strata (e.g. T3 when anchors exist) are listed separately.
        parts = [p for p, k in (("T1", b["t1"]), ("CO1", b["co1"]), ("T2", b["t2"]),
                                ("CO2", b["co2"])) if anchoring(k)]
        tier_basis = "+".join(parts)
        if t3c:
            supporting = sorted(r["ref_id"] for r in t3c)
        axes_named = [n for n, a in (("clinical", axes_clinical), ("co1", axes_co1),
                                     ("co2", axes_co2)) if a]
        if n_axes >= 2:
            # Axis co-presence is real; value-level convergence is NOT assessable
            # here. pending_assessment is the honest status — never claim
            # 'convergent' on ungraded values (G2 spirit).
            # The reason used to be given as "source_value_extractions empty",
            # both here and in the emitted rationale below. That is now false in
            # general (8 rows, item-typed since migration 052) AND it was never
            # something this code checked — it asserted a fact about the table it
            # had not queried. The true reason is narrower and does not expire:
            # no rule exists for grading value-level convergence, so nothing here
            # can grade it.
            # Rendering a pending_assessment cell deviates from §3.4's no-render
            # rule and is DR-gated as item G8 (mandatory disclosure in rendering).
            conv_status = "pending_assessment"
            rationale = (f"{n_axes} evidence axes present ({'/'.join(axes_named)}). "
                         f"Value-level convergence not yet assessable: no rule "
                         f"exists for grading agreement between extracted values; "
                         f"assessment queued, not assumed."
                         + (f" Supporting (non-governing) T3: {', '.join(supporting)}."
                            if supporting else ""))
        else:
            conv_status = "single_axis"
            axis = axes_named[0] if axes_named else "clinical"
            rationale = (f"single evidence axis: {axis}"
                         + (f"; supporting (non-governing) T3: {', '.join(supporting)}"
                            if supporting else ""))
        conv = dict(status=conv_status, clinical=axes_clinical, co1=axes_co1, co2=axes_co2,
                    downw=down_weighted, disc=discounted, rationale=rationale, synth=None)
        falsification = ("Overturned if the anchoring sources are retracted/superseded, or if "
                         "value-level extraction shows the axes diverge (then divergence protocol "
                         "§3.3 applies and a synthesis approach is owed).")
    elif t3c:
        # DR-2026-07-12-tier3-stated-threshold: T3-clinical-alone -> provisional
        state = "provisional"
        governing = sorted(r["ref_id"] for r in t3c)
        tier_basis = "T3-only"
        conv = dict(status="single_axis", clinical=[r["ref_id"] for r in t3c], co1=[], co2=[],
                    downw=down_weighted, disc=discounted,
                    rationale="single evidence axis: T3-clinical alone — 'rarely the sole basis' "
                              "(tier-system.md §1); provisional per tier3-stated-threshold DR",
                    synth=None)
        conf = dict(present=["Tier 3 lower-control primary clinical research"],
                    absent=["No Tier 1 clinical", "No Co-1", "No Tier 2 synthesis", "No Co-2 CPG"],
                    basis=f"Qualified synthesis from {len(t3c)} T3-clinical sources on {slug}")
        falsification = ("Overturned if T1/Co-1/T2/Co-2 evidence emerges (cell upgrades to stated "
                         "per §2.7) or the T3 sources are retracted (cell downgrades to pending).")
    elif regulatory:
        # G1: the determination is a Universal-Mode regulatory claim, never best practice.
        #
        # ── OPEN DOCTRINAL QUESTION, RECORDED 2026-09-10, DELIBERATELY NOT DECIDED ──
        # The B5a tier gate above conditions a source to NON-ANCHORING when its stored
        # tier is not derivable from its own (evidence_type, scope). That gate reaches
        # this branch NOT AT ALL: `regulatory = b["t45"] + b["t6"]` is unfiltered, and
        # unlike the T1/Co-1/T2/Co-2 and T3-clinical sets it does not pass through
        # `anchoring()`. Two consequences, both real and neither reachable on today's
        # corpus (0 sources at T4-T6, measured 2026-09-10):
        #
        #   1. A T4 source with scope=NULL -- tier underivable, exactly the state all
        #      nine live sources are in -- still reaches state=provisional,
        #      basis='T4-5-only', and writes a `specifications` row plus a `governing`
        #      link on a tier the repository cannot re-derive. The B5a comment in
        #      assess_source() says a warrant asserted out of an underivable tier is
        #      the defect; here it is asserted anyway.
        #
        #   2. B5a CHANGED WHAT REACHES THIS BRANCH. A cell whose T1 sources all fail
        #      the tier gate no longer stops at `stated` -- it falls through to here
        #      and, if any T4-6 source is present, emits a Universal-Mode FLOOR CLAIM.
        #      That is not a weaker version of the same claim; it is a different KIND
        #      of claim about the same cell, produced by a gate that was only meant to
        #      withhold anchoring.
        #
        # WHY IT IS LEFT OPEN. Whether an underivable tier disqualifies a CODE
        # citation is not the same question as whether it disqualifies an anchoring
        # source. A code's tier is a fact about the document's legal standing, and
        # `check_tier_consistency` derives tier from (evidence_type, scope) -- a map
        # built for the research ladder. Widening the gate to cover T4-6 might be
        # right, or might mean the map needs a regulatory arm; deciding that from
        # inside a defect fix is inventing doctrine at the point where it is least
        # visible, which is the failure this engine's own G2 comment refuses. Whoever
        # takes it: it is a §2.3/tier-system question, it needs a DR, and the two
        # consequences above are the evidence it should start from.
        rich, why = regulatory_richness(b["t45"], b["t6"])
        design_scale = SCALE_UNIVERSAL
        regulatory_stratum_only = 1
        code_floor_only = 1 if (b["t6"] and not b["t45"]) else 0
        if rich:
            state = "provisional"
            governing = sorted(r["ref_id"] for r in regulatory)
            _floor = ("T6-only" if code_floor_only else
                      ("T4-6-only" if b["t6"] else "T4-5-only"))
            if finding_anchors:
                # ── THE PROXY BRANCH (owner statement 2026-09-16, ACTIONS 1 and 2) ──
                #
                # The threshold is the regulatory stratum; the DIRECTION is measured by
                # anchoring-tier findings. Together they reach a determination that the
                # floor claim alone cannot: the codes say what is permitted, and the
                # findings say which end of what is permitted the evidence favours.
                # `compose_value` then selects most-accommodatingly, which is where the
                # findings actually bite -- without them, "gentlest ceiling" is a rule
                # with no evidence behind it on this parameter.
                #
                # WHAT CHANGES, AND WHAT DELIBERATELY DOES NOT:
                #   * `governing` is UNCHANGED. Findings do not supply values, so they
                #     do not govern -- stop condition 6 and migration 075 both turn on
                #     that, and the whole point of 075 was that findings and conditions
                #     had once governed a `stated` cell. They land in `supporting`.
                #   * `regulatory_stratum_only` becomes 0, because it is no longer TRUE:
                #     the evidence basis is not only the regulatory stratum. The
                #     tier_basis marker moves with it, because register_integrity_check
                #     cross-checks the two and a disagreement is a tuple misreport.
                #   * The absence list is CORRECTED. It read "No Tier 1 clinical" over a
                #     parameter with T1 dose-response evidence -- an assertion of absence
                #     across evidence that exists, which is the reading the owner called
                #     wrong.
                #   * `state` stays `provisional`, never `stated`. ACTION (1): a
                #     determination may rest on findings "marked as a proxy, never as a
                #     stated value". `stated` is what a source stating the value earns.
                rests_on_proxy_inference = 1
                regulatory_stratum_only = 0
                supporting = sorted(r["ref_id"] for r in finding_anchors)
                _fparts = [n for n, k in (("T1", fb["t1"]), ("CO1", fb["co1"]),
                                          ("T2", fb["t2"]), ("CO2", fb["co2"]))
                           if anchoring(k)]
                tier_basis = f"{_floor}-threshold+{'+'.join(_fparts)}-direction(proxy_inference)"
                _fax_clin = [r["ref_id"] for r in finding_anchors
                             if r["evidence_type"] not in ("co1", "co2")]
                _fax_co1 = [r["ref_id"] for r in finding_anchors
                            if r["evidence_type"] == "co1"]
                _fax_co2 = [r["ref_id"] for r in finding_anchors
                            if r["evidence_type"] == "co2"]
                # THE AXIS COUNT IS THE SAME RULE AS THE ANCHORED BRANCH, and it has to
                # be: `validate_evidence_state` recomputes it and refuses a convergence
                # row whose status contradicts the axes it carries. The first cut of
                # this branch hard-coded `single_axis` while populating three axes, and
                # that check caught it -- which is the check doing exactly its job.
                # `pending_assessment` rather than `convergent` for two or more, for the
                # reason the anchored branch gives at length: no rule exists for grading
                # value-level agreement, and on a PROXY determination there is even less
                # to grade, because the axes agree about DIRECTION and state no value.
                _fn_axes = sum(1 for a in (_fax_clin, _fax_co1, _fax_co2) if a)
                conv = dict(status=("pending_assessment" if _fn_axes >= 2 else "single_axis"),
                            clinical=_fax_clin, co1=_fax_co1, co2=_fax_co2,
                            downw=down_weighted, disc=discounted,
                            rationale="PROXY: the regulatory stratum supplies the threshold "
                                      "(" + why + ") and " + str(len(finding_anchors)) +
                                      " anchoring-tier finding(s) supply the direction. The "
                                      "value is selected most-accommodatingly within what the "
                                      "threshold permits; no source states it. Owner "
                                      "2026-09-16: 'yes it's not perfect it's a proxy'.",
                            synth=None)
                conf = dict(present=[f"Tier 4-5 standards ({len(b['t45'])})",
                                     f"Tier 6 statutory codes ({len(b['t6'])})",
                                     f"Anchoring-tier findings supplying direction "
                                     f"({len(finding_anchors)}: {'+'.join(_fparts)})"],
                            absent=["No source states a value for this parameter at an "
                                    "anchoring tier -- the threshold is regulatory and the "
                                    "direction is inferred, so this is a PROXY determination "
                                    "and not a best-practice claim"],
                            basis="Threshold from the regulatory stratum (" + why + "), "
                                  "direction from measured findings. A proxy inference under "
                                  "the owner statement of 2026-09-16, marked as one.")
                falsification = ("Overturned if a source states a value for this parameter at "
                                 "an anchoring tier (the cell then rests on that, not on a "
                                 "proxy), if the findings supplying direction are retracted or "
                                 "re-graded off `finding`, or if the cited threshold editions "
                                 "are superseded. It does NOT become a best-practice claim by "
                                 "more codes agreeing (§2.7), and the proxy step is degenerate "
                                 "without the threshold: 'best outcomes' alone resolves to the "
                                 "gentlest gradient physically possible, which for a ramp is "
                                 "not a ramp.")
            else:
                tier_basis = _floor + "(regulatory_stratum_only)"
                conv = dict(status="single_axis", clinical=[], co1=[], co2=[],
                            downw=[], disc=discounted,
                            rationale="regulatory stratum only (T4-6): convergence-not-evidence "
                                      "(tier-system.md §3). Universal-Mode regulatory "
                                      "determination; richness: " + why,
                            synth=None)
                conf = dict(present=[f"Tier 4-5 standards ({len(b['t45'])})",
                                     f"Tier 6 statutory codes ({len(b['t6'])})"],
                            absent=["No Tier 1 clinical", "No Co-1", "No Tier 2 synthesis",
                                    "No Co-2 CPG", "No Tier 3 clinical"],
                            basis="Regulatory-stratum floor synthesis (" + why + "). NOT an "
                                  "evidence-anchored best practice: no anchoring dimension "
                                  "exists.")
                falsification = ("This is a floor claim: overturned if the cited editions are "
                                 "superseded. It never becomes a best-practice claim by more "
                                 "codes agreeing; only T1/Co-1/T2/Co-2 evidence can do that "
                                 "(§2.7).")
        else:
            state = "pending"
            gap_needed = True
    elif b["t3g"]:
        # tier3-threshold DR item 2: T3-grey-alone does not even reach provisional
        state = "pending"
        gap_needed = True
    else:
        # B5a, second half — AND THIS BRANCH IS NOW REACHABLE FOR AN HONEST REASON.
        # It catches three distinct states that all mean the same thing for the book:
        # the parameter has no extractions at all; it has extractions but every
        # source holding one is disqualified; or every one of them failed the tier
        # gate above and so cannot anchor. In each case there is no qualifying
        # evidence FOR THIS PARAMETER, and the honest cell is `pending` with a gap.
        # Before B4c the same cell came out `stated` on the slug's evidence, none of
        # which had been read for this parameter.
        state = "pending"
        gap_needed = True

    # THE PROVENANCE RECORD (migration 077). Graded AFTER the state is settled, because
    # `governing` means "its source survived the anchoring gates this determination
    # applied" -- which is not knowable until those gates have run. Every extraction for
    # the parameter appears exactly once, so a `pending` cell carries the reasons it is
    # pending rather than leaving a reader to infer them from an absence.
    links = gather_extraction_links(conn, parameter_id, governing)

    # THE VALUE (078). Selected most-accommodatingly per the parameter's recorded
    # accessibility direction -- the ratified rule the engine has been unable to obey
    # since 2026-07-21 for want of that one piece of metadata.
    # TOLERANT OF A FIXTURE DATABASE, the same way `gather_sources` is tolerant of a
    # pre-049 one: this engine is run against scratch and synthetic databases as well as
    # the canonical schema, and `scripts/tests/test_assess_cell_pilot.py` builds one with
    # no `base_parameters` at all. A missing table means no direction is recorded, which
    # `compose_value` already handles and reports -- degrading to "cannot select" is
    # correct; raising would make the engine untestable on a fixture.
    _has_params = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='base_parameters'"
    ).fetchone() is not None
    _direction = None
    if _has_params:
        _cols = {r[1] for r in conn.execute("PRAGMA table_info(base_parameters)")}
        if "accessibility_direction" in _cols:
            _dir_row = conn.execute(
                "SELECT accessibility_direction FROM base_parameters "
                "WHERE parameter_id = ?", (parameter_id,)).fetchone()
            _direction = _dir_row[0] if _dir_row else None
    value_min, value_max, value_unit, value_note, value_notations = \
        compose_value(conn, links, _direction)

    # THE DERIVATION HANDSHAKE (080). H2/H3/H4 of DR-2026-07-13, whose
    # `[ENGINE-LAG 2026-08-15]` marker has named this absence ever since: "`specifications`
    # carries neither `functional_basis` nor `derivation_paths`; `population_icf_links` does
    # not exist; `assess_cell.py` implements no H4 gate." All three now exist, so the engine
    # reads them.
    #
    # BOTH PATHS ARE DERIVED, NEVER ASSERTED (CLAUDE.md rule 8). The population path is the
    # governing evidence this function has already computed; the function path is whatever
    # `population_icf_links` records for this cell's identity lens. An author cannot get
    # either wrong by typing, because neither is typed.
    functional_basis, derivation_paths, derivation_rationale, cultural_claim_anchor, gates = \
        derivation_handshake(conn, parameter_id, lens, sources)

    # H4, AND IT MOVES IN EXACTLY ONE DIRECTION. Doctrine: FDA verdicts UNLINKED /
    # MISLINKED / UNDER-CONSERVATIVE and FDR delta-classification CONTRADICTS "force the
    # affected cell to `provisional` -- never `stated` -- until resolved." That is a CAP,
    # not a downgrade ladder: a gate never lifts a `pending` cell up to provisional, and
    # never pushes a provisional cell lower. The ladder-inversion guard is upstream, in
    # derivation_handshake(), which marks a gate weaker than the cell's best anchor
    # `binds: False` rather than dropping it -- so a grey-tier CONTRADICTS cannot pin a
    # T1-anchored cell, and a reader can still see the gate existed and why it did not bite.
    #
    # THE GATE IS NOT COPIED ONTO THE DETERMINATION, and that is rule 5 rather than an
    # omission. A gate row is addressed by (parameter_id, identity_code) and reachable
    # through `v_open_determination_gates`; writing its id into `specifications` as well
    # would build the second home that a parity check can only make permanent. What the
    # row carries is the EFFECT -- a cell with anchors in `tier_basis` sitting at
    # `provisional` -- and `derivation_handshake_integrity` is what holds the two in step.
    if state == "stated" and any(g["binds"] for g in gates):
        state = "provisional"

    return {
        "links": links,
        "value_min": value_min, "value_max": value_max, "value_unit": value_unit,
        "value_note": value_note, "value_notations": value_notations,
        "accessibility_direction": _direction,
        "n_extractions": n_extractions,
        "parameter_id": parameter_id, "lens": dict(lens), "lens_key": lens_key(lens),
        "slug": slug, "note": note,
        "state": state, "design_scale": design_scale, "tier_basis": tier_basis,
        "governing_refs": governing, "supporting_refs": supporting,
        "convergence": conv, "confidence": conf,
        "gap_needed": gap_needed, "code_floor_only": code_floor_only,
        "regulatory_stratum_only": regulatory_stratum_only,
        "rests_on_proxy_inference": rests_on_proxy_inference,
        # Counted so the GAP DESCRIPTION can name the right absence. A parameter read
        # only into `finding` rows has sources that qualify perfectly well and supply
        # no value, which is a different fact from having none and a different fact
        # again from having them all superseded.
        "n_finding_sources": len(finding_sources),
        "n_finding_anchors": len(finding_anchors),
        "has_unverified_sources": 1 if has_unverified else 0,
        "all_sources_disqualified": 1 if all_disqualified else 0,
        "falsification": falsification,
        "derivation_sha": sha(parameter_id, lens_key(lens), links),
        "functional_basis": functional_basis,
        "derivation_paths": derivation_paths,
        "derivation_rationale": derivation_rationale,
        "cultural_claim_anchor": cultural_claim_anchor,
        "gates": gates,
        "n_sources": len(sources),
        "needs_population_assessment": sorted(r["ref_id"] for r in recs
                                              if r["needs_population_assessment"]),
        "tier_inconsistent": sorted(r["ref_id"] for r in recs if not r["tier_consistent"]),
        # B5a made visible. `tier_inconsistent` was ALREADY reported before this
        # change and the cell came out `stated` anyway -- a report naming the defect
        # beside a verdict that ignored it. This key names the sources the tier gate
        # actually excluded, so the report says what the engine DID, not only what it
        # noticed. The two lists coincide today by construction; they are kept
        # separate because the reasons differ and a future gate may widen one.
        "non_anchoring_on_tier": sorted(r["ref_id"] for r in recs
                                        if not r["tier_consistent"]),
        "source_records": recs,
    }


def next_gap_id(conn):
    """Zero-padded to three digits, because the schema and the Pydantic model both
    require it. This minted `GAP-1` until 2026-09-09 — one short of `^GAP-\\d{3,4}$` —
    so every gap it created failed EvidenceStateRecord's own validator at the pydantic
    gate, which is where a pending cell dies. The bug survived because the pilot's
    pending cells were never replayed."""
    rows = [r[0] for r in conn.execute("SELECT gap_id FROM gaps WHERE gap_id LIKE 'GAP-%'")]
    mx = max((int(g.split("-")[1]) for g in rows if g.split("-")[1].isdigit()), default=0)
    return f"GAP-{mx + 1:03d}"


ENUM_DRIFT = []  # populations valid in the live table but missing from PopulationCode


class Refusal(ValueError):
    """A deliberate refusal by the engine, addressed to the operator.

    A separate class rather than a bare ValueError so `__main__` can print these as
    sentences and leave everything else its traceback. The distinction is load-bearing:
    pydantic's ValidationError IS a ValueError, and a model rejecting a row THIS ENGINE
    built is an engine defect, not an operator mistake — it is how the GAP-1 padding bug
    (see next_gap_id) would have surfaced had a pending cell ever been replayed. Dressing
    that as a one-line refusal and throwing its location away is how such a defect gets
    read as a typo and retried.

    `scripts/dbcore.py` defines a class of the same name for the same reason, covering
    `db.py`'s write surface. The duplication is deliberate: this engine's import roster is
    documented per PILOT-MANIFEST.md §4 and reaches only `schemas.*`, and coupling it to
    the write library to share an exception class neither surface ever catches from the
    other would buy nothing.
    """


def validate_parameter(conn, parameter_id):
    """The SUBJECT must exist and be alive (owner 2026-08-26; migration 071).

    A merged or retired parameter is refused rather than written: a determination keyed
    on a parameter that was folded into another is a determination about a subject that
    no longer stands on its own, and the FK cannot see the difference because the row
    is still there.
    """
    row = conn.execute("SELECT status, merged_into FROM base_parameters "
                       "WHERE parameter_id=?", (parameter_id,)).fetchone()
    if not row:
        raise Refusal(
            f"parameter_id {parameter_id}: no such parameter. Mint one from a term:\n"
            f"  db.py add-parameter --term-id TERM-NNN --session ...")
    status, merged_into = row[0], row[1]
    if status != "active":
        target = f" (merged into {merged_into})" if merged_into else ""
        raise Refusal(
            f"parameter_id {parameter_id} is {status}{target}, not active. "
            f"Key the determination on the surviving parameter.")


def validate_lens(conn, lens):
    """Every supplied lens code must be live in its OWN base table, and at least one
    must be supplied (D-0182).

    The codes are checked against the tables, never against a list in code: the base
    tables ARE the vocabulary (CLAUDE.md §4). schemas.enums.PopulationCode is still
    consulted for the identity lens ONLY to record drift — the pilot found the enum's
    25 values did not match the table's 22 codes — and a mismatch is a finding, never a
    refusal, because the table is the truth and the enum is the copy.
    """
    if not lens_key(lens):
        raise Refusal(
            "a determination must be stated in at least one lens (D-0182): pass one or "
            "more of --identity / --icf / --needs / --medical. A cell in no lens is a "
            "cell about nobody.")
    # A BLANK IS NOT AN ABSENCE. `--identity ""` used to skip validation here (falsy),
    # satisfy lens_key() at the NEXT lens (truthiness), and be INSERTed as '' — which
    # COALESCE then returns as the key, so the row hashed one lens and was keyed on
    # another, and PRAGMA foreign_key_check reported a violation against `populations`.
    # Blanks are normalised to None before anything reads them.
    for col in LENS_ORDER:
        if lens.get(col) is not None and not str(lens[col]).strip():
            lens[col] = None
    for col, (table, key) in LENS_COLUMNS.items():
        code = lens.get(col)
        if not code:
            continue
        if not conn.execute(f"SELECT 1 FROM {table} WHERE {key}=?", (code,)).fetchone():
            raise Refusal(f"{col} {code!r} is not a live {key} in {table}")
    identity = lens.get("identity_code")
    if identity:
        try:
            PopulationCode(identity)
        except ValueError:
            ENUM_DRIFT.append(identity)


def validate_cell_undetermined(conn, parameter_id, lens):
    """This cell must not already carry a determination.

    `idx_spec_row_identity` (migration 071) is UNIQUE on the cell itself —
    `parameter_id` plus the four lens columns COALESCEd to `''` — so a second run for
    the same cell has always been refused. It was refused in the WRONG PLACE. The
    refusal fired inside the `specifications` INSERT, after the whole determination had
    been computed, as an untranslated `sqlite3.IntegrityError: UNIQUE constraint failed:
    index 'idx_spec_row_identity'`: a stack trace naming an index rather than a cell, no
    `--emit-sql` file written, and nothing said about what had happened or what to do.
    The engine knows the cell from argv, before it reads a single source, so it asks
    here — ahead of the gather, ahead of `next_gap_id`, ahead of the pydantic gate.

    The check restates the index's own COALESCE expression rather than probing for the
    error, so the two cannot drift apart on the blank-versus-NULL question that made the
    index need COALESCE in the first place. `validate_lens()` has already normalised
    blanks to None by the time this runs, which is what makes that restatement exact.

    THE REFUSAL NOW NAMES A REMEDY, because the owner made the decision it was waiting
    for. Until 2026-09-16 this asked "does a row exist for this cell" and named no way
    forward, deliberately: revisiting a determined cell needed a SUPERSEDE DESIGN, and a
    helpful-sounding suggestion here — delete the row, re-run on a fresh copy, bump the
    id — would have been that design, written in a help string by the one component that
    must not make it.

    The owner ruled "retire in place, never hard-delete" on 2026-09-16, which migration
    076 had already predicted would land here: "assess_cell's re-determination refusal
    could key on NOT RETIRED rather than NOT EXISTS". Migration 083 made
    `idx_spec_row_identity` PARTIAL over live rows, so the question this asks is now "is
    there a LIVE determination for this cell" — one live row per cell, any number of
    retired ones behind it. The remedy named below is the owner's design, not this
    function's invention, and the retirement it points at refuses without a reason.
    """
    where = ("parameter_id=? AND COALESCE(identity_code,'')=? "
             "AND COALESCE(icf_code,'')=? AND COALESCE(needs_code,'')=? "
             "AND COALESCE(medical_code,'')=?")
    vals = (parameter_id,) + tuple(lens.get(c) or "" for c in LENS_ORDER)
    # LIVE rows only. A retired determination is history, not an obstacle — that is the
    # whole point of retiring in place, and it must match idx_spec_row_identity's own
    # partial predicate (migration 083) or the two drift apart exactly as the COALESCE
    # expression above was written to avoid.
    row = conn.execute(
        "SELECT specification_id, state, rule_version, derivation_sha, created_at, "
        f"created_by_session FROM specifications WHERE {where} "
        "AND retired_at IS NULL", vals).fetchone()
    if not row:
        return
    spec_id, state, rule_version, dsha, created_at, created_by = row
    raise Refusal(
        f"cell {parameter_id}×{lens_key(lens)} is ALREADY DETERMINED. "
        f"specification_id {spec_id}, state {state!r}, rule_version {rule_version!r}, "
        f"derivation_sha {str(dsha)[:12]}, written {created_at} by session "
        f"{created_by}.\n"
        f"  Nothing was computed; no SQL artifact was written; the database is "
        f"unchanged.\n"
        f"  This is not a fault in the run. `idx_spec_row_identity` is UNIQUE on "
        f"(parameter_id, identity_code, icf_code, needs_code, medical_code) over LIVE "
        f"rows, so a cell carries one live determination at a time.\n"
        f"  TO RE-DETERMINE, retire the standing one first — it stays in the table as "
        f"history:\n"
        f"      python3 scripts/db.py retire-specification --specification-id {spec_id} "
        f"--reason '<why this determination no longer stands>' --session <session>\n"
        f"  Then run this engine again. Retirement refuses without a reason, and the "
        f"new determination links back to the retired one. Owner ruling 2026-09-16, "
        f"'retire in place, never hard-delete'.\n"
        f"  If you meant a DIFFERENT cell, the difference has to be in --parameter-id "
        f"or in --identity/--icf/--needs/--medical. --slug is not part of the cell's "
        f"identity: it records the topic, and changing it changes nothing here.")


def validate_with_models(det, gap_id):
    """Pre-insert validation against schemas.evidence_state pydantic models."""
    conv_model = None
    if det["convergence"]:
        c = det["convergence"]
        conv_model = ConvergenceAssessment(
            status=ConvergenceStatus(c["status"]),
            clinical_sources=c["clinical"], co1_sources=c["co1"], co2_sources=c["co2"],
            down_weighted_sources=c["downw"], discounted_sources=c["disc"],
            rationale=c["rationale"], synthesis_approach=c["synth"])
    flag = None
    if det["confidence"]:
        flag = ProvisionalConfidenceFlag(
            dimensions_present=det["confidence"]["present"],
            dimensions_absent=det["confidence"]["absent"],
            synthesis_basis=det["confidence"]["basis"])
    EvidenceStateRecord(
        parameter_id=det["parameter_id"],
        **det["lens"],
        design_scale=det["design_scale"],
        state=EvidenceCellState(det["state"]),
        convergence=conv_model, confidence_flag=flag,
        gap_register_id=gap_id,
        not_applicable_rationale=None)
    return True


def q(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def main():
    global SESSION, STAMP
    ap = argparse.ArgumentParser(
        description="Determine one cell: a parameter under one or more lenses.",
        epilog="--db IS WRITTEN, NOT ONLY READ. The engine gathers the cell's evidence "
               "from it and INSERTs the determination -- plus any gap and convergence "
               "row -- straight back into it, committing before it exits. --emit-sql is "
               "a replayable COPY of those same inserts, not the only place they land: "
               "emit_batch_sql.py captures them from the scratch DB, so applying the "
               "artifact AS WELL double-inserts. Two consequences before you run: a --db "
               "that has been run against is no longer pristine, and a re-run for the "
               "same cell is refused by the row-identity index; and comparing two runs "
               "for determinism means two fresh copies, not one DB run twice. The "
               "canonical DB is refused outright.")
    ap.add_argument("--db", required=True,
                    help="scratch DB, READ for the evidence and WRITTEN with the "
                         "determination (NEVER data/guidebook.db)")
    ap.add_argument("--emit-sql", required=True,
                    help="path for the replayable SQL copy of the rows this run also "
                         "commits into --db")
    ap.add_argument("--parameter-id", dest="parameter_id", type=int, required=True,
                    help="base_parameters.parameter_id — THE SUBJECT (owner 2026-08-26)")
    # NO LONGER "the slug to gather from" -- B4c gathers by parameter_id. This is the
    # topic the determination is being RECORDED under: it lands in the report and in
    # the gap description's context, and it is required so a determination cannot be
    # made without saying which piece of work it belongs to.
    ap.add_argument("--slug", required=True,
                    help="the topic this determination is recorded under. It does NOT "
                         "select evidence -- sources are gathered by the extractions "
                         "they hold for --parameter-id.")
    ap.add_argument("--identity", help="populations.population_code")
    ap.add_argument("--icf", help="base_icf.icf_code — a real ICF b/d code")
    ap.add_argument("--needs", help="access_needs.need_code")
    ap.add_argument("--medical", help="base_taxonomy_medical.medical_code")
    ap.add_argument("--note", default="", help="why this cell is being determined")
    ap.add_argument("--session", required=True)
    ap.add_argument("--stamp", required=True,
                    help="fixed timestamp, e.g. '2026-09-09 00:00:00'. An INPUT, never "
                         "now(): the engine run twice must be byte-identical.")
    ap.add_argument("--report-json", default=None)
    args = ap.parse_args()
    if os.path.abspath(args.db) == os.path.abspath(os.path.join(REPO_ROOT, "data", "guidebook.db")):
        sys.exit("REFUSING: this engine never writes the canonical DB (owner-gated).")
    SESSION, STAMP = args.session, args.stamp

    lens = {"identity_code": args.identity, "icf_code": args.icf,
            "needs_code": args.needs, "medical_code": args.medical}

    conn = sqlite3.connect(args.db)
    # FKs OFF is the sqlite3 default, so the engine was writing rows into its scratch DB
    # that the replay would refuse — the scratch state and the report both looked clean
    # and only the migration caught it. An engine whose own run is laxer than the replay
    # tells you the wrong thing at the moment you are deciding whether to replay.
    conn.execute("PRAGMA foreign_keys=ON")
    sql_lines = [
        "-- determination — generated by scripts/assess/assess_cell.py",
        f"-- rule_version {RULE_VERSION}; deterministic (--stamp; explicit ids)",
        "-- Replay onto the canonical DB through emit_data_migration.py -> migrate_db.py,",
        "-- never by hand: the engine computes the state (owner 2026-09-09) but the write",
        "-- path is unchanged.",
        "-- REPLAY CAVEAT: gap ids (GAP-NNN) are assigned from the generating DB's",
        "-- gaps table; REGENERATE this artifact against the canonical DB immediately",
        "-- before replay — a stale copy can collide with gap ids created since.",
        "--",
        "-- NOT WRAPPED. This body carried its own BEGIN;/COMMIT; until 2026-09-09.",
        "-- migrate_db.py STRIPS a file's transaction control rather than nesting it",
        "-- (DR-2026-08-19 §12.0 F5/F6), so the wrapper was never load-bearing — but a",
        "-- body that commits itself mid-run is precisely what F5 exists to prevent,",
        "-- and emit_data_migration.py says bodies are never wrapped. Relying on the",
        "-- stripper to undo something the convention says not to write is one edit",
        "-- away from a body that commits while its data_migrations ledger row rolls",
        "-- back. The engine still commits its own scratch DB: conn.commit(), not this.",
    ]
    report = []
    # Explicit ids from the live high-water mark: reproducible against a given DB, and
    # no autoincrement drift between the emitted SQL and the DB it was generated from.
    base = max(
        conn.execute("SELECT COALESCE(MAX(specification_id), 0) FROM specifications").fetchone()[0],
        conn.execute("SELECT COALESCE(MAX(convergence_id), 0) FROM convergence_assessment").fetchone()[0])
    conv_id = base
    specification_id = base
    for (parameter_id, lens, slug, note) in [(args.parameter_id, lens, args.slug, args.note)]:
        validate_parameter(conn, parameter_id)
        validate_lens(conn, lens)
        # AFTER validate_lens, which normalises blanks to None — the row-identity check
        # restates the index's COALESCE and needs the same lens dict the INSERT will use.
        validate_cell_undetermined(conn, parameter_id, lens)
        det = determine(conn, parameter_id, lens, slug, note)
        gap_id = None
        if det["gap_needed"]:
            gap_id = next_gap_id(conn)
            # THE GAP DESCRIPTION IS DERIVED, and it had to change with the gather.
            # It used to read "no evidence is linked via slug '<slug>' ... This
            # records absence of a slug-link" and point at the item_bpc_links
            # bridge — a sentence about a join this engine no longer makes and a
            # bridge into the emptied item layer. A gap description that names the
            # wrong absence sends the next session looking in the wrong place.
            det_at = det["n_sources"]
            det_x = det["n_extractions"]
            # THREE CAUSES, THREE SENTENCES, and the middle one exists because the
            # first draft of this text was FALSE. `count_extractions` counts every
            # extraction for the parameter; `gather_sources` filters
            # `superseded_by_ref_id IS NULL`. When the only source holding an
            # extraction has been superseded the two disagree, and the text read
            # "N extraction(s) from 0 source(s) ... none of those sources qualified
            # to anchor" — which names the tier gate for a supersession, and sends
            # the next session to re-read a tier ladder when what it needs is the
            # replacement source. A gap description that names the wrong cause is
            # worse than a vague one: it is followed.
            if det_x == 0:
                cause = (f"no source holds an extraction for parameter "
                         f"{parameter_id}: the parameter has never been read out of "
                         f"a document")
                remedy = ("read a source that is already admitted and record what it "
                          "says: `db.py add-extraction`. This is NOT corpus-level "
                          "absence of the topic — sources may be admitted and linked "
                          "to the slug and still have been read for no parameter at "
                          "all, so a new search is not the first move")
            elif det_at == 0 and det["n_finding_sources"]:
                # THE BATCH-08 CASE, AND THE BRANCH BELOW USED TO CLAIM IT WAS A
                # SUPERSESSION. `det_at` counts VALUE-SUPPLYING sources; a parameter
                # read only into `finding` rows has none, so it fell through to the
                # supersession text and told the next session that every source behind
                # it had been replaced. Nothing had been replaced: two studies had
                # measured the effect of the parameter and stated no value for it.
                # This block's own comment says a gap naming the wrong cause is worse
                # than a vague one because it is followed -- this is that, fixed.
                cause = (f"{det_x} extraction(s) exist for parameter {parameter_id} "
                         f"from {det['n_finding_sources']} source(s), but NONE STATES A "
                         f"VALUE: every one is a `finding` (an effect measured) or a "
                         f"`condition`, and a determination needs a threshold to reason "
                         f"against" +
                         (f". {det['n_finding_anchors']} of those source(s) are at an "
                          f"anchoring tier, so this is not weak evidence -- it is "
                          f"evidence of a different KIND"
                          if det["n_finding_anchors"] else ""))
                remedy = ("retrieve the THRESHOLD half: a code value or an equivalent "
                          "criterion of acceptability (owner 2026-09-16 ACTION 3). With "
                          "one present, the findings supply direction and the cell "
                          "reaches a PROXY determination; without one, 'best outcomes' "
                          "is degenerate -- it resolves to the gentlest value physically "
                          "possible, which for a ramp is not a ramp. Do NOT re-read the "
                          "same sources for a value they do not state")
            elif det_at == 0:
                cause = (f"{det_x} extraction(s) exist for parameter {parameter_id}, "
                         f"but EVERY source holding one has been SUPERSEDED "
                         f"(evidence_sources.superseded_by_ref_id is set) and a "
                         f"superseded source is not gathered")
                remedy = ("the reading exists; the document behind it was replaced. "
                          "Re-extract the same parameter from the superseding source")
            else:
                cause = (f"{det_x} extraction(s) from {det_at} source(s) exist for "
                         f"parameter {parameter_id}, but none of those sources "
                         f"qualified to anchor — disqualified, or tier not derivable "
                         f"from their own (evidence_type, scope)")
                remedy = ("the evidence has been read; what is missing is evidence "
                          "that can ANCHOR. Another extraction from the same sources "
                          "will not move this cell — fix the sources' derivable tier, "
                          "or admit evidence that qualifies")
            desc = (f"Evidence gap (parameter-scoped): {cause}. Cell "
                    f"{parameter_id}×{lens_key(lens)}; recorded while working slug "
                    f"'{slug}'. Remedy: {remedy}. Determination pending per §2.4.")
            gcols = ("gap_id, category, priority, status, description, created_at, "
                     "created_by_session, updated_at, updated_by_session")
            gvals = (gap_id, "EG", "P2", "OPEN", desc, STAMP, SESSION, STAMP, SESSION)
            conn.execute(f"INSERT INTO gaps ({gcols}) VALUES (?,?,?,?,?,?,?,?,?)", gvals)
            sql_lines.append(f"INSERT INTO gaps ({gcols}) VALUES (" +
                             ", ".join(q(v) for v in gvals) + ");")

        validate_with_models(det, gap_id)  # pydantic gate BEFORE any insert

        this_conv = None
        if det["convergence"]:
            conv_id += 1
            this_conv = conv_id
            c = det["convergence"]
            vals = (this_conv, c["status"], json.dumps(c["clinical"]), json.dumps(c["co1"]),
                    json.dumps(c["co2"]), json.dumps(c["downw"]), json.dumps(c["disc"]),
                    c["rationale"], c["synth"], STAMP, SESSION)
            conn.execute(
                "INSERT INTO convergence_assessment (convergence_id, status, clinical_sources, "
                "co1_sources, co2_sources, down_weighted_sources, discounted_sources, rationale, "
                "synthesis_approach, created_at, created_by_session) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?)", vals)
            sql_lines.append(
                "INSERT INTO convergence_assessment (convergence_id, status, clinical_sources, "
                "co1_sources, co2_sources, down_weighted_sources, discounted_sources, rationale, "
                "synthesis_approach, created_at, created_by_session) VALUES (" +
                ", ".join(q(v) for v in vals) + ");")

        specification_id += 1
        conf = det["confidence"]
        # regulatory_stratum_only is written HERE for the first time. determine() has
        # computed it since G1 landed and main() dropped it on the floor, so every row
        # the pilot emitted said 0 for a column whose whole purpose is to mark a
        # determination resting entirely on the regulatory stratum. A computed flag
        # that never reaches its column is the same defect as a column nothing reads.
        vals = (specification_id, det["parameter_id"],
                det["lens"]["identity_code"], det["lens"]["icf_code"],
                det["lens"]["needs_code"], det["lens"]["medical_code"],
                det["state"], det["design_scale"],
                this_conv,
                json.dumps(conf["present"]) if conf else None,
                json.dumps(conf["absent"]) if conf else None,
                conf["basis"] if conf else None,
                gap_id, None,
                det["tier_basis"],
                json.dumps(det["governing_refs"]) if det["governing_refs"] else None,
                RULE_VERSION, det["derivation_sha"], det["code_floor_only"],
                # value_min, value_max, value_unit -- literal None here from the 057
                # baseline until 078, which is why the specification stage emitted the
                # marker and never the millimetres.
                det["value_min"], det["value_max"], det["value_unit"],
                det["value_note"],
                # 087. Every notation the governing set states, carrying the selected
                # bound, each marked stated-or-derived and exact-or-not. Owner ruling
                # 2026-09-17: present both, never choose.
                json.dumps(det["value_notations"]) if det["value_notations"] else None,
                det["falsification"],
                det["has_unverified_sources"], det["all_sources_disqualified"],
                det["regulatory_stratum_only"],
                # 086. The third marker of a weakened claim, beside code_floor_only and
                # regulatory_stratum_only: the value was selected under a proxy inference
                # from findings rather than stated by a source (owner 2026-09-16).
                det["rests_on_proxy_inference"],
                # 080. `derivation_paths` carries a CHECK that a single-path row owes
                # either a rationale or a cultural anchor, so these four are written
                # together or the database refuses the row -- which is the dignity line
                # ceasing to be "doctrine binding on authors" and becoming a state the
                # schema will not hold.
                det["functional_basis"], det["derivation_paths"],
                det["derivation_rationale"], det["cultural_claim_anchor"],
                STAMP, SESSION, STAMP, SESSION)
        cols = ("specification_id, parameter_id, "
                "identity_code, icf_code, needs_code, medical_code, "
                "state, design_scale, convergence_id, "
                "confidence_dimensions_present, confidence_dimensions_absent, "
                "confidence_synthesis_basis, gap_register_id, not_applicable_rationale, "
                "tier_basis, governing_refs, rule_version, derivation_sha, code_floor_only, "
                "value_min, value_max, value_unit, value_note, value_notations, "
                "falsification_condition, "
                "has_unverified_sources, all_sources_disqualified, regulatory_stratum_only, "
                "rests_on_proxy_inference, "
                "functional_basis, derivation_paths, derivation_rationale, "
                "cultural_claim_anchor, "
                "created_at, created_by_session, updated_at, updated_by_session")
        conn.execute(f"INSERT INTO specifications ({cols}) VALUES ("
                     + ",".join("?" * len(vals)) + ")", vals)
        sql_lines.append(f"INSERT INTO specifications ({cols}) VALUES (" +
                         ", ".join(q(v) for v in vals) + ");")

        # THE JUNCTION, not just the JSON. The engine wrote only
        # specifications.governing_refs until 2026-09-10, and test_db_integrity H02 —
        # BLOCKING — asserts "every JSON entry is in the junction". Reproduced before
        # fixing: one engine row, 5 governing_refs entries, 0 specification_source_links
        # rows, H02 red. A determination engine that cannot produce a state its own
        # checker accepts is the failure CLAUDE.md names, and it was reintroduced here.
        #
        # RULE 5 TENSION, recorded rather than hidden: the JSON and the junction are two
        # homes for one fact, and the comment directly under H01/H02 in
        # test_db_integrity.py says H03/H04 were DELETED because "a parity check between
        # two homes of one fact does not prevent drift; it makes the second home
        # survivable, and therefore permanent." H01/H02 is that shape and it is live and
        # blocking, so the engine satisfies it. The retirement owed is the JSON's: the
        # junction is the pointer, `governing_refs` is the copy — but the copy is what
        # derivation_sha hashes (and K01 recomputes), so dropping it re-keys the
        # attestation. That is a sweep, not this change.
        for _ref in det["governing_refs"]:
            _link = (specification_id, _ref, "governing", STAMP, SESSION)
            _lcols = ("specification_id, ref_id, role, created_at, created_by_session")
            conn.execute(f"INSERT INTO specification_source_links ({_lcols}) "
                         f"VALUES (?,?,?,?,?)", _link)
            sql_lines.append(f"INSERT INTO specification_source_links ({_lcols}) VALUES (" +
                             ", ".join(q(v) for v in _link) + ");")

        # THE PROVENANCE JUNCTION (migration 077). Not a parallel copy of the one above:
        # that one records which SOURCES anchored, this one records which ROWS did, and
        # a source carries many rows that played different parts. It is also what
        # `derivation_sha` now hashes, so writing it is not optional bookkeeping -- the
        # attestation is unverifiable without it, and K01 recomputes the payload from
        # exactly these rows.
        _xcols = ("specification_id, extraction_id, role, exclusion_reason, "
                  "created_at, created_by_session")
        for _l in det["links"]:
            _xlink = (specification_id, _l["extraction_id"], _l["role"],
                      _l["exclusion_reason"], STAMP, SESSION)
            conn.execute(f"INSERT INTO specification_extraction_links ({_xcols}) "
                         f"VALUES (?,?,?,?,?,?)", _xlink)
            sql_lines.append(f"INSERT INTO specification_extraction_links ({_xcols}) "
                             f"VALUES (" + ", ".join(q(v) for v in _xlink) + ");")

        report.append({k: det[k] for k in
                       ("value_min", "value_max", "value_unit", "value_note",
                        "value_notations", "accessibility_direction",
                        "parameter_id", "lens", "lens_key", "slug", "note", "state", "design_scale",
                        "tier_basis", "governing_refs", "supporting_refs", "code_floor_only",
                        "regulatory_stratum_only", "rests_on_proxy_inference",
                        "has_unverified_sources",
                        "all_sources_disqualified", "derivation_sha", "n_sources",
                        "n_extractions", "non_anchoring_on_tier",
                        "needs_population_assessment", "tier_inconsistent", "falsification")}
                      | {"convergence": det["convergence"], "confidence": det["confidence"],
                         "gap_register_id": gap_id, "specification_id": specification_id,
                         "convergence_id": this_conv,
                         "source_records": [{k2: r[k2] for k2 in
                                             ("ref_id", "tier", "evidence_type", "grain",
                                              "grain_why", "scale_directness",
                                              "population_directness", "conditioning",
                                              "conditioning_before_tier_gate",
                                              "tier_consistent")}
                                            for r in det["source_records"]]})

    # REMOVED 2026-08-22 (BRK-26). An interim v_best_practice amendment used to sit
    # here: it DROPped and re-CREATEd the view mid-determination and shipped that DDL
    # inside the emitted replayable SQL, so the redefinition travelled into whatever
    # migration carried the rows. Its own comment said it held "until migration 027
    # adds a real regulatory_stratum_only column".
    #
    # That column exists. Migration 027 landed it, and migration 029 then went
    # further, under RATIFIED DR-2026-07-21-product-posture-thinking-tool-not-authority:
    # a determination whose entire evidence basis is the regulatory stratum IS a
    # best-practice determination at the WEAK band — surfaced, flagged with
    # strength_band, never suppressed. 029 deliberately DROPPED the two 027 guards
    # this block reproduced.
    #
    # So replaying this DDL would not have "restored a guard". It would have reverted
    # ratified doctrine: dropping the strength_band column and re-imposing an
    # exclusion the owner's own decision removed — and doing it by a fragile
    # `tier_basis LIKE '%(regulatory_stratum_only)'` string match rather than the
    # column test that now exists. Standing proof it travels:
    # working/pilot/data_20260712_pilot-cell-backfill.sql:23-24 still carries it.
    #
    # A determination engine has no business rewriting the schema it writes into.
    # The view is defined by migration and belongs to the migration layer.
    conn.commit()
    with open(args.emit_sql, "w") as f:
        f.write("\n".join(sql_lines) + "\n")
    if args.report_json:
        with open(args.report_json, "w") as f:
            json.dump(report, f, indent=1)

    for r in report:
        # `sources=` and `extractions=` are printed because the 1:N fan-out is
        # invisible otherwise: 2 sources / 9 extractions and 9 sources / 9
        # extractions are very different evidence bases and the old line showed
        # neither. `nonanchor=` names how many were excluded by the tier gate, so a
        # thin `stated` cannot look thick.
        print(f"param {r['parameter_id']}×{r['lens_key']:<8} {r['state']:<12} "
              f"basis={r['tier_basis'] or '-':<32} scale={r['design_scale']:<10} "
              f"refs={len(r['governing_refs'])} sources={r['n_sources']} "
              f"extractions={r['n_extractions']} "
              f"nonanchor={len(r['non_anchoring_on_tier'])} "
              f"rso={r['regulatory_stratum_only']} "
              f"cfo={r['code_floor_only']} sha={r['derivation_sha'][:12]}")
    print(f"\n{len(report)} cell(s) determined; SQL artifact: {args.emit_sql}\n"
          f"COMMITTED into {args.db} — those rows are in that scratch DB now, and\n"
          f"emit_batch_sql.py captures them from there. Applying the artifact AS WELL\n"
          f"double-inserts. Re-running this cell against this DB is refused.\n"
          f"REPLAY through emit_data_migration.py -> migrate_db.py, never by hand.")
    if ENUM_DRIFT:
        print(f"DRIFT FINDING: populations valid in live table but missing from "
              f"schemas.enums.PopulationCode: {sorted(set(ENUM_DRIFT))} — "
              f"recorded for the ratification package (reconciliation item).")


if __name__ == "__main__":
    # REFUSALS ARE MESSAGES, NOT STACK TRACES. The canonical-DB guard has exited cleanly
    # via sys.exit since this file was written, and every other refusal here — a merged
    # parameter, a lens code that is not live, a cell already determined — arrived as a
    # traceback with the sentence at the bottom. These messages cite the ruling and name
    # the next move; a stack trace above them buries the part the operator needs. Same
    # refusals, same non-zero exit, no stack. Refusal only: anything else keeps its
    # traceback, because anything else is a defect and its location is the evidence.
    try:
        main()
    except Refusal as exc:
        sys.exit(f"REFUSING: {exc}")
    except sqlite3.IntegrityError as exc:
        # Belt and braces on the one constraint an operator meets by ordinary use.
        # validate_cell_undetermined() restates this index's own COALESCE expression,
        # so reaching here means the two have drifted — which is worth saying plainly
        # rather than as a bare constraint name.
        if "idx_spec_row_identity" in str(exc):
            sys.exit("REFUSING: this cell is already determined — "
                     "`idx_spec_row_identity` refused a second row for the same "
                     "parameter × lens, at the INSERT rather than at the "
                     "pre-flight check that should have caught it "
                     "(validate_cell_undetermined). There is no re-determination path; "
                     "revisiting a determined cell needs a supersede design first.")
        raise
