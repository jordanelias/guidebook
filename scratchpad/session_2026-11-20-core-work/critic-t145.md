# Critic pass on T-145 (commit 57fcbf3, ledger 8a4c76d; subject HEAD a0214b5; DB user_version 165; 2026-11-20)

Read-only on the repository. Every verb was run on copies of `data/guidebook.db` under
`/tmp/claude-0/-home-user-guidebook/de695d5a-dedc-5500-919e-a70853955650/scratchpad/t145/` with `GUIDEBOOK_DB_PATH`
set inline. Canonical sha256 before and after: `de5f6fe6...2a8db81` (unchanged). Every count below was computed in
this pass. The diff-scoped gate was run once (`run_checks.py --changed-from origin/main --explain`): 72 green,
6 nothing-in-scope, 10 advisory failures, 0 blocking failures; none of the 10 names an object of this change.

## Ranked findings (worst first)

### 1. BLOCKS - "only the owner's review makes a row `stated`" is held by nothing; the proposing session states its own rows
Artifact: `scripts/db.py` `review_identity_need_icf` (the `reviewed_by` handling and the accept branch);
`scripts/migrations/165_identity_need_icf.sql` columns `reviewed_at`, `reviewed_by`.
Claim (migration header, THE STATES): "Only the review verb, run on the owner's review of a batch, sets `stated`".
Failure case, run on a copy:
```
db.py propose-identity-need-icf --identity ADHD --need A-AT --icf-code b114 --warrant w0 --session session_2026-11-20-critic-x
db.py review-identity-need-icf --triple-ids 1,1 --decision stated --reviewed-by "the session itself" --session session_2026-11-20-critic-x   # rc=0
python3 scripts/research/emit_batch_sql.py --scratch a.db --out a.sql      # "4 insert(s), 0 update(s)"
```
`a.sql` line 11 is `INSERT INTO "identity_need_icf" (...) VALUES (1,'ADHD','A-AT','b114','stated','w0',...,'the session itself',...)`.
One session, one scratch, one data migration: the row arrives in canonical already `stated`, and no step in between
involved the owner. The verb's only test of authority is `if not reviewed_by` (a non-blank string).
- What the schema gives a reader to tell an owner's review from a session's: one free-text cell. On an accept the
  `session` argument is required by argparse and then not used (it is read only in the `reject` branch), so the session
  that ran the review is recorded nowhere. A second review in another session emitted
  `UPDATE "identity_need_icf" SET "state"='stated',"reviewed_at"=...,"reviewed_by"='Anyone' WHERE "triple_id"=3;`
  with `session_2026-12-02-rev` appearing in no cell.
- The repository already has a way to bind a write to the owner's words: `_owner_approval` plus
  `dbcore.ledger_entry_names` (used by `retire-identity`, which refuses a heading that is not an `Owner ...` ledger
  entry naming the code). `grep -c "_owner_approval(" scripts/db.py` prints 7. The review verb uses none of it.
- No check reads the table. `adversarial_pass_recorded` derives its subject tables (11 printed in the gate run);
  `identity_need_icf` is not among them, so the research batch that fills the matrix is not required by that gate to
  record a pass either.
- The test's own case "AT-2 review makes it stated and names the reviewer" passes with `reviewed_by='owner'` typed by
  the test. It shows the string is stored, never that the owner reviewed.
The Q2 answer itself is an unratified [ASSUMPTION] in the ledger entry; the build claims to enforce it and does not.

### 2. MUST-AMEND - a provisional review of a `not_applicable` row discards the owner's caveat and reports success
Artifact: `review_identity_need_icf`, the line `reason if state == "provisional" else None`.
Run: `db.py review-identity-need-icf --triple-ids 4 --decision provisional --reviewed-by owner --reason "CAVEAT TEXT" --session ...`
on a `not_applicable` row. rc=0, output `"decision": "provisional"`. Stored row:
`(4,'ADHD','A-AT','b140','not_applicable','na',...,'owner', review_note=None, ...)`. `--reason` is demanded
(`require_reason`) and then thrown away; the return value says the opposite of what was written. A mixed batch
(pending and not_applicable ids, decision provisional) gives some rows the caveat and silently drops it for the rest.
The CHECK `(state='provisional') = (review_note IS NOT NULL)` makes a caveated "does not apply" unrepresentable; the
verb hides that instead of refusing. Not covered by the test.

