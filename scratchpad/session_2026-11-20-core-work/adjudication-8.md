# Delegated adjudication of eight open decisions, 2026-11-20

_Opus-class, read-only except this file. Not the owner's words. Under the delegation of 2026-11-12 (`grep -n -F "I guess opus can do it" references/project-standards.md`), conditions (a) to (e); DG-NON list `sed -n '/### 2.4/,/^---/p' governance/decision-protocol.md`. Every resolution stands until the owner reverses it and is not relied on until an independent critic checks it. DB read at `PRAGMA user_version` 164, HEAD `1ac3054`. Re-run every command; do not trust a figure here._

Owner steering applied to every item (`grep -n -F "as simple as possible in infrastructure" references/project-standards.md`): rungs tried in order (nothing, convention, reuse, delete, smallest code); no new table, verb or check except T-145's table, which the owner ordered.

---

## 1. T-145 Q1 — must a row of the judged crosswalk hold all three keys, or at least two?

- **STATUS:** RESOLVED UNDER DELEGATION.
- **Rulings:** "a big 3D matrix of ICF codes * access needs * disability identities" and "yes, correct" to "a table of the triples someone judged" (`grep -n -F "big 3D matrix of ICF codes" references/project-standards.md`; `grep -n -F "each with a warrant" references/project-standards.md`). "An identity with no ICF code … is a gap to close and not a state to leave" (`grep -n -F "an identity with no ICF code" references/project-standards.md`). D-0182 (`grep -n "D-0182 (owner ruling 2026-09-01)" references/project-standards.md`) relaxes the lens of a *determination* to at least one; it governs a different object and does not bind here.
- **Resolution:** all three keys, each NOT NULL with a real FK. A cell of a cube has three coordinates; the identity–need, identity–ICF and need–ICF faces are projections the view `v_lens_crosswalk` computes, not stored rows. Knowledge of only two coordinates is a `gaps` row: `gaps` already carries `identity_code`, `icf_code` and `needs_code` (`python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[1] for r in c.execute('pragma table_info(gaps)')])"`).
- **Why not at least two:** nullable keys need a COALESCE CHECK and break `UNIQUE` (SQLite treats NULLs as distinct, so duplicates land): two exceptions the owner's simplicity rule forbids. The 11 identities with no ICF code are the owner's named gap, not a reason to store partial cells.
- **Mechanism:** rung 2 (convention) inside the schema T-145 already must ship; it removes a CHECK rather than adding one. Read by: the view and the review verb T-145 names.
- **Would reverse it:** the owner saying the faces themselves must be stored, or a judged pair that no ICF code (b, s, d or e) can express.
- **CHECK:** pending.

## 2. T-145 Q2 — who marks a row stated? (confirmation only)

- **STATUS:** ALREADY ANSWERED by the owner: only the owner's batch review marks a row stated (`grep -n -F '"yes, correct"' references/project-standards.md`, which answered "does a session propose the triples and you review each batch before it counts as stated?"). Not re-decided. The reading that "yes, correct" covers the whole description is the recorder's [ASSUMPTION] in that entry, still unratified.
- **CHECK:** pending.

## 3. T-145 Q3 — `access_needs.absorbs` and the rows of `identity_icf_map` and `access_need_icf`: proposals now, or folded in?

- **STATUS:** RESOLVED UNDER DELEGATION.
- **Rulings:** "the maps propose" (`grep -n -F "the maps propose" references/project-standards.md`); one value per cell (`grep -n -F "the minimum code that is correct, one value per cell" references/project-standards.md`); point, do not copy (CLAUDE.md rule 5).
- **Resolution:** do nothing now. The map rows stay as proposals, read by the session that drafts the first triple batch and by T-126's writer (the reader of `absorbs`: `git grep -n "absorbs" -- scripts/db.py`). Folding them in would copy unreviewed proposals into a table whose rows count only after the owner's review: a second home that presents unjudged rows as judged. `absorbs` is retired later, once triples cover every need. That is a schema migration placed after every data migration that INSERTs it (`git grep -l absorbs -- 'scripts/migrations/data_*'`), with T-126's reader swept first (rule 4).
- **Mechanism:** rung 1 (do nothing). Rung 4 (delete the cause) for `absorbs` later; nothing is added.
- **Would reverse it:** the owner ruling that the maps are already judged facts, or T-126 being rewritten to read the triple table, at which point the maps may become deletable.
- **CHECK:** pending.

