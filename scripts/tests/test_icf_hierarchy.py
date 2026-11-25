"""The ICF hierarchy (OD-74, OD-75; migration 167): `db.py import-icf-tree`, `db.py icf-glossary` and the derived family rule, each shown to fire and to pass.

WHAT REACHES THE GUIDEBOOK WITHOUT THESE CASES. A block span or parent typed by hand rather than read from the persisted WHO
payload; a title replaced silently; a payload-sourced title overwritten; a stored range that is not a WHO block (`d910\u2013d920`)
presented as one; an import that is not repeatable, or that keeps a parent WHO has since changed; a glossary that does not end on a
cycle; a span with two keys (hyphen and en dash); a lens with a hierarchy that stops being derived from the schema. THE FIXTURE
IS BUILT HERE, not copied from the canonical database, so the cases keep their meaning after the data batch that runs the import
has landed (T-148): the canonical rows are neither read nor written.

  HI-0  the lens map has one home (`db._LENS_COLUMNS` is `dbcore.LENS_COLUMNS`); a lens has a hierarchy exactly when its
        registry has `parent_code` (identity and ICF yes, access need no); a database that predates the column reads each code as
        its own family.
  HI-1  a dry run writes nothing; the import mints every block, parents the held codes, names the untitled, replaces a title whose
        source is not a payload (returning the old value and source) and takes the payload as source of a title it confirms
        (returning the old title and source).
  HI-2  the span and parent of a block come from the payload (b765 under b750\u2013b789, Movement functions, under b710\u2013b799); a
        parent WHO names that the project does not hold is skipped for the next one up; a stored range WHO does not name is left alone.
  HI-3  a second import changes nothing; a code minted afterwards is parented by the next one; an intermediate code minted later
        takes over its children; a payload-sourced title that differs is refused.
  HI-4  the glossary lists an umbrella with the codes beneath it (finding it typed with a hyphen), labels the frozen map's count as
        frozen, ends on a parent cycle, and refuses a code with nothing beneath it; a file that is not a WHO tabulation is refused;
        `add-icf-code` gives one key to a span however its dash is typed.
  HI-5  cell-status holds a figure linked to a code in the cell of the umbrella above it (a copy of the canonical database).
"""
import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
os.chdir(REPO)
TMP = tempfile.mkdtemp(prefix="guidebook-icf-hierarchy-")
DB = os.path.join(TMP, "guidebook.db")
os.environ["GUIDEBOOK_DB_PATH"] = DB
sys.path.insert(0, str(REPO / "scripts"))
import db  # noqa: E402
import dbcore  # noqa: E402

SS = "session_2026-11-23-icf-hierarchy-test"
ZIP = "retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip"      # the persisted WHO ICF 2026-01 tabulation
HTML = "retrieval-log/session_2026-11-22-icf-umbrella-glossary/d2fd59c96965af9f.html"    # the browser's script shell: not a tabulation
RESULTS = []


def case(name, ok):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name)


def refused(fn, *a, **k):
    try:
        fn(*a, **k)
    except db.Refusal:
        return True
    return False


# The fixture: the live DDL of the four tables the verbs read, empty, then the rows each case needs.
live = sqlite3.connect(f"file:{REPO / 'data' / 'guidebook.db'}?mode=ro", uri=True)
con = sqlite3.connect(DB, isolation_level=None)
for (ddl,) in live.execute("SELECT sql FROM sqlite_master WHERE tbl_name IN ('base_icf','access_need_icf','identity_icf_map',"
                           "'identity_need_icf') AND sql IS NOT NULL AND type = 'table'"):
    con.execute(ddl)
if "parent_code" not in [r[1] for r in con.execute("PRAGMA table_info(base_icf)")]:
    print("FAIL base_icf has no parent_code: apply migration 167")
    sys.exit(1)
q = lambda sql, *a: con.execute(sql, a).fetchall()                                       # noqa: E731
EN = "\u2013"


def seed(code, title=None, source=None, rng=0):
    con.execute("INSERT INTO base_icf (icf_code, component, is_range, title, title_source, created_at, created_by_session) "
                "VALUES (?,?,?,?,?,'2026-11-23','seed')", (code, code[0], rng, title, source))


for c in ("b765", "b770", "d450", f"d310{EN}d329"):
    seed(c, rng=1 if EN in c else 0)
seed("d620", "Acquisition of goods/services", "skills/x.md")                 # a non-payload title that differs from WHO's
seed("d540", "Dressing", "skills/x.md")                                      # a non-payload title that WHO confirms
seed(f"d910{EN}d920", rng=1)                                                 # a stored range that is not a WHO block
seed("b1100")                                                                # its WHO parent b110 is not held

case("HI-0 the lens map has one home: db and the engine read the dbcore dict itself",
     db._LENS_COLUMNS is dbcore.LENS_COLUMNS)
