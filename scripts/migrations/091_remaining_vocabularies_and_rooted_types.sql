-- 091_remaining_vocabularies_and_rooted_types.sql
--
-- THE FOUR SIBLINGS 089 LEFT BEHIND, AND A CURATED LIST INSIDE THE MIGRATION THAT WAS
-- MEANT TO RETIRE CURATED LISTS.
--
-- 089 moved `evidence_sources.source_type`'s vocabulary into the column's own CHECK and
-- retired the seventeen-value tuple that had been its only home. It did ONE column.
-- GAP-042 recorded the other four the same day and said, in its own text, "Doing the
-- remaining four in ONE migration is cheaper than four" and "NOT A BACKLOG ITEM TO AGE".
-- The session record argued proportionality; that argument does not survive contact with
-- what the rebuild actually costs. The 97-column rebuild, the drop-and-restore of five
-- dependent views, the AFTER_DATA boundary and a fresh binary blob are the price -- the
-- CHECK clause is four generated lines. Against that, a second rebuild later is a second
-- chance to lose a view (089's own first attempt aborted on exactly that), a second data
-- boundary, and a second binary conflict for every open PR touching the DB when the
-- scheduled source-verification run fires.
--
-- SO: verification_status, metadata_quality, doi_resolution_outcome and
-- url_resolution_outcome each get the vocabulary that until now existed only as a tuple
-- in scripts/tests/test_db_integrity.py. Every live value is already inside its set --
-- verified immediately before writing this -- so nothing on disk is invalidated and this
-- constrains future writes only. NULL stays legal on all four; `metadata_quality` also
-- admits the literal string 'NULL', which is a real stored value in this corpus and is
-- transcribed as it stands rather than tidied.
--
-- WHAT THIS BUYS BEYOND TIDINESS. dbcore.check_values reads the column's CHECK, so with
-- it declared: db.py's argparse refuses a bad value BEFORE the command runs, --help
-- renders the live set, amend-source's generic check_declared arms itself on all four,
-- and B01-B04 can read check_expression the way B05 and B06 now do. Four consumers, one
-- home, and the next session cannot copy a value out of a stale help string the way this
-- batch copied Crossref's `journal-article`.
--
-- AND THE VIEW ARM 090 HARD-CODED. Migration 090 gave v_unregistered_roots a `rootless`
-- arm listing three of root_type's five CHECK values by hand -- a curated vocabulary
-- written into the migration whose sibling was retiring curated vocabularies, in the same
-- commit. A sixth value minted later would land in neither arm, silently. It is rewritten
-- here in COMPLEMENT form, so the burden of proof sits on the exclusions and a new
-- vocabulary member is covered the day it is minted:
--
--   'untraced'            -- the vocabulary's own word for "the root is not known", so a
--                            row saying untraced and naming nothing is CONSISTENT, not
--                            defective. This is what extraction 57 was corrected TO.
--   'derived_calculation' -- its provenance is its derived_from edges, not a root row;
--                            add-extraction already requires those via --input-role.
--
-- AFTER_DATA: 20260920044950

DROP VIEW IF EXISTS v_determination_provenance;
DROP VIEW IF EXISTS v_evidence_authors;
DROP VIEW IF EXISTS v_item_provenance;
DROP VIEW IF EXISTS v_source_admission;
DROP VIEW IF EXISTS v_source_reach_all;

CREATE TABLE evidence_sources_new (
        ref_id                      TEXT PRIMARY KEY,
        source_type                 TEXT CHECK (source_type IS NULL OR source_type IN (
                                   'journal_article',
                                   'book',
                                   'book_chapter',
                                   'conference_paper',
                                   'thesis',
                                   'primary_research',
                                   'case_study',
                                   'standard',
                                   'guideline',
                                   'report',
                                   'grey',
                                   'internal',
                                   'letter',
                                   'editorial',
                                   'commentary',
                                   'other',
                                   'code'
                                 )),
        -- Author summary (denorm)
        author_count                INTEGER,
        author_count_is_complete    INTEGER DEFAULT 0,
        first_author_last           TEXT,
        first_author_first          TEXT,
        is_corporate_primary        INTEGER DEFAULT 0,
        author_display              TEXT,
        -- Date
        pub_year                    INTEGER,
        pub_year_note               TEXT,
        -- Title
        pub_title                   TEXT,
        pub_subtitle                TEXT,
        chapter_title               TEXT,
        original_title              TEXT,
        -- Language
        lang_detected               TEXT,
        lang_detection_method       TEXT,
        pub_title_en                TEXT,
        pub_subtitle_en             TEXT,
        chapter_title_en            TEXT,
        journal_name_en             TEXT,
        translation_method          TEXT,
        translation_reviewed        INTEGER DEFAULT 0,
        -- Journal
        journal_name                TEXT,
        journal_abbrev              TEXT,
        volume                      TEXT,
        issue                       TEXT,
        pages_start                 TEXT,
        pages_end                   TEXT,
        article_number              TEXT,
        -- Book/Report
        publisher                   TEXT,
        publisher_location          TEXT,
        edition                     TEXT,
        book_title                  TEXT,
        series                      TEXT,
        series_number               TEXT,
        report_number               TEXT,
        institution                 TEXT,
        -- Standard
        standard_number             TEXT,
        -- Identifiers
        doi                         TEXT,
        pmid                        TEXT,
        pmcid                       TEXT,
        isbn                        TEXT,
        issn                        TEXT,
        url                         TEXT,
        url_accessed                TEXT,
        handle                      TEXT,
        local_id                    TEXT,
        -- Evidence classification
        tier                        INTEGER,
        evidence_type               TEXT,
        jurisdiction                TEXT,
        co1_provenance              TEXT,
        co1_source_type             TEXT,
        synthesis_attribution_required INTEGER,
        -- Quality
        metadata_quality TEXT CHECK (metadata_quality IS NULL OR metadata_quality IN ('COMPLETE', 'AUTHOR-TITLE-ONLY', 'GREY', 'PMID-ONLY', 'NULL', 'COMPLETE-STATUTORY')),
        verification_status TEXT CHECK (verification_status IS NULL OR verification_status IN ('VERIFIED', 'UNVERIFIED')),
        doi_resolution_outcome TEXT CHECK (doi_resolution_outcome IS NULL OR doi_resolution_outcome IN ('RESOLVED', 'NO-MATCH', 'REVERTED')),
        bpc_shorthand               TEXT,
        bpc_note                    TEXT,
        grey_flag                   INTEGER DEFAULT 0,
        grey_reason                 TEXT,
        verification_note           TEXT,
        prior_expectation           TEXT,
        search_queries_used         TEXT,
        derivation_chain            TEXT,
        -- Notes / Audit
        notes                       TEXT,
        created_at                  TEXT,
        created_by_session          TEXT,
        updated_at                  TEXT,
        updated_by_session          TEXT
    , verified_by_tool TEXT, last_verified_at TEXT, verification_attempt_count INTEGER DEFAULT 0, superseded_by_ref_id TEXT, pages TEXT, pub_month INTEGER, language TEXT, subtype TEXT, citation_count INTEGER, url_resolution_outcome TEXT CHECK (url_resolution_outcome IS NULL OR url_resolution_outcome IN ('MATCHED', 'PARTIAL', 'NO-MATCH', 'DEAD-LINK', 'DEAD-DNS', 'WAYBACK-MATCH', 'WAYBACK-PARTIAL', 'URL-NO-MATCH', 'RESOLVED', 'DEAD', 'RESOLVED-PARTIAL')), url_last_fetched TEXT, url_match_similarity REAL, metadata_integrity_status TEXT, metadata_integrity_detail TEXT, code_currency_status TEXT, code_currency_verified_at TEXT, code_currency_verified_by_session TEXT, code_currency_notes TEXT, scope TEXT
  CHECK (scope IS NULL OR scope IN (
    'high_control', 'lower_control', 'national', 'international', 'intrinsic'
  )), data_capture_status TEXT NOT NULL
  DEFAULT 'pending'
  CHECK (data_capture_status IN ('pending','captured','none-extractable','deferred')), citation_mining_status TEXT NOT NULL
  DEFAULT 'pending'
  CHECK (citation_mining_status IN ('pending','mined','deferred','not-applicable')), processing_blocked_reason TEXT
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
  )), standard_number_note TEXT, author_display_note  TEXT, publisher_note       TEXT, verification_disposition TEXT
  CHECK (verification_disposition IS NULL
         OR verification_disposition IN ('OPEN','CLOSED')), verification_method TEXT
  CHECK (verification_method IS NULL OR verification_method IN (
    'direct-render',              -- the document was fetched and read
    'co1-attestation',            -- the attestation itself was obtained (DR 3.1)
    'corroborated-not-retrieved', -- >=2 independent retrievals agree; doc not obtained
    'citing-bibliography',        -- existence attested only by another work's references
    'tool'                        -- resolve_dois / verify_urls; verified_by_tool names which
  )), verification_closure_reason TEXT
  CHECK (verification_closure_reason IS NULL OR verification_closure_reason IN (
    'paywalled',
    'print-only',
    'access-denied-persistent',
    'withdrawn',
    'not-found-after-search',
    'disputed-existence'          -- owner ruling: there may be no resolution
  )));

