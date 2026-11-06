# Base matrix: minimal schema and load path (DESIGN, 2026-11-06)

Approves nothing. Governing: `references/project-standards.md` 2026-11-06 entries (minimum correct code / one
value per cell; fifth, log the URL; sixth, equivalence classes; seventh, the base grounds itself and the
acceptance test is confirmed coverage; eighth, English labels allowed, no English bias), OR-17/E4, CLAUDE.md
rules 3, 4, 5, 7a, 8, 10, §4 and §8. Draft SQL: `draft_126_base_matrix.sql` beside this file, applied only to
a throwaway copy of the DB (FK check clean; four constraint probes refused or admitted as intended).

## 1. Verdict

Add three base tables: `base_sources` (one row per URL), `term_forms` (one row per occurrence of a form, with
its language, usage, page/line/clause and short quote, or a flagged seed with no source), and
`base_form_searches` (concept looked for in a source), plus two column pairs on `terms` (`kind`;
`split_of_term_id` + `discriminating_test`) and drop the 0-row `term_aliases.observation_id`. Coverage is a
derived view, `v_base_matrix` (every term x every `lang_jur_map` column, four cell states), and it is the
acceptance test. Nothing in the base points into evidence; evidence keeps `observe-term` / `adjudicate-term`,
whose adjudications already point the right way (evidence -> base).

## 2. Options compared

| | (A) extend `term_aliases` | **(B) new matrix tables** (recommended) | (C) pointer route, admit sources |
|---|---|---|---|
| Status | possible | recommended | **OUT** (seventh entry: "none of the work in base needs to be verified and stored in evidence") |
| Columns added | ~10 on `term_aliases` | 3 tables (14+17+4 cols, draft), 3 cols on `terms` | 0 |
| Tables touched | `term_aliases` (PK rebuild) | new tables; `terms` (ADD COLUMN); `term_aliases` (DROP COLUMN) | `evidence_sources`, `observed_terms`, `term_adjudications` |
| Reads it | `db.py`, `alias_provenance_audit`, query generation | `v_base_matrix`, `v_base_lookup`, `v_base_forms_unmapped`, `v_term_label_basis`, the new writer | as today |
| Wrong thing reaching the guidebook without it | a form found in two sources or jurisdictions cannot be held, so one is silently dropped | research searches one language and calls the concept covered | n/a |
| Migration size | table rebuild of a 2,382-row table + data move | 3 CREATE TABLE, 4 ADD/DROP COLUMN, 4 views | ~270 source admissions |
| Effect on 2,382 aliases | mixed in with attested rows; seeds and findings share one table and one `notes` cell | untouched; reachable through `v_base_lookup` as `legacy alias` | untouched |
| Effect on `observation_id` | kept, inverted pointer stays | dropped (0 rows) | is the route |

Why not A: the PK `(term_id, alias, language)` has no jurisdiction or source, so the TSVs' own occurrences
collide. Derive: the 64 below is `sum(n-1)` over `(concept_id, form, language)` groups in the 14
`terminology-pass/*/equivalents.tsv` files (`python3` one-liner; re-run, do not trust). A also mixes 996
`TRANSLATION` rows (`SELECT alias_type,COUNT(*) FROM term_aliases GROUP BY 1`), which R11 forbids for
sources, into the attested set, and `term_aliases.notes` is already a census candidate (`python3
scripts/audit/joined_cells_census.py | grep term_aliases.notes`).

Schema shape (§4). The TSVs join cells that B splits: `source` = "title | issuer | URL" -> `base_sources`
(`title_as_written`, `issuing_body`, `url`, `archive_url`); `jurisdiction` = "FR (national DPO)", "DE-BY",
"FR (commune de Loisin)" -> `jurisdiction` + `subdivision` (ISO 3166-2) + `source_class` + `issuing_body`;
`language` = "no (Bokmål)" -> `language` + `variety`; `locator` = "art. 3; text line 308 of 43802a8ee631.txt"
-> `clause` + `line` (+ `retrieved_sha256` on the source); `attestation_tier` 1-5 is a property of the
source, so it is `base_sources.source_class` (CHECK), not a form column. Vocabularies are the CHECKs in the
draft, read by `dbcore.check_values()`; no list in code. The URL has one home per source (distinct source
strings: 269 by the same one-liner, against 1,072 rows carrying it today). `quote` earns its column: the
file is not committed (fifth entry), so the quote is the only way a reader re-finds the occurrence and judges
its sense per occurrence (sixth entry, item 5), and the CHECK `instr(quote, form) > 0` tests it.

## 3. The concept side (redone on the eighth entry)

`terms.canonical_en` is OUR label, English allowed, never a form. A concept first met in Japanese gets an
English descriptive label; its instrument phrase is a `term_forms` row (language JA, source, clause). No EN
form is attached until an English-jurisdiction source uses one. Nothing new is typed for this:

| Fact | Where | Why no column |
|---|---|---|
| label basis (instrument term vs descriptive) | `v_term_label_basis`, derived: an attested form of the concept has the label's exact text | rule 8: the machine can compute it; a typed value could only be right or wrong |
| origin language and phrase | the concept's earliest attested `term_forms` row, same view | a pair on `terms` would be the second home of a form (rule 5) |
| kind | `terms.kind`, CHECK of the eight register kinds, NULL for the 94 held terms | not derivable; `domain` is topical (`SELECT domain,COUNT(*) FROM terms GROUP BY 1`) |

Effect on the 94 terms (`SELECT COUNT(*) FROM terms`): none written; all derive `descriptive` until forms
load (measured on the throwaway copy). Readers of `canonical_en`: `grep -c canonical_en scripts/db.py`
(71 today) plus `git grep -l canonical_en -- scripts ':!scripts/migrations'` (audit/research_batch_dod,
audit/scan_debt, validate_parameters, four tests) and the six views `SELECT name FROM sqlite_master WHERE
type='view' AND sql LIKE '% terms %'`; all keep working because the column keeps its meaning (a display
label) and stays NOT NULL (`grep -l canonical_en scripts/migrations/data_*` lists six INSERTing files).
Rejected: relaxing NOT NULL (table rebuild under six views and 71 readers for no gain once English labels are
allowed); `origin_language`/`origin_phrase` on `terms` (a copied form). The register's `origin_*` columns
become the first form row at load.

English bias: `v_base_matrix` reads only `term_forms`, never `canonical_en`, so an English label yields no EN
cell; keys contain no language preference; no view orders or filters on EN.

## 4. Keys and uniqueness

- **Cell** = (term_id, language, jurisdiction), a GROUP BY over `term_forms` JOIN `base_sources`; never
  stored. **Occurrence key** = `ux_term_forms_occurrence` (term, form, language, variety, source, clause,
  page, line): the same form in two sources is two rows, and counts once in the cell (`COUNT(DISTINCT form)`).
- **Language** is `lang_jur_map`'s code (FR, NO, ZH); **variety** is its own column (nb, nn, Hans, Hant),
  no CHECK, so Bokmål and Simplified/Traditional need no schema change. `base_sources (language,
  jurisdiction)` is a composite FK to `lang_jur_map`; a form in another language than its source (an English
  term in a Japanese standard) is caught by `v_base_forms_unmapped`, which must be empty or the pair declared.
  Arabic/Bengali/Hindi/Swahili are already map rows (`SELECT DISTINCT language FROM lang_jur_map`); admitting
  them is a `scope_status` value, not a schema change. Case mismatch: `term_aliases.language` is lower case,
  the map upper (`SELECT DISTINCT language FROM term_aliases`); the new tables follow the map.
- **Adopting instrument** (Land, comunidad autónoma, CN-BJ): `base_sources.subdivision`; the matrix column
  stays the national jurisdiction. A commune or a DPO is `issuing_body` / `source_class`, not a jurisdiction.
- **Equivalence class** = the term itself; its forms are its members. No class table.
- **Sense split** = a child term with `split_of_term_id` and `discriminating_test` (CHECK: both or neither);
  the child's forms are its own rows, never repeated on the parent. `sense_splits.tsv` names parents by label
  (`cut -f2 register-v2/sense_splits.tsv | sort -u | wc -l`); each must resolve to a term at load or wait.
- **Conflation** = `conflation_note` on the occurrence, optionally `conflates_term_id`; recorded, not resolved.
- **Seed** (OR-17/E4) = `source_id` NULL and `seed_origin` in ('owner-supplied','model'); CHECKs forbid a
  seed a locator or quote and forbid an attested row without `page` or `clause`.

## 5. Coverage is the acceptance test; load path

**(a) The view.** `v_base_matrix`: every term x every `lang_jur_map` row, `cell_state` in HAS-FORM /
SEARCHED-NONE-FOUND / NOT-SEARCHED / OUT-OF-SCOPE, plus `n_forms` and `n_sources_read`. Owed columns come from
the existing `v_research_scope` (one home of scope). English is split by jurisdiction because it is
language x jurisdiction like every other column. EXAMINED: `SELECT COUNT(*), COUNT(DISTINCT term_id) FROM
v_base_matrix`; per state: `SELECT cell_state, COUNT(*) FROM v_base_matrix GROUP BY 1`. On today's DB copy it
prints 6,580 NOT-SEARCHED (94 terms x 70 map rows; re-derive). Seeds are not HAS-FORM.

