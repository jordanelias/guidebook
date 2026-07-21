-- ============================================================================
-- STAGED — DO NOT APPLY BEFORE RATIFICATION OF
-- decisions/DR-2026-07-21-two-layer-functional-taxonomy.md
-- Deliberately located in working/taxonomy/ (NOT scripts/migrations/) so that
-- `db.py migrate` cannot pick it up. On ratification: move into
-- scripts/migrations/ with an apply-time timestamp prefix and record in
-- data_migrations per migration-based-writes doctrine.
-- Source doctrine: governance/functional-taxonomy.md (PROPOSED)
-- ============================================================================

BEGIN TRANSACTION;

-- ---------------------------------------------------------------------------
-- Layer 1: functional axes
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS axes (
  axis_code        TEXT PRIMARY KEY,               -- 'AX-BAL'
  name             TEXT NOT NULL,
  icf_b_anchors    TEXT,                           -- CSV of ICF body-function codes
  icf_d_anchors    TEXT,                           -- CSV of ICF activity codes
  mechanism        TEXT NOT NULL,
  design_domains   TEXT,                           -- indicative item families
  coverage_status  TEXT NOT NULL CHECK (coverage_status IN ('ESTABLISHED','PARTIAL','STUB')),
  falsification_condition TEXT,
  notes            TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
);

-- ---------------------------------------------------------------------------
-- Disposition of population codes (existing + newly admitted profiles)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS population_reclass (
  population_code  TEXT PRIMARY KEY,
  row_kind         TEXT NOT NULL CHECK (row_kind IN ('EXISTING-POP','NEW-PROFILE')),
  layer            TEXT NOT NULL CHECK (layer IN ('AXIS-ALIAS','PROFILE','QUALIFIER','SPLIT')),
  profile_kind     TEXT CHECK (profile_kind IN
                     ('diagnostic','identity-cultural','demographic','anthropometric','compound','umbrella')),
  icd11_anchor     TEXT,                           -- only where verified; else 'TO-VERIFY' or NULL by design
  parent_correction TEXT,
  fluctuating      TEXT CHECK (fluctuating IN ('yes','no') OR fluctuating IS NULL),
  emergent_corpus  TEXT,                           -- pointer to the authored corpus, if any
  rationale        TEXT NOT NULL,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
);

-- ---------------------------------------------------------------------------
-- Population/profile -> axis weighted mapping
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS population_axis_map (
  population_code  TEXT NOT NULL,
  axis_code        TEXT NOT NULL REFERENCES axes(axis_code),
  role             TEXT NOT NULL CHECK (role IN ('ALIAS','PRIMARY','SECONDARY','SITUATIONAL')),
  note             TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (population_code, axis_code)
);

-- ---------------------------------------------------------------------------
-- Item -> axis mechanism linkage (seeded later by FDA-brief harvest; §9 step 3)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS item_axis_links (
  item_code        TEXT NOT NULL,
  axis_code        TEXT NOT NULL REFERENCES axes(axis_code),
  mechanism_note   TEXT,
  strength_band    TEXT CHECK (strength_band IN ('full','partial','weak')),  -- ●◐○ per DR-2026-07-20
  source           TEXT,                           -- e.g. 'FDA-brief-harvest'
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (item_code, axis_code)
);

