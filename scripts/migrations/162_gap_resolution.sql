-- 162_gap_resolution.sql
-- SCHEMA migration (T-144; owner, typed 2026-11-20: "add a resolved column and a solution provenance column or
-- something ... unless we already have a table that links accordingly"). No data rows. No table links a gap to what
-- closed it: `close-gap` moved `status` alone, so a closed gap said neither when, in which session, nor by what.
--
-- Three cells on `gaps`, the shape `determination_gates` (resolved_at, resolved_by_session) and
-- `extraction_follow_ups` (resolved_at, resolved_by_session, resolution) already hold, the pointer read as
-- `adversarial_findings.disposition_ref` is read ("a data migration path; a quote-anchored ledger pointer; or the
-- reason"):
--   resolved_at          the minute the gap was closed, stamped as dbcore.now() stamps it (YYYY-MM-DD HH:MM), a real
--                        calendar minute (datetime() round-trips it) and not before the row's own created_at where
--                        that is a stamp;
--   resolved_by_session  the session stem that closed it (session_<name>, no '.md', nothing blank in it:
--                        dbcore.is_session_stem);
--   resolution_ref       what resolved it, not blank by dbcore.blank_chars().
-- All three are present or all are NULL, and a gap that carries them is CLOSED: an OPEN gap carries none (a gap is
-- reopened only by NULLing all three in the same UPDATE as its status; no verb reopens a gap today).
--
-- CHECKS, NOT TRIGGERS. Migration 160 used triggers because its three columns already existed (158) and a CHECK on
-- them needed a rebuild of source_value_extractions. These columns are new, so ALTER TABLE ... ADD COLUMN carries
-- the CHECK in place, as 161 did; the last column's CHECK names the other two and `status`. What a CHECK cannot
-- read, and so is not refused here: a stamp in the future ('now' is not allowed in a CHECK). The writer stamps
-- dbcore.now(); only hand SQL could write a future stamp.
--
-- The blank set is dbcore.blank_chars() less U+0000, spelled exactly as migration 160 spells it (test T144-01 pins
-- both spellings to the definition).
--
-- NO BACKFILL. The gaps closed before this migration carry no provenance and none can be honestly derived
-- (`select count(*) from gaps where status like 'CLOSED%' and resolved_at is null`); they stay NULL, and
-- scripts/audit/gap_mining_audit.py lists them as informational. Every closing through `close-gap` from now on
-- writes all three.

ALTER TABLE gaps ADD COLUMN resolved_at TEXT
    CHECK (resolved_at IS NULL OR (typeof(resolved_at) = 'text'
        AND resolved_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]'
        AND datetime(resolved_at) IS resolved_at || ':00'
        AND NOT (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]*'
                 AND resolved_at < substr(created_at, 1, 16))));

ALTER TABLE gaps ADD COLUMN resolved_by_session TEXT
    CHECK (resolved_by_session IS NULL OR (typeof(resolved_by_session) = 'text'
        AND resolved_by_session GLOB 'session_?*' AND resolved_by_session NOT GLOB '*.md'
        AND resolved_by_session NOT GLOB '*[' || char(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,173,1536,1537,1538,1539,1540,1541,1564,1757,1807,2192,2193,2274,5760,6158,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,8205,8206,8207,8232,8233,8234) || char(8235,8236,8237,8238,8239,8287,8288,8289,8290,8291,8292,8294,8295,8296,8297,8298,8299,8300,8301,8302,8303,10240,12288,12644,65279,65529,65530,65531,69821,69837,78896,78897,78898,78899,78900,78901,78902,78903,78904,78905,78906,78907,78908,78909,78910,78911,113824,113825,113826,113827,119155,119156,119157,119158,119159,119160,119161,119162,917505,917536,917537,917538,917539,917540,917541,917542,917543,917544,917545,917546,917547,917548,917549,917550,917551,917552,917553,917554,917555,917556,917557,917558,917559,917560,917561,917562,917563,917564,917565,917566,917567,917568,917569,917570,917571,917572,917573,917574,917575,917576) || char(917577,917578,917579,917580,917581,917582,917583,917584,917585,917586,917587,917588,917589,917590,917591,917592,917593,917594,917595,917596,917597,917598,917599,917600,917601,917602,917603,917604,917605,917606,917607,917608,917609,917610,917611,917612,917613,917614,917615,917616,917617,917618,917619,917620,917621,917622,917623,917624,917625,917626,917627,917628,917629,917630,917631) || ']*'));

ALTER TABLE gaps ADD COLUMN resolution_ref TEXT
    CHECK (
        (resolution_ref IS NULL OR (typeof(resolution_ref) = 'text'
            AND trim(resolution_ref, char(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,173,1536,1537,1538,1539,1540,1541,1564,1757,1807,2192,2193,2274,5760,6158,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,8205,8206,8207,8232,8233,8234) || char(8235,8236,8237,8238,8239,8287,8288,8289,8290,8291,8292,8294,8295,8296,8297,8298,8299,8300,8301,8302,8303,10240,12288,12644,65279,65529,65530,65531,69821,69837,78896,78897,78898,78899,78900,78901,78902,78903,78904,78905,78906,78907,78908,78909,78910,78911,113824,113825,113826,113827,119155,119156,119157,119158,119159,119160,119161,119162,917505,917536,917537,917538,917539,917540,917541,917542,917543,917544,917545,917546,917547,917548,917549,917550,917551,917552,917553,917554,917555,917556,917557,917558,917559,917560,917561,917562,917563,917564,917565,917566,917567,917568,917569,917570,917571,917572,917573,917574,917575,917576) || char(917577,917578,917579,917580,917581,917582,917583,917584,917585,917586,917587,917588,917589,917590,917591,917592,917593,917594,917595,917596,917597,917598,917599,917600,917601,917602,917603,917604,917605,917606,917607,917608,917609,917610,917611,917612,917613,917614,917615,917616,917617,917618,917619,917620,917621,917622,917623,917624,917625,917626,917627,917628,917629,917630,917631)) <> ''))
        -- all three present on a CLOSED gap, or all three absent
        AND ((resolved_at IS NULL AND resolved_by_session IS NULL AND resolution_ref IS NULL)
          OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL AND resolution_ref IS NOT NULL
              AND status LIKE 'CLOSED%'))
    );

PRAGMA user_version = 162;
