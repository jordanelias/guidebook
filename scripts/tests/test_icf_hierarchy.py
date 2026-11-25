#!/usr/bin/env python3
"""The ICF hierarchy (OD-74, OD-75; migration 167): `db.py import-icf-tree` and `db.py icf-glossary`, each rule shown to fire and to pass.

WHAT REACHES THE GUIDEBOOK WITHOUT THESE CASES. A block span or parent typed by hand rather than read from the persisted WHO
payload; a title replaced with a different title in the same cell, silently; a payload-sourced title overwritten; a stored range
that is not a WHO block (`d910–d920`) presented as one; an import that is not repeatable; a glossary that lists an umbrella
without its codes. Every probe writes a COPY of the database (the canonical file is not opened for writing) and reads the WHO
payload logged by the session that retrieved it.

  HI-1  a dry run writes nothing; the import mints every block, parents the held codes, names the untitled, and replaces a title
        whose source is not a payload, returning the old value and its source.
  HI-2  the span and parent of a block come from the payload: b765 sits under b750–b789 (Movement functions), which sits under
        b710–b799; a stored range WHO does not name is left alone and listed.
  HI-3  a second import changes nothing; a title sourced from a payload is never overwritten (it is refused and listed).
  HI-4  the glossary lists an umbrella with the codes beneath it and what links to each; an unknown umbrella is refused; a file
        that is not a WHO tabulation is refused.
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
shutil.copy(REPO / "data" / "guidebook.db", DB)
os.environ["GUIDEBOOK_DB_PATH"] = DB
sys.path.insert(0, str(REPO / "scripts"))
import db  # noqa: E402

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


con = sqlite3.connect(DB, isolation_level=None)
if "parent_code" not in [r[1] for r in con.execute("PRAGMA table_info(base_icf)")]:
    print("FAIL base_icf has no parent_code: apply migration 167")
    sys.exit(1)
q = lambda sql, *a: con.execute(sql, a).fetchall()                                       # noqa: E731
before = q("SELECT COUNT(*) FROM base_icf")[0][0]
held_range = q("SELECT icf_code FROM base_icf WHERE is_range = 1 AND icf_code = 'd910–d920'")
non_payload = {r[0]: r[1] for r in q("SELECT icf_code, title FROM base_icf WHERE title IS NOT NULL "
                                     "AND title_source NOT LIKE 'payload:%'")}

dry = db.import_icf_tree(payload=ZIP, session=SS, dry_run=True)
case("HI-1 a dry run reports work and writes nothing",
     bool(dry["inserted"]) and q("SELECT COUNT(*) FROM base_icf")[0][0] == before
     and q("SELECT COUNT(*) FROM base_icf WHERE parent_code IS NOT NULL")[0][0] == 0)
out = db.import_icf_tree(payload=ZIP, session=SS)
case("HI-1 the import mints blocks, each a range row whose title source is the payload",
     len(out["inserted"]) == q("SELECT COUNT(*) FROM base_icf")[0][0] - before and out["inserted"]
     and all(r[0] == 1 and r[1] == f"payload:{ZIP}" for r in q(
         "SELECT is_range, title_source FROM base_icf WHERE icf_code IN (%s)" % ",".join("?" * len(out["inserted"])), *out["inserted"])))
case("HI-1 every single code the project held now has a parent, and nothing is left untitled except what WHO does not name",
     q("SELECT COUNT(*) FROM base_icf WHERE parent_code IS NULL AND is_range = 0")[0][0] == 0
     and {r[0] for r in q("SELECT icf_code FROM base_icf WHERE title IS NULL")} <= set(out["unmatched"]))
case("HI-1 a title whose source is not a payload and differs from WHO's is replaced, with the old value and source returned",
     {r[0] for r in out["replaced"]} <= set(non_payload) and all(r[1] == non_payload[r[0]] and r[2] for r in out["replaced"])
     and all(q("SELECT title_source FROM base_icf WHERE icf_code=?", r[0])[0][0] == f"payload:{ZIP}" for r in out["replaced"]))
mv = q("SELECT title, parent_code FROM base_icf WHERE icf_code = 'b750–b789'")
case("HI-2 Movement functions is the block b750–b789, parented on b710–b799, named by the payload",
     mv == [("Movement functions", "b710–b799")])
case("HI-2 b765 and b770 sit under it",
     q("SELECT icf_code FROM base_icf WHERE parent_code = 'b750–b789' ORDER BY 1") == [("b765",), ("b770",)])
case("HI-2 d910–d920 is not a WHO block: left as stored, with no parent and no title, and listed",
     out["unmatched"] == ["d910–d920"] and q("SELECT parent_code, title FROM base_icf WHERE icf_code='d910–d920'") == [(None, None)])
again = db.import_icf_tree(payload=ZIP, session=SS)
case("HI-3 a second import changes nothing",
     not any(again[k] for k in ("inserted", "parented", "titled", "replaced", "refused")))
con.execute("UPDATE base_icf SET title='kept', title_source='payload:retrieval-log/other.zip' WHERE icf_code='d450'")
r3 = db.import_icf_tree(payload=ZIP, session=SS)
case("HI-3 a payload-sourced title that differs is refused, listed, and left",
     any(x.startswith("d450") for x in r3["refused"]) and q("SELECT title FROM base_icf WHERE icf_code='d450'") == [("kept",)])
g = db.icf_glossary("b750–b789")
case("HI-4 the glossary lists the umbrella with its codes and what links to each",
     g["count"] == 1 and [c["code"] for c in g["umbrellas"][0]["codes"]] == ["b765", "b770"]
     and g["umbrellas"][0]["title"] == "Movement functions" and g["umbrellas"][0]["codes"][0]["need_links"] >= 1)
case("HI-4 with no argument it lists the top umbrellas, and the codes beneath each are all held",
     all(u["codes"] for u in db.icf_glossary()["umbrellas"]))
case("HI-4 a code with nothing beneath it is not an umbrella", refused(db.icf_glossary, "b765"))
case("HI-4 a file that is not a WHO tabulation is refused", refused(db.import_icf_tree, payload=HTML, session=SS))

shutil.rmtree(TMP, ignore_errors=True)
print(f"EXAMINED: {len(RESULTS)}")
print(f"{RESULTS.count(False)} failed")
sys.exit(1 if False in RESULTS else 0)