-- ---------------------------------------------------------------------------
-- Seed: 17 axes
-- ---------------------------------------------------------------------------
INSERT INTO axes (axis_code, name, icf_b_anchors, icf_d_anchors, mechanism, design_domains, coverage_status, falsification_condition, notes) VALUES
('AX-AMB','Ambulation & gait','b770,b730','d450,d455,d460','Walking, stairs, distance, gradients for ambulant users','E ramps/stairs/corridors, E-07 slip, E-10 rest seating','ESTABLISHED',NULL,'Alias source: MOB (ambulant share)'),
('AX-WHM','Wheeled mobility & transfer','b730,b710','d465,d420,d410','Wheelchair/scooter geometry, turning, transfer','E-01/E-12, G-04, turning circles, clear widths','ESTABLISHED',NULL,'Alias source: MOB (wheeled share)'),
('AX-REA','Reach & manipulation','b730,b710','d440,d445','Reach ranges, grip, operating force, bilateral/one-hand use','H-01, I-01..03, G-05..08','ESTABLISHED',NULL,'Alias source: UPL'),
('AX-BAL','Balance & postural stability','b235,b240','d415,d410','(a) biomechanical fall risk; (b) vestibular-sensory precipitants: pattern, specular floors, glazed edges at height, escalators, large uniform visual fields','handrails, E-07, C-03 (dual-purpose), new candidates','STUB','Merges into AX-AMB if vestibular-slug research shows precipitant guidance fully reduces to existing fall-prevention parameters','NEW. Zero corpus presence verified 2026-07-21 (b235/b240/d415 absent). All claims require tier-anchored sourcing before thresholds'),
('AX-STA','Stamina & orthostatic tolerance','b455,b130','d230,d450,d455','Exertion limits, standing intolerance, post-exertional malaise; rest/distance/seating economy','E-10, F-05, seating provision','ESTABLISHED',NULL,'Alias source: OFS'),
('AX-PAI','Pain-limited function','b280','d410,d450,d640','Nociceptive load: impact, vibration, pressure, cold-triggered pain','floor-vibration, upholstered seating, hardware force','ESTABLISHED',NULL,'Alias source: PAIN. Distinct from AX-STA (nociception vs endurance); both feed pain-ofs slug'),
('AX-THR','Thermoregulation & autonomic tolerance','b550','d230','Impaired heat/cold regulation (Uhthoff, poikilothermia); ambient stability, zoned control','TC-01..05, H-02','PARTIAL',NULL,'Names the axis scattered across MS/SCI/OFS diagnoses'),
('AX-CHM','Chemical & air-quality tolerance','b435,b440','d230','Immune/respiratory reaction to VOCs, fragrance, particulates','F-02, F-04','PARTIAL',NULL,'NEW as named axis; fed by air-quality-voc-chemical-sensitivity slug; re-homes MCAS'),
('AX-VIS-L','Low vision','b210','d460,d166','Residual-vision use: contrast, lighting, glare, size','C-04 LRV, B lighting, D-08 signage','ESTABLISHED',NULL,'Split from VIS; FDA LOW-VISION resolves here'),
('AX-VIS-N','Non-visual function','b210','d460','Tactile/auditory substitution','E-09 TWSI, A-15 acoustic differentiation, braille','ESTABLISHED',NULL,'Split from VIS'),
('AX-AUD','Auditory access & alerting','b230','d310,d115','Speech access, alert receipt, assistive listening','A-10..13, B-10, H-03, B-02','ESTABLISHED',NULL,'Alias source: DEAF (function share; cultural share is the Deaf profile)'),
('AX-SPR','Sensory processing & modulation','b156,b140','d230,d160','Hyper/hypo-reactivity, sensory load, trigger avoidance incl. photic','A/B/C/F suites, sensory rooms','ESTABLISHED',NULL,'Was population SENS. ICF under-represents modulation; anchors are nearest-fit, recorded honestly'),
('AX-COG-O','Orientation & wayfinding cognition','b114,b144','d460,d175','Memory, spatial cognition, sequencing, legibility','C-02, D-01..11','ESTABLISHED',NULL,NULL),
('AX-COG-L','Learning & information access','b117,b167','d166,d310,d315','Comprehension of environmental information: Easy Read, pictograms, symbols','D-08, signage systems','STUB','Folds into AX-COG-O if evidence shows no design-parameter divergence between legible-space and legible-information provision','NEW. Un-proxies intellectual disability; answers GAP-277'),
('AX-COM-E','Expressive communication','b320,b330','d330,d340,d350','Producing speech/sign/AAC in the environment: counter dwell, sign sightlines, device acoustics','G-06, H-04, quiet interaction space','STUB','Folds into AX-AUD/service scope if built-environment residual proves empty after targeted review','NEW. d340 shared custody with Deaf-cultural profile corpus'),
('AX-ARO','Arousal, stress & emotional regulation','b152','d240','Threat appraisal, retreat, predictability, defensible space','G-01, A-16, D-05, F-01','STUB','Re-scoped out if b152/d240 evidence proves architecturally non-actionable beyond existing SPR provisions','NEW. Rescinds FDA scope-out for the actionable subset; MH primary axis'),
('AX-CNT','Continence & elimination urgency','b620,b525','d530','Urgency/frequency as plan-driver: proximity, provision count, management space','G-04, D-03 (dual), provision-count parameters','STUB','Folds into bathroom-geometry items if proximity/frequency evidence yields no plan-level parameters','NEW. Physiological driver behind Changing Places-class provision');

