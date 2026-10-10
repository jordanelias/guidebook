# Active-conflicts register

_Rendered from `conflicts.yaml` by `build_graph.py`. A conflict here is an adjudicated disagreement between ACTIVE atoms, or between an atom and a measured mechanism; the mechanical detector's candidate pairs are not conflicts until they are written into `conflicts.yaml`. Nothing here is a ruling._

46 entries. Severity: S1 16, S2 16, S3 14. Class: DOC-DOC 15, OPEN-QUESTION 1, PROVENANCE 2, RULING-DOC 6, RULING-MECHANISM 17, RULING-RULING 4, UNRECORDED 1.

## Index

| id | sev | class | resolver | probe -> live verdict | title |
|---|---|---|---|---|---|
| C-004 | S1 | DOC-DOC | OWNER | P-ENG-T3 -> PASS | Can T3-grey or a lone T6 source anchor a floor claim, or is the cell simply pending? |
| C-005 | S1 | RULING-RULING | OWNER | -- | A T4-T6-only basis: never best-practice language, or weak-band best practice 'as currently known' |
| C-012 | S1 | RULING-MECHANISM | OWNER | P-STAGE-SVE -> FAIL | source_value_extractions: judgment-stage table (owner) vs evidence-stage table (map and CLAUDE.md) |
| C-017 | S1 | RULING-MECHANISM | OWNER | P-AXIS -> FAIL, P-G -> PASS | 'I don't want axis to be used' -- yet 'axis' remains a table, column and code vocabulary (the narrower ICF ruling is carried) |
| C-019 | S1 | RULING-MECHANISM | OWNER+AGENT | P-UNWRITABLE -> FAIL | The item layer is deleted, and is still a foreign-key target, a renderer input and the vocabulary of four standing documents |
| C-022 | S1 | RULING-MECHANISM | OWNER | P-MEDICAL -> FAIL | Medical lens: delegated to be filled, owner-alone in the DR, and unwritable in practice |
| C-024 | S1 | RULING-RULING | OWNER | P-CO1 -> FAIL | Co-1's warrant: co-production (D-0178, CLAUDE.md) versus published_corpus (co1-operational) |
| C-027 | S1 | RULING-MECHANISM | OWNER | P-I -> FAIL | Render: dynamic from the database (owner words) versus built, regenerable artefacts that no script rebuilds |
| C-028 | S1 | RULING-MECHANISM | OWNER+AGENT | P-QUARANTINE -> FAIL | Register invariants and tier-consistency have no live gate |
| C-029 | S1 | RULING-MECHANISM | OWNER | P-L -> FAIL | Direct writes to the committed database by scheduled workflows |
| C-032 | S1 | RULING-MECHANISM | OWNER+AGENT | P-V2 -> FAIL | Scan contract (any source, all parameters, whatever slug) versus a writer that binds an extraction to the admitting slug |
| C-033 | S1 | RULING-MECHANISM | AGENT | P-M -> FAIL | Every slug is searched against every lens -- the search log cannot say which lens a search covered |
| C-034 | S1 | RULING-MECHANISM | AGENT | P-O -> FAIL | The vocabulary can grow only by add-term from an observation; several base tables have no sanctioned writer |
| C-035 | S1 | RULING-MECHANISM | OWNER+AGENT | P-X -> FAIL | Synthesis across parameters: ruled cardinalities and mission test versus no structure that relates two parameters |
| C-039 | S1 | OPEN-QUESTION | OWNER | -- | Questions only the owner can answer that block engine or writer behaviour |
| C-040 | S1 | RULING-RULING | AGENT | P-ENG-T3 -> PASS | 'Tier and evidence-type assignment' and 'anything touching specifications' are permanently manual -- but the determination is computed and the tier is derived |
| C-001 | S2 | RULING-DOC | OWNER | -- | Does the guidebook teach professional judgment? |
| C-002 | S2 | RULING-DOC | OWNER | -- | Two markers or three |
| C-003 | S2 | RULING-DOC | OWNER | P-ENG-T3 -> PASS | What a 'stated' cell needs: the T3-alone question |
| C-007 | S2 | DOC-DOC | OWNER | P-ENG-STATE -> FAIL | Cell-state transition table contradicts itself |
| C-008 | S2 | RULING-DOC | AGENT | -- | Cell key still written (parameter x population) in the methodology |
| C-009 | S2 | DOC-DOC | OWNER | P-TIER-DERIVE -> FAIL | Source-type to tier mapping: national frameworks and standards |
| C-013 | S2 | RULING-MECHANISM | AGENT | P-F -> FAIL | The tier verdict is a judgment output, but the tier column lives on evidence_sources and is written at admission |
| C-014 | S2 | RULING-RULING | OWNER | -- | When does the crossing happen: at judgment, or is applicability a synthesis output? |
| C-018 | S2 | RULING-MECHANISM | OWNER | P-C -> NOT-BUILT | 'Population' is retired vocabulary; the schema, the methodology and three DRs still use it |
| C-020 | S2 | RULING-MECHANISM | AGENT | P-A -> FAIL | Splinter population link tables: 'both sweeps are done' versus five tables still present |
| C-021 | S2 | RULING-MECHANISM | AGENT | P-GT -> FAIL | determination_gates attaches to a group through one lens column |
| C-023 | S2 | PROVENANCE | OWNER | -- | D-0184 (the lens is a column) is an agent decision awaiting owner review but is treated as binding |
| C-031 | S2 | RULING-MECHANISM | AGENT | P-H -> FAIL | Retire in place requires every reader to filter status first -- some views do not |
| C-036 | S2 | UNRECORDED | OWNER | P-LEDGER-GREP -> FAIL | Owner statements whose only home is a session record |
| C-037 | S2 | DOC-DOC | OWNER | -- | Process contradictions inside the commands, agents and rules |
| C-044 | S2 | DOC-DOC | OWNER | -- | Order of retiring a column: readers, rebuild, writer (DR-2026-09-26) versus writer, reader, NULL forward (CLAUDE.md rule 5) |
| C-006 | S3 | DOC-DOC | OWNER | -- | Seven tiers, or T1-T6 plus two tracks |
| C-010 | S3 | RULING-DOC | AGENT | -- | Stage list in the 2026-08-24 DR is five stages; 'specifications is not a stage' |
| C-011 | S3 | RULING-DOC | NONE | -- | Is `base` a stage, and is it 'substrate'? |
| C-015 | S3 | DOC-DOC | OWNER | -- | Evidence collection: 'a cursory scan' or a stage that judges relevance |
| C-016 | S3 | DOC-DOC | AGENT | -- | Pointer discipline: enforced by schema shape, or not enforced |
| C-025 | S3 | DOC-DOC | AGENT | P-VERIF-VOCAB -> PASS | Co-1 operational record: sub-type lists, retired verification values, ref-id format |
| C-026 | S3 | DOC-DOC | AGENT | P-UNWRITABLE -> FAIL | jurisdictional_values: reference-only (D-0181) versus restored as research_code_leads (D-0185) |
| C-030 | S3 | DOC-DOC | AGENT | -- | How checks are added and what gates a merge |
| C-038 | S3 | DOC-DOC | AGENT | -- | Hand-written counts and enumerations that disagree with each other or with the schema |
| C-041 | S3 | DOC-DOC | OWNER | -- | Scope of the operative instrument's supersession and the read-set it prescribes |
| C-042 | S3 | DOC-DOC | AGENT | -- | What a research batch's changeset contains, and how it is classified |
| C-043 | S3 | DOC-DOC | NONE | -- | Edit-in-place versus append for corrections to the instrument; migration-number allocator; open decisions |
| C-045 | S3 | PROVENANCE | NONE | -- | Status of DR-2026-09-26 and of the DOI-stash design in the operative instrument |
| C-046 | S3 | RULING-MECHANISM | OWNER | P-FWD-FK -> INFO | Pointers run from a later stage to an earlier one -- some foreign keys run the other way |

