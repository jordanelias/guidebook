-- data_20260525070000_sr_meta_t2_canonicalization.sql
-- Closes GAP-273 and GAP-296 per owner directive 2026-05-25 "t2>t3 this is enshrined".
-- Migrates 4 sr_meta rows from Tier 3 to Tier 2; closes both gaps; updates the
-- accompanying canonical document at governance/tier-system.md (file-level change,
-- not in this migration).
--
-- Rows being migrated:
--   REF-00700 (None 2022, "Les espaces Snoezelen", doi 10.1684/med.2022.792)
--   REF-00701 (None 2025, "Effectiveness of sensory integration-based intervention", doi 10.3389/fpsyt.2025.1623149)
--   REF-00702 (Korean OT researchers 2022, "Sensory Integration Interventions", doi 10.18064/jkasi.2022.20.3.48)
--   REF-00704 (Lotan 2009, "Meta-analysis of Snoezelen", doi 10.1080/13668250903080106)
--
-- After this migration: 0 sr_meta rows at T3; 8 sr_meta rows at T2.

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- ────────────────────────────────────────────────────────────────────────
-- 1. Migrate the 4 sr_meta rows from T3 to T2
-- ────────────────────────────────────────────────────────────────────────
UPDATE evidence_sources
   SET tier = 2,
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
 WHERE evidence_type = 'sr_meta'
   AND tier = 3
   AND ref_id IN ('REF-00700', 'REF-00701', 'REF-00702', 'REF-00704');

-- ────────────────────────────────────────────────────────────────────────
-- 2. Close GAP-273 (tier numbering inconsistency)
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET status = 'CLOSED-FIXED',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'CLOSED 2026-05-25 per owner directive "t2>t3 this is enshrined". Canonical decision: ' ||
         'sr_meta sits at Tier 2 alongside named-organisation evidence-based standards. The 4 sr_meta ' ||
         'rows previously at T3 (REF-00700, REF-00701, REF-00702, REF-00704) migrated to T2 in this ' ||
         'migration. Canonical tier-system document authored at governance/tier-system.md. ' ||
         'guidebook-auditor SKILL section 4.1 amended to match. Reasoning recorded in governance/' ||
         'tier-system.md section 2: PI v10.14 line 138 reading (rule #9 step 5 enumerates "Tier 2 / ' ||
         'Co-2 / Tier 3" naturally positioning T2 as synthesis above T3 primary clinical work) + ' ||
         'evidence-type homology (T2 already houses standard_eb synthesis from named DPOs / pro bodies) ' ||
         '+ citation behaviour (SR-as-warrant-source must rank above primary-clinical-as-input) + ' ||
         'GRADE alignment (SR/meta-analysis sits at top of evidence-quality hierarchy).'
 WHERE gap_id = 'GAP-273';

-- ────────────────────────────────────────────────────────────────────────
-- 3. Close GAP-296 (tier-system reconciliation follow-up — same closure)
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET status = 'CLOSED-FIXED',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'CLOSED 2026-05-25 in lock-step with GAP-273. All four deliverables enumerated in the original ' ||
         'gap description satisfied: (1) governance/tier-system.md canonical document authored; ' ||
         '(2) sr_meta canonical placement decided as T2 per owner directive; (3) 4 misplaced T3 sr_meta ' ||
         'rows migrated to T2 in this migration; (4) skills/guidebook-auditor_SKILL.md section 4.1 ' ||
         'amended to match.'
 WHERE gap_id = 'GAP-296';

COMMIT;