INSERT INTO evidence_sources_new (
    "ref_id",
    "source_type",
    "author_count",
    "author_count_is_complete",
    "first_author_last",
    "first_author_first",
    "is_corporate_primary",
    "author_display",
    "pub_year",
    "pub_year_note",
    "pub_title",
    "pub_subtitle",
    "chapter_title",
    "original_title",
    "lang_detected",
    "lang_detection_method",
    "pub_title_en",
    "pub_subtitle_en",
    "chapter_title_en",
    "journal_name_en",
    "translation_method",
    "translation_reviewed",
    "journal_name",
    "journal_abbrev",
    "volume",
    "issue",
    "pages_start",
    "pages_end",
    "article_number",
    "publisher",
    "publisher_location",
    "edition",
    "book_title",
    "series",
    "series_number",
    "report_number",
    "institution",
    "standard_number",
    "doi",
    "pmid",
    "pmcid",
    "isbn",
    "issn",
    "url",
    "url_accessed",
    "handle",
    "local_id",
    "tier",
    "evidence_type",
    "jurisdiction",
    "co1_provenance",
    "co1_source_type",
    "synthesis_attribution_required",
    "metadata_quality",
    "verification_status",
    "doi_resolution_outcome",
    "bpc_shorthand",
    "bpc_note",
    "grey_flag",
    "grey_reason",
    "verification_note",
    "prior_expectation",
    "search_queries_used",
    "derivation_chain",
    "notes",
    "created_at",
    "created_by_session",
    "updated_at",
    "updated_by_session",
    "verified_by_tool",
    "last_verified_at",
    "verification_attempt_count",
    "superseded_by_ref_id",
    "pages",
    "pub_month",
    "language",
    "subtype",
    "citation_count",
    "url_resolution_outcome",
    "url_last_fetched",
    "url_match_similarity",
    "metadata_integrity_status",
    "metadata_integrity_detail",
    "code_currency_status",
    "code_currency_verified_at",
    "code_currency_verified_by_session",
    "code_currency_notes",
    "scope",
    "data_capture_status",
    "citation_mining_status",
    "processing_blocked_reason",
    "standard_number_note",
    "author_display_note",
    "publisher_note",
    "verification_disposition",
    "verification_method",
    "verification_closure_reason"
) SELECT
    "ref_id",
    "source_type",
    "author_count",
    "author_count_is_complete",
    "first_author_last",
    "first_author_first",
    "is_corporate_primary",
    "author_display",
    "pub_year",
    "pub_year_note",
    "pub_title",
    "pub_subtitle",
    "chapter_title",
    "original_title",
    "lang_detected",
    "lang_detection_method",
    "pub_title_en",
    "pub_subtitle_en",
    "chapter_title_en",
    "journal_name_en",
    "translation_method",
    "translation_reviewed",
    "journal_name",
    "journal_abbrev",
    "volume",
    "issue",
    "pages_start",
    "pages_end",
    "article_number",
    "publisher",
    "publisher_location",
    "edition",
    "book_title",
    "series",
    "series_number",
    "report_number",
    "institution",
    "standard_number",
    "doi",
    "pmid",
    "pmcid",
    "isbn",
    "issn",
    "url",
    "url_accessed",
    "handle",
    "local_id",
    "tier",
    "evidence_type",
    "jurisdiction",
    "co1_provenance",
    "co1_source_type",
    "synthesis_attribution_required",
    "metadata_quality",
    "verification_status",
    "doi_resolution_outcome",
    "bpc_shorthand",
    "bpc_note",
    "grey_flag",
    "grey_reason",
    "verification_note",
    "prior_expectation",
    "search_queries_used",
    "derivation_chain",
    "notes",
    "created_at",
    "created_by_session",
    "updated_at",
    "updated_by_session",
    "verified_by_tool",
    "last_verified_at",
    "verification_attempt_count",
    "superseded_by_ref_id",
    "pages",
    "pub_month",
    "language",
    "subtype",
    "citation_count",
    "url_resolution_outcome",
    "url_last_fetched",
    "url_match_similarity",
    "metadata_integrity_status",
    "metadata_integrity_detail",
    "code_currency_status",
    "code_currency_verified_at",
    "code_currency_verified_by_session",
    "code_currency_notes",
    "scope",
    "data_capture_status",
    "citation_mining_status",
    "processing_blocked_reason",
    "standard_number_note",
    "author_display_note",
    "publisher_note",
    "verification_disposition",
    "verification_method",
    "verification_closure_reason"
