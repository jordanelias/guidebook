# T-092  Re-tag each stored figure's circumstance from its free-text setting

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the adjudication of the Edmonton digest, Q7 and proposal P8 (`scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 by the fold of the Edmonton case study. **Held on OD-49** and on T-091. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-092 |
| Title | Re-tag each stored figure's circumstance from its free-text setting |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: which building use, which kind of work and which side of the envelope a clause addresses is read from the clause and its instrument's own scope words (a "public" building differs by instrument: ADJUDICATION Q7) |
| Traces to | ADJUDICATION Q7, P8; T-091 (the carrier); OD-49 |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-091 merged (the typed carrier and its writer flags). Check by running: the after-test of `tasks/T-091-typed-circumstance-carrier.md` section 6 on `$BASE`.
- **Owner decisions:** OD-49 (the adjudication's AQ-3; OPEN, registered 2026-11-13, not yet asked). Read the answer by `grep -F "OD-49 STATUS:" references/project-standards.md | tail -1`. Under (a3) "leave it in `setting`" this task is declined with T-091.
- **Tests that must be red before you start:** section 6's count of figures with a non-NULL `setting` and no typed circumstance is above 0.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-092-retag-circumstances "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>            # the session stem: bare in the database, with .md for emit_data_migration --session
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-092" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later block by setting `BASE`, `STEM` and `SCRATCH` again to the same values.
- **Real execution:** open with `/session-open`, then `/orient`. Follow `skills/run-pipeline_SKILL.md`. **Pilot:** stay on the branch you were given, work on the scratch copy only, and stop before the write path.
- Work only on the scratch copy, every call inline: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`. Land the rows only by the write path:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```

## 3. The problem, in the guidebook's terms

Once T-091 gives a figure typed cells for its circumstance, the stored figures still hold theirs only in free text, so the engine's new branch (or key) sees none of them. Each must be read back from its clause and its instrument's scope words and typed, or the carrier changes nothing that is already held.

**Evidence command** (read-only, on `$SCRATCH/t.db`): the subject, measured as P8 asked:

```
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True);print(c.execute('select parameter_id, count(distinct setting) from source_value_extractions group by 1').fetchall())" "$SCRATCH/t.db"
```

**Output on 2026-11-13:** every parameter with figures has more than one distinct `setting`. The columns T-091 adds are not named here; read them from T-091's design file.

## 4. The change

Order of preference, from CLAUDE.md §8. Every verb this task needs is T-091's; it adds no code.

1. For each figure with a non-NULL `setting` (and each with NULL whose clause or heading states a circumstance), read the clause and the instrument's own scope words, and write each facet the owner's answer typed through T-091's writer (`amend-extraction --field <facet>` or the verb its design names), with a `--reason` quoting the words. A facet the clause does not state is left empty, never inferred from the instrument's general scope.
2. A scope phrase is adjudicated to the vocabulary per instrument (ADJUDICATION Q7: "public" is a legal scope phrase that differs by instrument); a phrase that names no value of the vocabulary is a gap, not a new value (a value is added by data with a warrant, under the owner's answer).
3. `setting` itself is not changed here (T-091's design says when it is retired).

**What reads what this task changes:** the engine (branches or keys by circumstance); render. **Data migration.** Rows land through `scripts/emit_data_migration.py` only.

## 5. Caller sweep

A research task changes no code. Prose that states how many figures carry a building type or that none does (rule 7a):
```
git grep -n -i -e 'building type' -e 'setting' -- governance architecture references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log' | head -20
```

## 6. Verification

**Red before, green after:** the count of figures with a non-NULL `setting` and every typed facet empty (the query uses the column names of T-091's design) is above 0 before, and after is 0 or every remaining row is listed in the pull request with what was read. The engine, before and after, on one parameter whose figures differ by building use (chosen by query): its report shows them composed together before and apart after. The gates, once each:
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep      # every amendment is an UPDATE, invisible to the count-only check
```
`research_dod_session` is red by construction on a batch that searches and admits nothing (OI-55 (1)): report its lines and say so.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: type each stored figure's circumstance from its setting (OD-49) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the owner's answer; the rule per facet; rows left and why; the engine before and after>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start before OD-49 is answered and T-091 is merged. Do not infer a facet the clause does not state. Do not add a vocabulary value without a warrant and the owner's answer.
- Do not change `claimed_value`, `claim_text` or `setting`. Do not write `data/guidebook.db` directly. Do not put tooling in this pull request (rule 10).
- Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity. Do not hand-type a count.

## 9. Stop conditions

Stop and report when: OD-49 is unanswered, or answered (a3); T-091 is not merged; a clause's scope phrase names no value of the vocabulary and the answer gives no rule for it (file a gap; do not invent); a check green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: a compensating batch through the same verbs.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `record-adversarial-pass`, closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once; call `unsubscribe_pr_activity` at once; push nothing afterwards except a deliberate change.
