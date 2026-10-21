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

from assess_cell import NOT_PUBLISHABLE_METHODS, determine, gap_account  # noqa: E402
from schemas.enums import EvidenceMarker  # noqa: E402
from schemas.evidence_state import ConvergenceAssessment, EvidenceStateRecord  # noqa: E402

# The glyphs come from the enum, never typed: the row's CHECK holds the same vocabulary.
FULL, PARTIAL, WEAK = EvidenceMarker.FULL.value, EvidenceMarker.PARTIAL.value, EvidenceMarker.WEAK.value


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
      -- identity_icf_map is also the honest default -- it is what a cell whose
      -- identity lens has no promoted functional mapping actually looks like.
      CREATE TABLE identity_icf_map (
        link_id INTEGER PRIMARY KEY AUTOINCREMENT, identity_code TEXT, icf_code TEXT,
        mechanism TEXT, mapping_confidence TEXT, provenance TEXT, notes TEXT,
        created_at TEXT, created_by_session TEXT);
      -- 086. Created here for the same reason as source_slug_links and
      -- identity_icf_map: `compose_value` reads accessibility_direction out of
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
        conn.execute("INSERT INTO identity_icf_map (identity_code, icf_code, "
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
    expect("T4-5(US, CA) floor claim is weak even though its sources' own band is partial "
           "(the row's CHECK pins a regulatory-stratum-only cell at weak)",
           d["regulatory_stratum_only"] == 1 and d["marker"] == WEAK, f"{d['marker']}")

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
    # promoted identity_icf_map row for this cell's identity lens).
    d = determine(synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK),
                  1, {"identity_code": "MOB"}, "syn-slug", "dual")
    expect("H2: both paths present => dual", d["derivation_paths"] == "dual",
           str(d["derivation_paths"]))
    expect("H3: functional_basis is READ from identity_icf_map, never typed",
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
                             "co1_source_type": "dpo_position_statement"}]),
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
                "regulatory_stratum_only": 0, "marker": FULL}
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
        # Migration 116: the marker column's vocabulary is its CHECK's and EvidenceMarker's, and no
        # test inserted the middle glyph before; every branch's engine output must also satisfy
        # the live CHECKs, or the first such row would fail at INSERT after the scratch DB is written.
        import dbcore  # noqa: E402
        expect("MARKER vocabulary: the column's CHECK and EvidenceMarker agree",
               set(dbcore.check_values(live, "specifications", "marker"))
               == {m.value for m in EvidenceMarker})
        for _m in EvidenceMarker:
            expect(f"MARKER vocabulary: {_m.name} inserts as a live stated row",
                   try_row(marker=_m.value) is None)
        _eng_t6 = [{"tier": 6, "evidence_type": "code", "jurisdiction": j} for j in ("US", "GB", "AU")]
        _eng_find = [{"tier": 1, "evidence_type": "clinical", "ref_id": "REF-FIND-1",
                      "figure_role": "finding", "claim_type": "qualitative", "claimed_value": "x"}]
        for _label, _srcs in (("anchored", [{"tier": 2, "evidence_type": "co2"}]),
                              ("T3-clinical", [{"tier": 3, "evidence_type": "clinical",
                                                "scope": "lower_control"}]),
                              ("floor claim", _eng_t6), ("proxy", _eng_t6 + _eng_find),
                              ("T4-5 floor claim", [{"tier": 5, "evidence_type": "national_fw",
                                                     "jurisdiction": j} for j in ("US", "CA")]),
                              ("pending", [dict(_eng_t6[0]) for _ in range(3)])):
            _d = determine(synth_db(_srcs), 1, {"identity_code": "MOB"}, "syn-slug", _label)
            _refused = try_row(state=_d["state"], marker=_d["marker"],
                               regulatory_stratum_only=_d["regulatory_stratum_only"],
                               rests_on_proxy_inference=_d["rests_on_proxy_inference"],
                               code_floor_only=_d["code_floor_only"])
            expect(f"MARKER engine output ({_label}: {_d['state']} {_d['marker']}) satisfies the live CHECKs",
                   _refused is None, str(_refused))
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

    # ── The marker (migration 116; RULINGS R7, R39) ───────────────────────────
    d = determine(synth_db([{"tier": 2, "evidence_type": "co2"}]), 1,
                  {"identity_code": "MOB"}, "syn-slug", "marker-anchored")
    expect("MARKER: an anchored (stated) cell takes the anchors' band", d["marker"] == FULL, str(d["marker"]))
    d = determine(synth_db([{"tier": 3, "evidence_type": "clinical", "scope": "lower_control"}]), 1,
                  {"identity_code": "MOB"}, "syn-slug", "marker-t3-clinical")
    expect("MARKER: T3-clinical alone is provisional and still full (band = evidence, state = status)",
           d["state"] == "provisional" and d["marker"] == FULL, f"{d['state']} {d['marker']}")
    d = determine(synth_db([{"tier": 6, "evidence_type": "code", "jurisdiction": j}
                            for j in ("US", "GB", "AU")]), 1,
                  {"identity_code": "MOB"}, "syn-slug", "marker-floor")
    expect("MARKER: a regulatory-stratum-only floor claim is weak", d["marker"] == WEAK, str(d["marker"]))
    d = determine(synth_db([{"tier": 6, "evidence_type": "code", "jurisdiction": "US"}
                            for _ in range(3)]), 1, {"identity_code": "MOB"}, "syn-slug", "marker-pending")
    expect("MARKER: a pending cell carries none", d["state"] == "pending" and d["marker"] is None,
           f"{d['state']} {d['marker']}")
    d = determine(synth_db(_t6 + _find), 1, {"identity_code": "MOB"}, "syn-slug", "marker-proxy")
    expect("MARKER: a proxy determination is weak unless a study confirms its codes",
           d["marker"] == WEAK, str(d["marker"]))

    # Owner, 2026-10-21: a skimmed or `absent` finding supplies no direction and confirms nothing
    # (a skimmed one cues a dedicated reading); a source must be VERIFIED to earn a band above
    # weak; one confirmed clause does not confirm a code.
    def _with_method(c):
        c.execute("ALTER TABLE source_value_extractions ADD COLUMN extraction_method "
                  "TEXT NOT NULL DEFAULT 'full'")
        return c

    _SKIM = sorted(NOT_PUBLISHABLE_METHODS)[0]
    d = determine(synth_db(_t6 + [dict(_find[0], claim_type="absent")]), 1,
                  {"identity_code": "MOB"}, "syn-slug", "absent-finding")
    expect("DIRECTION: an `absent` finding supplies none, so the cell is a floor claim, not a proxy",
           d["rests_on_proxy_inference"] == 0 and d["regulatory_stratum_only"] == 1
           and d["marker"] == WEAK, f"{d['rests_on_proxy_inference']} {d['regulatory_stratum_only']} {d['marker']}")
    c = _with_method(synth_db(_t6 + _find))
    c.execute("UPDATE source_value_extractions SET extraction_method=? WHERE ref_id='REF-FIND-1'", (_SKIM,))
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "skimmed-finding")
    expect("DIRECTION: a skimmed finding supplies none, and is REPORTED so a dedicated reading is cued",
           d["rests_on_proxy_inference"] == 0 and len(d["skimmed_findings"]) == 1,
           f"{d['rests_on_proxy_inference']} {d['skimmed_findings']}")
    d = determine(synth_db(_t6 + _find), 1, {"identity_code": "MOB"}, "syn-slug", "no-skim")
    expect("DIRECTION: nothing is reported when no finding was skimmed",
           d["rests_on_proxy_inference"] == 1 and d["skimmed_findings"] == [])
    c = _with_method(synth_db(_t6 + _find))
    c.execute("UPDATE source_value_extractions SET extraction_method=? WHERE ref_id='REF-SYN-000'", (_SKIM,))
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "skimmed-claim")
    expect("DIRECTION: a skimmed CLAIM row is not reported as a skimmed finding",
           d["skimmed_findings"] == [], str(d["skimmed_findings"]))
    c = _with_method(synth_db(_t6 + _find))
    c.execute("UPDATE source_value_extractions SET extraction_method=? WHERE ref_id='REF-FIND-1'", (_SKIM,))
    c.execute("UPDATE evidence_sources SET superseded_by_ref_id='REF-NEW' WHERE ref_id='REF-FIND-1'")
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "skimmed-superseded")
    expect("DIRECTION: a skimmed finding of a SUPERSEDED source is not reported (it owes no reading)",
           d["skimmed_findings"] == [] and d["n_findings_left_out"] == 0,
           f"{d['skimmed_findings']} {d['n_findings_left_out']}")

    # The gap a pending cell records names the right absence (a description that names the wrong
    # one is followed). Findings that no longer count must not read as a supersession.
    for _label, _fnd in (("skimmed-only", None), ("absent-only", dict(_find[0], claim_type="absent")),
                         ("counted finding", _find[0])):
        c = _with_method(synth_db([_fnd or _find[0]]))
        if _fnd is None:
            c.execute("UPDATE source_value_extractions SET extraction_method=?", (_SKIM,))
        d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "gap-" + _label)
        cause, _remedy = gap_account(d, 1)
        _want = "NONE COUNTS" if _label != "counted finding" else "NONE STATES A VALUE"
        expect(f"GAP: {_label} findings => the gap says '{_want}', never a supersession",
               d["state"] == "pending" and _want in cause and "SUPERSEDED" not in cause,
               f"{d['state']} | {cause}")

    # More ways a pending cell's gap must NOT read as a supersession (nothing was replaced).
    c = _with_method(synth_db([{"tier": 2, "evidence_type": "co2", "figure_role": "condition"}]))
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "gap-condition-only")
    cause, _r = gap_account(d, 1)
    expect("GAP: condition-only rows => neither a supersession nor a value claim",
           d["state"] == "pending" and "SUPERSEDED" not in cause and "supplies a value or a direction" in cause,
           f"{d['state']} | {cause}")
    c = _with_method(synth_db([{"tier": 2, "evidence_type": "co2"}]))
    c.execute("UPDATE source_value_extractions SET extraction_method=?", (_SKIM,))
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "gap-skimmed-claim")
    cause, _r = gap_account(d, 1)
    expect("GAP: a skimmed value row => not a supersession, and the dedicated reading is named",
           d["state"] == "pending" and "SUPERSEDED" not in cause and "skimmed value" in cause,
           f"{d['state']} | {cause}")
    c = synth_db([{"tier": 2, "evidence_type": "co2"}])
    c.execute("UPDATE evidence_sources SET superseded_by_ref_id='REF-NEW'")
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "gap-superseded")
    expect("GAP: when every source behind the extractions IS superseded, it says so",
           "SUPERSEDED" in gap_account(d, 1)[0], gap_account(d, 1)[0])
    c = _with_method(synth_db([dict(_find[0]), dict(_find[0], ref_id="REF-FIND-2")]))
    c.execute("UPDATE source_value_extractions SET extraction_method=? WHERE ref_id='REF-FIND-2'", (_SKIM,))
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "gap-mixed")
    cause, remedy = gap_account(d, 1)
    expect("GAP: a counted finding beside a skimmed one => the remedy still names the dedicated reading",
           "NONE STATES A VALUE" in cause and "owe a dedicated reading" in remedy, f"{cause} | {remedy}")
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical", "verification_status": None}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "null-status")
    expect("VERIFIED: a source with no recorded verification is left out of the marker AND flagged",
           d["marker"] == WEAK and d["has_unverified_sources"] == 1,
           f"{d['marker']} {d['has_unverified_sources']}")

    d = determine(synth_db([{"tier": 2, "evidence_type": "sr_meta", "verification_status": "UNVERIFIED"}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "unverified-sole")
    expect("VERIFIED: a stated cell resting on an unverified source is not full",
           d["state"] == "stated" and d["marker"] == WEAK and d["has_unverified_sources"] == 1,
           f"{d['state']} {d['marker']}")
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical"},
                            {"tier": 2, "evidence_type": "sr_meta", "verification_status": "UNVERIFIED"}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "unverified-one-of-two")
    expect("VERIFIED: an unverified source among verified ones is flagged and left out, so it "
           "neither raises nor lowers the marker",
           d["marker"] == FULL and d["has_unverified_sources"] == 1,
           f"{d['marker']} {d['has_unverified_sources']}")
    d = determine(synth_db(_t6 + [dict(_find[0], verification_status="UNVERIFIED")]), 1,
                  {"identity_code": "MOB"}, "syn-slug", "unverified-direction")
    expect("VERIFIED: a proxy cell whose direction is unverified says so (has_unverified_sources)",
           d["rests_on_proxy_inference"] == 1 and d["has_unverified_sources"] == 1,
           f"{d['rests_on_proxy_inference']} {d['has_unverified_sources']}")

    # R39: a `confirms` edge from an anchoring finding to a governing row confirms it; the row takes
    # the confirming study's band and a code the floor-mean of its rows, and ONLY a code every one
    # of whose governing rows is confirmed leaves weak. The confirming row is a finding of THIS
    # parameter that is neither skimmed nor `absent`; a `tested_at` edge and an edge to a label
    # confirm nothing; an unverified confirmer lends only the weak band.
    def _proxy(relation="confirms", which=slice(None), codes=_t6, to_label=False, confirmer="",
               finding=_find, confirmers_from=("REF-FIND-1",)):
        c = _with_method(synth_db(codes + finding))
        c.executescript("CREATE TABLE extraction_relations (relation_id INTEGER PRIMARY KEY "
                        "AUTOINCREMENT, from_extraction_id INT, relation TEXT, "
                        "to_extraction_id INT, to_label TEXT)")
        from_ids = [c.execute("SELECT MIN(extraction_id) FROM source_value_extractions "
                              "WHERE ref_id=?", (ref,)).fetchone()[0] for ref in confirmers_from]
        if confirmer:   # a SECOND finding row of the same anchoring source holds the edges
            from_ids = [c.execute(
                "INSERT INTO source_value_extractions (ref_id, slug, parameter_id, claim_type, "
                "claimed_value, figure_role, extraction_method) VALUES ('REF-FIND-1','syn-slug',?,?,'x',"
                "'finding',?)", (2 if confirmer == "other-parameter" else 1,
                                 "absent" if confirmer.startswith("absent") else "qualitative",
                                 _SKIM if confirmer in ("skimmed", "absent-skimmed") else "full")).lastrowid]
        code_rows = [r[0] for r in c.execute(
            "SELECT extraction_id FROM source_value_extractions WHERE ref_id NOT LIKE 'REF-FIND%' "
            "ORDER BY extraction_id")]
        for eid in code_rows[which]:
            for find_id in from_ids:
                c.execute("INSERT INTO extraction_relations (from_extraction_id, relation, "
                          "to_extraction_id, to_label) VALUES (?,?,?,?)",
                          (find_id, relation, None if to_label else eid,
                           "a code" if to_label else None))
        d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "marker-confirm")
        assert d["rests_on_proxy_inference"] == 1, "fixture lost its proxy determination"
        return d["marker"]

    two_rows = [dict(c, extractions=2) for c in _t6]
    expect("R39: every governing code confirmed by a full-band study => the cell is full",
           _proxy() == FULL)
    expect("R39: two of three codes confirmed => the floor of the mean, partial",
           _proxy(which=slice(2)) == PARTIAL)
    expect("R39: a tested_at edge confirms nothing", _proxy("tested_at") == WEAK)
    expect("R39: a confirms edge whose referent is a label, not a row, confirms nothing",
           _proxy(to_label=True) == WEAK)
    expect("R39: a skimmed confirming row confirms nothing", _proxy(confirmer="skimmed") == WEAK)
    expect("R39: an `absent` row CONFIRMS through its confirms edge: a study that tested the existing "
           "value and found no case to change it supports that value (owner 2026-10-21, REF-00980)",
           _proxy(confirmer="absent") == FULL)
    expect("R39: ...but the REF-00980 row as stored today is absent AND skimmed, so it confirms nothing "
           "until the paper is read in full", _proxy(confirmer="absent-skimmed") == WEAK)
    expect("R39: a confirming row of another parameter confirms nothing",
           _proxy(confirmer="other-parameter") == WEAK)
    expect("R39: an unverified confirming source lends only the weak band",
           _proxy(finding=[dict(_find[0], verification_status="UNVERIFIED")]) == WEAK)
    expect("R39: every clause of every code confirmed => full",
           _proxy(codes=two_rows) == FULL)
    expect("R39: one confirmed clause of two does not confirm the code (the floor of its rows: partial)",
           _proxy(codes=two_rows, which=slice(None, None, 2)) == PARTIAL)
    _find_t3 = {"tier": 3, "evidence_type": "clinical", "scope": "lower_control",
                "ref_id": "REF-FIND-3", "figure_role": "finding", "claim_type": "qualitative",
                "claimed_value": "x"}
    expect("R39: a confirms edge from a source that is not at an anchoring tier confirms nothing",
           _proxy(finding=_find + [_find_t3], confirmers_from=("REF-FIND-3",)) == WEAK)
    expect("R39: an unverified second confirmer is left out, so more evidence never lowers the marker",
           _proxy(finding=_find + [dict(_find[0], ref_id="REF-FIND-2", verification_status="UNVERIFIED")],
                  confirmers_from=("REF-FIND-1", "REF-FIND-2")) == FULL)
    expect("VERIFIED: a code that is not verified earns nothing even when a verified study confirms "
           "it (a cell with no verified governing source is weak)",
           _proxy(codes=[dict(c, verification_status="UNVERIFIED") for c in _t6]) == WEAK)
    expect("R39: codes are weighed per code, not per clause (5 confirmed clauses of one code beside "
           "two unconfirmed codes stay weak; weighing clauses would give partial)",
           _proxy(codes=[dict(_t6[0], extractions=5), _t6[1], _t6[2]], which=slice(5)) == WEAK)

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

    # band() and floor_mean(): tier-system section 5, and the owner's five rows of 2026-09-13.
    from schemas.enums import EvidenceMarker as M  # noqa: E402
    from schemas.tier_derivation import band, floor_mean  # noqa: E402
    T1, T4, T6 = band(1, "clinical"), band(4, "standard_eb"), band(6, "code")
    expect("BAND: section 5 reads off (tier, evidence_type)",
           [band(1, "co1"), band(2, "sr_meta"), band(2, "co2"), band(3, "clinical"),
            band(5, "national_fw"), band(3, "grey"), band(3, "standard_eb")]
           == [M.FULL] * 4 + [M.PARTIAL, M.WEAK, M.WEAK] and (T1, T4, T6) == (M.FULL, M.PARTIAL, M.WEAK))
    expect("BAND: floor_mean reproduces the owner's five rows (2 x T1 + T4 is the acceptance case)",
           [floor_mean(x) for x in ([T1, T1, T4], [T1] * 3, [T1, T1, T6], [T1, T6, T6], [T1] * 99 + [T4])]
           == [M.PARTIAL, M.FULL, M.PARTIAL, M.WEAK, M.PARTIAL])

    if FAILED:
        print(f"\nFAIL: {len(FAILED)} test(s): {FAILED}")
        sys.exit(1)
    print("\nPASS: all pilot-engine branch tests")


if __name__ == "__main__":
    main()
