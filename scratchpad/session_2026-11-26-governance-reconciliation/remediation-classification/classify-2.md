# Classifier 2: T-068 to T-107 (19 tasks)

Read on 2026-11-27 against the working tree of branch ccr-64231823-gqy3xr, schema `PRAGMA user_version` = 167, `data/guidebook.db` sha256 `3d419efb…edb9` (unchanged; every query read-only, the one engine run was on a scratch copy at `scratchpad/c2/v.db`).

**The shortest path assumed.** The live probe every task file uses: parameter 3 (ramp gradient), slug `accessible-circulation-geometry`, identity `MOB`. Re-run on a scratch copy today, `assess_cell.py` writes a `provisional` proxy cell with value ≤ 5 % / ≤ 1:20, 27 governing sources, `has_unverified_sources = 1`, marker `○`, and the value note "composed from 11 of 35 governing claims: 24 state no parsable numeric bound". No live determination exists (`select count(*), sum(retired_at is null) from specifications` → 8, 0). A task is "on the shortest path" if that cell cannot be published right without it.

| id | title | class | element(s) | shortest path? | one-line reason | confidence |
|---|---|---|---|---|---|---|
| T-068 | A convergent cell states its sources, their tiers and its independent roots | NEEDED-LATER | E4 | n | The engine writes only `pending_assessment` today (nothing says "converge"), so no false convergence reaches the book; owner said convergence "doesn't matter enough"; trim items 6 (gap cue, `/batch-done` line) and the diagnostics reader | medium |
| T-069 | Promote the adjudicated non-English observations to forms of their terms | NEEDED-LATER | E1 | n | 22 NAMES-EXISTING observations, 0 promoted; every non-English form is `model_seed` or `unrecorded`; affects future non-English searches, not the parameter-3 cell | high |
| T-070 | Blind double extraction: two readers, model and effort | APPARATUS (DEFER) | E2 (measurement) | n | A reliability study; it corrects no row and no wrong figure reaches the book without it; the shortest-path "we verify we recorded accurately" is T-104 plus the adversarial pass | medium |
| T-071 | Give every value-supplying figure its root | NEEDED-LATER | E4 | n | 81 tier-6 claims and 14 others carry no root; roots feed only the independence count T-068 shows; the marker does not read roots | medium |
| T-072 | Seed the list of quantities from the phrases the held codes use | NEEDED-LATER | E3 | n | Widens the parameter list; waits on T-105 (417 NOT-READ pairs) and T-101; nothing on parameter 3 | high |
| T-081 | Each stored zero-result search states its cause | NEEDED-NOW | E1 | y | 9 of the 12 unclassed zero-result searches are on parameter 3's slug; 4 of them (87, 133, 138, 191) never returned a result list, so the published search log would show absence where nothing ran; the task as written leaves those 4 untouched (defect) | high |
| T-082 | The two stored numerical claims with no comparator | NEEDED-LATER | E2 | n | Real (extractions 189, 190, REF-00992, parameter 4); a floor and a site-restricted allowance would read as bare values; parameter 4 only; two amendments, fold into T-108 | high |
| T-084 | The language-and-jurisdiction map names only declared jurisdictions | APPARATUS (DEFER, or fold into T-101) | E1 (coverage bookkeeping) | n | Real (17 undeclared codes, 19 pairs); OD-46 is answered (2026-11-19) so the task's hold is stale; but `set-pair-scope` scopes those pairs out without it, and search rows can already carry only declared codes | medium |
| T-085 | The map's jurisdiction column points at the registry | APPARATUS (RETIRE) | — | n | An FK duplicating `add-lang-jur-pair`'s existing `dbcore.check_jurisdiction` refusal; the map is not rendered | high |
| T-086 | The stored gradients whose unit says only `ratio` | NEEDED-NOW | E2, E5 | y | 11 rows on parameter 3 (4 claims, 7 findings) are dropped from the value today; the tooling (T-093, OD-41) has merged, so only the data amendments remain | high |
| T-087 | Ship the Edmonton checklist digest as a research batch | NEEDED-LATER | E1, E2, E3 | n | Owner-requested and still unshipped (REF-01037 not held); its cells are parameters 5, 6, 9, 12; the retrieval-log payload the task relies on is absent from this container | medium |
| T-091 | A figure's circumstance (building use, interior or exterior) in typed cells | NEEDED-LATER | E3, E5 | n | Real harm in principle (a dwelling figure and a public-building figure in one headline); on parameter 3 one claim carries a home setting and 39 of 46 carry none; run the design's own measurement first, then build | medium |
| T-092 | Re-tag each stored figure's circumstance from its free-text setting | NEEDED-LATER | E3 | n | Data half of T-091; blocked on it | high |
| T-101 | Record the research scope on every pair | NEEDED-LATER | E1 | n | Real (70 pairs, 0 scoped, `v_research_scope` returns all 70); OD-04 answered; the engine does not read scope, so the parameter-3 cell is unaffected; cheap | high |
| T-102 | Decompose the mobility family by device, and carry the rows filed under MOB | NEEDED-NOW | E3 | y | Owner-confirmed codes (OD-14) unbuilt: no WHEEL/PROSTH/WALKAID; 3 parameter-3 figures sit on `SCI`, which the owner equated with WHEEL and OD-83 retires, so they fall outside a MOB cell; the first cell's group should be settled before it is published | medium |
| T-104 | Verify the sources a first determination would rest on | NEEDED-NOW | E2 | y | 6 of 27 governing sources of the probe cell are UNVERIFIED (REF-00994, -00997, -01013, -01014, -01016, -01026) and the cell's marker is `○` with `has_unverified_sources = 1` | high |
| T-105 | Read what is held, in full, against every parameter | NEEDED-LATER | E1, E2 | n | Real (EXAMINED 580, NOT-READ 417, DEBT 457 pairs) but parameter 3 has no NOT-READ or READ-PARTIAL pair | high |
| T-106 | Tag figures with every relevant model | NEEDED-LATER | E3 | n | Real (216 live lens links: 212 identity, 1 ICF, 3 need); not needed for one identity-keyed cell; overlaps T-127 for code values; its OD-47 note is stale (answered 2026-11-19) | medium |
| T-107 | Attest forms per language and jurisdiction from instruments | NEEDED-LATER | E1 | n | Real (0 of 2382 forms attested by observation); blocked on T-057 (open tooling); future non-English searches only | high |

