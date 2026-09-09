"""Stage 2.3 — tests for the directness-aware cell-state machine.

Two parts: (1) the revised Pydantic models in schemas/evidence_state.py
(item_code cell key, design_scale, directness-conditioned convergence,
state-field validators); (2) the migration-024 table DDL — FK enforcement,
CHECK constraints, and the UNIQUE cell key — exercised against the shipped SQL
with stub parents. Exit 0 = pass.
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
fails = []


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


def reject(name, fn):
    try:
        fn(); check(name + " (NOT rejected!)", False)
    except Exception:
        check(name, True)


# ----------------------------------------------------------------------------
# Part 1 — models
# ----------------------------------------------------------------------------
from schemas.evidence_state import EvidenceStateRecord, ConvergenceAssessment  # noqa: E402

conv = ConvergenceAssessment(status="convergent", clinical_sources=["REF-001"],
                             co1_sources=["REF-050"], down_weighted_sources=["REF-099"],
                             discounted_sources=["REF-200"])
# Cell identity after migration 071: parameter_id is THE SUBJECT (owner 2026-08-26),
# the four lenses are THE LENS (owner 2026-08-28, relaxed by D-0182). item_code and
# population were the pre-071 key and are now refused outright.
cell = EvidenceStateRecord(parameter_id=1, identity_code="AUT", design_scale="population",
                           state="stated", convergence=conv)
check("stated cell with parameter_id + design_scale + directness convergence",
      cell.parameter_id == 1 and cell.design_scale == "population")
check("convergence carries directness-conditioned source lists",
      conv.down_weighted_sources == ["REF-099"] and conv.discounted_sources == ["REF-200"])
multi = EvidenceStateRecord(parameter_id=2, identity_code="DEAF", icf_code="b230",
                            needs_code="AN-HEAR", medical_code="H90", state="stated")
check("D-0182: a cell may be stated in several lenses at once",
      (multi.identity_code, multi.icf_code, multi.needs_code, multi.medical_code)
      == ("DEAF", "b230", "AN-HEAR", "H90"))
check("D-0182: one lens alone is enough — the other three stay None",
      EvidenceStateRecord(parameter_id=3, needs_code="AN-REACH",
                          state="not_applicable",
                          not_applicable_rationale="reach range not implicated"
                          ).identity_code is None)
reject("reject a cell stated in NO lens (D-0182 CHECK, mechanised)",
       lambda: EvidenceStateRecord(parameter_id=1, state="stated"))
reject("reject the retired item_code key (item layer emptied 2026-09-01)",
       lambda: EvidenceStateRecord(parameter_id=1, item_code="A-02",
                                   identity_code="AUT", state="stated"))
reject("reject the retired bare population key (populations is ONLY the identity lens)",
       lambda: EvidenceStateRecord(parameter_id=1, population="AUT", state="stated"))
reject("reject out-of-vocab design_scale",
       lambda: EvidenceStateRecord(parameter_id=1, identity_code="AUT",
                                   design_scale="molecular", state="stated"))
reject("pending without gap_register_id",
       lambda: EvidenceStateRecord(parameter_id=1, identity_code="AUT", state="pending"))
reject("provisional without confidence_flag",
       lambda: EvidenceStateRecord(parameter_id=1, identity_code="AUT", state="provisional"))
reject("not_applicable without rationale",
       lambda: EvidenceStateRecord(parameter_id=1, identity_code="AUT", state="not_applicable"))
reject("divergent convergence without rationale",
       lambda: ConvergenceAssessment(status="divergent", clinical_sources=["REF-1"]))
check("pending with real gap id accepted",
      EvidenceStateRecord(parameter_id=4, identity_code="MOB", state="pending",
                          gap_register_id="GAP-001").gap_register_id == "GAP-001")

# ----------------------------------------------------------------------------
# Part 2 — table DDL constraints (re-keyed table read LIVE, stub parents)
# ----------------------------------------------------------------------------
# The baseline is immutable and frozen at 2026-08-12, so it holds the PRE-071
# `specifications` — item_code, population_code, idx_specifications_item/_pop. A
# fixture built from it asserts against a table the database does not have, and
# passes: this file did exactly that until 2026-09-09, reporting "FK: non-existent
# item_code" green over a column dropped a fortnight earlier. So the re-keyed table,
# its indexes, and the parents its real FKs point into are read from the LIVE schema
# — the only place their current shape exists. `convergence_assessment` is untouched
# by 071 and still comes from the baseline.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _baseline_ddl import ddl_for  # noqa: E402

_con = sqlite3.connect("file:data/guidebook.db?mode=ro", uri=True)
_live = [r[0] for r in _con.execute(
    "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND ("
    "  name = 'specifications' OR tbl_name = 'specifications'"
    "  OR name IN ('base_parameters','terms','populations','axes',"
    "              'access_needs','base_taxonomy_medical'))")]
_con.close()
if not _live:
    print("  [FAIL] live schema has no `specifications` — fixture cannot be built.",
          file=sys.stderr)
    sys.exit(1)
# sqlite_master stores statements WITHOUT a trailing semicolon; executescript needs them.
ddl = ";\n".join(_live) + ";\n" + ddl_for("convergence_assessment")

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys=ON")
db.execute("CREATE TABLE gaps(gap_id TEXT PRIMARY KEY)")
db.execute("INSERT INTO gaps VALUES ('GAP-001')")
db.executescript(ddl)

check("both tables created from live + baseline DDL",
      {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")} >=
      {"specifications", "convergence_assessment", "base_parameters"})

STAMP = "2026-09-09T00:00:00Z"
SESS = "test_evidence_cell_state_2_3"
db.execute("INSERT INTO terms(term_id,canonical_en,created_at,created_by_session,"
           "updated_at,updated_by_session) VALUES ('TERM-0001','corridor clear width',?,?,?,?)",
           (STAMP, SESS, STAMP, SESS))
db.execute("INSERT INTO base_parameters(parameter_id,term_id,created_at,created_by_session) "
           "VALUES (1,'TERM-0001',?,?)", (STAMP, SESS))
db.execute("INSERT INTO populations(population_code,display_name) VALUES ('AUT','Autistic people')")
db.execute("INSERT INTO populations(population_code,display_name) VALUES ('MOB','Mobility')")
db.execute("INSERT INTO axes(axis_code,name,mechanism,coverage_status,falsification_condition) "
           "VALUES ('b230','Hearing functions','auditory demand','STUB',"
           "'a source shows the demand is not auditory')")

db.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources) "
           "VALUES (1,'convergent','[\"REF-001\"]')")
db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,"
           "design_scale,convergence_id) VALUES (1,1,'AUT','stated','population',1)")
db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,"
           "gap_register_id) VALUES (2,1,'MOB','pending','GAP-001')")
check("valid stated + pending cells inserted",
      db.execute("SELECT COUNT(*) FROM specifications").fetchone()[0] == 2)
check("D-0182 at the DB: a cell in several lenses at once is accepted",
      db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                 "icf_code,state) VALUES (3,1,'AUT','b230','stated')") is not None)

reject("CHECK: a cell in NO lens (D-0182 floor)",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,state) "
                          "VALUES (10,1,'stated')"))
reject("FK: non-existent parameter_id",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                          "state) VALUES (11,9999,'AUT','stated')"))
reject("FK: non-existent identity_code",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                          "state) VALUES (12,1,'NOPE','stated')"))
reject("FK: non-existent icf_code",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,icf_code,"
                          "state) VALUES (13,1,'zzz999','stated')"))
reject("FK: non-existent gap_id",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                          "state,gap_register_id) VALUES (14,1,'AUT','pending','GAP-99999')"))
reject("CHECK: bad state",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                          "state) VALUES (15,1,'AUT','halfbaked')"))
reject("CHECK: bad design_scale",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                          "state,design_scale) VALUES (16,1,'AUT','stated','galactic')"))
reject("CHECK: bad convergence status",
       lambda: db.execute("INSERT INTO convergence_assessment(convergence_id,status) VALUES (2,'bogus')"))
reject("CHECK: non-boolean has_unverified_sources",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                          "state,has_unverified_sources) VALUES (17,1,'AUT','stated',7)"))
reject("UNIQUE: duplicate (parameter_id, lens tuple)",
       lambda: db.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,"
                          "state) VALUES (18,1,'AUT','stated')"))
check("PRAGMA foreign_key_check clean", not db.execute("PRAGMA foreign_key_check").fetchall())
db.close()

print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}  ({len(fails)} failed)")
sys.exit(1 if fails else 0)
