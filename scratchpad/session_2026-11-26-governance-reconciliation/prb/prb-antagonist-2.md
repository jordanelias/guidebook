# PR B part 2 — antagonist pass (blind-then-compare, DR-2026-08-19 §7)

Repository HEAD ee815a82; canonical DB sha256 3d419efb94b7d5c8a1297ba9552bdee64228007e38da95af612e5406bb68edb9, user_version 167 (re-derive: `sha256sum data/guidebook.db`).

## PHASE 1: my independent specification (written before opening prb-design-2.md)

### (a) The four never-run searches (exec 87, 133, 138, 191)

Facts, derived:
- All four: `results_found=0`, `deferred_reason IS NULL`, `absence_class IS NULL`; every note says the request returned no result list (87: HTTP 429 "THE QUERIES WERE NEVER ASKED"; 133: curl exit 35 reset; 138: HTTP 403 + Wayback reset; 191: HTTP 202 sgcaptcha stub). Command: `select * from search_executions where exec_id in (87,133,138,191)`.
- 133 (KR/KO), 138 (SG/EN) and 191 (NL/NL) carry a jurisdiction and language; 87 carries neither.
- OD-45 (delegated, CHECK confirmed; `grep -n -F "Delegated resolution 2026-11-13 — OD-45" references/project-standards.md`) chose option (c): a request with no result list is a search NOT RUN, `deferred_reason` set, NO absence class, owed a re-run. Option (b), a fourth absence cause, was the alternative OD-45 rejected (`DECISION-CLOSURE.md` §7). **So a new CHECK value on `absence_class` is not a fix: it is a reversal of OD-45, which only the owner may make (its reversal condition).**
- Readers that read `deferred_reason IS NULL` as "this search ran" (so a NULL-deferred zero row reads as ran-and-found-nothing): `db.cell_status` (research.examined_empty; and the `searched` pair set, so KR/KO, SG/EN, NL/NL drop out of `owed.pairs_in_scope`); `db.get_coverage_completeness` (jurisdictions_searched, pairs_searched, languages_searched, searches_outside_scope); views `v_coverage_jurisdiction`, `v_coverage_language`, `v_coverage_branch`, `v_coverage_lens`, `v_coverage_priority`, `v_coverage_parameter_via_admission`; `scripts/audit/alias_provenance_audit.py:136`; `research_batch_dod.py` R14 (line ~1223) accepts a note in place of a class, so it is green on these rows. `v_deferred_acts` lists a search only when `deferred_reason IS NOT NULL`, so these four are absent from the owed list.
- Therefore a **re-run alone does not fix it**: a re-run is a NEW row (R8 append-only); the four old rows keep `deferred_reason NULL` and keep counting as examined. A **rule** fix (readers parse `findings_note`) is the joined-cell anti-pattern (CLAUDE.md §4). A **hand UPDATE** in a data migration is forbidden (§4 "do not hand-write SQL against a table the CLI can reach … coverage bug to fix"; rule 10).
- `amend-search` has typed setters (`--set-target-evidence-type`, `--set-origin`, `--set-absence-class`, …) but none for `deferred_reason` (`grep -n "set_deferred\|set-deferred" scripts/db.py` → nothing).

Smallest correct fix: **one setter, `amend-search --set-deferred-reason TEXT`** (tooling PR, rule 10), then T-081 (research PR) applies it to the four rows with the note's words, then the re-runs ACTION (3) owes are logged as new searches. No migration (the column exists; `emit_batch_sql.py` diffs scratch vs canonical and emits UPDATEs).

Refusals the setter must make:
1. blank/whitespace reason (log_search already strips; same rule);
2. `results_found <> 0` (R6: findings are never smuggled into deferred_reason; `research_batch_dod.py` R6);
3. `absence_class` already set ("a row cannot assert both", log_search line ~1058);
4. `deferred_reason` already set (write-once, like absence_class);
5. combined in one call with `--set-absence-class` (contradiction);
6. `results_admitted > 0` or a live `search_admissions` edge (a row that admitted something ran). Do NOT refuse on linked result artefacts: 138 and 191 persisted failed-retrieval artefacts, which is exactly the evidence of not-run.
7. **The converse, on the existing setter:** `--set-absence-class` must refuse a row whose `deferred_reason` is set. Today `amend_search` does not even SELECT `deferred_reason` (db.py ~5318), so it cannot refuse; log_search refuses the same pair at insert. I expect this to be reproducible as a live defect.
Trail: the change appended to findings_note by the existing marker mechanism (as every other setter does).

