# AGONIST-1 BRIEF — research batch 04, accessible circulation, R1 pass (Co-1 / T2 / Co-2)

**Session:** `session_2026-09-01-research-batch-04-accessible-circulation`
**Agent:** AGONIST-1 · **Pass:** R1 (Co-1 / T2 / Co-2), executed FIRST, before any T1 work
**Date executed:** 2026-09-01 · **Slugs:** all four, all with zero prior research
**Deliverable status:** 14 searches executed + 1 deliberate non-search · 3 admissions proposed · 0 database writes

**Vocabulary confirmed read-only** from `search_executions` CHECK constraints (`sqlite3` absent; Python
`mode=ro`):
`target_evidence_type ∈ {clinical, sr_meta, standard_eb, national_fw, code, co1, co2, grey}` ·
`depth_method ∈ {scoping, systematic}` · `mining_direction ∈ {none, backward, forward, both}` ·
`saturation_signal ∈ {none, partial, saturated}` · `engine` is free text with the schema comment
`pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual`.
`target_tier` is an INTEGER 1–6, so **Co-1 and Co-2 cannot be expressed in `target_tier` at all** — the
band is carried only by `target_evidence_type`. Rows below record `target_tier` as `NULL` where the
target was Co-1/Co-2. *(Flagged to the orchestrator: this is a schema fact, not a logging choice.)*

---

## ⚠ PROVENANCE HAZARD — READ BEFORE USING ANY PAYLOAD PATH

`retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/` is **shared with at least
one concurrent agonist**. Files appeared there during my run that I did not create
(`crossref_10.1016_j.ajem.*`, `crossref_10.3130_aija.*`, `europepmc_*`, `doaj_geoerg.json`,
`geoerg2019.pdf`, `s2_10.*`, `unpaywall_10.1155_*`, and others). **Do not attribute any payload to this
brief unless it is on the explicit list in §3.** I took no destructive action on the shared directory.
Recommend the orchestrator namespace future retrieval logs per agent.

---

## 1. QUERY LOG (R8 — verbatim, logged before screening, empties kept)

