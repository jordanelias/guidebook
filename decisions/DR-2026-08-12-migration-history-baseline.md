# DR-2026-08-12 — Freeze and archive the migration history; compress it into a full baseline

**Status:** OPERATIVE — 2026-08-12.
**Decision by:** Owner instruction 2026-08-12 ("freeze and archive existing change history then
compress change history for fresh start"), plus the retirement instructions given in the same turn.
**Category:** D-SCHEMA. **Delegation:** DG-NON — owner-directed; captured, not originated.
**Amends:** `scripts/migrate_db.py`, `scripts/migrations/`, `data/guidebook.db`,
`scripts/tests/test_evidence_cell_state_2_3.py`, `scripts/tests/test_validate_evidence_state_2_4.py`.
**Closes:** the deferred alternative recorded at `DR-2026-08-12-specification-rename-and-replay-order`
§4(5) (D-0158) — *"a schema + data baseline squashing the history … deferred, not refused."*

---

## 1. The decision

**`scripts/migrations/057_baseline_2026-08-12.sql`** holds the complete schema **and** data as of
2026-08-12: 67 tables, 18 views, 77 indexes, 5,072 rows. It supersedes all 355 prior migration
files, which are **frozen and archived** at `_archived/scripts/migrations/` with a README —
mirroring their origin path, per the retire-here-don't-delete rule. `BASELINE_DATA_CUTOFF_TS` in
`scripts/migrate_db.py` moves past the last archived data migration.

## 2. Why

Replaying the history was the only proof that the committed database had not been hand-edited.
**That property is kept** — the baseline is still replayed and compared by the blocking
reproducibility gate. What is shed is the accumulated cost:

1. **Immutable data migrations pinned retired names forever.** Renaming `evidence_cell_state` to
   `specifications` collided with 19 of them and required a new ordering mechanism (`AFTER_DATA`,
   schema 056) purely to work around replay. D-0158 named this baseline as the larger answer.
2. **Most of what replayed no longer existed.** The 2026-08-06 clean-room reset and the 2026-08-12
   evidence-stage clearance emptied the evidence, source, gap, connection and specification tables.
   297 data migrations ran to insert rows a later migration deleted.
3. **Two test fixtures reconstructed schema by scanning migration files for literal table names.**
   That selector had to match immutable historical text, so a rename sweep rewrote it and the
   fixture silently built the wrong schema. Both now read the baseline via
   `scripts/tests/_baseline_ddl.py`, and the hand-copied rename replay — itself flagged by
   adversarial review as unlinked drift — is deleted rather than maintained.

The corpus is at its smallest right now: 5,072 rows, ~91% controlled vocabulary. This is the
cheapest the operation will ever be, and that timing is the decision's main argument.

## 3. What is preserved, not discarded

- The **319-row `data_migrations` ledger is baked into the baseline**, so every historical
  `migration_id`, timestamp and content hash stays queryable from the database.
- The 355 files remain readable at their origin-mirroring archive path.
- `db_meta`, the 158-row `decisions` table and every vocabulary table carry over intact.

## 4. Alternatives considered

1. **Keep replaying the full history.** Refused: it is what forced `AFTER_DATA` into existence and
   it would force a comparable workaround at every future rename.
2. **Schema-only baseline, keep the 297 data migrations.** Refused: it leaves the retired names,
   the deleted-row churn and the fixture fragility exactly as they were — it solves the cheap half.
3. **Delete the superseded files instead of archiving them.** Refused: they are the record of what
   was done and when. Guardrail 2 is retire, never delete.
4. **Defer until the corpus is repopulated.** Refused on cost: every row added between now and then
   makes the baseline larger and the freeze more disruptive.

## 5. Retirements executed under the same instruction

Same rationale — a superseded artifact is frozen and archived, never deleted, and never left
rendered where it can be read as current.

| Retired to | What | Why |
|---|---|---|
| `_archived/site/populations/{dbl,neu,ofs,upl,vis}.html` | Five rendered population pages | Their codes were retired by the 2026-07-23 population schema replacement (`VIS→BLIND`, `UPL→LMB`, `DBL→DEAFBLIND`, `NEU→BRAIN`, `OFS→COM`). The generator refuses them, so they could not be regenerated. **Two are the banned umbrella framing in the project's own words** — `ofs.html` "Umbrella for orthostatic intolerance, dysautonomia, and chronic fatigue conditions", `neu.html` "General neurological category; includes MS, epilepsy, Parkinson, stroke sequelae" — so leaving them rendered kept teaching the erasure `DR-2026-07-22-work-from-axes` exists to stop |
| `_archived/specs/e-08.html` | The hand-authored Corridor Clear Width exemplar | `value-genealogy-worked-example-corridor-width.md` §7 found it rests on an unregistered anchor: a Koontz 2017 citation absent from the corpus, **all six** REF-IDs colliding with unrelated canonical rows, and a claimed source file that does not exist. Six links on the root `index.html` and the `population_page.py` link templates were repointed to the DB-generated `site/specs/e-08.html` |

Retiring the page does **not** answer whether Koontz 2017 exists; that question stays queued and is
recorded in `_archived/specs/README.md` and in the genealogy document itself.

> **CORRECTION, 2026-08-13 (owner instruction).** The sentence above is **withdrawn**. Keeping
> "does Koontz 2017 exist?" as a queued lead contradicts the clean slate this project has been
> operating under since the 2026-08-06 reset: the corpus starts empty, and every source enters
> through the research contract with its DOI pre-checked (R9) and every locator re-retrieved (R10).
> A citation inherited from a retired page — one whose six REF-IDs all collided with unrelated
> canonical rows — is not a lead. Carrying it forward would let a deleted artifact seed the new
> corpus, which is the circularity the reset exists to break. **There is no queued question.** The
> §7 finding in the genealogy document stands as a record of what the page contained. Corrected in
> `_archived/specs/README.md` and in that document; this DR keeps the original sentence visible
> rather than rewriting it, per the protocol's forward-only rule.

## 6. One consequence found by running the checks, and how it was resolved

Archiving migration 056 broke `adherence_log_audit` check #4: an attestation written hours earlier
cited it as an evidence path, and the path no longer resolved. The attestation is append-only and
was **not** rewritten. Instead the check now resolves a path that has been retired to `_archived/`,
because the archive mirrors origin paths precisely so references survive retirement. Verified in
both directions — the archived path passes, a genuinely missing path still fails.

## 6b. What the compression made visible — a finding, not a regression

The full-direction probe was re-run after the freeze (`audits/2026-08-12c-pipeline-probe-*`).
Surface coverage, silent passes, orphans and blocks are unchanged (481/481, 106, 6, 12). Two
sweeps moved, both for the same reason and both worth keeping:

- **`unwritable outputs` went 0 → 11.** The probe counted a data migration's `INSERT` as evidence
  that a table has a writer. With the 297 data migrations archived, that evidence is gone — and
  what it was masking is that **no live Python writes these eleven tables at all**:
  `citation_population_links`, `economics_entries`, `extraction_population_links`,
  `item_bpc_links`, `item_population_elaborations`, `probe_population_links`,
  `reasoning_doc_citations`, `search_candidates`, `search_coverage`, `search_languages`,
  `spec_value_probes`. They can be populated only by hand-written migration SQL. That is a true
  statement about the codebase that the history had been hiding, and it lands squarely on the
  pipeline stages this project is about to repopulate.
- **`unread inputs` went 19 → 10**, the mirror of the same effect: nine tables that read as
  "written but never read" no longer read as written either.

Neither is suppressed. The eleven unwritable tables are the concrete shape of "the pipeline has
no write path yet" and belong on the workplan, not in an exemption list.

## 7. Verification

| Gate | Result |
|---|---|
| Baseline applied to an empty DB vs the pre-baseline committed DB | **0** `sqlite_master` object differences either direction (name, type **and** SQL text) · **0** row-count divergences across all 67 tables · **0** content divergences compared row-by-row **including `rowid`** |
| `PRAGMA foreign_key_check` / `integrity_check` | empty / `ok`; all 18 views execute |
| `migrate_db.py --rebuild` | 1 schema migration, 0 data migrations |
| `migration_reproducibility.py` | **VERDICT: PASS** |
| `test_db_integrity.py` | **70/70** |
| Both rewired fixtures | ALL PASS; `_baseline_ddl.ddl_for()` verified to exit non-zero on an unknown object rather than build a short schema |

## 8. Reversal

By a new dated Decision Record and a forward migration. The archived files must **not** be restored
into `scripts/migrations/` — their effect is already in the baseline, and replaying one would apply
it twice.
