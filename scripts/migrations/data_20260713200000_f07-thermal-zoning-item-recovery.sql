-- data_20260713200000_f07-thermal-zoning-item-recovery.sql
-- Recovers item F-07 "Thermal Zoning" into the canonical `items` table.
--
-- Root cause: F-07 was drafted alongside F-06 and F-08 in the 2026-05-05
-- item-code audit session (all three marked "New item added in v10.0 per
-- item-code audit (session 2026-05-05)" in their source prose,
-- parts/88_to_90/part05-fg_v9-0_2026-03-20.md:204-260). F-06 and F-08 were
-- migrated into `items`; F-07 was not -- a drop, not a decision. Flagged as
-- a known gap in references/audits/item-code-audit-2026-05-05.md ("F-07
-- (Thermal Zoning) -- 7 connections reference this item. Not in Part 4.")
-- and confirmed still missing from the DB-generated parts/v10/part04.md as
-- of this migration. See workplan/ratification-execution-register-2026-07-13.md
-- "Contradiction sweep" item 3 / queue item Q17 for the full trace.
--
-- Scope: existence only. This migration registers the item's identity so it
-- is FK-valid and can be joined (item_population_links, item_bpc_links,
-- future evidence_cell_state rows). It does NOT insert any
-- evidence_cell_state row and does NOT assert a best-practice determination
-- -- F-07's two governing BPCs (ms-thermal-temperature-conflict-resolution,
-- thermal-comfort-older-adults-care-settings) are both RETRACTED-PRE-REHAB
-- (DR-2026-05-23 cohort) as of this migration; a determination is deferred
-- until they clear Phase E.2g reverification. Content and citations below
-- are drawn directly from the existing drafted source (v9.0 spec text,
-- 2026-03-20), not authored fresh by this migration.
--
-- item_bpc_links: two rows. CORRECTED (self-caught via the CI
-- migration-reproducibility gate, which rebuilds from migration history and
-- caught this before it ever reached the canonical DB): migration 013's
-- schema enforces AT MOST ONE link_type='primary' row per item_code
-- (idx_ibl_primary_per_item, a partial unique index) -- the original version
-- of this migration set both rows to 'primary' and would have failed on
-- apply. ms-thermal-temperature-conflict-resolution is 'primary' (the
-- item's namesake mechanism -- Uhthoff-phenomenon zoning is literally what
-- "Thermal Zoning" names, and it is listed first in the drafted source's own
-- BPC note); thermal-comfort-older-adults-care-settings is 'secondary' (a
-- related but distinct heat-shock-prevention concern per the same source
-- text). Both remain flagged RETRACTED-PRE-REHAB; the link_type choice is
-- about schema-required primacy ordering, not evidence weight.
--
-- item_population_links: parent-level population codes, matching the
-- existing convention used for F-08's own links (NEU not MS, OFS not its
-- POTS/CFS/MCAS sub-codes, applicability='applies', subtype='').

BEGIN;

INSERT INTO items (
    item_code, item_id, category, name, bpc_source_slug, status,
    created_at, created_by_session, updated_at, updated_by_session,
    pmp_delta_min, pmp_direction, pmp_last_walk_at, pmp_empirical_ceiling, pmp_gap_signed
) VALUES (
    'F-07', NULL, 'F', 'Thermal Zoning — Building-Wide Temperature Management', NULL, 'active',
    '2026-07-13 20:00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery',
    '2026-07-13 20:00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery',
    NULL, NULL, NULL, NULL, NULL
);

INSERT INTO item_bpc_links (item_code, slug, link_type, rationale, created_at, created_by_session) VALUES
    ('F-07', 'ms-thermal-temperature-conflict-resolution', 'primary',
     'Uhthoff-phenomenon cold-sensitivity mechanism (MS): ambient <=22C target -- the item namesake mechanism ("Thermal Zoning"), listed first in the drafted source''s own BPC note. BPC currently RETRACTED-PRE-REHAB; link records the governing relationship, not an evidence-state determination.',
     '2026-07-13T20:00:00+00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery'),
    ('F-07', 'thermal-comfort-older-adults-care-settings', 'secondary',
     'Heat-shock-mortality mechanism (DEM/older-adult): inter-room differential <=5C, bathroom pre-heating -- a related but distinct concern per the drafted source; schema (migration 013) permits only one primary link per item, so this is secondary by necessity, not by an evidence-weight judgment. BPC currently RETRACTED-PRE-REHAB; link records the governing relationship, not an evidence-state determination.',
     '2026-07-13T20:00:00+00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery');

INSERT INTO item_population_links (item_code, population_code, subtype, applicability, rationale_ref, created_at, created_by_session) VALUES
    ('F-07', 'NEU', '', 'applies', NULL, '2026-07-13T20:00:00+00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery'),
    ('F-07', 'OFS', '', 'applies', NULL, '2026-07-13T20:00:00+00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery'),
    ('F-07', 'DEM', '', 'applies', NULL, '2026-07-13T20:00:00+00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery'),
    ('F-07', 'PAIN', '', 'applies', NULL, '2026-07-13T20:00:00+00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery'),
    ('F-07', 'ALL', '', 'applies', NULL, '2026-07-13T20:00:00+00:00', 'session_2026-07-13-contradiction-sweep-f07-recovery');

COMMIT;
