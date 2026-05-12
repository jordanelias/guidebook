# Handoff — Source Verification & Data Integrity
**As of 2026-05-12** · Repo: `jordanelias/guidebook` · Branch: `main`

---

## Where the project is

**Sources** — 675 total in `evidence_sources`. The verification gate per PI rule
#10 (`verification_status='VERIFIED'` AND `metadata_quality='COMPLETE'`) currently
admits **82 sources (12%)** for Phase E synthesis.

| Metric | Count | Note |
|---|---|---|
| Total sources | 675 | master inventory |
| VERIFIED | 285 (42%) | most via Channel 1 DOI pipeline |
| COMPLETE metadata | 126 (19%) | doubled from 67 by V1.2 enrichment |
| **Eligible for synthesis** | **82 (12%)** | rule #10 gate |
| Has DOI | 224 (33%) | 211 manual + 13 pipeline-resolved |
| Has ORCID | 58 / 1069 authors | was 0 pre-V1.2 |
| REVERTED (permanent skip) | 29 | false-positives + manual exclusions |

**DB structure** — 29 tables, 81-column `evidence_sources`, 13 migrations applied,
SQLite `integrity_check = ok`. All 8 foreign-key relationships verified clean
(zero orphans). All 6 enum columns clean (no out-of-vocabulary values).

**Items** — 91 active items. None currently linked to sources via
`bpc_source_slug` — that linkage is Phase F of the operative workplan, not yet
built. Items have valid PMP coverage (3/3 numerical-spec items walked).

**Verification channels** —
- **Channel 1 (DOI registries)**: production, V1.2. 6 phases. Runs weekly.
- **Channel 2 (URL verification)**: production, V1. Generic URL+title verifier
  with Wayback fallback. Runs bi-weekly. Only 6 sources currently have URLs to
  verify — URL discovery (per-publisher scrapers) is the bottleneck, not the
  verifier itself.
- **Channel 3 (Co-1 expert review)**: manual only. 34 sources have
  `co1_provenance` populated; 133 have `verified_by_tool='co1-manual-pre-pipeline'`.

---

## Operational commands

All commands run from the repo root.

### Run DB integrity check (35 checks, ~1 second)
```bash
python3 scripts/tests/test_db_integrity.py
```
**Use when:** before any commit involving DB or pipeline scripts; debugging a
suspected data issue; confirming a migration didn't break referential integrity.

Covers: 8 foreign-key relationships, 6 enum columns, 6 consistency invariants,
3 duplicate-detection checks, 6 schema-contract checks, 4 pipeline-run-health
checks, 3 evidence-chain checks.

Exits 0 on clean, 1 on any failure. Also runs automatically in CI on every push
that touches `data/` or pipeline scripts.

### Run DOI resolution pipeline (Channel 1)
**Production cadence:** automated Monday 06:00 UTC. Action runs without intervention.

**Manual trigger:** GitHub Actions UI → "Source verification pipeline (V1.2)" → Run workflow.

**Local dry-run** (safe — uses copy):
```bash
cp data/guidebook.db data/.test-copy.db
GUIDEBOOK_DB_PATH=data/.test-copy.db MAX_RESOLVE=20 RATE_LIMIT=0.3 \
    python3 scripts/resolve_dois.py
```
Environment knobs:
- `MAX_RESOLVE` — cap candidates attempted per run (default 500)
- `RATE_LIMIT` — seconds between API calls (default 5.0)
- `SKIP_NO_MATCH_DAYS` — retry window for NO-MATCH rows (default 30)

### Run URL verifier (Channel 2)
**Production cadence:** automated 1st and 15th of each month, 06:00 UTC.

**Manual trigger:** Actions UI → "URL verification (Channel 2 V1)" → Run workflow.

