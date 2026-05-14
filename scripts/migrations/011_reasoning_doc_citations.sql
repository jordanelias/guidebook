-- 011_reasoning_doc_citations.sql
-- Create the `reasoning_doc_citations` table that records per-cell content
-- verification of claims in BPC reasoning documents. Supports the sharpened
-- standing rule #10 sub-rules 2 (jurisdiction-comparison cells) and 3
-- (qualitative/definitional claims). PMP (rule #8) continues to handle
-- numerical-spec claims via `spec_value_probes`.
--
-- Track 3 of DR-2026-05-13 (session_2026-05-13b).
--
-- schema_version → 11

CREATE TABLE reasoning_doc_citations (
    citation_id          TEXT PRIMARY KEY,
    reasoning_doc_slug   TEXT NOT NULL,
    parameter            TEXT NOT NULL,
    jurisdiction         TEXT,
    population           TEXT,
    claim_type           TEXT NOT NULL CHECK(claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )),
    claimed_value        TEXT,
    claimed_unit         TEXT,
    claim_text           TEXT,
    source_ref_id        TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    source_section       TEXT,
    value_match          TEXT CHECK(value_match IN (
        'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED'
    )),
    claim_match          TEXT CHECK(claim_match IN (
        'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED'
    )),
    verified_at          TEXT NOT NULL,
    verified_by_session  TEXT NOT NULL,
    paywall_purchase_candidate INTEGER NOT NULL DEFAULT 0 CHECK(paywall_purchase_candidate IN (0,1)),
    notes                TEXT,
    CHECK (
      (claim_type IN ('numerical_spec','jurisdiction_value') AND claimed_value IS NOT NULL AND value_match IS NOT NULL) OR
      (claim_type IN ('qualitative','definitional') AND claim_text IS NOT NULL AND claim_match IS NOT NULL)
    )
);

CREATE INDEX idx_rdc_slug_param ON reasoning_doc_citations(reasoning_doc_slug, parameter);
CREATE INDEX idx_rdc_ref        ON reasoning_doc_citations(source_ref_id);
CREATE INDEX idx_rdc_claim_type ON reasoning_doc_citations(claim_type);
CREATE INDEX idx_rdc_paywall    ON reasoning_doc_citations(paywall_purchase_candidate) WHERE paywall_purchase_candidate = 1;
