-- 016_code_currency_columns.sql
-- Schema migration: add code-currency tracking to evidence_sources.
--
-- Surfaced during session 2026-05-25 owner directive on outdated codes:
-- the metadata-quality gate (rule #10) verifies that the DB row parses and
-- the cited document exists, not that the cited edition is the current
-- legally-in-force or empirically-current edition. Two failure modes
-- observed in the same session: (1) DIN 18040-1:2010 still legally in
-- force but supersedable by DIN EN 17210:2021 and E DIN 18040-1:2023 draft;
-- (2) NZS 4121:2001 speculated as likely superseded from age alone, then
-- verified still operative per NZ Building Act §119 — age does not predict
-- supersession either way.
--
-- The code-currency check is a separate dimension from metadata integrity
-- (014) and from claim verification (PI rule #10 sub-rules 1-3). It asks
-- a single question: is the cited edition the current edition for the
-- jurisdiction it represents? Tier 4–6 sources (international standards,
-- national frameworks, statutory codes) bear the question; Tier 1–3
-- primary research and Co-1 lived-experience publications do not (they
-- are evaluated by supersession_check at the per-slug claim level, which
-- is a different question).
--
-- code_currency_status enum:
--   NULL                         — no code-currency check performed
--   VERIFIED-CURRENT             — confirmed current edition for jurisdiction;
--                                  re-verify annually
--   PERMANENT-FRAMEWORK          — foundational framework reference that does
--                                  not get revised on the same cadence
--                                  (e.g., CRPD treaty, ICF classification,
--                                  WHO Child Growth Standards); no annual
--                                  re-verification needed
--   SUPERSEDED-PENDING-REPLACEMENT — confirmed superseded by a newer edition;
--                                  row should be replaced or supplemented
--                                  in cited slugs; supersession_check rows
--                                  for the slug-specific work go separately
--   UNVERIFIED-CHECK-DEFERRED    — explicitly deferred to jurisdiction-tracker
--                                  (e.g., T6 codes flagged in MOB Pass-2
--                                  supersession audit as out-of-scope per
--                                  DR-2026-05-24)
--
-- code_currency_verified_at: ISO date 'YYYY-MM-DD' of last verification
-- (or NULL). The code_currency_audit.py script suppresses rows where
-- code_currency_verified_at is within the last 365 days AND
-- code_currency_status IN ('VERIFIED-CURRENT', 'PERMANENT-FRAMEWORK').
--
-- code_currency_verified_by_session: session that performed the check.
--
-- code_currency_notes: human-readable note recording the evidence basis
-- of the currency determination (URL to MVV TB / building-act reference /
-- standards-body announcement / etc).

ALTER TABLE evidence_sources ADD COLUMN code_currency_status TEXT;
ALTER TABLE evidence_sources ADD COLUMN code_currency_verified_at TEXT;
ALTER TABLE evidence_sources ADD COLUMN code_currency_verified_by_session TEXT;
ALTER TABLE evidence_sources ADD COLUMN code_currency_notes TEXT;

-- CHECK constraint enforced at audit-script level rather than DB level
-- because adding CHECK to ALTER TABLE in SQLite requires table-rebuild.
-- code_currency_audit.py validates the enum.

PRAGMA user_version = 16;
