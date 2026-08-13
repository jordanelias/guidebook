-- data_20260713000100_weighting-profile-seed.sql
-- Seed the audience emphasis profiles (best-practices-assessment-system.md §5;
-- DR-2026-07-12-evidence-architecture-unification item R + G5, ACCEPTED
-- 2026-07-13). Profiles re-rank EMPHASIS only; the claim-strength register map
-- (scripts/generate/pilot_renderings.py REGISTER_MAP) governs language, and no
-- profile can move a rendering to a different register-map row (invariants
-- I1-I5). tier_weights are qualitative foregrounding hints consumed by
-- renderers, deliberately not numeric confidence scores.
INSERT INTO weighting_profile (audience, use_pattern, tier_weights, notes) VALUES
('designer','decision-frame','{"foreground":["T1","CO1","conflict_notes","code_refs"],"delta":"show"}','Aspiration above floor; DAR provisions surfaced'),
('disabled_person','representation-checking','{"foreground":["CO1","variability","co1_limit"],"delta":"plain"}','Co-1 visibility is the point; solo-authorship limit always rendered'),
('disabled_person','advocacy-brief','{"foreground":["delta","rights","evidence_strength","gaps"],"delta":"cite-carefully"}','G5 use-pattern within the primary audience; instrument-status caveat mandatory'),
('policymaker','jurisdiction-comparison','{"foreground":["T4","T5","T6","delta","anti_laundering"],"delta":"floor-vs-anchor"}','I2: floor never rendered without anchor; regulatory-stratum rows carry the convergence-is-not-evidence line'),
('ot','specialist-handoff','{"foreground":["T1","ranges","person_mode_handoff"],"delta":"clinical"}','Population-Mode range legible for Person-Mode resolution');
