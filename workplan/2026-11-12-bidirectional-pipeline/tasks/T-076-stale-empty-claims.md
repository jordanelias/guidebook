# T-076  Sentences and suppressions that call a populated table empty

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source of the item: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 ("prose that calls `lang_jur_map` empty"), first reported by the T-025 task file (`grep -n 'False today, and not this task' workplan/2026-11-12-bidirectional-pipeline/tasks/T-025-base-writers.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13; its evidence commands were run on 2026-11-13 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-076 |
| Title | Sentences and suppressions that call a populated table empty |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 0-1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | OI-56; CLAUDE.md rule 7a ("a PROSE CALLER restating a checked fact" has no gate) and rule 0 (record the supersession) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from: `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it). Never use a literal `origin/main` in a command of this file.
- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** none. The supersession this task records is the owner's: D-0152, "Ratify all", 2026-07-24 (`grep -n -F 'RATIFIED — owner directive 2026-07-24' decisions/DR-2026-07-24-lang-jur-map-roles.md`), which adopted the PRIMARY/SECONDARY definitions and populated the map. This task changes no doctrine; it points two doctrine sentences at the ruling that superseded them.
- **Tests that must be red (or green) before you start:** none.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-076-stale-empty-claims "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-076" && mkdir -p "$SCRATCH"
```
- **Shell variables do not survive between tool calls.** Begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines.
- **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

Two ratified doctrine documents tell a reader that the language-and-jurisdiction map is empty, waiting for criteria. It is populated, under criteria the owner ratified. A session that reads them plans research as if the scope of languages per jurisdiction were undecided. Two suppressions in the structural audit's known-debt file are past their own lift condition: they say the debt is resolved and still sit in the file.

**Evidence commands** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print('lang_jur_map rows', c.execute('select count(*) from lang_jur_map').fetchone()[0])"
grep -n 'lang_jur_map. remains empty' governance/functional-taxonomy.md
grep -n 'population \*\*deferred' governance/held-tensions.md
python3 - <<'PY'
import yaml,sqlite3
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for e in yaml.safe_load(open('scripts/audit/graph/known_debt.yaml'))['entries']:
    n=c.execute(e['lift_when_sql']).fetchone()[0]
    print(e['id'], n, '>=', e['lift_when_ge'], 'STALE' if n>=e['lift_when_ge'] else 'live')
PY
git grep -n -i -E 'lang_jur_map|lang-jur-map' -- governance architecture references CLAUDE.md skills .claude scripts/audit/graph working ':(exclude)references/project-standards.md' ':(exclude)references/search-log' ':(exclude)governance/context-map.yaml' | grep -i -E 'empty|defer|unpopulated|0 rows|no rows|pending'
```

**Output on 2026-11-13:** `lang_jur_map rows 70`; `governance/functional-taxonomy.md:390`; `governance/held-tensions.md:100`; known-debt: `c1-source-value-extractions-empty 214 >= 1 STALE`, `c1-evidence-cell-state-pilot-only 8 >= 20 live`, `conflicts-empty-awaiting-migration 0 >= 1 live`, `lang-jur-map-deferred 70 >= 1 STALE`; the last grep prints the two doctrine lines and the two `known_debt.yaml` lines of the `lang-jur-map-deferred` entry. `python3 scripts/audit/graph_audit.py` already prints a `known_debt.stale` WARN telling the reader to remove a satisfied entry (`grep -n 'remove it from known_debt.yaml' scripts/audit/graph_audit.py`).

