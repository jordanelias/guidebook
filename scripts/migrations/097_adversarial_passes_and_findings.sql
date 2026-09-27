-- 097_adversarial_passes_and_findings.sql
--
-- THE ADVERSARIAL PASS GETS A RECORD, AND ITS ABSENCE GOES RED (RC4).
--
-- DR-2026-09-26-recurring-defect-shapes-remediation.md section 1, owner nod 2026-09-27.
-- The requirement already existed three times over -- the 2026-08-19 RULE ("records
-- SURVIVED claims as well as SUSTAINED ones -- a zero-finding pass must be able to show
-- what it attacked, or it is indistinguishable from a pass that never ran", plus its
-- ACTION (2) "claim-attacked / method / verdict / severity" and ACTION (5) "at most one
-- adversarial pass per research batch"), DR-2026-09-11 clause 2 ("a task is done when
-- the antagonist reports what it attacked the claim with"), and
-- governance/pipeline-contract.yaml's cross_stage/definition-of-done ("No ...
-- ready-for-review PR while ... an independent adversarial pass is unrun/unapplied") --
-- and none of the three was enforced. `select name from sqlite_master where name like
-- '%adversar%'` returned nothing before this migration. Batch 20's own antagonist pass
-- (session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa) ran claude-opus-5-5 on
-- both sides -- the same model as its author -- although the record called it "a different
-- model"; nothing checked that claim because nothing recorded the pass at all.
--
-- NO independence COLUMN. Whether the reviewer was a different model is COMPUTED from
-- reviewer_models and author_models (disjoint or not), never asserted (CLAUDE.md rule 8).
-- Both are writer-derived JSON arrays, never hand-typed: scripts/db.py's
-- record-adversarial-pass reads `message.model` off assistant-turn records in each
-- transcript, strips one trailing bracketed context-window suffix, and stores the sorted
-- distinct list. A transcript showing two normalised models (a mid-run fallback) keeps both.
--
-- THE LENS SET is the eight lenses of DR-2026-08-19 section 7 / the 2026-08-19 RULE, plus
-- the three standing subjects of skills/adversarial-research_SKILL.md (S1 harm-reached-row,
-- S2 mismatch-note-vs-payload, S3 containment). This CHECK is the set's one machine-readable
-- home; the prose stays explanation only (rule 8).
--
-- `reviewer_transcript <> author_transcript` makes a self-administered pass fail at INSERT,
-- not merely at review -- batch 20 section 0 records running exactly this when its
-- subagent had no agent-launching tool, and that pass "missed every one of the independent
-- pass's findings." The writer additionally normalises both paths before comparing or
-- storing them (os.path.normpath, then a check that the result still resolves under
-- transcripts/) -- a raw string comparison alone accepts `transcripts/x/./rev.jsonl` and
-- `transcripts/x/rev.jsonl` as "different" files, and accepts `transcripts/../scripts/db.py`
-- as "under transcripts/" by prefix alone. Both were demonstrated as live bypasses of the
-- refusal below during this migration's own adversarial review, and are why the writer
-- resolves before comparing rather than trusting the string it was given.
--
-- SEVERITY is nullable and required exactly when verdict='SUSTAINED' -- a claim that
-- SURVIVED, was never attacked, or is withheld for the owner has no defect to grade. The
-- writer enforces the pairing; the CHECK only enforces the vocabulary.
--
-- disposed_by_session/disposed_at exist because the first draft of this migration let
-- `dispose-adversarial-finding` set disposition with no record of who, silently
-- overwritable by a second call. Disposition is data with a judge (CLAUDE.md rule 8:
-- "derive it, or name who judged it"); these two columns are that name.
--
-- HONESTLY, NOT "LAYER 1 AT JUDGMENT". An earlier draft of this migration's own PR
-- description claimed these tables sit at the judgment stage and point backward along
-- the spine by a real pointer. Neither claim survived its own adversarial review:
-- `subject_table`/`subject_key` are untyped TEXT with no FK (SQLite has no polymorphic
-- foreign key, and a finding can legitimately point into any stage, not one), and
-- `subject_session`/`subject_commit`/the two transcript paths are process/session
-- identifiers, not stage data -- the same shape as `item_audit_runs` and `pipeline_runs`,
-- which CLAUDE.md's own table treats as apparatus rather than a spine stage. These two
-- tables are a QA/audit-trail record ABOUT a diff, not a stage table IN the spine; the
-- "pointer" in subject_table/subject_key is a loose, unenforced cross-reference, stated as
-- such rather than dressed up as rule 5's mechanism.
--
-- Once a committed data migration INSERTs into either table, rule 5 forbids dropping them:
-- reversing this decision means retiring the writer and writing NULL forward, not a DROP.

CREATE TABLE adversarial_passes (
  pass_id             INTEGER PRIMARY KEY,
  subject_session     TEXT NOT NULL,   -- bare stem of the batch attacked; writer strips a trailing .md
  subject_commit      TEXT NOT NULL,   -- the sha the reviewer read
  reviewer_transcript TEXT NOT NULL,   -- tracked path under transcripts/
  reviewer_models     TEXT NOT NULL CHECK (json_valid(reviewer_models) AND json_type(reviewer_models) = 'array'),
                                       -- DERIVED by the writer from the transcript; never typed
  author_transcript   TEXT NOT NULL,
  author_models       TEXT NOT NULL CHECK (json_valid(author_models) AND json_type(author_models) = 'array'),
  closed_at           TEXT,
  created_by_session  TEXT NOT NULL,
  created_at          TEXT NOT NULL,
  CHECK (reviewer_transcript <> author_transcript)   -- a self-administered pass is not a pass
) STRICT;

CREATE TABLE adversarial_findings (
  finding_id      INTEGER PRIMARY KEY,
  pass_id         INTEGER NOT NULL REFERENCES adversarial_passes(pass_id),
  lens            TEXT NOT NULL CHECK (lens IN (
                    'L1-existence','L2-fidelity','L3-independence','L4-tier','L5-population',
                    'L6-contrary','L7-recognition','L8-query-shape',
                    'S1-harm-reached-row','S2-mismatch-note-vs-payload','S3-containment')),
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

CREATE INDEX ix_adversarial_findings_pass ON adversarial_findings(pass_id);
CREATE INDEX ix_adversarial_passes_subject ON adversarial_passes(subject_session);

PRAGMA user_version = 97;
