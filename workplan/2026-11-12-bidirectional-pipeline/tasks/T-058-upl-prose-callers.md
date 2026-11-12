# T-058  UPL reinstated for upper limb: the retired crosswalk and the prose that names LMB or UPL

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-12 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Written in the OI-13 fold of 2026-11-12, from the owner's eighth and ninth sets. This file's own steps have not been executed by anyone. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-058 |
| Title | UPL reinstated for upper limb: the retired crosswalk and the prose that names LMB or UPL |
| Wave | 3 |
| Layer (CLAUDE.md §3) | 0-1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: governance and skill prose; no rows) |
| Executor | Sonnet-class |
| Traces to | OI-13 (owner, 2026-11-12, eighth set: "LMB should be UPL for upper limb then", "and that doesnt concern mobility"; ninth set: `LLD` is the lower-limb child of `MOB`) |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from (see `REMEDIATION-WORKPLAN.md` §2 step 0 and `OPEN-ITEMS-PLAN.md` OI-02 for how `$BASE` is chosen).
- **Tasks that must be merged to the integration base first:** T-116 merged (the prose must not say `UPL` is live before the row exists). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F "<that task's commit subject>"`.
- **Owner decisions:** none outstanding. The owner's answers are in the ledger (`grep -n -E "Owner clarification 2026-11-12 \((eighth|ninth) set\)" references/project-standards.md`); OI-13 is an open item of `OPEN-ITEMS-PLAN.md`, not a register decision.
- **Tests that must be red (or green) before you start:** the record of the 2026-07-23 crosswalk still says `UPL` is retired to `LMB`, with no mark.
- **Set-up.**

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
BASE=$(git cat-file -e origin/main:workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md 2>/dev/null && echo origin/main || echo origin/ccr-408aaa9b-z3e4s0); echo "BASE=$BASE"
git switch -c task/t-058-upl-prose-callers "$BASE"                               # real execution only; never commit on main (see below for a pilot)
sha256sum data/guidebook.db                                # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-058" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
```
- **Shell variables do not survive from one tool call to the next in this harness.** Begin every later command block with the `BASE=…` line and the `export SCRATCH=…` line above (both are fixed, so repeating them is safe), and pass `GUIDEBOOK_DB_PATH` inline on each `db.py` call as shown.
- **Real execution** (the working repository, a pull request intended): run `/session-open` before the first command, so the command log lands in this task's own session folder (CLAUDE.md §7), and create the branch as shown.
- **Pilot or dry run** (a scratch clone, no pull request): do not run `/session-open`, do not touch `scratchpad/CURRENT`, stay on the branch you were given instead of `git switch -c`, and stop after section 7 (no push, no pull request, no `/batch-done`). Say in your report that it was a pilot.


## 3. The problem, in the guidebook's terms

`UPL` was retired in favour of `LMB` by DR-2026-07-23 (its crosswalk "UPL→LMB"), and governance prose still records `UPL` as a retired token and, in older text, as a sub-code of mobility (`MOB/UPL`). The owner has reversed that: `UPL` is the upper-limb identity and "doesnt concern mobility". A reader who meets the old crosswalk or `MOB/UPL` is told the opposite of the ruling.

**Evidence command** (read-only):

```
grep -n -F "UPL→LMB" decisions/DR-2026-07-23-population-schema-replace.md
grep -n -E "UPL->LMB|tokens: \[VIS, UPL" governance/retired-vocabulary.yaml
git grep -n -E "(^|[^[:alnum:]_-])(UPL|LMB)([^[:alnum:]_-]|$)" -- governance architecture skills scripts schemas ':!scripts/migrations'
```

**Expected output today:** the DR line; the retired-vocabulary token list and crosswalk; hits in `governance/population-taxonomy.md` (crosswalk line and `MOB/UPL`), `governance/functional-taxonomy.md` (`MOB/UPL` rows), `governance/co1-operational.md`, `governance/mission-PROVISIONAL.md`, `governance/retired-vocabulary.yaml`, and one refusal message in `scripts/db.py` that lists `UPL` among retired codes.

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **The DR's crosswalk, marked by rule 0's back-pointer.** Append to `references/project-standards.md` one entry with the pair
   ```
   SUPERSEDES: decisions/DR-2026-07-23-population-schema-replace.md :: "UPL→LMB"
     BY: references/project-standards.md :: "LMB should be UPL for upper limb then"
   ```
   and add, in the DR's crosswalk paragraph or the one directly after it, one marker line naming SUPERSEDED and carrying the BY quote verbatim. Check both quotes occur exactly once under the audit's own normalisation, not with `grep -c` (from the repository root: `python3 -I -c "import sys;sys.path.insert(0,'scripts');import dbcore;print(dbcore.count_ledger_quote(open('decisions/DR-2026-07-23-population-schema-replace.md').read(),'UPL→LMB'))"`, which printed 1 on 2026-11-12, and the BY quote with `dbcore.strip_supersedes_citations` on the ledger); if the target quote is not unique, lengthen it within its sentence. Editing `decisions/` needs `attestations/<slug>.json` (CLAUDE.md rule 2). Run `python3 scripts/audit/supersession_backpointer_audit.py` before and after: one more examined, no failure.
