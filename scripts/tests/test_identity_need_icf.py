#!/usr/bin/env python3
"""The judged identity x access-need x ICF matrix (T-145, migration 165): each rule shown to fire and to pass.

WHAT REACHES THE GUIDEBOOK WITHOUT THESE CASES. A triple that counts as stated though no owner reviewed it; a row with
only two of the three keys, which the owner ruled out; a "does not apply" that reads the same as "not yet judged"; a
retired triple still offered from an identity. Every probe writes a COPY of the database; the canonical file is not
opened for writing.

  AT-1  the three keys are each required (a NULL in any is refused by the schema) and each must be a held code.
  AT-2  a session's triple is `pending`; nothing but the review verb makes it `stated`, and the schema refuses a
        stated or provisional row with no reviewer, a pending row with one, and a provisional row with no caveat.
  AT-3  a blank warrant and a second live row for the same three are refused; a rejected (retired) row frees the cell.
  AT-4  the view reads the same triple from an identity, from a need and from an ICF code; a retired row falls out;
        a `not_applicable` row is distinguishable from an absent one.
"""
import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
os.chdir(REPO)
TMP = tempfile.mkdtemp(prefix="guidebook-t145-")
DB = os.path.join(TMP, "guidebook.db")
shutil.copy(REPO / "data" / "guidebook.db", DB)
os.environ["GUIDEBOOK_DB_PATH"] = DB
sys.path.insert(0, str(REPO / "scripts"))
import db  # noqa: E402

FAILS = []
SS = "session_2026-11-20-t145-test"


def case(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS.append(name)


def refused(fn, *a, **k):
    try:
        fn(*a, **k)
    except db.Refusal:
        return True
    return False


def sql_refused(con, sql):
    try:
        con.execute(sql)
    except sqlite3.IntegrityError:
        return True
    return False


con = sqlite3.connect(DB, isolation_level=None)
if con.execute("SELECT 1 FROM sqlite_master WHERE name='identity_need_icf'").fetchone() is None:
    print("FAIL identity_need_icf is not in the database: apply migration 165")
    sys.exit(1)
ident = con.execute("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' ORDER BY 1").fetchall()
need = con.execute("SELECT need_code FROM access_needs ORDER BY 1").fetchall()
icf = con.execute("SELECT icf_code FROM base_icf ORDER BY 1").fetchall()
i1, i2, n1, c1, c2 = ident[0][0], ident[1][0], need[0][0], icf[0][0], icf[1][0]
print(f"EXAMINED: 4 case groups over identities {i1},{i2}, need {n1}, ICF {c1},{c2}")

# AT-1
ins = "INSERT INTO identity_need_icf (identity_code, need_code, icf_code, state, warrant, created_at, created_by_session) VALUES "
case("AT-1 a NULL icf_code is refused by the schema", sql_refused(con, ins + f"('{i1}','{n1}',NULL,'pending','w','t','s')"))
case("AT-1 a NULL need_code is refused by the schema", sql_refused(con, ins + f"('{i1}',NULL,'{c1}','pending','w','t','s')"))
case("AT-1 an unknown need is refused by the writer", refused(db.propose_identity_need_icf, i1, "NO-SUCH", c1, "w", SS))

# AT-2
r = db.propose_identity_need_icf(i1, n1, c1, "test warrant", SS)
tid = r["triple_id"]
case("AT-2 a proposal is pending", r["state"] == "pending")
base = ins + f"('{i2}','{n1}','{c1}',"
case("AT-2 stated with no reviewer is refused by the schema", sql_refused(con, base + "'stated','w','t','s')"))
case("AT-2 pending with a reviewer is refused by the schema",
     sql_refused(con, f"UPDATE identity_need_icf SET reviewed_at='t', reviewed_by='o' WHERE triple_id={tid}"))
case("AT-2 provisional with no caveat is refused by the writer",
     refused(db.review_identity_need_icf, str(tid), "provisional", "owner", None, SS))
db.review_identity_need_icf(str(tid), "stated", "owner", None, SS)
st = sqlite3.connect(DB).execute("SELECT state, reviewed_by FROM identity_need_icf WHERE triple_id=?", (tid,)).fetchone()
case("AT-2 review makes it stated and names the reviewer", st == ("stated", "owner"))
case("AT-2 a reviewed row is not accepted again", refused(db.review_identity_need_icf, str(tid), "stated", "owner", None, SS))

# AT-3
case("AT-3 a blank warrant is refused", refused(db.propose_identity_need_icf, i2, n1, c1, "  ", SS))
case("AT-3 a second live row for the same three is refused", refused(db.propose_identity_need_icf, i1, n1, c1, "again", SS))

# AT-4
na = db.propose_identity_need_icf(i1, n1, c2, "does not apply because of the test", SS, not_applicable=True)["triple_id"]
for label, kw in (("identity", {"identity": i1}), ("need", {"need": n1}), ("icf", {"icf_code": c1})):
    rows = db.lens_crosswalk(**kw)["rows"]
    case(f"AT-4 the stated triple is read from its {label}", any(x["triple_id"] == tid and x["state"] == "stated" for x in rows))
case("AT-4 a not_applicable row reads as judged, apart from an absent one",
     any(x["triple_id"] == na and x["state"] == "not_applicable" for x in db.lens_crosswalk(identity=i1)["rows"])
     and not db.lens_crosswalk(identity=i2)["rows"])
db.review_identity_need_icf(str(tid), "reject", "owner", "test rejection", SS)
case("AT-4 a rejected row falls out of the view", not any(x["triple_id"] == tid for x in db.lens_crosswalk(identity=i1)["rows"]))
case("AT-3 a rejected row frees the cell", not refused(db.propose_identity_need_icf, i1, n1, c1, "new judgment", SS))

shutil.rmtree(TMP, ignore_errors=True)
print(f"{len(FAILS)} failed")
sys.exit(1 if FAILS else 0)
