# T-101  Record the research scope on every pair

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Three tasks of this plan were executed in scratch clones (T-006, T-008, T-010) and the defects they showed in the task files were corrected in every file by one generator; this file's own steps have not been executed by anyone. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-101 |
| Title | Record the research scope on every pair |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-18 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-025 merged. Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions that must be answered first.** The answer must be in `references/project-standards.md` (the ledger), in the owner's words, in one of the forms below. An answer relayed in chat, or inferred, is not an answer. If it is absent, stop, except where an entry below says which part may proceed without it.
  - **OD-04** — **Answered by the owner, 2026-11-12:** `OD-04: scope = P1+P2+P3 as recorded; UN: out; sub-national: counts toward its country` (`grep -n -F "OD-04: scope = P1+P2+P3 as recorded" references/project-standards.md`). Check: `grep -F "OD-04 STATUS:" references/project-standards.md | tail -1` must read `ANSWERED BY THE OWNER` (the ledger convention of 2026-11-12; a reserved decision has no delegated resolution). The answer is also asked to say whether a sub-national jurisdiction (filed by T-113 under a code with its country as parent) owes coverage of its own or counts toward its country (the next bullet says where that question comes from).
- **Delegated resolutions this task rests on.** OD-01, as corrected: a sub-national code carries its country as parent as a provenance relation only, and the question whether it owes or counts toward coverage is referred to the scope decision above; this task fills scope only for the codes the owner's answer names, and gives a sub-national code no scope row unless that answer covers it. Each is a resolution by an Opus-class model under the owner's delegation of 2026-11-12: not the owner's words, reversible by the owner, and read only through the ledger's gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before you open the pull request; if any line prints CLOSED, stop and report: a CLOSED gate is a stop like those of section 9.
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-01; do gate $n; done
```
- **Tests that must be red (or green) before you start:** AT-57 red. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-101-scope-fill "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-101" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"   # s.db is the batch's working copy; t.db is for probes
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

Coverage owes research from places the owner excluded, and no list exists to cut a comparison table to.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*), sum(scope_status is not null) from lang_jur_map\").fetchall())"; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from v_research_scope\").fetchall())"
```

**Expected output today:** No pair has a scope; the view returns every pair.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. With T-025's `set-pair-scope`, one call per pair (`set-pair-scope --language L --jurisdiction J --scope-status V --approval-ref "Owner answers 2026-11-12 — OD-04 (research scope), OD-23 (a later parameter reaching a source already read), OD-15 (the medical lens and the WHO licence), OD-19 (conflict between groups in the engine)" --session "$STEM"`), set `scope_status` on every pair of `lang_jur_map` from the owner's answer to OD-04, and from nothing else. The `--approval-ref` is the full heading of the entry that records that answer; confirm it is found exactly once before the first call (`git grep -c -F "<heading>" references/project-standards.md` prints 1). Quote the answer's ledger line in the migration summary. The scope is these jurisdiction codes, exactly (P1, P2, P3 as the ledger records them): **US UK AU CA DE NO SE ISO EU · FR CH NL DK FI BE IE ES IT PT · JP SG NZ KR CN**. A pair whose `jurisdiction` is one of them is `in-scope`; every other pair is `scoped-out` (the CHECK's two values: `select sql from sqlite_master where name='lang_jur_map'`). This replaces buckets 1 and 2 of 2026-09-28 as the first floor (it adds BE, CH, CN, DK, IT and drops UN).
2. `UN` is out: it has no pair today; write none. `ISO` is in scope but has no pair (a standards body, not a language community): write none, and say so in the pull request; coverage of ISO instruments is read from the sources filed `ISO`, not from a pair.
3. A sub-national instrument counts toward its country and owes no coverage alone: write no pair for a sub-national code (T-113 files them); the roll-up to the country is read through the parent by the coverage readers (T-024 item 5).
4. Change no `role` and add or delete no pair: a pair the scope needs that `lang_jur_map` lacks (for example a second official language of an in-scope country) is reported, not written; adding one is a base-vocabulary act with its own warrant (2026-11-06 E7).

**What reads what this task adds or changes:** `v_research_scope`, `coverage`.

**Data migration.** This task lands rows through `scripts/emit_data_migration.py`, which names the file itself; never type a migration name or number, and never edit the file it writes. The pull request contains no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task renames nothing and changes no code, so the sweep that applies is the one for prose that restates a fact your rows change (CLAUDE.md rule 7a). For each row id, code or value you change, search the reading surface and the governance prose, and correct a sentence your rows make false (or stop, if correcting it is not research):

```
V='<the id, code or value you changed>'
git grep -n -F -e "$V" -- governance architecture CLAUDE.md references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

Structures this task touches, for orientation: `scope_status`. The ledger (`references/project-standards.md`), `sessions/` and committed migrations are records and are never edited.

## 6. Verification

**Red before, green after.** AT-57, restated for the owner's answer. Before: no pair has a scope. After (on the migrated database), this prints `0 0` (no unscoped pair, no pair scoped against the list):
```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);S=('US','UK','AU','CA','DE','NO','SE','ISO','EU','FR','CH','NL','DK','FI','BE','IE','ES','IT','PT','JP','SG','NZ','KR','CN');q=','.join('?'*len(S));print(c.execute('select count(*) from lang_jur_map where scope_status is null').fetchone()[0], c.execute(f\"select count(*) from lang_jur_map where (jurisdiction in ({q})) <> (scope_status='in-scope')\",S).fetchone()[0])"
```
and `select scope_status, count(*) from lang_jur_map group by 1` is reported in the pull request (derived, not typed here).

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
git commit -m "run-pipeline: record owner-confirmed research scope on language-jurisdiction pairs [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
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

## 10. Rollback

Before the migration is applied: delete the scratch copy; nothing has changed. After it is committed: a data migration is append-only and immutable; correct a wrong row with a compensating migration written through the same verbs (retire, supersede, amend), never by editing or deleting the file.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
