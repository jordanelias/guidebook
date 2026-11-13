# T-089  The refusal register: every captured refusal, its class, and what it cues

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the owner's statements 4 and 5 of 2026-11-13 (`grep -n -F 'Owner statements 2026-11-13 (eleventh set)' references/project-standards.md`), the adjudication's Q10 and P6 (`scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md`), and the design in `tasks/T-088-refusal-capture-and-disposition.md` section 4a. Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 by the fold of the Edmonton case study. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-089 |
| Title | The refusal register: every captured refusal, its class, and what it cues |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | owner statement 4 ("refusals will need to be dynamically typed/categorized and read by something so that we can have a proper register of specific instances of refusals as well as a way to understand them as a class so that we are able to point towards area for resolution") and statement 5 ("a cue to run a script/double check a protocol or skill/etc to ensure that the digest was actually performed correctly"); T-088 |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-088 merged (it writes `scratchpad/<session>/refusals.jsonl` and creates `scripts/audit/refusal_register.py`, which this task extends). Check by running: `grep -n 'def record_refusal' scripts/dbcore.py && python3 scripts/audit/refusal_register.py list --help`.
- **Owner decisions:** none. Nothing here writes a row; the classes are derived (statement 4 asks for that) and the cues are derived from the repository.
- **Tests that must be red before you start:** `T089-01` (section 6): no reader across sessions exists.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-089-refusal-register-reader "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-089" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

After T-088 each session keeps the refusals its writers made and how each was disposed. One session's list does not show that the same refusal keeps coming back across batches, which writer, which skill sentence or which part of the schema it points at, or whether a batch that met refusals at a stage re-checked that stage before calling itself done. The owner asked for both the instances and the class, and for the refusal to be "a cue" to re-check the digest.

**Evidence commands** (read-only; after T-088 has merged):

```
git ls-files 'scratchpad/*/refusals.jsonl' | head
python3 scripts/audit/refusal_register.py --help
python3 -c "import sys;sys.path.insert(0,'workplan/pipeline-state-graph');import build_graph as b;t=b.Tree('.');print(t.verbs['add-extraction']['writes'], t.stage('source_value_extractions'))"
python3 -c "import yaml,collections;r=yaml.safe_load(open('governance/check-registry.yaml'));print(collections.Counter(str(c.get('basis','')).split('/')[0] for c in r['checks']))"
grep -n -E '^## [0-9]+\. ' skills/run-pipeline_SKILL.md
```

**Output on 2026-11-13** (before T-088; the first two lines are T-088's to create): no committed `refusals.jsonl`; the third prints `{'extraction_lens_links': ['INSERT'], 'extraction_relations': ['INSERT'], 'source_value_extractions': ['INSERT']} judgment` (the state graph's builder already derives the tables a verb writes and each table's stage); the registry's `basis` values are stage-qualified (`judgment/…`, `evidence/…`, `base/…`, …) beside `hygiene`, `unattributed` and `cross_stage`; the skill's sections are headed `## N. <stage> — …`. If a reader across sessions already exists, stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8. **Do nothing:** fails statement 4 (no one reads twenty sessions' files to see a recurring class). **Convention:** a coordinator reading the files by hand is the curated list rule 8 forbids. **Reuse:** T-088's script and its file format; the state graph's derivation of verb to tables to stage (`workplan/pipeline-state-graph/build_graph.py`, class `Tree`); the check registry; the skill's own headings; the `gaps` table for a parked refusal's category and status. **Smallest code:** two subcommands in the existing script, and one line in `/batch-done`.

