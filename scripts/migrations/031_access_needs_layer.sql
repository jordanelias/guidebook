-- 031_access_needs_layer.sql
-- Schema migration — Access-needs layer, additive, crosswalked to the existing
-- ICF-anchored `axes` layer. Integrates the uploaded Access Taxonomy (v0.1 draft)
-- ALONGSIDE ICF, per owner directive 2026-07-23 ("additive" path).
--
-- ADDITIVE ONLY. Creates 5 new tables + seeds them. Touches NO existing table,
-- NO population code, NO evidence cell. The population reconciliation previously
-- drafted as "031" is HELD (its slash-parent mechanism conflicts with this
-- taxonomy) and will take a later number if/when it proceeds.
--
-- Design note (avoids the schema↔DB drift bug): ICF **b/d** anchors are NOT
-- duplicated here — they live on `axes` and are reached through
-- `access_need_axis_map`. `access_need_icf` carries only anchors NOT already
-- reachable that way: the environmental **e** layer (the net-new integration),
-- plus **b/d** for the few needs that have no/partial axis.
--
-- ICF confidence: 'confirmed' = code I am confident exists at that granularity.
-- 'proposed' = verify against an ICF browser before relying on it — never invented.
--
-- Forward-only; user_version bumped to 31 by migrate_db.py from the 031 prefix.
-- Determinism: seed provenance normalised to fixed literals at the tail (rebuild-safe).

BEGIN TRANSACTION;

-- ── Axis 1: the access needs (design obligations; name nobody) ──────────────
CREATE TABLE IF NOT EXISTS access_needs (
  need_code       TEXT PRIMARY KEY,               -- 'A-NOSIGHT' …
  family          TEXT NOT NULL CHECK (family IN
                    ('perceiving','communicating','operating','pacing','environment_safety')),
  design_obligation TEXT NOT NULL,                 -- "the design must …"
  absorbs         TEXT,                            -- populations/situations it covers (prose, audit-side)
  typical_stakes  TEXT CHECK (typical_stakes IN ('safety-critical','exclusion','friction')),
  source_version  TEXT NOT NULL DEFAULT 'access-taxonomy v0.1',
  notes           TEXT,
  created_at      TEXT DEFAULT (datetime('now')),
  created_by_session TEXT
);

-- Crosswalk: access need ↔ existing Layer-1 axis (b/d ICF flows through this join)
CREATE TABLE IF NOT EXISTS access_need_axis_map (
  need_code    TEXT NOT NULL REFERENCES access_needs(need_code),
  axis_code    TEXT NOT NULL REFERENCES axes(axis_code),
  relationship TEXT NOT NULL CHECK (relationship IN ('primary','partial','spans')),
  note         TEXT,
  created_at   TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (need_code, axis_code)
);

-- ICF anchoring — the "alongside ICF" core. e-layer + b/d only where no axis carries it.
CREATE TABLE IF NOT EXISTS access_need_icf (
  need_code   TEXT NOT NULL REFERENCES access_needs(need_code),
  icf_code    TEXT NOT NULL,                       -- 'e250','b765','d510' …
  icf_type    TEXT NOT NULL CHECK (icf_type IN ('b','d','e','s')),
  confidence  TEXT NOT NULL CHECK (confidence IN ('confirmed','proposed')),
  note        TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  created_by_session TEXT,
  PRIMARY KEY (need_code, icf_code)
);

-- Supporting vocabularies (reference/seed only; no guidance is tagged yet) ─────
CREATE TABLE IF NOT EXISTS access_duration (
  code TEXT PRIMARY KEY CHECK (code IN ('permanent','temporary','situational')),
  definition TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT
);
CREATE TABLE IF NOT EXISTS access_stakes (
  code TEXT PRIMARY KEY CHECK (code IN ('safety-critical','exclusion','friction')),
  definition TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT
);

