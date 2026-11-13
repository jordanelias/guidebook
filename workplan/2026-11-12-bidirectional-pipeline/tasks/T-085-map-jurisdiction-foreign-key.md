# T-085  The map's jurisdiction column points at the registry

> **HELD** — waits for T-084, which itself waits for the owner's answer to OI-55 (4). A foreign key cannot be added while the map holds a code the registry lacks (`PRAGMA foreign_key_check` would fail on those rows). An executor that opens this file before T-084 is merged does not start it: it reports that the task is waiting, and for what.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 ("the foreign key on `lang_jur_map.jurisdiction` (after OI-55 (4))"); T-024 section 4 (`grep -n 'no foreign key on .lang_jur_map.jurisdiction' workplan/2026-11-12-bidirectional-pipeline/tasks/T-024-jurisdiction-registry.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-085 |
| Title | The map's jurisdiction column points at the registry |
| Wave | 3 |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OI-56; AT-28 ("Every jurisdiction value in every table resolves to one declared vocabulary; adding a member requires no change to any script"); AT-58; CLAUDE.md rule 8 (a vocabulary is the registry, enforced by the schema, not by an audit beside it) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-084 merged (the map then names only declared codes). Check: section 3's first command prints `[]`.
- **Owner decisions:** none of its own; it inherits OD-46 (OI-55 (4)) through T-084.
- **Tests that must be red before you start:** `PRAGMA foreign_key_list(lang_jur_map)` names no `base_jurisdictions` key.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-085-map-jurisdiction-foreign-key "$BASE"       # real execution only
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-085" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

The map and the registry are two homes of "which jurisdictions exist", kept in step only by an audit run after the fact. A pair for an undeclared code can be written and is caught later, if at all; a foreign key refuses it at write.

**Evidence commands** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select distinct l.jurisdiction from lang_jur_map l left join base_jurisdictions b on b.jurisdiction_code=l.jurisdiction where b.jurisdiction_code is null').fetchall());print(c.execute('pragma foreign_key_list(lang_jur_map)').fetchall());print([(r[0],r[1]) for r in c.execute(\"select type,name from sqlite_master where sql like '%lang_jur_map%'\")])"
```

**Output on 2026-11-13** (before T-084): a list of 17 codes (T-084 section 3); `[]` (no foreign key); `[('table', 'lang_jur_map'), ('view', 'v_research_scope')]`. **Expected once T-084 is merged:** `[]`, `[]`, and the same objects (re-derive them: T-025 or T-101 may have added a reader).

If the first list is not empty, T-084 is not done: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **Schema migration:** rebuild `lang_jur_map` with `jurisdiction TEXT NOT NULL REFERENCES base_jurisdictions(jurisdiction_code)`, every other column, CHECK and the primary key exactly as the live DDL has them (read it: `select sql from sqlite_master where name='lang_jur_map'`; never retype it from this file). SQLite adds a foreign key only by create, copy, drop, rename; recreate every view that names the table (on 2026-11-13 `v_research_scope`) in the same migration from its live DDL. End with `PRAGMA foreign_key_check(lang_jur_map)` returning nothing on the migrated copy.
2. **The writers' refusal stays first.** T-025's `add-lang-jur-pair` (merged before T-084, which needs it) refuses an undeclared jurisdiction through `dbcore.check_jurisdiction` (`grep -n 'def check_jurisdiction' scripts/dbcore.py`): keep it, so a session meets a named refusal before the bare `FOREIGN KEY constraint failed`. Do not add a second check.
3. **The after-the-fact readers are now mentions for this table.** The registered check `jurisdiction_db_vocabulary` and the `jurisdictions_unreachable` field of `db.py coverage` (`grep -n 'jurisdictions_unreachable' scripts/db.py`) keep their other subjects; if one of them reads `lang_jur_map` only to do what the key now does, say so in the pull request and leave it (deleting a check is a separate act with its own evidence, CLAUDE.md §8).

**Chosen (authoring 2026-11-13):** a real foreign key, after the data is clean, rather than T-024's per-row form (impossible: one column carries one key for all its rows, T-024 pilot defect 1) or a trigger (a trigger restates what a key says).

**Schema migration (this task has one).** Never type a migration number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, ending with `PRAGMA user_version` set to the same number. Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). Run `python3 scripts/audit/joined_cells_census.py` before and after. After the migration, run `python3 scripts/generate/context_map.py` and include its output. The pull request contains no `scripts/migrations/data_*` file. A data migration replayed after this one that INSERTs a pair for an undeclared code now fails at rebuild: if one is open while you work, say so in the pull request.

**What reads what this task adds:** every writer of `lang_jur_map` (the key refuses an undeclared code); `v_research_scope` (unchanged in what it returns). **What it makes deletable:** possibly the `lang_jur_map` arm of the jurisdiction audits (item 3; not deleted here).

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: `lang_jur_map`, `v_research_scope`, `jurisdictions_unreachable`, `add-lang-jur-pair`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: a test that builds `lang_jur_map` from the live DDL with foreign keys on and no `base_jurisdictions` table (it now fails `no such table`, as `test_evidence_cell_state_2_3` did for T-020: add the parent to its live-DDL name list); a fixture that inserts a pair for an undeclared code; a sentence that says the map is kept in step by an audit only. A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="jurisdiction_db_vocabulary test_db_amend_writers test_run_pipeline_refusals test_evidence_cell_state_2_3 schema_reference_audit migration_reproducibility"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
Drop a name that is not a registry id on the day and say so.

**Step 2: red before, green after** (cases `T085-01`…; prefix free: `git grep -c 'T085-' scripts/tests/`):
- `T085-01` on a migrated scratch copy, a raw `INSERT INTO lang_jur_map` with foreign keys on and a jurisdiction no registry row holds (derive one: a two-letter string not in `select jurisdiction_code from base_jurisdictions`, built by the test) is refused `FOREIGN KEY constraint failed`. Red before (accepted).
- `T085-02` the same insert with a declared code (`select jurisdiction_code from base_jurisdictions where kind='country' order by 1 limit 1`) and a language/role pair not yet in the map is accepted.
- `T085-03` `v_research_scope` returns the same rows before and after the migration (compare a hash of its sorted rows on the pre- and post-migration copies).

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` changes only by the migration, and the rebuild reproduces it.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: the language-and-jurisdiction map points at the jurisdiction registry [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: evidence before and after; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start while the map holds an undeclared code; do not admit or remove any code here (T-084's).
- Do not change any other column, CHECK or the primary key of `lang_jur_map`; do not change what `v_research_scope` returns.
- Do not write `data/guidebook.db` except through `migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: section 3's first list is not empty; `PRAGMA foreign_key_check` reports a row after the migration; a view other than those derived names the table and cannot be recreated from its live DDL; a check green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: a compensating migration in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push. Re-derive the migration number after `git merge "$BASE"` if another merged first.
