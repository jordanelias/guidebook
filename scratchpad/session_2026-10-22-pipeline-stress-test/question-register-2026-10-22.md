# Question register, 2026-10-22: every question since "Stress test pipeline all directions. Attempt to render.", with the answers given, organised by pipeline stage

**What this is.** The owner's questions, verbatim, each with the answer already given (condensed, evidence kept), grouped by the stage of the spine it concerns (`base -> research -> evidence -> judgment -> synthesis -> specification -> render`, plus a cross-cutting group). Then the extrapolated questions (E1 to E13) that were derived from the throughlines. Every figure is the result of a command run on 2026-10-22 against `data/guidebook.db` at `PRAGMA user_version` = 116 (re-derive, do not quote; CLAUDE.md rule 7a). Nothing in the repository or the canonical database was changed to produce any of it; all experiments ran on scratch copies.

**Where the evidence lives (scratchpad, all under `/tmp/claude-0/-home-user-guidebook/f366a537-569c-50d0-a2d1-f74dc994928a/scratchpad/`).**
- `stress/conflicts.py` : engine on conflicting-value fixtures (G1 to G13), uses `scripts/tests/test_assess_cell_pilot.py:synth_db`.
- `stress/cells.sh` : engine over all 10 parameters and four lenses of parameter 3, on a scratch copy.
- `stress/render_attempt.py` : throwaway renderer over `v_best_practice`, on the canonical and on a populated scratch DB.
- `stress/listing.py` and `slugs-and-parameters-2026-10-22.md` : the parameter, term and slug listing with the mint-time value screen applied.
- `stress/walk_canonical.txt`, `stress/walk_populated.txt` : `workplan/pipeline-state-graph/walkability.py` output.
- `clone/` : a sparse scratch clone in which the write path was run (engine -> `emit_batch_sql.py` -> `emit_data_migration.py` -> `migrate_db.py` -> `--rebuild`).
- The ledger entry `references/project-standards.md`, "Correction 2026-10-22", and PR #201 (`jordanelias/guidebook`) hold the earlier review work.

**Standing facts the answers rely on.**
- 10 parameters (`base_parameters`), 94 terms, 106 slugs, 53 evidence sources, 101 extractions (all for parameter 3, ramp gradient, all tagged `identity_code='MOB'`), 8 determinations (all retired), 13 empty tables, 3 UNWRITABLE columns (medical lens chain).
- `source_scans` has 0 rows. `v_scan_ledger`: 47 EXTRACTED, 5 STATED-ABSENT, 468 NOT-READ.
- Engine: `scripts/assess/assess_cell.py` (`determine`, `compose_value`, `gather_*`, `stale_determinations`); writers: `scripts/db.py`; shared: `scripts/dbcore.py`.

---

## STAGE: base (vocabularies, lenses, parameters, slugs, aliases, units)

### Q6. "What about railings/rails, ramp surfaces, the ramp locations?"
**Answer given.** These are elements, and the owner's rule (parameter_declinations, TERM-089 `ramp`) is that a parameter is a quantity under determination, not an element. Of the 10 parameters only ramp gradient has extractions; ramp run length (12) is empty; there is a term `intermediate landing` (TERM-092) but no landing parameter; there is no term or parameter for handrail, surface friction or ramp location. Adding one is observe-term -> adjudicate-term -> add-parameter. Nothing assembles a ramp from its parts: C3.5 (a synthesis structure relating two or more parameters) FAILS in the capability register.

### Q7. "What about different access needs?"
**Answer given.** 17 `access_needs` rows and 43 `access_need_icf` rows exist. `needs_code` is a lens column on cells and on extractions (1 of 101 extraction rows has one). The engine never reads `access_need_icf`. A cell under need A-EFFORT received the same 26 sources and the same answer as the MOB cell. `accessibility_direction` is one value per parameter (parameter 3: lower_is_better), not per lens.

