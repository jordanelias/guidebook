# Batch 24 — orientation, corrections, nine parameters seeded from the existing terms, and a scan-contract catalogue plan (no searches, no admissions, no extractions)

**Session id:** `session_2026-10-09-research-batch-24-parameter-pilot`
**Branch:** `ccr-544a80b2-4d4ils`
**Session kind:** research (vocabulary rows only) plus planning working papers. No searches, no admissions, no extractions, no schema, script or check change.
**Pointers:** `sessions/LATEST` (the continuity pointer: where did work leave off) moves to this session. `sessions/LATEST-RESEARCH` is NOT moved: this is not an acquisition batch, and moving it would point the blocking batch gate at a session with no admissions.

**Derive every figure.** Re-run the command beside a number rather than trust the sentence.

---

## 0. What this session wrote to the database

Nine `base_parameters` rows (ids 4 to 12) through `scripts/migrations/data_20261009055057_2026-10-09-research-batch-24-parameter-pilot.sql` (9 inserts, 0 updates, 0 deletes in its `-- Totals` header), then two `terms` definition updates (TERM-003 and TERM-005, the two whose definitions stated a floor or a ceiling) through `scripts/migrations/data_20261010000310_2026-10-09-research-batch-24-parameter-pilot.sql` (0 inserts, 2 updates, 0 deletes). Nothing else. The second migration is the repair for a `/code-review` finding; its replay is `replay/amend-term-definitions.sh`. The rows were written on a scratch copy with `db.py add-parameter` (replay: `scratchpad/session_2026-10-09-research-batch-24-parameter-pilot/replay/populate-parameters.sh`), captured with `emit_batch_sql.py`, and applied with `migrate_db.py`. The canonical blob's sha256 did not move until the migration.

```
python3 - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
print(c.execute("select parameter_id, term_id, accessibility_direction from base_parameters order by 1").fetchall())
print(c.execute("select count(*) from base_parameters where created_by_session = 'session_2026-10-09-research-batch-24-parameter-pilot'").fetchone())
PY
```

The nine: corridor width (TERM-002), turning circle (TERM-003), operating force (TERM-005), reverberation time (TERM-007), LRV contrast (TERM-011), door width (TERM-021), colour temperature (TERM-024), headroom clearance (TERM-061), ramp run length (TERM-091). All are existing base-vocabulary terms. None carries a direction; direction is left unset until an admitted source states which way is better.

## 1. What happened

1. Orientation from live state. The state report said specification 8 "stands at 5%" and recommended retrieving the 2009 Vredenburgh study's full text. Both were wrong (section 2).
2. A read-only adjudication by a Fable agent on how to resolve the open issues. Its report was spot-checked; two of its claims were corrected (see section 2).
3. The owner asked for a parameter list large enough to scan every source against. Parameter names may only be minted from an observed source phrase (the 2026-09-09 ruling), so nine existing quantity terms were promoted and a larger harvest was planned. A six-agent scan of batch 23's saved texts was started and stopped by the owner after the owner pointed out that one slug's search results cannot seed a general list. Two scan outputs (52 items) exist only in the harness scratchpad and are not data.
4. The owner pointed at the existing lead material (`references/standards-registry.md`, the verified-source files, `source_locators`, `research_code_leads`, the pre-reset database). A worklist was built from it: `scratchpad/session_2026-10-09-research-batch-24-parameter-pilot/major-sources-worklist.md`.
5. A catalogue plan (v1) was written, critiqued by a read-only Fable 5.1 agent on the owner's commission (verbatim: `catalogue-plan-critique-fable.md`), and rewritten by an Opus agent as `catalogue-plan-v2.md`. Plan v1 failed three of the owner's four requirements; v2 is built to meet them.
6. Owner answers to D1, D2, D3 and D8 were received and recorded as addenda to v2 and in the ledger.

## 2. Corrections to this session's own earlier statements

