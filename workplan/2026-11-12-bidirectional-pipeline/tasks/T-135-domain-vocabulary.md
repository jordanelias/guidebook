# T-135  A concept's domain comes from a vocabulary the schema holds, and the non-quantity domains are read from it

_One task, one pull request (since the owner's instruction of 2026-11-15, one task of a stacked pull request: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Why this task exists, and the adjudication that chose its shape over the alternatives: `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. Every number in this file was read on 2026-11-17 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-17 by the Opus-class adjudicator of the owner's propagation and consolidation questions; its evidence command was run read-only on 2026-11-17 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-135 |
| Title | A concept's domain comes from a vocabulary the schema holds, and the non-quantity domains are read from it |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); a schema migration (a base table, `terms` rebuilt with a foreign key), the domain readers; the seed rows are the owner's answer |
| Executor | NOT FOR SONNET: Opus-class. The answer to OD-69 decides the vocabulary's shape and seed; the rebuild of `terms` recreates every view that reads it |
| Traces to | the owner's question Q1 of 2026-11-16 ("… as well as determining category …"); the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (G12); CLAUDE.md rule 8 ("A vocabulary comes from the column's own CHECK"); `scripts/db.py` (`grep -n -F 'has no CHECK, so there is no vocabulary' scripts/db.py`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** none (after T-129 if both are open: both migrate tables that point at `terms`, and the second derives its migration number from the first). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** OD-69 (what "category" means in the owner's question, and whether a concept's domain is a fixed vocabulary the owner approves). This file's design is the recommended answer; another answer is a stop.
- **Tests that must be red before you start:** `T135-01` (section 6).
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-135-domain-vocabulary "$BASE"                               # real execution only; on a stacked batch, the batch's branch instead
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-135" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `W=…; BASE=…` line and the `export SCRATCH=…` line above, and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call.
- **Real execution:** run `/session-open` before the first command. **Pilot or dry run:** no `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given, and stop after section 7.

## 3. The problem, in the guidebook's terms

A concept's topic domain (circulation, acoustic, lighting, wayfinding and the rest) is the closest thing the pipeline has to the "category" the owner asked about, and it is free text: `terms.domain` has no CHECK, `add-term --domain` stores any string, `amend-term` accepts a domain only if another term already carries it (a live-rows sample standing in for a vocabulary, which CLAUDE.md rule 8 forbids), and the domains a parameter may not be are a typed list in code (`dbcore.NON_QUANTITY_DOMAINS`) beside the column it describes. So a misspelt domain makes a new category, and nobody is named as having decided what the categories are.

**Evidence command** (run from the repository root, after the set-up block; it reads the canonical database read-only):

```
python3 -I -c "import sqlite3,sys;sys.path.insert(0,'scripts');import dbcore;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(dbcore.check_values(c,'terms','domain'), c.execute('select domain, count(*) from terms group by 1').fetchall(), sorted(dbcore.NON_QUANTITY_DOMAINS))"
```

**Expected output today:** `set()` (no vocabulary); the domains in use with their counts; the typed non-quantity list.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

**Gated on OD-69. With the recommended answer (a fixed vocabulary, seeded from the domains in use, the owner confirming the list once):**

1. **One base table, `term_domains`** (`domain_code TEXT PRIMARY KEY`, `label_en TEXT NOT NULL`, `is_quantity_domain INTEGER NOT NULL CHECK (is_quantity_domain IN (0,1))`, the session and time columns), seeded in the same migration with exactly the list the owner confirmed (the confirmation is a ledger entry the migration's comment names; no domain is invented).
2. **`terms` rebuilt** with `domain TEXT REFERENCES term_domains(domain_code)` (create, copy, drop, rename; every view that reads `terms` recreated: `select name from sqlite_master where type='view' and sql like '%terms%'`). A live domain not in the confirmed list stops the task (it is data for a research batch to correct first).
3. **`dbcore.NON_QUANTITY_DOMAINS` deleted;** its readers (`git grep -n NON_QUANTITY_DOMAINS -- scripts`) read `term_domains.is_quantity_domain = 0` through one helper. `amend-term --domain` and `add-term --domain` are validated by the foreign key's table, not by a sample of live rows; `db.py add-domain` is not added (a new domain is the owner's: a migration naming the owner's ledger entry).
4. Tests and the stage map (`term_domains: base`).

**With another answer:** stop; the file is rewritten to the answer first (for example, if "category" meant a source's evidence type, a claim's type, a quantity kind or a design scale, each is already a typed column or a derivation, and the adjudication's table says where).

**What reads what this task adds or changes:** `add-term`, `amend-term`, `add-parameter`'s domain refusal (T-010), `mint-term-from-catalogue`, T-130's `owner` mark (design B5 reads the non-quantity domains), and render's grouping of topics (T-037) when it lands.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_<slug>.sql`, and it ends by setting `PRAGMA user_version` to the same number. Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (a new column must not add a candidate). Apply it only with `python3 scripts/migrate_db.py`. Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). A view the migration rewrites is dropped and recreated in it; list them first (`select type, name from sqlite_master where sql like '%<table>%'`). The pull request contains no `scripts/migrations/data_*` file. After the migration is applied to your clone, run `python3 scripts/generate/context_map.py` and commit the regenerated `governance/context-map.yaml` (again after your last edit to `scripts/`).

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it and what existing code it replaces or makes deletable.

