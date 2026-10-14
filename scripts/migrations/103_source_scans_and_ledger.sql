-- 103_source_scans_and_ledger.sql
-- SCHEMA migration — a record of each READING of a source, and the source-by-parameter
-- ledger derived from it. Tooling T1 (owner approval D8, 2026-10-09);
-- catalogue-plan-v2 section 3.8, critique finding F13.
--
-- THE GAP. Nothing recorded which source had been read for which parameter. A parameter
-- promoted in month three was never looked for in month one's sources, and the catalogue
-- could imply "no code sets a requirement" where nobody had read the code for that
-- quantity -- while every gate read green. That is how GAP-061's lost figures happened.
-- The owner's requirement it answers, 2026-10-09: "Ensure that we can add and expand
-- parameter catalogue as required based on new information we come across."
--
-- ONE ROW PER READING, NOT ONE ROW PER (SOURCE, PARAMETER). Parameter numbers are never
-- reused (base_parameters is AUTOINCREMENT, migration 076), so a reading that stores the
-- highest parameter_id existing when it was made says exactly which parameters it could
-- have covered: "catalogue version N" means "parameters 1..N, those active at the time".
-- Silence is then DERIVED by the view below; nobody writes an `absent` extraction for
-- every pair, and explicit `absent` rows stay for positive statements of absence.
--
-- `catalogue_version` IS COMPUTED BY THE WRITER, NEVER TYPED (CLAUDE.md rule 8):
-- `db.py record-scan` reads MAX(parameter_id) at call time and refuses a typed value.
-- `pages_read`/`pages_total` are computed the same way, from the page markers of the
-- file read (retrieval_log.page_coverage), and `file_sha256` must name a file the
-- retrieval-log manifests hold for this source. The CHECKs below hold the invariants for
-- every writer, including a data migration that does not go through db.py.
--
-- STAGE: evidence (governance/stage-map.yaml) -- what was read of an admitted source,
-- beside its extraction rows.
--
-- WHAT READS IT (CLAUDE.md section 8): `v_scan_ledger` below; the batch rule R16-scan in
-- scripts/audit/research_batch_dod.py (every admission has a catalogue-mode reading);
-- scripts/audit/scan_debt.py through the view. Not built and not read here: a reading
-- does not prove the reader saw everything -- adversarial standing subject 4 samples
-- each source for figures no row carries.

CREATE TABLE source_scans (
    -- AUTOINCREMENT, as 076 did for the other ids a record names: a scan_id is cited by
    -- session records and must never come to mean a different reading.
    scan_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_id              TEXT    NOT NULL REFERENCES evidence_sources(ref_id),
    -- catalogue: every active parameter up to catalogue_version.
    -- targeted:  one parameter, target_parameter_id (a back-fill reading).
    mode                TEXT    NOT NULL CHECK (mode IN ('catalogue', 'targeted')),
    catalogue_version   INTEGER NOT NULL CHECK (catalogue_version >= 1),
    target_parameter_id INTEGER REFERENCES base_parameters(parameter_id),
    -- full: the whole document. partial: some pages of it. fragment: one page or clause
    -- of a larger instrument. abstract: an abstract or metadata record only.
    text_scope          TEXT    NOT NULL CHECK (text_scope IN
                                ('full', 'partial', 'fragment', 'abstract')),
    pages_read          INTEGER CHECK (pages_read IS NULL OR pages_read >= 0),
    pages_total         INTEGER CHECK (pages_total IS NULL OR pages_total >= 1),
    -- Which saved file was read, by checksum: the manifest's own sha256 of the bytes.
    file_sha256         TEXT    NOT NULL CHECK (length(file_sha256) = 64),
    -- Whether the open pass (quantities the catalogue lacks, plan section 3.4) was done
    -- in this reading.
    open_pass_done      INTEGER NOT NULL DEFAULT 0 CHECK (open_pass_done IN (0, 1)),
    -- full-read: the text was read against the list. pre-screen: only a script listed
    -- where catalogue terms occur -- weaker, and v_scan_ledger says which it was.
    method              TEXT    NOT NULL CHECK (method IN ('full-read', 'pre-screen')),
    notes               TEXT,
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    CHECK ((mode = 'targeted' AND target_parameter_id IS NOT NULL)
        OR (mode = 'catalogue' AND target_parameter_id IS NULL)),
    CHECK (pages_read IS NULL OR pages_total IS NULL OR pages_read <= pages_total),
    -- "full" over a paged text means every page; a reading of fewer pages is partial.
    CHECK (text_scope <> 'full' OR pages_read IS NULL OR pages_read = pages_total)
);

CREATE INDEX idx_source_scans_ref ON source_scans(ref_id);

CREATE VIEW v_scan_ledger AS
-- v_scan_ledger: one row per (source in scope) x (active parameter).
--
--   source in scope   evidence_sources with superseded_by_ref_id IS NULL. A tombstone is
--                     never read again; its replacement is.
--   active parameter  base_parameters.status = 'active'. Retired and merged parameters
--                     leave the ledger (their extractions stay, as history).
--
-- STATUS PRECEDENCE, first match wins:
--   1 EXTRACTED          a non-absent extraction exists for the pair (any figure_role).
--   2 STATED-ABSENT      only claim_type 'absent' extractions exist: the source addresses
--                        the quantity and sets nothing -- a positive statement.
--   3 READ-NOTHING-FOUND a FULL-scope reading covers the pair and found no row.
--   4 READ-PARTIAL       only partial / fragment / abstract readings cover it.
--   5 NOT-READ           no reading covers it.
-- A reading COVERS a pair when it is catalogue-mode with catalogue_version >=
-- parameter_id (the parameter existed when the reading was made), or targeted at that
-- parameter. Rows 1 and 2 win over readings because a row written is stronger evidence
-- than a reading recorded; 3 wins over 4 because a full reading supersedes a partial
-- one of the same source.
--
-- scan_id / text_scope / method name the STRONGEST covering reading (full scope first,
-- then full-read before pre-screen, then the latest), so a READ-NOTHING-FOUND resting on
-- a pre-screen only is visible as such. NULL when no reading covers the pair.
WITH pairs AS (
    SELECT e.ref_id, p.parameter_id
      FROM evidence_sources e
     CROSS JOIN base_parameters p
     WHERE e.superseded_by_ref_id IS NULL
       AND p.status = 'active'
),
best AS (
    SELECT pr.ref_id, pr.parameter_id,
           (SELECT s.scan_id FROM source_scans s
             WHERE s.ref_id = pr.ref_id
               AND ((s.mode = 'catalogue' AND s.catalogue_version >= pr.parameter_id)
                 OR (s.mode = 'targeted' AND s.target_parameter_id = pr.parameter_id))
             ORDER BY (s.text_scope = 'full') DESC, (s.method = 'full-read') DESC,
                      s.scan_id DESC
             LIMIT 1) AS scan_id
      FROM pairs pr
)
SELECT b.ref_id,
       b.parameter_id,
       CASE
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type <> 'absent') THEN 'EXTRACTED'
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type = 'absent') THEN 'STATED-ABSENT'
         WHEN s.text_scope = 'full' THEN 'READ-NOTHING-FOUND'
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         ELSE 'NOT-READ'
       END AS status,
       b.scan_id,
       s.text_scope,
       s.method
  FROM best b
  LEFT JOIN source_scans s ON s.scan_id = b.scan_id;

PRAGMA user_version = 103;