## C-004 [S1] Can T3-grey or a lone T6 source anchor a floor claim, or is the cell simply pending?

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-ENG-T3` = **PASS**

- tier-system section 8: every tier can anchor a best-practice claim; T3-grey and T6 sit in a weak band that anchors a floor claim.  
  _atoms:_ `EVI-049`(act), `EVI-055`(act)
- evidence-methodology: T3-grey alone and a single T6 source yield pending, i.e. no claim.  
  _atoms:_ `EVI-326`(act), `EVI-338`(act)

**Direction.** UNSETTLED. The engine returns pending for T3-grey alone (branch comment cites the tier3-stated-threshold DR, 2026-07-12); Option A (2026-07-21) is later and introduces the weak band. Whether Option A reached T3-grey is not stated. [ASSUMPTION: a lone T6 is handled by the regulatory branch, not re-derived here.]

## C-005 [S1] A T4-T6-only basis: never best-practice language, or weak-band best practice 'as currently known'

**Class** RULING-RULING  ·  **Resolver** OWNER  ·  **Confidence** medium

- 2026-07-13 and tier-system section 3: a basis of T4-T6 only never renders best-practice language in any register; a converged T5/T6 value is never 'best practice'.  
  _atoms:_ `LED-018`(act), `EVI-034`(act), `EVI-035`(act)
- 2026-07-21 Option A: code-consensus-only claims may render at the weak band if flagged; never unflagged or above weak.  
  _atoms:_ `LED-013`(act), `LED-014`(act), `EVI-094`(act), `EVI-241`(act), `POS-03`(act)
- methodology 3.4 offers the bare construction 'Code requires [value] per [standard]' for T4-T6-only cells, against the I3 flag-and-caveat requirement (EVI-229/230/194).  
  _atoms:_ `EVI-394`(act)

**Direction.** Option A (2026-07-21) is the later owner directive; LED-018 (2026-07-13) is not marked amended in the ledger and EVI-058 limits the older prohibition to cells without anchoring evidence. Treat LED-018 as amended in part; the status correction is owed. Render-side enforcement is the quarantined register check (see C-031).

## C-012 [S1] source_value_extractions: judgment-stage table (owner) vs evidence-stage table (map and CLAUDE.md)

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-STAGE-SVE` = **FAIL**

- owner 2026-08-27: source_value_extractions is a judgment-stage table.  
  _atoms:_ `LED-106`(act)
- pipeline-contract: the hand-off from evidence to judgment is source_value_extractions.ref_id NOT NULL, no UNIQUE -- the fan-out from one source to many judgment rows.  
  _atoms:_ `PIP-10`(act)

**Direction.** governance/stage-map.yaml renders the table at EVIDENCE and records the dispute as open (disputed: block). CLAUDE.md section 3's stage table says evidence holds 'extraction'. LED-106 is an owner ruling; under rule 0 the map and CLAUDE.md are what to correct. The consequence is not cosmetic: add-extraction writes evidence_sources.data_capture_status in the same transaction, a judgment-to-evidence write that the code comment itself calls 'evidence the column is in the wrong home'.

## C-017 [S1] 'I don't want axis to be used' -- yet 'axis' remains a table, column and code vocabulary (the narrower ICF ruling is carried)

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-AXIS` = **FAIL**  ·  **Probe** `P-G` = **PASS**

- owner: 'axis' must not name a vocabulary layer; AX- must never denote an ICF code anywhere; work in ICF/access-need codes AND names.  
  _atoms:_ `LED-076`(act), `LED-166`(act), `CLM-039`(act)
- 08-24 header: the axes rename is 'authorized and owed'.  
  _atoms:_ `DRS-006`(act)
- the same DR's R8 item 3: 'NOT DECIDED HERE', must not be attempted piecemeal.  
  _atoms:_ `DRS-023`(ope), `DRS-024`(act)
- D-0170 and D-0184 and functional-taxonomy still use `axes`, `item_axis_links`, `population_axis_map`, AX-* as live objects.  
  _atoms:_ `DRS-114`(act), `DRS-189`(act), `DRS-193`(act), `DRS-199`(ope), `ENT-105`(act), `ENT-156`(act), `ENT-076`(act)

**Direction.** LED-166 (an AX- code in an ICF-typed column) is carried: P-G passes. LED-076 is not: P-AXIS lists the tables and columns that still carry the word. The 2026-08-18 'bad coined term, do not relitigate' ruling is cited in CLAUDE.md rule 0 but was not found in the ledger by the ENT extractor (ENT note 10); LED-076 and LED-166 are the recorded owner statements. The rename itself is 'NOT DECIDED HERE' (DRS-024) -- no decision record executes it.

## C-019 [S1] The item layer is deleted, and is still a foreign-key target, a renderer input and the vocabulary of four standing documents

**Class** RULING-MECHANISM  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-UNWRITABLE` = **FAIL**

- items holds 0 rows and is a Part-4 render rollup derived from specifications; never file into an [A-Z]-NN container.  
  _atoms:_ `CLM-048`(act), `LED-091`(act)
- conceptual-model and functional-taxonomy: items.item_code is the Part-4 organizing unit; specification values attach to items.  
  _atoms:_ `ENT-023`(act), `ENT-148`(act), `ENT-172`(act), `ENT-002`(act), `ENT-003`(act), `ENT-029`(act)
- process rules and the operative instrument cross-reference item-layer cells (F-07, A-16, A-18, AUT).  
  _atoms:_ `PRC-027`(act), `PRC-059`(act), `PRC-068`(act), `OPI-047`(ope), `OPI-048`(ame), `OPI-050`(act)

**Direction.** Rulings of 2026-08-26 and 2026-09-01 supersede the item-keyed documents on contact. Mechanism: the derived UNWRITABLE set (see STATE-GRAPH.md) is the measured residue; renderer queries that still select item_code fail (P-K).

