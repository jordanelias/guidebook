# Catalogue plan, version 2: read every source for every parameter, grow the list safely, then derive items and categories

Prepared 2026-10-09 in the batch 24 session, after the independent critique in `catalogue-plan-critique-fable.md` (same folder). This is a session working paper. It proposes. It decides nothing, records no ruling and changes no file but itself. Version 1 (`catalogue-plan.md`) stays as written; this replaces it for reading and deciding.

---

## Executive summary

**What this is.** A rewrite of the catalogue plan. An independent critique failed version 1 on three of your four requirements. This version is built to meet all four. Nothing happens until you answer section 10.

**The core change.** Every source we hold is read against the whole parameter list, whatever topic folder ("slug") it came in under. Slugs stay what you said: search plans. Each reading leaves a record of which source was read, how much of its text, and against which version of the list. So for every source and every parameter the database can show: figure found, nothing found, or not yet read. When a parameter is added later, that record shows which earlier sources still need reading for it.

**What we already hold.** Far more than version 1 said. Saved files contain the full text of most national codes we admitted, including those of the US, UK, Ireland, Japan, Korea, Portugal, Spain, Sweden, Finland and New Zealand. Where batch 23's texts are partial, it is only because a few pages were pulled from PDFs we hold whole. The first research step needs no downloading.

**Tooling first.** Before bulk additions, one tooling change adds what is missing: ways to retire, merge, rename and un-decline a parameter; a way to add aliases; a check that an observed phrase is really in the source; and a record of each reading.

**Then research.** Small groups of sources, reviewed one source at a time, with no cap on how many figures a source yields. New documents come from the lists we hold, bucket 1 first.

**The catalogue.** For the first release, one item per parameter, grouped into categories you approve once. It shows the questions, what each held code says (marked), qualitative and lived-experience findings, and where reading is incomplete. No determination is published yet.

**Decide first (section 10):**
1. what your answer "2" meant (two readings are possible);
2. whether to keep the nine parameters already added;
3. whether names must still come only from a source's own phrase;
4. whether to approve the tooling list.

---

> ### How to read this
>
> **Order.** Sections 1 and 10 are for deciding. Sections 3, 4 and 6 are the design. Sections 5, 7, 8 and 12 are mechanics for the sessions that carry it out.
>
> **Labels on claims.** **[VERIFIED: how]** means checked in the repository or database for this paper, and the check is named. **[INFERRED]** means reasoned from verified facts but not tested. **[OPEN]** means not settled and not settleable without you or more work.
>
> **Numbers.** Every count sits beside the command that recomputes it (CLAUDE.md rule 7a). The numbers are as of 2026-10-09 and will move. Re-run the command rather than trusting the figure.
>
> **Plain words for the project's terms.**
>
> | Word | Meaning here |
> |---|---|
> | source | A document admitted into the evidence base, such as a building code, a study, a guide or a disability organization's statement. Each has an ID like REF-00987. |
> | slug | A topic folder that searches are planned and filed under, such as `accessible-circulation-geometry`. |
> | term | An entry in the project's vocabulary (a word or phrase with a definition). |
> | parameter | A term promoted to "a measurable design quantity the guidebook takes a position on", such as ramp gradient or door width. Parameters are numbered and a number is never reused. |
> | alias | Another way of writing a term, often in another language. |
> | observation | A record that a source uses a phrase, word for word, at a stated place in it. |
> | adjudication | The recorded judgment of what an observed phrase refers to: an existing term, a new term, not one of ours, or undecided. |
> | extraction | One thing a source says about one parameter, with its quote and location: a figure, a condition, a finding, an argument, or an explicit "sets nothing". |
> | determination | The guidebook's computed position on a parameter for a group of people. Stored in the `specifications` table. None is live today. |
> | scan | One reading of one source against the parameter list (defined fully in section 3). |
> | item, category, element | An **item** is a catalogue entry. A **category** is a browsing group of items. An **element** is the physical thing a quantity belongs to (door, ramp, toilet). |
> | cohort | The group of sources handled in one research session and one pull request. |
> | pull request (PR) | A proposed change you review and merge. A **tooling PR** changes the machinery. A **research PR** adds data. Project rule 10 says they never share a PR, and tooling merges first. |
> | migration | The append-only file that carries database changes into the shared database. |
> | check, gate | An automatic test. **Blocking** stops a merge, **advisory** only reports. A check is **vacuous** when it passes because it looked at nothing. |
> | the batch-completion gate | `scripts/audit/research_batch_dod.py`, also called the definition of done (DoD). Its rules are numbered R1 to R16. The ones that matter here are below this table. |
> | session name | The label stamped on every row a session writes, such as `session_2026-10-09-research-batch-24-parameter-pilot`. Two pointer files hold such names. `scratchpad/CURRENT` names the session running now. `sessions/LATEST-RESEARCH` names the last finished research batch. |
> | ledger | `references/project-standards.md`, where your rulings are recorded. |
> | tiers, markers | T1 is controlled research. Co-1 is lived experience or work by disabled people's organizations (co-primary with T1). T2 is a systematic review or synthesis. Co-2 is occupational-therapy professional guidance. T3 is lower-control research or grey literature. T4 to T6 are standards and codes. The markers are ● confirmed evidence, ◐ standards basis only (T4, T5), and ○ thin or code-floor (T3 grey, and T6 codes without research behind them). |
> | buckets | Your priority jurisdictions. Bucket 1 is UN, ISO, Canada, USA, UK, Germany, Norway, Sweden, Japan and Australia. Bucket 2 is EU, Singapore, New Zealand, Ireland, France, Spain, Portugal, Finland, Netherlands and South Korea. Re-derive with `sed -n '420,424p' workplan/2026-08-18-research-frame-proposal.md`. |
> | tombstone | A source replaced by a better copy. It is kept for history and never read again. |
>
> The batch-completion rules that matter here:
> - **R1:** some lived-experience work is present in the batch.
> - **R9a, R9b:** source IDs do not collide with ones already held.
> - **R11-harvest:** every admitted source has at least one observation.
> - **R13:** every T1 to T3 source has its study population graded against the population served.
> - **R16-adjudicate:** every observation is judged.
> - **R16:** every term a judgment names is promoted or declined.
>
> **K02** is the check that a live determination accounts for every figure on file for its parameter. **C10** is the check that a published value does not rest on an unverified source.
>
> **Where each of your four requirements is met.**
>
> | Your requirement (your words) | Met in |
> |---|---|
> | "Interrogate quality, logic, sequencing and flexibility of pipeline all directions as well as all gates, reads, writes, conditionals." | Section 5 (the graph, with backward edges), section 7 (sequence), section 8 (every gate) |
> | "scrape information across any parameter if it appears in any source no matter the slug. Slugs guide our searches, but they do not guide what we derive and mine from sources!" | Section 3 (scan contract), sections 3.7 and 7.4 (what a slug means, exhaustion by parameter) |
> | "I expect harvesting across multiple terms if a source discusses multiple terms." | Sections 3.3 to 3.5 (closed and open passes, one clause yielding many rows, one phrase naming two parameters) |
> | "Ensure that we can add and expand parameter catalogue as required based on new information we come across." | Section 4 (growth protocol and the tooling it needs), section 5.2 (re-reading old sources for new parameters) |

---

## 1. What changed from version 1, and why

### 1.1 A decision on every critique finding

The critic's findings were checked here before being relied on. Where a finding is rejected or changed, the evidence and the CLAUDE.md section 8 reasoning are given. Section 8 says adding apparatus carries the burden of proof: what wrong thing reaches the guidebook without it, and what reads it.