-- ── Seed: 17 access needs ───────────────────────────────────────────────────
INSERT INTO access_needs (need_code, family, design_obligation, absorbs, typical_stakes, notes) VALUES
 ('A-NOSIGHT','perceiving','Be perceivable and operable without sight; text alternatives, audio description, braille, logical reading order; never colour alone as a carrier of meaning.','blindness, low vision, colour vision deficiency, temporary eye injury, glare',NULL,NULL),
 ('A-NOSOUND','perceiving','Never carry meaning in sound alone; captions, transcripts, visual alerts, sign-language provision where it is the user''s language.','Deaf, hard of hearing, late-deafened, ear infection, loud/silent environments',NULL,NULL),
 ('A-TACTILE','perceiving','Offer touch as a first-class channel, not a fallback; tactile signage/maps, hand-under-hand guidance, protactile-aware interpreting, physical landmarks.','DeafBlind (Protactile) — not A-NOSIGHT + A-NOSOUND',NULL,'No exact axis: DeafBlind access is distinct. Genuine coverage gap vs the axis layer.'),
 ('A-STABLE','perceiving','Hold the visual reference still; no auto-playing motion/parallax; handrails, signalled level changes, rest points.','vestibular disorders, migraine, motion sensitivity, post-concussion, pregnancy',NULL,NULL),
 ('A-NOSPEECH','communicating','Never require speech or voice; text alternatives to calls, AAC-compatible interaction, no voice-only auth, time to compose.','aphasia, dysarthria, stammering, non-speaking people, AAC users, laryngitis, L2 users',NULL,NULL),
 ('A-PLAIN','communicating','Use plain, predictable language and structure; controlled reading level, no unexplained jargon, consistent patterns, glossary where terms are load-bearing.','dyslexia, intellectual disability, dementia, brain injury, distraction, L2 users',NULL,NULL),
 ('A-REACH','operating','Be physically reachable; step-free routes, seated-height controls, doorway/turning clearance, one-handed operation, no simultaneous-input requirement.','wheelchair users, ambulatory wheelchair users, cane/crutch users, limb difference, carrying a child',NULL,'Spans three axes (REA/WHM/AMB).'),
 ('A-PRECISION','operating','Tolerate imprecise input; large targets, generous spacing, no fine-motor/drag-only interaction, timing that tolerates tremor and overshoot.','tremor, dystonia, Parkinson''s, arthritis, neuropathy, cold hands',NULL,'No dedicated motor-precision axis — gap. Pairs with a MOVE population if adopted.'),
 ('A-AT','operating','Work with assistive technology; programmatically-determinable structure, standard controls, no custom widgets without full semantics.','screen readers, magnification, switch access, voice control, alternative keyboards',NULL,'Conformance/artifact property (WCAG Robust). Digital — may be out of built-environment scope; flagged for owner decision.'),
 ('A-SELFCARE','operating','Support personal care and daily tasks; accessible toilets and changing places, operable fixtures, privacy, dignity, no dependence on a helper being present.','bathing, dressing, toileting, eating',NULL,'Broader than AX-CNT (toileting only): adds washing/dressing/eating (d510/d540/d550).'),
 ('A-LOWLOAD','pacing','Keep memory and attention demand low; chunking, save/resume, no reliance on recall across steps, undo, progress visible.','ADHD, dementia, brain injury, brain fog, intellectual disability, anyone interrupted',NULL,NULL),
 ('A-TIME','pacing','Impose no time pressure; no session timeouts without extension, no timed inputs, no penalty for slowness.','slow processing, motor delay, AAC use, screen-reader navigation, translation, distraction',NULL,'No dedicated time-pressure axis — cuts across STA/COG. Gap.'),
 ('A-EFFORT','pacing','Cost little energy; short paths, seated options, save/resume, rest points, no forced continuous sessions, no penalty for stopping.','energy-limiting conditions, ME/CFS, Long COVID, POTS, MS fatigue, pain, cardiac/respiratory, older adults, recovery',NULL,NULL),
 ('A-STIMULUS','environment_safety','Let the user turn it down; reduce default stimulus density; mute, dim, reduce-motion, hide decorative content.','autistic people, sensory processing differences, migraine, post-concussion, PTSD, open-plan offices',NULL,NULL),
 ('A-TRIGGER','environment_safety','Not emit the trigger; under flash thresholds; fragrance-free; material/ingredient disclosure; no strobe.','photosensitive epilepsy, MCAS, chemical sensitivity, migraine','safety-critical','Spans SPR (photic) + CHM (airborne). Nearly always safety-critical.'),
 ('A-CALM','environment_safety','Not manufacture pressure; no artificial urgency or dark patterns, forgiving of errors, private by default, calm defaults, clear exit.','anxiety, PTSD, psychiatric distress, autistic people, anyone under stress',NULL,NULL),
 ('A-SIZE','environment_safety','Fit the range of bodies present; reach ranges at short and tall ends, seat width and weight rating, adjustable heights, clearance. Frame as the environment being wrongly normed to an average body, never as bodies deviating.','little people, tall people, fat people, pregnancy, children, wheelchair seating height',NULL,'The body-size link; the design home for the body-size population group.');

