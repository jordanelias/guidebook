-- 096_candidate_disposition_exhausted.sql
--
-- A DISPOSITION FOR "EXHAUSTED -- GIVEN UP ON FOR NOW", BY OWNER RULING 2026-09-25.
--
-- The owner ruled on 2026-09-25: "if we can't access something from anywhere then we
-- have to give up on it for now." Batch 20 applied that to candidates 109 (Walter 1971)
-- and 110 (the 1957 Illinois dissertation) and had nowhere to put it: the column's CHECK
-- offered REHOME, MISCELLANEOUS, PENDING-VERIFICATION, OUT-OF-SCOPE and ADMITTED, so both
-- rows said "exhausted, not queued for anyone" in prose while their typed disposition,
-- PENDING-VERIFICATION, told every sweep and every reader to go and verify them. The
-- prose and the column disagreed, and only the column is joinable -- the shape rule 8
-- exists to prevent. An independent adversarial pass on batch 20 raised it (finding
-- #15); the owner ruled the same day that a real, CHECK-permitted value be added.
--
-- WHAT IT MEANS, stated once here because the CHECK cannot carry prose: the item is
-- identified, and NO ROUTE to its text exists from anywhere this project can reach. It is
-- not OUT-OF-SCOPE (the item is on-topic) and not PENDING-VERIFICATION (nothing is pending).
-- "For now" is the owner's word: the value records a decision that can be revisited, not
-- a finding about the item. It is NOT for an item behind a possibly-transient barrier
-- (a bot check, a Cloudflare interstitial) that an ordinary browser gets past -- batch 20
-- left candidate 123 PENDING-VERIFICATION on exactly that distinction.
--
-- WHY A TABLE REBUILD. SQLite cannot alter a CHECK in place. The DDL below is the live
-- CREATE statement with one value added, generated from sqlite_master rather than
-- retyped (the lesson of migrations 089/091), and the table stays STRICT. Every live
-- disposition is inside the new set, so nothing on disk is invalidated. No view, trigger
-- or foreign key refers to search_candidates (verified against sqlite_master before
-- writing); its two indexes are recreated verbatim.
--
-- Consumers read the vocabulary from this CHECK (dbcore.check_values), so add-candidate
-- and resolve-candidate accept EXHAUSTED the moment this applies; no list in code
-- changes.

CREATE TABLE search_candidates_new (
  candidate_id     INTEGER PRIMARY KEY,
  exec_id          INTEGER REFERENCES search_executions(exec_id),  -- which search surfaced it
  found_under_slug TEXT NOT NULL REFERENCES slugs(slug),  -- the slug being searched when it surfaced
  suggested_slug   TEXT REFERENCES slugs(slug),  -- best-fit slug; NULL = MISCELLANEOUS / undecided
  disposition      TEXT NOT NULL CHECK (disposition IN
                     ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED',
                      'EXHAUSTED')),
  title            TEXT NOT NULL,
  locator          TEXT,                 -- DOI / URL / PMID as retrieved
  locator_status   TEXT CHECK (locator_status IS NULL OR locator_status IN
                     ('UNVERIFIED','RESOLVED','DEAD')),
  tier_guess       INTEGER CHECK (tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6),
  harm_finding     INTEGER NOT NULL DEFAULT 0 CHECK (harm_finding IN (0,1)),
  why_not_admitted TEXT,                 -- required in practice: metadata gap, unverified, etc.
  notes            TEXT,
  created_by_session          TEXT NOT NULL,
  created_at       TEXT NOT NULL
, resolved_ref_id TEXT REFERENCES evidence_sources(ref_id)) STRICT;

INSERT INTO search_candidates_new ("candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition", "title", "locator", "locator_status", "tier_guess", "harm_finding", "why_not_admitted", "notes", "created_by_session", "created_at", "resolved_ref_id")
    SELECT "candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition", "title", "locator", "locator_status", "tier_guess", "harm_finding", "why_not_admitted", "notes", "created_by_session", "created_at", "resolved_ref_id" FROM search_candidates;

DROP TABLE search_candidates;

ALTER TABLE search_candidates_new RENAME TO search_candidates;

CREATE INDEX ix_sc_suggested ON search_candidates(suggested_slug, disposition);
CREATE INDEX ix_sc_harm ON search_candidates(harm_finding);

PRAGMA user_version = 96;
