-- data_20260523230900_pre_rehab_banner_evidence_state.sql
-- B.0 closure: set bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB' for
-- 68 unique slugs corresponding to 70 references/bpc/*.md files bearing positive
-- [OPUS-SYNTHESIS*] tags pre-dating the 2026-05-23 evidence-metadata rehabilitation.
-- Cohort defined by DR-2026-05-23. Manifest committed alongside in
-- decisions/DR-2026-05-23-cohort-manifest.json (frozen at HEAD b0a4a25).
-- Forward-only; banner removal is a per-slug Phase E.2g operation, not a global revert.

BEGIN TRANSACTION;

-- Guard: every slug below must exist in bpc_metadata. If not, the UPDATE is a no-op
-- for that slug and the row-count check at the end will flag it.

UPDATE bpc_metadata
   SET evidence_state = 'RETRACTED-PRE-REHAB',
       updated_at     = datetime('now'),
       updated_by_session = 'session_2026-05-23-bpc-rewrite-phase-b-closure'
 WHERE slug IN (
    'accessibility-feature-market-value-uplift-framing',
    'accessible-bathroom-and-grab-bar',
    'accessible-circulation-geometry',
    'accessible-design-economics-cost-premium',
    'accessible-laundry-room-design',
    'acoustics-speech-intelligibility-disability',
    'air-quality-voc-chemical-sensitivity-built-environment',
    'assistive-listening-systems',
    'bariatric-turning-radius-built-environment',
    'bathroom-typology-global-south',
    'biophilic-design-healthcare-workplace',
    'body-sizes-supplementary-populations',
    'circadian-lighting-melanopic-edi',
    'co1-housing-research-global-south',
    'cognitive-wayfinding-design',
    'cross-population-conflict-resolutions',
    'crpd-implementation-built-environment',
    'deaf-acoustic-built-environment',
    'deaf-classroom-reverberation-time',
    'deaf-spatial-design',
    'deafblind-built-environment-design',
    'dementia-built-environment',
    'design-framework-evidence-audit',
    'detectable-gradient-protocol-sensory-zones',
    'ecological-psychology-haptic-affordances-built-environment',
    'european-accessibility-act-scope-clarification',
    'floor-vibration-wheelchair-disability',
    'fold-down-grab-bar-specification',
    'government-grant-programmes-home-adaptation',
    'intellectual-disability-built-environment-design',
    'jurisdiction-grant-programmes-comprehensive',
    'jurisdiction-matrix-accessibility-standards',
    'luminance-contrast-lrv-evidence-base',
    'mental-health-built-environment',
    'mobility-built-environment',
    'ms-thermal-temperature-conflict-resolution',
    'multilingual-evidence-convergence-non-english',
    'ndv-aut-built-environment-quantified-thresholds',
    'neurodivergent-built-environment',
    'neurological-built-environment',
    'ofs-built-environment',
    'ot-built-environment-interface',
    'ot-cpg-built-environment',
    'ot-frameworks-built-environment',
    'pain-ofs-built-environment-design',
    'reach-range-and-accessible-controls',
    'residential-dar-provisions-priority-register',
    'residential-entry-and-threshold',
    'residential-kitchen-and-task-surfaces',
    'room-acoustic-performance',
    'sensory-processing-model-design-application',
    'sensory-relief-space-design',
    'sensory-room-user-control',
    'sensory-space-global-south',
    'stair-ramp-threshold-biomechanics-accessibility',
    'therapeutic-lighting-design',
    'thermal-comfort-older-adults-care-settings',
    'thermoregulation-built-environment',
    'threshold-and-level-access',
    'threshold-door-hardware',
    'upper-limb-impairment-built-environment',
    'visitability-residential-accessibility-minimum-standards',
    'visual-alerting-and-wayfinding-light',
    'visual-fire-alarm-seizure-safety',
    'visual-impairment-built-environment',
    'wayfinding-cognitive-science-spatial-design',
    'wayfinding-dementia-spatial-design',
    'wayfinding-global-south'
 )
  -- Idempotency: don't re-touch rows already in the target state.
  AND COALESCE(evidence_state, '') != 'RETRACTED-PRE-REHAB';

-- Sanity check: the 68 slugs in the cohort must all now hold the banner state.
-- (Migration runner does not auto-verify; the post-apply audit script does.)

COMMIT;
