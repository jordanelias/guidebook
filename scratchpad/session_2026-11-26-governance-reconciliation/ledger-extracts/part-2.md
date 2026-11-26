# project-standards.md — current-state extract, part 2 (source L1146–L2547)

Conventions: "Owner words" are verbatim from the ledger. "[unratified reading]" = recorder's interpretation, not owner words. "[CHECK]" = unsure whether history or rule, or a pointer the adjudicator should verify. "[STATUS UNCERTAIN: …]" = a later change appears to exist outside this slice; not decided here. Measured counts that the ledger quotes only as dated history are omitted.

---

### 2026-08-25 — adversarial review commissioned; scope of the one-off supersession [L1146-L1180]
Owner words: "Fable 5 read-only adversarial review of plans and contents included for logic, sequence, factuality, walkability, correctness."
In force:
- The 2026-08-19 RULE (adversarial pass) is **not amended**; the pass owed on batch 1's admitted rows stands under it unchanged.
- The review's departures from that RULE (subject = plans, a pass on a pass, and a subject plan that schedules remediation) were superseded "for this session and this purpose only" — no standing effect.
- The governing DR section for the `icf_demands` entry is §R8 of `DR-2026-08-24-scaffolding-is-phase-specific.md` ("axis" is a descriptive word; it may not be a domain identifier). [CHECK: citation fix to an earlier entry]
- The "axis" metaphor connotes, not asserts, orthogonality; `AX-AMB` and `AX-WHM` are opposed on ramp gradient. [unratified reading]
Open: none.

### 2026-08-25 — mobility split, first cut [L1184-L1230]
Owner words: "As to 'mobility', separate out into 'ambulatory' and 'wheelchair user' to start."
In force:
- Mobility is split into ambulatory and wheelchair user as the first cut; not to be relitigated. (Codes ratified 2026-08-25 as `AMB` / `WHEEL`, next entry.)
- "To start" marks a first split, not the final taxonomy; the schema must be built to extend, not to close.
- Part-time wheelchair users and balance-demand users are covered by neither code and remain owed; name them as a gap in any cell that turns on them, never silently absorb them.
- Do not write new `MOB` rows; a retained umbrella may only ever be an additive cross-cutting tag, never a replacement code (permitted-umbrella test). [CHECK: whether `MOB` survives as an additive tag is not settled in this slice beyond "MOB is superseded", next entry]
- `evidence_population_match.study_population` is free text about the study's own participants — never fanned out across a split.
- A link that genuinely applies to both groups becomes two links; where not mechanically resolvable, flag for review rather than guess.
- Reason recorded: `MOB` fails clause (c) of the permitted-umbrella test (2026-07-23), "no opposed demand between members" (ramp gradient, handrails). [unratified reading]
Open: part-time wheelchair users; balance-demand users.
[STATUS UNCERTAIN: the (item × population) / `item_population_links` cells this entry governs belong to the item layer, which CLAUDE.md §7 says the owner deleted (outside this slice).]

