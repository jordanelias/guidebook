"""Stage 2.4 — tests for the DB cell-state validator in validate_evidence_state.py.

Exercises the conditional cross-field rules that SQLite CHECK/FK cannot express
(pending⇒gap, provisional⇒confidence, not_applicable⇒rationale, stated⇒
convergence, convergent⇒≥2 axes, single_axis⇒≤1, divergent⇒rationale+synthesis,
and the §1.7 directness rule that a discounted source cannot also anchor).
Exit 0 = pass.
"""
import os
import re
import sqlite3
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from validate_evidence_state import CELL_STATE_REQUIRED, validate_db  # noqa: E402

fails = []


sys.path.insert(0, HERE)
from _baseline_ddl import ddl_for  # noqa: E402
from schemas.enums import EvidenceMarker  # noqa: E402

M = EvidenceMarker.FULL.value   # a live stated or provisional row must carry a marker (migration 116)


def schema_ddl():
    """The specification/convergence DDL, read from the current baseline.

    This used to scan every numbered migration for a literal table name and then
    replay the 055 rename onto the result. That selector had to match the
    migrations' immutable text, so a token sweep rewrote it and silently built the
    wrong schema; then the history was frozen behind a baseline and the files were
    gone entirely. One baseline file holds the current schema, so both problems
    disappear along with the hand-copied replay they required.
    """
    # `specifications` and its indexes come from the LIVE schema, not the baseline.
    # Migration 071 dropped and recreated the table (parameter_id + four lens columns,
    # item_code and population_code gone) and replaced idx_specifications_item/_pop
    # with idx_spec_row_identity. The baseline is immutable and therefore frozen at the
    # pre-071 shape, so building the fixture from it would assert against a table the
    # database no longer has -- the exact failure this function's docstring describes.
    # Everything else still comes from the baseline; only the re-keyed table is live.
    import sqlite3 as _sq
    con = _sq.connect("file:data/guidebook.db?mode=ro", uri=True)
    # The re-keyed table carries real typed FKs into the three lens registries and
    # base_parameters (owner 2026-08-28: "real FKs"), so the fixture needs those parents
    # or every INSERT dies on a missing table. Pulled live for the same reason as
    # specifications itself: they are the only place their current shape exists.
    live = [r[0] for r in con.execute(
        "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND ("
        "  name = 'specifications' OR tbl_name = 'specifications'"
        # `axes` -> `base_icf` 2026-09-13: migration 081 re-pointed specifications.icf_code
        # at the ICF registry (owner ruling, "keep the ICF lens, give it real ICF codes"),
        # so a fixture pulling `axes` builds a parent nothing references and misses the one
        # the FK needs. Rule 4: a test fixture is a caller.
        # `convergence_sources` 2026-09-20: migration 093 moved the five JSON source arrays
        # into a junction with a real FK per ref_id, and validate_convergence_db reads it
        # now. A fixture without it builds a schema the validator cannot query at all.
        # `specification_source_links` 2026-09-21: the anti-hallucination gate reads the
        # junction now, not `specifications.governing_refs`. A fixture is a caller.
        "  OR name IN ('base_parameters','base_icf','access_needs',"
        "              'convergence_sources','specification_source_links'))")]
    con.close()
    if not live:
        print("  [FAIL] live schema has no `specifications` — fixture cannot be built.",
              file=sys.stderr)
        sys.exit(1)
    # sqlite_master stores statements WITHOUT a trailing semicolon; executescript needs
    # them separated. ddl_for() returns baseline text that already carries its own.
    return [";\n".join(live) + ";\n" + ddl_for("convergence_assessment")]


DDL = schema_ddl()
fd, DBP = tempfile.mkstemp(suffix=".db"); os.close(fd)


