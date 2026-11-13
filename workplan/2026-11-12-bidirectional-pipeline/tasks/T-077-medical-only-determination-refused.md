# T-077  A determination keyed on a medical code alone is refused at write

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 (AT-34, first half), probe in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/R2-probes.md` (section AT-34). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13; the R2 probe was re-run on that day's HEAD and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-077 |
| Title | A determination keyed on a medical code alone is refused at write |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 1-2 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | Sonnet-class |
| Traces to | AT-34 first half ("A determination with only a medical code is refused", `grep -n 'AT-34' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md`); REQ-075; the contract criterion `no-diagnosis-only-determination` (`grep -n -F 'No determination is keyed on medical_code alone' governance/pipeline-contract.yaml`) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it). Never use a literal `origin/main` in a command of this file.
- **Tasks that must be merged to the integration base first:** none. (T-018 and T-019, whose lens columns on `specifications` and `assess_cell.validate_lens` this task edits, are merged on 2026-11-13: `git log "$BASE" --oneline | grep -F 'task/t-019-lens-gather'`.) **Order:** this task must merge before any determination is written once `base_taxonomy_medical` holds rows (T-103 fills it; T-110 writes the first determinations); the coordinator records that edge.
- **Owner decisions:** none. The rule is ratified contract text: "No determination is keyed on medical_code alone. A medical lens always accompanies at least one of identity, ICF or access-need on the cell." (`governance/pipeline-contract.yaml`, criterion `no-diagnosis-only-determination`), and the owner's "we give our users the choice of what model they want to use to browse the site" with D-0170 offering the medical model as a choice and not adopting it.
- **Tests that must be red before you start:** AT-34 first half, restated in section 6.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-077-medical-only-determination-refused "$BASE"       # real execution only
sha256sum data/guidebook.db                                  # record it
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-077" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"
```
- Shell variables do not survive between tool calls: begin every later block with the `W=…; BASE=…` and `export SCRATCH=…` lines. **Real execution:** `/session-open` first. **Pilot:** no `/session-open`, stay on the given branch, stop after section 7.

## 3. The problem, in the guidebook's terms

A cell whose only lens is a diagnosis renders as "this is what disabled people with condition X need": the medical model as the project's frame, which the owner offers to readers as a choice and does not adopt. The schema accepts such a row, the engine does not refuse one, and the only detector is advisory, after the fact, and counts the wrong subject. Today the empty medical registry hides this: the engine refuses for the wrong reason (no such code). Once T-103 fills `base_taxonomy_medical`, a medical-only determination becomes writable.

**Evidence commands** (on the scratch copy; the canonical database is not written):

```
python3 - "$SCRATCH/t.db" <<'PY'
import sqlite3,sys
c=sqlite3.connect(sys.argv[1])
print([l.strip() for l in c.execute("select sql from sqlite_master where name='specifications'").fetchone()[0].splitlines() if 'COALESCE' in l])
print('medical rows', c.execute('select count(*) from base_taxonomy_medical').fetchone()[0])
print('triggers', [r[0] for r in c.execute("select name from sqlite_master where type='trigger' and tbl_name='specifications'")])
p=c.execute("select min(parameter_id) from base_parameters where status='active'").fetchone()[0]
c.execute('pragma foreign_keys=off')
try:
    c.execute("insert into specifications(parameter_id, medical_code, state) values (?,?,?)",(p,'TASK-FIXTURE-MED','pending')); print('raw medical-only insert, FKs off: ACCEPTED')
except Exception as e: print('raw medical-only insert, FKs off: REFUSED', e)
c.rollback()
PY
SL=$(python3 -I -c "import sqlite3,os;print(sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True).execute('select slug from slugs order by 1 limit 1').fetchone()[0])")
P=$(python3 -I -c "import sqlite3,os;print(sqlite3.connect('file:'+os.environ['SCRATCH']+'/t.db?mode=ro',uri=True).execute(\"select min(parameter_id) from base_parameters where status='active'\").fetchone()[0])")
python3 scripts/assess/assess_cell.py --db "$SCRATCH/t.db" --emit-sql "$SCRATCH/emit.sql" --slug "$SL" --stamp "$(date -u '+%Y-%m-%d %H:%M')" --parameter-id "$P" --medical TASK-FIXTURE-MED --session session_task-probe 2>&1 | tail -1
GUIDEBOOK_DB_PATH="$SCRATCH/t.db" python3 scripts/audit/medical_lens_integrity.py | grep -E 'EXAMINED|VERDICT'
```

