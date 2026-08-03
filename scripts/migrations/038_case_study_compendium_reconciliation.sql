-- 038_case_study_compendium_reconciliation.sql
-- Reconcile migration 037's case_studies table against the PRIOR WORK it should have been built
-- from: references/case-study-compendium.md (its own "## Schema" block + 26 existing entries).
-- Closes DR-2026-07-25 §6.1 / register D-0155 NEEDS-RECONCILIATION.
--
-- WHAT THE RECONCILIATION FOUND (037 was built from schemas/case_study.py alone):
--
--  1. ID FORMAT. The compendium schema says `id — CS-NN sequential` and holds CS-01..CS-26.
--     schemas/case_study.py demanded CS-NNNN (4-digit). THE PRIOR WORK WINS: it is the actual
--     corpus. The Pydantic validator is widened to CS-\d{2,4} in the same commit; no existing
--     identifier is renumbered (renumbering 26 entries to satisfy a model that never had a table
--     would be the tail wagging the dog, and would break every §13.x cross-reference).
--
--  2. MISSING FIELDS — the substantive finding. 037 modelled the descriptive half and omitted the
--     compendium's ENTIRE financial block plus its failure/conflict fields. Notably the compendium
--     already carried `failure_notes` and `conflict_documented` — i.e. the prior work had first-
--     class homes for failure evidence and cross-population conflict before this session
--     "discovered" the need for them. Added here:
--       design_intent, populations_served_note, outcome_data, conflict_documented, failure_notes,
--       construction_cost, accessible_design_premium, funding_sources, operational_cost_change,
--       remediation_cost, roi_data, financial_evidence_tier, financial_data_quality,
--       evidence_contribution, part13_status, sources
--
--  3. PART NUMBERING. Not a contradiction: case studies were §13.01–§13.14 in v9.0 and are
--     parts/v10/part12.md ("# Case Studies") in v10. `part_section` stays free text and now has a
--     sibling `part13_status` matching the compendium's own IN/CANDIDATE/EXCLUDED vocabulary.
--
-- financial_data_quality reuses the compendium's exact flags (VERIFIED/PROVISIONAL/GREY), which
-- match the existing cost_data_quality CHECK from 037.
--
-- Additive only; the table is still empty, so no backfill is required. Runner sets user_version 38.

BEGIN;

ALTER TABLE case_studies ADD COLUMN design_intent TEXT;              -- explicit multi-population / UD / single-pop
ALTER TABLE case_studies ADD COLUMN populations_served_note TEXT;    -- prose; codes live in case_study_populations
ALTER TABLE case_studies ADD COLUMN outcome_data TEXT;               -- POE findings with source and tier
ALTER TABLE case_studies ADD COLUMN conflict_documented TEXT;        -- YES/NO + description (cross-population conflict)
ALTER TABLE case_studies ADD COLUMN failure_notes TEXT;              -- failures, retrofits, complaints, litigation
ALTER TABLE case_studies ADD COLUMN construction_cost TEXT;          -- total or per-m2, currency, year, quality flag
ALTER TABLE case_studies ADD COLUMN accessible_design_premium TEXT;  -- % of project cost if isolated
ALTER TABLE case_studies ADD COLUMN funding_sources TEXT;
ALTER TABLE case_studies ADD COLUMN operational_cost_change TEXT;
ALTER TABLE case_studies ADD COLUMN remediation_cost TEXT;
ALTER TABLE case_studies ADD COLUMN roi_data TEXT;
ALTER TABLE case_studies ADD COLUMN financial_evidence_tier INTEGER;
ALTER TABLE case_studies ADD COLUMN financial_data_quality TEXT;     -- VERIFIED / PROVISIONAL / GREY
ALTER TABLE case_studies ADD COLUMN evidence_contribution TEXT;      -- how it contributes to the evidence base
ALTER TABLE case_studies ADD COLUMN part13_status TEXT;              -- IN / CANDIDATE / EXCLUDED
ALTER TABLE case_studies ADD COLUMN sources TEXT;

COMMIT;
