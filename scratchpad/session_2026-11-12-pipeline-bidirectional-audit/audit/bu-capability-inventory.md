# BU — capability inventory (bottom-up leg)

_Bottom-up leg of the 2026-11-12 pipeline audit. Built from code, schema and data only: `scripts/`, `schemas/`,
`governance/*.yaml`, `.claude/`, `skills/`, and `data/guidebook.db` opened read-only. No owner prose was used to decide
what should exist (two accidental exposures are disclosed in the SELF-ATTACK section)._

_State examined: git HEAD `64c10e2` (the dossier was generated at `e73b588`); `PRAGMA user_version` = 125;
`sha256(data/guidebook.db)` = `c9ecb8461baf…ab7c4d`, unchanged before and after this leg (`sha256sum data/guidebook.db`)._

**Evidence grammar.** Every claim carries `VERIFIED` (I read the code or ran the query/command), `INFERRED` (follows
from what I saw; the basis is named) or `UNVERIFIED`. Every count carries a command: `Qn` refers to the query list in
§Z, which is runnable as written. Counts in this file are as of the state above; re-run, do not trust (rule 7a).

---

## 0. Front summary

### Verdict

**The pipeline can be entered at base, research, evidence, judgment and specification, and walked forward to
specification, one cell at a time, on a scratch copy, through refusing writers. It cannot be walked to render, it cannot
be walked backward except by reading pointers, and it is not multilingual or multijurisdictional at the point where it
decides.** The determination is keyed on parameter × lens only; jurisdiction and language are not part of any cell key,
are not read by the engine, and are held in plain text columns governed by a Python enum (jurisdiction) and by the live
rows of one table (language, at one writer only). There are **zero live determinations** in the database (`Q1`), so every
specification-stage and render-stage gate, view and check is either vacuous or examining retired history.

### Worst problems, worst first

1. **Render does not exist as code, and nothing reads what would feed it.** `scripts/generate/` holds a governance map
   generator, a hook generator and a database browser; none renders a determination (§E). `v_best_practice`,
   `v_determination_provenance`, `v_item_provenance`, `v_pending`, `v_divergence`, `v_code_floor_only` have no Python
   reader (`Q20`), and `weighting_profile`, the only render table, has no reader at all. `render/register-invariants`
   is `check: null`. VERIFIED.
2. **Zero live determinations; all eight `specifications` rows are retired** (`Q1`), all on one cell (parameter 3 ×
   `MOB`), all written under `rule_version` `pilot-3` while the engine is `pilot-4` (`assess_cell.py:130`). The three
   blocking specification criteria are checked by `validate_evidence_state.py`, which iterates every row with no
   `retired_at` filter (`validate_evidence_state.py:246`), so its non-zero subject is retired history.
   `derivation_handshake_integrity` and `extraction_follow_up_audit` report 0 live determinations. VERIFIED.
3. **The lens is a label, not a filter.** `assess_cell.gather_sources` selects on `parameter_id` alone
   (`assess_cell.py:249-252`); the four lens columns on `source_value_extractions` are never read. Run on scratch
   copies, parameter 3 × `MOB`, × `BLIND` and × ICF `d450` returned the same state, basis, marker, 27 governing sources,
   122 linked extractions and the same value; only the sha and the population-assessment list differ (§C.2). A
   determination "for blind people" is today computed on wheelchair evidence. VERIFIED by run.
   [AMENDED 2026-11-12 by the handshake leg's resolution pass, FA-10: the rows are not wheelchair evidence. The 35
   governing rows are tagged `MOB` and come from T4–T6 instruments (codes, national frameworks, standards); none is
   device-scoped and none mentions a wheelchair. The defect stands: a cell for one lens is governed by rows tagged
   for another. See `hs-adversarial-findings.md` F-01 and §5.]
4. **Jurisdiction and language are not in the determination's key and are not consumed downstream of judgment.**
   `specifications` has no jurisdiction or language column (`Q30`). The engine reads `jurisdiction` only to count
   distinct jurisdictions for the regulatory "richness" test (`assess_cell.py:1147-1199`). A request for
   parameter × lens × jurisdiction × language cannot be represented at synthesis, specification or render. VERIFIED.
5. **The engine cannot compose a value across units, and most governing claims are not read into the value.**
   Parameter 12 × `MOB` on a scratch copy: `provisional ○` with no value, note "governing claims are stated in different
   units ('cm', 'm', 'mm')". Parameter 3 × `MOB`: value composed from 11 of 35 governing claims; 24 unparsed because
   `claimed_unit` carries prose conditions, `claimed_value` carries a `%` sign or a ratio under a non-exact unit string,
   or a number written in words (`'viisi prosenttia'`). `NOTATION_FAMILIES` holds one family (`assess_cell.py:511-513`).
   No length conversion exists. VERIFIED by run.
6. **Adding a jurisdiction is a code change; adding a language, a slug, an identity or an access need is hand-written
   SQL.** Jurisdiction vocabulary is `schemas.enums.JurisdictionCode` (36 members, `Q31`), checked by
   `dbcore.check_jurisdiction` (`dbcore.py:945-1020`). `lang_jur_map`, `slugs`, `base_taxonomy_identity`,
   `access_needs` have no `db.py` writer, and `lang_jur_map`, `base_taxonomy_identity`, `access_needs` are outside the
   capture set of `emit_batch_sql.py` (`Q11`). 19 of 70 owed (language, jurisdiction) pairs name a jurisdiction the
   enum refuses (`Q32`), so `db.py coverage` can never report `complete` for any slug by data alone. VERIFIED.
7. **Backward re-entry is prose.** The only typed backward edges are `specifications.gap_register_id → gaps`,
   `search_executions.mined_ref_id → evidence_sources`, `search_executions.origin_pass_id → adversarial_passes`,
   `extraction_follow_ups.extraction_id` and `determination_gates`. `gaps` has no parameter, lens, jurisdiction or
   language column (subject is free text); `gap_mining` holds 0 rows and stores its searches as JSON, not as pointers
   to `search_executions`; no table records a render question. The orchestration skill states "The database holds no
   marker for a return" (`skills/run-pipeline_SKILL.md`, invocation paragraph); the schema agrees. VERIFIED.
8. **English is hard-coded in the vocabulary layer's name screens, and several fidelity guards weaken outside Latin
   script.** `_VALUE_BEARING_NAME` screens English words and ASCII digits only; `_name_tokens` is `[a-z0-9]+`, so the
   near-match refusal examines nothing for a non-Latin name; the number-in-quote check reads ASCII and CJK numerals
   only; `normalise_quote` drops Indic and Thai dependent vowel signs (two different Hindi sentences normalise
   identically). `v_evidence_authors` truncates a CJK given name to one character. Tested, §D.5. VERIFIED.
9. **Synthesis is not a separable stage in code.** `convergence_assessment` and `convergence_sources` have no verb and
   are written only by `assess_cell.py` in the same transaction as the determination (`assess_cell.py:2238-2271`).
   `connections`, `connection_targets`, `conflicts`, `supersession_check`, `reasoning_doc_citations` hold 0 rows (`Q2`)
   and nothing computational reads them. The Opus floor is `check: null` and no code tests the authoring model. VERIFIED.
10. **Large standing debt under advisory checks.** `verified_scan_integrity` FAIL: 140 (row, class) pairs across 212
    live extractions; 105 extractions have no covering reading (`Q8`); 12 sit on non-VERIFIED sources (`Q7`);
    `scan_debt` 457 of 580 (source, parameter) pairs unread; `metadata_integrity_audit` FAIL (20 rows);
    `skill_vocabulary_audit` FAIL (76 tokens in 18 files). All advisory. VERIFIED by running each script.

---

## A. ENTRY — can work begin at this stage cold?

"Cold" = no upstream rows exist for the request beyond what the database already holds. "Schema" = FK / NOT NULL /
CHECK / UNIQUE; "writer" = a refusal in `db.py` or `assess_cell.py`; "convention" = prose only.

### A.1 base

| What | Entry path | Enforced by | Status |
|---|---|---|---|
| ICF code | `add-icf-code`, `set-icf-title` (title checked against a payload under `retrieval-log/`, per the `_payload_bodies` docstring, `db.py:8457-8470`) | schema CHECK `icf_code GLOB '[bdes][0-9][0-9][0-9]*'`, `title IS NULL OR title_source IS NOT NULL`; writer | VERIFIED (DDL); writer behaviour INFERRED (handlers at `db.py:8076-8198` not read) |
| identity ↔ ICF crossing | `add-population-icf-link` | FKs both ends, UNIQUE (identity, icf, mechanism) | VERIFIED |
| medical lens | `add-medical` (mints row + ≥1 crossing) | FKs; 0 rows live (`Q2`) | VERIFIED DDL; INFERRED behaviour from help text |
| term | `add-term --from-observation` only (needs an `observed_terms` row, hence an admitted source), or `mint-term-from-catalogue` (5 permitted catalogues in the column CHECK, needs entry ref + approval ref) | writer (`db.py:6478-6493`, `7669-7760`); schema CHECK on the catalogue triple | VERIFIED. **A term cannot be entered cold from nothing**: base re-enters from evidence by design of the writer. |
| parameter | `add-parameter --term-id` | FK + UNIQUE on `term_id`; writer refuses a declined term and a value-bearing name; does **not** require an adjudication (`db.py:6839-6860`, provenance "base-vocabulary") | VERIFIED |
| direction | `set-parameter-direction --ref-id` needs an admitted source holding an extraction for the parameter | writer only (`db.py:6997-7019`); `base-direction-from-source` is `check: null`; both live directions have `direction_ref_id` NULL (`Q3`) | VERIFIED |
| alias | `add-alias` from an adjudicated, verbatim-verified observation only; refuses `TRANSLATION` | writer (`db.py:7455-7495`); FK `observation_id`; 0 of 2382 aliases carry it (`Q33`) | VERIFIED |
| slug, identity, access need, room, life stage, stakes, duration, (language, jurisdiction) pair | **no verb** | — | VERIFIED (`Q10`, verb matrix; `grep -c` of each name in `db.py` returns 0 for rooms, life_stage_modifiers, access_duration, access_stakes, weighting_profile, access_need_icf) |
| jurisdiction code | **Python enum edit** (`schemas/enums.py:85-180`) | writer + blocking `jurisdiction_db_vocabulary`, `validate_jurisdiction` | VERIFIED |

Silent assumptions: `terms.canonical_en` is the single name of a concept; the writer permits a non-English phrase there
(`db.py:6486-6493`) while the column name, the screens and the near-match search assume English (§D.4). VERIFIED.

### A.2 research

- **Cold entry: yes.** `log-search` needs one of `--slug` / `--parameter` / `--mined-ref-id` (schema CHECK
  `COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL`; writer `db.py:740-745`), a non-empty
  `--prior-expectation` (writer only, `db.py:728-735`), a `--language` that `lang_jur_map` holds (writer only,
  `db.py:877-882`), and a `--jurisdiction` the enum declares or none (writer only, `db.py:739`). VERIFIED.
