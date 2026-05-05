-- 001_initial_schema.sql
-- Guidebook data layer — Phase 1 schema
-- Spec: architecture/sqlite-data-layer.md v3
-- Created: see db_meta seed below

-- ============================================================
-- 4.1 db_meta — Schema Versioning
-- ============================================================

CREATE TABLE db_meta (
    key     TEXT PRIMARY KEY,
    value   TEXT NOT NULL
);

-- ============================================================
-- 4.2 connections + connection_targets
-- ============================================================

CREATE TABLE connections (
    con_id              TEXT PRIMARY KEY,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'
                        )),
    confidence          TEXT NOT NULL
                        CHECK(confidence IN ('HIGH','MODERATE','SPECULATIVE')),
    connection_type     TEXT
                        CHECK(connection_type IN (
                            'CROSS-POPULATION','CROSS-ITEM',
                            'COMPOUND-INTERACTION','METHODOLOGY'
                        )),
    filed_in            TEXT NOT NULL,
    description         TEXT,
    source_skill        TEXT,
    opus_reviewed       INTEGER NOT NULL DEFAULT 0 CHECK(opus_reviewed IN (0,1)),
    session_applied     TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE TABLE connection_targets (
    con_id              TEXT NOT NULL REFERENCES connections(con_id),
    target              TEXT NOT NULL,
    PRIMARY KEY (con_id, target)
);

CREATE INDEX idx_conn_status     ON connections(status);
CREATE INDEX idx_conn_confidence ON connections(confidence);
CREATE INDEX idx_conn_filed_in   ON connections(filed_in);
CREATE INDEX idx_ct_target       ON connection_targets(target);

-- ============================================================
-- 4.3 gaps
-- ============================================================

CREATE TABLE gaps (
    gap_id              TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'RP','SW','CR','ST','MX','CD','EC','EG'
                        )),
    priority            TEXT NOT NULL CHECK(priority IN ('P1','P2','P3')),
    status              TEXT NOT NULL
                        CHECK(status LIKE 'OPEN%' OR status LIKE 'CLOSED%'),
    skill               TEXT,
    section             TEXT,
    description         TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE INDEX idx_gap_priority_status ON gaps(priority, status);

-- ============================================================
-- 4.4 slugs + bpc_metadata
-- ============================================================

CREATE TABLE slugs (
    slug                TEXT PRIMARY KEY,
    topic_directory     TEXT NOT NULL,
    sl_path             TEXT NOT NULL,
    bpc_path            TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'ACTIVE','MERGED','STUB','PROVISIONAL'
                        )),
    merged_into         TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE TABLE bpc_metadata (
    slug                    TEXT PRIMARY KEY REFERENCES slugs(slug),
    population              TEXT NOT NULL,
    last_updated            TEXT,
    jurisdictions_searched  INTEGER DEFAULT 0,
    co1_pass_count          INTEGER DEFAULT 0,
    evidence_state          TEXT,
    pico_complete           INTEGER NOT NULL DEFAULT 0 CHECK(pico_complete IN (0,1)),
    search_complete         INTEGER NOT NULL DEFAULT 0 CHECK(search_complete IN (0,1)),
    bpc_complete            INTEGER NOT NULL DEFAULT 0 CHECK(bpc_complete IN (0,1)),
    citation_mining_complete INTEGER NOT NULL DEFAULT 0
                            CHECK(citation_mining_complete IN (0,1)),
    created_at              TEXT NOT NULL,
    created_by_session      TEXT NOT NULL,
    updated_at              TEXT NOT NULL,
    updated_by_session      TEXT NOT NULL
);

-- ============================================================
-- 4.5 evidence_sources + source_slug_links
-- ============================================================

