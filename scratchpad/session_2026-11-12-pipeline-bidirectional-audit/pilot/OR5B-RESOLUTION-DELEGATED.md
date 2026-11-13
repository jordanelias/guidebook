# OR-5b: resolution of the three open edges (delegated, reversible by the owner)

Written 2026-11-13 by an Opus-class session on delegation. This is a delegated resolution: it is not the owner's words, and the owner can reverse any part of it. Nothing in the repository or the database was changed. Every figure is given as the command that computes it; re-run it and do not trust a number typed here.

## Verdicts

1. **Edge 1: resolved.** "Academic rigour re PubMed" means reading (b): a study is judged against the standard PubMed-indexed work meets, which is a method reported fully enough for its design to be appraised (the EQUATOR guideline for that design, as the owner confirmed). Whether the study is indexed in PubMed is recorded as a fact and is never the test, because reading (a) breaks R5 and the owner's 2026-11-06 ruling that a government report can be academically sound.
2. **Edge 2: resolved.** A DPO position statement, or a lived-experience publication that reports no study, has no route to "academically sound" and sets the direction, not the number. This is the ruling's own "otherwise" branch, and it keeps the source at Co-1, tier 1 and the full band. A DPO output or lived-experience work that does report a study is judged as a study under edge 1, so `co1_source_type` alone never decides.
3. **Edge 3: partly resolved.** The three-part test is the project's one definition of "academically sound" for every tier, since the owner's words name T4 to T6, which no Co-1 source can hold. What soundness *does* is ruled only for a Co-1 figure (OR-5), for a grey government report at T3 (2026-11-06) and for T4 to T6 (OR-23b). Whether soundness also controls a T1 clinical, T2 or Co-2 figure is evidence-tier doctrine. Logic cannot settle it, so it is put to the owner below.

---

## Sources read

- The OR-5b entry: `grep -n -F "OR-5b — how a Co-1 source" references/project-standards.md`. Its prompt is `grep -n "OR-5b" governance/owner-browser.yaml`.
- OR-5 itself and its ACTION, including the 2026-10-29 [ASSUMPTION] that OR-5 applies before OR-4: `grep -n "Co-1 figures may set a value" references/project-standards.md`.
- The owner's 2026-11-06 (second) ruling, item 3: "if government report is academically sound then it can be t3 I think". Find it with `grep -n "if government report is academically sound" references/project-standards.md`.
- OR-6c and OR-23b, in the tenth set.
- R5:
  - Its home is `governance/research-contract.yaml` (`git grep -n "INDEXING fact" -- governance`), and the harness hook in `.claude/settings.json` injects it.
  - Its enforcer is `scripts/audit/research_batch_dod.py`. Since 2026-10-02 the enforcer fails a non-English admission that is filed `grey` but is a journal article, names a journal or carries a DOI. A waiver needs the token `R5-GREY-WARRANTED:`.
  - The enforcer's resolution text records that "a DOI or journal name marks publication, not peer review".
- The tier derivation is `schemas/tier_derivation.py`:
  - `co1` takes only the scope `intrinsic` and always derives tier 1.
  - `clinical` is T1 with the scope `high_control` and T3 with `lower_control`.
  - `sr_meta` is T2.
  - `standard_eb` is T2 when national and T4 when international.
  - `national_fw` is T5 and `code` is T6.
- `governance/tier-system.md`:
  - Line 11: "Tier number reflects what kind of claim a source can anchor, not how good the source is."
  - The T2 definition (DR-2026-07-21): `sr_meta` is reserved for systematic reviews with "a defined method with risk-of-bias appraisal and/or effect synthesis".
- `governance/co1-operational.md` §1.2. Co-1's methodological grounding is "peer review", "organizational accountability" or "authorship by people whose lived experience is the subject".
- `references/methodology-evidence-hierarchy-mapping.md` §6.3 to §6.4 (the AMENDED note of 2026-10-29).
- CLAUDE.md §3 stage table: the **judgment** stage holds "whether it is sound".
- The live Co-1 rows, read only: `select ref_id, co1_source_type, source_type, grey_flag, verification_status, doi, pmid from evidence_sources where evidence_type='co1'`.
  - Today there are two `participatory_research` journal articles. Both carry a DOI and a PMID.
  - There is one `lived_experience_publication`, a first-person web article by a wheelchair user.
  - There is one `dpo_position_statement`, DPI-Japan's analysis of the CRPD Concluding Observations and its action plan.
  - **The last two have `source_type` NULL.** OR-5b's "derive" option reads the type, so it cannot be applied to them as the data stand.
