# Adjudication: pull request 246, the decisions the grant of 2026-11-25 reaches, and the shortest path through the remediation plan

Written 2026-11-25 by an Opus-class adjudicator under the owner's words of 2026-11-25 ("authority granted to opus to approve and ratify"; "i just want to get this remediation plan done asap"; "as always refer to doctrine/mission/claude.md etc for guidance as required"; ledger: `grep -n -F "## Owner statements 2026-11-25" references/project-standards.md`). Read-only: no tracked file, database row or ledger line was changed. Branch `ccr-3c44891c-yjtha4` at `b561ffa5`; schema `python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma user_version').fetchone())"`. **No figure below is to be trusted; each is given with the command that produces it.**

**Standing.** Nothing here is the owner's words. Every ruling is a **delegated resolution**. Under ACTION (2) of the 2026-11-25 entry and the convention of 2026-11-12, each one's check line is `pending` until a **different** instance has checked it. Until then its gate is CLOSED and it opens no task. No "Owner" heading is proposed for any ruling here.

---

## 0. How far the grant of 2026-11-25 reaches (ruled first, because every other ruling depends on it)

**Ruling G.** The grant is a live owner statement (CLAUDE.md rule 0). It supersedes what it touches, and it touches the referral-back of OD-73 to OD-78 and the coordinator's work on pull request 246. It does **not** name, and so does not touch, four things. These stay outside it:

1. **Population taxonomy structure (codes, sub-codes, proxy decisions).** This is DG-NON under `governance/decision-protocol.md` §2.4 item 2. A departure from a default delegation must be explicit (§2.3), and a general grant is not an explicit departure. Outside the grant: SCI's fate (OI-77), any identity code or parent edge, and the statement, as fact, that a given group of disabled people has a given need or ICF code.
2. **What the owner meant by their own words.** The delegate can weigh the record but cannot supply the owner's meaning. This covers "I don't think the mapping is correct".
3. **Any row the schema binds to the owner's review.** In `identity_need_icf` these are `review_ref LIKE 'Owner%'` and `retirement_ref LIKE 'Owner%'`, set by migration 166 (`grep -n "LIKE 'Owner" scripts/migrations/166_identity_need_icf_owner_review.sql`). Writing such a row is forbidden by the grant's own ACTION (3).
4. **The convention that a task needing the owner's own words opens only on `ANSWERED BY THE OWNER`.** `grep -n -F "## Convention 2026-11-12" references/project-standards.md`, ACTION (2).