CREATE TABLE evidence_sources (
    ref_id              TEXT PRIMARY KEY,
    authors             TEXT NOT NULL,
    year                TEXT,
    title               TEXT NOT NULL,
    doi                 TEXT,
    doi_less_key        TEXT,
    pmid                TEXT,
    tier                INTEGER CHECK(tier IS NULL OR tier BETWEEN 1 AND 6),
    evidence_type       TEXT,
    jurisdiction        TEXT,
    metadata_quality    TEXT
                        CHECK(metadata_quality IN (
                            'COMPLETE','PMID-ONLY','GREY','AUTHOR-TITLE-ONLY'
                        )),
    verification_status TEXT,
    co1_provenance      TEXT,
    co1_source_type     TEXT,
    synthesis_attribution_required INTEGER CHECK(
        synthesis_attribution_required IN (0,1)
    ),
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE TABLE source_slug_links (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (ref_id, slug)
);

CREATE INDEX idx_es_doi      ON evidence_sources(doi);
CREATE INDEX idx_es_tier     ON evidence_sources(tier);
CREATE INDEX idx_ssl_slug    ON source_slug_links(slug);
CREATE INDEX idx_ssl_ref     ON source_slug_links(ref_id);

-- ============================================================
-- 4.6 citation_mining
-- ============================================================

CREATE TABLE citation_mining (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    global_ref_id       TEXT REFERENCES evidence_sources(ref_id),
    doi                 TEXT,
    backward            INTEGER NOT NULL DEFAULT 0 CHECK(backward IN (0,1)),
    forward             INTEGER NOT NULL DEFAULT 0 CHECK(forward IN (0,1)),
    connections_produced TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (slug, local_ref_id)
);

CREATE INDEX idx_cm_unmined ON citation_mining(slug, backward, forward);

-- ============================================================
-- 4.7 search_coverage + search_languages
-- ============================================================

CREATE TABLE search_coverage (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    jurisdiction        TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN')),
    co1_attempted       INTEGER NOT NULL DEFAULT 0 CHECK(co1_attempted IN (0,1)),
    tier5_attempted     INTEGER NOT NULL DEFAULT 0 CHECK(tier5_attempted IN (0,1)),
    tier6_attempted     INTEGER NOT NULL DEFAULT 0 CHECK(tier6_attempted IN (0,1)),
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (slug, jurisdiction)
);

CREATE TABLE search_languages (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    language            TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN ('SEARCHED','PARTIAL','NOT-RUN')),
    results_count       INTEGER NOT NULL DEFAULT 0,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (slug, language)
);

-- ============================================================
-- 4.8 decisions
-- ============================================================

CREATE TABLE decisions (
    decision_id         TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES'
                        )),
    delegation          TEXT NOT NULL
                        CHECK(delegation IN ('DG-NON','DG-REVIEW','DG-AUTO')),
    delegation_rationale TEXT,
    summary             TEXT NOT NULL,
    outcome             TEXT NOT NULL,
    rationale           TEXT NOT NULL,
    decision_date       TEXT NOT NULL,
    decided_by          TEXT NOT NULL,
    model_routing       TEXT NOT NULL,
    effort_level        INTEGER NOT NULL,
    status              TEXT NOT NULL DEFAULT 'ACTIVE'
                        CHECK(status IN (
                            'ACTIVE','SUPERSEDED','WITHDRAWN','PROPOSED'
                        )),
    review_status       TEXT NOT NULL,
    supersedes          TEXT NOT NULL DEFAULT '[]',
    predecessors        TEXT NOT NULL DEFAULT '[]',
    decision_artifacts  TEXT NOT NULL DEFAULT '[]',
    alternatives_considered TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE INDEX idx_decision_status   ON decisions(status);
CREATE INDEX idx_decision_category ON decisions(category);

-- ============================================================
-- 4.9 terms + term_aliases + term_item_links
-- ============================================================

CREATE TABLE terms (
    term_id             TEXT PRIMARY KEY,
    canonical_en        TEXT NOT NULL,
    definition          TEXT,
    domain              TEXT,
    scope_note          TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE TABLE term_aliases (
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    alias               TEXT NOT NULL,
    language            TEXT NOT NULL DEFAULT 'EN',
    alias_type          TEXT NOT NULL
                        CHECK(alias_type IN (
                            'SYNONYM','TRANSLATION','NARROWER',
                            'BROADER','DEPRECATED','DOMAIN'
                        )),
    jurisdiction        TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (term_id, alias, language)
);

CREATE TABLE term_item_links (
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    item_code           TEXT NOT NULL,
    population          TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (term_id, item_code)
);

CREATE INDEX idx_ta_alias    ON term_aliases(alias);
CREATE INDEX idx_ta_language ON term_aliases(language);
CREATE INDEX idx_til_item    ON term_item_links(item_code);
