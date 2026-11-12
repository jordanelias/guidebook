# TD — Requirements ledger and stage interface specification (top-down leg)

_Written 2026-11-12 (UTC) against the working tree at `git rev-parse --short HEAD` = `64c10e2`. Line numbers were resolved with `grep -n -F` against that tree, not copied from the dossier (the dossier was generated at `e73b588`; re-resolve any line before relying on it: `grep -n -F '<quote fragment>' <file>`)._

## 0. Verdict

**The owner's prose warrants D4 in full, D3 for `base` and `research` only, and D2 and D1 thinly. The pipeline contract warrants no backward travel at all.** Read against D1–D4:

1. **D4 (verifiable, traceable) is the only dimension the prose states fully, verbatim and repeatedly.** Pointer discipline, retire-in-place, never-reissued identifiers, logged empties and computed determinations are all ruled.
2. **D3 (multilingual, multijurisdictional) is ruled in depth for `base` and `research` and almost not at all downstream.** Nothing in the prose says what language a rendered page is in, whether a source's sentence may be translated, or whether a determination varies by jurisdiction. The one concrete schema consequence the owner was told about (`terms.canonical_en` is required) is recorded as left open for the owner (PS:5194).
3. **D2 (dynamic) is ruled for one act only: the scan contract** (a source is read for every parameter whatever slug found it). "Dynamically" otherwise has no owner gloss; the only standing owner text on the subject says most research acts are judgment acts, not automation (C-18).
4. **D1 (omnidirectional) rests on three thin legs:** an antagonist finding the ledger adopted ("a walk may re-enter any stage"), one clause of a 2026-10-09 commission ("flexibility of pipeline all directions"), and relayed 2026-10-12 statements that are not in the ledger. Exactly **one** mid-pipeline cold entry is described by the owner (evidence onward, "without research"). Entry at judgment, synthesis, specification or render is described nowhere; section 3's interface for those entries is inference and is marked so.
5. **The pipeline contract is forward-only and unratified.** `governance/pipeline-contract.yaml` declares `status: PROPOSED`, `ratified: false` (PC:2-3), gives each stage one forward `entry:` condition and no backward one, and its synthesis and specification entries contradict the owner's stage order (C-11).

Counts are derived, never typed here: requirements `grep -c '^| REQ-' <this file>`; conflicts and gaps `grep -c '^### C-' <this file>`; owner decisions `grep -c '^- \*\*OWNER DECISION REQUIRED — yes' <this file>`; acceptance tests `grep -c '^| AT-' <this file>`.

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

