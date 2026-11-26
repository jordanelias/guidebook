# project-standards.md — current-state extract, part 5 (source L4922–L6163)

Conventions used here: "Owner words" are verbatim. "[unratified reading]" marks a recorder's [ASSUMPTION]. "[OPEN]" marks an unanswered question. "[CHECK]" marks a sentence kept because it might be a rule or might be history, or where something outside this slice may bear on it. Where a later entry in this slice changes an earlier one, the earlier entry says so and the resulting state sits with the later date.

---

### 2026-11-06 — OR-1c link table; the identity lens ALL; the tier of a government report [L4922-L4941]
Owner words:
1. OR-1c: "link table unless that is more prone to errors"
2. Lens for a clause under a disability heading: "ALL is a generic? what do you even mean? ALL implies it is just good design, not that it is accessible design in particular as it doesn't map to a particular group. I guess we can see it as a universal?"
3. Type of a government report: "if government report is academically sound then it can be t3 I think"
The owner also asked that every fix be queued for a later session (recorder's paraphrase, not quoted).

In force:
- OR-1c: carry several codes of one model on a figure by a link table; do not write the figure once per combination. The orphan-link error is caught at apply time by `scripts/migrate_db.py`'s before-and-after `PRAGMA foreign_key_check`. The table's shape, and how the lens columns already on a figure are retired (writer, then reader, then NULL forward), belong to a tooling PR.
  - [unratified reading] the alternative's row multiplication settles the owner's condition "unless that is more prone to errors"; if the owner reads it otherwise, OR-1c reopens. Measuring command as given: `python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);m=dict(c.execute('select identity_code,count(*) from identity_icf_map group by 1'));r=c.execute('select identity_code,count(*) from source_value_extractions where identity_code is not null group by 1').fetchall();print(sum(n for i,n in r),sum(n*max(1,m.get(i,1)) for i,n in r))"`
  - Superseding effect on the 2026-08-28 clause "Never a population_* link table": see OD-39 (L6058-L6090).
- ALL: superseded within this slice by OD-31 (2026-11-12, L6039-L6055): ALL leaves the identity lens; "universal" is stated by `design_scale`. The interim ACTION (2) of this entry is overtaken. [CHECK] The entry's sentence "OR-1b is unchanged: a figure tagged ALL reaches only an ALL determination" is overtaken in effect by OD-31's removal of ALL as an identity.
- Which group a provision carries is judgment's output, filled through the link table; one figure may carry several groups.
- A `grey` government report that is academically sound may be tier 3; do not reclassify it to `clinical`. REF-00468, REF-01005 and REF-01008 stay as filed. Whether a given report is academically sound is judged per source.
  - [unratified reading] "t3" is tier 3; "academically sound" is the test OR-5 uses for a Co-1 source; the answer takes "stay `grey`, tier 3" and rejects reclassifying to `clinical` and a new route to tier 1.
- Treat every [ASSUMPTION] in the entry as unratified.

Open:
- [OPEN] `governance/tier-system.md`'s line listing `grey` as "occasionally" tier 1 for unpublished primary research is in tension with item 3; its correction is queued as a doctrine change.
- [OPEN] Five further questions of the owner-decision sheet: the term for a width at a turn; sub-national instruments ([CHECK] possibly answered by OD-04, L5942-L5968, and the OD-01 correction, L5763-L5777); adversarial pass 7; a library route for six papers and BS 8300; in-place correction of a locator.

### 2026-11-06 — retire workplan-orchestrator; /run-pipeline replaces it [L4943-L4955]
Owner words: "please retire workplan orchestrator. please create a new skill in its place called /run-pipeline (which includes a variant for processing evidence and beyond without research)"

In force:
- Use `/run-pipeline` (variant `from-evidence`) for a multi-stage run, and `/session-open` then `/orient` to start a session; do not look for `workplan-orchestrator` (the skill file is deleted).
- Stated as in force by this entry, about rules elsewhere in the ledger: the RULE headed "Session start protocol (GraphQL batch read: LATEST + project-standards + workplan-orchestrator …)" and the RULE "Do not re-read workplan-orchestrator_SKILL.md mid-session" are superseded; the two RULEs sending a reader to the deleted skill's "§Population Codes" and "§CO-0004 Part Numbering Map" are amended. Recorded in prose, not in `SUPERSEDES:`/`BY:` grammar.
- The skill's population-code table is replaced by `base_taxonomy_identity`.
- The skill's risk-escalation rule (two or more escalation signals append a REVIEW gap) is not carried. [unratified reading] the owner's retirement instruction does not want it re-homed.

Open:
- [OPEN] [CHECK] Decisions-register rows D-0058 and D-0065 stay `ACTIVE` until a data-only PR marks them SUPERSEDED.

### 2026-11-06 — minimum code that is correct; one value per cell; more columns [L4957-L4973]
Owner words:
- "you can add columns. another session has pointed out that there is an erroneous "net negative" rule which taken to extreme means we have no code. what I mean is for there to be the minimum code possible to perform the action correctly such that we are lean, agile and centralize data which in turn means we minimize errors and breaks and detritus"
- "tables and columns must be as clearly organized as possible. we do NOT want to have data joined in cells that will cause issues further down the pipeline or have data stored in the wrong cell"
- "more columns = more specificity = more flexibility imo"

In force:
- Judge code by whether it is the minimum that performs the action correctly, not by line count; add a column where a convention would otherwise carry a fact. (Complements, does not supersede, the separate entry "Owner rulings 2026-11-06 — minimise code; no net-negative requirement".)
- One value in each cell, each fact in the cell that names it: a foreign key where a table exists, a row per repeated value; never a list, an array or a prefixed string.
- Before shipping a schema change, run `python3 scripts/audit/joined_cells_census.py` and add no cell it would flag.
- [unratified reading] "another session" is the session that raised the same objection; no ruling of that session is relied on.

Open:
- [OPEN] Classes the census found and that want their own tooling PR and adversarial pass (named in the entry; re-derive with the census, do not trust this list): JSON lists that are a second home of a junction table (`convergence_assessment.*_sources`, `specifications.governing_refs`); JSON and delimited lists elsewhere (`search_executions.terms_used`, `citation_mining.connections_produced`, `adversarial_passes.reviewer_models` and `author_models`, `access_needs.absorbs`, `source_locators.authors` and `used_in_bpcs`, `research_code_leads.clause`); corrections appended inside a note (`search_executions.findings_note`, `gaps.description`, notes the amend verbs append to).

### 2026-11-06 — the pipeline skill's requirements [L4975-L5003]
Owner words:
- "do we have a skill that manages the process of performing research then processing it throughout every stage of pipeline followed by doing an adversarial audit for accuracy, logic, sequence?"
- "base > research > evidence > judgment > synthesis > specification > render

please retire workplan orchestrator. please create a new skill in its place called /run-pipeline (which includes a variant for processing evidence and beyond without research)

research: must be performed by topic across languages and jurisdictions while tracking its queries. must be able to perform citation mining. must be able to record evidence from a source that pertains to other categories/topics/parameters to maximize search efficiency, which means that every research row for a source must list all different categories/topics/parameters found within that source. this means that a research session may search by a given slug for sources, but the actual review of any source will concern every single thing relevant to accessible design as per the reference tables in base / at suggestion of Claude while ensuring that equivalencies are found to prevent duplication. all relevant bibliographic data must be recorded.

evidence stage must carefully adjudicate sources to assignrelevant populations/access needs/ICF codes properly referenced, and the evidence needs to be stored in such a manner where it can be used to inform synthesis+specifications as well as be able to be used directly by rendering.

synthesis will ensure the use of cross referential analysis for table rows to see if there are any relevant links within parameters/topics/categories (eg wheel chair swept path analyses for different wheel chairs would inform different space requirements)

specifications: must be able to review all evidence and syntheses of evidence to determine what best practice is, which explicitly means the most accommodating/gentle/dignified set of values/rationales/solutions for a given specification item within a category. the most commonly seen value/etc is NOT evidence of best practice but most common practice. must be able to understand code is a floor unless backed up directly by high value evidence, and we are more likely to see best practices coming from academic research/professional clinical guidelines/advocacy groups.

renders: must be able to process specifications to be readable for a webpage, must be able to compile all evidence in tables for comparison, must be radically transparent in approach, must ensure proper bibliographic citations, etc."
- "(rendering step should refer to recent PRs that concerned the webpage display of a specification item)"
- "if code documents are the only things that inform a specification, then they can be best practice...it's just going to be a weaker evidence tier"

In force:
- Follow `skills/run-pipeline_SKILL.md` for pipeline orchestration; change it by ledger entry, not session preference.
- The adversarial pass covers accuracy, logic and sequence.
- A determination resting on code documents alone may be best practice, at a weaker evidence tier (agrees with the two 2026-10-30 entries: weak band, code-derived flag, never marked full).
- [unratified reading] "evidence stage … assign relevant populations/access needs/ICF codes" means the judgment stage (where CLAUDE.md §6 places the lens crossing); the owner's omission of a judgment stage from the list is read as the same collapse. (See also delegated OD-06, L5469-L5483.)

Open: none.

### 2026-11-06 — the 93 old item subjects admitted as a basis; base must serve P1+P2+P3 languages; Opus plans [L5005-L5031]
Owner words:
- "these base tables, as per our aliases and native terms and translations and multilingual and multijurisdictional requirements etc, must work across all languages that we have defined for this current edition of project (the p1+2+3, I think it's called, for the initial countries to focus on)"
- "we should have some work already done based upon previous editions of this project and those listed specification items"
- "great work. yes, use the 93 items with stripped values as a basis. with your criticisms in mind, have Opus plan out a strategy with which to populate the base tables and address all listed issues such that we have a truly comprehensive international project without English bias"

In force:
- The 93 pre-reset item subjects, value-stripped and code-stripped, are a permitted source of candidate names, never containers. This reverses, for the pre-reset `items` names only, the 2026-10-09 clause that old Part 4 item names "are not a permitted source" (entry "Owner statements 2026-10-09 — every source is scanned for every parameter…", item 3); recorded in prose.
- "Basis" mints nothing. The 2026-10-09 guard "Screen, then you approve" stands: each candidate is screened (no digit, comparator or min/max word, no old item code, not already held) and listed in one table with its source item; the owner approves that table in a further dated entry before any term is minted.
  - [unratified reading] "use … as a basis" means a source of candidate names under that guard, not approval of names and not licence to file into old item containers; the item-layer deletion (2026-09-01) stands.
- A catalogue route (resolver, no schema change) ships as a tooling-only PR before any name is minted.
- The base tables, aliases, native terms and translations must work across every P1+P2+P3 language, with in-language provenance (R11); never treat a word-for-word English translation as a native term.
  - [unratified reading] the set is the one in `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §3 (US UK AU CA DE NO SE ISO EU; FR CH NL DK FI BE IE ES IT PT; JP SG NZ KR CN) with the languages `lang_jur_map` pairs with them; the 2026-10-29 OR-12a scoping-out of Arabic, Bengali, Hindi and Swahili is untouched. (The set is confirmed by the owner in OD-04, L5942-L5968.)
- An Opus-class planner writes a strategy to populate the base tables; the plan is a proposal and approves nothing.
- Treat every [ASSUMPTION] as unratified.

Open: none beyond the owed tooling route and the owner's approval of the screened table.

### 2026-11-06 (second) — every recommendation of the base-population plan is applied [L5033-L5066]
Owner words:
- "apply all recommendations, carefully infer and apply all solutions from my rulings and context required for pipeline to operate, etc"
- "e1 e3 e4; Appy yes"

In force (each E-item answered by the plan's recommended option):
- E1 (DG-NON): a concept first met outside English is named by the instrument's own phrase, in its own language, until an English-language instrument of a P1+P2+P3 jurisdiction is observed naming it. Narrowed within this slice by the 2026-11-06 (eighth) clarification (L5200-L5215): an English descriptive label, marked as ours, is allowed; a model's wording is never presented as a source's term. See also delegated OD-03 (L5435-L5449).
- E2: the four terms carrying a name no source used (TERM-090, TERM-092 and two others the plan's D9 finds) are renamed to the observed phrase, in a research PR after the tooling merges.
- E3: the 93 item subjects are pointed at by row number in the pre-reset database (`items:<rowid>`); no old item code in a live row.
- E4 (OR-17b): model-generated and unrecorded aliases stay as flagged search aids, never vocabulary, and are not deleted; each becomes vocabulary only when an instrument in its language is read and the phrase found there.
- E5 (licensing): WHO titles in other languages: store the pointer to the persisted payload only, until the licence is read from WHO's own terms. [CHECK] cf. owner answer OD-15 (L5942-L5968): "We do not need licenses as this is a not-for-profit advocacy project."
- E6 (population taxonomy): the base may record each language community's own designation for an identity code, attested in its own Co-1 sources, beside the English name; no identity code changes; a gap stays visible.
- E7 (jurisdiction): Norwegian is split into Bokmål and Nynorsk only where an instrument is published in both; other official languages of in-scope countries stay out of scope for now.
- E8: rooms are frozen until a page reads them.
- E9: the model proposes a `typical_stakes` for each need lacking one, with warrant, in one table; the owner approves the table before any row is written.
- E10: this edition relies on attestation from codes alone; no named native-speaker reviewer is required.
- E11: the language-and-jurisdiction pairs `lang_jur_map` holds for P1+P2+P3 are approved as OR-8 bucket members; the count is derived, not quoted.
- E12: functional-axis terms and method terms are declined as parameters, each with a reason, and kept as terms; no taxonomy change.
- Build the plan's tooling (T1–T4) in a tooling-only change before any row is written; this authorises no row.
- Write no row from the item subjects, the stakes proposal or the renames until the owner approves the table in a dated entry.
- [unratified reading] "Appy" is "Apply"; the second message confirms the recommended options of E1, E3 and E4 specifically.
- [unratified reading] the blanket "apply all recommendations" chooses the recommended option of every other E-item, including the DG-NON E5, E6, E7; it does not approve the screened table, mints, declinations or stakes table.

Open:
- [OPEN] TERM-091 (parameter 12) rename needs the owner's quote on that parameter; not applied.

### 2026-11-06 (third) — the register is written in English first, then translated to search; not English-biased [L5068-L5104]
Owner words:
- "we have categories according to the kind of technique (acoustic, circulation, etc) as well as categories according to building typology and room"
- "and these cross-pollinate each other"
- "what appears in a category specification for type (eg circulation, acoustics) will appear in building typologies and rooms and vice versa"
- "you don't need French edition here"
- "what I mean is that you will build out a comprehensive register of concepts/items/terms/techniques but you have to ensure that you research them across all of our chosen jurisdictions and languages without an English bias"
- "so we are doing prep work to get this all written out in English and then we have to translate it all properly into other languages to search them too"
- "yes"
- "we set up the base and in turn we set up the research coverage"

In force:
- Technique categories and building typologies/rooms are two views generated from one table of tagged criteria; neither is maintained beside the other. Research coverage is also generated from the base register; keep no second list.
- The English register is the search plan, not the vocabulary, and is not definitive.
- A translation of the English register is a flagged, model-generated search seed (in use in the jurisdiction, not word for word), permitted by OR-12b; not a term, alias or evidence. It is promoted only by reading an instrument in its language and finding the phrase there (E4; OR-17; R11).
- The register also takes concepts from native-language open passes over each P1+P2+P3 instrument (OR-13; plan C.3), named by the instrument's own phrase, and records per concept and per language-and-jurisdiction pair whether it was searched and what was found, including absence.
- The French RHFAC edition is not used here.
- [unratified reading] "yes" answers the session's reading that a translation is a flagged search seed and that the register also takes native-language concepts; "we set up the base and in turn we set up the research coverage" means coverage is derived from the base register, concept by pair.
- [unratified reading] "translate it all properly" is OR-12b's generation of in-use terms for flagged searches, not licence to store translations as vocabulary; OR-17 ("It is not acceptable for the model to generate its own phrases/names/aliases") and E4 are not withdrawn.

Open: none.

### 2026-11-06 (fourth) — the project may hold retrieved standards [L5106-L5116]
Owner words: "oh fuck off with the "no electronic copy". we are doing a not for profit volunteer advocacy project. this is fine"

In force (as narrowed by the fifth statement, L5118-L5138):
- A publisher's copying notice ("no electronic copy") is not a reason to withhold a source from verification; a retrieved standard may be persisted like any other source under R10. Whether a file is committed is governed by the fifth statement (large files are not).
- Republication or rendering of such text in the book is a separate question for licensing (owner's).
- [unratified reading] this rules on holding retrieved copies for verification, not on republishing or rendering a standard's text.

Open:
- [OPEN] Republication/rendering of restricted standards' text.

### 2026-11-06 (fifth) — log where a large source was retrieved from; do not commit the file [L5118-L5138]
Owner words:
- "110k is...high?"
- "ohhh it's from retrieving"
- "well, we don't need to actually commit these large PDFs etc. we just need to log where we retrieved from ie the url"
- "we don't need to be saving these PDFs in repo just tracking where they can be found for reference which is our version of persistence"
- "otherwise you're going to blow the context tokens etc. just record page number and line if need be too"

In force:
- For a retrieved PDF, web page or full-text extraction, the repository keeps the `retrieval-log/` manifest line (URL, retrieval time, status, byte count, sha256), not the file. The project may, but need not, hold a standard in the repository, and for large files does not.
- Commit an artefact that a search-execution or admission gate must find (`retrieval_log.check_artefact_link`, `log-search --artefact`).
- Persistence is tracking where a source can be found; a locator is the page number and, where needed, the line.
- [unratified reading] "large PDFs etc." means PDFs, HTML pages and text extracted from them; a small structured payload such as an API response stays committed. (CLAUDE.md §5 notes the ledger reads this small-payload carve-out as unratified.)

Open: none.

### 2026-11-06 (sixth) — a concept is an equivalence class of forms, for every term researched [L5140-L5174]
Owner words: "handicapped parking is still accessible parking stall etc" / "*also" / "there are lots of equivalencies" / "barrier free parking" / "accessibility parking, disabled parking," / "this kind of equivalency finding is applicable for all terms researched" / "inclusive, universal" / "wheelchair friendly etc" / "an elevator is a lift" / "there is a lot of conflation in literature"

In force:
- The unit of the register is an equivalence class: a concept has many surface forms per language and jurisdiction (e.g. "accessible parking stall", "handicapped parking", "barrier free parking", "accessibility parking", "disabled parking"; held instruments add "designated accessible spaces" (RHFAC 1.1) and "designated accessible parking" (CSA/ASC B651:23, cl. 9.4)).
- Non-occurrence of a form in an instrument does not invalidate it; a form the code does not use is "not attested by these texts". Other attesting sources: statutes, road-sign and signage manuals, municipal and advocacy guidance, ordinary public usage.
- Every term researched gets equivalence-class discovery. Each form carries its usage type (code term, colloquial, regional variant, outdated or disfavoured, product name) and its attestation (instrument phrase with locator, another source, owner-supplied form, unattested seed). A disfavoured form is kept with a usage note, not deleted.
- The umbrella adjective ("accessible", "barrier-free", "inclusive", "universal", "wheelchair friendly") is itself a class.
  - [unratified reading] these are equivalent as usage and unequal in scope; each is recorded with a scope note; a code's own umbrella word (e.g. "universell utforming", "barrierefrei", "esteetön") is the instrument's term.
- Conflation is recorded, not resolved: equivalence is judged per occurrence by the sense the source gives the form, never by the form alone (a text match is not a sense match); a conflation note with locator is recorded.
- This does not widen what may become vocabulary: OR-17 and E4 stand; a form enters the base as an attested alias only when a source in its language uses it. An owner-supplied form is a seed marked owner-supplied until attested. (For base vocabulary, the grounding route is changed by the seventh statement, L5176-L5198.)
  - [unratified reading] the owner's examples are English; other-language forms are found by the passes, not translated from these.

Open: none.

### 2026-11-06 (seventh) — the base grounds itself; base vocabulary is not verified and stored in evidence [L5176-L5198]
Owner words:
- "we are working on the base to create a comprehensive multilingual multijurisdictional matrix of terms/concepts that can be leveraged by research"
- "none of the work in base needs to be verified and stored in evidence."
- "base grounds itself."
- "the only thing that we need to do is ensure that our matrix works properly so that we have proper coverage across all these languages and jurisdictions"
- "so long as we can confirm that we have correct coverage, we are fine"

In force:
- The base is the matrix and is self-grounding: a base cell (concept, language, jurisdiction, form) carries where it was found in the base's own columns (source URL and, if need be, page and line). It does not point into the evidence stage and waits on no admission, quote verification or adjudication.
- For base vocabulary only, this supersedes the 2026-10-09 route of an attested alias reached through `observed_terms` and `evidence_sources` (`db.py add-alias` requiring an adjudicated observation with a verified quote). That route stays for evidence-stage reading of a source for a parameter: keep using `observe-term`, `adjudicate-term` and `add-alias` there.
- Do not admit sources or adjudicate observations merely to populate base vocabulary.
- Acceptance test: confirmed coverage, derived from the base itself (concept by language-and-jurisdiction), not a list kept beside it.
  - [unratified reading] "none of the work in base needs to be verified and stored in evidence" releases base vocabulary from admission and quote verification but does not withdraw OR-17/E4: a form still carries URL and locator, and a sourceless model-generated form is still a flagged search seed.
  - [unratified reading] "correct coverage" is a derivable measure distinguishing a cell with a form, a cell searched with none found, and a cell not yet searched; the stopping rule is derived.

Open:
- [OPEN] Owner's schema decision: whether base-cell source columns go on `term_aliases` or a new matrix table; what happens to `term_aliases.observation_id`; how a concept first met outside English is held given `terms.canonical_en` is required. [CHECK] Delegated OD-03 (L5435-L5449) answers part of the last point.

### 2026-11-06 (eighth) — English labels allowed on non-English-origin concepts; avoid English bias, not English words [L5200-L5215]
Owner words: "you obviously can have English words for these rows." / "we are trying to avoid english BIAS"

In force:
- A non-English-origin concept may carry an English descriptive label, marked as ours; it is not asserted to be a form any English-language instrument uses.
- English must not be the pivot that decides which concepts exist, what the standard form is, or how a non-English concept is described. Bias is avoided by structure: the instrument's own phrase stays on the row as a form with its language, jurisdiction and source reference; an English-language form is attached only on a source for an English jurisdiction; no column is ordered, matched or ranked ahead of another.
- OR-17 and E1 still forbid presenting a model's wording as a source's term; they do not forbid an English label.
- [unratified reading] "English words for these rows" means a flagged descriptive label kept apart from attested English forms, not permission to present it as the concept's English name.

Open: none.

### 2026-11-12 — robust base; parameters defined dynamically; read once; pipeline runs in every direction; implementation authority [L5218-L5240]
Owner words:
- "ensure that our pipeline can be run in all directions at any stage in such a manner where we can dynamically research, adjudicate, synthesize, specify and render across a multitude of languages and jurisdictions."
- "ensure that we have a robust base for languages/jurisdictions/terms/etc so that we can leverage all of them for comprehensive research, and ensure that we can dynamically derive/define new parameters as well as find linkages and equivalencies and clauses in order to group things as much as possible for clarity and robustness"
- "ensure that whenever we read a source we are able to derive all information relevant to all parameters we have defined in our base so that we don't have to repeatedly read a source to get values or worry about missing it"
- "Fable has permission to design, author, curate, orchestrate, delete as required to ensure code pipeline works as desired" — and "Fable allowed to curiously stress test, patch and iterat[e]". The owner answered "Assumption is correct" to the reading that the grant covers the code pipeline, not doctrine.

In force:
- The pipeline is to be runnable in every direction from any stage, dynamically, across many languages and jurisdictions.
- The base is a robust substrate research can use in full; new parameters derivable/definable dynamically; linkages, equivalencies and clauses found and used to group.
- A source read is to yield everything relevant to every parameter defined in the base. Qualified within this slice by OD-23 (owner, L5942-L5968): an efficiency aim, not a prohibition; a source may be flagged and read again for a later parameter.
- Authority: a Fable implementation agent may design, author, curate, orchestrate, delete, stress test, patch and iterate on the code pipeline (code, schema, scripts, checks, skills), within the rules that bind code (migrations only; tooling and research rows in separate PRs; scratch copies for stress tests). Mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing and trajectory remain the owner's. (Owner confirmed this reading.)

Open (as recorded; status within slice noted):
- What "render across languages" means — [CHECK] read by delegated OD-02 as corrected (L5780-L5795).
- Whether a determination varies by jurisdiction — [CHECK] delegated OD-01 (L5401-L5415, L5763-L5777).
- How a parameter added after a source was read reaches it — answered by owner OD-23 (L5942-L5968).

### 2026-11-12 (second) — parameters approached from a higher, abstract vantage; unify then specify [L5243-L5255]
Owner words: "recognize that we need to approach parameters from a higher level abstract vantage as too many clauses and subclauses means we may lose commonality and therefore can't unify then specify"

In force:
- Commonality across clauses, instruments and jurisdictions is a property a parameter definition must preserve; the order is unify, then specify.
- Keep clause-level extractions and reach them from an abstract parameter by pointer.
- Does not supersede the 2026-08-26 ruling (judgment object is the canonical parameter) or the 2026-10-09 statement (parameter list seeded from existing terms).
- [unratified reading] "higher level abstract vantage" is a change of grain for parameters, not permission to discard clause-level extractions.

Open:
- [OPEN] Representation of the abstraction, who judges a grouping, clause-level traceability, and whether a granularity policy is doctrine or tooling convention. [CHECK] Delegated OD-24 (L5639-L5653) resolves grain and quantity kinds; whether granularity policy is doctrine was not stated as answered.

### 2026-11-12 (third) — synthesis finds equivalencies, adjacencies, similarities and commonalities dynamically [L5258-L5270]
Owner words: "so our synthesis needs to be very dynamic in finding equivalencies/adjacencies/similarities/commonalities so that it can discuss things properly"

In force:
- Finding equivalencies, adjacencies, similarities and commonalities is synthesis's duty, on demand and not only in a planned batch.
- Record each relation as a pointer between existing rows; copy no fact (rule 5).
- Only an Opus-class model authors `best_practice_synthesis` (unchanged).
- [unratified reading] "synthesis" is the pipeline stage, not `best_practice_synthesis` alone.

Open:
- [OPEN] Relation types, representation, judge, initiation of a dynamic run. [CHECK] Delegated OD-25 (L5656-L5670) and OD-07 (L5486-L5500) address these.

### 2026-11-12 (fourth) — stress-test information may be retained across topics, at Fable's judgment [L5273-L5285]
Owner words: "permission to retain information from the stress tests across topics if fable deems them worthwhile"

In force:
- Stress-test records the Fable agent judges worth keeping may be kept and used across topics; the judgment of worth is Fable's.
- Do not retain `STRESS-FIXTURE` rows as data.
- Enter any retained research row by migration, in a research PR apart from tooling, after re-retrieval and verification (R10), by the §4 write path.
- [unratified reading] "retain" covers records (logs, findings, scripts, plans) and, for the database, only real research rows entered by migration.

Open: none.

### 2026-11-12 (fifth) — the overall code is efficient, centralised and clean [L5288-L5300]
Owner words: "ensure the overall code is efficient and centralized and clean"

In force:
- Standing requirement on the code: efficient, centralised (one home per rule, vocabulary, function and fact), clean (no dead, duplicated or contradictory apparatus). Extends the 2026-10-12 and 2026-11-06 minimise-code statements and rules 5 and 8.
- Prefer one home and point to it; delete dead and duplicated code on evidence; measure efficiency before changing it; preserve behaviour under a refactor and prove it with a before-and-after comparison; callers swept (rule 4); tooling apart from research (rule 10).
- [unratified reading] "overall code" is scripts, schemas, checks, skills and hooks, not prose or data.

Open:
- [OPEN] Which duplications first, whether a large module is split, what "efficient" means per tool (audit's improvement programme).

### 2026-11-12 (sixth) — the pipeline must be flexible [L5303-L5315]
Owner words: "pipeline must be flexible"

In force:
- Flexibility is a standing property of the pipeline. Its meaning is supplied by the seventh statement (L5318-L5332); this entry's own [ASSUMPTION] on the reading of "flexible" is superseded by that gloss.
- Prefer a change made by data or in one place over edits in several; do not bake a stage, language, jurisdiction or run shape into code where the schema or a single registry can hold it; keep deliberate refusals.

Open: see seventh statement.

### 2026-11-12 (seventh) — flexible means no hard-coded behaviours and no dead ends [L5318-L5332]
Owner words: "and that means pipeline must not have hard coded behaviours" / "or dead ends or whatever"

In force:
- The pipeline carries no hard-coded behaviours and no dead ends "or whatever" of that kind.
- Hold each rule once (schema, registry or contract) and read it from there.
- A path, row, state or refusal that leads nowhere is a defect to record and remove.
- Keep deliberate refusals (CLAUDE.md §4); they are not hard-coded behaviours in this sense unless the owner says so.
- [unratified reading] "dead end" covers a path that cannot continue or return, a row that cannot be ended or corrected, a refusal that does not say what to do next, a stage with no outbound or inbound route.

Open:
- [OPEN] What counts as a hard-coded behaviour vs a rule held once; what counts as a dead end; the "whatever".

### 2026-11-12 (eighth) — a spelled-out number is translated into a numeral and unit; original wording may be kept [L5335-L5351]
Owner words: "\"vijf\" or \"viisi prosenttia\"
>
> lol just translate these into numbers/units as applicable. you can have an untranslated column for provenance if you want"

In force:
- At extraction, a number written in words is entered as a numeral (and unit where there is one) in `claimed_value` and `claimed_unit` ("vijf" → 5; "viisi prosenttia" → 5 and %). No row is exempted from the number check for being spelled out.
- The source's own wording may be kept as provenance in a column of its own; `claim_text` still holds the verbatim quote.
- Do not back-translate or invent: the translation is of what the quote says.
- Answers GAP-056 on how a spelled-out value is filed only.

Open:
- [OPEN] The column's name, whether required, whether checked against the quote, and how extraction 30 (Dutch "vijf") and extraction 80 (Finnish "viisi prosenttia") are brought into line; GAP-056's other parts.

### 2026-11-12 (ninth) — everything non-English is translated, probably at synthesis, or wherever needed [L5354-L5366]
Owner words: "probably at synthesis or whatever we need to actually translate everything"

In force:
- All non-English held text (quotations, terms, clauses, titles) is to be translated so it can be compared and discussed; translation is a capability called at the stage that needs it, probably at synthesis; numbers are translated at extraction (eighth statement).
- Keep the untranslated text; attach the translation by pointer, marked as a translation with its translator; never present a translation as the source's own wording (OR-17, E1; the 2026-11-06 English-bias statements stand).
- Narrows OD-02 on one point: quotations may be translated.
- [unratified reading] "translate everything" is a standing capability held apart from and pointing at the source text, not replacement of it.

Open:
- [OPEN] Default stage, translator class, review, target language. [CHECK] Delegated OD-30 (L5707-L5721), OD-02 as corrected (L5780-L5795) and the tenth statement address parts.

### 2026-11-12 (tenth) — a rule that synthesis translates is not necessarily hard-coding [L5369-L5381]
Owner words: "we can set a rule for synthesis to translate, which isn't hardcoding necessarily"

In force:
- A default behaviour, including "synthesis translates", held as a rule in one stated place and read from there is permitted; do not scatter it as a literal or name-branch in code.
- Keep the translation capability callable from other stages (translation is not exclusive to synthesis).
- [unratified reading] synthesis is the default stage for translation by a rule held in one place that other stages can override or call.

Open:
- [OPEN] Where the rule is held, how read, and who may change it.

### 2026-11-12 — delegation of twenty owner decisions to an Opus-class model [L5384-L5398]
Owner words: "I guess opus can do it" (in reply to the owner's own question about resolving decisions "if granted permission with the criteria being whatever is best for (1) long-term integrity of project in terms of accuracy, academic rigour and provenance, (2) making information legible for different user types, and (3) ensuring comprehensive coverage across all disability lenses, ethical approaches and universal/population/individual design modes")

In force:
- Delegated to an Opus-class model, judged against the three criteria: OD-01, OD-02, OD-03, OD-05, OD-06, OD-07, OD-08, OD-10, OD-11, OD-12, OD-14, OD-18, OD-20, OD-21, OD-22, OD-24, OD-25, OD-26, OD-29, OD-30 (register: `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`; OD-16 withdrawn).
- Not delegated (owner's): OD-04, OD-09, OD-13, OD-15, OD-17, OD-19, OD-23, OD-27, OD-28.
- Conditions: (a) recorded as delegated, never as owner words, with deciding criterion and reversal condition; (b) reversible by the owner, standing until then; (c) interpretations of owner words (OD-06, OD-18, OD-20, OD-29) are defensible readings, not statements of what the owner meant; (d) OD-01, OD-02, OD-12 and OD-14 checked by a second independent Opus-class instance before being relied on; (e) a resolution never overrides a standing owner ruling.
- Cite a delegated resolution as delegated; do not treat the nine reserved decisions as delegated.
- [unratified reading] the criteria's numbering is their priority order; "I guess opus can do it" accepts the list of twenty and conditions (a)–(e).

Open: none (status of each OD is tracked by the status/check lines; see L5724-L5744, L5819-L5859).

### 2026-11-12 — delegated OD-01: jurisdiction in a determination, sub-national codes, climate and culture [L5401-L5415]
Recorder/delegate entry — not owner words.
In force (as corrected L5763-L5777; status RESOLVED UNDER DELEGATION, check confirmed with corrections applied):
- One live determination per parameter and lens set; each in-scope jurisdiction's figure shown beside it as a spread by pointer (comparison view).
- Where a source conditions a figure on climate or cultural context, that is a typed condition on the figure and the determination branches by it (OR-2); never key a determination on it. A cultural caveat from another source is a pointer note, never a value.
- A sub-national instrument carries its own code with its country as parent (provenance only, per correction). Correct held rows forward in a research PR.
- Sub-national coverage: referred to OD-04, since answered by the owner (L5942-L5968): sub-national counts toward its country and owes no coverage alone.
- Reversal: a parameter whose values cannot be compared across jurisdictions on one scale, or the owner requiring a determination per jurisdiction.
Open: none.

### 2026-11-12 — delegated OD-02: language of a page; how a translated quotation is shown [L5418-L5432]
Recorder/delegate entry — not owner words.
In force (as corrected L5780-L5795; RESOLVED UNDER DELEGATION, confirmed with corrections applied):
- Pages in English for this edition. Every non-English quotation, term and clause shown in its own language and script, with our translation beside it marked as a translation with translator and review status; the original carries its language tag (WCAG 2.2, 3.1.2 Language of Parts).
- Page language is a parameter of render, not fixed in it.
- Reversal: the owner naming a non-English-reading primary audience, or reviewed translation capacity for a second page language.
- [unratified reading] criteria numbering is priority order (criterion 1 over 2).
Open: none.

### 2026-11-12 — delegated OD-03: a concept with no English name [L5435-L5449]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- A concept's identity is its neutral id; its names are rows in a forms table (every attested form, any language, one row per occurrence with its source).
- `canonical_en` stays as our English descriptive label, never a form, never read first; whether a label is an instrument's own term or ours is derived, not typed.
- The displayed name is derived by E1 (origin instrument's phrase until an English-jurisdiction instrument attests an English form); a stored, warranted choice only where no derivation decides. [CHECK] For a concept several English-language instruments name differently, OD-38 (owner, L6058-L6081) governs: first English name recorded until a named judge picks with `rename-term --from-form`.
- Reversal: display name underivable for most concepts, or owner reversing E1 or the eighth clarification.
Open: none.

### 2026-11-12 — delegated OD-05: out-of-scope evidence surfaced by citation mining [L5452-L5466]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- Out-of-scope evidence that mining surfaces is staged as a lead with the mined source it came from, its jurisdiction and claimed tier; never admitted before exhaustion as defined by the owner's order, and never discarded.
- Carried by a convention in the mining skills, with no new code: the clue store (`source_locators`) holds jurisdiction, origin and claimed tier, and `search_candidates.disposition` admits `OUT-OF-SCOPE` (correction at L5855).
- [CHECK] Within this slice the owner later answered OD-04 (P1+P2+P3 replaces buckets 1 and 2 of 2026-09-28 as the first floor of research) and OD-34 (the bucket order covers codes and standards; a T1–T3 study whose finding does not depend on country is admitted on its merits) — the latter answers this resolution's referred question. How the "exhaustion of buckets 1 and 2" condition reads after OD-04 is not stated.
- Reversal: owner answering the referred question (done, OD-34), widening scope, or buckets exhausted.
Open: [CHECK] as above.

### 2026-11-12 — delegated OD-06: which stage assigns lenses [L5469-L5483]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- Lens codes are assigned at judgment, from the full reading; evidence harvests words and concepts verbatim and assigns none; admission writers take no lens arguments.
- A defensible reading of the owner's 2026-11-06 sentence, not a statement of what the owner meant.
- Reversal: owner saying the 2026-11-06 sentence meant tagging at admission.
Open: none.

### 2026-11-12 — delegated OD-07: what one synthesis row is [L5486-L5500]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- Synthesis is a separable stage whose rows a determination points at: convergence (engine-computed and stored, as now), judged relations, conflicts and judged discussion text. A run may invoke synthesis from any stage; what synthesis finds is kept, with judge and warrant.
- A determination points at its synthesis rows through a link table, never a list in a cell.
- Reversal: measured evidence that kept relation rows go stale faster than they are re-judged.
Open: none.

### 2026-11-12 — delegated OD-08: what an absent cell means [L5503-L5517]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- No determination row is stored for a cell without a figure.
- A lens judged relevant to a parameter with no figure is recorded as an open typed gap naming parameter and lens, in the cross-stage gap register.
- Whether a cell is not relevant, not yet researched, or researched and empty is derived from gaps, searches and readings, not stored.
- Reversal: a reader-facing need the derived answer cannot meet, or the owner restoring stored `pending` cells.
Open: none.

### 2026-11-12 — delegated OD-11: which stage owns the gap register [L5520-L5534]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force (as corrected at L5855):
- Any stage that finds a gap may write it. The register is marked cross-stage in the stage map. The raising stage is not given a column now; it is added when a reader needs it.
- Run the walkability instrument before and after the stage-map change; lose no path.
- Reversal: the stage map gaining a stage for it, or the owner assigning gaps to one stage.
Open: none.

### 2026-11-12 — delegated OD-12: how render's prose is produced, and whether stored [L5537-L5551]
Recorder/delegate entry — not owner words.
In force: see the correction at L5798-L5816, which gives the resulting state (RESOLVED UNDER DELEGATION, confirmed with corrections applied). Surviving from this entry:
- Render assembles every sentence by templates held in one place from typed rows and writes no prose of its own judgment.
- Discussion needing judgment (divergence approach, relation, caveat) is a synthesis-stage row written at the Opus floor with its warrant, quoted by pointer.
- The render table holds the complete prose and bibliography of OW-1, regenerated in full from its inputs at each build, with a per-row input hash; never edited; never read as the source of a fact.
- Translations appear only as the page-language and translator resolutions allow.
- Reversal: a measured build cost making full regeneration impractical, or reader testing showing template prose fails the 2026-10-30 legibility requirement where synthesis discussion does not cure it.
Open: none.

### 2026-11-12 — delegated OD-14 (rows written under MOB) [L5554-L5568]: nothing in force (history only: withdrawn by correction L5747-L5760; OD-14 since answered by the owner, L6015-L6036 and L6058-L6081)

### 2026-11-12 — delegated OD-18: what "all directions" covers [L5571-L5585]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- The cold-entry and re-entry conditions of the top-down specification §3 stand, with five corrections recorded in `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md` (OD-18); among them: a specification with insufficient evidence writes no row and raises a typed gap; the base, synthesis and render postconditions take the same-date delegated resolutions. Write the corrected conditions into the pipeline contract.
- [CHECK] "a 'provisional reading' re-entry reads as a skimmed or preliminary reading until the owner answers the open question on `provisional`" — the owner answered OD-10 (L5971-L6012): `provisional` = thin evidence; a re-read owed is a reading's own status.
- An earlier stage's row may record a change in its own state (verification standing, retired, superseded-by); never a later stage's use or fact, which is reached by pointer.
- A defensible reading of the owner's objective, not a statement of what the owner meant.
- Reversal: owner correcting a condition, or a needed re-entry no condition permits.
Open: none.

### 2026-11-12 — delegated OD-20: the owner's edits [L5588-L5602]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- The owner's changes are proposals applied through the sanctioned write path, each by migration with the owner named as judge and reason recorded on the changed row; dependants recomputed.
- An edit aimed at a computed value (determination state, value or marker) is applied to the figure, source or rule it was computed from, or recorded as an open question on the cell, never written into the determination (owner, 2026-09-09 evening: "you have to compute it").
- Reversal: the owner ordering a direct-write route.
Open: none.

### 2026-11-12 — delegated OD-21: a question about a published cell [L5605-L5619]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- An objection to a published value is recorded in the database as an open gate on the cell, with who raised it and the objection's text; the cell is shown as "questioned" (not "wrong") until closed by re-derivation or a recorded answer with warrant.
- Reversal: gates raised faster than they can be answered.
Open: none.

### 2026-11-12 — delegated OD-22: rounding direction for converted lengths [L5622-L5636]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- A converted figure is shown at the nearest quarter inch or 5 mm (OR-10) that does not fall on the wrong side of the source's bound: a minimum never below, a maximum never above. If the nearest increment is already on the safe side, use it unchanged. Stored bound stays exact; shown figure marked as converted.
- Answers OR-10b only.
- Reversal: owner reading "nearest" as excluding any direction rule.
Open:
- [OPEN] Owner-queue prompts OR-5b, OR-6c, OR-22b, OR-23b, OT-2, OR-14b and OR-25 remain the owner's (as of this entry). (OW-1b/OW-1c: resolved under delegation, OD-12; OR-1c and OR-17b: answered by owner 2026-11-06.)

### 2026-11-12 — delegated OD-24: parameter coarseness and quantity kinds [L5639-L5653]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- A parameter is one measured quantity; clause variations are typed conditions; families reached by typed term pointers. Split test: two cases are two parameters only when they cannot be placed on one scale or their accessibility directions differ.
- Clause-level extractions kept and reached by pointer.
- Each parameter states its quantity kind from a registry of kinds held as rows (seeded from live parameters' needs, not a list typed in code), extended by data with a warrant. Kinds named: length, gradient (ratio, percentage or degrees as notations), force, time, luminous reflectance and its contrast (LRV), colour temperature.
- A parameter need not belong to an element; elements reach parameters by term pointers, many to many.
- Reversal: a parameter whose cases share scale and direction but cannot be determined together without losing a group's difference, or a kind that cannot be added without a schema change.
Open: none.

### 2026-11-12 — delegated OD-25: relations synthesis records, and who judges them [L5656-L5670]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- Four relation kinds: equivalence (same thing, interchangeable); commonality (share an identified element, differ in others; unify on it with differences as conditions); similarity (resemble without identified shared element; a lead, never a ground to unify); adjacency (distinct things that bear on or constrain each other).
- A recorded relation carries judge and warrant; judged by an Opus-class model or above; candidates found by query (any class) are not recorded without judgment.
- Unify only on equivalence or commonality. Conflict and convergence stay in their existing tables.
- A reading of the owner's four words of 2026-11-12 (third), at low confidence on the similarity/commonality line.
- Reversal: owner glossing the words otherwise, or similarity and commonality proving indistinguishable.
Open: none.

### 2026-11-12 — delegated OD-26: interim stage-pair gate before render exists [L5673-L5687]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- No interim gate on a stored baseline. Run the walkability instrument as a command at the end of every wave and before and after any stage-map change; OW-2's registration follows render. Command: `python3 workplan/pipeline-state-graph/walkability.py | grep "NO PATH"`.
- Reversal: a wave-end run finding a non-render path lost between waves; then an interim gate with an exemption derived from the graph, never stored.
Open: none.

### 2026-11-12 — delegated OD-29: retire-in-place and link rows [L5690-L5704]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- A connection and a search-to-source admission edge are both data rows under the 2026-09-16 ruling ("retire in place then"); neither is hard-deleted. A connection gains a retired status; an admission edge gains retired-at, retired-by and reason columns; `unlink-admission` becomes a retire verb that no longer writes the removed edge into a note.
- Before the first retirement, every reader of either table filters on the mark.
- A genuine deletion of either is an exception the owner rules on case by case.
- A defensible reading of the 2026-09-16 ruling.
- Reversal: the owner ruling an exception for edges without an identifier.
Open: none.

### 2026-11-12 — delegated OD-30: who may translate; review before use [L5707-L5721]
Recorder/delegate entry — not owner words. Status: RESOLVED UNDER DELEGATION; check not required.
In force:
- Any model may draft a translation, recorded with its translator.
- Synthesis may read an unreviewed translation only as an aid; it relies on a passage only after its Opus-class author has checked it against the original.
- A reader is shown only a translation reviewed by an Opus-class instance other than its translator (recorded in the translation's reviewer columns), beside the original.
- A translation that changes a figure is refused.
- Reversal: a fluent reader's sample check finding meaning-changing errors, or the owner naming human reviewers.
Open: none.

### 2026-11-12 — convention: how a delegated resolution's standing is recorded, and when it opens a gate [L5724-L5744]
Recorder/delegate entry — not owner words (a convention for reading the ledger; the owner may replace it; kept by the owner on OD-35, L5971-L6012).
In force:
- Per register decision: a status line `OD-NN STATUS: <value>` (`ANSWERED BY THE OWNER`, `RESOLVED UNDER DELEGATION`, `WITHDRAWN, REFERRED BACK TO THE OWNER`, `REFERRED BACK TO THE OWNER`; plus `DEFERRED BY THE OWNER` from the addendum, L5901-L5909), and for a delegated resolution a check line `OD-NN CHECK: <value>` (`not required`, `pending`, `confirmed`, `confirmed with corrections applied`, `referred back`).
- Each is read as the last line of its kind for that id; a later line supersedes an earlier; no line is edited.
- Gate OPEN only when the last status is `ANSWERED BY THE OWNER`, or the last status is `RESOLVED UNDER DELEGATION` and the last check is `not required`, `confirmed` or `confirmed with corrections applied`. All else CLOSED. A task whose text requires the owner's own words is open only on `ANSWERED BY THE OWNER`.
- Gate command:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
```
- `OD-NN:` answer lines remain the record of what was answered; they do not open a gate by themselves.
- When recording an owner's answer to a register decision, add `OD-NN STATUS: ANSWERED BY THE OWNER` in the same entry. Never edit a status or check line; append.
Open: none.

### 2026-11-12 — correction to delegated OD-14: withdrawn and referred back [L5747-L5760]
Recorder/delegate entry — not owner words.
In force:
- The delegated OD-14 resolution is withdrawn; build nothing on it. A delegated resolution may not conclude that an owner rule no longer binds because a later ruling removed its basis where the later ruling does not name it (reserved, condition (e)).
- The status lines in this entry (WITHDRAWN, REFERRED BACK; check referred back) are superseded within this slice by `OD-14 STATUS: ANSWERED BY THE OWNER` (L6028). The referred question was answered by the owner's third set (L6015-L6036), fourth set on GAP-076/OD-31 (L6039-L6055) and fifth set (L6058-L6081).
- Facts kept by this entry that may still bind [CHECK]: the 2026-08-25 ruling's grade clause ("Not fanned out, ever") kept in full; `evidence_population_match` has no retirement column (verify: `PRAGMA table_info(evidence_population_match)`), so retiring grade rows needs a tooling change first; `base_taxonomy_identity.status` takes `deprecated`, not "retired".
Open: none in this entry (question answered later in slice).

### 2026-11-12 — correction to delegated OD-01 [L5763-L5777]
Recorder/delegate entry — not owner words.
In force:
- OD-01 STATUS: RESOLVED UNDER DELEGATION; OD-01 CHECK: confirmed with corrections applied.
- The parent of a sub-national code is a provenance relation only; decide nothing about its coverage here (coverage since answered by owner OD-04: counts toward its country). A provincial code must not stand in for its country's coverage.
- Four held cases to re-file in a research PR after the registry exists (GAP-077: `select description from gaps where gap_id='GAP-077'`): REF-00992 (Approved Document M vol. 2, "for use in England", filed `UK`), REF-00995 (Flemish Government decree, filed `BE`), REF-01013 (Ontario Building Code, filed `CA`), REF-01029 (a Madrid methodology, filed `ES`).
- Branching a determination by a climatic or cultural condition rests on OR-2 ("Branches, and an empty headline when all are conditioned"). The Kawa and PAS 6463 rules and `governance/armature_v4_resolutions.md` Q29 (not an owner ruling) warrant only that culture and climate are conditions, not keys. A cultural branch keeps the Kawa rule's flag ("Specify the physics; flag the spatial model for Person Mode co-design").
- Sub-national codes follow ISO 3166-2 except the project convention `UK`, never `GB` (`governance/jurisdiction-philosophy.md` §3.3).
Open: none.

### 2026-11-12 — correction to delegated OD-02 [L5780-L5795]
Recorder/delegate entry — not owner words.
In force:
- OD-02 STATUS: RESOLVED UNDER DELEGATION; OD-02 CHECK: confirmed with corrections applied.
- It is a delegated reading (condition (c)) of the owner's "render across a multitude of languages and jurisdictions": met in this edition by showing each source's own language, tagged, beside our marked translation, with page language a render parameter, not by multilingual pages. Reversible by the owner.
- English pages are held to the 2026-11-06 anti-bias rulings ("we are trying to avoid english BIAS"): original shown first or beside every translation; our English never presented as a source's term; English one column of the matrix. They are not exempt.
- The reason for English-only this edition is criterion 1's priority over criterion 2 ([unratified reading]).
- The renderer must emit a page in a second language by data alone (template set and page-language value), with no code edit (owner, 2026-11-12, seventh).
- English is the target for display only; this does not fix the language in which synthesis compares evidence (left open by the ninth statement).
Open:
- [OPEN] Language in which synthesis compares evidence.

### 2026-11-12 — correction to delegated OD-12 [L5798-L5816]
Recorder/delegate entry — not owner words.
In force:
- OD-12 STATUS: RESOLVED UNDER DELEGATION; OD-12 CHECK: confirmed with corrections applied.
- OD-12: templates at render; judged discussion as Opus synthesis rows quoted by pointer, shown only once reviewed; render table rebuilt outside the database.
- This is OW-1b's "mixed" option with the model's text moved from render to synthesis and without the owner's review that both model-writing options offered; that removal is a delegated choice the owner may reverse (ground: owner, 2026-09-09, "I can't handle this load manually"). [CHECK] The owner later answered OD-32 (L5971-L6012): "Independent model review suffices; I can still question any cell".
- A judged-discussion row carries its review status; a reader sees it only once an Opus-class instance other than its author has reviewed it, or the page says the discussion is unreviewed.
- The deployed copy can be stale between builds; the per-row input hash detects it, read by one check (named in the render task) comparing deployed rows' hashes with their inputs now; otherwise the hash is not added.
- The render table is a build product outside `data/guidebook.db`, generated not committed (2026-08-27 rule that no committed file is a render holds). This departs from the [ASSUMPTION] recorded with OW-1 ("the render table lives in the database and the site reads it"). (Also given its own id, OD-33, L5877-L5898.)
- Mark OW-1b and OW-1c in `governance/owner-browser.yaml` "resolved under delegation (ledger, OD-12)", not "answered".
- Templates rewrite no source sentence; a translated sentence is shown only as OD-02 and OD-30 allow.
Open: none.

### 2026-11-12 — status lines for delegated resolutions needing no independent check, and OD-10 [L5819-L5859]
Recorder/delegate entry — not owner words.
In force:
- RESOLVED UNDER DELEGATION, CHECK not required: OD-03, OD-05, OD-06, OD-07, OD-08, OD-11, OD-18, OD-20, OD-21, OD-22, OD-24, OD-25, OD-26, OD-29, OD-30. Each reversible by the owner.
- OD-10: the status here (REFERRED BACK TO THE OWNER) is superseded within slice by `OD-10 STATUS: ANSWERED BY THE OWNER` (L5982).
- OD-11 correction: gap register marked cross-stage in the stage map; the raising stage gets no column until a reader needs it (CLAUDE.md §8); walkability instrument run before and after.
- OD-05 correction: staging needs no new code; carried by a convention in the mining skills (`PRAGMA table_info(source_locators)`; `search_candidates.disposition` admits `OUT-OF-SCOPE`).
- Read these lines through the gate convention.
Open: none.

### 2026-11-12 (twelfth) — remaining owner decisions resolved before the plan is called complete; Opus may judge where appropriate [L5862-L5874]
Owner words: "Address issues within remediation plan. Confirm that owner decisions located within batches are still actively required rather than having been answered in the most recent passes. I think it would be best to get the decisions resolved before saying the plan is complete. You have permission to use Opus for judgment if appropriate here."

In force:
- Address the plan's issues; confirm from the plan and ledger which owner decisions still hold up work.
- Treat the remediation plan as incomplete while a decision that blocks a task stands open.
- An Opus-class model may resolve only what the reading below allows, recorded as a delegated resolution with the gate convention; prepare every other open decision as a prompt for the owner with facts and a recommendation.
- Does not lift the reservations of the delegation entry.
- [unratified reading] "appropriate" = a decision the three criteria settle, overriding no standing owner ruling, and not the owner's own act or words, a licensing or legal determination, trajectory or control, or the weighing of one group's harm against another's under the CRPD posture.

Open: none in this entry.

### 2026-11-12 — register entries OD-31 to OD-35; OD-33 resolved [L5877-L5898]
Recorder/delegate entry — not owner words.
In force:
- Five questions from `workplan/2026-11-12-bidirectional-pipeline/FOLD-LOG.md` §2 (PQ-1 to PQ-5) entered as OD-31 (part of GAP-076), OD-32, OD-33, OD-34, OD-35. OD-31, OD-32, OD-34 and OD-35 were prepared for the owner and are answered by the owner later in this slice (L5971-L6012; L6039-L6055).
- OD-33 (STATUS: RESOLVED UNDER DELEGATION; CHECK: not required): the render table of OW-1 is generated from `data/guidebook.db` at each build and not stored in it; each row carries an input hash read by the one staleness check the render task names. Reversible by the owner on its own.
  - Reversal: the owner placing the render table in the database (a write path designed first), or a measured build cost a stored table would remove.
- Resolved under the twelfth instruction's [unratified reading].
Open: none.

### 2026-11-12 — convention addendum: status value for a decision the owner defers [L5901-L5909]
Recorder/delegate entry — not owner words (convention; the owner may replace it).
In force:
- Status value `DEFERRED BY THE OWNER`, written only by the session recording the owner's quoted deferral, in the same entry. The gate reads it as CLOSED. D-27 (Definition of Done, `REMEDIATION-WORKPLAN.md` §10) counts it as settled only for a decision no task's gate reads; a deferral of a decision a gate reads leaves the task stopped.
Open: none.

### 2026-11-12 (thirteenth) — MOB decomposes into more specific identity populations [L5912-L5924]
Owner words: "MOB is more difficult than other categories in that it decomposes into more specific identity populations (e.g. prosthetics vs wheelchairs vs other mobility aids, power wheelchair vs manual wheelchair, paraplegia vs quadraplegia)"

In force:
- The mobility identity is a family with more than two levels of division (by aid, by wheelchair drive, by impairment level); the owner's examples are examples, not a closed list. Do not assume the two-way split is the whole decomposition.
- Keep a division that describes a device or a participant's level in one home only (rule 5); whether a division is an identity code or a descriptor is decided with the owner.
- The resulting family is settled later in this slice (ninth set, L6149-L6162).
- [unratified reading] the statement describes the domain and widens OD-14; by itself it does not supersede the 2026-08-25 ruling.

Open: none beyond those carried to later sets.

### 2026-11-12 (fourteenth) — advocacy groups and disability ethics as the lens for grouping, sorting and taxonomy [L5927-L5939]
Owner words: "use advocacy groups and disability ethics as a lens for grouping/sorting/taxonomy"

In force:
- Take the organisation of disabled people's own advocacy groups, and the approaches of disability ethics, as the lens for how identity/population categories are drawn; record the group or ethical source a grouping rests on as provenance; leave the choice among competing groupings to the owner (population taxonomy is the owner's).
- Does not supersede the 2026-08-28 lens-column ruling or the ICF/access-need frame; it is a lens on how groupings within them are drawn. [CHECK] The entry says "four lens columns"; CLAUDE.md §6 records the medical lens deleted by the owner on 2026-11-16 (outside this slice).
- [unratified reading] "advocacy groups" means disabled people's own organisations and self-advocacy groups (CRPD "representative organizations"), not charities or bodies speaking for disabled people.

