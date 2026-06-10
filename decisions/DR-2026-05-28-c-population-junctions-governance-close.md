# DR-2026-05-28-c — Population-Junctions Governance Close (value-claim tables)

**Status:** PROPOSED — governance close for migration 021, already applied to the DB; pending owner commit. Part of the Stage 1.5 governance-hygiene set.
**Authored:** 2026-06-09 (`session_2026-06-09-stage-1-5-governance-hygiene`).
**Doctrine SHA:** `3da73bd` (after the Stage 1.1 doctrine commit; if 1.5 is committed before 1.1, use `61c7f95`).
**Relates to:** DR-2026-05-28-b (`source_value_extractions` schema — the value-directness substrate these junctions attach populations to); migration `021_value_claim_population_junctions.sql`; companion data migration `data_20260528211500_populate_population_junctions.sql`; the pre-existing `item_population_links` pattern; master workplan R10(b).

---

## Context

The project models item↔population membership relationally via `item_population_links` (FK-enforced, 361 rows). The three value-claim tables, however, stored population as free text — `reasoning_doc_citations.population` (e.g. `'NDV,AUT'`), `spec_value_probes.population` (e.g. `'AUT, PCS, DEM, MH, PAIN, OFS'`), and `source_value_extractions.population_code` (a single FK that cannot hold compounds). This conflated multi-valued membership into a string, made population validity un-enforceable at the DB level, and left drift detection to the render layer.

Migration 021 (schema-only, additive — applied to the DB; this DR is its retrospective governance record) closed that gap.

## Decision recorded

1. **Three FK-enforced junction tables**, mirroring `item_population_links`, now carry multi-valued population membership for the value-claim tables:
   - `citation_population_links` (`citation_id` ↔ `population_code`) — 7 rows
   - `probe_population_links` (`probe_id` ↔ `population_code`) — 36 rows
   - `extraction_population_links` (`extraction_id` ↔ `population_code`) — 0 rows (populated as `source_value_extractions` fills, per DR-28-b)

   Each FK-references `populations(population_code)`, structurally constraining every population value to the canonical **22-code taxonomy**. Compound populations become first-class multi-row sets rather than comma-strings.

2. **Scalar `population` / `population_code` columns RETAINED but DEPRECATED.** Audit scripts still read them, so they are kept denormalized-in-sync as a transition convenience. **Dropping them is deferred to a caller-sweep** per architecture v2.3 `<migration_and_growth>` ("Removing or renaming structural elements … the change is not complete until a caller-sweep is performed").

3. **Enforcement.** A companion **Level-2 audit, `scripts/audit/population_integrity_audit.py`**, enforces scalar↔junction consistency. CI `db_integrity` runs `PRAGMA foreign_key_check`, which now structurally validates the junction FKs at the blocking level. The Level-2 audit is not yet wired into CI; promotion to a blocking job is deferred per the enforcement-spectrum promotion path (promote when drift proves costly).

## PI `<hooks_status>` consequence (queued, not a standalone PI bump)

The new Level-2 audit `scripts/audit/population_integrity_audit.py` belongs in the PI `<hooks_status>` Level-2 list. Per the project's "no PI bump unless critical armature" rule (PI-update-needed.md, v10.15-rejected rationale) and architecture `<scope_assumptions>`, this is **queued to bundle with the next PI bump** (alongside the v10.16 `gap-driven-mining` skill-assignment line), not pasted out-of-band. The audit is invocable regardless of whether PI text names it; the PI line is documentation, not gate.

## Verification (DB, 2026-06-09)
All four junction tables present (`item_population_links` 361, `citation_population_links` 7, `probe_population_links` 36, `extraction_population_links` 0); `populations` = 22 codes; `population_integrity_audit.py` present. `[SOURCE: T0 — data/guidebook.db + scripts/migrations/021_value_claim_population_junctions.sql]`.
