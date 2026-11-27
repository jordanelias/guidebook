# Antagonist 4: attack on the four classifications of the remediation plan, and on the path-finder's report

Read-only. Repository /home/user/guidebook, branch ccr-64231823-gqy3xr at cd34b96; origin/main at 1d52215d (the merge of PR #248). Schema user_version 167. Canonical database sha256 3d419efb…edb9, the same before and after this pass. The engine ran only on scratch copies under scratchpad/a4/ (r3.db, r12.db). Every figure below was read on 2026-11-27 and comes with the command that produced it. Re-run the command; do not trust the figure (rule 7a). `R` means `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`.

Coverage: 73 rows across the four files, and every open-tasks.tsv id appears exactly once. No duplicates and no omissions (`comm -3` of the two sorted id lists printed nothing). The classifiers' class counts, derived with `cut -f2 a4_classes.tsv | sort | uniq -c`: NEEDED-NOW 12, NEEDED-LATER 35, APPARATUS 21, ALREADY-DONE-OR-SUPERSEDED 5, OWNER-HOLD 0. My verdicts, derived with `cut -f3 a4/verdicts.tsv | sort | uniq -c`: SURVIVES 57, WOUNDED 15, FALSE 1.

## Table (the 73 tasks)

| id | classifier class | verdict | corrected class | reason |
|---|---|---|---|---|
| T-005 | APPARATUS | SURVIVES | - | Determination views filter retired_at; v_code_floor_only no longer exists; v_gap_subject reads retired specs only to locate a gap's subject |
| T-027 | APPARATUS | SURVIVES | - | c9c84466 (partial) was reverted; the real E2 harm (code_currency_status NULL on all 59, all 27 governing) is research no task holds |
| T-032 | NEEDED-LATER | SURVIVES | - | connections and conflicts hold 0 rows; one cell needs no relation rows |
| T-033 | APPARATUS | SURVIVES | - | No relation writer exists to consume candidates |
| T-035 | NEEDED-LATER | SURVIVES | - | Skill drift is real; no live figure is wrong because of it |
| T-036 | NEEDED-LATER | WOUNDED | OWNER-HOLD | OD-63 (owner, 2026-11-14) puts per-jurisdiction colour coding on the render; on the path unless the owner relaxes it (path-finder Q1) |
| T-037 | NEEDED-NOW | SURVIVES | - | Nothing renders; the reduced form contradicts OD-63 unless the owner relaxes it |
| T-038 | APPARATUS | SURVIVES | - | Gate on the stage map; nothing book-facing reads it |
| T-039 | APPARATUS | SURVIVES | - | Rests on delegated OD-20 only; no owner request found |
| T-040 | APPARATUS | SURVIVES | - | 0-row tables; deletion is optional |
| T-047 | APPARATUS | SURVIVES | - | Tests a code property |
| T-052 | NEEDED-LATER | SURVIVES | - | add-locator has no --jurisdiction flag (confirmed); the task stops on it |
| T-053 | NEEDED-LATER | SURVIVES | - | 0 conflicts |
| T-056 | NEEDED-LATER | WOUNDED | NEEDED-NOW (item 3a only) | Probe: 3xMOB and 12xMOB both write design_scale=universal; OD-48 (a) ratified 2026-11-19 makes that "for everyone": a wrong group on the first row |
| T-057 | NEEDED-LATER | SURVIVES | - | Base acceptance, not a determination |
| T-058 | NEEDED-LATER | SURVIVES | - | Waits on T-116; not parameter 3 |
| T-059 | NEEDED-NOW | SURVIVES | NEEDED-NOW (slice) | Probe: four in-lens T3 grey sources stating ramp maxima (REF-01025 states 1:20) are neither governing nor supporting: the printed source list contradicts U1/OD-58 |
| T-060 | NEEDED-LATER | SURVIVES | - | Needs several parameter determinations first |
| T-062 | APPARATUS | SURVIVES | - | The gate is apparatus, but its 27 rows are all parameter 3 (see T-105) |
| T-068 | NEEDED-LATER | SURVIVES | - | Engine writes only pending_assessment; nothing says "converge" |
| T-069 | NEEDED-LATER | SURVIVES | - | Future non-English search only |
| T-070 | APPARATUS | WOUNDED | NEEDED-LATER (owner-only to defer) | Serves "verify we recorded accurately" (goal, 2026-11-20); owner answered OR-15 and OD-44 to launch it |
| T-071 | NEEDED-LATER | SURVIVES | - | Roots feed T-068 only |
| T-072 | NEEDED-LATER | SURVIVES | - | Widens the parameter list |
| T-081 | NEEDED-NOW | SURVIVES | - | Four searches that never ran (87, 133, 138, 191) have no typed home: amend-search has no deferred-reason flag and absence_class has no "not run" value |
| T-082 | NEEDED-LATER | SURVIVES | - | Parameter 4 only |
| T-084 | APPARATUS | WOUNDED | NEEDED-LATER | OD-46 answered by the owner 2026-11-19 with the action itself; a ratified owner action is not apparatus; the hold is stale |
| T-085 | APPARATUS | SURVIVES | - | add-lang-jur-pair already calls check_jurisdiction (db.py:9916) |
| T-086 | NEEDED-NOW | WOUNDED | NEEDED-LATER (conditional) | The 4 ratio claims are REF-01008, T3 grey, not in the governing set; "four code maxima" is false; the headline is unchanged |
| T-087 | NEEDED-LATER | SURVIVES | - | Parameters 5, 6, 9, 12 |
| T-091 | NEEDED-LATER | SURVIVES | - | One home-setting governing source (REF-00997) on parameter 3; not the headline |
| T-092 | NEEDED-LATER | SURVIVES | - | Blocked on T-091 |
| T-101 | NEEDED-LATER | SURVIVES | - | Engine does not read scope |
| T-102 | NEEDED-NOW | SURVIVES | - | Ledger line 1197: MOB fails the umbrella test for ramp gradient; T-110 item 2 keys on a child |
| T-104 | NEEDED-NOW | WOUNDED | NEEDED-NOW (rescoped) | REF-01026 is a transcription of REF-01032 (GAP-376): supersede, not verify; REF-00997 was 403 twice plus Wayback; REF-01015 is VERIFIED with the wrong edition and year, and is missing from the list |
| T-105 | NEEDED-LATER | WOUNDED | NEEDED-NOW (parameter-3 slice) | verified_scan_integrity: all 27 VERIFIED-WITHOUT-FULL-READING rows and 93 of 103 NO-COVERING-READING rows are parameter 3, including headline row 30 |
| T-106 | NEEDED-LATER | SURVIVES | - | Parameter-3 identity carry is T-102's |
| T-107 | NEEDED-LATER | SURVIVES | - | Future searches only |
| T-108 | NEEDED-NOW | WOUNDED | OWNER-HOLD (Q1) | Headline unchanged (no unparsed claim is gentler than 1:20); subject is 33 rows, not 35; on the path only if OD-63's four figures are shown |
| T-109 | APPARATUS | WOUNDED | APPARATUS (DEFER, not RETIRE) | T-143, kept by C4, needs parameter 3's quantity_kind, which is T-109's data |
| T-110 | NEEDED-NOW | SURVIVES | - | The deliverable; C3's "no Co-1 on ramp gradient" is false (4 Co-1 sources, coded tier 1 evidence_type co1) |
| T-111 | NEEDED-NOW | WOUNDED | OWNER-HOLD (Q1) | REF-01017 is already a governing ref and its 5 % equals the headline; row 30's real defect is GAP-372 truncation |
| T-112 | ALREADY-DONE-OR-SUPERSEDED | FALSE | NEEDED-NOW (parameter-3 five) | 11 live non-English claim texts have no current reviewed translation: the reviews were superseded by rejections citing truncated originals (GAP-372 OPEN) |
| T-113 | NEEDED-NOW | WOUNDED | NEEDED-NOW if jurisdictions are shown (OD-63) | Scope is incomplete: REF-00997 (des.sa.gov.au, South Australia, governing) and REF-00996 (Flemish handbook) are also filed under their country |
| T-114 | NEEDED-LATER | SURVIVES | - | No row carries MOVE or VES |
| T-115 | NEEDED-LATER | SURVIVES | - | No ALL link on parameter 3 |
| T-116 | NEEDED-LATER | SURVIVES | - | Class holds; its recommendation to retire the 6 LMB crossings is a population-taxonomy act (decision-protocol 2.4 item 2) |
| T-117 | NEEDED-NOW | SURVIVES | - | C10 refuses a live row with an unverified governing source and REF-00997 is unretrievable; "every determination carries a wrong marker" is not shown for 3xMOB (OD-59: the value's own sources are verified T6, so circle) |
| T-118 | APPARATUS | SURVIVES | - | Internal names, by its own text |
| T-120 | NEEDED-LATER | SURVIVES | - | Item 2a is on origin/main (PR #248 merged as 1d52215d); the caller's "open PR" premise is false |
| T-122 | APPARATUS | SURVIVES | - | Contract YAML only |
| T-123 | NEEDED-LATER | SURVIVES | - | Parameters 3 and 12 already have directions |
| T-124 | NEEDED-LATER | WOUNDED | OWNER-HOLD (Q1), NEEDED-NOW by default | OD-63 (owner-answered 2026-11-14) says what the render shows; it postdates DR-2026-08-19, so rule 0 binds |
| T-125 | NEEDED-LATER | SURVIVES | - | Fold into T-059 |
| T-127 | NEEDED-NOW | SURVIVES | - | 63 parameter-3 code figures carry only an unjudged MOB link; the T-149 wait rests on OD-88, whose CHECK is pending (CLOSED by the gate) |
| T-128 | ALREADY-DONE-OR-SUPERSEDED | SURVIVES | - | OD-87 withdrawal, CHECK confirmed (ledger 8600-8602) |
| T-129 | APPARATUS | WOUNDED | APPARATUS (DEFER; retirement owner-only) | Traces to the owner's Q2 of 2026-11-16; T-131 (C4) plans to use merge-term |
| T-130 | APPARATUS | WOUNDED | APPARATUS (DEFER; retirement owner-only) | The owner asked for "an iterative loop with limited repetitions" in those words |
| T-131 | NEEDED-LATER | SURVIVES | - | "paso libre" is held by both TERM-021 and TERM-002 |
| T-132 | APPARATUS | SURVIVES | - | 0 live determinations |
| T-133 | NEEDED-LATER | SURVIVES | - | Gate 1 is on MOB; a parent's gate does not reach a WHEEL cell (_open_gates), so item 1 is off route B |
| T-135 | APPARATUS | SURVIVES | - | OD-69 resolved and confirmed; the TSV status is stale |
| T-136 | NEEDED-LATER | SURVIVES | - | Question 7 is open but does not block: the engine reads accessibility_direction whatever direction_ref_id holds |
| T-137 | NEEDED-LATER | SURVIVES | - | Lengths and gradients are covered |
| T-138 | NEEDED-LATER | SURVIVES | - | Parameter 3 has no ALL link; "item 1 NEEDED-NOW" was never C4's class |
| T-139 | APPARATUS | WOUNDED | NEEDED-LATER (retirement owner-only) | Implements ratified adjudication-3 item 55 and the owner's schema-shape ruling of 2026-11-06 (CLAUDE.md section 4 names "a correction appended to a note") |
| T-140 | APPARATUS | SURVIVES | - | build_graph --check red on main; nothing book-facing |
| T-141 | APPARATUS | SURVIVES | - | Mostly blank-string CHECKs; items ratified 2026-11-19, so owner acknowledgement is advised |
| T-142 | NEEDED-LATER | SURVIVES | - | No attested instrument forms |
| T-143 | NEEDED-LATER | SURVIVES | - | The 4 degree rows are conditions and a finding |
| T-145 | ALREADY-DONE-OR-SUPERSEDED | SURVIVES | - | Merged in PR #244; migrations 165 and 166; 65 rows |
| T-147 | ALREADY-DONE-OR-SUPERSEDED | SURVIVES | - | Merged in PR #246; migration 167; verbs present |
| T-148 | ALREADY-DONE-OR-SUPERSEDED | SURVIVES | - | Merged in PR #247; base_icf 136 rows, 105 parented |

## Findings, worst first (one block each)

### F1. T-112 "ALREADY-DONE" is false. Eleven live non-English figures have no current English rendering, five of them on parameter 3, including a source of the headline (CRITICAL, L6/L2)
- Claim (classify-3.md, T-112 row): "Every live non-English figure has a reviewed translation; the 23 rows left untranslated are English."
- Failure: the classifier counted every `translations` row with status `reviewed`, superseded rows included. The live set is `v_translations_current` (rows with `superseded_by_translation_id IS NULL`). It holds 93 rows, and 104 rows are superseded. Joined against live extractions whose source language is not English, it leaves 11 with no current reviewed translation: extractions 30, 112 and 115 (nl), 102, 141 and 202 (es), 105 (fr), and 207, 208, 209 and 215 (ko). In each case the reviewed translation was superseded by a **rejection** whose `review_reason` reads "original cell is truncated". Extraction 30 (REF-00995, the Flemish decree) is one of the two verified readings that state the 5 % headline, and its stored quote drops the stem that carries the inequality ("Het hellingspercentage bedraagt hoogstens"). Extraction 105 (REF-01030) is the French 5 % governing claim.
- The defect is registered as GAP-372 (OPEN), which lists exactly those 11 ids. `git grep -n GAP-372 -- workplan/2026-11-12-bidirectional-pipeline` prints nothing: **no task in the plan covers it.** `claim_text` is in `_NOT_AMENDABLE_SVE` (scripts/db.py:12771), so the repair is to retire the row and add it again with the full quote. A new translation of the truncated cell would be rejected again.
- The path-finder's T-112 slice ("`request-translation` / `record-translation` / `review-translation` for five rows") inherits this flaw: it is a sequence failure (S4). The quote has to be repaired before it is translated.
- Command: the Python join in this pass over `v_translations_current` (shown in the transcript); `R.execute("select gap_id,status,description from gaps where gap_id='GAP-372'")`; `R.execute("select translation_id,status,review_reason from translations where translation_id in (83,190,30,136)")`.

### F2. Two instruments are counted twice among the governing sources of the probe cell, and one row carries a false edition (HIGH, L3/L1; uncovered by any task)
- The 3×MOB probe (scratchpad/a4/r3.json; `specification_source_links` of specification 9 in scratchpad/a4/r3.db) governs on 27 refs, including:
  - REF-01026 and REF-01032. Both are Decreto-Lei 163/2006. REF-01026 is the Ordem dos Arquitectos transcription, UNVERIFIED, and its own note says its extractions were "re-rooted to REF-01032". GAP-376 (OPEN) records the duplicate.
  - REF-01015 and REF-01018. REF-01015 is stored as VERIFIED, pub_year 2022, but its own note reads "pub_year, pub_title and institution on THIS ROW ARE WRONG … actually … Technical Guidance Document M … 2010 … ceased to have legal effect on 1 January 2024 … cite THAT row [REF-01018], not this one."
- Wrong things that reach the book: Portugal and Ireland each counted twice among the governing sources; a lapsed 2010 Irish instrument printed as a 2022 one; and, under OD-63's mode and median, two duplicated votes. `superseded_by_ref_id` is NULL on both duplicates. The analogous Korean pair (REF-01019 to REF-01031) has it set, and REF-01019 does not govern.
- `git grep -n "REF-01015\|REF-01026" -- workplan/2026-11-12-bidirectional-pipeline` prints nothing. T-104 lists REF-01026 as a source to *verify*, which is the wrong action, and does not list REF-01015 at all.
- Command: `R.execute("select ref_id,pub_year,superseded_by_ref_id,verification_status,substr(notes,1,300) from evidence_sources where ref_id in ('REF-01015','REF-01018','REF-01026','REF-01032','REF-01019','REF-01031')")`.

### F3. The path-finder drops T-059, but the probe cell's printed source list contradicts the owner's Unification (HIGH, L4/L2)
- Path-finder §4: "Why T-059 is off the path for parameter 3 … The selected value is the same 5 %."
- The value is the same; the governing sources are not. Four T3 grey sources with in-lens parameter-3 claims, all linked `MOB` (extractions 56, 60–64, 67, 93, 94, 101, 102), are in the engine's `source_records` but in neither the governing nor the supporting links. Among them, REF-01025 states 1:20, the headline value itself.
- U1 (ledger 7870) and OD-58: tier sets the marker and the weight, not eligibility. DR-2026-08-19 §4 publishes "its governing sources". A page built on today's engine omits eligible sources that state the headline. Classifier 1 is right that T-059 (or its selection slice) is on the path.
- Command: run `assess_cell.py` on a copy (as in scratchpad/a4/), then `select ref_id, role from specification_source_links where specification_id=9`, and compare with `[r['ref_id'] for r in json.load(open('r3.json'))[0]['source_records']]`.

### F4. design_scale = 'universal' on a mobility group's cell (HIGH, L7/L5; T-056 item 3a orphaned by the path-finder)
- The probe writes `design_scale: universal` for 3×MOB (and for 12×MOB, scratchpad/a4/r12.json).
- OD-48, answered by the owner on 2026-11-19 (ledger 7995–7996), took recommendation (a): `universal` states "whom it is for", meaning no identity (`OPEN-DECISIONS-ADJUDICATION-3.md:136`). Under it the stored row says the ramp maximum is for everyone while being keyed to a mobility group. Wheelchair users would not recognise "universal" as their cell.
- Classifier 1 moves T-056 item 3a into T-059. The path-finder drops T-059 and never mentions 3a. Whether the line at `assess_cell.py:1489` is reached for a 3×WHEEL cell is [UNVERIFIED], because no WHEEL code exists to probe. The 12×MOB run (regulatory_stratum_only=1) goes through exactly that branch.

### F5. The ⚠ marker for 3×MOB is asserted, not derived. The path-finder settles an owner-reserved question (HIGH, L4; doctrine)
- Path-finder §0: "Wrong marker … ⚠ in place of the circle"; §6: "T-117's 'thin' rule gives every PROXY-graded governing code ⚠. I took T-117's reading." Classifier 3, T-117 row: "Every determination published today would carry a wrong marker."
- `governance/tier-system.md` §5 on origin/main: "the value shown carries the marker of its own source, with ⚠ only where that value's own basis is grey, unverified or thin (OD-59)". It also lists as **"Not yet ruled (owner): … whether every PROXY grade makes a value thin; … whether a `provisional` cell … is thin in the ⚠ sense."**
- The 5 % value is stated by REF-00992 and REF-00995, both T6 and VERIFIED, so ○ under OD-59. That is what the engine writes. The same 1:20 is also stated by REF-00994 and REF-01014 (T4, UNVERIFIED). Which source is "the value's own" is likewise unruled.
- So the "wrong marker" is not established for this cell, and choosing ⚠ for PROXY decides what the owner left open (decision-protocol §2.4 item 3, evidence-tier definitions). T-117 stays necessary for other reasons: C10 refuses a live row with any UNVERIFIED governing source, and REF-00997 is unretrievable (F7).

### F6. The four figures (OD-63) are an owner ruling, not an open option. T-124 "NEEDED-LATER" and the "six-task" headline invert rule 0 (HIGH, doctrine)
- OD-63, ANSWERED BY THE OWNER (ledger 7421–7422): "the render shows the minimum, mode, median and maximum as a colour code on the surveyed jurisdictional code bodies." It postdates DR-2026-08-19 §4.
- Classifier 3 (T-124: "DR-2026-08-19 §4's acceptance … does not [need them]") and the path-finder (six tasks, with OD-63 as conditional Q1) both rest on the older text. The path-finder at least asks Q1. Under rule 0 the default is the longer path: T-124, T-036, T-108, T-086, T-111 and T-113 are on it until the owner relaxes OD-63.
- Under that default, F2's duplicates and F8's incomplete T-113 also corrupt the per-jurisdiction colour code.

### F7. T-104's six sources: one should be superseded, one is unretrievable, and one is a draft (MEDIUM, L1)
- The list is confirmed: REF-00994, REF-00997, REF-01013, REF-01014, REF-01016 and REF-01026 are the UNVERIFIED governing refs of the probe (`select ref_id from specification_source_links j join evidence_sources e using(ref_id) where specification_id=9 and e.verification_status<>'VERIFIED'` on scratchpad/a4/r3.db).
- REF-01026 is a duplicate: retire it to REF-01032 rather than verify it (F2). REF-00997's `verification_note` reads: "the publisher URL returned HTTP 403 on 2026-09-18 and again on 2026-11-20 … and the Wayback snapshot …". REF-01014's title says "(DRAFT PROPOSAL)".
- Consequence: C10 cannot pass by verification alone. Either REF-00997 leaves the governing set, or T-117 item 4a (⚠ accepted by C10) lands. The owner's words "let's return to keeping them but they get a triangle warning" (ledger 7005) support 4a.

### F8. T-113 names four sub-national instruments; there are more (MEDIUM, L1/L5)
- REF-00997 has URL des.sa.gov.au (the South Australian government) and is filed `AU`. It is a governing ref of the probe.
- REF-00996 has URL toegankelijkgebouw.be (the Flemish accessibility handbook) and is filed `BE`. It holds 2 parameter-3 rows.
- `base_jurisdictions` holds 0 sub-national codes (`select kind,count(*) from base_jurisdictions group by 1` gives country 32, meta 4).
- REF-00992 (England) and REF-00995 (Flanders) are also the two sources that state the headline and that govern parameter 12. Any jurisdiction shown beside them is wrong today.

### F9. The VERIFIED-WITHOUT-FULL-READING debt is on parameter 3, contrary to classifier 2's T-105 reasoning (MEDIUM, L2)
- Classifier 2 classed T-105 NEEDED-LATER because "parameter 3 has no NOT-READ or READ-PARTIAL pair". That is true of `scan_debt.py`, a different instrument.
- `python3 scripts/audit/verified_scan_integrity.py`: all 27 VERIFIED-WITHOUT-FULL-READING rows are parameter 3, including headline row 30 and the governing rows of REF-00988, -00990, -00991, -00994 and -00997. Ninety-three of the 103 NO-COVERING-READING rows are parameter 3 (`… | awk '/NO-COVERING-READING/{f=1;next} f' | grep -o "(3, [0-9]*)" | wc -l` gives 93).
- The path-finder does not mention this. If the page prints extraction status, "verified" is false for those rows under OR-11a.

### F10. T-081 cannot be done "data only, about one hour" (MEDIUM, L8/S4)
- Path-finder §2 E1: "List 87, 133, 138 and 191 as deferrals owed a re-run. Data only."
- `python3 scripts/db.py amend-search --help` offers `--set-absence-class {genuine_absence,query_shape_failure,wrong_index}` and no deferred-reason flag. No vocabulary value means "not run".
- All 203 rows have `absence_class` NULL; one row (exec 9) carries `deferred_reason` (`select count(*), sum(absence_class is null), sum(deferred_reason is not null) from search_executions` gives 203, 203, 1).
- The four non-searches can be typed only by a tooling change (rule 10, a separate PR first) or by re-running them as new searches. Classifier 2 found this defect in the task file, and it holds.

### F11. T-086's harm is misdescribed (MEDIUM, L4)
- Classifier 2: "four code maxima and seven findings for the same quantity are silently out of the interval."
- The four `ratio` claims (extractions 60, 61, 62, 64) are REF-01008, tier 3, evidence_type grey: not code maxima, and not in the governing set (F3). Fixing their unit changes nothing on today's cell. Its effect depends on T-059 (eligibility) and OD-63 (four figures).

### F12. Classifier 3's T-108 subject count is wrong, and its harm is conditional (LOW, L2)
- Classifier 3: "It returns 35 rows (ids 72 to 114)". Today the task's own selector returns **33** rows: 27 claims, 4 conditions and 2 findings, all parameter 3, retired rows included (`select parameter_id, figure_role, count(*) from source_value_extractions where retired_at is null and (length(claimed_unit)>20 or claimed_unit like '%(%' or claimed_unit like '% where %') group by 1,2`).
- Its "wrong thing": "computed on about 60 % … the code minimum, the maximum and the convergence would all be wrong". The headline holds, because no unparsed claim is gentler than 1:20 (`select … where parameter_id=3 and figure_role='claim'` lists none below 5 %). The harm arises only under OD-63's figures.
- The overall figure of 48 of 122 live ramp figures with a unit outside `base_units` is confirmed (`(122, 48)`): 11 `ratio`, 4 `degrees` and 33 sentences.

### F13. Classifier 3 says ramp gradient holds no Co-1 source; it holds four (LOW, L4)
- `select tier, evidence_type, count(*) from evidence_sources where ref_id in (select ref_id from source_value_extractions where parameter_id=3) group by 1,2` returns (1, 'co1', 4): REF-00989, -00993, -01006 and -01009, all supporting.
- T-110 §9's Co-1 stop is still not triggered, because no Co-1 figure states the selected bound.

### F14. T-127 "now waits for T-149" relies on a resolution the plan's own gate reads as CLOSED (LOW, S4)
- OD-88 CHECK: pending (ledger 8632), and OD-89 likewise. By the gate function in every task file (RESOLVED UNDER DELEGATION plus a check that is not `confirmed` or `not required` prints CLOSED), OD-88 is not in force.
- OD-87 (CHECK confirmed) made T-127 wait for PR 246 or T-148, and both have merged (71b7c582, 4645a618). T-149 and T-150 have no task file (`ls tasks | grep -E 'T-149|T-150'` prints nothing). The parameter-3 slice of T-127 is unblocked.

### F15. Classifier 4's "critical few #1" (T-133 item 1) and "unlisted hold" (owner question 7) do not bind route B (LOW)
- Gate 1 is keyed `MOB` (`select * from determination_gates`). The `_open_gates` docstring (scripts/assess/assess_cell.py:688): "a gate on the parent's code does not reach a child's cell". A 3×WHEEL cell is not reached by gate 1, so neither T-133 item 1 nor GAP-016 is on route B. On route A (MOB) the gate binds, and the stale-tier risk is reported by the advisory parity check, as classifier 4 says.
- Owner question 7 (workplan/2026-11-06-run-pipeline-round-2-adjudication.md:96–106) is unanswered: `git grep -n "R2-8\|backfill-ref-id" -- references/project-standards.md` prints nothing. It concerns backfilling a *warrant*. The engine reads `accessibility_direction` whatever `direction_ref_id` holds (skills/run-pipeline_SKILL.md:392–394), and parameter 3's rationale cites REF-00996, REF-00987 and REF-00994 in prose. It does not block a determination.
- The caller's brief lists "T-133 item 1" and "T-138 item 1" among the NEEDED-NOW classes. Classifier 4 classed both NEEDED-LATER, so that premise is false.

### F16. The caller's premise that T-120 item 2a sits only in open PR #248 is false (LOW)
- `git log origin/main -1` is `1d52215d Merge pull request #248` (2026-11-26 19:48 -0600, which is 2026-11-27 01:48 UTC). `git show origin/main:governance/tier-system.md` carries the owner's table and the "Until T-117 lands" sentence.
- Classifier 3 ("item 2a … already landed on 2026-11-26") survives: the commit 183a6d66 is stamped 2026-11-26 22:41 and the merge is 2026-11-26 in local time.

### F17. Retirements that reverse an owner act (MEDIUM, doctrine; see DOCTRINE LIMITS)
- T-130: the owner asked, in his own words, "is there an iterative loop with limited repetitions" (PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md:28, Q2 of 2026-11-16).
- T-129: traces to the same Q2 and Q4.
- T-139, T-140 and T-141: adjudication-3 items 55, 28/29/87 and 16–63, ratified by "Sure, append. Ratify all." (ledger 7967ff; the reading that this covers items 12–91 is itself marked [ASSUMPTION]).
- T-070: the owner answered OR-15 and OD-44 ("apply recommendations") to launch it.
- T-084: OD-46 is the owner's answer and orders the act.
- CLAUDE.md §8 and the owner's 2026-11-25 statement ("the project is simple") arguably license deleting code. But deleting a task the owner asked for by name, or ratified, is not a decision a classifier makes. List these OWNER-ONLY.

### F18. The open-task list is stale (MEDIUM, L1)
- Derived from git independently of the generator:
  - T-145: merge 778e1626, PR #244; migrations 165 and 166.
  - T-147: 263baa55 in PR #246 (71b7c582); migration 167.
  - T-148: 86d714ad and 903884b8 in PR #247 (4645a618).
- All three are on origin/main yet listed open. T-128 is listed open though withdrawn (OD-87). T-135's status "OWNER: OD-69" is stale (OD-69 CHECK confirmed, ledger 8016–8017). T-084's HELD banner is stale (OD-46 answered, ledger 7989–7990). The deps column still lists T-128 for T-059, T-110 and T-127, whose files already say "T-128 is withdrawn, so this task no longer waits for it".
- T-112 is **not** done (F1), so the stale set is not "everything a classifier called done".


## WRONGLY RETIRED OR DEFERRED (the wrong thing that would reach the book)

- **T-112 (called done).** Five parameter-3 figures (30, 102, 105, 112, 115) would be published with no English beside them, or with an English rendering the independent reviewer rejected because the stored original is truncated (F1). Extraction 30 is a headline source.
- **T-056 item 3a (deferred inside a NEEDED-LATER task).** A mobility group's cell stored as `universal`, which means "for everyone" under OD-48 (F4).
- **T-105, parameter-3 slice (NEEDED-LATER).** Twenty-seven parameter-3 rows marked `verified` with no full reading recorded, one of them the headline row (F9).
- **T-070, T-084, T-129, T-130, T-139 (APPARATUS).** None puts a wrong figure in the book. Each reverses or ignores an owner act (F17), so it is wrongly classed rather than wrongly harmless. T-084's own book harm is nil: `set_pair_scope` does not read the registry (scripts/db.py, `def set_pair_scope`, 0 calls to `check_jurisdiction`).
- **T-109 (RETIRE).** Nothing wrong reaches the book today, but retiring it strands T-143, which classifier 4 keeps. Defer, do not retire.
- **Survived the attack:** T-005, T-027, T-033, T-038, T-039, T-040, T-047, T-062, T-085, T-118, T-122, T-132, T-135, T-140, T-141 (as to book harm), T-128, T-145, T-147, T-148. [NULL: their files' "Today" evidence and the probes named in the table: examined, no book-facing wrong thing found.]

## WRONGLY KEPT (NEEDED-NOW that is not, or not unconditionally)

- **T-086:** its four claims are T3 grey and outside the governing set; the headline is unchanged (F11). Conditional on T-059 and OD-63.
- **T-108 and T-111:** the headline is unchanged; they are on the path only under OD-63's figures (F12). T-111's row 30 is better repaired through GAP-372 (F1).
- **T-113:** on the path only if jurisdictions are shown, which OD-63 makes the default. Its scope is incomplete (F8).
- **T-133 item 1 and T-138 item 1:** never classed NEEDED-NOW by classifier 4. Off route B (F15).
- **Survived:**
  - T-037: nothing renders (`git ls-files | grep -i -E 'render|template|site'` finds no generator).
  - T-059: F3.
  - T-081: F10.
  - T-102: ledger line 1197; T-110 item 2.
  - T-104: rescoped (F7).
  - T-110: the deliverable.
  - T-117: C10 plus REF-00997, though the 3×MOB marker claim is wounded (F5).
  - T-127: 63 parameter-3 code figures, each with only `MOB carried` (one also `A-EFFORT`); `select basis,count(*) from extraction_lens_links where retired_at is null group by 1` gives carried 216.
- Claims (a) to (h) of the brief, tested:
  - (a) 48 of 122: true, but 4 are degrees and 11 are T-086's, so 33 are T-108's.
  - (b) four sub-national: true but incomplete (F8).
  - (c) six UNVERIFIED: true, though one should be superseded and one is unretrievable (F7).
  - (d) eleven bare ratio rows: true (52, 53, 54, 57, 58, 60, 61, 62, 64, 65, 66), but the four claims are T3 grey and not governing (F11).
  - (e) searches 87, 133, 138, 191 never ran: true (findings_note: "AN UNFIRED QUERY", "RETRIEVAL FAILURE, NOT ABSENCE" ×3).
  - (f) `band()` and the marker CHECK refuse ⚠: true (`schemas/tier_derivation.py` `band`; the CHECK `marker IN ('●','◐','○') AND (regulatory_stratum_only = 0 OR marker = '○')`).
  - (g) 63 code figures, MOB only, unjudged: true, and T-127 can be scoped to them.
  - (h) the T-120 item 2a premise: false as stated by the caller; classifier 3 survives (F16).

## SHORTEST PATH

**Is parameter 3 closest?** It is not proven. The ranking query (path-finder §4, re-run) puts parameter 3 first by volume: 122 extractions, 58 sources, 50 verified, 16 T1/T2, 8 specifications all retired. Volume is not distance. **Parameter 12 (ramp run length)** was probed on scratchpad/a4/r12.db and returns:
- `provisional`, 6000 mm, `T4-6-only(regulatory_stratum_only)`, marker ○ (which **is** the owner's table for a T5/T6-only basis), 10 governing refs, **one** UNVERIFIED (REF-01016, against six for parameter 3);
- every unit readable (mm, cm, m; no T-108, T-086 or T-111 subject);
- one GAP-372 row (141) and no T3 grey claims (so no T-059 eligibility gap);
- a recorded direction (lower_is_better).

The umbrella failure the ledger records (line 1197) names ramp *gradient* and handrails. For run length the stated mechanism (a shorter run between landings, for rest) is not opposed between wheelchair users and ambulant people. Whether `MOB` passes the design-equivalence test for parameter 12 is a judgment that would drop T-102 from the path. No classifier and not the path-finder weighed it. [UNVERIFIED: whether that judgment is delegable or the owner's. The ledger treats the test as ratified (2026-07-23) and T-110 item 2 requires it before any MOB determination.] Its defects shared with parameter 3: `design_scale=universal` (F4), the slug's four non-searches (F10), REF-00992 and REF-00995 filed UK and BE (F8), and 20 code figures with unjudged lenses (T-127 slice).

**Path-finder reconciliation.**
- **Agrees with the classifiers:** parameter 3 as the candidate; T-102, T-104, T-081, T-117, T-110 and T-037 on the path; T-128 dropped (OD-87); T-122, T-120, T-068 and T-123 off the path; MOB fails the umbrella test (ledger 1197: true); C10 fails with UNVERIFIED governing sources (`test_db_integrity.py` on scratchpad/a4/r3int.db: "56/57 … FAILED: [C10]"); 216 links all `carried`.
- **Conflicts:**
  - T-059 dropped by the path-finder, NEEDED-NOW in classifier 1 (F3 sides with classifier 1).
  - T-108, T-111, T-086 and T-113: NEEDED-NOW in classifier 3 and classifier 2, conditional in the path-finder. The path-finder is closer as to the headline, but OD-63 makes its conditional set the default (F6).
  - T-127: a T-110 slice in the path-finder, a task in classifier 3. No substantive conflict.
  - T-133 item 1 and T-138 item 1: off the path in both. The caller's framing was wrong (F15).
- **Missed by all five:** GAP-372 (F1), GAP-376 and REF-01015 (F2), T-056 item 3a (F4; classifier 1 saw it), the parameter-3 slice of the verified-without-reading debt (F9; classifier 1 saw it), REF-00997 sub-national (F8), parameter 12 (above).
- **Path-finder's three wrong things for 3×MOB:**
  - (1) The MOB group: SURVIVES.
  - (2) The marker: WOUNDED (F5).
  - (3) 216 carried links: SURVIVES (OD-65).
  - A fourth it missed: `design_scale=universal` (F4).
  - C10: SURVIVES.
- **"62 to 67 of 73 off the path":** WOUNDED. With OD-63 binding and F1 to F4 and F9, the honest core is about 14 to 16 tasks or slices. Re-derive by counting the order below.
- **"T-059, T-068, T-120, T-123, T-133, T-128 can be dropped for one cell":** T-068, T-120 (already on main), T-123, T-133 (route B) and T-128 SURVIVE. T-059 is FALSE (F3).
- **D-line classification:**
  - D-05 (0), D-07 (3) and D-14 (no `NOTATION_FAMILIES =` line in scripts/) were spot-checked and hold. D-01 printed 10.
  - "D-01 may be unreachable by design" is WOUNDED: T-037 as written builds a render table (OD-12, T-037 line 66), so D-01 is reachable on the plan's own design. It is the reduced T-037 that leaves it unreachable.

**Verified order (route B, parameter 3 × WHEEL), smallest change first; rule 10 splits tooling from research:**
1. Research, existing verbs, no dependency:
   - T-081 classes for the eight searches that ran;
   - GAP-376 / REF-01015 dispositions [verb existence for `superseded_by_ref_id` UNVERIFIED];
   - T-104 for REF-00994, REF-01013, REF-01014, REF-01016;
   - GAP-372 re-quotes (retire and re-add) for 30, 102, 105, 112, 115, then their translations (the T-112 slice);
   - T-105 slice: full readings or a regrade for the 27 parameter-3 rows;
   - T-102 (mint WHEEL, LLD, WALKAID; carry the parameter-3 links by judgment; SCI into WHEEL, OD-83).
2. Tooling:
   - T-117 (band, CHECK, ⚠, C10 item 4a), without waiting for T-068 or T-120;
   - an `amend-search` deferred-reason flag, or none if the four searches are re-run;
   - the T-059 selection slice together with T-056 item 3a.
3. Research: the T-127 parameter-3 slice (it is T-102's carry), population-match grades, then T-110.
4. Tooling: T-037, reduced only if the owner relaxes OD-63; otherwise add T-124 and T-036 before it, and T-108, T-086, T-111 and T-113 (rescoped) in step 1.

**Owner gates on the path:**
- Q1: does OD-63 bind the first page? (F6)
- Q2: route A (MOB) is relitigation of ledger 1197; the path-finder correctly refers it.
- Whether PROXY or `provisional` is "thin" for ⚠: the owner's, per tier-system §5 (F5).
- Whether `MOB` passes the umbrella test for parameter 12, if that route is wanted.

Not owner-gated: T-102 (OD-14 answered), T-117 item 4a (the owner's "triangle warning"), T-127 (OD-65), question 7 (F15).

## CONSISTENCY (tasks whose class turns on another's)

- T-086 vs T-108 vs T-093: T-093 merged (8461535). The T-086 and T-108 subjects do not overlap (T-108's selector excludes `ratio`). Both turn on T-059 and OD-63.
- T-082 into T-108: compatible.
- T-125 into T-059: compatible. The T-035 dependency is a file collision only.
- T-036 into T-037: classifier 1 folds it in; the path-finder leaves it out; OD-63 puts it in by default.
- T-056 item 3a into T-059: classifier 1 folds it in; the path-finder drops T-059, so 3a is orphaned (F4).
- T-106 vs T-127: both touch code-value lenses on the same rows. Scope T-106 to non-code figures (classifier 2), and on route B T-102's carry does parameter 3.
- T-130 and T-131 need T-129. Classifier 3 retires T-129, while classifier 4 keeps T-131 using `merge-term` "once T-129 lands": incompatible.
- T-109 vs T-143: classifier 3 retires T-109, classifier 4 keeps T-143, which needs T-109's data: incompatible.
- T-133 vs T-110: classifier 4 says only item 1 bears on T-110; on route B none does.
- T-084 vs T-101 vs T-085: classifier 2 folds T-084 into T-101 and retires T-085. Consistent.
- T-117 vs T-120: the dependency is moot (item 2a is on main). T-117 vs T-068: same function, no logical dependency.
- T-104 vs T-117: T-117's necessity turns on whether T-104 can verify every governing source. It cannot (REF-00997).
- T-112 vs GAP-372: the translation slice turns on the re-quote.
- T-058 on T-116; T-115 on T-056 and T-127; T-092 on T-091; T-072 on T-101 and T-105; T-107 on T-057; T-053 on T-032; T-068 on T-059; T-132 on T-110 and T-131; T-118 on T-059, T-068 and T-117 (plus T-021, per classifier 3).

## COUNTS

- `cut -f2 a4_classes.tsv | sort | uniq -c`: ALREADY-DONE 5, APPARATUS 21, NEEDED-LATER 35, NEEDED-NOW 12. 73 rows, 0 duplicates, 0 missing.
- Each classifier's own derived summary matches its table (classifier 1: 8/9/2; classifier 2: 4/12/3; classifier 3: 6/7/4/2; classifier 4: 6/7/3).
- Merged but listed open: T-145, T-147, T-148 (F18). Withdrawn but listed: T-128. Classifier-called-done but not done: T-112.

## UNCOVERED DEFECTS (no open task covers them; each puts or would put a wrong thing in the book)

1. GAP-372: eleven truncated quotes, five on parameter 3, including headline row 30 (F1).
2. GAP-376 and REF-01015: duplicated instruments and a false edition among the governing sources (F2).
3. `code_currency_status` is NULL on all 59 sources and on all 27 governing refs of the probe (`select tier>=4, count(*), sum(code_currency_status is null) from evidence_sources group by 1` gives (0, 29, 29), (1, 30, 30)). Nothing records that a governing code is current, and REF-01015's lapse was found only in prose. T-027 holds the writer only.
4. REF-00997 and REF-00996 are sub-national and outside T-113 (F8).
5. Owner action not carried out, and no task: the 2026-11-26 ACTION (3) to retire A-SIZE e120 rows. Triples 53 (LPA), 57 (TALL) and 61 (BAR) are still live (`select triple_id, identity_code, retired_at from identity_need_icf where need_code='A-SIZE' and icf_code='e120'`). Not book-facing today (OD-85: nothing gathers `identity_need_icf`).
6. `claimed_value` holds a `%` symbol on governing rows (95–101, 103, 105, 109–111). The 2026-10-22 question register records that the reader leaves "8.33%" unread. That falls within T-108's reformat only if T-108 reformats values as well as units [UNVERIFIED].
7. CLAUDE.md §6 against tier-system §5 on main: [NULL: the marker table line and the ⚠ rule, examined, they agree; the residual is tier-system line 49's "⚠ Superseded" banner glyph, which T-120 item 2 already names].

## DOCTRINE LIMITS

- Path-finder §6: ⚠ for every PROXY-graded code. That decides "whether every PROXY grade makes a value thin", which tier-system §5 lists as "Not yet ruled (owner)" (F5).
- Classifier 3 (T-124) and the path-finder's six-task headline read DR §4 over the later owner answer OD-63. Under rule 0 OD-63 binds until relaxed (F6).
- Classifier 3 (T-116): "retire the 6 LMB rows" removes crossings from `identity_icf_map`, which OD-77 freezes as "the mapping meant". That is population-taxonomy structure (decision-protocol §2.4 item 2). OWNER-ONLY.
- Classifier 4 (T-130 RETIRE), classifier 3 (T-129 RETIRE), classifier 4 (T-139, T-140, T-141 RETIRE) and classifier 2 (T-070 DEFER) reverse acts the owner asked for or ratified (F17). OWNER-ONLY.
- OD-87 withdrawal: no recommendation reinstates T-128. [NULL: all five reports examined, none contradicts OD-87.]
- OD-83 SCI into WHEEL: the path-finder and classifier 2 apply it; none contradicts it. [NULL: examined.]
- The owner's 2026-11-14 marker words: no report proposes a circle beside ⚠ or a ◐ for T3 grey. [NULL: examined.]
- Route A (MOB for parameter 3) would relitigate ledger 1197. The path-finder refers it rather than deciding it, which is correct.

## APPROVAL LIST (smallest change first)

| # | Task | Action | Class | Confidence | Evidence command |
|---|---|---|---|---|---|
| 1 | T-145, T-147, T-148 | mark done; remove from the open list | DELEGABLE | high | `git log origin/main --oneline --grep 'T-145\|T-147\|T-148'`; `ls scripts/migrations/16[5-7]*` |
| 2 | T-128 | remove from the open list and from every deps column | DELEGABLE | high | `git grep -n '^OD-87' -- references/project-standards.md` |
| 3 | T-112 | reopen; not done | DELEGABLE | high | the `v_translations_current` join in F1; `select description from gaps where gap_id='GAP-372'` |
| 4 | T-135, T-084 | clear the stale holds (OD-69, OD-46 answered) | DELEGABLE | high | `git grep -n -E '^OD-(46\|69) (STATUS\|CHECK)' -- references/project-standards.md` |
| 5 | T-005, T-038, T-047, T-122, T-085 | retire | DELEGABLE | high | table rows; `select name, sql like '%retired_at%' from sqlite_master where type='view' and sql like '%specifications%'` |
| 6 | T-033, T-040, T-118, T-132, T-062, T-027, T-109 | defer (T-109 deferred, not retired) | DELEGABLE | medium-high | table rows; `git grep -n quantity_kind -- workplan/2026-11-12-bidirectional-pipeline/tasks/T-143-degrees-rule.md` |
| 7 | T-039 | retire | DELEGABLE | medium | `python3 scripts/db.py --help \| grep -c -i propos` |
| 8 | T-140, T-141 | retire or defer | OWNER-ONLY (ratified items) | medium | `python3 workplan/pipeline-state-graph/build_graph.py --check` |
| 9 | T-129, T-130 | defer; retire only with the owner | OWNER-ONLY | medium | `sed -n 28p workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` |
| 10 | T-139 | keep, later (or the owner chooses "stop appending notes") | OWNER-ONLY | medium | `git grep -n -F 'data stored in the wrong cell' -- references/project-standards.md` |
| 11 | T-070 | keep, later; deferral is the owner's | OWNER-ONLY | medium | `git grep -n -E '^OD-44' -- references/project-standards.md` |
| 12 | NEW: GAP-376 / REF-01015 dispositions | keep, now | DELEGABLE (research) | high | the F2 query |
| 13 | NEW: GAP-372 re-quotes (30, 102, 105, 112, 115), then the T-112 slice | keep, now | DELEGABLE (research) | high | F1 |
| 14 | T-081 | keep, now; type the 8 that ran, re-run or tool the 4 that did not | DELEGABLE | high | `python3 scripts/db.py amend-search --help` |
| 15 | T-104 | keep, now; rescoped (4 to verify, REF-01026 superseded, REF-00997 to ⚠) | DELEGABLE | high | F7 |
| 16 | T-105 parameter-3 slice | keep, now | DELEGABLE | medium-high | `python3 scripts/audit/verified_scan_integrity.py` |
| 17 | T-102 | keep, now | DELEGABLE (OD-14 answered) | high | `sed -n 1194,1199p references/project-standards.md` |
| 18 | T-117 | keep, now; drop the T-068 and T-120 deps; leave the PROXY-is-thin rule to the owner | DELEGABLE code / OWNER-ONLY on thin | high / medium | `sed -n '/^def band(/,/^def floor_mean/p' schemas/tier_derivation.py` |
| 19 | T-059 selection slice + T-056 item 3a | keep, now | DELEGABLE | medium | F3 and F4 probe commands |
| 20 | T-127 parameter-3 slice | keep, now; not blocked by T-149 (OD-88 CHECK pending) | DELEGABLE | medium-high | `git grep -n '^OD-88 CHECK' -- references/project-standards.md` |
| 21 | T-124, T-036, T-108, T-086, T-111, T-113 (rescoped) | keep, now unless the owner relaxes OD-63 | OWNER-ONLY (Q1) | high | `git grep -n '^OD-63' -- references/project-standards.md` |
| 22 | T-110, T-037 | keep, now (the deliverable) | DELEGABLE | high | `select count(*), sum(retired_at is null) from specifications` |
| 23 | Parameter 12 as the first determination | consider | OWNER-ONLY if the umbrella judgment is the owner's | low-medium | scratchpad/a4/r12.json |
| 24 | Every other NEEDED-LATER task in the table | keep, later | DELEGABLE | medium | table |

## NOT REACHED / UNVERIFIED

- A 3×WHEEL probe: WHEEL does not exist. Whether line 1489 (universal) and gate 1 behave as stated for a child cell rests on reading `_open_gates` and the probes of MOB, not on a run.
- Whether a writer can set `superseded_by_ref_id` on REF-01026 or REF-01015 (not searched in `db.py --help`).
- The retrievability of REF-00994, REF-01013, REF-01014 and REF-01016. No fetch was made.
- I did not re-run T-138's per-item subjects, T-131's 11 pairs or T-071's root counts; I accepted classifier 4 and classifier 2 there.
- Whether the owner reads "Ratify all" as covering adjudication-3 items 12–91: the ledger marks it [ASSUMPTION].
- The bibliographic fields of the sources in F2 against `retrieval-log/`: not diffed. The finding rests on the rows' own notes.

## Closing block

```json adversarial-findings
[
  {"lens": "L6-contrary", "subject_table": "translations", "subject_key": "GAP-372 (extractions 30,102,105,112,115,141,202,207,208,209,215)", "claim_attacked": "T-112 is already done: every live non-English figure has a reviewed translation", "method": "joined live non-English extractions to v_translations_current (superseded rows excluded) instead of all reviewed rows", "artefact": "data/guidebook.db", "verdict": "SUSTAINED", "severity": "CRITICAL"},
  {"lens": "L2-fidelity", "subject_table": "source_value_extractions", "subject_key": "30", "claim_attacked": "the headline 5 % is stated by a verified, faithfully quoted reading of REF-00995", "method": "read the rejected translation 190's review_reason and GAP-372: the stored quote drops the stem carrying 'hoogstens'", "artefact": "data/guidebook.db", "verdict": "SUSTAINED", "severity": "HIGH"},
  {"lens": "L3-independence", "subject_table": "evidence_sources", "subject_key": "REF-01026/REF-01032; REF-01015/REF-01018", "claim_attacked": "the probe cell's 27 governing refs are 27 distinct instruments", "method": "read each governing row's notes and superseded_by_ref_id; GAP-376", "artefact": "data/guidebook.db", "verdict": "SUSTAINED", "severity": "HIGH"},
  {"lens": "L1-existence", "subject_table": "evidence_sources", "subject_key": "REF-01015", "claim_attacked": "a VERIFIED governing source's stored identity (TGD M 2022) is the document held", "method": "row's own note: the persisted artefact is the 2010 edition, lapsed 2024-01-01", "artefact": "data/guidebook.db", "verdict": "SUSTAINED", "severity": "HIGH"},
  {"lens": "L4-tier", "subject_table": "specification_source_links", "subject_key": "scratch specification 9 (3xMOB)", "claim_attacked": "path-finder: T-059 is off the path because the selected value is unchanged", "method": "re-ran assess_cell on a scratch copy; compared source_records with governing and supporting links: four in-lens T3 grey sources (REF-01025 states 1:20) are dropped by tier, against U1/OD-58", "artefact": "scripts/assess/assess_cell.py", "verdict": "SUSTAINED", "severity": "HIGH"},
  {"lens": "L7-recognition", "subject_table": "specifications", "subject_key": "scratch 3xMOB and 12xMOB", "claim_attacked": "path-finder's three wrong things exhaust what is wrong with the 3xMOB row", "method": "probe writes design_scale=universal on a group cell; OD-48 (a), ratified 2026-11-19, reads universal as 'for everyone'", "artefact": "references/project-standards.md", "verdict": "SUSTAINED", "severity": "HIGH"},
  {"lens": "L4-tier", "subject_table": "specifications", "subject_key": "scratch 3xMOB marker", "claim_attacked": "the 3xMOB marker ○ is wrong and must be ⚠ (path-finder; classifier 3 on T-117)", "method": "read tier-system §5 on origin/main: OD-59 gives the value its own source's marker (verified T6, so ○); PROXY-as-thin is listed 'Not yet ruled (owner)'", "artefact": "governance/tier-system.md", "verdict": "SUSTAINED", "severity": "HIGH"},
  {"lens": "L4-tier", "subject_table": "source_value_extractions", "subject_key": "60,61,62,64", "claim_attacked": "classifier 2: T-086's four ratio claims are code maxima dropped from the value", "method": "joined to evidence_sources: REF-01008, tier 3 grey, not in the governing set", "artefact": "data/guidebook.db", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L4-tier", "subject_table": "evidence_sources", "subject_key": "REF-00989,REF-00993,REF-01006,REF-01009", "claim_attacked": "classifier 3: ramp gradient holds no Co-1 tier", "method": "grouped parameter-3 sources by tier and evidence_type: (1,'co1',4)", "artefact": "data/guidebook.db", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "L5-population", "subject_table": "base_taxonomy_identity", "subject_key": "MOB", "claim_attacked": "MOB fails the umbrella test for ramp gradient (path-finder, classifier 2)", "method": "read ledger lines 1194-1199 and T-110 item 2", "artefact": "references/project-standards.md", "verdict": "SURVIVED"},
  {"lens": "L5-population", "subject_table": "evidence_sources", "subject_key": "REF-00997,REF-00996", "claim_attacked": "T-113: the held sub-national instruments are four", "method": "read the URLs of every T4-6 and T5 source: des.sa.gov.au (South Australia) and toegankelijkgebouw.be (Flanders) are filed AU and BE", "artefact": "data/guidebook.db", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L2-fidelity", "subject_table": "source_value_extractions", "subject_key": "parameter 3 rows in verified_scan_integrity", "claim_attacked": "classifier 2: parameter 3 carries no reading debt, so T-105 can wait", "method": "ran scripts/audit/verified_scan_integrity.py: all 27 VERIFIED-WITHOUT-FULL-READING and 93 of 103 NO-COVERING-READING rows are parameter 3", "artefact": "scripts/audit/verified_scan_integrity.py", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L8-query-shape", "subject_table": "search_executions", "subject_key": "87,133,138,191", "claim_attacked": "classifier 2: four zero-result searches on the parameter-3 slug never ran", "method": "read findings_note, absence_class and deferred_reason for every zero-result row", "artefact": "data/guidebook.db", "verdict": "SURVIVED"},
  {"lens": "S4-sequence", "subject_table": "search_executions", "subject_key": "87,133,138,191", "claim_attacked": "path-finder: T-081 is data only, about an hour", "method": "read amend-search --help: no deferred-reason flag, and absence_class has no 'not run' value; needs a tooling PR first (rule 10) or re-runs", "artefact": "scripts/db.py", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "S4-sequence", "subject_table": "translations", "subject_key": "extractions 30,102,105,112,115", "claim_attacked": "path-finder: the T-112 slice is five translations inside T-110's batch", "method": "claim_text is in _NOT_AMENDABLE_SVE; the truncated originals must be retired and re-added before any translation can pass review", "artefact": "scripts/db.py", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "S4-sequence", "subject_table": null, "subject_key": "OD-88", "claim_attacked": "classifier 3: T-127 now waits for T-149", "method": "applied the plan's gate function to OD-88: CHECK pending prints CLOSED; OD-87's wait (PR 246 or T-148) is met", "artefact": "references/project-standards.md", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "L1-existence", "subject_table": null, "subject_key": "open-tasks.tsv", "claim_attacked": "the 73 tasks listed are open", "method": "derived merges from git independently of the generator: T-145 (#244), T-147 (#246), T-148 (#247) are on origin/main; T-128 withdrawn", "artefact": "scripts/migrations/167_icf_hierarchy.sql", "verdict": "SUSTAINED", "severity": "MEDIUM"},
  {"lens": "L1-existence", "subject_table": null, "subject_key": "T-145,T-147,T-148", "claim_attacked": "classifier 4: the three are merged", "method": "git log origin/main, the migrations present, db.py --help verbs, row counts", "artefact": "scripts/migrations/165_identity_need_icf.sql", "verdict": "SURVIVED"},
  {"lens": "L1-existence", "subject_table": null, "subject_key": "T-128", "claim_attacked": "classifier 3: T-128 was withdrawn by OD-87", "method": "read ledger 8600-8602: STATUS resolved under delegation, CHECK confirmed with corrections applied", "artefact": "references/project-standards.md", "verdict": "SURVIVED"},
  {"lens": "L1-existence", "subject_table": null, "subject_key": "T-120 item 2a", "claim_attacked": "caller's brief: item 2a sits only in open PR #248, not on main", "method": "git log origin/main -1 shows the 1d52215d merge of #248; git show origin/main:governance/tier-system.md carries the table", "artefact": "governance/tier-system.md", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "L6-contrary", "subject_table": "lang_jur_map", "subject_key": "T-084", "claim_attacked": "T-084 is held on an open owner question (OD-46)", "method": "git grep of the OD-46 status lines", "artefact": "references/project-standards.md", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "L6-contrary", "subject_table": "determination_gates", "subject_key": "1", "claim_attacked": "classifier 4: T-133 item 1 (gate 1 on REF-01002) is on the path to the first determination", "method": "read _open_gates: a gate on the parent code MOB does not reach a WHEEL child cell", "artefact": "scripts/assess/assess_cell.py", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "L6-contrary", "subject_table": "base_parameters", "subject_key": "3", "claim_attacked": "classifier 4: owner question 7 is an unlisted hold on the shortest path", "method": "confirmed it is unanswered (no ledger line); read run-pipeline_SKILL.md:392-394: the engine reads the direction whatever direction_ref_id holds", "artefact": "skills/run-pipeline_SKILL.md", "verdict": "SUSTAINED", "severity": "LOW"},
  {"lens": "L2-fidelity", "subject_table": "source_value_extractions", "subject_key": "25", "claim_attacked": "the ADM 1:20 headline row drops its going condition", "method": "read extraction 25's note and the condition_on edge 43 from 117; the 1:12 and 1:15 rows are filed as finding and condition", "artefact": "data/guidebook.db", "verdict": "SURVIVED"},
  {"lens": "S1-harm-reached-row", "subject_table": "source_value_extractions", "subject_key": "harm_finding", "claim_attacked": "a harm finding on parameter 3 failed to reach the cell", "method": "select sum(harm_finding=1) from source_value_extractions returned 0; no harm row exists to fail to reach anything, so the lens has no subject", "artefact": "data/guidebook.db", "verdict": "SURVIVED"},
  {"lens": "S2-mismatch-note-vs-payload", "subject_table": null, "subject_key": null, "claim_attacked": "a recorded mismatch_note is true against its payload", "method": "Not attacked: the work under review is a classification of plan tasks and writes no row, and none of the five reports cites a mismatch_note", "artefact": null, "verdict": "NOT-ATTACKED"},
  {"lens": "S3-containment", "subject_table": null, "subject_key": "data/guidebook.db", "claim_attacked": "the classifiers and path-finder stayed read-only", "method": "sha256 of the canonical database before and after this pass equals the value all five reports state (3d419efb...edb9); engine runs confirmed confined to scratch copies", "artefact": "data/guidebook.db", "verdict": "SURVIVED"},
  {"lens": "L5-population", "subject_table": "base_parameters", "subject_key": "12", "claim_attacked": "parameter 3 is the closest first determination (all five reports)", "method": "probed 12xMOB on a scratch copy: one unverified governing source, every unit readable, marker already the owner's table for T5/T6; not weighed by anyone", "artefact": "data/guidebook.db", "verdict": "WITHHELD-FOR-OWNER"},
  {"lens": "L7-recognition", "subject_table": null, "subject_key": "T-129,T-130,T-139,T-140,T-141,T-070", "claim_attacked": "retiring or deferring these is a classifier's call under CLAUDE.md section 8", "method": "traced each to the owner's Q2 of 2026-11-16, the 'Ratify all' of 2026-11-19, or OR-15/OD-44", "artefact": "workplan/2026-11-12-bidirectional-pipeline/PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md", "verdict": "WITHHELD-FOR-OWNER"},
  {"lens": "L7-recognition", "subject_table": null, "subject_key": "OD-63", "claim_attacked": "the first page may omit the four figures (T-124 later; path-finder's six tasks)", "method": "read OD-63, answered by the owner 2026-11-14, against DR-2026-08-19 section 4; rule 0", "artefact": "references/project-standards.md", "verdict": "WITHHELD-FOR-OWNER"}
]
```

## Summary

Coverage is complete: 73 tasks, each classified once. Classifier counts: 12 NEEDED-NOW, 35 NEEDED-LATER, 21 APPARATUS, 5 ALREADY-DONE. Of my verdicts, 57 survive, 15 are wounded and one is false. The false one is T-112 "done": eleven live non-English figures have no current English, because the reviews were superseded by rejections of truncated quotes (GAP-372). One of them is a source of the ramp headline. No task covers it. Also uncovered: duplicated or misidentified governing instruments (REF-01026 and REF-01032; REF-01015, a lapsed 2010 edition shown as 2022). The path-finder's six-task path wrongly drops T-059 (in-lens T3 grey sources stating 1:20 are omitted) and misses `design_scale=universal` on a group cell. Its ⚠ marker settles a question the owner left unruled, and it treats OD-63's four figures as optional although the owner answered them. T-081 needs tooling or re-runs. The retirements of T-129, T-130, T-139, T-140, T-141 and T-070 reverse owner acts and are the owner's to approve. Parameter 12 may be closer than parameter 3, and nobody weighed it.

File: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/antagonist-4.md