## C-022 [S1] Medical lens: delegated to be filled, owner-alone in the DR, and unwritable in practice

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-MEDICAL` = **FAIL**

- D-0184: populating base_taxonomy_medical is 'the owner's alone' (DG-NON).  
  _atoms:_ `DRS-194`(act)
- D-0188 delegates adjudication and execution to an agent for 'enumerated items and no further' and orders medical filled out.  
  _atoms:_ `DRS-231`(act), `DRS-232`(act), `DRS-233`(act), `LED-154`(act)
- the owner's words, 'all items that are presented to me', read wider than the DR's enumeration.  
  _atoms:_ `DRS-229`(act)

**Direction.** UNSETTLED which of D-0184 and D-0188 governs the medical rows. Mechanism: add-extraction refuses a lens code when its registry table is empty, so no extraction can carry a medical lens until the registry holds a row; the writer for the registry exists (add-medical) and was not run.

## C-024 [S1] Co-1's warrant: co-production (D-0178, CLAUDE.md) versus published_corpus (co1-operational)

**Class** RULING-RULING  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-CO1` = **FAIL**

- D-0178: a Co-1 tier is unwarranted-pending unless co1_provenance names the co-production; published_corpus is not a warrant.  
  _atoms:_ `DRS-146`(act), `DRS-147`(act), `DRS-148`(act), `CLM-037`(act)
- co1-operational: co1_provenance is {published_corpus, participatory_synthesis}; every pre-launch Co-1 citation must be published_corpus; grounds Co-1 in peer review, organisational accountability or scholarly authorship.  
  _atoms:_ `DRS-264`(act), `DRS-265`(act), `DRS-251`(act)

**Direction.** UNSETTLED. Mechanism: P-CO1 compares the live co1_source_type values with schemas.enums.Co1SourceType; the engine already treats the vocabulary as open (assess_cell.py module comment). Which warrant decides whether a source may be tiered Co-1, and so whether a cell can be stated.

## C-027 [S1] Render: dynamic from the database (owner words) versus built, regenerable artefacts that no script rebuilds

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-I` = **FAIL**

- owner words (quoted from migration 046's header, 2026-08-27): rendering is dynamic from the database; no per-page build event; the site must not rely on built artefacts; render has no hand-off table.  
  _atoms:_ `LED-103`(act), `LED-104`(act), `LED-105`(act)
- contract and CLAUDE.md: parts/ and site/ must not be stale relative to the DB; regenerate with scripts/regenerate_derived.sh.  
  _atoms:_ `PIP-07`(act), `CLM-050`(act)

**Direction.** P-I: regenerate_derived.sh does not mention parts/ or site/; P-K: renderers whose specifications query fails on the live schema. Neither reading is currently satisfiable: 'regenerate' reaches no such artefact and 'dynamic' has no live renderer. Owner decision needed on what render IS now.

## C-028 [S1] Register invariants and tier-consistency have no live gate

**Class** RULING-MECHANISM  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-QUARANTINE` = **FAIL**

- every rendering carries the identical tuple across registers; every rendered figure carries its strength flag; unmarked is an error.  
  _atoms:_ `PIP-06`(act), `POS-03`(act), `LED-019`(act)

**Direction.** The check that enforces these (register_integrity_check) is QUARANTINED because it is red by construction from the first determination onward; adjudication_integrity (tier derivation) is QUARANTINED and currently green. The generator reads the registry to list what is quarantined. Nothing live gates the weak-band rendering rule.

## C-029 [S1] Direct writes to the committed database by scheduled workflows

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-L` = **FAIL**

- the database is never written directly; nothing but migrate_db.py opens it read-write (OPI-124); direct writes fail the reproducibility check.  
  _atoms:_ `CLM-012`(act), `LED-153`(act), `ENT-468`(act), `OPI-124`(act)
- the committed DB reproduces the core invariants from migration history; job-owned tables are the only exception.  
  _atoms:_ `PIP-18`(act)

**Direction.** CLAUDE.md names one workflow (source-verification / resolve-dois.yml). P-L finds every workflow that `git add`s the DB blob. migration_reproducibility compares row counts only and exempts the author and run tables, so UPDATEs are invisible.

## C-032 [S1] Scan contract (any source, all parameters, whatever slug) versus a writer that binds an extraction to the admitting slug

**Class** RULING-MECHANISM  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-V2` = **FAIL**

- owner 2026-10-09: every admitted source is scanned for any and all applicable parameters; slugs guide searches only and do not limit what is mined.  
  _atoms:_ `LED-195`(act), `LED-196`(act), `LED-197`(act), `LED-199`(act)
- a figure from a source filed under another slug may be extracted and set a published value, tagged for follow-up.  
  _atoms:_ `LED-201`(act), `SES-057`(act)
- the earlier 2026-09-18 statements ('anything relevant to accessibility may be mined', 'search by slug, adjudicate by all slugs in a category') are not restated; 'category' is never defined.  
  _atoms:_ `SES-024`(act), `SES-025`(act)

**Direction.** P-V: the (source x parameter) read-state ledger does not exist on main (built in the unmerged T1 branch). P-V2: add-extraction refuses a ref that source_slug_links does not hold for the named slug; its comment argues ref-slug coherence is the stronger invariant, the opposite of LED-196. The ruling is not carried until T1 merges and the guard is reconciled.

## C-033 [S1] Every slug is searched against every lens -- the search log cannot say which lens a search covered

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-M` = **FAIL**

- owner/contract 2026-08-24: every slug is searched against every population/access-need/ICF code (R4 adds the medical lens).  
  _atoms:_ `LED-084`(act), `RES-04`(act)
- 2026-03-18 and population-taxonomy: each slug covers exactly one population; one slug, one population.  
  _atoms:_ `LED-029`(act), `ENT-236`(ame), `ENT-247`(ame), `ENT-222`(sup)

**Direction.** LED-084 supersedes LED-029 on contact (status correction owed: LED-029 -> SUPERSEDED). Mechanism: search_executions has no lens column and no linked table records slug x lens coverage, so R4 cannot be shown to have been done.

## C-034 [S1] The vocabulary can grow only by add-term from an observation; several base tables have no sanctioned writer

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-O` = **FAIL**

- parameter names are minted only from an observed phrase via add-term --from-observation.  
  _atoms:_ `LED-150`(ame), `LED-203`(act), `SES-065`(ame)
- 2026-10-09 amends that for prepopulation: names may come from previous catalogues, screened, listed once with source and approved by the owner before minting.  
  _atoms:_ `LED-204`(act), `LED-205`(act), `SES-058`(ame)
- when no verb can write a column, add the verb before claiming the write; a table the CLI cannot reach is a coverage bug.  
  _atoms:_ `LED-182`(act), `CLM-031`(act)