- A search of the schema found no column or table that records soundness, appraisal, peer review or the reporting guideline a source follows. Re-derive with a `sqlite_master` search for `sound|apprais|rigo|peer|reporting_guideline|risk_of_bias`. The only hits are `case_studies.evidence_quality_tier` and `evidence_sources.metadata_quality`, and neither is this fact.

External facts:

- **Checked 2026-11-13: EQUATOR.** "Reporting guidelines are recommendations of information to include when writing up research. … However, reporting guidelines are not design standards or tools for quality appraisal." (resources.equator-network.org/about/reporting-guidelines.html.)
- **Checked 2026-11-13: MEDLINE selection.** NLM selects journals for MEDLINE by the journal, not the article. It reviews "each journal comprehensively", on five elements that include editorial policies and processes (peer review) and scientific or methodological rigour (nlm.nih.gov/medline/medline_journal_selection.html).
- **Checked 2026-11-13: PubMed's makeup.** PubMed has three parts: MEDLINE, then PMC citations, then Bookshelf. The "About" page states nothing that makes inclusion a mark of quality (pubmed.ncbi.nlm.nih.gov/about/).
- **Checked 2026-11-13: GRIPP2.** GRIPP2 is the EQUATOR-method checklist for reporting patient and public involvement (Staniszewska et al., BMJ 2017;358:j3453). It has a long form and a short form (SF).
- **Held from memory, [UNVERIFIED]:**
  - PRISMA 2020 (Page et al., BMJ 2021) is the reporting guideline for systematic reviews and meta-analyses.
  - COREQ covers interview and focus-group qualitative research.
  - SRQR covers qualitative research generally.
  - STROBE covers observational studies.

---

## Edge 1: what "academic rigour re PubMed" means

**The owner's words, read closely.** The owner's first answer was the EQUATOR link. The assistant read it as "conformity to the reporting guideline for the source's design" and asked to confirm. The reply opens with "Yes", so the EQUATOR reading of the design-specific reporting guideline is confirmed. The rest of the reply names the guideline for one design (PRISMA, for systematic reviews and meta-analyses) and then sets "academic rigour re PubMed" for "any other study outside those bounds". In that clause the noun is *rigour*, a property of the work. "Re PubMed" names whose standard of rigour applies. If membership of an index were meant, the words "indexed in PubMed" were available. Read inside an answer that has just confirmed EQUATOR, the clause names the bar that EQUATOR's design-specific guidelines describe: the bar of biomedical journal work.

**Reading (a), "indexed in PubMed", breaks three standing rulings and one fact:**

- **R5.** "Non-indexation in PubMed/Scopus is an INDEXING fact, not an evidence-quality fact." Reading (a) turns that indexing fact into the quality test for the clause. A non-English peer-reviewed study in a journal outside MEDLINE's biomedical scope would fail on the index, not on its rigour. R5 is a standing ruling, and rule 0 gives no licence to read a later answer as silently overturning it when another reading keeps both true.
- **The 2026-11-06 ruling.** "If government report is academically sound then it can be t3." A government report is almost never in PubMed. Under (a) that ruling is close to empty, so (a) makes one owner ruling nearly vacuous in order to define a phrase in another.
- **Criterion 1, integrity.** NLM's selection is made per journal (checked). An index flag is a fact about a venue's editorial process, not about the article in hand. PMC citations, PubMed's second part, enter by a separate route. Using the flag as the article's soundness would record a venue fact as an article fact, a false provenance, which is the failure criterion 1 ranks first.
- **Criterion 3, coverage.** Built-environment, architectural and non-English journals lie largely outside PubMed's biomedical scope. Under (a) a whole discipline's figures would be held to direction for a reason unrelated to their quality.

**Reading (b) keeps every standing ruling true.**

- R5 holds, because the index is never the test.
- The 2026-11-06 ruling has content, because a report can meet the bar.
- OR-5 holds, because soundness stays a property of the source.
- Rule 8 holds, because a judgment is made and recorded with its warrant.

**What "the standard" is.** The work's own report gives its design and method fully enough to be appraised, measured against the EQUATOR guideline for that design (for example STROBE, COREQ, SRQR or GRIPP2; their scopes are [UNVERIFIED] beyond GRIPP2).

