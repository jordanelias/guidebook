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
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); a schema migration (a base table, `terms` rebuilt with a foreign key), the domain readers; the seed rows are the owner's answer _[Amended 2026-11-19 (ledger: Owner ratification 2026-11-19), because the last clause is now false: the seed rows are the values in use at migration, each warranted "in use at migration", and a new domain is added by data with a warrant (`db.py add-domain`); no list is the owner's. Section 12 governs.]_ |
| Executor | NOT FOR SONNET: Opus-class. The answer to OD-69 decides the vocabulary's shape and seed; the rebuild of `terms` recreates every view that reads it _[Amended 2026-11-19 (same ledger entry): the shape is decided (adjudication 3, item 10). Still Opus-class, because the task writes the meaning of a warrant (`add-domain`) and moves a judged rule (`NON_QUANTITY_DOMAINS`) into a typed column.]_ |
| Traces to | the owner's question Q1 of 2026-11-16 ("… as well as determining category …"); the adjudication `workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` (G12); CLAUDE.md rule 8 ("A vocabulary comes from the column's own CHECK"); `scripts/db.py` (`grep -n -F 'has no CHECK, so there is no vocabulary' scripts/db.py`); _added 2026-11-19:_ `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md` section 3 items 10 and 60, section 4 item 5; the ledger entries "Owner statement 2026-11-18 (third) — OD-69" and "Owner ratification 2026-11-19" |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`; otherwise the remote branch that carries the newest commit to this folder. Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`.
- **Tasks that must be merged to the integration base first:** none (after T-129 if both are open: both migrate tables that point at `terms`, and the second derives its migration number from the first). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`. _[Amended 2026-11-19 (ledger: Owner ratification 2026-11-19, ACTION (2), "in its order"): the adjudication's section 4 orders this task fifth, after the tooling tasks T-136, T-137 and T-138 (authored in parallel; T-136 rebuilds `term_aliases` and `term_relations`, both of which hold a foreign key into `terms`). On a stacked branch each of them is a commit on HEAD; check by running each one's own after-test (its section 6). The T-129 clause stands.]_
- **Owner decisions:** none. OD-69 is a delegated resolution (next bullet), not a decision that needs the owner's own words.
- **Delegated resolutions this task rests on.** OD-69 (what "category" means in the owner's question, and whether a concept's domain is a fixed vocabulary the owner approves): "a concept's topic area; the list is not fixed; held as rows extended by data with a warrant", RESOLVED UNDER DELEGATION with its CHECK confirmed, in the entry the owner ratified ("Ratify all", ledger "Owner ratification 2026-11-19"; `git grep -n -E '^OD-69 (STATUS|CHECK):' references/project-standards.md`, the last line of each kind). The design of section 4 is NOT that answer; section 12 is. ACTION (2) of "Owner statement 2026-11-18 (third) — OD-69" ("do not execute T-135 until the owner answers the form") is superseded on contact by the 2026-11-19 entry's readings (CLAUDE.md rule 0). Run the gate of section 12.1 (`for n in OD-69; do gate $n; done`); if it prints CLOSED, stop.
- **Tests that must be red before you start:** `T135-01` (section 6). _[Amended 2026-11-19: `T135-01`, `T135-02`, `T135-04` and `T135-05` of section 12.4.]_
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

**Expected output today:** `set()` (no vocabulary); the domains in use with their counts; the typed non-quantity list. _[Re-run 2026-11-19 read-only: `set()`; the domains in use with their counts; `['economics', 'functional_axis', 'legal', 'medical', 'methodology', 'population']`. Every member of the typed list is still a domain some term carries (`medical` included, though the medical lens was deleted on 2026-11-16: the domain is a fact of the term). Section 12.2 adds two more commands.]_

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

_[Amended 2026-11-19 (ledger: Owner ratification 2026-11-19): items 1 to 3 below are FALSE as written. The list is not fixed and no owner confirms it; the seed is the values in use, warranted "in use at migration"; `db.py add-domain` IS added. Do not execute items 1 to 4 below; execute section 12.3. They are kept as the record of the design that was held.]_

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

**Step 2: red before, green after.** _[Amended 2026-11-19: the cases below assume a confirmed list; the cases that govern are section 12.4's.]_ A new test file, `scripts/tests/test_term_domains.py`, registered `test_term_domains`. `T135-01`: `dbcore.check_values`-style read of the domain vocabulary returns the confirmed set (read from `term_domains`, never typed in the test), and `add-term --domain <a string not in it>` is refused naming the vocabulary. `T135-02`: no constant in `scripts/` lists a domain (`derived_not_curated_audit` reports none; an AST scan of `dbcore.py` finds no `frozenset` of domain strings). `T135-03`: `add-parameter` still refuses a term in a non-quantity domain, now read from the table. Before: `T135-01` red. After: green.

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
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass; do not choose, add or rename a domain yourself: the list is the owner's answer to OD-69. _[Amended 2026-11-19: the clause after the semicolon is false: the list is open and any session adds a domain with a warrant. What stays forbidden is section 12.5's.]_

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
- _[Amended 2026-11-19: the two lines above are replaced by section 12.6's stop conditions.]_

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass.
2. Run `/batch-done`; it is the only definition of finished. On a stacked batch, the end-of-batch sweep of the owner's instruction of 2026-11-15 (later) follows the last task (`grep -n -F "sweep the changes forward and backward" references/project-standards.md`).
3. Push the branch. Open the pull request **last**, once, against the integration base. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified; a heading "Task-file defects". End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it. Do not watch it, poll it, or schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.

**Amended 2026-11-17 on the owner's answer to OD-69** (ledger, "Owner answers 2026-11-17"). The meaning of "category" is settled: a concept's topic area, the overall class of a parameter (the owner's example: circulation, for the parameters about ramps, stairs, corridors and doors; "the project is supposed to be like that"). **Not answered, so this task stays held:** whether the classes are a fixed list, who confirms it, and which of the domains now in use (`select domain, count(*) from terms group by 1`) are topic areas and which are kinds of concept a parameter may not be (`dbcore.NON_QUANTITY_DOMAINS`). The seed of `term_domains` is the list the owner confirms, not the values in use.

## 12. Amended 2026-11-19 (ledger: Owner ratification 2026-11-19) — what now governs

_Written 2026-11-19 by an Opus-class task author on the owner's instruction "Author the tooling tasks in order" (the ratified adjudication `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, section 4 item 5; section 3 items 10 and 60). Every figure below was read on 2026-11-19 read-only and is given with its command: re-run it; do not trust the figure. Where this section and sections 1 to 11 disagree, this section governs; where it is silent, sections 5, 7, 10 and 11 stand as written, and section 6 steps 1, 3 and 4 stand with the check list of 12.4. Sections 1 to 11 are kept as the record of what was held._