### 3. MUST-AMEND - the provisional caveat, the rejection reason and the rejecter are written and read by nothing
Artifact: `165_identity_need_icf.sql`, view `v_lens_crosswalk` column list; `lens_crosswalk` (`SELECT * FROM v_lens_crosswalk`).
- `review_note` is not in the view. `db.py lens-crosswalk --identity ADHD` returned triple 2 as `"state":"provisional"`
  with keys triple_id, identity_code, identity_name, need_code, need_obligation, icf_code, icf_title, state, warrant,
  reviewed_at, reviewed_by, created_by_session. The caveat `cav2` is in the table and on no reading surface.
  "accepted with a caveat held in review_note" (header) names a cell with no reader (CLAUDE.md section 8).
- `retirement_reason`, `retired_by_session`, `retired_at`: the view filters `retired_at IS NULL` and no verb lists
  retired rows. A rejected judgment and its reason are unreachable except by hand SQL.
- On `reject` the required `--reviewed-by` is discarded: `--reviewed-by "OWNERNAME" --session session_2026-12-01-other`
  left row 1 as `state='stated', reviewed_by='the session itself', retired_by_session='session_2026-12-01-other'`.
  Who rejected is not stored. Any session can retire a row the owner stated, with any reason, and the record cannot
  show whether the owner did it. The header's "A row the owner rejects is retired in place" is not what the row says.

### 4. MUST-AMEND - the named reader has no caller, and the judgment reaches no stage that determines anything
Artifact: migration header "READERS: the view v_lens_crosswalk, read by db.py lens-crosswalk"; "They propose; this table judges."
- `git grep -n -E "identity_need_icf|v_lens_crosswalk|lens-crosswalk|lens_crosswalk" -- . ':!transcripts' ':!scratchpad'`
  outside `scripts/db.py`, the migration and the test: `check-registry.yaml` (the test), `context-map.yaml`
  (generated), `owner-browser.yaml` (gloss), `stage-map.yaml`, and T-145 itself. No skill, no `.claude/` command or
  agent, no governance document and none of T-126, T-127, T-128 names any of the three verbs
  (`git grep -l -E "propose-identity-need-icf|review-identity-need-icf"` returns db.py, the migration, T-145).
  The reader is a CLI verb nothing invokes.
- The engine reads the unjudged map: `scripts/assess/assess_cell.py:630-633`
  (`FROM identity_icf_map WHERE identity_code = ? AND retired_at IS NULL`); `add-extraction` / `add-lens-link`
  proposals read `identity_icf_map`, `access_need_icf` and `access_needs.absorbs` (`db.py` near 11622-11661);
  `derivation_handshake_integrity.py:113-116` and `code_value_identity_audit.py:78` read `identity_icf_map`.
  None reads `identity_need_icf`. A triple the owner reviews as `not_applicable` leaves the same identity-ICF pair
  live in `identity_icf_map` and still feeding the function path. The two can disagree and nothing compares them.
- Rule 5: a triple (I, N, C) restates the pair (I, C) that `identity_icf_map` holds (61 rows) and the pair (N, C)
  that `access_need_icf` holds (43 rows), each with its own retire state. With 0 triples this is unproven, not clean.
  The live maps share 2 ICF codes (`select count(distinct icf_code) from identity_icf_map where retired_at is null
  and icf_code in (select icf_code from access_need_icf)`), and 11 of 23 active identities have no map row, so the
  header's "the maps a session reads when it proposes" supplies a single shared code for almost no cell.
- "What is known of only two is a `gaps` row": no verb here writes one, and `gaps` has no warrant, state or review
  columns (critic-8 finding 7, unanswered by this build).

### 5. MUST-AMEND - `--uncovered` and the gloss disagree with the ruling: an unreviewed row counts as coverage
Artifact: `lens_crosswalk` (`NOT IN (SELECT ... FROM identity_need_icf WHERE retired_at IS NULL)`);
`governance/owner-browser.yaml:67` "Only a reviewed link counts."
Run on a fresh copy: one `propose ... --not-applicable` (unreviewed, `reviewed_at` NULL) for ADHD / A-AT / b114, then
`db.py lens-crosswalk --uncovered`: ADHD is absent from `identities_without_a_triple` (22 listed of 23) and A-AT from
`needs_without_a_triple` (16 of 17). One session-written, unreviewed "does not apply" removes an identity and a need
from "the gaps ACTION 3 of the ledger entry says to close". The docstring reads "`not_applicable` was judged and does
not apply" for a row no owner has seen. No reader filters on `reviewed_at`; the gloss sentence is enforced by nothing.

