# project-standards.md — current-state extract, part 3 (source L2548-L3684)

### 2026-09-09 — lens CHECK is "at least one", not "exactly one" [L2548-L2588]
Owner words (D-0182, owner ruling 2026-09-01, three messages): "it is OKAY for a link to be absent in a related taxonomy column", "but a link MUST be tied to at least one", "and ideally it ties into many"
In force:
- Any table attaching a determination to a group of disabled people applies "at least one" lens: `CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)` — never "exactly one".
- Only the "exactly one / never two lenses in one row" clause of the 2026-08-28 ACTION is changed. The rest of that ACTION stands: lens columns, one CHECK, real typed FKs, never a `population_*` link table, and `population_code` retired in favour of the lens columns (the entry records this as still owed on `specifications.population_code`) [CHECK: whether since done].
- [CHECK: this entry names four lens columns including `medical_code`; CLAUDE.md §6 records the owner deleting the medical lens on 2026-11-16, outside this slice.]
Open: none.

### 2026-09-09 — the project is five layers; CLAUDE.md is Layer 0 [L2590-L2622]
Owner words:
"**Layer 0** is Claude.md and tools/scripts that ensure that Layer 1's architecture/shape/pipelines/schema etc are working
**Layer 1** is code architecture and data shape and pipeline orchestration and schematic compliance etc — it is what guides all processes in the pipeline
**Layer 2** is comprised of each stage in the pipeline including its tools/workflows/processes/scripts etc
**Layer 3** is the actual data being recorded in the tables
**Layer 4** is supplementary data"
In force:
- CLAUDE.md is Layer 0: it holds process, workflow and rules; every volatile fact is derived, not stated.
- `layer-N` in records dated before 2026-09-09 (principally the retired `pipeline-map.yaml`, now under `_archived/governance/`) means that file's old table-to-stage bucketing, never this five-layer model; that bucketing must be re-derived against the seven-stage spine in any case.
Open: none.

### 2026-09-09 — parameter registry is BASE; prior corpus archived; `add-term` is the naming route for now [L2625-L2681]
Owner words: "parameter at base, archive prior corpus so it can't be found by tools we use commonly, use add-term for now"
In force:
- The parameter registry is staged at `base`, not `judgment`; the adjudication that puts a row in it is judgment's, and it points.
- The prior-version corpus is archived (not deleted) under `_archived/`, which `.ignore` hides from ripgrep and the Grep tool; `grep -r`, `git grep`, Glob and Read still reach it. A path under `_archived/` is prior-version content.
- `add-term` is the naming route "for now" — a working decision, the owner's to revisit. Mint parameter names with `db.py add-term --from-observation`, never by hand and never bearing a value.
- [CHECK] `add-term` refuses a canonical name bearing a digit, a comparator or a min/max word, and refuses an existing name as NAMES-EXISTING (pointing to `adjudicate-term` instead).
- An `[A-Z]-NN` code met anywhere is not a container to file into.
- [STATUS UNCERTAIN: entry carries "AMENDED 2026-10-09 for prepopulating the parameter list only: see 'Owner statements 2026-10-09', item 3, below. Names that come out of research still follow the clause above." — the amendment lies outside this slice.]
Open: none.

### 2026-09-09 (evening) — the determination is COMPUTED, not hand-assigned [L2684-L2731]
Owner words: "oh. you have to compute it. I can't handle this load manually. you need to repair this and anything else"
In force:
- `DR-2026-08-19` §12.5's "permanently manual" clause no longer applies to `specifications`: a determination's cell state (`stated`/`provisional`/`pending`/`not_applicable`) is derived by the engine (`scripts/assess/assess_cell.py`), not asserted by hand.
- §12.5 still governs the reasoning doc, the Opus floor on `best_practice_synthesis`, the B-before-E gate and its other clauses.
- The engine still refuses `data/guidebook.db` and emits SQL replayed through `emit_data_migration.py` → `migrate_db.py`.
- [CHECK] Ratified A5 items G2, G3, G6 are implemented only in `assess_cell.source_grain()` while `schemas/directness.py` maps `co1 → specific` and `standard_eb → code` unconditionally; promotion into the shared model is register item Q4 (two implementations of one ratified rule, disagreeing).
Open: Q4 promotion of G2/G3/G6 into the shared model [OPEN].

