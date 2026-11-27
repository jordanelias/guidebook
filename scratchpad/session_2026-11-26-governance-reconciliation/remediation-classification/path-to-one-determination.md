# The shortest honest path to one published determination (DR-2026-08-19 §4)

Path-finder report, 2026-11-27, branch `ccr-64231823-gqy3xr` at `cd34b96`, schema `user_version` 167.
Read-only throughout. The engine was run only on scratch copies under
`/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/pf/`. The canonical
`data/guidebook.db` sha256 was `3d419efb…edb9` before the runs and unchanged after them.
Rule 7a: every figure below is a reading taken today, and its command sits beside it. Re-run the command
rather than trusting the figure.

The criterion (DR-2026-08-19 lines 373-375): *"One research question, with a determination, its governing
sources, its population-match grading, and its search log including the empty searches, rendered and
readable as output."* The brief also asks for tiers and markers.

---

## 0. Answer in brief

- **Candidate:** parameter 3, ramp gradient (TERM-001). It holds far more recorded evidence than any
  other parameter. Of the parameters that hold figures, it is one of only two with a recorded
  accessibility direction (the other is parameter 12). Without a direction, a cell gets no value (T-059
  item 6, "No recorded direction").
- **The engine can determine it today.** It writes `provisional`, 5 % / 1:20, at `MOB`, with marker `○`.
  Three things in that output would put wrong content in the book:
  1. **Wrong group.** `MOB` fails the umbrella test for ramp gradient: the ledger records that its
     members' demands are opposed (project-standards.md line 1197). T-110 item 2 forbids a `MOB`
     determination that has not passed that test.
  2. **Wrong marker.** The owner's marker table puts ⚠ in place of the circle for an unverified,
     proxy-inferred or thin basis (OD-59, OD-64). The engine cannot write ⚠: the CHECK on the
     `specifications` table refuses it.
  3. **Unjudged group assignments.** All 216 live lens links have basis `carried`, none judged. OD-65,
     answered by the owner, requires each code value's lens to be judged and to carry its warrant.
- **What does not exist:** a page a reader can open.
- **Core path, Route B: six tasks**, plus slices of two more. T-102, T-104, T-081 and T-110 are
  research. T-117 and a reduced T-037 are tooling. T-110 carries the slices of T-112 and T-127.
- **If the first page must also show OD-63's four figures:** add T-124, T-036, T-108, T-086 and T-111,
  which makes **eleven**. One owner question decides whether they are on the path.
- **Of the 73 open tasks, about 62 to 67 are not on the path.**

---

## 1. Today's state (read-only derivations)

All commands run from `/home/user/guidebook`. `R` stands for `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`.

### 1.1 Parameters
`select p.parameter_id, t.canonical_en, p.accessibility_direction from base_parameters p join terms t using(term_id)`

There are 10 active parameters, ids 3 to 12. Two have a direction, both `lower_is_better`:
- 3, ramp gradient
- 12, ramp run length

The other eight have a NULL direction. For them the engine composes no headline value; supplying a
direction is T-123's job.

### 1.2 Recorded evidence per parameter (the candidate ranking)
`select x.parameter_id, count(*), count(distinct ref_id), …` (the full query is in §4).

| param | name | extractions | sources | verified sources | T1/T2 sources | extractions verified or reviewed | direction | sources graded |
|---|---|---|---|---|---|---|---|---|
| 3 | ramp gradient | 122 | 58 | 50 | 16 | 44 | lower_is_better | 53 |
| 4 | corridor width | 24 | 7 | 7 | 0 | 0 | — | 6 |
| 12 | ramp run length | 21 | 11 | 10 | 1 | 0 | lower_is_better | 9 |
| 9 | door width | 16 | 7 | 7 | 0 | 0 | — | 6 |
| 6, 5, 11, 8 | … | ≤11 | ≤6 | | 0 | 0 | — | |