mem = sqlite3.connect(":memory:")
mem.executescript("CREATE TABLE base_taxonomy_identity (identity_code TEXT PRIMARY KEY, parent_code TEXT);"
                  "CREATE TABLE base_icf (icf_code TEXT PRIMARY KEY, parent_code TEXT);"
                  "CREATE TABLE access_needs (need_code TEXT PRIMARY KEY, family TEXT);")
case("HI-0 a lens has a hierarchy exactly when its registry carries parent_code: identity and ICF do, the access need does not",
     [dbcore.family_sql(mem, c).startswith("(WITH RECURSIVE") for c in ("identity_code", "icf_code", "needs_code")] == [True, True, False])
mem.execute("ALTER TABLE base_icf DROP COLUMN parent_code")
case("HI-0 a database that predates the column reads each ICF code as its own family, and does not fail",
     dbcore.lens_families(mem, {"icf_code": "b750"}) == {"icf_code": {"b750"}})

before = q("SELECT COUNT(*) FROM base_icf")[0][0]
dry = db.import_icf_tree(payload=ZIP, session=SS, dry_run=True)
case("HI-1 a dry run reports work and writes nothing",
     bool(dry["inserted"]) and q("SELECT COUNT(*) FROM base_icf")[0][0] == before
     and q("SELECT COUNT(*) FROM base_icf WHERE parent_code IS NOT NULL")[0][0] == 0)
tree = db._who_tree(ZIP)
blocks = [n["code"] for n in tree if n["block"]]
out = db.import_icf_tree(payload=ZIP, session=SS)
case("HI-1 the import mints every WHO block it does not hold, each a range row sourced from the payload",
     sorted(out["inserted"]) == sorted(set(blocks) - {f"d310{EN}d329"})
     and all(r == (1, f"payload:{ZIP}") for r in q("SELECT is_range, title_source FROM base_icf WHERE icf_code IN (%s)"
                                                    % ",".join("?" * len(out["inserted"])), *out["inserted"])))
case("HI-1 a held block range takes its parent and title; every held single code takes a parent",
     q(f"SELECT parent_code, title FROM base_icf WHERE icf_code = 'd310{EN}d329'") == [(f"d310{EN}d399", "Communicating - receiving")]
     and q("SELECT COUNT(*) FROM base_icf WHERE parent_code IS NULL AND is_range = 0")[0][0] == 0)
case("HI-1 a title whose source is not a payload and differs from WHO's is replaced, with the old value and source returned",
     out["replaced"] == [["d620", "Acquisition of goods/services", "skills/x.md", "Acquisition of goods and services"]]
     and q("SELECT title_source FROM base_icf WHERE icf_code = 'd620'") == [(f"payload:{ZIP}",)])
case("HI-1 a title the payload confirms takes the payload's wording and source, and the old title and source are returned",
     out["confirmed"] == [["d540", "Dressing", "skills/x.md"]] and q("SELECT title, title_source FROM base_icf WHERE icf_code = 'd540'") == [("Dressing", f"payload:{ZIP}")])
case(f"HI-2 Movement functions is the block b750{EN}b789, parented on b710{EN}b799, named by the payload, with b765 and b770 beneath it",
     q(f"SELECT title, parent_code FROM base_icf WHERE icf_code = 'b750{EN}b789'") == [("Movement functions", f"b710{EN}b799")]
     and q(f"SELECT icf_code FROM base_icf WHERE parent_code = 'b750{EN}b789' ORDER BY 1") == [("b765",), ("b770",)])
case("HI-2 a held code whose WHO parent is not held takes the next one up, and the insert does not fail",
     q("SELECT parent_code FROM base_icf WHERE icf_code = 'b1100'") == [(f"b110{EN}b139",)])
case(f"HI-2 d910{EN}d920 is not a WHO block: left as stored, with no parent and no title, and listed",
     out["unmatched"] == [f"d910{EN}d920"] and q(f"SELECT parent_code, title FROM base_icf WHERE icf_code='d910{EN}d920'") == [(None, None)])
again = db.import_icf_tree(payload=ZIP, session=SS)
case("HI-3 a second import changes nothing",
     not any(again[k] for k in ("inserted", "parented", "reparented", "titled", "replaced", "confirmed", "refused")))
db.insert_icf_code(icf_code="b110", session=SS)               # minted afterwards, with no second import
case("HI-3 a code minted afterwards that WHO places between a code and its parent is parented at once, and takes its children: "
     "b110 under its block, b1100 under b110, with no second import",
     q("SELECT parent_code FROM base_icf WHERE icf_code = 'b110'") == [(f"b110{EN}b139",)]
     and q("SELECT parent_code FROM base_icf WHERE icf_code = 'b1100'") == [("b110",)]
     and dbcore.lens_families(con, {"icf_code": "b110"})["icf_code"] == {"b110", "b1100"})
