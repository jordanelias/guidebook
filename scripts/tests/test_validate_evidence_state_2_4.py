"""Stage 2.4 — tests for the DB cell-state validator in validate_evidence_state.py.

Exercises the conditional cross-field rules that SQLite CHECK/FK cannot express
(pending⇒gap, provisional⇒confidence, not_applicable⇒rationale, stated⇒
convergence, convergent⇒≥2 axes, single_axis⇒≤1, divergent⇒rationale+synthesis,
and the §1.7 directness rule that a discounted source cannot also anchor).
Exit 0 = pass.
"""
import os
import sqlite3
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from validate_evidence_state import validate_db  # noqa: E402

fails = []
DDL = open(os.path.join(REPO, "scripts", "migrations", "024_evidence_cell_state.sql")).read()
fd, DBP = tempfile.mkstemp(suffix=".db"); os.close(fd)


def fresh():
    if os.path.exists(DBP):
        os.remove(DBP)
    c = sqlite3.connect(DBP)
    c.execute("CREATE TABLE items(item_code TEXT PRIMARY KEY)")
    c.execute("CREATE TABLE populations(population_code TEXT PRIMARY KEY)")
    c.execute("CREATE TABLE gaps(gap_id TEXT PRIMARY KEY)")
    c.executemany("INSERT INTO items VALUES(?)", [(x,) for x in ("A-02", "A-03", "A-04", "A-05", "A-06", "A-07")])
    c.executemany("INSERT INTO populations VALUES(?)", [(x,) for x in ("AUT", "MOB", "DEAF")])
    c.execute("INSERT INTO gaps VALUES('GAP-001')")
    c.executescript(DDL)
    return c


def run(setup, fk=True):
    c = fresh()
    c.execute(f"PRAGMA foreign_keys={'ON' if fk else 'OFF'}")
    setup(c)
    c.commit(); c.close()
    errors, _, _ = validate_db(DBP)
    return errors


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


def has(errs, *subs):
    return any(all(s in e for s in subs) for e in errs)


# clean baseline — a valid stated cell + convergent convergence (2 axes)
def clean(c):
    c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources) "
              "VALUES (1,'convergent','[\"REF-1\"]','[\"REF-2\"]')")
    c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,design_scale,convergence_id) "
              "VALUES (1,'A-02','AUT','stated','population',1)")
check("clean stated+convergent → 0 errors", run(clean) == [])

# pending without gap
check("pending without gap_register_id caught",
      has(run(lambda c: c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state) "
                                  "VALUES (1,'A-03','MOB','pending')")), "pending", "requires gap_register_id"))

# pending with gap not in gaps table (FK off to construct the row)
check("pending with unknown gap caught (defense-in-depth vs FK)",
      has(run(lambda c: c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,gap_register_id) "
                                  "VALUES (1,'A-03','MOB','pending','GAP-999')"), fk=False), "not in gaps table"))

# provisional without confidence flag
check("provisional without confidence flag caught",
      has(run(lambda c: c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,convergence_id) "
                                  "VALUES (1,'A-04','AUT','provisional',NULL)")), "provisional", "confidence flag"))

# not_applicable without rationale
check("not_applicable without rationale caught",
      has(run(lambda c: c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state) "
                                  "VALUES (1,'A-05','DEAF','not_applicable')")), "not_applicable", "rationale"))

# stated without convergence
check("stated without convergence caught",
      has(run(lambda c: c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state) "
                                  "VALUES (1,'A-06','AUT','stated')")), "stated", "convergence"))

# convergent with <2 axes
check("convergent with <2 axes caught",
      has(run(lambda c: c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources) "
                                  "VALUES (1,'convergent','[\"REF-1\"]')")), "convergent", "≥2 evidence axes"))

# single_axis with >1 axis
check("single_axis with >1 axis caught",
      has(run(lambda c: c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources,rationale) "
                                  "VALUES (1,'single_axis','[\"REF-1\"]','[\"REF-2\"]','clinical only')")), "single_axis", "axes present"))

# divergent without rationale + synthesis_approach
check("divergent without rationale/synthesis caught",
      has(run(lambda c: c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources) "
                                  "VALUES (1,'divergent','[\"REF-1\"]','[\"REF-2\"]')")), "divergent", "rationale"))

# directness (§1.7): a discounted source also listed as anchoring
check("discounted source also anchoring caught (§1.7)",
      has(run(lambda c: c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources,discounted_sources) "
                                  "VALUES (1,'convergent','[\"REF-1\"]','[\"REF-2\"]','[\"REF-1\"]')")), "discounted_sources also listed as anchoring"))

# malformed JSON column
check("malformed JSON source list caught",
      has(run(lambda c: c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources) "
                                  "VALUES (1,'convergent','not json','[\"REF-2\"]')")), "not a valid JSON array"))

if os.path.exists(DBP):
    os.remove(DBP)
print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}  ({len(fails)} failed)")
sys.exit(1 if fails else 0)
