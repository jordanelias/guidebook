# T-012 pilot report: follow-up reasons for a skimmed figure and an absence finding

**Pilot, not real execution.** `/session-open` not run, `scratchpad/CURRENT` untouched, stayed on branch `pilot-T-012` in a clone, one local commit, nothing pushed.

- **Base commit:** `d0952279b2c741406793bb86cfad57e586a7c80e` (`origin/claude/peaceful-noether-kvf3sf`). I overrode the file's BASE line (which picks `origin/ccr-408aaa9b-z3e4s0` or `origin/main`) because the brief says the branch tip is the base and local `main` is stale.
- **Canonical DB sha256** before and after: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` (equal). The migration was applied only to the clone's copy.
- **Outcome: PILOTED.** Red before, green after.

## Held / not held
1. Followed only CLAUDE.md and the task file (plus the brief and the baseline file the brief names): **held**.
2. Evidence command printed what the file says: **held**. Printed `reason              TEXT    NOT NULL CHECK (reason IN ('read-outside-admitting-purpose')),`. The file writes it as `reason TEXT NOT NULL ...` and adds "spacing as stored"; the regex returns the stored multi-space form, so a literal string comparison against the file's text would differ (minor).
3. Red before, green after: **held**.
   - Step 2 before: `raise-follow-up --reason skimmed-needs-full-read` is refused by argparse: `invalid choice ... (choose from 'read-outside-admitting-purpose')`. It is a usage error (exit 2), not a Refusal. After, on a migrated copy: it writes follow_up_id 1 and `resolve-follow-up` closes it (both rc 0).
   - New test cases `T012-01` and `T012-02` in `scripts/tests/test_scan_contract.py`. Prefix was free (`grep -c '"T012-'` printed 0). Shown RED on the unmigrated database (the test copies `data/guidebook.db`: both ✗, 117/121) and GREEN on the migrated one (119/121, the remaining 2 are baseline G01/G02).
4. Gate ran: **held, with one re-run.** The first gate run (`$SCRATCH/gate1.txt`) showed `context_map_fresh` FAIL (STALE) caused by my change; I regenerated it and ran the gate again (the file's section 6 allows a re-run if a file changes afterwards). Final gate: `RESULT: PASS — 60 check(s) green, 4 nothing-in-scope, 11 advisory failure(s)`; `PREFLIGHT: PASS`; `SELFTEST: PASS`. NOTHING-IN-SCOPE: extraction_follow_up_audit, citation_mining_session, adversarial_pass_recorded, medical_lens_integrity. No blocking FAIL. Advisory FAILs: see below. Every named check's `EXAMINED:` was read (table).
5. Patch and report saved: **held** (`T-012.patch` was verified to `git am` cleanly onto the base and reproduce the migrated database byte for byte).

## Migration
- Derived number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` gave `125_alias_observation_pointer.sql`, so `126_extraction_follow_up_reasons.sql`, ending `PRAGMA user_version = 126;`.
- Create / copy / drop / rename; recreates `ux_extraction_follow_ups_open`; preserves the AUTOINCREMENT floor via a temp table (the 114 recipe). Proven on a seeded copy (3 rows inserted, 1 deleted: sqlite_sequence stays 3, ids 1 and 2 kept).
- `select type,name from sqlite_master where sql like '%extraction_follow_ups%'` gave the table and the one index only: no view or trigger.
- No `AFTER_DATA` marker: no committed data migration touches the table and 125's marker precedes it. Not mentioned in the file (see defects).
- `joined_cells_census.py` last line before and after: `EXAMINED: 457 text column(s) with data; 66 candidate(s)` (identical).
- `migrate_db.py --rebuild` rc 0 ("Rebuilt ... successfully"). `migration_reproducibility.py --deep`: `EXAMINED: 57`, `EXAMINED: 56`, `VERDICT: PASS`.

## Check-by-check, before and after
No check that was green went red; the failing-case diffs were empty for all twelve.