def fresh():
    if os.path.exists(DBP):
        os.remove(DBP)
    c = sqlite3.connect(DBP)
    # `items` stub retired 2026-09-09: migration 071 removed specifications.item_code,
    # so nothing in this fixture references it. `base_taxonomy_identity` stays — it is the identity
    # lens and specifications.identity_code points at it.
    c.execute("CREATE TABLE base_taxonomy_identity(identity_code TEXT PRIMARY KEY)")
    # description/category/priority are stubbed because v_pending selects them.
    # Not needed while nothing re-parses the views, but a stub parent that matches
    # the real column set is the honest fixture either way.
    c.execute("CREATE TABLE gaps(gap_id TEXT PRIMARY KEY, category TEXT, "
              "priority TEXT, description TEXT)")
    c.executemany("INSERT INTO base_taxonomy_identity VALUES(?)", [(x,) for x in ("AUT", "MOB", "DEAF")])
    c.execute("INSERT INTO gaps(gap_id,category,priority,description) "
              "VALUES('GAP-001','RP','P2','fixture gap')")
    for step in DDL:
        c.executescript(step)
    # Seed the subject side. base_parameters.term_id is NOT NULL UNIQUE into `terms`,
    # which this fixture does not stub, so FKs stay off for the seed — this file tests
    # the §2 STATE MACHINE, not referential integrity, and the real FK behaviour is
    # proven against the live schema in test_db_integrity.
    c.execute("PRAGMA foreign_keys=OFF")
    c.executemany("INSERT INTO base_parameters(parameter_id,term_id,created_at,created_by_session)"
                  " VALUES(?,?,?,?)",
                  [(i, f"TERM-{i:03d}", "2026-09-09", "fixture") for i in range(1, 7)])
    return c


def assert_fixture_current():
    """Fail loudly here if the fixture drifts from what the validator selects.

    Without this, a missing column surfaces as an OperationalError raised deep
    inside validate_evidence_state on the first check — which reads as a broken
    validator rather than a stale fixture. That misreading is exactly what
    happened: the file was nearly retired as testing a schema the DB no longer
    had, when in fact the DB had moved on and the fixture had not.
    """
    c = fresh()
    present = {r[1] for r in c.execute("PRAGMA table_info(specifications)")}
    c.close()
    # Imported, not restated. A second hardcoded copy of the validator's column
    # list would silently stop covering any column added there — the guard would
    # keep passing while checking less, which is the failure it exists to catch.
    missing = sorted(set(CELL_STATE_REQUIRED) - present)
    if missing:
        print(f"  [FAIL] fixture schema is stale — specifications lacks {missing}.\n"
              f"         A migration changed the table and schema_ddl() did not pick it up.")
        print(f"\nFAILURES: stale fixture  (1 failed)")
        sys.exit(1)


assert_fixture_current()


def run(setup, fk=True):
    c = fresh()
    c.execute(f"PRAGMA foreign_keys={'ON' if fk else 'OFF'}")
    setup(c)
    c.commit(); c.close()
    errors, _, _ = validate_db(DBP)
    return errors


_CASES = []


def check(name, cond):
    _CASES.append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


def has(errs, *subs):
    return any(all(s in e for s in subs) for e in errs)


def conv(c, cid, status, clinical=(), co1=(), co2=(), downw=(), disc=(),
         rationale=None, synth=None):
    """Insert a convergence row the way assess_cell.py writes one since migration 093.

    The five *_sources ARRAYS ARE NOT WRITTEN. They are frozen history on rows that
    predate 093; the live home is the `convergence_sources` junction, which is what
    validate_convergence_db reads. A test that kept writing the arrays would assert
    against a shape the writer no longer produces -- rule 4, a fixture is a caller.
    """
    c.execute("INSERT INTO convergence_assessment(convergence_id,status,rationale,"
              "synthesis_approach) VALUES (?,?,?,?)", (cid, status, rationale, synth))
    for role, refs in (("clinical", clinical), ("co1", co1), ("co2", co2),
                       ("down_weighted", downw), ("discounted", disc)):
        for ref in refs:
            c.execute("INSERT INTO convergence_sources(convergence_id,ref_id,role) "
                      "VALUES (?,?,?)", (cid, ref, role))