-- ── Seed: access need → axis crosswalk (b/d ICF flows through these joins) ───
INSERT INTO access_need_axis_map (need_code, axis_code, relationship, note) VALUES
 ('A-NOSIGHT','AX-VIS-N','primary',NULL),
 ('A-NOSIGHT','AX-VIS-L','partial','residual-vision route'),
 ('A-NOSOUND','AX-AUD','primary',NULL),
 ('A-TACTILE','AX-VIS-N','partial','closest; DeafBlind not fully captured'),
 ('A-STABLE','AX-BAL','primary',NULL),
 ('A-NOSPEECH','AX-COM-E','primary',NULL),
 ('A-PLAIN','AX-COG-L','primary',NULL),
 ('A-REACH','AX-REA','primary',NULL),
 ('A-REACH','AX-WHM','spans',NULL),
 ('A-REACH','AX-AMB','spans',NULL),
 ('A-PRECISION','AX-REA','partial','no dedicated precision axis'),
 ('A-SELFCARE','AX-CNT','partial','AX-CNT is toileting-only; A-SELFCARE broader'),
 ('A-LOWLOAD','AX-COG-O','primary',NULL),
 ('A-LOWLOAD','AX-COG-L','partial',NULL),
 ('A-EFFORT','AX-STA','primary',NULL),
 ('A-STIMULUS','AX-SPR','primary',NULL),
 ('A-TRIGGER','AX-SPR','spans','photic'),
 ('A-TRIGGER','AX-CHM','spans','airborne'),
 ('A-CALM','AX-ARO','primary',NULL),
 ('A-SIZE','AX-REA','spans','envelope'),
 ('A-SIZE','AX-WHM','spans','envelope');
-- (A-AT and A-TIME intentionally have NO axis row — the two clean gaps.)