## 5. Caller sweep

Names to sweep: `NON_QUANTITY_DOMAINS`, `domain_key`, `--domain`, `terms.domain`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you change; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention*. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`; `machines.yaml` there is hand-written and is swept); `references/project-standards.md` (the append-only ledger); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference; it is red on the base, so only a failure line your change adds is yours. An object that returns 0 rows is unproven, not clean.

**Callers already known** (found by this file's author; each is in scope): `scripts/db.py` (the refusals of `add-parameter` and `amend-term`; `grep -n 'NON_QUANTITY_DOMAINS\|domain_key' scripts/db.py`); `scripts/dbcore.py`; the T-010 tests (`git grep -l NON_QUANTITY_DOMAINS -- scripts/tests`); every view of item 2; `governance/context-map.yaml`.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `derived_not_curated_audit column_vocabulary_audit schema_reference_audit test_db_integrity migration_reproducibility context_map_fresh`. Run each as the registry runs it and keep the output:

```
CHECKS="derived_not_curated_audit column_vocabulary_audit schema_reference_audit test_db_integrity migration_reproducibility context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
A check red here was red before you touched anything: record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** A new test file, `scripts/tests/test_term_domains.py`, registered `test_term_domains`. `T135-01`: `dbcore.check_values`-style read of the domain vocabulary returns the confirmed set (read from `term_domains`, never typed in the test), and `add-term --domain <a string not in it>` is refused naming the vocabulary. `T135-02`: no constant in `scripts/` lists a domain (`derived_not_curated_audit` reports none; an AST scan of `dbcore.py` finds no `frozenset` of domain strings). `T135-03`: `add-parameter` still refuses a term in a non-quantity domain, now read from the table. Before: `T135-01` red. After: green.

**Writing the test.** Case ids carry this task's prefix (`T135-01`, …); confirm it is free first (`git grep -c '"T135-' -- scripts/tests` prints nothing). Never type into a test an id, a code or a count the database can derive: choose every probe by query, or build it on the test's own scratch copy, labelled `TASK-FIXTURE`. A probe for "the legitimate case still works" must be one no other refusal stops. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`; compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before.

**Step 4: the gate, once**, when every edit is made, before the commit, in the background with a long timeout:

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`. A FAIL on a check that was red on the base is not yours: run its `cmd` once on the base in a worktree and give both lines.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: a concept's domain comes from a vocabulary the schema holds [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, from `date -u`.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author a specification row or any synthesis prose.
- Do not treat any `[A-Z]-NN` code as a container, an example or a name.
- Do not put research rows (`scripts/migrations/data_*`, new evidence, extractions, merges, determinations) in this pull request (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb, flag or script that section 4 does not name. If one seems needed, stop and report. **This does not forbid fixing a caller** the sweep of section 5 finds.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass; do not choose, add or rename a domain yourself: the list is the owner's answer to OD-69.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller you cannot repair without adding something section 4 does not name;
- a check or test that was green in the before-run is red in the after-run, at any level;
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent;
- OD-69 is unanswered, or answered in a form other than this file's design;
- a live `terms.domain` value is not in the confirmed list.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished. On a stacked batch, the end-of-batch sweep of the owner's instruction of 2026-11-15 (later) follows the last task (`grep -n -F "sweep the changes forward and backward" references/project-standards.md`).
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, poll it, or schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
