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


def synth_db(sources, parameter_id=1, extractions_per_source=1,
             icf_links=(), gates=(), direction=None):
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
        claim_type TEXT, claimed_value TEXT, claimed_unit TEXT,
        figure_role TEXT, comparator TEXT);
      CREATE TABLE evidence_population_match (
        match_id TEXT, ref_id TEXT, match_grade TEXT, target_population TEXT);
      -- 080. CREATED UNCONDITIONALLY, EVEN EMPTY, for the reason this docstring
      -- already gives about source_slug_links: a fixture laxer than the database it
      -- stands for is how an engine passes its tests and fails on replay. An empty
      -- population_icf_links is also the honest default -- it is what a cell whose
      -- identity lens has no promoted functional mapping actually looks like.
      CREATE TABLE population_icf_links (
        link_id INTEGER PRIMARY KEY AUTOINCREMENT, population_code TEXT, icf_code TEXT,
        mechanism TEXT, mapping_confidence TEXT, provenance TEXT, notes TEXT,
        created_at TEXT, created_by_session TEXT);
      -- 086. Created here for the same reason as source_slug_links and
      -- population_icf_links: `compose_value` reads accessibility_direction out of
      -- this table, and a fixture without it can only ever exercise the branch that
      -- declines for want of a direction. Left EMPTY unless a case passes one, so the
      -- no-direction branch stays testable too.
      CREATE TABLE base_parameters (
        parameter_id INTEGER PRIMARY KEY, term_id TEXT, status TEXT,
        accessibility_direction TEXT, direction_rationale TEXT);
      CREATE TABLE determination_gates (
        gate_id INTEGER PRIMARY KEY AUTOINCREMENT, parameter_id INTEGER,
        identity_code TEXT, verdict TEXT, trigger_ref_id TEXT, trigger_tier INT,
        trigger_evidence_type TEXT, detail TEXT, raised_at TEXT, raised_by_session TEXT,
        resolved_at TEXT, resolved_by_session TEXT, resolution_rationale TEXT);
      CREATE VIEW v_open_determination_gates AS
        SELECT g.gate_id, g.parameter_id, g.identity_code, g.verdict, g.trigger_ref_id,
               g.trigger_tier, g.trigger_evidence_type, g.detail, g.raised_at,
               g.raised_by_session
          FROM determination_gates g WHERE g.resolved_at IS NULL;
    """)
    if direction:
        conn.execute("INSERT INTO base_parameters (parameter_id, term_id, status, "
                     "accessibility_direction, direction_rationale) "
                     "VALUES (?, 'TERM-SYN', 'active', ?, 'synthetic fixture')",
                     (parameter_id, direction))
    for L in icf_links:
        conn.execute("INSERT INTO population_icf_links (population_code, icf_code, "
                     "mechanism, mapping_confidence, provenance) VALUES (?,?,?,?,?)", L)
    for g in gates:
        conn.execute("INSERT INTO determination_gates (parameter_id, identity_code, verdict, "
                     "trigger_tier, trigger_evidence_type, detail, raised_at, "
                     "raised_by_session) VALUES (?,?,?,?,?,?,'2026-09-13','syn')", g)
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
                # `figure_role` is per-source since 086. It defaults to 'claim' for the
                # reason the comment above gives, and a fixture may set 'finding' to
                # exercise the proxy branch -- a source that MEASURED the parameter
                # without stating a value for it (owner 2026-09-16).
                "INSERT INTO source_value_extractions "
                "(ref_id, slug, parameter_id, identity_code, claim_type, claimed_value, "
                " claimed_unit, figure_role, comparator) "
                "VALUES (?, 'syn-slug', ?, 'MOB', ?, ?, ?, ?, ?)",
                (ref, parameter_id,
                 s.get("claim_type", "numerical"),
                 s.get("claimed_value", "1"),
                 s.get("claimed_unit"),
                 s.get("figure_role", "claim"),
                 s.get("comparator")))
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

    # ── 8. THE DERIVATION HANDSHAKE (migration 080) — H2, H3, H4 ──────────────
    # DR-2026-07-13, carrying an `[ENGINE-LAG 2026-08-15]` marker whose own text named
    # what was missing. Every branch below has NO live cell to exercise it —
    # `base_parameters` is empty after the 2026-09-13 circulation clear — which is the
    # condition this whole file exists for.
    MOB_LINK = [("MOB", "d450", "Biomechanical — ambulation", "high_predictive", "fda-skill")]
    # Tier 1 is (evidence_type=clinical, scope=high_control) per schemas.tier_derivation
    # .TIER_MAP; _default_scope() supplies the scope, and B5a makes an underivable tier
    # non-anchoring, so naming the wrong evidence_type here would send every assertion
    # below through `pending` and prove nothing.
    T1 = {"tier": 1, "evidence_type": "clinical"}

    # 8a. DUAL: the population path (governing evidence) meets the function path (a
    # promoted population_icf_links row for this cell's identity lens).
    d = determine(synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK),
                  1, {"identity_code": "MOB"}, "syn-slug", "dual")
    expect("H2: both paths present => dual", d["derivation_paths"] == "dual",
           str(d["derivation_paths"]))
    expect("H3: functional_basis is READ from population_icf_links, never typed",
           bool(d["functional_basis"]) and "d450" in d["functional_basis"])
    expect("H2: a dual determination owes no named-path rationale",
           d["derivation_rationale"] is None)

    # 8b. POPULATION_ONLY with no functional mapping: the rationale is OWED, and is
    # generated rather than asked for.
    d = determine(synth_db([dict(T1)]), 1, {"identity_code": "MOB"}, "syn-slug", "pop-only")
    expect("H2: no icf link => population_only",
           d["derivation_paths"] == "population_only", str(d["derivation_paths"]))
    expect("H2: an unanchored single-path claim owes a rationale",
           bool(d["derivation_rationale"]))
    expect("H3: no mapping => functional_basis absent, not empty JSON",
           d["functional_basis"] is None)

    # 8c. THE DIGNITY LINE. A community-rooted claim stays fully assertable as
    # population_only and owes NO rationale: "there is no bottom-up override of Co-1."
    d = determine(synth_db([{"tier": 1, "evidence_type": "co1",
                             "co1_source_type": "dpo_research"}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "co1-anchored")
    expect("H2: Co-1 community provenance => cultural_claim_anchor recorded",
           bool(d["cultural_claim_anchor"]))
    expect("H2: a culturally anchored claim owes no rationale",
           d["derivation_rationale"] is None)
    expect("H2: the anchor does not upgrade the path — still population_only",
           d["derivation_paths"] == "population_only")

    # 8d. THE ANCHOR IS CHECKED, NOT SELF-DECLARED. Same Co-1 tier, individual-grain
    # provenance (G3) -> no anchor, so the standard rationale is owed after all. This is
    # the criterion that stops the protection becoming a route around the mechanism.
    d = determine(synth_db([{"tier": 1, "evidence_type": "co1",
                             "co1_source_type": "academic_narrative"}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "co1-unanchored")
    expect("H2: Co-1 tier ALONE does not anchor the protection",
           d["cultural_claim_anchor"] is None)
    expect("H2: so the unanchored Co-1 claim owes the rationale",
           bool(d["derivation_rationale"]))

    # 8e. H4: an open gate CAPS a stated cell at provisional.
    d = determine(synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK,
                           gates=[(1, "MOB", "MISLINKED", 1, "primary_research",
                                   "population links omit DEAF")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "gated")
    expect("H4: an open gate forces provisional", d["state"] == "provisional", d["state"])
    expect("H4: the gate is reported as binding", any(g["binds"] for g in d["gates"]))
    expect("H4: a gate CAPS — the cell keeps its anchors",
           d["tier_basis"] == "T1" and bool(d["governing_refs"]), str(d["tier_basis"]))

    # 8f. THE LADDER-INVERSION GUARD: "a grey-tier CONTRADICTS cannot pin a T1-anchored
    # cell indefinitely". The weaker gate is kept and REPORTED, never silently dropped.
    d = determine(synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK,
                           gates=[(1, "MOB", "CONTRADICTS", 6, "code", "a code disagrees")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "weak-gate")
    expect("H4: a T6 gate does not bind a T1-anchored cell",
           d["state"] == "stated", d["state"])
    expect("H4: the non-binding gate is reported, not dropped",
           len(d["gates"]) == 1 and not d["gates"][0]["binds"])

    # 8g. A gate raised on another identity lens does not reach this cell.
    d = determine(synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK,
                           gates=[(1, "DEAF", "UNLINKED", 1, "primary_research", "other lens")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "other-lens")
    expect("H4: a gate on another lens does not bind", d["state"] == "stated", d["state"])

    # 8h. Resolution is a NAMED PATH, and the view is what enforces it: a resolved gate
    # stops binding, so no cell sits at provisional with no owner of resolution.
    c = synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK,
                 gates=[(1, "MOB", "UNLINKED", 1, "primary_research", "d")])
    c.execute("UPDATE determination_gates SET resolved_at='2026-09-13', "
              "resolved_by_session='syn', resolution_rationale='adjudicated'")
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "resolved")
    expect("H4: a resolved gate no longer binds", d["state"] == "stated", d["state"])

    # 8i. THE DIGNITY LINE IS A DATABASE CONSTRAINT, not doctrine binding on authors.
    # The LIVE DDL is read rather than restated: a CHECK copied into this file would be a
    # second home for the rule and would keep passing after the real constraint drifted.
    live_db = os.path.join(REPO_ROOT, "data", "guidebook.db")
    if os.path.exists(live_db):
        live = sqlite3.connect(f"file:{live_db}?mode=ro", uri=True)
        ddl = live.execute("SELECT sql FROM sqlite_master WHERE type='table' "
                           "AND name='specifications'").fetchone()[0]
        probe = sqlite3.connect(":memory:")
        probe.executescript(ddl)
        # The UNIQUE row identity comes with the table, so each probe row below takes a
        # distinct lens. Without the index the fixture would be laxer than the object it
        # stands for, which is how a test passes over a state the database refuses.
        for (isql,) in live.execute(
                "SELECT sql FROM sqlite_master WHERE type='index' "
                "AND tbl_name='specifications' AND sql IS NOT NULL"):
            probe.executescript(isql)
        base = {"parameter_id": 1, "state": "stated", "code_floor_only": 0,
                "has_unverified_sources": 0, "all_sources_disqualified": 0,
                "regulatory_stratum_only": 0}
        seq = [0]

        def try_row(**extra):
            seq[0] += 1
            # D-0182: at least one lens column. A row with none is refused by a DIFFERENT
            # CHECK, and supplying the lens is what keeps the assertions below about the
            # constraint they name.
            row = dict(base, identity_code=f"LENS{seq[0]}", **extra)
            cols = ", ".join(row)
            try:
                probe.execute(f"INSERT INTO specifications ({cols}) VALUES ("
                              + ",".join("?" * len(row)) + ")", tuple(row.values()))
                return None
            except sqlite3.IntegrityError as e:
                return str(e)

        # THE POSITIVE CONTROL FIRST, and it is not ceremony. Every other assertion here
        # expects a REFUSAL, so a fixture that refuses everything would pass them all
        # while testing nothing -- the vacuous-gate failure CLAUDE.md 5(a) names, inside
        # the test written to prove a constraint works. If this line fails, the fixture is
        # wrong and the refusals below mean nothing.
        _control = try_row()
        expect("H2 CHECK: control — a row with no derivation_paths is accepted",
               _control is None, str(_control))
        expect("H2 CHECK: population_only with neither rationale nor anchor is REFUSED",
               try_row(derivation_paths="population_only") is not None)
        expect("H2 CHECK: population_only WITH a cultural anchor is accepted",
               try_row(derivation_paths="population_only",
                       cultural_claim_anchor='["REF-1"]') is None)
        expect("H2 CHECK: population_only WITH a rationale is accepted",
               try_row(derivation_paths="population_only",
                       derivation_rationale="no function path") is None)
        expect("H2 CHECK: function_only without a rationale is REFUSED",
               try_row(derivation_paths="function_only") is not None)
        expect("H2 CHECK: dual owes neither", try_row(derivation_paths="dual") is None)
        expect("H2 CHECK: cultural_claim_anchor must be valid JSON",
               try_row(derivation_paths="dual", cultural_claim_anchor="not json") is not None)
    else:
        expect("H2 CHECK: live DDL available to test against", False,
               "data/guidebook.db absent")

    # ── 086 / owner statement 2026-09-16: the PROXY branch ────────────────────
    # ACTION (2) said assess_cell "must be able to reach a determination from
    # findings plus a threshold, not only from `claim` rows". These four cases are
    # the regression cover for that, and for the three things it must NOT do.
    _t6 = [{"tier": 6, "evidence_type": "code", "jurisdiction": j} for j in ("US", "GB", "AU")]
    _find = [{"tier": 1, "evidence_type": "clinical", "ref_id": "REF-FIND-1",
              "figure_role": "finding", "claim_type": "qualitative",
              "claimed_value": "discomfort rises with gradient"}]

    d = determine(synth_db(_t6 + _find), 1, {"identity_code": "MOB"}, "syn-slug", "proxy")
    expect("PROXY: threshold + anchoring finding => marked rests_on_proxy_inference",
           d["rests_on_proxy_inference"] == 1, str(d["rests_on_proxy_inference"]))
    expect("PROXY: regulatory_stratum_only is FALSE — the stratum is not all there is",
           d["regulatory_stratum_only"] == 0, str(d["regulatory_stratum_only"]))
    expect("PROXY: tier_basis carries the marker and NOT the rso marker",
           "(proxy_inference)" in d["tier_basis"]
           and not d["tier_basis"].endswith("(regulatory_stratum_only)"), d["tier_basis"])
    expect("PROXY: state is provisional, NEVER stated (ACTION 1)",
           d["state"] == "provisional", d["state"])
    # The invariant migration 075 exists for, and stop condition 6: a finding never
    # governs. It supplies direction and lands in `supporting`.
    expect("PROXY: the finding does NOT govern",
           "REF-FIND-1" not in d["governing_refs"], str(d["governing_refs"]))
    expect("PROXY: the finding DOES support",
           "REF-FIND-1" in d["supporting_refs"], str(d["supporting_refs"]))
    expect("PROXY: the absence list no longer asserts 'No Tier 1 clinical' over T1 evidence",
           not any("No Tier 1" in a for a in d["confidence"]["absent"]),
           str(d["confidence"]["absent"]))

    expect("PROXY: one finding axis => single_axis",
           d["convergence"]["status"] == "single_axis", d["convergence"]["status"])
    # TWO finding axes must NOT report single_axis. The first cut of the proxy branch
    # hard-coded it while populating three axes, and validate_evidence_state -- which
    # recomputes the axis count from the row it is given -- refused the convergence
    # row. This is that defect, pinned.
    d2 = determine(synth_db(_t6 + _find + [
        {"tier": 1, "evidence_type": "co1", "ref_id": "REF-FIND-2",
         "co1_source_type": "lived_experience_publication", "figure_role": "finding",
         "claim_type": "qualitative", "claimed_value": "too steep to self-propel"}]),
        1, {"identity_code": "MOB"}, "syn-slug", "proxy-2-axes")
    expect("PROXY: two finding axes => pending_assessment, never single_axis",
           d2["convergence"]["status"] == "pending_assessment", d2["convergence"]["status"])

    # The floor claim is UNCHANGED when no finding is present. If this regresses, the
    # proxy branch has started firing on cells that have no direction evidence at all.
    d = determine(synth_db(_t6), 1, {"identity_code": "MOB"}, "syn-slug", "floor")
    expect("NO-PROXY: threshold alone is still an unmarked floor claim",
           d["rests_on_proxy_inference"] == 0 and d["regulatory_stratum_only"] == 1,
           f"proxy={d['rests_on_proxy_inference']} rso={d['regulatory_stratum_only']}")
    expect("NO-PROXY: tier_basis keeps the rso marker",
           d["tier_basis"].endswith("(regulatory_stratum_only)"), d["tier_basis"])

    # Findings with NO threshold: still pending — the proxy step is degenerate without
    # a bound, which is the owner's own limit on the inference.
    d = determine(synth_db(_find), 1, {"identity_code": "MOB"}, "syn-slug", "no-threshold")
    expect("NO-THRESHOLD: findings alone do not reach a determination",
           d["state"] == "pending" and d["rests_on_proxy_inference"] == 0,
           f"{d['state']} proxy={d['rests_on_proxy_inference']}")
    expect("NO-THRESHOLD: the finding sources are counted, so the gap can name the "
           "right absence instead of claiming supersession",
           d["n_finding_sources"] == 1 and d["n_sources"] == 0,
           f"findings={d['n_finding_sources']} value-suppliers={d['n_sources']}")

    # ── Owner ruling 2026-09-17: PRESENT BOTH, never choose ───────────────────
    # Three codes state the same quantity, two as a percentage and one as a RATIO.
    # Before the ruling the ratio was unreadable and the interval was composed from
    # the two percentages alone. Now all three compose, on one exact scale.
    d = determine(synth_db([
        {"tier": 6, "evidence_type": "code", "jurisdiction": "US",
         "claimed_value": "8.33", "claimed_unit": "%", "comparator": "<="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "GB",
         "claimed_value": "1:20", "claimed_unit": "rise:run ratio", "comparator": "<="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "AU",
         "claimed_value": "6", "claimed_unit": "%", "comparator": "<="}],
        direction="lower_is_better"),
        1, {"identity_code": "MOB"}, "syn-slug", "both-notations")
    # 1:20 is 5%, gentler than either percentage row. If the ratio were still being
    # dropped this would return 6 -- the STEEPER figure -- and call it
    # most-accommodating, which is the failure the ruling was asked about.
    expect("NOTATION: a ratio now composes, and wins on the most-accommodating rule",
           d["value_max"] == 5.0, str(d["value_max"]))
    _n = {x["notation"]: x for x in (d["value_notations"] or [])}
    expect("NOTATION: BOTH notations are carried, neither chosen",
           set(_n) == {"%", "rise:run ratio"}, str(list(_n)))
    expect("NOTATION: the percentage rendering is 5 and the ratio rendering is 1:20",
           _n.get("%", {}).get("max") == "5"
           and _n.get("rise:run ratio", {}).get("max") == "1:20",
           str(d["value_notations"]))
    # The winning bound was WRITTEN as a ratio by a source and not as a percentage, so
    # one notation is stated and the other is the engine's rendering. ACTION (2) of the
    # ruling: mark which is which.
    expect("NOTATION: the notation a source actually wrote is marked stated",
           _n["rise:run ratio"]["stated"] is True, str(_n["rise:run ratio"]))
    expect("NOTATION: the notation the engine rendered is marked NOT stated",
           _n["%"]["stated"] is False, str(_n["%"]))
    expect("NOTATION: both renderings of 1:20 are exact, so neither is flagged inexact",
           _n["%"]["exact"] and _n["rise:run ratio"]["exact"], str(d["value_notations"]))

    # ACTION (3): a derived notation that does not terminate is marked INEXACT. 1:12 is
    # 8.333...% and no finite decimal is what the source wrote.
    d = determine(synth_db([
        {"tier": 6, "evidence_type": "code", "jurisdiction": "US",
         "claimed_value": "1:12", "claimed_unit": "rise:run ratio", "comparator": "<="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "GB",
         "claimed_value": "9", "claimed_unit": "%", "comparator": "<="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "AU",
         "claimed_value": "10", "claimed_unit": "%", "comparator": "<="}],
        direction="lower_is_better"),
        1, {"identity_code": "MOB"}, "syn-slug", "inexact-derivation")
    _n = {x["notation"]: x for x in (d["value_notations"] or [])}
    expect("NOTATION: 1:12 wins over 9% and 10% on the exact scale",
           _n.get("rise:run ratio", {}).get("max") == "1:12", str(d["value_notations"]))
    expect("NOTATION: a non-terminating derived rendering is marked INEXACT",
           _n["%"]["exact"] is False and _n["rise:run ratio"]["exact"] is True,
           str(d["value_notations"]))

    # A UNIT mismatch is still refused. The ruling is about NOTATION of one quantity
    # (ACTION 4); millimetres and degrees remain different units.
    d = determine(synth_db([
        {"tier": 6, "evidence_type": "code", "jurisdiction": "US",
         "claimed_value": "1200", "claimed_unit": "mm", "comparator": ">="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "GB",
         "claimed_value": "5", "claimed_unit": "degrees", "comparator": "<="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "AU",
         "claimed_value": "6", "claimed_unit": "degrees", "comparator": "<="}],
        direction="lower_is_better"),
        1, {"identity_code": "MOB"}, "syn-slug", "unit-mismatch")
    expect("NOTATION: genuinely different UNITS still refuse to compose",
           d["value_max"] is None and "different units" in (d["value_note"] or ""),
           str(d["value_note"]))

    # A ceiling stored with NO comparator is read as a point and contributes a floor
    # as well, giving min > max. That describes nothing and must not be emitted.
    d = determine(synth_db([
        {"tier": 6, "evidence_type": "code", "jurisdiction": "US",
         "claimed_value": "1:12", "claimed_unit": "rise:run ratio"},   # comparator MISSING
        {"tier": 6, "evidence_type": "code", "jurisdiction": "GB",
         "claimed_value": "1:20", "claimed_unit": "rise:run ratio", "comparator": "<="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "AU",
         "claimed_value": "5", "claimed_unit": "%", "comparator": "<="}],
        direction="lower_is_better"),
        1, {"identity_code": "MOB"}, "syn-slug", "no-comparator")
    expect("COMPARATOR: a missing comparator yields an INCOHERENT interval, and the "
           "engine refuses it instead of publishing min above max",
           d["value_min"] is None and d["value_max"] is None
           and "INCOHERENT INTERVAL" in (d["value_note"] or ""), str(d["value_note"]))

    # A family member with no arithmetic behind it must RAISE, not be read as if it
    # were already canonical. `degrees` is the arctangent of the ratio, not a
    # rescaling, so adding it to the family by analogy would make 5 degrees read as
    # 5 % -- silently, and only in the composed value.
    import assess_cell as _ac
    _saved = _ac.NOTATION_FAMILIES["gradient"]
    try:
        _ac.NOTATION_FAMILIES["gradient"] = _saved + ("degrees",)
        try:
            _ac.to_canonical("5", "degrees")
            expect("NOTATION: an unbacked family member is REFUSED", False,
                   "to_canonical accepted it")
        except NotImplementedError:
            expect("NOTATION: an unbacked family member is REFUSED, not read as canonical",
                   True)
    finally:
        _ac.NOTATION_FAMILIES["gradient"] = _saved

    # And a claim with no number at all is still reported rather than dropped (086).
    d = determine(synth_db([
        {"tier": 6, "evidence_type": "code", "jurisdiction": "US",
         "claimed_value": "5", "claimed_unit": "%", "comparator": "<="},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "GB",
         "claimed_value": "as gentle as practicable", "claimed_unit": "%",
         "claim_type": "qualitative"},
        {"tier": 6, "evidence_type": "code", "jurisdiction": "AU",
         "claimed_value": "6", "claimed_unit": "%", "comparator": "<="}],
        direction="lower_is_better"),
        1, {"identity_code": "MOB"}, "syn-slug", "unparsable-reported")
    expect("COMPOSE: a claim stating no number is REPORTED, not silently dropped",
           d["value_note"] and "2 of 3" in d["value_note"], str(d["value_note"]))

    if FAILED:
        print(f"\nFAIL: {len(FAILED)} test(s): {FAILED}")
        sys.exit(1)
    print("\nPASS: all pilot-engine branch tests")


if __name__ == "__main__":
    main()
