-- 134_gate_lens_comment.sql
-- SCHEMA migration -- a COMMENT-ONLY correction of the table definition migration 133 created. No column, CHECK,
-- row, view or index changes. Tooling (workplan T-021 repair after the critic); no research rows.
--
-- WHY. 133's DDL comment on the lens columns said a gate "applies to a cell that carries ALL of them". The engine
-- (assess_cell._open_gates) and derivation_handshake_integrity apply the rule the identity column always had: a gate is
-- skipped for a cell only when the cell carries a DIFFERENT code in a lens the gate names, and a lens the cell does
-- not carry never skips it. The comment in the schema was false; this recreates the table with the true one (SQLite
-- keeps a table's comments in its stored text, so the only way to correct one is create, copy, drop, rename, as in 133).
CREATE TEMP TABLE _134_seq AS SELECT name, seq FROM sqlite_sequence WHERE name = 'determination_gates';

DROP VIEW "v_open_determination_gates";

CREATE TABLE "_134_new_determination_gates" (
    gate_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_id        INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
    -- The lens the finding applies to, NULL meaning every lens on this parameter. Not an FK set like
    -- specifications' four, because a gate is raised against a parameter by an audit that may not know which cells
    -- exist yet. A gate is skipped for a cell only when the cell carries a DIFFERENT code in a lens the gate names; a lens the cell does not carry never skips it (the rule the identity column always had).
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

INSERT INTO "_134_new_determination_gates"
    (gate_id, parameter_id, identity_code, verdict, trigger_ref_id, trigger_tier, trigger_evidence_type, detail,
     raised_at, raised_by_session, resolved_at, resolved_by_session, resolution_rationale)
SELECT gate_id, parameter_id, identity_code, verdict, trigger_ref_id, trigger_tier, trigger_evidence_type, detail,
       raised_at, raised_by_session, resolved_at, resolved_by_session, resolution_rationale
  FROM determination_gates;

DROP TABLE determination_gates;
ALTER TABLE "_134_new_determination_gates" RENAME TO determination_gates;

DELETE FROM sqlite_sequence WHERE name = 'determination_gates';
INSERT INTO sqlite_sequence (name, seq) SELECT name, seq FROM _134_seq;
DROP TABLE _134_seq;

CREATE INDEX idx_gates_open ON determination_gates(parameter_id, resolved_at);

CREATE VIEW v_open_determination_gates AS
SELECT g.gate_id, g.parameter_id, g.identity_code, g.icf_code, g.needs_code, g.medical_code, g.verdict,
       g.trigger_ref_id, g.trigger_tier, g.trigger_evidence_type, g.detail,
       g.raised_at, g.raised_by_session
  FROM determination_gates g
 WHERE g.resolved_at IS NULL;

PRAGMA user_version = 134;
