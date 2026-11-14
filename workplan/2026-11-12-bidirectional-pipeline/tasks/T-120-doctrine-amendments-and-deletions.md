# T-120  Doctrine says what the owner ruled: one home for best, most common and minimum; dead names and dead copies removed; atoms re-quoted

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/TERM-RESOLUTION-PLAN.md` section 2 (the rows marked R with no task named), section 5 (the delete list), section 4 TT-5 (the state-graph edits) and section 7 step 2 (its PR-2) (folded 2026-11-14; where that plan and this file differ, that plan governs, and the ledger's owner rulings govern both). Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the fold of the term-resolution plan (its PR-2). It needs no owner answer: every amendment applies a ruling already in the ledger. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-120 |
| Title | Doctrine says what the owner ruled: one home for best, most common and minimum; dead names and dead copies removed; atoms re-quoted |
| Wave | 0 (now, after T-119) |
| Layer (CLAUDE.md §3) | 0-1 |
| Kind | **TOOLING** (doctrine prose, CLAUDE.md, the state-graph instrument's atoms, deletions of unread content; no code, no research rows) |
| Executor | NOT FOR SONNET: Opus-class. It rewords doctrine (`governance/mission-and-epistemics.md` commitment 2, `governance/evidence-architecture.md`) to the owner's words, and each amended passage must still say what its file is for. Doctrine is the owner's: the pull request is the owner's to merge, and its body lists every passage before and after |
| Traces to | TERM-RESOLUTION-PLAN §1, §2 (R rows), §5, §4 TT-5, §7 step 2, §8 risks 4 and 6 |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-119 merged (each amended passage carries a note "Amended 2026-11-14 (ledger: Unification 2026-11-14 — best, most common, minimum; showing and grading)", which must name a heading that exists). Check by running: `git grep -c -F 'Unification 2026-11-14' references/project-standards.md` prints at least 1. If T-119 is not yet merged but its branch is pushed, a draft may be stacked on it (`git switch -c task/t-120-doctrine-amendments-and-deletions origin/task/t-119-ledger-unification-entry`) and takes `git merge "$BASE"` once it merges.
- **Owner decisions:** none. The rulings applied are in the ledger (from "Owner statement 2026-11-14 — convergence means values coming together" to the end). **Not this task's, because they wait on an owner answer:** the W rows of TERM-RESOLUTION-PLAN §2 (the circle table, T-117, on OD-57 and OD-59); the prose-register voice line (T-035, on OD-60); the `.ignore` change (T-121, on OD-61).
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T120-01` to `T120-03` (section 6).
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-120-doctrine-amendments-and-deletions "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task never moves it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-120" && mkdir -p "$SCRATCH"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

The doctrine every session reads says best practice is chosen from T1–T2 values only, that a code value never establishes it, that the floor is selected as the most accommodating value, and that the hierarchy "adjudicates"; the owner ruled the opposite on 2026-11-14. CLAUDE.md and other files (the first evidence command lists them) name a table, `best_practice_synthesis`, that is not in the schema. Copies with no reader (a queue for an absent skill, an uncited population list, a template for files no skill writes) keep the old sense alive in every search.

**Evidence commands** (read-only):

```
git grep -n -F 'best_practice_synthesis' -- CLAUDE.md governance skills | cut -c1-120
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select name from sqlite_master where name in ('best_practice_synthesis','v_best_practice','v_code_floor_only')\").fetchall())"
grep -c -F '## 0.' governance/evidence-architecture.md
git grep -n -i -E 'most-accommodating floor|does not establish best practice|hierarchy adjudicates|converged best-practice' -- governance references/methodology-evidence-hierarchy-mapping.md | cut -c1-140
for f in references/connections/application-queue.md references/website/data/populations.json references/bpc/_template.md; do printf '%s readers: ' "$f"; git grep -l -F "$(basename "$f")" -- scripts skills .claude .github | wc -l; done
for a in workplan/pipeline-state-graph/atoms/*.jsonl; do python3 workplan/pipeline-state-graph/verify_atoms.py "$a" > /dev/null 2>&1; echo "$a rc=$?"; done
```

**Expected output today:** hits for `best_practice_synthesis` in CLAUDE.md, governance and skills; the schema holds `v_best_practice` and `v_code_floor_only` only; `0` (no §0); hits for each superseded sense; `0` readers for each of the three files; every atoms file verifying (record the rc of each: it is the base state). If the output differs, the ground has moved: stop (section 9). Check `verify_atoms.py`'s own usage line before relying on the loop above; if it takes no file argument, run it as its usage says.

