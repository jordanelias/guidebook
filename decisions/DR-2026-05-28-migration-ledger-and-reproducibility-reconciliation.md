# DR-2026-05-28 — Migration-Ledger Drift & DB Reproducibility Reconciliation

**Status:** ACCEPTED — option **3a** ratified by owner 2026-06-11 (see §Ratification). Step 2 (ledger backfill) was already executed in a prior session: `migrate_db.py --dry-run` reports 0 pending / 187 applied. **No further DB mutation required.**
**Authored:** 2026-05-28 (`session_2026-05-28-migration-ledger-diagnosis`)
**Doctrine SHA at authorship:** `61c7f95` (`governance/mission-and-epistemics.md`)
**Relates to:** the long-standing "Known broken #1 — data_migrations tracking drift" carried in session handoffs since 2026-05-23; GAP-290 (migration-reproducibility CI enforcement).

---

## Context

The `data_migrations` tracking drift has been a flagged-but-uncaptured "known broken" item across multiple sessions, always deferred as needing "a dedicated DR + reconciliation script." This session ran the diagnosis. It surfaced **three distinct issues** of different severity. All numbers below are measured at HEAD `0de84c6` by rebuilding a fresh DB to `/tmp` (`python3 scripts/migrate_db.py --rebuild`) and comparing table-by-table against the committed `data/guidebook.db` — a non-destructive procedure.

### Finding 1 — Ledger drift: 113 data migrations applied out-of-band, unrecorded (live footgun)

- Migration files on disk: 17 schema (`012_baseline_2026-05-15.sql` present), 157 data (154 post-baseline-cutoff `20260515000000`, 3 pre-cutoff intentionally skipped by the baseline convention in `migrate_db.py`).
- Committed DB `data_migrations` table: **66 rows**.
- `python3 scripts/migrate_db.py --dry-run` reports **113 data migrations pending** — i.e., their effects are present in the committed DB (applied out-of-band via direct `scripts/db.py` / SQL writes) but they are absent from the `data_migrations` ledger.

**Why this is a real problem (not cosmetic):** the next person to run `migrate_db.py` (normal mode) against the committed DB will attempt to **re-apply all 113** "pending" migrations, because the ledger says they haven't run. Re-applying already-applied data migrations risks duplicate INSERTs / UNIQUE violations / double-application for any non-idempotent migration. This is precisely the "address before the next regular migration session" warning.

### Finding 2 — Non-reproducible entity content from the `source-verification` job (rules out rebuild-replace)

The rebuild does **not** reproduce the committed DB on two entity tables:

| Table | Committed | Rebuild | Delta |
|---|---|---|---|
| `evidence_source_authors` | 1244 | 1079 | **+165 in committed** (across 38 ref_ids; e.g. REF-00032 has 19 authors committed vs 1 rebuilt) |
| `pipeline_runs` | 8 | 6 | **+2 in committed** (`2026-05-18 09:37`, `2026-05-25 09:45`) |

Root cause confirmed: the two extra `pipeline_runs` rows are `source-verification` job runs (commit `5007ede` = "source-verification: V1.2 run 2026-05-25 09:45"). The 165 extra author rows are that job's phase-4 PubMed author enrichment. **A recurring scheduled job writes real, correct entity content directly to the DB and commits it, with no corresponding migration file.** The data is genuine; it is simply not reproducible from migration history.

**Consequence:** `migrate_db.py --rebuild` followed by replacing the committed DB — the naive "make it reproducible" fix — **would silently delete 167 rows of correct author/run data.** It is categorically wrong and must not be done.

### Finding 3 — Architecture spec vs CI enforcement scope gap

`architecture/.../data_layer_pattern` states the committed DB "must be reproducible from its migration history." CI's BLOCKING reproducibility job (`audit.yml`, GAP-290) actually enforces a **narrower** contract: it compares only 7 invariants — `user_version` and `COUNT(*)` of `evidence_sources`, `citation_mining`, `source_slug_links`, `gaps`, `connections`, `items`. The committed DB passes all 7 (verified this session). The job does not check `evidence_source_authors`, `pipeline_runs`, or `data_migrations` — which is why CI is green despite Findings 1 and 2. The de-facto contract is "7 core entity invariants reproduce," not "the whole DB reproduces."

---

## Decision (PROPOSED)

A single reconciliation that resolves Finding 1 without triggering Finding 2's data-loss trap, plus a formalization that makes the real contract explicit.

1. **DO NOT rebuild-and-replace.** Documented above: loses 167 rows. The committed DB — not the rebuild — is authoritative for `evidence_source_authors` and `pipeline_runs`.

2. **Reconcile the ledger by content-preserving backfill, not by rebuild.** Insert the 113 missing post-cutoff `data_migrations` rows (migration_id + recomputed content_sha + reconciliation timestamp + `notes='reconciliation backfill per DR-2026-05-28: applied out-of-band, ledger corrected'`). This touches only the ledger table — **zero entity-data change** — and is truthful because the rebuild-compare proved the committed DB already contains the effects of all 154 post-cutoff migrations (all 7 core invariants match). Net effect: `--dry-run` returns 0 pending; the re-application footgun is closed.

