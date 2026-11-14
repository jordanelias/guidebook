# T-119  The ledger's unification entry: best, most common, minimum; showing and grading (with its supersession pairs)

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/TERM-RESOLUTION-PLAN.md` section 1 (the canonical definitions), section 3 (the supersession entries) and section 7 step 1 (its PR-1) (folded 2026-11-14; where that plan and this file differ, that plan governs, and the ledger's owner rulings govern both). Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the fold of the term-resolution plan (its PR-1). It can ship now: it needs no owner answer and no earlier task. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-119 |
| Title | The ledger's unification entry: best, most common, minimum; showing and grading (with its supersession pairs) |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 0 |
| Kind | **TOOLING** (governance: the ledger, `decisions/` markers and an attestation; no code, no research rows) |
| Executor | NOT FOR SONNET: Opus-class. The entry restates the owner's rulings of 2026-11-14 in their own words and chooses the anchor quotes; a misquote here becomes the record every later task points at |
| Traces to | TERM-RESOLUTION-PLAN §1, §3 (a) to (c), §7 step 1; the owner instruction to fold it (`grep -n -F "Owner instruction 2026-11-14 (last) — fold the term-resolution plan" references/project-standards.md`) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none.
- **Owner decisions:** none. This task records rulings already in the ledger (the entries from "Owner statement 2026-11-14 — convergence means values coming together" to the end); it decides nothing. OD-57 to OD-62 stay open and are named in the entry as open, never answered by it.
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T119-01` (section 6): the unification entry and its pairs do not exist.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-119-ledger-unification-entry "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task never moves it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-119" && mkdir -p "$SCRATCH"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

The owner's meaning of best practice (the most accommodating identified value), most common practice (where values come together) and the minimum (the code stratum's least accommodating value) is spread over the ledger entries of one day (count them: `grep -c -E '^## Owner .*2026-11-14' references/project-standards.md`), while decision records that a live reader still reaches say the opposite (best practice as convergence, or as T1–T2-only, or the floor as best), and nothing at those records says they no longer hold. A reader who greps "best practice" meets the old sense first.

**Evidence commands** (read-only):

```
grep -c -F 'Unification 2026-11-14' references/project-standards.md
python3 scripts/audit/supersession_backpointer_audit.py 2>&1 | grep -E 'EXAMINED|PASS|FAIL' | tail -3
for f in DR-2026-05-24-best-practice-supersession-protocol DR-2026-05-26-gap-driven-mining-protocol DR-2026-07-12-evidence-architecture-unification DR-2026-07-12-evidence-cell-state-schema-reconciliation DR-2026-07-13-value-genealogy-and-derivation-handshake DR-2026-07-20-intra-category-cross-test DR-2026-07-21-evidence-architecture-option-a-execution DR-2026-07-21-product-posture-thinking-tool-not-authority RATIFICATION-PACKAGE-2026-07-12; do printf '%s ' "$f"; grep -c -i -E 'best[ _-]?practice|floor|converg' "decisions/$f.md"; done
```

**Output on 2026-11-14:** `0`; the audit's line (record it: the after-run's `EXAMINED:` must be higher by exactly the number of pairs this task adds); a non-zero count for each record. If the first prints a non-zero count, the entry exists: stop (section 9).

## 4. The change