Open:
- [OPEN] Which groups count, how their categories become codes, how disagreeing ethical approaches are weighed, which present codes change (partly answered by OD-37, L6015-L6036).

### 2026-11-12 — owner answers OD-04, OD-23, OD-15, OD-19 [L5942-L5968]
Owner words:
- OD-04 (selected option): "P1+P2+P3 as recorded; UN out; sub-national counts toward its country"
- OD-23: "Clause inventory backed by retained text; clause NOT shown. However, we can still read a source more than once--we just want to minimize duplicate reads for efficiency and managing effort. We can flag a source to be read again for later parameters."
- OD-15: "We do not need licenses as this is a not-for-profit advocacy project."
- OD-19 (selected option): "Record now; the engine applies an ordering once you approve it"

In force:
- OD-04 (ANSWERED BY THE OWNER): scope for base, research and page is P1+P2+P3 as recorded (US UK AU CA DE NO SE ISO EU · FR CH NL DK FI BE IE ES IT PT · JP SG NZ KR CN); `UN` is outside it (cited, owing no coverage); a sub-national instrument counts toward its country and owes no coverage alone. This replaces buckets 1 and 2 of 2026-09-28 as the first floor of research (adds BE, CH, CN, DK, IT; drops UN).
- OD-23 (ANSWERED BY THE OWNER): a later parameter reaches a source already read by matching a stored inventory of the source's clauses, backed by retained text; held clause text is not shown on a page. Re-reading is permitted; minimise duplicate reads; a source may be flagged to be read again for a later parameter. Qualifies the 2026-11-12 read-once objective as an efficiency aim.
- OD-15 (ANSWERED BY THE OWNER): proceed; no WHO written agreement sought (ground: not-for-profit advocacy project). The medical lens is filled from ICD-11 at block grain by correspondence, as ruled 2026-09-11. Do not read this as a legal opinion on the WHO terms.
  - [UNVERIFIED] that not-for-profit status removes the requirement; the WHO terms (`https://icd.who.int/en/docs/icd11-license.pdf`; CC BY-ND 3.0 IGO; cl. 1.2.4 on mappings, crosswalks, translations) carry no stated not-for-profit exemption; the decision and risk are the owner's.
  - [unratified reading] attribution (code, title and URI together; WHO named as source; correspondence marked as the project's addition) is kept as ordinary practice.
  - [CHECK] CLAUDE.md §6 records the medical lens deleted by the owner on 2026-11-16 (outside this slice).
- OD-19 (ANSWERED BY THE OWNER): the engine records every conflict between groups as a row with its named judge and computes nothing from it until the owner approves an ordering (approved as OD-36, L6039-L6055).
Open: none (harm ordering approved later in slice).

### 2026-11-12 (second set) — owner answers OD-28, OD-10, OD-34, OD-13, OD-32, OD-09, OD-27, OD-35 [L5971-L6012]
Owner words (selected options): OD-28 "Enter them verbatim from the transcript"; OD-10 "Strength: 'provisional' = thin evidence; a re-read is a reading's own status"; OD-34 "Instruments only: a T1–T3 study is admitted on its merits"; OD-13 "Superseded by the pair rulings"; OD-32 "Independent model review suffices; I can still question any cell"; OD-09 "On demand, judgments warranted; no request table"; OD-27 "Serial is fine"; OD-35 "Keep it".

In force (each ANSWERED BY THE OWNER):
- OD-28: the eight relayed sentences of 2026-10-12 (O1–O8) are entered verbatim from the committed transcript, including trimmed openings ("use Opus to" in O1, "yeah, and" in O7). Task T-023.
- OD-10: a cell's `provisional` means thin evidence (2026-09-09); a re-read owed is a reading's own status (`preliminary` or follow-up). [unratified reading] that is how the 2026-09-09 and 2026-10-30 statements reconcile.
- OD-34: the 2026-09-28 bucket order covers codes and standards, not laboratory or clinical studies whose finding does not depend on the country; such a T1–T3 study is admitted on its merits.
- OD-13: the 2026-03-19 "at least nine languages" rule is superseded by the language–jurisdiction pair rulings; mark it by back-pointer (`SUPERSEDES` convention), not by editing the ledger.
- OD-32: independent model review suffices; the owner can question any cell.
- OD-09: runs may be carried through on demand without the owner present, each judgment warranted; no request table.
- OD-27: research batches land serially.
- OD-35: the status-and-check convention for decisions is kept.
Open: none.

### 2026-11-12 (third set) — owner answers OD-14 (what MOB is) and OD-37 (identity-lens rule) [L6015-L6036]
Owner words: "MOVE and VES are access needs, agreed. Decompose MOB by device to wheelchair user, prosthetic device user, other mobility aids (or something like that). retain MH and NDV and TALL"

In force:
- OD-14 (ANSWERED BY THE OWNER): MOB is decomposed; exact codes confirmed and later revised (fifth set, eighth and ninth sets; resulting family at L6149-L6162). It widens the 2026-08-25 two-way split; it does not by itself say the 2026-08-25 ruling is withdrawn.
- OD-37 (ANSWERED BY THE OWNER): `MOVE` and `VES` are access needs, not identity populations — move them to the access-need frame. `MH`, `NDV` and `TALL` are retained as identity codes. The memo's wholesale rule (identity codes only where an organised, self-named community exists) is not adopted. `ALL`, `DEAF`, `LMB` and `COM` stand unchanged unless the owner says otherwise — [CHECK] `ALL` later leaves the identity lens (OD-31, L6039-L6055) and `LMB` becomes `UPL` (L6129-L6146).
- Keep a division held in `device_class` and as an identity code in one home only (rule 5).
- [unratified reading] "(or something like that)" invites proposal of exact codes by the T-102 design, subject to the owner seeing them; not a delegation to decide the taxonomy.
Open: none in this entry (OD-31 answered in the fourth set).

### 2026-11-12 (fourth set) — owner answers OD-31 (ALL) and OD-36 (harm ordering) [L6039-L6055]
Owner words (selected options): OD-31 "Heading's group; ALL leaves the identity lens"; OD-36 "Approve that ordering, held once as data; each class warranted by a held source's own finding".

In force:
- OD-31 (ANSWERED BY THE OWNER): a provision that names no one carries the group its heading names (under a mobility heading, the parent `MOB` with no child; under a general disability heading, no identity, only its ICF and access-need lenses). `ALL` leaves the identity lens; "universal" is stated once, by `design_scale = 'universal'` (rule 5). Rows filed under `ALL` as an identity are re-tagged by their links. Do not use `ALL` as an identity. This resolves the hedged 2026-11-06 answer ("I guess we can see it as a universal?").
- OD-36 (ANSWERED BY THE OWNER): the harm ordering injury > loss of independent use > pain > effort > discomfort is approved, held once as data (a row, changeable in one place), each class warranted by a held source's own finding and never a model's estimate; a tie goes to a named judge. The engine may apply it where groups conflict, defaulting to the less harmful option for the group the ordering protects and flagging the supplementary provision for the other group. T-053 builds it.
Open: none.

### 2026-11-12 (fifth set) — T-102 codes; OD-17; OD-38; OD-39 [L6058-L6081]
Owner words (selected options): T-102 codes "Confirm all as proposed"; OD-17 "Ratify after T-022 merges, once I have read the corrected contract"; OD-38 "First recorded, until a named judge picks; the pick is recorded with its reason"; OD-39 "Yes, the 2026-11-06 ruling supersedes that clause".

In force:
- T-102 codes (OD-14 confirmation), as revised within this slice by the seventh, eighth and ninth sets: surviving from this confirmation — `MOB` stays as the parent, renamed "disabled people with mobility needs"; `WHEEL` (wheelchair users, including ambulatory and part-time wheelchair users); `WALKAID` (people who use walking aids: crutches, canes, frames, rollators); `AMB` is not minted; scooter users stay on `MOB` with `device_class = scooter`; a person with a mobility need who uses no aid has no child (MOB plus ICF d4 codes and access needs). Superseded within slice: `PROSTH` (replaced by `LLD`, ninth set) and "LMB is unchanged" (LMB becomes UPL, eighth set). Rows may be written on the confirmed options. [Not the owner's: "PROSTH" and "WALKAID" are descriptive names; no organisation of walking-aid users was found.]
- OD-17 (DEFERRED BY THE OWNER): the owner will ratify the corrected `governance/pipeline-contract.yaml` after T-002 and T-022 have merged, once they have read it; ask again with the diff in front of the owner. Nothing waits on it.
- OD-38 (ANSWERED BY THE OWNER): for a concept several English-language instruments name differently, the first English name recorded is shown until a named judge picks one with `rename-term --from-form`; the pick is recorded with its reason. Follow it in T-028's `rename-term`.
- OD-39 (ANSWERED BY THE OWNER): the 2026-11-06 link-table ruling supersedes the 2026-08-28 clause "Never a population_* link table"; T-018 builds `extraction_lens_links`. How the supersession is recorded: see correction L6084-L6090 (no `SUPERSEDES` pair).
Open:
- [OPEN] OD-17 ratification (deferred).

### 2026-11-12 — correction: how OD-39's supersession is recorded [L6084-L6090]
Recorder/delegate entry — not owner words.
In force:
- The 2026-08-28 clause "Never a `population_*` link table" is superseded by the 2026-11-06 link-table ruling, on the owner's answer to OD-39.
- Do not add a `SUPERSEDES` pair for it (it would fail `supersession_backpointer_audit`); this entry and `workplan/2026-11-12-bidirectional-pipeline/tasks/T-018-link-table.md` are the record, in prose.
- Where the fifth set says T-018 appends the pair, read it as corrected here.
Open: none.

### 2026-11-12 (sixth set) — SCI and LMB go under MOB (OI-13) [L6093-L6108]
Owner words: "SCI and LMB go under MOB"

In force:
- Superseded in substance within this slice by the seventh, eighth and ninth sets: `SCI` is held as one population with `WHEEL` under `MOB`; `LMB` becomes `UPL`, outside mobility. Resulting family at L6149-L6162.
- Surviving: identity children are set through the registry's existing `parent_code` column; the children are not treated as mutually exclusive ([unratified reading]: the identity lens takes at least one code per figure and a figure may name more than one group).
- [OPEN] [CHECK] Whether a determination at `MOB` gathers its children by `parent_code` (T-055).

### 2026-11-12 (seventh set) — SCI is basically WHEEL; LMB is basically PROSTH [L6111-L6126]
Owner words: "except SCI is the same as WHEELCHAIR basically and LMB is the same as PROSTHETIC"

In force:
- `SCI` is "basically" the same population as `WHEEL`; each such pair is held under one code (rule 5). The surviving code is the device code `WHEEL` ([unratified reading], consistent with the eighth set's "only SCI is the same as WHEEL"); retire `SCI` by the sanctioned verb with its successor; re-tag its rows by what each names; do not fan out a grade.
- Impairment level (paraplegia, quadriplegia) is a descriptor in the medical lens and ICF codes, not an identity code. [CHECK] CLAUDE.md §6 records the medical lens deleted 2026-11-16 (outside this slice).
- Superseded within slice by the eighth set: the pairing of `LMB` with `PROSTH`, and the action to describe `PROSTH` as holding what `LMB` held.
Open:
- [OPEN] How the cases "basically" leaves out are handled (e.g. a person with an incomplete spinal cord injury who walks). Rows under `SCI` to be carried (derive counts; do not trust the dated figures).

### 2026-11-12 (eighth set) — LMB becomes UPL (upper limb), not part of mobility; only SCI is the same as WHEEL [L6129-L6146]
Owner words: "LMB should be UPL for upper limb then" / "and that doesnt concern mobility"

In force:
- `LMB` is to be `UPL` (upper limb); it does not concern mobility, is not a child of `MOB`, and is not the same population as `PROSTH`. Do not describe `PROSTH`/`LLD` as holding what `LMB` held.
- `SCI` and `WHEEL` are held as one population under `WHEEL`.
- Make `LMB` into `UPL` by the sanctioned verb with the successor if it is a new code; move its map rows without duplicating.
- Supersedes the seventh set's `LMB`–`PROSTH` pairing and the sixth set's placing of `LMB` under `MOB`.
- [unratified reading] `UPL` is an identity-lens population like the others and keeps `LMB`'s ICF map rows; a lower-limb difference without a prosthesis sits on `MOB` with ICF d4 codes, and an upper-limb prosthesis user on `UPL` ([CHECK] partly overtaken by `LLD` in the ninth set).
Open:
- [OPEN] Rename vs new code with `LMB` retired to it; `UPL` display name and description; edge cases (upper-limb disability affecting reach as a lens on reach and manipulation parameters; the owner's `upper-limb-impairment-built-environment` topic).

### 2026-11-12 (ninth set) — the lower-limb child of MOB is LLD, "people with lower-limb differences" [L6149-L6162]
Owner words (selected option): "LLD — 'people with lower-limb differences'"

In force (resulting mobility family):
- The lower-limb child of `MOB` is `LLD`, people with lower-limb differences, replacing `PROSTH`; defined by the condition, so it holds lower-limb prosthesis users and people with a lower-limb difference who use none. It is the lower-limb counterpart of `UPL` (upper limb, outside mobility). The owner chose this knowing it departs, for this one child, from decomposition "by device".
- The mobility family is the parent `MOB` with children `WHEEL` (taking in `SCI`), `LLD` and `WALKAID`; `LMB` becomes `UPL`, outside mobility. (Other confirmed points from the fifth set stand: `MOB` renamed "disabled people with mobility needs", `AMB` not minted, scooter on `MOB` with `device_class = scooter`, no-aid person on `MOB` with ICF d4 codes and access needs.)
- Use `LLD`, not `PROSTH`. Place the rows of the old `LMB` on `UPL` or `LLD` by what each names.
- Keep the prosthesis, where it is a device fact, in `device_class` only if the design settles it there without a second home.
- Supersedes the confirmed T-102 code `PROSTH` (fifth set) and the seventh set's `LMB`–`PROSTH` pairing.
- OI-13 STATUS: ANSWERED BY THE OWNER.
- [unratified reading] identity codes are not mutually exclusive: a person with a lower-limb difference who also uses a wheelchair or walking aid is in `LLD` and in `WHEEL` or `WALKAID`.
Open:
- [OPEN] Whether the T-102 design's proposed `device_class` values (`lower_limb_prosthesis`, `crutches`, `cane`) remain, given `LLD` is condition-defined; the registry description of `LLD`; placement of each old `LMB` map row (derive the rows; do not trust dated counts).

---

Slice stats: entries read 63; entries reduced to nothing in force 1; entries tagged [STATUS UNCERTAIN] 0 (in-slice supersessions were resolvable; out-of-slice bearings flagged [CHECK] instead: the medical-lens deletion of 2026-11-16 at L5927-L5939, L5942-L5968, L6111-L6126); lines read 4922-6163.