Known consequence to state, not fix: `v_deferred_acts` says a deferred search stands for ever ("A search later run is a new row that names nothing it discharges … Not derivable today"), so after the re-run the four still list as owed. Also the column comment "deliberate no-search" becomes inaccurate prose (DDL comment; OD-45 asked only for a sentence in the PR).

### (b) The minimal reader-facing page

Must contain (DR-2026-08-19 §4: "a determination, its governing sources, its population-match grading, and its search log including the empty searches — rendered and readable"):
- the determination: value_min/value_max/value_unit (and value_notations), state, the STORED marker (never re-derived; ⚠ cannot be stored until T-117 — `specifications.marker` CHECK admits only ●◐○), the lens by code AND name (identity/ICF/need), parameter name (terms.canonical_en through base_parameters);
- each governing source (role='governing' in specification_extraction_links via v_determination_provenance): authors (v_author display / author table), title in the original, reviewed English beside it, year, tier, evidence_type, verification_status (UNVERIFIED shown, not refused: owner 2026-11-14 "keeping them but they get a triangle warning"; "triangle instead if the value is coming from grey or unverified"); the governing figure (claim_text original + reviewed English; claimed_value/unit never translated);
- every evidence_population_match row for each governing source (not assess_cell.population_match's first hit), and "not assessed" where none (G2);
- the search log: every search_executions row on the slugs of the governing extractions (and parameter_id rows), each zero row stated as one of three things: ran and found nothing (absence_class), NOT RUN (deferred_reason), or cause unrecorded — never collapsed;
- open determination gates (v_open_determination_gates) for the cell, and gaps.
Must refuse: a specification that is not live (retired_at set, or state not in stated/provisional, i.e. not in v_best_practice). Translation: per OD-30/T-037 amendment, a translation is shown only when status='reviewed', not superseded, reviewer ≠ translator (CHECK), and `translation_sha256(read_cell(...)) == source_sha256` (db.translations_shown does exactly this and returns original:null on mismatch). Whether a missing English refuses the PAGE or shows the original alone is a design choice; OD-30 says "otherwise only the original is shown", so refusing the whole page is stricter than the ruling, but defensible for the acceptance page given "i only know english" (readable). I would show-and-flag by default, refuse only under the acceptance mode.
Reads: v_best_practice, v_determination_provenance, specification_extraction_links, evidence_sources (+ author display), evidence_population_match, search_executions, translations via db.translations_shown semantics (dbcore.read_cell + translation_sha256), base_parameters/terms, lens registries, v_open_determination_gates, gaps.
Output: outside the repository ($TMPDIR), never committed (CLAUDE.md §3: "Book surfaces, read from the database when rendered (owner, 2026-08-27); no committed file is one"; 2026-10-28 owner statement ACTION: page generated to $TMPDIR and published privately).
Reuse: `scripts/generate/owner_browser_build.py` (145 lines) + `owner_browser.html` embed the WHOLE database (base64) and query it in the browser with sql.js at view time, publish as a private Artifact, refuse --out inside the repo, enforce the 16 MB limit. That is the most literal reading of "read from the database when rendered". The page could be a new view/tab inside it. Obstacle: the translation hash check (`translation_sha256` normalisation) would have to be re-implemented in JS, a second home for the rule; or the build step could pre-compute the shown translations in Python into META (which is what `holds` already does for determinations_resting_on). Alternatively a small standalone Python composer reusing owner_browser_build's out-path refusal. Canonical DB is 5.9 MB, so the 16 MB limit holds for an embedded build today.
Today there is NO live determination (specifications 1–8 all retired), so on canonical the page can only refuse; it must be built and tested against a scratch DB holding T-110 output.

### (c) OD-63

OD-63 is ANSWERED BY THE OWNER (fifteenth set, 2026-11-14): render shows min/mode/median/max as a colour code on the surveyed jurisdictional code bodies; the determination uses all values. T-037 §4 (iii)/(iv) fixes placeholders and defaults under the sixteenth set ("these aren't real decisions"). `cell_figures` (T-124) does not exist: `git grep -n "def cell_figures" -- scripts` → nothing. T-037 says render reads T-124 and never computes a figure, and needs T-036's jurisdiction comparison for "the surveyed code bodies". Omitting the four figures on the first page is a relaxation of an owner answer, so Q1 is genuinely owner-only. Variant A (omit): the page states visibly that the four figures are not shown and why, lists the governing figures with citations. Variant B (keep): blocked on T-124 (itself after T-059 and T-068 per its file — to be verified) and T-036 (or an equivalent jurisdiction query).

### (d) Red tests first

Tooling: (1) `amend-search --set-absence-class genuine_absence` on a scratch row with deferred_reason set is ACCEPTED today (expect red → must refuse); (2) `--set-deferred-reason` does not exist (argparse error); after: sets the column, appends a trail; (3) refused on results_found>0, on absence_class set, on already-deferred, on blank, on both flags in one call, on an admitted row; (4) after amending exec 133 on scratch, cell_status(parameter of its slug) moves 133 from research.examined_empty to never_examined.deferred_searches and KO/KR appears in owed if no other run covers it; get_coverage_completeness pairs_searched does not rise. Page: refuses a retired spec; prints a deferred row as "not run"; prints an unclassed zero row as "cause not recorded"; shows original only when the source cell's hash differs; prints both of two dissenting grades; prints the stored marker, never one it computed.

### (e) Riskiest decision

Turning a logged "ran" row into "not run" by amendment edits R8's append-only log. It is justified only because each row's own contemporaneous note already says not run, so the typed column is brought into line with what was recorded at the time; write-once plus refusal on any admission keeps it from becoming a way to erase an empty result. Second risk: page refusals that encode a doctrine (translation completeness, grade completeness) stricter than the rulings (OD-30, G2).

---

## PHASE 2: comparison against prb-design-2.md

Scratch copies used (never canonical): `scratchpad/ant2/s.db`, `t.db`, `u.db` (copies of canonical), and the path-finder's `scratchpad/pf/r3MOB.db` read-only (holds live specification 9, 3 × MOB). Canonical sha256 unchanged after every probe: `3d419efb…edb9`.

Note on scope: the antagonist brief I run under forbids me to propose repairs (a critic who drafts the fix talks itself into accepting it). Where the caller asked for "corrections as exact text", I give the **correct statement of fact** the design should carry (true reader list, true dependency closure, the ruling text it missed), not replacement code or design text.

### Diff against my phase 1

| Point | Phase 1 (mine) | Agonist | Same? |
|---|---|---|---|
| (IV) fix | one `amend-search --set-deferred-reason` setter; no CHECK value (OD-45 rejected option (b)); no migration | same | yes |
| converse refusal | predicted reproducible | reproduced | yes |
| refuse on admissions | yes (results_admitted / edge) | not listed | agonist omits |
| prose callers | R6 contract text, DDL comment "deliberate", amend-search docstring/help | log_search comment, two skills, T-081 file | agonist omits mine |
| page form | owner browser is the only surface that reads the DB at view time; static composer acceptable under OD-12 (4) | static composer; browser rejected | differ (see claim 3/7) |
| translation refusal | stricter than OD-30, defensible, not owner-only | same reading | yes |
| ungraded governing | prefer "not assessed" (G2) over refusal | refuse | differ |
| OD-63 deps | T-124 (+T-059/T-068 to verify), T-036 | T-124, T-059, T-068; drop T-036 | differ (both incomplete; see claim 8) |

### Comparison table

| # | Claim | Agonist | Antagonist | Verdict | Evidence |
|---|---|---|---|---|---|
| 1 | Re-running alone does not fix; readers read NULL `deferred_reason` as ran | five readers listed | cell_status, alias_provenance_audit:136, research_batch_dod R8 (l.614)/R14 (l.1223), test_scan_contract T026-14, six `v_coverage_*` views all verified. **Missed:** `db.get_coverage_completeness` (`coverage --slug`). **False sub-claim:** §1.6 "the four rows' pairs return to owed": measured, they do not on this slug | WOUNDED | `cell_status(3)` examined_empty `[87,133,138,191]` → after deferral `[]`, deferred `[87,133,138,191]`; `get_coverage_completeness('accessible-circulation-geometry')` pairs_searched 19 → 19, jurisdictions 23 → 23, languages 12 → 12, outside_scope 68 → 67, deferred 0 → 4; `owed.pairs_in_scope` `[]` before and after |
| 2 | `--set-absence-class` accepts a deferred row | reproduced | reproduced; no gate catches it (`git grep absence_class -- scripts/audit` finds only R14, which skips deferred rows) | SURVIVES | `amend-search --exec-id 9 … --set-absence-class genuine_absence` rc=0; row `(9, 0, 'genuine_absence', 1)` |
| 3 | No migration; emit_batch_sql captures the UPDATE | yes | yes; R8 forbids only deletion (contract hook "Never delete or backfill"; DoD R8 tests id gaps), not an UPDATE | SURVIVES | `emit_batch_sql.py --scratch t.db` → "0 insert(s), 1 update(s), 0 delete(s)", `UPDATE "search_executions" SET "deferred_reason" = … WHERE "exec_id" = 87;` |
| 4 | owner_browser_build cannot be the renderer | "embeds every row, can refuse nothing" | Overstated: the build step is Python and can refuse before writing (it already exits 2 on NOT_SHOWN drift and size). The real reason (refusals and the sha256 check would need a JS second home) holds. But the browser is the only surface that reads the database **at view time**; the design rejects it in favour of a static generator the 2026-10-30 ACTION (3) names | WOUNDED | `owner_browser_build.py` l.103–105, 134–136; ledger `grep -n "do not restore a static generator" references/project-standards.md` |
| 5a | Refusal: not live | yes | right; on canonical every specification is retired, so the page can only refuse there | SURVIVES | `select specification_id, retired_at from specifications` → 1–8 all retired |
| 5b | Refusal: non-EN without current reviewed hash-matching English; today 30, 105, 115 | yes | Subjects confirmed: each had a reviewed translation superseded by a **rejection** ("original cell is truncated"), so the refusal fires on a defective original, not a hash mismatch. Hash handling matches storage (`translations_shown` sets `original: null` + problem on mismatch). **Gap:** `claimed_value` in a non-English word form (extraction 80, `viisi prosenttia`) and `claimed_unit` prose are outside the refusal's subject | WOUNDED (scope) | translations ids 30/40/83 reviewed → superseded by 136/146/190 rejected; `v_determination_provenance` row 80 |
| 5c | Refusal: NULL verification_status | yes | examines 0 rows anywhere (51 VERIFIED, 8 UNVERIFIED, 0 NULL); engine treats NULL as not-verified (`assess_cell.py` l.1278 `(… or "") in VERIFIED_OK`), so the page would be stricter on NULL than on UNVERIFIED, which the engine equates | WOUNDED (LOW) | `select verification_status, count(*) from evidence_sources group by 1` |
| 5d | Refusal: governing source without a grade; today five | yes, five | five confirmed (REF-00988, -00990, -00991, -00992, -01010). But: (i) undefined for a cell with no identity lens (`population_match` returns None with no population); (ii) the attribution rule ("target_population names the identity code as a word") re-implements `population_match`'s regex, which the design's own §2.11 stop condition forbids; (iii) G2 already defines the ungraded state as NOT_ASSESSED, and the design itself prints "not graded" for conditioning sources | WOUNDED | design l.400 vs l.614; `assess_cell.py` l.1033–1053 |
| 5e | Not refusing UNVERIFIED | right | right; owner 2026-11-14 "keeping them but they get a triangle warning" and "triangle instead if the value is coming from grey or unverified" | SURVIVES | ledger l.7005, 7053 |
| 6 | Six governing sources carry PARTIAL and PROXY; `population_match` hides it | yes | Six confirmed (REF-01012 … -01017). Mischaracterised: every PROXY row's `mismatch_note` begins "CORRECTION (independent adversarial pass, batch 22): this source's earlier PARTIAL grade misapplied the 2026-09-25 owner ruling". `population_match` returns the **lowest match_id**, i.e. the grade the adversarial row says is wrong, and the engine graded spec 9 on it. The design treats this as a display issue only; the published determination rests on it | WOUNDED | query over `evidence_population_match` for the six refs on `pf/r3MOB.db` |
| 7 | Static file as private Artifact is compatible | medium confidence; open input 2 | The design cites 2026-08-27 and 2026-10-28 but **not** "Owner rulings 2026-10-30" ACTION (3): "Render a specification page from the database, not from a committed file … do not restore a static generator". The narrowing to "committed HTML" is an [ASSUMPTION] that ACTION (7) of the same entry marks unratified. `skills/run-pipeline_SKILL.md` §7 restates it as "No committed file and no static generator", which the design proposes to "reconcile" (edit) as a caller. OD-12 (4) (delegated) supports a build product outside the database. So open input 2 is genuinely owner-only, but mis-stated | WOUNDED | `sed -n 4852,4867p references/project-standards.md`; `sed -n 407,417p skills/run-pipeline_SKILL.md`; OD-12 l.5806 |
| 8 | Variant B needs T-124 + T-059 + T-068; no T-036 | "transitively" | Not transitive: T-059 needs T-120 and T-127 (unmerged; T-127 needs T-102); T-068 needs T-059 and T-120. And **Variant A is not cheaper on that axis:** it needs T-117, whose preconditions are T-119 (merged), T-120, T-068, T-102, so A already pulls T-068 → T-059 → T-120, T-127, T-102. B's increment over A is T-124 plus the unit data and T-113. "No T-036": T-036 §4 is "limited to in-scope pairs", which carries the owner's 2026-10-30 item 5/7 ("one row per in-scope jurisdiction"; "P1+P2+P3 … current editions only"); a GROUP BY over `cell_figures` rows does not apply it | WOUNDED | task files §2 of T-124, T-059, T-068, T-117; REMEDIATION-PLAN.md "Merged" list (T-016, T-019, T-119, T-126 merged; T-120, T-127, T-059, T-068, T-102, T-117, T-124 not) |
| 8b | 28 of 51 code-stratum rows unparsed | yes | recomputed: 51 rows, 28 refused by `dbcore.figure_refusal` | SURVIVES | ids 74 … 114 |
| 9 | Size and callers | listed | missed callers, below | WOUNDED | below |
| 10 | Open owner inputs | four | Q1 owner-only: yes. Form: owner-only, but must cite 2026-10-30 ACTION (3). Non-EN queries: answerable from the owner's 2026-11-20 words ("translate the stuff from other languages so that i can actually see it"); delegable. Ungraded conditioning: delegable. **Missing:** dropping the audience lens contradicts 2026-10-30 item 4 / ACTION (4) ("A page offers an audience lens … and a disability lens"); evidence order (item 5, alphabetical by first author, regrouped by lens) and page scope (item 7) are rulings the design neither applies nor puts to the owner | WOUNDED | ledger l.4855–4858, 4866 |

### Defects (worst first)

**D1 — HIGH. The page mixes two databases.** Design §2.4: `page(conn, specification_id)` is "a pure function over a read-only connection", yet reads `db.translations_shown()` and `db.cell_status()`, neither of which takes a connection: both open `dbcore.connect(readonly=True)`, which resolves `GUIDEBOOK_DB_PATH` or the canonical file (`dbcore.py` `def db_path` and `def connect`, `target = Path(path) if path is not None else db_path()`). With `--db scratch.db` and no matching env var, the value and grades come from the scratch copy and the translations and search log from canonical. T037R-05 ("a --db other than the canonical file prints DRAFT") is the exact case where this bites, and no case would see it. Correct fact: the two helpers bind to `db_path()`, not to a passed connection (`grep -n "def translations_shown\|def cell_status" scripts/db.py`).

**D2 — HIGH. The DRAFT test cannot fire under the project's own write path.** "--db is not dbcore.db_path()'s canonical file": `db_path()` returns `GUIDEBOOK_DB_PATH` when set, and CLAUDE.md §4 requires that variable inline on every call to a scratch copy. A page built that way reads as canonical and prints no DRAFT. `dbcore.is_canonical` exists (`dbcore.py` l.119; `grep -n "def is_canonical" scripts/dbcore.py`) and is what the comparison has to be against.

**D3 — HIGH. A ratified ruling on the page's form was not found.** Owner rulings 2026-10-30 ACTION (3) "do not restore a static generator"; ACTION (7) makes the "committed HTML" narrowing unratified; ACTION (4) requires both lenses; items 5 and 7 fix the comparison table's rows and scope. None is cited in design §2.2. The design proposes to edit the skill sentence that restates ACTION (3) ("reconcile"), i.e. to change prose that carries a ruling instead of asking the owner. Command: `sed -n 4852,4867p references/project-standards.md`.

**D4 — HIGH. Variant dependency lists are wrong both ways.** See claim 8. The correct closure on HEAD ee815a82: Variant A = T-117 {T-120, T-068 {T-059 {T-120, T-127 {T-102}}}, T-102} + (IV) + T-110 data; Variant B = Variant A + T-124 + T-108, T-086, T-111, T-113 data (+ an in-scope filter, T-036 or equivalent). The "A is the short path" framing that Q1 is put to the owner on is therefore materially overstated.

**D5 — MEDIUM. The contested grades are a correction, and the determination used the withdrawn one.** See claim 6. The page as designed prints both rows "as a contest" (which CLAUDE.md §4 permits) but says nothing about which one the engine used, so a reader sees PARTIAL and PROXY with no sign that the published value was graded on PARTIAL.

**D6 — MEDIUM. Apparatus prose reaches the published page through `claimed_unit`.** The design bans `value_note`, `falsification_condition`, `confidence_*`, `tier_basis`, `derivation_rationale` (T037R-03) and prints `claimed_unit` "as stored". On spec 9, extraction 80's unit reads "… Digit-equivalents are an editorial gloss, not verbatim -- see notes and GAP filed this batch on _require_verbatim's digit-check." and its value is `viisi prosenttia` (Finnish words, no English owed by `_translations_owed`). Variant A prints both.

**D7 — MEDIUM. §1.6's predicted reader effect is false on the target slug.** "The four rows' pairs return to owed": measured, pairs_searched, jurisdictions and languages are unchanged (other searches cover KR/KO, SG/EN, NL/NL), only `searches_outside_scope` drops 68 → 67. A test written to that prediction would be red for the wrong reason.

**D8 — MEDIUM. Refusal 4 re-implements `population_match`'s attribution and is undefined for an ICF- or need-only cell** (claim 5d). It contradicts the design's own §2.11 stop condition.

**D9 — LOW. The setter's refusals omit admissions.** `results_found = 0` does not imply no `search_admissions` edge (no CHECK pairs them); a row with an edge ran.

**D10 — LOW. NULL-verification refusal examines nothing today and treats NULL more strictly than the engine does** (claim 5c).

**D11 — LOW. Variant B's colour code depends on 28 unparsed governing code-stratum figures that the engine nonetheless governed on** (spec 9 links them as `governing`). Whether the engine's value is right with 28 figures `figure_refusal` cannot read is outside this design, but Variant A publishes that value. [UNVERIFIED: how the engine treated those rows.]

### Omissions (callers and facts the design missed)

- `db.get_coverage_completeness` (`coverage --slug`, cited in `skills/run-pipeline_SKILL.md` §4): output changes (`searches_outside_scope`, `searches_deferred_with_reason`).
- `governance/research-contract.yaml` R6: "deferred_reason means DELIBERATELY NOT SEARCHED". A 429 is not deliberate; OD-45's plan changes asked for a sentence on "deliberate". That text is injected every session by the SessionStart hook in `.claude/settings.json` and compared by the blocking `research_contract_sync`, so any edit touches a blocking check. The design says "R6 stays true".
- The DDL comment `deferred_reason TEXT -- non-NULL => deliberate no-search for this cell` (needs a schema migration to change; at minimum a PR sentence, as OD-45 asked).
- `amend_search`'s docstring ("APPEND a correction to a logged search's findings_note. Never rewrite it.") and the `p_am` help string ("APPEND a dated correction …"): already inaccurate, made more so.
- `skills/citation-miner_SKILL.md` l.120 and `scripts/audit/research_batch_dod.py` R6 message repeat "DELIBERATELY NOT SEARCHED".
- T-037 §3's own evidence ("no page generator", `ls scripts/generate`) is already false (owner_browser_build.py exists since 2026-10-28), so T-037 as written stops at its §3; the design does not say so.
- `v_deferred_acts` keeps every deferred search listed after its re-run ("Not derivable today"); deferring four rows adds four permanent entries. The design reports the listing as the intended effect and omits the permanence.
- Readers the design lists by line number (`test_scan_contract.py:1492`, `alias_provenance_audit.py:136`) are fine; tests that derive their counts from the same predicate (`test_run_pipeline_refusals.py` l.1232, 1262, 1276; `test_db_amend_writers.py` l.4303, 4391) move with the data and belong in the before/after run.

### SPLIT

- **Ready now (tooling PR, rule 10):** (IV) the setter plus the converse refusal on `--set-absence-class`, with the prose callers above swept. No owner input; OD-45 is delegated and confirmed.
- **Then (research PR):** T-081 using the setter on 87, 133, 138, 191 with each note's words; re-runs as new searches afterwards (OD-45 ACTION (3)).
- **Waits for the owner:** Q1 (OD-63 relaxation); the page's form against 2026-10-30 ACTION (3) (static generator) and whether a private Artifact is "published" for DR §4; whether the first page may omit the audience lens (2026-10-30 item 4).
- **Waits for tooling not merged:** any page build, under either variant, needs T-117, which needs T-068, T-059, T-120, T-127, T-102. Building the page script now against `pf/r3MOB.db` is possible but cannot publish.
- **Drop from the design:** the claim that T-036 is unnecessary (until the in-scope filter has a home); the "five readers" count as stated; the §1.6 "pairs return to owed" prediction.

### Approval list (smallest first)

| # | Item | Class | Confidence | Evidence command |
|---|---|---|---|---|
| 1 | Converse refusal on `--set-absence-class` for a deferred row | DELEGABLE | high | `GUIDEBOOK_DB_PATH=<copy> python3 scripts/db.py amend-search --exec-id 9 --append-note "TASK-FIXTURE" --set-absence-class genuine_absence --session s` → rc 0 today |
| 2 | `amend-search --set-deferred-reason` (write-once; refused on found, classed, deferred, blank, admitted) | DELEGABLE | high | `amend-search --help | grep -c set-deferred` → 0; emit dry run "1 update(s)" |
| 3 | Sweep R6 contract text / DDL comment / amend-search docstring and help | DELEGABLE (R6 touches the blocking `research_contract_sync`) | medium | `git grep -n "DELIBERATELY NOT SEARCHED"` |
| 4 | T-081 deferral of 87, 133, 138, 191 | DELEGABLE (research, Opus-class) | high | `select exec_id, deferred_reason from search_executions where exec_id in (87,133,138,191)` |
| 5 | Page refusal set (not live; translation; grades) | DELEGABLE except where it drops an owner requirement | medium | design §2.4 |
| 6 | Page form (static file vs view-time read) | OWNER-ONLY | high | `sed -n 4866,4867p references/project-standards.md` |
| 7 | Dropping the audience lens on the first page | OWNER-ONLY | high | ledger 2026-10-30 item 4 |
| 8 | Q1: omit the four figures | OWNER-ONLY | high | `grep -E '^OD-63' references/project-standards.md` |

### Summary (under 200 words)

The design for (IV) holds up. Re-running the searches does not fix them; adding a CHECK value would reverse OD-45; `emit_batch_sql` captures the UPDATE; the converse defect reproduces (exec 9, rc 0) and no gate catches it. Its weaker points: it misses one reader (`get_coverage_completeness`), it predicts that pairs return to owed (measured, they do not), it omits the R6 and "deliberate" prose callers (R6 is held by the blocking `research_contract_sync`), and its setter does not refuse rows with admissions. The design for (V) has two high-severity build defects. First, `page(conn)` calls `translations_shown()` and `cell_status()`, which read `GUIDEBOOK_DB_PATH`, not `conn`. Second, the DRAFT label tests against `db_path()`, so under the write path it can never fire. It also misses the owner's 2026-10-30 rulings: ACTION (3) "do not restore a static generator", both lenses, and the in-scope jurisdiction rows. Its dependency lists are wrong both ways: Variant A already pulls in T-068, T-059, T-120, T-127 and T-102 through T-117. The "contested" grades are adversarial corrections, and the engine graded spec 9 on the withdrawn grade. Q1, the page's form and the audience lens are owner-only.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/prb-antagonist-2.md
