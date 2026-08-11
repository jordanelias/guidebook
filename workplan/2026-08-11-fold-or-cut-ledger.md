# 2026-08-11 — Fold-or-cut ledger: every table, view, tool and skill against the twelve phases

**Status:** LEDGER — nothing executed. Answers one question for each object in the repository:
**does it earn independent existence, or does it fold into something else, or does it go?**
**Method:** independence is tested against the twelve pipeline phases
(`workplan/2026-08-11-remediation-and-pipeline-anatomy.md` Part 2), not against row count.
An object named by one phase is a stage-local artifact and a fold candidate by default; an
object named by four or more is spine and is not.
**Governing constraint from the owner:** *there are no limits on table sizes.* So width is not a
reason to keep two tables apart, and normalisation that exists only to keep tables narrow is
cost without benefit. Every fold below moves in that direction.
**Subject:** `3eed5d4`. 66 tables · 18 views · 132 executables · 49 skills.

---

## Part 0 — The answer in one table

| Category | Now | After the folds | Net | Confidence |
|---|---|---|---|---|
| **Tables** | 66 | **57** | **−9** | high — 7 of the 9 are empty and free to move today |
| **Views** | 18 | **16** | **−2** | high (a further 11 need a wire-or-retire ruling) |
| **Duplicated columns** | 48 locator columns across 3 tables | **16 in one place** | **−32** | high |
| **Executables** | 132 | **~106** | **−26** | high for 19, medium for 7 |
| **Skills** | 49 | **49** | **0** | high — *no skill is cuttable on any test I ran* |

**The headline is not the count.** It is that **one fold is simultaneously the fix for a broken
structural hop** (§2.1), and it is free today because all four tables involved are empty.

---

## Part 1 — Independence measured against the twelve phases

Every table and view, by how many of the twelve phases name it:

| Phases naming it | Count | Reading |
|---|---|---|
| **4+** | 15 | **Spine.** `evidence_sources`(10) `items`(8) `citation_mining`(6) `search_executions`(5) `item_population_links`(5) `populations`(5) `gaps`(5) `item_bpc_links`(5) `source_slug_links`(5) `evidence_cell_state`(5) `jurisdictional_values`(4) `slugs`(4) `connections`(4) `evidence_population_match`(4) `reasoning_doc_citations`(4). Not foldable, not cuttable. |
| **3** | 10 | Genuine cross-stage carriers. Leave alone. |
| **2** | 21 | Mostly real. Three pairs fold (§2.2, §2.4). |
| **1** | 28 | **Stage-local artifacts — the fold pool.** 13 of the 28 are views. |
| **0** | 11 | Split: 4 are infrastructure (`data_migrations`, `db_meta`, `decisions`, `sqlite_sequence`) and stay; 4 are orphaned children of stage-7 parents (§2.3); 3 are unread views. |

**The test's own limit, stated up front.** Phase-multiplicity measures what the *anatomy document*
names, not what code does. It is a good proxy — the anatomy was written from the schema — but a
table the anatomy forgot would score 0 and look cuttable. That is why every cut below is
additionally checked against: rows in the live DB, rows in the pre-reset DB, live writers, live
readers, and mention in any governance document. **No object is cut on phase-count alone.**

---

## Part 2 — The folds

### 2.1 Four population-link tables → one. *This fold is also a correctness fix.*

| Table | Cols | Shape | FK to `populations` |
|---|---|---|---|
| `citation_population_links` | 5 | `(citation_id, population_code, note, created_at, created_by_session)` | **yes** |
| `extraction_population_links` | 5 | `(extraction_id, population_code, note, created_at, created_by_session)` | **yes** |
| `probe_population_links` | 5 | `(probe_id, population_code, note, created_at, created_by_session)` | **yes** |
| `evidence_population_match` | 11 | `(match_id, source_ref, target_population, study_population, sample_size, match_grade, …)` | **NONE** |