### 12.1 The gate, the order and the set-up

- **The decision this task rests on, by the convention of 2026-11-12** (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). Run it before you start and again before the commit; if it prints CLOSED, stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-69; do gate $n; done
grep -c -F "## Owner ratification 2026-11-19" references/project-standards.md      # 1: the entry that ratifies items 10 and 60 by reference
```
  Printed 2026-11-19: `OD-69 OPEN (delegated; confirmed)` and `1`. Item 60 carries no OD number; it is ratified by reference in the same entry ("the design questions numbered 12 to 91 that carry no OD number are ratified by reference"), which that entry's ACTION (3) still marks an [ASSUMPTION] until the owner confirms the breadth of "all": if a later ledger line withdraws the CHECK lines of that entry, stop.
- **Order.** Fifth of the adjudication's section 4: after T-136, T-137 and T-138 (each a commit on HEAD of the stack, proven by its own after-test), before T-139. Nothing already merged is reverted.
- **Set-up (the stacked-branch convention, `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1, or the brief the coordinator names).** Stay on the branch you are given; do not `git switch -c`; do not run `/session-open` (the coordinator has). Diffs, the gate's `--base` and the code-size line use `$BASE_PRE`:
```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin; BASE_PRE=$(git rev-parse HEAD); echo "BASE_PRE=$BASE_PRE"
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-135" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
  Every probe or fixture write passes `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline and `--session session_task-probe`; never delete or edit a `refusals.jsonl`.

### 12.2 The problem, re-measured

