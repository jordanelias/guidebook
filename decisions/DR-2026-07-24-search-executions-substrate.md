# DR-2026-07-24 — `search_executions` logged-search substrate (coverage-loop memory)

- **RATIFIED — owner directive 2026-07-24 ("Ratify all").** Register D-0151 `review_status:
  CONFIRMED`. Applied this session: `scripts/migrations/033_search_executions.sql`
  (`user_version` 32→33, table ships empty), `schemas/search_execution.py`, and the `v_coverage_*`
  views; legacy grids frozen read-only, not dropped. Rebuild reproducibility verified on the 7 CI
  invariants. The proposal text below is preserved as authored.
- Status: **PROPOSED — DG-REVIEW (agent decides, owner reviews before canonical).**
  Register entry D-0151 carries `review_status: PENDING`. The migration + Pydantic
  artifacts are *embedded here for review*; they are **not** yet placed in
  `scripts/migrations/` and **not** applied to `data/guidebook.db` (see §7 —
  applying an unratified schema migration would bump `PRAGMA user_version` and is
  itself the ratification act). Ratification = owner approval of this DR / PR merge.
- Date: 2026-07-24
- Category: **D-SCHEMA** (new table + views mirrored in a Pydantic model).
- Delegation: **DG-REVIEW** (decision-protocol §2.2 default for schema that satisfies
  already-canonical methodology; this table is called for verbatim by an already-ratified
  workplan, so it is *application of existing methodology*, not novel doctrine).
- Prepared by: Claude (Opus), operationalizing Phase 0b of
  `workplan/research-matrix-completion-execution-plan-2026-07-24.md`.
- Affects (on ratification): `scripts/migrations/033_search_executions.sql` (new),
  `schemas/search_execution.py` (new), `PRAGMA user_version` 32→33. No entity-row
  deltas; the table ships empty. Legacy `search_coverage` / `search_languages` are
  **not** dropped — they are frozen read-only historical artifacts, superseded by the
  derived views but preserved (redirect-stub discipline, CLAUDE.md §9 guardrail 2).
- Related: `workplan/search-coverage-completion-workplan.md` §2.2 (the DDL this
  implements), `workplan/coverage-completion-loop-methodology-2026-07-21.md` §4 (the loop
  this feeds), `DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation`
  (reproducibility gate), the pipeline-contract `reproducibility-invariant` stage.

## Context — the gap this closes (facts ledger; re-verifiable, DB-checkable)

Measured against `data/guidebook.db` on 2026-07-24 (read-only):

- Coverage is two hand-maintained placeholder grids: `search_coverage` (4,960 rows,
  **4,286 NOT-RUN ≈ 86%**) and `search_languages` (1,558 rows, 859 NOT-RUN), joined by
  **nothing** — `lang_jur_map` is empty (0 rows).
- **No table records what was searched.** Verbatim query text survives only in ~47
  scattered rows (`evidence_sources.search_queries_used`, `spec_value_probes.search_query`,
  derivation chains). A cell reading `SEARCHED` today cannot prove *what* was searched,
  in what language, how deep — so coverage can neither be trusted nor resumed.
- `search_executions` (the single-source-of-truth event log the completion workplan §2.2
  specifies) **does not exist**; `gap_mining` is empty.