**Direction.** Prepopulation has no verb on main (the T1 branch adds mint-term-from-catalogue). P-O lists base tables that no db.py verb writes. These are Layer 1 gaps, filed as GAPS rather than patched with SQL (rule 10).

## C-035 [S1] Synthesis across parameters: ruled cardinalities and mission test versus no structure that relates two parameters

**Class** RULING-MECHANISM  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-X` = **FAIL**

- owner 2026-08-27: many judgment rows feed one synthesis; many synthesis rows feed one specification.  
  _atoms:_ `LED-097`(act), `LED-098`(act)
- a synthesis must show Co-1/Tier-1 divergence and which dimension governs; convergence counts independent roots.  
  _atoms:_ `MIS-06`(act), `PIP-08`(act)

**Direction.** P-X: no synthesis-stage table carries parameter_id; connections hold free-text targets and conflicts are keyed on item_code/pop_a/pop_b (item-layer columns). A determination is one parameter x one lens; the engine takes one cell per run. Cross-parameter synthesis has no place to be recorded.

## C-039 [S1] Questions only the owner can answer that block engine or writer behaviour

**Class** OPEN-QUESTION  ·  **Resolver** OWNER  ·  **Confidence** high

- which band a code value upgraded by confirmation lands in is unruled.  
  _atoms:_ `LED-159`(act)
- the lens set: an owner statement naming three vocabularies, not read as retiring the medical lens; unresolved.  
  _atoms:_ `LED-168`(ope)
- whether a preliminary-status full-read figure may set a published value.  
  _atoms:_ `LED-202`(ope)
- whether the pilot extraction cap carries to the scan contract; owner decisions D4-D13.  
  _atoms:_ `LED-208`(act), `LED-209`(ope)
- OD-7 recommends retiring the decisions YAML register; DR-2026-09-26 OQ-5 re-asks the same question and leaves it open while its section 11 adds a register row on landing.  
  _atoms:_ `OPI-105`(ope), `RC-224`(ope), `RC-238`(act)
- OQ-5 and OQ-8; whether to guard against spurious infrastructure; mining deferral has no ageing or backlog failure condition.  
  _atoms:_ `LED-191`(ope), `SES-041`(ope), `SES-029`(act)

**Direction.** Not conflicts of statements: gaps in what has been ruled. Listed so the engine/writers are not made to guess.

## C-040 [S1] 'Tier and evidence-type assignment' and 'anything touching specifications' are permanently manual -- but the determination is computed and the tier is derived

**Class** RULING-RULING  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-ENG-T3` = **PASS**

- DR-2026-08-19 section 12.5: tier and evidence-type assignment, and anything touching specifications or the reasoning doc, are permanently manual.  
  _atoms:_ `OPI-226`(act), `OPI-229`(act)
- owner 2026-09-09 evening: 'you have to compute it. I can't handle this load manually'; the determination state is computed by assess_cell from tier arithmetic.  
  _atoms:_ `LED-151`(act), `LED-152`(act)

**Direction.** Rule 0 and CLAUDE.md's own worked example: the 2026-09-09 evening ruling superseded section 12.5's clause on contact, with no edit to the DR. OPI-229 is still ACTIVE in the atom set because the DR's text is unmarked; status correction owed (AMENDED, by LED-151). What section 12.5 still governs (the reasoning doc, the Opus floor, the B-before-E gate) is untouched. Tier DERIVATION from (evidence_type, scope) is machine work; evidence_type ASSIGNMENT remains a judgment (OPI-226 survives in that part).

## C-001 [S2] Does the guidebook teach professional judgment?

**Class** RULING-DOC  ·  **Resolver** OWNER  ·  **Confidence** high

- mission-and-epistemics.md: 'The guidebook teaches professional judgment; it does not substitute for it.'  
  _atoms:_ `MIS-02`(act)
- ledger 2026-04-26 19:25: the guidebook 'does not teach professional judgment' and confers no competence.  
  _atoms:_ `LED-024`(act)
- the mission file's header says CANONICAL/locked 2026-04-26 05:29 while its Status section says 'not yet operative'.  
  _atoms:_ `MIS-08`(ope)

**Direction.** The ledger entry is later than the header lock (19:25 vs 05:29) and is an owner statement, so it supersedes the mission sentence on contact (rule 0). The mission text is therefore stale. POS-04 records that the mission file is already owed an edit (adjudicate-vs-dictate).

_Note: Mission text is doctrine; an agent may not edit it without owner sign-off (CLAUDE.md section 8)._

## C-002 [S2] Two markers or three

**Class** RULING-DOC  ·  **Resolver** OWNER  ·  **Confidence** high

- mission file: every specification carries one of two markers, filled or empty.  
  _atoms:_ `MIS-03`(act)
- three markers: filled (confirmed), half (policy/standards only), empty (grey/thin); unmarked is an error.  
  _atoms:_ `LED-015`(ame), `LED-016`(act), `LED-017`(ame), `CLM-038`(act)

**Direction.** Ledger records the two-marker rule as reconciled 2026-07-13 (LED-015 AMENDED). Three markers govern; the mission file is stale.

## C-003 [S2] What a 'stated' cell needs: the T3-alone question

**Class** RULING-DOC  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-ENG-T3` = **PASS**

- mission file: stated = derived from >= Tier 3, Co-1 or Co-2 evidence.  
  _atoms:_ `MIS-04`(act)
- a cell whose only anchor is Tier 3 is not stated; T3-clinical alone is provisional.  
  _atoms:_ `LED-010`(act), `PIP-03`(act)
- tier-system section 8 places T3-clinical in the Full band, which anchors outright.  
  _atoms:_ `EVI-052`(act)
- evidence-methodology and the architecture matrix: T3 supports; T3-clinical alone yields provisional.  
  _atoms:_ `EVI-306`(act), `EVI-325`(act), `EVI-128`(act)

**Direction.** The engine implements LED-010/PIP-03 (T3-clinical alone -> provisional; T3-grey alone -> pending); the probe re-reads that. MIS-04 only survives if '>= Tier 3' is read as tiers 1-3 with T3 needing a second axis. EVI-052 is the outlier.

## C-007 [S2] Cell-state transition table contradicts itself

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-ENG-STATE` = **FAIL**

- transition table: any -> not_applicable.  
  _atoms:_ `EVI-361`(act)
- the same section lists stated -> not_applicable among transitions that do not occur.  
  _atoms:_ `EVI-364`(act)
- methodology 2.6 cites 'section 2.2 condition (3)' for Co-2; after the G7 insertion Co-2 is condition 4 (EVI-322, EVI-323).  
  _atoms:_ `EVI-352`(act)

**Direction.** The engine recomputes state per run and stores no from-state, so the table is not enforced as a transition relation; see machine M05.

## C-008 [S2] Cell key still written (parameter x population) in the methodology