- Schema enforces: FKs on slug, parameter, four lens codes, `mined_ref_id`, `origin_pass_id`; CHECKs on tier,
  evidence type, scope, depth, origin, absence class; `STRICT`. `language` is `TEXT NOT NULL` with no CHECK and no FK;
  `jurisdiction` is free `TEXT`. VERIFIED (DDL).
- Not enforced anywhere: that the (language, jurisdiction) pair is one `lang_jur_map` holds (deliberately; the writer
  reports `in_research_scope`, `db.py:661-668`). Live data: language values in mixed case, and `HR` (1 search, exec 66,
  created 2026-09-18) is not a language of the map (`Q34`) — written while the column was free text (`db.py:870-872`
  dates the refusal 2026-11-06). VERIFIED.
- The lens columns on `search_executions` are NULL on all 203 rows (`Q5`); a lens-scoped search is writable and has
  never been written. VERIFIED.
- `add-candidate`, `add-locator`, `add-code-lead`: cold entry yes; `source_locators` requires at least one identifier
  or a title (schema CHECK). `source_locators.jurisdiction` is exempt from the vocabulary gate and holds URLs and a
  slug name (`Q35`). VERIFIED.
- Gap-driven entry (`unmined-gaps` → `add-gap-mining`): verbs exist; `gap_mining` holds 0 rows and 106 of 110 gaps have
  `mining_addressability` NULL (`Q6`). The path is unexercised on live data. VERIFIED counts; behaviour INFERRED from
  `db.py:10150-10300`.

### A.3 evidence

- **Cold entry: yes, with no research row.** `add-source` requires authors, year, title, `--evidence-type`, a scope
  where the type admits two, and derives the tier (`db.py:3450-3500`); it does not require a search, a candidate, a
  locator or a slug (`db.py:3367-3569`). `evidence_sources` has no FK to research. VERIFIED.
- What ties an admission to research is a junction written elsewhere (`search_admissions`, by `log-search
  --admitted-ref-id` or `link-admission`) and a session-scoped blocking gate (`research_dod_session`, rule R17 per the
  skill). 2 of 59 sources have no admission edge (`Q9`). VERIFIED counts; gate behaviour UNVERIFIED (not run).
- Schema enforces on `evidence_sources`: only CHECKs on `source_type`, `metadata_quality`, `verification_*`,
  `scope`, `data_capture_status`, `citation_mining_status`, `processing_blocked_reason`, resolution outcomes. `tier`,
  `evidence_type`, `jurisdiction`, `lang_detected`, `language`, `co1_source_type` carry no CHECK and no FK. `ref_id`
  shape, VERIFIED-needs-method, Co-1-needs-provenance, DOI de-duplication and next-id are **writer-only**
  (`db.py:3979-4130`, `3509-3521`). VERIFIED.
- `observe-term` needs an admitted, non-superseded source, a locator, a context quote containing the phrase, and the
  quote found in a file saved for that `ref_id` or a ledgered exemption (`db.py:6244-6279`). `language` defaults to
  `EN`, is upper-cased, and is **not validated against anything** (`db.py:6251`). VERIFIED.
- `record-scan` needs a sha256 that matches a file the retrieval log holds for the source, re-hashes the file, and
  refuses `full` over a fetched (non-derived) file (`db.py:7803-7884`). The retrieval log is a filesystem manifest
  (`retrieval-log/<session>/manifest.jsonl`), not a table. VERIFIED.
- `case_studies` (0 rows), `economics_entries` (1 row): verbs exist; entry cold yes. VERIFIED counts.

### A.4 judgment

- **Cold entry: only onto an existing, VERIFIED, read source and an existing active parameter.** `add-extraction`
  refuses: an unadmitted or superseded source; a source not `VERIFIED` (`db.py:9037-9045`); no parameter or an inactive
  one (`9058-9083`); no covering `source_scans` row (`9092-9097`); `verified` status without a full-scope reading
  (`9098-9099`); no lens code (`9102-9106`); a blank or unverifiable `claim_text` (`9130-9144`, `8510-8589`); an
  undeclared jurisdiction (`9013`). VERIFIED.
- Schema enforces of those: `ref_id NOT NULL FK`, `parameter_id NOT NULL FK`, lens FKs and "at least one lens" CHECK,
  claim-type/value CHECK, vocabulary CHECKs. **Not** in schema: source VERIFIED, covering reading, verbatim. Live data
  proves the gap: 12 extractions on non-VERIFIED sources (`Q7`), 105 with no covering reading (`Q8`) — rows written
  before the writer refused, or by migration. VERIFIED.
- `adjudicate-term`: needs an observation and a rationale; no uniqueness, a second adjudication is a contest
  (`db.py:6353-6396`). `add-population-match`: `target_population` is a `TEXT` column with no FK (DDL); the writer
  refuses a value that is not an `identity_code` (`db.py:10411-10413`), so the pointer is writer-held, not
  schema-held; the engine attributes a grade to a cell by a word-boundary regex on that text
  (`assess_cell.py:1026-1034`). Live values are all identity codes (`Q36`). VERIFIED.
- `raise-follow-up`: `reason` vocabulary has one value, `read-outside-admitting-purpose` (DDL). 0 rows. VERIFIED.

### A.5 synthesis

- **`convergence_assessment` / `convergence_sources` cannot be entered at all except by running the determination
  engine**: no `db.py` verb writes them (verb matrix; `Q10`); `assess_cell.py:2250-2271` is the only INSERT. VERIFIED.
- `add-connection`, `add-conflict`, `add-supersession-check`, `add-gap`: cold entry yes; each needs only base or
  evidence rows (FKs to parameters, identities, slugs, extractions, sources). `connections.opus_reviewed` is hard-coded
  to 0 by the writer (`db.py:2947`). All four synthesis tables other than `gaps` and convergence hold 0 rows (`Q2`).
  VERIFIED.
- The contract's entry conditions for synthesis and specification are circular ("a determination with a resolved
  value" / "a synthesis with a resolved value", `pipeline-contract.yaml` stages synthesis and specification); the code
  resolves the circle by writing both in one act. VERIFIED.

### A.6 specification

- **Cold entry: yes, and it writes.** `assess_cell.py` needs an active parameter, an existing slug, at least one live
  lens code, and no live determination for the cell (`assess_cell.py:2207-2212`). With no extraction at all it writes a
  `pending` determination plus a `gaps` row: run on a scratch copy for parameter 7 × `DEAF` (0 extractions) →
  `pending`, `GAP-103`, 0 links. VERIFIED by run.
- Schema enforces: `parameter_id NOT NULL FK`, lens FKs and "at least one" CHECK, state and scale CHECKs, the marker
  CHECKs (`marker` only on `stated`/`provisional`; `regulatory_stratum_only` ⇒ `○`), partial UNIQUE index on the cell
  over live rows, the retirement trigger. Not in schema: that a `stated`/`provisional` row has a governing source
  (checked by `validate_evidence_state.py`), that a `pending` row has a gap (same). VERIFIED.
- No hand-entry verb exists for a determination; `retire-specification`, `raise-determination-gate`,
  `resolve-determination-gate` are the only `db.py` verbs on the stage (verb matrix). VERIFIED.
- `--slug` is required and selects nothing (`assess_cell.py:2141-2144`); it lands in the gap description and report
  only. A vestigial required argument. VERIFIED.

### A.7 render

- **No entry.** There is no render verb, no render script, no render table other than `weighting_profile` (5 rows, no
  writer, no reader). §E. VERIFIED.

---

## B. FORWARD / BACKWARD / LATERAL

### B.1 Boundary table

| Boundary | Forward (verbs, views) | Backward by pointer | Typed? | Status |
|---|---|---|---|---|
| base → research | `log-search` (FK slug/parameter/lenses; language from `lang_jur_map`; jurisdiction from enum); `coverage`; `v_research_scope`, `v_coverage_priority` (slug × owed pair anti-join), `v_coverage_lens` | `search_executions.{slug, parameter_id, identity_code, icf_code, needs_code, medical_code}` FKs. `terms_used` is a JSON array of term ids, not FK. No pointer from a search to the `lang_jur_map` row or the alias it used. | partly | VERIFIED (DDL, `db.py:853-936`) |
| research → evidence | `add-source` (promotes a matching staged locator, keeping its `ref_id`, `db.py:4040-4092`); `log-search --admitted-ref-id` / `link-admission` (`search_admissions`); `resolve-candidate` (`resolved_ref_id`); `update-locator --status PROMOTED` | `search_admissions(exec_id, ref_id)` both FK; `v_source_admission` (evidence + research); `search_execution_artefacts.artefact` → file path in `retrieval-log/` (text pointer). 70 of 203 searches carry an artefact (`Q12`). | yes, except the artefact (path) | VERIFIED |
| evidence → base (re-entry) | `observe-term` → `adjudicate-term` / `add-term` → `add-parameter` / `add-alias` / `rename-term` | `term_adjudications.observation_id` FK → `observed_terms.ref_id` FK; `term_aliases.observation_id` FK (0 used) | yes | VERIFIED |
| evidence → judgment | `record-scan` → `add-extraction`; `add-population-match`; `v_scan_ledger` (base + evidence + judgment) gives the per-(source, parameter) state | `source_value_extractions.ref_id` FK; extraction → reading is a **rule** (`catalogue_version >= parameter_id` or targeted), not a pointer; extraction → observation: no pointer (the DDL comment names it a "KNOWN RESIDUAL"); extraction → bytes: `file_anchor` on 18 of 214 rows (`Q13`), otherwise a runtime search of the retrieval log by `ref_id` | partly | VERIFIED |
| judgment → synthesis | `add-connection` (targets: parameter / slug / identity / extraction FK, methodology text), `add-conflict`; convergence only via `assess_cell` | `connection_targets.extraction_id` FK; `convergence_sources.ref_id` FK → `v_convergence_sources` (evidence + synthesis). Convergence points at **sources**, not at extractions. | yes where rows exist; 0 rows in connections/conflicts | VERIFIED |
| judgment/synthesis → specification | `assess_cell.py` (one command per cell): writes `gaps` (if pending), `convergence_assessment`, `convergence_sources`, `specifications`, `specification_source_links`, `specification_extraction_links` | `specification_extraction_links` (every extraction of the parameter, graded governing / conditioning / excluded with reason) → `v_determination_provenance` (base + evidence + judgment + specification); `specification_source_links` → `v_item_provenance`, `v_source_reach_all`; `convergence_id` FK → `v_divergence`; `gap_register_id` FK → `v_pending`; `dbcore.determinations_resting_on` | yes | VERIFIED by run (122 provenance rows for parameter 3 on scratch); 0 rows live (`Q1`) |
| specification → render | **none** | none | — | VERIFIED (§E) |

### B.2 Is traversal one-way?

- **Forward is a chain of writes; backward is read-only.** Every backward pointer above is traversable by SQL. No verb
  takes a downstream row and creates or schedules upstream work, except: `log-mining` / `log-search --mined-ref-id`
  (evidence → research), `raise-follow-up` (judgment → a re-read), `raise-determination-gate` (an audit finding caps a
  cell), `retire-specification` (reopens a cell), and the gap that `assess_cell` writes for a pending cell. VERIFIED.
