# T-122  The stage contracts carry the owner's rulings of 2026-11-14 as criteria, each pointing at a test that already exists

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: finding A4.1 of the adversarial pass on the remediation plan (`scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/adj/AUDIT-FINDINGS.md`), re-verified 2026-11-14. Every number in this file was read on 2026-11-14 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-14 by the repair writer of the adversarial pass. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-122 |
| Title | The stage contracts carry the owner's rulings of 2026-11-14 as criteria, each pointing at a test that already exists |
| Wave | 6 (after the term-resolution tooling) |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: Opus-class. Each criterion states an owner ruling in the contract's words, which is a reading of the ledger, and must quote it without adding to it |
| Traces to | the ledger entries from "Owner statement 2026-11-14 — what \"best practice\" is" to the end (`grep -n -E '^## Owner (statement|answer|answers|correction|proposal) 2026-11-14' references/project-standards.md`); `governance/pipeline-contract.yaml` (the stage contracts) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-059, T-068, T-117 and T-124 merged. Each writes the test cases a criterion below points at: T-059 the selection tests `T059-H1` to `T059-H7` (`T059-H4` withdrawn under OD-65), T-068 the convergence tests (`T068-11` guards that convergence changes no value or marker), T-117 the marker tests `T117-01` to `T117-08` and the C10 change, T-124 the four-figure tests `T124-01` onward; a criterion may not point at a case that does not exist. Check by running, per task, `git log "$BASE" --format=%s | grep -c -E 'task/<its branch>|^T-NNN:|execute workplan T-NNN'` with its branch (`task/` plus its file stem in lower case) and id, printing at least 1, and `git grep -c -E 'T059-H7|T068-11|T117-07|T124-01' -- scripts/tests` printing a count for each.
- **Owner decisions:** none as a gate. The criteria state rulings already in the ledger. OD-63, OD-64 and OD-65 were **answered by the owner 2026-11-14** (fifteenth set; `grep -n -F "Owner answers 2026-11-14 (fifteenth set)" references/project-standards.md`): the maximum, the mode and the median over all identified values, and the render page showing only the four figures as a colour code on the surveyed code bodies (OD-63); the triangle for every grey basis (OD-64); every code value carrying a lens, assigned by contextual judgment where not stated (OD-65). Each criterion that rests on one quotes its answer line (`grep -E '^OD-63:' references/project-standards.md | tail -1`, and the same for OD-64 and OD-65); *earlier text, answered, see this bullet:* "where a ruling is still the owner's … the criterion … is not written while that line is missing".
- **Delegated resolutions this task rests on:** none.
- **Tests that must be red before you start:** `T122-01` (section 6).
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-122-contract-carries-the-owner-rulings "$BASE"         # real execution only
sha256sum data/guidebook.db                                  # record it; this task never moves it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-122" && mkdir -p "$SCRATCH"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

The owner's rulings of 2026-11-14 (best is the most accommodating identified value, replaced only under the harm test; the four figures in the parameter's accessibility direction; the minimum from the code stratum; the circle table and ⚠; convergence is the mode, never the best) reach the engine through T-059, T-068, T-117 and T-124, but no stage contract names them. `governance/pipeline-contract.yaml` is the single statement of what each stage must satisfy; a session reading it learns nothing of these rulings, and a later change that undoes one meets no criterion saying it is a stage's obligation.

**Evidence commands** (read-only):

```
python3 -c "import yaml;d=yaml.safe_load(open('governance/pipeline-contract.yaml'));print(d.get('status'),d.get('ratified'));[print(s['id'],[(c['id'],c.get('check')) for c in s.get('criteria',[])]) for s in d['stages'] if s['id'] in ('synthesis','specification','render')]"
git grep -n -i -E 'accommodat|harm|direction|marker|minimum' -- governance/pipeline-contract.yaml governance/stage-map.yaml | cut -c1-120
python3 scripts/audit/pipeline_contract_audit.py | grep -E '^\[2\]|INCOMPLETE|BROKEN'
```

