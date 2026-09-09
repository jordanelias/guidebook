#!/usr/bin/env python3
"""
scripts/tests/test_assess_cell_pilot.py — unit tests for the pilot determination
engine's doctrinal branches that have NO real cell in the corpus (adversarial
finding 2 established that PILOT-MANIFEST.md previously claimed these tests
existed when they did not; this file makes the claim true).

Branches covered here, each against a synthetic in-memory DB:
  - pure Co-2-only basis  -> stated, tier_basis CO2 (§2.2 condition 3)
  - pure T6-only, >=3 distinct jurisdictions -> provisional + code_floor_only
    + regulatory_stratum_only + design_scale universal (G1)
  - pure T6-only, single jurisdiction -> pending (fails §2.3 jurisdiction
    distinctness, per the pilot-2 richness fix)
  - all sources disqualified -> pending + all_sources_disqualified flag (§2.8)
  - UNVERIFIED present -> has_unverified_sources flag set (§2.8; D-0157 vocabulary)
  - not_applicable requires rationale; divergent requires synthesis_approach
    (schemas.evidence_state model enforcement — the validator's counterparts of
    the two mutation cases the manifest previously claimed without artifacts)

Run: python3 scripts/tests/test_assess_cell_pilot.py   (exit 1 on any failure)
"""
import os
import sqlite3
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "assess"))

from assess_cell import determine  # noqa: E402
from schemas.evidence_state import ConvergenceAssessment, EvidenceStateRecord  # noqa: E402


def synth_db(sources):
    """Minimal in-memory schema for determine(): evidence_sources +
    source_slug_links + evidence_population_match."""
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
      CREATE TABLE evidence_sources (
        ref_id TEXT PRIMARY KEY, tier INT, evidence_type TEXT, co1_source_type TEXT,
        verification_status TEXT, scope TEXT, jurisdiction TEXT, superseded_by_ref_id TEXT);
      CREATE TABLE source_slug_links (ref_id TEXT, slug TEXT);
      CREATE TABLE evidence_population_match (
        match_id TEXT, ref_id TEXT, match_grade TEXT, target_population TEXT);
    """)
    for i, s in enumerate(sources):
        ref = s.get("ref_id", f"REF-SYN-{i:03d}")
        conn.execute("INSERT INTO evidence_sources VALUES (?,?,?,?,?,?,?,?)",
                     (ref, s["tier"], s["evidence_type"], s.get("co1_source_type"),
                      s.get("verification_status", "VERIFIED"), s.get("scope"),
                      s.get("jurisdiction"), None))
        conn.execute("INSERT INTO source_slug_links VALUES (?, 'syn-slug')", (ref,))
    return conn


FAILED = []


def expect(label, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}: {label}" + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILED.append(label)


def main():
    # 1. Pure Co-2-only -> stated (§2.2 condition 3)
    d = determine(synth_db([{"tier": 2, "evidence_type": "co2"},
                            {"tier": 2, "evidence_type": "co2"}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "co2-only")
    expect("Co-2-only => stated", d["state"] == "stated", d["state"])
    expect("Co-2-only tier_basis == CO2", d["tier_basis"] == "CO2", d["tier_basis"])

    # 2. T6-only, 3 distinct jurisdictions -> provisional + cfo + rso + universal
    d = determine(synth_db([{"tier": 6, "evidence_type": "code", "jurisdiction": j}
                            for j in ("US", "GB", "AU")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "t6-only")
    expect("T6-only(3 jur) => provisional", d["state"] == "provisional", d["state"])
    expect("T6-only => code_floor_only=1", d["code_floor_only"] == 1)
    expect("T6-only => regulatory_stratum_only=1", d["regulatory_stratum_only"] == 1)
    expect("T6-only => design_scale universal", d["design_scale"] == "universal")
    expect("T6-only never stated", d["state"] != "stated")

    # 3. T6-only, one jurisdiction x3 -> pending (jurisdiction distinctness)
    d = determine(synth_db([{"tier": 6, "evidence_type": "code", "jurisdiction": "US"}
                            for _ in range(3)]),
                  1, {"identity_code": "DEM"}, "syn-slug", "t6-mono")
    expect("T6-only(1 jur) => pending", d["state"] == "pending", d["state"])

    # 4. All sources disqualified -> pending + flag (§2.8)
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical",
                             "verification_status": "UNVERIFIED-CLOSED"}]),
                  1, {"identity_code": "NEU"}, "syn-slug", "disqualified")
    expect("all-disqualified => pending", d["state"] == "pending", d["state"])
    expect("all_sources_disqualified flag set", d["all_sources_disqualified"] == 1)

    # 5. UNVERIFIED present -> has_unverified_sources (§2.8)
    d = determine(synth_db([{"tier": 2, "evidence_type": "sr_meta"},
                            {"tier": 6, "evidence_type": "code",
                             "verification_status": "UNVERIFIED"}]),
                  1, {"identity_code": "DEM"}, "syn-slug", "unverified-present")
    expect("UNVERIFIED => has_unverified_sources=1", d["has_unverified_sources"] == 1)
    expect("anchored despite unverified T6", d["state"] == "stated", d["state"])

    # 5b. A cell stated in NO identity lens leaves population-directness NOT_ASSESSED.
    # New with the 071 re-key: evidence_population_match.target_population is written in
    # identity terms only, so a determination stated in ICF / access-need / medical terms
    # alone has nothing to attribute a match row TO. G2 says that dimension is unassessed,
    # not absent — it caps consolidation at DOWN-WEIGHTED and flags the source. The old
    # engine could not reach this state at all, because population was mandatory.
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical"}]),
                  1, {"icf_code": "AX-AMB"}, "syn-slug", "lens without identity")
    expect("no identity lens => every source needs population assessment (G2)",
           d["needs_population_assessment"] == [r["ref_id"] for r in d["source_records"]],
           str(d["needs_population_assessment"]))
    expect("no identity lens => population_directness NOT_ASSESSED, never EXACT",
           all(r["population_directness"] == "NOT_ASSESSED" for r in d["source_records"]),
           str([r["population_directness"] for r in d["source_records"]]))

    # 6. Model enforcement: not_applicable requires rationale.
    #
    # This assertion passed for the wrong reason between migration 071 and
    # 2026-09-09. The cell was keyed (item_code="E-06", population="MOB"), 071
    # re-keyed EvidenceStateRecord to parameter_id + lens, and the model forbids
    # extras -- so the rejection fired on `extra_forbidden` for item_code and never
    # reached the rationale rule at all. A bare `except Exception` cannot tell the
    # two apart, which is why the assertion below now names the rule it is testing:
    # a refusal is only evidence for the refusal you asked for.
    try:
        EvidenceStateRecord(parameter_id=1, identity_code="MOB", state="not_applicable",
                            not_applicable_rationale=None)
        expect("not_applicable without rationale rejected", False)
    except Exception as e:
        expect("not_applicable without rationale rejected",
               "not_applicable_rationale" in str(e), str(e).splitlines()[0])

    # 7. Model enforcement: divergent requires synthesis_approach
    try:
        ConvergenceAssessment(status="divergent", rationale="axes disagree",
                              synthesis_approach=None)
        expect("divergent without synthesis_approach rejected", False)
    except Exception:
        expect("divergent without synthesis_approach rejected", True)

    if FAILED:
        print(f"\nFAIL: {len(FAILED)} test(s): {FAILED}")
        sys.exit(1)
    print("\nPASS: all pilot-engine branch tests")


if __name__ == "__main__":
    main()