### 1.3 Admitted sources
`select tier, verification_status, count(*) from evidence_sources group by 1,2`

- 59 sources in all.
- 51 are `VERIFIED` and 8 `UNVERIFIED`: one T1, two T4, one T5 and four T6.
- Population-match grades: 61 rows (4 EXACT, 25 PARTIAL, 32 PROXY). Every `target_population` holds an
  identity code.

### 1.4 Extractions and lens links
`select extraction_status, count(*) from source_value_extractions where retired_at is null group by 1`

- Extraction status: 167 preliminary, 13 reviewed, 31 verified, 3 absent-confirmed.
- Lens links: `select basis, count(*) from extraction_lens_links where retired_at is null group by 1` gives
  **216 `carried`, 0 judged.**
- Lens distribution for parameter 3: `MOB` 116, `SCI` 3, `MS` 2, `A-EFFORT` 2, `d450` 1. The query is in
  this file's §1.6.

### 1.5 Specifications
`select specification_id, state, retired_at is not null from specifications`

- 8 rows. All are for parameter 3 at `MOB`, and **all 8 are retired**. None is live.
- One determination gate is open: gate 1, `UNLINKED`. It records that REF-01002 (T1, a 7 % maximum) is not
  linked to the old specification 8, and it remains unresolved.
- 5 `convergence_assessment` rows, all `pending_assessment`.

### 1.6 The engine (`scripts/assess/assess_cell.py`), run on scratch copies
The command:
`cp data/guidebook.db $S/rXY.db; python3 scripts/assess/assess_cell.py --db $S/rXY.db --emit-sql $S/rXY.sql --parameter-id P --slug accessible-circulation-geometry --identity I --session session_pf-probe --stamp "2026-01-01 00:00" --report-json $S/rXY.json`

Note: `--emit-sql` is not a dry run. The engine **commits into `--db`** and writes the SQL file as a copy.
It refuses the canonical database.

| cell | result |
|---|---|
| 3 × MOB | `provisional`, value_max 5.0 % (notations: `5` %, `1:20` rise:run), basis `T4-6-only-threshold+CO1+T2-direction(proxy_inference)`, `rests_on_proxy_inference=1`, `has_unverified_sources=1`, **marker ○**, 27 governing refs and 5 supporting, 116 extractions in lens. "GATE binds: gate 1". Extractions 45 and 51 excluded as skimmed; 10 skimmed findings left out. `needs_population_assessment`: REF-00988, REF-00990, REF-00991, REF-00992, REF-01010. |
| 12 × MOB | `provisional`, 6000 mm max (stated as 600 cm), `T4-6-only(regulatory_stratum_only)`, marker ○ |
| 4 × MOB | `pending`, no value (no direction) |
| 3 × DEAF | **REFUSING: no figure of parameter 3 is stated in this lens** (D-08 is met) |

**Defects visible in that output:**
- **The `value_note` contradicts itself.** It says *"24 state no parsable numeric bound ('12%', '1:10', …
  '5%', …)"*. These claims sit in `claimed_value` / `claimed_unit` cells that also carry conditions
  (T-108), the bare unit `ratio` (T-086), or a spelled-out number (T-111).
- **The headline is still right.** The gentlest parsable claim is 5 %, and none of the 24 unparsed claims
  is gentler: the 1:24 of REF-00139 is a condition branch. The headline 1:20 / 5 % is stated by
  `verified` extractions of `VERIFIED` sources: extraction 25 (REF-00992, Approved Document M) and
  extraction 30 (REF-00995, Flemish decree).
- **The engine's prose contradicts later owner rulings.** It says "not a best-practice claim" and "This is
  a floor claim … only T1/Co-1/T2/Co-2 evidence can do that". OD-58 / T-059 item 6 make the most
  accommodating value from any tier the best. D-43 count: `assess_cell.py:3`, `adjudication_integrity.py:1`.