**Output on 2026-11-14:** `PROPOSED False`; synthesis `[('opus-routing', None)]`; specification `governing-refs-nonempty`, `no-regulatory-stratum-stated`, `tier3-alone-threshold`, `no-diagnosis-only-determination`, `derivation-handshake`; render `register-invariants` (check `None`) and `mode-stratum-matrix-consistency`; the second command prints only `base-direction-from-source` and the band lines T-120 amends, nothing in `stage-map.yaml` (it maps tables to stages and names no tools, so it is not edited here); the audit's referential-integrity line. If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: no new check, no new script. Each criterion points its `check:` at a registered test file that already holds the cases (`scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_integrity.py`: both are registered, so the contract audit classes them VERIFIABLE: `python3 -c "import yaml;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if c['id'] in ('test_assess_cell_pilot','test_db_integrity')])"`), names the case ids in its `criterion` text, and quotes the ledger heading in `references`. Where no test exists yet, `check: null` and the criterion says so (the audit classes it INCOMPLETE, a declared gap, as `register-invariants` already is).

1. **specification: `spec-best-is-most-accommodating`** (kind: integrity). The criterion is the selection rule, quoted from its one home (`tasks/T-059-wp-t4-agreement.md` section 4 item 6, "The selection rule, one home in this plan", as built), with the OD-58 and OD-65 answer lines the ledger carries; a parameter with no recorded direction states no value. `check: scripts/tests/test_assess_cell_pilot.py` (cases `T059-H1` to `T059-H7`, `T059-H4` withdrawn under OD-65). References: the harm-test entry; "where the only values are code, the code determines the best"; OD-58; OD-65.
2. **specification: `spec-four-figures`** (kind: integrity). The minimum is the code stratum's least accommodating value, or the least accommodating identified value where the cell has no code value, labelled by stratum; the maximum, mode and median over every identified value for the cell and its context, every stratum (OD-63, answered 2026-11-14); every figure in the parameter's accessibility direction, never in numeric order; no minimum or maximum without a recorded direction. `check: scripts/tests/test_assess_cell_pilot.py` (cases `T124-…`, the ones T-124 wrote). References: the four-figure entry, the minimum's scope, the direction entry, OD-63.
3. **specification: `spec-marker-table`** (kind: integrity). ● T1, T2, Co-1, Co-2; ◐ T3 (a non-grey basis), T4; ○ T5, T6; ⚠ (U+26A0 alone) and no circle for every grey basis (T3 grey included: OD-64, answered 2026-11-14, "triangle for all"), and for an unverified or thin basis; a showcased value carries its own source's grade (OD-59). `check: scripts/tests/test_assess_cell_pilot.py` (cases `T117-01` to `T117-08`). References: the circles entries, the triangle entries, OD-57, OD-59, OD-64.
4. **specification: `spec-unverified-kept-at-triangle`** (kind: integrity). A published cell may rest on an unverified source only with ⚠. `check: scripts/tests/test_db_integrity.py` (C10 as T-117 item 4a rewrote it, and `T117-07`). References: "grey, thin and unverified sources are kept, and carry a triangle warning"; the triangle correction.
5. **synthesis: `convergence-is-the-mode`** (kind: integrity). A convergent assessment is most common practice; it changes neither the value stated nor the marker. `check: scripts/tests/test_assess_cell_pilot.py` (case `T068-11`). References: OD-43; the convergence entry, ACTION (3) to (5).
6. **render: `render-figures-in-direction`** and **`render-figures-cited`** (kind: integrity). The page shows the four figures as T-124 returns them, in the parameter's accessibility direction, only as a colour code on the jurisdictional code bodies surveyed for the cell, with a non-colour carrier for each colour, each figure and code body cited (OD-63, answered 2026-11-14); it calls no value acceptable, required or recommended on the project's authority. `check: null`, with the sentence "UNENFORCED until T-037 fills it with its own test file (T-037 section 6, cases `T037-F1` to `T037-F5`); the wording half is a reading (AT-38) and may stay unenforced". References: OD-63, the transparency entry, "we gather and show", the four-figure entry. *Renamed 2026-11-14 from `render-every-value-cited` on OD-63's answer (the render page no longer lists every value); the tension with the transparency entry is recorded, not resolved: `TERM-PLAN-FOLD.md` conflict 23.*
7. **Leave** `governance/stage-map.yaml` unedited (it maps tables, not tools) and say so in the pull request; leave the band statements T-120 already amended.