r2 = db.import_icf_tree(payload=ZIP, session=SS)
case("HI-3 the import afterwards moves nothing and only names the code minted without a title (the mint parents, the import titles)",
     r2["titled"] == ["b110"] and not any(r2[k] for k in ("inserted", "parented", "reparented", "replaced", "confirmed", "refused")))
con.execute("UPDATE base_icf SET title='kept', title_source='payload:retrieval-log/other.zip' WHERE icf_code='d450'")
r3 = db.import_icf_tree(payload=ZIP, session=SS)
case("HI-3 a payload-sourced title that differs is refused, listed, and left",
     any(x.startswith("d450") for x in r3["refused"]) and q("SELECT title FROM base_icf WHERE icf_code='d450'") == [("kept",)])
g = db.icf_glossary(f"b750{EN}b789")
LINKS = ("access_need_icf_rows", "identity_icf_map_rows (frozen, OD-77)", "identity_need_icf_reviewed", "identity_need_icf_pending")
case("HI-4 the glossary lists the umbrella with its codes and the labelled counts of what links to each, the frozen map named as frozen",
     g["count"] == 1 and [c["code"] for c in g["umbrellas"][0]["codes"]] == ["b765", "b770"]
     and g["umbrellas"][0]["title"] == "Movement functions"
     and all(c[k] == 0 for c in g["umbrellas"][0]["codes"] for k in LINKS))
case("HI-4 the glossary finds an umbrella typed with a hyphen, as the owner types it",
     db.icf_glossary("b750-b789")["count"] == 1)
case("HI-4 with no argument it lists the top umbrellas, and each has codes beneath it",
     all(u["codes"] for u in db.icf_glossary()["umbrellas"]))
case("HI-4 a code with nothing beneath it is not an umbrella", refused(db.icf_glossary, "b765"))
con.execute(f"UPDATE base_icf SET parent_code = 'b765' WHERE icf_code = 'b750{EN}b789'")        # a cycle: b765 > b750-b789 > b765
case("HI-4 the glossary ends on a parent cycle, and so does the family, which is every code on it",
     len(db.icf_glossary("b765")["umbrellas"]) == 1
     and dbcore.lens_families(con, {"icf_code": "b765"})["icf_code"] == {"b765", f"b750{EN}b789", "b770"})
con.execute(f"UPDATE base_icf SET parent_code = 'b710{EN}b799' WHERE icf_code = 'b750{EN}b789'")
for typed in ("e100-e199", f"e100 {EN} e199", "e100\u2014e199"):
    try:
        db.insert_icf_code(icf_code=typed, session=SS)
    except db.Refusal:
        pass                                                  # the second and third are the same span: refused as already held
case("HI-4 a span typed with a hyphen, a spaced en dash or an em dash is one key, the unspaced en dash the import mints",
     q("SELECT icf_code FROM base_icf WHERE icf_code LIKE 'e100%'") == [(f"e100{EN}e199",)])
case("HI-4 a file that is not a WHO tabulation is refused", refused(db.import_icf_tree, payload=HTML, session=SS))

# HI-5: cell-status reads an ICF umbrella's figures through the hierarchy. On a copy of the canonical database (read for one
# extraction, whichever there is), a figure linked to b765 is held by the cell keyed on its umbrella and not by an unrelated one.
CAN = os.path.join(TMP, "canonical-copy.db")
shutil.copy(REPO / "data" / "guidebook.db", CAN)
os.environ["GUIDEBOOK_DB_PATH"] = CAN
db.import_icf_tree(payload=ZIP, session=SS)                 # a no-op once the data batch has landed
c2 = sqlite3.connect(CAN, isolation_level=None)
ex, par = c2.execute("SELECT extraction_id, parameter_id FROM source_value_extractions WHERE retired_at IS NULL LIMIT 1").fetchone()
c2.execute("INSERT INTO base_icf (icf_code, component, is_range, created_at, created_by_session) SELECT 'b765','b',0,'2026-11-23','seed' "
           "WHERE NOT EXISTS (SELECT 1 FROM base_icf WHERE icf_code='b765')")
c2.execute("INSERT INTO extraction_lens_links (extraction_id, icf_code, basis, basis_text, created_at, created_by_session, "
           "updated_at, updated_by_session) VALUES (?, 'b765', 'named_in_text', 'seed', '2026-11-23', 'seed', '2026-11-23', 'seed')", (ex,))
held = lambda icf: ex in db.cell_status(par, icf=icf)["stages"]["judgment"]["held"]                # noqa: E731
case("HI-5 cell-status holds a figure linked to b765 in the cell of its umbrella and of its own code, and not in an unrelated one",
     held("b765") and held(f"b750{EN}b789") and held(f"b710{EN}b799") and not held("b770"))

shutil.rmtree(TMP, ignore_errors=True)
print(f"EXAMINED: {len(RESULTS)}")
print(f"{RESULTS.count(False)} failed")
sys.exit(1 if False in RESULTS else 0)
