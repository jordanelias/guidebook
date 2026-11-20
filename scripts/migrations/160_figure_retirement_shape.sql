-- 160_figure_retirement_shape.sql
-- SCHEMA migration (T-078, second repair after the adversarial pass). No data rows. Compensating: 158 and 159 are not
-- edited.
--
-- 1. ONE DEFINITION OF BLANK. 159's triggers trimmed migration 154's whitespace set and dbcore.ZERO_WIDTH, so a reason
--    of U+180E, U+00AD, U+2800, U+3164, U+200E or U+2063 passed, and U+001F passed the trigger while the verb refused
--    it. The set is now dbcore.blank_chars(): Unicode categories Cc, Cf, Zs, Zl, Zp and U+2800, U+3164, spelled below
--    without U+0000 (char(0) ends a string in SQLite's text functions; a NUL cannot be typed into a reason through
--    the CLI). Test T078-40 pins the spelling to the definition. db.py retire-extraction reads the same definition
--    (dbcore.is_blank). dbcore.require_reason is not tightened: it would move defer-reading's refusal ground (T079-30).
-- 2. RETIRED_AT is text, stamped as dbcore.now() stamps it, a real calendar minute (datetime() round-trips it, so
--    '9999-99-99 99:99' and '2026-02-30 00:00' are refused), not in the future, and not before the row's own
--    created_at where that is a stamp (so '1900-01-01 00:00' is refused on every live row).
-- 3. RETIRED_BY_SESSION is a session stem: 'session_' and a name, no '.md' (dbcore.session_stem), nothing blank in it
--    (dbcore.is_session_stem). No sibling table's CHECK states a session shape; every live stem starts 'session_'.
-- 4. A RETIRED ROW IS FROZEN: once retired_at is set, an UPDATE of any other column but the updated_* stamps is
--    refused (159's trigger already refuses the three retirement columns). The column list is every column of the
--    table at this migration less those five, read from PRAGMA table_info; test T078-41 fails when a later column is
--    not in it.
-- Not closable, recorded again: INSERT OR REPLACE of the same extraction_id (no trigger fires without
-- recursive_triggers). A born-retired INSERT stays allowed when well formed (emit_batch_sql captures a figure added
-- and retired in one batch as one INSERT).

DROP TRIGGER trg_sve_retirement_shape_insert;
DROP TRIGGER trg_sve_retirement_shape_update;

CREATE TRIGGER trg_sve_retirement_shape_insert
BEFORE INSERT ON source_value_extractions
WHEN NEW.retired_at IS NOT NULL
 AND (typeof(NEW.retired_at) <> 'text'
      OR NEW.retired_at NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]'
      OR datetime(NEW.retired_at) IS NOT NEW.retired_at || ':00'
      OR NEW.retired_at > strftime('%Y-%m-%d %H:%M', 'now')
      OR (NEW.created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]*' AND NEW.retired_at < substr(NEW.created_at, 1, 16))
      OR typeof(NEW.retired_by_session) <> 'text'
      OR NEW.retired_by_session NOT GLOB 'session_?*' OR NEW.retired_by_session GLOB '*.md'
      OR NEW.retired_by_session GLOB '*[' || char(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,173,1536,1537,1538,1539,1540,1541,1564,1757,1807,2192,2193,2274,5760,6158,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,8205,8206,8207,8232,8233,8234) || char(8235,8236,8237,8238,8239,8287,8288,8289,8290,8291,8292,8294,8295,8296,8297,8298,8299,8300,8301,8302,8303,10240,12288,12644,65279,65529,65530,65531,69821,69837,78896,78897,78898,78899,78900,78901,78902,78903,78904,78905,78906,78907,78908,78909,78910,78911,113824,113825,113826,113827,119155,119156,119157,119158,119159,119160,119161,119162,917505,917536,917537,917538,917539,917540,917541,917542,917543,917544,917545,917546,917547,917548,917549,917550,917551,917552,917553,917554,917555,917556,917557,917558,917559,917560,917561,917562,917563,917564,917565,917566,917567,917568,917569,917570,917571,917572,917573,917574,917575,917576) || char(917577,917578,917579,917580,917581,917582,917583,917584,917585,917586,917587,917588,917589,917590,917591,917592,917593,917594,917595,917596,917597,917598,917599,917600,917601,917602,917603,917604,917605,917606,917607,917608,917609,917610,917611,917612,917613,917614,917615,917616,917617,917618,917619,917620,917621,917622,917623,917624,917625,917626,917627,917628,917629,917630,917631) || ']*'
      OR typeof(NEW.retirement_reason) <> 'text'
      OR trim(NEW.retirement_reason, char(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,173,1536,1537,1538,1539,1540,1541,1564,1757,1807,2192,2193,2274,5760,6158,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,8205,8206,8207,8232,8233,8234) || char(8235,8236,8237,8238,8239,8287,8288,8289,8290,8291,8292,8294,8295,8296,8297,8298,8299,8300,8301,8302,8303,10240,12288,12644,65279,65529,65530,65531,69821,69837,78896,78897,78898,78899,78900,78901,78902,78903,78904,78905,78906,78907,78908,78909,78910,78911,113824,113825,113826,113827,119155,119156,119157,119158,119159,119160,119161,119162,917505,917536,917537,917538,917539,917540,917541,917542,917543,917544,917545,917546,917547,917548,917549,917550,917551,917552,917553,917554,917555,917556,917557,917558,917559,917560,917561,917562,917563,917564,917565,917566,917567,917568,917569,917570,917571,917572,917573,917574,917575,917576) || char(917577,917578,917579,917580,917581,917582,917583,917584,917585,917586,917587,917588,917589,917590,917591,917592,917593,917594,917595,917596,917597,917598,917599,917600,917601,917602,917603,917604,917605,917606,917607,917608,917609,917610,917611,917612,917613,917614,917615,917616,917617,917618,917619,917620,917621,917622,917623,917624,917625,917626,917627,917628,917629,917630,917631)) = '')
