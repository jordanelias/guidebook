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
-- would be a guess. A NULL admission_ref therefore marks exactly the seeded set, and a seed
-- row never carries a session (the migration wrote it); scripts/audit/jurisdiction_db_vocabulary.py
-- reports a row with no admission_ref that does, and a pointer no ledger heading answers.
-- This header is the seed's record. UN is seeded because the table is the vocabulary a row may carry,
-- not the research scope: OD-04's "UN: out" is recorded on lang_jur_map.scope_status, and
-- search_executions already holds rows with jurisdiction 'UN'.
--
-- THE SEED'S PROVENANCE, quoted verbatim from schemas/enums.py JurisdictionCode as the
-- last commit that declared it left it (the comments that named the ruling behind each
-- admission; the enum is deleted in this change and git history is not a place a reader
-- looks):
--
--       # Admitted 2026-09-18 (owner ruling). Each was already live in the corpus
--       # tables while absent from this enum, so the declared vocabulary could not be
--       # used to gate the column it describes.
--       BE = "BE"   # Belgium -- REF-00995 (Flemish decree), REF-00996 (Handboek Toegankelijkheid)
--       ES = "ES"   # Spain -- search_executions (CTE DB-SUA line of enquiry)
--       HR = "HR"   # Croatia -- REF-01001 (Lepoglavec 2023)
--       IT = "IT"   # Italy -- search_executions
--
--       # Admitted 2026-10-01, executing the owner ruling of 2026-09-28 ("jurisdiction
--       # scope: buckets 1-2 exhausted before reaching further", references/
--       # project-standards.md). PT and FI are named Bucket-2 members and UN a Bucket-1
--       # member of that ruling, which calls UN's absence from this enum "a tooling gap
--       # (rule 10: fix in its own PR)". Where each is live:
--       #     select jurisdiction, count(*) from <table> where jurisdiction in
--       #         ('PT','FI','UN','UG') group by 1;
--       PT = "PT"   # Portugal -- Bucket 2
--       FI = "FI"   # Finland -- Bucket 2
--       UN = "UN"   # United Nations -- Bucket 1. A meta-code like ISO and EU, not a country.
--       # UG is NOT in either bucket and is admitted by owner decision D2, approved 2026-10-01
--       # (references/project-standards.md, grep "plan's decisions D1–D4 approved"): declared
--       # for PR #165's rows, which are not unwound; outside research scope by the 2026-09-28
--       # ruling. This enum is the declared vocabulary of rows held, not the canonical list --
--       # so declaring UG licenses no further Ugandan research; the ruling, not this list,
--       # sets research scope.
--       UG = "UG"   # Uganda
--
--       # Meta-codes (not individual countries)
--       ISO = "ISO"   # ISO international standards
--       EU = "EU"     # European Union directives
--       INT = "INT"   # International / no single jurisdiction. DISTINCT FROM ISO: ISO
--       #               means an ISO-published standard, INT means the work spans
--       #               jurisdictions without being one -- REF-00994 (IPC Accessibility
--       #               Guide) and REF-00977 (a review searched across three databases).
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
    -- THE SHAPE OF A CODE, held by the table where a table can hold it: upper-case letters,
    -- digits and at most one dash, with a letter first; the GB prefix is the ruled rejected
    -- spelling (UK is the project's code). The dash belongs to a sub-national code and to
    -- no other kind, and a sub-national code is exactly <parent_code>-<a non-empty
    -- subdivision>. That the parent is a `country` cannot be a CHECK (it reads another
    -- row); the writer, db.py add-jurisdiction, refuses it.
    jurisdiction_code  TEXT PRIMARY KEY
                       CHECK (jurisdiction_code = UPPER(jurisdiction_code)
                              AND jurisdiction_code NOT LIKE 'GB%'
                              AND jurisdiction_code GLOB '[A-Z]*'
                              AND jurisdiction_code NOT GLOB '*[^A-Z0-9-]*'
                              AND jurisdiction_code NOT GLOB '*-*-*'
                              AND jurisdiction_code NOT GLOB '*-'),
    kind               TEXT NOT NULL CHECK (kind IN ('country', 'sub-national', 'meta')),
    parent_code        TEXT REFERENCES base_jurisdictions(jurisdiction_code),
    admission_ref      TEXT,
    created_at         TEXT,
    created_by_session TEXT,
    CHECK ((kind = 'sub-national') = (parent_code IS NOT NULL)),
    CHECK ((kind = 'sub-national') = (jurisdiction_code LIKE '%-%')),
    CHECK (kind <> 'sub-national'
           OR (substr(jurisdiction_code, 1, length(parent_code) + 1) = parent_code || '-'
               AND length(jurisdiction_code) > length(parent_code) + 1))
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
