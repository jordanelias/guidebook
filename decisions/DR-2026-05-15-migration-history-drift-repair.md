# Decision Record: Migration-History Drift — Repair Strategy
**Date:** 2026-05-15
**Status:** PROPOSED — awaiting owner directive on repair strategy (A / B / C)
**Author:** Claude (session_2026-05-15, continuation under DR-2026-05-13 delegation framing)
**Self-review caveat:** This DR diagnoses drift my predecessor sessions allowed to accumulate (i.e., other Claude sessions). `[SELF-AUTHORED — bias risk]` applies in the AI-system sense; independent-human-reviewer limitations are flagged in §6.

---

## 1. Context

CI's migration-reproducibility check in `.github/workflows/audit.yml` rebuilds `data/guidebook.db` from scratch by replaying `scripts/migrations/*.sql` and compares against the committed DB. The check fails on `sqlite3.OperationalError: no such column: edition` while applying `data_20260513025900_track1_versioning_backfill_pass1.sql`.

The visible failure is one missing column. The underlying state is wider: rebuilding from migration history produces an `evidence_sources` table with **23 columns**; the committed DB has **81 columns**. 8 entire tables (`populations`, `pipeline_runs`, `url_verification_runs`, `evidence_source_authors`, `item_population_links`, `item_population_elaborations`, `evidence_sources_v1_legacy`, `sqlite_sequence`) exist in the committed DB but are not created by any migration file.

The `data_migrations` table inside the committed DB documents 11 schema-mutating operations that were applied to the DB but never committed as SQL files in `scripts/migrations/`:

| `data_migrations` entry | Schema impact (inferred from committed DB) |
|---|---|
| `schema_v2_evidence_sources_2026-05-11` | Major rewrite: normalized authors into separate table, added language detection columns, translation columns, structured bibliographic fields (~30 columns added to evidence_sources) |
| `cutover_evidence_sources_v2_2026-05-11` | Rename `evidence_sources_v2` → `evidence_sources`; original renamed to `evidence_sources_v1_legacy` |
| `items_applicable_groups_normalization_2026-05-11` | Created `populations`, `item_population_links`, `item_population_elaborations`; dropped `items.applicable_groups` column |
| `verification_pipeline_v1_columns_2026-05-12` | Added `verified_by_tool`, `last_verified_at`, `verification_attempt_count`, `superseded_by_ref_id` to evidence_sources |
| `pipeline_runs_table_2026-05-12` | Created `pipeline_runs` table |
| `metadata_enrichment_columns_2026-05-12` | Added `pages`, `pub_month`, `language`, `subtype`, `citation_count` to evidence_sources |
| `pipeline_runs_phase_4_columns_2026-05-12` | Extended `pipeline_runs` with Phase 4 metrics columns |
| `channel_2_url_verification_2026-05-12` | Added `url_resolution_outcome`, `url_last_fetched`, `url_match_similarity` to evidence_sources; created `url_verification_runs` table |
| `iec_60118_4_triplicate_documented_2026-05-12` | Annotation only (no schema change) |
| `doi_resolution_outcome_backfill_2026-05-12` | Data-only: set `doi_resolution_outcome=RESOLVED` on 211 rows |
| `verified_by_tool_backfill_2026-05-12` | Data-only: set `verified_by_tool=co1-manual-pre-pipeline` on 133 rows |

Architecture v2.3 `<data_layer_pattern>` states: *"Direct writes that bypass migrations are prohibited; CI enforces reproducibility."* That prohibition was violated 11 times between 2026-05-11 and 2026-05-13. The `data_migrations` table captured human-readable intent but the actual SQL was never preserved in `scripts/migrations/`.

This is a pre-existing condition on `main`. Current sessions did not introduce the drift; this DR proposes the repair.

---

## 2. Why this matters

Three concrete consequences:

1. **The committed `data/guidebook.db` cannot be rebuilt from version control.** The schema definition lives only in the binary blob. If the blob is corrupted, lost, or needs to be recreated for any reason (CI bootstrap, contributor onboarding, disaster recovery), the schema must be reverse-engineered from the artifact rather than read from migration history.

2. **The migration-reproducibility CI check is permanently red until repaired.** This is a level-4 blocking enforcement (per architecture v2.3 `<enforcement_spectrum>`). Every push currently fails this gate. The longer it stays red, the more contributors learn to ignore it, eroding its enforcement value.