BEGIN
    SELECT RAISE(ABORT, 'a figure is retired with a retired_at that is a real past minute stamped YYYY-MM-DD HH:MM (not before the row was created), a session stem session_<name>, and a reason that is not blank (dbcore.blank_chars)');
END;

CREATE TRIGGER trg_sve_retirement_shape_update
BEFORE UPDATE OF retired_at, retired_by_session, retirement_reason ON source_value_extractions
WHEN NEW.retired_at IS NOT NULL
 AND (typeof(NEW.retired_at) <> 'text'
      OR NEW.retired_at NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]'
      OR datetime(NEW.retired_at) IS NOT NEW.retired_at || ':00'
      OR NEW.retired_at > strftime('%Y-%m-%d %H:%M', 'now')
      OR (NEW.created_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]*' AND NEW.retired_at < substr(NEW.created_at, 1, 16))
      OR typeof(NEW.retired_by_session) <> 'text'
      OR NEW.retired_by_session NOT GLOB 'session_?*' OR NEW.retired_by_session GLOB '*.md'
      OR NEW.retired_by_session GLOB '*[' || char(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,173,1536,1537,1538,1539,1540,1541,1564,1757,1807,2192,2193,2274,5760,6158,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,8205,8206,8207,8232,8233,8234) || char(8235,8236,8237,8238,8239,8287,8288,8289,8290,8291,8292,8294,8295,8296,8297,8298,8299,8300,8301,8302,8303,10240,12288,12644,65279,65529,65530,65531,69821,69837,78896,78897,78898,78899,78900,78901,78902,78903,78904,78905,78906,78907,78908,78909,78910,78911,113824,113825,113826,113827,119155,119156,119157,119158,119159,119160,119161,119162,917505,917536,917537,917538,917539,917540,917541,917542,917543,917544,917545,917546,917547,917548,917549,917550,917551,917552,917553,917554,917555,917556,917557,917558,917559,917560,917561,917562,917563,917564,917565,917566,917567,917568,917569,917570,917571,917572,917573,917574,917575,917576) || char(917577,917578,917579,917580,917581,917582,917583,917584,917585,917586,917587,917588,917589,917590,917591,917592,917593,917594,917595,917596,917597,917598,917599,917600,917601,917602,917603,917604,917605,917606,917607,917608,917609,917610,917611,917612,917613,917614,917615,917616,917617,917618,917619,917620,917621,917622,917623,917624,917625,917626,917627,917628,917629,917630,917631) || ']*'
      OR typeof(NEW.retirement_reason) <> 'text'
      OR trim(NEW.retirement_reason, char(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,173,1536,1537,1538,1539,1540,1541,1564,1757,1807,2192,2193,2274,5760,6158,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,8205,8206,8207,8232,8233,8234) || char(8235,8236,8237,8238,8239,8287,8288,8289,8290,8291,8292,8294,8295,8296,8297,8298,8299,8300,8301,8302,8303,10240,12288,12644,65279,65529,65530,65531,69821,69837,78896,78897,78898,78899,78900,78901,78902,78903,78904,78905,78906,78907,78908,78909,78910,78911,113824,113825,113826,113827,119155,119156,119157,119158,119159,119160,119161,119162,917505,917536,917537,917538,917539,917540,917541,917542,917543,917544,917545,917546,917547,917548,917549,917550,917551,917552,917553,917554,917555,917556,917557,917558,917559,917560,917561,917562,917563,917564,917565,917566,917567,917568,917569,917570,917571,917572,917573,917574,917575,917576) || char(917577,917578,917579,917580,917581,917582,917583,917584,917585,917586,917587,917588,917589,917590,917591,917592,917593,917594,917595,917596,917597,917598,917599,917600,917601,917602,917603,917604,917605,917606,917607,917608,917609,917610,917611,917612,917613,917614,917615,917616,917617,917618,917619,917620,917621,917622,917623,917624,917625,917626,917627,917628,917629,917630,917631)) = '')
BEGIN
    SELECT RAISE(ABORT, 'a figure is retired with a retired_at that is a real past minute stamped YYYY-MM-DD HH:MM (not before the row was created), a session stem session_<name>, and a reason that is not blank (dbcore.blank_chars)');
END;

CREATE TRIGGER trg_sve_retired_row_frozen
BEFORE UPDATE OF extraction_id, ref_id, slug, parameter_id, identity_code, icf_code, needs_code, jurisdiction, setting, claim_type, claimed_value, claimed_unit, claim_text, source_section, root_id, root_type, root_ref_id, echo_of, measurement_paradigm, device_class, root_population_note, root_classification_basis, contested, file_anchor, locator_scheme, loc_division, loc_part, loc_section, loc_subsection, loc_paragraph, loc_clause, loc_subclause, loc_division_end, loc_part_end, loc_section_end, loc_subsection_end, loc_paragraph_end, loc_clause_end, loc_subclause_end, loc_note, extraction_method, extraction_status, promoted_to_rdc_id, notes, created_at, created_by_session, figure_role, comparator, harm_finding, value_as_written, clause_id ON source_value_extractions
WHEN OLD.retired_at IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'a retired figure is history and is not changed -- write the correct figure with db.py add-extraction');
END;

PRAGMA user_version = 160;
