-- 053_locator_hierarchy.sql
-- SCHEMA migration — decompose the pinpoint locator into its levels, on every
-- table that carries one.
--
-- THE PROBLEM THIS SOLVES
-- A code or standard is cited at a position inside it, and that position is
-- hierarchical: division > part > section > subsection > paragraph > clause >
-- subclause. Today it is one TEXT column, `source_section`, on three tables --
-- and in `jurisdictional_values` the position is not even there: it is packed
-- into `standard_name` alongside the document's identity, so a row reads
-- 'DIN 18040-2 §5.7' or 'ADA 2010 §404.2.5'.
--
-- That packing costs three things, all measured against the 109 live
-- jurisdictional_values rows:
--   * IDENTITY. The same document appears under several strings, so nothing
--     joins. ADA 2010 occurs in ten clause variants, BS 8300-2:2018 in four,
--     ISO 21542:2021 in three. There is no way to ask "everything we hold from
--     ADA 2010" without matching prose.
--   * ORDERING. As a string, §12.10 sorts before §12.9. Any ordered reading of
--     a standard is wrong by default.
--   * DEPTH. 85 rows cite one level, 9 cite two, 3 cite three. The structure is
--     real and none of it is queryable.
--
-- WHY LEVELS AND NOT A SINGLE PARSED FIELD
-- Because the levels are named differently by document family for the same
-- depth. ISO's top numbered level is a CLAUSE; ADA's is a SECTION; a building
-- code's may sit under a DIVISION and a PART that ISO has no equivalent of.
-- Storing the level a document actually uses keeps the citation honest, and
-- `locator_scheme` records the family so a reader knows whether the deepest
-- populated level renders as '§404.2' or 'clause 12.3'.
--
-- Most rows will leave most levels NULL. That is the design, not a defect: a
-- level that a document does not have is not missing data.
--
-- SPANS
-- `ADA 2010 §604-608` is live in the data. A citation can span a range, so each
-- level carries a matching `_end`. A NULL `_end` means a point citation, which
-- is the overwhelming majority; the columns exist so a span never has to be
-- flattened into prose to be recorded.
--
-- WHAT THIS MIGRATION DOES NOT DO
-- It adds columns and touches no row. Two follow-on pieces are deliberately
-- separate because each needs judgement over live data:
--   (a) SPLITTING multi-document rows. 21 of 109 jurisdictional_values rows
--       contain '/'. Three are FALSE POSITIVES -- 'ANSI/ASA S12.60-2010',
--       'AS/NZS 1428.4.1:2009', 'AS/NZS 2107:2016' are single standards jointly
--       issued, and splitting them would invent a source. Of the rest, some are
--       two independent attestations of one requirement and some are one
--       document citing another ('IPC / ADA reference'). Those mean different
--       things for code convergence and cannot be told apart by a regex.
--   (b) RE-KEYING. `UNIQUE (item_code, jurisdiction, standard_name)` is unique
--       today only because standard_name still carries the clause. Once the
--       locator moves out, one item cited at two clauses of one document in one
--       jurisdiction collides. Verified: zero such collisions exist right now,
--       so nothing is broken by waiting -- but the key must gain the locator
--       (and the ref_id FK that table has never had) in the same migration that
--       unpacks standard_name.
-- `source_section` is left in place and still populated. It retires when its
-- values have been decomposed, not before.

-- ── jurisdictional_values ────────────────────────────────────────────────────
ALTER TABLE jurisdictional_values ADD COLUMN locator_scheme     TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_division       TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_part           TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_section        TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_subsection     TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_paragraph      TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_clause         TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_subclause      TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_division_end   TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_part_end       TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_section_end    TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_subsection_end TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_paragraph_end  TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_clause_end     TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_subclause_end  TEXT;
ALTER TABLE jurisdictional_values ADD COLUMN loc_note           TEXT;

-- ── source_value_extractions ────────────────────────────────────────────────
ALTER TABLE source_value_extractions ADD COLUMN locator_scheme     TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_division       TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_part           TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_section        TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_subsection     TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_paragraph      TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_clause         TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_subclause      TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_division_end   TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_part_end       TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_section_end    TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_subsection_end TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_paragraph_end  TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_clause_end     TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_subclause_end  TEXT;
ALTER TABLE source_value_extractions ADD COLUMN loc_note           TEXT;

-- ── reasoning_doc_citations ─────────────────────────────────────────────────
ALTER TABLE reasoning_doc_citations ADD COLUMN locator_scheme     TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_division       TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_part           TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_section        TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_subsection     TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_paragraph      TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_clause         TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_subclause      TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_division_end   TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_part_end       TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_section_end    TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_subsection_end TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_paragraph_end  TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_clause_end     TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_subclause_end  TEXT;
ALTER TABLE reasoning_doc_citations ADD COLUMN loc_note           TEXT;

-- Indexes on the levels that carry the citation in practice. 85 of 109 live
-- rows cite a single top level, so section/clause are what any "what do we hold
-- from this document" query will filter on.
CREATE INDEX IF NOT EXISTS ix_jv_locator  ON jurisdictional_values (loc_section, loc_clause);
CREATE INDEX IF NOT EXISTS ix_sve_locator ON source_value_extractions (loc_section, loc_clause);
CREATE INDEX IF NOT EXISTS ix_rdc_locator ON reasoning_doc_citations (loc_section, loc_clause);

PRAGMA user_version = 53;