### 2026-09-10 — the Layer 2 line, and owner-gated work [L2734-L2820]
Owner words: "deciding at Layer 2 isn't allowed, and owner-gated stuff stays"; correction same day: "you can decide at layer 2. why wouldn't you be able to? layer 2 is reserved for actual project materials tho"; second clarification same day: "layer 1 is ensuring that layer 2 works properly when project parameters"
In force (resulting state after the same-day corrections):
- Deciding at Layer 2 is NOT prohibited; a stage tool decides its own stage's business. The "decides vs invokes" test is not the rule.
- The rule is tenancy: Layer 2 is reserved for the project's real stage work (materials, tools, processes). A check is apparatus (Layer 0/1) and does not belong at Layer 2 at all; it may invoke a Layer 2 tool and let that tool decide its stage's business. What may not happen is check logic living inside project materials.
- Test for a meta-script: "is this artefact apparatus or project material, and does its filing match?"
- Layers are a recursion: Layer 0 ensures Layer 1 works; Layer 1 ensures Layer 2 works; Layer 2 is the real stage work; Layer 3 is what it produces; Layer 4 is supplementary. L1 meta-script test: "for every Layer 1 statement about what Layer 2 must produce, can Layer 2 actually produce it?"; L0 meta-script test: "for every Layer 1 property, is something gating it?"
- [CHECK] Named as misfiled on 2026-09-10 (check logic inside project-material scripts; remedy: move the check to Layer 0 calling the Layer 2 tool): `author_fidelity`, `research_contract_sync`, `pipeline_completeness_fresh`, `evidentiary_audit_fresh`, `context_map_fresh`, `site_pages_fresh`.
- Owner-gated brokenness stays (exempt from the non-compliance deletion rule) until its decision is made. Named 2026-09-10: `scripts/generate/room_page.py` and `skills/question-author_SKILL.md`, in `governance/schema-reference-exemptions.yaml`, awaiting decision 8 on the room stratum.
Open: decision 8 on the room stratum [OPEN].

