<!-- Recorded from the session scratchpad on 2026-11-06 so that the citations in skills/ and in `db.py coverage` ("owner question N of the 2026-11-06 round-2 adjudication") resolve to a tracked file. Dated record; the counts in it were measured that day. -->

# run-pipeline repair, round 2: adjudication (2026-11-06)

Adjudicator: Fable 5.1 (this session), adjudication only. Branch `ccr-6a40256f-gf1my6`, checkpoint
`41190b6`. No tracked file was edited. Every finding was re-derived against the code and reproduced on
a scratch copy of `data/guidebook.db` (canonical sha256 `b4ab7888…`, unchanged; scratch copies under
`/tmp/claude-0/-home-user-guidebook/908d973d-7650-4b6a-9ab3-eb41dc090acc/scratchpad/adj2/`). Counts below
are measurements of 2026-11-06; re-derive, never quote (rule 7a).

Dispositions: PATCH (tooling, this tooling-only change), OWNER DECISION (not decided here), NO ACTION
(with reason), NOT REPRODUCED. Section 8 order was applied to each: do nothing and say why; change a rule
or convention; reuse what exists; delete the cause; only then the smallest added code.

## 1. Disposition table

| ID | Reproduced | Disposition | Unit | Reason, in one breath |
|---|---|---|---|---|
| R2-1 | yes: marking four languages `scoped-out` on a scratch copy drove `coverage` to `required 0/0, complete true` | PATCH (delete the cause) | M, A | NULL `scope_status` meant "not recorded", so a partial fill emptied the requirement. The one home of "what is owed" becomes one view, `v_research_scope` (map rows not `scoped-out`; NULL is owed), read by `v_coverage_priority` and `coverage`. Required counts pairs, never falls to zero by a partial fill, and `complete` is false on an empty requirement. |
| R2-2 | yes by reading (`db.py` log_search pair refusal) and by data: live `search_executions` hold pairs outside the map (derive: anti-join below) | PATCH (delete the cause) | A | The pair refusal conflates "counts toward the scope" with "may be logged" (R8). Deleted. `--language` is folded to upper case before the map check; `--jurisdiction` keeps the declared vocabulary. A search outside the scope is logged and `coverage` reports it apart. ISO/INT/UN/HR/UG becoming *owed* is data (owner question 5). |
| R2-3 | yes: nine CHECK values all map to BLOCKED; six UNVERIFIED sources carry NULL reason and extractions; no verb sets the column after admission | PATCH (migration + writers + gates) | M, A, C | Only the values whose CHECK comment says the text could not be obtained or read are obstacles; the ledger maps those alone to BLOCKED, below every recorded reading. `superseded` and `no-quantified-claims` are copies of typed facts and the writers refuse them by pointer (CLAUDE.md section 4 shape). `amend-source` sets the column; `record-scan` clears it when a reading lands. The six legacy sources are a data PR. `out-of-scope` / `tier-not-required` go to the owner (question 8). |
| R2-4 | yes: deleting REF-01034's sixth author on a scratch copy; `--verify-authors` printed MALFORMED-PAYLOAD and no cross | PATCH | R | Compare stored rows against the payload's family-named (human) authors even when the payload repeats a name; keep the MALFORMED-PAYLOAD report. CLAUDE.md 5(c) class. |
| R2-5 | yes by reading and data: REF-01034 holds one HTML landing page; `full_text.py` derives from it; `record-scan --text-scope full` checks pages only when markers exist (`page_coverage` returns None for a web page) | PATCH | R, A | A `full` claim is checked against what the document is, and the only machine-knowable statement of that is the source's own logged bibliographic payload: when a held Crossref-shaped payload states a page range (`page`), the document is paged, and a text with no page markers cannot be a full reading of it. No landing-page signatures. A source no deposit describes as paged (a code section page) keeps `full` over its single page. |
| R2-6 | yes by reading: `_require_scoped_verbatim` returns the exemption marker without `_refuse_exempt_with_body`; REF-00992 holds two derived full texts | PATCH (reuse what exists) | A | `observe-term` calls the same helper `add-extraction` already calls. Also found: `decodable_body_artefacts` recognises a derivation only by the `-full-text.txt` suffix, so REF-01019's and REF-01026's derived `-text.txt` bodies are invisible to it; it reads the manifest's `derived` flag instead. |
| R2-7 | yes: `assess_cell.py --slug nope` wrote one specification row on a scratch copy | PATCH | C | `validate_slug` beside `validate_parameter` and `validate_lens`: the slug is the topic the row is recorded under and must exist in `slugs`. |
| R2-8 | yes: parameters 3 and 12 carry a direction with NULL `direction_ref_id`; OR-21 records a direction per lens when a contest first arises; the writer requires one source | OWNER DECISION | — | Doctrinal (question 7). No code change is safe before the answer except none: `lower_is_better` / `higher_is_better` from one source is unaffected; `contested` and the backfill wait. |
| R2-9 | yes by reading: `--ref-id` `required=True` on `add-source` and `add-locator`, refused unless it equals `next_ref_id` | PATCH (derive, as `add-connection --con-id`) | A, P | Optional; omitted, computed; given, must equal the computed id (or, for `add-source`, the id its locator staged). Callers swept below. CLAUDE.md:180 stops listing it as an outstanding violation. |
| R2-10 | yes by reading: `_CONNECTION_ARITY.get(ctype, (None, 0))` passes an unknown type though the comment says it is refused by name | PATCH | A, T | Refuse by name; a test derives the CHECK and asserts every value has an arity row, so the dict cannot silently lag the CHECK. The arity itself is judgment (what a type means), recorded in code, named as such. |
| R2-11 | yes: `add-extraction --help` prints "Live vocabulary, read from the column's own CHECK" and no values for `--claim-type`, `--extraction-method`, `--extraction-status`, `--root-type`, `--measurement-paradigm`; same for `add-candidate --disposition`, `resolve-candidate --disposition`, `add-code-lead --status`, `add-population-match --match-grade`, `update-locator --status` | PATCH (reuse what exists) | A | `choices=dbcore.schema_choices(table, column)` on each; argparse prints the set. `--relation` admits the literal `none`, so its help text carries the derived set instead of `choices=`. |
| R2-12 | yes: `_VALUE_BEARING` does not match "not steeper than" | PATCH | A | The name rule's own regex gains the comparator words (`than`, `at least`, `at most`, `no more`, `no less`, `not exceeding`, `exceed(s|ing)`); help text already says "never a comparator". |
| R2-13 | yes by reading: `ok("R2", "0 citation_mining rows for 0 anchors")` | PATCH | C | On zero anchors print "EXAMINED: 0 tier-1..3 anchors, so this asserts nothing", as R17 does. |
| R2-14 | yes by reading (`:129`, `:353`, `:373`, `:436-438`) | PATCH | T | Derive `CON-0001` from `_next_con_id`, the identity codes from `base_taxonomy_identity`, the domain label as a fixture string, and rewrite G02 against the view. |
| R2-15 | yes by reading: criterion `verified-reading` states three clauses; the check reads one | PATCH (extend the reader) | C | The criterion is the ruling-shaped sentence (OR-11a plus the write-time rules); the reader is the cheaper thing to change and the two other clauses already have live violators (derive: run it). Reader named honestly: the re-reading worklist and the adversarial pass, not the draft render contract. |
| R2-16 | yes: `item_code`, `E-08`, `population_code`, `axis_code` resolve; `DELETE`, `RES`, `FIRED`, `PREDICTED`, `DISCARDED`, `INTEGRATED`, `HIGH-IMPACT` do not; red on 18 files | PATCH (narrow; keep, advisory) | C | Homes from the schema, the verb/flag inventory, check and criterion ids, R-rule ids, skill/command/agent stems and tracked paths only; no audit-script strings, no CLAUDE.md backticks, no module names. No live table has `item_code`, `axis_code` or `population_code`, so they stop resolving with no list. Examined set: backticked tokens only (a value the skill tells the operator to type), not bare capitals in prose. Hand-typed "three skills" sentence deleted. |
| R2-17 | yes: `v_best_practice` is `specifications` filtered; `governing_refs` writer-retired 2026-09-21 and cannot be dropped (twelve committed data migrations INSERT it; derive: `grep -l governing_refs scripts/migrations/data_*.sql`) | PATCH (prose) | P | The skill says the trace is `v_determination_provenance.role` (governing / conditioning / excluded) and that `governing_refs` is frozen history. |
| R2-18 | yes: `architecture/sqlite-data-layer.md:142` `CROSS-ITEM`, `:541` `next-id connections\|gaps\|terms`; `scripts/db.py:20` `--con-id CON-0001`; `:7479` five statuses; `references/connection-reasoning/_template.md:11,36` SPECULATIVE | PATCH (prose) | A (db.py text), P | Rule 4 prose callers. The template is under the attestation regex (`adherence_log_audit.py:81`), so its edit ships with `attestations/connection-reasoning__template.json`. |
| R2-19 | yes: `conflicts` has no `item_code` (`PRAGMA table_info`); CLAUDE.md:433 says it survives; `CAPABILITIES.md` is rendered from `capabilities.yaml` by `build_graph.py` | PATCH (prose) | P | Fix the CLAUDE.md sentence (account in the commit message); fix the `capabilities.yaml` note and re-render. |
| R2-20 | yes for every claim checked: `amend-search --append-note` required; `is-mined --slug`, `log-mining --slug --direction` required; lens flag required (`db.py:8781`); `--result-artefact` is a manifest-relative path checked by `check_artefact_link`; `GUIDEBOOK_RETRIEVAL_LOG` is `LOG_ROOT`; `close-adversarial-pass` refuses an artefact path that resolves to no file; `parameter_declinations.revoked_at` exists; parameters 3 and 12 are the NULL-ref state | PATCH (prose) | P | Each sentence rewritten to match the flag it cites. The `processing_blocked_reason` sentence waits for unit A's verb. |

