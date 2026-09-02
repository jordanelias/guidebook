-- 067_citation_mining_anchor_is_an_identity.sql
-- SCHEMA migration — the mining anchor is a ref_id IDENTITY, not an evidence_sources row.
--
-- THE DEFECT, MEASURED 2026-09-02. All ten citation_mining rows carry global_ref_id
-- NULL, doi NULL, and a local_ref_id whose resolver (source_slug_links) is empty. They
-- are records of mining against nothing: citation_mining_completeness reports
-- NOTHING-IN-SCOPE, db.py is_mined() can never match, and log_mining now raises rather
-- than duplicating. 147 harvested DOI leads survive in connections_produced with no way
-- to say which anchor produced them.
--
-- WHY IT HAPPENED, AND WHY NEITHER OBVIOUS FIX IS RIGHT.
-- The 2026-09-01 retraction nulled global_ref_id because it points at
-- evidence_sources(ref_id) and that table was emptied. The two obvious repairs both fail:
--
--   (a) Restore the pointer as-is -> FK violation. evidence_sources is empty by ruling.
--   (b) Write the anchor DOI into citation_mining.doi -> reverses a deliberate rule-5
--       decision. db.py:log_mining DROPPED that write on 2026-08-24 on the explicit
--       premise that the DOI "is reachable through global_ref_id". Restoring the copy
--       re-creates the dual home the project removed on purpose. This migration does NOT
--       take that route, and the defect register entry that proposed it (D04-019) is
--       corrected rather than followed.
--
-- WHAT IS ACTUALLY WRONG IS THE FOREIGN KEY. A ref_id is an identity that SPANS two
-- tables: source_locators (research-stage leads) and evidence_sources (admitted
-- evidence). dbcore.next_ref_id() already encodes this -- it computes the high-water mark
-- as the UNION of every table holding a ref_id, and CLAUDE.md records that the older rule
-- naming a single table was WRONG. A SQLite foreign key cannot express "exists in either
-- table", so a key naming just one of them asserts something the identity model does not:
-- that an anchor must be admitted evidence. It need not be. Mining a lead is legitimate
-- research, and under the owner's 2026-09-02 ruling those leads are exactly where the six
-- retracted anchors now live.
--
-- So the FK is dropped and global_ref_id becomes a soft identity reference, matching how
-- every other ref_id in this schema behaves. This LOSES a referential guarantee and the
-- loss is stated rather than buried: nothing now stops a typo'd ref_id being written here.
-- The compensating control is dbcore.fold_ref/REF_ID_SHAPE at the writer, plus R9a/R9b,
-- which already reconcile admitted ref_ids against the stash. An audit that checks every
-- citation_mining.global_ref_id resolves in EITHER table is the honest replacement and is
-- OWED -- not added here, because CLAUDE.md §1 puts the burden of proof on new apparatus
-- and this migration should not smuggle a check in behind a constraint change.
--
-- SQLite cannot ALTER a foreign key, so the table is rebuilt. Every column, CHECK, the
-- primary key and idx_cm_unmined are reproduced verbatim; only the FK clause on
-- global_ref_id is removed.

CREATE TABLE citation_mining_new (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    -- WAS: TEXT REFERENCES evidence_sources(ref_id). See the header.
    global_ref_id       TEXT,
    doi                 TEXT,
    backward            INTEGER NOT NULL DEFAULT 0 CHECK(backward IN (0,1)),
    forward             INTEGER NOT NULL DEFAULT 0 CHECK(forward IN (0,1)),
    connections_produced TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    deferred_reason     TEXT,
    PRIMARY KEY (slug, local_ref_id)
);

INSERT INTO citation_mining_new
SELECT slug, local_ref_id, global_ref_id, doi, backward, forward,
       connections_produced, notes, created_at, created_by_session,
       updated_at, updated_by_session, deferred_reason
FROM citation_mining;

DROP TABLE citation_mining;
ALTER TABLE citation_mining_new RENAME TO citation_mining;

CREATE INDEX idx_cm_unmined ON citation_mining(slug, backward, forward);

PRAGMA user_version = 67;