- **No single view spans specification to research.** The trace determination → extraction → source →
  admitting search → payload path needs `v_determination_provenance` joined to `v_source_admission` joined to
  `search_execution_artefacts` by hand. INFERRED from the view DDL (no view names all of them; `Q21`).
- **Upstream change does not propagate.** `assess_cell.stale_determinations` (`assess_cell.py:1777-1797`) recomputes
  each live determination and reports differing fields; it is called only by the advisory
  `derivation_handshake_integrity` and a test. `db.py` refuses some edits to rows a live determination rests on
  (`_refuse_if_resting`, `_refuse_live_confirmation`, `db.py:5663`, `8630-8644`). Remedy in both cases is manual:
  retire, then re-run the engine. VERIFIED (code); vacuous on live data (0 live determinations).

### B.3 Lateral movement

| Axis | Mechanism | Evidence | Status |
|---|---|---|---|
| slug ↔ slug | `link-source-slug` (cross-file a source to another slug, with rationale); `resolve-candidate --disposition REHOME`; `slugs.merged_into` | 71 links over 59 sources, 5 slugs used; 2 slugs ever searched of 106 (`Q14`) | VERIFIED |
| parameter ↔ parameter | `relate-extraction` / `derive-extraction` edges may cross parameters: 17 of 32 row-referent edges do; 0 cross sources (`Q15`). `merge-parameter`. `add-connection --type CROSS-PARAMETER` (0 rows). | `Q15` | VERIFIED |
| lens ↔ lens | crossing maps `identity_icf_map` (61), `access_need_icf` (43), `identity_medical_map` (0), `icf_medical_map` (0). `assess_cell.derivation_handshake` reads `identity_icf_map` (5 references in the file). The gather does not use any map: every lens of a parameter receives the same evidence. | §C.2 run; `grep -c identity_icf_map scripts/assess/assess_cell.py` = 5 | VERIFIED |
| jurisdiction ↔ jurisdiction | none typed. `jurisdiction` is a text column on searches, sources, extractions, leads, aliases, economics. No jurisdiction table, no FK, no view comparing jurisdictions for a parameter. A comparison is an ad hoc `GROUP BY x.jurisdiction` over extractions. | `Q30` key matrix | VERIFIED |
| language ↔ language | `term_aliases (term_id, alias, language)` — one term, many languages (15 live, lower case); `observed_terms.language` + `term_adjudications.term_id` gives "what sources in language L call term T" by pointer | `Q33`, `Q37` | VERIFIED |
| source ↔ source | `supersede-source` (`superseded_by_ref_id`, 1 row), `source_value_extractions.root_ref_id` (76 rows), `v_value_independence`; `external_root_registry` has 0 rows and no writer, so `root_id` is unwritable (`db.py:9050-9055`) | `Q16` | VERIFIED |

### B.4 Re-entrant edges: rows or prose?

