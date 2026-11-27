# Classifier 3: T-108 to T-129 (19 tasks)

Read on 2026-11-27 against branch `ccr-64231823-gqy3xr` (head cd34b96, schema `user_version` 167). All database reads were read-only (`file:data/guidebook.db?mode=ro`). Nothing in the repository was edited. Every count below comes with the command that produced it; re-run the command before relying on the figure.

Context that applies to several tasks: `specifications` holds 8 rows, all retired, all on parameter 3 (ramp gradient) keyed `MOB` (`select specification_id,parameter_id,identity_code,state,retired_at from specifications`). So ramp gradient (parameter 3, 122 extractions) is the obvious first determination, and "shortest path" below means the path to a published ramp-gradient determination.

| id | title | class | element(s) | on the shortest path? | one-line reason | confidence |
|---|---|---|---|---|---|---|
| T-108 | Move conditions out of the unit cell | NEEDED-NOW | E2 | y | 35 extractions, most of them ramp-gradient figures, hold a sentence in `claimed_unit`. No `base_units` row matches it, so the engine leaves those figures out of the value they govern | high |
| T-109 | Give the live parameters their quantity kind | APPARATUS (RETIRE) | E3 | n | `base_parameters.quantity_kind` has no reader in the engine or in any extraction writer. Unit kinds come from `base_units`, so filling the column changes nothing in the book | medium |
| T-110 | First live determinations | NEEDED-NOW | E5, E6 | y | This is the deliverable itself (no live row in `specifications`). Its dependency list is stale: T-128 is withdrawn, and T-133 and T-123 are not needed for a ramp determination | high |
| T-111 | Bring the two stored spelled-out figures into line | NEEDED-NOW | E2 | y | The value of extraction 80 is the Finnish words `viisi prosenttia`, so the engine cannot read this ramp figure. Extraction 30 lacks its `value_as_written` | high |
| T-112 | Translate the held non-English text that synthesis needs | ALREADY-DONE-OR-SUPERSEDED | E2 | n | Done by commit 7680c9f and the review that followed. Every live non-English figure has a reviewed translation; the 23 rows left untranslated are English | high |
| T-113 | File the four held sub-national instruments under their own codes | NEEDED-NOW | E2, E4 | y | ADM vol. 2 (England), the Flemish decree, the Ontario code and the Madrid methodology are filed under UK, BE, CA and ES, and all four hold ramp-gradient figures. A comparison would say a country requires what one region requires | high |
| T-114 | Retire MOVE and VES to the access needs that carry them | NEEDED-LATER | E3 | n | The owner's ruling is not yet applied, but no row carries either code, so nothing wrong reaches the book today. Two verb calls | high |
| T-115 | Re-tag the figures filed under ALL, then retire ALL | NEEDED-LATER | E3 | n | 34 code figures carry `ALL`, all on parameters 4, 5, 6, 8, 9 and 11, none on ramp gradient. It has to be done before those parameters are determined | high |
| T-116 | Hold the upper-limb population as UPL, and retire LMB to it | NEEDED-LATER | E3 | n | No figure or grade sits on `LMB`, only 6 `identity_icf_map` rows. Step 2 copies those rows to UPL, which conflicts with the OD-77 freeze | medium |
| T-117 | The marker table applied (circle by tier, ⚠ in place of it) | NEEDED-NOW | E5, E6 | y | `band()` still gives T3 clinical ●, T3 grey and T6 ○, and T5 ◐. A regulatory-only cell is forced to ○, and the marker CHECK refuses ⚠. Every determination published today would carry a wrong marker | high |
| T-118 | The specification stage's tools carry the stage's name | APPARATUS (DEFER) | none | n | The task file says it: "Internal names only: no wrong thing reaches the guidebook". The rule is the owner's, so defer it rather than retire it | high |
| T-120 | Doctrine says what the owner ruled; dead names | NEEDED-LATER | E5 (indirect) | n | The prose contradictions are real, but item 2a (the marker table) already landed on 2026-11-26. It should stop gating T-117, T-059 and T-068. Item 6 (state-graph atoms) is apparatus | medium |
| T-122 | The stage contracts carry the owner's rulings as criteria | APPARATUS (RETIRE) | none | n | It adds contract criteria that point at tests other tasks write, plus no code. The wrong thing it names is a future regression of the apparatus, not anything in the book | high |
| T-123 | Each parameter with figures gets an accessibility direction from a source | NEEDED-LATER | E3, E5 | n | Six parameters (4, 5, 6, 8, 9, 11) have figures and no direction, so the engine states no value for them. Ramp gradient already has `lower_is_better`, and the writer refuses a second statement, so item 3 has nothing to do | high |
| T-124 | The four figures of a cell (minimum, mode, median, maximum) | NEEDED-LATER | E5, E6 | n | No function computes them, and the owner ruled that render shows them. Their absence leaves a figure out; it puts no wrong figure in | medium |
| T-125 | Judgment records a source's statement of greater difficulty | NEEDED-LATER | E2, E5 | n | One skill paragraph that teaches T-059's harm-statement record. Fold it into T-059's tooling PR; its dependency on T-035 is only a file collision | medium |
| T-127 | Give every stored code value its lens by contextual judgment | NEEDED-NOW | E3 | y | All 63 ramp-gradient code figures carry only a `carried` `MOB` link with no warrant. A ramp determination at `MOB` is barred (the children's demands are opposed), so the figures must reach the child cells through judged links | medium |
| T-128 | Population-to-ICF rows for the proposals | ALREADY-DONE-OR-SUPERSEDED | E3 | n | Withdrawn by OD-87 (2026-11-25). Its own file carries the WITHDRAWN banner | high |
| T-129 | Merge two terms judged one concept | APPARATUS (RETIRE) | none | n | It defends against a hypothetical: there is no `term_merges` table and no known duplicate pair. `merge-parameter` already joins the level determinations are keyed on. Adds a table, a view, two verbs, a check and a test file | high |

## Per-task detail

### T-108 (NEEDED-NOW, E2, on path)
- **Evidence.** The task's own command, extended to list rows: `select extraction_id, claimed_value, claimed_unit from source_value_extractions where length(claimed_unit)>20 or claimed_unit like '%(%' or claimed_unit like '% where %'`. It returns 35 rows (ids 72 to 114), for example 84 `1:6` with unit `rise:run ratio (maximum) where the height difference is <= 0.05 m`. The engine reads units only from `base_units`: `select unit from base_units` returns `% cm ft in m mm rise:run ratio`. For parameter 3, `select count(*), sum(claimed_unit not in (select unit from base_units)) from source_value_extractions where parameter_id=3 and retired_at is null` returns `(122, 48)`. Of those 48, 11 have the bare unit `ratio` (T-086's rows, not this task's), 4 have `degrees`, and the rest are this task's sentences. The dash ranges are extractions 11 and 12 (`0-4.8`, `3.5-15` degrees). Every precondition has merged: T-016 (a902516), T-061 (bdf68c9) and T-008. `condition_on` exists in `extraction_relations`.
- **Wrong thing that reaches the book.** The ramp-gradient determination is computed on about 60 % of its figures. The left-out rows include the conditional relaxations of a dozen national codes, so the code minimum, the maximum and the convergence would all be wrong.
- **Dependency not listed in the plan.** T-086 has to finish as well, or the 11 `ratio` rows stay out.

### T-109 (APPARATUS, recommend RETIRE)
- **Evidence.** `select parameter_id, quantity_kind from base_parameters` returns NULL for all 10 parameters. The readers are `git grep -n quantity_kind -- scripts ':!scripts/migrations'`, which finds only `db.py` add-parameter, set-parameter-kind and add-quantity-kind, `_kind_refusal`, and a comment in `research_batch_dod.py`. `scripts/assess/assess_cell.py` never reads it: it gets each unit's kind from `base_units.kind_id` (`dbcore.load_units`, T-030, migration 149). The task names T-030 as its reader, but T-030 merged (4ee40b6) and reads `base_units`.
- **CLAUDE.md §8.** What wrong thing reaches the guidebook without it? None: a parameter that mixes kinds is already refused when the engine composes units of different kinds. Nothing reads the added warrants. Delete the task file. Keep the column for new parameters, since add-parameter requires it. If a reader is built later (for example, refusing an extraction whose unit kind differs from its parameter's), fill the column then.

### T-110 (NEEDED-NOW, E5 and E6, the deliverable)
- **Evidence.** `select count(*), sum(retired_at is null) from specifications` returns `(8, 0)`.
- **Dependencies to correct.**
  - Remove T-128 (withdrawn, OD-87; ledger ACTION (4) of 2026-11-25 says T-110 drops the d4452-from-T-128 clause).
  - T-123 adds nothing for ramp gradient: parameter 3 already holds `lower_is_better`, and the writer refuses to state it again (`db.py set_parameter_direction`: "RE-STATING A DIRECTION IS REFUSED").
  - T-127 now waits for T-149 (tooling) and prefers T-150 (ledger OD-88 ACTION (1), 2026-11-26). Neither has a task file under `tasks/`. That is a dependency the plan's TSV does not show.
  - T-133 (records pointing at map rows, gate weighing) is outside my set; judge it as apparatus.
  - On the real path: T-108, T-111, T-086, T-113, T-117, T-102, T-127 and T-059 (the selection rule, not mine).
- **Partial owner hold, not a whole-task hold.** Section 9 stops on any cell whose selected bound is stated by a Co-1 figure, because OR-5b's three edges are open (ledger line `OR-5b STATUS: ANSWERED BY THE OWNER, PARTLY`). Ramp gradient holds no Co-1 tier in the tier split `select e.tier, count(*) ... where parameter_id=3`: 24 T1, 2 T2, 33 T3, 4 T4, 16 T5, 43 T6. Check how Co-1 is coded before relying on that.

### T-111 (NEEDED-NOW, E2, on path)
- **Evidence.** Extraction 30: value `5`, unit `%`, `<=`, `value_as_written` NULL, quote `vijf procent bij niveauverschillen…`. Extraction 80: value `viisi prosenttia`, unit `Finnish spelled-out cardinal, = 5 percen…`. GAP-056 is OPEN. T-008 has merged, and `amend-extraction` accepts `value_as_written` (`db.py` around line 12963).
- **Wrong thing that reaches the book.** The Finnish code's 5 % ramp maximum is missing from the ramp determination. Row 30 shows a numeral without recording that the source wrote it in words. That falls under the owner's rule to keep the original beside the figure (CLAUDE.md, three never-wrong things, item 2).

### T-112 (ALREADY-DONE-OR-SUPERSEDED)
- **Evidence.** `select source_table,source_column,status,count(*) from translations group by 1,2,3` returns claim_text 149 reviewed and 12 rejected, and pub_title 48 reviewed and 2 rejected. Commits 7680c9f ("translate the 24 non-English titles and 80 figures"), 2cfe7de and 75eba43 (independent reviews under OD-30). Listing every live extraction whose source is not `en` and that has no reviewed claim_text translation returns 23 rows (ids 11–18, 78, 79, 81, 126, 127, 132–134, 140, 182–186, 192). All 23 are English text whose `lang_detected` is NULL.
- **Action.** Mark it done and delete it from the open list. The NULL `lang_detected` on English sources is cosmetic.

### T-113 (NEEDED-NOW, E2 and E4, on path)
- **Evidence.** REF-00992 is filed `UK` (Approved Document M, which applies to England), REF-00995 `BE`, REF-01013 `CA`, REF-01029 `ES`. Their extraction rows carry the same codes. GAP-077 is OPEN. Every one of the four has parameter 3 rows: 3, 2, 1 and 2 respectively (`select ref_id, parameter_id, count(*) ... group by 1,2`). `base_jurisdictions` accepts `kind='sub-national'` with `<parent>-<sub>` codes, but holds none yet. `amend-extraction --field jurisdiction` exists (T-024 item 4, `dbcore.check_jurisdiction`). The approval heading is found exactly once.
- **Wrong thing that reaches the book.** A jurisdictional comparison on the ramp page would attribute England's, Flanders', Ontario's and Madrid's requirements to the UK, Belgium, Canada and Spain.
- **Out of scope here.** `jurisdiction` is stored on both `evidence_sources` and `source_value_extractions`, which is a rule-5 dual home. Not this task's to fix.

### T-114 (NEEDED-LATER)
- **Evidence.** MOVE and VES are both `active` with no successor. Searching every identity-bearing column finds no row carrying MOVE or VES: the only hits for MOVE, VES, ALL and LMB are 34 `ALL` lens links and 6 `LMB` map rows. A-PRECISION and A-STABLE exist.
- **Why it can wait.** It is cheap, but nothing wrong reaches the book until a writer tags a figure MOVE or VES. Do it whenever a batch is open.

### T-115 (NEEDED-LATER)
- **Evidence.** The task's command returns `[('code', 34, 5, 0, 0)]`: 34 `ALL` figures from 5 code sources, none with an ICF or needs lens. By parameter they are 4:11, 5:2, 6:3, 8:1, 9:12, 11:5, with no row on parameter 3. Dependencies: T-056 (open, READY) and T-127.
- **Why it can wait.** It blocks the corridor-width, turning-space, door-force, door-width and headroom determinations, not the first ramp determination.

### T-116 (NEEDED-LATER, plan defect)
- **Evidence.** `LMB` is active, with no figures or grades. `identity_icf_map` has 6 `LMB` rows. UPL is not held.
- **Plan defect.** Step 2 (`add-population-icf-link` for UPL, copying each LMB crossing) conflicts with OD-77 as resolved on 2026-11-25: "no session adds a row to `identity_icf_map`, cites one as a warrant or copies one". The exception covers only rows the owner confirmed (OI-03); the LMB rows are not among them. The smallest compliant path is to mint UPL, retire the 6 LMB rows with `retire-population-icf-link` (a retirement, not an addition), then `retire-identity --code LMB --to-identity UPL`. Whether the six crossings should instead be re-added for UPL is an owner question that OD-77 leaves open, but nothing in the book depends on the answer.
- **Downstream.** T-058 depends on this task.

### T-117 (NEEDED-NOW, E5 and E6, on path)
- **Evidence.**
  - `sed -n '/^def band(/,/^def floor_mean/p' schemas/tier_derivation.py` shows T3 FULL when clinical and WEAK otherwise, T4 and T5 PARTIAL, T6 WEAK.
  - `scripts/assess/assess_cell.py:1743` reads `if regulatory_stratum_only: source_bands = []`.
  - The `specifications` DDL has `CHECK (marker IS NULL OR (marker IN ('●', '◐', '○') AND (regulatory_stratum_only = 0 OR marker = '○')))`.
  - `grep '⚠' scripts/assess/assess_cell.py schemas/*.py` finds nothing.
  - Doctrine already carries the owner's table (`governance/tier-system.md:63-81`, line 81: "Until T-117 lands, … `band()` and the `specifications.marker` CHECK implement the earlier table"). CLAUDE.md §6 carries it too.
- **Wrong thing that reaches the book.** On the ramp page, a T4-only value would show ○ (it should be ◐), a T5 value ◐ (it should be ○), and a T3 clinical value ● (it should be ◐). A grey or unverified basis would show a circle where the owner ruled ⚠. A wrong marker is one of the named wrong things.
- **Dependencies.**
  - T-119 has merged (`git grep -c 'Unification 2026-11-14' references/project-standards.md` returns 1).
  - The T-120 dependency is met for the marker doctrine (item 2a applied 2026-11-26) and should be dropped.
  - T-068 (same function) and T-102 (for thin via parent) stay.

### T-118 (APPARATUS, recommend DEFER)
- **Evidence.** The file's own section 3 says "Internal names only: no wrong thing reaches the guidebook without this task", and section 4 says "What it makes deletable: nothing; it renames".
- **CLAUDE.md §8.** The rule behind it is the owner's ("the pipeline stage tools should match the actual name of the stage"), so defer it rather than delete it. Run it after the engine stops changing. It costs a migration, a table rebuild and a caller sweep.
- **Dependency not listed in the TSV.** T-021, which section 5 names.

### T-120 (NEEDED-LATER, split recommended)
- **Evidence.**
  - `git grep -F best_practice_synthesis` still hits `.claude/README.md`, `.claude/settings.json` and seven governance files.
  - `grep -c '## 0.' governance/evidence-architecture.md` returns 0.
  - "most-accommodating floor selection" is at `governance/evidence-architecture.md:122`, and "A code value does NOT establish best practice" at `governance/jurisdiction-philosophy.md:74`.
  - The ○ gloss "grey, thin or unverified" survives in `governance/owner-browser.yaml:111,807` and `skills/evidence-auditor_SKILL.md:47`.
  - The three files the task would delete still exist.
  - Item 2a (`tier-system.md` §5) was applied on 2026-11-26.
- **Why it can wait.** The prose contradicts the ledger, but rule 0 already makes the ledger win, and determinations are computed, not written from the prose. What a stale passage can actually do is mislead a session writing judged synthesis text or the evidence-auditor skill.
- **Recommendations.**
  - Drop T-120 as a dependency of T-117, T-059, T-068 and T-035; each can be built to the ledger.
  - Keep items 1 to 4 as one short prose PR, which the A/B approval of 2026-11-26 partly overlaps (approval-list A2, A3, B10).
  - Treat item 6 (state-graph atoms and `build_graph.py`) as APPARATUS and drop it. Item 5 (`doctrine-deltas.json`) is apparatus too.

### T-122 (APPARATUS, recommend RETIRE)
- **Evidence.** Its own text says it adds no code, only YAML criteria pointing at test cases in T-059, T-068, T-117 and T-124. Its "wrong thing" is that "a later change that undoes a ruling … breaks no stage contract". The tests those tasks write are what would go red.
- **CLAUDE.md §8.** The answer to "what reaches the book" concerns the apparatus. Delete the task file. If kept, T-037's dependency on it also goes.

### T-123 (NEEDED-LATER)
- **Evidence.** `select parameter_id, accessibility_direction, direction_ref_id from base_parameters` shows 3 and 12 `lower_is_better` with no source, and the rest NULL. Parameters with figures and no direction: 4 (24 rows), 5 (8), 6 (11), 8 (5), 9 (16), 11 (7). `assess_cell.py:877` returns no value when the direction is None.
- **Why it can wait.** It is needed before any determination of parameters 4 to 11, but not for ramp gradient. Item 3 (attach a source to parameters 3 and 12) cannot run, because the writer refuses to state a direction again.
- **Plan correction.** Remove it from T-110's preconditions for a ramp-first run.

### T-124 (NEEDED-LATER)
- **Evidence.** `git grep -n -i -E 'def .*(median|mode|minimum|maximum|figures)' -- scripts/assess/assess_cell.py scripts/dbcore.py` finds no such function, and `median` appears nowhere in `scripts`.
- **Why it can wait.** OD-63 says the render page shows the four figures as a colour code on the surveyed code bodies, so a full render needs them. DR-2026-08-19 §4's acceptance (a determination, governing sources, population-match grading, search log) does not. Leaving them out puts no wrong figure in.
- **Owner question.** If the owner counts the four figures as part of "one answered question", this becomes NEEDED-NOW: does the first published page require the minimum, mode, median and maximum?

### T-125 (NEEDED-LATER, fold recommended)
- **Evidence.** `select sum(harm_finding=1) from source_value_extractions` returns `(0,)`. `skills/run-pipeline_SKILL.md:335-339` teaches only `--harm-finding` plus an `insufficient` edge.
- **Why it can wait.** The record it teaches is T-059's. Without the skill paragraph, a harm statement may go unrecorded and the most accommodating value would stand where a source says it is worse. That is a real risk on ramp gradient (long gentle ramps against fatigue; the owner's rest-landing hypothesis, TERM-091), but the risk arises only once T-059 exists.
- **Recommendation.** Write the paragraph in T-059's own tooling PR instead of a separate task. The T-035 dependency is a file collision, not a logical need.

### T-127 (NEEDED-NOW, E3, on path for ramp gradient)
- **Evidence.**
  - First command: `(144,)` code figures with no judged link.
  - `select basis,count(*) from v_live_lens_links group by 1` returns `[('carried', 216)]`: every lens link is `carried`.
  - The 63 ramp code figures all carry `MOB` (`select identity_code, icf_code, needs_code, count(*) … parameter_id=3 and tier between 4 and 6`): `MOB` 63, and one `A-EFFORT`.
  - T-110 §4 item 2 says a `MOB` determination must pass the design-equivalence test, and the children's demands are opposed on ramp gradient. So no `MOB` ramp determination is written, and the code figures reach no child cell until links are judged.
  - T-126 has merged (3806b05), and `add-lens-link --basis context` exists.
- **Wrong thing that reaches the book.** Code figures compared under a lens no one judged (OD-65). Concretely, ramp code values either reach no cell or are lumped across wheelchair users and walking-aid users whose demands are opposed.
- **Dependency corrections.**
  - Drop T-128 (OD-87).
  - Add T-149 (wait) and T-150 (prefer) per OD-88 ACTION (1). Neither has a task file.
  - T-102 stays.
- **Scoping option.** A first batch scoped to the 63 parameter-3 rows would unblock the ramp determination without the whole 144.

### T-128 (ALREADY-DONE-OR-SUPERSEDED)
- **Evidence.** The file's banner reads "WITHDRAWN 2026-11-25 (OD-87, delegated resolution…)". The ledger reads "OD-87 (T-128 withdrawn) … OD-87 CHECK: confirmed with corrections applied". Delete it from the open list and from the preconditions of T-110 and T-127.

### T-129 (APPARATUS, recommend RETIRE)
- **Evidence.** `select name from sqlite_master where name in ('term_merges','v_term_survivor')` returns `[]`. The verbs present include `merge-parameter` (the db.py help grep counted 2 matches across `merge-term|unmerge-term|merge-parameter`; `merge-term` is absent per the task's own command). There are 94 terms and 10 parameters. The task names no actual pair of duplicate terms.
- **CLAUDE.md §8.** Determinations are keyed on `parameter_id`, and `merge-parameter` already joins two parameters found to be one. The write-time screens `_name_holder` and `_near_terms` stop near duplicates at mint. The task would add a table, a view, a helper, two verbs, a refusal on every term-taking writer, an advisory check and a test file against a split no one has observed. Delete T-129 and `T-129-design.md`. T-130, which depends on it, should be judged on the same grounds.

## Not verified
- T-108: I did not check that `amend-extraction` accepts every reformat in practice (a dry run on a scratch copy). The step-1 design depends on T-061's reformat path, which has merged.
- T-110: I did not verify how Co-1 is coded in `evidence_sources.tier`, so "no Co-1 on ramp gradient" is [UNVERIFIED].
- T-127: I did not check whether `add-icf-code` still has the off-root bug OD-88 names (T-149's fix), which is the reason it now waits.
- T-113: I did not check whether the sources' own statements of scope are in the retained payloads.

## Summary (≤150 words)

Counts by class, derived with `grep -E '^\| T-1' classify-3.md | awk -F'|' '{print $4}' | sed 's/ (.*//;s/^ *//;s/ *$//' | sort | uniq -c`:
NEEDED-NOW 6 (T-108, T-110, T-111, T-113, T-117, T-127); NEEDED-LATER 7 (T-114, T-115, T-116, T-120, T-123, T-124, T-125); APPARATUS 4 (T-109, T-122, T-129 retire; T-118 defer); ALREADY-DONE-OR-SUPERSEDED 2 (T-112, T-128); OWNER-HOLD 0.

The critical few for one published ramp-gradient determination are T-108, T-111 and T-113 (data fixes; existing verbs; ready now), T-117 (wrong markers), T-127 (judged lenses, scoped to parameter 3; now waits on T-149) and T-110 itself. Update T-110's dependency list: drop T-128, T-123, T-120 and probably T-133; add T-086, T-149 and T-150.
