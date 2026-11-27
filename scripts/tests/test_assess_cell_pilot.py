#!/usr/bin/env python3
"""
scripts/tests/test_assess_cell_pilot.py — unit tests for the pilot determination
engine's doctrinal branches that have NO real cell in the corpus (adversarial
finding 2 established that PILOT-MANIFEST.md previously claimed these tests
existed when they did not; this file makes the claim true).

Branches covered here, each against a synthetic in-memory DB:
  - pure Co-2-only basis  -> stated, tier_basis CO2 (§2.2 condition 3)
  - pure T6-only, >=3 distinct jurisdictions -> provisional + code_floor_only
    + regulatory_stratum_only (G1); design_scale population, read off the key (OD-48)
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

from assess_cell import (  # noqa: E402
    NOT_PUBLISHABLE_METHODS, RULE_VERSION, STORED_ANSWER, OpenQuestion, Refusal, derivation_handshake, determine, gap_account, population_match,
    scan_command, stale_determinations, validate_lens)
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
             icf_links=(), gates=(), direction=None, row_lens=({"identity_code": "MOB"},), family=(), icf_family=()):
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

    A source may carry `extraction_method` (the column exists only when some source does, as it
    does not in the oldest fixtures) and `superseded_by_ref_id`.

    LENS (T-019). The engine reads a figure's lens only from `v_live_lens_links` (T-018), so the
    fixture holds the retired lens columns of `source_value_extractions` no longer and writes one
    link row per entry of the source's `lenses` key, defaulting to `row_lens` (most cases are
    stated in `MOB`). Each entry is a dict of the link's three code columns.
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
        claim_type TEXT, claimed_value TEXT, claimed_unit TEXT,
        figure_role TEXT, comparator TEXT);
      -- T-019: the figure's lens lives in the link table (T-018) and is read through the live view,
      -- the only columns of it the engine reads.
      CREATE TABLE extraction_lens_links (
        link_id INTEGER PRIMARY KEY AUTOINCREMENT, extraction_id INT, identity_code TEXT,
        icf_code TEXT, needs_code TEXT, retired_at TEXT);
      CREATE VIEW v_live_lens_links AS
        SELECT link_id, extraction_id, identity_code, icf_code, needs_code
          FROM extraction_lens_links WHERE retired_at IS NULL;
      CREATE TABLE evidence_population_match (
        match_id TEXT, ref_id TEXT, match_grade TEXT, target_population TEXT);
      -- 080. CREATED UNCONDITIONALLY, EVEN EMPTY, for the reason this docstring
      -- already gives about source_slug_links: a fixture laxer than the database it
      -- stands for is how an engine passes its tests and fails on replay. An empty
      -- identity_icf_map is also the honest default -- it is what a cell whose
      -- identity lens has no promoted functional mapping actually looks like.
      CREATE TABLE identity_icf_map (
        retired_at TEXT,
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
      CREATE TABLE base_taxonomy_identity (identity_code TEXT PRIMARY KEY,
        parent_code TEXT REFERENCES base_taxonomy_identity(identity_code));
      CREATE TABLE base_icf (icf_code TEXT PRIMARY KEY, parent_code TEXT REFERENCES base_icf(icf_code));
      CREATE TABLE determination_gates (
        gate_id INTEGER PRIMARY KEY AUTOINCREMENT, parameter_id INTEGER,
        identity_code TEXT, icf_code TEXT, needs_code TEXT,
        verdict TEXT, trigger_ref_id TEXT, trigger_tier INT,
        trigger_evidence_type TEXT, detail TEXT, raised_at TEXT, raised_by_session TEXT,
        resolved_at TEXT, resolved_by_session TEXT, resolution_rationale TEXT);
      CREATE VIEW v_open_determination_gates AS
        SELECT g.gate_id, g.parameter_id, g.identity_code, g.icf_code, g.needs_code,
               g.verdict, g.trigger_ref_id,
               g.trigger_tier, g.trigger_evidence_type, g.detail, g.raised_at,
               g.raised_by_session
          FROM determination_gates g WHERE g.resolved_at IS NULL;
    """)
    # T-030: the engine reads units from `base_units` (and each unit's kind from `base_quantity_kinds`). The fixture takes
    # the live schema and rows of both, so it is no laxer than the database it stands for and a unit added by migration
    # reaches every case that states one.
    _live = sqlite3.connect(f"file:{os.environ.get('GUIDEBOOK_DB_PATH') or os.path.join(REPO_ROOT, 'data', 'guidebook.db')}?mode=ro", uri=True)
    try:
        for _t in ("base_quantity_kinds", "base_units"):
            for _ddl, in _live.execute("SELECT sql FROM sqlite_master WHERE tbl_name=? AND sql IS NOT NULL "
                                       "ORDER BY type DESC", (_t,)):
                conn.execute(_ddl)
            _cur = _live.execute(f"SELECT * FROM {_t}")
            conn.executemany(f"INSERT INTO {_t} VALUES ({','.join('?' * len(_cur.description))})", _cur.fetchall())
    finally:
        _live.close()
    has_method = any("extraction_method" in s for s in sources)
    if has_method:
        conn.execute("ALTER TABLE source_value_extractions ADD COLUMN extraction_method "
                     "TEXT NOT NULL DEFAULT 'full'")
    if direction:
        conn.execute("INSERT INTO base_parameters (parameter_id, term_id, status, "
                     "accessibility_direction, direction_rationale) "
                     "VALUES (?, 'TERM-SYN', 'active', ?, 'synthetic fixture')",
                     (parameter_id, direction))
    for L in icf_links:
        conn.execute("INSERT INTO identity_icf_map (identity_code, icf_code, "
                     "mechanism, mapping_confidence, provenance) VALUES (?,?,?,?,?)", L)
    for child, parent in family:             # (child, parent) identity codes; empty by default, so every code is a root
        for code in (parent, child):
            conn.execute("INSERT OR IGNORE INTO base_taxonomy_identity (identity_code) VALUES (?)", (code,))
        conn.execute("UPDATE base_taxonomy_identity SET parent_code = ? WHERE identity_code = ?", (parent, child))
    for child, parent in icf_family:         # (child, parent) ICF codes; empty by default, so every code is a root (OD-75)
        for code in (parent, child):
            conn.execute("INSERT OR IGNORE INTO base_icf (icf_code) VALUES (?)", (code,))
        conn.execute("UPDATE base_icf SET parent_code = ? WHERE icf_code = ?", (parent, child))
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
                      s.get("jurisdiction"), s.get("superseded_by_ref_id")))
        conn.execute("INSERT INTO source_slug_links VALUES (?, 'syn-slug')", (ref,))
        for _ in range(s.get("extractions", extractions_per_source)):
            eid = conn.execute(
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
                "(ref_id, slug, parameter_id, claim_type, claimed_value, "
                " claimed_unit, figure_role, comparator"
                + (", extraction_method" if has_method else "") + ") "
                "VALUES (?, 'syn-slug', ?, ?, ?, ?, ?, ?" + (", ?" if has_method else "") + ")",
                (ref, parameter_id,
                 s.get("claim_type", "numerical"),
                 s.get("claimed_value", "1"),
                 s.get("claimed_unit"),
                 s.get("figure_role", "claim"),
                 s.get("comparator"),
                 *((s.get("extraction_method", "full"),) if has_method else ()))).lastrowid
            for lens in s.get("lenses", row_lens):
                link_lens(conn, eid, lens)
    return conn


def link_lens(conn, extraction_id, lens):
    """One live link row for a fixture figure, carrying the codes of `lens` (a dict)."""
    conn.execute("INSERT INTO extraction_lens_links (extraction_id, identity_code, icf_code, "
                 "needs_code) VALUES (?,?,?,?)",
                 (extraction_id, lens.get("identity_code"), lens.get("icf_code"),
                  lens.get("needs_code")))


FAILED = []


_EXPECTED = []


