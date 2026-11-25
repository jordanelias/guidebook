# T-147  The ICF lens has a hierarchy: umbrellas, a glossary, and a gather that reaches the codes beneath an umbrella

_Tooling only (CLAUDE.md rule 10). The rows are T-148's. Read `CLAUDE.md` first. Authority: the ledger entries "Owner statements 2026-11-22 and 2026-11-23" and "Delegated resolutions 2026-11-23" (OD-74, OD-75) in `references/project-standards.md`; the reasoning and its independent check are in `scratchpad/session_2026-11-22-icf-umbrella-glossary/reconciliation.md`._

## What this task changes

| Object | Change | What reads it |
|---|---|---|
| `base_icf.parent_code` (migration 167) | nullable pointer to the code or block above | `dbcore.family_sql(conn, 'icf_code')`, `db.py icf-glossary` |
| `dbcore.family_sql(conn, col)`, `lens_families`, `lens_differs`, `LENS_COLUMNS` | one family rule, derived from the schema: a lens has a hierarchy when its registry carries `parent_code` (identity, ICF; the access-need lens does not), and a database that predates the column reads each code as its own family. Replaces `IDENTITY_FAMILY_SQL`, `identity_family` and the identity-only `lens_differs`; `assess_cell.LENS_COLUMNS` and `db._LENS_COLUMNS` are now `dbcore.LENS_COLUMNS` itself (one home; `HI-0` asserts identity, not equality) | `assess_cell._lens_clause` (now takes `conn`) and its gate filter, `db.py cell-status` (the extraction count, gap and gate filters), `derivation_handshake_integrity` |
| `db.py import-icf-tree` | mints every WHO level-2 and level-3 block as a range row, sets `parent_code` on the codes the project holds, names the untitled, resets a parent that differs from the payload's (parent is derived data, so the verb is safe to run again after a code is minted), replaces a title whose source is not a payload (returning old value and source), takes the payload as source of a title it confirms (returning the old title and source), refuses a payload-sourced title that differs, lists a held code WHO does not name (`d910–d920`) | the data batch (T-148) |
| `db.py icf-glossary [--umbrella CODE]` | read-only: each umbrella with the codes beneath it, WHO's titles, and the live link counts | the owner |
| `scripts/tests/test_icf_hierarchy.py`, `ICF-01..04` in `test_assess_cell_pilot.py` | the cases; the hierarchy test builds its own fixture (it does not read the canonical rows, so it keeps its meaning after T-148); `ICF-01` and `ICF-04` go red when the ICF lens is made flat | `run_checks.py` |

Without the family rule a cell keyed on `b750–b789` gathers nothing from a figure linked to `b765`; without the import verb a session types some 440 parents and titles by hand (rule 8).

## Rulings it carries out, and what it leaves

- A block is a row keyed by the span of the 3-digit categories beneath it, derived from the payload (the tabulation holds no range string). Level 1 (Body functions and the others) is `component`.
- `d910–d920` is not a WHO block (WHO's is `d910–d999`); the verb leaves it as stored.
- The access-need lens stays flat (`access_needs.family`). No identity parent writer is added (OD-76 withdrawn). No pairs table (OD-73 is the owner's). `identity_icf_map` is untouched and frozen (OD-77).
- `RULE_VERSION` stays: no ICF parent is written by this task, and the data batch changes only cells keyed on an ICF code, of which `specifications` holds none today (`select count(*) from specifications where icf_code is not null`). Re-derive before T-148 merges.
- `set-icf-title` takes the code through `dbcore.icf_key` and is otherwise unchanged: the import verb is the one path that replaces a title, because it compares a title with that code's own row.
- `add-icf-code` parents a code it mints by the import's own rule (the payload's nearest present ancestor, and the children WHO places beneath it), reading the payload from the block rows the import sourced, so a code minted after the import is never orphaned and a figure linked to it reaches its umbrella's cell at once. A span typed with a hyphen, an em dash or a spaced en dash is stored as the unspaced en dash (`dbcore.icf_key`), the key the import mints; `icf-glossary --umbrella` takes the same forms.
- `icf-glossary` labels its counts by what they count: `access_need_icf_rows`, `identity_icf_map_rows (frozen, OD-77)`, `identity_need_icf_reviewed` and `identity_need_icf_pending`.
- Owed before the first ICF-keyed determination is written (T-110 or earlier): a fixture case in the derivation-handshake audit's test that drives an ICF lens through `lens_differs(g, s, lens_families(con, s))`. The audit examines no ICF-keyed determination today, so the line examines nothing; the case is filed as a gap by the data batch, not here (rule 10).

## T-148 (the research pull request, after this merges)

1. Run `import-icf-tree --payload retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip` on a scratch copy; put the `replaced` list (code, old title, old source, new title), the `confirmed` list (code, old title, old source) and any `reparented` triples in the data migration's header. Re-derive `select count(*) from specifications where icf_code is not null` before writing parents (RULE_VERSION stays only while it is 0).
2. Whether to import the rest of the classification (373 3-digit categories) is the owner's to say; the first batch holds the blocks and the codes the project already holds.
3. Re-run the pairs and mapping questions only after the owner answers OD-73, OD-78 and the mapping question.