### Q9 (base half). "Do access needs, identities, ICF codes all get directed appropriately?"
**Answer given.** No. See the specification stage for the routing result. Base facts: `base_taxonomy_identity` 23, `base_icf` 72, `access_needs` 17, `identity_icf_map` 61, `access_need_icf` 43, `base_taxonomy_medical` 0, `identity_medical_map` 0, `icf_medical_map` 0 (the medical lens cannot be used: the engine refuses `--medical`, and FKs into the empty table are unwritable). `evidence_population_match` has 54 rows, all for MOB (PROXY 29, PARTIAL 21, EXACT 4), so population directness is gradeable only for MOB.

### Q11 (aliases half). "How are the correct terms/aliases ensured for other languages when searching?"
**Answer given.** `term_aliases` holds 2,382 rows in 15 languages (996 typed TRANSLATION). `alias_provenance_audit.py`: of 1,967 non-English aliases, 15 verified (Indonesian), 0 attested by a source, 1,163 model-generated, 789 provenance unknown; 880 older aliases are grandfathered; AR, BN, HI and SW are required by `lang_jur_map` but have no aliases (structurally unsearchable). Observed non-English terms: 33 of 88 observations, 11 of the 88 not adjudicated; no alias has been promoted from an observed term. No tool builds a per-language query from the alias table; `search_executions.terms_used` is filled on 12 of 191 rows.

### Q12. "What are all of our search slugs and parameters? We should have a robust value-free generic list populating both"
**Answer given.** Full listing in `slugs-and-parameters-2026-10-22.md`. Parameters: 10 (ramp gradient, corridor width, turning circle, operating force, reverberation time, LRV contrast, door width, colour temperature, headroom clearance, ramp run length). Terms: 94, of which 84 are elements, concepts, conditions, populations, methods, including 17 `functional_axis` "...demand" terms (leftover of the retired axes layer). Slugs: 106 (80 ACTIVE, 23 STUB, 3 MERGED); 81 date from the 2026-05-08 migration, 24 from 2026-07-24; a slug is a research topic; no column links a slug to a parameter; 6 slugs have any source or search, 2 have searches. Value screen (`db._VALUE_BEARING`, `db._ITEM_CODE`, the `mint-term-from-catalogue` screen): 3 terms fail (`turning circle` "360°" and `reverberation time` "RT60", both live parameters and both false positives in definition text; `visitability` "Minimum"), 2 slugs fail (`visitability-residential-accessibility-minimum-standards` "minimum", a real hit; `co1-housing-research-global-south` "1", a false positive). The owner's 2026-10-09 ruling permits pre-population only from the code and standards registries and the pre-reset corpus terms (not old Part 4 item names), "Screen, then you approve"; the registries hold documents, not quantity names, and the pre-reset terms (88) are already ported. Sanctioned routes: observe-term from admitted sources, or an approved table through `db.py mint-term-from-catalogue` (needs a dated ledger approval). Two routes were offered; the owner has not chosen.

### E2. (extrapolated) Is "slope" measured over the same thing everywhere (going versus rise, clear versus nominal width)?
Equivalence of quantity definitions across jurisdictions is a different problem from aliasing a term. Not examined.

### E3. (extrapolated) Is a US customary length converted?
Only the gradient family (`%` and `rise:run ratio`) converts (`NOTATION_FAMILIES`, `assess_cell.py`). `ft` appears as a condition row in the corpus. Not examined beyond that.

---

## STAGE: research (searching, coverage, citation mining)

### Q10 (coverage half). "How does it ensure that all jurisdictions/languages have been robustly searched? How does it do the same for academic bodies?"
**Answer given.** Measured, not ensured. 191 `search_executions` cover 2 of 106 slugs (163 and 28); none carries a `parameter_id`; 24 jurisdictions were searched against 48 in `lang_jur_map`; `v_coverage_priority` is a 7,190-row slug x jurisdiction x language to-do matrix, mostly unsearched. Language labels are case-split in the coverage views (`en`/`EN`, `fr`/`FR`, `ja`/`JA`, `nl`/`NL`: 17 raw labels, 13 folded). The index searched (`engine`) is free text with 21 distinct values; 124 of 191 are plain `web`; no registry of academic bodies, publishers or indices exists to compare coverage against; `co2` (professional-body guideline) sources: 0; `evidence_sources.language` is NULL on all 53. Gates that exist are advisory (`research_dod`, `search_log_completeness`, `research_protocol_audit`); `prior_expectation` is recorded on 163 of 191 searches, `saturation_signal` is NULL on 76, 13 zero-yield searches were kept.