## Per-task detail

### T-068 (NEEDED-LATER, E4)
- Evidence: `select status, count(*) from convergence_assessment group by 1` → `[('pending_assessment', 5)]`; `v_value_independence` → `[(3, 'ramp gradient', 14)]`; `v_value_independence_rows` absent. The probe cell's convergence row is `pending_assessment` with a PROXY rationale. So no page says "converge" today; the defect the task names (a convergence laundering one root) cannot occur until the engine writes `convergent`.
- Ledger: OD-43 answered (convergence = most common practice, never best practice); OD-66 closed by the sixteenth set, "just ignore the 2% and convergence because it doesn't matter enough … these aren't real decisions" (`grep -n -F "Owner instruction 2026-11-14 (sixteenth set)" references/project-standards.md`).
- Dependencies: T-059 and T-120 both still open (open-tasks.tsv), so the task cannot start.
- Recommendation: keep items 1 to 5 and 8 (one predicate, the engine's rule, the misnaming strings); treat item 6's gap-row cue and `/batch-done` line, and the "What the investigation looks at" reader (already deferred as OI-57), as apparatus. A risk to note: the regulatory-only branch hard-codes `single_axis` (`assess_cell.py:1581`), which would print "one source" over a many-code cell; that is the one string worth fixing early, and item 3 fixes it.

### T-069 (NEEDED-LATER, E1)
- Evidence: non-English observations by latest outcome `[('DEFERRED', 3), ('NAMES-EXISTING', 22), ('NAMES-NEW', 2), ('NOT-OURS', 2), ('UNADJUDICATED', 4)]`; `term_aliases where observation_id is not null` → 0; `term_aliases.attestation` → `model_seed` 1163, `unrecorded` 1219. T-026, T-028 and T-074 have merged (the `waits for T-028's occurrence grain` string is gone from `scripts/db.py`; commit da86854).
- Why later: OR-17 forbids searching on the model's own phrases, which is a research-method defect for future non-English searches; no stored figure or rendered value changes. Part of the task stays held on OI-55 (6) [UNVERIFIED whether OI-55 (6) has since been answered: no ledger line matched `OI-55 \(6\)`].

### T-070 (APPARATUS, DEFER)
- Evidence: the task measures agreement between two blind extractions and between model and effort settings; its output is a measurement, and section 4 corrects no stored row. OD-44 was answered (`OD-44: A`).
- Section 8 test: no wrong thing reaches the guidebook if it is not done; a wrong row is caught by the adversarial pass and by re-reading figures against the persisted payload (T-104's route). Defer until a determination is published and a reliability statement is wanted on the page.

### T-071 (NEEDED-LATER, E4)
- Evidence: rows with no root or `untraced`, by tier and role: tier 6 claims NULL 81; tier 3 claims NULL 5 and untraced 2; tier 5 claims NULL 4 and untraced 2; tier 4 claim NULL 1; plus conditions and findings. `root_id` set on 0 rows; `external_root_registry` 0 rows. `root_type` and `root_ref_id` are no longer in `_NOT_AMENDABLE_SVE` (`scripts/db.py:12766`), so the amendment path exists; T-048 is closed.
- Why later: roots feed only the independence count beside a convergence (T-068) and OR-19's echo presumption; the marker is the floor mean of the governing sources' bands and does not read roots. It becomes needed with T-068.

### T-072 (NEEDED-LATER, E3)
- Evidence: 10 active parameters (`select parameter_id, status from base_parameters`); the task's own expected output says no regulatory source in scope has a full reading with an open pass, which is why it waits on T-105. Dependencies T-101 and T-105 are open.
- Why later: it widens what the book can ask, not what it answers; nothing on parameter 3 depends on it.

### T-081 (NEEDED-NOW, E1, shortest path)
- Evidence: 12 rows with `results_found=0 and deferred_reason is null`, every one with `absence_class` NULL. By slug: exec 26, 27, 28 `room-acoustic-performance`; exec 29, 81, 82, 84, 85, 87, 133, 138, 191 `accessible-circulation-geometry` (parameter 3's slug). Notes: 87 "NOT A ZERO-YIELD — AN UNFIRED QUERY … All three requests returned HTTP 429"; 133, 138, 191 "RETRIEVAL FAILURE, NOT ABSENCE". `amend-search --set-absence-class` exists (`scripts/db.py:1934`).
- The wrong thing that reaches the book: DR-2026-08-19 §4's acceptance criterion publishes the determination's search log, including the empty searches. Today four searches on the parameter-3 slug that never ran would be shown as searches that found nothing, a false statement of absence. The other five need their typed cause so "no evidence exists" reads apart from "wrong index" without parsing prose; the notes carry that cause as a prefix in free text, which is the joined-cell shape CLAUDE.md §4 forbids.
- **Defect in the task file:** section 4 item 1 leaves 87, 133, 138 and 191 unamended because "`amend-search` has no deferred-reason flag", and lists them in the pull request only. So the false "found nothing" stays in the database for exactly the rows that cause the harm. The smallest repair: either a `--set-deferred-reason` on `amend-search` (tooling, a separate PR under rule 10), or re-run the four searches and log the real results. This is a dependency the plan does not list.
- Carry-only gating: OD-84 (2026-11-25) answers OI-55 (1). The batch is red on R1, R9a and R9b by construction and says so in the pull request; the task text that says "follow the coordinator's ruling when it exists" is stale.

### T-082 (NEEDED-LATER, E2)
- Evidence: `claims with no comparator` → `[(189, 'REF-00992', '1800', 'mm', None), (190, 'REF-00992', '1200', 'mm', None)]`, as the task states. `dbcore.figure_refusal` does not test the comparator, so the engine reads both figures as values, not as a floor ("can accommodate any amount of traffic") and a restricted-site allowance.
- Wrong thing (later): parameter 4's headline would take a site-restricted allowance or a capacity remark as a value. Not parameter 3. Two `amend-extraction --field comparator` calls; fold into T-108's batch, as the task itself offers.

### T-084 (APPARATUS, DEFER or fold into T-101)
- Evidence: 17 undeclared codes over 19 pairs (AR, AT, CL, CO, CR, CY, EC, ET, GH, GT, MA×2, MX, PE, PH, TH, TZ×2, UY), as the task states.
- Stale hold: the task says OD-46 is OPEN. The ledger records `OD-46: admit as declared, scoped-out codes` and `OD-46 STATUS: ANSWERED BY THE OWNER` (`references/project-standards.md:7989-7990`, ratification of 2026-11-19).
- Section 8 test: `set_pair_scope` (`scripts/db.py:9938`) scopes a pair without checking the registry, so T-101 can take these pairs out of "owed" without T-084. `add-lang-jur-pair` already refuses an undeclared code (`dbcore.check_jurisdiction`), and no search or determination can carry one. The 17 registry rows serve only T-085's FK and registry tidiness. The owner has already ruled the content, so if it is kept, do it as 17 `add-jurisdiction` calls inside T-101's batch, not as its own PR.

### T-085 (APPARATUS, RETIRE)
- Evidence: `pragma foreign_key_list(lang_jur_map)` → `[]`; `add_lang_jur_pair` calls `dbcore.check_jurisdiction(jurisdiction, …)` before inserting (`scripts/db.py:9916`), and that function refuses a code `base_jurisdictions` does not hold.
- What to delete: the task file `tasks/T-085-map-jurisdiction-foreign-key.md` and the planned schema migration. The refusal at write already exists, and an FK adds a second home for the same rule. The map is not a render surface, so no wrong thing reaches the book.

### T-086 (NEEDED-NOW, E2 and E5, shortest path)
- Evidence: `claimed_unit='ratio'` rows → extraction ids 52, 53, 54, 57, 58, 60, 61, 62, 64, 65, 66 (values 1:20 … 1:10.67), all parameter 3. Running `dbcore.figure_refusal` over parameter 3's claims gives 4 `ratio` claims refused with "the engine reads an a:b figure only under 'rise:run ratio'". The probe cell's value note lists '1:12', '1:16', '1:20' among the "24 [that] state no parsable numeric bound". The tooling has merged: T-093 is closed and commit 8461535 is "a bare ratio unit reformats to rise:run ratio (OD-41 (a))".
- The wrong thing that reaches the book: the first published cell is composed from 11 of 35 governing claims and says so on the page; four code maxima and seven findings for the same quantity are silently out of the interval.
- Dependency the plan does not list: most of the other refusals on parameter 3 (about 20 claims) are conditions written into the unit cell ("% longitudinal gradient (maximum) where the rise is <= 0.4 m …"; "rise:run ratio (maximum) where the height difference is …"). That is T-108's subject, not this task's. T-086 alone lifts 4 of the 24; T-108 is the larger half of the same shortest-path repair.

### T-087 (NEEDED-LATER, E1/E2/E3)
- Evidence: `select ref_id from evidence_sources where ref_id='REF-01037'` → `[]`; high-water mark `REF-01036`, so the batch has not shipped. `retrieval-log/session_2026-11-13-edmonton-checklist-pass` does not exist in this container (it was untracked); only the scratchpad notes (`scratchpad/session_2026-11-13-edmonton-checklist-pass/`, with ADJUDICATION.md, batch.sql, cell JSONs) are tracked.
- Why later: the owner asked for it, but its cells are parameters 5, 6, 9 and 12, not the first determination.
- Dependencies the plan does not list: (1) the PDF must be re-retrieved and persisted through `retrieval_log.py`, because the section 3 evidence command will fail here; (2) the replay must apply the sixteenth-set ruling that a code value's lens is assigned at recording, and OD-47 as answered on 2026-11-19 ("the document's stated audience judged per item by context").

### T-091 (NEEDED-LATER, E3/E5)
- Evidence: parameter 3's 46 claims carry `setting` NULL on 39; one is "home environment (domiciliary equipment prescription)", one a laboratory ramp, three kerb ramps. No typed circumstance column exists. `assess_cell.py` mentions `setting` only in a docstring (line 345).
- The wrong thing in principle: a headline that mixes dwelling and public-building figures. On the first cell that risk is one figure, and a hand read of it during judgment answers it. The design step already orders a measurement on a scratch copy of how many headlines would change. Run that measurement first, and build the carrier only if it changes headlines (CLAUDE.md §8: reuse, then the smallest code).

### T-092 (NEEDED-LATER, E3)
- The data half of T-091; blocked on it (T-091 is open). Same reasoning.

### T-101 (NEEDED-LATER, E1)
- Evidence: `select count(*), sum(scope_status is not null) from lang_jur_map` → `(70, 0)`; `v_research_scope` → 70. OD-04 is answered by the owner. `v_research_scope` is read by `scripts/db.py` (log-search's "owed" test, around line 845, and a coverage report, around lines 1456-1487) and by tests, not by `assess_cell.py`.
- Why later: it stops coverage from owing research in excluded places; the parameter-3 cell does not read scope. It is cheap (one verb call per pair) and absorbs T-084's effect on the book.

### T-102 (NEEDED-NOW, E3, shortest path)
- Evidence: mobility identities → `[('LMB', None, 'active'), ('MOB', None, 'active'), ('SCI', None, 'active')]`, so no WHEEL, PROSTH or WALKAID exists; lens links → MOB 170, ALL 34, BLIND 3, SCI 3, MS 2. On parameter 3: MOB 116 links (15 of whose claim texts name a wheelchair, 65 with a `device_class`) and SCI 3.
- Ledger: OD-14 answered by the owner with the codes (`references/project-standards.md:6063`); OD-83 (2026-11-25, delegated) retires SCI into WHEEL; the ACTION says "T-102 runs in full with existing verbs … its batch is carry-only under OD-84". Dependencies T-018, T-025, T-054 and T-055 are closed. The task's gate text ("start only when OD-14 reads ANSWERED BY THE OWNER") is met.
- The wrong thing that reaches the book: the first ramp cell would be published for MOB while three ramp figures sit on an identity the owner has said "is the same as WHEELCHAIR basically" and has ordered retired. Those figures are outside the cell, and a WHEEL cell cannot be determined at all. The owner's words of 2026-11-20 ("this project will die upon itself if it doesn't treat disability identities properly") make the lens of the first published cell part of getting it right. [Confidence medium: whether a MOB cell gathers its children's figures after the split is not verified; if it does not, choose the first published lens with that in mind.]

### T-104 (NEEDED-NOW, E2, shortest path)
- Evidence: the task's own command, run on a scratch copy, gives governing sources with `verification_status` UNVERIFIED: REF-00994 (T4), REF-00997 (T5), REF-01013 (T6), REF-01014 (T4), REF-01016 (T6), REF-01026 (T6). The probe cell carries `has_unverified_sources = 1` and `marker = '○'`. Corpus-wide: UNVERIFIED 8, VERIFIED 51.
- The wrong thing that reaches the book: six of the sources the first determination rests on were never re-retrieved (CLAUDE.md §5(c): a fabricated citation passing green gates), and the published marker is a circle over them. The owner's rule is ⚠ in place of the circle for an unverified basis.
- Dependency: the marker half needs T-117 (open tooling); until T-117 merges, the engine prints `○` over an unverified basis. Verifying the six removes the problem without waiting on T-117.

### T-105 (NEEDED-LATER, E1/E2)
- Evidence: `scan_debt.py` → `EXAMINED: 580`, `NOT-READ 417`, `DEBT: 457 pair(s)`. `v_scan_ledger` for parameter 3: EXTRACTED 52, STATED-ABSENT 5, READ-NOTHING-FOUND 1, and no NOT-READ or READ-PARTIAL. The debt sits on parameters 4 to 12.
- Why later: the first cell's sources have been read for parameter 3. The task is the main feed of every later determination, and T-072 waits on it.

### T-106 (NEEDED-LATER, E3)
- Evidence: `v_live_lens_links` → 216 rows: identity 212, ICF 1, need 3.
- Why later: one cell keyed on an identity can be published without ICF or need lenses. The owner wants the identity, need and ICF matrix ready for every later cell, so this follows the first determination.
- Stale text and overlap: the task says OD-47 is "OPEN, not yet asked"; it was answered and ratified on 2026-11-19 (`references/project-standards.md:7992-7993`). The sixteenth set assigns a code value's lens at recording, and T-127 back-fills stored code values, so T-106's scope should shrink to non-code figures to avoid sweeping rows twice. That is an overlap the plan names only as "a neighbouring task".

### T-107 (NEEDED-LATER, E1)
- Evidence: `select count(*), sum(observation_id is not null) from term_aliases` → `(2382, 0)`. Dependency T-057 (tooling, base coverage view) is open; T-026 and T-028 are closed.
- Why later: the same harm as T-069 (non-English searches on unattested words), for future searches only.

## Not reached or not verified
- OI-55 (6) (T-069's partial hold): status not found in the ledger by `git grep`; [UNVERIFIED].
- Whether the engine gathers a parent identity's children after T-102: not tested (T-102 rationale).
- The pass/fail lines of every gate the task files name (`research_batch_dod.py`, `preflight.sh`) were not run, by design (CLAUDE.md §1: run suites rarely).
- T-102-design.md and the T-091 design requirement were read only through the task files.

## Summary

Counts by class (derived: `grep -E '^\| T-' classify-2.md | awk -F'|' '{print $4}' | sed 's/ (.*//;s/^ *//;s/ *$//' | sort | uniq -c`): NEEDED-NOW 4, NEEDED-LATER 12, APPARATUS 3, ALREADY-DONE-OR-SUPERSEDED 0, OWNER-HOLD 0.

The critical few for one published determination (parameter 3, ramp gradient): **T-104** (six unverified governing sources under a circle marker), **T-086** (four code maxima and seven findings dropped from the value; the tooling has merged, only data remains), **T-081** (four never-run searches on that slug would publish as absences; the task file must be repaired to amend or re-run them) and **T-102** (the owner-confirmed mobility split, with SCI figures on a retired group). Outside this set but on the same path: T-108 (conditions in the unit cell cause most of the refused claims) and T-117 (the ⚠ marker). Retire T-085. Fold T-084 into T-101 and T-082 into T-108.
