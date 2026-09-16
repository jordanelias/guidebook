# Idempotency audit — write paths in the guidebook pipeline

Method: copied `data/guidebook.db` to `/tmp/idem/scratch.db` (and fresh copies per test),
pointed `GUIDEBOOK_DB_PATH` at the copy INLINE on every call, and ran the interesting
commands **twice with identical arguments**, diffing row counts / files before and after.
Canonical `data/guidebook.db` was never written. No live network calls were made;
`retrieval_log.fetch()` is classified from code only, per instructions.

Legend: **IDEMPOTENT** (2nd run no-op, same state) · **REFUSING** (2nd run cleanly
refused, nothing written) · **DUPLICATING** (2nd run silently writes a second row/effect —
dangerous) · **DELIBERATELY-DUP** (duplicates by design, and the design is documented).

---

## 1. `scripts/db.py` subcommands (full list from `--help`)

### Priority commands — executed twice against a scratch copy

| Command | Class | Evidence |
|---|---|---|
| `add-source` | REFUSING | Row 1 succeeds (`REF-00983`). Row 2: `REFUSING: REF-00983 already exists. R9: cross-file...`. `evidence_sources` count stayed 1. Mechanism: `insert_evidence_source` pre-checks `ref_id` (db.py:2986-2995) and cross-checks the DOI case-folded against both `evidence_sources` and `source_locators` (db.py:3009-3031). |
| `observe-term` | IDEMPOTENT | Call 1 → `{"observation_id":1,"created":true}`. Call 2 (same ref_id+surface_form+language) → `{"observation_id":1,"created":false,"reason":"already observed"}`. `observed_terms` count stayed 1. Mechanism: db.py:3505-3511, keyed on `(ref_id, surface_form, language)`. |
| `add-term` | REFUSING | Call 1 mints `TERM-089`. Call 2 (same `--canonical-en`, new rationale) → `REFUSING: 'wobble corridor gap width' is already TERM TERM-089...`. `terms` count stayed 1. Mechanism: case-insensitive clash check, db.py:3619-3626. |
| `add-parameter` | REFUSING | Call 1 mints parameter 3 for `TERM-089`. Call 2 (same term-id) → `REFUSING: TERM-089 is already parameter 3... One parameter per term`. `base_parameters` count stayed 1. Mechanism: db.py:3909-3917 (also backed by a real UNIQUE on `term_id`). |
| `add-extraction` | **DELIBERATELY-DUP** | Call 1 writes extraction 11. Call 2 (byte-identical ref/parameter/claim) prints `NOTE: REF-00983 already carries 1 extraction(s) for parameter 3 ([11]). Writing another — evidence to judgment is 1:N (D-0168)...` and writes extraction 12. Count went 0→1→2. Mechanism: **no** uniqueness on `(ref_id, parameter_id)`, documented at db.py:4846-4856 as the D-0168 1:N fan-out *and* the DR-2026-08-19 §7 dissent contest, both intentional. |
| `add-population-match` | **DELIBERATELY-DUP** | Exactly the CLAUDE.md §4 case. Call 1 writes `idem-audit-session-REF-00983-ALL`. Call 2 prints `NOTE: ... already graded by [...]. Writing a second row -- divergent grades read as a contest`, writes `...-ALL-2`. Count 0→1→2. Mechanism: db.py:5804-5842. |
| `log-search` | **DUPLICATING** | Two back-to-back calls with identical slug/query-text/prior-expectation produced exec_id 29 **and** exec_id 30, both persisted, no note, no refusal. `search_executions` is a pure append-only log (db.py:415-538) with no dedup on content — by design for legitimate re-runs of the same query, but nothing distinguishes an intentional re-search from an accidental double-submit. |
| `log-mining` | IDEMPOTENT | Call 1 inserts one `citation_mining` row (slug, REF-00983). Call 2 (same args, different deferred-reason text) **updates the same row in place** (`forward=1`, `deferred_reason` overwritten, `updated_at` bumped) — row count stayed 1. Mechanism: keyed lookup on `(slug, global_ref_id)`, db.py:280-293. |
| `add-candidate` | **DUPLICATING** | Two identical calls (`--found-under-slug`, `--disposition OUT-OF-SCOPE`, `--title "duplicate candidate test"`) produced candidate_id 61 **and** 62. No dedup, no NOTE, no refusal. Mechanism: db.py:5771-5773 — `candidate_id` is `MAX(candidate_id)+1` computed fresh per call; nothing checks (found_under_slug, title) for a prior row. |
| `adjudicate-term` | **DELIBERATELY-DUP** | Same mechanic as `add-population-match`, explicitly cross-referenced in the code (db.py:3522-3526). Call 1 on a fresh observation writes adjudication 2 (`contested:false`). Call 2, **identical args**, prints `NOTE: observation 2 ... already adjudicated ... Writing a second row`, writes adjudication 3 (`contested:true`). Count 0→1→2. |