| ID | What the critic attacked in v1 | Decision | Evidence checked for this paper | What v2 does |
|---|---|---|---|---|
| F1 | Release 0 promised code attributions and evidence state, but no phase before rendering writes extractions | **MODIFIED** (finding accepted; its acceptance test changed) | Every extraction is on one parameter: `select parameter_id, count(*) from source_value_extractions group by 1`. **[VERIFIED: query]** R16 says in its own text that it does not read whether a parameter carries an extraction (`research_batch_dod.py`, the comment ending "is not read either" and the PASS line naming "adversarial standing subject 4"). **[VERIFIED: read]** | The reading phases (P3, P4 in section 7) write extractions for every parameter before anything renders. Release 0 is gated on **no unread source-parameter pairs** over its source set. The critic's test was "at least one extraction per parameter"; v2 does not use it. "No held code sets a requirement" is true and useful content, and forcing a row per parameter would invite padding. |
| F2 | Separate fetch and harvest PRs cannot pass the blocking gate. A harvest-only session examines nothing | **MODIFIED** (accepted; different remedy) | The batch-completion gate run on this session's name fails R1, R9a and R9b with "NOTHING IN SCOPE". It reports R11-harvest, R16 and R16-adjudicate as "EXAMINED: 0". **[VERIFIED: ran it]** The registry runs it blocking against `LATEST-RESEARCH`. **[VERIFIED: registry]** The remediation plan already assumed a read-only session leaves that pointer in place (`process-gap-remediation-plan.md`, line beginning "[ASSUMPTION: a judgement-only session"). **[VERIFIED: read]** | Sessions that fetch new documents also read, judge and dispose of them in the same session and PR. Re-reading documents already held is judged through the session names that admitted them, plus the blocking corpus-wide ratchet (`research_contract_baseline_ratchet`). Every reading session also admits at least one new document through a logged list-driven search, so its own gate has a subject (section 7.3). |
| F3 | One observation per phrase per source, so a phrase used for two quantities is folded into one | **ACCEPTED** | The table's DDL has `UNIQUE (ref_id, surface_form, language)`, and `observe_term` returns the earlier row with `created: False` (`scripts/db.py`, `def observe_term`). **[VERIFIED: read]** The held ADA text uses "clear width" 53 times across different elements. **[VERIFIED: counted in the persisted HTML]** The batch 23 scanner invented an `also_at` field to hold second places (`harvest/es-small.json` in the harness scratchpad). **[VERIFIED: read]** | Tooling T1 makes an observation one sighting: phrase plus place (section 3.5). |
| F4 | Search, candidates, citation mining, coverage and the determination engine are keyed by slug, and nothing maps slugs to parameters | **MODIFIED** | **Accepted:** `search_executions.slug` and `search_candidates.found_under_slug` are NOT NULL. `citation_mining` is keyed per slug. `v_coverage_jurisdiction` groups by slug. **[VERIFIED: DDL]** `slugs.serves_axes` holds one row. All 53 sources link to one slug, all 101 extractions sit under it, and searches used two slugs. **[VERIFIED: query, §12 command S1]** **Rejected, part 1:** removing `--slug` from `assess_cell`. The flag selects no evidence; sources are gathered by parameter (`assess_cell.py`, the argparse comment "NO LONGER 'the slug to gather from'" and `gather_sources`). **[VERIFIED: read]** It is a label, it misleads nothing, and changing it is cost without benefit. **Rejected, part 2:** a slug-to-parameter map. It would be a curated list beside the thing it describes (rule 8). | Exhaustion is judged per parameter and jurisdiction, derived from reading records and logged searches (decision D4, section 7.4). Slug-keyed tables stay as they are, because slugs do guide searches. The "pulled from another slug" follow-up marker waits on decision D1 (section 3.7). |
| F5 | No way to retire, merge, rename or un-decline a parameter. Names and topic labels cannot be amended. Direction is write-once | **ACCEPTED, and widened** | `db.py` has 72 commands and none retires, merges, renames or un-declines. **[VERIFIED: §12 command V1]** Only `definition` and `scope_note` are amendable (`_AMENDABLE_TERM_FIELDS`). `set-parameter-direction` refuses a second statement. **[VERIFIED: read]** **Missed by the critic:** no `db.py` command writes `term_aliases`. Only the 057 baseline migration and a selftest insert into it, so a new language alias has no sanctioned path at all. **[VERIFIED: `git grep -lE 'INTO "?term_aliases"?' -- scripts/`; `grep -n term_aliases scripts/db.py` shows only a reader]** | The minimum lifecycle set ships in tooling T1 before any bulk promotion (section 4.2). |
| F6 | Parameter-to-element is many-to-many, "unassigned" hides leaks, and `terms.domain` is curated free text | **MODIFIED** (accepted; simpler design) | `terms.domain` has no CHECK. **[VERIFIED: DDL]** It files "laundry and utility room" (TERM-084) and "upper limb function and grip" (TERM-088) under `hardware`. **[VERIFIED: query]** Of the ten parameters, at most door width, ramp gradient and ramp run length belong to a single element. The others (operating force, light-reflectance contrast, reverberation time, colour temperature, headroom, turning space, corridor width) span several elements or none. **[INFERRED from the term definitions]** | Release 0 makes **one item per parameter**, so no element table is needed yet (decision D6). Categories come from a registry you approve. A parameter may sit in several categories, each placement with its warrant. A blocking check goes red when an active parameter reaches no category (section 6). |
| F7 | No check that an observed phrase is in the source's text | **ACCEPTED** | The verbatim check has one call site, `add-extraction` (`_require_verbatim`). **[VERIFIED: read]** Of the 88 observations, 34 have their context quote in the source's own files and 37 only in some other file. The remaining 17 are in no saved file at all. 82 of the 88 phrases appear inside their own context quote. **[VERIFIED: §12 command O1, a few minutes' run]** | T1 makes `observe-term` refuse a quote that is not in the source's saved text, with the same recorded exemption route as extractions, plus an advisory backstop over old rows with a baseline. Re-derived full texts carry the source's ID, so matches become scoped. |
| F8 | v1 recorded your words against the wrong questions | **ACCEPTED, refined** | Your "2" answered "Does a preliminary or skim extraction ever govern a published cell?" Your "A" answered "What did you mean by the 90+ cleaned parameters without values?" **[VERIFIED: transcript]** "pull from the major codes, literature and advocacy from major countries" was queued at 06:07:12, before the 06:07:27 message offering "1. Slug by slug / 2. You seed it". It answered your own question about batch 23, so the 1-or-2 choice was never answered. **[VERIFIED: transcript queue timestamps]** | Section 2.5 quotes each answer beside its question. Section 11 ledgers them verbatim. Your "2" is carried as an open ambiguity (D1). The unanswered choice comes back as D3. |
| F9 | Version 1's Part A facts were wrong (saved text, tombstone, missing lead list, worklist double counts) | **ACCEPTED, refined twice** | 49 of 53 sources match a saved file by ID or address. **[VERIFIED: §12 command A1]** The other four are not empty. The full statute text of REF-00990 and REF-00991 sits in e-Gov API files saved without the source ID. The abstracts of REF-00999 (PubMed XML) and REF-01000 (journal page) are held the same way. **[VERIFIED: §12 command A2]** Batch 23's "partial" texts come from PDFs held whole; for example REF-01027's text covers 4 of its 79 pages. **[VERIFIED: page counts]** REF-01026 is a transcription of the decree whose original is REF-01032, and it is not tombstoned. **[VERIFIED: source notes]** The worklist double-counts several standards and has four blank Co-2 rows. **[VERIFIED: read]** | Section 2.2 classifies all 53 sources by what can be read today without fetching. REF-01026 is superseded by REF-01032 before scanning. The lead lists, including `source_locators`, are in section 2.3. |
| F10 | v1's proposed checks were red or vacuous and v1 did not say so | **ACCEPTED** | 8 of the 10 parameters have no adjudication behind their term. **[VERIFIED: §12 command S1]** | Section 8 names, for every check, what it examines, its level and the row that fails it today. |
| F11 | Nine parameter rows reached the branch database with no PR, session record, attestation or review, and with no direction set | **ACCEPTED**; the rows are kept, not reverted | Commit `a8b7c11` carries migration `data_20261009055057_…` with 9 inserts, 0 updates and 0 deletes. **[VERIFIED: read]** It is on this branch only: `git ls-tree origin/main scripts/migrations/ \| grep -c 20261009` gives 0. **[VERIFIED]** There is no `sessions/` record and no attestation. **[VERIFIED: ls]** **Reverting is rejected.** Your 2026-09-16 ruling says "retire in place, never hard-delete". The blocking `identifier_floor_audit` exists because freed numbers get reissued, and parameters 4 to 12 are already named in this session's permanent record (transcript, critique). | Decision D2: you review the nine. Kept rows reach `main` only through a PR with a session record, attestation and your recorded review (phase P1). The wrong note on parameter 12 is annotated (F18). |
| F12 | Documents admitted from lists, with no logged search, pass the gate and leave no coverage record | **MODIFIED** | **Accepted:** no search uses the `lead-index` origin. Two sources have no admission edge (REF-00987, REF-01010), and no check flags this. **[VERIFIED: §12 command S1]** The test named S01 compares candidates with admissions; it does not require an edge. **[VERIFIED: read]** **Corrected:** R13 and R2 apply to tiers 1 to 3 only (`research_batch_dod.py`, "tier BETWEEN 1 AND 3"). **[VERIFIED: read]** A code admission owes no population grade; the critic's "codes = PROXY" does not hold. A `lead-index` search may not carry a target tier (`log_search` refusal "A lookup targets no tier"). **[VERIFIED: read]** So the lived-experience rule R1 is met by admitting at least one Co-1 source per cohort, or by a reasoned waiver. | Every list-driven acquisition is logged with `log-search --origin lead-index`. The no-admission-edge rule becomes a batch-scoped rule in the gate, not a refusal in `add-source`, because `log-search` requires the source to exist before it records the admission. **[VERIFIED: read]** The two old rows are repaired by a backfilled search row. |
| F13 | No record of which source was read for which parameter, so a parameter added later is never looked for in earlier sources | **ACCEPTED; cheaper design** | Parameter numbers are never reused (the AUTOINCREMENT comment in the `base_parameters` DDL). **[VERIFIED]** So a reading record that stores the highest parameter number at reading time says exactly which parameters that reading could have covered. That is one row per source per reading, not one "absent" row per source-parameter pair. The critic's "3 absent rows" counts `extraction_status='absent-confirmed'`; `claim_type='absent'` holds 5. **[VERIFIED: query]** | A reading record plus a derived source-by-parameter ledger, with an advisory scan-debt check (sections 3.8 and 8). |
| F14 | The first live determination turns the next extraction on the same parameter red (K02) | **ACCEPTED** | K02 compares a live determination with every extraction that exists for its parameter "RIGHT NOW" (`test_db_integrity.py`, the K02 block). **[VERIFIED: read]** | "Determine late": no determination on a parameter until its reading debt over the held bucket 1 and 2 sources is zero. After that, any PR adding an extraction on a determined parameter re-runs the engine in the same PR (section 7.6). |
| F15 | "Paywalled codes listed as leads in the evidence-state column" cannot be derived: leads carry no parameter | **ACCEPTED, narrowed** | `research_code_leads` has no parameter column. **[VERIFIED: PRAGMA]** Minor correction: `search_candidates.exec_id` is nullable. **[VERIFIED: PRAGMA]** | No per-parameter paywall column. Release 0 shows, per jurisdiction, "governing instrument not held (paywalled lead)", derived from lead and candidate status. A lead-to-parameter link is not built: nothing would read it that the jurisdiction-level fact does not already serve (section 8). |
| F16 | The 60-extraction cap penalizes breadth, and review at scale was pushed to you without saying so | **ACCEPTED** | The cap was "2 × batch 23's" 30 extractions in the remediation plan's pilot, which its own text calls "discretionary". **[VERIFIED: read]** | Cap removed. The review unit is one source. Cohort size is set by how many sources one independent review can sample. The comparator is findings per source sampled (section 7.7). |
| F17 | v1 would re-key or remove dead item tables that cannot be dropped, relied on a vacuous render check, and forgot several gates | **ACCEPTED** | Committed data migrations insert into `jurisdictional_values` and `item_taxonomy_links` (`data_20260821185244…`, `data_20260901183203…`). **[VERIFIED: grep]** `build_site.py --check` prints "EXAMINED: 0". **[VERIFIED: ran it]** | The item-keyed tables are left alone and nothing new builds on them. The render check is repointed at the new catalogue pages in tooling T2, or deleted if no render ships. Every forgotten gate is in section 8. |
| F18 | Parameter 12's note says "no source adjudication behind it" | **ACCEPTED** | TERM-091 carries a NAMES-NEW adjudication from batch 20 on REF-00992's "going of a flight". **[VERIFIED: query]** | Corrected with an append-only note verb (section 4.2). The correction is recorded in the session record. |
| L5 | "Who it serves stays empty until determinations exist" | **ACCEPTED** | Every extraction carries the four lens columns (identity, ICF, access need, medical), and the table's CHECK requires at least one. **[VERIFIED: DDL]** | Release 0 shows, per source and parameter, which group each finding concerns. It is labelled as the source's own scope, not a determination. |
| L6 | v1 omitted your 2026-09-18 directive | **ACCEPTED** | `grep -rn "adjudicate by all slugs" sessions/` finds line 53 of the batch 15 record. **[VERIFIED: grep -r]** | Quoted in section 2.6. It is the root of the scan contract. |
| L7 | Release 0 was code-first and quantity-only, against the 2026-09-18 call to mine "logics and arguments and qualitative work" | **ACCEPTED** | The table already holds qualitative and argument findings: `select claim_type, figure_role, count(*) from source_value_extractions group by 1,2`. **[VERIFIED: query]** | Release 0 shows quoted qualitative findings, arguments and Co-1 findings beside each parameter. **[OPEN]** An argument about a whole element ("ramps … often generate problems of their own", REF-01000) has no home except attachment to a parameter. Section 6.6 explains. |
| S1 | REF-00999's harm findings cannot be re-checked against its text | **MODIFIED** | Its two extractions match only the PubMed abstract XML (unscoped). The abstract is held; the article is not. **[VERIFIED: §12 command A2]** | Shown with "abstract only" reading scope. The full article may be fetched if a route exists: your 2026-09-25 ruling bars only items with no route. |

The critic's labelled findings map onto the table:
- L1 is F7 and L2 is F8.
- L3 is the worklist double count in F9.
- S2 is F18.
- L8 and S3 survived the attack.
- L4 was not attacked.

### 1.2 Corrections that neither v1 nor the critique made

1. **Markers on code content.** v1 said code attributions would show ◐. The tier system gives ◐ only to T4 and T5. A T6 statutory code is ○ unless research backs it, and your 2026-09-13 ruling is "It is when a code/regulatory input does not have research backing that it gets the empty circle." **[VERIFIED: `governance/tier-system.md` lines 69–71; ledger 2026-09-13]** 20 of the 53 sources are T6 (`select tier, count(*) from evidence_sources group by 1`).
2. **`axes` is retired vocabulary.** v1 offered the 17 `axes` as a grouping frame. On 2026-08-18 you ruled it a bad coined term, "do not relitigate" (CLAUDE.md rule 0's proof), and its rename is scheduled (ledger, 2026-08-26 entry on the demand-layer rename). CLAUDE.md §6 says "never bare axis codes". v2 uses only the ICF and access-need frames. **[VERIFIED: CLAUDE.md; ledger]**
3. **Aliases are mostly unverified.** Of 2,382 aliases, 1,163 are marked model-generated and 880 predate provenance marking. Only 15 (all Indonesian) are verified. **[VERIFIED: `python3 scripts/audit/alias_provenance_audit.py`]** Aliases can guide a reader's eye; they are never evidence (section 3.9).
4. **Language codes disagree in case.** `observed_terms` stores `EN` and `term_aliases` stores `en`. **[VERIFIED: query]** Any matching between them must normalize case.
5. **Two parameter definitions state a direction.** TERM-003's definition is "Minimum space for wheelchair 360° rotation" and TERM-005's is "Maximum force required to operate hardware". The value guard reads names only. Definitions are amendable today with `amend-term`. **[VERIFIED: §12 command V2]**
6. **Answer-shaped names the guard cannot catch.** TERM-022 "level threshold" names a target state, not a quantity, and has no digit for the guard to catch. The held ADA text says "turning space" 57 times and "turning circle" none. **[VERIFIED: counted]** That is why rename must exist before names multiply.
7. **Stale prose in the check registry** (rule 7a). `validate_parameters`'s note says `base_parameters` is empty; it holds 10 rows. `site_pages_fresh`'s note says "93 today"; it examines 0. **[VERIFIED: registry and runs]** Fix when those entries are next touched.
8. **The orchestrator's correction "four sources have no artefact" is right by ID and address but incomplete** (F9 above). All 53 have some saved file, but REF-00997's is only a bot-check page with no content. For four sources the useful bytes are filed without the source ID.

---

## 2. State, re-derived

All figures are as of 2026-10-09. The command that recomputes each one is beside it or in section 12.

### 2.1 Pipeline counts

Run §12 command **S1** (one read-only script). Its results today:

| Stage | Today | What it means for this plan |
|---|---|---|
| Vocabulary | 94 terms; 10 active parameters (ramp gradient, plus the nine added this session); 8 parameters with no adjudication behind their term; 9 with direction unset; 1 term declined (TERM-089 "ramp", as an element) | The list is tiny and mostly unreviewed |
| Aliases | 2,382 across 15 languages; no writer exists | Recognition aid only |
| Research | 191 searches, using 2 slugs; 0 list-driven (`lead-index`) searches; 110 candidates pending verification; 893 rows in `source_locators` | Coverage records exist for two slugs only |
| Evidence | 53 admitted sources, 1 tombstone (REF-01019), 6 unverified, 2 with no admission edge | |
| Observations and judgment | 88 observations, 11 unjudged; 8 terms named by judgments but neither promoted nor declined (TERM-016, -053, -075, -079, -090, -092, -093, -094) | This is the R16 debt, baseline 9 and now 8 |
| Extractions | 101, all on parameter 3 (ramp gradient), all under one slug. 54 preliminary, 14 skimmed, 5 explicit "absent", 28 with a recorded verbatim exemption | Nothing has been read for the other nine parameters |
| Determinations | 8, all retired; 0 live; one open gate on parameter 3 for MOB | K01, K02 and C10 examine nothing |
| Render | `site/` holds no pages; `build_site.py --check` examines 0 | |

### 2.2 What can be read today, source by source

Run §12 command **A1** for the file list and PDF page counts, and **A2** for the four unscoped sources. Classes:

| Class | Sources | What is needed before a full scan |
|---|---|---|
| **A. Full text held and readable now** (web page, statute data or derived text) | REF-00987 (US ADA 2010, 716 kB HTML); REF-00995 (Flemish decree, BE, out of bucket); REF-01016 (NZS 4121 full text, 200k characters; still UNVERIFIED); REF-01017 (Finnish decree); REF-01021 (NL guidance page); REF-01022, -01024, -01025, -01031 (derived text covers all pages); REF-01028 (Spanish street-spaces order); web pages REF-00989, -00993, -00998 | A reading record. REF-01016's status stays as it is. |
| **A′. Full text held, filed without the source ID** | REF-00990, REF-00991 (Japanese cabinet order and ordinance, full e-Gov JSON) | Register a derived text with the ID, using `retrieval_log.record_file` or `derive`. No fetching. |
| **B. Whole PDF held, no derived text** | REF-00988 (DE, a 4-page excerpt); REF-00992 (UK Approved Document M, 74 pp); REF-00994 (IPC guide, 216 pp); REF-01001 (20 pp); REF-01005 (170 pp report); REF-01010 (UG, 42 pp, out of bucket); REF-01014 (ISO 21542 2007 committee draft, 120 pp, UNVERIFIED); REF-01015 (IE TGD M 2010, 129 pp); REF-01018 (IE TGD M 2022, 180 pp) | Extract text from the held PDF with page markers. `pymupdf` is installed. No fetching. |
| **C. Whole PDF held, derived text partial** | REF-01020 (4 of 39 pp); REF-01023 (3 of 9); REF-01026 (6 of 41; a transcription, supersede first); REF-01027 (4 of 79); REF-01029 (6 of 68); REF-01030 (5 of 65); REF-01032 (5 of 20) | Re-extract all pages from the held PDF. No fetching. |
| **D. Fragment only** | REF-01012 (Norway TEK17, the § 12-16 page only); REF-01013 (Ontario, one clause, and its own text calls itself a plain-language summary); REF-00996 (one handbook page, BE); REF-01008 (9 page images of a report over 300 pages long); REF-00997 (a bot-check page with no content; its 3 extractions carry recorded exemptions) | The rest of the instrument is a new retrieval (phase P4) or stays partial. Readings record "fragment". |
| **E. Abstract or metadata only** | REF-00977, -00979, -00980, -00983, -00984, -00985, -00986, -01003, -01004, -01006, -01007, -01009 (plus a supplementary .docx), -01011; REF-00999 and REF-01000 (unscoped); REF-01002 (given up under the 2026-09-25 ruling) | Read the abstract with scope "abstract". A full text is fetched only where a route exists. REF-01002 is not queued. |
| **Tombstone** | REF-01019 | Never read. Its replacement REF-01031 is read instead. |

**What this changes.** Classes A to C hold full text of the national codes of the US, UK, Ireland (two editions), Japan, Korea, Portugal, Spain, Sweden, Finland, New Zealand and parts of the Netherlands, plus the IPC guide and a 170-page research report. All of it can be scanned with no network use. **[VERIFIED: A1]**

### 2.3 Lead lists we already hold (the "outdated but correct" material)

| List | Where | Size (command) | Caveat |
|---|---|---|---|
| Pre-reset reference stash | `source_locators` table | 893 rows, 313 with a standard number, 880 REFERENCE-ONLY (S1) | The largest list. Some rows have columns shifted against each other: GAP-008 for DOIs; `tier_claimed` and `jurisdiction` hold slug names and URLs on many rows (`select jurisdiction, count(*) from source_locators group by 1 order by 2 desc limit 10`). **[VERIFIED]** Use titles and identifiers, re-verify everything. |
| Standards registry, dated 2026-03-18 | `references/standards-registry.md` | `grep -c '^jurisdiction:' references/standards-registry.md` gives 112, including the template | Version status as of its own date |
| Verified code, Co-1 and Co-2 bodies | `references/tier456-verified-sources.json`, `co1-…`, `co2-…` | `python3 -c "import json;[print(f,len(json.load(open('references/'+f)))) for f in ['tier456-verified-sources.json','co1-verified-sources.json','co2-verified-sources.json']]"` | Lead lists only (2026-08-06 ruling) |
| Code leads | `research_code_leads` | 96 (S1); `select status, count(*) from research_code_leads group by 1` | No parameter column; that is fine (F15) |
| Worklist built this session | `major-sources-worklist.md` (this folder) | Read it | Double counts at least AS 1428.1, CAN/ASC 2.8, DIN 18040-1/-2, EN 17210, ICC A117.1, NEN 9120, PAS 6463 and Approved Document M. Has four blank Co-2 rows. Lists CH (SIA 500) and UG, which are outside buckets 1 and 2. **[VERIFIED: read]** |
| Two finished batch 23 scan outputs (52 items) | harness scratchpad `harvest/es-small.json` (40), `harvest/fr.json` (12) | `python3 -c "import json;[print(f,sum(len(x['items']) for x in json.load(open(f))['files'])) for f in ['es-small.json','fr.json']]"` run in that folder | Read from partial texts. Not data. Proposed use: a test fixture for the one-phrase-two-parameters fix (D13). |

### 2.4 The nine parameters added this session

These are parameters 4 to 12: corridor width (TERM-002), turning circle (TERM-003), operating force (TERM-005), reverberation time (TERM-007), LRV contrast (TERM-011), door width (TERM-021), colour temperature (TERM-024), headroom clearance (TERM-061) and ramp run length (TERM-091). **[VERIFIED: query]**

- **Where they are.** They are real rows on this branch's database only. `main` does not have them.
- **What is missing.** No PR, no session record, no attestation. Direction is unset on all nine. One note is wrong: TERM-091 does have an adjudication.
- **Review points.** "Turning circle" is not the phrase the held ADA text uses (it says "turning space"). The definitions of TERM-003 and TERM-005 carry "Minimum" and "Maximum".

### 2.5 What you said this session, beside what you were asked

Extracted from `transcripts/harness_db856d85/main.jsonl` with §12 command **T1**.

| Time (UTC) | The question or context | Your words, verbatim | Status |
|---|---|---|---|
| 02:35 | Commissioning the first adjudication | "note that while we search by slug, we scan each source for any and all applicable parameters. we may need to just prepopulate a parameters list." | Direction. Recorded in §11. |
| 03:08 | "1. Is the existing `terms` registry acceptable as the seed for the parameter list?" | "1 yes" | Answered |
| 03:08 | "2. Does a `preliminary` or `skim` extraction ever govern a published cell?" | "2 ..yes? like, one pulled from another slug? should be yes, but we still tag it for follow up later" | **Ambiguous. Not settled. See D1.** |
| 03:08 | "3. WP12: confirm the R7 floor removal?" | "3 don't know what is" | Superseded by 05:48 |
| 03:46 | About the session's language | "Here's my problem: you have developed a vocabulary that I don't have, and I do not have immediate knowledge of things like "work package 12 from PR#170" in this format as I am a human, not a computer" | Applied to this paper |
| 05:48 | After a plain-words restatement | "keep wp12 rule" and "populate a parameters table" | Answered |
| 05:52 | Typed mid-turn | "we need like the 90+ cleaned parameters without values" | Prompted the A/B question |
| 06:01 | "What did you mean by 'the 90+ cleaned parameters without values'? A. The 94 existing terms. I would turn each object into its measurable quantity … and propose the new names for your review. B. The 93 old guidebook items with the numbers stripped …" | "A" | Answered. How A meets the naming rule is D3. |
| 06:03 | Queued mid-turn, during the batch 23 scans | "what are these full text sources?" | Answered by the session at 06:04 (it then wrongly said earlier batches had no saved full text) |
| 06:06 | About scanning batch 23 | "... why would you develop a parameter database for coverage of all accessible design terms possible by using batch 23 that came from a specific slug" | Direction |
| 06:07 | Queued at 06:07:12, before the "1. slug by slug / 2. you seed it" options arrived at 06:07:27 | "pull from the major codes, literature and advocacy from major countries" | Direction on sources. **The 1-or-2 choice is unanswered (D3).** |
| 06:07 | Typed mid-turn | "there should be an exhaustive bibliography that is outdated but correct that has info on each jurisdiction code bodies and major groups" | Answered by section 2.3 |
| 06:10 | — | "organize the collected information above then prepare a plan to derive and orchestrate accessibility items into categories for a catalogue" | Version 1 |
| 20:22 | Commissioning the critique and this rewrite | The four requirements quoted in the "How to read this" box | This paper |

The two readings of "2":
- **(a)** A figure only skimmed, or still preliminary, may set a published value, tagged for follow-up.
- **(b)** A figure taken from a source filed under another slug may set a published value, tagged for follow-up.

Two things favour (b). Your own words "like, one pulled from another slug?" read as a guess at what "preliminary" meant. Your later statements ("Slugs guide our searches, but they do not guide what we derive") fit (b). The session then restated the answer as (a) ("I took your answer as yes, as long as it is flagged for follow-up. Please correct me if you meant something else.") and you did not reply to that. **Neither reading is recorded as settled.**

### 2.6 Rulings that bind this work

| Date | Ruling (short) | Effect here |
|---|---|---|
| 2026-08-06 | The old corpus is a lead list, not evidence | Every lead is re-fetched and admitted on its own provenance |
| 2026-08-19 | Item names are leads, not topics; no value crosses; blind-first ordering (`decisions/DR-2026-08-19-…` §1.4) | The old item index is consulted only after the derivation is frozen, names only |
| 2026-08-19 | Adversarial review only of data diffs, never of plans (ledger, line beginning "RULE: Adversarial review is a truth-instrument") | You commissioned the critique of v1 anyway. That supersedes the rule for this plan only (rule 0) and must be recorded (section 11). A further critique of v2 would need your fresh commission. |
| 2026-08-26 | The thing a determination is about is the parameter; `items` is a render roll-up "derived from specifications rather than keyed by them" | An item is a derived view, never a key |
| 2026-08-27 | "the crossing is JUDGMENT's output" (CLAUDE.md §6) | Lens attachments are recorded on extractions at judgment |
| 2026-09-01 | The item layer is deleted: a container whose name states its answer biases every finding | No name may state a value or a target state |
| 2026-09-09 | "parameter at base … use add-term for now"; names are minted from an observed phrase | Still in force. Revisiting it is yours (D3). |
| 2026-09-09 (evening) | "you have to compute it. I can't handle this load manually" | Determinations are computed. Review load on you must stay small. |
| 2026-09-11 | Adjudication may be delegated for a named set (precedent) | Basis for D5 |
| 2026-09-13 | Code value without research backing gets the empty circle | Marker rule for Release 0 |
| 2026-09-16 | "retire in place then" | No row is deleted. Every reader must filter retired rows before the first retirement. |
| **2026-09-18** | **"we are looking not only for values and parameters, but also logics and arguments and qualitative work"; "wherever is relevant to accessibility can be mined from it"; "you search by slug, but you have to adjudicate by all slugs in a category and stuff for each source"** (`sessions/session_2026-09-18-research-batch-15-t2-synthesis-threshold.md` lines 50–53) | **The root of the scan contract.** v1 omitted it. |
| 2026-09-25 | "if we can't access something from anywhere then we have to give up on it for now" | No retrieval task for a source with no route. Reachable re-fetches are allowed. |
| 2026-09-28 | Buckets 1 and 2 only, until "categorically exhausted" per slug "against the slug's parameters" | How to judge exhaustion when the catalogue is per parameter is D4 |
| 2026-10-01 | Remediation plan decisions D1 to D4 approved ("approve all") | The batch 24 branch was approved. The pilot's numbers were the plan's own "discretionary" choices. |

---

## 3. The scan contract

### 3.1 The principle, in your words

> "Slugs guide our searches, but they do not guide what we derive and mine from sources! Our terms/parameter catalogue will, which means I expect harvesting across multiple terms if a source discusses multiple terms."

So:
- **Slugs decide what to look for and where.** That is search planning, search logging, and search coverage by jurisdiction.
- **The parameter catalogue decides what is taken from every admitted source.** That holds whatever slug the source came in under, and the catalogue's aliases help the reader recognize parameters in other languages.

### 3.2 Definitions

- **Source in scope.** An admitted source that is not a tombstone.
- **Catalogue.** The active parameters, with their terms, definitions, aliases and the phrases sources have already been observed using for them.
- **Catalogue version.** The highest parameter number that exists when a reading starts. Numbers are never reused (`base_parameters` is AUTOINCREMENT), so "version N" means exactly "parameters 1 to N, those active at the time". **[VERIFIED: DDL comment]**
- **Scan.** One reading of one source.
  - In **catalogue mode** it covers every active parameter up to the catalogue version.
  - In **targeted mode** it covers one named parameter (used for back-filling, section 5.2).
  - Every scan states its **text scope**: full, partial (pages a to b of N), fragment, or abstract. It also states which saved file it read, by checksum.
- **Closed pass.** Looking for every parameter already in the catalogue.
- **Open pass.** Looking for design quantities and qualities the catalogue lacks.

### 3.3 The closed pass (every source, every parameter)

For each source in scope, in catalogue mode:

1. **Get the whole text.** Use the saved text. Where only a PDF is held, extract all pages with page markers and register the result under the source's ID (section 2.2, classes A′, B and C). No network.
2. **Pre-screen by script (optional; no judgment).** List the passages where any catalogue term, any alias, or any phrase already observed for a parameter occurs, with page and position. This is a reading aid. It never stands in for reading the text.
3. **Read the whole text against the whole list.** For every passage that states anything about a catalogued parameter (a figure, a range, a condition, a qualitative finding, an argument, or an explicit statement that it sets nothing), write:
   - an **observation** of the source's own phrase at that place, judged NAMES-EXISTING to the parameter's term;
   - **one extraction per thing said per parameter**, with the verbatim quote, the structured locator for codes, the figure role, the comparator, at least one lens, and relations such as "applies only when" (`relate-extraction … condition_on`).
4. **Record the reading** with its text scope, the file read, the catalogue version, and "open pass done: yes/no".

Your 2026-09-18 directive applies at step 3. Arguments and qualitative findings are recorded, not just numbers. `claim_type` already allows `qualitative` and `framework`, and `figure_role` allows `finding`. **[VERIFIED: DDL]**

### 3.4 The open pass (new quantities)

In the same reading:

1. Observe, verbatim, every phrase the source treats as a design quantity or quality and that the catalogue does not hold.
2. Judge each one:
   - NAMES-EXISTING, if it is another name for something we hold; this also proposes a source-attested alias;
   - NAMES-NEW through `add-term --from-observation`, if a reviewer would accept it as a new concept;
   - DEFERRED, if it cannot be settled from this source;
   - NOT-OURS.
3. Collect the NAMES-NEW terms into the cohort's **vocabulary review table**. It gives one row per proposed parameter: the source phrase and place, the session's recommendation (promote, decline, or merge into an existing parameter), and the reason.
4. Only after review are terms promoted (`add-parameter`) or declined (`decline-parameter`, with reason). Then the cohort's sources get **targeted** readings for the newly promoted parameters, in the same PR.

A scanner may not mint a parameter by itself. An extraction can only point at a parameter that exists (`parameter_id NOT NULL`, refused unless active). **[VERIFIED: DDL and `insert_extraction`]**

### 3.5 Many quantities in one clause; one phrase naming two quantities

- **One clause states several quantities.** Write one extraction per quantity. They can share the same quote; each row's quote must contain its own figure (the digits check). **[VERIFIED: `_require_verbatim`]** Nothing stops several rows per source and parameter; this is the ruled one-to-many fan-out (D-0168), and a blocking check pins it (`judgment_handoff_shape`). **[VERIFIED: read]**
- **One phrase is used for two quantities.** For example, "clear width" at a door clause and at a route clause. Today the second sighting folds into the first and returns `created: False`, losing its place and quote. The second sense is then never judged.
  - **Repair (tooling T1):** an observation becomes one sighting. The uniqueness key gains the locator, so each sighting is judged separately. One sighting can name a door width and the other a corridor width.
  - A deliberate second judgment of one sighting stays what it is today: a contest, not a second meaning.
- **One quantity under many phrases and languages.** Each phrase is its own observation, judged to the same term. The phrase then becomes a candidate, source-attested alias (section 3.9).

### 3.6 Who decides what

| Act | Decided by | Verified by script | Recorded in |
|---|---|---|---|
| Text scope and pages read | Script (page markers against PDF page count) | Yes | Reading record |
| The phrase is in the source, at that place | Scanner quotes it | **Yes**: the quote is in the source's own saved file (scoped) and the phrase is inside the quote (new in T1 for observations; exists for extractions) | `observed_terms`, `source_value_extractions.claim_text` |
| The figure is in the quote | Scanner | **Yes**, digits including CJK numerals (exists) | Extraction |
| Which parameter a passage concerns | **Scanner (judgment)**, with a rationale | No; sampled by the independent review once per source | Adjudication rationale, extraction |
| Figure role, comparator, claim type, relations | Scanner | Vocabulary only, from the column CHECKs (exists) | Extraction |
| Which group a finding concerns (lens) | Scanner, from the source's own scope | Code must exist in its registry (exists) | Extraction lens columns |
| A phrase names a new concept | Scanner proposes | Name refused if it carries a digit, a comparator or a min/max word (exists) | `terms` plus NAMES-NEW |
| Promote, decline, merge, split, rename, retire | **You, or a reviewer you name (D5)** | The refusals of each verb | `base_parameters`, `parameter_declinations`, notes |
| Direction (which way is better) | Session, only when an admitted source states it; reviewed | Write-once (exists) | `base_parameters` |
| Category vocabulary and order | **You, once (D7)** | Name guard | Category registry (T2) |
| Placing a parameter in a category | Session, with warrant | Category must be in the registry | Assignment table (T2) |
| Tier | Derived from evidence type and scope | Yes (exists) | Source |
| Determination | **Engine only** (2026-09-09 ruling) | K01, K02, C10 | `specifications` |

**A scanner may not:**
- promote, decline, retire, merge or rename a parameter;
- set a direction without a source's statement;
- add a jurisdiction, category or lens code;
- write a determination;
- add a slug link just to relabel an extraction.

### 3.7 What `slug` means on an extraction, and the "other slug" follow-up

- **Meaning.** `source_value_extractions.slug` records **which filing the source came in under**. v2 fixes the convention: use the slug of the search that admitted the source, reached through `search_admissions`. It says nothing about which topic the parameter belongs to. The table's own DDL comment already says this ("says the reading happened there"). **[VERIFIED: DDL]** `add-extraction` requires the source to be linked to that slug, and it deliberately does not check the parameter against the slug (`test_db_integrity.py`, J01 retirement note). **[VERIFIED: read]** So the closed pass needs no "slug fiction".
- **Rule for every reader:** no catalogue surface groups or filters by `extraction.slug`. The only slug-keyed views are search-plan views (`v_coverage_jurisdiction` and the others).
- **The follow-up marker.** Your answer "2" asks for a tag "for follow up later". What a tag means depends on D1:
  - Under reading **(a)**, the tag already exists. `extraction_method='skim'` and `extraction_status='preliminary'` are typed columns. What is missing is any reader: `assess_cell.py` contains no reference to either column. **[VERIFIED: `grep -c "extraction_status\|extraction_method" scripts/assess/assess_cell.py` gives 0]** A second home for the same fact would break rule 5. So v2 adds no new column for (a). It adds a reader: the engine report and the catalogue mark any value-setting figure that is skimmed or preliminary, and an advisory check lists live determinations resting on one.
  - Under reading **(b)**, nothing records that a figure was read outside the purpose its source was admitted for. Nothing can derive it either, because no slug-to-parameter map exists, and building one would be curation. v2 proposes a small typed table, `extraction_follow_ups`:
    - one row per open follow-up on an extraction;
    - a reason from a CHECK list (starting with `read-outside-admitting-purpose`);
    - a required warrant sentence;
    - who raised it, and who resolved it, when and how.

    It is written by the scanner's judgment and read by the catalogue and by the same advisory check.
  - **Caution under (b).** Once every source is read for every parameter, most figures in a whole-code reading are "from another slug". Tagging all of them makes the tag noise. v2 therefore proposes that under (b) the scanner tags only figures a reviewer should re-check against the parameter's own literature, and states why on each row.
  - Neither table nor reader is built until you answer D1.

### 3.8 Evidence that a scan is complete

- **Reading record (new table, tooling T1): `source_scans`.**
  - **Fields:** source, mode (catalogue or targeted), catalogue version or target parameter, text scope with pages read and pages total, the checksum of the file read, open pass done, method (full read or pre-screen only), session.
  - **Writer:** `db.py record-scan`.
  - **It refuses:**
    - a tombstone;
    - a file not saved for that source;
    - "full" when the derived text's pages are fewer than the PDF's;
    - a typed-in catalogue version. The command computes it, never the person (rule 8).
- **Ledger (derived view): `v_scan_ledger`.** One row per source in scope and active parameter, with a status:
  - EXTRACTED: at least one non-absent extraction;
  - STATED-ABSENT: an extraction of type `absent`, meaning the source addresses the quantity and sets nothing;
  - READ-NOTHING-FOUND: a full catalogue-mode or targeted reading covers it and found no row;
  - READ-PARTIAL: only partial, fragment or abstract readings cover it;
  - NOT-READ.

  Explicit "absent" rows stay for positive statements of absence. Silence is derived, so nobody writes an "absent" row for every source-parameter pair.
- **What reads it:**
  - the catalogue's evidence-state line;
  - the parameter-by-jurisdiction coverage view (section 7.4);
  - the advisory **scan-debt** check (section 8.2);
  - the new batch rule **R16-scan**: every admission in the batch has a catalogue-mode reading;
  - the worklist for back-filling (section 5.2).
- **Why it earns its place (section 8 test).** Without it, the catalogue can say or imply "no code sets a requirement" where nobody read the code for that quantity. A parameter added in month three would then never be looked for in month one's sources while every gate reads green. That is how GAP-061's lost figures happened.
- **What it does not prove.** It does not prove the scanner saw everything. The independent review's standing subject 4 samples each source once for figures no row carries (`skills/adversarial-research_SKILL.md`, standing subject 4). **[VERIFIED: read]**

### 3.9 Aliases: an aid to the eye, never evidence

- **What aliases do.** Pre-screening and reading use aliases in 15 languages. A hit means "look here"; it means nothing more. 1,163 aliases are model-generated (section 1.2).
- **Growth path (tooling T1).** A phrase observed in an admitted source and judged NAMES-EXISTING becomes a **source-attested alias** through a new `add-alias` command.
- **What `add-alias` does:**
  - requires a provenance marker, as `alias_provenance_audit` already blocks unmarked new aliases (**[VERIFIED: read]**);
  - points at the observation;
  - normalizes language case.

### 3.10 What exists today, and what needs new tooling

| Part of the contract | Exists today? |
|---|---|
| Extraction for any active parameter from any admitted source, whatever slug | **Yes** |
| Verbatim and digits check on extractions; structured locator for codes; at least one lens | **Yes** |
| Observe, judge, mint from observation, promote, decline | **Yes** |
| Many rows per source and parameter | **Yes** (and pinned) |
| Extract full text from a held PDF and register it under the source ID | **Partly.** Done by hand in batch 23 through `record_file`. T1 adds a small helper so every reading does it the same way and page coverage is computed. |
| Observation per sighting (phrase plus place) | **No**, T1 |
| Verbatim check on observations | **No**, T1 |
| Reading record, ledger view, scan-debt check, R16-scan rule | **No**, T1 |
| Pre-screen helper | **No**, T1 (optional) |
| Alias writer | **No**, T1 |
| Follow-up marker | **No**, after D1 |
| Category registry and placement | **No**, T2 |

---

## 4. Catalogue growth protocol

### 4.1 Every way the list changes

"Cost at 1" and "cost at 100" mean the work to do it once versus for a hundred terms.

| Change | Sanctioned path today | Refusals today | Irreversible | Cost at 1 / at 100 | Needed before bulk promotion |
|---|---|---|---|---|---|
| **Add** a parameter from new reading | `observe-term`, then `add-term --from-observation`, then `add-parameter` | Name with a digit, comparator or min/max word; duplicate name; declined term; tombstoned source | The name (no rename); the number (never reused); no retire | 3 commands plus review / 300 commands, a 100-row review table, R16 disposal | Rename, retire, merge (below) |
| **Add** from an existing term with no observation (as the nine were) | `add-parameter` alone | Same | Same | 1 / 100 commands | Same; plus your D3 answer |
| **Add after sources were read** (back-fill) | None. Debt is invisible. | — | — | Today: unknown work. With T1: pre-screen of every held text by script (seconds), then a targeted reading of each hit / the same, scaling with hits | Reading record and ledger (T1) |
| **Split** (one parameter is really two) | Mint two new terms from observations; the old one cannot be retired; extractions cannot be repointed (`amend-extraction` cannot change `parameter_id`) | — | Old rows stay on the old number | Hours / not feasible | Retire; re-point rule (in merge) |
| **Merge** (two parameters are one) | None. `status='merged'` and `merged_into` exist with no writer. | — | — | — | `merge-parameter`: sets merged, re-points extractions with a recorded note, refuses while either has a live determination |
| **Rename** (wrong or answer-shaped name) | None. `canonical_en` is not amendable. | — | Name | — | `rename-term`: the new name must come from an observation (or your ruling, D3); keeps the old name as a DEPRECATED alias; same value guard |
| **Retire** (not a design quantity after all) | None. `status='retired'` has no writer. | — | — | — | `retire-parameter`, with reason; refuses while a live determination exists; first, every reader is swept to filter retired rows (2026-09-16 condition) |
| **Un-decline** | None, by design ("nothing reads an un-decline yet") | `add-parameter` refuses a declined term | Declination | — | `revoke-declination` with reason and decision reference. Its reader is the vocabulary review. |
| **Wrong or disputed direction** | `set-parameter-direction` once; `contested` is an allowed answer | A second statement | Direction | — | `revise-direction`, only with no live determination for the parameter and with a decision reference. **Deferrable:** directions are set late (section 7.6), so this can wait for the first dispute. |
| **Correct a parameter's note** (F18) | None | — | Note | — | `annotate-parameter`: append a dated line, never overwrite |
| **New language alias** | **None at all** | — | — | — | `add-alias` (section 3.9) |
| **New jurisdiction** | Edit `schemas/enums.py` in a tooling PR, plus your scope ruling | `jurisdiction_db_vocabulary` (blocking) | — | One tooling PR | None now: all of buckets 1 and 2 are in the list. **[VERIFIED: enum check, §12 V3]** |
| **New source family** (for example a new kind of Co-1 body) | Schema or enum change in tooling | Column CHECKs; GAP-063 records the Co-1 type mismatch | — | One tooling PR | None now |
| **Superseded source** (new edition, better copy) | `supersede-source` exists; the engine drops tombstones | Writers refuse new work on a tombstone | — | 1 command, then re-read the replacement and re-run any determination it fed | Ledger handles tombstones (T1) |
| **Category change** | — | — | — | — | T2: registry rows by migration on your approval; placements by command with warrant |

### 4.2 Minimum tooling before bulk promotion (tooling PR T1)

1. Reading record, ledger view, scan-debt check, R16-scan rule (this needs the research contract text updated and the session-start copy regenerated, because `research_contract_sync` is blocking), and the full-text helper.
2. Observation per sighting, and the verbatim check on observations.
3. `retire-parameter`, `merge-parameter` (with the re-point rule), `rename-term`, `revoke-declination`, `annotate-parameter`, `add-alias`.
4. Before the first retirement, a sweep so that every view and reader of `base_parameters` filters on status (rule 4: views are callers).
5. The batch rule "every admission has an admission edge", seeded at the corpus baseline of 2 so it is not red on `main`.

Each item must:
- go red on today's code in a fault-injected test before it is fixed;
- be captured by `emit_batch_sql`. The capture set is derived by `dbcore.writable_tables`, so add a test that each new table is in it.

**Deliberately left out**, each with its section 8 reason:
- A slug-to-parameter map: curated, and not needed once exhaustion is by parameter.
- `observation_id` on extractions: the DDL comment says add it with its reader, and nothing here reads it.
- Amending `terms.domain`: stop reading it instead.
- An element table: not needed if D6 is "item = parameter".
- A room-by-parameter relation: later, with its own reader.
- A lead-to-parameter link: F15.
- `revise-direction`: until the first dispute.
- Dropping the item-keyed tables: committed migrations insert into two of them.

---

## 5. The pipeline as a graph

### 5.1 Stages

"New" marks a stage this plan proposes. Gate levels: **B** = blocking, **A** = advisory.

| Stage (command) | Reads | Writes | Refuses (selected) | Gates: name, level, what it examines, can it pass having examined nothing? | Conditions and notes |
|---|---|---|---|---|---|
| Plan a search | slugs, coverage views | nothing | — | none | Buckets 1 and 2 only (2026-09-28) |
| Search (`log-search`) | slugs, sources (an admitted ID must already exist) | `search_executions`, `search_admissions`, result-file links | No prior expectation; jurisdiction outside the list; mining without a named source; **a list-driven search with a target tier**; admitted count not equal to IDs | R8, R14 (B, via batch gate); `search_log_completeness` (A, `CURRENT`; sees web tool calls only); R7 reports "EXAMINED: 0 searches" when none | `--origin lead-index` for list-driven acquisition (never used yet) |
| Screen (`add-candidate`, `resolve-candidate`) | search row, saved files | `search_candidates` | `surfaced_in` text not in the saved bytes | `provenance_artefact_audit` (B; candidates with `surfaced_in`); S01 (B) | Optional for list-driven acquisition |
| Retrieve (`retrieval_log.fetch`), derive text | the web; held bytes | `retrieval-log/<session>/` files and manifest | A derived text whose root fetch failed | `author_fidelity` (A, `LATEST-RESEARCH`, Crossref only) | No route: mark EXHAUSTED (2026-09-25). Held PDF: extract locally (new helper). |
| Admit (`add-source`, `link-source-slug`, `supersede-source`) | `source_locators` stash, sources | sources, authors, slug links | Duplicate DOI or ID; merged slug; tombstone reuse | R9, R9a, R9b, R10 (B, batch gate; R9a and R9b fail an empty batch); C03, C04 (B); `jurisdiction_db_vocabulary` (B); `identifier_floor_audit` (B) | `add-source` still asks for `--tier`, which is derivable (rule 8 debt). New batch rule: admission edge. |
| Grade population (`add-population-match`) | sources | `evidence_population_match` | — | R13 (B; tiers 1 to 3; checks presence only) | Not owed by codes |
| Mine citations (`log-mining`) | slug links | `citation_mining` | Source not linked to slug | R2 (B; tiers 1 to 3); `citation_mining_session` (A, `LATEST-RESEARCH`, tier ≤ 2) | Keyed per slug (GAP-011, open) |
| **Record a reading (`record-scan`)**, new | saved files, highest parameter number | `source_scans` | Tombstone; file not saved for the source; "full" when pages are missing | **R16-scan** (B, batch), **scan-debt** (A, corpus). R16-scan examines nothing when a batch admits nothing, but R9a and R9b fail that batch. | Catalogue or targeted mode |
| Observe (`observe-term`) | sources | `observed_terms` | Unknown source; tombstone; a term ID offered. **New:** quote not in the source's bytes; phrase not in its quote. | R11-harvest (B, batch; at least one per admission; examines nothing with no admissions); new observation backstop (A) | Per sighting after T1 |
| Judge (`adjudicate-term`, `add-term`) | observations, terms | `term_adjudications`, `terms` | Name with a digit, comparator or min/max word; duplicate name; no rationale | R16-adjudicate (B, batch) | Not a subject of the adversarial rule's list of research tables. Who reviews is D5. |
| Promote or decline (`add-parameter`, `decline-parameter`) | terms, declinations | `base_parameters`, `parameter_declinations` | Declined term; duplicate; value-bearing name | R16 (B, batch); `validate_parameters` (A; names of active parameters) | Only after the cohort's vocabulary review |
| **Lifecycle (retire, merge, rename, revoke, annotate, alias)**, new | parameters, extractions, aliases | updates to those tables | See section 4.1 | `migration_reproducibility` (B) **cannot see updates** (it compares row counts); `migration_reproducibility_deep` (A) can; `alias_provenance_audit` (B) | Readers must filter retired and merged rows |
| Direction (`set-parameter-direction`) | parameter | update on `base_parameters` | A second statement; no rationale | none, so you are the gate; the update is invisible to the blocking reproducibility check | Set only at the determination phase, from a source's statement |
| Extract (`add-extraction`, `derive-extraction`) | slug links, parameters, saved files, lens registries | `source_value_extractions`, `extraction_relations`; sets `data_capture_status` | Source not linked to the slug; inactive parameter; quote not in bytes (or recorded exemption); digits not in quote; code without structured locator; no lens; value outside a CHECK | C06, `extraction_relations_integrity`, `judgment_handoff_shape` (all B); K02 (B; examines nothing until a live determination); the independent review is required (this table is in the rule's list) | The follow-up marker comes after D1 |
| Relate (`relate-extraction`) | extractions | `extraction_relations` | Self-edge; a condition with no row | `extraction_relations_integrity` (B) | — |
| **Place in a category**, new (T2) | parameters, category registry | assignment table | Inactive parameter; category not in registry; no warrant | **catalogue-reach** (B once it has a subject) | Many categories per parameter allowed |
| Determine (`assess_cell` on a scratch copy; `retire-specification`) | extractions by parameter from any slug; sources; gates | `specifications`, link tables | The canonical database; inactive parameter; missing `--slug` (a label only) | K01, K02, C10, `validate_evidence_state` (B). K01, K02 and C10 examine nothing today. | Determine late; re-run on every new extraction for a determined parameter |
| Synthesis | determinations | convergence, reasoning documents | Opus floor | attestation gates (B) | Out of scope here |
| Render (catalogue generator, new; `build_site.py` today) | views | `site/`, `parts/`, `tools/` | — | `site_pages_fresh` (A; **examines 0, by construction**); `pipeline_completeness_fresh`, `evidentiary_audit_fresh` (B; regenerate after every data change); `render_audit_browser` (A) | `build_site.py` walks `items`, which is empty |
| Close a batch (`/batch-done`) | everything above | session record, transcripts | — | batch gate on `CURRENT`; `adversarial_pass_audit`; `search_log_completeness`; `--all`; `research_contract_baseline_ratchet` (B) | PR opened last and not watched (rule 9) |

### 5.2 Backward and re-entrant edges

1. **New parameter, old sources.** A parameter numbered P, promoted in cohort N, leaves every earlier catalogue-mode reading with version below P as NOT-READ for P in the ledger. The pre-screen script lists candidate passages across all held texts. The next cohort does targeted readings for those hits. Sources with no hit get a targeted reading in "pre-screen only" mode, which the ledger shows as weaker than a full read. The scan-debt check counts what remains.
2. **New source, whole catalogue.** Every admission gets a catalogue-mode reading in its own session. R16-scan enforces this.
3. **New alias.** Re-run the pre-screen. A new hit in a source already read becomes a targeted reading.
4. **Superseded source.**
   - `supersede-source` first.
   - The tombstone leaves the ledger, and its readings stay as history.
   - The replacement gets a catalogue-mode reading.
   - Any live determination its figures fed is re-run (K01, K02).
5. **Merge.**
   - Extractions are re-pointed by the merge command, with a note.
   - Any live determination on either parameter is retired first, then re-run.
   - K02 enforces this.
6. **Split.** Mint the new parameters from observations, retire the old one, then re-read the clauses behind the old parameter's extractions in targeted mode for each new parameter. Old rows stay, as history on a retired parameter.
7. **Rename.** No pointer moves. The old name becomes a DEPRECATED alias. Render regenerates.
8. **Retire.** Readers filter it. Its extractions stay. Any live determination is retired first.
9. **Search under slug S admits a document.** It is read for all parameters, and its figures for parameters other slugs plan for are filed under S's admission. This is the owner's rule working, not a fault.
10. **Independent review finding.** It is corrected in the same pass, by migration, and may trigger a targeted re-read.
11. **Reasoning documents produce leads.** This is normal re-entry (CLAUDE.md §3). Leads go to the lead lists, never straight into the catalogue.
12. **Your ruling.** It is recorded on contact (rule 0). It may change gates, and any supersession is named (section 11).

### 5.3 Gates this plan relies on, and gates v1 forgot

- **Relied on:**
  - the batch gate (`research_dod_session`) and its corpus ratchet;
  - `test_db_integrity` (C06, K01, K02, C10);
  - `extraction_relations_integrity`, `judgment_handoff_shape`;
  - `alias_provenance_audit`, `jurisdiction_db_vocabulary`, `identifier_floor_audit`;
  - `schema_reference_audit`, `derived_not_curated_audit`, `column_vocabulary_audit`;
  - `research_contract_sync`, `research_dod_selftest`;
  - the two blocking render-freshness checks;
  - the attestation gates;
  - `adversarial_pass_audit` (through `/batch-done`).
- **Forgotten by v1 and now named:**
  - `research_contract_sync`, which a new R-rule triggers;
  - `migration_reproducibility`, which cannot see updates;
  - `identifier_floor_audit`, which argues against reverting the nine;
  - `jurisdiction_db_vocabulary`, because the worklist carries CH and UG;
  - `derived_not_curated_audit`, because the category list must not be an argparse list;
  - `column_vocabulary_audit`, because new tables must use the standard session-column names;
  - `pipeline_completeness_fresh` and `evidentiary_audit_fresh`, because every data PR must regenerate derived outputs.
- **Still vacuous and stated as such:** K01, K02, C10 and `site_pages_fresh`.

---

## 6. Items and categories (your original request)

### 6.1 What an item is

- **Recommendation (D6).** For Release 0, **one item per active parameter**. The item is a derived view that rolls up, for that parameter:
  - its determinations (none yet);
  - its extractions by source, stratum and jurisdiction;
  - its open follow-ups;
  - its reading coverage from the ledger.
- **Why.** This matches your 2026-08-26 ruling that items are "derived from specifications rather than keyed by them". No item table is created and no item key exists.
- **The alternative** is one item per element (door, ramp, toilet). It needs a many-to-many parameter-to-element relation with a warrant on each link. Of the ten parameters, only door width and the two ramp quantities plausibly belong to one element each (F6). That relation is apparatus with no reader until element pages exist, so it is deferred unless you choose it.

### 6.2 Categories

- **Source of the vocabulary.** A new base registry (T2) of category names, descriptions and a reading order, approved by you once (D7). It is not computed from `terms.domain`, which is unchecked free text with misfilings (F6), and not from `axes` (retired vocabulary).
- **How the draft list is made.** After the first reading cohorts, from the chapter structure of the held national codes and the access-need families. The proposal cites, for each category, the code chapters that ground it. You then approve, rename or strike names.
- **Placement.** A parameter may sit in several categories. Operating force, for example, may sit with doors and with controls. Each placement carries a warrant: the source clause or the reason. Placement is recorded by a command that refuses a category not in the registry.
- **Order.** A journey order (approach, entry, moving through, level changes, rooms and fixtures, controls, wayfinding and information, environmental conditions) is offered for your approval with the list. It is not assumed.

### 6.3 Names

- Item names are parameter names, already refused at write time if they carry a digit, comparator or min/max word. `validate_parameters` backstops this.
- Category names pass the same guard, imported from `db.py` (one home).
- The guard cannot see an answer-shaped name with no digit, such as "level threshold". That is a reviewer's check, written into the vocabulary review table as a standing question: **does this name state a quantity, or a target state?**

### 6.4 The check that nothing is left out

`catalogue_reach` (T2, blocking once it has a subject) fails when an active parameter reaches no category. There is no "unassigned" bucket that passes green.

**First-run note.** Until registry rows exist, every active parameter fails. That is red, not vacuous, so the check is registered when the registry and the first placements land together.

### 6.5 Dead item-keyed tables and the vacuous render check

- `items` is empty. Several tables cannot accept rows, because their item-code key points into it. Derive them with the CLAUDE.md §4 command (§12 V4). They are left alone.
- Two of them received rows from committed migrations, so they cannot be dropped (rule 5).
- Nothing new reads or writes them.
- `site_pages_fresh` walks `items` and examines 0. T2 repoints it at the parameter-keyed catalogue pages, or deletes it if no render ships.

### 6.6 What Release 0 can honestly show

Per parameter:
1. **The question.** The parameter's name and definition. TERM-003 and TERM-005 have their direction words removed with `amend-term` first.
2. **Reading coverage.** "Read in full in X of Y held sources; partial in Z; not yet read in W", computed from the ledger.
3. **What held codes say.** Quoted, with clause, jurisdiction and edition. Marked ◐ for T4 and T5, and ○ for T6 without research backing (2026-09-13). For a jurisdiction whose governing instrument is not held: "instrument not held (paywalled lead)".
4. **Research, lived-experience and professional findings.** Quoted, with tier marker, including qualitative findings and arguments (2026-09-18). Co-1 findings are shown as co-primary.
5. **Who each finding concerns.** From the extraction lens columns, labelled "as scoped by the source".
6. **Open follow-ups**, and skim or preliminary flags.
7. **"No determination yet"** until the engine computes one. No value is published as the guidebook's position.

- **[OPEN] Element-level arguments.** "Ramps … often generate problems of their own" (REF-01000) has no home except under a parameter. Release 0 shows it under the parameters it bears on, with that caveat. Whether element-level arguments need their own home is a later decision, after D6.
- **Coverage check against the old item index.** This happens only after the category list and placements are frozen. It compares names only, never values, and lists topics the derivation missed (DR-2026-08-19 §1.4, blind-first). Each missed topic becomes a search lead, not a container.

---

## 7. Sequence

### 7.1 Phases at a glance

| Phase | What | PR type | Depends on | Can run alongside |
|---|---|---|---|---|
| **P0** | Your decisions (section 10), D1, D2, D3 and D8 first | none | — | — |
| **P1** | Carry the nine (as reviewed) to `main`: session record, attestation, ledger entry with your words, TERM-091 note correction (after T1) | research (vocabulary) | D2, D12; T1 only if any is retired or annotated | T1 build |
| **P2 = T1** | Scan contract and vocabulary lifecycle tooling (section 4.2) | **tooling, merged first** | D8 | P1, T2 design |
| **P3** | Read what is held: cohorts of already-admitted sources, with no network use except the one paired admission per session (section 7.3) | research | T1 merged; D5; D11 | P4 cohorts, T2 |
| **P4** | Acquire from lead lists: bucket 1, then bucket 2; every admission read in its own session | research | T1 merged; D4 | P3 cohorts, T2 |
| **P5 = T2** | Catalogue tooling: category registry and placement command, catalogue views, generator, `catalogue_reach`, render check repointed | **tooling** | D6, D7 | P3, P4 |
| **P6** | Category registry rows (your approved list) and placements with warrants | research | T2 merged; D7 | later P3/P4 cohorts |
| **P7** | Release 0 render | render | P6; Release 0 acceptance tests (section 12) | — |
| **P8** | Determinations, parameter by parameter, once reading debt is zero; the first published determination (DR-2026-08-19 §4) | research | D1; per-parameter debt = 0 | continuing |

### 7.2 Phase by phase

**P1 (the nine).**
- **Reads:** this branch's database and transcript.
- **Writes:**
  - `sessions/session_2026-10-09-research-batch-24-parameter-pilot.md`, with its attestation (rule 2);
  - the ledger entry (section 11);
  - if T1 has merged, an `annotate-parameter` line on parameter 12 and `amend-term` definition fixes for TERM-003 and TERM-005.
- **Gating:**
  - `LATEST-RESEARCH` is **not** moved, because this is not an acquisition batch and moving it would point the blocking gate at a batch with no admissions. Run the batch gate against batch 23's name and `--all` with the ratchet.
  - `validate_parameters` examines the ten names.
- **Exit:** your review is recorded; `main` has the rows.
- **On failure:** none of the nine is deleted. A rejected one waits for `retire-parameter`.

**P2 = T1 (tooling).**
- **Session name:** `session_YYYY-MM-DD-tooling-scan-contract`.
- **Writes:** a numbered schema migration; `db.py` commands; the registry entries; the research contract text with its session-start copy regenerated; Pydantic models mirrored; selftests.
- **Gates:** `run_checks.py --selftest`; `schema_reference_audit`; `research_contract_sync`; `research_dod_selftest`; `derived_not_curated_audit`; `column_vocabulary_audit`; `judgment_handoff_shape`; `test_db_integrity`; `migration_reproducibility` with a rebuild.
- **Exit:** every new refusal and check has a fault-injection test that is red on today's code.
- **On failure:** cut scope. Items 1 and 2 of section 4.2 are the floor. Never patch inside a research PR (rule 10).

**P3 (read what is held).**
- **Session name:** `session_YYYY-MM-DD-research-batch-NN-rescan-<cohort>`.
- **Cohort order:**
  - **C1:** the full national instruments of buckets 1 and 2 (US ADA, UK AD M, IE TGD M 2010 and 2022, JP order and ordinance, KR, PT; REF-01026 superseded first; ES CTE and order, SE, FI, NZ, NL). Split into two cohorts if over the size rule.
  - **C2:** IPC guide, FR guide, ISO draft, the 170-page report, DE excerpt, Co-1 and advocacy texts held, out-of-bucket sources if D11 is yes.
  - **C3:** abstract-only literature.
  - The first cohort also clears the R16 debt (8 terms, 11 observations), because those observations sit on sources it re-reads.
- **Per source:** derive full text; record the reading; closed pass; open pass; judge; vocabulary review table; promotions and declines; targeted readings for new parameters; follow-ups (after D1).
- **Per cohort:**
  - one independent review sampling each source once;
  - `/batch-done`;
  - the batch gate run on each admitting batch's name for the sources re-read;
  - `--all` with the ratchet;
  - regenerate derived outputs;
  - one PR.
- **Plus:** at least one list-driven admission in the same session (section 7.3).
- **Exit:** scan debt for the cohort's sources is zero at the cohort's catalogue version.
- **On failure:** stop and file a GAP. Leave rows unwritten rather than hand-write SQL.

**P4 (acquire).**
- **Session name:** `session_YYYY-MM-DD-research-batch-NN-<jurisdiction-or-family>`.
- **Per lead:**
  - `log-search --origin lead-index --jurisdiction J --prior-expectation …`, filed under the slug whose plan it serves. `jurisdiction-matrix-accessibility-standards` is an existing active slug for whole national instruments. **[VERIFIED: query]**
  - `retrieval_log.fetch` with the source ID;
  - admit;
  - C04 no-DOI explanation for codes;
  - R13 and R2 for T1 to T3;
  - at least one Co-1 source in the cohort (R1);
  - catalogue-mode reading in the same session.
- **Unreachable:** EXHAUSTED, never queued. **Paywalled:** the lead stays REFERENCE-ONLY.
- **Exit:** each bucket jurisdiction's governing instruments are admitted and read, or recorded as not held.

**P5 = T2, P6, P7, P8** are as in the table above. T2's gates are those of T1 plus the render checks. P7 regenerates derived outputs. P8 follows section 7.6.

### 7.3 How sessions are formed so their gates examine something

| Kind of session | `CURRENT` | `LATEST-RESEARCH` at close | Batch gate run on | Why it is not vacuous |
|---|---|---|---|---|
| Acquisition (P4) | its own name | moves to it | its own name (blocking in CI) | It has admissions and searches, so R1, R9a, R9b, R11-harvest, R16 and R16-scan all have subjects |
| Re-read (P3), with at least one list-driven admission | its own name | moves to it | its own name **and** each admitting batch's name (run locally, results in the session record) | Its own admission gives the session's gate a subject. The re-read sources' rules run against the batches that admitted them, and the corpus ratchet blocks any rise in debt. |
| Re-read with no admission (only if you prefer it) | its own name | does not move | admitting batches' names only | The remediation plan's assumption. `/batch-done` on `CURRENT` would fail R1, R9a and R9b, so the session record must say why. |
| Vocabulary only (P1, P6) | its own name | does not move | batch 23's name, plus `--all` | `validate_parameters` examines the names. The ratchet shows R16 debt did not rise. **No gate examines the nine themselves**, because no adjudication names eight of them: your recorded review is the check, and the session record says so. |
| Tooling (T1, T2) | its own name | does not move | not applicable | Selftests and fault injection |

### 7.4 Scope and exhaustion when coverage is by slug but the catalogue is by parameter

- **The tension.** Your 2026-09-28 ruling measures exhaustion "for every bucket-1 and bucket-2 jurisdiction against the slug's parameters", and the corrected mechanism reads `v_coverage_jurisdiction`, grouped by slug. No slug-to-parameter map exists. Under the scan contract a slug's searches feed every parameter.
- **Proposal (D4).** Judge exhaustion per **parameter and jurisdiction**, with a derived view (built in T2). A pair counts as covered when either:
  - (i) at least one admitted source from that jurisdiction has been read in full for that parameter; or
  - (ii) a logged search for that jurisdiction was deferred or came back empty with a reason, or the governing instrument is recorded as not held.

  Slug-level coverage stays as the search-plan record.
- **Out-of-bucket sources already admitted** (BE, UG, IN, BR, HR) are read if D11 is yes. Their rows never count toward bucket coverage.

### 7.5 Reuse before fetching

- P3 precedes P4 within each jurisdiction. Nothing is fetched that is already held whole.
- Batch 23's partial texts are re-extracted from their held PDFs, not re-fetched.
- REF-01002 stays given up (2026-09-25).

### 7.6 The determination trap (K02) and when to determine

- **Determine late.** No determination on a parameter until its reading debt over held bucket 1 and 2 sources is zero, D1 is answered, and its direction is stated by a source.
- **After the first live determination on P,** any PR that adds an extraction for P also:
  - retires the old determination;
  - re-runs `assess_cell` on the scratch copy;
  - captures the new one in the same PR.

  Otherwise K02 is red.

### 7.7 Review unit, volume, and who reviews the vocabulary

- **Review unit.** One source, with a per-source sheet: the catalogue checklist with each parameter's status, the rows written, new-term proposals and follow-ups.
- **Volume.**
  - No cap on figures.
  - A cohort holds at most as many sources as one independent review has sampled in full before. Batch 23's review sampled 14: `select count(*) from evidence_sources where created_by_session='session_2026-10-01-research-batch-23'`.
  - **[INFERRED, discretionary]** An instrument over about 100 pages counts as two.
- **Comparator.** Sustained findings per source sampled. Batch 23 had 13 over 14 sources: `select verdict, count(*) from adversarial_findings where pass_id=4 group by 1`. If a cohort's rate rises, the next cohort halves.
- **Vocabulary review.** The adversarial rule's list of research tables does not include the vocabulary tables (`adversarial_pass_audit.py` reports "NOTHING-IN-SCOPE" for this session). **[VERIFIED: ran it]** Whether vocabulary writes need independent review was withheld for you by the critic. **Recommendation (D5):**
  - a reviewer you name (an independent model, as on 2026-09-11) adjudicates each cohort's vocabulary review table;
  - you get the one-page table with a short window to veto;
  - the batch's independent review names vocabulary writes as a standing subject.

---

## 8. Gates and checks

### 8.1 Existing gates this plan touches

"EXAMINED today" values come from runs on 2026-10-09 and must be re-derived.

| Gate | Level | Examines | Today | Row that fails it today |
|---|---|---|---|---|
| `research_dod_session` | B | admissions of the batch named by `LATEST-RESEARCH` (batch 23) | COMPLIANT | On this session's name: R1, R9a and R9b fail (no admissions, no searches) |
| `research_contract_baseline_ratchet` | B | corpus rule counts against `origin/main` | passes | — (R16 is 8 against a baseline of 9: can ratchet down) |
| `research_dod` (`--all`) | A | whole corpus | COMPLIANT with inherited debt | R16-adjudicate 11 and R16 8 (§12 S1 lists them); also R3 8, R7 1, R11 856, all at baseline |
| `test_db_integrity` | B | 71 checks | all pass | 19 pass having examined nothing, including C10, K01 and K02 |
| `validate_parameters` | A | names of active parameters (10) | passes | — (its registry note is stale) |
| `adversarial_pass_recorded` | A | this session's rows in the rule's research tables | NOTHING-IN-SCOPE | — (vocabulary is not in the list) |
| `site_pages_fresh` | A | pages built from `items` | EXAMINED 0 | Vacuous by construction |
| `migration_reproducibility` | B | user_version plus counts on six tables | — | Blind to the lifecycle updates; use `--deep` (A) in T1's tests |
| `identifier_floor_audit` | B | identifiers in committed migrations against live tables | — | Would object to any revert of the nine |
| `jurisdiction_db_vocabulary` | B | jurisdiction values in tables | — | — (all bucket codes present) |
| `alias_provenance_audit` | B | aliases | EXAMINED 2,382 | — (new aliases need a marker) |
| `provenance_artefact_audit` | B | candidates with `surfaced_in` (34) | — | — |
| `search_log_completeness` | A | web tool lines on `CURRENT` | — | Does not see MCP searches |
| `citation_mining_session` | A | mining for tiers ≤ 2, `LATEST-RESEARCH` | — | Keyed per slug (GAP-011) |
| `extraction_relations_integrity`, `judgment_handoff_shape` | B | relations; the hand-off key | pass | — |
| `research_contract_sync`, `research_dod_selftest` | B | contract against hook; gate selftest | pass | Turn red if R16-scan is added without regeneration or a selftest case |
| `derived_not_curated_audit`, `column_vocabulary_audit`, `schema_reference_audit` | B | curated lists; column names; name resolution | pass | New tooling must satisfy each |
| `pipeline_completeness_fresh`, `evidentiary_audit_fresh` | B | derived dashboards | — | Red on any data PR that does not regenerate |
| `attestation_presence`, `attestation_schema` | B | synthesis-path changes | — | P1's session record needs an attestation |
| `supersession_backpointer_audit` | A | `SUPERSEDES:` lines | — | Section 11's lines must quote exactly-once text |
| `research_tooling_separation` | A | each changeset | — | Ledger edits classify as governance, allowed in either PR |

### 8.2 New checks and rules proposed

| Check | Level | What wrong thing it prevents | What reads it | Examines on first run |
|---|---|---|---|---|
| **R16-scan** (batch rule) | B, via the batch gate | An admitted source never read against the catalogue | the batch gate; `/batch-done` | The batch's admissions. A batch with none examines 0, and R9a and R9b fail that batch anyway. |
| **scan-debt** | A; blocking over the Release 0 source set from P7 | The catalogue implying "nothing found" where nobody read; a new parameter never back-filled | the catalogue evidence line; Release 0 acceptance; the next cohort's worklist | **Red, not vacuous**: every pair is NOT-READ until the first readings |
| **observation backstop** | A, with a baseline | A phrase not in its source mints vocabulary | R16; the independent review | 88 observations; 17 not found, reported against a baseline; unscoped matches reported apart |
| **admission-edge rule** | B (batch) | A source with no search behind it, invisible to coverage | coverage views | Batch admissions. Corpus baseline 2 (REF-00987, REF-01010), repaired in P3 C1. |
| **catalogue_reach** | B, from P6 | A parameter silently missing from the catalogue | the render | All active parameters. Registered with the first placements so it is not red on `main`. |
| **follow-up governing** | A | A published value resting on an open follow-up or a skim figure, without the reader being told | the render; the engine report | **Vacuous until the first live determination**; stated in its note |
| category-name guard | write refusal, plus `validate_parameters` extended | A category name stating a value | the render | The registry rows |

---

## 9. Risks and what this plan does not do

### 9.1 Risks

| Risk | How it is contained |
|---|---|
| The list mirrors what codes measure, not what disabled people need | Co-1 and research sources in every cohort (R1); qualitative and argument findings recorded; coverage compared with the ICF and access-need frames; the old item index compared only after freezing |
| The old container bias returns through names | Names come from source phrases; value guard; the "quantity or target state?" question in every review table; rename exists before names multiply |
| Bulk promotion with no way back | T1 lifecycle commands merge before any bulk promotion; retire in place only |
| Review load lands on you | Delegated vocabulary review with a veto (D5); one-page tables per cohort; no per-figure review |
| Readings claim more than they read | Text scope computed from page markers; "full" refused when pages are missing; independent review samples each source |
| Unscoped quote matches let a quote from one source verify another | Full texts re-registered under source IDs; scoped and unscoped reported separately |
| Partial and abstract-only texts read as "nothing found" | The ledger distinguishes READ-PARTIAL from READ-NOTHING-FOUND |
| The first live determination turns later work red (K02) | Determine late; same-PR re-run |
| The scheduled source-verification job writes the database and conflicts with open PRs (CLAUDE.md rule 3) | Take the branch's database when resolving; the next run re-emits |
| Aliases are mostly model-generated | Aid only; source-attested aliases grow from observations |
| Tooling scope creeps | Section 4.2 floor (items 1 and 2) ships even if the rest slips |
| A misread of your words is ledgered | Verbatim quotes beside their questions; the ambiguity kept open |

### 9.2 What this plan deliberately does not do

- No slug-to-parameter map. No element table unless D6 says so. No room relation yet.
- No lead-to-parameter link. No `observation_id` on extractions.
- No change to the slug-keyed search tables.
- No deletion of rows, including the nine.
- No retrieval task for anything with no route.
- No research outside buckets 1 and 2.
- No published determination before reading debt is zero.
- No use of `terms.domain` or `axes` for grouping.
- No old item name or value imported.
- No determination by hand.
- No new critique of this plan without your commission.

---

## 10. Decisions for you

Each decision gives one question, a recommendation, and what changes with your answer. **Answer D1, D2, D3 and D8 first. They gate everything else.**

**D1. What did your answer "2" mean?** You were asked "Does a preliminary or skim extraction ever govern a published cell?" and answered *"..yes? like, one pulled from another slug? should be yes, but we still tag it for follow up later"*. Please answer each part separately:
- **(a)** May a figure that was only skimmed, or not yet reviewed, set a published value if it is tagged for follow-up?
- **(b)** May a figure from a source filed under a different topic set a published value if it is tagged for follow-up?

*Recommendation:* (b) yes, with the tag. (a) no, until someone reads the full text. In batch 15, an abstract suggested REF-01001 was Co-1 work; the session declined to claim it, and the full text showed the claim would have been false (recorded in the parameter 3 determination gate).

*Effect:* (b)-yes adds the follow-up table to T1. (a)-yes adds only a reader of the existing columns. (a)-no adds an engine rule, in tooling, so skimmed figures cannot set a value. Determinations (P8) wait on this answer.

**D2. Keep the nine parameters?** The nine are corridor width, turning circle, operating force, reverberation time, LRV contrast, door width, colour temperature, headroom clearance and ramp run length.

*Recommendation:* keep all nine and bring them to `main` in P1. Note two points for later renaming once the command exists: sources say "turning space" rather than "turning circle", and "vertical clearance" rather than "headroom".

*Effect:* if you strike any, the struck ones wait for `retire-parameter` (T1). They are never deleted.

**D3. Must parameter names still come only from a phrase an admitted source uses?** That is your 2026-09-09 rule, "use add-term for now". Your "A" asked for each object turned into its quantities with names proposed for your review. Your 06:07 message arrived before you saw the choice "1. slug by slug / 2. you seed it", so that choice is open.

*Recommendation:* keep the rule. Use your "A" list (each object term's likely quantities) as a **search checklist** for the readers. The names themselves are still taken from source phrases.

*Effect:* if you revisit the rule, T1 gains a way to mint names on your authority, and the ledger records a supersession of the 2026-09-09 clause.

**D4. Judge "categorically exhausted" per parameter and jurisdiction, not per slug?**

*Recommendation:* yes (section 7.4).

*Effect:* T2 builds the parameter-by-jurisdiction view. The ledger records the change to the 2026-09-28 wording.

**D5. Who reviews new parameters in bulk, and must vocabulary writes get independent review?**

*Recommendation:* a reviewer you name (an independent model, as on 2026-09-11) adjudicates each cohort's one-page table, and you keep a veto. The batch's independent review covers vocabulary writes as a standing subject.

*Effect:* this sets P3 and P4's review step and its load on you.

**D6. Is an item one parameter or one element?**

*Recommendation:* one parameter, for Release 0 (section 6.1).

*Effect:* element items need a warranted many-to-many relation in T2.

**D7. Approve the category list and its order once, from a draft built after the first reading cohorts.**

*Recommendation:* yes. Draft from the held codes' chapter structure and the access-need families. Not from old items, `terms.domain` or `axes`.

**D8. Approve tooling PR T1 as listed in section 4.2, merged before any bulk promotion.**

*Recommendation:* yes.

*Effect:* without it, P3 and P4 cannot record readings or correct names.

**D9. Publish Release 0 as described in section 6.6, with no determinations, once reading debt over its source set is zero?**

*Recommendation:* yes.

**D10. Read what is already held before fetching anything new?**

*Recommendation:* yes. It costs no network, and it covers most bucket codes we have.

**D11. Read the out-of-bucket sources already admitted (BE, UG, IN, BR, HR) too?**

*Recommendation:* yes. They are held evidence. They do not count toward bucket coverage.

**D12. Record this session's words in the ledger verbatim, as in section 11, with "2" marked ambiguous?**

*Recommendation:* yes.

**D13. Keep the two finished batch 23 scan outputs (52 items) only as test material for the one-phrase-two-parameters fix?**

*Recommendation:* yes. They are not data.

---

## 11. Record-keeping

### 11.1 What a later session writes to the ledger

Write one dated entry in `references/project-standards.md`, titled for example "Owner statements 2026-10-09: scanning is by parameter, not slug; the parameter registry seed; the catalogue plan". It goes in the first PR that acts on it (P1). It must carry:

- **Your words, verbatim, each beside the question it answered.** That is every row of section 2.5, including:
  - "note that while we search by slug, we scan each source for any and all applicable parameters. we may need to just prepopulate a parameters list.";
  - "1 yes" (seed);
  - "2 ..yes? like, one pulled from another slug? should be yes, but we still tag it for follow up later", recorded as **ambiguous between (a) and (b), pending D1**;
  - "keep wp12 rule";
  - "populate a parameters table";
  - "we need like the 90+ cleaned parameters without values";
  - "A", with the A/B text quoted;
  - "... why would you develop a parameter database for coverage of all accessible design terms possible by using batch 23 that came from a specific slug";
  - "pull from the major codes, literature and advocacy from major countries", noting it preceded the 1-or-2 choice;
  - "there should be an exhaustive bibliography that is outdated but correct that has info on each jurisdiction code bodies and major groups";
  - the 20:22 requirements, quoted in full.
- **Your answers to section 10**, verbatim, when given.
- **The fact about the nine:** added on a scratch copy and applied on this branch by `a8b7c11` without a PR, record, attestation or review; kept, not reverted, per the 2026-09-16 ruling.
- **CONDITION / ACTION / DATE** lines in the ledger's usual form.

### 11.2 Supersessions rule 0 requires to be named

The grammar is documented in `scripts/audit/supersession_backpointer_audit.py`. A later session writes these. This paper does not. Each target quote must occur exactly once under that script's normalization: check with the script before writing. Each target also needs a SUPERSEDED or AMENDED marker carrying the BY quote, placed in or right after the quoted paragraph.

1. **The adversarial rule, for this plan only.**
   `SUPERSEDES: references/project-standards.md :: "Plans, critiques, censuses, handoffs, registers, session records, Decision Records and this ledger are not adversarial-pass subjects"`
   `BY: references/project-standards.md :: "<a sentence from the new entry quoting your commission of the critique>"`
   Scope: this catalogue plan only.
2. **The pilot's scope.**
   `SUPERSEDES: scratchpad/session_2026-10-01-research-batch-23/process-gap-remediation-plan.md :: "The pilot is a judgement-stage re-read of batch 23's 14 admitted sources."`
   with a BY quote of "pull from the major codes, literature and advocacy from major countries".
   Name the cap the same way: `:: "**Extractions ≤ 2 × batch 23's.**"`.
3. **The pilot's figure-only harvest.** The step 2 phrase `"Do this for every concept phrase the source states a figure for"` narrowed your 2026-09-18 directive. Name it superseded BY the new entry's quotation of "Slugs guide our searches, but they do not guide what we derive and mine from sources!".
4. **Only if D4 is yes:** `SUPERSEDES: references/project-standards.md :: "exists for every bucket-1 and bucket-2 jurisdiction against the slug's parameters"`.
5. **Only if D3 revisits the rule:** `SUPERSEDES: references/project-standards.md :: "Mint parameter names with \`db.py add-term --from-observation\`, never by hand"`.

### 11.3 Elsewhere

- The session record for this session, with its attestation (rule 2).
- Commit the scratchpad and transcripts at natural breaks (`python3 scripts/preserve_transcripts.py`).
- Open each PR last, then unsubscribe from it straight after creating it (rule 9).
- Correct the two stale registry notes (section 1.2, item 7) when those entries are next touched.

---

## 12. Acceptance tests and re-derive commands

### 12.1 Commands (all read-only; run from the repository root)

**S1. State counts.**

```
python3 - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
Q = {"terms": "select count(*) from terms",
 "active parameters": "select count(*) from base_parameters where status='active'",
 "parameters with no adjudication behind their term": "select count(*) from base_parameters p where not exists (select 1 from term_adjudications a where a.term_id=p.term_id)",
 "parameters with direction unset": "select count(*) from base_parameters where accessibility_direction is null",
 "admitted sources": "select count(*) from evidence_sources",
 "tombstoned sources": "select count(*) from evidence_sources where superseded_by_ref_id is not null",
 "unverified sources": "select count(*) from evidence_sources where verification_status<>'VERIFIED'",
 "sources with no admission edge": "select group_concat(ref_id) from evidence_sources e where not exists (select 1 from search_admissions a where a.ref_id=e.ref_id)",
 "extractions": "select count(*) from source_value_extractions",
 "parameters carrying any extraction": "select count(distinct parameter_id) from source_value_extractions",
 "slugs carrying any extraction": "select count(distinct slug) from source_value_extractions",
 "slugs used by any search": "select count(distinct slug) from search_executions",
 "lead-index searches": "select count(*) from search_executions where origin='lead-index'",
 "live determinations": "select count(*) from specifications where retired_at is null",
 "observations / unjudged": "select count(*) || ' / ' || sum(not exists (select 1 from term_adjudications a where a.observation_id=o.observation_id)) from observed_terms o",
 "named terms neither promoted nor declined": "select group_concat(distinct a.term_id) from term_adjudications a where a.term_id is not null and not exists (select 1 from base_parameters p where p.term_id=a.term_id) and not exists (select 1 from parameter_declinations d where d.term_id=a.term_id)",
 "aliases / languages": "select count(*) || ' / ' || count(distinct language) from term_aliases",
 "source_locators / with standard number / REFERENCE-ONLY": "select count(*) || ' / ' || sum(coalesce(standard_number,'')<>'') || ' / ' || sum(status='REFERENCE-ONLY') from source_locators",
 "code leads": "select count(*) from research_code_leads",
 "candidates pending verification": "select count(*) from search_candidates where disposition='PENDING-VERIFICATION'",
 "extractions preliminary / skim / absent / verbatim-exempt": "select sum(extraction_status='preliminary') || ' / ' || sum(extraction_method='skim') || ' / ' || sum(claim_type='absent') || ' / ' || sum(notes like '%VERBATIM-EXEMPT%') from source_value_extractions"}
for k, q in Q.items(): print(f"{k}: {c.execute(q).fetchone()[0]}")
PY
```

**A1. Saved files per source, with PDF pages and derived-text pages.** pymupdf reads the PDFs.

```
python3 - <<'PY'
import sqlite3, json, glob, os, re
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
recs = []
for m in glob.glob('retrieval-log/*/manifest.jsonl'):
    for line in open(m, encoding='utf-8'):
        r = json.loads(line); r['_d'] = os.path.dirname(m); recs.append(r)
import pymupdf
for ref, url in c.execute("select ref_id, url from evidence_sources order by ref_id"):
    roots = [r for r in recs if not r.get('derived') and (r.get('ref_id') == ref or (url and r.get('url') == url))]
    names = {(r['_d'], r['artefact']) for r in roots}
    kids = [r for r in recs if r.get('derived') and ((r['_d'], r.get('derived_from')) in names or r.get('ref_id') == ref)]
    out = []
    for r in roots + kids:
        p = os.path.join(r['_d'], r['artefact'])
        if not os.path.exists(p): continue
        if p.endswith('.pdf'): out.append(f"{r['artefact']} {pymupdf.open(p).page_count}pp")
        elif p.endswith('-text.txt'):
            n = len(re.findall(r'^\[PDF page', open(p, encoding='utf-8', errors='replace').read(), re.M))
            out.append(f"{r['artefact']} text:{n}pp" if n else f"{r['artefact']} text")
        else: out.append(r['artefact'])
    print(ref, '|', '; '.join(sorted(set(out))) or 'NO MATCHED ARTEFACT')
PY
```

**A2. Where the four unmatched sources' quotes verify (scoped or unscoped).**

```
python3 - <<'PY'
import sys, sqlite3; sys.path[:0] = ['scripts/research', 'scripts']
import retrieval_log as rl
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for eid, ref, ct in c.execute("select extraction_id, ref_id, claim_text from source_value_extractions where ref_id in ('REF-00990','REF-00991','REF-00999','REF-01000')"):
    print(eid, ref, rl.quote_in_artefacts(ct, ref_id=ref))
PY
```

**O1. How observation quotes verify today** (a few minutes).

```
python3 - <<'PY'
import sys, sqlite3, collections; sys.path[:0] = ['scripts/research', 'scripts']
import retrieval_log as rl
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True); res = collections.Counter(); inside = 0
for ref, sf, cq in c.execute("select ref_id, surface_form, context_quote from observed_terms"):
    if not cq: res['no quote'] += 1; continue
    inside += rl.normalise_quote(sf) in rl.normalise_quote(cq)
    ok, d = rl.quote_in_artefacts(cq, ref_id=ref)
    res['scoped' if ok and 'UNSCOPED' not in d else 'unscoped' if ok else 'not found'] += 1
print(dict(res), 'phrase inside its own quote:', inside)
PY
```

**V1. Every `db.py` command.**

```
python3 -c "import re;v=sorted(set(re.findall(r'add_parser\(\s*\"([a-z0-9-]+)\"',open('scripts/db.py').read())));print(len(v));print(' '.join(v))"
```

**V2. Parameter definitions carrying value or direction words.** Uses the same pattern as `db.py`.

```
python3 - <<'PY'
import sqlite3, re
V = re.compile(r"[0-9≥≤<>=]|\b(min|max|minimum|maximum)\b", re.I)
c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for t, n, d in c.execute("select t.term_id, t.canonical_en, t.definition from base_parameters p join terms t using(term_id)"):
    if d and V.search(d): print(t, n, '|', d)
PY
```

**V3. Bucket jurisdictions in the enum.**

```
python3 -c "import sys;sys.path.insert(0,'.');from schemas.enums import JurisdictionCode as J;h={j.value for j in J};print([x for x in 'UN ISO CA US UK DE NO SE JP AU EU SG NZ IE FR ES PT FI NL KR'.split() if x not in h])"
```

**V4. Tables that cannot accept rows.** This is CLAUDE.md §4's command; run it as printed there.

**T1. Your messages this session, with times.**

```
python3 - <<'PY'
import json
for line in open('transcripts/harness_db856d85/main.jsonl'):
    e = json.loads(line)
    if e.get('type') == 'queue-operation' and e.get('operation') == 'enqueue' and not e.get('content', '').startswith('<'):
        print(e['timestamp'], 'QUEUED:', e['content'][:300].replace('\n', ' '))
    elif e.get('type') == 'user' and (e.get('origin') or {}).get('kind') == 'human':
        c = e['message']['content']
        t = c if isinstance(c, str) else ' '.join(x.get('text', '') for x in c if isinstance(x, dict))
        print(e['timestamp'], 'TYPED:', t[:300].replace('\n', ' '))
PY
```

QUEUED lines are the moment you sent a message, including messages sent while the session was working. TYPED lines are when the session received it.

**Gates.**

```
python3 scripts/audit/research_batch_dod.py --session session_2026-10-09-research-batch-24-parameter-pilot
python3 scripts/audit/research_batch_dod.py --session session_2026-10-01-research-batch-23
python3 scripts/audit/research_batch_dod.py --all
python3 scripts/audit/adversarial_pass_audit.py --session session_2026-10-09-research-batch-24-parameter-pilot
python3 scripts/tests/test_db_integrity.py
python3 scripts/generate/build_site.py --check
python3 scripts/audit/alias_provenance_audit.py
```

### 12.2 Acceptance tests (each must be able to go red on the defect it addresses)

| Test | Proves | Red today? | Command (new ones are built in T1 or T2) |
|---|---|---|---|
| **Q1. Slug independence.** A fixture source linked only to slug S yields extractions for two parameters no search under S targeted. The catalogue view for each parameter lists it. No catalogue query reads `extraction.slug`. | Requirement 2 | The extraction part already works. Grep for a catalogue view reading `.slug`: none exists yet. | `pytest`-style fixture in `scripts/tests/test_scan_contract.py` (T1); plus `git grep -n "\.slug" -- scripts/generate/` showing no catalogue use |
| **Q2. One clause, many quantities.** A fixture clause stating three quantities yields three extractions with the same locator. | Requirement 3 | Works today; pinned | same file |
| **Q3. One phrase, two parameters.** Observing "clear width" at two locators in one source gives **two** observation rows, judged to two terms; R16 counts both. | Requirement 3, F3 | **Red today:** the second call returns `created: False` | same file; reuse `harvest/es-small.json` `also_at` cases (D13) |
| **Q4. Back-fill debt is visible.** A source read at catalogue version N shows NOT-READ for a parameter numbered above N, and scan-debt counts it. | Requirements 3 and 4, F13 | **Red today:** no record exists | `test_scan_contract.py`; then `select status, count(*) from v_scan_ledger group by 1` |
| **Q5. "Full" cannot be claimed over partial text.** `record-scan --text-scope full` on REF-01027 with its 4-page text is refused. | F9, F13 | No command yet | same file |
| **Q6. Observation quote must be in the source.** `observe-term` with a context quote absent from the source's saved text is refused. With `--verbatim-exempt` it lands, recorded. | F7 | **Red today:** accepted | `scripts/tests/test_db_amend_writers.py` extension |
| **Q7. Growth paths exist and refuse correctly.** Retire refuses with a live determination. Merge re-points every extraction and K02 then needs re-determination. Rename refuses a value-bearing or answer-shaped name and keeps a DEPRECATED alias. Revoke needs a reason. Add-alias needs a provenance marker. | Requirement 4, F5 | **Red today:** the commands do not exist | V1 shows the commands; tests in `test_db_amend_writers.py` |
| **Q8. New tables are captured.** Each new table is in `dbcore.writable_tables(conn)` on a scratch copy, and a round trip through `emit_batch_sql` reproduces it. | Rule 8 trap (capture blindness) | Not applicable until T1 | `test_scan_contract.py` |
| **Q9. Readers filter retired parameters.** After retiring a fixture parameter, no view or catalogue surface lists it. | 2026-09-16 condition | Not applicable until T1 | `test_scan_contract.py` over every view selecting `base_parameters` |
| **Q10. Sessions have subjects.** Each research session's record shows the batch gate on its own name with R1, R9a, R9b, R11-harvest, R16 and R16-scan examining more than 0, and on each admitting name for re-reads. | Requirement 1, F2 | **Red today** on this session's name | `research_batch_dod.py --session <name>` |
| **Q11. No parameter left out.** `catalogue_reach` fails on a fixture parameter with no category. | F6 | Not applicable until T2 | T2 test |
| **Q12. Release 0 is honest.** For the Release 0 source set, scan debt is 0. Every figure shown carries a marker matching tier-system §5 and the 2026-09-13 ruling (T6 without research backing shows ○). No item or category name matches the value guard. | F1, L7, §1.2 item 1 | Red until P3/P4 | scan-debt check; `validate_parameters` extended; render test |
| **Q13. Determination re-run.** A PR adding an extraction on a determined parameter without re-running the engine is red on K02. | F14 | Vacuous today (no live determination) | `python3 scripts/tests/test_db_integrity.py` |
| **Q14. Your words are recorded verbatim.** Each quote in the ledger entry occurs in the transcript (T1 command), and "2" is marked ambiguous. | F8 | Not applicable until P1 | T1 command plus a `grep -F` per quote |
| **Q15. The nine reach `main` properly.** The PR carrying `data_20261009055057_…` also carries a session record, an attestation and your recorded review. | F11 | **Red today** | `git ls-tree origin/main scripts/migrations/ \| grep 20261009` after merge; `attestation_presence` |

---

## Addendum 2026-10-09 (written after the paper): your answer to D1

This addendum is appended, not edited into the sections above, so the paper still shows what was true when it was written. Sections 3.7, 4.2, 7.6 and 10 are read with this addendum.

**Your words, verbatim:** "D1: yes figure from source filed by another slug allowed. skimmed values are not publishable"

**How it is read (assumptions marked):**
- **D1(b), yes.** A figure taken from a source filed under another slug may be extracted and may set a published value. Your earlier words, "we still tag it for follow up later" (03:08), were not withdrawn, so the follow-up tag stays. [ASSUMPTION: the tag is still wanted.]
- **D1(a), no.** "Skimmed" is read as the typed column `extraction_method = 'skim'`. A skimmed extraction may be recorded and shown, marked as skimmed, but may not set a published value. [ASSUMPTION: that is what "skimmed" means to you.]
- **Not settled (D1c).** Figures that were read in full but are still marked `preliminary` (not yet reviewed): the engine rule below does not exclude them. They keep governing exactly as they do today, and the new follow-up reader lists them. [OPEN: if you want them excluded as well, say so.]

**What this changes in the plan**
1. Tooling T1 gains the follow-up table described in section 3.7 under reading (b): typed reason, required warrant sentence, who raised it and who resolved it. Its first reason is `read-outside-admitting-purpose`.
2. Tooling T1 gains one engine rule: the determination engine excludes skimmed extractions from the set that governs a value, and records each as excluded with a reason. The engine already has a way to record an excluded figure with a reason, and the integrity check that every figure is accounted for counts it. Today the engine reads neither `extraction_method` nor `extraction_status` (`grep -c "extraction_status\|extraction_method" scripts/assess/assess_cell.py` gives 0). The rule is the first reader of that column.
3. D1 is closed except D1c. Section 7.6 ("determine late") no longer waits on D1.

**An opportunity this opens (not scheduled).** 14 extractions are skimmed today, all on parameter 3 (`select count(*) from source_value_extractions where extraction_method='skim'`). They include both of REF-01002's extractions (44, 45) and both of REF-01004's (50, 51), which is why the ramp-gradient cell has been stuck: the one T1 source with a stated maximum is held only as an abstract. Once the rule exists, those rows leave the set that governs the value, so the cell would no longer depend on REF-01002, and the check that blocks a value resting on an unverified source would not be engaged by it. Parameter 3 for wheelchair users could then be determined from the full-read rows (codes, the grey and Co-1 sources, the reviews) without the 2009 study. [INFERRED: the engine has not been run.] The paper schedules determinations after reading debt is zero (section 7.6). You may bring this one forward.

**Still to be recorded.** This answer goes into the ledger verbatim with the other words from section 2.5, in the first pull request that acts on it (P1).

---

## Addendum 2 (2026-10-09): your answers to D2, D3 and D8

**Your words, verbatim:** "D2 yes, D3 keep the rule, D8 approve tooling"

- **D2, yes.** The nine parameters (4 to 12) are kept and go to `main` through phase P1, with a session record, an attestation and the ledger entry. Nothing is reverted.
- **D3, keep the rule**, qualified by the follow-up in Addendum 3. Parameter names that come out of research are minted only from a phrase an admitted source uses (`add-term --from-observation`), as the 2026-09-09 ruling says. Section 10 recommended also using your option A list as a search checklist for the readers; you did not answer that part, so it is not adopted. [OPEN: say if you want it.]
- **D8, approve tooling.** Tooling PR T1 as listed in section 4.2, items 1 to 5, is approved and ships before any bulk promotion. T1 must be its own pull request off `main` (project rule 10), so it needs its own branch.

**Still unanswered, with the recommendations in section 10 standing but unapproved:** D4, D5, D6, D7, D9, D10, D11, D12 (the ledger entry is written anyway because CLAUDE.md rule 0 requires it), D13.

---

## Addendum 3 (2026-10-09): your follow-up on D3

**Your words, verbatim, sent right after "D2 yes, D3 keep the rule, D8 approve tooling":** "D3 for parameter terms? it can be pulled from previous catalogues of entries for prepopulating"

**How it is read.** For prepopulating the parameter list, names may be taken from previous catalogues of entries. That narrows the 2026-09-09 rule ("never by hand") for prepopulation only; names that come out of research still come from observed phrases. Section 11.2 item 5 is therefore triggered: the supersession of the 2026-09-09 clause is recorded, in prose, in the 2026-10-09 ledger entry (the back-pointer grammar cannot mark a clause that sits in the ledger itself).

**Not settled, and it matters (nothing is minted from a previous catalogue until you answer):**
1. **Which previous catalogues?** The candidates, none of them chosen: the 93 old Part 4 item names (the list the 2026-09-01 ruling deleted); the terms and parameters held in the pre-reset corpus database; the code and standards registries (`references/standards-registry.md` and the verified-source files); or something else.
2. **What guard applies to names taken from them?** The earlier rulings say a container whose name states its answer biases every finding (2026-09-01), that no old item name becomes a topic and no old value crosses (2026-08-19, DR §1.4), and the database already refuses a name carrying a digit or a min/max word. Your own earlier words were "cleaned parameters without values".
3. **How is a name minted without a source phrase?** `insert_term` refuses to mint from nothing. This is the "you seed it" route: T1 gains a minting route on your authority, with the catalogue and the warrant recorded on each term, and the old item index is not read until you have named it as a source.

**Effect on the sequence.** T1 (approved) gains item 3 above. Reading the held sources for the existing parameters (phase P3) does not depend on it and can go ahead. The open pass for new quantities still produces names from source phrases.

---

## Addendum 4 (2026-10-09): your answers on the previous catalogues, the guard and the T1 branch

**Your selections (from listed options; not typed words):**
- Previous catalogues that names may be pulled from: **"Code and standards registries"** and **"Old corpus terms"**. The old Part 4 item names were offered and not selected.
- Guard: **"Screen, then you approve"**.
- A second branch for tooling T1: **"Yes, second branch"**.

**What follows.**
1. The candidate pool for prepopulation is the two selected catalogues. The old item names stay out, as the 2026-08-19 and 2026-09-01 rulings keep them. Reading the pre-reset corpus database for its terms is a read of a lead list.
2. Every candidate is screened (no digit, comparator or min/max word, no old item code) and shown to you in one table, with the catalogue and the entry it came from, before any is minted.
3. Minting a name on this authority needs a route `insert_term` does not have. That is a new item in tooling T1, with the catalogue and the table row recorded on each term so the provenance is machine-readable. **[NOTE 2026-10-10: the session added this route after D8. The owner has approved the permission and the guard, not the route's design; it goes to the owner on the T1 pull request (ledger entry, items 3 and 5).]**
4. T1 is built on its own branch off `main`. This branch keeps the nine parameters, the records and the plan. **[CORRECTED 2026-10-10: this branch's pull request was opened first, but T1 merges first (project rule 10, tooling before research); the second to merge takes `main`'s database blob and re-runs `migrate_db.py`. The ledger entry's item 5 is the record; the sentence this replaces said this branch goes up first.]**
5. The registries list code bodies and standards, not measurable quantities, so they will yield few parameter names. [INFERRED: not yet read for names.] The pre-reset terms are mostly the terms already in the live registry, since the live registry was seeded from them. [INFERRED: the archive has not been read for this.] Both are cheap to check before T1 is built.
