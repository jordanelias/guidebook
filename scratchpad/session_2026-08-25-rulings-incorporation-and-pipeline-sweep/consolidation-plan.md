# Suite consolidation — execution plan (Fable 5, 2026-08-25)

Owner-authorized: *"fable 5 plan out suite consolidation with shared library and full table
CLI coverage then Opus to execute carefully agonist-antagonist."*

**Committed because a plan that lives only in a conversation is this session's own finding.**
The pointer-discipline queue existed only in a transcript and three of its items shipped citing
labels no file defined. This file is the primary record of what Opus is executing.

**This is a DERIVED document under CLAUDE.md §2(b).** Every count carries its command and drifts
the moment anything lands. Re-derive at execution time; where measurement and this file disagree,
the measurement wins.

## The point, kept in front of everything

Hand-written SQL exists **because** `db.py` cannot write `search_candidates`,
`evidence_population_match`, `economics_entries`, `case_studies`, `jurisdictional_values`. That
channel delivered the 2026-08-19 author fabrication into committed data — 12 of 19 author rows
naming non-authors, past six green gates — through a capture tool that was itself blind
(`emit_batch_sql` silently emitted 32 statements for 40 rows on 2026-08-23). Judge every act on
whether it narrows that channel, not on file counts.

**What this programme does NOT fix, stated so it is never claimed:** fidelity. A CLI cannot know
whether an author list is true. `retrieval_log.py --verify-authors` remains the only gate on that.
The consolidation's worth is the narrower channel it leaves for that gate to police.

## Supersession to record on contact (CLAUDE.md rule 0)

`workplan/2026-08-22-master-execution-plan.md` §6.5 Workstream D says *"Do not build the helpers…
If a helper is ever built, it must be because a batch was blocked by its absence."* The owner's
live directive supersedes that. Record the supersession; do not argue the workplan back at the
owner, and do not bother arguing that the condition was met anyway.

## A. Target architecture

**One new module `scripts/dbcore.py`; one CLI `scripts/db.py`; one capture `emit_batch_sql.py`;
one canonical writer `migrate_db.py` (untouched).** No package, no `-m` sweep — the registry's
63 `cmd:` entries are callers of the current `python3 scripts/...` form.

`dbcore` absorbs, moved not copied:
1. `connect(dry_run, readonly, db_path)` — with the no-`journal_mode` comment moved VERBATIM.
2. `db_path()` and `REPO_ROOT` — one resolution each.
3. `now()` / `audit()` / `_upd()` audit stamps.
4. `norm_doi()`, `fold_ref()`, the ref-id shape regex.
5. `next_ref_id(conn)` — computed, never stored, over the UNION of `source_locators` and
   `evidence_sources`.
6. `WRITABLE_TABLES` — moved from `emit_batch_sql.py`, imported by both CLI and capture.
   **This is the structural fix for the silent-drop class:** a table cannot again be
   writable-but-invisible to capture, because both read one constant.

**NOT absorbed, each for a reason:** `schemas/*.py` mirrors (independence is what makes drift a
detectable bug); `retrieval_log.py` (its value is being outside the write path); check-side SQL
(a gate that imports the library it polices fails together with it — rule 5 forbids two *stored*
homes, not two *computations*); the migration pair; business/query logic.

## B. Full-table CLI coverage — the CLI's value is its REFUSALS

New: `add-candidate`, `add-population-match`, `add-jurisdictional-value`, `add-economics-entry`,
`add-case-study`, `add-locator`/`update-locator`. Each with FK existence pre-checks, vocabulary
checks derived from live rows and `schemas/` (never invented), audit stamps, `--dry-run`,
`--session` required.

**Two refusal rules that are easy to get backwards:**
- `add-population-match` must **NOT** refuse a second row for the same (ref, population).
  DR-2026-08-19 §7 rules a dissenting grade lands as a second row distinguished by
  `created_by_session`. A uniqueness refusal would silently abolish the adversarial mechanic.
- `add-locator` **must** refuse a DOI already held under a different ref_id, case-folded. That is
  what turns off the stash's duplicate growth (32 duplicated DOI groups today, was 29 on 08-22).

`add-source` gains `--url`, `--url-accessed`, `--pages`, `--doi-resolution-outcome`. It must NOT
gain `--first-author-last` — that is a derived copy; close the gap as a REFUSAL mirroring the
existing `author_display` refusal.

**No subcommand for:** `specifications` + synthesis tables (doctrine routes those writes),
`search_coverage`/`search_languages` (frozen), `data_migrations` (runner-owned), `pipeline_runs`/
`url_verification_runs` (job-owned), `reference_stubs` (replay tombstone), `decisions`,
`axes` (retired frame), and standalone author edits (a post-hoc author edit is a correction and
ships as a compensating migration — a subcommand would recreate the fabrication surface with
better ergonomics).

## C. The acts

