# Active-conflicts register

_Rendered from `conflicts.yaml` by `build_graph.py`. A conflict here is an adjudicated disagreement between ACTIVE atoms, or between an atom and a measured mechanism; the mechanical detector's candidate pairs are not conflicts until they are written into `conflicts.yaml`. Nothing here is a ruling._

48 entries. Severity: S1 15, S2 18, S3 15. Class: DOC-DOC 15, OPEN-QUESTION 1, PROVENANCE 2, RULING-DOC 9, RULING-MECHANISM 17, RULING-RULING 3, UNRECORDED 1.

## Index

| id | sev | class | resolver | probe -> live verdict | title |
|---|---|---|---|---|---|
| C-004 | S1 | RULING-MECHANISM | OWNER | P-ENG-T3 -> PASS | T3-grey and a lone T6 source may anchor a floor claim (owner directive 2026-07-20) -- the engine returns pending for T3-grey alone |
| C-005 | S1 | RULING-RULING | OWNER | -- | A T4-T6-only basis: never best-practice language, or weak-band best practice 'as currently known' |
| C-012 | S1 | RULING-MECHANISM | OWNER | P-STAGE-SVE -> FAIL | source_value_extractions: judgment-stage table (owner) vs evidence-stage table (map and CLAUDE.md) |
| C-017 | S1 | RULING-MECHANISM | OWNER+AGENT | P-AXIS -> FAIL, P-G -> PASS | 'Axes' is a bad coined term and the axes tables are retired (owner R3, 2026-08-18; again 2026-08-24) -- the tables, columns and codes are live |
| C-019 | S1 | RULING-MECHANISM | OWNER | P-UNWRITABLE -> FAIL | The item layer is deleted from the database (step 1.2) and is still the vocabulary of standing documents and process rules |
| C-022 | S1 | RULING-DOC | OWNER+AGENT | P-MEDICAL -> FAIL | Medical lens: D-0184 reserves the rows to the owner; the owner's 2026-09-11 words say to fill it out |
| C-024 | S1 | RULING-DOC | OWNER | P-CO1-PROV -> PASS | Co-1's warrant: D-0178 (name the co-production) versus co1-operational (published_corpus / participatory_synthesis) |
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
| C-007 | S2 | DOC-DOC | OWNER | P-ENG-STATE -> FAIL | Cell-state transition table contradicts itself |
| C-008 | S2 | RULING-DOC | AGENT | -- | Cell key still written (parameter x population) in the methodology |
| C-009 | S2 | DOC-DOC | OWNER | P-TIER-DERIVE -> FAIL | Source-type to tier mapping: national frameworks and standards |
| C-013 | S2 | RULING-MECHANISM | AGENT | P-F -> FAIL | The tier verdict is a judgment output, but the tier column lives on evidence_sources and is written at admission |
| C-014 | S2 | RULING-RULING | OWNER | -- | When does the crossing happen: at judgment, or is applicability a synthesis output? |
| C-018 | S2 | RULING-MECHANISM | OWNER | P-C -> NOT-BUILT | 'We don't use the word population' -- the schema, the methodology and three DRs still do |
| C-020 | S2 | RULING-MECHANISM | AGENT | P-A -> FAIL | Splinter population link tables: 'both sweeps are done' versus five tables still present |
| C-021 | S2 | RULING-MECHANISM | AGENT | P-GT -> FAIL | determination_gates attaches to a group through one lens column |
| C-023 | S2 | PROVENANCE | OWNER | -- | D-0184 (the lens is a column) is an agent decision awaiting owner review but is treated as binding |
| C-031 | S2 | RULING-MECHANISM | AGENT | P-H -> FAIL | Retire in place requires every reader to filter status first -- some views do not |
| C-036 | S2 | UNRECORDED | OWNER | P-LEDGER-GREP -> FAIL | Owner statements whose only home is a session record |
| C-037 | S2 | DOC-DOC | OWNER | -- | Process contradictions inside the commands, agents and rules |
| C-044 | S2 | DOC-DOC | OWNER | -- | Order of retiring a column: readers, rebuild, writer (DR-2026-09-26) versus writer, reader, NULL forward (CLAUDE.md rule 5) |
| C-047 | S2 | DOC-DOC | AGENT | -- | 'Code-enforced checks trump text rules' versus 'a live owner statement supersedes every prior ratified record' |
| C-048 | S2 | RULING-MECHANISM | AGENT | P-STATUS-WRITERS -> FAIL | A status column's values need a writer -- the probe lists data_capture_status values that none of db.py names |
| C-049 | S2 | RULING-DOC | OWNER | -- | Jurisdiction scope: R5/R6 (2026-08-18) versus 'buckets 1-2 only' (2026-09-28) versus 'all 24 jurisdictions' in the philosophy document |
| C-003 | S3 | DOC-DOC | OWNER | P-ENG-T3 -> PASS | 'Anchors outright' (band) versus 'T3 alone is provisional' (state): one word, two axes |
| C-006 | S3 | DOC-DOC | OWNER | -- | Seven tiers, or T1-T6 plus two tracks |
| C-010 | S3 | RULING-DOC | AGENT | -- | Stage list in the 2026-08-24 DR is five stages; 'specifications is not a stage' |
| C-011 | S3 | RULING-DOC | NONE | -- | Is `base` a stage, and is it 'substrate'? |
| C-015 | S3 | DOC-DOC | OWNER | -- | Evidence collection: 'a cursory scan' or a stage that judges relevance |
| C-016 | S3 | DOC-DOC | AGENT | -- | Pointer discipline: enforced by schema shape, or not enforced |
| C-025 | S3 | DOC-DOC | AGENT | P-VERIF-VOCAB -> PASS, P-CO1-TYPE -> FAIL | Co-1 operational record: sub-type lists, retired verification values, ref-id format |
| C-030 | S3 | DOC-DOC | AGENT | -- | How checks are added and what gates a merge |
| C-038 | S3 | DOC-DOC | AGENT | -- | Hand-written counts and enumerations that disagree with each other or with the schema |
| C-041 | S3 | DOC-DOC | OWNER | -- | Scope of the operative instrument's supersession and the read-set it prescribes |
| C-042 | S3 | DOC-DOC | AGENT | -- | What a research batch's changeset contains, and how it is classified |
| C-043 | S3 | DOC-DOC | NONE | -- | Edit-in-place versus append for corrections to the instrument; migration-number allocator; open decisions |
| C-045 | S3 | PROVENANCE | NONE | -- | Status of DR-2026-09-26 and of the DOI-stash design in the operative instrument |
| C-046 | S3 | RULING-MECHANISM | OWNER | P-FWD-FK -> INFO | Pointers run from a later stage to an earlier one -- some foreign keys run the other way |
| C-050 | S3 | RULING-DOC | NONE | -- | 'Three lenses' (R2, 2026-08-18) -- the lens count is now four, and the registries stay separate |

