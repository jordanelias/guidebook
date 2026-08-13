# 2026-08-13 — The eleven writerless tables: required, duplicated, or untooled?

**Owner question:** *"If tables have no writers, are they even required? Are they duplicated
somewhere? Or do we just have insufficient tooling?"*

**Answer: insufficient tooling.** None is redundant, none is duplicated, and several are *gated* —
a check refuses to pass a research batch until they are populated. What the migration-history
baseline exposed is that the pipeline has never had a write path past the research stage; the rows
that used to appear in them were placed by hand-authored migration SQL, one batch at a time.

**And the number understates it.** The probe reports 11 because it asks "does any live `.py`
contain a write statement against this table?" Four more tables sit at 0 rows and happen to have a
writer somewhere, so they were not flagged: `source_value_extractions`, `evidence_population_match`,
`source_slug_links`, `case_studies`. The honest statement is not "eleven tables lack a writer" but
**"the post-research pipeline has no write path, and the probe can only see part of that."**

---

## 1. Required? — yes; every one has readers, and three are gated

| Table | Read by | Status |
|---|---|---|
| `reasoning_doc_citations` | 4 Pydantic schemas · `reasoning_doc_citations_audit.py` · `population_integrity_audit.py` · `adherence_log_audit.py` · graph topology · completeness dashboard · vetting surface | Named in the live PI |
| `spec_value_probes` | 4 Pydantic schemas · `pmp_audit.py` · `gap_mining_audit.py` · `validate_population.py` · `population_integrity_audit.py` · vetting surface | Named in `pipeline-operations.md` and the PI |
| `economics_entries` | `research_batch_dod.py` · `test_db_integrity.py` | **GATED** — R12 |
| `search_candidates` | `research_batch_dod.py` | **GATED** — R7 |
| `search_languages` | `research_batch_dod.py` · `research_protocol_audit.py` · `db.py` · `evidentiary_audit.py` | **GATED** — R11 |
| `search_coverage` | `db.py` · `generate_search_queries.py` · `evidentiary_audit.py` · completeness dashboard | Feeds query generation |
| `item_bpc_links` | `assess_cell.py` · `build_site.py` · `spec_page.py` · completeness dashboard | Render path |
| `citation_population_links` · `extraction_population_links` · `probe_population_links` | `schemas/population_links.py` · `population_integrity_audit.py` · `validate_pydantic_schemas.py` · vetting surface | R13 |
| `item_population_elaborations` | `test_db_integrity.py` · the probe | — |

The three gated ones are the sharpest evidence that they are required. `research_batch_dod.py` is
the "before you claim done" gate, and it fails a batch when economic or value data is left in prose
instead of `economics_entries`, when off-slug material is left in prose instead of
`search_candidates`, or when language coverage is unrecorded. **A table something refuses to pass
without is not optional.**

## 2. Duplicated? — no. Two plausible pairs, both genuinely distinct

**The four `*_population_links` vs `item_population_links` (372 rows, populated).** Different
subjects, not different names for one thing:

- `item_population_links` — *which populations a design parameter applies to*. Structural. Populated.
- `citation_population_links` / `extraction_population_links` / `probe_population_links` — *which
  populations a particular citation, extraction or probe speaks to*. Evidential, per artifact.

That split is **R13**, which requires grading population-of-STUDY against population-SERVED on every
admission and warns that a missing match row is "silently claiming they are the same." Collapsing
these into `item_population_links` would destroy exactly the distinction the rule exists to force.

**`spec_value_probes` vs `source_value_extractions`.** Also distinct:

- `spec_value_probes` — a *search structure*: `walk_id`, `step_index`, `direction`, `search_query`,
  `passes_strict`. It records walking a value up or down to find where a standard stops holding.
- `source_value_extractions` — a *captured value from a source we hold*: `claimed_value`,
  `claim_text`, `source_section`, a full locator scheme, `root_id`/`echo_of` provenance.

A probe is how you look; an extraction is what you found. Merging them would lose the walk.

**No other overlap found.** `economics_entries` (25 columns: BCR, currency, study design) has no
partner anywhere. `reasoning_doc_citations` (34 columns, a full locator scheme) is the only
claim-level verification record.

## 3. So what is actually missing

Not tables. **Writers.** Concretely:

| Stage | Has a tool? |
|---|---|
| Research / search logging | Partly — `db.py` and `generate_search_queries.py` read, little writes |
| Candidate triage → `search_candidates` | **No** |
| Value extraction → `source_value_extractions` | **No** |
| Value probing → `spec_value_probes` | **No** |
| Population grading → the three `*_population_links` | **No** |
| Claim verification → `reasoning_doc_citations` | **No** |
| Economics capture → `economics_entries` | **No** |
| Synthesis → `specifications` | `assess_cell.py` only, and it refuses the canonical DB by design |

Every one of those writes has to go through `emit_data_migration.py` → `migrate_db.py`, which is
correct and should not change. What is missing is the layer *above* it: something that takes a
research finding and emits the migration, instead of a session hand-writing INSERT statements.

## 4. Why this is the right finding to have surfaced now

The corpus is empty, so **nothing is lost by building the write path before the content**. The
alternative — repopulate by hand-authored SQL again — reproduces the exact condition that made the
migration history unmanageable in the first place: 297 data migrations, each a bespoke INSERT batch,
which then pinned retired table names and had to be frozen.

**Recommended sequence, for the owner to rule on:**

1. **Write-path first, content second.** One emitter per pipeline stage, each producing a migration
   rather than touching the DB — smallest useful unit is the research stage, since R7/R11/R12 are
   already gated there.
2. **Let the gates specify the tools.** `research_batch_dod.py` already states what a complete
   research batch must contain. Those requirements are the spec for the first three emitters.
3. **Do not widen the schema first.** Every table needed already exists, with FKs and Pydantic
   models. This is a tooling gap, not a modelling gap.

## 5. What was *not* concluded

- **No table is proposed for retirement.** The question "are they even required?" has a clean
  negative answer for all eleven.
- **No exemption was added.** The probe will keep reporting 11 until writers exist, which is the
  correct behaviour: it is measuring a real absence, and silencing it would restore the mask the
  baseline removed.
- **The probe's own limit is recorded**, not smoothed over: it detects write *statements*, not write
  *paths*, so it under-reports by at least four tables.
