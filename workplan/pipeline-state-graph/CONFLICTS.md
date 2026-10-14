# Active-conflicts register

_Rendered from `conflicts.yaml` by `build_graph.py`. A conflict here is an adjudicated disagreement between ACTIVE atoms, or between an atom and a measured mechanism; the mechanical detector's candidate pairs are not conflicts until they are written into `conflicts.yaml`. Nothing here is a ruling._

26 entries. Severity: S1 9, S2 5, S3 12. Class: DOC-DOC 8, OPEN-QUESTION 1, PROVENANCE 1, RULING-DOC 4, RULING-MECHANISM 12.

## Index

| id | sev | class | resolver | probe -> live verdict | title |
|---|---|---|---|---|---|
| C-004 | S1 | RULING-MECHANISM | OWNER | P-ENG-T3 -> PASS | T3-grey and a lone T6 source may anchor a floor claim (owner directive 2026-07-20) -- the engine returns pending for T3-grey alone |
| C-017 | S1 | RULING-MECHANISM | OWNER | P-AXIS -> PASS, P-G -> PASS | 'Axes' is retired and its tables, column and check are dropped (step 1.4); the one-act sweep is partial and the documents still use the word |
| C-019 | S1 | RULING-MECHANISM | OWNER | P-UNWRITABLE -> PASS | The item layer is deleted from the database (step 1.2) and is still the vocabulary of standing documents and process rules |
| C-022 | S1 | RULING-DOC | OWNER+AGENT | P-MEDICAL -> FAIL | Medical lens: D-0184 reserves the rows to the owner; the owner's 2026-09-11 words say to fill it out |
| C-028 | S1 | RULING-MECHANISM | OWNER+AGENT | P-QUARANTINE -> FAIL | Register invariants have no live gate (tier-consistency has one since step 1.6) |
| C-032 | S1 | RULING-MECHANISM | OWNER+AGENT | P-V2 -> PASS | Scan contract (any source, all parameters, whatever slug) versus a writer that binds an extraction to the admitting slug |
| C-034 | S1 | RULING-MECHANISM | AGENT | P-O -> FAIL | The vocabulary can grow only by add-term from an observation; several base tables have no sanctioned writer |
| C-035 | S1 | RULING-MECHANISM | OWNER+AGENT | P-X -> FAIL | Synthesis across parameters: ruled cardinalities and mission test versus no structure that relates two parameters |
| C-039 | S1 | OPEN-QUESTION | OWNER | -- | Questions only the owner can answer that block engine or writer behaviour |
| C-013 | S2 | RULING-MECHANISM | AGENT | P-F -> FAIL | The tier verdict is a judgment output, but the tier column lives on evidence_sources and is written at admission |
| C-018 | S2 | RULING-MECHANISM | OWNER | P-C -> NOT-BUILT | 'We don't use the word population' -- the schema, the methodology and three DRs still do |
| C-021 | S2 | RULING-MECHANISM | AGENT | P-GT -> FAIL | determination_gates attaches to a group through one lens column |
| C-031 | S2 | RULING-MECHANISM | AGENT | P-H -> FAIL | Retire in place requires every reader to filter status first -- some views do not |
| C-044 | S2 | DOC-DOC | OWNER | -- | Order of retiring a column: readers, rebuild, writer (DR-2026-09-26) versus writer, reader, NULL forward (CLAUDE.md rule 5) |
| C-011 | S3 | RULING-DOC | NONE | -- | Is `base` a stage, and is it 'substrate'? |
| C-015 | S3 | DOC-DOC | OWNER | -- | Evidence collection: 'a cursory scan' or a stage that judges relevance |
| C-016 | S3 | DOC-DOC | AGENT | -- | Pointer discipline: enforced by schema shape, or not enforced |
| C-030 | S3 | DOC-DOC | AGENT | -- | How checks are added and what gates a merge |
| C-038 | S3 | DOC-DOC | AGENT | -- | Hand-written counts and enumerations that disagree with each other or with the schema |
| C-041 | S3 | DOC-DOC | OWNER | -- | Scope of the operative instrument's supersession and the read-set it prescribes |
| C-042 | S3 | DOC-DOC | AGENT | -- | What a research batch's changeset contains, and how it is classified |
| C-043 | S3 | DOC-DOC | NONE | -- | Edit-in-place versus append for corrections to the instrument; migration-number allocator; open decisions |
| C-045 | S3 | PROVENANCE | NONE | -- | Status of DR-2026-09-26 and of the DOI-stash design in the operative instrument |
| C-046 | S3 | RULING-MECHANISM | OWNER | P-FWD-FK -> INFO | Pointers run from a later stage to an earlier one -- some foreign keys run the other way |
| C-049 | S3 | RULING-DOC | OWNER | -- | Jurisdiction scope: the instrument still records the R5 fill order and the R6 amendment as an open owner decision (OD-2) |
| C-050 | S3 | RULING-DOC | NONE | -- | An owner statement of 2026-09-13 names three vocabularies; the four-lens rulings stand until the owner confirms |

