-- Migration 0001 — jurisdiction hygiene (L0)
-- STATUS: PROPOSED, NOT APPLIED. Review before running. Migration-based write
-- (governance/migration-based-writes-adopted-2026-05-11.md). Reversible: see rollback note.
--
-- Rationale: evidence_sources.jurisdiction has 45 distinct values with coding seams that make the
-- per-slug equity coverage matrix uncountable. This normalizes only the DETERMINISTIC, safe cases and
-- leaves judgement cases as explicit TODOs — no jurisdiction is guessed.

BEGIN;

-- (1) Seam: INTL is a synonym for INT (international / supranational-global). 5 rows, all REF-VERIFIED-*.
--     EU is deliberately KEPT distinct (a real supranational jurisdiction, not "global").
UPDATE evidence_sources
   SET jurisdiction = 'INT',
       updated_at = updated_at            -- (session/audit columns set by the write tooling, not hard-coded)
 WHERE jurisdiction = 'INTL';
--     affects: REF-VERIFIED-003, -005, -006, -008, -010   (verify count = 5 after)

-- (2) Compound tag AU/NZ (REF-00574, AS/NZS 2107:2016). AS/NZS standards are genuinely joint AU+NZ, so
--     the compound is MEANINGFUL, not a seam. Decision: KEEP as 'AU/NZ' but document it as an intentional
--     joint-jurisdiction code so coverage-matrix logic treats it as {AU, NZ}. No row change here.

-- (3) 19 NULL/'' jurisdictions — NOT auto-assigned (would violate "never guess a jurisdiction", S3).
--     These are mostly the REF-007xx import block (712–725) plus REF-00150/00233/00240/00302/00571.
--     TODO (per-ref, during first batch): backfill from publisher / standard_number / institution where
--     determinable; tag 'INT' only where the source is genuinely trans-national; leave NULL where truly
--     unknown AND record that null is a deliberate "unknown", not a missing value.
--     Left as-is in this migration on purpose.

COMMIT;

-- Rollback: UPDATE evidence_sources SET jurisdiction='INTL' WHERE ref_id IN
--   ('REF-VERIFIED-003','REF-VERIFIED-005','REF-VERIFIED-006','REF-VERIFIED-008','REF-VERIFIED-010');
-- Verify after apply:
--   SELECT jurisdiction, COUNT(*) FROM evidence_sources WHERE jurisdiction IN ('INT','INTL','EU') GROUP BY 1;
--   -- expect INTL = 0, INT = 168+5 = 173, EU = 5