**Local dry-run:**
```bash
cp data/guidebook.db data/.test-copy.db
GUIDEBOOK_DB_PATH=data/.test-copy.db MAX_VERIFY=20 RATE_LIMIT=1.0 \
    python3 scripts/verify_urls.py
```
Environment knobs:
- `MAX_VERIFY` — cap URLs to attempt (default 500)
- `RATE_LIMIT` — seconds between requests (default 3.0)
- `USE_WAYBACK` — Wayback Machine fallback for dead URLs (default 1)

### Run Phase E readiness audit (per PI rule #10)
```bash
python3 scripts/audit_evidence_metadata.py
```
**Use when:** wanting to know how many BPCs are unblocked for synthesis.

Reports per-BPC eligibility based on the rule #10 gate. Current state:
2 READY BPCs, 65 BLOCKED on source quality, 14 EMPTY.

### Run Channel 1 pipeline test suite
```bash
python3 scripts/tests/test_verification_pipeline.py
```
18/18 tests. Covers Phase 4 enrichment, ORCID, COMPLETE promotion,
false-positive gates, NO-MATCH state, env vars.

### Run Channel 2 pipeline test suite
```bash
python3 scripts/tests/test_url_verifier.py
```
25/25 tests. Covers schema, title extraction, similarity, soft-404
detection, candidate query, retry windows, write idempotency.

### Inspect specific source state
```bash
python3 -c "
import sqlite3
c = sqlite3.connect('data/guidebook.db')
c.row_factory = sqlite3.Row
r = c.execute('SELECT * FROM evidence_sources WHERE ref_id=?', ('REF-00050',)).fetchone()
print({k: v for k, v in dict(r).items() if v is not None and v != ''})
"
```

### Inspect pipeline run history
```bash
python3 -c "
import sqlite3
c = sqlite3.connect('data/guidebook.db')
for r in c.execute('SELECT run_id, doi_before, doi_after, verified_before, verified_after, metadata_complete_before, metadata_complete_after FROM pipeline_runs ORDER BY started_at'):
    print(r)
"
```

---

## How the verification pipeline works

### Channel 1 — DOI resolution (`scripts/resolve_dois.py`, 1055 lines)

Six phases, each idempotent and rate-limited:

| Phase | What | API | Acceptance |
|---|---|---|---|
| **0** | Extract PMC IDs from `pub_title` text | none (regex) | mechanical |
| **1a** | PMID → DOI | NCBI ID Converter | NCBI returns DOI |
| **1b** | PMCID → DOI | NCBI ID Converter | NCBI returns DOI |
| **2a** | Person-author CrossRef structured query | CrossRef `/works` | author surname match + title overlap ≥2 words, ≥40% ratio + year ±2 |
| **2b** | Corporate-author CrossRef bibliographic query | CrossRef `/works` | publisher/author name match + title overlap |
| **3** | Standards via `type:standard` filter | CrossRef `/works` | publisher in {ISO, BSI, ANSI, DIN, etc.} + numeric token IN title (mandatory) + word overlap ≥2, ≥20% ratio |
| **4** | DOI-lookup enrichment of already-resolved rows | CrossRef `/works/{doi}` | populates pages, pub_month, language, subtype, citation_count, full author list, ORCID; promotes `metadata_quality` → `COMPLETE` |

**State machine per source row:**
- Never tried → `doi_resolution_outcome=NULL`, eligible
- Resolved → `doi_resolution_outcome=RESOLVED`, `verification_status=VERIFIED`,
  `verified_by_tool=<phase>`
- No match → `doi_resolution_outcome=NO-MATCH`, retried after 30 days
- Manually reverted → `doi_resolution_outcome=REVERTED`, **permanent skip**

**Crucial guards** (each enforced by tests):
- Numeric standard-number token must appear in CrossRef title (prevents PAS 6463 → IEC/PAS 63313 false match)
- NO-MATCH writes never overwrite existing `verification_status`
- REVERTED rows never re-enter any candidate pool
- All writes idempotent via central `write_verification()` function

### Channel 2 — URL verification (`scripts/verify_urls.py`, 504 lines)

Single-phase generic verifier:

1. Fetch URL with proper User-Agent, 20s timeout
2. Extract page title (prefers `citation_title` / `og:title` meta tags over `<title>`)
3. Fuzzy word-overlap similarity vs source's `pub_title`
4. Decision:
   - ≥0.50 → `VERIFIED` + `MATCHED`
   - ≥0.20 → `PROBABILISTIC` + `PARTIAL` (human review queue)
   - <0.20 → `NO-MATCH` (30-day retry)
   - HTTP 404/410 → try Wayback Machine; if snapshot matches → `WAYBACK-MATCH`; else `UNVERIFIED-CLOSED` + `DEAD-LINK`
   - DNS failure → `UNVERIFIED-CLOSED` + `DEAD-DNS` (no Wayback attempt)
   - HTTP 5xx/403/429/timeout → transient, no DB write, retry next run

**Operates entirely at corpus layer.** Does not consume BPC context. Verifies
URLs independent of which BPC declared them — matches the corrected architectural
flow (corpus is primary, BPCs derive from corpus).

---

## What still needs to happen

### Active automation (no work needed)
- Channel 1 weekly run — picks up remaining ~50 Phase 4 candidates, occasional
  Phase 2b/3 resolutions
- Channel 2 bi-weekly run — verifies the 6 URLs currently present
- DB integrity test on every push touching pipeline code

### Open work, ranked by leverage