## C-004 [S1] T3-grey and a lone T6 source may anchor a floor claim (owner directive 2026-07-20) -- the engine returns pending for T3-grey alone

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-ENG-T3` = **PASS**

- DR-2026-07-20 weighted-strength anchor model (owner directive 2026-07-20: 'all evidence tiers can be used to anchor a best practice claim ... T3-grey/T6 weak'): the weak band 'anchors only a floor/convergence claim', rendered with an honesty flag.  
  _atoms:_ `EVI-049`(act), `EVI-055`(act)
- evidence-methodology (ratified 2026-07-13): T3-grey alone and a single T6 source yield pending, i.e. no claim.  
  _atoms:_ `EVI-326`(act), `EVI-338`(act)

**Direction.** The weak band comes from the 2026-07-20 owner directive, which is later than the 2026-07-12 tier3-stated-threshold DR and the 'tier3-threshold DR item 2' that the engine comment cites ('T3-grey-alone does not even reach provisional'), and the methodology text of 2026-07-13. By rule 0 the later directive governs what it touches. Whether it lifts item 2 of the earlier DR for the STATE (the Option A DR keeps the state machine unchanged) or only weights claim strength is not stated, so whether the engine is behind or the directive is band-only is the owner's to say. [CONFIDENCE: medium -- the lone-T6 case is handled by the regulatory branch, which was not re-derived here.]

## C-017 [S1] 'Axes' is retired and its tables, column and check are dropped (step 1.4); the one-act sweep is partial and the documents still use the word

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-AXIS` = **PASS**  ·  **Probe** `P-G` = **PASS**

- owner R3 (2026-08-18, DG-NON, 'standing decisions, do not relitigate'): 'axes' is a bad coined term; use ICF codes directly with their names; `axes` and `item_axis_links` are retired; `population_axis_map` is re-derived mechanically as population-to-ICF.  
  _atoms:_ `WRK-178`(act), `WRK-179`(act), `WRK-180`(act), `WRK-181`(act), `WRK-007`(act), `WRK-031`(act), `WRK-166`(act)
- owner 2026-08-24: 'I don't want axis to be used'; owner 2026-09-13: 'AX-' for ICF should never exist anywhere; work in ICF/access-need codes AND names.  
  _atoms:_ `LED-076`(act), `LED-166`(act), `CLM-039`(act)
- the 2026-08-24 DR: the rename is 'authorized and owed' yet 'NOT DECIDED HERE', to be done as one act and not piecemeal.  
  _atoms:_ `DRS-006`(sup), `DRS-023`(sup), `DRS-024`(act)
- D-0170, D-0184, functional-taxonomy and the operative instrument still treat `axes`, `item_axis_links`, `population_axis_map` and AX-* as live objects (the instrument quarantines the axis map under owner directive D-1).  
  _atoms:_ `DRS-114`(act), `DRS-189`(act), `DRS-193`(act), `DRS-199`(sup), `ENT-105`(sup), `ENT-156`(ame), `ENT-076`(act), `OPI-049`(sup)

**Direction.** Mechanism executed by step 1.4 (migration drop_axes; validate_axes and its criterion deleted). Open: DRS-024 says the retirement is one act, never piecemeal, and R35 leaves the documents (D-0170, D-0184, functional-taxonomy, the operative instrument) and the AX- strings in references/ to an owner merge and step 1.6(c); the atoms that treated axes as live are marked SUPERSEDED, but their documents still say it.