The decision records (`decisions/DR-2026-06-11-remove-colonial-role.md`, `decisions/DR-2026-07-24-search-executions-substrate.md`) also say the table is empty: they are dated records of the state on their day and are mentions, not callers; leave them.

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **`governance/functional-taxonomy.md`**: after the clause "`lang_jur_map` remains empty pending owner-defined PRIMARY/SECONDARY criteria per DR-2026-06-11 …", insert one parenthesis: "(superseded 2026-07-24: the owner ratified the role definitions and the map was populated, D-0152, `decisions/DR-2026-07-24-lang-jur-map-roles.md`; derive its size with `select count(*) from lang_jur_map`, never quote it)".
2. **`governance/held-tensions.md`**: after "`lang_jur_map` population **deferred pending owner-defined criteria** per DR-2026-06-11-remove-colonial-role", insert the same parenthesis. The sentence that follows ("classify only under ratified criteria") stays: the ratified criteria now exist, which is what it asked for.
   **Chosen (authoring 2026-11-13):** an inline supersession pointer, not a rewrite of the sentence. Rejected: rewriting the clause to state the present state (it is ratified doctrine text, and CLAUDE.md §8 reserves doctrine edits to the owner; a pointer records rule 0's supersession without restating doctrine). No number is typed: the parenthesis carries the command (rule 7a).
3. **`scripts/audit/graph/known_debt.yaml`**: delete every entry whose lift condition is satisfied on the day (evidence command, `STALE`): on 2026-11-13 that is `lang-jur-map-deferred` and `c1-source-value-extractions-empty`. **Chosen (authoring 2026-11-13):** both, not only the `lang_jur_map` one: the set is derived by the file's own rule (`lift_when_sql` ≥ `lift_when_ge`), and `graph_audit.py` already says to remove each satisfied entry; keeping one because the plan named the other would be a curated list (rule 8).

**What reads what this task changes:** a session or reader of the two doctrine documents; `scripts/audit/graph_audit.py` (reads `known_debt.yaml`; with the stale entries gone its `known_debt.stale` WARN stops).

**Code size.** No code changes. Report `git diff --shortstat "$(git merge-base HEAD "$BASE")"`.

## 5. Caller sweep

Names to sweep: `lang-jur-map-deferred`, `c1-source-value-extractions-empty`, `remains empty pending`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task (code, a test, a registry entry, a governance sentence that states the same fact). A hit that stays true is a *mention*. Fixing a caller the sweep finds is in scope (CLAUDE.md rule 4). Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `decisions/` (dated records), `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills governance architecture CLAUDE.md references ':(exclude)scripts/migrations' ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
`scripts/tests/test_graph_audit.py` may assert on the entries' ids: read every hit there; a test that names a deleted id is a caller to repair.

## 6. Verification

**Step 1, before any edit:** `python3 scripts/audit/graph_audit.py > "$SCRATCH/before-graph.txt" 2>&1; echo rc=$?; grep -E 'EXAMINED|VERDICT|stale' "$SCRATCH/before-graph.txt"` and `python3 scripts/tests/test_graph_audit.py > "$SCRATCH/before-tga.txt" 2>&1; echo rc=$?` (slow; once before, once after).

**Step 2: red before, green after.** Before: the evidence command's known-debt loop prints at least one `STALE`; after: it prints none. Before: `graph_audit.py` prints the `known_debt.stale` WARN; after: it does not, and its `EXAMINED:` number is unchanged and its `VERDICT` is unchanged. Before: both doctrine greps print a line with no pointer; after: each line is followed by the parenthesis (show `grep -n -A1`).

**Step 3: after-run.** The same two commands with `after-`. No case failing after may have passed before.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run it once, in the background. If T-075 is not yet merged, `research_tooling_separation` reads `origin/main`, not `$BASE`: run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report that result. The canonical database must not move (`sha256sum data/guidebook.db`).

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: point the empty-map sentences at D-0152 and drop satisfied debt suppressions [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the evidence before and after; the entries removed and the command that showed each satisfied>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not rewrite or delete a doctrine sentence; add the pointer only.
- Do not edit a decision record, the ledger, or a migration.
- Do not delete a known-debt entry whose lift condition is not satisfied on the day.
- Do not type the map's row count into any file.
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: an evidence command prints something section 3 does not state; a further doctrine sentence makes the same claim in a form you would have to rewrite rather than point (report it for the owner); `test_graph_audit.py` was green before and is red after and the cause is not a deleted id you can repoint; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request and delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base, with the evidence before and after; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