Section 3's command still holds. Two more, read-only:
```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select sum(domain is null), count(*), sum(domain<>lower(trim(domain))) from terms').fetchone(), [(t,f[3]) for (t,) in c.execute(\"select name from sqlite_master where type='table'\") for f in c.execute(f'pragma foreign_key_list(\"{t}\")') if f[2]=='terms'])"
grep -n -A3 'is not a domain another term' scripts/db.py | head -4
```
Printed 2026-11-19: `(0, 94, 0)` (no term without a domain, none in another letter case) and seven foreign keys into `terms` (`term_adjudications`, `base_parameters`, `parameter_declinations`, `term_aliases`, `term_label_picks`, `term_relations` twice); the second shows `amend-term --field domain` accepting a domain only when another term already carries it, so a class whose last carrier moves away can never be chosen again (item 60). If either differs, stop.

### 12.3 The change (replaces section 4 items 1 to 4)

1. **One base table, `term_domains`** (one schema migration; derive its number as section 4 says): `domain_code TEXT PRIMARY KEY` with a CHECK of the shape the seeded values have (lower-case letters and underscores, a letter first: the shape `add-quantity-kind` refuses outside); `admits_parameter INTEGER NOT NULL CHECK (admits_parameter IN (0, 1))`; `warrant_reason TEXT NOT NULL` and `judge TEXT NOT NULL`, each with a non-blank CHECK; `created_at`, `created_by_session`. No `label_en` (the code is the word; nothing reads a second name: CLAUDE.md §8), no `notes`.
2. **The seed, written by the migration from data, never typed as a list:** `INSERT INTO term_domains SELECT DISTINCT domain, …` over `terms.domain` (every value in use at migration), `warrant_reason` `in use at migration NNN (terms.domain)`, `judge` `migration_NNN`. `admits_parameter` is 0 for exactly the members of `dbcore.NON_QUANTITY_DOMAINS` as it stands at execution: they are MOVED from the constant into the migration, which becomes their one home, and the reason row of each says so (`… admits no parameter: moved from dbcore.NON_QUANTITY_DOMAINS, the T-010 reading`). Which in-use values are topic areas and which are kinds of concept a parameter may not be is moved, not decided (adjudication item 10); a later judgment changes a row by data.
3. **`terms` rebuilt** with `domain TEXT REFERENCES term_domains(domain_code)` (nullable: a term with no domain stays legal). Create, copy, drop, rename inside the migration with `PRAGMA foreign_keys=OFF` and a `PRAGMA foreign_key_check` that prints nothing after; recreate every index, trigger and view that names `terms` (list them first: `select type, name, sql from sqlite_master where sql like '%terms%'` and keep the ones that read the table `terms` itself, not `observed_terms`). Every row of `terms` must be identical before and after, column by column.
4. **`db.py add-domain --domain-code C --admits-parameter yes|no --reason TXT --judge NAME --session S [--dry-run]`.** Any session may add a class (OD-69: "the list is not fixed"; no owner gate, no `--approval-ref`). Refuses, each naming the next action and saying `Nothing was written.`: a blank session; a code outside the shape (the message reads the shape from the CHECK, never retypes it); a code already held (naming its judge and reason, and `amend-term` or T-130's candidates for a rename); a blank reason or one with no letter; a blank judge; an `--admits-parameter` outside `yes|no`. The writer is in the capture set by derivation (`dbcore.writable_tables`); confirm `emit_batch_sql` captures it on a scratch copy.
5. **`dbcore.NON_QUANTITY_DOMAINS` and `dbcore.domain_key` are deleted.** One helper, `dbcore.non_quantity_domains(conn)`, returns `{domain_code where admits_parameter = 0}`; `add-parameter`'s domain refusal (T-010) and `amend-term`'s "already a parameter" refusal read it. With a foreign key the value is exact, so no fold is needed (a case or spacing variant is refused by the key, which is the point).
6. **`amend-term --field domain`:** the "another term already carries it" sample is deleted (rule 8: live rows are a sample, never the vocabulary); `dbcore.fk_declared` (already called there) now refuses an unknown domain. Make the refusal of an unknown domain, at `add-term`, `amend-term` and `mint-term-from-catalogue`, name `db.py add-domain` as the next action (pass `remedy=` to `fk_declared`; do not write a second check). A class row persists when its last carrier moves (item 60 closed).
7. **Stage map:** `term_domains: base` in `governance/stage-map.yaml`; regenerate `governance/context-map.yaml` after the migration is applied.
8. **Not built, named:** changing an existing class's `admits_parameter`, and renaming or merging a class (a judged act through T-130's candidates, adjudication item 10). Each is a GAP to file in the pull request, not code.

