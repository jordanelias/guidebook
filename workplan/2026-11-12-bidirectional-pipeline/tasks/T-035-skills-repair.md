# T-035  Skills that describe the database that exists

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Evidence base: `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md`, as corrected by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md` (where they differ, the corrections govern). Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Three tasks of this plan were executed in scratch clones (T-006, T-008, T-010) and the defects they showed in the task files were corrected in every file by one generator; this file's own steps have not been executed by anyone. **Superseded in part by TERM-RESOLUTION-PLAN section 4 (TT-4) and section 2 (its skills rows) (2026-11-14):** the skills that rank Ideal → Best Practice → Acceptable → Minimum, that say "this guidebook recommends" or that route work through an absent skill are corrected here (section 4 item 5); the prose register's "to be + [value]" voice is held on OD-60. Its evidence command was run on 2026-11-12 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-035 |
| Title | Skills that describe the database that exists |
| Wave | 4 |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | IMP-36 in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`). Every command in this file uses `$BASE`, set by the first line of the set-up block, and never a literal `origin/main`: on a base that lacks the workplan, a diff against `origin/main` contains the whole workplan and every gate and count is about the wrong change.
- **Tasks that must be merged to the integration base first:** T-120 merged (added 2026-11-14 by the term-resolution fold: item 5's replacements point to `governance/evidence-architecture.md` §0, which T-120 writes, and both edit `skills/research-log-manager_SKILL.md`, where T-120 changes only the dead table name). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** OD-60 (the term-resolution plan's Q4: does the prose register's "to be + [value]" survive?), referred to the owner on 2026-11-14 (ledger: `grep -n -F "## Registration 2026-11-14" references/project-standards.md`). It holds only item 5's voice line, but the gate holds the task. The recommended answer, the unifier's: keep it for process prose; state values as attributed data. Run the gate before you start and again before you open the pull request; it must print `OD-60 OPEN (owner)`, else stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-60; do gate $n; done
```
  The other items rest on rulings already in the ledger.
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red (or green) before you start:** `python3 scripts/audit/skill_vocabulary_audit.py` exits 1. (`AT-` numbers are the acceptance tests of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §4, §7 and §9 and of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`; the test this task must turn is restated in full in section 6, so you do not need to open either.)
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-035-skills-repair "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-035" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.

## 3. The problem, in the guidebook's terms

Research is run to procedures that name tables, columns and identity codes that no longer exist.

**Evidence command** (run from the repository root, after the set-up block so that `$SCRATCH` exists; it reads the canonical database read-only or works on a copy):

```
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/audit/skill_vocabulary_audit.py | tail -3
```

**Expected output today:** FAIL, naming the tokens and files.

If the output differs, the ground has moved: stop (section 9). Ids that appear in this command are probes read on 2026-11-12; where the command derives an id by query, that is deliberate, and a test you write must do the same (section 6).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. For each token the audit names: correct the sentence to the live name, or delete the sentence if the thing is gone. Do not add a name to make the audit pass. (Item 5 below, added 2026-11-14, corrects senses, not tokens.) Add the missing frontmatter `description:` line to the four unlinked skill files only if the owner or the Fable agent supplies the sentence (a wrong description fires the skill on the wrong work).

**Added 2026-11-13 by the fold of the Edmonton case study** (`scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md`, proposals P2 and P4, reconciliations R8 and R13). Three conventions of judgment, stated once in the skill and in the two help strings that state the opposite. They are prose: no code, no refusal. Copy each text exactly.