-- ── Seed: ICF anchors (e-layer = net-new; b/d only where no axis carries it) ─
INSERT INTO access_need_icf (need_code, icf_code, icf_type, confidence, note) VALUES
 ('A-NOSIGHT','e150','e','confirmed','building design (public)'),
 ('A-NOSIGHT','e155','e','confirmed','building design (private)'),
 ('A-NOSIGHT','e240','e','confirmed','Light'),
 ('A-NOSIGHT','e125','e','confirmed','products & technology for communication'),
 ('A-NOSOUND','e250','e','confirmed','Sound'),
 ('A-NOSOUND','e125','e','confirmed',NULL),
 ('A-NOSOUND','e1251','e','confirmed','assistive products & technology for communication (sub-code of e125); verified WHO/ICF 2026-07-23'),
 ('A-TACTILE','e150','e','confirmed',NULL),
 ('A-TACTILE','e155','e','confirmed',NULL),
 ('A-TACTILE','e340','e','confirmed','personal-care providers / SSPs'),
 ('A-STABLE','e150','e','confirmed',NULL),
 ('A-STABLE','e240','e','confirmed',NULL),
 ('A-NOSPEECH','e125','e','confirmed',NULL),
 ('A-NOSPEECH','e340','e','confirmed',NULL),
 ('A-PLAIN','e150','e','confirmed','signage/wayfinding'),
 ('A-PLAIN','e155','e','confirmed',NULL),
 ('A-REACH','e150','e','confirmed',NULL),
 ('A-REACH','e155','e','confirmed',NULL),
 ('A-REACH','e120','e','confirmed','mobility products & technology'),
 ('A-PRECISION','e115','e','confirmed','products for daily living'),
 ('A-PRECISION','b765','b','confirmed','involuntary movement functions: tremor, dystonia, chorea, dyskinesia (excl. b760 voluntary control, b770 gait); verified WHO/ICF 2026-07-23. No axis carries it.'),
 ('A-AT','e125','e','confirmed',NULL),
 ('A-AT','e1251','e','confirmed','assistive products & technology for communication (sub-code of e125); verified WHO/ICF 2026-07-23'),
 ('A-SELFCARE','e115','e','confirmed',NULL),
 ('A-SELFCARE','e150','e','confirmed',NULL),
 ('A-SELFCARE','e340','e','confirmed',NULL),
 ('A-SELFCARE','d510','d','confirmed','washing oneself — beyond AX-CNT'),
 ('A-SELFCARE','d540','d','confirmed','dressing — beyond AX-CNT'),
 ('A-SELFCARE','d550','d','confirmed','eating — beyond AX-CNT'),
 ('A-LOWLOAD','e150','e','confirmed','wayfinding'),
 ('A-TIME','b164','b','confirmed','higher-level cognitive functions: time management, planning & sequencing (verified WHO/ICF 2026-07-23). Rationale (owner 2026-07-23): brain fog impairs organizing time and retaining the sequence of actions, so tasks run slower as people work to hold onto intent -> the environment must impose no time pressure. No axis carries it.'),
 ('A-EFFORT','e150','e','confirmed','rest points, seating'),
 ('A-EFFORT','e120','e','confirmed',NULL),
 ('A-STIMULUS','e240','e','confirmed',NULL),
 ('A-STIMULUS','e250','e','confirmed',NULL),
 ('A-STIMULUS','e150','e','confirmed',NULL),
 ('A-TRIGGER','e240','e','confirmed','flash/strobe'),
 ('A-TRIGGER','e260','e','confirmed','Air quality'),
 ('A-CALM','e150','e','confirmed',NULL),
 ('A-SIZE','e150','e','confirmed',NULL),
 ('A-SIZE','e155','e','confirmed',NULL),
 ('A-SIZE','e115','e','confirmed',NULL),
 ('A-SIZE','e120','e','confirmed',NULL);

-- ── Seed: supporting vocabularies ───────────────────────────────────────────
INSERT INTO access_duration (code, definition) VALUES
 ('permanent','A lasting characteristic of the person''s relationship to the barrier.'),
 ('temporary','Time-limited (injury, recovery, pregnancy, treatment).'),
 ('situational','Context-induced for anyone (loud room, bright sun, carrying a child). A non-empty situational relevance is why there is no ALL code.');
INSERT INTO access_stakes (code, definition) VALUES
 ('safety-critical','Harm if violated.'),
 ('exclusion','Locks people out.'),
 ('friction','Degrades the experience.');

-- ── Determinism: fixed provenance for the rebuild-reproducibility gate ───────
UPDATE access_needs         SET created_at='2026-07-23T00:00:00Z', created_by_session='session_2026-07-23-access-needs-integration';
UPDATE access_need_axis_map SET created_at='2026-07-23T00:00:00Z', created_by_session='session_2026-07-23-access-needs-integration';
UPDATE access_need_icf      SET created_at='2026-07-23T00:00:00Z', created_by_session='session_2026-07-23-access-needs-integration';
UPDATE access_duration      SET created_at='2026-07-23T00:00:00Z', created_by_session='session_2026-07-23-access-needs-integration';
UPDATE access_stakes        SET created_at='2026-07-23T00:00:00Z', created_by_session='session_2026-07-23-access-needs-integration';

COMMIT;
