-- 013_item_bpc_links.sql
-- Create item_bpc_links join table per Phase E.1 pilot Item 4 closure
-- (references/bpc-reasoning/room-acoustic-performance.md, session 2026-05-17,
-- owner directive "do whatever makes most sense long-term integrity").
--
-- Resolves the items↔BPCs many-to-many relationship that items.bpc_source_slug
-- (single-string FK) cannot model. A-10b ("RT60 for Hydrotherapy and Pool
-- Environments") is the existing precedent: it draws on room-acoustic-performance
-- for the parameter AND on a hydrotherapy/pool BPC for the context. The
-- forthcoming cross-population-conflict-resolutions BPC will produce more such
-- items. Denormalized 1:1 would force an arbitrary "primary BPC" per multi-source
-- item, captured only in `items.notes` — the same topic-vs-claim drift that
-- standing rule #10 sub-rule 2 exists to prevent at the citation level.
--
-- link_type values:
--   primary    — principal BPC this item derives from (exactly one per item;
--                enforced via partial unique index)
--   parameter  — additional BPC supplying the parameter (e.g., RT60 source)
--   context    — additional BPC supplying the context (e.g., hydrotherapy)
--   secondary  — supporting BPC of any other relation
--
-- items.bpc_source_slug retained read-only during the migration period for
-- backward compatibility. A future migration will deprecate the column once
-- all 91 items have ≥1 row here.
--
-- CI structure check extension (verify every ACTIVE item has ≥1 link with
-- link_type='primary') is a follow-up validator change, NOT part of this
-- schema migration. Adding the validator now would CI-block — 0/91 items
-- currently have any link. Validator ships after the items-to-BPC backfill
-- pass populates the table.
--
-- schema_version → 13

CREATE TABLE item_bpc_links (
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    link_type           TEXT NOT NULL CHECK(link_type IN (
        'primary','parameter','context','secondary'
    )),
    rationale           TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    PRIMARY KEY (item_code, slug)
);

CREATE INDEX idx_ibl_slug ON item_bpc_links(slug);
CREATE INDEX idx_ibl_type ON item_bpc_links(link_type);
CREATE UNIQUE INDEX idx_ibl_primary_per_item
    ON item_bpc_links(item_code) WHERE link_type = 'primary';