- "Specification 8 stands at 5%": wrong. All eight specifications are retired (`select count(*) from specifications where retired_at is null` gives 0).
- Recommended next action "retrieve REF-01002's full text": closed by the owner's 2026-09-25 ruling; GAP-016 is NOT-ADDRESSABLE. The session read only the first 1,800 characters of the gap and missed its correction block.
- "Full text is saved for only 14 of 53 sources": wrong. 49 of 53 have a saved file (`catalogue-plan-v2.md` section 12, command A1). The session had counted only derived `-text.txt` files.
- The adjudicator's claim of "0 PROPOSED decisions" was wrong: `select count(*) from decisions where status='PROPOSED'` gives 2.
- A session-open misrouting: ten read-only commands run before `/session-open` were logged into batch 23's `commands.jsonl`. They were moved to `scratchpad/session_2026-10-08-orientation-state-and-adjudication/commands.jsonl`, an orientation folder with no session record and no database rows (the orientation turns that preceded `/session-open`; count with `wc -l`), and batch 23's file was restored to its committed state with `git checkout`. This session's own `commands.jsonl` begins at `/session-open`; the orientation folder is part of this session's record.
- The nine migrated rows carry one identical hand-typed note. Its clause "no source adjudication behind it" is false for parameter 12 (TERM-091 holds a NAMES-NEW adjudication from batch 20), and the note's other clauses restate what the schema already derives (direction unset, who asked). The first migration is immutable once committed (`CLAUDE.md` rule 3), so it is not re-emitted. **Owed before this pull request merges:** after tooling T1 merges, `db.py annotate-parameter` (T1 adds it; it appends a dated line and never overwrites) is run on the nine rows through a compensating data migration. The false statement stands in the meantime and is recorded here, in the ledger entry's session record pointer, and in the pull request.
- The `/code-review` of this branch (fourteen findings) is answered in section 7.

## 3. Owner statements

All recorded verbatim in `references/project-standards.md`, "Owner statements 2026-10-09". The 03:08 answer "2 ..yes? like, one pulled from another slug? should be yes, but we still tag it for follow up later" was ambiguous; D1 resolved it (cross-slug figure allowed and tagged; skimmed figure not publishable; a figure read in full but still `preliminary` is NOT settled). D3 ("keep the rule") was qualified immediately by "D3 for parameter terms? it can be pulled from previous catalogues of entries for prepopulating"; the owner then selected the code and standards registries and the pre-reset corpus terms (not the old Part 4 item names) as the permitted catalogues, with the guard "Screen, then you approve" and a second branch for the first tooling pull request. Nothing was minted from any previous catalogue.

## 4. Disclosures

1. **The nine rows reached this branch without a pull request, a record or an attestation** when they were committed in `a8b7c11` (`[skip ci]`). This record and its attestation are the repair. The owner's D2 ("yes") is the review.
2. **No adversarial pass.** The rows are in `base_parameters`, which is outside the 2026-08-19 rule's list of research tables (`python3 scripts/audit/adversarial_pass_audit.py --session session_2026-10-09-research-batch-24-parameter-pilot` reports NOTHING-IN-SCOPE). No gate examines the nine themselves: eight have no adjudication behind their term. The owner's recorded review is the only check.
3. **A critique of a plan was run.** The 2026-08-19 rule bars critiques of plans. The owner commissioned this one, for the catalogue plan only; the supersession is recorded in prose in the ledger.
4. **Derived outputs were regenerated** with `scripts/regenerate_derived.sh` after each migration, as the blocking freshness checks require, and the context map with `python3 scripts/generate/context_map.py`. The other advisory freshness checks (site pages) were stale on `main` before this session and were not touched.
5. **Commits carry `[skip ci]`**, because they carry only append-only logs, working papers and the rows; the final push to the pull request does not.
6. **Agent work.** Read-only agents scanned, adjudicated, critiqued and drafted. The Opus agent wrote only `catalogue-plan-v2.md`. The orchestrator verified a sample of their claims (listed in the critique file) and did not verify the rest.
7. **Edits to a closed session's file.** Three one-paragraph `SUPERSEDED IN PART` markers were inserted into `scratchpad/session_2026-10-01-research-batch-23/process-gap-remediation-plan.md`, which the back-pointer grammar requires (currency lives at the superseded text).

## 5. Gates

Measured 2026-10-10 after the second migration, the code-review repairs, and the regenerated outputs; the figures are this run's, so re-run rather than trust them.

