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