**Class** RULING-DOC  ·  **Resolver** AGENT  ·  **Confidence** high

- evidence-architecture: a cell is parameter_id x at least one lens column.  
  _atoms:_ `EVI-171`(act)
- evidence-methodology 2.1, 2.5, 3.2 still say (parameter x population), with population-specific rationales.  
  _atoms:_ `EVI-314`(act), `EVI-351`(act), `EVI-374`(act)
- architecture reserves 'Tier N' for the evidence ladder and forbids 'Tier 1/Tier 2' as design modes.  
  _atoms:_ `EVI-239`(act), `EVI-235`(act)
- methodology 3.2-4.3 still use 'Tier 1 design range', 'routes to Tier 2', 'applies at Tier 1 only'.  
  _atoms:_ `EVI-388`(act), `EVI-415`(act), `EVI-407`(act)

**Direction.** Owner rulings 2026-08-26 (subject) and 2026-08-28/2026-09-01 (lens) are later than the methodology text; the methodology is stale.

_Note: Pure restatement drift; correcting it changes no doctrine but the methodology is a ratified document, so list it for the owner's merge._

## C-009 [S2] Source-type to tier mapping: national frameworks and standards

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-TIER-DERIVE` = **FAIL**

- methodology 1.5: a source's tier follows from its type; Tier 2 organizational guidelines may carry national_fw.  
  _atoms:_ `EVI-301`(act), `EVI-302`(act)
- section 1.1 table: national_fw is Tier 5; standard_eb spans T2/T4/T5, occasionally T3 (architecture G6).  
  _atoms:_ `EVI-303`(act), `EVI-280`(act)

**Direction.** UNSETTLED in prose. The ratified table schemas/tier_derivation.py keys tier on (evidence_type, scope); the adjudication_integrity check that would compare stored tier to it is QUARANTINED (see C-031).

## C-013 [S2] The tier verdict is a judgment output, but the tier column lives on evidence_sources and is written at admission

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-F` = **FAIL**

- judgment delivers the tier verdict; evidence_sources.tier is to be retired (D-0168).  
  _atoms:_ `LED-108`(act), `DRS-098`(act), `DRS-099`(ope)
- pipeline-operations: admission and tier adjudication are the gate between discovery and extraction, recorded on the source.  
  _atoms:_ `OPS-06`(act)
- D-0179 sets evidence_sources.tier for a source; co1-operational puts tier (int 1-6) on EvidenceSource; D-0178 notes the column carries no CHECK.  
  _atoms:_ `DRS-164`(act), `DRS-249`(act), `DRS-298`(act), `DRS-151`(act)

**Direction.** Ruled but not executed (LED-108 ambiguity: 'the move is queued, not done'). Readers that must be re-pointed first: add-extraction's R3 guard and assess_cell's gather both read evidence_sources.tier.

## C-014 [S2] When does the crossing happen: at judgment, or is applicability a synthesis output?

**Class** RULING-RULING  ·  **Resolver** OWNER  ·  **Confidence** medium

- 08-24 section 2.4 (and the operative instrument): applicability is an output of synthesis; zero links before synthesis is correct; writing applicability edges first is the forbidden presupposition.  
  _atoms:_ `DRS-052`(act), `DRS-053`(act), `DRS-054`(act), `DRS-055`(act), `DRS-056`(act), `ENT-151`(sup), `ENT-152`(act), `OPI-147`(sup)
- owner 2026-08-27 (D-0173) overrules the deferral: the crossing is judgment's output; zero links after judgment is a defect.  
  _atoms:_ `LED-113`(act), `LED-118`(act)
- D-0174, issued the same day, still says 'applicability remains a synthesis judgement'; D-0184 builds on that reservation.  
  _atoms:_ `DRS-117`(act), `DRS-193`(act)
- D-0175/6/7 fix or re-derive item-population link sets for named items before synthesis; functional-taxonomy schedules a serves_axes backfill and a zero-axes gap query.  
  _atoms:_ `DRS-134`(act), `DRS-153`(act), `DRS-157`(act), `DRS-158`(act), `ENT-164`(act), `ENT-183`(act)

**Direction.** LED-113 supersedes the 08-24 deferral on contact. D-0174's residual sentence and D-0184's reliance on it are not reconciled. D-0175-0177 operate on the deleted item layer (see C-019) and are inert.

## C-018 [S2] 'Population' is retired vocabulary; the schema, the methodology and three DRs still use it

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-C` = **NOT-BUILT**

- owner 2026-08-28: 'population' is retired; the lenses are identity, icf, needs, medical. The owner's phrasing was 'i think'; identity was put back for confirmation; the rename was not applied.  
  _atoms:_ `LED-127`(act)
- contract and process rules still require population codes/keys; population-taxonomy retains 'one slug, one population'.  
  _atoms:_ `PIP-15`(act), `PRC-082`(act), `ENT-236`(ame), `ENT-247`(ame), `ENT-222`(sup)
- conceptual-model counts 24 population codes; the population-taxonomy banner says a flat 23.  
  _atoms:_ `ENT-040`(act), `ENT-192`(act)

**Direction.** OPEN QUESTION for the owner: the confirmation LED-127 asks for is not recorded. Until then 'populations' is the identity lens table (CLM-043) and the rename is not applied.

## C-020 [S2] Splinter population link tables: 'both sweeps are done' versus five tables still present

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-A` = **FAIL**

- owner 2026-08-28: no population_* link table may exist; every table attaching a determination to a group takes four lens columns.  
  _atoms:_ `LED-132`(act), `CLM-042`(act)
- CLAUDE.md section 6 states both sweeps are done (and that migration 071 dropped population_code from specifications).  
  _atoms:_ `CLM-042`(act)

**Direction.** Only `specifications` was swept. P-A and P-B measure the tables and columns that were not. Doc overstates; the empty tables are removable without owner sign-off (CLAUDE.md section 8) through a tooling migration (rule 10).

## C-021 [S2] determination_gates attaches to a group through one lens column

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** medium  ·  **Probe** `P-GT` = **FAIL**

- any table attaching a determination to a group has four lens columns.  
  _atoms:_ `LED-128`(act)
- a medical lens always accompanies another lens; no determination is keyed on medical_code alone.  
  _atoms:_ `PIP-04`(act)

**Direction.** P-GT: determination_gates carries identity_code only. Whether PIP-04 is enforced anywhere is not probed; the specifications CHECK is 'at least one' (LED-130), which admits medical alone.

## C-023 [S2] D-0184 (the lens is a column) is an agent decision awaiting owner review but is treated as binding

**Class** PROVENANCE  ·  **Resolver** OWNER  ·  **Confidence** high

- D-0184 is 'ADOPTED, REVIEW PENDING': a session decision the owner has not yet reviewed (AGENT_PROPOSAL).  
  _atoms:_ `DRS-200`(ope)
