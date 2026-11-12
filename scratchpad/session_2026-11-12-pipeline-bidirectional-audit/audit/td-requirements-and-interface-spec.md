# TD — Requirements ledger and stage interface specification (top-down leg)

_Written 2026-11-12 (UTC) against the working tree at `git rev-parse --short HEAD` = `64c10e2`. Line numbers were resolved with `grep -n -F` against that tree, not copied from the dossier (the dossier was generated at `e73b588`; re-resolve any line before relying on it: `grep -n -F '<quote fragment>' <file>`)._

## 0. Verdict

**The owner's prose does not yet state the objective it was asked to support.** Read against D1–D4:

1. **D4 (verifiable, traceable) is the only dimension the prose states fully, verbatim and repeatedly.** Pointer discipline, retire-in-place, never-reissued identifiers, logged empties and computed determinations are all ruled.
2. **D3 (multilingual, multijurisdictional) is ruled in depth for `base` and `research` and almost not at all downstream.** Nothing in the prose says what language a rendered page is in, whether a source's sentence may be translated, or whether a determination varies by jurisdiction. The one concrete schema consequence the owner was told about (`terms.canonical_en` is required) is recorded as left open for the owner (PS:5194).
3. **D2 (dynamic) is ruled for one act only: the scan contract** (a source is read for every parameter whatever slug found it). "Dynamically" otherwise has no owner gloss; the only standing owner text on the subject says most research acts are judgment acts, not automation (C-19).
4. **D1 (omnidirectional) rests on three thin legs:** an antagonist finding the ledger adopted ("a walk may re-enter any stage"), one clause of a 2026-10-09 commission ("flexibility of pipeline all directions"), and relayed 2026-10-12 statements that are not in the ledger. Exactly **one** mid-pipeline cold entry is described by the owner (evidence onward, "without research"). Entry at judgment, synthesis, specification or render is described nowhere; section 3's interface for those entries is inference and is marked so.
5. **The pipeline contract is forward-only and unratified.** `governance/pipeline-contract.yaml` declares `status: PROPOSED`, `ratified: false` (PC:2-3), gives each stage one forward `entry:` condition and no backward one, and its synthesis and specification entries contradict the owner's stage order (C-11).

Counts are derived, never typed here: requirements `grep -c '^| REQ-' <this file>`; conflicts and gaps `grep -c '^### C-' <this file>`; owner decisions `grep -c 'OWNER DECISION REQUIRED — yes' <this file>`; acceptance tests `grep -c '^| AT-' <this file>`.

## 0.1 Conventions

