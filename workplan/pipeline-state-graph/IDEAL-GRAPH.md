# Ideal pipeline graph: the least structure that meets the project's conditions

**Status:** PROPOSED design, not a ruling. Adjudications in §2 are made on the owner's instruction of 2026-10-12 and are open to override. · **Date:** 2026-10-12 · **Reader:** the owner, then an antagonist.
**Basis:** this folder's instrument (atoms, `conflicts.yaml`, `capabilities.yaml`, `STATE-GRAPH.md` generated 2026-10-12 01:08 from `eda7de43`); the live database read-only (schema version: `python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma user_version').fetchone()[0])"`, 101 on 2026-10-12); the T1 branch's migrations 102–105 (local worktree `/home/user/guidebook-t1`, branch `claude/t1-scan-contract-tooling`, not on `main`). Every figure is the output of the command beside it, run 2026-10-12 from the repository root; re-run rather than trust it (CLAUDE.md rule 7a). Atom ids resolve with `grep '^<ID>' workplan/pipeline-state-graph/ATOMS.tsv`. Commands containing a pipe sit in code blocks under their tables (`[c…]`), because a pipe inside a Markdown table does not survive copying. Database queries use one read-only helper:

```
q() { python3 -c "import sqlite3,sys;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(sys.argv[1]).fetchall())" "$1"; }
```

**Owner instructions this answers** (2026-10-12, relayed verbatim by the coordinating session; none is in the ledger yet, see A30):
O1 "create an idealized new state graph that has as little infrastructure and code as possible that still meets all conditions required of project for a walkable pipeline all directions that can dynamically scrape mine organize and sort all relevant information from any source for any parameter regardless of search slug" · O2 "ideal state graph just be code architecture compliant" (read as "must") · O3 "wherever there is a conflict, adjudicate to ensure 100% accuracy, code compliance and logic for ensuring walkability in pipeline as well as dynamic information collection" · O4 "ensure that you strive to minimize amount of code so that it is as distilled and clean as possible as well as deduplicating and reconciling all conflicts" · O5 "centralized where possible and rely on pointers and injectable code" · O6 "the less hard coded, the better" · O7 "we need to ensure handshakes both top-down and bottom-up, and we need to ensure walkability across all tables with references and ids" · O8 "handshake ALL directions".

---

## 1. CONDITIONS

A condition is a requirement an active ruling, the mission, a governance contract or one of the four owner capabilities imposes. Every object in §3 cites the conditions it serves; an object with none is not in the ideal.

- **K01** Read every admitted source against the whole parameter catalogue, whatever slug it was filed under; one source yields many judgment rows, so no `UNIQUE(ref_id)` on the capture table. LED-195, LED-196, LED-197, LED-199, LED-100, LED-101, PIP-10.
- **K02** Keep a per-(source × parameter) record of what was read and what was found, including "read in full, nothing found"; absence is evidence. `capabilities.yaml:24-29`; LED-163; RES-14; `mission-and-epistemics.md:120`.
- **K03** Mine arguments, qualitative findings and harm, not only figures. SES-022, SES-023 (session record only, C-036); RES-07; LED-163.
- **K04** A figure from a source filed under another slug may set a published value and is tagged for follow-up; a skimmed figure never sets one. LED-201, SES-057, SES-061.
- **K05** Harvest each concept phrase a source uses, verbatim and unjudged, one row per sighting; judgment adjudicates; divergent adjudications stand as a contest. LED-114, LED-115, LED-197, CLM-040, RES-11; STATE-GRAPH.md M03.t2.
- **K06** Grow the catalogue: a name is minted from an observed phrase or, for prepopulation only, from the owner-selected catalogues, screened and owner-approved; the warrant is recorded; a broader/narrower relation is a pointer. LED-198, LED-116, LED-203, LED-204, LED-205, LED-200, SES-054, LED-062.
- **K07** No container states its own answer: no digit, comparator or min/max word in a name; no `[A-Z]-NN` item container. LED-148, LED-149, PIP-16, CLM-048, WRK-169.
- **K08** Retire in place through the status a table carries; never hard-delete; a term judged not-a-parameter is declined with its reason; readers filter status. LED-169, LED-170, LED-171, RES-16.
- **K09** The determination key is `parameter_id` from a constrained vocabulary × at least one of four lens columns; never medical alone. LED-091, LED-092, LED-128, LED-130, EVI-171, PIP-04.
- **K10** Four lenses (identity, ICF, needs, medical) in separate registries, never reconciled; real ICF codes; no "axis" or `AX-` vocabulary; medical from ICD-11, never from recollection; identity↔ICF map re-derived. LED-110, LED-121, WRK-177, LED-167, LED-076, LED-166, LED-156, LED-157, WRK-181.
- **K11** Search every slug against every lens; read coverage off logged searches. LED-084, RES-04, SES-046.
- **K12** Log every query verbatim with its prior; keep empties and deferrals; a zero-yield search names its cause; searches through MCP tools are witnessed too. RES-08, RES-06, RES-14, PRC-176.
- **K13** Research buckets 1–2 jurisdictions only until both are exhausted for the slug. LED-193, LED-194, `references/project-standards.md:4295-4309`.
- **K14** Slugs guide searches only; a slug is not a stage and never limits what is derived. LED-196, LED-125.
- **K15** Mine T1–T2 anchors backward and forward; "mined" means executed; a deferral is legitimate if it eventually runs. RES-02, LED-030, LED-179, LED-180, PIP-19.
- **K16** Re-retrieve every locator before admission (no re-retrieval, no admission); never leave `verification_status` NULL; a publisher block is not terminal; never send the owner's email to third-party APIs. RES-10, CLM-044, LED-027, LED-187.
- **K17** Bibliographic fields come from the retrieved payload, never memory; verification leaves an artefact; a candidate is checked against its payload bytes. CLM-036, LED-117, PIP-19.
- **K18** No duplicate-DOI admission; no new DOI column; identifiers are never reissued; `ref_id` comes from `next_ref_id`. RES-09, LED-074, PIP-17, CLM-032.
- **K19** Tiers T1–T6 with Co-1 and Co-2 tracks; the tier verdict is judgment's; tier is derived from (evidence_type, scope); assigning evidence_type is a judgment. EVI-002, LED-108, OPI-226 (in part, C-040), `schemas/tier_derivation.py:1-24`.
- **K20** Co-1's warrant is co-production, named in `co1_provenance`; co-authors are kept. CLM-037, DRS-146, LED-021, LED-022.
- **K21** Grade each admission's population-of-study against population-served per lens; a dissenting grade is a second row. RES-13, LED-186, `CLAUDE.md:295-296`.
- **K22** A relative figure carries its relation as a row; a derived figure's band is floor(mean band ordinal); findings plus a threshold reach a determination as a proxy, never `stated`. PIP-09, LED-161, LED-162, LED-172, LED-173, LED-174, SES-009.
- **K23** Convergence counts independent roots, never documents; grey literature restating a code is not an independent root. PIP-08, LED-164.
- **K24** Many judgment rows feed one synthesis; many syntheses feed one specification. LED-097, LED-098.
- **K25** A synthesis shows Co-1/T1 divergence and which dimension governs; a finding that depends on two or more parameters, or two lenses in conflict, has a recorded place and a trace. MIS-06, LED-037, LED-050, `capabilities.yaml:56-61`.
- **K26** Best-practice synthesis prose is authored only at the Opus/Fable floor. LED-061, CLM-041, PIP-22.
- **K27** The state (stated / provisional / pending / not_applicable) is computed by the engine and emitted as SQL; a pending cell carries a gap. LED-151, LED-152, LED-153, `mission-and-epistemics.md:111-118`.
- **K28** Tier arithmetic: T3 alone → provisional; code-floor or regulatory-stratum-only → never stated, weak band, flagged; stated/provisional need governing inputs; a code value confirmed by research is upgraded. LED-010, PIP-03, PIP-02, LED-013, LED-014, PIP-01, LED-159, LED-160.
- **K29** Every rendered figure carries one marker (●◐○), its strength flag and evidence trail, identical across registers and weighting profiles; unmarked is an error. LED-019, CLM-038, POS-03, PIP-06, LED-057.
- **K30** Every notation the governing set states is carried. LED-176.
- **K31** Render reads the database and does not rely on built artefacts; citations are looked up by `ref_id`; render's hand-off is not a table. LED-103, LED-104, LED-105, LED-081.
- **K32** A figure is for thought, not a requirement; questions are first-class data. POS-02, LED-001, LED-002, `mission-and-epistemics.md:72`.
- **K33** The database is written only through migrations, append-only; the committed DB reproduces from history; only `migrate_db.py` opens it read-write. CLM-012, CLM-013, OPI-124, PIP-18, LED-153.
- **K34** One home per fact; a stage holds only its own data; downstream rows carry a reference id and a grouping key; no parity checks. CLM-015, LED-077, LED-080, LED-075, LED-078.
- **K35** Vocabularies, writable sets and counts are derived, never curated; where judgment is required the writer records judge and warrant. CLM-018, CLM-019, CLM-032.
- **K36** Seven stages; a table is never a stage; walks re-enter stages. CLM-027, LED-124, LED-125, CLM-029.
- **K37** Walkable in all directions; every canonical concept traceable to the sources that used it. `references/project-standards.md:4381` ("pipeline all directions"), LED-116, O1, O7, O8.
- **K38** Dynamic: any source, any parameter, no pre-existing container; the crossing is defined after evidence. LED-199, LED-085 (AMENDED), O1.
- **K39** An adversarial pass records survived as well as sustained claims. LED-070, LED-067, LED-068.
- **K40** Architecture: five layers, the spine, the write path, one check registry, research and tooling shipped apart. LED-140, LED-142, `CLAUDE.md:229-240`, `:284-287`, `:510`, CLM-022, PIP-14, O2.
- **K41** Minimal, deduplicated, conflicts reconciled. O3, O4, CLM-052, CLM-054.
- **K42** Centralized, pointer-based, injectable code. O5, CLM-015.
- **K43** Nothing hard-coded that can be derived or injected. O6, CLM-018, CLM-019.
- **K44** Handshakes in every direction; every table with an id or reference walkable to and from the spine. O7, O8.

**UNSOURCED, excluded from the design**
- U1 A category list for "organize and sort" (O1): D7 is unanswered (LED-209). Only the broader-term pointer (LED-062) is built; sorting is a query.
- U2 An extraction cap or review unit for the scan contract: left to the owner (LED-208, LED-209). Nothing below depends on it.
- U3 Setting-keyed (building/room) determinations: LED-120 rules `base_building`'s shape if it is built; no condition requires it now. `setting` stays free text on an extraction.
- U4 Unattended crawling: no ruling asks for acquisition without an agent. The agent is the scraper; code persists and refuses (§7).

---

## 2. ADJUDICATED

Tests, one each: **(a)** accuracy (traceable, not contradicted by the live repo); **(b)** compliance (CLAUDE.md, architecture); **(c)** walkability (§5 does not break); **(d)** dynamic collection (no slug or container gate). Tie-breaks in order: **T1** later live owner statement; **T2** specific over general; **T3** less code and one home. Recorded as made on O3/O4 of 2026-10-12; the owner may override any row. Doctrine questions and owner-reserved questions are in §12, not here.

