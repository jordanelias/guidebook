-- 088: search_candidates gains the edge to the source it became.
--
-- WHY. R15 makes a staged candidate a HYPOTHESIS that must be re-described from the
-- source on resolution. `resolve-candidate` recorded the disposition and the
-- re-description and NOT WHICH SOURCE THE CANDIDATE BECAME, so the only link from a
-- candidate to its admitted ref was a ref id mentioned in free-text `notes`.
--
-- WHAT THAT COST, measured 2026-09-18 on batch 17. Candidates 107 and 108 were staged
-- against exec 71 -- a Co-1 web search whose own findings_note reads ZERO YIELD and
-- whose results_admitted is 0 -- while `search_admissions` records exec 77 as the
-- search that admitted REF-01003 and REF-01004. Two provenance pointers naming
-- different searches for the same two sources, and NOTHING could detect it: the
-- comparison needs a candidate-to-ref edge, and there was no column holding one. The
-- batch then wrote into a committed migration that it had "corrected" the attribution.
-- It had not, and no gate could have said so.
--
-- Nullable by construction: a candidate that is PENDING, REHOMED or SCREENED-OUT never
-- became a source, and a legacy row cannot have its resolution reconstructed. The
-- writer (`db.py resolve-candidate`) requires it going forward for the one disposition
-- where it is knowable -- ADMITTED -- and the integrity check S01 asserts the
-- agreement only where the edge exists. Backfill is an operator act with evidence, not
-- a default.
ALTER TABLE search_candidates
    ADD COLUMN resolved_ref_id TEXT REFERENCES evidence_sources(ref_id);

PRAGMA user_version = 88;