## Status corrections owed

Atoms whose recorded status is behind a later statement. The atom files record each document's own markers; these are the supersessions the documents themselves do not carry. Applying one means editing the atom's `status` and `superseded_by`; the check then fails until the entry here is removed.

| atom | now | should be | decided by | why |
|---|---|---|---|---|
| LED-029 | ACTIVE | SUPERSEDED | LED-084 | 2026-08-24: every slug is searched against every lens; 'one slug, one population' (2026-03-18) is overtaken. |
| LED-018 | ACTIVE | AMENDED | LED-013, EVI-058 | Option A (2026-07-21) permits a flagged weak-band rendering of a T4-T6-only basis. |
| DRS-039 | ACTIVE | SUPERSEDED | LED-094, LED-124 | owner 2026-08-27: base is a stage (LED-124) and the stage verbs end 'specify syntheses, and render specifications' (LED-094), so specification is a stage; the 2026-08-24 five-stage list that said otherwise is overtaken. |
| DRS-040 | ACTIVE | SUPERSEDED | LED-094, LED-124 | as DRS-039. |
| OPI-229 | ACTIVE | AMENDED | LED-151, LED-152 | owner 2026-09-09 (evening): the determination is computed; section 12.5's 'permanently manual ... specifications' clause is superseded on contact. |
| WRK-003 | ACTIVE | SUPERSEDED | OPI-015, OPI-022 | the owner ratified the operative instrument on 2026-08-19 as OD-1, items-as-leads included (OPI-015); its section 1.4 rule 1 forbids making a slug by stripping an item name (OPI-022), and its supersession table records that R1's strip mechanism is overturned. |
| WRK-033 | ACTIVE | SUPERSEDED | OPI-015, OPI-022 | as WRK-003. |
| WRK-171 | ACTIVE | SUPERSEDED | OPI-015, OPI-022 | as WRK-003 (the handoff's restatement). |
| WRK-172 | ACTIVE | AMENDED | OPI-015, OPI-022 | its first limb (the strip is done manually) is overtaken -- no item name becomes a slug by stripping at all; its second limb (a regex smuggles the bias through) is subsumed by the stronger rule and still stands. |
| WRK-004 | ACTIVE | AMENDED | LED-128, LED-110 | the lens count is four, not three. |
| WRK-173 | ACTIVE | AMENDED | LED-128, LED-110 | the lens count is four, not three. |
| WRK-043 | ACTIVE | SUPERSEDED | LED-091 | owner 2026-08-26 keyed the determination on the canonical parameter; migration 071 re-keyed specifications. |
| WRK-068 | ACTIVE | SUPERSEDED | LED-091 | as WRK-043. |

## C-004 [S1] T3-grey and a lone T6 source may anchor a floor claim (owner directive 2026-07-20) -- the engine returns pending for T3-grey alone

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-ENG-T3` = **PASS**

- DR-2026-07-20 weighted-strength anchor model (owner directive 2026-07-20: 'all evidence tiers can be used to anchor a best practice claim ... T3-grey/T6 weak'): the weak band 'anchors only a floor/convergence claim', rendered with an honesty flag.  
  _atoms:_ `EVI-049`(act), `EVI-055`(act)
- evidence-methodology (ratified 2026-07-13): T3-grey alone and a single T6 source yield pending, i.e. no claim.  
  _atoms:_ `EVI-326`(act), `EVI-338`(act)

**Direction.** The weak band comes from the 2026-07-20 owner directive, which is later than the 2026-07-12 tier3-stated-threshold DR and the 'tier3-threshold DR item 2' that the engine comment cites ('T3-grey-alone does not even reach provisional'), and the methodology text of 2026-07-13. By rule 0 the later directive governs what it touches. Whether it lifts item 2 of the earlier DR for the STATE (the Option A DR keeps the state machine unchanged) or only weights claim strength is not stated, so whether the engine is behind or the directive is band-only is the owner's to say. [CONFIDENCE: medium -- the lone-T6 case is handled by the regulatory branch, which was not re-derived here.]

## C-005 [S1] A T4-T6-only basis: never best-practice language, or weak-band best practice 'as currently known'

**Class** RULING-RULING  ·  **Resolver** OWNER  ·  **Confidence** medium

- 2026-07-13 and tier-system section 3: a basis of T4-T6 only never renders best-practice language in any register; a converged T5/T6 value is never 'best practice'.  
  _atoms:_ `LED-018`(act), `EVI-034`(act), `EVI-035`(act)
- 2026-07-21 Option A: code-consensus-only claims may render at the weak band if flagged; never unflagged or above weak.  
  _atoms:_ `LED-013`(act), `LED-014`(act), `EVI-094`(act), `EVI-241`(act), `POS-03`(act)
- methodology 3.4 offers the bare construction 'Code requires [value] per [standard]' for T4-T6-only cells, against the I3 flag-and-caveat requirement (EVI-229/230/194).  
  _atoms:_ `EVI-394`(act)

**Direction.** Option A (2026-07-21) is the later owner directive, and EVI-058/EVI-229/EVI-230 quote its amended text, which is live. LED-018 (2026-07-13) is not marked amended in the ledger; treat it as amended in part and correct its status. EVI-034/EVI-035 (the unamended tier-system section 3 prohibition) stand only for cells without anchoring evidence. Render-side enforcement is the quarantined register check (see C-028).

## C-012 [S1] source_value_extractions: judgment-stage table (owner) vs evidence-stage table (map and CLAUDE.md)

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-STAGE-SVE` = **FAIL**

- ledger entry headed 'Owner ruling 2026-08-27, adopting item #2 of the architecture note' (the owner's words are the two quoted evidence/judgment descriptions; the table assignment is the ledger author's application, which the owner adopted).  
  _atoms:_ `LED-106`(act)
- pipeline-contract: the hand-off from evidence to judgment is source_value_extractions.ref_id NOT NULL, no UNIQUE -- the fan-out from one source to many judgment rows.  
  _atoms:_ `PIP-10`(act)

**Direction.** governance/stage-map.yaml renders the table at EVIDENCE and records the dispute as open (disputed: block). CLAUDE.md section 3's stage table says evidence holds 'extraction'. LED-106 is the adopted ruling (OWNER_RELAYED); under rule 0 the map and CLAUDE.md are what to correct. The consequence is not cosmetic: add-extraction writes evidence_sources.data_capture_status in the same transaction, a judgment-to-evidence write that the code comment itself calls 'evidence the column is in the wrong home'.

## C-017 [S1] 'Axes' is a bad coined term and the axes tables are retired (owner R3, 2026-08-18; again 2026-08-24) -- the tables, columns and codes are live

**Class** RULING-MECHANISM  ·  **Resolver** OWNER+AGENT  ·  **Confidence** high  ·  **Probe** `P-AXIS` = **FAIL**  ·  **Probe** `P-G` = **PASS**

- owner R3 (2026-08-18, DG-NON, 'standing decisions, do not relitigate'): 'axes' is a bad coined term; use ICF codes directly with their names; `axes` and `item_axis_links` are retired; `population_axis_map` is re-derived mechanically as population-to-ICF.  
  _atoms:_ `WRK-178`(act), `WRK-179`(act), `WRK-180`(act), `WRK-181`(act), `WRK-007`(act), `WRK-031`(act), `WRK-166`(act)
- owner 2026-08-24: 'I don't want axis to be used'; owner 2026-09-13: 'AX-' for ICF should never exist anywhere; work in ICF/access-need codes AND names.  
  _atoms:_ `LED-076`(act), `LED-166`(act), `CLM-039`(act)
- the 2026-08-24 DR: the rename is 'authorized and owed' yet 'NOT DECIDED HERE', to be done as one act and not piecemeal.  
  _atoms:_ `DRS-006`(act), `DRS-023`(ope), `DRS-024`(act)
- D-0170, D-0184, functional-taxonomy and the operative instrument still treat `axes`, `item_axis_links`, `population_axis_map` and AX-* as live objects (the instrument quarantines the axis map under owner directive D-1).  
  _atoms:_ `DRS-114`(act), `DRS-189`(act), `DRS-193`(act), `DRS-199`(ope), `ENT-105`(act), `ENT-156`(act), `ENT-076`(act), `OPI-049`(act)

**Direction.** The owner's rulings are consistent and the earliest is recorded, standing and unqualified (R3, with LED-076 and LED-166 later). The 2026-08-24 DR does not reverse them: it scopes WHEN the rename happens ('not piecemeal'), so the retirement is ruled and unexecuted. LED-166 is carried (P-G); the retirement of the vocabulary is not (P-AXIS lists the tables and columns). [CORRECTION: an earlier draft said the 2026-08-18 ruling could not be found; it is in workplan/2026-08-18-handoff-next-session.md section 2 and the research-frame proposal, which the operative instrument names as the RULING RECORD.]

## C-019 [S1] The item layer is deleted from the database (step 1.2) and is still the vocabulary of standing documents and process rules

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-UNWRITABLE` = **FAIL**

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

## C-024 [S1] Co-1's warrant: D-0178 (name the co-production) versus co1-operational (published_corpus / participatory_synthesis)

**Class** RULING-DOC  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-CO1-PROV` = **PASS**

- D-0178 (owner ruling relayed, 2026-08-31): a Co-1 tier is unwarranted-pending unless co1_provenance names the co-production; published_corpus is not a warrant.  
  _atoms:_ `DRS-146`(act), `DRS-147`(act), `DRS-148`(act), `CLM-037`(act)
- co1-operational (2026-04-29): co1_provenance takes exactly two values and every pre-launch Co-1 citation is published_corpus; grounds Co-1 in peer review, organisational accountability or scholarly authorship.  
  _atoms:_ `DRS-264`(act), `DRS-265`(act), `DRS-251`(act)

**Direction.** D-0178 is later and is the owner's ruling, so by rule 0 the co1-operational vocabulary and its 'every pre-launch Co-1 citation is published_corpus' clause are stale. The data already conforms: P-CO1-PROV finds each Co-1 source carrying prose that names the co-production and none holding only a co1-operational value; the column has no CHECK vocabulary, so nothing enforces it. Correcting co1-operational is a doctrine-document edit, owner-merged.

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

**Direction.** The ledger entry (a ratified RULE block recording the owner's ruling, LED-024) is later than the header lock (19:25 vs 05:29), so by rule 0 it supersedes the mission sentence on contact; the mission text is therefore stale. POS-04 records that the mission file is already owed an edit (adjudicate-vs-dictate).

_Note: Mission text is doctrine; an agent may not edit it without owner sign-off (CLAUDE.md section 8)._

## C-002 [S2] Two markers or three

**Class** RULING-DOC  ·  **Resolver** OWNER  ·  **Confidence** high

- mission file: every specification carries one of two markers, filled or empty.  
  _atoms:_ `MIS-03`(act)
- three markers: filled (confirmed), half (policy/standards only), empty (grey/thin); unmarked is an error.  
  _atoms:_ `LED-015`(ame), `LED-016`(act), `LED-017`(ame), `CLM-038`(act)

**Direction.** Ledger records the two-marker rule as reconciled 2026-07-13 (LED-015 AMENDED). Three markers govern; the mission file is stale.

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
- owner 2026-08-27 (D-0173): 'overrule Aug 24 DR. we go evidence>judgment>synthesis' -- CLAUDE.md section 6 (CLM-040, CLAUDE.md's own prose attributing it to the owner, not the owner's words) states the consequence, that the crossing is judgment's output and zero links after judgment is a defect.  
  _atoms:_ `LED-113`(act), `LED-118`(act), `CLM-040`(act)
- D-0174, issued the same day, still says 'applicability remains a synthesis judgement'; D-0184 builds on that reservation.  
  _atoms:_ `DRS-117`(act), `DRS-193`(act)
- D-0175/6/7 fix or re-derive item-population link sets for named items before synthesis; functional-taxonomy schedules a serves_axes backfill and a zero-axes gap query.  
  _atoms:_ `DRS-134`(act), `DRS-153`(act), `DRS-157`(act), `DRS-158`(act), `ENT-164`(act), `ENT-183`(act)

**Direction.** LED-113 supersedes the 08-24 deferral on contact. D-0174's residual sentence and D-0184's reliance on it are not reconciled. D-0175-0177 operate on the deleted item layer (see C-019) and are inert.

## C-018 [S2] 'We don't use the word population' -- the schema, the methodology and three DRs still do

**Class** RULING-MECHANISM  ·  **Resolver** OWNER  ·  **Confidence** high  ·  **Probe** `P-C` = **NOT-BUILT**

- owner 2026-08-28: "we don't use the word 'population' though" (unqualified); the lenses are identity, icf, needs, medical. Only the choice of 'base_taxonomy' as the replacement carries the owner's 'i think'; identity was put back for confirmation and the rename was not applied.  
  _atoms:_ `LED-127`(act), `ADD-001`(act)
- contract and process rules still require population codes/keys; population-taxonomy retains 'one slug, one population'.  
  _atoms:_ `PIP-15`(act), `PRC-082`(act), `ENT-236`(ame), `ENT-247`(ame), `ENT-222`(sup)
- conceptual-model counts 24 population codes; the population-taxonomy banner says a flat 23.  
  _atoms:_ `ENT-040`(act), `ENT-192`(act)

**Direction.** The retirement of the word is ruled and unqualified (ADD-001), so PIP-15, PRC-082, ENT-236/247/222 and the methodology wording are stale on contact. What is open is the replacement name ('base_taxonomy ... i think') and the confirmation LED-127 asks for, which is not recorded: until then `populations` is the identity lens table (CLM-043) and no rename has been applied (P-C).

## C-020 [S2] Splinter population link tables: 'both sweeps are done' versus five tables still present

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-A` = **FAIL**

- owner 2026-08-28: no population_* link table may exist; every table attaching a determination to a group takes four lens columns.  
  _atoms:_ `LED-132`(act), `CLM-042`(act)
- CLAUDE.md section 6 stated both sweeps were done; step 0.5 removed the claim and left the accurate sentence that migration 071 dropped population_code and item_code from specifications.  
  _atoms:_ `CLM-042`(act)

**Direction.** Only `specifications` was swept. P-A and P-B measure the tables and columns that were not. The doc overstated and no longer does (step 0.5); the empty tables are removable without owner sign-off (CLAUDE.md section 8) through a tooling migration (rule 10), plan step 1.3.

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

**Direction.** Step 0.3 (migration views_filter_retired) made the views over base_parameters filter status, and two source views filter supersession; P-H, now matching the column and not the substring, lists the four evidence_sources views left alone: v_convergence_sources, v_determination_provenance, v_evidence_authors, v_source_admission. Each is held back for a reason in that migration's header (supersede-source's refusal ignores specification_extraction_links; a recorded assessment's participants; ref_id lookups read by a blocking test). LED-171 says every READER, and P-H reads views only: non-view readers (audit_evidence_metadata, metadata_integrity_audit, research_batch_dod R2/R4/R13, get_unmined, validate_parameters) still surface a tombstone or a retired parameter. Open: GAP-062 (a data row, not amended here).

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
- the adversarial closing block carries a hand-written count of lenses ('eleven'); close-adversarial-pass itself defines coverage as a finding row for every lens in the column's CHECK (M08.t3), so the count is the only drift.  
  _atoms:_ `PRC-259`(act)
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

## C-047 [S2] 'Code-enforced checks trump text rules' versus 'a live owner statement supersedes every prior ratified record'

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** medium

- architecture v2.3 (2026-04-30): code-enforced checks (hooks, CI) trump text rules for the matching invariant.  
  _atoms:_ `ENT-465`(act)
- CLAUDE.md rule 0: a live owner statement supersedes every prior ratified record it touches, on contact; record the supersession, never weigh the ruling against the paperwork.  
  _atoms:_ `CLM-000`(act), `CLM-001`(act)

**Direction.** Both are agent-maintained process texts (rule 0 cites an owner ruling as its proof, not as its source), so this is recency, not rank: rule 0 governs as the later, process-level statement: a check that encodes a superseded invariant is what to change, not obey. ENT-465 remains a fair description of what to do when no ruling intervenes and is stale as a precedence rule.

## C-048 [S2] A status column's values need a writer -- the probe lists data_capture_status values that none of db.py names

**Class** RULING-MECHANISM  ·  **Resolver** AGENT  ·  **Confidence** medium  ·  **Probe** `P-STATUS-WRITERS` = **FAIL**

- when the CLI cannot reach a column, add the verb and do not claim the write; a table the CLI cannot reach is a coverage bug to fix.  
  _atoms:_ `LED-182`(act), `CLM-031`(act)
- any status column ships with its biconditional check or it does not ship (C06 covers the 'captured' value).  
  _atoms:_ `OPS-04`(act)

**Direction.** P-STATUS-WRITERS (lexical) lists the non-default values the column's CHECK accepts that no db.py line names beside the column. Those values are reachable only by hand SQL, so 'looked, nothing extractable' cannot be recorded, an absence the project treats as evidence (R7, R14). A Layer 1 gap: file it as a GAP and add the verb in a tooling PR (rule 10), not in a batch's data migration.

## C-049 [S2] Jurisdiction scope: R5/R6 (2026-08-18) versus 'buckets 1-2 only' (2026-09-28) versus 'all 24 jurisdictions' in the philosophy document

**Class** RULING-DOC  ·  **Resolver** OWNER  ·  **Confidence** high

- owner R5 (2026-08-18), as relayed by the handoff: five prioritised buckets; the jurisdiction-scope question is settled at the 48-scope, not the 27-code enum; R5 is only a fill order.  
  _atoms:_ `WRK-186`(act), `WRK-187`(act), `WRK-188`(act), `WRK-189`(act), `WRK-193`(act)
- owner R6 (2026-08-18): 'no longer need global South to move from provisional'; the PROVISIONAL gate no longer waits for the Global South.  
  _atoms:_ `WRK-084`(act), `WRK-195`(act)
- the handoff author's own derivation of R6: only the first conjunct of section 2.3 falls, the Co-1 >=9-language floor stays, replacement wording pinned at 'buckets 1-3', and a disclosure clause -- the handoff marks the bucket 4/5 split and the disclosure clause as authored proposals, not the owner's words.  
  _atoms:_ `WRK-196`(act), `WRK-199`(act), `WRK-200`(act), `WRK-201`(act), `WRK-204`(act)
- owner 2026-09-28: research scope is bucket 1 and bucket 2 only until both are categorically exhausted for the slug.  
  _atoms:_ `LED-193`(act), `SES-047`(act)
- the operative instrument lists the R5 fill order and the R6 amendment as owner decision OD-2, still open.  
  _atoms:_ `OPI-100`(ope)
- governance/jurisdiction-philosophy.md section 2.3 still reads 'PROVISIONAL until all 24 jurisdictions are recorded' -- the amendment R6 requires has not been made.  
  _atoms:_ `ENT-338`(act)

**Direction.** Later owner statements narrow rather than contradict: R6 (2026-08-18) releases the Global South requirement; LED-193 (2026-09-28) narrows research to buckets 1-2 first. Whether the owner's release equals the author's buckets 4-5 split, and whether the 9-language floor survives, are the author's derivations and are not owner-confirmed. The document is stale on contact (rule 0) but it is doctrine (jurisdiction), so the repair is the owner's, and the R6 amendment still needs its decision record (OPI-100 open). The 'all 24' figure and the '48-scope' are also two different counts (C-038).

## C-003 [S3] 'Anchors outright' (band) versus 'T3 alone is provisional' (state): one word, two axes

**Class** DOC-DOC  ·  **Resolver** OWNER  ·  **Confidence** medium  ·  **Probe** `P-ENG-T3` = **PASS**

- tier-system section 8 (owner directive 2026-07-20, DR-2026-07-20 weighted-strength anchor model): T3-clinical sits in the Full band, which 'anchors a best-practice claim outright'.  
  _atoms:_ `EVI-052`(act)
- T3 alone is not enough for `stated`: T3-clinical alone is provisional (tier3-stated-threshold DR, 2026-07-12; methodology 2.2; contract).  
  _atoms:_ `LED-010`(act), `PIP-03`(act), `EVI-306`(act), `EVI-325`(act), `EVI-128`(act)
- the mission file's rule: stated = derived from >= Tier 3, Co-1 or Co-2 evidence.  
  _atoms:_ `MIS-04`(act)

**Direction.** Not a contradiction once band and state are separated: the 2026-07-20 directive weights the STRENGTH of a claim (the marker band), and the Option A DR (2026-07-21, line 'State machine unchanged') leaves the state machine alone, so T3-clinical alone is marked at full strength and held at `provisional`. The engine implements exactly that (P-ENG-T3 requires the documented comment and the assignment that immediately follows it; a reworded comment would turn it red without the logic having changed). 'Anchors' is overloaded across the two axes in EVI-052 and in MIS-04, which reads as if tier alone decided `stated`. A wording repair, not a ruling.

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

**Class** DOC-DOC  ·  **Resolver** AGENT  ·  **Confidence** high  ·  **Probe** `P-VERIF-VOCAB` = **PASS**  ·  **Probe** `P-CO1-TYPE` = **FAIL**

- four Co-1 source types in section 1.1, five co1_source_type values in section 6.1 (adds validated_tool).  
  _atoms:_ `DRS-248`(act), `DRS-294`(act)
- sections 3.4 and 6.3, methodology 2.8 and an old ledger rule still test UNVERIFIED-CLOSED and CLOSED-DELETED; D-0157 made verification_status binary.  
  _atoms:_ `DRS-274`(ame), `DRS-301`(ame), `EVI-365`(ame), `EVI-369`(ame), `LED-028`(act)
- co1-operational prescribes Co1-NN ref ids and puts population_codes and parameters_supported on the Co-1 record; CLAUDE.md requires dbcore.next_ref_id and each stage holds only its own data.  
  _atoms:_ `DRS-293`(act), `DRS-295`(act), `DRS-296`(act)

**Direction.** The schema CHECK on evidence_sources.verification_status admits VERIFIED and UNVERIFIED only; the retired values cannot be written. P-CO1-TYPE compares the live co1_source_type values with schemas.enums.Co1SourceType, a drift independent of the warrant question (C-024). The co1-operational sections that cite them are stale (DRS-274 and DRS-301 are already marked AMENDED).

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

## C-050 [S3] 'Three lenses' (R2, 2026-08-18) -- the lens count is now four, and the registries stay separate

**Class** RULING-DOC  ·  **Resolver** NONE  ·  **Confidence** medium

- R2: three lenses (disability populations, ICF functional demands, access needs), three theoretical approaches, three tables.  
  _atoms:_ `WRK-004`(act), `WRK-173`(act), `WRK-174`(act)
- owner 2026-08-27/28: identity, icf, needs and medical are the lenses; 'because i said we need the medical model too'.  
  _atoms:_ `LED-110`(act), `LED-128`(act)
- the lens registries stay separate and are never reconciled (the four taxonomies keep parallel base_taxonomy_* names).  
  _atoms:_ `WRK-016`(act), `WRK-177`(act), `LED-121`(act)
- an owner statement naming three vocabularies on 2026-09-13 is not read as retiring the medical lens; unresolved.  
  _atoms:_ `LED-168`(ope)

**Direction.** Not a contradiction of the 'separate and never reconciled' limb, which survives. The count in R2 is superseded by the later four-lens rulings; LED-168 stays open until the owner confirms.

