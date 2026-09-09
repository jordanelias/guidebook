-- 068_concept_vocabulary_harvest.sql
-- SCHEMA migration — the concept vocabulary gets the harvest D-0173 ordered.
--
-- OWNER RULING 2026-09-03: "harvest now and as you go". That closes the question the
-- programme's §6 had answered for itself with a blanket "no new tables and no new
-- columns" — a scope rule for one repair programme, which CLAUDE.md rule 0 makes no
-- kind of argument against a live directive. D-0173 (ADOPTED 2026-08-27, DG-NON,
-- status ACTIVE) already ORDERED this and has been owed since:
--
--   "Missing is the harvest; nothing holds terms as they appear in a source, and
--    search_executions.terms_used is the opposite direction."
--
-- terms_used records the terms we searched WITH. Nothing records the terms a source
-- turned out to USE. That gap is why the vocabulary cannot grow from evidence.
--
-- WHY TWO TABLES AND NOT ONE, which is the whole content of the ruling.
-- D-0173 resolves an aporia the owner posed: we must not presuppose our categories,
-- and we cannot research without them. Its answer is that the vocabulary "can be
-- observed but not yet adjudicated" —
--
--   "Recording that a source uses a phrase is a fact about the document, not a claim
--    that the phrase names one of our categories -- the same epistemic act as
--    recording its DOI. Judgment then adjudicates with the source in hand, and the
--    vocabulary is grown with warrant."
--
-- So observation and adjudication are DIFFERENT STAGES and must not share a row.
-- observed_terms is EVIDENCE: it says what the document says, and carries no term_id,
-- because a term_id would be exactly the claim the ruling forbids at this point.
-- term_adjudications is JUDGMENT: it decides, with the source in hand, whether the
-- observed phrase names one of our concepts. Merging them into one table with a
-- nullable term_id would re-create the presupposition the ruling exists to prevent —
-- the row would be born already half-adjudicated.
--
-- RULE 5 THROUGHOUT. observed_terms points at evidence_sources(ref_id) and copies
-- nothing from it: no DOI, no title, no year. term_adjudications points at
-- observed_terms(observation_id) and at terms(term_id) and copies neither the surface
-- form nor the canonical name. Each stage holds its own fact and reaches the rest by
-- pointer.
--
-- DIVERGENT ADJUDICATIONS ARE DELIBERATELY PERMITTED. There is no UNIQUE on
-- observation_id: an adversarial pass that disagrees lands a SECOND row, and divergent
-- judgements read as a contest. That is the same mechanic DR-2026-08-19 §7 fixes for
-- evidence_population_match, and which CLAUDE.md §4 names as a refusal that must stay
-- absent. Do not add that constraint later without ruling on the mechanic first.
--
-- WHAT READS THESE, per CLAUDE.md §1. term_adjudications reads observed_terms by
-- foreign key; db.py's observe-term and adjudicate-term are the sanctioned writers and
-- readers; and the harvest is what R11's terms_used can finally be populated FROM,
-- which is the defect D05-002 records. The authority for adding them is the owner
-- ruling, not a burden-of-proof argument of mine.

CREATE TABLE observed_terms (
    observation_id      INTEGER PRIMARY KEY,
    -- POINTER, not a copy. The source's bibliography stays in evidence_sources.
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    -- The phrase EXACTLY as the source writes it. Not normalised, not translated,
    -- not mapped. R11 forbids back-translation and this is where that starts.
    surface_form        TEXT NOT NULL,
    -- The language the phrase APPEARS IN, which need not be the source's language.
    language            TEXT NOT NULL DEFAULT 'EN',
    -- R3's locator discipline: where in the source it appears.
    locator             TEXT,
    -- Enough surrounding text that judgment can adjudicate without re-retrieving.
    context_quote       TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    -- One observation per phrase per language per source. A second sighting of the
    -- same phrase in the same source is the same fact.
    UNIQUE (ref_id, surface_form, language)
);

CREATE TABLE term_adjudications (
    adjudication_id     INTEGER PRIMARY KEY,
    observation_id      INTEGER NOT NULL REFERENCES observed_terms(observation_id),
    -- OUTCOMES, documented HERE and not inside the CHECK. dbcore.check_values() reads
    -- this constraint's own value list to build the CLI's refusal, and an inline
    -- comment between the quoted values defeats its parser -- measured 2026-09-03,
    -- when a first cut of this migration carried the descriptions inside the IN(...)
    -- and every legitimate outcome was refused with a mangled vocabulary. The whole
    -- reason vocabularies come from the schema rather than a list in the code
    -- (CLAUDE.md §4) is defeated by punctuation the parser cannot see past.
    --
    --   NAMES-EXISTING  names a term we already hold
    --   NAMES-NEW       names a concept new to the vocabulary
    --   NOT-OURS        a real phrase, but not one of our concepts
    --   DEFERRED        cannot be settled on this source alone
    outcome             TEXT NOT NULL CHECK (outcome IN
                            ('NAMES-EXISTING','NAMES-NEW','NOT-OURS','DEFERRED')),
    term_id             TEXT REFERENCES terms(term_id),
    -- NOT NULL: an adjudication that does not say why cannot be contested, and the
    -- whole point of splitting observation from judgment is that the judgement is
    -- inspectable.
    rationale           TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    -- The outcome and the pointer must agree. An outcome that names a term must name
    -- one; an outcome that declines must not.
    CHECK (
        (outcome IN ('NAMES-EXISTING','NAMES-NEW') AND term_id IS NOT NULL)
     OR (outcome IN ('NOT-OURS','DEFERRED')        AND term_id IS NULL)
    )
);

CREATE INDEX idx_observed_terms_ref ON observed_terms(ref_id);
CREATE INDEX idx_term_adjudications_obs ON term_adjudications(observation_id);

PRAGMA user_version = 68;
