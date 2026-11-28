# Rulings on the evidence stage, the judgment stage, and how groups attach — a collation

Collated 2026-11-28 in `session_2026-11-28-param-13-rise-landings`, by reading the repository only (no web, no DB
writes). **This is a collation, not a plan and not a ruling.** Nothing here decides anything.

How to read it:

- **Line numbers** come from `git grep -n` at the time of writing. The ledger is append-only, so they should hold, but
  re-check with `git grep -n -F "<first words of the quote>" references/project-standards.md`.
- **Who said it** uses five labels:
  - **OWNER TYPED**: words the ledger records as the owner's own typing.
  - **OWNER SELECTED A LABELLED OPTION**: the owner picked from a menu; the words are the option's label, not the owner's.
  - **OWNER RATIFIED A DRAFTED DEFAULT**: the 2026-11-19 "Sure, append. Ratify all." covered resolutions an adjudicator
    drafted. The ledger gives some of them status ANSWERED BY THE OWNER, but the words are the adjudicator's.
  - **DELEGATED RESOLUTION, not the owner's**: the ledger itself says "not an owner statement".
  - **DR RATIONALE / RECORD**: a recorder's or session's reasoning, or a decision record's text.
- **Bears on**: (a) what evidence is and may refuse or require; (b) what judgment is, does and decides; (c) how groups
  (identity, ICF, access need) attach to figures and parameters, including parameter domains and categories.
- **The quote column is verbatim.** Ellipses inside a quote are the ledger's own unless marked `[…]`. A recorder's
  reading is never put in the quote column.
- **`.ignore` caveat**: `sessions/`, `_archived/`, `audits/` and `versions/` were searched with `git grep` (for
  example `git grep -n -i -E 'domains? (should|must) be automatically|automatically relate parameters' -- sessions
  _archived audits versions`, which returned nothing). The transcripts under `transcripts/` were **not** read line by
  line; every owner quote below is taken from the ledger or a decision record that quotes it. Owner words that live only
  in a transcript and were never put into the ledger are therefore **[UNVERIFIED] as absent**.

---

## 1. Chronological table