**What follows for the fields:**

- **The PMID.** `evidence_sources.pmid` stays a recorded fact. It is neither necessary nor sufficient for soundness.
- **Peer review.** Peer review counts toward rigour, but it is not a necessary condition: the 2026-11-06 ruling contemplates a sound report that was not refereed. Neither `source_type = 'journal_article'` nor a DOI shows peer review. The R5 enforcer's own text says "a DOI or journal name marks publication, not peer review".

**One fact the owner should have, though it is not a question for the owner.** EQUATOR states that reporting guidelines "are not design standards or tools for quality appraisal". The owner's test is therefore a test of *reporting adequacy*: whether the work shows enough of its method for a reader to judge it. That is a defensible floor for "academically sound", and the owner chose it. It is not a risk-of-bias appraisal. Nothing recorded under this test may claim that a source was "appraised" or "low risk of bias". The warrant column (below) records which guideline was used and what was found.

**What would change this resolution:**

- the owner stating that indexing itself was meant (then R5 is superseded, rule 0, and the supersession is recorded);
- the owner stating that peer review is a necessary condition (then a non-refereed report or DPO research output can never set a value, and the 2026-11-06 ruling narrows to refereed government reports).

## Edge 2: a DPO position statement or a lived-experience publication

**What the ruling already decides.** OR-5 reads: "Co-1 figures may set a value insofar as the source is academically sound. Otherwise, they set the direction, not the number." The ruling expects some Co-1 sources not to be academically sound, and it gives them a role: direction. "Academically" is the owner's word. A DPO position statement is a statement of an organisation accountable to a disabled constituency. Its grounding is organisational accountability (`governance/co1-operational.md` §1.2), not academic method. It is not a study, and the second clause ("any other study") does not reach it. Its claim to evidence is real and different. A first-person article that reports no method is in the same position: its grounding is authorship by the person whose experience is the subject.

**Why a test these sources cannot pass does not erase the warrant.** Co-1's warrant is co-production, and the warrant is what earns the **tier**. The tier is fixed by `derive_tier('co1','intrinsic') = 1` and is untouched. Soundness decides only whether the figure is the number or sets the direction. Erasure, as CLAUDE.md §6 means it, would be any of the following:

- removing the source;
- moving it out of Co-1;
- deleting the people who produced it;
- dropping its direction from the determination.

None of these happens. The source stays verified Co-1, tier 1 and full band. It governs the cell's state and direction, and it is rendered beside the value (the effect the OR-5 prompt already describes).

**The reading that would break a ruling.** Treating organisational accountability or authorship as "academic soundness" would let a position statement set a dimensional value. That breaks the owner's clear word "academically" and the "Otherwise" sentence (rule 0: the owner's words bind where clear). It also re-creates the risk the 2026-10-29 ruling was answering: a number adopted with no method behind it. That would be a failure under criterion 1, which the owner ranks above criterion 3 (coverage).

**Why `co1_source_type` does not decide.** The vocabulary in `schemas.enums.Co1SourceType` sorts sources by **who** produced them, not by **whether a study is reported**:

- A DPO can publish research with a stated method; the definition's type 2 is "DPO research outputs".
- A lived-experience publication can be peer-reviewed academic work; types 1 and 4 cover peer-reviewed lived-experience literature and Co-1-authored academic narratives.
- `participatory_research` is not sound by its type; it is judged as a study.

So the route depends on whether the source reports a study, which is a judgment. Such a source is judged by edge 1's standard, and a DPO's or a disabled author's own study can set a value. This is the route by which Co-1 numbers enter on the work's merit, and it keeps criterion 3 served without lowering criterion 1. On their face, the two held sources that are not journal articles report no study. That is not decided here; the judging task records it with its warrant.

**Legibility (criterion 2).** "Not academically sound" and "not a study" are different findings, and the second must not be rendered as the first. A DPO position statement printed as "unsound" would read as a slight on the organisation and would misstate why its figure gives direction only. The verdict therefore needs a value of its own for "reports no study" (see the section on what follows).

**What would change this resolution:** the owner naming a route for a non-study Co-1 source to set a number, for example "a DPO position adopted by a national cross-disability assembly may set the value". That is a new owner ruling, not a reading.

## Edge 3: Co-1 only, or every tier

