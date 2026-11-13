# T-071  Give every value-supplying figure its root

_One task, one pull request. Read `CLAUDE.md` first; beyond it this file is self-contained. Index, order and the owner decision register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`. Every number in this file was read on 2026-11-13 and is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Authored 2026-11-13 (Opus-class, cluster B). Its evidence command was run read-only on 2026-11-13 and printed what section 3 states. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-071 |
| Title | Give every value-supplying figure its root |
| Wave | research |
| Layer (CLAUDE.md §3) | 3 |
| Kind | **RESEARCH** (CLAUDE.md rule 10: tooling and research never share a pull request) |
| Executor | NOT FOR SONNET: whether a grey or clinical figure is its own measurement, an echo of a code, or traced to a cited study is read from each source's methods and citations |
| Traces to | prior workplan D-7 (`grep -n '^| D-7 ' workplan/2026-10-23-pipeline-resolution-workplan.md`; the report: `sed -n '/^### D-7 roots/,/^### D-8/p' scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md`); OR-19 (`grep -n -F 'OR-19: "Yes, presume an echo"' references/project-standards.md`); OR-20 (`grep -n -F "OR-20: \"No — We don't need to mine backwards for T4 to T6" references/project-standards.md`); the 2026-09-13 ruling on grey literature (`grep -n -F 'Do not count a grey source as an independent root on value agreement alone' references/project-standards.md`); OI-52 |

## 2. Preconditions

- **The integration base.** This workplan must be on the branch you start from. If the workplan's pull request is merged, that is `origin/main`. Until then it is the workplan branch, `origin/ccr-408aaa9b-z3e4s0` (if that name is gone: `git branch -r --contains "$(git log --all --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md)"`).
- **Tasks that must be merged to the integration base first:** T-048 merged (the root registry's writer, for a root that is not an admitted source). Check by running that task's own after-test (its section 6), or `git log "$BASE" --oneline | grep -F 'task/t-048'`. **Pointing an existing figure at a registered root also needs `root_id` to be amendable**, and today it is not (`grep -n -A3 '_AMENDABLE_SVE_FIELDS = ' scripts/db.py` lists `root_type` and `root_ref_id`, not `root_id`); T-048 adds it since the fold of 2026-11-13 (its section 4 item 4, OI-57 (7)). If `root_id` is still absent from that set on `$BASE`, do step 4 for no figure: register nothing, list each figure that needs an external root, and file the writer gap (`db.py add-gap`), never hand SQL (rule 10).
- **Owner decisions:** none in the register. Rulings: OR-19 (a grey source repeating a code's value is presumed to echo it, rebuttably, and is not re-tiered) and OR-20 (T4 to T6 are not mined backward; what a regulation states as its own rule is accepted as given). The readings in section 4 that are this file's, not the owner's, are marked Chosen and listed in the pull request for the owner (OR-17's spirit: the owner reads the pull request).
- **Tests that must be red before you start:** section 6's count of value-supplying figures with no root is above 0.
- **Set-up.**

```
cd /home/user/guidebook
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
git switch -c task/t-071-regrade-roots "$BASE"
STEM=session_$(date -u +%Y-%m-%d)-<slug>
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-071" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/s.db" && cp data/guidebook.db "$SCRATCH/t.db"
```
- **Shell variables do not survive between tool calls.** Set `BASE`, `STEM` and `SCRATCH` again at the top of every block.
- **Real execution:** `/session-open`, then `/orient`; follow `skills/run-pipeline_SKILL.md`. **Pilot or dry run:** work on the scratch copy only and stop before the write path.
- Work only on the scratch copy: `GUIDEBOOK_DB_PATH="$SCRATCH/s.db" python3 scripts/db.py <verb> ... --session "$STEM"`. Land the rows only by the write path:
```
python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH/s.db" --out "$SCRATCH/batch.sql"
python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<what the batch is>" --input "$SCRATCH/batch.sql"
python3 scripts/migrate_db.py
python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"      # must exit 0
```

## 3. The problem, in the guidebook's terms

Evidence counts roots, not documents (`governance/evidence-architecture.md` §4.5). A figure with no root type can neither count as an independent measurement nor be shown to be an echo, so the independence count reads only part of the evidence, and a grey report that repeats a code is indistinguishable from fieldwork. Most value-supplying figures carry no root: the codes' own rules, recorded before the convention, and a few grey and clinical figures.

**Evidence command** (read-only):

```
python3 -I - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
print("no root or untraced, by tier, role, root_type:", c.execute("select e.tier, x.figure_role, coalesce(x.root_type,'NULL'), count(*) from source_value_extractions x join evidence_sources e using(ref_id) where x.root_type is null or x.root_type='untraced' group by 1,2,3 order by 1,2,3").fetchall())
print("the convention already used for codes (tier 6 rows with a root):", c.execute("select x.root_type, x.root_ref_id = x.ref_id, count(*) from source_value_extractions x join evidence_sources e using(ref_id) where e.tier=6 and x.root_type is not null group by 1,2").fetchall())
print("root_id set on any row:", c.execute("select count(*) from source_value_extractions where root_id is not null").fetchone()[0], "| registry rows:", c.execute("select count(*) from external_root_registry").fetchone()[0])
PY
grep -n -A3 '_AMENDABLE_SVE_FIELDS = ' scripts/db.py
```

**Expected output today** (2026-11-13): value-supplying (`claim`) figures with no root at tiers 3, 4, 5 and 6, most of them tier 6; `untraced` claims at tiers 3 and 5; many `condition` and `finding` rows with no root; tier 6 rows that do carry a root are all `committee_assertion`, nearly all rooted to themselves (21 of 26) and a few to another source; no `root_id` and an empty registry; the amendable set without `root_id`.

## 4. The change

Order of preference, from CLAUDE.md §8. Every verb this task needs exists (`amend-extraction --field root_type|root_ref_id`, and T-048's `add-root`); it adds no code.

1. **The subject: value-supplying figures only** (`figure_role IN ('claim','derived')`) whose `root_type` is NULL or `untraced`. **Chosen (authoring 2026-11-13).** Rejected: every row with no root, as the report wrote it. A `condition` row (the slope a treadmill was set to) and a `finding` row (a study's result, often an absence) are not values a cell composes, and `v_value_independence` already counts the roots of such rows alongside claims (T-068 section 3 reports the gap that makes: 14 roots for parameter 3 counted over all rows, 3 over value-supplying rows). Giving them roots now would widen that gap before the owner has seen it. List the condition and finding rows with no root in the pull request by command; do not change them.
2. **Tier 4 to 6, the regulatory stratum (OR-20).** The stratum is derived, never listed: a figure is in it when its source's `(evidence_type, scope)` is one of `db._regulatory_pairs()` (`python3 -c "import sys;sys.path.insert(0,'scripts');import db;print(sorted(db._regulatory_pairs()))"`). For each such figure: `amend-extraction --extraction-id N --field root_type --value committee_assertion --reason "OR-20: a regulation's own rule is accepted as given; not traced backward" --session "$STEM"`, then `--field root_ref_id --value <the figure's own ref_id>` with the same reason. **Chosen: `committee_assertion` rooted to itself**, the shape most tier-6 rows already carry (section 3). Rejected: `untraced`, which says a trace is owed when OR-20 says none is wanted; and rooting a code to an older code it cites, which is the backward mining OR-20 declines. A figure already rooted to another source is left as it is (OR-20 does not unwind recorded provenance). Both rejected readings and the chosen one are named in the pull request: the effect on the guidebook is nil today (neither `committee_assertion` nor `untraced` counts as an independent root), and the owner may correct the reading.
3. **Tier 1 to 3, read from the source.** For each remaining figure, open the source's derived text (or its held bytes) and record what its methods and citations show, each with `amend-extraction` and a `--reason` that quotes or locates the passage:
   - the source measured or observed it itself: `measurement_primary`, rooted to itself;
   - a Co-1 source whose disabled co-producers generated it: `participatory_finding`, rooted to itself (CLAUDE.md §6: the co-production is the warrant; never record it as anything less);
   - it is computed from other figures: `derived_calculation`, rooted to the source of the inputs if it is held, else left for step 4;
   - it cites an admitted source for the figure: rooted to that `ref_id`, with that source's root type;
   - **a grey figure whose value equals a code figure of the same parameter and jurisdiction, with no recorded independent measurement (OR-19, presumed echo):** `committee_assertion`, rooted to that code's `ref_id`. Find the coincidence by query (same `parameter_id`, same source jurisdiction, the bound read with `dbcore.bound_on_scale` equal), never by eye. The source is **not re-tiered**. The presumption is rebutted only by the source's own account of measuring it, which then gives `measurement_primary`.
   - **a figure the source itself marks as a code's** ("Code (required)", "as required by the building code"; added 2026-11-13 by the fold of the Edmonton case study, ADJUDICATION P2): this is the source's own root attribution, not a property of the figure. Root it to the code's `ref_id` with `committee_assertion` when the code is held; else leave or set `untraced`, and say in the `--reason` the words of the marking and that the code is not held (`root_classification_basis` is not amendable: `grep -n -A3 '_AMENDABLE_SVE_FIELDS = ' scripts/db.py`; a figure written after T-035 carries the sentence there instead). Either way it supplies no independent root (OR-19). The source's own pairing of a higher figure with that code figure is an `extraction_relations` edge (`relate-extraction`), written in this batch only where both rows exist and the edge is missing; never a label, and no figure is recorded as "best practice".
   - none of these can be shown from the source: leave `untraced` (or set it) with a reason saying what was read.
