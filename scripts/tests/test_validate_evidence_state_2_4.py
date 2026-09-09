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
    # The re-keyed table carries real typed FKs into the four lens registries and
    # base_parameters (owner 2026-08-28: "real FKs"), so the fixture needs those parents
    # or every INSERT dies on a missing table. Pulled live for the same reason as
    # specifications itself: they are the only place their current shape exists.
    live = [r[0] for r in con.execute(
        "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND ("
        "  name = 'specifications' OR tbl_name = 'specifications'"
        "  OR name IN ('base_parameters','axes','access_needs','base_taxonomy_medical'))")]
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
    # so nothing in this fixture references it. `populations` stays — it is the identity
    # lens (base_taxonomy_identity) and specifications.identity_code points at it.
    c.execute("CREATE TABLE populations(population_code TEXT PRIMARY KEY)")
    # description/category/priority are stubbed because v_pending selects them.
    # Not needed while nothing re-parses the views, but a stub parent that matches
    # the real column set is the honest fixture either way.
    c.execute("CREATE TABLE gaps(gap_id TEXT PRIMARY KEY, category TEXT, "
              "priority TEXT, description TEXT)")
    c.executemany("INSERT INTO populations VALUES(?)", [(x,) for x in ("AUT", "MOB", "DEAF")])
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
    c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,design_scale,convergence_id,governing_refs) "
              "VALUES (1,1,'AUT','stated','population',1,'[\"REF-1\"]')")
check("clean stated+convergent → 0 errors", run(clean) == [])

# stated without governing_refs — the anti-hallucination gate. Untested until now:
# the rule postdates this file, and the clean baseline was the only 'stated' row.
check("stated without governing_refs caught (anti-hallucination gate)",
      has(run(lambda c: (
          c.execute("INSERT INTO convergence_assessment(convergence_id,status,clinical_sources,co1_sources) "
                    "VALUES (1,'convergent','[\"REF-1\"]','[\"REF-2\"]')"),
          c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,design_scale,convergence_id) "
                    "VALUES (1,7,'MOB','stated','population',1)"))),
          "stated", "governing_refs"))

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
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state,convergence_id) "
                                  "VALUES (1,4,'AUT','provisional',NULL)")), "provisional", "confidence flag"))

# not_applicable without rationale
check("not_applicable without rationale caught",
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state) "
                                  "VALUES (1,5,'DEAF','not_applicable')")), "not_applicable", "rationale"))

# stated without convergence
check("stated without convergence caught",
      has(run(lambda c: c.execute("INSERT INTO specifications(specification_id,parameter_id,identity_code,state) "
                                  "VALUES (1,6,'AUT','stated')")), "stated", "convergence"))

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
