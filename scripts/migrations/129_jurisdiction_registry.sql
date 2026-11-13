-- 129_jurisdiction_registry.sql
-- SCHEMA migration -- the declared jurisdiction vocabulary moves from an enum in code
-- (schemas/enums.py JurisdictionCode) to a base table the writers read: base_jurisdictions.
-- Tooling (IMP-17, workplan T-024); no research rows.
--
-- WHY. A jurisdiction was added by editing code, and the pairs lang_jur_map says are owed
-- name jurisdictions the code refuses, so a search for a declared pair could not be logged
-- with its jurisdiction and coverage could never read complete. Now a code is admitted with
-- `db.py add-jurisdiction`, which writes a row naming the ledger entry that approves it.
--
-- THE SEED is every member of JurisdictionCode at the base of this change, nothing else:
-- `meta` for the four codes the enum itself called meta-codes (ISO, EU, INT, UN), `country`
-- for the rest. parent_code, admission_ref and created_* are NULL on them: no single ledger
-- heading admitted the seeded set (the enum's comments cite several rulings and, for the
-- first group, jurisdiction-tracker 4.7.3, which is not a ledger entry), so naming one
-- would be a guess. A NULL admission_ref therefore marks exactly the seeded set; this
-- header is its record. UN is seeded because the table is the vocabulary a row may carry,
-- not the research scope: OD-04's "UN: out" is recorded on lang_jur_map.scope_status, and
-- search_executions already holds rows with jurisdiction 'UN'.
--
-- KIND is `country`, `sub-national` or `meta`; a sub-national code names its parent country
-- in parent_code (a pointer, rule 5), and the table CHECK binds the pointer to that kind.
-- A sub-national code is written <parent>-<subdivision> (ISO 3166-2), England under the
-- project's UK prefix, never GB (governance/jurisdiction-philosophy.md 3.3). No sub-national
-- row is seeded here.
--
-- NO FOREIGN KEY ON lang_jur_map.jurisdiction. A column carries one foreign key for all its
-- rows, and lang_jur_map holds codes this table does not (the candidate jurisdictions the
-- project may expand into; list them with the command in workplan T-024 section 3), so a
-- foreign key would fail PRAGMA foreign_key_check on those rows. Admitting those codes or
-- removing their pairs is a decision on scope and is the owner's. `db.py coverage` reports
-- them under jurisdictions_unreachable, which now reads this table.
--
-- COVERAGE ROLLS A SUB-NATIONAL SEARCH UP TO ITS COUNTRY (OD-04, owner 2026-11-12):
-- COALESCE(b.parent_code, se.jurisdiction) over LEFT JOIN base_jurisdictions b, never a list.
-- Applied to the four views that group by, or compare, a search's jurisdiction. With no
-- sub-national row they render the same rows as before. v_research_scope (lang_jur_map holds
-- no sub-national pair) and v_coverage_language (not keyed on jurisdiction) are unchanged.
--
-- READERS: dbcore.declared_jurisdictions (so check_jurisdiction, jurisdiction_declared,
-- jurisdiction_db_vocabulary, validate_jurisdiction), the four views below, db.py
-- get_coverage_completeness and _in_research_scope. WRITER: db.py add-jurisdiction.
-- STAGE: base.

CREATE TABLE base_jurisdictions (
    jurisdiction_code  TEXT PRIMARY KEY
                       CHECK (jurisdiction_code = UPPER(jurisdiction_code)
                              AND jurisdiction_code NOT LIKE 'GB%'),
    kind               TEXT NOT NULL CHECK (kind IN ('country', 'sub-national', 'meta')),
    parent_code        TEXT REFERENCES base_jurisdictions(jurisdiction_code),
    admission_ref      TEXT,
    created_at         TEXT,
    created_by_session TEXT,
    CHECK ((kind = 'sub-national') = (parent_code IS NOT NULL))
);

INSERT INTO base_jurisdictions (jurisdiction_code, kind) VALUES
    ('AU', 'country'), ('BD', 'country'), ('BE', 'country'), ('BR', 'country'),
    ('CA', 'country'), ('CH', 'country'), ('CN', 'country'), ('DE', 'country'),
    ('DK', 'country'), ('EG', 'country'), ('ES', 'country'), ('EU', 'meta'),
    ('FI', 'country'), ('FR', 'country'), ('HR', 'country'), ('ID', 'country'),
    ('IE', 'country'), ('IN', 'country'), ('INT', 'meta'), ('ISO', 'meta'),
    ('IT', 'country'), ('JP', 'country'), ('KE', 'country'), ('KR', 'country'),
    ('NG', 'country'), ('NL', 'country'), ('NO', 'country'), ('NZ', 'country'),
    ('PT', 'country'), ('SE', 'country'), ('SG', 'country'), ('UG', 'country'),
    ('UK', 'country'), ('UN', 'meta'), ('US', 'country'), ('ZA', 'country');

DROP VIEW v_coverage_jurisdiction;
CREATE VIEW v_coverage_jurisdiction AS
SELECT slug, COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction,
       COUNT(*) AS searches, SUM(results_admitted) AS admitted,
       MAX(depth_method='systematic') AS reached_systematic,
       MAX(saturation_signal='saturated') AS saturated
FROM search_executions se
LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
WHERE deferred_reason IS NULL
GROUP BY 1, 2;

DROP VIEW v_coverage_branch;
CREATE VIEW v_coverage_branch AS
SELECT slug, COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction,
       target_tier, target_evidence_type, target_scope,
       COUNT(*) AS targeted_searches, SUM(results_admitted) AS admitted
FROM search_executions se
LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
WHERE deferred_reason IS NULL
GROUP BY 1,2,3,4,5;

DROP VIEW v_coverage_lens;
CREATE VIEW v_coverage_lens AS
SELECT slug, parameter_id, COALESCE(b.parent_code, se.jurisdiction) AS jurisdiction, language,
       identity_code, icf_code, needs_code, medical_code,
       SUM(deferred_reason IS NULL) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
FROM search_executions se
LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8;

DROP VIEW v_coverage_priority;
CREATE VIEW v_coverage_priority AS
SELECT
    s.slug,
    ljm.jurisdiction,
    ljm.language,
    ljm.role,
    ( (CASE ljm.role WHEN 'PRIMARY' THEN 3 ELSE 1 END)
      + (CASE WHEN (SELECT COUNT(*) FROM search_executions se2
                    WHERE se2.slug = s.slug AND se2.deferred_reason IS NULL) = 0
              THEN 2 ELSE 0 END)
    ) AS priority_score,
    (SELECT COUNT(*) FROM search_executions se3
     WHERE se3.slug = s.slug AND se3.deferred_reason IS NULL) AS slug_searches
FROM slugs s
JOIN v_research_scope ljm        -- CROSS JOIN: every in-scope slug x every owed (lang,jur)
WHERE s.status IN ('ACTIVE', 'STUB')
  AND NOT EXISTS (
      SELECT 1 FROM search_executions se
      LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction
      WHERE se.slug = s.slug
        AND COALESCE(b.parent_code, se.jurisdiction) = ljm.jurisdiction
        AND UPPER(se.language) = ljm.language
  );

PRAGMA user_version = 129;
