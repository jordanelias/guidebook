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

Implements the pure determination function of workplan/best-practices-assessment-system.md
§3 under the doctrine of governance/evidence-architecture.md, with the G1/G2/G3/G6
fixes active ADDITIVELY — no existing schema function is modified; every deviation from
the schemas/directness.py defaults is engine-side and tagged rule_version="pilot-2".
G2, G3 and G6 are RATIFIED (RATIFICATION-PACKAGE-2026-07-12, owner directive
2026-07-13) and implemented ONLY here; schemas/directness.py still maps co1 → specific
and standard_eb → code unconditionally. Promoting them into the shared model is
register item Q4, and it is now urgent: two implementations of one ratified rule that
disagree is a live inconsistency, not a dormant one.

Determinism: same evidence + same rule_version ⇒ same state + same derivation_sha.
Timestamps come from --stamp, not wall-clock reads, so a re-run is byte-identical and
the double-run determinism check (evidence-architecture.md §10, check 2) is meaningful.

Module roster (PILOT-MANIFEST.md §4 — no silent omissions):
  schemas.directness          grain-matching, scale-directness, consolidation
  schemas.tier_derivation     tier/evidence_type/scope consistency audit per source
  schemas.evidence_state      EvidenceStateRecord / ConvergenceAssessment /
                              ProvisionalConfidenceFlag — every row validated
                              against the pydantic model BEFORE insert
  schemas.enums               PopulationCode / EvidenceCellState / ConvergenceStatus /
                              Co1SourceType / VerificationStatus vocabularies
  schemas.evidence_source     (via enums + verification gates below)
  schemas.source_value_extraction  value substrate (table empty — value dimension
                              recorded NOT_ASSESSED, never silently EXACT; G2)
  schemas.population, schemas.population_links, schemas.slug, schemas.bpc_metadata,
  schemas.gap                 identity/attribution semantics (lens codes validated
                              against their own live base tables)

G-fixes (evidence-architecture.md §4, DR-2026-07-12-evidence-architecture-unification):
  G1  T4–6-only basis ⇒ regulatory-stratum determination: design_scale='universal',
      never 'stated', code_floor_only=1 iff T6-only; T4/T5 keep GRAIN_CODE (no pilot
      source has documented T1/T2 traceability, so no re-graining is claimed).
  G2  A directness dimension that APPLIES but has never been assessed is NOT_ASSESSED,
      not None ("not applicable"): it caps consolidation at DOWN-WEIGHTED via
      consolidate()'s existing partial-dimension path, and the source is flagged.
  G3  Co-1 grain follows co1_source_type (dpo_research/advocacy_position → aggregate;
      academic_narrative → specific; others → specific, noted).
  G6  standard_eb grain follows (type × tier): T2 → aggregate; T4/T5 → code.
