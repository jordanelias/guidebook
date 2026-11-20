# T-145  A disability identity, an access need and an ICF code are linked in one judged, reviewable table, readable from any of the three

> **ANSWERED 2026-11-20 and BUILT** (migration 165, `identity_need_icf`, `v_lens_crosswalk`, verbs `propose-identity-need-icf`, `review-identity-need-icf`, `lens-crosswalk`). Question 1: all three keys, in the owner's words. Questions 2 to 4 at the recommendations, as unratified assumptions. Ledger: `grep -n -F "Owner statements 2026-11-20 (fifth)" references/project-standards.md`. The triples that fill it are the later research pull request.

_One task, one pull request, tooling only (CLAUDE.md rule 10: the rows that fill the table are a later research pull request). Read `CLAUDE.md` first. Authored 2026-11-20 on the owner's ruling (ledger: `grep -n -F "## Owner statement 2026-11-20 (second)" references/project-standards.md`). Every figure below is given with the command that produces it: re-run the command; do not trust the number._

**Pilot status.** Not piloted. Expect to find a defect in this file, and report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-145 |
| Title | One judged table links identity, access need and ICF code, with a view readable from any of the three |
| Kind | **TOOLING** (schema migration, one writer pair, one view) |
| Executor | Opus-class for the design questions; Sonnet-class once section 4 is answered |
| Traces to | The owner's 2026-11-20 statements (ledger: `grep -n -F "## Owner statements 2026-11-20 — translation runs before judgment" references/project-standards.md`); `MAPPING-DESIGN.md` section 2(a), whose rejection of a new link table the owner's ruling supersedes (rule 0); the schema-shape ruling of 2026-11-06 (one value per cell) |

## 2. Preconditions

- **Owner decisions:** the four questions of section 4, in the ledger in the owner's words.
- **Read first:** `MAPPING-DESIGN.md` sections 1 and 2 (the proposals the recording session reads; this task does not change the engine, `_lens_clause`, D-0184 or OR-1); T-126 to T-128 (what is built for a code value's lens).
- **Tests that must be red before you start:** section 3's command prints the unmapped identities and an empty identity-to-need answer.

## 3. The problem, in the guidebook's terms

Readers will navigate the repository first by a disability identity (owner, 2026-11-20). From an identity the database cannot say which access needs it has, and for 11 of the 23 identities it cannot name an ICF code. The two maps that exist cross at almost nothing: identities map only to ICF activity (d) codes, needs mostly to environmental (e) codes. The earlier identity-to-need route was dropped by migration 109, and `access_needs.absorbs` is a delimited free-text cell naming identities, which one-value-per-cell does not allow to stay the only home.

**Evidence commands** (read-only):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select identity_code from base_taxonomy_identity where status=\'active\' and identity_code not in (select identity_code from identity_icf_map where retired_at is null) order by 1').fetchall())"
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[1] for r in c.execute('pragma table_info(access_needs)')])"
python3 scripts/audit/joined_cells_census.py
```

(If `base_taxonomy_identity` has no `status` column on the day, read its columns first and use the live name.)

## 4. The change, and the four questions that are the owner's

A table of judged links, stored sparsely: a cell with no row reads as not yet judged; a row in the not-applicable state reads as judged and not applying. Following the shape of `identity_icf_map` (the nearest sibling): its own primary key, real foreign keys to `base_taxonomy_identity`, `access_needs` and `base_icf`, a warrant held in the table's own cells (never a pointer to a ledger heading), `created_by_session`, `created_at`, and the retire-in-place columns with their paired CHECK.

**Plus:** a state column whose values are the project's existing cell states (derive them from the column CHECK they already carry: `grep -n -E "stated.*provisional.*pending.*not_applicable" scripts/migrations/*.sql | head`); a reviewed pair (`reviewed_at`, `reviewed_by`) set only by a review verb; one writer to propose a link (state `pending`) and one to review a batch (the owner's reviewed state), each refusing as `db.py` writers do (a blank warrant, an unknown code, a duplicate live row, a review that names no rows); and one view, `v_lens_crosswalk`, returning for an identity its needs and ICF codes, and for a need or an ICF code its identities, joined on the shared codes (a cross-stage view is the pointer, CLAUDE.md section 3).

**Questions for the owner (the design cannot be finished without them):**

1. **How many of the three must a row hold?** All three (a cell of the cube), or at least two (so identity–need, identity–ICF and need–ICF faces are all fillable, with the third left empty)? Recommended: at least two, because 11 identities have no ICF code and the maps cross at 2 codes.
2. **Who may mark a row stated?** Only the owner's review verb, or a session once a source attests it? Recommended: only a review the owner makes, per batch, as the owner confirmed on 2026-11-20.
3. **What becomes of `access_needs.absorbs` and the 61 + 43 rows of the two flat maps?** Kept and read as proposals (the design of 2026-11-15), or folded into the new table's rows? Recommended: kept as proposals now; `absorbs` retired in a later task once the table covers every need.
4. **Does a not-applicable row need a warrant?** Recommended: yes, the same cell as a stated row, because a quiet "does not apply" is the failure the cell states exist to prevent.

## 5. Caller sweep

Rule 4: a view is a caller, so is a skill and the registry. Grep `sqlite_master` and the tree for `absorbs`, `identity_icf_map`, `access_need_icf` and `extraction_lens_links` before you decide what the new table points at or replaces. A new reader names itself in the migration header (CLAUDE.md section 8).

## 6. Verification

**Red before, green after.** Before: the identity-to-need query is empty for every identity. After, on a scratch copy loaded with a handful of seeded rows: one identity returns its needs and ICF codes; one need and one code return their identities; a retired row falls out; a row marked not applicable is distinguishable from an absent one. The reproducibility rebuild (`migrate_db.py --rebuild`) exits 0, and the gate once: `scripts/preflight.sh --explain`.

## 7. Commit

`{skill}: {action} [YYYY-MM-DD HH:MM]` per rule 1; no research rows in this pull request.

## 8. What you must NOT do

- Write any triple (that is the research pull request after this merges, reviewed by the owner).
- Change `_lens_clause`, the engine or the determination key.
- Delete `access_needs.absorbs` or any row of the two flat maps in this task.
- Hand-write SQL against a table the CLI can reach; add a check that reads only itself; write the table without naming what reads it.

## 9. Stop conditions

Stop and report when: a question of section 4 is unanswered; the ledger and `MAPPING-DESIGN.md` still disagree after the ruling's supersession is read; the sibling table's shape has changed since this file was written; or the rebuild does not reproduce the database.

## 10. Rollback

Before the migration lands: delete the branch. After: a schema migration is immutable; correct forward.

## 11. Adversarial pass and pull request

Once, by `/adversarial`, before the pull request; open it last, then `unsubscribe_pr_activity` immediately (rule 9).