# clean baseline — a valid stated cell + convergent convergence (2 axes)
def clean(c):
    conv(c, 1, 'convergent', clinical=["REF-1"], co1=["REF-2"])
    # governing_refs is required on 'stated' (anti-hallucination gate, §2.7). The
    # baseline predated that rule, so it was not clean once the fixture caught up.
    c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,design_scale,convergence_id,marker) "
              "VALUES (1,1,'AUT','stated','population',1,'%s')" % M)
    # Through the junction: `governing_refs` is retired and a row written today leaves it
    # NULL, so stating the ref in the JSON would no longer satisfy the gate.
    c.execute("INSERT INTO specification_source_links(specification_id,ref_id,role) "
              "VALUES (1,'REF-1','governing')")
check("clean stated+convergent → 0 errors", run(clean) == [])

# stated with NO governing source — the anti-hallucination gate. The row below writes no
# specification_source_links entry, which since the 2026-09-21 retirement is the only way
# to state one: a row leaves `governing_refs` NULL now, so the JSON cannot answer this.
check("stated without a governing source caught (anti-hallucination gate)",
      has(run(lambda c: (
          conv(c, 1, 'convergent', clinical=["REF-1"], co1=["REF-2"]),
          c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,design_scale,convergence_id,marker) "
                    "VALUES (1,7,'MOB','stated','population',1,'%s')" % M))),
          "stated", "specification_source_links"))

# pending without gap
check("pending without gap_register_id caught",
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state) "
                                  "VALUES (1,3,'MOB','pending')")), "pending", "requires gap_register_id"))

# pending with gap not in gaps table (FK off to construct the row)
check("pending with unknown gap caught (defense-in-depth vs FK)",
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,gap_register_id) "
                                  "VALUES (1,3,'MOB','pending','GAP-999')"), fk=False), "not in gaps table"))

# provisional without confidence flag
check("provisional without confidence flag caught",
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,convergence_id,marker) "
                                  "VALUES (1,4,'AUT','provisional',NULL,'%s')" % M)), "provisional", "confidence flag"))

# not_applicable without rationale
check("not_applicable without rationale caught",
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state) "
                                  "VALUES (1,5,'DEAF','not_applicable')")), "not_applicable", "rationale"))

# stated without convergence
check("stated without convergence caught",
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,marker) "
                                  "VALUES (1,6,'AUT','stated','%s')" % M)), "stated", "convergence"))

# convergent with <2 axes
check("convergent with <2 axes caught",
      has(run(lambda c: conv(c, 1, 'convergent', clinical=["REF-1"])),
          "convergent", "≥2 evidence axes"))

# single_axis with >1 axis
check("single_axis with >1 axis caught",
      has(run(lambda c: conv(c, 1, 'single_axis', clinical=["REF-1"], co1=["REF-2"],
                             rationale='clinical only')), "single_axis", "axes present"))

# divergent without rationale + synthesis_approach
check("divergent without rationale/synthesis caught",
      has(run(lambda c: conv(c, 1, 'divergent', clinical=["REF-1"], co1=["REF-2"])),
          "divergent", "rationale"))

# directness (§1.7): a discounted source also listed as anchoring
check("discounted source also anchoring caught (§1.7)",
      has(run(lambda c: conv(c, 1, 'convergent', clinical=["REF-1"], co1=["REF-2"],
                             disc=["REF-1"])), "discounted_sources also listed as anchoring"))

# malformed JSON column
check("malformed JSON source list caught",
      # RAW ON PURPOSE. The malformed-array check now applies ONLY to rows that predate
      # migration 093 and still carry the arrays; a row written after it has NULL there and
      # is validated from the junction. So this case must write the array directly -- using
      # conv() would produce a post-093 row and stop exercising the branch at all.
      has(run(lambda c: c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources) "
                                  "VALUES (1,'convergent','not json','[\"REF-2\"]')")), "not a valid JSON array"))

# ── T-004: four checks say how many of the determinations they read are live ─────────────────────────────────
import shutil  # noqa: E402
import subprocess  # noqa: E402


def _chk(name, cond, detail=None):
    check(name, cond)
    if not cond and detail is not None:
        print(f"        {str(detail)[:300]}")


_T004_LIVE = os.environ.get("GUIDEBOOK_DB_PATH") or os.path.join(REPO, "data", "guidebook.db")
_T004_EV, _T004_VC, _T004_AJ, _T004_HS = ("scripts/validate_evidence_state.py", "scripts/validate_verification_consistency.py",
                                          "scripts/audit/adjudication_integrity.py", "scripts/audit/derivation_handshake_integrity.py")