**What the view says today, and why it would have said so.** `SELECT COUNT(*) FROM v_research_scope` is 70:
`lang_jur_map.scope_status` is unfilled (`SELECT COUNT(scope_status) FROM lang_jur_map`), so the view owes all
70 pairs, not the session's 20 columns. [GAP] The P1+P2+P3 fill of `scope_status` is a data migration and an
owner decision (D4). The coordinator's throwaway baseline (560 concepts x 20 columns, 314 of 11,200 cells with
a form, 477 concepts with none) is what the view prints after load once scope is filled; re-derive it with the
view, not from this line. [GAP] SEARCHED-NONE-FOUND has thin input: the passes' `coverage.tsv` holds
SEARCHED-ABSENT keyed by first-pass labels, not `concept_id` (`cut -f3 terminology-pass/*/coverage.tsv | sort |
uniq -c`), so most cells will load as NOT-SEARCHED, which is the truthful state.

**(b) Gap query** (research targets):
`SELECT language, jurisdiction, COUNT(*) AS gaps, group_concat(term_id) FROM v_base_matrix WHERE cell_state =
'NOT-SEARCHED' GROUP BY 1,2 ORDER BY gaps DESC;` (one row per column; a column with no gaps is absent).

**(c) Invariants that prove it works**, each a query that must return 0 rows:
1. Unmapped form: `SELECT * FROM v_base_forms_unmapped`.
2. Unsourced non-seed: enforced by CHECK `(source_id IS NULL) = (seed_origin IS NOT NULL)`; seeds counted by
   `SELECT seed_origin, COUNT(*) FROM term_forms WHERE source_id IS NULL GROUP BY 1`.
3. English label read as English coverage: `SELECT * FROM v_base_matrix m JOIN v_term_label_basis b USING
   (term_id) WHERE m.language='EN' AND m.cell_state='HAS-FORM' AND NOT EXISTS (SELECT 1 FROM term_forms f JOIN
   base_sources s USING(source_id) WHERE f.term_id=m.term_id AND f.language='EN' AND s.jurisdiction=m.jurisdiction)`
   (structurally 0, since the view never reads the label; kept as the regression test).
4. Double count: `SELECT term_id, language, jurisdiction, COUNT(*) FROM v_base_matrix GROUP BY 1,2,3 HAVING
   COUNT(*) > 1`; a split child and its parent are distinct terms, so each holds its own cells.
5. Quote not containing form: CHECK `instr(quote, form) > 0`.

**(d) Stopping rule ("proper coverage"), derived.** A column is saturated when a full round (every
NOT-SEARCHED or SEARCHED-NONE-FOUND term in that column put to at least one new source of each
`source_class` the column has used) adds no `term_forms` row. Derivable: the round is the set of
`base_form_searches` rows created by one session; saturation is `NOT EXISTS (term_forms created_by_session =
that session in that column)`. Proper coverage = every owed column saturated and every cell HAS-FORM or
SEARCHED-NONE-FOUND. No hand-set percentage.

**Load path.** Rule 10: **PR 1 tooling** (migration 126, the writer, its tests, registry note) merges first;
**PR 2 research** (rows) after. Existing verbs cannot reach the new tables (`add-alias` needs an observation;
`add-term` needs an observation or a catalogue entry), so the smallest writer is one module in `db.py`:
- `add-base-source` (url, title, language, jurisdiction, class...): refuses a pair not in `lang_jur_map`, a
  duplicate URL, a class outside the CHECK.
- `add-form` (term, form, language, usage, source + page/clause/line/quote, or `--seed owner-supplied|model`):
  refuses an unknown term or source, a vocabulary value outside its CHECK, an attested row with no locator, a
  quote not containing the form, a seed with a locator, a duplicate occurrence; reports other terms already
  holding the same form (conflation surfaced, not resolved).
- `add-form-search` (term, source): the NONE-FOUND record.
- `add-term --descriptive-label ... --kind ... --first-form <add-form args>`: a third warrant route that mints
  the term and its first attested form in one act (as `insert_term` pairs term with adjudication), so no term
  exists without a form or a recorded owner approval.
A scratchpad driver (not committed tooling) reads the TSVs and calls those functions against a scratch DB
copy; `emit_batch_sql.py` -> `emit_data_migration.py` -> `migrate_db.py`. Quotes and URLs are checked without
committing files: the CHECK tests quote-contains-form; `retrieved_sha256` lets anyone refetch the URL and
compare; a sampled `retrieval_log.fetch()` re-retrieval in the research PR's adversarial pass checks the rest.
The 9 `NOT-IN-REGISTER` rows (`grep -c NOT-IN-REGISTER terminology-pass/*/equivalents.tsv`) wait for a term.

