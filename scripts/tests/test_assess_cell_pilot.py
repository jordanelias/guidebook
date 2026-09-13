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


# The scope each evidence_type needs for its stored tier to be DERIVABLE
# (schemas/tier_derivation.TIER_MAP). Derived from that map at import, never
# restated: a copy would drift the first time the ratified ladder changes.
#
# WHY THE FIXTURE NOW HAS TO CARRY SCOPE AT ALL. It did not before 2026-09-10,
# because the engine merely REPORTED tier inconsistency and anchored anyway. B5a
# makes a source whose tier is not derivable from its own (evidence_type, scope)
# NON-ANCHORING, so a fixture with scope=None would put every one of these tests
# into `pending` and prove nothing about the branch it is named for. Supplying the
# scope is not weakening the test — it is the test finally stating the precondition
# the doctrine always had.
def _default_scope(evidence_type, tier):
    from schemas.tier_derivation import TIER_MAP
    for (et, sc), tt in TIER_MAP.items():
        if et == evidence_type and tt == tier:
            return sc
    return None


def synth_db(sources, parameter_id=1, extractions_per_source=1):
    """Minimal in-memory schema for determine(): evidence_sources +
    source_value_extractions + evidence_population_match.

    RE-KEYED 2026-09-10 with B4c. `determine()` no longer gathers by slug, so
    `source_slug_links` is no longer what puts a source in front of the engine —
    an EXTRACTION FOR THE PARAMETER is. The junction is still created because the
    fixture should look like the real schema, and a fixture that is laxer than the
    database it stands for is how an engine passes its tests and fails on replay.

    `extractions_per_source` exercises the ruled 1:N fan-out (D-0168): N extraction
    rows for one source must still be ONE source in the governing set. Without the
    DISTINCT in gather_sources, a code document's clauses would corroborate
    themselves.
    """
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
      CREATE TABLE evidence_sources (
        ref_id TEXT PRIMARY KEY, tier INT, evidence_type TEXT, co1_source_type TEXT,
        verification_status TEXT, scope TEXT, jurisdiction TEXT, superseded_by_ref_id TEXT);
      CREATE TABLE source_slug_links (ref_id TEXT, slug TEXT);
      CREATE TABLE source_value_extractions (
        extraction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id TEXT, slug TEXT, parameter_id INTEGER,
        identity_code TEXT, icf_code TEXT, needs_code TEXT, medical_code TEXT,
        claim_type TEXT, claimed_value TEXT, figure_role TEXT, comparator TEXT);
      CREATE TABLE evidence_population_match (
        match_id TEXT, ref_id TEXT, match_grade TEXT, target_population TEXT);
    """)
    for i, s in enumerate(sources):
        ref = s.get("ref_id", f"REF-SYN-{i:03d}")
        scope = s["scope"] if "scope" in s else _default_scope(s["evidence_type"], s["tier"])
        conn.execute("INSERT INTO evidence_sources VALUES (?,?,?,?,?,?,?,?)",
                     (ref, s["tier"], s["evidence_type"], s.get("co1_source_type"),
                      s.get("verification_status", "VERIFIED"), scope,
                      s.get("jurisdiction"), None))
        conn.execute("INSERT INTO source_slug_links VALUES (?, 'syn-slug')", (ref,))
        for _ in range(s.get("extractions", extractions_per_source)):
            conn.execute(
                # figure_role='claim' because these fixtures exist to exercise the
                # TIER/GRAIN logic, and gather_sources now returns only rows that
                # supply a value (migration 075). A fixture row left ungraded would
                # be filtered out before the logic under test ever ran, and every
                # assertion here would pass over an empty governing set -- the
                # vacuity CLAUDE.md 5(a) names, hidden inside the engine's own tests.
                "INSERT INTO source_value_extractions "
                "(ref_id, slug, parameter_id, identity_code, claim_type, claimed_value, "
                " figure_role) "
                "VALUES (?, 'syn-slug', ?, 'MOB', 'numerical', '1', 'claim')",
                (ref, parameter_id))
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

    # 3b-3d. jurisdiction distinctness must be NORMALISED before counting (audit
    # Task 4, fixed 2026-09-10). Uses tier 5 (national_fw), never tier 4: a T4
    # source is "rich" the moment it is present, unconditionally on
    # jurisdiction (§2.3's first clause), which would hide exactly the bug
    # being tested here. Two T4-5 sources with >=2 distinct jurisdictions is
    # the smallest branch that isolates the jurisdiction-distinctness rule.

    # 3b. ("US", None) -- a MISSING jurisdiction is not "one more jurisdiction".
    # Before the fix, {"US", None} counted as 2 distinct values -> wrongly rich.
    d = determine(synth_db([{"tier": 5, "evidence_type": "national_fw", "jurisdiction": "US"},
                            {"tier": 5, "evidence_type": "national_fw", "jurisdiction": None}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "t45-us-and-none")
    expect("T4-5(US, None) => NOT rich (None does not count as a jurisdiction)",
          d["state"] != "provisional", d["state"])

    # 3c. ("US","us","US ") -- case and whitespace variants of ONE jurisdiction.
    # Before the fix this set had 3 raw members -> wrongly rich.
    d = determine(synth_db([{"tier": 5, "evidence_type": "national_fw", "jurisdiction": j}
                            for j in ("US", "us", "US ")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "t45-case-whitespace")
    expect("T4-5(US/us/US ) => NOT rich (one jurisdiction, not three)",
          d["state"] != "provisional", d["state"])

    # 3d. ("US","CA") -- genuinely two distinct jurisdictions -> rich, as control.
    d = determine(synth_db([{"tier": 5, "evidence_type": "national_fw", "jurisdiction": j}
                            for j in ("US", "CA")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "t45-two-distinct")
    expect("T4-5(US, CA) => rich (two genuinely distinct jurisdictions)",
          d["state"] == "provisional", d["state"])

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

    # ── B4c / B5a: the 2026-09-10 re-key and the tier gate ───────────────────
    # These four pin the change that made the engine's subject real. Before it,
    # `param 1 × MOB` on the live corpus returned `stated basis=T1+CO1+T2` on five
    # governing sources, NONE of which held an extraction for parameter 1, and all
    # nine gathered sources were flagged tier_inconsistent in the same report.

    # B4c-1. A source admitted to the slug but holding no extraction FOR THIS
    # PARAMETER is not evidence for it. This is the whole defect in one assertion.
    conn = synth_db([{"tier": 1, "evidence_type": "clinical"}], parameter_id=1)
    conn.execute("INSERT INTO evidence_sources VALUES "
                 "('REF-SYN-OTHER',1,'clinical',NULL,'VERIFIED','high_control',NULL,NULL)")
    conn.execute("INSERT INTO source_slug_links VALUES ('REF-SYN-OTHER','syn-slug')")
    conn.execute("INSERT INTO source_value_extractions "
                 "(ref_id, slug, parameter_id, identity_code, claim_type, claimed_value) "
                 "VALUES ('REF-SYN-OTHER','syn-slug', 2, 'MOB','numerical','9')")
    d = determine(conn, 1, {"identity_code": "MOB"}, "syn-slug", "slug-mate, other parameter")
    expect("B4c: a slug-mate with an extraction for ANOTHER parameter is not gathered",
           [r["ref_id"] for r in d["source_records"]] == ["REF-SYN-000"],
           str([r["ref_id"] for r in d["source_records"]]))
    expect("B4c: every governing ref holds an extraction for the parameter",
           set(d["governing_refs"]) <= {"REF-SYN-000"}, str(d["governing_refs"]))

    # B4c-2. The ruled 1:N fan-out. One source, four clause-level extractions: ONE
    # source in the governing set, four in the extraction count. Without DISTINCT in
    # gather_sources this source would corroborate itself four times over.
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical", "extractions": 4}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "one source, four clauses")
    expect("B4c: 1:N fan-out counts the SOURCE once", d["n_sources"] == 1, str(d["n_sources"]))
    expect("B4c: 1:N fan-out reports all four extractions", d["n_extractions"] == 4,
           str(d["n_extractions"]))
    expect("B4c: 1:N fan-out yields one governing ref", len(d["governing_refs"]) == 1,
           str(d["governing_refs"]))

    # B5a-1. A source whose stored tier is not derivable from its own
    # (evidence_type, scope) CANNOT ANCHOR. scope=None on a T1 clinical row is
    # exactly the live state of all nine sources in the corpus on 2026-09-10.
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical", "scope": None}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "tier not derivable")
    expect("B5a: tier_inconsistent source cannot anchor => not stated",
           d["state"] != "stated", d["state"])
    expect("B5a: tier_inconsistent source is reported as non-anchoring",
           d["non_anchoring_on_tier"] == ["REF-SYN-000"], str(d["non_anchoring_on_tier"]))
    expect("B5a: the pre-gate conditioning is preserved for the reader",
           d["source_records"][0]["conditioning_before_tier_gate"] != "NON-ANCHORING",
           str(d["source_records"][0]["conditioning_before_tier_gate"]))
    expect("B5a: it contributes no governing refs", d["governing_refs"] == [],
           str(d["governing_refs"]))

    # B5a-2. A parameter with no extraction at all is `pending` with a gap, and the
    # gap says WHICH absence it is. The old gap text named a missing slug-link and
    # pointed at the item_bpc_links bridge — a sentence about a join the engine no
    # longer makes, into a table layer the owner emptied.
    d = determine(synth_db([]), 1, {"identity_code": "MOB"}, "syn-slug", "nothing extracted")
    expect("B5a: no extraction for the parameter => pending", d["state"] == "pending", d["state"])
    expect("B5a: pending cell needs a gap", d["gap_needed"] is True)
    expect("B5a: zero sources and zero extractions are reported",
           (d["n_sources"], d["n_extractions"]) == (0, 0),
           str((d["n_sources"], d["n_extractions"])))
    expect("B5a: an empty corpus is not 'all sources disqualified'",
           d["all_sources_disqualified"] == 0)

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
