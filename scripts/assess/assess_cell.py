#!/usr/bin/env python3
"""
scripts/assess/assess_cell.py — pilot determination engine (rule_version "pilot-1").

Implements the pure determination function of workplan/best-practices-assessment-system.md
§3 for the pilot cells in working/pilot/PILOT-MANIFEST.md §3, under the doctrine of
governance/evidence-architecture.md (PROPOSED) with the G1/G2/G3/G6 fixes active
ADDITIVELY — no existing schema function is modified; every deviation from the
schemas/directness.py defaults is engine-side and tagged rule_version="pilot-1",
so no PROPOSED doctrine changes live behavior before owner ratification.

Determinism: same evidence + same rule_version ⇒ same state + same derivation_sha.
Timestamps are fixed strings (this run's date), not wall-clock reads, so a re-run is
byte-identical and the double-run determinism check is meaningful.

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
  schemas.gap                 identity/attribution semantics (codes validated against
                              live tables + PopulationCode enum)

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

RULE_VERSION = "pilot-1"
SESSION = "session_2026-07-12-evidence-architecture-pilot"
STAMP = "2026-07-12 00:00:00"  # fixed, not wall-clock: determinism (see docstring)

# G2: engine-side grade for "dimension applies but was never assessed".
# Deliberately NOT added to schemas.directness vocab pre-ratification (additive rule).
# Passing it to consolidate() makes pop_full/val_full False -> caps at DOWN-WEIGHTED,
# which is exactly the G2 semantics, without touching consolidate() itself.
NOT_ASSESSED = "NOT_ASSESSED"

# Verification gates (evidence-methodology.md §2.2 cond. 2 / §2.8)
VERIFIED_OK = {VerificationStatus.VERIFIED.value, VerificationStatus.VERIFIED_WITH_CORRECTION.value} \
    if hasattr(VerificationStatus, "VERIFIED") else {"VERIFIED", "VERIFIED-WITH-CORRECTION"}
DISQUALIFIED = {"UNVERIFIED-CLOSED", "CLOSED-DELETED"}

# Pilot cells — PILOT-MANIFEST.md §3 (manual slug→item mapping recorded there)
PILOT_CELLS = [
    ("E-08", "DEAF", "deaf-spatial-design",
     "Co-1-anchored corridor width; canonical tier-system.md §3 case"),
    ("E-12", "MOB", "mobility-built-environment",
     "full-mix; convergence assessed from real data"),
    ("G-03", "MOB", "ot-cpg-built-environment",
     "Co-2 + T2 anchoring (§2.2 cond. 3)"),
    ("C-02", "DEM", "wayfinding-cognitive-science-spatial-design",
     "T3-alone; exercises DR-2026-07-12-tier3-stated-threshold"),
    ("E-06", "MOB", "threshold-and-level-access",
     "T4-6 only; decisive G1 regulatory-stratum test"),
    ("G-03", "SCI", "fold-down-grab-bar-specification",
     "zero evidence; pending + gap"),
    ("B-10", "NEU", "visual-fire-alarm-seizure-safety",
     "mixed with one T2 anchor lifting cell out of regulatory stratum"),
]

CELL_ID_BASE = 9000  # explicit ids: reproducible artifact, no autoincrement drift


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
    q = """SELECT e.ref_id, e.tier, e.evidence_type, e.co1_source_type,
                  e.verification_status, e.scope, e.jurisdiction
           FROM source_slug_links l JOIN evidence_sources e ON e.ref_id = l.ref_id
           WHERE l.slug = ? AND e.superseded_by_ref_id IS NULL
           ORDER BY e.ref_id"""
    return [dict(zip(("ref_id", "tier", "evidence_type", "co1_source_type",
                      "verification_status", "scope", "jurisdiction"), r))
            for r in conn.execute(q, (slug,))]


def population_match(conn, ref_id):
    row = conn.execute(
        "SELECT match_grade FROM evidence_population_match WHERE ref_id = ?",
        (ref_id,)).fetchone()
    return row[0] if row else None


def assess_source(conn, src, claim_scale):
    """Per-source directness record under pilot-1 (G2/G3/G6 active)."""
    grain, grain_why = source_grain(src["evidence_type"], src["tier"], src["co1_source_type"])
    sd = scale_directness(grain, claim_scale)
    mg = population_match(conn, src["ref_id"])
    if mg is not None:
        pop = population_directness_from_match_grade(mg)
    else:
        pop = NOT_ASSESSED  # G2: applies but unassessed — never graded as EXACT
    # value dimension: home substrate source_value_extractions is EMPTY (0 rows) —
    # G2 again: applies but unassessed, never silently full-match.
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
    }


def classify(recs):
    """Bucket assessed sources into doctrinal strata (disqualified sources excluded)."""
    live = [r for r in recs if (r["verification_status"] or "") not in DISQUALIFIED]
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
    """§2.3 richness for a T4–6-only provisional (else pending)."""
    jur45 = {r.get("jurisdiction") for r in t45}
    if len([r for r in t45 if r["tier"] == 4]) >= 1:
        return True, ">=1 T4 international standard (§2.3)"
    if len(t45) >= 2 and len(jur45) >= 2:
        return True, ">=2 T4-5 sources, distinct jurisdictions (§2.3)"
    if len(t6) >= 3:
        return True, ">=3 T6 codes (§2.3)"
    return False, "below §2.3 richness"


def sha(refs):
    return hashlib.sha256(("|".join(sorted(refs)) + "::" + RULE_VERSION).encode()).hexdigest()


def determine(conn, item_code, population, slug, note):
    """The pure determination function. Returns (record dicts for insert, log)."""
    sources = gather_sources(conn, slug)
    recs = [assess_source(conn, s, SCALE_POPULATION) for s in sources]
    b = classify(recs)
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

    if anchors:
        state = "stated"
        governing = sorted(r["ref_id"] for r in anchors)
        parts = [p for p, k in (("T1", b["t1"]), ("CO1", b["co1"]), ("T2", b["t2"]),
                                ("CO2", b["co2"]), ("T3", t3c)) if anchoring(k)]
        tier_basis = "+".join(parts)
        if n_axes >= 2:
            # Axis co-presence is real; value-level convergence is NOT assessable
            # (source_value_extractions empty). pending_assessment is the honest
            # status — never claim 'convergent' on unextracted values (G2 spirit).
            conv_status = "pending_assessment"
            rationale = (f"{n_axes} evidence axes present (clinical/co1/co2). Value-level "
                         f"convergence not yet assessable: source_value_extractions has no "
                         f"rows for these sources; assessment queued, not assumed.")
        else:
            conv_status = "single_axis"
            axis = "clinical" if axes_clinical else ("co1" if axes_co1 else "co2")
            rationale = f"single evidence axis: {axis}"
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
        "item_code": item_code, "population": population, "slug": slug, "note": note,
        "state": state, "design_scale": design_scale, "tier_basis": tier_basis,
        "governing_refs": governing, "convergence": conv, "confidence": conf,
        "gap_needed": gap_needed, "code_floor_only": code_floor_only,
        "regulatory_stratum_only": regulatory_stratum_only,
        "falsification": falsification,
        "derivation_sha": sha(governing),
        "n_sources": len(sources),
        "needs_population_assessment": sorted(r["ref_id"] for r in recs
                                              if r["needs_population_assessment"]),
        "tier_inconsistent": sorted(r["ref_id"] for r in recs if not r["tier_consistent"]),
        "source_records": recs,
    }


def next_gap_id(conn):
    rows = [r[0] for r in conn.execute("SELECT gap_id FROM gaps WHERE gap_id LIKE 'GAP-%'")]
    mx = max((int(g.split("-")[1]) for g in rows if g.split("-")[1].isdigit()), default=0)
    return f"GAP-{mx + 1}"


ENUM_DRIFT = []  # populations valid in the live table but missing from PopulationCode


def validate_population(conn, code):
    """Cell identity truth is the live populations table (DR-2026-07-12 schema
    reconciliation keys cells on population_code REFERENCES populations).
    schemas.enums.PopulationCode is ALSO checked; a code present in the table but
    absent from the enum is recorded as a drift finding (pilot discovery:
    the enum's 25 values do not match the table's 22 codes), never silently passed."""
    row = conn.execute("SELECT 1 FROM populations WHERE population_code=?", (code,)).fetchone()
    if not row:
        raise ValueError(f"population {code!r} not in populations table")
    try:
        PopulationCode(code)
    except ValueError:
        ENUM_DRIFT.append(code)


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
        item_code=det["item_code"],
        population=det["population"],
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, help="pilot DB (NEVER the canonical data/guidebook.db)")
    ap.add_argument("--emit-sql", required=True)
    ap.add_argument("--report-json", default=None)
    args = ap.parse_args()
    if os.path.abspath(args.db) == os.path.abspath(os.path.join(REPO_ROOT, "data", "guidebook.db")):
        sys.exit("REFUSING: this engine never writes the canonical DB (owner-gated).")

    conn = sqlite3.connect(args.db)
    sql_lines = [
        "-- working/pilot pilot-cell backfill — generated by scripts/assess/assess_cell.py",
        f"-- rule_version {RULE_VERSION}; deterministic (fixed STAMP; explicit ids)",
        "-- Replayable onto the canonical DB ONLY after owner ratification",
        "-- (DR-2026-07-12-evidence-architecture-unification + ratification package).",
        "BEGIN;",
    ]
    report = []
    conv_id = CELL_ID_BASE
    cell_id = CELL_ID_BASE
    for item_code, population, slug, note in PILOT_CELLS:
        validate_population(conn, population)
        det = determine(conn, item_code, population, slug, note)
        gap_id = None
        if det["gap_needed"]:
            gap_id = next_gap_id(conn)
            desc = (f"Evidence gap: no admissible evidence for cell {item_code}×{population} "
                    f"(slug {slug}). Determination pending per §2.4; search history: "
                    f"source_slug_links empty or below richness for this slug.")
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

        cell_id += 1
        conf = det["confidence"]
        vals = (cell_id, det["item_code"], det["population"], det["state"], det["design_scale"],
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
                STAMP, SESSION, STAMP, SESSION)
        cols = ("cell_id, item_code, population_code, state, design_scale, convergence_id, "
                "confidence_dimensions_present, confidence_dimensions_absent, "
                "confidence_synthesis_basis, gap_register_id, not_applicable_rationale, "
                "tier_basis, governing_refs, rule_version, derivation_sha, code_floor_only, "
                "value_min, value_max, value_unit, falsification_condition, "
                "created_at, created_by_session, updated_at, updated_by_session")
        conn.execute(f"INSERT INTO evidence_cell_state ({cols}) VALUES ("
                     + ",".join("?" * 24) + ")", vals)
        sql_lines.append(f"INSERT INTO evidence_cell_state ({cols}) VALUES (" +
                         ", ".join(q(v) for v in vals) + ");")

        report.append({k: det[k] for k in
                       ("item_code", "population", "slug", "note", "state", "design_scale",
                        "tier_basis", "governing_refs", "code_floor_only",
                        "regulatory_stratum_only", "derivation_sha", "n_sources",
                        "needs_population_assessment", "tier_inconsistent", "falsification")}
                      | {"convergence": det["convergence"], "confidence": det["confidence"],
                         "gap_register_id": gap_id, "cell_id": cell_id,
                         "convergence_id": this_conv,
                         "source_records": [{k2: r[k2] for k2 in
                                             ("ref_id", "tier", "evidence_type", "grain",
                                              "grain_why", "scale_directness",
                                              "population_directness", "conditioning")}
                                            for r in det["source_records"]]})

    sql_lines.append("COMMIT;")
    conn.commit()
    with open(args.emit_sql, "w") as f:
        f.write("\n".join(sql_lines) + "\n")
    if args.report_json:
        with open(args.report_json, "w") as f:
            json.dump(report, f, indent=1)

    for r in report:
        print(f"{r['item_code']}×{r['population']:<5} {r['state']:<12} "
              f"basis={r['tier_basis'] or '-':<32} scale={r['design_scale']:<10} "
              f"refs={len(r['governing_refs'])} rso={r['regulatory_stratum_only']} "
              f"cfo={r['code_floor_only']} sha={r['derivation_sha'][:12]}")
    print(f"\n{len(report)} cells written; SQL artifact: {args.emit_sql}")
    if ENUM_DRIFT:
        print(f"DRIFT FINDING: populations valid in live table but missing from "
              f"schemas.enums.PopulationCode: {sorted(set(ENUM_DRIFT))} — "
              f"recorded for the ratification package (reconciliation item).")


if __name__ == "__main__":
    main()