The first three are **structurally identical** — same five column names, differing only in which
parent they point at. They are one table written three times because three stages each needed
"attach a population to my row."

The fourth is the graded one, and it is **hop 4 of the seven-hop walk, which the remediation
register records as BROKEN**: *"`target_population` has no FK; recovered by a regex over prose
(`assess_cell.py:180`); three scripts treat the column as three different types."*

**So the schema already contains the fix for its own broken hop, three times over.** The three
stage-local siblings all key population correctly. A single

```
population_links(parent_kind, parent_id, population_code REFERENCES populations,
                 match_grade, study_population, sample_size, note, created_at, created_by_session)
```

collapses **4 tables → 1** and makes the FK on hop 4 true by construction, rather than as a
separate migration nobody has scheduled. All four tables hold **0 rows** in both the live and the
pre-reset database, so the migration is pure DDL with no data movement — the cheapest it will
ever be, and it gets monotonically more expensive once determinations start being written.

**Net: −3 tables. Also closes one of the two "cannot be recorded at all" legs of the project's
constitutive claim.**

### 2.2 Two coverage tables → one

`search_coverage` `(slug, jurisdiction, status, co1_attempted, tier5_attempted, tier6_attempted, …)`
and `search_languages` `(slug, language, status, results_count, …)` are the same table on two
axes — both stage 3–4, both keyed on `slug` + one axis value, both 0 rows.

`search_coverage(slug, axis_kind, axis_value, status, attempted_flags, results_count, …)`. With
no width constraint, the union of both column sets in one table costs nothing. **Net: −1.**

### 2.3 Case studies 5 → 3, economics 3 → 2

`case_studies` carries **37 columns**, including `outcome_data`, `roi_data`, `funding_sources`,
`construction_cost`, `remediation_cost` and `sources`. Beside it sit `case_study_outcomes`
`(outcome_id, case_study_id, metric, value, source, tier)` and `case_study_strategies`
`(strategy_id, case_study_id, strategy)` — **both named by no phase at all**, both 0 rows in both
databases, both duplicating concepts the parent already has columns for.

Same shape in economics: `economics_entry_populations` is a 2-column junction named by no phase,
on a parent with 25 columns and 5 pre-reset rows.

Fold `case_study_outcomes`, `case_study_strategies`, `economics_entry_populations` into their
parents. **Keep `case_study_populations`, `case_study_specs` and `economics_entry_specs`** — those
are true many-to-many junctions onto the `populations` and `items` spine, and the register's
§1.4c specifically names `case_study_specs` as the junction that would exercise the item spine
when the 26-entry compendium is loaded. **Net: −3.**

> **This makes the register's own recommendation cheaper, not harder.** §1.4c says load the
> compendium (~26 entries) and the economics corpus as the first content work, because they are
> bounded corpora with known targets. Loading 26 entries into 3 tables is a smaller migration
> than into 5, and the folds are free while the tables are empty. **Fold first, then load.**

### 2.4 One fact, two representations, inside one stage

`search_executions.admitted_ref_ids` is a TEXT list of admitted refs. `search_admissions` is a
junction `(exec_id, ref_id)` carrying the same fact with real foreign keys to both parents.

This is the C11 dual-representation class inside a single stage. Keep the junction — it is the
one with referential integrity — and drop the column. **Net: −1 column, −1 shadow store.**

### 2.5 The locator block: 48 columns expressing one concept

Three tables each carry the **identical 16-column locator block** (`locator_scheme`,
`loc_division` … `loc_subclause_end`, `loc_note`):

| Table | Locator cols | Total cols |
|---|---|---|
| `jurisdictional_values` | 16 | 32 — **half the table** |
| `source_value_extractions` | 16 | 49 |
| `reasoning_doc_citations` | 16 | 34 |