## 4. T-145 Q4 — does a not_applicable row need a warrant?

- **STATUS:** ALREADY ANSWERED by the confirmed description: "a table of the triples someone judged, each with a warrant", where "a not_applicable row [reads] as judged and not applying" (`grep -n -F "each with a warrant" references/project-standards.md`). A not_applicable row is a judged triple, so it carries the same warrant cell. This rests on the same [ASSUMPTION] as Q2.
- **Mechanism:** the warrant column is NOT NULL for every state, with no state exception. This is one CHECK fewer than a conditional one. Precedent: `specifications.not_applicable_rationale`.
- **Would reverse it:** the owner saying an unexplained "does not apply" is acceptable.
- **CHECK:** pending.

## 5. GAP-368 — English renderings in `claimed_value` and `claimed_unit` of non-English figures

- **STATUS:** RESOLVED UNDER DELEGATION.
- **Rulings:** "An English rendering is not written into `claimed_value` or `claimed_unit`" (`grep -n -F "An English rendering is not written into" references/project-standards.md`; CLAUDE.md never-wrong item 2). Retire in place (`grep -n -F '"retire in place then"' references/project-standards.md`). A changed qualitative value is a second row (D-0168; `grep -n "a changed qualitative value is a second row" scripts/db.py`). Migrations are append-only.
- **Facts:** 10 qualitative rows (20 21 27 31 32 93 102 104 106 112) hold English paraphrases, and row 80 holds the words `viisi prosenttia` as its value. Every one has a current translation of its `claim_text`. Rows 20 to 32 sit only in RETIRED specifications 3 to 8, so `retire-extraction`'s live-determination refusal does not block them. Derive with: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select l.extraction_id,s.specification_id,s.retired_at from specification_extraction_links l join specifications s using(specification_id) where l.extraction_id in (20,21,27,31,32)').fetchall())"`.
- **Resolution (where each part goes):**
  - The original wording stays in `claim_text`.
  - The English stays in `translations` (it is already there).
  - A qualitative figure's `claimed_value` holds the source's own words, a literal span of its `claim_text`, in the source's language. That satisfies the NOT NULL CHECK with no schema change.
  - The unit cell holds only the unit spelling. The English conditions are dropped, because they already live in `claim_text` and its translation.
- **Mechanism:** rung 2 (one ledger convention) plus rung 3 (existing verbs only):
  - `retire-extraction` then `add-extraction` for the 11 rows. Row 80 is re-added as numeral `5` with `--value-as-written "viisi prosenttia"`.
  - `amend-extraction --field claimed_unit` (the OD-41 "leads the cell" rule) on the numerical rows whose unit cell carries words after the unit.
  - No new verb, column or CHECK.
- **Would reverse it:** the owner ruling that a qualitative figure's value is a judged English summary rather than a rendering.
- **CHECK:** pending.

## 6. GAP-371 — REF-00994's title is composed from a file name

- **STATUS:** RESOLVED UNDER DELEGATION.
- **Rulings:** "Fetch before you write any author, title or figure" (`grep -n -F "Fetch before you write any author" CLAUDE.md`); CLAUDE.md §5(c).
- **Facts (viewed):**
  - The cover render `retrieval-log/session_2026-11-20-core-work/b1e81d4770d19d9b.p0000.png` reads "ACCESSIBILITY GUIDE / OCTOBER 2020 / INTERNATIONAL PARALYMPIC COMMITTEE".
  - The logged full text carries the running head "IPC Accessibility Guide".
  - "edition" occurs nowhere in the text (`grep -c -i edition retrieval-log/session_2026-11-20-core-work/b1e81d4770d19d9b-full-text.txt` prints 0).
- **Resolution:** the composed title may not stand. "4th edition" is read from a URL, not from the work. Correct it to the title-page title, `Accessibility Guide`; the date and the corporate author are already held.
- **Correction path:** the smallest code (rung 5). `correct-source --field pub_title` accepts a value that `_verbatim(value, ref_id)` finds in the source's persisted artefacts (a text extraction or a logged page transcription, a convention already in use, e.g. `5dd866a236fb5978.p0001-transcription.txt`), and ledgers the artefact's path. It reuses the occurs-in-bytes test that `claim_text` already passes. No new verb.
  - Read by: `correct-source`, then `author_fidelity`.
  - What reaches the book without it: a title no fetched page states.
- **Would reverse it:** a fetched IPC page that titles this file "4th edition".
- **CHECK:** pending.

