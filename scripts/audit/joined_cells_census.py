#!/usr/bin/env python3
"""scripts/audit/joined_cells_census.py -- which live text columns hold more than one value in a cell.

Owner, 2026-11-06 (references/project-standards.md, "Owner statements 2026-11-06"; CLAUDE.md section 4):
one value per cell, each fact in the cell that names it. This reads the live schema and reports, per TEXT
column with data, how many values (a) parse as JSON arrays or objects, (b) look like short delimiter-joined
tokens, or (c) carry an appended correction (`|| CORRECTED`, `|| NOTE`, a dated bracket). A hit is a
CANDIDATE: prose with commas also matches (b), so read the example before acting. Read-only. It is a report,
not a gate: it exits 0, and prints `EXAMINED: <n>` text columns so a run over nothing is visible.

Run it before adding a cell, and after, to see that the change added no class it flags.
"""
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

DB = Path(os.environ.get("GUIDEBOOK_DB_PATH",
                         Path(__file__).resolve().parents[2] / "data" / "guidebook.db"))
TOKENS = re.compile(r"^[^,;|\n]{1,40}([,;|]\s*[^,;|\n]{1,40}){1,}$")
APPENDED = re.compile(r"\|\| (CORRECTED|NOTE)|\n\[\d{4}-\d\d-\d\d|; \[20")


def _is_json_container(v: str) -> bool:
    if v.lstrip()[:1] not in "[{":
        return False
    try:
        return isinstance(json.loads(v), (list, dict))
    except ValueError:
        return False


def main() -> int:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    examined, hits = 0, []
    for (table,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                                "ORDER BY name"):
        for _, col, typ, *_ in con.execute(f'PRAGMA table_info("{table}")'):
            if (typ or "").upper() not in ("TEXT", ""):
                continue
            vals = [v for (v,) in con.execute(f'SELECT "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL')
                    if isinstance(v, str)]
            if not vals:
                continue
            examined += 1
            js = sum(_is_json_container(v) for v in vals)
            dl = sum(1 for v in vals if len(v) < 200 and TOKENS.match(v))
            ap = sum(1 for v in vals if APPENDED.search(v))
            if js or dl >= 3 or ap:
                hits.append((table, col, len(vals), js, dl, ap, vals[0][:60].replace("\n", " ")))
    for t, c, n, js, dl, ap, ex in hits:
        print(f"{t}.{c:34} rows={n:5} json={js:4} delimited={dl:4} appended={ap:4}  e.g. {ex!r}")
    print(f"EXAMINED: {examined} text column(s) with data; {len(hits)} candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
