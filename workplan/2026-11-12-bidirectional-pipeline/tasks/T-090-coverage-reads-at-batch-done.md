# T-090  Every research batch reports which groups the catalogue can speak about

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: the adjudication of the Edmonton digest, section 3 ("What surfaces this mechanically") and proposal P5 (`scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md`); the owner's instruction that the case study serve "disability coverage" (`HANDOFF-TO-FABLE.md` section 2's instruction, recorded in `grep -n -F 'Owner statements 2026-11-13 (eleventh set)' references/project-standards.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 by the fold of the Edmonton case study; the three queries were run on a scratch copy that day. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-090 |
| Title | Every research batch reports which groups the catalogue can speak about |
| Wave | 2 |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | ADJUDICATION section 3 and P5; CLAUDE.md §6 ("Work from the ICF/access-need frame with codes AND names, never bare axis codes, never population umbrellas") |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** none. The reads count rows; they decide nothing about who a figure is for.
- **Tests that must be red before you start:** `grep -c -F 'COVERAGE' .claude/commands/batch-done.md` prints 0.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-090-coverage-reads-at-batch-done "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task has no migration
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-090" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

A batch can read a document whose provisions are for blind, Deaf, cognitive and fatigue-limited people and still write only mobility figures, because those are the quantities the catalogue holds; the rest stays as observations. Nothing in the batch's report says so. A book whose parameters are mobility quantities would then present itself as covering disabled people. The adjudication showed this on the Edmonton checklist and named three reads, derived from the pipeline's own rows, that make it visible (ADJUDICATION section 3).

**Evidence commands** (read-only, on `$SCRATCH/t.db`): the three reads of section 4 item 1, saved by the executor to `$SCRATCH/coverage.py` and run as `python3 -I "$SCRATCH/coverage.py" "$SCRATCH/t.db"`.

**Output on 2026-11-13** (on a scratch copy of the canonical database; re-run, do not trust): (1) lens by parameter, live value-supplying figures per (lens code, active parameter): every ICF code and every access-need code is zero against every parameter, and most identity codes are; (2) of the value-supplying figures with a live link, every one has an identity link and none an ICF or access-need link, and some carry only `ALL` or a parent code; (3) observations whose latest adjudication is `DEFERRED`, `NOT-OURS` or absent, by source, are listed for several sources. If the reads already appear in `/batch-done`, stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8. **Convention first** (the adjudication's own order): three queries printed by `/batch-done`, read by the owner at the pull request. No view: none is added until T-034 (`cell-status`) or the renderer's Gaps section reads one (`v_coverage_lens` exists and counts searches, a different thing: `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select sql from sqlite_master where name='v_coverage_lens'\").fetchone()[0][:200])"`).

1. **In `.claude/commands/batch-done.md`**, after the gate lines, a block headed `COVERAGE (read it; it does not fail)` that runs, read-only against the database the batch used (`GUIDEBOOK_DB_PATH`, else `data/guidebook.db`), a Python heredoc printing three reads:
   - **(1) Lens by parameter.** For every active code of each lens registry (`base_taxonomy_identity where status='active'`, `access_needs`, `base_icf`, `base_taxonomy_medical`) crossed with every active parameter (`base_parameters where status='active'`), the count of distinct live value-supplying figures (`figure_role in ('claim','derived')`) linked to it in `v_live_lens_links`, zeros included. Print, per lens model, the codes whose count is zero against every parameter (a group the catalogue cannot speak about), and the non-zero cells.
   - **(2) Lens by figure.** The value-supplying figures with a live link whose links are identity only; and those whose only identity links are `ALL` or a code that is some active code's `parent_code` (a figure filed to an umbrella).
   - **(3) Group words with no parameter.** Per source admitted or read by this batch (and, with `--all`, every source), the observations whose latest adjudication (`max(adjudication_id)` per observation) is `DEFERRED`, `NOT-OURS`, or none, with their surface form and locator.
   Every count is printed with the query beside it in the block's own text; no number is typed.
   **Chosen (authoring 2026-11-13):** printed, not failed. Rejected: a gate that fails on a zero row (zero is the honest state of most of the catalogue today, and a check red by construction teaches its reader to ignore it: CLAUDE.md rule 6's argument). **Chosen:** in `/batch-done`, not in `research_batch_dod.py` (that script is a gate; these reads are for the owner's reading of the pull request).
2. **The research batch's pull request quotes the three reads.** One sentence under the block: "Quote the three reads in the pull request body; the owner reads coverage there (OR-17's 'with me reading the PR')."
3. When T-029 has merged, a fourth read (elements, that is declined terms, with no `element has parameter` pointer) is added by T-029's executor or a later task; not here.

**What reads what this task adds:** the owner at each research pull request; T-110, before the first live determinations, which should quote read (1) (a correction owed to T-110's file, recorded in `OPEN-ITEMS-PLAN.md` OI-57); T-034 and the renderer when they want a view. **What wrong thing reaches the guidebook without it:** a book whose determinations are all mobility quantities, presented as covering disabled people, with nothing in any batch's record saying which groups it could not hold. **What it makes deletable:** nothing.

**Code size.** This task changes no file under `scripts/`, `schemas/`, `.github/` or `skills/`; report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- .claude/commands/batch-done.md`.

## 5. Caller sweep

Names to sweep: `batch-done`, `v_coverage_lens`, `COVERAGE`.

**What a caller is.** A hit whose behaviour or truth changes: a sentence that says what `/batch-done` runs or prints (`.claude/commands/`, `skills/`, `CLAUDE.md`), a test that reads the command file. Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills CLAUDE.md governance ':(exclude)scripts/migrations'
```

## 6. Verification

**Step 1: before.** `claude_skills_loadable` (it reads `.claude/`): run it as the registry runs it and keep the output.
```
c=claude_skills_loadable; cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$?"
```
**Step 2: red before, green after.** Before: section 2's `grep -c` prints 0. After: the block runs as written from the command file (copy it out with `sed -n '/COVERAGE/,/^PY$/p'`) against `$SCRATCH/t.db` and prints the three reads, each with its query; then run it against a copy on which one figure has been given an ICF link with `db.py add-lens-link --icf <the first ICF code by query> --basis named_in_text --basis-text <words chosen by query from that figure's claim_text>` (`TASK-FIXTURE` session): read (1) shows that code non-zero for that figure's parameter and read (2) no longer lists the figure as identity-only.
**Seeded defect:** drop the `figure_role` filter from read (1); a `finding` row's link then counts (show the count moves); restore.
**Step 3: after.** The same `claude_skills_loadable` run; nothing new may fail.
**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
`sha256sum data/guidebook.db` must not move.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: every research batch prints which groups the catalogue can speak about [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the three reads, their output before and after the fixture; callers>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not add a view, a check or a gate; do not make the block fail.
- Do not type a code list (every code set is read from its registry), a count or a threshold.
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the reads already appear in `/batch-done`; a registry table or `v_live_lens_links` is missing or renamed (report the live name); a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