48 columns for one concept. The 2026-08-09 locator document already proposed a scheme registry
table for FK integrity; this is the same argument one level up. One `locators` table keyed by
`(owner_kind, owner_id)`, or — since width is free — one locator *view* over a shared block. The
decision is which; the duplication is not in question. **Net: −32 columns, 0 tables.**

### 2.6 Views: 13 of 18 have no reader

17 of 18 views return 0 rows (expected post-reset). More telling: **13 have zero live `.py`
readers.** Only `v_divergence`, `v_best_practice`, `v_coverage_jurisdiction`,
`v_coverage_language` and `v_coverage_branch` are read by code.

The odd one is `v_coverage_priority` — **7,210 rows and no reader at all.** It is named by three
phases, so it is intended surface; nothing consumes it.

Two views (`v_root_id_conflicts`, `v_unregistered_roots`) exist only to police
`external_root_registry`, which §3 recommends cutting; they go with it. **Net: −2.** The other 11
need a **wire-or-retire ruling, not a cut** — several are the declared query path in the research
contract, and retiring a documented query path is a different act from deleting dead code.

---

## Part 3 — The cuts

Only two objects survive every test for removal — never populated in either database, named by at
most one phase, no live reader, no live writer:

| Object | Live rows | Pre-reset rows | Phases | Live code | Verdict |
|---|---|---|---|---|---|
| `situations` | 0 | **0** | 1 | none | **CUT candidate** — designed, migrated, never written in the project's entire history. Named in 4 governance documents, so this is a D-SCHEMA retirement with a paper trail, not a deletion. |
| `external_root_registry` | 0 | **0** | 7 | none | **CUT candidate**, together with `v_root_id_conflicts` and `v_unregistered_roots` which exist solely to police it. |

**Everything else empty stays.** `case_studies`, `economics_entries`, `room_items`,
`connection_targets`, `supersession_check`, `item_audit_runs` and the rest are
*designed-awaiting-content* — the register's §1.4c verdict, which I did not disturb: the content
exists in markdown (a 56 KB case-study compendium, `references/economics/`, and 142 room↔item
pairs sitting in an archived seed script), and the missing piece is the writer, not the table.
**Emptiness is not the test. Never-having-been-written plus no-code plus one-phase is the test,
and only two objects meet it.**

---

## Part 4 — Executables: 132 → ~106

| Bucket | Count | Lines | Disposition |
|---|---|---|---|
| Registered as an active check | 55 | 16,815 | keep |
| Library (imported by something live) | 29 | 8,883 | keep |
| Workflow entrypoint | 6 | 3,281 | keep |
| **Quarantined** | 16 | 3,590 | keep as-is — `tooling-register.md` §6.5 makes quarantine-with-reason terminal; needs the four-way `disposition:` split, not deletion |
| **Unreferenced** | **26** | **7,330** | the cut pool |

**The one-shot importer directories are the cut.** `scripts/convert/` (13), `scripts/db/` (3) and
the non-guard half of `scripts/migrate/` are the tools that built the database from markdown in
April–May. That job is finished, and the reset then emptied what they loaded.

- `scripts/db/**` targets `data/db/guidebook.db` — **a path that does not exist on disk.**
- `scripts/convert/` — 13 scripts, 2,669 lines, referenced only from prose and one legacy caller.
- **Retiring them is also the fix for two open findings.** My reconciled register's **R-01** (the
  unguarded replay script that can silently undo the clean-room reset) and **R-05** (two more
  unguarded legacy writers) are exactly `scripts/migrations/session_2026_05_11g_replay.py`,
  `scripts/migrate/init_database.py` and `scripts/migrate/phase_jv_appendix_a.py`. Retiring the
  one-shot layer to `_archived/` removes the danger and the clutter in one act.

Plus the small set: the superseded singular validators `validate_item.py` and
`validate_conflict.py` (439 lines) which shadow the live plural ones by one character, and **four
database initialisers** (`scripts/init_db.py`, `scripts/db/init_db.py`,
`scripts/migrate/init_database.py`, and `migrate_db.py --rebuild`, the only one that works)
collapsing to one.