### 6. MUST-AMEND - the test crashes on the first research rows, is not selected by the diff that causes it, and skips the rules it names
Artifact: `scripts/tests/test_identity_need_icf.py`; `governance/check-registry.yaml` entry `test_identity_need_icf`
(`kinds: tooling, schema`; `level: advisory`; `no_floor: selftest`).
- It copies the canonical DB and picks the first two active identities, first need, first two ICF codes
  (ADHD, ALL, A-AT, b114, b117). Run with the copy replaced by a DB holding one live triple ADHD / A-AT / b117:
  `CRASH Refusal propose-identity-need-icf: triple 2 (provisional, ...) already holds this identity, need and ICF code`
  — an uncaught exception, not a FAIL line. `not db.lens_crosswalk(identity=i2)["rows"]` likewise goes false as soon
  as the second identity has any live row. The test is green only while the table is empty, and the data migration
  that fills it is kind `data`, which does not select this check.
- `EXAMINED: 4 case groups` is a string literal; `run_checks.py` reported "examined 4 item(s)" from it. The run
  printed 17 PASS lines.
- Named in the docstring or the verb docstrings and not exercised: a NULL `identity_code` (only need and ICF are
  tried); an unknown identity or ICF code; a deprecated identity; a batch refused whole when one id is bad; a retired
  row refused for review; reject or provisional without a reason at reject; `--dry-run`; the provisional-on-
  not_applicable path of finding 2. "each rule shown to fire and to pass" (line 2) is false for these.
- "nothing but the review verb makes it `stated`" is tested by one schema INSERT with no reviewer. The INSERT with a
  reviewer string succeeds (finding 7) and is not tried.

### 7. MUST-AMEND - "a retired row is never revived" and the reviewed row's content are held by the absence of a verb only
Artifact: `165_identity_need_icf.sql` (no trigger; `select name from sqlite_master where type='trigger'` returns five,
all on `specifications` / `source_value_extractions`, including `trg_sve_retirement_is_final` and
`trg_sve_retired_row_frozen`).
On a copy, each ALLOWED by the schema:
- `UPDATE identity_need_icf SET retired_at=NULL, retired_by_session=NULL, retirement_reason=NULL WHERE triple_id=1` (revived, back in the view as `stated`);
- `UPDATE ... SET warrant='rewritten after review' WHERE triple_id=3` on a stated row (the owner reviewed other words);
- `UPDATE ... SET state='pending', reviewed_at=NULL, reviewed_by=NULL` (a review erased); `SET state='not_applicable'` on a reviewed stated row (the judgment inverted, the review stamp kept);
- `INSERT ... 'stated' ... reviewed_at='', reviewed_by='x', created_at='', created_by_session=''` (empty strings satisfy every NOT NULL and the reviewer CHECK); `retired_at='', retired_by_session=''` likewise.
`emit_batch_sql.py` renders UPDATEs on this table (shown in finding 1), so these shapes travel the sanctioned path.
The header states the rule as a property of the table; the table does not have it.

### Notes
- N1. `db.py lens-crosswalk --identity NOPE` returns `{"rows": [], "count": 0}`, identical to a held identity with no
  judgment. A mistyped code reads as "not yet judged".
- N2. `icf_title` is NULL for 43 of 72 `base_icf` rows (`select count(*), sum(title is null) from base_icf`); the view
  shows a bare code for most ICF coordinates. 4 rows are `is_range`; nothing says whether a range code is a valid
  cube coordinate.
- N3. `--triple-ids` help: "every one must be live and unreviewed" is false for `--decision reject` (a reviewed row
  is accepted, by design). Bad input `1,abc` is answered "names no rows".
- N4. Migration header literals "identity_icf_map (61 rows), access_need_icf (43)" are true today (recomputed: 61, 43)
  and carry no command (rule 7a). "11 of the 23" carries a pointer and recomputes to 11 of 23.
- N5. Ledger entry "(fifth)" says the three messages answered "after an Opus adjudication ... and an antagonist's
  critique". `transcripts/harness_de695d5a/main.jsonl` line 151: "Yes @ T-145" was enqueued 2026-11-20T21:37:58Z;
  the critic transcript is stamped 21:45:27 and the other two messages 23:24:59 and 23:25:14. The first preceded both.
- N6. `retire-identity`'s refusal text names the re-tag routes for figures and map rows only; a live triple now blocks
  retirement (see survived) and the message names no route for it.
