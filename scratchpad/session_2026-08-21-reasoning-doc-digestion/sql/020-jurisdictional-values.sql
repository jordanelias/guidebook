-- A-18 (RT60 in Occupied Learning and Listening Spaces) jurisdictional values,
-- digested from the pilot reasoning doc's rule-#9 step-3 comparison table.
--
-- R12: code values belong in jurisdictional_values, never in prose notes.
-- R3:  every quantified value carries [UNVERIFIED-QUANT] because the doc itself
--      states "Citation-grade verification of this table is PENDING" — no cell
--      has been checked against the standard's own text.
-- value_numeric is deliberately left NULL throughout: that column is for a
-- verified scalar, and asserting one here would claim a verification that has
-- not happened. The value lives in value_text with its marker.
-- A-18 had ZERO rows in this table before this migration.
INSERT INTO jurisdictional_values
 (jv_id,item_code,jurisdiction,standard_name,value_text,value_numeric,unit,is_code_minimum,
  evidence_tier,source_section,notes,created_at,created_by_session,updated_at,updated_by_session)
VALUES
 (110,'A-18','US','ANSI/ASA S12.60-2010/Part 1',
  '[UNVERIFIED-QUANT] general RT60 <= 0.6 s (core learning space <= 283 m3); <= 0.7 s (283-566 m3). Hearing-aid/CI users: RT60 <= 0.3 s (<= 283 m3).',
  NULL,'s',1,6,'Footnote e; Commentary 5.3.1',
  'Comparator type: volume-based. The 0.3 s figure is the DEAF-population differentiator and the pilot doc treats it as the lowest-barrier code in the surveyed set.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (111,'A-18','GB','BB93 (Building Bulletin 93, 2015)',
  '[UNVERIFIED-QUANT] general RT60 <= 0.4-0.8 s by room type; hearing-impaired "specially resourced provision" RT60 <= 0.4 s.',
  NULL,'s',1,6,NULL,
  'Comparator type: room-type-based. Statutory under the Education (School Premises) Regulations. Next-lowest barrier after ANSI/ASA in the room-type family.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (112,'A-18','GB','PAS 6463:2022',
  'No quantified RT60. Qualitative only ("acoustic calm in sensory-sensitive spaces"); references BB93.',
  NULL,NULL,0,6,NULL,
  'The ONLY standards-body publication in the surveyed set explicitly addressing neurodivergent occupant acoustic needs, and it stays qualitative. Not statutory. This absence is a first-class finding (R7), not a coverage gap.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (113,'A-18','DE','DIN 18041:2016',
  '[UNVERIFIED-QUANT] volume-dependent target curve, typically 0.4-0.8 s by room type.',
  NULL,'s',1,6,'Annex — "Hoersamkeit bei Behinderung"',
  'Comparator type: formula-based. The disability annex is qualitative; NDV/AUT not quantified. Exec 4 of batch-01 searched this standard and could not retrieve the clause — held as [UNVERIFIED-QUANT] there too.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (114,'A-18','IT','UNI 11532-2:2020',
  '[UNVERIFIED-QUANT] RT60 by room class A1-A4; class A4 (high-criticality educational) approx 0.5 s. Classes A3.1/A4 address students with hearing deficit at lower RT targets.',
  NULL,'s',1,6,NULL,
  'Comparator type: room-class-based. Mandatory citation in IT acoustic design. Category A4 considers cognitive accessibility qualitatively; NDV/AUT not quantified.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (115,'A-18','FR','NF S 31-080 (2006)',
  '[UNVERIFIED-QUANT] RT60 <= 0.4-0.8 s by room category.',
  NULL,'s',1,6,NULL,'Comparator type: room-category-based. Not differentiated for hearing impairment.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (116,'A-18','AU','AS/NZS 2107:2016',
  '[UNVERIFIED-QUANT] RT60 by space type; typical classroom 0.4-0.6 s.',
  NULL,'s',1,6,NULL,'Comparator type: space-type table. AS/NZS 2107 is the joint Australia/New Zealand standard; filed under AU because NZ is not in this table established jurisdiction vocabulary. References but does not quantify hearing-impaired-specific targets.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (117,'A-18','CN','GB 50118-2010',
  '[UNVERIFIED-QUANT] classroom RT60 <= 0.7-0.9 s by volume.',
  NULL,'s',1,6,NULL,'Comparator type: volume-based. Not differentiated by population. Highest (least inclusive) general target in the surveyed set.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (118,'A-18','NL','NEN 3088',
  '[UNVERIFIED-QUANT] RT60 <= 0.5-0.8 s.',
  NULL,'s',1,6,NULL,'Comparator type: room-type-based. Not differentiated.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (119,'A-18','BE','NBN S 01-400-2',
  '[UNVERIFIED-QUANT] typical classroom RT60 <= 0.8 s.',
  NULL,'s',1,6,NULL,'Comparator type: room-type-based. Not differentiated.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (120,'A-18','ES','DB-HR (CTE)',
  '[UNVERIFIED-QUANT] typical classroom RT60 <= 0.7 s.',
  NULL,'s',1,6,NULL,'Comparator type: room-type-based. Sound protection under the technical building code. Not differentiated.',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion'),
 (122,'A-18','JP','JIS Z 8731 + Barrier-Free Law',
  'No quantified RT60 target in the acoustic standard. Barrier-Free Law addresses physical access; acoustic provisions not quantified per population.',
  NULL,NULL,0,6,NULL,'Measurement-method standard, not a target-setting one. Absence recorded as a finding (R7).',
  '2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion','2026-08-21 18:50','session_2026-08-21-reasoning-doc-digestion');