Protocol per act: `ensure-deps.sh` first; `--changed-from origin/main` **and `--selftest`** green
before and after; DB sha256 recorded either side of any act that must not move it; scratchpad
committed at every break.

1. **Extract `dbcore.py`**; db.py + emit_batch_sql become its first importers. Correct CLAUDE.md
   §4's mint rule. Pure code. Falsified by: sha unchanged; db.py retains no own `sqlite3.connect`;
   `readonly_db_open_audit` EXAMINED stays 32.
2. **Full-table CLI coverage** — the causal-defect fix. Sweep the 29 skills that reference db.py.
   Falsified by REHEARSING BOTH REAL FAILURES on a scratch: the 8-row rescue (assert emitted
   count == write count) and the fabrication shape (assert `--verify-authors` still fires).
3. **One capture list; hand-SQL closed by instruction.** DR-2026-08-19 gets an APPENDED
   supersession note, never an in-place edit.
4. **Job-writer gate collision — OWNER ACT. NARROWED 2026-08-25:** the jobs are STAGE-PURE (every column they write to `evidence_sources` is evidence-collection content: identity, verification, extraction). No boundary is crossed and no fact is duplicated, so option (ii) "jobs emit migrations" buys NOTHING doctrinally — it changes the mechanism, not the stage content. Cleaner basis for (i): `pipeline_runs` / `url_verification_runs` are run ledgers, facts about the JOB not about a source — substrate infrastructure, never stage data, so never subject to the crossing rule. Doctrine-level, so the plan's job is the brief, not
   the verdict. Code floor (jobs adopt dbcore) ships regardless.
5. **Read-side consolidation** — RE-SCOPED 2026-08-25. The unit of work is NOT "does this file import dbcore" but **"does this reader cross a stage by POINTER or by reading a COPY"**. That supplies the acceptance test the original act lacked — *no live reader selects a stage-foreign column directly* — which fails today on `evidence_sources.search_queries_used`. The connect() migration rides along free. Four slices, LAST among code acts. The two AST audits must be
   re-taught IN SLICE 5a, before subjects move — otherwise a slice greens the board by emptying a
   gate's scope, which is this repo's signature failure.
6. ~~**Drop the 11 unread views**~~ **REFUSED ON EVIDENCE 2026-08-25 — see
   `acts-456-under-the-stage-ruling.md`.** A cross-stage view IS the pointer; 8 of 11 are
   pre-data, not dead. Per-caller join helpers survive as the cheap half.

Serial: 1→2→3. Act 4 parallel (owner-bound). Act 5 after 1, slices serial. **Act 5 and Act 6 must
never run concurrently** — both sweep the same reader files, and a sweep against a moving tree is
not a sweep.

## F. What NOT to do

No parity check between CLI coverage and the capture list (a parity check makes a dual home
permanent — one constant with two importers leaves nothing to keep in parity). No config file
restating the registry. No new registered check for "all writes go through the CLI" (it polices
the apparatus, not the book; `migration_reproducibility` already gates the real harm). No stored
ref-id allocator. No `scripts/` package. No seeding empty tables to exercise subcommands. No
triggers. **No third map** — this plan is executed then discarded into the commit record.

## G. Acceptance test

Not a file count — a structural property of the live tree:
1. The only live code opening the canonical DB outside `dbcore` is the sanctioned writer set
   (`migrate_db.py` + the two DR-2026-05-28 jobs); every surviving hit is an audit-classified
   scratch/fixture open, with `readonly_db_open_audit` printing EXAMINED ≥ 32 and 0 findings.
2. Every table a session may legitimately write has exactly one write path, that path refuses,
   and the capture tool walks the identical list.

## H. Risk

**Act 5 is the most dangerous** — ~50 files, two AST audits whose subject detection must be
rewritten in the same motion, and the standing risk of greening the board by emptying a gate's
scope. Mitigated by EXAMINED floors per slice, byte-diff against the REBUILT db (not just the
committed one), audits rewritten first, and explicit license to abandon slices: **Acts 1–4 deliver
the causal-defect fix without Act 5.**

**Act 2's refusal design is risky in both directions:** too strict and the next batch stalls
against its own tooling; too loose and the hand-SQL failure mode returns wearing a CLI. Every
refusal needs a fixture proving it fires AND a fixture proving the legitimate shape passes.

## Uncertainties, reported as such

Fable's counts differ slightly from the earlier briefing (55 vs 56 files; 48 of 85
`GUIDEBOOK_DB_PATH` lines are real resolutions; 37 root resolutions by a narrower regex — treat as
a floor). The `migration_reproducibility_deep` registry note describes a pre-baseline 277-row
divergence that no longer exists. `search_candidates.disposition` and
`evidence_population_match.match_grade` vocabularies must be read from live rows at execution time
— inventing them here would be the §2(b) defect. Whether `db.py init` still exists is unclear.
