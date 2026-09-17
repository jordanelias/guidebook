-- 086_proxy_inference_marking.sql
--
-- A DETERMINATION MAY REST ON DOSE-RESPONSE FINDINGS. IT MUST SAY SO.
--
-- WHAT THIS IS FOR. Owner statement 2026-09-16: "even if they aren't asserting a
-- gradient, they are examining the impacts of gradients ... this means that
-- adjudication will be able to reason that whatever range of gradients corresponds
-- to the best outcomes is the best range of gradient" -- and, on being shown the
-- limit of that inference, "yes it's not perfect it's a proxy". Its ACTION (1) is
-- that a determination may rest on such findings "marked as a proxy, never as a
-- stated value", and ACTION (2) is that assess_cell must be able to reach a
-- determination from findings plus a threshold. This column is the mark.
--
-- WHY A COLUMN AND NOT A SENTENCE. CLAUDE.md section 8 asks what wrong thing
-- reaches the GUIDEBOOK without a new piece of apparatus. Without this: a cell
-- whose value was chosen because measured outcomes worsen across the code-permitted
-- range renders identically to a cell where a source stated that value outright.
-- The reader of the book cannot tell an inference from a citation, which is the one
-- distinction the owner's statement spends its whole second half drawing. A free-text
-- note cannot be gated; a boolean can, and it sits beside the two markers that already
-- do this job for the other two kinds of weakened claim -- `code_floor_only` and
-- `regulatory_stratum_only`. One role, one shape.
--
-- WHAT IT DOES NOT DO, because ACTION (4) is explicit and stop condition 4 of
-- workplan/2026-09-10-road-to-batch-06.md repeats it: this is NOT a value-directness
-- scale and must not be read as the first column of one. `source_value_extractions.
-- value_directness` still sits at NOT_ASSESSED on every row and still has no ratified
-- grading rule. This column records ONE fact with no gradations: whether the
-- determination's value was selected under a proxy inference from findings, or stated
-- by a source. A scale would need a DR; a boolean needs only the owner's own word,
-- which is "proxy".
--
-- ORDERING. 085 introduced AFTER_DATA because a rebuild applies numbered schema
-- migrations before timestamped data ones, and committed data migrations are
-- immutable. This column is only ever written by data migrations emitted AFTER it
-- exists, and the DEFAULT 0 keeps every older INSERT valid, so the marker is not
-- strictly required here. It is set anyway, to the newest data migration on disk at
-- the time of writing, because that is the true chronology and because a reader
-- comparing 085 and 086 should not have to work out why one declares it and one does
-- not.
--
-- AFTER_DATA: 20260917215404

ALTER TABLE specifications
  ADD COLUMN rests_on_proxy_inference INTEGER NOT NULL DEFAULT 0
  CHECK (rests_on_proxy_inference IN (0, 1));

PRAGMA user_version = 86;