FROM evidence_sources;

DROP TABLE evidence_sources;
ALTER TABLE evidence_sources_new RENAME TO evidence_sources;

CREATE INDEX idx_evidence_sources_standing
  ON evidence_sources(verification_status, verification_disposition);

-- The five views, restored exactly as they stood before the rebuild.
CREATE VIEW v_determination_provenance AS
SELECT s.specification_id,
       s.parameter_id,
       t.canonical_en                AS parameter_name,
       s.state,
       COALESCE(s.identity_code, s.icf_code, s.needs_code, s.medical_code) AS lens,
       l.role,
       l.exclusion_reason,
       x.extraction_id,
       x.figure_role,
       x.comparator,
       x.claimed_value,
       x.claimed_unit,
       x.claim_text,
       x.ref_id,
       e.tier,
       e.evidence_type,
       e.verification_status
  FROM specifications s
  JOIN specification_extraction_links l ON l.specification_id = s.specification_id
  JOIN source_value_extractions       x ON x.extraction_id    = l.extraction_id
  JOIN base_parameters                p ON p.parameter_id     = s.parameter_id
  JOIN terms                          t ON t.term_id          = p.term_id
  LEFT JOIN evidence_sources          e ON e.ref_id           = x.ref_id
 WHERE s.retired_at IS NULL;

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