**What it reaches:**
- approval of the coordinator's tooling work. The owner still reads PR 246 before it merges (2026-11-23 ACTION (1); 2026-11-25 ACTION (1));
- schema, method and operational decisions the owner had kept or that were referred back (OD-73, OD-78's method, import scope, plan ordering);
- per-row *recommendations* that the owner confirms in one line.

**Precedent.** When the owner did want to ratify reserved items, they wrote "Sure, append. Ratify all." in reply to a report that named those items. The recorder then gave those items `ANSWERED BY THE OWNER` (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). That is the route for DG-NON. The owner can widen this grant in one line. **Reversal cost:** none, since this ruling builds nothing.

---

## PART A — The adversarial pass on PR 246, and the repair at `b561ffa5`

**Tests run on `b561ffa5`:**
- `python3 scripts/tests/test_icf_hierarchy.py`: every case passes (`EXAMINED:` printed; re-run).
- `python3 scripts/tests/test_assess_cell_pilot.py`: all pass.
- `python3 scripts/audit/derivation_handshake_integrity.py`: CLEAN, but it examines no ICF-keyed determination (see (5)).
- The engine's `assess_cell.stale_determinations(conn)` on the canonical database, read-only, returns `[]`. No live determination changed under the new gather.
- `import-icf-tree --dry-run` was run on a scratch copy against the persisted payload. Re-derive: `cp data/guidebook.db $S/t.db; GUIDEBOOK_DB_PATH=$S/t.db python3 scripts/db.py import-icf-tree --payload retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip --session session_x --dry-run`.

| # | Finding | Verdict on the repair | What remains |
|---|---|---|---|
| 1 | test pinned to canonical data | **Adequate.** The fixture is built from the live DDL of four tables and seeded in the test. HI-5 copies the canonical database only to borrow one live extraction. | HI-5 crashes, rather than failing, if no live extraction exists (`fetchone()` on an empty result). That is cosmetic. Also, HI-5 is missing from the module docstring's case list. |
| 2 | ICF cell crashes on a database without `parent_code` | **Adequate.** `dbcore.family_sql(conn, col)` reads `columns(conn, table)`, so a lens has a hierarchy exactly when its registry carries `parent_code` (rule 8). HI-0 shows identity and ICF yes, need no, and the pre-167 fallback. | Nothing. |
| 3 | import re-parenting and orphaning | **Inadequate on the orphan half.** Re-parenting is right: a parent is derived data, and HI-3 shows b1100 moving under a newly minted b110. The defect is in T-147, which says of a code minted by `add-icf-code` before the import is re-run that "Nothing reads the gap in between". **That is false.** The engine's `_lens_clause`, `cell-status` and the gate and gap filters read `parent_code` on every gather. A figure linked to a newly minted code is silently missing from its umbrella's cell until the import runs again. That is §5(a)'s shape. It is on the critical path, because T-128 mints d4452, d4153 and d4154. | Factor the import's parent derivation (the nearest present ancestor in the payload tree, which covers both the new code's parent and the children it takes over) into a helper taking `conn`. Call it from `insert_icf_code` whenever a payload-sourced block row exists. Ranges not sourced from a payload are excluded, so `d910–d920` never adopts children. Add a case in which a code minted after the import is gathered by its umbrella without a second import. If this is deferred, the T-147 sentence must be corrected and T-128 must run the import after its mints and before `emit_batch_sql`. |
| 4 | `FAMILY_TABLE` a curated list | **Inadequate.** `FAMILY_TABLE` is gone and `assess_cell.LENS_COLUMNS = dbcore.LENS_COLUMNS` is correct. But `db._LENS_COLUMNS` (`grep -n "^_LENS_COLUMNS" scripts/db.py`) is still a literal copy, and HI-0's equality case is a parity check. **CLAUDE.md rule 5: "A parity check is not a fix — it makes a dual home survivable, therefore permanent."** Rule 8 says the same. The stated reason for the mirror ("the extraction and the determination it feeds must name the lens the same way") is an argument *for* one home. `db.py` already imports `dbcore`. | Replace the literal with `_LENS_COLUMNS = dbcore.LENS_COLUMNS`. Move the re-pointing comment to dbcore. Delete HI-0's mirror case, or make it `is`. Correct the dbcore comment and T-147 ("deliberate mirror … held equal by HI-0"). HI-0 is **not** a sufficient guard: it keeps the duplication. |
| 5 | untested paths | Walk-up branch: **covered** (HI-2, b1100 → `b110–b139`). `cell-status` on the ICF lens: **covered** (HI-5). **Handshake audit: the gap is acceptable for merge.** Its one changed line calls the same `lens_differs(g, s, lens_families(con, s))` that ICF-04 tests directly, and `s` is a `dict` (`specs = [dict(r) …]`). No ICF-keyed determination exists today (`select count(*) from specifications where icf_code is not null`), so the line examines nothing whatever a test says. | File a gap: a fixture case in the handshake audit's test, owed before the first ICF-keyed determination is written (T-110 or earlier). |
| 6 | 19 confirmed titles sourced as unverified | **Partly adequate.** The new `confirmed` branch re-sources a title that the payload matches case-insensitively. However, it **returns only the code**. The old `title_source` is lost from the verb's output, even though OD-74 says the old value and its source go in the data migration's header. The dry run shows the confirmed rows' old sources are a skill file and `access_need_icf.note`. The branch also writes the payload's wording, so the HI-1 label "keeps its wording" holds only because no casing differs today (dry run: none). | Return `[code, old_title, old_source]` for `confirmed`, as for `replaced`. T-148 step 1 must also put the `confirmed` list in the migration header. Relabel HI-1 ("takes the payload's wording and source; the old source is returned"). |
| 7 | glossary cycle | **Adequate.** The path guard uses `instr(t.path, '/'||code||'/')`, and `family_sql` uses `UNION`. HI-4 builds a cycle. | Nothing. |
| 8 | en dash vs hyphen key | **Inadequate. New defect, demonstrated** on a scratch copy. `insert_icf_code` normalises `\s*[-—]\s*` only. An **en dash with spaces** (`"e100 – e199"`) is stored verbatim as a **second key** for the span, because `_ICF_CODE_RE` admits `\s*` around an en dash. U+2212 (minus) and U+2010 (hyphen) are refused, which is safe. `icf-glossary --umbrella b750-b789` (a hyphen, as the owner types it: "b750-789") refuses with "is not an ICF code with codes beneath it", which is misleading. | One normaliser in dbcore, `icf_key()`: `re.sub(r"\s*[-‐-―−]\s*", "–", s.strip())`. Call it from `insert_icf_code`, `icf_glossary` and every verb that takes an ICF code (`git grep -n -E "icf_code: str|--icf-code|--icf\b" -- scripts/db.py`). Add a case for the en dash with spaces. The existing CHECK (`GLOB '[bdes][0-9][0-9][0-9]*'`) and every stored code are unaffected: every stored range already uses an unspaced en dash (`select icf_code from base_icf where is_range=1`). |
| 9 | garbled refusal text | **Adequate** ("should be a header row that names 'ClassKind'"). | Nothing. |
| 10 | prose callers | **Partly adequate.** Still stale: T-147's first table row (`dbcore.family_sql('icf_code')`), migration 167's header (the same; immutable, so the account goes in the next migration's header), and the PR body (see 11). The ledger's OD-75 line naming `IDENTITY_FAMILY_SQL` is history and stays. | Sweep: `git grep -n -E "FAMILY_TABLE|IDENTITY_FAMILY_SQL|family_sql\('" -- ':!transcripts' ':!*commands.jsonl'`. |
| 11 | PR body errors | **Unrepaired.** The PR body still carries the original errors (`gh api repos/jordanelias/guidebook/pulls/246 --jq .body`). See the corrected sentences below. | Edit the PR body once, with the final push. |
| 12 | test labels | **Partly.** False or loose labels remain: HI-0 "the lens map has one home and its mirror agrees" contradicts itself; HI-1 "keeps its wording" (see 6); HI-4 "gives one key to a span however its dash is typed" in the docstring is false (see 8); HI-4 "and so does the family" asserts only that the family is non-empty. | Relabel as in 4, 6 and 8. For the family half of HI-4, assert the set equals `{b765, b750–b789}`. |
| 13 | OD-73..OD-78 not in the §8 register | **Unrepaired.** The convention scopes "each decision of the register §8". The generator reads the register from `^### OD-NN` headings, so it reads 71 decisions and none of these (re-derive with the copy in Part C). | Add §8 entries for OD-73 to OD-78, and for the decisions proposed below, each with its status line command and the tasks it releases. This is a governance text edit and may ride in PR 246. |
| 14 | payload held twice | **Adequate for the tree.** `who/` is deleted, and `icf_glossary.py` reads the logged zip in place. | The extracted text stays in the branch's history. This repository merges with merge commits (`git log origin/main --merges -3 --format=%s`), so it reaches `main`'s history. That cannot be undone without a rewrite, which is blocked. Record it; it is not a defect to chase. |

**Withheld item: the glossary's `identity_links` and `triples` columns. Ruling: keep both, and relabel them.** OD-77 forbids copying, citing or extending `identity_icf_map`. A count shown to the owner does none of those. Hiding the table would hide the very thing the owner doubted. But an unlabelled count reads as vetted links. Changes:
- `identity_links` becomes `identity_icf_map_rows (frozen, OD-77)`;
- `triples` splits into `identity_need_icf_stated` and `identity_need_icf_pending`, because a count that mixes pending rows with the one stated row overstates review;
- `need_links` becomes `access_need_icf_rows`.

Basis: OD-77 (`grep -F "OD-77 STATUS:" references/project-standards.md | tail -1`); CLAUDE.md §5(b) (prose contradicting the database); the owner reads only what the glossary prints. **Reversal:** rename the keys back.

### New defects in the repair diff (`git diff 9fca0b4..b561ffa5 -- scripts`)

- **N1** (= 8): the en dash with spaces creates a second key for one span. *Must fix before merge.*
- **N2** (= 6): the `confirmed` branch drops the old source. *Must fix before merge.*
- **N3**: `db._gap_applies(row, lens, …, families={})` has a mutable default. With the repair, `lens_differs` reads `families.get(c, ())` for **every** lens, the access-need lens included. A caller that omits `families` therefore skips every gap naming any lens the cell states. Before the repair, the need lens compared by equality. No caller omits it today (`grep -n "_gap_applies(" scripts/db.py`). *Remove the default.*
- **N4** (= 3): the orphan window, and the false T-147 sentence.
- **N5**: the glossary refuses a hyphen-typed span, the owner's own typing (see 8).
- **N6**: `_lens_clause(conn, …)`: every call site is updated (`grep -n "_lens_clause(" scripts/assess/assess_cell.py` shows `conn` first everywhere; T-019's task file is history). `lens_families` now runs one query for the need lens as well. That is harmless.
- **N7**: the reparent branch is correct and idempotent (HI-3). `parented` returns codes, while `reparented` returns triples `[code, old, new]`. T-148's header must list both.
- **Not a defect**: `RULE_VERSION` stays. ICF-03 shows an ICF cell with no parents gathers exactly its own code, and `stale_determinations` is empty. T-148 must re-derive `select count(*) from specifications where icf_code is not null` before it writes parents.

### PR 246: corrected sentences for the body

- In place of the quotation paragraph: Your words of 2026-11-22: "so perhaps for ICF I really want those classification umbrellas like "Movement functions" , "Pain", "Hearing and vestibular systems" etc and some kind of glossary that shows all the codes bundled under those classification umbrellas", and "our project filters specifications based on three approaches, and the browsing user chooses one of those approaches to use for browsing".
- In place of "One family rule per lens with a hierarchy …": **One family rule, derived from the schema.** A lens has a hierarchy when its registry carries `parent_code` (`dbcore.family_sql(conn, col)`): the identity and ICF lenses do, and the access-need lens does not (`access_needs.family` is its grouping). A database that predates the column reads each code as its own family. `dbcore.LENS_COLUMNS` is the one home of the lens map.
- Append to the import bullet: It resets a stored parent that differs from the payload's, because parents are derived, so it can be run again after a code is minted. It also takes the payload as the source of a stored title the payload confirms, returning the old source.
- In place of "`family_sql('icf_code')` is read by …": `dbcore.family_sql(conn, col)` is read by `assess_cell._lens_clause`, `assess_cell._open_gates`, `db.py cell-status` (the extraction count, gap and gate filters) and `derivation_handshake_integrity`.
- In place of the Measure sentence: Measure: `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`. The tests' share: `git diff --shortstat origin/main -- scripts/tests`. Tests are not most of the insertions; re-run both.
- In place of "New cases: `test_icf_hierarchy` (13) … With `icf_code` removed from `FAMILY_TABLE` …": New cases: `python3 scripts/tests/test_icf_hierarchy.py` (it prints its `EXAMINED:` count) and `ICF-01` to `ICF-04` in `test_assess_cell_pilot.py`. With the ICF lens made flat (no `parent_code` on the fixture's `base_icf`), `ICF-01` and `ICF-04` go red.
- In place of the import figures: the import was run on a scratch copy against the persisted WHO payload. Re-derive what it would mint, parent, title, replace, confirm and leave unmatched with `import-icf-tree --dry-run` on a scratch copy. `d910–d920` is the one held code WHO does not name.
- Footer, as the session's attribution requires: "🤖 Generated with [Claude Code](https://claude.com/claude-code)" and the session link.

**Verdict on PR 246 (delegated approval, check pending).** **Approved for the owner's reading once N1 to N4 are repaired**, together with finding 4, the glossary relabel, the T-147 prose, finding 13's register entries and the PR body. Without them, merging would land a second home for a span key and a parity-checked duplicate (rule 5). The owner merges; the delegate does not.

---

## PART B — Delegated resolutions

Each is written as it would be appended. The recorder confirms the next free OD number with `grep -ohE "OD-[0-9]+" references/project-standards.md | sort -t- -k2 -n -u | tail -1`. **Every CHECK line below reads `pending`, and stays so until a different instance has checked it.**

### OD-73: an identity–need pair may be recorded before any ICF code is chosen. **RESOLVED UNDER DELEGATION, check pending.**

**Ruling.** Yes, in a table of its own. **"Should be all three" is untouched**: every `identity_need_icf` row keeps identity, need and ICF code, each NOT NULL.

**Basis.**
- The owner's later words, typed 2026-11-22 (`git grep -n -F "we should be able to map them to one another" -- transcripts`): "So we should have a list of access needs, we should have a list of disability identities, and we should be able to map them to one another / and from there, perhaps, we select ICF codes that pertain to those relationships". The mapping sentence is unhedged. "Perhaps" qualifies only "we select ICF codes".
- Rule 0: the 2026-11-22 statement supersedes what it touches. What it touches is the sentence of migration 165's header, "What is known of only two is a `gaps` row … not a stored row" (`sed -n 12,13p scripts/migrations/165_identity_need_icf.sql`). That sentence is the coordinator's design text, not the owner's words.
- The "should be all three" answer (2026-11-20 fifth) chose how many keys a row **of that table** holds. It is not contradicted by a second object the owner later asked for.
- 2026-11-20 ACTION (3): "an identity … with no recorded need, is a gap to close". The owner's "i don't want to have to constantly map … the base needs to get that ready for me".
- CLAUDE.md rule 5. Today the only way to record a pair is to copy a need's own environmental code onto the identity. The copied rows are those of the triple table that `access_need_icf` already holds: `select count(*) from identity_need_icf t where retired_at is null and exists (select 1 from access_need_icf a where a.need_code=t.need_code and a.icf_code=t.icf_code)`. TRIPLE-65 came from that pressure.
- The ruling is D-SCHEMA. It creates no population code and states no pair, so §2.4 item 2 is not reached.

**Minimal schema** (tooling, its own pull request, rule 10). It folds in the antagonist's corrections and one defect found here:
- One table, `identity_need`. Columns:
  - `pair_id` INTEGER PRIMARY KEY AUTOINCREMENT;
  - `identity_code` and `need_code`, NOT NULL with real FKs;
  - `state` (the cell states' CHECK, read as migration 166 reads it), `warrant` NOT NULL;
  - **`inferred` INTEGER NOT NULL CHECK (inferred IN (0,1))**, the inference flag in its own cell (one value per cell, 2026-11-06);
  - stamps;
  - the review cells and retirement cells **with migration 166's `LIKE 'Owner%'` CHECKs and its no-edit trigger, copied unchanged**. No guard is relaxed.
- **A partial unique index on live rows**, `(identity_code, need_code) WHERE retired_at IS NULL`, so that a retired pair can be proposed again.
- **No composite foreign key from `identity_need_icf`.** Measured here: SQLite refuses a partial unique index as a foreign-key parent ("foreign key mismatch"). R2's FK and the antagonist's partial index therefore cannot both stand, and the partial index is the one that matters. The shared `(identity_code, need_code)` is the pointer, as a shared `ref_id` is (CLAUDE.md §3). `review-identity-need-icf` refuses to state a triple whose live pair is not `stated` or `provisional` (R4). `identity_need_icf` is not rebuilt.
- **No seed in the schema migration.** Pairs are proposed in the research pull request by `propose-identity-need-icf` with no `--icf-code`, each carrying its warrant and `inferred`.
- **TRIPLE-65 stays retired**, and COM–A-TIME is not proposed (Owner review 2026-11-21, ACTION (2)).
- `v_lens_crosswalk` shows pairs with no code, and reaches a need's own `access_need_icf` codes through the pair by a join. The owner's 2026-11-21 (sixth) "they count as identity's ICF coverage" is met by counting through the join, not by stored copies.
- Read by: `v_lens_crosswalk`, `lens-crosswalk --uncovered`, the two verbs, and the owner.
- Without it, a pair forces an invented ICF code, which is what produced the copied rows and TRIPLE-65.

**Reversal cost.**
- Before the tooling merges: delete the branch.
- After it merges with no rows: a compensating migration drops the table and the verb branch.
- After pairs are recorded: they are `pending` until the owner reviews them, so dropping loses no judgment.

**What the grant does not reach.** Whether any pair is true, and every pair's `stated` state. Those are the owner's (Q3).

**Opens, once the check is confirmed:** authoring and building T-146 (tooling), then the pair-recording part of T-148 (research). The pairs reach `stated` only on the owner's review.

### OD-78: what may ground a body-function code on an identity or pair. **RESOLVED UNDER DELEGATION, check pending.**

**Ruling.**
1. A persisted WHO **simple tabulation** grounds a code's existence, title and place in the hierarchy only. It holds no definitions and no relations (its header columns are URI, code, BlockId, title, kind, depth, flags, coding note and parent). It is never cited as the warrant for an identity's or a pair's code.
2. A WHO **entity page** may be quoted in a proposal's warrant as the code's meaning, once it has been retrieved through `retrieval_log.fetch()` and persisted. Its definition, inclusions and exclusions are facts about the code, not about any group.
3. A session **may propose** a body-function or body-structure code for an identity or a live pair. The proposal is `pending`, and its warrant must say in words that the tie is the session's own inference and name the definition text it relied on. It is **never `stated` without the owner's review**; migration 166's guard stays as it is.
4. No code is proposed on a pair that has no recorded basis.

**Basis.**
- The owner's own review practice. The owner **accepted TRIPLE-64** knowing the coordinator had disclosed that b210 and its meaning came from its general knowledge, and **rejected TRIPLE-65** because "the pair is an inference no record states" (`grep -n -F "## Owner review 2026-11-21" references/project-standards.md`). The rejection concerned the pair, not the code. That supports clause 4, and it shows the owner reviews disclosed inferences about codes.
- The owner's "1 yes b is seeing therefore ties into blind etc" (2026-11-21 third). "Etc" asks for more ties of this kind.
- "the base needs to get that ready for me" (2026-11-20).
- CLAUDE.md §5(c) and "fetch before you write": a title comes from the payload, never from memory.
- `governance/mission-and-epistemics.md` §"Purpose": a thinking tool, not an authority. A disclosed inference that the owner reviews is the honest form of a proposal.
- The ACTION (2) list of 2026-11-21 (third) is the recorder's text. This ruling reads its "payload fetched from WHO" clause as grounding the code's meaning, which narrows no owner word.

**Reversal cost.** Withdraw the clause. Proposed rows are `pending` and are retired by the owner's entry; nothing is stated.

**What the grant does not reach.** Whether any body-function code ties to any identity. That stays the owner's, row by row.

**Opens, once confirmed:** the proposal step of T-148 for pairs the owner has accepted (reconciliation §3.2 item 6). No plan task in §3 waits on it.

### "The mapping" the owner doubted. **No resolution of meaning; a hold ruling.** OD-77 stays as checked.

**Finding from the transcript.** The reconciliation's draft reading ("it was the mapping the session had just described") **is contradicted by the timestamps**. Trace with: `python3 -c "import json;[print(json.loads(l).get('timestamp'),json.loads(l).get('type')) for l in open('transcripts/harness_c6286d2b/main.jsonl').read().splitlines()[100:170]]"`. The sequence:

| UTC time on 2026-11-22 | Event |
|---|---|
| 04:04:08 | The owner types "I don't think the mapping is correct". |
| 04:04:15 | The coordinator's first message describing `identity_icf_map`. |
| 04:03:02 | Before the owner's message, the owner had been told that PR 245 "filled `identity_need_icf` with pending rows". |
| 04:02:11 | The owner's own first message objected that "the ICF codes used are not what I was expecting". |

The 2026-11-22 ledger reading was right, and the weight of the record leans towards the PR 245 rows (`identity_need_icf`). The rows of those triples that copy a need's own environmental code onto each identity fit "the ICF codes used". Re-derive their count with the rule 5 query under OD-73 above.

**Ruling.** The delegate does not decide what the owner meant (Ruling G, item 2). Both candidates are already safe without guessing:
- `identity_need_icf` is all `pending` except the owner's own TRIPLE-64 (`select state,count(*) from identity_need_icf where retired_at is null group by 1`), and nothing in it can become `stated` without the owner.
- `identity_icf_map` stays frozen for new rows, warrants and copies (OD-77).
- No table is retired. The question goes to the owner as Q2, naming both candidates and the timing.

**Reversal:** none needed. **Opens:** nothing until the owner answers. T-128 may still prepare its list on a scratch copy; its own file allows that.

### The pairs of the live triples (reconciliation §2 Q1). **A delegated recommendation, not a review.**

Derive the pairs with: `select identity_code, need_code, group_concat(triple_id), max(state), min(warrant) from identity_need_icf where retired_at is null group by 1,2`. Each row is classed by the words of its own warrant.

| Class | Pairs | Basis in the record | Recommendation |
|---|---|---|---|
| A: the need's registry text names the identity's group, or each side names the other | ADHD–A-LOWLOAD, AUT–A-CALM, AUT–A-STIMULUS, BLIND–A-NOSIGHT, BRAIN–A-LOWLOAD, BRAIN–A-PLAIN, DEAF–A-NOSOUND, DEAFBLIND–A-TACTILE, DEM–A-LOWLOAD, DEM–A-PLAIN, ID–A-LOWLOAD, ID–A-PLAIN, MS–A-EFFORT, PAIN–A-EFFORT; BAR–A-SIZE, LPA–A-SIZE, TALL–A-SIZE | `access_needs.absorbs` and the identity's own description. These are proposals under owner review (OD-77). | **Accept.** |
| B: the need names a condition the identity's description lists; the row is keyed on the whole identity | BRAIN–A-STABLE, BRAIN–A-STIMULUS, COM–A-EFFORT, COM–A-TRIGGER, EPI–A-TRIGGER, MH–A-CALM, MH–A-STIMULUS; NDV–A-CALM, NDV–A-LOWLOAD, NDV–A-STIMULUS | The condition appears on both sides. For A-TRIGGER: "photosensitive epilepsy, MCAS" in the need; "photosensitivity is a relevant subtype" in EPI; "MCAS" in COM. Keying on an umbrella is the owner's own answer, "to umbrella and to specific, yes" (2026-11-21 second). `governance/mission-and-epistemics.md` commitment 1: "people are not uniform … Co-occurring conditions are the norm". | **Accept**, with the warrant saying the need serves part of the identity. Accepting COM–A-TRIGGER and EPI–A-TRIGGER answers GAP-379's open sub-question. |
| C: "No record read stated this link; it was recorded as an inference" | BRAIN–A-NOSPEECH (aphasia; stroke), COM–A-LOWLOAD (brain fog; long COVID) | None. This is the owner's TRIPLE-65 ground. | **Reject.** Do not re-propose without a recorded basis (Owner review 2026-11-21, ACTION (2)). |

**What the grant can make true:** this per-pair recommendation, recorded as a delegated resolution, and a one-line question the owner answers. **What it cannot make true:** a pair or triple `stated`, `provisional` or retired. All three need an "Owner" heading the owner made. Two points of order:
- The owner's answer should be recorded **onto pair rows once OD-73's table exists**, not onto the triples. Stating the copied triples would make a forbidden dual home permanent (rule 5).
- BLIND–A-NOSIGHT's pair needs the owner's line too. The owner accepted TRIPLE-64, not a pair token.

### Q4: retire the triples that only repeat a need's own environmental code. **Not now.**

Rule 5 makes them copies (re-derive with the query under OD-73). But until a pairs home exists, they are the **only** record of most pairs. Retiring them now would erase pairs and leave BLIND–A-NOSIGHT alone (TRIPLE-64).

**Ruling.** Retire them only after the pairs are recorded (OD-73, then T-148). Retirement needs an Owner entry (`retirement_ref LIKE 'Owner%'`), so it is folded into Q3. Once they are retired, GAP-379's `e120` sub-question (A-SIZE's mobility-products code on LPA, TALL and BAR) dissolves, because the code is reached through the pair.

### Q5 is not asked; where WHEEL stands

OD-14 is answered by the owner (`grep -F "OD-14 STATUS:" references/project-standards.md | tail -1` prints `ANSWERED BY THE OWNER`). The owner decomposed mobility by device. The eighth set says "only SCI is the same as WHEEL" and the ninth names LLD. **WHEEL is not minted:** `select count(*) from base_taxonomy_identity where identity_code='WHEEL'` returns 0. The split is T-102, a research task for an Opus-class session, which is open on its owner gate. T-102 itself must stop before retiring SCI until the owner answers OI-77 (`grep -n -F "Do not run T-102's retirement of" references/project-standards.md`).

### OD-76 stays withdrawn. **Confirmed.**

Writing `parent_code = MOB` on SCI and LMB contradicts the owner's eighth set ("LMB becomes UPL … not part of mobility; only SCI is the same as WHEEL"; `grep -n -F "## Owner clarification 2026-11-12 (eighth set)" references/project-standards.md`). SCI's fate is OI-77, which is DG-NON. T-102 mints its new codes with `add-identity --parent` at mint, so no `amend-identity --parent` is owed. **Opens nothing.**

### Proposed OD (next free number): import every 3-digit ICF category, not only the codes held. **RESOLVED UNDER DELEGATION, check pending.**

**Basis.** The owner's own words in S1, not the unratified reading of S2: "some kind of glossary that shows **all the codes** bundled under those classification umbrellas". The glossary reads `base` (render reads the database, CLAUDE.md §3), so `base` must hold them. The 3-digit grain is the grain of the owner's examples (b210, b230, b265, b280). Deeper codes are minted when used. CLAUDE.md §6 (codes and names). This is WHO's vocabulary, not population taxonomy.

**Reversal.** Unreferenced rows are deleted by a compensating migration.

**Opens, once confirmed:** a small tooling change (a `--categories` switch on `import-icf-tree`, or making it the default), in PR 246 before merge if the check lands in time, otherwise a follow-up tooling PR. Then T-148 imports. It **supersedes** OD-74's correction that "the rest only if the owner says so". That clause rested on S2; S1's words state it.

### Proposed OD (next free number): T-102 runs without retiring SCI, and T-127 and T-128 wait only for WHEEL. **RESOLVED UNDER DELEGATION, check pending.**

**Ruling.** T-102 mints the owner-confirmed codes and carries the MOB rows, leaving SCI active and its rows untouched until OI-77 is answered. The preconditions of T-128 and T-127 ("WHEEL minted, SCI retired to it") are narrowed to "WHEEL minted". SCI-keyed rows are carried later by the step that executes the owner's OI-77 answer.

**Basis.** D-OP; it decides nothing about SCI. The owner's ACTION bars only the retirement. The rows at stake are few: re-derive per table with `select count(*) from <t> where identity_code='SCI'` over `identity_icf_map`, `extraction_lens_links` and `gaps`. "get this remediation plan done asap" (2026-11-25).

**Reversal.** Restore the precondition text.

**Opens, once confirmed:** T-102 as a whole except its SCI step. It also removes OI-77 from the head of the critical chain. T-128 still waits for the mapping answer and its OD-67 list.

---

## Questions for the owner (yes or no; three, all population taxonomy or the owner's own meaning)

1. **Spinal cord injury (OI-77).** With the medical lens deleted, is "people with spinal cord injuries" (SCI) still retired into the new wheelchair-user code, as you said on 2026-11-12 ("only SCI is the same as WHEEL")? **Yes**, or **no** (keep SCI as an identity of its own).
2. **"I don't think the mapping is correct" (2026-11-22).** Did you mean the identity–need–ICF rows of PR 245, which copy a need's own building and lighting codes (e150, e240 and others) onto each identity? **Yes**, or **no** (you meant the identity-to-activity list, for example DEAF → d310–d329).
3. **The identity–need pairs.** Accept the pairs of classes A and B (listed in this file, Part B), which include the no-trigger need for both epilepsy and the complex-conditions group. Reject BRAIN with no-speech (aphasia) and COM with low cognitive load (brain fog), because no record states either. Once the pairs are recorded, retire the rows that only repeat a need's own environmental code. **Yes**, or **no** (name the exceptions).

---

## PART C — The remediation plan: live state and the shortest path

**Commands.**
- **Gates:** run the convention's `gate()` for every register decision: `for i in $(seq -w 1 78); do gate OD-$i; done | grep -v OPEN` (define `gate()` from `grep -n -A3 "^\*\*The gate" references/project-standards.md`). On `b561ffa5` it printed only OD-16 (no register entry), OD-73, OD-76 and OD-78.
- **Tasks:** run a copy of the generator with its output moved out of the tree. The script writes `REMEDIATION-PLAN.md` despite its docstring.
  - `S=<scratch>; sed "s#^OUT = W / \"REMEDIATION-PLAN.md\"#OUT = __import__('pathlib').Path('$S/plan-now.md')#" scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py > $S/bb.py && python3 -I $S/bb.py`
  - Then the task rows: `grep -E "^\| \[T-" $S/plan-now.md`.
- **Merged:** the generator's "merged" set (it reads `BATCH-1-EXECUTION-NOTES.md` "Executed" and `git log`), **plus T-145**, which merged in #244 (`git log origin/main --merges --format='%h %b' | grep -F T-145`) but is absent from the notes the generator reads.

### Where the plan and the repository disagree (flags)

- **T-145 is merged but the generator calls it open.** The executed record (`BATCH-1-EXECUTION-NOTES.md`) omits it. Add it.
- **T-112 was largely executed by #243 and is recorded nowhere.** That PR translated the non-English titles and figures. The residue is `python3 scripts/db.py translations --due-at judgment`, which shows the cells still owed. T-104 overlaps #243's re-retrieval and downgrade of unproven VERIFIED sources. Record both as "in part".
- **T-128's file says "HELD until the owner answers OD-67".** OD-67's gate is OPEN on the owner (2026-11-19 ratification). The real holds are T-102 (WHEEL) and OD-77 with the mapping question. The file and the workplan's §6 stop row are stale.
- **The generator reports OD-69 as "blocking" T-135.** That is an artefact: it treats every named decision as needing the owner's words. T-135's own gate prints OPEN (delegated; confirmed by the owner's "Ratify all"), and its file does not require owner words for the shape. T-135 is open.
- **T-055 is "merged", but its parent-gathering has examined nothing.** No identity carries a parent (`select count(*) from base_taxonomy_identity where parent_code is not null`) until T-102. That is §5(a), not a defect in T-055.
- **The register lacks OD-73 to OD-78 and OI-77** (finding 13). OI-77 holds T-102's SCI step and has no status line.
- **New tasks are outside the index:** T-147 (this PR), T-146 (pairs, not authored) and T-148 (research, described in T-147).

### Open tasks, with what holds each (derived on `b561ffa5`; re-run the generator)

| Task(s) | Kind (rule 10) | Who | Holds it |
|---|---|---|---|
| T-147 | tooling | coordinator repairs; **owner merges** | Part A must-fixes; owner's read (OD-74, OD-75 gates OPEN) |
| T-148 | research | Opus | T-147 merged; pairs part: OD-73 (CLOSED, check pending) and owner Q3; b-code part: OD-78 (CLOSED, check pending) |
| T-146 | tooling | Opus, or Sonnet with a design | OD-73 check; to be authored |
| T-102 | research | Opus | nothing now (OD-14 owner; deps merged); SCI step: owner Q1 (OI-77) |
| T-128 | research | Opus | T-102 merged; owner Q2 (mapping, OD-77 hold); owner confirms its list (OD-67) |
| T-127 | research | Opus | T-102, T-128 |
| T-120 | tooling (doctrine prose) | Opus | nothing (T-119 merged) |
| T-137, T-136 | tooling | Opus | nothing |
| T-138 | tooling | Opus | T-136, T-137 |
| T-143 + T-059 | tooling | Opus | T-120, T-127, T-128, T-137 |
| T-068 | tooling | Opus | T-059, T-120 |
| T-117 | tooling | Opus | T-068, T-102, T-120 |
| T-124 | tooling | Opus | T-059, T-068 |
| T-122 | tooling | Opus | T-059, T-068, T-117, T-124 |
| T-037 | tooling | Opus | T-032, T-036, T-122, T-124 |
| T-038 | tooling | Sonnet | T-037 |
| T-039 | tooling | Opus | T-037 |
| T-110 | research | Opus | T-059, T-068, T-102, T-104, T-117, T-123, T-127, T-128, T-133 |
| T-005, T-033, T-047, T-052, T-056, T-057, T-084, T-140, T-130 (after T-129) | tooling (T-084 research) | Sonnet | READY per generator |
| T-101, T-104, T-108, T-111, T-112 (residue), T-113, T-114, T-116 | research | Sonnet | READY (one research PR at a time, OD-27) |
| T-027, T-032, T-035, T-053, T-060 (design missing), T-091 (design missing), T-129, T-135, T-139, T-141, T-142 | tooling | Opus | see generator column 8 |
| T-069, T-070, T-071, T-072, T-081, T-082, T-086, T-087, T-092, T-105, T-106, T-107, T-109, T-115, T-123, T-131 | research | Opus | see generator column 8 |
| T-036, T-040, T-058, T-062, T-085, T-118, T-125, T-132, T-133 | tooling | mixed | their listed deps |

### ODs still closed, and what opens each

| OD | State | What opens it |
|---|---|---|
| OD-73 | CLOSED | this file's delegated resolution plus a confirmed check by a different instance |
| OD-78 | CLOSED | the same |
| OD-76 | CLOSED | stays withdrawn; nothing to open |
| OI-77 | no status line | the owner's answer (Q1); register it first |
| Mapping question | not registered | the owner's answer (Q2); OD-77's hold reads it |
| The two proposed ODs above | not yet written | ledger lines, then a confirmed check |

### Critical path (the generator's longest chain, with today's holds)

**T-102 → T-128 → T-127 → T-059 (with T-143) → T-068 → T-117 → T-122 → T-037 → T-038**, beside T-120 and T-137, which feed T-059 and the chain after it. T-110, the first live determination, closes it, with T-104, T-123 and T-133 in parallel. The two owner answers on the chain are Q1 (removed from its head by the proposed T-102 ruling once checked) and Q2 (it gates T-128, together with the OD-67 list).

**Ordered next steps.**
1. **Now, in parallel.**
   - (a) The coordinator repairs PR 246 per Part A (tooling) and has a different Opus instance check this file's rulings.
   - (b) An Opus session starts **T-120** (tooling, no gate).
   - (c) An Opus session starts **T-137** (tooling, no gate).
   - (d) An Opus session starts **T-102** (research, SCI step held).
   - (e) The coordinator puts Q1 to Q3 to the owner.
2. **The owner merges PR 246.** Then **T-148** imports the ICF tree (research). The pairs half waits for the OD-73 check, T-146 (tooling) and Q3.
3. **T-102 merges.** **T-128** prepares its list. The owner answers Q2 and confirms the list (OD-67). T-128 merges.
4. **T-127** (research). Then **T-143 with T-059** (tooling), **T-068**, then **T-117 and T-124**, **T-122**, **T-037**, **T-038**. T-110 follows once T-104, T-123 and T-133 have merged.
5. **Off the critical path, throughout:** the READY Sonnet tasks, one PR at a time (plan §2 step 2), tooling before research (rule 10).

**Single next action:** the coordinator applies Part A's must-fix repairs to PR 246 (tooling) and sends this file to a different Opus-class instance for its check. The owner's Q1 and Q2 go out in the same message.

---

## What could not be verified

- I did not run the Definition of Done lines (§10) or `preflight.sh`; per CLAUDE.md §1, the gate is run once on the final diff.
- I did not read whether T-120's doctrine edits need the owner's sign-off under CLAUDE.md §8 ("doctrine"). The plan says no owner answer is needed. Check before starting.
- Whether the owner's "Ratify all" (2026-11-19) covers T-135's own-words clause was read from T-135's file, not re-adjudicated.
- I did not open the WHO entity pages, so OD-78's clause 2 rests on their being retrievable.
- I did not check every merged task's after-test; the spot-checked schema objects exist.
