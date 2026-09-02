-- 066_research_code_leads.sql
-- SCHEMA migration — the research-stage home for code and standard leads.
--
-- WHAT THE OWNER RULED, 2026-09-02, choosing between three options put to them:
--     "restore as research_code_leads"
--
-- This EXECUTES D-0181 (2026-08-31) rather than superseding it. That decision already
-- called these rows research and already named this table: "jurisdictional_values holds
-- 109 rows and is renamed research_code_leads by the parked migration 065". The rename
-- never happened — migration slot 065 was consumed by the four-lens link table on
-- 2026-09-01 — and on the same day the owner's base-and-research-only ruling emptied
-- jurisdictional_values as a side effect of deleting the item layer, because its
-- item_code column is NOT NULL REFERENCES items.
--
-- DR-2026-08-19 §1.5 had demanded exactly the opposite sequencing: the
-- jurisdictional_values consequence must be decided "as its own decision, before `items`
-- is touched… It must not be collateral damage." It was collateral damage. This migration
-- and D-0185 are the repair, and the record says so rather than tidying it away.
--
-- WHAT IS RESTORED, MEASURED. The 109 archived records carry exactly three non-null
-- columns — item_code, jurisdiction, standard_name — because the 2026-08-12 REFERENCE-ONLY
-- ruling cleared every value field ("it names which document to go and get, never what it
-- says"). Collapsed on (jurisdiction, standard_name) they are 83 distinct leads across 12
-- jurisdictions; the other 26 rows are the same standard listed against a different item.
-- So 100% of the surviving information is item-independent, and the ONLY thing dropped in
-- the move is the item link — which is the thing the owner ruled must not exist. The
-- item mapping survives in the archived filenames (a-3_e08.yaml -> E-08) for provenance,
-- and is deliberately absent from the live frame so it cannot presuppose a research answer.
--
-- WHY A NEW TABLE AND NOT source_locators. source_locators is the DOI-shaped lead store,
-- and it already demonstrates what happens when two identifier shapes share one row
-- format: 24 of its rows carry BOTH a standard_number AND a DOI, and a standard has no
-- DOI. That misalignment is the same defect that made REF-00037 carry a PLoS ONE DOI
-- against a RIBA housing-guide title, which falsely blocked an admission on 2026-09-01.
-- This table therefore has NO DOI COLUMN AT ALL — not as discouragement but as a
-- structural impossibility — and makes jurisdiction mandatory, which source_locators
-- cannot do (its jurisdiction column has degraded into a free-text field holding URLs,
-- prose findings and quantified claims).
--
-- WHY THIS IS NOT A RULE-5 DUAL HOME. Rule 5 forbids writing the same FACT into a second
-- table. After this migration a code lead lives in exactly one place. The 11 standards
-- that also appear in source_locators.standard_number are reconciliation debt, recorded
-- as such, not a licence to duplicate.
--
-- WHAT THIS MIGRATION DOES NOT DO, AND WHY. It does not DROP jurisdictional_values.
-- That table is now empty, but v_code_floor_only reads it — and CLAUDE.md holds a
-- cross-stage view to be "the most protected object in the schema", the pointer that
-- rule 5's point-don't-copy actually means in SQL. That view joins on item_code, a
-- column the owner ruled out of existence, so deciding what v_code_floor_only becomes is
-- its own question and is owed. Dropping a table whose protected view has no agreed
-- successor, inside the migration that restores its data, is how one repair becomes two
-- defects. The empty table and the drop are recorded as owed in D-0185.

CREATE TABLE research_code_leads (
    lead_id             INTEGER PRIMARY KEY,

    -- The two facts that survived the REFERENCE-ONLY ruling. Both mandatory: a lead that
    -- cannot say which jurisdiction it belongs to is not retrievable, and that is the
    -- whole purpose of the row.
    jurisdiction        TEXT NOT NULL,
    standard_name       TEXT NOT NULL,

    -- The locator R3 asks of a code value: "clause/section/page". NULL until someone
    -- actually retrieves the document — which is the work this table exists to queue.
    clause              TEXT,

    status              TEXT NOT NULL DEFAULT 'REFERENCE-ONLY'
                        CHECK (status IN ('REFERENCE-ONLY', 'RETRIEVED', 'SUPERSEDED')),

    recovered_from      TEXT,
    notes               TEXT,

    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,

    -- The dedup the old shape could not express: 109 rows were 83 leads because the same
    -- standard was restated per item. Keyed on the lead itself, that restatement is
    -- impossible rather than merely discouraged.
    UNIQUE (jurisdiction, standard_name)
);

-- NO CHECK ON jurisdiction, DELIBERATELY. The vocabulary's nearest live home is
-- lang_jur_map.jurisdiction (70 rows), and two of the twelve values this table restores —
-- 'GB' and 'ISO' — are absent from it, 'ISO' because it is a standards body rather than a
-- country. A hardcoded CHECK list here would be a second home for a vocabulary that
-- belongs in one place, which is rule 5 in the shape it is easiest to commit by accident.
-- Registering a real jurisdiction vocabulary and pointing both at it is owed, not faked.

CREATE INDEX ix_rcl_jurisdiction ON research_code_leads (jurisdiction);
CREATE INDEX ix_rcl_standard     ON research_code_leads (standard_name);

PRAGMA user_version = 66;
