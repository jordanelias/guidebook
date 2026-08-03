-- 030_two_layer_functional_taxonomy.sql
-- Schema migration — two-layer functional taxonomy (axes × profiles).
-- Ratifies into the DB: DR-2026-07-21-two-layer-functional-taxonomy (v1.2);
-- owner directive "just do it" (2026-07-21). Doctrine: governance/functional-taxonomy.md
-- v1.2, incl. §0.5 the irreducibility principle (axes describe specification-variation,
-- not persons; population_axis_map is a retrieval index, not a portrait).
--
-- Forward-only and immutable once committed. Deterministic for the CI rebuild-
-- reproducibility gate: seed rows carry FIXED created_at/created_by_session
-- (normalised at the tail of this transaction), never datetime('now').
--
-- Creates: axes (17), population_reclass (29), population_axis_map (69),
-- item_axis_links (EMPTY), situations (EMPTY). The item↔axis and slug↔axis
-- bridges are intentionally empty — coverage holes are visible-by-construction;
-- the population→axis / FDA-brief harvest is a tracked follow-up (execution
-- register E2/E3), not part of this schema step.

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS axes (
  axis_code        TEXT PRIMARY KEY,
  name             TEXT NOT NULL,                  -- interaction-framed
  icf_b_anchors    TEXT,
  icf_d_anchors    TEXT,
  mechanism        TEXT NOT NULL,                  -- demand the environment places
  design_domains   TEXT,
  coverage_status  TEXT NOT NULL CHECK (coverage_status IN ('ESTABLISHED','PARTIAL','STUB')),
  falsification_condition TEXT NOT NULL,           -- symmetric: every axis carries one
  notes            TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
);

CREATE TABLE IF NOT EXISTS population_reclass (
  population_code  TEXT PRIMARY KEY,               -- DB code
  canonical_code   TEXT,                           -- population-taxonomy.md form (e.g. OFS/ME)
  row_kind         TEXT NOT NULL CHECK (row_kind IN ('EXISTING-POP','NEW-PROFILE')),
  layer            TEXT NOT NULL CHECK (layer IN ('AXIS-ALIAS','PROFILE','QUALIFIER','SPLIT')),
  profile_kind     TEXT CHECK (profile_kind IN
                     ('diagnostic','identity-cultural','demographic','anthropometric','compound','umbrella')),
  mapping_confidence TEXT CHECK (mapping_confidence IN
                     ('high','moderate','low','minimal','TO-ASSESS') OR mapping_confidence IS NULL),
                                                   -- armature §4.2 model; navigation hypothesis, not prescription
  icd11_anchor     TEXT,                           -- optional; never gates membership or content (doctrine §3.3)
  parent_correction TEXT,
  fluctuating      TEXT CHECK (fluctuating IN ('yes','no') OR fluctuating IS NULL),
  emergent_corpus  TEXT,
  rationale        TEXT NOT NULL,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
);

CREATE TABLE IF NOT EXISTS population_axis_map (
  population_code  TEXT NOT NULL,
  axis_code        TEXT NOT NULL REFERENCES axes(axis_code),
  role             TEXT NOT NULL CHECK (role IN ('ALIAS','PRIMARY','SECONDARY','SITUATIONAL')),
  note             TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (population_code, axis_code)
);

CREATE TABLE IF NOT EXISTS item_axis_links (
  item_code        TEXT NOT NULL,
  axis_code        TEXT NOT NULL REFERENCES axes(axis_code),
  mechanism_note   TEXT,
  strength_band    TEXT CHECK (strength_band IN ('full','partial','weak')),
  use_mode         TEXT CHECK (use_mode IN ('independent','assisted','collective') OR use_mode IS NULL),
  source           TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (item_code, axis_code)
);

