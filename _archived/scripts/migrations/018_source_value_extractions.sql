-- 018_source_value_extractions.sql
-- Schema migration: adds the per-source extracted-value layer.
--
-- Per DR-2026-05-28-b-source-value-extractions-schema. The existing chain
-- has a bare-link layer (source_slug_links: "source X is relevant to topic Y")
-- and a synthesis-verification layer (reasoning_doc_citations: "re-read
-- confirms value_match=EXACT for parameter/jurisdiction/population"). The
-- in-between unit of work — "this source asserts value X for parameter P,
-- population Q" — has no schema home, which makes the spread of asserted
-- values across linked sources invisible until full synthesis.
--
-- This migration adds source_value_extractions as the missing layer.
-- It is append-friendly (no UNIQUE on the natural key), mirroring
-- supersession_check (DR-2026-05-24) and gap_mining (DR-2026-05-26).
-- Operative row per (ref_id, slug, parameter, population, jurisdiction)
-- is determined by application code: most recent verified, else most recent.
--
-- An extraction graduates to the synthesis-gate layer by setting
-- promoted_to_rdc_id to a reasoning_doc_citations.citation_id; rule #10
-- sub-rules 2/3 remain the synthesis gate, unchanged.

BEGIN;

CREATE TABLE source_value_extractions (
  extraction_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  ref_id                 TEXT NOT NULL,
  slug                   TEXT NOT NULL,
  parameter              TEXT NOT NULL,
  parameter_canonical    TEXT,
  population_code        TEXT,
  population_label       TEXT,
  jurisdiction           TEXT,
  claim_type             TEXT NOT NULL
                           CHECK (claim_type IN ('numerical','range','qualitative','framework','absent')),
  claimed_value          TEXT,
  claimed_unit           TEXT,
  claim_text             TEXT,
  source_section         TEXT,
  extraction_method      TEXT NOT NULL
                           CHECK (extraction_method IN ('skim','full-read','re-read','auto-mined')),
  extraction_status      TEXT NOT NULL DEFAULT 'preliminary'
                           CHECK (extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed')),
  promoted_to_rdc_id     TEXT,
  notes                  TEXT,
  created_at             TEXT NOT NULL,
  created_by_session     TEXT,
  updated_at             TEXT NOT NULL,
  updated_by_session     TEXT,

  FOREIGN KEY (ref_id) REFERENCES evidence_sources(ref_id),
  FOREIGN KEY (population_code) REFERENCES populations(population_code),
  FOREIGN KEY (promoted_to_rdc_id) REFERENCES reasoning_doc_citations(citation_id),

  -- Soft consistency: if claim_type='absent', claimed_value must be NULL
  --                  if claim_type!='absent', claimed_value must NOT be NULL
  CHECK (
    (claim_type =  'absent' AND claimed_value IS NULL) OR
    (claim_type <> 'absent' AND claimed_value IS NOT NULL)
  )
);

CREATE INDEX idx_sve_slug_param ON source_value_extractions(slug, parameter_canonical);
CREATE INDEX idx_sve_ref        ON source_value_extractions(ref_id);
CREATE INDEX idx_sve_status     ON source_value_extractions(extraction_status);

COMMIT;
