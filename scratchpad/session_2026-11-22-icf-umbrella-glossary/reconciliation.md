# Reconciliation: ICF umbrellas, the three base lenses, and identity–need pairs before ICF codes

Written 2026-11-23 by the Opus-class reconciler at the owner's words: "Okay. Opus to reconcile, make rulings as required and allow us to keep moving forward in project" (typed 2026-11-23 00:35 UTC; `git grep -n -F "Opus to reconcile" -- transcripts/harness_c6286d2b`). Read-only: no row, migration or tracked file was changed. Every figure below is followed by the command that produces it, or was derived on 2026-11-23 from `data/guidebook.db` opened `mode=ro` (schema `PRAGMA user_version` = 166). Re-run the commands; do not trust the figures.

**Standing.** Nothing here is the owner's words. Every R-row is a **delegated resolution** under the 2026-11-23 delegation, DG-REVIEW unless marked otherwise. Each is to be read through the gate of "Convention 2026-11-12" (`references/project-standards.md:5724`) after the independent check: `CHECK: pending` until then. DG-NON matters are not ruled. They are the five questions in section 2.

**The owner's words this reconciliation answers** (typed, session `session_2026-11-22-icf-umbrella-glossary`, preserved in `transcripts/harness_c6286d2b/main.jsonl`; times UTC on 2026-11-22):

- S1 (04:02): "the ICF codes used are not what I was expecting. I had been expecting ICF codes like b210, b230, b265, b280 etc.. but then we have entire groups like b750 to b789 which are all under "Movement functions" … so perhaps for ICF I really want those classification umbrellas like "Movement functions" , "Pain", "Hearing and vestibular systems" etc and some kind of glossary that shows all the codes bundled under those classification umbrellas"
- S2 (04:03): "gather all ICF, access needs, disability identities/populations in base"
- S3 (04:04): "I don't think the mapping is correct"
- S4 (04:04): "https://icd.who.int/browse/2026-01/icf/en"
- S5 (04:09): "our project filters specifications based on three approaches, and the browsing user chooses one of those approaches to use for browsing / ICF codes/classifications (e.g. Neuromusculoskeletal and movement-related functions, Movement functions b750-789) / Access needs (e.g. wheelchair access) / Disability identity (e.g. wheelchair user)"
- S6 (04:11): "So we should have a list of access needs, we should have a list of disability identities, and we should be able to map them to one another / and from there, perhaps, we select ICF codes that pertain to those relationships"

---

## 1. Rulings

Reversal cost is stated twice: **before** the tooling pull request merges (delete the branch; zero), and **after** (what undoing costs then). "Unblocks" names the work that cannot proceed without the ruling.

