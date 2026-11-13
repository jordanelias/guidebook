# T-082  The two stored numerical claims with no comparator get one from their source

> **NOT FOR SONNET** — Opus-class. Whether a code's "a surface width of 1800mm can accommodate any amount of … traffic" states a minimum, an exact value or a sufficiency is a reading of the source's meaning, made from the held text; it is not mechanical. A Sonnet-class executor that opens this file does not start it: it reports that the task is waiting for an Opus-class session.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` row OI-56 ("rows 189 and 190 carry no comparator"), found by the T-016 pilot (`grep -n 'Every live numerical claim already carries a comparator' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-016-report.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-082 |
| Title | The two stored numerical claims with no comparator get one from their source |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET (see the note above) |
| Traces to | OI-56; T-016's rule that a value-supplying numerical row carries a comparator (`dbcore.comparator_refusal`, `grep -n 'def comparator_refusal' -A6 scripts/dbcore.py`: "a bare number is read as a point and adds a floor as well as a ceiling"); the writers refuse a new row without one, but the two stored rows predate the rule |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** none. (`amend-extraction --field comparator` exists: `grep -n '_AMENDABLE_SVE_FIELDS =' -A3 scripts/db.py`). **T-108 does not cover these rows** (its subject is conditions held in the unit cell: `grep -n '^| Title' workplan/2026-11-12-bidirectional-pipeline/tasks/T-108-unit-condition-repair.md`); the coordinator may fold this task into T-108 as one more step, since both amend stored figures in one research batch.
- **Owner decisions:** none in the register. OI-55 (1) (how a carry-only research batch is gated) applies to this batch as to T-111: follow the coordinator's ruling when it exists; until then report `research_dod_session`'s lines and do not treat its red as this batch's defect.
- **Tests that must be red before you start:** `select extraction_id from source_value_extractions where figure_role in ('claim','derived') and claim_type in ('numerical','range') and comparator is null` is not empty.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-082-comparator-on-two-stored-figures "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-comparator-two-figures
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-082" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db"
```
- Shell variables do not survive between tool calls: set `BASE`, `STEM` and `SCRATCH` again in every block. **Real execution:** `/session-open`, then `/orient`. **Pilot:** skip `/session-open`, stay on the given branch, stop before the write path.
- Every call points at the scratch copy inline (`GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py … --session "$STEM"`), and rows land only by `emit_batch_sql.py` → `emit_data_migration.py --session "$STEM.md"` → `migrate_db.py` → `migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0), as CLAUDE.md §4 says.

## 3. The problem, in the guidebook's terms

A figure without a comparator does not say whether its number is a floor, a ceiling or a value, so the engine cannot compare it with the other figures for the same parameter. Two claims from one building code carry no comparator; every other claim from that source does.

**Evidence command** (read-only):

```
python3 - <<'PY'
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
ids=[r[0] for r in c.execute("select extraction_id from source_value_extractions where figure_role in ('claim','derived') and claim_type in ('numerical','range') and comparator is null order by 1")]
print('claims with no comparator', ids)
for i in ids:
    print(c.execute("select extraction_id, ref_id, parameter_id, claimed_value, claimed_unit, file_anchor, loc_section, loc_paragraph, claim_text from source_value_extractions where extraction_id=?",(i,)).fetchone())
print('live determinations using them', c.execute("select count(*) from specification_extraction_links l join specifications s using(specification_id) where s.retired_at is null and l.extraction_id in (%s)" % ','.join(map(str,ids or [0]))).fetchone()[0])
PY
```

**Output on 2026-11-13:** `claims with no comparator [189, 190]`; both from `REF-00992` (Approved Document M, Volume 2, UK), parameter 4, `1800 mm` "A surface width of 1800mm can accommodate any amount of non-vehicular traffic without the need for passing places." and `1200 mm` "A surface width of 1200mm may be acceptable on restricted sites, subject to agreement with the building control body." (locator section `1`, paragraph `1.11` for both); `live determinations using them 0`. No `extraction_relations` row names either (`select * from extraction_relations where from_extraction_id in (189,190) or to_extraction_id in (189,190)` printed `[]`). (Six other numerical rows with no comparator are `figure_role = 'finding'`, not claims; T-016's rule does not ask a comparator of them, and they are not this task's.)

If the output differs, the ground has moved: stop (section 9).

## 4. The change

1. **Read each row's passage in the held text** of `REF-00992` (the file named in the retrieval manifest that holds it: `grep -l 'REF-00992' retrieval-log/*/manifest.jsonl`; open the file it names, at the row's locator). Never decide from the row's `claim_text` alone, and never from memory.
2. **Decide the comparator** from the passage, from the column's vocabulary (`dbcore.check_values` of `source_value_extractions.comparator`; on 2026-11-13 `=`, `<`, `<=`, `>`, `>=`, `between`, `approx`). The sibling claims of the same source and parameter (`select extraction_id, comparator, claimed_value, claim_text from source_value_extractions where ref_id='REF-00992' and parameter_id=4`) show how the same document's other widths were read; they inform, they do not decide.
3. **Write it** with `db.py amend-extraction --extraction-id N --field comparator --value '<value>' --reason '<the passage words that decide it, with the locator>' --session "$STEM"`.
4. **The condition in 190** ("on restricted sites, subject to agreement with the building control body") is not this task's to encode: if no `condition_on` relation already records it (`select * from extraction_relations where from_extraction_id=190 or to_extraction_id=190`), list it in the pull request as owed to the conditions work (T-017's branches, T-108's repair) and leave it.
5. **If the passage does not let you decide** (a sufficiency statement that is neither a floor nor a value), do not write a comparator: list the row with the passage and the two readings, for the owner.

**Data migration.** Through `scripts/emit_data_migration.py` only; no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task changes no code. For each row you amend: `git grep -n -F -e 'extraction 189' -e 'extraction 190' -e 'extraction_id 189' -e 'extraction_id 190' -- governance architecture references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'`; a sentence your amendment makes false is corrected if it is research prose, or listed.

## 6. Verification

**Red before, green after.** Before: section 3's first line lists the two ids. After, on the migrated database: it lists none (or only a row left under item 5, with its reason in the pull request); every other column of each amended row is unchanged (compare the full row before and after).

**The gates, once each, after the migration is applied:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep
```
Confirm the batch was examined: `select count(*) from source_value_extractions where updated_by_session='<stem>'` is above 0 on the migrated database.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: give two stored code claims their comparator from the held text [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: each row, the passage and locator, the value chosen, and the reading rejected>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not change a value, unit, quote, role or lens of either row; amend the comparator only.
- Do not decide from memory or from the row's quote alone. Do not encode the condition of row 190 here.
- No tooling in this pull request (rule 10). Do not write `data/guidebook.db` except by the write path. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the evidence differs from section 3; the held text cannot be found or does not contain the passage; a live determination uses either row; `amend-extraction` refuses for a reason other than the value; the rebuild does not reproduce the database.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After: a data migration is immutable; a wrong comparator is corrected forward with `amend-extraction`.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `db.py record-adversarial-pass`, closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