-- ---------------------------------------------------------------------------
-- Seed: disposition of existing population codes
-- ---------------------------------------------------------------------------
INSERT INTO population_reclass (population_code, row_kind, layer, profile_kind, icd11_anchor, parent_correction, fluctuating, emergent_corpus, rationale) VALUES
('MOB','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,'Fuses ambulant (AX-AMB) and wheeled (AX-WHM); 31 item links re-derived per mechanism at harvest'),
('UPL','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,'Direct alias of AX-REA'),
('VIS','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,'Split alias: AX-VIS-L + AX-VIS-N (partially inverse design responses)'),
('DEAF','EXISTING-POP','SPLIT','identity-cultural',NULL,NULL,NULL,'DeafSpace / DSDG corpus','Dual: axis-alias AX-AUD (hearing function) + Deaf-cultural profile (no ICD anchor by design). Flagged judgment call'),
('SENS','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,'Axis mislabeled as population; explains 1-item-link starvation. Alias of AX-SPR'),
('PAIN','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,'yes',NULL,'Alias of AX-PAI'),
('OFS','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,'yes',NULL,'Alias of AX-STA (+AX-THR secondary)'),
('DEM','EXISTING-POP','PROFILE','diagnostic','TO-VERIFY',NULL,'no','dementia-friendly design corpus (DSDC etc.)','Diagnostic profile with mature emergent corpus'),
('NDV','EXISTING-POP','PROFILE','umbrella',NULL,NULL,NULL,'neurodivergent design literature','Umbrella; identity-cultural framing; no ICD anchor by design'),
('AUT','EXISTING-POP','PROFILE','diagnostic','6A02','parent NDV retained',NULL,'ASPECTSS','Retained distinct (in-session AUT≡NDV claim retracted: FDA mapping coarseness, not world-fact)'),
('ADHD','EXISTING-POP','PROFILE','diagnostic','6A05','parent NDV retained',NULL,NULL,'Diagnostic profile under NDV umbrella; SPR primary, COG-O secondary'),
('MH','EXISTING-POP','PROFILE','umbrella',NULL,NULL,'yes','trauma-informed design literature','Primary axis AX-ARO (previously scoped out; proxy-only representation fixed)'),
('NEU','EXISTING-POP','PROFILE','umbrella',NULL,NULL,NULL,NULL,'Umbrella (ABI, stroke, TBI). FDA term ABI resolves here'),
('EPI','EXISTING-POP','PROFILE','diagnostic','TO-VERIFY','parent NEU retained',NULL,NULL,'AX-SPR situational (photic trigger avoidance); documented judgment call'),
('MS','EXISTING-POP','PROFILE','diagnostic','8A40','re-parented OFF NEU (etiological shelf)','yes',NULL,'Functional vector: THR primary (Uhthoff), STA, AMB, VIS-L, CNT'),
('SCI','EXISTING-POP','PROFILE','diagnostic','TO-VERIFY','re-parented OFF MOB',NULL,NULL,'Biomechanical + autonomic (FDA noted; table did not): WHM, REA, THR, CNT, PAI'),
('POTS','EXISTING-POP','PROFILE','diagnostic','TO-VERIFY','was OFS sub-code','yes',NULL,'Diagnostic profile; STA primary, THR secondary, BAL situational (presyncope)'),
('CFS','EXISTING-POP','PROFILE','diagnostic','TO-VERIFY','was OFS sub-code','yes',NULL,'PEM note: rest does not equal recovery'),
('MCAS','EXISTING-POP','PROFILE','diagnostic','TO-VERIFY','re-parented OFF OFS (comorbidity, not mechanism)','yes',NULL,'Primary axis AX-CHM'),
('PCS','EXISTING-POP','SPLIT','diagnostic','TO-VERIFY (ICD-10 legacy F07.2)',NULL,'yes',NULL,'SPLIT: PCS-TBI (post-concussion: BAL, SPR, COG-O, STA) + LCOV (post-COVID). Resolves DB-vs-FDA dual definition'),
('DBL','EXISTING-POP','PROFILE','compound',NULL,NULL,NULL,'DBL tactile-first corpus (K-04 vibrotactile)','De-privileged as special population; retained as compound profile with authored content'),
('ALL','EXISTING-POP','QUALIFIER',NULL,NULL,NULL,NULL,NULL,'Link-scope marker, not a population');

INSERT INTO population_reclass (population_code, row_kind, layer, profile_kind, icd11_anchor, parent_correction, fluctuating, emergent_corpus, rationale) VALUES
('CHD','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,'Supplementary Volume Part 1','Admitted from supplementary volume; weights on REA/AMB envelope parameters'),
('LPA','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,'Supplementary Volume Part 2','Weights on REA/AMB envelopes'),
('EXH','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,'Supplementary Volume Part 3','Envelope/headroom parameters'),
('BAR','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,'Supplementary Volume Part 4','Weights on WHM/AMB envelopes, structural loading'),
('OLD','NEW-PROFILE','PROFILE','demographic',NULL,NULL,'yes','age-friendly design corpus (WHO Age-Friendly et al.)','Readmitted per decomposition-test consistency (same emergent-corpus criterion that keeps DEM)'),
('VES','NEW-PROFILE','PROFILE','diagnostic','TO-VERIFY',NULL,'yes',NULL,'Vestibular disorders; AX-BAL primary, AX-SPR secondary. STUB pending slug; queued behind language debt'),
('LCOV','NEW-PROFILE','PROFILE','diagnostic','RA02',NULL,'yes',NULL,'Post-COVID condition, split out of PCS; STA (PEM), THR, COG-O. FDA "PCS=post-COVID" resolves here');

-- ---------------------------------------------------------------------------
-- Seed: population/profile -> axis mapping
-- ---------------------------------------------------------------------------
INSERT INTO population_axis_map (population_code, axis_code, role, note) VALUES
('MOB','AX-AMB','ALIAS','ambulant share'),
('MOB','AX-WHM','ALIAS','wheeled share'),
('UPL','AX-REA','ALIAS',NULL),
('VIS','AX-VIS-L','ALIAS','low-vision share'),
('VIS','AX-VIS-N','ALIAS','blind share'),
('DEAF','AX-AUD','ALIAS','hearing-function share; cultural share is Deaf profile'),
('SENS','AX-SPR','ALIAS',NULL),
('PAIN','AX-PAI','ALIAS',NULL),
('OFS','AX-STA','ALIAS',NULL),
('OFS','AX-THR','SECONDARY',NULL),
('DEM','AX-COG-O','PRIMARY',NULL),
('DEM','AX-ARO','SECONDARY','agitation/distress'),
('DEM','AX-VIS-L','SECONDARY','ageing eye interaction'),
('DEM','AX-AMB','SECONDARY',NULL),
('NDV','AX-SPR','PRIMARY',NULL),
('NDV','AX-ARO','SECONDARY',NULL),
('NDV','AX-COG-O','SECONDARY',NULL),
('AUT','AX-SPR','PRIMARY',NULL),
('AUT','AX-ARO','SECONDARY',NULL),
('AUT','AX-COM-E','SECONDARY','non-speaking AAC use'),
('ADHD','AX-SPR','PRIMARY',NULL),
('ADHD','AX-COG-O','SECONDARY',NULL),
('MH','AX-ARO','PRIMARY','real axis; previously proxy-only'),
('MH','AX-SPR','SECONDARY',NULL),
('NEU','AX-COG-O','PRIMARY',NULL),
('NEU','AX-AMB','SECONDARY',NULL),
('NEU','AX-ARO','SECONDARY',NULL),
('NEU','AX-COM-E','SECONDARY','aphasia/dysarthria within umbrella'),
('EPI','AX-SPR','SITUATIONAL','photic/flicker trigger avoidance (B-04)'),
('MS','AX-THR','PRIMARY','Uhthoff phenomenon'),
('MS','AX-STA','SECONDARY',NULL),
('MS','AX-AMB','SECONDARY',NULL),
('MS','AX-VIS-L','SECONDARY',NULL),
('MS','AX-CNT','SECONDARY',NULL),
('SCI','AX-WHM','PRIMARY',NULL),
('SCI','AX-REA','SECONDARY',NULL),
('SCI','AX-THR','SECONDARY','poikilothermia'),
('SCI','AX-CNT','SECONDARY',NULL),
('SCI','AX-PAI','SECONDARY','neuropathic'),
('POTS','AX-STA','PRIMARY',NULL),
('POTS','AX-THR','SECONDARY',NULL),
('POTS','AX-BAL','SITUATIONAL','presyncope'),
('CFS','AX-STA','PRIMARY','PEM'),
('MCAS','AX-CHM','PRIMARY',NULL),
('PCS','AX-BAL','PRIMARY','as PCS-TBI'),
('PCS','AX-SPR','SECONDARY','photo/phonophobia'),
('PCS','AX-COG-O','SECONDARY',NULL),
('PCS','AX-STA','SECONDARY',NULL),
('DBL','AX-VIS-N','PRIMARY','compound weight'),
('DBL','AX-AUD','PRIMARY','compound weight'),
('CHD','AX-REA','PRIMARY','envelope shift'),
('CHD','AX-AMB','SECONDARY',NULL),
('LPA','AX-REA','PRIMARY','envelope shift'),
('LPA','AX-AMB','SECONDARY',NULL),
('EXH','AX-REA','PRIMARY','headroom/envelope'),
('BAR','AX-WHM','PRIMARY','turning/width envelope'),
('BAR','AX-AMB','SECONDARY','loading, seating'),
('OLD','AX-VIS-L','SECONDARY',NULL),
('OLD','AX-AUD','SECONDARY',NULL),
('OLD','AX-AMB','SECONDARY',NULL),
('OLD','AX-BAL','PRIMARY','falls'),
('OLD','AX-COG-O','SECONDARY',NULL),
('OLD','AX-THR','SECONDARY',NULL),
('OLD','AX-CNT','SECONDARY',NULL),
('VES','AX-BAL','PRIMARY',NULL),
('VES','AX-SPR','SECONDARY','visual motion sensitivity'),
('LCOV','AX-STA','PRIMARY','PEM'),
('LCOV','AX-THR','SECONDARY',NULL),
('LCOV','AX-COG-O','SECONDARY','cognitive fog');

COMMIT;

-- Post-apply (§9): backfill slugs.serves_axes; harvest item_axis_links from
-- references/audit-briefs/*_brief.md; regenerate FDA skill §1-2; normalise
-- evidence_population_match.target_population; extend db.py validate with
-- zero-coverage axis queries; close GAP-277; open STUB-axis evidence-debt gaps.