| # | slug | lang | engine | target_tier | target_evidence_type | verbatim query | found | screened | R14 classification (empties/near-empties) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | accessible-circulation-geometry | en | pubmed | NULL | co1 | `(wheelchair[Title/Abstract]) AND ("built environment"[Title/Abstract] OR "physical environment"[Title/Abstract] OR accessibility[Title/Abstract]) AND ("lived experience"[Title/Abstract] OR qualitative[Title/Abstract] OR participatory[Title/Abstract])` | 56 | 25 returned, 14 full-metadata | Not empty, but **low precision / partial wrong-index**: 0/14 addressed a circulation dimension. Architecture and access-audit literature is largely outside PubMed's scope. |
| 2 | accessible-circulation-geometry | en | consensus | 2 | co1 | `DeafSpace deaf people spatial requirements corridor width signing while walking architecture` | 10 | 10 | Not empty. **Zero quantified spatial parameters returned** — see §7. |
| 3 | stair-ramp-threshold-biomechanics-accessibility | en | scholar (Scholar Gateway) | NULL | co1 | `How do people with energy-limiting chronic illness such as myalgic encephalomyelitis, multiple sclerosis fatigue or post-exertional malaise experience walking distance, ramps and the availability of rest seating in public buildings?` | 15 (12 unique) | 15 | **WRONG INDEX.** Scholar Gateway's corpus is Wiley clinical/health; the semantic match landed on exercise physiology and ME/CFS patient-experience-of-research papers. **0/15 on-topic for built environment.** NOT evidence of absence. |
| 4 | threshold-door-hardware | en | web | NULL | co2 | `AOTA occupational therapy practice guidelines home modifications older adults disabilities evidence-based` | 9 links | 9 | Not empty. |
| 5 | threshold-and-level-access | en | web | 2 | co1 | `Muscular Dystrophy UK Trailblazers report access wheelchair users step free entrance venues` | 10 links | 10 | **Effectively empty for the target cell.** Trailblazers reports found (air travel, public transport, spectator sports) but **no report on building step-free entry**. Well-formed query, right index (the org's own site). **Genuine absence of a Trailblazers publication on this cell**; their reports are transport/venue-attendance framed, not entrance-geometry framed. |
| 6 | threshold-and-level-access | en | web | NULL | co1 | `RNIB Guide Dogs blind people level access flush thresholds shared surface detectability kerb report` | 9 links | 9 | Not empty. **Highest-yield search of the batch.** |
| 7 | threshold-door-hardware | en | web | NULL | co2 | `Royal College of Occupational Therapists "Adaptations without Delay" 2019 guidance home adaptations level access` | 10 links | 10 | Not empty; source retrieved and then **rejected on measurement** (§2). |
| 8 | threshold-door-hardware | en | web | NULL | co1 | `door opening force disabled people unable to open doors 22 newtons evidence study manual wheelchair users` | 9 links | 9 | **EMPTY OF EVIDENCE, full of standards.** Returned US Access Board / ADA National Network factsheets (T6/T5) and four patent documents. **Zero primary or lived-experience evidence on operating force.** Well-formed query; general web index is the right first index for grey/DPO material. Provisional **genuine absence** — see §7 and the deferral row #15. |
| 9 | threshold-door-hardware | en | pubmed | NULL | co2 | `("Occupational Therapy Practice Guidelines"[Title]) OR ("American Journal of Occupational Therapy"[Journal] AND "home modification"[Title/Abstract])` | 13 | 13 (8 full-metadata) | Not empty, but **0/13 bear on a design parameter**. This is the load-bearing negative result of the pass — §7. |
| 10 | threshold-door-hardware | en | pubmed | NULL | co1 | `(intercom[Title/Abstract] OR "door entry"[Title/Abstract] OR entryphone[Title/Abstract] OR "video doorbell"[Title/Abstract]) AND (deaf[Title/Abstract] OR blind[Title/Abstract] OR "hearing loss"[Title/Abstract] OR "visual impairment"[Title/Abstract])` | 3 | 3 | **DELIBERATE ZERO-YIELD, KEPT.** All 3 hits are off-topic (2 military-aviation headset studies, 1 1981 social-psychology study on visual communication). **Query is well-formed** — correct concepts, correct field tags, OR-grouped within concept, AND-ed across concepts. **Genuine absence in the biomedical/rehab index for H-04.** Caveat, stated so it is not overclaimed: PubMed's `query_translation` **silently dropped `"video doorbell"`** (absent from the echoed translation), and the HCI venues where this work would live (ACM ASSETS, CHI) are not PubMed-indexed — see deferral row #15. |
| 11 | threshold-door-hardware | en | pubmed | NULL | co1 | `autistic[Title/Abstract] AND "automatic door"[Title/Abstract] AND sensory[Title/Abstract] AND "built environment"[Title/Abstract]` | **0** | 0 | **DELIBERATE QUERY-SHAPE FAILURE, logged as such.** PubMed ANDs every term; a 4-concept chain in which one term (`"automatic door"`) is a rare exact phrase returns zero **by construction**. This row is **NOT evidence of absence** and must never be cited as such. It is logged to make the distinction in R14 concrete and auditable, and because the probe it stands for (E-11 automatic doors × NDV/AUT, an *unexplored* cross-product cell) is still owed a properly-shaped search. |
| 12 | accessible-circulation-geometry | en | web | 2 | co1 | `"Transport for All" OR "Disability Rights UK" OR "Inclusion London" disabled-led research report step-free access seating rest points fatigue` | 9 links | 9 | Not empty. Transport-framed, not building-framed — staged, not admitted (§6). |
| 13 | accessible-circulation-geometry | en | consensus | 2 | sr_meta | `wheelchair users experiences of corridor width, doorway width and manoeuvring space in housing and public buildings` | 10 | 10 | Not empty. **Highest-value academic search of the batch.** |
| 14 | threshold-door-hardware | en | web | NULL | co2 | `CAOT OR "Occupational Therapy Australia" OR WFOT OR COTEC occupational therapy guideline home modification ramp gradient threshold doorway width dimensions` | 8 links | 8 | Not empty; retrieved CAOT 2024 and then **rejected on measurement** (§2). Run specifically so the Co-2 absence claim in §7 could not be dismissed as untested outside the US/UK. |
| **15** | **threshold-door-hardware** | — | — | — | — | **DELIBERATE NON-SEARCH (`deferred_reason`, R6)** — see below | — | — | — |

**Row 15 — deliberate non-search, with reason (R6: `deferred_reason`, findings must NOT be smuggled here).**
Cell: **H-04** (accessible intercom / video door entry) × the ACM Digital Library corpus (ASSETS, CHI,
CSCW). **Not searched, deliberately.** Reason: this environment has no bibliographic index tool for ACM,
and search #10 established that the corpus where accessible door-entry work would actually live is not
PubMed-indexed. Substituting an open-web query would return vendor marketing for entryphone products,
not evidence, and would enter a **non-replayable** query into the log — which is worse than an honest
gap. The cell is **owed a search**, not closed. Recommend it be handed to a pass with an ACM/DL or
Scopus reach. *(Consensus search #13 returned one ACM paper — Wu et al. 2022, `Proc. ACM Hum.-Comput.
Interact.` — confirming ACM material is reachable **incidentally** through Consensus but not
**systematically**, which is exactly why this is a deferral rather than a claim of coverage.)*

**Screening volume.** ≈140 records surfaced. **62 given substantive screening** (full metadata or
abstract read: 14+10+12+8+3+10 = 57 records, plus 5 primary documents read in whole or part). ≈64
further web-result links triaged on title and snippet. Reported as measured; this is above the 30–60
target because web-result triage is cheap, and I would rather over-report the number than trim it.

**Saturation:** `none` on every row. Four slugs at zero prior evidence and one pass is not saturation,
and claiming otherwise would be the "gate that passed having examined nothing" failure in a new dress.

---

## 2. SCREENING — what was rejected, and why

**Two OT professional-body documents were retrieved in full, read, and REJECTED on measurement.** Both
would have passed a title-match screen. This is the single most important screening result in the pass.

**(a) RCOT (2019), *Adaptations without delay* — REJECTED as an anchor.**
Retrieved in full (5.0 MB PDF, 101,750 chars extracted). Measured by term count over the extracted text:

| term | hits |
|---|---|
| `threshold` | **0** |
| `level access` | **0** |
| `corridor` | **0** |
| `width` | **0** |
| `handle` | **0** |
| `door` | **1** |
| `lever` | **1** |
| `step` | **1** |
| `ramp` | 5 |

All of `door` / `lever` / `step` are **the same single sentence**, a competence-delegation list: *"OTA
AOs can assess and recommend simple level-access showers, stairlifts, half steps, hand rails, ramps,
door widening, lever taps, window winders."* The five `ramp` hits are all demand-and-delay statistics
(*"the greatest demand is for adaptations such as showers, stairlifts and ramps"*). **This is a
service-delivery and triage guide. It contains no design parameter for any of the eleven items in this
batch.** Admitting it would have been admitting a topical source that cannot bear on a determination.

**(b) CAOT (2024), *OT Practice Document: Home Assessment and Modifications* — REJECTED as an anchor.**
Retrieved in full (2 pages, 7,342 chars). Measured: `threshold` 0 · `door` 0 · `width` 0 · `entrance` 0
· `step` 0 · `corridor` 0 · `lever` 0 · `ramp` 1 · `handle` 1. The single `handle` hit is *"D-shaped
cabinet pull handles"* — **cabinet** hardware, no force value, not door hardware. Same shape as RCOT: a
scope-of-practice document.
**Trap named:** its closing line reads *"developed and reviewed in collaboration with diverse
occupational therapists with lived experience and expertise in the respective areas of practice."*
**"Lived experience" here means OTs' lived experience of practice, not disabled people's lived
experience.** Read carelessly this is a Co-1 warrant; it is not one. Flagging it because the phrase is
exactly the kind that a co-production check keyed on strings rather than meaning would accept.

**(c) The whole AJOT / AOTA Practice Guidelines series — REJECTED as out of scope for this batch.**
13 records; 8 read in full metadata. Every one is intervention-effectiveness guidance for a *clinical
population*: stroke, TBI, Parkinson's, MS, Alzheimer's/NCD, autism, OA/RA, low vision, chronic
conditions, children 5–21, early childhood, TKR. **Not one addresses a built-environment dimension.**

**(d) Search #1's PubMed set — rejected item by item.** Wheelchair maintenance and repair services; adapted
ride-on cars; a VR power-wheelchair simulator; gynaecological care barriers; accessible diagnostic
equipment; air travel; MWC training needs; a breast-care-centre interior-design paper that matched only
on the word "wheelchair accessibility" in a list of finishes. Two were kept as staged candidates (§6).

**(e) Search #8's returns — rejected as evidence.** US Access Board *Chapter 4: Entrances, Doors and Gates*
and ADA National Network *Adjusting Doors for Access* are **T6/T5 regulatory-stratum** material, out of
band for an R1 pass; four USPTO patent documents are not evidence of anything about people. The search
summary's "5 lbs ≈ 22 N" gloss is a **restatement of the ADA code floor**, not a finding — treating it
as support for I-01's "≤22 N" would be the convergence-not-evidence trap (tier-system §3) executed on a
single source.

**(f) Search #14's returns — rejected as Co-2.** The numbers that surfaced (1:14 and 1:20 gradients; 35 mm
/ 280 mm / 1:8 threshold ramp; 1000 mm walkway width; 9 m landing spacing) come from **AS 1428.1—2009**
(Australian statutory standard, **T6**), a South Australian government prescriber document (**T5**), and
two commercial sites (`moddy.io`, `medbridgeeducation.com`). **None is Co-2 and none was retrieved as a
payload.** They are recorded here as *not admitted and not verified*, so that a later reader cannot
mistake them for something this pass established.

**(g) Screened and NOT rejected, but out of band → staged (§6):** Geoerg et al. 2019; Huang et al. 2025;
Fredericks et al. 2024; Henje et al. 2021; Childs et al. 2009; Cloete & Rout 2025; Edwards & Harold 2014.

---

## 3. PROPOSED ADMISSIONS — 3

Deliberately three, not five. DR §12.2: a failed batch of 30 remediates far worse than one of 10. Two
plausible fourth and fifth candidates (AOTA 2014; Fredericks 2024) are **staged instead of admitted**,
with reasons given in §6. **Every bibliographic field below comes from a payload retrieved in this
session and saved to disk. Nothing is written from memory. No co-author has been dropped.**

### A-1 · NFBUK (2014) — `co1` — **the strongest Co-1 warrant in the batch**

- **ref_id:** orchestrator assigns
- **Title:** *Access for Blind People in Towns. SS1401* · subtitle on the document: *"Additional guidance
  note to Local Authorities to assist the creation of streetscapes which are fully accessible to blind
  people as required by the Public Sector Equality Duty"*
- **Corporate author:** The National Federation of the Blind of the UK (NFBUK) · **circulated by** the
  Department for Transport
- **Named person on the document:** **Editor: David M Bates, Executive Officer, NFBUK** (Sir John Wilson
  House, 215 Kirkgate, Wakefield, WF1 1JG)
- **Year:** 2014. *Derived from the file's own OLE metadata inside the retrieved payload* — Created
  2014-01-28 13:41, Last Saved 2014-01-28 13:41, Last Printed 2014-01-28 13:38 — and corroborated by the
  document code `SS1401`. **No printed publication date appears in the body text**; recorded as
  `2014 [from file metadata]`, not as a title-page date.
- **DOI:** none (grey/DPO publication, not DOI-bearing)
- **Locator (R3, clause form):** §2.1, §2.7, §2.8, §2.9, §1.3, §4.1 — the document is clause-numbered
- **Tier:** **Co-1**, `evidence_type: co1`. Justification: tier-system §1 defines Co-1 as *"Disability-led
  lived-experience publications — DPOs, named-org … blind … organisation outputs"*. NFBUK is an
  organisation **of** blind people. This is its own publication.
- **CO-PRODUCTION, NAMED (DR-2026-08-31 / D-0178 compliance).** The document states its own
  co-production twice, in its own words:
  1. Overview: *"This short document was prepared by **engineers and blind people from the National
     Federation of the Blind of the UK (NFBUK)** and **edited by technical staff from The Royal National
     Institute for Blind People (RNIB) and the Guide Dogs for the Blind Association**"*
  2. §1.3: *"this information document has been prepared and checked by **various professionals, some of
     whom are now blind**"*
  **Proposed `co1_provenance`:** `dpo_authored_with_named_blind_contributors — prepared by engineers and
  blind people of NFBUK (a blind persons' DPO); technical edit by RNIB and Guide Dogs for the Blind
  Association staff; editor David M Bates, NFBUK Executive Officer`.
  **`published_corpus` would be wrong here and D-0178 forbids it.** The warrant is that blind people
  wrote it, and the document says so.
  **Honest limit:** the blind contributors are **not individually named** beyond the editor. The
  co-production is named *as a class*, not *as persons*. If D-0178 is read to require named individuals,
  this is `unwarranted-pending` and the remedy is correspondence with NFBUK, not a tier drop.
- **Retrieval rung (R10):** DOI n/a → Crossref n/a → **publisher/org direct URL, rung 3, resolved 200**
  (`https://www.nfbuk.org/wp-content/uploads/2016/09/SS_Access_for_Blind_People_in_Towns_1401.doc`,
  `application/msword`, 35,840 bytes). WebFetch on the same URL was **Cloudflare-blocked (interstitial)**;
  `curl` with a browser UA resolved it. `doi_resolution_outcome`: `no_doi_org_url_resolved`.
  `verified_by_tool`: `direct_publisher_fetch` (**not** `crossref` — there is nothing at Crossref to check
  it against, and asserting `crossref` here would be the 2026-08-19 failure mode exactly).
- **Payloads (mine):**
  `retrieval-log/session_2026-09-01-.../NFBUK_Access_for_Blind_People_in_Towns.doc` (raw bytes as received)
  `retrieval-log/session_2026-09-01-.../NFBUK_Access_for_Blind_People_in_Towns.txt` (my extraction)

### A-2 · RNIB (2021) — `co1` — lived-experience survey, 485 respondents

- **ref_id:** orchestrator assigns
- **Title:** *Seeing streets differently: How changes to our streets and vehicles are affecting the lives
  of blind and partially sighted people*
- **Corporate author / publisher:** Royal National Institute of Blind People (RNIB) · **Year:** 2021
  (from the publisher's own filename and document; **no individual authors are printed** — this is a
  corporate-authored report, and I am not inventing any)
- **DOI:** none · **Locator (R3):** p. 5 (Methodology); p. 9 (Detectable kerbs, mobility aids); pp. 19–21
  (The importance of kerbs and crossings); p. 37 (References)
- **Tier:** **Co-1**, `evidence_type: co1` — named-org blind-organisation output under tier-system §1.
- **CO-PRODUCTION, NAMED — AND ITS LIMIT STATED (D-0178).** Proposed `co1_provenance`:
  `lived_experience_survey — RNIB Travel Survey, May 2020, UK-wide self-selecting online survey of blind
  and partially sighted people; report states 485 respondents (p.5) and quotes them directly throughout`.
  **I will not call this co-production without qualifying it.** It is lived-experience testimony
  *collected and analysed by* a blind people's organisation. It is **not** co-authorship, and **not**
  co-analysis by named disabled researchers. That is a weaker Co-1 warrant than A-1's and the record
  should say so. If the orchestrator applies D-0178 strictly, A-2 is `warranted` on the
  organisation-output limb of tier-system §1 and `pending` on the co-production limb.
- **⚠ INTERNAL ARITHMETIC INCONSISTENCY IN THE SOURCE — found by reading, not by assuming.** p. 5 states
  *"485 blind and partially sighted people responded"*, then *"We received 302 responses from blind
  people, and 153 responses from partially sighted people."* **302 + 153 = 455, not 485.** The
  Introduction says *"more than 480"*. **Do not store a single n.** Store `n_reported = 485`,
  `n_component_sum = 455`, `discrepancy = 30`, with this note. Any downstream percentage computed from
  this survey inherits a ±30 denominator ambiguity.
- **Retrieval rung (R10):** DOI n/a → **publisher media URL, resolved 200**
  (`https://media.rnib.org.uk/documents/Seeing_Streets_Differently_report_RNIB_2021.pdf`, 1.3 MB).
  WebFetch could not read the PDF; text extracted locally with `pdfminer.six` (74,043 chars).
  `verified_by_tool`: `direct_publisher_fetch`. `doi_resolution_outcome`: `no_doi_org_url_resolved`.
- **Payloads (mine):** `.../RNIB_Seeing_Streets_Differently_2021.pdf` · `.../RNIB_Seeing_Streets_Differently_2021.txt`

### A-3 · Kapsalis, Jaeger & Hale (2022/2024) — `sr_meta`, **T2** — the synthesis anchor

- **ref_id:** orchestrator assigns
- **Authors, in order, complete, from the Crossref payload (with ORCIDs):**
  1. **Kapsalis, Efthimis** — ORCID `0000-0003-1598-6426` (`sequence: first`)
  2. **Jaeger, Nils** — ORCID `0000-0002-4686-2568`
  3. **Hale, Jonathan** — ORCID `0000-0002-4929-0497`
- **Title:** *Disabled-by-design: effects of inaccessible urban public spaces on users of mobility
  assistive devices – a systematic review*
- **Journal:** *Disability and Rehabilitation: Assistive Technology* · ISSN 1748-3107 / 1748-3115
- **Volume/issue/pages:** **19(3), 604–622** · **DOI:** `10.1080/17483107.2022.2111723`
- **Year — TWO DATES, BOTH RECORDED, NEITHER SUPPRESSED:** `published-online` **2022-08-19**;
  `published-print` **2024-04-02**. Crossref `issued` = 2022. Unpaywall `year` = 2022. **Cite as
  2022 (online) / 2024 (issue)**; storing one silently would create the prose-vs-database drift CLAUDE.md
  §2(b) names.
- **Licence:** CC BY-NC-ND 4.0 (Crossref) / CC BY-NC (Unpaywall) — **the two payloads disagree on the ND
  clause; recorded, not resolved.**
- **Tier:** **T2**, `evidence_type: sr_meta`. Justification: tier-system §2 places systematic reviews and
  meta-analyses at T2. This is a **systematic** review with a defined method and formal appraisal — three
  databases (Scopus, Web of Science, PubMed), 3,980 records screened, **48** peer-reviewed articles
  included, English-language, 2005–2021, quality appraised with the **Mixed Methods Appraisal Tool**.
  It is therefore T2 and **not** the T3 that tier-system §9 assigns to scoping and narrative reviews.
- **Why it bears on a determination, not merely on the topic:** its stated result names the design
  elements themselves — *"Pathway characteristics, boarding ramps, entrance features, confined spaces,
  and service surfaces were deemed to be the least accessible elements."* That is a synthesis-level
  statement across 48 studies about **E-03, E-05, E-06, E-08, E-12** simultaneously, and its conclusion
  — *"the critical role of the design of the built environment as a factor of disablement"* — is the
  disablement claim the guidebook's whole circulation chapter rests on.
- **Retrieval rung (R10), four rungs walked, publisher block NOT accepted as terminal:**
  1. DOI → **Crossref API 200** → full author list, ORCIDs, volume/issue/pages, both dates, licence.
     Payload: `crossref_10.1080_17483107.2022.2111723.json`
  2. Publisher (`tandfonline.com/doi/full/...`) → **403 Forbidden**
  3. PubMed → **PMID 35984675** (found via `esearch` on the DOI); PMC id-converter → *"Identifier not
     found in PMC"* — **no PMC copy**
  4. Unpaywall → `is_oa: true`, `oa_status: green`, repository = Repository@Nottingham →
     **`nottingham-repository.worktribe.com` returns 403** on the landing page and on two guessed file
     paths (Cloudflare). OpenAlex confirms the same single OA location, also no direct `pdf_url`.
  5. **Semantic Scholar Graph API → 200, full verified abstract returned.**
  **Rung that resolved the record:** Crossref (bibliography) + Semantic Scholar (abstract/method).
  `verified_by_tool`: `crossref`. `doi_resolution_outcome`: `resolved_crossref_publisher_403_oa_repo_403`.
  **Full text NOT obtained** — see §8.
- **⚠ GIVEN-NAME DISAGREEMENT BETWEEN INDEXES — recorded, not silently resolved.** **OpenAlex renders the
  first author as "Timo Kapsalis"; Crossref (the publisher's own deposit, carrying the ORCID) and
  Semantic Scholar both render "Efthimis Kapsalis."** I take **Efthimis** on the strength of the ORCID-
  bearing publisher deposit plus S2 agreement, 2 payloads to 1. **This is exactly the class of field that
  was fabricated on 2026-08-19**, so it is flagged rather than smoothed over. If the orchestrator wants
  certainty, resolve `0000-0003-1598-6426` at orcid.org.
- **Payloads (mine):** `crossref_10.1080_17483107.2022.2111723.json` · `s2_kapsalis.json` ·
  `unpaywall_kapsalis.json` · `openalex_kapsalis.json` · `pubmed_esearch_kapsalis.json` ·
  `pmc_idconv_kapsalis.json` · `crossref_query_kapsalis.json` · `nott_probe.html` (the 403 body, kept as
  proof the rung was walked)

---

## 4. POPULATION GRADING (R13) — one row per admission

**Every grade below is a grade against the population *served* by the items, which is disabled people in
buildings. No admission is EXACT.**

| # | population SERVED (item links + probed) | population OF STUDY (as the source itself states it) | grade | mismatch note |
|---|---|---|---|---|
| **A-1** | BLIND, DEAFBLIND (E-06, E-05); **and, as an unexpected connection, MOB/SCI/DEM whose interests point the other way** | Blind people and guide-dog owners **in UK street environments**. No sample: this is a DPO consensus/guidance document, not a study, with n unstated. | **PARTIAL** | Two mismatches, both material. **(i) Setting:** the source is about **kerbs between footway and carriageway**; the items are about **building thresholds and entrances**. The *mechanism* — loss of a detectable vertical datum for cane and guide-dog navigation — transfers; the *setting* does not. **Do not let a 100–150 mm street kerb value migrate into a building-threshold determination.** (ii) **Population subset:** §1.4 explicitly splits blind people into guide-dog users (*"a small number"*) and long-cane users (*"the majority"*), and §2.7–2.8 argue chiefly from **guide-dog** behaviour. Guide-dog users are a minority within BLIND, so the strongest claims rest on the smaller subgroup. Nothing at all is said about **partially sighted** people, **DEAFBLIND**, or people with residual vision using contrast rather than touch. |
| **A-2** | BLIND + partially sighted (E-06, E-05, E-07); DEAFBLIND untested | **485 (or 455 — see §3 A-2) blind and partially sighted UK adults**, self-selecting online survey, May 2020. Composition **302 blind / 153 partially sighted**. The report itself states the sample **over-represents registered-blind respondents** relative to the UK registered population (which is ~50/50). | **PARTIAL** | Four mismatches. **(i) Setting:** streets, not building entrances — same transfer caveat as A-1. **(ii) Self-selection:** an online, self-advertised survey; the report concedes it *"is likely to exclude the experience of those people with sight loss who do not use the internet"*, i.e. it under-samples older and poorer blind people, who are plausibly the most affected by circulation barriers. **(iii) Known skew:** blind over-represented vs partially sighted — the report says so itself, to its credit. **(iv) Timing:** fielded May 2020, mid-pandemic, when walking patterns were abnormal. **(v)** No disaggregation by additional impairment, so DEAFBLIND is invisible in the data. |
| **A-3** | MOB, SCI, LMB, and by item-link BLIND/DEM/COM/PAIN (E-03, E-05, E-06, E-08, E-12) | Users of **Mobility Assistive Devices**, synthesised from **48 studies, 2005–2021, English only**; the review states its included studies *"mostly focused on **wheelchair users** residing in **high-income countries**."* | **PROXY for every non-wheelchair population; PARTIAL for MOB/SCI** | The review **self-declares** its two skews, which is why it is trustworthy and why it must be graded down. **(i) Device skew:** "MobAD users" is broader than wheelchair users, but the underlying corpus is not — so any read-across to walking-frame, crutch, cane, or prosthesis users (**LMB**, **PAIN**, **VES**, **MS**) is **PROXY**. **(ii) Geographic skew:** high-income countries only, so it cannot speak to the global majority of disabled people. **(iii) Language skew — an R5 point:** English-only inclusion, 2005–2021. Under R5, non-English peer-reviewed work is **academic**, not grey; a review that excludes it has excluded evidence, not noise. **This is a ceiling on the review, and the guidebook should record it as one.** **(iv)** Populations with no mobility-device involvement at all — **DEAF, DEAFBLIND, AUT/NDV, ID, MH, BAR, LPA, TALL** — are **MISMATCH**: the review says nothing about them and must not be cited for them. |

---

## 5. HARM / FAILURE / INADEQUACY FINDINGS (R7) — first-class, with locators

**H-1 · ZERO-STEP LEVEL ENTRY REMOVES THE NAVIGATIONAL DATUM BLIND PEOPLE USE. THIS IS THE BATCH'S
CENTRAL FINDING AND IT CONTRADICTS AN ITEM NAME.**
Item **E-06** is named *"Level Entry (Zero Step at All Accessible Entrances)"* and its taxonomy links
**BLIND** with `applicability = applies`. Two Co-1 sources say, in their own words, that removing the
level difference **harms** blind people:
- NFBUK §2.8: *"When a guide dog steps over a kerb, the vertical movement of his harness handle tells the
  owner that their next step will be up or down a kerb. **With a low kerb this vertical handle movement
  is imperceptible and the guide dog owner may then be presented with an unexpected tripping hazard.**"*
- NFBUK §2.7: *"**Guide dogs may not recognise lowered or removed kerbs, and walk across them instead of
  stopping as they are taught, thereby endangering their owners.**"*
- NFBUK §2.9: *"**Guide dogs, white cane users and also many motorists will not recognise a coloured or
  textured line across a flat surface as indicating the edge of a footway.**"* — this is the direct
  refutation of the standard designer's substitute for a level change.
- RNIB p. 19: *"**Research shows that kerbs with an upstand of less than 60mm are unlikely to be
  detectable to blind and partially sighted people (Childs et al., 2009).**"* and *"A few slabs of tactile
  paving in a large area of level surface does not have a clear message and is difficult or impossible for
  blind or partially sighted people to find."*
- RNIB p. 20, respondent verbatim: *"**[On] flat surfaces I cannot detect where I am, I cannot tell if I
  am on the road or pavement, I cannot find any pavement markings to get across a busy road via a
  crossing.**"*
- RNIB p. 19, respondent verbatim: *"I am a white cane user and severely sight impaired, so when
  travelling I rely heavily on tactile clues such as raised kerbs and tactile paving. **Without these,
  independent travel would be impossible for me.**"*
**What this does and does not establish.** It does **not** establish that a zero-step building entrance is
wrong — level entry is load-bearing for wheelchair and mobility-aid users and A-3 supports that. It
establishes that **"zero step" and "detectable" are in tension, that the tension is evidenced on the
blind side by Co-1 sources, and that E-06's `applies` link to BLIND encodes an assumption the evidence
contests.** The synthesis owes an explicit resolution — most likely a *detectable-but-traversable*
threshold treatment, tonal-contrast plus tactile, which neither source specifies for buildings. Under the
owner ruling of 2026-08-24, applicability is an **output** of synthesis; here is a case where the input
link and the evidence point in opposite directions.

**H-2 · THE 60 mm DETECTABILITY FLOOR AND THE 100–150 mm STREET NORM ARE BOTH ON THE RECORD, AND BOTH
EXCEED ANY "FLUSH" THRESHOLD.**
RNIB p. 19: *"The standard height kerb in the UK has a **120mm** (around 5 inch) upstand, which is widely
recognised as detectable."* + the 60 mm floor above. NFBUK §2.1: *"Standard height kerbs (**100–150mm**
high)."* **Locators:** RNIB p. 19; NFBUK §2.1. **Both figures are street values and must be flagged
`[UNVERIFIED-QUANT]` for any building-threshold use** — the 60 mm figure is a *citation-of-a-citation*
(RNIB citing Childs et al. 2009), and I could not retrieve Childs et al. (see §6, C-5).

**H-3 · CORRIDOR CAPACITY MODELS DERIVED FROM NON-DISABLED CROWDS DO NOT HOLD WHEN WHEELCHAIR USERS ARE
PRESENT — AN EGRESS-SAFETY FINDING BEARING ON E-08.**
Geoerg, Schumann, Holl & Hofmann (2019), *J. Advanced Transportation* 2019:1–17, DOI
`10.1155/2019/9717208` (Crossref-verified, §6 C-1). From its abstract: *"the empirical relations … are
**strongly affected by the presence of participants with visible disabilities** (such as wheelchair
users). We observed an adaption of the overall movement speeds to the movement speeds of participants
using a wheelchair, **even for low densities and free flow scenarios**. … the concept of specific flow
fits for the nondisabled subpopulation but **it is not valid for scenario considering wheelchair users in
the population.**"* **Why this is a harm finding, not a curiosity:** egress capacity for corridors and exit
widths is calculated from specific-flow models. If specific flow is invalid with wheelchair users
present, **corridor and exit widths sized by those models are unsafe for mixed populations** — and E-08's
"≥1200 mm" is a width claim with no stated egress basis. **Out of my band (T1/T3 experimental) — staged,
not admitted — but it should be pulled forward in the T1 pass.**

**H-4 · THE ACCESSIBLE ROUTE IS THE HOSTILE ROUTE — reported harm outside the geometry.**
RNIB p. 6: *"When these issues are not fully addressed, **streets can become inaccessible, putting people
at risk of injury or loss of life.** Even near misses or the perception that areas are inaccessible can
damage confidence and mental health, affecting independence and significantly reducing opportunities for
exercise."* and p. 7, respondent: *"I've had a lot of issues with having to avoid some routes. This has
made me **more dependent on taxis** and other public transport, as it's just not possible to safely walk
to these places."* **This is the avoidance/substitution harm** — the cost of an inaccessible route is not
only difficulty but route abandonment and forced paid substitution. It bears on **E-10 (rest seating)**
and on the whole `accessible-circulation-geometry` slug: a route that is geometrically compliant but
unusable produces the same outcome as no route.

**H-5 · A HARM CLASS THAT IS ENTIRELY UNEVIDENCED — stated as a gap, not as a finding.**
R7 asks me to hunt failure. The prompt named several harms I looked for and **did not find evidence
for**: lifts stranding wheelchair users in fire; post-exertional malaise induced by ramp length; the
"accessible" route being longer and colder; entryphones unusable by Deaf or blind people. **Searches 3,
8, 10 and 12 were the probes and none returned evidence.** I am recording this as an absence rather than
filling it, because an invented harm is worse than a missing one. See §7.

---

## 6. CANDIDATES TO STAGE (R7 / R15) — `search_candidates` rows, NOT admissions

**Every entry marked HYPOTHESIS is a description I have NOT confirmed by reading the source.**

| id | source (verified fields only) | disposition | description |
|---|---|---|---|
| **C-1** | **Geoerg, Paul; Schumann, Jette; Holl, Stefan; Hofmann, Anja** (2019). *The Influence of Wheelchair Users on Movement in a Bottleneck and a Corridor.* **J. Advanced Transportation** 2019, 1–17. DOI `10.1155/2019/9717208`. **Crossref-verified** (`crossref_query_geoerg.json`, mine). | **REHOME** → T1/T3 pass, slug `accessible-circulation-geometry` (**E-08**) | **NOT a hypothesis** — the quoted claims in H-3 are from the retrieved abstract. **The single highest-value staged item in this batch.** Controlled large-scale movement experiments with wheelchair users in corridors and bottlenecks; directly addresses E-08's width question with an egress-safety mechanism. Out of the R1 band (primary experimental, not Co-1/T2/Co-2) — **which is the only reason it is not an admission.** Flag: **`geoerg2019.pdf` in the shared retrieval-log is NOT mine** (see the provenance warning) — re-retrieve before use. |
| **C-2** | **Huang, Yizhe** et al. (2025). *Measuring spatial accessibility for wheelchair users: A case study in a Chinese campus.* **PLOS One**. Open access (CC BY). Author list **NOT verified beyond the first author** — Consensus rendered it "Yizhe Huang et al." and **I did not run a Crossref lookup**. | **PENDING-VERIFICATION** → then REHOME to T1/T3, slug `stair-ramp-threshold-biomechanics-accessibility` (**E-03**) | From the retrieved Consensus abstract: n=30 students with wheelchair experience; measured travel speeds **1.03 m/s assisted vs 0.67 m/s unassisted**; *"For unassisted wheelchair users, it was challenging for them to pass through the curb ramps with slopes steeper than 1:5."* **Read that carefully: 1:5 is a *failure* threshold, not a best-practice gradient** — it says nothing in favour of E-03's "≤1:20" and must not be cited as if it did. **HYPOTHESIS** that the paper contains gradient data at gentler slopes. **Do not store any author beyond "Huang, Yizhe" without a Crossref/PLOS payload.** |
| **C-3** | **Fredericks, Jerome P.; Visagie, Surona; van Niekerk, Lana** (2024). *A qualitative exploration of community mobility experiences of wheelchair users.* **African Journal of Disability** 13. DOI `10.4102/ajod.v13i0.1253`. **Crossref-verified** (`crossref_query_fredericks.json`, mine). Note: Consensus rendered this as "Jerome P Fredericks et al." — **the full list is three authors**, recovered only because I checked. | **REHOME** → a housing/transport slug; **retain the Co-1 flag** | **Genuinely co-produced**: the abstract describes a **"co-operative inquiry"** with wheelchair users, caregivers, minibus-taxi drivers and community stakeholders as **"co-researchers"**, whose *"purpose … was to allow co-researchers to find their voice and develop solutions."* That is a **stronger co-production warrant than either admitted Co-1 source**, and it is from South Africa, correcting the high-income skew in A-3. **Not admitted only because it is off-slug** — its subject is minibus-taxi access and community mobility, not corridor, ramp, door or threshold geometry. Admitting it would be padding. **Recommend it be picked up wherever community mobility is slugged.** |
| **C-4** | **Henje, Catharina; Stenberg, Gunilla; Lundälv, Jörgen; Carlsson, Anna** (2021). *Obstacles and risks in the traffic environment for users of powered wheelchairs in Sweden.* **Accident Analysis & Prevention** 159:106259. DOI `10.1016/j.aap.2021.106259`. Authors from the **PubMed metadata payload**. | **REHOME** → T3, slug `stair-ramp-threshold-biomechanics-accessibility` (**E-03, E-07**) | From the retrieved abstract: 13 powered-wheelchair users aged 20–66, video + in-depth interview, Haddon Matrix analysis; identifies *"uneven surfaces, **differences in ground levels, steep slopes**, as well as interactions with other road users and the influence of **weather conditions**"*. Bears on E-03 (gradient), E-07 (surface), **E-05 (weather protection)**. **HYPOTHESIS** that it contains any quantified gradient or surface value — the abstract has none. Setting is traffic, not building. |
| **C-5** | **Childs, C.R.; Boampong, D.K.; Rostron, H.; Morgan, K.; Eccleshall, T.; Tyler, N.** (2009). *"Effective Kerb Heights for Blind and Partially Sighted People".* Accessibility Research Group, Civil, Environmental and Geomatic Engineering, University College London. **Citation transcribed verbatim from the RNIB 2021 reference list (p. 37) — a payload I retrieved — NOT from memory.** | **PENDING-VERIFICATION** → then T1/T3, slug `threshold-and-level-access` (**E-06**) | **This is the primary source under the 60 mm figure that the whole H-1/H-2 finding leans on.** R10 walked: no DOI (institutional report) → the UCL URL printed in RNIB's reference list returns **HTTP 403 with an HTML body**, not a PDF (`UCL_Childs_2009_kerb_heights.pdf` in the log is **6,067 bytes of HTML**, kept as proof of the failed rung — **do not mistake it for the report**). **The 60 mm value is therefore a citation-of-a-citation and is `[UNVERIFIED-QUANT]` until this report is in hand.** Highest-priority retrieval task arising from this pass. |
| **C-6** | **Cloete, Magdalena; Rout, Michael** (2025). *'DeafSpace' in the built school environment: A scoping review.* **Acta Structilia** 32(2), 238–263. DOI `10.38140/as.v32i2.9146`. **Crossref-verified** (`crossref_query_deafspace_school.json`, mine). | **PENDING-VERIFICATION** — **and flagged to the owner, see §7** | Retrieved abstract: JBI scoping-review method; **11 studies from 6 countries**, 72.7% North American; consensus on *"visual connectivity (100%), lighting quality (81.8%), and acoustic management (72.7%)"*; and — importantly — *"an overreliance on technical rather than sociocultural approaches, with **minimal participatory engagement of deaf users**."* **Tier note:** a **scoping** review is **T3** under tier-system §9, explicitly **not** T2 `sr_meta`. **HYPOTHESIS** (abstract only) that it contains no quantified corridor-width parameter — the abstract names none. |
| **C-7** | **Edwards, Claire; Harold, Gill** (2014). *DeafSpace and the principles of universal design.* **Disability and Rehabilitation** 36(16), 1350–1359. DOI `10.3109/09638288.2014.913710`. **Crossref-verified** (`crossref_query_deafspace_ud.json`, mine). | **MISCELLANEOUS** (context, not anchor) | Its own abstract declares **"Method: Commentary."** A commentary is not primary research and not a synthesis — **T3 at best, and it cannot anchor a dimension.** Useful for the doctrine question it raises (whether DeafSpace produces particularist space or generalisable principles), which touches the guidebook's mission framing. **Recorded chiefly so that a later reader does not mistake a well-cited commentary for evidence.** |
| **C-8** | **Siebert, Carol; Smallfield, Stacy; Stark, Susan.** *Occupational Therapy Practice Guidelines for Home Modifications.* **AOTA Press**, published **2014**, ISBN 978-1-56900-459-3, DOI `10.7139/2017.978-1-56900-459-3`. **Bibliography fully verified from two independent payloads:** Crossref API (author order, ISBN, publisher — note Crossref's `issued` is **empty**, so the year does **not** come from there) and the AOTA Digital Library page (*"Published: 2014"*, ISBN, product code 900459, full ToC). | **PENDING-VERIFICATION** — **deliberately NOT admitted** | **The one Co-2 candidate whose scope might reach these items — and I could not read it.** Paywalled; only front matter, abstract and ToC retrieved. The publisher's own abstract frames it as *"an overview of the occupational therapy **process** and best practices for home modification **interventions**. Topics include **service delivery concepts, team involvement**, the home as a context for practice, and **involving family members**"* — the same process framing that got RCOT and CAOT rejected. Its ToC shows **"Best Practices and Summaries of Evidence" (pp. 43–53)** and **"Appendix D. Evidence Table" (pp. 67–89)**, which are the only places dimensional content could live. **Any statement that this book contains a corridor, ramp, threshold or door-force value is a HYPOTHESIS and I do not make it.** Admitting an unread source to fill the Co-2 leg of R1 would be filling a slot rather than finding evidence. **Recommend: obtain pp. 43–53 and Appendix D, then admit or discard.** |
| **C-9** | **Transport for All** (UK disabled-people's-led organisation) — disabled-led research programme on transport, incl. rest points for people with energy-limiting impairments. **No specific report identified; no publication payload retrieved.** | **PENDING-VERIFICATION** | **HYPOTHESIS**, from search-result snippets only: TfA's disabled-led research reports discuss *long distances between barriers and platforms* and *absence of information about rest areas* as barriers for people with energy-limiting impairments. **This is the closest thing to Co-1 evidence for E-10 (rest seating) that this pass located, and I could not pin it to a document.** No title, no date, no author, no URL to a report — **do not store any of those.** Task: identify the actual TfA publication. |
| **C-10** | **Muscular Dystrophy UK — Trailblazers** (network of 400+ young disabled people; disabled-led). Reports located on **air travel**, **public transport**, **assistive technology**, **spectator sports**. | **OUT-OF-SCOPE** for these four slugs | Recorded so the empty search #5 is not re-run. **HYPOTHESIS** from snippets: the spectator-sports report states *"One in four say that venue access, including parking, is the number one reason for not attending more sporting events"* — which would touch **E-04 (accessible parking)** if verified. **No report payload retrieved; that figure is unverified and must not be stored.** Trailblazers is a strong Co-1 source class that has **no publication on entrance geometry**. |
| **C-11** | **PubMed record PMID 35299240** — *Occupational Therapy Practice Guidelines for Adults With Chronic Conditions* (Fields, Beth; Smallfield, Stacy), AJOT 76(2), 2022. | **OUT-OF-SCOPE** (content) — **but log the defect** | **A DATA-INTEGRITY TRAP, verified by probe, not assumed.** This PubMed record carries DOI **`10.5104/ajot.2022/762001`** — prefix **10.5104**. The duplicate record **PMID 35311934** for the same article carries **`10.5014/ajot.2022/762001`** — prefix **10.5014**, AJOT's real prefix. I probed all three plausible strings against Crossref: `10.5014/ajot.2022/762001` → **200**; `10.5104/ajot.2022/762001` → **404**; `10.5014/ajot.2022.762001` → **404**. **A batch that trusted PMID 35299240's DOI would have stored a permanently dead identifier while a `verified_by_tool='pubmed'` flag asserted it was checked** — structurally the 2026-08-19 failure. Payloads: `crossref_probe_10_5014_ajot_2022_762001.txt`, `crossref_probe_10_5104_ajot_2022_762001.txt` (both mine). |

---

## 7. MY ADJUDICATION OF VALUE

### 7.1 What actually bears on a determination, and what is merely topical

**Bears on a determination:**
- **A-3 (Kapsalis, Jaeger & Hale)** is the only source in the pass that speaks at synthesis level across
  48 studies and *names the design elements* — pathways, ramps, **entrance features**, confined spaces,
  surfaces — as the least accessible. It can anchor the *existence and ranking* of the barrier classes
  for E-03/E-05/E-06/E-08/E-12. **It cannot anchor a number**, and nothing I retrieved suggests it
  contains one.
- **A-1 and A-2** bear on a determination **about E-06 specifically, and they bear against the item's own
  name.** That is their value. They do not tell us what a threshold should be; they tell us that
  "zero step, universally" is a determination the evidence will not simply hand over.
- **C-1 (Geoerg et al.)**, though out of band, bears on E-08 more directly than anything I admitted.

**Merely topical, and I say so rather than admitting it:**
- **The entire OT professional-body corpus** (RCOT 2019, CAOT 2024, AOTA 2014, and the 13-strong AJOT
  Practice Guidelines series). Every one of these matches the *topic* of home modification and
  accessibility. **Not one carries a design parameter.** They are about who assesses, when, with what
  competence, and whether the intervention works — not about what the built thing should measure.
- **Search #12's Transport for All material** — right organisation, right epistemics (disabled-led),
  wrong setting (transport network, not building circulation), and no document pinned.
- **C-7 (Edwards & Harold)** — heavily cited, self-declared commentary.

### 7.2 Where the evidence contradicts the item names

**This is the part DR-2026-08-19 §1 exists for: 42 of 93 item names embed a determination. Three of the
eleven items in this batch had their embedded determination touched by what I found, and in every case
the evidence pushed *against* the name.**

1. **E-06, "Level Entry (Zero Step at All Accessible Entrances)" — contradicted for BLIND.** Two Co-1
   sources, in their own words, say removing the level change removes the datum blind people navigate by
   and creates a tripping hazard (H-1). The word doing the damage in the item name is **"All."** The
   determination that survives is not "zero step everywhere" but "level *and* detectable", and **no
   source I retrieved says how to do both at a building entrance.** That is a real, open design question
   the guidebook is well placed to pose — and posing it is the mission ("get people to ask the right
   questions").
2. **E-08, "Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)" — unsupported in this pass,
   and undermined from an unexpected direction.** Nothing in the Co-1/T2/Co-2 bands produced a corridor
   width. Meanwhile C-1 indicates the *flow model* that width figures are conventionally derived from
   **does not hold** when wheelchair users are present. So 1200 mm is currently a number with, on this
   evidence, **no anchoring in this batch at all**. It should be treated as a code-floor convergence
   value (tier-system §3) until the T1 pass says otherwise.
3. **I-01, "Hardware Throughout (Lever, D-Pull, One-Hand Operable, ≤22 N)" — the ≤22 N is, on this pass's
   evidence, a restatement of the ADA 5 lbf code floor and nothing else.** Search #8 returned the code
   and four patents. Search #14 returned Australian standard values. **Not one piece of primary or
   lived-experience evidence about what force disabled people can actually exert on a door was found.**
   Storing "≤22 N" as best practice on this basis would be convergence-not-evidence with a sample size of
   one jurisdiction.

### 7.3 What is genuinely absent from the literature, versus absent from my search

**I have tried hard to keep these two apart, because conflating them is how a research programme
manufactures false confidence.**

**Genuinely absent (well-formed query, right index, nothing there):**
- **Co-2 has no design-parameter content for circulation. This is a property of the OT professional-body
  literature, not of my searching.** I tested four bodies across two continents — AOTA (US, book + the
  13-record AJOT guideline series), RCOT (UK, full text, term-counted), CAOT (Canada, full text,
  term-counted), plus a targeted probe at OT Australia/WFOT/COTEC. **OT professional bodies write CPGs
  about what therapists do, not about what a corridor measures.** The R1 contract requires a Co-2 *pass*;
  it cannot conjure a Co-2 *source* where the genre does not produce one. **The honest output of the Co-2
  leg of this pass is a documented negative, and the guidebook should record it as one** rather than
  leaving a reader to assume the search was never run.
- **Muscular Dystrophy UK Trailblazers has no publication on building entrance geometry** (search #5,
  right index — the organisation's own site).
- **H-04 (accessible intercom / video door entry) has no biomedical- or rehab-indexed literature**
  (search #10). Well-formed, right index for assistive-technology work. **Caveated**, not absolute: the
  HCI venues are not in PubMed, PubMed silently dropped one of my four search terms, and I deliberately
  did not search ACM (row 15). **So: absent from the health literature; status in the HCI literature
  unknown and deliberately left unknown rather than guessed.**

**Absent from my search only — do NOT read these as absence of evidence:**
- **Everything Scholar Gateway was asked for (search #3).** Wrong index, cleanly diagnosed: a Wiley
  health corpus answering a built-environment question with exercise physiology. **The E-10 / E-03
  question — rest seating, ramp length, and post-exertional malaise — remains completely unsearched in a
  suitable index.** Given TERM-053, TERM-054 and TERM-087 are linked to these items, this is the largest
  hole this pass leaves.
- **E-11 × AUT/NDV (automatic doors and sensory response).** Search #11 was a deliberate demonstration of
  a query-shape failure and establishes **nothing**. The cell is untouched.
- **E-04 (accessible parking, 3600 mm), E-01 and E-02 (lifts and platform lifts).** **No search in this
  pass targeted them.** Three of the eleven items in the batch received no Co-1/T2/Co-2 search at all —
  stated plainly so that a later reader cannot infer coverage from the pass's existence.
- **All four slugs in every language other than English.** R5 makes non-English peer-reviewed work
  academic, not grey. **Every one of my 14 searches was `language: en`**, and A-3 is itself an
  English-only review. The pass therefore inherits and compounds an English-language ceiling.

### 7.4 One finding that touches the repository's own governance text — flagged, not asserted

`governance/tier-system.md` §3 carries a worked example: *"Co-1/T2/T3 evidence (DSDG Bauman 2010,
DeafScape Vaughn 2018, **Cloete & Rout 2025**) anchors 2440mm primary corridors."* In search #2 I
retrieved and Crossref-verified that paper (**C-6**: Cloete, Magdalena; Rout, Michael (2025), *Acta
Structilia* 32(2):238–263, DOI `10.38140/as.v32i2.9146`). Three things about it are worth the owner's
eye, and I state all three as **flags requiring the full text, not as claims**:
1. It is a **scoping review**, which tier-system **§9** places at **T3**, not T2.
2. Its abstract reports *"minimal participatory engagement of deaf users"* in the literature it maps —
   which bears on any reading of it as Co-1.
3. **Its abstract does not mention 2440 mm**, or any corridor dimension; the spatial parameters it reports
   consensus on are visual connectivity, lighting and acoustics. **I have not read the full text**, so this
   is a **HYPOTHESIS** that the 2440 mm figure is not in this paper — not a finding. But the guidebook's
   own corridor-width worked example rests partly on it, and **E-08 is an item in this very batch**, so
   the check is cheap and overdue. *(I say nothing about Bauman 2010 or Vaughn 2018: I did not retrieve
   them.)*

---

## 8. WHAT I COULD NOT VERIFY — every unconfirmed field, named

| source | field(s) unverified | why |
|---|---|---|
| **A-1 NFBUK** | **Formal publication date**; individual blind contributors' **names**; whether a later revision of SS1401 exists | The document carries **no printed date**. My "2014" is from the retrieved file's **OLE metadata** (created/saved 2014-01-28) plus the `SS1401` code — recorded as such, not as a title-page date. Contributors are named only as a class ("engineers and blind people from NFBUK"); only the editor, David M Bates, is named individually. |
| **A-2 RNIB** | **Individual authors** (none printed — corporate authorship); **exact month of publication**; **the true sample size** | Corporate-authored; I invented no author. Year 2021 from publisher filename and document. **n is internally inconsistent in the source: 485 stated vs 302+153=455 component sum vs "more than 480" in the introduction** — recorded, not resolved. |
| **A-3 Kapsalis et al.** | **FULL TEXT — not obtained.** Therefore: every specific finding, every number, every table, the per-element evidence counts, and any threshold value inside the review | Four retrieval rungs walked (§3 A-3): publisher **403**, no PMC copy, Nottingham green-OA repository **403** on the landing page and two guessed file paths. **I have the Crossref record and the Semantic Scholar abstract, and nothing else.** All claims I make about it are drawn from the abstract and are labelled as such. |
| **A-3 Kapsalis et al.** | **First author's given name — genuinely contested between indexes** | Crossref (publisher deposit, with ORCID) and Semantic Scholar say **Efthimis**; **OpenAlex says Timo**. I record **Efthimis** on 2-payloads-to-1 plus the ORCID, and flag the disagreement rather than hide it. Resolve at `orcid.org/0000-0003-1598-6426`. |
| **A-3 Kapsalis et al.** | **Licence** | Crossref says **CC BY-NC-ND 4.0**; Unpaywall says **CC BY-NC**. The two payloads disagree on the ND clause. Not resolved. |
| **A-3 Kapsalis et al.** | **Which year to cite** | `published-online` **2022-08-19** vs `published-print` **2024-04-02**. Both recorded; neither suppressed. |
| **C-5 Childs et al. 2009** | **Everything except the citation string.** Authors, title, year and URL are transcribed verbatim from RNIB's reference list (a payload I hold) — **but the report itself was never retrieved** | UCL URL returns **403 with an HTML body**. `UCL_Childs_2009_kerb_heights.pdf` in the log is **6 KB of HTML, not the report** — do not use it. **Consequence: the 60 mm detectability figure is a citation-of-a-citation and carries `[UNVERIFIED-QUANT]`.** |
| **C-2 Huang et al. 2025** | **All authors after the first**; journal volume/issue/pages; DOI | Only Consensus's "Yizhe Huang et al." rendering; **no Crossref lookup run.** Store nothing beyond the first author. |
| **C-8 AOTA 2014** | **All content.** Whether it contains any dimensional value at all | Paywalled. Front matter, publisher abstract and ToC only. **Crossref's `issued` field is empty**, so even the year rests solely on the AOTA library page. |
| **C-9 Transport for All** | **Everything.** Title, author, date, URL of any actual report | Only search-result snippets. No publication identified, none retrieved. |
| **C-10 MDUK Trailblazers** | **The "one in four" venue-access figure**, and every report's bibliographic detail | Snippet only; no report payload retrieved. |
| **§7.4 Cloete & Rout 2025** | **Full text.** Whether it does or does not contain the 2440 mm corridor value attributed to it in `governance/tier-system.md` §3 | Abstract only. My statement that the abstract does not mention it is verified; the inference about the full text is explicitly a **HYPOTHESIS**. |
| **All 14 searches** | **Non-English literature (R5)** | Every search was `language: en`. Nothing about the non-English evidence base for any of these eleven items has been established by this pass. |
| **Retrieval-log directory** | **Provenance of files I did not create** | The directory is shared with a concurrent agonist. Only the payloads explicitly listed in §3 and §6 are mine. |

---

## 9. HOUSEKEEPING

- **No database was opened except read-only** (`mode=ro`, once, to read the `search_executions` CHECK
  vocabulary). `scripts/db.py`, `migrate_db.py` and `emit_data_migration.py` were **not** run.
- **Writes confined** to `scratchpad/session_2026-09-01-.../agonist-1/` and the session retrieval-log
  directory.
- **Two Python packages were installed** into the container to extract PDF text (`cffi`, to repair a
  broken `cryptography` import that made `pypdf` and `pdfminer.six` unusable; then `pdfminer.six`).
  `pip install -r requirements.txt` was **not** run — CLAUDE.md §5 forbids it in this container.
- **`saturation_signal: none` on every row.** Four slugs, zero prior evidence, one pass.