| check | before | after |
|---|---|---|
| test_run_pipeline_refusals | rc0, EXAMINED 175 cases | same |
| test_db_amend_writers | rc0, EXAMINED 161 | same |
| test_scan_contract | rc1, EXAMINED 119, 117/119, G01 G02 fail (baseline) | rc1, EXAMINED 121, 119/121, same G01 G02 (+2 = my cases) |
| test_author_presence | rc0 (prints per-case EXAMINED, no summary line) | same |
| test_search_log_completeness | rc0, EXAMINED 23 | same |
| test_assess_cell_pilot | rc0, **no EXAMINED line** | same, examined nothing visible |
| test_validate_evidence_state_2_4 | rc0, **no EXAMINED line** | same |
| extraction_follow_up_audit | rc0, **EXAMINED: 0** | same, EXAMINED: 0 (vacuous: no follow-ups, no live determinations) |
| migration_reproducibility | rc0, EXAMINED 57, PASS | same |
| schema_reference_audit | rc0, EXAMINED 1125 | same |
| test_db_integrity | rc0, 56/56, EXAMINED 3659 | same (10 passed having examined nothing, same list) |
| column_vocabulary_audit | rc0, EXAMINED 56 tables | same |

Gate advisory FAILs (all pre-existing, none from this diff): scan_debt, verified_scan_integrity, research_protocol_audit, metadata_integrity_audit (each run on the stashed base and mine: same rc 1, same output), validate_schema_cross_check, retired_vocabulary, research_dod, skill_vocabulary_audit, test_scan_contract (G01/G02) (baseline file); search_log_completeness (passes standalone rc 0; fails in the gate on 4 unlogged WebSearch ledger lines of the coordinating session); research_tooling_separation (see defect 3).

## Sweep
Ran the four sweep commands for both names, plus `build_graph.py --check`.
- `extraction_follow_ups`: code hits `extraction_follow_up_audit.py`, `db.py`, `test_scan_contract.py`; skills `run-pipeline_SKILL.md` (lines 194, 334). All are mentions or already read the CHECK: `db.py` uses `dbcore.schema_choices(...)` and `check_declared`, so nothing typed to change. `run-pipeline_SKILL.md:194` ("its `--reason` vocabulary is `extraction_follow_ups.reason` ... a doubt it cannot name is a GAP") stays true. The audit prints `reason` and hard-codes none. Test file: U03 (`a-new-reason`) still refused; the `read-outside-admitting-purpose` hits are fixtures, still true. Views/indexes: table plus `ux_extraction_follow_ups_open`. Registry: `[]` for both names. Prose: `governance/context-map.yaml`, `owner-browser.yaml`, `stage-map.yaml` are mentions, **except** `context-map.yaml`'s generated header (`schema_version`, `db_fingerprint`), which my change made stale. That is a caller (the registry check `context_map_fresh`); repaired with `python3 scripts/generate/context_map.py` (2 lines).
- `read-outside-admitting-purpose`: only test fixtures; mentions.
- `build_graph.py --check`: **rc 1, 109 failures, 5 warnings ("quote found ... but not near cited line N")**. Identical on the stashed unchanged base (`109 failure(s), 5 warning(s)`), so not this change's. I did not need it (no verb, table, view or refusal text was added, removed or renamed; only a CHECK was widened).
- Zero-row objects: no view/trigger exists to prove; the table itself holds 0 rows today, so the rebuild copy step moved nothing in the real DB. The seeded-copy test is what proves the copy and the sequence floor.

## Code size
`git diff --cached --shortstat <merge-base> -- scripts schemas .github skills ':!scripts/migrations'` → ` 1 file changed, 20 insertions(+)` (all the test file). The migration is outside that count (62 lines). Reads: `raise-follow-up` / `resolve-follow-up` (via the CHECK), `extraction_follow_up_audit`. Replaces or makes deletable: nothing. Whole commit: 4 files (also `data/guidebook.db` binary and `governance/context-map.yaml`).

## Task-file defects
Seven, in order of cost.

