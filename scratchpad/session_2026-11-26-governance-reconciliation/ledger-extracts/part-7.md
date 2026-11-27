# Part 7 — current-state extract of references/project-standards.md, L7393-L8625

Conventions: "Owner words" are verbatim. Every reading of the recorder or a delegate is flagged [unratified reading]. Where a later entry in this slice changes an earlier one, the earlier entry shows the resulting state and names the later date.

---

### 2026-11-14 — OD-63 to OD-66: figures, grey marker, code-value lens, convergence tolerance [L7393-L7435]
Owner words:
> "1. good point. all values when synthesizing and making determinations, but on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies that we surveyed for comparison purposes"
> "2 triangle for all"
> "3 all code values will have a lens even if it's not explicitly stated. use contextual judgment"
> "4 okay. well, let's drop it down to 2% and apply everywhere"
> "2% is a tolerance. it applies to whatever is converging. I don't have to specify a minimum or maximum"
> "if values are drifting apart, then they aren't converging, and therefore they aren't being used to determine a commonality? what do you think the point of collecting data is?"

In force:
- OD-63 (ANSWERED BY THE OWNER): when synthesising and determining, the maximum, mode and median are taken over every identified value for the cell and its context; the render page shows only the minimum, mode, median and maximum, as a colour code on the surveyed jurisdictional code bodies, for comparison. [unratified reading of the exact scope]
- OD-64 (ANSWERED BY THE OWNER): a value from any grey basis takes the triangle, not the circle, with no T3-grey exception; the unverified and thin bases take it too. [unratified reading of "for all"]
- OD-65 (ANSWERED BY THE OWNER): every code value has a lens even where the code states none, assigned by contextual judgment; test T059-H4 (such a value "not selected, shown") is moot. Where and when the lens is assigned: see the 2026-11-14 entries below (judgment stage, at the recording call).
- OD-66 (a)(b): tolerance is 2%, one tolerance applied everywhere to every quantity kind; a band around whatever value is being converged on, not a bound against a minimum or maximum; values drifting apart are not converging and are not grouped; no chaining of near neighbours. [unratified reading of "band" and "no chaining"]
- OD-66 (c)(d): closed by default by the 2026-11-14 sixteenth-set instruction (next entry); OD-66 status there is ANSWERED BY THE OWNER.
- ACTION: T-068 uses 2% in one constant, around the converging value, no chaining (the 5% is withdrawn); T-117 shows the triangle for every grey basis and no circle; T-059 treats every code value as carrying a lens; T-124 and T-037 follow OD-63.
Open:
- How the render colour code is read by a reader whose access need concerns colour (T-037; see next entry: non-colour carrier required).
- How a code body with several values is shown.

### 2026-11-14 — sixteenth set: convergence and colour are not owner decisions; lens assignment by context [L7439-L7458]
Owner words:
> "just ignore the 2% and convergence because it doesn't matter enough. you can just choose colour placeholders. these aren't real decisions that you're asking of me aside from task assigning lenses to code values by context"
> "that should be done in evidence stage"

