# Classifier 1: 19 tasks of the remediation plan, judged against the goal

Read-only. Every result below came from a command run on 2026-11-27 against `data/guidebook.db` (`user_version` 167) opened `mode=ro`, or from a file read. Re-run any figure before relying on it. The ledger was read to its last entry ("Owner statements 2026-11-26").

Facts that apply to several tasks (re-derive them):
- `select specification_id, retired_at from specifications` returned 8 rows, all for parameter 3 and all retired. **No live determination exists.** Nothing has been rendered (`ls site specs`: neither exists).
- `python3 scripts/audit/verified_scan_integrity.py` returned `VERIFIED-WITHOUT-FULL-READING: 27 row(s)`, `SOURCE-NOT-VERIFIED: 15`, `NO-COVERING-READING: 103` out of `EXAMINED: 212`.
- `connections`, `connection_targets` and `conflicts` hold 0 rows each.
- `scripts/assess/assess_cell.py` still decides by tier which sources can govern: the `elif regulatory:` (G1) branch is reached only when no T1 to T3 set applies, and it sets `design_scale = SCALE_UNIVERSAL`. The ledger's "Unification 2026-11-14" (U1, U2, U7) says the tier grades the marker and never decides eligibility.

## Table

| id | title | class | element(s) | shortest path? | one-line reason | confidence |
|---|---|---|---|---|---|---|
| T-005 | Seeded test that a retired determination is surfaced by no view | APPARATUS | E5 | n | Every live determination view already filters `retired_at`, and `v_pending` is already tested (T013-14). RETIRE | high |
| T-027 | Source's own title, edition and currency can be written | APPARATUS | E2 | n | Titles are held in their original language in `pub_title` with the edition in the text, and currency is already writable. An eight-column warrant per field is machinery. DEFER | medium |
| T-032 | Relations synthesis, and what a synthesis row is | NEEDED-LATER | E4, E5 | n | Nothing can record a conflict between groups with its judge, or a relation. One determination needs neither | medium |
| T-033 | Candidate relations on demand (read-only) | APPARATUS | E4 | n | A helper that proposes candidates. If it is missing, something may be overlooked but nothing wrong is written. DEFER | high |
| T-035 | Skills that describe the database that exists | NEEDED-LATER | E1, E2, E6 | n | The skill audit fails on 79 dead tokens and the prose register still teaches a value ladder the owner rejected. The comparator risk has no live rows | medium |
| T-036 | The jurisdiction comparison as a view | NEEDED-LATER | E6 | n | Render's colour-coded code bodies (OD-63) need this query. Fold it into T-037 rather than run it as a separate task | medium |
| T-037 | Render from the database | NEEDED-NOW | E6 | y | Nothing a reader can open exists. Its dependencies (T-032, T-122, a hash staleness check) are heavier than one page needs | high |
| T-038 | Register the stage-pair gate | APPARATUS | (none) | n | A gate on the stage map that no published page reads. RETIRE | high |
| T-039 | The owner's edits as proposals through the write path | APPARATUS | (none) | n | The owner already directs a session that writes through `db.py`. A proposal mechanism adds machinery and fixes nothing wrong in the book. RETIRE or DEFER | medium |
| T-040 | Caller sweep for the deletion candidates | APPARATUS | (none) | n | Removes `gap_mining` and `reasoning_doc_citations` (0 rows each) and `connections.opus_reviewed`. A cheap clean-up, off the path. DEFER | high |
| T-047 | A durable test that the base changes by data alone | APPARATUS | E3 | n | Tests a property of the code, not anything in the book. RETIRE | high |
| T-052 | Mining stages an out-of-scope source as a lead | NEEDED-LATER | E1 | n | Real gap: both skills are silent (0 matches), and `add-locator` has no `--jurisdiction` flag, so the task's own stop condition fires | high |
| T-053 | Conflict between groups in the engine | NEEDED-LATER | E4 | n | OD-36 is answered and the engine applies no harm ordering (0 matches). It is needed only when a cell has an open conflict, and 0 conflicts exist | high |
| T-056 | ALL leaves the identity lens | NEEDED-LATER | E3, E5 | n | `ALL` is still active on 34 figure lens links, none on parameter 3. OD-48 has since been answered, which releases item 3a, and 3a can mislabel a group's determination as `universal` | medium |
| T-057 | Base coverage view | NEEDED-LATER | E1, E3 | n | The owner's own acceptance test for the base. It does not block a first determination | medium |
| T-058 | UPL reinstated for upper limb: retired crosswalk and prose | NEEDED-LATER | E3 | n | Governance prose still says UPL→LMB and MOB/UPL, the reverse of the owner's ruling. It waits on T-116, and parameter 3 does not depend on it | high |
| T-059 | Prior workplan's T-4: agreement, divergence, fragility | NEEDED-NOW | E4, E5 | y | The engine still lets tier decide eligibility and detects no divergence, so the value a cell states can be the wrong one. T-110 depends on it | high |
| T-060 | Specifications pass writes an element-level determination | NEEDED-LATER | E5 | n | The owner answered OD-56 and OR-14b, but no design file exists and one parameter determination does not need it | high |
| T-062 | A `verified` figure with no full reading is refused at rest | APPARATUS | E2 | n | The writer already refuses this state. The 27 bad rows are fixed by T-105's research, not by this gate, and the task's precondition (0 rows) fails today. DEFER | high |