Settled in round 1 and not reopened: A12, A17, A19, C10, the comparator-alias case (OR-17).

Derivations used above (re-run, do not quote):

```
# live search pairs outside the map
SELECT language, jurisdiction, COUNT(*) FROM search_executions se WHERE NOT EXISTS
  (SELECT 1 FROM lang_jur_map m WHERE m.language = se.language AND m.jurisdiction = se.jurisdiction)
  GROUP BY 1, 2;
# the two jurisdiction homes
python3 - <<'PY'
import sqlite3, sys; sys.path.insert(0, '.'); from schemas.enums import JurisdictionCode
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
m = {r[0] for r in con.execute('SELECT DISTINCT jurisdiction FROM lang_jur_map')}; e = {x.value for x in JurisdictionCode}
print('map-only', sorted(m - e)); print('enum-only', sorted(e - m))
PY
# processing_blocked_reason vocabulary and its comments
python3 -c "import sqlite3,sys; sys.path.insert(0,'scripts'); import dbcore; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); print(sorted(dbcore.check_values(c,'evidence_sources','processing_blocked_reason')))"
grep -n -A10 "processing_blocked_reason IS NULL OR" scripts/migrations/091_remaining_vocabularies_and_rooted_types.sql
# UNVERIFIED sources holding extractions with no reason
SELECT e.ref_id FROM evidence_sources e WHERE e.verification_status <> 'VERIFIED' AND e.processing_blocked_reason IS NULL
  AND EXISTS (SELECT 1 FROM source_value_extractions x WHERE x.ref_id = e.ref_id);
```

## 2. Owner questions

Carried from round 1 (unchanged; numbering kept):

1. **Conflict-matrix identity descriptors** VIS, DBL, OFS, SENS, NEU, IntD, POTS, MCAS, "fibro" are not
   `base_taxonomy_identity` codes. (a) map each to an existing code; (b) add rows; (c) retire the matrix until
   its domains are parameters. Derive the live codes: `SELECT identity_code, display_name FROM base_taxonomy_identity`.
2. **Lens-scoped gathering.** Should a cell keyed on an ICF or access-need lens gather only extractions stated in
   that lens (or crossed to it through `identity_icf_map` / `access_need_icf`)? (a) exact lens; (b) lens or
   crossing; (c) keep as is and say so on the page.
3. **NAMES-NEW terms with no decision** (derive with the query in round 1 section 4.3; today TERM-090 level
   difference, TERM-092 intermediate landing, TERM-093 ramp usability, TERM-094 accessibility audit). Each:
   `add-parameter` or `decline-parameter`.
