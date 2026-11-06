# Pipeline batch 2: the Anthropometry of Wheeled Mobility report admitted; turning, passage, door and force figures from it and from three non-English codes

**Session id:** `session_2026-11-06-pipeline-batch-2`
**Branch:** `ccr-f9662223-3a0e7g` (restarted from `main` after PR #211 merged)
**Session kind:** research (rows only). No schema, script or check change. The tooling gaps found are listed in section 4 and not patched (CLAUDE.md rule 10).
**Pointers:** `sessions/LATEST` and `sessions/LATEST-RESEARCH` move to this session.

**Derive every figure.** Re-run the command beside a number rather than trust the sentence.

## 1. What this session did

The request was again "perform pipeline batch", with no scope. The reading taken was the next one the previous session left open: parameters 4 to 11 still rested on few sources, and the previous batch's own searches had named a primary measurement study it could not reach. This batch admitted that study and read three more held codes in other languages against the same parameters.

- **Admitted:** the Anthropometry of Wheeled Mobility Project Final Report (IDeA Center, University at Buffalo, for the US Access Board, 31 December 2010), 173 pages, retrieved from the authoring centre's site and admitted as **REF-00468**, the stash id that already held its title (the stash row carried an unrelated URL, the GAP-008 defect). Filed `grey`, tier 3. The tier is disputed (section 2).
- **Read, no admission:** Orden TMA/851/2021 (Spain, REF-01028), the Korean Enforcement Rule Annex 1 (REF-01031) and Decreto-Lei 163/2006 pages held (Portugal, REF-01032), all with their persisted texts from batch 23.
- Rows: `select ref_id, parameter_id, count(*) from source_value_extractions where created_by_session = 'session_2026-11-06-pipeline-batch-2' group by 1, 2`. Searches: `select exec_id, query_text from search_executions where created_by_session = 'session_2026-11-06-pipeline-batch-2'` (three web searches; the first, aimed at Co-1, found no disabled-persons-organisation source).
- Observations 96 to 98 harvested from the report and adjudicated: one NAMES-EXISTING (TERM-003), two DEFERRED. A width at a 90-degree turn and a turning-clearance family are the owner's to define; nothing was minted.

## 2. The adversarial pass and what it changed

Pass 9, a read-only critic against commit `4194f981`: eighteen sustained findings, eleven survived (`select verdict, count(*) from adversarial_findings where pass_id = 9 group by 1`). Thirteen are REPAIRED by a second migration; five are left PROVISIONAL-DISPUTED. The substantive ones: the first scan of the report said it states no door clear width and no operating force, and it states both (860 mm; 9 N and 22.2 N); the Portuguese scan said parameter 6 was not on the held pages and page 20 states 22 N; a Korean row cited item 8 for a clause in item 13; the harm statement in the admitted report reached no flag; two relaxation clauses were filed as claims against batch 23's precedent of filing them as conditions. Twelve omitted figures were added, notes and locators corrected where the writers allow, the two relaxation rows became conditions with edges, and the population match was lowered from EXACT to PARTIAL.

Left disputed, with reasons on the findings:
- **Lens (findings 171, 172).** The lens on the Korean rows 207 to 210 is inconsistent with prior rows on the same codes and with the item headings, which name persons with disabilities. No writer changes a lens column. The rows added after the pass use MOB where the clause or heading names disabled people, ALL otherwise.
- **Gate scope (166).** The batch gate reads neither scans nor extractions (same as pass 8 finding 153).
- **Parameter for the 180-degree turn width (175).** Filed on parameter 4, while the 1525 mm it is measured against and the 360-degree figures sit on parameter 5. A determination on parameter 5 will not see the 1700 mm figure until the owner defines the term for a width at a turn.
- **Tier (177).** `governance/tier-system.md` line 15 lists `grey` as occasionally T1; `schemas/tier_derivation.py` derives `grey` to tier 3 only.
- **Extraction 211's locator** still reads item 8; the correction is on the row's notes (item 13). **Extraction 193's setting** still reads "whole sample of 495"; its sample is 339 (Figure 3-13).

## 3. Disclosures

- The priors on searches 201 to 203 were stated in the transcript before the searches ran; `log-search` wrote them with the results. WebSearch leaves no payload; the result lists exist only in the transcript. Search 201's count (15) was wrong; the result held 17 links, corrected in its note.
- The scans are `pre-screen`. The report was read in full over about twenty of its 173 pages; the Spanish order over four articles; the Korean annex over items 1, 6, 7, 12, 13; the Portuguese text over pages 9, 10 and 20. `pages_read` on a scan row counts the pages held, not the pages read. Scans 10, 11, 12 and 13 are superseded in part by 15 to 18; the later notes say what changed.
- Every extraction is `skim`, `preliminary`.
- Figures are filed in the unit each source states (metres, centimetres, millimetres, newtons); rows in metres will not compose with millimetre rows until the engine owns a length family (GAP-072).
- The report's own tables are cell sequences without row labels in the text; only sentence-form figures are filed. The 210 cm figure for scooter users at the 180-degree turn straddles a page break and is not filed.
- Citation mining of REF-00468 is deferred in both directions; the bibliography begins at PDF page 170 (the deferral note says 159, corrected in scan 15).
- `harm_finding` is raised on search 203 and on search 197 (previous batch). Extraction 183 (ADA 1525 mm) and the new turning rows keep `contested = 0`; no writer changes that column.

## 4. For the owner

1. How a width at a 90-degree or 180-degree turn is to be named and which parameter holds it (observations 97 and 98; finding 175).
2. Whether `grey` may reach T1 for a controlled primary measurement report (finding 177), and so what tier the Anthropometry report carries.
3. The lens rule for a clause under a disability heading (MOB or ALL), and who re-keys the first rows (findings 147, 171, 172).
4. Tooling gaps, none patched: the gate does not read extractions or scans; no writer amends `contested`, a lens, a title, a setting or a `source_section`; `amend-search --add-result-artefact` cannot link a payload whose host is not in the query text.
5. The IDeA review paper (candidate 151, PMID 20402047) may belong under stash REF-00044, whose title matches and whose DOI differs from PubMed's; unverified.
6. A targeted search for disabled-persons-organisation guidance (Disability Rights UK, Scope, Centre for Accessible Environments) is not done and stays open.

## 5. Every issue, and where it is recorded

Filed as `gaps` rows on 2026-11-06 at the owner's instruction ("explicitly record all issues so that they can be resolved later"). Each row names its evidence, the command that re-derives it, and what resolves it. List them with `select gap_id, category, priority, substr(description, 1, 90) from gaps where gap_id between 'GAP-074' and 'GAP-102'`.

| Gap | Issue |
|---|---|
| GAP-074 | Term and parameter for a width at a turn (observations 97, 98; the 180-degree figures on parameter 4 beside the 360-degree figures on parameter 5) |
| GAP-075 | Tier of REF-00468: `tier-system.md` line 15 against the derivation (`grey` to T3 only) |
| GAP-076 | Lens convention (MOB or ALL) and the rows already filed inconsistently |
| GAP-077 | England-only instrument below `UK` |
| GAP-078 | Parameters 7 and 10 hold no row; parameter 8 rests on one numeric source |
| GAP-079 | No Co-1 source retrieved for door, corridor or turning dimensions |
| GAP-080 | Six staged candidates with no reachable full text; the REF-00044 DOI question |
| GAP-081 | Citation mining of REF-00468 deferred both ways; bibliography page |
| GAP-082 | Stated figures left unfiled; concepts the report names with no observation |
| GAP-083 | The Portuguese decree held as 5 of 20 pages; its turning dimension absent |
| GAP-084 | UK 1500 by 1500 mm spaces not settled as turning spaces; BS 8300 not held |
| GAP-085 | Every scan is `pre-screen`; absence sentences in scan notes are unverified |
| GAP-086 | The DoD gate reads neither scans nor extractions |
| GAP-087 | No writer corrects a lens, locator, setting, `contested`, a candidate's harm flag or title, or a scan note (extraction 211's locator and 193's setting stay wrong on the row) |
| GAP-088 | A result payload links only if the query text names its host; WebSearch leaves no payload (search 201's result count was mis-stated) |
| GAP-089 | `pages_read` counts pages held, not pages read |
| GAP-090 | The verbatim check cannot quote a Korean sentence across a line break |
| GAP-091 | A search prompted by a critic cannot be labelled `adversarial-pass` at write time |
| GAP-092 | Keyword screens missed stated figures in both batches; no figure inventory |
| GAP-093 | `update-locator` rewrites `created_by_session` and `created_at` |
| GAP-094 | Metre, centimetre, millimetre and newton rows with no unit family (extends GAP-072) |
| GAP-095 | Undiagnosed advisory preflight failures; `test_scan_contract` G01 and G02 red on `main` |
| GAP-096 | Adversarial pass 7 still open (carried from the previous session) |

Four older gaps are cross-referenced by appended notes: GAP-034, GAP-056, GAP-061, GAP-072. Not given a gap because it is already a standing rule or recorded where it binds: the stop hook's commit-per-turn loop (CLAUDE.md section 7), and that `log-search` writes a prior with the results (the DoD gate's R8 line says so).

## 6. Resolution analysis of the register (Opus, read-only)

At the owner's instruction the register above was handed to an Opus analyst, told to test each gap's claim before accepting it. Report: `scratchpad/session_2026-11-06-pipeline-batch-2/resolution-analysis-GAP-074-096.md` (per-gap evidence, options, a recommended PR sequence, an owner-decision sheet, what closes with no work, risks). Its verdicts are appended to each gap with `amend-gap`.

- **The register was partly wrong.** Of the 23 gaps the analyst confirmed 5, found 17 partly right and 1 wrong (GAP-090: the verbatim check strips all whitespace, so the full Korean sentences verify and the short quotes were cut by hand; confirmed by running `quote_in_artefacts`). GAP-094's force half and GAP-096's "one open pass" (four are open: 1, 2, 5, 7) were also wrong. The corrections are on the gap rows, and the note this session appended to GAP-056 on the strength of GAP-090 is itself corrected.
- **Six issues the register missed**, now GAP-097 to GAP-102: parameters 4 to 11 have no `accessibility_direction` (nothing can be composed); the ICF and access-need lenses are empty on every row against OR-1 action 2; `v_scan_ledger` counts a pre-screen as a full read, so the batches lowered scan debt on readings the critic disproved; none of the owner decisions is on the owner's page; adversarial pass 5 has undisposed sustained findings; typed columns contradict their notes.
- **Under the owner's 2026-11-06 steer (minimise code, no net-negative requirement)** the analyst sized the whole tooling set at about 23 lines added and 1 removed beyond the already-ruled workplan steps (about 3 and 1 if GAP-086 is closed as accepted), and one view migration; most tooling gaps close as accepted, by prose, or by reusing an existing verb. Each recommendation is marked CLOSE-AS-ACCEPTED, RULE-OR-PROSE, REUSE, DELETE or NEW-CODE in section E of the report.
- **Recommended order:** (A) a tooling PR carrying the ledger predicate, the test-fixture fix, the `claim_text` walk, the two-field amender widening, the deletion of the unread `--contested` flag and one line of scan-procedure prose; (B) the ruled workplan steps for the amender and the length family; (C) doctrine entries for the owner's answers; (D) a data PR setting directions and closing the gaps that need no work; (E) data PRs for read-first full-read scans, then lens fill after OR-1c, mining, Co-1 retrieval and acquisitions.
- **Eight owner questions** are in section B of the report, ordered by what each unblocks. The first three: OR-1c (one row per ICF or need combination, or a link table); the lens for a clause under a disability heading (MOB or ALL); the type of controlled research published as a government report (`clinical` with the grey flag, `grey` tier 3, or a new route).
- Also removed in this commit: `scratchpad/session_2026-11-06-pipeline-batch-2/awm.txt`, a byte-identical duplicate of the registered full text.

## 7. Queued for a later session

At the owner's instruction every fix is deferred to a later session; nothing below was started. The queue is the `gaps` table (GAP-074 to GAP-102) plus the order below, which follows `scratchpad/session_2026-11-06-pipeline-batch-2/resolution-analysis-GAP-074-096.md` section A, revised for the owner's answers of 2026-11-06 (ledger: "Owner rulings 2026-11-06" and "(second)"). Tooling and research ship apart (rule 10); under the owner's steer each tooling item is the smallest code that closes the defect, and several close as accepted or by prose.

1. **Tooling PR A (no ruling needed).** The `v_scan_ledger` predicate requiring `method = 'full-read'` (GAP-099, closes 085 and 089); the `test_scan_contract` fixture fix (GAP-095); optionally a `claim_text` walk in `observation_verbatim_audit.py` (GAP-086); `loc_*` and `source_section` added to the amendable set, and deleting the unread `--contested` flag (GAP-087); one line of scan-procedure prose (GAP-092).
2. **Tooling PR B (already ruled).** Workplan T-1b step 8 (the amender for value, unit and setting; OR-3) and step 9 (the length family; OR-10), closing GAP-072 and GAP-094.
3. **Tooling PR C, the lens link table (OR-1c answered).** Design the smallest table that lets a figure carry several codes of one model; retire the four lens columns writer, then reader, then NULL forward (a column a committed data migration inserts can never be dropped, so grep `scripts/migrations/data_*` first); size it against the minimise-code steer. Unblocks T-3 and the lens fill (GAP-076, GAP-098).
4. **Doctrine PR.** Correct the `governance/tier-system.md` line that lists `grey` as occasionally T1 (GAP-075); update `governance/owner-browser.yaml` so OR-1c reads answered and the open questions are prompts (GAP-100). Attestation if a `decisions/` file is touched.
5. **Research-data PR D.** Set directions for parameters 4 to 11 from quoted source statements (GAP-097); relabel executions 199 and 200 with the existing two-step verb (GAP-091); log the two Europe PMC lookups as executions (GAP-088); dispose adversarial pass 5's findings (GAP-101); correct the typed columns by note (GAP-102); close with reasons the gaps that need no work (088, 089, 090, 091, 093, the six advisory checks of 095, and 094 as a duplicate of 072).
6. **Research-data PRs E.** Full-read catalogue scans with the open pass, held sources first (REF-00468, REF-00992, REF-00987, REF-01028, REF-01031, REF-01018, REF-01015, REF-01014; GAP-078, 082, 084, 085); the whole Portuguese decree and REF-01026 superseded (GAP-083); REF-00468 mining (GAP-081); a Co-1 retrieval at disabled-persons organisations (GAP-079); the lens fill by links after PR C (GAP-076, 098); the six staged candidates only after a library route and the `correct-locator` writer of GAP-030 (GAP-080).
7. **Still the owner's.** Confirm the reading of ALL (ledger item 2); the term for a width at a turn with GAP-068 (GAP-074); sub-national instruments (GAP-077); adversarial pass 7 (GAP-096); a library route for six papers and BS 8300; in-place correction of a locator (GAP-087).

Start with `/orient`, then read the gaps with `select gap_id, category, priority, substr(description, 1, 90) from gaps where gap_id between 'GAP-074' and 'GAP-102'` and the ledger tail. Nothing in this PR changes `scripts/`, `schemas/`, `.github/` or `skills/`.