| # | conflict | governing side: what the ideal does | (a) | (b) | (c) | (d) | by |
|---|---|---|---|---|---|---|---|
| A01 | C-027 render | LED-103/104: one renderer reads `v_render`; nothing generated is committed; `parts/`, `site/`, `tools/*.html`, `regenerate_derived.sh` go; contract `render-freshness` and `CLAUDE.md:458` are edited | ADD-002 has no primary record (C-027) | sweep (rule 4); contract edit by owner merge | `v_render.specification_id` walks up | — | T1 |
| A02 | C-029 scheduled DB writes | delete `resolve-dois.yml`, `verify-urls.yml`, `resolve_dois.py`, `verify_urls.py`; DOI resolution happens at admission through `fetch` | `pipeline_runs.total_resolved` is 0 in all 5 runs [cA02] | restores rule 3, PIP-18, OPI-124 | — | retrieval in `add-source` | (a)(b) |
| A03 | C-035 cross-parameter synthesis vs workplan v2 §4 "do not build" | build, by generalising: `syntheses` + `synthesis_inputs` replace eight synthesis tables and `determination_gates`; cross-parameter = inputs over more than one `parameter_id` (derived) | LED-097/098; capability C3 | fewer tables than today | gives judgment↔synthesis its first FK | no container | T3 (the workplan is a proposal) |
| A04 | C-032 extraction bound to the admitting slug | LED-196: extractions carry no slug; slug is a label on searches, candidates and scans | P-V2 FAIL | removes a guard | unaffected | ungated | T1 |
| A05 | C-033 slug × lens coverage | four nullable lens FKs on `search_executions`; `v_coverage` | P-M FAIL; `terms_used` is free text | FK, not a parser | coverage walkable | — | T3 |
| A06 | C-034 base writers | verbs for registries research grows (terms, parameters, ICF, medical, crossings, slugs); migration only for doctrine registries (identity, needs, jurisdictions, tier ladder) | LED-182; LED-154 (medical delegated) | `CLAUDE.md:501` doctrine list | — | catalogue grows by verb | T2 |
| A07 | C-012 stage of extractions | judgment (LED-106); `stage-map.yaml` and `CLAUDE.md:253` corrected | LED-106 adopted | CLAUDE.md is "what to correct" (`CLAUDE.md:5`) | scans and extractions share a stage | — | T1 |
| A08 | C-013, C-040 tier storage | `evidence_type`, `scope`, `co1_provenance` move to `source_grades` (judgment); tier and band derived through `tier_ladder`; nothing stores a tier | LED-108, LED-151; `derive_tier` at `schemas/tier_derivation.py:83` | rule 8 | `v_source_tier` | — | T1, T3 |
| A09 | C-015 where the scan sits | cursory listing (`observe-term`) at evidence; deep read (`scans`, extractions) at judgment | LED-114 names both acts | — | — | scan contract unchanged | T2 (owner words over D-0168/D-0174) |
| A10 | C-014 when the crossing happens | lens columns on each extraction, written at judgment; a CHECK makes a lens-less extraction unwritable | LED-113, LED-118 | CHECK, not a gate | lens lateral walk | — | T1 |
| A11 | C-017 axes | `axes`, `access_need_axis_map`, `population_axis_map`, `situations`, `slugs.serves_axes` go in one migration | R3 (WRK-178..181), LED-076, DRS-024 | — | — | — | T1 |
| A12 | C-018, C-050, LED-168 lens names and count | four lenses; registries `base_taxonomy_{identity,icf,needs,medical}` keyed `identity_code`/`icf_code`/`needs_code`/`medical_code`; `evidence_population_match` → `lens_matches` | LED-110, LED-121 (owner's naming), LED-127, LED-154 (medical, specific) | one rename act with its sweep | lens column = registry key name | — | T1, T2 [CONFIDENCE: medium — "base_taxonomy" carries the owner's "i think" (C-018)] |
| A13 | C-019, C-026 item layer | deleted: every item-keyed table, `add-item`, `add-jurisdictional-value`, item audits | WRK-169, LED-091, P-UNWRITABLE | — | removes 0-row dead ends | no container | T1 |
| A14 | C-020, C-021 splinter tables; one-lens gate | splinter tables deleted; `determination_gates` becomes `syntheses(kind='determination-gate')`, whose inputs carry the lens | LED-132, LED-128 | — | gate walks to its cell | — | T1, T3 |
| A15 | C-022, C-023 medical lens | registry and `add-lens-code` exist; rows are research content under the 2026-09-11 delegation; the lens-as-column rests on LED-128/130, not D-0184 | LED-154 later than D-0184 | — | — | — | T1 |
| A16 | C-024, C-025 Co-1 | D-0178: a CHECK on `source_grades` (non-empty, not a co1-operational value); `co1_source_type` dropped, which also ends the enum drift P-CO1-TYPE reports | DRS-146; P-CO1-PROV PASS | CHECK, not a gate | — | — | T1, T3 |
| A17 | C-028, C-005 register invariants, weak band | structural: one `marker` column computed by the engine; CHECKs (regulatory-stratum ⇒ ○ and never stated); every register reads `v_render`; `register_integrity_check` deleted | `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md:44-50` | CHECK + one view | render walks up | — | T1 (Option A later than LED-018) |
| A18 | C-031 readers filter status | every view in §3 filters lifecycle | LED-171 | — | — | — | (a) |
| A19 | C-046 forward FKs | kept only on the many side of an N:1 handshake (`search_candidates.resolved_ref_id`) or as a re-entry record (`search_executions.mined_ref_id`, `.synthesis_id`); every other forward FK leaves with its table | 14 today (STATE-GRAPH.md §2a) | CLM-029 | re-entry explicit | gap-driven search needs no slug | (c) |
| A20 | C-044 order of retiring a column | rule 5 order for every column; RC-153's order bound only `citation_mining.connections_produced`, which leaves with its table | LED-079, RC-153 | — | — | — | T2 |
| A21 | C-048 `data_capture_status` | derived by `v_scan_ledger`; column retired by A26 | 23 data migrations insert it [cA21] | LED-079 | — | — | T3 |
| A22 | C-007 `not_applicable` | value and its rationale CHECK stay; no producer is built; predicate C4.4 stays failing by design | P-ENG-STATE | — | — | — | T3 (no ruling decides) |
| A23 | LED-202 preliminary full-read figure | may set a value; its `extraction_status` shows in the trail; only a skim scan is barred from governing | LED-201 names skim only | — | — | — | T2, T3 [CONFIDENCE: medium — the owner left D1c open] |
| A24 | Pydantic mirrors (`CLAUDE.md:307`, `:460`; v2.3:86) vs one home | table mirrors generated from the live schema; hand mirrors, `MODEL_TABLE_MAP` and `validate_pydantic_schemas` go; modules with logic stay | a generated mirror cannot drift | it still mirrors | — | — | T1 (O4) |
| A25 | one `gaps` table for tooling defects and evidence gaps | evidence gaps become `syntheses(kind='gap')`, reached from the pending cell; `gaps` stays for tooling defects only (infrastructure) | 9 of 76 rows are category EG; the rest are other codes [cA25] | rule 10 still files a GAP | pending → gap → search | gap-driven search | (c), T3 |
| A26 | dead columns vs one home | under pruning, a column a committed data migration INSERTs is writer-retired, reader-retired and NULLed by a compensating data migration: no value remains, so the fact has one home | LED-079 | rule 3 | — | — | T2 |
| A27 | four crossing maps | one typed `lens_crossings` (four lens FKs, CHECK ≥ 2) | LED-128 pattern; LED-133 (an aid, not a render path) | — | lens↔lens walk | — | T3 |
| A28 | architecture v2.3 vs CLAUDE.md | CLAUDE.md and the five-layer ruling (§11 R18) | LED-140/142 later than v2.3 | C-030, C-047 | — | — | T1 |
| A29 | `navigation-modes.md:60-64` item-keyed routes vs LED-091 | routes keyed parameter × lens; D-NAV-006..012 ethics rules (`:314-320`) kept as renderer constraints | LED-091 | — | lens switching | — | T1 |
| A30 | C-036, and O1–O8 not in the ledger | append each verbatim to `references/project-standards.md` with its session, as the 2026-10-09 entry did | precedent `project-standards.md:4371-4373` | rule 0 | — | — | (a) |
| A31 | bucket membership "derived from the one citation, never re-typed" (`project-standards.md:4306`) vs LED-073 | `jurisdictions.bucket` holds membership once; the workplan lines become its citation; `log-search` refuses an out-of-bucket jurisdiction until `v_coverage` shows buckets 1–2 covered for the slug | LED-073 is owner-quoted; the "never re-typed" line is the ledger author's | rule 8 | — | gates a search, not admission | T1 |
| A32 | K04 "another slug" undefined | the tag is derived: `v_follow_up` lists preliminary extractions read under a slug the source was not admitted under; it clears when the extraction is reviewed; T1's `extraction_follow_ups` and `raise-follow-up` are not needed | LED-201 | rule 8 | lateral | never gates | T3 [ASSUMPTION: the reader's slug is the comparison] |
| A33 | LED-188 `results_admitted` raise-only | derived: count of ADMITTED candidates of the search; ADMITTED is terminal, so it only rises | LED-188 | rule 5 | — | — | T3 |
| A34 | `citation_mining` rows with no execution | "mined" = an execution exists; 11 of 33 rows have one [cA34]; the rest re-enter the K15 backlog | LED-179, PIP-19 | — | — | — | T1 |
| A35 | `source_slug_links` | derived from candidates → searches; 51 of 65 derivable [cA35]; the other 14 become `kind='locator'` PROMOTED rows in the compensating migration | (a) | — | — | — | T3 |
| A36 | `case_studies`, `economics_entries` (RES-12 names them) | a case study or cost figure is an `evidence_sources` row plus extractions against a parameter | 0 and 1 rows (STATE-GRAPH.md §4) | research-contract edit by owner merge | walks as any extraction | no container | T3 [CONFIDENCE: medium — I did not read the economics volume] |
| A37 | T1 extras (SES-063) | target shape only: `term_catalogue_origins` → three `terms` columns; `extraction_follow_ups` → `v_follow_up`; declination revocation → `base_parameters.status`. The owner's accept-or-strike on the T1 pull request stands. | 1:1 tables are columns | — | — | — | T3 |
| A38 | C-003, C-008, C-010, C-011, C-016, C-030, C-038, C-041, C-042, C-043, C-045, C-047 | `conflicts.yaml`'s stated direction (the later statement); text edits only; no object here changes | `conflicts.yaml` | — | — | — | T1 |
| A39 | C-037 process commands | outside the graph | — | — | — | — | [NULL: no ideal object depends on them] |

```
# [cA02] 
q 'select run_id, total_resolved from pipeline_runs'
# [cA21]
grep -l 'INSERT INTO "evidence_sources"' scripts/migrations/data_*.sql | xargs grep -l data_capture_status | wc -l
# [cA25]
q 'select category, status, count(*) from gaps group by 1, 2'
# [cA34]
q 'select count(*), sum(exists(select 1 from search_executions e where e.mined_ref_id = m.global_ref_id)) from citation_mining m'
# [cA35]
q 'select count(*), sum(exists(select 1 from search_admissions a join search_executions e on e.exec_id = a.exec_id where a.ref_id = l.ref_id and e.slug = l.slug)) from source_slug_links l'
```

---

## 3. THE IDEAL GRAPH