### Q13 (citation mining half). "How does citation mining work for it?"
**Answer given.** Rule R2: mine every confirmed T1/T2 anchor backward and forward to depth 2 to 3 (gap-driven mode is depth 1). Logged in `citation_mining` (33 rows: 30 backward items, 14 forward items; `connections_produced` zero throughout) and on `evidence_sources.citation_mining_status` (53 sources: 15 mined, 8 deferred, 30 pending; the 30 pending are 1 T3-clinical, 2 T4, 7 T5, 20 T6). 14 backward and 10 forward mining searches are logged (`mining_direction`). `scripts/research/mining_screen.py` derives a yield from persisted reference lists using named screens in `governance/mining-screens.yaml`. New finds go through the same logged-search and admission gates.

### Q11 (search half). see base (aliases). Non-English queries in the log (78 of 191) were typed by the researcher or model.

### E9. (extrapolated) What is the stopping rule, in sources x parameters, for "robust"?
Today 520 pairs; it grows with every parameter. No rule exists. Not examined.

---

## STAGE: evidence (retrieval, admission, verification, source language)

### Q11 (retrieval half). "How are non-English sources retrieved?"
**Answer given.** `retrieval_log.fetch(url, session, ref_id)` persists the bytes with a manifest line, language-agnostic; `full_text.py` derives whole text of a held PDF or page (`[PDF page N of M]`); `page_image.py` renders pages. Quotes stay in the source's own language and are matched by `normalise_quote` (NFKC, accent-fold, letters and digits only). Nothing is translated. Source language fields: `lang_detected` set on 45 of 53, `lang_detection_method` on 38 of 53, `language` and `translation_method` NULL on all 53, `translation_reviewed` = 0 on all 53. A Finnish row stores `viisi prosenttia` as the value; the verbatim digit gate does not check the digit gloss for spelled-out numbers (a GAP was filed); the engine cannot parse the row.

### Q13 (trust half). "How can we trust the pipeline to read a source correctly?"
**Answer given.** Guaranteed: real bytes persisted; `claim_text` must occur in a persisted artefact (`_require_verbatim`); a numerical claim's digits must appear in the quote; exemptions are ledgered and refused if the text would verify; `--verify-authors` diffs stored authors against received bytes; vocabularies are column CHECKs. Not guaranteed: that a quote supports its `figure_role`, `comparator` or unit (comparator is NULL on 40 of 101 rows); that the source was read completely (`source_scans` has 0 rows; `extraction_method` is self-declared; the check that refuses "full" over a PDF with missing pages is in `record-scan`, never run). `extraction_status` over the 101 rows: preliminary 54 (12 skim), verified 31, reviewed 13, absent-confirmed 3. What earns `verified` was not traced.

### E10. (extrapolated) What happens when a code is re-issued after a determination?
Staleness detection (`stale_determinations`, writer guards) covers internal edits to the database, not external edition changes. Not examined.

---

## STAGE: judgment (what is recorded from a source)

### Q3. "Let's say we have ramp slopes at different values assigned as ratios, percentages and slopes. How are you giving them a common base? Are you converting?"
**Answer given.** Yes, within one family, exactly: `NOTATION_FAMILIES = {"gradient": ("%", "rise:run ratio")}`; canonical scale percent; conversion in `Fraction`; both notations presented, each marked stated or derived and exact or not (owner ruling 2026-09-17). Degrees are deliberately not in the family (arctangent), so a mixed-unit set refuses to compose. Probe of the reader (`bound_on_scale`): `1:12` -> 8.333%; `8.33%` (symbol in the value) -> unread; `1 in 12` -> unread; `12:1` (inverted) -> read as 1200%; `1/12` with unit `rise:run ratio` -> 0.0833% (100 times too gentle; would win a lower_is_better minimum); bare unit `ratio` or `gradient` -> unread. On the real corpus: of parameter 3's 34 governing claims, 10 enter the interval and 24 are dropped because their qualifiers live in `claimed_unit` text (unit strings such as "rise:run ratio (maximum) where the height difference is <= 0.05 m"); the value `max 5 %` (= 1:20) rests on those 10; the caveat is printed in `value_note`.

