# T-121  The frozen best-practices compendium leaves agent search (`.ignore`), on the owner's answer

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/TERM-RESOLUTION-PLAN.md` section 6, Q5 (folded 2026-11-14 as OD-61; the plan names no task for it, and putting it in T-120 would have held that task, which the plan says can ship now). Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the fold of the term-resolution plan. **Held on OD-61** (referred to the owner). Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-121 |
| Title | The frozen best-practices compendium leaves agent search (`.ignore`), on the owner's answer |
| Wave | 0 (now, once answered) |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (one line of search configuration and one CLAUDE.md trap line; no code, no research rows) |
| Executor | Sonnet-class |
| Traces to | TERM-RESOLUTION-PLAN §6 Q5; `decisions/DR-2026-08-06-cold-storage-search-scope.md` (the record that makes `.ignore` the owner's) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** OD-61 (the term-resolution plan's Q5: add `references/bpc/` to `.ignore`?), referred to the owner (ledger: `grep -n -F "## Registration 2026-11-14" references/project-standards.md`). Build only on an answer of yes; on no, the task is declined (report so). Run the gate before you start and again before you open the pull request; it must print `OD-61 OPEN (owner)`, else stop (section 9):
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-61; do gate $n; done
```
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T121-01` (section 6).
- **Set-up.**

```
cd /home/user/guidebook
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-121-ignore-frozen-bpc "$BASE"         # real execution only
sha256sum data/guidebook.db
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-121" && mkdir -p "$SCRATCH"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

The best-practices compendium under `references/bpc/` is frozen and quarantined (DR-2026-08-19 §1.4), and every record in it uses "best practice" in senses the owner has since ruled out; agent search returns it first for that phrase, so a session reads the old sense as current.

**Evidence commands** (read-only):

```
grep -n -E '^references/bpc' .ignore; git grep -l -i 'best practice' -- references/bpc | wc -l; git grep -l -F 'references/bpc' -- scripts skills .claude .github | head
```

**Output on 2026-11-14:** no `.ignore` line for it; a count of files (re-run); the readers in code, if any (none of them reads `.ignore`: the file's own header says Python tooling ignores it). If `.ignore` already has the line, stop (section 9).

## 4. The change

1. **`.ignore`**: add `references/bpc/` in the section for frozen records, with a one-line comment naming OD-61's answer and DR-2026-08-06.
2. **`CLAUDE.md` §7**, the `.ignore` trap line: add `references/bpc/` to its list of hidden paths (a prose caller of the list).

**What reads what this task changes:** ripgrep and the Grep tool (nothing in `scripts/` reads `.ignore`). **What wrong thing reaches the guidebook without it:** a session that searches "best practice" copies a superseded sense from a frozen record. **What it makes deletable:** nothing.

## 5. Caller sweep

Names to sweep: `.ignore` (prose callers that list its paths).
```
git grep -n -F -e '.ignore' -- CLAUDE.md governance .claude skills decisions/DR-2026-08-06-cold-storage-search-scope.md
```

## 6. Verification

**Step 2: red before, green after.** `T121-01`: `grep -c -E '^references/bpc' .ignore` prints 0 before and 1 after; `git grep -l -i 'best practice' -- references/bpc | wc -l` is unchanged (git still sees the files); `claude_md_spine` stays green.
**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: frozen BPC corpus leaves agent search (OD-61) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: OD-61's answer and its ledger line; the two edits>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not build this while section 2's gate prints CLOSED. Do not move, delete or edit any file under `references/bpc/`. Do not add any other path to `.ignore`.
- Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the gate prints CLOSED, or the owner answered no (the task is declined); `.ignore` already lists the path; `claude_md_spine` goes red.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
