# project-standards.md — current-state extract, part 6 (source L6164–L7392)

Read-only extract. Owner words are quoted verbatim; everything else is the recorder's reduction. "[unratified reading]" marks a recorder's [ASSUMPTION], never the owner's. Within this slice, later entries are applied to earlier ones and the result is attributed to the later date.

---

### 2026-11-13 — tenth set: T-4 agreement rules (OR-5b, OR-6c), floor marker (OR-22b), code route (OR-23b), element pages (OR-14b), scan batches (OR-25), "barrier-free path of travel" (OT-2), order of the three criteria (OI-14), mobility crossings and edges (OI-03, OI-48, OI-49, OI-50) [L6164-L6215]
Owner words:
- OR-5b (first a link only): "https://equator-network.org/"; then: "Yes, PRISM for systematic reviews/meta-analyses, academic rigour re PubMed for any other study outside those bounds, and then ISO for T4-6 as relevant"
- OR-6c: selected "Any different tiers" and added: "Co-1 and T1 are same value"; then answered "Yes, both (1) and (2)" to the assistant's text: "(1) Co-1 against T2 (or lower): the Co-1 figure is stated and the T2 dispute noted, as for T1; (2) Co-1 against T1: same rank, so neither is stated over the other, and the divergence waits for an approach written by an Opus-class session (the same applies to two sources of the same tier)." (the block is the assistant's wording, affirmed by the owner)
- OR-22b: selected "The study's own band"
- OR-23b: selected "Yes, for T4 to T6"
- OR-14b: selected "Written by the pass"
- OR-25: selected "No cap; one source (Recommended)"
- OT-2: selected "Approve"
- OI-14: selected "Yes: 1, then 2, then 3"
- OI-03: selected "Yes, as proposed"
- OI-48: selected "Accept"
- OI-49: selected "Confirm both"
- OI-50: selected "Confirm both"