### Q4. "Let's say we have code mentions that a ramp can be a higher slope if it's less than one metre. How does that get taken in by pipeline?"
**Answer given.** In the corpus such a clause is stored as a claim row whose condition is in the unit text (rows #74, #78, #80, #84 to #88 are examples: Norwegian "1:15, 1:12 for strekninger under 3,0 m"; Finnish 5 %, relaxed to 8 % where the height difference is <= 1000 mm; a Dutch five-step table keyed on height difference 0.05, 0.10, 0.25, 0.50, 1.00 m). Row #74 etc. are dropped from the interval (unit not a bare family member). Fixture results (clean units): the five-step table gives `max 5.0 %` (the strictest step; the conditions are gone), a general 1:15 plus a relaxed 1:12 gives `6.67 %` (the relaxation vanishes: lower_is_better takes the minimum). Condition rows (`figure_role='condition'`) are linked to the determination as role `conditioning` but never composed into the value; the 10 live `condition_on` edges are not read by the engine. `specifications` has no column for a condition or a piecewise rule.

### Q8. "How does the pipeline handle qualitative information? How does it handle clauses and exceptions? How does it handle conditionals?"
**Answer given.** Qualitative claims (`claim_type='qualitative'`, 2 as claims, 24 as findings) govern state and marker but contribute no value: qualitative-only governing claims at T1 give `stated` with marker ● and a NULL value and the note "no governing claim states a numeric value". The content of a qualitative claim lives only in `source_value_extractions.claim_text`, reached through links; `specifications` has no field for it. Clauses and exceptions: see Q4. Conditionals ("if A then B"): no structure exists; a step function is five rows with conditions in free text or one row with the whole rule in the unit field. Corpus row counts: claim types numerical/claim 43, numerical/finding 14, qualitative/finding 24, absent/finding 5, range/condition 4, numerical/condition 6, framework/finding 2.

### Q13 (what to record). "How does it know what to record? How does it review the source for other information not directly related to a slug?"
**Answer given.** By contract, not by slug: R16 (read every admission against the whole parameter list; `record-scan --mode catalogue` computes the catalogue version; open pass for quantities the list lacks), R11 (observe each concept phrase in the source's own words: 88 observations, outcomes NAMES-EXISTING 40, DEFERRED 18, NOT-OURS 14, NAMES-NEW 6, 11 not adjudicated), R7 (failure and harm as first-class evidence), R12 (code values to `research_code_leads`, case studies, economics to their own tables), off-slug material to `search_candidates` (REHOME/MISC/PENDING). The scan contract has never been exercised across the corpus: `source_scans` 0 rows; 9 of 10 parameters have no extraction from any of the 53 sources; the scan ledger cannot tell "not present in the source" from "not looked at" except as NOT-READ (468 pairs).

### E1. (extrapolated) Where does applicability live (new build versus alteration, building type, public versus private)?
The `setting` column exists on `source_value_extractions`; the engine ignores it. Corpus text shows scoped clauses ("buildings under alteration or conservation only", "existing ERP/IOP"). Not examined.

### E11. (extrapolated) Would two agents, blind, extract the same rows from one source?
No inter-rater measure exists. Decision D13 (the two finished batch 23 scans as test material) is unanswered. Not examined.

---

## STAGE: synthesis (what the judgments say together)

### Q1. "How would it handle multiple competing rows on the same parameters? Have you tested a gradient of conflicting values assigned to different tier values for a parameter?"
**Answer given.** Not tested before; tested now (`stress/conflicts.py`, G1 to G13, fixtures via `synth_db`). Tier acts as a stratum gate, not a weight: anchors (T1, Co-1, T2, Co-2) take the value; T3-clinical only if no anchors; T4 to T6 only if neither. Lower strata are dropped from the value however much they disagree: G2 (T1 900 mm against three T6 codes at 1200 mm) gives `stated` ● `>=900` with the codes only as excluded links, and the exclusion reason says "disqualified on tier, verification or supersession" (wrong cause). Within the anchoring set tiers compete tier-blind and the most accommodating value wins (G3: T1 900 vs T1 1500 gives 1500, ●, no conflict recorded; G4: T1 1000 / Co-1 1500 / T2 1200 gives 1500, ●; G12 and G13 monotone gradients up and down the ladder confirm). The engine never writes `divergent`: `convergence_assessment` has 5 rows, all `pending_assessment`; `v_divergence` is empty. Unit conflict (G7) or opposing comparators (G8) or a contested direction (G10): value NULL with a note, state remains `stated` and marker ●. Same-source contest (G11, rows 900 and 1500 in one source, D-0168): collapsed to one source, picks 1500. The determination does not record which source set the value.

### Q2 (cross-referencing half). "How does the engine handle cross referencing? Testing a parameter by other related parameters?"
**Answer given.** It does not. Capability C3.5 fails (probe P-X = FAIL). 0 live `extraction_relations` edges cross parameters; `derived_from` can cross parameters in the schema. Experiment (scratch `xparam2.db`): a derived row in parameter 4 with `derived_from` base in parameter 5 and a deliberately wrong stored value (20 against base 6 + delta 2 = 8): the engine returned `stated` ● using the stored value; `v_derived_figure_check` shows the mismatch and nothing reads it; `db.amend_extraction` of the base row in parameter 5 was ALLOWED (no live determination links it); after changing the base value, `v_derived_figure_check` shows 62 and `stale_determinations` returns `[]`. `condition_on` edges are not read. `connections` and `conflicts` tables have 0 rows, free-text targets, item-layer keys.

### E4. (extrapolated) When evidence says the code is inadequate (`insufficient`, `harm_finding`), where does the book say so?
4 live `insufficient` edges and 1 `exceeds`; the engine ignores them; `search_executions.harm_finding` is not read. Not examined beyond that.

### E5. (extrapolated) How are independent confirmations told apart from echoes of one dataset?
`external_root_registry` has 0 rows; `echo_of` and `root_id` columns exist on extractions; convergence is "independent roots". Not examined.

### E6. (extrapolated) Where is a contested direction's spread stored?
The engine writes a NULL value and a note that the spread "is rendered with each population's direction stated"; no column holds the spread; `accessibility_direction` is per parameter, not per lens. Not examined beyond that.

---

## STAGE: specification (the determination)

### Q2 (assembly half). "How are specifications critically assembled?"
**Answer given (the sequence in `determine`).** gather value-supplying sources (claim/derived rows, not skimmed, source not superseded) -> gather findings (direction) -> gather confirmers -> `assess_source` per source (tier derivable from evidence_type and scope; population directness G2 via `evidence_population_match` for the identity lens only; value directness; grain G3/G6; conditioning: NON-ANCHORING, DISCOUNTED, DOWN-WEIGHTED) -> `classify` into strata -> state ladder (anchors -> stated; T3-clinical -> provisional; T4 to T6 -> provisional regulatory with a proxy branch when anchoring findings exist; else pending with a gap) -> `compose_value` (most accommodating per the parameter's direction; exact notation conversion; refusals) -> derivation handshake (function path from `identity_icf_map`, derivation_paths, cultural anchor; H4 gates cap stated to provisional) -> marker (floor of the mean of verified governing sources' bands; proxy cells weak unless a verified study confirms the code rows) -> junction rows (`specification_extraction_links`, `specification_source_links`) and `derivation_sha`. Critical checks present: tier-consistency gate, disqualification, `determination_gates` (1 open in the corpus), verbatim and CHECK gates at write, K01/K02/C10, `stale_determinations`, a falsification-condition text (boilerplate). Critical checks absent: cross-stratum conflict flag, divergence detection, cross-parameter checks, value provenance, derived-arithmetic check.

### Q5. "What about ramps needing to terminate every so often for a rest landing?"
**Answer given.** Landing interval and landing length are quantities that do not exist as parameters (TERM-092 `intermediate landing` exists as a term; ramp run length is parameter 12, empty). The corpus text carries them inside slope rows ("advised maximum between landings at least 2 m long; at most 0.5 m rise between landings"), in the dropped unit text. The relation slope-given-run-length is a `condition_on` edge within one parameter, unread. There is no structure that composes slope, run, rise per flight and landing into one rule.

### Q9 (routing half). "Do access needs, identities, ICF codes all get directed appropriately?"
**Answer given.** No (`stress/cells.sh`, `lens.db`). The engine gathers by `parameter_id` only. Parameter 3 under identity AUT, BLIND, ADHD, ICF d450 and need A-EFFORT each gets the same 26 governing sources and 101 extractions (all extractions are tagged MOB; icf_code is NULL on all 101; needs_code on 1). Population directness for a non-MOB identity is NOT_ASSESSED, which down-weights but does not stop anchoring. The "function path" for AUT (ICF d230, d710-d729, d910-d920) and BLIND (d310-d329, d460, d620) is the identity's generic `identity_icf_map` profile, unrelated to slope, yet the cell is labelled `dual`. ICF-only and need-only cells get `population_only` with the rationale "no identity_icf_map row characterises this lens". The sha for a multi-lens cell hashes only `lens_key` (first present of identity, icf, needs, medical): identity MOB and identity MOB + icf d450 produce identical `derivation_sha`.

### E7. (extrapolated) Who reaches Person Mode, and how does an individual's assessed need reach a population value?
Design scales exist (`SCALE_FROM_RECOMMENDATION`); no mechanism connects an individual assessment to a cell. Not examined.

### E8. (extrapolated) Does Co-1's non-primacy for dimensional values hold mechanically?
In fixture G4 a Co-1 value (1500) competed on equal terms with T1 and T2 and won, with `value_directness` NOT_ASSESSED. The methodology says Co-1 is not co-primary for dimensional values. Not examined further.

### E13. (extrapolated) Which determinations would change under a +/-10% perturbation of each input, and which flip state?
This is the "step values up and down" question done properly. Nothing in the pipeline does it (no sensitivity analysis). The only stepped information is what a study itself tested: 10 `tested_at` edges (9 point at a text label, 1 at a row), 4 `insufficient`, 1 `exceeds`, 8 `audited_against`, 3 `confirms`. Not examined beyond that.

---

## STAGE: render

### Q0. "Stress test pipeline all directions. Attempt to render."
**Answer given.** The pipeline cannot render today, and rendering now would mislead. Walkability (`walkability.py`): `render` is unreachable in every direction (research<->render, evidence<->render, judgment<->render, synthesis<->render, specification<->render: NO PATH, canonical and populated); its only table is the orphan `weighting_profile` (5 rows). The workplan's step 3.R (one renderer over a view to be built) is unbuilt. Canonical: all 8 determinations are retired, `v_best_practice` has 0 rows. `v_best_practice` is `SELECT * FROM specifications WHERE state IN ('stated','provisional') AND code_floor_only = 0 AND retired_at IS NULL`: pending and floor-only cells are invisible to it. Populated scratch (13 cells written by the engine): the write path replays cleanly (674 inserts in 6 tables, applied by `migrate_db`; `--rebuild` reproduces every table's rows except `data_migrations` metadata); a throwaway render assembles a ramp-gradient cell as provisional ○, proxy, unverified, "max 5 %", from 10 of 34 claims, identical across lenses, with conditions linked but not attached. Checks on the populated DB: `test_db_integrity` C10 red (4 of 4 published cells cite an unverified source: correct), `extraction_follow_up_audit` passes but the registry flags its `no_floor` claim stale (correct ratchet signal); `migration_reproducibility` and `context_map_fresh` flips are artefacts of the scratch setup. Not completed: per-writer fault-injection matrix; a second determinism run; the stress of evidence and judgment writers.

### Q6 (assembly for display). see base. A rendered ramp would need slope, run, landing, rails, surface and location composed; the plan says `items` is a Part-4 render aggregate derived from specifications, not a key.

---

## CROSS-CUTTING (assurance, testing, models, effort, scale, ownership)

### Q10 (stepping half). "How does it step values up/down for testing?"
**Answer given.** It does not. No sensitivity or perturbation mechanism exists in the engine, writers or audits.

### Q13 (work, models, effort). "How much work does a Claude agent do, and do different effort levels or models change the possible results recorded when reviewing a source?"
**Answer given.** The agent fetches, derives text, reads, and writes rows through the CLI; the gates refuse bad writes. The database stores no token, effort or model telemetry. Extraction rows carry only `created_by_session`. The only model record is `adversarial_passes` (5 rows): reviewers `claude-fable-5-1`, authors `claude-sonnet-5` or `claude-sonnet-5-5`. The Opus-class floor for `best_practice_synthesis` is doctrine (PI rule #2, DR-2026-06-10) with no check found in the writers or audits. Whether model or effort changes what is recorded is unknown; only model-independent gates would catch a difference; preserved transcripts under `transcripts/` could support a retrospective comparison.

### Q14. "Review all of my questions again ... Identify question throughlines, and extrapolate from them to ask other questions."
**Answer given.** Six throughlines: (1) does meaning survive transcription; (2) how do pieces combine; (3) who is this for (lens routing); (4) have we looked everywhere and would we know if not; (5) is assurance a mechanism or an intention; (6) what are things called and who decides. Unifying frame: a clause in a Finnish code becomes a recommendation for a particular person; each question tests one joint. Underlying tension: the owner keeps asking for an element-level assembly (a ramp as a whole); the item layer was deleted because containers that state their answers bias findings; nothing replaces its legitimate function. Priority by consequence to the book: dropped conditions and exceptions; lens routing; conflict flagging; blind double extraction; insufficiency of the code.

### E12. (extrapolated) What does the owner actually review per day, at what row volume?
D5 (who reviews vocabulary in bulk) is unanswered. Not examined.

### E0. (extrapolated) The element-level assembly tension
A coherent ramp specification (slope, run, landing, rails, surface, location) needs a composition structure; the deleted item layer once provided containers, and its removal rationale (a container named for its answer biases findings) must be honoured by any replacement. Not examined.

---

## OPEN OWNER RULINGS ALREADY RECORDED OR PENDING (context for resolutions)
- Pending, recorded in the ledger "Correction 2026-10-22" item 2: a floor claim a study confirms (all rows `absent`, no direction, migration 116 CHECK holds regulatory-stratum-only at weak). Owner to rule.
- Assumption flagged in tier-system section 8: an unretrievable source keeps its tier and may still anchor (D-0157), earning no band above weak. Owner to confirm.
- Unanswered decisions in the 2026-10-09 ledger entry: D4 (exhaustion per parameter and jurisdiction), D5 (who reviews vocabulary in bulk), D6 (an item is one parameter), D7 (category list), D9 (publish Release 0), D10 (read what is held before fetching), D11 (read out-of-bucket sources already held), D13 (finished scans as test material).
- Container cleanup (the `/tmp` sweep) denied by the auto-mode classifier; no new decision.

## CONSTRAINTS ANY RESOLUTION MUST RESPECT (from CLAUDE.md)
Rule 0 (a live owner statement supersedes records, on contact); rule 3 (migrations only, append-only); rule 4 (sweep callers: views, skills, the registry, prose); rule 5 (point, do not copy; never a second home for a fact); rules 7/7a (no hand-written counts; write the command); rule 8 (derive it or name who judged it; adding apparatus carries the burden of proof; net-negative: a PR touching scripts/, schemas/, .github/ or skills/ does not raise their line total unless its description names the exception); rule 9 (no PR watching; open the PR last); rule 10 (tooling and research ship apart; a schema migration, a new db.py verb or a new check goes in a tooling-only PR merged first); the layers (Layer 0 to 4); the item layer is gone and every `[A-Z]-NN` code is prior-version content, never a container.