4. **Follow-up reasons.** The CHECK admits one reason. Extend by migration, or route other doubts to a GAP.
5. **Jurisdiction and language scope: the two homes.** `lang_jur_map` names jurisdictions the declared
   vocabulary `schemas.enums.JurisdictionCode` refuses (derive: the script above; today 17) and lacks some the
   vocabulary declares (today HR, INT, ISO, UG, UN; ISO and EU are in the P1 list of
   `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md`, and live searches are already logged against ISO, INT and
   UN). Options: (a) the enum is the vocabulary: mark the map-only rows `scoped-out` or delete them, and add map
   rows for the owed enum codes; (b) add the map-only codes to the enum; (c) the map becomes the one home and
   the enum reads from it. **Consequence of each:** under (a) and (b) the map stays "what is owed" and the enum
   "what may be logged", and `coverage` can reach `complete` only once no owed row is refused by the enum;
   under (c) a jurisdiction is added in one place. **What this round makes correct without the answer:** the
   requirement no longer collapses on a partial scope fill; a search in any declared jurisdiction is loggable
   whether or not the map pairs it; `coverage` names the owed rows the enum refuses (`jurisdictions_unreachable`)
   and reports `complete: false` while any exist, naming this question. **What waits on it:** which of the 17
   are owed; the map rows for ISO/INT/UN (and HR, UG); the P1+P2+P3 `scope_status` fill (a data PR). A
   sub-question: the research *languages* have no declared home but the map's rows (the 19-language doctrine);
   a search in a twentieth language (one HR-language row exists) is refused by `log-search`. Say whether the
   map's language set is the vocabulary or whether a language column CHECK should declare it.
6. **Conflict domain matrix.** Keep the 12-domain table as a prose seed list, or key conflicts only on
   parameters and retire the domain codes.
7. **Contested direction and the backfill (R2-8).** OR-21 ("Yes, when it first arises") records a direction per
   lens once a contest first arises. The writer now requires `--ref-id` naming one admitted source holding an
   extraction for the parameter, and refuses to restate a direction, so parameters 3 and 12 (direction set,
   `direction_ref_id` NULL; derive: `SELECT parameter_id FROM base_parameters WHERE accessibility_direction IS
   NOT NULL AND direction_ref_id IS NULL`) cannot be backfilled. Options: (a) `contested` is itself a cross-source
   judgment: the writer takes one `--ref-id` per side (two or more), each holding an extraction, and OR-21's
   per-lens direction is a later row per lens on the same column set; (b) `contested` takes no source and the
   per-lens rows carry the sources; (c) keep one source for every value and treat `contested` as the parameter's
   own statement. **Backfill:** (i) a compensating data migration naming the source for 3 and 12, written through
   a new `--backfill-ref-id` path that accepts a ref only where the direction already stands and the ref holds an
   extraction; or (ii) leave NULL as history, as the contract criterion `base-direction-from-source` already
   says. **Safe before the answer:** nothing changes for `lower_is_better` / `higher_is_better` from one source;
   no `contested` direction is written and no backfill is attempted.
