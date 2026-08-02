-- 040_source_processing_state.sql
-- SCHEMA migration — give every source an explicit, coded processing state.
--
-- Rationale (workplan/2026-08-02-architecture-decision-and-execution-plan.md W5.2):
-- "so we don't just input a data row but forget to get the source data".
-- Today 852 of 863 sources have no capture row in any joinable evidence table,
-- and they are indistinguishable from sources that were read and had nothing
-- extractable. Absence is being asked to mean three different things: never
-- looked at, looked at and empty, and deliberately postponed.
--
-- WHY COLUMNS ON evidence_sources, and not rows in citation_mining:
--   citation_mining's primary key is (slug, local_ref_id) and a source appears
--   under up to 7 slugs, so a per-source state does not fit its grain — one
--   backlog row per source would mean picking an arbitrary slug or writing up
--   to 7 rows. citation_mining stays what it is: the per-pass discovery log.
--   Discovery state and capture state live together here, at source grain, so
--   there is exactly one place to ask "what has been done with this source".
--
-- WHY CODED VALUES AND NO FREE-TEXT COLUMN:
--   a table column carries a value, not prose. The reason a source is blocked
--   is a coded term; narrative elaboration belongs in the existing `notes`
--   column. This migration deliberately adds no new free-text field — a
--   state written as prose cannot be queried, counted, or checked, and this
--   repo already carries the proof: three metadata_quality='COMPLETE' rows
--   hold '[author surname pending ...]' in first_author_last, which the
--   blocking C03 check accepts as an author because the string is non-empty.
--
-- ALTER TABLE ADD COLUMN does not rebuild the table, so this is safe on
-- evidence_sources (88 columns, 9 inbound foreign keys) in a way that adding
-- a constraint would not be. NOT NULL with a default means no source can
-- exist without a state — the ambiguity cannot reappear for new rows.
--
-- Backfill of the two statuses from their detail tables is a DATA migration
-- (it must run after the data phase has loaded those tables).
--
-- Forward-only; user_version -> 40.

-- Has the source's data been captured into a table yet?
--   pending          — logged; nothing captured (the default, and the honest
--                      starting state for every existing row)
--   captured         — at least one row exists in a joinable evidence table
--   none-extractable — read in full; contains nothing this project extracts
--   deferred         — deliberately postponed; processing_blocked_reason set
ALTER TABLE evidence_sources ADD COLUMN data_capture_status TEXT NOT NULL
  DEFAULT 'pending'
  CHECK (data_capture_status IN ('pending','captured','none-extractable','deferred'));

-- Has THIS SOURCE been used as a citation-mining anchor (R2: backward through
-- its reference list, forward through works citing it)?
--   pending | mined | deferred | not-applicable
--
-- The column is named citation_mining_status, not mining_status, because
-- "mining" is overloaded in this project and the bare word is ambiguous.
-- Citation mining is anchor-driven DISCOVERY and is source-scoped, which is
-- why it can live here. Gap-driven mining is gap-scoped (gap_mining) and data
-- extraction is a different operation with a different output. The five
-- operations, their inputs, outputs, tables and logs are defined in
-- governance/pipeline-operations.md; do not add a column here whose meaning
-- is not pinned there.
--
-- Scope is policy, not data: project-standards RULE 2026-04-09 requires mining
-- for confirmed Tier 1-2. That scoping lives in the check, not in a default
-- here, so a tier reclassification does not silently rewrite history.
ALTER TABLE evidence_sources ADD COLUMN citation_mining_status TEXT NOT NULL
  DEFAULT 'pending'
  CHECK (citation_mining_status IN ('pending','mined','deferred','not-applicable'));

-- Coded reason a source is 'deferred' or 'none-extractable'. Controlled
-- vocabulary; NULL when neither status applies.
ALTER TABLE evidence_sources ADD COLUMN processing_blocked_reason TEXT
  CHECK (processing_blocked_reason IS NULL OR processing_blocked_reason IN (
    'no-full-text',        -- full text could not be obtained
    'paywalled',           -- access blocked by paywall
    'no-doi',              -- no resolvable identifier for automated paths
    'not-indexed',         -- absent from the indexes the pipeline queries
    'language',            -- awaiting in-language reading capacity
    'no-quantified-claims',-- read; carries no extractable value
    'superseded',          -- superseded by another source
    'out-of-scope',        -- outside the corpus this project extracts from
    'tier-not-required'    -- tier does not oblige the work
  ));