- D-0182 and D-0188 treat it as in force; D-0182 says crossings 'stop being render machinery'.  
  _atoms:_ `DRS-180`(act), `DRS-181`(act), `DRS-189`(act), `DRS-193`(act), `DRS-237`(act)
- D-0170: lens-switching runs through the crossing maps; D-0188 records that mechanism as superseded but D-0170's own text is unmarked.  
  _atoms:_ `DRS-104`(act)
- the ledger quotes the owner ruling of 2026-08-28/2026-09-01 on which D-0184 is built.  
  _atoms:_ `LED-133`(act), `CLM-042`(act)

**Direction.** The owner rulings underneath (LED-128, LED-130) are recorded and binding; the specific mechanism D-0184 chooses (lens as column, crossing maps as authoring aid) rests on an unreviewed DR. D-0170 should carry a BY back-pointer.

## C-031 [S2] Retire in place requires every reader to filter status first -- some views do not

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** medium  ·  **Probe** `P-H` = **FAIL**

- owner 2026-09-16: retire data rows and identifiers in place via the status the table carries; never hard-delete.  
  _atoms:_ `LED-169`(act), `LED-170`(act), `SES-027`(act)
- precondition: before any retirement, every reader/view that could surface the row must filter on status.  
  _atoms:_ `LED-171`(act)

**Direction.** P-H lists views over base_parameters/specifications/evidence_sources whose SQL names no lifecycle column. On main, base_parameters has no verb that reaches 'merged' or 'retired'; the unreleased T1 branch adds retire-parameter and merge-parameter, so P-H on the T1 tree is the precondition check for that PR. The regex is a lexical test: a view may filter by a different spelling.

## C-036 [S2] Owner statements whose only home is a session record

**Class** UNRECORDED  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-LEDGER-GREP` = **FAIL**

- four 2026-09-18 statements (mine arguments and qualitative work; relevant sources carry qualitative mining; anything relevant to accessibility may be mined; search by slug, adjudicate by category) have no ledger entry of their own.  
  _atoms:_ `SES-022`(act), `SES-023`(act), `SES-024`(act), `SES-025`(act)
- 'fix mechanisms, not hand edit'; sub-national jurisdiction satisfies a bucket; a Buckets 1-2 restatement; and a 2026-09-16 ruling cited without its words.  
  _atoms:_ `SES-032`(act), `SES-045`(act), `SES-047`(act), `SES-027`(act)
- the session reports the owner raised a point but the owner's words are not quoted.  
  _atoms:_ `SES-015`(his), `SES-018`(his), `SES-020`(his)

**Direction.** Rule 0 binds on contact whether or not the ledger records the statement, so these bind. The risk is a search that cannot see them (.ignore hides sessions/): P-LEDGER-GREP asserts that the quoted phrases are absent from references/project-standards.md. Recording each is an append to the owner ledger; whether an agent may append on the owner's behalf is the owner's call.

## C-037 [S2] Process contradictions inside the commands, agents and rules

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** medium

- RC4 fails unless an adversarial pass is closed; /adversarial says passes 1 and 2 are never to be closed; the owner ruled not to chase pass 1 closed.  
  _atoms:_ `PRC-169`(act), `LED-192`(act)
- close-adversarial-pass refuses unless every lens is 'covered'; the closing block allows NOT-ATTACKED rows; 'covered' is undefined; 'eleven' is a hand-written count.  
  _atoms:_ `PRC-156`(act), `PRC-259`(act)
- /orient and /session-open each claim to be the first thing run.  
  _atoms:_ `PRC-184`(act), `PRC-203`(act)
- the scratchpad folder must be named identically to CURRENT, yet it is to be renamed after the PR number exists while CURRENT keeps the DB stem.  
  _atoms:_ `PRC-207`(act), `PRC-214`(act), `PRC-216`(act)
- /batch-done is 'the only definition of finished' but does not list the gate CLAUDE.md section 1 prescribes; a corpus-wide --all reflex is warned against elsewhere.  
  _atoms:_ `PRC-160`(act), `PRC-182`(act)
- invariant I5 leaves MCP-tool searches unwitnessed while R8 requires every search be logged.  
  _atoms:_ `PRC-176`(act)

**Direction.** CLAUDE.md rule 0 does not decide between two process documents; these are for the owner or for the next session that touches the commands.

## C-044 [S2] Order of retiring a column: readers, rebuild, writer (DR-2026-09-26) versus writer, reader, NULL forward (CLAUDE.md rule 5)

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** low

- citation_mining.connections_produced is retired in the order readers, then rebuild, then writer.  
  _atoms:_ `RC-153`(act)
- a column a committed data migration INSERTs can never be dropped: writer-retire, reader-retire, NULL forward.  
  _atoms:_ `LED-079`(act), `CLM-015`(act)

**Direction.** UNSETTLED. [CONFIDENCE: low -- the extractor did not record this pair inside RC-153; read RC-153 and LED-079 together before acting.] They agree if 'retire' means NULL-forward rather than drop, and disagree on the order of writer and readers.

## C-006 [S3] Seven tiers, or T1-T6 plus two tracks

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** high

- tier-system: T1-T6 plus Co-1 and Co-2 tracks; the schema column `tier` is an integer 1-6.  
  _atoms:_ `EVI-002`(act)
- evidence-architecture, evidence-methodology, the process rules and legal-regulatory speak of 'seven tiers'.  
  _atoms:_ `EVI-085`(act), `EVI-269`(act), `PRC-100`(act), `ENT-392`(act)
- tier number is a claim-type, not quality (tier-system) vs 'higher numbers = weaker evidence' (methodology 1.2).  
  _atoms:_ `EVI-003`(act), `EVI-284`(act)
- T2 is described as 'below international standards' though standards are T4, which rank lower.  
  _atoms:_ `EVI-010`(act), `EVI-275`(act)
- the practice (Co-3) encoding sits 'below Co-1/Co-2' yet a firm POE can be placed at T1, which ranks alongside Co-1.  
  _atoms:_ `EVI-076`(ope), `EVI-069`(act), `EVI-070`(act)

**Direction.** Tier definitions are doctrine; no later owner statement decides between the readings.

## C-010 [S3] Stage list in the 2026-08-24 DR is five stages; 'specifications is not a stage'

**Class** RULING-DOC  ·  **Resolver** AGENT  ·  **Confidence** high

- five-stage spine; DRS-038 and LED-087 are already marked SUPERSEDED.  
  _atoms:_ `DRS-038`(sup), `LED-087`(sup)
- 08-24 section 2.2: specifications is a table judgment writes, not a stage -- not marked superseded.  
  _atoms:_ `DRS-039`(act), `DRS-040`(act)
- owner 2026-08-27: seven stages; a table is never a stage; specification is a stage.  
  _atoms:_ `LED-124`(act), `LED-125`(act), `CLM-027`(act), `DRS-124`(act), `DRS-125`(act), `DRS-131`(act)

**Direction.** LED-124 (owner, 2026-08-27) supersedes DRS-039/DRS-040 on contact. Status correction owed on those two atoms: mark SUPERSEDED.

## C-011 [S3] Is `base` a stage, and is it 'substrate'?

**Class** RULING-DOC  ·  **Resolver** NONE  ·  **Confidence** medium

- D-0167: base is stage one; 'substrate' was never owner vocabulary and is reserved for construction elements.  
  _atoms:_ `DRS-126`(act), `DRS-127`(act), `DRS-130`(act), `DRS-132`(act), `LED-123`(act), `LED-124`(act)
- D-0175 is titled 'item_population_links are SUBSTRATE, provisionally'.  
  _atoms:_ `DRS-157`(act)

**Direction.** D-0167 and the owner's 2026-08-27 words (LED-123) are later than D-0175's title only if D-0175 is read as an earlier usage; dates in the DR set make D-0175 later. UNSETTLED which wins; the term is retired in practice and D-0175's subject (the item layer) is gone.

## C-015 [S3] Evidence collection: 'a cursory scan' or a stage that judges relevance

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** medium

- D-0168: the owner defines evidence collection as a cursory scan that lists every concept/topic/phrase; judgment deep-reads.  
  _atoms:_ `DRS-097`(act), `LED-114`(act)
- D-0174: evidence collection judges relevance and must not be treated as a pure log.  
  _atoms:_ `DRS-120`(act), `DRS-116`(act), `DRS-121`(act)
- 2026-10-09 scan contract: every admitted source is scanned for any and all applicable parameters; a multi-term source is harvested across all of them.  
  _atoms:_ `LED-195`(act), `LED-197`(act)

**Direction.** UNSETTLED between D-0168 and D-0174 (same-day DRs). The scan contract (owner, 2026-10-09) is later and asks for more than 'cursory', but it names the verb (scan) rather than the stage; stage placement of the scan is not stated.

## C-016 [S3] Pointer discipline: enforced by schema shape, or not enforced

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** medium

- 08-24 DR: pointer discipline is enforced by schema shape, not by a gate.  
  _atoms:_ `DRS-046`(act), `DRS-037`(act)
- CLAUDE.md rule 5: NOT ENFORCED -- you are the gate.  
  _atoms:_ `CLM-015`(act)
- generated DRs say 'edit the register, not this file' and that C9 catches drift; D-0188 says no generator exists, the header is wrong and C9 only checks each file is cited.  
  _atoms:_ `DRS-064`(act), `DRS-227`(act), `DRS-228`(act)

**Direction.** CLAUDE.md (newer, process rule) is the better statement of enforcement; the DR sentences are stale.

## C-025 [S3] Co-1 operational record: sub-type lists, retired verification values, ref-id format

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-VERIF-VOCAB` = **PASS**