1. **One ledger entry**, appended to `references/project-standards.md` (append only; never edit an earlier line), headed `## Unification 2026-11-14 — best, most common, minimum; showing and grading`. It carries:
   - **The definitions, U1 to U9 of TERM-RESOLUTION-PLAN §1,** each as the owner's words quoted verbatim from the ledger entries they come from (find each by `grep -n -F '<the quoted words>' references/project-standards.md`; a quote that is not found verbatim is not written), with the home that holds the operative text (`governance/evidence-architecture.md` §0 for U1 to U4, U6; `governance/mission-and-epistemics.md` for U5 and U8; `governance/tier-system.md` §5 for U7; `governance/stage-map.yaml` for U9). The entry points; it does not re-explain (rule 5).
   - **A BY sentence unique in the ledger**, for example "the figures of a cell are read under evidence-architecture §0 from 2026-11-14"; check it occurs once with the audit's normalisation (the docstring of `scripts/audit/supersession_backpointer_audit.py`).
   - **(a) machine pairs**, one `SUPERSEDES: <one path> :: "<quote>"` line with its `BY: references/project-standards.md :: "<the BY sentence>"` line per target, for the decision records TERM-RESOLUTION-PLAN §3 (a) lists **except** those it marks for when the circle table is applied (the weighted-strength reconciliation record and the option-A execution record's table lines: T-117's): `decisions/DR-2026-05-24-best-practice-supersession-protocol.md` (three passages), `decisions/DR-2026-05-26-gap-driven-mining-protocol.md`, `decisions/DR-2026-07-12-evidence-architecture-unification.md`, `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md` (two), `decisions/DR-2026-07-13-value-genealogy-and-derivation-handshake.md`, `decisions/DR-2026-07-20-intra-category-cross-test.md`, `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md` (the two passages not tied to the table), `decisions/DR-2026-07-21-product-posture-thinking-tool-not-authority.md` ("the practice the evidence best supports"), `decisions/RATIFICATION-PACKAGE-2026-07-12.md` (two). Locate each passage by the term plan's line number **and then by its text**: line numbers drift; the quote must occur exactly once in its file under the audit's normalisation. **The posture record's passage the term plan calls :45 is not superseded** (the owner's definition of determination answers it).
   - **(b) prose-only supersession** (no pair, no marker): one paragraph naming the frozen corpora of TERM-RESOLUTION-PLAN §3 (b), by path, as superseded in their sense of best practice by this entry. `governance/doctrine-deltas.json` is not superseded here: T-120 appends a new state to it when commitment 2 is amended.
   - **(c) ledger rules and migration rows that can only be superseded in prose**: the earlier ledger lines and rulings §3 (c) names (OR-4, and OR-6c as to selection only; OR-6 and OR-6b keep their status words), found by their text, not by line number (`grep -n -E '^OR-4:|OR-6c' references/project-standards.md`), and the `decisions` rows of `scripts/migrations/057_baseline_2026-08-12.sql` it names, which stay `ACTIVE` because no writer exists (the GAP of `OPEN-ITEMS-PLAN.md`, the term plan's TT-6).
   - **What stays open:** OD-57 to OD-62, by number, unanswered.
   - `CONDITION:` / `ACTION:` / `DATE:` lines in the ledger's form.
2. **A marker beside each (a) target**: in the target paragraph, or the paragraph directly after it, one line naming SUPERSEDED (or AMENDED where the passage is only narrowed) and carrying the BY sentence verbatim. The old text stays.
3. **An attestation**: touching `decisions/` needs `attestations/<slug>.json` against `schemas/attestation.schema.json` (CLAUDE.md rule 2); copy the shape of the newest file in `attestations/` and fill it for this pull request.

**Chosen (authoring 2026-11-14):** one entry with one BY sentence for every pair, as the plan says. Rejected: one entry per corpus (the plan's reconciliation 6 collapsed those).

**What reads what this task adds:** `supersession_backpointer_audit` (the pairs and markers); T-120 (its "Amended 2026-11-14 (ledger: <heading>)" notes point to this entry's heading); T-117 (adds its pairs under the same BY sentence); every reader of a decision record. **What wrong thing reaches the guidebook without it:** a session reading a decision record takes "best practice" to mean convergence or the code floor, and copies it into a page or a check.

## 5. Caller sweep

Names to sweep: the BY sentence (it must occur once), and each target quote (once in its file).
```
python3 scripts/audit/supersession_backpointer_audit.py
git grep -n -F -e '<the BY sentence>' -- references/project-standards.md decisions
```
Left out: everything this task does not edit. This task changes no code, view, verb or check.

## 6. Verification

**Step 1, the before-run.**
```
CHECKS="supersession_backpointer_audit attestation_presence attestation_schema"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
**Step 2: red before, green after.** `T119-01`: section 3's first command prints 0 before and 1 after; `supersession_backpointer_audit` PASSes with `EXAMINED:` higher than the before-run by exactly the number of `SUPERSEDES:` lines added (`git diff "$(git merge-base HEAD "$BASE")" -- references/project-standards.md | grep -c '^+SUPERSEDES:'`). Seeded defect: delete one marker line; the audit FAILs naming that target; restore.
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
git commit -m "governance: unification entry for best, most common and minimum, with supersession pairs [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the entry's heading; each pair and its marker; the audit's EXAMINED before and after; the attestation>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not edit any earlier ledger line; append only. Do not write a quote you did not find verbatim.
- Do not answer, or read as answered, any of OD-57 to OD-62. Do not supersede the posture record's passage the plan says stands.
- Do not write pairs for the records T-117 owns (the circle table). Do not edit governance files (T-120) or code.
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the entry already exists; a target quote occurs zero or several times in its file and no unique quote of the same passage can be found; the BY sentence is not unique; the audit FAILs after on a pair this task added; a check green before is red after; `sha256sum data/guidebook.db` changes.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: a new ledger entry that withdraws this one (the ledger is append-only), with the markers removed in the same pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (it should test each quote against the ledger); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