**The one-shot layer measured exactly:** `scripts/convert/` (13) + `scripts/db/` (3) +
`init_database.py` + `phase_jv_appendix_a.py` + the replay script = **19 scripts, 6,074 lines.**
**Realistic net: −19 with high confidence, −26 if the singular validators and the surplus
initialisers go too.**
`scripts/audit/graph/__init__.py` appears unreferenced and is not — it is a package marker; that
is my method's artifact, not a finding.

---

## Part 5 — Skills: nothing to cut, and I checked three ways

**This is a negative result and it is the most useful thing in this section.**

1. **Reachability.** All 49 active skills have inbound references outside their own file and the
   registry. The lowest is `question-author` at 3. **Zero unreachable.**
2. **Function-pair overlap.** The obvious fold candidates are the auditor/researcher pairs —
   `economics-auditor`/`economics-researcher`, `functional-deficit-auditor`/`-researcher`,
   `connection-auditor`/`connection-discovery`. **Reading them refutes the fold in every case:**
   each pair is audit-vs-produce, and two of the three say so explicitly in their own frontmatter
   (*"Distinct from…"*, *"Complements multilingual-research (top-down)…"*). Folding them would
   merge a checker into the thing it checks.
3. **Deprecation hygiene.** The 12 deprecated skills are already parked in `skills/deprecated/`
   and listed with retirement reasons under a `## Deprecated skills` heading. This is the repo
   doing it correctly.

The only skill-layer action is the inverse of a cut: **register `integrity-protocol` and
`supersession-audit`**, which are active, unlisted, and currently failing
`adherence_log_audit` CHECK 3 with four forward-only attestations depending on the fix (R-24).

**The volume is not in the skills.** It is in one-shot tooling (7,330 lines), frozen prose
(~40,890 lines), and duplicated schema (48 locator columns) — not in the 49 authoring protocols.

---

## Part 6 — Sequence, and what each fold costs

Every fold in Part 2 touches a table that is **empty in both the live and the archived database**,
except the locator block (§2.5, which is DDL-only) and `search_executions.admitted_ref_ids`
(§2.4, one column drop). There is no data migration to write for any of them.

1. **§2.1 population links (4→1).** First, because it is the only one that also fixes a broken
   hop, and because `evidence_population_match` is spine (4 phases) — every day of content work
   makes it costlier.
2. **§2.3 case-study and economics folds (−3).** Before loading the compendium, not after.
3. **§2.2 coverage axes (−1)** and **§2.4 shadow store (−1 column).**
4. **§2.5 locator block.** Needs the owner's choice of shape (table vs shared block) first.
5. **Part 4 one-shot retirement (−16 executables).** Independent of all the above; also closes
   R-01 and R-05.
6. **Part 3 cuts (−2 tables, −2 views).** D-SCHEMA, owner-gated, and last — they are the only
   irreversible items here and the smallest prize.
7. **§2.6 views.** A wire-or-retire ruling on 11 views, not a cut.

**What this does not do.** None of it makes the guidebook more true about the built environment,
and none of it is content. It removes 9 tables, 2 views, 32 duplicated columns and ~26 scripts
from the surface a future session has to understand, and it closes two open findings on the way.
The case for doing it now rather than later is that **seven of the nine table folds are free
while the tables are empty, and stop being free the moment content resumes** — which is the same
argument DR-2026-08-06 made about migrations, applied to the schema the reset left behind.

---

*Counts derived on 2026-08-11 against `3eed5d4`: phase-multiplicity from the anatomy document's
Part 2; row counts from `data/guidebook.db` and `_archived/data/corpus-pre-reset-2026-08-06.db`;
reader/writer reachability from SQL-pattern and plain-name scans over all non-archived code,
excluding `scripts/migrations/`. Re-derive before acting — Part 1 states the method's own limit.*