| Re-entry | Representable in rows? | Evidence |
|---|---|---|
| evidence → base (a source names a new concept) | **Yes**, fully typed: observation → adjudication → term → parameter | 96 observations, 90 adjudications, 6 `NAMES-NEW` (`Q37`). VERIFIED |
| evidence → research (mine a source's citations) | **Yes**: `search_executions.mined_ref_id` FK (11 rows), `citation_mining` (38 rows; `global_ref_id` is text, not FK) | `Q5`, `Q17`. VERIFIED |
| adversarial pass → research | **Yes**: `origin='adversarial-pass'` + `origin_pass_id` FK (1 row with that origin; `origin_pass_id` NULL on all rows, `Q5`) | VERIFIED |
| "a lead met while doing something else" | **Half**: `origin='incidental'` (4 rows) says that it was incidental; nothing points at what it was met in | VERIFIED |
| judgment → evidence (re-read doubtful row) | **Yes, narrowly**: `extraction_follow_ups` (one reason value; 0 rows) | VERIFIED |
| judgment / specification → research (a gap needs a search) | **Half**: `specifications.gap_register_id` FK → `gaps`; `gaps` carries no parameter, lens, jurisdiction or language column — the cell is named in `description` text (`assess_cell.py:2225-2227`); `gap_mining.gap_id` FK exists, 0 rows; its searches are a JSON blob, its discoveries a JSON array of ref ids; `search_executions` has no `gap_id` | DDL of `gaps`, `gap_mining`; `Q6`. VERIFIED |
| synthesis → research (a conflict or connection needs evidence) | **Half**: `conflicts.gap_id` FK (0 rows) | VERIFIED |
| render → judgment (a render question) | **No.** No table, column or verb | `Q30`; §E. VERIFIED |
| specification → specification (re-determine) | **Yes**: retire in place + `superseded_by_specification_id`; the 8 retired rows form one chain (`Q1`) | VERIFIED |
| "why did this run return to stage X" | **No.** Only the session record and `commands.jsonl` | skill text; no column found (`Q30`). VERIFIED |

---

## C. DYNAMIC OPERATION

### C.1 Can one cell be executed end to end now?

**Yes to specification on a scratch copy; no to render; and the cell is parameter × lens, never × jurisdiction ×
language.** VERIFIED by run for the specification step; the upstream steps VERIFIED by reading the writers, not by
running them.

Minimum chain for one new source feeding one cell (each step one command, all on a scratch copy with
`GUIDEBOOK_DB_PATH` set inline):

1. `log-search` (prior expectation first) — research.
2. Retrieve and persist bytes: `retrieval_log.fetch()` (network) — produces the manifest record.
3. `add-source` — evidence. Then `link-admission` or the search's `--admitted-ref-id`.
4. `full_text.py --ref-id` (derive text), `record-scan` — evidence.
5. `observe-term` → `adjudicate-term` (and `add-term` → `add-parameter` if the concept is new) — base/judgment.
6. `add-extraction` (+ `relate-extraction`, `add-population-match`) — judgment.
7. `set-parameter-direction` if none is recorded — base.
8. `assess_cell.py --db … --emit-sql … --parameter-id … --slug … --identity|--icf|--needs|--medical … --session …
   --stamp …` — synthesis + specification.
9. `emit_batch_sql.py --scratch` → `emit_data_migration.py --session --summary --input` → `migrate_db.py` → commit →
   PR (data-only, rule 10) — to make any of it canonical.

Nothing in steps 1–8 is batch-only: each verb acts on one row. What is batch- or session-shaped:

| Element | Shape | Evidence | Status |
|---|---|---|---|
| Every write | scratch copy; `dbcore.connect` refuses the canonical file read-write with no override (`dbcore.py:129-160`); `assess_cell` refuses it too (`assess_cell.py:2156-2157`) | code | VERIFIED |
| Every verb | `--session` required (63 `"--session"` arguments across 72 verbs: `grep -c '"--session"' scripts/db.py`, `grep -c 'add_parser(' scripts/db.py`) | grep | VERIFIED |
| Capture | whole-database diff of the capture set (43 tables, `Q11`) between scratch and canonical; refuses on schema-version mismatch and on any canonical row missing from scratch (`emit_batch_sql.py:137`, `142`, `234`) | code | VERIFIED |
| Landing | one migration file named `data_<timestamp>_<session-slug>.sql`; canonical blob rewritten by `migrate_db.py`; 157 data migrations on disk (`ls scripts/migrations/data_* \| wc -l`), 476 ledger rows (`Q18`) | fs, query | VERIFIED |
| Gates | session-scoped: `research_dod_session` (blocking), `citation_mining_session`, `author_fidelity`, `adversarial_pass_recorded`, `search_log_completeness` read `sessions/LATEST`, `LATEST-RESEARCH` or `scratchpad/CURRENT` (`run_checks.py:76-84`, `220-226`) | registry (`requires_session` on 5 checks, `Q19`) | VERIFIED |
| Determination | one cell per invocation; a re-run for a live cell is refused; ids are taken from the scratch's high-water mark, so two scratch copies determining different cells allocate the same `specification_id` and `GAP-` id (both my parameter 4 and parameter 7 runs allocated `GAP-103`) and cannot both be replayed | run; `assess_cell.py:2201-2205`, `1911` | VERIFIED |
| Concurrency | none: a second session working from an older copy fails capture on the first session's rows ("exist in the canonical DB but not in the scratch") | INFERRED from `emit_batch_sql.py` refusal text |

**Latency and ceremony.** A determination is available in the scratch database immediately (seconds per cell; my six
runs each completed without delay). It becomes canonical only after capture, migration, commit and a merged PR. One
run for parameter 3 emitted 187 INSERT statements (`grep -c INSERT cell_3_MOB.sql` in my scratch). VERIFIED.

### C.2 What the engine does today (run on scratch copies of the live database)

Commands: `cp data/guidebook.db $S/x.db; python3 scripts/assess/assess_cell.py --db $S/x.db --emit-sql $S/x.sql
--parameter-id N --slug accessible-circulation-geometry <lens flag> --session … --stamp '2026-11-12 03:00'
--report-json $S/x.json` — one fresh copy per cell, in the harness scratch directory, outside the repository.

| Cell | State | Marker | Basis | Governing sources | Linked extractions | Value | Note |
|---|---|---|---|---|---|---|---|
| 3 × `MOB` (identity) | provisional | ○ | `T4-6-only-threshold+CO1+T2-direction(proxy_inference)` | 27 | 122 (35 governing, 22 conditioning, 65 excluded) | max 5 % = 1:20 | composed from 11 of 35 governing claims; 24 unparsed |
| 3 × `BLIND` (identity) | provisional | ○ | identical | 27 | 122 | identical | only `needs_population_assessment` and the sha differ |
| 3 × `d450` (ICF) | provisional | ○ | identical | 27 | 122 | identical | — |
| 12 × `MOB` | provisional | ○ | `T4-6-only(regulatory_stratum_only)` | 10 | 21 | **none** | "different units ('cm', 'm', 'mm')" |
| 4 × `MOB` | pending | — | — | 0 | 24 (16 claims excluded as skimmed) | none | no direction recorded; gap written |
| 7 × `DEAF` | pending | — | — | 0 | 0 | none | gap written; cold entry accepted |

All VERIFIED by run. Consequences, each VERIFIED:

- The lens changes nothing but the label (problem 3).
- Jurisdiction is collapsed: the 35 governing rows of parameter 3 come from 20 jurisdiction codes and the output is one
  value (query in §Z `Q22`, run on the scratch copy).
- Units: no conversion; a joined `claimed_unit` cell ("rise:run ratio (maximum) where the height difference is …")
  falls outside the exact-match notation family (`assess_cell.py:527-532`); a value with a `%` sign inside
  `claimed_value` fails `Fraction()`; a number in words fails. `claimed_unit` holds 32 distinct non-NULL strings for
  parameter 3 (`Q23`).

### C.3 Owner-gated and model-gated: code versus prose

| Gate | In code? | Evidence | Status |
|---|---|---|---|
| Canonical DB written by migrations only | **Yes** (two refusals + harness allow-list for `migrate_db.py` only) | `dbcore.py:129-160`; `assess_cell.py:2156`; `.claude/settings.json` permissions | VERIFIED |
| Research and tooling in separate PRs | advisory check `research_tooling_separation` (changeset-scoped) | registry | VERIFIED level; behaviour UNVERIFIED |
| Adversarial pass by a different transcript | **Yes**: schema CHECK `reviewer_transcript <> author_transcript`; `close-adversarial-pass` refusals; `adversarial_pass_recorded` is advisory | DDL; registry | VERIFIED |
| Opus-class floor on synthesis | **No.** `synthesis/opus-routing` is `check: null`; no table or column named `best_practice_synthesis` exists (`grep -rn best_practice_synthesis scripts schemas` finds only comments); `connections.opus_reviewed` is written 0 and read by nothing | grep; `db.py:2947` | VERIFIED |
| Owner approval of a new parameter | **No** flag or column; `mint-term-from-catalogue` alone requires `--approval-ref` (schema CHECK on the catalogue triple) | DDL `terms`; skill text | VERIFIED |
| New jurisdiction | enum edit in a tooling PR (the refusal text says so, `dbcore.py:1014-1020`) | code | VERIFIED |
| New language | a `lang_jur_map` row by hand-written migration; table not in the capture set | `Q11` | VERIFIED |
| Attestation on synthesis paths | blocking, changeset-scoped (`attestation_presence`, `attestation_schema`); subject is files in `HEAD~1..HEAD` | registry `no_floor` text | VERIFIED level; behaviour UNVERIFIED |

---

## D. LANGUAGE AND JURISDICTION

### D.1 Which tables carry the keys

Derived by `Q30` (key matrix over every table). `FK` = column with a foreign key; `col` = plain column; blank = absent.

| Table (stage) | jurisdiction | language | Notes |
|---|---|---|---|
| `lang_jur_map` (base) | col (PK part) | col (PK part) | the only table holding the pair; nothing references it by FK |
| `term_aliases` (base) | col (nullable; report-only in the audit) | col, default `'EN'`, lower case in data | 249 of 2382 rows carry a jurisdiction; values include `TW`, `colloquial` |
| `terms` (base) | — | — (`canonical_en` in the column name) | one name per concept |
| `base_parameters`, lenses, `slugs` (base) | — | — | |
| `search_executions` (research) | col | col `NOT NULL`, no CHECK | |
| `source_locators`, `research_code_leads` (research) | col | — | locators exempt from the gate |
| `search_candidates` (research) | — | — | a candidate carries neither |
| `evidence_sources` (evidence) | col | `lang_detected` col (mixed case), `language` col (NULL on all 59 rows) | six `*_en` / translation columns, all NULL |
| `observed_terms` (evidence) | — (reached via the source) | col, default `'EN'`, upper case | |
| `economics_entries` (evidence) | col | — | `currency` col, NULL |
| `source_value_extractions` (judgment) | col (nullable; 19 NULL) | — (reached via the source) | |
| `evidence_population_match`, `term_adjudications`, `extraction_relations` (judgment) | — | — | |
| `gaps`, `conflicts`, `connections`, `convergence_*` (synthesis) | — | — | a gap cannot say which jurisdiction or language it concerns except in prose |
| `reasoning_doc_citations` (synthesis, 0 rows) | col | — | |
| `specifications`, `specification_*_links`, `determination_gates` (specification) | — | — | **absent from the determination** |
| `weighting_profile` (render) | — | — | |

VERIFIED (`Q30`). Tables that carry neither where the request shape parameter × lens × jurisdiction × language would
need them to address a row: `specifications`, `gaps`, `determination_gates`, `convergence_assessment`, `conflicts`,
`search_candidates`, `evidence_population_match`. Stated as a capability fact, not as a requirement.

### D.2 How the vocabularies are defined

| Vocabulary | Home | Enforced where | Add by data only? | Status |
|---|---|---|---|---|
| Jurisdiction | Python enum `schemas.enums.JurisdictionCode`, 36 members (`Q31`) incl. meta-codes `ISO`, `EU`, `UN`, `INT` | `dbcore.check_jurisdiction` at six call sites: `log-search` (`db.py:739`), `add-source` (`3996`), `amend-source` (`5849`), `add-extraction` (`9013`), `add-economics-entry` (`10476`), `add-code-lead` (`10602`) — `grep -n 'check_jurisdiction(' scripts/db.py`; blocking `jurisdiction_db_vocabulary` (EXAMINED 114 table × rejected-spelling pairs; PASS) and `validate_jurisdiction` | **No — code change** | VERIFIED |
| Rejected spellings (`GB`→`UK`) | parsed from `governance/jurisdiction-philosophy.md` by the audit | same | prose edit | VERIFIED (audit output) |
| Language | the distinct `language` values of `lang_jur_map` (19: `Q32`) | `log-search` only (`db.py:877-882`). Not `observe-term`, not `add-source --lang-detected`, not `term_aliases`, no CHECK anywhere | data, but by hand-written migration (no verb; table outside capture) | VERIFIED |
| (language, jurisdiction) scope | `lang_jur_map.scope_status` → `v_research_scope`; `scope_status` is NULL on all 70 rows (`Q32`) | `coverage` reads it; nothing refuses on it | data, by hand | VERIFIED |
| Language case | none: `lang_jur_map` upper, `term_aliases` lower, `observed_terms` upper, `evidence_sources.lang_detected` mixed (`EN` 6, `en` 21, `FI` 1 …), `search_executions` mixed (`Q34`) | `_alias_language` measures the table's majority case at write time (`db.py:7281-7291`); `log-search` folds to upper | — | VERIFIED |

Concrete defects that follow, all VERIFIED:

- **19 of 70 owed pairs are unreachable** (`Q32`): `lang_jur_map` names 17 jurisdictions the enum does not declare
  (`AR AT CL CO CR CY EC ET GH GT MA MX PE PH TH TZ UY`), so a search for them cannot be logged with its jurisdiction
  and `db.py coverage --slug accessible-circulation-geometry` reports `jurisdictions_unreachable` with those 17 and
  `complete: false` (run read-only).
- `get_unmined_for_all_slugs` orders "non-English first" with `COALESCE(lang_detected, language, 'en') = 'en'`
  (`db.py:10098`), a case-sensitive test: the 6 sources stored `'EN'` sort as non-English.
- Four map languages (`AR`, `BN`, `HI`, `SW`) have no alias in `term_aliases` (`Q33` against `Q32`); parameter 12
  (`ramp run length`, `TERM-091`) has no alias in any language (`Q38`).

### D.3 Where English or one convention is hard-coded

| Location | What is hard-coded | Consequence | Status |
|---|---|---|---|
| `terms.canonical_en` (schema) | one canonical name, named English | the writer admits a non-English phrase into it when no English instrument has been observed (`db.py:6486-6493`); 0 of 94 live names are non-ASCII (`Q39`), so the non-English branch is unexercised | VERIFIED |
| `_VALUE_BEARING_NAME` (`db.py:6403-6409`) | `[0-9≥≤<>=]`, `min/max/minimum/maximum`, `than`, `at least/most`, `no more/less…`, `exceed` | a name stating its answer in another language passes: tested `Mindestbreite`, `largeur minimale`, `最小幅`, `ancho mínimo`, `幅１２００` (full-width digits), `١٢٠٠ مم` → all pass | VERIFIED (re-implementation of the regex, §D.5) |
| `_name_tokens` / `_near_terms` (`db.py:6412-6441`) | tokens are `[a-z0-9]+`; comparison set is `terms.canonical_en` + aliases `WHERE upper(language)='EN'` | the "equivalence before minting" refusal examines nothing for a non-Latin name (`勾配`, `경사로` → empty token set) and splits accented Latin (`Rampenläufe` → `rampenl`, `ufe`); non-English aliases are never compared | VERIFIED |
| `_name_holder` (`db.py:6548-6549`) | `lower()` in SQL (ASCII-only in SQLite) | case-insensitive duplicate detection is ASCII-only | INFERRED from SQLite semantics |
| `add-alias` (`db.py:7460-7464`) | refuses `TRANSLATION` | by design: 996 existing `TRANSLATION` aliases are model-generated or pre-provenance and none is source-attested (`Q33`) | VERIFIED |
| `observed_terms.language`, `term_aliases.language` defaults | `'EN'` | an omitted language is recorded as English | VERIFIED (DDL) |
| Number-in-quote check (`db.py:8559-8588`) | ASCII digits, plus CJK numerals `〇零一二…十百千` (`8592-8622`) | Arabic-Indic, Persian, Bengali, Devanagari digits are not folded by NFKC, so a claimed `1:12` against `١:١٢` is refused; a number in words (Finnish `viisi prosenttia`) has no digits to check and must be stored as the words (extraction 80) | VERIFIED (§D.5; `Q24`) |
| `retrieval_log.normalise_quote` (`retrieval_log.py:605-644`) | NFKC, lower, NFKD, drop combining marks, keep `isalnum()` | correct for Latin, CJK, Hangul, kana. **Drops dependent vowel signs** in Devanagari, Bengali, Thai and Arabic harakat: `रैंप की ढलान` and `रैंप का ढलान` normalise to the same string, so a misquote differing only in vowels verifies | VERIFIED (§D.5) |
| `retrieval_log.decode_artefact` (`retrieval_log.py:657-721`) | strict UTF-8, then declared charset; no statistical detection | a legacy-encoded page with no declaration is reported undecodable, not guessed | VERIFIED (code) |
| Author model (`evidence_source_authors`) | `last_name` / `first_name` / `suffix`; display = last + first initial (`v_evidence_authors`) | CJK personal name `白倉 栄一` renders `白倉 栄` (`Q25`); corporate names carry an English gloss inside the native string (`内閣（Cabinet of Japan）`), `corporate_name_en` NULL on all rows | VERIFIED |
| Engine value parsing (`assess_cell.py:535-563`, `624-673`) | `Fraction(text)` / `float(tok)`; ratio regex `\d+(?:\.\d+)?:\d+…`; range split on `to`, `-`, `–` | comma decimals (`'30,0'`, extraction 72) and number words do not parse; only "a to b" English ranges split on a word | VERIFIED (code; `Q24`) |
| Units (`assess_cell.py:511-524`, `892-896`) | one notation family (`%`, `rise:run ratio`), exact string match; no unit conversion | mm / m / cm / ft / in never compose; operators have converted at extraction instead (extraction 182 stores `915` `mm` for a source sentence reading "36 inches (915 mm)") | VERIFIED (`Q26`) |
| `source_scans` / `v_scan_ledger` | keyed on (source, parameter) | a reading is not per language or jurisdiction; BLOCKED reasons include `language` ("awaiting in-language reading capacity") | VERIFIED (DDL) |
| Skills | `multilingual-research` asserts "19 languages AND 46 jurisdictions" in its description; live map holds 19 languages and 48 jurisdictions, enum 36 | prose count drift | VERIFIED (`Q32`, `Q31`) against the skill description; I did not read the skill body |
| Dates | `created_at` strings `YYYY-MM-DD HH:MM`; `pub_year` INTEGER; `assess_cell --stamp` regex | no non-Gregorian or era dates (Japanese instruments are titled with era years: `平成十八年`, stored in the title only) | VERIFIED (`Q25`) |
| RTL / bidi | no code path | `grep -rni 'bidi\|\brtl\b\|right-to-left' --include=*.py scripts schemas` returns only "bidirectional grain-match" in `schemas/directness.py` and its test | VERIFIED as an absence under that grep only |

### D.4 Can a language or a jurisdiction be added by data only?

- **Jurisdiction: no.** Enum member (code), in a tooling PR; then the `lang_jur_map` row by hand SQL. VERIFIED.
- **Language: by data, but not through the write path.** A `lang_jur_map` row (no verb; table not captured by
  `emit_batch_sql.py`, `Q11`), then aliases through `add-alias`, which needs an admitted source, a persisted quote and
  an adjudication in that language first — so the first search in a new language has no source-attested vocabulary and
  must use model-generated aliases or the source's words found some other way. VERIFIED (writers); the "first search"
  consequence is INFERRED.
- **What then works without change:** `log-search`, `observe-term`, `add-source`, `add-extraction`, the verbatim check
  for Latin/CJK/Hangul scripts, the engine (which ignores language). **What does not:** the name screens, the near-match
  refusal, the digit check and vowel-sign fidelity for Arabic/Indic/Thai scripts, author display, number words.
  VERIFIED per §D.3.

### D.5 Tests run (pure functions re-implemented verbatim from the cited lines; no repository code imported)

Command: an inline `python3 -I` script copying `normalise_quote` (`retrieval_log.py:641-644`), `_name_tokens`
(`db.py:6415-6416`) and `_VALUE_BEARING_NAME` (`db.py:6403-6409`). Results:

| Input | Output | Reading |
|---|---|---|
| `रैंप की ढलान 1:12 से अधिक नहीं` / `रैंप का ढलान …` | both `रपकढलन112सअधकनह` | vowel signs dropped; two different sentences collide |
| `র‌্যাম্পের ঢাল ১:১২` | digits stay `১১২` | Bengali digits not folded to ASCII |
| `منحدر بميل لا يتجاوز ١:١٢`, `شیب ۱:۱۲` | digits stay `١١٢`, `۱۱۲` | Arabic-Indic and Persian digits not folded |
| `ทางลาดชันไม่เกิน 1:12` | `ทางลาดชนไมเกน112` | Thai vowel/tone marks dropped |
| `경사로의 기울기는 12분의 1`, `勾配は、十二分の一を超えないこと` | preserved | Hangul and CJK intact (CJK numerals handled separately by `_cjk_to_arabic`) |
| `_name_tokens('勾配')`, `('경사로')` | `[]` | near-match check vacuous |
| `_name_tokens('Rampenläufe')` | `['rampenl','ufe']` | accent splits the token |
| `_VALUE_BEARING_NAME` on `Mindestbreite`, `largeur minimale`, `最小幅`, `ancho mínimo`, `幅１２００`, `١٢٠٠ مم` | no match | screen passes all |

VERIFIED as behaviour of the copied logic; INFERRED for the live functions (identical source text at the cited lines).

### D.6 Trace of real non-English rows

**Term.** Japanese `勾配`: `observed_terms` id 7 (`ref_id REF-00989`, `language 'JA'`, locator
`法律でスロープの勾配基準は1/12（1/8）`) → `term_adjudications` (`NAMES-EXISTING`, `TERM-001`) → `terms.canonical_en
'ramp gradient'` → `base_parameters.parameter_id 3`. `term_aliases` for `TERM-001` in `ja` holds `スロープ勾配`
(TRANSLATION), `バリアフリースロープ`, `傾斜路` (SYNONYM), none with an `observation_id` and none equal to the observed
`勾配`. Meanwhile observation 9 adjudicates `傾斜路` as `TERM-089` (`ramp`), while the alias table files `傾斜路` under
`TERM-001` (`ramp gradient`); likewise Dutch `hellingbaan` is an alias of `TERM-001` and is adjudicated three times as
`TERM-089`. **The source-attested path (observations → adjudications) and the alias table disagree, and the alias
table is the one multilingual search is told to use.** VERIFIED (`Q37`, `Q40`).

**Source.** `REF-00990` (Japanese Cabinet Order): `evidence_sources.pub_title` holds the native title;
`pub_title_en`, `original_title`, `translation_method`, `language` NULL; `lang_detected 'ja'`; `jurisdiction 'JP'`;
tier 6 `code`; author row corporate `内閣（Cabinet of Japan）`. No verb writes `pub_title_en`, `original_title`,
`translation_method`, `language` or `corporate_name_en` (`grep -rn 'pub_title_en\|original_title\|translation_method'
scripts schemas` finds two comment lines and the verifier's read list). → `source_slug_links` → extractions 22 and 23:
`claimed_value '1:12'` / `'1:8'`, `claimed_unit 'rise:run ratio'`, `comparator '<='`, `claim_text` in Japanese with
kanji numerals (`勾配は、十二分の一を超えないこと。`), `jurisdiction 'JP'`. → In my scratch run both rows are linked to the
parameter 3 determination; the language is not carried past the extraction. VERIFIED (`Q25`, `Q27`).

**Korean.** `REF-01019` and `REF-01031` are two rows for one instrument (identical title bar one space), one
`UNVERIFIED`, one `VERIFIED`; observations 75 and 89 record `경사로` at the same locator under each. A duplicate
identity the DOI-keyed refusal cannot see (no DOI on a statute). VERIFIED (`Q25`); whether one supersedes the other is
UNVERIFIED (`superseded_by_ref_id` is set on 1 source in total, `Q9`).

**Finnish.** Observation 72 `kulkuvayla` and 74 `kulkuväylä` (a correction row for dropped diacritics), both
unadjudicated; extraction 80 stores the value as the words `viisi prosenttia` with the digit gloss inside
`claimed_unit`. VERIFIED (`Q37`, `Q24`).

**Lead stores.** `source_locators` (893 rows, 879 `REFERENCE-ONLY`): `jurisdiction` holds `—` (89), URLs and a slug
name; no language column. `research_code_leads` (96, 91 `REFERENCE-ONLY`): `(jurisdiction, standard_name)` unique; no
language. VERIFIED (`Q35`).

---

## E. RENDER

**Verdict: render is a documented intent with no code.** VERIFIED.

- `ls scripts/generate/` → `context_map.py` (emits `governance/context-map.yaml`, a repository orientation index),
  `research_contract_hook.py` (renders the research contract into the SessionStart hook), `owner_browser_build.py` +
  `owner_browser.html` (embeds the whole database in one HTML page with sql.js for the owner to browse tables,
  pointers and a decision queue; refuses to write inside the repository, `owner_browser_build.py:109-112`). None reads
  `specifications` to produce a page of the book. `grep -o 'FROM [a-z_"]*' scripts/generate/*.py` → `sqlite_master`
  (3), `evidence_sources` (1).
- `parts/` contains three directories, each holding only `_MOVED.md` (`ls parts/*`).
- The render stage's one table, `weighting_profile` (5 rows: audience × use pattern with a JSON `tier_weights`), has no
  writer (verb matrix) and no reader in `scripts/`, `schemas/` or `.claude/` (grep; it is named in governance prose,
  `stage-map.yaml`, `context-map.yaml`, `owner-browser.yaml`).
- The orchestration skill says so itself: "No specification renderer exists … this stage is walking the contract by
  hand against the database and writing the findings to the session record" and "No check examines rendered output"
  (`skills/run-pipeline_SKILL.md` §7). Consistent with the code.
- Registry battery `render` holds one check, `context_map_fresh` (advisory), whose subject is the governance map, not a
  rendering. `render/register-invariants` is `check: null`; `render/mode-stratum-matrix-consistency` checks a matrix in
  a governance document against `schemas/directness.py` (advisory).

**What the database offers a future renderer for tracing a claim to bytes** (all VERIFIED unless marked):

1. `specifications` → `specification_extraction_links (role, exclusion_reason)` → `source_value_extractions`
   (`claim_text` verbatim, `source_section`, 16 `loc_*` columns of which 9 are never populated, `Q28`) →
   `evidence_sources` — one view, `v_determination_provenance`. 0 rows live; 122 on my parameter 3 scratch run.
2. Source → admitting search: `search_admissions` → `search_executions` (query text, engine, language, jurisdiction,
   prior expectation) — `v_source_admission`, 61 rows; 2 sources have no edge (`Q9`).
3. Search → payload: `search_execution_artefacts.artefact`, a path under `retrieval-log/`; 70 of 203 searches (`Q12`).
4. Source → bytes: `retrieval-log/*/manifest.jsonl` records carrying `ref_id` (a filesystem index, not a table): 49 of
   59 sources have at least one (`Q29`). `source_scans.file_sha256` names the file read: 18 scans over 11 sources
   (`Q29`). `source_value_extractions.file_anchor`: 18 rows (`Q13`).
5. Extraction → the exact bytes: **no stored pointer.** The verbatim check is performed at write time by searching the
   log (`retrieval_log.locate_quote`); the row keeps the quote and, for 29 rows, a `[VERBATIM-EXEMPT: …]` marker in
   `notes` (`Q13`). A renderer would have to re-run the search to show where the quote sits. INFERRED from the absence
   of any artefact column other than `file_anchor`.
6. Translation: no column for a translated quote or title is ever populated (`Q28`); the skill states translation
   "waits on the owner".

---

## F. ENFORCEMENT AUDIT

Registry: 75 checks — 30 blocking, 43 advisory, 2 informational (`Q19`). Contract: 32 criteria examined by
`pipeline_contract_audit` (PASS; "incomplete=5, verifiable=27"), 5 with `check: null`:
`base/base-direction-from-source`, `judgment/convergence-independence`, `judgment/comparator-recorded`,
`synthesis/opus-routing`, `render/register-invariants`. `governance/stage-map.yaml` is read by no registered check (its
own header says so). VERIFIED.

Checks I ran individually (read-only; each command is `python3 scripts/audit/<name>.py`), with the subject each printed:

| Stage | Criterion / check | Level | Result today | Subject (EXAMINED) | Vacuous? |
|---|---|---|---|---|---|
| base | `jurisdiction_db_vocabulary` | blocking | PASS | 114 table × rejected-spelling pairs over 8 tables; 1 exempt (`source_locators`), 1 candidate-only (`lang_jur_map`), 1 report-only (`term_aliases`: reports `TW`, `colloquial`) | no; but the three tables with the dirtiest values are outside the failing set |
| base | `alias_provenance_audit` | blocking | PASS | 2382 aliases; 880 grandfathered, reported not failed | partly: provenance text, not attestation; 0 aliases point at an observation |
| base | `identifier_floor_audit` | blocking | CLEAN | 3 identifier floors vs 226 migration files | no |
| base | `medical_lens_integrity` (also `specification/no-diagnosis-only-determination`) | advisory | CLEAN | **0** | **yes, both criteria** |
| base | `skill_vocabulary_audit` | advisory | **FAIL** | 509 tokens in 33 files; 76 tokens in 18 files resolve nowhere | no |
| base | `base-direction-from-source` | — | `check: null` | both live directions have no source (`Q3`) | unenforced |
| research | `research_protocol_audit` (`adversarial-fields-complete`) | advisory | **23 issues** (exit 1) | 230 | no |
| research | `gap_mining_audit` | advisory | PASS | 110 gaps; 0 `gap_mining` rows | substantively vacuous for mining attempts |
| research | `provenance_artefact_audit --mode surfaced` | blocking | PASS | 42 candidates carrying `surfaced_in` | no; 73 without `surfaced_in` are "reported without failing" by `--mode attribution` (advisory) |
| evidence | `metadata_integrity_audit` (`evidence-verification-gate`) | advisory | **FAIL** | 59 sources; 20 COMPLETE rows with an open integrity flag | no |
| evidence | `observation_verbatim_audit` | advisory | PASS vs baseline | 96 observations; 12 quote-missing, 29 unscoped, 6 phrase-not-in-quote | no; passes by ratchet baseline, not by absence |
| evidence | `scan_debt` | advisory | DEBT (exit 1) | 580 (source, parameter) pairs; 457 owed | no |
| judgment | `judgment_handoff_shape` (`handoff-fanout-preserved`) | blocking | PASS | 3 schema invariants | no; shape only, not content |
| judgment | `extraction_relations_integrity` (`figure-role-stated`) | blocking | CLEAN | 271 = 214 rows + 57 edges + **0** `v_derived_figure_check` rows | derived-figure half vacuous (0 derived rows) |
| judgment | `verified_scan_integrity` (`verified-reading`) | advisory | **FAIL** | 212 live extractions; 140 (row, class) pairs | no |
| judgment | `adjudication_integrity` | blocking | PASS | 59 sources (tier derivable). Its readiness block reports "8 determination(s)" without excluding retired rows | no for tiers; misleading on determinations |
| judgment | `convergence-independence`, `comparator-recorded` | — | `check: null` | `v_value_independence` returns 1 row; `external_root_registry` 0 rows | unenforced |
| judgment | `extraction_follow_up_audit` | advisory | PASS | **0** follow-ups, **0** live determinations | **yes** |
| synthesis | `opus-routing` | — | `check: null` | — | unenforced |
| specification | `validate_evidence_state` (3 criteria) | blocking | not run (outside `scripts/audit/`) | code iterates all `specifications` rows with no `retired_at` filter (`:246`) → 8 retired rows | **live subject is 0**; passes on history. INFERRED result, VERIFIED scoping |
| specification | `derivation_handshake_integrity` | advisory | CLEAN | 1 (the open gate); "determinations: 0". Its printed explanation ("`specifications` holds 0 rows … cannot accept a row until a parameter is minted … none has been since the 2026-09-13 circulation clear") is false: 8 rows, 10 parameters (`Q1`, `Q3`) | **yes**; and the prose contradicts the database |
| render | `register-invariants` | — | `check: null` | — | unenforced |
| render | `context_map_fresh` | advisory | not run | governance map | not a render check |
| cross-stage | `pipeline_contract_audit` | advisory | PASS | 32 criteria | no |

Not run (state the limit rather than imply a result): `test_db_integrity` (blocking; holds K01/K02 sha verification),
`migration_reproducibility` (blocking; rebuilds a database), `validate_evidence_state`, `validate_jurisdiction`,
`validate_verification_consistency`, `schema_reference_audit`, `column_vocabulary_audit`, `derived_not_curated_audit`,
`source_slug_links_duplicates`, `db_path_env_audit`, `research_dod*`, all `attestation_*`, all `tests/*`,
`run_checks.py` in any mode. Their levels are VERIFIED from the registry; their results are UNVERIFIED.

Structural facts about enforcement, VERIFIED:

- **Preconditions live in writers, not in the schema.** Source-VERIFIED-before-extraction, reading-before-extraction,
  verbatim, direction-from-source, search-before-admission, tier derivation, DOI de-duplication, id minting, language
  membership, jurisdiction membership are all `db.py` refusals. A data migration written by hand bypasses every one;
  the checks that would notice afterwards are advisory (`verified_scan_integrity`, `metadata_integrity_audit`) except
  jurisdiction. Live counts of pre-refusal rows: `Q7`, `Q8`.
- **`migration_reproducibility` (blocking) compares counts**; the row-level variant is advisory (CLAUDE.md states it;
  registry levels confirm; behaviour UNVERIFIED).
- **The capture set is a text regex over two files** (`dbcore.py:1075-1100`). `slugs` is in it only because
  `assess_cell.py:1975` contains the words `INSERT INTO slugs` inside a refusal message (`grep -n 'INSERT INTO slugs'
  scripts/db.py scripts/assess/assess_cell.py`). Harmless today (an extra table diffed); it shows the derivation reads
  prose.
- `run_checks.py` treats a check whose every `EXAMINED:` line is zero as NOTHING-IN-SCOPE and refutes a `no_floor`
  reason that asserts emptiness over a non-zero subject (`run_checks.py:287-420`). It cannot see a check that prints a
  non-zero EXAMINED over the wrong subject (retired rows; sources instead of determinations). INFERRED from the
  mechanism being the EXAMINED line alone.

---

## G. ORPHANS AND DEAD APPARATUS

### G.1 Tables with no writer (no `db.py` verb, not written by `assess_cell.py`)

From the verb matrix and `Q10`; rows from `Q2`.

| Table | Stage | Rows | Reader in code? | Note |
|---|---|---|---|---|
| `lang_jur_map` | base | 70 | `log-search`, `coverage`, views, 2 audits | load-bearing vocabulary with no writer |
| `slugs` | base | 106 | many | no writer; 2 slugs searched, 5 linked to sources (`Q14`) |
| `base_taxonomy_identity` | base | 23 | lens FK target | no writer |
| `access_needs`, `access_need_icf` | base | 17, 43 | lens FK target; `access_need_icf` 0 references in `db.py`/`assess_cell.py` | no writer |
| `rooms` | base | 17 | **none** (`grep -c '\brooms\b'` = 0 in `db.py`, `assess_cell.py`; no hit in `scripts/` or `schemas/` outside tests/migrations) | no FK in or out |
| `life_stage_modifiers`, `access_duration`, `access_stakes` | base | 2, 3, 3 | **none** | no FK in or out |
| `external_root_registry` | evidence | 0 | FK target of `source_value_extractions.root_id`; `add-extraction` refuses any `root_id` because the registry is empty and "has no writer yet" (`db.py:9050-9055`) | makes `root_id` unwritable; `root_id` NULL on all 214 rows |
| `reasoning_doc_citations` | synthesis | 0 | FK target of `promoted_to_rdc_id` (NULL on all rows) | dead pair |
| `convergence_assessment`, `convergence_sources` | synthesis | 5, 69 | engine-written only | all 5 belong to retired determinations |
| `weighting_profile` | render | 5 | **none** | |
| `specification_*_links`, `specifications` | specification | 151, 38, 8 | engine-written | all on retired rows |
| `decisions` | infrastructure | 188 | several audits | no verb; latest `decision_date` 2026-09-11 (`Q18`) |

### G.2 Empty tables (`Q2`) and what that disables

`base_taxonomy_medical`, `icf_medical_map`, `identity_medical_map` (medical lens: a non-NULL `medical_code` is
unwritable anywhere); `case_studies`; `gap_mining`; `extraction_follow_ups`; `conflicts`; `connections`;
`connection_targets`; `supersession_check`; `reasoning_doc_citations`; `external_root_registry`. Twelve empty tables of
56 (`Q2`). The UNWRITABLE derivation of CLAUDE.md §4 (NOT NULL FK into an empty table), re-run: `Q41` → the NOT NULL
FKs into empty tables are on the children of those empty parents only (`connection_targets.con_id`,
`icf_medical_map.medical_code`, `identity_medical_map.medical_code` — three lines, all children of empty parents);
no populated stage table is blocked by a NOT NULL FK. The nullable FKs into empty tables
(`source_value_extractions.root_id`, `.medical_code`, `.promoted_to_rdc_id`; `specifications.medical_code`;
`search_executions.medical_code`) are writable only as NULL. VERIFIED by running the derivation.

### G.3 Views with no code reader

23 views (`Q21`). No Python reader found for `v_best_practice`, `v_determination_provenance`, `v_item_provenance`,
`v_pending`, `v_divergence`, `v_code_floor_only`, `v_source_reach_all` beyond comments, the reproducibility audit's
schema comparison and one test stub (`Q20`). Each returns 0 rows live except `v_source_reach_all` (88). The
cross-stage pointer views exist and are unread. VERIFIED (grep); a reader in a skill's prose is not a code reader.

### G.4 Columns never populated on a non-empty table (`Q28`)

Derived per column (`count(*) where col is not null and col <> ''` = 0). Highlights:

- `evidence_sources`: 45 columns, including every translation/English-title column (`original_title`,
  `pub_title_en`, `pub_subtitle_en`, `chapter_title_en`, `journal_name_en`, `translation_method`), `language`,
  `standard_number`, `isbn`, `issn`, `pmcid`, `edition`, the four `code_currency_*` columns,
  `processing_blocked_reason`, `verification_closure_reason`, the writer-retired author copies, `bpc_shorthand`,
  `bpc_note`, `search_queries_used`, `derivation_chain`, `prior_expectation`.
- `source_value_extractions`: `medical_code`, `root_id`, `echo_of`, `promoted_to_rdc_id`, 9 of 16 `loc_*` columns.
- `search_executions`: `origin_pass_id`, all four lens codes, `absence_class`.
- `term_aliases.observation_id`; `terms.catalogue*` (3); `lang_jur_map.scope_status`;
  `base_parameters.direction_ref_id`, `merged_into`; `evidence_population_match.gap_id`;
  `convergence_assessment.synthesis_approach`; `specifications.icf_code`, `needs_code`, `medical_code`, `value_min`,
  `marker`, `cultural_claim_anchor`, `not_applicable_rationale`; `gaps.confidence_interval`, `shift_conditions`;
  `economics_entries` (13 of 25 columns on its single row); `rooms.category`, `description`.

Some are new columns awaiting first use (`scope_status`, `absence_class`, `observation_id`, `direction_ref_id`,
`marker`); some are retired copies kept because migrations insert them; the translation and `code_currency_*` sets have
no writer at all. Which is which per column: INFERRED from migration comments in the DDL, not established per column.

### G.5 Verbs whose output nothing reads

`add-connection`, `update-connection`, `delete-connection`, `add-conflict`, `update-conflict` (rows read only by the
two query verbs and the graph audit; the skill says "No code reads `connections`, `connection_targets` or
`conflicts`"); `add-supersession-check` (read by `gap_mining_audit` and a vocabulary audit); `add-case-study`,
`add-economics-entry` (read by `research_batch_dod.py` only); `add-code-lead` / `update-code-lead` (no reader outside
the writer's own duplicate check). VERIFIED by word grep, which over-reports (English words); a missed reader would
make this list shorter, not longer.

### G.6 Skills presupposing structures that no longer exist

- `skill_vocabulary_audit` (advisory) fails on 18 files; per-file tokens include `item-specification-writer`,
  `connection-scout`, `bpc_metadata`, `part7_items`, `bpc_slugs`, `chunk-assembler`, `update-gap-research-fields`
  (a verb `db.py` does not have), `supersession_check.checked_at` (a column that does not exist), `v_source_containment`
  (a view that does not exist). VERIFIED (script output).
- By grep of `skills/*_SKILL.md`: `item-specification-writer` is named by `functional-deficit-researcher`,
  `research-log-manager`, `toc-editor` (no such skill file exists: `ls skills | grep -i item-spec` is empty);
  `item_code`/"item code" by 6 skills; `BPC` by 12; `volii-validator` by 2; `slug-registry` by `research-log-manager`.
  VERIFIED.
- `.claude/skills/<name>/SKILL.md` are symlinks into `skills/`; 22 are loadable, 4 files in `skills/` are not linked
  (`adversarial-research`, `evidence-metadata-rehabilitation`, `integrity-protocol`, `voice-style`);
  `integrity-protocol` names `scripts/regenerate_derived.sh`, which does not exist. VERIFIED.
- `slugs.sl_path` and `bpc_path` are `NOT NULL` columns naming per-slug search-log and BPC files — a prior-version
  file architecture that `research-log-manager` still describes. Whether those files exist was not checked.
  UNVERIFIED.

---

## H. DIRECTION MATRIX

Rows = stage the run **enters** at; columns = stage it **reaches**. Above the diagonal is forward work; on and below
it, a cell states (a) whether the row stage's rows can be **traversed** back to the column stage by pointer and
(b) whether a **re-entry act** (new work at the column stage caused by the row stage) is representable.

Verdicts: **MECH** = verbs/scripts with refusals do it; **MANUAL** = possible only by hand SQL, by a code edit, or with
a link that is prose/JSON; **PROSE** = only a skill or session record describes it; **NONE** = nothing.
All forward chains are scratch-copy, session-stamped, and need a model or person to retrieve and read; "MECH" means
every write on the path has a refusing writer, not that the path is automatic.

| enter ↓ / reach → | base | research | evidence | judgment | synthesis | specification | render |
|---|---|---|---|---|---|---|---|
| **base** | **MECH / MANUAL** ICF, medical, catalogue terms, parameter lifecycle by verb; slugs, identities, needs, languages by hand SQL; jurisdictions by enum edit (A.1) | **MECH** `log-search --slug\|--parameter`, `coverage`, `v_coverage_priority` (A.2) | **MECH** via research, or `add-source` directly; nothing selects sources *for* a base object except by search | **MECH** chain → `record-scan` → `add-extraction` | **MECH** for convergence (engine); narrative rows by verb, unread | **MECH** `assess_cell`; cold cell writes `pending` + gap (run, C.2) | **NONE** |
| **research** | traverse **MECH** (FKs to slug, parameter, lenses); act **NONE** (a search mints nothing in base; an unknown language is refused, an unknown jurisdiction is refused) | **MECH** lateral: `log-search --origin incidental`, `log-mining`, candidates, `link/unlink-admission` | **MECH** `add-source` (+ locator promotion), `search_admissions`, `resolve-candidate` (B.1) | **MECH** chain | **MECH** chain | **MECH** chain | **NONE** |
| **evidence** | **MECH** `observe-term` → `adjudicate-term` / `add-term` → `add-parameter` / `add-alias`; typed (B.4) | **MECH** `log-search --mined-ref-id`, `log-mining`, `add-locator`; `unmined`, `is-mined` | **MECH** `link-source-slug`, `supersede-source`, `correct-source`, `amend-source`, `record-scan` | **MECH** `record-scan` → `add-extraction` (source must be VERIFIED) | **MECH** chain | **MECH** chain (`from-evidence` variant of the skill) | **NONE** |
| **judgment** | **MECH** `set-parameter-direction` (needs an extraction), `add-term`, `merge-parameter`, `retire-parameter` | **MANUAL** `add-gap` (free text) → `unmined-gaps` → `add-gap-mining` (JSON; 0 rows); or `log-search --parameter` with no pointer back to the extraction | traverse **MECH** (`ref_id` FK; reading by rule); act **MECH**, narrow: `raise-follow-up` (one reason; 0 rows), targeted `record-scan` | **MECH** lateral: `relate-extraction` (17 cross-parameter edges), `derive-extraction`, `amend-extraction`, contest rows | **MECH** write (`add-connection`, `add-conflict`), **no reader** | **MECH** `assess_cell` (run, C.2) | **NONE** |
| **synthesis** | traverse **MECH** (FKs); act **NONE** | **MANUAL** `conflicts.gap_id` → gap → mining (0 rows) | traverse **MECH** (`convergence_sources`, `v_convergence_sources`, `supersession_check.ref_id`) | traverse **partial**: `connection_targets.extraction_id`; convergence points at sources, not extractions | convergence **not enterable** except through the engine; narrative rows **MECH** | convergence **MECH** (same act); connections/conflicts → determination **NONE** (engine does not read them) | **NONE** |
| **specification** | traverse **MECH** (parameter + lens FKs); act: `retire-specification`; parameter merge/retire refuse while a live determination stands | **MANUAL** `gap_register_id` → `gaps` typed; beyond that prose/JSON (B.4) | traverse **MECH** `specification_source_links`, `v_item_provenance`, `v_source_reach_all`, `dbcore.determinations_resting_on` | traverse **MECH** `specification_extraction_links`, `v_determination_provenance` (122 rows on scratch; 0 live); act **MECH** `raise-determination-gate`; staleness detected by an advisory check, not propagated | traverse **MECH** `convergence_id`, `v_divergence` | **MECH** retire + re-run (`superseded_by_specification_id`); lateral across lenses = re-run, same evidence (C.2) | **NONE** |
| **render** | **NONE** | **NONE** | **NONE** | **NONE** (PROSE: skill §7 says findings go to the session record) | **NONE** | **NONE** | **NONE** (PROSE; `owner_browser_build.py` is a database browser, not a rendering of a determination) |

Evidence for each non-NONE cell is the section cited in the cell or the boundary table B.1. Cells that are MECH on
paper and **unexercised on live data** (0 rows of the thing they produce): every backward traversal from
specification (0 live determinations, `Q1`); judgment → research and synthesis → research (0 `gap_mining`);
judgment → evidence re-read (0 follow-ups); judgment → synthesis narrative (0 connections, 0 conflicts);
research with a lens (0 lens-scoped searches); base medical lens (0 rows). Under CLAUDE.md rule 4 these are unproven,
not clean.

---

## SELF-ATTACK — where this inventory is weakest

1. **Independence was breached twice, mechanically.** A `grep -rn weighting_profile` over the repository printed two
   lines of `references/project-standards.md` (lines 3198 and 3213) and one line of
   `workplan/pipeline-state-graph/WALKABILITY.md`, and `governance/pipeline-contract.yaml` quotes owner sentences in its
   `references:` fields. I did not use them to decide what should exist, and no claim above rests on them; the handshake
   leg should discount this file's independence by that much.
2. **`db.py` is 10,821 lines; I read the handlers I rely on, not the file.** Read in full or in the decisive part:
   `log_search`, `insert_evidence_source` and the `add-source` dispatch, `observe_term`, `adjudicate_term`,
   `insert_term`, `add_alias`, `_require_verbatim` and the CJK helpers, the first 245 lines of `insert_extraction`,
   `add_gap_mining`, `get_unmined_gaps`, `get_unmined_for_all_slugs`. Read as an outline only (refusal strings):
   `insert_parameter`, `set_parameter_direction`, `record_scan`. **Not read**: `amend-*` beyond `amend_source`'s head,
   `correct_source`, `merge/retire-parameter`, `add-connection`, `add-conflict`, `add-medical`, `link/unlink-admission`,
   `resolve-candidate`, `supersede-source`, `raise/resolve-determination-gate`, the adversarial-pass verbs. Claims about
   those are from the dossier's verb matrix, help strings and the skill, and are INFERRED however they are worded.
3. **`assess_cell.determine` was read to line 1598 of a function ending near 1770**; `assess_source`, `classify`,
   `derivation_handshake`, `_confirmed_bands`, `gap_account` were not read. The marker rule and the handshake are known
   to me only through the six runs' outputs.
4. **The six engine runs are my strongest evidence and they are on scratch copies with an arbitrary slug and stamp.**
   They show what `pilot-4` does to today's rows; they are not a replay through capture and migration, which I did not
   run. Whether `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py --rebuild` round-trips today is
   UNVERIFIED.
5. **The language tests are re-implementations.** I copied three small functions rather than importing repository
   modules. If the live functions differ from the lines I copied, §D.5 is wrong. `_cjk_to_arabic`, `_name_in`,
   `decode_artefact`, `phrase_in_quote` and `locate_quote` were read, not exercised.
6. **Static reader detection is weak in both directions.** "No Python reader" claims come from `grep` for a table or
   view name; a dynamically built SQL string would be missed (dossier limit), and English-word table names
   (`connections`, `conflicts`, `decisions`, `rooms`) over-report. I did not grep `tools/`, `workplan/` scripts or
   `.github/` for readers.
7. **Checks I did not run are the blocking ones that matter most**: `test_db_integrity` (K01/K02),
   `migration_reproducibility`, `validate_evidence_state`, `schema_reference_audit`, `research_dod_session`. Section F
   states their level and scoping from registry and code, never their result. The claim that
   `validate_evidence_state` passes on retired history is INFERRED from line 246, not observed.
8. **Skills were treated as hypotheses but only one was read** (`run-pipeline`). `multilingual-research`,
   `citation-miner`, `gap-driven-mining`, `research-log-manager` contain the operating instructions for language and
   jurisdiction work; what they tell an operator to do (query languages, vocabulary sources, the "46 jurisdictions")
   was not examined beyond descriptions and the vocabulary audit's token list. Hard-coded English in skill prompts is
   therefore under-reported.
9. **Hooks**: `.claude/settings.json` was read to its first PostToolUse entry; the SessionStart and Stop hooks and
   `record-command.py` were not read. Claims about session-shaping from hooks are not made here for that reason.
10. **"Unexercised" is not "broken".** For gap mining, follow-ups, connections, conflicts, the medical lens and
    lens-scoped searches I report 0 rows; I did not attempt the verbs on a scratch copy, so whether they work is
    UNVERIFIED either way.
11. **Counts of pre-refusal rows (`Q7`, `Q8`) re-implement the covering rule in SQL** (`catalogue_version >=
    parameter_id` or targeted). `verified_scan_integrity` prints 140 (row, class) pairs over 212 live extractions; my
    105 and 12 are over all 214 rows and are a different cut. Use the script's figure where they differ.
12. **Render absence is asserted from `scripts/generate/`, `parts/` and a grep for view readers.** A renderer living
    under `tools/`, `working/`, `workplan/` or an archived path would not have been found. `ls` of the repository root
    shows no `tools/` directory; `workplan/2026-10-30-ramp-spec-pages/` exists by reference in the skill and was not
    opened.

---

## Z. Query list (run as written; read-only)

Preamble for every `Qn`:

```python
python3 -I - <<'PY'
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
def q(sql): print(con.execute(sql).fetchall())
# paste the query line(s) below
PY
```

| Id | Query | Result at the state examined |
|---|---|---|
| Q1 | `q("select count(*), sum(retired_at is null), group_concat(distinct rule_version), group_concat(distinct parameter_id||'x'||identity_code) from specifications")` | `(8, 0, 'pilot-3', '3xMOB')`; views `v_best_practice`, `v_determination_provenance`, `v_item_provenance`, `v_pending`, `v_divergence`, `v_code_floor_only` each `count(*)` = 0 |
| Q2 | for each table in `sqlite_master`: `select count(*)` | 56 tables excluding `sqlite_sequence`; 12 empty (listed in G.2); `connections` 0, `conflicts` 0, `gap_mining` 0, `supersession_check` 0 |
| Q3 | `q("select parameter_id, status, accessibility_direction, direction_ref_id from base_parameters")` | 10 active; directions on 3 and 12 (`lower_is_better`), `direction_ref_id` NULL on all |
| Q5 | `q("select sum(slug is not null), sum(parameter_id is not null), sum(mined_ref_id is not null), sum(coalesce(identity_code,icf_code,needs_code,medical_code) is not null), sum(origin_pass_id is not null) from search_executions")`; `q("select origin, count(*) from search_executions group by 1")` | `(196, 7, 11, 0, 0)` of 203; planned 195, incidental 4, lead-index 3, adversarial-pass 1 |
| Q6 | `q("select coalesce(mining_addressability,'NULL'), count(*) from gaps group by 1")`; `q("select count(*) from gap_mining")` | NULL 106, NOT-ADDRESSABLE 4; 0 |
| Q7 | `q("select count(*) from source_value_extractions x join evidence_sources e using(ref_id) where coalesce(e.verification_status,'')<>'VERIFIED'")` | 12 |
| Q8 | `q("select count(*) from source_value_extractions x where not exists (select 1 from source_scans s where s.ref_id=x.ref_id and ((s.mode='catalogue' and s.catalogue_version>=x.parameter_id) or (s.mode='targeted' and s.target_parameter_id=x.parameter_id)))")` | 105 |
| Q9 | `q("select count(*), sum(exists(select 1 from search_admissions a where a.ref_id=e.ref_id)), sum(exists(select 1 from source_scans s where s.ref_id=e.ref_id)), sum(superseded_by_ref_id is not null) from evidence_sources e")` | `(59, 57, 11, 1)` |
| Q10 | the dossier's derived list "Tables no `db.py` verb writes" (`dossier/12-db-verb-matrix.md`, regenerate with `build_dossier.py`), cross-checked against Q11 | 18 tables with no `db.py` verb; of these `convergence_assessment`, `convergence_sources`, `specification_extraction_links`, `specification_source_links` (and `specifications`, `gaps`) are written by `assess_cell.py` |
| Q11 | `python3 -I -c "import sys,sqlite3; sys.path.insert(0,'scripts'); import dbcore; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); w=dbcore.writable_tables(c); print(len(w)); print(sorted({r[0] for r in c.execute(\"select name from sqlite_master where type='table'\")}-set(w)))"` | 43 captured; not captured: `access_duration, access_need_icf, access_needs, access_stakes, base_taxonomy_identity, data_migrations, decisions, external_root_registry, lang_jur_map, life_stage_modifiers, reasoning_doc_citations, rooms, sqlite_sequence, weighting_profile` |
| Q12 | `q("select count(distinct exec_id) from search_execution_artefacts")` | 70 (of 203 searches) |
| Q13 | `q("select sum(file_anchor is not null), sum(notes like '%VERBATIM-EXEMPT%') from source_value_extractions")` | `(18, 29)` of 214 |
| Q14 | `q("select (select count(distinct slug) from search_executions where slug is not null), (select count(distinct slug) from source_slug_links), (select count(*) from slugs)")` | `(2, 5, 106)` |
| Q15 | `q("select count(*), sum(a.parameter_id<>b.parameter_id), sum(a.ref_id<>b.ref_id) from extraction_relations r join source_value_extractions a on a.extraction_id=r.from_extraction_id join source_value_extractions b on b.extraction_id=r.to_extraction_id")` | `(32, 17, 0)` |
| Q16 | `q("select sum(root_ref_id is not null), sum(root_id is not null) from source_value_extractions")`; `q("select * from v_value_independence")` | `(76, 0)`; 1 row |
| Q17 | `q("select count(*), sum(deferred_reason is not null) from citation_mining")` | `(38, 13)` |
| Q18 | `q("select count(*) from data_migrations")`; `q("select max(decision_date), count(*) from decisions")` | 476; `('2026-09-11 01:20', 188)` |
| Q19 | `python3 -c "import yaml,collections; r=yaml.safe_load(open('governance/check-registry.yaml')); print(len(r['checks']), collections.Counter(c['level'] for c in r['checks']), sum(1 for c in r['checks'] if c.get('requires_session')))"` | 75; blocking 30, advisory 43, informational 2; 5 session-scoped |
| Q20 | `grep -rn 'v_best_practice\|v_determination_provenance\|v_item_provenance\|v_pending\|v_divergence\|v_code_floor_only\|v_source_reach_all' --include=*.py scripts schemas .claude` | 10 hits: comments, the reproducibility audit, one test stub, `db.py` docstring; no query |
| Q21 | `q("select name from sqlite_master where type='view'")` | 23 views |
| Q22 | on the scratch copy after the parameter 3 run: `select x.jurisdiction, count(*) from specification_extraction_links l join source_value_extractions x using(extraction_id) where l.specification_id=(select max(specification_id) from specifications) and l.role='governing' group by 1` | 20 codes + 1 NULL over 35 rows |
| Q23 | `q("select count(distinct claimed_unit) from source_value_extractions where parameter_id=3")` | 32 |
| Q24 | `q("select extraction_id, claimed_value from source_value_extractions where extraction_id in (72,80)")` | `(72, '30,0')`, `(80, 'viisi prosenttia')` |
| Q25 | `q("select e.ref_id, e.pub_title, e.pub_title_en, e.lang_detected, e.verification_status, v.author_display from evidence_sources e join v_evidence_authors v using(ref_id) where lower(e.lang_detected) in ('ja','ko')")` | 6 rows; `REF-00989` displays `白倉 栄`; `REF-01019`/`REF-01031` same title |
| Q26 | `q("select parameter_id, claimed_unit, count(*) from source_value_extractions where parameter_id in (4,12) group by 1,2")`; `q("select claimed_value, claimed_unit, claim_text from source_value_extractions where extraction_id=182")` | param 4: mm 12, m 11, cm 1; param 12: m 13, mm 6, cm 1, NULL 1; 182: `915`, `mm`, "…36 inches (915 mm) minimum." |
| Q27 | `q("select extraction_id, jurisdiction, claimed_value, claimed_unit, comparator, claim_text from source_value_extractions where ref_id='REF-00990'")` | extractions 22, 23 |
| Q28 | per table, per column: `select count(*) from T where C is not null and C <> ''` = 0 | list in G.4 |
| Q29 | parse every `retrieval-log/*/manifest.jsonl`, collect `ref_id`; intersect with `evidence_sources.ref_id`; `q("select count(*), count(distinct ref_id) from source_scans")` | 1101 records in 32 manifests, 111 with `ref_id`, 49 of 59 sources covered; `(18, 11)` |
| Q30 | per table: `pragma table_info`, `pragma foreign_key_list`; mark presence/FK of `parameter_id`, the four lens columns, `jurisdiction`, `language`, `slug`, `ref_id` | matrix summarised in D.1 |
| Q31 | `python3 -c "import sys; sys.path.insert(0,'.'); from schemas.enums import JurisdictionCode as J; print(len(list(J)))"` | 36 |
| Q32 | `q("select count(*), count(distinct language), count(distinct jurisdiction), sum(scope_status is not null) from lang_jur_map")`; unreachable = rows of `v_research_scope` whose jurisdiction is not an enum member | `(70, 19, 48, 0)`; 19 rows over 17 jurisdictions |
| Q33 | `q("select count(*), sum(observation_id is not null), count(distinct language), sum(jurisdiction is not null) from term_aliases")`; `q("select alias_type, count(*) from term_aliases group by 1")` | `(2382, 0, 15, 249)`; TRANSLATION 996, SYNONYM 1119, NARROWER 146, BROADER 70, DOMAIN 49, DEPRECATED 2 |
| Q34 | `q("select language, count(*) from search_executions group by 1")`; `q("select lang_detected, count(*) from evidence_sources group by 1")` | mixed case in both; `HR` 1 search; `lang_detected` NULL on 8 sources |
| Q35 | `q("select jurisdiction, count(*) from source_locators group by 1 order by 2 desc limit 8")`; `q("select status, count(*) from source_locators group by 1")` | NULL 403, `—` 89, `INT` 26, …, URLs; REFERENCE-ONLY 879, RETIRED 13, PROMOTED 1 |
| Q36 | `q("select target_population, match_grade, count(*) from evidence_population_match group by 1,2")` | MOB/PROXY 32, MOB/PARTIAL 23, MOB/EXACT 4, MS/PARTIAL 1, SCI/PARTIAL 1 |
| Q37 | `q("select o.observation_id, o.ref_id, o.language, o.surface_form, a.outcome, a.term_id from observed_terms o left join term_adjudications a using(observation_id) where o.language<>'EN' order by 3,1")`; `q("select outcome, count(*) from term_adjudications group by 1")` | 34 rows (33 observations; one carries two adjudications) over 10 languages; NAMES-EXISTING 46, DEFERRED 24, NOT-OURS 14, NAMES-NEW 6; 8 observations unadjudicated |
| Q38 | `q("select p.parameter_id, count(distinct a.language) from base_parameters p left join term_aliases a on a.term_id=p.term_id group by 1")` | parameter 12 → 0; others 13–15 |
| Q39 | `q("select count(*) from terms where canonical_en glob '*[^ -~]*'")` | 0 of 94 |
| Q40 | `q("select term_id, alias, language, alias_type from term_aliases where alias in ('傾斜路','hellingbaan','勾配')")` | `傾斜路` and `hellingbaan` under `TERM-001`; `勾配` absent |
| Q41 | the UNWRITABLE derivation in CLAUDE.md §4, verbatim | 3 lines: `identity_medical_map.medical_code`, `icf_medical_map.medical_code`, `connection_targets.con_id`; 12 empty tables |

Engine runs (C.2) and the audits (F) are commands, given in those sections. Scratch artefacts of the engine runs are in
the harness scratch directory `/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/`
(`cell_<param>_<lens>.{db,sql,json}`), outside the repository and not committed.