-- First-person, language-carrying episode/journey accounts: the native Co-1
-- attachment point (doctrine §5.4). Never decomposed into axis fragments as
-- primary representation; seeds questions-led navigation (mission #6).
CREATE TABLE IF NOT EXISTS situations (
  situation_id     TEXT PRIMARY KEY,               -- SIT-#### at apply time
  title            TEXT NOT NULL,
  account_language TEXT NOT NULL,                  -- language of the original account
  account_text_ref TEXT NOT NULL,                  -- source/provenance pointer (may be non-DOI intake, §5.6)
  translation_ref  TEXT,
  attaches_items   TEXT,                           -- CSV item codes
  attaches_axes    TEXT,                           -- CSV axis codes
  attaches_profiles TEXT,                          -- CSV population/profile codes
  operational_access TEXT CHECK (operational_access IN ('yes','no') OR operational_access IS NULL),
                                                   -- marks broken-lift-class evidence (doctrine §5.5)
  co1_status       TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
);

-- ---------------------------------------------------------------------------
-- Seed: 17 axes (falsification symmetric)
-- ---------------------------------------------------------------------------
INSERT INTO axes (axis_code, name, icf_b_anchors, icf_d_anchors, mechanism, design_domains, coverage_status, falsification_condition, notes) VALUES
('AX-AMB','Ambulant movement','b770,b730','d450,d455,d460','Continuous walking, stairs, distance, gradients; floor-level living incl. floor-sitting, prostration, floor-to-standing transitions','E ramps/stairs/corridors, E-07 slip, E-10 rest seating; floor-level transfer provisions','ESTABLISHED','Re-merges with AX-WHM if evidence shows no parameter divergence between ambulant and wheeled movement','Alias source: MOB ambulant share (canonical MOB/AMB)'),
('AX-WHM','Wheeled movement & transfer','b730,b710','d465,d420,d410','Turning, clearance, transfer geometry — independent and assisted (two-person, hoist)','E-01/E-12, G-04, turning circles, clear widths, hoist clearances','ESTABLISHED','Re-merges with AX-AMB if evidence shows no parameter divergence; transfer splits out per armature §5 if ratification item R6 so decides','Alias source: MOB wheeled share'),
('AX-REA','Reach & manipulation','b730,b710','d440,d445','Reach envelopes, grip, operating force at chair, counter, and floor-level heights','H-01, I-01..03, G-05..08','ESTABLISHED','Splits per armature (limb presence / reach / grip) if build-stage evidence shows the consolidated axis loses specification precision','Alias source: UPL (canonical MOB/UPL)'),
('AX-BAL','Balance & postural demand','b235,b240','d415,d410','(a) fall-risk under gait/transfer load; (b) environments that precipitate dizziness: repeating pattern, specular floors, glazed edges at height, escalators, large uniform visual fields','handrails, E-07, C-03 (dual-purpose), stair geometry','STUB','Merges into AX-AMB if vestibular-slug research shows precipitant guidance fully reduces to existing fall-prevention parameters','Named in canon (armature §5 vestibular axis; NEU/PCS prose) yet operationally invisible: zero b-codes, zero slugs, zero searches in 19 tracked languages (EN-term caveat; §9.2 gate applies). Claims require tier-anchored sourcing before thresholds'),
('AX-STA','Sustained-exertion demand','b455,b130','d230,d450,d455','Standing, queueing, distance without rest; grid/lift failure converting routes into exertion cliffs','E-10, F-05, seating provision; passive redundancy for grid intermittency','ESTABLISHED','Merges with AX-PAI into a single symptom-load axis if evidence shows no parameter divergence (nociceptive/central vs exertional)','Alias source: OFS'),
('AX-PAI','Pain-load demand','b280','d410,d450,d640','Impact, vibration, pressure, cold; spans nociceptive AND centrally-sensitized pain — provisions must not assume load-avoidance alone suffices (fibromyalgia-type pain is not nociception-dominant)','floor-vibration, upholstered seating, hardware force','ESTABLISHED','Merges with AX-STA per the same condition, symmetrically','Alias source: PAIN; both feed pain-ofs slug'),
('AX-THR','Thermal demand','b550','d230','Heat/cold exposure for impaired thermoregulation — via conditioning and passive means (shading, mass, ventilation) where grids are intermittent','TC-01..05, H-02; passive-first options','PARTIAL','Dissolves into item-level thermal specs if no population-differentiated thresholds survive evidence review','Names the axis scattered across MS/SCI/OFS diagnoses'),
('AX-CHM','Airborne-exposure demand','b435,b440','d230','VOCs, fragrance, particulates, smoke','F-02, F-04','PARTIAL','Dissolves into F-04 item family if no axis-level (cross-item) guidance survives evidence review','Fed by air-quality-voc slug; re-homes MCAS by mechanism'),
('AX-VIS-L','Low-vision information demand','b210','d460,d166','Environments legible through residual vision: contrast, lighting, glare, size','C-04 LRV, B lighting, D-08 signage','ESTABLISHED','Re-merges with AX-VIS-N if evidence shows no response divergence (current evidence: partially inverse responses)','Split from VIS; FDA LOW-VISION resolves here'),
('AX-VIS-N','Non-visual information demand','b210','d460','Environments legible without vision: tactile, acoustic, layout consistency','E-09 TWSI, A-15, braille','ESTABLISHED','Re-merges per the same condition, symmetrically','Split from VIS'),
('AX-AUD','Auditory access & alerting demand','b230','d310,d115','Speech access, alert receipt, assistive listening infrastructure','A-10..13, B-10, H-03, B-02','ESTABLISHED','Splits acuity/processing per armature §5 if build-stage evidence requires it','Alias source: DEAF function share; Deaf-community profile holds DeafSpace/d340 (doctrine §4)'),
('AX-SPR','Sensory-load demand','b156,b140','d230,d160','Stimulus intensity, unpredictability, trigger exposure incl. photic','A/B/C/F suites, sensory rooms','ESTABLISHED','Splits by modality if evidence shows modality-specific parameters dominate cross-modal load','Was NDV/SENS as population; ICF under-represents modulation — anchors nearest-fit, recorded honestly'),
('AX-COG-O','Orientation demand','b114,b144','d460,d175','Legible-space demands: memory, sequencing, decision-point load','C-02, D-01..11','ESTABLISHED','Restructures to armature four-sub-dimension model if ratification item R7 so decides','—'),
('AX-COG-L','Information-access demand','b117,b167','d166,d310,d315','Legible-information demands across scripts and literacy levels, not only Easy-Read-genre English','D-08, signage systems, plain-language provisions','STUB','Folds into AX-COG-O if evidence shows no design-parameter divergence between legible-space and legible-information provision','Un-proxies IntD information access (GAP-277); armature §5.1 governs IntD treatment'),
('AX-COM-E','Expressive-communication demand','b320,b330','d330,d335,d350','Environments requiring speech production under time/acoustic pressure: counters, intercoms; AAC dwell and device acoustics. d340 sign production held by Deaf-community profile; this axis serves sightline/lighting infrastructure only','G-06, H-04, quiet interaction space','STUB','Folds into AX-AUD/service scope if built-environment residual proves empty after targeted review','Signed languages are languages, not deficits (doctrine §2.1)'),
('AX-ARO','Arousal-safety demand','b152','d240','Threat-appraisal load: exposure, unpredictability, lack of retreat or exit legibility','G-01, A-16, D-05, F-01','STUB','Re-scoped out if b152/d240 evidence proves architecturally non-actionable beyond existing SPR provisions','Rescinds FDA scope-out for actionable subset; MH primary axis; trauma-informed design curates here'),
('AX-CNT','Toileting-proximity demand','b620,b525','d530','Urgency/frequency as plan-driver: distance, provision count, management space; squat and sitting WC typologies both first-class','G-04, D-03 (dual), provision-count parameters, adult-changing provision','STUB','Folds into bathroom-geometry items if proximity/frequency evidence yields no plan-level parameters','Physiological driver behind need-driven provision');

-- ---------------------------------------------------------------------------
-- Seed: disposition of existing population codes
-- ---------------------------------------------------------------------------
INSERT INTO population_reclass (population_code, canonical_code, row_kind, layer, profile_kind, mapping_confidence, icd11_anchor, parent_correction, fluctuating, emergent_corpus, rationale) VALUES
('MOB','MOB','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,NULL,'Canonical sub-codes MOB/AMB+MOB/UPL already split; axis layer completes it (AX-AMB + AX-WHM); 31 item links re-derived per mechanism at harvest'),
('UPL','MOB/UPL','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,NULL,'Direct alias of AX-REA'),
('VIS','VIS','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,NULL,'Split alias: AX-VIS-L + AX-VIS-N (partially inverse design responses)'),
('DEAF','DEAF','EXISTING-POP','SPLIT','identity-cultural',NULL,NULL,NULL,NULL,'DeafSpace / DSDG corpus; d340 sign-space provisions','Dual: axis-alias AX-AUD (infrastructure) + Deaf-community profile (identity; no ICD by design) holding DeafSpace and sign-language spatial practice as language, not deficit. Answers armature §5 open question; flagged judgment call'),
('SENS','NDV/SENS','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,NULL,NULL,'Sub-code was an axis in population clothing (AX-SPR); explains 1-item-link starvation'),
('PAIN','PAIN','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,'yes',NULL,'Alias of AX-PAI (nociceptive + centrally-sensitized span)'),
('OFS','OFS','EXISTING-POP','AXIS-ALIAS',NULL,NULL,NULL,NULL,'yes',NULL,'Alias of AX-STA (+AX-THR secondary)'),
('DEM','DEM','EXISTING-POP','PROFILE','diagnostic','low','TO-VERIFY',NULL,'no','dementia-friendly design corpus (DSDC etc.)','Diagnostic profile with mature emergent corpus; low-predictive: stage and individual variation dominate'),
('NDV','NDV','EXISTING-POP','PROFILE','umbrella',NULL,NULL,NULL,NULL,'neurodivergent design literature','Umbrella; identity-framed; no ICD anchor by design'),
('AUT','NDV/AUT','EXISTING-POP','PROFILE','diagnostic','low','6A02','parent NDV retained',NULL,'ASPECTSS','Distinct profile with autism-specific emergent corpus; low-predictive (spectrum variation)'),
('ADHD','NDV/ADHD','EXISTING-POP','PROFILE','diagnostic','TO-ASSESS','6A05','parent NDV retained',NULL,NULL,'Diagnostic profile under NDV umbrella; SPR primary, COG-O secondary'),
('MH','NDV/MH','EXISTING-POP','PROFILE','umbrella',NULL,NULL,'top-level per population-taxonomy §2.4','yes','trauma-informed design literature','Canon holds MH top-level for distinct functional profile; AX-ARO gives it the axis it lacked'),
('NEU','NEU','EXISTING-POP','PROFILE','umbrella','low',NULL,NULL,NULL,NULL,'Umbrella (ABI, stroke, TBI); FDA term ABI resolves here; low-predictive per armature (ABI listed)'),
('EPI','NEU/EPI (proposed)','EXISTING-POP','PROFILE','diagnostic','TO-ASSESS','TO-VERIFY','parent NEU retained',NULL,NULL,'AX-SPR situational (photic trigger avoidance, B-04); documented judgment call'),
('MS','NEU/MS (proposed)','EXISTING-POP','PROFILE','diagnostic','low','8A40','re-homed by mechanism, not etiology (was NEU shelf)','yes',NULL,'Functional vector: THR primary (Uhthoff), STA, AMB, VIS-L, CNT; low-predictive per armature (EDSS scaffold)'),
('SCI','MOB/SCI (proposed)','EXISTING-POP','PROFILE','diagnostic','high','TO-VERIFY','re-homed off MOB',NULL,NULL,'High-predictive at complete lesions (armature example: complete T6), moderate otherwise; autonomic demands (THR, CNT) made visible alongside WHM/REA/PAI'),
('POTS','OFS/POTS','EXISTING-POP','PROFILE','diagnostic','TO-ASSESS','TO-VERIFY','was OFS sub-code','yes',NULL,'STA primary, THR secondary, BAL situational (presyncope)'),
('CFS','OFS/ME','EXISTING-POP','PROFILE','diagnostic','TO-ASSESS','TO-VERIFY','was OFS sub-code; canonical name OFS/ME; display ME/CFS per community preference','yes',NULL,'Post-exertional malaise is a first-class design constraint: environments must not assume exertion is recoverable by rest — distance, queueing, and standing demands are harm vectors, not inconveniences'),
('MCAS','OFS/MCAS','EXISTING-POP','PROFILE','diagnostic','TO-ASSESS','TO-VERIFY','re-homed off OFS (mechanism: immune, not orthostatic comorbidity)','yes',NULL,'AX-CHM primary. Contested-legitimacy history noted: thin Tier-1 evidence partly reflects historical dismissal; non-DOI intake path (doctrine §5.6) applies'),
('PCS','NEU/PCS','EXISTING-POP','SPLIT','diagnostic','TO-ASSESS','TO-VERIFY (ICD-10 legacy F07.2)',NULL,'yes',NULL,'SPLIT: PCS-TBI (post-concussion: BAL, SPR, COG-O, STA — matches canon NEU/PCS prose) + LCOV (post-COVID). Resolves DB-vs-FDA dual definition'),
('DBL','DBL','EXISTING-POP','PROFILE','compound',NULL,NULL,NULL,NULL,'DBL tactile-first corpus (K-04 vibrotactile)','First-class compound profile with authored corpus; canon rule preserved verbatim: DBL is not VIS + DEAF (population-taxonomy §3.1). Structural placement changes; standing does not'),
('ALL','ALL','EXISTING-POP','QUALIFIER',NULL,NULL,NULL,NULL,NULL,NULL,'Scope marker, not a population (population-taxonomy §1.3)');

INSERT INTO population_reclass (population_code, canonical_code, row_kind, layer, profile_kind, mapping_confidence, icd11_anchor, parent_correction, fluctuating, emergent_corpus, rationale) VALUES
('CHD','CHD','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,NULL,'Supplementary Volume Part 1','Admitted from supplementary volume; envelope weights on REA/AMB; supplementary containment rule preserved'),
('LPA','LPA','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,NULL,'Supplementary Volume Part 2','Envelope weights on REA/AMB; community-preferred naming per term_aliases'),
('EXH','EXH','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,NULL,'Supplementary Volume Part 3','Headroom/envelope parameters'),
('BAR','BAR','NEW-PROFILE','PROFILE','anthropometric',NULL,NULL,NULL,NULL,'Supplementary Volume Part 4','Envelope weights on WHM/AMB; structural loading; BAR containment validator rule preserved'),
('OAD','OAD','NEW-PROFILE','PROFILE','demographic',NULL,NULL,NULL,'yes','age-friendly design corpus (WHO Age-Friendly et al.)','Older adults; readmitted under the same emergent-corpus criterion that keeps DEM; BAL primary (falls), VIS-L/AUD/AMB/COG-O/THR/CNT secondary'),
('VES','VES','NEW-PROFILE','PROFILE','diagnostic','TO-ASSESS','TO-VERIFY',NULL,'yes',NULL,'Vestibular disorders; AX-BAL primary, AX-SPR secondary. Evidence-stub RECORD status — describes the record, never the people; research queued per doctrine §8 with its equity cost stated'),
('LCOV','LCOV','NEW-PROFILE','PROFILE','diagnostic','TO-ASSESS','RA02',NULL,'yes',NULL,'Post-COVID condition, split out of PCS; STA (PEM), THR, COG-O; FDA "PCS=post-COVID" resolves here');

-- ---------------------------------------------------------------------------
-- Seed: population/profile -> axis mapping
-- ---------------------------------------------------------------------------
INSERT INTO population_axis_map (population_code, axis_code, role, note) VALUES
('MOB','AX-AMB','ALIAS','ambulant share (MOB/AMB)'),
('MOB','AX-WHM','ALIAS','wheeled share'),
('UPL','AX-REA','ALIAS',NULL),
('VIS','AX-VIS-L','ALIAS','low-vision share'),
('VIS','AX-VIS-N','ALIAS','blind share'),
('DEAF','AX-AUD','ALIAS','infrastructure share; DeafSpace/d340 held by Deaf-community profile'),
('SENS','AX-SPR','ALIAS',NULL),
('PAIN','AX-PAI','ALIAS',NULL),
('OFS','AX-STA','ALIAS',NULL),
('OFS','AX-THR','SECONDARY',NULL),
('DEM','AX-COG-O','PRIMARY',NULL),
('DEM','AX-ARO','SECONDARY','distress/agitation'),
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
('MH','AX-ARO','PRIMARY','the axis MH lacked; previously proxy-only'),
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
('CFS','AX-STA','PRIMARY','PEM: exertion as harm vector'),
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
('OAD','AX-BAL','PRIMARY','falls'),
('OAD','AX-VIS-L','SECONDARY',NULL),
('OAD','AX-AUD','SECONDARY',NULL),
('OAD','AX-AMB','SECONDARY',NULL),
('OAD','AX-COG-O','SECONDARY',NULL),
('OAD','AX-THR','SECONDARY',NULL),
('OAD','AX-CNT','SECONDARY',NULL),
('VES','AX-BAL','PRIMARY',NULL),
('VES','AX-SPR','SECONDARY','visual motion sensitivity'),
('LCOV','AX-STA','PRIMARY','PEM'),
('LCOV','AX-THR','SECONDARY',NULL),
('LCOV','AX-COG-O','SECONDARY','cognitive fog');


-- ── Determinism: normalise seed-row provenance to fixed values (rebuild-safe) ──
UPDATE axes             SET created_at='2026-07-21T22:45:00Z', created_by_session='session_2026-07-21-taxonomy-execution';
UPDATE population_reclass SET created_at='2026-07-21T22:45:00Z', created_by_session='session_2026-07-21-taxonomy-execution';
UPDATE population_axis_map SET created_at='2026-07-21T22:45:00Z', created_by_session='session_2026-07-21-taxonomy-execution';

COMMIT;