3. **The pattern is reinforcing.** Every additional direct write to the DB without an accompanying migration file deepens the drift. The Track 1 versioning backfill from 2026-05-13 is itself an example: the data migration ran, but its precondition (the `edition` column) was added by an undocumented earlier operation, so the data migration can't be replayed.

---

## 3. Repair strategy options

### Option A — Retroactive migrations

Author 11 separate migration files (`012_*.sql` through `022_*.sql`) each reconstructing one documented `data_migrations` entry by reverse-engineering the committed DB schema.

| Pro | Con |
|---|---|
| Preserves per-change historical granularity | SQL must be fabricated from inference (committed-DB schema is the only source of truth for what each migration did); subtle errors (column order, default values, missing indexes, missing CHECK constraints) likely |
| Future migration discipline reads naturally — each migration has a documented intent | Significant authoring effort (~11 SQL files, each requiring schema introspection + verification round-trip) |
| Each migration can be code-reviewed in isolation | If any one migration is wrong, the rebuild diverges from committed state — and the error may not surface until much later |
| Aligns with the architecture's forward-only migration discipline | Cannot validate against original intent (the actual SQL that ran is lost) |

### Option B — Baseline snapshot

Author one migration `012_baseline_2026-05-15.sql` containing the complete current schema (extracted via `.schema` from committed DB). Prior migrations 001–011 are retained as historical reference but the baseline supersedes them at rebuild time. Migration runner is updated to apply the baseline if `PRAGMA user_version = 0`, otherwise apply incremental migrations forward from the user_version checkpoint.

| Pro | Con |
|---|---|
| Deterministic: schema is dumped, not inferred | Discards per-migration provenance (cannot answer "which migration introduced column X") |
| Verifiable: rebuild from baseline + check schema equality with committed DB | Requires migration-runner change (decide which baseline to apply based on user_version) |
| One-time fix; future migrations resume normal forward-only discipline | Sets a precedent that drift can be papered over with snapshots — needs paired policy (`pre-commit hook` deferred per architecture `<scope_assumptions>`, but a CI check could fail any push that touches DB without a matching migration) |
| Migration consolidation is a known and documented pattern in mature projects (Django `squashmigrations`, Rails `schema.rb`) | The `data_migrations` table contents remain as the only record of intent for what historically happened — but they remain readable |

### Option C — CI tolerance

Narrow the migration-reproducibility check to compare only structural invariants (table existence, row counts) rather than full schema equivalence. Migrations stay broken; CI stops complaining.

| Pro | Con |
|---|---|
| Trivial change (one CI workflow edit) | Defeats the check's purpose: architecture explicitly says CI enforces reproducibility |
| Unblocks the audit job in one commit | Encodes the drift as acceptable, removes pressure to repair |
| | Future drift won't be detected either |

---

## 4. Recommendation (subject to owner directive)

**Option B (baseline snapshot).** Reasoning:

1. **Honesty about state.** The committed DB *is* the schema source of truth right now. Pretending otherwise (Option A) requires fabrication. Codifying the snapshot makes the existing reality explicit and verifiable.
2. **Lower error surface.** A schema-dump-based migration can be byte-compared against committed reality; an inferred migration cannot.
3. **Future discipline restored.** Once baselined, migration 013+ proceed normally. The `data_migrations` table continues to serve as a write-time record of intent for any future operations.
4. **Paired enforcement.** Add a level-4 CI check that fails any commit touching `data/guidebook.db` without an accompanying file in `scripts/migrations/`. This is the actual prevention; the baseline is the repair.

Option A is defensible if historical provenance matters more than rebuild reliability — but the historical provenance already exists in the `data_migrations` table as prose. Migration files would just translate that prose to SQL.

Option C is the wrong answer for a project where the architecture pattern explicitly says CI enforces reproducibility.

---

## 5. Implementation sketch (if Option B adopted)

1. **Author `012_baseline_2026-05-15.sql`.** Generated by `sqlite3 data/guidebook.db .schema` filtered to remove `sqlite_sequence` and other internal artifacts, then split into `CREATE TABLE`, `CREATE INDEX`, `CREATE VIEW` blocks for readability. Header comment documents the supersession of 001–011 and lists the 11 `data_migrations` entries it incorporates.
2. **Update `scripts/migrate_db.py`.** Add baseline-detection logic: on rebuild, if migrations directory contains a baseline file (recognizable by filename or header marker), apply it instead of 001–011; then apply 013+ incrementally. Document the contract.
3. **Verify rebuild.** Run `python3 scripts/migrate_db.py --rebuild /tmp/test.db` and compare `.schema` output byte-for-byte against committed DB. Diff must be empty (excluding `sqlite_sequence` and migration-bookkeeping rows).
4. **Add prevention CI job.** New job in `audit.yml`: on every push that modifies `data/guidebook.db`, check that the diff also touches `scripts/migrations/`. Fail if not.
5. **Update architecture v2.4 or DR-2026-05-15-b** documenting the baseline pattern and the prevention check.