1. **`refusal_register.py register`**: reads every committed `scratchpad/*/refusals.jsonl` (`git ls-files`; an uncommitted file of the running session is added when `--session` names it) and prints the register of instances, one line each: session, `ts`, verb, the argv joined, the sentence, the disposition (or `UNDISPOSED`) and the gap id, with the gap's live `category` and `status` read from `data/guidebook.db` (`--db` overrides). Ends with `EXAMINED: <instances> refusal(s) in <sessions> session(s)`.
2. **`refusal_register.py classes [--session S]`**, every field derived at read time, never stored:
   - **signature**: the sentence with quoted values (`'…'`, `"…"`, `` `…` ``), numbers, and identifiers (`REF-\d+`, `GAP-[\w-]+`, `TERM-\d+`, `session_\S+`) each replaced by a placeholder, and whitespace collapsed; one function, so every class is computed the same way.
   - **cited rule ids**: every match in the sentence of `R\d+[a-z]?`, `OR-\d+[a-z]?`, `OD-\d+`, `OT-\d+`, `D-\d{4}`, `T-\d{3}`, `E\d+`.
   - **tables and stage**: for a `scripts/db.py` verb, `Tree(repo).verbs[verb]['writes']` and `Tree.stage(table)` (one `Tree` per run); for the engine, the stage of `specifications`. A verb the builder does not know prints `?`, never a guess.
   - **the classes**: instances grouped by signature, and again by verb, by stage and by cited id; for each group the count, the sessions, first and last seen, the share undisposed, and the dispositions and gap categories met. Ranked by count, recurring signatures first, so the top of the output is the area to resolve (the writer, the skill sentence, the schema or the stage).
   - **the triage type** of a class is what its instances were disposed as and filed under: `retried` (a policy refusal that was right), `parked` with the gap's `category` (`SW` for a missing verb or field and for a tool defect, the description says which), `waived` with its reasons. No second vocabulary is added (T-088 section 4a).
   - **the cue**: for each stage a class touches, the registered checks to re-run, derived as those whose `basis` begins with `<stage>/`, and those whose `cmd` script's text names a table the refused verb writes (read the script file named in `cmd`; never a list); and the skill section to re-read, the `## N. <stage> —` heading of `skills/run-pipeline_SKILL.md`. Printed as `CUE <stage>: re-run <check ids>; re-read "<heading>"`.
   With `--session S`, only that session's instances and their cues are printed, and the exit is 1 if any of them is undisposed.
   **Chosen (authoring 2026-11-13): import `Tree` from the state graph's builder.** Rejected: copying its `_derive_verbs` (a second home for the verb-to-table derivation, rule 8) and reading the generated `graph.json` (generated on a date and stale between builds: `python3 -c "import json;print(json.load(open('workplan/pipeline-state-graph/graph.json'))['generated'])"`). If the builder moves, this import is a caller to sweep (rule 4).
   **Chosen:** the cue is printed, not run. Rejected: running the checks from the reader (the gate already runs checks; a second runner is the duplicate CLAUDE.md §8 forbids, and §1 asks that suites be run rarely and on purpose).
3. **`/batch-done` reads the cue.** In `.claude/commands/batch-done.md`, replace T-088's `list` line by `python3 scripts/audit/refusal_register.py classes --session "$(cat scratchpad/CURRENT)"` and add: "For each `CUE` line, run the named checks once and re-read the named skill section before calling the batch done; say in the pull request what each showed. A refusal in a batch is the sign that the stage it names may not have been performed as the skill says." Keep T-088's disposition sentence.

**What reads what this task adds:** `/batch-done` (the cue for the running batch); the coordinator and the owner (the register and the classes across sessions, to choose which writer, skill sentence or schema to fix next); a tooling task that closes a parked gap (its instances are the replay list). **What wrong thing reaches the guidebook without it:** a recurring writer gap that keeps dropping one kind of content from every batch, seen by no one because each session saw it once; a digest called done although the stage its refusals point at was not re-checked. **What it makes deletable:** nothing.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`, and name what reads each addition.

## 5. Caller sweep

Names to sweep: `refusal_register`, `build_graph`, `class Tree`, `batch-done`.

**What a caller is.** As in T-088 section 5: a hit whose behaviour or truth changes with this task. `workplan/pipeline-state-graph/build_graph.py` becomes imported by a script under `scripts/`: a comment there that says nothing imports it is a caller. Left out: `workplan/` other than `workplan/pipeline-state-graph/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills workplan/pipeline-state-graph ':(exclude)scripts/migrations'
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_run_pipeline_refusals claude_skills_loadable"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

**Step 2: red before, green after** (cases `T089-01`… in `scripts/tests/test_run_pipeline_refusals.py`; prefix free: `git grep -c 'T089-' scripts/tests/`). Fixtures: a temporary tree with two session folders, each holding a `refusals.jsonl` built by T-088's `dbcore.record_refusal` (never typed JSON), from refusals produced by real `db.py` calls on a scratch copy under each fixture session; one disposed `parked` with a gap built on the copy (`TASK-FIXTURE`), one `retried`, one undisposed.
- `T089-01` `register` lists every instance of both sessions with its disposition and gap category; red before (no subcommand: assert the exit and the `EXAMINED:` line, so an absent subcommand cannot pass).
- `T089-02` two refusals with the same sentence but different quoted values and ids fall in one signature class; two different sentences do not.
- `T089-03` the stage of an `add-extraction` refusal is the stage the state graph gives `source_value_extractions` (read from `Tree`, not typed); a verb unknown to the builder prints `?`.
- `T089-04` the cue for a judgment-stage refusal names every registered check whose `basis` begins with that stage (the set read from the registry in the test) and the skill heading for that stage.
- `T089-05` `classes --session <the fixture with an undisposed refusal>` exits 1; for the fully disposed one, 0.
- Seeded defect: make the signature keep numbers; `T089-02` goes red; restore.

**Step 3: after-run.** The same loop with `after-`; nothing new may fail.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. `sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: the refusal register, its derived classes and the cue it gives a batch [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the owner's statements 4 and 5; what is derived from where; evidence before and after; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not store a derived field (signature, stage, tables, class) in any file or table; compute it at read time.
- Do not add a class vocabulary, a gap category, a table or a registered check. Do not run the cued checks from the reader.
- Do not copy the state graph's derivation; import it.
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: T-088 is not merged, or its line shape differs from its section 4 item 1; a reader across sessions already exists; `Tree` cannot be imported from `scripts/audit/` without changing the builder (report what it needs; do not change the builder in this task); a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
