# DR-2026-07-12: `evidence_cell_state` schema reconciliation — proposed resolution

- Status: **PROPOSED — pending owner ratification**
- Date: 2026-07-12
- Prepared by: Claude, at the owner's request to reconcile identified conflicts and propose a path forward. **Not owner-ratified.** The merge decision below (which columns to keep, add, or drop) is a technical recommendation for the owner to review, not a settled fact.
- Affects (if ratified): `scripts/migrations/026_reconcile_evidence_cell_state.sql`, `scripts/validate_evidence_state.py`, `workplan/best-practices-assessment-system.md`
- Related: `decisions/DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation.md`, `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md`, `decisions/DR-2026-07-12-tier3-stated-threshold.md` (also PROPOSED)

## Context

Two incompatible schemas exist for `evidence_cell_state`, the empty table meant to hold the project's central per-cell best-practice determination:

**A. `scripts/migrations/024_evidence_cell_state.sql` (already applied; the live, empty table, `user_version=25`):** keyed on `(item_code, population_code)`, FK'd to the real `items` and `populations` tables. Convergence is normalized into a separate, directness-aware `convergence_assessment` table (also empty) carrying `clinical_sources`/`co1_sources`/`co2_sources` and `down_weighted_sources`/`discounted_sources` — ties directly into the Stage 2.2 directness-conditioning work (`schemas/directness.py`) and DR-2026-05-29's scale/directness doctrine. No jurisdiction dimension. No provenance hash.

**B. `workplan/best-practices-assessment-system.md` §4 (2026-06-22; explicitly "sketch; finalize as migration 026," never built):** keyed on `(slug, population, jurisdiction)` — `slug` is a BPC topic identifier, a different and coarser grain than `item_code`. Convergence is a flat `convergence` enum column (`converge`/`diverge`/`single`/`none`) with no directness distinction and no source-list tracking. Adds real, valuable capability schema A lacks: `governing_refs` (anti-hallucination — a determination cannot exist without citing the sources that establish it), `rule_version` + `derivation_sha` (lets a `stated`/`provisional` cell be checked for staleness against the live evidence set), `tier_basis`, `code_floor_only`, `value_range`, and a `falsification` condition per doctrine #6.

Naively adopting B as migration 026 would **regress** the already-built directness-aware convergence model from schema A with no replacement — B's flat `convergence` enum cannot express down-weighting or discounting, both load-bearing per DR-2026-05-29's directness conditioning layer. Naively keeping A as-is would forgo B's genuinely useful provenance/reproducibility additions, which directly serve the project's own stated anti-hallucination priority.

## Proposed decision

**Merge, not replace.** Rebuild `evidence_cell_state` (0 rows; safe to rebuild without a data-preserving migration) to:

1. **Keep schema A's cell identity** — `(item_code, population_code)` — per migration 024's own rationale: no canonical `specification`/`slug` table exists in the migration-built DB, and `item_code` is the FK-valid parameter key today. *(This is the same identity question DR-2026-07-12-website-architecture-lock.md resolves for the site's URL routing — both should stay in sync: population-code taxonomy, not slug/axis identity, for v1.)*
2. **Add a `jurisdiction` column** (schema B's addition) as `TEXT NOT NULL DEFAULT ''`, where `''` means jurisdiction-agnostic — **not nullable**, because SQLite does not treat `NULL` as equal to itself in a `UNIQUE` constraint, so a nullable jurisdiction column would silently permit duplicate "agnostic" rows for the same cell. The composite uniqueness becomes `(item_code, population_code, jurisdiction)`.
3. **Keep schema A's `convergence_assessment` table and FK unchanged** — do not regress to B's flat enum. `convergence_assessment.status` (`convergent`/`divergent`/`single_axis`/`pending_assessment`) already carries the semantic information B's `convergence` column would; the directness fields (`down_weighted_sources`, `discounted_sources`) are additionally preserved.
4. **Add schema B's provenance/reproducibility columns** that schema A lacks: `tier_basis`, `governing_refs` (JSON array, `CHECK (governing_refs IS NULL OR json_valid(governing_refs))`), `rule_version`, `derivation_sha`, `code_floor_only`, `value_range`, `falsification_condition`. A new `confidence_bucket` column (`high`/`medium`/`low`) is added alongside — not instead of — schema A's existing `confidence_dimensions_present`/`confidence_dimensions_absent`/`confidence_synthesis_basis` fields, since those serve a different (diagnostic detail vs. queryable summary) purpose and are already relied on by `validate_evidence_state.py`.
5. **Reuse schema A's existing `created_at`/`created_by_session`/`updated_at`/`updated_by_session` audit columns** instead of adding schema B's separate `computed_at`/`computed_by`, to keep one audit-column convention across the table.
6. **Add `weighting_profile`** exactly as proposed in schema B (`(audience, use_pattern)` primary key, `tier_weights` JSON) — no conflict with schema A, since it didn't exist there.
7. **Add the four derived views** from `best-practices-assessment-system.md` §4 (`v_best_practice`, `v_pending`, `v_divergence`, `v_code_floor_only`), adjusted to the actual `gaps` table columns (`description`, `category`, `priority` — not the sketch's assumed column names) and to the merged schema's `convergence_assessment` join instead of a flat `convergence` column.

This DR does **not** decide the Tier-3 `stated`-threshold question (whether a cell can be `stated` on Tier-3-alone evidence) — that is addressed separately in `decisions/DR-2026-07-12-tier3-stated-threshold.md`, since it's an evidence-methodology question, not a schema question, though the two are related (the threshold decision will need a validator check against this schema).

## Consequences if ratified

- `scripts/migrations/026_reconcile_evidence_cell_state.sql` (drafted alongside this DR) implements the merge. Since both `evidence_cell_state` and `convergence_assessment` have 0 rows, this is a schema-only migration with no data to preserve or lose.
- `scripts/validate_evidence_state.py`'s existing column-name-based `SELECT` statements continue to work unchanged (new columns are additive, not reordering or removing existing ones) — no immediate code change required there for the schema alone. A separate validator addition is needed for the Tier-3 threshold check (see the companion DR).
- `workplan/best-practices-assessment-system.md` §4's SQL sketch is superseded by the actual migration; its phasing plan (§8: schema → engine+backfill → gates → weighting → surface) is otherwise unaffected and remains the reference for what comes next once this schema exists.
- The engine/backfill work (`best-practices-assessment-system.md` §8 Phase 1 — "implement the pure determination function... backfill all cells that have evidence") is **not done by this DR**. The table will exist with the merged shape and 0 rows; populating it is separately scoped in `workplan/website-v0-path-forward-2026-07-12.md`.

## What would make this ACCEPTED

Owner review of the merge decision in "Proposed decision" above (particularly item 1 — keeping `item_code` rather than moving to `slug`/axis-based identity — and item 3 — keeping the richer directness-aware convergence model rather than the simpler enum), followed by an explicit ratification note or session directive.
