# session_2026-09-13-clear-circulation-corpus

**Owner ruling, 2026-09-13:** *"Basically all the circulation rows that have been
produced are not able to be trusted, so we have to redo them all from the start."*

Preceded by: *"I want you to clear all the recent research performed and how it went
down the pipeline."* The scope was widened by the second statement from batches 06–07
to the whole circulation corpus, which reaches back to batches 04 and 05.

## What this session did

Emitted one compensating data migration deleting **229 rows** — every row any stage
of the pipeline produced under the slug `accessible-circulation-geometry`. No
analysis, no retrieval, no admission. The canonical DB was not written directly
(rule 3); the migration is append-only and the batch migrations that wrote these
rows stay on disk and stay applied.

## Why the scope is the slug and not the sessions

The obvious reading of "the recent research" is batches 06 and 07. That reading is
wrong in two places, and both were found by deriving the closure rather than
listing sessions:

- **33 `observed_terms` rows** were written by `session_2026-09-03-defect-programme`,
  which is not a research batch at all. Every one of them points at a circulation
  `ref_id`. They are circulation term-harvest wearing another session's stamp.
- **1 `source_locators` row** sits in an 881-row table whose other 880 rows have
  nothing to do with circulation.

A session-scoped delete would have left both behind, and the second one silently:
`source_locators` is the table a re-run's R9 duplicate-DOI pre-check reads, so a
stale locator for a deleted source is exactly the row that makes a re-run cross-file
against a `ref_id` that no longer exists.

## The closure, as deleted

| Stage | Table | Rows |
|---|---|---|
| specification | `specifications` | 2 |
| specification | `gaps` (GAP-001, GAP-002) | 2 |
| judgment | `extraction_relations` | 6 |
| judgment | `source_value_extractions` | 10 |
| base | `base_parameters` (the TERM-001/002 promotions) | 2 |
| research | `term_adjudications` | 6 |
| research | `observed_terms` | 42 |
| evidence | `evidence_population_match` | 19 |
| evidence | `evidence_source_authors` | 52 |
| evidence | `search_admissions` | 11 |
| evidence | `source_locators` | 1 |
| evidence | `source_slug_links` | 13 |
| evidence | `evidence_sources` | 13 |
| research | `citation_mining` | 9 of 19 |
| research | `search_candidates` | 21 of 81 |
| research | `search_executions` | 20 of 48 |
| | **total** | **229** |

## What was kept, and why none of it is research output

- **`terms`, `term_aliases`, `slugs`** — base vocabulary, minted 2026-05-09, months
  before any of this. TERM-001 `ramp gradient` and TERM-002 `corridor width` survive
  as terms. What went is `base_parameters`, which is the *promotion* of those terms
  into the parameter layer, and that promotion is research output.
- **`research_code_leads`** (83) — a restored register carrying neither `ref_id` nor
  `slug`.
- **`gaps` GAP-B01-\*, GAP-B02-\*** (5) and every `room-acoustic-performance` row
  across `search_executions` (28), `search_candidates` (60) and `citation_mining`
  (10) — acoustics batches 01 and 02, out of scope.
- **`decisions`** (188), untouched.
- **`retrieval-log/`** — untouched on disk. The payload bytes are the evidence. A
  re-run verifies against the same bytes and re-fetches nothing, which also means
  the re-run can be checked against what the first run actually received.
- **`sessions/`, `attestations/`** — the record that the work happened. Clearing the
  rows is not erasing the audit trail, and the earlier batch records stand as
  written.

## The defect the rehearsal caught

The first draft ordered `source_slug_links` **last** among the ref-reached tables,
reasoning that every ref-scoped selector reads it. That is true and it is also a
child of `evidence_sources`, so the two requirements are in direct conflict: order
it last and the FK fails on `evidence_sources`; order it first and every selector
after it scopes to nothing, deleting almost nothing while reporting success. The
rehearsal against a scratch copy failed with `FOREIGN KEY constraint failed`
thirteen statements in. Resolved by materialising the ref list into a temp table
before the first delete, so ordering and selector correctness stop competing.

**The silent branch is the one worth recording.** Had the draft happened to order the
junction first instead, the migration would have applied cleanly, reported success,
and left the corpus mostly intact — and every gate would have been green over it.

## Verification

- `PRAGMA foreign_key_check` empty before and after, on the rehearsal and on canonical.
- Keep-list asserted row-by-row against the pre-migration DB: acoustics, terms,
  aliases, slugs, code leads and decisions all unchanged.
- Residual sweep for circulation rows anywhere in the schema: zero.

## State after

No `specifications`, no `evidence_sources`, no `source_value_extractions` anywhere in
the corpus. `v_best_practice` surfaces 0 rows. The circulation slug is back to base
vocabulary with nothing produced under it, which is the state a re-run needs.

Note that this also clears the blocker recorded in the verification pass earlier
today: both cells were frozen at `pending` because `assess_cell` refuses on the
existence of a `specifications` row. Those rows are gone, so the cells are
determinable again. **That is a side effect of clearing, not a supersede design** —
the underlying question, what happens when a determined cell meets new evidence,
is still open and still an owner decision.
