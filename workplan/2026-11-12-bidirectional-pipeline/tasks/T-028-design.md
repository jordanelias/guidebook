# T-028 design — a concept is its id; its names are forms; `canonical_en` is our label

_Written 2026-11-12 by an Opus-class designer under the owner's instruction "Opus to write design files that must be written first", on the delegated resolution of OD-03. Plan document: it changes no script, schema, row or ruling. Every count is given as the command that produces it; re-run it. SQL marked **sketch** is a shape, not a file to paste unread. Canadian English._

_Revised 2026-11-13, after the T-028 pilot (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-028-report.md`) and the fold of T-026: no pointer reaches `term_aliases` by `rowid` (SQLite cannot declare a foreign key on one and `emit_batch_sql.py` does not carry implicit rowids), so T-026's junction is keyed and T-028 remaps it by key to `form_id`; `attestation` keeps T-026's `DEFAULT`; the judge, reason and former label of every label set by judgment get one typed home, `term_label_picks`, which also holds the base route's rationale; the refusals of `rename-term` and `mint-term-from-catalogue` are kept, and one cross-language question is left to the owner; `label_is_instrument_term` is renamed `label_is_attested_form`. Where the 2026-11-12 text and this revision differ, the revision governs._

## 0. Verdict

**The one table that holds a form is `term_aliases`.** No new forms table is built. T-026 puts the attestation and locator columns on it (names fixed in section 4 so the two tasks agree). T-028 then rebuilds it to one row per **occurrence**, keyed by a new `form_id` (equal to each existing row's `rowid`), with a unique occurrence index in place of today's primary key `(term_id, alias, language)`, and adds `usage_type`. In the same migration it remaps T-026's search-to-form junction from the old key to `form_id`, by key, and adds `term_label_picks`, the one home of the judge, the reason and the former label of a label set by judgment (OD-38). A concept's identity stays `terms.term_id`; its equivalence class is its member rows in `term_aliases`. **`terms.canonical_en` stays `TEXT NOT NULL`, as our English descriptive label: never written as a form, never read first.** (A new label is screened against other concepts' labels and attested forms so that one phrase does not point at two concepts, section 8.) Whether the label is also an instrument's term, and the name shown (E1), are derived by one view, `v_term_names`; the only stored choice is the label itself, changed by `rename-term` with its warrant. Five writers change: the two name screens (`_name_holder`, `_near_terms`) become attestation-aware and stop making English the pivot for a non-English name; `add-term` gains a base route that mints a concept with its first attested form and stops forcing a non-English concept's label to sit inside the source's phrase (the defect AT-25 exposes); `rename-term` stops writing our former label as a form or as a `scope_note` trailer and gains `--from-form`, every route naming its judge; `add-alias` refuses the legacy relation values and records an occurrence, not a key.

**Confidence.** Medium-high (about 75%) that `term_aliases` is the right single home: the alternative (`term_forms`, the 2026-11-06 matrix design) leaves 2382 baseline rows in a second table that can never be emptied (section 2). Medium (about 60%) on the display rule's tie-break (section 7, rule 2), which is deterministic but arbitrary when several English instruments use different forms.

**Owner's call.** None is outstanding: OD-03 is resolved under delegation (`grep -F "OD-03 STATUS:" references/project-standards.md | tail -1`; its check is `not required`), reversible by the owner. The points at which the owner may disagree are listed in section 15; the one most likely to matter is the tie-break of section 7.

## 1. What the rulings require

| Ruling (find it with) | Requirement | Met by |
|---|---|---|
| OD-03 (delegated), `grep -n -F 'OD-03: forms table' references/project-standards.md` | identity is the neutral id; names are rows of one forms table, one row per occurrence with language, jurisdiction, source; `canonical_en` our label, never a form; label basis derived; display by E1; a stored choice only where no derivation decides | sections 3, 6, 7 |
| Sixth statement 2026-11-06, `grep -n -F 'a concept is an equivalence class of forms' references/project-standards.md` | equivalence class; usage type and attestation per form; disfavoured forms kept; conflation recorded per occurrence, not resolved | member rows; `usage_type`; T-026's `attestation`; conflation derived (section 5) |
| Seventh statement 2026-11-06, `grep -n -F 'base grounds itself' references/project-standards.md` | a base form carries its own source columns (URL, page, line), not an `evidence_sources` row | T-026's locator columns; `add-term` base route (section 8) |
| Eighth statement 2026-11-06, `grep -n -F 'English labels are allowed on non-English-origin concepts' references/project-standards.md` | an English label allowed, marked as ours; the instrument's phrase kept as a form; no English form until an English-jurisdiction source uses one; no column read, matched or ranked first | `canonical_en` as label; `v_term_names.label_is_attested_form`; screens per language (section 8) |
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
    form_id             INTEGER PRIMARY KEY AUTOINCREMENT,   -- assigned once, in the migration, from the old rowid; nothing stored points by rowid
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    alias               TEXT NOT NULL,                       -- the form, verbatim
    language            TEXT NOT NULL DEFAULT 'EN',
    alias_type          TEXT NOT NULL CHECK (alias_type IN
                            ('SYNONYM','TRANSLATION','NARROWER','BROADER','DEPRECATED','DOMAIN')),  -- unchanged; section 5
    jurisdiction        TEXT,
    notes               TEXT,
    observation_id      INTEGER REFERENCES observed_terms(observation_id),
    attestation         TEXT NOT NULL DEFAULT 'unrecorded' CHECK (attestation IN
                            ('instrument','other_source','owner_supplied','model_seed','unrecorded')),  -- (T-026; the DEFAULT is kept)
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

-- T-026's junction, remapped by key to form_id (section 10, step 3).
CREATE TABLE search_execution_forms (
    exec_id            INTEGER NOT NULL REFERENCES search_executions(exec_id),
    form_id            INTEGER NOT NULL REFERENCES term_aliases(form_id),
    created_at         TEXT NOT NULL,
    created_by_session TEXT NOT NULL,
    PRIMARY KEY (exec_id, form_id)
);

-- The one home of the judge and reason of a label set by judgment (OD-38), and of the label it replaced.
CREATE TABLE term_label_picks (
    pick_id             INTEGER PRIMARY KEY,
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    former_label        TEXT,                                 -- the label replaced; NULL only for a mint by add-term --first-form
    form_id             INTEGER REFERENCES term_aliases(form_id),          -- rename-term --from-form, or a mint's first form
    observation_id      INTEGER REFERENCES observed_terms(observation_id), -- rename-term --from-observation
    ruling_quote        TEXT,                                               -- rename-term --ruling-quote (found once in the ledger)
    judge               TEXT NOT NULL,                        -- who picked
    reason              TEXT NOT NULL,                        -- why (add-term --first-form: its --rationale)
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,                        -- with whatever else dbcore.stamp_for fills
    CHECK ((form_id IS NOT NULL) + (observation_id IS NOT NULL) + (ruling_quote IS NOT NULL) = 1),
    CHECK (former_label IS NOT NULL OR form_id IS NOT NULL)
);
```

`term_label_picks` stores no route (derived from which pointer is set, rule 8) and no new label (it is `terms.canonical_en`; the pick reaches it by `term_id`, rule 5). The label a term carried between two picks is the `former_label` of the later one, or `canonical_en` after the last. A mint by `add-term --from-observation` writes no row: its warrant is its `term_adjudications` row. A catalogue mint writes none: its warrant is the catalogue columns on `terms`. Columns on `terms` for the judge and reason were rejected (section 15, G).

`usage_type` is nullable: NULL means "not yet typed", which is the truth for every existing row; it is typed by judgment when a row is next touched (T-107), never guessed by the migration. The five values are the sixth statement's list, in the column's own CHECK (read by `dbcore.check_values`, never retyped).

## 4. What T-026 builds on this table (as folded 2026-11-13; T-026's section 4 governs its own details)

- `attestation TEXT NOT NULL DEFAULT 'unrecorded'` with the five-value CHECK above (the sixth statement's four kinds plus `unrecorded`): `instrument` (a code, standard or statute uses the form), `other_source` (any other source uses it: signage manual, public-body or advocacy guidance, a study, a glossary), `owner_supplied` (a seed the owner gave), `model_seed` (a model generated it), `unrecorded` (no provenance). `instrument` and `other_source` are attestations; the other three are seeds or unknowns and are **search aids only** (E4). The `DEFAULT` is required by `ADD COLUMN ... NOT NULL`, and T-028's rebuild keeps it (section 10, step 2).
- `source_url`, `source_page`, `source_line`, `source_clause`, and the two cross-column CHECKs of section 3, in DDL.
- **Mechanical fill**, from what the row already says, in `classify()`'s precedence (`scripts/audit/alias_provenance_audit.py`), by `INSTR`: `VERIFIED-GLOSSARY`, `VERIFIED-CROSS` and `VERIFIED-NATIVE` → `unrecorded` (they carry no observation and no locator, so the first CHECK would refuse `other_source`; the condition this page set on 2026-11-12 came true, and T-026 lists those rows for T-107 to re-attest with a locator); `observation_id` set → `other_source`; `model-generated` → `model_seed`; anything else → `unrecorded`. Never `instrument` by inference.
- `add-alias` gains the base route of the seventh statement (`--alias --language --jurisdiction --source-url (--source-page | --source-clause) [--source-line] --attestation instrument|other_source`, the pair checked against `lang_jur_map`) and a seed route (`--seed owner_supplied|model_seed`). The base route's warrant is its locator and its judge is `created_by_session`: no rationale column. The observation route writes `other_source` unless `--attestation instrument` is given.
- `alias_provenance_audit` reads `attestation` first and falls back to the notes markers for `unrecorded` rows only, so the curated, repo-shorthand and `VERIFIED-*` classes survive until T-107 re-attests them. T-028 changes nothing in it: it already counts per row, which is per `form_id`.
- **The search-forms junction, `search_execution_forms`**, points at a form by `term_aliases`' present key `(term_id, alias, language)` with a real foreign key, not by `rowid`: SQLite cannot declare a foreign key on a rowid (measured: `foreign key mismatch`), and `scripts/research/emit_batch_sql.py` diffs a table by its declared key and emits rows without their implicit rowids (`grep -n 'implicit rowids' scripts/research/emit_batch_sql.py`), so a rowid captured on a scratch copy can name another row in the canonical database. `log-search --form-id N` takes a rowid as input only and stores the key. T-028 remaps the junction by that key to `form_id` (section 10, step 3).

**Why the occurrence grain is T-028's and not T-026's:** T-026 adds columns by `ALTER TABLE` and needs no rebuild; the grain needs one. Until T-028 merges, a second occurrence of a form a term already holds in that language cannot be stored, so **T-107 (attest forms) now waits for T-028** (its task file is corrected in the same pass).

## 5. Membership, the legacy `alias_type` values, and conflation

- **Members of the equivalence class** are the rows whose `alias_type` is not `NARROWER` or `BROADER`. A `NARROWER` or `BROADER` row is a related search string, not a name of the concept: it is never shown as a name, never counted as a form, never matched as a name. (Term-to-term relations are T-029's table; these strings name no term.)
- **`TRANSLATION`, `DEPRECATED`, `DOMAIN` are legacy values.** Each joins a relation with another fact (a seed's origin; a usage; a domain variant). After T-026 and T-028 those facts have typed homes (`attestation`, `usage_type`). The existing rows are **not rewritten** (`DOMAIN` cannot be mapped to a usage without judgment: `select alias, language, notes from term_aliases where alias_type='DOMAIN'`); no writer writes these three values again; no reader infers attestation or usage from them. `add-alias` already refuses `TRANSLATION` and `DEPRECATED`; it now refuses `DOMAIN` too, naming `--usage-type`. `rename-term` stops writing `DEPRECATED` (section 8).
- **Conflation is derived, not stored:** a form held as a member by two concepts in one language is a conflation. Query: `select upper(language), alias, group_concat(distinct term_id) from term_aliases where alias_type not in ('NARROWER','BROADER') group by 1, 2 having count(distinct term_id) > 1`. `add-alias` reports it; `add-term` refuses it unless the operator names the other concept with `--distinct-from`; `rename-term` and `mint-term-from-catalogue` refuse a label another concept holds as an attested form, as they do today (section 8; corrected 2026-11-13).

## 6. `canonical_en`

- **Kept, `NOT NULL`, meaning "our English descriptive label".** Six committed data migrations INSERT `terms.canonical_en` (`git grep -l canonical_en -- 'scripts/migrations/data_*' | wc -l`) and six views read it as a parameter's name (`select name from sqlite_master where type='view' and sql like '%canonical_en%'`); every one keeps working because the column keeps its meaning: a label to show and to search our own registry by. Relaxing `NOT NULL` would rebuild `terms` for no gain once English labels are allowed (eighth statement).
- **Never a form.** No writer copies `canonical_en` into `term_aliases`. `rename-term` stops doing so (it wrote the old label as `DEPRECATED`); the former label is recorded once, in `term_label_picks.former_label` (section 3). **Corrected 2026-11-13:** this page first kept it in the `AMENDED` trailer `rename-term` writes on `scope_note`, which the 2026-11-06 schema-shape statement forbids (a correction appended to a note); no route of `rename-term` writes that trailer now, and existing trailers are not rewritten.
- **Marked as ours by derivation, not a column** (OD-03: "add no label-kind column"): `v_term_names.label_is_attested_form` is 1 exactly when an attested member form (`instrument` or `other_source`) of the same concept has the label's text. (Named `label_is_instrument_term` until 2026-11-13; it was never restricted to instruments.) Otherwise the label is ours.
- **The 94 terms** (`select count(*) from terms`) are unchanged; every one derives `label_is_attested_form = 0` today, because no row is attested yet (`select count(*) from term_aliases where observation_id is not null` prints 0, and T-026's fill adds no locator).
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
                 AND lower(a.alias) = lower(p.canonical_en)) AS label_is_attested_form,
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
2. Else an English instrument form of such a jurisdiction exists → show the first recorded of them (`english_instrument_form`). **[ANSWERED 2026-11-12, fifth set, OD-38: "First recorded, until a named judge picks; the pick is recorded with its reason".]** The pick is `rename-term --from-form` with a named judge and a reason, in `term_label_picks` (sections 3 and 8). **Arbitrary when there are several** (for example two English-language codes naming one concept differently); the remedy is rule 1 via `rename-term`, and `select term_id from v_term_names v where display_basis='english_instrument_form' and (select count(distinct lower(alias)) from term_aliases a where a.term_id=v.term_id and upper(a.language)='EN' and a.attestation='instrument') > 1` lists the concepts owed that choice.
3. Else an instrument form in any language exists → show the origin instrument's phrase, in its own language (`origin_instrument_form`): E1 proper.
4. Else → show our label (`label_ours`), which a page marks as ours.

"Owed English-language jurisdiction" is read from `v_research_scope`, the one home of scope (T-101 fills it); no list of jurisdictions is typed. Readers: render (T-037, the name shown and the "ours" mark), any writer output that names a concept, the base coverage view when one is built (section 15).

## 8. Every writer that screens or matches a name, and how it changes

| Writer (locate by symbol in `scripts/db.py`) | Today | After T-028 |
|---|---|---|
| `_name_holder(conn, name, *, aliases, exclude_term)` | exact match on `canonical_en` first, then on any alias in any language | `_name_holder(conn, name, language, *, exclude_term=None)` returns **every** clash, none first: `label` (another term's `canonical_en`, case-folded, compared only when `language` is EN: the eighth statement, our label is not a form and English is not matched first) and `form` (another term's **attested** form, case-folded, of any `alias_type`, **in any language**: today's reach, kept until the owner answers the cross-language question of section 15). Seeds never clash (E4); they are returned as `seed_matches` for information. **Corrected 2026-11-13:** this page first compared forms in the same language only, a narrowing no ruling licenses. |
| `_near_terms(conn, name)` | token overlap with every `canonical_en` and every EN alias (T-026: attested EN aliases only) | `_near_terms(conn, name, language)`: token overlap with attested forms in `language`, of any `alias_type` (`NARROWER` and `BROADER` included, as T-026 has it: not names, but a near one is worth the refusal), and with labels only when `language` is EN. A non-English name is never screened against English (the eighth statement). Tokenising is T-009's script-aware `_name_tokens`; until T-009 merges, a non-Latin name yields no tokens and no near match, and no refusal fires, so **the writer's output** (not a refusal text) must say that no near screen ran. |
| `insert_term` / `add-term --from-observation` | mints the term and the NAMES-NEW adjudication; refuses a label not inside the observed phrase; writes no form | also writes the observation's surface form as the concept's **first member row** (`alias_type SYNONYM`, `observation_id` set) **through the function `add-alias`'s observation route uses**, so the attestation is written to one standard: where its check passes (the quote contains the phrase and is in a file saved for the source, or is `VERBATIM-EXEMPT`), `attestation` is `--attestation instrument\|other_source`, optional, default `other_source` (as T-026's observation route); where it fails, the term is still minted and the row is `unrecorded`, the output saying so and that `add-alias` promotes it once the quote is verified. Screens the label as a label and the surface form as a form; the inside-the-phrase rule applies only when the observation's language is EN (section 6); its warrant stays the `term_adjudications` row (no pick row) |
| `add-term`, **new base route** | — | `db.py add-term --first-form "<text>" --form-language XX --form-jurisdiction YY --source-url URL (--source-page P \| --source-clause C) [--source-line N] --attestation instrument\|other_source [--usage-type T] --canonical-en "<our label>" --judge "<who>" --rationale "..." [--distinct-from TERM-ID ...] --session S`. Exactly one of `--from-observation` and `--first-form`. Writes the term, its first member row and one `term_label_picks` row (`form_id` the first form, `former_label` NULL, `judge`, `reason` = `--rationale`) in one transaction: the base route writes no adjudication (`term_adjudications.observation_id` is `NOT NULL`), and a judgment about the concept does not belong in the form's `notes`. Refuses: a (language, jurisdiction) pair `lang_jur_map` lacks, compared case-insensitively as T-026's `add-alias` base route does; no locator; a value-bearing label (the existing `_VALUE_BEARING_NAME` refusal); an English first form whose text does not contain the label; a label clash; an attested form clash (any language, section 15) unless named by `--distinct-from` (a recorded conflation). |
| `rename_term` / `rename-term` | sets the label; writes the old label into `term_aliases` as `DEPRECATED` and an `AMENDED` trailer on `scope_note` | sets the label; writes **no** alias row and **no** `scope_note` trailer; new warrant route `--from-form <form_id>` (an attested member form of this term whose text equals the new label), beside `--from-observation` and `--ruling-quote`. **[OD-38, corrected 2026-11-13]** every route requires `--judge` (who picked) beside `--reason`, and writes one `term_label_picks` row: `former_label`, the route's pointer (`form_id`, `observation_id` or `ruling_quote`), `judge`, `reason`. Screen: `_name_holder(conn, new, 'EN', exclude_term=term_id)`, so a name another term holds as an attested form is **still refused** (this page first said "label screen only", which weakened that refusal without a ruling); seeds no longer refuse (E4). |
| `mint_term_from_catalogue` | exact clash on label and aliases | the same screen as `rename-term` (corrected 2026-11-13 from "label screen only"): labels, and attested forms in any language; seeds no longer refuse (E4). Writes no pick row (the catalogue columns on `terms` are its warrant) |
| `insert_alias` / `add-alias` | key `(term, alias, language)`; promotes a held seed in place; refuses `TRANSLATION`, `DEPRECATED`; T-026's base and seed routes and its no-downgrade refusal | records an occurrence: the **first** attested occurrence of a held seed's text promotes that seed row in place (its `attestation` and locator are set; no second row); a further occurrence (another observation, jurisdiction or locator) is a new row, so T-026's "a second occurrence waits for T-028" refusal goes and no row is ever re-attested; refuses `DOMAIN` as well, naming `--usage-type`; writes `--usage-type` (the column's CHECK); reports conflation (section 5); a duplicate occurrence refused in words before the index would, keeping the texts the existing tests match |
| `observe-term`, `adjudicate-term` | evidence-stage reading | unchanged (the scan contract) |
| `log-search` | T-026: `--form-id` (a rowid as input), junction row stored by key | `--form-id` takes and stores a `form_id`; a search records the forms it used, never the label |
| `amend-term` | refuses `canonical_en` | unchanged |

## 9. Pointers to other homes

- **Translations (T-049).** A translation of a form is a `translations` row pointing at `('term_aliases', 'alias', <form_id>)`, never an alias and never a term; a concept is minted only from an observed or located phrase (no back-translation). The English label is **not** a translation of any form and is never stored as one. **Corrected 2026-11-13:** this page said a pointer made by `rowid` before T-028 "survives, since `form_id` is the old `rowid`". It survives a rebuild, but not the capture: `emit_batch_sql.py` does not carry implicit rowids (section 4), so a rowid written on a scratch copy can name another row in the canonical database, and before T-028 `term_aliases` has a composite key that a single `source_row_key` cell does not hold without an encoding nobody has defined. So no translation points into `term_aliases` before T-028: T-049's file, as folded on 2026-11-13, already says so (`request-translation` refuses a table whose declared primary key has more than one column, and never points by `rowid`). After T-028 a translation points at `form_id`, which the migration preserves, so nothing is remapped; if `translations` nevertheless holds a row pointing into `term_aliases` at execution, T-028 stops rather than guess its encoding (the task file's section 9).
- **`value_as_written` (T-008)** is the same principle at the grain of a figure: the source's words in a cell that names them (`term_aliases.alias`, with its locator), our reading in a cell that names it ours (`canonical_en`). No second mechanism is built.
- **`observed_terms`** stays the evidence-stage record of a sighting; a member row points at it by `observation_id` where it came that way.

## 10. Migration shape (one schema migration; derive its number, never type it)

Number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one, zero-padded; `scripts/migrations/NNN_term_forms_occurrence.sql`; ends `PRAGMA user_version = NNN;`. Steps:

1. Header: OD-03, this design, and `-- AFTER_DATA: <newest data_ timestamp>` (`ls scripts/migrations/data_*.sql | sed -E 's/.*data_([0-9]{14})_.*/\1/' | sort | tail -1`). T-107's data migrations may insert `term_aliases` rows before this runs; without the marker the rebuild would replay them after the reshape and diverge.
2. `CREATE TABLE _NNN_term_aliases` as section 3 (copy T-026's column definitions from `sqlite_master` at execution, not from this page; this keeps `attestation`'s `DEFAULT 'unrecorded'`, which stays: a writer that omits the column, such as `research_batch_dod.py`'s selftest INSERT or a test fixture, then records `unrecorded`, which is true of it).
   `INSERT INTO _NNN_term_aliases (form_id, <every column>) SELECT rowid, <every column>, NULL FROM term_aliases;` (`usage_type` NULL). The `rowid` is read once, here, to number the forms; the rebuild reproduces it (`migration_reproducibility.py --deep` is the proof), and no stored row points by it.
3. **Remap T-026's junction by key** (corrected 2026-11-13: this page said the junction "will name it by FK: recreate as it stands"; recreated as it stands, its foreign key on `(term_id, alias, language)` would answer `foreign key mismatch` once that key is no longer unique): `CREATE TABLE _NNN_search_execution_forms` as section 3, then `INSERT INTO _NNN_search_execution_forms (exec_id, form_id, created_at, created_by_session) SELECT j.exec_id, a.form_id, j.created_at, j.created_by_session FROM search_execution_forms j JOIN _NNN_term_aliases a USING (term_id, alias, language);` (one row per key until now, so the join is exact; the row count must equal the old junction's). This is T-026's own statement of the remap (its section 4 item 1), joined to the new table by key rather than to the old one's `rowid`.
4. `DROP TABLE search_execution_forms; DROP TABLE term_aliases; ALTER TABLE _NNN_term_aliases RENAME TO term_aliases; ALTER TABLE _NNN_search_execution_forms RENAME TO search_execution_forms;` then the unique occurrence index, the two existing indexes, and any index the junction carried. `migrate_db.py` runs the body with foreign keys off and checks them after (`grep -n 'foreign_keys=OFF' scripts/migrate_db.py`), so the order is safe. List what names either table at execution: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,name from sqlite_master where (sql like '%term_aliases%' or sql like '%search_execution_forms%') and name not in ('term_aliases','search_execution_forms')\").fetchall())"`; anything it prints is recreated.
5. `CREATE TABLE term_label_picks` (section 3).
6. `CREATE VIEW v_term_names` (section 7).

Do not `VACUUM`: the file grows by the rebuild's free pages, and `VACUUM` may renumber the implicit rowids of every table without an `INTEGER PRIMARY KEY`. The `AFTER_DATA` marker of step 1 opens no new segment when no data migration has landed since T-026's migration (which carries the same kind of marker); it is written all the same.

Proof: `migrate_db.py --rebuild` exits 0; `migration_reproducibility.py --deep` passes; `joined_cells_census.py` before and after (a new candidate is a stop); and the remap of step 3 shown on a non-empty junction (a `TASK-FIXTURE` row written with `log-search --form-id` on a scratch copy before the migration reaches the same `(term_id, alias, language)` after it): the pilot proved it on an empty junction only, which proves nothing (CLAUDE.md rule 4).

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

`v_term_names`: render (T-037), writer outputs that name a concept, the base coverage view (T-057). `form_id`: the search junction, `log-search --form-id`, `term_label_picks`, T-049's pointers (after T-028 only), `add-alias` outputs. `term_label_picks`: the tests; it is the record OD-38 requires, and replaces the two former homes of a former label (the `DEPRECATED` alias row and the `scope_note` trailer). `usage_type`: T-107 (writes), render (a disfavoured form shown with its note). The occurrence index: `add-alias`, `add-term`.

## 13. Caller sweep (found by reading the code; re-run the task file's section 5 commands for every needle it names, the verb and function needles included)

| Caller | Change |
|---|---|
| `scripts/db.py` `_name_holder`, `_near_terms`, `insert_term`, `rename_term`, `mint_term_from_catalogue`, `insert_alias`, `log_search`, the `add-term`, `rename-term`, `add-alias`, `log-search` parsers | section 8 |
| `scripts/db.py` `_alias_language` | unchanged (T-015 folds case); the occurrence index compares `language` as stored |
| `scripts/audit/alias_provenance_audit.py` | unchanged by T-028: T-026 makes it read `attestation` with a notes fallback for `unrecorded` rows, and it already counts per row, which is per `form_id` |
| `scripts/audit/graph/extract_db.py`, `scripts/audit/jurisdiction_db_vocabulary.py`, `scripts/audit/research_batch_dod.py`, `scripts/audit/scan_debt.py`, `scripts/validate_parameters.py` | read `canonical_en` as a label or `term_aliases` columns by name: run before/after; a key-based read of `term_aliases` moves to `form_id` |
| tests: `scripts/tests/test_scan_contract.py` (the add-alias and rename-term cases), `test_db_amend_writers.py`, `test_evidence_cell_state_2_3.py`, `test_run_pipeline_refusals.py` | the rename-term case that asserts a `DEPRECATED` alias (N07) is rewritten to assert **no** alias row, an unchanged `scope_note` and one `term_label_picks` row holding the former label; a fixture that calls `insert_term` needs no new argument (`--attestation` defaults), unless the shared verification of section 8 leaves its member row `unrecorded` where the case asserts otherwise; any `add-alias` case whose premise was T-026's second-occurrence refusal is a caller |
| `skills/run-pipeline_SKILL.md` (the `add-term` paragraph), `skills/research-log-manager_SKILL.md` (the `--form-id` wording T-026 wrote) (`git grep -n -e canonical_en -e term_aliases -e add-term -e add-alias -e rename-term -e form-id -- skills`) | a search uses the forms of its language, never the label; minting a non-English concept uses `add-term --first-form` with an English descriptive label and a judge; `rename-term` names its judge; `--form-id` is a `form_id`. `skills/multilingual-research_SKILL.md` names neither table nor verb (pilot): a mention |
| prose and registrations: `governance/owner-browser.yaml`, `governance/pipeline-contract.yaml`, `governance/functional-taxonomy.md`, `governance/stage-map.yaml`, `governance/context-map.yaml` (regenerated), `governance/held-tensions.md`, `workplan/pipeline-state-graph/machines.yaml` (M03.t3: "a term can only be minted FROM an observation" becomes false) | sentences that call `canonical_en` "the name" or `term_aliases` keyed by language become "label" and "occurrence"; `term_label_picks` registered under `base` in `stage-map.yaml` and described in `owner-browser.yaml` (without the stage-map entry `build_graph.py --check` gains `tables in the schema but not in stage-map`); `build_graph.py --check` before and after. `architecture/sqlite-data-layer.md` §4.9 is a design document of 2026-05-05 already false before T-026 (old key, item codes): a mention, left and reported |

## 14. Red tests (prefix `T028-`; confirm free first)

The "expected today" column says what stops the case on the unchanged code; which of several errors appears depends on argument order and on which new parameter the test passes first, so a test asserts only that the case fails before and passes after, and the red is observed, not assumed (corrected 2026-11-13).

| Id | File | Test | Expected today (red) | After |
|---|---|---|---|---|
| T028-01 (AT-25) | `scripts/tests/test_scan_contract.py` | on a scratch copy, `add-term --first-form` with a form in the first non-EN language of `lang_jur_map` (by query) and its paired jurisdiction, a URL and clause, `--attestation instrument`, an English descriptive label, `--judge` and `--rationale`; then reads `v_term_names` | an argparse usage error (an unknown or a missing argument) | one term; one member row in that language; one `term_label_picks` row with `former_label` NULL; `label_is_attested_form = 0`; `display_basis = 'origin_instrument_form'`; no attested EN row for the term |
| T028-02 (C-04) | same | `add-term --from-observation` on a fixture observation whose language is not EN, with an English label not inside the phrase | refused (not inside the observed phrase), or an unexpected keyword | accepted; the observation's phrase is the first member row |
| T028-03 | same | the same form text attested in two jurisdictions for one term (two `add-alias` base-route calls) | refused by the `(term_id, alias, language)` key | two rows, two `form_id`s |
| T028-04 | same | `rename-term --from-form <id> --judge J --reason R` | an unknown argument; and the old label is written as a `DEPRECATED` alias | label changed; `display_basis = 'english_instrument_label'` when that form is an EN instrument form; no alias row; `scope_note` unchanged |
| T028-05 (AT-24 for names) | same | a `model_seed` row whose text equals a new label does not make `_name_holder` refuse | refused as an alias clash, or the wrong arity | no clash; reported in `seed_matches` |
| T028-06 | same | `_near_terms` on a non-EN name does not return English labels | English labels compared regardless of language, or the wrong arity | none returned |
| T028-07 (OD-38) | same | `rename-term` on each of its three routes without `--judge` is refused; with it, each writes one `term_label_picks` row (`former_label`, the route's one pointer, `judge`, `reason`) and no `AMENDED` trailer | an unknown argument | as stated |
| T028-08 | same | `add-alias --alias-type DOMAIN` is refused, naming `--usage-type`; `--usage-type` outside the column's CHECK is refused; inside it, written | `DOMAIN` accepted; an unknown argument | as stated |
| T028-09 (guard) | same | a name equal to another term's **attested** form in another language: `rename-term` to it is refused; `add-term --first-form` with it is refused unless `--distinct-from` names that term | green before (the alias screen refuses), or the wrong arity | still refused: the kept refusal of section 8 |
| T028-10 | same | `add-term --from-observation` from an observation whose quote is not in a file saved for its source and is not `VERBATIM-EXEMPT` | an unexpected keyword, or no member row | the term is minted; its member row is `unrecorded` with the `observation_id`; the output says so |

## 15. Rejected alternatives, and where the owner may disagree

- **A. A new `term_forms` table (the 2026-11-06 matrix design).** Leaves the 2382 rows in a second home (section 2).
- **B. Relax `canonical_en` to nullable and name a non-English concept by its phrase in that column.** Rebuilds `terms` under six views; puts a form in the label's cell, the opposite of OD-03.
- **C. A typed label-kind column on `terms`.** OD-03 forbids it: derivable, and a typed value can only be right or wrong.
- **D. A stored display pointer on `terms`.** A second home for the choice `rename-term` already stores in the label with its warrant; it could disagree with the forms.
- **E. Rewrite the legacy `alias_type` values in the migration.** `DOMAIN` needs judgment per row; a mechanical rewrite would invent usages.
- **F. Put the occurrence grain into T-026.** Turns a column addition into a rebuild for a Sonnet task, while T-028 rebuilds the table anyway; instead T-107 waits for T-028.
- **G. The judge and reason as columns on `terms`** (2026-11-13). A later rename would overwrite them, so they would describe a pick no longer in force, and the former label would still need a home; one row per pick in `term_label_picks` keeps each. It is not alternative D: `v_term_names` does not read it.
- **H. The base route's rationale in the first form's `notes`** (the pilot's choice). A judgment about the concept in a cell about one form, which the 2026-11-06 schema-shape statement forbids; and T-026 rules out a rationale in `notes` for `add-alias`'s base route too.

**Where the owner may disagree:** (1) [ANSWERED 2026-11-12, OD-38: first recorded until a named judge picks, the pick recorded with its reason] the tie-break of section 7, rule 2 (first recorded English instrument form) against showing our label when several English instruments differ; (2) lifting the inside-the-phrase rule only for non-English first forms (section 6); (3) the label clash being checked only for English names (a non-English candidate's English label is still screened, as a label); (4) **open, the owner's (2026-11-13):** whether an identical string attested in one language for one concept clashes with a name in another language for a different concept, or is an independent form. It is a question of what the sixth statement's conflation and the eighth statement's "English is one column" mean across languages, not of code. Until it is answered the exact screen keeps today's reach (attested forms in every language; section 8), and the task file's section 9 stops on any step that would narrow it.

**Not resolved here, reported:** the base coverage view the seventh statement makes the acceptance test is T-057's (AT-23; corrected 2026-11-13: this page said no task builds it); `v_term_names`, the occurrence grain and the junction by `form_id` are what it reads.