- N7. `warrant` holds "a source it rests on ... named here" as prose. The sibling `identity_icf_map` keeps `mechanism`,
  `mapping_confidence`, `provenance` and `notes` as four cells. Whether a source reference inside the warrant cell is
  "each fact in the cell that names it" (owner, 2026-11-06) is the owner's question; the header settles it by citing OD-71.

## What survived
- All or none: `--triple-ids 1,2,999 --decision stated` refused, rc=1, rows 1 and 2 still `pending`.
- `--dry-run` on propose and on review wrote nothing (0 rows; states unchanged).
- A retired row is refused by the verb for both an accept and a reject ("triple 1 is retired").
- A NULL in any key is refused (`NOT NULL constraint failed: identity_need_icf.identity_code`); the FK-OFF migration
  path does not weaken it. Orphan and empty-string keys insert with `foreign_keys=OFF` but `migrate_db.py` re-runs
  `foreign_key_check` inside the transaction and rolls back a new violation (lines 146-170); with FK ON they are refused.
- Capture: `dbcore.writable_tables(conn)` includes `identity_need_icf` (53 tables), not in `NOT_CAPTURED`;
  `emit_batch_sql.py` rendered 4 INSERTs and, separately, 1 UPDATE.
- Deprecated identity: refused at propose with the successor named; `_identity_carriers` returns
  `[('identity_need_icf.identity_code', 3)]`, so `retire-identity` refuses while a live triple names the code (the
  carriers are derived from the FK graph). A deprecated identity with live triples is reachable only by hand SQL.
- View: three inner joins on base tables (`stage-map.yaml`: all four are `base`), crosses no stage; retired rows fall out.
- Rebuild: `migrate_db.py --rebuild` succeeded; user_version 165 = 165; 228 schema objects each side, identical SQL;
  65 tables, 0 count differences; row content differs only in `data_migrations` (`applied_at`, `applied_by_session`, `notes`).
- No triple written: 0 rows, no `sqlite_sequence` entry for the table. Branch is 5 commits ahead of `origin/main`
  and carries only the matrix, the ledger entry and logs.
- The owner's three quoted messages exist as typed in `transcripts/harness_de695d5a/main.jsonl` (lines 151, 239, 249).
- `derived_not_curated_audit.py` reports nothing on the new verbs.

[NULL: bibliographic fields / retrieval-log payloads — no source row or author field is in this diff; nothing to diff]
[NULL: migration_reproducibility subject — had a subject (schema 165 rebuilt); nothing found]
[NULL: joined cells in the new table — 0 rows; unproven, not clean]

