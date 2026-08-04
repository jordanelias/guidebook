"""Refuse to let a one-time legacy importer write the canonical database.

WHY THIS EXISTS
`scripts/migrate/migrate_*.py` are one-time importers from the pre-SQLite era.
Six of the nine defaulted their target to
`os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")` — the CANONICAL
database — and wrote it with plain INSERT + commit, entirely outside the
migration system. CLAUDE.md §0 rule 4 makes migrations-only absolute, and the
blocking reproducibility gate compares `PRAGMA user_version` plus `COUNT(*)` on
six tables, so an out-of-band INSERT into `connections`, `slugs`, `gaps` or
`decisions` lands below its detection floor.

This was not theoretical. Audited 2026-08-04:
  * `migrate_connections.py` was fully runnable — every column in its
    `INSERT INTO connections` exists in the live table, its input
    `references/connections/_index.md` is present, and it needs no network,
    no PAT and no arguments beyond local paths.
  * `migrate_items.py` took NO required arguments at all and opened the
    canonical DB immediately; it was saved only by naming `applicable_groups`,
    a column that no longer exists, so it crashed before committing. One schema
    change ago it was a zero-argument canonical-DB writer.

CLAUDE.md §7 warns that `scripts/db/**` targets `data/db/guidebook.db`, "a
different, legacy file". That is true, and that directory's target does not even
exist — so the documented hazard is inert while the undocumented one was live.
This guard closes the real one.

WHY GUARD RATHER THAN DELETE
Archiving these files is owner-gated and blocked on a precondition the project
set for itself: commit `366766ee` (2026-08-03) archived 33 sibling scripts and
deliberately kept these, recording that six are named in
`architecture/sqlite-data-layer.md` §9's build table and that archiving them
"would silently falsify a spec document". The files therefore stay where the
spec says they are — but the gun is unloaded.

Pattern copied from `scripts/audit/graph/build.py:26-41`, which is
mutation-tested by `graph_audit`'s selftest.
"""

import os
from pathlib import Path

CANONICAL = "data/guidebook.db"


def assert_not_canonical(db_path, script_name):
    """Raise SystemExit if `db_path` is (or is named like) the canonical DB."""
    p = Path(db_path).resolve()
    canonical = Path(os.environ.get("GUIDEBOOK_DB_PATH", CANONICAL)).resolve()
    if p == canonical or p == Path(CANONICAL).resolve() or p.name == "guidebook.db":
        raise SystemExit(
            f"{script_name}: refusing to open {db_path!r}.\n"
            f"This is a ONE-TIME LEGACY IMPORTER from the pre-SQLite era. It writes with\n"
            f"plain INSERT outside the migration system, and the canonical database accepts\n"
            f"changes ONLY through scripts/emit_data_migration.py -> scripts/migrate_db.py\n"
            f"(CLAUDE.md §0 rule 4 — the rule is absolute, and the blocking reproducibility\n"
            f"gate cannot see an out-of-band INSERT).\n"
            f"If you are reconstructing history, pass --db pointing at a SCRATCH copy."
        )
    return p
