# T-116  Hold the upper-limb population as UPL, and retire LMB to it

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Written in the OI-13 fold of 2026-11-12, from the owner's sixth to ninth sets. This file's own steps have not been executed by anyone. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-116 |
| Title | Hold the upper-limb population as UPL, and retire LMB to it |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request; the prose callers are T-058's) |
| Executor | Sonnet-class |
| Traces to | OI-13 (owner, 2026-11-12, eighth set: "LMB should be UPL for upper limb then", "and that doesnt concern mobility"; ninth set: the lower-limb child is `LLD`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from (see `REMEDIATION-WORKPLAN.md` §2 step 0 and `OPEN-ITEMS-PLAN.md` OI-02 for how `$BASE` is chosen).
- **Tasks that must be merged to the integration base first:** T-025, T-054 merged (T-025 for the identity add verb and the widened amend; T-054 for `retire-identity --to-identity` and `retire-population-icf-link`). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none outstanding. The owner's answers this task rests on are in the ledger: `grep -n -E "Owner clarification 2026-11-12 \((eighth|ninth) set\)" references/project-standards.md`; check `grep -F "OI-13 STATUS:" references/project-standards.md | tail -1` reads `ANSWERED BY THE OWNER` (OI-13 is an open item of `OPEN-ITEMS-PLAN.md`, not a register decision). `UPL`'s display name, description and category are **proposals the owner confirms** (section 4, item 1): write them as proposed, report them, and correct them with T-025's amend if the owner answers otherwise.
- **Tests that must be red (or green) before you start:** no `UPL` row; `LMB` `active` with live crossing rows.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-116-upl-for-upper-limb "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-116" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"   # s.db is the batch's working copy; t.db is for probes
```
- **Shell variables do not survive from one tool call to the next in this harness.** Write the stem down once and begin every later command block by setting `BASE`, `STEM` and `SCRATCH` again to the same values.
- **Real execution:** open with `/session-open` (it sets `scratchpad/CURRENT` to the stem and creates the folder of the same name), then `/orient`. Follow `skills/run-pipeline_SKILL.md`. **Pilot or dry run** (a scratch clone): skip `/session-open`, stay on the branch you were given, do the work on the scratch copy only, and stop before the write path below.
- Work only on the scratch copy and point every call at it inline:
```
GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"
```
- Land the rows only by the write path, after the work is finished:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```
Research batches are serial: if another research batch merged after you copied the database, `emit_batch_sql.py` refuses ("copied from a different base"). Do not force it; start again from the new base.


## 3. The problem, in the guidebook's terms

The owner made the limb-difference identity into an upper-limb one, `UPL`, outside the mobility family; the lower-limb counterpart, `LLD`, is a child of `MOB` (T-102). The registry still holds `LMB`, "people with limb differences; upper-limb disabilities", two things in one cell, filed under `mobility`.

**Evidence command** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select identity_code,display_name,category,description,status from base_taxonomy_identity where identity_code in ('LMB','UPL','LLD')\").fetchall());print(c.execute(\"select link_id,icf_code,mechanism,mapping_confidence from identity_icf_map where identity_code='LMB'\").fetchall());T=[t for (t,) in c.execute(\"select name from sqlite_master where type='table'\")];print({t+'.'+r[1]:c.execute('select count(*) from \"'+t+'\" where \"'+r[1]+'\"=?',('LMB',)).fetchone()[0] for t in T for r in c.execute('pragma table_info(\"'+t+'\")') if r[1] in ('identity_code','target_population','pop_a','pop_b','parent_code')})"
```

**Expected output today:** `LMB` active, category `mobility`; no `UPL`; `LLD` only if T-102 has merged; six `LMB` crossings (d440, d445, d510, d520, d540, d630), every one with the mechanism "Biomechanical — grip, force, range of motion, bilateral function"; no figure, grade or determination on `LMB` (after T-018, read figures through `v_live_lens_links`). If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. **Mechanism:** a new code with `LMB` retired to it, not a rename: `identity_code` is a key other rows point at, and the 2026-09-16 ruling retires identifiers in place (T-054 holds the one successor mechanism, shared with `SCI` to `WHEEL` in T-102).

1. **Mint `UPL`** with T-025's `add-identity`, no parent, with `--approval-ref "Owner clarification 2026-11-12 (eighth set) — LMB becomes UPL (upper limb) and is not part of mobility; only SCI is the same as WHEEL"` (the full heading of the eighth-set entry, found exactly once: `git grep -c -F "<heading>" references/project-standards.md` prints 1). **CONFIRMED 2026-11-13 (tenth set, OI-49, "Confirm both"):** display name "people with upper-limb differences or disabilities"; description "People whose disability or limb difference affects the shoulder, arm or hand (reach, grip and manipulation), including people who use an upper-limb prosthesis. Not part of the mobility family; the lower-limb counterpart is `LLD`."; category `general` (the CHECK has no physical-not-mobility value: `dbcore.check_values(conn, 'base_taxonomy_identity', 'category')`; `general` already holds `TALL`, `BAR`, `LPA`; a new category value would be a schema change and is the owner's to ask for). The code `UPL` was retired by DR-2026-07-23 in favour of `LMB` and is reinstated by the owner (T-058 marks the old crosswalk).
2. **Place each `LMB` crossing by what it names**, judging its `icf_code` and `mechanism`: upper limb → add the same `icf_code`, `mechanism` and `mapping_confidence` for `UPL` with `add-population-icf-link`, provenance naming the old `link_id`; lower limb → the same for `LLD` (stop if `LLD` does not exist yet); then retire the old row with `retire-population-icf-link`. On 2026-11-12 all six name grip and bilateral arm function, so all go to `UPL`. The table's UNIQUE refuses a duplicate; nothing is copied twice.
3. **Figures and grades on `LMB`:** none today. If any appear, carry each by what it names (upper limb → `UPL`; a lower-limb difference → `LLD`) with T-018's link verbs; never fan out a grade.
4. **Retire `LMB`:** `retire-identity --code LMB --to-identity UPL` with the same `--approval-ref` (the eighth-set heading) and a `--reason` quoting the eighth set.
5. **Report, do not decide:** the edges the eighth and ninth sets leave open (an upper-limb prosthesis user is `UPL`: ratified 2026-11-13, OI-50; whether `UPL` has children: not asked, none invented; the lower-limb half of `LMB`'s old description now belongs to `LLD`, with no row to move today).

**What reads what this task adds or changes:** every writer that takes an identity code (they refuse `LMB` and name `UPL`); the engine's identity predicate; T-058 (prose).

**Data migration.** This task lands rows through `scripts/emit_data_migration.py`, which names the file itself; never type a migration name or number. The pull request contains no schema migration.

## 5. Caller sweep

Prose callers are T-058's (a tooling pull request after this one). Here, list them for it: `git grep -n -E "(^|[^[:alnum:]_-])(UPL|LMB)([^[:alnum:]_-]|$)" -- governance architecture skills scripts ':!scripts/migrations'`. The ledger, `sessions/` and committed migrations are records and are never edited.

## 6. Verification

**Red before, green after.** After, on the migrated database: `select identity_code,status,category,superseded_by_identity from base_taxonomy_identity where identity_code in ('LMB','UPL')` prints `LMB` deprecated with successor `UPL`, and `UPL` active; `select count(*) from identity_icf_map where identity_code='LMB' and retired_at is null` prints 0; every live `UPL` crossing names its old `link_id` in `provenance`; a writer given `LMB` refuses and names `UPL`.

**Fixtures.** Probes run on `$SCRATCH/t.db`; the batch's own rows are written on `$SCRATCH/s.db` and reach `data/guidebook.db` only through the write path of section 2.

**The gates, once each:**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8   # the research gate
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run each once, after the migration is applied and before the commit.** `preflight.sh` runs the selftest and `run_checks.py --changed-from`; do not run `run_checks.py` separately, and never `--all`.
- **Proof that each gate examined something.** A check scoped to a session id that matches no row passes having read nothing. Confirm the stem is the one stored on your rows. The tables a batch writes carry `created_by_session` and `updated_by_session`; for each table this task writes, `python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(*) from '+sys.argv[2]+' where created_by_session=? or updated_by_session=?',(sys.argv[1],sys.argv[1])).fetchone())" "$STEM" <table>` must be above 0 after the migration is applied. `research_batch_dod` prints its own `EXAMINED:` lines: read them in `dod.txt`. A passing check prints no `EXAMINED:` line in `gate.txt`; any check under `NOTHING-IN-SCOPE` there has not passed. `migration_reproducibility` compares row counts only, so an UPDATE is invisible to it: also run `python3 scripts/audit/migration_reproducibility.py --deep`, which compares every row.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "run-pipeline: hold the upper-limb population as UPL and retire LMB to it [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly. Rows land only by the write path of section 2.
- Do not hand-write SQL against a table a `db.py` verb can reach. A table no verb reaches is a gap to file (`db.py add-gap`), not a licence.
- Do not put tooling in this pull request: no schema migration, no new verb, no new check, no edit under `scripts/`, `schemas/`, `.github/` or `skills/` (CLAUDE.md rule 10). A writer gap found on the way is filed and left.
- Do not write a bibliographic field from memory when a payload is in hand; do not mark a source verified that was not re-retrieved; never leave `verification_status` NULL.
- Do not move, round or re-key an adjudicated figure. Do not back-translate a term. Do not delete an empty search.
- Do not author `best_practice_synthesis` or synthesis prose below the Opus floor.
- Do not decide doctrine (mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory). Stop instead.
- Do not treat any `[A-Z]-NN` code as a container, an example or a name.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent.
- a crossing row of `LMB` names neither the upper limb nor the lower limb clearly, so its placement would be guessed: leave it, list it, and stop before retiring `LMB`;
- a row would go to `LLD` and `LLD` does not exist yet (T-102 mints it): leave it on `LMB`, list it, and stop before retiring `LMB`;
- `retire-identity --code LMB --to-identity UPL` refuses: it names the rows still live; carry them, do not force it.

## 10. Rollback

Before the migration is applied: delete the scratch copy; nothing has changed. After it is committed: a data migration is append-only and immutable; correct a wrong row with a compensating migration written through the same verbs (retire, supersede, amend), never by editing or deleting the file.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
