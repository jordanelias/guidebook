-- 135_identity_successor.sql
-- SCHEMA migration -- an identity code can be retired in place to the access need or the identity code that carries
-- it, and a crossing-map row can be retired in place. Tooling (workplan T-054, OD-37, OI-13 fold); no research rows.
--
-- WHY. MOVE and VES sit in the identity registry as populations, though the owner agreed they are access needs (OD-37),
-- and SCI and LMB are to be carried by WHEEL and UPL (T-102, T-116). Nothing could retire an identity code and say where
-- its readers should go, and nothing could retire a crossing row of identity_icf_map, so a retirement had no way to
-- finish. Identifiers are retired in place, never renamed or deleted (the 2026-09-16 ruling).
--
-- WHAT. base_taxonomy_identity gains superseded_by_need (an access_needs code) and superseded_by_identity (an identity
-- code). A DEPRECATED row names exactly ONE successor, an ACTIVE row none: one CHECK, carried by the second added
-- column (SQLite adds a column in place; a column CHECK may name the table's other columns, and it is tested on every
-- write of the row). identity_icf_map gains retired_at / retired_by_session / retired_reason, set together or not at all.
-- Every row stays; nothing is rewritten.
ALTER TABLE base_taxonomy_identity ADD COLUMN superseded_by_need TEXT REFERENCES access_needs(need_code);
ALTER TABLE base_taxonomy_identity ADD COLUMN superseded_by_identity TEXT REFERENCES base_taxonomy_identity(identity_code)
    CHECK ((status = 'deprecated' AND (superseded_by_need IS NOT NULL) + (superseded_by_identity IS NOT NULL) = 1)
        OR (status <> 'deprecated' AND superseded_by_need IS NULL AND superseded_by_identity IS NULL));

ALTER TABLE identity_icf_map ADD COLUMN retired_at TEXT;
ALTER TABLE identity_icf_map ADD COLUMN retired_by_session TEXT;
ALTER TABLE identity_icf_map ADD COLUMN retired_reason TEXT
    CHECK ((retired_at IS NULL AND retired_by_session IS NULL AND retired_reason IS NULL)
        OR (retired_at IS NOT NULL AND retired_by_session IS NOT NULL AND retired_reason IS NOT NULL));

PRAGMA user_version = 135;
