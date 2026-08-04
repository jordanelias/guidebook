-- 049_verification_standing_columns.sql
-- SCHEMA migration — split verification into the columns D-0157 ratified.
--
-- Implements decisions/DR-2026-08-04-verification-status-is-a-standing-not-a-history.md
-- (ADOPTED by owner directive 2026-08-04). This migration adds the columns; the
-- data migration that follows remaps 863 rows onto them, and the same commit
-- updates the two weekly jobs that write this column, per DR §5.1.
--
-- WHAT WAS WRONG
-- `verification_status` encoded three orthogonal facts at once: what is
-- established, how it was established, and how hard anyone tried. The evidence
-- that this is not a stylistic complaint: `UNVERIFIED-1` claims one search
-- attempt while 25 of its 31 rows have `verification_attempt_count = 0`, and
-- the meaning governance documents for the suffix is not the meaning the
-- project owner inferred reading it cold. An encoding both ambiguous and
-- contradicted by its own dedicated column.
--
-- This is the same conflation migration 041 ended for author_display,
-- publisher and standard_number, in 041's words: "A column must hold one
-- domain."
--
-- THE COLUMNS
--   verification_disposition   is more effort owed?      OPEN | CLOSED
--   verification_method        how was it established?
--   verification_closure_reason  why did it stop?        (CLOSED only)
-- plus the pre-existing verification_attempt_count, which becomes the third
-- column of the set rather than a fact duplicated in the status string.
--
-- `verification_status` itself is NOT altered here. Its CHECK-less TEXT shape
-- stays, the data migration narrows its values to {VERIFIED, UNVERIFIED}, and
-- test_db_integrity's B01 becomes the enforcer. Adding a CHECK constraint would
-- require a table rebuild of 94 columns -- migration 039's header warns that
-- hand-copying such a definition "is how a rebuild silently changes a type,
-- default, or CHECK" -- for an invariant a registered check already covers.
--
-- CO-1 IS ACCOMMODATED, NOT DEMOTED
-- `co1-attestation` is a first-class method (DR §3.1). Read literally, the
-- definition of VERIFIED -- the document itself was obtained -- would have
-- demoted all 41 rows carrying verified_by_tool='co1-manual-pre-pipeline',
-- which are co-primary with T1 under CRPD Art. 4.3. For a Co-1 source the
-- artefact obtained is the attestation. Same standard, different artefact.
--
-- TIMESTAMPS
-- No column here carries `DEFAULT (datetime('now'))`. That default is why a
-- rebuilt database cannot be byte-compared against the committed one.
--
-- Forward-only; user_version -> 49.

ALTER TABLE evidence_sources ADD COLUMN verification_disposition TEXT
  CHECK (verification_disposition IS NULL
         OR verification_disposition IN ('OPEN','CLOSED'));

ALTER TABLE evidence_sources ADD COLUMN verification_method TEXT
  CHECK (verification_method IS NULL OR verification_method IN (
    'direct-render',              -- the document was fetched and read
    'co1-attestation',            -- the attestation itself was obtained (DR 3.1)
    'corroborated-not-retrieved', -- >=2 independent retrievals agree; doc not obtained
    'citing-bibliography',        -- existence attested only by another work's references
    'tool'                        -- resolve_dois / verify_urls; verified_by_tool names which
  ));

-- Its own column rather than reusing processing_blocked_reason, whose
-- CHECK vocabulary (migration 040) belongs to data capture and mining
-- deferral and excludes three of the five reasons below. Reusing it would have
-- reproduced the exact one-column-two-domains failure this DR diagnoses.
ALTER TABLE evidence_sources ADD COLUMN verification_closure_reason TEXT
  CHECK (verification_closure_reason IS NULL OR verification_closure_reason IN (
    'paywalled',
    'print-only',
    'access-denied-persistent',
    'withdrawn',
    'not-found-after-search',
    'disputed-existence'          -- owner ruling: there may be no resolution
  ));

CREATE INDEX IF NOT EXISTS idx_evidence_sources_standing
  ON evidence_sources(verification_status, verification_disposition);
