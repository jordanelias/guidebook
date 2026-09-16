# Retirement reader sweep — `specifications` (owner ruling 2026-09-16, migration 083)

Read-only sweep. Nothing was written to `data/guidebook.db` or any script. All commands run
against the committed DB (`file:data/guidebook.db?mode=ro`) and the working tree as of commit
`6067b88` (branch `pr-137-research-batch-08`).

**Pre-existing state confirmed before the sweep:**

```
python3 -c "import sqlite3; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); \
print(c.execute(\"PRAGMA table_info(specifications)\").fetchall())"
```
→ 35 columns today, **no `retired_at`/`retired_by_session`/`retirement_reason`/`superseded_by_specification_id`**.
The migration has not been applied to the canonical DB yet.

```
git status --short scripts/migrations/083_specification_retire_in_place.sql scripts/db.py scripts/assess/assess_cell.py
```
→ `scripts/migrations/083_specification_retire_in_place.sql` is **untracked** (drafted, not committed);
`scripts/db.py` and `scripts/assess/assess_cell.py` are **already modified** in the working tree — the
writer (`retire_specification`) and the write-time re-determination guard
(`validate_cell_undetermined`) have already been updated to reference `retired_at`. **This means
`scripts/assess/assess_cell.py` and `scripts/db.py retire-specification` will both throw
`sqlite3.OperationalError: no such column: retired_at` against the live DB until migration 083 is
applied** — they are ahead of the schema, not behind it. This is a real, immediate finding, separate
from the view/script sweep below.

Migration 083's own header (read in full) **already names the exact seven views this sweep found
independently** (see §1) and states outright: *"WHAT THIS MIGRATION DELIBERATELY DOES NOT DO: retire
anything. The ruling's ACTION item 2 is that no row is retired until every reader that could surface
it filters... Adding the columns surfaces nothing while no row is retired."* The cross-check below
confirms that list is complete and adds the non-view readers (scripts, checks) the migration text
does not enumerate.

---

## 1. Views

