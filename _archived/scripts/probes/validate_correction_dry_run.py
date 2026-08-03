#!/usr/bin/env python3
import sqlite3

sql = open('scripts/migrations/data_20260521000000_full_db_metadata_corrections.sql').read()
conn = sqlite3.connect("/tmp/test_correction.db")
conn.execute("PRAGMA foreign_keys = ON")
try:
    conn.executescript(sql)
    conn.commit()
    print("Apply succeeded")
except sqlite3.Error as e:
    print(f"FAIL: {type(e).__name__}: {e}")
    raise

c = conn.cursor()
n_total = c.execute("SELECT COUNT(*) FROM evidence_sources").fetchone()[0]
n_elig = c.execute("""SELECT COUNT(*) FROM evidence_sources
WHERE metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY')
  AND verification_status IN ('VERIFIED','UNVERIFIED-1')""").fetchone()[0]
print(f"Total: {n_total}  Eligible: {n_elig}")
print()

checks = [
    ('REF-00028', 'Levine', 2021),
    ('REF-00150', 'Iker', 2019),
    ('REF-00176', 'Barker', 1968),
    ('REF-00233', 'Richardson', 2018),
    ('REF-00262', 'Carr', 2013),
    ('REF-00302', 'Mauldin', 2022),
    ('REF-00478', 'Passini', 1984),
    ('REF-00571', 'Kotloski', 2020),
    ('REF-00731', 'Szanton', 2019),
    ('REF-00735', 'Devos', 2019),
]
for ref, exp_author, exp_year in checks:
    r = c.execute("SELECT first_author_last, pub_year, doi FROM evidence_sources WHERE ref_id=?", (ref,)).fetchone()
    ok = r[0] == exp_author and r[1] == exp_year
    flag = 'OK' if ok else 'FAIL'
    print(f"  {flag}  {ref}: author={r[0]!r:25s} year={r[1]} doi={r[2]}")
