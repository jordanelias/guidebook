-- 098_search_execution_provenance.sql
--
-- THE DISCOVERY ROUTE IS TYPED, AND ITS DUAL HOME IS SETTLED (RC5), TOGETHER WITH
-- RC1's CANDIDATE-AGAINST-PAYLOAD CHECK. DR-2026-09-26-recurring-defect-shapes-
-- remediation.md sections 2.2(b)(c) and 5.2(b), owner nod 2026-09-27.
--
-- THE DUAL HOME. `search_executions` becomes the one EVENT record of a discovery
-- step, planned or not, including mining -- following the owner's 2026-09-26
-- ruling (2), "log each real discovery step as a backfill search". Before this,
-- `search_candidates.exec_id` was the only discovery pointer, and nothing said
-- WHICH source a mining pass mined, or that a step was a lookup rather than a
-- designed query: the workarounds show in `engine` values like `multi-index`,
-- `crossref-deposit` and `source_locators`. `citation_mining.connections_produced`
-- is the surviving second home; it retires in phase 2b, once its readers are swept
-- and the table is rebuilt to accept NULL (see that migration for why the order
-- has to be rebuild-then-retire, not retire-then-rebuild).
--
-- `origin` is the INITIATION axis (why the step ran); `mining_direction` stays the
-- METHOD axis (how). The two are orthogonal, so no fact gains a second home. The
-- cross-column CHECK ties `origin_pass_id` to `origin='adversarial-pass'` only --
-- it does not require one, because batch 19's own adversarial pass (the origin of
-- exec 100) predates `adversarial_passes` entirely and can never be backfilled a
-- real id.
--
-- THE JUNCTION, `search_execution_artefacts`, is the pointer RC1 asks for between
-- a discovery event and the payload(s) it returned -- many-to-many on purpose,
-- because one content-addressed file can be the fetched result of two searches
-- (measured: `d03a6fc8797e5f99.json` is both T7 and C4 in batch 19's log, a
-- byte-identical empty ERIC result). `scripts/research/retrieval_log.py`'s
-- `check_artefact_link()` is the one place both writers (`log-search
-- --result-artefact`, `amend-search --add-result-artefact`) and
-- `provenance_artefact_audit.py`'s re-derivation evaluate this fact, so a write-time
-- refusal and its audit can never drift apart (rule 5, one level up from a table).
--
-- `search_candidates.surfaced_in`/`surfaced_quote` are the pointer from a STAGED
-- CANDIDATE to the specific payload it was read out of -- narrower than the
-- junction above, because a search can return several payloads and a candidate
-- came from exactly one of them (or, for a route like exec 100's that was never
-- persisted, a tracked transcript file instead).
--
-- No rebuild. Every existing `search_executions` row takes `origin`'s default,
-- `search_candidates`' two new columns are nullable, and the junction is new.
-- Verified against a scratch copy: the migration applies cleanly with
-- `foreign_keys=ON`, the cross-column CHECK fires on a violating UPDATE, and every
-- view still resolves.

ALTER TABLE search_executions ADD COLUMN origin TEXT NOT NULL DEFAULT 'planned'
  CHECK (origin IN ('planned','incidental','adversarial-pass','owner-supplied','lead-index'));
ALTER TABLE search_executions ADD COLUMN mined_ref_id TEXT REFERENCES evidence_sources(ref_id);
ALTER TABLE search_executions ADD COLUMN origin_pass_id INTEGER
  REFERENCES adversarial_passes(pass_id) CHECK (origin_pass_id IS NULL OR origin = 'adversarial-pass');

ALTER TABLE search_candidates ADD COLUMN surfaced_in TEXT;
ALTER TABLE search_candidates ADD COLUMN surfaced_quote TEXT;

CREATE TABLE search_execution_artefacts (
  exec_id            INTEGER NOT NULL REFERENCES search_executions(exec_id),
  artefact           TEXT NOT NULL,   -- retrieval-log/<session stem>/<file>: a POINTER into Layer 4
  created_by_session TEXT NOT NULL,
  created_at         TEXT NOT NULL,
  PRIMARY KEY (exec_id, artefact)
) STRICT;

PRAGMA user_version = 98;
