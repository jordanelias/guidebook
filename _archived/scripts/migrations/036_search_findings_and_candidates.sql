-- 036_search_findings_and_candidates.sql
-- Completes the search_executions logger: a place for substantive findings that are NOT
-- admissions, and a register for candidates that surface off-slug or unverified.
--
-- WHY (defects found by owner challenge, 2026-07-24):
--  1. search_executions had no findings field, so substantive non-admitted findings were being
--     written into `deferred_reason` — a field that semantically means "deliberately NOT
--     searched". Because v_coverage_* and v_coverage_priority filter on `deferred_reason IS
--     NULL`, six genuinely-searched cells were being counted as deferred. Data bug.
--  2. Evidence of FAILURE / HARM / INADEQUACY (e.g. tactile guiding blocks terminating at power
--     poles; accessible routes used for parking) had no first-class home, despite being
--     high-mission-value ("get people to ask the right questions") and despite an ACTIVE slug
--     `accessible-design-failures-poor-performance` existing with zero logged searches.
--  3. Candidates that surface but belong to a DIFFERENT slug, or are not yet locator-verified,
--     existed only in prose (commit messages / PR bodies) and were evaporating.
--
-- This EXTENDS the existing logger rather than spinning up a new register (CLAUDE.md §9
-- guardrail 3): findings_note/harm_finding are columns on search_executions, and
-- search_candidates is the logger's missing many-side (one search yields N candidates).
--
-- Schema-only, additive. The runner sets PRAGMA user_version to 36.

BEGIN;

-- 1. Substantive findings that are not admissions (incl. negative/failure findings).
ALTER TABLE search_executions ADD COLUMN findings_note TEXT;

-- 2. First-class flag: this search surfaced evidence of failure, harm, or inadequacy
--    (built environment performing badly / causing exclusion), not just design guidance.
ALTER TABLE search_executions ADD COLUMN harm_finding INTEGER NOT NULL DEFAULT 0;

-- 3. The candidate register — everything that surfaced but was not admitted, including
--    material whose best-fit slug is NOT the slug that was searched ("filed elsewhere"),
--    and material with no confident home yet ("miscellaneous").
CREATE TABLE search_candidates (
  candidate_id     INTEGER PRIMARY KEY,
  exec_id          INTEGER REFERENCES search_executions(exec_id),  -- which search surfaced it
  found_under_slug TEXT NOT NULL,        -- the slug being searched when it surfaced
  suggested_slug   TEXT,                 -- best-fit slug; NULL = MISCELLANEOUS / undecided
  disposition      TEXT NOT NULL CHECK (disposition IN
                     ('REHOME','MISCELLANEOUS','PENDING-VERIFICATION','OUT-OF-SCOPE','ADMITTED')),
  title            TEXT NOT NULL,
  locator          TEXT,                 -- DOI / URL / PMID as retrieved
  locator_status   TEXT CHECK (locator_status IS NULL OR locator_status IN
                     ('UNVERIFIED','RESOLVED','DEAD')),
  tier_guess       INTEGER CHECK (tier_guess IS NULL OR tier_guess BETWEEN 1 AND 6),
  harm_finding     INTEGER NOT NULL DEFAULT 0 CHECK (harm_finding IN (0,1)),
  why_not_admitted TEXT,                 -- required in practice: metadata gap, unverified, etc.
  notes            TEXT,
  session          TEXT NOT NULL,
  created_at       TEXT NOT NULL
) STRICT;
CREATE INDEX ix_sc_suggested ON search_candidates(suggested_slug, disposition);
CREATE INDEX ix_sc_harm ON search_candidates(harm_finding);

COMMIT;