### Remaining `db.py` writers — classified by code inspection, several spot-executed

| Command | Class | Basis |
|---|---|---|
| `add-jurisdictional-value` | REFUSING | Executed: refuses at `item_code not in items` (items is empty — the item-layer-deleted state, CLAUDE.md §4/§7) before the `jv_id` question even arises. Clean message every time. |
| `add-economics-entry` | REFUSING (crash) | Executed: `--entry-id` is caller-supplied and `entry_id` is `TEXT PRIMARY KEY`. 2nd identical call → uncaught `sqlite3.IntegrityError: UNIQUE constraint failed: economics_entries.entry_id`. No duplicate persisted, but it is a traceback, not a `Refusal` sentence. |
| `add-case-study` | REFUSING | Explicit `case_study_id` clash check, db.py:5955-5956. |
| `add-code-lead` | REFUSING | Dedup on `(jurisdiction, standard_name)`, db.py:6004-6011. |
| `correct-source` | IDEMPOTENT | Skips the UPDATE when the payload-derived value already equals the stored one, db.py:3138-3139. |
| `amend-search` | IDEMPOTENT (+ REFUSING sub-case) | Appending the same note twice is a no-op (`"reason": "this amendment is already on the row"`, db.py:3207-3210); re-raising `harm_finding` when already 1 is refused (monotonic flag, db.py:3223-3225). |
| `resolve-candidate` | **DUPLICATING** | Executed: called twice with the same `--redescription` on candidate 61. Both calls return success (`was/now: OUT-OF-SCOPE`); `notes` ends up with the **same "RESOLVED ... re-described..." tail appended twice**, verbatim. No new row, but the prose record of the resolution is silently duplicated — no check on disposition already being resolved (db.py:3260-3286). |
| `amend-source` | IDEMPOTENT | `if (was or "").strip() == replacement: return {"changed": False}`, db.py:3358-3359. |
| `update-locator` | IDEMPOTENT | `if row["status"] == status: return {"changed": False}`, db.py:3466-3467. |
| `set-parameter-direction` | REFUSING | Re-stating a direction is refused once `accessibility_direction` is set, db.py:3974-3981. |
| `add-icf-code` | REFUSING | Clash on `icf_code`, db.py:4148-4152. |
| `set-icf-title` | REFUSING | Overwriting an existing title is refused, db.py:4205-4210. |
| `add-population-icf-link` | REFUSING | UNIQUE triple `(population, icf_code, mechanism)`, refused with the row named, db.py:4086-4091. |
| `raise-determination-gate` | **DUPLICATING** | Executed: two identical calls (`--parameter-id 3 --identity ALL --verdict UNLINKED --detail "..."`) produced gate_id **1 and 2**, both open, no dedup, no NOTE. This is the most consequential DUPLICATING case in `db.py` proper — see ranking below. |
| `resolve-determination-gate` | REFUSING | Re-resolving an already-resolved gate is refused (`resolved_at` check), db.py:3358-3363 region (3g). |
| `add-medical` | REFUSING | Clash on `medical_code`, db.py:3770-3776. |
| `relate-extraction` | REFUSING | Exact-edge dedup `(from_extraction_id, relation, to_extraction_id/to_label)`, db.py:4686-4696. |
| `repoint-extraction-relation` | REFUSING | Explicit dup check before repointing, db.py:5268-5276. |
| `amend-extraction` | IDEMPOTENT | `if old == value: return {"changed": False}`, db.py:5366-5368. |
| `derive-extraction` | **DELIBERATELY-DUP** (inherited) | Thin wrapper over `insert_extraction`; inherits its documented 1:N/dissent behaviour. Not separately executed. |
| `add-locator` | REFUSING | `ref_id` existence check + case-folded DOI dedup across two tables, db.py:6036-6054. |
| `add-gap` | **DUPLICATING** | Executed: two identical calls produced `GAP-001` and `GAP-002`. `gap_id` is `next_gap_id()` computed fresh **at CLI dispatch time**, before `insert_gap` runs — no content dedup at all (db.py:2015-2029, `next_gap_id` at 174-183). |
| `close-gap` | IDEMPOTENT | Plain UPDATE keyed on `gap_id`; re-closing with the same status is a no-op end state. |
| `add-connection` | REFUSING (crash) | Executed: `--con-id` is caller-required and `con_id` is `TEXT PRIMARY KEY`. 2nd identical call → uncaught `sqlite3.IntegrityError: UNIQUE constraint failed: connections.con_id`. No duplicate persisted. |
| `update-connection` | IDEMPOTENT | Plain UPDATE by `con_id`. |
| `upsert-coverage` / `upsert-language` | REFUSING | Always refuse — the grids are frozen (`FrozenGridError`), db.py:380-412. |
| `update-bpc` (`update_bpc_metadata`) | IDEMPOTENT | Real upsert: UPDATE if the slug row exists, else INSERT, db.py:2751-2769. |
| `add-conflict` | **DUPLICATING** | Executed: two identical calls (no `--conflict-id`) produced `CONF-0001` and `CONF-0002`. Same auto-ID-with-no-content-dedup shape as `add-gap` (db.py:2535, `next_conf_id` at 746-755). |
| `update-conflict` | IDEMPOTENT | Plain field UPDATE by `conflict_id`. |
| `delete-connection` | IDEMPOTENT | Hard DELETE; naturally idempotent (2nd call matches 0 rows). |
| `add-item` | REFUSING | Always refuses — item layer deleted, db.py:2571 ff. |
| `add-audit-run` | REFUSING (crash, unwritable) | Executed: `item_audit_runs.item_code` is `NOT NULL REFERENCES items(item_code)` and `items` holds 0 rows, so **every** call — not just the 2nd — dies with `sqlite3.IntegrityError: FOREIGN KEY constraint failed`. This is the CLAUDE.md §4 "FK into an emptied table" shape, on a second live table beyond `specifications`/`item_taxonomy_links`. |
| `update-audit-run` | IDEMPOTENT (moot) | Plain UPDATE by `run_id`; unreachable in practice since no row can ever be inserted. |
| `add-supersession-check` | **DUPLICATING** | Executed three times. Two calls issued **within the same wall-clock second** collided on the derived `check_id` (a hash of `slug|local_ref_id|checked_at|session`) and the 2nd crashed with `UNIQUE constraint failed: supersession_check.check_id` — but a 3rd call, same session, ~2 seconds later, sailed through and wrote a **second, fully duplicate** row for the identical `(slug, local_ref_id, ref_id, outcome)`. The "protection" seen on the fast repeat is an accident of clock granularity, not a designed dedup — there is no check on `(slug, local_ref_id, ref_id)` at all (db.py:5556-5586). |
| `add-gap-mining` | **DELIBERATELY-DUP** | Explicitly documented: "Append-only: multiple attempts per gap_id are allowed; the most recent row (MAX(attempt_at)) is the operative outcome" (db.py:5600-5604). Not separately executed; the doctrine is stated in the code. |
| `update-gap-addressability` | IDEMPOTENT | Plain UPDATE by `gap_id`. |
| Read-only (`gaps`, `connections`, `is-mined`, `coverage`, `synonyms`, `next-id`, `unmined*`, `conflicts`, `items`, `audit-runs`) | n/a | Not writers. |

