# T-083  A verb sets the quantity kind and its warrant on an existing parameter

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 ("a verb to set `quantity_kind` and its observation on an existing parameter (blocks T-109)"), and T-109's own precondition (`grep -n 'A writer for the two cells on a held parameter' workplan/2026-11-12-bidirectional-pipeline/tasks/T-109-parameter-kinds-data.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 against T-020's task file and pilot patch (T-020 is not yet merged). Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-083 |
| Title | A verb sets the quantity kind and its warrant on an existing parameter |
| Wave | 1 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OI-56; T-109 (the research task that gives the live parameters their kind, which stops without this verb); OD-24 (delegated: a parameter is one measured quantity and its kind is a row of the kinds table) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-020 merged (it adds `base_parameters.quantity_kind` and `quantity_kind_observation_id`, the table `base_quantity_kinds`, and `add-parameter`'s refusals on both). Check: `python3 -I -c "import sqlite3;print([r[1] for r in sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma table_info(base_parameters)') if 'quantity_kind' in r[1]])"` prints both names.
- **Owner decisions:** none.
- **Delegated resolutions this task rests on.** OD-24 (a parameter is one measured quantity; its kind is a row of the kinds table T-020 builds), a resolution under the owner's delegation of 2026-11-12, not the owner's words, read through the ledger gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`); run it before you start and before you open the pull request; if it prints CLOSED, stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-24; do gate $n; done
```
- **Tests that must be red before you start:** none of the acceptance tests; T-109's precondition (`git grep -n -e 'quantity-kind-observation-id' -- scripts/db.py` names a verb other than `add-parameter`) is red.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-083-set-kind-on-existing-parameter "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-083" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

After T-020, a new parameter must say what kind of quantity it is (a length, a gradient, a force …) and point at the words of a source that show it; the existing parameters carry neither, and T-109 is to give them both. No verb writes the two cells on a parameter that already exists, so T-109 could only do it by hand SQL, which CLAUDE.md §4 forbids. A parameter with no kind cannot have its units checked against the right family when T-030 lands.

**Evidence commands** (on `$BASE`, after T-020 has merged; read-only):

```
git grep -n -e 'quantity-kind-observation-id' -- scripts/db.py | head
git grep -n -e 'add_parser("' -- scripts/db.py | grep -i -E 'parameter|quantity' 
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select status, count(*), sum(quantity_kind is null) from base_parameters group by 1\").fetchall())"
```

**Expected output** (on 2026-11-13 the commands could not be run: T-020 is not merged and `quantity_kind` does not exist on `HEAD`, `git grep -c 'quantity-kind-observation-id' scripts/db.py` printed 0): the flag appears only in `add-parameter`'s parser and in `insert_parameter`; the parameter verbs are `add-parameter`, `decline-parameter`, `retire-parameter`, `merge-parameter`, `annotate-parameter` and `add-quantity-kind`, none of which sets the kind on an existing row; every `active` parameter has `quantity_kind` NULL. T-020's pilot patch is no guide to the names: it predates the warrant column (`grep -c 'quantity_kind_observation' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-020.patch` printed 0; the fold added it, T-020 section 4 item 1a). Read the names from the merged code.

