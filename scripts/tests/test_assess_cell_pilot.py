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
  - UNVERIFIED-1 present -> has_unverified_sources flag set (§2.8)
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
                  "G-03", "MOB", "syn-slug", "co2-only")
    expect("Co-2-only => stated", d["state"] == "stated", d["state"])
    expect("Co-2-only tier_basis == CO2", d["tier_basis"] == "CO2", d["tier_basis"])

    # 2. T6-only, 3 distinct jurisdictions -> provisional + cfo + rso + universal
    d = determine(synth_db([{"tier": 6, "evidence_type": "code", "jurisdiction": j}
                            for j in ("US", "GB", "AU")]),
                  "E-06", "MOB", "syn-slug", "t6-only")
    expect("T6-only(3 jur) => provisional", d["state"] == "provisional", d["state"])
    expect("T6-only => code_floor_only=1", d["code_floor_only"] == 1)
    expect("T6-only => regulatory_stratum_only=1", d["regulatory_stratum_only"] == 1)
    expect("T6-only => design_scale universal", d["design_scale"] == "universal")
    expect("T6-only never stated", d["state"] != "stated")

    # 3. T6-only, one jurisdiction x3 -> pending (jurisdiction distinctness)
    d = determine(synth_db([{"tier": 6, "evidence_type": "code", "jurisdiction": "US"}
                            for _ in range(3)]),
                  "E-06", "DEM", "syn-slug", "t6-mono")
    expect("T6-only(1 jur) => pending", d["state"] == "pending", d["state"])

    # 4. All sources disqualified -> pending + flag (§2.8)
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical",
                             "verification_status": "UNVERIFIED-CLOSED"}]),
                  "B-10", "NEU", "syn-slug", "disqualified")
    expect("all-disqualified => pending", d["state"] == "pending", d["state"])
    expect("all_sources_disqualified flag set", d["all_sources_disqualified"] == 1)

    # 5. UNVERIFIED-1 present -> has_unverified_sources (§2.8)
    d = determine(synth_db([{"tier": 2, "evidence_type": "sr_meta"},
                            {"tier": 6, "evidence_type": "code",
                             "verification_status": "UNVERIFIED-1"}]),
                  "B-10", "DEM", "syn-slug", "unverified-present")
    expect("UNVERIFIED-1 => has_unverified_sources=1", d["has_unverified_sources"] == 1)
    expect("anchored despite unverified T6", d["state"] == "stated", d["state"])

    # 6. Model enforcement: not_applicable requires rationale
    try:
        EvidenceStateRecord(item_code="E-06", population="MOB", state="not_applicable",
                            not_applicable_rationale=None)
        expect("not_applicable without rationale rejected", False)
    except Exception:
        expect("not_applicable without rationale rejected", True)

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