**Settled by the owner's words.** The reply ends "and then ISO for T4-6 as relevant". No Co-1 source can be T4 to T6, because `TIER_MAP` maps `co1` only to tier 1. Read as Co-1 only, that clause would have no subject. On 2026-11-06 the owner also used the same phrase, "academically sound", for a grey government report at T3. The test is therefore one definition of soundness across tiers, and rule 5 says to keep it in one home: one definition, not a Co-1 version beside a tier-wide version.

**Settled by what already exists, so it is not to be duplicated (rules 5 and 8).**

- **T2 systematic reviews.** "Systematic", with a defined method, is already the admission criterion for `sr_meta` (tier-system, DR-2026-07-21: a review that maps without appraisal goes to T3). PRISMA conformity is the reporting face of that criterion. A soundness verdict on an `sr_meta` row should therefore *read* the tier evidence and record only the PRISMA reporting finding. It must not create a second place where "is it systematic" is decided.
- **T4 to T6.** Read under the [ASSUMPTION] that the instrument is its own test, soundness for the regulatory stratum is the instrument's identity and currency. Those are already columns: `standard_number`, `jurisdiction`, `code_currency_status`, and the clause locator that R3 and OR-23b require. A T4 to T6 source is "sound as relevant" when the instrument is identified to jurisdiction, standard number and clause. This is derivable, needs no new field, and must not be stored a second time.
  - The other reading of "ISO for T4-6" is that ISO standards are the benchmark T4 to T6 figures are checked against. That reading is not excluded. It changes nothing above, because it would be a comparison made at synthesis, not a fact about a source.
- **T1 clinical.** The `high_control` / `lower_control` scope is already a method judgment that sets the tier. The Co-1 soundness test plays the same part for Co-1 that scope plays for clinical work, because `co1` enters tier 1 by its type alone with no method gate. This symmetry is why the test keeps OR-6c (Co-1 and T1 one rank) true rather than making Co-1 subordinate: each route to tier 1 carries one method gate.

**Not settled by logic: whether soundness controls a figure at every tier.** The consequences ruled so far are these: a Co-1 figure sets the number or the direction (OR-5); a grey report may be T3 (2026-11-06); a T4 to T6 instrument may anchor by registry citation (OR-23b). Nothing rules that a T1 clinical, T2 or Co-2 figure whose report fails its guideline loses the number. To say it would decide which sources can anchor what, which is evidence-tier doctrine and the owner's (CLAUDE.md §8). Two rulings bear on it in opposite directions:

- OR-6c's "same value" favours symmetry: if Co-1 must pass, perhaps T1 must too.
- tier-system line 11 favours the status quo: the tier says what a source can anchor, not how good it is.

Neither is forced, so the question goes to the owner (below).

**Coverage residue noted, not decided.** The three-part test does not name `standard_eb` at national scope (T2, a DPO or professional-body evidence-based standard) or `co2` (OT clinical practice guidelines). No ruled consequence attaches to their soundness today, so nothing is blocked. If the owner extends the consequence to every tier, these two need a route.

**What would change this resolution:** the owner saying the test is for Co-1 only and that "ISO for T4-6" was a separate remark. The definition would then have a Co-1 home, and T4 to T6 would rest on OR-23b alone. Under that answer the 2026-11-06 government-report ruling would need its own test.

---

## What follows for T-059, T-110 and a later Co-1 soundness task

**T-059 (agreement, steps 1, 2 and 4).** No change to its scope. Step 3 stays held until the soundness verdict exists. One ordering is forced by logic and should be stated in its pull request:

- OR-5 applies before OR-4 and OR-6c. A Co-1 figure without a soundness verdict of "sound" is out of the numeric bound, so it can never be "the higher rank stating the value" against T2.
- Read otherwise, OR-6c would let a Co-1 figure set the number that OR-5 says it may not. Reading OR-6c as being about Co-1 figures that may set a value keeps both rulings true.
- This upgrades the 2026-10-29 [ASSUMPTION] ("OR-5 applies first") from assumption to entailment. The [ASSUMPTION] text in the ledger is not edited.

**T-110 (first determinations).** Its stop holds: a cell whose selected bound is set by a Co-1 figure is not written until that source carries a verdict. No other cell changes. Cells set by T1 or T2 figures are unaffected, unless the owner chooses option B of question Q1 below.

**What is derivable (no new field):**