| # | Question | Ruling | DG | Basis | Reversal cost (after merge) | Unblocks |
|---|---|---|---|---|---|---|
| **R1** | May an identity–need pair be recorded before any ICF code is chosen for it? Does S6 supersede "all three keys NOT NULL"? | **Yes, a pair may be recorded on its own.** S6 supersedes, on contact (rule 0), **two things only**: (a) the sentence in `scripts/migrations/165_identity_need_icf.sql:13` that "what is known of only two is a `gaps` row … not a stored row"; (b) the reading at `references/project-standards.md:8252` *in so far as* it made the triple table the only home of an identity–need link. **It does not supersede "should be all three"** for a row that carries an ICF code. Such a row still names an identity, a need and a code, each present. What changes is that its identity and need become a pointer to a recorded pair, not a free-standing copy. [ASSUMPTION, unratified: "we should be able to map them to one another" means the identity–need link is a fact recorded and reviewed in its own right, and "and from there … we select ICF codes" means the code is chosen for a pair that already exists. Basis: the order of S6's two sentences.] | D-SCHEMA, DG-REVIEW. The reading of the owner's words is subject to the check. | S6. `references/project-standards.md:8246` ("T-145: should be all three") and `:8260` ACTION (1). `CLAUDE.md:77` (rule 0). | One compensating schema migration that folds the pairs back into the triple table. No data is lost, because the triples keep their three codes (R2). | R2–R4 and the owner's pair review (Q1). Pairing the 5 needs and 6 identities that have none is possible without inventing an ICF code. |
| **R2** | What is the minimal pairs schema (reuse first, point don't copy, one value per cell)? What becomes of `identity_need_icf`? | **One new table, `identity_need`.** Its columns: `pair_id` INTEGER PRIMARY KEY AUTOINCREMENT, `identity_code` and `need_code` (NOT NULL, real FKs), and `UNIQUE (identity_code, need_code)` over **all** rows (not a partial index, so it can be an FK parent). The cell-state, warrant, review and retire columns are copied from migration 166: `state`, `warrant`, `review_ref` LIKE 'Owner%', `reviewed_at`, `reviewed_session`, `review_note`, the four retirement cells with `retirement_ref` LIKE 'Owner%', and the same CHECKs. 166's no-edit trigger is copied too. **`identity_need_icf` stays** as the code-bearing row. It gains a composite `FOREIGN KEY (identity_code, need_code) REFERENCES identity_need(identity_code, need_code)`, so its two key columns become the pointer (as a shared `ref_id` is) and not a copy. Its `icf_code` stays NOT NULL. **Reuse the verbs**: `propose-identity-need-icf` with no `--icf-code` proposes a pair, and with one it proposes a code for a **live** pair (it refuses if the pair is missing or retired). `review-identity-need-icf` accepts `PAIR-<id>` tokens beside `TRIPLE-<id>`. `v_lens_crosswalk` is extended so that a pair with no code is visible, and the need's own `access_need_icf` codes are reached through the pair by a join, never stored. | D-SCHEMA, DG-REVIEW | Rule 5 (`CLAUDE.md:110`): "Point, do not copy". 2026-11-06 schema-shape ACTION (2) (`references/project-standards.md:4972`). 2026-11-21 (sixth) ACTION (1) (`:8374`): a need-side environmental row *counts* as the identity's coverage, and counting through a join meets that. CLAUDE.md §8: reuse before adding. | A compensating migration that drops `identity_need` and the composite FK. The triples are untouched. | Q1 and Q4 can be executed. Pairs can be browsed from either lens without any ICF code (S5, S6). |
| **R3** | How do the existing 64 live triples meet the new FK? | **The schema migration that adds the FK seeds `identity_need` mechanically** with the distinct live (identity, need) pairs of `identity_need_icf`, all `pending`, each with a warrant that reads "carried from TRIPLE-<ids> by migration NNN; no new judgment". `identity_need_icf` is rebuilt to add the FK. Every `triple_id` (TRIPLE-64 is cited in the ledger), every state and review cell, and `sqlite_sequence` are kept. **Nothing is retired or deleted by the migration.** It carries an `-- AFTER_DATA:` line no earlier than the newest `data_*.sql` that INSERTs into `identity_need_icf` (`grep -l 'identity_need_icf' scripts/migrations/data_*.sql \| sort \| tail -1`), because it rebuilds a table those migrations write (rule 5's AFTER_DATA clause). This is a structural carry of committed rows, not research content, so it is not a rule-10 breach. | D-SCHEMA, DG-REVIEW | `CLAUDE.md:110` (AFTER_DATA). `scripts/migrations/166_identity_need_icf_owner_review.sql` (drop-and-recreate precedent, on an empty table). Rule 3 (fix forward). | A compensating migration. The seeded pairs are `pending` and carry no owner review, so nothing judged is lost. | The rebuild reproduces the database (`migrate_db.py --rebuild`). |
| **R4** | In what order are the two halves reviewed? | **A triple may be marked `stated` or `provisional` only when its pair is `stated` or `provisional`.** This is a refusal in `review-identity-need-icf`, not a CHECK, because SQLite cannot check across tables. A pair is reviewed first or in the same owner entry, which may name both `PAIR-` and `TRIPLE-` tokens. TRIPLE-64 already stands `stated` while its pair will be `pending`. That is the one known exception. It is closed by the owner's answer to Q1, and until then the verb's `--uncovered` output reports it. | D-METH (applying an existing method), DG-REVIEW | S6's order. The 2026-11-20 (second) entry: the owner reviews batches (`:8171`). | Delete the refusal (a few lines). | No ICF code is ever stated on a pair the owner has not accepted. That is the TRIPLE-65 failure ("the pair is an inference no record states", `:8377` entry). |
| **R5** | Does `base_icf` get a parent pointer and block rows, and how is a block identified? | **Yes.** `base_icf.parent_code TEXT REFERENCES base_icf(icf_code)`, nullable. **A block is a row** whose `icf_code` is its span `<first 3-digit code>–<last 3-digit code>`, with an en dash as in the stored ranges (`d310–d329`). It fits the existing CHECK `icf_code GLOB '[bdes][0-9][0-9][0-9]*'`, and `add-icf-code` already derives `is_range`. **The span is derived from the WHO payload, not copied from it**: the tabulation carries no range strings (`grep -c 'b750-b789' …/SimpleTabulation-ICF-en.txt` → 0). Its identifiers are `BlockId` (`BlockL3-b75`) and the Foundation URI. The span is the minimum and maximum of the 3-digit categories under the block. **Levels:** WHO's L2 and L3 blocks become rows. L1 ("Body functions" and the others) is **not** a row, because `component` already holds it. A category's parent is its WHO parent, which is a block for a 3-digit code and a category for deeper ones (e1251 → e125). **No `who_block_id` column**: nothing would read it. The title source `payload:retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip` pins the release. [ASSUMPTION, unratified: S5's two-level example ("Neuromusculoskeletal and movement-related functions, Movement functions b750-789") asks for both L2 and L3. Basis: the words.] | D-SCHEMA, DG-REVIEW | S1, S5. WHO payload (verified: `BlockL3-b75` spans b750–b789 with 8 categories; `BlockL2-b71` spans b710–b799). `references/project-standards.md:3530` ("The ICF lens is `base_icf`"). Rule 8: derive, do not curate. | A compensating migration drops the column. Block rows that nothing references can be deleted forward. | R7, R9 and R10. The owner's umbrellas exist as base rows. |
| **R6** | What about stored ranges that are not WHO blocks? | **`d910–d920` is not a WHO block.** WHO's block is `BlockL2-d91` "Community, social and civic life", which spans **d910–d999** (verified from the payload). The other three stored ranges equal WHO L3 spans: d310–d329 = `BlockL3-d31`, d330–d349 = `BlockL3-d33`, d710–d729 = `BlockL3-d71`. They become those block rows by taking a title and a parent, with no new row. `d910–d920` keeps its row, because 2 `identity_icf_map` rows reference it (`select count(*) from identity_icf_map where icf_code='d910–d920'`). It gets **no parent and no title**, it is **not an umbrella**, and nothing new references it. It is a joined cell (two categories in one code, 2026-11-06), and it dies with `identity_icf_map` if Q2 is answered yes. **"Is a WHO block" is derived and needs no column**: `is_range = 1 AND title_source LIKE 'payload:%'`. | D-SCHEMA, DG-REVIEW | WHO payload. `references/project-standards.md:4972` (one value per cell). Rule 8. | None. Nothing is written for d910–d920. | The glossary does not present a coined grouping as WHO's. |
| **R7** | How much of ICF does base hold, and by what writer? | **Every L2 and L3 block, and every 3-digit category, with WHO's titles from the persisted payload.** Deeper codes are minted when used, as now. The **writer is one verb that derives everything from the payload** (name for the task, e.g. `import-icf-tree --payload <zip>`). It reads the persisted zip through the existing `_payload_bodies`, computes spans, parents and titles, inserts absent rows, sets `parent_code` and a NULL `title` on held rows, and **refuses and lists** held rows whose non-null title differs from WHO (R8 handles those). It is not 400+ hand-typed `add-icf-code --parent` calls, which would be curation by hand (rule 8). Counts (re-derive): 67 L2/L3 blocks, 373 3-digit categories, 3 of the blocks already held as ranges. All 68 held single codes exist in WHO 2026-01. [ASSUMPTION, unratified: "gather all ICF … in base" (S2) and "a glossary that shows all the codes bundled under those classification umbrellas" (S1) mean the classification's codes under each umbrella, not only the ones the project has used. The 3-digit grain is the one S1's examples use (b210, b230, b265, b280).] | D-SCHEMA, DG-REVIEW | S1, S2. `references/project-standards.md:3530` ACTION (4) ("`GAP-ICF-TITLES` closes by retrieval and persisted bytes, never by recall"). CLAUDE.md §5(c). | Unreferenced base rows can be deleted by a compensating migration. Once a lens row points at one, it stays. | GAP-ICF-TITLES closes. A browsing reader can see b265 and every other code the owner expected. |
| **R8** | What about stored titles that differ from WHO's? | **They are corrected to WHO's wording from the payload.** `set-icf-title` refuses to overwrite today, so it gains one path: a `--title-payload`-verified title **replaces a title whose source is not a payload**, and the verb prints the old title and its source. The old and new values go in the data migration's header (owner, 2026-11-21: "make transparent and record your hand fixes", `:8263` entry). A payload-sourced title is still never overwritten. The rows that differ: **10** in all, compared case-insensitively with the payload. Nine of the 12 titles whose source is `access_need_icf.note` differ: b164, b765, e115, e120, e125, e1251, e150, e155 and e340. Each is a need's note pasted into the title, and two of them (b164, b765) carry a rationale and an exclusion clause, which is two facts in one cell. The other three (e240, e250, e260) match WHO. The tenth is d620 ("Acquisition of goods/services", from a skill file), which differs from WHO's "Acquisition of goods and services". Re-derive with a comparison of `select icf_code,title from base_icf where title is not null` against the payload. The notes are already held in `access_need_icf.notes`, so no fact is lost. | D-SCHEMA, DG-REVIEW | CLAUDE.md §5(c) and the "fetch before you write" rule. 2026-11-06 ACTION (2). `scripts/db.py` `set_icf_title` docstring ("A correction is a different act and owes its own reason"). | Revert the verb path. Corrected titles are restored by migration from the recorded old values. | Codes and **names** (CLAUDE.md §6). The glossary shows WHO's titles. |
| **R9** | Should a cell keyed on an umbrella gather its descendants? What is the smallest generalisation? Does the need lens need a hierarchy? | **Yes, by parity with the identity lens. The helper is generalised, not copied.** In `scripts/dbcore.py`, `IDENTITY_FAMILY_SQL` and `identity_family()` become one per-lens family map (identity: `base_taxonomy_identity.parent_code`; ICF: `base_icf.parent_code`) and one `lens_family(conn, col, code)`. `lens_differs(row, lens, families)` reads a family per lens and falls back to equality where a lens has no hierarchy. **The call sites, counted: six places in four files.** `assess_cell._lens_clause` (`scripts/assess/assess_cell.py:263`). The gate filter in `assess_cell` (`:703–712`). `db.py cell-status` (`:1296`, `:1346`, `:1385`, `:1414`). `dbcore.lens_differs`. `scripts/audit/derivation_handshake_integrity.py:159`. **The need lens gets no parent pointer.** Its browsing grouping is the existing `access_needs.family` column, a five-value CHECK vocabulary that is already a one-level umbrella. S5's need example is flat. | D-SCHEMA, DG-REVIEW | T-055 (`assess_cell.py:258` comment). CLAUDE.md §5(a): without it, a cell keyed on `b750–b789` gathers nothing from figures linked to b765 and reports empty. S5. | Revert the helper. It replaces code and adds nothing alongside it. | Umbrella-keyed cells and an umbrella browse filter read one helper. |
| **R10** | Where does the glossary live? | **A read verb, `db.py icf-glossary [--umbrella CODE]`.** For each L2 and L3 block it lists every code under it (through R9's helper), with WHO's titles and which lens or map rows reference each code. **No view, and no committed file**: render reads the database when rendered (CLAUDE.md §3 table, owner 2026-08-27). The scratch `icf-umbrellas.md` and `icf_glossary.py` are superseded when the verb lands. | D-PRES (first of its kind), DG-REVIEW | S1. CLAUDE.md §3 ("no committed file is one"). §8: name what reads it. Here the owner reads it, and so does `lens-crosswalk` for umbrella display. | Delete the verb. | S1's glossary comes from base, not from a scratch script. |
| **R11** | How does S5's three-way browse filter use the hierarchy and the crosswalk? | **Each approach filters specifications on the lens column the specification itself states, through that lens's family (R9). There is no crossing.** A specification keyed only on BLIND does not appear under "Seeing functions" because a pair links them. The pair and triple crosswalk is shown beside a result as navigation ("related needs and codes"). It supplies **proposals at recording** (T-126's model), never a read-time filter. This changes nothing ruled: D-0184 and `_lens_clause` ("never through a crossing map", `assess_cell.py:273`) stand. **No render surface exists today** (`ls scripts \| grep -i render` → nothing). This rule governs the first one; it builds nothing now. | D-METH (applying an existing method), DG-REVIEW | S5 ("the browsing user chooses one of those approaches"). D-0184. 2026-11-20: "the base needs to get that ready for me" (`:8130`). | None. Nothing is built. | A render task can be written without reopening D-0184. |
| **R12** | What is a legitimate basis for a body-function code on an identity, or on a pair? | **The persisted WHO payload grounds a code's existence, title and place in the hierarchy only. It states no relation between an identity or need and a code**: the simple tabulation has no definitions and no identity relations (`head -1 …/SimpleTabulation-ICF-en.txt`; its columns are URI, code, BlockId, title, kind, depth, residual flag, link, leaf flag, coding note, parent). A relation needs the owner's words, or a cited source in the evidence stage. **ACTION (2) of 2026-11-21 (third)** (`:8318`) lists "an owner statement, a recorded map row, or a payload fetched from WHO under T-128". It is **corrected**: the WHO-payload clause is read as the code and title only. The "recorded map row" clause depends on Q2. `identity_icf_map` holds no b rows, so it cannot be the basis of a b-code (`select count(*) from identity_icf_map where icf_code like 'b%'` → 0). This corrects recorder text, not owner words. The owner's words there ("b is seeing therefore ties into blind etc") are untouched. Whether a session may propose a code by inference for owner review is DG-NON. That is Q3. | D-METH, DG-REVIEW | The 2026-11-21 (third) ACTION (2). The 2026-11-21 review of TRIPLE-65 (`:8377` entry). CLAUDE.md §5(c). | Withdraw the correction (no data effect). | No session cites WHO's tabulation as the warrant for an identity's code. |
| **R13** | What happens to `identity_icf_map` and `access_need_icf` given S3? | **`identity_icf_map` is frozen** until Q2 is answered. No session copies its rows into `identity_need_icf` or `identity_need`, and no session cites one as a warrant. **T-128 is HELD** even though OD-67 is answered: it would add rows to the map S3 may condemn. **T-126 and T-127** keep the map as a printed proposal source until Q2, then are re-pointed to `v_lens_crosswalk`. **`access_need_icf` stands.** It is the need's own code list, recorded 2026-07-23 with `confirmed` confidence (`select need_code,icf_code,created_by_session from access_need_icf where icf_type<>'e'`), and nothing in S1–S6 names it. The 5 duplicate (identity, code) pairs in `identity_icf_map` (`select identity_code,icf_code,count(*) from identity_icf_map where retired_at is null group by 1,2 having count(*)>1`) differ only in their mechanism prose. The three COM ones come from the 2026-09-13 crosswalk that merged two retired auditor codes into COM (OFS and PCS; see the header of `data_20260913060346_…`). The origin of the two BLIND ones was not traced. They are not fixed, because the whole table awaits Q2. | D-OP (a hold), DG-REVIEW | S3. `references/project-standards.md:8012–8013` (OD-67). | Lift the hold. | Nothing new is built on a map the owner has said may be wrong. |
| **R14** | What becomes of `access_needs.absorbs`? | **It is untouched by both pull requests.** It mixes identity-like group names with conditions and situations (A-NOSPEECH absorbs "laryngitis, L2 users"; A-REACH absorbs "carrying a child"), so pairs cannot wholly replace it. It is retired only after pairs cover every need **and** the non-identity terms have a home. That home is a separate design, not decided here. Until then it is read only as prose that proposes a pair, under owner review. | D-SCHEMA, DG-REVIEW | T-145 Q3 recommendation (unratified, `:8254`). 2026-11-06 census list (`:4969`). | None. | Nothing. It is recorded so that no session retires `absorbs` early. |
| **R15** | The identity hierarchy the session called existing has no data. Can the owner's ruled edges be written? | **Add one writer path: `amend-identity --parent`.** It is bound to an owner ledger entry, as `amend-identity` already is, and refuses a cycle and a parent that is not active. The owner ruled "SCI and LMB go under MOB" (`:6097`; ACTION (1) at `:6107`: "Set `parent_code = MOB` for `SCI` and `LMB`"). That edge is **unexecuted**: 0 identities carry a parent (`select count(*) from base_taxonomy_identity where parent_code is not null`). **No verb can set a parent on an existing code**: `add-identity --parent` works only at mint (`scripts/db.py` `add_identity`). The edges are written in the research pull request, after the recorder confirms that OI-77 (whether SCI survives) does not bar a parent edge (`workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`, OI-77). | D-SCHEMA, DG-REVIEW | Owner answer 2026-11-12 (sixth set). Correction 2026-11-16 (`:7713`). | Remove the flag. A parent is undone by setting it to NULL through the same verb. | The identity family stops being a code path that has examined nothing (§5(a)). An owner ACTION can be executed. |
| **R16** | Sequencing (rule 10), and which pull requests. | **Tooling first, in one pull request: T-146 (pairs) + T-147 (ICF hierarchy, titles path, lens family, glossary, identity parent writer).** It merges to main before any row. **Then one research pull request: T-148.** The matrix stays separate from unrelated work, as the owner asked ("the matrix can be on its own", `:8235`). [ASSUMPTION, unratified: putting the ICF hierarchy tooling in the matrix's tooling pull request keeps "on its own", because the hierarchy is the matrix's third key. Basis: 2026-11-20 (fourth), "so i don't have to waste time".] | D-OP, DG-AUTO | `CLAUDE.md:212` (rule 10). `references/project-standards.md:8235`. | Split the pull request. | The work list in section 3. |

---

## 2. Questions for the owner (DG-NON only)

These are population-taxonomy and code-to-identity decisions, which `governance/decision-protocol.md:76` (§2.4 item 2) reserves to the owner. Each takes yes, no or a pick.

**Q1. Do you accept these 29 identity–need pairs?** Each pair says that this group of people has this access need. The pairs come from the rows you saw in pull request 245. Regenerate the list with `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select identity_code, group_concat(distinct need_code) from identity_need_icf where retired_at is null group by 1\").fetchall())"`.

| Identity | Needs |
|---|---|
| ADHD | A-LOWLOAD |
| AUT | A-CALM, A-STIMULUS |
| BAR | A-SIZE |
| BLIND | A-NOSIGHT |
| BRAIN | A-LOWLOAD, A-NOSPEECH, A-PLAIN, A-STABLE, A-STIMULUS |
| COM | A-EFFORT, A-LOWLOAD, A-TRIGGER (A-TRIGGER is the open part of GAP-379) |
| DEAF | A-NOSOUND |
| DEAFBLIND | A-TACTILE |
| DEM | A-LOWLOAD, A-PLAIN |
| EPI | A-TRIGGER |
| ID | A-LOWLOAD, A-PLAIN |
| LPA | A-SIZE |
| MH | A-CALM, A-STIMULUS |
| MS | A-EFFORT |
| NDV | A-CALM, A-LOWLOAD, A-STIMULUS |
| PAIN | A-EFFORT |
| TALL | A-SIZE |

Answer: **all**, or **all except** (name the pairs to reject).

**Q2. When you said "I don't think the mapping is correct", did you mean the 61-row list that links each identity to ICF *activity* codes?** For example, DEAF → d310–d329 and d330–d349, and BLIND → d310–d329, d460 and d620. That list came from an old skill's table and holds no body-function code. **Yes**: the list is retired and nothing is copied from it. **No**: say which mapping you meant.

**Q3. May a session propose a body-function code for a pair you have accepted, marked as its own inference, for you to accept or reject in a batch?** It would work from WHO's code title and the identity's own description. For example, it might ask whether DEAF with A-NOSOUND should carry b230, which WHO titles "Hearing functions". **Yes**, or **no**: then each code comes only from your words or from a cited study.

**Q4. Once pairs exist, 63 pending rows only repeat a need's own environmental code (e150, e240 and so on) for each identity.** They would still show through the need, and still count as the identity's coverage as you ruled on 2026-11-21. **Retire them? Yes or no.** (The table requires an owner entry to retire any row.)

**Q5. Your example identity, "wheelchair user", has no code of its own.** It sits inside MOB ("disabled people with mobility needs; wheelchair users"). Pick one:
- **(a)** give it its own code under MOB (the mobility split, already waiting on OD-14 and OI-77);
- **(b)** leave it inside MOB for now.

(Your need example, "wheelchair access", is read here as A-REACH, "Be physically reachable". That reading is unratified.)

---

## 3. Ordered work list

### 3.1 Tooling pull request (T-146 and T-147 together; no rows; merged first)

Each item names what reads it, and what wrong thing reaches the guidebook without it.

1. **T-146: schema migration `identity_need`** (R2), the composite FK and rebuild of `identity_need_icf`, and the mechanical pair seed (R3, with `-- AFTER_DATA:`). *Read by* `v_lens_crosswalk`, `lens-crosswalk` (including `--uncovered`), and the two verbs. *Without it*, pairing a need with an identity forces an invented ICF code. That pressure produced the 63 copies and TRIPLE-65.
2. **T-146: verb changes.** `propose-identity-need-icf` accepts no `--icf-code` (a pair), and with a code it refuses a missing or retired pair. `review-identity-need-icf` accepts `PAIR-<id>` and enforces R4's order. *Read by* the research pull request.
3. **T-146: `v_lens_crosswalk` extended.** It shows pairs with no code, and joins in the need's own `access_need_icf` codes as derived coverage. *Read by* `lens-crosswalk`, and later by the render stage.
4. **T-147: schema migration `base_icf.parent_code`** (R5). *Read by* R9's helper, the import verb and the glossary verb.
5. **T-147: the import verb** (R7). *Read by* the research pull request. *Without it*, a session hand-types 440 parents and titles.
6. **T-147: the `set-icf-title` replacement path** (R8). *Without it*, the 10 differing titles can never be corrected through the CLI.
7. **T-147: the lens-family generalisation** (R9), which replaces `IDENTITY_FAMILY_SQL` and `identity_family` and updates the six call sites. *Read by* the engine, `cell-status` and the handshake audit. Tests: the T-055 cases stay green. A new case puts a figure linked to b765 inside a cell keyed on `b750–b789`. It must fail on the unmodified helper.
8. **T-147: `db.py icf-glossary`** (R10). *Read by* the owner.
9. **T-147: `amend-identity --parent`** (R15). *Read by* the identity family.
10. **Prose callers** (rule 4, rule 7a): add a supersession pointer to T-145's header. Correct the header comment of `165_identity_need_icf.sql` by putting the account in the new migration's header, because 165 is immutable. Sweep `governance/conceptual-model.md` and `governance/functional-taxonomy.md` for "flat" or "no hierarchy" claims about the ICF lens (`grep -rn "base_icf" governance references architecture`). Then run `run_checks.py --selftest`, `migrate_db.py --rebuild`, `scripts/preflight.sh`, `joined_cells_census.py` before and after, and `derived_not_curated_audit.py`.

Measure: `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`.

### 3.2 Research pull request (T-148; after the tooling merges)

1. **Import the WHO tree**: the L2 and L3 blocks, the 3-digit categories, parents on held codes, and titles from `retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip`. *Read by* the glossary, the browse filter and the proposals. Closes GAP-ICF-TITLES.
2. **Correct the 10 differing titles** with old and new values in the migration header (R8).
3. **Record the owner's pair review** (Q1) under a ledger entry that names each `PAIR-<id>`. This includes BLIND–A-NOSIGHT, which closes R4's exception.
4. **If Q4 is yes**: retire the 63 copied environmental rows with that entry as `retirement_ref`. GAP-379's `e120` sub-question then dissolves (it asked whether e120 attaches through A-SIZE). Record that in the gap's resolution.
5. **If Q2 is yes**: retire every live `identity_icf_map` row, with S3's entry cited in `retired_reason`. Then lift R13's hold on T-126 and T-127, and re-point them to `v_lens_crosswalk`. T-128 is then superseded.
6. **If Q3 is yes**: propose body-function codes per accepted pair (`pending`, inference stated in the warrant, WHO title as the code's name only). The owner reviews them in the next batch.
7. **Propose pairs** for the needs with none (A-AT, A-PRECISION, A-REACH, A-SELFCARE, A-TIME) and the identities with none (ALL, LMB, MOB, MOVE, SCI, VES). Derive both lists with `lens-crosswalk --uncovered`. MOB, SCI and LMB stay withheld while OD-37, T-102 and OI-49 hold (pull request 245's withholding). ALL is a scope marker and takes no pair. COM–A-TIME is not re-proposed without a recorded basis (`:8377` ACTION (2)).
8. **Write the SCI → MOB and LMB → MOB parent edges** (R15), once the recorder has checked OI-77.

### 3.3 Tasks

- **Exist**: T-145 (built; needs the header pointer), T-055 (built), T-126 and T-127 (proposal source to re-point after Q2), T-128 (HELD by R13).
- **To author**: T-146 (pairs layer), T-147 (ICF hierarchy, titles path, lens family, glossary, identity parent writer), T-148 (the research pull request).
- **Not to author**: a render task. R11 governs it when one is written.

---

## 4. Defects and contradictions found, worst first

1. **"The identity lens already has a hierarchy" is true of the code and false of the data.** The session's message at 2026-11-22 04:10 and the coordinator's brief both say it. 0 of 23 identities carry `parent_code`. The owner's ACTION "Set `parent_code = MOB` for `SCI` and `LMB`" (`references/project-standards.md:6107`, 2026-11-12) was never executed, and no verb can execute it (R15). So every identity-family code path has examined only single-member families. The parity argument for R9 rests on code that has never gathered a child: a §5(a) shape.
2. **The basis list in 2026-11-21 (third) ACTION (2) (`:8318`) is empty for a body-function code.** "A recorded map row" cannot ground a b-code, because `identity_icf_map` holds none. "A payload fetched from WHO" cannot ground any identity relation, because the tabulation states none. As written, only the owner's own words could ever add a b-code. That is why Q3 is needed (R12).
3. **The provenance of `identity_icf_map` is misdescribed** in the session's message of 04:04 and in the coordinator's brief ("axis-layer-derived"). The header of `data_20260913060346_2026-09-13-derivation-handshake.sql` says the rows are the functional-deficit-auditor skill's table. "Via crosswalk" there means a crosswalk of retired *population* codes (UPL → LMB, OFS and PCS → COM), not of the axis layer. Nothing read shows the skill's d-codes came from the axis layer. The claim is unverified and probably wrong.
4. **63 of the 64 live triples copy a fact `access_need_icf` already holds** (identity × the need's own e-code). That is the dual home rule 5 forbids (`select count(*) from identity_need_icf t where retired_at is null and exists (select 1 from access_need_icf a where a.need_code=t.need_code and a.icf_code=t.icf_code)`). The all-three-keys shape forced it (R1–R2, Q4).
5. **The header of migration 165 (`:13`) states a rule S6 contradicts**: "what is known of only two is a `gaps` row". It is superseded (R1). The file is immutable, so the correction lives in the next migration's header and in the ledger.
6. **10 stored ICF titles differ from WHO 2026-01, and the CLI cannot correct them** (`set-icf-title` refuses to overwrite). Nine are need notes pasted into the title (source `access_need_icf.note`), and one is d620 from a skill file. The pasted notes carry rationale and exclusion clauses in two of them (b164, b765). That is a one-value-per-cell breach (R8).
7. **S5's own examples have no base row.** "Wheelchair user" is folded into MOB. "Wheelchair access" is not a need name (the nearest is A-REACH). The mobility split that would mint WHEEL is held on OD-14 (withdrawn and referred back) and OI-77 (Q5).
8. **T-128 is unblocked on paper and wrong to run.** OD-67 is answered (`:8013`), but it writes into `identity_icf_map`, which S3 may condemn (R13).
9. **The block spans the session presented as WHO's are derived.** "Movement functions (b750–b789)" and the others appear in no WHO byte of the payload. They are the minimum and maximum of the child codes. The figures are correct (re-derived here), but the provenance must be stated (R5).
10. **The scratch glossary misplaces stored ranges.** Section 1 of `icf-umbrellas.md` omits "General interpersonal interactions (d710–d729)", although a stored range is exactly that block and 5 identities use it. Section 3 shows it as holding "0" stored codes. Section 2 says `d910–d920` "spans … Community, social and civic life" without saying that it is not that block (WHO: d910–d999).
11. **The extracted WHO text (473 KB) is committed** under `scratchpad/…/who/`, beside the logged zip. CLAUDE.md §5(c) says extracted text is logged by where it came from, not committed. `icf_glossary.py` reads the copy, not the logged zip. Harmless now, because the two are identical, but it is a second home of the payload.
12. **The session said the lens helper has "five call sites"; there are six places in four files** (R9). `assess_cell` has two: `_lens_clause` and the gate filter.
13. **The 2026-09-13 statement reading** describes `base_icf` as "ICF **b**/**d**, the person's function" and `access_needs` as ICF **e** (`:3466` block). `base_icf` now holds 10 e-codes (`select count(*) from base_icf where component='e'`). This is prose drift; correct it when the prose is next touched.
14. **The `mechanism` cell of `identity_icf_map` joins a category prefix to a description** ("Sensory — partial vision, contrast, lighting dependency"). It is a joined cell. Moot if Q2 is answered yes.

One error of my own, withdrawn before writing: I first read the scratch umbrella list as missing "Skin and related structures (s810–s899)". It is there, as the file's last line, which has no trailing newline.

---

## 5. Draft ledger entries (not written to the ledger)

### 5.1 Owner statements

```
## Owner statements 2026-11-22 — ICF classification umbrellas and a glossary of the codes under each; the base gathers the three lenses; identities and needs are mapped to one another, then ICF codes chosen for each relationship

Given in the session `session_2026-11-22-icf-umbrella-glossary` ([session URL: the recorder fills it from the harness]), in typed messages, the first while the session oriented and the rest while it gathered the base and retrieved WHO's ICF release. Derive the times from the preserved transcript (`git grep -n -F "classification umbrellas like" -- transcripts`; `git grep -n -F "gather all ICF, access needs" -- transcripts`; `git grep -n -F "I don't think the mapping is correct" -- transcripts`; `git grep -n -F "filters specifications based on three approaches" -- transcripts`; `git grep -n -F "we should have a list of access needs" -- transcripts`).

**Owner's words, quoted (typed):**

> "the ICF codes used are not what I was expecting. I had been expecting ICF codes like b210, b230, b265, b280 etc.. but then we have entire groups like b750 to b789 which are all under "Movement functions""
>
> "so perhaps for ICF I really want those classification umbrellas like "Movement functions" , "Pain", "Hearing and vestibular systems" etc and some kind of glossary that shows all the codes bundled under those classification umbrellas"
>
> "gather all ICF, access needs, disability identities/populations in base"
>
> "I don't think the mapping is correct"
>
> "https://icd.who.int/browse/2026-01/icf/en"
>
> "our project filters specifications based on three approaches, and the browsing user chooses one of those approaches to use for browsing"
>
> "ICF codes/classifications (e.g. Neuromusculoskeletal and movement-related functions, Movement functions b750-789)"
> "Access needs (e.g. wheelchair access)"
> "Disability identity (e.g. wheelchair user)"
>
> "So we should have a list of access needs, we should have a list of disability identities, and we should be able to map them to one another"
>
> "and from there, perhaps, we select ICF codes that pertain to those relationships"

**Readings.**

- [ASSUMPTION: "classification umbrellas" are WHO's ICF blocks (for example Movement functions, BlockL3-b75, whose 3-digit categories run b750 to b789 in the 2026-01 tabulation), and the ICF lens browses through them as well as through single codes. Basis: the words, and the persisted WHO payload (`retrieval-log/session_2026-11-22-icf-umbrella-glossary/manifest.jsonl`). WHO's title is "Hearing and vestibular functions", and the base uses WHO's wording.]
- [ASSUMPTION: "a glossary that shows all the codes bundled under" each umbrella means the classification's codes under it, not only the codes the project has used, and "gather all ICF … in base" means the base holds them. Basis: the words. The grain (3-digit categories) is the one the owner's examples use.]
- [ASSUMPTION: "the mapping" is the identity-to-ICF-activity list (`identity_icf_map`). Basis: it was the mapping the session had just described. This is put to the owner as a question and is not acted on until answered.]
- [ASSUMPTION: the URL names WHO's ICF 2026-01 release as the source of codes, titles and hierarchy. Basis: the message. The browser page is a script shell, so the release file it links to was retrieved instead.]
- [ASSUMPTION: the three approaches are the three lens columns a specification states (`identity_code`, `icf_code`, `needs_code`), and a browsing reader filters by one of them. Basis: the words and the 2026-08-28 lens ruling. Nothing here changes D-0184: a specification is not pulled into another lens through the crosswalk.]
- [ASSUMPTION: "map them to one another" means an identity–need pair is recorded and reviewed as a fact in its own right, before and without an ICF code. "From there … we select ICF codes" means a code is chosen for a pair that exists. This supersedes, on contact (rule 0), the header sentence of `scripts/migrations/165_identity_need_icf.sql` ("What is known of only two is a `gaps` row … not a stored row"), and the entry "Owner statements 2026-11-20 (fifth)" in so far as it made the triple table the only home of an identity–need link. It does not supersede "should be all three" for a row that carries an ICF code. Basis: the order of the two sentences. "Perhaps" qualifies the selection of codes, not the mapping.]
- The owner's examples "wheelchair user" and "wheelchair access" name no row the base holds today. "Wheelchair user" is inside MOB, and the split is held on OD-14 and OI-77. Reading "wheelchair access" as A-REACH is an assumption and is unratified.

CONDITION: any session designing, writing or reading `base_icf`, `identity_need_icf`, `identity_icf_map`, `access_need_icf`, `access_needs` or `base_taxonomy_identity`; any session building a browse surface or the ICF glossary; T-126, T-127, T-128 and T-145.
ACTION: (1) Treat an identity–need pair as recordable before any ICF code, and treat a code as chosen for a pair. (2) Build the ICF umbrellas and the glossary from WHO's persisted 2026-01 payload, never from memory. (3) Do not copy from, cite or extend `identity_icf_map` until the owner says which mapping is not correct. (4) Treat every [ASSUMPTION] above as unratified except where the owner's words state it.
DATE: 2026-11-22 — owner statements (typed words, quoted above).
```

### 5.2 Delegated resolutions

The OD numbers are proposals. The highest in the ledger is OD-72 (`grep -ohE "OD-[0-9]+" references/project-standards.md | sort -t- -k2 -n -u | tail -1`). The recorder assigns the real ones in the register.

```
## Delegated resolution 2026-11-23 — identity–need pairs, the ICF umbrella hierarchy and the glossary (OD-73 to OD-79)

A resolution by an Opus-class model under the owner's instruction of 2026-11-23 ("Okay. Opus to reconcile, make rulings as required and allow us to keep moving forward in project"; `git grep -n -F "Opus to reconcile" -- transcripts`), applied to the owner statements of 2026-11-22 (entry above). **It is not the owner's words**, and it stands until the owner reverses it. Reasoning: `scratchpad/session_2026-11-22-icf-umbrella-glossary/reconciliation.md` (rulings R1 to R16). Population-taxonomy and code-to-identity matters were not resolved. They are the five owner questions of that file's section 2.

OD-73: the pairs layer (R1–R4). A table `identity_need` holds the judged identity–need pair, with the cell states, warrant, owner-bound review and retire-in-place cells of migration 166. `identity_need_icf` keeps all three codes NOT NULL and points at its pair by a composite foreign key. The schema migration seeds the pairs mechanically from the live triples as `pending` and retires nothing. A triple is stated only on a stated or provisional pair. The need's own environmental codes are reached through the pair by a join and are counted as the identity's coverage, as the owner ruled on 2026-11-21.
OD-73 STATUS: RESOLVED UNDER DELEGATION
OD-73 CHECK: pending

OD-74: the ICF hierarchy (R5–R7, R9). `base_icf.parent_code`. WHO's L2 and L3 blocks become rows keyed by their span, derived from the payload (b750–b789). All 3-digit categories are imported with WHO's titles by one verb that derives them from the persisted payload. `d910–d920` is not a WHO block and takes no parent. The lens-family helper is generalised from the identity lens to the ICF lens, and the need lens stays flat (its `family` column is its grouping).
OD-74 STATUS: RESOLVED UNDER DELEGATION
OD-74 CHECK: pending

OD-75: ICF titles (R8). A payload-verified title replaces a title whose source is not a payload. The old and new values are recorded in the migration header. A payload title is never overwritten.
OD-75 STATUS: RESOLVED UNDER DELEGATION
OD-75 CHECK: pending

OD-76: the glossary and the browse filter (R10, R11). The glossary is a read verb over the base, with no view and no committed file. A browse filter reads the specification's own lens column through that lens's family, never through the crosswalk. D-0184 is unchanged.
OD-76 STATUS: RESOLVED UNDER DELEGATION
OD-76 CHECK: pending

OD-77: the basis for an identity's ICF code (R12). WHO's tabulation grounds a code, its title and its place in the hierarchy, never an identity or need relation. The clause "a payload fetched from WHO under T-128" in ACTION (2) of "Owner answer 2026-11-21 (third)" is read so. That corrects the recorder's text, not the owner's words.
OD-77 STATUS: RESOLVED UNDER DELEGATION
OD-77 CHECK: pending

OD-78: holds (R13, R14). `identity_icf_map` is frozen and T-128 is held until the owner answers which mapping is not correct. `access_need_icf` stands. `access_needs.absorbs` is untouched until pairs cover every need and its non-identity terms have a home.
OD-78 STATUS: RESOLVED UNDER DELEGATION
OD-78 CHECK: pending

OD-79: the identity parent writer and the order of work (R15, R16). Add `amend-identity --parent`, bound to an owner entry, so that the owner's 2026-11-12 ruling "SCI and LMB go under MOB" can be executed. Ship the tooling (T-146, T-147) as one pull request before the research pull request (T-148).
OD-79 STATUS: RESOLVED UNDER DELEGATION
OD-79 CHECK: pending

**Reversal condition.** The owner reads S6 as one step, not two, or wants only the ICF codes the project uses in the base, or wants an umbrella cell not to gather its members. Before the tooling merges, reversal is deleting the branch. After it merges, reversal is a compensating schema migration. No judged row is lost, because the seeded pairs are pending and every triple keeps its three codes.

CONDITION: any session building T-146, T-147 or T-148, or reading the pairs layer, the ICF hierarchy, the glossary or `identity_icf_map`.
ACTION: (1) Read each OD above through the gate of "Convention 2026-11-12"; act only on OPEN. (2) Put the five questions of the reconciliation's section 2 to the owner; record each answer in the owner's words before acting on it. (3) Treat the [ASSUMPTION] marks in the reconciliation as unratified.
DATE: 2026-11-23 — delegated resolution under the owner's instruction of 2026-11-23, not an owner statement.
```
