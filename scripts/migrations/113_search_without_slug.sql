-- 113_search_without_slug.sql
-- SCHEMA migration -- a search can be for a parameter, or for a source it mines, without naming a slug
-- (plan Phase 3 research; RULINGS R43). The owner's words are "any parameter regardless of search slug";
-- the scan contract (LED-195, LED-196, LED-201) makes the slug a guide to searching and no more; and the key
-- of a determination is parameter x lens, so a search aimed at a parameter had nowhere to say which one.
--
--   search_executions.slug              NOT NULL -> nullable
--   search_executions.parameter_id      NEW, nullable, REFERENCES base_parameters(parameter_id)
--   search_executions                   CHECK (COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL)
--   search_candidates.found_under_slug  NOT NULL -> nullable (the column stays: data migrations INSERT it)
--
-- The rows already logged keep their slugs: the CHECK holds for every one of them, and the copy below
-- would fail loudly if it did not.
--
-- SQLite cannot drop a NOT NULL, so both tables are rebuilt by migration 081's recipe, GENERATED from the
-- live DDL with three substitutions rather than retyped: build under a temporary name, copy by column
-- name, DROP the old, RENAME the new (so the inbound keys from search_candidates.exec_id,
-- search_admissions and search_execution_artefacts keep naming search_executions and resolve again at the
-- rename), recreate the indexes, then the views from their own stored SQL. The views come down first because
-- SQLite refuses a rename while a view is unresolvable: v_coverage_jurisdiction, v_coverage_language, v_coverage_branch, v_coverage_priority, v_source_admission, v_coverage_lens.
-- v_coverage_lens is recreated with parameter_id added to its select and grouping: left as it was, every slug-less
-- search would fall into one NULL-slug group and the parameter it was for would be invisible. The other five are verbatim.
-- Neither table is AUTOINCREMENT, so no sqlite_sequence row is carried:
--   select count(*) from sqlite_sequence where name in ('search_executions','search_candidates')  -> 0.
--
-- ORDER: the rebuild copies every row once, after every committed data migration has written theirs.
-- AFTER_DATA: 20261016003719

DROP VIEW "v_coverage_jurisdiction";
DROP VIEW "v_coverage_language";
DROP VIEW "v_coverage_branch";
DROP VIEW "v_coverage_priority";
DROP VIEW "v_source_admission";
DROP VIEW "v_coverage_lens";