## 4. The change

Every replacement is a pointer ("see `governance/evidence-architecture.md` §0") or a short phrase in the owner's words; where a passage would restate the definition, it points instead (rule 5). Each amended passage is replaced in place (the old text lives in `git log -p`) and carries one note line: "Amended 2026-11-14 (ledger: Unification 2026-11-14 — best, most common, minimum; showing and grading)".

1. **`governance/evidence-architecture.md` §0 "The figures of a cell"** (new; the one home): U1 best (the most accommodating identified value for the cell's lens and context; tier sets marker and weight, never eligibility; the one exception, the harm test: "does the research prove that the more accommodating value leads to worse results? if so, research wins. if no, code wins"); U2 most common (convergence, values coming together across any tiers, is most common practice, never best; the definition of convergence stays in `governance/evidence-methodology.md` §3.2, which T-068 rewrites); U3 the minimum (a factual data point; from the code stratum unless there is no code data; in accommodation order, so it may be the highest number); U4 the four figures (minimum, mode, median, maximum) in the parameter's accessibility direction, the best being the maximum in accommodation order; U6 code-only (where the only values are code, the most accommodating code value is the best, with its code marker); U8 transparency (every value shown, cited, no claim of the project's own authority). Quote the owner from the ledger entries, by heading.
2. **The R rows of TERM-RESOLUTION-PLAN §2 with no task named**, each located by its text (the line numbers in the plan drift): `governance/evidence-architecture.md` (the "most-accommodating floor selection" passages become "most-accommodating selection; the minimum is its own figure"; best is never convergence; roots shown beside convergence; "best-practice determination" stays, but the floor is never called the best); `governance/evidence-methodology.md` (the passages the plan lists outside T-068's sweep: point to §0; "the hierarchy adjudicates" becomes "the tier grades the marker"; **do not touch** §3.2's convergence definitions, the voice-pattern rows or §2.3's richness criteria, which are T-068's); `governance/mission-and-epistemics.md` (commitment 2 and Test 3 point to §0; "specifies the evidence-based value" becomes "shows the most accommodating identified value with its citation"; the "which dimension governs" passage becomes: the most accommodating value stands unless a source shows it leads to worse results, and the divergence stays visible); `governance/tier-system.md` (the two lines that withhold T4 and T5 values: they are eligible like any other, and tier sets weight and marker; the superseded banner's ⚠ becomes the word "Superseded", since ⚠ is now a marker: check whether the line the plan calls 22 carries the glyph, `grep -n '⚠' governance/tier-system.md`); `governance/adversarial-use-framework.md` (the passages that contradict each other inside the file both point to §0); `governance/jurisdiction-philosophy.md` ("A code value does NOT establish best practice" becomes "best only where a cell's values are all code, or under the harm test"; the ranking by jurisdiction count is the mode's significance, not best); `governance/legal-regulatory.md` (show the four figures; "recommendations" becomes "cited values"); `governance/co1-operational.md` ("the converged best-practice value" becomes "the most common identified value"); `governance/grounds.md` and `governance/held-tensions.md` (one meaning; point to §0); `references/methodology-evidence-hierarchy-mapping.md` (the code stratum is where the minimum comes from, and its values are eligible; the row the plan marks W is T-117's); `references/methodology/economics-methodology-core.md` ("Best practice based on [N] jurisdictions" becomes the mode; "Tier 0/1/2" become the design-mode names); `workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md` (its best-practice definition points to §0; its "OR-4" becomes the harm test; "the guidebook's own choice" stands under the determination ruling). `governance/audience-priority.md`'s "specifies the evidence-based aspiration" is left (it states the ideal).
3. **The dead table name** `best_practice_synthesis`, a prose caller of a table not in the schema: in CLAUDE.md §6 and every governance file and skill the first evidence command lists, it becomes `specifications` (read through `v_best_practice`). CLAUDE.md is loaded into every turn: change only the name, and run `claude_md_spine` after. Where a skill file is also T-035's (its BPC flows), change only the name here; T-035 does the rest.
4. **The delete list** (TERM-RESOLUTION-PLAN §5): delete `references/connections/application-queue.md` and `references/bpc/_template.md` (no reader: the evidence command); move `references/website/data/populations.json` to `_archived/references/website/data/populations.json` (content, not code: CLAUDE.md §8) and correct its two prose callers (`git grep -n -F 'populations.json' -- architecture references/website`). Re-run the reader search after each; a reader that appears is a stop.
5. **`governance/doctrine-deltas.json`**: commitment 2 is amended, so append a new state recording the amendment, in the file's own shape (read its newest entry first); never edit an earlier state.
6. **The state-graph instrument** (TERM-RESOLUTION-PLAN §4 TT-5; data, not a registered check: do not register it): apply the adjudicator G's edits the plan lists (atoms `ent`, `evi`, `led1`, `prc`; two records in `conflicts.yaml`; one line of `machines.yaml`), with "○" changed to "code marker"; correct atoms through the instrument's own `status_corrections` (TERM-RESOLUTION-PLAN §3 (d)), not through the ledger; re-quote every atom whose governance source items 1 to 3 change (`verify_atoms.py` checks quotes verbatim: risk 4 of the plan); add atoms quoting the ledger where the plan says ADD. Then rebuild the generated files (`ATOMS.tsv`, `AMBIGUITIES.tsv`, `CONFLICTS.md`, `STATE-GRAPH.md`) with `python3 workplan/pipeline-state-graph/build_graph.py`; never edit them by hand. The T4 limb of these edits waits on T-117 and is left.
7. **Prose-caller re-grep** (risk 6): after items 1 to 6, `git grep -n -i -E 'best_practice_synthesis|floor claim|Ideal → Best Practice|\bacceptable\b' -- governance references architecture skills ':!references/project-standards.md' ':!references/bpc' ':!references/search-log'`; list every remaining hit in the pull request as amended, left (with why), or another task's (T-035, T-068, T-117).

**Chosen (authoring 2026-11-14):** one pull request for the doctrine, the dead name, the deletions and the atoms, because the atoms quote the doctrine and must move with it (risk 4). Rejected: superseding each frozen corpus file by file (T-119's one entry does it in prose).

**What reads what this task changes:** every session (CLAUDE.md, governance); `verify_atoms.py` and `build_graph.py` (the atoms); T-068, T-059, T-035, T-117 (they point to §0). **What wrong thing reaches the guidebook without it:** a session writing a page or a check from the doctrine names the floor or the most common value best practice, or withholds a code value the owner made eligible.

## 5. Caller sweep

Names to sweep: `best_practice_synthesis`, `application-queue.md`, `populations.json`, `_template.md`, and each superseded phrase item 2 replaces.
```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
Left out: `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`, and frozen workplan prose (T-119 supersedes it in prose).

## 6. Verification

**Step 1, the before-run.**
```
CHECKS="claude_md_spine schema_reference_audit skill_vocabulary_audit retired_vocabulary"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
python3 workplan/pipeline-state-graph/build_graph.py --check > "$SCRATCH/before-graph.txt" 2>&1; echo "graph rc=$?"
```
**Step 2: red before, green after.**
- `T120-01`: `git grep -c -F 'best_practice_synthesis' -- CLAUDE.md governance skills` prints hits before and none after.
- `T120-02`: `grep -c -F '## 0.' governance/evidence-architecture.md` prints 0 before and 1 after; every superseded phrase of section 3's fourth command prints nothing after.
- `T120-03`: the three deleted or moved files are absent from their old paths; `populations.json` exists under `_archived/`; no live reader names an old path.
- Every atoms file verifies after (each rc as before or better); `build_graph.py --check` reports no failure above its before-run.
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
git commit -m "governance: doctrine states best, most common and minimum as ruled; dead names and copies removed [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: every amended passage before and after; the deletions and their reader searches; the doctrine-deltas state; the atoms re-quoted; the re-grep of item 7; checks with EXAMINED>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not apply the circle table, gloss ○ anew, or write ⚠ as a marker in doctrine (T-117, on OD-57 and OD-59). Do not change the prose register's voice (T-035, on OD-60). Do not edit `.ignore` (T-121, on OD-61).
- Do not touch the convergence definitions, voice rows or richness criteria of `governance/evidence-methodology.md` (T-068's sweep).
- Do not edit the ledger, a decision record (T-119) or a frozen record. Do not edit a generated state-graph file by hand. Do not register the state-graph instrument as a check.
- Do not delete a file with a live reader. Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: T-119 is not merged; a passage the plan names is not found by its text; an amendment would need a doctrine choice the ledger does not hold (stop: it is the owner's); a deleted file has a reader; an atom cannot be re-quoted verbatim; `claude_md_spine` or `schema_reference_audit` is red after; a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request (the deleted files come back with it).

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (it should test each amended passage against the ledger's words); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