**Chosen (authoring 2026-11-14):** criteria that point at tests the dependencies write. Rejected: a new registered check per ruling (apparatus with no book-facing defect the tests do not already catch: CLAUDE.md §8). A new check is justified only if the executor names a wrong thing that reaches the guidebook which none of the cited cases can catch; then stop and report it.

**What reads what this task adds:** `pipeline_contract_audit.py` (and `test_pipeline_contract`), every session that reads the contract before working a stage, and T-037 (which fills item 6's `check:`). **What wrong thing reaches the guidebook without it:** a later change that undoes a ruling (a numeric minimum, a convergence that lifts a marker, a code value hidden behind research) breaks no stage contract, so a session working the stage from the contract never learns the ruling binds it. **What it makes deletable:** nothing.

**Code size.** No code: `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` prints nothing.

## 5. Caller sweep

Names to sweep: each new criterion id. `governance/context-map.yaml` is generated from the contract: run `python3 scripts/generate/context_map.py` and include its output. Prose that restates a criterion list (`git grep -n -F 'derivation-handshake' -- governance architecture CLAUDE.md references ':!references/project-standards.md'`) is read; a sentence that enumerates the specification criteria and is now short is corrected, or listed.

## 6. Verification

**Step 1, the before-run.**
```
CHECKS="test_pipeline_contract"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$?"; done
python3 scripts/audit/pipeline_contract_audit.py > "$SCRATCH/before-audit.txt" 2>&1; grep -E '^\[2\]' "$SCRATCH/before-audit.txt"
```
**Step 2: red before, green after.**
- `T122-01`: `python3 -c "import yaml;d=yaml.safe_load(open('governance/pipeline-contract.yaml'));print(sorted(c['id'] for s in d['stages'] for c in s.get('criteria',[]) if c['id'] in ('spec-best-is-most-accommodating','spec-four-figures','spec-marker-table','spec-unverified-kept-at-triangle','convergence-is-the-mode','render-figures-in-direction','render-figures-cited')))"` prints `[]` before and all seven after.
- The audit's `[2]` line after shows VERIFIABLE up by five and INCOMPLETE up by two, BROKEN and QUARANTINED unchanged.
- Each cited case id exists: `git grep -c -E '<case id>' -- scripts/tests/<file>` for every id the criteria name.
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
git commit -m "governance: stage contracts carry the owner's rulings of 2026-11-14 [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: each criterion, its ledger quote and the case ids it points at; the audit's [2] line before and after; the context map regenerated>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not add a check, a script or a registry entry. Do not point a criterion at a case that does not exist. Do not paraphrase a ruling beyond its ledger words, and do not state a ruling the ledger does not carry (OD-63 to OD-65 are quoted from their answer lines, answered 2026-11-14).
- Do not edit `governance/stage-map.yaml`, the ledger, a decision record, a skill or code. Do not ratify the contract (OD-17 is the owner's).
- Do not write `data/guidebook.db`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: a dependency is not merged; a case id a criterion would cite does not exist; the audit's BROKEN or QUARANTINED count rises; a ruling would need wording the ledger does not hold; an answer line for OD-63, OD-64 or OD-65 is missing; a check green before is red after.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: `git revert <merge commit>` in a new pull request.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (it should test each criterion against the ledger's words and each `check:` against the cases it names); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
