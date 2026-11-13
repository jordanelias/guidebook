# T-084  The language-and-jurisdiction map names only declared jurisdictions

> **HELD** — waits for the owner's answer to OI-55 (4): whether the jurisdiction codes the map holds and the registry lacks are admitted to the registry (and how their pairs are scoped), or their pairs are withdrawn. An executor that opens this file before the answer is in the ledger in the owner's words does not start it: it reports that the task is waiting, and for what.

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Source: `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` rows OI-56 ("the foreign key on `lang_jur_map.jurisdiction` (after OI-55 (4))") and OI-55 (4); T-024's pilot report, defect 1 (`grep -n 'impossible as written' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-024-report.md`). Every number in this file was read on 2026-11-13 on commit `66a5ba8a` and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-084 |
| Title | The language-and-jurisdiction map names only declared jurisdictions |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request; the rows are base rows landed by a data migration) |
| Executor | Sonnet-class, once the owner has answered (every step is then mechanical from the answer) |
| Traces to | OI-55 (4); AT-58 ("every jurisdiction in `lang_jur_map` resolves in the vocabulary the writers read", `grep -n 'AT-58' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md`); T-085 (the foreign key, which needs this first) |

## 2. Preconditions

- **The integration base.** `origin/main` once the workplan's pull request is merged, otherwise the remote branch carrying the newest commit to this folder (the set-up block's first line finds it).
- **Tasks that must be merged to the integration base first:** T-025 merged (its `set-pair-scope` writes a pair's `scope_status` with an approval pointer). Check: `git grep -c '"set-pair-scope"' -- scripts/db.py` prints 1 or more. (T-024's `add-jurisdiction` is merged on 2026-11-13.)
- **Owner decisions:** OD-46 (OI-55 (4)), OPEN (registered 2026-11-13, not yet asked). **The question, as OI-55 records it:** the codes `lang_jur_map` holds that `base_jurisdictions` lacks: "admit as declared out-of-scope codes or remove their pairs". What it rests on: T-024's ruling that admitting such a code "is the owner's decision on scope" (`grep -n -F "is the owner's decision on scope" workplan/2026-11-12-bidirectional-pipeline/tasks/T-024-jurisdiction-registry.md`); jurisdiction scope is doctrine the owner holds (CLAUDE.md §8); the owner's "retire in place then" (`grep -n -F 'retire in place then' references/project-standards.md`), under which "remove their pairs" would be a delete the owner rules on case by case. Also OI-55 (1) (how a carry-only research batch is gated) applies: this batch searches nothing and admits no source.
- **Tests that must be red before you start:** AT-58: section 3's command prints a non-empty list.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-084-unregistered-map-codes "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-unregistered-map-codes
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-084" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db"
```
- Shell variables do not survive between tool calls: set `BASE`, `STEM` and `SCRATCH` again in every block. **Real execution:** `/session-open`, then `/orient`. **Pilot:** skip `/session-open`, stay on the given branch, stop before the write path.
- Every call points at the scratch copy inline (`GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py … --session "$STEM"`); rows land only by `emit_batch_sql.py` → `emit_data_migration.py --session "$STEM.md"` → `migrate_db.py` → `migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0), as CLAUDE.md §4 says.

## 3. The problem, in the guidebook's terms

The map of which languages are researched for which jurisdiction names jurisdictions the registry has never declared. A search or a determination can carry only a declared code, so those pairs are research the pipeline can owe but never record; and the foreign key that would keep the map and the registry in step cannot be added while they disagree.

**Evidence command** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select l.jurisdiction, count(*), group_concat(l.language), group_concat(coalesce(l.scope_status,\"-\")) from lang_jur_map l left join base_jurisdictions b on b.jurisdiction_code=l.jurisdiction where b.jurisdiction_code is null group by 1 order by 1').fetchall())"
```

**Output on 2026-11-13:** one row per undeclared code, and the codes are `AR, AT, CL, CO, CR, CY, EC, ET, GH, GT, MA, MX, PE, PH, TH, TZ, UY` (`select count(distinct …)` of the same join printed 17, over 19 pairs).

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Apply the owner's answer, and only it:
- **If the answer admits the codes:** for each code the command prints, `db.py add-jurisdiction --code C --kind <the kind the answer gives; country unless it says otherwise> --approval-ref "<the ledger heading that holds the answer, exactly>" --session "$STEM"`; then, if the answer scopes their pairs, `db.py set-pair-scope --language L --jurisdiction C --scope-status <the value the answer gives> --approval-ref "<same heading>" --session "$STEM"` for each pair the command prints. The verbs refuse an approval pointer that is not exactly one `## ` heading of the ledger.
- **If the answer withdraws the pairs:** no sanctioned verb removes a `lang_jur_map` row, and `lang_jur_map` is not in `dbcore.deletable_tables` (`python3 -I -c "import sys;sys.path.insert(0,'scripts');import dbcore,sqlite3;print('lang_jur_map' in dbcore.deletable_tables(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)))"`). Stop and report: the withdrawal needs a tooling task first (a retire-in-place path for a pair, or the owner's recorded exception to retire-in-place), which the coordinator files.
- **A mixed answer** (some codes admitted, some withdrawn) is applied code by code under the two rules above.

**Data migration.** Through `scripts/emit_data_migration.py` only; no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task changes no code. For each code you admit or whose pair you scope, `git grep -n -w -e "<code>" -- governance/jurisdiction-philosophy.md governance architecture references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log' | head` and read whether a sentence lists the declared jurisdictions or says this code is undeclared; correct research prose, list the rest.

## 6. Verification

**Red before, green after.** Before: section 3's command prints the codes. After, on the migrated database: it prints `[]` (or only codes the answer withdrew, if that path was stopped). `python3 scripts/audit/jurisdiction_db_vocabulary.py` is green before and after (record its `EXAMINED:`).

**The gates, once each, after the migration is applied:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep
```
Confirm the batch was examined: `select count(*) from base_jurisdictions where created_by_session='<stem>'` (and, for scoped pairs, `select count(*) from lang_jur_map where updated_by_session='<stem>'` if the table has that column on the day) is above 0.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "jurisdiction-tracker: declare the map's undeclared jurisdictions per the owner's answer [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the owner's answer quoted with its ledger heading; each code and pair and what was done>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not start before the owner's answer is in the ledger in the owner's words.
- Do not delete a `lang_jur_map` row by any route. Do not add the foreign key (T-085).
- No tooling in this pull request (rule 10). Do not write `data/guidebook.db` except by the write path. Do not run `run_checks.py --all`, `bootstrap.sh` or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push; do not subscribe to pull-request activity.

## 9. Stop conditions

Stop and report when: the owner's answer is absent or would need a verb that does not exist; T-025 is not merged; the evidence differs from section 3; a verb refuses for a reason other than an argument; the rebuild does not reproduce the database.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After: a data migration is immutable; correct forward through the same verbs.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `db.py record-adversarial-pass`, closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once, against the integration base; call `unsubscribe_pr_activity` for it immediately; push nothing afterwards except a deliberate change, never `[skip ci]` on the final push.
