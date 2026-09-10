# PR #131 verification — the two findings, and what was done about them

**Verdict carried forward: PASS.** PR #131 is merged (`5d9ed6e`). Its load-bearing claims
were exercised at the terminal and held: `db.py add-extraction` exists and refuses in
words; `assess_cell.gather_sources()` gathers by `(ref_id, parameter_id)` rather than by
slug; a source whose tier is not derivable from its own `(evidence_type, scope)` cannot
anchor `stated`; the engine is deterministic. Nothing here reopens any of that. The two
`⚠` findings the verification raised were about the engine's SURFACE, not its judgment,
and this branch closes both.

## Reproduced first, on scratch copies, before anything was edited

Canonical `data/guidebook.db` sha256 `9152f92e…` at start and at finish, `git status
data/` clean throughout. Every write went to a copy under the scratchpad with
`GUIDEBOOK_DB_PATH` inline.

```
db.py add-parameter --term-id TERM-002          -> parameter_id 1 (corridor width)
db.py add-extraction --ref-id REF-00973 ...     -> extraction_id 1
assess_cell.py --parameter-id 1 --identity MOB  -> stated, basis=T1, sha 2df4314b32ed
assess_cell.py … same cell, same DB, again      -> Traceback (most recent call last):
                                                     …
                                                   sqlite3.IntegrityError: UNIQUE
                                                   constraint failed: index
                                                   'idx_spec_row_identity'
```

The stated-case sha (`2df4314b32ed`) and the non-anchoring pending-case sha
(`ef3dd1fb6f97`, `REF-00971`, scope NULL) both reproduce the verification's figures
exactly, on an independent run. That is corroboration of the report, not a re-derivation
of it.

## Finding 1 — re-determining a cell died on a raw SQLite error

**What was wrong.** Not the refusal: `idx_spec_row_identity` SHOULD refuse a second row
for the same `parameter_id × lens`, and the doctrine behind that is settled — there is no
re-determination path, and a batch revisiting a determined cell needs a supersede design,
which is an owner decision (`workplan/2026-09-10-road-to-batch-06.md`, "DELIBERATELY
WAITING"). What was wrong is WHERE and HOW it refused: inside the `specifications`
INSERT, after the whole determination had been computed, as an untranslated traceback
naming an index rather than a cell — telling the operator neither that the cell was
already determined nor that there is nothing they can do about it.

**Fix.** `assess_cell.validate_cell_undetermined()` asks the question from argv, before
the gather, before `next_gap_id`, before the pydantic gate. It restates the index's own
COALESCE expression rather than probing for the error, and runs after `validate_lens()`
has normalised blanks to None, so the two cannot disagree about blank-versus-NULL. The
message names the standing `specification_id`, its state, its `rule_version`, its
`derivation_sha` and the session that wrote it — and NAMES NO REMEDY, deliberately:
"delete the row and re-run" is the supersede design, and writing it into a help string is
making an owner decision in the one component that must not make it.

**Behaviour after:**

```
REFUSING: cell 1×MOB is ALREADY DETERMINED. specification_id 1, state 'stated',
rule_version 'pilot-2', derivation_sha 2df4314b32ed, written 2026-09-10 00:00:00 by
session claude-pr-131-verification-wzz6tt.
  Nothing was computed; no SQL artifact was written; the database is unchanged.
  …
```

Exit 1, no `--emit-sql` file — the same outcome as before, which is why every instruction
in the batch-06 runbook still stands. Only the operator's view of it moved, and the
runbook's hazard paragraph was swept to say so rather than to keep describing a traceback
at a line number that has since moved twice.

## Finding 2 — `--db` both writes and emits, and said neither

`--db` read as an input ("scratch DB (NEVER data/guidebook.db)") while the run also
INSERTs the determination into it and commits. That is not a defect — `emit_batch_sql.py`
captures those rows from the scratch DB, and the runbook's step 6a depends on it — but it
is invisible from the flag names, and it is what makes finding 1 fire in the first place.
It is also why a determinism comparison needs two fresh copies rather than one DB run
twice.

**Fix.** Said, in the two places it is acted on rather than only where it is configured:
the `--db` and `--emit-sql` help strings, a parser epilog, and three lines added to the
run's own closing message naming the DB the rows were committed into.

## The third item — refusals arriving as tracebacks

Flagged in the verification as house style rather than a regression, and it is. It is also
what buries finding 1's message under a stack trace, so it is closed HERE and only here:
`assess_cell.py` now prints its own refusals as sentences. A `Refusal(ValueError)` subclass
carries the distinction, and the reason it is a subclass rather than a bare `except
ValueError` is load-bearing — pydantic's `ValidationError` IS a `ValueError`, and a model
rejecting a row THIS ENGINE built is an engine defect whose location is the evidence. It
keeps its traceback.

**`scripts/db.py` was left alone.** It has the same house style and no top-level handler,
and its refusal messages are unusually good ones to bury — but it is a 4139-line surface
that PR #131 only partly touched, and translating its exceptions is a sweep with its own
caller question (`dbcore` raises `ValueError` from paths `db.py` is not the only caller
of). Recorded as owed, not done.

## Not exercised

Replaying an emitted artifact through `emit_data_migration.py` → `migrate_db.py` into
canonical. That writes the real database; this branch stayed off it. `migration_reproducibility`
is what verifies that path, in CI, and it is not verified here.

## Gates

`run_checks.py --changed-from origin/main --explain` → PASS, 21 green. `--selftest` → PASS.
`test_assess_cell_pilot` (registered) → PASS. The two advisory failures in the run —
`retired_vocabulary` (64 occurrences, EXAMINED: 26) and `test_verification_pipeline`
(15/18) — were measured on a stashed, untouched tree first and fail identically there.
Pre-existing, not this diff's.