## C-019 [S1] The item layer is deleted from the database (step 1.2) and is still the vocabulary of standing documents and process rules

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-UNWRITABLE` = **PASS**

- owner R1 (2026-08-18): item codes bias research at this stage; the items rows are archived, not deleted (the instrument later suspends the archival, OD-12, and CLAUDE.md says the rows are gone from the database).  
  _atoms:_ `WRK-169`(act), `WRK-170`(act)
- the item layer is emptied (P-UNWRITABLE lists what still points into it) and items is a Part-4 render rollup derived from specifications; never file into an [A-Z]-NN container.  
  _atoms:_ `CLM-048`(act), `LED-091`(act)
- conceptual-model and functional-taxonomy: items.item_code is the Part-4 organizing unit; specification values attach to items.  
  _atoms:_ `ENT-023`(act), `ENT-148`(act), `ENT-172`(act), `ENT-002`(act), `ENT-003`(act), `ENT-029`(act)
- process rules and the operative instrument cross-reference item-layer cells (F-07, A-16, A-18, AUT).  
  _atoms:_ `PRC-027`(act), `PRC-059`(act), `PRC-068`(act), `OPI-047`(ope), `OPI-048`(ame), `OPI-050`(act)

**Direction.** Mechanism half executed: migration drop_item_layer_cluster dropped the tables, and the renderers that selected item_code went with step 1.1. Documents half OPEN: the rulings of 2026-08-26 and 2026-09-01 supersede the item-keyed sentences on contact, but RULINGS R36 assigns the edit of the taxonomy documents to an owner merge and no plan step makes it.

## C-022 [S1] Medical lens: D-0184 reserves the rows to the owner; the owner's 2026-09-11 words say to fill it out

**Class** RULING-DOC  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-MEDICAL` = **FAIL**

- D-0184 (2026-09-01, an agent decision awaiting owner review, C-023): populating base_taxonomy_medical is 'the owner's alone' (DG-NON).  
  _atoms:_ `DRS-194`(act)
- owner, 2026-09-11 (quoted): 'Fable 5.1 to adjudicate and resolve all items that are presented to me ... Ensure that medical gets filled out.'  
  _atoms:_ `LED-154`(act), `DRS-229`(act), `DRS-231`(act)
- D-0188's own text limits the delegation to the 'enumerated items and no further' -- which may be narrower than the owner's 'all items that are presented to me', depending on what was presented.  
  _atoms:_ `DRS-232`(act), `DRS-233`(act)

**Direction.** Rule 0: the owner's words of 2026-09-11 outrank D-0184's reservation to the extent of those words ('all items that are presented to me'; 'ensure that medical gets filled out'). D-0188's 'enumerated items and no further' is the agent's text and may be narrower than the owner's; whether that narrowing is intended is the owner's to confirm. Mechanism: add-extraction refuses a lens code whose registry table is empty; P-MEDICAL shows the medical registry empty although its writer (add-medical) exists. The instruction has not been executed.

## C-028 [S1] Register invariants have no live gate (tier-consistency has one since step 1.6)

**Class** RULING-MECHANISM  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-QUARANTINE` = **FAIL**

- every rendering carries the identical tuple across registers; every rendered figure carries its strength flag; unmarked is an error.  
  _atoms:_ `PIP-06`(act), `POS-03`(act), `LED-019`(act)

**Direction.** The check that enforced these (register_integrity_check) read a frozen document keyed on item codes and could never agree with the DB again, so step 1.6 deleted it (RULINGS R4); adjudication_integrity (tier derivation) was promoted to blocking in the same step. Nothing live gates the weak-band rendering rule until step 3.R builds a render surface keyed on parameter_id x lens for a check to read.

## C-032 [S1] Scan contract (any source, all parameters, whatever slug) versus a writer that binds an extraction to the admitting slug

**Class** RULING-MECHANISM  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-V2` = **PASS**

- owner 2026-10-09: every admitted source is scanned for any and all applicable parameters; slugs guide searches only and do not limit what is mined.  
  _atoms:_ `LED-195`(act), `LED-196`(act), `LED-197`(act), `LED-199`(act)
- a figure from a source filed under another slug may be extracted and set a published value, tagged for follow-up.  
  _atoms:_ `LED-201`(act), `SES-057`(act)
