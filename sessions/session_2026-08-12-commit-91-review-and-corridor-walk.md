# Session — Adversarial review of commit #91, and a content walk on corridor width

**Date:** 2026-08-12
**Branch:** `claude/commit-91-adversarial-review-rozgrn`
**Doctrine SHA:** `0f2f525`
**Kind:** governance / tooling review. **No content, no synthesis, no canonical DB writes, no migrations.**
**Subject:** PR #91, merged at `356efda` — 13 commits, 8 files, +9,005 / −112.

---

## Task

Review commit #91 in its entirety, adversarially, for factuality and logic. Reason about the
questions its handoff raises. Then run a trial walking real content from stage 1 to stage 12
using corridor widths as the basis — extended mid-session, at the owner's direction, to add
wheelchair turning radius and swept path as a second trial and to test whether the two can be
connected or contested against each other and against other items in their category.

## Method

The audited document's own protocol (its Part 3), turned back on it: lens-separated passes —
factual, method/logic, vacuity, doctrine, cross-artefact — with the default verdict REFUTED and
CONFIRMED requiring personal reproduction. Every quoted measurement was re-executed rather than
read. The trial ran in a byte copy of the repository through the sanctioned write path
(`emit_data_migration.py` → `migrate_db.py`), 25 migrations emitted (23 surviving; two deleted to escape the deadlocked queue); **the canonical clone was
never written**, verified clean at close.

## What was delivered

- `workplan/2026-08-12-commit-91-adversarial-review.md` — the review, the answers to the
  handoff's questions, and the four owner questions on how the tools understand best practice.
- `workplan/2026-08-12-pipeline-walk-trial-log.md` — the complete action/IO log: every command,
  every SQL payload verbatim, every emitted migration file, every stdout/stderr, exit code, and
  the row-count delta on all 67 tables per action (3,875 lines).
- `workplan/2026-08-12-pipeline-phase-state-map.md` — what the data looks like at each of the
  twelve phases, what key carries the work forward, and what is dropped at each boundary.

## What the review found

Commit #91 is serious work and most of it survives re-derivation. The deep comparison
(63 of 66 tables identical), `test_db_integrity` 70/70, the 5-of-28 vacuity floors, the
unread `deps:` field, the malformed `governance` battery YAML, the `graph_audit.py:277` crash,
the three unguarded writers, the non-existent `session_pointer_resolvable`, and the broken
`requirements.txt` all reproduced exactly.

Three factual corrections: **"345 SQL migrations reproduce the database"** — the replay set is
**331** (the baseline convention skips 14); **`55 green, 9 advisory`** is now **56**, because the
commit's own new check made it so; and §0.2 is titled "what the antagonist pass killed" over a
table in which six of eleven rows were corrected rather than killed.

**Its central conclusion does not survive.** "BREAK POINT: none — the row traversed all twelve
stages" was established by writing rows directly into a scratch database. A real item walked
through the sanctioned path broke four times.

## The four breaks

1. **The foreign-key guard is a post-commit alarm.** `migrate_db.py:161-183` disables FKs,
   executes, writes the ledger row, **commits**, then re-enables FKs and raises. The `except`
   rolls back nothing. A violating migration is committed, ledgered, and reported as an error.
2. **The word "bootstrap" disables foreign-key enforcement.** `migrate_db.py:174` substring-tests
   the first 500 bytes, which `emit_data_migration.py` fills with the session name and the
   `--summary` text. The identical rejected insert was accepted at exit 0 with the summary
   reworded.
3. **One failed migration voids every migration behind it.** Twice. No ledger row means still
   pending; the applier iterates in timestamp order and re-raises on the first failure. The
   documented remedy — fix forward with a compensating migration — cannot run, because the
   compensating migration is queued behind the failure. All three escapes break a stated rule.
   The error also names the wrong migration.
4. **Stage 9 has no writer.** `assess_cell.py` is a fixed-list pilot script whose seven
   `(item, population, slug)` triples are source-code literals, so E-08 × MOB is unreachable —
   and it aborts anyway on `GAP-1`, because `next_gap_id` returns `max+1` on a table the
   clean-room reset emptied and the schema requires three digits. **The reset broke the
   determination writer**, which is a direct counter-example to the audited plan's governing
   "empty is free" argument.

## What the render actually does

§1.0h — "the renderer makes evidence-thin populations disappear" — is **refuted for the live
generator**. All thirteen of E-08's populations render. What does not render is everything that
makes a determination checkable: **the value** (the determination table has no column for it),
**any `●`/`◐`/`○` marker** (Option A requires `○` for a code-consensus claim; there is no
renderer for the band system at all), **the gap link** beside the pending cell, and **the seven
governing sources** — so the page states the determination has no governing sources, which is
false. The honest-banner mechanism is what misreports.

## Turning radius vs swept path

