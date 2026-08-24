-- 063_authors_are_derived.sql
-- SCHEMA migration — give the evidence stage ONE home for who wrote a source, and a view
-- to read it from. No data is touched here; the copies are retired by the code sweep and
-- NULLed forward by the data migration that follows.
--
-- OWNER RULING 2026-08-24, DR-2026-08-24-scaffolding-is-phase-specific §2.1, general form:
--     "If a crossing row 'carries' its own reason, that introduces the possibility of error
--      and drift because it implies the reason is being written across two or more tables.
--      It is better to have a table cell point to another table cell than to rewrite."
-- The rule as stated there: NEVER WRITE THE SAME FACT INTO A SECOND TABLE.
--
-- THE COPY. `evidence_source_authors` holds the authors, one row each, ordered by position.
-- `evidence_sources` then holds five columns that are that same fact re-written:
--     author_count            = COUNT(*) of those rows
--     first_author_last       = position-1 last_name (or corporate_name)
--     first_author_first      = position-1 first_name
--     is_corporate_primary    = position-1 is_corporate
--     author_display          = the rows, formatted
--
-- THE DRIFT IS NOT HYPOTHETICAL — IT WAS REPRODUCED BEFORE THIS WAS WRITTEN.
-- `scripts/resolve_dois.py` is the only program that writes evidence_source_authors. On
-- enrichment it DELETEs every author row and reinserts the Crossref list, then updates
-- author_count and author_count_is_complete — and NOTHING ELSE. first_author_last and
-- author_display are left holding the previous authors. Nothing in the repository refreshes
-- them. Run against a scratch copy of the live DB with a payload naming different authors:
--
--     BEFORE: first_author_last='Bettarello'  author_display='Bettarello F; Caniato M; Scavuzzo G; Gasparella A'
--     AFTER : first_author_last='Bettarello'  author_display='Bettarello F; Caniato M; Scavuzzo G; Gasparella A'
--     AUTHOR ROWS (the truth): [(1,'Zzzz','Aaa'), (2,'Yyyy','Bbb')]   author_count=2
--
-- The row is left self-contradicting — a count of 2 beside a display of four names — and
-- every citation rendered from it names people who are not the authors of record. That is
-- the failure class of 2026-08-19 (CLAUDE.md §2(c), §6), reachable this time by a routine
-- enrichment run rather than by a model writing from memory. On the live DB five sources
-- carry author_count_is_complete=0 and are eligible for exactly this on the next --enrich.
--
-- WHY A VIEW AND NOT A RECONCILIATION CHECK. A check that polices agreement between two
-- copies makes the copy safe instead of removing it, and adds enforcing surface to protect
-- a defect. CLAUDE.md §1 puts the burden of proof on the apparatus, so the copy goes.
--
-- THE COLUMNS ARE NOT DROPPED, AND CANNOT BE. Committed data migrations INSERT them, and
-- migrations are append-only and replay from the baseline (CLAUDE.md §0.3): dropping a
-- column that an earlier migration writes breaks the rebuild. They are WRITER-RETIRED —
-- no program writes them after this — and NULLed forward by the data migration. They stay
-- in the schema as tombstones. author_count_is_complete and author_display_note are NOT
-- retired: the first is a curation assertion (did we obtain the WHOLE list?) and the second
-- is prose standing in where no name exists. Neither is derivable from the rows.
--
-- INITIALS CONVENTION. author_display below reproduces the stored strings EXACTLY on all 10
-- live sources, byte for byte, including the first-initial-only form: the rows hold
-- 'Sarah R.' and the display has always read 'Payne S'. A fuller convention ('Payne SR')
-- would be a change to how every citation renders, which is a content decision and not
-- this migration's to make.
--
-- NO DATA IS READ HERE. A view stores a query, not a result, so this replays correctly
-- ahead of every data migration.

CREATE VIEW v_evidence_authors AS
SELECT
  e.ref_id                                                                   AS ref_id,
  (SELECT COUNT(*) FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id)                                              AS author_count,
  (SELECT CASE WHEN a.is_corporate = 1 THEN a.corporate_name ELSE a.last_name END
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id ORDER BY a.position LIMIT 1)                  AS first_author_last,
  (SELECT CASE WHEN a.is_corporate = 1 THEN NULL ELSE a.first_name END
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id ORDER BY a.position LIMIT 1)                  AS first_author_first,
  (SELECT CASE WHEN a.is_corporate = 1 THEN 1 ELSE 0 END
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id ORDER BY a.position LIMIT 1)                  AS is_corporate_primary,
  (SELECT group_concat(
            CASE WHEN a.is_corporate = 1 THEN COALESCE(a.corporate_name, '')
                 ELSE TRIM(COALESCE(a.last_name, '') || ' ' ||
                           substr(COALESCE(a.first_name, ''), 1, 1)) END,
            '; ' ORDER BY a.position)
     FROM evidence_source_authors a
     WHERE a.ref_id = e.ref_id)                                              AS author_display
FROM evidence_sources e;

PRAGMA user_version = 63;