**Output on 2026-11-13:** the CHECK line `CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)`; `medical rows 0`; `triggers ['trg_spec_retire_needs_reason']`; `raw medical-only insert, FKs off: ACCEPTED`; the engine prints `REFUSING: medical_code 'TASK-FIXTURE-MED' is not a live medical_code in base_taxonomy_medical` (the wrong reason: the registry is empty); the audit prints `EXAMINED: 0` and `VERDICT: CLEAN` (its `EXAMINED` counts medical-registry rows, not the determinations it tests).

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect.

1. **Schema migration: two triggers on `specifications`.** `trg_spec_lens_not_medical_only_ins` (`BEFORE INSERT`) and `trg_spec_lens_not_medical_only_upd` (`BEFORE UPDATE OF identity_code, icf_code, needs_code, medical_code`), each `WHEN COALESCE(NEW.identity_code, NEW.icf_code, NEW.needs_code) IS NULL AND NEW.medical_code IS NOT NULL`, each `SELECT RAISE(ABORT, '<message>')`, where the message names the rule and the next act: "REFUSING: a determination keyed on medical_code alone renders the medical model as the project's frame (pipeline-contract no-diagnosis-only-determination). Add an identity, ICF or access-need lens to the cell." Copy the shape of `trg_spec_retire_needs_reason` (`grep -n -A7 'CREATE TRIGGER trg_spec_retire_needs_reason' scripts/migrations/083_specification_retire_in_place.sql`).
   **Chosen (authoring 2026-11-13):** triggers, not a narrowed table CHECK. A CHECK change in SQLite is a create-copy-drop-rename of `specifications`, which every determination view, index, inbound foreign key and trigger names (`select type, name from sqlite_master where sql like '%specifications%'`); a trigger is added in place, refuses every writer including hand SQL, and its message can name the next act, which a CHECK failure cannot. The existing at-least-one CHECK stays as it is (D-0182).
2. **The engine refuses first, with the same rule.** In `assess_cell.validate_lens` (`grep -n '^def validate_lens' scripts/assess/assess_cell.py`), after the existing "at least one lens" refusal, refuse when the lens has `medical_code` and none of `identity_code`, `icf_code`, `needs_code`, before any registry lookup, so the refusal is for the frame and not for an empty registry. One condition and one message (the trigger's wording).
3. **`medical_lens_integrity.py` counts what it tests.** Keep its existing `EXAMINED: <n>` (medical-registry rows) and print, before it, `EXAMINED: <m>` where `<m>` is the number of live determinations its frame test read (`select count(*) from specifications where retired_at is null`). The runner treats a check as vacuous only when every `EXAMINED:` line is zero (`grep -n 'Deliberately requires EVERY' scripts/run_checks.py`), so the second line makes a run over live determinations count as examined. Do not change its `level` or its `no_floor` reason.

**Schema migration (this task has one).** Never type a migration number. Derive it at execution time: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gives the highest; yours is that plus one, zero-padded, in `scripts/migrations/NNN_spec_not_medical_only.sql`, ending with `PRAGMA user_version` set to the same number. Apply it only with `python3 scripts/migrate_db.py`. Prove it with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). Run `python3 scripts/audit/joined_cells_census.py` before and after (no new candidate). After the migration, run `python3 scripts/generate/context_map.py` and include its output (a schema bump makes `governance/context-map.yaml` stale). The pull request contains no `scripts/migrations/data_*` file.

**What reads what this task adds:** every writer of `specifications` (the engine, and any hand SQL a test or session runs) meets the triggers; `run_checks.py` reads the audit's new `EXAMINED:` line. **What it makes deletable:** nothing; the advisory audit stays as the at-rest detector for rows written before the triggers (none live today: `select count(*) from specifications where retired_at is null and coalesce(identity_code,icf_code,needs_code) is null and medical_code is not null`).

**Code size.** Report `git diff --shortstat "$(git merge-base HEAD "$BASE")" -- scripts schemas .github skills ':!scripts/migrations'` after `git add`.

## 5. Caller sweep

Names to sweep: `validate_lens`, `medical_lens_integrity`, `medical_code`, `specifications`.