CREATE VIEW v_item_provenance AS
SELECT
    bp.parameter_id,
    t.canonical_en              AS parameter_name,
    t.domain                    AS parameter_domain,
    ecs.specification_id,
    COALESCE(ecs.identity_code, ecs.icf_code, ecs.needs_code, ecs.medical_code) AS lens_code,
    ecs.state                   AS cell_state,
    ecs.tier_basis,
    ecs.regulatory_stratum_only,
    csl.role                    AS source_role,
    es.ref_id,
    es.pub_title,
    -- POINTER, NOT COPY (migration 063). Was `es.author_display`, a writer-retired
    -- tombstone reading NULL. The authors have one home, evidence_source_authors, and
    -- v_evidence_authors renders it.
    va.author_display,
    es.pub_year,
    es.tier                     AS source_tier,
    es.evidence_type,
    es.verification_status,
    es.jurisdiction
FROM base_parameters bp
JOIN terms t                            ON t.term_id           = bp.term_id
JOIN "specifications" ecs               ON ecs.parameter_id    = bp.parameter_id
JOIN "specification_source_links" csl   ON csl.specification_id = ecs.specification_id
JOIN evidence_sources es                ON es.ref_id           = csl.ref_id
LEFT JOIN v_evidence_authors va         ON va.ref_id           = es.ref_id
WHERE ecs.retired_at IS NULL;

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

CREATE VIEW v_source_reach_all AS
SELECT
    es.ref_id,
    es.pub_title,
    es.tier                     AS source_tier,
    es.verification_status,
    CASE WHEN ecs.specification_id IS NULL THEN 0 ELSE 1 END AS reaches,
    ecs.specification_id,
    ecs.parameter_id,
    t.canonical_en              AS parameter_name,
    COALESCE(ecs.identity_code, ecs.icf_code, ecs.needs_code, ecs.medical_code) AS lens_code,
    ecs.state                   AS cell_state,
    (SELECT GROUP_CONCAT(ssl.slug, '; ')
       FROM source_slug_links ssl
      WHERE ssl.ref_id = es.ref_id)  AS admitted_under_slugs
FROM evidence_sources es
LEFT JOIN "specification_source_links" csl ON csl.ref_id = es.ref_id
-- THE PREDICATE IS IN THE JOIN, NOT A WHERE. See the header: a WHERE would delete the
-- source from this audit instead of showing that it now reaches nothing.
LEFT JOIN "specifications" ecs ON ecs.specification_id = csl.specification_id
                              AND ecs.retired_at IS NULL
LEFT JOIN base_parameters bp   ON bp.parameter_id = ecs.parameter_id
LEFT JOIN terms t              ON t.term_id       = bp.term_id;

-- v_unregistered_roots: the rooted-type list becomes a complement (see header).
DROP VIEW IF EXISTS v_unregistered_roots;

CREATE VIEW v_unregistered_roots AS
    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'unregistered' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NOT NULL
      AND sve.root_ref_id IS NULL
      AND NOT EXISTS (
          SELECT 1 FROM external_root_registry err
          WHERE err.root_id = sve.root_id)

    UNION ALL

    SELECT sve.extraction_id,
           sve.slug,
           sve.parameter_id,
           t.canonical_en AS parameter_label,
           sve.root_id,
           'rootless' AS defect
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_id IS NULL
      AND sve.root_ref_id IS NULL
      AND sve.root_type IS NOT NULL
      AND sve.root_type NOT IN ('untraced', 'derived_calculation');

PRAGMA user_version = 91;
