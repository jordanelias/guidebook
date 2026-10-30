# Render contract: the ramp element, parameters 3 and 12

**Status: DRAFT, unratified.** Written 2026-10-30 by the session `session_2026-10-30-ramp-spec-pages-rebuild`. It is a design document: no renderer, no HTML and no schema change is made here. The owner has not seen it.

**Derive every figure.** Counts and states in this file are not typed; each element names a probe. Run `python3 -I scratchpad/session_2026-10-30-ramp-spec-pages-rebuild/contract_probe.py` (read-only, prints `EXAMINED:`) and read the line for the element id. The probe is a working, not a check; it is registered nowhere.

## 1. What this is, and what it is not

CLAUDE.md names the render stage: *book surfaces, read from the database when rendered; no committed file is one* (2026-08-27). The owner's invariant (the memory note `contract-traceability-invariant`, copied at `owner-rules/`) is that every boundary has a contract that can be verified, and an untraceable hand-off is a defect. HANDOFF.md section 5.6 asks for this document before any HTML: **page element → required data → table.**

This contract takes the page for **a ramp** (term TERM-089) with two sections, **ramp gradient** (parameter 3, TERM-001) and **ramp run length** (parameter 12, TERM-091). Per owner ruling OR-14 (2026-10-29) the page is derived from a typed term pointer to the live determinations of its parameters. It is never a container rows are filed into, and it carries no item code.

It is written to hold **whichever way the owner answers OW-1b** (is the prose templated or written by a model) **and OW-1c** (is the render table stored or rebuilt). Those choices change how an element's text is produced and kept, not which inputs the element needs. Section 5 states the one shape both share.

It is not the page design. Layout, type, colour, grid and the WCAG 2.2 AA tests are in `reports/spec-page-design-requirements-2026-10-29.md` (R1 to R16) and are carried over by reference only. **Accessibility is never self-certified** (owner standing rule); no element below is claimed to meet it.

## 2. Rules every element obeys

- **C1. No value without a pointer.** Every figure on the page carries an `extraction_id` that reaches `evidence_sources` on `ref_id` and a verbatim `claim_text` and a locator. (Probe I1.)
- **C2. The renderer selects and formats; it never composes.** Which value is "the" best-practice value, which cap is the most accommodating, how divergent rows are reconciled, and the spread note are the engine's (workplan T-2 to T-4, owner OR-4, OR-6b). A renderer that computes one writes a second home for a derived fact (CLAUDE.md rules 5 and 8). Where several rows answer one cell, all are listed in a fixed order, with their conditions, and none is chosen.
- **C3. A displayed value has a marker or is not displayed as a determination.** Unmarked is an error (CLAUDE.md section 6). The marker lives on `specifications.marker`. A row read straight from `source_value_extractions` is shown only as a sourced reading, labelled with its source's tier and its own `extraction_status`, never as "best practice".
- **C4. Absence is rendered, not hidden and not invented.** A cell with no live determination prints the gap statement (`v_pending` with its gap). It never prints "Not set" and never fills the cell from a neighbour. The owner's earlier "no Not-set rows" instruction (2026-10-30, requirements report section 12) is kept: such a cell is not a table row; it is named under Gaps.
- **C5. State is shown as stored.** `extraction_status` and the verification of the source print as they are. Under OR-11b a `preliminary` figure may set a published value only flagged; the flag is rendered. Under OR-11a `verified` requires a full-scope scan (probe E11 reports the rows where that does not hold yet).
- **C6. Units are converted by the one function that owns them** (`assess_cell.to_canonical`, `notation_family`), never reimplemented. Per OR-10 an exact linear unit is converted and shown beside the source's own figure, rounded to the nearest quarter inch or 5 mm; the stored value is never altered. A ratio and a percentage convert exactly; degrees do not, so they print rounded beside the source's figure.
- **C7. Every row on the page can be traced back to a retrieval, where one exists.** `retrieval_log.artefacts_for_source(ref_id)`. Where none exists the page says the source was read from a live page and no bytes are held (probe E14).

## 3. The element table

Statuses are those the probe returned on the day of writing (2026-10-30, schema version read from `PRAGMA user_version`); they are not asserted for any later day. **POPULATED** means the inputs exist; it does not mean the element is correct.