The coverage-completion loop is ratified (DR-adjacent, owner-directive 2026-07-21) but its
*memory* was never built. A loop that hand-writes coverage re-creates the un-auditable grid
it exists to escape (loop methodology §6, Decision Gate 1 — resolved: "thin append-only
logger first"). This DR builds that logger.

## Decision — the proposed schema (embedded for review)

One row = one executed search. Coverage is **derived** from this log, never hand-written.
STRICT table, reusing the established STRICT + CHECK + `json_valid()` pattern
(`item_population_links`, `spec_value_probes`, `evidence_cell_state`).

```sql
-- 033_search_executions.sql
-- Schema migration (Phase 0b, coverage-loop substrate): the single logged-search
-- event table + derived coverage views. Implements search-coverage-completion-workplan
-- §2.2 and coverage-completion-loop-methodology §4. Per DR-2026-07-24-search-executions-substrate
-- (DG-REVIEW). Doctrine SHA 0f2f525. Schema-only, additive; ships empty.
-- Runner sets PRAGMA user_version to 33.
BEGIN;

CREATE TABLE search_executions (
  exec_id              INTEGER PRIMARY KEY,
  slug                 TEXT NOT NULL REFERENCES slugs(slug),
  jurisdiction         TEXT,                 -- NULL = jurisdiction-agnostic search
  language             TEXT NOT NULL,        -- ISO; one of the 19 research languages
  -- hierarchy branch the search TARGETED (diffable against what was FOUND):
  target_tier          INTEGER CHECK (target_tier IS NULL OR target_tier BETWEEN 1 AND 6),
  target_evidence_type TEXT CHECK (target_evidence_type IS NULL OR target_evidence_type IN
     ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')),
  target_scope         TEXT CHECK (target_scope IS NULL OR target_scope IN
     ('intrinsic','lower_control','high_control','national','international')),
  -- the verbatim, replayable query:
  query_text           TEXT NOT NULL,
  terms_used           TEXT,                 -- JSON array of term ids
  engine               TEXT NOT NULL,        -- pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual
  -- depth as real method, not booleans:
  depth_method         TEXT NOT NULL CHECK (depth_method IN ('scoping','systematic')),
  mining_direction     TEXT CHECK (mining_direction IS NULL OR mining_direction IN
     ('none','backward','forward','both')),
  -- yield:
  results_found        INTEGER NOT NULL DEFAULT 0,
  results_screened     INTEGER NOT NULL DEFAULT 0,
  results_admitted     INTEGER NOT NULL DEFAULT 0,
  saturation_signal    TEXT CHECK (saturation_signal IS NULL OR saturation_signal IN
     ('none','partial','saturated')),
  admitted_ref_ids     TEXT,                 -- JSON array of evidence_sources.ref_id
  deferred_reason      TEXT,                 -- non-NULL => deliberate no-search for this cell
  backfill             INTEGER NOT NULL DEFAULT 0 CHECK (backfill IN (0,1)),
  session              TEXT NOT NULL,
  executed_at          TEXT NOT NULL,        -- explicit ISO ts (deterministic under rebuild)
  CHECK (terms_used IS NULL OR json_valid(terms_used)),
  CHECK (admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids))
) STRICT;
CREATE INDEX ix_se_cell   ON search_executions(slug, jurisdiction, language);
CREATE INDEX ix_se_branch ON search_executions(target_tier, target_evidence_type, target_scope);

-- Derived coverage — replaces the hand-kept grids (which are frozen read-only, not dropped):
CREATE VIEW v_coverage_jurisdiction AS
SELECT slug, jurisdiction,
       COUNT(*) AS searches, SUM(results_admitted) AS admitted,
       MAX(depth_method='systematic') AS reached_systematic,
       MAX(saturation_signal='saturated') AS saturated
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, jurisdiction;

CREATE VIEW v_coverage_language AS
SELECT slug, language, COUNT(*) AS searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, language;

CREATE VIEW v_coverage_branch AS
SELECT slug, jurisdiction, target_tier, target_evidence_type, target_scope,
       COUNT(*) AS targeted_searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY 1,2,3,4,5;

COMMIT;
```

Companion Pydantic model (mirrors the table; schema↔SQLite drift is a CI-caught bug):

```python
# schemas/search_execution.py
"""One executed search — the coverage-loop event log (migration 033).
Coverage is DERIVED from these rows (v_coverage_*), never hand-written."""
from typing import Optional
from pydantic import BaseModel, Field

class SearchExecution(BaseModel):
    exec_id: Optional[int] = None
    slug: str = Field(..., description="FK slugs.slug")
    jurisdiction: Optional[str] = None       # NULL = jurisdiction-agnostic
    language: str
    target_tier: Optional[int] = Field(None, ge=1, le=6)
    target_evidence_type: Optional[str] = None   # clinical|sr_meta|standard_eb|national_fw|code|co1|co2|grey
    target_scope: Optional[str] = None           # intrinsic|lower_control|high_control|national|international
    query_text: str
    terms_used: Optional[str] = None             # JSON array
    engine: str                                  # pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual
    depth_method: str                            # scoping|systematic
    mining_direction: Optional[str] = None       # none|backward|forward|both
    results_found: int = 0
    results_screened: int = 0
    results_admitted: int = 0
    saturation_signal: Optional[str] = None      # none|partial|saturated
    admitted_ref_ids: Optional[str] = None       # JSON array of ref_id
    deferred_reason: Optional[str] = None
    backfill: int = 0
    session: str
    executed_at: str
```

**Rationale.** (a) The loop's success metric is *% required cells with ≥1 logged search* and
*% saturated-or-deferred* — both are `COUNT`/`MAX` over this log; they are un-fakeable because
coverage is derived, not asserted. (b) `deferred_reason` makes an honest non-search a
first-class, counted outcome (owner directive 2026-07-21). (c) `admitted_ref_ids` back-links
every admitted source to the exact search that found it — the chain of custody the completion
workplan §6 requires, and the hook that makes *spillover routing* auditable (a source found
under slug X but linked to slug Y is visible in the diff between the search's `slug` and the
`source_slug_links` it produced). (d) `backfill=1` isolates the ~47 recoverable historical
queries from forward loop rows. (e) `executed_at` is an explicit ISO string, **not**
`DEFAULT datetime('now')`, so rebuild is byte-deterministic.

**Alternatives considered.** (1) *Keep hand-writing the two grids* — rejected: re-creates the
un-auditable state (loop §6). (2) *Full `search_executions` + FTS5 companion + materialized
`v_priority_queue` now* — deferred: owner Gate 1 resolved to "thin logger first, evolvable
later"; FTS5 and the priority-queue view are additive follow-ons that do not require reshaping
this table. (3) *A boolean-depth column set like `search_coverage`* — rejected: depth is a
measured method (`scoping`/`systematic` + mining), not three booleans; that was the exact
defect being escaped.

## Adversarial pass (one pass, this version — R2 / DR-2026-05-09)

- **Objection: overbuild before the loop has run.** A 24-column log before a single loop batch
  risks scaffolding-for-scaffolding (the repo's known failure mode, CLAUDE.md §1). **Answer:**
  the columns are exactly the five coverage axes the mission commits to making auditable
  (terms, jurisdictions, languages, depth, hierarchy-branch) plus provenance — none speculative;
  and the *thin*-logger scope defers FTS5 + the queue view. If a column proves unused after the
  first batches, dropping it is a forward migration. Net: minimal, not maximal.
- **Objection: STRICT + FK with `PRAGMA foreign_keys` off.** SQLite doesn't enforce the
  `REFERENCES slugs(slug)` FK unless PRAGMA is on. **Answer:** matches every existing table's
  loose-coupling convention; `test_db_integrity.py` checks FK validity as a data invariant, so
  orphaned slugs are caught by audit rather than by engine — consistent with the repo, not a
  regression.
- **Objection: coverage views hide deferred cells.** The `WHERE deferred_reason IS NULL` filter
  means a cell "covered" only by deferrals shows zero searches. **Answer:** that is intended —
  deferred ≠ searched; a fourth view (or the raw log) surfaces deferrals explicitly so they are
  *counted, never silently dropped* (workplan §3). The filter prevents a deferral from masquerading
  as coverage, which is the honest behavior.
- **Refutation test:** if ratified and applied, `migrate_db.py --rebuild` must byte-reproduce the
  7 CI invariants (`user_version=33` + the six entity counts unchanged) — falsifiable, and the
  gate that guards this DR's reproducibility claim.

## What this DR does NOT do

- Does **not** drop or alter `search_coverage` / `search_languages` (frozen, preserved).
- Does **not** ship FTS5, the `v_priority_queue` materialization, or any audit script — deferred.
- Does **not** write a single coverage row — the table ships empty; population is the loop's job.
- Does **not** self-ratify: schema is DG-REVIEW; the migration is applied only on owner approval.