| # | Work | Effort | Unblocks |
|---|---|---|---|
| 1 | **URL discovery for Channel 2** — populate `url` column for the ~580 sources without one. Either via per-publisher scrapers (DIN, CSA, JIS, GB, ABNT, 14 gov't portals) or via web-search shim. | 20–40h | Channel 2 from ceiling 6 to ~580 |
| 2 | **Items↔sources linking (Phase F)** — populate `items.bpc_source_slug` so the items table connects to the verified corpus. Currently 91/91 items have `bpc_source_slug=NULL`. | varies — depends on existing BPC source declarations | item validity tracking; supports the 9-step rule synthesis |
| 3 | **BPC reasoning documents (Phase E)** — apply the 9-step rule to BPCs whose sources are eligible. Currently 2 BPCs READY. | per-BPC effort: ~3–8h | actual synthesis output |
| 4 | **Co-1 review queue** — formalize Channel 3 with a tracked queue table and review log. Currently manual / scattered. | 4–8h | Channel 3 throughput tracking |
| 5 | **`superseded_by_ref_id` linkage on duplicate-DOI sets** — link the 14 intentional duplicates so the dedup-exception list can be retired. | 2h | cleaner duplicate detection |

### Known minor issues from review (not blocking)

- **Channel 2 commits one row at a time.** Fine at current pool size (6); needs batching to 10-row commits when pool grows past ~50. ~20 min when needed.
- **Scripts lack `conn.rollback()` on unhandled exception.** Partial-write state possible on unexpected errors. ~30 min to add. Low risk in steady state — pipeline runs complete cleanly.
- **`evidence_sources_v1_legacy` still present.** Migration backup table. Drop when comfortable that V2 schema has had a few months in production. Integrity test handles its absence gracefully.

---

## Repo file map

### Pipeline scripts
- `scripts/resolve_dois.py` — Channel 1 (V1.2, 6 phases)
- `scripts/verify_urls.py` — Channel 2 (V1)
- `scripts/audit_evidence_metadata.py` — Phase E readiness audit

### Tests (all currently passing)
- `scripts/tests/test_db_integrity.py` — **35 checks** (the main integrity tool)
- `scripts/tests/test_verification_pipeline.py` — Channel 1 (18 tests)
- `scripts/tests/test_url_verifier.py` — Channel 2 (25 tests)

### Workflows
- `.github/workflows/ci.yml` — 6 jobs including `db_integrity`. Runs on every push.
- `.github/workflows/resolve-dois.yml` — Channel 1 cron, weekly Monday 06:00 UTC
- `.github/workflows/verify-urls.yml` — Channel 2 cron, bi-weekly 1st/15th 06:00 UTC
- `.github/workflows/audit.yml` — broader governance audits

### Data
- `data/guidebook.db` — single source of truth, 81-column `evidence_sources`,
  29 tables, 13 migrations recorded

### State tables (append-only run logs)
- `pipeline_runs` — Channel 1 run history (5 records)
- `url_verification_runs` — Channel 2 run history (0 records — first run pending)
- `data_migrations` — schema migration log (13 records)
- `spec_value_probes` — PMP walk history (18 records)
- `item_audit_runs` — item audit history (87 records)

### Governance
- `audits/bpc-rewrite-workplan-2026-05-11.md` — operative workplan (Phases A–G)
- `references/audits/verification-pipeline-proposal-2026-05-12-v2.md` — original three-channel design
- `references/audits/v1-verification-pipeline-deployment-report-2026-05-12.md` — Channel 1 V1.0 deployment
- `decisions/DR-2026-05-09-adversarial-research-protocol.md` — PI rule #7
- `decisions/DR-2026-05-10-progressive-measurement-protocol.md` — PI rule #8

---

## Quick health check sequence

If you've stepped away and want to confirm everything's still good in 30 seconds:

```bash
# 1. DB integrity
python3 scripts/tests/test_db_integrity.py
# Expected: 35/35

# 2. Channel 1 pipeline tests
python3 scripts/tests/test_verification_pipeline.py
# Expected: 18/18

# 3. Channel 2 verifier tests
python3 scripts/tests/test_url_verifier.py
# Expected: 25/25

# 4. Recent pipeline run health
python3 -c "
import sqlite3
c = sqlite3.connect('data/guidebook.db')
n_runs = c.execute('SELECT COUNT(*) FROM pipeline_runs').fetchone()[0]
n_incomplete = c.execute('SELECT COUNT(*) FROM pipeline_runs WHERE completed_at IS NULL').fetchone()[0]
last = c.execute('SELECT run_id, total_resolved, metadata_complete_after FROM pipeline_runs ORDER BY started_at DESC LIMIT 1').fetchone()
print(f'Pipeline runs: {n_runs} ({n_incomplete} incomplete)')
print(f'Most recent: {last}')
"

# 5. Phase E eligibility (Channel 1 throughput indicator)
python3 -c "
import sqlite3
c = sqlite3.connect('data/guidebook.db')
e = c.execute(\"SELECT COUNT(*) FROM evidence_sources WHERE verification_status='VERIFIED' AND metadata_quality='COMPLETE'\").fetchone()[0]
print(f'Eligible for Phase E synthesis: {e}/675')
"
```

If all 4 first commands return clean and the last shows a number ≥82, the
pipeline is healthy. If eligible-count has decreased since 2026-05-12, something
regressed and the test_db_integrity output will identify what.

---

## Key invariants — never violate

1. **`verification_status` is the rule #10 gate.** Never set to VERIFIED without
   an audit trail (doi/url/pmid set OR `verified_by_tool` set).
2. **REVERTED is permanent.** Once `doi_resolution_outcome='REVERTED'`, the row
   is excluded from all future candidate pools. Reversal requires deliberate
   manual UPDATE with documented reason.
3. **NO-MATCH does not overwrite VERIFIED.** A failed retry attempt must never
   downgrade a previously successful verification.
4. **Migrations are append-only and logged.** Every `ALTER TABLE` /
   `CREATE TABLE IF NOT EXISTS` writes a row to `data_migrations`.
5. **State lives in SQLite, not in files.** No temp files for pipeline state —
   everything in `pipeline_runs` / `url_verification_runs`.
6. **PRAGMA foreign_keys = ON** at the start of every script that writes to
   the DB.

Test `test_db_integrity.py` enforces #1 (C01), #5 (E03/E04), #6 (set on conn).
Tests in the pipeline suites enforce #2 (D-group) and #3 (G01).
