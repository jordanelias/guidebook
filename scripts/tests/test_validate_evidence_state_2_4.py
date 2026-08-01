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
MIGRATIONS = os.path.join(REPO, "scripts", "migrations")
sys.path.insert(0, os.path.join(REPO, "scripts"))
from validate_evidence_state import CELL_STATE_REQUIRED, validate_db  # noqa: E402

fails = []


def schema_ddl():
    """The cell-state DDL, discovered from the migrations rather than pinned to one.

    The fixture used to read 024 alone. 026 then rebuilt the table (adding
    governing_refs et al.) and 027 added regulatory_stratum_only, so the fixture
    fell behind a validator that selects those columns and the whole file died
    with `no such column: governing_refs` before asserting anything. Collecting
    every schema migration that touches these two tables keeps the fixture
    tracking the schema instead of re-pinning it to a newer number that will
    rot the same way. Verified to reproduce the live table definitions exactly.
    """
    out = []
    for fn in sorted(os.listdir(MIGRATIONS)):
        m = re.match(r"^(\d{3})_.*\.sql$", fn)
        if not m:
            continue  # data_*.sql are rows, not shape
        text = open(os.path.join(MIGRATIONS, fn)).read()
        body = "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("--"))
        if "evidence_cell_state" in body or "convergence_assessment" in body:
            out.append((int(m.group(1)), text))
    return [text for _, text in sorted(out)]


DDL = schema_ddl()
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
    for step in DDL:
        c.executescript(step)
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
    present = {r[1] for r in c.execute("PRAGMA table_info(evidence_cell_state)")}
    c.close()
    # Imported, not restated. A second hardcoded copy of the validator's column
    # list would silently stop covering any column added there — the guard would
    # keep passing while checking less, which is the failure it exists to catch.
    missing = sorted(set(CELL_STATE_REQUIRED) - present)
    if missing:
        print(f"  [FAIL] fixture schema is stale — evidence_cell_state lacks {missing}.\n"
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
    # governing_refs is required on 'stated' (anti-hallucination gate, §2.7). The
    # baseline predated that rule, so it was not clean once the fixture caught up.
    c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,design_scale,convergence_id,governing_refs) "
              "VALUES (1,'A-02','AUT','stated','population',1,'[\"REF-1\"]')")
check("clean stated+convergent → 0 errors", run(clean) == [])

# stated without governing_refs — the anti-hallucination gate. Untested until now:
# the rule postdates this file, and the clean baseline was the only 'stated' row.
check("stated without governing_refs caught (anti-hallucination gate)",
      has(run(lambda c: (
          c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources) "
                    "VALUES (1,'convergent','[\"REF-1\"]','[\"REF-2\"]')"),
          c.execute("INSERT INTO evidence_cell_state(cell_id,item_code,population_code,state,design_scale,convergence_id) "
                    "VALUES (1,'A-07','MOB','stated','population',1)"))),
          "stated", "governing_refs"))

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
