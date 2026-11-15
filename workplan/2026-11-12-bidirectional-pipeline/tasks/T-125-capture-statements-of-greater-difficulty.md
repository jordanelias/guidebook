# T-125  The judgment stage records a source's statement that disabled people struggle more at a value, in the record T-059 defines

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: finding A4.5 of the adversarial pass on the remediation plan (`scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/adj/AUDIT-FINDINGS.md`), re-verified 2026-11-14: the harm test has a record (T-059 designs it) and a reader (selection), but no session is taught to write it, so the test examines nothing. Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the repair writer of the adversarial pass. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-125 |
| Title | The judgment stage records a source's statement that disabled people struggle more at a value, in the record T-059 defines |
| Wave | 6 (after the term-resolution tooling) |
| Layer (CLAUDE.md §3) | 2 |
| Kind | **TOOLING** (skill text only; CLAUDE.md rule 10: no research rows) |
| Executor | NOT FOR SONNET: Opus-class. It writes extraction guidance that applies the owner's OD-58 standard, a reading of the owner's words |
| Traces to | OD-58 (`grep -E '^OD-58:' references/project-standards.md | tail -1`); the harm-test entry (`grep -n -F 'the most accommodating value stands unless research shows' references/project-standards.md`); research contract R7 (harm findings are first-class) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-059 and T-035 merged (T-059 designs and builds the record and its writer, item 6, and this task teaches it; T-035 rewrites the same section of `skills/run-pipeline_SKILL.md`, so it lands first and this task edits the text it leaves). Check by running, per task, `git log "$BASE" --format=%s | grep -c -E 'task/t-059-wp-t4-agreement|^T-059:|execute workplan T-059'` and the same with `t-035-skills-repair`/`T-035`, each printing at least 1.
- **Owner decisions:** none as a gate; OD-58 is answered and T-059 builds on it.
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T125-01` (section 6).
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-125-capture-statements-of-greater-difficulty "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task never moves it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-125" && mkdir -p "$SCRATCH"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

Under the owner's harm test the most accommodating value stands unless a source states that disabled people struggle more at it than at the value the source proposes (OD-58). The engine can read such a statement once T-059 builds its record; the skill that guides a judging session through extraction teaches only the outcome-shaped `harm_finding` with an `insufficient` edge, which T-059 found reads the other way. So no session records the statements, the replacement never fires, and a value a source says is worse for disabled people is shown as the best.

**Evidence commands** (read-only):

```
python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select sum(harm_finding=1) from source_value_extractions').fetchone())"
grep -n -i -E 'harm.finding|insufficient' skills/run-pipeline_SKILL.md | cut -c1-120
git grep -n -i -E '<the verb or relation T-059 added>' -- scripts/db.py skills | cut -c1-120
```

**Output on 2026-11-14:** `(0,)`; the skill's harm-finding paragraph (an outcome flag plus an `insufficient` edge); the third command, run with the name T-059's pull request gives, prints the writer and no skill line. If the third prints a skill line already, the ground has moved: stop (section 9).

## 4. The change

1. **In `skills/run-pipeline_SKILL.md`, the judgment section where extraction is taught** (locate by the harm-finding paragraph, never by line number): add one paragraph that teaches the OD-58 statement as T-059 recorded it: when a held source (a research publication or a clinical guideline; a Co-1 source on the recorder's flagged reading; never a code; never the session's own inference) states that a person with a disability struggles more, has more difficulty, or makes some negative statement about the parameter at a value compared with the value the source proposes, write the record with the verb T-059 built, quoting the source's own words, joining the two extraction rows (the value proposed, the value said to be worse) with their lens links. A statement is enough; no measured outcome is required. Point to T-059's selection rule (`tasks/T-059-wp-t4-agreement.md` section 4 item 6) and to the ledger's OD-58 line for the standard; do not restate it beyond the one sentence the session needs.
2. **Keep the outcome flag distinct.** The existing `harm_finding` paragraph stays for measured outcomes; one sentence says the two are different records and why (T-059 item 6's finding that `insufficient` reads "not enough", the opposite direction).
3. **The judging session's checklist.** Where the skill lists what a judging pass reads for (`grep -n -i 'checklist\|before you close' skills/run-pipeline_SKILL.md`), add the statement of greater difficulty as one item.

**What reads what this task adds:** every judging session that follows `/run-pipeline`; the record it teaches is read by T-059's selection. **What wrong thing reaches the guidebook without it:** a value a source says is worse for disabled people is shown as the best, because the statement that should replace it was never recorded. **What it makes deletable:** nothing.

**Code size.** No code: `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github ':!scripts/migrations'` prints nothing; the skill diff is reported.

## 5. Caller sweep

Names to sweep: the verb or relation name T-059 added, `harm_finding`, `insufficient`, across `skills/` and `.claude/commands/`; a skill that teaches extraction elsewhere and omits the statement is listed, and corrected if it is a caller.

## 6. Verification

**Step 1, the before-run.**
```
CHECKS="claude_skills_loadable skill_vocabulary_audit"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$?"; done
```
**Step 2: red before, green after.**
- `T125-01`: `git grep -c -F '<the verb or relation T-059 added>' -- skills/run-pipeline_SKILL.md` prints 0 before and at least 1 after; `grep -c -F 'OD-58' skills/run-pipeline_SKILL.md` prints at least 1 after.
- A dry run of the taught call on a scratch copy (`GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/db.py <verb> … --dry-run`), with a fixture statement, is accepted, and the same call naming a code source is refused (T-059's writer refusal); show both.
**Step 3: after-run**, as step 1 with `after-`.
**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
`sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: teach the capture of a source's statement of greater difficulty (OD-58) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the paragraph added and where; the dry runs accepted and refused; checks before and after>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not change code, schema or the writer (T-059's). Do not write research rows. Do not restate the selection rule or the OD-58 standard beyond one sentence; point to their homes.
- Do not teach a session to infer a statement from a figure's size or from a gap. Do not edit the prose register (T-035's).
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: a dependency is not merged; T-059 recorded no verb or relation for the statement (its design point unresolved); the evidence output differs; a check green before is red after.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