8. **NEW. Blocked reasons that are not obstacles.** `processing_blocked_reason` admits `out-of-scope` ("outside
   the corpus this project extracts from") and `tier-not-required` ("tier does not oblige the work"). Neither
   says the text could not be read, and the 2026-10-09 rule says every admitted source is read against the
   whole catalogue. No row carries either value. Options: (a) retire both by migration (a source outside the
   corpus is not admitted; a tier that owes no reading is a doctrine the tier system does not state); (b) keep
   them and let a source carrying one owe no reading (the ledger would show a sixth state, NOT-OWED, and
   `scan_debt` would exclude it); (c) keep them as annotations that exempt nothing. Until answered the ledger
   treats them as NULL (the source owes its reading), which is (c).

## 3. Executor briefs

Common rules for every unit. Edit the working tree only: no commit, no push, no PR. Never write
`data/guidebook.db` except through `scripts/migrate_db.py`. Test on a scratch copy:
`S=<scratchpad>/exec-<unit>; mkdir -p $S; cp data/guidebook.db $S/guidebook.db;` and pass
`GUIDEBOOK_DB_PATH=$S/guidebook.db` inline on every call (the harness resets env between shells). Run
`bash .claude/hooks/ensure-deps.sh` first; never `pip install -r requirements.txt`. No `sqlite3` CLI: read with
`python3` and `file:...?mode=ro`. Hand SQL is allowed on the scratch copy only, to build a fixture state the
sanctioned CLI cannot (say so in the test's comment). Sweep callers with `grep -r` / `git grep`, never the Grep
tool (`.ignore` hides frozen records; frozen records under `_archived/`, `sessions/`, `audits/`, `versions/`,
`workplan/_superseded/` are out of scope and must not be edited). Every vocabulary a message, help text or test
names is derived (`dbcore.check_values`, `dbcore.schema_choices`, a live query), never typed. Every refusal
names the rule and the correct flag, and ends "Nothing was written." Acceptance tests must be shown failing on
the current tree (`git stash` or a copy of the unpatched file) and passing after, and must not type a count, id
or code they could derive. Canadian English in prose (artefact, licence, judgement where the file already uses
it; follow the file's existing spelling of a term). Before finishing, run
`python3 scripts/run_checks.py --changed-from origin/main --explain` and report what went red that was green on
an untouched `origin/main` worktree (a check red on untouched main tells you nothing about your diff).

Order: **M → R → A1 → A2 → T**, with **C** in parallel with R/A1/A2 (after M), then **P**, then **V**. Units that
share a file are sequential and named so below.

### Unit M — migration 123 (sequential; runs first; owns `scripts/migrations/123_*.sql`, `data/guidebook.db` via `migrate_db.py`, `governance/context-map.yaml` regeneration)

Closes: R2-1 (schema half), R2-3 (ledger half). Touch nothing else.

Re-check the highest migration number when you write it (`ls scripts/migrations | grep -E '^[0-9]{3}_' | tail -1`);
this brief assumes 123. Verify `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` is green through the new
version and `python3 scripts/audit/joined_cells_census.py` is unchanged before and after.

1. **`v_research_scope`** (new view): `SELECT language, jurisdiction, role FROM lang_jur_map WHERE
   COALESCE(scope_status, 'in-scope') <> 'scoped-out'`. Header comment: the ONE home of "what is owed"; a NULL
   `scope_status` is owed (an unrecorded scope never shrinks the requirement: on 2026-11-06 marking four
   languages `scoped-out` left every other row NULL and `coverage` read required 0/0, complete true); the fill
   is a data migration after owner question 5.
2. **`v_coverage_priority`** recreated from its live SQL (`SELECT sql FROM sqlite_master WHERE
   name='v_coverage_priority'`) with two changes only: it joins `v_research_scope` instead of `lang_jur_map`, and
   the anti-join compares `UPPER(se.language) = ljm.language` (live rows hold `en`, `fr`, `ja`, `nl`; derive:
   `SELECT language, COUNT(*) FROM search_executions GROUP BY 1`). Readers: `db.py coverage` (unit A1),
   `skills/run-pipeline_SKILL.md`, `skills/research-log-manager_SKILL.md`.
3. **`v_scan_ledger`** recreated with (a) precedence EXTRACTED, STATED-ABSENT, READ-NOTHING-FOUND, READ-PARTIAL,
   BLOCKED, NOT-READ — a recorded reading always outranks a block, because a reading of held bytes proves the
   block lifted (migration 122 ranked BLOCKED above the readings and masked them); (b) BLOCKED only when
   `processing_blocked_reason` is one of the values whose CHECK comment (migration 091 lines ~161-171) says the
   text could not be obtained or read: `no-full-text`, `paywalled`, `no-doi`, `not-indexed`, `language`. State in
   the view comment that this CASE is the one home of that classification (the writers and gates read the
   view's status, never the column), that `no-quantified-claims` and `superseded` are copies of typed facts the
   writers refuse by pointer (unit A1), and that `out-of-scope` / `tier-not-required` are treated as NULL pending
   owner question 8. Keep the rest of the 122 text.
4. `PRAGMA user_version = 123`. Then `python3 scripts/generate/context_map.py` (it lists views; `context_map_fresh`
   is registered) and confirm `--check` is clean.

What it reads / prevents / makes deletable: read by `coverage`, `scan_debt`, `research_batch_dod` R16-scan and
R11-harvest, `verified_scan_integrity`; prevents a requirement that empties on a partial fill and a reading
masked by a stale block; makes `coverage`'s `scope_recorded` branch and `research_batch_dod`'s direct read of the
column deletable (units A1, C).

Acceptance (scratch copy; run the SQL by `python3`): before, with four languages marked `scoped-out` by hand,
`SELECT COUNT(*) FROM v_coverage_priority WHERE slug=<an ACTIVE slug>` equals the count over the whole map
(scope ignored); after, it equals the count over `v_research_scope`. Before, a source given
`processing_blocked_reason='no-full-text'` by hand AND a `text_scope='full'` catalogue scan reads BLOCKED for
its pairs; after, READ-NOTHING-FOUND. Before, `processing_blocked_reason='out-of-scope'` reads BLOCKED; after,
NOT-READ. Assert by comparing counts the test computes from the same scratch copy, never literals. Checks:
`--rebuild`, `joined_cells_census`, `context_map --check`, `run_checks.py --battery db_integrity`.

### Unit R — `scripts/research/retrieval_log.py` (sequential after M, before A1; owns that file only)

Closes: R2-4; the `decodable_body_artefacts` half of R2-6; the helper for R2-5.

1. **R2-4.** In the `--verify-authors` loop, compute `human = [a for a in msg['author'] if a.get('family')]`
   (Crossref deposits a human author with `family`/`given`; the affiliation-as-author entries REF-01034's record
   carries have `name` only). When `repeated_author_name()` fires, still append MALFORMED-PAYLOAD, and ALSO
   compare `stored` against `human` with `_author_conflict`; report a cross when they disagree. When nothing
   repeats, compare as today. Do not weaken the MALFORMED report or `correct-source`'s refusal.
2. **R2-6 helper.** `decodable_body_artefacts` recognises a derived text by the manifest's `derived` flag (carry it
   on `_Artefact`; the index already reads `derived`/`derived_from` at `~:978`), not by the `-full-text.txt`
   suffix. Today REF-01019's and REF-01026's `-text.txt` derivations are invisible to it (derive: call it).
3. **R2-5 helper.** `payload_page_range(ref_id)`: the `page` string of a held Crossref-shaped JSON payload for the
   source (same parse `--verify-authors` uses; manifest records with this `ref_id`), else None. Read by `db.py
   record-scan` (unit A1). Docstring: the deposit is the only machine-knowable statement that the document is
   paged; nothing here curates what a landing page looks like.

What it reads / prevents / makes deletable: reads the logged payloads and manifest already held; prevents a
damaged byline passing behind a malformed deposit (CLAUDE.md 5(c)) and a derived body being treated as absent;
makes the suffix test deletable.

Acceptance: a scratch script that (a) copies the DB, deletes the last `evidence_source_authors` row of a source
whose logged payload repeats a name (derive the source: iterate the session's payloads with
`repeated_author_name`; today REF-01034 in `session_2026-10-30-ramp-spec-pages-rebuild`), runs
`retrieval_log.py --verify-authors --session <that session>` and asserts the source appears both under
MALFORMED-PAYLOAD and in the AUTHORS cross list — fails before, passes after; (b) on the untouched copy the same
source is MALFORMED only; (c) `decodable_body_artefacts` is non-empty for every source whose manifest holds a
`derived: true` text record (derive the set from the manifests); (d) `payload_page_range` returns a non-empty
string for a source whose held payload has `page` and None for one with no payload (derive both from the
manifests). Checks: `run_checks.py --battery tests` (`test_author_presence`, `test_scan_contract`; note
`test_scan_contract` G01/G02 fail identically on `origin/main`).

### Unit A1 — `scripts/db.py`, first pass (sequential after R; owns `scripts/db.py`)

Closes: R2-1 (reader half), R2-2, R2-3 (writers), R2-5 (writer), R2-6 (writer), R2-9 (writers), R2-18 (db.py
text). Also owns the `scripts/db.py` usage header and docstrings.

1. **`get_coverage_completeness`** (R2-1). Delete `scope_recorded` and the `admissible` / `required` branch.
   Required pairs = rows of `v_research_scope`; unsearched pairs = rows of `v_coverage_priority` for the slug;
   searched pairs = required − unsearched. Report: `pairs_required`, `pairs_searched`, `pairs_unsearched`
   (list of `[language, jurisdiction]`), `jurisdictions_required`, `languages_required` (distinct over the
   required pairs), `jurisdictions_searched`, `languages_searched` (as today, over `UPPER(language)`),
   `searches_outside_scope` (non-deferred searches for the slug whose upper-folded pair is not in
   `v_research_scope`), `jurisdictions_unreachable` (required jurisdictions `dbcore.jurisdiction_declared`
   refuses, with the sentence "owed by lang_jur_map, refused by schemas.enums.JurisdictionCode: owner question 5
   of the 2026-11-06 round-2 adjudication"), `searches_deferred_with_reason`, and
   `complete = pairs_required > 0 and not pairs_unsearched`. Keep the unknown-slug refusal. Rewrite the comment
   block so the "48" sentence becomes the command that derives today's figure.
2. **`log_search`** (R2-2). Fold `language` with `.strip().upper()` before any check (and store the folded value).
   Keep the language-in-map refusal (the map is the typed home of the 19-language doctrine; a new language is
   a doctrine change, owner question 5). Delete the (language, jurisdiction) pair refusal and its `_paired`
   query entirely; keep `dbcore.check_jurisdiction`. The result dict gains `in_research_scope: bool` (pair in
   `v_research_scope`), so a search outside the scope is logged and visible, never refused (R8).
3. **`processing_blocked_reason`** (R2-3). (a) `insert_evidence_source` and `amend_source` refuse
   `no-quantified-claims` ("a reading is recorded with `db.py record-scan --text-scope full`; the ledger derives
   READ-NOTHING-FOUND from the reading and the absence of a row, so the reason would be a copy, CLAUDE.md rule
   5") and `superseded` ("the typed home is `evidence_sources.superseded_by_ref_id`, written by `db.py
   supersede-source --ref-id A --by B` (`supersede_source`; confirm the parser name with `grep -n
   'supersede-source' scripts/db.py`)"). Derive the
   two values' presence from the CHECK (`dbcore.check_values`) so the refusal cannot fire on a value the schema
   no longer admits. (b) Add `processing_blocked_reason` to `_AMENDABLE` with the comment that it is a judgement
   about the retrieval ("could not be read, and why") no payload settles; vocabulary via
   `dbcore.check_declared`; the same two refusals apply. (c) `record_scan`: after the row is inserted, if the
   source's pairs read BLOCKED in `v_scan_ledger` before the insert (query the view, never the class list), set
   `processing_blocked_reason = NULL` in the same transaction and return `block_cleared: <old value>`: a reading
   of held bytes is the proof the block lifted; the ledger would already outrank the block (unit M), and leaving
   the reason would be a false statement on the row. (d) The ledger docstring at `record_scan` (R2-18, `:7479`)
   lists the six states in the new precedence.
4. **`record_scan --text-scope full`** (R2-5). After the existing derived-text and page-count checks: when
   `pages_read is None` (no page markers) and `retrieval_log.payload_page_range(ref)` is non-empty, refuse:
   "`--text-scope full` over `<artefact>`, which carries no page markers, but the source's logged bibliographic
   payload states pages `<range>`: the document is paged and this text is not it (a landing page is a record
   about the document, not the document). Retrieve the document (R10; try the Internet Archive on a block,
   CLAUDE.md section 7), derive it with `scripts/research/full_text.py`, and record the reading of that; or
   record this reading as `abstract`/`partial`. Nothing was written." Rule stated in the docstring: a `full`
   claim is checked against what the document is, and the deposit is the only derivable statement of that.
5. **`_require_scoped_verbatim`** (R2-6). In the `exempt_reason` branch, before returning the marker, call
   `_refuse_exempt_with_body(ref_id, field, context)`; the message then names the bodies held. Same helper
   `add-extraction` uses; no second copy.
6. **`--ref-id` derived** (R2-9). `add-locator --ref-id` and `add-source --ref-id` become optional
   (`required=False`, help: "omit it; computed by dbcore.next_ref_id (CLAUDE.md section 4). Given, it must equal
   the computed id" — and for add-source "or the id its own locator staged"). In `insert_locator`: omitted →
   `dbcore.next_ref_id(conn)`; given → must equal it (existing refusal). In `insert_evidence_source`: omitted →
   `dbcore.next_ref_id(conn)`; given → existing rule. The dispatch code passes `args.ref_id` through as None.
   Return the id used (already returned). Usage header line `:25` drops `--ref-id REF-00971`; line `:20` drops
   `--con-id CON-0001` (R2-18). Callers to sweep in THIS unit: `scripts/db.py` only. Other callers are listed
   under units T and P (`skills/run-pipeline_SKILL.md:85,91`, `CLAUDE.md:180`,
   `scripts/tests/test_run_pipeline_refusals.py` I01–I04, `scripts/tests/test_db_amend_writers.py:462,1014,1669`,
   `scripts/tests/test_author_presence.py:69` — the last four keep working because the flag stays accepted; the
   executor of unit T confirms by running them).

What it reads / prevents / makes deletable: reads `v_research_scope`, `v_coverage_priority`, `v_scan_ledger`,
the CHECK vocabularies and the retrieval log; prevents a vacuous coverage pass, an unloggable real search, a
masked reading, a `full` claim over a landing page, a quote from memory on a source whose body is held, and a
hand-typed reference id; makes `scope_recorded`, the pair refusal, the `-full-text.txt` suffix test and
`required=True` on two parsers deletable.

Acceptance: append a section to `scripts/tests/test_run_pipeline_refusals.py` ONLY IF unit T has not started
(it has not: T runs after A2); otherwise hand the cases to T. Cases, each derived from the scratch copy:
coverage required equals `COUNT(*) FROM v_research_scope` and, after marking all but one map row `scoped-out`
by hand, equals 1 (never 0) with `complete` false; `log-search` with a declared jurisdiction the map does not
pair with the language (derive: an enum code absent from the map, or a map jurisdiction with another map
language) is ACCEPTED and reports `in_research_scope: False`; `log-search --language` in lower case lands upper
case; `add-source --processing-blocked-reason no-quantified-claims` and `superseded` are refused naming
`record-scan` / `superseded_by_ref_id`; `amend-source --field processing_blocked_reason --replacement <a value
the view maps to BLOCKED; derive: pick a value, set it by hand on a copy, read the ledger>` lands and the
ledger reads BLOCKED; a `record-scan` on that source clears it and the result says `block_cleared`; a
`record-scan --text-scope full` over a text with no page markers for a source whose payload states a page
range (derive: `payload_page_range`) is refused naming the range, and the same call with `--text-scope
abstract` lands; `record-scan --text-scope full` over a page-less text for a source with NO payload page range
still lands (derive such a source from the manifests; today a code page); `observe-term --verbatim-exempt`
on a source with a decodable body (derive: `decodable_body_artefacts`) is refused naming the body;
`add-locator` with no `--ref-id` lands as `dbcore.next_ref_id`; `add-source` with no `--ref-id` lands as the
next id; a given wrong id is still refused. Checks: `run_checks.py --battery tests`;
`python3 scripts/tests/test_db_amend_writers.py`; `python3 scripts/tests/test_scan_contract.py`.

### Unit A2 — `scripts/db.py`, second pass (sequential after A1; owns `scripts/db.py`)

Closes: R2-10, R2-11, R2-12.

1. **R2-10.** In `insert_connection`, a `connection_type` with no `_CONNECTION_ARITY` row is refused by name:
   "`<type>` is in the CHECK but `add-connection` holds no arity rule for it; a type is added with its rule
   (what it must join), never silently. Nothing was written." Keep the dict; its comment says it is judgement
   (the skill's own test for the type), and unit T's test asserts it covers the CHECK.
2. **R2-11.** `choices=dbcore.schema_choices(<table>, <column>)` on: `add-extraction --claim-type`,
   `--extraction-method`, `--extraction-status`, `--root-type`, `--measurement-paradigm`; `add-candidate
   --disposition`; `resolve-candidate --disposition`; `add-code-lead --status`; `add-population-match
   --match-grade`; `update-locator --status`; `add-locator --status` (`:2293`, no choices today). Derive each
   table/column from the writer's own `dbcore.check_declared(conn, <table>, <column>, …)` call for that flag —
   never guess. `--relation` admits the literal `none`, so instead its help text reads "one of
   {<derived set>} or the literal 'none'" built from `dbcore.schema_choices('extraction_relations','relation')`
   at parser build (None-safe: the DB may be unreadable). Keep each help sentence "Live vocabulary, read from
   the column's own CHECK" — now true, since argparse prints the set. Measure before/after:
   `grep -c 'choices=' scripts/db.py` against `grep -c 'choices=dbcore\.\(schema_choices\|check_values\)' scripts/db.py`
   (report the two commands, not the numbers).
3. **R2-12.** Extend `_VALUE_BEARING` with `\bthan\b|\bat (least|most)\b|\bno (more|less|fewer|greater)\b|\bnot exceeding\b|\bexceed(s|ing)?\b`.
   The refusal already says "a number, a comparator or a min/max word"; make its second sentence name the
   matched word.

What it reads / prevents / makes deletable: reads the CHECKs; prevents an arity-less type landing, an operator
reading "live vocabulary" and finding none, and a comparator phrase minted as a term; makes nothing deletable
(says so).

Acceptance (cases handed to unit T, or appended if T has not started): `add-connection` with a
`connection_type` the CHECK admits but the dict lacks (simulate by monkey-patching `db._CONNECTION_ARITY` to
drop one derived CHECK value in the test) is refused naming the type; every value of the CHECK has a dict row
(derive the CHECK); `db.py add-extraction --help` output contains every value of
`check_values('source_value_extractions','claim_type')` (derive), and likewise for each converted flag;
`add-term --canonical-en "not steeper than"` (and "at least one landing") refused naming the word, while a
plain two-word name passes the regex. Checks: `run_checks.py --battery tests`; `derived_not_curated_audit.py`.

### Unit C — audits, engine, registry (parallel with R/A1/A2, after M; owns `scripts/audit/research_batch_dod.py`, `scripts/audit/scan_debt.py`, `scripts/audit/verified_scan_integrity.py`, `scripts/audit/skill_vocabulary_audit.py`, `scripts/assess/assess_cell.py`, `governance/check-registry.yaml`, `governance/pipeline-contract.yaml`)

Closes: R2-3 (gates), R2-7, R2-13, R2-15, R2-16.

1. **R2-3 gates.** `research_batch_dod` R16-scan and R11-harvest read BLOCKED from `v_scan_ledger`
   (`EXISTS (SELECT 1 FROM v_scan_ledger l WHERE l.ref_id = e.ref_id AND l.status = 'BLOCKED')`), never from
   the column: the view is the one home of which reasons are obstacles (unit M). R11-harvest reports a BLOCKED
   admission apart ("owes no observation until the block clears: nothing of it can be read") instead of failing
   it; R16-scan already reports. `scan_debt.py`'s docstring and the BLOCKED sentence say "a reason the ledger
   classes as an obstacle", not "any reason". Selftest fixtures: a BLOCKED source does not fail R11-harvest or
   R16-scan; one with `out-of-scope` still does.
2. **R2-13.** R2 branch `admitted == 0`: `ok("R2", "EXAMINED: 0 tier-1..3 anchors admitted, so this asserts nothing")`.
   Selftest fixture: the zero-anchor fixture prints that sentence.
3. **R2-7.** `assess_cell.py`: `validate_slug(conn, slug)` refusing a slug not in `slugs` with the sentence "the
   slug is the topic this determination is recorded under (`--slug`); it does not select evidence. Name an
   existing one (`SELECT slug FROM slugs WHERE status IN ('ACTIVE','STUB')`); `db.py` has no slug writer
   (derive: `grep -n 'INSERT INTO slugs' scripts/db.py` is empty), so a new slug is a migration (see how the
   last one landed: `grep -ln 'INSERT INTO slugs' scripts/migrations/*.sql | tail -1`)." Called with the other
   validators, before any write.
4. **R2-15.** `verified_scan_integrity.py` examines every live extraction (source not superseded, parameter
   active) and reports three classes, each with its remedy: VERIFIED-WITHOUT-FULL-READING (as today),
   SOURCE-NOT-VERIFIED (`evidence_sources.verification_status <> 'VERIFIED'`: verify it — `correct-source`,
   `amend-source --field verification_status` — or retire the row through the extraction writers), NO-COVERING-READING
   (no `source_scans` row covers the pair at any scope: `record-scan`). EXAMINED = live extraction rows; FAIL
   when any class is non-empty; print per-class counts and sources. Registry note: reader is the re-reading
   worklist (plan section 7, P3) and the adversarial pass; delete the "render contract (C5)" sentence (a draft is
   not a reader). Contract criterion text unchanged (it already states the three clauses); update its
   `references` to drop C5 if named there.
5. **R2-16.** `skill_vocabulary_audit.py`: `homes()` is rebuilt from, and only from: tables, views, columns,
   `table.column`, CHECK values and view CASE literals (schema); `db.py` verbs (from `--help`) and flags (from
   the parser source); registered check ids; contract stage and criterion ids; R-rule ids; skill, command and
   agent stems; tracked paths and basenames; identity, ICF, access-need, slug, term and gap ids live in their
   registries; `sqlite_master`/`sqlite_sequence`. Delete the audit-script string harvest, the module-level-name
   harvest, the environ harvest, the registry-key harvest and the CLAUDE.md backtick harvest. Examined tokens:
   backticked tokens only (drop the bare ALL-CAPS pattern), still SHAPED and non-placeholder; keep the
   per-file "defines it in its own table" allowance. Docstring states what wrong thing reaches the guidebook
   without it: an operator following a skill that names a retired container or a column that does not exist
   writes the fact into a note cell, which no later stage can join (2026-11-06 ruling on joined cells), or is
   refused by a writer the skill said would accept the value. Advisory stays. Registry note: delete the "three
   skills" sentence; say "red while prior-version skills name retired or non-existent homes (derive: run it)".
   The markers gates read out of note cells (`[UNVERIFIED-QUANT]`, `CO1-NOT-APPLICABLE`, `NOTHING-IN-SCOPE`)
   will now be reported where a skill backticks them; that is correct — they are conventions the 2026-11-06
   ruling queues for typed columns — and the docstring says so.

What it reads / prevents / makes deletable: reads the view, the schema and the inventories; prevents a vacuous
R2 pass, a determination recorded under a slug that does not exist, two of three contract clauses examined by
nothing, and a vocabulary check that cannot go red on `item_code`; makes the gates' direct column reads, the
`-rstrip('s')` allowance (keep only if a derived plural is needed; say which) and five harvest blocks deletable.

Acceptance: `python3 scripts/audit/research_batch_dod.py --selftest` fires R2's asserts-nothing sentence and
the BLOCKED fixtures; `GUIDEBOOK_DB_PATH=$S/guidebook.db python3 scripts/assess/assess_cell.py --parameter-id
<an active parameter> --slug no-such-slug --identity <a live code> --db $S/guidebook.db --emit-sql $S/x.sql
--session s --stamp '2026-11-06 00:00:00'` exits non-zero naming `slugs` and writes no row (count
`specifications` before and after); `verified_scan_integrity.py` on a scratch copy where an extraction row's
source is set `UNVERIFIED` by hand prints SOURCE-NOT-VERIFIED for it, and where its covering scan rows are
deleted by hand prints NO-COVERING-READING; `skill_vocabulary_audit.py --paths <a scratch dir>` over a fixture
file naming `` `item_code` ``, `` `E-08` ``, `` `axis_code` ``, `` `population_code` `` and `` `mode_s_trigger` ``
reports all five, and over a fixture naming a derived live column, a derived CHECK value, a verb from
`--help` and a bare prose word "HIGH-IMPACT" (no backticks) reports none. Before/after on the current tree:
run it and report the per-file residue (derive; do not type). Checks: `run_checks.py --battery governance`,
`--battery db_integrity`, `--selftest`.

### Unit T — `scripts/tests/test_run_pipeline_refusals.py` (sequential after A2 and C; owns that file; also runs, without editing, `test_db_amend_writers.py`, `test_author_presence.py`, `test_scan_contract.py`)

Closes: R2-14; lands every acceptance case units R, A1, A2 and C handed over (one section per unit, named by
the R2 ids it proves).

1. `:129` and `:373`: derive the identity codes (`SELECT identity_code FROM base_taxonomy_identity ORDER BY 1`),
   replace `"LIGHT-INT"` with a fixture label such as `"fixture-domain"` (free-text column; say so), and make the
   "nothing is hard-coded" comment true.
2. `:353`: `expected = db._next_con_id(conn)` read before the call; assert equality.
3. `:436-438` (G02): assert `cov["pairs_required"] == COUNT(*) FROM v_research_scope`,
   `cov["pairs_unsearched"] == COUNT(*) FROM v_coverage_priority WHERE slug=?`, `jurisdictions_unreachable` is
   the list the enum/map anti-join derives, and the all-but-one collapse case from unit A1. No literal `48`,
   no `scope_recorded`.
4. J02 inverts: the pair outside the map is ACCEPTED with `in_research_scope: False`; J01 (`ZZ`) stands; add
   the lower-case folding case.
5. Each new case shows the refusal AND the legitimate shape beside it. Print `EXAMINED: <n cases>`.

Acceptance: the file is red on the unpatched tree (`git stash` the units' edits, run, un-stash) and green
after; `test_db_amend_writers.py`, `test_author_presence.py`, `test_scan_contract.py` unchanged in result from
their `origin/main` state (G01/G02 of `test_scan_contract` pre-exist). Checks: `run_checks.py --battery tests`.

### Unit P — prose (sequential after A2, C and T; owns `skills/run-pipeline_SKILL.md`, `skills/connection-discovery_SKILL.md`, `skills/cross-population-conflict-mapper_SKILL.md`, `architecture/sqlite-data-layer.md`, `CLAUDE.md`, `workplan/pipeline-state-graph/capabilities.yaml` + its rendered outputs, `references/connection-reasoning/_template.md` + `attestations/connection-reasoning__template.json`)

Closes: R2-17, R2-18 (non-db.py), R2-19, R2-20, R2-9 (prose callers), and the prose half of R2-1/2/3/5/6/9/11.

Every sentence that names a flag is checked against `python3 scripts/db.py <verb> --help` after units A1/A2.
Every value named is derived (write the command beside it where the value must appear). ICF codes carry their
names; no bare axis codes, no population umbrellas; every `[A-Z]-NN` code met in the live surface is
prior-version content, never a container; tier and marker words per `governance/tier-system.md`.

- **run-pipeline**: coverage reads `pairs_required` / `pairs_unsearched` / `jurisdictions_unreachable` and
  `complete` is false while any owed row is refused by the declared vocabulary (owner question 5); a search is
  logged in any declared jurisdiction and `in_research_scope` says whether it counts; languages are upper-case
  two-letter codes from `lang_jur_map` (derive: `SELECT DISTINCT language FROM lang_jur_map`); `--ref-id` is
  omitted on `add-locator` and `add-source` (lines 85, 91); the `processing_blocked_reason` paragraph: set at
  admission or with `amend-source --field processing_blocked_reason`, only for a reason the ledger classes as
  an obstacle (derive from `v_scan_ledger`'s SQL), cleared by the reading itself (`record-scan`), never for
  "read, nothing found" (that is the reading plus no row) and never for "superseded" (that is
  `superseded_by_ref_id`); `full` is for a text whose pages are counted, or for a source no deposit describes as
  paged; `--verbatim-exempt` is refused on both `add-extraction` and `observe-term` when a body is held (derive:
  `decodable_body_artefacts`); section 4's "every vocabulary is in `add-extraction --help`" now true and states
  the column each comes from; section 7: `v_determination_provenance.role` is the trace, `governing_refs` is
  frozen history; section 8: `close-adversarial-pass` refuses an artefact path that resolves to no file;
  `amend-search --append-note`; `is-mined --slug`; `log-mining --slug --direction`; a lens flag on
  `add-extraction`; `--result-artefact` is the manifest-relative path `check_artefact_link` accepts (copy its
  docstring sentence); `GUIDEBOOK_RETRIEVAL_LOG` scratch roots must hold the artefacts and apply to
  `record-scan`, `add-extraction`, `observe-term` alike; the NAMES-NEW-neither join filters
  `parameter_declinations.revoked_at IS NULL`; the session record is `sessions/<STEM>.md` plus
  `attestations/<slug>.json` (rule 2, rule 6); a lead met during synthesis is recorded with `log-search
  --origin incidental` (verify the value against the CHECK; derive) or `add-locator`; the stage-6 test text
  names the direction-with-NULL-ref state as history and points at owner question 7.
- **connection-discovery**: `--con-id` omitted; unknown-type refusal; nothing else unless `--help` disagrees.
- **conflict mapper**: the seven descriptors stay marked prior-version (owner question 1); `--parameter-id`.
- **sqlite-data-layer.md**: `:142` the live CHECK set (derive: `check_values('connections','connection_type')`),
  `:541` `next-id connections|gaps|terms|conflicts|ref` as `db.py --help` prints it.
- **CLAUDE.md** `:433`: the sentence becomes "(migration 121 dropped `conflicts.item_code`; `add-conflict` takes
  `--parameter-id`)" — verify with `PRAGMA table_info(conflicts)`; `:180`: remove `add-source --ref-id` from the
  outstanding list, leaving `amend-source --tier`. Put the account of both errors in the commit message, not
  the file.
- **capabilities.yaml** "Connections and conflicts" note: `conflicts.parameter_id` exists (migration 122);
  connection targets are typed columns (migration 120); re-render with `python3
  workplan/pipeline-state-graph/build_graph.py` and inspect the diff (derived documents; report any other
  change it makes).
- **_template.md** `:11,36`: `HIGH | MODERATE` (derive: `check_values('connections','confidence')`), with the
  attestation JSON against `schemas/attestation.schema.json` (copy the shape of the newest file in
  `attestations/`; `attestation_presence` and `attestation_schema` are blocking).

What it reads / prevents / makes deletable: prose callers under rule 4; prevents an operator following a
sentence the writer contradicts; deletes the `scope_recorded`, pair-refusal, `--ref-id`, `mode_s_trigger`,
SPECULATIVE and CROSS-ITEM sentences.

Acceptance: `python3 scripts/audit/skill_vocabulary_audit.py` reports nothing for the three skills (derive the
residue; if any token remains, it must be one owner question 1 holds); every flag the run-pipeline skill names
appears in the corresponding `--help` (script it: extract backticked `--flags` per verb from the skill and check
each against `db.py <verb> --help`); `run_checks.py --changed-from origin/main --explain` with
`attestation_presence`, `attestation_schema`, `claude_md_spine`, `context_map_fresh` green.

### Unit V — independent replay (after P; edits nothing; writes only `<scratchpad>/round2-replay/`)

You are a Sonnet usability reviewer who has not seen this round. On a fresh scratch copy
(`GUIDEBOOK_DB_PATH` inline on every call) and, where a scratch retrieval-log root is needed, a copy of the
held session directories under `GUIDEBOOK_RETRIEVAL_LOG`, replay every PATCH id in both directions through the
CLI as an operator would, and record commands and results only (no interpretation). For each id: the wrong
write, the exact refusal text, whether it names the rule and the correct flag, and the valid write beside it
landing (`dry_run` is acceptable where the fixture is hard). Minimum list:

R2-1 coverage never 0/0 after a partial scope fill (hand-mark on scratch); R2-2 a search in ISO (or any enum
code the map lacks) logs; lower-case language lands upper; R2-3 `add-source --processing-blocked-reason
no-quantified-claims` refused naming `record-scan`; `amend-source` sets `paywalled`; the ledger reads BLOCKED;
`record-scan` clears it; R2-4 the damaged-byline cross appears; R2-5 `full` over a landing-page text refused
naming the page range, `abstract` accepted; `full` over a code page accepted; R2-6 `observe-term
--verbatim-exempt` refused on a bodied source, accepted on a source with only undecodable bytes (the
test's own fixture pattern); R2-7 `assess_cell.py --slug nope` refused, a live slug accepted; R2-9 `add-locator`
and `add-source` without `--ref-id` land on the next id, a wrong id refused; R2-10 an unmapped type refused;
R2-11 `--help` prints the values for each converted flag; R2-12 "not steeper than" refused, "ramp landing"
accepted; R2-13 the zero-anchor R2 line; R2-14 the test passes with no literal id; R2-15 the three classes
print on a doctored copy; R2-16 the five poisoned tokens fail, the prose word does not; then read the three
skills end to end and list every sentence whose flag or value disagrees with `--help` or the schema. Report
plainly; do not claim a result you did not run.

## 4. Data follow-ups (rule 10: their own PR after this tooling lands; not for these units)

- The six UNVERIFIED sources holding extractions (derive: section 1 query). REF-01019 and REF-01026 hold
  derived texts: record their readings (`record-scan`). REF-01002, REF-01013, REF-01014, REF-01016 hold no body:
  set the reason through `amend-source --field processing_blocked_reason` with the value the retrieval log
  justifies, or retrieve them (Wayback first, CLAUDE.md section 7).
- The `scope_status` fill (P1+P2+P3 in scope; Arabic, Bengali, Hindi, Swahili out) after owner question 5.
- Map rows for ISO/INT/UN (and HR, UG) after owner question 5.
- Optional: a compensating data migration folding the lower-case `search_executions.language` rows (the view
  already compares folded; this is tidiness, not correctness).
- Re-grading the legacy `verified` rows (unchanged from round 1).