- four Co-1 source types in section 1.1, five co1_source_type values in section 6.1 (adds validated_tool).  
  _atoms:_ `DRS-248`(act), `DRS-294`(act)
- sections 3.4 and 6.3, methodology 2.8 and an old ledger rule still test UNVERIFIED-CLOSED and CLOSED-DELETED; D-0157 made verification_status binary.  
  _atoms:_ `DRS-274`(ame), `DRS-301`(ame), `EVI-365`(ame), `EVI-369`(ame), `LED-028`(act)
- co1-operational prescribes Co1-NN ref ids and puts population_codes and parameters_supported on the Co-1 record; CLAUDE.md requires dbcore.next_ref_id and each stage holds only its own data.  
  _atoms:_ `DRS-293`(act), `DRS-295`(act), `DRS-296`(act)

**Direction.** The schema CHECK on evidence_sources.verification_status admits VERIFIED and UNVERIFIED only; the retired values cannot be written. The co1-operational sections that cite them are stale (DRS-274 and DRS-301 are already marked AMENDED).

## C-026 [S3] jurisdictional_values: reference-only (D-0181) versus restored as research_code_leads (D-0185)

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** medium  ·  **Probe** `P-UNWRITABLE` = **FAIL**

- D-0181 calls jurisdictional_values REFERENCE-ONLY, not to be written.  
  _atoms:_ `DRS-169`(act)
- D-0185 says D-0181 had 'already called these rows research' and restores them as research_code_leads.  
  _atoms:_ `DRS-209`(act), `DRS-218`(act)
- operative instrument: the minimum viable batch lists 1-2 jurisdictional_values backfills, while its own STOP notice (2026-08-22) forbids writing any value into jurisdictional_values.  
  _atoms:_ `OPI-204`(act), `OPI-193`(act), `OPI-190`(sup)
- D-0175 and D-0183 require a rationale_ref on determination edges; the column is nullable and the enforcing check was never built.  
  _atoms:_ `DRS-159`(act), `DRS-162`(ope), `DRS-186`(act)

**Direction.** D-0185 is later. add-jurisdictional-value exists but its table has a NOT NULL FK into the empty items table (P-UNWRITABLE lists it), so the verb cannot write.

## C-030 [S3] How checks are added and what gates a merge

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** medium

- checks are added only through governance/check-registry.yaml; run_checks.py is the sole invoker; deleting code, checks and scripts needs evidence, not permission; git history is the archive.  
  _atoms:_ `CLM-055`(act), `CLM-052`(act)
- process and architecture documents add blocking checks as CI workflow jobs and keep the branch-protection ruleset on.  
  _atoms:_ `PRC-077`(act), `ENT-468`(act), `ENT-499`(act), `ENT-484`(act), `ENT-487`(act), `ENT-520`(act)
- the same process section keeps the ruleset DISABLED during Phase A; PRC-093 does not say whether Phase A ended.  
  _atoms:_ `PRC-091`(act), `PRC-093`(act)
- owner-gated removal of BPC validation; 'archive' a retired script to _archived/.  
  _atoms:_ `PRC-084`(act), `PRC-088`(his)
- the architecture assumes the claude.ai chat surface, a PI bootstrap block and skills/<name>_SKILL.md; CLAUDE.md describes Claude Code, PRs and .claude/skills/.  
  _atoms:_ `ENT-461`(act), `ENT-531`(act), `ENT-503`(act), `ENT-477`(act), `ENT-527`(act)

**Direction.** CLAUDE.md is the current process; the architecture (v2.3) and the 2026-04 process rules are stale on these points. The stale statements are listed so a reader does not obey them.

## C-038 [S3] Hand-written counts and enumerations that disagree with each other or with the schema

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** medium

- '24 countries plus 2 meta', a 24/46/49 jurisdiction structure; the section table has 25 country rows.  
  _atoms:_ `ENT-338`(act), `ENT-360`(act), `ENT-418`(pro), `ENT-402`(act)
- EvidenceType has 7 members in one block and 9 in the audit.  
  _atoms:_ `ENT-036`(act), `ENT-039`(act)