If Option A adopted instead: same flow but step 1 expands to 11 migration files, step 3 changes to incremental replay.

---

## 6. Limitations

- This DR is authored by Claude with no human in the loop on the drift itself. The drift was introduced over multiple sessions by Claude instances responding to "fix this now" pressure; the same pressure could push toward Option C if not checked.
- Recommendation favors Option B but the trade-off (provenance vs reliability) is a values call, not a technical one. Owner directive is genuinely required.
- The 11 `data_migrations` entries may not be exhaustive. If additional undocumented writes occurred, the baseline snapshot will capture them silently; retroactive migrations would surface them as unaccountable schema. Either way, the audit benefits from owner review of `data_migrations` against memory.
- The prevention CI check in §5 step 4 is necessary but not sufficient — someone could still commit a no-op migration file alongside a real DB change. Pre-commit hooks (level 5) are the structural fix, deferred per architecture `<scope_assumptions>`.

---

## 7. Action queue

- [ ] Owner directive: select A, B, or C
- [ ] If A or B: implementation per §5
- [ ] If A or B: PI v10.12 bump documenting the repair and pointing to this DR
- [ ] If A or B: prevention CI check added to `audit.yml`
- [ ] If C: PI v10.12 bump documenting the explicit relaxation and the policy gap it creates

---

## 8. Related findings (this session) — owner directives needed

The migration-drift investigation surfaced four adjacent items requiring owner directive. None are part of the migration repair itself; each has independent decisions.

### 8.1 B04: url_resolution_outcome vocabulary drift

CI's `db_integrity` check B04 fails on 53 rows whose `url_resolution_outcome` values fall outside the audit's allowed set.

Audit allowed set: `{MATCHED, PARTIAL, NO-MATCH, DEAD-LINK, DEAD-DNS, WAYBACK-MATCH, WAYBACK-PARTIAL, URL-NO-MATCH}`.

Actual DB values: 48 × `RESOLVED`, 4 × `DEAD`, 1 × `RESOLVED-PARTIAL`.

Pattern matches B03 (`doi_resolution_outcome`) which uses `RESOLVED` as a value. Likely the URL-pipeline vocabulary was tightened in the audit but never migrated in data. Two paths:
- **A.** Widen the audit's allowed set to include `RESOLVED`, `DEAD`, `RESOLVED-PARTIAL`. Pro: existing data preserved; matches `doi_resolution_outcome` vocabulary. Con: keeps two parallel vocabularies for similar fields.
- **B.** Migrate data: `RESOLVED → MATCHED`, `DEAD → DEAD-LINK`, `RESOLVED-PARTIAL → PARTIAL`. Pro: vocabulary consolidates. Con: maps may not be semantically exact (e.g., `MATCHED` implies title-match verification; `RESOLVED` from the pipeline may not have done that check).

### 8.2 D01: unexpected duplicate DOIs — three sub-issues

CI's `db_integrity` check D01 fails on 7 unexpected duplicate DOIs (excluding the documented IEC 60118-4 triplicate). Investigation reveals three distinct sub-issues:

**8.2a — Audit-script typo (fixed this session in commit batch below).** `KNOWN_DUP_DOIS` had the HIPI Lancet entry truncated to `"10.1016/S0140-6736(14"` (missing the closing paren and remainder of the DOI). The `NOT IN` match failed. Corrected to full DOI `"10.1016/S0140-6736(14)61006-0"`.

**8.2b — Intentional standard-section duplicates not yet documented.** Two additional German standards exhibit the same pattern as the documented IEC 60118-4 triplicate:
- `10.31030/1803049` (DIN 18040-2) appears 5 times — REF-00144, REF-00207, REF-00323, REF-00412, REF-00431 — each citing a different section (general apartment, operating heights, Wohnungen subset, edition reference, Nullschwelle doctrine).
- `10.31030/1715500` (DIN 18040-1) appears 3 times — REF-00351, REF-00422, REF-00445 — each citing a different section (induction loop, Pt 1 general, doors).