## Per-task detail

### T-005: APPARATUS, RETIRE
- Evidence: the task's view probe returned `('v_best_practice', True), ('v_determination_provenance', True), ('v_item_provenance', True), ('v_pending', True), ('v_divergence', True), ('v_code_floor_only', False)`. `select sql from sqlite_master where name='v_code_floor_only'` returned None, so the view no longer exists. The False is an absent view, not a missing filter, and the task's expected output is stale.
- `grep -rn v_pending scripts/tests` found `test_run_pipeline_refusals.py:2504`, case `T013-14`: "an OPEN gap whose cell is retired is not in v_pending". The retirement filter is already tested on one view.
- Nothing wrong reaches the book: every live view filters, and there are no live determinations to leak. What to delete: the task file. Nothing would be added.

### T-027: APPARATUS, DEFER
- Evidence: `select sum(original_title is not null), sum(edition is not null), sum(code_currency_status is not null) from evidence_sources` returned `(0, 0, 0)`. Commit `cb7e75a` ("a source's code currency can be written") already makes `code_currency_status` writable through `amend-source` (the task's section 3 says the same).
- `pub_title` holds the original-language titles, for example REF-00990 (Japanese), REF-01019 (Korean), REF-01012 "Byggteknisk forskrift (TEK17)". Editions appear in the title text, for example REF-00994 "IPC Accessibility Guide, 4th edition".
- What remains (section 12.3) is a rebuild of `evidence_sources` plus eight warrant columns per field, for `edition` and `original_title`. That is substantial machinery for a fact the title already carries.
- A real E2 gap does exist, but this task does not close it: every T4 to T6 source (30 of 59 by `tier>=4`) has `code_currency_status` NULL. A superseded code could therefore be cited as current. That is research work with the existing `amend-source` (jurisdiction-tracker), not this tooling.
- Undeclared dependency: section 2 now requires T-139 and T-135. T-135 is OWNER: OD-69.
- What to delete: defer the task file. Recommend dropping the per-field warrant design unless a published reference list actually needs a separate `edition` cell.

### T-032: NEEDED-LATER (E4, E5)
- Evidence: `select (select count(*) from connections),(select count(*) from conflicts)` returned `(0, 0)`. `pragma table_info(conflicts)` has no judge or warrant column: domain, pop_a, pop_b, status, resolution, evidence, gap_id, …, parameter_id. OD-07, OD-12, OD-25 and OD-29 are RESOLVED UNDER DELEGATION and OD-19 is ANSWERED BY THE OWNER (ledger STATUS lines).
- Why it can wait: DR-2026-08-19 §4 asks for a determination, its governing sources, its population-match grading and its search log. It does not ask for relations or judged discussion. Divergence within one cell is T-059's.
- Recommendation: build only the OD-19 slice (a judge and warrant on `conflicts`, refused without them) when the first real conflict appears. The four relation kinds, and judged discussion reviewed by a second Opus instance, are heavy and nothing on the path reads them.
- Plan dependency to change: T-037 lists T-032 as a hard dependency. Render can state "no discussion" instead (OD-12 already allows "says when a determination's discussion is unreviewed"), so T-032 should not block T-037.

### T-033: APPARATUS, DEFER
- Evidence: `python3 scripts/db.py --help | grep -c -E 'synthesis-candidates|relation-candidates'` returned 0. Nothing writes relations today (0 `connections`), so a candidate list has no consumer yet.
- If it is missing, a relation may be overlooked. No wrong figure, group, source or marker reaches the book. What to delete: defer the task file. Revisit only if T-032's relation half is built.

### T-035: NEEDED-LATER (E1, E2, E6)
- Evidence: `python3 scripts/audit/skill_vocabulary_audit.py` returned `FAIL: 79 token(s) in 18 file(s)`. Research run from these skills follows instructions that name objects which no longer exist.
- `git grep -n 'Ideal → Best Practice' -- skills` hits `skills/prose-style-checker_SKILL.md:6,53`. `skills/voice-style_SKILL.md:212` still carries "this guidebook recommends". Both contradict the owner's 2026-11-14 rulings, and OD-60 (ANSWERED) says rewrite.
- Item 3 (comparator): `skills/run-pipeline_SKILL.md:303` still reads "`=` for a point", and the `db.py` help at line 2932 reads "'=' for a point". However, `select … from source_value_extractions where comparator='=' and claim_text like '%should%' or '%recommend%' or '%prefer%'` returned no rows. The risk is prospective, and the owner's 2026-11-14 bound-word text on the same line already says to guess no comparator when the direction is unclear.
- Why it can wait: no live figure is wrong because of these skills. The register rewrite (item 5) must land before T-037's templates are written, because render is where the project's voice reaches the reader. Depends on T-120 (open).
- If it is split, items 2 to 4 are a few sentences and cost almost nothing.

### T-036: NEEDED-LATER (E6)
- Evidence: `select name from sqlite_master where type='view' and name like '%jurisdiction%'` returned only `v_coverage_jurisdiction`. OD-01 is RESOLVED UNDER DELEGATION. OD-63 (owner): the render shows the four figures "as a colour code on the surveyed jurisdictional code bodies", which needs a figure per jurisdiction.
- Recommendation: merge it into T-037 as the one query render needs, not a separate migration task. It depends on T-101 (research, open) for the in-scope pairs, and `v_research_scope` already returns 70 rows.

### T-037: NEEDED-NOW (E6), on the shortest path
- Evidence: `ls site specs` found neither. `ls scripts/generate` lists `context_map.py`, `owner_browser.html`, `owner_browser_build.py` and `research_contract_hook.py`, and no page generator. DR-2026-08-19 line 77: "Acceptance is one answered question, published (§4) — the only criterion apparatus cannot satisfy."
- What goes wrong without it: goal element E6 cannot be met at all.
- Dependencies to cut: T-122 (stage-contract criteria; apparatus), T-032 (see above) and the registered hash staleness check (OD-12 already allows "or the hash is not added", and the render table is rebuilt in full at every build anyway). Keep T-124 (the four figures, OD-63) and T-036's query (folded in). Also note that `owner_browser_build.py` already reads the database. Check whether it can be reused before writing a new generator (§8, reuse what exists). [UNVERIFIED: I did not read owner_browser_build.py beyond its line 20.]
- It cannot render anything until a live determination exists (T-110). Today there are 0 live `specifications` rows.

### T-038: APPARATUS, RETIRE
- Evidence: `python3 workplan/pipeline-state-graph/walkability.py | grep -c 'NO PATH'` returned 10. That is a gate on the stage map (OD-26, delegated). Nothing wrong reaches the book if a migration breaks a stage path: the render itself fails, and that is the real test.
- What to delete: the task file. Do not add the `views:` key or the registry entry.

### T-039: APPARATUS, RETIRE or DEFER
- Evidence: `db.py --help | grep -c -i propos` returned 4, all `propose-identity-need-icf`; no edit-proposal verb exists. `owner_browser_build.py:20` "opened read-only".
- The owner changes a value today by telling a session, which writes through the sanctioned path. Rule 0 records the owner's words, and the engine recomputes dependants. A second, page-driven path adds a design and verbs with no wrong thing to prevent. OD-20 is delegated, not the owner's words. If the owner wants in-page editing, that is their call; until then, retire.

### T-040: APPARATUS, DEFER (a cheap deletion)
- Evidence: the `git grep -l -e gap_mining -e reasoning_doc_citations -e opus_reviewed` found 21 files. `gap_mining` and `reasoning_doc_citations` each hold 0 rows. §8 makes deletion cheap, but nothing wrong reaches the book while they stay. `connections.opus_reviewed` belongs to T-032's reshape and should go only if that is built. Item 2 (report advisory failures) is pure apparatus. Do it opportunistically, or not at all.

### T-047: APPARATUS, RETIRE
- Evidence: the task's evidence is `git status --porcelain scripts schemas | wc -l`, a property of the tree. The verbs it would exercise already exist and refuse (T-015, T-020, T-024, T-025, T-029 merged). Without the test, a future vocabulary could be typed into code. That is caught at review, and it is the code's flexibility, not the book's content. What to delete: the task file.

### T-052: NEEDED-LATER (E1)
- Evidence: `grep -c -E 'OUT-OF-SCOPE|outside the scope in force'` returned 0 for both `skills/citation-miner_SKILL.md` and `skills/gap-driven-mining_SKILL.md`. OD-04 and OD-34 are ANSWERED BY THE OWNER, and OD-05 is delegated with CHECK "not required".
- Wrong thing it prevents: an out-of-scope code or standard admitted against OD-04 or OD-34, putting a wrong jurisdiction's figure into a cell. Why it can wait: parameter 3's corpus is already gathered, and the rule is two skill paragraphs.
- **Undeclared defect.** `python3 scripts/db.py add-locator --help` shows no `--jurisdiction` flag, although `source_locators` has a `jurisdiction` column. The task's section 4 item 2 says "If add-locator cannot record one of those facts … stop: that is a writer gap for its own tooling pull request". So the task as written stops. The smallest fix is one flag on `add-locator`, which is tooling and must come first under rule 10.

### T-053: NEEDED-LATER (E4)
- Evidence: `git grep -n -i -E 'harm.?asym|broadest' -- scripts/assess | wc -l` returned 0. `harm_classes` does not exist. OD-36 and OD-19 are ANSWERED BY THE OWNER. `conflicts` holds 0 rows.
- Why it can wait: it applies only to a cell where two groups' figures pull in opposite directions. A first determination can be chosen without one. Depends on T-032's OD-19 slice.

### T-056: NEEDED-LATER (E3, E5)
- Evidence: the task's probe returned `base_taxonomy_identity.identity_code: 1` (ALL is 'active'), `extraction_lens_links.identity_code: 34` and `gaps.identity_code: 1`. By parameter, the ALL links fall on 4 (11), 5 (2), 6 (3), 8 (1), 9 (12) and 11 (5), and none on parameter 3, which holds 122 of 214 figures. `code_value_identity_audit.py` (iv): "34 carry no identity but ALL, so reach no group cell".
- **The precondition is stale, and the change releases work.** The file says OD-48 is OPEN. The ledger at lines 7995–7996 reads "OD-48: whom it is for (the adjudication's recommended default, ratified) / OD-48 STATUS: ANSWERED BY THE OWNER". That releases item 3a.
- Item 3a matters for the book. `assess_cell.py`'s G1 branch writes `design_scale = SCALE_UNIVERSAL` for any regulatory-only basis. Under OD-48 (a), `universal` means the determination names no group, so a group's determination resting on codes alone would be shown as for everyone. Recommend moving item 3a into T-059 (same function, same `RULE_VERSION` bump). Items 1, 2 and 5 can wait with T-115.

### T-057: NEEDED-LATER (E1, E3)
- Evidence: the `v_coverage_*` views are jurisdiction, branch, language, lens, priority and parameter_via_admission. None returns the three states per concept and pair. `select count(*) from v_research_scope` returned 70. Owner, 2026-11-06: the base is accepted when coverage can be confirmed correct by a derived measure. The task itself records that the "three states" reading is an [ASSUMPTION].
- Why it can wait: it accepts the base, not a determination. The per-determination search log, including empty searches, is already in `search_executions` (T-080 merged). It is one view with no stored data. T-107 reads it.

### T-058: NEEDED-LATER (E3)
- Evidence: the DR has "UPL→LMB" at line 27, `governance/retired-vocabulary.yaml:870` has "tokens: [VIS, UPL, …]", `governance/population-taxonomy.md:18,35,93` has the crosswalk and `MOB/UPL`, `governance/functional-taxonomy.md:284-285` has `MOB/UPL`, and `scripts/db.py:10310` lists UPL among retired codes. The database has `LMB` active and no `UPL` row (`select identity_code,status from base_taxonomy_identity where identity_code in ('UPL','LMB','SCI','WHEEL')` returned `[('LMB','active'),('SCI','active')]`).
- Wrong thing: a session reading this prose files upper-limb evidence under mobility or LMB, which is a wrong group. It waits on T-116 (research, open), and parameter 3 does not turn on it.
- Ledger note: "Owner statements 2026-11-26" ACTION (4) holds back sweeps of other documents for Co-2 (C1). That does not touch UPL.

### T-059: NEEDED-NOW (E4, E5), on the shortest path
- Evidence: `grep -n 'def determine' scripts/assess/assess_cell.py` gives line 1322 `determine(conn, parameter_id, lens, slug, note)`, with no synthesis-approach parameter. Exclusion reasons now vary by cause (lines 523–550), so step 1 is partly done already. No divergence detection exists. The G1 branch (around line 1451) is reached only when no T1 to T3 set applies, and line 539 excludes "a value-supplying figure … disqualified on tier".
- Wrong thing: the Unification of 2026-11-14 and OD-58 (ANSWERED) make the stated value the most accommodating across all tiers, displaced only by a source stating worse results. Today the engine can state a T1 to T3 value while a more accommodating code value is in hand, or the reverse, and can record two incompatible anchoring claims as one cell without marking it `divergent`. Both put a wrong figure on the page.
- Dependencies: the file lists T-128, but OD-87 (2026-11-25) withdrew T-128, so that dependency is stale. T-127 is open (research; under OD-89 it waits for T-149/T-150). T-120 is open. T-110 depends on T-059.
- Trim: item 7 (flip `code_value_identity_audit` to blocking) is apparatus. Its probe shows list (i) is 0, so the flip is possible, but no wrong thing reaches the book without it. Drop it. Add T-056 item 3a (above).

### T-060: NEEDED-LATER (E5)
- Evidence: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-060-design.md` reported no such file. `git grep 'v_element_page|element_determination'` found no hits. OD-56 and OR-14b are answered by the owner.
- Why it can wait: an element row only points at parameter determinations, and none is live. It must not become a container (CLAUDE.md §7). Build it after several parameter determinations exist.

### T-062: APPARATUS, DEFER
- Evidence: `verified_scan_integrity.py` returned `VERIFIED-WITHOUT-FULL-READING: 27 row(s)`. The task's own precondition requires 0 and says "stop". The registry has `('verified_scan_integrity','advisory')`. The writers already refuse the state (V01 to V06, per the task).
- The wrong thing is real: 27 figures carry `verified` without a full reading, and render prints the status. It is repaired by T-105 (research: read in full or re-grade), not by this gate. Once those rows are clean, the gate only guards against hand SQL, which rule 3 already forbids. What to delete: defer the task file. Make sure T-105's 27 rows are on the path before T-110.

## Not reached, or unverified
- I did not open the before and after checks or the gate of any task (none was executed).
- `owner_browser_build.py`: I read only line 20. Whether it can serve as the render generator is [UNVERIFIED].
- T-032's and T-037's full design sections were read only through section 4.
- For T-059, I did not read the 2026-10-22 report's T-4 section; I confirmed only that it exists.
- I did not verify whether parameter 3's governing set actually contains a T4 to T6 value more accommodating than its T1 to T3 values. The defect is shown in the code, not yet in a live cell (there are no live cells).

## Summary

Counts derived with `awk '/^## Table/{t=1;next} /^## Per-task/{t=0} t && /^\| T-/' classify-1.md | awk -F'|' '{gsub(/ /,"",$4); n[$4]++} END{for(k in n) print k, n[k]}' | sort` (re-run it rather than trust these): APPARATUS 8, NEEDED-LATER 9, NEEDED-NOW 2, ALREADY-DONE-OR-SUPERSEDED 0, OWNER-HOLD 0.

Only two of my 19 are on the shortest path to one published determination: **T-059** (the engine selects the value across all tiers by the harm test and marks divergence; fold in T-056 item 3a; drop item 7 and the stale T-128 dependency) and **T-037** (render; cut its T-032, T-122 and hash-check dependencies, and fold in T-036). Outside my set, the 27 `verified` rows without a full reading need T-105 before any determination is published. T-052 cannot proceed until `add-locator` gets a `--jurisdiction` flag. Eight of my tasks are apparatus: retire T-005, T-038, T-047 and T-039, and defer T-027, T-033, T-040 and T-062.