```json adversarial-findings
[
  {"lens": "S4-sequence", "subject_table": "identity_need_icf", "subject_key": null,
   "claim_attacked": "only the review verb, run on the owner's review of a batch, sets a row stated",
   "method": "proposed and reviewed in one session on a scratch copy with --reviewed-by 'the session itself', then ran emit_batch_sql.py; the row was emitted as an INSERT already in state stated",
   "artefact": "scripts/db.py review_identity_need_icf", "verdict": "SUSTAINED", "severity": "HIGH"},
  {"lens": "L2-fidelity", "subject_table": "identity_need_icf", "subject_key": "review_note",
   "claim_attacked": "a provisional decision records the reviewer's caveat",
   "method": "reviewed a not_applicable row with --decision provisional --reason; rc=0, output said provisional, review_note stored NULL",
   "artefact": "scripts/db.py review_identity_need_icf", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L1-existence", "subject_table": "identity_need_icf", "subject_key": "review_note, retirement_reason",
   "claim_attacked": "every added object has a named reader (v_lens_crosswalk, lens-crosswalk)",
   "method": "read the view's column list and ran lens-crosswalk on a provisional row; git grep for callers of the three verbs outside db.py, the migration and the task",
   "artefact": "scripts/migrations/165_identity_need_icf.sql view v_lens_crosswalk", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "S1-harm-reached-row", "subject_table": "identity_need_icf", "subject_key": null,
   "claim_attacked": "the maps propose and this table judges",
   "method": "grepped every reader of identity_icf_map and access_need_icf; the engine and the proposal printers read the maps and nothing reads the judged table, so a not_applicable judgment reaches no determination",
   "artefact": "scripts/assess/assess_cell.py lines 630-633", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L3-independence", "subject_table": "identity_need_icf", "subject_key": null,
   "claim_attacked": "the table is not a second home for the pairs in identity_icf_map and access_need_icf (rule 5)",
   "method": "compared key columns and retire states of the three tables; counted shared ICF codes (2) and unmapped identities (11 of 23); 0 triples exist, so the overlap is unproven and not clean",
   "artefact": "scripts/migrations/165_identity_need_icf.sql", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "L7-recognition", "subject_table": "identity_need_icf", "subject_key": null,
   "claim_attacked": "only a reviewed link counts; --uncovered lists the identities and needs still to be judged",
   "method": "wrote one unreviewed not_applicable row on a copy and ran lens-crosswalk --uncovered; the identity and the need left the list",
   "artefact": "governance/owner-browser.yaml line 67", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L6-contrary", "subject_table": null, "subject_key": "test_identity_need_icf",
   "claim_attacked": "the test shows each rule firing and passing and can go red on each defect it names",
   "method": "re-ran it (17 PASS) and re-ran it over a copy holding one live triple for the first identity: uncaught Refusal; listed the named rules with no case; EXAMINED is a literal",
   "artefact": "scripts/tests/test_identity_need_icf.py", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "S3-containment", "subject_table": "identity_need_icf", "subject_key": null,
   "claim_attacked": "a retired row is never revived and a reviewed row is changed only by rejecting it",
   "method": "ran UPDATEs on a copy: un-retire, rewrite the warrant of a stated row, erase a review, flip a reviewed state, empty-string stamps; all allowed; no trigger exists on the table",
   "artefact": "scripts/migrations/165_identity_need_icf.sql", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L8-query-shape", "subject_table": "v_lens_crosswalk", "subject_key": null,
   "claim_attacked": "an empty lens-crosswalk answer means not yet judged",
   "method": "queried an identity code that is not held; the answer is the same empty result as an unjudged identity",
   "artefact": "scripts/db.py lens_crosswalk", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "S2-mismatch-note-vs-payload", "subject_table": null, "subject_key": "Owner statements 2026-11-20 (fifth)",
   "claim_attacked": "the three quoted owner messages answered the coordinator after the adjudication and its critique",
   "method": "read the enqueue lines in the session transcript; the quotes are verbatim, but 'Yes @ T-145' is stamped 21:37:58Z, before the critic transcript of 21:45:27",
   "artefact": "transcripts/harness_de695d5a/main.jsonl line 151", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "S4-sequence", "subject_table": "identity_need_icf", "subject_key": null,
   "claim_attacked": "a review batch is written all or none; a dry run writes nothing; a retired row is not reviewed",
   "method": "ran --triple-ids 1,2,999, both --dry-run paths and both decisions on a retired row on a scratch copy and read the rows back",
   "artefact": "scripts/db.py review_identity_need_icf", "verdict": "SURVIVED"},
  {"lens": "L1-existence", "subject_table": "identity_need_icf", "subject_key": null,
   "claim_attacked": "all three keys are NOT NULL and hold on the FK-OFF migration path; the capture set includes the table; the rebuild reproduces schema 165",
   "method": "NULL and orphan inserts with foreign_keys ON and OFF; read migrate_db.py's in-transaction foreign_key_check; dbcore.writable_tables; migrate_db.py --rebuild and a full object, count and row comparison",
   "artefact": "scripts/migrate_db.py lines 146-170", "verdict": "SURVIVED"},
  {"lens": "L5-population", "subject_table": "base_taxonomy_identity", "subject_key": null,
   "claim_attacked": "a deprecated identity is refused at propose and cannot keep live triples",
   "method": "deprecated an identity on a copy and proposed against it (refused); called _identity_carriers, which returns the live triples and so blocks retire-identity",
   "artefact": "scripts/db.py _identity_carriers", "verdict": "SURVIVED"},
  {"lens": "L4-tier", "subject_table": null, "subject_key": null,
   "claim_attacked": "no claim in this diff assigns a tier or an evidence type",
   "method": "This is a tooling diff with no source, tier or evidence_type written; the lens has no subject here.",
   "artefact": null, "verdict": "NOT-ATTACKED"},
  {"lens": "L2-fidelity", "subject_table": null, "subject_key": "warrant cell holding a source reference in prose",
   "claim_attacked": "one value per cell: a source the warrant rests on is named inside the warrant",
   "method": "Compared with the sibling identity_icf_map, which keeps mechanism, confidence, provenance and notes apart; whether OD-71 licenses a source named in prose is the owner's reading of the 2026-11-06 schema-shape statement.",
   "artefact": null, "verdict": "WITHHELD-FOR-OWNER"}
]
```
