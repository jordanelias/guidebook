-- 164: drop two views that nothing reads (CLAUDE.md section 8: an unread object is deleted, with evidence).
--
-- Evidence, re-derive rather than trust:
--   git grep -n -e v_registry_duplicate_descriptions -e v_code_floor_only -- . ':(exclude)transcripts' \
--     ':(exclude)_archived' ':(exclude)scripts/migrations' ':(exclude)scratchpad' ':(exclude)sessions' \
--     ':(exclude)attestations' ':(exclude)decisions' ':(exclude)audits' ':(exclude)references/audits' ':(exclude)workplan'
--   finds only governance/context-map.yaml, which is generated from sqlite_master and regenerated with this change.
--   No view, trigger or index in sqlite_master names either (rule 4: a view is a caller); no skill, check-registry
--   entry or script reads either.
-- Neither is a cross-stage pointer (CLAUDE.md section 3): v_code_floor_only reads specifications plus base
-- (base_parameters, terms); v_registry_duplicate_descriptions reads external_root_registry alone.
-- specifications.code_floor_only stays: only the view over it goes.

DROP VIEW IF EXISTS v_registry_duplicate_descriptions;
DROP VIEW IF EXISTS v_code_floor_only;

PRAGMA user_version = 164;
