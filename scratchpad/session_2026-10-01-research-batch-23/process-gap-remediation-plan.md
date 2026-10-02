# Process-gap remediation plan — research batch 23 (PR #166)

Generated 2026-10-01 against HEAD `a485c6b` on `ccr-55d11bad-yxa6e4` (`git rev-list --count origin/main..HEAD` → 5 ahead of `origin/main` = `464eb31`). Every figure sits beside the command that computes it. Re-run the command rather than trusting the figure (CLAUDE.md rule 7a). All database reads use `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`. `/tmp/claude-0/main.db` is a copy of main's database. This plan reconciles Report A (GAP-055, -058, -059, -060, -061) and Report B (I1–I10).

---

## 1. Verdict and shape

Four new tooling PRs (one conditional), plus the existing research PR #166 and the batch-24 pilot. **T1** adds the writer verbs and migration 101. **#166** then carries batch 23's owed judgement and repairs, written through T1's verbs. **T2** adds contract rule R16 and the R5, R7 and R8 changes, and corrects the prose. **T3** adds the tool-call ledger. **T4**, the two-phase search log, ships only if T3 proves out.

The order is T1 → #166 → T2 → batch 24. T3 runs in parallel. T4 waits for a searching batch run with T3 live.

This order means no blocking check turns red on main at any merge:
- D04 clears inside #166.
- R16 lands only after the session that `sessions/LATEST-RESEARCH` names has paid its R16 debt.

No data rides in a tooling PR, and no verb is used before it is on main.

---

## 2. Corrections to the earlier draft

**Corrections the orchestrator required:**

