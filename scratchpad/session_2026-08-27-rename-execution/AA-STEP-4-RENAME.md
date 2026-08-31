# Step 4 — the rename, argued both ways, with the insurance run

**Status: BUILT AND VERIFIED AGAINST SCRATCH. NOT APPLIED TO CANONICAL.** The map carries more of
my judgment than any prior step, and a wrong name costs a second sweep — the one thing I have argued
against all session. The evidence is below so the decision is cheap.

---

## C-8 · What does "the insurance" have to be?

**AGONIST.** Run the checks after the migration. They are green or they are not.

**ANTAGONIST — the checks cannot see this failure.** 33 of 66 tables hold **0 rows**. A rename that
breaks a reader on an empty table renders nothing, and a byte-diff of the regenerated output
certifies it clean. That is the 2026-08-19 class exactly: six gates passed a fabrication because each
asked whether fields were *populated*, never whether they were *true*. **"The checks pass" is not
evidence about the half of this schema that is empty.**

**RESOLUTION — build the instrument first, and mutation-test it.** `scripts/audit/rename_insurance.py`
snapshots every structural fact a rename must preserve and compares two snapshots under a name map:
row counts, column sets, every FK edge, every view's row count **and its recursively resolved base
tables**, indexes, triggers, CHECK text. Proven to fail before being trusted:

| injected | detected |
|---|---|
| deleted 1 row | `ROWS CHANGED: rooms(17) -> rooms(16)` |
| dropped 2 FKs | `FK LOST: source_slug_links.ref_id -> evidence_sources.ref_id` |
| broke an existing view | `VIEW BROKEN: v_pending ERROR: no such table` |
| re-routed a view | `VIEW BASE TABLES CHANGED: expected [gaps, specifications] got []` |
| unchanged control | `PASS` |

A `writable_schema` mutation was also tried and **rejected as a bad test** — it produced a malformed
schema SQLite refuses to open, which proves nothing about a rename.

---

## C-9 · Does the migration preserve pointers and walkability? — **measured, not assumed**

**AGONIST.** `ALTER TABLE RENAME` rewrites `REFERENCES` clauses and view bodies automatically on
SQLite 3.45.1. So pointers survive.

**ANTAGONIST.** That was measured on a two-table fixture by a prior audit. **This schema has 18
views, several nested, and 80 foreign keys.** A claim from a fixture is not a claim about the real
object, and `CLAUDE.md` rule 4 says a 0-row object is unproven — 11 of the 18 views return 0 rows, so
none of them would *visibly* break.

**RESOLUTION — run it and measure.** Applied to a scratch copy:

```
64 ALTER statements
PRAGMA foreign_key_check   -> clean
rename_insurance --compare -> PASS — names changed, structure identical
                              (66 tables, 18 views, 80 foreign keys)
```

**All 18 views survived with identical row counts and correctly re-pointed base tables. All 80
foreign keys preserved. Every index and CHECK intact.** Pointers and walkability are verified
empirically on the real schema, not inferred from a fixture.

---

## C-10 · The sweep — and the number that would have caused a disaster

**AGONIST.** Sweep every file that names a renamed table. Measured: **959 live files.**

**ANTAGONIST — that number is a trap, and acting on it would corrupt the repository.** The top
"callers" are ordinary English words:

| name | files |
|---|---:|
| `populations` | 428 |
| `decisions` | 427 |
| `items` | 397 |
| `specifications` | 321 |

**A find-and-replace across 959 files would rewrite the word "decisions" inside every governance
document in the repository.** 520 of the 959 are `.md` prose.

**RESOLUTION — sweep SQL-context references only**, i.e. a name preceded by
`FROM|JOIN|INTO|UPDATE|TABLE|REFERENCES`. Measured that way, with immutable migrations excluded:

> **65 files · 271 reference sites.**

Concentrated where expected: `scripts/db.py` 26 · `scripts/tests/test_db_integrity.py` 24 ·
`tools/pipeline_completeness.py` 15 · `tools/regenerate_vetting_surface.py` 11.

**`scripts/migrations/` is excluded and must never be edited** — data migrations are immutable and
replay; that is what the `AFTER_DATA` marker exists for.

---

## C-11 · How much of this map is RULED, and how much is mine?

**This is the honest accounting, and it is why this step stops here.**

| | count | source |
|---|---:|---|
| hand-off objects → `<stage>_items` | 5 | **ruled** — D-0167, D-0168 |
| owner-ruled renames (`icf_*`, taxonomies, `base_room_types`, `access_need_icf_codes`) | 8 | **ruled** — D-0169, D-0171 |
| stage prefix only, subject untouched | ~19 | mechanical |
| **subject renames following Part D's grammar** | **~33** | **my judgment** |
| `items` → `render_provisions` | 1 | **my coinage — contentious** |

**ANTAGONIST.** ~34 of 66 names are mine. A2 found Part E's own subject choices inconsistent (D1: it
assigned `res_searches` on taste while giving `citation_mining` a `_runs` suffix; D2: `syn_convergence`
is a mass noun against the plural rule). If I inherit that inconsistency, the correction is a **second**
rename — two sweeps of 65 files, and migration 064 exists because one sweep missed one view.

**RESOLUTION — the map goes to the owner before canonical is touched.** Everything reversible is
done: the migration is written, applied to scratch, and proven structure-preserving; the sweep
surface is measured and bounded. What remains is a naming judgement that is cheap to correct now and
expensive to correct later.

**Sanity checks on the map, all passing:** no stutters (`evidence_evidence_sources` eliminated), no
collisions, `_items` reserved to the five ruled hand-off objects only, and two tables correctly keep
their existing names (`evidence_source_authors`, `specification_source_links`).