| Short | File |
|---|---|
| PS | `references/project-standards.md` (the owner's append-only ledger) |
| PC | `governance/pipeline-contract.yaml` |
| RC | `governance/research-contract.yaml` |
| CM | `CLAUDE.md` |
| ME | `governance/mission-and-epistemics.md` |
| JP | `governance/jurisdiction-philosophy.md` |
| AP | `governance/audience-priority.md` |
| EA | `governance/evidence-architecture.md` |
| PO | `governance/pipeline-operations.md` |
| SM | `governance/stage-map.yaml` |
| DR19 | `decisions/DR-2026-08-19-research-restart-operative-instrument.md` |
| IG | `workplan/pipeline-state-graph/IDEAL-GRAPH.md` |
| RUL | `workplan/pipeline-state-graph/RULINGS.md` |
| MEM | `workplan/2026-10-30-ramp-spec-pages/owner-rules/` |
| OBJ | `transcripts/harness_4a95df3b/main.jsonl:4` (the owner's 2026-11-12 instruction; also `dossier/01-method-and-brief.md:5`) |

**Warrant classes**, because "the owner said" covers four different things in this repository:

- **OWNER** — the owner's words, quoted in the ledger or a transcript.
- **LEDGER** — text a session wrote in the ledger under an owner ruling (readings, ACTION lines, conditions). Binding where the entry says so; many carry `[ASSUMPTION]` marks the ledger itself calls unratified.
- **CONTRACT** — `pipeline-contract.yaml` or `research-contract.yaml` text. The pipeline contract is `PROPOSED`, `ratified: false`, `authored_by: Claude` (PC:2-4); the research contract is `OPERATIVE` (RC:44).
- **RELAYED / MEMORY** — owner statements reported by a session but not in the ledger (IG:11), or an assistant's memory note of owner direction (MEM). Not verbatim owner prose in the second case.
- **ASSUMPTION** — my inference. Each says what it follows from.

**Status:** `LIVE`, `SUPERSEDED by <ruling>`, `CONTESTED` (two live texts disagree and section 2 names which governs).

**Pointers.** A table or column name appears only to say where a requirement points. Every such name is `[POINTER, not evidence of capability]`, abbreviated **[P]**. I read DDL in `dossier/30-data-tables.md` for names only and drew no conclusion about what works.

**Claim grammar.** Every quote is `VERIFIED` (I read it at the cited line). Every requirement not classed OWNER/CONTRACT is `INFERRED` and says from what.

---

## 1. Requirements ledger

### 1.A Objective, spine and direction of travel

| ID | Requirement | Warrant (verbatim) | Source | Class | Serves | Binds | Status |
|---|---|---|---|---|---|---|---|
| REQ-001 | The pipeline can be run in all directions from any stage, dynamically, to research, adjudicate, synthesize, specify and render across many languages and jurisdictions. | "ensure that our pipeline can be run in all directions at any stage in such a manner where we can dynamically research, adjudicate, synthesize, specify and render across a multitude of languages and jurisdictions" | OBJ | OWNER | D1 D2 D3 D4 | all | LIVE; not yet in the ledger (C-18) |
| REQ-002 | There are seven stages in one ruled order, and `base` is the first. | "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications."; "base is a stage insofar as it supplies the base information upon which research can perform its task" | PS:1454-1455; PS:2302-2303 | OWNER | D1 D4 | all | LIVE; supersedes the five-stage ruling of 2026-08-25 (PS:1457) |
| REQ-003 | A run re-enters stages; stage order is not write order; a re-entered stage still holds only its own facts. | "A walk may re-enter any stage; each stage's tables still carry only their own facts (rule 5)."; "A walk **re-enters** stages rather than passing through them once — digesting a reasoning document produced research leads, a backward edge, and that is normal." | PS:1048-1049; CM:260-261 | LEDGER (adopting an antagonist finding of 2026-08-21); Layer 0 | D1 | all | LIVE; no owner quote states it (self-attack 1) |
| REQ-004 | Flexibility in all directions is a property to be interrogated of every gate, read, write and conditional, not only of the stage order. | "Interrogate quality, logic, sequencing and flexibility of pipeline all directions as well as all gates, reads, writes, conditionals." | PS:4385 | OWNER (a commission to a critic, 2026-10-09) | D1 D4 | all | LIVE |
| REQ-005 | Every table that carries a reference or an id is walkable to and from the spine; handshakes hold in every direction. | "we need to ensure handshakes both top-down and bottom-up, and we need to ensure walkability across all tables with references and ids"; "handshake ALL directions" | IG:11 (O7, O8) | RELAYED 2026-10-12; "none is in the ledger yet" (IG:11) | D1 D4 | all | LIVE but unrecorded (C-18) |
| REQ-006 | Every pair of stages has a path, and a registered gate fails when one does not. | "Yes, register it"; ledger: "is registered as the stage-pair gate, by one registry entry that fails when a stage pair has no path" | PS:4731; PS:4761 | OWNER; LEDGER | D1 D4 | all | LIVE |
| REQ-007 | A run can start at `evidence` with sources already held and proceed forward, skipping discovery searching only. | "please create a new skill in its place called /run-pipeline (which includes a variant for processing evidence and beyond without research)" | PS:4947 | OWNER | D1 D2 | evidence → render | LIVE; the only cold entry the owner names |
| REQ-008 | Data can be reworked at any stage while the evidence chain stays auditable. | "every pipeline stage needs rigorous, portable, transparent data management so the data can be reworked at any stage and the evidence chain stays auditable" | MEM `project-end-goal.md:15` | MEMORY (assistant's note of owner direction, not verbatim) | D1 D4 | all | LIVE as a note; thin (self-attack 2) |
| REQ-009 | The owner can open any table, review and edit a value, and have the change propagate to whatever depends on it. | "I need there to be some kind of interface where I can manually review and edit the different table values/information and have it propagate accordingly. At the moment, everything in the database is opaque to me." | PS:4580 | OWNER | D1 D2 D4 | all | LIVE; "edit" and "propagate" carry unratified readings (PS:4586) |
| REQ-010 | Hand-offs fan out from research to judgment and fan in from judgment to specification. | "research produces many rows of evidence from one slug. each row of evidence provides one row for judgment. one-to-many rows of judgment provide one row for syntheses. one-to-many rows of syntheses provide one row for specifications." | PS:1538-1540 | OWNER | D1 D4 | research → specification | LIVE except the second sentence: SUPERSEDED by REQ-011 (PS:1847) |
| REQ-011 | Evidence to judgment is one-to-many and must never be constrained to one-to-one. | "one evidence source may provide many rows of judgment (eg a code document like Canada's NBC 3.8)" | PS:1845; PC:163-167 | OWNER; CONTRACT | D2 D4 | evidence ↔ judgment | LIVE |
| REQ-012 | The stage that consumes writes the link to what it consumed; an upstream row is never rewritten to record downstream use. | "The junction is written by the *downstream* stage as it creates its own item: *"this synthesis drew on these judgments."* Every stage still writes only its own tables." | PS:1557-1558 | LEDGER (session reasoning under the hand-off ruling) | D1 D4 | all boundaries | LIVE; decisive for backward travel and not an owner quote (self-attack 3) |

### 1.B Pointers, traceability and verification (D4)

| ID | Requirement | Warrant (verbatim) | Source | Class | Serves | Binds | Status |
|---|---|---|---|---|---|---|---|
| REQ-013 | No fact is written into a second table; a cell points to another cell. | "It is better to have a table cell point to another table cell than to rewrite." | PS:874-875 | OWNER | D4 | all | LIVE |
| REQ-014 | Any table's information can be called up from any other through a shared reference identifier. | "So long as each table has a row with a column that shares the same reference identifier, then you can call up information from any one so long as you point to the correct table and column." | PS:870-872 | OWNER | D1 D4 | all | LIVE |
| REQ-015 | A stage holds only its own stage's data; a later stage reaches earlier data by reference ID, and a citation is looked up in evidence, not carried. | "Reference IDs carry from table to table across stages. Data relevant in one stage does not cross to another stage."; "For rendering a citation, then, we point towards the evidence table for that reference ID." | PS:898-899; PS:902-903 | OWNER | D4 | all | LIVE |
| REQ-016 | Every boundary has an explicit contract whose conformance can be checked and whose exchange can be followed backward and forward. | "EVERY handshake / contract / handoff / exchange / input-output MUST be **verifiable** (you can mechanically check the contract held) AND **traceable** (you can follow provenance backward and forward across the boundary)."; "Is the underlying data verifiable (clean data) and the methodology declared (transparent methodology)?" | MEM `contract-traceability-invariant.md:10`; ME:181 | MEMORY; doctrine (CANONICAL) | D4 D1 | all boundaries | LIVE; the strong form is a memory note (self-attack 2) |
| REQ-017 | A view that joins stages is the pointer; views are assigned to stages and counted in walkability. | "Yes, map views to a stage"; "A cross-stage view IS the pointer, and is therefore the most protected object in the schema." | PS:4729; CM:255 | OWNER; Layer 0 | D1 D4 | all | LIVE |
| REQ-018 | Data rows and identifiers are retired in place, never hard-deleted. | "retire in place then" | PS:3540 | OWNER | D4 D1 | all | LIVE |
| REQ-019 | An identifier the permanent record has used is never issued again. | "An identifier the permanent record has already used is spent, whatever the live tables say." | PC:71-72 | CONTRACT | D4 | base, evidence, specification | LIVE |
| REQ-020 | Every reader that could surface a retired row filters on its status. | "**No row is retired in place until every reader that could surface it filters on status**" | PS:3575-3576 | LEDGER (execution condition of REQ-018) | D4 | all readers, render most | LIVE |
| REQ-021 | Each operation leaves a row saying it happened, so "not done" and "done, nothing found" are different states. | "Each operation must leave a row saying it happened, so that "not done" and "done, nothing found" are distinguishable states rather than the same absence."; "KEEP EMPTIES - a zero-yield search is a COMPLETED unit of work." | PO:81-82; RC:188-189 | doctrine (PO is `PROPOSED`, PO:3); CONTRACT | D4 D2 | research, evidence, judgment | LIVE |
| REQ-022 | A retrieval is persisted as where it was found (URL, and page or line where needed); the file itself need not be committed. | "we don't need to actually commit these large PDFs etc. we just need to log where we retrieved from ie the url"; "just record page number and line if need be too" | PS:5126; PS:5132 | OWNER | D4 D3 | research, evidence, base | LIVE; narrows CM:345 "persists every payload" (C-15) |
| REQ-023 | Bibliographic fields are written from the retrieved payload, never from memory. | "Never write a bibliographic field from memory when a payload is in hand." | CM:347 | Layer 0 | D4 D3 | evidence | LIVE |
| REQ-024 | No `stated` or `provisional` determination exists without at least one governing source link. | "No `stated` or `provisional` determination without at least one `specification_source_links` row with role `governing` (anti-hallucination)" | PC:244-245 | CONTRACT | D4 | specification | LIVE |
| REQ-025 | A determination is computed, reproducibly, from its inputs; the same evidence under the same rule version gives the same answer. | "oh. you have to compute it. I can't handle this load manually. you need to repair this and anything else"; "same evidence + same `rule_version` ⇒ same state and same `derivation_sha`" | PS:2690-2691; EA:116 | OWNER; doctrine | D2 D4 | specification | LIVE; supersedes DR19 §12.5 "permanently manual" for `specifications` only (PS:2693) |
| REQ-026 | Evidence is either recorded in the library or it is not evidence; nothing relied on sits outside it. | "how on earth do we have evidence outside the library? we either have evidence or we do not have evidence. our library is just what we have recorded" | PS:4834 | OWNER | D4 | evidence, render | LIVE |

### 1.C Dynamic, on-demand operation and the named backward edges (D2, D1)

| ID | Requirement | Warrant (verbatim) | Source | Class | Serves | Binds | Status |
|---|---|---|---|---|---|---|---|
| REQ-027 | Every admitted source is read against the whole parameter catalogue, whatever slug found it. | "note that while we search by slug, we scan each source for any and all applicable parameters."; "Slugs guide our searches, but they do not guide what we derive and mine from sources!" | PS:4381; PS:4385 | OWNER | D2, lateral | evidence, judgment | LIVE |
| REQ-028 | The record of a source lists every category, topic and parameter found in it, finds equivalencies to prevent duplication, and carries all bibliographic data. | "every research row for a source must list all different categories/topics/parameters found within that source … while ensuring that equivalencies are found to prevent duplication. all relevant bibliographic data must be recorded." | PS:4985 | OWNER | D2 D3 D4 | research, evidence | LIVE |
| REQ-029 | The parameter catalogue can be added to and expanded whenever new information requires it. | "Ensure that we can add and expand parameter catalogue as required based on new information we come across." | PS:4385 | OWNER | D2; backward edge evidence/judgment → base | base, evidence, judgment | LIVE |
| REQ-030 | A figure from a source filed under another slug may set a value, tagged for follow-up; a skimmed value may not be published. | "D1: yes figure from source filed by another slug allowed. skimmed values are not publishable" | PS:4396 | OWNER | D2, lateral | judgment, specification | LIVE; "skimmed" = `extraction_method = 'skim'` ruled PS:4759 |
| REQ-031 | A search may be recorded for a parameter or a mined source with no slug. | "**R43 Searches without a slug.** … a CHECK requires that a search says what it is for"; owner: "no idea what these are, but resolve them for me in a logical manner" | RUL:305; PS:4425-4444 | LEDGER (owner-delegated resolution) | D2 | research | LIVE; overridable by a later owner statement (PS:4439) |
| REQ-032 | Research crosses every topic with every lens; applicability is found, not presupposed. | "Every research slug gets cross-referenced against a population code, access need or ICF code because there is always the chance that there is an unexpected connection between them." | PS:943-945 | OWNER | D2 D3 | research, judgment | LIVE for the cross-product; "applicability is an OUTPUT of synthesis" is SUPERSEDED by the 2026-08-27 ruling (PS:2040-2042): the crossing is judgment's output |
| REQ-033 | Concept vocabulary is observed at evidence, verbatim and unjudged, and adjudicated at judgment. | "overrule Aug 24 DR. we go evidence>judgment>synthesis."; "listing out all concepts/topics/key words/phrases that appear in the source and then judgment phase will actually do the deep read on it" | PS:2002; PS:2004-2007 | OWNER | D2 D3 | evidence, judgment, base | LIVE for evidence-stage reading; for base vocabulary SUPERSEDED by REQ-060 (PS:5192) |
| REQ-034 | No container states its own answer; a parameter name carries no value and is not an old item code. | "parameter at base, archive prior corpus so it can't be found by tools we use commonly, use add-term for now"; "No base_parameters row points at a terms.canonical_en that itself states a determination (a digit, a comparator, or a min/max word)." | PS:2629; PC:53-54 | OWNER; CONTRACT | D2 | base | LIVE |
| REQ-035 | Sources already held are read before more are fetched. | "Yes, read what we hold first" | PS:4683 | OWNER | D2 | research, evidence | LIVE |
| REQ-036 | A deferral is legitimate, and it must eventually run. | "deferred is okay so long as it runs eventually" | PS:3737 | OWNER | D2 D4 | research; by extension every owed act | LIVE; the ledger records that nothing measures the obligation (PS:3761-3764) |
| REQ-037 | A skimmed finding supplies nothing to a determination; it cues a dedicated reading. | "no. skimmed findings cue tools for a dedicated pass." | PS:4472 | OWNER | D1 backward edge specification → evidence/judgment | specification, judgment, evidence | LIVE |
| REQ-038 | A provisional reading sends work back to its source for re-reading and confirmation. | "provisional means that we have to go back and review the source again to confirm information accuracy" | PS:4833 | OWNER | D1 backward edge specification/render → evidence | specification, evidence | LIVE; changes what `provisional` means against ME:116 (C-24) |
| REQ-039 | Where a study reports no change, backward citation mining and context find the values it tested; if they cannot be found the source has no value. | "This is why we use backwards citation mining and contextual clues. If we are unable to find the actual parameters/values under discussion, then the source itself has no value." | PS:4723 | OWNER | D1 backward edge judgment → research | judgment, research | LIVE |
| REQ-040 | A cell without evidence is a recorded gap, and an open gap is an entry to research. | "an OPEN gap or an item/parameter lacking sufficient evidence"; "`[BEST-PRACTICE-PENDING]` + gap link" | PC:107; ME:117 | CONTRACT; doctrine | D1 backward edge specification → research | specification, research | LIVE; which stage owns `gaps` is disputed (C-22) |
| REQ-041 | Research coverage is set up from the base, not kept beside it. | "we set up the base and in turn we set up the research coverage" | PS:5088 | OWNER | D2 D3; edge base → research | base, research | LIVE |
| REQ-042 | Technique categories and building typologies or rooms show the same criteria in both directions. | "what appears in a category specification for type (eg circulation, acoustics) will appear in building typologies and rooms and vice versa" | PS:5076 | OWNER | D1 lateral | base, render | LIVE; `rooms` are frozen "until a page reads them" (PS:5056) |
| REQ-043 | Synthesis cross-references rows to find links across parameters, topics and categories. | "synthesis will ensure the use of cross referential analysis for table rows to see if there are any relevant links within parameters/topics/categories (eg wheel chair swept path analyses for different wheel chairs would inform different space requirements)" | PS:4989 | OWNER | D1 lateral | synthesis | LIVE |
| REQ-044 | Evidence is stored so it can inform synthesis and specification and can be used directly by render. | "the evidence needs to be stored in such a manner where it can be used to inform synthesis+specifications as well as be able to be used directly by rendering." | PS:4987 | OWNER | D1 non-adjacent forward edge evidence → render | evidence, render | LIVE |
| REQ-045 | A page for an element is derived from the live determinations of its parameters and is never a container rows are filed into. | "Yes, derive it — This derivation is what I expect the specifications pass to be doing--adjudicating, deriving and synthesizing across rows of related evidence." | PS:4679 | OWNER | D2 | specification, render | LIVE; OR-14b open (PS:4695) |
| REQ-046 | A question that is the owner's stops the run and is put as a prompt with full context; a saved answer binds nothing until the ledger quotes it. | "waiting on me decisions need to be prompts with full context" | PS:4598; PS:4602 | OWNER; LEDGER | D2 (what a stage must refuse) | all | LIVE |
| REQ-047 | An item no route reaches is given up for now, with a typed disposition, and is not queued. | "if we can't access something from anywhere then we have to give up on it for now" | PS:3980 | OWNER | D2 D4 | research, evidence | LIVE |
| REQ-048 | Research tracks its queries; a zero-yield search says why. | "must be performed by topic across languages and jurisdictions while tracking its queries"; "say query-shape failure vs wrong index vs genuine absence." | PS:4985; RC:281-282 | OWNER; CONTRACT | D4 D3 | research | LIVE |
| REQ-049 | Confirmed T1–T2 anchors are mined backward and forward; T4–T6 sources are not mined backward. | "Mine every CONFIRMED T1-T2 anchor backward AND forward."; "We don't need to mine backwards for T4 to T6--whatever is given to us by them is what we accept as a matter of fiat." | RC:79; PS:4719 | CONTRACT; OWNER | D1 edge evidence → research | research, evidence | LIVE |
| REQ-050 | Every admission has a logged search behind it, including a source taken from a list or already held. | "Every admission has a logged search behind it. A source taken from a list is logged as one … a held source with no edge gets one" | RC:341-344 | CONTRACT | D4; governs the cold entry of REQ-007 | research, evidence | LIVE |
| REQ-051 | No admission without re-retrieval; a source that cannot be retrieved cannot be top tier and reads ○. | "No re-retrieval = no admission."; "if we can't retrieve a study, then we can't verify it as a primary source, which means that we can't claim it as a top tier." | RC:216; PS:4540 | CONTRACT; OWNER | D4 | evidence, specification | LIVE; anchoring by an unretrievable source needs "a valid academic route" (PS:4725) |
| REQ-052 | The Co-1 / T2 / Co-2 pass runs first, in native-language terms. | "Co-1 / T2 / Co-2 pass FIRST - no exceptions (Co-1 co-primary w/ T1, CRPD 4.3)" | RC:64 | CONTRACT | D3 | research | LIVE |

### 1.D Languages and jurisdictions (D3)

| ID | Requirement | Warrant (verbatim) | Source | Class | Serves | Binds | Status |
|---|---|---|---|---|---|---|---|
| REQ-053 | Research is performed by topic across languages and jurisdictions. | "research: must be performed by topic across languages and jurisdictions while tracking its queries." | PS:4985 | OWNER | D3 | research | LIVE |
| REQ-054 | The base tables work across every language defined for this edition (P1+P2+P3). | "these base tables, as per our aliases and native terms and translations and multilingual and multijurisdictional requirements etc, must work across all languages that we have defined for this current edition of project (the p1+2+3, I think it's called, for the initial countries to focus on)" | PS:5011 | OWNER | D3 | base | LIVE; set membership is an `[ASSUMPTION]` (PS:5026; C-06) |
| REQ-055 | The project is international without English bias: English does not decide which concepts exist or how they are described. | "such that we have a truly comprehensive international project without English bias"; "we are trying to avoid english BIAS" | PS:5019; PS:5206 | OWNER | D3 | base, research, and by extension all | LIVE |
| REQ-056 | A concept first met in another language may carry an English label of ours, kept apart from any attested English form. | "you obviously can have English words for these rows." | PS:5204 | OWNER | D3 | base | LIVE; narrows how E1 and OR-17 were applied (PS:5211) |
| REQ-057 | A concept is an equivalence class of forms per language and jurisdiction; equivalence-finding applies to every term; conflation is expected. | "this kind of equivalency finding is applicable for all terms researched"; "there is a lot of conflation in literature" | PS:5154; PS:5162 | OWNER | D3 | base, research, evidence | LIVE |
| REQ-058 | Every phrase, name and alias is attested in its own jurisdiction and language; the model generates none; nothing is back-translated. | "Ensure that these phrases/names/aliases are all present in their prescribed jurisdiction/language. It is not acceptable for the model to generate its own phrases/names/aliases."; "No back-translation. Every alias carries its in-language source, else [UNVERIFIED-TERMS]." | PS:4713; RC:227-228 | OWNER; CONTRACT | D3 D4 | base, research | LIVE |
| REQ-059 | A translation of the English register is a search seed, flagged, and is produced as terms actually in use in the jurisdiction. | "so we are doing prep work to get this all written out in English and then we have to translate it all properly into other languages to search them too"; "With that said, I expect that the model will be using real terms that are actually in use within a jurisdiction." | PS:5082; PS:4675 | OWNER | D3 | base, research | LIVE; "search seed, never vocabulary" is the ledger's reading the owner answered "yes" to (PS:5086-5088) |
| REQ-060 | The base grounds itself: a base cell records where its form was found and needs no admitted evidence source; the base is accepted when coverage across languages and jurisdictions is confirmed correct. | "none of the work in base needs to be verified and stored in evidence."; "base grounds itself."; "so long as we can confirm that we have correct coverage, we are fine" | PS:5182; PS:5184; PS:5188 | OWNER | D3 D4 | base | LIVE; supersedes the observation route for base vocabulary (PS:5192) |
| REQ-061 | The register does not end where English ends: concepts met in native-language readings enter under the instrument's own phrase. | "you have to ensure that you research them across all of our chosen jurisdictions and languages without an English bias"; "A concept first met outside English is named by the instrument's own phrase, in its own language" | PS:5080; PS:5049 | OWNER; LEDGER (E1, applied on "e1 e3 e4; Appy yes", PS:5042) | D3; backward edge evidence → base | base, evidence | LIVE |
| REQ-062 | Exhaustion and coverage are judged per parameter per bucket member, and a bucket member is a jurisdiction with its associated language. | "Yes, per parameter and bucket so long as the bucket is not just jurisdiction but associated language." | PS:4655 | OWNER | D3 D2 | base, research | LIVE; supersedes "distinct axes" for exhaustion (C-05) |
| REQ-063 | Research stays inside the in-scope jurisdictions until they are categorically exhausted for the subject. | "Standing order: do not research from countries other than Bucket 1 and Bucket 2 for any slug until those buckets are categorically exhausted."; "do not include countries outside of the major identified countries for now" | PS:4295-4297; PS:4835 | OWNER | D3 D2 (a refusal) | research, render | LIVE; membership contested (C-06) |
| REQ-064 | Languages scoped out are not owed until the in-scope set is exhausted. | "Yes, scope them out for now" | PS:4673 | OWNER | D3 D2 (a refusal) | base, research | LIVE |
| REQ-065 | Every jurisdiction value resolves to the declared vocabulary; `UK` never `GB`; a work spanning jurisdictions is `INT`, distinct from `ISO`; admitting a code is a scope decision. | "UK is canonical, add BE HR INT ES IT to the enum"; "Every jurisdiction value resolves to the declared vocabulary."; "admitting a code silently converts a candidate jurisdiction into a declared one, and that is a scope decision" | PS:3687; PC:48; PS:3714-3715 | OWNER; CONTRACT; LEDGER | D3 D4 | base and every table carrying a jurisdiction | LIVE; the vocabulary's home is an enum in code (C-08) |
| REQ-066 | Non-English peer-reviewed work is academic; absence from an English-language index is not a quality fact. | "Non-English peer-reviewed work is ACADEMIC, not grey. Non-indexation in PubMed/Scopus is an INDEXING fact, not an evidence-quality fact." | RC:127-128 | CONTRACT | D3 | evidence, judgment | LIVE |
| REQ-067 | Only the current state is researched and stated; history and superseded editions are not. | "We are interested in what are best practices NOW, and that means we do not need to interrogate the history of anything but rather the current state of everything" | PS:4826 | OWNER | D3 | research, evidence, specification | LIVE |
| REQ-068 | A value keeps the notation and unit its source wrote; both notations are presented; exact linear units are converted and both shown. | "Present both--don't choose between ratio or percentage."; "Yes, convert and show both — Round to nearest 1/4" or 5mm." | PS:3644; PS:4667 | OWNER | D3 D4 | judgment, specification, render | LIVE |
| REQ-069 | A page can show, for one parameter, what each in-scope jurisdiction has for the value, in one comparison table. | "for ramp gradient, i want there to also be an easy comparison master table where you just see what each jurisdiction has for the value" | PS:4844; AP:86 | OWNER; doctrine (jurisdiction-comparison use-pattern) | D3 | render, judgment | LIVE |
| REQ-070 | A language community's own designation for an identity may be recorded beside the English name when its own Co-1 sources attest it. | "The base may record each language community's own designation for an identity code, attested in its own Co-1 sources, beside the English name." | PS:5054 | LEDGER (E6, DG-NON, applied on "apply all recommendations", PS:5037) | D3 | base | LIVE; rests on a blanket approval the ledger marks as an assumption (PS:5046) |
| REQ-071 | A non-English source keeps its own bibliographic identity (original-language title and names) and states its language; nothing about it is recoverable only through an English rendering. | — | follows from REQ-023, REQ-028 ("all relevant bibliographic data must be recorded"), REQ-055 and PS:4993 ("must ensure proper bibliographic citations") | ASSUMPTION | D3 D4 | evidence, render | no owner sentence states it (self-attack 4) |

### 1.E Lenses and the determination's key

| ID | Requirement | Warrant (verbatim) | Source | Class | Serves | Binds | Status |
|---|---|---|---|---|---|---|---|
| REQ-072 | A determination is keyed on the design parameter and at least one of four lenses. | "The judgment object is the **canonical parameter**"; "it is OKAY for a link to be absent in a related taxonomy column", "but a link MUST be tied to at least one", "and ideally it ties into many" | PS:1317; PS:2554-2556 | LEDGER recording an owner selection; OWNER | D4 D2 | judgment, specification | LIVE |
| REQ-073 | Every relevant model is filled on a determination and on the figures under it; never only one. | "a determination should never be limited to only one lens because we have different models for discussing disability (ICF, population identity, access needs)--we need to have each model filled out accordingly." | PS:4614 | OWNER | D4 | judgment, specification | LIVE |
| REQ-074 | No row is stored, and none is shown, for a lens the parameter is not relevant to. | "Do not store table rows for parameters when there is a missing lens for a disability population or access need, i.e. for when the parameter is not relevant."; "we do not need to have rows for people where the value is just "Not set." that just means that it shouldn't be showing on the page" | PS:4614; PS:4845 | OWNER | D2 D4 | specification, render | LIVE; supersedes stored `not_applicable` (C-13) |
| REQ-075 | The reader chooses the model; the medical model is offered and never stands alone on a determination. | "yes we include the medical model too. we give our users the choice of what model they want to use to browse the site."; "No determination is keyed on medical_code alone." | PS:1935-1936; PC:264 | OWNER; CONTRACT | D1 lateral | base, specification, render | LIVE |
| REQ-076 | Several codes of one model on one figure are carried by a link table, not by repeating the figure. | "link table unless that is more prone to errors" | PS:4926 | OWNER | D4 | judgment | LIVE; the condition is met by a measurement the ledger marks as an assumption (PS:4934) |
| REQ-077 | A figure tagged for everyone reaches only a determination for everyone. | "No, ALL reaches only an ALL determination" | PS:4657 | OWNER | D4 | judgment, specification | LIVE |

### 1.F Stage content the request must be able to reach

| ID | Requirement | Warrant (verbatim) | Source | Class | Serves | Binds | Status |
|---|---|---|---|---|---|---|---|
| REQ-078 | Judgment delivers the tier verdict and the extracted value, and grades the population studied against the population served. | "delivers a verdict on an evidence item for what tier of evidence hierarchy it belongs to (1, 2…6)"; "Grade population-of-STUDY vs population-SERVED on every admission." | PS:1885-1886; RC:270 | OWNER; CONTRACT | D4 | judgment | LIVE; the tier is still stored on the evidence row, a move the ledger records as "Queued, not done" (PS:1909-1914) |
| REQ-079 | A reading is verified only on a recorded full-scope reading; a source is covered only when read, extracted and verified. | "Yes, require a full-scope scan"; "...covered means that the source that has been listed in the database has been read and had information extracted from it then verified" | PS:4669; PS:4832 | OWNER | D4 | evidence, judgment | LIVE |
| REQ-080 | Convergence counts independent roots, never documents or jurisdictions; divergence is shown, never suppressed. | "Convergence counts INDEPENDENT evidence axes … never document/citation count."; "A synthesis that suppresses divergence is in error." | PC:172-173; ME:132 | CONTRACT; doctrine | D4 D3 | synthesis | LIVE |
| REQ-081 | Specification reviews all evidence and syntheses and names the most accommodating value, never the commonest; code is a floor unless backed by high-value evidence. | "specifications: must be able to review all evidence and syntheses of evidence to determine what best practice is, which explicitly means the most accommodating/gentle/dignified set of values/rationales/solutions for a given specification item within a category. the most commonly seen value/etc is NOT evidence of best practice but most common practice." | PS:4991 | OWNER | D3 D4 | specification | LIVE |
| REQ-082 | A determination resting on codes alone is best practice at the weak band, flagged, never `stated`. | "if code documents are the only things that inform a specification, then they can be best practice...it's just going to be a weaker evidence tier"; "Yes, keep the ○ band and flag" | PS:4997; PS:4873; PC:252-254 | OWNER; CONTRACT | D4 | specification, render | LIVE |
| REQ-083 | Render reads the database; no committed file is a render and the site does not rely on built artefacts. | "i want it to be coming from database directly in ideal world"; "the entire pipeline is dynamic rendering on site"; "do not rely on artifacts for rendering the site" | PS:4840; PS:1658-1659 | OWNER | D2 D4 | render | LIVE |
| REQ-084 | The render table holds specification rows converted into complete prose with bibliographic information drawn from the preceding tables. | "I expect the rendering to occur on the basis of whatever specification has been synthesized accordingly, and I expect the render table to be one where the specification table rows have been converted into complete prose, bibliographic information etc accordingly from the preceding tables such that it can be displayed properly on the website repository." | PS:4729 | OWNER | D1 D4 | render | LIVE; supersedes "render's hand-off is not a table" (C-01); production and storage open (OW-1b, OW-1c) |
| REQ-085 | Render presents and does not claim correctness; it compiles all evidence in tables for comparison and cites properly. | "i want to be as radically transparent for my audience as possible while simply PRESENTING information without claiming correctness myself"; "renders: must be able to process specifications to be readable for a webpage, must be able to compile all evidence in tables for comparison, must be radically transparent in approach, must ensure proper bibliographic citations, etc." | PS:4888; PS:4993 | OWNER | D4 | render | LIVE |
| REQ-086 | A page offers an audience lens and a disability lens, and the filters come before the information. | "There is an audience lens (the four audiences) and a disability lens (population, ICF, access needs)"; "the filters have to precede the information" | PS:4841; PS:4843 | OWNER | D1 lateral | render | LIVE |
| REQ-087 | Every rendering of a cell carries the identical determination tuple in every register. | "Every rendering of a cell carries the identical determination tuple across registers" | PC:285 | CONTRACT (the contract itself says `UNENFORCED`, PC:287) | D4 | render | LIVE |
| REQ-088 | Rendered work meets web accessibility standards; compliance is never self-certified. | "note: all work must comply with website accessibility standards and best practices" | PS:4847; PS:4860 | OWNER; LEDGER | — (constraint on render) | render | LIVE |
| REQ-089 | Every specification carries a marker; unmarked is an error. | "Every specification sentence carries a marker … Unmarked = error." | PS:26 | OWNER (Core Doctrine) | D4 | specification, render | LIVE |

### 1.G Constraints that bind any run in any direction

| ID | Requirement | Warrant (verbatim) | Source | Class | Serves | Binds | Status |
|---|---|---|---|---|---|---|---|
| REQ-090 | The database is written only through migrations. | "ALWAYS: migrations-only (emit_data_migration -> migrate_db). Never hand-edit the DB." | RC:351 | CONTRACT | D4 | all | LIVE |
| REQ-091 | Research rows and tooling ship in separate changes; a writer gap found mid-run is filed, not patched. | "Research data (rows, or a data migration) and tooling (schema, scripts, checks, governance prose) ship in separate changesets -- never both in one" | PC:332-333; CM:201 | CONTRACT; Layer 0 | D2 (a limit on it) | all | LIVE |
| REQ-092 | Code is the minimum that performs the action correctly; one value per cell; each fact in the cell that names it; more columns over joined cells. | "tables and columns must be as clearly organized as possible. we do NOT want to have data joined in cells that will cause issues further down the pipeline or have data stored in the wrong cell"; "more columns = more specificity = more flexibility imo" | PS:4963; PS:4965 | OWNER | D4 D2 | all | LIVE |
| REQ-093 | A fact the machine can compute is derived, never curated beside the thing it describes; where judgment is needed the script asks for it and records the warrant. | "DERIVE IT, OR NAME WHO JUDGED IT. Never curate a fact the machine can compute."; "The model fills a field. It never invents a value, never invents a vocabulary term, and never supplies a number the schema could have computed." | CM:153; CM:162-163 | Layer 0 | D2 D3 | all | LIVE |
| REQ-094 | A pipeline run ends with an adversarial audit of accuracy, logic and sequence. | "followed by doing an adversarial audit for accuracy, logic, sequence" | PS:4979 | OWNER | D4 | all | LIVE |
| REQ-095 | Each stage boundary emits an adherence record, and a doctrine recheck fires at every stage transition. | "Each stage boundary emits `[ADHERENCE-LOG — stage N: <name>]`"; "A doctrine recheck fires at every stage transition and every 25 sessions" | PC:301; PC:321 | CONTRACT (`PROPOSED`) | D4 | all boundaries | LIVE as contract text; written for a forward walk (section 3.9) |
| REQ-096 | Best-practice synthesis prose is authored at the Opus floor. | "best_practice_synthesis is authored at the ratified capability floor (Opus-class), never by a lower tier" | PC:232-233; RC:352 | CONTRACT | — (constraint on D2) | synthesis | LIVE |

---

## 2. Owner-prose conflicts and gaps

Ranked worst first for the objective. "Governs" applies rule 0: the later owner statement wins on contact, and the conflict is reported, not weighed.

### C-01 What render's hand-off is
- **A.** "the entire pipeline is dynamic rendering on site", "do not rely on artifacts for rendering the site" (PS:1658-1659, quoted from the header of a 2026-08 migration); the ledger concluded "**render's hand-off is not a table**" (PS:1667).
- **B.** "I expect the render table to be one where the specification table rows have been converted into complete prose, bibliographic information etc accordingly from the preceding tables" (PS:4729, 2026-10-29). "i want it to be coming from database directly in ideal world" (PS:4840, 2026-10-30).
- **Governs:** B. There is a render table, in the database. A and B agree if the site reads that table. The ledger's "not a table" sentence and IG K31 ("render's hand-off is not a table") are superseded.
- **Still open, recorded by the ledger as the owner's:** how the prose is produced (OW-1b) and whether the table is stored or rebuilt (OW-1c) (`governance/owner-browser.yaml:913-957`). Until both are answered the specification → render boundary has no ruled postcondition and no ruled pointer shape, and every backward edge from render (staleness, re-derivation) is undefined.
- **OWNER DECISION REQUIRED — yes** (OW-1b, OW-1c).

### C-02 What "render across a multitude of languages" means
- **A.** OBJ: "render across a multitude of languages and jurisdictions".
- **B.** No other owner statement says what language a page is rendered in. The only adjacent text is the open question "whether and by whom a source's sentence may be translated or rewritten" (PS:4897, OW-1b's residue) and ME:27's four audiences with no language named.
- **Two readings, different pipelines.** (i) Pages are in English and render evidence that originates in many languages, each source cited in its own language. (ii) Pages are produced in several reader languages. Reading (ii) needs language-neutral identity for determinations, register text and base labels, an attested (not model-generated) target-language vocabulary under REQ-058, and a ruling on translating quotes. Reading (i) needs REQ-071 and a ruling on whether a quoted sentence is shown in the original, in translation, or both.
- **Governs:** nothing; the prose is silent.
- **OWNER DECISION REQUIRED — yes.**

### C-03 What "jurisdiction" keys, and whether a determination varies by it
- **A.** The determination's key is ruled: parameter × at least one lens (REQ-072). No jurisdiction is in it. Best practice is "the most accommodating/gentle/dignified set of values" found (PS:4991), which is jurisdiction-neutral, and "Where evidence-based best practice exceeds code, the guidebook specifies the evidence-based value and notes the code value as the regulatory minimum" (ME:149).
- **B.** OBJ asks to "specify … across a multitude of … jurisdictions". AP:86 names a policymaker pattern, "What do other jurisdictions do for this provision? Why?", and PS:4844 asks for a per-jurisdiction comparison table.
- **Reading applied in section 3 (ASSUMPTION):** jurisdiction is a property of sources, extracted figures, searches, code leads and vocabulary forms; a determination is one per parameter × lens across jurisdictions; "specify across jurisdictions" is met by the jurisdiction spread and the code-versus-best-practice delta at render. If the owner means a determination per jurisdiction, the key ruled on 2026-08-26/28 changes.
- **Sub-gaps the prose leaves open:** what a jurisdiction is below the country (the owner's waiting list names "sub-national instruments", PS:4938); what `INT`, `ISO`, `EU`, `UN` are when a request names a country; whether a jurisdiction's identity includes the edition in force (REQ-067 says current editions only; JP §3 tracks currency per standard).
- **OWNER DECISION REQUIRED — yes** (confirm the reading; rule on sub-national instruments).

### C-04 What a concept's language-neutral identity is
- **A.** "we are trying to avoid english BIAS" (PS:5206); ledger reading: "English is one column of the matrix among the others and is not read first, matched first or ranked first" (PS:5210, marked unratified).
- **B.** The parameter's name is reached through an English-named term, and the contract's base criterion is written on it: "No base_parameters row points at a terms.canonical_en that itself states a determination" (PC:53-54). `terms.canonical_en` **[P]**.
- **The ledger says this is open and whose it is:** "**Consequences left open for the owner's schema decision:** … how a concept first met outside English is held (`terms.canonical_en` is required)" (PS:5194).
- **Governs:** the later statements (2026-11-06) govern intent: a concept's identity is the concept, with forms per language and jurisdiction, and English is a label. No ruling says how that is held.
- **OWNER DECISION REQUIRED — yes** (the ledger's own classification).

### C-05 Language and jurisdiction: two axes or one pair
- **A.** "Language and jurisdiction coverage are distinct axes — both satisfied independently." and "All 14 languages searched to completion on every run." (PS:123, PS:129; March 2026).
- **B.** "Yes, per parameter and bucket so long as the bucket is not just jurisdiction but associated language." (PS:4655, 2026-10-29); "Yes, scope them out for now" (PS:4673).
- **Governs:** B. The unit of coverage is the pair, and the set of pairs is scoped. The two March rules are superseded for exhaustion; no back-pointer marks them at PS:123/129. The number of languages is quoted three ways in the record (14 at PS:129, 19 in RC and the skills, and "the 14 languages `lang_jur_map` pairs with them" at PS:5026); none should be quoted. Derive: `python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(distinct language),count(*) from v_research_scope').fetchall())"` (run by the bottom-up leg; I did not open the database).
- **OWNER DECISION REQUIRED — no.** A supersession record is owed.

### C-06 Which jurisdictions are in scope
- **A.** JP:13 and JP §1.1: 24 countries plus two meta-codes, "Global South ≥8 jurisdictions" (JP §1.2), CANONICAL.
- **B.** "Standing order: do not research from countries other than Bucket 1 and Bucket 2 for any slug until those buckets are categorically exhausted." (PS:4295-4297, 2026-09-28), buckets listed at PS:4313-4314.
- **C.** "Yes it is P1+P2+P3" and "do not include countries outside of the major identified countries for now" (PS:4835, 2026-10-30); the P-set is recorded only as an `[ASSUMPTION]` (PS:5026).
- **B and C name different sets.** Derive, do not trust: `python3 -c "b=set('UN ISO CA US UK DE NO SE JP AU EU SG NZ IE FR ES PT FI NL KR'.split());p=set('US UK AU CA DE NO SE ISO EU FR CH NL DK FI BE IE ES IT PT JP SG NZ KR CN'.split());print(sorted(b-p),sorted(p-b))"` (lists typed from PS:4313-4314 with country names converted to codes by me, and from PS:5026).
- **The ledger itself records A against B as unresolved** ("NOT RESOLVED BY THIS RULING", PS:4315-4320).
- **Governs:** C over B (later); B/C over A for research now. Whether `UN` remains in scope, and the Global South tension, are not settled.
- **OWNER DECISION REQUIRED — yes** (jurisdiction scope is owner-gated, CM §8).

### C-07 Evidence from outside the in-scope jurisdictions
- **A.** "**Does not exclude other jurisdictions' evidence.** If Tier 1–3 clinical evidence comes from a non-canonical jurisdiction (e.g., Finland, Austria, Turkey), it is cited. The 24-jurisdiction requirement applies to code/standards research (Tier 4–6), not to clinical evidence." (JP:62).
- **B.** Owner: "do not research from countries other than Bucket 1 and Bucket 2" (PS:4295). The ledger's ACTION widens "research" to "Do not admit evidence from a jurisdiction outside buckets 1–2" (PS:4329-4330), which is the session's wording, not the owner's.
- **C.** "Yes, read what we hold first" (PS:4683), read as covering held sources "inside and outside buckets 1 and 2" (PS:4697). A memory note records the order of work as codes first, "then look for higher-tier evidence (T1-T3, any language, any jurisdiction)" (MEM `spec-page-requirements.md`, the "Jurisdiction scope" paragraph).
- **What cannot be avoided:** citation mining (REQ-049) of an in-scope T1 anchor will surface studies from out-of-scope countries. The prose does not say whether such a study is admitted, staged, or refused.
- **OWNER DECISION REQUIRED — yes.**

### C-08 "Adding a language or a jurisdiction is data, not code"
- **A.** The brief's D3 clause (`dossier/01-method-and-brief.md:11`), which the brief itself calls the assistant's decomposition.
- **B.** The owner's words place the jurisdiction vocabulary in code: "add BE HR INT ES IT to the enum" (PS:3687); the contract notes "the architecture note's base.jurisdictions, which has no table yet" (PC:49); and admitting a member is a scope decision (PS:3714-3715; CM §8).
- **Reading:** "data, not code" is supported by rule 8 (REQ-093) and by the base holding the language–jurisdiction pairs (`lang_jur_map` **[P]**), not by any owner sentence about jurisdictions. Mechanically a new member should be a row; its authorisation is always an owner ruling. A request for an undeclared jurisdiction is refused with a prompt (REQ-046), never auto-admitted.
- **OWNER DECISION REQUIRED — no** for the mechanism (tooling); **yes** for each admission, as now.

### C-09 Which stage assigns the lenses
- **A.** The crossing is judgment's output: "overrule Aug 24 DR. we go evidence>judgment>synthesis." (PS:2002), with the ledger's ACTION "the crossing is **judgment's output**" (PS:2041-2042); CM:365.
- **B.** "evidence stage must carefully adjudicate sources to assignrelevant populations/access needs/ICF codes properly referenced" (PS:4987, 2026-11-06). The same message lists research, evidence, synthesis, specifications and renders, and no judgment stage, although its first line gives all seven.
- **The ledger reads B as a collapse of evidence and judgment and marks the reading `[ASSUMPTION]`** (PS:4999).
- **Governs:** on the letter of rule 0, B is later. On the ledger's reading, A stands. This decides what a cold entry at evidence (REQ-007) must do before it hands on, so it cannot be left as a reading.
- **CONTESTED. OWNER DECISION REQUIRED — yes** (one sentence: confirm that "evidence stage" in the 2026-11-06 list means evidence and judgment together).

### C-10 No owner prose describes entry at judgment, synthesis, specification or render
- OBJ requires entry "at any stage". The prose describes forward entry at research (a slug, a gap), a cold entry at evidence (REQ-007), and the owner's editing entry at any table (REQ-009). Nothing describes a run that starts from a specification, a rendered cell or a synthesis and moves backward on purpose, except the four named backward edges (REQ-037 to REQ-040).
- **Consequence:** section 3's entries for those stages are my inference from the pointer rule and the hand-off cardinalities. They are the minimum those rules imply, not what the owner specified.
- **OWNER DECISION REQUIRED — no**, but the interface in section 3 should be put to the owner before anything is built on it.

### C-11 The pipeline contract contradicts the owner's stage order and is forward-only
- **A.** Owner: "synthesize judgments, specify syntheses" (PS:1454).
- **B.** PC:227-228, synthesis `entry:` "a determination with a resolved value, ready for cross-jurisdictional synthesis"; PC:239-240, specification `entry:` "a synthesis with a resolved value, ready for determination". A determination cannot be both the input to synthesis and the output of the stage after it.
- **Also:** every stage has exactly one `entry:` and it is a forward one; the research entry still names "an item" (PC:107); the evidence criterion is written on "BPC synthesis claim" (PC:122); the file is `PROPOSED`, `ratified: false` (PC:2-3) while CM §3 treats its `stages:` as the single home of the stage ids.
- **Governs:** A. The contract is what gets corrected.
- **OWNER DECISION REQUIRED — no** for the correction; ratification of the contract is the owner's.

### C-12 What a synthesis is, as an object a specification points at
- **A.** "one-to-many rows of judgment provide one row for syntheses. one-to-many rows of syntheses provide one row for specifications." (PS:1539-1540).
- **B.** The determination is computed from governing sources and extractions (REQ-024, REQ-025), and the owner describes the specification pass itself as "adjudicating, deriving and synthesizing across rows of related evidence" (PS:4679); "the critical methodology comes from synthesis/adjudication/specifications" (PS:4828).
- **Gap:** the prose names synthesis's work (cross-referential analysis, convergence, divergence) and never says what one synthesis row is for a parameter × lens, nor that a specification must point at it rather than straight at judgment rows. Whether the specification pass writes an element-level determination is already put to the owner (OR-14b, PS:4695).
- **OWNER DECISION REQUIRED — yes** (OR-14b, widened: is a synthesis row a required input to a determination).

### C-13 Absence of a row has three meanings and the prose stores none of them
- **A.** ME:118 keeps `not_applicable` as a state with "explicit rationale"; ME:120, "**Silence on evidence-thin populations is not the default.**"; ME:117, a pending cell shows `[BEST-PRACTICE-PENDING]` and a gap link.
- **B.** "Do not store table rows for parameters when there is a missing lens … i.e. for when the parameter is not relevant." (PS:4614); "we do not need to have rows for people where the value is just "Not set."" (PS:4845).
- **Governs:** B. But a dynamic request for a cell with no row must still answer one of: not relevant; relevant and not yet researched; researched and nothing found. The ledger's bridge is an `[ASSUMPTION]` ("the gaps table still records a missing figure for a lens that is relevant", PS:4630) and the page behaviour is recorded as "not settled" (PS:4861, item 9(a)).
- **OWNER DECISION REQUIRED — yes** (item 9(a), already on the record as unsettled).

### C-14 The two architecture documents for render describe a deleted model
- `architecture/navigation-modes.md` and `architecture/page-templates.md` (both `Status: ACTIVE`) route by `[item_code]`, query `jurisdictional_value` and `specification_population`, name `site/specs/e-08.html` as the exemplar, and define the markers as "● stated … ◐ provisional … ○ pending" (page-templates C-01; navigation-modes §6 rule 4).
- **Against:** the item layer is deleted (CM §7); the owner has ruled the E-08 page out repeatedly (PS:1603-1604); the markers mean confirmed, policy or standards only, and grey, thin or unverified (CM §6; PS:26; PS:4540).
- **Governs:** the later rulings. Both documents are listed as render's prose homes and will mislead any session that reads them as current.
- **OWNER DECISION REQUIRED — no.** They need a supersession mark or archiving.

### C-15 What "traced to the retrieved bytes" can mean
- **A.** CM:345, "`scripts/research/retrieval_log.py` persists every payload"; RC:216, "No re-retrieval = no admission."
- **B.** "we don't need to be saving these PDFs in repo just tracking where they can be found for reference which is our version of persistence" (PS:5128-5130); and for the base, "none of the work in base needs to be verified and stored in evidence." (PS:5182).
- **Governs:** B. A trace ends at a manifest line (URL, time, status, byte count, sha256) and a locator, and at a committed artefact only where a gate needs one (PS:5135). On a fresh clone the bytes may not exist; the sha256 lets a reader re-fetch and compare, and a moved or altered URL breaks the comparison with nothing in the repository to fall back on.
- **OWNER DECISION REQUIRED — no.** It is ruled; it bounds what D4 can promise and CM:345 should say so.

### C-16 The 2026-08-19 rule against adversarial review of plans, and this audit
- **A.** "Adversarial review is a truth-instrument bound to evidence, never a plan-instrument" (PS:642), whose ACTION forbids a pass that schedules remediation or creates a workplan (quoted at PS:1168-1170).
- **B.** OBJ commissions an adversarial audit of the pipeline and "a master document and plan suite".
- **Governs:** B, for this session and purpose, as on 2026-08-25 (PS:1058) and 2026-10-09 (PS:4407, item 6). The supersession record is owed in the ledger.
- **OWNER DECISION REQUIRED — no.**

### C-17 The owner statements this objective rests on are not in the ledger
- O1–O8 of 2026-10-12 ("walkable pipeline all directions", "handshake ALL directions") are relayed in IG:11, which says "none is in the ledger yet". OBJ exists only in a transcript and the brief.
- Rule 0's second sentence is "Record the supersession"; PS:2763-2765 records what happens otherwise: "an unrecorded ruling binds nothing mechanical".
- **OWNER DECISION REQUIRED — no.** A ledger entry quoting OBJ and O1–O8 is owed before any plan cites them.

### C-18 (numbering note)
C-17 above is the item REQ-001 and REQ-005 cite as "C-18" in section 1; the reference there should read C-17. Recorded rather than silently renumbered so a reader comparing drafts is not misled.

### C-19 What "dynamically" may automate
- **A.** DR19:1057-1061, "**Permanently manual:** query design and tier targeting; screening judgment; tier and evidence-type assignment; population-of-study grading and its mismatch note … The contract's premise is that these are judgment acts machinery can only *check*."
- **B.** OBJ, "dynamically research, adjudicate, synthesize, specify and render"; "oh. you have to compute it" (PS:2690), which superseded A for `specifications` only (PS:2693, PS:2713-2714).
- **Reading applied (ASSUMPTION):** "dynamically" means a run is started on demand for a request and executes the acts that request needs, in whatever stage order it needs them; it does not mean unattended. Judgment acts stay acts of the model under REQ-093, with a recorded warrant. IG's U4 reached the same reading: "no ruling asks for acquisition without an agent."
- **OWNER DECISION REQUIRED — yes**, if the owner means more than on-demand orchestration.

### C-20 Dynamic operation against the write path and the tooling split
- REQ-090 and REQ-091 mean a run's rows reach the canonical database only through a data migration in its own change, and a missing writer stops the run. REQ-083 means the site reads the committed database. So the answer to a dynamic request is live only after a merge.
- The owner's interface statement, "have it propagate accordingly" (PS:4580), is read by the ledger as proposals applied through the same path (PS:4586, `[ASSUMPTION]`), with the alternative named as "a ruling against rule 3 … the owner's to make".
- **OWNER DECISION REQUIRED — no**, unless the owner wants immediate writes, which the ledger already flags.

### C-21 Old doctrine on coverage that later rulings have overtaken without a mark
- "BPC entry PROVISIONAL until all 24 recorded + co1_pass ≥9 languages" (PS:123; JP:93) against "provisional means that we have to go back and review the source again" (PS:4833) and the scope rulings (C-06). RUL:54 records the "≥9-language conjunct" as `UNDETERMINED`, awaiting an owner premise.
- "Each slug covers exactly one population. Combined slugs not permitted." (PS:120) against REQ-032 and REQ-027.
- **OWNER DECISION REQUIRED — yes** for the ≥9-language rule; the slug rule is superseded and needs only a mark.

### C-22 Which stage owns the gap register
- PC:107 makes "an OPEN gap" research's entry; SM:143-151 files `gaps` **[P]** under synthesis and says "SYNTHESIS IS THE ONE STAGE WITH NO SUPPORT … The honest answer is a cross-stage register with no single home", adding "under rule 0 an owner ruling settles it".
- The gap register is the carrier of every backward edge that ends at research (REQ-040). A carrier with no stage has no boundary contract.
- **OWNER DECISION REQUIRED — yes** (the stage map's own words).

### C-23 `provisional`: a strength of evidence or a stage of review
- **A.** ME:116, `provisional` = "Synthesis based on partial evidence dimension"; PC:259, T3-alone is `provisional`; PC:252-254, a regulatory-only cell is `provisional`.
- **B.** "provisional means that we have to go back and review the source again to confirm information accuracy" (PS:4833); the ledger reads this as "Provisional is a stage" and assumes no new field is needed (PS:4853, `[ASSUMPTION]`).
- **Why it matters here:** under A a provisional cell is a resting state; under B it is an owed backward edge (REQ-038) that should close. One word cannot be both without the request contract knowing which is meant.
- **OWNER DECISION REQUIRED — yes.**

### C-24 (cross-reference)
REQ-038 cites "C-24" for the `provisional` conflict; that conflict is C-23 above.
