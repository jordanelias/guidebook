-- data_20260525090000_chaikhot_2023_authorship_correction.sql
-- Completes REF-00736 to pass test_db_integrity.py check [C02] AND corrects
-- an authoring error in the prior migration data_20260525080000_manoeuvring_methodology_bpc.sql.
--
-- Prior migration recorded first_author_last='Vergara' and author_display='Vergara M,
-- van der Slikke RMA, et al.' from a misread PMC full-text snippet for PMID 37383064.
-- The correct authors per PubMed are:
--   1. Chaikhot, Dhissanuvach (Christian University of Thailand)
--   2. Taylor, Matthew J D (University of Essex)
--   3. de Vries, W H K (Swiss Paraplegic Research)
--   4. Hettinga, Florentina J (Northumbria University)
-- doi 10.3389/fspor.2023.1127514 is correct; PMC10293636 is correct; subject-matter
-- content of the BPC (97% spin-turn dominance, 15.3× braking force, etc.) is correct
-- — only the author attribution was wrong.
--
-- The scheduled source-verification job (run 2026-05-25 09:45 at commit 5007ede)
-- already populated the correct evidence_source_authors rows from PubMed XML.
-- This migration therefore: (1) sets doi_resolution_outcome=RESOLVED on REF-00736;
-- (2) corrects first_author_last + first_author_first + author_display on the
-- evidence_sources row; (3) marks author_count as complete.
-- The methodology BPC text is corrected in the same commit (no SQL needed).

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- 1. Set doi_resolution_outcome = RESOLVED (DOI verified via PubMed)
UPDATE evidence_sources
   SET doi_resolution_outcome = 'RESOLVED',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE ref_id = 'REF-00736'
   AND doi_resolution_outcome IS NULL;

-- 2. Correct author attribution
UPDATE evidence_sources
   SET first_author_last = 'Chaikhot',
       first_author_first = 'Dhissanuvach',
       author_display = 'Chaikhot D, Taylor MJD, de Vries WHK, Hettinga FJ',
       author_count = 4,
       author_count_is_complete = 1,
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       notes = COALESCE(notes, '') || char(10) || char(10) ||
         'AUTHORSHIP CORRECTION (2026-05-25): The prior migration data_20260525080000 recorded ' ||
         'first_author_last=''Vergara'' and author_display=''Vergara M, van der Slikke RMA, et al.'' ' ||
         'based on a misread of the PMC10293636 full-text snippet. Per PubMed PMID 37383064 the ' ||
         'correct authors are: Chaikhot D (first author, Christian University of Thailand), ' ||
         'Taylor MJD (University of Essex), de Vries WHK (Swiss Paraplegic Research), ' ||
         'Hettinga FJ (Northumbria University). Subject-matter content (97% spin-turn dominance, ' ||
         '15.3× braking force, n=10) is unchanged and correct. Methodology BPC corrected in ' ||
         'same commit.'
 WHERE ref_id = 'REF-00736';

COMMIT;