-- search_executions
CREATE TABLE "_113_new_search_executions" (
  exec_id              INTEGER PRIMARY KEY,
  slug                 TEXT REFERENCES slugs(slug),   -- NULL when the search is for a parameter or mines a source (R43)
  parameter_id         INTEGER REFERENCES base_parameters(parameter_id),   -- the parameter a slug-less search was FOR (R43)
  jurisdiction         TEXT,                 -- NULL = jurisdiction-agnostic search
  language             TEXT NOT NULL,        -- ISO; one of the 19 research languages
  -- hierarchy branch the search TARGETED (diffable against what was FOUND):
  target_tier          INTEGER CHECK (target_tier IS NULL OR target_tier BETWEEN 1 AND 6),
  target_evidence_type TEXT CHECK (target_evidence_type IS NULL OR target_evidence_type IN
     ('clinical','sr_meta','standard_eb','national_fw','code','co1','co2','grey')),
  target_scope         TEXT CHECK (target_scope IS NULL OR target_scope IN
     ('intrinsic','lower_control','high_control','national','international')),
  -- the verbatim, replayable query:
  query_text           TEXT NOT NULL,
  terms_used           TEXT,                 -- JSON array of term ids
  engine               TEXT NOT NULL,        -- pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual
  -- depth as real method, not booleans:
  depth_method         TEXT NOT NULL CHECK (depth_method IN ('scoping','systematic')),
  mining_direction     TEXT CHECK (mining_direction IS NULL OR mining_direction IN
     ('none','backward','forward','both')),
  -- yield:
  results_found        INTEGER NOT NULL DEFAULT 0,
  results_screened     INTEGER NOT NULL DEFAULT 0,
  results_admitted     INTEGER NOT NULL DEFAULT 0,
  saturation_signal    TEXT CHECK (saturation_signal IS NULL OR saturation_signal IN
     ('none','partial','saturated')),
  admitted_ref_ids     TEXT,                 -- JSON array of evidence_sources.ref_id
  deferred_reason      TEXT,                 -- non-NULL => deliberate no-search for this cell
  backfill             INTEGER NOT NULL DEFAULT 0 CHECK (backfill IN (0,1)),
  created_by_session              TEXT NOT NULL,
  created_at          TEXT NOT NULL, findings_note TEXT, harm_finding INTEGER NOT NULL DEFAULT 0, prior_expectation TEXT, origin TEXT NOT NULL DEFAULT 'planned'
  CHECK (origin IN ('planned','incidental','adversarial-pass','owner-supplied','lead-index')), mined_ref_id TEXT REFERENCES evidence_sources(ref_id), origin_pass_id INTEGER
  REFERENCES adversarial_passes(pass_id) CHECK (origin_pass_id IS NULL OR origin = 'adversarial-pass'), updated_at TEXT, updated_by_session TEXT, identity_code TEXT REFERENCES populations(population_code), icf_code TEXT REFERENCES base_icf(icf_code), needs_code TEXT REFERENCES access_needs(need_code), medical_code TEXT REFERENCES base_taxonomy_medical(medical_code),        -- explicit ISO ts (deterministic under rebuild)
  CHECK (terms_used IS NULL OR json_valid(terms_used)),
  CHECK (admitted_ref_ids IS NULL OR json_valid(admitted_ref_ids)),
  CHECK (COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL)   -- a search says what it is for (R43)
) STRICT;
INSERT INTO "_113_new_search_executions" ("exec_id", "slug", "jurisdiction", "language", "target_tier", "target_evidence_type", "target_scope", "query_text", "terms_used", "engine", "depth_method", "mining_direction", "results_found", "results_screened", "results_admitted", "saturation_signal", "admitted_ref_ids", "deferred_reason", "backfill", "created_by_session", "created_at", "findings_note", "harm_finding", "prior_expectation", "origin", "mined_ref_id", "origin_pass_id", "updated_at", "updated_by_session", "identity_code", "icf_code", "needs_code", "medical_code")
  SELECT "exec_id", "slug", "jurisdiction", "language", "target_tier", "target_evidence_type", "target_scope", "query_text", "terms_used", "engine", "depth_method", "mining_direction", "results_found", "results_screened", "results_admitted", "saturation_signal", "admitted_ref_ids", "deferred_reason", "backfill", "created_by_session", "created_at", "findings_note", "harm_finding", "prior_expectation", "origin", "mined_ref_id", "origin_pass_id", "updated_at", "updated_by_session", "identity_code", "icf_code", "needs_code", "medical_code" FROM "search_executions";
DROP TABLE "search_executions";
ALTER TABLE "_113_new_search_executions" RENAME TO "search_executions";
CREATE INDEX ix_se_cell   ON search_executions(slug, jurisdiction, language);
CREATE INDEX ix_se_branch ON search_executions(target_tier, target_evidence_type, target_scope);