## 7. GAP-373 — non-English text outside titles and `claim_text` is not owed a translation

- **STATUS:** RESOLVED UNDER DELEGATION.
- **Rulings:** "i only know english, so the base has to record all the translation work for me" and "so that it can be properly evaluated in context" (`grep -n -F "i only know english" references/project-standards.md`). R11 forbids translating a harvested surface form (`observed_terms` DDL).
- **Resolution, by the test "is it the source's own words?":**
  - **Owed:** `source_section` (headings, which give the context judgment reads), `extraction_relations.quote`, `observed_terms.context_quote`, and a corporate author's name as written. The English held inside a corporate-name cell today (e.g. `内閣（Cabinet of Japan）`) is a joined cell (2026-11-06): it moves to `translations`, and the cell is corrected through §6's path.
  - **Not owed:** `loc_*` (addresses for finding the clause, which a translation would make a second home); `observed_terms.surface_form` (R11: its English is the adjudicated term); Korean inside `claimed_unit` (deleted by §5's cleanup, not translated).
- **Mechanism (data, not a column list):**
  - `_translations_owed` takes its owed (table, column) pairs from the `translations` table itself: the distinct pairs that already hold a row. One `request-translation` (an existing verb) on one cell opens a column for every non-English row. This replaces the hard-coded UNION.
  - `_cell_language` follows one FK hop to a table carrying `ref_id`, derived from `PRAGMA foreign_key_list`. Without it, `extraction_relations` (no `ref_id`) resolves to no language.
  - Rung 5. Read by: `translations --owed` and the judgment stage.
- **[GAP]:** whether `dbcore.single_key` resolves `evidence_source_authors` (composite key?), and whether `correct-source` covers `corporate_name`, were not verified.
- **Would reverse it:** the owner asking for clause addresses in English.
- **CHECK:** pending.

## 8. GAP-374 — any HTTP 2xx satisfies "VERIFIED needs a retrieval"

- **STATUS:** RESOLVED UNDER DELEGATION.
- **Facts:**
  - The e-Gov shell `d984761fd993755a.html` is 800 bytes, logged identically for two different laws.
  - The API XML for REF-00990 contains its title stem 6 times; the shell contains it 0 times (`grep -c "高齢者、障害者等の移動等の円滑化の促進に関する法律施行令" retrieval-log/session_2026-11-20-core-work/{a4390f9b6c346623.xml,d984761fd993755a.html}`).
  - REF-00990 and REF-00991 are both also backed by real XML retrievals, so their VERIFIED standing is correct today.
- **Resolution:** a retrieval holds the source's text when the source's stored title occurs in its logged bytes. That is the test `verify_corpus` already applies (`_row_haystacks` plus `_presence_missing`, `grep -n "def _presence_missing" scripts/research/retrieval_log.py`). No byte floor and no new exception.
- **Mechanism:** rung 3 (reuse). `_refuse_unlogged_verified` (`grep -n "def _refuse_unlogged_verified" scripts/db.py`) calls that same presence test. It is the same test §6 uses: one home. `_failure_reason` stays a transport test.
- **[GAP]:** whether the full stored title, including its 「（平成十八年政令第三百七十九号）」 tail, passes `_presence_missing`'s normalisation was not run.
- **Would reverse it:** a source whose own text does not state its title (a statute cited by number only). Its locator would then be the test instead.
- **CHECK:** pending.

## 9. GAP-376 — duplicate sources, each translated twice

- **STATUS:** RESOLVED UNDER DELEGATION: keep both rows, do not merge.
- **Facts (derived):**

  | Pair | Mirror retrieval (sha256) | Official retrieval (sha256) | Mirror figures | Official figures |
  |---|---|---|---|---|
  | REF-01026 / REF-01032 | ordemdosarquitectos.org `5744dca7…` | files.dre.pt `5b800bfb…` | 95 96 97 | 109 110 111 |
  | REF-01019 / REF-01031 | nepla.ai `7952f862…` | law.go.kr `b71c64f1…` | 82 83 | 107 108 |

  - Neither pair has a DOI.
  - REF-01019 is already `superseded_by_ref_id = REF-01031`. REF-01026 is not superseded.
  - All mirror figures are re-rooted (`root_ref_id`) to the official source.
  - Edges among the mirror figures: 83→82 and 97→96 (`condition_on`).
- **Resolution:** two different retrievals are two records of what was fetched. A merge would delete or repoint a `ref_id` and figures, against retire-in-place and the identifier floor.
  - `supersede-source --ref-id REF-01026 --by REF-01032`, following the REF-01019 precedent.
  - `retire-extraction` on 83 and 97, then 82, 96 and 95 (the order follows the edges), so one clause is one live figure (rule 5).
  - The double translations are sunk cost; retired figures are not owed.
- **Mechanism:** rung 3, existing verbs only. Convention line: a mirror found beside its official text is superseded at admission.
- **[GAP]:** whether `v_live_lens_links` and render drop a retired figure's lens links was not verified.
- **Would reverse it:** the mirror and the official text differing in a clause the figures read.
- **CHECK:** pending.

---

## Interactions

1. **GAP-376 before GAP-368.** Rows 82, 83 and 95 to 97 carry English conditions in `claimed_unit`. Retire them, do not clean them.
2. **GAP-368's retire and re-add mints new `extraction_id`s, so their `claim_text` translations are owed again for identical text.** `translations` is keyed by row and checked by sha256. No rule lets a reviewed translation of an identical sha256 be carried to the new row. [GAP]: decide this before the batch, or pay 11 re-translations and reviews. The same rows also need their lens links (`add-extraction` requires them) and the edges from 20 and 21 re-added.
3. **GAP-371 and GAP-374 share one test (the stored text occurs in logged bytes).** Build it once, in one tooling commit. Correcting REF-00994 removes the red that `author_fidelity` shows on main; whether it is then green is a [GAP] (not run). Only once it is green is promoting it from advisory to blocking (a registry `level:` edit, no new check) a real gate for GAP-374.
4. **GAP-373 depends on GAP-368** (the Korean in `claimed_unit` is deleted, not translated) **and on GAP-371** (the corporate-name cells are corrected through the widened `correct-source`).
5. **The translations contract default (`translation: default_stage: judgment`, `sed -n '/^translation:/,+1p' governance/pipeline-contract.yaml`) is circular for `extraction_relations.quote`.** Relations are written at judgment, so that cell cannot be translated before judgment reads it. Read "due at judgment" as "before the judgment that reads it", or leave the relation quote due at synthesis. [GAP]: not decided here.
6. **T-137 (units as data, unmerged).** `git log --oneline | grep -c -F "T-137"` prints 0. Its matcher reads `claimed_unit` against `base_units` spellings, and §5's unit cleanup is that matcher's data precondition. If T-137 lands first, re-check that `amend-extraction`'s OD-41 "leads the cell" rule still holds under it.
7. **T-126 to T-128.** Q3 leaves T-126's proposals (maps plus `absorbs`) unchanged. T-128 (held on OD-67) adds `identity_icf_map` proposals. Under Q1 (all three keys), the triples for the 11 identities with no ICF code wait on those proposals, and until then each is a `gaps` row. Retiring `absorbs` later must sweep T-126's reader first.
8. **Rule 10 and the PR shape.** "one big pull request … the matrix can be on its own" (`grep -n -F "the matrix can be on its own" references/project-standards.md`). GAP-368, 371, 373, 374 and 376 go in the big PR, with tooling commits first. T-145 is its own PR. Its triples are a later research PR the owner reviews.

## Minimum work to close all resolved items, in order

1. **Ledger:** one entry recording these resolutions, pending the critic. It includes two convention lines: a qualitative `claimed_value` holds the source's own words; a mirror is superseded at admission.
2. **Big PR, tooling commit A (no schema):** one "stored text occurs in logged bytes" test, read by `_refuse_unlogged_verified` (GAP-374) and by `correct-source --field pub_title` and `corporate_name` (GAP-371).
3. **Big PR, tooling commit B (no schema):** `_translations_owed` takes its pairs from `translations`; `_cell_language` follows one FK hop (GAP-373). It replaces the hard-coded UNION.
4. **Big PR, data commit, in this order (existing verbs only):**
   1. GAP-376: supersede, then retire.
   2. GAP-368: retire and re-add 11 figures, then amend the unit cells.
   3. GAP-371: correct the title.
   4. GAP-373: seed one `request-translation` per newly owed column, then translate.
   5. `close-gap` each, with its resolution pointer.
5. **T-145 own PR — THE ONLY SCHEMA MIGRATION (tooling-first commit):** a new table with three NOT NULL FK keys, a warrant NOT NULL in every state, a review verb that alone sets `stated`, and `v_lens_crosswalk`. The triples follow as a separate research PR for the owner's review.
