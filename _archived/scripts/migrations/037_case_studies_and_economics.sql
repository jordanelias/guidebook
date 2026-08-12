-- 037_case_studies_and_economics.sql
-- Build the MISSING tables for case studies and economics.
--
-- WHY (owner challenge 2026-07-24): schemas/case_study.py (CaseStudy, CaseStudyOutcome) and
-- schemas/economics.py (EconomicsEntry) have existed as fully-specified Pydantic models — with
-- validators, pillars, entry types, BCR, currency, evidence tiers — but NO corresponding SQLite
-- table was ever built. CLAUDE.md §10 is explicit that "schemas/*.py <-> SQLite drift is a bug,
-- not a convention". Eight ACTIVE slugs depend on this layer:
--   residential-accessible-home-case-studies, cross-population-case-studies,
--   case-study-economics-financial-data, accessible-design-economics-cost-premium,
--   economics-sources, government-grant-programmes, government-grant-programmes-home-adaptation,
--   jurisdiction-grant-programmes-comprehensive
-- Consequence of the gap: economic findings surfaced by this session's searches (universal-design
-- cost premium 0-2% vs retrofit 20-50%; IE Housing Adaptation Grant EUR30,000 cap; Rick Hansen /
-- Conference Board of Canada business-case BCR work) had nowhere to land and survived only as
-- prose. This migration gives them a home.
--
-- Mirrors the Pydantic models exactly; list-valued fields become junction tables (the established
-- idiom in this DB, cf. item_population_links / citation_population_links).
--
-- Schema-only, additive; ships empty. The runner sets PRAGMA user_version to 37.

BEGIN;

-- ---------- Economics ----------
CREATE TABLE economics_entries (
  entry_id        TEXT PRIMARY KEY,            -- ECON-NNNN / HO-NNN / CP-NNN
  pillar          TEXT NOT NULL CHECK (pillar IN ('health','inaction','construction','market')),
  entry_type      TEXT NOT NULL CHECK (entry_type IN
                    ('cost_premium','retrofit_multiplier','grant_programme','health_outcome',
                     'market_value','housing_deficit','research_gap')),
  source          TEXT NOT NULL,               -- citation reference (REF-ID where available)
  ref_id          TEXT REFERENCES evidence_sources(ref_id),  -- structured link when admitted
  jurisdiction    TEXT,                        -- ISO code or 'MULTI'
  finding         TEXT NOT NULL,
  study_design    TEXT,
  sample          TEXT,
  value_numeric   REAL,
  value_unit      TEXT,                        -- '%','currency','ratio','years'
  currency        TEXT,                        -- ISO currency code
  bcr             TEXT,                        -- benefit-cost ratio
  evidence_tier   INTEGER CHECK (evidence_tier IS NULL OR evidence_tier BETWEEN 1 AND 6),
  confidence      TEXT CHECK (confidence IS NULL OR confidence IN ('HIGH','MODERATE','LOW')),
  source_section  TEXT,                        -- clause/section/page for coded or statutory values
  quant_status    TEXT CHECK (quant_status IS NULL OR quant_status IN
                    ('VERIFIED-QUANT','UNVERIFIED-QUANT')),  -- CLAUDE.md §6 discipline
  year            INTEGER,
  journal         TEXT,
  status          TEXT NOT NULL DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL,
  created_by_session TEXT NOT NULL,
  updated_at      TEXT,
  updated_by_session TEXT
) STRICT;
CREATE INDEX ix_econ_pillar ON economics_entries(pillar, entry_type);
CREATE INDEX ix_econ_juris  ON economics_entries(jurisdiction);

CREATE TABLE economics_entry_specs (          -- EconomicsEntry.specification_refs
  entry_id  TEXT NOT NULL REFERENCES economics_entries(entry_id),
  item_code TEXT NOT NULL REFERENCES items(item_code),
  PRIMARY KEY (entry_id, item_code)
) STRICT;

CREATE TABLE economics_entry_populations (    -- EconomicsEntry.population_codes
  entry_id        TEXT NOT NULL REFERENCES economics_entries(entry_id),
  population_code TEXT NOT NULL REFERENCES populations(population_code),
  PRIMARY KEY (entry_id, population_code)
) STRICT;

-- ---------- Case studies ----------
CREATE TABLE case_studies (
  case_study_id   TEXT PRIMARY KEY,            -- CS-NNNN (validator-enforced in the model)
  slug            TEXT NOT NULL,
  title           TEXT NOT NULL,
  building_type   TEXT NOT NULL,
  location        TEXT NOT NULL,
  architect       TEXT,
  year            INTEGER,
  setting         TEXT,
  population_description TEXT,
  evidence_quality_tier  INTEGER CHECK (evidence_quality_tier IS NULL
                                        OR evidence_quality_tier BETWEEN 1 AND 3),
  cost_data       TEXT,
  cost_data_quality TEXT CHECK (cost_data_quality IS NULL OR cost_data_quality IN
                     ('VERIFIED','PROVISIONAL','GREY')),
  part_section    TEXT,                        -- e.g. §12.01
  limitations     TEXT,                        -- REQUIRED in practice: what this case cannot show
  harm_finding    INTEGER NOT NULL DEFAULT 0 CHECK (harm_finding IN (0,1)),  -- failure/inadequacy case
  status          TEXT NOT NULL DEFAULT 'active',
  notes           TEXT,
  created_at      TEXT NOT NULL,
  created_by_session TEXT NOT NULL,
  updated_at      TEXT,
  updated_by_session TEXT
) STRICT;
CREATE INDEX ix_cs_slug ON case_studies(slug);
CREATE INDEX ix_cs_harm ON case_studies(harm_finding);

CREATE TABLE case_study_outcomes (            -- CaseStudyOutcome (one-to-many)
  outcome_id    INTEGER PRIMARY KEY,
  case_study_id TEXT NOT NULL REFERENCES case_studies(case_study_id),
  metric        TEXT NOT NULL,
  value         TEXT,
  source        TEXT,                          -- how it was verified
  tier          INTEGER CHECK (tier IS NULL OR tier BETWEEN 1 AND 3)
) STRICT;

CREATE TABLE case_study_populations (         -- CaseStudy.primary_populations
  case_study_id   TEXT NOT NULL REFERENCES case_studies(case_study_id),
  population_code TEXT NOT NULL REFERENCES populations(population_code),
  PRIMARY KEY (case_study_id, population_code)
) STRICT;

CREATE TABLE case_study_specs (               -- CaseStudy.specification_refs
  case_study_id TEXT NOT NULL REFERENCES case_studies(case_study_id),
  item_code     TEXT NOT NULL REFERENCES items(item_code),
  PRIMARY KEY (case_study_id, item_code)
) STRICT;

CREATE TABLE case_study_strategies (          -- CaseStudy.design_strategies (prose list)
  strategy_id   INTEGER PRIMARY KEY,
  case_study_id TEXT NOT NULL REFERENCES case_studies(case_study_id),
  strategy      TEXT NOT NULL
) STRICT;

COMMIT;