1. [CORRECTION: draft A3 said `decline-parameter` was optional ("ship only if the report proves noisy") — it is required, and it ships in T1, before the gate.] The terms R16 must dispose of include concepts that are not design parameters: `select distinct a.term_id, t.canonical_en from term_adjudications a join terms t using(term_id) where not exists (select 1 from base_parameters p where p.term_id=a.term_id)` → TERM-016 wheelchair user, TERM-053, TERM-075, TERM-079, TERM-089 ramp, TERM-090..094. Without a disposition, R16 is red forever on these terms, and the gate cannot land green on main (§4).
2. [CORRECTION: the draft's Package B included a GAP-059 writer (`amend-candidate --set-harm-finding`) — cut.] `search_candidates.harm_finding` has no reader outside `db.py` and adversarial lens S1. Check with `git grep -l harm_finding -- scripts ':(exclude)scripts/migrations'`: the hits other than `db.py` read `search_executions.harm_finding` or a test fixture. No view reads it: `select name from sqlite_master where type='view' and sql like '%harm_finding%'` → none. The harm did reach exec 171, where R7 and S1 read it. GAP-059 is closed `CLOSED-DECIDED` in #166, with the reason recorded in the session record. Report A left it OPEN, which would make it a gap that can never go green.
3. [CORRECTION: the draft's GAP-055 remedy was "a finding-amendment path" — ruled out.] The owner ruling of 2026-09-27 says "Do not build `amend-adversarial-finding`": `grep -n 'amend-adversarial-finding' references/project-standards.md` → L4188, L4225. The same ruling names the artefact-shape mismatch for "the next tooling PR". The remedy is therefore WP4: the close-pass parse plus one line in the antagonist brief. Passes 1 and 2 stay open.
4. [CORRECTION: draft A4 added steps to `/session-open` and `/batch-done` — dropped in favour of the runbook.] `/batch-done` already runs the gate: `grep -n research_batch_dod .claude/commands/batch-done.md` → L9, L30. The structural cause of GAP-061 is the operative runbook. `workplan/2026-09-10-batch-06-runbook.md` Step 1 is "mint the parameter" (one parameter, before searching), and Step 4b says "EXTRACT what each source asserts for the parameter". WP13 rewrites Step 4b.
5. [CORRECTION: the session record §6 said `test_verification_pipeline` "fails on main and passes here; not examined why" — it fails on both, and the line is already corrected at `a485c6b`; no further edit to the record is needed.] Measured: `python3 scripts/tests/test_verification_pipeline.py >/dev/null 2>&1; echo $?` → 1. The same with `GUIDEBOOK_DB_PATH=/tmp/claude-0/main.db` → 1. Both runs report "15/18", with G01–G03 failing (corpus floors ≥50/≥30/≥100). The "passes here" came from a `--changed-from` run, which never selects `kinds: [tooling]` checks (`scripts/run_checks.py` `select()`, L192–198). The §6 line now in the record reads, and should keep reading:
   > `test_verification_pipeline` (15/18 on both databases: G01 to G03 assert corpus-size floors; `python3 scripts/tests/test_verification_pipeline.py; echo $?` exits 1 on this branch and, with `GUIDEBOOK_DB_PATH` set to main's DB, on main). An earlier version of this line said it failed on main and passed here. That was wrong: the diff-scoped run never selects `kinds: [tooling]` checks, and its absence from the failure list was read as a pass.

   Two further prose callers are stale or will be, and WP9 fixes both. The registry `note: 18/18 assertions.` is already wrong. The CLAUDE.md rule 7a sentence "`test_verification_pipeline` still asserts a corpus of ≥50/≥30/≥100" becomes false once G01–G03 are deleted.

**Corrections to the two reports and to the draft's sequence:**

6. [CORRECTION: Report A said "merge #166 now, D04 waived", then PR A, PR B and data PR C — #166 waits for T1 and absorbs PR C.] T1 carries migration 101 and the DB blob, so its CI is data-kind and runs `test_db_integrity` (blocking). If #166 merges first, T1 merges red on D04, a defect it is forbidden to fix (rule 10), and every data or schema PR stays red until PR C. Rule 10 does **not** require #166 to wait: #166 uses no new tooling. The hold is chosen to keep main green and to land batch 23's repair rows on batch 23's own PR. This is owner decision D1.
7. [CORRECTION: Report A scoped R16 to "adjudications this session wrote" — R16 and R16-adjudicate are both scoped to the batch's admissions, the scope R11-harvest already uses (`research_batch_dod.py` L721–730).] This makes the pointer gate examine batch 23's terms whichever session stamps the repair rows. It also makes a judgement-only pilot checkable through the batch whose sources it re-reads (§7).
8. [CORRECTION: Report A said batch 20 "must FAIL R16 (10 terms)" — 10 is the `--all` count; under admission scoping batch 20 names TERM-089 and TERM-094, and only TERM-094 after #166 declines TERM-089.] The query is in WP11.
9. [CORRECTION: Report A's pilot step 7 expected `research_batch_dod.py --session <pilot>` to be green — it cannot be.] A session with no searches and no admissions fails R1, R9a and R9b by design: `python3 scripts/audit/research_batch_dod.py --session session_2099-01-01-nothing` → NON-COMPLIANT on exactly those three rules. §7 redefines the pilot's gate.
10. [CORRECTION: the draft treated the baseline as a trap and kept R16 session-scoped only — there is no trap.] `--write-baseline` adds a new code (`merged[code] = n`, `research_batch_dod.py` L1107), and `check_baseline` prints `NEW` and passes (L262). The baseline must still be rewritten in T2, because the Stop hook runs `--all`.
11. [CORRECTION: Report B N8 would make `validate_schema.py --cross-check` one-directional and expected "both exit 0" — falsified; reclassified NO-ACTION.] `timeout 120 python3 scripts/validate_schema.py --cross-check | grep -c 'in the archive, absent'` → 17, all `GB / …` rows, against 37 issues in total. The archive spells the jurisdiction GB and the live table UK, so "archive ⊆ table" still fails 17 times. Report B's "3 archive-only GB leads" is also wrong.
12. [CORRECTION: Report B N7 normalised lead names with `re.sub('[^a-z0-9]','',lower())` — that erases non-Latin script.] Every Korean or Japanese standard name would fold to the empty string and collide. Use the Unicode-aware fold that D04 uses (`re.sub(r"\W","",s.casefold(),flags=re.UNICODE)`, `scripts/tests/test_db_integrity.py` `_norm_title`).
13. [CORRECTION: Report B N3 added a second PostToolUse object with matcher `Bash|WebSearch|WebFetch` — that logs every Bash call twice; the matcher is `WebSearch|WebFetch`.]
14. [CORRECTION: Report B gave `search_log_completeness` `min_items: 1` — that fails every session that ran no WebSearch, including the pilot; it takes `no_floor: session-scoped`.]
15. [CORRECTION: Report B said the harness classifier blocks agent edits to `.claude/settings.json` (citing CLAUDE.md §7) — §7's block is on `~/.claude/stop-hook-git-check.sh`.] `scripts/fix_stop_hook_loop.sh` header: "editing ~/.claude/ is refused here". The repo's `.claude/settings.json` was written by an agent at `611a975`. The owner's own `SessionStart[1]` now runs `fix_stop_hook_loop.sh`. Whether the harness lets an agent write `.claude/settings.json` today is unverified, and T2's `--write` faces the same question as T3 (D4).
16. [CORRECTION: Report B said "CUT" the R7 floor — NARROW instead: the floor goes and count-integrity predicates replace it.] `DR-2026-08-19` Step 4 restates the floor ("R7 floor: ≥1 candidate per 25 screened", L865). It is a prose caller, so T2 appends an amendment to it and updates `attestations/decisions_DR-2026-08-19-research-restart-operative-instrument.json` (rule 2).
17. [CORRECTION: Report B N1 said "do not blank `co1_provenance`" when a row leaves co1 — the text moves into the ledger, then the column is set NULL.] Only co1 rows carry the field: `select evidence_type, count(co1_provenance) from evidence_sources group by 1` → non-zero only for `co1`.

---

## 3. Issue register

Disposition key: BUILD, NARROW, CUT, OWNER-DECISION, NO-ACTION. The reason column is the §8 test: what wrong thing reaches the book without the change.

| Issue | Disposition | Where | §8 reason |
|---|---|---|---|
| GAP-061 (P1) no term → parameter promotion | BUILD | WP1 (T1), WP10 (#166), WP11/WP13 (T2), pilot | Every figure a source states for any concept other than parameter 3 is lost. `select parameter_id,count(*) from source_value_extractions group by 1` → `[(3,101)]`. |
| GAP-060 no supersede writer | BUILD | WP3 (T1), WP10 | A mirror counts as a second source in `assess_cell.gather_sources`. D04 (blocking) is red. The only alternative is hand SQL. `KNOWN_DUP_SOURCE_KEYS` is rejected: it is a curated list (rule 8) and leaves the mirror live. |
| GAP-058 add-source half-writes | BUILD | WP2 (T1) | A refused command leaves an orphan admission. It is either captured or hand-deleted, as batch 23 did (record §2.1a). |
| GAP-055 close-pass unsatisfiable | BUILD, narrowed to parse plus brief | WP4 (T1), WP10 | The pass that caught two mis-tiers stays open, so its audit (`adversarial_pass_recorded`) trains readers to ignore it. No amend verb, per the ruling. |
| GAP-059 harm_finding writer | CUT | WP10 closes it CLOSED-DECIDED | The column has no reader. The harm reached exec 171, where R7 and S1 read it. |
| I1 tier misfiling, no correction path | BUILD (correction path); CUT (a "derivable Co-1 refusal") | WP5 (T1) | A mis-tiered Co-1/T6 row cannot be corrected after capture except by hand SQL. The contradiction is a judgement, so no derivable refusal exists. |
| I2 R8 priors written after results | NARROW now; BUILD conditional | WP12 (T2); WP15 (T4) | Only an external timestamp can witness precedence. Until one exists, R8 must not claim it does. |
| I3 R7 floor gamed both ways | NARROW (floor removed; count-integrity kept) | WP12 | The party being judged types both terms of the ratio. RC1 (`provenance_artefact_audit`, blocking) already roots candidates in bytes. |
| I4 R5 gate tests a proxy | NARROW to admissions | WP12 | A non-English journal article filed `grey` drops from ● to ○. The search-target proxy forced batch 23 into a false `co1` retarget. |
| I5 unlogged searches and probes | BUILD (advisory) | WP14 (T3) | A coverage claim built on an unscreened search reaches `v_coverage_jurisdiction` and R14. Today only a reviewer diffing the transcript by hand can find it. |
| I6 author_fidelity INDETERMINATE | BUILD presence mode | WP8 (T1) | A fabricated person-author on a PDF or HTML source passes every gate (§5(c)). Presence in the bytes is a record-versus-artefact check, not a tautology. |
| I7 jurisdiction vocabulary | BUILD (PT, FI, UN plus writer refusal); OWNER-DECISION (UG) | WP7 (T1); D2 | A blocking check is red on untouched main. Writers check nothing, so PT reached 14 rows before any gate saw it. |
| I8 code leads, GAP-005 | BUILD | WP6 (T1), WP10 | R15 cannot be discharged against a lead. `insert_code_lead`'s refusal names a remedy ("Update that row instead") that no verb performs. |
| I9 checks that differ from main | BUILD (WP9 cuts G01–G03); NO-ACTION on the other two | WP9; WP10 | A unit test asserting corpus size is red forever. `adversarial_pass_recorded` differs because of pass 4 (cleared by WP10). `author_fidelity` → WP8. |
| I10 inherited reds | NO-ACTION (triage) | table below | None hides a book-facing defect created by this batch. |

I10 triage. All are advisory; levels come from `governance/check-registry.yaml`.

| Check | Owner of the defect | Hides a book-facing wrong? |
|---|---|---|
| `migration_reproducibility_deep` | The scheduled bot writes the DB without migrations (rule 3); the cron is the owner's | Yes in principle (a silent UPDATE of tier or title). Recurring, outside this plan. |
| `validate_schema_cross_check` | Archive (GB) versus live table (UK) after the rename; 37 issues | No. See correction 11. A GB→UK fold is a later small fix. |
| `validate_pydantic_schemas --strict` | The curated `MODEL_TABLE_MAP` (rule 8, named) | No. Schema-mirror drift only. |
| `retired_vocabulary` | Prose | No |
| `research_protocol_audit` | Research hygiene; same 15 issues on main | No |
| `metadata_integrity_audit` | An owner-review queue of `CORRECTED` rows; WP5 adds to it by design | No |
| `validate_reasoning --strict` | A pre-deletion reasoning document | No |
| `site_pages_fresh` | Built from `items` (0 rows) | No; the §7 item-layer trap |
| `source_locators_integrity` | Blocked on a `correct-locator` writer | No (clue store) |

---

## 4. PR plan

The session may push to `ccr-55d11bad-yxa6e4` (#166) without asking. **Every other branch below needs the owner's go-ahead (D3).** Each new branch is cut from `origin/main` with `git switch -c <name> origin/main`. `git checkout -B` and `git rebase` are blocked; bring main into a branch with `git merge origin/main`. Rule 9 applies to every PR:
- Open it last, after `scripts/preflight.sh` is clean.
- Call `unsubscribe_pr_activity` immediately after `create_pull_request`.
- Do not push again except for a deliberate change.
- The final push is never `[skip ci]`.

### T1 — writer verbs and migration 101 (tooling)

- **Branch:** `claude/process-gaps-t1-writers`. Needs go-ahead.
- **Packages:** WP1–WP9.
- **Why its own PR (rule 10):** it adds verbs, a table and a check mode. It carries no research rows. `data/guidebook.db` ships with a schema-only migration, which is the named exception in `research_tooling_separation`.
- **Depends on:** nothing. D2 decides one enum member.
- **Merges:** first.

### #166 — batch 23 plus its owed repair rows (research)

- **Branch:** `ccr-55d11bad-yxa6e4`. Allowed.
- **Package:** WP10.
- **Why separate:** these are research rows written through verbs that are already on main once T1 merges. Rule 10 is satisfied by order, not by holding the rows back.
- **Depends on:** T1 merged (hard).

### T2 — contract R16, R5/R7/R8, prose (tooling and governance)

- **Branch:** `claude/process-gaps-t2-contract`. Needs go-ahead.
- **Packages:** WP11–WP13.
- **Why its own PR:** it changes the contract and the gate, and touches no data.
- **Depends on:**
  - T1 (hard): the R16 predicate reads `parameter_declinations`, and `--selftest` clones the live schema.
  - #166 merged (hard): `LATEST-RESEARCH` must name a session with zero R16 debt.
- **Owner review:** the R16 sentence is reviewed in this PR, as DG-REVIEW (`governance/decision-protocol.md` §2.2, application of D-0173 and the 2026-08-26 ruling).
- **CI caveat:** T2's diff is tooling and governance only, so CI does not select `research_dod_session`. The builder runs it locally (WP11 acceptance).

### T3 — tool-call ledger (tooling)

- **Branch:** `claude/process-gaps-t3-ledger`. Needs go-ahead.
- **Package:** WP14.
- **Why its own PR:** its hook semantics are unverified, and it carries a `.claude/settings.json` hunk the owner may need to apply (D4). Splitting it keeps T1, #166 and T2 from waiting on that.
- **Depends on:** nothing hard. Merge it before batch 24 if possible.

### T4 — two-phase search log (tooling, conditional)

- **Branch:** `claude/process-gaps-t4-two-phase-log`. Needs go-ahead, later.
- **Package:** WP15.
- **Build only when:** T3 is merged and a searching batch run with T3 live has produced WebSearch ledger lines that match its `search_executions` rows.

### Batch 24 pilot (research)

- **Branch:** `claude/research-batch-24-parameter-pilot`. Needs go-ahead.
- **Depends on:** T1, #166 and T2 (hard); T3 (preference).

### Migration numbers

Derive the current top with `ls scripts/migrations | grep -E '^[0-9]{3}_' | tail -1` → `100_search_execution_candidate_update_stamps.sql`.
- T1 takes **101** (`101_parameter_declinations.sql`, `user_version` 100→101).
- T4 takes the next free number at build time: re-run the same command and add 1. That is 102 if nothing else intervenes.

No other PR adds a schema migration. Data migrations are timestamp-named and cannot collide.

### File-conflict matrix

✓ means the PR edits the file. The only PRs built in parallel are T1∥T3, #166∥T3 and T2∥T3. The rest are sequential, each branched or merged from the preceding merged main, so a shared file there is a sequential edit, not a conflict.

| File | T1 | #166 | T2 | T3 | T4 | B24 | Parallel conflict? |
|---|---|---|---|---|---|---|---|
| `scripts/db.py` | ✓ verbs | | ✓ comment near the `--set-target-evidence-type` flag (~L1398) | | ✓ | | No (sequential) |
| `scripts/dbcore.py` | ✓ | | | | | | — |
| `scripts/migrations/101_parameter_declinations.sql` | ✓ | | | | | | — |
| `scripts/migrations/data_*.sql` (new files) | | ✓ | | | | ✓ | No (distinct names) |
| `data/guidebook.db` | ✓ schema bump | ✓ | | | ✓ | ✓ | #166 takes main's blob after T1 (WP10 step 1). The bot cron can hit any of them (rule 3). |
| `schemas/base_parameter.py` | ✓ | | | | | | — |
| `schemas/enums.py` | ✓ | | | | | | — |
| `schemas/source_locator.py` (docstring) | | | ✓ | | | | — |
| `schemas/search_execution.py` | | | | | ✓ | | — |
| `scripts/audit/validate_pydantic_schemas.py` | ✓ | | | | | | — |
| `scripts/tests/test_db_amend_writers.py` | ✓ | | | | ✓ | | No |
| `scripts/tests/test_author_presence.py` (new) | ✓ | | | | | | — |
| `scripts/research/retrieval_log.py` | ✓ | | | | | | — |
| `scripts/tests/test_verification_pipeline.py` | ✓ | | | | | | — |
| `CLAUDE.md` (rule 7a sentence) | ✓ | | | | | | — |
| `governance/check-registry.yaml` | ✓ notes plus a new test entry | | ✓ notes | ✓ new entry | ✓ | | T1∥T3 and T2∥T3: different entries. Place T3's entry after `adversarial_pass_recorded` so its hunk is not adjacent to the others. |
| `governance/context-map.yaml` (generated) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Always resolve by regenerating: `python3 scripts/generate/context_map.py` |
| `governance/conceptual-model.md`, `governance/jurisdiction-philosophy.md` | ✓ | | | | | | — |
| `.claude/agents/antagonist.md` | ✓ artefact line | | ✓ subject-4 pointer | | | | No (sequential) |
| `skills/adversarial-research_SKILL.md` | | | ✓ | | | | — |
| `workplan/2026-09-10-batch-06-runbook.md` | | | ✓ | | ✓ | | No |
| `scripts/audit/research_batch_dod.py` | | | ✓ | | | | — (both reports' edits are merged into T2, so the selftest `expected` set has one editor) |
| `governance/research-contract.yaml` | | | ✓ | | ✓ (R8 text) | | No |
| `governance/research-contract-baseline.json` | | | ✓ | | | | — |
| `scripts/generate/research_contract_hook.py` | | | ✓ | | | | — |
| `.claude/settings.json` | | | ✓ `SessionStart[0].hooks[0].command` | ✓ new `PostToolUse[1]` | | | T2∥T3: different keys. Both must write `json.dumps(s, indent=2, ensure_ascii=False)+"\n"` (the file is in that form today: see WP14). |
| `scripts/ci_helpers/check_json.py`, `repo_files.py` | | | ✓ | | | | — |
| `decisions/DR-2026-08-19-…md` and its attestation | | | ✓ | | | | — |
| `.claude/hooks/record-command.py`, `scripts/tests/test_record_command_session.py`, `scripts/audit/search_log_completeness.py` (new), `.claude/commands/batch-done.md` | | | | ✓ | ✓ (audit mode) | | — |
| `sessions/…batch-23.md`, `attestations/sessions_session_2026-10-01-research-batch-23.json` | | ✓ | | | | | — |
| `sessions/LATEST`, `scratchpad/CURRENT`, a new session record and attestation | | | | | | ✓ | — |

---

## 5. Work packages

### Shared commands

Paste these into the same shell as the call; the harness resets the environment between shells.

```bash
# Rule-4 tree sweep. :(exclude) form — ':!_archived' fails as "pathspec magic".
# Frozen records are excluded on purpose. Dated workplans and migrations are historical; read the hits, edit none.
sweep() { git grep -n -E "$1" -- . ':(exclude)transcripts' ':(exclude)scratchpad' ':(exclude)sessions' \
  ':(exclude)_archived' ':(exclude)audits' ':(exclude)retrieval-log' ':(exclude)scripts/migrations' \
  ':(exclude)tools/*.html' ':(exclude)attestations' ':(exclude)workplan/_superseded'; }
# Rule-4 schema sweep: a VIEW is a caller.
dbsweep() { python3 -c "import sqlite3,sys; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); [print(*r) for r in c.execute(\"select type,name from sqlite_master where sql like ?\",('%'+sys.argv[1]+'%',))]" "$1"; }
```

**Write path for any scratch-DB step:**
1. `cp data/guidebook.db "$S/x.db"`.
2. Every call is `GUIDEBOOK_DB_PATH="$S/x.db" python3 scripts/db.py …`.
3. Capture with `scripts/research/emit_batch_sql.py` → `scripts/emit_data_migration.py --session <stem>.md` → `python3 scripts/migrate_db.py`.

**Per PR, once, when the diff is ready:**
- `scripts/preflight.sh`
- `python3 scripts/run_checks.py --changed-from origin/main --explain`
- `python3 scripts/run_checks.py --selftest`, which C7 needs for basis refs and the CI runs.

### T1

#### WP1 — `parameter_declinations` and `decline-parameter` (GAP-061 prerequisite)

**Files:**
- `scripts/migrations/101_parameter_declinations.sql`
- `schemas/base_parameter.py`: add `ParameterDeclination` beside `BaseParameter`
- `scripts/audit/validate_pydantic_schemas.py`: add `"base_parameter.ParameterDeclination": "parameter_declinations"` to `MODEL_TABLE_MAP` (L59ff)
- `scripts/db.py`: new verb, plus one refusal in `insert_parameter` (locate with `grep -n 'def insert_parameter' scripts/db.py` → L5903)
- `scripts/tests/test_db_amend_writers.py`
- `data/guidebook.db`: schema-only bump

**DDL** (stage: base, the registry's negative space; its reader is base's own writer):

```sql
CREATE TABLE parameter_declinations (
    term_id            TEXT PRIMARY KEY REFERENCES terms(term_id),
    reason             TEXT NOT NULL CHECK (length(trim(reason)) > 0),
    created_at         TEXT NOT NULL,
    created_by_session TEXT NOT NULL
);
PRAGMA user_version = 101;
```

A separate table, and not a `base_parameters.status` value: a declined term must never hold a `parameter_id` that an extraction could reference.

**Verb:** `db.py decline-parameter --term-id TERM-NNN --reason TEXT --session S [--dry-run]` → `decline_parameter(term_id, reason, session, dry_run=False)`. Stamp with `dbcore.stamp_for(conn, "parameter_declinations", session)`.

Refusals:
1. Blank `--term-id`.
2. Unknown term. Name the `observe-term` → `add-term --from-observation` path.
3. Blank reason, via `dbcore.require_reason(reason, term_id, why="A declination that cannot say why cannot be contested.")`.
4. The term is already a parameter. Name the `parameter_id`; retiring a parameter is a different act.
5. The term is already declined. Name the existing reason and session.

**`insert_parameter` gains one refusal:** a declined term. Name the declination; reversing one is a recorded decision, not a promotion. No `--undecline` verb (§8: nothing reads one yet).

**Capture:** `dbcore.writable_tables()` derives the table from the literal `INSERT INTO parameter_declinations` in `db.py`, so no list is edited. Verify with:
`python3 -c "import sys,sqlite3; sys.path.insert(0,'scripts'); import dbcore; c=sqlite3.connect('file:/tmp/rebuilt.db?mode=ro',uri=True); print('parameter_declinations' in dbcore.writable_tables(c))"` → True.

**Rule-4 sweep:** nothing is renamed. Run `sweep 'parameter_declin|decline-parameter'` and `dbsweep parameter_declinations`; both should show only the new code.

**Tests**, all on the temp copy, with fixture terms minted through `observe-term` and `add-term` and never a hard-coded live id:
- Each refusal fires.
- The legitimate shape writes one row.
- **`insert_parameter` refuses a declined term.** This fails on old code: no table, no verb.

The test file's EXAMINED line is its assertion count.

**Acceptance:**
- `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db`, then `python3 -c "import sqlite3; print(sqlite3.connect('/tmp/rebuilt.db').execute('pragma user_version').fetchone())"` → (101,)
- `python3 scripts/tests/test_db_amend_writers.py`
- `python3 scripts/audit/validate_pydantic_schemas.py` must not add drift for `parameter_declinations`.

**Risk:** a wrong declination blocks promotion of that term; reversing it needs a compensating migration. **Rollback:** retire the writer. The table stays (rule 5: a table that committed migrations INSERT into is never dropped).

#### WP2 — add-source refuses before it writes; `link-source-slug --local-ref-id` (GAP-058)

**Files:**
- `scripts/db.py`: the `add-source` dispatch (the block opened by the comment `# REFUSE BEFORE ANY WRITE, NOT AFTER.`, L3189; the write is at `ref_id = insert_evidence_source(data` L3213); the `link-source-slug` parser (L1593); `link_source_slug` (L7806); `insert_source_slug_link` (L7771)
- `scripts/tests/test_db_amend_writers.py`

**Change:**
1. When `args.slug` is set, the dispatch first runs, before `insert_evidence_source`:
   ```python
   with connect(readonly=True) as c:
       _check_slug_filable(c, args.slug)
       label = args.local_ref_id or _next_local_ref_id(c, args.slug)
   ```
   It refuses if `label` is already held on that slug by another ref_id.
2. It then inserts and calls `insert_source_slug_link(ref_id, args.slug, label, …)`.
3. If that call returns `inserted=False`, it raises. It does not emit a `linked_slug` it skipped.
4. Put the same label-collision refusal inside `insert_source_slug_link`, the single writer, so both callers inherit it. `source_slug_links` has no `UNIQUE(slug, local_ref_id)`: `select sql from sqlite_master where name='source_slug_links'`.
5. Correct the comment that claims "REFUSE BEFORE ANY WRITE"; it is false for this refusal today.

`link-source-slug` gains an optional `--local-ref-id`, passed through to `insert_source_slug_link`.

**Rule-4 sweep:** `sweep 'link-source-slug|local-ref-id'`. Update any prose that says the label cannot be supplied.

**Tests:**
1. Derive a mixed-scheme slug on the copy with `_next_local_ref_id`'s own regex. Today it is `accessible-circulation-geometry` on both DBs.
2. Run `add-source --slug <mixed>` without `--local-ref-id`. The row counts of `evidence_sources` and `evidence_source_authors` must be unchanged. **This fails on old code: both grow.**
3. The same call with an explicit, unused `--local-ref-id` succeeds.
4. `link-source-slug --local-ref-id` links an admitted, unlinked fixture source.
5. A colliding label refuses.

GAP-013 (reconciling the scheme) stays open.

**Acceptance:** `python3 scripts/tests/test_db_amend_writers.py`.
**Risk:** low. **Rollback:** revert.

#### WP3 — `supersede-source` (GAP-060)

**Files:**
- `scripts/dbcore.py`: new helper `determinations_resting_on(conn, ref_id)`
- `scripts/db.py`: new verb
- `scripts/tests/test_db_amend_writers.py`

**Helper:** returns `(table, key)` rows from the two junctions where a determination rests on a source:
- `specification_source_links`, which `dbcore.governing_refs` already treats as the one access path (L930–950);
- `convergence_sources`.

Two named junctions are the pointer, not a vocabulary. `pipeline-contract.yaml` has no table→stage map to derive them from. WP5 uses the same helper.

**Verb:** `db.py supersede-source --ref-id A --by B --reason TEXT --session S [--dry-run]`.

Write:
```sql
UPDATE evidence_sources SET superseded_by_ref_id = B,
  notes = dbcore.append_dated_note(notes, 'SUPERSEDED', session, 'by B: <reason>', stamp),
  updated_at, updated_by_session
WHERE ref_id = A
```

Refusals:
- A == B.
- A or B is missing (both via `dbcore.fold_ref`).
- A is already superseded (name its target).
- B is itself superseded. No chains; name B's target.
- Blank reason.
- `determinations_resting_on(conn, A)` is non-empty: retire the specification or re-run the convergence first.

**Output:** A's dependents, derived by iterating `PRAGMA foreign_key_list` over every table in `sqlite_master` for references to `evidence_sources.ref_id`, never a list. They are printed and left in place. The readers already filter on supersession:
- `assess_cell.py` L301, L358 (`superseded_by_ref_id IS NULL`)
- D04
- `link_source_slug` (L7837)
- `add-source`'s R9 check (L3741)
- `audit_evidence_metadata.py`

**Rule-4 sweep:** `sweep 'superseded_by_ref_id|KNOWN_DUP_SOURCE_KEYS|supersede'`. Update `test_db_integrity.py`'s `KNOWN_DUP_SOURCE_KEYS` comment ("every current collision is a genuine re-entry queued for merge", L812ff) to name `supersede-source` as the merge path. A09 keeps guarding the pointer.

**Tests:**
- Create two DOI-less fixture sources on the copy with the same corporate author, year and title.
- Run `GUIDEBOOK_DB_PATH=<copy> python3 scripts/tests/test_db_integrity.py`: D04 ✗.
- Supersede: D04 ✓ and A09 ✓. **This fails on old code: there is no verb.**
- Every refusal fires.

**Acceptance:** `python3 scripts/tests/test_db_amend_writers.py`.
**Risk:** superseding a source that a provisional cell reads changes its evidence set. The determination refusal covers stated cells only.
**Rollback:** retire the verb. Superseded rows stay as tombstones.

#### WP4 — close-pass artefact parse and the antagonist's artefact line (GAP-055)

**Files:**
- `scripts/db.py`: `close_adversarial_pass` (L4596), its SURVIVED branch
- `.claude/agents/antagonist.md`: the SURVIVED paragraph (~L92)
- `scripts/tests/test_db_amend_writers.py`

**Change:**
- Build the candidates: `tokens = [artefact] + [t.strip('()[]{},;:') for t in artefact.split() if '/' in t]`.
- Accept the finding when at least one token resolves through `dbcore.resolve_under(dbcore.REPO_ROOT, t)` to an existing file. Containment stays on the resolved path.
- Otherwise refuse, listing the tokens tried.
- Return path tokens that did not resolve as `unresolved` in the result and print them as REPORTED.

**Brief:** "Lead `artefact` with one repo-relative path to a committed file; anything after it (pages, 'and the other N', a second path) is a qualifier."

**Do not close passes 1 or 2:** ruling 2026-09-27, ACTION (2).

**Evidence on live data:** pass 4's SURVIVED rows 71, 80, 81, 83 and 88 fail the old literal check, and each contains at least one tracked path that exists. Re-derive with:
`select finding_id, artefact from adversarial_findings where pass_id=4 and verdict='SURVIVED'`
then `git ls-files --error-unmatch <token>`.

**Rule-4 sweep:** `sweep 'artefact.*SURVIVED|SURVIVED.*artefact|close-adversarial-pass'`. Align `skills/adversarial-research_SKILL.md` if it states the single-file shape.

**Tests:**
- Fixture pass and findings are set by SQL on the copy. Stated reason: `record-adversarial-pass` derives findings from two real transcripts. The lens set comes from `dbcore.check_values(conn,'adversarial_findings','lens')`.
- A SURVIVED artefact `"<tracked file> (and the other 11)"` closes. **This fails on old code.**
- `"source_value_extractions rows 70 and 71"` still refuses.
- `"../outside/x.txt"` refuses (containment).

**Acceptance:** `python3 scripts/tests/test_db_amend_writers.py`.
**Risk:** at least one resolvable token admits a finding that also cites a missing file. The REPORTED list keeps that visible.
**Rollback:** revert.

#### WP5 — `amend-source --field evidence_type` (I1)

**Files:**
- `scripts/db.py`: `_AMENDABLE` (L5103), `amend_source` (L5156), parser `p_ams` (L1575), dispatch (L2838)
- `scripts/tests/test_db_amend_writers.py`

**Change:** add `evidence_type` to `_AMENDABLE`. The parser gains `--scope` and `--co1-provenance`; both are refused unless `--field evidence_type`.
- The vocabulary is the keys of `schemas.tier_derivation.VALID_SCOPES_BY_TYPE`, the ladder and the one home. The column has no CHECK: `dbcore.check_values(conn,'evidence_sources','evidence_type')` → empty. Say so in the code comment.
- `--scope` is required unless the new type admits exactly one scope, in which case derive it.
- Compute `derive_tier(new_type, scope)`. `--tier` is optional and refused if it disagrees.

Refusals:
- → `co1` without `--co1-provenance`. Same text as add-source's D-0178 refusal (~L3181).
- `dbcore.determinations_resting_on(conn, ref_id)` is non-empty (from WP3). Footer: "Never move an adjudicated figure."

**Ledger:** one `metadata_integrity_detail` segment recording type, scope and tier moves. When leaving `co1`, copy `co1_provenance` into the segment, then set it NULL (correction 17).

**Rule-4 and rule-8 notes:**
- `_AMENDABLE` is a curated tuple, which rule 8 names. This grows it by one; GAP-013 item (1) remains the fix. Say so in the commit.
- Run `sweep 'amend-source|_AMENDABLE|tier was reachable|PAIRED CHANGE'`. Update `amend_source`'s "PAIRED CHANGE, added 2026-09-12" comment to name the new path.
- CLAUDE.md rule 8's `amend-source --tier` clause stays true.

**Tests**, on fixture sources created on the copy:
- (a) `refusal(db.amend_source, ref, "evidence_type", "national_fw", reason, session=S)`. Old code returns a not-amendable refusal. **This fails on old code.** New code succeeds with tier 6→5 and the ledger text.
- (b) → co1 without provenance refuses.
- (c) A contradicting `--tier` refuses.
- (d) A ref_id taken from the copy's `specification_source_links` refuses.
- (e) Leaving co1 moves the provenance text into the ledger and NULLs the column.

**Acceptance:** `python3 scripts/tests/test_db_amend_writers.py`.
**Risk:** a type change re-weights any undetermined cell, mitigated by (d) and the ledger. Each amendment adds a row to the `metadata_integrity_audit` review queue by design.
**Rollback:** remove the field from `_AMENDABLE`.

#### WP6 — `update-code-lead` and the near-duplicate refusal (I8, GAP-005)

**Files:**
- `scripts/db.py`: new verb; `insert_code_lead` (L8385, dedup at ~L8414)
- `scripts/tests/test_db_amend_writers.py`

**Verb:** `db.py update-code-lead --lead-id N --append-note TEXT --session S [--status V] [--clause C] [--dry-run]`.
- `--status` comes from the CHECK, via `dbcore.check_vocab(conn,'research_code_leads','status',…)`.
- Report B's forward-only transition order is **not** adopted: it would be an ordering list kept beside the CHECK (rule 8). Every move is ledgered instead.
- The note is appended with `dbcore.append_dated_note(notes,'UPDATED',session,detail)`. Any replaced clause or status goes into that note.
- Stamps `updated_at` and `updated_by_session`, which no row has used yet.

Refusals:
- Unknown lead.
- Empty `--append-note` (R15: re-describe from the source).
- No-op (status and clause unchanged).

**`insert_code_lead` gains a near-duplicate refusal:**
- Key: `re.sub(r"\W","",name.casefold(),flags=re.UNICODE)` within the same jurisdiction (correction 12).
- The refusal names the near match, unless `--distinct-from <lead_id>` is given; `--notes` must then say why.
- Its existing refusal text "Update that row instead" becomes `db.py update-code-lead --lead-id N`.

**Rule-4 sweep:** `sweep 'update-code-lead|add-code-lead|research_code_leads'`. Readers are unaffected: `validate_schema --cross-check` and `test_db_integrity` L02 key on exact strings.

**Tests:**
- **Old: the verb is absent (refusal() returns None → red).**
- New: a fixture lead moves REFERENCE-ONLY→RETRIEVED with a note.
- A case or punctuation variant refuses.
- Two distinct CJK-only names do not collide. This fails with an ASCII fold.

**Acceptance:** the test file. Leads 91, 92 and 93 are repaired in #166 (WP10), not here.
**Rollback:** retire the verb.

#### WP7 — jurisdiction vocabulary and writer refusal (I7)

**Files:**
- `schemas/enums.py`: `JurisdictionCode` (L140)
- `scripts/dbcore.py`
- `scripts/db.py`
- `governance/conceptual-model.md` (L188)
- `governance/jurisdiction-philosophy.md` (L13)
- `scripts/tests/test_db_amend_writers.py`

**Membership:**
- Add `PT`, `FI` and `UN`, each commented with the 2026-09-28 ruling. `grep -n 'tooling gap (rule 10' references/project-standards.md` → L4315 calls UN's absence a tooling gap. PT and FI are named Bucket-2 members.
- Add `UG` only per D2.
- No migration: `jurisdiction_db_vocabulary` reads the enum, and no `jurisdiction` column has a CHECK.

**Refusal:** new `dbcore.check_jurisdiction(value, context)`.
- NULL passes.
- A value not in the enum refuses.
- A rejected spelling refuses with its replacement. Import `rejected_spellings()` from `scripts/audit/jurisdiction_db_vocabulary.py`; do not copy it.

**Callers:** every `db.py` writer whose target table is one the audit FAILs on. That is, tables with a `jurisdiction` column, minus its `EXEMPT`, `CANDIDATE_TABLES` and `REPORT_ONLY` sets. Find them with `grep -n 'jurisdiction' scripts/db.py`. At least:
- `insert_evidence_source`
- `log_search`
- `insert_code_lead`
- the `add-extraction` insert
- `amend_source(field='jurisdiction')`

Fix that path's comment "The vocabulary stays gated by validate_jurisdiction". It is false: `validate_jurisdiction` never reads a table (`jurisdiction_db_vocabulary.py` docstring).

**Prose callers:**
- `conceptual-model.md` "(27 codes)" becomes the command `python3 -c "import sys; sys.path.insert(0,'.'); from schemas.enums import JurisdictionCode as J; print(len(list(J)))"` (→ 32 today).
- In `jurisdiction-philosophy.md` L13, keep the doctrinal "24 countries plus 2". Replace the false clause "encoded in schemas/enums.py JurisdictionCode" with "JurisdictionCode declares a superset; derive its members with the command above". This is a doctrine file, so the owner reviews it in the PR.

**Sweep:** `sweep 'JurisdictionCode|jurisdiction codes|\(27 codes\)'`.

**Tests:**
- `add-source --jurisdiction XX` refuses.
- `GB` refuses and names UK.
- `PT` is accepted.
- **Old code accepts XX.**

**Acceptance:** `python3 scripts/audit/jurisdiction_db_vocabulary.py` → `VERDICT: PASS`. The TW and colloquial values in `term_aliases` stay REPORTED. If D2 declines UG, the verdict is FAIL on UG alone, by decision.
**Rollback:** remove the members; the refusal stays.

#### WP8 — author and title presence mode (I6)

**Files:**
- `scripts/research/retrieval_log.py`: `verify_authors` (L1259), whose non-JSON branch prints INDETERMINATE at L1287
- new `scripts/tests/test_author_presence.py`
- `governance/check-registry.yaml`: `author_fidelity` note plus `compares: record-artefact`, and the new test entry

**Change:** when `_logged_payloads(session)` is empty but `_unparsed_payloads(session)` is not, run a presence pass instead of returning INDETERMINATE.

Each row's artefacts are:
- manifest lines whose `ref_id` equals the row's ref_id, or whose `url` equals the row's url;
- plus lines whose `derived_from` is one of those.

This mapping finds artefacts for 14 of the 14 batch-23 sources. Re-derive with the mapping script in §7. The text is `decode_artefact(bytes)`, compared with `normalise_quote`.

- **ASSERT:** every personal author's (`is_corporate=0`) `last_name`, and the title's first segment (`pub_title` up to the first ` — `, `: ` or ` - `).
- **REPORT:** a `corporate_name` that is absent. Corporate glosses like "Republic of Korea" on a Korean statute are a project convention, not a fabrication.

Verdict lines:
- `PRESENT-IN-BYTES: n of m source(s); not Crossref-diffed; cannot detect an omitted author`
- `EXAMINED: <rows with ≥1 decodable artefact>`
- Rows without a decodable artefact are listed as UNEXAMINABLE.

Exit 1 if any asserted field is absent or EXAMINED is 0. The JSON path is unchanged.

**Registry entry `test_author_presence`:**
- `cmd: [python3, scripts/tests/test_author_presence.py]`
- `battery: tests`, `kinds: [tooling]`, `level: advisory`, `basis: hygiene`, `cost: fast`
- `no_floor: "selftest — subject is its own fixtures, not a corpus"`

Then run `python3 scripts/run_checks.py --selftest`; C7 must resolve the basis.

**Tests:**
- Use a temporary log root (`GUIDEBOOK_RETRIEVAL_LOG=<tmp>`, read at `retrieval_log.py` L142) and a temporary DB (`GUIDEBOOK_DB_PATH`, L143), with one manifest line, one text artefact and one source row.
- A person-author present in the text → exit 0. **This fails on old code, which returns INDETERMINATE (exit 1).**
- An absent person-author → exit 1, with the row named.

**Acceptance:** `python3 scripts/research/retrieval_log.py --session session_2026-10-01-research-batch-23 --verify-authors`. Read every NOT-FOUND title against its text before treating the result as meaningful.
**Risk:** [ASSUMPTION: a typed title's first segment occurs in the decoded text] Composed titles may fail. The check is advisory, so a false FAIL gates nothing.
**Rollback:** delete the branch; the JSON path is untouched.

#### WP9 — `test_verification_pipeline` corpus floors (I9)

**Files:**
- `scripts/tests/test_verification_pipeline.py`: delete G01–G03 (L336–364)
- `governance/check-registry.yaml`: in `test_verification_pipeline`, replace `note: 18/18 assertions.` with "derive: `python3 scripts/tests/test_verification_pipeline.py | tail -3`"
- `CLAUDE.md`, rule 7a (L145): put the "still asserts … ≥50/≥30/≥100" sentence into the past tense with the commit that removed them, and record the account in the commit message per CLAUDE.md's own convention. This is a CLAUDE.md change, so the owner sees it in review.
- Regenerate `governance/context-map.yaml`.

**Sweep:** `sweep 'test_verification_pipeline|18/18'`. Leave dated workplans and `references/audits/` reports as they are (historical). Registry L69 stays true, because G04 still reads live `pipeline_runs`.

**Test that fails on the old behaviour:** the file's own exit code. It is 1 on both DBs today, and must be 0 on both after the change.

**Acceptance:**
```bash
python3 scripts/tests/test_verification_pipeline.py >/dev/null; echo $?
GUIDEBOOK_DB_PATH=/tmp/claude-0/main.db python3 scripts/tests/test_verification_pipeline.py >/dev/null; echo $?
```
Both must print 0. [UNVERIFIED until run]

**Rollback:** revert.

### #166

#### WP10 — batch 23's owed judgement and repairs, through T1's verbs (data, working branch)

**Precondition:** T1 is merged.

**Step 1 — bring main in.**
1. `git fetch origin && git merge origin/main`.
2. On the `data/guidebook.db` conflict, run `git checkout --theirs data/guidebook.db`. This takes main's blob, which has migration 101 and any bot rows.
3. Run `python3 scripts/migrate_db.py`. It applies the five batch-23 data migrations (`ls scripts/migrations | grep '^data_20261001'`), because they are absent from main's ledger.
4. Run `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db`.
5. Resolve `governance/context-map.yaml` by regenerating it.

**Step 2 — scratch writes.** Use stem `session_2026-10-01-research-batch-23`.

[ASSUMPTION: the repair rows are stamped with the batch's own stem, as batch 20's fix-forward rows were (`0fb5f62`). The pass did not review them. The session record discloses this, and the batch-24 pass reviews them (§7).]

a. **Adjudicate all 14 observations.** List them with:
   `select observation_id, ref_id, surface_form, language, context_quote from observed_terms where created_by_session='session_2026-10-01-research-batch-23'` → 14.
   Run `adjudicate-term --observation-id N --outcome … [--term-id …] --rationale '<from the context_quote>'` for each.
   Proposed mapping, [ASSUMPTION: confirm each against its context_quote]:
   - slope phrases (ramplutning, inclinação, pendiente, pendiente longitudinal, Pendientes longitudinales máximas) → `NAMES-EXISTING TERM-001`;
   - element phrases (경사로 ×2, hellingbaan ×2, hellingbanen, ramp, rampas, plan incliné) → `NAMES-EXISTING TERM-089`;
   - `utjämning till 0-nivå` → `DEFERRED`, unless its context names TERM-090.

b. **Decline TERM-089.**
   `decline-parameter --term-id TERM-089 --reason "an element, not a quantity under determination; its quantities are separate terms (TERM-001 ramp gradient, TERM-091 ramp run length, TERM-092 intermediate landing)"`.
   Any other term named in (a) gets `add-parameter` or `decline-parameter`, as judged.

c. **Supersede the mirror.**
   `supersede-source --ref-id REF-01019 --by REF-01031 --reason "NEPLA mirror of the official Annex 1; extractions 82/83 duplicate 107/108 and already carry root_ref_id REF-01031"`.
   Check that no figure is lost: `select extraction_id, ref_id, root_ref_id, claim_text from source_value_extractions where ref_id in ('REF-01019','REF-01031')` shows 107 and 108 on REF-01031.

d. **Close pass 4.** `close-adversarial-pass --pass-id 4`.

e. **Leads (preference).** Run `update-code-lead` on leads 91, 92 and 93 from batch 23's search rows (R15).

f. **Gaps.**
   - `close-gap` GAP-055, GAP-058 and GAP-060 as `CLOSED-FIXED`.
   - GAP-005 as `CLOSED-FIXED` if (e) was done.
   - GAP-059 as `CLOSED-DECIDED`.
   - GAP-061 stays OPEN until batch 24.

**Step 3 — capture and apply** through the write path (§5 header), with `--session session_2026-10-01-research-batch-23.md`.

**Step 4 — record.**
- Session record: add to §2 the disclosure that the repair rows were written after pass 4. Mark §4.3 and §4.4 resolved, with the commands. Re-run the §6 gates.
- Update `attestations/sessions_session_2026-10-01-research-batch-23.json`.
- Run `python3 scripts/preserve_transcripts.py`.

**Acceptance — R16 debt is zero for the pointer session.** This is what lets T2 land green:
```bash
python3 - <<'PY'
import sqlite3; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); S='session_2026-10-01-research-batch-23'
print(c.execute("select count(*) from observed_terms o join evidence_sources e on e.ref_id=o.ref_id where e.created_by_session=? and not exists (select 1 from term_adjudications a where a.observation_id=o.observation_id)",(S,)).fetchone())  # must be (0,)
print(c.execute("select distinct a.term_id from term_adjudications a join observed_terms o on o.observation_id=a.observation_id join evidence_sources e on e.ref_id=o.ref_id where e.created_by_session=? and a.term_id is not null and not exists (select 1 from base_parameters p where p.term_id=a.term_id) and not exists (select 1 from parameter_declinations d where d.term_id=a.term_id)",(S,)).fetchall())  # must be []
PY
```

**Acceptance — the remaining gates:**
- `python3 scripts/tests/test_db_integrity.py`: D04 ✓
- `python3 scripts/audit/adversarial_pass_audit.py --session session_2026-10-01-research-batch-23`: pass 4 closed
- `python3 scripts/audit/jurisdiction_db_vocabulary.py`
- `python3 scripts/audit/research_batch_dod.py --session session_2026-10-01-research-batch-23`
- Then `scripts/preflight.sh` once, and push. The final push is not `[skip ci]`.

**Rollback:** fix forward with a compensating data migration.

### T2

#### WP11 — R16 and R16-adjudicate (GAP-061)

**Files:**
- `governance/research-contract.yaml`
- `scripts/generate/research_contract_hook.py`
- `.claude/settings.json` (regenerated)
- `scripts/audit/research_batch_dod.py`
- `governance/research-contract-baseline.json`

**Contract.** Add `R16`:
- `phase: when-filing`, `enforcer: R16`
- `title: "Every concept a source states a figure for is disposed of"`
- `anchor: "D-0173; owner ruling 2026-08-26 (the parameter is the judgment object); workplan/2026-09-10-batch-06-runbook.md Step 4b"`
- Hook text, for owner review in this PR: *"Every concept a source states a figure for is filed against a parameter, not left in prose or a code lead: observe-term -> adjudicate-term (or add-term) -> add-parameter -> add-extraction. A term that is not a design parameter is declined with its reason (db.py decline-parameter). Every phrase observed on this batch's admissions is adjudicated before the gate; NOT-OURS and DEFERRED are answers."*
- Regenerate with `python3 scripts/generate/research_contract_hook.py --write`. The generator rewrites `SessionStart[0].hooks[0].command` in place (L175), and nothing is inserted at index 0.

**Generator.** Widen L146 to `\bR[1-9]\d?(?:[a-z]|-[a-z]+)?\b`. Run against the current enforcer, it adds no new ids. Update the docstring at L6 ("R1-R15") and the L136 comment.

**Enforcer.** Add two predicates after R11-harvest (L721ff), both using `escope` (L499; empty in `--all`):
- **R16-adjudicate:** observations on this batch's admissions with no `term_adjudications` row.
  ```sql
  SELECT o.observation_id FROM observed_terms o JOIN evidence_sources e ON e.ref_id=o.ref_id
  WHERE NOT EXISTS (SELECT 1 FROM term_adjudications a WHERE a.observation_id=o.observation_id) {escope}
  ```
  Fail with the count and the first eight ids. The PASS line reads `EXAMINED: <n> observation(s) on this batch's admissions; every one adjudicated`.
- **R16:** distinct terms named by adjudications of those observations, with neither a parameter nor a declination.
  ```sql
  SELECT DISTINCT a.term_id FROM term_adjudications a
  JOIN observed_terms o ON o.observation_id=a.observation_id JOIN evidence_sources e ON e.ref_id=o.ref_id
  WHERE a.term_id IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM base_parameters p WHERE p.term_id=a.term_id)
    AND NOT EXISTS (SELECT 1 FROM parameter_declinations d WHERE d.term_id=a.term_id) {escope}
  ```
  `term_id IS NOT NULL` is the schema's own pairing CHECK for the naming outcomes. This keeps the outcome list out of the code (rule 8) and counts NAMES-EXISTING as well as NAMES-NEW.
  The PASS line reads `EXAMINED: <n> term(s) named`, plus REPORTED counts of DEFERRED and NOT-OURS. It also states: "a figure stated for a concept never observed is NOT tested here — adversarial standing subject 4".

Add both to the docstring table.

**Selftest.** In `selftest()` (L880):
- Seed two terms; mark one declined in `parameter_declinations`.
- Seed three observations on REF-ST2: one NAMES-NEW to the undeclined term, one NAMES-EXISTING to the declined term, one unadjudicated.
- Add `"R16"` and `"R16-adjudicate"` to `expected` (L1023).
- Assert `caught["R16"] == 1` and `caught["R16-adjudicate"] == 1`. These are negative cases in the R9a style.
- R11-harvest still fires on REF-ST1, ST3 and later.

**Baseline.** Write the baseline after #166 has merged, so it captures post-repair debt:
`python3 scripts/audit/research_batch_dod.py --write-baseline`
Expect NEW entries for `R16` (corpus terms undisposed), `R16-adjudicate` (batches 21–22) and `R7` (from WP12), and `R3` lowered. Verify the figures with:
- `select count(distinct a.term_id) from term_adjudications a where a.term_id is not null and not exists (select 1 from base_parameters p where p.term_id=a.term_id) and not exists (select 1 from parameter_declinations d where d.term_id=a.term_id)`
- `select count(*) from observed_terms o where not exists (select 1 from term_adjudications a where a.observation_id=o.observation_id)` (25 before #166; 11 expected after)

Then `python3 scripts/audit/research_batch_dod.py --check-baseline origin/main` must exit 0 and print NEW for each new code. Skipping this leaves every Stop hook ending "RESEARCH DoD: FAIL".

**Prose callers (rule 4/7a).** Run `sweep 'R1-R15|R1–R15|fifteen rules|15 rule'`. Edit only present-tense claims, and replace each with "the research contract" so the next rule does not re-trigger the sweep:
- `research-contract.yaml:1`
- `check-registry.yaml:1281` (the `research_dod` no_floor)
- `research_batch_dod.py:18`
- `research_contract_hook.py:6`
- `scripts/ci_helpers/check_json.py:5`
- `scripts/ci_helpers/repo_files.py:9`
- `schemas/source_locator.py:19`

Historical sentences stay: `research-contract.yaml:10`, `check-registry.yaml:1245`, `research_batch_dod.py:933`, migrations, dated workplans. Registry basis refs are unchanged. Run `python3 scripts/run_checks.py --selftest`.

**Falsification (acceptance):**
- `--session session_2026-10-01-research-batch-23` → COMPLIANT, with R16 and R16-adjudicate EXAMINED > 0.
- `--session session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa` → FAIL R16 naming TERM-094. Derive with the WP10 R16 query using the batch-20 stem.
- `--session session_2026-09-28-research-batch-22-selection` → FAIL R16-adjudicate.
- `--selftest` → both FIRED, with counts 1 and 1.
- `python3 scripts/generate/research_contract_hook.py --check` → `agree on 16 rule ids (+5 sub-rules …)` and the hook in sync.

**Risk:** a session that adjudicates another batch's observations is not itself gated on the terms it names. `--all` and the baseline ratchet see that.
**Rollback:** revert the commit together with the baseline file; the ratchet refuses a dropped code.

#### WP12 — R5 to admissions, R7 floor to count-integrity, R8 stated honestly (I2, I3, I4)

**Files:**
- `scripts/audit/research_batch_dod.py`: R5 block L393–408, R7 block L420–448, R8 block L450ff, the TUNABLE block L150–170, the selftest's R7 interaction comment L988–992 and the "R5 (non-EN targeted grey)" note at L908
- `governance/research-contract.yaml`: `resolution:` notes on R5, R7 and R8. Hook texts are unchanged, so the regeneration in WP11 is the only `settings.json` change.
- `scripts/db.py`: the comment above `--set-target-evidence-type` (~L1398)
- `skills/adversarial-research_SKILL.md` L103 ("only `candidates < screened/25` can fail that rule")
- `decisions/DR-2026-08-19-research-restart-operative-instrument.md` Step 4 (L865): append an `AMENDED 2026-10-xx — APPENDED, NOT EDITED` block, in the DR's own convention
- `attestations/decisions_DR-2026-08-19-research-restart-operative-instrument.json` (rule 2)

**R5.** FAIL on admitted sources in scope:
```sql
upper(coalesce(lang_detected,'EN'))<>'EN' AND evidence_type='grey'
AND (source_type='journal_article' OR coalesce(journal_name,'')<>'' OR coalesce(doi,'')<>'')
```
`source_type` vocabulary comes from `dbcore.check_values(conn,'evidence_sources','source_type')`, which includes `journal_article`. The PASS line reads `EXAMINED: <non-EN admissions>`, and the old search-target count becomes a REPORTED line. Corpus today: 0 failing rows of 24 non-EN admissions:
- `select count(*) from evidence_sources where upper(coalesce(lang_detected,'EN'))<>'EN'` → 24
- the predicate above → 0

**R7.**
- Delete `R7_SCREENED_PER_CANDIDATE` and the floor.
- Assert only `results_screened <= results_found AND results_admitted <= results_screened`, over EXAMINED rows in scope.
- Keep candidate and harm counts as REPORTED.
- The comment names RC1 (`provenance_artefact_audit`, blocking) and standing subject 1 as R7's substantive enforcers.

Corpus check: `select exec_id, created_by_session from search_executions where results_screened>results_found` → exec 50 (batch 11). It is inherited and goes into the baseline in WP11. The TUNABLE block's header says to "say so in the PR" whenever a threshold is weakened; the PR text does that.

**R8.** No enforcer change of substance. The PASS line gains: "precedence of the prior over the search is NOT tested: `dbcore.now()` is minute-precision (`dbcore.py` L190–191) and log-search writes after results; the adversarial pass (L6) and the transcript are its only witnesses". The `resolution:` note records the same. The hook text keeps the obligation unchanged, because it is an instruction, not a claim of enforcement. If T3 never lands, this is what R8 says, permanently.

**Selftest:**
- Add `REF-ST8` (lang `id`, `grey`, `source_type='journal_article'`, session T).
- Assert `caught["R5"] == 1`. The exec-1 search-target fixture no longer counts; this is the negative case.
- Add exec 5 (found 1, screened 2) so R7 fires.
- Rewrite the R7 interaction comment.

**Prose callers:** `sweep 'per 25|screened/25|screened // ?25|R7_SCREENED|1 candidate per|candidates < screened'` and `sweep "targeted as 'grey'|pre-classified as grey"`. Edit the live callers listed above. Leave `references/search-log/` (frozen), dated workplans and attestations.

**Acceptance:**
- `python3 scripts/audit/research_batch_dod.py --selftest`
- `--session session_2026-10-01-research-batch-23`: R5 PASS with its EXAMINED line, R7 with no floor
- `python3 scripts/generate/research_contract_hook.py --check`
- `python3 scripts/run_checks.py --battery attestation`

**Rollback:** revert. No data is touched.

#### WP13 — the runbook loop, standing subject 4, the antagonist pointer (GAP-061 structural cause)

**Files:**
- `workplan/2026-09-10-batch-06-runbook.md`
- `skills/adversarial-research_SKILL.md` (L91ff)
- `.claude/agents/antagonist.md`

**Runbook.**
- Step 1 stays, for a cell with no parameter.
- Step 4b's "One `add-extraction` per source that says something about the parameter" becomes the per-source loop in §7: every figure, for any concept, through observe → adjudicate or add-term → add-parameter or decline-parameter → add-extraction. Step 4b states R16 as its gate.
- Correct L93–94, which says "a second, separate `adjudicate-term` call … is refused (already adjudicated)". `adjudicate_term` writes a second row and prints a NOTE (L5575ff: divergent adjudications are deliberate).

**Skill.** Add standing subject 4: *figures the payload states that no extraction carries, and concepts it names that no observation records*. Change "These three properties" to "These four". Subject 1's floor sentence is fixed in WP12.

**Antagonist.** Add one line under L2 pointing at subject 4.

**Sweep:** `sweep 'add-parameter|adjudicate-term|observe-term'` over `skills`, `.claude` and the runbook. Update any text that ends the loop at harvest.

Nothing new is read by machine; §8 is satisfied because no apparatus is added.

**Acceptance:** read-through against `db.py --help` for each verb named.

### T3

#### WP14 — tool-call ledger and `search_log_completeness` (I5)

**Files:**
- `.claude/settings.json`: append `hooks.PostToolUse[1]` = `{"matcher": "WebSearch|WebFetch", "hooks": [{"type": "command", "command": "python3 \"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/record-command.py\" 2>/dev/null || true"}]}`. Leave `PostToolUse[0]` (`Bash`) and every `SessionStart` entry untouched. Write with `json.dumps(…, indent=2, ensure_ascii=False)+"\n"`, and check the form is preserved: `python3 -c "import json; r=open('.claude/settings.json',encoding='utf-8').read(); print(r==json.dumps(json.loads(r),indent=2,ensure_ascii=False)+'\n')"` → True.
- `.claude/hooks/record-command.py`: branch on `d.get("tool_name")` before `if not c: sys.exit(0)` (L147).
  - For `WebSearch`, write `{"ts","tool":"WebSearch","query","allowed_domains","blocked_domains","session_id","response_sha256"}`.
  - For `WebFetch`, write `{"ts","tool":"WebFetch","url","session_id","response_sha256"}`.
  - Bash lines gain `"tool":"Bash"`. Readers treat a missing `tool` as Bash.
  - Session routing (`open_session`) is unchanged.
- `scripts/tests/test_record_command_session.py` (registered): add a WebSearch payload fixture.
- New `scripts/audit/search_log_completeness.py`.
- `governance/check-registry.yaml`: new entry.
- `.claude/commands/batch-done.md`: add `python3 scripts/audit/search_log_completeness.py --session "$(cat scratchpad/CURRENT)"` beside L9.

**Audit:**
- FAIL: a ledger WebSearch query whose casefolded, whitespace-collapsed text equals, or is contained in, no `search_executions.query_text` for the session.
- REPORTED: WebFetch URLs found in neither `query_text` nor the manifest. WebFetch returns a summary, not bytes, so R10 persistence cannot apply.
- REPORTED: `curl` and `wget` hosts in Bash lines that are absent from the manifest.
- Prints `EXAMINED: <WebSearch+WebFetch ledger lines>`.

**Registry entry:**
- `id: search_log_completeness`
- `cmd: [python3, scripts/audit/search_log_completeness.py, --session, '@SESSION@']`
- `battery: research`, `kinds: [data, synthesis]`, `level: advisory`
- `basis: evidence/discovery-provenance`: `search_executions` is the one event home of a discovery step
- `cost: fast`, `requires_session: true`, `session_pointer: CURRENT`, `compares: record-artefact`
- `no_floor: "session-scoped — a session that ran no WebSearch has an honest zero"`
- `note`: promote after the first searching batch with ledger lines

Run `python3 scripts/run_checks.py --selftest`; C7 resolves the basis and C11 checks `compares`.

**Tests:**
- The hook test: a WebSearch payload writes a `tool`/`query` line, and the Bash path is unchanged.
- The audit: a fixture `commands.jsonl` plus a scratch DB with one unlogged query → FAIL; all logged → PASS. **Old code: no line is written, so the audit has nothing to compare.**

**Acceptance:** the audit on the fixture. After the hook is live, run one WebSearch in a session and inspect the line. [UNVERIFIED: matcher semantics and payload field names]
**Rollback:** remove `PostToolUse[1]`. The audit then reports NOTHING-IN-SCOPE.

### T4 (conditional)

#### WP15 — two-phase search log and the precedence check (I2)

**Build only after** T3 is merged and a searching batch run with T3 live shows ledger WebSearch lines matching its `search_executions` rows.

**Files:**
- `scripts/migrations/<next>_search_executions_completed_at.sql`: additive `completed_at TEXT`, bumps `user_version`
- `schemas/search_execution.py`
- `scripts/db.py`:
  - `log-search` refuses `--results-*` unless `--backfill 1`;
  - new `complete-search --exec-id N --results-found --results-screened [--findings-note --saturation-signal --admitted-ref-id …]`, which refuses if `completed_at` or `deferred_reason` is set, and stamps `completed_at` and `updated_*`.
- `search_log_completeness.py --mode precedence`:
  - FAIL when a ledger minute precedes the row's `created_at` and `backfill=0`;
  - an equal minute is REPORTED as indeterminate;
  - `backfill=1` rows are counted.
- `emit_batch_sql.py` already emits UPDATEs (L165–170).

**Sweep, for the signature change:**
`git grep -n -E 'log-search|results-found' -- . ':(exclude)transcripts' ':(exclude)scratchpad' ':(exclude)retrieval-log' ':(exclude)scripts/migrations' ':(exclude)sessions' ':(exclude)attestations'`
Expected hits: the `db.py` help text, the runbook, `skills/research-log-manager_SKILL.md`, DR-2026-08-19 Step 3 (append, with an attestation), `.claude/commands/session-open.md`, and R8's hook text ("register before, complete after"), which needs a `--write` regeneration.

**Tests:** `complete-search` twice refuses; a row created after its ledger timestamp → FAIL.

**Acceptance:** `migrate_db.py --rebuild`, `python3 scripts/dbcore.py --selftest`, and the audit on a fixture.
**Risk:** an UPDATE on an append-only table, the same class as `amend-search`'s setters. Name it in the migration header.
**Rollback:** retire the writer. The column stays (rule 5).

---

## 6. Sequence

1. **Owner decisions D1–D4.** D3 is a hard prerequisite for every new branch. D1 is a hard prerequisite for steps 4–6, because it fixes where #166 sits. D2 changes WP7's content only. D4 matters for T2's regeneration and for T3.
2. **Build T1** (WP1–WP9) on a new branch from `origin/main`. Hard: D3.
3. **Build T3** (WP14) in parallel on its own branch. Hard: D3, plus D4 for its `settings.json` hunk.
4. **T1 opens and merges.** Hard: preflight clean. Its CI must be green on D04, which it is because main has no REF-01019. `jurisdiction_db_vocabulary` is green if D2 admits UG.
5. **#166 takes main and gets WP10,** then merges. Hard: T1 merged. After this, `LATEST-RESEARCH` on main is batch 23, with zero R16 debt.
6. **Build T2** (WP11–WP13) from `origin/main`, then open and merge it. Hard: T1 (schema) and #166 (pointer debt). Run the WP11 falsification against main's DB before opening the PR.
7. **T3 merges** whenever it is green. Preference: before step 8. If it merges after T2, take main and confirm the `settings.json` form check.
8. **Batch 24 pilot** (§7). Hard: T1, #166, T2. Preference: T3. GAP-061 closes here.
9. **T4**, only after a searching batch has run with T3 live. Hard: T3 plus that evidence.

Only preferences, not hard dependencies:
- leads 91–93 in #166 rather than in batch 24;
- T3 before batch 24;
- lowering the baseline after batch 24, in a later tooling PR.

---

## 7. Batch 24 pilot

**Shape.** The pilot is a judgement-stage re-read of batch 23's 14 admitted sources. There are no searches, no admissions and no refetch. Two figures to re-derive:
- `select count(*) from evidence_sources where created_by_session='session_2026-10-01-research-batch-23'` → 14
- `ls retrieval-log/session_2026-10-01-research-batch-23 | wc -l` → 68

**Gating.** A session with no searches and no admissions fails R1, R9a and R9b (correction 9). The pilot therefore:
- has its own stem (for example `session_2026-10-0X-research-batch-24-parameter-pilot`), set in `scratchpad/CURRENT` with a folder of the identical name (CLAUDE.md §7);
- moves `sessions/LATEST` at close, and **does not move `sessions/LATEST-RESEARCH`**;
- is gated by `research_batch_dod.py --session session_2026-10-01-research-batch-23`. Because R16 and R16-adjudicate are scoped to admissions, they examine the pilot's new observations and adjudications. CI's `research_dod_session` follows the unchanged pointer to the same session.
- runs `/batch-done` with the batch-23 stem for the DoD line, and records why.

[ASSUMPTION: a judgement-only session may leave `LATEST-RESEARCH` in place. If the owner wants the pointer to move, pair the re-read with a genuine search phase so R1, R9a and R9b have a subject.]

**Mapping sources to persisted text:**
```bash
python3 - <<'PY'
import json, sqlite3
S='session_2026-10-01-research-batch-23'; root=f'retrieval-log/{S}/'
M=[json.loads(l) for l in open(root+'manifest.jsonl')]
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for r,u in c.execute("select ref_id,url from evidence_sources where created_by_session=?",(S,)):
    a=[d['artefact'] for d in M if d.get('ref_id')==r or (u and d['url']==u)]
    print(r, sorted(set(a+[d['artefact'] for d in M if d.get('derived_from') in a])))
PY
```

**Per-source loop.**
- Write to a scratch copy (`cp data/guidebook.db "$S/pilot.db"`).
- Prefix every call with `GUIDEBOOK_DB_PATH="$S/pilot.db" python3 scripts/db.py`.
- Pass `--session <pilot stem>` on every call.

1. Read the persisted `-text.txt`, falling back to the raw artefact.
2. `observe-term --ref-id REF --surface-form '<verbatim>' --language XX --locator '<clause>' --context-quote '<sentence>'`. Do this for every concept phrase the source states a figure for (D-0173: verbatim, unjudged).
3. Adjudicate, choosing one:
   - `adjudicate-term --observation-id N --outcome NAMES-EXISTING --term-id TERM-NNN --rationale '…'`
   - `add-term --from-observation N --canonical-en '<name with no value>' --rationale '…'` (which performs NAMES-NEW)
   - `NOT-OURS` or `DEFERRED`, with a rationale.
4. For each named term with no parameter, choose one:
   - `add-parameter --term-id TERM-NNN`, for a design quantity;
   - `decline-parameter --term-id TERM-NNN --reason '…'`, for an element, a lens term or a method.
5. `set-parameter-direction --parameter-id P --direction <from the CHECK> --rationale '…'` **only** where an admitted source states which way is better for a disabled person. Otherwise leave it NULL (the column permits it).
6. `add-extraction` per figure, with:
   - `--ref-id`, `--slug` (from `source_slug_links`), `--parameter-id`
   - `--claim-type`, `--claim-text` (a substring of the payload under `normalise_quote`)
   - `--extraction-method`, `--figure-role` (vocabulary from `dbcore.check_values(conn,'source_value_extractions','figure_role')`), `--comparator`, `--claimed-value`, `--claimed-unit`
   - `--relation`, `--jurisdiction`
   - at least one of `--identity`, `--icf`, `--needs`, `--medical`
   - the locator flags.
7. `relate-extraction --from E --relation condition_on --to-extraction E2` for every `condition` row. `extraction_relations_integrity` requires it.

**Then:**
- capture and apply;
- `python3 scripts/audit/research_batch_dod.py --session session_2026-10-01-research-batch-23`: COMPLIANT, with R16 and R16-adjudicate EXAMINED above their pre-pilot values;
- `python3 scripts/audit/extraction_relations_integrity.py`;
- `python3 scripts/tests/test_db_integrity.py`;
- `python3 scripts/audit/research_batch_dod.py --all` within the baseline;
- the adversarial pass;
- `/batch-done`.

**Owed repairs in the same PR, through existing verbs:**
- Review the targets of execs 157 and 171. They were retargeted `grey→co1` to clear the old R5 (record §2.5). Use `amend-search --exec-id N --set-target-evidence-type grey --append-note '<why>'` only where the search sought grey material.
- Close GAP-061 `CLOSED-FIXED` once at least one new parameter carries at least one extraction and R16 is green.

**Row budget.** These numbers are discretionary; they are stated so they can be audited.
- **New parameters ≤ 4.** This is the number the session record's §4.5 scratch experiment promoted without tripping a content check (`grep -n 'promoting door width' sessions/session_2026-10-01-research-batch-23.md`). Count with `select count(*) from base_parameters where created_by_session='<pilot stem>'`.
- **Extractions ≤ 2 × batch 23's.** `select count(*) from source_value_extractions where created_by_session='session_2026-10-01-research-batch-23'` → 30, so the cap is 60.

**Stop conditions:**
- the budget is reached;
- `add-parameter` refuses a value-bearing name. `canonical_en` is not amendable (`_AMENDABLE_TERM_FIELDS`, L5017), so stop on that term and file a GAP;
- a figure's text is absent from the persisted payload. Record it as a lead; there is no refetch in the pilot;
- any writer refuses in a way this plan did not anticipate. Stop and file a GAP (rule 10). Never patch.

**Adversarial pass.**
- One pass per batch (RULE ACTION 5).
- Every lens: `python3 -c "import sys,sqlite3; sys.path.insert(0,'scripts'); import dbcore; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); print(sorted(dbcore.check_values(c,'adversarial_findings','lens')))"` → 11 today.
- Standing subjects 1–4. Subject 4 is sampled once per source (14 samples), not once per figure.
- WP10's post-pass-4 repair rows are a named subject.

**Comparator.** The rate is SUSTAINED findings per extraction written. Batch 23:
- `select count(*) from adversarial_findings where pass_id=4 and verdict='SUSTAINED'` → 13
- divided by its 30 extractions.

If the pilot's rate is higher, batch 25 halves the extraction budget. The budget is what keeps one pass's load comparable across batches.

---

## 8. Owner decisions

Two of these gate everything else: D1 and D3.

**D1. #166 waits for T1, then carries batch 23's repair rows (WP10).**
- Default: yes.
- Cost of the alternative (merge #166 now, red on D04): T1 merges with a blocking red it is forbidden to fix (rule 10). A separate data PR C is needed. Every data or schema PR stays red on D04 until C lands.
- Cost of the default: #166 waits for T1, and absorbs one blob conflict and any cron conflicts (cheap, rule 3).

**D2. UG in `JurisdictionCode`.**
- Default: admit, with the comment "declared for PR #165's rows, which are not unwound; outside research scope by the 2026-09-28 ruling". The enum is the declared vocabulary of rows held, not the canonical 24.
- PT, FI and UN are admitted in WP7 as execution of that ruling.
- Cost of declining: `jurisdiction_db_vocabulary` (blocking) stays red on untouched main for every data or schema PR. The alternative is a compensating migration that the ruling declined.

**D3. Go-ahead for new branches and pushes.**
- `claude/process-gaps-t1-writers`, `-t2-contract` and `-t3-ledger` now; `-t4-two-phase-log` and `claude/research-batch-24-parameter-pilot` later.
- Without it, only #166 can move.

**D4. `.claude/settings.json` edits.**
- Default: approve agent edits. That covers T2's regenerated `SessionStart[0]` command (one command: `python3 scripts/generate/research_contract_hook.py --write`) and T3's `PostToolUse[1]` object. If the harness refuses the write, the owner runs that one command or applies the T3 hunk.
- Cost of declining T3: unlogged searches and R8 precedence stay without a reader. WP12's honest R8 text stands permanently, and T4 is never built.

The R16 sentence and the CLAUDE.md rule 7a edit are reviewed in their PRs (DG-REVIEW). They are not separate decisions.

---

## 9. Not verified

- **Harness PostToolUse behaviour for `WebSearch|WebFetch`.** Matcher semantics and payload field names (`tool_name`, `tool_input.query`, `tool_input.url`) are documented behaviour that was not exercised here.
- **Whether the harness lets an agent write `.claude/settings.json` today.** The last agent write was `611a975`, on 2026-09-10. The owner has written it since (`f6adf7a`).
- **The session record's §4.5 scratch-copy experiment** (promoting four terms tripped no content check) was not re-run; this task was read-only. Code reading supports it: `grep -rln base_parameters scripts/` names no content check that reads a parameter's direction or extraction count.
- **`test_verification_pipeline` exit 0 after deleting G01–G03.** Expected, not run.
- **WP8's title-first-segment assertion on batch 23** (whether typed titles occur in decoded text) was not run.
- **The R16 and R16-adjudicate counts after #166** depend on WP10's adjudication outcomes, which are judgements. The WP10 queries are the check.
- **`validate_pydantic_schemas --strict` drift contents.** Not run; it writes a temp DB.
- **PR #166's live CI state** (D04 and `jurisdiction_db_vocabulary` red) is taken from Report A and the session record; GitHub was not queried.
- **Pointer drift, not examined.** Batches 21 and 22 merged without moving `LATEST-RESEARCH`: `git log origin/main --format='%h %s' -3 -- sessions/LATEST-RESEARCH` shows batch 20 as the last move. Their R16-adjudicate debt is therefore seen only by `--all`. Whether that was deliberate was not examined.