### 2026-09-10 — `v_item_extractions` deleted [L2823-L2857]
Recorder entry — not owner words.
In force:
- `v_item_extractions` no longer exists (it joined on the item edge the owner's 2026-08-26 ACTION (5) removed); no replacement.
- Never quote a cross-stage view count; derive it: enumerate `sqlite_master` views, assign each to a stage under CLAUDE.md §3's seven-stage table, with `base` not a stage (a view reading one stage plus base crosses nothing).
Open: none.

### 2026-09-11 — adjudication delegated for a named set; the medical lens gets filled [L2860-L2901]
Owner words: "Fable 5.1 to adjudicate and resolve all items that are presented to me. Opus to execute in agonist-antagonist method. Ensure that medical gets filled out."
In force:
- Register row D-0188. Clause 1 delegates adjudication only for the items that were presented; it supersedes the Delegation clauses of D-0170, D-0169, D-0182 and `governance/decision-protocol.md` §2.4 items 2–3 as applied to those enumerated items and no further. The DG-NON list is not amended generally.
- Clause 3 enforces D-0170's existing adoption of the medical lens (owner, 2026-08-27: "yes we include the medical model too. we give our users the choice of what model they want to use to browse the site.").
- Lens mechanism: cite D-0184 (lens is a column; render is `WHERE medical_code = ?`), not D-0170's crossing mechanism; crossing maps survive as authoring aid and coverage measure, not the render path.
- Before escalating, search `sessions/` with `grep -r` for a ruling that already settles it; an empty table is not evidence that nobody has decided.
- [CHECK: CLAUDE.md §6 records the owner deleting the medical lens on 2026-11-16, outside this slice.]
Open: none.

### 2026-09-11 — ICD-11 is the medical-lens source, at BLOCK grain, for correspondence [L2904-L2951]
Owner words: "Yes, use ICD-11." / "eg MB5 series of codes discussing paralytic symptoms" / "we are looking through ICD-11 for how it corresponds to our existing ICF/identities/access needs on a high level"
In force:
- DG-NON item 7 answered: ICD-11 is the source.
- Grain is the BLOCK, not the entity.
- Purpose is CORRESPONDENCE (a reader with a diagnosis reaches the functional demand held), not a clinical vocabulary; it must not grow into one.
- Derive candidates via ICD-11 block → impaired ICF b-code → axis (`axes.icf_b_anchors`) → attached identities/needs, then PRUNE; never ship the raw join. Pruning reason goes in the row's `note`, strength in `mapping_confidence`.
- Leave `icd11_verified_at` NULL until a persisted WHO payload exists; never write a code from recollection. [CHECK] WHO API credentials (free registration at `icd.who.int/icdapi`) set on the remote environment would let `retrieval_log.fetch()` persist `codeinfo` payloads for `add-medical --icd11-payload`.
- [CHECK: medical lens deleted by owner 2026-11-16 per CLAUDE.md §6, outside this slice.]
Open: none.

### 2026-09-11 — medical lens "demand-populated" [L2954-L3001]
Owner words: "maybe the medical vocabulary is just too granular to be usable."
In force (after the same-day correction at L3004-L3060):
- Never pre-populate a mirror of the ICD-11 classification (from a chapter, a block list, or recollection); anchors are verified against a persisted WHO release file at write time.
- The "write a row only when a source or reader names a diagnosis" trigger is superseded the same day — see next entry.
- [CHECK: medical lens deleted by owner 2026-11-16 per CLAUDE.md §6, outside this slice.]
Open: none.

### 2026-09-11 — correction: medical lens populated by correspondence first, then on demand [L3004-L3060]
Recorder entry (adversarial pass) — not owner words; it applies the owner's "Ensure that medical gets filled out." and the granularity doubt above.
In force:
- Never mirror the classification.
- Populate by correspondence from `populations` and `axes` first — bounded at roughly 15–20 rows (identity-first/umbrella populations BAR, LPA, TALL, NDV, MOB, COM and ALL take no anchor; `governance/functional-taxonomy.md:241-245`) — then grow on demand.
- Anchor on the block whose title states the presentation, wherever it sits (chapter 21 for motor/pain; disease chapters for sensory, cognitive, energy-limiting, e.g. `9D9`, `AB5`, `6A00`, `8E49`).
- Do not cite "the circulation literature is device-based" as a property of the field; it is a finding about this project's queries.
- Measure demand against the corpus being built, not only the committed table.
- [CHECK: medical lens deleted by owner 2026-11-16 per CLAUDE.md §6, outside this slice.]
Open: none.

### 2026-09-12 — the four `scope` escalations [L3063-L3121]
Owner selections among options in `workplan/2026-09-10-b5b-scope-owner-escalation.md` — no quoted owner words.
In force:
- Ruling 1: REF-00784 — scope and tier follow from retrieved bytes, not prose records; read REF-00784 as T3 (`lower_control`).
- Ruling 2: REF-00971 / REF-00972 — `lower_control` (`scope` discriminates on study-design control; a device bench measurement with no instrumented human protocol is observational).
- Ruling 3: REF-00976 — `lower_control`, tier 3.
- Amend scope through `db.py amend-source`, with `--tier` only beside `--field scope` and only equal to the tier the ratified ladder derives; never by hand SQL.
- Sources anchoring at T3 do not make a `stated` determination; run the engine rather than predict.
- [CHECK: the 2026-09 corpus clear (L3342) and later events may have changed these rows.]
Open:
- Ruling 4 — retrospective ratification of the five `scope` values B5(b) applied on 2026-09-10 [OPEN].
- Promotion of `adjudication_integrity` out of quarantine is an owner call (OD-E ruled 2026-08-31, D-0179) [OPEN].

### 2026-09-13 — a code value confirmed by research is upgraded; empty circle is for code without research backing [L3124-L3175]
Owner words: "Sometimes code standards come from T1. If a code standard is being confirmed as genuine best practice according to studies, then the code/regulatory input can be upgraded." / "It is when a code/regulatory input does not have research backing that it gets the empty circle."
In force:
- Confirmation-by-study is a second re-graining route alongside G1's documented traceability (genealogy).
- `○` means "no research backing", not "is a code".
- Record the confirming relation on the row (a `confirms` edge is the upgrade trigger; `tested_at` is not), not in prose. The engine rule reading these edges is unbuilt: ruled and unexecuted.
- [unratified reading] An upgraded value takes the band of the confirming evidence (T1 confirmation → `●`).
Open:
- Which band an upgraded value lands in [OPEN].
- Whether T4/T5 and T6 behave alike here [OPEN].
- What counts as confirmation (a study merely using a code value as its rig setting is not confirming it) [OPEN].

### 2026-09-13 — a derived figure takes a weighted average of its inputs, not the weakest [L3178-L3218]
Owner words: "Derived figures are a weighted average of their figures. If something has like two T1 and a single T4...it's probably a half circle."
In force:
- Compute a `figure_role='derived'` row's band from all inputs; never take the weakest.
- Do not read `weighting_profile.tier_weights` as tier weights (it holds audience foregrounding).
- The weighting function, left open here, is closed later the same day — see L3304-L3339.
Open: none (closed in slice).

### 2026-09-13 — a finding that a CODE is insufficient supplies no value, and is still first-class evidence [L3221-L3256]
Owner words: "Insufficient findings don't provide anything, do they? They're insufficient. All you do is log you looked at them, I think" — confirmed on query as: the finding supplies no VALUE, but is real evidence. [CHECK: the confirmation is recorded in the recorder's words, not quoted.]
In force:
- `insufficient` is a relation (finding → baseline it says is inadequate).
- Never let such a finding supply `value_min`/`value_max`; never discard it — it anchors direction at its own source's tier, remains first-class R7 harm evidence, and is rendered.
- A cell whose only evidence is `insufficient` findings is `pending` on value and states the inadequacy.
Open: none.

### 2026-09-13 — grey literature stating a code's value is regulatory stratum [L3259-L3300]
Owner words: "If T3-grey is the same value as T6, I think T3-grey is not T3 but T6"
In force:
- Do not count a grey source as an independent root on value agreement with a code alone; check its recorded provenance first; where none exists, treat it as regulatory stratum.
- Expect no marker change (both `○`); the effect is on independence counts (`v_value_independence`) and `regulatory_stratum_only`.
Open:
- Recorder's proposed shape, for the owner to confirm or reject: value coincidence raises a rebuttable presumption of echo, rebutted only by recorded independent measurement (`root_type='measurement_primary'` with a root that is not the code) [OPEN] [unratified reading].

### 2026-09-13 — derived-figure weighting function: mean of band ordinals, ROUNDED DOWN [L3304-L3339]
Owner words: "yeah round down"
In force:
- Band of a `figure_role='derived'` row = floor(mean(ordinal(input bands))), ordinals `●`=3, `◐`=2, `○`=1, inputs equally weighted.
- Acceptance case: 2×T1 + 1×T4 → mean 2.667 → `◐` (falsifies rounding to nearest). Test rows: 3×T1 → `●`; 2×T1 + 1×T6 → `◐`; 1×T1 + 2×T6 → `○`; 99×T1 + 1×T4 → `◐`.
- Consequence: a derived figure is fully anchored only if every input is fully anchored.
- Per-input weighting by anything else (sample size, source count, directness) is NOT ruled.
- [CHECK] No numeric ordinal encoding exists in the schema; it must be introduced with the engine rule (`v_best_practice.strength_band` computes a two-value band).
Open: none.

### 2026-09-13 — the whole circulation corpus is untrusted and cleared for a re-run [L3342-L3395]
Owner words: "I want you to clear all the recent research performed and how it went down the pipeline" / "Basically all the circulation rows that have been produced are not able to be trusted, so we have to redo them all from the start"
In force:
- Every circulation row (`accessible-circulation-geometry`) any stage produced is untrusted and is to be redone from the start.
- Base vocabulary (`terms`, `term_aliases`, `slugs`) is not research output; `retrieval-log/`, `sessions/`, `attestations/` stand.
- Settle the `ref_id` minting floor BEFORE admitting the first source of a re-run, so retired identifiers are not reissued.
- Derive the scope of any clear from the slug and its reachable `ref_id`s, never from session stamps.
- [CHECK] "any future corpus clear" is subject to the 2026-09-16 retire-in-place ruling (L3538), which supersedes hard-deleting rows.
Open:
- Whether to revive `reference_stubs` (no writer) to park retired ids is a decision [OPEN].
- [CHECK] The DR-2026-08-19 clause (c) freeze-exit condition (`evidence_sources >= 1`) no longer held after the clear; recorded, not adjudicated [OPEN].

### 2026-09-13 — `AX-` may never denote an ICF code, anywhere [L3398-L3463]
Owner words: "'AX-' for ICF should never ever exist anywhere."
In force:
- Write no new `AX-` value anywhere, under any column name; the 17 code values are re-minted (`AX-` is not correct live data).
- Do not execute the re-mint piecemeal; the 2026-08-25 RULE's action item 3 stands and this ruling widens that migration. When it runs it states the new code shape explicitly.
- The ruling does not fold `icf_demands` into `access_needs`, does not retire the demand layer (its `icf_b_anchors`/`icf_d_anchors` are correct), and does not license re-minting the 17 codes as bare ICF d-codes.
- Derive the `AX-` surface, never quote it:
```
python3 - <<'PY'
import sqlite3; con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for (t,) in con.execute("select name from sqlite_master where type='table' order by name"):
    for c in con.execute(f'PRAGMA table_info("{t}")'):
        try: n = con.execute(f'select count(*) from "{t}" where "{c[1]}" GLOB "*AX-*"').fetchone()[0]
        except Exception: continue
        if n: print(f"{t}.{c[1]}: {n}")
PY
```
- [CHECK] A retired-vocabulary register entry for `AX-` cannot be written in any of the register's three match modes (each requires a non-`[\w-]` character after the token).
- The lens-column question this opened is answered by the next entry.
Open:
- Replacement code shape (`DM-AMB` to match `demand_code` is the obvious reading) [OPEN] [unratified reading].

### 2026-09-13 — the ICF lens keeps its name and holds real ICF codes [L3466-L3510]
Owner ruling (selection of an option, not quoted words) — recorder text.
In force:
- `base_icf` is the ICF registry and the one home of ICF codes; all six columns named `icf_code` (`specifications`, `source_value_extractions`, `item_taxonomy_links`, `icf_medical_map`, `access_need_icf`, `population_icf_links`) point at it.
- `base_icf` codes are seeded only from codes already held in the repository, never from a remembered classification. A title requires a `title_source`; `db.py set-icf-title --title-payload` verifies against persisted bytes. Missing titles are logged as `GAP-ICF-TITLES` and close by retrieval, never recall.
- The demand layer (`axes`, `population_axis_map`, `access_need_axis_map`) is untouched and is no longer a lens; the ICF lens holds b and d codes directly; `access_needs` keeps its e-anchors; the 2026-08-25 refusal to fold the demand layer into `access_needs` stands.
Open:
- The 2026-08-25 rename `axes` → `icf_demands` cannot execute as specified (it would put `AX-` codes in an "icf" table); what the demand layer is called, and whether it survives, is owner-gated [OPEN].

### 2026-09-13 — owner statement "access needs, ICF codes, disability identities" [L3512-L3535]
Owner words: "access needs, ICF codes, disability identities"
In force:
- [unratified reading] The three base vocabularies the pipeline keys on: `access_needs` (ICF e, what the environment must do), `base_icf` (ICF b/d, the person's function), `populations` (identity); the demand layer is not among them.
- The ICF lens is `base_icf` and holds real ICF codes; mint with `db.py add-icf-code`.
- Do not re-introduce a demand code into any `icf_*` column.
- Do not treat the medical lens as retired without an owner ruling that says so. [CHECK: CLAUDE.md §6 records such a ruling, 2026-11-16, outside this slice.]
- `GAP-ICF-TITLES` closes by retrieval and persisted bytes, never by recall.
Open:
- Whether the statement was meant to retire the medical lens — flagged, not decided [OPEN] [CHECK: see 2026-11-16 ruling outside slice].

### 2026-09-16 — RETIRE IN PLACE, NEVER HARD-DELETE [L3538-L3587]
Owner words: "retire in place then"; and "This is a recurring provenance and data management issue."
In force:
- Data rows and identifiers: retire in place — set the status the table already carries — never hard-delete. Applies to deleting a data row, retracting a source, clearing a corpus, designing a supersede path, and any migration that would empty a table.
- Before the first retirement, sweep every reader (views included) that could surface a retired row and make it filter on status; a view that does not filter is the defect. No row is retired in place until that sweep is done.
- Re-key `assess_cell`'s re-determination refusal on NOT RETIRED rather than NOT EXISTS.
- A row that MUST genuinely leave (owner-ordered destruction, fabricated data) is an exception the owner rules on case by case, recorded in this ledger.
- Does not touch CLAUDE.md §8: code, checks, scripts, dead tables and views are still deleted (git history is their archive).
Open: none.

### 2026-09-16 — dose-response evidence may be reasoned to a range, AS A PROXY [L3590-L3640]
Owner words: "even if they aren't asserting a gradient, they are examining the impacts of gradients … this means that adjudication will be able to reason that whatever range of gradients corresponds to the best outcomes is the best range of gradient" / "yes it's not perfect it's a proxy"
In force:
- A source measuring the effect of a parameter without prescribing a value is not silent on it; a determination may rest on dose-response findings, marked as a proxy, never recorded as a stated value.
- `assess_cell` must be able to reach a determination from findings plus a threshold, not only from `claim` rows [CHECK: whether built].
- The threshold half is a code value or equivalent criterion; `research_code_leads` names documents but holds no values (2026-08-12 REFERENCE-ONLY ruling), so it must be retrieved.
- Do not invent a `value_directness` scale on the strength of this statement; the proxy inference is admissible and must be marked.
- [CHECK] Lead, not a finding: REF-00985's 0°–4.8° range may match the 1:12 code ceiling (`arctan(1/12) = 4.76°`); confirm against full text before filing as anything.
Open:
- The `value_directness` scale is still owed (no ratified grading rule) [OPEN].

### 2026-09-17 — PRESENT BOTH notations; never choose between ratio and percentage [L3642-L3683]
Owner words: "Present both--don't choose between ratio or percentage."
In force:
- No notation is dropped: a governing claim stated as a ratio contributes on the same footing as one stated as a percentage.
- No notation is privileged; the determination carries both and a render surface shows both.
- Conversion is for comparison (e.g. applying the most-accommodating rule), not replacement; never overwrite what a source wrote.
- Mark any notation the engine derived rather than read; mark a non-terminating derived notation as inexact; never round it into the position of a stated figure.
- This is about notation of one quantity, not units: millimetres and degrees remain different units and the refusal to compose across them is untouched.
- [STATUS UNCERTAIN: item 4 carries "[AMENDED for exact linear units (inches, feet, millimetres, metres) by 'Owner rulings 2026-10-29 (second)' below, item 7.]" — the amendment lies outside this slice.]
Open: none.

---
Slice stats: entries read 23; entries reduced to nothing in force 0; entries tagged [STATUS UNCERTAIN] 2; lines read 2548-3684.