---

## 2. `scripts/migrate_db.py`

**IDEMPOTENT — confirmed by execution.**

- Fresh copy of canonical, run twice: `Done. Schema at version 81; 0 data migration(s) applied.` both times; `sha256sum` of the DB file was **byte-identical** across both runs (`0a797814bf4e...`).
- Built a synthetic pending data migration (`data_<ts>_idem-test.sql`), applied once (`1 data migration(s) applied`, 1 row landed in `gaps`), then ran again: `0 data migration(s) applied`, row count stayed 1, `data_migrations` ledger held exactly one row for that `migration_id`.
- Mechanism: `applied_data_migrations()` reads `data_migrations.migration_id` (migrate_db.py:215-218) and `run_migrations()` skips anything already in that set (migrate_db.py:419-420). Schema migrations are gated the same way by `version <= current` (migrate_db.py:385-386).

`data_migrations` **does** prevent re-application, exactly as CLAUDE.md §3 rule 3 describes it (append-only, immutable, forward-fix-only).

---

## 3. `scripts/assess/assess_cell.py`

Both CLAUDE.md/runbook claims verified by execution (not just reading):

1. **`--stamp` is a real input, not `now()`.** Ran the identical determination (`--parameter-id 3 --identity ALL`, same `--stamp "2026-09-16 00:00:00"`) against **two independently-fresh copies** of the same starting scratch DB. `diff` of the two `--emit-sql` artifacts, excluding nothing, was **empty** — byte-identical, including the derivation_sha (`22372acb4cb4` on both).
2. **A second run for the same cell is refused by `idx_spec_row_identity`.** Re-ran the same command against the DB that already held the determination: `REFUSING: cell 3×ALL is ALREADY DETERMINED. specification_id 1, state 'stated', ... derivation_sha 22372acb4cb4 ...`. Nothing written, exit 1. Mechanism: `validate_cell_undetermined()` (assess_cell.py:1289-1339) restates the UNIQUE index's own COALESCE expression and refuses *before* any evidence gather, ahead of the raw `sqlite3.IntegrityError` the index itself would throw at INSERT time.

