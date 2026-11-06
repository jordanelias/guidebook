<!-- Recorded from the session scratchpad on 2026-11-06 so that citations in skills/ and in refusal text ("owner question N of the 2026-11-06 round-3 adjudication") resolve to a tracked file. Dated record; counts in it were measured that day. Supersedes the round-2 file where they differ. -->

# run-pipeline repair, round 3: adjudication (2026-11-06)

Adjudicator: Fable 5.1 (this session), adjudication only. Branch `ccr-6a40256f-gf1my6`, HEAD `bb4fbf9`
(round 2 began at `41190b6`; base `origin/main`). No tracked file was edited. Every finding was re-derived
against the code and, where it is a behaviour, reproduced on a scratch copy of `data/guidebook.db`
(canonical sha256 `8afd9fc3a81f…`, unchanged; scratch under
`/tmp/claude-0/-home-user-guidebook/908d973d-7650-4b6a-9ab3-eb41dc090acc/scratchpad/adj3/`, scratch log root
`adj3/log/`). Counts and ids below are measurements of 2026-11-06; re-derive, never quote (rule 7a).

The rule applied (findings file, "Why a third round"): for each HIGH item, first "do nothing and say why",
then "change a convention", then "reuse", then "delete the cause", and only then the smallest added code,
with an acceptance test that uses the real shapes the reviewers found as well as a synthetic fixture.
Three of the five HIGH items are **removals** of round-2 code; one is a convention change with a small
derivation; one is an owner decision with facts.

## 1. Disposition table

