# T-144  A closed gap says when, in which session and by what it was resolved

_One task, one pull request (a standalone tooling pull request, executed 2026-11-20). Read `CLAUDE.md` first. Index: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number below is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Executed directly on the owner's instruction; this file records what was built.

## 1. Identity

| | |
|---|---|
| Task | T-144 |
| Title | A closed gap says when, in which session and by what it was resolved |
| Wave | standalone (after the third stack) |
| Layer (CLAUDE.md §3) | 1 and 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10) |
| Executor | NOT FOR SONNET |
| Traces to | The owner's instruction typed 2026-11-20: "add a resolved column and a solution provenance column or something ... unless we already have a table that links accordingly" |

## 2. Preconditions

- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** none outstanding. The instruction above is the owner's own.
- **Set-up.** As `tasks/T-050-*.md` section 2; the schema migration's number is derived at execution time (`ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one).

## 3. The problem, in the guidebook's terms

`close-gap` moved `gaps.status` and nothing else, and no table links a gap to what closed it, so a closed gap said neither when it was resolved, in which session, nor by what. A gap closed by mistake, or for a reason since withdrawn, reads as answered and cannot be checked.

**Evidence command** (before the change): `git show <base>:scripts/db.py | grep -n -A12 'def close_gap' | grep -c resolution` printed `0`, and `pragma table_info(gaps)` held no resolution column. After: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[1] for r in c.execute('pragma table_info(gaps)') if 'resol' in r[1]])"` prints `['resolved_at', 'resolved_by_session', 'resolution_ref']`.

## 4. The change

The shape the project already holds, reused: `determination_gates` (`resolved_at`, `resolved_by_session`, `resolution_rationale`), `extraction_follow_ups` (`resolved_at`, `resolved_by_session`, `resolution`), and `adversarial_findings.disposition_ref` for what the pointer may hold ("a data migration path; a quote-anchored ledger pointer; or the reason").

1. Schema migration `scripts/migrations/162_gap_resolution.sql`: `gaps` gains `resolved_at`, `resolved_by_session`, `resolution_ref`, each by `ALTER TABLE ... ADD COLUMN` with a CHECK (the columns are new, so no rebuild; migration 160 used triggers only because its columns already existed). All three present or all NULL; a gap that carries them is CLOSED (an OPEN gap carries none); `resolved_at` has `dbcore.now()`'s shape, is a real calendar minute and is not before the row's own stamped `created_at`; `resolved_by_session` is a session stem (`dbcore.is_session_stem`); the pointer is not blank by `dbcore.blank_chars()`, spelled as migration 160 spells it. A stamp in the future is not refused (a CHECK cannot read 'now'; the writer stamps `dbcore.now()`).
2. `scripts/db.py` `close_gap` / `close-gap`: takes `--resolution-ref`, writes the three cells with the status in one UPDATE, and refuses a blank pointer (naming what to give), a ledger pointer whose quote is not found once (`dbcore.require_ledger_quote_once`, as `dispose-adversarial-finding` reads it), a session that is not a stem, an unknown gap (it used to UPDATE nothing and print "closed"), and a gap already closed (its first closing stands). `amend-gap` is unchanged. No verb reopens a gap; a reopening by hand must NULL the three cells with the status or the CHECK refuses it.
3. No backfill: the gaps closed before the migration carry no provenance and none can be honestly derived (`select count(*) from gaps where status like 'CLOSED%' and resolved_at is null`). `scripts/audit/gap_mining_audit.py` lists them by id as informational CHECK 8 (the smallest existing home; no new script or check).

**What reads what this task adds:** `gap_mining_audit.py` CHECK 8; `close-gap`'s already-closed refusal; `emit_batch_sql.py` (the capture set is derived, so the three cells ride the UPDATE).

## 5. Caller sweep

Names swept: `close_gap`, `close-gap`, `gaps.status`, `FROM gaps`, `'CLOSED%'`, and `sqlite_master` (`v_pending`, `v_gap_subject`: neither reads status; no trigger on `gaps`). Callers repaired: `scripts/db.py` (usage line, `amend-gap` help, `amend_gap` docstring), `scripts/tests/test_run_pipeline_refusals.py` (the two `close_gap` calls), `skills/gap-driven-mining_SKILL.md` and `skills/toc-editor_SKILL.md` (the command examples), `architecture/sqlite-data-layer.md` (a note on the illustration), `workplan/pipeline-state-graph/machines.yaml` (M07.t2's guard and needle). Mentions left: the status readers (`research_protocol_audit.py`, `refusal_register.py`, `bootstrap.sh`, `get_open_gaps`), whose truth does not change.

## 6. Verification

- `python3 scripts/tests/test_db_amend_writers.py`: `EXAMINED` rose by exactly the T144 cases (`grep -c 'record("T144-' scripts/tests/test_db_amend_writers.py`; re-run the file, its last lines print the count). T144-01 pins the blank spelling; -02 to -06, -08, -09 each refusal; -07 the stamp in one UPDATE; -10 an accepted ledger pointer; -11 the CHECK (an OPEN gap with provenance, a partial set, impossible, early, seconds-bearing and BLOB stamps, non-stem sessions, blank pointers refused; a well formed closing accepted); -12 the audit listing; -13 the capture through `emit_batch_sql`. Each was shown red on a seeded defect (writer refusals removed; the migration's clauses and spelling weakened in a scratch worktree) and the files restored byte for byte (`cmp`).
- `python3 scripts/migrate_db.py --rebuild <scratch>/rebuilt.db` exit 0; `python3 scripts/audit/migration_reproducibility.py --deep` PASS; `python3 scripts/audit/joined_cells_census.py` reported the same candidate count before and after.
- `python3 workplan/pipeline-state-graph/build_graph.py --check`: the same one failure (PIP-01) before and after.

## 7. Commit

`governance: give a closed gap its resolution stamp, session and pointer [YYYY-MM-DD HH:MM]`, one commit, explicit paths.

## 8. What you must NOT do

File no gap row, touch no other table, write no data migration (rule 10), backfill no closed gap.

## 9. Stop conditions

A reader of `gaps.status` whose truth changes and cannot be repaired here; a check green before and red after; a vocabulary the schema does not hold.

## 10. Rollback

Before merge: drop the commit. After merge: `git revert`, and a compensating migration that drops the three columns (162 is never edited).

## 11. Adversarial pass and pull request

The coordinator runs the adversarial pass on the commit and opens the pull request.