In force:
- OR-5b (partly answered): Co-1 soundness test named: reporting guideline for systematic reviews/meta-analyses; "academic rigour re PubMed" for other studies; ISO/standards instrument for T4–T6. [unratified reading] "PRISM" = PRISMA. [unratified reading] "ISO for T4-6" = the standards body's own instrument (ISO or national standard) is the test for the regulatory stratum.
- OR-6c: divergence between different tiers: the higher tier's figure is stated and the lower tier's dispute noted. Co-1 and T1 are one rank; a Co-1 vs T1 divergence (or any same-tier divergence) states neither over the other and waits for an approach written by an Opus-class session. Design range unchanged. [CHECK: the tier-ranking element of OR-6c is later addressed by the 2026-11-14 harm-test answer, L7173-L7187, which says neither tier nor stratum decides which value is best; that entry says edits to OR-6c follow the adjudication.]
- OR-22b: a floor claim confirmed by absence reads the band of the verified, retrieved study that confirmed it; the regulation-only ○ rule does not apply to it.
- OR-23b: an unretrievable code or standard (T4–T6 only) keeps its tier and may anchor below the weak band when cited by jurisdiction, standard number and clause; other kinds of source still need the academic route.
- OR-14b: the specifications pass writes an element-level determination from the related parameters' determinations (new stage output: table and rule version, built in a tooling PR). Ends the R17 deferral of cross-parameter synthesis tables for the element case only. The element is still never a container that figures are filed into. A task for it is to be filed; T-037 builds no element page until it has merged.
- OR-25: no extraction cap on scans; one source is the review unit; batch scans by source (D-3, T-105).
- OT-2: the drafted definition and scope note of "barrier-free path of travel" (as in `governance/owner-browser.yaml`, OT-2) are approved; mint the term from observation 68 with `db.py add-term` in a data PR, citing this answer; observation 71 is untouched and waits on its own prompt. [CHECK: see OD-52 referral, L6544-L6552, on the term's reach.]
- OI-14: the three criteria are ordered integrity/rigour/provenance, then legibility, then coverage, from 2026-11-13; not retroactive (decisions already resolved on that order stand).
- OI-03: mobility crossings: `WHEEL` → d465, d420, d410 (beside the `SCI` crossings T-102 judges to hold for wheelchair users); `LLD` → d450, d455; `WALKAID` → d450, d465 (moderate, contextual), per `tasks/T-102-design.md` §§6a, 7. T-102 writes them with stated confidence and mechanism.
- OI-48: a person with an incomplete spinal cord injury who walks is placed by aid (`WALKAID`, or `MOB` with ICF d450/d455), never under `WHEEL`; the injury and level are held in the medical lens and ICF b-codes; `SCI` has no identity code of its own. [CHECK: CLAUDE.md §6 says the medical lens was deleted by the owner on 2026-11-16 (outside this slice); the "medical lens" clause here may be affected.]
- OI-49: `UPL` display name "people with upper-limb differences or disabilities", category `general`. `LLD` description: "People with a lower-limb difference, from limb loss or from birth, whether or not they use a prosthesis. The prosthesis, where a figure concerns one, is recorded on the figure, never as a code." T-116 and T-025 use this wording.
- OI-50: (a) upper-limb prosthesis user is `UPL`; lower-limb is `LLD` with the prosthesis named in `device_class`; (b) identity codes are not mutually exclusive (e.g. `LLD` and `WHEEL`). The two [ASSUMPTION] marks of the eighth and ninth sets are ratified by OI-50.
- Applies to: any session building the T-4 agreement task, writing a determination's marker or value, tagging/crossing a mobility figure, minting or rewording `UPL`, `LLD`, `WHEEL`, `WALKAID`, building an element page, batching a scan, or minting "barrier-free path of travel".

Open:
- [OPEN] OR-5b edge 1: whether "academic rigour re PubMed" means indexed in PubMed or judged by the standard PubMed-indexed work meets (the first collides with research contract R5: non-indexation is an indexing fact, not an evidence-quality fact).
- [OPEN] OR-5b edge 2: how a DPO position statement or lived-experience publication (no reporting guideline, not a study) is shown to be sound.
- [OPEN] OR-5b edge 3: whether the three-part test is for Co-1 only or every tier. T-4 asks these three first.
- [OPEN] Whether `UPL` has children (not asked; none invented).

---

### 2026-11-13 — link table for a figure's lens codes (OD-39, OR-1c; T-018) [L6217-L6233]
Owner words: (quoted from earlier entries outside this slice) OR-1c: "link table unless that is more prone to errors"; OD-39: "Yes, the 2026-11-06 ruling supersedes that clause". Recorder entry (T-018 executor) — not itself an owner statement.
D-0182 words quoted (owner 2026-09-01, outside slice): "a link MUST be tied to at least one"; "ideally it ties into many".

In force:
- The 2026-11-06 link-table ruling (OR-1c) supersedes the clause of the 2026-08-28 ACTION that forbade a `population_*` link table.
- A figure's lens is held as one row per (figure, lens code) in `extraction_lens_links`, read through `v_live_lens_links` (the one read surface), never from the four lens columns on `source_value_extractions` (held NULL by CHECK, not dropped because committed data migrations INSERT them).
- Write lens via `add-extraction` / `derive-extraction` (repeat the lens flag; `--lens-basis` and `--lens-basis-text` required) and `add-lens-link` / `retire-lens-link`.
- A research batch captured before the link-table migration that holds an `INSERT` of a lens column must be captured again through those verbs.
- A link row states exactly one code by CHECK (T-018's design choice). D-0182's "at least one lens" rule lives in the writers and the blocking `test_db_integrity` case T018-05.
- "Never two lenses in one row" does not stand as a ruling (overturned by D-0182).
- Derive the tables carrying lens columns, never list them: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);L={'identity_code','icf_code','needs_code','medical_code'};print([(t,[x for x in (r[1] for r in c.execute(f'pragma table_info(\"{t}\")')) if x in L]) for (t,) in c.execute(\"select name from sqlite_master where type='table'\")])"`. Count carried links: `select count(*), count(distinct extraction_id) from extraction_lens_links where basis='carried'`.
- [unratified reading] The supersession covers a figure's lens codes only, not `specifications` or any other table with lens columns.
- [unratified reading] The rest of the 2026-08-28 ACTION stands as D-0182 left it: typed lens columns with real FKs, lens names in the name (no `population`), `population_code` retired. [CHECK: entry says "four" lenses; CLAUDE.md §6 records the medical lens deleted 2026-11-16, outside this slice.]

Open:
- [OPEN] Whether determinations also take a link table (OI-55); a determination's cell stays a key with one code per model meanwhile.

---

### 2026-11-13 — eleventh set: Edmonton checklist digest — questions and the refusal register [L6235-L6283]
Owner words (relayed; questions, proposals and instructions, not rulings except as noted):
Framing:
> "perform a research pass on this PDF. what do you extract? give me a document with everything you did"
> "use the research approach from pipeline."
> "ie how would you digest this PDF in pipeline"
> "again, you are treating this PDF as if it came up in a research sweep"
> "you must digest it following the pipeline rules"
> "show me a report of what you did for the digest including results"
Questions:
> **Q1.** "best practice is the best/most forgiving/etc of all values/approaches for a given term. isn't it presumptuous to have a best practice column at this stage? differentiate as code floor vs above code floor"
> **Q2.** "what does the workplan plan to do to address all the parameters/subjects within this PDF that are not currently defined as a term in base?"
> **Q3.** "how do we dynamically improve our base for terminology/parameters/concepts?"
> **Q4.** "how do we ensure that we aren't duplicating if we add dynamically, ie find equivalencies and synonyms?"
> **Q5.** "how do we differentiate between something as a clause/branch/subitem for a term/parameter versus its own?"
> **Q6.** "how do you handle different values for a parameter based upon different access needs/ICF codes/identities? or different design modes of universal vs population vs person specific?"
> **Q7.** "how do you handle a commercial versus residential versus public?"
> **Q8.** "and how do you handle whether something is too granular to be valuable versus too encompassing to be useful?"
> **Q9.** "how do you combine things like stair widths and handrails? different parameters, but belonging together in specification?"
Refusal register statements:
> **1.** "it may be worthwhile to have a mechanism whereby when our scripting/pipeline cannot execute something, we explicitly flag it as a gap/issue for future resolution in a register alongside having an agent fix it by hand with correct context so we aren't losing content alongside filling in its resolution and proposed amendments for that gap/issue in register"
> **2.** "that way we aren't held up"
> **3.** "it could be like a layer 2 protocol or something"
> **4.** "refusals will need to be dynamically typed/categorized and read by something so that we can have a proper register of specific instances of refusals as well as a way to understand them as a class so that we are able to point towards area for resolution"
> **5.** "it could also then be a cue to run a script/double check a protocol or skill/etc to ensure that the digest was actually performed correctly"
Instructions:
> "pass off all of my questions and your answers about Edmonton PDT to Fable for adjudication and reconciliation with aim to incorporate into pipeline with view of ensuring best long-term integrity of project, legibility and logical coherence, and disability coverage"
> "you need to consider how to resolve all issues identified"
> "then fold into remediation plan"
> "remember the fable is treating the Edmonton PDF and related questions/concerns I raised alongside your responses subsequently as a case study to be used to improve entire pipeline"

In force:
- Q1's two sentences state a rule: best practice is the best/most forgiving of all values for a term (restating the 2026-10-30 rulings: the most accommodating value for the intended group, an output of determination, not a label on an input); and "differentiate as code floor vs above code floor" is an instruction.
- [unratified reading] Floor vs above-floor is derived against the code stratum of the same parameter and jurisdiction, never typed on a figure; a source's own "code" marking is recorded as root attribution (the code's `ref_id` when held, else `untraced` with the marking quoted); a source's pairing of a higher figure with a code figure is a relation edge; no "best practice" is stored on any input row.
- [unratified reading] Statement 1's "fix it by hand" = the agent records the intended row, its refusal and a proposed amendment in the register, replayed through the sanctioned writer once tooling is fixed (not a canonical row written by hand; that reading is OD-54, open).
- [unratified reading] "layer 2 protocol" = a per-stage protocol (acknowledge, refuse-and-park, replay) on a Layer 1 carrier under a Layer 0 gate.
- [unratified reading] "PDT" = PDF. [unratified reading] the relay quotes the owner faithfully.
- Carriers in the remediation plan (`workplan/2026-11-12-bidirectional-pipeline/`): Q1 → T-035 item 2, T-071 step 3, T-087; Q2/Q3 → T-079 deferred-adjudication arm, T-087, OD-50; Q4 → T-029 item 2 (with T-033); Q5/Q8 → OD-24; Q6 → OD-47, OD-48, T-056; Q7 → OD-49, T-091, T-092; Q9 → T-060 design constraint and T-029; statements 1–5 → T-088, T-089 (OD-54 holds the set-aside reading); "disability coverage" → T-090.

Open:
- The adjudication's eight owner questions are register decisions OD-47 to OD-54; their states within this slice are given in the entries below (OD-49, OD-50, OD-53 resolved under delegation; OD-47, OD-48, OD-51, OD-52, OD-54 referred back, open).

---

### 2026-11-13 — owner question: may OD-40 to OD-55 be resolved by an Opus-class model [L6286-L6302]
Owner words:
> "are you sure you can't resolve these owner decisions using Opus based upon prior rulings, mission/doctrine and project goal?"
> "I don't know the machinery or code"

In force:
- The first sentence is a question, not a ruling.
- The grant reaching OD-40 to OD-55 is the owner's twelfth instruction of 2026-11-12, "You have permission to use Opus for judgment if appropriate here" (not the 2026-11-12 "I guess opus can do it" delegation, which named OD-01 to OD-30 only).
- [unratified reading] The question asks that the twelfth instruction be applied to OD-40 to OD-55 with conditions (a)–(e) of the 2026-11-12 delegation: nothing in an always-DG-NON type (`governance/decision-protocol.md` §2.4) is resolved; no resolution overrides a standing owner ruling (e); each resolution is checked by a second, independent Opus-class instance before reliance (d); judged against the three criteria in OI-14's order.
- Read each decision's state by the gate of the 2026-11-12 convention, never by its `OD-NN:` line. Every delegated resolution is not the owner's words and is reversible by the owner.

Open: none.

---

### 2026-11-13 — OD-40 (delegated): a derived figure's quote and locator [L6305-L6322]
Recorder/delegate entry — not owner words. Owner rulings cited: 2026-08-24 "It is better to have a table cell point to another table cell than to rewrite"; 2026-09-13 "Derived figures are a weighted average of their figures".

In force (RESOLVED UNDER DELEGATION; check: confirmed with corrections applied):
- A derived row stores no quote and no locator; both are its two inputs', reached through its two `derived_from` edges, each carrying its input's verified quote.
- The writer refuses a derived row whose inputs lack a quote or locator, and keeps the arithmetic check.
- A figure a source states in words is a claim row, never a derived row.
- Reversal condition: a derived figure must be shown with a sentence of its own no input supplies, or the owner wants computed figures kept only in prose.

Open: none.

---

### 2026-11-13 — OD-41 (delegated): unit `ratio` to `rise:run ratio` is a reformat [L6325-L6342]
Recorder/delegate entry — not owner words (reads OR-3, "Yes, reformat in place").

In force (RESOLVED UNDER DELEGATION; check: confirmed with corrections applied):
- Stored rows with the bare unit `ratio` are amended in place under OR-3 (same digits and quote, old unit kept in notes); no second row.
- `amend-extraction` gains one branch: a new unit in the notation families is accepted when the old unit stands, on word boundaries, in the new one and the stored figure reads under it.
- Reversal condition: owner says the OR-3 example did not mean these rows, or a source defines its ratio otherwise (rise over sloped length).

Open: none.

---

### 2026-11-13 — OD-42 (delegated): metric-to-metric conversion shown exactly [L6345-L6362]
Recorder/delegate entry — not owner words (reads OR-10).

In force (RESOLVED UNDER DELEGATION; check: confirmed with corrections applied):
- A change of metric prefix (cm→mm, m→mm) keeps the source's digits and is shown exactly.
- Rounding to the nearest quarter inch or 5 mm, on the safe side (OR-10, OD-22), applies only to inch-foot ↔ metric conversion.
- Reversal condition: owner says OR-10's rounding covers every shown converted length.

Open: none.

---

### 2026-11-13 — OD-43 (delegated): when the engine may call a cell `convergent` [L6365-L6384]
Recorder/delegate entry — not owner words.

In force:
- The delegated limit of `convergent` to the clinical (Tier 1–3) and Co-1 axes is superseded in this slice by the owner's answer of 2026-11-14 (thirteenth set, L6566-L6614) and refined by the owner's convergence statements of 2026-11-14 (L6639-L6698); see those entries for the resulting state. OD-43 now reads ANSWERED BY THE OWNER.
- What survives of this resolution (as carried by the 2026-11-14 entries, [unratified reading]): values the same (same value or same range on the parameter's scale) and the anchoring claims can all hold (OR-6b: differing floors that can all be met are not divergent, which is not agreement); a rationale written true of the cell, never "queued" where the definition cannot be met. [CHECK: the "two or more independent roots" condition is turned, in the 2026-11-14 convergence entry, into a count shown beside the word; see L6639-L6698.]

Open: none here (see later entries).

---

### 2026-11-13 — OD-45 (delegated): a logged search whose request never returned results [L6387-L6404]
Recorder/delegate entry — not owner words. Owner principle cited (2026-09-18): 'deferred is okay so long as it runs eventually'.

In force (RESOLVED UNDER DELEGATION; check: confirmed with corrections applied):
- A logged search whose request returned no result list (403 or bot challenge, 429, connection reset, stub page) is a search not run: recorded with `deferred_reason` naming the failure, no absence class, owed a re-run (including the Internet Archive route).
- A zero-result search is read as a finding only where `deferred_reason` is NULL.
- Reversal condition: owner wants a blocked request kept as a finding about a source's reachability.

Open: none.

---

### 2026-11-13 — OD-49 (delegated): building type, a figure's other circumstances, where an element lives [L6407-L6424]
Recorder/delegate entry — not owner words. Owner example cited (2026-08-27): "eg residential, commercial".

In force (RESOLVED UNDER DELEGATION, in the scope narrowed by the owner on 2026-11-14, thirteenth set answer 3; check: confirmed with corrections applied):
- (a1) Building type (use) and interior or exterior are each a typed circumstance on the figure, one value per cell, shown as branches within one determination per parameter and lens set. ("New or existing work" was removed as a circumstance by the owner on 2026-11-14; no code-status circumstance is added.)
- Building type points at the first of the owner's three building levels (2026-08-27). Each building type is minted from an instrument's own scope phrase, in its jurisdiction and language, in a data PR the owner reads (OR-17, E1); the owner's examples are not minted as names. "Public" is adjudicated per instrument.
- Before stored figures are re-tagged, measure on a scratch copy how many cells' headlines OR-2 would empty (counting only the two remaining circumstances), say how a circumstance shared by every figure of a cell is shown, and show the result to the owner.
- (b2) The owner's 2026-08-27 "three tables" ruling stands; an element row, when needed, points at its term and holds no name of its own; any relation between elements is decided in that design.
- Reversal condition: owner wants building type in the key, or elements as terms only, or measured headlines show branching hides a group's difference. Reversal retires vocabulary rows and NULLs typed cells forward.

Open: none here beyond the measurement owed.

---

### 2026-11-13 — OD-50 (delegated): a source that is not a code adding a parameter [L6427-L6444]
Recorder/delegate entry — not owner words. Owner intent cited (2026-10-09): "pull from the major codes, literature and advocacy from major countries".

In force (RESOLVED UNDER DELEGATION; check: confirmed with corrections applied):
- Any admitted source may promote a quantity it states to a parameter in its data PR, under the standing conditions: the source's own phrase (OR-17), minted from an observation, a quantity with a kind (T-020), the owner reading the PR.
- Reversal condition: owner wants parameters only from codes/standards or from two independent sources; reversal retires (never deletes) the parameters added.

Open: none.

---

### 2026-11-13 — OD-53 (delegated): declining held terms in a single-source batch [L6447-L6466]
Recorder/delegate entry — not owner words.

In force (RESOLVED UNDER DELEGATION, as limited on 2026-11-14 by the owner's answer 4 and OD-56; check: confirmed with corrections applied):
- A research batch may decline a held term that an adjudication of its own observations names, only when the term is an element, a lens term or a method, with one stated reason per term, listed in its data PR. It may never decline a quantity (promote it under OD-50 or leave it for T-072).
- T-072's catalogue pass (item 6) reviews these declinations and may revoke any.
- Limitation (2026-11-14, owner answer 4 and OD-56 (b)): a provision whose question is presence (hearing loop, tactile indicator, etc.) is reached by an element pointer and is not declined away; a declination of such a term *as a parameter* stays lawful, but no declination may leave the term with no pointer possible.
- Reversal condition: batch declinations prove inconsistent under catalogue review, or a declined element hides a group no coverage read reports.

Open: none.

---

### 2026-11-13 — OD-55 (delegated): stored row after a second reading of a bare-`ratio` gradient [L6469-L6486]
Recorder/delegate entry — not owner words. Owner words cited (2026-09-16): "retire in place then".

In force (RESOLVED UNDER DELEGATION; conditional on OD-41; check: confirmed with corrections applied):
- Not reached while OD-41 stands as a reformat. If OD-41 is reversed to a new reading, the stored row is retired in place with its successor named, and the note and engine count one claim per pair.
- Reversal condition: owner says a second reading must leave the first live.

Open: none.

---

### 2026-11-13 — OD-44 referral: second source for the blind double extraction [L6489-L6497]
Recorder/delegate entry — not owner words.

In force:
- Superseded in this slice: OD-44 was answered by the owner on 2026-11-14 (thirteenth set, answer 2: "apply recommendations" → option A). See L6566-L6614.

Open: none.

---

### 2026-11-13 — OD-46 referral: language-map codes missing from the jurisdiction registry [L6500-L6508]
Recorder/delegate entry — not owner words. Owner words cited (2026-09-18): "UK is canonical, add BE HR INT ES IT to the enum".

In force:
- OD-46 is the owner's (inclusion/exclusion of jurisdictions is always DG-NON, §2.4 item 4); CLOSED by the gate; ask it in plain form (`OWNER-SHEET-PLAIN.md` question 2); record the answer with `ANSWERED BY THE OWNER`. Not to be resolved under delegation.

Open:
- [OPEN] OD-46 (REFERRED BACK TO THE OWNER). No answer within this slice; an answer may lie after L7392.

---

### 2026-11-13 — OD-47 referral: lens of a figure whose clause names no person, function or need [L6511-L6519]
Recorder/delegate entry — not owner words. Owner words cited: "The population taxonomy remains the owner's"; OD-31 answer: a provision under a general disability heading carries "no identity, only its ICF and access-need lenses".

In force:
- OD-47 is the owner's (population taxonomy, incl. proxy decisions, always DG-NON); CLOSED by the gate; ask in plain form (question 3); record with `ANSWERED BY THE OWNER`. Applies to replaying the Edmonton batch's parked figures.

Open:
- [OPEN] OD-47 (REFERRED BACK TO THE OWNER). No answer within this slice.

---

### 2026-11-13 — OD-48 referral: what `design_scale = 'universal'` states [L6522-L6530]
Recorder/delegate entry — not owner words. Owner record cited: directive 2026-07-13 ("T4–6-only determinations are Universal-Mode regulatory determinations"); Design Modes rule ("Universal Mode = Universal Design / Code Compliance").

In force:
- OD-48 is the owner's (Design Modes are mission doctrine; DR-2026-07-12 G1(a) and the 2026-11-12 OD-31 option conflict; neither is treated as superseded by implication); CLOSED by the gate; ask in plain form (question 4). Applies to T-056, T-115.

Open:
- [OPEN] OD-48 (REFERRED BACK TO THE OWNER). No answer within this slice.

---

### 2026-11-13 — OD-51 referral: municipal advisory committee's document and Co-1 standing [L6533-L6541]
Recorder/delegate entry — not owner words.

In force:
- OD-51 is the owner's (evidence-tier definitions and the Co-1 corpus always DG-NON, §2.4 items 3, 6); CLOSED by the gate; ask in plain form (question 5). Applies to re-tiering the Edmonton checklist.

Open:
- [OPEN] OD-51 (REFERRED BACK TO THE OWNER); also turns on OR-5b's open second edge.

---

### 2026-11-13 — OD-52 referral: "barrier-free path of travel" as the Edmonton checklist uses it [L6544-L6552]
Recorder/delegate entry — not owner words.

In force:
- OD-52 is the owner's (OT-2's definition "a circulation route through a building" is the owner's approved wording; the Ontario code, REF-01013, applies the phrase to "floors or walks", not before the owner at OT-2); CLOSED by the gate; ask in plain form (question 6). Applies to adjudicating the Edmonton path phrases.

Open:
- [OPEN] OD-52 (REFERRED BACK TO THE OWNER).

---

### 2026-11-13 — OD-54 referral: writing a canonical row by hand when a writer cannot hold content [L6555-L6563]
Recorder/delegate entry — not owner words.

In force:
- OD-54 is the owner's (option B would set aside CLAUDE.md rules 3 and 10); CLOSED by the gate; ask in plain form (question 7), last. Meanwhile the eleventh set's reading (option A: register, park, replay) is the only one acted on.

Open:
- [OPEN] OD-54 (REFERRED BACK TO THE OWNER).

---

### 2026-11-14 — thirteenth set: convergence, the second source, new/existing work, provisions of presence [L6566-L6614]
Owner words:
- Answer 1: "yes convergence is possible too, and it helps define most common practice (which isn't same as best practice)"
- Answer 2: "apply recommendations"
- Answer 3: "noted. apply recommendations. do not worry about existing/renovating and code as we are only concerned about design itself"
- Answer 4: "hearing loops and other similar provisions should be included"

In force:
- OD-43 (ANSWERED BY THE OWNER): "agreement between any two kinds of evidence counts as convergence; convergence defines most common practice, which is not best practice". (Reach widened later the same day: see L6639-L6698.)
- [unratified reading] Answer 1 selects: agreement between any two kinds of evidence counts as convergence, symmetric with OR-6/OR-6c's "divergent" for any two tiers (incl. two research studies, or a research study and a professional guideline).
- [unratified reading] Other conditions stand: same value or same range on the parameter's scale; anchoring claims can all hold (OR-6b); governing figures on two or more independent roots, shared-root sources counting as one (H1). [CHECK: the roots condition is reshaped by L6639-L6698.]
- [unratified reading] A convergent assessment states most common practice; a convergence output is never labelled, stored or rendered as best practice; best practice stays the most accommodating value in the parameter's recorded direction.
- The definition in `governance/evidence-methodology.md` (`agree on the parameter value or range`) and the Co-1-C rendered sentence are touched by this answer and are swept by T-068 (with their marked supersession written there).
- OD-44 (ANSWERED BY THE OWNER): "A". [unratified reading] Option A: one of the two research studies with most findings corpus-wide (the 2015 study of wheelchair users pushing up ramps), fetched again first. Use the source T-070 §3's query prints for "T1/T2 source with the most finding rows, corpus-wide" — re-run it, do not trust an id. The owner still launches the raters.
- Answer 3 → OD-49 narrowed: "new or existing work" leaves as a circumstance; building use and interior/exterior remain; no code-status circumstance. OD-49's headline measurement stands (counting only the two remaining circumstances) and is shown to the owner before any re-tag; no heading rule is set now.
- [unratified reading] "do not worry about existing/renovating and code as we are only concerned about design itself" is a scope statement: the guidebook concerns the design of the environment itself, not renovation/retrofit and not code-compliance status.
- [unratified reading] "code" here means a figure's code-compliance status as a circumstance only; it does not touch code floor vs above code floor derivation, T4–T6, or the weak-band flag.
- Answer 4: provisions whose question is presence are included (scope statement of inclusion). The mechanism was decided by the owner as OD-56 (b) (next entry). Meanwhile no research batch declines a provision of presence.
- [unratified reading] Such provisions (hearing loop, visual alarm, tactile walking surface indicator, TTY, tactile signage and the like) are included with a determination or mark of their own.
- Carriers: T-068 (answer 1; T-037, T-032 the render note), T-070 (answer 2), T-091 and T-092 (answer 3).

Open:
- [OPEN] Whether agreement within a stated tolerance counts — answered by the owner's working view (5%) on L6639-L6698; parts remain open as OD-66.
- [OPEN] How most common practice is shown on a page, and whether stored as its own value (render's, T-037 under OD-12).
- [OPEN] What becomes of a figure a source states only for existing or altered buildings (a renovation relaxation): read into the corpus at all, or read and shown without the circumstance. T-091 reports how many; decides nothing.

---

### 2026-11-14 — OD-56: how a provision whose question is presence is included [L6616-L6637]
Owner words: "b" (reply to the options "(a) a presence quantity, so such a provision becomes a parameter with its own determination; (b) an element-level list of the provisions an element should carry; (c) a separate typed register of provisions; (d) prose only, which your answer 4 rules out.")

In force:
- OD-56 (ANSWERED BY THE OWNER): "(b) an element-level determination lists the provisions an element should carry; a provision is not a parameter".
- [unratified reading] "b" selects option (b). (Entry says: if the owner meant otherwise, this entry is to be superseded on contact.)
- A provision of presence is not a parameter and no value is computed for it.
- The element-level determination (T-060) points at the provision terms (`terms.term_id`) the element should carry and at the source statements that say so (`observed_terms.observation_id` or `source_value_extractions.extraction_id`), as well as at its parameters' determinations (`specifications.specification_id`) and the relation rows crossing them; it holds no value column (its design names the test that it has none). The provision gets its mark only through that pointer, on the element's page.
- T-029 carries the pointer kind: an element-to-provision kind (`element has provision`) in its CHECK, with tests that it is accepted and an undeclared kind refused.
- T-072 item 6 and T-087: "a provision of presence is reached by an element pointer (OD-56), not declined away".
- Options (a), (c), (d) not taken. OD-56 needs no delegated resolution and no check line.
- Which held terms are provisions of presence is judged term by term by the session writing the pointer, never by a curated list (rule 8).

Open:
- [OPEN] How a source's statement "a hearing loop should be provided" is typed (observation–element relation, or term-to-term pointer with the observation as warrant): T-060 design / T-029 pointer kinds.
- [OPEN] Where a provision belonging to no one element is reached (TTY at a service counter, building alarm system): T-060 names the element or reports none.
- [OPEN] What mark a provision carries on the element page, and whether ●/◐/○ read as for a value (render's, T-037 after T-060).

---

### 2026-11-14 — convergence means values coming together; clusters, tolerance, ranges, bound words [L6639-L6698]
Owner words (in order):
> "convergence just means values coming together. why wouldn't that make sense for evidence methodology intuitively"

> "it's just that different tiers of evidence have different importance, so tier 1 item convergence is more significant than tier 4 item convergence
>
> but you can still converge across tiers like a tier 1 and a tier 6 proposing same value"

> "this is why we differentiate most common practice versus best practice. convergence is not evidence of best practice but most common practice"

> "and if a different set of evidence for a parameter converge together on the same value but there are other sets of evidence for a parameter  converge together on a different value, then we have divergence between two sets of converged values
>
> and that itself should cue further investigation/analysis to see what is happening for that parameter"

> "different values because different ICF/access need/identity targeted?
>
> or is there a clause somewhere that hasn't been picked up that modifies the parameter? are there conditions? is it step-based? triggered?"

> "tolerance should be within 5%, I think, but given the strictness of application it's often the same values"

> "other reasons for divergence vs convergence may be residential vs non-residential, fully universal design vs limited mobility design, etc"

> "it may also speak towards RANGES of values / eg a mirror mounted between 1000mm aff to 1200mm"

> "oh God we need to include ranges"

> "at most"
> "minimum"
> "maximum"
> "within"

> "etc"

In force:
- OD-43's answer line stands, refined: convergence reaches agreement among any sources, codes alone included, and across any tiers (e.g. a Tier 1 and a Tier 6 source). OD-43 status unchanged (ANSWERED BY THE OWNER). The question whether agreement among regulatory sources alone is convergence is decided: it is.
- The T-068 carve-out keeping code-only agreement `pending_assessment`, and (to the same extent) the delegated OD-43 resolution, are overtaken.
- [unratified reading] Convergence is descriptive (values coming together); corroboration is a separate fact: the independent-roots count (H1), shown beside every convergence statement and never implied by the word. The `single_axis` clause "Tier 4–6 only … No convergence or divergence assessment is possible" and the `convergent` clause "carries higher confidence than either dimension alone" do not stand as written.
- [unratified reading] Significance is weighted by the tiers of the converging sources (T1 convergence more significant than T4), read from the tiers and weight bands listed (`schemas/tier_derivation.py` `band(tier, evidence_type)`), never as a numeric score. Cross-tier convergence is not a lesser status. Roots still counted honestly (one root if the code took its figure from the study).
- Every convergent statement carries: number of sources, number of independent roots (from `v_value_independence_rows`), each converging source with tier and band; no column and no score added.
- A convergence among codes alone is labelled most common practice with the code-derived flag (`regulatory_stratum_only`) and the convergence-not-evidence caveat; never best practice; never raises confidence.
- `convergent` asserts no higher confidence. A convergent assessment changes neither the best-practice value nor the marker (●, ◐, ○); T-068's test guards that. (Re-check the code paths; do not trust: `grep -n -A14 '^    marker = None' scripts/assess/assess_cell.py`; `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select type,name from sqlite_master where sql like '%convergence%' and type in ('view','trigger')\").fetchall())"`.)
- [unratified reading] Convergence is never an input to selecting best practice; best practice is the most accommodating value in the recorded direction.
- Clusters: a parameter whose evidence forms two or more clusters on different values is divergence between sets of converged values and is an investigation cue: the engine records an open gap row (existing gaps mechanism and category; no new vocabulary) naming the clusters by the command that lists them; `v_divergence` and `/batch-done` list such parameters as the investigation queue. T-068 writes `divergent` for two or more clusters where T-059's rule applies.
- [unratified reading] The cue is never resolved by choosing the larger cluster (frequency is never evidence). It is additive to OR-6/OR-6c (tier-level rule not replaced).
- Investigation checklist (owner's statements 5 and 7, questions not rulings; [unratified reading] a starting list, not closed): different groups targeted (ICF, access need, identity); an uncaptured modifying clause; conditions; stepped series; trigger; building use (residential vs non-residential, public/commercial — T-091 carrier); design mode (universal vs a named group: `specifications.design_scale` on the determination side, lens links on the evidence side). A divergence no check separates is reported "undetermined". T-068's section "What the investigation looks at" specifies a read-only diagnostics reader; the task to build it is owed (OI-57).
- Ranges: ranges are included; every figure is grouped as the interval it states, points the special case (intervals already derived by `dbcore.bound_on_scale`: point (v,v); floor (v,open) for `>=`/`>`; ceiling (open,v) for `<=`/`<`; range/`between` (a,b); strictness not modelled). No figure is reduced to a point or midpoint; both bounds kept.
- [unratified reading] Two interval relations kept apart: **consistent** (overlap or within tolerance of overlap — OR-6b's "can all hold") and **the same** (each finite bound within tolerance, same sides open). Working reading groups by the same and reports consistent beside it (a range spanning two clusters is printed as spanning them); the choice is the owner's (OD-66 (c)).
- Bound words: land as the comparator their direction names, in extraction guidance prose only (one home: `skills/run-pipeline_SKILL.md`, "the comparator is read from what the wording says about direction"); no code reads a word list.
- [unratified reading] Mapping: "at most", "maximum" → `<=`; "minimum" (and "at least") → `>=`; "within" never mapped silently: with two figures → `between`; with one figure → `<=` on a deviation. Any other wording mapped by direction; unclear direction → kept as written (`value_as_written`, `claim_text`), no comparator guessed, writer refuses. The source's "within" (a bound) and the owner's tolerance "within 5%" (grouping) are kept apart.
- Tolerance: working tolerance for cluster membership is 5% ("I think": the owner's working view, reversible). [unratified reading] Relative, |a − b| ÷ larger ≤ 5%, on a common scale, applied to points and to each bound of a range; until the owner says otherwise, relative to the larger. Stored and shown values stay exact; the tolerance is one value in one home read by engine and validator. "often the same values" is an observation, not a second rule.
- T-068 edge tests: 4.9% apart clusters; 5.1% does not; exact match clusters; stepped series 1:20, 1:16, 1:12 stays three clusters; a point inside a range is consistent with it; a point outside by more than 5% of the nearer bound is not; two overlapping ranges are consistent; 1000 and 1200 as points are two clusters while a 1000–1200 range is reported as spanning them; list by command the live cells where the tolerance changes a cluster vs exact equality.
- T-068's caller sweep corrects `governance/evidence-methodology.md` (`convergent`, `divergent`, `single_axis` definitions; Co-1-C sentence; `single_axis` Tier 4–6 voice row, which joins code convergence to "best practice"; §2.3 richness criteria where code convergence decides `provisional` vs `pending`), the engine branch hard-coding `single_axis` for a regulatory-only cell, and the validator rule that `convergent` needs two or more axes; each with marked supersession and machine pair in that PR. No doctrine file is edited by this entry.

Open (now registered as OD-66, L7367-L7389):
- [OPEN] Tolerance relative to larger or smaller value; whether one tolerance serves every quantity kind.
- [OPEN] Grouping by "the same" vs "consistent".
- [OPEN] Status of two clusters on differing floors that can all be met (`divergent` vs OR-6b's spread in the note); the cue applies either way.
- [OPEN] How most common practice, tiers and clusters are shown on a page (render's, T-037).
- [OPEN] Whether converging regulatory sources are recorded in `convergence_sources` (role CHECK names only clinical, co1, co2, down_weighted, discounted); T-068 derives from governing extraction links instead, adding no column, role or score.
- [OPEN] How a cluster is ranked for T-059's rank rule when its sources span ranks.

---

### 2026-11-14 — what "best practice" is, and how the term is swept [L6702-L6720]
Owner words:
> "best practice is the best/most forgiving/etc of all values/approaches for a given term" (2026-11-13, eleventh set)
>
> "but how many errors and issues are occurring because your understanding of best practice, which can be found all across our tools and doctrines etc, keeps understanding it as the most common figure"
>
> "I think we need to run this sweep carefully and comprehensively, which means we ensure that our grep etc is paired with a contextual reading of the term. The most accommodating value is one that has been identified in our research, which in turn means that it is based in the evidence that we have collected enough if the research source itself simply asserts the value"

In force:
- Read "best practice" as the most accommodating identified value, never as the most common figure; where a passage says otherwise, name the conflict and do not copy the wording.
- A sweep of the live surface (`git grep -i -E 'best[ _-]?practice'`, excluding frozen records and data migrations), each hit paired with a contextual reading and classified by sense, flagging conflicts; amendments go through this ledger.
- [unratified reading] Best practice is chosen from values already held as extractions, not computed outside them.
- [unratified reading] A source that merely asserts a value makes it eligible; the source's tier sets marker and weight, not eligibility.
- [unratified reading] Most common practice (convergence) and best practice are different quantities.

Open:
- Rename to "ideal": meaning settled later the same day; the word question is OD-62 (default: no rename), L7261-L7293.

---

### 2026-11-14 (later) — the most accommodating value is relative to the lens and the context [L6724-L6738]
Owner words:
> "The most accommodating, then, is the one that best responds to an ICF/access need/identity within whatever context, and that means it is the ideal from what we have found"

In force:
- A best-practice value belongs to a cell and its context; a figure offered without either is incomplete, not wrong.
- [unratified reading] "Most accommodating" is read per cell and per context (cell key = a parameter by at least one lens; circumstances are the context), never one figure for a parameter across every lens and circumstance.
- [unratified reading] "the ideal from what we have found" = ideal among identified values, not beyond them.
- Sweep flag `TENSION` for a passage giving one best-practice figure for a parameter with no lens or context.

Open:
- [OPEN] How a cell's context is stored (T-091's typed circumstances is the working home, not a ruling).

---

### 2026-11-14 (later still) — best practice, ideal and most accommodating are one definition [L6742-L6756]
Owner words:
> "This means that my definition of best practice IS the same as ideal IS the same as most accommodating"

In force:
- The three words name one quantity; read them as one; name a passage that ranks them apart; do not rewrite it without a ledger entry.
- [unratified reading] One quantity = the value, for a cell and context, that best responds to the lens among identified values.
- [unratified reading] A passage ranking "ideal" and "best practice" as different rungs (the prose register's Ideal → Best Practice → Acceptable → Minimum, `skills/prose-style-checker_SKILL.md`) conflicts with the definition. (The prose register is to be rewritten: OD-60, L7297-L7344.)

Open:
- Which word the project writes: OD-62, default no rename (L7261-L7293). Rename of `best_practice_synthesis` and `v_best_practice` not decided.

---

### 2026-11-14 (last) — three terms: best, most common and floor [L6760-L6774]
Owner words:
> "we have best, most common, and floor"

In force (classification superseded the same day by the four figures, L6796-L6810; the distinctness rule stands):
- Name which quantity a value is; do not use one word for another (e.g. "best practice" for the code floor or for the most common figure is a conflict).
- [unratified reading] best (ideal / best practice / most accommodating), most common (convergence), floor (code floor) are distinct; this does not rank them by strength of evidence (the marker's job).

Open: none beyond later entries.

---

### 2026-11-14 — the guidebook shows data and does not determine; minimum is a fact, acceptable is a judgment [L6778-L6792]
Owner words:
> "remember that we are showing data, not determining. the minimum is a factual data point. acceptable isn't relevant as that's a value judgment. our ideals are simply data points"

In force:
- Show the value and what it rests on; do not say it is acceptable, adequate or required unless a source states a requirement, and then attribute it.
- A passage that ranks "acceptable" as a tier, or presents best practice, the minimum or a convergent value as what a design must/should/may do rather than as a figure the research shows, conflicts.
- [unratified reading] "acceptable" is not a quantity the project holds; the prose register's Acceptable rung has no place; Ideal and Minimum rungs stand as best and floor.
- [unratified reading] the minimum (floor) is a stated figure carrying no judgment; ideals are data points.
- The tension with the stage word "determination" is resolved later the same day (L7207-L7221).

Open: none (render re-wording follows the sweep).

---

### 2026-11-14 — the project holds four data points: minimum, mode, median, maximum [L6796-L6810]
Owner words:
> "we just have minimum, mode, median, maximum"

In force:
- For a cell and its context, show four descriptive figures over the identified values — minimum, mode, median, maximum — as data with what each rests on; do not add a fifth tier or call any of them acceptable, required or recommended. A passage using one of the four words for another, or naming a fifth tier, conflicts.
- [unratified reading] floor = minimum; most common = mode (T-068's cluster step); best/ideal/most accommodating is not a fifth figure but the most accommodating end (refined by the direction entry, L6884-L6900: the maximum in accommodation order).
- [unratified reading] an interval contributes both bounds to minimum and maximum; the 5% tolerance applies to the mode only.

Open:
- [OPEN] Scope of the minimum — answered next entry (L6814-L6828).
- [OPEN] Scope of the maximum, mode, median: OD-63 (L7367-L7389).
- [OPEN] Whether the median is shown wherever the mode is; how a one-value cell is shown (all four coincide); names of schema objects and render sentences.

---

### 2026-11-14 — the minimum is the code stratum's least accommodating value, or the identified values' where there is no code data [L6814-L6828]
Owner words:
> "minimum is code stratum unless there is no code data"

In force (as corrected by the direction entry, L6884-L6900):
- Take the minimum from the code stratum when it holds a value for the cell; otherwise from the identified values, and say so (shown as research-derived, never as a code floor).
- The sweep's `FLOOR` sense is the code stratum's minimum, not the minimum of everything found.
- [unratified reading] "code stratum" = the regulatory stratum T4–T6.
- [unratified reading] A research value below the code minimum is shown among the identified values and does not replace the minimum.
- The earlier reading that a ceiling-only code claim contributes nothing to the minimum is withdrawn (L6884-L6900): the minimum is ordered by accommodation.

Open:
- [OPEN] Scope of maximum, mode, median — left to the owner (OD-63).
- [OPEN] How a cell with code data from several jurisdictions presents the minimum (one figure or the set).
- [OPEN] Whether a research-drawn minimum is marked differently from a code-drawn one in the render.

---

### 2026-11-14 (last) — radically transparent: show every value and source, claim no authority over the design [L6832-L6846]
Owner words:
> "remember our project is radically transparent, presents all values/approaches/data for comparative purposes, provides citations for values/approaches/data, does not claim with own authority that something is the correct way to design but instead simply showcases the best/ideal value/approach/datum for the parameter in whatever context it's in"

In force:
- Show the value with its citation and context; say it is the most accommodating identified value; do not say it is correct, required or recommended on the project's own authority.
- Wording test: a passage conflicts if it claims authority for a design choice, hides a value, or presents a figure without a citation; naming the most accommodating identified value "best" with its citation is not a conflict.
- [unratified reading] restates the thinking-tool-not-authority doctrine; a cell shows every identified value with its citation; the four figures summarise that set, not replace it.
- [unratified reading] "approach" (a method, a provision such as a hearing loop) is shown and cited as figures are; no schema consequence drawn.

Open:
- Whether a code-only value may be showcased as best — answered by L6866-L6880.

---

### 2026-11-14 (last) — "we gather and show" [L6850-L6862]
Owner words:
> "we gather and show"

In force:
- Describe the project as gathering and showing; do not describe any stage as deciding how to design.
- [unratified reading] the two acts are gathering (research, evidence) and showing (render); intermediate stages organise and decide nothing about the design.
- The stages' tables and the spine are not touched; the spine changes only through the ledger. (The "determination" tension is resolved by L7207-L7221.)

Open: none.

---

### 2026-11-14 (last) — where the only values are code, the code determines the best [L6866-L6880]
Owner words:
> "if the only values are from code then code determines the ideal/best"

In force:
- For a cell whose identified values are all code values, take the most accommodating code value for the parameter's direction as the best, show its code source with it, and keep the minimum and mode as their own figures.
- A passage naming the most accommodating code value best in a code-only cell, with its source, is not a conflict; naming a code figure best because jurisdictions agree on it, or naming the floor best, remains a conflict.
- [unratified reading] agreement among codes is the mode, never the best.

Open:
- Marker/wording for a code-sourced best: addressed by L6904-L6918 and the circle table (OD-57).

---

### 2026-11-14 (last) — figures run in the parameter's accessibility direction; the minimum may be the highest number [L6884-L6900]
Owner words:
> "remember that value direction of parameter matters. the minimum in some contexts may be the highest allowable number in absolute terms"

In force:
- Order the identified values by the parameter's accessibility direction before taking any of the four figures; never take the numerically smallest value as the minimum without that order.
- [unratified reading] minimum = least accommodating value the code stratum allows (e.g. for an operating force or gradient, the highest number: "no more than 38 N"); maximum = most accommodating identified value; direction from `accessibility_direction` (`higher_is_better` or the reverse).
- [unratified reading] best = the maximum in accommodation order.
- [unratified reading] mode and median are taken over values ordered by accommodation.
- [unratified reading] a parameter with no recorded direction, or contested, gets no minimum or maximum, only the identified values, until a direction is recorded.
- A ceiling-only code claim is the minimum of a lower-is-better parameter; a floor-only claim ("at least 1200") is the minimum of a higher-is-better parameter. (Replaces the numeric reading in L6814-L6828.)

Open:
- [OPEN] How a parameter whose direction depends on context is shown; whether figures are labelled by accommodation or numeric names in the render.

---

### 2026-11-14 (last) — the marker, not the word, says how a best value is derived [L6904-L6918]
Owner words:
> "that's why we have the circles: we can say something is best practice but the empty circle makes it clear that it's not academically or clinically derived"

In force:
- Let the marker carry provenance; do not drop the marker; do not use ● for a value resting only on code.
- A passage naming the most accommodating code value best practice with the ○ marker (or equivalent statement of its code source) is not a conflict on that ground; with no marker or source, or at ● strength, it is.
- [unratified reading] the empty circle (○) means "not academically or clinically derived"; a ○ best practice is not equal to a ● one.
- (Circle meanings were then rebuilt by tier, L6940-L7203, and applied by OD-57, L7297-L7344.)

Open:
- The ○ vs ◐ question for a code-only best is settled by the circle table (○ for T5/T6; ◐ for T4: L7191-L7203).
- [OPEN] Marker rule for a best resting on research that is itself thin — addressed by the triangle entries (L7067-L7169).

---

### 2026-11-14 (last) — "grey, thin or unverified" may not belong in the empty circle's meaning [L6922-L6936]
Owner words:
> "grey thin or unverified maybe shouldn't be included"

In force:
- Superseded in this slice: the admission reading is answered by "let's return to keeping them" (L7001-L7017); the ○ gloss is replaced by the circle table and ⚠ (OD-57 "yes", L7297-L7344). Nothing independently in force.

Open: none here.

---

### 2026-11-14 (last) — owner proposal: circles by tier [L6940-L6965]
Owner words:
> "i think empty for code, half for tier 3/4 as 4 is above jurisdiction code, full for tier 1/2?"

In force (completed by L6969-L6997, applied by OD-57 "yes", L7297-L7344):
- The proposal's table as against the present `band()` (derive: `sed -n 100,115p schemas/tier_derivation.py`): T1, T2 ● (no change); T3 clinical ● → ◐ (lowered); T3 grey ○ → ◐ (raised); T4 ◐ (no change); T6 (code) ○ (no change). [CHECK: T3 grey's ◐ meets the triangle rule, OD-64 open.]
- [unratified reading] "code" = T6; "4 is above jurisdiction code" = T4 international standards sit above T6 national/sub-national codes.
- The hold ("keep `band()` as it is until the owner rules") ended with OD-57 "yes".

Open: none here (see OD-64).

---

### 2026-11-14 (last) — tiers 5 and 6 take the empty circle [L6969-L6981]
Owner words:
> "empty for 5/6"

In force:
- With the proposal: T1, T2 ●; T3, T4 ◐; T5, T6 ○. T5 (national beyond-code frameworks, e.g. BS 8300, DIN 18040) moves ◐ → ○.
- [unratified reading] The "code stratum" used for the minimum stays T4–T6 (T4 ◐, T5/T6 ○); the circles change marking, not where values come from.

Open: none here.

---

### 2026-11-14 (last) — Co-1 and Co-2 take the full circle [L6985-L6997]
Owner words:
> "Co-1 stays full, Co-2 full too"

In force:
- Full table: ● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6. (Applied by OD-57 "yes".)

Open:
- [OPEN] Where an unretrievable (`UNVERIFIED`) source sits — answered by the triangle (L7049-L7063).

---

### 2026-11-14 (last) — grey, thin and unverified sources are kept [L7001-L7017]
Owner words:
> "what are grey or thin or unverified sources? let's return to keeping them but they get a triangle warning"

In force (the beside-the-circle reading withdrawn by L7049-L7063):
- Admit grey, thin and unretrievable sources; do not exclude them.
- From the record (not owner words): *grey* = T3 grey, `evidence_type` `grey`; *unverified* = could not be retrieved, `verification_status` `UNVERIFIED` (2026-10-21 ruling: cannot be claimed as primary evidence or at a top tier); *thin* = not a source property; defined later (L7083-L7169). Derive live counts: `select verification_status, count(*) from evidence_sources group by 1`, and the same on `evidence_type`.
- [unratified reading] The triangle is derived, never stored beside its cause (rules 5, 8): grey from `evidence_type`, unverified from `verification_status`, thin from its rule.
- The meaning "grey, thin or unverified" for ○ ends.

Open:
- [OPEN] Whether an unverified source's circle is capped (moot under ⚠ replacing the circle) [CHECK]; where the warning is shown (source, figure, cell).

---

### 2026-11-14 (last) — the warning glyph ⚠️ [L7021-L7031]
Owner words:
> "⚠️"

In force:
- The triangle warning is named by a single warning glyph; no other glyph is added for it. The emoji form typed here is replaced by the plain Unicode form (next entry).

Open: none.

---

### 2026-11-14 (last) — the warning glyph is the plain Unicode character, not the emoji [L7035-L7045]
Owner words:
> "except use the Unicode one"

In force:
- Write U+26A0 WARNING SIGN with no U+FE0F after it (⚠, text presentation, same kind as ● ◐ ○); if a renderer draws it as an emoji, say so and do not switch glyph.

Open: none.

---

### 2026-11-14 (last) — the warning triangle replaces the circle for a value from a grey or unverified source [L7049-L7063]
Owner words:
> "no, triangle instead if the value is coming from grey or unverified"

In force:
- A figure whose governing source is grey or unverified carries ⚠ and no circle; do not write both. Marker states are ●, ◐, ○, ⚠.
- Such sources are kept; the glyph is U+26A0.
- [unratified reading] "the value is coming from" = the figure's governing source (the source its extraction rests on).
- (Thin added as a cause by L7067-L7079.)

Open:
- [OPEN] How a cell resting on grey/unverified plus other sources is marked (triangle, the others' circle, or floor of the two). [CHECK: OD-59 (own source's grade, ⚠ only where the showcased value's own basis is grey/unverified/thin) bears on this, L7297-L7344.]
- [OPEN] OD-64: T3 grey ◐ vs ⚠ (L7367-L7389).

---

### 2026-11-14 (last) — thin also takes the triangle [L7067-L7079]
Owner words:
> "thin too"

In force:
- ⚠ in place of the circle for a grey, thin or unverified basis; do not write both.
- [unratified reading] thin is a property of the value/cell basis (the doctrine's `[THIN BASE]`), not of a source, so the triangle for thin attaches to the value.

Open: definition of thin — next entries.

---

### 2026-11-14 (last) — thin means the evidence does not directly concern the people served and is conjecture [L7083-L7097]
Owner words:
> "I think thin is when the evidence doesn't directly concern someone but is conjecture"

In force (owner's working view, "I think"):
- Derive thin from the population match and the proxy-inference record; do not count roots to decide it; do not store it beside them.
- [unratified reading] thin = what supports the value was not gathered about the people or situation it is shown for (proxy population, extrapolation, inference from another group) and the step across is conjecture.
- [unratified reading] thin is per value, derived from the study-vs-served population match (R13; `db.py add-population-match`, PROXY grades) and `specifications.rests_on_proxy_inference`; no new column.
- [unratified reading] a direct study of the people concerned is not thin however few the studies; a count of independent roots is not the test.

Open:
- [OPEN] Whether any PROXY grade makes a value thin or only some grades.
- [OPEN] How a cell resting on a direct value and a proxy value is marked.

---

### 2026-11-14 (last) — a clinician's vetted professional judgment is not thin [L7101-L7115]
Owner words:
> "this is not thin. a clinician has rendered a professional judgment that has been vetted by colleagues based upon available information"

In force:
- Do not mark a value thin because its basis is a vetted professional judgment; ask of an inference whether it was rendered and vetted as a judgment or is a bare transfer or extrapolation.
- [unratified reading] conjecture = an inference not rendered or vetted as a professional judgment; the vetting record (professional-body guideline, peer-reviewed clinical argument, or similar) is what it is derived from; sits where Co-2 and clinical peer-reviewed argument already sit (no new category).

Open:
- [OPEN] How the vetting is recorded or derived.
- [OPEN] A single clinician's unvetted opinion (not covered).

---

### 2026-11-14 (last) — the project's own inferences are conjecture and carry the triangle [L7119-L7133]
Owner words:
> "when we do cross referential analyses in synthesis and pair testing etc, we can make conjectures based on evidence about what makes sense but we aren't clinicians so it is flagged as thin"

In force:
- A figure or conclusion the project reaches by its own inference (cross-referential analysis, pair testing, a synthesis step beyond what any one source states) is thin and takes ⚠. Show the inference with the evidence it rests on and mark it ⚠; never present a project inference as a source's finding or a professional judgment.
- Thin = an indirect basis (a proxy), or conjecture with no vetted professional judgment behind it, including the project's own inferences.
- [unratified reading] a derivation a source itself publishes takes that source's marker (confirmed by L7137-L7151 for clinicians/academics).
- [unratified reading] derived from existing records (`specifications.derivation_paths`, `derivation_rationale`, `rests_on_proxy_inference`, cross-parameter connection tables); no new column.

Open:
- [OPEN] Which records mark a value as the project's own inference in each stage.

---

### 2026-11-14 (last) — a derivation by a clinician or an academic is not thin [L7137-L7151]
Owner words:
> "derivation by a clinician or academic counts"

In force:
- Do not mark a value thin because it rests on a clinician's or an academic's derivation; do mark the project's own. The test is who made the derivation.
- [unratified reading] "not thin" removes only the thin cause; a derivation in a grey or unverified source still takes ⚠ for that cause; the source's tier and marker still apply.

Open:
- [OPEN] How the author's standing (clinician or academic) is recorded or derived; whether an academic's derivation needs vetting (peer-reviewed venue the nearest record).

---

### 2026-11-14 (last) — a value mixing a source's finding with a project inference is a new proposed value and takes the triangle [L7155-L7169]
Owner words:
> "because if it mixes then it's a new value proposed for something so it's conjecture because we don't have authority"

In force:
- Show the findings with their circles; mark the combined value ⚠; never give a mixed value the circle of its best source.
- [unratified reading] the source's own finding, shown by itself, keeps its circle and citation; only the mixed value takes ⚠.

Open:
- [OPEN] How the engine tells a value mixes a finding with an inference (which stage writes the flag, which records show it).

---

### 2026-11-14 (last) — the most accommodating value stands unless research shows it leads to worse results [L7173-L7187]
Owner words:
> "does the research prove that the more accommodating value leads to worse results? if so, research wins. if no, code wins"

In force (standard of proof supplied by OD-58, L7297-L7344):
- Take the most accommodating value as the best; replace it only with a recorded finding of worse results for the same lens and context; show both with their citations.
- Neither tier nor stratum decides which value is best (bears on OR-4 and OR-6c); the one exception is evidence of worse results. The tier still sets the marker.
- [unratified reading] the test is general (not only code vs research).
- [unratified reading] "worse results" = harm, failure or inadequacy for the people the cell concerns (R7), recorded as `harm_finding` or an `insufficient` relation between extractions (named from memory; not re-read).

Open:
- Edits to OR-4, OR-6c and the engine follow the adjudication through this ledger and a tooling PR. [CHECK]

---

### 2026-11-14 (last) — a cell resting on tier 4 only takes the half circle [L7191-L7203]
Owner words:
> "T4 only half circle"

In force:
- A T4-only basis takes ◐; a T5- or T6-only basis takes ○ (applies now the table is applied by OD-57).
- The mixed-tier reading here (floor of the mean of governing bands) is superseded by OD-59 "yes" (L7297-L7344): the showcased value carries its own source's grade.

Open: none.

---

### 2026-11-14 (last) — what "determination" means [L7207-L7221]
Owner words:
> "determination means to determine the ideal within the context of all evidence factors and consequently what to choose and how to grade quality of evidence for it"

In force:
- Describe a determination as identifying the ideal for a cell and its context and grading the evidence for it; never as the project deciding how to design. A passage saying a design must or should is still a verdict and conflicts.
- The phrase "best-practice determination" and the act do not conflict with "showing data, not determining". (The noun for the specification stage's output is "specification": L7225-L7239.)
- [unratified reading] "what to choose" is which identified value is shown as the ideal, not a design choice.
- [unratified reading] evidence factors are those the pipeline records (tier, directness, independence, direction, lens and context, harm findings).

Open:
- [OPEN] The list of evidence factors.

---

### 2026-11-14 (last) — a stage's tools carry the stage's own name [L7225-L7239]
Owner words:
> "the pipeline stage tools should match the actual name of the stage"

In force:
- Name a stage's tools and output with the stage's own id (research, evidence, judgment, synthesis, specification, render; base for the vocabulary layer); do not coin a second word for the stage's product; the specification stage's output is a "specification".
- Do not rename existing objects until a tooling task is opened for it (rename = migration with caller sweep, rule 4; ships apart from research, rule 10).
- [unratified reading] first mismatches: `determination_gates`, `v_open_determination_gates`, `v_determination_provenance`, `determinations_resting_on`; full sweep not done.
- Derive any object's stage from `governance/stage-map.yaml` and `pipeline-contract.yaml`, not from its name.
- Resolved by default (L7261-L7293, [unratified reading]): no aliases after a rename; the verb for the act is "states the ideal and grades its evidence"; the stage stays "specification".

Open:
- [OPEN] The list of objects to rename and the sequence.

---

### 2026-11-14 (last) — fold the term-resolution plan into the remediation plan; the newer plan wins in conflicts [L7243-L7257]
Owner words:
> "and then we need to fold plan into remediation plan and ensure they are commensurate with this newest plan having priority in conflicts"

In force:
- Where a remediation-plan statement conflicts with the unified term-resolution plan (`workplan/2026-11-12-bidirectional-pipeline/TERM-RESOLUTION-PLAN.md`), follow the unified plan and name the supersession in the task file; where either conflicts with a ledger ruling, follow the ledger.
- [unratified reading] "commensurate" = no task, dependency, decision or open item contradicts the new plan, and its tasks appear in the remediation plan with numbers, dependencies and gates.

Open:
- [OPEN] The unified plan's content (not yet read by the owner at recording) and its held questions.

---

### 2026-11-14 — OD-57 to OD-62 registration (term-resolution plan's questions) [L7261-L7293]
Recorder/delegate entry — not owner words. Owner words cited: "best practice IS the same as ideal IS the same as most accommodating"; "whatever doesn't matter".

In force:
- OD-57 to OD-61 answered by the owner in the next entries (L7297-L7363).
- OD-62 (optional: rename "best practice" to "ideal"): REFERRED BACK TO THE OWNER; **if unanswered, the default stands: no rename.** Holds no task. Not to be resolved under delegation.
- Resolved by default ([unratified reading], plan's readings): no aliases after a rename; verb "states the ideal and grades its evidence"; stage stays "specification".

Open:
- [OPEN] OD-62 (default: no rename).

---

### 2026-11-14 — fourteenth set: OD-57 to OD-61 [L7297-L7344]
Owner words:
> "od57 yes"
>
> "od58 research publication or clinical guidelines state that a person with disability struggles more or has more difficulties or some kind of negative statement with a parameter being at a certain value compared to the one it proposes"
>
> "od59 yes"
>
> "od60 prose register needs to be rewritten according to doctrine mission etc it is stale"
>
> "od60 yes"
>
> "od61 ignore. we just needed to clean up all definitions"

In force:
- OD-57 (ANSWERED BY THE OWNER): "yes". [unratified reading] Apply the circle table now: ● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6; ⚠ in place of the circle for a grey, unverified or thin basis — including T3 clinical ● → ◐, T3 grey ○ → ◐, T5 ◐ → ○, and replacing the ○ gloss in `CLAUDE.md` §6. T-117 may apply it. Ends every 2026-11-14 hold on the table. [CHECK: CLAUDE.md §6 as loaded still glosses ○ "grey, thin or unverified"; OD-64 open on T3 grey.]
- OD-58 (ANSWERED BY THE OWNER): "a research publication or a clinical guideline states that a person with a disability struggles more, has more difficulty, or makes some negative statement about the parameter being at a certain value compared with the value that source proposes". T-059 builds selection on this: such a source statement about the more accommodating value makes that research value win; nothing else does. [unratified reading] a source statement suffices (no measured outcome required); never the project's own inference; Co-1 statements read as counting (flagged).
- OD-59 (ANSWERED BY THE OWNER): "yes". [unratified reading] where a cell's sources differ, the showcased value carries the grade of its own source, with ⚠ only when that value's own basis is grey, unverified or thin.
- OD-60 (ANSWERED BY THE OWNER): "rewrite the prose register according to the doctrine and the mission; yes to the recommended shape". T-035 rewrites the prose register from doctrine and mission, not from the stale text. [unratified reading] "to be + [value]" does not survive as it stands; shape = subjunctive kept for process prose, values stated as attributed data.
- OD-61: superseded by the correction below (L7348-L7363).
- OD-62 not answered; default no rename.

Open:
- [OPEN] Whether Co-1 statements count under OD-58 beyond the reading.
- [OPEN] How a statement of difficulty is recorded (harm finding / insufficient relation shape, or a typed observation): for the task to design.

---

### 2026-11-14 (fourteenth set, later) — OD-61 correction: add `references/bpc/` to `.ignore` [L7348-L7363]
Owner words:
> "od61 incorrect. ignore the references/bpc folder as suggested"

In force:
- OD-61 (ANSWERED BY THE OWNER): "yes, add `references/bpc/` to `.ignore`". The last OD-61 line wins.
- T-121 is open: it adds `references/bpc/` to `.ignore` and says so in `CLAUDE.md` §7.
- "we just needed to clean up all definitions" is the owner's remark that the definitions were the main point, not a reason.

Open:
- [OPEN] Whether other frozen corpora join `.ignore` (not asked); form of the `.ignore` line and §7 trap line (T-121 designs).

---

### 2026-11-14 — OD-63 to OD-66 registration (questions the adversarial pass found left to the owner) [L7367-L7389]
Recorder/delegate entry — not owner words. Owner words cited: "minimum is code stratum unless there is no code data"; "triangle instead if the value is coming from grey or unverified"; "a figure offered without either is incomplete, not wrong" (recorder's ACTION text); "if no, code wins"; "presents all values … for comparative purposes".

In force:
- OD-63 to OD-66 are the owner's, CLOSED by the gate; ask each in plain form (`OWNER-SHEET-PLAIN.md` questions 14–17; `DECISION-CLOSURE.md` §4 prompts 25–28); record with `ANSWERED BY THE OWNER`; do not resolve under delegation.
- T-124 held by OD-63; T-117 held by OD-64; T-059 held by OD-65. T-068 builds OD-66's working readings, reversible, not held, and lists the live cells each changes.
- `DECISION-CLOSURE.md` prompt 5's statement that "values within 5% count as the same" as settled is corrected there.

Open:
- [OPEN] OD-63: over which values are the maximum, mode and median taken? (Recommendation, not a decision: all identified values for the cell in context, every stratum, each cited, in accommodation order.)
- [OPEN] OD-64: a value from a T3 grey source: ◐ (circle table) or ⚠ (triangle correction)? (Recommendation: ⚠.) T-117's test asserts ⚠ for T3 grey.
- [OPEN] OD-65: may a code value with no lens of its own, beside research matching the cell's lens, be selected as the best? (Recommendation: shown always; selected only where no lens-matched value exists.) Today code values carry identity `ALL`, which OD-31 removes from the identity lens; OD-47 open.
- [OPEN] OD-66: (a) 5% relative to larger or smaller; (b) one tolerance for every quantity kind; (c) group by "the same" or "consistent"; (d) two clusters on differing floors that can all be met: `divergent` or OR-6b's spread in the note. (Recommendations: (a) larger; (b) one until a live measurement misgroups; (c) the same, consistency reported beside; (d) OR-6b, with the cue written.)

---

Slice stats: entries read 58; entries reduced to nothing in force 2 (OD-44 referral, L6489, answered in slice; ○-gloss proposal, L6922, overtaken in slice — owner words kept for both; the OD-43 delegated resolution is reduced to its surviving conditions and the ⚠️ emoji entry to its one-glyph rule, neither counted as nothing); entries tagged [STATUS UNCERTAIN] 0 (open referrals OD-46, -47, -48, -51, -52, -54, -62 to -66 are tagged [OPEN]; their answers may lie after L7392); lines read 6164-7392.
