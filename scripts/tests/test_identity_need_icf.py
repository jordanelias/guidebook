#!/usr/bin/env python3
"""The judged identity x access-need x ICF matrix (T-145, migrations 165 and 166): each rule shown to fire and to pass.

WHAT REACHES THE GUIDEBOOK WITHOUT THESE CASES. A triple that counts as stated though no owner reviewed it (a session
typing a name into a free-text cell); a row with fewer than the three keys the owner ruled; a "does not apply" that
reads the same as "not yet judged"; a retired or reviewed row edited afterwards by a data migration; an unreviewed
proposal that hides a gap. Every probe writes a COPY of the database; the canonical file is not opened for writing, and
the ledger the review is bound to is a temporary file.

  AT-1  each key is required by the schema and must be a held, live code at the writer.
  AT-2  a proposal is pending; only the review verb, bound to an owner ledger entry that names the triple, makes it
        stated; the schema refuses a stated row with no review, a pending row with one, a provisional row with no
        caveat; a batch with one refused row writes nothing; a dry run writes nothing.
  AT-3  a blank warrant and a second live row for the same three are refused; a rejected row records its owner entry
        and reason, frees the cell, and can no longer be edited; a recorded review and a triple's keys cannot be edited.
  AT-4  the view reads one triple from an identity, a need and an ICF code; a not_applicable row is distinguishable
        from an absent one; `--uncovered` counts only reviewed rows; `--retired` lists the rejected.
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
import db      # noqa: E402
import dbcore  # noqa: E402

SS = "session_2026-11-20-t145-test"
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


def sql_refused(sql):
    try:
        con.execute(sql)
    except sqlite3.DatabaseError:
        return True
    return False


def row(tid):
    return con.execute("SELECT state, review_ref, reviewed_session, review_note, retired_at, retirement_ref "
                       "FROM identity_need_icf WHERE triple_id=?", (tid,)).fetchone()


con = sqlite3.connect(DB, isolation_level=None)
if con.execute("SELECT 1 FROM sqlite_master WHERE name='identity_need_icf'").fetchone() is None:
    print("FAIL identity_need_icf is not in the database: apply migrations 165 and 166")
    sys.exit(1)
idents = [r[0] for r in con.execute("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' ORDER BY 1")]
needs = [r[0] for r in con.execute("SELECT need_code FROM access_needs ORDER BY 1")]
icfs = [r[0] for r in con.execute("SELECT icf_code FROM base_icf ORDER BY 1")]
live = set(con.execute("SELECT identity_code, need_code, icf_code FROM identity_need_icf WHERE retired_at IS NULL"))
free = [(i, n, c) for i in idents[:6] for n in needs[:3] for c in icfs[:6] if (i, n, c) not in live]
(i1, n1, c1) = free[0]
(i2, n2, c2) = next(t for t in free if all(a != b for a, b in zip(t, (i1, n1, c1))))
(i3, n3, c3) = next(t for t in free if all(a not in (b, c) for a, b, c in zip(t, (i1, n1, c1), (i2, n2, c2))))
deprecated = con.execute("SELECT identity_code FROM base_taxonomy_identity WHERE status='deprecated'").fetchone()

LEDGER = os.path.join(TMP, "ledger.md")
OWNER = "Owner statements 2026-11-20 (test review)"

# AT-1
ins = ("INSERT INTO identity_need_icf (identity_code, need_code, icf_code, state, warrant, created_at, "
       "created_by_session) VALUES ")
case("AT-1 a NULL identity is refused by the schema", sql_refused(ins + f"(NULL,'{n1}','{c1}','pending','w','t','s')"))
case("AT-1 a NULL need is refused by the schema", sql_refused(ins + f"('{i1}',NULL,'{c1}','pending','w','t','s')"))
case("AT-1 a NULL icf_code is refused by the schema", sql_refused(ins + f"('{i1}','{n1}',NULL,'pending','w','t','s')"))
case("AT-1 an unknown identity is refused by the writer", refused(db.propose_identity_need_icf, "NO-SUCH", n1, c1, "w", SS))
case("AT-1 an unknown need is refused by the writer", refused(db.propose_identity_need_icf, i1, "NO-SUCH", c1, "w", SS))
case("AT-1 an unknown ICF code is refused by the writer", refused(db.propose_identity_need_icf, i1, n1, "z999", "w", SS))
if deprecated:
    case("AT-1 a deprecated identity is refused by the writer",
         refused(db.propose_identity_need_icf, deprecated[0], n1, c1, "w", SS))

# AT-2
t1 = db.propose_identity_need_icf(i1, n1, c1, "warrant one", SS)["triple_id"]
t2 = db.propose_identity_need_icf(i2, n2, c2, "warrant two", SS)["triple_id"]
t3 = db.propose_identity_need_icf(i3, n3, c3, "warrant three", SS, not_applicable=True)["triple_id"]
Path(LEDGER).write_text(
    f"## {OWNER}\nThe owner reviewed TRIPLE-{t1} TRIPLE-{t2} TRIPLE-{t3} and TRIPLE-9999.\n\n"
    f"## Session test heading\nTRIPLE-{t1} TRIPLE-{t2} TRIPLE-{t3}.\n\n"
    f"## Owner statements 2026-11-20 (names only one)\nTRIPLE-{t1}.\n", encoding="utf-8")
dbcore.LEDGER_PATH = Path(LEDGER)
case("AT-2 a proposal is pending and a non-link is not_applicable", row(t1)[0] == "pending" and row(t3)[0] == "not_applicable")
case("AT-2 stated with no review is refused by the schema",
     sql_refused(f"UPDATE identity_need_icf SET state='stated' WHERE triple_id={t1}"))
case("AT-2 a pending row carrying a review is refused by the schema",
     sql_refused(f"UPDATE identity_need_icf SET review_ref='Owner x', reviewed_at='t', reviewed_session='s' "
                 f"WHERE triple_id={t1}"))
case("AT-2 a session heading approves nothing", refused(db.review_identity_need_icf, str(t1), "stated", "Session test heading", None, SS))
case("AT-2 an owner entry that does not name the triple approves nothing",
     refused(db.review_identity_need_icf, str(t2), "stated", "Owner statements 2026-11-20 (names only one)", None, SS))
case("AT-2 provisional with no caveat is refused", refused(db.review_identity_need_icf, str(t1), "provisional", OWNER, None, SS))
case("AT-2 provisional on a judged non-link is refused", refused(db.review_identity_need_icf, str(t3), "provisional", OWNER, "c", SS))
case("AT-2 a batch with one refused row writes nothing",
     refused(db.review_identity_need_icf, f"{t1},9999", "stated", OWNER, None, SS) and row(t1)[0] == "pending")
db.review_identity_need_icf(f"{t1},{t3}", "stated", OWNER, None, SS, dry_run=True)
case("AT-2 a dry run writes nothing", row(t1)[0] == "pending")
db.review_identity_need_icf(f"{t1},{t3}", "stated", OWNER, None, SS)
case("AT-2 review states a pending row and records the entry and the running session",
     row(t1)[:3] == ("stated", OWNER, "session_2026-11-20-t145-test"))
case("AT-2 review stamps a not_applicable row and keeps its state", row(t3)[0] == "not_applicable" and row(t3)[1] == OWNER)
case("AT-2 an accept is not repeated on a reviewed row", refused(db.review_identity_need_icf, str(t1), "stated", OWNER, None, SS))
db.review_identity_need_icf(str(t2), "provisional", OWNER, "caveat words", SS)
case("AT-2 provisional records its caveat", row(t2)[0] == "provisional" and row(t2)[3] == "caveat words")

# AT-3
case("AT-3 a blank warrant is refused", refused(db.propose_identity_need_icf, i2, n1, c1, "  ", SS))
case("AT-3 a second live row for the same three is refused", refused(db.propose_identity_need_icf, i1, n1, c1, "again", SS))
case("AT-3 a recorded review cannot be erased",
     sql_refused(f"UPDATE identity_need_icf SET review_ref=NULL, reviewed_at=NULL, reviewed_session=NULL WHERE triple_id={t1}"))
for name, sql in (("a warrant", f"UPDATE identity_need_icf SET warrant='x' WHERE triple_id={t1}"),
                  ("a key", f"UPDATE identity_need_icf SET icf_code='{next(c for c in icfs if c != c1)}' WHERE triple_id={t1}"),
                  ("a state", f"UPDATE identity_need_icf SET state='pending' WHERE triple_id={t1}")):
    try:
        con.execute(sql)
        edited = True
    except sqlite3.DatabaseError:
        edited = False
    case(f"AT-3 {name} of a reviewed row cannot be edited", not edited)
case("AT-3 a reject without a reason is refused", refused(db.review_identity_need_icf, str(t1), "reject", OWNER, None, SS))
db.review_identity_need_icf(str(t1), "reject", OWNER, "owner rejected it", SS)
case("AT-3 a reject records the owner entry and the reason and retires in place",
     row(t1)[4] is not None and row(t1)[5] == OWNER)
case("AT-3 a rejected row frees the cell", not refused(db.propose_identity_need_icf, i1, n1, c1, "new judgment", SS))
try:
    con.execute(f"UPDATE identity_need_icf SET retired_at=NULL, retired_by_session=NULL, retirement_reason=NULL, "
                f"retirement_ref=NULL WHERE triple_id={t1}")
    revived = True
except sqlite3.DatabaseError:
    revived = False
case("AT-3 a retired row cannot be revived", not revived)
case("AT-3 a retired row cannot be reviewed", refused(db.review_identity_need_icf, str(t1), "reject", OWNER, "again", SS))

# AT-4
for label, kw in (("identity", {"identity": i2}), ("need", {"need": n2}), ("icf", {"icf_code": c2})):
    got = db.lens_crosswalk(**kw)["rows"]
    case(f"AT-4 the provisional triple is read from its {label}, with its caveat",
         any(x["triple_id"] == t2 and x["review_note"] == "caveat words" and x["review_ref"] == OWNER for x in got))
case("AT-4 a not_applicable row reads as judged, apart from an absent one",
     any(x["triple_id"] == t3 and x["state"] == "not_applicable" for x in db.lens_crosswalk(identity=i3)["rows"])
     and not db.lens_crosswalk(identity=idents[-1], need=needs[-1], icf_code=icfs[-1])["rows"])
case("AT-4 a rejected row falls out of the view", not any(x["triple_id"] == t1 for x in db.lens_crosswalk(identity=i1)["rows"]))
case("AT-4 --retired lists the rejected row with its reason",
     any(x["triple_id"] == t1 and x["retirement_reason"] == "owner rejected it" for x in db.lens_crosswalk(retired=True)["rows"]))
unc = db.lens_crosswalk(uncovered=True)
# the proposal that freed cell (i1, n1, c1) after the reject is still pending, so it must not cover i1 or n1
case("AT-4 an unreviewed proposal does not cover its identity or need; a reviewed one does",
     i1 in unc["identities_without_a_reviewed_triple"] and n1 in unc["needs_without_a_reviewed_triple"]
     and i2 not in unc["identities_without_a_reviewed_triple"] and n2 not in unc["needs_without_a_reviewed_triple"])

shutil.rmtree(TMP, ignore_errors=True)
print(f"EXAMINED: {len(RESULTS)}")
print(f"{RESULTS.count(False)} failed")
sys.exit(1 if False in RESULTS else 0)