| ID | Reproduced | Disposition | Unit | Ruling, in one breath |
|---|---|---|---|---|
| R3-1 | yes: REF-00988 (holds a derived text, no reading) given `paywalled` by `amend-source` read BLOCKED x8; an `abstract` scan over its HTML returned `block_cleared: paywalled`, the column went NULL and the ledger read READ-PARTIAL x8 (permanent debt). `amend-source` then re-set `paywalled` with the ledger unchanged (R3-21). Blanking the column is refused. | **REMOVE** the clearing; **change the convention** (migration 124 re-ranks the ledger) | M4, A3a, C3, T3, P3 | A block set at admission and a reading are two facts about two things (retrieval; what was read). `record_scan` must not write `evidence_sources` (a judgment-stage verb updating an evidence-stage row, unnamed in round 2). The column is the retrieval record and stays as history; nothing clears it, and `amend-source` may re-describe it. The ledger alone says whether a pair is still blocked, and the sound precedence is derived from what each fact proves: a **full** reading proves the block lifted (READ-NOTHING-FOUND outranks BLOCKED); a partial or abstract reading does not (BLOCKED outranks READ-PARTIAL, and the ledger row still carries that reading's `scan_id` and `text_scope`, so "abstract read, full text paywalled" prints as BLOCKED with the abstract scan beside it: not debt, and the un-read full text is not hidden). Migration 122 put BLOCKED above every reading; 123 put it below every reading; both were guesses. What reaches the guidebook without the clearing: nothing wrong; with it: a source whose full text was never obtained counted as ordinary reading debt forever, and a false NULL on the row. |
| R3-2 | yes: REF-01001 holds one 20-page PDF with a text layer (4509 chars on page 1), `decodable_body_artefacts` is `[]`, and `observe-term --verbatim-exempt` with a fabricated quote landed (`verbatim: exempt`). REF-01005 (170-page microfiche PDF; 166 pages carry an OCR layer that is unreadable, e.g. "Ranp slopes and 'Completton Time"; page renders p0055/p0056/p0162 persisted) accepted; REF-00139 (derived text + page renders p0042/p0046) refused. | **PATCH** (reuse `full_text.py`'s own test; one derivation) | R3, A3a, T3, P3 | "A body that can be decoded" = a fetched `text/*` page, a derived text with text beyond its page markers, or a held PDF on which at least one page yields text under `normalise_quote(page.get_text())`, the exact test `full_text.py` uses to report "NO TEXT LAYER". No file lists. The exemption's one legitimate ground is the sentence the refusal already states: "the pages it comes from persisted first (R10)", i.e. a persisted **page render** (`derivation_kind: page-render`, `scripts/research/page_image.py`). So: accepted when a page render is held for the source or when nothing decodable is held; refused when a decodable body is held and no render is. A PDF this container cannot open (no pymupdf) is reported as unexaminable and the exemption is refused naming the dependency: a gate that cannot examine does not pass. Consequence on the real cases: REF-01001 refused (correct); REF-01005 accepted on its renders (correct); REF-00139 accepted on its renders (changes from round 2's "correctly refused": the renders are the R10 artefact the exemption exists for, and the marker tail now names them so the adversarial pass can check the locator against them). |
| R3-3 | yes, three shapes on the real payloads in a scratch log root: REF-00986 (`page` "103027" = `article-number`) refused `full` over a page-less derived text; REF-01009 (`article-number` "237", no `page`) accepted; and a third shape the reviewers did not name: REF-01002 (no DOI) is refused on pages 789-802 because the Crossref payload bound to it in the manifest is a different paper's (DOI 10.1682/JRRD.2013.07.0168, Gagnon et al.; see R3-20). REF-00985 (`page` "8659", no `article-number` filed) would be refused on a bare number. REF-01034 (109-127) caught. | **REMOVE** `payload_page_range` and the refusal it feeds | R3, A3a, T3, P3 | The inference cannot be made sound: a deposit's `page` says the PDF is paginated, not that an HTML rendering is not the document (a PMC/OA HTML full text of a 109-127 article is a legitimate `full` reading and would stay refused); a bare number is an elocator as often as a page; a payload bound to the wrong ref_id is not the source's own. Narrowing to "a-b ranges on a DOI-matched payload" would still refuse the OA-HTML case. The thing a `full` claim is checked against is what the scan itself can count, `pages_read` against `pages_total`, and that check stays. What reaches the guidebook after removal: a landing page recorded `full` by an operator (REF-01034's original defect) reads READ-NOTHING-FOUND for pairs nobody read; the row carries `pages_read NULL` under `text_scope='full'`, which `scan_debt` now prints as a count ("full, uncounted"), and the adversarial pass reads it. What reached it with the inference: REF-00985 and REF-00986 (two legitimate elocator-paged articles) could never be recorded `full` from any derived text, and REF-01002 could never be recorded `full` from its own PDF because of someone else's deposit, so three sources would carry READ-PARTIAL debt no reading could pay; REF-01009 and REF-01035 were not caught either way. |
| R3-4 | yes: `add-source --ref-id REF-00001` with an unrelated title landed (dry run) while `source_locators.REF-00001` is a DOI-bearing lead on room acoustics; after `add-locator` staged two no-DOI leads as REF-01037 and REF-01038, `add-source` for lead A with the flag omitted landed REF-01039 (orphaning REF-01037) and with `--ref-id REF-01038` (lead B's id) landed under B's id. | **PATCH** (derive the promotion; rule 8) | A3a, T3, P3 | The id is derived from the document's identity, never from the flag. Omitted: if exactly one non-RETIRED staged locator matches the new source (a shared typed identifier equal after folding: `doi` via `norm_doi`, `pmid`, `pmcid`, `isbn`, `standard_number`, `url`; or, when no typed identifier is shared, `retrieval_log._norm_title` equal and no shared identifier unequal), the source lands under that locator's id (a promotion keeps the id `add-locator` minted); none → `next_ref_id`; several → refused naming them. Given: must equal `next_ref_id` or the id of a locator that matches by the same rule; any other staged id is refused naming the lead it is staged for. "Its own locator" when there is no DOI is the locator carrying the same other identifier or the same normalised title. `update-locator --status PROMOTED` follows as today (its own refusal already requires the evidence row). |
| R3-5 | yes (facts in section 2, O-10): `check_0_presence` passes when the attestation file merely exists; `_attestation_path_for` maps one artefact to one file, so a second file "with its own slug" would be an orphan no gate reads; the schema's `reattestation` array is for doctrine-delta re-grounding (`delta_ref`, `materiality`), not artefact edits; `attestations/` is declared append-only by one attestation (DR-2026-08-12) and amended in place by two others (batch 24 ×3, DR-2026-08-19 ×2). | **OWNER DECISION** (O-10) | — (P3 does not write it) | Rule 2 requires an attestation for a touched synthesis path; the gate is satisfied by the stale file, and only a human reads the free text. Options and recommendation in O-10. |
| R3-6 | yes: `STATE-GRAPH.md:375`, `CAPABILITIES.md:69`, `CONFLICTS.md:19,168` print P-X/C3.5/C-035 PASS from the live probe (typed `parameter_id` on `connection_targets` and `conflicts`); `RULINGS.md` R17 says they stay failing by design, overturn = "a second parameter's data and a passing row-level rehearsal"; `capabilities.yaml:98` keeps `C3: NO` beside a note saying the probe reads PASS. | **OWNER DECISION** (O-9) | — | A derived document printing the live probe result is behaving correctly; the ruling record and a hand-kept cell disagree with it. Which of the two moves is the owner's. |
| R3-7 | yes by reading (`verify_authors` :1909-1918: `real` becomes the family-named authors unfiltered for repeats, so a real author filed twice makes the correctly de-duplicated byline cross) and yes on data: REF-01033 crosses on the untouched DB (payload files "Hashizume Tsutomu" in `family` with no `given`; stored family "Hashizume", given "T"). | **PATCH** the duplicate case; **NO ACTION** on given-versus-initial | R3, T3 | When a family-named author repeats, de-duplicate `real` preserving order before comparing, and word MALFORMED as "repeats a name (an affiliation filed as an author, or an author filed twice)". The REF-01033 cross is a true disagreement of form (the deposit's byline is one token; the row asserts a split and an initial); normalising "family carrying the given name" would be guessing which token is the surname. Data follow-up: `correct-source` from the payload, or leave the cross as the honest state. |
| R3-8 | yes by reading: CHECK (9 values, migration 091), view CASE (5), `_BLOCK_REASON_COPIES` (2), test `COPY_HOME` (2, a second home of the writer's judgement); no test covers the CHECK; 091's comments for `no-doi` ("no resolvable identifier for automated paths") and `not-indexed` ("absent from the indexes the pipeline queries") name discovery obstacles, not obstacles to a text in hand. | **PATCH** (one home per fact; coverage test) | M4, T3 | The obstacle classification has one home: `v_scan_ledger`'s CASE (migration 124), whose header names **every** CHECK value with its class. BLOCKED admits `no-full-text`, `paywalled`, `language`. `no-doi` and `not-indexed` join `out-of-scope` and `tier-not-required` as pending owner question 8 (extended), treated as NULL (the source owes its reading) until answered. The copy refusal stays in `db.py` (`_BLOCK_REASON_COPIES`) because it classifies a different fact (restates a typed home) and is judgement named as such; the test imports it (the second home `COPY_HOME` goes). Coverage: a test derives the CHECK and asserts every value occurs as a token in the view's stored SQL (`sqlite_master.sql` keeps the header comment: measured), so a tenth value goes red until the migration that adds it names it. Narrowing the CHECK itself was considered and rejected: it needs a 12-step rebuild of `evidence_sources` for no live row. |
| R3-9 | yes: 86 unresolved tokens in 20 files on HEAD; `--paths skills/run-pipeline_SKILL.md` and `--paths nonexistent_dir` both print `EXAMINED: 0 … PASS`; the "defines it in its own table" allowance is a union over the path set; env vars and tool names fail. | **PATCH** (keep, narrowed) | C3 | Section 8 answer: without it, a skill naming a retired container or a column that does not exist sends an operator to a note cell or a refused write, and rule 4 says prose callers are swept by nothing else; the owner's 2026-11-06 instruction names this. It stays, advisory, with: homes by kind, each derived (schema; verb/flag inventory; check, criterion and R-rule ids; skill/command/agent stems; tracked paths; live registries; **environment variables the code reads**, derived from `os.environ` reads over `scripts/` and `.claude/hooks/`); per-file (not global) own-table allowance; `--paths` taking files or directories and **failing (exit 2) when a path names nothing**; markers the gates read (`CO1-NOT-APPLICABLE`, `NOTHING-IN-SCOPE`, `[UNVERIFIED-QUANT]`) stay reported, as round 2 decided and the docstring says (conventions queued for typed columns); harness tool names (`unsubscribe_pr_activity`) and `db.py` result keys are not vocabulary the operator types and are written in plain text in the skills (P3), which the docstring states under "what is not examined". |
| R3-10 | yes by reading: `UNVERIFIED_REF`/`NOSCAN_REF` `[0][0]` IndexError on an empty selection; `_full_fixture`/`_abstract_fixture` `SystemExit`; `COPY_HOME` restates `_BLOCK_REASON_COPIES`; feature probes exist for two attributes only (`getattr(retrieval_log, "payload_page_range", …)` :747; `db._VALUE_BEARING_NAME` :829 unguarded). | **PATCH** | T3 | Rule rewritten in the file's header: a fixture selector never raises; when the live corpus no longer offers the state it builds the state by hand on the scratch copy (marked HAND) or records the case as SKIPPED-NO-FIXTURE with the reason (a skip is printed, never silent, and counted apart from EXAMINED); every case that depends on a round-2/3 feature is gated by a probe (`hasattr`, a `--help` grep, or a `sqlite_master` query) and records a red case naming the missing feature instead of raising; "red on the old tree" is checked by stashing the unit's edits and running to completion (exit 1, per-case crosses, no traceback). |
| R3-11 | yes: the five live `provisional` rows carry non-NULL `governing_refs` (written 2026-09-16..18, before the 2026-09-21 writer-retire); `validate_evidence_state.py` :294 reads the junction (`dbcore.governing_refs`), while the contract criterion text (`pipeline-contract.yaml` `governing-refs-nonempty`) and `evidence-architecture.md:116,214` still say "non-empty `governing_refs`". | **PATCH** contract text and skill sentence; **OWNER** for the doctrine file (O-11) | C3, P3 | The criterion keeps its id (registry basis refs name it) and its text says what the check reads: at least one `specification_extraction_links` row with role `governing`; `specifications.governing_refs` is frozen history. The skill sentence becomes a derivation ("set on rows written before the writer was retired; derive: `SELECT specification_id FROM specifications WHERE governing_refs IS NOT NULL`"). `evidence-architecture.md` is doctrine: owner. |
| R3-12 | yes: `relate-extraction --help` prints `'named'/'unnamed'/'inferred'` by hand for `--stated` and nothing for `--to-kind` / `--input-role`; `add-extraction` hand-lists five flags' values (equal to the CHECKs today); `adjudicate-term --term-id` help says "Required for NAMES-EXISTING and NAMES-NEW" while :6245 refuses NAMES-NEW. | **PATCH** | A3b | `relate-extraction`'s three flags take `choices=dbcore.schema_choices("extraction_relations", <col>)`. `add-extraction`'s aligned, repeatable flags accept the `-` placeholder (:8681), so they cannot take `choices=`; their help is built from `schema_choices` at parser build like `--relation` (None-safe). `--term-id` help: "Required for NAMES-EXISTING; NAMES-NEW is written only by `add-term --from-observation`, which this verb refuses". The run-pipeline sentence "every vocabulary, each read from its own column" is made true by this and P3 names the column each comes from. |
| R3-13 | yes for every sentence checked: `connection-discovery` rule 2 and `cross-population-conflict-mapper` section 4 name `assess_cell.py` consumption that no file under `scripts/assess/` performs (`grep -rn 'connections\|conflicts' scripts/assess/` hits only the `contested` direction); `research-log-manager` LOG steps 2-3 omit the required `--prior-expectation`; `citation-miner` :304 "REQUIRED" for `--lang-detected` (optional in the parser, :2612), `.schema evidence_sources` (:255, no sqlite3 CLI), `connections_produced` still in its session report (:263); `run-pipeline` :136-137 "reports NOT SEARCHED" (the code prints NOT INGESTED / UNEXAMINABLE). **Not reproduced:** "section 1 ties `v_research_scope` to migration 122": :41's parenthesis attaches to `scope_status`, which migration 122 did add; one clarifying clause is optional. | **PATCH** (delete the consumption sentences; fix the rest) + **O-12** | P3 | A skill describes what the code does. The two consumption sentences are deleted and replaced by the fact (no code reads `connections`, `connection_targets` or `conflicts`; the determination's reader of them is the operator at the adversarial pass; the `contested` direction is the only typed input the engine takes). Whether the engine should consume them is O-12, recorded there and not as a GAP row in a tooling PR. |
| R3-14 | yes: `add-gap --category XX` raises a raw `IntegrityError` (no `choices=`; `gaps.category` has a 12-value CHECK); `add-conflict --pop-a VIS --pop-b MOB` refuses naming `pop_b` because the pair is sorted before `fk_declared` runs, and names neither flag nor how to list codes; `ALL` (row description: "applies to all populations (scope marker)") accepted as a population; `--domain ""` accepted; `log-search` on a MERGED slug accepted (`_check_slug_filable` exists at :9580 and is not called there). | **PATCH** (four one-liners) | A3b, T3 | `--category` takes `choices=dbcore.schema_choices("gaps","category")`; `add-conflict` validates each population under the flag the operator typed before sorting, refuses `ALL` quoting its own `display_name` (the scope marker is not a population: judgement, named), refuses a blank `--domain`; `log-search --slug` goes through `_check_slug_filable`. |
| R3-15 | yes: `log-mining --session session_x.md` stored `session_2026-11-06-adj3.md` in `citation_mining.updated_by_session`; `log-search` would store the same. | **PATCH** (one home) | A3b (`dbcore.py`), C3 (`assess_cell.py`) | `dbcore.audit()` and `upd()` strip a trailing `.md` (every writer stamps through them, `stamp_for` included), with the sentence from CLAUDE.md section 7 as the comment. `assess_cell.py` stamps from its own `SESSION`; the same strip there. |
| R3-16 | yes by reading: `--stamp` is stored verbatim (:2158, :2312); live rows use `YYYY-MM-DD HH:MM:SS` (`specifications`) and `YYYY-MM-DD HH:MM` (`gaps`, `dbcore.now()`). | **PATCH** (one regex) | C3 | Refuse a stamp not matching `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$`, naming `dbcore.now()`'s shape; nothing written. |
| R3-17 | yes: `coverage --slug hearing-impairment-built-environment` (MERGED into `deaf-acoustic-built-environment`) prints `pairs_required 70, pairs_searched 0, pairs_unsearched []`, `complete false`. | **PATCH** (report the status) | A3b | `coverage` reports `slug_status` and `merged_into` from `slugs`; for a slug outside ACTIVE/STUB it adds `owes_searches: false` with the survivor named. `complete` stays false. The view's scope is correct and is not changed. |
| R3-18 | yes by reading: the check scopes to `p.status = 'active'`; the criterion's second clause has no parameter qualifier. | **PATCH** (criterion wording) | C3 | The ledger excludes retired parameters by design (their extractions stay as history), so the check's scope is right and the sentence is wrong: add "on an active parameter" to the criterion. |
| R3-19 | yes for all four | **NO ACTION** (each kept; reasons) | — | `sqlite-data-layer.md:538-543`: `log-mining --connections` and `synonyms` are not in `db.py` (`grep -c '"synonyms"\|--connections' scripts/db.py` is 0 for the flag; `--help` lists no `synonyms`), so the usage block was a prose caller of two retired things (rule 4), correctly swept. `_template.md:12,26,44`: `CROSS-ITEM` and "item_code" are item-layer content in a live template (CLAUDE.md section 7), correctly swept; its attestation is R3-5. `research_batch_dod.selftest` loading views: required, because the gate now reads `v_scan_ledger` and SQLite resolves a view at query time (selftest comment at :1279 says so). `validate_parameters.py` → `_VALUE_BEARING_NAME`: round 2 split the regex into `_VALUE_BEARING` (quotes) and `_VALUE_BEARING_NAME` (names, with comparators); the parameter-name rule is the NAME rule, so the caller sweep was right. |
| R3-20 | partly: the Crossref payload bound to REF-01002 in the manifest (`7f15186320d39a8d.json`, `api.crossref.org/works/10.1682/JRRD.2013.07.0168`) is Gagnon et al. 2013 (789-802), not Vredenburgh et al. 2009 (the stored byline; `pages` 145-158 is consistent with JAPR 26(2)). A mis-bound manifest line, not a pages error. It bears on R3-3 (third shape above). | **NO ACTION** here; data follow-up (section 4) | — | Rebind the manifest line (or drop its `ref_id`) in the data PR; `--verify-authors` cannot see it because REF-01002 has no DOI (UNEXAMINABLE). |
| R3-21 | yes (see R3-1) | folded into R3-1 | — | With the clearing removed and the column defined as the retrieval record, re-describing the reason after a reading is legitimate; the ledger decides. |

Settled in earlier rounds and not reopened: A12, A17, A19, C10, OR-17's comparator alias, `test_scan_contract` G01/G02.
What survived both reviews is not touched (findings file, "What survived"); note that R3-2 changes one of its
sentences deliberately (REF-00139's exemption) and says why.

Derivations used above (re-run, do not quote):

```
# the blocked-reason vocabulary and the view's own text
python3 -c "import sqlite3,sys; sys.path.insert(0,'scripts'); import dbcore; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); print(sorted(dbcore.check_values(c,'evidence_sources','processing_blocked_reason'))); print(c.execute(\"select sql from sqlite_master where name='v_scan_ledger'\").fetchone()[0][:1200])"
# sources holding a PDF with a text layer and no derived text / no page render (R3-2 real shape)
python3 - <<'PY'
import sys; sys.path.insert(0,'scripts/research'); import retrieval_log as rl, sqlite3, pymupdf
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for (r,u) in c.execute("select ref_id,url from evidence_sources"):
    held=rl.artefacts_for_source(r,u); pdfs=[h for h in held if h['exists'] and h['artefact'].endswith('.pdf')]
    renders=[h for h in held if h['derived'] and h['artefact'].endswith('.png')]
    if pdfs and not rl.decodable_body_artefacts(r):
        d=pymupdf.open(str(pdfs[0]['path'])); txt=sum(1 for p in d if rl.normalise_quote(p.get_text()))
        print(r, 'pdf pages', d.page_count, 'with text', txt, 'renders', len(renders))
PY
# payloads whose `page` is an article number, or absent (R3-3 real shapes)
python3 - <<'PY'
import sys,json; sys.path.insert(0,'scripts/research'); import retrieval_log as rl
for a in rl._artefact_index():
    if a.derived or not a.ref_id: continue
    try: m=json.loads(a.path.read_text()).get('message')
    except Exception: continue
    if isinstance(m,dict) and m.get('DOI'): print(a.ref_id, repr(m.get('page')), repr(m.get('article-number')))
PY
# staged no-DOI leads and the high-water mark (R3-4)
python3 scripts/db.py next-id ref; python3 -c "import sqlite3; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); print(c.execute(\"select count(*) from source_locators where coalesce(doi,'')='' and status<>'RETIRED'\").fetchone())"
```

## 2. Owner questions

Questions 1-8 of the round-2 record (`workplan/2026-11-06-run-pipeline-round-2-adjudication.md` section 2)
stand unchanged except 8, which is extended below. In one line each: 1 conflict-matrix descriptors
(VIS, DBL, OFS, …) are not identity codes; 2 lens-scoped gathering; 3 NAMES-NEW terms with no decision;
4 follow-up reasons beyond the one the CHECK admits; 5 the two jurisdiction homes and the language home;
6 the 12-domain conflict table; 7 contested direction and the backfill of parameters 3 and 12.

**8 (extended). Blocked reasons that are not obstacles to a text.** `processing_blocked_reason` admits
`out-of-scope` and `tier-not-required` (round 2) and also `no-doi` ("no resolvable identifier for automated
paths") and `not-indexed` ("absent from the indexes the pipeline queries"): the last two describe discovery,
and a URL-only report admitted without a DOI can be read. No live row carries any of the four (derive:
`SELECT processing_blocked_reason, COUNT(*) FROM evidence_sources GROUP BY 1`). Options: (a) retire all
four by migration (a 12-step rebuild of `evidence_sources`; nothing live needs it); (b) keep them as
annotations that exempt nothing (the ledger treats them as NULL: the source owes its reading); (c) make
`no-doi`/`not-indexed` obstacles after all (then a source whose text is in hand owes no reading, which the
2026-10-09 rule contradicts). **This round implements (b)** in migration 124 and names the four in the
view's header as pending this question. Recommendation: (b) now, (a) when a rebuild is needed for another
reason.

**O-9 (R3-6). RULINGS R17 versus the rendered graph.** Facts: the probe `P-X` passes because migrations
120-122 gave `connection_targets` and `conflicts` a typed `parameter_id`; R17's overturn clause names "a
second parameter's data and a passing row-level rehearsal"; the data half has fired (derive:
`SELECT COUNT(DISTINCT parameter_id) FROM source_value_extractions`), no rehearsal is recorded, and
`capabilities.yaml:98` keeps `C3: NO` beside a note saying the probe passes. Options: (a) ratify the
overturn: append an ACTION to R17 recording the rehearsal (or that the schema half alone suffices) and set
`C3` for that row to `PARTIAL`; (b) keep R17 in force and make the probe assert what R17 means (a
synthesis-stage ROW relating two parameters, not a column that could), so the graph prints FAIL again until
a row exists; (c) leave both and record in R17 why they disagree. Consequences: (a) closes C-035 on a
schema fact with no row behind it; (b) is a `build_graph.py` edit the owner's ruling licenses and keeps the
graph honest about rows; (c) leaves a derived document contradicting a ruling. **Recommendation: (b)**, with
the probe reading `connection_targets`/`conflicts` rows that name two distinct parameters (derive), because
R17's test was always about rows.

**O-10 (R3-5). How the `_template.md` edit is attested.** Facts found: (1) `attestation_presence` passes
when `attestations/connection-reasoning__template.json` exists, whatever it says (`check_0_presence`:
`rel in changed or target.exists()`); no gate reads the free text. (2) The gate maps one artefact to exactly
one attestation path (`_attestation_path_for`), so "a new attestation file with its own slug" would be a
file no check reads: not an option. (3) The schema's only append mechanism, `reattestation[]`, is
re-grounding against a doctrine delta (`delta_ref`, `materiality`, `prior_doctrine_sha`); using it for an
artefact edit would be a false record. (4) Precedent: two attestations have been modified after creation
(`git log --oneline -- attestations/*.json`, count >1: `sessions_session_2026-10-09-research-batch-24-parameter-pilot.json` three times,
`decisions_DR-2026-08-19-research-restart-operative-instrument.json` twice), both edited in place on the
same branch as the artefact's revision; one attestation (`decisions_DR-2026-08-12-specification-curator-rename.json`)
calls the adherence log append-only, in the different context of rewriting *other sessions'* files to a
renamed rule id. The template itself has two commits in its history (the 2026-08-06 path fix and
`bb4fbf9`). So: append-only is asserted by one record and practised by none for a re-touched artefact.
Options: (a) rewrite `connection-reasoning__template.json` for this session (session, doctrine_sha,
per-rule reasons describing the six-line vocabulary edit; verdict CLEAN; git holds the 2026-08-06 record);
(b) revert the template edit and leave the live template offering `SPECULATIVE` and `CROSS-ITEM`, which
the `connections` CHECK no longer admits (an operator copying the template is refused by the writer);
(c) ratify a rule: an attestation file is per artefact and is rewritten by each session that touches the
artefact (the practice), or is append-only with a dated `amendments[]` list (a schema change). **Recommendation:
(a) now under (c)'s first reading**, recorded in the commit message, because the gate's own mapping already
makes the file per-artefact; (b) ships a template that refuses.

**O-11 (R3-11). `governing-refs-nonempty`.** The check already reads the junction; the criterion text and
`governance/evidence-architecture.md:116,214` still say `governing_refs`. This round rewrites the criterion
text (keeping the id) and the skill. Owner: amend the two doctrine sentences to say "at least one governing
link in `specification_extraction_links`" and that the JSON column is frozen history; or leave them with a
note that the column is historical. Recommendation: amend.

**O-12 (R3-13). Downstream consumption the skills asserted.** `connection-discovery` and the conflict
mapper said HIGH connections and the conflict matrix feed `assess_cell.py`; no code does. This round deletes
the sentences and states the fact. Owner: should the engine consume them (a Layer-2 build: conditioning a
cell on a connection or a conflict row), or is the operator at the adversarial pass the reader? If the
former, it is a GAP for a tooling PR, not a skill sentence. Recommendation: operator for now; file the GAP
only if the owner wants the build.

**O-13 (new, from R3-2). The exemption's ground.** This round makes `--verbatim-exempt` acceptable only
when a page render of the source is persisted (R10's "pages persisted") or nothing decodable is held, and
refused when a decodable body (including a PDF with a text layer) is held with no render. Consequence: an
OCR-garbage microfiche needs its page rendered before a quote from it can be ledgered (REF-01005 already
is), and a text-layer PDF must be derived and quoted from. Owner: confirm this reading of R10, or state the
alternative (an operator-asserted exemption with no artefact, which is the round-2 state).

## 3. Executor briefs

Common rules for every unit. Edit the working tree only: no commit, no push, no PR. Never write
`data/guidebook.db` except through `scripts/migrate_db.py`. Test on a scratch copy:
`S=<scratchpad>/exec3-<unit>; mkdir -p $S; cp data/guidebook.db $S/guidebook.db;` and pass
`GUIDEBOOK_DB_PATH=$S/guidebook.db` inline on every call (the harness resets env between shells). Where a
case needs held artefacts, use the tracked `retrieval-log/` read-only (the writers read it; nothing here
writes it) or a scratch `GUIDEBOOK_RETRIEVAL_LOG` root seeded by copying the manifest lines and files of the
sources the case names (the adjudicator's `adj3/log/session_adj3` shows the shape). Run
`bash .claude/hooks/ensure-deps.sh` first; never `pip install -r requirements.txt`. No `sqlite3` CLI: read
with `python3` and `file:...?mode=ro`. Hand SQL is allowed on the scratch copy only, to build a fixture state
the sanctioned CLI cannot (say HAND in the comment). Sweep callers with `grep -r` / `git grep`, never the
Grep tool; frozen records (`_archived/`, `sessions/`, `audits/`, `versions/`, `workplan/_superseded/`,
`transcripts/`) are out of scope and must not be edited. Every vocabulary a message, help text or test names
is derived (`dbcore.check_values`, `dbcore.schema_choices`, a live query), never typed; ICF codes carry their
names; no bare axis codes, no population umbrellas; every `[A-Z]-NN` code met in the live surface is
prior-version content, never a container; tier and marker words per `governance/tier-system.md`. Every
refusal names the rule and the correct flag and ends "Nothing was written." Acceptance tests are shown
failing on the current tree (`git stash` the unit's edits, run, un-stash) and passing after, must exercise
the REAL shapes named below (derived from the DB and the manifests, never typed ids) as well as a synthetic
fixture, and must not go red on legitimate future data (a selector that finds no live example builds one or
records SKIPPED-NO-FIXTURE; it never raises). Canadian English in prose (artefact, licence, judgement where
the file already uses it). Before finishing, run `python3 scripts/run_checks.py --changed-from origin/main
--explain` and report what went red that is green on an untouched `origin/main` worktree. Each unit's report
names: the ids it closes, what the added code reads, what wrong thing it prevents, what it makes deletable,
and the two measurements `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'`
before and after.

Order: **M4 → R3 → A3a → A3b → T3**, with **C3** in parallel with R3/A3a/A3b (after M4), then **P3**, then
**V3**, then **AD3**. Units sharing a file run in sequence and are named so.

### Unit M4 — migration 124 (sequential; runs first; owns `scripts/migrations/124_*.sql`, `data/guidebook.db` via `migrate_db.py`, `governance/context-map.yaml` regeneration)

Closes: R3-1 (ledger half), R3-8 (the one home). Touch nothing else.

Re-check the highest migration number when you write it (`ls scripts/migrations | grep -E '^[0-9]{3}_' | tail -1`);
this brief assumes 124. Verify `python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db` is green through
the new version and byte-identical to the migrated canonical copy, and that
`python3 scripts/audit/joined_cells_census.py` is unchanged before and after.

1. `DROP VIEW v_scan_ledger; CREATE VIEW v_scan_ledger AS …` recreated from the live SQL
   (`SELECT sql FROM sqlite_master WHERE name='v_scan_ledger'`) with exactly these changes:
   (a) **precedence** EXTRACTED, STATED-ABSENT, READ-NOTHING-FOUND, **BLOCKED**, READ-PARTIAL, NOT-READ. The
   header states the derivation: a full reading proves the obstacle is gone (the whole text was read), so it
   outranks a block; a partial, fragment or abstract reading does not prove the full text obtainable, so
   under a standing obstacle the pair is BLOCKED and not reading debt, and the row still names that
   reading in `scan_id`/`text_scope`/`method` (the LEFT JOIN is unchanged), so "abstract read, full text
   paywalled" is visible as both facts. Say that 122 ranked BLOCKED above every reading and 123 below every
   reading, and that this order is the one derived from what each fact proves. (b) **BLOCKED admits**
   `no-full-text`, `paywalled`, `language`. (c) The header is the ONE HOME of the classification and names
   **every** value of the CHECK (derive the list with `dbcore.check_values` when writing it, and re-derive
   it in the acceptance test) under one of three heads: obstacle to the text (the three above); a copy of a
   typed fact the writers refuse by pointer (`no-quantified-claims` → a recorded full reading;
   `superseded` → `superseded_by_ref_id`; the judgement lives in `db.py _BLOCK_REASON_COPIES`); pending
   owner question 8 of the round-3 adjudication, treated as NULL (`out-of-scope`, `tier-not-required`,
   `no-doi`, `not-indexed`), with the one-line reason for the last two (migration 091's own comments
   describe discovery, not a text in hand). Each value appears as a bare token in the header so the T3
   coverage test can find it. (d) State that nothing clears the column: it is the retrieval record and
   stays as history; the writers and gates read this view's status, never the column.
2. `PRAGMA user_version = 124`. Then `python3 scripts/generate/context_map.py` and confirm `--check` is clean.

What it reads / prevents / makes deletable: read by `scan_debt`, `research_batch_dod` R16-scan and
R11-harvest, `record_scan`'s docstring and `db.py` help; prevents a partially read, still-blocked source
being counted as ordinary debt and a full reading being masked by a stale reason; makes `record_scan`'s
UPDATE of `evidence_sources` deletable (A3a).

Acceptance (scratch copy; SQL by `python3`; assert by counts the test computes, never literals): pick, from the
copy, a source with no reading and a derived text held (derive; today REF-00988) — HAND set
`processing_blocked_reason='paywalled'`; before, with a HAND `source_scans` row at `text_scope='abstract'`
(`mode='catalogue'`, `catalogue_version` = `MAX(parameter_id)`, any held sha), its pairs read READ-PARTIAL;
after, BLOCKED with `scan_id` = that row and `text_scope='abstract'`; with the row changed to `'full'`,
READ-NOTHING-FOUND both before and after. For each CHECK value set on an unread source, the status is BLOCKED
iff the value is one of the three obstacles (derive the three from the view's SQL, not from this brief).
Checks: `--rebuild`, `joined_cells_census`, `context_map --check`, `run_checks.py --battery db_integrity`.

### Unit R3 — `scripts/research/retrieval_log.py` (sequential after M4, before A3a; owns that file only)

Closes: R3-2 (helper), R3-3 (deletion), R3-7 (duplicate author).

1. **R3-3.** Delete `payload_page_range` (its only reader is `record_scan`, deleted in A3a; its only test is
   T3's R01/F01/F02, rewritten there; `grep -rn payload_page_range --include=*.py --include=*.md .` must be
   empty after T3 and P3).
2. **R3-2.** `decodable_body_artefacts(ref_id)` returns the held artefacts that carry a decodable BODY: a
   fetched `text/*` page (as today); a derived text whose text with `PAGE_MARKER` lines removed normalises
   to non-empty (a scan-only PDF's derivation is markers only, and is not a body); a held `.pdf` on which at
   least one page's `normalise_quote(page.get_text())` is non-empty under pymupdf (the same test
   `full_text.pdf_text` uses for its `empty` list; do not import `full_text`, factor the one-page test into a
   `pdf_text_pages(path)` helper beside `pdf_page_count` that `full_text.py` can call later). When pymupdf
   cannot be imported, a `.pdf` is returned with the suffix ` (unexaminable: pymupdf missing)` so the caller
   refuses naming the dependency rather than passing. Add `page_render_artefacts(ref_id)`: the held derived
   artefacts whose manifest `derivation_kind` is `page-render` (the kind `page_image.py` records: derive it
   from that script, never type a file extension). Docstrings state the rule: the exemption is for a quote
   read off a persisted page image or from a source holding nothing decodable; nothing here curates file lists.
3. **R3-7.** In `verify_authors`, when `repeated_author_name` fires, build `real` from the family-named
   authors **de-duplicated in order** (key `_norm(family)|_norm(given)`), so an author the deposit filed
   twice compares as one against a correctly stored byline; keep the MALFORMED report; its sentence becomes
   "whose payload repeats a name; a byline never does, so the deposit filed an affiliation as an author, or
   an author twice". Do not touch `_author_conflict` or the given-name rule (R3-7's second half is NO ACTION).

What it reads / prevents / makes deletable: reads the manifests and held bytes already persisted; prevents a
fabricated quote behind the exemption on a text-layer PDF (CLAUDE.md 5(c)), a `full` claim refused on
another document's deposit, and a cross printed over a correct byline; deletes `payload_page_range`.

Acceptance (a scratch script; derive every source): (a) for every source holding a `.pdf` and no derived
text (derive from the manifests), `decodable_body_artefacts` is non-empty iff pymupdf finds text on at least
one page (today REF-01001 non-empty; a source whose PDF has no text on any page, if one exists, empty — if
none exists, build one: a one-page PDF with no text via pymupdf in a scratch log root); (b) for a source with
persisted page renders (derive; today REF-01005, REF-00139) `page_render_artefacts` lists them and nothing
else; (c) a derived text of markers only (fixture) is not a body; (d) `verify_authors` on a copy where a
source's payload lists a real author twice (fixture payload in a scratch log root, built from a real
payload's shape) prints MALFORMED and no cross when the stored byline is de-duplicated, and a cross when a
stored row is deleted — fails before on the first half, passes after; (e) `payload_page_range` is absent.
Checks: `run_checks.py --battery tests` (`test_author_presence`, `test_scan_contract`; G01/G02 pre-exist).

### Unit A3a — `scripts/db.py`, first pass (sequential after R3; owns `scripts/db.py`)

Closes: R3-1 (writer), R3-2 (writer), R3-3 (writer), R3-4, R3-21.

1. **R3-1 / R3-21.** In `record_scan`: delete the `_blocked`/`_old_block` reads, the `UPDATE evidence_sources`
   and `block_cleared` (the verb writes `source_scans` only). Docstring: the six states in the migration-124
   precedence; "nothing clears `processing_blocked_reason`: it is the retrieval record; a full reading
   outranks it in `v_scan_ledger`, a partial one does not, and `amend-source` re-describes it". The
   `add-source --processing-blocked-reason` help loses "A reading clears it (record-scan)" and says "a full
   reading outranks it in v_scan_ledger; the column stays as the retrieval record". `_AMENDABLE`'s comment
   loses "It is cleared by `record-scan`, never here".
2. **R3-3.** Delete the `_range` refusal block in `record_scan` and the two docstring paragraphs about the
   deposit; keep the fetched-file refusal and the `pages_read < pages_total` refusal. The result dict already
   carries `pages_read`; when `text_scope == 'full'` and `pages_read is None`, add `"uncounted": True` so the
   operator sees that nothing here counted the claim (one key, no prose).
3. **R3-2.** `_refuse_exempt_with_body(ref_id, field, context)`: `bodies = decodable_body_artefacts(ref_id)`;
   `renders = page_render_artefacts(ref_id)`; if `renders`: return a tail string naming them (`" (page renders
   held: a; b)"`) which `_require_scoped_verbatim` and `add-extraction`'s caller append to the marker via
   `exempt_marker(reason, tail)`; elif `bodies`: refuse as today, and when any body carries
   `(unexaminable: pymupdf missing)` say "cannot examine the PDF's text layer here: run
   .claude/hooks/ensure-deps.sh"; else return `""`. All three callers (`_require_scoped_verbatim` for
   observe-term, the `add-extraction` exemption path, and the `--quote` exemption on relations; derive:
   `grep -n '_refuse_exempt_with_body' scripts/db.py`) use the returned tail; no second copy of the rule.
4. **R3-4.** In `insert_evidence_source`, replace the "next id or ANY staged id" rule: compute
   `_matches = _staged_locators_matching(conn, data)` — non-RETIRED `source_locators` rows where a typed
   identifier both carry is equal after folding (`doi` via `dbcore.norm_doi`; `pmid`, `pmcid`, `isbn`,
   `standard_number` stripped; `url` stripped, lower-cased, trailing slash dropped), or, when no typed
   identifier is shared, `retrieval_log._norm_title(locator.title) == _norm_title(pub_title)` and no shared
   identifier differs. Omitted `--ref-id`: one match → its id (promotion); none → `next_ref_id`; several →
   refuse naming them. Given: must equal `next_ref_id` or a match's id; otherwise refuse, and when it equals a
   non-matching staged id say "`REF-NNNNN` is staged for '<that lead's title>' (source_locators), not for
   this source; a promotion keeps its own lead's id and nothing else does". Help text on `--ref-id`: "omit it:
   computed — the next id, or the id of the staged locator this source matches (same DOI, pmid, pmcid, isbn,
   standard number or URL; else the same title)". The DOI-duplicate refusal stays.

What it reads / prevents / makes deletable: reads the ledger, the manifests, `source_locators`; prevents
a judgment-stage verb falsifying an evidence-stage row, a `full` claim refused on someone else's deposit,
a quote from memory behind the exemption on a text-layer PDF, and two identities for one document; deletes
the cross-stage UPDATE, the page-range refusal, and the any-staged-id branch.

Acceptance (cases handed to T3): `record-scan` on a blocked source leaves the column as it was and the
ledger reads BLOCKED with that scan beside it; `full` over a page-less derived text for a source whose
payload's `page` equals its `article-number` (derive; today REF-00986) lands with `uncounted: true` in a
scratch log root; `observe-term --verbatim-exempt` on a source holding one text-layer PDF and no render
(derive; today REF-01001) is refused naming the PDF; on a source holding renders (derive; today REF-01005)
accepted with the renders in the marker tail; `add-source` with no `--ref-id` after `add-locator` staged a
no-DOI lead with the same title lands on the lead's id; with the other lead's id refused naming that lead's
title; with `--ref-id REF-00001` and an unrelated title refused; with no match lands on `next_ref_id`.
Checks: `python3 scripts/tests/test_db_amend_writers.py`; `python3 scripts/tests/test_scan_contract.py`.

### Unit A3b — `scripts/db.py` second pass and `scripts/dbcore.py` (sequential after A3a; owns both files)

Closes: R3-12, R3-14, R3-15 (dbcore half), R3-17.

1. **R3-12.** `relate-extraction --to-kind/--stated/--input-role`: `choices=dbcore.schema_choices("extraction_relations", <col>)`
   (confirm the table/column from the writer's own `check_declared` calls). `add-extraction`'s aligned
   `--to-kind/--stated/--input-role` keep the `-` placeholder, so their help is built at parser build from
   `schema_choices` ("one of {derived} or '-'"), None-safe, as `--relation` is; delete the hand-typed lists.
   `adjudicate-term --term-id` help: "Required for NAMES-EXISTING; NAMES-NEW is written only by `add-term
   --from-observation` and this verb refuses it".
2. **R3-14.** `add-gap --category`: `choices=dbcore.schema_choices("gaps", "category")`. `insert_conflict`:
   before sorting, `fk_declared` each population with the context `add-conflict --pop-a` / `--pop-b`, the
   remedy "`SELECT identity_code, display_name FROM base_taxonomy_identity`"; refuse `ALL` quoting the row's
   own `display_name` (derive it) — "a scope marker, not a population" (judgement, named); refuse a blank
   `--domain` after `strip()`. `log_search`: call `_check_slug_filable(conn, slug)` when a slug is given (the
   refusal already names `merged_into`).
3. **R3-15.** `dbcore.audit()` and `upd()` strip a trailing `.md` from `session` (one home; `stamp_for` goes
   through `audit`), comment citing CLAUDE.md section 7 ("bare stem in the DB, `.md` in pointers").
4. **R3-17.** `get_coverage_completeness` adds `slug_status` and `merged_into` from `slugs`; when the status
   is outside ACTIVE/STUB, `owes_searches: false` and `complete: false` (unchanged), with `merged_into` naming
   the survivor.

Measure before/after and report the two commands (not the numbers): `grep -c 'choices=' scripts/db.py`
against `grep -c 'choices=dbcore\.\(schema_choices\|check_values\)' scripts/db.py`.

What it reads / prevents / makes deletable: reads the CHECKs and `slugs`; prevents a raw IntegrityError, a
refusal naming the wrong flag, a scope marker filed as a population, a search logged under a folded slug, a
`.md` session stem scoping a gate to nothing, and a coverage report that reads as "nothing owed, nothing
searched"; deletes three hand-typed value lists.

Acceptance (handed to T3): `add-gap --category <a value not in the CHECK>` is refused by argparse naming
the live values; `add-conflict --pop-a <unknown> --pop-b <live>` names `--pop-a`; `--pop-a ALL` refused
quoting the display name; `--domain " "` refused; `log-search --slug <a MERGED slug; derive>` refused naming
`merged_into`; `log-mining --session x.md` stores `x`; `coverage` on the MERGED slug reports
`slug_status: MERGED`, `owes_searches: false`; `relate-extraction --help` prints the three derived sets.

### Unit C3 — audits, engine, registry, contract (parallel with R3/A3a/A3b after M4; owns `scripts/audit/scan_debt.py`, `scripts/audit/research_batch_dod.py`, `scripts/audit/skill_vocabulary_audit.py`, `scripts/assess/assess_cell.py`, `governance/check-registry.yaml`, `governance/pipeline-contract.yaml`)

Closes: R3-1 (gates), R3-9, R3-11 (contract), R3-15 (assess half), R3-16, R3-18.

1. **R3-1 gates.** `scan_debt.py`: DEBT unchanged (NOT-READ + READ-PARTIAL); print BLOCKED pairs apart with a
   breakdown by covering reading (`text_scope` NULL / abstract / partial / fragment) so "blocked, abstract
   read" is visible; and print the count of `source_scans` rows with `text_scope='full' AND pages_read IS
   NULL` as "full readings nothing counted" (the operator's claim, named). `research_batch_dod` R11-harvest:
   the BLOCKED exemption applies only to admissions whose every ledger row has `scan_id IS NULL` (nothing of
   it was read); an admission read at abstract scope under a block still owes its observations. R16-scan:
   unchanged in effect (a BLOCKED source with an abstract catalogue reading has a catalogue reading); make the
   comment say so. Selftest fixtures: a BLOCKED-with-abstract-reading admission with no observation fails
   R11-harvest; one with no reading at all is reported.
2. **R3-9.** `skill_vocabulary_audit.py`: `homes()` gains environment variables the code reads, derived by
   regex over `scripts/**/*.py` and `.claude/hooks/*` for `os.environ.get("X")` / `os.environ["X"]` /
   `environ.get("X")`; the own-table allowance becomes per file; `--paths` accepts files and directories and
   exits 2 naming any path that matches nothing (a pass that examined nothing is the defect this project
   names); the docstring's "WHAT IS NOT EXAMINED" lists: fenced blocks, plain-text tokens, harness tool names,
   `db.py` result keys, and the gate markers (reported by decision, round 2). Registry note: the count is
   derived (`run it`), never stated. Keep the five poisoned-token test behaviour (E09/E10 in T3).
3. **R3-11.** `pipeline-contract.yaml` `governing-refs-nonempty`: keep the id; criterion text: "No `stated` or
   `provisional` determination without at least one `specification_extraction_links` row with role
   `governing` (anti-hallucination); `specifications.governing_refs` is frozen history the writer no longer
   sets (writer-retired 2026-09-21)"; references unchanged plus `validate_evidence_state.py`'s own comment.
   Run `run_checks.py --selftest` (basis refs).
4. **R3-15.** `assess_cell.py`: strip a trailing `.md` from `--session` where `SESSION` is set.
5. **R3-16.** `assess_cell.py`: refuse `--stamp` not matching `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$`,
   naming `dbcore.now()`'s shape; nothing written (before any write; exit 2).
6. **R3-18.** `verified-reading` criterion: "… and no extraction **on an active parameter** exists for a
   source that is not VERIFIED or for a (source, parameter) no reading covers" (retired parameters' rows are
   history, as the ledger says).

What it reads / prevents / makes deletable: reads the view, the code's own environ reads, `slugs`;
prevents a vacuous vocabulary pass, a partially read blocked source excused from harvest, a stamp in a
foreign shape, a criterion wider than its check; deletes the global own-table union.

Acceptance: `skill_vocabulary_audit.py --paths skills/run-pipeline_SKILL.md` examines ≥1 file;
`--paths no-such-dir` exits 2; a fixture dir with two files, one defining `` `item_code` `` in a table and
the other naming `` `item_code` `` in prose, reports it for the second only; a fixture naming
`` `GUIDEBOOK_RETRIEVAL_LOG` `` reports nothing (derive that the code reads it);
`research_batch_dod.py --selftest` fires the new fixtures; `assess_cell.py --stamp 2026-11-06T00:00:00Z`
exits non-zero naming the shape and writes no row (count `specifications` before/after on a scratch copy);
`scan_debt.py` prints the BLOCKED breakdown on a copy with a HAND blocked+abstract source; checks:
`run_checks.py --battery governance`, `--battery db_integrity`, `--selftest`.

### Unit T3 — `scripts/tests/test_run_pipeline_refusals.py` (sequential after A3b and C3; owns that file; runs, without editing, `test_db_amend_writers.py`, `test_author_presence.py`, `test_scan_contract.py`)

Closes: R3-10, R3-8 (coverage test); lands every case R3, A3a, A3b and C3 handed over.

1. **R3-10 rule, in the header and in the code.** Selectors never raise: `_full_fixture`, `_abstract_fixture`,
   `UNVERIFIED_REF`, `NOSCAN_REF`, `read_ref`, `unread_ref` and every `[0][0]` become functions that return
   the live example or build one by HAND on the scratch copy (an UNVERIFIED source: HAND-flip one; a source
   with no scan: HAND-delete its scans on the copy; a full reading with a quotable derived text: a fixture
   text in a scratch log root with `[PDF page 1 of 1]` and a figure) or record `SKIPPED-NO-FIXTURE: <why>`
   (printed, counted apart from EXAMINED, never silent). `COPY_HOME` goes; use `db._BLOCK_REASON_COPIES`.
   Every case depending on a round-2/3 feature is gated by a probe (`hasattr(retrieval_log,
   "page_render_artefacts")`, `"uncounted"` in the result, a `sqlite_master` read of the view's SQL,
   `--help` text) and records a red case naming the feature when it is absent. Verify "red on the old tree"
   per case: stash every unit's edits, run, confirm exit 1 with per-case crosses and no traceback, un-stash.
2. **R3-8 coverage.** Derive `check_values(evidence_sources, processing_blocked_reason)`; read
   `v_scan_ledger`'s SQL from `sqlite_master`; assert each value occurs as a bare token in it; assert the
   BLOCKED `IN (…)` list ⊆ CHECK; W02 becomes "a full reading or an extraction outranks a block; a partial
   reading does not" (both directions, by HAND rows); W03 asserts the obstacle set equals the view's IN list
   and excludes `_BLOCK_REASON_COPIES`.
3. Land A3a's, A3b's, R3's and C3's cases (one section per unit, named by the R3 ids). Remove R01/F01/F02,
   `PAGES`, `PAGED_REF`/`PLAIN_REF`; replace with the real-shape cases: the elocator-paged source (derive by
   the payload scan in section 1) lands `full` over a page-less derived text in a scratch log root with
   `uncounted: true`; the exemption cases on the derived PDF-with-text / renders sources; the `add-source`
   promotion cases with two staged no-DOI leads of distinct titles. Print `EXAMINED: <n cases>` and
   `SKIPPED-NO-FIXTURE: <n>`.

Acceptance: green on the patched tree; red per case with the edits stashed; the three sibling test files
unchanged in result from `origin/main` (G01/G02 pre-exist). Checks: `run_checks.py --battery tests`.

### Unit P3 — prose (sequential after A3b, C3 and T3; owns `skills/run-pipeline_SKILL.md`, `skills/connection-discovery_SKILL.md`, `skills/cross-population-conflict-mapper_SKILL.md`, `skills/research-log-manager_SKILL.md`, `skills/citation-miner_SKILL.md`)

Closes: R3-13, the prose halves of R3-1/2/3/4/9/11/12/14. Does NOT touch `references/connection-reasoning/_template.md`
or `attestations/` (O-10 is the owner's).

Every sentence naming a flag is checked against `python3 scripts/db.py <verb> --help` after A3b; every value
named is derived (write the command beside it where the value must appear).

- **run-pipeline**: the `processing_blocked_reason` paragraph (:113-124): set at admission or by
  `amend-source`, only for a reason the ledger's BLOCKED case names (derive from the view's SQL); nothing
  clears it; a full reading outranks it, a partial one does not (the pair reads BLOCKED with the reading
  beside it: not debt); "abstract read, full text paywalled" is recorded as the abstract reading plus the
  reason, and the full text is still owed when obtainable (Wayback first, section 7). The `full` paragraph
  (:146-149): `full` is refused over a fetched file and over fewer pages than held; over a page-less derived
  text it lands as the operator's claim and the result says `uncounted`; no sentence about deposits. The
  exemption sentence: refused where a decodable body is held (a `text/*` page, a derived text, a PDF with a
  text layer) unless a page render is persisted (`page_image.py`); accepted on renders or on a source holding
  nothing decodable; the marker names the renders. `--ref-id` on `add-source`: omit it; the writer promotes a
  matching staged lead under its own id (same DOI, pmid, pmcid, isbn, standard number or URL, else the same
  title) and refuses any other staged id; then `update-locator --status PROMOTED`. :136-137: `--verify-authors`
  prints NOT INGESTED for bytes it cannot parse and UNEXAMINABLE for a source with no DOI (copy the words
  from the script). :41: "(column added by migration 122; the view by migration 123)". Section 7: the
  `governing_refs` sentence becomes the derivation in the R3-11 ruling. Un-backtick harness tool names and
  result keys where the audit's docstring says they are not vocabulary; keep every value the operator types in
  backticks. The stage-6 `contested` sentence stays as round 2 wrote it (owner question 7).
- **connection-discovery** rule 2 and **conflict mapper** section 4: delete the `assess_cell.py` consumption
  sentences; state: no code reads `connections`, `connection_targets` or `conflicts`; the `contested`
  direction is the engine's only typed input from this work; the reader is the operator at the adversarial
  pass; owner question O-12 asks whether the engine should consume them.
- **research-log-manager** steps 2-3: add `--prior-expectation '<what you expect and why>'` to both examples
  (the writer refuses without it); step 2 keeps `--depth-method`.
- **citation-miner**: :304 "REQUIRED" → optional in the writer (derive from `add-source --help`), set it
  when the language is known and say how in `--lang-detection-method` (free text today: no CHECK; derive);
  :255 `.schema evidence_sources` → `python3 -c "import sqlite3; print([r[1] for r in
  sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('PRAGMA table_info(evidence_sources)')])"`;
  :263 drop `connections_produced` from the session report, consistent with :64/:91.

Acceptance: `python3 scripts/audit/skill_vocabulary_audit.py --paths <each of the five files>` reports, per
file, only tokens that are owner question 1 descriptors or gate markers (derive; list the residue in the
report); every backticked `--flag` in the five files appears in the corresponding `db.py <verb> --help`
(script it); `run_checks.py --changed-from origin/main --explain` with `attestation_presence`,
`attestation_schema`, `claude_md_spine`, `context_map_fresh` green.

### Unit V3 — independent replay (after P3; edits nothing; writes only `<scratchpad>/round3-replay/`)

You are a Sonnet usability reviewer who has not seen this round. On a fresh scratch copy of the database
(`GUIDEBOOK_DB_PATH` inline on every call) and, where a case needs it, a scratch `GUIDEBOOK_RETRIEVAL_LOG`
root seeded from the tracked `retrieval-log/` (copy the manifest lines and files of the sources you use),
replay every PATCH and REMOVE id in both directions through the CLI as an operator would, and record
commands and results only (no interpretation). Derive every id from the database or the manifests with the
queries in section 1 of the adjudication; do not type one.

For each: the wrong write, the exact refusal text, whether it names the rule and the correct flag, and the
valid write beside it landing (`--dry-run` where the fixture is hard).

- R3-1/R3-21: a source holding a derived text and no reading; `amend-source … paywalled`; ledger BLOCKED;
  `record-scan --text-scope abstract` over its HTML: result has no `block_cleared`, column unchanged, ledger
  BLOCKED with that `scan_id`; `record-scan --text-scope full` over its derived text: ledger
  READ-NOTHING-FOUND, column unchanged; `scan_debt.py` shows the BLOCKED breakdown.
- R3-2: `observe-term --verbatim-exempt` on the source holding one text-layer PDF and no render: refused
  naming the PDF; on a source with page renders: accepted, marker tail names them; on a scratch source holding
  only undecodable bytes: accepted; `add-extraction --verbatim-exempt` the same three ways.
- R3-3: `record-scan --text-scope full` over a page-less derived text (scratch root) for the source whose
  payload `page` equals its `article-number`: lands with `uncounted: true`; for the source whose manifest
  carries another paper's payload: lands; `full` over a fetched HTML still refused; `full` over 4 of 79 pages
  still refused.
- R3-4: two `add-locator` leads without DOI (distinct titles); `add-source` for lead A with no `--ref-id`
  lands on A's id; with B's id refused naming B's title; `--ref-id REF-00001` with an unrelated title refused;
  a title matching no lead lands on `next-id ref`.
- R3-7: `--verify-authors` on a scratch session whose payload repeats a real author: MALFORMED, no cross;
  delete a stored row: cross.
- R3-8: the coverage test runs; set a CHECK value on an unread source and read the ledger for each value.
- R3-9: `--paths` with a file, with a missing path, with the two-file fixture.
- R3-10: stash the units' edits; the test file exits 1 with per-case crosses and no traceback; un-stash.
- R3-12/14/15/16/17: the help texts and refusals listed in A3b and C3, each with the valid shape beside it.
- R3-13: read the five skills end to end and list every sentence whose flag, value or claimed behaviour
  disagrees with `--help`, the schema or the code.

Report plainly; do not claim a result you did not run.

### Unit AD3 — adversarial pass (after V3; read-only; writes only `<scratchpad>/adv-r3/`)

Attack the round-3 diff (`git diff bb4fbf9` on the working tree) as the two prior antagonists did: for each
PATCH, find the first real case outside its fixture on which the new rule misfires; for each REMOVE, name
the wrong thing that now reaches the guidebook and whether a cheaper gate than the removed one would catch
it; check every new sentence in the skills against the code; check every count or id typed anywhere in the
diff (rule 7a); check that `record_scan` writes one table, that no test selector can raise, that the view's
header names every CHECK value, that `--paths` cannot pass on nothing. Number the problems; cite file and
line; reproduce each on a scratch copy before reporting it.

## 4. Data follow-ups (rule 10: their own PR; not for these units)

- REF-01002's manifest line `7f15186320d39a8d.json` (Crossref 10.1682/JRRD.2013.07.0168) is bound to the
  wrong ref_id: rebind or drop the `ref_id`; its `pages` 145-158 stand (R3-20).
- REF-01033: the deposit files whole names in `family`; `correct-source` from the payload or record the
  cross as the honest state (R3-7).
- The six UNVERIFIED sources, the `scope_status` fill and the map rows (round-2 section 4) stand.
- After O-10: the attestation for `references/connection-reasoning/_template.md`.