1. **The sweep misses the generated context map; the file's own gate goes red on it.** Widening a CHECK changes `PRAGMA user_version` and the DB fingerprint, so `context_map_fresh` (advisory) printed `STALE: governance/context-map.yaml differs from a fresh generation. Run: python3 scripts/generate/context_map.py`. It is fresh on the unchanged base (`EXAMINED: 1 context map (1741 lines) — fresh against HEAD and the live DB`). The file never says to regenerate it, and the "run the gate once" rule means a naive executor either ships a stale map or runs the gate twice. Fix: section 4 should say "after the migration, run `python3 scripts/generate/context_map.py` and commit the 2-line result" (every migration task needs this).
2. **Section 4's "What reads what" claims the engine "leaves out a figure under an open follow-up". It does not.** `git grep -n -i -e follow_up -e follow-up -- scripts/assess scripts/dbcore.py` finds nothing in the engine; it leaves out `extraction_method = 'skim'` (`dbcore.NOT_PUBLISHABLE_METHODS`). The thing that fails a live determination on an open follow-up is `extraction_follow_up_audit` (advisory, `EXAMINED: 0` today). The reader list is wrong, and an executor looking for the engine to check or change has nothing to find. Also migration 105's own header says "Skimmed figures need no follow-up row: the typed column extraction_method = 'skim' already says it"; the file does not tell the executor that the new `skimmed-needs-full-read` reason overlaps that (a row can be skim AND carry the follow-up) or that the 105 comment is now false. It is immutable so cannot be fixed; one sentence in the file would have settled it.
3. **The gate cannot be read at face value for `research_tooling_separation`.** The registry cmd takes no base, so it diffs against `origin/main` (stale locally) instead of the `--base` that `preflight.sh` was given. In the gate it printed `VERDICT: FAIL — this changeset carries both research data and tooling`, listing 737 paths with `scripts/validate_parameters.py` etc. that this change never touched. With the right base: `python3 scripts/audit/research_tooling_separation.py --base origin/claude/peaceful-noether-kvf3sf` → `EXAMINED: 3 ... VERDICT: PASS`. On the unchanged base with the default it still gives FAIL (`EXAMINED: 736`). The file's section 6 step 4 says to read only `RESULT`, NOTHING-IN-SCOPE and blocking FAILs, so this advisory FAIL is not actionable as written; the file should say it is a stale-base artefact until the workplan is merged, or the check should accept `$BASE`.
4. **The gate takes more than 120 seconds** (first run ~2.5 minutes, 316 lines; `test_run_pipeline_refusals` 41 s, `retired_vocabulary` 17 s). In a harness with a 120 s foreground limit it is silently moved to the background; the file's one-line command prints `rc=` and the grep only when it finishes. The file should say "run it in the background and wait".
5. **The "baseline red" set is incomplete in the pilot baseline file and in the file's prose.** The file names only `test_scan_contract` G01/G02 and `retired_vocabulary` as pre-existing. The gate also shows scan_debt, verified_scan_integrity, research_protocol_audit, metadata_integrity_audit, search_log_completeness and research_tooling_separation FAIL, all advisory. I verified four by running them on the stashed base (same rc and output) and one passes standalone. A less careful executor would have to prove each is not theirs; the file should list the advisory red set or tell the executor to compare to a base gate run.
6. **Migration instructions are silent on three things I had to decide:** (a) whether to put an `AFTER_DATA` marker (I did not: no data migration touches the table, 125's marker already precedes); (b) preserving the AUTOINCREMENT floor (the recipe lives only inside migration 114; the file points to no example); (c) the committed `data/guidebook.db` binary: "Apply it only with `python3 scripts/migrate_db.py`" changes the tracked database, and `format-patch -1 --stdout` (the brief's form) omits binary content unless `--binary` is given. I used `--binary`; the patch applies and reproduces the DB byte for byte.
7. **Smaller:** (a) Step 2 types `--extraction-id 11`, an id, which the same file forbids in tests ("Never type into a test an id ... the database can derive"); fine for a one-off probe, but the file should say so, or pick it by query. 11 is a skim extraction today; it is a valid foreign key and nothing more. (b) The before-run `rc=` shown in step 2 is hidden by any pipe; argparse's refusal is exit 2 and a usage error, not the Refusal-style message the other cases use, so "is refused" means two different things. (c) The file says `test_assess_cell_pilot` and `test_validate_evidence_state_2_4` are read for `EXAMINED:`; both print none, so the instruction "a check that prints no EXAMINED: line examined nothing" leaves them as unverifiable. (d) Section 5's hit list says `skills/run-pipeline_SKILL.md` for the first name; the live grep also matches line 334 (second use); trivially covered. (e) `test_author_presence` prints per-case `EXAMINED` text but no summary line.