In force:
- OD-66 STATUS: ANSWERED BY THE OWNER. (c) grouping by "the same", with consistency reported beside it; (d) the registered recommendation; the 2% and no chaining are kept; no further question to the owner on tolerance or colour. [unratified reading: "ignore the 2%" does not withdraw the 2%]
- Render colours in T-037 are placeholders, each figure with a non-colour carrier; the final palette is a render design choice.
- A task assigns a lens to each code value by context (building type, user group or access need the clause serves, jurisdiction, applicability), with its warrant recorded, before T-059 and T-110.
- "evidence stage" is read, per the later 2026-11-14 owner answer "yes lens in judgment", as timing only (assign at recording); the lens stays in the judgment stage and the 2026-08-27 ruling (crossing is judgment's output) is not superseded.
Open:
- Task design: where the context warrant is recorded (the lens link's `basis`/`basis_text` do not accept a context warrant today; `scripts/db.py` `_require_lens_warrant`).
- How the new task and T-018's link table meet.
- OD-47 (lens of a clause naming no one) — answered 2026-11-19 (see ratification entry below).

### 2026-11-14 — lens of a code value is assigned when its row is recorded [L7462-L7474]
Owner words:
> "at the moment of recording the row is when you will have best idea of context"

In force:
- The session recording a code extraction (`add-extraction`) assigns the lens and records its warrant in the same step; not a later pass over stored rows.
- [unratified reading] A code row recorded without a lens is refused or flagged by the writer.
Open:
- Writer design; how already-stored code rows get lenses (a one-time data migration, separate from the writer, rule 10).

### 2026-11-14 — default contextual lens: mounting height [L7478-L7490]
Owner words:
> "typically anything to do concerning mounting height will concern wheelchair users"

In force:
- A code value concerning a mounting height (control, counter, mirror, fixture) takes the wheelchair-user lens by default, warrant recorded (e.g. "mounting height; typically concerns wheelchair users"); overridden where the clause names another group.
- [unratified reading] It is guidance for the recording session's judgment (writer prompt or skill guidance), not a lookup table in code (rule 8).
Open:
- Which lens columns carry it (identity, ICF reach code, access need): the task derives them from live registries. Other typical mappings not given.

### 2026-11-14 — clearance height takes the same default [L7494-L7504]
Owner words:
> "same with clearance height"

In force:
- As for mounting height: default wheelchair-user lens with warrant; override where the clause names another group.
- [unratified reading] "clearance height" = a clearance a seated user needs; an overhead/protruding-object clearance whose clause names people who are blind or have low vision takes that group's lens.
Open: none.

### 2026-11-14 — clearance of any dimension takes the default [L7508-L7518]
Owner words:
> "or clearance"

In force:
- The default (wheelchair-user lens, warrant recorded, override where the clause names another group) applies to any clearance, any dimension (height, width, depth, clear floor or turning space). [unratified reading of reach]
- [unratified reading] Override stays for overhead/protruding-object clearance tied to blind or low-vision users, or a clearance tied to another group.
Open: none.

### 2026-11-14 — the lens stays in the judgment stage [L7522-L7532]
Owner words:
> "yes lens in judgment"

In force:
- The lens tables and lens assignment are in the judgment stage (`governance/stage-map.yaml`); the lens of a code value is assigned in the recording call (`add-extraction`, a judgment-stage step). Do not move the lens tables or the assignment to the evidence stage.
- The crossing stays judgment's output (2026-08-27); only its timing for code values is "at recording". [unratified reading]
Open: none.

### 2026-11-14 — populations still coded through ICF and access-need lenses [L7536-L7548]
Owner words:
> "but ICF and access needs are supposed to be mapped to populations too so populations still get coded as a result"

In force (resulting state per the 2026-11-15 recorder correction, next entry):
- The recording session judges and writes the identity link of a code value (basis `context`, with warrant) in the same call as the ICF and access-need links; the maps (`identity_icf_map`, and the b/d rows of `access_need_icf`) are the writer's source of proposals, shown with mapping confidence and provenance, never a lookup consulted at read time. [unratified reading — recorder's]
- An identity the clause itself names is written as a link.
Open:
- Whether a live access-need-to-identity mapping exists under another name, or the needs lens reaches populations only via ICF: for T-126 to derive and report. [CHECK]
- Coverage of `identity_icf_map` for the ICF codes the defaults use (derive: `select count(*) from identity_icf_map`).

### 2026-11-15 — recorder correction: code-value lens judged and written at recording; maps propose; OD-67 registered [L7552-L7568]
Recorder/delegate entry — not owner words (it quotes the owner's 2026-11-14 words above).
In force:
- The lens of a code value (identity, ICF, access need) is judged and written at recording; the maps propose. [unratified reading — recorder's]
- OD-31's option text ("under a general disability heading, no identity, only its ICF and access-need lenses") no longer governs a code value whose context the recording session judges; it still holds where the lens comes from a heading (the `heading` basis). [unratified reading]
- D-0184 and OR-1 stand: a figure reaches a determination only through the lens tags written on it; the engine is not edited.
- OD-67 (may the batch's full list of new population-to-ICF rows be confirmed in one answer): resulting state per later entries in this slice — ratified 2026-11-19 ("yes, one answer on the full list, VES withheld", ANSWERED BY THE OWNER); 2026-11-25 notes the confirmation of the list itself is still owed, and OD-87 (2026-11-25) makes OD-67 moot while T-128 is withdrawn; if T-128 is reinstated, its list is owed again.
Open: confirmation of OD-67's list (moot while T-128 withdrawn).

### 2026-11-15 — stack remediation tasks into a single pull request [L7573-L7587]
Owner words:
> "going forward, we will stack branches into single PR instead of one item per PR"

In force:
- Remediation-plan tasks are carried as separate commits on one branch in one pull request; a task does not wait for the previous task's pull request to merge. Dependencies are unchanged (an earlier commit on the same branch).
- [unratified reading] Each task keeps its own commits, caller sweep, before/after check run, gate, adversarial pass and entry in the PR body; only the unit of merge changes.
- "One task, one pull request", "One pull request merges at a time" and "Do not start batch n until every READY task of batch n-1 is merged" no longer govern the unit of merge.
- Rule 10 is not relaxed: a stacked PR carries tooling tasks only; a research task goes in its own PR. (But see 2026-11-20 fourth: one large PR for that plan.)
- The generated `REMEDIATION-PLAN.md` is not hand-edited; its "merged" test counts a stacked task merged only when the PR merges.
Open: how large a stacked PR may grow before the owner wants it split.

### 2026-11-15 — end-of-batch forward and backward sweep [L7592-L7604]
Owner words:
> "for unrepaired items: please sweep your changes at end of each batch both forward and backward to assess compatibility with existing work and proposed work, and then rectify accoridngly. we do not want to leave hanging unfixed work"

In force:
- After the last task of a remediation-plan batch: (1) list every reported-and-not-repaired item; (2) read every later task file naming anything the batch changed and correct it; (3) re-run checks of every earlier task of the stack on the final tree and re-grep callers of everything changed; (4) regenerate derived files; (5) commit, push, and say in the PR what was repaired and what is now the owner's question.
- Do not report an item "not repaired" without repairing it or naming the owner question and the task files amended for it.
- [unratified reading] "Unrepaired items" = adversarial findings reported unrepaired plus every limit a task report states; "forward" = later task files; "backward" = existing code, tests, skills, governance, derived files and earlier tasks in the stack; "rectify" = repair in the batch PR, or put an owner-held decision to the owner and amend the affected task files.
Open: none.

### 2026-11-15 — back-pointer: the nine-languages rule (OD-13) [L7606-L7615]
Recorder/delegate entry — not owner words (records the owner's OD-13 answer of 2026-11-12, outside this slice).
In force:
- SUPERSEDES: governance/jurisdiction-philosophy.md :: "A BPC entry is PROVISIONAL until the Co-1 pass covers ≥9 languages." BY: references/project-standards.md :: "is superseded by the language–jurisdiction pair rulings"
- Treat that sentence and the March 2026 rules (one population per slug; language and jurisdiction as distinct axes; all 14 languages on every run) as superseded; coverage is judged per parameter and bucket member (a jurisdiction with its associated language).
Open: none.

### 2026-11-15 — three March 2026 rules overtaken (T-001 record) [L7617-L7629]
Recorder/delegate entry — not owner words (records rulings of 2026-08-24, 2026-10-29 and 2026-11-12, outside this slice).
In force:
- "One population per slug" is superseded by the 2026-08-24 ruling: every research slug is crossed with a population code, access need or ICF code; a slug names a topic, not a population.
- "Language and jurisdiction as independent axes" is superseded by OR-8 (2026-10-29 second): exhaustion is judged per parameter and per bucket member (a jurisdiction with its associated language).
- "All languages on every run" is superseded by the same OR-8 answer, with the bucket table's scope, and by the 2026-11-12 OD-13 answer.
- The 2026-03-19 provisional-until-covered clause is the clause OD-13 supersedes.
- Do not add a `SUPERSEDES` pair for a ledger target; a restatement outside the ledger is marked where it stands.
Open: none.

### 2026-10-12 — the owner's eight sentences on the idealized state graph (entered 2026-11-15) [L7631-L7671]
Owner words (verbatim from transcript):
> O1: "use Opus to create an idealized new state graph that has as little infrastructure and code as possible that still meets all conditions required of project for a walkable pipeline all directions that can dynamically scrape mine organize and sort all relevant information from any source for any parameter regardless of search slug"
> O2: "ideal state graph just be code architecture compliant"
> O3: "wherever there is a conflict, adjudicate to ensure 100% accuracy, code compliance and logic for ensuring walkability in pipeline as well as dynamic information collection"
> O4: "ensure that you strive to minimize amount of code so that it is as distilled and clean as possible as well as deduplicating and reconciling all conflicts"
> O5: "centralized where possible and rely on pointers and injectable code"
> O6: "the less hard coded, the better"
> O7: "yeah, and we need to ensure handshakes both top-down and bottom-up, and we need to ensure walkability across all tables with references and ids"
> O8: "handshake ALL directions"

In force:
- Cite this entry for the eight sentences, not the relay (`workplan/pipeline-state-graph/IDEAL-GRAPH.md` line 11); where they differ, this entry's quoted text governs.
- Cite only the quoted sentences, not the entry's summarising paragraph "What they record" (per the 2026-11-15 corrections, next entry). Only O1 and O2 name the state graph; O3 concerns adjudicating conflicts; O4 to O8 name no object.
- Read no further meaning into a sentence than it states; the relay's reading of O2 as "must" is the relay's.
Open: none.

### 2026-10-12 — a ninth sentence, and corrections to the entry above (entered 2026-11-15) [L7673-L7685]
Owner words:
> "upon completion, perform a comparative analysis between workplan v2 and ideal state graph"

In force:
- The ninth sentence (queued 48 seconds before O3) is the owner's and is cited with O1 to O8.
- Cite O1 to O8 and the ninth sentence, nothing the "What they record" paragraph adds; read no sentence as naming an object it does not name.
Open: none.

### 2026-11-16 — the medical taxonomy, maps and codes are deleted [L7688-L7711]
Owner words:
> "delete medical taxonomy , medical maps and medical codes btw"
> "perform carefully thoroughly stacking all items into one batch for pr then running close sequence on that" (process instruction)

In force:
- The medical lens is deleted: `base_taxonomy_medical`, `identity_medical_map`, `icf_medical_map`, the `medical_code` column of every table that carried one, the `MD-` vocabulary, `db.py add-medical`/`insert_medical`, every `--medical` flag, check `medical_lens_integrity` and the contract criteria reading it, and prose offering the lens. [unratified reading of the scope]
- Frozen records (ledger entries, `decisions/`, `sessions/`, committed migrations) are not edited; a phrase there offering the lens is history, not a gap. A restatement outside a frozen record that still names it is repaired where it stands.
- The lens set is three — identity, ICF, access need — and D-0182's "at least one" reads over those three. [unratified reading]
- `terms.domain = 'medical'` (`dbcore.NON_QUANTITY_DOMAINS`) is a kind of concept, not the lens, and stays. [unratified reading]
- Superseded as to the medical lens: the medical lens of D-0170 (identity, ICF and access-need lenses stand); DR-2026-09-11 adjudication-delegated/medical-lens-enforced and the 2026-09-11 ledger entries on filling the medical lens, ICD-11 as its source, and its demand-population (with its correction); the OD-15 answer (moot); "four lens columns" in the 2026-08-28 ruling and the "four" in D-0182 / the `population_code` retirement clause (now three); remediation tasks existing for the medical lens (T-077, T-103) and clauses naming it.
- Do not restore, fill or key a cell on the lens. The medical model as a framing to avoid (`voice-style`, `framing-checker`, the social-model posture) is doctrine and untouched.
- A diagnosis may still be recorded as the evidence states it (a term, an observed phrase, a note); nothing in the schema keys on it. ICD-11 anchoring already in the retrieval log stays as a record.
Open: none (but see next entry).

### 2026-11-16 — correction: two acceptances lose their premise (SCI edge, OI-48); medical terms [L7713-L7728]
Recorder/delegate entry — not owner words.
In force:
- Seventh-set (2026-11-12) ACTION (4) now reads "keep impairment level in ICF codes" (an ICF body-function code holds the function an injury changes, not the injury).
- OI-48 / SCI: resulting state per OD-83 (delegated resolution 2026-11-25 second, below): SCI retires into WHEEL; T-102 closes GAP-111 (the OI-77 question) citing OD-83, then retires SCI.
- Do not key a determination on a diagnosis term.
Open:
- Whether "medical codes" reaches the eight live `terms` with `domain = 'medical'` (search vocabulary; kept) is the owner's reading, not a fact. [OPEN]

### 2026-11-17 — OD-68, OD-69, OD-70: homographs, "category", who assigns the tier [L7730-L7770]
Owner words:
> "od68 different but how could this happen in first place"
> "od69 like the overall class of a parameter eg circulation for all the ones that deal with ramps and stairs and corridors and doors etc. the project is supposed to be like that"
> "od70 yes"

In force:
- OD-68 (ANSWERED BY THE OWNER): two independent names — the same written word in two languages is two names; a name is screened for a clash only within its own language (T-028's screens change reach accordingly). [unratified reading of "different"] Until T-028 changes it, `db.py _near_terms` still compares across languages. T-130 still proposes a pair where a seed or reviewed translation bridges the forms, and a judge decides; no fifth proposal reason.
- OD-69: "category" = a concept's topic area, the overall class of a parameter (e.g. circulation). Resulting state per 2026-11-18 (third) and 2026-11-19: the list is not fixed; held as rows extended by data with a warrant (RESOLVED UNDER DELEGATION, CHECK confirmed). Other readings of "category" (evidence type, claim type, quantity kind, design scale) were not meant.
- OD-70 (ANSWERED BY THE OWNER): the evidence type and scope are judged and recorded; the tier is computed (`derive_tier`, as `adjudication_integrity` holds it). [unratified reading of "yes"]
- SUPERSEDES: decisions/DR-2026-08-19-research-restart-operative-instrument.md :: "tier and evidence-type" BY: references/project-standards.md :: "OD-70: type and scope judged, tier computed" — DR-2026-08-19 §12.5 superseded as to the TIER only.
- The "do not resolve OD-69 under delegation" clause is superseded by the owner's 2026-11-19 instruction.
Open:
- How a form two concepts already hold in one language is resolved (merge or `distinct` judgment, T-129).
- Which of the domains now in use are topic areas and which are non-quantity kinds (`dbcore.NON_QUANTITY_DOMAINS`); whether existing values are renamed or merged. [CHECK — the 2026-11-19 resolution sets the form only]

### 2026-11-18 — OD-71 (the base grounds itself) and OD-72 (displayed name) [L7772-L7809]
Owner words:
> "then the base grounds itself except for when evidence that allows for new terms/aliases/parameters to be found is pointed to as justification"
> "but this justification should then be absorbed by base and grounded as if it were always there to prevent loops/recursion/sequencing conflicts"
> "likely have to do a convergence test for number of term appearances for concept or I rule"
> "ref_id as provenance? sure. but it's ONLY for provenance"

In force:
- OD-71 (ANSWERED BY THE OWNER): a base row may cite the evidence that allowed it to be found as justification, but the justification is absorbed into the base row's own columns (what was found and where: form, language, jurisdiction, URL, page, line, quoted words) so the base row reads, checks and orders without any evidence row. [unratified reading of "absorbed"]
- A base table holds no foreign key into evidence or judgment and no pointer a base row's validity waits on; sequencing runs one way (evidence may be found from the base; the base is never ordered after evidence). Reaches `term_label_picks.observation_id`, `add-term --from-observation`'s hold of a form `unrecorded`, the warrant keys of `term_relations`, `term_aliases`' source columns and any later base table carrying a warrant.
- A `ref_id` (or observation id) may be kept as plain provenance only: nothing validates against it, orders after it, joins through it to decide a state, or waits on it; a base writer neither requires it nor refuses a row lacking it.
- OD-71 residue (2026-11-19, ANSWERED BY THE OWNER): see the ratification entry below.
- OD-72: resulting state per 2026-11-19 (RESOLVED UNDER DELEGATION, CHECK confirmed) — see the ratification entry. Do not choose the displayed name by `MIN(form_id)` or by recency. OD-38's "until a named judge picks; the pick is recorded with its reason" is not withdrawn.
- The ACTION clause "do not resolve under delegation" is superseded by the owner's 2026-11-19 instruction.
Open:
- How an existing pointer is migrated.

### 2026-11-18 (second) — OD-72 refined: forms as written, counted, a preferred display term, CSA/ISO first [L7811-L7838]
Owner words:
> "for the displayed name of parameter, record it in whatever form and then have a preferred display term column maybe"
> "but we're basically just counting the number of times it appears written in a given way. I would prefer to prioritize CSA/ISO for terminology"

In force:
- Record every written form as found; do not choose a name at recording; the displayed name is a separate, derived choice.
- An appearance is an occurrence of a form written in a given way (one row of `term_aliases`); the test is a count of appearances. [unratified reading]
- A preferred-display-term cell is proposed ("maybe"). [unratified reading]
- CSA and ISO forms take priority for terminology. The combination rule: resulting state per 2026-11-19 (OD-72 RESOLVED UNDER DELEGATION): CSA or ISO wins, then the count; see the ratification entry.
Open:
- Whether the preferred-display cell lives on the concept or the parameter; whether it is derived (view) or stored (cell) and who writes it.
- Whether "CSA/ISO" means those two bodies exactly or standards bodies generally, and which of their documents are terminology sources. [CHECK]

### 2026-11-18 (third) — OD-69: the list of topic areas is not fixed [L7840-L7862]
Owner words:
> "list of topic areas is not fixed"

In force:
- The classes of a concept are an open set; no closed list confirmed once by the owner. Do not treat the 18 values in use as a closed or confirmed list (derive: `select domain, count(*) from terms group by 1`).
- T-135's design "seeded from the list the owner confirms, changed only by the owner" is not the design.
- The form: resulting state per 2026-11-19 — held as rows extended by data with a warrant (RESOLVED UNDER DELEGATION, CHECK confirmed). The ACTION "ask the owner; do not resolve under delegation" is superseded by the 2026-11-19 instruction.
Open:
- The non-quantity domains; whether an existing value is renamed or merged. [CHECK]

### 2026-11-14 (recorded 2026-11-19) — Unification: best, most common, minimum; showing and grading [L7864-L7964]
Recorder/delegate entry (executor of T-119) — it decides nothing; it gathers the owner's 2026-11-14 words, quoted below verbatim.
Owner words (2026-11-14, as quoted in the entry):
- U1 best: "my definition of best practice IS the same as ideal IS the same as most accommodating"; "The most accommodating, then, is the one that best responds to an ICF/access need/identity within whatever context, and that means it is the ideal from what we have found"; "The most accommodating value is one that has been identified in our research, which in turn means that it is based in the evidence that we have collected enough if the research source itself simply asserts the value"; exception: "does the research prove that the more accommodating value leads to worse results? if so, research wins. if no, code wins".
- U2 most common: "convergence just means values coming together"; "you can still converge across tiers like a tier 1 and a tier 6 proposing same value"; "convergence is not evidence of best practice but most common practice".
- U3 minimum: "the minimum is a factual data point"; "minimum is code stratum unless there is no code data"; "the minimum in some contexts may be the highest allowable number in absolute terms".
- U4 figures and direction: "we just have minimum, mode, median, maximum"; "remember that value direction of parameter matters".
- U5 show, do not rule: "we gather and show"; "remember that we are showing data, not determining"; "acceptable isn't relevant as that's a value judgment"; "determination means to determine the ideal within the context of all evidence factors and consequently what to choose and how to grade quality of evidence for it".
- U6 code only: "if the only values are from code then code determines the ideal/best"; "that's why we have the circles: we can say something is best practice but the empty circle makes it clear that it's not academically or clinically derived".
- U7 markers: "i think empty for code, half for tier 3/4 as 4 is above jurisdiction code, full for tier 1/2?"; "empty for 5/6"; "Co-1 stays full, Co-2 full too"; "T4 only half circle"; "no, triangle instead if the value is coming from grey or unverified"; "thin too"; "except use the Unicode one"; "I think thin is when the evidence doesn't directly concern someone but is conjecture"; "this is not thin. a clinician has rendered a professional judgment that has been vetted by colleagues based upon available information"; "derivation by a clinician or academic counts"; "because if it mixes then it's a new value proposed for something so it's conjecture because we don't have authority".
- U8 transparency: "remember our project is radically transparent, presents all values/approaches/data for comparative purposes, provides citations for values/approaches/data, does not claim with own authority that something is the correct way to design but instead simply showcases the best/ideal value/approach/datum for the parameter in whatever context it's in".
- U9 names: "the pipeline stage tools should match the actual name of the stage".

In force:
- Homes for the operative text: U1, U2 (sentence), U3, U4, U6 → `governance/evidence-architecture.md` §0; definition of convergence → `governance/evidence-methodology.md` §3.2 (T-068); U5, U8 → `governance/mission-and-epistemics.md` (commitment 2 and the posture section); U7 → `governance/tier-system.md` §5 (T-120) and `schemas/tier_derivation.py` `band()` (T-117); U9 → this ledger and `governance/stage-map.yaml`. Where a home does not yet carry the text, the quoted entries govern. [CHECK whether T-120/T-117 have written the homes]
- See also OD-57, OD-58, OD-59, OD-61 (fourteenth set) and OD-63, OD-64 (fifteenth set).
- [unratified reading] A source's tier sets the marker and the weight, not whether its value may be the best.
- [unratified reading] The best is the maximum in accommodation order, except where U1's exception replaces it.
- [unratified reading] A determination states the ideal and grades its evidence; "must"/"should" said of a design remains a verdict.
- [unratified reading] The stage stays "specification", and `v_best_practice` keeps its name (OD-62: no rename, RESOLVED UNDER DELEGATION 2026-11-19).
- Back-pointer sentence: "best, most common and minimum are read as the owner defined them on 2026-11-14". A decision-record passage carrying a marker naming this entry is read that way; the old text stays.
- (a) Machine SUPERSEDES pairs (all BY the back-pointer sentence above), targets:
  - DR-2026-05-24-best-practice-supersession-protocol: "best practice for the guidebook is determined by the evidence hierarchy"; "a best-practice claim derived from a *superseded* Tier-3 source is also in error" (as to whether it may be the best; currency untouched); "a Tier-1 candidate supersedes a Tier-3 anchor regardless of recency" (amended: governs searching, not the best value).
  - DR-2026-05-26-gap-driven-mining-protocol: "Grounds best practice in evidence hierarchy?** Yes — search matrix is tier-prioritized per gap pattern" (amended: searching stays tier-prioritised).
  - DR-2026-07-12-evidence-architecture-unification: "T4–6-only determinations are Universal-Mode regulatory determinations, never rendered as best practice in any register" (by U6).
  - DR-2026-07-12-evidence-cell-state-schema-reconciliation: "jurisdiction-specific code convergence, e.g. 1800mm" (gloss only; decision stands); "`v_best_practice` must exclude `code_floor_only = 1` rows" (by U6).
  - DR-2026-07-13-value-genealogy-and-derivation-handshake: "the computable best-practice-vs-consensus discriminator" (clause only; fields and view stand).
  - DR-2026-07-20-intra-category-cross-test: "the *method* for cross-mode best-practice adjudication is ratified (DR-2026-07-13)" (amended).
  - DR-2026-07-21-evidence-architecture-option-a-execution: "I5 applies with the register map's ○ row as ceiling"; "is a best-practice determination at the weak band (○)"; "§6 register map row 3 (weak-band best-practice phrasing at ○"; "it is a weak-band (○) best-practice claim"; "an unflagged or above-weak-band code-consensus best-practice claim *is* still in error" (amended by U2/U6/U7; the 2026-07-21 owner ruling "no, it's just weak" stands as to a code-only cell having a best at the weak marker, the value named best being the most accommodating code value, never the value codes agree on).
  - DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation: "cell becomes a `○`-strength best-practice determination" (amended by U7).
  - DR-2026-07-20-weighted-strength-anchor-model: "T1/2/3 full, T4/5 partial, T6/grey weak" (bands superseded by U7; "all evidence tiers can be used to anchor a best practice claim" stands); "T1, Co-1, T2, Co-2, **T3-clinical**" (band rows by U7); "multiple T4–T6 codes agreeing on a value is convergence of floors" (gloss by U2/U3; agreement is never relabelled best practice stands). [unratified reading — added by the T-119 repair "for the owner to confirm"]
  - DR-2026-07-21-product-posture-thinking-tool-not-authority: "the practice the evidence best supports" (by U1; "offered as a figure for thought, not imposed as a requirement" stands; its passage quoting the owner's 2026-07-21 words on adjudicating to surface the best is NOT superseded).
  - RATIFICATION-PACKAGE-2026-07-12: "the machinery refuses to call it best practice in any register" (by U6; refusing to call agreeing codes best stands, by U2); "The adjudication engine for best-practice-vs-consensus, made computable" (by U1/U2).
  - Also (from the 2026-11-19 ratification entry): DR-2026-07-21-tier-doctrine-source-class-consistency: "weak-band convergence floor".
  - Five quotes wrap across a line break; grep their first words; the audit's normalisation joins lines.
- (b) Superseded in prose only, in their sense of best practice (best as convergence, as T1/T2 only, or as the code floor), not edited: `references/bpc/` (every file; derive count with `find references/bpc -type f | wc -l`); `references/audits/bpc-audit-pass0-2026-05-10.md`, `references/audits/bpc-audit-pass2-2026-05-10.md`; `references/connections/` (every file); `references/fdr/reach-range-and-accessible-controls.md`; `references/systematic-reviews/dd1-ndv-qualitative-dd7-umbrella.md`; `references/methodology/economics-research-methodology-v1.9-archived.md`; in `workplan/`: `2026-08-11-remediation-and-pipeline-anatomy.md`, `2026-08-12-commit-91-adversarial-review.md`, `2026-08-18-research-frame-proposal.md`, `2026-08-20-provenance-walk-execution-plan.md`, `2026-10-30-ramp-spec-pages/owner-rules/code-baselines-accepted.md`, `2026-10-30-ramp-spec-pages/owner-rules/spec-page-requirements.md`, `2026-10-30-ramp-spec-pages/reports/spec-page-design-requirements-2026-10-29.md`, `2026-10-30-ramp-spec-pages/reports/stress-test-ramp-slopes-2026-10-29__report.md`, `2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2-REVIEW.md`, `best-practices-assessment-system.md`, `methodology-and-pipeline-enforcement-plan-2026-07-23.md`, `next-steps-synthesis-2026-07-14.md`, `phase-e-execution-plan-v1.md`; attestations `decisions_DR-2026-05-24-best-practice-supersession-protocol.json`, `sessions_session_2026-07-20-bathroom-typology-global-south-rederivation.json`, `sessions_session_2026-07-20-retracted-slice-rederivation-batch.json`; `governance/mission-PROVISIONAL.md`, `governance/pre-stage-a-decisions.md`. `governance/doctrine-deltas.json` is not superseded (T-120 appends a state when commitment 2 is amended).
- (c) Earlier ledger rules, superseded in prose only (find by text):
  - 'walled off from best-practice anchoring' and 'Best practice is determined by the evidence hierarchy' — as to tier deciding which value is best (U1); in the second, also a code-consensus value named best (U2, U6).
  - 'A T4–6-only basis never renders best-practice language' — that sentence (U6) and that RULE's marker bands (U7).
  - 'Best practice based on [N] jurisdictions and [tier] evidence is [value]' — as to naming a best by count of jurisdictions (U2); its point on authority stands.
  - 'Working target: 18–22°C' — as to "require", "Working target", "not acceptable" (U5); figures stand as data with sources.
  - 'MAXIMUM ACCEPTABLE gradient' — as to framing as acceptability (U5).
  - 'the guidebook uses to say *this is best practice today*' — as to tier deciding the label (U1); its point on currency stands.
  - [unratified reading] 'Population Mode = Population-Informed Inclusive Design (ranges; median as default)' — as to the median as default figure.
  - [unratified reading] 'BPC best_practice_synthesis governs as primary evidence basis' — as to a synthesis governing over identified values.
  - 'Universal design is co-extensive with code compliance' — NOT superseded.
  - OR-4 and the ACTION (3) of the same entry ("Let the most accommodating anchoring value win among differing figures that can all be met") — as to confining the choice of best to T1, Co-1, T2, Co-2; OR-6c — as to selection only. OR-6 and OR-6b keep their status words.
  - `decisions` rows D-0004, D-0042, D-0076 (in `scripts/migrations/057_baseline_2026-08-12.sql`) superseded in the same senses as their RULE lines; they stay `ACTIVE` because no writer marks them. D-0005 likewise, except its clause that a value derived solely from code consensus is in error, which is not superseded.
- Treat every [ASSUMPTION] of the entry as unratified.
Open:
- OD-62 (rename "best practice" to "ideal"): RESOLVED UNDER DELEGATION 2026-11-19, no rename (see next entry).

### 2026-11-19 — owner ratification of the third adjudication [L7967-L8035]
Owner words:
> "have Opus adjudicate all open decisions based upon long-term integrity re provenance and walkability as well as context from my prior rulings"
> "Sure, append. Ratify all."

In force:
- Scope of "all open decisions" and "Ratify all": every register entry not answered or resolved, the sweep lists' open items, and the eleven questions of PR #240; the nine items reserved to the owner become owner answers; delegated resolutions are confirmed; design questions 12 to 91 without OD numbers are ratified by reference to `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`. [unratified reading — the breadth of "all" is the first to confirm]
- The earlier "not to be resolved under delegation" clauses (ACTION (3) of 2026-11-18 OD-71; ACTION (3) of 2026-11-18 (third) OD-69; ACTION (4) of 2026-11-17 OD-68; ACTION (4) of the 2026-11-15 correction; the 2026-11-14 registration sentence on OD-62) are superseded for these items. [unratified reading]
- "provenance" and "walkability" read as defined in section 0 of the adjudication. [unratified reading]
- OD-17: the corrected contract is ratified (its condition, T-022 merged, is met) — ANSWERED BY THE OWNER. [unratified reading: the owner was not shown the contract diff]
- OD-46: admit as declared, scoped-out codes — ANSWERED BY THE OWNER.
- OD-47: the document's stated audience judged per item by context, the audience words quoted — ANSWERED BY THE OWNER.
- OD-48: whom it is for — ANSWERED BY THE OWNER.
- OD-51: yes, on retrieved proof of authorship — ANSWERED BY THE OWNER.
- OD-52: names the term; the contrast provision is separate — ANSWERED BY THE OWNER.
- OD-54: into the register, replayed through the writer — RESOLVED UNDER DELEGATION; CHECK confirmed.
- OD-62: no rename — RESOLVED UNDER DELEGATION; CHECK confirmed.
- OD-67: yes, one answer on the full list, VES withheld — ANSWERED BY THE OWNER. (Later: list confirmation still owed; moot while T-128 withdrawn, OD-87.)
- OD-69: a concept's topic area; the list is not fixed; held as rows extended by data with a warrant — RESOLVED UNDER DELEGATION; CHECK confirmed.
- OD-71: the absorbed grounding holds the locator and the words the base cell asserts were found, as far as a base refusal reads them; `direction_ref_id` and `term_aliases.observation_id` become provenance only or are dropped; an absorbed phrase with a URL and a page or clause is attested — ANSWERED BY THE OWNER.
- OD-72: an appearance is one attested occurrence; CSA or ISO wins, then the count; an exact tie shows the label and a judge is owed; a named judge's pick overrides; no form shows the label; a concept with no attested English instrument form of an in-scope jurisdiction is counted across its attested forms in every language — RESOLVED UNDER DELEGATION; CHECK confirmed.
- Licensing default (adjudication item 15): retained clause text may enter git history; showing it stays forbidden (ratified; no status line).
- OD-11 delegated resolution corrected: a cross-stage table is walkable as an intermediate and counted in no stage; "count it as a member of each stage it carries" is withdrawn; ACTION (3) "lose no path" is met.
- SUPERSEDES: decisions/DR-2026-07-21-tier-doctrine-source-class-consistency.md :: "weak-band convergence floor" BY: references/project-standards.md :: "best, most common and minimum are read as the owner defined them on 2026-11-14"
- Gate convention (2026-11-12): a status line opens a decision; RESOLVED UNDER DELEGATION opens it with its CHECK; a task needing the owner's own words opens only on ANSWERED BY THE OWNER.
- Author the adjudication's section-4 tooling tasks in its order, each its own PR; ship research separately (rule 10).
- The ratified defaults are owner rulings from 2026-11-19; a later owner statement supersedes them on contact.
Open: none stated.

### 2026-11-19 (second) — "grab bar" and "grabbar" are one parameter [L8037-L8053]
Owner words:
> "grab bar and grab bar are obviously the same parameter"

In force:
- [unratified reading] The second "grab bar" is "grabbar".
- Group a concept's forms by the ratified key (third adjudication item 11: by language and by the form after the one quote normaliser, case-folded); a form differing from another only in whitespace or case is the same form. Do not narrow the key to keep whitespace.
Open:
- Accents are not decided.

### 2026-11-19 (third) — "ramp slopes"/"ramp gradient" one concept; door-width forms one concept [L8055-L8077]
Owner words:
> "ramp slopes and ramp gradient are the same"
> "doorway width and door opening width and door clear space are the same"
> "*clear width"

In force:
- The forms name one concept each (one term, one parameter); do not mint a second term or parameter; file each form as an alias of the one concept.
- [unratified reading] "*clear width" adds "clear width" of a door only (not corridor/route clear width); "door clear space" = the door's clear opening, not the floor space beside it; "ramp slopes" is the plural of the alias "ramp slope".
- A form a source states is recorded with its locator through the alias writer; a form only the owner stated is recorded as an owner-supplied alias (`attestation` `owner_supplied`), which counts for nothing toward a displayed name until a source attests it.
- A source's figure for any of these forms is extracted against the one parameter whatever slug it came in under.
- The alias rows are research data, written in a research PR after the tooling (T-136, T-142).
Open: none.

### 2026-11-20 — issues are filed in the `gaps` table, with resolution and solution provenance [L8079-L8101]
Owner words:
> "shouldn't we just write all of this to gaps table because we already have tools pointed there"
> "file all in gap table"
> "add a resolved column and a solution provenance column or something"
> "unless we already have a table that links accordingly for the"

In force:
- File an unresolved issue as a gap through `db.py add-gap`, in a data PR following the tooling change; do not hand-keep a register file.
- Close a gap with `db.py close-gap` and its resolution pointer; a closing with no recorded resolution is a legacy row.
- [unratified reading] The resolved/provenance columns are `resolved_at`, `resolved_by_session` and a pointer to what resolved the gap, as sibling tables carry; schema merges before rows (rule 10).
- [unratified reading] A decision registered as an OD stays with its ledger status lines.
- ACTION (3) ("record a critic's findings as an adversarial pass, not as gaps") is replaced by the 2026-11-20 correction (next entry).
Open: none.

### 2026-11-20 — correction: standing critic findings are filed as gaps [L8103-L8116]
Recorder/delegate entry — not owner words (cites the owner's "file all in gap table" and, earlier, "Create a register with all issues logged that have yet to be resolved").
In force:
- File an unresolved issue (including a critic's finding that still stands, an item a task will repair but has not, a limit, an unconfirmed owner reading) as a gap row via `db.py add-gap` in a data PR; priority follows the critic's severity where given (CRITICAL and HIGH → P1, MEDIUM → P2, LOW → P3). [unratified reading of scope]
- Not filed: an item a later commit repaired, a past event that cannot be resolved, an OD (its ledger status line is its home); a repaired critic finding's record is the repair commit and the sweep list. [unratified reading]
- Use `record-adversarial-pass` only where the one-pass-per-batch rule allows it. Neither the one-pass rule nor the REPAIRED-requires-a-data-migration rule is changed.
- Close a gap with `db.py close-gap` and its resolution pointer.
Open: none.

### 2026-11-20 — translation runs before judgment; identities are the main lens; base holds translation, units and the identity–need–ICF crosswalk [L8118-L8150]
Owner words:
> "we research, we record, we verify we recorded things accurately, we evaluate things in context with other related things, we synthesize then show"
> "base is the substitute for me asking for a research topic directly"
> "i only know english, so the base has to record all the translation work for me"
> "i don't want to have to constantly map and cross-reference disability identities vs access needs vs ICF codes, so the base needs to get that ready for me too"
> "we need to actually also translate the stuff from other languages so that i can actually see it and so that it can be properly evaluated in context"
> "this is also why we need to be able to convert units etc"
> "this project will die upon itself if it doesn't treat disability identities properly. they are going to be by far the most common lens upon which people will navigate the repository"
> "yes, translation runs before judgment"

In force:
- Translation of a non-English source's title and of each figure's wording is recorded, with the original, before judgment reads it; this supersedes the `translation: default_stage: synthesis` default in `governance/pipeline-contract.yaml` (the contract to be corrected in a tooling PR).
- An English rendering is not written into `claimed_value` or `claimed_unit`.
- [unratified reading] The translation is recorded with the original beside it, who/what translated it and when, and its review state, and is what render shows.
- [unratified reading] Identity, access-need and ICF mappings are recorded as data a session judges and proposes; the owner is not asked to map by hand.
- [unratified reading] Unit conversion: a figure in one unit/notation is comparable with the same quantity in another, as data in `base_units`.
- A disability identity is the first lens of the repository: an identity with no ICF code, or with no recorded need, is a gap to close.
- The statements decide no schema, table name or task order.
Open:
- Form of the identity–need link (stored or derived) — see 2026-11-20 (second): judged triples table.

### 2026-11-20 (second) — the identity × access-need × ICF crosswalk is a table of judged triples [L8152-L8172]
Owner words:
> "you basically need to have a big 3D matrix of ICF codes * access needs * disability identities"
> "yes, correct"

In force:
- The owner confirmed this description (coordinator's wording): the cube is stored sparsely as a table of judged triples, each with a warrant, who/what judged it and when, and a cell state (stated, provisional, pending, not_applicable); a missing cell reads as not yet judged, a not_applicable row as judged and not applying; the cube is a view over the table, readable from an identity, a code or a need; a session proposes triples and the owner reviews each batch before it counts as stated. [unratified reading that "yes, correct" covers the whole description]
- [unratified reading] `MAPPING-DESIGN.md` section 2(a)'s rejection of a new identity–need table is not a reason not to build it; `access_needs.absorbs` (a delimited cell) cannot stay the only home under the one-value-per-cell ruling.
- Design the table as a tooling task and ship it before any triple is written (rule 10); name what reads it. The filling batch is research data in its own PR; the owner reviews it before rows count as stated.
- Key shape: all three keys present (2026-11-20 fifth).
Open: none further.

### 2026-11-20 (third) — the project is a database and a pipeline, kept simple; proposed CLAUDE.md rewrite [L8174-L8215]
Owner words:
> "this entire infrastructure is just trying to formalize asking a Claude session to do research on a topic"
> "i have just spent a huge amount of time trying to harness an LLM through gates/scripts/github/etc instead of just using it to translate things i can't read"
> "all i want is for the information to be properly recorded in a database"
> "that's it"
> "and then we squeeze it through a pipeline"
> "i am just saying that the heart of this project really isnt that complicated"
> "overall we need to make this project as simple as possible in infrastructure because the more exceptions we have the more complexity we guard against which is the more we spiral"

In force:
- Simplicity rule: each addition names the existing thing it replaces or deletes and what reads it; a new exception is a reason to change the rule, not to add a guard. Before adding apparatus, state what it replaces and what reads it.
- The goal sentence lives in the 2026-11-20 entry above (not repeated here).
- Proposed CLAUDE.md rewrite (coordinator's proposal, unratified): (1) Goal — goal sentence verbatim; thinking tool, not an authority; DB records research and a pipeline processes it; `base` is the owner's request layer. (2) Never get wrong — fetch before writing author/title/figure; original text, unit and clause beside every translated figure, English rendering recording who/what translated and when, never in `claimed_value`/`claimed_unit`; Co-1 co-producers are evidence and stay credited. (3) Six verbs with commands. (4) The write path in one sentence. (5) Derive, do not type, a number. (6) Pointers. Moved to a working-rules file: rules 0, 1, 4, 5, 6, 9, 10; sections 3, 7, 8. Deleted: Layer-0 preamble, rule 7 (merged into 7a), the `stage_label()` sentence, the "Proof" narratives.
- Constraints: `scripts/audit/claude_md_spine.py` pins the SPINE line (it stays in CLAUDE.md or the check moves); scripts cite CLAUDE.md rules by number, so sweep them before renumbering. Size test: `[ $(wc -w < CLAUDE.md) -le $(( $(git show origin/main:CLAUDE.md | wc -w) / 4 )) ]`.
- The owner approves the goal sentence, rule 0, rule 9, the tier and Co-1 definitions, and the fate of the layer model; a session may reorder and reword process rules, traps and command lists.
[STATUS UNCERTAIN: the entry says CLAUDE.md is not to be rewritten until the owner approves; the 2026-11-20 (fourth) entry says the big PR carries the rewrite and merging approves it; whether that PR merged is not stated in this slice.]
Open:
- Owner approval of the rewrite content. [OPEN / STATUS UNCERTAIN]

### 2026-11-20 (fourth) — one large pull request for the remediation work; the matrix ships on its own [L8217-L8236]
Owner words:
> "no, just do a big pull request so i don't have to waste time"
> "the matrix can be on its own"

In force:
- Ship the open work of the 2026-11-20 entries (translation before judgment, units, verification, the CLAUDE.md rewrite, housekeeping) as one PR, with their tooling and the research rows they need; the matrix (T-145 and its rows) ships as its own PR, tooling first. [unratified reading of scope]
- [unratified reading] For this one PR only, rule 10's research/tooling separation is suspended; it stands for every other PR.
- Inside the PR, order commits tooling first, then the rows they enable; keep each part's checks in the same PR and report any that cannot go red on the defect.
- The PR carries the CLAUDE.md rewrite for the owner's review, rule 0 and rule 9 text moved but unchanged; merging approves it.
[STATUS UNCERTAIN: one-off instruction for a single PR; whether it has shipped is not stated in this slice.]
Open: none.

### 2026-11-20 (fifth) — the matrix holds all three keys; qualitative value cell may be corrected in place (GAP-368) [L8238-L8261]
Owner words:
> "Yes @ T-145"
> "T-145: should be all three. We need to do the identity-ICF-access matrix."
> "GAP-368: Yes, you can correct in place."

In force:
- A row of the identity, access-need and ICF table holds an identity, an access need and an ICF code, each present (all three keys NOT NULL). Does not touch D-0182 (a determination's lens columns).
- [unratified reading] Only the owner's review of a batch marks a row `stated`.
- [unratified reading] T-145 Q3 (the two flat maps and `access_needs.absorbs` stay as proposals; `absorbs` retired in a later task) and Q4 (a `not_applicable` row carries the same warrant cell as a stated row) are taken at the task's recommendations.
- The eleven qualitative value cells (`source_value_extractions` ids 20, 21, 27, 31, 32, 93, 102, 104, 106, 112, 80) may be corrected in place, not retired and re-added; the original wording stays in `claim_text`, the English is in `translations`. The means: by hand in a data migration, per 2026-11-21 (next entry); no purpose-built writer.
- The triples that fill T-145 are a later research PR the owner reviews.
- The Opus adjudication of the eight decisions and its critique are not rulings.
Open: none.

### 2026-11-21 — qualitative cells may be corrected by hand, each hand fix recorded; GAP-368 needs no writer [L8263-L8282]
Owner words:
> "I think GAP-368 points towards Claude having permission to hand edit as required for specific columns"
> "We don't need a tool for many qualitative judgments/corrections because Claude IS a tool. We just need to ensure that you make transparent and record your hand fixes"

In force:
- Do not build a writer for a qualitative correction on the strength of GAP-368; correct the cell by hand in a data migration (the CLAUDE.md §4 write path is unchanged) and record the old value, new value, reason and session in the migration header and in the gap's resolution.
- [unratified reading] "specific columns" = columns holding a qualitative judgment or wording; identifiers, keys, vocabularies, counts and bibliographic fields stay behind their writers and fetch-before-write.
- Do not extend this to a column outside the owner's meaning of "qualitative"; ask.
Open:
- The list of columns covered. [OPEN]

### 2026-11-21 (second) — a need may be keyed on an umbrella identity and on its members [L8284-L8300]
Owner words:
> "3 to umbrella and to specific, yes"

In force:
- [unratified reading] "3" = GAP-379.
- A need's row may be keyed on the umbrella identity (NDV, COM, BRAIN, MH) and on each member identity at once; keep both, do not collapse.
- A-TRIGGER for COM and EPI: settled under delegation by OD-85 (2026-11-25 second; class B accepted, no row changing state).
Open:
- Whether the `e120` row is attached to LPA, TALL and BAR through A-SIZE's row (GAP-379's other part). [OPEN]

### 2026-11-21 (third) — an identity may be linked to a body-function (b) code [L8302-L8319]
Owner words:
> "1 yes b is seeing therefore ties into blind etc"

In force:
- [unratified reading] "1" = GAP-377.
- A body-function row may be proposed for an identity.
- The only body-function tie the owner's words state is b210 to the blind identity; every other identity and code needs its own recorded basis (an owner statement, a recorded map row, or a WHO payload), never an axis anchor. [unratified reading: "b is seeing" = b210; "etc" generalisation not decided]
- Per OD-80 (2026-11-25): the WHO simple tabulation grounds a code's existence, title and hierarchy only, not a relation between an identity/need and a code. Per OD-78 (2026-11-25 second): no body-function proposal path is added; a body-function code reaches an identity only from the owner's words.
Open: none further (see OD-78).

### 2026-11-21 (fourth) — A-AT is inside the built-environment scope [L8321-L8338]
Owner words:
> "4 A-AT is in scope"

In force:
- [unratified reading] "4" = GAP-380.
- A-AT is an access need inside the built-environment scope; the registry note's flag is answered; A-AT may be paired with an identity like any other need.
Open:
- Which identities A-AT serves (not stated).

### 2026-11-21 (fifth) — the project is about architectural design; building design and light [L8340-L8358]
Owner words:
> "we are concerned about building design and light."
> "our project is literally about artchitectural design techniques"

In force:
- The statements stand as owner words on scope. The question they bore on (GAP-378) is answered by the 2026-11-21 (sixth) entry; this entry's interim ACTION is overtaken.
- [unratified reading] "building design and light" = ICF e150, e155 and e240.
Open:
- Whether matrix rows 46 and 47 (EPI with e260, COM with e240), proposed for rejection, stand — awaits the owner. [OPEN; CHECK whether OD-85/OD-86 reach them]

### 2026-11-21 (sixth) — a need-side environmental row counts as an identity's ICF coverage [L8360-L8375]
Owner words:
> "Yes, they count as identity's ICF coverage."

In force:
- A need-side environmental row (an identity-need row whose ICF code is an environmental code held by the need's own `access_need_icf` rows) counts as the identity's ICF coverage; do not file or build a change that excludes it (incl. `db.py lens-crosswalk --uncovered`).
- The 2026-11-20 rule that an identity with no ICF code is a gap is met for an identity holding such a row.
- The review of each matrix row stays the owner's.
Open: none.

### 2026-11-21 — owner review: TRIPLE-64 accepted, TRIPLE-65 rejected [L8377-L8393]
Owner words:
> "Reject Row 65. Accept Row 64."

In force:
- TRIPLE-64 (BLIND, A-NOSIGHT, b210) is `stated`; TRIPLE-65 (COM, A-TIME, b164) is retired with this entry as the reference, by `db.py review-identity-need-icf`. [unratified reading of row identities and of the acceptance's basis]
- TRIPLE-65's warrant mislabelled a quotation from the need's ICF notes as registry text, and the pair is an inference no record states.
- Do not propose a replacement for TRIPLE-65 without a recorded basis for the identity's link to the need.
Open: none.

### 2026-11-22 and 2026-11-23 — ICF umbrellas and glossary; three browsing approaches; identities and needs mapped, then ICF chosen; delegation to Opus [L8395-L8434]
Owner words:
> "the ICF codes used are not what I was expecting. I had been expecting ICF codes like b210, b230, b265, b280 etc.. but then we have entire groups like b750 to b789 which are all under "Movement functions""
> "so perhaps for ICF I really want those classification umbrellas like "Movement functions" , "Pain", "Hearing and vestibular systems" etc and some kind of glossary that shows all the codes bundled under those classification umbrellas"
> "gather all ICF, access needs, disability identities/populations in base"
> "I don't think the mapping is correct"
> "https://icd.who.int/browse/2026-01/icf/en"
> "our project filters specifications based on three approaches, and the browsing user chooses one of those approaches to use for browsing"
> "ICF codes/classifications (e.g. Neuromusculoskeletal and movement-related functions, Movement functions b750-789)"
> "Access needs (e.g. wheelchair access)"
> "Disability identity (e.g. wheelchair user)"
> "So we should have a list of access needs, we should have a list of disability identities, and we should be able to map them to one another"
> "and from there, perhaps, we select ICF codes that pertain to those relationships"
> "Okay. Opus to reconcile, make rulings as required and allow us to keep moving forward in project" (2026-11-23)

In force:
- The ICF umbrellas and glossary are asked for; derived from the persisted WHO payload (`retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip`), never from recall. [unratified reading: umbrellas = WHO ICF blocks and the group above them]
- The three browsing approaches are the three lens columns of a specification (ICF, access need, identity); a browsing user picks one. [unratified reading]
- [unratified reading] "gather all ICF ..." asked for a listing of what base holds, not necessarily that base hold every ICF code (see OD-81).
- Pairs before ICF: resolved under delegation by OD-73 (2026-11-25 second): no pairs table; "should be all three" stands.
- The mapping the owner doubted: resolved under delegation by OD-77 (2026-11-25 second): read as `identity_icf_map`.
- The 2026-11-23 delegation does not reach decisions reserved to the owner (`governance/decision-protocol.md` §2.4 item 2: population taxonomy structure), and a task needing the owner's own words is not opened by a delegated resolution. (Extended by the owner's 2026-11-25 statements, below.)
Open: none further in this entry.

### 2026-11-23 — delegated resolutions: ICF hierarchy, glossary, mapping hold (OD-74, OD-75, OD-77); OD-73, OD-76, OD-78 referred back [L8437-L8469]
Recorder/delegate entry — not owner words.
In force:
- OD-74 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): `base_icf.parent_code`, nullable, referencing `base_icf(icf_code)`; WHO level-2 and level-3 blocks as rows keyed by the span of the 3-digit categories under them, derived from the payload; level 1 is the `component` column; `d910–d920` is not a WHO block (WHO's is d910–d999) and gets no parent and no umbrella standing; one writer derives block spans, parents and titles from the persisted payload; a title verified against that code's own row of the payload may replace a title whose source is not a payload, with old value and source recorded in the data migration's header. First data batch imports the blocks and the codes the project already holds; the rest only if the owner says so (see OD-81).
- OD-75 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): a cell keyed on an ICF umbrella gathers the codes beneath it; `IDENTITY_FAMILY_SQL`/`identity_family` are generalised, not copied (derive callers: `git grep -n -E "IDENTITY_FAMILY_SQL|identity_family|lens_differs" -- scripts`); the access-need lens stays flat (its `family` column is its grouping); the glossary is `db.py icf-glossary`, no view and no committed file; no browse filter reads a crosswalk (D-0184 unchanged). Test whether writing parents changes what an existing cell gathers (T055-03's `RULE_VERSION` premise) before merge; the change goes in a tooling-only PR the owner reads before it merges. ("Yes, build the tooling PR", 2026-11-25.)
- OD-76 (write `parent_code = MOB` for SCI and LMB): WITHDRAWN — superseded by the owner's 2026-11-12 eighth and ninth sets (LMB leaves mobility; SCI is held with WHEEL). No parent edge written; no `amend-identity --parent` flag.
- OD-77: resulting state per 2026-11-25 (second), below. `access_need_icf` stands; `access_needs.absorbs` is read only as prose proposing a pair, under owner review; the recorded provenance of `identity_icf_map` is the functional-deficit-auditor skill's table via a crosswalk of retired population codes (UPL, VIS, LOW-VISION, OFS, PCS, ABI, ASD).
- OD-73, OD-78: resolved under delegation 2026-11-25 (second), below.
- Tooling for OD-74 and OD-75 may be built in a tooling-only PR with no rows, read by the owner before merge; the data batch follows in its own PR. Derive every count in the reconciliation again before use.
Open: none further.

### 2026-11-25 — build the tooling PR; Opus may approve and ratify; finish the remediation plan [L8471-L8497]
Owner words:
> "Yes, build the tooling PR"
> "double check work carefully, send to opus for rulings/adjudication as required"
> "authority granted to opus to approve and ratify"
> "i just want to get this remediation plan done asap"
> "as always refer to doctrine/mission/claude.md etc for guidance as required"

In force:
- The tooling PR of OD-74 and OD-75 (including the engine gather-clause change) is asked for; the owner reads it before it merges. [unratified reading]
- An Opus-class delegate may approve the coordinator's work and ratify delegated resolutions; each ruling is written as `OD-NN STATUS: RESOLVED UNDER DELEGATION` (never `ANSWERED BY THE OWNER`) and checked by a different instance before its check line reads `confirmed`.
- Do not write an "Owner" ledger heading for a ruling the owner did not make; do not relax a guard binding a row to the owner's review (e.g. `review-identity-need-icf --approval-ref`); a delegate's ratification does not meet it.
- A delegate rules against recorded doctrine and rules (`governance/mission-and-epistemics.md`, `CLAUDE.md`, `governance/tier-system.md`, `governance/decision-protocol.md`, the ledger) and names the passage each ruling rests on.
- [unratified reading] "this remediation plan" = `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`.
- [unratified reading] A ruling deciding what a group needs or which ICF code ties to which identity is recorded with its basis in the record, not the delegate's knowledge.
- Reach of the grant over population-taxonomy decisions: see OD-79 and the owner's 2026-11-25 (sixth) statement below.
Open: none.

### 2026-11-25 — delegated resolutions: grant reach (OD-79), WHO tabulation (OD-80), ICF import grain (OD-81), OD-77 corrected; OD-73, OD-78, OD-82 referred back [L8499-L8539]
Recorder/delegate entry — not owner words.
In force:
- OD-79 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): the 2026-11-25 grant reaches approval of the coordinator's work and decisions of schema, method and ordering satisfying methods the owner has ruled. It does not reach: population-taxonomy structure and the statement that a group has a need (`governance/decision-protocol.md` §2.4 item 2, "always DG-NON"); what the owner meant by the owner's own words (e.g. "perhaps"); a row the schema binds to an "Owner" entry; the 2026-11-12 convention. [STATUS UNCERTAIN only as to scope: the owner's 2026-11-25 (sixth) statement delegates the specific questions named there, superseding this limit for them — recorded as an unratified reading in that entry.]
- OD-80 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): the persisted WHO simple tabulation grounds a code's existence, title and place in the hierarchy; it holds no relation between an identity or need and a code. A persisted WHO entity page retrieved through `retrieval_log` may be quoted for what a code means (untested: none retrieved). "A payload fetched from WHO under T-128" does not admit the tabulation as a warrant for an identity's code.
- OD-81 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): the first data batch (T-148) imports level-2 and level-3 blocks and the codes the project holds; importing every 3-digit category (derive: Code column matching `[bdes]\d{3}`) is a delegated reading, proposed to the owner with T-148, not run before it.
- OD-77, OD-73, OD-78, OD-82: resulting state per 2026-11-25 (second), below.
- Critical path is derived by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py` (listed then: T-102, T-128, T-127, T-059 with T-143, T-068, T-117, T-122, T-037, T-038, closed by T-110; T-120 and T-137 ungated tooling). [CHECK — T-128 since withdrawn, OD-87] The generator's block of T-135 on OD-69 is an artefact of how it reads gates.
- The 29 identity-need pairs: see OD-85.
- ACTION (2) and (3) of this entry (build no mobility split or identity-to-ICF row; put five questions to the owner) are overtaken by the owner's 2026-11-25 (sixth) statement and the second delegated resolutions.
Open: none further.

### 2026-11-25 (sixth) — Opus adjudicates the referred-back questions; the owner will not answer now; the project is simple [L8541-L8563]
Owner words:
> "Opus to adjudicate all of the above and log it"
> "I don't want to answer these right now so just make it happen"
> "Remember that this project is simple!!!"

In force:
- An Opus-class instance rules on the questions named (OD-73, OD-78 clauses 3 and 4, OD-82, which mapping the owner doubted, the 29 pairs and 63 repeated rows, OI-55 item 1 with SCI); each ruling is a delegated resolution (`RESOLVED UNDER DELEGATION`, never `ANSWERED BY THE OWNER`), logged in the ledger with basis, checked by a different instance before `confirmed`. [unratified reading of "all of the above" and "log it"]
- [unratified reading] This supersedes OD-79's limit for those questions; it does not reach what the schema binds to the owner's own review (`review-identity-need-icf --approval-ref`, `retire`); §2.4 stays the rule for everything not named.
- [unratified reading] The questions are not put to the owner again before work goes on; the coordinator carries out what the rulings open; this does not by itself authorise merging a PR.
- A ruling says which tasks it opens and what it leaves for a mechanism the schema binds to the owner.
- Rule for the smallest change meeting the owner's recorded words (CLAUDE.md §8 order: do nothing and say why; change a rule or convention; reuse; delete the cause; only then add the smallest code); add no apparatus the questions do not need.
Open: none.

### 2026-11-25 (seventh) — CLAUDE.md's goal states the project is simple [L8565-L8580]
Owner words:
> "maybe claude.md goal should also state this is a simple project where we build as little machinery as possible to enact our goal"

In force:
- Meet the goal with the least machinery; apply CLAUDE.md §8's order to every task.
- [unratified reading] "maybe" invites the edit; a sentence in CLAUDE.md's Goal section quotes the owner and points at §8; the owner may replace the wording and merging approves it. The sentence adds no rule and no check.
Open: none.

### 2026-11-25 (second delegated set) — OD-73, OD-77, OD-78, OD-82, OD-83 to OD-87 [L8582-L8624]
Recorder/delegate entry — not owner words (under the owner's 2026-11-25 sixth statement). No ruling here is an owner answer; none writes an "Owner" heading; no guard is relaxed.
In force:
- OD-73 (RESOLVED UNDER DELEGATION; CHECK confirmed): no pairs table; "should be all three" stands. A pair is a row of `identity_need_icf` whose ICF code is one of the need's own `access_need_icf` codes (counts as coverage, 2026-11-21 sixth); "perhaps, we select ICF codes" = further rows for a pair with a body-function or activity code where grounded. Nothing is built.
- OD-86 (RESOLVED UNDER DELEGATION; CHECK confirmed): the 63 rows that repeat a need's own codes are kept (the owner-ruled coverage; retiring them would need an "Owner" `retirement_ref`). Derive: `select count(*) from identity_need_icf t where retired_at is null and exists (select 1 from access_need_icf a where a.need_code=t.need_code and a.icf_code=t.icf_code)`. OD-80 and OD-81 stand as checked on 2026-11-25.
- OD-85 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): the 29 live pairs — class A (need's registry text names the identity's group, or each names the other) and class B (need names a condition the identity's description lists; mission commitment 1) accepted; class C (BRAIN with A-NOSPEECH, COM with A-LOWLOAD; warrant "recorded as an inference") rejected — with no row changing state; a delegated accept is never cited as a review or warrant; `stated` and retirement stay the owner's mechanism. Settles A-TRIGGER for COM and EPI. T-127 does not take class C rows as proposals. Derive classes: `select identity_code, need_code, warrant from identity_need_icf where retired_at is null`.
- OD-77 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): `identity_icf_map` is taken as the mapping the owner doubted (delegated reading resting on range codes: only it holds ranges among ICF link tables). The freeze binds additions a session proposes (no session adds a row, cites one as a warrant, or copies one); it does not bind owner-confirmed rows: per the owner's OI-03 answer ("Yes, as proposed": WHEEL to d465, d420, d410 beside SCI crossings T-102 judges to hold, "T-102 writes them"), T-102 writes the OI-03 crossings and carries each SCI crossing to WHEEL or retires it by judgment. The PR-245 rows are not condemned.
- OD-87 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): T-128 is withdrawn (its file marked withdrawn). The reach code `d4452` is minted by `add-icf-code` when T-127 needs it, after PR 246 merges (parented at mint, OD-74); T-127 waits for that merge or for T-148; T-059 and T-110 drop the clause taking `d4452` from T-128. OD-67 is moot while T-128 is withdrawn; if reinstated, its list is owed again.
- OD-78 (clauses 3 and 4; RESOLVED UNDER DELEGATION; CHECK confirmed): do nothing; no proposal path. A body-function code reaches a figure as a lens link when the clause names the function, and reaches an identity only from the owner's words (as TRIPLE-64); the 2026-11-21 (third) ACTION (2) and the 2026-11-23 interim stand.
- OD-83 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied; replaces OD-82): SCI retires into WHEEL, per the owner's OI-13 answer ("SCI is the same as WHEELCHAIR basically", 2026-11-12 seventh set) and the eighth-set heading, which `retire-identity --approval-ref` takes; the medical-lens deletion did not restore SCI. Order: T-102 mints WHEEL; carries SCI's three lens links to WHEEL and its `identity_icf_map` crossings to WHEEL or retires them by judgment (OD-77); closes GAP-111 (the OI-77 question) with `close-gap --resolution-kind ledger` citing this entry; then retires SCI (refused while a carrier remains). Retirement is one-way through sanctioned verbs (`amend-identity` takes no `--status`); restoring SCI needs a compensating migration.
- OD-82: RESOLVED UNDER DELEGATION; CHECK confirmed (decided the other way: OD-83).
- OD-84 (RESOLVED UNDER DELEGATION; CHECK confirmed with corrections applied): a carry-only batch (searches and admits nothing) is red on R1, R9a and R9b by construction; that red, and only that, is recorded in its PR body; every other rule of `research_batch_dod.py` must pass; its own task tests and the rebuild gate it; it does not move `sessions/LATEST-RESEARCH`. Applies to tasks whose gate text names it (`grep -l "red by construction" workplan/2026-11-12-bidirectional-pipeline/tasks/*.md`) and ISSUES-REGISTER ISS-005 (T-081, T-082, T-084, T-102, with T-111). `.claude/commands/batch-done.md` says so.
- ACTION: build no pairs table, no body-function proposal path, no new check; do not set a pair `stated` or retire a class C row (the owner's mechanism); T-102 runs in full with existing verbs (mint WHEEL, write OI-03 crossings, carry or retire SCI's rows, close GAP-111 citing OD-83, retire SCI; carry-only under OD-84); T-127 waits for PR 246's merge (or T-148); derive every count by the command beside it, never quote one.
Open:
- GAP-379's `e120`/A-SIZE question for LPA, TALL and BAR stays open.

---

Slice stats: entries read 46; entries reduced to nothing in force 0; entries tagged [STATUS UNCERTAIN] 3 (2026-11-20 third, 2026-11-20 fourth, 2026-11-25 OD-79 scope); lines read 7393-8625.