- the earlier 2026-09-18 statements ('anything relevant to accessibility may be mined', 'search by slug, adjudicate by all slugs in a category') are not restated; 'category' is never defined.  
  _atoms:_ `SES-024`(act), `SES-025`(act)

**Direction.** P-V: the (source x parameter) read-state ledger does not exist on main (built in the unmerged T1 branch). P-V2: add-extraction refuses a ref that source_slug_links does not hold for the named slug; its comment argues ref-slug coherence is the stronger invariant, the opposite of LED-196. The ruling is not carried until T1 merges and the guard is reconciled.

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

## C-013 [S2] The tier verdict is a judgment output, but the tier column lives on evidence_sources and is written at admission

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-F` = **FAIL**

- judgment delivers the tier verdict; evidence_sources.tier is to be retired (D-0168).  
  _atoms:_ `LED-108`(act), `DRS-098`(act), `DRS-099`(ope)
- pipeline-operations: admission and tier adjudication are the gate between discovery and extraction, recorded on the source.  
  _atoms:_ `OPS-06`(act)
- D-0179 sets evidence_sources.tier for a source; D-0178 notes the column carries no CHECK.  
  _atoms:_ `DRS-164`(act), `DRS-249`(act), `DRS-151`(act)

**Direction.** Ruled but not executed (LED-108 ambiguity: 'the move is queued, not done'). Readers that must be re-pointed first: add-extraction's R3 guard and assess_cell's gather both read evidence_sources.tier.

## C-018 [S2] 'We don't use the word population' -- the schema, the methodology and three DRs still do

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-C` = **NOT-BUILT**

- owner 2026-08-28: "we don't use the word 'population' though" (unqualified); the lenses are identity, icf, needs, medical. The replacement name was put back for confirmation; RULINGS R49 (c) records it.  
  _atoms:_ `LED-127`(act), `ADD-001`(act)
- contract and process rules still require population codes/keys; population-taxonomy retains 'one slug, one population'.  
  _atoms:_ `PRC-082`(act), `ENT-236`(ame), `ENT-222`(sup)

**Direction.** The retirement of the word is ruled and unqualified (ADD-001), so PRC-082, ENT-236/222 and the methodology wording are stale on contact. Migration 112 renamed the identity registry and its ICF map (base_taxonomy_identity, identity_icf_map; plan Phase 3 base). What stays open is the word in other names: evidence_population_match and its two columns await the owner's choice of name (LED-127 names served_group and study_group), and seven columns and the verb and flag names still carry it, which is why P-C stays NOT-BUILT.

## C-021 [S2] determination_gates attaches to a group through one lens column

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** medium  ·  **Probe** `P-GT` = **FAIL**

- any table attaching a determination to a group has four lens columns.  
  _atoms:_ `LED-128`(act)
- a medical lens always accompanies another lens; no determination is keyed on medical_code alone.  
  _atoms:_ `PIP-04`(act)

**Direction.** P-GT: determination_gates carries identity_code only. Whether PIP-04 is enforced anywhere is not probed; the specifications CHECK is 'at least one' (LED-130), which admits medical alone.

## C-031 [S2] Retire in place requires every reader to filter status first -- some views do not

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** medium  ·  **Probe** `P-H` = **FAIL**

- owner 2026-09-16: retire data rows and identifiers in place via the status the table carries; never hard-delete.  
  _atoms:_ `LED-169`(act), `LED-170`(act), `SES-027`(act)
- precondition: before any retirement, every reader/view that could surface the row must filter on status.  
  _atoms:_ `LED-171`(act)

**Direction.** Step 0.3 (migration views_filter_retired) made the views over base_parameters filter status, and two source views filter supersession; P-H, now matching the column and not the substring, lists the four evidence_sources views left alone: v_convergence_sources, v_determination_provenance, v_evidence_authors, v_source_admission. Each is held back for a reason in that migration's header (supersede-source's refusal ignores specification_extraction_links; a recorded assessment's participants; ref_id lookups read by a blocking test). LED-171 says every READER, and P-H reads views only: non-view readers (audit_evidence_metadata, metadata_integrity_audit, research_batch_dod R2/R4/R13, get_unmined, validate_parameters) still surface a tombstone or a retired parameter. Open: GAP-062 (a data row, not amended here).

## C-044 [S2] Order of retiring a column: readers, rebuild, writer (DR-2026-09-26) versus writer, reader, NULL forward (CLAUDE.md rule 5)

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** low

