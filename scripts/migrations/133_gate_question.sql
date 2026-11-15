-- 133_gate_question.sql
-- SCHEMA migration -- a question about a published cell can be recorded as an open determination gate.
-- Tooling (workplan T-021, OD-21 resolved under delegation: yes, as an open gate); no research rows.
--
-- WHY. A reader's or the owner's objection to a published value lives only in a session file; the value stays up
-- with nothing beside it. A gate already exists for a finding that contests a cell, but it can name only an identity
-- code, takes a fixed verdict list and requires a trigger tier, so a question (which has no source and no tier)
-- could not be written, and a question about a cell keyed on an ICF, need or medical code could not name its cell.
--
-- WHAT. determination_gates gains the other three lens columns (icf_code, needs_code, medical_code, the same typed
-- foreign keys specifications carries), the verdict list gains 'QUESTION', and trigger_tier / trigger_evidence_type
-- become nullable FOR THAT VERDICT ONLY: a QUESTION carries no tier, no evidence type and no trigger source (the
-- engine reports it beside the cell and never lets it cap the cell; a tier invented for a question would let it
-- pin, or fail to pin, a cell on a strength nobody established). Every other verdict keeps its NOT NULL tier. A
-- gate is still closed only with resolved_at, resolved_by_session and resolution_rationale together (unchanged).
-- Nothing else changes; the one existing row is copied as it stands.
--
-- SQLite cannot change a CHECK or a NOT NULL in place: create, copy, drop, rename. The view and the index that name
-- the table are recreated (v_open_determination_gates now also carries the three lens columns and may hold a
-- QUESTION, whose tier columns read NULL).
CREATE TEMP TABLE _133_seq AS SELECT name, seq FROM sqlite_sequence WHERE name = 'determination_gates';

DROP VIEW "v_open_determination_gates";

CREATE TABLE "_133_new_determination_gates" (
    gate_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_id        INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- The lens the finding applies to, NULL meaning every lens on this parameter. Not an FK set like
    -- specifications' four, because a gate is raised against a parameter by an audit that may not know which cells
    -- exist yet. A gate that names several lens columns applies to a cell that carries ALL of them.
    identity_code       TEXT REFERENCES "base_taxonomy_identity"(identity_code),
    icf_code            TEXT REFERENCES base_icf(icf_code),
    needs_code          TEXT REFERENCES access_needs(need_code),
    medical_code        TEXT REFERENCES base_taxonomy_medical(medical_code),
    verdict             TEXT NOT NULL
                        CHECK (verdict IN ('UNLINKED', 'MISLINKED',
                                           'UNDER-CONSERVATIVE', 'CONTRADICTS', 'QUESTION')),
    -- The ladder-inversion guard: how strong the thing raising the gate actually is. A QUESTION has no such
    -- thing and carries NULL in all three trigger columns; every other verdict states them.
    trigger_ref_id      TEXT REFERENCES evidence_sources(ref_id),
    trigger_tier        INTEGER CHECK (trigger_tier BETWEEN 1 AND 6),
    trigger_evidence_type TEXT,
    detail              TEXT NOT NULL,
    raised_at           TEXT NOT NULL,
    raised_by_session   TEXT NOT NULL,
    resolved_at         TEXT,
    resolved_by_session TEXT,
    resolution_rationale TEXT,
    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL
            AND resolution_rationale IS NULL)
        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL
            AND resolution_rationale IS NOT NULL)),
    CHECK ((verdict = 'QUESTION'
            AND trigger_tier IS NULL AND trigger_evidence_type IS NULL AND trigger_ref_id IS NULL)
        OR (verdict <> 'QUESTION'
            AND trigger_tier IS NOT NULL AND trigger_evidence_type IS NOT NULL))
);

INSERT INTO "_133_new_determination_gates"
    (gate_id, parameter_id, identity_code, verdict, trigger_ref_id, trigger_tier, trigger_evidence_type, detail,
     raised_at, raised_by_session, resolved_at, resolved_by_session, resolution_rationale)
SELECT gate_id, parameter_id, identity_code, verdict, trigger_ref_id, trigger_tier, trigger_evidence_type, detail,
       raised_at, raised_by_session, resolved_at, resolved_by_session, resolution_rationale
  FROM determination_gates;

DROP TABLE determination_gates;
ALTER TABLE "_133_new_determination_gates" RENAME TO determination_gates;

DELETE FROM sqlite_sequence WHERE name = 'determination_gates';
INSERT INTO sqlite_sequence (name, seq) SELECT name, seq FROM _133_seq;
DROP TABLE _133_seq;

CREATE INDEX idx_gates_open ON determination_gates(parameter_id, resolved_at);

CREATE VIEW v_open_determination_gates AS
SELECT g.gate_id, g.parameter_id, g.identity_code, g.icf_code, g.needs_code, g.medical_code, g.verdict,
       g.trigger_ref_id, g.trigger_tier, g.trigger_evidence_type, g.detail,
       g.raised_at, g.raised_by_session
  FROM determination_gates g
 WHERE g.resolved_at IS NULL;

PRAGMA user_version = 133;