**Warrant classes**, because "the owner said" covers five different things in this repository:

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
| REQ-001 | The pipeline can be run in all directions from any stage, dynamically, to research, adjudicate, synthesize, specify and render across many languages and jurisdictions. | "ensure that our pipeline can be run in all directions at any stage in such a manner where we can dynamically research, adjudicate, synthesize, specify and render across a multitude of languages and jurisdictions" | OBJ | OWNER | D1 D2 D3 D4 | all | LIVE; not yet in the ledger (C-17) |
| REQ-002 | There are seven stages in one ruled order, and `base` is the first. | "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications."; "base is a stage insofar as it supplies the base information upon which research can perform its task" | PS:1454-1455; PS:2302-2303 | OWNER | D1 D4 | all | LIVE; supersedes the five-stage ruling of 2026-08-25 (PS:1457) |
| REQ-003 | A run re-enters stages; stage order is not write order; a re-entered stage still holds only its own facts. | "A walk may re-enter any stage; each stage's tables still carry only their own facts (rule 5)."; "A walk **re-enters** stages rather than passing through them once — digesting a reasoning document produced research leads, a backward edge, and that is normal." | PS:1048-1049; CM:260-261 | LEDGER (adopting an antagonist finding of 2026-08-21); Layer 0 | D1 | all | LIVE; no owner quote states it (self-attack 1) |
| REQ-004 | Flexibility in all directions is a property to be interrogated of every gate, read, write and conditional, not only of the stage order. | "Interrogate quality, logic, sequencing and flexibility of pipeline all directions as well as all gates, reads, writes, conditionals." | PS:4385 | OWNER (a commission to a critic, 2026-10-09) | D1 D4 | all | LIVE |
| REQ-005 | Every table that carries a reference or an id is walkable to and from the spine; handshakes hold in every direction. | "we need to ensure handshakes both top-down and bottom-up, and we need to ensure walkability across all tables with references and ids"; "handshake ALL directions" | IG:11 (O7, O8) | RELAYED 2026-10-12; "none is in the ledger yet" (IG:11) | D1 D4 | all | LIVE but unrecorded (C-17) |
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
| REQ-031 | A search may be recorded for a parameter or a mined source with no slug. | "**R43 Searches without a slug.** … a CHECK requires that a search says what it is for"; owner: "no idea what these are, but resolve them for me in a logical manner" | RUL:305; PS:4433 | LEDGER (owner-delegated resolution) | D2 | research | LIVE; overridable by a later owner statement (PS:4437) |
| REQ-032 | Research crosses every topic with every lens; applicability is found, not presupposed. | "Every research slug gets cross-referenced against a population code, access need or ICF code because there is always the chance that there is an unexpected connection between them." | PS:943-945 | OWNER | D2 D3 | research, judgment | LIVE for the cross-product; "applicability is an OUTPUT of synthesis" is SUPERSEDED by the 2026-08-27 ruling (PS:2040-2042): the crossing is judgment's output |
| REQ-033 | Concept vocabulary is observed at evidence, verbatim and unjudged, and adjudicated at judgment. | "overrule Aug 24 DR. we go evidence>judgment>synthesis."; "listing out all concepts/topics/key words/phrases that appear in the source and then judgment phase will actually do the deep read on it" | PS:2002; PS:2004-2007 | OWNER | D2 D3 | evidence, judgment, base | LIVE for evidence-stage reading; for base vocabulary SUPERSEDED by REQ-060 (PS:5192) |
| REQ-034 | No container states its own answer; a parameter name carries no value and is not an old item code. | "parameter at base, archive prior corpus so it can't be found by tools we use commonly, use add-term for now"; "No base_parameters row points at a terms.canonical_en that itself states a determination (a digit, a comparator, or a min/max word)." | PS:2629; PC:53-54 | OWNER; CONTRACT | D2 | base | LIVE |
| REQ-035 | Sources already held are read before more are fetched. | "Yes, read what we hold first" | PS:4683 | OWNER | D2 | research, evidence | LIVE |
| REQ-036 | A deferral is legitimate, and it must eventually run. | "deferred is okay so long as it runs eventually" | PS:3737 | OWNER | D2 D4 | research; by extension every owed act | LIVE; the ledger records that nothing measures the obligation (PS:3760-3762) |
| REQ-037 | A skimmed finding supplies nothing to a determination; it cues a dedicated reading. | "no. skimmed findings cue tools for a dedicated pass." | PS:4472 | OWNER | D1 backward edge specification → evidence/judgment | specification, judgment, evidence | LIVE |
| REQ-038 | A provisional reading sends work back to its source for re-reading and confirmation. | "provisional means that we have to go back and review the source again to confirm information accuracy" | PS:4833 | OWNER | D1 backward edge specification/render → evidence | specification, evidence | LIVE; changes what `provisional` means against ME:116 (C-22) |
| REQ-039 | Where a study reports no change, backward citation mining and context find the values it tested; if they cannot be found the source has no value. | "This is why we use backwards citation mining and contextual clues. If we are unable to find the actual parameters/values under discussion, then the source itself has no value." | PS:4723 | OWNER | D1 backward edge judgment → research | judgment, research | LIVE |
| REQ-040 | A cell without evidence is a recorded gap, and an open gap is an entry to research. | "an OPEN gap or an item/parameter lacking sufficient evidence"; "`[BEST-PRACTICE-PENDING]` + gap link" | PC:107; ME:117 | CONTRACT; doctrine | D1 backward edge specification → research | specification, research | LIVE; which stage owns `gaps` is disputed (C-21) |
| REQ-041 | Research coverage is set up from the base, not kept beside it. | "we set up the base and in turn we set up the research coverage" | PS:5088 | OWNER | D2 D3; edge base → research | base, research | LIVE |
| REQ-042 | Technique categories and building typologies or rooms show the same criteria in both directions. | "what appears in a category specification for type (eg circulation, acoustics) will appear in building typologies and rooms and vice versa" | PS:5076 | OWNER | D1 lateral | base, render | LIVE; `rooms` are frozen "until a page reads them" (PS:5056) |
| REQ-043 | Synthesis cross-references rows to find links across parameters, topics and categories. | "synthesis will ensure the use of cross referential analysis for table rows to see if there are any relevant links within parameters/topics/categories (eg wheel chair swept path analyses for different wheel chairs would inform different space requirements)" | PS:4989 | OWNER | D1 lateral | synthesis | LIVE |
| REQ-044 | Evidence is stored so it can inform synthesis and specification and can be used directly by render. | "the evidence needs to be stored in such a manner where it can be used to inform synthesis+specifications as well as be able to be used directly by rendering." | PS:4987 | OWNER | D1 non-adjacent forward edge evidence → render | evidence, render | LIVE |
| REQ-045 | A page for an element is derived from the live determinations of its parameters and is never a container rows are filed into. | "Yes, derive it — This derivation is what I expect the specifications pass to be doing--adjudicating, deriving and synthesizing across rows of related evidence." | PS:4679 | OWNER | D2 | specification, render | LIVE; OR-14b open (PS:4699) |
| REQ-046 | A question that is the owner's stops the run and is put as a prompt with full context; a saved answer binds nothing until the ledger quotes it. | "waiting on me decisions need to be prompts with full context" | PS:4598; PS:4600 | OWNER; LEDGER | D2 (what a stage must refuse) | all | LIVE |
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
| REQ-061 | The register does not end where English ends: concepts met in native-language readings enter under the instrument's own phrase. | "you have to ensure that you research them across all of our chosen jurisdictions and languages without an English bias"; "A concept first met outside English is named by the instrument's own phrase, in its own language" | PS:5080; PS:5049 | OWNER; LEDGER (E1, applied on "e1 e3 e4; Appy yes", PS:5041) | D3; backward edge evidence → base | base, evidence | LIVE |
| REQ-062 | Exhaustion and coverage are judged per parameter per bucket member, and a bucket member is a jurisdiction with its associated language. | "Yes, per parameter and bucket so long as the bucket is not just jurisdiction but associated language." | PS:4655 | OWNER | D3 D2 | base, research | LIVE; supersedes "distinct axes" for exhaustion (C-05) |
| REQ-063 | Research stays inside the in-scope jurisdictions until they are categorically exhausted for the subject. | "Standing order: do not research from countries other than Bucket 1 and Bucket 2 for any slug until those buckets are categorically exhausted."; "do not include countries outside of the major identified countries for now" | PS:4295-4297; PS:4835 | OWNER | D3 D2 (a refusal) | research, render | LIVE; membership contested (C-06) |
| REQ-064 | Languages scoped out are not owed until the in-scope set is exhausted. | "Yes, scope them out for now" | PS:4673 | OWNER | D3 D2 (a refusal) | base, research | LIVE |
| REQ-065 | Every jurisdiction value resolves to the declared vocabulary; `UK` never `GB`; a work spanning jurisdictions is `INT`, distinct from `ISO`; admitting a code is a scope decision. | "UK is canonical, add BE HR INT ES IT to the enum"; "Every jurisdiction value resolves to the declared vocabulary."; "admitting a code silently converts a candidate jurisdiction into a declared one, and that is a scope decision" | PS:3687; PC:48; PS:3714-3715 | OWNER; CONTRACT; LEDGER | D3 D4 | base and every table carrying a jurisdiction | LIVE; the vocabulary's home is an enum in code (C-08) |
| REQ-066 | Non-English peer-reviewed work is academic; absence from an English-language index is not a quality fact. | "Non-English peer-reviewed work is ACADEMIC, not grey. Non-indexation in PubMed/Scopus is an INDEXING fact, not an evidence-quality fact." | RC:127-128 | CONTRACT | D3 | evidence, judgment | LIVE |
| REQ-067 | Only the current state is researched and stated; history and superseded editions are not. | "We are interested in what are best practices NOW, and that means we do not need to interrogate the history of anything but rather the current state of everything" | PS:4826 | OWNER | D3 | research, evidence, specification | LIVE |
| REQ-068 | A value keeps the notation and unit its source wrote; both notations are presented; exact linear units are converted and both shown. | "Present both--don't choose between ratio or percentage."; "Yes, convert and show both — Round to nearest 1/4" or 5mm." | PS:3644; PS:4667 | OWNER | D3 D4 | judgment, specification, render | LIVE |
| REQ-069 | A page can show, for one parameter, what each in-scope jurisdiction has for the value, in one comparison table. | "for ramp gradient, i want there to also be an easy comparison master table where you just see what each jurisdiction has for the value" | PS:4844; AP:86 | OWNER; doctrine (jurisdiction-comparison use-pattern) | D3 | render, judgment | LIVE |
| REQ-070 | A language community's own designation for an identity may be recorded beside the English name when its own Co-1 sources attest it. | "The base may record each language community's own designation for an identity code, attested in its own Co-1 sources, beside the English name." | PS:5054 | LEDGER (E6, DG-NON, applied on "apply all recommendations", PS:5037) | D3 | base | LIVE; rests on a blanket approval the ledger marks as an assumption (PS:5045) |
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
| REQ-088 | Rendered work meets web accessibility standards; compliance is never self-certified. | "note: all work must comply with website accessibility standards and best practices" | PS:4847; PS:4858 | OWNER; LEDGER | — (constraint on render) | render | LIVE |
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
- **A.** "the entire pipeline is dynamic rendering on site", "do not rely on artifacts for rendering the site" (PS:1658-1659, quoted in the ledger from the header of archived migration 046; I did not find the original statement); the ledger concluded "**render's hand-off is not a table**" (PS:1667).
- **B.** "I expect the render table to be one where the specification table rows have been converted into complete prose, bibliographic information etc accordingly from the preceding tables" (PS:4729, 2026-10-29). "i want it to be coming from database directly in ideal world" (PS:4840, 2026-10-30).
- **Governs:** B. There is a render table, in the database. A and B agree if the site reads that table. The ledger's "not a table" sentence and IG K31 ("render's hand-off is not a table") are superseded.
- **Still open, recorded by the ledger as the owner's:** how the prose is produced (OW-1b) and whether the table is stored or rebuilt (OW-1c) (`governance/owner-browser.yaml:913-957`). Until both are answered the specification → render boundary has no ruled postcondition and no ruled pointer shape, and every backward edge from render (staleness, re-derivation) is undefined.
- **OWNER DECISION REQUIRED — yes** (OW-1b, OW-1c).