- **The integrity test blocks a live row.** `GUIDEBOOK_DB_PATH=$S/r3MOB-int.db python3 scripts/tests/test_db_integrity.py`
  gives `rc=1`, `[C10] no published cell rests on an unverified or disputed source`. Six governing sources
  are UNVERIFIED: REF-00994 (IPC), REF-00997, REF-01013 (Ontario), REF-01014 (ISO), REF-01016 (NZS),
  REF-01026. So with today's code, a live determination cannot pass the blocking test.

### 1.7 Render
- `git ls-files | grep -i -E 'render|template|page|publish|site'` finds no renderer.
- `ls scripts/generate` lists `context_map.py`, `owner_browser_build.py`, `owner_browser.html` and
  `research_contract_hook.py`.
- The one script that turns the database into reader-facing HTML is `owner_browser_build.py`. It embeds the
  whole database through sql.js as a table browser, refuses to write inside the repository, and is published
  as a private Artifact. It browses tables; it does not compose a page for a question.
- The old static generator was deleted by the 2026-10-14 ruling (handoff:
  `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §1). A draft render contract exists at
  `workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md`.
- No views serve render; `walkability.py` reports every `X<->render` pair as `NO PATH`.

### 1.8 Translation, units and the identity-need-ICF matrix
- **Translations.** `select status, count(*) from v_translations_current group by 1` gives 93 current rows,
  all `reviewed`, each by a reviewing instance other than the translator (OD-30 is met).
- **Translation gaps for parameter 3.** Non-English `claim_text` without a current reviewed translation:
  nl 3, es 1, fr 1, five rows in all (query: §1.8 of the working, `Counter((lang, has_reviewed))`).
  Non-English source titles: all translated.
- **Units.** `base_units` holds 7 rows: mm, cm, m, in, ft for length, and % and `rise:run ratio` for
  gradient. `NOTATION_FAMILIES` is gone from the engine, so D-14 is met. The parameter-12 run shows three
  length notations.
- **`identity_need_icf`.** 65 rows: 1 `stated`, 64 `pending`. The delegated ruling of 2026-11-25 (OD-85)
  records: "no gather, determination or gate reads `identity_need_icf` (D-0184)". **Not on the path.**

### 1.9 Search log
`select slug, count(*), sum(coalesce(results_found,0)=0) from search_executions group by 1`

- `accessible-circulation-geometry`: 168 searches, 9 with zero results.
- `room-acoustic-performance`: 28.
- No slug: 7.
- 196 of 203 searches have `parameter_id` NULL, so a parameter's search log is its slug's log.
- **`absence_class` is NULL on all 203.**
- Of the eight zero-result rows in the circulation slug (exec ids 29, 81, 82, 84, 85, 87, 133, 138, 191),
  **four are not searches at all: 87, 133, 138 and 191.** Their notes call them an unfired query and three
  retrieval failures. Under OD-45 (resolved under delegation) each is a search not run, a deferral owed a
  re-run.

---

## 2. What is missing, per goal element, for ONE parameter end to end

| Element | Missing capability (concrete) | Task(s) that supply it | Smallest version |
|---|---|---|---|
| **E1 research** | A page that shows "the empty searches" would present four retrieval failures as evidence of absence. | **T-081** | Class the eight circulation-slug zero rows with `amend-search --set-absence-class`. List 87, 133, 138 and 191 as deferrals owed a re-run. Data only, about one hour. |
| **E2 recording** | (a) Governing citations printed from unverified rows; C10 also blocks. (b) Five param-3 non-English claim texts have no reviewed English. (c) Conditions in the unit cell, the bare `ratio` unit and spelled-out numbers: they break the headline only through the misleading `value_note`, and break the four figures if those are shown. | (a) **T-104**; (b) slice of **T-112**; (c) T-108, T-086, T-111 (conditional, §4) | (a) Re-retrieve the six unverified governing sources. Any that cannot be retrieved keeps UNVERIFIED and shows ⚠ (needs T-117 4a). (b) `request-translation` / `record-translation` / `review-translation` for five rows. (c) Only if the four figures are rendered. |
| **E3 lens** | (a) `MOB` is the wrong group for ramp gradient: opposed demand (ledger line 1197; T-110 item 2). (b) All lens links are `carried`, unjudged (OD-65). (c) Five governing sources have no population-match grade. | (a)+(b) **T-102**, scoped, which also does T-127's job for param 3's rows; (c) inside **T-110** | Mint `WHEEL` (and `LLD`, `WALKAID`, as the owner confirmed: cheap) under `MOB`. Rename `MOB`. Carry param 3's 119 identity links by judgment to `WHEEL` or `MOB`, with `named_in_text` / `heading` / `context` warrants. Retire `SCI` into `WHEEL` (OD-83). Grade the ungraded governing refs against `WHEEL` with `add-population-match`. All verbs exist: `add-identity`, `amend-identity`, `retire-identity`, `add-lens-link`, `retire-lens-link`, `add-population-match`. |
| **E4 adjudicate** | Gate 1 (REF-01002, T1, 7 %) is unresolved. Nothing else is needed for one cell whose figures are all ceilings that can all be met: none diverge (T-059 OR-6b). | inside **T-110** | Either read the Vredenburgh full text (GAP-016) or `resolve-determination-gate` with its reason. 7 % is looser than the stated 5 %, and under OD-58 it states no harm at 5 %, so the selection is unchanged. |
| **E5 determine** | (a) The marker is wrong: the engine writes ○, while the owner's table gives ⚠ for an unverified, proxy or thin basis, and the CHECK admits no ⚠. (b) C10 refuses the live row. (c) The engine's prose contradicts OD-58. | (a)+(b) **T-117**; (c) **none, if render does not print that prose** (else T-068 item 8, four strings) | T-117 as written: `band()`, the override deletion, the ⚠ branch, the CHECK rebuild, C10 4a. Then run the engine for `3 × WHEEL` in T-110's research batch. |
| **E6 render** | Nothing a reader can open. | **T-037, reduced** | One script, outside the repository's output tree, publishing as a private Artifact like `owner_browser_build.py`. For one `specification_id` it prints: the value in its stored notations, the state, the marker, the lens by name; each governing and supporting source (original-language title, reviewed English, tier, marker, verification state); the population-match grades; the slug's search log with zero rows and `absence_class`; the cell's gaps. It prints only typed columns and composes its own sentences, never `value_note`, `falsification_condition` or `confidence_*`. Left out: render table, hash or staleness check, T-032 discussion, T-036 view, T-122 criteria, page-language parameter. |

---

## 3. Definition of Done D-01..D-21, classified

There is no D-10 in §10. Commands are as written in REMEDIATION-WORKPLAN.md §10.

| # | Command (abridged) | Result today | Class |
|---|---|---|---|
| D-01 | `walkability.py \| grep -c "NO PATH"` | `10`, all `X<->render` (output ran in 0.1 s) | **OFF-PATH APPARATUS.** Render holds no tables by design (OD-33, 2026-08-27), so "0" may be unreachable by construction. |
| D-02 | `run_checks.py --list \| grep -c -i walkab` | `0` | OFF-PATH APPARATUS |
| D-03 | T-043 §3 command | `64 distinct; 34 name a next action` | OFF-PATH APPARATUS |
| D-04 | CLAUDE.md §4 UNWRITABLE block | `UNWRITABLE connection_targets.con_id -> empty table` | OFF-PATH APPARATUS (connections are T-050's retirement subject) |
| D-05 | `grep -c "writer yet, so until one exists" scripts/db.py` | `0` | ALREADY MET |
| D-06 | gaps.parameter_id / search_executions.gap_id | `[(1, 1)]` | ALREADY MET |
| D-07 | `db.py --help \| … grep -c cell-status` | `3` | ALREADY MET |
| D-08 | assess 3 × DEAF on a scratch copy | `REFUSING: no figure of parameter 3 is stated in this lens` | ALREADY MET (T-019's wrong-lens test not run [UNVERIFIED]) |
| D-09 | mobility rows of `base_taxonomy_identity` | `LMB, MOB, MOVE, SCI, VES`, none with a parent | **ON-PATH, in part:** `WHEEL` under `MOB` and `SCI` retired (T-102). `LMB→UPL` (T-116) and `MOVE`/`VES` (T-114) are off-path. |
| D-11 | `lang_jur_map` scope | `[(70, 0)]` | OFF-PATH (NEEDED-LATER, T-101) |
| D-12 | language spellings | `[(13, 13)]` | ALREADY MET |
| D-13 | AT-104 test file | `file=`, `rc=1` | OFF-PATH APPARATUS |
| D-14 | `git grep NOTATION_FAMILIES =` | no line; param 12 shows mm/cm/m | ALREADY MET |
| D-15 | T-009 probe | `False False`; `{'勾配'} {'경사로'} True` | ALREADY MET |
| D-16 | T-008 probe; `value_as_written` count | six `REFUSED`; `[(0,)]` | Probe ALREADY MET. Count half NEEDED-LATER (T-111): on the path only if the four figures are rendered. |
| D-17 | `scan_debt.py` | `EXAMINED: 580`, `DEBT: 457 pair(s)` | OFF-PATH (NEEDED-LATER). The engine already excludes skimmed rows from the value. |
| D-18 | synthesis/relation-candidates verb | `0` | OFF-PATH (T-032/T-033; one cell needs no relation rows) |
| D-19 | live specifications; test_db_integrity | `[(0,)]`, `rc=0` (passes on history only). On a scratch copy with the 3 × MOB row: `rc=1`, C10 FAILED. | **ON-PATH.** This line is the goal itself. Needs T-117 4a and/or T-104. |
| D-20 | T-037 after-tests | nothing to open | **ON-PATH**, reduced as in §2 E6 |
| D-21 | `skill_vocabulary_audit.py` | `rc=1`; `FAIL: 79 token(s) in 18 file(s)` | OFF-PATH APPARATUS |

Lines past D-21 that bear on the path, run read-only:

- **D-43** (strings): `assess_cell.py:3`, `adjudication_integrity.py:1`. On the path only if render prints
  engine prose; recommended not to.
- **D-44:** `◐ ● ◐`, then `0` (no ⚠ in the CHECK). **ON-PATH (T-117).**
- **D-50:** `(144,)` code-value extractions with no judged link, 63 of them parameter 3's. **ON-PATH for
  parameter 3's rows only.**
- **D-37:** `ALL` active. Off-path: parameter 3 has no `ALL` links.
- **D-49:** no `cell_figures`. Conditional (§4).

---

## 4. The candidate parameter, what it lacks, and the task count

Ranking query (read-only):
```
select x.parameter_id, t.canonical_en, count(*), count(distinct x.ref_id),
 count(distinct case when e.verification_status='VERIFIED' then x.ref_id end),
 count(distinct case when e.tier in (1,2) then x.ref_id end),
 sum(x.extraction_status in ('verified','reviewed')), p.accessibility_direction
from source_value_extractions x join evidence_sources e using(ref_id)
 join base_parameters p on p.parameter_id=x.parameter_id join terms t on t.term_id=p.term_id
where x.retired_at is null group by 1 order by 3 desc
```

**Parameter 3, ramp gradient**, keyed on `WHEEL`. [CONFIDENCE: high] Reasons:
- It holds the most extractions, sources, T1/T2 sources and verified readings.
- Its direction is recorded with a rationale citing four admitted sources.
- Its headline value is already stated by verified readings of verified sources.
- It has Co-1 sources (REF-00989, REF-00993, REF-01006, REF-01009).
- It has 50 search admissions and both kinds of zero-result search.

### What it lacks, in order
1. **A lens the umbrella test allows (E3).** `WHEEL` minted, and param 3's figures carried to it by
   judgment with warrants (T-102 scoped; this also does T-127's job for these rows).
2. **Verified or ⚠-marked governing sources (E2/E5).** Six UNVERIFIED (T-104). Any that cannot be
   retrieved needs T-117 4a.
3. **The correct marker (E5).** T-117.
4. **Population-match grades for the five ungraded governing refs, against `WHEEL` (E3, criterion).** In
   T-110's batch.
5. **Gate 1 resolved (E4).** In T-110's batch.
6. **Five translations of non-English claim texts (E2, CLAUDE.md three-things #2).** The T-112 slice, in
   T-110's batch.
7. **Zero-result searches classed, with the four unfired ones shown as deferrals (E1, criterion).** T-081.
8. **A page (E6).** T-037, reduced.

### Task count
**Core path: 6 tasks**, as separate PRs per rule 10:
- Tooling: **T-117**, **T-037-reduced**.
- Research: **T-102** (scoped to param 3's rows, or in full: the carry is the same verbs), **T-104**,
  **T-081**, **T-110** (one cell, carrying the T-112 and T-127 slices).
- Order: T-117 ∥ T-081 ∥ T-104 ∥ T-102, then T-110, then T-037-reduced.
- T-037-reduced can be built against a scratch database that holds the T-110 output before T-110 merges.

**Conditional, +5 tasks: T-124, T-036, T-108, T-086, T-111.** These apply if the first page must carry
OD-63's four figures (minimum, mode, median, maximum, colour-coded on the surveyed code bodies). Without
the unit-cell cleanup, the four figures would be taken over 11 of 35 governing claims. They would then be
**wrong figures in the book**, so the conditional set comes as a block or not at all.

**Route A, which drops T-102.** Key the cell on `MOB` after a recorded design-equivalence judgment for
parameter 3. Some admitted evidence supports this: the parameter's own direction rationale says *"NOT
contested: no admitted source identifies a population for whom a steeper ramp is better"*. But the ledger
(line 1197, ruling of 2026-08-25, "not to be relitigated") states the opposite as its paradigm case. A
delegate should not settle that, so it is an **owner question**. The judged-link work, the T-127 slice,
is needed either way.

**Plan dependencies to drop for this path** (they serve the whole corpus, not one cell):
- T-110's deps T-059, T-068, T-123, T-127 (whole), T-128 (withdrawn by OD-87) and T-133.
- T-117's deps T-068 and T-120. T-117's code reads neither; T-102 is needed only for the parent match in
  `population_match`.
- T-037's deps T-032, T-036, T-122 and T-124 (conditional).

Why T-059 is off the path for parameter 3, under item 6's rule (most accommodating identified value from
any tier):
- The selected value is the same 5 %. No identified T1, Co-1 or T2 value is gentler: REF-01005 states
  1:20, REF-01001 5.5 %, REF-01006 1:12.
- No admitted source states harm at 5 %.
- Ceilings that can all be met are not divergent (OR-6b).

[CONFIDENCE: medium] I read the engine's output, not every branch of `compose_value`.

---

## 5. Recommendations

1. **First published determination: parameter 3 × `WHEEL`, `provisional`, ⚠.** OD-10 makes `provisional`
   mean thin evidence, so publishing a provisional cell is honest.
   [CONFIDENCE: high] for the parameter. [CONFIDENCE: medium] for `WHEEL` having enough figures after the
   carry: OD-31 puts a clause that names no one under its heading's group, often `MOB`, so the `WHEEL`
   cell may hold fewer code values than the 116 `MOB` links suggest. Not measured.
2. **Run T-117 as written, without waiting for T-068 or T-120.** [CONFIDENCE: high] Without it a wrong
   marker reaches the book, and C10 refuses the live row: confirmed `rc=1` on a scratch copy.
3. **Run T-102 now, as a carry-only batch (OD-84), not deferred to "the full corpus".** [CONFIDENCE: high]
   The group named by a ramp-gradient determination at `MOB` is a group the ledger says is not one for
   this parameter.
4. **Run T-104 for the six governing UNVERIFIED sources; T-081 for the eight circulation-slug zero rows.**
   [CONFIDENCE: high] for T-081: four of the "empty searches" were never run. [CONFIDENCE: medium-high]
   for T-104: with T-117 4a a ⚠ is honest about the basis, but a printed citation from an unverified row
   can still be wrong (CLAUDE.md §5(c)).
5. **Build T-037 reduced, not T-037 as written.** [CONFIDENCE: medium] The criterion is met without a
   render table, hash check, discussion rows or page-language parameter. Each of those is apparatus until
   a second page exists (CLAUDE.md §8). Whether the owner accepts a first page without OD-63's four
   figures is the owner question below.
6. **The page prints no engine prose fields.** [CONFIDENCE: medium] This avoids touching T-068 item 8 for
   now. The stored `value_note` and `falsification_condition` contradict the 2026-11-14 rulings and
   misreport "24 … no parsable numeric bound".
7. **Defer every other open task until the page exists.** Re-classify after it, against what the page
   showed was wrong. [CONFIDENCE: medium] This rests on my reading of each task's purpose line, not on a
   per-task proof (the classifier tasks cover that).

**Owner questions (plain):**
- (Q1) May the first published page omit the four figures of OD-63 and show the stated value with its
  sources? Yes keeps the path at 6 tasks; no makes it 11.
- (Q2) Does parameter 3 at `MOB` pass the design-equivalence test? The admitted evidence names no
  population that is better served by a steeper ramp; the ledger's 2026-08-25 example says it fails. Yes
  drops T-102 from the path; no keeps it.

---

## 6. What I could not verify

- Whether a `3 × WHEEL` cell after the carry has enough figures to compose a value (the carry has not been done).
- Whether every **blocking** gate passes with a live row. I ran only `test_db_integrity` (C10 fails),
  `adjudication_integrity` (PASS, `EXAMINED: 59`) and `derivation_handshake_integrity` (`EXAMINED: 2`) on
  a scratch copy holding the row. Not run: the full `run_checks.py` or `--selftest`.
- How T-059's rewrite would change `rests_on_proxy_inference` and the marker under OD-59. The marker
  could fall to the stating sources' band, ○ for T6, except that T-117's "thin" rule gives every
  PROXY-graded governing code ⚠. I took T-117's reading.
- T-019's wrong-lens test (part of D-08). The full text of the render contract
  (`RENDER-CONTRACT-parameters-3-and-12.md`) and T-102-design.md §6 (read only in summary).
- Whether `walkability.py` measured anything: it ran in 0.1 s and printed a matrix.
- Why `translations` holds 197 `reviewed` rows while `v_translations_current` shows 93. 104 are
  superseded; I did not check whether any superseded one is the only English for a row.
- The OD-63 four figures for parameter 3: not computed (`cell_figures` does not exist).

---

## Summary (under 150 words)

Parameter 3 (ramp gradient) is the clear candidate: 122 extractions, 58 sources, a recorded direction,
and a 5 % / 1:20 headline stated by verified readings. The engine already determines it on a scratch
copy. Three wrong things would reach the book: the group `MOB`, which the ledger says fails the umbrella
test for this parameter; the marker ○ where the owner's table requires ⚠, which the schema cannot store;
and lens links that are all `carried`, never judged. A live row also fails integrity check C10 today.
Nothing renders. The core path is six tasks: T-117 and a reduced T-037 (tooling); T-102, T-104, T-081
and T-110 (research, carrying slices of T-112 and T-127). OD-63's four figures would add five more. Of
the D-01..D-21 lines, D-09 (in part), D-19 and D-20 are on the path; eight are already met; the rest are
apparatus or later work. Two owner questions (Q1, Q2) decide the length.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/path-to-one-determination.md
