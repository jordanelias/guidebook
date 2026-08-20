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
| **Tables** | 66 | **63** | **−3** | low-to-medium — **two of five folds were refuted by my own adversarial pass** (§2.1, §2.3). What survives: §2.2 (−1) and the two Part-3 cuts (−2). |
| **Views** | 18 | **16** | **−2** | high (a further 11 need a wire-or-retire ruling) |
| **Duplicated columns** | 48 locator columns across 3 tables | **16 in one place** | **−32** | high |
| **Executables** | 132 | **~106** | **−26** | high for 19, medium for 7 |
| **Skills** | 49 | **49** | **0** | high — *no skill is cuttable on any test I ran* |

**The headline is a retraction.** §2.1 originally claimed a fold that was simultaneously a fix
for a broken structural hop. **It was wrong** — the fold would have destroyed three working
foreign keys to create one, and the obvious alternative fails against the archived data. The
retraction is in place, and it is the most useful thing in this document: *identical column
shape is not identical meaning*, and I applied a structural test where a semantic one was
needed.

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

### 2.1 Four population-link tables → one — ~~a fold that is also a correctness fix~~ **RETRACTED**

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

> ## ⚠ RETRACTED 2026-08-11 — this fold was wrong, and so was its replacement
>
> **What I proposed:** collapse the four into one
> `population_links(parent_kind, parent_id, population_code REFERENCES populations, match_grade, …)`,
> on the argument that it fixes hop 4's missing FK by construction. **Net −3 tables.**
>
> **Why it is refuted.** A foreign key can only reference one fixed table. A `parent_id` column
> that holds a `citation_id` on one row and a `probe_id` on the next **cannot be constrained at
> all** — verified: SQLite rejects the mismatched row, so the constraint has to be dropped
> entirely. The trade is therefore:
>
> | | Today | After the proposed fold |
> |---|---|---|
> | population FK | 3 of 4 tables have it | 1 table has it |
> | parent FK | **3 real, enforced** | **0 — unenforceable by construction** |
>
> **I proposed trading three working foreign keys for one**, in a repository whose stated
> problem is that its most important relationships are not schema-enforced. The three sibling
> tables are not duplication to be collapsed; they are three correctly-keyed tables that happen
> to share a column list. **Identical shape is not identical meaning.**
>
> **The obvious replacement is also wrong.** "Just add the FK to
> `evidence_population_match.target_population`" fails on inspection of the pre-reset data:
> **22 of its 30 distinct values would violate that FK** — they are prose, not codes
> (*"Autistic students in school built environments"*, *"DEAF/HoH adults relying on
> lipreading"*). The column was never used as a code column. Adding the FK while the table is
> empty would pass trivially and silently redefine the column's meaning, so the next writer —
> following the only precedent that exists — would immediately break it.
>
> **What the finding actually is.** `target_population` is not a code column missing a
> constraint; it is a **prose column that three scripts read as three different types**. The
> fix is a D-SCHEMA decision to split it — `target_population_code` (FK'd, nullable) plus
> `target_population_note` (free text) — and to migrate the 64 archived rows by hand, since no
> parser will do it. That is more work than either shortcut and it is the only version that
> survives contact with the data.
>
> **Net: 0 tables. The −3 is withdrawn**; Part 0's table count is corrected from −9 to −6
> (66 → 60).

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

> **⚠ CORRECTED 2026-08-11 — the fold direction was backwards.** I proposed folding
> `case_study_outcomes` *into* `case_studies.outcome_data`. But `case_study_outcomes` is
> **1:N structured data** — `(metric, value, source, tier)` per outcome, with a real FK to the
> parent — while `outcome_data` is a single TEXT column. Folding N structured rows into one
> text blob destroys the structure and the tier grading, which is exactly the evidence metadata
> this project exists to preserve. Same for `case_study_strategies` (N strategies per study).
>
> **The duplication is real; the resolution runs the other way.** Keep the child tables, and
> **drop the parent's unstructured rival columns** — `outcome_data`, and audit `roi_data`,
> `funding_sources`, `sources` for the same overlap. That removes the shadow store without
> losing a key or a grade. `case_studies` is 37 columns wide precisely because prose fields
> were added beside the structured children rather than instead of them.
>
> `economics_entry_populations` also survives: it carries a **real FK to `populations`**, which
> is the constraint §2.1 just established is the scarce thing here.
>
> **Net: 0 tables — but −1 to −4 unstructured columns, which is the actual defect.**

The remaining junctions — `case_study_populations`, `case_study_specs`, `economics_entry_specs` —
are true many-to-many links onto the `populations` and `items` spine. The register's §1.4c names
`case_study_specs` as the junction that would exercise the item spine when the 26-entry
compendium is loaded. All stay.

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

1. **§2.1 — do not fold. RETRACTED.** What remains is a D-SCHEMA decision to split
   `evidence_population_match.target_population` into a code column and a note column. Still
   first in the ordering, because `evidence_population_match` is spine (4 phases) and the 64
   archived rows need hand migration — but it is a decision to take, not a fold to execute.
2. **§2.3 — do not fold. CORRECTED.** Drop the parent's unstructured rival columns instead,
   keeping the structured children. Before loading the compendium, not after.
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

---

## Part 7 — Adversarial review of this ledger, and the differential-code-audit question

### 7.1 What the review killed

Run on 2026-08-11 against this document's own claims, default verdict REFUTED.

| Claim | Verdict | Test that killed it |
|---|---|---|
| §2.1 fold 4 population-link tables → 1, "also fixes hop 4" | **REFUTED** | A FK targets one fixed table. A polymorphic `parent_id` cannot be constrained — verified in SQLite. The fold trades **3 working parent FKs for 1 population FK.** |
| The replacement — "just add the FK to `target_population`" | **REFUTED** | 22 of 30 distinct pre-reset values are prose, not codes. The FK would pass trivially on an empty table and break the first real writer. |
| §2.3 fold `case_study_outcomes` into `case_studies.outcome_data` | **REFUTED, direction backwards** | The child is 1:N structured `(metric, value, source, tier)`; the parent column is one TEXT blob. The fold destroys the tier grading. Drop the parent's prose columns instead. |
| §2.2 coverage fold, Part 3 cuts, Part 4 tooling, Part 5 skills | **SURVIVE** | `search_coverage`/`search_languages` FK only to `slugs`, which the fold preserves; the two cuts are 0-rows-in-both-databases; the tooling and skill findings were unaffected. |

**Table net falls from −9 to −3.** Two of five folds were wrong, and both failed the same way:
**I tested column shape and inferred meaning from it.** Identical shape, different semantics —
three correctly-keyed sibling tables read as duplication; a structured child read as a
duplicate of a prose column. The phase-multiplicity test in Part 1 is structural too, which is
why Part 1's stated limit should be read as applying to the folds, not only the cuts.

### 7.2 Is a differential code audit worth running?

**Yes, but not as a style survey — and I know that because I ran one and two of its five
dimensions dissolved on inspection.** Measured across the 132 executables, normalised to the
scripts that actually face each decision:

| Dimension | Consistency | Has a registered check? |
|---|---|---|
| DB path resolution (`GUIDEBOOK_DB_PATH`) | **74%** honour it, **0%** hardcode | **yes** — `db_path_env_audit.py` |
| Read-only opens among read-only scripts | **76%** use `mode=ro` | **yes** — added 2026-08-06 |
| Path handling (`pathlib` vs `os.path`) | 54% / 50%, **18 files use both** | no |
| Exit convention | 83% `sys.exit`, 47% also return codes | no |
| SQL parameter style | 39% f-string / 34% bound | no |

**The pattern is the finding: every dimension with an enforcer sits at ~75%; every dimension
without one sits at ~50%, which is indistinguishable from no convention at all.** That is the
repo's own five-level enforcement spectrum (CLAUDE.md §2) measured from the outside, and it
says the spectrum works.

**But the last row is a warning about the audit's own output.** The f-string SQL split looks
like a finding and is not: inspecting all 135 interpolations shows they are safe idioms —
`UPDATE {table} SET {', '.join(sets)} WHERE ref_id = ?`, `IN ({placeholders})`, `PRAGMA
user_version = {version}` — where identifiers are interpolated because they *cannot* be bound
and the values are still parameterised. **A style-dispersion metric flagged a security-shaped
problem that does not exist.** Had I reported the raw numbers, that is what would have shipped.

**So the recommendation is narrow.** Do not commission a general "how consistent is our code"
audit; its output is mostly noise requiring per-hit adjudication, and this repo has already
recorded five occurrences of a check that looks like success while examining nothing. Commission
instead the specific version that earns its keep:

> **A convention-vs-enforcement gap detector.** For each convention the repo has *stated*
> anywhere — in `CLAUDE.md`, `references/project-standards.md`, a skill, or a docstring — ask
> whether a registered check enforces it. Report the stated-but-unenforced set.

That is a bounded question with an actionable answer, it reuses the existing check registry
rather than adding a register (guardrail 3), and it is the same shape as the finding that
`run_checks.py` never reads the `deps:` field the registry has always declared. The general
style audit answers "are we consistent?", which nobody needs. This one answers "which of our
own rules are we not checking?", which is the question every finding in the reconciled register
turned out to be an instance of.

**Cost note, stated because the ledger is about pruning:** the detector is one script against
the existing registry. It should not become a fourth register, and if it cannot be expressed as
a check in `governance/check-registry.yaml`, that is evidence it should not be built.
