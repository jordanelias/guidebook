# T-018 design — the lens link table (OR-1c)

_Written 2026-11-12 by an Opus-class designer under the owner's instruction "Opus to write design files that must be written first". Plan document: it changes no script, schema, row or ruling. Every count below is given as the command that produces it; re-run it, do not trust a figure. SQL marked **sketch** is the shape to build, not a file to paste unread. Canadian English._

_Revised 2026-11-13 after the pilot (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-018-report.md`). A replaced carried link could not be replayed from the captured batch, so the emitter's order changes (§6, "Captured set"). Also folded: the Python API shape (§6); a plain deprecated-code refusal in place of T-054's, which T-018 does not wait for (§6, §7, §9); the code check through the shared helper, not `fk_declared` (§6); `evidence_population_match.source_ref` (§6); the stage-map line and the blocking `research_dod_selftest` fixture (§9); the corrected expected-red output, the new case T018-08, and T018-06 moved out of the test files into a one-time assertion (§10)._

## 0. Verdict

**Build one table, `extraction_lens_links`: one row per (figure, lens code), four typed lens columns of which each row states exactly one, a typed warrant (`basis`, `basis_text`), and retire-in-place columns; plus one view, `v_live_lens_links`, which is the only read surface.** The four lens columns on `source_value_extractions` are retired in this pull request: the migration carries every value they hold into the table as a `carried` link, NULLs the columns, and replaces their "at least one" CHECK with a CHECK that keeps them NULL. They are not dropped, because committed data migrations INSERT them. "At least one lens per figure" (D-0182) moves to the writers and to one blocking integrity case. Two verbs are added (`add-lens-link`, `retire-lens-link`); `add-extraction` and `derive-extraction` take each lens flag repeatedly. `specifications` keeps its four columns: a cell is a key, with one code per model; a figure that concerns two ICF codes reaches two cells.

**The gather rule T-019 builds on:** a figure reaches a cell when every code the cell states is among the figure's live links (identity widened to the code's descendants by T-055). A figure is never copied.

**Confidence.** High (about 85%) on the shape: it is the 2026-08-28 four-typed-column shape moved onto a link row, which is what OR-1c asks for, and it keeps every lens a real foreign key. Medium (about 70%) on the `basis` vocabulary: it is the smallest that records the three warrants the rulings name (a quote naming the users, D-2; a heading, OD-31; a study's participants, the 2026-08-25 grade rule). Medium (about 70%) that dropping the figure-row CHECK in favour of a writer refusal plus a blocking integrity case is acceptable; the alternative (keep the columns live) is a second home.

**Owner's call.** Nothing doctrinal is decided here. One reading was marked as an assumption and **is now the owner's answer: OD-39, 2026-11-12 (fifth set), "Yes, the 2026-11-06 ruling supersedes that clause"** (`grep -n -F "OD-39: the 2026-11-06 link-table ruling supersedes" references/project-standards.md`): OR-1c ("link table unless that is more prone to errors", 2026-11-06) supersedes, for a figure's lens codes, the clause "Never a `population_*` link table" of the 2026-08-28 ACTION. The pull request records the supersession in a ledger entry in prose (section 5, step 6, corrected: the machine `SUPERSEDES` pair cannot pass the audit for a target inside the ledger). The rest of the 2026-08-28 ACTION stands and is met: four typed lens columns, real FKs, "never two lenses in one row" (now true of every link row), the lens names in the table's name (no `population`).

## 1. What the rulings require, and where this design meets each

| Ruling (find it with) | Requirement | Met by |
|---|---|---|
| OR-1c, `grep -n -F 'link table unless that is more prone to errors' references/project-standards.md` | several codes of one model on a figure, by a link table; the figure written once | `extraction_lens_links`; the figure row is never copied |
| 2026-08-28 lens ruling, `grep -n -F 'real FKs. Never a `population_*` link table.' references/project-standards.md` | four lens columns, one CHECK, real typed FKs, nothing polymorphic; never two lenses in one row; lens names, not `population` | four typed FK columns on the link row; CHECK exactly one per link row; no `(lens, code)` text pair |
| D-0182, `grep -n -F 'The lens CHECK is "at least one"' references/project-standards.md` | a figure carries at least one lens, ideally many | writers refuse a figure with no live link and refuse to retire its last one; integrity case (section 9, T018-05) |
| OR-1, `grep -n -F 'a figure reaches a determination only through the lens tags written on that figure' references/project-standards.md` | a figure reaches a cell only through its own lens codes; every relevant model is named | the gather predicate of section 4; T-106 fills further models as links |
| OD-29 (delegated), `grep -n -F 'OD-29: both retire in place' references/project-standards.md`, with the 2026-09-16 ruling it reads | link rows retire in place; every reader filters on the mark first | `retired_at` columns; `v_live_lens_links` is the filtered read |
| D-2 / OD-06 (delegated), `grep -n -F 'OD-06' references/project-standards.md \| tail -3` | judgment assigns lenses, only where a quote names the users | `basis = 'named_in_text'` with the words, checked against the row's own text |
| OD-31 (owner), `grep -n -F 'OD-31: a provision that names no one' references/project-standards.md` | a provision that names no one carries its heading's group | `basis = 'heading'` with the heading's words |
| CLAUDE.md rule 5 | one home for a figure's lens | the columns are NULLed and held NULL by CHECK; the link table is the only home |

## 2. The table and the view (sketch)

```sql
-- sketch: extraction_lens_links -- the lens codes of a figure, one row per code (OR-1c)
CREATE TABLE extraction_lens_links (
    link_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
    -- THE FOUR LENSES, typed, one per row (2026-08-28 shape; "never two lenses in one row").
    identity_code       TEXT REFERENCES base_taxonomy_identity(identity_code),
    icf_code            TEXT REFERENCES base_icf(icf_code),
    needs_code          TEXT REFERENCES access_needs(need_code),
    medical_code        TEXT REFERENCES base_taxonomy_medical(medical_code),
    -- THE WARRANT (rule 8: a judgment records its answer and its evidence in named columns).
    --   named_in_text       the figure's own words name the users / function / need (D-2)
    --   heading             the provision names no one; its heading names the group (OD-31)
    --   study_participants  a study's own participants are this group (2026-08-25 grade rule)
    --   carried             moved by migration from the retired column; no judged warrant yet
    basis               TEXT NOT NULL CHECK (basis IN
                            ('named_in_text', 'heading', 'study_participants', 'carried')),
    basis_text          TEXT,          -- the exact words that warrant the link
    retired_at          TEXT,
    retired_by_session  TEXT,
    retirement_reason   TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    CHECK ((identity_code IS NOT NULL) + (icf_code IS NOT NULL)
         + (needs_code IS NOT NULL) + (medical_code IS NOT NULL) = 1),
    CHECK ((basis = 'carried') = (basis_text IS NULL)),
    CHECK (basis_text IS NULL OR length(trim(basis_text)) > 0),
    CHECK ((retired_at IS NULL) = (retired_by_session IS NULL)
       AND (retired_at IS NULL) = (retirement_reason IS NULL))
);
-- One LIVE link per (figure, code). A retired link may repeat a live one (history).
CREATE UNIQUE INDEX ux_extraction_lens_live ON extraction_lens_links
    (extraction_id, COALESCE(identity_code, ''), COALESCE(icf_code, ''),
     COALESCE(needs_code, ''), COALESCE(medical_code, ''))
    WHERE retired_at IS NULL;
CREATE INDEX ix_ell_extraction ON extraction_lens_links(extraction_id);
CREATE INDEX ix_ell_identity   ON extraction_lens_links(identity_code) WHERE retired_at IS NULL;
CREATE INDEX ix_ell_icf        ON extraction_lens_links(icf_code)      WHERE retired_at IS NULL;
CREATE INDEX ix_ell_needs      ON extraction_lens_links(needs_code)    WHERE retired_at IS NULL;

-- The one read surface (OD-29: every reader filters on the retired mark first).
CREATE VIEW v_live_lens_links AS
SELECT link_id, extraction_id, identity_code, icf_code, needs_code, medical_code,
       basis, basis_text, created_at, created_by_session
  FROM extraction_lens_links
 WHERE retired_at IS NULL;
```

Decided, not left open: the table name (`extraction_lens_links`: "lens" names all four, as the naming ruling of 2026-08-28 asks; `population_*` is retired vocabulary); `link_id` as an integer key so `retire-lens-link` and the batch capture address one row; no `superseded_by_link_id` (a retired link names its reason; the replacing link is the live one for the same figure, found by query); no column saying "this is a link" (the table is the mark). `basis_text` is a quote of the row's words, not a copy of a fact held elsewhere: it records which words the judge relied on, which no other column says.

## 3. What becomes of the four lens columns on the figure

1. **Carried.** The migration inserts one `carried` link per non-NULL lens column of every figure, stamped with that figure's own `created_at` / `created_by_session` and `updated_*` (the lens was asserted when the figure was written). Count before: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select sum(identity_code is not null)+sum(icf_code is not null)+sum(needs_code is not null)+sum(medical_code is not null) from source_value_extractions').fetchone())"`; after, `select count(*) from extraction_lens_links where basis='carried'` prints the same number.
2. **NULLed and held NULL.** The table is rebuilt (SQLite cannot drop or change a CHECK in place) with the four columns kept, their values set to NULL in the copy, and the D-0182 CHECK `COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL` replaced by `CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NULL)`, with a comment: "HISTORY, retired by migration NNN: a figure's lens lives in extraction_lens_links (OR-1c). Kept because committed data migrations INSERT these columns (rule 5); never written again." The inverted CHECK makes the retirement a typed fact rather than a convention: no writer can bring the dead home back.
3. **Why not dropped.** `git grep -l -E 'INSERT INTO "?source_value_extractions"?' -- 'scripts/migrations/data_*' | wc -l` prints the number of committed data migrations that INSERT these columns; replay needs the columns to exist.
4. **Why `AFTER_DATA` is required.** `scripts/migrate_db.py --rebuild` applies every numbered schema migration before every data migration unless a schema migration carries `-- AFTER_DATA: <timestamp>` (`grep -n 'AFTER_DATA' scripts/migrate_db.py`). Without the marker, the rebuild would carry from an empty table and then replay the data migrations into the columns, so the rebuilt database would hold values in the columns and no links, and the CHECK of step 2 would refuse those replayed INSERTs. The migration therefore declares, on its own line, the timestamp of the newest committed data migration at execution time: `ls scripts/migrations/data_*.sql | sed -E 's/.*data_([0-9]{14})_.*/\1/' | sort | tail -1`. Migration 114 is the precedent (`grep -n AFTER_DATA scripts/migrations/114_extraction_slug_and_root.sql`).

`specifications` is not touched: its four columns are the cell key (section 4), and its D-0182 CHECK stays.

## 4. How the engine's gather uses the links (consumed by T-019, then T-055)

**The rule.** A cell is the set of codes its four key columns state (at least one). A figure reaches the cell when, for every lens the cell states, the figure has a live link carrying that code. Lenses the cell leaves NULL impose nothing. So a figure linked to `{WHEEL, d465}` reaches the cells `(WHEEL)`, `(d465)` and `(WHEEL, d465)`, and a figure linked to `{d450, d465}` reaches `(d450)` and `(d465)`: written once, counted in each.

```sql
-- sketch: the lens predicate T-019 adds to assess_cell._gather's WHERE (x = source_value_extractions)
  AND (:identity IS NULL OR EXISTS (SELECT 1 FROM v_live_lens_links k
                                    WHERE k.extraction_id = x.extraction_id AND k.identity_code = :identity))
  AND (:icf      IS NULL OR EXISTS (SELECT 1 FROM v_live_lens_links k
                                    WHERE k.extraction_id = x.extraction_id AND k.icf_code      = :icf))
  AND (:needs    IS NULL OR EXISTS (SELECT 1 FROM v_live_lens_links k
                                    WHERE k.extraction_id = x.extraction_id AND k.needs_code    = :needs))
  AND (:medical  IS NULL OR EXISTS (SELECT 1 FROM v_live_lens_links k
                                    WHERE k.extraction_id = x.extraction_id AND k.medical_code  = :medical))
```

**T-055's widening, identity only.** The identity `EXISTS` becomes `k.identity_code IN (SELECT code FROM family)` with
`WITH RECURSIVE family(code) AS (SELECT :identity UNION SELECT i.identity_code FROM base_taxonomy_identity i JOIN family f ON i.parent_code = f.code)`.
A child's cell gathers only that child (its family is itself plus its own descendants, none today).

**Why "cell within figure" and not exact match.** `specifications` holds one code per model. Under exact match a figure with two ICF codes could reach no cell at all, which is the defect OR-1c exists to remove. Under "any code in common" a figure tagged `(MOB, d450)` would reach the cell `(BLIND, d450)` through d450 alone, which is the wrong-group defect T-019 fixes.

**AT-32's second half** ("a determination's lens set lists every model its governing figures carry") is T-019's: the engine reads, for each determination, the distinct models of its governing figures' live links from `v_live_lens_links` and reports any model the cell key leaves NULL. Several codes of one model are several cells (section 11, alternative D).

## 5. Migration shape (one schema migration; derive its number, never type it)

Number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one, zero-padded; file `scripts/migrations/NNN_extraction_lens_links.sql`; it ends `PRAGMA user_version = NNN;`. Template for the rebuild: `scripts/migrations/114_extraction_slug_and_root.sql` (drop the views that name the table, create `_NNN_new_source_value_extractions`, copy, drop, rename, recreate indexes, restore the `sqlite_sequence` floor, recreate the views). In order:

1. Header comment naming OR-1c, this design, and the `-- AFTER_DATA: <newest data_ timestamp>` line (section 3, item 4).
2. `CREATE TABLE extraction_lens_links`, its indexes (section 2).
3. Four `INSERT INTO extraction_lens_links (extraction_id, <lens>, basis, created_at, created_by_session, updated_at, updated_by_session) SELECT extraction_id, <lens>, 'carried', created_at, created_by_session, COALESCE(updated_at, created_at), COALESCE(updated_by_session, created_by_session) FROM source_value_extractions WHERE <lens> IS NOT NULL;` — one per lens column, before the rebuild. (`created_by_session` is NOT NULL here; if any figure has it NULL — `select count(*) from source_value_extractions where created_by_session is null` — use the migration's own stem for those rows and say so in the header.)
4. Rebuild `source_value_extractions` exactly as it stands except: the four lens columns are copied as `NULL`; the D-0182 CHECK becomes the all-NULL CHECK of section 3, item 2. Every other column, CHECK, default and comment is copied verbatim from `select sql from sqlite_master where name='source_value_extractions'` read at execution time (T-016, T-017 and others may have changed the table since this was written).
5. Recreate every view, trigger and index that names the table: list them at execution with `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,name from sqlite_master where sql like '%source_value_extractions%' and name<>'source_value_extractions'\").fetchall())"`. Each view's text is copied from `sqlite_master` unchanged (none reads the four lens columns today: confirm by grepping the printed SQL for `identity_code`). Then `CREATE VIEW v_live_lens_links`.
6. Not in the migration, in the same pull request: append to `references/project-standards.md` one entry, headed in the form of the 2026-09-01 precedent (`grep -n -F "and the 2026-08-28 ACTION above is superseded on that clause only" references/project-standards.md`), recording that the clause "Never a `population_*` link table" of the 2026-08-28 ACTION is SUPERSEDED, for a figure's lens codes only, by the link-table ruling of 2026-11-06 (OR-1c), as the owner answered on 2026-11-12 (OD-39, fifth set; cite it by `grep -n -F "OD-39: the 2026-11-06 link-table ruling supersedes" references/project-standards.md`). Say that the rest of the 2026-08-28 ACTION stands. **[CORRECTED 2026-11-12, in the fold of the fifth set] Do not write a machine `SUPERSEDES:`/`BY:` pair for this target.** The first version of this step did, and claimed both quotes occur once; that was measured with `grep -c`, which counts lines. Under the audit's own normalisation (`dbcore.count_ledger_quote`, which joins wrapped lines) the target quote "real FKs. Never a `population_*` link table." already occurs twice (the 2026-08-28 ACTION and the 2026-09-01 entry's quotation of it), the audit counts the target in the raw ledger, so the citation line itself would add a third, and the audit requires a SUPERSEDED marker in the target's own paragraph or the next one, which the append-only ledger forbids. Tested on a scratch copy on 2026-11-12: appending the pair turned `supersession_backpointer_audit` from PASS to FAIL ("target quote occurs 3 time(s)"). Run `python3 scripts/audit/supersession_backpointer_audit.py` before and after the append; the verdict must be the same. A supersession whose target is in the ledger is recorded in prose; the audit covers targets outside it (CLAUDE.md rule 0: "Naming them is yours").

Proof: `python3 scripts/migrate_db.py` on the branch; `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` exits 0; `python3 scripts/audit/migration_reproducibility.py --deep` passes (it compares every row, so it sees the carry and the NULLs); `python3 scripts/audit/joined_cells_census.py` before and after (a new candidate is a stop: `basis_text` holds one quote, not two things).

## 6. The writers (exact verbs and flags)

All in `scripts/db.py`; locate by symbol. `_LENS_COLUMNS` (the lens → registry map) is reused for every code check; nothing restates a vocabulary (`basis` choices come from `dbcore.check_values(conn, "extraction_lens_links", "basis")`, minus `carried`, which only the migration writes).

**`add-extraction` and `derive-extraction`, changed.**
- `--identity`, `--icf`, `--needs`, `--medical` become `action="append"` (each may be repeated; argparse today keeps only the last of a repeated flag, silently).
- New, required whenever any lens flag is given (which is always, since a figure needs one): `--lens-basis {named_in_text,heading,study_participants}` and `--lens-basis-text "<words>"`; they apply to every link the call writes. A code with a different warrant is added afterwards with `add-lens-link`.
- `insert_extraction` validates each code as today (registry row exists, registry not empty), refuses a `deprecated` identity code, refuses a duplicate code within the call, writes the figure with the four columns NULL, then one link per code, in one transaction. The refusal "an extraction must be stated in at least one lens (D-0182)" is kept word for word. The result's `lens` key becomes a list of `{link_id, lens, code}`. The existence and empty-registry refusals move out of `insert_extraction` into one shared helper that `add-lens-link` calls as well. Use that helper, not `dbcore.fk_declared`: `fk_declared` has no empty-registry message (the CLAUDE.md §4 trap), so using it would drop a refusal `insert_extraction` gives today.
- **The deprecated-code refusal [corrected 2026-11-13].** The first version said "with the successor named (T-054's general refusal, reused)". No such refusal exists in this stack, and no successor column either: `base_taxonomy_identity` has only `status` (`active`/`deprecated`). T-018 does not depend on T-054, and T-054 does not depend on T-018. So the helper refuses a code whose `status` is `deprecated` in plain words: "a figure is not newly stated in a retired group; use the live code that replaced it". It names no successor. T-054 (its item 3) extends this refusal to read the successor column it adds. If T-054 has merged first, the helper calls T-054's refusal instead (task file §2).
- **The Python API [decided 2026-11-13].** `insert_extraction(data, session, …)` keeps its signature. Each lens key in `data` (`identity_code`, `icf_code`, `needs_code`, `medical_code`) takes one code or a list of codes. The warrant travels in the same dict as two more keys, `lens_basis` and `lens_basis_text`. These are not columns: `insert_extraction` removes them from `data` before `dbcore.validate_cols`, and they become `basis` and `basis_text` of every link the call writes. The CLI dispatch puts `--lens-basis` and `--lens-basis-text` into the dict it already builds. `derive_extraction` gains the keyword arguments `lens_basis=` and `lens_basis_text=` and puts them into its own `data`; its lens keywords accept a list. Why keys and not keyword arguments: the codes are already payload keys and their warrant belongs beside them, and every test reaches `insert_extraction` through a payload builder. So the repair is one edit per builder (the warrant's words may be the payload's own `claim_text`, which the found-in-the-figure check then accepts), not an edit at each call. List the call sites with `git grep -n -E 'insert_extraction|derive_extraction' -- scripts/tests scripts/audit` and the builders behind them with `git grep -n -E 'def (extraction|claim)\(|X_PAYLOAD =|X_P =' -- scripts/tests`. On 2026-11-13 these were the `extraction()` builder in `test_run_pipeline_refusals.py`; `X_PAYLOAD`, `X_P` and one literal payload in `test_db_amend_writers.py`; and the `claim()` builder and one literal payload passed to `fn("insert_extraction")` in `test_scan_contract.py`. A literal payload whose case expects a refusal that fires before the lens block (an undeclared jurisdiction, a retired parameter) needs no warrant; give it one anyway if the order of refusals is in doubt. Re-run the commands; a new hit is a caller. The CLI callers of `add-extraction` and `derive-extraction` in tests and skills need `--lens-basis` and `--lens-basis-text` (`git grep -n -E '"(add|derive)-extraction"' -- scripts/tests skills .claude`).

**`add-lens-link`, new.**
`db.py add-lens-link --extraction-id N (--identity C | --icf C | --needs C | --medical C) --basis {named_in_text,heading,study_participants} --basis-text "<words>" --session S [--dry-run]`
The flags are `--basis` and `--basis-text`, as written here; T-102's design calls the verb with these names, so do not reuse `add-extraction`'s `--lens-basis` names for it (the pilot did, and that is a divergence, not a choice). Refuses, each in words naming the next action: an extraction that does not exist; none or more than one code flag; a code not in its registry, or a registry with no rows (the shared helper of `add-extraction` above, not `dbcore.fk_declared`); a `deprecated` identity code (the plain refusal above); a blank `--basis-text`; a `--basis-text` that is not found, case-insensitively, in the figure's `claim_text`, `source_section` or `root_population_note`, nor in a file saved for the figure's source (the helper `add-alias` already uses: `grep -n 'classify_observation' scripts/db.py`), nor, for `study_participants`, in a `study_population` of an `evidence_population_match` row whose `source_ref` is the figure's `ref_id` (the column is `source_ref`, not `ref_id`: `PRAGMA table_info(evidence_population_match)`; the pilot's query named `ref_id` and would have raised `no such column` on the first such call); a live link for the same figure and code, **except** when that live link's basis is `carried`, in which case the carried link is retired in the same transaction with reason `superseded by judged link <new id>` (a judged warrant replaces a carried one in one act).

**`retire-lens-link`, new.**
`db.py retire-lens-link --link-id N --reason "<why>" --session S [--dry-run]`
Sets `retired_at`, `retired_by_session`, `retirement_reason` and the `updated_*` pair. Refuses: no such link; already retired; a blank reason; **the figure's last live link** ("add the replacing link first with add-lens-link; a figure with no lens is a value about nobody", D-0182).

**Not changed.** `amend-extraction` stays a field writer; it gains no lens arguments (this corrects the task file's item 2, which said it would). `specifications`, `search_executions`, `connection_targets`, `conflicts`, `determination_gates` keep their own single lens columns: OR-1c concerns figures.

**Captured set.** `dbcore.writable_tables(conn)` derives the tables from the writers' `INSERT INTO` text and orders them by the FK graph, so `extraction_lens_links` enters it after `source_value_extractions` with no list edited; `emit_batch_sql.py` captures the retirements as `UPDATE`s by `link_id`. **[Corrected 2026-11-13] Being captured is not enough: the capture must replay.** `emit` writes each table's INSERTs before its UPDATEs. A batch in which a judged link replaces a carried one therefore inserts the judged link while the carried one is still live, and the replay fails on `ux_extraction_lens_live` (pilot: `sqlite3.IntegrityError: UNIQUE constraint failed: index 'ux_extraction_lens_live'`; with the UPDATE first the replay reproduced the scratch table exactly). The same happens to a retired link re-added, and to a `specifications` cell retired and determined again in one batch (`idx_spec_row_identity`). **Fix: in `emit`, a table's UPDATEs are written before its INSERTs** (`lines += updates + inserts`; deletes stay first, and the restore pairs stay inside `inserts`). Why it is safe for every table: the UPDATEs touch only rows that already exist and bring them to their end-state values, so after each statement the table holds a subset of the batch's end-state rows. A UNIQUE index that holds over a set of rows holds over any subset of them, partial indexes included. CHECKs and the one trigger (`trg_spec_retire_needs_reason`) read only their own row. Foreign keys are not checked statement by statement: `migrate_db.py` applies every migration with them off and checks them once before commit (`_apply_atomically`), so an UPDATE that points at a row inserted later in the same file is fine. Rejected: having `add-lens-link` write the retirement first (the emitter diffs end states and never sees a verb's order); a non-unique or trigger-held form of the live-link rule (it weakens a refusal); a special case for this table (the defect is general). Confirm membership: `python3 -I -c "import sys,sqlite3;sys.path.insert(0,'scripts');import dbcore;c=sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True);t=dbcore.writable_tables(c);print('extraction_lens_links' in t, t.index('extraction_lens_links')>t.index('source_value_extractions'))" "$SCRATCH/t.db"` prints `True True` on the migrated scratch copy.

## 7. What reads it

| Reader | Reads | Task |
|---|---|---|
| `scripts/assess/assess_cell.py` `_gather` (the lens predicate) | `v_live_lens_links` | T-019 |
| the same predicate, identity through `parent_code` | `v_live_lens_links`, `base_taxonomy_identity` | T-055 |
| `add-extraction` output; `add-lens-link`, `retire-lens-link` refusals | the table | this task |
| `retire-identity` "a live row still carries this code" refusal (derived from the FKs into `base_taxonomy_identity`) | the table, filtered `retired_at IS NULL` | built by T-054, which already names this table's live filter (its item 3); T-018 does not write it. If T-054 merged first, T-018 confirms it on a scratch copy (task file §2) |
| `scripts/research/emit_batch_sql.py` `emit` | the table's UPDATEs and INSERTs, in that order | this task (section 6, "Captured set"); every research batch after it |
| `workplan/pipeline-state-graph/build_graph.py --check` | `governance/stage-map.yaml`'s line for the table | this task |
| `test_db_integrity` case "every figure has a live lens link" | `v_live_lens_links` | this task |
| lens re-tagging, mobility carry, `ALL` re-tag | the verbs | T-106, T-102, T-115 (research) |

## 8. The backfill

- **Mechanical, in this tooling pull request:** the carry of section 3. It is a reshape of values already held, decided by no one, and it must land with the schema or every figure would lose its lens when the columns go NULL.
- **Judged, never here (rule 10):** filling further models and codes (T-106, `basis named_in_text`), moving `MOB` figures to the device children (T-102), moving figures off `ALL` (T-115). Each is a research pull request through the write path, using `add-lens-link` and `retire-lens-link`; a judged link for a code that already has a `carried` link replaces it in one call.

## 9. Caller sweep (found by reading the code on 2026-11-12; re-run the task file's section 5 commands, a new hit is judged)

| Caller | Why it is a caller | What changes |
|---|---|---|
| `scripts/db.py` `insert_extraction`, the `add-extraction` and `derive-extraction` parsers and dispatch | write the four columns | write links; repeated flags; `--lens-basis*` |
| `scripts/db.py` `_LENS_COLUMNS` | lens → registry map | reused, unchanged |
| `scripts/db.py` `retire_identity` (T-054) and any writer whose "live row carries this code" count is derived from the FKs into `base_taxonomy_identity` | would count retired links, or the NULL columns | **[corrected 2026-11-13]** not in this stack: `retire_identity` does not exist until T-054 merges (`git grep -n 'def retire_identity' scripts/db.py`), and T-054's item 3 already counts `extraction_lens_links` live-only. T-018 writes nothing here. If T-054 merged first, confirm the live-only count on a scratch copy; a failure is a stop (task file §9) |
| `scripts/research/emit_batch_sql.py` `emit` | writes a table's INSERTs before its UPDATEs, so a replaced carried link cannot be replayed | UPDATEs before INSERTs (section 6, "Captured set"); red test T018-08 |
| `governance/stage-map.yaml` | `build_graph.py --check` fails on a table it does not place, and the name sweep cannot find this, because the map names no lens column | `extraction_lens_links: judgment`, with a dated comment naming the judge and the reason (task file §4 item 5) |
| registered check `research_dod_selftest` (**blocking**; `scripts/audit/research_batch_dod.py --selftest`) | its corpus is cloned from the live schema and raw-INSERTs a figure naming `identity_code`; after the migration it dies with `IntegrityError: CHECK constraint failed` | run before and after (task file §6); the fixture repair is the next row |
| `scripts/db.py` the lens-moving writer T-056 item 4 would have built | wrote `identity_code` on the figure | not built; replaced by `add-lens-link` + `retire-lens-link` (T-056 task file corrected) |
| `scripts/audit/research_batch_dod.py` (its fixture `INSERT INTO source_value_extractions (… identity_code …)`: `grep -n 'INSERT INTO source_value_extractions' scripts/audit/research_batch_dod.py`) | the new CHECK refuses it | write the figure without lens columns and its link row (basis `carried` with a NULL `basis_text` is a valid row for a fixture standing for a pre-existing figure) |
| `scripts/tests/test_scan_contract.py` (fixture INSERTs naming `identity_code`; find all raw lens writes with the task file's §5 raw-write sweep, since one of these INSERTs names the column on its second line) | the new CHECK refuses them | same; one small fixture helper that writes the figure and its link is enough |
| `scripts/tests/test_db_amend_writers.py`, `test_run_pipeline_refusals.py`, `test_evidence_cell_state_2_3.py`, `test_db_integrity.py` | exercise `add-extraction` with lens flags or read the columns | run before/after; fix any fixture the CHECK refuses; add the new integrity case |
| `scripts/tests/test_assess_cell_pilot.py` | builds its own fixture schema with the four columns | runs unchanged here; T-019 rewrites its gather fixtures onto links |
| views and indexes naming `source_value_extractions` (section 5, step 5) | dropped and recreated by the rebuild | recreated verbatim |
| `governance/check-registry.yaml` | the integrity case lives in a registered check | no entry added: the case goes into the registered `test_db_integrity` |
| skills naming `add-extraction --identity` (`git grep -n -e '--identity' -e '--icf' -e '--needs' -- skills .claude`) | describe a single lens flag | one sentence each: flags repeat, `--lens-basis` and `--lens-basis-text` required |
| prose: `architecture/schema-spec.md`, `architecture/meta-scripts-spec.md`, `governance/evidence-architecture.md`, `governance/context-map.yaml`, `workplan/pipeline-state-graph/machines.yaml` (find the sentences with the task file's prose `git grep` for each lens name) | state that a figure's lens is its four columns | corrected to the link table; `python3 workplan/pipeline-state-graph/build_graph.py --check` run once (new verbs) |
| `schemas/evidence_state.py`, `scripts/validate_evidence_state.py`, `scripts/validate_verification_consistency.py`, `scripts/audit/medical_lens_integrity.py`, `scripts/audit/derivation_handshake_integrity.py` | read **`specifications`'** lens columns, not the figure's | mentions; unchanged |

## 10. Red tests (prefix `T018-`; confirm the prefix is free in each file first)

All probes are chosen by query on a scratch copy; nothing typed that the database can derive. Fixture rows are labelled `TASK-FIXTURE`.

| Id | File | What it does | Expected today (red) | After (green) |
|---|---|---|---|---|
| T018-01 (AT-32) | `scripts/tests/test_db_amend_writers.py` | `add-extraction` on a scratch copy for an admitted, non-superseded `ref_id` and an active parameter (both by query), `--icf <d1> --icf <d2>` where d1, d2 are the first two `d%` codes of `base_icf` by `icf_code`, `--lens-basis named_in_text --lens-basis-text <a word of the claim text>`; then reads the figure's live links, guarded so a missing view records red rather than raising | **[corrected 2026-11-13]** argparse refuses first: rc 2, "unrecognized arguments: --lens-basis …"; the case records `[✗]` (an unguarded read of the missing view would raise and hide the later cases); without the new flags the row would hold only d2 | one figure; two live links {d1, d2}; the four columns NULL |
| T018-02 | same | `retire-lens-link` on a figure's only live link | `invalid choice: 'retire-lens-link'` | refused, naming `add-lens-link`; nothing written |
| T018-03 | same | `add-lens-link` with a `--basis-text` absent from the figure's words and from its source's saved file | `invalid choice: 'add-lens-link'` | refused, naming where the words were looked for |
| T018-04 | same | `add-lens-link` on a code that has a `carried` link (the first live carried identity link whose figure has a non-blank `claim_text`, by query; the basis text is a word of that claim text) | `invalid choice: 'add-lens-link'`; on the unchanged schema there is no carried link to probe, and the case **records a failure** saying so (never `SKIPPED-NO-FIXTURE`, which would be a vacuous pass) | the carried link retired with reason `superseded by judged link <id>`; one live link |
| T018-05 | `scripts/tests/test_db_integrity.py`, new `record()` case (next free id: `grep -o 'record("[A-Z][0-9]*' scripts/tests/test_db_integrity.py \| sort -u`) | every row of `source_value_extractions` has at least one row in `v_live_lens_links`; shown red on a copy where one link is retired by raw SQL (seeded defect, then removed) | case absent; on the seeded copy the new case prints `[✗]` | `[✓]` with `subject=` the figure count |
| T018-06 | **not a test file [moved 2026-11-13]** | carry fidelity: for every figure, the set of `carried` links equals the set of non-NULL lens columns of the same figure before the migration, with equal stamps | — | run **once**, straight after the migration is applied, with the command in the task file §6 ("The carry assertion"); its output goes in the pull request. It cannot be a committed case: no pre-migration copy exists once the migration is committed, and the carried set rightly shrinks as T-106, T-102 and T-115 retire links |
| T018-07 | `scripts/tests/test_db_amend_writers.py` | an `INSERT INTO source_value_extractions` naming `identity_code` on the migrated copy | succeeds today (the dead home is writable) | `CHECK constraint failed` |
| T018-08 | `scripts/tests/test_db_amend_writers.py` | **capture round trip [added 2026-11-13].** Immediately before the call, copy the test's scratch database to `base`. On the scratch copy, `add-lens-link` replaces a carried link (T018-04's probe, or one chosen the same way). Run `emit_batch_sql.emit(<scratch>, <base>, <out>, replay_path=<base>)`. Import the module as the existing X14 and M03 cases do. `replay_path=<base>` spares a rebuild of the whole chain, as the emitter's own selftest does. Apply the emitted statements to a second copy of `base` the way `migrate_db.py` applies a data migration: locate `_apply_atomically` in `scripts/migrate_db.py` by symbol and call it, or reproduce it (foreign keys off, one transaction, `PRAGMA foreign_key_check` empty before commit). Then compare `SELECT * FROM extraction_lens_links ORDER BY link_id` between the replay and the scratch copy | on the unchanged code `add-lens-link` does not exist (records `[✗]`); with the verb but the emitter unchanged, the replay raises `UNIQUE constraint failed: index 'ux_extraction_lens_live'` (show this red by reverting the one-line order change, then restore it) | the replay applies, and the two tables are equal row for row |

AT-32's second half is T-019's (section 4).

## 11. Alternatives rejected

- **A. One row per figure per combination of codes** (write the figure once per (identity, ICF, need) combination). The owner's condition was "unless that is more prone to errors"; the ledger measured the multiplication with `python3 -c` in the OR-1c entry (re-run it there). Every repeated value and quote is a copy (rule 5), and a correction to one copy misses the others.
- **B. A polymorphic link `(extraction_id, lens TEXT, code TEXT)`.** One column less, but the code is a foreign key to no table: a typo is stored. The 2026-08-28 ruling's "every lens column is a real typed foreign key — nothing is polymorphic" forbids it.
- **C. Keep the four columns as the figure's first code per model and use links only for extra codes.** Two homes for one fact (rule 5): every reader must union two places, and a re-tag must decide which to edit. Rejected; this is the "parity check is not a fix" case.
- **D. A link table for determinations too.** A cell is a key; `validate_cell_undetermined`'s uniqueness and `derivation_sha` are over one code per model. A set-valued key would make two determinations of the same figures incomparable. Several codes of one model are several cells; the figure reaches each.
- **E. Drop the four columns.** Committed data migrations INSERT them (section 3, item 3); a drop breaks the rebuild.
- **F. Keep the D-0182 CHECK on the figure and keep writing the columns from the first link.** That is alternative C with a cosmetic difference.
- **G. A trigger enforcing "at least one live link".** SQLite has no deferred triggers; an `AFTER INSERT` on the figure fires before its links exist. The writer refusal plus the blocking integrity case is the floor a trigger cannot hold.
- **H. No `basis` columns.** Smaller, but a judged link and a carried one would look the same, and the warrant OD-06 and D-2 require would live only in the session's prose.

## 12. What this changes in other task files (applied in the same pass as this design)

- **T-018 itself:** Sonnet may now execute it against this design; item 2 names the two new verbs and drops `amend-extraction` (section 6).
- **T-019:** the gather predicate is section 4 of this file; AT-32's second half is its own.
- **T-055:** the identity predicate widens on `v_live_lens_links`.
- **T-056:** item 4 (a writer that rewrites `identity_code` on a figure, only when the code is already `deprecated`) is replaced by `add-lens-link` / `retire-lens-link`. As written it could not work: T-054's retirement refuses a code that live rows still carry, and item 4 moved rows only off a code that was already retired.
- **T-106, T-115, T-102:** write and retire links with these verbs; a judged link replaces a carried one in one call.
- **T-019, T-102, T-106, T-115 evidence commands and T-102's after-test (3):** they read a figure's lens from `source_value_extractions.identity_code` (and the other three columns); after this task those columns are NULL, so each would print an empty or zero result having examined nothing and the executor would stop on "the ground has moved" or, worse, pass a vacuous test. Each now reads `v_live_lens_links`.
## 13. Not resolved here

- [ANSWERED 2026-11-12, fifth set, OD-39] Whether the owner reads OR-1c's measurement as meeting "unless that is more prone to errors": the owner answered that the 2026-11-06 ruling supersedes the 2026-08-28 clause, so the link table is built.
- The figure-row CHECK becomes a writer refusal plus a blocking integrity case: a hand-written INSERT that bypasses `db.py` and adds a figure with no link would pass the schema and fail only the integrity case. That is the same exposure every cross-table rule in this schema has.
- [2026-11-13] A data migration replayed after this migration's `AFTER_DATA` timestamp that INSERTs a lens column is refused by the all-NULL CHECK. A research batch captured before T-018 merges and merged after it must be captured again through the new verbs (task file §4).