- all 14 languages searched on every run; the research skill obliges 19; jurisdiction scope later limited to Buckets 1-2 (LED-193).  
  _atoms:_ `LED-031`(act)
- adopting CC BY-SA 4.0 is a DG-REVIEW example in one section and licensing is always DG-NON in another.  
  _atoms:_ `ENT-272`(act), `ENT-280`(act)
- model-version pins that the decision protocol says are stripped on touch; effort_level 'numeric only' against an example and a regex that admit 'none'.  
  _atoms:_ `ENT-363`(act), `ENT-311`(act), `ENT-312`(act), `ENT-308`(act), `ENT-290`(act), `ENT-304`(act), `ENT-314`(act)
- standards-registry.md kept as markdown against the owner directive that citation data in .md goes into a table; a differently named tracker.  
  _atoms:_ `ENT-361`(act), `ENT-043`(act), `ENT-410`(act)

**Direction.** CLAUDE.md rule 7a: every figure is a command. These sentences are stale or internally inconsistent; none is an owner statement.

## C-041 [S3] Scope of the operative instrument's supersession and the read-set it prescribes

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** medium

- the instrument supersedes all other planning documents and every document in its supersession table becomes 'binding on nothing'.  
  _atoms:_ `OPI-001`(act), `OPI-002`(act), `OPI-005`(act)
- yet its section B labels some of those files OPERATIVE (the 2026-08-22 master execution plan, the 2026-08-20 A-18 adjudication).  
  _atoms:_ `OPI-007`(act), `OPI-009`(act)
- a fresh session reads exactly four documents, two labelled SPENT or HISTORY ONLY, against section A's two live companions; 'no fifth document'.  
  _atoms:_ `OPI-096`(act), `OPI-099`(act)
- 'no successor to this document may be written' against DR-2026-09-26's 'a decision record, not a plan'; OPI-013 is already marked AMENDED.  
  _atoms:_ `OPI-013`(ame), `OPI-058`(ame), `RC-012`(act)
- the instrument outranks CLAUDE.md; CLAUDE.md adds that a live owner ruling outranks the instrument -- the instrument's text carries no such exception.  
  _atoms:_ `OPI-003`(act)

**Direction.** CLAUDE.md states the precedence chain (owner ruling > DR-2026-08-19 > CLAUDE.md). The instrument's internal OPERATIVE labels and the four-document read set are not reconciled; no later statement decides.

## C-042 [S3] What a research batch's changeset contains, and how it is classified

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** medium

- the changeset is exactly the DB, one data_*.sql, two pointers, the session record and one attestation, nothing else.  
  _atoms:_ `OPI-217`(act)
- commit the scratchpad and agent transcripts at every natural break; tooling and research ship in separate PRs.  
  _atoms:_ `CLM-016`(act), `CLM-022`(act), `RC-189`(act)
- acceptance names checks H03/H04/H05/H07, which DR-2026-09-26 section 2.1 says are deleted, and expects the changeset to classify as data where the RC DR says data migrations classify as schema.  
  _atoms:_ `OPI-215`(act), `OPI-216`(act), `RC-205`(act)

**Direction.** CLAUDE.md rule 6 and DR-2026-09-26 are later than the operative instrument's acceptance text; OPI-217 and OPI-215/216 are stale.

## C-043 [S3] Edit-in-place versus append for corrections to the instrument; migration-number allocator; open decisions

**Class** DOC-DOC  ·  **Resolver** NONE  ·  **Confidence** medium

- 2026-08-22 note edits the instrument in place ('correcting it here is the cheaper repair').  
  _atoms:_ `OPI-057`(act)
- 2026-08-25 callout: rewriting in place destroys the record; append, do not edit.  
  _atoms:_ `OPI-131`(act)
- the 2026-08-17 plan's table is 'the sole allocator' of migration numbers; DR-2026-09-26 assigns the next free number at build time.  
  _atoms:_ `OPI-006`(act), `RC-201`(act)
- 'opens zero new DEFERRED/PENDING markers' against OD-2 to OD-12 left open and OD-11/OD-12 recorded as explicit deferrals; OD-10 is both open and SIGNED.  
  _atoms:_ `OPI-120`(act), `OPI-016`(ope), `OPI-110`(ope)
- DR-2026-07-21 consequence 2 'remains in force' and is 'implemented by' a mechanism stated to be satisfied, spent and retired.  
  _atoms:_ `OPI-063`(his), `OPI-064`(ame)

**Direction.** Later statement wins in each pair (OPI-131 over OPI-057; RC-201 over OPI-006); the open-decisions and consequence-2 pairs are internal inconsistencies with no later statement.

## C-045 [S3] Status of DR-2026-09-26 and of the DOI-stash design in the operative instrument

**Class** PROVENANCE  ·  **Resolver** NONE  ·  **Confidence** medium

- DR-2026-09-26 (v2) is ratified as of 2026-09-27 by owner nod, with PR #159 merged.  
  _atoms:_ `RC-001`(act)
- its section 0 header still reads 'v2, PROPOSED'.  
  _atoms:_ `RC-011`(act)
- it adds an entry to validate_pydantic_schemas' curated MODEL_TABLE_MAP, which CLAUDE.md rule 8 names as an outstanding derive-it violation; it proposes no CHECK on search_executions.engine, while rule 8 says vocabularies come from CHECKs.  
  _atoms:_ `RC-067`(act), `RC-116`(act)
- seed 3 is 'not shipped' in one place, and the recommended answer to OQ-6 refers to it in another.  
  _atoms:_ `RC-142`(sup), `RC-225`(act)

**Direction.** Treated as ratified (owner nod recorded, RC-001). The two apparatus choices (curated map, free-text engine) are knowingly retained and recorded by the DR itself.

## C-046 [S3] Pointers run from a later stage to an earlier one -- some foreign keys run the other way

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-FWD-FK` = **INFO**

- a stage holds only its own data; earlier-stage facts are reached by a pointer on the shared reference id.  
  _atoms:_ `LED-080`(act), `CLM-015`(act)
- a walk re-enters stages: write order and what a stage may hold are separate questions.  
  _atoms:_ `CLM-029`(act)
- a table is never a stage; the stage assignment of a table is a classification the map carries, and the map's own `disputed:` block lists tables it could not place.  
  _atoms:_ `LED-125`(act), `LED-124`(act)

**Direction.** UNSETTLED. P-FWD-FK lists every foreign key whose child sits in an earlier stage than its parent (STATE-GRAPH.md 2a). Research tables pointing at admitted evidence are the re-entrancy CLM-029 licenses; the others (a table in the capture stage pointing at a synthesis-stage citation table, a judgment table pointing at gaps, tables pointing at the emptied `items` table that the map files under render) are either misclassified or genuine upward dependencies. Which, is the owner's classification.