2. **`governance/retired-vocabulary.yaml`, edited as text, never through a YAML writer** (its own warning). Remove `UPL` from that entry's `tokens` list and from the residue `grep` in its note; append to its note one dated line: `UPL` reinstated by the owner on 2026-11-12 (eighth set) for upper limb, outside mobility; `LMB` retired to it by T-116. Add `LMB` nowhere (it is retired in the database, where the writers refuse it).
3. **Prose callers.** In `governance/population-taxonomy.md` and `governance/functional-taxonomy.md`, add one pointer line beside the crosswalk and beside each `MOB/UPL` row: superseded on 2026-11-12, `UPL` is upper limb and outside mobility, the lower-limb child of `MOB` is `LLD`; change nothing else (taxonomy is the owner's). `governance/co1-operational.md` and `governance/mission-PROVISIONAL.md` name `UPL` as a population: correct now, leave them. The refusal message in `scripts/db.py` that lists `UPL` among retired codes: remove `UPL` from that list (locate by the string, not the line).
4. **Skills.** `git grep -n -E "(^|[^[:alnum:]_-])(UPL|LMB)([^[:alnum:]_-]|$)" -- skills`: a skill that scopes to `LMB` is pointed at `UPL`; one that places `UPL` under mobility is corrected. The research corpus under `references/` (for example `references/bpc/population-general/upper-limb-impairment-built-environment.md`, `references/bpc/MOB.md`) is prior-version content: list the files, edit none (a corpus sweep is a content migration the owner scopes, `governance/retired-vocabulary.yaml`'s own precondition).

**What reads what this task adds or changes:** sessions reading governance and skills; `supersession_backpointer_audit`; the refusal message's readers.

## 5. Caller sweep

The evidence command's third line is the sweep. A hit is a caller when its truth changes with the eighth set (it says `UPL` is retired, or under mobility, or that `LMB` is the upper-limb code); a mention that stays true is left. `references/project-standards.md`, `sessions/`, `_archived/` and committed migrations are records and are never edited.

## 6. Verification

**Red before, green after.** Before: the audit examines no pair for the DR's crosswalk, and the retired list holds `UPL`. After: `python3 scripts/audit/supersession_backpointer_audit.py` passes with one more `EXAMINED`; `grep -c -E "tokens: \[VIS, UPL" governance/retired-vocabulary.yaml` prints 0; the sweep prints no caller left unmarked.

**Step 4: the gate, once.**

```
BASE=$(git cat-file -e origin/main:workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md 2>/dev/null && echo origin/main || echo origin/ccr-408aaa9b-z3e4s0)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
- **Run it once, when every edit is made, before the commit.** It compares your working tree (committed or not, untracked files included) with the point where your branch left `$BASE`, so it does not need a commit first. `preflight.sh` runs the registry selftest and then `run_checks.py --changed-from`: do not run `run_checks.py` separately on the same diff, and never `--all`. Re-run it only if you change a file afterwards.
- **A passing check prints no `EXAMINED:` line in this output.** The subject of each check is read in the per-check runs above (`$SCRATCH/after-<check>.txt`), not here. In `gate.txt` read three things: the `RESULT` line; any check under `NOTHING-IN-SCOPE` (it has not passed: say so); any blocking `FAIL`.
- **A check that was already red before your change** (the before-run shows it) tells you nothing about your diff: name it in the pull request with its before and after lines, and move on.

## 7. Commit

Commit **after** the gate of section 6 is clean.
```
git add -A . ':!transcripts' ':!*commands.jsonl'      # add the two append-only logs only at a natural break (CLAUDE.md rule 6)
git commit -m "governance: UPL reinstated for upper limb; the retired crosswalk and prose callers marked [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence commands and their output, the callers the sweep found and what was done to each>" -m "<the attribution trailers your own session instructions give: a Co-Authored-By line and a Claude-Session line>"
```
The format is `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last, taken from `date -u`. Do not copy trailers from this file; use the ones your session was given.

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly, with SQL, Python or any tool. Only `scripts/migrate_db.py` changes it.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`.
- Do not decide doctrine: mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing, trajectory. If the task seems to need such a decision, stop.
- Do not author `best_practice_synthesis` or any synthesis prose. A Sonnet-class model is below that floor.
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
- you would have to guess a value, a vocabulary term, a name or an owner's intent.

## 10. Rollback

Before merge: close the pull request and delete the branch; nothing else has changed. After merge: `git revert <merge commit>` in a new pull request. A migration that has been committed is never edited or deleted: fix forward with a compensating migration (CLAUDE.md rule 3). Never rewrite history.

## 11. Adversarial pass and pull request

Real execution only; a pilot stops after section 7.
1. Run `/adversarial` once on the finished diff (a read-only critic attacks the claim, then you repair). One pass; no pass on the pass. For a research task the pass is recorded in the database with `db.py record-adversarial-pass` and closed with `close-adversarial-pass`.
2. Run `/batch-done`; it is the only definition of finished.
3. Push the branch. Open the pull request **last**, once, against the integration base (section 2). Title = the commit subject. Body: the problem; the evidence before and after; each caller the sweep found and what was done to it; each check you ran with its `EXAMINED:` line, before and after; the code-size line; what was not verified. End the body with the pull-request attribution line your session instructions give.
4. Immediately after creating the pull request call `unsubscribe_pr_activity` for it (creating a pull request subscribes the session by itself). Do not watch it, do not poll, do not schedule a reminder. Push nothing afterwards except a deliberate change; the final push is never `[skip ci]`.
5. One pull request merges at a time. If another task's pull request merged while you worked, take it with `git merge "$BASE"` after `git fetch origin` (never rebase) and, if you carry a schema migration, derive its number again by the rule in section 4.