| Id | Element (requirement) | Required data → table.column | Selection and ordering | Empty-state rule | Status today and why |
|---|---|---|---|---|---|
| E0 | Page title and one-line definition | `terms.canonical_en`, `terms.definition` for TERM-089, TERM-001, TERM-091; `base_parameters.term_id` | Fixed: element first, then parameters in `parameter_id` order | none; a missing term fails the build | POPULATED |
| E1 | Hero: best-practice value for each parameter, with its marker (R1) | `specifications`: `state`, `value_min`, `value_max`, `value_unit`, `value_notations`, `marker`, `tier_basis`, `code_floor_only`, `rule_version`, `derivation_sha`; view `v_best_practice` (a T6-only cell must appear flagged ○, owner OR-7, so the view's `code_floor_only = 0` filter is to change in T-5) | one live row per (parameter, lens) | print the gap (C4); never print a number | **BLOCKED.** No live determination for either parameter. Needs T-2 to T-4 and the first engine run S-1 |
| E2 | Master comparison table, one row per in-scope jurisdiction (R2) | `source_value_extractions`: `jurisdiction`, `claim_type`, `figure_role`, `comparator`, `claimed_value`, `claimed_unit`, `parameter_id`; `evidence_sources`: `standard_number`, `pub_year`, `edition`, `verification_status`, `tier`, `title` (the standard's name under each row) | jurisdictions alphabetical (owner); within a cell every `claim` row, ordered by `source tier` then `pub_year` descending then `extraction_id`; each row's `condition_on` edges listed as its condition (E12) | a jurisdiction with no claim row is omitted from the table and named under Gaps (E8) | POPULATED for both parameters; coverage is partial, and the probe lists the in-scope jurisdictions with no row for each. **Scope cannot be read from the database** (E2.scope) |
| E2.scope | The jurisdiction list the table is cut to | the owner's scope (US UK AU CA DE NO SE ISO EU; FR CH NL DK FI BE IE ES IT PT; JP SG NZ KR CN) | n/a | n/a | **BLOCKED.** No table holds it; passing a list to the renderer is a curated list (rule 8). `jurisdiction_buckets` is workplan T-6b step 4, and the owner's OR-8 says a bucket member is a jurisdiction with its associated language. Until then the probe carries the list as an input, and says so |
| E3 | Value detail: what the source says, where, and in what state (R2 popup) | `claim_text` (verbatim), `source_section`, `loc_*`, `extraction_status`, `extraction_method`, `figure_role`; source pointer `ref_id` | one detail per extraction | none: a row without text or locator is a defect (I1) | POPULATED; probe reports zero rows without text or locator |
| E4 | Lens controls and the "no evidence" list (R6) | lens columns `identity_code`, `icf_code`, `needs_code`, `medical_code` on the extraction; vocabularies `base_taxonomy_identity`, `base_icf`, `access_needs`, `base_taxonomy_medical` | options = codes present on the parameter's rows, with counts computed; the "no evidence" list = vocabulary codes not present, computed | a lens with no rows is not offered; its codes appear in the no-evidence list | POPULATED, but thin: the probe's E4 line gives rows per lens column and the identity codes in use against the vocabulary; most lens columns carry few or no rows, so the filters can do little today |
| E5 | Unit controls: length and slope (R5) | `claimed_unit` of numerical and range rows; `assess_cell.to_canonical` | per C6 | a row whose unit the converter cannot parse prints as stated with no conversion, and is listed in a build report | **POPULATED WITH DEFECTS.** Parameter 3 rows from earlier batches carry prose in the unit field, so they cannot be parsed. `amend-extraction` cannot change a unit until workplan T-1b step 8, so the repair is a data PR (workplan D-1) after that |
| E6 | Why it matters: short bullets (R9) | extractions with `figure_role = 'finding'`, `claim_text`, `ref_id`; harm and inadequacy findings via `search_executions.harm_finding` | one bullet per finding, ordered by source tier then year; each ends in its citation | the section is omitted; no bullet is invented | POPULATED. The bullet's sentence is the source's `claim_text` or a rewriting of it; which, is OW-1b |
| E7 | Evidence: an APA list, alphabetical by the first author's last name (R8) | `evidence_sources` (`pub_year`, `pub_title`, `journal_name`, `volume`, `issue`, `pages`, `publisher`, `doi`, `url`, `source_type`), `evidence_source_authors` (via `v_evidence_authors.first_author_last`) | alphabetical by `first_author_last`, corporate authors by their name | a source with no author row fails the build | **POPULATED WITH DEFECTS.** `journal_name` is NULL for journal articles because `add-source` cannot set it (GAP-072): an APA entry needs the container. Fixed by a tooling PR, then a data PR |
| E7.cited | "Cited on" under each entry | which sections cite the source: `source_value_extractions.parameter_id` for the source | computed | n/a | POPULATED. On this page the answer is a set of the two parameter sections |
| E8 | Gaps: what the page does not know | (a) derived coverage gaps: in-scope jurisdictions with no row; lens vocabulary codes with no row; (b) recorded gaps: `gaps` reached through `specifications.gap_register_id` and `v_pending` | derived first, recorded second | n/a | (a) POPULATED. (b) **BLOCKED.** `gaps` has no parameter key: a gap reaches a parameter only through a live pending specification, and none is live. GAP-070 and GAP-071 (rise-based spacing, landing dimensions) are prose-only and cannot be selected. A pointer from a gap to a parameter is a schema change, so a tooling PR (proposed, section 7) |
| E9 | The Co-1 statement | `evidence_sources.evidence_type = 'co1'` joined to the parameter's extractions | count and list; prints "no lived-experience evidence recorded for this parameter" only when the count is zero | n/a | POPULATED. Co-1 sources do reach these parameters on main (the probe lists them), so the earlier page's "no Co-1 evidence" statement, true of the old library, is not to be carried over |
| E10 | Study population versus population served | `evidence_population_match`: `match_grade`, `mismatch_note`, `target_population`, `sample_size` | beside each source in E7, one line per target | a source with no match row prints nothing; the build report lists it | POPULATED; the probe lists the count of sources with none (the DoD requires one only for tiers 1 to 3) |
| E11 | State of each reading | `extraction_status`, `source_scans.text_scope`, `source_scans.method` | per C5 | n/a | POPULATED; the probe counts `verified` rows that lack a full-scope reading (OR-11a is unbuilt, T-1 step 10) |
| E12 | Conditions and branches | `extraction_relations` (`relation`, `to_extraction_id`, `quote`) from the parameter's rows | a row's `condition_on` edges print as "applies when" lines pointing at the conditioning row | a claim with no edge prints unconditioned | POPULATED. **The schema cannot say a claim is absolute:** `--relation none` writes no row, so "stated absolutely" and "no condition recorded" read the same (probe I2). C2 forbids the renderer to guess; it prints unconditioned in both cases |
| E13 | Audience lens: designer, disabled person, OT, policymaker | none | none | n/a | **BLOCKED.** `weighting_profile` holds tier weights by audience and use pattern for synthesis and is read by no script. No table says what each audience sees first or which sections open, so an audience lens has no data to render from. The owner confirmed on 2026-10-30 that two lenses exist and only the disability lens was built; the audience lens needs a data home before it has a contract |
| E14 | Provenance footer | `PRAGMA user_version`; the sha256 of the database file; `retrieval_log.artefacts_for_source`; `specifications.rule_version` | one block | n/a | POPULATED |
| E15 | Evidence marker (●/◐/○) with its words (R1, doctrine) | `specifications.marker` | beside each E1 value | none printed; see C3 | **BLOCKED** with E1 |
| E16 | Navigation, controls order, type, colour, grid, accessibility | none from the database | n/a | n/a | Out of this contract. Requirements R10 to R16 and section 6a of the requirements report govern; the page is not shown to the owner until its own tests pass |

## 4. Invariants the build is to verify

Each is stated so a check could be written; **none is a registered check** (CLAUDE.md section 8: nothing is added without naming what reads it, so a check waits for the renderer that would be its reader).

- **I1.** Every numerical row printed has `extraction_id`, `ref_id`, `claim_text` and a locator. (Probe I1.)
- **I2.** A claim row printed unconditioned has no `condition_on` edge. (Probe I2 reports the count; the schema cannot separate absolute from unrecorded.)
- **I3.** No figure on the page is produced by the renderer. Review, not a check.
- **I4.** Every displayed state is one of `stated`, `provisional`, `pending`, `not_applicable`; none is displayed without a live determination.
- **I5.** Each source printed has at least one author row and a year (probe E7).
- **I6.** The page's input set is hashed and the hash printed in the footer, so a change in any input row is detectable (OW-1c says this is needed if the table is stored; it costs nothing if rebuilt).

## 5. The render record, in the shape both OW-1b and OW-1c share

Owner OW-1 (2026-10-29) says the render stage holds the specification rows converted to complete prose, with bibliographic text drawn from the preceding tables, so the site can show it as it stands. Whatever the answers to OW-1b and OW-1c, an element needs this record, whether it is stored or produced at build time:

| Field | Holds | Why |
|---|---|---|
| `element_id` | E-number from section 3 | what the record is |
| `page_term_id` | TERM-089 | the page it belongs to (OR-14) |
| `parameter_id` | 3 or 12, NULL for E0 | the section |
| `lens_key` | the lens codes of the row, or NULL | the cell |
| `position` | integer | the fixed order |
| `specification_id` | NULL when the element is a gap statement | the pointer (rule 5: point, do not copy) |
| `text` | the prose | what the site shows |
| `text_form` | `template` or `model` | OW-1b |
| `inputs` | list of (table, key) the text was built from | traceability |
| `inputs_sha256` | hash of those rows' values | staleness (OW-1c, I6) |
| `rule_version` | the engine's | the same label the determination carries |

This is a proposal for the owner and is not a schema: a table with these columns is workplan T-5's, and T-5 waits on OW-1b, OW-1c and T-2 to T-4. If OW-1c is "rebuilt", the record is the build's in-memory form and nothing is stored.

## 6. What the held data can and cannot fill

- **"Preferred" and "Maximum" columns have no structural source.** The old page had a column for each. The schema has `comparator` (`<=`, `>=`, `=`, ...) and `figure_role` (claim, finding, condition, derived), and nothing marks a figure as preferred. The Irish "preferred maximum 1:20, relaxed to 1:12 for flights not above 2000 mm" and the UK Table 1 are conditions; they are held as `condition_on` rows for the tiers, and, for the Irish preferred maximum, still as prose in row 81's unit (an E5 defect). This contract therefore replaces the two columns with **Limit** (one line per claim row) and **Applies when** (its condition edges). If the owner wants a "preferred" column, it needs a typed field, which is a schema change. [ASSUMPTION: the owner's "preferred / maximum" wording was the earlier page's, not a ruling.]
- **"Between landings" is parameter 12**, and is filled for only some of the in-scope jurisdictions (probe E2.p12 lists which and which not).
- **The old page's other columns are not parameters 3 or 12:** landing size, clear width, handrails, cross-slope. Landing dimensions are TERM-092, not minted (GAP-071); the others have no parameter. They are outside this contract.
- **The old staged data** (`data/E-03.json`, the hand-typed jurisdiction readings): probe X1 compares its jurisdiction list with what is held. The readings were hand-typed from sources that mostly have extractions now; they are not to be loaded, only superseded.
- **Recorded gaps cannot be selected by parameter** until a gap points at a parameter (E8). Until then the page's Gaps section is the derived list.

## 7. Order of work and what blocks it

| Step | Does | Needs | Can start now? |
|---|---|---|---|
| a | Owner answers OW-1b, OW-1c, and whether the audience lens is wanted | the owner | yes |
| b | Mint `jurisdiction_buckets` so scope is data (T-6b step 4) | OR-8 (answered) | yes, tooling PR |
| c | A pointer from `gaps` to a parameter; a writer for journal and publisher; a way to say a claim is absolute | owner view on c1 and c3 | tooling PRs, each small |
| d | Repair parameter 3 rows whose unit carries prose (workplan D-1) | T-1b step 8 if OR-3 yes | after T-1b |
| e | Engine T-2 to T-4, then T-5 view change and the render record | OW-1b, OW-1c | after (a) |
| f | First engine run over parameters 3 and 12 (S-1) | e, D-1, D-3 | after (e) |
| g | The page itself, against requirements R1 to R16 | e, f | last |

Until (e) and (f), the only honest page for this element is the evidence list with its sourced rows and the Gaps section: no hero, no marker, no best-practice language. That follows from C2 to C4 and is not a limitation of this contract.

## 8. Questions for the owner

Each changes the contract; none is a restatement of an answered ruling.

1. **Preferred versus maximum.** Is a "preferred" figure a thing the data should carry, as a typed field, or is Limit plus Applies-when enough?
2. **Absolute versus unrecorded.** Should the schema record that a claim is stated absolutely (so an unconditioned row means something)?
3. **A pointer from a gap to a parameter.** Is the missing key worth a schema change so a page can list its own recorded gaps?
4. **Audience lens.** Is it wanted on this page, and where is the data for it to live? (E13.)
5. **OW-1b and OW-1c**, already open in the browser page.

## 9. Sources this contract rests on

CLAUDE.md sections 3, 6, 7a, 8; `governance/pipeline-contract.yaml` stage `render`; `workplan/2026-10-23-pipeline-resolution-workplan.md` section 5 (T-5, T-7, D-1, D-3), section 4 (OR and OW rows); `references/project-standards.md`, "Owner rulings 2026-10-29" (second and third entries: OR-4, OR-6b, OR-7, OR-8, OR-10, OR-11a, OR-11b, OR-14, OR-20, OW-1); `governance/owner-browser.yaml` (OW-1b, OW-1c); `reports/spec-page-design-requirements-2026-10-29.md` (R1 to R16 and sections 10 to 12); `owner-rules/contract-traceability-invariant.md`.
