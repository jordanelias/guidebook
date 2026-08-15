# Archived scripts — the 2026-08-15 Tier-1 retirement batch

**Retired by:** owner approval of 2026-08-14 ("APPROVE WHOLE TIER-1 BATCH"), against the package
list in `workplan/2026-08-14-remediation-workplan.md` §6.

**Nothing here was deleted.** Every file sits at the path it occupied under `scripts/`, so a
`git log --follow` still walks its whole history and a reader who greps an old document for a
filename finds it. Retire here, don't delete (`CLAUDE.md` §9 guardrail 2).

---

## What is here, and why each one stopped being live

| Path | Rows/size | Why retired |
|---|---|---|
| `convert/` | 13 files, 2,669 lines | One-time converters from the pre-database era. They read markdown and YAML corpora into forms the SQLite layer replaced. No caller, no registry entry, no schedule. |
| `db/` | 3 files | They target `data/db/guidebook.db` — a *different, legacy* database file that does not exist in this tree. `CLAUDE.md` §7 already placed the directory outside the `GUIDEBOOK_DB_PATH` contract. |
| `migrate/` | 8 of 10 files | The one-time entity importers. **Two files stayed live** in `scripts/migrate/`: `migrate_decisions.py`, which still reads the decision register YAML while that dual store awaits an owner ruling, and `_legacy_guard.py`, which disarms it. |
| `init_db.py` | — | Applied migration 001 only, so it never produced a working database. `CLAUDE.md` §10 already warned readers not to expect one from it. `migrate_db.py --rebuild` is the real path. |
| `validate_db.py` | 9 checks | Superseded by `scripts/tests/test_db_integrity.py` (72 checks). Repaired on 2026-08-05 but never selected by any battery. Its registry entry survives at `status: retired` and carries the one substantive finding it had left. |
| `migrate_evidence_sources_v2.py` | — | A one-time migrator FROM the old evidence-source schema. Its inputs are `/home/claude/*` paths that do not exist here. |
| `tests/test_generate_parts_4_2.py` | — | Exited 0 having asserted nothing: its fixture database `/tmp/work14.db` does not exist, so every assertion was skipped. A test that cannot fail is worse than no test. |

## What the caller sweep actually checked

`git grep`, never ripgrep — the root `.ignore` hides seven directories, and a sweep run through it
would make an unsafe deletion look safe. This is recorded because the same audit that produced this
batch also produced a cull list that named five load-bearing things as dead, two of them read by
*blocking* gates.

Reachability was tested six ways, not one: registry or CI selection, gate-readership, contract or
doctrine citation, operator CLI paths, transitive imports, and scheduled jobs. A cull driven only by
"nothing in CI runs it" would have deleted `emit_data_migration.py` — the only sanctioned way to
write the canonical database — along with `db.py` and the documented generators.

Two live CLI paths pointed into this directory and were retired in the same commit rather than left
dangling: `db.py init` (invoked `init_db.py`) and `db.py validate` (invoked `validate_db.py`).

## What must not be done

**Do not move a file back into `scripts/` to "fix" a broken reference.** Every reference that
mattered was updated in the retiring commit. A stale mention in a dated workplan, audit or session
record is *correct for its date* and must stay as it is — those directories are frozen records, which
is why `.ignore` hides them from search in the first place.
