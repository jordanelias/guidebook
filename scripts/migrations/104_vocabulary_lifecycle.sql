-- 104_vocabulary_lifecycle.sql
-- SCHEMA migration — the parameter vocabulary can be corrected, not only grown.
-- Tooling T1 (owner approval D8, 2026-10-09); catalogue-plan-v2 section 4, critique F5,
-- and the owner's D3 follow-up of the same evening.
--
-- THREE CHANGES, each with its reader.
--
-- (1) A DECLINATION CAN BE REVOKED, and the revocation is recorded on the row.
--     Migration 101 shipped `parameter_declinations` with "no un-decline verb: reversing
--     a declination is a recorded decision plus a compensating migration, and nothing
--     reads an un-decline yet". The catalogue plan names the reader: the cohort's
--     vocabulary review, which may find a declined term is a quantity after all. The
--     row stays (retire in place, owner ruling 2026-09-16, "retire in place then"): a
--     revoked declination is history, and every reader treats it as absent --
--     `insert_parameter`'s declined-term refusal, research_batch_dod.py R16's
--     'disposed' predicate, and the adversarial skill's declination query.
--     The three columns are all-or-nothing, the shape determination_gates uses for its
--     resolution triple, and the CHECK sits on the last column added so SQLite can
--     evaluate it against both siblings (the 078 precedent for ADD COLUMN checks).
--     `db.py revoke-declination` also requires a decision reference; it is written into
--     revocation_reason, not a column of its own, because nothing machine-reads it.
--
-- (2) A TERM MINTED FROM A PERMITTED CATALOGUE CARRIES ITS PROVENANCE. Owner, 2026-10-09:
--     "D3 for parameter terms? it can be pulled from previous catalogues of entries for
--     prepopulating", then, from listed options, the catalogues "Code and standards
--     registries" and "Old corpus terms" (the old Part 4 item names were offered and NOT
--     selected), and the guard "Screen, then you approve". `insert_term` mints only from
--     an observation, so `db.py mint-term-from-catalogue` is the route, and this table is
--     where the catalogue, the entry and the owner's approving words are recorded
--     against the term. One row per term (PRIMARY KEY): a term has one origin.
--
--     THE CATALOGUE CHECK LISTS THE FILES THE LEDGER NAMES FOR THE OWNER'S SELECTION, and
--     nothing else: "Code and standards registries" is references/standards-registry.md
--     and the three verified-source files; "Old corpus terms" is the `terms` table of
--     _archived/data/corpus-pre-reset-2026-08-06.db. The value IS the file path, so the
--     writer resolves `entry_ref` inside the file the CHECK names, with no second list.
--     ADDING A CATALOGUE IS A SCHEMA CHANGE AND AN OWNER RULING, never a CLI argument:
--     the owner chose these and refused the item names, and a list this short is the
--     ruling, mechanised.
--
--     Its reader: scripts/validate_parameters.py (P2), which fails a catalogue-origin row
--     whose approval quote is no longer in references/project-standards.md.
--
-- (3) v_value_independence LISTS ACTIVE PARAMETERS ONLY. It groups extractions by
--     parameter, and a retired parameter keeps its extractions as history, so without a
--     filter a retired parameter would still be listed as a subject with independent
--     roots. A merged parameter's extractions are re-pointed by merge-parameter, so it
--     drops out either way. Recreated verbatim from the live definition plus the one
--     predicate (CLAUDE.md rule 4: a view is a caller of the table it filters). The
--     other views that join base_parameters read live determinations only, and neither
--     retire-parameter nor merge-parameter permits a live determination on the parameter
--     they change, while assess_cell refuses to determine an inactive one.

ALTER TABLE parameter_declinations ADD COLUMN revoked_at TEXT;
ALTER TABLE parameter_declinations ADD COLUMN revoked_by_session TEXT;
ALTER TABLE parameter_declinations ADD COLUMN revocation_reason TEXT
    CHECK ((revoked_at IS NULL AND revoked_by_session IS NULL AND revocation_reason IS NULL)
        OR (revoked_at IS NOT NULL AND revoked_by_session IS NOT NULL
            AND length(trim(revocation_reason)) > 0));

CREATE TABLE term_catalogue_origins (
    term_id             TEXT PRIMARY KEY REFERENCES terms(term_id),
    catalogue           TEXT NOT NULL CHECK (catalogue IN ('references/standards-registry.md', 'references/tier456-verified-sources.json', 'references/co1-verified-sources.json', 'references/co2-verified-sources.json', '_archived/data/corpus-pre-reset-2026-08-06.db')),
    -- The entry the name was taken from, resolvable inside the catalogue file: a
    -- registry `standard_cited` value, a verified-source `ref_id`, or `terms:<TERM-ID>`
    -- in the archived corpus. A pointer, never a copy of the entry (rule 5).
    entry_ref           TEXT NOT NULL CHECK (length(trim(entry_ref)) > 0),
    -- The owner's approving words, verbatim, found exactly once in
    -- references/project-standards.md when the term was minted.
    approval_quote      TEXT NOT NULL CHECK (length(trim(approval_quote)) > 0),
    rationale           TEXT NOT NULL CHECK (length(trim(rationale)) > 0),
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL
);

DROP VIEW v_value_independence;
CREATE VIEW v_value_independence AS
    SELECT sve.parameter_id,
           t.canonical_en AS parameter_label,
           COUNT(DISTINCT COALESCE(sve.root_ref_id, sve.root_id)) AS independent_root_count
    FROM source_value_extractions sve
    JOIN base_parameters p ON p.parameter_id = sve.parameter_id
    JOIN terms t           ON t.term_id      = p.term_id
    WHERE sve.root_type IN ('measurement_primary', 'participatory_finding',
                            'derived_calculation')
      AND (sve.root_ref_id IS NOT NULL
           OR sve.root_id IN (SELECT root_id FROM external_root_registry))
      -- 104: active parameters only; a retired parameter's extractions are history.
      AND p.status = 'active'
    GROUP BY sve.parameter_id, t.canonical_en;

PRAGMA user_version = 104;