"""
import argparse
import hashlib
import json
import os
import sqlite3
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)

from schemas.directness import (  # noqa: E402
    GRAIN_AGGREGATE, GRAIN_CODE, GRAIN_SPECIFIC, GRAIN_FROM_EVIDENCE_TYPE,
    SCALE_POPULATION, SCALE_UNIVERSAL,
    SD_NON_ANCHORING,
    COND_DIRECT, COND_DOWN_WEIGHTED, COND_DISCOUNTED, COND_NON_ANCHORING,
    consolidate, population_directness_from_match_grade, scale_directness,
)
from schemas.tier_derivation import check_tier_consistency  # noqa: E402
from schemas.enums import (  # noqa: E402
    Co1SourceType, ConvergenceStatus, EvidenceCellState, PopulationCode,
    VerificationStatus,
)
from schemas.evidence_state import (  # noqa: E402
    ConvergenceAssessment, EvidenceStateRecord, ProvisionalConfidenceFlag,
)

RULE_VERSION = "pilot-2"  # pilot-1 + adversarial-review corrections (see PILOT-MANIFEST §7):
#   tier_basis now describes the GOVERNING set only (supporting strata listed separately);
#   derivation_sha includes cell identity (pending cells no longer share one constant sha);
#   has_unverified_sources / all_sources_disqualified implemented per §2.8;
#   population-match rows attributed to the cell's population or treated NOT_ASSESSED;
#   §2.3 richness checks T6 jurisdiction distinctness and names its unchecked clause;
#   gap descriptions are slug-scoped (absence of a slug-link is not corpus-level absence);
#   ~~the SQL artifact amends v_best_practice to exclude regulatory-stratum-only rows
#   (interim, marker-based; migration 027 adds the real column).~~ WITHDRAWN
#   2026-08-22 (BRK-26): the column exists and migration 029 superseded the
#   exclusion under ratified DR-2026-07-21. See the note at the emit site.
# Run-supplied, not wall-clock: --session and --stamp. Determinism is the point
# (evidence-architecture.md §10 check 2: the engine run twice must produce a
# byte-identical derivation_sha), so the stamp is an INPUT, never `now()`.
SESSION = None
STAMP = None

# G2: engine-side grade for "dimension applies but was never assessed".
# Deliberately NOT added to schemas.directness vocab pre-ratification (additive rule).
# Passing it to consolidate() makes pop_full/val_full False -> caps at DOWN-WEIGHTED,
# which is exactly the G2 semantics, without touching consolidate() itself.
NOT_ASSESSED = "NOT_ASSESSED"

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
    "icf_code": ("axes", "axis_code"),
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


def source_grain(evidence_type, tier, co1_source_type):
    """G3 + G6: grain from (type × tier × co1_source_type); default map otherwise."""
    if evidence_type == "co1":  # G3
        if co1_source_type in (Co1SourceType.DPO_RESEARCH.value if hasattr(Co1SourceType, "DPO_RESEARCH") else "dpo_research",
                               "dpo_research", "advocacy_position"):
            return GRAIN_AGGREGATE, "G3:population-grain co1"
        return GRAIN_SPECIFIC, "G3:individual-grain co1"
    if evidence_type == "standard_eb":  # G6
        if tier == 2:
            return GRAIN_AGGREGATE, "G6:standard_eb@T2=synthesis-tier"
        return GRAIN_CODE, "G6:standard_eb@T4/5=regulatory (no re-graining claimed: G1)"
    return GRAIN_FROM_EVIDENCE_TYPE.get(evidence_type, GRAIN_SPECIFIC), "default map"


def gather_sources(conn, slug):
    # verification_disposition arrived with migration 049 (D-0157). This script
    # is run against scratch and fixture databases as well as the canonical one
    # -- it refuses the canonical DB by design -- so the column is selected only
    # when it exists. A pre-049 database still disqualifies correctly through
    # the legacy status values in DISQUALIFIED.
    has_disp = any(r[1] == "verification_disposition"
                   for r in conn.execute("PRAGMA table_info(evidence_sources)"))
    disp_col = "e.verification_disposition" if has_disp else "NULL"
    q = f"""SELECT e.ref_id, e.tier, e.evidence_type, e.co1_source_type,
                   e.verification_status, {disp_col}, e.scope, e.jurisdiction
            FROM source_slug_links l JOIN evidence_sources e ON e.ref_id = l.ref_id
            WHERE l.slug = ? AND e.superseded_by_ref_id IS NULL
            ORDER BY e.ref_id"""
    return [dict(zip(("ref_id", "tier", "evidence_type", "co1_source_type",
                      "verification_status", "verification_disposition",
                      "scope", "jurisdiction"), r))
            for r in conn.execute(q, (slug,))]


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
    grain, grain_why = source_grain(src["evidence_type"], src["tier"], src["co1_source_type"])
    sd = scale_directness(grain, claim_scale)
    mg = population_match(conn, src["ref_id"], population)
    if mg is not None:
        pop = population_directness_from_match_grade(mg)
    else:
        pop = NOT_ASSESSED  # G2: applies but unassessed — never graded as EXACT
    # value dimension: still NOT_ASSESSED, but the reason has changed and the
    # old one was that source_value_extractions "is EMPTY (0 rows)". It holds 8
    # rows as of migration 052 and, since that migration, an item_code to join
    # them on. What is still absent is any assessment RULE for grading a value
    # dimension from them — writing one is a judgment act, not a caller sweep.
    # G2 stands: applies but unassessed, never silently full-match.
    val = NOT_ASSESSED
    cond = consolidate(pop, val, sd)
    tier_ok = check_tier_consistency(src["evidence_type"], src["scope"], src["tier"])
    return {
        "ref_id": src["ref_id"], "tier": src["tier"], "evidence_type": src["evidence_type"],
        "grain": grain, "grain_why": grain_why, "scale_directness": sd,
        "population_directness": pop, "value_directness": val, "conditioning": cond,
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


def regulatory_richness(t45, t6):
    """§2.3 richness for a T4–6-only provisional (else pending).

    Honestly-partial implementation, named as such in the rationale it emits:
    §2.3's T4 clause requires "an evidence-based value directly addressing the
    parameter" — the T4 branch checks presence only and SAYS SO. (This used to
    read "not mechanically checkable while source_value_extractions is empty";
    the table now has 8 rows and, per migration 052, an item_code to address the
    parameter with. The branch is unchanged because deciding what counts as
    "directly addressing" is a judgment call, not a missing join.) The T6 clause
    requires convergence "on the same value or range" — likewise unverifiable;
    jurisdiction distinctness IS checkable and is enforced."""
    jur45 = {r.get("jurisdiction") for r in t45}
    if len([r for r in t45 if r["tier"] == 4]) >= 1:
        return True, (">=1 T4 international standard present (§2.3; the clause's "
                      "'value directly addressing the parameter' is unverified — "
                      "value extraction pending)")
    if len(t45) >= 2 and len(jur45) >= 2:
        return True, ">=2 T4-5 sources, distinct jurisdictions (§2.3)"
    jur6 = {r.get("jurisdiction") for r in t6}
    if len(t6) >= 3 and len(jur6) >= 3:
        return True, (f">=3 T6 codes from {len(jur6)} distinct jurisdictions (§2.3; "
                      "value-level convergence unverified — extraction pending)")
    return False, "below §2.3 richness"


def sha(parameter_id, lens, refs):
    """Cell-scoped derivation sha: identity + governing set + rule version, so
    pending cells do not all share one constant hash (staleness stays checkable).

    The payload is byte-for-byte what test_db_integrity K01 recomputes when it verifies
    a stored sha, and K01 was re-keyed to (parameter_id × lens) by migration 071. Two
    implementations of one hash that disagree is a hash that attests nothing, so this
    one and K01's move together or not at all. `lens` is the COALESCE value, not the
    whole dict — see lens_key().
    """
    payload = f"{parameter_id}|{lens}|" + "|".join(sorted(refs)) + "::" + RULE_VERSION
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
    sources = gather_sources(conn, slug)
    recs = [assess_source(conn, s, SCALE_POPULATION, identity) for s in sources]
    b = classify(recs)
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
        rich, why = regulatory_richness(b["t45"], b["t6"])
        design_scale = SCALE_UNIVERSAL
        regulatory_stratum_only = 1
        code_floor_only = 1 if (b["t6"] and not b["t45"]) else 0
        if rich:
            state = "provisional"
            governing = sorted(r["ref_id"] for r in regulatory)
            tier_basis = ("T6-only" if code_floor_only else
                          ("T4-6-only" if b["t6"] else "T4-5-only")) + "(regulatory_stratum_only)"
            conv = dict(status="single_axis", clinical=[], co1=[], co2=[],
                        downw=[], disc=discounted,
                        rationale="regulatory stratum only (T4-6): convergence-not-evidence "
                                  "(tier-system.md §3). Universal-Mode regulatory determination; "
                                  "richness: " + why,
                        synth=None)
            conf = dict(present=[f"Tier 4-5 standards ({len(b['t45'])})",
                                 f"Tier 6 statutory codes ({len(b['t6'])})"],
                        absent=["No Tier 1 clinical", "No Co-1", "No Tier 2 synthesis",
                                "No Co-2 CPG", "No Tier 3 clinical"],
                        basis="Regulatory-stratum floor synthesis (" + why + "). NOT an "
                              "evidence-anchored best practice: no anchoring dimension exists.")
            falsification = ("This is a floor claim: overturned if the cited editions are "
                             "superseded. It never becomes a best-practice claim by more codes "
                             "agreeing; only T1/Co-1/T2/Co-2 evidence can do that (§2.7).")
        else:
            state = "pending"
            gap_needed = True
    elif b["t3g"]:
        # tier3-threshold DR item 2: T3-grey-alone does not even reach provisional
        state = "pending"
        gap_needed = True
    else:
        state = "pending"
        gap_needed = True

    return {
        "parameter_id": parameter_id, "lens": dict(lens), "lens_key": lens_key(lens),
        "slug": slug, "note": note,
        "state": state, "design_scale": design_scale, "tier_basis": tier_basis,
        "governing_refs": governing, "supporting_refs": supporting,
        "convergence": conv, "confidence": conf,
        "gap_needed": gap_needed, "code_floor_only": code_floor_only,
        "regulatory_stratum_only": regulatory_stratum_only,
        "has_unverified_sources": 1 if has_unverified else 0,
        "all_sources_disqualified": 1 if all_disqualified else 0,
        "falsification": falsification,
        "derivation_sha": sha(parameter_id, lens_key(lens), governing),
        "n_sources": len(sources),
        "needs_population_assessment": sorted(r["ref_id"] for r in recs
                                              if r["needs_population_assessment"]),
        "tier_inconsistent": sorted(r["ref_id"] for r in recs if not r["tier_consistent"]),
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
        raise ValueError(
            f"parameter_id {parameter_id}: no such parameter. Mint one from a term:\n"
            f"  db.py add-parameter --term-id TERM-NNN --session ...")
    status, merged_into = row[0], row[1]
    if status != "active":
        target = f" (merged into {merged_into})" if merged_into else ""
        raise ValueError(
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
        raise ValueError(
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
            raise ValueError(f"{col} {code!r} is not a live {key} in {table}")
    identity = lens.get("identity_code")
    if identity:
        try:
            PopulationCode(identity)
        except ValueError:
            ENUM_DRIFT.append(identity)


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
        description="Determine one cell: a parameter under one or more lenses.")
    ap.add_argument("--db", required=True, help="scratch DB (NEVER data/guidebook.db)")
    ap.add_argument("--emit-sql", required=True)
    ap.add_argument("--parameter-id", dest="parameter_id", type=int, required=True,
                    help="base_parameters.parameter_id — THE SUBJECT (owner 2026-08-26)")
    ap.add_argument("--slug", required=True, help="the evidence slug to gather from")
    ap.add_argument("--identity", help="populations.population_code")
    ap.add_argument("--icf", help="axes.axis_code")
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
        det = determine(conn, parameter_id, lens, slug, note)
        gap_id = None
        if det["gap_needed"]:
            gap_id = next_gap_id(conn)
            desc = (f"Evidence gap (slug-scoped): no evidence is linked via slug '{slug}' "
                    f"for cell parameter {parameter_id}×{lens_key(lens)}, and no linked "
                    f"evidence met the "
                    f"determination thresholds. This records absence of a slug-link, NOT "
                    f"corpus-level absence: item-relevant evidence may exist under sibling "
                    f"slugs and is unreachable until the item_bpc_links bridge (1/92 "
                    f"populated) is backfilled. Determination pending per §2.4.")
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
                None, None, None,
                det["falsification"],
                det["has_unverified_sources"], det["all_sources_disqualified"],
                det["regulatory_stratum_only"],
                STAMP, SESSION, STAMP, SESSION)
        cols = ("specification_id, parameter_id, "
                "identity_code, icf_code, needs_code, medical_code, "
                "state, design_scale, convergence_id, "
                "confidence_dimensions_present, confidence_dimensions_absent, "
                "confidence_synthesis_basis, gap_register_id, not_applicable_rationale, "
                "tier_basis, governing_refs, rule_version, derivation_sha, code_floor_only, "
                "value_min, value_max, value_unit, falsification_condition, "
                "has_unverified_sources, all_sources_disqualified, regulatory_stratum_only, "
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

        report.append({k: det[k] for k in
                       ("parameter_id", "lens", "lens_key", "slug", "note", "state", "design_scale",
                        "tier_basis", "governing_refs", "supporting_refs", "code_floor_only",
                        "regulatory_stratum_only", "has_unverified_sources",
                        "all_sources_disqualified", "derivation_sha", "n_sources",
                        "needs_population_assessment", "tier_inconsistent", "falsification")}
                      | {"convergence": det["convergence"], "confidence": det["confidence"],
                         "gap_register_id": gap_id, "specification_id": specification_id,
                         "convergence_id": this_conv,
                         "source_records": [{k2: r[k2] for k2 in
                                             ("ref_id", "tier", "evidence_type", "grain",
                                              "grain_why", "scale_directness",
                                              "population_directness", "conditioning")}
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
        print(f"param {r['parameter_id']}×{r['lens_key']:<8} {r['state']:<12} "
              f"basis={r['tier_basis'] or '-':<32} scale={r['design_scale']:<10} "
              f"refs={len(r['governing_refs'])} rso={r['regulatory_stratum_only']} "
              f"cfo={r['code_floor_only']} sha={r['derivation_sha'][:12]}")
    print(f"\n{len(report)} cell(s) determined; SQL artifact: {args.emit_sql}\n"
          f"REPLAY through emit_data_migration.py -> migrate_db.py, never by hand.")
    if ENUM_DRIFT:
        print(f"DRIFT FINDING: populations valid in live table but missing from "
              f"schemas.enums.PopulationCode: {sorted(set(ENUM_DRIFT))} — "
              f"recorded for the ratification package (reconciliation item).")


if __name__ == "__main__":
    main()