The schema records the distinction — `measurement_paradigm`, `device_class`, `root_type`,
`echo_of`, `contested` — and it is the most sophisticated part of the data model. **Nothing reads
it.** Two T1 sources at 1500 mm (static turning circle) and 1830 mm (dynamic swept path), same
parameter, same population, both became anchors; every blocking gate stayed green;
`contested` stayed 0.

Underneath sits the structural fact both trials establish: **`assess_cell.py` writes
`value_min`, `value_max` and `value_unit` as `None`, unconditionally, and it is the only writer.
There is no code path anywhere from N extracted values to one determined value.** The pipeline
determines a *state*; the *number* is written by hand in synthesis prose. That may be the right
boundary — but it is nowhere named as one.

## Cross-item comparison

Nothing compares two items. The axes that exist are population×population within one item
(`conflicts`, 0 rows), one item over time (`spec_value_probes`, 0 rows), one item across eight
audit steps (`item_audit_pipeline.py --item`, singular), and `connections` typed `CROSS-ITEM`
(0 rows, target un-keyed — `item:E-99-DOES-NOT-EXIST` was accepted).

**The cost, measured.** One query putting E-04, E-08 and E-12 side by side returned
`E-12 | ISO | 81.0 | mm` for manoeuvring space. The `value_text` reads *"References EN 81-41"*.
**The extractor pulled `81` out of a standard's designation.** A wrong number is in the canonical
database now, and the first cross-item comparison anyone ran found it. Two further items for
owner ruling: E-12's six values are all platform-lift specifications under an item named for
manoeuvring space; and `references/conflict-matrices/CORRIDOR-W.md` asserts ≥2440 mm for the same
parameter whose item title says ≥1200 mm, four months apart, neither aware of the other.

## A correction to my own work, recorded rather than absorbed

I attributed the determination writer's abort to the retired population code `NEU` in
`PILOT_CELLS[6]`. The traceback shows it dying at `PILOT_CELLS[0]` on the gap-id pattern. Right
conclusion, wrong mechanism — the exact failure the audited document's §3.7 names as its main
methodological lesson, recurring inside a review of that document, on the first prediction I made
without reading the traceback.

## What was NOT done, deliberately

Nothing was executed. No fix, no promotion, no migration against the canonical DB, no retirement.
Eleven recommendations are proposed with their evidence and their gate; four need no decision and
are four lines each.

## Bias and counterclaim

Recorded in `attestations/sessions_session_2026-08-12-commit-91-review-and-corridor-walk.json`.

## For the next session

Read the review's Part 5. Recommendations 1–4 are one-to-four-line changes to `migrate_db.py` and
`assess_cell.py` that between them restore the write path; nothing else in the register is worth
doing while a foreign-key violation can commit and a failed migration can silently void the
queue behind it. Recommendation 9 — ruling whether value determination is a machine stage or a
human one — is upstream of most of the rest.

---

## Addendum 2026-08-12 — four-direction audit of the work log

At owner direction, the work log was audited forward, backward, for completeness, and for
internal consistency. Full report: `workplan/2026-08-12-work-log-audit-four-directions.md`.

**Forward and backward pass.** Five load-bearing results re-derived against the surviving scratch
database match the log exactly, and all ten log-level findings are carried into the review with
none dropped. But the review cites **no log identifier at all** — claims join to their evidence
by prose correspondence, which is the same defect the review faults elsewhere in the corpus.

**Completeness found the real gap.** The log covers the trial and not the review: probing it for
`migration_reproducibility`, `run_checks`, `check-registry`, `graph_audit`, `_legacy_guard`,
`requirements.txt` and `70/70` returns zero for every one. The review's **19 load-bearing
verdicts** — 13 factual-lens rows and 6 self-corrections — were produced by direct shell calls
whose commands are quoted in prose and whose outputs were never recorded. The trial has a
130-action verbatim log; the review that pronounces CONFIRMED and OVERSTATED on another session's
work has none. By the standard the review imports from commit #91 — *"where a claim has no
command, treat it as unaudited"* — it sits one rung below the document it audits.

The trial driver scripts existed only in an ephemeral scratch tree. The reusable half is now
preserved as `scripts/tests/walk_harness.py`; the content-laden stage scripts are deliberately
not, since they carry the pre-existing material the owner has ruled must not seed content
research, and their payloads are already in the log verbatim.

**Two number discrepancies, both fixed in this commit.** The log was cited as 3,865 lines and is
3,875 — my own quarantine banner added ten and invalidated two citations, the third instance of
that defect class in three consecutive documents. And **"23 migrations were emitted" was wrong:
25 were.** The two missing are precisely the files deleted to escape the deadlocked queue, so the
figure reported was the one that makes the interventions invisible. Not deliberate — the count
came from an `ls` of survivors — but the direction of the error is unlucky and it is corrected.
