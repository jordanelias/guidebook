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
cell = EvidenceStateRecord(item_code="A-02", population="AUT", design_scale="population",
                           state="stated", convergence=conv)
check("stated cell with item_code + design_scale + directness convergence",
      cell.item_code == "A-02" and cell.design_scale == "population")
check("convergence carries directness-conditioned source lists",
      conv.down_weighted_sources == ["REF-099"] and conv.discounted_sources == ["REF-200"])
check("letter-suffixed item_code A-10b accepted",
      EvidenceStateRecord(item_code="A-10b", population="DEAF", state="not_applicable",
                          not_applicable_rationale="acoustic absorption not relevant to DEAF tactile profile").item_code == "A-10b")
reject("reject spec-layer SPEC-0001 as item_code",
       lambda: EvidenceStateRecord(item_code="SPEC-0001", population="AUT", state="stated"))
reject("reject out-of-vocab design_scale",
       lambda: EvidenceStateRecord(item_code="A-02", population="AUT", design_scale="molecular", state="stated"))
reject("pending without gap_register_id",
       lambda: EvidenceStateRecord(item_code="A-02", population="AUT", state="pending"))
reject("provisional without confidence_flag",
       lambda: EvidenceStateRecord(item_code="A-02", population="AUT", state="provisional"))
reject("not_applicable without rationale",
       lambda: EvidenceStateRecord(item_code="A-02", population="AUT", state="not_applicable"))
reject("divergent convergence without rationale",
       lambda: ConvergenceAssessment(status="divergent", clinical_sources=["REF-1"]))
check("pending with real gap id accepted",
      EvidenceStateRecord(item_code="A-08", population="MOB", state="pending", gap_register_id="GAP-001").gap_register_id == "GAP-001")

# ----------------------------------------------------------------------------
# Part 2 — table DDL constraints (shipped migration-024 SQL, stub parents)
# ----------------------------------------------------------------------------
SQL_PATH = os.path.join(os.path.dirname(__file__), "..", "migrations", "024_evidence_cell_state.sql")
ddl = open(SQL_PATH).read()

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys=ON")
# minimal parents matching the real PKs
db.execute("CREATE TABLE items(item_code TEXT PRIMARY KEY)")
db.execute("CREATE TABLE populations(population_code TEXT PRIMARY KEY)")
db.execute("CREATE TABLE gaps(gap_id TEXT PRIMARY KEY)")
db.executemany("INSERT INTO items VALUES (?)", [("A-02",), ("A-03",), ("A-08",)])
db.executemany("INSERT INTO populations VALUES (?)", [("AUT",), ("MOB",), ("DEAF",)])
db.execute("INSERT INTO gaps VALUES ('GAP-001')")
db.executescript(ddl)

check("both tables created from shipped DDL",
      {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")} >=
      {"evidence_cell_state", "convergence_assessment"})

db.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources) VALUES (1,'convergent','[\"REF-001\"]')")
db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,design_scale,convergence_id) VALUES (1,'A-02','AUT','stated','population',1)")
db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,gap_register_id) VALUES (2,'A-08','MOB','pending','GAP-001')")
check("valid stated + pending cells inserted", db.execute("SELECT COUNT(*) FROM evidence_cell_state").fetchone()[0] == 2)

reject("FK: non-existent item_code",
       lambda: db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state) VALUES (3,'Z-99','AUT','stated')"))
reject("FK: non-existent population_code",
       lambda: db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state) VALUES (4,'A-02','NOPE','stated')"))
reject("FK: non-existent gap_id",
       lambda: db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,gap_register_id) VALUES (5,'A-03','AUT','pending','GAP-99999')"))
reject("CHECK: bad state",
       lambda: db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state) VALUES (6,'A-03','AUT','halfbaked')"))
reject("CHECK: bad design_scale",
       lambda: db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,design_scale) VALUES (7,'A-03','AUT','stated','galactic')"))
reject("CHECK: bad convergence status",
       lambda: db.execute("INSERT INTO convergence_assessment(convergence_id,status) VALUES (2,'bogus')"))
reject("CHECK: non-boolean has_unverified_sources",
       lambda: db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,has_unverified_sources) VALUES (8,'A-03','AUT','stated',7)"))
reject("UNIQUE: duplicate (item_code,population)",
       lambda: db.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state) VALUES (9,'A-02','AUT','stated')"))
check("PRAGMA foreign_key_check clean", not db.execute("PRAGMA foreign_key_check").fetchall())
db.close()

print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}  ({len(fails)} failed)")
sys.exit(1 if fails else 0)