```
python3 -c "import sqlite3; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); \
[print(n) for (n,) in c.execute(\"select name from sqlite_master where type='view'\")]"
```
→ 20 views total. Programmatic scan (regex `\bspecifications\b` over each view's `sql`, plus a
second pass checking whether any view's `sql` names another view) found **7 views reading
`specifications` directly** and **0 chains** (no view reads a view that reads `specifications` — the
one cross-view reference in the whole set, `v_item_provenance` → `v_evidence_authors`, does not
pass through `specifications`). This exactly matches the 7 views migration 083's own comment names.

| View | Reads `specifications`? | Already filters on a lifecycle/trust predicate? | Proposed predicate | Where it goes |
|---|---|---|---|---|
| `v_best_practice` | direct | `state IN ('stated','provisional') AND code_floor_only=0` — **epistemic state, not lifecycle** (083's own distinction: state="how well the evidence supports it", retirement="a lifecycle fact") | `AND retired_at IS NULL` | Append to the existing `WHERE` clause |
| `v_code_floor_only` | direct | No | `AND ecs.retired_at IS NULL` | Append to `WHERE ecs.code_floor_only = 1` |
| `v_divergence` | direct | No (filters `ca.status='divergent'`, nothing on `ecs`) | `AND ecs.retired_at IS NULL` | Append to `WHERE ca.status = 'divergent'` |
| `v_pending` | direct | No (filters `ecs.state='pending'`) | `AND ecs.retired_at IS NULL` | Append to `WHERE ecs.state = 'pending'` |
| `v_determination_provenance` | direct | No — **no WHERE clause exists at all** | `WHERE s.retired_at IS NULL` | New clause, end of the view body |
| `v_item_provenance` | direct | No — no WHERE clause; this is the render-rollup source (CLAUDE.md: `items` is "the render rollup... derived FROM specifications") | `WHERE ecs.retired_at IS NULL` | New clause, end of the view body |
| `v_source_reach_all` | direct | No | `AND ecs.retired_at IS NULL` **on the JOIN, not in a WHERE** (see below) | Inside the `LEFT JOIN "specifications" ecs ON ecs.specification_id = csl.specification_id` clause |

**`v_source_reach_all` needs care.** It `LEFT JOIN`s from `evidence_sources` (the driving table) —
the view's whole point is to enumerate every source and say whether it `reaches` a determination
(`CASE WHEN ecs.specification_id IS NULL THEN 0 ELSE 1 END AS reaches`). Putting
`retired_at IS NULL` in a `WHERE` clause would drop the entire source row when its only link is to a
now-retired spec (because a `WHERE` clause on an outer-joined column, once matched, filters the
*whole result row*, not just the failed match) — defeating the view's purpose of listing every
source. The predicate belongs in the **join condition** instead:
`LEFT JOIN "specifications" ecs ON ecs.specification_id = csl.specification_id AND ecs.retired_at IS NULL`.
That way a source whose only link is retired correctly falls back to `reaches=0` (it does not reach
a *live* determination) while the source itself stays in the result set.

**The other 13 views** (`v_coverage_branch`, `v_coverage_jurisdiction`, `v_coverage_language`,
`v_coverage_priority`, `v_derived_figure_check`, `v_evidence_authors`, `v_open_determination_gates`,
`v_pmp_latest_walk`, `v_registry_duplicate_descriptions`, `v_root_id_conflicts`,
`v_source_admission`, `v_unregistered_roots`, `v_value_independence`) do not name `specifications` in
their SQL and do not read any view that does — **no change needed.**

---

## 2. Scripts

Command used throughout (git grep, not the Grep tool, per the task — `.ignore` hides `_archived/`,
`audits/`, `sessions/`, `versions/`, `references/search-log/`, `workplan/_superseded/`,
`transcripts/` from ripgrep/Grep but not from `git grep`):

```
git grep -n 'specifications' -- 'scripts/*' 'scripts/**/*'
git grep -n 'specifications' -- 'tools/*' 'tools/**/*'
```
263 raw hits under `scripts/` (78 outside `scripts/migrations/` and `scripts/tests/`, the rest are
migration DDL/DML history and test fixtures) plus 19 under `tools/`. After excluding migration files
(historical DDL, immutable, not "readers"), pure prose/comments naming the table without a live SQL
read of it, and hits where "specifications" is plain English for "design specifications" /
"the items table" rather than the SQL table (`tools/evidentiary_audit.py`,
`tools/*-dashboard.html` — verified: `git grep -n 'FROM specifications\|JOIN specifications' -- tools/**` returns
only `tools/pipeline_completeness.py`), the real SQL reads are:

### Count by category

| Category | Count (distinct read-sites) |
|---|---|
| **MUST exclude retired rows** | **13** |
| **MUST include retired rows** | **2** (both already correct) |
| **Indifferent** | **9** |

(Three further sites are currently *dead code* — see the note at the end of this section — and are
not counted in the three-way split because they do not execute successfully against the live schema
at all, independent of retirement.)

### MUST EXCLUDE — render surfaces, determination counts, anything a reader of the guidebook (or a
### gate standing in for one) sees

| # | file:line | What it does | Why a retired row corrupts it | Proposed predicate |
|---|---|---|---|---|
| 1 | `scripts/generate_parts.py:127` | `full_mode_ready()`: `cells = count(conn, "specifications") or 0`; `if cells == 0: reasons.append("specifications is empty...")` — gates whether Part 4+ can render in "full mode" | A parameter whose only rows are retired reads as "cells exist, ready" when nothing live backs it | `SELECT COUNT(*) FROM specifications WHERE retired_at IS NULL` in place of `count(conn, "specifications")` |
| 2 | `scripts/generate_parts.py:236` | `build_part04()`: `cells = count(conn, "specifications") or 0` then writes `"The cell-state machine holds {cells} cells."` **into the generated Part 4 markdown** — a number a reader of the guidebook sees | Retired rows inflate a count printed directly into book content | Same as above |
| 3 | `scripts/audit/register_integrity_check.py:151-156` | `check()`: `SELECT parameter_id, COALESCE(...), state, tier_basis, ... FROM specifications` with no WHERE, builds `db_rows` keyed by cell, then flags `"COMPLETENESS VIOLATION — specifications row exists but no rendering appears in the document"` for any DB row absent from the rendered HTML | A retired row is *supposed* to have no rendering — without the filter, retiring a row makes this check fire a false "suppressed determination" violation forever | `"...FROM specifications WHERE retired_at IS NULL"` |
| 4 | `scripts/audit/medical_lens_integrity.py:85-88` | "THE FRAME TEST": `SELECT specification_id FROM specifications WHERE medical_code IS NOT NULL AND identity_code IS NULL AND icf_code IS NULL AND needs_code IS NULL` — flags any determination whose *only* lens is a diagnosis (D-0170 frame violation) | The whole check exists because of what "renders... the medical model as the project's frame" (its own docstring's bar); a retired medical-only row never reaches a reader and should not be flagged forever | `AND retired_at IS NULL` |
| 5 | `scripts/audit/derivation_handshake_integrity.py:85` | `specs = [dict(r) for r in con.execute("SELECT * FROM specifications ORDER BY specification_id")]` then, per row, checks the H4 open-gate cap ("`stated` under open gate... the book is asserting a value an audit has already contested"), the cultural-claim-anchor/single-path obligation, and the functional_basis-vs-`population_icf_links` snapshot | Docstring's own bar is "WHAT WRONG THING REACHES THE GUIDEBOOK" — every one of its four checks is about a value the book would assert; a retired row asserts nothing | `"SELECT * FROM specifications WHERE retired_at IS NULL ORDER BY specification_id"` |
| 6 | `scripts/tests/test_db_integrity.py:551-566` (**C10**) | `SELECT COUNT(DISTINCT c.specification_id) FROM specifications c JOIN json_each(c.governing_refs)... WHERE c.state IN ('stated','provisional') AND ... NOT VERIFIED` — "no published cell rests on an unverified or disputed source" | A retired cell is no longer *published*; if its source is later disputed, C10 would fail on history that no reader sees | `AND c.retired_at IS NULL` on both the `unsound` and `total_cells` queries (lines 553, 561) |
| 7 | `scripts/tests/test_db_integrity.py:1170-1214` (**K01**) | Recomputes `derivation_sha` per row. **Pilot-2 branch** (line 1197-1198) recomputes the hash payload from `SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id=?` — **scoped to the parameter, not the specification row**. Once a determination is retired, new evidence can keep arriving for the same parameter (feeding its live successor) and this recount changes under the retired row too | A retired pilot-2 row goes permanently "stale" the moment fresh evidence lands for its parameter after retirement — a false fire, since a retired determination is not supposed to keep tracking live evidence | `"...FROM specifications WHERE COALESCE(derivation_sha,'')<>'' AND COALESCE(rule_version,'')<>'' AND retired_at IS NULL"` (line ~1173's source query) and add `AND retired_at IS NULL` to the `subject=subj(...)` query at line 1212-1214 so EXAMINED and the loop agree |
| 8 | `scripts/tests/test_db_integrity.py:1216-1277` (**K02**) | `SELECT specification_id, parameter_id FROM specifications WHERE rule_version='pilot-3'`, then compares `specification_extraction_links` (the row's own frozen "have" set) against `SELECT extraction_id FROM source_value_extractions WHERE parameter_id=?` (the **live, parameter-scoped** "want" set, line 1236-1238) | Same shape as K01: once new extractions accrue for a parameter after one of its determinations is retired, the retired row's frozen junction can never again equal the growing "want" set — a permanent false "unaccounted extraction" fire on history | `AND retired_at IS NULL` on the query at line 1230-1232, and on the `subject=subj(...)` query at line 1277 |
| 9 | `scripts/validate_evidence_state.py:239-296` (`validate_cell_states_db`, **BLOCKING** via `validate_evidence_state`) | `for row in conn.execute(f"SELECT {cols} FROM specifications"):` — state-machine invariants. The Tier-3-alone check (line ~286-296) calls `_ref_tiers(conn, clinical_refs)`, reading the **current, live** `evidence_sources.tier` | If a source's tier is later corrected after a `stated` determination is retired, this can flag the retired row as needing to be "provisional" — a false fire on a row no longer asserted | `f"SELECT {cols} FROM specifications WHERE retired_at IS NULL"` |
| 10 | `scripts/validate_verification_consistency.py:56-80` (`_check`, **BLOCKING**) | `SELECT specification_id,... ,has_unverified_sources FROM specifications WHERE state IN ('stated','provisional')` — compares the stored flag against the **current** `evidence_sources.verification_status` of governing refs | If a governing source's verification status changes after retirement, a retired row's frozen `has_unverified_sources` flag can mismatch the now-current status — false "truthfulness" violation on history | `AND retired_at IS NULL` appended to the existing `WHERE state IN (...)` |
| 11 | `tools/pipeline_completeness.py:148,150,154,160,163,186,189,227,243,247` (`pipeline_completeness_fresh`, **BLOCKING**, `--check`) | Builds `tools/pipeline-completeness-dashboard.html` — CLAUDE.md's own render-layer table names `tools/*.html` as a `render` stage surface. Nine separate unfiltered reads: `cells_total`, per-state counts, `parameters_judged`, `govrefs_ok`/`govrefs_denom`, `render_ready`, `design_scales`, per-population `det` count, the `judged_items` list, and each item's `cells` list | Every one of these is a completeness/progress number a person reads off the dashboard; retired rows inflate "how much of the pipeline is done" | `AND retired_at IS NULL` (or `WHERE retired_at IS NULL`) added to each of the ten query strings at those lines |

**Line 70** of `tools/pipeline_completeness.py` (`... UNION ALL SELECT MAX(updated_at) FROM specifications`,
feeding the dashboard's "as-of" date) is **indifferent** — a retirement's `updated_at` stamp is a
real, correct freshness signal, not a count.

### MUST INCLUDE — retirement is the thing they exist to see

| # | file:line | What it does | Status |
|---|---|---|---|
| 1 | `scripts/db.py:3465-3529` (`retire_specification`, the writer for `db.py retire-specification`) | Reads `specification_id, parameter_id, state, retired_at, superseded_by_specification_id` by primary key and branches on whether the row is already retired (link-only follow-up) or not (first retirement) | **Already correct as written** — this is the writer the ruling asks for, and it necessarily reads retired rows to do its job. No change needed (only: it will not run until migration 083 lands — see the top-of-report finding). |
| 2 | `scripts/assess/assess_cell.py:1320-1334` (`validate_cell_undetermined`, the write-time refusal `assess_cell.py` uses before computing a determination) | `SELECT specification_id, state, ... FROM specifications WHERE {cell} AND retired_at IS NULL` — refuses to re-determine a cell only if a **live** row exists; a retired row is correctly treated as "not an obstacle" | **Already correct as written**, and already anticipates migration 083's partial index. Same caveat: broken until 083 lands. |

### Indifferent (no change needed)

| file:line | Why it's safe as-is |
|---|---|
| `scripts/tests/test_db_integrity.py:198` (**A10**) | FK-shape existence check (`specification_source_links.specification_id → specifications.specification_id`); a retired row is still a row, so the reference still resolves. |
| `scripts/tests/test_db_integrity.py:997-1080` (**H01/H02/H06/H07**) | `governing_refs` JSON ↔ `specification_source_links` junction parity. Retirement touches only the four new lifecycle columns; it does not touch `governing_refs` or the junction, so parity is unaffected either way. |
| `scripts/audit/identifier_floor_audit.py:66-67,103` | Tracks the `specification_id` high-water mark (AUTOINCREMENT sequence / historical `INSERT ... VALUES (N`). Identifiers are never reused regardless of retirement; retired rows must still count toward the floor, and do. |
| `scripts/audit/graph/topology.py:33` (`MISSION_CRITICAL["specifications"]=20`) and `scripts/audit/graph/known_debt.yaml`'s `c1-evidence-cell-state-pilot-only` (`lift_when_sql: SELECT COUNT(*) FROM specifications`, `lift_when_ge: 20`) | `INFO`-severity only (`topology.py:198`, `store.add_finding(..., "INFO", ...)`), non-blocking either way. Worth a note, not a fix: once rows retire, `COUNT(*)` reaching 20 would say "the backlog is resolved" even if most of those 20 are dead history rather than live determinations. Low priority because the finding is informational, not gating. |
| `scripts/audit/graph/topology.py:233-247` (`state_distribution`) and `scripts/audit/graph/extract_db.py:39` (`STATE_COLS["specifications"]`) | `INFO`-severity distribution reporting; `specifications` is not in `PRIMARY` (no per-row entity node is created for it), so no edges/citation logic touches it either. |
| `scripts/audit/adjudication_integrity.py:77-86` (`_readiness`) | Prints `"specifications: {n} determination(s)"` and a state distribution. The check is **quarantined** (registry `status: quarantined`) — not currently gating anything — and this function is advisory INFO text, not a pass/fail assertion. Minor accuracy note only: once rows retire, this would slightly overstate live determination volume. |
| `scripts/generate/context_map.py:111` | Generic `SELECT COUNT(*) FROM "{t}"` looped over **every** table for `governance/context-map.yaml`'s orientation listing (raw table sizes, not "live determinations"). Not a book/reader surface. |
| `scripts/tests/test_assess_cell_pilot.py:406-433` | Reads the **live** `specifications` DDL/indexes off `sqlite_master` to build its fixture DB, rather than hard-coding a copy. Self-updating: once migration 083 lands, this test automatically probes the new UNIQUE-partial-index/trigger shape. No independent risk. |

### Dead code (pre-existing, unrelated to retirement — flagged for completeness, not counted above)

Three generators query `specifications.item_code`, a column **migration 071 already dropped** (well
before this migration). They error out before ever reading live content, so retirement is moot for
them until someone repairs the item_code→parameter_id rekey — at which point the repair should add
`retired_at IS NULL` too:
- `scripts/generate/pilot_renderings.py:264-271` (`fetch_cells`) — its own docstring says outright
  "THIS FUNCTION HAS BEEN DEAD SINCE 2026-09-09."
- `scripts/generate/spec_page.py:76-84` (`query_item`'s cells query) — queries
  `specifications WHERE item_code = ?`; not yet documented as dead, but `item_code` is not a column
  on the live table.
- `scripts/generate/build_site.py:96-101` (`governing_refs`) — joins on `ecs.item_code`; same defect.
  `site_pages_fresh` (advisory) is the registry entry that would exercise this path, but
  `build_specs()` iterates `items` (0 rows today), so the code path that would hit the broken join
  is not currently reached at all.

---

## 3. Checks (`governance/check-registry.yaml`)

| Check id | Level | Reads `specifications`? | Retired row: fires falsely / passes falsely / unaffected |
|---|---|---|---|
| `test_db_integrity` | **blocking** | Yes (A10, C10, H01/H02/H06/H07, K01, K02 — see §2 table) | **C10, K01, K02: fires falsely** once rows retire, for the reasons in §2 (published-cell / live-evidence-drift dependencies). A10/H01/H02/H06/H07: unaffected. |
| `adjudication_integrity` | **quarantined** (registry `status: quarantined`, not currently run as a gate) | Yes, `_readiness()` only (INFO text) | Neither — it's advisory prose inside a quarantined check, not a pass/fail assertion. |
| `migration_reproducibility` | **blocking** | Indirectly — `compare()` (`scripts/audit/migration_reproducibility.py:194-224`) does `COUNT(*)` on **every** user table except `EXEMPT_TABLES=("evidence_source_authors","pipeline_runs")` (line 72), so `specifications` is one of the tables it counts | `retire_specification()` is an **UPDATE** (row count unchanged) — **invisible to this check**, exactly as CLAUDE.md rule 3 and this script's own docstring (`scripts/audit/migration_reproducibility.py:262-266`, "An UPDATE changes no count") already say in general. Confirmed here as concretely true of the retire-in-place path specifically. |
| `migration_reproducibility_deep` | advisory | Yes, via `deep_compare()`'s full-row walk (`scripts/audit/migration_reproducibility.py:258-`) | **Would** catch a retirement UPDATE's value drift (it diffs every column of every row) — but it's advisory, so it doesn't block on it. This is the safety net rule 3 already names. |
| `validate_evidence_state` | **blocking** | Yes (`scripts/validate_evidence_state.py:242-307`) | **Fires falsely** — see §2 #9 (live-tier dependency in the Tier-3-alone check). |
| `validate_verification_consistency` | **blocking** | Yes (`scripts/validate_verification_consistency.py:56-80`) | **Fires falsely** — see §2 #10 (live verification_status dependency). |
| `register_integrity_check` | **quarantined** (registry `status: quarantined`, reason: keyed on `item_code`, which 071 removed) | Yes (`scripts/audit/register_integrity_check.py:151-156`) | Not currently run, but if reactivated on a `parameter_id`-keyed document it would **fire falsely** exactly as §2 #3 describes. Fix belongs to whoever reactivates it. |
| `derivation_handshake_integrity` | advisory | Yes (`scripts/audit/derivation_handshake_integrity.py:85`) | **Fires falsely** on the H4-cap sub-check once retired `stated` rows sit under gates opened/tightened after retirement — see §2 #5. Advisory today, so non-blocking, but will mislead a reader of the check output. |
| `medical_lens_integrity` | advisory | Yes (`scripts/audit/medical_lens_integrity.py:85-88`) | **Fires falsely** forever on a retired medical-only row — see §2 #4. |
| `schema_reference_audit` | **blocking** | No direct row-content read — it resolves table/column **names**, not row content (rule 4 mechanised) | Unaffected by retirement; irrelevant to this sweep. |
| `validate_pydantic_schemas` | advisory (run `--strict`) | Compares `schemas.evidence_state.EvidenceStateRecord` fields against `PRAGMA table_info(specifications)` (`scripts/audit/validate_pydantic_schemas.py:79`) | **Will go red** the moment migration 083 lands, reporting the 4 new columns as "present in the DB table but absent from the Pydantic model" (case (b) in its own docstring) — advisory only, so non-blocking, but it is exactly the drift CLAUDE.md §7 calls "a bug, not a convention." Fixed by §5 below. |
| `pipeline_completeness_fresh` | **blocking** (`--check`) | Yes, extensively — `tools/pipeline_completeness.py` (§2 #11) | **Fires falsely as a staleness/count check** in the sense that its numbers become wrong (inflated) — not that `--check` itself errors, but that the dashboard it certifies "fresh" is fresh-and-wrong. Needs the 10 site fixes in §2 #11. |
| `evidentiary_audit_fresh` | **blocking** (`--check`) | **No** — `tools/evidentiary_audit.py` only uses the English word "specifications" to mean *items* (verified: `git grep -n 'FROM specifications\|JOIN specifications' -- 'tools/*'` returns only `pipeline_completeness.py`) | Not applicable. |
| `context_map_fresh` | advisory (`--check`) | Yes, generically (`scripts/generate/context_map.py:111`, every table) | Indifferent — raw row count of a table, not a determination count; see §2. |
| `site_pages_fresh` | advisory (`--check`) | Yes, but through dead code (`build_site.py`'s `governing_refs()`, §2 dead-code note) | Not reachable today (`build_specs()` iterates `items`, which is 0 rows) — moot until the item_code→parameter_id repair happens. |

---

## 4. The partial index

```
python3 -c "import sqlite3; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); \
print(c.execute(\"select sql from sqlite_master where name='idx_spec_row_identity'\").fetchone())"
```
Current (pre-migration) index:
```sql
CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(
    parameter_id,
    COALESCE(identity_code, ''), COALESCE(icf_code, ''),
    COALESCE(needs_code, ''),    COALESCE(medical_code, '')
)
```
— UNIQUE over the **whole table**, which is exactly why a determined cell could never be
re-determined before this ruling.

Migration 083's replacement (`scripts/migrations/083_specification_retire_in_place.sql:49-54`):
```sql
DROP INDEX IF EXISTS idx_spec_row_identity;
CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(
    parameter_id,
    COALESCE(identity_code, ''), COALESCE(icf_code, ''),
    COALESCE(needs_code, ''),    COALESCE(medical_code, '')
) WHERE retired_at IS NULL;
```

**This is sound**, and matches the migration's own stated intent ("Restricting uniqueness to live
rows means one live determination per cell and any number of retired ones behind it").

- **Two retired rows for the same cell: NOT prevented.** The partial index only enforces uniqueness
  among rows where `retired_at IS NULL`; two rows with `retired_at IS NOT NULL` and identical
  `(parameter_id, identity_code, icf_code, needs_code, medical_code)` can coexist. This is
  **by design** — retired rows are unconstrained history, and the migration says so explicitly
  ("retired rows are unconstrained history", line 48 comment). It is not a gap to fix.
- **One live row + any number of retired rows for the same cell: this IS the intended state.**
  Confirmed by the migration's own comment (lines 29-34): the partial index is "the actual supersede
  mechanism," and `assess_cell.validate_cell_undetermined()` (already updated — §2 above) is what
  enforces "one live row" at write time by refusing a new determination while a live row exists.
- `CREATE INDEX idx_spec_retired ON specifications(retired_at)` (line 57) is a plain (non-unique)
  index for the read pattern "find the live row" / "find retired rows" — unremarkable, no concerns.
- `trg_spec_retire_needs_reason` (lines 63-69) is a `BEFORE UPDATE OF retired_at` trigger requiring a
  non-empty `retirement_reason` whenever `retired_at` is set — structural, fires for hand SQL too.
  Sound; mirrors migration 082's `source_locators.screened_reason` CHECK pattern, as its own comment
  says.

---

## 5. The schema mirror (`schemas/*.py`)

The Pydantic model for `specifications` is `schemas.evidence_state.EvidenceStateRecord`
(`schemas/evidence_state.py:116`), mapped in `validate_pydantic_schemas.py:79` as
`"evidence_state.EvidenceStateRecord": "specifications"`.

**Fields that must be added to mirror migration 083:**

```python
retired_at: Optional[str] = None
retired_by_session: Optional[str] = None
retirement_reason: Optional[str] = None
superseded_by_specification_id: Optional[int] = None
```

Optionally, mirroring `trg_spec_retire_needs_reason` the way `at_least_one_lens` already mirrors the
table's `CHECK (COALESCE(...) IS NOT NULL)` (same file, lines 187-208) — a `model_validator` asserting
that `retirement_reason` is non-empty whenever `retired_at` is set — would keep the Python and SQL
lifecycle rules in the same place the project already keeps the lens rule.

**Pre-existing, out-of-scope context:** `EvidenceStateRecord` is already a lossy subset of the live
35-column table (missing `specification_id`, `tier_basis`, `governing_refs`, `rule_version`,
`derivation_sha`, `code_floor_only`, `value_min/max/unit`, `value_note`,
`falsification_condition`, `has_unverified_sources`, `all_sources_disqualified`,
`regulatory_stratum_only`, `functional_basis`, `derivation_paths`, `derivation_rationale`,
`cultural_claim_anchor`, `created_at/by_session`, `updated_at/by_session`) —
`scripts/audit/graph/extract_db.py:14` already calls Pydantic models here "a lossy subset" for this
reason, and `validate_pydantic_schemas` (advisory) already reports these as case-(b) drift today,
independent of this migration. Not this task's job to close, but the 4 new columns should not be
added to a model that is already known-incomplete without noting that the model was incomplete
before 083 too.