_T004_LINE = re.compile(r"^\s*determinations read: (\d+) live, (\d+) retired", re.M)


def _t004_q(db_file, sql):
    c = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)
    out = c.execute(sql).fetchone()
    c.close()
    return tuple(out)


def _t004_expect(db_file):
    """What each check should print, derived from the table by the predicate of the rows THAT check reads:
    (its line's (live, retired), its EXAMINED number)."""
    live_all = _t004_q(db_file, "SELECT COALESCE(SUM(retired_at IS NULL),0), COALESCE(SUM(retired_at IS NOT NULL),0) FROM specifications")
    live_sp = _t004_q(db_file, "SELECT COALESCE(SUM(retired_at IS NULL),0), COALESCE(SUM(retired_at IS NOT NULL),0) FROM specifications "
                               "WHERE state IN ('stated','provisional')")
    n_spec = _t004_q(db_file, "SELECT COUNT(*) FROM specifications")[0]
    n_conv = _t004_q(db_file, "SELECT COUNT(*) FROM convergence_assessment")[0]
    n_src = _t004_q(db_file, "SELECT COUNT(*) FROM evidence_sources")[0]
    n_gate = _t004_q(db_file, "SELECT COUNT(*) FROM determination_gates")[0]
    return {_T004_EV: (live_all, n_spec + n_conv), _T004_VC: (live_sp, live_sp[0] + live_sp[1]),
            _T004_AJ: (live_all, n_src), _T004_HS: ((live_all[0], 0), live_all[0] + n_gate)}


def _t004_run(db_file, script):
    argv = [sys.executable, os.path.join(REPO, script)] + (["--db", db_file] if script == _T004_HS else [])
    r = subprocess.run(argv, capture_output=True, text=True, env=dict(os.environ, GUIDEBOOK_DB_PATH=db_file))
    out = r.stdout + r.stderr
    m = _T004_LINE.search(out)
    e = re.search(r"^EXAMINED: (\d+)", out, re.M)
    return ((int(m.group(1)), int(m.group(2))) if m else None, int(e.group(1)) if e else None, out, r.returncode)