- `python3 scripts/run_checks.py --changed-from origin/main --explain`: PASS, 62 green, 7 nothing-in-scope, 9 advisory failures, 0 blocking failures. The nine advisory failures are `migration_reproducibility_deep`, `validate_schema_cross_check`, `validate_pydantic_schemas`, `retired_vocabulary`, `research_protocol_audit`, `metadata_integrity_audit`, `validate_reasoning`, `site_pages_fresh` and `source_locators_integrity`, all present on `main` before this session (`context_map_fresh` was a tenth until this session regenerated the map). Nothing-in-scope includes `adversarial_pass_recorded` (this session wrote to no table on the rule's list) and `search_log_completeness` (no search was run).
- `python3 scripts/tests/test_db_integrity.py`: 71/71. K01, K02 and C10 still examine nothing (no live specification).
- `python3 scripts/migrate_db.py --rebuild`: reproduces the nine `base_parameters` rows and the two amended definitions exactly.
- `python3 scripts/audit/research_batch_dod.py --session session_2026-10-01-research-batch-23`: COMPLIANT.
- **`python3 scripts/audit/research_batch_dod.py --session session_2026-10-09-research-batch-24-parameter-pilot`: NON-COMPLIANT, 3 rules unmet (R1, R9a, R9b).** This is `/batch-done`'s own first command and it fails by design: the session admitted no source, and those rules count admissions. This paragraph is the explicit reasoned waiver that command asks for; the owner reads it on the pull request. The batch is *not* finished in `/batch-done`'s sense, because it is not an acquisition batch.
- `python3 scripts/audit/research_batch_dod.py --all` and `--check-baseline origin/main`: COMPLIANT. R16 debt is now below its old baseline because TERM-091 is promoted, and the baseline file is lowered to the live value in this pull request (the ratchet only goes down). Tooling T1 also edits that file, so whichever pull request merges second resolves a one-line conflict in it.
- `python3 scripts/audit/supersession_backpointer_audit.py`: PASS (it prints how many `SUPERSEDES` lines it examined; re-run for the count).
- The attestation validates against `schemas/attestation.schema.json`.
- `scripts/regenerate_derived.sh` and `scripts/generate/context_map.py --check` pass.

## 6. What the next session takes

1. **T1, the tooling pull request** (`catalogue-plan-v2.md` section 4.2, items 1 to 5, approved by the owner as D8): its own pull request off `main` (branch `claude/t1-scan-contract-tooling`, which the owner approved), merged BEFORE this branch's pull request and before any bulk promotion. This branch's pull request was opened first and waits. Both change `data/guidebook.db` and `PRAGMA user_version`, so the second to merge takes `main`'s blob and re-runs `python3 scripts/migrate_db.py`. T1 was built by a subagent and carries more than items 1 to 5 (derive: `git diff --stat origin/main..claude/t1-scan-contract-tooling`); the extra items are for the owner to accept or strike (ledger entry, item 5). It had not been reviewed or gated by the orchestrator when this record was written, and no pull request exists for it. **Owed after T1 merges and before this pull request merges:** the compensating migration for the nine notes (section 2).
2. Read the two permitted catalogues for candidate names (read-only), screen them, and bring the one approval table to the owner before anything is minted.
3. Phase P3: read what is already held against the ten parameters, after T1.
4. Undecided: D4 to D7, D9 to D11, D13.

## 7. Answers to the code review

A `/code-review` of this branch returned fourteen findings. Disposition of each, by what the finding said:

| Finding | Disposition |
|---|---|
| The nine migrated notes are identical, restate derived facts, and are false for parameter 12 | Not re-emitted (the migration is immutable once committed). Compensating migration owed after T1 merges (section 2). |
| Ledger item 7 presents the cap withdrawal as an owner statement | Reworded: the budgets lapse with the scope they budgeted; the one-source review unit is the session's recommendation, not an owner statement. |
| Ledger item 4 dropped the `[ASSUMPTION]` label on "skimmed" | Restored, with the owner's actual words quoted. |
| `/batch-done` on this session's own stem is NON-COMPLIANT | Disclosed in section 5 and the attestation as the explicit waiver; the failure is by design (no admissions). |
| No mark at the 2026-09-09 naming clause; the CONDITION omits naming and minting | Marks added at the 2026-09-09 and 2026-08-19 entries; CONDITION and ACTION extended. The audit's raw-text target count (`supersession_backpointer_audit.py`) is not changed here (rule 10: tooling ships apart). |
| TERM-003 and TERM-005 definitions state a direction | Repaired through a second data migration with `amend-term`. |
| Ledger quote of the 20:22 commission dropped an "s" | Corrected; every quote in the entry was re-checked against the transcript. |
| The "new parameters up to four" budget is unmarked | Marked, with a `SUPERSEDES` line and a back-pointer. |
| Attestation says the ten commands were moved to this session's log | Corrected to name the orientation folder (section 2). |
| The context map is stale | Regenerated. |
| The R16 baseline sits at its old value | Lowered to the live value. |
| The replay script takes its session stem from `CURRENT` | Pinned. |
| Documents disagree on pull-request order and T1's contents | Reconciled in the ledger (items 3 and 5), plan v2 Addendum 4, and section 6. |
| Plan v1 and the worklist carry claims later found wrong | A pointer to the correction was added at the head of each; the text below is left as written. |