- **The route** (which leg of the test applies) follows from fields already held:
  - `evidence_type = 'sr_meta'` takes PRISMA;
  - `standard_eb` with scope `international`, `national_fw` and `code` (T4 to T6) take the instrument test;
  - `co1`, `clinical` and `grey` take the study test, or "reports no study".
  - Compute it from `(evidence_type, scope)` the way `derive_tier` does. Never keep it as a list beside the ladder.
- **T4 to T6 soundness** follows from `standard_number`, `jurisdiction`, `code_currency_status` and the clause locator.

**What needs a field, and why it is unavoidable.** Whether a study reports its method to the standard of its design, and whether a source reports a study at all, cannot be derived:

- `source_type` is NULL on two of the four Co-1 rows (`select ref_id from evidence_sources where evidence_type='co1' and source_type is null`).
- Neither a DOI nor a journal name shows peer review (R5 enforcer text).
- `co1_source_type` sorts by producer, not by method.

Without a recorded verdict, one of two wrong things reaches the guidebook. A Co-1 number with no reported method behind it is printed as the determination's value, or a Co-1 figure produced through a sound co-produced study is held to direction. In either case no reader can see why. Per CLAUDE.md §3 the fact belongs to the **judgment** stage ("whether it is sound"), not to `evidence_sources` (the evidence stage). Per the 2026-11-06 schema-shape statement it takes one value per cell. The smallest shape is one judgment table keyed on `ref_id`:

- `verdict`, with a CHECK of three values: `sound`, `not_sound` and `reports_no_study`. The third keeps the DPO case legible and separate from failure.
- `reporting_guideline`, the guideline the verdict was measured against, in a column of its own and never as a prefix in the warrant. It is NULL for `reports_no_study` and T4 to T6.
- `warrant`, the finding, quoting or locating the report's method sections.
- `judged_by_session` and the date.

One row per judgment, not a column on the source, so that a dissenting adversarial verdict lands as a second row and divergence reads as a contest. This follows the precedent CLAUDE.md §4 records for `add-population-match`. The vocabulary of `reporting_guideline` should come from the column's own CHECK, or be minted as base rows when first used. It is never a list in code (rule 8). The verb asks for the verdict, constrained to the CHECK, and refuses `sound` without a guideline and a warrant. The engine (`compose_value`) reads `verdict = 'sound'` (latest row, no unresolved dissent) to let a Co-1 figure into the numeric bound.

**The first executable task:**

1. **Tooling pull request.** Add the table, the verb, and `compose_value`'s read of it. This is T-059's held step 3, rewritten from "drop every Co-1 row" to "drop Co-1 rows whose source lacks a `sound` verdict".
   - Test: a Co-1 figure without a verdict is excluded from the bound and still governs the direction.
   - Test: a `sound` row lets it set the bound.
   - Test: `reports_no_study` renders differently from `not_sound`.
   - Probes chosen by query, never by typed ref_id.
2. **Then a judgment-stage research pull request.** It judges the held Co-1 sources one at a time and reads, for each:
   - the persisted retrieval payload (`retrieval_log`);
   - `co1_provenance`;
   - the report's methods section;
   - the EQUATOR guideline for its design.

   A session below the Opus floor proposes; the warrant is written for adversarial review.

## Where the owner is still needed

- **Q1 (edge 3, doctrine).** Should soundness also decide whether a T1 clinical, T2 or Co-2 figure sets the number?
  - **A: No.** Soundness controls a figure only where a ruling attaches a consequence (Co-1 under OR-5, grey reports at T3, T4 to T6 under OR-23b), and the tier and scope remain the method gate elsewhere. No doctrine change. This is the default if unanswered, because it changes nothing already ruled.
  - **B: Yes, at every tier.** A figure whose report fails its design's guideline sets the direction only, whatever its tier. This amends `governance/tier-system.md` line 11 and requires a route for `standard_eb` national and `co2`.
- **Confirmations, not open questions, of the two [ASSUMPTION]s in the tenth set:**
  - "PRISM" is PRISMA.
  - "ISO for T4-6" is the instrument as its own test. Edge 3 above holds under either reading of that clause.
- **Peer review, only if the owner disagrees with edge 1.** Is peer review necessary for a study to be academically sound (which would narrow the 2026-11-06 government-report ruling to refereed reports), or is it one sign of rigour among others (this resolution)? The resolution stands unless the owner says otherwise.
