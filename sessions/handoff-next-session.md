# Handoff — infrastructure legibility work, W4 landed

**Repo:** `jordanelias/guidebook`
**Branch:** `claude/w4-continuity`
**HEAD at handoff:** `2585e1a0`
**Last session record:** `sessions/session_2026-08-01-tooling-second-pass.md`
**Latest PI in repo:** `governance/project-instructions-v10_14.md` (the repo PI legitimately lags — the owner pastes it into claude.ai)
**Doctrine SHA:** `0f2f525`
**The plan to work from:** `workplan/2026-08-02-architecture-decision-and-execution-plan.md`

> **The header fields above are now checked.** `scripts/audit/session_pointer_audit.py`
> (registered blocking as `session_pointer_resolvable`) fails if `Last session record` or
> `The plan to work from` names a file that does not exist, and reports drift if
> `HEAD at handoff` is not an ancestor of the current HEAD. The previous handoff went eleven
> weeks naming a May HEAD and a merged branch; the fix for that was to rewrite it, and the fix
> for the fix is that a rewrite is no longer the only thing standing between this file and
> being wrong. **Keep rewriting it at session close** — the check catches dangling, not stale.

---

## The frame this work is under

The owner's stated goal, in their words: *"a very clean working tree that doesn't get bogged down
by Claude Code constantly pulling up stale information or getting confused when scanning because
too much context."*

The operative metric is **agent legibility**: when a session greps for a fact, how many answers
come back, and how many are wrong. "Stale" means **readable and wrong**, not merely old — an
archived record with a date on it is fine; a live-looking sentence describing a dropped column is
not. Infrastructure only, by explicit instruction. Content and research work are deferred.

---

## Where things stand

**One plan supersedes the rest.** `workplan/2026-08-02-architecture-decision-and-execution-plan.md`.
W1 is complete (PR #78). **W4 is complete** (this branch). W2, W3 and parts of W5–W8 are open.

### What landed in W4

| Item | State |
|---|---|
| W4.1 split `sessions/LATEST` into `LATEST` + `LATEST-RESEARCH` | done |
| W4.2 handoff rewritten, and its named HEAD / paths now checked | done |
| W4.5 close the `research-contract-baseline.json` self-amnesty | done |
| W4.6 promote `research_contract_sync` to blocking | done |
| W4.7 drop `db_meta.schema_version` | done |
| W4.3 enforce `YYYY-MM-DD-slug.md` in `workplan/` | forward-only check; the 57-file rename is owner-gated |
| W4.4 collapse three connection registers to one | reconciled + callers swept; **the retirement itself is owner-gated** |

**The finding worth carrying forward from W4.1.** The pointer split was necessary and *not
sufficient*. Pointed at the correct research session, the blocking `citation_mining_session` gate
still reported `Outstanding: 0` — because the pointer files hold a filename ending in `.md` while
`evidence_sources.created_by_session` holds the bare stem on 32 of its 33 values. The scoping
predicate had been selecting nothing, for every session, under either pointer, since `--session`
was added. The diagnosis in CLAUDE.md §10 was right about the pointer and blind to the join.

That is the fourth vacuous gate found in this stretch of work. **When a check passes, check that
it had a subject.** `citation_mining_completeness.py` now prints an `Examined` count and a verdict
of `OUTSTANDING` / `CLEAN` / `NOTHING-IN-SCOPE`; the same treatment is owed to any gate that can
be pointed at an empty scope.

---

## Decision queue — surface to the owner, do not auto-execute

⚑1 branch protection (with the `DB integrity` carve-out until W7 completes) · ⚑2 consolidate the
five rival (c)-layer tables · ⚑3 `room_page.py` fix-or-archive · ⚑4
`test_adjudication_integrity` · ⚑5 `test_generate_parts_4_2` (recommend keep + re-fixture) ·
⚑6 `citation_mining_pipeline.py` · ⚑7 ratify the 11 vocabulary values.

**Added by W4:**

- **The `workplan/` rename.** 57 of 60 top-level files do not sort chronologically by name, so CLAUDE.md
  §9's instruction — "sort `workplan/` by date and read the newest" — is unfollowable for most of
  the directory. The forward-only check stops it growing; fixing it is a bulk file move, which is
  owner-gated (§9 guardrail 4).
- **Retire the three connection registers to `_archived/references/`.** W4.4. The
  prerequisites are done and the answer is clean: the two split files hold 113 distinct CON ids,
  `references/connections/**` holds 246, the `connections` table holds 273, and **every id in the
  split files appears in both of the others**. They are a strict subset carrying nothing unique
  and missing 160 rows the DB has, so the retirement loses nothing (§9 guardrail 5 satisfied).
  The caller sweep found one live caller — `github-io_SKILL.md` told sessions to fetch
  `connection-register-active.md` over the API with a PAT — now repointed at
  `scripts/db.py connections`. `connection-register.md`'s redirect stub, which had been sending
  readers to the two archived files for four months, now points at the DB and carries the
  reconciliation. **All that remains is the file move, which is owner-gated.**
- **The advisory `retired_vocabulary` failures are a real backlog, not noise.** 71 occurrences,
  concentrated in `references/tier*-verified-sources.json` (D-0157 vocabulary in a JSON store whose
  status vs. the DB is unruled) and `governance/project-instructions-v10_14.md` (a PI snapshot
  naming `audit.yml`). Both need a classification ruling before a sweep.

---

## Working rules that bit during this work

- **The DB is a ~7 MB binary blob with no merge driver.** Two branches both touching it produce an
  unresolvable conflict. Serialize anything that writes it. The resolution protocol is to discard
  both blobs and `migrate_db.py --rebuild` — except `evidence_source_authors` and `pipeline_runs`,
  which are written outside migrations and would be lost.
- **Reproduce a CI check the way CI invokes it.** An `attestation` battery run *without*
  `--changed-from` passed on an empty diff and was reported green; CI then failed. Running a gate
  over nothing is the same defect as the gates being fixed.
- **Use a quoted heredoc for commit messages** (`<<'EOF'`), or write the message to a file. An
  unquoted heredoc command-substituted backticked terms out of a message.
- **`$?` after a pipeline is the last command's status.** Use `${PIPESTATUS[0]}`.
- **Verify by execution, not by reading**, and fault-inject every new check — the population
  validator's first draft could not even write the bad value it claimed to catch.

---

## Tools and access

`scripts/preflight.sh` gates a diff; `python3 scripts/run_checks.py --changed-from origin/main
--explain` says why each check ran or didn't. Install deps first: `pip install -r requirements.txt`,
then `pip install jsonschema`.

Expect **pre-existing** failures unrelated to your diff: `test_db_integrity` at 63/69 (content
backlog), and six advisories including `retired_vocabulary`. Read the run before assuming your
change caused a red — two blocking gates are red on `main` today for owner-gated reasons
(`references/tooling-register.md` §4).

Never write `data/guidebook.db` directly. All changes ship as migrations
(`scripts/emit_data_migration.py` → `scripts/migrate_db.py`), verified with
`python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` before pushing.
