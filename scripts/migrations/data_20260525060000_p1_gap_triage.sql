-- data_20260525060000_p1_gap_triage.sql
-- Triage of 9 open P1 gaps following Pass-3 cleanups (2026-05-25).
-- Outcomes per gap (after substantive content review):
--   GAP-265, GAP-266, GAP-269 — content-level fixes present in accessible-circulation-geometry.md
--     but BPC carries PRE-REHABILITATION RETRACTED flag pending Phase E.2g reverification per
--     DR-2026-05-23. Annotate; do NOT close until reverification clears the BPC.
--   GAP-268 — partial: 3 of 7 wayfinding/circulation BPCs now have meaningful DEAF coverage;
--     4 still invisible (cognitive-wayfinding-design ≈ token, wayfinding-cognitive-science-spatial-design,
--     luminance-contrast-and-pattern, detectable-gradient-protocol-sensory-zones, threshold-and-level-access).
--     Annotate with per-BPC status.
--   GAP-272 (geometry framing failure: turning circle vs swept envelope) — annotate; conceptual
--     reframing requires owner direction; intractable in a triage turn.
--   GAP-273 (tier numbering inconsistency) — annotate with database analysis showing the
--     inconsistency runs deeper than the SKILL file (sr_meta rows split between T2 and T3);
--     fix path documented; open new follow-up gap GAP-296.
--   GAP-274 (3 STUB BPCs cited as evidence basis in Part 4) — annotate; requires BPC content
--     work to resolve; not a triage-turn fix.
--   GAP-278 (Avandell-NJ fabrication) — fabrication confirmed and REMOVED from BPC inline at
--     2026-05-10 Pass 2B (lines 27, 41 of accessibility-feature-market-value-uplift-framing.md
--     explicitly document removal). CLOSE-FIXED.
--   GAP-283 (citation-miner integration) — annotate; architectural; requires the gap-driven
--     mining protocol decision; not a triage-turn fix.
--
-- Triage does NOT itself perform content work. The point is to record current state, separate
-- "already fixed" from "needs work", and surface what each unfixed gap actually requires.

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- ────────────────────────────────────────────────────────────────────────
-- 1. CLOSE GAP-278 (fabrication removed and documented inline)
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET status = 'CLOSED-FIXED',
       updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'CLOSED 2026-05-25: Avandell-NJ 60% premium fabrication confirmed and removed at 2026-05-10 Pass 2B. ' ||
         'Current state of references/bpc/economics/accessibility-feature-market-value-uplift-framing.md: ' ||
         'line 27 (NL row) states "US private-pay premium claim (Avandell) removed — fabrication"; line 41 ' ||
         '(Channel 3a) states "[REMOVED — CONFIRMED FABRICATION per BPC audit Pass 2B, 2026-05-10.] Prior ' ||
         'text cited Avandell NJ at $12,000/month vs US memory-care average ~$7,500/month — 60% revenue ' ||
         'premium. Verification found: Avandell is not operational (still in zoning review as of 2024); no ' ||
         'published pricing exists; the $12,000 figure has no primary source." The fabrication is no longer ' ||
         'in the BPC text. Channel 3a now correctly notes the empirical gap. RULE 2026-04-09 economics-BPC ' ||
         'fabrication pattern caught and documented.'
 WHERE gap_id = 'GAP-278';

-- ────────────────────────────────────────────────────────────────────────
-- 2. ANNOTATE GAP-265, GAP-266, GAP-269 (content fixes present; reverification-blocked)
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25: Content-level fix is present in accessible-circulation-geometry.md. Line 41 ' ||
         'now cites DSDG Bauman 2010 (Co-1), DeafScape Vaughn 2018 (Tier 2), and Cloete & Rout 2025 Acta ' ||
         'Structilia 32(2):238-263 (Tier 3 cross-cultural scoping review) and specifies 2440mm primary ' ||
         'corridors with glazed/transparent intersections. Line 56 "Most inclusive provision" sets 2440mm ' ||
         'primary mixed-population corridors. Gap is NOT closed because the BPC carries the ' ||
         'PRE-REHABILITATION RETRACTED flag pending Phase E.2g reverification per DR-2026-05-23. Close ' ||
         'on Phase E.2g clearance, not before.'
 WHERE gap_id = 'GAP-265';

UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25: Content-level fix is present in accessible-circulation-geometry.md line 42: ' ||
         '"Tier 3 swept-path evidence: Steinfeld 2006 RESNA reports 2400mm clear floor area to accommodate ' ||
         'IDEA + BS8300 entire-sample 180 turn — converges with the DEAF 2440mm primary. Different evidence ' ||
         'streams, same dimensional conclusion." This explicitly cites the entire-sample 180-degree turn ' ||
         'evidence that the gap flagged as missing. Gap is NOT closed because the BPC carries the ' ||
         'PRE-REHABILITATION RETRACTED flag pending Phase E.2g reverification per DR-2026-05-23.'
 WHERE gap_id = 'GAP-266';

UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25: The internal contradiction is resolved by population stratification in ' ||
         'accessible-circulation-geometry.md. Line 40: "Tier 5 standards values: 1800mm primary route ' ||
         'two-way passing ... Adequate where DEAF population is not anticipated and only wheelchair-passing ' ||
         'geometry governs." Line 41: "Tier Co-1 / Tier 2 / Tier 3 best practice (DEAF-inclusive primary ' ||
         'corridors): 2440mm primary corridors ... Required where signed conversation is anticipated." ' ||
         'Line 56 sets "Most inclusive provision: 2440mm corridor width on primary mixed-population routes." ' ||
         'Line 73 distinguishes code-consensus value (1800mm) from best practice (2440mm). The two values ' ||
         'are no longer contradictory but stratified by population. Gap NOT closed because the BPC carries ' ||
         'the PRE-REHABILITATION RETRACTED flag pending Phase E.2g reverification per DR-2026-05-23.'
 WHERE gap_id = 'GAP-269';

-- ────────────────────────────────────────────────────────────────────────
-- 3. ANNOTATE GAP-268 (partial: per-BPC DEAF-coverage scan)
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25 — per-BPC DEAF/signing/DSDG/Gallaudet/DeafScape reference scan across the ' ||
         'circulation + wayfinding cluster: accessible-circulation-geometry.md (6 refs, SUBSTANTIVE); ' ||
         'visual-alerting-and-wayfinding-light.md (3 refs, PARTIAL); cognitive-wayfinding-design.md ' ||
         '(1 ref, TOKEN); wayfinding-cognitive-science-spatial-design.md (0, INVISIBLE); ' ||
         'luminance-contrast-and-pattern.md (0, INVISIBLE); detectable-gradient-protocol-sensory-zones.md ' ||
         '(0, INVISIBLE); threshold-and-level-access.md (0, INVISIBLE). Scope reduced from "5 BPCs" at ' ||
         'original audit time to 4 BPCs still requiring DEAF-population integration. accessible-circulation-' ||
         'geometry.md substantively addressed but pending Phase E.2g reverification per DR-2026-05-23. The ' ||
         'remaining 4 invisible BPCs need explicit DEAF-population content sections that cite DSDG Bauman ' ||
         '2010 Co-1, DeafScape Vaughn 2018 Tier 2, and Cloete & Rout 2025 Tier 3 for the relevant parameter ' ||
         '(wayfinding-cognitive-science: cognitive wayfinding load + visual sightline; luminance-contrast: ' ||
         'high-contrast surrounds for signing visibility; detectable-gradient: DEAF-specific tactile/visual ' ||
         'redundancy; threshold-and-level-access: signing-group threshold geometry). Not a triage-turn fix.'
 WHERE gap_id = 'GAP-268';

-- ────────────────────────────────────────────────────────────────────────
-- 4. ANNOTATE GAP-272, GAP-274, GAP-283 (other open P1 — out of triage scope)
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25: Conceptual reframing — turning circle vs swept envelope is a measurement-' ||
         'methodology shift that needs to propagate across mobility-built-environment, accessible-' ||
         'circulation-geometry, bariatric-turning-radius, and any other BPC that references "turning ' ||
         'circle" as a parameter. Steinfeld 2006 figures are empirical swept paths, not idealised circles; ' ||
         'this matters because pivot-axis assumptions overestimate clear-floor adequacy for power-base ' ||
         'wheelchairs and scooters. Requires owner direction on whether to (a) deprecate "turning circle" ' ||
         'as a parameter name in favour of "swept envelope" / "manoeuvring footprint", or (b) keep both ' ||
         'and require dual-spec when divergent. Not a triage-turn fix.'
 WHERE gap_id = 'GAP-272';

UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25: Requires BPC content authorship on three STUB BPCs ' ||
         '(sensory-processing-model-design-application, sensory-relief-space-design, ' ||
         'upper-limb-impairment-built-environment) that are cited as evidence basis in Part 4. ' ||
         'Each STUB needs either substantive content authorship to make the Part 4 citations honest, ' ||
         'or the Part 4 citations need to be retracted. Not a triage-turn fix.'
 WHERE gap_id = 'GAP-274';

UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25: Architectural — citation-miner skill invocation pattern. Owner pivoted ' ||
         'B.11 from v1-eligible mining to gap-driven mining (session turn 14, 2026-05-23). Resolution ' ||
         'depends on the gap-driven mining protocol decision (open architectural question per ' ||
         'session record). Backlog of 163 T1-2 unmined remains; this gap is the architectural-level ' ||
         'symptom. Not a triage-turn fix.'
 WHERE gap_id = 'GAP-283';

-- ────────────────────────────────────────────────────────────────────────
-- 5. ANNOTATE GAP-273 + open follow-up GAP-296 (tier-system inconsistency)
-- ────────────────────────────────────────────────────────────────────────
UPDATE gaps
   SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure',
       description = description || char(10) || char(10) ||
         'TRIAGE 2026-05-25 — database-level scan of actual tier × evidence_type usage reveals the ' ||
         'inconsistency is deeper than the SKILL file. Canonical usage in evidence_sources table: ' ||
         'T1 = clinical primary + co1 (29 rows co1); T2 = standard_eb 53 + sr_meta 4 + co2 3; ' ||
         'T3 = clinical 175 + grey 20 + standard_eb 7 + sr_meta 4; T4 = standard_eb 63 + clinical 2; ' ||
         'T5 = national_fw 118 + standard_eb 3 + co1 1; T6 = code 89. The sr_meta rows are split ' ||
         'between T2 (4 rows) and T3 (4 rows) — the database itself does not have one canonical ' ||
         'tier for SR/meta-analysis. PI v10.14 line 138 implies T4 = international / T5 = national-' ||
         'recommended, matching database usage from T4 onward. guidebook-auditor SKILL section 4.1 ' ||
         'has SHIFTED tier definitions (T4 = SR, T5 = international standard, T6 = national beyond-' ||
         'code, T7 = statutory code) — offset by one from T4 onward and not matched in data. ' ||
         'Fix path requires: (a) create canonical tier-system definition document under governance/, ' ||
         '(b) decide canonical sr_meta placement (T2 alongside named-organization standards, OR T3 ' ||
         'alongside primary clinical work), (c) migrate misplaced evidence_sources rows, (d) update ' ||
         'guidebook-auditor SKILL section 4.1 to match. Follow-up GAP-296 opened to track. Not a ' ||
         'triage-turn fix.'
 WHERE gap_id = 'GAP-273';

INSERT INTO gaps (gap_id, category, priority, status, skill, section, description, created_at, created_by_session, updated_at, updated_by_session)
VALUES (
    'GAP-296',
    'AUDT',
    'P1',
    'OPEN',
    'doctrine-recheck',
    'governance/tier-system-canonical',
    'Tier-system reconciliation follow-up to GAP-273. Database has sr_meta rows split between Tier 2 (4 rows, alongside standard_eb 53 + co2 3) and Tier 3 (4 rows, alongside clinical 175 + grey 20). PI v10.14 line 138 names the tier system through T6 (T4 = international standard, T5 = national-recommended, T6 = statutory code implied). guidebook-auditor SKILL section 4.1 has a different system (T4 = SR/meta, T5 = international, T6 = national, T7 = statutory) — shifted by one from T4 onward. Required deliverables: (1) governance/tier-system.md canonical definition document defining T1 through T6 + Co-1 + Co-2 with explicit evidence_type mapping; (2) decision and migration on sr_meta placement (T2 or T3? — current PI line 138 reading suggests T2 because sr_meta + named-organization both encode community-consensus synthesis above primary studies but below international standards); (3) skills/guidebook-auditor_SKILL.md section 4.1 amended to match; (4) any BPCs using "[Tier X]" markers reconciled with the canonical system. Priority P1 because tier markers govern citation-claim mapping and downstream compliance with project-standards.',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure',
    strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
    'session_2026-05-23-bpc-rewrite-phase-b-closure'
);

COMMIT;