**What reads what this task adds:** `add-term`, `mint-term-from-catalogue`, `amend-term` and the key itself (the vocabulary); `add-parameter` and `amend-term` (the non-quantity rule, through the helper); T-130's `owner` mark (design B5); render's grouping by topic (T-037) when it lands. **What wrong thing reaches the guidebook without it:** a misspelt or case-variant domain silently becomes a new topic class, so a parameter files under a near-duplicate class (the owner's harm in Q2); and the rule that a lens or a body of law is never a parameter lives in a typed list beside the column it describes (rule 8). **Code it makes deletable:** `NON_QUANTITY_DOMAINS`, `domain_key`, and `amend-term`'s live-rows sample.

### 12.4 Verification (replaces section 6 step 2; the before-run of step 1 adds `test_db_amend_writers test_run_pipeline_refusals test_scan_contract emit_batch_sql_selftest`)

A new file `scripts/tests/test_term_domains.py`, registered `test_term_domains` (`battery: tests`, `kinds: [tooling, data]`, `level: advisory`, `basis: hygiene`, a `no_floor:` that says its subject is its own fixtures), each case on a scratch copy built inside the test (`TASK-FIXTURE`), every probe chosen by query. Confirm the prefix is free first (`git grep -c '"T135-' -- scripts/tests` prints nothing; printed nothing on 2026-11-19). Each case below must be shown red on the unchanged code or on a named seeded defect that is then removed (restore with `cmp`):

- `T135-01` the vocabulary is the table's: the set of `term_domains.domain_code` equals the set of `terms.domain` in use on the pre-migration copy (both derived), and `add-term --domain <a code not held, built by the test>` is refused naming `add-domain`. Red before (no table; any string stored).
- `T135-02` no constant in `scripts/` lists a domain: an AST scan of `scripts/dbcore.py` and `scripts/db.py` finds no string literal equal to any `term_domains.domain_code` inside a `frozenset`, `set`, `tuple` or `list` literal, and `dbcore` has no attribute `NON_QUANTITY_DOMAINS`. Red before.
- `T135-03` `add-parameter` refuses a term whose domain has `admits_parameter = 0` (the probe term chosen by query among terms that are not parameters and not declined); seeded defect: flip that row's flag to 1 on the copy and the refusal is not the domain refusal. Green before for the refusal, red on the seeded defect after (proves the table is what is read).
- `T135-04` `add-domain`: one case per refusal of 12.3 item 4 and one legitimate write; then `add-term --domain` with the new code passes. Each refusal's case red when its check is removed. Red before (no verb).
- `T135-05` item 60: a term moved by `amend-term --field domain` into a class no other term carries but `term_domains` holds is accepted; moving the last carrier of a class away leaves the class row, and moving a term back into it is accepted. Red before (the sample refuses).
- `T135-06` the key holds at the schema: with `PRAGMA foreign_keys=ON`, a raw INSERT of a term with an unknown domain on the copy raises; a case variant of a held code (`upper()` of one, derived) is refused by `add-term`. Red on a seeded defect (the key dropped from the migration on a copy).
- `T135-07` the rebuild loses nothing: every row of `terms` and every row of each of the seven referencing tables is identical on the copy before and after the migration, and `sqlite_master.sql` of every object other than `terms` and the new table is unchanged except the views the migration names.

Also run, before and after: `python3 scripts/audit/derived_not_curated_audit.py` (no new finding; a removed one is reported), `python3 scripts/audit/joined_cells_census.py` (no new candidate), `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0), `python3 scripts/audit/migration_reproducibility.py --deep` (PASS), `python3 workplan/pipeline-state-graph/build_graph.py --check` (no failure line added; a new verb and table are expected in the graph only after regeneration at the end of the stack).

**Caller sweep (section 5, names widened):** `NON_QUANTITY_DOMAINS`, `domain_key`, `terms.domain`, `--domain`, `is not a domain another term`, `has no CHECK, so there is no vocabulary`, `term_domains`. Known on 2026-11-19 by the section 5 commands: `scripts/db.py` (the `add-parameter` refusal and its docstring, `amend_term`, the `add-parameter` help string naming the constant), `scripts/dbcore.py` (the constant, its comment, `domain_key`), `scripts/audit/research_batch_dod.py` (a comment naming the constant: a prose caller, corrected), `scripts/tests/test_run_pipeline_refusals.py` (T010-01 asserts the constant exists and its members are carried: rewrite it to assert the same of the table, and say so in the pull request), `scripts/tests/test_db_amend_writers.py` and `scripts/tests/test_scan_contract.py` (fixtures filter on the constant: point them at the helper). `--domain` also names `add-conflict`'s prose label (`conflicts.domain`), which is not `terms.domain`: a mention.

### 12.5 What you must NOT do (in addition to section 8)

- Do not type a domain value into the migration, a test or the code, except the members of `NON_QUANTITY_DOMAINS` moved once into the migration's `admits_parameter = 0` statement (read them from the constant at execution and copy them; the constant is then deleted).
- Do not rename, merge or re-flag a seeded class; do not decide whether `medical`, `population` or any other in-use value is a topic area: the migration moves what is, nothing more.
- Do not add a `label_en`, an owner gate or an `--approval-ref` to `add-domain`.

### 12.6 Stop conditions (replace the two last lines of section 9)

- the gate of 12.1 prints CLOSED, or the ratification entry is withdrawn as to item 10 or 60;
- 12.2 prints a term with a domain in another letter case or with surrounding spaces (it is data for a research batch to correct first, through `amend-term`, after this task: report it), or a foreign key into `terms` the list does not hold;
- a member of `NON_QUANTITY_DOMAINS` is no longer a domain any term carries (the seed would then lack it; report, do not add it by hand);
- T-136, T-137 or T-138 is not on HEAD, or the migration number you derive collides with theirs.

### 12.7 Corrections 2026-11-19, after the adversarial review of this amendment (the lines above stay as written; where they disagree, these govern)

- **Correction to 12.3 item 1 (the code's shape).** The CHECK "lower-case letters and underscores, a letter first" is withdrawn: OD-69's ruling ("held as rows extended by data with a warrant") specifies no shape, and that CHECK would refuse a topic area recorded in a non-Latin script, against the owner's direction of a base that is dynamic across all languages. **The author's reading, for the coordinator to confirm:** `domain_code TEXT PRIMARY KEY` with only `CHECK (length(trim(domain_code)) > 0 AND domain_code = trim(domain_code))`, in any script; no separate label (no reader asks for one; one value per cell). `add-domain`'s shape refusal of 12.3 item 4 is replaced by those two; `T135-04` tests a non-Latin code accepted and a blank or padded one refused. 12.6's second bullet stands for case and spaces only.
- **Correction to 12.2 and `T135-07` (a count).** "seven foreign keys into `terms`" is right; "the seven referencing tables" is not: six tables carry the seven keys (`term_relations` carries two). Derive, never quote: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);k=[(t,f[3]) for (t,) in c.execute(\"select name from sqlite_master where type='table'\") for f in c.execute(f'pragma foreign_key_list(\"{t}\")') if f[2]=='terms'];print(len({t for t,_ in k}), len(k))"` printed `6 7` on 2026-11-19 (T-136, ordered first, may change it: re-run).
- **Correction to `T135-02` (it could not go green).** An AST scan for any domain string inside a literal collection fails on legitimate code: `scripts/db.py`'s `_CONNECTION_TARGET_KINDS` (`grep -n "_CONNECTION_TARGET_KINDS =" scripts/db.py`) holds `methodology`, a domain word, among column names. The test asserts what the rule means, a TYPED LIST OF DOMAINS: no literal `frozenset`, `set`, `tuple` or `list` in `scripts/` (excluding `scripts/migrations` and `scripts/tests`) has two or more string members that are ALL `term_domains.domain_code` values read from the copy; and `dbcore` has no `NON_QUANTITY_DOMAINS`. Green after the change; seeded defect: add a literal holding two domain codes read from the table to a temporary copy of `dbcore.py`, and the case goes red; `_CONNECTION_TARGET_KINDS` does not trip it (a member is not a domain).