**What a caller is.** A hit is a *caller* when its behaviour or its truth changes with this task: code or a test that writes a `specifications` row with a medical code and no other lens, or calls `validate_lens` with such a lens; a view or trigger on `specifications`; a registry entry; a skill or governance sentence that says a medical-only determination is possible or is caught only after the fact. A mention stays true and needs nothing. Fixing a caller is in scope (CLAUDE.md rule 4). Left out: `workplan/`, `references/project-standards.md`, `scripts/migrations/`, `sessions/`, `_archived/`, `audits/`, `versions/`, `transcripts/`, `scratchpad/`.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
`medical_code` and `specifications` have many hits: judge each against the definition, not by name. Known callers on 2026-11-13: `scripts/tests/test_assess_cell_pilot.py` (`T019-28` calls `validate_lens` with a medical-only lens `{"medical_code": "SUP"}` and expects the "superseded" refusal: after this task that lens is refused for the frame first; repoint the case to a lens that also carries an identity, ICF or need code so it still tests what it names, and say so); the fixtures that build `specifications` in `test_evidence_cell_state_2_3.py`, `test_validate_evidence_state_2_4.py`, `test_scan_contract.py` (each inserts with an identity or ICF code: mentions unless one inserts medical alone; check each).

## 6. Verification

**Step 1, before any edit: the before-run.**
```
CHECKS="medical_lens_integrity test_assess_cell_pilot test_evidence_cell_state_2_3 test_validate_evidence_state_2_4 test_scan_contract migration_reproducibility"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E '^ *EXAMINED:|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
On 2026-11-13 `test_assess_cell_pilot`, `test_evidence_cell_state_2_3` and `test_validate_evidence_state_2_4` printed no `EXAMINED:` line (T-075 adds one); count their `PASS` lines instead, and say so. `test_scan_contract` failed G01 and G02 on the base: record and carry on.

**Step 2: red before, green after** (cases `T077-01`…; confirm the prefix is free with `git grep -c 'T077-' scripts/tests/`):
- `T077-01` AT-34 first half, at the schema: on a scratch copy holding one medical registry row made by the test (`db.py add-medical`, labelled `TASK-FIXTURE`, so the foreign key is satisfied and cannot be the reason), an `INSERT INTO specifications` with `medical_code` only, FKs ON, is refused with the trigger's message. Red before (accepted once the FK is satisfied; show it), green after.
- `T077-02` the same row with an identity code chosen by query (`select identity_code from base_taxonomy_identity where status='active' order by 1 limit 1`, or the column the table has on the day) is accepted: the legitimate case still works.
- `T077-03` an `UPDATE` that clears every non-medical lens of a row is refused.
- `T077-04` the engine: `validate_lens` on `{"medical_code": <the fixture code>}` returns the frame refusal, before any registry lookup (also with an empty medical table). Red before (the registry refusal), green after.
- `T077-05` the audit: on a scratch copy with one live determination, `medical_lens_integrity.py` prints an `EXAMINED:` line ≥ 1. Seeded defect: drop the trigger on a copy, insert a medical-only row, the audit FAILs; restore.

**Fixtures** go to a copy, are labelled `TASK-FIXTURE`, and never reach `data/guidebook.db`.

**Step 3: after-run.** The same loop with `after-`; compare failing lines check by check; nothing new may fail.

**Step 4: the gate, once.**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Run once, in the background, after every edit and the migration. If T-075 is not yet merged, run `python3 scripts/audit/research_tooling_separation.py --base "$BASE"` by hand and report it (its registered `cmd` reads `origin/main`). `sha256sum data/guidebook.db` changes only by the migration, and the rebuild reproduces it.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "governance: refuse a determination keyed on a medical code alone (AT-34) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: evidence before and after; callers found and what was done; checks with EXAMINED before and after>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not relax or rebuild the existing lens CHECK; add the triggers only.
- Do not fill `base_taxonomy_medical` beyond a test's own `TASK-FIXTURE` row on a copy (that is T-103, a research task).
- Do not change the medical audit's level or `no_floor` reason.
- Do not write `data/guidebook.db` except through `migrate_db.py`. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.
- Do not hand-type an id, a code or a count; derive it.

## 9. Stop conditions

Stop and report when: the evidence output differs from section 3; a live determination keyed on a medical code alone exists (the triggers would not touch it, but it is a defect for the owner: report it); a caller writes a medical-only determination for a reason you cannot repoint; a check green before is red after; the rebuild does not reproduce the database.

## 10. Rollback

Before merge: close the pull request, delete the branch. After merge: a compensating migration that drops the two triggers, in a new pull request. A committed migration is never edited.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once; `/batch-done`; push; open the pull request last, once, against the integration base (body: problem, evidence before and after, callers, checks with `EXAMINED:`, code size, what was not verified); call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push. One pull request merges at a time; re-derive the migration number after `git merge "$BASE"` if another merged first.
