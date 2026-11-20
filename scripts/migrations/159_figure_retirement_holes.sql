-- 159_figure_retirement_holes.sql
-- SCHEMA migration (T-078 repair, after the adversarial pass on migration 158). No data rows. Compensating: 158 is
-- committed and is not edited.
--
-- 1. BLANK AND SHAPE. 158's CHECK holds the three retirement cells together and refuses a cell trim() empties, but
--    trim() strips the ASCII space only: a reason of a no-break space and a zero-width space passed, as did a
--    retired_at of 'not a date'. Two triggers (on INSERT and on UPDATE of the three cells) refuse, when retired_at is
--    set: a retired_at not shaped as dbcore.now() stamps it ('YYYY-MM-DD HH:MM', the shape every sibling's
--    retired_at holds), and a retired_by_session or retirement_reason that holds only whitespace or zero-width
--    characters. The character sets are migration 154's whitespace set and dbcore.ZERO_WIDTH, spelled as migration
--    156 spells them (a test reads both). TRIGGERS, NOT A CHECK: a CHECK cannot be altered in place, and rebuilding
--    source_value_extractions (five tables point into it, six views read it) is the cost T-078's design rejected
--    for this table (task file section 4 item 1). A born-retired INSERT is NOT refused: emit_batch_sql captures a
--    figure added and retired in one batch as one INSERT of its end state, and its replay must pass.
-- 2. FINALITY. 158's trigger refused a change to retired_at only; a retired row's reason and session could be
--    rewritten. It is replaced by one refusing any change to any of the three cells once retired_at is set.
--    NOT CLOSABLE HERE, and recorded: INSERT OR REPLACE of the same extraction_id deletes the retired row and inserts
--    a live one; a DELETE trigger does not fire for REPLACE without PRAGMA recursive_triggers, so no trigger closes it.
--    No writer issues INSERT OR REPLACE on this table.
-- 3. A CORRECTION OF 158's HEADER. It said v_determination_provenance "KEEPS HISTORY". It does not: its text ends
--    WHERE s.retired_at IS NULL, so it lists the figures of LIVE determinations only, and retire-extraction refuses a
--    figure a live determination links, so the view never shows a retired figure. No view answers "which
--    determinations did this retired figure feed"; specification_extraction_links holds it, and none is added
--    (nothing reads it).

DROP TRIGGER trg_sve_retirement_is_final;

CREATE TRIGGER trg_sve_retirement_is_final
BEFORE UPDATE OF retired_at, retired_by_session, retirement_reason ON source_value_extractions
WHEN OLD.retired_at IS NOT NULL
 AND (NEW.retired_at IS NOT OLD.retired_at OR NEW.retired_by_session IS NOT OLD.retired_by_session
      OR NEW.retirement_reason IS NOT OLD.retirement_reason)
BEGIN
    SELECT RAISE(ABORT, 'a retired figure stays retired as it was retired -- a wrong retirement is answered by a new figure (db.py add-extraction), never by changing its retirement cells');
END;

CREATE TRIGGER trg_sve_retirement_shape_insert
BEFORE INSERT ON source_value_extractions
WHEN NEW.retired_at IS NOT NULL
 AND (NEW.retired_at NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]'
      OR trim(COALESCE(NEW.retired_by_session, ''), char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) = ''
      OR trim(COALESCE(NEW.retirement_reason, ''), char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) = '')
BEGIN
    SELECT RAISE(ABORT, 'a figure is retired with a retired_at stamped YYYY-MM-DD HH:MM and a session and a reason that are not blank (whitespace or zero-width characters only)');
END;

CREATE TRIGGER trg_sve_retirement_shape_update
BEFORE UPDATE OF retired_at, retired_by_session, retirement_reason ON source_value_extractions
WHEN NEW.retired_at IS NOT NULL
 AND (NEW.retired_at NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]'
      OR trim(COALESCE(NEW.retired_by_session, ''), char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) = ''
      OR trim(COALESCE(NEW.retirement_reason, ''), char(32,9,10,11,12,13,133,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,8232,8233,8239,8287,12288) || char(8203,8204,8205,8288,65279)) = '')
BEGIN
    SELECT RAISE(ABORT, 'a figure is retired with a retired_at stamped YYYY-MM-DD HH:MM and a session and a reason that are not blank (whitespace or zero-width characters only)');
END;

PRAGMA user_version = 159;