2. **Floor and above the floor (P2; the owner's Q1 of 2026-11-13, `grep -n -F 'Owner statements 2026-11-13 (eleventh set)' references/project-standards.md`).** In `skills/run-pipeline_SKILL.md` section "4. judgment", after the bullet that begins `- Failure, harm and inadequacy (R7)`, add the bullet:
   > - **A source's own "code" marking is root attribution, not a property of the figure.** A figure the source attributes to a code ("Code (required)", "per the building code") is recorded with `--root-type committee_assertion --root-ref-id <the code's ref_id>` when the code is held, else `--root-type untraced` with `--root-classification-basis` quoting the marking (precedent: extractions 57 and 64); it is presumed to echo the code and supplies no independent root (OR-19). The source's own pairing of a higher figure with the code figure beside it is an `extraction_relations` edge written with `relate-extraction`, never a label. Whether a figure is a floor or above it is derived against the regulatory stratum of the same parameter and jurisdiction, never typed; and no input row is stored as "best practice": best practice is the determination's output, the most accommodating value in the parameter's direction (`grep -n -F 'best practice = the best way to do something' references/project-standards.md`).
3. **The comparator (R8).** In the same section, replace the parenthesis `` `--comparator` for a numerical figure, `=` for a point) `` by `` `--comparator` for a numerical figure: `=` only where the source states an exact value; a figure the source frames as "should be", "preferred" or "recommended" is the bound that framing gives (a floor `>=` or a ceiling `<=`), with the source's words as the warrant in the row) ``. In `scripts/db.py`, the `--comparator` help of `add-extraction` (`grep -n -A5 'p_ax.add_argument("--comparator"' scripts/db.py`) says `'=' for a point`: make it `'=' only for an exact stated value; a "should", "preferred" or "recommended" figure is a bound`. The engine reads `=` as floor and ceiling at once (`grep -n 'def bound_on_scale' -A30 scripts/dbcore.py`), so a "should be 1100" stored as `=` composes as a ceiling.
4. **The lens warrant (R13).** In the same section, after the words `name the group) are required;` (`grep -n -F 'name the group) are required;' skills/run-pipeline_SKILL.md`; the sentence spans two lines), add: `The words are the figure's own item's, or the basis is \`heading\` with the heading's words; a preamble or general statement of the document warrants only the quantities it names, never every figure of the document.` In `scripts/db.py`, the `--lens-basis-text` help (`grep -n -A3 'add_argument("--lens-basis-text"' scripts/db.py`) gains the same sentence after its first. **Chosen (fold 2026-11-13):** a convention, no code; the judge is the gate and the warrant is auditable (ADJUDICATION R13). Rejected: a writer refusal on the warrant's place in the file (the writer cannot tell a preamble from an item's own words without a clause inventory, T-031).

