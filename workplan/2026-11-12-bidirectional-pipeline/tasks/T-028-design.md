# T-028 design — a concept is its id; its names are forms; `canonical_en` is our label

_Written 2026-11-12 by an Opus-class designer under the owner's instruction "Opus to write design files that must be written first", on the delegated resolution of OD-03. Plan document: it changes no script, schema, row or ruling. Every count is given as the command that produces it; re-run it. SQL marked **sketch** is a shape, not a file to paste unread. Canadian English._

_Revised 2026-11-13, after the T-028 pilot (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-028-report.md`) and the fold of T-026: no pointer reaches `term_aliases` by `rowid` (SQLite cannot declare a foreign key on one and `emit_batch_sql.py` does not carry implicit rowids), so T-026's junction is keyed and T-028 remaps it by key to `form_id`; `attestation` keeps T-026's `DEFAULT`; the judge, reason and former label of every label set by judgment get one typed home, `term_label_picks`, which also holds the base route's rationale; the refusals of `rename-term` and `mint-term-from-catalogue` are kept, and one cross-language question is left to the owner; `label_is_instrument_term` is renamed `label_is_attested_form`. Where the 2026-11-12 text and this revision differ, the revision governs._

## 0. Verdict

**The one table that holds a form is `term_aliases`.** No new forms table is built. T-026 puts the attestation and locator columns on it (names fixed in section 4 so the two tasks agree). T-028 then rebuilds it to one row per **occurrence**, keyed by a new `form_id` (equal to each existing row's `rowid`), with a unique occurrence index in place of today's primary key `(term_id, alias, language)`, and adds `usage_type`. In the same migration it remaps T-026's search-to-form junction from the old key to `form_id`, by key, and adds `term_label_picks`, the one home of the judge, the reason and the former label of a label set by judgment (OD-38). A concept's identity stays `terms.term_id`; its equivalence class is its member rows in `term_aliases`. **`terms.canonical_en` stays `TEXT NOT NULL`, as our English descriptive label: never written as a form, never matched against forms, never read first.** Whether the label is also an instrument's term, and the name shown (E1), are derived by one view, `v_term_names`; the only stored choice is the label itself, changed by `rename-term` with its warrant. Five writers change: the two name screens (`_name_holder`, `_near_terms`) become per-language and attestation-aware; `add-term` gains a base route that mints a concept with its first attested form and stops forcing a non-English concept's label to sit inside the source's phrase (the defect AT-25 exposes); `rename-term` stops writing our former label as a form or as a `scope_note` trailer and gains `--from-form`, every route naming its judge; `add-alias` refuses the legacy relation values and records an occurrence, not a key.

**Confidence.** Medium-high (about 75%) that `term_aliases` is the right single home: the alternative (`term_forms`, the 2026-11-06 matrix design) leaves 2382 baseline rows in a second table that can never be emptied (section 2). Medium (about 60%) on the display rule's tie-break (section 7, rule 2), which is deterministic but arbitrary when several English instruments use different forms.

**Owner's call.** None is outstanding: OD-03 is resolved under delegation (`grep -F "OD-03 STATUS:" references/project-standards.md | tail -1`; its check is `not required`), reversible by the owner. The points at which the owner may disagree are listed in section 15; the one most likely to matter is the tie-break of section 7.

## 1. What the rulings require

| Ruling (find it with) | Requirement | Met by |
|---|---|---|
| OD-03 (delegated), `grep -n -F 'OD-03: forms table' references/project-standards.md` | identity is the neutral id; names are rows of one forms table, one row per occurrence with language, jurisdiction, source; `canonical_en` our label, never a form; label basis derived; display by E1; a stored choice only where no derivation decides | sections 3, 6, 7 |
| Sixth statement 2026-11-06, `grep -n -F 'a concept is an equivalence class of forms' references/project-standards.md` | equivalence class; usage type and attestation per form; disfavoured forms kept; conflation recorded per occurrence, not resolved | member rows; `usage_type`; T-026's `attestation`; conflation derived (section 5) |
| Seventh statement 2026-11-06, `grep -n -F 'base grounds itself' references/project-standards.md` | a base form carries its own source columns (URL, page, line), not an `evidence_sources` row | T-026's locator columns; `add-term` base route (section 8) |
| Eighth statement 2026-11-06, `grep -n -F 'English labels are allowed on non-English-origin concepts' references/project-standards.md` | an English label allowed, marked as ours; the instrument's phrase kept as a form; no English form until an English-jurisdiction source uses one; no column read, matched or ranked first | `canonical_en` as label; `v_term_names.label_is_instrument_term`; screens per language (section 8) |
| E1 and E4, `grep -n -E '^\| E1 |^\| E4 ' references/project-standards.md` | E1: named by the instrument's own phrase until an English-language instrument of a P1+P2+P3 jurisdiction names it. E4: model-generated and unrecorded aliases stay as flagged search aids, never vocabulary, never deleted | `v_term_names` rules (section 7); screens read attested forms only (section 8) |
| CLAUDE.md rule 5 and the 2026-11-06 schema-shape statement | one home per fact; one value per cell | one forms table; `usage_type` and `attestation` in their own cells; legacy `alias_type` values frozen (section 5) |

## 2. Why `term_aliases`, not a new `term_forms`

- **One home.** `term_aliases` already holds every name the base has (`select count(*) from term_aliases`). Its rows were inserted by the 057 baseline (`grep -c 'INSERT INTO "term_aliases"' scripts/migrations/057_baseline_2026-08-12.sql`), and the 2026-09-16 ruling retires data rows in place, never deleting them. A new `term_forms` beside it leaves those rows where they are forever: either copied (two homes) or reached through a union view (the matrix design's `v_base_lookup`), which is two homes joined at read time.
- **The matrix design's two objections are answered in place.** (i) "The PK has no jurisdiction or source": the rebuild replaces the PK by a surrogate key and an occurrence index that includes jurisdiction and locator (section 3). (ii) "It mixes model seeds with attested forms": T-026's typed `attestation` separates them in a cell, and every vocabulary read filters on it (section 8).
- **The name stays.** Renaming the table would make every caller a sweep item (`git grep -l -F term_aliases -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'` and the prose `git grep` of the task file) for a legibility gain only; a row of `term_aliases` is documented as "a form of the concept, or a related search string" (section 5).

## 3. The table after T-026 and T-028 (sketch)

```sql
-- sketch: term_aliases after T-028's rebuild. Columns marked (T-026) are added by T-026 first.
CREATE TABLE term_aliases (
    form_id             INTEGER PRIMARY KEY AUTOINCREMENT,   -- = the old rowid (pointers made by rowid still resolve)
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    alias               TEXT NOT NULL,                       -- the form, verbatim
    language            TEXT NOT NULL DEFAULT 'EN',
    alias_type          TEXT NOT NULL CHECK (alias_type IN
                            ('SYNONYM','TRANSLATION','NARROWER','BROADER','DEPRECATED','DOMAIN')),  -- unchanged; section 5
    jurisdiction        TEXT,
    notes               TEXT,
    observation_id      INTEGER REFERENCES observed_terms(observation_id),
    attestation         TEXT NOT NULL CHECK (attestation IN
                            ('instrument','other_source','owner_supplied','model_seed','unrecorded')),  -- (T-026)
    source_url          TEXT CHECK (source_url IS NULL OR source_url GLOB 'http*://*'),             -- (T-026)
    source_page         TEXT,                                                                       -- (T-026)
    source_line         INTEGER CHECK (source_line IS NULL OR source_line > 0),                    -- (T-026)
    source_clause       TEXT,                                                                       -- (T-026)
    usage_type          TEXT CHECK (usage_type IS NULL OR usage_type IN
                            ('code_term','colloquial','regional_variant','outdated_or_disfavoured','product_name')),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    -- (T-026) an attested occurrence says where; a seed says nowhere.
    CHECK (attestation NOT IN ('instrument','other_source')
           OR observation_id IS NOT NULL
           OR (source_url IS NOT NULL AND (source_page IS NOT NULL OR source_clause IS NOT NULL))),
    CHECK (attestation IN ('instrument','other_source')
           OR (source_url IS NULL AND source_page IS NULL AND source_line IS NULL AND source_clause IS NULL))
);
-- One row per OCCURRENCE: the same form in two sources or jurisdictions is two rows.
CREATE UNIQUE INDEX ux_term_aliases_occurrence ON term_aliases
    (term_id, alias, language, COALESCE(jurisdiction, ''), COALESCE(observation_id, 0),
     COALESCE(source_url, ''), COALESCE(source_clause, ''), COALESCE(source_page, ''),
     COALESCE(source_line, 0));
CREATE INDEX idx_ta_alias    ON term_aliases(alias);      -- recreated (exists today)
CREATE INDEX idx_ta_language ON term_aliases(language);   -- recreated (exists today)
```

`usage_type` is nullable: NULL means "not yet typed", which is the truth for every existing row; it is typed by judgment when a row is next touched (T-107), never guessed by the migration. The five values are the sixth statement's list, in the column's own CHECK (read by `dbcore.check_values`, never retyped).

## 4. What T-026 builds on this table (names fixed here; T-026 executes them)

- `attestation TEXT NOT NULL` with the five-value CHECK above (the sixth statement's four kinds plus `unrecorded`): `instrument` (a code, standard or statute uses the form), `other_source` (any other source uses it: signage manual, public-body or advocacy guidance, a study, a glossary), `owner_supplied` (a seed the owner gave), `model_seed` (a model generated it), `unrecorded` (no provenance). `instrument` and `other_source` are attestations; the other three are seeds or unknowns and are **search aids only** (E4).
- `source_url`, `source_page`, `source_line`, `source_clause`, and the two CHECKs of section 3.
- **Mechanical fill**, from what the row already says, with no judgment: `observation_id` set → `other_source` (an admitted source used the phrase; whether it is an instrument is a judgment left to T-107); notes carrying a `VERIFIED-GLOSSARY` or `VERIFIED-CROSS` marker → `other_source`; `model-generated` → `model_seed`; anything else, including `curated`, `repo shorthand`, `VERIFIED-NATIVE` and NULL notes → `unrecorded`. The markers are the ones `classify()` in `scripts/audit/alias_provenance_audit.py` reads; reuse that function's precedence. (The other_source rows carry no URL, so the first CHECK admits them through `observation_id` or, for the glossary markers, not at all: if `select count(*) from term_aliases where notes like '%VERIFIED-GLOSSARY%' or notes like '%VERIFIED-CROSS%'` is not 0 at execution, those rows go to `unrecorded` and are listed in T-026's pull request for T-107 to re-attest with a locator.)
- `add-alias` gains the base route of the seventh statement: `--source-url --source-page --source-line --source-clause --attestation instrument|other_source` as an alternative to `--observation-id`, and `--seed owner_supplied|model_seed` for a flagged seed with no locator.
- The search-forms junction (T-026 item 1) points at `term_aliases.form_id` once T-028 has run; until then at `rowid`, which T-028 preserves as `form_id`.

**Why the occurrence grain is T-028's and not T-026's:** T-026 adds columns by `ALTER TABLE` and needs no rebuild; the grain needs one. Until T-028 merges, a second occurrence of a form a term already holds in that language cannot be stored, so **T-107 (attest forms) now waits for T-028** (its task file is corrected in the same pass).

## 5. Membership, the legacy `alias_type` values, and conflation

- **Members of the equivalence class** are the rows whose `alias_type` is not `NARROWER` or `BROADER`. A `NARROWER` or `BROADER` row is a related search string, not a name of the concept: it is never shown as a name, never counted as a form, never matched as a name. (Term-to-term relations are T-029's table; these strings name no term.)
- **`TRANSLATION`, `DEPRECATED`, `DOMAIN` are legacy values.** Each joins a relation with another fact (a seed's origin; a usage; a domain variant). After T-026 and T-028 those facts have typed homes (`attestation`, `usage_type`). The existing rows are **not rewritten** (`DOMAIN` cannot be mapped to a usage without judgment: `select alias, language, notes from term_aliases where alias_type='DOMAIN'`); no writer writes these three values again; no reader infers attestation or usage from them. `add-alias` already refuses `TRANSLATION` and `DEPRECATED`; it now refuses `DOMAIN` too, naming `--usage-type`. `rename-term` stops writing `DEPRECATED` (section 8).
- **Conflation is derived, not stored:** a form held as a member by two concepts in one language is a conflation. Query: `select upper(language), alias, group_concat(distinct term_id) from term_aliases where alias_type not in ('NARROWER','BROADER') group by 1, 2 having count(distinct term_id) > 1`. Writers report it and do not refuse it when the operator names the other concept with `--distinct-from` (section 8).

## 6. `canonical_en`

- **Kept, `NOT NULL`, meaning "our English descriptive label".** Six committed data migrations INSERT `terms.canonical_en` (`git grep -l canonical_en -- 'scripts/migrations/data_*' | wc -l`) and six views read it as a parameter's name (`select name from sqlite_master where type='view' and sql like '%canonical_en%'`); every one keeps working because the column keeps its meaning: a label to show and to search our own registry by. Relaxing `NOT NULL` would rebuild `terms` for no gain once English labels are allowed (eighth statement).
- **Never a form.** No writer copies `canonical_en` into `term_aliases`. `rename-term` stops doing so (it wrote the old label as `DEPRECATED`); the former label stays recorded once, in the `scope_note` trailer `rename-term` already writes.
- **Marked as ours by derivation, not a column** (OD-03: "add no label-kind column"): `v_term_names.label_is_instrument_term` is 1 exactly when an attested member form of the same concept has the label's text. Otherwise the label is ours.
- **The 94 terms** (`select count(*) from terms`) are unchanged; every one derives `label_is_instrument_term = 0` today, because no row is attested yet (`select count(*) from term_aliases where observation_id is not null` prints 0, and T-026's fill adds no locator).
- The rule that a label must sit inside an observed phrase (the owner's 2026-09-09 rule, kept 2026-10-09) **still binds when the first form is English**; it is lifted only for a concept whose first form is not English, where the eighth statement allows an English descriptive label.

## 7. The name shown: `v_term_names` (E1 derived; sketch)

```sql
-- sketch: one view, the only reader of "what is this concept called"
CREATE VIEW v_term_names AS
WITH attested AS (                  -- member forms a source uses; seeds are never vocabulary (E4)
    SELECT form_id, term_id, alias, upper(language) AS language, jurisdiction, attestation
      FROM term_aliases
     WHERE alias_type NOT IN ('NARROWER','BROADER')
       AND attestation IN ('instrument','other_source')),
en_instrument AS (                  -- English forms an instrument of an owed English-language jurisdiction uses
    SELECT a.* FROM attested a
     WHERE a.attestation = 'instrument' AND a.language = 'EN'
       AND EXISTS (SELECT 1 FROM v_research_scope r
                    WHERE upper(r.language) = 'EN' AND r.jurisdiction = a.jurisdiction)),
pick AS (
    SELECT t.term_id, t.canonical_en,
           (SELECT form_id FROM en_instrument e WHERE e.term_id = t.term_id
              AND lower(e.alias) = lower(t.canonical_en) ORDER BY form_id LIMIT 1) AS en_label_form,
           (SELECT MIN(form_id) FROM en_instrument e WHERE e.term_id = t.term_id) AS en_first_form,
           (SELECT MIN(form_id) FROM attested o WHERE o.term_id = t.term_id
              AND o.attestation = 'instrument') AS origin_form
      FROM terms t)
SELECT p.term_id,
       p.canonical_en AS label,
       EXISTS (SELECT 1 FROM attested a WHERE a.term_id = p.term_id
                 AND lower(a.alias) = lower(p.canonical_en)) AS label_is_instrument_term,
       CASE WHEN p.en_label_form IS NOT NULL THEN 'english_instrument_label'
            WHEN p.en_first_form IS NOT NULL THEN 'english_instrument_form'
            WHEN p.origin_form   IS NOT NULL THEN 'origin_instrument_form'
            ELSE 'label_ours' END AS display_basis,
       COALESCE(p.en_label_form, p.en_first_form, p.origin_form) AS display_form_id,
       COALESCE((SELECT alias FROM term_aliases f
                  WHERE f.form_id = COALESCE(p.en_label_form, p.en_first_form, p.origin_form)),
                p.canonical_en) AS display_name,
       COALESCE((SELECT upper(language) FROM term_aliases f
                  WHERE f.form_id = COALESCE(p.en_label_form, p.en_first_form, p.origin_form)),
                'EN') AS display_language,
       p.origin_form AS origin_form_id
  FROM pick p;
```

**The rules, in order (E1, with the stored choice):**
1. Our label equals an English form an instrument of an owed English-language jurisdiction uses → show it (`english_instrument_label`). This is also how the stored, warranted choice works: `rename-term --from-form <form_id>` sets the label to one attested form (section 8).
2. Else an English instrument form of such a jurisdiction exists → show the first recorded of them (`english_instrument_form`). **[ANSWERED 2026-11-12, fifth set, OD-38: "First recorded, until a named judge picks; the pick is recorded with its reason".]** The pick is `rename-term --from-form` with a named judge and a reason, both in typed columns (section 8, corrected). **Arbitrary when there are several** (for example two English-language codes naming one concept differently); the remedy is rule 1 via `rename-term`, and `select term_id from v_term_names v where display_basis='english_instrument_form' and (select count(distinct lower(alias)) from term_aliases a where a.term_id=v.term_id and upper(a.language)='EN' and a.attestation='instrument') > 1` lists the concepts owed that choice.
3. Else an instrument form in any language exists → show the origin instrument's phrase, in its own language (`origin_instrument_form`): E1 proper.
4. Else → show our label (`label_ours`), which a page marks as ours.

"Owed English-language jurisdiction" is read from `v_research_scope`, the one home of scope (T-101 fills it); no list of jurisdictions is typed. Readers: render (T-037, the name shown and the "ours" mark), any writer output that names a concept, the base coverage view when one is built (section 15).

## 8. Every writer that screens or matches a name, and how it changes

| Writer (locate by symbol in `scripts/db.py`) | Today | After T-028 |
|---|---|---|
| `_name_holder(conn, name, *, aliases, exclude_term)` | exact match on `canonical_en` first, then on any alias in any language | `_name_holder(conn, name, language, *, exclude_term=None)` returns **every** clash, none first: `label` (another term's `canonical_en`, case-folded, compared only when `language` is EN) and `form` (an **attested** member form in the same language, case-folded). Seeds never clash (E4); they are returned as `seed_matches` for information. |
| `_near_terms(conn, name)` | token overlap with every `canonical_en` and every EN alias | `_near_terms(conn, name, language)`: token overlap with attested member forms in `language`, and with labels only when `language` is EN. A non-English name is never screened against English. Tokenising is T-009's script-aware `_name_tokens`; until T-009 merges, a non-Latin name yields no tokens and no near match, which the refusal text must say. |
| `insert_term` / `add-term --from-observation` | mints the term and the NAMES-NEW adjudication; refuses a label not inside the observed phrase; writes no form | also writes the observation's surface form as the concept's **first member row** (`alias_type SYNONYM`, `observation_id` set, `attestation` from `--attestation instrument\|other_source`, required); screens the label as a label and the surface form as a form; the inside-the-phrase rule applies only when the observation's language is EN (section 6) |
| `add-term`, **new base route** | — | `db.py add-term --first-form "<text>" --form-language XX --form-jurisdiction YY --source-url URL (--source-page P \| --source-clause C) [--source-line N] --attestation instrument\|other_source [--usage-type T] --canonical-en "<our label>" --rationale "..." [--distinct-from TERM-ID ...] --session S`. Exactly one of `--from-observation` and `--first-form`. Writes the term and its first member row in one transaction. Refuses: a (language, jurisdiction) pair `lang_jur_map` lacks; no locator; a value-bearing label (the existing `_VALUE_BEARING_NAME` refusal); an English first form whose text does not contain the label; a label clash; an attested form clash in that language unless named by `--distinct-from` (a recorded conflation). |
| `rename_term` / `rename-term` | sets the label; writes the old label into `term_aliases` as `DEPRECATED` | sets the label; writes **no** alias row; new warrant route `--from-form <form_id>` (an attested member form of this term whose text equals the new label), beside `--from-observation` and `--ruling-quote`; label screen only. **[Added 2026-11-12 on OD-38]** `--from-form` requires `--judge` (who picked) beside `--reason`; both are recorded in typed columns, not in the `AMENDED` trailer on `scope_note` that the verb writes today (a correction appended to a note, which the 2026-11-06 schema-shape statement forbids); the executor names the one home and reports it |
| `mint_term_from_catalogue` | exact clash on label and aliases | label screen only (a catalogue entry is our English register, not an attested form) |
| `insert_alias` / `add-alias` | key `(term, alias, language)`; promotes a held seed in place; refuses `TRANSLATION`, `DEPRECATED` | records an occurrence: the **first** attested occurrence of a held seed's text promotes that seed row in place (its `attestation` and locator are set; no second row); a further occurrence is a new row; refuses `DOMAIN` as well, naming `--usage-type`; reports conflation (section 5); duplicate occurrence refused in words before the index would |
| `observe-term`, `adjudicate-term` | evidence-stage reading | unchanged (the scan contract) |
| `log-search` | `terms_used` JSON | T-026's junction to `form_id`; a search records the forms it used, never the label |
| `amend-term` | refuses `canonical_en` | unchanged |

## 9. Pointers to other homes

- **Translations (T-049).** A translation of a form is a `translations` row pointing at `('term_aliases', 'alias', <form_id>)`, never an alias and never a term; a concept is minted only from an observed or located phrase (no back-translation). Before T-028 merges, a pointer made by `rowid` survives, since `form_id` is the old `rowid`. The English label is **not** a translation of any form and is never stored as one.
- **`value_as_written` (T-008)** is the same principle at the grain of a figure: the source's words in a cell that names them (`term_aliases.alias`, with its locator), our reading in a cell that names it ours (`canonical_en`). No second mechanism is built.
- **`observed_terms`** stays the evidence-stage record of a sighting; a member row points at it by `observation_id` where it came that way.

## 10. Migration shape (one schema migration; derive its number, never type it)

Number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one, zero-padded; `scripts/migrations/NNN_term_forms_occurrence.sql`; ends `PRAGMA user_version = NNN;`. Steps:

1. Header: OD-03, this design, and `-- AFTER_DATA: <newest data_ timestamp>` (`ls scripts/migrations/data_*.sql | sed -E 's/.*data_([0-9]{14})_.*/\1/' | sort | tail -1`). T-107's data migrations may insert `term_aliases` rows before this runs; without the marker the rebuild would replay them after the reshape and diverge.
2. `CREATE TABLE _NNN_term_aliases` as section 3 (copy T-026's column definitions from `sqlite_master` at execution, not from this page).
3. `INSERT INTO _NNN_term_aliases (form_id, <every column>) SELECT rowid, <every column>, NULL FROM term_aliases;` (`usage_type` NULL).
4. `DROP TABLE term_aliases; ALTER TABLE _NNN_term_aliases RENAME TO term_aliases;` then the unique index and the two existing indexes. No view or trigger names the table today: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,name from sqlite_master where sql like '%term_aliases%' and name<>'term_aliases'\").fetchall())"`; re-run at execution (T-026's junction will name it by FK: recreate as it stands).
5. `CREATE VIEW v_term_names` (section 7).

Proof: `migrate_db.py --rebuild` exits 0; `migration_reproducibility.py --deep` passes; `joined_cells_census.py` before and after (a new candidate is a stop).

## 11. The existing data

| Held | Command | After T-026 and T-028 |
|---|---|---|
| terms | `select count(*) from terms` | unchanged; each label derives as ours (section 6) |
| aliases | `select count(*), count(distinct term_id) from term_aliases` | every row kept with `form_id` = its old `rowid`; T-026's `attestation` fill; `usage_type` NULL |
| `TRANSLATION` aliases | `select count(*) from term_aliases where alias_type='TRANSLATION'` | flagged search aids per E4: T-026's fill gives `model_seed` or `unrecorded`, never an attestation; not shown, not matched as vocabulary, not deleted; promoted only by a located occurrence (T-107) |
| `NARROWER` / `BROADER` | `select alias_type, count(*) from term_aliases where alias_type in ('NARROWER','BROADER') group by 1` | non-members; search strings only |
| `DEPRECATED` / `DOMAIN` | `select alias_type, count(*) from term_aliases where alias_type in ('DEPRECATED','DOMAIN') group by 1` | legacy values, frozen; typed by `usage_type` when next touched |
| non-ASCII labels | the task file's evidence command | 0 before and after: labels stay English; non-English names are forms |

## 12. What reads what this adds

`v_term_names`: render (T-037), writer outputs that name a concept, the base coverage view when built. `form_id`: T-026's search junction, T-049's pointers, `add-alias` outputs. `usage_type`: T-107 (writes), render (a disfavoured form shown with its note). The occurrence index: `add-alias`, `add-term`.

## 13. Caller sweep (found by reading the code; re-run the task file's section 5 commands for `canonical_en`, and the same for `term_aliases`, `_name_holder`, `_near_terms`)

| Caller | Change |
|---|---|
| `scripts/db.py` `_name_holder`, `_near_terms`, `insert_term`, `rename_term`, `mint_term_from_catalogue`, `insert_alias`, the `add-term`, `rename-term`, `add-alias` parsers | section 8 |
| `scripts/db.py` `_alias_language` | unchanged (T-015 folds case); the occurrence index compares `language` as stored |
| `scripts/audit/alias_provenance_audit.py` | reads `attestation` (T-026); counts per `form_id`, not per key |
| `scripts/audit/graph/extract_db.py`, `scripts/audit/jurisdiction_db_vocabulary.py`, `scripts/audit/research_batch_dod.py`, `scripts/audit/scan_debt.py`, `scripts/validate_parameters.py` | read `canonical_en` as a label or `term_aliases` columns by name: run before/after; a key-based read of `term_aliases` moves to `form_id` |
| tests: `scripts/tests/test_scan_contract.py` (the add-alias and rename-term cases), `test_db_amend_writers.py`, `test_evidence_cell_state_2_3.py`, `test_run_pipeline_refusals.py` | the rename-term case that asserts a `DEPRECATED` alias is rewritten to assert the label is recorded in `scope_note` and **no** alias row is written; any fixture inserting `term_aliases` without `attestation` gains it |
| `skills/run-pipeline_SKILL.md`, `skills/multilingual-research_SKILL.md` (`git grep -n -e canonical_en -e term_aliases -e add-term -e add-alias -- skills`) | a search uses the forms of its language, never the label; minting a non-English concept uses `add-term --first-form` with an English descriptive label |
| prose: `architecture/sqlite-data-layer.md`, `governance/owner-browser.yaml`, `governance/pipeline-contract.yaml`, `governance/functional-taxonomy.md`, `governance/stage-map.yaml`, `governance/context-map.yaml`, `governance/held-tensions.md` | sentences that call `canonical_en` "the name" or `term_aliases` keyed by language become "label" and "occurrence"; `build_graph.py --check` once |

## 14. Red tests (prefix `T028-`; confirm free first)

| Id | File | Test | Expected today (red) | After |
|---|---|---|---|---|
| T028-01 (AT-25) | `scripts/tests/test_scan_contract.py` | on a scratch copy, `add-term --first-form` with a form in the first non-EN language of `lang_jur_map` (by query) and its paired jurisdiction, a URL and clause, `--attestation instrument`, and an English descriptive label; then reads `v_term_names` | `add-term: error: the following arguments are required: --from-observation` | one term; one member row in that language; `label_is_instrument_term = 0`; `display_basis = 'origin_instrument_form'`; no attested EN row for the term |
| T028-02 (C-04) | same | `add-term --from-observation` on a fixture observation whose language is not EN, with an English label not inside the phrase | refused: `--canonical-en '...' is not inside the observed phrase` | accepted; the observation's phrase is the first member row |
| T028-03 | same | the same form text attested in two jurisdictions for one term (two `add-alias` base-route calls) | refused or promoted in place by the `(term_id, alias, language)` key | two rows, two `form_id`s |
| T028-04 | same | `rename-term --from-form <id>` | `unrecognized arguments: --from-form`; and the old label is written as a `DEPRECATED` alias | label changed; `display_basis = 'english_instrument_label'` when that form is an EN instrument form; no alias row written |
| T028-05 (AT-24 for names) | same | a `model_seed` row whose text equals a new label does not make `_name_holder` refuse | refused as an alias clash today | no clash; reported in `seed_matches` |
| T028-06 | same | `_near_terms` on a non-EN name does not return English labels | English labels compared regardless of language | none returned |

## 15. Rejected alternatives, and where the owner may disagree

- **A. A new `term_forms` table (the 2026-11-06 matrix design).** Leaves the 2382 rows in a second home (section 2).
- **B. Relax `canonical_en` to nullable and name a non-English concept by its phrase in that column.** Rebuilds `terms` under six views; puts a form in the label's cell, the opposite of OD-03.
- **C. A typed label-kind column on `terms`.** OD-03 forbids it: derivable, and a typed value can only be right or wrong.
- **D. A stored display pointer on `terms`.** A second home for the choice `rename-term` already stores in the label with its warrant; it could disagree with the forms.
- **E. Rewrite the legacy `alias_type` values in the migration.** `DOMAIN` needs judgment per row; a mechanical rewrite would invent usages.
- **F. Put the occurrence grain into T-026.** Turns a column addition into a rebuild for a Sonnet task, while T-028 rebuilds the table anyway; instead T-107 waits for T-028.

**Where the owner may disagree:** (1) [ANSWERED 2026-11-12, OD-38: first recorded until a named judge picks, the pick recorded with its reason] the tie-break of section 7, rule 2 (first recorded English instrument form) against showing our label when several English instruments differ; (2) lifting the inside-the-phrase rule only for non-English first forms (section 6); (3) the label clash being checked only for English names (a non-English candidate's English label is still screened, as a label).

**Not resolved here, reported:** no task builds the base coverage view the seventh statement makes the acceptance test (AT-23 is listed against T-026, whose change does not describe it); `v_term_names` and the occurrence grain are what it would read.