- citation_mining.connections_produced is retired in the order readers, then rebuild, then writer.  
  _atoms:_ `RC-153`(act)
- a column a committed data migration INSERTs can never be dropped: writer-retire, reader-retire, NULL forward.  
  _atoms:_ `LED-079`(act), `CLM-015`(act)

**Direction.** UNSETTLED. [CONFIDENCE: low -- the extractor did not record this pair inside RC-153; read RC-153 and LED-079 together before acting.] They agree if 'retire' means NULL-forward rather than drop, and disagree on the order of writer and readers.

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
  _atoms:_ `ENT-338`(act), `ENT-418`(pro), `ENT-402`(act)
- all 14 languages searched on every run; the research skill obliges 19; jurisdiction scope later limited to Buckets 1-2 (LED-193).  
  _atoms:_ `LED-031`(act)
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
- it proposes no CHECK on search_executions.engine, while rule 8 says vocabularies come from CHECKs.  
  _atoms:_ `RC-116`(act)
- seed 3 is 'not shipped' in one place, and the recommended answer to OQ-6 refers to it in another.  
  _atoms:_ `RC-142`(sup), `RC-225`(act)

**Direction.** Treated as ratified (owner nod recorded, RC-001). The apparatus choice (free-text engine) is knowingly retained and recorded by the DR itself; the curated map it also added went with step 1.10.

## C-046 [S3] Pointers run from a later stage to an earlier one -- some foreign keys run the other way

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-FWD-FK` = **INFO**

- a stage holds only its own data; earlier-stage facts are reached by a pointer on the shared reference id.  
  _atoms:_ `LED-080`(act), `CLM-015`(act)
- a walk re-enters stages: write order and what a stage may hold are separate questions.  
  _atoms:_ `CLM-029`(act)
- a table is never a stage; the stage assignment of a table is a classification the map carries, and the map's own `disputed:` block lists tables it could not place.  
  _atoms:_ `LED-125`(act), `LED-124`(act)

**Direction.** UNSETTLED. P-FWD-FK lists every foreign key whose child sits in an earlier stage than its parent (STATE-GRAPH.md 2a). Research tables pointing at admitted evidence are the re-entrancy CLM-029 licenses; the others (a table in the capture stage pointing at a synthesis-stage citation table, a judgment table pointing at gaps, tables pointing at the emptied `items` table that the map files under render) are either misclassified or genuine upward dependencies. Which, is the owner's classification.

## C-049 [S3] Jurisdiction scope: the instrument still records the R5 fill order and the R6 amendment as an open owner decision (OD-2)

**Class** RULING-DOC  ·  **Resolver** OWNER  ·  **Confidence** high

- owner R6 (2026-08-18): 'no longer need global South to move from provisional'; the PROVISIONAL gate no longer waits for the Global South.  
  _atoms:_ `WRK-084`(act), `WRK-195`(act)
- owner 2026-09-28: research scope is bucket 1 and bucket 2 only until both are categorically exhausted for the slug.  
  _atoms:_ `LED-193`(act), `SES-047`(act)
- the operative instrument lists the R5 fill order and the R6 amendment as owner decision OD-2, still open.  
  _atoms:_ `OPI-100`(ope)

**Direction.** Step 2.2b made the section 2.3 amendment (the 'all 24 jurisdictions' conjunct deleted, the Co-1 language floor kept, RULINGS R12). The instrument's OD-2 line is unmarked and the instrument is append-only (OPI-131); the owner confirms the amendment or closes OD-2.

## C-050 [S3] An owner statement of 2026-09-13 names three vocabularies; the four-lens rulings stand until the owner confirms

**Class** RULING-DOC  ·  **Resolver** NONE  ·  **Confidence** medium

- owner 2026-08-27/28: identity, icf, needs and medical are the lenses; 'because i said we need the medical model too'.  
  _atoms:_ `LED-110`(act), `LED-128`(act)
- an owner statement naming three vocabularies on 2026-09-13 is not read as retiring the medical lens; unresolved.  
  _atoms:_ `LED-168`(ope)

**Direction.** RULINGS R39 (b): four lenses stand; the owner is asked to confirm. The R2 count of three is marked AMENDED where it is written (the 2026-08-18 proposal and handoff).