**Added 2026-11-14 by the fold of the term-resolution plan** (TERM-RESOLUTION-PLAN §4 TT-4 and the skills rows of its §2; the owner's rulings of 2026-11-14: best, ideal and most accommodating are one quantity; "acceptable isn't relevant as that's a value judgment"; "we gather and show"; the project "does not claim with own authority"). Each replacement is a pointer to `governance/evidence-architecture.md` §0 or a short phrase in the owner's words; locate each passage by its text, the plan's line numbers drift.

5. **The skills rows.**
   - `skills/prose-style-checker_SKILL.md`: the four-rung ladder (Ideal → Best Practice → Acceptable → Minimum, in its description and body: `grep -n -i -E 'Ideal|Acceptable|Minimum' skills/prose-style-checker_SKILL.md`) becomes the values in the parameter's direction order, each cited, with no "acceptable" rung. **The "to be + [value]" voice (the register's subjunctive) is changed only as OD-60's answer says** (recommended: kept for process prose, values stated as attributed data).
   - `skills/voice-style_SKILL.md`: remove "this guidebook recommends", "treats X as mandatory" and the "Population-Mode default: 33 mm" line; the line the plan calls 215 must not keep "recommended"; **re-read each line the plan lists as unflagged** (its 209, 210, 212, 218, 236, 237, 239, 251, 256 and 328, by text) and correct only those that state a design verdict on the project's own authority.
   - `skills/research-log-manager_SKILL.md`: remove the "BPC governs" sentences and the flows that feed `item-specification-writer` (that skill is absent: `ls skills | grep -c item-specification` prints 0); this is also the plan's delete-list item for this file.
   - `skills/supersession-audit_SKILL.md`: its passage resting on DR-2026-05-24 points to the ledger entry that supersedes that record (T-119's unification entry: `grep -n -F 'Unification 2026-11-14' references/project-standards.md`).
   After item 5: `git grep -n -i -E 'Ideal → Best Practice|this guidebook recommends|\bacceptable\b' -- skills` lists only lines that state no value tier (list each remaining hit in the pull request).

For items 2 to 4, the prose callers are `skills/run-pipeline_SKILL.md` and the two `add-extraction --help` strings in `scripts/db.py`; sweep `'=' for a point`, `for a point`, `lens-basis-text` and `best practice` (section 5) and correct any other sentence that states the opposite.

**What reads what this task adds or changes:** Every research session; items 2 to 4 are read by every judging session, by `v_value_independence` and T-068 (item 2: a grey echo is not counted as independent corroboration of the code it copies), and by the engine through the rows judges write (item 3).

**Code size.** Report in the pull request the output of `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` (run it after `git add`, so new files count), and for anything added name what reads it and what existing code it replaces or makes deletable. The base is the point where your branch left `$BASE`, not `origin/main` by name.

## 5. Caller sweep

Names to sweep: `skill_vocabulary_audit`

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code that calls or imports the name; a test that exercises the behaviour you are changing, even if it asserts nothing about it; a view, trigger or index; a registry `cmd` or `basis`; a skill, command or governance sentence that states the behaviour being changed. A hit that stays true after your change is a *mention* and needs nothing. **Fixing a caller the sweep finds is in scope** (CLAUDE.md rule 4): make the fix in this pull request and list it there.

**What the sweep leaves out, and why.** `workplan/` (plans, and the generated `workplan/pipeline-state-graph/graph.json` and `STATE-GRAPH.md`, which list every verb and are rebuilt by their builder; only `machines.yaml` there is hand-written, and it is swept); `references/project-standards.md` (the append-only ledger: a sentence there is superseded by a new entry, never edited); `scripts/migrations/` (immutable once committed); `sessions/`, `_archived/`, `audits/`, `versions/`, `dossier/`, `transcripts/`, `scratchpad/` (frozen records).

```
N='<name>'                                                 # run once per name
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'                    # code, tests, skills, agents, commands, hooks, workflows
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"   # views, triggers, indexes
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"   # the check registry
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'   # prose and hand-written needles
```
If this task adds, renames or removes a verb, a table, a view or the text of a refusal, also run `python3 workplan/pipeline-state-graph/build_graph.py --check` (it writes nothing) before your change and after it, and report the difference. It is red on the base: its failure count there is the base state, not yours; only a count above your before-run is yours. An object that returns 0 rows is unproven, not clean.

**Hits when this file was written** (2026-11-12, the two `git grep` lines above with `-l`; re-run them, a new file in your output is a hit to judge):

- `skill_vocabulary_audit`: code and skills: `scripts/audit/skill_vocabulary_audit.py`, `scripts/tests/test_run_pipeline_refusals.py`. Prose: `governance/check-registry.yaml`, `governance/context-map.yaml`.

Every test file in that list is run before and after the change (section 6): a test that calls what you change is a caller even when it asserts nothing about it.

## 6. Verification

**Step 1, before any edit: the before-run.** These registered checks read what this task touches: `skill_vocabulary_audit`, `claude_skills_loadable`. Run each as the registry runs it and keep the output. The command reads each check's `cmd` from the registry, so a renamed script is still found:

```
CHECKS="skill_vocabulary_audit claude_skills_loadable"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```

Each line shows the check's subject (`EXAMINED:`). A check that is red here was red before you touched anything (on 2026-11-12 `test_scan_contract` failed two cases, G01 and G02, and `retired_vocabulary` reported occurrences): record it and carry on. A check that prints no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so in the pull request.

**Step 2: red before, green after.** Exit 1 before, 0 after, with `EXAMINED:` above 0. For items 2 to 4: `grep -c -F "'=' for a point" scripts/db.py; grep -c -F '`=` for a point' skills/run-pipeline_SKILL.md; grep -c -F 'is root attribution, not a property of the figure' skills/run-pipeline_SKILL.md; grep -c -F 'warrants only the quantities it names' skills/run-pipeline_SKILL.md scripts/db.py` prints `1 1 0 0 0` before and `0 0 1 1 1` after; `python3 scripts/db.py add-extraction --help` still runs (`claude_skills_loadable` is the skill's loader check). For item 5: `git grep -c -F 'Ideal → Best Practice' -- skills/prose-style-checker_SKILL.md; git grep -c -F 'this guidebook recommends' -- skills/voice-style_SKILL.md; git grep -c -F 'item-specification-writer' -- skills/research-log-manager_SKILL.md` each prints a count above 0 before and 0 after.

**Writing the test.** Take case ids that cannot collide: prefix them with this task's number (`T035-01`, `T035-02`, …) and confirm the prefix is free first (`grep -c '"T035-' <the test file>` prints 0). Never type into a test an id, a code or a count the database can derive: choose every probe by query (for example the first term of a domain that is not yet a parameter, is not declined in `parameter_declinations` with `revoked_at IS NULL`, and whose name carries no digit). A probe for "the legitimate case still works" must be one that no *other* refusal stops, or it fails for the wrong reason. Where the live data offers no such row, build it on the test's own scratch copy or print the file's `SKIPPED-NO-FIXTURE` line, as the file's existing cases do. A new test must be able to fail: show it red on the unchanged code, or on a seeded defect that you then remove.

**Fixtures.** Anything a test or probe writes goes to a copy, is labelled `TASK-FIXTURE`, and never reaches `data/guidebook.db`.

**Step 3, after the change: the after-run.** The same loop with `after-` in place of `before-`. Then compare, check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; the `EXAMINED:` number may only change by the cases you added.

**Step 4: the gate, once.**

```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **The gate takes several minutes.** Run it in the background with a long timeout and read `$SCRATCH/gate.txt` when it ends; do not re-run it because the first call timed out.
- **`research_tooling_separation` reads `origin/main`, not `$BASE`** (its registered `cmd` takes no `--base`), so on any other base it can FAIL on paths you never touched (pilots saw far more paths than their diff touched). Run it once by hand with the base: `python3 scripts/audit/research_tooling_separation.py --base "$BASE"`, report that result, and treat a gate FAIL that disappears with `--base` as not yours.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

**The canonical database must not move:** `sha256sum data/guidebook.db` gives the value recorded in section 2.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: correct skill vocabulary to the live schema [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author a specification row (`specifications`, read through `v_best_practice`; CLAUDE.md §6's `best_practice_synthesis` names a table not in the schema: superseded in part by TERM-RESOLUTION-PLAN §2, 2026-11-14) or any synthesis prose. A Sonnet-class model is below that floor.
- Do not treat any `[A-Z]-NN` code (old item codes met in `references/`, `working/`) as a container, an example or a name.
- Do not put research rows (`scripts/migrations/data_*`, new evidence, extractions, determinations) in a tooling pull request, or tooling in a research one (CLAUDE.md rule 10).
- Do not push to `main`, rebase, or force-push. Do not subscribe to pull-request activity or schedule check-ins.
- Do not hand-type a count into any file or message; write the command that computes it. Do not type into a test an id, a code or a count the database can derive.
- Do not add a table, column, check, verb or script that section 4 does not name. If one seems needed, stop and report. **This does not forbid fixing a caller:** a test fixture, a comment, a skill sentence or a help string that the sweep of section 5 shows is made false or red by your change is in scope, is fixed in this pull request, and is listed there.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level to make something pass.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, what you saw, what you expected) when any of these happens:
- a precondition in section 2 is not met, or an owner decision named there is unanswered or answered in another form;
- the evidence command in section 3 does not give today's expected output (the defect may already be fixed, or the ground has moved);
- the red test is not red before the change, or is not green after it, after one honest attempt;
- the sweep of section 5 finds a caller (as defined there) that you cannot repair without adding something section 4 does not name. A caller you can repair is repaired and listed; a mention is left;
- a check or test that was green in the before-run is red in the after-run, at any level (the test files are registered as advisory, so the gate will not stop you: the before-and-after comparison is what does);
- `sha256sum data/guidebook.db` changes when this task has no migration, or the rebuild does not reproduce the database when it has one;
- you would have to guess a value, a vocabulary term, a name or an owner's intent (OD-60's gate prints CLOSED: stop);
- A skill's procedure, not only its vocabulary, presupposes a deleted structure: report it; rewriting a procedure is not this task.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
