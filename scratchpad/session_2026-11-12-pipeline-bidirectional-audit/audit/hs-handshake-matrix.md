# HS-1 — Handshake matrix (top-down requirements met against bottom-up capability)

_Handshake leg, 2026-11-12 (UTC). State examined: `git rev-parse --short HEAD` = `186defb` at the time of writing (TD and BU were written at `64c10e2`; `git diff --stat 64c10e2 HEAD -- . ':(exclude)transcripts' ':(exclude)scratchpad'` shows only `references/project-standards.md`, which gained the owner statements of 2026-11-12 at PS:5218-5270). `PRAGMA user_version` = 125. `sha256(data/guidebook.db)` = `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d` before and after (see `hs-adversarial-findings.md` §0)._

## 0. Verdict first

_Amended 2026-11-12 after an independent antagonist pass; what changed is in §9 (resolution record) and in `fa-corrections-for-suite.md`._

**The objective is not met in any of its four dimensions, and several rows below are marked CONTRADICTED (count them with the command under this table). The gravest is the engine's treatment of the lens: it contradicts the owner's answer on `ALL` (PS:4657) and the ledger's reading of the owner's answer to OR-1 (PS:4630, which the entry itself marks as the assistant's reading), and no gate tests it.**

| Dimension | Overall verdict | Shortest chain of blockers |
|---|---|---|
| **D1 omnidirectional** | **UNMET** | (1) nothing exists at render: every stage pair ending at render prints `NO PATH` (`python3 workplan/pipeline-state-graph/walkability.py`); (2) backward acts have no typed cause: `gaps` has no parameter, lens, jurisdiction or language column, `search_executions` has no `gap_id`, `extraction_follow_ups.reason` has one value, no row can hold a question about a rendered cell; (3) the stage-pair gate the owner ordered registered (PS:4731, PS:4761) is not in the registry, so a lost path goes unseen. |
| **D2 dynamic** | **PARTIAL** | One cell can be walked forward to a determination on a scratch copy in seconds. Blockers: (1) the cell is not a cell: the engine ignores the lens (REQ-077, HS-A02 CONTRADICTED); (2) cells determined on separate scratch copies of one base allocate the same ids (several cells on one copy do not, and capture as one delta; replay of two copies was not tested); (3) the cell key has no jurisdiction or language (owner decision, C-03); (4) a parameter defined after a source was read forces a re-read (REQ-098); (5) synthesis finds nothing on demand (REQ-100). |
| **D3 multilingual, multijurisdictional** | **UNMET**, CONTRADICTED at base | (1) a concept's identity is one English string (`terms.canonical_en NOT NULL`; owner schema decision open, PS:5194); (2) the jurisdiction vocabulary is a Python enum that disagrees with `lang_jur_map`; the in-scope set is in no table and `v_research_scope` owes what the owner scoped out; (3) no alias is attested by pointer; (4) the verbatim and name guards fail outside Latin script; (5) no unit conversion, no locale number parsing; (6) a provincial code is stored under its country; (7) render language is undefined (C-02). |
| **D4 verifiable** | **PARTIAL** | (1) zero live determinations: every specification gate is vacuous or examines retired history; (2) preconditions live in writers, the checks that would catch a bypass are advisory and already FAIL; (3) no gate tests the lens: a determination for the wrong lens failed only `test_db_integrity` C10, for unverified governing sources, and passed the three specification checks (§6); (4) synthesis and render have no enforced criterion; (5) an extraction does not point at the bytes it quotes. |

**Counts are commands, not literals** (rule 7a). Verdict distribution over every requirement row in this file:

```
grep -o -E '^\| (REQ-[0-9]{3}|HS-A[0-9]{2}) \| \*\*[A-Z]+\*\*' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-handshake-matrix.md | awk '{print $NF}' | sort | uniq -c
```

Boundary verdicts: the same command with `^\| B[0-9]+ ` in place of the requirement pattern.

## 0.1 Conventions

- **Verdicts** (exactly one per row): `MET` enforced and evidenced · `PARTIAL` exists, not enforced or one-directional · `UNMET` absent · `CONTRADICTED` current code or current data do the opposite · `UNPROVEN` cannot be determined, reason given.
- **Rule applied for legacy rows.** Where a writer now refuses what older rows did, the verdict is `PARTIAL` and the violating rows are counted by command. `CONTRADICTED` is kept for code that does the opposite today, or for a ruling the live tables as a whole negate.
- **Evidence tags.** `[V]` re-run or read by this leg · `[B]` verified by the BU leg, not re-run here · `[I]` inferred, basis named · `[U]` unverified.
- **Sources.** PS = `references/project-standards.md` (line numbers resolved with `grep -n -F` at `186defb`); PC = `governance/pipeline-contract.yaml`; BU §x = `bu-capability-inventory.md`; Qn = BU's query list §Z; `walk` = the walkability instrument's output.
- **REQ-101 to REQ-103** are the owner statements of 2026-11-12 on code quality, flexibility and dead ends, added in the final pass; their rows follow REQ-100 and their evidence is HS-3 §9.
- **REQ-097 to REQ-100** are the owner statements of 2026-11-12 (PS:5224, PS:5226, PS:5247, PS:5262), which the TD leg never saw. **HS-A01 to HS-A18** are requirements this leg found in the ledger span the TD leg did not read (`dossier/44`) or in rulings it cited without carrying.

---

## 1. Requirement handshake, REQ-001 to REQ-103

### 1.A Objective, spine, direction

| ID | Verdict | TD side | BU / HS side |
|---|---|---|---|
| REQ-001 | **UNMET** | "run in all directions at any stage … dynamically … across a multitude of languages and jurisdictions" (now PS:5222) | Composite of D1–D4 above. [V] |
| REQ-002 | **MET** | "you research slugs … render specifications"; "base is a stage" | `stages:` of PC lists the seven ids in the ruled order (`python3 -c "import yaml;print([s['id'] for s in yaml.safe_load(open('governance/pipeline-contract.yaml'))['stages']])"`) [V]. `claude_md_spine` is blocking per CLAUDE.md §3; its result [U]. |
| REQ-003 | **PARTIAL** | "A walk may re-enter any stage" (PS:1048-1049; ledger, not owner) | Typed re-entry exists for evidence → base and evidence → research only (BU §B.4) [B]; "database holds no marker for a return" (`skills/run-pipeline_SKILL.md:16`) [V]. |
| REQ-004 | **PARTIAL** | "Interrogate … flexibility of pipeline all directions as well as all gates, reads, writes, conditionals" (PS:4385) | Five checks are session-scoped; every precondition is forward; no gate has a backward entry. [B] |
| REQ-005 | **PARTIAL** | "walkability across all tables with references and ids" (relayed, IG:11) | `walk`: nine tables with no key in or out (`access_duration, access_stakes, data_migrations, decisions, life_stage_modifiers, research_code_leads, rooms, source_locators, weighting_profile`); five pairs `NO PATH`. [V] |
| REQ-006 | **UNMET** | "Yes, register it" (PS:4731); "registered as the stage-pair gate … fails when a stage pair has no path" (PS:4761) | The registry loaded as YAML holds no entry naming the instrument (`python3 -c "import yaml;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if 'walkab' in str(c)])"` → empty); the instrument exits 0 while printing `NO PATH` for five stage pairs (ten lines, two sections). BU never opened `workplan/`. [V] |
| REQ-007 | **PARTIAL** | "/run-pipeline (… a variant for processing evidence and beyond without research)" (PS:4947) | `add-source` needs no search row (BU §A.3) [B]; the admission edge is held by a session-scoped gate; `Q9`: two sources have none [V]. End-to-end cold run not exercised by any leg [U]. |
| REQ-008 | **PARTIAL** | memory note, "reworked at any stage" | Retire-in-place, amend verbs and `_refuse_if_resting` exist; stale detection is advisory and vacuous on zero live determinations. [B] |
| REQ-009 | **PARTIAL** | "interface where I can manually review and edit … and have it propagate" (PS:4580) | `scripts/generate/owner_browser_build.py` builds a read-only browser with a decision queue; no edit, no proposal path, no propagation. [B] |
| REQ-010 | **PARTIAL** | fan-out then fan-in (PS:1538-1540) | Fan-out is in the schema. Fan-in is one `convergence_id` per determination written in the same transaction; a synthesis row points at sources, not at judgment rows. [B] |
| REQ-011 | **MET** | "one evidence source may provide many rows of judgment" (PS:1845) | `judgment_handoff_shape` blocking, PASS on three schema invariants. [B] |
| REQ-012 | **CONTRADICTED** | "The junction is written by the downstream stage" (ledger reasoning, TD self-attack 3) | `walk` lists re-entrant keys held by the earlier stage: `search_candidates.resolved_ref_id` (7 non-NULL), `search_admissions.ref_id` (61), `base_parameters.direction_ref_id`, `term_aliases.observation_id`; `resolve-candidate` and `update-locator --status PROMOTED` rewrite a research row to record downstream use. [V] **The requirement is the weak party here, not the code** (see HS-2 F-08). |

### 1.B Pointers, traceability, verification

| ID | Verdict | TD side | BU / HS side |
|---|---|---|---|
| REQ-013 | **PARTIAL** | "point to another table cell than to rewrite" (PS:874-875) | Not enforced (CLAUDE.md rule 5). `specifications.governing_refs` still holds values on five retired rows beside `specification_source_links` (`select sum(governing_refs is not null) from specifications`); `claim_text` repeats a clause once per parameter it states. [V] |
| REQ-014 | **PARTIAL** | "call up information from any one" (PS:870-872) | Nine orphan tables; `gaps` reaches a parameter only through a determination. [V] |
| REQ-015 | **PARTIAL** | "Data relevant in one stage does not cross" (PS:898-903) | Link tables point; `evidence_sources.tier` is a judgment output on an evidence row ("Queued, not done", PS:1909-1914). [B] |
| REQ-016 | **PARTIAL** | memory note; ME:181 | PC criteria per stage: base 9, research 1, evidence 2, judgment 5, synthesis 1, specification 5, render 2; five carry `check: null`, among them synthesis's only one and one of render's two. No backward condition anywhere. [V] |
| REQ-017 | **UNMET** | "Yes, map views to a stage" (PS:4729) | `governance/stage-map.yaml` has no `views:` key (`python3 -c "import yaml;print(list(yaml.safe_load(open('governance/stage-map.yaml'))))"`); its header says "STILL OWED: the 20 views". [V] |
| REQ-018 | **PARTIAL** | "retire in place then" (PS:3540) | Determinations, parameters and sources retire; `delete-connection` and `unlink-admission` are hard deletes. [B] |
| REQ-019 | **MET** | PC:71-72 | `identifier_floor_audit` blocking, CLEAN over three floors. [B] Ids allocated on separate scratch copies of one base collide at replay (stress run `crosstopic.005`: `UNIQUE constraint failed: evidence_sources.ref_id`); that is the ordinary property of a scratch copy, not reissue against the permanent record (REQ-025 row; HS-3 IMP-41). |
| REQ-020 | **PARTIAL** | "every reader that could surface it filters on status" (PS:3575) | Views filter: each of the six determination views names `retired_at` in its body, and on a scratch copy with four live cells five of them return rows (the zero-row result on `main` alone proved nothing) [V]. `scripts/validate_evidence_state.py:246` reads every row with no `retired_at` filter [V]; `adjudication_integrity` reports "8 determination(s)" [B]. |
| REQ-021 | **PARTIAL** | PO:81-82; RC:188-189 | Zero-yield searches and readings are rows; `search_executions.absence_class` is NULL on every row, so the reason is not typed. [B] |
| REQ-022 | **PARTIAL** | "log where we retrieved from" (PS:5126) | `retrieval-log/*/manifest.jsonl` is a filesystem index. Of the live sources, most hold a record with a file on disk and fewer a derived text-extraction record; some hold nothing (command and figures in §5.2). `file_anchor` on 18 of 214 extractions (Q13). [V] |
| REQ-023 | **PARTIAL** | CLAUDE.md §5(c) | `metadata_integrity_audit` advisory, FAIL on 20 rows. [B] |
| REQ-024 | **PARTIAL** | PC:244-245 | Blocking `validate_evidence_state` PASS, `EXAMINED: 13`, "8 cells": all retired [V]. On a scratch copy with one live determination it passed with 27 links [V]. Its seeded-defect test exists and passes (`scripts/tests/test_validate_evidence_state_2_4.py`, "stated without a governing source caught") [V]. The blocking `test_db_integrity` criterion C10 is a live-row gate on the same links and exits 1 on every `provisional` scratch determination (parameter 3: four governing sources not `VERIFIED`; parameter 12: one, `REF-01016`) [V]. Not a schema constraint. |
| REQ-025 | **PARTIAL** | "you have to compute it" (PS:2690) | Engine computes; no hand-entry verb. The eight stored rows are `pilot-3`, the engine is `pilot-4`, `stale_determinations` reads only current-version rows, so nothing stored can be reproduced. Each single-cell run on a fresh copy allocated `specification_id` 9, and each `pending` one `GAP-103`; four cells run on one copy took ids 9 to 12 and gaps `GAP-103`, `GAP-104`. [V] |
| REQ-026 | **PARTIAL** | "we either have evidence or we do not" (PS:4834) | The engine reads only admitted sources. Both recorded directions carry `direction_ref_id` NULL (Q3): a fact the engine relies on has no source. [V] |

### 1.C Dynamic operation and the named backward edges

| ID | Verdict | TD side | BU / HS side |
|---|---|---|---|
| REQ-027 | **PARTIAL** | "we scan each source for any and all applicable parameters" (PS:4381) | `v_scan_ledger` derives the pair state; `scan_debt` advisory, `DEBT: 457` of `EXAMINED: 580`. [V] |
| REQ-028 | **PARTIAL** | PS:4985 | Observations and adjudications are typed (96 and 90); the equivalence test before minting compares English only. [V] |
| REQ-029 | **MET** | "add and expand parameter catalogue as required" (PS:4385) | `observe-term` → `adjudicate-term` → `add-term` → `add-parameter`, each refusing; ten active parameters, six `NAMES-NEW` adjudications, one declination. [V counts; B writers] |
| REQ-030 | **PARTIAL** | "figure from source filed by another slug allowed. skimmed values are not publishable" (PS:4396) | Engine gathers by parameter whatever the slug and leaves out skimmed rows [V]. The follow-up tag has one reason value and zero rows. [V] |
| REQ-031 | **MET** | RUL:305 | CHECK `COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL`; Q5: 7 parameter searches, 11 mining searches. [V] |
| REQ-032 | **PARTIAL** | "Every research slug gets cross-referenced against a population code, access need or ICF code" (PS:943) | Four lens columns with FKs exist on `search_executions`; all are NULL on all 203 rows (Q5). [V] |
| REQ-033 | **MET** | "we go evidence>judgment>synthesis" (PS:2002) | Typed and populated (Q37). [B] |
| REQ-034 | **PARTIAL** | PC:53-54 | `db._VALUE_BEARING_NAME` passes `最小幅`, `Mindestbreite`, `largeur minimale`, `幅１２００`, `١٢٠٠ مم` (live function, HS-2 §2). [V] |
| REQ-035 | **PARTIAL** | "Yes, read what we hold first" (PS:4683) | Convention; `scan_debt` lists the debt, nothing orders work by it. [I from BU §F] |
| REQ-036 | **PARTIAL** | "deferred is okay so long as it runs eventually" (PS:3737) | Deferral rows exist (`citation_mining.deferred_reason` on 13 of 38, Q17); no measure of age or obligation. [B] |
| REQ-037 | **PARTIAL** | "skimmed findings cue tools for a dedicated pass" (PS:4472) | Excluded by the engine; the cue is a printed command (`assess_cell.scan_command`), not a row. [V] |
| REQ-038 | **UNMET** | "provisional means that we have to go back and review the source again" (PS:4833) | No owed-re-read record; the engine uses `provisional` as an evidence-strength state (C-22 open). [I] |
| REQ-039 | **PARTIAL** | PS:4723 | `mined_ref_id` and `confirms` edges exist; nothing ties an absence row to the search run for it. [B] |
| REQ-040 | **PARTIAL** | PC:107; ME:117 | Engine wrote `GAP-103` for a pending cell [V]. `gaps` columns: `PRAGMA table_info(gaps)` shows no parameter, lens, jurisdiction or language [V]; `gap_mining` 0 rows; 106 of 110 gaps have no addressability (Q6) [V]. |
| REQ-041 | **PARTIAL** | "we set up the base and in turn we set up the research coverage" (PS:5088) | `v_coverage_priority` is slug × owed pair (not parameter); 19 owed pairs name a jurisdiction the enum refuses (Q32). [V] |
| REQ-042 | **UNMET** | PS:5076 | `rooms` has no key in or out and no reader; frozen by E8 (PS:5056). [V] |
| REQ-043 | **UNMET** | "cross referential analysis for table rows" (PS:4989) | `connections`, `connection_targets`, `conflicts` hold 0 rows and nothing computational reads them. [V counts] |
| REQ-044 | **PARTIAL** | PS:4987 | Evidence is stored with typed authors and locators; no renderer reads it; translation columns are never written. [B] |
| REQ-045 | **UNMET** | "Yes, derive it" (PS:4679) | No term-to-term or element-to-parameter pointer exists (`select name from sqlite_master` shows no relation table over `terms`). [V] |
| REQ-046 | **PARTIAL** | PS:4598-4600 | `governance/owner-browser.yaml` holds prompts with context; nothing stops a run in code. Its `answered` marks lag the ledger (OR-1c, HS-2 F-19). [V] |
| REQ-047 | **PARTIAL** | PS:3980 | `source_locators.status` `RETIRED` 13 (Q35); `processing_blocked_reason` exists and is never populated. [B] |
| REQ-048 | **PARTIAL** | PS:4985; RC:281 | Queries logged verbatim; `absence_class` empty. [B] |
| REQ-049 | **PARTIAL** | RC:79; PS:4719 | `citation_mining` 38 rows, 13 deferred; gate is session-scoped. [B] |
| REQ-050 | **PARTIAL** | RC:341-344 | 57 of 59 (Q9). [V] |
| REQ-051 | **PARTIAL** | RC:216; PS:4540 | Writer-only; 12 extractions sit on sources not `VERIFIED` (Q7). [V] |
| REQ-052 | **UNPROVEN** | RC:64 | No leg examined a check or data for pass order. |

### 1.D Languages and jurisdictions

| ID | Verdict | TD side | BU / HS side |
|---|---|---|---|
| REQ-053 | **PARTIAL** | PS:4985 | Searches exist in 13 languages after case folding; 2 of 106 slugs ever searched (Q14, Q34). [V] |
| REQ-054 | **UNMET** | "must work across all languages … P1+2+3" (PS:5011) | 0 of 2382 aliases carry an observation pointer (Q33); ICF, identity, need and room tables are English-only; the P-set is in no table. [V] |
| REQ-055 | **CONTRADICTED** | "without English bias" (PS:5019); "we are trying to avoid english BIAS" (PS:5206) | `terms.canonical_en NOT NULL`; `_near_terms` compares `canonical_en` and aliases `WHERE upper(language)='EN'` only; `_name_tokens` is `[a-z0-9]+` (live: `勾配` → empty set); `language` defaults to `'EN'`. [V] |
| REQ-056 | **UNMET** | "you obviously can have English words for these rows" (PS:5204) | No column separates a descriptive English label from an attested English form. [V DDL] |
| REQ-057 | **PARTIAL** | PS:5154, PS:5162 | `term_aliases (term_id, alias, language)` holds forms; the alias table and the adjudications disagree (`傾斜路`, `hellingbaan` under `TERM-001`; adjudicated to `TERM-089`, Q40). [V] |
| REQ-058 | **PARTIAL** | "not acceptable for the model to generate its own phrases" (PS:4713) | `add-alias` now refuses `TRANSLATION`; 996 such rows remain and no alias is attested by pointer (Q33). E4 (PS:5052) keeps them "as flagged search aids", and no typed flag exists. [V] |
| REQ-059 | **UNMET** | PS:5082; PS:4675 | No flag on an alias or on a search that used one; `terms_used` is a JSON array. [B] |
| REQ-060 | **UNMET** | "base grounds itself" (PS:5184) | `term_aliases` has no locator column; provenance is a marker in `notes`; the only attested route runs through evidence. [V DDL] |
| REQ-061 | **PARTIAL** | PS:5080; E1 | Writer admits a non-English name into `canonical_en`; 0 of 94 names are non-ASCII (Q39), so the branch is unexercised. [V] |
| REQ-062 | **PARTIAL** | "per parameter and bucket … associated language" (PS:4655) | The pair exists (`lang_jur_map`); coverage is per slug, not per parameter. [B] |
| REQ-063 | **UNMET** | standing order (PS:4295-4297); PS:4835 | No table holds the in-scope set; the enum admits codes outside it; nothing refuses. [V] |
| REQ-064 | **CONTRADICTED** | "Yes, scope them out for now" (PS:4673) | `select sum(scope_status is not null) from lang_jur_map` = 0 and `v_research_scope` returns all 70 pairs, the four scoped-out languages included. [V] |
| REQ-065 | **PARTIAL** | PS:3687; PC:48 | Enum of 36 members plus a blocking audit; `lang_jur_map` names 17 codes the enum lacks; `source_locators` and `term_aliases` are outside the failing set. [V] |
| REQ-066 | **UNPROVEN** | RC:127-128 | No check; `select lower(coalesce(lang_detected,'?'))<>'en', evidence_type, count(*) from evidence_sources group by 1,2` shows 3 non-English `grey` rows whose warrants no leg read. [V count; U warrant] |
| REQ-067 | **PARTIAL** | PS:4826 | `superseded_by_ref_id` on one source; `edition` and four `code_currency_*` columns never populated; `supersession_check` 0 rows. [B] |
| REQ-068 | **PARTIAL** | "Present both" (PS:3644); "convert and show both" (PS:4667) | One notation family (`%`, ratio) presents both. Length conversion is ruled and unbuilt: parameter 12 × `MOB` returns no value, "different units" [V]. |
| REQ-069 | **UNMET** | "easy comparison master table" (PS:4844) | No view or renderer; in-scope list in no table; `REF-01013` (Ontario Building Code) is stored as `CA`. [V] |
| REQ-070 | **UNMET** | E6 (PS:5054) | No table or column for a community's own designation. [V DDL] |
| REQ-071 | **PARTIAL** | TD assumption | Native titles are stored; `evidence_sources.language` NULL on every row, `lang_detected` mixed case and NULL on eight; six translation columns unwritten; CJK given names truncated in `v_evidence_authors`. [B; V for Q34] |

### 1.E Lenses and the key

| ID | Verdict | TD side | BU / HS side |
|---|---|---|---|
| REQ-072 | **MET** | PS:1317; PS:2554-2556 | CHECK "at least one lens" and a partial unique index over live rows. [B; V by seven scratch runs] |
| REQ-073 | **UNMET** | "never be limited to only one lens" (PS:4614) | `select sum(identity_code is not null), sum(icf_code is not null), sum(needs_code is not null), count(*) from source_value_extractions` → 212, 1, 3 of 214; every stored determination carries identity only. [V] |
| REQ-074 | **CONTRADICTED** | "Do not store table rows … for when the parameter is not relevant" (PS:4614) | Engine wrote `provisional ○` for ramp gradient × `DEAF`, although no figure of parameter 3 carries `DEAF`; it stores a row for any lens named and tests nothing about relevance [V]. That no tagged figure means "not relevant" is the ledger's unratified assumption (PS:4630), so the reading of this run as a breach of the owner's sentence is [I]. The first version also cited parameter 7 × `DEAF`; parameter 7 is reverberation time, which concerns Deaf and hard-of-hearing people, and that run is withdrawn as evidence here. |
| REQ-075 | **UNMET** | "we include the medical model too" (PS:1935) | `base_taxonomy_medical` 0 rows, so the lens cannot be offered; `medical_lens_integrity` examines 0. [V; B] |
| REQ-076 | **UNMET** | "link table" (PS:4926) | One column per model on extraction and determination; no link table. [V DDL] |
| REQ-077 | **CONTRADICTED** | "No, ALL reaches only an ALL determination" (PS:4657) | Scratch run parameter 3 × `ALL`: 35 governing extractions, all tagged `MOB`. `gather_sources(conn, parameter_id)` takes no lens (`scripts/assess/assess_cell.py:255`). [V] |

### 1.F Stage content

| ID | Verdict | TD side | BU / HS side |
|---|---|---|---|
| REQ-078 | **PARTIAL** | PS:1885; RC:270 | Tier is derived at `add-source` and stored on the evidence row; `evidence_population_match.target_population` is text, held to the registry by the writer only. [B] |
| REQ-079 | **PARTIAL** | "require a full-scope scan" (PS:4669) | Writer refuses now; `verified_scan_integrity` advisory, `FAIL: 140 (row, class) pair(s) across 212`. [V] |
| REQ-080 | **PARTIAL** | PC:172-173; ME:132 | `convergence-independence` is `check: null`; `root_id` unwritable (empty registry with no writer); `v_value_independence` returns one row. [V] |
| REQ-081 | **PARTIAL** | "most accommodating/gentle/dignified" (PS:4991) | Value composed from the direction over the claims the engine can parse: 11 of 35 for parameter 3 (BU §C.2) [B]; two of ten parameters have a direction, neither sourced [V]. |
| REQ-082 | **MET** | PS:4997; PS:4873 | Schema CHECK; scratch run 12 × `MOB`: `provisional ○`, `T4-6-only(regulatory_stratum_only)`. [V] |
| REQ-083 | **UNMET** | "coming from database directly" (PS:4840) | No renderer; `ls site specs` fails; `scripts/generate/` holds no page generator. The negative half (no committed render) holds. [V] |
| REQ-084 | **UNMET** | "the render table" (PS:4729) | No such table; OW-1b and OW-1c unanswered. [V] |
| REQ-085 | **UNMET** | PS:4888; PS:4993 | No surface. [V] |
| REQ-086 | **UNMET** | PS:4841; PS:4843 | `weighting_profile` (5 rows) has no reader. [B] |
| REQ-087 | **UNMET** | PC:285 | `check: null`; no surface. [V] |
| REQ-088 | **UNMET** | PS:4847 | No surface to test. [V] |
| REQ-089 | **PARTIAL** | PS:26 | Current engine writes a marker; `select sum(marker is not null) from specifications` = 0 on the stored rows; CHECK permits a marker only on `stated`/`provisional` and does not require one. [V] |

### 1.G Constraints

| ID | Verdict | TD side | BU / HS side |
|---|---|---|---|
| REQ-090 | **MET** | RC:351 | `dbcore.connect` and `assess_cell` refuse the canonical file; hash unchanged across this leg's seven engine runs. [V] |
| REQ-091 | **PARTIAL** | PC:332; CLAUDE.md rule 10 | Advisory check, behaviour [U]. |
| REQ-092 | **PARTIAL** | "we do NOT want to have data joined in cells" (PS:4963) | `claimed_unit` carries conditions in prose; `terms_used`, `value_notations`, `tier_weights`, `gap_mining` hold JSON; 29 `notes` carry a `VERBATIM-EXEMPT` marker (Q13). [V] |
| REQ-093 | **PARTIAL** | CLAUDE.md rule 8 | `JurisdictionCode` is a curated list beside the table it should describe; `NOTATION_FAMILIES` is a list in code. [V] |
| REQ-094 | **PARTIAL** | PS:4979 | 9 passes, 193 findings; the recording check is advisory and session-scoped. [V counts] |
| REQ-095 | **UNPROVEN** | PC:301; PC:321 | No leg examined an adherence record or a recheck at a boundary. |
| REQ-096 | **PARTIAL** | PC:232; correct wording at PS:608: "Opus-class or above, which includes Fable-class" | `check: null`; no code tests the authoring model; no table or column is named `best_practice_synthesis`. [B] |

### 1.H Owner statements of 2026-11-12

| ID | Verdict | Owner side (verbatim source) | BU / HS side |
|---|---|---|---|
| REQ-097 | **PARTIAL** | "robust base for languages/jurisdictions/terms/etc … dynamically derive/define new parameters … find linkages and equivalencies and clauses in order to group" (PS:5224) | Parameter definition is typed and works (REQ-029). The base is not robust (REQ-054 to REQ-065). A clause is not a unit: it exists as `loc_*` columns and a repeated `claim_text` on judgment rows (`locator_scheme`: section 153, page 17, NULL 44). No equivalence group, no term-to-term pointer. §5.1. [V] |
| REQ-098 | **UNMET** | "whenever we read a source … derive all information relevant to all parameters … so that we don't have to repeatedly read a source" (PS:5226) | 18 scans over 11 sources, every one `method='pre-screen'`, none `full-read`, `open_pass_done` 0 on all; 457 of 580 pairs unread; a parameter added tomorrow makes every existing scan stale for it by rule (`catalogue_version >= parameter_id`), and what text is held for a later sweep is not established (§5.2). [V] |
| REQ-099 | **UNMET** | "approach parameters from a higher level abstract vantage … lose commonality and therefore can't unify then specify" (PS:5247) | `base_parameters` is flat (`merged_into` is its only self-pointer); no parameter family, no dimension or unit model; conditions sit in `claimed_unit` prose, which is why 24 of 35 governing claims do not compose. §5.3. [V DDL; B for the 24] |
| REQ-100 | **UNMET** | "synthesis needs to be very dynamic in finding equivalencies/adjacencies/similarities/commonalities" (PS:5262) | Nothing finds: 0 rows in `connections`, `connection_targets`, `conflicts`; no finder code was found [I: a search cannot establish absence]; convergence is written only inside the determination engine; `connection_type` has no equivalence, adjacency or similarity value; `skills/connection-discovery_SKILL.md` contains none of the four words; `cross-population-conflict-mapper` teaches seven retired identity codes. §5.4. [V] |
| REQ-101 | **PARTIAL** | "ensure the overall code is efficient and centralized and clean" (`grep -n -F 'efficient and centralized and clean' references/project-standards.md`) | Efficient: met as measured (a verb and a determination well under a second, a rebuild about two seconds; timings in `stress/results2/`, `stress/results3/`; not measured at larger row counts). Centralized: helpers defined in two files (`next_gap_id`, `_is_tracked`, `db_path`, `columns`, `_jlist`, `glob_to_re`; command in workplan task T-041), jurisdictions and notation families as lists in code; the `argparse` value lists are already read from the schema (`derived_not_curated_audit` CLEAN). Clean: `skill_vocabulary_audit` FAIL, a no-op verb that exits 0, a documented command that does not run, typed counts in the registry. [V] HS-3 §9. |
| REQ-102 | **PARTIAL** | "pipeline must be flexible", glossed by the owner: "pipeline must not have hard coded behaviours" (`grep -n -F 'must not have hard coded behaviours' references/project-standards.md`). What counts as hard-coded is not ruled; reading used: [ASSUMPTION] code edited for something that is data, or in more than one place | Data-driven and kept: the check registry, vocabularies from the column's CHECK, the derived capture set, one home for stage ids. Hard-coded: jurisdictions (an enum that disagrees with `lang_jur_map`), research scope (in no table), lens selection (ignored by the engine), units, what may be a parameter. No test adds a language, jurisdiction, term and parameter by data alone (AT-104, red). [V] HS-3 §9.4. |
| REQ-103 | **UNMET** | "or dead ends or whatever" (same ledger entry). What counts as a dead end is not ruled; reading used: [ASSUMPTION] a row, state, path, stage or refusal with no sanctioned way onward, back or out; a deliberate refusal is not one | Structural: every stage pair ending at render has no path; `external_root_registry` and the base tables `lang_jur_map`, `base_taxonomy_identity` have no writer; the medical lens is empty and its two crossing maps are unwritable (CLAUDE.md §4 derivation). State: a retired determination with no successor pointer; a `pending` row for a lens nothing will fill. Operational: about half of the distinct refusal messages in the stress logs name no next action (command in workplan task T-043; a heuristic, [I]). Reader and process: no carrier for a question about a cell; skills that name deleted structures. [V] HS-3 §9.5. |

---

## 2. Requirements the TD leg did not carry (HS-A series)

Each was found in `dossier/44` or in a ruling TD cited without carrying. Class per TD's own vocabulary.

| ID | Verdict | Requirement and warrant | Evidence |
|---|---|---|---|
| HS-A01 | **CONTRADICTED** | `MOB` is split into `AMB` and `WHEEL`; "do not write new `MOB` rows" (OWNER, PS:1184-1230, PS:1291-1296, "not to be relitigated") | `base_taxonomy_identity` holds `MOB` active and neither new code; 170 of 214 extractions, every population grade but two, and all eight determinations are on `MOB` (`select identity_code, count(*) from source_value_extractions group by 1`). No later ledger line mentions either code (`grep -n -E '\bAMB\b|\bWHEEL\b' references/project-standards.md`), and `grep -rn` over `sessions decisions governance skills scripts/migrations` finds no execution or withdrawal [V for the registry and the rows; I for "not withdrawn": a withdrawal worded without the code strings would be invisible, and `sessions/` was searched, not read]. |
| HS-A02 | **CONTRADICTED** | A figure reaches a determination only through the lens tags written on it (LEDGER reading of the owner's OR-1 answer, PS:4630; D-0184 ACTIVE) | `gather_sources` filters on `parameter_id` alone; ramp gradient × `DEAF`, × `BLIND`, × `ALL` and × need `A-REACH` each return the same 27 sources and 35 `MOB`-tagged governing rows. [V] |
| HS-A03 | **UNMET** | "Ensure that medical gets filled out" (OWNER, PS:2863); populate by correspondence from the registries held (PS:3004-3062) | `base_taxonomy_medical`, `identity_medical_map`, `icf_medical_map`: 0 rows. Named again as open at PS:5028 item 5. [V] |
| HS-A04 | **UNMET** | A registry of research targets, "prompts for research to target" (OWNER, PS:1965-1969; D-0172 ACTIVE) | No table; `search_executions.engine` is free text with 21 distinct values. [V] |
| HS-A05 | **UNMET** | `base_building` as three tables: building types, room types, elements (OWNER, PS:2056-2057; "5 is three", PS:2419; D-0171 ACTIVE) | Only `rooms` exists; frozen by E8. [V] |
| HS-A06 | **CONTRADICTED** | "always assume I Ratify if I merge it"; stale `PROPOSED` text is flipped (OWNER, PS:585) | PC header reads `status: PROPOSED`, `ratified: false`; its DR reads "ACCEPTED (doctrine) — owner ratification 'Yes, ratify ALL recent work', 2026-07-21" (`decisions/DR-2026-07-13-pipeline-contract.md:3`). [V] |
| HS-A07 | **PARTIAL** | Facts about the repository are established from its structure, never from a text-search hit count (RULE 2026-08-22, PS:663) | BU's "no reader" lists (§G.3, §G.5) are grep-derived and marked VERIFIED. HS-2 F-09. [V] |
| HS-A08 | **UNPROVEN** | Symmetric disclosure; no scope narrowing in restatement (RULES 2026-07-25, PS:594, PS:600; level 1 by their own text) | No surface or synthesis prose exists to test them on. |
| HS-A09 | **UNMET** | A rendered document is gated against the database and in a browser (RULE 2026-07-25, PS:588) | `ls scripts/audit/check_rendered_docs.py scripts/audit/render_audit.js` fails for both; the render apparatus was deleted on the owner's ruling (`workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §1). [V] |
| HS-A10 | **UNMET** | A conflict between groups is resolved by harm asymmetry, or by broadest benefit for a values conflict, with a Person-Mode hand-off (RULE PS:210; `governance/evidence-methodology.md` §3.3, §4, CANONICAL) | `conflicts` 0 rows [V]; `grep -c -i harm scripts/assess/assess_cell.py` returns 0 [V for that file; I for "the engine applies no such rule"]. |
| HS-A11 | **UNMET** | Freshness windows per tier and standards currency (A9 `time-model.md` §4.3, CANONICAL, PS:539; JP §3) | `FRESHNESS_WINDOWS` exists in `schemas/temporal.py`; `code_currency_*` and `edition` never populated; whether any registered check reads live sources is [U]. A time-driven re-entry (a determination goes stale because a code was reissued) is unrepresented. |
| HS-A12 | **UNMET** | A determination may be conditional on climate or cultural context (RULES PS:372-381; `specifications.cultural_claim_anchor`) | Column never populated; engine has no such input. Refutes TD's "nothing in the prose says … whether a determination varies by jurisdiction" in part (HS-2 F-05). [V] |
| HS-A13 | **UNPROVEN** | Saturation is the stopping rule for a region (LEDGER, PS:2034) | `search_executions.saturation_signal` exists; no leg examined its use. |
| HS-A14 | **PARTIAL** | An alias declares its provenance; a relation between concepts is a pointer, never a shared alias string (RULES 2026-07-25, PS:624, PS:612) | `alias_provenance_audit` blocking, PASS with 880 grandfathered [B]; relations are `NARROWER`/`BROADER` alias strings plus prose in `scope_note`, not pointers [V DDL]. |
| HS-A15 | **UNPROVEN** | Downstream of evidence a row carries a reference and a grouping key, nothing else about the source (OWNER, PS:767) | Not measured by any leg for the current schema. |
| HS-A16 | **PARTIAL** | "as little infrastructure and code as possible"; "the less hard coded, the better"; "centralized … pointers" (relayed O1, O4–O6, IG:11) | Enum, notation list and capture-set regex are hard-coded (REQ-093). [V] |
| HS-A17 | **UNPROVEN** | Norwegian is split into Bokmål and Nynorsk only where an instrument is published in both; other official languages stay out (E7, PS:5055) | `lang_jur_map` holds `NO` only; whether a held instrument exists in both was not checked. |
| HS-A18 | **PARTIAL** | A determination is tagged with a design scale (Universal, Population, Person), and a range carries a Person-Mode hand-off (RULES PS:170-221; PC render entry "determinations tagged with design_scale") | `design_scale` CHECK exists; the engine wrote `universal` for a `MOB`, a `DEAF` and an `A-REACH` cell and `population` for a pending one [V]. No leg treated the mode as part of a request. |

---

## 3. Boundary handshake (TD §3.8 against BU §B)

| # | Verdict | Boundary | Evidence |
|---|---|---|---|
| B1 | **PARTIAL** | base → research | Subject and lens resolve by FK; the pair is not a key and the scope is unrecorded (REQ-063/064). |
| B2 | **PARTIAL** | research → evidence | Typed junction; no schema tie; session-scoped gate; 57 of 59. |
| B3 | **PARTIAL** | evidence → judgment | Preconditions writer-only; Q8: 105 extractions with no covering reading. |
| B4 | **UNMET** | judgment → synthesis | Convergence is written only by the determination engine and points at sources. |
| B5 | **PARTIAL** | synthesis → specification | Computed and linked in one transaction; contract entries circular (C-11). |
| B6 | **UNMET** | specification → render | Nothing. |
| B7 | **PARTIAL** | evidence → research (mining) | `mined_ref_id` typed (11 rows); `citation_mining.global_ref_id` is text. |
| B8 | **PARTIAL** | judgment → research (absence) | No pointer from the finding to the search. |
| B9 | **UNMET** | synthesis → research | `conflicts.gap_id`, 0 rows; otherwise prose. |
| B10 | **PARTIAL** | specification → research (gap) | Determination → gap is typed; gap → cell and search → gap are not. |
| B11 | **PARTIAL** | specification → evidence/judgment | One follow-up reason, 0 rows; one open determination gate. |
| B12 | **MET** | evidence/judgment → base | Typed chain, exercised. |
| B13 | **UNMET** | research → base (attested form with locator) | No locator columns; the only route is through evidence. |
| B14 | **PARTIAL** | base → evidence/judgment (catalogue grew) | `v_scan_ledger` derives the debt; nothing holds the text to sweep (REQ-098). |
| B15 | **UNMET** | evidence → render | Nothing. |
| B16 | **UNMET** | judgment → render | Nothing. |
| B17 | **UNMET** | owner/render → any table | Browser is read-only. |

Edges TD could not warrant (TD §3.8 tail): synthesis → judgment, specification → synthesis, render → specification, render → research. All **UNMET** as acts; specification → synthesis is traversable by `convergence_id` only.

---

## 4. Stage-by-stage synthesis

| Stage | Can enter cold | Leaves by pointer | Enforced | Verdict in one line |
|---|---|---|---|---|
| base | by verb for ICF, medical, terms (from an observation or a catalogue), parameters; by hand SQL for languages, pairs, identities, needs, slugs; by code edit for jurisdictions | FK targets for everything | nine criteria, one null | The most-used stage is the least writable; English is structural. |
| research | yes | search → subject, lens, mined source | one criterion | Works for slug searches; lens-scoped, gap-driven and target-keyed research are unexercised or absent. |
| evidence | yes, with no search row | source → admission; reading → file hash | two criteria | Admission is sound; reading is thin (no `full-read` scan exists) and nothing a clause could be pointed at. |
| judgment | onto a verified, read source and an active parameter | extraction → source, parameter, lens; relations between extractions | five criteria, two null | The strongest stage; its rows carry joined cells and one lens. |
| synthesis | no, except inside the engine | convergence → sources | one criterion, null | Not a separable stage; finds nothing. |
| specification | yes; writes | links to every extraction of the parameter, graded | five criteria over zero live rows | Computes reproducibly for the wrong population. |
| render | no | none | none | Deleted on ruling; replacement undesigned beyond a draft contract. |

---

## 5. The four statements of 2026-11-12, met against the code

### 5.1 REQ-097 — base, dynamic parameters, linkages, equivalencies, clauses

- **Parameters, dynamically: present.** Observation → adjudication → term → parameter, with decline, revoke, merge and retire verbs. [B; counts V]
- **Clause as a unit: absent.** A clause is known only as attributes of a judgment row: `source_section`, fifteen `loc_*` columns with `locator_scheme` (`select locator_scheme, count(*) from source_value_extractions group by 1`), and the verbatim `claim_text`. A clause stating three parameters is three rows repeating its text. `observed_terms.locator` is free text. Nothing can point at a clause, so an equivalence group over clauses of several jurisdictions has nothing to hold.
- **Equivalence: at term level only.** `term_adjudications` (`NAMES-EXISTING` 46) ties a source's phrase to a term; `term_aliases` holds forms without attestation. No equivalence of values (1:12 and 8.33 %) beyond one notation family; none of clauses; none of parameters across instruments.
- **Linkage: stored kinds exist, unread.** `extraction_relations` (57 edges, source-stated relations only); `connections`/`connection_targets` (0 rows).
- **What a language-neutral, jurisdiction-keyed clause unit needs** [I]: an evidence-stage row per clause (source, typed locator, verbatim text in the source's language, the file hash it was read from), which extractions, observations and relations point at. It is a fact about the document, the same act as an observation (PS:2004-2007), so it is not a second judgment object and leaves "the judgment object is the canonical parameter" untouched. Holding retrieved copies of standards is ruled acceptable (PS:5110-5112); putting every clause's text into a database the site reads, and showing it, is not ruled and is the owner's (licensing).

### 5.2 REQ-098 — read once, miss nothing

Measured (re-run, do not trust):

```
python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select status,count(*) from v_scan_ledger group by 1').fetchall());print(c.execute('select mode,text_scope,method,open_pass_done,count(*),count(distinct ref_id) from source_scans group by 1,2,3,4').fetchall())"
python3 scripts/audit/scan_debt.py | head -3
```

- No source has a `full-read` scan; no scan has its open pass done. "Covered" in the owner's sense (read, extracted, verified, PS:4832) is true of nothing by the ledger's own columns.
- **Catalogue growth is detected, not served.** `v_scan_ledger` counts a catalogue scan as covering a parameter only when `catalogue_version >= parameter_id`, so a parameter minted tomorrow shows every source as owed. That is correct bookkeeping and it means a re-read: nothing retains what the earlier reading saw beyond the rows it chose to write.
- **What is retained** (live sources, command in HS-2 §2.7; re-run, do not trust): an artefact on disk for 48 of 58; a derived `text-extraction` or `extraction` record for 20 (three more hold only page renders or a bibliography extract); nothing for 10. Some artefacts are text as retrieved (`.txt`, `.html`, `.json`, `.xml`), and a `.json` is often an index record, not the source. Which sources hold their full text in a form a later sweep could read is therefore not established. The first version's "23 hold a text layer" counted any derived record and was wrong (FA-11). `.gitignore:53` already keeps one session's payloads out of the repository under the 2026-11-06 ruling (log by location, PS:5126), so a fresh clone holds less.
- **What "read once" requires of schema and writers** [I]: (a) a full-scope reading that inventories every quantitative or normative clause, catalogue or not (the open pass, as rows); (b) that inventory, or the text layer, retained in a form a later sweep can query without re-retrieval; (c) a scan keyed to the parameter set it covered, so a later parameter is matched against the inventory rather than against the document; (d) a blocking check, once sources are read, that no determination rests on a source without (a). Whether (b) is retained text in the repository, retained clause rows, or a recorded re-read is the owner's (OD-23 in HS-3).

### 5.3 REQ-099 — abstract vantage, unify then specify

- **`base_parameters` is flat.** Columns: `PRAGMA table_info(base_parameters)`; the only self-reference is `merged_into`. `terms.domain` is a category label. `NARROWER`/`BROADER` are alias strings, not pointers between terms.
- **The only level between a clause and a parameter is the extraction row**, qualified by `setting`, `device_class`, `measurement_paradigm`, `comparator`, and `condition_on` edges (31).
- **Why unification fails today** [B for the figures]: conditions are written into `claimed_unit` (32 distinct strings for parameter 3, Q23), so the engine composes 11 of 35 governing claims; there is no dimension or unit model, so parameter 12 yields no value across `mm`, `cm`, `m`.
- **The trap both ways.** Too fine: every conditional clause becomes its own parameter and nothing converges. Too coarse: a single "ramp gradient" value hides that one instrument relaxes it for short rises and another does not, which is the divergence the book exists to show (PS:4626; DR-2026-08-19 §7). The ledger's own ACTION is to keep clause-level extractions and reach them by pointer (PS:5254). That is satisfied by an abstract parameter plus typed conditions on its extractions, with a family pointer above it; it is not satisfied by merging rows.
- **Effect on the scan contract** [I]: a coarser parameter set means fewer pairs to read; a split or a new parent mints ids above every scan's `catalogue_version`, so every completed scan becomes stale for the new rows although the text was read. A hierarchy needs a stated inheritance rule for scans, or the clause inventory of §5.2, or each change of grain is a re-read of the corpus.

### 5.4 REQ-100 — synthesis that finds

| Relation | Meaning | Typed, pointer-only home today | Finder today |
|---|---|---|---|
| equivalence | the same thing in other words, units, jurisdictions | terms: adjudications and aliases; values: one notation family; clauses, parameters: none | none |
| adjacency | neighbouring parameters that constrain one another | `connection_targets(parameter_id | extraction_id)` under `connection_type='CROSS-PARAMETER'`, 0 rows; 17 cross-parameter `extraction_relations` edges stated by sources | none; the connection-discovery skill is a prompt |
| similarity, commonality | shared structure across clauses that licenses an abstraction | none | none |
| conflict | groups pulled opposite ways on one parameter | `conflicts` (identity pair only, 0 rows) | `cross-population-conflict-mapper`, which teaches retired codes |
| convergence | independent roots agree | `convergence_assessment` + `convergence_sources`, engine-written with the determination | the engine, for one cell at a time |

Nothing runs on demand for a request; `connections.filed_in` is `NOT NULL REFERENCES slugs`, so a relation must still be filed under a topic container; and nothing downstream reads a connection. "Unify then specify" therefore has no unify step.

---

## 6. Direction matrix (7 × 7), handshake reading

Rows = stage entered; columns = stage reached. `M` = every write on the path has a refusing writer · `m` = by hand SQL, code edit, JSON or prose link · `t` = traversable by typed pointer, no act representable · `–` = nothing. `*` = unexercised on live data (0 rows of what it produces), which under CLAUDE.md rule 4 is unproven, not clean. Source: BU §H, corrected by this leg's runs.

| enter ↓ / reach → | base | research | evidence | judgment | synthesis | specification | render |
|---|---|---|---|---|---|---|---|
| base | M/m | M | M | M | M (engine) | M | – |
| research | t | M | M | M | M | M | – |
| evidence | M | M | M | M | M | M | – |
| judgment | M | m* | M* (one reason) | M | M*, unread | M | – |
| synthesis | t | m* | t | t (sources only) | not enterable | M (same act) | – |
| specification | t | m (gap untyped) | t* | t*, M* (gate) | t* | M (retire, re-run) | – |
| render | – | – | – | – | – | – | – |

Reading against the objective:
- **Forward:** complete to specification, absent to render (six of six cells `–`).
- **Backward acts:** representable in rows at four cells (evidence → base, evidence → research, judgment → evidence narrowly, specification → specification); half-representable at three (through an untyped gap); absent at the rest.
- **Lateral:** slug and parameter moves exist; lens-to-lens is a re-run on identical evidence (HS-A02); jurisdiction-to-jurisdiction and language-to-language have no typed form downstream of judgment.
- **No gate tests the lens.** A determination for ramp gradient × Deaf people, governed by 35 figures tagged `MOB` (T4–T6 code provisions, none device-scoped, none mentioning a wheelchair), passed `validate_evidence_state` (PASS), `derivation_handshake_integrity` (CLEAN) and `extraction_follow_up_audit` (PASS) on a scratch copy. The blocking `test_db_integrity` exits 1 on that copy at criterion C10, because four governing sources are not `VERIFIED`; the same failure occurs for the correct lens (3 × `MOB`), so it is not a test of the lens. [V] The first version said the determination passed every gate; it had run three. (FA-02)

---

## 7. ORPHAN — capability no requirement asks for (CLAUDE.md §8)

Evidence is BU §G unless marked; "requirement" means REQ-001 to REQ-100 and HS-A01 to HS-A18.

| Object | Why orphan | Disposition to consider |
|---|---|---|
| `gap_mining` (0 rows, JSON columns), `add-gap-mining`, `unmined-gaps`, `update-gap-addressability`, `gap_mining_audit` | REQ-040 is better served by a `gap_id` on the search; no committed migration INSERTs into the table [V]. It has callers: a registered check, two test files, the graph topology list, a live skill (`git grep -l gap_mining -- scripts schemas governance skills .claude ':(exclude)scripts/migrations'`) | candidate only, behind a caller sweep (HS-3 IMP-05) |
| `reasoning_doc_citations`, `source_value_extractions.promoted_to_rdc_id` | 0 rows, no writer; but named by `schemas/directness.py`, two audit scripts and governance files (`git grep -l reasoning_doc_citations -- scripts schemas governance skills .claude`) | candidate only, behind a caller sweep |
| `connections.opus_reviewed`, `connections.filed_in NOT NULL` | `opus_reviewed` is written 0 (`scripts/db.py:2947`) and named in `governance/conceptual-model.md:122`; `filed_in` is a container key | reshape with REQ-100, after a caller sweep |
| `specifications.not_applicable_rationale`, `governing_refs`, `confidence_*` | superseded by REQ-074 and by the link tables | tombstone |
| `evidence_sources.bpc_shorthand`, `bpc_note`, `search_queries_used`, `derivation_chain`, `prior_expectation`; `slugs.sl_path`, `bpc_path` | prior-version file architecture | tombstone; `NOT NULL` on the two slug columns blocks a slug writer |
| `access_duration`, `access_stakes`, `life_stage_modifiers` | no key, no reader; E9 (PS:5057) mentions `typical_stakes` for needs, so `access_stakes` may gain a reader | hold `access_stakes`; the other two have none |
| `case_studies` (0), `economics_entries` (1), `research_code_leads` (96, no reader), their verbs | outside the objective; in scope of other volumes | not this programme's to delete; name the reader or leave |
| 18 skill files failing `skill_vocabulary_audit` | name values, columns or codes the repository holds nowhere | correct the tokens (HS-3 IMP-36) |

Not orphan although unread: `weighting_profile` (REQ-086), `rooms` (REQ-042, frozen), `external_root_registry` (REQ-080), `supersession_check` (REQ-067), `connections`, `conflicts` (REQ-043, REQ-100).

Withdrawn from this table after the antagonist pass: `assess_cell --slug` (it is validated and written into each gap, `scripts/assess/assess_cell.py:1963-1969`, `2224-2228`); `v_item_provenance` (it reads the source junction, not a subset of the extraction view's rows); the four unlinked skill files (each has readers and lacks only a frontmatter `description:` line).

---

## 8. What this file could not determine

- REQ-052, REQ-066, REQ-095, HS-A08, HS-A13, HS-A15, HS-A17: UNPROVEN, reasons in their rows.
- Blocking checks, as now measured on a scratch copy of `main` by the stress run (`stress/results2/tools/log.jsonl`): `migration_reproducibility` PASS, `schema_reference_audit` PASS, `claude_md_spine` PASS, each with a non-zero subject; `run_checks.py --selftest` PASS; `run_checks.py --changed-from origin/main --explain` PASS with advisory failures (HS-5 B-54). `test_db_integrity` was run in the resolution pass: exit 0 on a copy of `main`, exit 1 at C10 on each `provisional` scratch determination. Round 3 of the stress run then ran every battery as `--battery <name> --all`: all PASS, with the advisory failures and nothing-in-scope checks listed in HS-5 B-82. Still not run by anyone: `run_checks.py --all` in one call, and `research_dod_session` with a session set. Their levels are from the registry; their results are unknown.
- The capture → migration → rebuild round trip was run by the stress scripts for one batch at a time and holds by row counts (HS-5 B-38). It fails for batches captured in parallel (HS-5 B-40). For a batch carrying six determinations it holds by content: this leg's clean-clone re-run rebuilt a database equal to the scratch copy in every table but the migration ledger (HS-5 §7.0).
- `governance/time-model.md` and `governance/evidence-methodology.md` were read by grep at the cited sections only.

---

## 9. Resolution record (antagonist pass of 2026-11-12)

The complete record, one row per objection with this leg's re-run evidence, is in `hs-adversarial-findings.md` §5. The rows below are the objections that touch this file.

| FA id | What it touched here | Disposition |
|---|---|---|
| FA-02 | §0 D4, §6, REQ-024 | **amended**: C10 named; "every gate" removed |
| FA-03 | §7 | **withdrawn**: the four skill files |
| FA-09 | §0 D2, REQ-025 | **amended** |
| FA-10 | §6 | **amended**: the governing rows are code provisions tagged `MOB` |
| FA-11 | REQ-022, REQ-098, §5.2 | **amended**: retained-text figures |
| FA-12 | REQ-006 | **amended**: ten lines, five pairs; evidence by YAML load |
| FA-13 | REQ-074 | **amended**: second example withdrawn; verdict kept on the first, basis marked |
| FA-16 | REQ-006, REQ-017, REQ-020, REQ-100, HS-A01, HS-A09, HS-A10 | **amended**: structural evidence given or status lowered to inferred |
| FA-20 | §7 | **withdrawn** for `--slug`; two rows made sweep-gated |
| FA-21 | §0 | **amended**: warrant class of the lens rule |
| FA-23 | §7 | **amended**: IMP-36, not IMP-41 |
| FA-24 | §0 | **amended**: no typed count |
| FA-25 | REQ-006, REQ-025 | **amended** |
| FA-26 | REQ-055, REQ-096, HS-A04, HS-A05 | **amended**: line references |
| FA-27 | HS-A09 | **amended**: command replaced |
| FA-32 | §7 | **withdrawn**: `v_item_provenance` |
