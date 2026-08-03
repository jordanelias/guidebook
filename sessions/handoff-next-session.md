# Handoff — Execute the comprehensive plan, then return to research

**Repo:** `jordanelias/guidebook`
**Branch:** `claude/resume-infrastructure-work-zvl5ft` (restarted from `main` after PR #77 merged)
**HEAD at handoff:** `c4073a0` ("Merge pull request #77 …")
**Last session record:** `sessions/session_2026-08-01-tooling-second-pass.md`
**Latest PI in repo:** `governance/project-instructions-v10_14.md` (the repo PI legitimately lags — the owner pastes it into claude.ai)
**Doctrine SHA:** `0f2f525`
**The plan to work from:** `workplan/2026-08-02-architecture-decision-and-execution-plan.md`

> **Rewritten 2026-08-02.** The previous handoff pointed at HEAD `de364a88` and a 2026-05-13
> session record for eleven weeks, and named branch `main`. Keeping this file current is W4.2 of
> the plan; until the mechanical check lands, rewrite it at every session close.

---

## Where things stand

**One plan supersedes the rest.** `workplan/2026-08-02-architecture-decision-and-execution-plan.md` replaces the
2026-08-01 consolidation plan and the 2026-08-02 prune plan. Those remain as the record of how the
findings were reached — do not start from them.

It is organised as eight workstreams and written against the owner's stated target shape — twelve
pipeline stages and five tables (a)–(e) — rather than the repo's own five-stage abstraction. Every
number in it carries its derivation in §9.

**W1 is done** (this session): the two skills that directed sessions at a nonexistent database are
repointed and every rewritten query verified by execution; CLAUDE.md's two self-contradictions are
fixed; this handoff is current.

**W2–W8 are open.** W2, W3, and W4 need no owner decision and can land as small PRs.

---

## The findings that should shape the next session

1. **Three blocking gates cannot fail.** `doctrine_recheck` as invoked (deleting a CANONICAL
   governance document exits 0), `audit_evidence_metadata` as invoked (garbage in every metadata
   field exits 0), and `matrix_consistency` (compares code against a transcription of the doctrine
   held inside the check itself). That is W2, and none of it needs a decision.
2. **`test_db_integrity` is not one backlog.** It is 111 rows across 11 unratified vocabulary
   values — one D-SCHEMA decision, ⚑7 — plus 120 distinct rows of genuine metadata backfill that
   does require re-retrieval under R10. Four of the 111 (`high`, `medium`) are junk from a foreign
   vocabulary, marked *investigate*, not *ratify*.
3. **The schema cannot express two defining features of the target shape.** Table (b) has no column
   recording whether a source's data has been scraped — 856 of 863 sources have no extraction row
   and are indistinguishable from "read, nothing to extract". Table (a) does not store per-tier
   source counts per topic. Both are W5.
4. **`sessions/LATEST` serves two incompatible consumers** and has been quietly disabling the
   blocking `citation_mining_session` check for seven weeks. W4.1 splits it.
5. **`main` is not branch-protected**, so 30 blocking controls are advisory in fact. ⚑1.

---

## Decision queue — surface to the owner, do not auto-execute

⚑1 branch protection (with the `DB integrity` carve-out until W7 completes) · ⚑2 consolidate the
five rival (c)-layer tables · ⚑3 `room_page.py` fix-or-archive · ⚑4 `test_adjudication_integrity`
· ⚑5 `test_generate_parts_4_2` (recommend keep + re-fixture — it is the only test of a live
generator) · ⚑6 `citation_mining_pipeline.py` · ⚑7 ratify the 11 vocabulary values.

**New this session:** whether the spec template's prose fields should have a home in the schema at
all. No table carries them — `summary`, `why_md`, `schedule_md`, `dar_note` and the rest exist in
no table across all 63. They are file-canonical by default rather than by decision, which is part
of why 79 of 87 generated spec pages render an empty best-practice banner.

---

## Working rules that bit during this session

- **The DB is a 6.8 MB binary blob with no merge driver.** Two branches both touching it produce an
  unresolvable conflict. Serialize anything that writes it. The resolution protocol is to discard
  both blobs and `migrate_db.py --rebuild` — except `evidence_source_authors` and `pipeline_runs`,
  which are written outside migrations and would be lost.
- **Use a quoted heredoc for commit messages** (`<<'EOF'`). An unquoted one command-substituted
  backticked terms out of a message earlier in this session.
- **`$?` after a pipeline is the last command's status**, not the interesting one. Use
  `${PIPESTATUS[0]}`.
- **Verify by execution, not by reading.** Five of the six data-sourcing queries in
  `item-specification-writer` had been broken for months precisely because nobody ran them.

---

## Carried forward, still open (P1, not blocking)

- `skills/workplan-orchestrator_SKILL.md`: 1 hardcoded DB path, 1 absolute path, 8 embedded dates,
  and a stale embedded skill-index taxonomy. Fix when touching that skill for any reason. Given
  what W1 found in two other skills, **the whole `skills/` directory deserves the same
  execute-every-query sweep** — that is a candidate addition to W2.
- 3 rows in `data_migrations` have row-IDs from the Python migrations that don't match the SQL
  filenames. Cosmetic; doesn't affect CI.

---

## Tools and access

`scripts/preflight.sh` gates a diff; `python3 scripts/run_checks.py --changed-from origin/main
--explain` says why each check ran or didn't. Expect one blocking failure on any branch —
`test_db_integrity` at 31/41 — nine pre-existing content rows plus C10 — and a dozen advisories.
Install deps first: `pip install -r requirements.txt`, then `pip install jsonschema`.

Never write `data/guidebook.db` directly. All changes ship as migrations
(`scripts/emit_data_migration.py` → `scripts/migrate_db.py`), verified with
`python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` before pushing.