### C-02 What "render across a multitude of languages" means
- **A.** OBJ: "render across a multitude of languages and jurisdictions".
- **B.** No other owner statement says what language a page is rendered in. The only adjacent text is the open question "whether and by whom a source's sentence may be translated or rewritten" (PS:4895, OW-1b's residue) and ME:14's four audiences with no language named.
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
- **Governs:** B. The unit of coverage is the pair, and the set of pairs is scoped. The two March rules are superseded for exhaustion; no back-pointer marks them at PS:123/129. The number of languages is quoted three ways in the record (14 at PS:129, 19 in RC and the skills, and "the 14 languages `lang_jur_map` pairs with them" at PS:5026); none should be quoted. Derive: `python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select count(distinct language),count(*) from v_research_scope').fetchall())"` (`v_research_scope` **[P]**; for the bottom-up leg to run, since this leg did not open the database).
- **OWNER DECISION REQUIRED — no.** A supersession record is owed.

### C-06 Which jurisdictions are in scope
- **A.** JP:13 and JP §1.1: 24 countries plus two meta-codes, "Global South ≥8 jurisdictions" (JP §1.2), CANONICAL.
- **B.** "Standing order: do not research from countries other than Bucket 1 and Bucket 2 for any slug until those buckets are categorically exhausted." (PS:4295-4297, 2026-09-28), buckets listed at PS:4312-4313.
- **C.** "Yes it is P1+P2+P3" and "do not include countries outside of the major identified countries for now" (PS:4835, 2026-10-30); the P-set is recorded only as an `[ASSUMPTION]` (PS:5026).
- **B and C name different sets.** Derive, do not trust: `python3 -c "b=set('UN ISO CA US UK DE NO SE JP AU EU SG NZ IE FR ES PT FI NL KR'.split());p=set('US UK AU CA DE NO SE ISO EU FR CH NL DK FI BE IE ES IT PT JP SG NZ KR CN'.split());print(sorted(b-p),sorted(p-b))"` (lists typed from PS:4312-4313 with country names converted to codes by me, and from PS:5026).
- **The ledger itself records A against B as unresolved** ("NOT RESOLVED BY THIS RULING", PS:4315-4320).
- **Governs:** C over B (later); B/C over A for research now. Whether `UN` remains in scope, and the Global South tension, are not settled.
- **OWNER DECISION REQUIRED — yes** (jurisdiction scope is owner-gated, CM §8).

### C-07 Evidence from outside the in-scope jurisdictions
- **A.** "**Does not exclude other jurisdictions' evidence.** If Tier 1–3 clinical evidence comes from a non-canonical jurisdiction (e.g., Finland, Austria, Turkey), it is cited. The 24-jurisdiction requirement applies to code/standards research (Tier 4–6), not to clinical evidence." (JP:62).
- **B.** Owner: "do not research from countries other than Bucket 1 and Bucket 2" (PS:4295). The ledger's ACTION widens "research" to "Do not admit evidence from a jurisdiction outside buckets 1–2" (PS:4329-4330), which is the session's wording, not the owner's.
- **C.** "Yes, read what we hold first" (PS:4683), read as covering held sources "inside and outside buckets 1 and 2" (PS:4701). A memory note records the order of work as codes first, "then look for higher-tier evidence (T1-T3, any language, any jurisdiction)" (MEM `spec-page-requirements.md:25`).
- **What cannot be avoided:** citation mining (REQ-049) of an in-scope T1 anchor will surface studies from out-of-scope countries. The prose does not say whether such a study is admitted, staged, or refused.
- **OWNER DECISION REQUIRED — yes.**

### C-08 "Adding a language or a jurisdiction is data, not code"
- **A.** The brief's D3 clause (`dossier/01-method-and-brief.md:11`), which the brief itself calls the assistant's decomposition.
- **B.** The owner's words place the jurisdiction vocabulary in code: "add BE HR INT ES IT to the enum" (PS:3687); the contract notes "the architecture note's base.jurisdictions, which has no table yet" (PC:49); and admitting a member is a scope decision (PS:3714-3715; CM §8).
- **Reading:** "data, not code" is supported by rule 8 (REQ-093) and by the base holding the language–jurisdiction pairs (`lang_jur_map` **[P]**), not by any owner sentence about jurisdictions. Mechanically a new member should be a row; its authorization is always an owner ruling. A request for an undeclared jurisdiction is refused with a prompt (REQ-046), never auto-admitted.
- **OWNER DECISION REQUIRED — no** for the mechanism (tooling); **yes** for each admission, as now.

### C-09 Which stage assigns the lenses
- **A.** The crossing is judgment's output: "overrule Aug 24 DR. we go evidence>judgment>synthesis." (PS:2002), with the ledger's ACTION "the crossing is **judgment's output**" (PS:2041-2042); CM:365.
- **B.** "evidence stage must carefully adjudicate sources to assignrelevant populations/access needs/ICF codes properly referenced" (PS:4987, 2026-11-06). The same message lists research, evidence, synthesis, specifications and renders, and no judgment stage, although its first line gives all seven.
- **The ledger reads B as a collapse of evidence and judgment and marks the reading `[ASSUMPTION]`** (PS:4999).
- **Governs:** on the letter of rule 0, B is later. On the ledger's reading, A stands. This decides what a cold entry at evidence (REQ-007) must do before it hands on, so it cannot be left as a reading.
- **OWNER DECISION REQUIRED — yes** (CONTESTED; one sentence: confirm that "evidence stage" in the 2026-11-06 list means evidence and judgment together).

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
- **Gap:** the prose names synthesis's work (cross-referential analysis, convergence, divergence) and never says what one synthesis row is for a parameter × lens, nor that a specification must point at it rather than straight at judgment rows. Whether the specification pass writes an element-level determination is already put to the owner (OR-14b, PS:4699).
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
- **B.** "we don't need to be saving these PDFs in repo just tracking where they can be found for reference which is our version of persistence" (PS:5130); and for the base, "none of the work in base needs to be verified and stored in evidence." (PS:5182).
- **Governs:** B. A trace ends at a manifest line (URL, time, status, byte count, sha256) and a locator, and at a committed artefact only where a gate needs one (PS:5134). On a fresh clone the bytes may not exist; the sha256 lets a reader re-fetch and compare, and a moved or altered URL breaks the comparison with nothing in the repository to fall back on.
- **OWNER DECISION REQUIRED — no.** It is ruled; it bounds what D4 can promise and CM:345 should say so.

### C-16 The 2026-08-19 rule against adversarial review of plans, and this audit
- **A.** "Adversarial review is a truth-instrument bound to evidence, never a plan-instrument" (PS:642), whose ACTION forbids a pass that schedules remediation or creates a workplan (PS:644; quoted again at PS:1171).
- **B.** OBJ commissions an adversarial audit of the pipeline and "a master document and plan suite".
- **Governs:** B, for this session and purpose, as on 2026-08-25 (PS:1058) and 2026-10-09 (PS:4407, item 6). The supersession record is owed in the ledger.
- **OWNER DECISION REQUIRED — no.**

### C-17 The owner statements this objective rests on are not in the ledger
- O1–O8 of 2026-10-12 ("walkable pipeline all directions", "handshake ALL directions") are relayed in IG:11, which says "none is in the ledger yet". OBJ exists only in a transcript and the brief.
- Rule 0's second sentence is "Record the supersession"; PS:2763-2765 records what happens otherwise: "an unrecorded ruling binds nothing mechanical".
- **OWNER DECISION REQUIRED — no.** A ledger entry quoting OBJ and O1–O8 is owed before any plan cites them.

### C-18 What "dynamically" may automate
- **A.** DR19:1057-1061, "**Permanently manual:** query design and tier targeting; screening judgment; tier and evidence-type assignment; population-of-study grading and its mismatch note … The contract's premise is that these are judgment acts machinery can only *check*."
- **B.** OBJ, "dynamically research, adjudicate, synthesize, specify and render"; "oh. you have to compute it" (PS:2690), which superseded A for `specifications` only (PS:2693, PS:2713-2714).
- **Reading applied (ASSUMPTION):** "dynamically" means a run is started on demand for a request and executes the acts that request needs, in whatever stage order it needs them; it does not mean unattended. Judgment acts stay acts of the model under REQ-093, with a recorded warrant. IG's U4 reached the same reading: "no ruling asks for acquisition without an agent."
- **OWNER DECISION REQUIRED — yes**, if the owner means more than on-demand orchestration.

### C-19 Dynamic operation against the write path and the tooling split
- REQ-090 and REQ-091 mean a run's rows reach the canonical database only through a data migration in its own change, and a missing writer stops the run. REQ-083 means the site reads the committed database. So the answer to a dynamic request is live only after a merge.
- The owner's interface statement, "have it propagate accordingly" (PS:4580), is read by the ledger as proposals applied through the same path (PS:4586, `[ASSUMPTION]`), with the alternative named as "a ruling against rule 3 … the owner's to make".
- **OWNER DECISION REQUIRED — no**, unless the owner wants immediate writes, which the ledger already flags.

### C-20 Old doctrine on coverage that later rulings have overtaken without a mark
- "BPC entry PROVISIONAL until all 24 recorded + co1_pass ≥9 languages" (PS:123; JP:93) against "provisional means that we have to go back and review the source again" (PS:4833) and the scope rulings (C-06). RUL:54 records the "≥9-language conjunct" as `UNDETERMINED`, awaiting an owner premise.
- "Each slug covers exactly one population. Combined slugs not permitted." (PS:120) against REQ-032 and REQ-027.
- **OWNER DECISION REQUIRED — yes** for the ≥9-language rule; the slug rule is superseded and needs only a mark.

### C-21 Which stage owns the gap register
- PC:107 makes "an OPEN gap" research's entry; SM:143-151 files `gaps` **[P]** under synthesis and says "SYNTHESIS IS THE ONE STAGE WITH NO SUPPORT … The honest answer is a cross-stage register with no single home", adding "under rule 0 an owner ruling settles it".
- The gap register is the carrier of every backward edge that ends at research (REQ-040). A carrier with no stage has no boundary contract.
- **OWNER DECISION REQUIRED — yes** (the stage map's own words).

### C-22 `provisional`: a strength of evidence or a stage of review
- **A.** ME:116, `provisional` = "Synthesis based on partial evidence dimension"; PC:259, T3-alone is `provisional`; PC:252-254, a regulatory-only cell is `provisional`.
- **B.** "provisional means that we have to go back and review the source again to confirm information accuracy" (PS:4833); the ledger reads this as "Provisional is a stage" and assumes no new field is needed (PS:4854, `[ASSUMPTION]`).
- **Why it matters here:** under A a provisional cell is a resting state; under B it is an owed backward edge (REQ-038) that should close. One word cannot be both without the request contract knowing which is meant.
- **OWNER DECISION REQUIRED — yes.**

---

## 3. Stage interface specification

**How to read this section.** A cell marked **[R]** restates a requirement the prose rules (the REQ is cited). A cell marked **[I]** is my inference from the pointer rule (REQ-013 to REQ-015), the hand-off cardinalities (REQ-010, REQ-011) and the write rule (REQ-012). C-10 applies: no owner prose describes entry at judgment, synthesis, specification or render, so most backward entries below are **[I]**. Table and column names are **[P]** throughout.

**Three rules that hold at every stage in every direction** (each **[R]**):

1. *Re-entry adds, it never rewrites.* Arriving at a stage from downstream produces new rows, or retires rows in place and adds their successors (REQ-012, REQ-018). It never edits an upstream row to make a downstream fact true.
2. *A stage answers from its own tables and points for the rest* (REQ-015). It never receives a copy of an earlier stage's fact.
3. *An act that happened leaves a row; an act that was skipped leaves a row saying why* (REQ-021, REQ-036). "Not examined" is never represented by silence.

### 3.1 base

- **Purpose, in the owner's words.** "it supplies the base information upon which research can perform its task … it's the first layer of information" (PS:2302-2304). "we are working on the base to create a comprehensive multilingual multijurisdictional matrix of terms/concepts that can be leveraged by research" (PS:5180).
- **Inbound.**
  - *Forward:* none; base is first. Prepopulation enters from the owner-selected catalogues under "Screen, then you approve" (PS:4398) **[R]**.
  - *From research (backward):* a form found in an instrument of a language and jurisdiction, with where it was found (REQ-060) **[R]**; a search seed becomes vocabulary only when an instrument in its language is read and the phrase found there (REQ-058, REQ-059) **[R]**.
  - *From evidence (backward):* a phrase observed in an admitted source (REQ-033); a concept first met in a non-English reading, under the instrument's own phrase (REQ-061) **[R]**.
  - *From judgment (backward):* an adjudication that mints or matches a term; a parameter promoted from a term or declined with its reason (REQ-029, REQ-034) **[R]**; a parameter's accessibility direction recorded from an admitted source (PC:93-95; PS:4866) **[R]**.
  - *From synthesis, specification, render:* none named in the prose. The owner's editing entry (REQ-009) and owner approvals arrive here as ledger-backed changes **[I]**.
- **Outbound postconditions.** Every concept has an identity that is not an English string (C-04, open). Each form states its language, its jurisdiction, its usage type and its attestation: found in a source with a locator, owner-supplied, or a flagged model-generated seed (PS:5167, ledger reading) **[R]**. Coverage is derivable per concept × language-and-jurisdiction pair and distinguishes a cell with a form, a cell searched with none found, and a cell not yet searched (PS:5193, `[ASSUMPTION]` in the ledger) **[R as assumption]**. Every code resolves to its registry (REQ-065). No name states a determination (REQ-034). Nothing is deleted (REQ-018).
- **Pointer back.** A base cell points at its own source locator (URL, page, line), not into evidence (REQ-060, REQ-022). A parameter points at its term; a parameter's direction points at the admitted source that states it, which is the one ruled base → evidence pointer.
- **Cold entry.** Given a form in any in-scope language, base must resolve it to a concept or answer UNKNOWN and record the form as an unattested seed. It must refuse: a name the model generated presented as vocabulary (REQ-058); a name carrying a value (REQ-034); a jurisdiction or language that is not declared or is scoped out (REQ-064, REQ-065), which becomes an owner prompt (REQ-046).
- **Neutral identity required.** A concept id independent of every label; a jurisdiction code; a language code; the pair as the unit of coverage (REQ-062); lens codes whose labels may exist per language (REQ-070). `terms.canonical_en`, `term_aliases(language, jurisdiction)`, `lang_jur_map(language, jurisdiction, scope_status)`, `base_parameters.term_id` **[P]**.

### 3.2 research

- **Purpose.** "you research slugs" (PS:1454); "must be performed by topic across languages and jurisdictions while tracking its queries. must be able to perform citation mining." (PS:4985). Ledger gloss: "a lead: what to go and get" (PS:1466).
- **Inbound.**
  - *Forward from base:* the owed coverage, derived from the base as subject × lens × in-scope pair (REQ-041, REQ-062, REQ-032); the subject is a slug or a parameter (REQ-031) **[R]**.
  - *From evidence (backward):* a confirmed T1–T2 anchor to mine backward and forward (REQ-049) **[R]**.
  - *From judgment (backward):* an absence finding whose tested values must be found (REQ-039) **[R]**.
  - *From synthesis (backward):* reasoning that yields leads (CM:260-261) **[R]**.
  - *From specification (backward):* an open gap on a pending cell (REQ-040) **[R]**.
  - *From render (backward):* nothing named. A reader-facing gap reaches research only through the gap register **[I]**.
- **Outbound postconditions.** Every query is logged verbatim with its language, jurisdiction, lens cell and prior; empties and deferrals are kept and say why (REQ-021, REQ-048). Each candidate is tied to the search that surfaced it (PC:128-130). A pair deliberately not searched is a deferred search row, not an absence (PS:4344-4350, ledger correction) **[R]**. An unreachable item is typed and closed (REQ-047). A deferral is a measurable debt (REQ-036).
- **Pointer back.** A search points at its subject (slug or parameter), its lens codes, its language and jurisdiction, and, where it is a mining or gap-driven search, at the source or gap that caused it. `search_executions(slug, parameter_id, mined_ref_id, language, jurisdiction, identity_code, icf_code, needs_code, medical_code)`, `gap_mining.gap_id` **[P]**.
- **Cold entry.** Given a request cell, research must first say what is already held (REQ-035), then what has been searched for that cell, and only then search. It must refuse an out-of-scope jurisdiction (REQ-063) or a scoped-out language (REQ-064) by recording the deferral, and must flag a search run on a model-generated term (REQ-059).
- **Neutral identity required.** The query in its own language, verbatim; language and jurisdiction as codes on the search, never inferred from the query text; the subject by id.

### 3.3 evidence

- **Purpose.** "evidence research" (PS:1454). "logs all relevant items found in search with a unique reference ID, DOI/PMID and other codes if available, type of source (academic, code, professional practices, etc)" (PS:1883-1884). "the evidence needs to be stored in such a manner where it can be used to inform synthesis+specifications as well as be able to be used directly by rendering." (PS:4987).
- **Inbound.**
  - *Forward from research:* a candidate, re-retrieved (REQ-051), checked for an existing identity (RC:207), with a logged search behind it (REQ-050) **[R]**.
  - *Cold (REQ-007):* a source already held or handed in. It still gets a search row saying it came from a list (REQ-050) and a retrieval record (REQ-022) **[R]**.
  - *From judgment or specification (backward):* a dedicated full reading owed on a skimmed or provisional source (REQ-037, REQ-038); verification owed on a source a determination rests on ("must be verified", PS:4474) **[R]**. A corrected bibliographic field comes from the payload (REQ-023).
  - *From base (lateral):* the catalogue grew, so held sources are owed a reading against the new parameters (REQ-027 with REQ-029; PC:215-217) **[I]**.
  - *From render:* read-only lookup of a citation by reference id (REQ-015) **[R]**.
- **Outbound postconditions.** One row per source under an identifier never reissued (REQ-019). Bibliographic fields from the payload, in the source's own language (REQ-023, REQ-071). A verification standing that is never empty (RC:217-219). A record of what was read of the source and for which parameters, including "read in full, nothing found" (REQ-021, REQ-027). Phrases observed verbatim with the language they appear in (REQ-033). A source is "covered" only when read, extracted and verified (REQ-079).
- **Pointer back.** A source points at the search that admitted it and at its retrieval record; an observed phrase points at its source and locator; a reading points at its source and, when targeted, its parameter. `search_admissions(exec_id, ref_id)`, `source_scans(ref_id, target_parameter_id)`, `observed_terms(ref_id, language)`, `evidence_sources.language` **[P]**.
- **Cold entry.** May admit without a discovery search; may not admit without re-retrieval, may not create a second identity for one DOI, and may not claim a tier the retrieved bytes do not support (REQ-051).
- **Neutral identity required.** The reference id; DOI, PMID or standard number where one exists; the source's language and original-script title; the issuing jurisdiction and, for a standard, the edition in force (REQ-067).

### 3.4 judgment

- **Purpose.** "judge evidence" (PS:1454). "delivers a verdict on an evidence item for what tier of evidence hierarchy it belongs to (1, 2…6)"; "determines category of judgment item, derives value/process/figure/goal for it" (PS:1885-1887). "judgment phase will actually do the deep read on it to determine what can be derived from the source" (PS:2006-2007).
- **Inbound.**
  - *Forward from evidence:* an admitted source that is verified and has a recorded reading covering the parameter (PC:215-218) **[R]**.
  - *From base (lateral):* a new parameter, against which held sources are re-read **[I]**.
  - *From specification (backward):* a skimmed finding to be read in full (REQ-037); a provisional reading to be confirmed (REQ-038); a figure that set a value while still preliminary, flagged for follow-up (PS:4671) **[R]**.
  - *From synthesis (backward):* a contested root-versus-echo judgment or a divergence that needs the figures re-graded **[I]**.
  - *From render or owner (backward):* a proposed correction to a figure (REQ-009) **[I]**.
- **Outbound postconditions.** One row per figure or finding (REQ-011), each with: the parameter by id; the value, unit and notation as the source wrote them (REQ-068); the verbatim quote and locator (RC:100-101); every relevant lens (REQ-073, REQ-076); the jurisdiction the figure belongs to; how it was read (skimmed or in full) and its review status (REQ-030, REQ-079); the relation to any figure it depends on (PC:183-184); its root (REQ-080). A tier verdict per source (REQ-078). A grade of population studied against population served, with a dissent as a second row (CM §4). An adjudication for every observed phrase (RC:312-314).
- **Pointer back.** An extraction points at its source (required, never unique), its parameter and its lens codes; a relation points at the other extraction; an adjudication points at its observation. `source_value_extractions(ref_id, parameter_id, identity_code, icf_code, needs_code, medical_code, jurisdiction, root_id, root_ref_id)`, `extraction_relations`, `term_adjudications(observation_id, term_id)` **[P]**.
- **Cold entry.** Given a held source and a parameter, judgment can produce extractions. It must refuse a source that is not verified or has no reading covering the parameter (PC:215-218), must not change a figure's digits in place (only reformat: "Yes, reformat in place", PS:4618), and must not alter a row a live determination rests on without that determination being refused or re-derived (PS:4560, ledger) **[R]**.
- **Neutral identity required.** The value held exactly, in the unit and notation of the source, with any converted notation marked as derived (REQ-068); the quote in the source's language (translation is C-02, open); jurisdiction and clause as the locator of a code value; lens codes, never an English group name.

### 3.5 synthesis

- **Purpose.** "synthesize judgments" (PS:1454). "synthesis will ensure the use of cross referential analysis for table rows to see if there are any relevant links within parameters/topics/categories" (PS:4989). Ledger gloss: "what the judgments say together" (PS:1469).
- **Inbound.**
  - *Forward from judgment:* one or more judgment rows for a parameter (REQ-010) **[R]**.
  - *Lateral:* judgment rows of other parameters (REQ-043) and of other lenses on the same parameter **[R]**.
  - *From specification (backward):* claims that cannot all hold, needing a stated approach ("Stated and divergent, with a synthesis approach", PS:4626); a contested direction, recorded per lens "when it first arises" (PS:4721) **[R]**.
  - *From render (backward):* nothing named.
- **Outbound postconditions.** A convergence assessment that counts independent roots and treats agreeing jurisdictions as transmission, not corroboration (REQ-080; EA:102). Divergence recorded with which dimension governs and why (ME:132). Cross-parameter links and cross-lens conflicts as typed rows (REQ-043). Gaps recorded. Synthesis prose only at the Opus floor (REQ-096).
- **Pointer back.** A synthesis row points at the judgment rows and sources it drew on, through a link the synthesis writes (REQ-012); a connection points at each target by a typed key. `convergence_sources(convergence_id, ref_id)`, `connection_targets(parameter_id, extraction_id, identity_code, slug)` **[P]**. What a synthesis row *is* for a parameter × lens is not ruled (C-12).
- **Cold entry.** Given a parameter, synthesis answers from the judgment rows held. With none, it answers OWED and names the judgment or research act that would supply them. It must not count documents or jurisdictions as roots.
- **Neutral identity required.** The parameter id; a root identity that is the same whichever jurisdiction or language repeats the figure; jurisdiction as an attribute of the spread, never as a unit of agreement.

### 3.6 specification

- **Purpose.** "specify syntheses" (PS:1454). "specifications: must be able to review all evidence and syntheses of evidence to determine what best practice is, which explicitly means the most accommodating/gentle/dignified set of values/rationales/solutions" (PS:4991). Ledger gloss: "therefore: 1200 mm, marked ●" (PS:1470).
- **Inbound.**
  - *Forward from synthesis:* the syntheses for the parameter (REQ-010); and, by pointer, the governing judgment rows and sources (REQ-024) **[R]**.
  - *From base:* the parameter and its recorded direction (PC:93-95) **[R]**.
  - *From render or owner (backward):* a question about a cell, or a change upstream of it, which is answered by re-deriving, never by editing the determination (REQ-025, REQ-009) **[I]**.
- **Outbound postconditions.** At most one live determination per parameter × lens set, computed (REQ-025), carrying: state; marker (REQ-089); the value in every notation the governing set states (REQ-068); the flags for a regulatory-only basis, unverified sources and proxy inference (REQ-082, REQ-051); rule version and derivation hash (EA:116); at least one governing link if `stated` or `provisional` (REQ-024); a gap link if `pending` (REQ-040); no row at all for a lens the parameter is not relevant to (REQ-074). An earlier determination is retired and pointed at its successor (REQ-018).
- **Pointer back.** To the governing sources and extractions through links the specification writes; to its convergence or synthesis; to its gap; to its parameter and lenses; to the determination it supersedes. `specification_source_links`, `specification_extraction_links`, `specifications(parameter_id, convergence_id, gap_register_id, superseded_by_specification_id, derivation_sha, rule_version)` **[P]**.
- **Cold entry.** Given parameter × lens, specification computes from what is held. Where evidence is insufficient it answers with a pending determination and a gap, which is the entry to research (REQ-040). It must refuse: a hand-assigned state (REQ-025); `stated` on a regulatory-only basis (REQ-082); a full marker on an unverified governing source (PS:4474); a determination keyed on a diagnosis alone (REQ-075); a published value from a skimmed figure (REQ-030).
- **Neutral identity required.** Parameter id and lens codes. No jurisdiction and no language in the key (C-03, as read). The direction that makes "most accommodating" computable, recorded per parameter.

### 3.7 render

- **Purpose.** "render specifications" (PS:1455). "renders: must be able to process specifications to be readable for a webpage, must be able to compile all evidence in tables for comparison, must be radically transparent in approach, must ensure proper bibliographic citations, etc." (PS:4993). Ledger gloss: "the surface a reader opens" (PS:1471).
- **Inbound.**
  - *Forward from specification:* live determinations only (REQ-020, REQ-084) **[R]**.
  - *Direct from evidence:* citations and bibliographic data, looked up by reference id (REQ-015, REQ-044) **[R]**.
  - *Direct from judgment:* the figure each in-scope jurisdiction states, for the comparison table (REQ-069) **[R]**.
  - *Direct from synthesis:* the dispute to be noted in the item's discussion (PS:4626) **[R]**; cross-parameter links **[I]**.
  - *Direct from base:* lens registries and labels, categories and rooms (REQ-042), the audience profiles **[R]**.
- **Outbound postconditions.** Complete prose and bibliographic information built from the preceding tables (REQ-084); the same determination tuple, marker and flags in every register (REQ-087, REQ-089); both lenses, with the filters first (REQ-086); a comparison across in-scope jurisdictions only (REQ-063, REQ-069); no row for an empty cell, with the gap stated (REQ-074; C-13); nothing presented as correct (REQ-085); accessibility tested and recorded, never self-certified (REQ-088); nothing committed as a render (REQ-083).
- **Pointer back.** Every rendered cell points at its determination; every citation at a source; every comparison row at the judgment row it shows. If render rows are stored, each carries what it was built from so staleness is detectable (OW-1c, open).
- **Backward out of render.** A reader or the owner at a rendered cell must be able to reach, by pointers alone: the determination, its governing figures, their sources, the retrieval records, the searches that found them, and the base concepts and lens codes, each in the language it was recorded in (REQ-014, REQ-015) **[R in principle; the path is not described]**. The owner's edit at any table propagates forward from that table (REQ-009).
- **Cold entry.** Given a cell with no live determination, render answers "no determination" with the gap and coverage status (C-13); it writes no prose of its own for it, shows no retired row, and reads no committed file.
- **Neutral identity required.** A page is identified by a parameter, or by an element reached through a term pointer (REQ-045), never by an old item code. The reader's language is C-02, open. `weighting_profile(audience, use_pattern)` **[P]**; the render table of REQ-084 has no name in the prose.

### 3.8 Boundary table

"Pre" is what must be true to cross; "Post" is what the crossing leaves; "Pointer" is what the arriving side carries back.

| # | Boundary | Direction | Pre | Post | Pointer back | Warrant | Status |
|---|---|---|---|---|---|---|---|
| B1 | base → research | forward | subject, lens and in-scope pair all resolve in base | a logged search, or a logged deferral, for the cell | search → subject, lens, language, jurisdiction | REQ-041, REQ-062, REQ-021 | ruled |
| B2 | research → evidence | forward | candidate re-retrieved; identity pre-checked; search logged | a source row with a spent identifier and a non-empty verification standing | source → admitting search; source → retrieval record | REQ-050, REQ-051, REQ-019 | ruled |
| B3 | evidence → judgment | forward | source verified; a recorded reading covers the parameter | one or many figure rows; tier verdict; population grade | figure → source (required, not unique) | REQ-011, REQ-079 | ruled |
| B4 | judgment → synthesis | forward | at least one judgment row for the parameter | a convergence or divergence statement | synthesis → the judgment rows it drew on | REQ-010, REQ-012, REQ-080 | ruled in outline; the object is C-12 |
| B5 | synthesis → specification | forward | a synthesis for the parameter × lens; governing figures reachable | a computed determination, or pending with a gap | determination → synthesis, governing figures and sources | REQ-010, REQ-024, REQ-025 | ruled in outline; contract contradicts (C-11) |
| B6 | specification → render | forward | a live, marked determination | prose and bibliography built from preceding tables | rendered cell → determination; citation → source | REQ-084, REQ-015 | ruled in outline; shape open (C-01) |
| B7 | evidence → research | backward | a confirmed T1–T2 source | a mining search and its candidates | search → mined source | REQ-049 | ruled |
| B8 | judgment → research | backward | an absence finding with unidentified tested values | a mining search, or the source given no role and flagged | search → mined source; figure → code row it confirms | REQ-039 | ruled |
| B9 | synthesis → research | backward | reasoning that names something to go and get | leads | lead → the reasoning that produced it | REQ-003 | ledger |
| B10 | specification → research | backward | a pending cell | an open gap, then a gap-driven search | search → gap; determination → gap | REQ-040 | ruled; carrier unowned (C-21) |
| B11 | specification → evidence/judgment | backward | a skimmed or provisional reading under a determination | a full reading and a confirmed or corrected figure | new reading → source; follow-up → figure | REQ-037, REQ-038 | ruled |
| B12 | evidence/judgment → base | backward | an observed phrase, or a concept met in a native-language reading | an adjudicated term, an alias, a parameter or a recorded declination | adjudication → observation; base form → its locator | REQ-029, REQ-033, REQ-061 | ruled |
| B13 | research → base | backward | a form found in an instrument of a pair | an attested form on the base cell | form → URL, page, line | REQ-060 | ruled |
| B14 | base → evidence/judgment | lateral re-entry | a parameter added to the catalogue | held sources re-read against it | reading → source and parameter | REQ-027 with REQ-029 | inferred |
| B15 | evidence → render | forward, skipping | a verified source | a citation or an evidence table row | citation → source | REQ-044, REQ-015 | ruled |
| B16 | judgment → render | forward, skipping | a figure with its jurisdiction | a comparison-table row | row → figure → source | REQ-069 | ruled |
| B17 | render/owner → any table | backward, then forward | an owner edit or answer, recorded in the ledger where it is a ruling | a change through the write path, and re-derivation of whatever depended on it | change → ledger entry; superseded row retained | REQ-009, REQ-046, REQ-018, REQ-025 | ruled, with unratified readings |

**Edges the objective needs and no prose names:** synthesis → judgment, specification → synthesis, render → specification (other than through the owner), and render → research (other than through a gap). They are covered only by the general rules at the head of this section.

### 3.9 The minimum dynamic request contract

**The owner has not described a request object.** D2 in the brief is the assistant's decomposition, and this subsection is **[I]** throughout. It is the least that REQ-001, REQ-014, REQ-021, REQ-062, REQ-063, REQ-072 and REQ-092 jointly imply.

**What a request must be able to say** (one typed value per field, REQ-092):

| Field | Meaning | Resolves against | Rule |
|---|---|---|---|
| subject | a parameter, or a concept, or an element; given as an id, or as a form plus the language it is in | base | resolved by base or answered UNKNOWN; never matched on an English string alone (REQ-055, REQ-057) |
| lens | one or more codes from any of the four models, or "every relevant model" | base registries | at least one (REQ-072); never a diagnosis alone for a determination (REQ-075) |
| jurisdiction | one or more declared codes; default, the in-scope set | base | an undeclared or out-of-scope code is REFUSED with its ruling (REQ-063, REQ-065) |
| language | one or more declared codes; default, the languages paired with the jurisdictions | base | a scoped-out language is REFUSED (REQ-064); the pair is the unit (REQ-062) |
| audience | one of the four audiences | render | changes register and emphasis, never data (REQ-087) |
| entry | the stage the run starts at | — | any of the seven (REQ-001) |
| travel | forward to a named stage, backward to a named stage, or lateral across subjects, lenses, jurisdictions or languages | — | REQ-001, REQ-004 |
| requester and session | who asked and in which session | — | every row the run writes carries it (REQ-021) |

**What every stage must answer**, using one of five verbs so that silence is never an answer:

- **ANSWER** — rows, each with its pointers back.
- **EMPTY** — examined, nothing found, with the row that records the examination (REQ-021).
- **UNKNOWN** — never examined. Distinct from EMPTY.
- **OWED** — an act is due; the answer names the act, the edge it opens (section 3.8) and the row that records the debt (REQ-036).
- **REFUSED** — a rule forbids it; the answer cites the ruling and, where the question is the owner's, raises a prompt (REQ-046).

| Stage | Must be able to answer for a request cell |
|---|---|
| base | Does the subject resolve, and to which concept? Which forms exist for each requested pair, and how is each attested? Which requested pairs are in scope, scoped out or undeclared? Which lens codes are relevant candidates? |
| research | For each requested pair and lens: searched (with what, when, yielding what), deferred (why), or never searched? What is already held that bears on the cell? What debts are open (mining, gaps)? |
| evidence | Which sources are held for the subject, from which jurisdictions and in which languages, each with its verification standing? Which have been read for this parameter, in full or skimmed, and which not at all? |
| judgment | Which figures and findings exist for the cell, each with value, notation, quote, locator, lens codes, jurisdiction, reading method, review status and tier? Which are owed a dedicated reading or follow-up? |
| synthesis | How many independent roots support each value? Where do sources diverge and which dimension governs? What links to other parameters or conflicts across lenses are recorded? |
| specification | Is there a live determination? Its state, marker, value in every notation, flags and governing links; or pending with its gap; or no row because the lens is not relevant. Is it current against its inputs? |
| render | The page or row for the cell, read from the database: prose, marker and flags, the per-jurisdiction comparison, the evidence tables, citations by pointer, gaps stated. For an empty cell: which of not relevant, UNKNOWN, EMPTY or OWED applies (C-13). |

**Limits on "dynamic" that the prose imposes** (each **[R]**): a run writes to a scratch copy and its rows reach the database through a data migration (REQ-090); a missing writer stops the run and is shipped separately (REQ-091); judgment acts are the model filling fields with a warrant, not automation (REQ-093; C-18); an owner-gated question stops the run (REQ-046); a run ends with an adversarial audit (REQ-094); the boundary record and doctrine recheck of REQ-095 are written for a forward walk and, in a re-entrant run, would fire at every crossing in either direction, which the contract does not address.

---

## 4. Acceptance tests

Each test is phrased so the bottom-up leg can run it against code and data. "Mechanical" = decidable by a query, a command or a refusal test on a scratch copy. Tests that need a human or an owner reading are marked.

| ID | REQ | Test | Mechanical |
|---|---|---|---|
| AT-01 | 006, 005 | For every ordered pair of the seven stage ids, a path of foreign keys, links or views exists from a table of the first to a table of the second, and a registered check fails when one is removed. | yes |
| AT-02 | 014, 015, 022 | From one live determination, reach by keys only: its governing figures, their sources, each source's retrieval record (URL and sha256) and the search that admitted each source. No step uses a name match, a note or a JSON list. | yes |
| AT-03 | 014, 071, 058 | Repeat AT-02 for a determination with a governing source whose language is not English. The source's title and author names are stored in the original script, and the quote verified against it is in the source's language. | yes, if such a row exists; otherwise UNPROVEN, not passed |
| AT-04 | 015, 013 | No table at synthesis, specification or render holds an author name, a title, a DOI or a year. | yes |
| AT-05 | 007, 050 | Start a run at evidence with a source in hand and no prior search. It completes to a determination on a scratch copy, and the source has an admission edge to a search whose origin says it came from a list. | yes |
| AT-06 | 007, 051 | The same run is refused admission when the source has not been re-retrieved. | yes |
| AT-07 | 001, C-10 | For each of judgment, synthesis, specification and render, a run can be started at that stage for a parameter × lens with upstream work absent, and the stage answers OWED naming the upstream act, rather than failing or passing vacuously. | yes |
| AT-08 | 037 | A determination whose only findings are skimmed excludes them from direction and value and names each as owing a dedicated reading; recording that reading and re-running changes the answer. | yes |
| AT-09 | 038, C-22 | A provisional reading can be listed as owed a re-read, and a re-read closes it. | yes, once C-22 says which sense of `provisional` is meant |
| AT-10 | 040 | Every live `pending` determination has a gap, and every such gap can be the stated cause of a search. | yes |
| AT-11 | 039 | An absence finding can point at the code figure it tested, and a mining search can be recorded as run to identify that figure. | yes |
| AT-12 | 029, 033 | A phrase observed in an admitted source can become, through adjudication, a term and then a parameter, without hand SQL; a declined term carries its reason. | yes |
| AT-13 | 027, B14 | After a parameter is added, the sources read before it are listed as not yet read for it. | yes |
| AT-14 | 027, 030 | A figure from a source filed under one slug can govern a determination of a parameter researched under another, and carries a follow-up tag. | yes |
| AT-15 | 031 | A search can be logged for a parameter with no slug and is refused when it names neither a slug, a parameter nor a mined source. | yes |
| AT-16 | 021, 048 | A zero-result search is stored, cannot be deleted through the sanctioned path, and states which of three causes applies. | yes |
| AT-17 | 036 | The set of deferred acts (mining, searches, readings) older than a stated age can be listed by one query. | yes |
| AT-18 | 018, 019 | Retiring a source, a figure, a parameter and a determination leaves each row present with a status, and the next identifier issued is higher than any ever used. | yes |
| AT-19 | 020 | A retired row appears in no view and no rendered output. Run on a scratch copy that contains at least one retired row of each kind; a 0-row subject proves nothing. | yes |
| AT-20 | 025, 009 | Changing a column the engine reads, on a figure under a live determination, is refused or is reported as a stale determination by a check that examined at least one live determination. | yes |
| AT-21 | 025 | Re-running the engine on unchanged inputs reproduces the stored state, marker and derivation hash for every live determination. | yes |
| AT-22 | 024, 082 | No live `stated` or `provisional` determination lacks a governing link; none flagged regulatory-only is `stated` or marked above ○. | yes |
| AT-23 | 054, 060, 062 | For any concept, one query returns, per in-scope language-and-jurisdiction pair, exactly one of: form present (with locator), searched and none found, not yet searched. | yes |
| AT-24 | 058, 059 | No alias marked as model-generated or unattested is used as vocabulary by any writer or view; each is usable only by a search that is flagged. | yes |
| AT-25 | 055, 056, C-04 | A concept can be stored whose first and only attested form is non-English, with an English label marked as descriptive and not counted as an attested English form. | yes; expected to expose C-04 |
| AT-26 | 057 | Two forms of one concept in one language and jurisdiction resolve to the same concept; one form used for two concepts is recorded as a conflation, not merged. | yes |
| AT-27 | 063, 064 | A search for an out-of-scope jurisdiction or scoped-out language is stored only as a deferral with its reason, and the in-scope set is read from the base, not from a list in code. | yes |
| AT-28 | 065, 093, C-08 | Every jurisdiction value in every table resolves to one declared vocabulary; adding a member requires no change to any script. | yes |
| AT-29 | 062, 041 | Coverage for a parameter is computed from the base pairs joined to logged searches; no table or file stores coverage separately. | yes |
| AT-30 | 068 | A determination whose governing figures use two notations carries both; a converted notation is marked derived, and an inexact one is marked inexact. | yes |
| AT-31 | 069, 016 | The comparison table for a parameter has one row per in-scope jurisdiction, each traceable to a figure and its source; a jurisdiction with no figure is not shown and its absence is classified (AT-23 style). | yes for data; page form needs a reading |
| AT-32 | 073, 076 | A figure concerning two codes of one model is stored once with two links; a determination's lens set lists every model its governing figures carry. | yes |
| AT-33 | 074, C-13 | No determination row exists for a parameter × lens with no figure; for such a cell a query still distinguishes not relevant, not yet researched and researched-empty. | yes; expected to expose C-13 |
| AT-34 | 075, 077 | A determination with only a medical code is refused; a figure tagged for everyone reaches only a determination for everyone. | yes |
| AT-35 | 044, 083 | A page can be produced for a source (its citation and the determinations that use it) and for a parameter, reading only the database; deleting every generated file changes nothing rendered. | yes |
| AT-36 | 084, C-01 | Each stored render row points at one determination and can be shown stale when that determination or one of its sources changes. | yes, once OW-1b and OW-1c are answered |
| AT-37 | 087, 089 | The same cell rendered for each of the four audiences carries the identical state, marker, value and flags. | yes |
| AT-38 | 085, 026 | A rendered page cites nothing that is not a source row, and uses no wording that calls a value correct or recommended. | citations yes; wording no (needs a reading) |
| AT-39 | 086, 088 | Filters precede content; the page passes the accessibility tests recorded for it, with the date and build recorded. | partly; a screen-reader pass is not mechanical |
| AT-40 | 010, 012 | No writer at a later stage updates a row of an earlier stage in order to record that it was used. | yes, by reading the writers |
| AT-41 | 090, 091 | A full run for one request leaves the canonical database's hash unchanged until a migration is applied, and its rows and any tooling change are in separate changes. | yes |
| AT-42 | 046 | A run that meets an owner-gated question stops and produces a prompt with context and options; no answer saved on a page is acted on before a ledger entry quotes it. | partly |
| AT-43 | 002, C-11 | Each stage's contract entry conditions are consistent with "synthesize judgments, specify syntheses", and every stage has an entry condition for each direction it can be entered from. | yes, by reading the contract; fails today on the text read here |
| AT-44 | 003, 095 | A run that crosses a boundary backward emits the same boundary record a forward crossing does. | yes |
| AT-45 | 042 | The criteria listed under a technique category and those listed under a room that uses them are produced from the same rows. | not testable until rooms are read by a page (PS:5056) |
| AT-46 | 045 | An element's page lists the live determinations of its parameters through a typed pointer and no row is filed under the element. | yes |
| AT-47 | 066 | No non-English journal article is filed as grey without a recorded warrant. | yes |
| AT-48 | C-02 | — | not testable: the prose does not say what language a page is in |
| AT-49 | C-03 | — | not testable: the prose does not say whether a determination varies by jurisdiction |

---

## 5. Self-attack: the five weakest points of this ledger

1. **Re-entry has no owner sentence behind it.** REQ-003 is the hinge of D1, and its warrant is a ledger paragraph adopting an antagonist finding of 2026-08-21, plus CLAUDE.md. The owner's own words on direction are a clause in a commission to a critic (REQ-004), relayed statements that are not in the ledger (REQ-005), and the objective itself. Everything in section 3 about entering judgment, synthesis, specification and render from downstream is my construction (C-10). If the owner means something narrower by "all directions" — for instance only the four named backward edges plus the evidence entry — a large part of section 3 and AT-07 over-reach.

2. **Three requirements rest on notes, not quotes.** REQ-008 ("reworked at any stage") and the strong form of REQ-016 ("verifiable AND traceable … backward and forward") come from `workplan/2026-10-30-ramp-spec-pages/owner-rules/`, which are an assistant's memory files of owner direction from a local session. I found no transcript line for either. REQ-005 comes from statements relayed in a design document that itself says they are unrecorded. I kept them because they are the closest the record comes to the objective, and flagged the class on each row; a strict reader should treat all three as unproven.

3. **I imported at least three software-engineering assumptions the owner did not make.** (a) REQ-012, that an upstream row is never rewritten to record downstream use, is session reasoning inside the ledger; the owner's rule is about not copying facts, which is not the same as immutability. The whole "re-entry adds, never rewrites" rule in section 3 stands on it and on retire-in-place. (b) The request object and the five answer verbs in section 3.9 are mine; the owner has never described a request, and D2 itself is the assistant's decomposition. (c) "A stage answers OWED rather than failing" assumes stages are callable units with return values. The prose describes stages as groups of tables and acts performed by a session.

4. **On the two words the objective adds — languages and jurisdictions downstream of research — I am reading silence.** REQ-071 is an assumption. The reading in C-03 that a determination is jurisdiction-neutral, and both readings of C-02, are mine. The only requirements about languages past the research stage that carry owner words are about notation and units (REQ-068). Section 3's "neutral identity required" entries for judgment through render are therefore inference from base-stage rulings, and could be wrong in either direction.

5. **Sources I could not pin, and one breach of independence.**
   - CLAUDE.md attributes "read from the database when rendered" to the owner on 2026-08-27. The only owner words I found are quoted in the ledger from the header of a deleted migration (PS:1658-1659); I did not find the original statement or its date.
   - "The judgment object is the **canonical parameter**" (REQ-072) is ledger text recording an option the owner selected, not owner speech.
   - The dossier's verbatim file omits the ledger span PS:1146-2547, which holds the rulings of 2026-08-25 to 2026-08-28 that fix the spine, the hand-offs, the lenses and the determination's subject. I read the rule headers of that span and these parts in full: PS:1234-1380, 1451-1712, 1842-2049, 2298-2345, 2454-2547. I did not read the rest (PS:1384-1450, 1713-1841, 2050-2297, 2346-2453) beyond its headers, so a qualification in those lines could have been missed.
   - `sessions/` was searched with `grep -r` on chosen terms, not read. A ruling worded otherwise would not have been found, and I do not report any ruling as absent on that basis.
   - **Independence.** The brief keeps this leg from reading what exists. I read `dossier/26-stage-render.md` in full and the table, foreign-key and view listings of `dossier/30-data-tables.md` §30.1-30.3, which show row counts, the absence of writers for the render stage and which tables no row can enter. I used them for names only, but I saw them, and the handshake should weigh my render and base sections with that in mind. I also read two ledger passages that describe built behaviour (PS:4560 on what the writers guard; PS:4344 on the coverage views) and cited them as ledger text.

---

## 6. What was read

- **In full:** `CLAUDE.md`; `dossier/00`, `01`, `40`, `41`, `43`; `dossier/42` except `governance/mission-PROVISIONAL.md` (superseded by its own header); `governance/pipeline-contract.yaml`; `governance/stage-map.yaml`; `governance/pipeline-operations.md`; `governance/conceptual-model.md`; `governance/research-contract.yaml`; `governance/jurisdiction-philosophy.md` (through `dossier/42`); the five files of `workplan/2026-10-30-ramp-spec-pages/owner-rules/` cited above.
- **In part:** `governance/evidence-architecture.md` (§4.5, §5, §6 and an outline of the rest); `decisions/DR-2026-08-19-…` (§A, §B, §C, §11, §12.5, and every line matching language, jurisdiction or direction); `architecture/navigation-modes.md` (§1-§3, templates 5-7, §5.4, §6); `architecture/page-templates.md` (shared components, template 1's facets and rules, templates 5-7); `references/project-standards.md` outside the dossier's sections (the parts listed in self-attack 5, and PS:118-139, 612-632, 1146-1182); `workplan/pipeline-state-graph/IDEAL-GRAPH.md` lines 1-75; `RULINGS.md` lines 35, 54, 305; `governance/owner-browser.yaml` lines 905-975; `decisions/DR-2026-07-24-lang-jur-map-roles.md` lines 1-60; `_archived/governance/pipeline-map.yaml` lines 70-84 and 150-172; the owner's messages in `transcripts/harness_4a95df3b/main.jsonl`.
- **Not read:** `scripts/`, `scripts/migrations/`, `data/guidebook.db`, `governance/check-registry.yaml`, `dossier/10`-`13`, the bodies of `dossier/20`-`25`, `governance/tier-system.md`, `governance/evidence-methodology.md`, `governance/held-tensions.md`, `sessions/` (grep only).
