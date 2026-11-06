-- 118_adversarial_lens_sequence.sql
-- SCHEMA migration -- the adversarial pass gains a lens for SEQUENCE.
--
-- WHY. The owner asks for the adversarial audit to cover accuracy, logic and sequence (references/project-
-- standards.md, "Owner statements 2026-11-06 — the pipeline skill's requirements"). The eleven lenses of
-- migration 097 cover the first two; none covered sequence (the order stages are written and verified in,
-- and whether every pointer resolves to a row of an earlier stage), so a critic's sequence finding had to be
-- filed under a lens it did not belong to or not recorded. `close-adversarial-pass` derives its list of
-- required lenses from this CHECK (dbcore.check_values), so the new lens is required of every pass closed
-- after this file; passes already closed are not reopened. A pass still open would owe one more lens that no
-- verb can add to it (a pass takes one record and findings are not amendable), so this file gives every open
-- pass a NOT-ATTACKED row for the new lens, saying so. That is honest (the pass did not attack sequence) and
-- leaves each pass closable exactly when it was closable before. The rows carry the NEGATIVE of their pass_id as
-- finding_id: a scratch database allocates the next positive id and a data migration INSERTs it explicitly, so
-- an id taken from the same sequence here would collide with the findings of a pass recorded after this file was
-- written (the first version of this file did, and failed the rebuild on pass 9). Passes held open by owner ruling (2026-09-27
-- second, ACTION 2) stay open; nothing here closes one.
--
-- ORDER. The open passes are written by data migrations dated after the 095 cutoff, which a rebuild replays
-- after the schema migrations. The marker below places this file after the latest of them, so the backfill sees
-- the same open passes in a rebuild as in an incremental apply (otherwise the two databases would differ).
-- AFTER_DATA: 20261106053823
--
-- WHAT READS IT. db.py `record-adversarial-pass` (validates each finding's lens against this CHECK) and
-- `close-adversarial-pass`; `.claude/agents/antagonist.md` names the lens for the critic.
--
-- A CHECK cannot be altered in place. The table is rebuilt with identical columns and constraints plus the
-- new lens; nothing references it (re-derive: PRAGMA foreign_key_list over every table), and its one index
-- is recreated.

CREATE TABLE adversarial_findings_new (
  finding_id      INTEGER PRIMARY KEY,
  pass_id         INTEGER NOT NULL REFERENCES adversarial_passes(pass_id),
  lens            TEXT NOT NULL CHECK (lens IN (
                    'L1-existence','L2-fidelity','L3-independence','L4-tier','L5-population',
                    'L6-contrary','L7-recognition','L8-query-shape',
                    'S1-harm-reached-row','S2-mismatch-note-vs-payload','S3-containment',
                    'S4-sequence')),
  subject_table   TEXT,                -- loose pointer to the row attacked; never a copy of it,
                                       -- and never FK-enforced -- see header, "not Layer 1"
  subject_key     TEXT,
  claim_attacked  TEXT NOT NULL,
  method          TEXT NOT NULL,
  artefact        TEXT,                -- what the claim was attacked WITH (DR-2026-09-11 clause 2)
  verdict         TEXT NOT NULL CHECK (verdict IN
                    ('SUSTAINED','SURVIVED','NOT-ATTACKED','WITHHELD-FOR-OWNER')),
  severity        TEXT CHECK (severity IS NULL OR severity IN ('CRITICAL','HIGH','MEDIUM','LOW')),
                                       -- required iff verdict='SUSTAINED' (RULE ACTION 2)
  disposition     TEXT CHECK (disposition IS NULL OR disposition IN
                    ('REPAIRED','REJECTED','PROVISIONAL-DISPUTED','OWNER-RULED')),
  disposition_ref TEXT,                -- a data migration path; a quote-anchored ledger pointer; or the reason
  disposed_by_session TEXT,            -- NULL until disposed; set once, never overwritten (writer-enforced)
  disposed_at     TEXT,
  created_by_session TEXT NOT NULL,
  created_at      TEXT NOT NULL,
  -- The SUSTAINED<->severity pairing is a schema CHECK, not only a Python refusal, on
  -- the same precedent as `reviewer_transcript <> author_transcript` above: an invariant
  -- worth enforcing in a writer is worth enforcing for every future writer and every
  -- data migration that ever touches this table, not just the one call path that exists
  -- today. (severity IS NOT NULL) is 0/1 in SQLite, so this compares cleanly with the
  -- 0/1 of (verdict = 'SUSTAINED').
  CHECK ((verdict = 'SUSTAINED') = (severity IS NOT NULL))
) STRICT;

INSERT INTO adversarial_findings_new (finding_id, pass_id, lens, subject_table, subject_key, claim_attacked, method, artefact, verdict, severity, disposition, disposition_ref, disposed_by_session, disposed_at, created_by_session, created_at)
  SELECT finding_id, pass_id, lens, subject_table, subject_key, claim_attacked, method, artefact, verdict, severity, disposition, disposition_ref, disposed_by_session, disposed_at, created_by_session, created_at FROM adversarial_findings;

DROP TABLE adversarial_findings;
ALTER TABLE adversarial_findings_new RENAME TO adversarial_findings;
CREATE INDEX ix_adversarial_findings_pass ON adversarial_findings(pass_id);

INSERT INTO adversarial_findings (finding_id, pass_id, lens, claim_attacked, method, verdict, created_by_session, created_at)
  SELECT -pass_id, pass_id, 'S4-sequence', 'stage and write order (lens added after this pass was recorded)',
         'not attacked: migration 118 added this lens after the pass was recorded, and a recorded pass cannot take a further finding',
         'NOT-ATTACKED', 'migration_118', '2026-11-06 00:00'
  FROM adversarial_passes WHERE closed_at IS NULL;

PRAGMA user_version = 118;