Thirty-three tables, five views, twenty-eight verbs, twelve gates (counted by command in §9). The DDL below is executable SQLite; §9 gives the command that extracts and loads it. Columns not shown on a table that exists today are retired: NULL-forward where a committed data migration inserts them (A26), dropped by a table rebuild otherwise. CHECK vocabularies are the live ones (`dbcore.check_values`); the only new values are those an adjudication introduces: `base_parameters.status` `declined` (A37), `search_candidates.kind` and `syntheses.kind` (named for the tables merged, A03, A14, A25), and `author_class` (`opus`/`fable` from LED-061, plus `engine` for the engine's own rows).

Gates by stage (all in the registry, §9): evidence `artefact_integrity`; judgment `judgment_handoff_shape`, `research_dod_session`; specification `determination_reproducible`; the whole graph `walkability`, `migration_reproducibility`, `schema_reference_audit`; Layer 0 the remaining five. Everything else a stage needs is a CHECK, an FK or a refusal in its writer.

### 3.1 Centralized homes (O5)

| kind of thing | single home | duplicates it replaces (command, 2026-10-12) |
|---|---|---|
| vocabulary | the column's CHECK or FK target, read by `dbcore.check_values` | 42 enum classes in `schemas/enums.py` [c8b]; 22 of 55 `choices=` not derived [c8a] |
| stage of a table | ids: `pipeline-contract.yaml` `stages:`; table→stage: `governance/stage-map.yaml` (judged, named) | per-tool judgments the stage-map moved out of `tools/pipeline_walk.py` (stage-map.yaml:3-10) |
| check inventory | `governance/check-registry.yaml`; `run_checks.py` | — |
| write path | `db.py` verb → `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py` | scheduled workflow writes (A02) |
| retrieval entry point | `retrieval_log.fetch` / `record_file` | 3 files doing HTTP [c3.1a] |
| bytes | files under `retrieval-log/` + one `retrievals` row each | manifest as sole home; `file_anchor` (18 of 101 extractions); `search_execution_artefacts`; `url_verification_runs`; `pipeline_runs`; URL/DOI-resolution columns |
| a refusal | the `db.py` verb that writes the table, helpers in `dbcore` | audits that re-check what a writer can refuse (`medical_lens_integrity`, `jurisdiction_db_vocabulary`, `adjudication_integrity`, T1's `observation_verbatim_audit`, `extraction_follow_up_audit`) |
| a walk | `dbcore.walk` (§4.1) | 2,635 lines across four walkers [c3.1b] |
| tier and band | `tier_ladder` rows | `TIER_MAP` in code, `evidence_sources.tier`, `adjudication_integrity` |
| DB path, repo root, clock | `dbcore.connect`, `dbcore.REPO_ROOT`, `dbcore.now` | 69 files resolving `GUIDEBOOK_DB_PATH`, 58 `REPO_ROOT` definitions, 18 `datetime.now` calls ([c8i], [c8j]) |

```
# [c3.1a]
grep -rlE 'urllib\.request|requests\.(get|post)|"curl"' scripts tools --include=*.py | wc -l
# [c3.1b]
wc -l tools/pipeline_walk.py tools/schema_walkability.py scripts/audit/graph/*.py scripts/audit/graph_audit.py | tail -1
```

### 3.2 Injection points (O5)

Each entry point binds a default once and passes it down; library code reads no globals.

| collaborator | passed as | bound by | default |
|---|---|---|---|
| database | `conn`, first argument of every verb function, `walk`, gate `check(conn)`, `determine(conn, …)`, `render(conn, …)` | each script's `main()` | `dbcore.connect(path=None)`: the only reader of `GUIDEBOOK_DB_PATH` |
| vocabulary | not passed: derived from `conn` (CHECK, FK) | — | the schema |
| retrieval | `fetch(url, session, *, log_root, get)`; `get` is the HTTP call | caller; a test passes a fake `get` | `retrieval_log` `main()` binds `log_root` (today bound at import, `retrieval_log.py:143-144`) |
| clock | `now` parameter on stamping writers | caller; tests pin it | `dbcore.now` |
| session | `session` argument | CLI `--session` | none: required |
| stages | `stages` mapping and spine order | `run_checks.py`, CLI `main()` | loaded once from stage-map and contract |

Not fewer lines, so left: `migrate_db.py` (already injectable by env, `migrate_db.py:42-44`); gate scripts keep a three-line `main()` because `run_checks.py` runs them as processes (§12 Q4). Hooks under `.claude/hooks/` are invoked by the harness with fixed arguments and cannot be injected.

### 3.3 base

```sql
-- stage: base
CREATE TABLE terms (term_id TEXT PRIMARY KEY, canonical_en TEXT NOT NULL UNIQUE, definition TEXT, scope_note TEXT,
  broader_term_id TEXT REFERENCES terms(term_id),
  catalogue TEXT, catalogue_entry TEXT, approval_ref TEXT,
  CHECK ((catalogue IS NULL) = (catalogue_entry IS NULL) AND (catalogue IS NULL) = (approval_ref IS NULL)));
CREATE TABLE term_aliases (term_id TEXT NOT NULL REFERENCES terms(term_id), alias TEXT NOT NULL, language TEXT NOT NULL, alias_type TEXT);
CREATE TABLE base_parameters (parameter_id INTEGER PRIMARY KEY, term_id TEXT NOT NULL UNIQUE REFERENCES terms(term_id),
  status TEXT NOT NULL CHECK (status IN ('active','declined','merged','retired')),
  status_reason TEXT CHECK (status = 'active' OR length(trim(status_reason)) > 0),
  merged_into INTEGER REFERENCES base_parameters(parameter_id),
  accessibility_direction TEXT CHECK (accessibility_direction IN ('contested','higher_is_better','lower_is_better')),
  direction_rationale TEXT, question TEXT, CHECK ((status = 'merged') = (merged_into IS NOT NULL)));
CREATE TABLE base_taxonomy_identity (identity_code TEXT PRIMARY KEY, display_name TEXT NOT NULL,
  parent_code TEXT REFERENCES base_taxonomy_identity(identity_code), status TEXT);
CREATE TABLE base_taxonomy_icf (icf_code TEXT PRIMARY KEY, component TEXT NOT NULL, title TEXT, title_source TEXT);
CREATE TABLE base_taxonomy_needs (needs_code TEXT PRIMARY KEY, family TEXT NOT NULL, design_obligation TEXT NOT NULL);
CREATE TABLE base_taxonomy_medical (medical_code TEXT PRIMARY KEY, display_name TEXT NOT NULL, status TEXT NOT NULL,
  icd11_anchors TEXT, icd11_verified_at TEXT);
CREATE TABLE lens_crossings (crossing_id INTEGER PRIMARY KEY,
  identity_code TEXT REFERENCES base_taxonomy_identity(identity_code), icf_code TEXT REFERENCES base_taxonomy_icf(icf_code),
  needs_code TEXT REFERENCES base_taxonomy_needs(needs_code), medical_code TEXT REFERENCES base_taxonomy_medical(medical_code),
  warrant TEXT NOT NULL,
  CHECK ((identity_code IS NOT NULL) + (icf_code IS NOT NULL) + (needs_code IS NOT NULL) + (medical_code IS NOT NULL) >= 2));
CREATE TABLE jurisdictions (jurisdiction TEXT PRIMARY KEY, bucket INTEGER);
CREATE TABLE slugs (slug TEXT PRIMARY KEY, status TEXT NOT NULL CHECK (status IN ('ACTIVE','MERGED','PROVISIONAL','STUB')),
  merged_into TEXT REFERENCES slugs(slug));
CREATE TABLE tier_ladder (evidence_type TEXT NOT NULL, scope TEXT NOT NULL, tier INTEGER NOT NULL CHECK (tier BETWEEN 1 AND 6),
  band TEXT NOT NULL CHECK (band IN ('●','◐','○')), PRIMARY KEY (evidence_type, scope));
```

Serves: `terms` K05 K06 K07 · `term_aliases` K11 K12 (frozen legacy search guidance; no writer) · `base_parameters` K06 K08 K09 K22 K32 · four registries K09 K10 · `lens_crossings` K10 K11 · `jurisdictions` K13 K35 · `slugs` K11 K14 · `tier_ladder` K19 K28 K29.

Writers: `add-term` (exactly one warrant: `--from-observation` writes the NAMES-NEW adjudication in the same act; `--from-catalogue` needs catalogue, entry and the owner's approval reference; refuses a digit, comparator or min/max word and an existing name) · `add-parameter` (from a term; `--status declined` needs a reason; refuses a value-bearing name) · `amend-parameter` (status with reason; direction; a `question` carrying a digit is refused, K07) · `add-lens-code` (ICF and medical only; an ICD-11 anchor needs a persisted WHO payload, LED-157) · `add-lens-crossing` · `add-slug`. Identity, needs, jurisdiction and ladder rows: migration only (doctrine, `CLAUDE.md:501`).

| `base_parameters.status` | to | via | guard |
|---|---|---|---|
| (none) | active, declined | `add-parameter` | term exists; name screen; declined needs a reason |
| active | merged, retired | `amend-parameter` | reason; merged needs `merged_into`; readers filter status (LED-171) |
| declined | active | `amend-parameter` | reason (revocation) |
| merged, retired | — | — | terminal; retire in place |

### 3.4 research

```sql
-- stage: research
CREATE TABLE search_executions (exec_id INTEGER PRIMARY KEY,
  slug TEXT REFERENCES slugs(slug), synthesis_id INTEGER REFERENCES syntheses(synthesis_id),
  mined_ref_id TEXT REFERENCES evidence_sources(ref_id),
  mining_direction TEXT CHECK (mining_direction IN ('backward','both','forward')),
  identity_code TEXT REFERENCES base_taxonomy_identity(identity_code), icf_code TEXT REFERENCES base_taxonomy_icf(icf_code),
  needs_code TEXT REFERENCES base_taxonomy_needs(needs_code), medical_code TEXT REFERENCES base_taxonomy_medical(medical_code),
  jurisdiction TEXT REFERENCES jurisdictions(jurisdiction), language TEXT NOT NULL,
  query_text TEXT NOT NULL, terms_used TEXT, engine TEXT NOT NULL, prior_expectation TEXT,
  results_found INTEGER NOT NULL, results_screened INTEGER NOT NULL CHECK (results_screened <= results_found),
  deferred_reason TEXT, findings_note TEXT, harm_finding INTEGER NOT NULL DEFAULT 0,
  origin TEXT NOT NULL CHECK (origin IN ('adversarial-pass','planned','incidental','owner-supplied','lead-index')),
  created_by_session TEXT NOT NULL, created_at TEXT NOT NULL,
  CHECK (COALESCE(slug, synthesis_id, mined_ref_id) IS NOT NULL),
  CHECK ((mined_ref_id IS NULL) = (mining_direction IS NULL)));
CREATE TABLE retrievals (retrieval_id INTEGER PRIMARY KEY, sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
  path TEXT NOT NULL UNIQUE, url TEXT, http_status INTEGER, retrieved_at TEXT NOT NULL,
  exec_id INTEGER REFERENCES search_executions(exec_id), created_by_session TEXT NOT NULL);
CREATE TABLE search_candidates (candidate_id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN ('candidate','locator','code-clause')),
  exec_id INTEGER REFERENCES search_executions(exec_id),
  ref_id TEXT UNIQUE,
  title TEXT NOT NULL, doi TEXT, url TEXT, standard_number TEXT, clause TEXT,
  jurisdiction TEXT REFERENCES jurisdictions(jurisdiction), suggested_slug TEXT REFERENCES slugs(slug),
  surfaced_in INTEGER REFERENCES retrievals(retrieval_id), surfaced_quote TEXT,
  disposition TEXT NOT NULL CHECK (
       (kind = 'candidate'   AND disposition IN ('ADMITTED','REHOME','EXHAUSTED','PENDING-VERIFICATION','MISCELLANEOUS','OUT-OF-SCOPE'))
    OR (kind = 'locator'     AND disposition IN ('PROMOTED','RETIRED','REFERENCE-ONLY','SCREENED-OUT'))
    OR (kind = 'code-clause' AND disposition IN ('REFERENCE-ONLY','SUPERSEDED','RETRIEVED'))),
  resolved_ref_id TEXT REFERENCES evidence_sources(ref_id),
  harm_finding INTEGER NOT NULL DEFAULT 0, why_not_admitted TEXT, created_by_session TEXT,
  CHECK ((disposition IN ('ADMITTED','PROMOTED')) = (resolved_ref_id IS NOT NULL)));
```

Serves: `search_executions` K11 K12 K13 K15 · `retrievals` K16 K17 K37 · `search_candidates` K03 K12 K16 (merges `search_candidates`, `source_locators`, `research_code_leads`; its `ref_id` holds the REF ids pre-reset locators already carry, so `next_ref_id` never reissues them, LED-083, PIP-17).

**Where the slug lives.** `slugs` (base). Pointed at by `search_executions.slug`, `search_candidates.suggested_slug`, `scans.slug`. Read by `v_coverage` (K11, K13), `v_follow_up` (K04) and `log-search`'s bucket refusal (A31), which gates a search, never an admission. No slug column exists in `source_value_extractions`, `syntheses`, `specifications` or `v_render`; the engine and renderer read none. A violation shows as `grep -n slug scripts/assess/assess_cell.py scripts/render.py` returning a line.

Writers: `log-search` (an artefact is required unless `deferred_reason` is set; an MCP result is saved with `record_file` first; out-of-bucket refusal, A31) · `add-candidate` (cites the retrieval it surfaced in; `surfaced_quote` must be in those bytes, PIP-19) · `resolve-candidate` (re-description from the source, R15; ADMITTED/PROMOTED terminal, fixing M01.t3). A `retrievals` row is inserted by the first verb that cites its artefact, after the verb confirms the manifest line and the file's sha256.

| `search_candidates.disposition` | to | via | guard |
|---|---|---|---|
| (none) | any of its kind | `add-candidate` | exec and retrieval exist; quote in bytes |
| PENDING-VERIFICATION, REFERENCE-ONLY | any other of its kind | `resolve-candidate` | re-description; ADMITTED/PROMOTED need `resolved_ref_id` |
| ADMITTED, PROMOTED | — | — | terminal (refusal) |

### 3.5 evidence

```sql
-- stage: evidence
CREATE TABLE evidence_sources (ref_id TEXT PRIMARY KEY,
  retrieval_id INTEGER NOT NULL REFERENCES retrievals(retrieval_id),
  source_type TEXT NOT NULL, pub_title TEXT NOT NULL, pub_year INTEGER, journal_name TEXT, publisher TEXT,
  standard_number TEXT, doi TEXT UNIQUE COLLATE NOCASE, url TEXT, language TEXT,
  jurisdiction TEXT REFERENCES jurisdictions(jurisdiction),
  verification_status TEXT NOT NULL CHECK (verification_status IN ('VERIFIED','UNVERIFIED')),
  superseded_by_ref_id TEXT REFERENCES evidence_sources(ref_id),
  created_by_session TEXT NOT NULL, created_at TEXT NOT NULL, CHECK (superseded_by_ref_id <> ref_id));
CREATE TABLE evidence_source_authors (ref_id TEXT NOT NULL REFERENCES evidence_sources(ref_id), position INTEGER NOT NULL,
  last_name TEXT, first_name TEXT, corporate_name TEXT, role TEXT NOT NULL, PRIMARY KEY (ref_id, position, role));
CREATE TABLE observed_terms (observation_id INTEGER PRIMARY KEY,
  ref_id TEXT NOT NULL REFERENCES evidence_sources(ref_id), retrieval_id INTEGER NOT NULL REFERENCES retrievals(retrieval_id),
  surface_form TEXT NOT NULL, language TEXT NOT NULL, locator TEXT, context_quote TEXT NOT NULL,
  created_by_session TEXT NOT NULL, UNIQUE (ref_id, surface_form, language, locator));
```

Serves: `evidence_sources` K01 K16 K17 K18 · `evidence_source_authors` K17 K20 · `observed_terms` K05 K06 (sighting key from T1 migration 102). The bibliographic columns shown are representative: the set is what the payload parsers emit, not redesigned here.

Writers: `add-source` (needs a retrieval; fields and authors come from a parseable payload with no CLI override; otherwise the title must be found in the bytes; a held DOI is refused and its `ref_id` named; `verification_status` computed, never typed) · `amend-source` (fields only from a newer retrieval) · `supersede-source` (existing guards: no chains; refused while a live determination rests on the source) · `observe-term` (retrieval, locator and `context_quote` found in the bytes; no `term_id`).

| `evidence_sources` | to | via | guard |
|---|---|---|---|
| (none) | UNVERIFIED, VERIFIED | `add-source` | retrieval exists; VERIFIED needs a 2xx payload whose DOI or title matches |
| UNVERIFIED | VERIFIED | `amend-source` | a newer matching retrieval |
| live | superseded | `supersede-source` | no live determination rests on it; no un-supersede |

### 3.6 judgment

```sql
-- stage: judgment
CREATE TABLE scans (scan_id INTEGER PRIMARY KEY,
  ref_id TEXT NOT NULL REFERENCES evidence_sources(ref_id), retrieval_id INTEGER NOT NULL REFERENCES retrievals(retrieval_id),
  catalogue_version INTEGER NOT NULL, target_parameter_id INTEGER REFERENCES base_parameters(parameter_id),
  text_scope TEXT NOT NULL CHECK (text_scope IN ('full','partial','fragment','abstract')),
  method TEXT NOT NULL CHECK (method IN ('auto-mined','full-read','re-read','skim')),
  slug TEXT REFERENCES slugs(slug), created_by_session TEXT NOT NULL, UNIQUE (scan_id, ref_id));
CREATE TABLE term_adjudications (adjudication_id INTEGER PRIMARY KEY,
  observation_id INTEGER NOT NULL REFERENCES observed_terms(observation_id),
  outcome TEXT NOT NULL CHECK (outcome IN ('NAMES-EXISTING','NAMES-NEW','NOT-OURS','DEFERRED')),
  term_id TEXT REFERENCES terms(term_id), rationale TEXT NOT NULL, created_by_session TEXT NOT NULL,
  CHECK ((outcome IN ('NAMES-EXISTING','NAMES-NEW')) = (term_id IS NOT NULL)));
CREATE TABLE source_value_extractions (extraction_id INTEGER PRIMARY KEY,
  ref_id TEXT NOT NULL REFERENCES evidence_sources(ref_id), scan_id INTEGER NOT NULL,
  parameter_id INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
  identity_code TEXT REFERENCES base_taxonomy_identity(identity_code), icf_code TEXT REFERENCES base_taxonomy_icf(icf_code),
  needs_code TEXT REFERENCES base_taxonomy_needs(needs_code), medical_code TEXT REFERENCES base_taxonomy_medical(medical_code),
  claim_type TEXT NOT NULL CHECK (claim_type IN ('absent','framework','numerical','qualitative','range')),
  figure_role TEXT NOT NULL CHECK (figure_role IN ('claim','condition','derived','finding')),
  claimed_value TEXT, claimed_unit TEXT, comparator TEXT CHECK (comparator IN ('<','<=','=','>','>=','approx','between')),
  claim_text TEXT NOT NULL, locator TEXT, jurisdiction TEXT REFERENCES jurisdictions(jurisdiction), setting TEXT,
  root_type TEXT CHECK (root_type IN ('measurement_primary','derived_calculation','participatory_finding','committee_assertion','untraced')),
  root_ref_id TEXT REFERENCES evidence_sources(ref_id), root_candidate_id INTEGER REFERENCES search_candidates(candidate_id),
  extraction_status TEXT NOT NULL CHECK (extraction_status IN ('preliminary','reviewed','verified','contradicted','absent-confirmed')),
  created_by_session TEXT NOT NULL,
  FOREIGN KEY (scan_id, ref_id) REFERENCES scans(scan_id, ref_id),
  CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL),
  CHECK (claim_type <> 'absent' OR (claimed_value IS NULL AND figure_role = 'finding')));
CREATE TABLE extraction_relations (relation_id INTEGER PRIMARY KEY,
  from_extraction_id INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
  to_extraction_id INTEGER REFERENCES source_value_extractions(extraction_id), to_label TEXT,
  relation TEXT NOT NULL CHECK (relation IN ('insufficient','audited_against','delta_over','exceeds','condition_on','tested_at','confirms','derived_from')),
  stated INTEGER NOT NULL, quote TEXT NOT NULL, CHECK (to_extraction_id IS NOT NULL OR to_label IS NOT NULL));
CREATE TABLE source_grades (ref_id TEXT PRIMARY KEY REFERENCES evidence_sources(ref_id),
  evidence_type TEXT NOT NULL, scope TEXT NOT NULL, co1_provenance TEXT, graded_by_session TEXT NOT NULL,
  FOREIGN KEY (evidence_type, scope) REFERENCES tier_ladder(evidence_type, scope),
  CHECK (evidence_type <> 'co1' OR (length(trim(co1_provenance)) > 0
         AND co1_provenance NOT IN ('published_corpus','participatory_synthesis'))));
CREATE TABLE lens_matches (match_id INTEGER PRIMARY KEY, ref_id TEXT NOT NULL REFERENCES evidence_sources(ref_id),
  identity_code TEXT REFERENCES base_taxonomy_identity(identity_code), icf_code TEXT REFERENCES base_taxonomy_icf(icf_code),
  needs_code TEXT REFERENCES base_taxonomy_needs(needs_code), medical_code TEXT REFERENCES base_taxonomy_medical(medical_code),
  match_grade TEXT NOT NULL CHECK (match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')),
  study_population TEXT, sample_size INTEGER, mismatch_note TEXT, created_by_session TEXT NOT NULL,
  CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL));
```

Serves: `scans` K01 K02 K04 (T1 migration 103's design, without its `mode` column) · `term_adjudications` K05 K06 · `source_value_extractions` K01 K03 K09 K22 K23 (the composite FK keeps the contract's hand-off key `ref_id` and makes it agree with the scan; no `UNIQUE(ref_id)`) · `extraction_relations` K22 K25 · `source_grades` K19 K20 · `lens_matches` K21.

Writers: `record-scan` (`catalogue_version` = `max(parameter_id)` at the time, computed by the verb) · `adjudicate-term` (no uniqueness: a contest) · `add-extraction` (parameter active; `claim_text` found in the scan's bytes; relations inline, `derived_from` needs a base) · `amend-extraction` (status, figure role, comparator, root only; a changed value or text is a second row, D-0168) · `relate-extraction` · `grade-source` · `add-lens-match` (no uniqueness, `CLAUDE.md:295-296`).

| `extraction_status` | to | via | guard |
|---|---|---|---|
| (none) | preliminary, absent-confirmed | `add-extraction` | as above; `absent` is a finding with no value |
| preliminary | reviewed, contradicted | `amend-extraction` | — |
| reviewed | verified, contradicted | `amend-extraction` | — |
| any | — | — | no delete; a skim scan's extraction never governs (§4.3) |

### 3.7 synthesis

```sql
-- stage: synthesis
CREATE TABLE syntheses (synthesis_id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN ('convergence','connection','conflict','gap','determination-gate')),
  verdict TEXT CHECK ((kind = 'convergence' AND verdict IN ('convergent','divergent','single_axis','pending_assessment'))
                   OR (kind = 'determination-gate' AND verdict IN ('CONTRADICTS','MISLINKED','UNDER-CONSERVATIVE','UNLINKED'))
                   OR (kind NOT IN ('convergence','determination-gate') AND verdict IS NULL)),
  statement TEXT NOT NULL, governing_dimension TEXT,
  author_class TEXT NOT NULL CHECK (author_class IN ('engine','opus','fable')),
  falsification_condition TEXT, confidence_interval TEXT, shift_conditions TEXT, named_dissenter TEXT,
  closed_at TEXT, closed_reason TEXT, created_by_session TEXT NOT NULL,
  CHECK ((closed_at IS NULL) = (closed_reason IS NULL)),
  CHECK (kind <> 'gap' OR closed_at IS NULL OR (falsification_condition IS NOT NULL AND confidence_interval IS NOT NULL
         AND shift_conditions IS NOT NULL AND named_dissenter IS NOT NULL)));
CREATE TABLE synthesis_inputs (synthesis_id INTEGER NOT NULL REFERENCES syntheses(synthesis_id),
  extraction_id INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),
  role TEXT NOT NULL CHECK (role IN ('governing','conditioning','excluded','down_weighted','discounted')),
  reason TEXT, PRIMARY KEY (synthesis_id, extraction_id));
```

Serves: `syntheses` K23 K24 K25 K26 K27 · `synthesis_inputs` K24 K25 K37. `kind` names the tables merged in (A03, A14, A25); the four closure fields are the research contract's `adversarial-fields-complete` criterion (`pipeline-contract.yaml:107-112`). The evidence-axis labels of `convergence_sources.role` (`clinical`, `co1`, `co2`) are derived from `v_source_tier`, so only its weighting roles survive.

Writers: `add-synthesis` (inputs required except for `gap`; prose kinds need `author_class` opus or fable; a `governing` input from a skim scan is refused) · `close-synthesis` (reason; a gap needs its four fields). The engine writes `convergence` and `gap` syntheses with `author_class='engine'`.

| `syntheses` | to | via | guard |
|---|---|---|---|
| (none) | open | `add-synthesis`, engine | as above |
| open | closed | `close-synthesis` | reason; gap fields; a closed determination-gate stops capping its cell |

### 3.8 specification

```sql
-- stage: specification
CREATE TABLE specifications (specification_id INTEGER PRIMARY KEY,
  parameter_id INTEGER NOT NULL REFERENCES base_parameters(parameter_id),
  identity_code TEXT REFERENCES base_taxonomy_identity(identity_code), icf_code TEXT REFERENCES base_taxonomy_icf(icf_code),
  needs_code TEXT REFERENCES base_taxonomy_needs(needs_code), medical_code TEXT REFERENCES base_taxonomy_medical(medical_code),
  state TEXT NOT NULL CHECK (state IN ('stated','provisional','pending','not_applicable')),
  marker TEXT CHECK (marker IN ('●','◐','○')),
  design_scale TEXT CHECK (design_scale IN ('person','population','universal')),
  value_min TEXT, value_max TEXT, value_unit TEXT, value_notations TEXT, value_note TEXT,
  code_floor_only INTEGER NOT NULL DEFAULT 0, regulatory_stratum_only INTEGER NOT NULL DEFAULT 0,
  rests_on_proxy_inference INTEGER NOT NULL DEFAULT 0, not_applicable_rationale TEXT,
  derivation_sha TEXT NOT NULL, rule_version TEXT NOT NULL,
  retired_at TEXT, retirement_reason TEXT,
  superseded_by_specification_id INTEGER REFERENCES specifications(specification_id),
  created_by_session TEXT NOT NULL,
  CHECK (COALESCE(identity_code, icf_code, needs_code) IS NOT NULL),
  CHECK ((state IN ('stated','provisional')) = (marker IS NOT NULL)),
  CHECK (state <> 'stated' OR (code_floor_only + regulatory_stratum_only + rests_on_proxy_inference) = 0),
  CHECK (regulatory_stratum_only = 0 OR marker = '○'),
  CHECK (state <> 'not_applicable' OR length(trim(not_applicable_rationale)) > 0),
  CHECK ((retired_at IS NULL) = (retirement_reason IS NULL)));
CREATE TABLE specification_syntheses (specification_id INTEGER NOT NULL REFERENCES specifications(specification_id),
  synthesis_id INTEGER NOT NULL REFERENCES syntheses(synthesis_id), PRIMARY KEY (specification_id, synthesis_id));
```

Serves: `specifications` K09 K22 K27 K28 K29 K30 · `specification_syntheses` K24 K37. The first CHECK carries PIP-04 (never medical alone) and the "at least one lens" rule together, replacing `medical_lens_integrity`. `marker` is the determination's own output, "therefore 1200 mm, marked ●" (`CLAUDE.md:256`); today it is not stored (`tier_basis` is a text summary). Removed as copies: `governing_refs`, `convergence_id`, `gap_register_id`, `tier_basis`, `has_unverified_sources` (all reachable by walk; the last is computed in `v_render`).

Writers: `assess_cell.py --emit-sql` only (computes state, marker, flags, notations and `derivation_sha`; writes the cell's `convergence` synthesis and, when pending, its `gap` synthesis; caps at provisional while an open `determination-gate` synthesis bears on the cell's extractions; excludes skim scans from governing) · `retire-specification`.

| `specifications.state` | to | via | guard |
|---|---|---|---|
| (none) | stated, provisional, pending | engine | tier arithmetic (K28); CHECKs |
| (none) | not_applicable | none (A22) | rationale CHECK |
| live | retired | `retire-specification` | reason; then re-determine; `superseded_by` links the new row |

### 3.9 render and infrastructure

```sql
-- stage: render
CREATE TABLE weighting_profile (audience TEXT NOT NULL, use_pattern TEXT NOT NULL, tier_weights TEXT NOT NULL,
  PRIMARY KEY (audience, use_pattern));
-- stage: infrastructure (key columns shown; the rest unchanged)
CREATE TABLE data_migrations (filename TEXT PRIMARY KEY, applied_at TEXT NOT NULL);
CREATE TABLE adversarial_passes (pass_id INTEGER PRIMARY KEY, session TEXT NOT NULL, closed_at TEXT);
CREATE TABLE adversarial_findings (finding_id INTEGER PRIMARY KEY, pass_id INTEGER NOT NULL REFERENCES adversarial_passes(pass_id),
  lens TEXT NOT NULL, disposition TEXT);
CREATE TABLE gaps (gap_id TEXT PRIMARY KEY, category TEXT NOT NULL, status TEXT NOT NULL, description TEXT NOT NULL);
CREATE TABLE decisions (decision_id TEXT PRIMARY KEY, summary TEXT NOT NULL);
```

Render has no hand-off table (LED-105): `scripts/render.py` reads `v_render`, `v_source_tier` and the audience's `weighting_profile`, and writes nothing. Infrastructure is not a stage.

### 3.10 views (the only five)

```sql
CREATE VIEW v_source_tier AS
  SELECT g.ref_id, g.evidence_type, l.tier, l.band
    FROM source_grades g JOIN tier_ladder l USING (evidence_type, scope)
    JOIN evidence_sources e ON e.ref_id = g.ref_id WHERE e.superseded_by_ref_id IS NULL;
CREATE VIEW v_scan_ledger AS
  WITH pairs AS (SELECT e.ref_id, p.parameter_id FROM evidence_sources e CROSS JOIN base_parameters p
                  WHERE e.superseded_by_ref_id IS NULL AND p.status = 'active'),
       best AS (SELECT pr.*, (SELECT s.scan_id FROM scans s WHERE s.ref_id = pr.ref_id
                   AND ((s.target_parameter_id IS NULL AND s.catalogue_version >= pr.parameter_id)
                     OR  s.target_parameter_id = pr.parameter_id)
                 ORDER BY (s.text_scope = 'full') DESC, (s.method <> 'skim') DESC, s.scan_id DESC LIMIT 1) AS scan_id
                  FROM pairs pr)
  SELECT b.ref_id, b.parameter_id, b.scan_id,
    CASE WHEN EXISTS (SELECT 1 FROM source_value_extractions x WHERE x.ref_id = b.ref_id
                       AND x.parameter_id = b.parameter_id AND x.claim_type <> 'absent') THEN 'EXTRACTED'
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x WHERE x.ref_id = b.ref_id
                       AND x.parameter_id = b.parameter_id) THEN 'STATED-ABSENT'
         WHEN s.text_scope = 'full' AND s.method <> 'skim' THEN 'READ-NOTHING-FOUND'
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         ELSE 'NOT-READ' END AS status
    FROM best b LEFT JOIN scans s ON s.scan_id = b.scan_id;
CREATE VIEW v_follow_up AS
  SELECT x.extraction_id, x.ref_id, s.slug AS read_under
    FROM source_value_extractions x JOIN scans s ON s.scan_id = x.scan_id
   WHERE x.extraction_status = 'preliminary' AND s.slug IS NOT NULL
     AND s.slug NOT IN (SELECT e.slug FROM search_candidates k JOIN search_executions e ON e.exec_id = k.exec_id
                         WHERE k.resolved_ref_id = x.ref_id AND e.slug IS NOT NULL);
CREATE VIEW v_coverage AS
  SELECT slug, jurisdiction, language, identity_code, icf_code, needs_code, medical_code,
         COUNT(*) AS searches, SUM(deferred_reason IS NOT NULL) AS deferred
    FROM search_executions WHERE slug IS NOT NULL GROUP BY 1, 2, 3, 4, 5, 6, 7;
CREATE VIEW v_render AS
  SELECT s.specification_id, s.parameter_id, t.canonical_en AS parameter, p.question,
         s.identity_code, s.icf_code, s.needs_code, s.medical_code, s.state, s.marker, s.design_scale,
         s.value_min, s.value_max, s.value_unit, s.value_notations,
         s.code_floor_only, s.regulatory_stratum_only, s.rests_on_proxy_inference,
         (SELECT group_concat(DISTINCT x.ref_id) FROM specification_syntheses ss
            JOIN synthesis_inputs i ON i.synthesis_id = ss.synthesis_id
            JOIN source_value_extractions x ON x.extraction_id = i.extraction_id
           WHERE ss.specification_id = s.specification_id AND i.role = 'governing') AS governing_refs,
         EXISTS (SELECT 1 FROM specification_syntheses ss JOIN synthesis_inputs i ON i.synthesis_id = ss.synthesis_id
            JOIN source_value_extractions x ON x.extraction_id = i.extraction_id
            JOIN evidence_sources e ON e.ref_id = x.ref_id
           WHERE ss.specification_id = s.specification_id AND i.role = 'governing'
             AND e.verification_status <> 'VERIFIED') AS has_unverified_sources
    FROM specifications s JOIN base_parameters p ON p.parameter_id = s.parameter_id JOIN terms t ON t.term_id = p.term_id
   WHERE s.retired_at IS NULL AND p.status = 'active';
```

Each view exists because no foreign key can carry its relation: `v_scan_ledger` an absence (K02), `v_follow_up` a predicate over two paths (K04), `v_coverage` an aggregate (K11, K13), `v_render` the one tuple every register reads (K29, K31), `v_source_tier` the ladder join that both engine and renderer read (K19). Everything else is the generic walk.

---

## 4. HANDSHAKES

### 4.1 One generic walk

`dbcore.walk(conn, table, key, direction, stages, order)` reads edges from `PRAGMA foreign_key_list` at call time (no list in code) and yields reachable rows. `up` follows each FK to its parent, repeating to base and to `retrievals`; `down` follows FKs backwards; `lateral` goes down to a child and up to a different row of the same stage (siblings sharing a parent); `skip` repeats up or down until a named stage; `re-entrant` follows only edges whose child stage precedes its parent's in the contract order. `stages` and `order` are injected (§3.2). Estimate: about 30 lines; the four walkers it replaces total 2,635 lines (§3.1 command).

### 4.2 Direction × stage pair (ideal)

| pair | down | up (ends at bytes) | lateral (receiving stage) | skip | re-entrant |
|---|---|---|---|---|---|
| base → every stage | walk down from a vocabulary row to every row using that parameter, lens code, slug, jurisdiction or rung | each row names its vocabulary by FK | `lens_crossings` (lens↔lens); `terms.broader_term_id`; `base_parameters.merged_into` | none: base is the floor | judgment → base: `term_adjudications` (NAMES-NEW) → `terms` → `base_parameters`; base → judgment: a new parameter appears as NOT-READ in `v_scan_ledger` |
| research → evidence | `search_candidates.resolved_ref_id` (N:1, so the pointer sits on the many side) | `evidence_sources.retrieval_id` → `retrievals` (→ `exec_id`) | authors, observations by `ref_id`; `superseded_by_ref_id` | none: adjacent | evidence → research: `search_executions.mined_ref_id` |
| evidence → judgment | `scans`, `source_value_extractions`, `source_grades`, `lens_matches` by `ref_id`; `term_adjudications.observation_id` | `scans.retrieval_id` → `retrievals`; composite FK (scan, ref) | siblings by `ref_id`; `extraction_relations`; parameter → extractions; source → parameters read (`v_scan_ledger`) | judgment → research: `root_candidate_id` | none needed: judgment produces no source; a cited, unheld source enters research as a candidate |
| judgment → synthesis | `synthesis_inputs.extraction_id` | → extraction → scan → `retrievals` | syntheses sharing an input; cross-parameter = inputs over more than one parameter | synthesis → source: walk up through extractions | synthesis → research: `search_executions.synthesis_id` (gap-driven search; a reasoning document's leads) |
| synthesis → specification | `specification_syntheses.synthesis_id` | → `synthesis_inputs` → … → `retrievals` | other lens cells of one parameter (`parameter_id`); `superseded_by_specification_id` | determination → source: walk up; source → every determination: walk down | specification → judgment: a `determination-gate` synthesis on the cell's extractions; the engine retires and re-determines |
| specification → render | `v_render` (live rows) | `v_render.specification_id` → walk up | `v_render` rows sharing `parameter_id` (lens switching, LED-110) | figure → source: `governing_refs` → `evidence_sources` (LED-081) | none: render has no writer (LED-105); a reader's challenge enters research as a candidate |

### 4.3 Handshake rules

| handshake | crosses when | receiver verifies (inside the writer, or by FK/CHECK) | a record that cannot cross |
|---|---|---|---|
| base → any | the vocabulary row exists and is live | FK; `status='active'` refusal for parameters | refused at write |
| research → evidence | candidate is ADMITTED | a retrieval exists for the locator (R10); DOI not already held (refusal names the held `ref_id`) | stays a candidate: PENDING-VERIFICATION, EXHAUSTED or OUT-OF-SCOPE, with `why_not_admitted` |
| evidence → judgment | source live | composite FK (scan, ref); quote and claim text found in the scan's bytes (`quote_in_artefacts`, `retrieval_log.py:717`) | refused; a superseded source is refused and its successor named; an unadjudicated observation holds the batch open (`research_dod_session`) |
| judgment → synthesis | extraction live, parameter active | a skim-scan extraction cannot be `governing` | recorded as `excluded` with a reason |
| synthesis → specification | engine run | stated/provisional need a governing input and pass the CHECKs; an open determination-gate caps at provisional | pending with a `gap` synthesis; old rows retired in place |
| specification → render | `retired_at IS NULL`, parameter active | `v_render`'s WHERE | not rendered; history stays walkable |
| re-entry | synthesis open; mined source live; new parameter active | `log-search` refuses a closed synthesis; FKs | refused |

### 4.4 What the current repo leaves empty

```
python3 - <<'PY'
import sqlite3, yaml, re
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
st = yaml.safe_load(open('governance/stage-map.yaml'))['tables']
sp = [s['id'] for s in yaml.safe_load(open('governance/pipeline-contract.yaml'))['stages']]
T = [r[0] for r in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
fk = [(st.get(t), st.get(f[2]), f'{t}.{f[3]}') for t in T for f in c.execute(f'pragma foreign_key_list("{t}")')]
vs = {n: {st.get(t) for t in T if re.search(rf'\b{t}\b', s)} for n, s in c.execute("select name, sql from sqlite_master where type='view'")}
for a, b in zip(sp[1:], sp[2:]):
    print(f'{a}->{b}', 'FK:', [e for x, y, e in fk if (x, y) == (b, a)] or 'NONE',
          'fwd:', [e for x, y, e in fk if (x, y) == (a, b)] or '-', 'views:', [v for v, s in vs.items() if {a, b} <= s] or '-')
PY
```

Result 2026-10-12 (stage-map placements, so extractions count as evidence):
- **judgment ↔ synthesis: down and up empty.** No synthesis table names a judgment row; the only FKs run forward (`evidence_population_match.gap_id`, `citation_population_links.citation_id`). Ideal: `synthesis_inputs`.
- **specification ↔ render: empty.** No FK and no view; the render tables are item-keyed. Ideal: `v_render`.
- **research → evidence: no pointer from evidence back.** Three forward FKs and `v_source_admission` carry it; that is walkable, and the ideal keeps only the many-side pointer (A19).
- **Up to the bytes: no FK at all.** `file_anchor` names a retrieval-log path on 18 of 101 extractions [c4a]; 49 of 53 sources have no extraction path to bytes [c4b]; the manifests carry a `ref_id` on 80 of 433 lines, naming 38 distinct sources [c4c]. Ideal: `retrievals` with NOT NULL pointers.
- **Lateral source → parameters read: empty** (P-V NOT-BUILT on `main`). Ideal: `v_scan_ledger`.
- **Skip determination → source: a copy.** `specification_source_links` is 38 of 38 derivable through governing extraction links [c4d]. Ideal: the walk.
- **Re-entrant: base → judgment re-scan empty;** synthesis → research is `gap_mining` (0 rows); a reasoning document's lead is `search_candidates.surfaced_in`, free text. Ideal: `v_scan_ledger`, `search_executions.synthesis_id`, `surfaced_in` as an FK.

```
# [c4a]
q 'select count(*), count(file_anchor) from source_value_extractions'
# [c4b]
q "select count(*) from evidence_sources e where not exists (select 1 from source_value_extractions x where x.ref_id = e.ref_id and x.file_anchor like 'retrieval-log/%')"
# [c4c]  lines, lines with ref_id, distinct ref_ids
python3 -c "import json,glob;L=[json.loads(l) for f in glob.glob('retrieval-log/*/manifest.jsonl') for l in open(f) if l.strip()];R=[d['ref_id'] for d in L if d.get('ref_id')];print(len(L),len(R),len(set(R)))"
# [c4d]
q "select count(*), sum(exists(select 1 from specification_extraction_links l join source_value_extractions x on x.extraction_id = l.extraction_id where l.specification_id = s.specification_id and x.ref_id = s.ref_id and l.role = 'governing')) from specification_source_links s"
```

---

## 5. THE WALKS

**(a) One source → every parameter × lens, with what was not found:**
```
SELECT l.parameter_id, l.status, x.identity_code, x.icf_code, x.needs_code, x.medical_code, x.extraction_id
  FROM v_scan_ledger l LEFT JOIN source_value_extractions x ON x.ref_id = l.ref_id AND x.parameter_id = l.parameter_id
 WHERE l.ref_id = :ref;
```
**(b) A concept in a source → a new parameter → its re-scan backlog:** `observed_terms` → `term_adjudications` (outcome NAMES-NEW, `term_id`) → `terms` → `base_parameters`; then `SELECT ref_id FROM v_scan_ledger WHERE parameter_id = :new AND status = 'NOT-READ'` lists every earlier source to re-read for it (`record-scan` with `target_parameter_id`).
**(c) One parameter → all sources, lenses, extractions and syntheses:** `SELECT x.*, t.tier, t.band FROM source_value_extractions x LEFT JOIN v_source_tier t ON t.ref_id = x.ref_id WHERE x.parameter_id = :p`; what was read and held nothing: `SELECT ref_id, status FROM v_scan_ledger WHERE parameter_id = :p AND status IN ('READ-NOTHING-FOUND','STATED-ABSENT','NOT-READ')`; syntheses: `SELECT DISTINCT i.synthesis_id FROM synthesis_inputs i JOIN source_value_extractions x ON x.extraction_id = i.extraction_id WHERE x.parameter_id = :p`.
**(d) Parameter × lens → determination → rendered figure → bytes, and back:** forward `SELECT * FROM v_render WHERE parameter_id = :p AND identity_code = :code`; backward
```
SELECT x.extraction_id, x.claim_text, r.path, r.sha256
  FROM specification_syntheses ss JOIN synthesis_inputs i ON i.synthesis_id = ss.synthesis_id
  JOIN source_value_extractions x ON x.extraction_id = i.extraction_id JOIN scans s ON s.scan_id = x.scan_id
  JOIN retrievals r ON r.retrieval_id = s.retrieval_id
 WHERE ss.specification_id = :spec AND i.role = 'governing';
```
The file at `r.path` re-hashes to `r.sha256`; the source's metadata payload is `evidence_sources.retrieval_id`.
**(e) Re-entrant edges:** synthesis → research (`search_executions.synthesis_id`: gap-driven mining and a reasoning document's leads); evidence → research (`mined_ref_id`: citation mining); judgment → base (NAMES-NEW → term → parameter); base → judgment (NOT-READ backlog); specification → judgment (determination-gate synthesis, retire, re-determine); judgment → research (`root_candidate_id`: an unadmitted root).

I ran (a)–(d) and the five views on the DDL above with one synthetic chain in an in-memory database (scratch, 2026-10-12): every view returned its row, a second parameter appeared as NOT-READ, a cross-slug preliminary figure appeared in `v_follow_up`, and the CHECKs refused a medical-only cell, an unmarked stated cell, a stated proxy, a `published_corpus` Co-1 grade, a lens-less extraction, a source without a retrieval and a search with no slug, synthesis or mined source.

**Directions the ideal cannot walk, and why:**
- Legacy rows to bytes: today's extractions and sources mostly have no retrieval pointer (§4.4). Reaching the ideal needs each source's payload linked (from manifests, `retrieval_log.reconstruct_manifest`/`backfill` at `retrieval_log.py:1729-1748`) or re-retrieved; a row with no bytes cannot meet the NOT NULL pointer and is re-read, not migrated. [GAP: how many can be linked is not measured.]
- A candidate is not walkable from a parameter: candidates precede judgment and carry no parameter (by design, K38).
- By setting or room: `setting` is free text (U3).
- By category: only `broader_term_id` (U1).

---

## 6. WALKABILITY ACROSS ALL TABLES

One derived check over every table in `sqlite_master`: stage from the stage-map; FK edges from `PRAGMA foreign_key_list`; an id column is a column named like another table's single-column primary key; `up` = path to a base table; `down` = path to `specifications` not passing through base (base tables may). Re-run:

```
python3 - <<'PY'
import sqlite3, yaml, collections as C
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
st = yaml.safe_load(open('governance/stage-map.yaml'))['tables']
T = [r[0] for r in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
fk = [(t, f[3], f[2]) for t in T for f in c.execute(f'pragma foreign_key_list("{t}")')]
cols = {t: c.execute(f'pragma table_info("{t}")').fetchall() for t in T}
home = C.defaultdict(set)
for t in T:
    pk = [r[1] for r in cols[t] if r[5]]
    if len(pk) == 1: home[pk[0]].add(t)
adj = C.defaultdict(set)
for a, _, b in fk: adj[a].add(b); adj[b].add(a)
def bfs(s, goal, via_base):
    seen, q = {s: 0}, C.deque([s])
    while q:
        n = q.popleft()
        if n != s and goal(n): return seen[n]
        if n != s and not via_base and st.get(n) == 'base': continue
        for m in adj[n] - seen.keys(): seen[m] = seen[n] + 1; q.append(m)
bad = C.Counter(r[0] for r in c.execute('pragma foreign_key_check'))
for t in sorted(T, key=lambda t: (st.get(t, '?'), t)):
    fkc = {col for a, col, _ in fk if a == t}
    loose = [r[1] for r in cols[t] if r[1] in home and t not in home[r[1]] and r[1] not in fkc]
    up = 0 if st.get(t) == 'base' else bfs(t, lambda n: st.get(n) == 'base', True)
    dn = 0 if t == 'specifications' else bfs(t, lambda n: n == 'specifications', st.get(t) == 'base')
    fail = [d for d, v in (('up', up), ('down', dn)) if v is None] + ['orphan'] * (not adj[t]) \
         + [f'dangling:{bad[t]}'] * bool(bad[t]) + [f'unFK:{",".join(loose)}'] * bool(loose)
    print(t, st.get(t, 'UNMAPPED'), '-' if up is None else up, '-' if dn is None else dn, ' '.join(fail) or 'ok', sep='\t')
PY
```

Columns: table, stage, hops toward base, hops toward the determination, failures. Result 2026-10-12: **21 of 82 tables fail**; `PRAGMA foreign_key_check` reports no dangling rows. The walk is structural: a 0-row table that passes is unproven (rule 4).

| failing today | direction | the ideal |
|---|---|---|
| `access_duration`, `access_stakes`, `life_stage_modifiers`, `situations`, `lang_jur_map` | down, orphan | deleted: no condition |
| `external_root_registry`; `source_value_extractions` (`root_id` has no FK) | orphan; unFK | deleted; pointer added (`root_ref_id` or `root_candidate_id`) |
| `url_verification_runs`, `pipeline_runs`, `bpc_metadata` | orphan / down | deleted (`retrievals`; A02) |
| `citation_mining`, `search_coverage`, `search_languages` | down | deleted: derived from `search_executions` (A34) |
| `reference_stubs`, `research_code_leads`, `source_locators` | orphan | merged into `search_candidates`, which has FKs |
| `conflicts` (`gap_id` has no FK), `connections`, `connection_targets` | up, down | merged into `syntheses` / `synthesis_inputs` |
| `weighting_profile` | orphan | kept: render configuration chosen by audience; named residual |
| `data_migrations` | orphan | kept: infrastructure, keyed on migration filenames |

The same function over the §3 DDL (scratch, 2026-10-12, stages from its `-- stage:` lines) fails only `search_candidates.ref_id` (the LED-083 reservation, a residual), `weighting_profile`, and the five infrastructure tables, which are outside the spine by definition.

**Minimum code that keeps it true:** one registered gate, `walkability`, of about this size, failing on any `UNMAPPED`, any non-infrastructure `up`/`down`/`orphan`/`dangling`/`unFK` result outside two named residuals (LED-083; `weighting_profile`). It reads the schema at run time, so a new table, column or FK is covered without editing it. It replaces `graph_audit`, `test_graph_audit`, `pipeline_walk_fresh` and `schema_walkability_fresh`.

---

## 7. ACQUISITION

For any source and any parameter, with no container and no slug in the way:

1. **Find.** The agent queries (an MCP search tool, an API, a catalogue, the Internet Archive). Before anything reads the response, `retrieval_log.fetch` (HTTP) or `record_file` (an MCP result or a local file) writes the bytes and a manifest line (`retrieval_log.py:203-230`). `log-search` records the query verbatim, the prior, its reason (slug, synthesis or mined source), lens codes, jurisdiction, language and counts, and cites the artefact; the `retrievals` row enters with it.
2. **Stage.** `add-candidate` for each result considered, citing the retrieval and a quote that must be in it (PIP-19).
3. **Admit.** Re-retrieve the locator with `fetch` (DOI → Crossref/PubMed → publisher → repository → Wayback `if_` form, `CLAUDE.md` §7); `add-source --retrieval`: fields and authors parsed from the payload; DOI de-duplication; verification computed; `resolve-candidate ADMITTED`.
4. **Read.** Fetch or record the full text; one `record-scan` row says "read for every parameter up to version N".
5. **Mine.** `observe-term` for each concept phrase, located in the bytes; `add-extraction` for each parameter the source bears on, in each lens it names: figures, arguments, findings, harms and stated absences.
6. **Organize.** `adjudicate-term` → `add-term` / `add-parameter` or decline; `grade-source`; `add-lens-match`; `relate-extraction`. A new parameter shows every earlier source as NOT-READ at once.
7. **Sort.** Queries over the views and the walk (band, tier, independent roots, recency). No stored order.
8. **Weigh.** `assess_cell.py --emit-sql`; Opus/Fable add divergence, conflict and connection syntheses.
9. **Emit.** `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py`.

**What must persist for CLAUDE.md 5(c) and R10:** the bytes (committed under `retrieval-log/`), the manifest line written before the caller sees data, the `retrievals` row, and the NOT NULL pointers to it from `evidence_sources`, `observed_terms` and `scans` (and through scans, every extraction). A field typed from memory has nowhere to go: `add-source` takes no bibliographic flags when a parseable payload exists.

**Code** (what cannot be a constraint or a writer refusal): `fetch`/`record_file`; a payload parser per structured API actually used [I did not count them]; byte decoding and `quote_in_artefacts`; the verbs; the engine; the renderer; `walk`; the write path; `run_checks.py` and twelve gates. **Data:** vocabularies, `tier_ladder`, bucket membership, the catalogues and the parameter list, mining screens (`governance/mining-screens.yaml`, LED-181), rulings, and the bytes. No per-source scraper, crawler or scheduled job.

---

## 8. HARD-CODED INVENTORY

| literal in the current repo | find it | 2026-10-12 | the ideal | residual, and why |
|---|---|---|---|---|
| `choices=` mirroring a CHECK | [c8a] | 55 total; 33 derived | every one from `dbcore.check_values` | none |
| enums for DB vocabularies | [c8b] | 42 classes | CHECK or FK table | enums for values not in the DB [I did not classify the 42] |
| tier map in code | [c8c] | 10 pairs | `tier_ladder` rows | the ladder: a ruling is the value |
| curated table lists and row floors | [c8d] | 8 tables with floors; 7 state columns | deleted with `graph_audit`; `walkability` reads `sqlite_master` | none |
| exemption lists | [c8e] | 8 assignments; 49 + 55 lines of exemption files | derived: stage `infrastructure`; immutable paths | LED-083 (pre-reset REF ids); `scripts/migrations/` and `_archived/` path skips (immutable by rule 3) |
| job-owned tables | [c8f] | 2 | none (A02) | none |
| registry floors | [c8g] | 91 `min_items`; 14 `floor` lines | a gate must examine > 0 whenever its subject table holds rows | none |
| `MODEL_TABLE_MAP` | [c8h] | 1 map | deleted (A24) | none |
| paths bound at import | [c8i] | 157 bindings; 69 files read `GUIDEBOOK_DB_PATH`; 58 `REPO_ROOT` definitions | one binding each in `dbcore` (§3.2) | `dbcore.REPO_ROOT`; the env-var name |
| clock calls | [c8j] | 18 | `now` injected | `dbcore.now` |
| counts in prose | [c8k] | 118 lines | the command beside the number | ruled numbers ("four lenses" LED-128, "three tables" LED-120, ordinals 3/2/1 LED-162); dated history in frozen records |
| bucket membership | [c8l] | prose table | `jurisdictions.bucket` (A31) | the assignment is a ruling |
| name screen | [c8m] | one regex in `insert_term` | kept | the ruling (LED-148) is the value |
| prepopulation catalogues | T1 `scripts/migrations/104_vocabulary_lifecycle.sql` (local branch) | 5 paths in a CHECK | `terms.catalogue` CHECK | the owner's selection (LED-204) is the value |
| table → stage | `governance/stage-map.yaml` | judged | kept as the one judged home | no derivable edge exists (`stage-map.yaml:12-17`) |

```
# [c8a]
grep -c 'choices=' scripts/db.py; grep -c 'choices=dbcore\.\(schema_choices\|check_values\)' scripts/db.py
# [c8b]
grep -c '^class .*Enum' schemas/enums.py
# [c8c]
grep -n -A11 'TIER_MAP = ' schemas/tier_derivation.py
# [c8d]
grep -n -A10 'MISSION_CRITICAL =\|STATE_DIST =' scripts/audit/graph/topology.py
# [c8e]
grep -rnE '^[A-Z_]*(EXEMPT|KNOWN|ALLOW|IGNORE|SKIP|DEBT)[A-Z_]* *=' scripts --include=*.py | wc -l
wc -l governance/schema-reference-exemptions.yaml scripts/audit/graph/known_debt.yaml
# [c8f]
grep -n '^EXEMPT_TABLES' scripts/audit/migration_reproducibility.py
# [c8g]
grep -c 'min_items' governance/check-registry.yaml; grep -cE '^\s+floor' governance/check-registry.yaml
# [c8h]
grep -n 'MODEL_TABLE_MAP = ' scripts/audit/validate_pydantic_schemas.py
# [c8i]
grep -rnE '^[A-Z_]+ *= *.*(Path\(|os\.path\.|os\.environ)' scripts tools --include=*.py | wc -l
grep -rl GUIDEBOOK_DB_PATH scripts tools --include=*.py | wc -l
grep -rnE '^REPO(_ROOT)? *=' scripts tools --include=*.py | wc -l
# [c8j]
grep -rn 'datetime.now\|datetime.utcnow' scripts --include=*.py | grep -v migrations | wc -l
# [c8k]
grep -rnE '\b[0-9]{1,4} (tables|rows|checks|verbs|parameters|sources|views|migrations)\b' CLAUDE.md governance/*.md architecture/*.md | wc -l
# [c8l]
sed -n '420,424p' workplan/2026-08-18-research-frame-proposal.md
# [c8m]
grep -n 'states a determination in its own name' scripts/db.py
```

Where derivation would cost more than the literal (the ruled numbers, the stage judgment, path skips), the literal stays and names its ruling.

---

## 9. MINIMALITY

One line per object: the condition that fails if it is removed.

| kind | object | stage | conditions | fails if removed |
|---|---|---|---|---|
| TABLE | terms | base | K05 K06 K07 | a parameter has no name; growth has no target |
| TABLE | term_aliases | base | K11 K12 | legacy multilingual search terms lost |
| TABLE | base_parameters | base | K06 K08 K09 | the determination has no key |
| TABLE | base_taxonomy_identity | base | K09 K10 | identity lens |
| TABLE | base_taxonomy_icf | base | K09 K10 | ICF lens |
| TABLE | base_taxonomy_needs | base | K09 K10 | needs lens |
| TABLE | base_taxonomy_medical | base | K09 K10 | medical lens |
| TABLE | lens_crossings | base | K10 K11 | WRK-181 map and LED-156 correspondence homeless |
| TABLE | jurisdictions | base | K13 K35 | vocabulary returns to an enum and a check script |
| TABLE | slugs | base | K11 K14 | coverage cannot group by slug |
| TABLE | tier_ladder | base | K19 K28 K29 | tier returns to a stored column or code |
| TABLE | search_executions | research | K11 K12 K13 K15 | no record of what was looked for |
| TABLE | retrievals | research | K16 K17 K37 | backward walk stops short of the bytes |
| TABLE | search_candidates | research | K03 K12 K16 | surfaced, unadmitted material homeless |
| TABLE | evidence_sources | evidence | K01 K16 K17 K18 | nothing admitted |
| TABLE | evidence_source_authors | evidence | K17 K20 | Co-1 co-producers unrecorded |
| TABLE | observed_terms | evidence | K05 K06 | no harvest, no growth route |
| TABLE | scans | judgment | K01 K02 K04 | "read, nothing found" unrecordable; skim indistinguishable |
| TABLE | term_adjudications | judgment | K05 K06 | phrase → term unjudged |
| TABLE | source_value_extractions | judgment | K01 K03 K09 | no judgment rows |
| TABLE | extraction_relations | judgment | K22 | relative and derived figures lose their relation |
| TABLE | source_grades | judgment | K19 K20 | tier verdict has no judgment home |
| TABLE | lens_matches | judgment | K21 | directness ungraded |
| TABLE | syntheses | synthesis | K23–K27 | no synthesis; a pending cell has no gap |
| TABLE | synthesis_inputs | synthesis | K24 K25 K37 | a synthesis cannot name what it weighed |
| TABLE | specifications | specification | K09 K27–K30 | no determination |
| TABLE | specification_syntheses | specification | K24 K37 | many syntheses → one determination lost |
| TABLE | weighting_profile | render | K29 | audience registers lose their profile |
| TABLE | data_migrations | infrastructure | K33 | replay cannot tell what was applied |
| TABLE | adversarial_passes | infrastructure | K39 | survived claims unrecorded |
| TABLE | adversarial_findings | infrastructure | K39 | same |
| TABLE | gaps | infrastructure | K40 | tooling defects homeless (rule 10) |
| TABLE | decisions | infrastructure | — | kept only until OQ-5 is answered (§12 Q7) |
| VIEW | v_source_tier | — | K19 K29 | engine and renderer each re-join the ladder |
| VIEW | v_scan_ledger | — | K01 K02 | absence unreadable |
| VIEW | v_follow_up | — | K04 | the cross-slug tag lost |
| VIEW | v_coverage | — | K11 K13 | slug × lens × jurisdiction coverage unreadable |
| VIEW | v_render | — | K29 K31 | registers diverge |
| VERB | log-search | research | K11 K12 K13 | searches unlogged |
| VERB | add-candidate | research | K03 K12 K17 | surfaced material unrecorded |
| VERB | resolve-candidate | research | K16 | no admission edge |
| VERB | add-source | evidence | K16 K17 K18 | nothing admitted |
| VERB | amend-source | evidence | K16 K17 | verification cannot improve |
| VERB | supersede-source | evidence | K08 | no retire-in-place for sources |
| VERB | observe-term | evidence | K05 | no harvest |
| VERB | record-scan | judgment | K02 | no read-state |
| VERB | adjudicate-term | judgment | K05 K06 | no adjudication |
| VERB | add-extraction | judgment | K01 K03 | no judgment rows |
| VERB | amend-extraction | judgment | K22 | status cannot advance |
| VERB | relate-extraction | judgment | K22 K25 | no late or cross-parameter relation |
| VERB | grade-source | judgment | K19 K20 | no tier verdict |
| VERB | add-lens-match | judgment | K21 | no directness grade |
| VERB | add-term | base | K06 K07 | no growth |
| VERB | add-parameter | base | K06 K08 | no parameter, no declination |
| VERB | amend-parameter | base | K08 K22 K32 | no retire, merge, direction or question |
| VERB | add-lens-code | base | K10 | ICF and medical codes unregistrable |
| VERB | add-lens-crossing | base | K10 | maps unwritable |
| VERB | add-slug | base | K14 | slugs unwritable (P-O) |
| VERB | add-synthesis | synthesis | K24 K25 K26 | no human synthesis |
| VERB | close-synthesis | synthesis | K08 K27 | gaps and gates never close |
| VERB | retire-specification | specification | K08 | determinations cannot be retired |
| VERB | record-adversarial-pass | infrastructure | K39 | pass unrecorded |
| VERB | dispose-adversarial-finding | infrastructure | K39 | findings undisposed |
| VERB | close-adversarial-pass | infrastructure | K39 | pass never closes |
| VERB | add-gap | infrastructure | K40 | tooling gaps unfiled |
| VERB | close-gap | infrastructure | K40 | tooling gaps never close |
| GATE | migration_reproducibility (deep form, blocking) | — | K33 | an UPDATE outside migrations passes (CLAUDE.md:85-98) |
| GATE | artefact_integrity (merges provenance_artefact_audit, author_fidelity) | — | K16 K17 | a deleted or altered payload passes |
| GATE | determination_reproducible (test_db_integrity K01 alone) | — | K27 | a hand-edited or stale determination passes |
| GATE | walkability (new; §6) | — | K37 K44 | a new table or column can be an orphan |
| GATE | judgment_handoff_shape | — | K01 | a `UNIQUE(ref_id)` collapses the fan-out |
| GATE | research_dod_session | — | K01 K02 K05 | a batch closes with unread sources or unadjudicated phrases |
| GATE | schema_reference_audit | — | K40 | rule 4 callers unswept |
| GATE | claude_md_spine | — | K36 | the spine line drifts |
| GATE | attestation (merges attestation_presence, attestation_schema) | — | K40 | rule 2 unenforced |
| GATE | supersession_backpointer_audit | — | K40 | rule 0 supersessions unmarked |
| GATE | research_tooling_separation | — | K40 | rule 10 unchecked |
| GATE | research_contract_sync | — | K40 | the session hook drifts from the contract |
| FILE | CLAUDE.md | Layer 0 | K40 | no process rules |
| FILE | governance/pipeline-contract.yaml | Layer 1 | K36 K40 | no stage ids |
| FILE | governance/research-contract.yaml | Layer 1 | K12 | no research rules |
| FILE | governance/stage-map.yaml | Layer 1 | K36 K44 | tables unplaced |
| FILE | governance/check-registry.yaml | Layer 0 | K40 | no check inventory |
| FILE | scripts/run_checks.py | Layer 0 | K40 | no invoker |
| FILE | scripts/dbcore.py | Layer 1 | K35 K42 K43 | no connect, vocabulary, next_ref_id, writable set, walk, clock |
| FILE | scripts/db.py | Layer 2 | K35 | no verbs |
| FILE | scripts/research/emit_batch_sql.py | Layer 1 | K33 | write path broken |
| FILE | scripts/emit_data_migration.py | Layer 1 | K33 | write path broken |
| FILE | scripts/migrate_db.py | Layer 1 | K33 | write path broken |
| FILE | scripts/migrations/ | Layer 1 | K33 | no history |
| FILE | scripts/research/retrieval_log.py | Layer 2 | K16 K17 | no persisted bytes |
| FILE | scripts/assess/assess_cell.py | Layer 2 | K27 K28 | no computed state |
| FILE | scripts/render.py (new) | Layer 2 | K31 | no book surface |
| FILE | schemas/ (generated mirrors; modules with logic) | Layer 1 | K40 | mirror requirement unmet (A24) |
| FILE | .github/workflows/ci.yml | Layer 0 | K40 | no CI |
| FILE | .claude/hooks/ | Layer 0 | K40 | no command log, deps, contract hook |
| FILE | .claude/commands/ and .claude/agents/ | Layer 0 | K39 K40 | no session and adversarial procedure |
| FILE | skills/ (one procedure per stage) | Layer 2 | K12 K26 | research and synthesis procedures lost |
| FILE | retrieval-log/ | Layer 4 | K17 | bytes lost |
| FILE | data/guidebook.db | Layer 3 | K33 | no data |

**Compare by command** (re-run; figures are 2026-10-12):
```
f=workplan/pipeline-state-graph/IDEAL-GRAPH.md
grep -c '^CREATE TABLE' $f; grep -c '^CREATE VIEW' $f                      # ideal: 33, 5
for k in VERB GATE FILE; do grep -c "^| $k |" $f; done                       # ideal: 28, 12, 22
python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,count(*) from sqlite_master where type in ('table','view','trigger') and name not like 'sqlite_%' group by type\").fetchall())"   # live: 82 tables, 21 views, 1 trigger
python3 -c "import re;print(len(set(re.findall(r'add_parser\(\s*[\'\"]([a-z0-9-]+)',open('scripts/db.py').read()))))"   # live verbs: 72
python3 -c "import yaml;print(len(yaml.safe_load(open('governance/check-registry.yaml'))['checks']))"                   # live checks: 85
python3 - <<'PY'   # the ideal DDL loads
import re, sqlite3
s = open('workplan/pipeline-state-graph/IDEAL-GRAPH.md').read()
c = sqlite3.connect(':memory:'); c.executescript('\n'.join(re.findall(r'```sql\n(.*?)```', s, re.S)))
print(c.execute("select type, count(*) from sqlite_master group by type").fetchall())
PY
```
Code size: the workplan's §1 commands measure each area (`workplan/2026-10-12-simplification-workplan.md:15-27`). [GAP: I did not size the ideal's code; `db.py` with 28 verbs and refusals moved into CHECKs is smaller than 9,355 lines (`wc -l scripts/db.py`), by an amount I did not estimate.]

---

## 10. DELTA

| current object class | ideal | justified by |
|---|---|---|
| item layer (`items`, `item_*`, `term_item_links`, `room_items`, `spec_value_probes`, `probe_population_links`, `case_study_specs`, `economics_entry_specs`, `jurisdictional_values`, `item_audit_runs`) | DELETE | A13, C-019 |
| splinter `*_population*` tables, `case_study_outcomes`, `case_study_strategies`, `case_study_populations` | DELETE | A14, LED-132 |
| axes tables, `situations`, `slugs.serves_axes` | DELETE | A11 |
| `access_duration`, `access_stakes`, `life_stage_modifiers`, `rooms`, `lang_jur_map` | DELETE | no condition (U3) |
| four lens registries | KEEP, renamed | A12 |
| four crossing maps | MERGE → `lens_crossings` | A27 |
| `terms`, `base_parameters`, `parameter_declinations`, T1 `term_catalogue_origins` | MERGE → `terms` (+ warrant, broader) and `base_parameters` (+ `declined`) | A37, K06, K08 |
| `term_aliases` | KEEP frozen | K12 |
| JurisdictionCode enum, `jurisdiction_db_vocabulary` | NEW `jurisdictions` | A31, K35 |
| `TIER_MAP`, `evidence_sources.tier`, `adjudication_integrity` | NEW `tier_ladder` + `source_grades` | A08 |
| `search_executions` + `citation_mining`, `gap_mining`, `search_admissions`, `search_coverage`, `search_languages` | KEEP `search_executions` (+ lens FKs, `synthesis_id`); the rest derived or DELETE | A05, A33, A34 |
| `search_candidates`, `source_locators`, `research_code_leads`, `reference_stubs`, `external_root_registry` | MERGE → `search_candidates` | K12, LED-083 |
| manifests as sole home, `search_execution_artefacts`, `file_anchor`, `url_verification_runs`, `pipeline_runs`, resolution columns | NEW `retrievals` | K16, K17 |
| `evidence_sources` (97 columns today: `q "select count(*) from pragma_table_info('evidence_sources')"`) | KEEP lean; derived and copied columns retired (A26) | K34 |
| `source_slug_links` | DELETE (derived) | A35 |
| `case_studies`, `economics_entries`, `economics_entry_populations` | MERGE → sources + extractions | A36 |
| T1 `source_scans`, `v_scan_ledger` | NEW on `main` (T1 design) | K02 |
| `source_value_extractions`, `extraction_relations`, `term_adjudications`, `observed_terms` | KEEP (slug, method, `file_anchor`, `promoted_to_rdc_id` retired) | K01, K05, A04 |
| `evidence_population_match` | KEEP as `lens_matches` (four lens columns) | A12, LED-128 |
| `convergence_assessment`, `convergence_sources`, `connections`, `connection_targets`, `conflicts`, `reasoning_doc_citations`, `supersession_check`, `determination_gates`, evidence gaps | MERGE → `syntheses` + `synthesis_inputs` | A03, A14, A25 |
| `specification_extraction_links`, `specification_source_links` | MERGE → `synthesis_inputs` + `specification_syntheses`; source links DELETE | §4.4 |
| renderers, `tools/*.py`, `regenerate_derived.sh`, `parts/`, `site/`, `tools/*.html` | DELETE; NEW `scripts/render.py` | A01 |
| scheduled workflows and their scripts | DELETE | A02 |
| four walkers | DELETE; NEW `dbcore.walk` + `walkability` | §6 |
| `db.py` verbs (72) | 28 | §9 |
| registry checks (85) | 12 | §9 |
| hand-written Pydantic mirrors | generated | A24 |

**Prune in place or rebuild?** Prune in place, by forward migrations, in tooling PRs ordered along the spine. Evidence: every change above is a CREATE, an INSERT…SELECT, a DROP of a whole table, a rename, or a writer/reader retirement, all of which rule 3 allows as fix-forward; the only things a rebuild would add are physically dropping NULL-forward columns, which A26 makes harmless, and a shorter migration chain, whose replay costs about 1.7 s (`workplan/2026-10-12-simplification-workplan.md:47`, measured there, not by me). A re-baseline breaks the provenance chain: the migration ledger has 458 rows today (STATE-GRAPH.md §4) and attestations and session records name migration files. A re-baseline is an architecture amendment (§12 Q2).

**Where the ideal contradicts workplan v2:** §4 "cross-parameter synthesis: do not build" (A03 builds it); §4 slug × lens by logged query text (A05 uses FKs); step 0.2 lands T1 as built (A37 folds two of its tables); step 1.2 rebuilds `conflicts` (merged into `syntheses`); step 1.3 keeps `case_studies` (A36); Phase 3 evidence keeps a stored tier derived at `add-source` and promotes `adjudication_integrity` (A08 stores no tier, so the gate has nothing to check); step 1.6 keeps `medical_lens_integrity` (a CHECK replaces it); step 4.1 keeps `decline-parameter`, `add-icf-code`, `set-icf-title`, `add-population-icf-link` (merged into `add-parameter`, `add-lens-code`, `add-lens-crossing`); Phase 3 judgment removes the slug guard later (the ideal has no slug on extractions); the workplan keeps `gaps` for both uses (A25). Phases 0.1, 0.4, 1.1, 1.4, 1.5, 1.7, 1.8 and 3.R agree with the ideal.

---

## 11. COMPLIANCE

| # | requirement | source | how the ideal meets it | what shows a violation |
|---|---|---|---|---|
| R1 | five layers | `CLAUDE.md:229-233`; LED-140, LED-142 | L0: CLAUDE.md, registry, `run_checks.py`, 12 gates, hooks · L1: migrations, contracts, stage-map, `dbcore`, write path, generated mirrors · L2: verbs, `retrieval_log`, engine, renderer, skills · L3: rows · L4: bytes, `term_aliases`, catalogues. A refusal lives in its stage's writer (LED-143); no check lives in L2 (LED-146) | [cR1] |
| R2 | spine; stage ids in one home | `CLAUDE.md:240-243`; `pipeline-contract.yaml:13-14` | seven ids; every table placed in the stage-map | `claude_md_spine`; `walkability` reports UNMAPPED |
| R3 | data layer | `project-architecture-guidebook-v2.3.md:76-89` | DB is the single source; NNN and `data_` migrations; `migrate_db.py`; reproducibility; FKs enforced (`dbcore.py:165`) | `migration_reproducibility`; `PRAGMA foreign_key_check` |
| R4 | write path | `CLAUDE.md:284-287` | unchanged; retrieval rows enter through verbs; the engine emits SQL into it | the DB blob moves in a commit without a new `data_*.sql` |
| R5 | append-only; never drop an inserted column | `CLAUDE.md:85-98`, rule 5; v2.3:80-81 | forward migrations only; A26 | [cR5] |
| R6 | Pydantic mirrors | `CLAUDE.md:307-308`, `:460`; v2.3:86 | generated from the schema (A24) | a hand-written table class under `schemas/` |
| R7 | one check inventory; one invoker | `CLAUDE.md:510-511` | 12 gates, all registered; the commit-message job in `ci.yml` (`CLAUDE.md:75-77`) is an existing exception, kept | `grep -n 'scripts/audit' .github/workflows/*.yml` |
| R8 | a view is a caller; a cross-stage view is the pointer | `CLAUDE.md:99-105`, `:263-268` | five views, each named for what no FK carries | `schema_reference_audit`; `run_checks.py --selftest` |
| R9 | one home per fact | `CLAUDE.md:107-117` | copies removed: listed in §2 and §10 | not enforced; `walkability` catches un-keyed id columns only |
| R10 | numbers as commands | `CLAUDE.md:131-160` | every figure here has its command | the reader |
| R11 | derive or name the judge | `CLAUDE.md:161-207` | CHECK/FK vocabularies; `writable_tables`; judged stage-map | §8 commands |
| R12 | attestation; research and tooling apart | `CLAUDE.md:79-83`, `:209-222` | gates kept | those gates |
| R13 | no scheduled DB writes | `CLAUDE.md:89-97` | A02 | `grep -ln 'guidebook.db' .github/workflows/*.yml` lists more than `ci.yml` |
| R14 | centralized | O5 | §3.1 | the §3.1 commands return more than one home |
| R15 | pointers | O5, rule 5 | no copied columns; `v_render` computes `has_unverified_sources` | `walkability` unFK; review |
| R16 | injectable | O5 | §3.2 | [cR16] lists files other than `dbcore.py` |
| R17 | less hard-coded | O6 | §8 | §8 commands |
| R18 | contradictions among architecture documents | see right | followed: CLAUDE.md and the five-layer ruling over v2.3's three runtime layers (v2.3:13-25) and "code checks trump text rules" (v2.3:22, C-047); the registry over "add a blocking CI job" (v2.3:66-69, :125, C-030); git history for code and `_archived/` for reader content (`CLAUDE.md:499-500`, consistent with v2.3:131); Claude Code over the claude.ai surface (v2.3:9); LED-091 over item routes (`navigation-modes.md:60-64`, A29). Not normative: `schema-spec.md:3` ("Governs schema work: NO"), `schema-reconciliation.md:3` (OWNER-TO-DETERMINE). `pipeline-contract.yaml:2-3` says PROPOSED, ratified false, yet CLAUDE.md makes its `stages:` the single home; followed CLAUDE.md, since the stage list is the owner's (LED-124, CLM-027) | — |

```
# [cR1]  a gate importing Layer 2 code
grep -lnE 'from db import|^import db$' scripts/audit/*.py
# [cR5]  an edited or deleted migration
git diff --name-status origin/main -- scripts/migrations | grep -v '^A'
# [cR16] import-time bindings outside dbcore
grep -rlE '^[A-Z_]+ *= *.*(Path\(|os\.path\.|os\.environ)' scripts --include=*.py
```

---

## 12. OPEN QUESTIONS

Ranked. Each would rewrite doctrine text, is reserved to the owner by the record, or amends the architecture.

1. **Q1 C-004: does T3-grey alone stay `pending`?** The 2026-07-20 directive says all tiers may anchor, T3-grey/T6 weak; the methodology (EVI-326, EVI-338) and the engine say pending. Changing it rewrites ratified methodology. *Recommend:* provisional at ○, flagged, the same treatment Option A gives a T6-only cell (`decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md:44-50`) and consistent with LED-164; one engine branch changes.
2. **Q2 Re-baseline the migrations?** Architecture amendment (rule 3; v2.3:80-84). *Recommend:* no (§10); fallback is pruning with A26.
3. **Q3 Retire the Pydantic mirror requirement entirely?** Architecture amendment (`CLAUDE.md:307`, `:460`; v2.3:86; OD-7). *Recommend:* yes if a caller sweep finds no reader of the table mirrors; fallback is A24's generated mirrors.
4. **Q4 Run gates in-process with an injected connection?** Changes the registry's script-per-check form. *Recommend:* no; each gate keeps a three-line `main()` (§3.2).
5. **Q5 T1 extras (SES-063, owner-reserved):** *Recommend:* strike `term_catalogue_origins`, `extraction_follow_ups`, `raise-follow-up` in favour of A37; keep `source_scans`, `v_scan_ledger`, the sighting key and the lifecycle verbs.
6. **Q6 Doctrine text owed by the adjudications:** mission "teaches professional judgment" (C-001; recommend LED-024's wording) and two markers (C-002; recommend three, as the ledger reconciled); "seven tiers" and the national_fw mapping (C-006, C-009; recommend `tier_ladder` = `schemas/tier_derivation.py`'s table, prose corrected); `jurisdiction-philosophy.md` §2.3 (C-049; recommend amending it to the 2026-09-28 floor, leaving the Global South tension open as LED-193 ACTION 3 does); the band for a code value upgraded by research (LED-159; recommend the confirming study's band).
7. **Q7 Owner-reserved, outside the graph:** OQ-5, retire the decisions register (LED-191; recommend yes, it is not a pipeline object); the pilot extraction cap and review unit (LED-208; recommend no cap, one source per review).

---

## 13. LIMITS

[ASSUMPTION: O1–O8 are the owner's words as relayed; I did not see them in the ledger or a session record.]
[ASSUMPTION: A32 reads LED-201's "another slug" as the slug the reader worked under against the slugs the source was admitted under.]
[ASSUMPTION: "catalogue_version = max(parameter_id)" stays sound only while parameter ids are monotonic and never reissued (PIP-17).]
[GAP: how many current sources and extractions can be linked to persisted bytes was not measured; §5 says what follows for those that cannot.]
[GAP: code size of the ideal not estimated beyond `walk` (§4.1); the payload parsers were not counted.]
[GAP: which T1 objects are D8's approved items 1–5 was not verified; A37 states the target shape only.]
[GAP: readers of `schemas/*.py` table mirrors, of `term_aliases`, and of `weighting_profile` were not swept.]
[CONFIDENCE: medium — A12 (registry names), A23 (preliminary figures publishable) and A36 (economics) adjudicate questions the owner has left open or I read only in part.]
[CONFIDENCE: medium — `pipeline-contract.yaml` declares itself PROPOSED; PIP-* conditions are treated as binding through CLAUDE.md and the later owner rulings that restate them.]
[CONFIDENCE: low — the stage judgments in `stage-map.yaml` drive §4.4 and §6; a different placement of `source_value_extractions` (A07) changes which pairs report empty.]
[NULL: `references/project-standards.md` lines 300–512 were not re-read; the instrument records them as read through an agent.]
I did not run any check suite; the only commands run were the read-only queries and greps cited above, plus the §5 and §6 scratch tests against an in-memory database.
