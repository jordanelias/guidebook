#!/usr/bin/env python3
"""
scripts/audit/translation_pointer_audit.py -- every current translation still translates the cell it points at.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT IT (T-049): a translation shown beside a quotation it no longer
translates. SQLite cannot hold a foreign key to "any cell", so `translations.source_*` is a pointer nothing else
enforces, and `source_sha256` is how a change to the original is seen.

For every CURRENT translation (status translated or reviewed, not retired) it checks that
  * the pointer resolves to a text cell today (`dbcore.read_cell`, the one rule the verbs use);
  * the cell's hash is the one recorded when it was translated;
  * the translation states the original's numbers and no others (`db.translation_number_gaps`, the rule
    `db.py record-translation` applies at write time).
Prints `EXAMINED: <n>`, the current translations. Zero until the first translation is recorded.

Usage:  python3 scripts/audit/translation_pointer_audit.py
Exit 0 every current translation holds; 1 one does not; 2 cannot run.
"""
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import dbcore                                                          # noqa: E402
import db                                                              # noqa: E402

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))


def main():
    if not DB_PATH.exists():
        print(f"translation_pointer_audit: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='translations'").fetchone():
            print("translation_pointer_audit: the translations table is absent", file=sys.stderr)
            return 2
        rows = conn.execute("SELECT * FROM translations WHERE status IN ('translated', 'reviewed') "
                            "AND superseded_by_translation_id IS NULL ORDER BY translation_id").fetchall()
        bad = []
        for r in rows:
            tid, where = r["translation_id"], (r["source_table"], r["source_column"], r["source_row_key"])
            original, _, why = dbcore.read_cell(conn, *where)
            if why:
                bad.append(f"translation {tid}: the pointer does not resolve: {why}")
            elif db.translation_sha256(original) != r["source_sha256"]:
                bad.append(f"translation {tid}: the original at {where[0]}.{where[1]} [{where[2]}] "
                           f"has changed since it was translated")
            else:
                dropped, added = db.translation_number_gaps(original, r["translated_text"],
                                                            db.translation_claimed_value(conn, *where))
                if dropped or added:
                    bad.append(f"translation {tid}: numbers dropped {dropped or 'none'}, added {added or 'none'}")
    finally:
        conn.close()
    print("translation_pointer_audit -- every current translation still translates the cell it points at")
    print(f"EXAMINED: {len(rows)}")
    for b in bad:
        print(f"  FAIL: {b}")
    if bad:
        return 1
    print("PASS: every current translation resolves, matches its cell's hash and keeps its numbers"
          if rows else "PASS: no current translation yet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
