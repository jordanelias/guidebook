# Pipeline operations — what each one consumes, produces, and logs

**Status:** PROPOSED · **Date:** 2026-08-02 · **Scope:** definitional

This document exists because **"mining" in this project means at least two different
operations with different inputs, different outputs, and different tables** — and the bare word
has been used for both. Migration 040 named a column `citation_mining_status` rather than
`mining_status` for exactly this reason.

The rule this document establishes:

> **No column, check, or skill may use "mining" unqualified.** Name the operation.

---

## 1. The five operations

The single most useful distinction: **discovery produces _sources_, extraction produces _values_,
synthesis produces _statements_.** Confusing them is what lets a source be "processed" in one sense
and untouched in another.

| # | Operation | Consumes | Produces | Output table | Log of the act |
|---|---|---|---|---|---|
| 1 | **Search execution** | a query × index × language × jurisdiction | screened results | `search_candidates` | `search_executions` |
| 2 | **Citation mining** *(anchor-driven discovery)* | one confirmed source, as an anchor | further candidate **sources** | `search_candidates` / new `evidence_sources` | `citation_mining` (per slug × local ref) + `evidence_sources.citation_mining_status` |
| 3 | **Gap-driven mining** *(gap-driven discovery)* | one open row in `gaps` | further candidate **sources** | `search_candidates` | `gap_mining` |
| 4 | **Data extraction** *(value capture)* | one source we hold | **values**, with locator and lens grain, keyed on the parameter (`db.py add-extraction`) | `source_value_extractions`, `spec_value_probes`, `jurisdictional_values`, `economics_entries` | `evidence_sources.data_capture_status` |
| 5 | **Synthesis** | extracted values across sources for one (parameter × lens) | a **best-practice statement** with an evidence marker | `specifications` + `convergence_assessment` | `specifications.derivation_sha`, attestations |

*Rows 4 and 5 read `(item × population)` until 2026-09-10. Migrations 071 and 073 re-keyed both
tables onto `parameter_id` and the four lens columns (owner 2026-08-26 and 2026-08-28); the item
layer was emptied 2026-09-01 and `items` is a Part-4 render rollup derived from specifications.*

*Row 4's status column is **maintained by `db.py add-extraction`**, which sets
`data_capture_status='captured'` in the same transaction as the INSERT — before that it had no
writer at all, and the first extraction row would have turned the blocking `test_db_integrity`
C06 red. Read the comment at that UPDATE before relying on it: the column is a derived duplicate
of "does a capture row exist", C06 is therefore a parity check over a dual home, and CLAUDE.md
rule 5 says such a check makes the dual home survivable rather than curing it. This row and C06/C07
are the readers a writer-retire must re-point at the four capture tables' own EXISTS predicates.*

Adjudication (does this source qualify for admission, at which tier) is not a sixth operation —
it is the gate between 1–3 and 4, recorded on the source itself
(`verification_status`, `tier`, `search_candidates.disposition`).

---

## 2. The distinctions that keep being lost

**Citation mining reads a source's _bibliography_. Data extraction reads its _content_.**
A source can be fully mined and hold no captured value, or hold captured values and never have
been mined. They are independent axes, which is why migration 040 gave `evidence_sources` two
separate status columns rather than one "processed" flag.

**Citation mining is source-scoped; gap-driven mining is gap-scoped.** That is why
`citation_mining_status` can live on `evidence_sources` and a gap-mining status cannot. It is
also why `citation_mining`'s primary key is `(slug, local_ref_id)` — one source is mined *for a
given slug*, and a source may serve up to 7 slugs.

**Discovery does not admit.** Producing a candidate is not admitting a source. R10 governs the
boundary: no re-retrieval, no admission.

**Extraction is not synthesis.** Capturing "RT60 ≤ 0.6 s, BB93 §1.2, classrooms" is extraction.
Deciding what the best practice *is* across sources, populations and jurisdictions is synthesis,
and only synthesis is gated to Opus-class authorship (PI rule #2, DR-2026-06-10).

---

## 3. Where each operation stands today

Measured 2026-08-02 and left at that vintage on purpose — every row below predates the
2026-08-12 evidence-stage clearance, after which `search_executions`, `evidence_sources`,
`gaps`, `source_value_extractions` and `specifications` are all **0 rows**. Derive current
numbers rather than trusting these; a row here is a record of the 08-02 state, not a claim
about today.

| Operation | State |
|---|---|
| Search execution | `search_executions` 84 rows, 3 days of activity; 39 admissions logged against 863 sources |
| Citation mining | 100 sources mined, 67 deferred, **696 pending**. Tier 1–2, where R2 obliges the work: **134 pending, 23 deferred, 34 mined of 191** |
| Gap-driven mining | `gap_mining` **0 rows** — the table exists and has never been written to; 50 gaps OPEN |
| Data extraction | **11 of 863** sources have a joinable capture row; 852 pending |
| Synthesis | `specifications` 15 rows of a 93 × 23 grid |

---

## 4. The logging rule, and its unresolved tension

Each operation must leave a row saying it happened, so that "not done" and "done, nothing found"
are distinguishable states rather than the same absence. Migration 040 closed that gap for
operations 2 and 4 at source grain.

**A status column without a biconditional check is an assertion nobody verifies.** The first
backfill of `citation_mining_status` resolved rows by `global_ref_id` alone — NULL in 146 of 183
rows — and left 80 sources reading `pending` while holding a non-deferred mining row. The capture
status had check `C06` from the start; the mining status had no counterpart, so nothing
contradicted it. Both now have one (`C06`, `C08`). Any future status column ships with its check
or it does not ship.

**Unresolved (⚑8 in the current plan):** under migrations-only, a log row is authored by the same
session whose compliance it attests, at commit time, with self-reported timestamps. R8's
append-only check catches deletion, not omission — and omission is precisely what produced 39
logged admissions against 863 sources. There are three possible homes and no fourth: migrations
(confessional, status quo), job-owned direct writers (one DR per table under DR-2026-05-28 §3), or
a new hook-owned class. Until that is decided, "mandatory logging" means "self-reported logging".

---

## 5. Prose and values

A **state** is a coded value: `pending`, `deferred`, `no-full-text`. It goes in a constrained
column so it can be counted, joined and checked.

**Extracted content may be prose** — a verbatim claim, a quoted clause — provided it sits in a
dedicated table with the pointers that make it traceable, alongside the typed value it
accompanies. `source_value_extractions` is the model: `claimed_value` and `claimed_unit` are
typed, `claim_text` is the verbatim quote, `source_section` and the 16 `loc_*` columns are the
locator, and `ref_id`, `slug`, `parameter_id`, the four lens columns and `promoted_to_rdc_id`
carry the trace. *(This named `population_code` until 2026-09-10; migration 073 retired it in
favour of the four lens columns, under the 2026-08-28 owner ruling.)*

What is forbidden is a **state written as prose in a value column**. This is not hypothetical:
four rows held `[author surname pending …]` in `first_author_last`, and because the string was
non-empty the blocking `C03` check counted them as having an author. A missing author passed a
gate by wearing a value's clothes. Check `C07` now forbids the pattern.
