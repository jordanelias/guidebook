#!/usr/bin/env python3
"""
scripts/audit/derived_not_curated_audit.py — CLAUDE.md rule 8, mechanised.

THE RULE: derive it, or name who judged it. Never curate a fact the machine can compute.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS. A curated list and the thing it
describes drift, and only the list is ever read. Every instance found on 2026-09-13 failed
in the SAFE-LOOKING direction, which is why none was noticed:

  * `dbcore.WRITABLE_TABLES` — a hand list of the tables a session may write. Blind eight
    times. A `gap_mining` row written through the sanctioned CLI was captured as nothing
    and the session was told "no delta — nothing to emit".
  * `db.py --verification-method` — an argparse `choices=` list missing `direct-render`
    for as long as that value had existed, so the CLI REFUSED a value the schema admits.
  * `PRE_075_UNGRADED_IDS` — a frozen id list that outlived the rows it froze.
  * `governance/check-registry.yaml`'s "N today" counts — every one measured stale.

None of those made a wrong claim reach the book directly. Each made a TRUE thing
unreachable, or a checkable thing uncheckable, which is how a corpus quietly stops being
verifiable.

WHAT THIS CHECKS, and why only this class for now. Rule 8 is general and most of it is
judgement, which a script cannot police. ONE class of violation is mechanically decidable:
an argparse `choices=` literal whose values are exactly a live column's CHECK vocabulary.
That is a second home with a first home sitting next to it, and the fix is always the same
(`dbcore.schema_choices(table, column)`). The other known violations named in rule 8 —
`--ref-id` and `--tier` asking for derivable values, the curated `MODEL_TABLE_MAP`, the
registry's counts — need judgement about what the single home should BE, so they are
listed in the rule for a reader rather than asserted here.

A CHECK THAT GREPS ITS OWN REPOSITORY, deliberately. The alternative is importing db.py
and inspecting the parser, which would run module-level code and couple this gate to the
writer it polices — the thing dbcore's own docstring says a gate must not do.

EXAMINED counts `choices=` literals inspected, not files read.
"""
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = os.environ.get("GUIDEBOOK_DB_PATH", str(ROOT / "data" / "guidebook.db"))

#: Files whose argparse parsers are in scope. The writers; a report script that offers a
#: fixed menu of its own output formats is not restating a schema vocabulary.
SCANNED = ("scripts/db.py",)

_CHOICES = re.compile(r"choices=\[([^\]]*)\]")
_LITERAL = re.compile(r'"([^"]*)"|\'([^\']*)\'')


def check_vocabularies(con):
    """Every column CHECK vocabulary in the live schema, keyed by its value set."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import dbcore                                                    # noqa: E402
    out = {}
    for (table,) in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"):
        for col in con.execute('PRAGMA table_info("%s")' % table):
            vals = dbcore.check_values(con, table, col[1])
            if vals:
                out.setdefault(frozenset(vals), []).append((table, col[1]))
    return out


def main():
    if not Path(DB).exists():
        print("FAIL: no database at %s" % DB)
        return 2
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    vocab = check_vocabularies(con)

    examined, violations = 0, []
    for rel in SCANNED:
        path = ROOT / rel
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8", errors="replace")
        for m in _CHOICES.finditer(src):
            lits = {a or b for a, b in _LITERAL.findall(m.group(1))}
            if not lits:
                continue          # a non-literal list: derived already, or numeric
            examined += 1
            owner = vocab.get(frozenset(lits))
            if owner:
                line = src[:m.start()].count("\n") + 1
                table, column = owner[0]
                violations.append(
                    "%s:%d restates the CHECK on %s.%s — replace with "
                    "dbcore.schema_choices(%r, %r)%s"
                    % (rel, line, table, column, table, column,
                       "" if len(owner) == 1 else
                       " (several columns share this vocabulary: %s — pick the one the "
                       "flag WRITES, not whichever is found first)" % owner))

    print("EXAMINED: %d argparse choices= literal(s) across %d writer file(s), against "
          "%d live CHECK vocabular(ies)" % (examined, len(SCANNED), len(vocab)))
    print("VERDICT: " + ("FAIL" if violations else "CLEAN"))
    for v in violations:
        print("  * " + v)
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