If these are intentional multi-section citations (consistent with IEC 60118-4 precedent), add to `KNOWN_DUP_DOIS` with explanatory comments. Owner confirmation that these are intentional is required before this lands; the alternative (genuine duplication) would require dedup.

**8.2c — Genuine duplicate ingestion events.** Four DOIs appear to be the same paper ingested multiple times under distinct ref_ids:

| DOI | Count | Refs | Topic |
|---|---|---|---|
| 10.3390/ijerph18063203 | 4 | REF-00046, REF-00490, REF-00546, REF-00710 | "Built Environment Design and ASD" (2021) — title variations |
| 10.1371/journal.pone.0291228 | 2 | REF-00006, REF-00154 | "Accessible independent housing for people with disabilities" (2024) |
| 10.3233/978-1-61499-684-2-612 | 2 | REF-00204, REF-00455 | "Wheelchair and walker users passing through doors" (2016) |
| 10.1080/10400430903520280 | 2 | REF-00023, REF-00060 | "Wheeled mobility device dimensions" (2010) |

Dedup strategy needed:
- Identify the canonical `ref_id` per group (oldest? most-complete metadata? most-cited downstream?).
- Repoint FK references in `source_slug_links`, `evidence_source_authors`, `evidence_population_match`, `reasoning_doc_citations`, etc.
- Demote duplicate `ref_id`s — either delete (loses history) or mark `superseded_by_ref_id` with a `MERGED` status.

This is itself a separable DR. Recommended scope: own session, owner-directed canonical-ref selection per group, FK repoint via migration.

### 8.3 D-0138 effort_level=200 — outside schema enum

`data/decisions/decision_register.yaml` decision D-0138 (operative storage form selection) has `model_routing: opus/200/synth` and `effort_level: 200`. The Pydantic schema's `VALID_EFFORT_LEVELS = {50, 75, 100, 125, 150}` (matching userPreferences `<effort_levels>` low/medium/high/max). `200` violates both the regex (`MODEL_ROUTING_PATTERN`) and the enum.

Three possibilities:
- **A.** Typo — should be `150` (max). Lowest-disruption fix.
- **B.** Deliberate informal extension — "200" was used to signal extra-deep effort beyond the standard `max=150` for an unusually high-stakes architectural decision. If so, the schema should widen to `{50, 75, 100, 125, 150, 200}` and `MODEL_ROUTING_PATTERN` should include `200`. But this conflicts with the userPreferences effort scale.
- **C.** Notation drift — someone used `200` ad-hoc, no real meaning. Should be normalized to a valid value.

Owner directive needed. I cannot resolve this from data alone.

### 8.4 Pilot BPC for Phase E.1 — pre-existing item

Per the prior queue: recommended pilot BPC is `neurological-built-environment` (8 sources, 5 eligible, single-population ABI, mixed claim types). PI rule #10 reserves inline owner review for the pilot before authoring begins; this is not a step delegation can substitute for. Awaiting confirmation or substitution.

---

## 9. Session deliverables (this session, against this DR)

**Authored / committed in this session toward the items above:**
- Skill file `skills/reasoning-doc-citations_SKILL.md` (commit `efde432842`)
- Skill registry updated, placeholder removed (commit `19d916086d`)
- PI v10.11 promoting the skill from placeholder to active (commit `80e2b4263a`)
- Audit-script SQL fix `scripts/audit/citation_mining_completeness.py` (commit `69ebe9ab65`) — partial: cleared the immediate column error; Audits job still red on migration-reproducibility (covered by this DR)
- `scripts/validate_temporal.py` T-05 patch (commit `1c40cfaa16`) — Schema validation now green
- `schemas/enums.py` DecisionStatus widening — pending commit
- `scripts/decision_capture.py` counter widening — pending commit
- `scripts/tests/test_db_integrity.py` D01 HIPI typo fix — pending commit
- This DR draft — pending commit

**Net CI change once pending commits land:** Schema validation (green, prior session), Audits (still red on §3 migration-reproducibility — needs this DR's directive), DB integrity (still red until §8.1, §8.2b, §8.2c addressed — but §8.2a removes 2 of the 7 dups from the failure surface), Governance (will go green once §8.3 resolved or D-0138 manually edited), Structure (workplan-scale; out of scope here).