If the output differs (a verb already sets both), the defect is fixed: stop and report (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **One shared refusal, two callers.** Move the refusals `insert_parameter` runs on the kind and its warrant (T-020 section 4 item 1a: no kind or an unknown kind, naming every kind read from `base_quantity_kinds`; no observation id; an unknown observation id; an observation whose `context_quote` states no value) into one function in `scripts/db.py` (for example `_kind_refusal(conn, kind, observation_id)`), called by `insert_parameter` unchanged in order and message. Reuse; do not write a second copy (T-041's rule, one home for helpers).
2. **`db.py set-parameter-kind --parameter-id N --quantity-kind K --quantity-kind-observation-id O --session S [--dry-run]`** (function `set_parameter_kind`). It runs, in this order: the parameter exists and is `active` (`_parameter_row`; a retired or merged parameter is refused, naming its survivor for a merge); the shared refusal of item 1; **the kind is not already set** (write-once; the refusal names the stored kind and its observation); **no live determination and no open gate stands on the parameter** (`_refuse_live_work`, `grep -n 'def _refuse_live_work' scripts/db.py`). Then one `UPDATE` of the two columns with the `updated_*` stamp (`_updated(conn, "base_parameters", session, stamp)`, the helper `retire-parameter` uses).
   **Chosen (authoring 2026-11-13):** write-once. Rejected: an overwrite with a reason (a kind that changes under a parameter changes what every stored figure of it means; a wrong kind is a new decision recorded as such, and no such case exists yet, so the path is not built: CLAUDE.md §8, nothing is added without naming what reads it). **Chosen:** refuse while a live determination or open gate stands, as `retire-parameter` does: a determination computed before its parameter had a kind would silently gain one. No live determination exists today (`select count(*) from specifications where retired_at is null`), so the refusal changes no present act. **Chosen:** the flag spelling `--quantity-kind-observation-id`, so T-109's own precondition command finds the verb. **Chosen:** a new verb rather than a flag on `annotate-parameter` (that verb appends a dated line to `notes` and nothing else, `grep -n 'def annotate_parameter' -A8 scripts/db.py`; giving it a typed write would make one verb do two kinds of act, and its "any status" rule is wrong for a kind).
3. **No row is written by this task.** T-109 writes the kinds (research, rule 10).

**What reads what this task adds:** T-109 (its precondition, then its rows); `workplan/pipeline-state-graph/machines.yaml` if it lists the parameter verbs (the sweep says). **What it makes deletable:** nothing; it removes the only reason T-109 would reach for hand SQL.

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: `insert_parameter`, `quantity_kind`, `quantity-kind-observation-id`, `add-parameter`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code or a test that calls `insert_parameter` and asserts one of the moved refusals' messages (the move must keep them byte-identical; a test that goes red has found a changed message); a skill, command or plan sentence that says the kind can be set only when a parameter is added; a registry entry. A mention stays true. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/` except `workplan/pipeline-state-graph/machines.yaml`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task adds a verb: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference (only a failure count above the before-run is yours).

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="test_db_amend_writers test_run_pipeline_refusals test_scan_contract"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
`test_scan_contract` failed G01 and G02 on 2026-11-13: record and carry on.

**Step 2: red before, green after** (cases `T083-01`… in `scripts/tests/test_db_amend_writers.py`; prefix free: `git grep -c 'T083-' scripts/tests/`). Probes chosen by query, never typed: an active parameter with no kind (`select parameter_id from base_parameters where status='active' and quantity_kind is null order by 1 limit 1`), a kind (`select kind_id from base_quantity_kinds order by 1 limit 1`), an observation whose quote states a value (`select observation_id from observed_terms where context_quote glob '*[0-9]*' order by 1 limit 1`) and one whose quote does not (`… not glob '*[0-9]*' …`; if none exists, print `SKIPPED-NO-FIXTURE` for that case).
- `T083-01` the verb sets both cells on the probe parameter; every other column of the row is unchanged. Red before (no verb; assert stderr starts `REFUSING:` or names the verb unknown, so an absent verb cannot pass).
- `T083-02` the shared refusals, through the new verb: unknown kind (names the kinds); no observation; unknown observation (`coalesce(max(observation_id),0)+1`); an observation with no value in its quote.
- `T083-03` a second call on the same parameter is refused (write-once), naming the stored kind.
- `T083-04` a retired parameter is refused (retire one on the copy first with `retire-parameter`); a parameter with a live determination is refused (build one on the copy, labelled `TASK-FIXTURE`).
- `T083-05` `add-parameter`'s own kind refusals print the same messages as before the move (compare against the before-run of `test_run_pipeline_refusals` and `test_db_amend_writers`).
- Seeded defect: drop the write-once check; `T083-03` goes red; restore.

**Fixtures** go to a copy, are labelled `TASK-FIXTURE`, and never reach `data/guidebook.db`.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it. `sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: set the quantity kind and its warrant on an existing parameter [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: evidence before and after; the moved refusals; callers; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not set a kind on any parameter of the canonical database (T-109's).
- Do not add an overwrite path, a new kind, or a `choices=` list of kinds (argparse cannot read rows; the refusal names them).
- Do not change the text of a refusal you move.
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: T-020 is not merged; OD-24's gate prints CLOSED; a verb already sets both cells (the defect is fixed); T-020 merged with different column or flag names than this file uses (use the merged names, and report the difference); a moved refusal's message cannot stay identical; a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