4. **External roots** (only if `root_id` is amendable on `$BASE`, section 2): a figure whose root is a study or dataset that is not an admitted source: register it once with T-048's `add-root` (its flags as T-048 built them; read `python3 scripts/db.py add-root --help`), then point the figure at it. One root, one registry row: check the registry by description before adding (the writer refuses a duplicate). Otherwise list these figures and file the gap.
5. **Never write a root type or a pointer you have not read the warrant for.** A figure you could not read is listed, not guessed.

**What reads what this task changes:** `v_value_independence` (and T-068's `v_value_independence_rows` once merged), `v_unregistered_roots`, the engine's convergence (T-068), the render's convergence sentence.

**Data migration.** Rows land through `scripts/emit_data_migration.py` only. The pull request contains no schema migration and no file under `scripts/` other than that one `scripts/migrations/data_*` file.

## 5. Caller sweep

A research task changes no code. For prose that restates a fact your rows change (rule 7a), search for sentences that state root counts or call the corpus's roots unrecorded:
```
git grep -n -i -e 'independent root' -e 'root_type' -e 'untraced' -- governance architecture references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
`governance/evidence-architecture.md` §4.5's dated BUILD STATE note says no determination may cite root-independence until rows exist; your rows do not change that sentence's truth (it is dated). A sentence stating a count is a caller: replace the count with the command (rule 7a), or stop if the sentence is doctrine.

## 6. Verification

**Red before, green after.**
```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from source_value_extractions where figure_role in ('claim','derived') and root_type is null\").fetchone()[0], c.execute('select count(*) from v_unregistered_roots').fetchone()[0], c.execute('select * from v_value_independence').fetchall())"
```
Before: the first figure is above 0. After (on the migrated database): the first figure is 0, or every remaining row is listed in the pull request with what was read and why no root could be shown; `v_unregistered_roots` is 0 (a figure rooted to an unregistered `root_id` is a defect this task must not create); the change in `v_value_independence` is reported, before and after, with the figures that moved it. Every amendment's `--reason` is non-empty (the writer refuses otherwise).

**The gates, once each:**
```
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1)
python3 scripts/audit/research_batch_dod.py --session "$STEM" > "$SCRATCH/dod.txt" 2>&1; echo "rc=$?"; grep -E 'EXAMINED|BLOCKED|PASS|FAIL' "$SCRATCH/dod.txt" | tail -8
scripts/preflight.sh --base "$BASE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
python3 scripts/audit/migration_reproducibility.py --deep      # every amendment is an UPDATE, invisible to the count-only check
```
Proof each gate examined something: `source_value_extractions` rows with `updated_by_session = "$STEM"` above 0 after the migration. `research_dod_session` is red by construction on a batch that searches and admits nothing (OI-55 (1)): report its lines and say so.

## 7. Commit

```
git add -A . ':!transcripts' ':!*commands.jsonl'
git commit -m "run-pipeline: record the root of every value-supplying figure (D-7, OR-19, OR-20) [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: the rule applied per stratum, the presumed echoes found by query, the rows left and why, v_value_independence before and after>" -m "<the attribution trailers your own session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db` directly; do not hand-write SQL against `source_value_extractions` or `external_root_registry`.
- Do not re-tier a source (OR-19). Do not mine a T4 to T6 source backward (OR-20). Do not record a Co-1 figure as anything but `participatory_finding` when its co-producers generated it.
- Do not change `claimed_value`, `claim_text` or any field other than `root_type`, `root_ref_id` (and `root_id` if section 2 allows).
- Do not give roots to `condition` or `finding` rows in this batch.
- Do not put tooling in this pull request (rule 10): the `root_id` gap is filed, not patched. Do not decide doctrine. Do not run `run_checks.py --all`, `bootstrap.sh`, or `pip install -r requirements.txt`. Do not push to `main`, rebase or force-push. Do not subscribe to pull-request activity.
- Do not hand-type a count; write the command.

## 9. Stop conditions

Stop and report when: a precondition is not met; section 3's output differs in shape (no value-supplying figure without a root); a figure's source cannot be read and its stratum is not regulatory (list it; do not guess); the writer refuses an amendment you would have to work around; `v_unregistered_roots` is above 0 after your rows; you would have to guess a value, a root or an owner's intent.

## 10. Rollback

Before the migration is applied: delete the scratch copy. After it is committed: correct a wrong root with a further `amend-extraction` in a compensating batch; never edit the data migration.

## 11. Adversarial pass and pull request

Real execution only. `/adversarial` once (recorded with `record-adversarial-pass`, closed with `close-adversarial-pass`); `/batch-done`; push; open the pull request last, once; call `unsubscribe_pr_activity` at once; push nothing afterwards except a deliberate change.