### 2026-08-25 — a specification keys from the judgment object and cross-references all three modes [L1234-L1287]
Owner words: "specifications as a synthesis should be keying from a judgment item (if we use the word item) and cross-referencing itself against disability populations, access needs and ICF, ie all three modes."
In force:
- The `(item × population)` cell grain is superseded; population is demoted from identity to cross-reference, alongside access needs and ICF.
- The judgment object is the canonical parameter (resolved 2026-08-26, below).
- The three modes are cross-referenced independently; none may be derived from another (deriving one from another would collapse the distinction the ruling preserves). [unratified reading — reasoning]
- Applicability is not presupposed in a primary key.
- ACTION: (1) Do not write a determination keyed on a population. (2) Do not build `db.py add-specification --state stated` (see the companion RULE on the sole-writer resolution). (3) The cross-reference structure lands in the same migration as the key change. (4) Amend R4's second sentence ("Cells are (item x population)") in `governance/research-contract.yaml` in the same change. [CHECK: whether done]
- [CHECK: ACTION (3) specifies "three N:N junctions"; the 2026-08-28 lens ruling in this slice (L2490) puts all lenses as typed columns in the same table and forbids `population_*` link tables — that bears on the junction shape.]
- [CHECK: the statement that applicability is "an OUTPUT of synthesis" is superseded by the 2026-08-27 harvest/adjudicate ruling (L1999): the crossing is judgment's output.]
Open: none in this entry (the naming question it left open is closed at L1317).

### 2026-08-25 — mobility codes `AMB` / `WHEEL`, fan-out [L1291-L1313]
Owner words: "yes, AMB and WHEEL to fan out."
In force:
- `AMB` — ambulatory disabled people. `WHEEL` — wheelchair users. `MOB` is superseded.
- `MOB` links fan out to one `AMB` and one `WHEEL` row each, carrying fields verbatim. The fan-out is a mechanical carry of the umbrella's union, not a judgment that each demand applies equally; every fanned row is pending re-derivation, and the migration header must say so. The `with-upper-limb-involvement` rows are flagged for review rather than guessed.
- Never fan out `evidence_population_match.study_population` (a grade is a fact about a paper).
- [CHECK: "pending synthesis re-derivation" — per L1999 the crossing is judgment's output.]
Open: none.
[STATUS UNCERTAIN: the fanned `item_population_links` rows belong to the item layer, which CLAUDE.md §7 says was dropped (outside this slice).]

### 2026-08-26 — the judgment object is the canonical parameter; `items` is the render rollup [L1317-L1380]
Owner words: none verbatim (owner selected the option "key on the canonical parameter"); the question answered was the owner's parenthesis "(if we use the word item)".
In force:
- The determination is keyed on the design parameter under determination, reusing `source_value_extractions.parameter_canonical`.
- `items` is demoted from identity to rollup: the Part-4 render aggregate, derived from specifications, not keyed by them.
- ACTION: (1) The P1.0 migration drops both `item_code` and `population_code` from `specifications`' identity and keys it on the canonical parameter; the cross-reference structure lands in the same migration. (2) A canonical-parameter vocabulary lands in or before that migration — the key may not be unconstrained free text; its home is the schema's own CHECK or a registry table, decided by the executing session and recorded, never a list in code. (3) `add-extraction` must require `parameter_canonical`. (4) `v_value_independence`'s grain (grouped by `population_code`) is re-derived in the same change, or independence counts fragment across populations. (5) No new writer keys anything on `item_code` at the judgment stage.
- [CHECK: CLAUDE.md §6 reports migration 071 dropped `population_code` and `item_code` from `specifications` and that `base_parameters` exists — verify by `PRAGMA table_info(specifications)`.]
Open: none.

### 2026-08-26 — §R8 rename executes together with a retired-vocabulary register entry [L1384-L1447]
Owner words: none verbatim (owner selected "schema rename plus register entry" on open decision 3 of the repair plan).
In force:
- The §R8 rename is paired with `governance/retired-vocabulary.yaml` entries, enforced by `retired_vocabulary_audit.py`.
- Order: rename first, register entry last, in one change (the register's admission test 2 forbids the reverse).
- Entries are one per retired identifier, never the bare word `axis`: `axes`, `axis_code`, `item_axis_links`, `population_axis_map`, `access_need_axis_map`, `serves_axes`, `attaches_axes`.
- `AX-` cannot be expressed in any matcher mode (no prefix mode). The migration must state whether `AX-*` code values are re-minted; if not, `AX-` goes to the register's `deferred:` section with the matcher reasoning.
- Category-A `exempt_paths` for documents recording the retirement: `DR-2026-07-22-work-from-axes.md`, `DR-2026-08-24-scaffolding-is-phase-specific.md`, this ledger, and the attestations naming them.
- The rename stays owner-gated and whole; §R8 item 3's bar on piecemeal execution is unchanged.
- `validate_axes` and `check-registry.yaml` itself are callers of the rename.
- The replacement names are now the `base_taxonomy_icf` / `icf_*` family (L2089, L2349), not `icf_demands` / `demand_*`.
Open: whether `AX-*` values are re-minted.

### 2026-08-27 — `specification` is a stage, after synthesis [L1451-L1488]
Owner words: "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications."
In force:
- `specification` is a stage after synthesis, not inside judgment; the 2026-08-25 ruling that "`specifications` is a TABLE, not a stage — `judgment` writes it" is superseded and must not be cited against this.
- Synthesis precedes specification, agreeing with `governance/conceptual-model.md` ("BPC synthesis produces specifications").
- The stage count and list are now the seven-stage spine of 2026-08-27 (L2298); the six-stage list and "substrate is still not a stage" are superseded there.
- Changes to the stage list must re-point `check-registry.yaml`'s stage-qualified `basis:` refs together (blocking gate; `--selftest` failure if piecemeal).
- [CHECK: the `stage_id[:3]` prefix derivation is reached by L2122, which says full-word namespaces retire the 3-character prefix collision hazard.]
Open: none.

### 2026-08-27 — every stage's hand-off object is `<stage>_items` [L1492-L1592]
Owner words:
- "instead of using the word 'items' or anything like that, just call them whatever their stage is and add -item … an 'item' in evidence is just under column called… evidence-item. evidence-items get judged in judgment. these judgments are judgment-item"
- "we don't need to iterate different words for item — we just append '-item'."
- (selection) "the rename creates the spine"
- "research produces many rows of evidence from one slug. each row of evidence provides one row for judgment. one-to-many rows of judgment provide one row for syntheses. one-to-many rows of syntheses provide one row for specifications."
In force:
- The hand-off object of every stage is named by its stage with `_items` appended; do not coin a distinct noun per stage. Satellite tables inside a stage keep descriptive names. [CHECK: L2122/L2375 use full stage words — `evidence_items`, `judgment_items`, `specification_items` — rather than 3-letter prefixes]
- `items` is retired as a table name outright — "the word was the ambiguity".
- Owner-ruled content is the naming and the cardinality; NOT NULL columns, junctions and the fan-out/fan-in pivot are agent design, not owner ruling (per L1776). [unratified reading]
- Evidence → judgment is 1:N (owner, 2026-08-27, L1842), superseding "each row of evidence provides one row for judgment". No `UNIQUE` on the evidence→judgment key (would abolish the dissent contest under `DR-2026-08-19` §7).
- Fan-in through synthesis → specification: a downstream-written junction rather than a back-pointer on the upstream row, so no stage writes into a completed stage. [unratified reading]
- "≥1 required per synthesis" is not expressible in SQLite DDL; it needs a check, not a constraint (L1649).
- The specification → render hand-off is not in either owner quote; render's hand-off is not a table (L1649).
- `judgment_items` is not a new table: the judgment item is `source_value_extractions` (L1842, L1880).
Open: none.

### 2026-08-27 — measure against the instrument before the database; never use E-08 [L1596-L1645]
Owner words: "yet again e-08.html appears despite me having ruled it doesn't exist a million times." Also: E-08 "has been ruled against for like a month now."
In force:
- Before reporting a measured corpus property as new, `git grep` the instrument, `decisions/` and this ledger for the same property — `grep -r` / `git grep`, never the Grep tool (blinded by `.ignore` to `sessions/`).
- When the record already carries a figure, cite it and reconcile; a fresh number that disagrees with a ratified one is a finding about the reconciliation, not a replacement.
- A regex invented at the keyboard is not a taxonomy; the instrument's numeric / prescriptive / overlap split is the taxonomy for determinations in item names.
- Do not use E-08 as an example of anything; its page was purged and its name is a catalogued defect. (Mention in a passage recording its retirement is permitted — L1776.)
Open: none.

### 2026-08-27 — nomenclature audit, second pass [L1649-L1712]
Owner words (quoted from the header of migration 046): "the entire pipeline is dynamic rendering on site"; "do not rely on artifacts for rendering the site". [CHECK: attribution of the following quoted paragraph is unclear — "Under dynamic rendering there is no per-page build event to record. A manifest of build events is not a weaker version of the right table; it is a record of something that will not happen."]
In force:
- `ren_items` (a render manifest) does not exist and must not be proposed again; cite migration 046. Render's hand-off is not a table.
- The `<stage>_items` ruling holds for the stages that produce rows.
- "≥1 required per synthesis" needs a check, not a DDL constraint.
- The specification → render hand-off is recorder extrapolation; the owner's chain (in the hand-off quote) ends at specifications. [unratified reading]
- Parts E and J of the 2026-08-27 nomenclature audit are a contradiction, not a plan; reconcile before any migration. `search_admissions` is the only keyed research→evidence edge; J's premise for deleting it is false.
- The cross-stage counts this entry told sessions to quote are superseded (L2240, L2298); evidence→judgment is 1:N (L1842), not "1:1, unresolved".
Open: reconciliation of Parts E and J. [CHECK]

### 2026-08-27 — nomenclature audit, third pass (schema correctness) [L1716-L1772]
Owner words: none — recorder/delegate entry (adversarial audit).
In force:
- Do not repeat "SQLite cannot rename" — at SQLite 3.45.1 `ALTER TABLE … RENAME` propagates through REFERENCES clauses and view bodies. The true limit: SQLite cannot add a NOT NULL foreign key to an existing table without create/copy/drop/rename.
- Price an ordinary migration series before choosing a baseline.
- Any baseline must first migrate `migration_reproducibility.py`'s `CORE_INVARIANTS` (it names tables the proposal renames or retires), or the blocking gate dies.
- Part E's single NOT NULL fan-in back-pointer columns are stale; Part B's junctions govern.
- The research→evidence key belongs on the source, not the extraction (consistent with L1880: the evidence item is the source); it needs the `DR-2026-08-06` supersession (clue store demoted — "nothing joins it, no determination may cite it") recorded before it lands. [CHECK: whether recorded]
- `syn_items` keeping PK `slug` forbids a comparative synthesis as a second row. [OPEN]
Open: DR-2026-08-06 supersession; synthesis PK vs comparative synthesis.

### 2026-08-27 — nomenclature audit, fourth pass (doctrine conformance) [L1776-L1838]
Owner words: none — recorder/delegate entry.
In force:
- Owner-ruled content of the hand-off ruling is naming and cardinality only; NOT NULL columns, junctions and the fan-out/fan-in pivot are agent design and must be labelled as derived, never placed under an owner-ruling banner.
- Mention versus use: a document that retires a token may name it; any other use is a violation (as `retired-vocabulary.yaml` codifies).
- `evidence_population_match` carries both `source_ref` and `ref_id` holding one fact — a rule-5 dual home. [OPEN / CHECK: whether fixed]
- "Unwired" and "non-blocking" are different defects: `site_pages_fresh` is invoked (render battery) and advisory; separately `regenerate_derived.sh` does not rebuild `parts/`/`site/`. The registry records that `site_pages_fresh` stays advisory until the committed-versus-generated policy is settled. [CHECK]
- A new object justified only by spine integrity (an argument about the apparatus) has not paid the §1 burden of naming what wrong thing reaches the guidebook.
- The caller set for retiring `items` must include generators (`build_site.py`), `validate_items.py`, audit scripts, tests, and the `context-map` / `pipeline-map` / `retired-vocabulary` YAMLs. [CHECK]
- (The session-close ACTION is specific to that session — expired.)
Open: `source_ref`/`ref_id` dual home; committed-versus-generated policy.

### 2026-08-27 — evidence → judgment is 1:N [L1842-L1876]
Owner words: "one evidence source may provide many rows of judgment (eg a code document like Canada's NBC 3.8)". Also, on the architecture note: "not complete, and not definitive — just a thought document".
In force:
- Evidence → judgment is 1:N. Supersedes "each row of evidence provides one row for judgment"; the superseded wording is not an argument against this.
- The rule rests on the owner's explicit instruction to adopt item #1, not on the note's status.
- The hand-off key is `source_value_extractions.ref_id` (NOT NULL, FK to `evidence_sources(ref_id)`, no UNIQUE). `judgment_items` needs no new table and no new key.
- Q1 is CLOSED: do not put the evidence→judgment cardinality to the owner again. Never add `UNIQUE(ref_id)` to that table.
- ACTION: (1) Pin the shape with a registered check — NOT NULL present, no UNIQUE on `ref_id` — so a 0-row table cannot hide regression. (2) Do not design a new judgment table.
Open: none.

### 2026-08-27 — the evidence item is the source; the judgment item is the extracted value [L1880-L1928]
Owner words:
- Evidence: "logs all relevant items found in search with a unique reference ID, DOI/PMID and other codes if available, type of source (academic, code, professional practices, etc)"
- Judgment: "delivers a verdict on an evidence item for what tier of evidence hierarchy it belongs to (1, 2…6)" · "determines category of judgment item, derives value/process/figure/goal for it"
In force:
- Evidence stage item = the source (`evidence_sources`, one row per document). Judgment stage item = the extracted, tiered, categorised value (`source_value_extractions`, one row per clause or parameter).
- `source_value_extractions` is a judgment table — a stage re-assignment, not a rename. Do not rename `evidence_sources` as part of this.
- The tier verdict is a judgment output; `tier` on `evidence_sources` is a judgment written into an evidence row. Its move is queued, not done: writer-retire → reader-retire → NULL forward, grep `scripts/migrations/data_*` first. [CHECK: whether done]
- `claim_type` is adjacent to but not the same as the ruled "category of judgment item"; that column is new. [unratified reading]
- Items #3 and #4 of the architecture note are NOT adopted (owner instruction): the clue store is not moved, and the `~825` reconciliation is not pursued.
- The note's naming grammar was not ruled by this entry. [CHECK: underscore ruled at L2122; `base_` prefixes used in later rulings]
- ACTION: (1) Re-assign `source_value_extractions` to `judgment` in `governance/pipeline-contract.yaml` and `tools/pipeline_completeness.py`; stage maps predating 2026-08-27 must be re-derived, not read. (2) Do not rename `evidence_sources`. (3) Queue the `tier` move with its measured caller set.
Open: the `tier` move.

### 2026-08-27 — the disability taxonomies are user-selectable browsing lenses, medical model included [L1932-L1958]
Owner words: "yes we include the medical model too. we give our users the choice of what model they want to use to browse the site."
In force:
- The taxonomies are views of one base, not competing vocabularies to reconcile; the reader chooses the frame.
- Never render one taxonomy as the project's own frame. A determination is keyed to base and reached through whichever lens the reader picked.
- Lens switching runs through the crossing maps; a new taxonomy needs crossings into the others or the lens cannot switch — a schema change, not a vocabulary addition.
- Reading: user agency over how a reader's experience is described is consistent with the social model and CRPD Art 4.3. [unratified reading]
Open: none.
[STATUS UNCERTAIN: CLAUDE.md §6 states the owner deleted the medical lens on 2026-11-16 (outside this slice).]

### 2026-08-27 — the target registry (`base_sources`) holds research targets, neither evidence nor research [L1962-L1995]
Owner words: "academic publishing institutions, research journals, university publications, books and articles, etc are all 'sources' for finding evidence sources. so too are countries, codes and standards, professional organizations, clinical bodies, and advocacy groups. none of these are evidence, and none of these are research. they are all prompts for research to target such that they can find evidence"
In force:
- The registry is a set of prompts for where to look; it is a third input to the research matrix alongside the clue store (topic × language × target body). [unratified reading — "third input"]
- ACTION: (1) Do not treat target-registry rows as evidence or as leads. (2) Give `search_executions.engine` a foreign key into the registry once it exists, so target coverage is measurable. (3) Settle the "sources" name collision (where to look vs `evidence_sources`, what we found) before the table is created.
Open: the registry's name. [OPEN]

### 2026-08-27 — concept vocabulary harvested at evidence, adjudicated at judgment; DR-2026-08-24 §2.4 overruled [L1999-L2049]
Owner words:
- "overrule Aug 24 DR. we go evidence>judgment>synthesis."
- "evidence is probably working by doing more cursory scans and grep/regex or whatever rather than line by line analysis, so it's probably just getting all required metadata for apa standards and listing out all concepts/topics/key words/phrases that appear in the source and then judgment phase will actually do the deep read on it to determine what can be derived from the source"
- (the aporia) "we do not want to presuppose categories/concepts/approaches/elements/techniques/practices by defining them all at the start… however we also can't perform our research properly if we don't presuppose all of those."
In force:
- Evidence harvests concepts verbatim and unjudged; judgment adjudicates with the source in hand. Every canonical concept is traceable to the sources that used it.
- The crossing is judgment's output; zero links after judgment is a defect. "Applicability is an OUTPUT of synthesis" and "zero `item_population_links` is the correct pre-synthesis state" are superseded.
- The existing topics are a revisable seed; a walk re-enters layers rather than passing through phases.
- Harvest object (evidence stage, verbatim, unjudged) and adjudication object (judgment stage, mints canonical concepts with the warranting source) — recorder's design (`observed_terms`, `term_adjudications`). [unratified reading]
- Saturation is a stopping rule alongside matrix spread. [unratified reading]
- ACTION: (1) CLAUDE.md §6 states judgment as the crossing. (2) D-0165 is downstream of judgment, not synthesis. (3) `research_batch_dod`'s R4 phase must be re-declared. [CHECK: whether done] (4) Evidence metadata is machine-fetched, never model-authored; `retrieval_log.py --verify-authors` is the guarantee.
- SCOPE: read as scoped to §2.4's deferral; §2.1 (rule 5, "point, do not copy") untouched and operative. [unratified reading]
Open: owner confirmation of the scope reading. [OPEN]

### 2026-08-27 — `base_building` is three levels; `items` is none of them [L2053-L2085]
Owner words: "Building types (eg residential, commercial), room types (eg kitchen, entry, bathroom), construction elements (eg door, door handle, window, floor) are what I wanted for that table"
In force:
- Three levels: building type · room type · construction element. `items` is none of them; `items` (design provisions) stays the Part-4 render rollup derived from specifications.
- Shape: three tables (owner, 2026-08-27, L2419): `base_building_types`, `base_room_types` (← `rooms`), `base_elements`. `items` is not renamed into `base_`.
- Reading: `items` names conflate element, parameter and determination because no element table or parameter registry existed; the three-level split removes the cause. [unratified reading]
- `items.category` holds bare letters with no name column — a second instance of the collapse. [CHECK: item layer status]
Open: none.

### 2026-08-27 — the taxonomies keep parallel `base_taxonomy_*` names; `icf_demands` superseded [L2089-L2118]
Owner words: "we have multiple taxonomies. respect that. base_taxonomy_icf, base_taxonomy_medical etc"
In force:
- `axes` → `base_taxonomy_icf`; medical → `base_taxonomy_medical`. The §R8 name `icf_demands` is superseded.
- `populations` → `base_taxonomy_identity` and `access_needs` → `base_taxonomy_needs` are derived completions of "etc", not owner words (L2170 D1). [unratified reading]
- §R8's retirement of `axes` / `axis_code` / `AX-`, rename-then-register, and the seven register entries stand. The companion replacement names are the `icf_*` family (L2349).
- The ruled anti-fold bar is the 2026-08-25 one (demand layer not folded into `access_needs`; `axes` anchors ICF b/d and carries `mechanism`, `access_needs` anchors e and carries `design_obligation`). "Do not fold any taxonomy into another" in general form is a reading (L2170 D2). [unratified reading]
- A new `base_taxonomy_medical` needs crossing maps into the others or the lens cannot switch.
Open: none.
[STATUS UNCERTAIN: CLAUDE.md §6 states the owner deleted the medical lens on 2026-11-16 (outside this slice).]

### 2026-08-27 — namespace separator is the underscore [L2122-L2131]
Owner words: "yeah use underscore then"
In force:
- Underscore, never a dot: `base_models`, `research_logs`, `evidence_items`, `judgment_items`. SQLite has no schemas; a dot collides with `schema.table` syntax. Full-word namespaces retire the collision hazard of 3-character `stage_id[:3]` prefixes.
Open: none.

### 2026-08-27 — "substrate" no longer names the pipeline layer; that layer is `base` [L2135-L2166]
Owner words: "stop using the word substrate."
In force (as refined at L2206 and L2298):
- Use `base` for the pipeline layer.
- "Substrate" is reserved for construction elements (L2206); do not grep-replace repo-wide — construction-sense occurrences are live content and must not be rewritten.
- Storage/data-store sense is wrong-domain; reword when touched.
- Register entry cannot be the bare word (the matcher's boundary would flag the construction sense); it must be path-scoped to pipeline-layer surfaces (governance/, `CLAUDE.md`, the stage maps). `_archived/` is exempt.
- `base` is a stage (stage 1, L2298); the "base is not a stage" convention and ACTION (4) of this entry are superseded.
Open: none.

### 2026-08-27 — correction to the `base_building`, `base_taxonomy_*` and underscore entries (R2 audit) [L2170-L2202]
Owner words: none — recorder/delegate entry.
In force:
- `base_taxonomy_identity` and `base_taxonomy_needs` are derived completions, labelled as derived. [unratified reading]
- The general bar "do not fold any taxonomy into another" is a reading; the ruled bar is the 2026-08-25 specific one. [unratified reading]
- M1 (orphaned `demand_*` replacement names) is resolved by the `icf_*` family (L2349); D3 (one table vs three) is resolved by "5 is three" (L2419).
Open: none remaining in this slice.

### 2026-08-27 — "substrate" reserved for construction elements [L2206-L2236]
Owner words: "reserve the word substrate for construction elements."
In force:
- "Substrate" has one correct domain: construction elements — the material an element mounts to, bears on, or is finished over. Reserved; do not touch.
- Pipeline-layer use → `base`. Storage/data-store use → wrong domain; reword when touched.
- ACTION: (1) The register entry is path-scoped to pipeline-layer surfaces (governance/, `CLAUDE.md`, the stage maps); a bare token would flag the reserved use. (2) Never rewrite a construction-sense occurrence. (3) `base_elements` carries substrate on the element ↔ context relation, not as a column on the element. [unratified reading — design consequence]
Open: none.

### 2026-08-27 — "substrate" never named a stage [L2240-L2294]
Owner words: "saying 'move clues to substrate' is nonsense to me because what the hell is substrate in our pipeline? we don't have any stage named that"
In force:
- "Substrate" as a pipeline bucket was agent-coined (a 2026-08-24 audit), never an owner statement. Say `base`.
- "Move clues to substrate" names no destination; the owner's non-adoption of the architecture note's item #3 declined a sentence whose destination does not exist. [unratified reading]
- Counts derived from the "not a stage" exclusion must not be quoted; `base`'s status is now ruled (stage 1, L2298), which supersedes this entry's OPEN on that point and its ACTIONS (2)–(3).
Open: none (closed at L2298).

### 2026-08-27 — the pipeline is seven stages, `base` first [L2298-L2345]
Owner words:
- "Base · Research · Evidence · Judgment · Synthesis · Specifications · Render"
- "base is a stage insofar as it supplies the base information upon which research can perform its task, and it doesn't belong under research because none of it IS research. it's the first layer of information"
- "Slugs isn't a stage as that word doesn't actually make sense for it."
In force:
- Seven stages, `base` first, in `governance/pipeline-contract.yaml` and `tools/pipeline_completeness.py`. The "not a stage" convention is dead.
- A table is never a stage; `slugs` is base-layer content (the topic list).
- `v_coverage_priority` (base + research; the matrix view) is a protected cross-stage pointer — do not delete it.
- Stage id is singular `specification` (owner selection, L2349); the plural stays as the recorded wording of this ruling.
- ACTION (2): quote cross-stage figures with the convention and date — the entry gives 49/31 foreign keys cross-stage/within and 10 of 18 views, measured 2026-08-27 at `user_version` 64 under a 66-table assignment. "43 / 37 on eight columns" must not be repeated. [CHECK: CLAUDE.md rule 7a requires the derivation command instead of a quoted result]
Open: none.

### 2026-08-27 — four ratification and naming choices (owner selections) [L2349-L2415]
Owner words: none verbatim beyond selections from options put (and the spine wording "Base Research Evidence Judgment Synthesis Specifications Render").
In force:
- ICF family takes `icf_*`: `axes` → `base_taxonomy_icf`; `axis_code` → `icf_code`; `item_axis_links` → `item_icf_links`; `population_axis_map` → `population_icf_map`; `access_need_axis_map` → `access_need_icf_map`; `slugs.serves_axes` → `serves_icf`; `situations.attaches_axes` → `attaches_icf`; `access_need_icf` → `access_need_icf_codes` (rename in the same migration, breaking the one-letter collision). Supersedes the §R8 `demand_*` family; §R8's retired tokens unaffected.
- Stage id singular: `specification`; hand-off object `specification_items`.
- Ratification is one decision record per substantive ruling, not one consolidated DR. The surviving substantive set of 2026-08-27: (1) seven-stage spine, `base` first; (2) the hand-off object, and evidence→judgment 1:N; (3) evidence item = source, judgment item = extraction; (4) naming grammar — underscore, `base_` prefix, `icf_*` family, singular stage ids; (5) taxonomies as browsing lenses, medical included; (6) `base_building` — levels and shape; (7) `base_sources` as a target registry; (8) concept vocabulary harvested at evidence, adjudicated at judgment, `DR-2026-08-24` §2.4 overruled. ACTION: write eight DRs plus eight register rows; attestation owed (`decisions/` is a rule-2 path). [CHECK: whether done]
- `decision_capture` stays ADVISORY for now; clear the backlog first; promotion not made in the same session as the rename. Do not cite `decision_capture` green as evidence the register is complete.
- Decisions have a dual home (`data/decisions/decision_register.yaml` and the `decisions` table) with no sync; ratifying needs two writes. Recorded, not fixed; flagged for a later cull. [OPEN]
- [CHECK: L2454 cites "`item_axis_links → base_item_icf_links` (D-0169)", which differs from `item_icf_links` here.]
Open: `decision_capture` promotion; decisions dual home.

### 2026-08-27 — `base_building` is three tables [L2419-L2450]
Owner words: "5 is three."
In force:
- Three tables: `base_building_types` (new), `base_room_types` (from `rooms`), `base_elements` (new). Supersedes the same-day one-table-with-level proposal.
- Parent columns are self-referential within each table (e.g. door handle → door).
- Cross-level relationships are many-to-many junctions; `room_items` is the existing room × element junction and is re-pointed, not replaced. No polymorphic parent column. [unratified reading — the non-nesting analysis is the recorder's]
Open: none.

### 2026-08-28 — "population" is retired vocabulary; lens names [L2454-L2486]
Owner words: "we don't use the word 'population' though. we have identity/icf/needs/medical (because i said we need the medical model too). 'base_taxonomy' instead of 'population', i think"
In force:
- Never `population` for a table, column or code naming a group of disabled people.
- Recorder's proposal, put back to the owner: use the lens name (`identity`/`icf`/`needs`/`medical`) for a link or code, and `base_taxonomy_<lens>` for the registry itself. [unratified reading]
- `evidence_population_match.study_population` / `.target_population` grade the paper's own participants and become `study_group` / `served_group`, outside the lens vocabulary. [unratified reading]
- Add `population` and `population_code` to `governance/retired-vocabulary.yaml` when the rename lands — rename first, register second, per §R8.
Open: owner confirmation of `identity` versus `base_taxonomy`; "the rename is not applied". [OPEN]
[STATUS UNCERTAIN: the entry says confirmation pending; the next entry (L2490) and CLAUDE.md §6 use `identity` lens columns, but no confirmation appears in this slice. CLAUDE.md §6 also states the medical lens was deleted 2026-11-16 (outside this slice).]

### 2026-08-28 — after the base phase, all lenses live in the same table as typed columns [L2490-L2544]
Owner words: "we must have all of identity, icf, needs and medical grouped into same tables after the base phase, and we need to do it in an intelligent manner. if i understand things correctly, it really doesn't matter if we have loads of rows concerning the same source or concept"
In force:
- After the base phase, a table attaching a determination, extraction, case study or economics entry to a group of disabled people carries four typed lens columns (`identity_code`, `icf_code`, `needs_code`, `medical_code`), each a real FK into its `base_taxonomy_*` registry, with a CHECK that a row states exactly one. Never a `population_*` link table. Never two lenses in one row. `population_code` is retired in favour of the lens columns.
- Row multiplicity is fine (owner, above): one value stated in several lenses is several rows.
- Exactly-one reasoning: the crossing maps already hold translations, so a second lens on a row would duplicate them (rule 5 in DDL). [unratified reading]
- The splinter tables `extraction_population_links`, `probe_population_links`, `citation_population_links`, `case_study_populations`, `economics_entry_populations` are deleted, not renamed.
- Scope is after the base phase: base registries keep their separate shapes and do not fold; base crossing maps are pairwise and untouched.
Open: none.
[STATUS UNCERTAIN: CLAUDE.md §6 states the owner deleted the medical lens on 2026-11-16 and that D-0182 relaxed the CHECK from "exactly one" to "at least one" (migration 065) — both outside this slice.]

---

Slice stats: entries read 29; entries reduced to nothing in force 0 (none reduced to one line; several — L1146, L1451, L2170, L2240 — survive only as pointers to later in-slice rulings plus residual items); entries tagged [STATUS UNCERTAIN] 6 (L1184, L1291, L1932, L2089, L2454, L2490); lines read 1146–2547.