Classification: **REFUSING**, with the determinism claim independently confirmed.

---

## 4. `scripts/research/emit_batch_sql.py` and `scripts/emit_data_migration.py`

**`emit_batch_sql.py` — IDEMPOTENT (byte-stable).**
- Built-in `--selftest` asserts this directly ("output is deterministic") and passed 9/9.
- Independently re-verified on real data: ran it twice against the same (scratch, canonical) pair from the `assess_cell` test above. `diff`, excluding only the `-- Captured:` timestamp comment line, was **empty** across 90 lines / 36 inserts.

**`emit_data_migration.py` — DUPLICATING at the artifact level (important nuance).**
- The **body** is byte-stable: running it twice on the identical `--input` file with the identical `--session`/`--summary` produces two files whose content is identical except for the filename-echo line and the `-- Generated:` timestamp (verified by diff).
- But the **filename / `migration_id`** is a real wall-clock timestamp (`datetime.now(timezone.utc)`, emit_data_migration.py:750), never an input. Two runs one second apart produced **two separate files on disk** — `data_20260916043756_idem-audit-test.sql` and `data_20260916043757_idem-audit-test.sql` — each carrying the *same* INSERT statement. `--force-timestamp` exists to pin this, but is documented "advanced; for tests only" (line 686) and nothing in the normal workflow uses it.
- Consequence: nothing stops an operator (or a retried script) from emitting the same batch's SQL twice. Both files are legitimate, distinctly-named migrations; `migrate_db.py`'s dedup is keyed on `migration_id`, which differs between them, so **both would apply**. CLAUDE.md §4 itself notes migrations from different sessions "land cleanly on `main` — git merges them as text" — the same mechanism that makes concurrent sessions safe makes an accidental double-emit of *one* session's own batch invisible to every existing gate.

Classified DUPLICATING (not IDEMPOTENT) because the actually-produced artifact differs run to run and both artifacts are live, applicable migrations.

---

## 5. `scripts/regenerate_derived.sh`

Checked first: all three generators it calls (`tools/pipeline_completeness.py`, `tools/evidentiary_audit.py`, `tools/regenerate_vetting_surface.py`) open the DB `mode=ro` only (grep-verified). Safe to run.

**IDEMPOTENT — confirmed by execution.** Ran it twice on the unchanged DB:
- Run 1: `Wrote 0 changed / 5 total output files (all byte-identical to committed copies)`, both `--check` gates `OK`.
- Run 2: identical output, `git status --porcelain -- parts/ site/ tools/ audits/` empty before and after both runs.

---

## 6. `scripts/research/retrieval_log.py` `fetch()`

Classified from code only — no live network calls made, per instructions.

**DUPLICATING (append-only, no dedup on URL).** `fetch()` (retrieval_log.py:200-287) always:
- writes the artefact bytes to `retrieval-log/<session>/<sha256[:16]><ext>` (content-addressed, so re-fetching the *same bytes* does not duplicate the artefact file itself), and
- **unconditionally appends** one line to `manifest.jsonl` (`open(..., "a")`, line 265), regardless of whether an identical URL was already logged in that session.

