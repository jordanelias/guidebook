#!/usr/bin/env python3
"""
scripts/audit/identifier_floor_audit.py — an identifier is never reissued.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md section 1's burden of proof).
A source's `ref_id` is how every record outside the database names it: retrieval-log
manifests, session records, attestations, decision registers, pull-request bodies, and the
committed data migrations themselves. Those records are append-only and immutable. The
identifier they name is NOT: it is computed as MAX+1 over the live tables
(`dbcore.ref_id_high_water`), and `parameter_id` / `specification_id` are rowid aliases that
SQLite reassigns from 1 the moment a table is emptied.

So deleting rows silently frees identifiers that permanent records still claim. On 2026-09-13
the circulation-corpus clear did exactly that -- the ref_id mark fell REF-00982 -> REF-00970,
and the next mint would have been REF-00971, an id the batch-07 session record and its
attestation attribute to a specific scooter-manoeuvring study. Nothing caught it. Every gate
was green, because no gate was looking: the database was internally consistent and the
contradiction lived between the database and the record of what it used to hold.

What reaches the guidebook if this does not exist: a citation that names one paper and
resolves to another, with the audit trail agreeing with itself at every step.

WHY THIS IS A CHECK AND NOT A FIX. The fix for the 2026-09-13 regression is two things that
have already landed -- retired `ref_id`s retained as RETIRED rows in `source_locators`, and
AUTOINCREMENT on the two integer keys (migration 076). Both are floors: they repair identity
after a delete has destroyed it. Neither prevents the NEXT delete from doing the same thing to
some other key. This check is the general form of the rule, and it is the part that is
supposed to last:

    an identifier the permanent record has used is spent, whatever the live tables say.

WHERE THE HISTORICAL FLOOR COMES FROM, and why not from a table. A counter column or a
`retired_identifiers` table would be a second home for a fact (rule 5), and -- worse -- a home
that the same DELETE that causes this defect could empty. The committed data migrations under
`scripts/migrations/` cannot be emptied: they are append-only and immutable once committed
(CLAUDE.md rule 3), and every identifier this project has ever minted passed through one,
because the migration path is the only sanctioned route into the canonical database. So the
floor is derived by reading them. That is slower than a counter and it is the only source that
cannot be destroyed by the operation it guards.

EXAMINED counts identifiers compared, not files read (CLAUDE.md 5(a)).
"""
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = os.environ.get("GUIDEBOOK_DB_PATH", str(ROOT / "data" / "guidebook.db"))
MIGRATIONS = ROOT / "scripts" / "migrations"

# REF-NNNNN is the only mintable ref_id form dbcore treats as a high-water candidate;
# REF-VERIFIED-NNN and Co1-NN are separate, non-sequential namespaces (dbcore._MINTABLE).
_REF = re.compile(r"\bREF-(\d{5})\b")

# An INTEGER-keyed identifier is only recoverable from a migration where the column is
# named in an INSERT's column list, so the value can be located positionally. Rather than
# parse SQL, read the sequence SQLite itself maintains and compare it against the ids the
# migrations name in the one place they are unambiguous: an explicit INSERT INTO <table>
# ... VALUES (<id>, ... form, which is what emit_batch_sql.py produces for every row.
_INT_KEYS = {
    "base_parameters": re.compile(
        r'INSERT\s+INTO\s+"?base_parameters"?\s*\([^)]*\bparameter_id\b[^)]*\)\s*VALUES\s*\(\s*(\d+)',
        re.I),
    "specifications": re.compile(
        r'INSERT\s+INTO\s+"?specifications"?\s*\([^)]*\bspecification_id\b[^)]*\)\s*VALUES\s*\(\s*(\d+)',
        re.I),
}


def historical_floors():
    """The highest identifier the committed, immutable migrations have ever named."""
    ref_high = 0
    int_high = {t: 0 for t in _INT_KEYS}
    files = 0
    for path in sorted(MIGRATIONS.glob("*.sql")):
        text = path.read_text(encoding="utf-8", errors="replace")
        files += 1
        for m in _REF.finditer(text):
            ref_high = max(ref_high, int(m.group(1)))
        for table, rx in _INT_KEYS.items():
            for m in rx.finditer(text):
                int_high[table] = max(int_high[table], int(m.group(1)))
    return ref_high, int_high, files


def live_floors(con):
    """What the live database would hand out next, by its own rules."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import dbcore                                                    # noqa: E402
    ref_live = dbcore.ref_id_high_water(con)
    seqs = {}
    for table in _INT_KEYS:
        row = con.execute(
            "SELECT seq FROM sqlite_sequence WHERE name = ?", (table,)).fetchone()
        if row is not None:
            seqs[table] = ("sqlite_sequence", row[0])
            continue
        # No AUTOINCREMENT: SQLite will reissue MAX(rowid)+1, so the live floor is
        # whatever rows happen to remain -- which is exactly the defect this check exists
        # for, and it is reported as such rather than silently treated as a floor.
        col = "parameter_id" if table == "base_parameters" else "specification_id"
        mx = con.execute('SELECT COALESCE(MAX("%s"), 0) FROM "%s"' % (col, table)).fetchone()[0]
        seqs[table] = ("max(rowid) — NO AUTOINCREMENT", mx)
    return ref_live, seqs


def main():
    if not Path(DB).exists():
        print("FAIL: no database at %s" % DB)
        return 2
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)

    hist_ref, hist_int, files = historical_floors()
    live_ref, live_int = live_floors(con)

    failures = []
    examined = 1 + len(_INT_KEYS)

    print("EXAMINED: %d identifier floor(s) against %d committed migration file(s)"
          % (examined, files))
    print("  ref_id            historical REF-%05d   live REF-%05d" % (hist_ref, live_ref))
    for table, (how, val) in sorted(live_int.items()):
        print("  %-17s historical %-13d live %d  (%s)"
              % (table, hist_int[table], val, how))

    if live_ref < hist_ref:
        failures.append(
            "ref_id floor REGRESSED: the committed migrations have already minted "
            "REF-%05d, but the live high-water is REF-%05d, so the next mint would be "
            "REF-%05d -- an identifier permanent records already attribute to something "
            "else. Retain the retired ids (RETIRED rows in source_locators carrying their "
            "own DOI, so a re-admission cross-files to the original under R9) rather than "
            "letting them be reissued."
            % (hist_ref, live_ref, live_ref + 1))

    for table, (how, val) in sorted(live_int.items()):
        if val < hist_int[table]:
            failures.append(
                "%s floor REGRESSED: committed migrations name id %d, live floor is %d "
                "(%s), so the next row would reuse an id the permanent record has spent."
                % (table, hist_int[table], val, how))
        if "NO AUTOINCREMENT" in how and hist_int[table]:
            failures.append(
                "%s has no AUTOINCREMENT, so SQLite reissues MAX(rowid)+1 and emptying the "
                "table frees every id it held. Migration 076 added it to this table; a "
                "later rebuild that dropped it is the likeliest cause." % table)

    print("VERDICT: " + ("FAIL" if failures else "CLEAN"))
    for f in failures:
        print("  * " + f)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