def expect(label, cond, detail=""):
    _EXPECTED.append(label)
    print(f"  {'PASS' if cond else 'FAIL'}: {label}" + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILED.append(label)


# ── T-117 (the marker table) and T-056 item 3a (design_scale from the key) ─────────────────────
# Each case names the defect it goes red on. A T4-T6-only fixture reaches `provisional` only above the
# section 2.3 richness (one T4, or three VERIFIED T6 in three jurisdictions); below it the cell is
# `pending` before and after and the case could not go red, so every engine case carries a T4.
_R = "rise:run ratio"


def _src(tier, value, verified=True, jur=None, ref=None):
    s = {"tier": tier, "evidence_type": {4: "standard_eb", 5: "national_fw", 6: "code"}[tier],
         "claimed_value": value, "claimed_unit": _R, "comparator": "<=", "jurisdiction": jur or f"J{tier}",
         "verification_status": "VERIFIED" if verified else "UNVERIFIED"}
    if ref:
        s["ref_id"] = ref
    return s


def _det(sources, lens=None, row_lens=None):
    lens = lens or {"identity_code": "MOB"}
    return determine(synth_db(sources, direction="lower_is_better", row_lens=(row_lens or lens,)),
                     1, lens, "syn-slug", "t117")


def _refused(sources):
    """The refusal text, or None when the engine wrote an answer (its marker is then in the detail)."""
    try:
        d = _det(sources)
    except Refusal as exc:
        return str(exc), None
    return None, d


def t117_t056_cases():
    import assess_cell as _ac
    from schemas import tier_derivation as _td
    W = getattr(EvidenceMarker, "WARNING", None)

    # T117-01: red on the regulatory-only override (a T4-only cell shown ○; owner: "T4 only half circle").
    d = _det([_src(4, "1:12")])
    expect("T117-01: one VERIFIED T4 states the value => ◐ (red: the override gives ○)",
           d["state"] == "provisional" and d["marker"] == PARTIAL, f"{d['state']} {d['marker']}")
    # T117-02: red on band() T5 → PARTIAL (the table: ○ T5, T6).
    expect("T117-02: band(5, national_fw) is ○ (red: ◐)",
           _td.band(5, "national_fw") == EvidenceMarker.WEAK, str(_td.band(5, "national_fw")))
    # T117-03: red on band() T3 clinical → FULL (OD-57: ◐ T3), and on a grey basis getting a circle (OD-64).
    expect("T117-03: band(3, clinical) is ◐ (red: ●)",
           _td.band(3, "clinical") == EvidenceMarker.PARTIAL, str(_td.band(3, "clinical")))
    _own = getattr(_ac, "own", None)
    _g = _own({"ref_id": "G", "tier": 3, "evidence_type": "grey", "verification_status": "VERIFIED"}) \
        if callable(_own) else None
    expect("T117-03: own() of a grey source is ⚠, U+26A0 alone, no U+FE0F (red: no module-level own(), "
           "no warning marker)",
           _g is not None and _g.value == "\u26a0" and "\ufe0f" not in _g.value, repr(_g))
    # T117-04: red on an unverified stating source being given a circle (OD-99 Q1 and OD-100 decided by code).
    txt, d = _refused([_src(4, "1:20", verified=False, ref="REF-U4"), _src(4, "1:12", jur="J4b")])
    expect("T117-04: an UNVERIFIED source stating the shown value alone => Refusal naming OD-99 and OD-100, "
           "not OD-92 (red: a circle is written)",
           txt is not None and "OD-99" in txt and "OD-100" in txt and "OD-92" not in txt and "REF-U4" in txt,
           txt or f"answered {d['state']} {d['marker']}")
    # T117-05: red on the old CHECK (refuses ⚠ and ◐ with rso 1); guards on ● with rso 1 and on the emoji form.
    _db = os.environ.get("GUIDEBOOK_DB_PATH") or os.path.join(REPO_ROOT, "data", "guidebook.db")
    _live = sqlite3.connect(f"file:{_db}?mode=ro", uri=True)
    _ddl = _live.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='specifications'").fetchone()[0]
    _live.close()

    def _try(marker, rso):
        m = sqlite3.connect(":memory:")
        m.execute(_ddl)
        try:
            m.execute("INSERT INTO specifications (parameter_id, identity_code, state, marker, "
                      "regulatory_stratum_only) VALUES (1, 'MOB', 'provisional', ?, ?)", (marker, rso))
            return True
        except sqlite3.IntegrityError:
            return False
    expect("T117-05: the specifications CHECK accepts ⚠ (red: refused)", _try("\u26a0", 0))
    expect("T117-05: the specifications CHECK accepts ◐ with regulatory_stratum_only = 1 (red: refused)",
           _try(PARTIAL, 1))
    expect("T117-05: guard, ● with regulatory_stratum_only = 1 is refused", not _try(FULL, 1))
    expect("T117-05: guard, the emoji form ⚠ + U+FE0F is refused", not _try("\u26a0\ufe0f", 0))
    # T117-06: red on the floor mean over every governing source (OD-59: "its own").
    d = _det([_src(4, "1:20"), _src(6, "1:12")])
    expect("T117-06: T4 states 1:20, T6 states 1:12, lower is better => 5 %, ◐ from the stating T4 "
           "(red: ○)", d["state"] == "provisional" and d["value_max"] is not None
           and abs(d["value_max"] - 5) < 1e-9 and d["marker"] == PARTIAL,
           f"{d['state']} {d['value_max']} {d['marker']}")
    # T117-07: red on an answer being written; and on a refusal naming only the first blocking question.
    txt, d = _refused([_src(6, "1:20", verified=False, ref="REF-U6"), _src(6, "1:20", jur="J6b"),
                       _src(4, "1:12")])
    expect("T117-07: an UNVERIFIED and a VERIFIED T6 both state the shown value => one Refusal naming "
           "OD-99, OD-100 and OD-92 (red: a circle is written)",
           txt is not None and all(q in txt for q in ("OD-99", "OD-100", "OD-92")),
           txt or f"answered {d['state']} {d['marker']}")
    # T117-08: red on the best (or any) circle being chosen among stating sources with different markers.
    txt, d = _refused([_src(4, "1:20"), _src(6, "1:20")])
    expect("T117-08: a VERIFIED T4 and a VERIFIED T6 both state the shown value => Refusal naming OD-92, "
           "not OD-99 (red: a circle is written)",
           txt is not None and "OD-92" in txt and "OD-99" not in txt,
           txt or f"answered {d['state']} {d['marker']}")
    # T117-09: kills "refuse on any unverified governing source" and "drop a retrieved-UNVERIFIED source"
    # (OD-99 Meanwhile, first bullet); red today only on the override's ○.
    txt, d = _refused([_src(4, "1:20"), _src(6, "1:12", verified=False, ref="REF-U6N")])
    expect("T117-09: an UNVERIFIED T6 that governs without stating the value => no refusal, ◐, still "
           "governing", txt is None and d["marker"] == PARTIAL and "REF-U6N" in d["governing_refs"],
           txt or f"{d['marker']} {d['governing_refs']}")
    # T117-12: red on a warning marker that is absent, or that is an ordinary member with an ordinal.
    expect("T117-12: EvidenceMarker.WARNING is U+26A0 (red: absent)", W is not None and W.value == "\u26a0",
           repr(W))
    expect("T117-12: the circles keep ● 3, ◐ 2, ○ 1",
           [m.ordinal for m in (EvidenceMarker.FULL, EvidenceMarker.PARTIAL, EvidenceMarker.WEAK)] == [3, 2, 1])
    _raised = False
    if W is not None:
        try:
            W.ordinal
        except Exception:
            _raised = True
    expect("T117-12: the warning marker has no ordinal (red: absent)", _raised)
    _fm = False
    if W is not None:
        try:
            _td.floor_mean([W, EvidenceMarker.FULL])
        except Exception:
            _fm = True
    expect("T117-12: floor_mean refuses the warning marker (red: absent)", _fm)
    expect("T117-12: floor_mean over circles is unchanged (floor of ● and ○ is ◐)",
           _td.floor_mean([EvidenceMarker.FULL, EvidenceMarker.WEAK]) == EvidenceMarker.PARTIAL)
    # T056-01: red on the G1 line writing `universal` from the stratum (OD-48 "whom it is for").
    d = _det([_src(6, "1:12", jur=j) for j in ("US", "GB", "AU")])
    expect("T056-01: a G1 cell keyed on an identity => population (red: universal)",
           d["state"] == "provisional" and d["design_scale"] == "population", f"{d['state']} {d['design_scale']}")
    # T056-02: red on an anchored cell keyed on an ICF code only reading `population` (it names no group).
    d = determine(synth_db([{"tier": 2, "evidence_type": "co2"}, {"tier": 2, "evidence_type": "co2"}],
                           row_lens=({"icf_code": "d450"},)), 1, {"icf_code": "d450"}, "syn-slug", "t056-02")
    expect("T056-02: an anchored cell keyed on an ICF code only => universal (red: population)",
           d["state"] in ("stated", "provisional") and d["design_scale"] == "universal",
           f"{d['state']} {d['design_scale']}")
    t117_c10_cases()


def t117_c10_cases():
    """T117-11: C10 on a temporary copy of the live database, one seeded live cell per case. The
    canonical C10 subject is the live published cells, of which there may be none, so each case seeds
    one; the cell's sources are derived by query, never typed. (d) is seeded with
    ignore_check_constraints so its red state is C10's verdict, not the marker CHECK's."""
    import contextlib, io, shutil, tempfile
    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "tests"))
    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "research"))
    import test_db_integrity as tdi
    import retrieval_log as rl
    src = os.environ.get("GUIDEBOOK_DB_PATH") or os.path.join(REPO_ROOT, "data", "guidebook.db")
    ro = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    _saved = rl.LOG_ROOT            # cwd-relative unless GUIDEBOOK_RETRIEVAL_LOG is set: read from the repository root
    if not _saved.is_absolute():
        rl.LOG_ROOT = rl.Path(REPO_ROOT) / _saved
    try:
        recs = rl.all_manifest_records()
    finally:
        rl.LOG_ROOT = _saved
    not_got = ("corroborated-not-retrieved", "citing-bibliography")
    pid = 3   # a parameter with live rows from every kind of source below; asserted, not assumed
    rows = ro.execute(
        "SELECT ref_id, tier, verification_status, verification_method, url, doi, standard_number "
        "FROM evidence_sources WHERE ref_id IN (SELECT ref_id FROM source_value_extractions "
        "WHERE parameter_id = ? AND retired_at IS NULL) ORDER BY ref_id", (pid,)).fetchall()
    got = {r[0]: bool(rl.manifest_lines_for(r[0], r[4], r[5], recs)) and r[3] not in not_got for r in rows}
    verified = [r[0] for r in rows if r[2] == "VERIFIED"]
    retrieved_unv = [r[0] for r in rows if r[2] != "VERIFIED" and got[r[0]] and r[1] >= 4]
    unretrieved_noroute = [r[0] for r in rows if r[2] != "VERIFIED" and not got[r[0]] and r[1] >= 4 and not r[6]]
    ro.close()
    if not (verified and retrieved_unv and unretrieved_noroute):
        expect("T117-11: fixture sources derivable on parameter 3", False,
               f"verified={verified[:1]} retrieved_unverified={retrieved_unv[:1]} unretrieved={unretrieved_noroute[:1]}")
        return

    def c10(refs, marker, seed=None):
        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, "c10.db")
        shutil.copy(src, path)
        c = sqlite3.connect(path)
        c.execute("PRAGMA ignore_check_constraints = ON")
        sid = c.execute("INSERT INTO specifications (parameter_id, identity_code, state, design_scale, marker, "
                        "regulatory_stratum_only, rule_version) VALUES (?, 'MOB', 'provisional', 'population', ?, 0, "
                        "'t117-11')", (pid, marker)).lastrowid
        c.executemany("INSERT INTO specification_source_links (specification_id, ref_id) VALUES (?, ?)",
                      [(sid, r) for r in refs])
        if seed:
            seed(c)
        c.commit()
        c.close()
        tdi.results.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            tdi.run_checks(path)
        shutil.rmtree(tmp, ignore_errors=True)
        r = [x for x in tdi.results if x["id"] == "C10"]
        return (r[0]["passed"], r[0]["subject"]) if r else (None, None)

    ok, n = c10([verified[0], retrieved_unv[0]], WEAK)
    expect("T117-11(a): a retrieved-UNVERIFIED governing source beside a VERIFIED one under ○ passes C10 "
           "(red: C10 refuses every non-VERIFIED source)", ok is True and n and n >= 1, f"passed={ok} subject={n}")
    ok, n = c10([verified[0], unretrieved_noroute[0]], WEAK)
    expect("T117-11(b): guard, an unretrieved source with no standard_number fails C10", ok is False,
           f"passed={ok} subject={n}")
    ok, n = c10([retrieved_unv[0]], WEAK)
    expect("T117-11(c): guard, every governing source non-VERIFIED under a circle fails C10", ok is False,
           f"passed={ok} subject={n}")
    ref_d = unretrieved_noroute[0]

    def _route(c):
        c.execute("UPDATE evidence_sources SET standard_number = 'T117-11' WHERE ref_id = ?", (ref_d,))
        c.execute("UPDATE source_value_extractions SET loc_clause = COALESCE(loc_clause, '1') "
                  "WHERE ref_id = ? AND parameter_id = ?", (ref_d, pid))
    ok, n = c10([ref_d], "\u26a0", seed=_route)
    expect("T117-11(d): an unretrieved source with a route, sole governing, under ⚠ passes C10 "
           "(red: C10 refuses every non-VERIFIED source)", ok is True, f"passed={ok} subject={n}")


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
    # T-056 item 3a (OD-48, "whom it is for"): the scale is read off the key, and this cell names MOB.
    expect("T6-only keyed on an identity => design_scale population", d["design_scale"] == "population")
    expect("T6-only never stated", d["state"] != "stated")

    # 3. T6-only, one jurisdiction x3 -> pending (jurisdiction distinctness)
    d = determine(synth_db([{"tier": 6, "evidence_type": "code", "jurisdiction": "US"}
                            for _ in range(3)], row_lens=({"identity_code": "DEM"},)),
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

    # 3e. ("US","US-CA") -- OD-04: a sub-national code counts toward its country, read from
    # base_jurisdictions.parent_code. One jurisdiction, not two; and with the table absent the
    # engine is unchanged (the same two sources count as two, as in 3d).
    def _with_registry(c, rows):
        c.execute("CREATE TABLE base_jurisdictions (jurisdiction_code TEXT PRIMARY KEY, "
                  "kind TEXT, parent_code TEXT)")
        c.executemany("INSERT INTO base_jurisdictions VALUES (?,?,?)", rows)
        return c
    _reg = [("US", "country", None), ("CA", "country", None), ("US-CA", "sub-national", "US")]
    d = determine(_with_registry(synth_db([{"tier": 5, "evidence_type": "national_fw",
                                            "jurisdiction": j} for j in ("US", "US-CA")]), _reg),
                  1, {"identity_code": "MOB"}, "syn-slug", "t45-sub-national")
    expect("T4-5(US, US-CA) => NOT rich (a sub-national code counts toward its country)",
           d["state"] != "provisional", d["state"])
    d = determine(_with_registry(synth_db([{"tier": 5, "evidence_type": "national_fw",
                                            "jurisdiction": j} for j in ("US-CA", "CA")]), _reg),
                  1, {"identity_code": "MOB"}, "syn-slug", "t45-sub-national-control")
    expect("T4-5(US-CA, CA) => rich (two countries, one reached through its sub-national code)",
           d["state"] == "provisional", d["state"])
    d = determine(synth_db([{"tier": 5, "evidence_type": "national_fw", "jurisdiction": j}
                            for j in ("US", "US-CA")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "t45-no-registry")
    expect("T4-5(US, US-CA) with no registry table => rich (unchanged: the engine splits no strings)",
           d["state"] == "provisional", d["state"])

    # 4. All sources disqualified -> pending + flag (§2.8)
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical",
                             "verification_status": "UNVERIFIED-CLOSED"}],
                           row_lens=({"identity_code": "NEU"},)),
                  1, {"identity_code": "NEU"}, "syn-slug", "disqualified")
    expect("all-disqualified => pending", d["state"] == "pending", d["state"])
    expect("all_sources_disqualified flag set", d["all_sources_disqualified"] == 1)

    # 5. UNVERIFIED present -> has_unverified_sources (§2.8)
    d = determine(synth_db([{"tier": 2, "evidence_type": "sr_meta"},
                            {"tier": 6, "evidence_type": "code",
                             "verification_status": "UNVERIFIED"}],
                           row_lens=({"identity_code": "DEM"},)),
                  1, {"identity_code": "DEM"}, "syn-slug", "unverified-present")
    expect("UNVERIFIED => has_unverified_sources=1", d["has_unverified_sources"] == 1)
    expect("anchored despite unverified T6", d["state"] == "stated", d["state"])

    # 5b. A cell stated in NO identity lens leaves population-directness NOT_ASSESSED.
    # New with the 071 re-key: evidence_population_match.target_population is written in
    # identity terms only, so a determination stated in ICF / access-need terms
    # alone has nothing to attribute a match row TO. G2 says that dimension is unassessed,
    # not absent — it caps consolidation at DOWN-WEIGHTED and flags the source. The old
    # engine could not reach this state at all, because population was mandatory.
    d = determine(synth_db([{"tier": 1, "evidence_type": "clinical"}],
                           row_lens=({"icf_code": "AX-AMB"},)),
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
                 "(ref_id, slug, parameter_id, claim_type, claimed_value) "
                 "VALUES ('REF-SYN-OTHER','syn-slug', 2, 'numerical','9')")
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
    expect("B4c: 1:N fan-out reports all four extractions", d["n_extractions_in_lens"] == 4,
           str(d["n_extractions_in_lens"]))
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

    # B5a-2. A parameter with no extraction at all has no cell: the engine refuses and writes
    # nothing (OD-08, an absent cell has no row; T-019). This case used to expect a `pending` row
    # with a gap whose text named the unread parameter; that row is the defect OD-08 closes.
    try:
        determine(synth_db([]), 1, {"identity_code": "MOB"}, "syn-slug", "nothing extracted")
        _refused = None
    except Refusal as e:
        _refused = str(e)
    expect("B5a: no extraction for the parameter => refused, no row (OD-08)",
           _refused is not None and "has no row" in _refused, str(_refused))

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

    # 8g2. T-021 (OD-21): a QUESTION about a published cell is an open gate that FLAGS the cell and never caps it.
    _Q = "a reader asks whether the 5% in this cell is right for a user of a long cane"
    def _gate_rows(conn, *rows):
        for lens_cols, verdict, tier, etype, detail in rows:
            cols = ["parameter_id", "verdict", "trigger_tier", "trigger_evidence_type", "detail", "raised_at",
                    "raised_by_session", *lens_cols]
            conn.execute(f"INSERT INTO determination_gates ({','.join(cols)}) VALUES "
                         f"({','.join('?' * len(cols))})",
                         [1, verdict, tier, etype, detail, "2026-11-15", "syn", *lens_cols.values()])
    c = synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK)
    _gate_rows(c, ({"identity_code": "MOB"}, "QUESTION", None, None, _Q))
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "question")
    _qs = [g for g in d["gates"] if g.get("question")]
    expect("T021-01: a QUESTION on the cell leaves a stated cell stated", d["state"] == "stated", d["state"])
    expect("T021-02: the cell's report carries the question, not binding, with its words and no tier",
           len(d["gates"]) == 1 and len(_qs) == 1 and not _qs[0]["binds"] and _qs[0]["why"] == _Q
           and _qs[0]["trigger_tier"] is None and _qs[0]["verdict"] == "QUESTION", str(d["gates"]))
    c = synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK)
    _gate_rows(c, ({"identity_code": "MOB"}, "QUESTION", None, None, _Q),
               ({"identity_code": "MOB"}, "MISLINKED", 1, "primary_research", "population links omit DEAF"))
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "question+binding")
    expect("T021-03: a QUESTION beside a binding gate does not stop the binding gate capping the cell, and both are reported",
           d["state"] == "provisional" and sorted((g["verdict"], g["binds"]) for g in d["gates"])
           == [("MISLINKED", True), ("QUESTION", False)], str(d["gates"]))
    c = synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK)
    _gate_rows(c, ({"icf_code": "ICF-A"}, "QUESTION", None, None, "q-a"),
               ({"needs_code": "NEED-A"}, "QUESTION", None, None, "q-n"),
               ({"identity_code": "MOB", "icf_code": "ICF-A"}, "QUESTION", None, None, "q-ma"))
    _flag = lambda lens: sorted(g["why"] for g in derivation_handshake(c, 1, lens, [dict(T1)])[4])  # noqa: E731
    _all = ["q-a", "q-ma", "q-n"]
    expect("T021-04: a gate is skipped only when the cell carries a DIFFERENT code in a lens the gate names "
           "(a lens the cell does not carry never skips it, as before)",
           _flag({"icf_code": "ICF-A"}) == _all and _flag({"icf_code": "ICF-B"}) == ["q-n"]
           and _flag({"needs_code": "NEED-B"}) == ["q-a", "q-ma"]
           and _flag({"identity_code": "MOB", "icf_code": "ICF-A"}) == _all
           and _flag({"identity_code": "OTHER"}) == ["q-a", "q-n"],
           str([_flag({"icf_code": "ICF-A"}), _flag({"icf_code": "ICF-B"}), _flag({"needs_code": "NEED-B"})]))
    c.execute("UPDATE determination_gates SET resolved_at='2026-11-15', resolved_by_session='syn', "
              "resolution_rationale='answered' WHERE detail = 'q-a'")
    expect("T021-05: a question closed with a rationale no longer flags the cell",
           "q-a" not in _flag({"icf_code": "ICF-A"}))

    # 8g3. T-054: a RETIRED crossing row is history: the function path the engine reads leaves it out.
    c = synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK)
    _fb_live = derivation_handshake(c, 1, {"identity_code": "MOB"}, [dict(T1)])[0]
    c.execute("UPDATE identity_icf_map SET retired_at='2026-11-15'")
    _fb_ret = derivation_handshake(c, 1, {"identity_code": "MOB"}, [dict(T1)])[0]
    expect("T054-07: a live crossing row gives the cell a functional basis and a retired one does not",
           _fb_live is not None and "d450" in _fb_live and _fb_ret is None, f"{_fb_live} / {_fb_ret}")

    # 8h. Resolution is a NAMED PATH, and the view is what enforces it: a resolved gate
    # stops binding, so no cell sits at provisional with no owner of resolution.
    c = synth_db([dict(T1), dict(T1)], icf_links=MOB_LINK,
                 gates=[(1, "MOB", "UNLINKED", 1, "primary_research", "d")])
    c.execute("UPDATE determination_gates SET resolved_at='2026-09-13', "
              "resolved_by_session='syn', resolution_rationale='adjudicated'")
    d = determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "resolved")
    expect("H4: a resolved gate no longer binds", d["state"] == "stated", d["state"])

    # Three regulatory-stratum codes, and a source that measured the parameter without stating a
    # value for it (owner 2026-09-16): the proxy branch's inputs, and the engine cases of 8i.
    _t6 = [{"tier": 6, "evidence_type": "code", "jurisdiction": j} for j in ("US", "GB", "AU")]
    _find = [{"tier": 1, "evidence_type": "clinical", "ref_id": "REF-FIND-1",
              "figure_role": "finding", "claim_type": "qualitative",
              "claimed_value": "discomfort rises with gradient"}]

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
        for _label, _srcs in (("anchored", [{"tier": 2, "evidence_type": "co2"}]),
                              ("T3-clinical", [{"tier": 3, "evidence_type": "clinical",
                                                "scope": "lower_control"}]),
                              ("floor claim", _t6), ("proxy", _t6 + _find),
                              ("T4-5 floor claim", [{"tier": 5, "evidence_type": "national_fw",
                                                     "jurisdiction": j} for j in ("US", "CA")]),
                              ("pending", [dict(_t6[0]) for _ in range(3)])):
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
    expect("MARKER: T3-clinical alone is provisional and takes the half circle (OD-57: ◐ T3)",
           d["state"] == "provisional" and d["marker"] == PARTIAL, f"{d['state']} {d['marker']}")
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
    expect("DIRECTION: nothing is reported when no finding was skimmed", d["skimmed_findings"] == [])

    # Owner, 2026-10-21: a skimmed or `absent` finding supplies no direction and confirms nothing
    # (a skimmed one cues a dedicated reading); a source must be VERIFIED to earn a band above
    # weak; one confirmed clause does not confirm a code.
    _SKIM = sorted(NOT_PUBLISHABLE_METHODS)[0]
    d = determine(synth_db(_t6 + [dict(_find[0], claim_type="absent")]), 1,
                  {"identity_code": "MOB"}, "syn-slug", "absent-finding")
    expect("DIRECTION: an `absent` finding supplies none, so the cell is a floor claim, not a proxy",
           d["rests_on_proxy_inference"] == 0 and d["regulatory_stratum_only"] == 1
           and d["marker"] == WEAK, f"{d['rests_on_proxy_inference']} {d['regulatory_stratum_only']} {d['marker']}")
    d = determine(synth_db(_t6 + [dict(_find[0], extraction_method=_SKIM)]), 1,
                  {"identity_code": "MOB"}, "syn-slug", "skimmed-finding")
    expect("DIRECTION: a skimmed finding supplies none, and is REPORTED so a dedicated reading is cued",
           d["rests_on_proxy_inference"] == 0 and len(d["skimmed_findings"]) == 1,
           f"{d['rests_on_proxy_inference']} {d['skimmed_findings']}")
    d = determine(synth_db([dict(_t6[0], extraction_method=_SKIM)] + _t6[1:] + _find), 1,
                  {"identity_code": "MOB"}, "syn-slug", "skimmed-claim")
    expect("DIRECTION: a skimmed CLAIM row is not reported as a skimmed finding",
           d["skimmed_findings"] == [], str(d["skimmed_findings"]))
    d = determine(synth_db(_t6 + [dict(_find[0], extraction_method=_SKIM, superseded_by_ref_id="REF-NEW")]),
                  1, {"identity_code": "MOB"}, "syn-slug", "skimmed-superseded")
    expect("DIRECTION: a skimmed finding of a SUPERSEDED source is not reported (it owes no reading)",
           d["skimmed_findings"] == [] and d["n_findings_left_out"] == 0,
           f"{d['skimmed_findings']} {d['n_findings_left_out']}")

    # The gap a pending cell records names the right absence (a description that names the wrong
    # one is followed). Findings that no longer count must not read as a supersession.
    for _label, _fnd in (("skimmed-only", dict(_find[0], extraction_method=_SKIM)),
                         ("absent-only", dict(_find[0], claim_type="absent", extraction_method="full")),
                         ("counted finding", dict(_find[0], extraction_method="full"))):
        d = determine(synth_db([_fnd]), 1, {"identity_code": "MOB"}, "syn-slug", "gap-" + _label)
        cause, _remedy = gap_account(d)
        _want = "NONE COUNTS" if _label != "counted finding" else "NONE STATES A VALUE"
        expect(f"GAP: {_label} findings => the gap says '{_want}', never a supersession",
               d["state"] == "pending" and _want in cause and "SUPERSEDED" not in cause,
               f"{d['state']} | {cause}")

    # More ways a pending cell's gap must NOT read as a supersession (nothing was replaced).
    d = determine(synth_db([{"tier": 2, "evidence_type": "co2", "figure_role": "condition",
                             "extraction_method": "full"}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "gap-condition-only")
    cause, _r = gap_account(d)
    expect("GAP: condition-only rows => neither a supersession nor a value claim",
           d["state"] == "pending" and "SUPERSEDED" not in cause and "supplies a value or a direction" in cause,
           f"{d['state']} | {cause}")
    d = determine(synth_db([{"tier": 2, "evidence_type": "co2", "extraction_method": _SKIM}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "gap-skimmed-claim")
    cause, _r = gap_account(d)
    expect("GAP: a skimmed value row => not a supersession, and the dedicated reading is named",
           d["state"] == "pending" and "SUPERSEDED" not in cause and "skimmed value" in cause,
           f"{d['state']} | {cause}")
    d = determine(synth_db([{"tier": 2, "evidence_type": "co2", "superseded_by_ref_id": "REF-NEW"}]),
                  1, {"identity_code": "MOB"}, "syn-slug", "gap-superseded")
    expect("GAP: when every source behind the extractions IS superseded, it says so",
           "SUPERSEDED" in gap_account(d)[0], gap_account(d)[0])
    d = determine(synth_db([dict(_find[0]), dict(_find[0], ref_id="REF-FIND-2", extraction_method=_SKIM)]),
                  1, {"identity_code": "MOB"}, "syn-slug", "gap-mixed")
    cause, remedy = gap_account(d)
    expect("GAP: a counted finding beside a skimmed one => the remedy still names the dedicated reading",
           "NONE STATES A VALUE" in cause and "owe a dedicated reading" in remedy
           and "REF-FIND-2" in remedy, f"{cause} | {remedy}")
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
    def _proxy_cell(relation="confirms", which=slice(None), codes=_t6, to_label=False, confirmer="",
                    finding=_find, confirmers_from=("REF-FIND-1",), proxy=1, direction=None):
        c = synth_db(codes + [dict(f, extraction_method="full") for f in finding],
                     direction=direction)
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
            link_lens(c, from_ids[0], {"identity_code": "MOB"})   # the confirming row is stated in the cell
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
        assert d["rests_on_proxy_inference"] == proxy, "fixture lost its determination type"
        return c, d

    def _proxy(*a, **k):
        return _proxy_cell(*a, **k)[1]["marker"]

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

    # A confirming source is read apart from the direction set: an `absent` row supplies no
    # direction, so its source is not a direction anchor, yet its `confirms` edge confirms.
    _absent_src = dict(_find[0], ref_id="REF-FIND-2", claim_type="absent")
    expect("R39: an absent-only source confirms the codes beside a counted finding that supplies the "
           "direction (REF-00980's shape)",
           _proxy(finding=_find + [_absent_src], confirmers_from=("REF-FIND-2",)) == FULL)
    expect("R39: ...but an unverified absent-only confirmer lends nothing, and is flagged",
           _proxy(finding=_find + [dict(_absent_src, verification_status="UNVERIFIED")],
                  confirmers_from=("REF-FIND-2",)) == WEAK
           and _proxy_cell(finding=_find + [dict(_absent_src, verification_status="UNVERIFIED")],
                           confirmers_from=("REF-FIND-2",))[1]["has_unverified_sources"] == 1)
    _c, _d = _proxy_cell(finding=[_absent_src], confirmers_from=("REF-FIND-2",), proxy=0)
    expect("R39: with NO counted finding there is no direction, so the cell is a floor claim; confirmed by "
           "the study it reads the study's band and is no longer regulation-only (OR-22b, owner 2026-11-13: "
           "\"The study's own band\")",
           _d["regulatory_stratum_only"] == 0 and _d["marker"] == FULL and _d["skimmed_findings"] == []
           and _d["tier_basis"].endswith("(confirmed_by_study)"),
           f"{_d['regulatory_stratum_only']} {_d['marker']} {_d['tier_basis']}")

    # An unverified Co-1 finding source is no anchor (classify holds it back), so it supplies no
    # direction; it is still an input the answer would turn on, and is flagged.
    _d = determine(synth_db(_t6 + [dict(_find[0], evidence_type="co1", verification_status="UNVERIFIED")]),
                   1, {"identity_code": "MOB"}, "syn-slug", "unverified-co1-finding")
    expect("VERIFIED: an unverified Co-1 finding supplies no direction but is flagged, not dropped silently",
           _d["rests_on_proxy_inference"] == 0 and _d["has_unverified_sources"] == 1,
           f"{_d['rests_on_proxy_inference']} {_d['has_unverified_sources']}")

    # The junction says WHY a finding was left out, and which still owes a reading.
    _d = determine(synth_db(_t6 + [dict(_find[0], extraction_method=_SKIM),
                                   dict(_find[0], ref_id="REF-FIND-2", claim_type="absent"),
                                   dict(_find[0], ref_id="REF-FIND-3"),
                                   dict(_find[0], ref_id="REF-FIND-4", extraction_method=_SKIM,
                                        superseded_by_ref_id="REF-NEW")]),
                   1, {"identity_code": "MOB"}, "syn-slug", "left-out-reasons")
    _by = {l["ref_id"]: l for l in _d["links"]}
    expect("JUNCTION: a skimmed finding says it supplies no direction and owes a dedicated reading",
           _by["REF-FIND-1"]["left_out"] == "skimmed"
           and "owes a dedicated reading" in _by["REF-FIND-1"]["exclusion_reason"])
    expect("JUNCTION: an absent finding says it supplies no direction but may confirm",
           _by["REF-FIND-2"]["left_out"] == "absent"
           and "confirm" in _by["REF-FIND-2"]["exclusion_reason"])
    expect("JUNCTION: a counted finding, and a finding of a superseded source, are not left out",
           _by["REF-FIND-3"]["left_out"] is None and _by["REF-FIND-4"]["left_out"] is None
           and _by["REF-FIND-4"]["superseded"] is True)
    expect("JUNCTION: the report names the source that owes the reading, in a runnable command",
           _d["skimmed_finding_refs"] == ["REF-FIND-1"]
           and "--file-sha256" in scan_command(1) and "--target-parameter-id 1" in scan_command(1))

    # Some, not all, of the extractions belong to a superseded source: the gap says so.
    _d = determine(synth_db([{"tier": 2, "evidence_type": "co2", "superseded_by_ref_id": "REF-NEW"},
                             {"tier": 2, "evidence_type": "co2", "figure_role": "condition"}]),
                   1, {"identity_code": "MOB"}, "syn-slug", "gap-mixed-superseded")
    _cause, _remedy = gap_account(_d)
    expect("GAP: part superseded, part condition => both are named, neither is claimed of the other",
           _d["state"] == "pending" and "1 of the 2 belong to a SUPERSEDED source" in _cause
           and "each that is gathered is a condition" in _cause
           and "superseding source" in _remedy, f"{_cause} | {_remedy}")

    # The stored answer is a cache; the engine is asked again (stale_determinations).
    def _store(c, d):
        """Write the engine's answer into a bare `specifications` table, as main() would."""
        c.executescript("CREATE TABLE specifications (specification_id INTEGER PRIMARY KEY, "
                        "parameter_id INT, identity_code TEXT, icf_code TEXT, needs_code TEXT, "
                        "retired_at TEXT, rule_version TEXT, "
                        + ", ".join(STORED_ANSWER) + ")")
        c.execute("INSERT INTO specifications (parameter_id, identity_code, rule_version, "
                  + ", ".join(STORED_ANSWER) + ") VALUES (1, 'MOB', ?, " + ",".join("?" * len(STORED_ANSWER))
                  + ")", (RULE_VERSION, *[d[f] for f in STORED_ANSWER]))

    _c, _d = _proxy_cell(finding=_find + [_absent_src], confirmers_from=("REF-FIND-2",))
    _store(_c, _d)
    expect("STALE: a determination the engine would write again is not stale",
           stale_determinations(_c) == [], str(stale_determinations(_c)))
    _c.execute("UPDATE evidence_sources SET verification_status='UNVERIFIED' WHERE ref_id='REF-FIND-2'")
    expect("STALE: a confirmer demoted after the answer was written is found, by the marker and the flag",
           stale_determinations(_c) == [(1, ["marker", "has_unverified_sources"])],
           str(stale_determinations(_c)))
    _c, _d = _proxy_cell(direction="lower_is_better",
                         codes=[dict(c, claimed_value=v, claimed_unit="%", comparator="<=")
                                for c, v in zip(_t6, ("8.33", "6", "5"))])
    _store(_c, _d)
    _c.execute("UPDATE source_value_extractions SET comparator='>=' WHERE ref_id='REF-SYN-000'")
    expect("STALE: a comparator corrected after the answer was written is found, by the bounds it composed",
           _d["value_max"] is not None and len(stale_determinations(_c)) == 1
           and "value_max" in stale_determinations(_c)[0][1], str(stale_determinations(_c)))
    _c.execute("UPDATE specifications SET retired_at='2026-10-22'")
    expect("STALE: a retired determination is history, not stale",
           stale_determinations(_c) == [])

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

    # T-030 (OR-10, OD-22, OD-42): units are rows. Probes are chosen by query, never typed: the kind with the most units,
    # its canonical unit (factor 1), a unit of another measuring system, and a unit of a kind that has no relation to it.
    import dbcore as _ac
    from decimal import Decimal
    from fractions import Fraction
    _uc = synth_db([])
    _kind = _uc.execute("SELECT kind_id FROM base_units GROUP BY kind_id ORDER BY COUNT(*) DESC, kind_id LIMIT 1").fetchone()[0]
    _fac = {u: Fraction(n, dn) for u, n, dn in _uc.execute(
        "SELECT unit, factor_numerator, factor_denominator FROM base_units WHERE kind_id = ?", (_kind,))}
    _canon = next(u for u, f in _fac.items() if f == 1)
    _sysof = dict(_uc.execute("SELECT unit, system FROM base_units WHERE kind_id = ?", (_kind,)).fetchall())
    _same = sorted((u for u in _fac if u != _canon and _sysof[u] == _sysof[_canon]), key=_fac.get)   # prefixes of the canonical unit
    _other = sorted((u for u in _fac if _sysof[u] != _sysof[_canon]), key=_fac.get)                  # the other system, smallest first
    _alien = _uc.execute("SELECT unit FROM base_units WHERE kind_id <> ? ORDER BY unit LIMIT 1", (_kind,)).fetchone()[0]
    _w = lambda v, u, k, j: {"tier": 6, "evidence_type": "code", "jurisdiction": j, "claimed_value": v, "claimed_unit": u, "comparator": k}
    # AT-68: the same ceiling stated in three units of one kind composes (it declined before), exactly, on the canonical unit
    _vals = [("6", _same[-1]), ("900", _same[0]), ("7000", _canon)]
    d = determine(synth_db([_w(v, u, "<=", j) for (v, u), j in zip(_vals, ("US", "GB", "AU"))], direction="lower_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-compose")
    _want = min(Fraction(v) * _fac[u] for v, u in _vals)
    expect("T030-01: ceilings stated in three units of one kind compose on the canonical unit, the lowest winning, exactly",
           d["value_max"] == float(_want) and d["value_unit"] == _canon and "different units" not in (d["value_note"] or ""),
           f"max={d['value_max']} want={_want} unit={d['value_unit']} note={d['value_note']!r}")
    _nn = {x["notation"]: x for x in (d["value_notations"] or [])}
    expect("T030-02: every unit a source stated is shown; the unit that wrote the winning bound is marked stated, the others derived",
           set(_nn) == {u for _v, u in _vals}
           and [u for u, x in _nn.items() if x["stated"]] == [u for v, u in _vals if Fraction(v) * _fac[u] == _want],
           str(d["value_notations"]))
    # units of different kinds never convert: a unit of another kind beside the length stays apart
    d = determine(synth_db([_w("1200", _canon, ">=", "US"), _w("5", _alien, ">=", "GB"), _w("6", _alien, ">=", "AU")], direction="higher_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-kinds")
    expect("T030-03: units of different kinds never convert: still refused, naming both",
           d["value_min"] is None and "different units" in (d["value_note"] or ""), str(d["value_note"]))
    # the converter: OD-22 (safe side) and OD-42 (a prefix change is exact)
    _in = _other[0]
    _thirty = 30 * _fac[_in]
    for _bound, _txt, _mark, _label in (("min", "765", _ac.MARK_UP, "a minimum of 30 in is shown at 765 mm, never below the 762 it states"),
                                        ("max", "760", _ac.MARK_DOWN, "a maximum of 30 in is shown at 760 mm, never above the 762 it states"),
                                        (None, "760", _ac.MARK_NEAREST, "a point (no bound) is shown at the nearest 5 mm")):
        _got = _ac.from_canonical(_uc, _thirty, _canon, _bound, {_in})
        expect(f"T030-04: {_label}, and the figure says how it was reached", _got == (_txt, False, _mark), str(_got))
    _got = _ac.from_canonical(_uc, 127 * _fac[_canon], _in, "min", {_canon})
    expect("T030-05: a bound already on the owner's increment is shown unchanged and exact (127 mm is 5 in)",
           _got[:2] == ("5", True), str(_got))
    _got = (_ac.from_canonical(_uc, 100 * _fac[_canon], _in, "min", {_canon}), _ac.from_canonical(_uc, 100 * _fac[_canon], _in, "max", {_canon}))
    expect("T030-06: toward inch-foot a minimum rounds up to the quarter inch and a maximum down (100 mm: 4 in, 3.75 in)",
           [g[:2] for g in _got] == [("4", False), ("3.75", False)], str(_got))
    _got = _ac.from_canonical(_uc, 80 * _fac[_same[0]], _canon, "min", {_same[0]})
    _big = _same[-1]                                      # 1203 of the canonical unit, off the 5 mm grid, shown in the largest prefix unit
    _got2 = _ac.from_canonical(_uc, 1203 * _fac[_canon], _big, "min", {_canon})
    expect("T030-07: a change of metric prefix keeps the source's digits and is exact, never rounded to 5 mm",
           _got[:2] == (str(80 * int(_fac[_same[0]])), True) and _got2[:2] == (str(Decimal(1203) / int(_fac[_big])), True)
           and _got[2] == _got2[2] == _ac.MARK_CONVERTED, f"{_got} {_got2}")
    expect("T030-08: the rounding rule's keys are rows of the live schema (a renamed kind or system cannot disarm it)",
           {k for k, _s in _ac.SHOWN_STEPS} <= {r[0] for r in _uc.execute("SELECT kind_id FROM base_quantity_kinds")}
           and {s_ for _k, s_ in _ac.SHOWN_STEPS} <= _ac.check_values(_uc, "base_units", "system"),
           str(sorted(_ac.SHOWN_STEPS)))
    # end to end: the stored bound stays exact, the shown notations carry the rounding and are marked derived
    d = determine(synth_db([_w("30", _in, ">=", "US"), _w("700", _canon, ">=", "GB"), _w("600", _canon, ">=", "AU")], direction="higher_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-shown")
    _nn = {x["notation"]: x for x in (d["value_notations"] or [])}
    expect("T030-09: the headline minimum is exact (762.0 mm); shown in mm it is 765 (derived, rounded up, inexact), in inches 30 (stated, exact)",
           d["value_min"] == float(_thirty) and _nn[_canon]["min"] == "765" and _nn[_canon]["stated"] is False
           and _nn[_canon]["min_mark"] == _ac.MARK_UP and _nn[_canon]["exact"] is False
           and _nn[_in]["min"] == "30" and _nn[_in]["stated"] is True and _nn[_in]["min_mark"] == _ac.MARK_STATED and _nn[_in]["exact"] is True,
           f"min={d['value_min']} {d['value_notations']}")
    # BOTH bounds, mixed: a floor stated in inches and a ceiling stated in millimetres. No source stated 765 mm or 35.25 in.
    d = determine(synth_db([_w("30", _in, ">=", "US"), _w("900", _canon, "<=", "GB"), _w("700", _canon, ">=", "AU")], direction="higher_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-mixed")
    _nn = {x["notation"]: x for x in (d["value_notations"] or [])}
    expect("T030-09b: with a floor stated in inches and a ceiling stated in mm, each notation marks EACH bound: the mm notation has "
           "765 derived (rounded up) beside 900 stated, the inch notation 30 stated beside 35.25 derived (rounded down); neither is `stated` as a whole",
           (_nn[_canon]["min"], _nn[_canon]["min_mark"], _nn[_canon]["max"], _nn[_canon]["max_mark"]) == ("765", _ac.MARK_UP, "900", _ac.MARK_STATED)
           and (_nn[_in]["min"], _nn[_in]["min_mark"], _nn[_in]["max"], _nn[_in]["max_mark"]) == ("30", _ac.MARK_STATED, "35.25", _ac.MARK_DOWN)
           and _nn[_canon]["stated"] is False and _nn[_in]["stated"] is False, str(d["value_notations"]))
    # a point (the floor and the ceiling are one figure) is shown at the nearest increment, not min up and max down
    d = determine(synth_db([_w("30", _in, "=", "US"), _w("30", _in, "=", "GB"), _w("700", _canon, ">=", "AU")], direction="higher_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-point")
    _nn = {x["notation"]: x for x in (d["value_notations"] or [])}
    expect("T030-11: a point is shown at the nearest increment on both ends (760 mm, not 765 above 760)",
           d["value_min"] == d["value_max"] == float(_thirty) and (_nn[_canon]["min"], _nn[_canon]["max"]) == ("760", "760"),
           f"min={d['value_min']} max={d['value_max']} {d['value_notations']}")
    # a unit is added by data: a row in base_units and the engine composes it, with no edit to any code
    _uc2 = synth_db([_w("3", "task-fixture-unit", "<=", "US"), _w("2500", _canon, "<=", "GB"), _w("2600", _canon, "<=", "AU")], direction="lower_is_better")
    _uc2.execute("INSERT INTO base_units (unit, kind_id, factor_numerator, factor_denominator, figure_form, system, created_at, "
                 "created_by_session) VALUES ('task-fixture-unit', ?, 914400, 1, 'number', NULL, 'TASK-FIXTURE', 'TASK-FIXTURE')", (_kind,))
    d = determine(_uc2, 1, {"identity_code": "MOB"}, "syn-slug", "t030-added")
    expect("T030-12: a unit added as a row composes with the rest of its kind (TASK-FIXTURE: 3 of them are 2743200 canonical units, so 2500 wins)",
           d["value_max"] == 2500.0 and d["value_unit"] == _canon and "different units" not in (d["value_note"] or ""),
           f"max={d['value_max']} note={d['value_note']!r}")

    # T030 repair: every seeded factor is held to its DEFINITION. The definitions are external truths, typed here as exact
    # Fractions (an inch is 25.4 mm by the 1959 agreement, a foot twelve inches, a centimetre 10 mm, a metre 1000 mm; 1:12 is
    # 100/12 percent); WHICH units exist is read from the table, and a unit with no pinned definition fails.
    _PIN = {"mm": Fraction(1), "cm": Fraction(10), "m": Fraction(1000), "in": Fraction(254, 10), "ft": Fraction(3048, 10),
            "%": Fraction(1), "rise:run ratio": Fraction(100)}
    _PIN_READ = [("30", "in", Fraction(762)), ("1", "ft", Fraction(3048, 10)), ("1", "cm", Fraction(10)), ("1", "m", Fraction(1000)),
                 ("1:12", "rise:run ratio", Fraction(100, 12)), ("1:20", "rise:run ratio", Fraction(5)), ("5", "%", Fraction(5))]

    def _pin_defects(c):
        bad = [u for u, n, dn in c.execute("SELECT unit, factor_numerator, factor_denominator FROM base_units")
               if u not in _PIN or Fraction(n, dn) != _PIN[u]]
        return bad + [f"{v} {u}" for v, u, want in _PIN_READ if _ac.to_canonical(c, v, u) != want]
    expect("T030-13: every unit in base_units has a pinned definition and its factor equals it; the figures read as the definitions say",
           _pin_defects(_uc) == [], str(_pin_defects(_uc)))
    _bad = synth_db([])
    _bad.execute("UPDATE base_units SET factor_numerator = 11 WHERE unit = 'cm'")
    _bad.execute("UPDATE base_units SET factor_numerator = 100 WHERE unit = 'm'")
    _bad2 = synth_db([])
    _bad2.execute("UPDATE base_units SET factor_numerator = 127 , factor_denominator = 5 WHERE unit = 'ft'")
    _bad3 = synth_db([])
    _bad3.execute("INSERT INTO base_units VALUES ('task-fixture-unit', ?, 3, 1, 'number', NULL, 'TASK-FIXTURE', 'TASK-FIXTURE', NULL, NULL)", (_kind,))
    expect("T030-13b: the pin goes red on a cm and m seeded wrong, on a foot equal to an inch, and on a unit nobody pinned",
           {"cm", "m"} <= set(_pin_defects(_bad)) and "ft" in _pin_defects(_bad2) and "task-fixture-unit" in _pin_defects(_bad3),
           f"{_pin_defects(_bad)} {_pin_defects(_bad2)} {_pin_defects(_bad3)}")
    # the headline is a converted figure and says so
    _bigu = _same[-1]
    d = determine(synth_db([_w(v, _bigu, "<=", j) for v, j in (("9", "US"), ("10", "GB"), ("11", "AU"))], direction="lower_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-headline")
    expect("T030-14: a headline converted to the canonical unit says in value_note that it is, and from which unit",
           d["value_unit"] == _canon and "converted from the stated" in (d["value_note"] or "") and repr(_bigu) in (d["value_note"] or ""),
           f"{d['value_max']} {d['value_unit']} {d['value_note']!r}")
    d = determine(synth_db([_w(v, _canon, "<=", j) for v, j in (("9", "US"), ("10", "GB"), ("11", "AU"))], direction="lower_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-headline-ctl")
    expect("T030-14b: control: a set stated in the canonical unit carries no conversion note", "converted from" not in (d["value_note"] or ""), str(d["value_note"]))
    # a unit string equal to a kind id is a unit with no row, never the kind: it does not compose, in either order
    expect("T030-15 guard: the kind id is no unit of the table", _ac.unit_kind(_uc, _kind) is None)
    _rows15 = [("5", _kind, "US"), ("8", _canon, "GB"), ("9", _canon, "AU")]
    for _order, _rs in (("as written", _rows15), ("reversed", list(reversed(_rows15)))):
        d = determine(synth_db([_w(v, u, "<=", j) for v, u, j in _rs], direction="lower_is_better"),
                      1, {"identity_code": "MOB"}, "syn-slug", "t030-kindname")
        expect(f"T030-15: a unit spelled like its kind ({_order}) does not compose with the kind's units",
               d["value_max"] is None and "different units" in (d["value_note"] or ""), f"{d['value_max']} {d['value_unit']} {d['value_note']!r}")
    d = determine(synth_db([_w("1200", _canon, ">=", "US"), _w("5", _alien, ">=", "GB"), _w("6", _alien, ">=", "AU")], direction="higher_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-kinds-note")
    _kinds = {r[0] for r in _uc.execute("SELECT kind_id FROM base_quantity_kinds")} - {_canon, _alien}
    expect("T030-15b: the refusal lists the units stated, never a kind id",
           repr(_canon) in (d["value_note"] or "") and repr(_alien) in (d["value_note"] or "")
           and not any(repr(k) in (d["value_note"] or "") for k in _kinds), str(d["value_note"]))
    _kid = _uc.execute("SELECT kind_id FROM base_units WHERE unit = ?", (_alien,)).fetchone()[0]
    expect("T030-15c: ...and in particular not the kind id of either unit", repr(_kid) not in (d["value_note"] or "") and repr(_kind) not in (d["value_note"] or ""),
           str(d["value_note"]))
    # a floor and a ceiling that coincide are two claims, not a point: the minimum is never shown below its source
    d = determine(synth_db([_w("30", _in, ">=", "US"), _w("30", _in, "<=", "GB"), _w("700", _canon, ">=", "AU")], direction="higher_is_better"),
                  1, {"identity_code": "MOB"}, "syn-slug", "t030-coincide")
    _nn = {x["notation"]: x for x in (d["value_notations"] or [])}
    expect("T030-16: a floor and a ceiling of the same 30 in show 762 mm on neither wrong side (a minimum never below 762, a maximum never above), "
           "not 760 for both",
           d["value_min"] == d["value_max"] == float(_thirty) and Fraction(_nn[_canon]["min"]) >= _thirty and Fraction(_nn[_canon]["max"]) <= _thirty
           and Fraction(_nn[_canon]["min"]) <= Fraction(_nn[_canon]["max"]) and _nn[_canon]["min_mark"] == _ac.MARK_UNROUNDED,
           str(d["value_notations"]))
    # shown text comes from the exact Fraction, never a float
    _t = _ac.from_canonical(_uc, 900 * _fac[_canon], "ft" if "ft" in _fac else _other[-1], None, {_canon})
    _p = _ac.from_canonical(synth_db([]), Fraction(100, 12), "%", "min", ())
    _pm = _ac.from_canonical(synth_db([]), Fraction(100, 12), "%", "max", ())
    expect("T030-17: a figure that does not terminate shows SHOWN_DIGITS significant digits cut from the exact Fraction on the safe side "
           "(8.33334 as a minimum, 8.33333 as a maximum), and 900 mm in feet is not a float repr",
           (_p[0], _pm[0]) == ("8.33334", "8.33333") and not _p[1] and Fraction(_p[0]) >= Fraction(100, 12) >= Fraction(_pm[0])
           and len(_t[0].replace(".", "")) <= _ac.SHOWN_DIGITS + 1, f"{_t} {_p} {_pm}")
    # a positive allowance is never shown as zero
    _s1 = _ac.from_canonical(_uc, Fraction(1, 8) * _fac[_in], _canon, "max", {_in})
    _s2 = _ac.from_canonical(_uc, 1 * _fac[_canon], _in, "max", {_canon})
    expect("T030-18: a maximum of 1/8 in shown in mm, and of 1 mm shown in inches, is shown unrounded and marked, never 0",
           _s1[2] == _s2[2] == _ac.MARK_UNROUNDED and Fraction(_s1[0]) == Fraction(1, 8) * _fac[_in] / _fac[_canon]
           and 0 < Fraction(_s2[0]) <= Fraction(1) / _fac[_in], f"{_s1} {_s2}")
    # the canonical index says "the factor is one", not the literal 1/1
    try:
        _uc.execute("INSERT INTO base_units VALUES ('task-fixture-twice', ?, 2, 2, 'number', NULL, 'TASK-FIXTURE', 'TASK-FIXTURE', NULL, NULL)", (_kind,))
        expect("T030-19: a second unit of factor one stored unreduced (2/2) is refused", False, "accepted")
    except sqlite3.IntegrityError:
        expect("T030-19: a second unit of factor one stored unreduced (2/2) is refused", True)
    # a ratio unit is asked of the kind the caller means
    _ratio_kind = _uc.execute("SELECT kind_id FROM base_units WHERE figure_form = 'ratio' LIMIT 1").fetchone()[0]
    expect("T030-20: ratio_unit is the a:b unit of THAT kind, and None for a kind that has none",
           _ac.ratio_unit(_uc, _ratio_kind) == _uc.execute("SELECT unit FROM base_units WHERE kind_id = ? AND figure_form = 'ratio'", (_ratio_kind,)).fetchone()[0]
           and _ac.ratio_unit(_uc, _kind) is None and _ac.ratio_unit(_uc, _ratio_kind) in _ac.ratio_units(_uc), "")

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

    # A kind whose units have no factor-1 unit must RAISE, not be read as if the number were already canonical. The
    # old shape of the defect was a `degrees` member added to the gradient family by analogy: `degrees` is the arctangent
    # of the ratio, not a rescaling, so 5 degrees would read as 5 % -- silently, and only in the composed value. Now a
    # unit is a row with an exact factor, so the shape that remains is a kind left with no scale to compose on.
    import dbcore as _ac       # the unit arithmetic's one home (T-016, T-030); the engine imports its names back
    _uc = synth_db([])
    _kind, _other = _uc.execute(
        "SELECT kind_id, MIN(unit) FROM base_units WHERE NOT (factor_numerator = 1 AND factor_denominator = 1) "
        "GROUP BY kind_id ORDER BY kind_id LIMIT 1").fetchone()
    _uc.execute("DELETE FROM base_units WHERE kind_id = ? AND factor_numerator = 1 AND factor_denominator = 1", (_kind,))
    try:
        _ac.to_canonical(_uc, "5", _other)
        expect("NOTATION: a kind with no factor-1 unit is REFUSED", False, "to_canonical accepted it")
    except NotImplementedError:
        expect("NOTATION: a kind with no factor-1 unit is REFUSED, not read as canonical", True)
    expect("NOTATION: `degrees` has no row, so it is never read as a unit of the gradient kind",
           _ac.unit_kind(_uc, "degrees") is None)

    # One definition of which roles supply a value: the engine's name is the same object as the writers' (dbcore).
    import assess_cell as _engine
    expect("VALUE_SUPPLYING_ROLES is one definition (the engine's name is dbcore's)",
           _engine.VALUE_SUPPLYING_ROLES is _ac.VALUE_SUPPLYING_ROLES)

    # The reader the writer and the engine now share: exact Fractions on the family's scale (dbcore.bound_on_scale).
    from fractions import Fraction
    for _args, _want in [(("1:12", "rise:run ratio", "<=", "numerical"), (None, Fraction(25, 3))),
                         (("8.33", "%", "<=", "numerical"), (None, Fraction("8.33"))),
                         (("1:20", "rise:run ratio", ">=", "numerical"), (Fraction(5), None)),
                         (("0 to 4.8", "%", "between", "range"), (Fraction(0), Fraction("4.8"))),
                         (("1/12", "rise:run ratio", "<=", "numerical"), (None, Fraction(1, 12))),
                         (("8.33%", "%", "<=", "numerical"), None)]:
        _got = _ac.bound_on_scale(synth_db([]), *_args)
        expect(f"dbcore.bound_on_scale{_args} reads {_want}", _got == _want, str(_got))

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

    # T-017 (OR-2): a governing claim with an outgoing `condition_on` edge is a branch, never the
    # headline. Each row is (value, unit, comparator, conditioned?); a conditioned row gets an edge to
    # a `condition` row of ANOTHER parameter, the shape the live edges have. `reverse` points the edge
    # the other way, the relaxation shape: an edge arriving at a row conditions nothing. `relation`
    # is the edge's type (a governing row's `exceeds` edge is not a condition); `qualitative` lists
    # values whose claim is stored as a qualitative statement, which states no number.
    # Tier 1 clinical, so a single source can state the cell (two tier-6 rows leave it pending).
    def _t017_cell(rows, direction="lower_is_better", reverse=False, relation="condition_on",
                   qualitative=()):
        c = synth_db([{"tier": 1, "evidence_type": "clinical", "claimed_value": v,
                       "claimed_unit": u, "comparator": k} for v, u, k, _c in rows],
                     direction=direction)
        for v in qualitative:
            c.execute("UPDATE source_value_extractions SET claim_type = 'qualitative' "
                      "WHERE claimed_value = ?", (v,))
        c.executescript("CREATE TABLE extraction_relations (relation_id INTEGER PRIMARY KEY "
                        "AUTOINCREMENT, from_extraction_id INT, relation TEXT, "
                        "to_extraction_id INT, to_label TEXT, input_role TEXT)")
        for v, _u, _k, cond in rows:
            if not cond:
                continue
            gid, ref = c.execute("SELECT extraction_id, ref_id FROM source_value_extractions "
                                 "WHERE claimed_value = ?", (v,)).fetchone()
            cid = c.execute("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, "
                            "claim_type, claimed_value, claimed_unit, figure_role, comparator) "
                            "VALUES (?, 'syn-slug', 2, 'numerical', '0.5', 'm', 'condition', '>')",
                            (ref,)).lastrowid
            c.execute("INSERT INTO extraction_relations (from_extraction_id, relation, "
                      "to_extraction_id) VALUES (?, ?, ?)",
                      (cid, relation, gid) if reverse else (gid, relation, cid))
        return determine(c, 1, {"identity_code": "MOB"}, "syn-slug", "t017")
    R = "rise:run ratio"
    _b1 = [("1:12", R, "<=", False), ("1:20", R, "<=", True)]
    d = _t017_cell(_b1)
    expect("T017-B1: a conditioned claim is a branch: the headline is the unconditioned 1:12, not the "
           "gentler conditioned 1:20, and the note counts the branch",
           d["value_max"] is not None and abs(d["value_max"] - 100 / 12) < 1e-9
           and "1 conditioned claim(s)" in (d["value_note"] or ""),
           f"max={d['value_max']} note={d['value_note']!r}")
    d = _t017_cell([(v, R, "<=", True) for v in ("1:6", "1:10", "1:12", "1:16", "1:20")])
    expect("T017-B2: every claim conditioned: the headline is EMPTY and the note says piecewise only",
           d["value_max"] is None and (d["value_note"] or "").startswith("piecewise only"),
           f"max={d['value_max']} note={d['value_note']!r}")
    d = _t017_cell([(v, u, k, False) for v, u, k, _c in _b1])
    expect("T017-B3: control, no edge: the same two rows compose as before (the lowest ceiling, 5.0)",
           d["value_max"] == 5.0 and "conditioned" not in (d["value_note"] or ""),
           f"max={d['value_max']} note={d['value_note']!r}")
    d = _t017_cell(_b1, reverse=True)
    expect("T017-B3b: an edge ARRIVING at a claim conditions nothing (the relaxation shape): 5.0, "
           "no branch counted",
           d["value_max"] == 5.0 and "conditioned" not in (d["value_note"] or ""),
           f"max={d['value_max']} note={d['value_note']!r}")
    d = _t017_cell([("1200", "mm", ">=", False), ("1500", "mm", ">=", True)], direction="higher_is_better")
    expect("T017-B4: under higher_is_better the conditioned 1500 would be the most accommodating; "
           "the headline is the unconditioned 1200",
           d["value_min"] == 1200.0 and "1 conditioned claim(s)" in (d["value_note"] or ""),
           f"min={d['value_min']} note={d['value_note']!r}")
    # two units no row of base_units relates (T-030 made cm and m one kind, so they no longer decline): a length and `degrees`
    d = _t017_cell([("600", "mm", "<=", False), ("9", "degrees", "<=", False), ("10", "degrees", "<=", True)])
    expect("T017-B7: a decline over the headline still says how many claims are branches",
           d["value_max"] is None and "different units" in (d["value_note"] or "")
           and "1 conditioned claim(s)" in (d["value_note"] or ""),
           f"max={d['value_max']} note={d['value_note']!r}")
    expect("T017-B7b: ...and names its denominator: the units note is about the UNCONDITIONED claims",
           "unconditioned governing claims are stated in different units" in (d["value_note"] or ""),
           f"note={d['value_note']!r}")
    d = _t017_cell([("1:12", R, "<=", False), ("as gentle as practicable", R, None, False),
                    ("1:20", R, "<=", True)], qualitative=("as gentle as practicable",))
    expect("T017-B8: a composed note counts the headline subset against UNCONDITIONED governing claims, "
           "not against every governing claim",
           "composed from 1 of 2 unconditioned governing claims" in (d["value_note"] or "")
           and "1 conditioned claim(s)" in (d["value_note"] or ""),
           f"note={d['value_note']!r}")
    d = _t017_cell([("as gentle as practicable", R, None, False), ("1:20", R, "<=", True)],
                   qualitative=("as gentle as practicable",))
    expect("T017-B8b: ...and the no-number decline names the unconditioned claims it read",
           (d["value_note"] or "").startswith("no unconditioned governing claim states a numeric value")
           and "1 conditioned claim(s)" in (d["value_note"] or ""), f"note={d['value_note']!r}")
    d0 = _t017_cell([(v, u, k, False) for v, u, k, _c in _b1])
    d1 = _t017_cell(_b1)
    d2 = _t017_cell(_b1, reverse=True)
    expect("T017-B10: the derivation sha carries the conditioned set: the same links with a condition_on "
           "edge FROM a governing row hash differently, so a stored determination goes stale when one is filed",
           d0["derivation_sha"] != d1["derivation_sha"],
           f"{d0['derivation_sha'][:12]} {d1['derivation_sha'][:12]}")
    expect("T017-B10b: ...and an edge ARRIVING at a claim, which changes no answer, does not move it",
           d0["derivation_sha"] == d2["derivation_sha"],
           f"{d0['derivation_sha'][:12]} {d2['derivation_sha'][:12]}")
    d = _t017_cell(_b1, relation="exceeds")
    expect("T017-B9: only a condition_on edge makes a branch: an `exceeds` edge from a governing row "
           "leaves it in the headline (5.0, no branch counted)",
           d["value_max"] == 5.0 and "conditioned" not in (d["value_note"] or ""),
           f"max={d['value_max']} note={d['value_note']!r}")

    # band() and floor_mean(): tier-system section 5, and the owner's five rows of 2026-09-13.
    from schemas.enums import EvidenceMarker as M  # noqa: E402
    from schemas.tier_derivation import band, floor_mean  # noqa: E402
    T1, T4, T6 = band(1, "clinical"), band(4, "standard_eb"), band(6, "code")
    expect("BAND: section 5 reads off (tier, evidence_type)",
           [band(1, "co1"), band(2, "sr_meta"), band(2, "co2"), band(3, "clinical"),
            band(5, "national_fw"), band(3, "grey"), band(3, "standard_eb")]
           == [M.FULL] * 3 + [M.PARTIAL, M.WEAK, M.WEAK, M.PARTIAL] and (T1, T4, T6) == (M.FULL, M.PARTIAL, M.WEAK))
    expect("BAND: floor_mean reproduces the owner's five rows (2 x T1 + T4 is the acceptance case)",
           [floor_mean(x) for x in ([T1, T1, T4], [T1] * 3, [T1, T1, T6], [T1, T6, T6], [T1] * 99 + [T4])]
           == [M.PARTIAL, M.FULL, M.PARTIAL, M.WEAK, M.PARTIAL])

    # ── T-019: a figure reaches a cell only through the live lens links written on it ──────────
    # The fixture codes are labels: the gather never reads a registry. Every figure states a ratio
    # with comparator `<=`, so the cell's value is the lowest ceiling of the figures it gathered
    # and a figure from the wrong lens shows in `value_max`.
    R19 = "rise:run ratio"
    LENS_REASON = "not stated in this cell's lens ("

    def _fig(ref, value, *lenses, **kw):
        s = {"tier": 1, "evidence_type": "clinical", "ref_id": ref, "claimed_value": value,
             "claimed_unit": R19, "comparator": "<="}
        s.update(kw)
        if lenses:
            s["lenses"] = lenses
        return s

    def _mob(code="MOB"):
        return {"identity_code": code}

    # T-055: the identity lens counts through parent_code. A parent's cell gathers its descendants' figures, a child's only its
    # own, and a figure linked to two codes of one family is gathered once.
    _T55 = {"tier": 1, "evidence_type": "clinical"}
    _fam = [("KIDA", "PAR"), ("KIDB", "PAR"), ("GRAND", "KIDA")]
    _src = [dict(_T55, lenses=[{"identity_code": "KIDA"}]), dict(_T55, lenses=[{"identity_code": "KIDB"}]),
            dict(_T55, lenses=[{"identity_code": "GRAND"}]), dict(_T55, lenses=[{"identity_code": "KIDA"}, {"identity_code": "GRAND"}]),
            dict(_T55, lenses=[{"identity_code": "OTHER"}])]
    _ids = lambda d: sorted(l["extraction_id"] for l in d["links"] if l["in_lens"])          # noqa: E731
    def _t55(cell, family):
        # A family defect makes a cell refuse for want of a figure; that is a failed case, not a crashed file that skips
        # every case after it (T-055 critic, 2026-11-15).
        try:
            return determine(synth_db(_src, family=family, direction="lower_is_better"), 1, _mob(cell), "syn-slug", "t055")
        except Refusal as e:
            return {"links": [], "n_extractions_in_lens": -1, "n_sources": -1, "governing_refs": [], "refused": str(e)[:120]}
    _par19, _a19, _g19, _root = _t55("PAR", _fam), _t55("KIDA", _fam), _t55("GRAND", _fam), _t55("KIDA", ())
    expect("T055-01: a parent's cell gathers the figures of every descendant (four of the five here, each once), not an unrelated code's",
           _ids(_par19) == [1, 2, 3, 4] and len(_par19["links"]) == 5 and _par19["n_extractions_in_lens"] == 4,
           f"{_ids(_par19)} {_par19.get('n_extractions_in_lens')}")
    expect("T055-02: a child's cell gathers only itself and its own descendants, never its parent's other children or a sibling",
           _ids(_a19) == [1, 3, 4] and _ids(_g19) == [3, 4], f"{_ids(_a19)} {_ids(_g19)}")
    expect("T055-03: with no family declared every code is a root and the cell gathers only its own code's figures (the premise of "
           "leaving RULE_VERSION alone)", _ids(_root) == [1, 4], str(_ids(_root)))
    expect("T055-04: a figure linked to two codes of one family is one governing figure, not two (counts and refs are each once)",
           _par19["n_extractions_in_lens"] == len(set(_ids(_par19))) == 4 and _par19["n_sources"] == 4
           and len(_par19["governing_refs"]) == len(set(_par19["governing_refs"])),
           f"{_par19.get('n_extractions_in_lens')} {_par19.get('n_sources')} {_par19.get('governing_refs')}")
    # T055-05 (OD-08): a parent with no figure of its own is determined from its descendants' figures.
    _own = determine(synth_db([dict(_T55, lenses=[{"identity_code": "KIDA"}])], family=_fam, direction="lower_is_better"),
                     1, _mob("PAR"), "syn-slug", "t055")
    expect("T055-05: a parent code no figure names is still a cell, and gathers the descendant's figure",
           _own["n_extractions_in_lens"] == 1 and _own["n_sources"] == 1, f"{_own.get('n_extractions_in_lens')} {_own.get('n_sources')}")
    # T055-06: a retired link carries nothing up to the parent.
    _rc = synth_db([dict(_T55, lenses=[{"identity_code": "KIDA"}])], family=_fam, direction="lower_is_better")
    _rc.execute("UPDATE extraction_lens_links SET retired_at = '2026-01-01'")
    try:
        _rr = determine(_rc, 1, _mob("PAR"), "syn-slug", "t055")
        _rr_ok = _rr["n_extractions_in_lens"] == 0
        _rr_msg = ""
    except Exception as _e:                                                  # noqa: BLE001 - a refusal for no gatherable figure is the other right answer
        _rr_ok, _rr_msg = "has no row" in str(_e), str(_e)[:160]
    expect("T055-06: a figure whose only link is retired reaches neither its own code's cell nor its parent's", _rr_ok, _rr_msg)
    # T055-07 (T-055 critic, 2026-11-15): an open gate on a descendant's code reaches the parent's cell, which gathers the figure.
    def _gated(cell):
        d_ = determine(synth_db([dict(_T55, lenses=[{"identity_code": "KIDA"}]), dict(_T55, lenses=[{"identity_code": "KIDB"}]),
                                 dict(_T55, lenses=[{"identity_code": "GRAND"}])],
                                family=_fam, direction="lower_is_better",
                                gates=[(1, "KIDA", "CONTRADICTS", 1, "primary_research", "a trial disagrees")]),
                       1, _mob(cell), "syn-slug", "t055")
        return d_["state"], [g["gate_id"] for g in d_["gates"]]
    _gp, _gc, _gs, _gg = _gated("PAR"), _gated("KIDA"), _gated("KIDB"), _gated("GRAND")
    expect("T055-07: a gate on KIDA reaches KIDA's cell and its parent's, and not a sibling's or a grandchild's (a child's own figures are not the parent's)",
           _gp[1] == [1] and _gc[1] == [1] and _gs[1] == [] and _gg[1] == [] and _gp[0] == _gc[0] == "provisional" and _gs[0] != "provisional",
           f"{_gp} {_gc} {_gs} {_gg}")
    # T055-08: the 2026-08-25 ruling "Not fanned out, ever": a match grade written against a child is not the parent's.
    _pc = synth_db([dict(_T55, ref_id="REF-KID", lenses=[{"identity_code": "KIDA"}])], family=_fam, direction="lower_is_better")
    _pc.execute("INSERT INTO evidence_population_match (match_id, ref_id, match_grade, target_population) VALUES ('M1','REF-KID','EXACT','KIDA')")
    expect("T055-08: a population match graded against a child code is read for that child and never for its parent",
           population_match(_pc, "REF-KID", "KIDA") is not None and population_match(_pc, "REF-KID", "PAR") is None,
           f"{population_match(_pc, 'REF-KID', 'KIDA')} {population_match(_pc, 'REF-KID', 'PAR')}")

    # OD-75 (migration 167): the ICF lens counts through base_icf.parent_code as the identity lens does, so a cell keyed on an
    # umbrella gathers the figures linked to any code beneath it.
    _ifam = [("b765", "b750\u2013b789"), ("b770", "b750\u2013b789"), ("b750\u2013b789", "b710\u2013b799")]
    _isrc = [dict(_T55, lenses=[{"icf_code": "b765"}]), dict(_T55, lenses=[{"icf_code": "b770"}]),
             dict(_T55, lenses=[{"icf_code": "b210"}]), dict(_T55, lenses=[{"icf_code": "b765"}, {"icf_code": "b770"}])]
    def _icf(cell, fam):
        try:
            return determine(synth_db(_isrc, icf_family=fam, direction="lower_is_better"), 1, {"icf_code": cell}, "syn-slug", "od75")
        except Refusal as e:
            return {"links": [], "n_extractions_in_lens": -1, "refused": str(e)[:120]}
    _iu, _ic = _icf("b750\u2013b789", _ifam), _icf("b765", _ifam)
    expect("ICF-01: an umbrella's cell gathers the figures of every code beneath it, once each, and not an unrelated code's",
           _ids(_iu) == [1, 2, 4] and _iu["n_extractions_in_lens"] == 3, f"{_ids(_iu)} {_iu.get('n_extractions_in_lens')} {_iu.get('refused')}")
    expect("ICF-02: a code's cell gathers only its own figures, never the umbrella's other codes",
           _ids(_ic) == [1, 4], f"{_ids(_ic)} {_ic.get('refused')}")
    expect("ICF-03: with no parent written an ICF cell gathers exactly what it did before the hierarchy, its own code's figures (the premise "
           "of leaving RULE_VERSION alone; `specifications` holds no ICF-keyed row, so no determination reads the new rule)",
           _ids(_icf("b765", ())) == [1, 4] and _ids(_icf("b770", ())) == [2, 4], f"{_ids(_icf('b765', ()))} {_ids(_icf('b770', ()))}")
    _ig = lambda cell: dbcore.lens_differs({"icf_code": "b765"}, {"icf_code": cell}, dbcore.lens_families(synth_db([], icf_family=_ifam), {"icf_code": cell}))  # noqa: E731
    expect("ICF-04: a gate or gap on b765 reaches the cell of its umbrella and its own, and not another code's",
           not _ig("b750\u2013b789") and not _ig("b765") and not _ig("b710\u2013b799") and _ig("b770") and _ig("b210"),
           f"{_ig('b750\u2013b789')} {_ig('b765')} {_ig('b770')}")

    def _cell19(sources, cell, **kw):
        return determine(synth_db(sources, direction="lower_is_better", **kw), 1, cell,
                         "syn-slug", "t019")

    _two = [_fig("REF-MOB", "1:12", _mob()), _fig("REF-DEAF", "1:20", _mob("DEAF"))]
    d = _cell19(_two, _mob())
    expect("T019-01: a cell gathers the figures tagged for its lens, not the other group's",
           d["governing_refs"] == ["REF-MOB"] and d["n_sources"] == 1 and d["n_extractions_in_lens"] == 1
           and d["n_extractions_outside_lens"] == 1,
           f"{d['governing_refs']} {d['n_sources']} {d['n_extractions_in_lens']}")
    expect("T019-02: ...so the value is the MOB figure's (1:12), not the looser-by-5.0 DEAF one",
           d["value_max"] is not None and abs(d["value_max"] - 100 / 12) < 1e-9, str(d["value_max"]))
    _by = {l["ref_id"]: l for l in d["links"]}
    expect("T019-03: both figures stay linked (K02); the DEAF one is `excluded` with the lens reason",
           set(_by) == {"REF-MOB", "REF-DEAF"} and _by["REF-MOB"]["role"] == "governing"
           and _by["REF-DEAF"]["role"] == "excluded" and _by["REF-DEAF"]["in_lens"] is False
           and _by["REF-DEAF"]["exclusion_reason"].startswith(LENS_REASON)
           and "identity_code=MOB" in _by["REF-DEAF"]["exclusion_reason"],
           str(_by["REF-DEAF"]))
    d = _cell19(_two, _mob("DEAF"))
    expect("T019-04: the DEAF cell gathers the DEAF figure only, and its value is that figure's",
           d["governing_refs"] == ["REF-DEAF"] and d["value_max"] is not None
           and abs(d["value_max"] - 5.0) < 1e-9, f"{d['governing_refs']} {d['value_max']}")

    _all = [_fig("REF-MOB", "1:12", _mob()), _fig("REF-ALL", "1:20", _mob("ALL"))]
    expect("T019-05: a figure tagged ALL reaches only an ALL cell (OR-1b), and a MOB one only MOB",
           _cell19(_all, _mob())["governing_refs"] == ["REF-MOB"]
           and _cell19(_all, _mob("ALL"))["governing_refs"] == ["REF-ALL"])

    _AB = [_fig("REF-A", "1:12", _mob(), {"icf_code": "d450"}), _fig("REF-B", "1:20", _mob())]
    gov = lambda cell: sorted(_cell19(_AB, cell)["governing_refs"])
    expect("T019-06: a cell stating a lens is reached by every figure carrying it; a cell stating two "
           "is reached by a figure carrying both",
           gov(_mob()) == ["REF-A", "REF-B"] and gov({"icf_code": "d450"}) == ["REF-A"]
           and gov({"identity_code": "MOB", "icf_code": "d450"}) == ["REF-A"],
           f"{gov(_mob())} {gov({'icf_code': 'd450'})} {gov({'identity_code': 'MOB', 'icf_code': 'd450'})}")

    for _model in ("icf_code", "needs_code"):
        _one = [_fig("REF-A", "1:12", _mob(), {_model: "X1"})]
        d1, d2 = _cell19(_one, _mob()), _cell19(_one, {"identity_code": "MOB", _model: "X1"})
        expect(f"T019-07: (MOB) and (MOB, {_model}) over the same links differ in derivation_sha: the "
               "hash carries all three lens codes, not the COALESCE key",
               d1["links"] == d2["links"] and d1["derivation_sha"] != d2["derivation_sha"],
               f"{d1['derivation_sha'][:12]} {d2['derivation_sha'][:12]}")

    expect("T019-08 (AT-32): the model a cell's key leaves NULL but its governing figures carry is "
           "reported, and a cell that keys it reports none",
           _cell19(_AB, _mob())["unkeyed_models"] == ["icf_code"]
           and _cell19(_AB, {"identity_code": "MOB", "icf_code": "d450"})["unkeyed_models"] == [])

    _c = synth_db([_fig("REF-MOB", "1:12")], direction="lower_is_better")
    _c.execute("UPDATE extraction_lens_links SET retired_at = '2026-01-01'")
    try:
        determine(_c, 1, _mob(), "syn-slug", "t019")
        _r = None
    except Refusal as e:
        _r = str(e)
    expect("T019-09: a retired link carries no lens: the figure no longer reaches its cell",
           _r is not None and "has no row" in _r, str(_r))

    for label, cell in (("T019-10", {"identity_code": "AUT"}), ("T019-11", {})):
        try:
            determine(synth_db([_fig("REF-MOB", "1:12")], direction="lower_is_better"), 1, cell,
                      "syn-slug", "t019")
            _r = None
        except Refusal as e:
            _r = str(e)
        expect(f"{label}: " + ("a lens no figure carries has no row (OD-08): refused, nothing returned"
                               if cell else "a cell stating no lens would gather by parameter alone: refused"),
               _r is not None and (("has no row" in _r) if cell else ("at least one lens" in _r)), str(_r))

    _grey = {"tier": 3, "evidence_type": "grey", "ref_id": "REF-GREY"}
    d = _cell19([_grey], _mob(), icf_links=MOB_LINK)
    expect("T019-12: a pending cell that has a figure claims no derivation: no paths, no basis, no "
           "rationale, no anchor",
           d["state"] == "pending" and d["derivation_paths"] is None and d["functional_basis"] is None
           and d["derivation_rationale"] is None and d["cultural_claim_anchor"] is None,
           f"{d['state']} {d['derivation_paths']} {d['functional_basis']} "
           f"{d['derivation_rationale']} {d['cultural_claim_anchor']}")

    d = _cell19([{"tier": 1, "evidence_type": "co1", "co1_source_type": "dpo_position_statement",
                  "verification_status": "UNVERIFIED-CLOSED"}], _mob())
    expect("T019-12b: ...including the cultural claim anchor a community-rooted source would otherwise "
           "leave on a pending cell",
           d["state"] == "pending" and d["cultural_claim_anchor"] is None and d["derivation_paths"] is None,
           f"{d['state']} {d['cultural_claim_anchor']} {d['derivation_paths']}")

    # The direction and confirming sets are gathered through the same clause (T019-16, -17), and the
    # count of superseded figures is over the figures the cell reaches (T019-18).
    _wrong = ({"identity_code": "DEAF"},)
    for _lens_of_finding, _expect_proxy in ((_wrong, 0), ((_mob(),), 1)):
        d = determine(synth_db(_t6 + [dict(_find[0], lenses=_lens_of_finding)]), 1, _mob(), "syn-slug", "t019")
        expect(f"T019-16: a finding tagged for {'another group' if not _expect_proxy else 'the cell'} "
               f"{'supplies no direction to the cell' if not _expect_proxy else 'supplies its direction (control)'}",
               d["rests_on_proxy_inference"] == _expect_proxy and d["n_finding_sources"] == _expect_proxy,
               f"{d['rests_on_proxy_inference']} {d['n_finding_sources']}")
    expect("T019-17: a confirming row tagged for another group confirms nothing (the codes stay weak); "
           "the same row tagged for the cell confirms them (control, R39)",
           _proxy(finding=_find + [dict(_absent_src, lenses=_wrong)], confirmers_from=("REF-FIND-2",)) == WEAK
           and _proxy(finding=_find + [dict(_absent_src, lenses=(_mob(),))],
                      confirmers_from=("REF-FIND-2",)) == FULL)
    d = _cell19([_fig("REF-MOB", "1:12", _mob()), _fig("REF-DEAF", "1:20", _mob("DEAF"),
                                                        superseded_by_ref_id="REF-NEW")], _mob())
    expect("T019-18: a superseded figure the cell does not reach is not counted as superseded in it",
           d["n_extractions_superseded"] == 0, str(d["n_extractions_superseded"]))
    _c = synth_db([_fig("REF-MOB", "1:12", _mob())], direction="lower_is_better")
    _store(_c, determine(_c, 1, _mob(), "syn-slug", "t019"))
    _c.execute("UPDATE extraction_lens_links SET retired_at = '2026-01-01'")
    expect("T019-19: a stored determination whose figures have left its lens is reported stale, not "
           "crashed on",
           stale_determinations(_c) == [(1, ["lens (no figure is stated in it now)"])],
           str(stale_determinations(_c)))

    # ── T-019 repair pass ───────────────────────────────────────────────────────────────────────
    # F1: the confirming row of a `confirms` edge is stated in the cell's lens too (`_confirmed_bands`).
    # One source holds finding f1 (tagged MOB) and f2; f1 confirms the first code, f2 all three.
    # No direction, so no value is shown and the marker is the floor mean of the codes (R7): with a value, codes
    # whose marks differ state it together and the cell is refused (OD-92), which is not what this case tests.
    def _f1(f2_lens, f2_edges=True):
        c = synth_db(_t6 + [dict(_find[0], extraction_method="full")])
        c.executescript("CREATE TABLE extraction_relations (relation_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "from_extraction_id INT, relation TEXT, to_extraction_id INT, to_label TEXT)")
        f1 = c.execute("SELECT MIN(extraction_id) FROM source_value_extractions WHERE ref_id='REF-FIND-1'").fetchone()[0]
        f2 = c.execute("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, claim_type, claimed_value, "
                       "figure_role, extraction_method) VALUES ('REF-FIND-1','syn-slug',1,'qualitative','x',"
                       "'finding','full')").lastrowid
        link_lens(c, f2, f2_lens)
        codes = [r[0] for r in c.execute("SELECT extraction_id FROM source_value_extractions "
                                         "WHERE ref_id NOT LIKE 'REF-FIND%' ORDER BY extraction_id")]
        edges = [(f1, codes[0])] + ([(f2, e) for e in codes] if f2_edges else [])
        c.executemany("INSERT INTO extraction_relations (from_extraction_id, relation, to_extraction_id) "
                      "VALUES (?, 'confirms', ?)", edges)
        return determine(c, 1, _mob(), "syn-slug", "t019")["marker"]
    _m0 = _f1({"identity_code": "DEAF"}, f2_edges=False)
    expect("T019-20: a finding tagged for another group confirms nothing in the cell: its edges leave the "
           "marker as it was without them; the same finding tagged for the cell raises it (control)",
           _f1({"identity_code": "DEAF"}) == _m0 and _f1(_mob()) != _m0, f"{_m0} {_f1({'identity_code': 'DEAF'})} {_f1(_mob())}")

    # F2: a lens link added to or retired from a figure that stays `excluded` moves the stored
    # determination's sha, so `stale_determinations` reports it.
    def _stored(finding_lens):
        c = synth_db([_fig("REF-MOB", "1:12", _mob()),
                      dict(_find[0], ref_id="REF-FND", lenses=(finding_lens,))], direction="lower_is_better")
        _store(c, determine(c, 1, _mob(), "syn-slug", "t019"))
        return c
    _c = _stored({"identity_code": "DEAF"})
    expect("T019-21: control: an unchanged stored cell is not stale", stale_determinations(_c) == [])
    link_lens(_c, _c.execute("SELECT extraction_id FROM source_value_extractions WHERE ref_id='REF-FND'").fetchone()[0],
              _mob())
    expect("T019-21: a lens link ADDED to an excluded figure under a stored cell (its role stays excluded) is "
           "reported stale", stale_determinations(_c) == [(1, ["derivation_sha"])], str(stale_determinations(_c)))
    _c = _stored(_mob())
    _c.execute("UPDATE extraction_lens_links SET retired_at = '2026-01-01' WHERE extraction_id = "
               "(SELECT extraction_id FROM source_value_extractions WHERE ref_id='REF-FND')")
    expect("T019-22: a lens link RETIRED from an excluded figure under a stored cell is reported stale",
           stale_determinations(_c) == [(1, ["derivation_sha"])], str(stale_determinations(_c)))

    # F4: the gap names the lens as the scope of its count and the figures outside it, both derived.
    _c = synth_db([_grey, {"tier": 3, "evidence_type": "grey", "ref_id": "REF-GREY2", "lenses": (_mob("DEAF"),)}])
    d = determine(_c, 1, _mob(), "syn-slug", "t019")
    _total = _c.execute("SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id = 1").fetchone()[0]
    _cause, _ = gap_account(d)
    expect("T019-23: a pending cell's gap says its count is over the lens, and how many of the parameter's "
           "figures lie outside it",
           d["state"] == "pending" and "stated in the lens (identity_code=MOB)" in _cause
           and f"{_total - d['n_extractions_in_lens']} further extraction(s)" in _cause
           and d["n_extractions_outside_lens"] == _total - d["n_extractions_in_lens"] > 0, _cause)

    # F6: every lens model gates a figure (needs as well as identity and ICF); a code is
    # compared, never matched as a pattern; the sha cannot confuse two splits of the same characters.
    for _model in ("icf_code", "needs_code"):
        _AB = [_fig("REF-A", "1:12", _mob(), {_model: "X1"}), _fig("REF-B", "1:20", _mob())]
        _g = lambda cell: sorted(_cell19(_AB, cell)["governing_refs"])   # noqa: E731
        try:
            _cell19(_AB, {_model: "X2"})
            _none = False
        except Refusal:
            _none = True
        expect(f"T019-24: a cell stating {_model} is reached only by the figure carrying it (alone, and with "
               "an identity)", _g({_model: "X1"}) == ["REF-A"] and _g({"identity_code": "MOB", _model: "X1"})
               == ["REF-A"] and _g(_mob()) == ["REF-A", "REF-B"] and _none, f"{_g({_model: 'X1'})}")
    for _pattern in ("M%", "MO_"):
        try:
            _cell19([_fig("REF-MOB", "1:12", _mob())], {"identity_code": _pattern})
            _r = None
        except Refusal as e:
            _r = str(e)
        expect(f"T019-25: a code is compared, not matched as a pattern ({_pattern!r} reaches no MOB figure)",
               _r is not None and "has no row" in _r, str(_r))
    _split = [_fig("REF-A", "1:12", _mob("AB"), {"icf_code": "C"}, _mob("A"), {"icf_code": "BC"})]
    expect("T019-26: two cells whose codes split the same characters differently over one figure differ in sha",
           _cell19(_split, {"identity_code": "AB", "icf_code": "C"})["derivation_sha"]
           != _cell19(_split, {"identity_code": "A", "icf_code": "BC"})["derivation_sha"])
    _c = synth_db([_fig("REF-G", "1:12", _mob()), _fig("REF-D", "1:20", _mob("DEAF"), {"icf_code": "d450"}),
                   dict(_find[0], ref_id="REF-FND", lenses=(_mob(), {"icf_code": "d450"})),
                   _fig("REF-R", "1:30", _mob(), {"needs_code": "N1"})], direction="lower_is_better")
    _c.execute("UPDATE extraction_lens_links SET retired_at = '2026-01-01' WHERE needs_code = 'N1'")
    d = determine(_c, 1, _mob(), "syn-slug", "t019")
    expect("T019-27: the models a cell leaves NULL are read off its GOVERNING figures' LIVE links only: an "
           "out-of-lens figure, a non-governing finding and a retired link report nothing",
           d["unkeyed_models"] == [] and _cell19(_AB, _mob())["unkeyed_models"] == ["needs_code"],
           str(d["unkeyed_models"]))

    # F7: AT-51 on a fixture where it is not vacuous: a figure carrying ALL is governing and not
    # excluded in the ALL cell, and an out-of-lens figure is excluded in each cell it does not reach.
    _am = [_fig("REF-ALL", "1:12", _mob("ALL")), _fig("REF-MOB", "1:20", _mob())]
    dA, dM = _cell19(_am, _mob("ALL")), _cell19(_am, _mob())
    _roleA = {l["ref_id"]: (l["role"], l["in_lens"]) for l in dA["links"]}
    _roleM = {l["ref_id"]: (l["role"], l["in_lens"]) for l in dM["links"]}
    expect("T019-14 (AT-51 on a fixture): the ALL cell's governing, non-excluded figure carries ALL; the MOB "
           "figure is excluded out of lens there, and the ALL figure is excluded out of lens in the MOB cell",
           _roleA == {"REF-ALL": ("governing", True), "REF-MOB": ("excluded", False)}
           and _roleM == {"REF-ALL": ("excluded", False), "REF-MOB": ("governing", True)}, f"{_roleA} {_roleM}")

    # F10: a retired code gets no new cell, in each registry that carries a status.
    _v = sqlite3.connect(":memory:")
    _v.executescript("CREATE TABLE base_taxonomy_identity (identity_code TEXT, status TEXT);"
                     "INSERT INTO base_taxonomy_identity VALUES ('OK','active'),('DEP','deprecated');"
                     "CREATE TABLE base_icf (icf_code TEXT); INSERT INTO base_icf VALUES ('d1');"
                     "CREATE TABLE access_needs (need_code TEXT); INSERT INTO access_needs VALUES ('N1');")
    def _refuses(lens):
        try:
            validate_lens(_v, dict(lens))
            return None
        except Refusal as e:
            return str(e)
    expect("T019-28: validate_lens refuses a deprecated identity code, and accepts "
           "the live ones and a registry with no status",
           "deprecated" in (_refuses({"identity_code": "DEP"}) or "")
           and _refuses({"identity_code": "OK", "icf_code": "d1", "needs_code": "N1"}) is None)

    # Live database, read-only (`determine` writes nothing). Every probe is chosen by query from the
    # figures' own live links; none is typed.
    _live = None
    if os.path.exists(live_db):
        _live = sqlite3.connect(f"file:{live_db}?mode=ro", uri=True)
        if not _live.execute("SELECT 1 FROM sqlite_master WHERE name = 'v_live_lens_links'").fetchone():
            _live = None
    _par = dict(_live.execute("SELECT identity_code, parent_code FROM base_taxonomy_identity").fetchall()) if _live else {}

    def _family_py(code):
        """The code and every descendant, computed in Python from the registry (independent of the engine's SQL)."""
        fam, grew = {code}, True
        while grew:
            grew = False
            for k, p in _par.items():
                if p in fam and k not in fam:
                    fam.add(k); grew = True
        return fam

    def _carries(pid, code):
        fam = sorted(_family_py(code))
        return {r[0] for r in _live.execute(
            "SELECT DISTINCT x.extraction_id FROM source_value_extractions x JOIN v_live_lens_links l USING (extraction_id) "
            f"WHERE x.parameter_id = ? AND l.identity_code IN ({','.join('?' * len(fam))})", (pid, *fam))}
    _pairs = _live.execute("SELECT DISTINCT x.parameter_id, l.identity_code FROM v_live_lens_links l "
                           "JOIN source_value_extractions x USING (extraction_id) "
                           "WHERE l.identity_code IS NOT NULL ORDER BY 1, 2").fetchall() if _live else []
    if not _pairs:
        print("      SKIPPED-NO-FIXTURE: T019-13..15 need the live database with identity links on figures")
    else:
        _bad, _reached, _open = [], 0, []
        for pid, code in _pairs:
            try:
                d = determine(_live, pid, _mob(code), "syn-slug", "t019-live")
            except OpenQuestion:          # refused, naming an owner question (T-117): no links to read
                _open.append((pid, code))
                continue
            inl = {l["extraction_id"] for l in d["links"] if l["in_lens"]}
            _reached += len(inl)
            carries = _carries(pid, code)
            out_ok = all(l["role"] == "excluded" and (l["exclusion_reason"] or "").startswith(LENS_REASON)
                         for l in d["links"] if not l["in_lens"])
            gov_ok = all(l["extraction_id"] in carries for l in d["links"] if l["role"] != "excluded")
            if not (inl and inl == carries and out_ok and gov_ok):
                _bad.append((pid, code))
        expect("T019-13 (AT-50): for every (parameter, identity code) the live links name, the figures "
               f"a cell reaches are exactly those carrying its code ({len(_pairs) - len(_open)} cells, {_reached} "
               f"figures reached; {len(_open)} refused on an open owner question, not examined: {_open}), none "
               "is empty, and every other figure of the parameter is linked "
               "`excluded` with the lens reason", not _bad and _reached > 0, str(_bad))

        # AT-51 live: every parameter whose figures carry ALL and another identity, cell by cell. The
        # equality (reached == carrying) holds for each; whether a cell has a NON-EXCLUDED row is derived,
        # and the case says so when no ALL cell has one, since then nothing plays a part there.
        _ap = _live.execute("SELECT DISTINCT x.parameter_id, o.identity_code FROM source_value_extractions x "
                            "JOIN v_live_lens_links a ON a.extraction_id = x.extraction_id "
                            "AND a.identity_code = 'ALL' JOIN source_value_extractions y "
                            "ON y.parameter_id = x.parameter_id JOIN v_live_lens_links o "
                            "ON o.extraction_id = y.extraction_id AND o.identity_code <> 'ALL' "
                            "ORDER BY 1, 2").fetchall()
        if not _ap:
            print("      SKIPPED-NO-FIXTURE: T019-14 needs a parameter whose figures carry ALL and "
                  "another identity")
        else:
            ok, _played = True, 0
            for pid, other in _ap:
                for code in ("ALL", other):
                    d = determine(_live, pid, _mob(code), "syn-slug", "t019-live")
                    inl = {l["extraction_id"] for l in d["links"] if l["in_lens"]}
                    ok &= inl == _carries(pid, code) and bool(inl)
                    _fam = sorted(_family_py(code))
                    ok &= all(_live.execute("SELECT 1 FROM v_live_lens_links WHERE extraction_id = ? "
                                            f"AND identity_code IN ({','.join('?' * len(_fam))})", (l["extraction_id"], *_fam)).fetchone()
                              for l in d["links"] if l["role"] != "excluded")
                    _played += code == "ALL" and any(l["role"] != "excluded" for l in d["links"])
            expect("T019-14 (AT-51, live): every ALL cell reaches exactly the figures carrying ALL, and every "
                   "other identity's cell reaches an ALL-tagged figure only if it also carries that identity "
                   f"({_played} of the ALL cells hold a non-excluded row)",
                   ok, f"{len(_ap)} parameter/identity pairs")
            if not _played:
                print("      SKIPPED-NO-FIXTURE: T019-14 live non-vacuity: no ALL cell holds a non-excluded "
                      "row, so AT-51 is met on the fixture case only (the equality above is over reached "
                      "figures that supply nothing)")

        _n = next(((pid, code) for (pid,) in _live.execute("SELECT DISTINCT x.parameter_id FROM source_value_extractions x "
                                                          "JOIN v_live_lens_links l USING (extraction_id) ORDER BY 1")
                    for code in sorted(_par) if not _carries(pid, code)), None)
        if not _n:
            print("      SKIPPED-NO-FIXTURE: T019-15 needs a parameter with links and an identity "
                  "no figure of it carries")
        else:
            try:
                determine(_live, _n[0], _mob(_n[1]), "syn-slug", "t019-live")
                _r = None
            except Refusal as e:
                _r = str(e)
            expect("T019-15 (AT-52): an identity no figure of the parameter carries has no row: refused",
                   _r is not None and "has no row" in _r, f"parameter {_n[0]} {_n[1]}: {_r}")

    # T-011: a cell determined again after a retirement points its newest retired row at the new one. The engine runs as a
    # subprocess on copies of the live database (it commits into the copy). The cell is derived by query (an identity-only
    # cell with a determination, live or retired) and each copy is PREPARED to the state the case needs: the live row is
    # retired by the verb, pointers are cleared by HAND on the copy. So the cases survive the cell being determined again.
    import shutil
    import subprocess
    import tempfile
    _ro = sqlite3.connect(f"file:{os.path.join(REPO_ROOT, 'data', 'guidebook.db')}?mode=ro", uri=True)
    _cell = _ro.execute(
        "SELECT parameter_id, identity_code FROM specifications WHERE identity_code IS NOT NULL AND icf_code IS NULL "
        "AND needs_code IS NULL GROUP BY 1, 2 HAVING COUNT(*) >= 3 ORDER BY 1, 2 LIMIT 1").fetchone()
    _slug = _ro.execute("SELECT slug FROM slugs WHERE status='ACTIVE' ORDER BY slug LIMIT 1").fetchone()
    _ro.close()
    if not _cell or not _slug:
        print("      SKIPPED-NO-FIXTURE: T011 needs an identity-only cell with three determinations and an active slug")
    else:
        _tmp = tempfile.mkdtemp(prefix="t011-")
        _CELLQ = ("FROM specifications WHERE parameter_id=? AND identity_code=? AND icf_code IS NULL AND needs_code IS NULL")
        _SESS = "session_t011-fixture"

        def _sql_on(db_file, sql, *args):
            c = sqlite3.connect(db_file)
            out = c.execute(sql, args).fetchall()
            c.commit()
            c.close()
            return out

        def _prep(tag, clear=(), point=()):
            """A copy of the live database whose cell has no live row: the live row is retired by the verb, the pointers
            of the rows named in `clear` (offsets from the newest retired row) are set NULL by hand, and those in `point`
            are set to the oldest row of the cell (a pointer that already exists)."""
            f = os.path.join(_tmp, tag + ".db")
            shutil.copy(os.path.join(REPO_ROOT, "data", "guidebook.db"), f)
            # T-117: a cell whose shown value a non-VERIFIED source states is refused, naming OD-99 (owner). These cases
            # test the supersession pointer, not the marker, so on the copy such sources' figures of the parameter are
            # retired and the cell answers.
            _sql_on(f, "UPDATE source_value_extractions SET retired_at = strftime('%Y-%m-%d %H:%M', 'now', '-1 minute'), "
                       "retired_by_session = ?, "
                       "retirement_reason = 'T011 fixture: answer without an open owner question (T-117)' "
                       "WHERE parameter_id = ? AND retired_at IS NULL AND ref_id IN (SELECT ref_id FROM evidence_sources "
                       "WHERE COALESCE(verification_status, '') <> 'VERIFIED')", _SESS, _cell[0])
            live = _sql_on(f, f"SELECT specification_id {_CELLQ} AND retired_at IS NULL", *_cell)
            if live:
                subprocess.run([sys.executable, os.path.join(REPO_ROOT, "scripts", "db.py"), "retire-specification",
                                "--specification-id", str(live[0][0]), "--reason", "TASK-FIXTURE T011", "--session", _SESS],
                               capture_output=True, text=True, env=dict(os.environ, GUIDEBOOK_DB_PATH=f), check=True)
            order = [r[0] for r in _sql_on(f, f"SELECT specification_id {_CELLQ} AND retired_at IS NOT NULL "
                                              "ORDER BY retired_at DESC, specification_id DESC", *_cell)]
            for k in clear:
                _sql_on(f, "UPDATE specifications SET superseded_by_specification_id=NULL WHERE specification_id=?", order[k])
            for k in point:
                _sql_on(f, "UPDATE specifications SET superseded_by_specification_id=? WHERE specification_id=?",
                        order[-1], order[k])
            return f, order

        def _engine(db_file, tag, stamp, session=_SESS):
            sql_file = os.path.join(_tmp, tag + ".sql")
            r = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "scripts", "assess", "assess_cell.py"),
                                "--db", db_file, "--emit-sql", sql_file, "--parameter-id", str(_cell[0]),
                                "--slug", _slug[0], "--identity", _cell[1], "--session", session, "--stamp", stamp],
                               capture_output=True, text=True)
            return r, sql_file

        def _full(db_file):
            c = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)
            cur = c.execute(f"SELECT * {_CELLQ} ORDER BY specification_id", _cell)
            names = [d[0] for d in cur.description]
            out = {r[0]: dict(zip(names, r)) for r in cur.fetchall()}
            c.close()
            return out

        def _ptr(rows, spec_id):
            return rows[spec_id]["superseded_by_specification_id"]

        # --- the ordinary case: the newest retired row has no pointer
        _a, _order = _prep("a", clear=(0,))
        _b, _ = _prep("b", clear=(0,))
        _c, _ = _prep("c", clear=(0,))
        _before = _full(_a)
        _newest = _order[0]
        _ra, _sa = _engine(_a, "a", "2026-01-01 00:00")
        _rb, _sb = _engine(_b, "b", "2026-01-01 00:00")
        _after = _full(_a)
        _new = max(_after)
        expect("T011-01: the newest retired row of the cell now points at the new determination, which is live",
               _ra.returncode == 0 and _ptr(_after, _newest) == _new and _after[_new]["retired_at"] is None,
               f"cell {_cell}, newest {_newest}, {_ra.stderr[-200:]}")
        _same = {k: v for k, v in _after.items() if k not in (_newest, _new)} == \
                {k: v for k, v in _before.items() if k != _newest}
        _others = {k: v for k, v in _after[_newest].items() if k not in ("superseded_by_specification_id", "updated_at",
                                                                         "updated_by_session")} == \
                  {k: v for k, v in _before[_newest].items() if k not in ("superseded_by_specification_id", "updated_at",
                                                                          "updated_by_session")}
        expect("T011-02: no other row of the cell changed in any column, and the linked row changed only in its pointer and "
               "its update stamp", _same and _others, f"{_before.keys()} -> {_after.keys()}")
        _sql = open(_sa).read()
        expect("T011-03: the emitted SQL carries the UPDATE once, after the INSERT of the new row",
               _sql.count("UPDATE specifications SET superseded_by_specification_id=") == 1
               and _sql.index("INSERT INTO specifications") < _sql.index("UPDATE specifications SET superseded_by"),
               _sql.count("UPDATE specifications"))
        _cc = sqlite3.connect(_c)
        _cc.executescript(_sql)
        _cc.commit()
        _cc.close()
        expect("T011-04: replaying the SQL on a second prepared copy reproduces the engine's rows in EVERY column, stamps included",
               _full(_c) == _after, "replayed rows differ from the engine's")
        expect("T011-05: the same inputs on a second prepared copy give byte-identical SQL",
               _rb.returncode == 0 and open(_sa).read() == open(_sb).read())
        # --- the chain: retire the new row, determine again; the first link is untouched
        _rt = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "scripts", "db.py"), "retire-specification",
                              "--specification-id", str(_new), "--reason", "TASK-FIXTURE T011", "--session", _SESS],
                             capture_output=True, text=True, env=dict(os.environ, GUIDEBOOK_DB_PATH=_a))
        _r2, _s2 = _engine(_a, "a2", "2026-01-01 00:01")
        _last = _full(_a)
        _new2 = max(_last)
        expect("T011-06: determining again after a second retirement links the second row and leaves the first link alone",
               _rt.returncode == 0 and _r2.returncode == 0 and _ptr(_last, _new) == _new2 and _ptr(_last, _newest) == _new,
               f"{_rt.stderr[-150:]} {_r2.stderr[-150:]}")
        # --- two retired rows with no pointer: only the newest is linked, the older is named
        _d, _od = _prep("d", clear=(0, 1))
        _rd, _sd = _engine(_d, "d", "2026-01-01 00:00")
        _rows7 = _full(_d)
        expect("T011-07: with two retired rows holding no pointer only the newest retired is linked; the older stays as history "
               "and is named, by id, on stderr",
               _rd.returncode == 0 and _ptr(_rows7, _od[0]) == max(_rows7) and _ptr(_rows7, _od[1]) is None
               and f"[{_od[1]}]" in _rd.stderr, f"{_rd.stderr[-250:]}")
        # --- the newest retired row already has its successor: nothing is linked, the older bare row is named
        _e, _oe = _prep("e", clear=(1,), point=(0,))
        _re, _se = _engine(_e, "e", "2026-01-01 00:00")
        _rows8 = _full(_e)
        expect("T011-08: when the newest retired row already has a pointer nothing is linked and no UPDATE is emitted; the older "
               "bare row is named",
               _re.returncode == 0 and _ptr(_rows8, _oe[0]) == _oe[-1] and _ptr(_rows8, _oe[1]) is None
               and "UPDATE specifications SET superseded_by" not in open(_se).read() and f"[{_oe[1]}]" in _re.stderr,
               f"{_re.stderr[-200:]}")
        # --- 'most recently retired' is read from retired_at, not from the id
        _f, _of = _prep("f", clear=(0, 1))
        _sql_on(_f, "UPDATE specifications SET retired_at='2099-01-01 00:00' WHERE specification_id=?", _of[1])
        _rf, _sf = _engine(_f, "f", "2026-01-01 00:00")
        _rows9 = _full(_f)
        expect("T011-09: the row retired most recently by its retired_at is the one linked, not the one with the highest id",
               _rf.returncode == 0 and _ptr(_rows9, _of[1]) == max(_rows9) and _ptr(_rows9, _of[0]) is None,
               f"{_rf.stderr[-200:]}")
        # --- a '?' in a value is data: the emitted SQL and the database agree
        _g, _og = _prep("g", clear=(0,))
        _gc, _ = _prep("gc", clear=(0,))
        _rg, _sg = _engine(_g, "g", "2026-01-01 00:00", session="session_t011-what?")
        _gcc = sqlite3.connect(_gc)
        _gcc.executescript(open(_sg).read())
        _gcc.commit()
        _gcc.close()
        expect("T011-10: a '?' in --session does not corrupt the emitted UPDATE: replaying it reproduces the engine's rows",
               _rg.returncode == 0 and _full(_gc) == _full(_g), _rg.stderr[-200:])
        # --- T-021: a QUESTION on the cell appears in what the engine prints, and does not change the answer
        _Qtext = "TASK-FIXTURE: a reader asks whether this value suits a person who uses a long cane"
        _q0, _ = _prep("q0", clear=(0,))
        _q1, _ = _prep("q1", clear=(0,))
        _sql_on(_q1, "INSERT INTO determination_gates (parameter_id, identity_code, verdict, detail, raised_at, raised_by_session) "
                     "VALUES (?, ?, 'QUESTION', ?, '2026-11-15', 'syn')", _cell[0], _cell[1], _Qtext)
        _r0, _ = _engine(_q0, "q0", "2026-01-01 00:00")
        _r1, _ = _engine(_q1, "q1", "2026-01-01 00:00")
        _pl = lambda r: next((l.split() for l in r.stdout.splitlines() if l.startswith("param ")), [])  # noqa: E731
        expect("T021-06: the engine prints the question beside the cell (QUESTIONED, the gate id and the words) and a run without it prints none",
               _r0.returncode == 0 and _r1.returncode == 0 and "QUESTIONED" not in _r0.stdout
               and "QUESTIONED: gate" in _r1.stdout and _Qtext[:60] in _r1.stdout, f"{_r1.stdout[-300:]} {_r1.stderr[-200:]}")
        expect("T021-07: the question does not change the determination: the printed state of the cell is the same with and without it",
               len(_pl(_r0)) > 2 and _pl(_r0)[2] == _pl(_r1)[2], f"{_pl(_r0)[:3]} {_pl(_r1)[:3]}")
        shutil.rmtree(_tmp, ignore_errors=True)

    t117_t056_cases()

    if FAILED:
        print(f"\nFAIL: {len(FAILED)} test(s): {FAILED}")
        sys.exit(1)
    print(f"\nEXAMINED: {len(_EXPECTED)} case(s)")
    print("\nPASS: all pilot-engine branch tests")


if __name__ == "__main__":
    main()