There is no check against prior manifest lines for the same `url`. Fetching the same URL twice therefore produces two manifest lines. This is lower-severity than the DB-level duplications: the artefact bytes are deduplicated by hash, and a second identical manifest line is actually usable corroborating evidence (a *different* hash on refetch would indicate drift) rather than a corrupted count — but it is not documented as an intentional multi-attempt design the way `add-gap-mining` is, so it is filed here as DUPLICATING rather than DELIBERATELY-DUP.

---

## Summary counts

| Classification | Count |
|---|---|
| IDEMPOTENT | 18 (`observe-term`, `log-mining`, `correct-source`, `amend-search`, `amend-source`, `update-locator`, `amend-extraction`, `update-bpc`, `update-connection`, `update-conflict`, `delete-connection`, `update-gap-addressability`, `update-audit-run`, `close-gap`, plus `migrate_db.py`, `emit_batch_sql.py`, `regenerate_derived.sh`) |
| REFUSING | 21 (`add-source`, `add-term`, `add-parameter`, `add-case-study`, `add-code-lead`, `add-jurisdictional-value`, `add-economics-entry`, `set-parameter-direction`, `add-icf-code`, `set-icf-title`, `add-population-icf-link`, `resolve-determination-gate`, `add-medical`, `relate-extraction`, `repoint-extraction-relation`, `add-locator`, `add-connection`, `add-item`, `add-audit-run`, `upsert-coverage`/`upsert-language`, plus `assess_cell.py`) |
| DELIBERATELY-DUP | 5 (`add-population-match`, `adjudicate-term`, `add-extraction`, `derive-extraction`, `add-gap-mining`) |
| DUPLICATING | 9 (`log-search`, `add-candidate`, `add-gap`, `add-conflict`, `raise-determination-gate`, `add-supersession-check`, `resolve-candidate`, `emit_data_migration.py`, `retrieval_log.fetch()`) |

## Severity ranking of the DUPLICATING paths (most dangerous first)

1. **`emit_data_migration.py`** — the canonical write path itself. A double-emit produces two independently-applicable migration files carrying the SAME batch; `migrate_db.py` dedups only by `migration_id` (the differing timestamp), so both replay and an **entire batch's rows land twice in canonical**. No existing gate reads for this (`research_batch_dod.py` never compares migration file pairs or content hashes across files).
2. **`raise-determination-gate`** — duplicate open H4 gates on the same cell. `resolve-determination-gate` closes one `gate_id` at a time, so resolving the "first" twin leaves a live, unresolved twin silently still pinning the cell at `provisional`. Nothing in `research_batch_dod.py` reads `determination_gates` at all.
3. **`add-supersession-check`** — duplicates a DR-2026-05-24 compliance record with no warning (unlike `add-population-match`/`adjudicate-term`, there is no `NOTE:` printed). `research_batch_dod.py` never queries `supersession_check`.
4. **`log-search`** — inflates `search_executions` counts (`results_found`/`results_screened`/`results_admitted`) that R7 and R14 in `research_batch_dod.py` read; a duplicate could help a batch pass R7's screened/candidate ratio or mask thin coverage. R8 in the same file only detects **deletions** (`max(exec_id) > COUNT(*)`), not duplicate insertions — it would not fire.
5. **`add-candidate`** — inflates the `search_candidates` count R7 asserts against (`>= 1 per 25 screened`), which could mask under-screening. Not otherwise checked.
6. **`add-gap`** / **`add-conflict`** — duplicate open triage records; wastes review effort but doesn't corrupt evidence. Not checked by the DoD script.
7. **`resolve-candidate`** — duplicate text appended to one row's `notes`; no new row, low functional risk.
8. **`retrieval_log.fetch()`** — duplicate manifest line for a re-fetched URL; content-addressed artefact storage means no data loss, and a repeat fetch is arguably useful corroboration. Lowest severity of the nine.

**Cross-check against `scripts/audit/research_batch_dod.py`:** none of the nine DUPLICATING paths above are caught by any of its R1–R15 rules. The script counts `search_candidates` (R7) and integrity-checks `search_executions` only for row *deletion* (R8), checks DOI duplication only in `evidence_sources`/`source_locators` (R9/R9a/R9b), and checks `evidence_population_match` only for *presence* (R13, which explicitly does not read `match_grade`). It never references `determination_gates`, `supersession_check`, `gaps`, `conflicts`, or migration files at all.