_tmp4 = tempfile.mkdtemp(prefix="t004-")
try:
    _a = os.path.join(_tmp4, "a.db")
    shutil.copy(_T004_LIVE, _a)
    _exp = _t004_expect(_a)
    _ra = {sc: _t004_run(_a, sc) for sc in _exp}
    _chk("T004-01: each of the four checks states 'determinations read: <live> live, <retired> retired' over the rows IT reads "
         "(all, all, stated/provisional, live only), and the numbers are the table's",
         all(_ra[sc][0] == _exp[sc][0] for sc in _exp), {sc: (_ra[sc][0], _exp[sc][0]) for sc in _exp})
    _chk("T004-02: the line stands alone, and every check's EXAMINED number is still the number of rows it reads (a live-only count "
         "would be 0 here and a blocking check's floor would fail)",
         all(_ra[sc][1] == _exp[sc][1] and _ra[sc][1] is not None for sc in _exp), {sc: (_ra[sc][1], _exp[sc][1]) for sc in _exp})
    _hs = _ra[_T004_HS][2]
    _chk("T004-03: the handshake check no longer calls a table that holds rows empty, and says what it does not read",
         sum(_exp[_T004_EV][0]) > 0 and not re.search(r"(holds|has) 0 rows|table is empty", _hs) and "history and are not read" in _hs,
         "the empty-table sentence is still printed or the retired rows are not named")
    # The FAIL exit of the blocking check prints the line too (a failure over retired cells must not read as one over live ones).
    _f = os.path.join(_tmp4, "f.db")
    shutil.copy(_T004_LIVE, _f)
    _fc = sqlite3.connect(_f)
    _fc.execute("UPDATE convergence_assessment SET clinical_sources='not json' WHERE convergence_id="
                "(SELECT MIN(convergence_id) FROM convergence_assessment)")
    _fc.commit()
    _fc.close()
    _rf = _t004_run(_f, _T004_EV)
    _chk("T004-04: validate_evidence_state prints the line on its FAIL exit, with its EXAMINED number",
         _rf[3] == 1 and _rf[0] == _exp[_T004_EV][0] and _rf[1] is not None, (_rf[0], _rf[1], _rf[3]))
    # A database with no specifications table: the handshake check runs as it did (its own _table() guard) and the others do not crash.
    _e = os.path.join(_tmp4, "e.db")
    sqlite3.connect(_e).close()
    _re = _t004_run(_e, _T004_HS)
    _chk("T004-05: derivation_handshake_integrity on a database with no specifications table still ends with EXAMINED and a VERDICT",
         _re[1] is not None and "VERDICT:" in _re[2] and "Traceback" not in _re[2], _re[2][-200:])
    # One live determination on a copy: the cell is derived (an identity-only cell with a determination), its live row retired by the
    # verb, and the engine determines it again; each check says one more live.
    _c4 = sqlite3.connect(f"file:{_T004_LIVE}?mode=ro", uri=True)
    _cell4 = _c4.execute("SELECT parameter_id, identity_code FROM specifications WHERE identity_code IS NOT NULL AND icf_code IS NULL "
                         "AND needs_code IS NULL GROUP BY 1, 2 ORDER BY COUNT(*) DESC, 1, 2 LIMIT 1").fetchone()
    _slug4 = _c4.execute("SELECT slug FROM slugs WHERE status='ACTIVE' ORDER BY slug LIMIT 1").fetchone()
    _c4.close()
    if not _cell4 or not _slug4:
        print("  [SKIP] T004-06: SKIPPED-NO-FIXTURE: no identity-only cell with a determination, or no active slug")
    else:
        _b = os.path.join(_tmp4, "b.db")
        shutil.copy(_T004_LIVE, _b)
        _lv = sqlite3.connect(_b).execute("SELECT specification_id FROM specifications WHERE parameter_id=? AND identity_code=? AND "
                                          "icf_code IS NULL AND needs_code IS NULL AND retired_at IS NULL",
                                          _cell4).fetchall()
        _prep = [subprocess.run([sys.executable, os.path.join(REPO, "scripts", "db.py"), "retire-specification", "--specification-id",
                                 str(sid), "--reason", "TASK-FIXTURE T004", "--session", "session_t004-fixture"],
                                capture_output=True, text=True, env=dict(os.environ, GUIDEBOOK_DB_PATH=_b)) for (sid,) in _lv]
        _before4 = _t004_q(_b, "SELECT COALESCE(SUM(retired_at IS NULL),0), COALESCE(SUM(retired_at IS NOT NULL),0) FROM specifications")
        _eng = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "assess", "assess_cell.py"), "--db", _b, "--emit-sql",
                               os.path.join(_tmp4, "b.sql"), "--parameter-id", str(_cell4[0]), "--slug", _slug4[0], "--identity",
                               _cell4[1], "--session", "session_t004-fixture", "--stamp", "2026-01-01 00:00"],
                              capture_output=True, text=True)
        _exp4 = _t004_expect(_b)
        _rb = {sc: _t004_run(_b, sc) for sc in _exp4}
        _chk("T004-06: after one determination is written each check says one more live, and its EXAMINED number moves with the rows it reads",
             all(p.returncode == 0 for p in _prep) and _eng.returncode == 0
             and _t004_q(_b, "SELECT COALESCE(SUM(retired_at IS NULL),0) FROM specifications")[0] == _before4[0] + 1
             and all(_rb[sc][0] == _exp4[sc][0] and _rb[sc][1] == _exp4[sc][1] for sc in _exp4),
             {sc: (_rb[sc][0], _exp4[sc][0], _rb[sc][1], _exp4[sc][1]) for sc in _exp4})
except subprocess.CalledProcessError as _exc:                 # a fixture step failing is a failed case, not a crashed file
    _chk("T004-fixture: a fixture step ran", False, _exc)
finally:
    shutil.rmtree(_tmp4, ignore_errors=True)

if os.path.exists(DBP):
    os.remove(DBP)
print(f"EXAMINED: {len(_CASES)} case(s)")
print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}  ({len(fails)} failed)")
sys.exit(1 if fails else 0)