3. **Formalize the source-verification exemption (the owner design choice).** Pick one:
   - **(3a) Exempt by ownership** *(recommended)* — declare `evidence_source_authors` and `pipeline_runs` as "job-owned" tables for which the `source-verification` scheduled job is the authoritative writer; document that these are deliberately outside the migration-reproducibility contract; align the architecture wording to CI's actual 7-invariant scope (or add these tables to the job-owned exemption list explicitly). Lowest friction; matches current reality (enrichment/log tables, not core synthesis content).
   - **(3b) Make the job reproducible** — have `source-verification` emit a data migration snapshotting its writes each run, so the full DB becomes rebuild-reproducible. Higher fidelity to the original invariant; more job-side engineering.

4. **(Optional, future) Decide the ledger end-state for pre-cutoff rows.** The committed ledger also holds ~25 pre-cutoff rows (ts `20260511`–`20260514`) that a rebuild does not generate. Whether the ledger should track pre-baseline history or match rebuild exactly is a separate, lower-priority cleanup; not required to close the footgun.

---

## Why no DB mutation was performed this session

The safe reconciliation (step 2) is unambiguous in mechanism but entangled with the step-3 design choice the owner must ratify (if 3b is chosen, the reconciliation co-ships with a job change). Mutating the authoritative data layer — even the ledger — on a freshly-discovered, design-entangled reproducibility issue under a general authorization is the kind of corner-cut `handoff_under_pressure` exists to prevent. The integrity-maximizing action this turn was to diagnose precisely, **rule out the data-losing "obvious fix,"** and capture a ratifiable decision. Execution (step 2 ± step 3) is a focused follow-up: a one-line owner go-ahead suffices, and the backfill is non-destructive and reversible.

---

## Decision rationale per mission test (abbrev.)

Verifiable (test 7): every figure is reproducible by re-running `--dry-run` + `--rebuild`-compare against HEAD. Acknowledges non-uniformity (test 2): preserves the source-verification-owned content rather than flattening it into a rebuild. Surfaces convergence/divergence (test 4): makes the architecture-vs-CI contract gap explicit instead of letting green CI imply full reproducibility.

## Deliverables

**This session (diagnosis + DR):** this DR + its attestation. No code, no DB write.
**Follow-up (post-ratification):** ledger backfill script for the 113 rows (step 2); the chosen step-3 formalization; optional step-4 cleanup.

---

## Ratification (2026-06-11)

**Doctrine SHA at ratification:** `3da73bd` (was `61c7f95` at authorship).
**Decided by owner:** option **3a — Exempt by ownership** (session `session_2026-06-11-stage-4.3-gate-closure`, Stage 4.3 gate G1).

**1. Step 2 (ledger backfill) — already executed.** A prior session ran `scripts/reconcile_ledger_dr_2026_05_28.py` against the authoritative DB. Re-measured at current HEAD: `migrate_db.py --dry-run` → **0 pending, 187 applied**; `data_migrations` ledger = 187 rows. The re-application footgun is closed. No further backfill needed.

**2. Step 3a (formalization) — adopted.** `evidence_source_authors` and `pipeline_runs` are hereby declared **job-owned tables**, deliberately outside the migration-reproducibility contract. The migration-reproducibility invariant covers exactly the **7 core invariants** enforced by `.github/workflows/audit.yml` (GAP-290): `PRAGMA user_version` + `COUNT(*)` of `evidence_sources`, `citation_mining`, `source_slug_links`, `gaps`, `connections`, `items`. These 7 cover all synthesis-bearing content and reproduce fully from migration history.

**3. Write-contract for job-owned tables.** The `source-verification` scheduled job (`.github/workflows/resolve-dois.yml`, `verify-urls.yml`, and the V1.x source-verification runs) is the **authoritative writer** for `evidence_source_authors` (PubMed author enrichment) and `pipeline_runs` (run log). These jobs MAY write these two tables directly, outside the migration framework, and commit the result; such writes are NOT a reproducibility-contract violation. Any OTHER table written outside migrations remains a violation. Adding a table to the job-owned exemption requires a new DR.

**4. Architecture alignment — OWNER ACTION REQUIRED.** `architecture/…/<data_layer_pattern>` still states the committed DB "must be reproducible from its migration history… any direct DB write that bypasses migrations fails this check." Per 3a this should be amended to scope the invariant to the 7 core invariants and name the two job-owned exemptions. Exact suggested wording is provided in the session report. This layer is owner-paste (project-knowledge copy); it is not changed by this commit.

**Code formalization landed this commit:** the `.github/workflows/audit.yml` reproducibility job is annotated with the explicit job-owned exemption list + rationale (behavior unchanged — the job already checked only the 7 invariants).