| # | Date | Source (file:line) | Verbatim quote | Who | Bears on |
|---|---|---|---|---|---|
| 1 | undated (project baseline) | references/project-standards.md:14 | "RULE: Design Modes governs all specifications. Universal Mode = Universal Design / Code Compliance (population-agnostic, fixed values). Population Mode = Population-Informed Inclusive Design (ranges; median as default). Person Mode = Person-Specific Co-Design (OT assessment resolves position within the Population-Mode range). DAR mandatory at all modes." | DR RATIONALE / RECORD (a RULE line; its author is not stated on the line) | (b) scope |
| 2 | 2026-08-24 | decisions/DR-2026-08-24-scaffolding-is-phase-specific.md:285-294 | "### §2.4 Applicability is an OUTPUT of synthesis, never an input to it" … "Every research slug gets cross-referenced against a population code, access need or ICF code because there is always the chance that there is an unexpected connection between them. If we only link our taxonomy to research slugs by what seems obvious, we may miss evidence." … "we are waiting until we have finished our syntheses to ensure we define them with evidenced justification, not presuppositions." | The heading is the DR's. The two inner quotes are recorded in the DR as the owner's words (OWNER TYPED, as quoted by the DR). The DR is "RATIFIED BY MERGE". | (b)(c); **overruled as to the stage by row 10** |
| 3 | 2026-08-25 | references/project-standards.md:1185 | "As to 'mobility', separate out into 'ambulatory' and 'wheelchair user' to start." | OWNER TYPED (recorded "not to be relitigated") | (c) |
| 4 | 2026-08-26 | references/project-standards.md:1317-1319 | "RULE: The judgment object is the **canonical parameter**, and `items` is the render rollup the entity model already calls it. Owner ruling 2026-08-26, selecting "key on the canonical parameter" from the options put" | OWNER SELECTED A LABELLED OPTION ("key on the canonical parameter"); the RULE wording is the recorder's | (b)(c) |
| 5 | 2026-08-27 | references/project-standards.md:1454-1455 | "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications." | OWNER TYPED | (a)(b) |
| 6 | 2026-08-27 | references/project-standards.md:1467-1468 (the recorder's table of the owner's spine) | "\| 2 \| `evidence-collection` \| research-items \| **evidence-items** — "the paper says 1200 mm" \|" / "\| 3 \| `judgment` \| evidence-items \| **judgment-items** — whether that extraction is sound, and how it weighs \|" | DR RATIONALE / RECORD (the recorder's table, which CLAUDE.md §3 descends from) | (a)(b) |
| 7 | 2026-08-27 | references/project-standards.md:1845 | "one evidence source may provide many rows of judgment (eg a code document like Canada's NBC 3.8)" | OWNER TYPED | (a)(b) |
| 8 | 2026-08-27 | references/project-standards.md:1883-1886 | Evidence: "logs all relevant items found in search with a unique reference ID, DOI/PMID and other codes if available, type of source (academic, code, professional practices, etc)" Judgment: "delivers a verdict on an evidence item for what tier of evidence hierarchy it belongs to (1, 2…6)" · "determines category of judgment item, **derives value/process/figure/goal for it**" | OWNER TYPED (the owner's architecture note, adopted as ruling; the bold is the recorder's) | (a)(b) |
| 9 | 2026-08-27 | references/project-standards.md:1894-1895 | "**`source_value_extractions` is a JUDGMENT table, not an evidence-collection table.** The value is derived at judgment; collection logs what was found." | DR RATIONALE / RECORD (consequence of row 8; D-0168) | (a)(b) |
| 10 | 2026-08-27 | references/project-standards.md:2002-2007 | "overrule Aug 24 DR. we go evidence>judgment>synthesis." / "evidence is probably working by doing more cursory scans and grep/regex or whatever rather than line by line analysis, so it's probably just getting all required metadata for apa standards and listing out all concepts/topics/key words/phrases that appear in the source and then judgment phase will actually do the deep read on it to determine what can be derived from the source" | OWNER TYPED | (a)(b)(c) |
| 11 | 2026-08-27 | references/project-standards.md:2041-2042 | "the crossing is **judgment's output**, so zero links after judgment IS a defect." | DR RATIONALE / RECORD (the recorder's ACTION drawn from row 10) | (b)(c) |
| 12 | 2026-08-27 | decisions/DR-2026-08-27-relevance-is-adjudicated-at-collection.md:17-18 (owner's source: references/owner-notes/2026-08-27-architecture-note.md:112) | "evidence states relevant items, and relevancy is something that must be adjudicated against a topic/category/concept." | OWNER TYPED (D-0174, decided by `jordanelias`) | (a)(b) |
| 13 | 2026-08-27 | decisions/DR-2026-08-27-relevance-is-adjudicated-at-collection.md:22-26 | "Relevance is not a property a document carries but a relation, so evidence collection judges -- it simply judges a different question from judgment. […] relevance must be settled at collection or nothing can be admitted." | DR RATIONALE / RECORD | (a) |
| 14 | 2026-08-27 | references/project-standards.md:1935-1936 | "yes we include the medical model too. we give our users the choice of what model they want to use to browse the site." | OWNER TYPED (D-0170); **medical half deleted by row 33** | (c) |
| 15 | 2026-08-28 | references/project-standards.md:2493-2495 | "we must have all of identity, icf, needs and medical grouped into same tables after the base phase, and we need to do it in an intelligent manner. if i understand things correctly, it really doesn't matter if we have loads of rows concerning the same source or concept" | OWNER TYPED | (c) |
| 16 | 2026-08-28 | references/project-standards.md:2542-2543 | "ACTION: Four lens columns, one CHECK, real FKs. Never a `population_*` link table. Never two lenses in one row. `population_code` is retired in favour of the four." | DR RATIONALE / RECORD (the recorder's ACTION; "four" cut to three by row 33; "never a link table" superseded by row 25) | (c) |
| 17 | 2026-09-01 | decisions/DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md:21-23 (also references/project-standards.md:2554-2556) | "it is OKAY for a link to be absent in a related taxonomy column", "but a link MUST be tied to at least one", "and ideally it ties into many" | OWNER TYPED (D-0182, decided by `jordanelias`) | (c) |
| 18 | 2026-09-01 | decisions/DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md:46-47 | "The ideally-many clause is an AUTHORING aim, not a constraint, and is deliberately not mechanised" | DR RATIONALE / RECORD | (c) |
| 19 | 2026-09-01 | decisions/DR-2026-09-01-the-lens-is-a-column-not-a-traversal.md (Rationale) | "TRAVERSAL MANUFACTURES INFERENCE AND CHANGES THE ANSWER" … "a render layer that crosses is adjudicating where nothing reviews it and no attestation covers it." | DR RATIONALE / RECORD (D-0184, decided by `session_2026-09-01-lens-architecture`, delegation DG-REVIEW; **not an owner ruling**) | (b)(c) |
| 20 | 2026-09-09 | references/project-standards.md:2690-2691 | "oh. you have to compute it. I can't handle this load manually. you need to repair this and anything else" | OWNER TYPED (about determinations in `specifications`) | (b) |
| 21 | 2026-10-21 | references/project-standards.md:4540 | "if we can't retrieve a study, then we can't verify it as a primary source, which means that we can't claim it as a top tier. add unverified in this context where something can't be retrieved to the empty circle alongside grey or thin" | OWNER TYPED | (a)(b) |
| 22 | 2026-10-29 | references/project-standards.md:4723 | "OR-22: "Something else — This is why we use backwards citation mining and contextual clues. If we are unable to find the actual parameters/values under discussion, then the source itself has no value. If we are able to find the actual parameters/values under discussion, then the absence of findings--i.e. the lack of prescribed change to that parameter/value--is simply a confirmation of the validity of those parameters/values."" | OWNER TYPED (free text under "Something else") | (a)(b) |
| 23 | 2026-10-29 | references/project-standards.md:4725 | "OR-23: "Confirm -- This applies only when the source is properly cited in an academic context, i.e. there is a valid academic route to the source."" | OWNER TYPED (beside a "Confirm" selection) | (a)(b) |
| 24 | 2026-11-06 | references/project-standards.md:4630 | "a figure reaches a determination only through the lens tags written on that figure, so D-0184 stands." … "no row is stored for a parameter and lens the parameter is not relevant to, and none for a lens that no figure carries." | DR RATIONALE / RECORD (OR-1, recorded as "Taken from the prompt's "yes""; the words are the recorder's) | (b)(c) |
| 25 | 2026-11-06 | references/project-standards.md:4926-4928 | "1. OR-1c: "link table unless that is more prone to errors"" / "2. The lens for a clause under a disability heading: "ALL is a generic? what do you even mean? ALL implies it is just good design, not that it is accessible design in particular as it doesn't map to a particular group. I guess we can see it as a universal?"" / "3. The type of a government report: "if government report is academically sound then it can be t3 I think"" | OWNER TYPED | (b)(c) scope |
| 26 | 2026-11-06 | references/project-standards.md:4963-4965 | "tables and columns must be as clearly organized as possible. we do NOT want to have data joined in cells that will cause issues further down the pipeline or have data stored in the wrong cell" / "more columns = more specificity = more flexibility imo" | OWNER TYPED | (c) shape |
| 27 | 2026-11-06 | references/project-standards.md:5182 | "none of the work in base needs to be verified and stored in evidence." | OWNER TYPED | (a) |
| 28 | 2026-11-12 | references/project-standards.md:6043-6044 | "**OD-31.** Selected: "Heading's group; ALL leaves the identity lens"." / "OD-31: a provision that names no one carries the group its heading names (under a mobility heading, the parent MOB with no child; under a general disability heading, no identity, only its ICF and access-need lenses); ALL leaves the identity lens, universal being stated once, by design_scale" | OWNER SELECTED A LABELLED OPTION (the gate line is the recorder's) | (b)(c) scope |
| 29 | 2026-11-12 | references/project-standards.md:6075-6076 | "Selected: "Yes, the 2026-11-06 ruling supersedes that clause"." / "OD-39: the 2026-11-06 link-table ruling supersedes the 2026-08-28 clause "Never a population_* link table"; T-018 appends the SUPERSEDES/BY pair and builds extraction_lens_links" | OWNER SELECTED A LABELLED OPTION | (c) |
| 30 | 2026-11-13 | references/project-standards.md:6255 | "**Q6.** "how do you handle different values for a parameter based upon different access needs/ICF codes/identities? or different design modes of universal vs population vs person specific?"" | OWNER TYPED, **a question, not a ruling** (the ledger: "not owner answers") | (b)(c) scope |
| 31 | 2026-11-14 | references/project-standards.md:7443-7445 | "just ignore the 2% and convergence because it doesn't matter enough. you can just choose colour placeholders. these aren't real decisions that you're asking of me aside from task assigning lenses to code values by context" / "that should be done in evidence stage" | OWNER TYPED | (a)(b)(c) |
| 32 | 2026-11-14 | references/project-standards.md:7466, 7482, 7498, 7512, 7526, 7540 | "at the moment of recording the row is when you will have best idea of context" / "typically anything to do concerning mounting height will concern wheelchair users" / "same with clearance height" / "or clearance" / "yes lens in judgment" / "but ICF and access needs are supposed to be mapped to populations too so populations still get coded as a result" | OWNER TYPED (six messages) | (b)(c) |
| 33 | 2026-11-14 | references/project-standards.md:7403 | "3 all code values will have a lens even if it's not explicitly stated. use contextual judgment" | OWNER TYPED (OD-65, status ANSWERED BY THE OWNER at 7427-7428) | (b)(c) |
| 34 | 2026-11-14 | references/project-standards.md:7005, 7053, 7159 | "what are grey or thin or unverified sources? let's return to keeping them but they get a triangle warning" / "no, triangle instead if the value is coming from grey or unverified" / "because if it mixes then it's a new value proposed for something so it's conjecture because we don't have authority" | OWNER TYPED | (a)(b) |
| 35 | 2026-11-15 | references/project-standards.md:7567 | "ACTION: (1) The lens of a code value is judged and written at recording; the maps propose." | DR RATIONALE / RECORD (the ledger: "correction and registration, not an owner statement") | (b)(c) |
| 36 | 2026-11-16 | references/project-standards.md:7692 | "delete medical taxonomy , medical maps and medical codes btw" | OWNER TYPED | (c) |
| 37 | 2026-11-17 | references/project-standards.md:7738-7740 | "od69 like the overall class of a parameter eg circulation for all the ones that deal with ramps and stairs and corridors and doors etc. the project is supposed to be like that" / "od70 yes" | OWNER TYPED ("od70 yes" answers "type and scope judged, tier computed") | (b)(c) domains |
| 38 | 2026-11-18 | references/project-standards.md:7778-7784 | "then the base grounds itself except for when evidence that allows for new terms/aliases/parameters to be found is pointed to as justification" / "but this justification should then be absorbed by base and grounded as if it were always there to prevent loops/recursion/sequencing conflicts" / "ref_id as provenance? sure. but it's ONLY for provenance" | OWNER TYPED | (a)(c) |
| 39 | 2026-11-18 | references/project-standards.md:7842 | "list of topic areas is not fixed" | OWNER TYPED (OD-69) | (c) domains |
| 40 | 2026-11-19 | references/project-standards.md:7969-7975, 7989, 7992, 7995, 8015 | "Sure, append. Ratify all." … "OD-46: admit as declared, scoped-out codes (the adjudication's recommended default, ratified)" / "OD-47: the document's stated audience judged per item by context, the audience words quoted (the adjudication's recommended default, ratified)" / "OD-48: whom it is for (the adjudication's recommended default, ratified)" / "OD-69: a concept's topic area; the list is not fixed; held as rows extended by data with a warrant" | "Sure, append. Ratify all." is OWNER TYPED. OD-46, OD-47, OD-48 are OWNER RATIFIED A DRAFTED DEFAULT (status ANSWERED BY THE OWNER). OD-69 is a DELEGATED RESOLUTION confirmed by that ratification (status RESOLVED UNDER DELEGATION, CHECK confirmed). | (a) admission; (b)(c) scope, domains |
| 41 | 2026-11-20 | references/project-standards.md:8124-8138 | "i don't want to have to constantly map and cross-reference disability identities vs access needs vs ICF codes, so the base needs to get that ready for me too" / "this project will die upon itself if it doesn't treat disability identities properly. they are going to be by far the most common lens upon which people will navigate the repository" / "yes, translation runs before judgment" | OWNER TYPED | (a)(b)(c) |
| 42 | 2026-11-20 | references/project-standards.md:8158-8160 | "you basically need to have a big 3D matrix of ICF codes * access needs * disability identities" / "yes, correct" | OWNER TYPED ("yes, correct" confirms a description written by the coordinator) | (c) |
| 43 | 2026-11-20 | references/project-standards.md:8246 | "T-145: should be all three. We need to do the identity-ICF-access matrix." | OWNER TYPED | (c) |
| 44 | 2026-11-21 | references/project-standards.md:8290, 8308, 8366 | "3 to umbrella and to specific, yes" / "1 yes b is seeing therefore ties into blind etc" / "Yes, they count as identity's ICF coverage." | OWNER TYPED | (c) |
| 45 | 2026-11-22/23 | references/project-standards.md:8411-8421 | "our project filters specifications based on three approaches, and the browsing user chooses one of those approaches to use for browsing" … "So we should have a list of access needs, we should have a list of disability identities, and we should be able to map them to one another" / "and from there, perhaps, we select ICF codes that pertain to those relationships" / "Okay. Opus to reconcile, make rulings as required and allow us to keep moving forward in project" | OWNER TYPED | (c) |
| 46 | 2026-11-26 | references/project-standards.md:8654 | "Co-2 is co-primary with tier 2." | OWNER TYPED | (b) |
| 47 | 2026-11-27 | references/project-standards.md:8726-8755 | "**OD-91 (Q4, the first cell and the order of work): a test picks the first cell, after T-102 and the T-127 slice have run.**" … "[ASSUMPTION: neither ramp cell may therefore be keyed on MOB.]" | DELEGATED RESOLUTION, not the owner's (RESOLVED UNDER DELEGATION; ledger 9066: "not an owner statement") | (b)(c) |
| 48 | 2026-11-27 | references/project-standards.md:8758-8768 | "OD-92 (Q-B2: several stating sources carry different markers)." … "Meanwhile: the engine refuses the cell and names this question." | DELEGATED RESOLUTION, not the owner's; **REFERRED BACK TO THE OWNER**, open | (b) |
| 49 | 2026-11-27 | references/project-standards.md:8831-8832 | "**OD-98 (Q3b): `rests_on_proxy_inference` is not, by itself, a thin cause.**" / "A value is thin under the project-inference cause only when no source in the lens states it." | DELEGATED RESOLUTION, not the owner's (RESOLVED UNDER DELEGATION) | (b)(c) |
| 50 | 2026-11-27 | references/project-standards.md:8839-8861 | "**Question 1.** A source that was retrieved and logged but is stored UNVERIFIED, its identity or edition unconfirmed: when it states the shown value, does the value carry ⚠ or its tier's circle?" … "**Question 2.** How does the record show "could not be retrieved"?" | DELEGATED RESOLUTION, not the owner's; OD-99 **REFERRED BACK TO THE OWNER**, open | (a)(b) |
| 51 | 2026-11-27 | references/project-standards.md:8864-8876 | "**Question.** May such a source govern a value, marked ⚠?" … "**Meanwhile:** (a), which is reversible." | DELEGATED RESOLUTION, not the owner's; OD-100 **REFERRED BACK TO THE OWNER**, open | (a)(b) |
| 52 | 2026-11-27 | references/project-standards.md:8879 | "**OD-101 (the eligibility union): an unverified Co-1 source is eligible to govern on the same terms as an unverified T1 source.**" | DELEGATED RESOLUTION, not the owner's (RESOLVED UNDER DELEGATION) | (b) |
| 53 | 2026-11-28 | references/project-standards.md:9069-9071 | "start doing our research across languages and jurisdictions" / "whatever doesn't work in a session just gets fixed by hand logically within context of project then recorded as a tooling issue to resolve" / "solving by hand is also a clue for how to solve a tooling problem" | OWNER TYPED | (a) process |
| 54 | 2026-11-28 | references/project-standards.md:9076-9077 | "TERM-090 could work" / "Asked which to record, the owner selected "(b) Mint a per-flight rise term" (the option stating a term for the rise of a single flight between landings, distinct from TERM-090's total rise)." | First sentence OWNER TYPED (the ledger: "tentative"). The rest is OWNER SELECTED A LABELLED OPTION (correction at 9081: "not typed words"). | (b) parameters |
| 55 | 2026-11-28 | references/project-standards.md:9085-9086 | "Please log all instances of refusals and denials." / "Please log all instances of hand editing, ie overriding tools." | OWNER TYPED | (a) process |
| 56 | 2026-11-28 | references/project-standards.md:9091 | "ramps do not specifically need to state populations. ramps as ramps are circulation related, which means that they would automatically key on to all identities/ICF/access needs that are concerned with mobility and circulation" | OWNER TYPED | (a)(b)(c) |
| 57 | 2026-11-28 | references/project-standards.md:9092 | "this is why we have categories for parameters too: so that we can automatically relate parameters to their needs" | OWNER TYPED | (c) |
| 58 | 2026-11-28 | references/project-standards.md:9093 | "it's why judgment needs to be performed upon logged evidence, and evidence shouldn't be getting refused because it doesn't have a classification yet because there's another phase that can do that in supplement" | OWNER TYPED | (a)(b) |
| 59 | 2026-11-28 | references/project-standards.md:9094 | "Domains should be automatically connected identities/ICF/needs." | OWNER TYPED | (c) |
| 60 | 2026-11-28 | references/project-standards.md:9095 | "This is a mission critical requirement as it appears that it will have huge impacts upon recording research and preventing refusals" | OWNER TYPED | (a) |
| 61 | 2026-11-28 | references/project-standards.md:9096 | "If evidence is not able to log the domain by itself when recording information, then it still needs to be approved so that the judgment phase can properly assign the domain and consequently the relevant groups" | OWNER TYPED | (a)(b)(c) |
| 62 | 2026-11-28 | references/project-standards.md:9097 | "TOUCHES (rule 0, not yet changed in code): the `add-extraction` refusal "an extraction must be stated in at least one lens (D-0182)", which turns away a figure with no lens, and the absence of any link from a parameter's domain (`terms.domain`) to identities, ICF codes and access needs. D-0182's cardinality rule is read as governing the judged link, not the logging of evidence; whether that reading stands is the owner's." | DR RATIONALE / RECORD (the recorder's) | (a)(c) |
| 63 | 2026-11-28 | references/project-standards.md:9102 | "Universal/Population Specific/Individual relates to Identity/ICF/Access Needs relates to accessible design domains under which parameters are categorized" | OWNER TYPED | (b)(c) scope |
| 64 | 2026-11-28 | references/project-standards.md:9107 | "Where evidence is unable to determine for itself, the judgment phase will adjudicate the missing domains/values/relationships/etc and thereby determine admissible" | OWNER TYPED (marked mission critical, 9115) | (a)(b) |
| 65 | 2026-11-28 | references/project-standards.md:9112 | "Evidence is the recording of our research, and Judgment is the vetting of it to show saliency" | OWNER TYPED (marked mission critical, 9115) | (a)(b) |
| 66 | 2026-11-28 | references/project-standards.md:9115 | "Follow-up to the sixth statement, same day: "Again, mission critical". Both the fifth and sixth statements are marked mission critical by the owner, in addition to the third entry's statement of the same day." | The inner "Again, mission critical" is OWNER TYPED; the sentence around it is the recorder's | (a)(b) |

Rulings outside the ledger that the brief names, and where they stand:

- **CLAUDE.md §3** (CLAUDE.md:256-257): "| **evidence** | What was admitted, its identity and its verification |" / "| **judgment** | What each source asserts for each parameter (the extraction), whether it is sound, and how it weighs |". This is Layer 0 prose that carries rows 5, 6, 8 and 9. It is not itself an owner statement.
- **CLAUDE.md §6** (CLAUDE.md:377-381): "**The crossing is JUDGMENT's output** (owner, 2026-08-27, overruling `DR-2026-08-24` §2.4): harvest concepts at evidence (`db.py observe-term`, verbatim and unjudged), adjudicate at judgment. Zero links **after judgment** is a defect." CLAUDE.md:383-401 carries rows 4, 15-17 and 36 and the "lens" and "subject" halves of the key.
- **governance/pipeline-contract.yaml**. Evidence stage entry, governance/pipeline-contract.yaml:137-138: "sources discovered for the topic/slug under research". Judgment stage, governance/pipeline-contract.yaml:184-187: "anchor: the 4-state determination machine + convergence + directness (evidence-architecture.md §5)" and "entry: - an admitted evidence source, ready for value extraction and a tier verdict". The judgment criterion `judgment-code-value-identity-not-omitted` (governance/pipeline-contract.yaml:254-265) requires a live tier 4-6 figure to carry a live identity, ICF or need link. The header says `ratified: false` (governance/pipeline-contract.yaml:3), and the corrected contract was ratified as OD-17 under row 40.

---

## 2. What the owner's own words settle

Only rows labelled OWNER TYPED or OWNER SELECTED are used. Where a proposition needs a recorder's reading to stand,
that is said.

1. **The judgment object is the parameter.** A determination is keyed on the design parameter, not on an item and not on
   a slug × population pair. (Row 4, a selected option. CLAUDE.md:390-393 carries it.)
2. **Stage order, and the two stage verbs.** Evidence comes before judgment ("evidence research, judge evidence"; "we go
   evidence>judgment>synthesis"). On 2026-11-28 the owner defined them: "Evidence is the recording of our research, and
   Judgment is the vetting of it to show saliency." Both the fifth and sixth statements are marked mission critical.
   (Rows 5, 10, 65, 66.)
3. **One source yields many judgment rows.** (Row 7.)
4. **What evidence does (2026-08-27).** Evidence logs the source and its identifiers and type, does cursory scans, and
   lists every concept, topic, key word and phrase. Judgment "will actually do the deep read" and "derives
   value/process/figure/goal". (Rows 8, 10.)
5. **Judgment gives the tier verdict, and the tier is computed.** Judgment "delivers a verdict on an evidence item for
   what tier of evidence hierarchy it belongs to". "od70 yes" answers "type and scope judged, tier computed".
   Determinations are computed ("you have to compute it"). (Rows 8, 20, 37.)
6. **Relevance is an adjudication made at evidence (2026-08-27).** "evidence states relevant items, and relevancy is
   something that must be adjudicated against a topic/category/concept." (Row 12, D-0174, owner.) How this sits with
   proposition 7 is open (§3, conflict C3).
7. **Evidence is not refused for want of a classification (2026-11-28).** Judgment supplies what evidence cannot
   determine: "the missing domains/values/relationships/etc". In doing so, judgment "thereby determine[s] admissible".
   Evidence that cannot log its own domain "still needs to be approved so that the judgment phase can properly assign
   the domain and consequently the relevant groups". All three statements are marked mission critical.
   (Rows 58, 60, 61, 64, 66.)
8. **Domains connect parameters to groups automatically.** "Domains should be automatically connected
   identities/ICF/needs." "this is why we have categories for parameters too: so that we can automatically relate
   parameters to their needs." The worked case is ramps: "circulation related", keying "on to all identities/ICF/access
   needs that are concerned with mobility and circulation", and "ramps do not specifically need to state populations".
   (Rows 56, 57, 59.)
9. **A category is the overall class of a parameter, and the list is not fixed.** "like the overall class of a parameter
   eg circulation for all the ones that deal with ramps and stairs and corridors and doors etc." "list of topic areas
   is not fixed". (Rows 37, 39.) Holding the list "as rows extended by data with a warrant" is a delegated resolution
   that the owner's "Ratify all" covered, not the owner's words. (Row 40.)
10. **The scope chain.** "Universal/Population Specific/Individual relates to Identity/ICF/Access Needs relates to
    accessible design domains under which parameters are categorized." The owner's words do not say which scope pairs
    with which lens. (Row 63.)
11. **There are three lenses: identity, ICF, access need.** The medical lens is deleted (rows 14, 36). Within the
    three, a link "MUST be tied to at least one" and "ideally it ties into many" (row 17). Many rows per source or concept
    are fine (row 15). Several codes on one figure are carried by a link table (rows 25 and 29: OR-1c typed, OD-39
    selected). Disability identity is the lens "by far the most common" for navigation (row 41). A browsing user picks one
    of the three approaches (row 45).
12. **Code values always carry a lens, assigned by contextual judgment at the moment of recording, and the lens is in
    judgment.** "all code values will have a lens even if it's not explicitly stated. use contextual judgment"; "at the
    moment of recording the row is when you will have best idea of context"; "yes lens in judgment". Defaults: mounting
    height, clearance height and any clearance go to wheelchair users (stated as "typically"). ICF and access-need
    lenses also reach populations ("populations still get coded as a result"). (Rows 31-33.) The words name *code
    values*. Whether the 2026-11-28 domain route (proposition 8) replaces this or adds to it is open (§3, C5).
13. **ALL is not an accessible-design group.** "ALL implies it is just good design, not that it is accessible design in
    particular" (row 25, typed but hedged with "I guess"). "Heading's group; ALL leaves the identity lens" (row 28,
    selected option). The meaning of `design_scale = universal` ("whom it is for", OD-48) is a ratified drafted default,
    not the owner's words (row 40).
14. **The identity × need × ICF matrix.** A row holds all three keys ("should be all three"). The owner reviews each
    batch. A need may be keyed on an umbrella identity and on its members. An identity may take a b-code (only b210 to
    blind is stated). Need-side environmental rows count as an identity's ICF coverage. Pairing identity and need first,
    then choosing ICF codes, is prefaced "perhaps". (Rows 42-45.)
15. **Mobility is split into ambulatory and wheelchair user "to start".** (Row 3.)
16. **Unretrievable, grey and unverified sources are kept, and their values take ⚠ in place of the circle. A value that
    mixes a finding with a project inference is conjecture, ⚠.** (Rows 21, 34.) An unretrievable source counts only with
    a valid academic route (row 23, typed beside "Confirm"). Whether a retrieved-but-UNVERIFIED source governs, and what
    marker it takes, is open: OD-99 and OD-100 are referred back.
17. **Translation runs before judgment.** (Row 41.)
18. **Base vocabulary is not admitted through evidence.** "none of the work in base needs to be verified and stored in
    evidence." Evidence that justified a base row is absorbed into the base, with `ref_id` kept "ONLY for provenance".
    (Rows 27, 38.)
19. **Hand fixes are allowed and recorded as tooling issues. Refusals, denials and hand edits are logged.** (Rows 53,
    55.)
20. **A per-flight rise term.** For GAP-070 the owner selected "(b) Mint a per-flight rise term". This was a selection,
    not typed words. (Row 54.)

---

## 3. Conflicts and open points

None is resolved here. "Who resolves" follows CLAUDE.md rule 0 (a live owner statement supersedes on contact) and §8
(doctrine, population taxonomy and evidence-tier definitions are the owner's). It also follows the 2026-11-27 reach of
the Opus grant: it does not reach "what the owner meant by the owner's own words, population-taxonomy structure" (8695).

**C1. D-0182's "a link MUST be tied to at least one" against "evidence shouldn't be getting refused because it doesn't
have a classification yet".**
- Rows: 17 against 58, 61, 64.
- The recorder already read D-0182 as governing "the judged link, not the logging of evidence" and left it to the owner
  (row 62).
- Reading A, D-0182 governs every extraction at recording (the tools today):
  - `add-extraction` keeps refusing a figure with no lens (scripts/db.py:12133-12137).
  - A research figure whose own words name no group cannot be recorded at all (C2).
  - The owner's 2026-11-28 words are not met.
- Reading B, D-0182 governs the judged link and the determination only:
  - `add-extraction` accepts a figure with no lens.
  - Something marks the figure as awaiting judgment (the proposal in GAP-388).
  - The lens CHECK on `specifications` (`COALESCE(identity_code, icf_code, needs_code) IS NOT NULL`) and
    `schemas/evidence_state.py:203-223` are untouched.
  - `assess_cell._lens_clause` already ignores a figure that has no live link, so such a figure reaches no cell until
    judged.
- Who resolves: the owner (the meaning of the owner's own D-0182 words, and a lens rule).

**C2. The `context` lens basis is limited to tier 4-6, which makes a research figure that names no group
unrecordable.**
- Rows: 33 ("all code values") against 56 and 58 (ramps need not state populations; no refusal for want of a
  classification).
- `_require_lens_warrant` refuses basis `context` unless the source is tier ≥ `dbcore.REGULATORY_FROM_TIER`
  (scripts/db.py:11752-11759). It gives the reason that the owner "moved the contextual assignment … for code values
  only".
- A T1-T3 figure therefore needs its group in its own words, its heading or its study's participants, or it cannot be
  written at all.
- Reading A (rows 31-33 confine contextual assignment to codes): the refusal stands, and research figures without named
  groups are lost at recording.
- Reading B (rows 56-61 generalise it through the domain): the tier limit goes or is bypassed by a no-lens path.
- Who resolves: the owner.

**C3. D-0174 "relevancy … must be adjudicated" at evidence against "Judgment is the vetting of it to show saliency" and
judgment determining "admissible".**
- Rows: 12, 13 against 64, 65.
- D-0174's rationale says "relevance must be settled at collection or nothing can be admitted" (row 13). The
  2026-11-28 statements place the finding of admissibility in judgment.
- "Relevance" (against a topic, at collection) and "saliency" or "admissible" (at judgment) may name different acts.
  The ledger's READING under the fifth statement says "this statement may move part of admission; whether it does is
  the owner's to say" (9108).
- Reading A, both stand as different acts: evidence keeps admitting a source as relevant to a topic, and judgment
  decides whether each figure is admissible for a determination. The tools would need an admissibility outcome at
  judgment, which does not exist as a column today [UNVERIFIED: no column was searched for by that name].
- Reading B, the 2026-11-28 words supersede D-0174's "must be settled at collection": admission becomes recording, and
  admissibility moves wholly to judgment.
- Who resolves: the owner.

**C4. CLAUDE.md §3's table against "Evidence is the recording of our research, and Judgment is the vetting of it to show
saliency".**
- Rows: CLAUDE.md:256-257 against 65.
- "What was admitted, its identity and its verification" puts admission at evidence. "Whether it is sound, and how it
  weighs" does not name saliency, domain assignment or admissibility.
- By rule 0 the live statement supersedes CLAUDE.md, which "is what to correct". The ledger's READING says whether
  the table is amended "is the owner's to say" (9113).
- What it would require: a one-line CLAUDE.md edit in a governance pull request, and the same in
  `governance/pipeline-contract.yaml`'s judgment `entry:` ("an admitted evidence source", line 187).
- Who resolves: the owner confirms the wording. The edit itself is the coordinator's under rule 0.

**C5. "the lens is assigned at recording by contextual judgment" (2026-11-14) against "groups follow from the domain,
assigned at judgment" (2026-11-28).**
- Rows: 31-33 and 35 against 56, 59, 61.
- The first set has the recording session judge and write each code value's lens with a warrant. The second has
  groups derived from the parameter's domain, with judgment assigning the domain "and consequently the relevant groups".
- The two may combine (a figure carries its own judged lens where it has one, and inherits the domain's groups where it
  has none), or the second may replace the first.
- Reading "combine": the tools need a domain-to-groups mapping and a rule for when an inherited group and a judged
  group differ.
- Reading "replace": the `context` basis and its warrant columns (`basis_reason`) would fall idle for code values.
- Who resolves: the owner.

**C6. D-0184 and OR-1 ("a figure reaches a determination only through the lens tags written on that figure"; "none for
a lens that no figure carries") against domain-derived groups.**
- Rows: 19, 24, 35 against 56, 59.
- D-0184 (a session decision, DG-REVIEW) rejected crossing at render because "TRAVERSAL MANUFACTURES INFERENCE". A
  group derived from a domain at read time would be such a traversal.
- If instead the derived groups are written onto each figure as judged links, they are tags on the figure, and D-0184
  and OR-1 hold.
- Reading A, the domain is a source of proposals: the derivation writes links with a warrant, and the engine is
  unchanged.
- Reading B, the domain is a read-time join: `assess_cell._lens_clause` would have to admit figures without links, and
  D-0184 and OR-1 would be superseded.
- Who resolves: the owner (D-0184 is not an owner ruling, but OR-1 rests on the owner's "yes").

**C7. No mapping exists from a domain to identities, ICF codes or needs, and its content is doctrine.**
- Rows: 57, 59.
- No table or view links `terms.domain` to a lens (§4). `terms.domain` is free text with no CHECK.
- The ledger says the mapping "is not written here: it is doctrine for the owner or an adjudication with a warrant"
  (9098).
- The list of domains is open (row 39). The adjudicated form, "rows extended by data with a warrant" (row 40, OD-69),
  has no table yet. T-135 was held.
- Who resolves: the owner for the content (population taxonomy is §8 doctrine). An adjudication may propose it.

**C8. The scope chain against how the engine sets `design_scale`.**
- Rows: 1, 28, 40 (OD-48), 63.
- The engine sets `design_scale = population if identity else universal` (scripts/assess/assess_cell.py:1413-1417).
  So a cell keyed on an ICF code or a need alone reads "universal", and `person` is never derived.
- Row 63 ties universal, population and individual to the lenses and domains without saying which pairs with which.
- Row 1's Design Modes and the 2026-07-12/13 G1(a) record ("T4–6-only determinations are Universal-Mode regulatory
  determinations", 6524) are the conflict OD-48 was referred for. OD-48 then took the drafted default "whom it is for".
- Who resolves: the owner, since row 63 may change OD-48.

**C9. The provisional MOB workaround against the MOB split and OD-91.**
- GAP-388 and this session's override O12 put lens MOB with basis `context` on every code row
  (`select description from gaps where gap_id='GAP-388'`;
  scratchpad/session_2026-11-28-param-13-rise-landings/overrides-refusals-denials.md:37).
- Row 3 splits MOB into ambulatory and wheelchair user "to start". OD-91's delegated assumption says "neither ramp cell
  may therefore be keyed on MOB" (row 47).
- OD-31 (row 28) allows "the parent MOB with no child" under a mobility heading, but O12's basis is `context`, not
  `heading`.
- Who resolves: no owner question. It is a workaround to retire when GAP-388 ships, and the coordinator should keep it
  flagged.

**C10. "evidence shouldn't be getting refused" against the evidence-stage refusals that are not classifications.**
- Rows: 58 against 21 and CLAUDE.md §5(c).
- `add-extraction` also refuses a source that is not VERIFIED (scripts/db.py:12068-12076), a figure with no covering
  `source_scans` row (12117-12122), and a quote not found in the saved bytes (12165-12178).
- The owner's words name "a classification", "the domain", and "domains/values/relationships". On their face they do
  not reach verification or the verbatim floor, which guard against fabricated citations (§5(c)).
- Whether "refused" covers these is open.
- Who resolves: the owner. Until then a reading that keeps them is the narrower one.

**C11. Stage of the extraction.**
- Row 9 (2026-08-27) makes `source_value_extractions` a judgment table, so `add-extraction` is a judgment-stage call
  (the ledger says so at 7528).
- The owner's 2026-11-28 words speak of "logged evidence" and "evidence … when recording information".
- If recording a figure is evidence's act, row 9's stage assignment moves. If it stays a judgment act, "evidence is
  not refused" refers to something upstream of the extraction (the source, its scan or its observed terms).
- Who resolves: the owner, since this is a stage assignment under row 5.

**C12. Pairing order in the matrix.**
- "should be all three" (row 43) against "perhaps, we select ICF codes" after pairing (row 45).
- OD-73 (a delegated resolution, 8586) kept all three and built no pairs table.
- Recorded here only because row 63's chain (lens → domain) may bear on it.
- Who resolves: the owner.

---

## 4. What the tools do today

All read from the working tree and from `data/guidebook.db` opened read-only. Schema version:
`python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma user_version').fetchone()[0])"`.

**`scripts/db.py insert_extraction` (`add-extraction`)**, in order of firing:

| file:line | refusal (verbatim, opening words) | ruling it cites |
|---|---|---|
| scripts/db.py:12068-12076 | "add-extraction: {ref} is {_vs or 'NULL'}, not VERIFIED. An extraction is a reading of a document this project obtained" | R10; D-0157 |
| scripts/db.py:12089-12093 | "--parameter-id is required: an extraction whose subject is unknown cannot reach the determination it exists to support" | owner 2026-08-26 |
| scripts/db.py:12117-12122 | "add-extraction: no source_scans row covers {ref} for parameter {pid}. Record the reading first" | R16, OR-11a |
| scripts/db.py:12123-12124 | `verified` needs a full-scope reading (`_require_full_scan_for_verified`, message at 11004-11008) | OR-11a |
| **scripts/db.py:12133-12137** | **"an extraction must be stated in at least one lens (D-0182): pass one or more of --identity / --icf / --needs. A value attached to no lens is a value about nobody."** | **D-0182** |
| scripts/db.py:12165-12178 | the verbatim floor: the quote must be in the saved bytes | CLAUDE.md 5(c) |
| scripts/db.py:12187-12190 | the lens warrant (`_require_lens_warrant`) and `_refuse_all_by_context` | OD-31, OD-65 |

**`_require_lens_warrant`** (scripts/db.py:11724-11798):

- Basis must be one of the column's CHECK values.
- A reason is allowed only with `context`.
- **Basis `context` is refused unless the source is tier ≥ `dbcore.REGULATORY_FROM_TIER`** (11752-11759): "basis
  `context` is for a code value (a source of tier 4 to 6); … a research figure's group comes from its own words
  (named_in_text, heading) or its study's participants."
- The warrant words must be found on word boundaries in the claim text, the heading, the study population or the saved
  file.

**`_refuse_all_by_context`** (scripts/db.py:11801-11807): refuses identity `ALL` with basis `context` (OD-31).

**`add-parameter` domain refusal** (scripts/db.py:7942-7966):

- Refuses a term whose `domain` is in `dbcore.NON_QUANTITY_DOMAINS` (scripts/dbcore.py:768). The members are
  `functional_axis`, `population`, `medical`, `methodology`, `legal` and `economics`.
- A NULL or blank domain passes (`dbcore.domain_key`, scripts/dbcore.py:771-775: "A NULL or blank domain is '' and is not
  in the rule").
- **No writer requires a domain.** `terms.domain` is a nullable TEXT with no CHECK.

**`scripts/assess/assess_cell.py`:**

- `_lens_clause` (260-280) raises `Refusal("a cell states at least one lens (D-0182); gathering without one would
  select evidence by parameter alone")`.
- A figure reaches a cell only through its live links in `v_live_lens_links` (D-0184, OR-1b). A figure with no link
  reaches no cell.
- `design_scale = SCALE_POPULATION if identity else SCALE_UNIVERSAL` (1413-1417, citing OD-48).
- RULE_VERSION `pilot-9` (127-131) refuses a cell whose shown value a non-VERIFIED source states, or whose stating
  sources' markers differ, "naming the open owner questions (OD-99, OD-100, OD-92)".

**`schemas/evidence_state.py`:** `EvidenceStateRecord.at_least_one_lens` (203-223) raises "A determination must be stated
in at least one lens: set one or more of identity_code / icf_code / needs_code (D-0182). A cell in no lens is a cell
about nobody." `design_scale` is validated against `ALL_SCALES` (187-191).

**Schema CHECKs** (read from `sqlite_master`):

- `extraction_lens_links`:
  - `CHECK ((identity_code IS NOT NULL) + (icf_code IS NOT NULL) + (needs_code IS NOT NULL) = 1)`, so each link row
    carries exactly one lens.
  - `basis IN ('named_in_text','heading','study_participants','context','carried')`.
  - `CHECK ((basis = 'context') = (basis_reason IS NOT NULL))`.
  - **No schema constraint requires an extraction to have any link.** "At least one lens per extraction" lives only in
    db.py:12133.
- `source_value_extractions`: its own retired lens columns carry `CHECK (COALESCE(identity_code, icf_code, needs_code) IS
  NULL)`. The lens lives only in `extraction_lens_links`.
- `specifications`:
  - `CHECK (COALESCE(identity_code, icf_code, needs_code) IS NOT NULL)` (D-0182).
  - `design_scale IN ('universal','population','person')`.
  - `parameter_id INTEGER NOT NULL REFERENCES base_parameters(parameter_id)`.
- `terms`: `domain TEXT` with no CHECK and no foreign key.

**Domain-to-lens link: none.**

- The objects in `sqlite_master` whose SQL mentions `domain` are `terms`, `conflicts` (`domain TEXT NOT NULL`, its own
  conflict-domain column), `term_aliases` (a relation-type value `'DOMAIN'`) and the view `v_item_provenance`.
  `v_item_provenance` shows `t.domain AS parameter_domain` beside the lens of an existing specification, and derives no
  group from the domain.
- No table carries both `domain` and a lens code.
- Re-run: `python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r for r in c.execute(\"select type,name from sqlite_master where sql like '%domain%'\")])"`.
- Domains in use: `select domain, count(*) from terms group by 1`.

**Gaps that carry this:**

- GAP-388 (P1, OPEN, "lens and domain at recording (owner, mission critical)") is readable in `data/guidebook.db`:
  `select description from gaps where gap_id='GAP-388'`. Whether it reached the canonical DB through a committed
  migration or through another path was not checked [UNVERIFIED].
- GAP-070 stays open (`select status from gaps where gap_id='GAP-070'`).

**Not checked** [UNVERIFIED]:

- `scripts/audit/code_value_identity_audit.py`'s exact predicate. Only its contract text (pipeline-contract.yaml:254-265)
  was read.
- Whether any skill (`run-pipeline`, `citation-miner` and others) instructs refusing a figure without a lens.
- Whether a column exists that records a judgment-stage admissibility outcome.
- The owner's words in `transcripts/` that never reached the ledger.