-- search_candidates
CREATE TABLE "_113_new_search_candidates" (
  candidate_id     INTEGER PRIMARY KEY,
  exec_id          INTEGER REFERENCES search_executions(exec_id),  -- which search surfaced it
  found_under_slug TEXT REFERENCES slugs(slug),  -- the slug being searched when it surfaced
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
, resolved_ref_id TEXT REFERENCES evidence_sources(ref_id), surfaced_in TEXT, surfaced_quote TEXT, updated_at TEXT, updated_by_session TEXT) STRICT;
INSERT INTO "_113_new_search_candidates" ("candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition", "title", "locator", "locator_status", "tier_guess", "harm_finding", "why_not_admitted", "notes", "created_by_session", "created_at", "resolved_ref_id", "surfaced_in", "surfaced_quote", "updated_at", "updated_by_session")
  SELECT "candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition", "title", "locator", "locator_status", "tier_guess", "harm_finding", "why_not_admitted", "notes", "created_by_session", "created_at", "resolved_ref_id", "surfaced_in", "surfaced_quote", "updated_at", "updated_by_session" FROM "search_candidates";
DROP TABLE "search_candidates";
ALTER TABLE "_113_new_search_candidates" RENAME TO "search_candidates";
CREATE INDEX ix_sc_suggested ON search_candidates(suggested_slug, disposition);
CREATE INDEX ix_sc_harm ON search_candidates(harm_finding);

-- The views, recreated verbatim from their own stored SQL.
CREATE VIEW v_coverage_jurisdiction AS
SELECT slug, jurisdiction,
       COUNT(*) AS searches, SUM(results_admitted) AS admitted,
       MAX(depth_method='systematic') AS reached_systematic,
       MAX(saturation_signal='saturated') AS saturated
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, jurisdiction;

CREATE VIEW v_coverage_language AS
SELECT slug, language, COUNT(*) AS searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY slug, language;

CREATE VIEW v_coverage_branch AS
SELECT slug, jurisdiction, target_tier, target_evidence_type, target_scope,
       COUNT(*) AS targeted_searches, SUM(results_admitted) AS admitted
FROM search_executions WHERE deferred_reason IS NULL
GROUP BY 1,2,3,4,5;

CREATE VIEW v_coverage_priority AS
SELECT
    s.slug,
    ljm.jurisdiction,
    ljm.language,
    ljm.role,
    ( (CASE ljm.role WHEN 'PRIMARY' THEN 3 ELSE 1 END)
      + (CASE WHEN (SELECT COUNT(*) FROM search_executions se2
                    WHERE se2.slug = s.slug AND se2.deferred_reason IS NULL) = 0
              THEN 2 ELSE 0 END)
    ) AS priority_score,
    (SELECT COUNT(*) FROM search_executions se3
     WHERE se3.slug = s.slug AND se3.deferred_reason IS NULL) AS slug_searches
FROM slugs s
JOIN lang_jur_map ljm            -- CROSS JOIN: every in-scope slug x every required (lang,jur)
WHERE s.status IN ('ACTIVE', 'STUB')
  AND NOT EXISTS (
      SELECT 1 FROM search_executions se
      WHERE se.slug = s.slug
        AND se.jurisdiction = ljm.jurisdiction
        AND se.language = ljm.language
  );

CREATE VIEW v_source_admission AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.verification_disposition,
    se.exec_id,
    se.slug                     AS admitted_under_slug,
    se.query_text,
    se.engine,
    se.language,
    se.jurisdiction             AS search_jurisdiction,
    se.depth_method,
    se.mining_direction,
    se.target_tier,
    se.backfill                 AS search_was_backfilled,
    se.created_by_session                  AS admitting_session,
    se.created_at              AS admitted_at,
    -- The research-stage prior, reached by pointer rather than copied onto the
    -- evidence row. This is what makes CHECK 7 answerable.
    se.prior_expectation
FROM evidence_sources es
JOIN search_admissions sa ON sa.ref_id  = es.ref_id
JOIN search_executions se ON se.exec_id = sa.exec_id;

CREATE VIEW v_coverage_lens AS
SELECT slug, parameter_id, jurisdiction, language, identity_code, icf_code, needs_code, medical_code,
       SUM(deferred_reason IS NULL) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
FROM search_executions GROUP BY 1, 2, 3, 4, 5, 6, 7, 8;

PRAGMA user_version = 113;