Checks that read the new columns, from `governance/check-registry.yaml` (none invented):
`jurisdiction_db_vocabulary` (derives every table with a `jurisdiction` column: covers `base_sources`),
`column_vocabulary_audit`, `schema_reference_audit`, `migration_reproducibility` (+ `_deep`, advisory: counts
alone miss an UPDATE), `identifier_floor_audit` [GAP: whether it reads `term_id` minting], and
`alias_provenance_audit` (reader of `observation_id`; must be edited in PR 1, rule 4). The coverage invariants
in (c) are queries; registering them as one check is decision D5. `joined_cells_census.py`: run before (EXAMINED
457 columns, 66 candidates, today) and after on the copy (unchanged: empty tables have no data to examine, so
the "after" run is only meaningful on PR 2's loaded copy).

## 6. `observation_id` and the observed_terms route

The phrase-in-context quote for **evidence** stays in `observed_terms` (scan contract, 2026-10-09 item 1:
every admitted source is read for every parameter; the quote is what judgment adjudicates). The **base** has
its own `term_forms.quote`. Those are two different facts (a base sighting; an evidence reading), not a copy.

| Object | Verdict | Reason |
|---|---|---|
| `observe-term`, `adjudicate-term` | keep, evidence only | the scan contract; adjudication NAMES-EXISTING is already the evidence -> base pointer |
| `term_aliases.observation_id` | **drop** | inverted pointer; 0 rows (`SELECT COUNT(observation_id) FROM term_aliases`); no data migration writes it |
| `add-alias` | **retire** | it copies what the adjudication already says into a base table; its only callers are `db.py`, `test_scan_contract.py` AL01-AL0n, and `alias_provenance_audit`'s SOURCE-ATTESTED class (`git grep -n add_alias -- scripts`) |
| `rename-term` DEPRECATED alias | keep | a former label is a fact about our label, not a form |
| `term_aliases` 2,382 rows | keep, frozen | data migrations INSERT it (`grep -l term_aliases scripts/migrations/data_* \| wc -l`), so rule 5 forbids dropping; reached as `legacy alias` in `v_base_lookup` |
| `insert_term --from-observation` | keep | evidence-met concepts still mint from an observation |

Smaller fallback if the owner prefers: leave `observation_id` and `add-alias` in place, unused by the base
(zero code), and accept the inverted pointer as dead weight.

## 7. Owner decisions (recommended option first)

Blocking PR 1 (tooling):
1. **D1 Option B** (three tables). Else A: PK rebuild, and same-form-two-sources occurrences are lost.
2. **D2 Drop `observation_id`, retire `add-alias`.** Else leave both unused: no code, a dead pointer stays.
3. **D3 Label basis derived** (no column). Else a typed `label_basis` CHECK column: one more field that can be
   wrong.
4. **D4 Ratify the eight `kind` values as a CHECK.** Else no `kind` column; kind stays in the scratchpad.

Blocking PR 2 (rows), not PR 1:
5. **D5 Fill `lang_jur_map.scope_status` for P1+P2+P3** (data migration). Else the view owes all 70 pairs and
   coverage can never be confirmed.
6. **D6 Register the five invariants as one blocking check.** Else they are queries the adversarial pass runs.
7. **D7 Load `coverage.tsv` SEARCHED-ABSENT rows only where they map to a concept_id.** Else they are dropped
   and those cells read NOT-SEARCHED.
8. **D8 Model seeds load as `seed_origin='model'`** (21 `unattested seed` rows). Else they stay out of the base.

## 8. Self-attack

| # | Failure | Detector |
|---|---|---|
| 1 | A form typed from memory is given a real URL it does not appear in; CHECKs pass | quote-contains-form CHECK only tests the row against itself; the detector is the PR 2 adversarial re-fetch of a sample by `retrieval_log.fetch()` and `--verify`-style diff; no gate reads the URL bytes [GAP] |
| 2 | Scope unfilled, so "complete" is unreachable, or filled wrongly so it is reached falsely | `SELECT COUNT(*) FROM v_research_scope` against the ratified P1+P2+P3 list in the ledger; the 2026-11-06 R2-1 precedent in `db.py` |
| 3 | A form in a language other than its source's falls out of every column | `v_base_forms_unmapped` must be empty (invariant 1) |
| 4 | The derived label basis calls a descriptive label an instrument term because the strings coincide | then it IS that instrument's term; review `SELECT * FROM v_term_label_basis WHERE label_basis='instrument term'` at PR 2 |
| 5 | Saturation declared after a lazy round that read one source per column | the stopping rule requires each used `source_class`; `SELECT jurisdiction, source_class, COUNT(*) FROM base_sources GROUP BY 1,2` in the PR 2 record |
| 6 | `v_base_lookup` lets research treat legacy TRANSLATION aliases as found forms | `standing` column; `alias_provenance_audit` still classifies them |
