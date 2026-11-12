# 41 — Owner rulings, verbatim

_Generated 2026-11-12 02:02 UTC at commit e73b588 by build_owner_prose.py; verbatim text is copied, never paraphrased._




<!-- O01 references/project-standards.md:6-58 -->

## Core Doctrine (locked)

RULE: THE PURPOSE OF THIS GUIDEBOOK IS TO GET PEOPLE TO ASK THE RIGHT QUESTIONS. This is the most important principle governing the entire project. The guidebook is not a prescription manual. It is not an authority on measurements. It does not dictate values that designers, policymakers, or practitioners must apply. It is a thinking tool that equips people to ask the right questions about how to design for accessibility depending on the circumstance. Measurements, ranges, and reference data exist to support this process — they serve the questions, not the other way around. Every item specification, every BPC synthesis, every piece of guidebook prose must be evaluated against this standard: does it help the reader ask better questions about this design element? Does it surface considerations they would not have encountered otherwise? Does it make them think more critically about the specific situation they face? When you know better, you do better. A designer who knows what questions to ask will produce a better outcome than one who does not — even without perfection, even without specialist input. The guidebook aims to raise the floor of understanding for everyone who touches the built environment.
DATE: 2026-04-24 23:38 — enshrined as foundational principle; governs all other rules

RULE: Disability populations are not uniform. Every person within a population code has a unique experience and unique functional limitations, even where there is significant overlap with others who share the same condition. There are different ways to struggle with mobility, different ways to be blind, different ways to have MS, different ways to be autistic, different ways to have dementia, different ways to experience PTSD. There is no generic ideal for any population. Specifications provide ranges and starting points — not definitive answers. It is rare for a disability to be experienced in isolation; co-occurring conditions are the norm. Every item specification must acknowledge functional variability within the population and discuss how co-occurrence affects the design parameter, because that is the lived reality of the people the guidebook serves. Population codes are a high-level organizing principle: at Universal Mode they are comprehensive (mapping all considerations); at Population Mode they offer insight (what to think about for a known population); at Person Mode they step aside because a person is not defined by their disabilities — OT works bottom-up from functional impairments because everything must be uniquely tailored to the individual.
DATE: 2026-04-24 23:38

RULE: Design Modes governs all specifications. Universal Mode = Universal Design / Code Compliance (population-agnostic, fixed values). Population Mode = Population-Informed Inclusive Design (ranges; median as default). Person Mode = Person-Specific Co-Design (OT assessment resolves position within the Population-Mode range). DAR mandatory at all modes.
DATE: Established — pre-session

RULE: Evidence hierarchy is seven tiers, per governance/tier-system.md (OPERATIVE 2026-05-25, owner directive "t2>t3 this is enshrined"; DR-2026-05-29 ACCEPTED 2026-07-13). Tier 1 = primary research with intervention-level or biomechanical control (OT-prioritized, not OT-exclusive, per D-E); Co-1 = lived experience / participatory design (CRPD Art. 4.3, co-primary with Tier 1); Tier 2 = synthesis — (a) systematic reviews / meta-analyses AND (b) named-organisation evidence-based standards; Co-2 = OT professional body CPGs (co-primary with Tier 2); Tier 3 = lower-control primary clinical research + grey-literature primary research (supporting; rarely the sole basis — T3-alone never reaches `stated`, per the tier3-stated-threshold DR); Tiers 4–6 = the regulatory stratum (international standards, national frameworks, statutory codes) — walled off from best-practice anchoring; convergence-not-evidence. The evidence hierarchy determines what constitutes best practice. Where higher-tier evidence exists, it governs.
DATE: 2026-03-19 19:00; consolidated 2026-03-29; elevated to Core Doctrine 2026-04-24 23:46; reconciled to the canonical ladder 2026-07-13 (ratification record; this rule previously restated the superseded pre-2026-05-25 ordering)

RULE: Best practice means the most accommodating, thoughtful, respectful, dignified, and usable condition achievable for the disabled person. Best practice is determined by the evidence hierarchy — Tier 1 primary research, Co-1 lived experience, Tier 2 synthesis (SR/MA + named-organisation evidence-based standards), Co-2 OT CPGs — not by code consensus. Codes are Tier 6: the compliance floor, not the aspiration. Code consensus across jurisdictions establishes what most codes agree on; it does not establish what is most accommodating or most dignified. A BPC best_practice_synthesis that derives its value solely from code consensus is a weak-band (○) best-practice claim — "best practice as currently known," valid only when flagged code-derived with the convergence-not-evidence caveat, and never rendered unflagged or above the weak band (amended 2026-07-21, owner directive, Option A; `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md`). An unflagged or full-strength code-consensus best-practice claim is in error. The test: does this specification provide the most accommodating, dignified, usable condition the evidence supports — or does it merely reflect what codes agree on?
DATE: 2026-04-24 23:46 — replaces and supersedes prior "best practice is not determined by code" rule

RULE: Universal design is co-extensive with code compliance — the floor, not an aspiration. Inclusive design is the positive aspiration.
DATE: Established — pre-session

RULE: Evidence specification markers, per governance/tier-system.md §5. ● = confirmed evidence base (T1, T2 both streams, T3-clinical, Co-1, Co-2). ◐ = policy/standards basis only, not primary evidence (T4, T5). ○ = grey, expert consensus, thin base, unconfirmed (T3-grey, [EXPERT CONSENSUS], [THIN BASE], T6). A T4–6-only basis never renders best-practice language in any register (G1b, invariant I3). Every specification sentence carries a marker; for quantitative specifications the confirmed marker additionally requires value-level support, not only direction. Unmarked = error.
DATE: 2026-03-20 21:00; reconciled to the ●/◐/○ system 2026-07-13 (the prior two-marker rule graded T4–6-only as ● — the convergence-laundering failure mode in its oldest form)

RULE: BAR is not a main taxonomy code. Large body size is not a disability. BAR provisions belong in Supplementary Volume Supp. Part 4 only. No BAR reference, cross-reference, heading, or J-code is permitted in Volumes I–II. Delete on sight without replacement or pointer. Category J (J-01–J-05) is struck from Volume II Part 4.
DATE: Established — pre-session; consolidated 2026-03-29

RULE: Specification ranges are not expressions of uncertainty. They are the designed-in bridge between Population Mode and Person Mode. At Population Mode use median. At Person Mode resolve through co-design. Never write a range without specifying which end applies at which mode.
DATE: Established — pre-session

RULE: Lived experience evidence (Co-1) is co-primary with Tier 1 on the claim types it anchors (preference, dignity, autonomy, self-determined accommodation) — unconditionally, not merely where no clinical trial is feasible. (Reconciled 2026-07-13: this rule previously placed Co-1 at "Tier 3–4", contradicting Core Doctrine co-primacy.)
DATE: Established — pre-session; reconciled 2026-07-13

RULE: VIS, DEAF, DBL are three distinct independent population codes. VIS/DEAF as a compound code is an error. DBL ≠ VIS + DEAF. See workplan-orchestrator §Population Codes for full canonical list.
AMENDED 2026-11-06: the full canonical list is the `base_taxonomy_identity` table; the skill section this rule pointed to is retired. See "Owner instruction 2026-11-06 — retire workplan-orchestrator; /run-pipeline replaces it".
DATE: Established — pre-session; consolidated 2026-03-29

RULE: IntD (Intellectual Disability) is not a standalone population code. IntD provisions are proxied through DEM (wayfinding, cognitive simplicity) and NDV (sensory environment, Easy Read signage). No §2.12, no IntD matrix column, no IntD population code table entry. All IntD specifications carry THIN-BASE disclosure.
DATE: 2026-03-25 19:35; consolidated 2026-03-29

RULE: Biophilic Design (BIO-01–BIO-05) and Thermal Comfort (TC-01–TC-05) are in Appendices B and C respectively. Supplementary Resources A and B struck from Volume II body. No inline BIO- or TC- cross-references in Part 4 specs or room matrices. Single opening notice permitted in volume front matter.
DATE: 2026-03-18 20:10; consolidated 2026-03-29

RULE: The guidebook is a starting framework for professional judgment, not a substitute for it. Population-level specifications (Universal Mode and Population Mode) are necessary but insufficient. Part 1 must state this explicitly as a foundational principle.
DATE: 2026-03-26 16:00

RULE: Conflict resolution protocol (Part 5 and cross-synthesis escalation) operates at Population Mode only. At Person Mode, conflict resolution is the domain of the OT and the individual through co-design. The guidebook's Person Mode role is to equip non-OT professionals with decision frameworks and structured approaches — not prescriptive answers.
DATE: 2026-03-26 16:00

RULE: The guidebook is an advocacy project, not an authority. It does not teach professional judgment, does not confer competence, and is not a registered body, standard-setting organization, or regulatory instrument. It is derived from comprehensive research and presents its findings in a multimodal manner to equip people who touch the built environment with better questions, better evidence, and better starting points. Readers apply their own professional judgment, informed by this material. The guidebook's value is in the quality and comprehensiveness of the research it synthesizes and the accessibility of its presentation — not in any claim to authority over practice.
DATE: 2026-04-26 19:25 — enshrined as Core Doctrine; supersedes any language elsewhere that implies institutional authority or mandating power

---



<!-- O02 references/project-standards.md:849-977 -->

## RULES 2026-08-25 — the four owner rulings of 2026-08-24, entered as operative rules

Appended, not edited: this file is the append-only operative rule ledger.

**Why this entry exists, stated plainly because it is the finding.** These four rulings were given
on 2026-08-24, recorded in `decisions/DR-2026-08-24-scaffolding-is-phase-specific.md` §2 — and
**reached no operative surface for a day.** They were not in this ledger. They were not in
`CLAUDE.md`. Meanwhile PD-0, PD-3 and PD-5 all shipped to `main` *citing* §2.1. Work was being
executed against rulings that no rule surface carried, which is the defect
`workplan/2026-08-24-pointer-discipline-queue.md` records one level down and `CLAUDE.md` rule 0
records one level up. **A ruling that governs the work belongs where the work looks.**

They are **not proposals and were never awaiting ratification.** `CLAUDE.md` rule 0: a live owner
statement supersedes every prior ratified record it touches, on contact.

---

**RULE: Never write the same fact into a second table. Point, do not copy.**

> *"If you have reference identification in tables that allow them to be cross-referenced, then you
> don't need to duplicate anything from one table to the other aside from that reference identifier
> because you can point to it. I could literally have a thousand tables. So long as each table has a
> row with a column that shares the same reference identifier, then you can call up information from
> any one so long as you point to the correct table and column."*
>
> *"If a crossing row 'carries' its own reason, that introduces the possibility of error and drift
> because it implies the reason is being written across two or more tables. It is better to have a
> table cell point to another table cell than to rewrite."*
>
> *"A crossing row only takes its reference ID. If it is providing a reason, then that reason is
> specific to the new table."*

**DATE: 2026-08-24** — owner ruling. `DR-2026-08-24` §2.1.

Two corollaries that are not optional, both learned by failing:

- **A parity check is not a fix.** It makes a dual home *survivable*, therefore permanent. Do not add
  parity checks, triggers or CHECK apparatus to police a copy — remove the copy. (`CLAUDE.md` §1
  already puts the burden of proof on apparatus. H03/H04 were deleted for this reason, not weakened.)
- **A column a committed data migration INSERTs can never be physically dropped.** Migrations are
  append-only and replay from the baseline, so a DROP replaying before the INSERT that names it
  breaks `migration_reproducibility` — the trap migration 062 sprang. The available shape is
  **writer-retire, reader-retire, NULL forward**; the column stays as a tombstone. **Grep
  `scripts/migrations/data_*` for the column name before proposing any drop. That grep is the gate.**

---

**RULE: "Highly procedural" means pointer discipline, not a checklist.**

> *"Reference IDs carry from table to table across stages. Data relevant in one stage does not cross
> to another stage. We do not need an author name in a synthesis table when synthesizing information.
> We do not need an author name when writing a specification in a specification table. We do not need
> an author name when rendering in a render table. If we have the same reference ID, then we know
> that we can just point towards the relevant table in the relevant stage for that information. For
> rendering a citation, then, we point towards the evidence table for that reference ID."*

**DATE: 2026-08-24** — owner ruling. `DR-2026-08-24` §2.2.

Each stage — research → evidence → synthesis → specification → render — holds only its own stage's
data; anything from an earlier stage is reached by pointer on the shared reference ID. A renderer
needing a citation does not *receive* a citation, it *looks one up*. **No checklist of what may cross
is written and none is owed**: the rule is structural, enforced by schema shape, not by a gate.

**A view is a caller.** Migration 064 exists because 063 swept eight Python readers and six skills
and missed `v_item_provenance`. When retiring a copy, grep `sqlite_master` as well as the tree, and
**treat a 0-row object as unproven rather than clean** — an empty scope hid that defect from a
byte-exact render diff.

---

**RULE: The clue store exists to be copied out of. Duplication out of it is the point.**

> *"The clues table is a historical artifact. The DOIs it contains are expected to be used by the
> researcher and, if the researcher deems that DOI to be relevant, then it will write that DOI into
> the new correct evidence sources table. This means that whenever the new correct evidence sources
> table duplicates the DOI from the clues table, it simply means that the clues table was useful. We
> do not care about information in the clues table being duplicated. We just want to shortcut
> research time because we've already found so many sources."*

**DATE: 2026-08-24** — owner ruling. `DR-2026-08-24` §2.3.

| Case | Verdict |
|---|---|
| Same DOI in `source_locators` and in `evidence_sources` | **Fine.** The clue was useful. Not a defect |
| Same fact written into two tables *within* the live pipeline | **Defect.** Point, do not copy |
| Same DOI under **different reference IDs** | **Defect** — two identities for one source; `R9a`/`R9b` detect it |

`source_locators` is **exempt, permanently.** Its case-drifted DOIs are allowed to be wrong-ish; do
not spend effort normalising rows no determination may cite.

---

**RULE: Applicability is an OUTPUT of synthesis, never an input to it. Research the full cross-product.**

> *"Every research slug gets cross-referenced against a population code, access need or ICF code
> because there is always the chance that there is an unexpected connection between them. If we only
> link our taxonomy to research slugs by what seems obvious, we may miss evidence."*
>
> *"Until we have secured an astounding body of evidence and synthesized that work while
> cross-referencing against our populations/access needs/ICFs, we are not able to define these
> connections — we are waiting until we have finished our syntheses to ensure we define them with
> evidenced justification, not presuppositions."*

**DATE: 2026-08-24** — owner ruling. `DR-2026-08-24` §2.4.

**This inverts the model the project worked from for three days and dissolves the blocker called
critical.** `item_population_links` edges are **findings**, produced by synthesis and justified by
evidence. Writing them first is the presupposition the ruling forbids.

| Superseded | Operative |
|---|---|
| A-18's zero `item_population_links` is a defect blocking determination | It is the **correct state** before synthesis. Nothing is owed |
| D-0165 (population-taxonomy pass) blocks the deliverable | **D-0165 does not block research at all.** It is downstream of it. Every "blocked by D-0165" note is void |
| Frame research by the populations a slug already links to | **Every slug is searched against every population / access need / ICF code** — an unexpected hit is the point of running it |

**The frame is the full cross-product, and it is not optional.** Not *"which populations does this
slug already link to"*, which assumes the answer. Per `CLAUDE.md` §6 the frame is pulled as **ICF and
access-need codes WITH names**, never as bare `axis_code`.

**One structural consequence, recorded because it is owed work, not a defect to argue about:**
`search_executions` carries no population, access-need or ICF column, so a search cannot today
declare which cell of the cross-product it covered. The ruling is therefore unrecordable and
ungateable as the schema stands — which is exactly what `GAP-B01-003` already names (*"a population
that appears only as a conjunct in someone else's query has not been searched"*). The
pointer-correct shape is a junction on `exec_id`, mirroring `search_admissions`; **never a copied
code on the row.**

---



<!-- O03 references/project-standards.md:978-1005 -->

## RULE 2026-08-25 — Scratchpads are committed, not accumulated

**DATE: 2026-08-25** — owner directive: *"ensure that we are always committing our scratchpads to
the repository so that we actually have a surface to review… committed regularly enough that they
do not [get] impacted [by compaction]."*

A scratchpad that lives only in a session's context is not a review surface — it is a transcript,
and transcripts are lost to compaction, to session end, and to container reclamation. **This
repository has already paid for that twice in two days:** the pointer-discipline queue existed only
in one conversation and three of its items shipped to `main` citing labels (`M3`, `M5`) that no file
defined; and the Fable audit that designed the queue survived only because it was recovered from a
transcript before that transcript was gone.

- **Commit the scratchpad at every natural break** — a finished investigation, a batch step, a
  migration emitted, an answer given to the owner — **not once at session end.** The failure mode is
  a long uncommitted stretch, so the interval that matters is *elapsed work*, not file size.
- **Never wait for a session record to exist before committing working notes.** Both 2026-08-24
  sessions closed with no `sessions/` file, so their scratchpads had no home and their reasoning was
  nearly lost. If no session directory exists, create it and commit into it.
- **A scratchpad commit needs no ceremony**: `governance: session command log [YYYY-MM-DD HH:MM]` is
  a complete commit message. Cost is one commit; the thing it buys is that the work is reviewable at
  all.
- **`scratchpad/**/commands.jsonl` is exempt from `retired_vocabulary`** (`retired-vocabulary.yaml`)
  — it is a verbatim record of what was typed, in the same class as a search log. A session that
  greps for a retired term to prove it unused must not redden the check by doing so.

---



<!-- O04 references/project-standards.md:1006-1057 -->

## RULE 2026-08-25 — the pipeline is five stages: research → evidence collection → judgment → synthesis → render

Appended, not edited: this file is the append-only operative rule ledger.

> *"research → evidence collection → judgment → synthesis → render"*
> *"that works for me"*

**DATE: 2026-08-25** — owner ruling, given on being shown that eighteen pipeline models exist
in this repository and that the two live ones disagreed.

**THIS SUPERSEDES THE OWNER'S OWN FIVE STAGES OF 2026-08-24**, recorded in
`DR-2026-08-24-scaffolding-is-phase-specific.md` §2.2 and in this ledger's RULE of the same date
as *"research to evidence to synthesis to specifications to render"*. Two changes, both
substantive:

| 2026-08-24 | 2026-08-25 | |
|---|---|---|
| `evidence` | **`evidence collection`** | Named for the act, not the artifact |
| — | **`judgment`** | Restored as its own stage. Determination is not folded into synthesis |
| `specifications` | — | **Not a stage.** `specifications` is a table that `judgment` writes |

Per `CLAUDE.md` rule 0 this binds on contact and the 2026-08-24 wording is superseded, not
weighed against it. Both records are kept: this ledger is append-only and the DR carries a
supersession note.

**WHAT IT RATIFIES, AND THIS IS THE USEFUL PART.** It is the five-stage spine of
`DR-2026-07-13-pipeline-contract` (ACCEPTED 2026-07-21), which `governance/pipeline-contract.yaml`
declares and which the machine has been enforcing all along — `tools/pipeline_completeness.py:37`
holds `STAGES = ["research", "collection", "judgment", "synthesis", "render"]` and its freshness
gate `pipeline_completeness_fresh` is **blocking**. **The conflict between the owner's model and
the machine's is resolved in the machine's favour**, with one renaming: stage 2 is
**evidence collection**, not bare *collection*.

**Substrate is not a stage.** The vocabularies and registries — `items`, `populations`, `slugs`,
`terms`, `access_needs`, the crossing maps — are the layer all five stages point into. The
six-bucket model in `scratchpad/session_2026-08-24-pointer-discipline/fable-stage-discipline-audit-2026-08-24.txt`
PART 1 added SUBSTRATE as a sixth bucket; that addition is agent-authored and is **not** part of
this ruling. Its table-to-stage assignments must be re-derived against these five stages before
they are relied on again.

**Re-entrancy is untouched by this ruling and still holds.** `governance/pipeline-map.yaml`'s
antagonist finding of 2026-08-21 — *"the stages are table buckets, not phases… a walk re-enters
them"* — answers **write order**, a different question from what a stage may hold. A walk may
re-enter any stage; each stage's tables still carry only their own facts (rule 5).

**Owed, not done:** stage 2's identifier still reads `collection` in `pipeline-contract.yaml`,
`tools/pipeline_completeness.py` and the dashboard. `schemas/pipeline_contract.py` sets
`extra="forbid"`, so a display-name field cannot simply be added; the rename is a caller sweep
under `CLAUDE.md` rule 4 and is tracked as such rather than done in the same breath as this record.

---



<!-- O05 references/project-standards.md:1058-1145 -->

## SUPERSESSION RECORD — owner directive 2026-08-25, pipeline smoke test

**Recorded, not argued.** `CLAUDE.md` rule 0: *"A live owner statement supersedes every prior
ratified record it touches, on contact. Your job on hearing one is to record the supersession,
never to weigh the ruling against the paperwork it changes."* This is that record. It was owed from
the moment the directive was given and was not written until a read-only auditor pointed out the
omission — which is itself the failure rule 0 exists to prevent, committed by the session auditing
for it.

**The directive.** The owner commissioned a full-pipeline smoke test ahead of a mobility research
batch: *"run a smoke test on the pipeline from start to finish… ensure that you attempt to run all
skills/tools, including those that may not be explicitly built yet… ensure that you run every
skill/tool/hook/script/etc by stage"*, and separately *"use Fable 5 read-only to investigate the
consequences of each step… you are auditing Sonnet 5's output by contextualizing it against the
repository's doctrine/mission/pipeline."*

**What it touches.** The RULE of 2026-08-19 in this ledger — *"Adversarial review is a
truth-instrument bound to evidence, never a plan-instrument"* — restricts any commissioned pass to
a diff that (a) wrote rows to the research tables or (b) authored or amended a synthesis artifact,
and its ACTION clause (5) states: *"Budget: at most one adversarial pass per research batch. **A
pass on a pass is forbidden** — defects in a pass are the next batch's pass's business."*

The commissioned work is outside both limbs in letter: its subject is the **apparatus and the write
path**, not a research or synthesis diff, and its structure is explicitly a pass on a pass — three
read-only auditors whose subject is six stage traces.

**Scope of the supersession.** For the session
`session_2026-08-25-pipeline-smoke-test-mobility` only, and for its purpose only — establishing
whether the pipeline can carry a mobility batch before one is attempted. The 2026-08-19 RULE is
**not amended**. Its reasoning is undisturbed and its measurement still stands: ten fresh-context
passes between 2026-07-14 and 2026-08-19 examined no research output, because there was none. A
future session may not cite this record to authorise a critique of a plan, a census, a register or
another pass. **The next adversarial pass owed remains the one on batch 1's admitted rows**, under
the 2026-08-19 RULE unchanged.

**Why the distinction is worth keeping rather than dissolving.** The 2026-08-19 RULE targets passes
that *cannot be wrong about anything a reader could check* — its own words. This session's subject
is executable: every claim it makes is a command someone can re-run, and several were re-run and
overturned within the session. That is the property the RULE protects, arrived at from the other
direction. It is not a licence to audit prose.

DATE: 2026-08-25 — owner prompt commissioning the smoke test; recorded the same day.

---

RULE: The person-side demand layer is named `icf_demands`, and it is NOT folded into `access_needs`.
Owner ruling 2026-08-25, resolving the two items `DR-2026-08-24-scaffolding-is-phase-specific.md`
§R8 left explicitly NOT DECIDED. The layer presently called `axes` is renamed **`icf_demands`**
(`icf_demands.demand_code`, and correspondingly `item_demand_links`, `population_demand_map`,
`access_need_demand_map`, `slugs.serves_demands`, `situations.attaches_demands`). §R8 item 1 —
"axis" is descriptive vocabulary, never a domain identifier — stands and is now executable; its
prescribed replacement wording ("ICF-anchored access needs") is superseded by this ruling because
that name was already taken by a different table, and executing §R8 literally would have created a
collision between the two layers it is most important to keep apart.

**Why the fold is refused, measured.** `axes` and `access_needs` both hold 17 rows and are joined by
a 21-row map, which reads as duplication and is not:

| | anchors | carries | side |
|---|---|---|---|
| `axes` → `icf_demands` | ICF **b** (body function) + **d** (activity/participation) | `mechanism` | the person's functional demand |
| `access_needs` | ICF **e** (environmental factors) | `design_obligation` | what the environment must do |

The map is many-to-many (15 distinct codes each side across 21 rows, `A-REACH` fanning to 3). The
b/d ÷ e split is the social model expressed in the schema: demand on one side, obligation on the
other. Folding them would collapse person and environment into one table, which is the medical-model
regression this project's whole taxonomy resists. The 17/17 coincidence is a coincidence.

**A second defect in the retired term, recorded because it outlives the rename.** "Axis" asserts an
orthogonal scalar dimension. `AX-AMB` (ambulant movement) and `AX-WHM` (wheeled movement) are not
orthogonal — they are alternatives, simultaneous for part-time wheelchair users, and on ramp gradient
their demands are **opposed**. The ratified permitted-umbrella test (2026-07-23) turns on precisely
that distinction — an umbrella is forbidden when it collapses "opposed **or** orthogonal demands" —
so the metaphor flattened two words the rule depends on keeping apart. The substance of "work from
axes" is unaffected and survives the rename intact: every clause reads correctly with "ICF-anchored
demand mechanism" substituted. The word was decorative, not load-bearing.

CONDITION: Any session naming, querying, renaming or reasoning about the person-side demand layer, or
proposing to reconcile it with `access_needs`.
ACTION: (1) Use `icf_demands` and its codes WITH names, never bare codes (the 2026-08-18 rule
stands). (2) Do not fold the two layers; cite this record if asked to. (3) The rename itself is a
D-SCHEMA migration with a full caller sweep across four tables, six columns, a blocking check
(`validate_axes.py`) and 297 tracked files — it is scoped and owner-gated, and must not be attempted
piecemeal (§R8 item 3 stands unchanged).
DATE: 2026-08-25 — owner ruling, selecting `icf_demands` and refusing the fold.

---



<!-- O06 references/project-standards.md:2548-2589 -->

## The lens CHECK is "at least one", not "exactly one" — and the 2026-08-28 ACTION above is superseded on that clause only

The entry dated 2026-08-28 ends: *"Four lens columns, one CHECK, real FKs. Never a `population_*`
link table. **Never two lenses in one row.** `population_code` is retired in favour of the four"* —
and states the CHECK as a sum equal to 1.

**D-0182 (owner ruling 2026-09-01) overturned that clause**, in three messages: *"it is OKAY for a
link to be absent in a related taxonomy column"*, *"but a link MUST be tied to at least one"*, *"and
ideally it ties into many"*. Migration 065 built it accordingly, and the live table carries the
newer rule with the reasoning in its own comment:

```sql
-- The owner's rule, mechanised: absence in a lens is fine, absence in ALL of them
-- is not. COALESCE is the whole constraint — "at least one", never "exactly one".
CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
```

**Only that clause is superseded.** The rest of the 2026-08-28 ACTION stands and is still owed:
four lens columns, one CHECK, real typed FKs, never a `population_*` link table, and
**`population_code` retired in favour of the four** — which `specifications.population_code` has
not yet had done to it.

**Why this is recorded rather than edited.** This ledger is append-only, and a superseded ruling
that is silently deleted takes its reasoning with it — the 2026-08-28 rationale (a row naming two
lenses writes a fact the crossing maps already hold, rule 5) is a real argument that D-0182 answered
by ruling multiplicity acceptable, not by refuting it. A reader who meets the older entry first must
be able to find that.

**How this was found, because the search pattern matters.** A session about to record
"what a determination keys on is an open owner decision" grepped this ledger before writing it, and
found the owner had ruled the lens half on 2026-08-28. CLAUDE.md rule 4b names the inverse failure —
reporting a ruling absent from a search that could not have seen it — and this is the same error
wearing the other face: declaring open a question already answered.

CONDITION: Any session reading the 2026-08-28 lens entry, or designing a table that attaches a
determination to a group of disabled people.
ACTION: Apply "at least one" (`COALESCE ... IS NOT NULL`), never "exactly one". Everything else in
the 2026-08-28 ACTION stands, including the retirement of `population_code`.
DATE: 2026-09-09 — derived from D-0182 and the live schema; supersession recorded, not decided.

---



<!-- O07 references/project-standards.md:2590-2624 -->

## The project is five layers, and CLAUDE.md is Layer 0

Owner ruling 2026-09-09, quoted verbatim:

> **Layer 0** is Claude.md and tools/scripts that ensure that Layer 1's architecture/shape/pipelines/schema etc are working
> **Layer 1** is code architecture and data shape and pipeline orchestration and schematic compliance etc — it is what guides all processes in the pipeline
> **Layer 2** is comprised of each stage in the pipeline including its tools/workflows/processes/scripts etc
> **Layer 3** is the actual data being recorded in the tables
> **Layer 4** is supplementary data

**What this settles.** CLAUDE.md's own scope: it is Layer 0, so it holds **process, workflow and
rules**, and every volatile fact is derived there rather than stated. That is the standing
justification for rule 7 and for the removal of the hardcoded figures the file carried until this
date — cross-stage foreign-key counts, cross-stage view counts, and a `ref_id` high-water mark, all
three stale, one of them contradicting the list printed beneath it.

**A name collision to know about.** `layer-N` appears in frozen records dated before this ruling —
principally the retired `governance/pipeline-map.yaml`, moved to `_archived/governance/` on
2026-09-09 — where it means that file's old table-to-stage bucketing. It is **not** this five-layer
model. Do not read one for the other; the bucketing predates the seven-stage spine and must be
re-derived against it in any case.

**Why the map was archived rather than deleted.** Nothing executable reads it — the readers are
prose, two DRs and nine attestations. CLAUDE.md §8 puts retired reader-facing *content* in
`_archived/` and reserves deletion for executable surface, whose archive is git history. Deleting it
outright would also have left dangling paths inside frozen attestations, which is the defect rule 4
names by example.

CONDITION: Any session editing CLAUDE.md, or reading `layer-N` in a record dated before 2026-09-09.
ACTION: Treat CLAUDE.md as Layer 0 — process, workflow and rules; derive every volatile fact. Read
`layer-N` in older records as the retired pipeline-map bucketing, never as this model.
DATE: 2026-09-09 — owner ruling, quoted above.

---



<!-- O08 references/project-standards.md:2625-2683 -->

## The parameter registry is BASE; the prior corpus is archived out of reach of the common tools; `add-term` is the naming route for now

Three owner rulings, 2026-09-09, given together and recorded on contact per `CLAUDE.md` rule 0:

> *"parameter at base, archive prior corpus so it can't be found by tools we use commonly, use add-term for now"*

**(1) The parameter registry sits at `base`, not at `judgment`.** This settles a fork an adversarial
pass had opened: `governance/pipeline-contract.yaml` already stages `base-parameter-vocabulary` at
`base`, while a proposed design put the registry at `judgment` because that is where a parameter is
adjudicated. The ruling keeps the registry where the contract already stages it — the vocabulary is
the layer every stage points into, and *adjudicating* into a vocabulary is not the same act as
*holding* it. Rule 5 reads the same way: the registry is base substrate; the adjudication that puts a
row in it is judgment's, and it points.

**(2) The prior-version corpus is archived, and the test is reachability by the tools actually
used.** Not deletion — `CLAUDE.md` §8 reserves `_archived/` for retired reader-facing content and
deletion for executable surface. `_archived/` is in `.ignore`, so ripgrep and the Grep tool stop
returning it; `grep -r`, `git grep`, Glob and Read still reach it, which is the deliberate escape
hatch for history work. **What archiving changes is what a hit says about itself**: a path under
`_archived/` is labelled by its own path, while the same file under `references/` reads as live.
That is the whole benefit and it should not be oversold.

**(3) `add-term` is the naming route "for now".** The vocabulary runs through `terms`, and the
provisional wording is recorded as given — this is a working decision, not a doctrine, and it is the
owner's to revisit.

**Why (3) is discharging a defect rather than adding apparatus.** `adjudicate-term --outcome
NAMES-NEW` refused unless the term already existed — *"create the term first, then adjudicate
NAMES-NEW to it"* — and **nothing created one**. NAMES-NEW was an outcome the CLI documented and
could not reach: a checker whose satisfying writer does not exist, which `CLAUDE.md` §8 names as a
trap. `add-term` mints the term and writes its NAMES-NEW adjudication **in one act**, so a term with
no provenance is unreachable through the sanctioned path.

**Two refusals it carries, and why each exists.** A canonical name bearing a digit, a comparator or a
min/max word is REFUSED: that is the item-layer defect in miniature — a container that announces its
answer predisposes every finding filed into it, which is why the owner deleted the layer on
2026-09-01. And a name that already exists is refused as NAMES-EXISTING with the exact
`adjudicate-term` command to run instead, because minting a second term for one concept is the dual
home rule 5 forbids.

**`terms` was blind to the capture path, and that is the fourth time.** `dbcore.WRITABLE_TABLES` did
not list it, after the identical failure for `evidence_source_authors`, `source_locators`, and
`observed_terms`/`term_adjudications` a week earlier. Left alone it would have been worse than the
previous three: `add-term` writes two rows, so a harvest would have shipped the adjudication and
silently dropped the term it points at, producing a migration whose `term_adjudications.term_id`
violates its own foreign key. `terms` is now listed **before** `term_adjudications`, since the list
replays in order and the child references the parent.

CONDITION: Any session naming a design parameter, staging the parameter registry, or reading the
prior-version corpus.
ACTION: Mint parameter names with `db.py add-term --from-observation`, never by hand and never
bearing a value. Stage the parameter registry at `base`. Treat anything under `_archived/` as
prior-version content; if you meet an `[A-Z]-NN` code, it is not a container to file into.
DATE: 2026-09-09 — owner ruling, quoted above.

> **AMENDED 2026-10-09** for prepopulating the parameter list only: see "Owner statements 2026-10-09", item 3, below. Names that come out of research still follow the clause above.

---



<!-- O09 references/project-standards.md:2684-2733 -->

## Owner ruling 2026-09-09 (evening) — the determination is COMPUTED, not hand-assigned

Asked whether `DR-2026-08-19` §12.5's *"Permanently manual: … anything touching `specifications` …
The contract's premise is that these are judgment acts machinery can only **check**"* retires the
determination engine as a writer or merely human-gates it, the owner ruled:

> **"oh. you have to compute it. I can't handle this load manually. you need to repair this and
> anything else"**

**This supersedes §12.5's "permanently manual" clause as it applies to `specifications`, on contact
(`CLAUDE.md` rule 0).** The clause is not an argument against the ruling; it is what the ruling
changes. Recorded here rather than weighed.

**What was actually being asked.** Whether a cell's state — `stated` / `provisional` / `pending` /
`not_applicable` — is derived by a script from the tier arithmetic, or decided by a person and
merely recorded. `scripts/assess/assess_cell.py` derives it: anchoring strata, the T3-alone split
(T3-clinical-alone ⇒ provisional, T3-grey-alone ⇒ pending), the G1 regulatory-stratum test, §2.3
richness with jurisdiction distinctness, and the §1.7 directness conditioning. Migration 071
re-keyed `specifications` and left that engine writing `item_code, population_code` — columns the
table no longer has — so the only implementation of those rules could not emit an acceptable row.

**Two sessions had already read §12.5 as retiring the engine** (`sessions/session_2026-08-20…:212`
"the write path for a determination is hand SQL"; `…2026-08-22…:297` "a dead pilot engine"). Those
were session authors' readings, not rulings, and they are now wrong. The engine is repaired, not
deleted, and the reading it rested on is closed.

**What does NOT change.** The engine still refuses `data/guidebook.db` outright and emits SQL for
replay through `emit_data_migration.py` → `migrate_db.py`. Computing the state is not licence to
write the canonical blob; the migration path is untouched. Nor does this touch the Opus floor on
`best_practice_synthesis`, or the B-before-E gate, or any other clause of §12.5 — only the
`specifications` clause, and only as to whether a machine may derive the state.

**A ratified debt this makes urgent.** Three A5 items — G2 (an unassessed applicable dimension caps
at DOWN-WEIGHTED), G3 (Co-1 grain follows `co1_source_type`), G6 (`standard_eb` grain follows type ×
tier) — are ratified (`RATIFICATION-PACKAGE-2026-07-12.md`, owner directive 2026-07-13) and
implemented **only** inside `assess_cell.source_grain()`.
`workplan/2026-08-11-remediation-and-pipeline-anatomy.md:4661-4663` records them as *"UNENFORCED in
the shared model"*, and `schemas/directness.py` still maps `co1 → specific` and `standard_eb → code`
unconditionally. Promotion into the shared model is register item Q4. While the engine was thought
dead this was a dormant inconsistency; with the engine computing determinations it is a live one —
two implementations of one ratified rule, disagreeing.

CONDITION: Any session writing, checking, or reasoning about a determination's state.
ACTION: The state is derived by the engine, not asserted by hand. Do not cite §12.5's "permanently
manual" against a machine-computed `specifications` state; cite it for the reasoning doc and the
Opus floor, which it still governs.
DATE: 2026-09-09 — owner ruling, quoted above.

---



<!-- O10 references/project-standards.md:2734-2859 -->

## Owner rulings 2026-09-10 — the Layer 2 line, and owner-gated work

Asked whether the six checks that invoke Layer 2 stage tools are compliant, and whether
brokenness parked awaiting an owner decision falls under the deletion rule, the owner
ruled:

> **"deciding at Layer 2 isn't allowed, and owner-gated stuff stays"**

**Scope of the first clause.** It answers a question that was explicitly about CHECKS
("ensure that our checks are actually checking something, that we are only using Layer 0
or Layer 1 for checks"). A check may INVOKE a Layer 2 tool — a freshness check has no
other way to know an artefact is fresh — but the pass/fail judgment must be computed at
Layer 0/1. It does **not** retire a pipeline stage's own output: a stage tool producing
its stage's result is that stage doing its job, and judgment's job is to decide. The
2026-09-09 evening ruling directing the engine to compute the determination stands.

**Mechanical form.** "Decides" = the Layer 2 file contains a conditional non-zero exit
reachable from `main`. "Invokes" = a Layer 0 file runs it and computes the verdict from
its output. Six registry entries fail today: `author_fidelity`,
`research_contract_sync`, `pipeline_completeness_fresh`, `evidentiary_audit_fresh`,
`context_map_fresh`, `site_pages_fresh`.

**Scope of the second clause.** Work parked awaiting an owner decision is exempt from the
non-compliance deletion rule. Named today: `scripts/generate/room_page.py` and
`skills/question-author_SKILL.md`, both in `governance/schema-reference-exemptions.yaml`
awaiting decision 8 on the room stratum, open since 2026-08-02.

**Recorded late, and that is the point.** These rulings were acted on for two hours
before being written here. Rule 0's second sentence is *"Record the supersession"*, and
an unrecorded ruling binds nothing mechanical: a meta-script reads code, YAML and DDL,
never a transcript. This entry was added only after an audit observed that
`grep -n 2026-09-10 references/project-standards.md` returned nothing.

**CORRECTION, same day, owner:** *"you can decide at layer 2. why wouldn't you be able
to? layer 2 is reserved for actual project materials tho"*

The reading above was wrong and is superseded. **Deciding at Layer 2 is not prohibited** —
a stage tool decides constantly; that is what a stage does, and judgment's entire job is
to decide. The "decides vs invokes" test proposed above is therefore NOT the rule, and any
meta-script built on it would enforce a prohibition that does not exist.

**The actual rule is about tenancy, not about deciding.** Layer 2 is reserved for the
project's real stage work — its materials, tools and processes. Apparatus is not stage
work. So a CHECK does not belong at Layer 2 *at all*, whatever it does there: the check is
Layer 0 by definition, and may freely invoke a Layer 2 tool and freely let that tool decide
its own stage's business.

The six entries named above are still misfiled, for this reason instead: check logic is
sitting inside project-material scripts (`scripts/research/retrieval_log.py`,
`scripts/generate/research_contract_hook.py`, and four freshness checks whose verdict is
computed inside the generator they run). The remedy is unchanged — the check moves to
Layer 0 and calls the Layer 2 tool — but the test a meta-script applies is
**"is this artefact apparatus or project material, and does its filing match?"**, not
"does a Layer 2 file exit non-zero".

**SECOND CLARIFICATION, same day, owner:** *"layer 1 is ensuring that layer 2 works
properly when project parameters"*

This gives the layers their actual shape, which is a **recursion, not a checklist**:

> **Layer 0 ensures Layer 1 works. Layer 1 ensures Layer 2 works. Layer 2 is the project's
> real stage work. Layer 3 is what that work produces. Layer 4 is supplementary.**

Each layer's conformance question is therefore the same single question — *does it ensure
the layer below it works?* — and this is what the per-layer meta-scripts must measure,
rather than an assembled list of desirable properties.

**It also names the session's whole failure family in one sentence.**
`evidence_sources.scope` carried a CHECK, so Layer 1 stated what a valid value was; no
writer could set it, so Layer 2 could not produce one; all 9 rows are NULL and every
stored tier is underivable. That is not six unrelated bugs. It is **Layer 1 failing to
ensure Layer 2 works**, six times: a vocabulary with no writer, a table outside the
capture path, a CHECK value no verb can produce, a mirror missing a live column, a
contract criterion pointed at a retired object, a rule whose only executable home is the
stage it was supposed to govern.

So the L1 meta-script's test is not "is the schema well-formed" but **"for every Layer 1
statement about what Layer 2 must produce, can Layer 2 actually produce it?"** — and the
L0 meta-script's is "for every Layer 1 property, is something gating it?"

CONDITION: Any session registering a check, filing a script, or judging whether broken
apparatus may be deleted.
ACTION: File apparatus at Layer 0/1 and stage work at Layer 2. A check may invoke a Layer
2 tool and that tool may decide its own stage's business; what may not happen is a check
living inside project materials. Owner-gated brokenness stays until its decision is made.
DATE: 2026-09-10 — owner rulings and same-day correction, quoted above.

---

CORRECTION — 2026-09-10. **`v_item_extractions` is DELETED; the ledger entry that names it
live stands as written and is superseded here, not edited.**

**What is now wrong on the record.** The 2026-08-27 correction entry above (the cross-stage
VIEW count, `grep -n 'v_item_extractions'`) reads: *"Under that convention it is **five**, not
seven: `v_coverage_priority` (research+substrate) and `v_item_extractions` (evidence+substrate)
do not cross."* The view no longer exists. **Migration 073 dropped it**, having asked the
question `CLAUDE.md` §3 requires before any view is deleted — which stages does it span, and
does deleting it force the next reader back to copying — and recorded both the answer and the
sweep in its own text. The short version: the view joined `sve.item_code = i.item_code`, the
hop-4 item edge, and the owner's 2026-08-26 ACTION (5) says *"`items` survives as the Part-4
rollup only — no new writer keys anything on `item_code` at the judgment stage"*. The edge the
view was the pointer for is the edge the ruling itself deleted, so a reader deprived of it is
pushed toward the route the ruling installed, not toward copying. No replacement was built,
because nothing read the old one: `CLAUDE.md` §8, *"nothing is added without naming what reads
it."*

**Why this is an appended entry and not an edit at line 1669.** This ledger is **append-only**.
Editing the 2026-08-27 entry would silently rewrite what was true when it was written — the
view WAS live that day, and the count of five WAS correct under the stated convention. The
entry is not wrong about 2026-08-27; it is out of date about 2026-09-10, and those are
different things. Anyone re-deriving a cross-stage view count reads forward to here.

**Do not re-derive the figure from this entry either.** The five/seven count was a measurement
of a moving object and it has now moved twice. Derive it: enumerate `sqlite_master` views,
assign each stage under `CLAUDE.md` §3's seven-stage table, and apply the stated convention
that `base` is not a stage — a view reading one stage plus base crosses nothing.

CONDITION: Any session quoting a cross-stage view count, looking for `v_item_extractions`, or
reading the 2026-08-27 correction entry.
ACTION: (1) Treat `v_item_extractions` as deleted; migration 073 carries the reasoning. (2)
Re-derive any view count from the live schema — never quote 5, 7, or any successor figure. (3)
Leave line 1669 as written; this entry is its supersession.
DATE: 2026-09-10 — sweep of migration 073's prose callers.

---



<!-- O11 references/project-standards.md:2860-2903 -->

## Owner ruling 2026-09-11 — adjudication delegated for a named set; the medical lens gets filled

> **"Fable 5.1 to adjudicate and resolve all items that are presented to me. Opus to execute in
> agonist-antagonist method. Ensure that medical gets filled out."**

Register row **D-0188**. Three clauses, and the third is not what it looks like.

**Clause 1 delegates adjudication, and it reaches only the items that were presented.** On contact
this supersedes the Delegation clauses of D-0170, D-0169 and D-0182, and
`governance/decision-protocol.md` §2.4 items 2–3, **as applied to the enumerated items and no
further**. The DG-NON list is not amended generally. Reading it wider would be an agent enlarging
its own authority out of a sentence about a queue.

**Clause 3 ENFORCES AN EXISTING RULING. It does not make a new one.** D-0170 adopted the medical
lens on 2026-08-27 — *"yes we include the medical model too. we give our users the choice of what
model they want to use to browse the site."* This session had nevertheless escalated
*"`base_taxonomy_medical` stays empty; the medical lens is explicitly deferred"* as though it were an
open owner question. **That escalation contradicted a ratified ruling and is withdrawn.**

It is the identical failure §6 of `CLAUDE.md` already documents for the subject half of the cell key:
*a ruling can be in the repository, in the file §9 sends you to, and still fail to bind if the search
stops at the first answer it finds.* There the first answer was the lens half. Here it was an empty
table — 0 rows read as an open question rather than as an unexecuted ruling, which is rule 4's *"treat
a 0-row object as unproven, not clean"* failing in the other direction. **An empty table is not
evidence that nobody has decided.**

**What the adjudication then corrected, which matters more than the delegation.** The mechanism
D-0170 stated for lens-switching — *"a medical taxonomy needs the same crossings into the other three
or the lens cannot switch"* — was itself superseded on 2026-09-01. D-0184 measured that traversal
manufactures inference and made the lens a **column**: render is `WHERE medical_code = ?`. The
crossing maps survive as the authoring aid that lets a row state its other lens codes without
inference, and as the coverage measure — not as the render path. A session reading D-0170 alone
would have built the wrong thing, correctly citing a ratified DR while doing it.

CONDITION: Any session acting on an escalation, reading an empty base-vocabulary table, or citing
D-0170's crossing mechanism.
ACTION: Before escalating, search `sessions/` with `grep -r` (`.ignore` hides it from ripgrep) for a
ruling that already settles it — an empty table is the likeliest place a ratified ruling sits
unexecuted. Cite D-0184 for the lens mechanism, not D-0170. This delegation covers the enumerated
items only.
DATE: 2026-09-11 — owner ruling, quoted above.

---



<!-- O12 references/project-standards.md:2904-2953 -->

## Owner ruling 2026-09-11 — ICD-11 is the medical-lens source, at BLOCK grain, for correspondence

> **"Yes, use ICD-11."**
> **"eg MB5 series of codes discussing paralytic symptoms"**
> **"we are looking through ICD-11 for how it corresponds to our existing ICF/identities/access
> needs on a high level"**

This resolves the licensing hold recorded the same day: **DG-NON item 7 is answered — ICD-11 is the
source.** It also settles two things the adjudication had to guess, and corrects it on one.

**The grain is the BLOCK, not the entity.** MB5 is a block, and "on a high level" says so outright.
The adjudication had proposed 29 disease *entities* (6A02 autism, 8A40 MS, 8B00 stroke); that is the
wrong shape for a browsing lens and is superseded.

**The purpose is CORRESPONDENCE, not vocabulary.** The lens exists so a reader arriving with a
diagnosis reaches the functional demand the project holds. It is not a clinical nomenclature and must
not grow into one.

**THE JOIN IS DERIVABLE AND MUST STILL BE PRUNED.** ICF and ICD-11 are complementary WHO
classifications, and all 17 axes already declare ICF b-anchors, so the route is: ICD-11 block → the
ICF b-code it impairs → our axis → the identities and needs already attached. Nothing in that chain
is invented. **But it over-reaches, and the owner's own example proves it**: MB5 impairs b730 (muscle
power); b730 is declared by AX-AMB, AX-REA and AX-WHM; those axes carry nine identities including
BAR, LPA and TALL — who attach for *anthropometric* reasons, not muscle power. Run the join naively
and the map asserts that paralytic symptoms correspond to being tall. **That is the inference
D-0184 measured when it made the lens a column rather than a traversal, reappearing one hop further
out.** The route proposes candidates; judgment prunes; the pruning reason is recorded in the row's
`note` and its strength in `mapping_confidence`.

**What the lens reaches that nothing else does, as a measurement not an argument:** `AX-COG-L`
(Information-access demand, b117/b167) carries **zero** identities and is the only orphan of the
seventeen. ICD-11's intellectual-development and language blocks land there.

**AND NO CODE CAN BE VERIFIED FROM THE CONTAINER.** Measured: `id.who.int` 401 on every route, the
token endpoint 400 (OAuth2 client credentials required), the public browser a JavaScript application
whose HTML carries no codes, its search endpoint 0 bytes, and no WHO credentials in the environment.
So `icd11_verified_at` lands NULL on every row written today, which is precisely what that column
means. Free registration at `icd.who.int/icdapi` yields the credentials; set them on the remote
environment and `retrieval_log.fetch()` can persist real `codeinfo` payloads for
`add-medical --icd11-payload` to stamp from.

CONDITION: Any session writing a medical-lens row, or deriving an ICD-11 ↔ ICF correspondence.
ACTION: Work at block grain. Derive candidates through `axes.icf_b_anchors`, then PRUNE — never ship
the join's raw output. Leave `icd11_verified_at` NULL until a persisted WHO payload exists; never
write a code from recollection, which is CLAUDE.md §5(c) made worse by the payload being
unobtainable rather than merely unfetched.
DATE: 2026-09-11 — owner ruling, quoted above.

---



<!-- O13 references/project-standards.md:3063-3123 -->

## Owner rulings 2026-09-12 — the four `scope` escalations, closed from bytes

The owner ruled on three of the four questions in
`workplan/2026-09-10-b5b-scope-owner-escalation.md`, selecting among the options that document
itself tabled. Recorded as selections, not as quoted speech — the owner wrote no prose here and none
is invented for them.

**Ruling 1 — REF-00784: retrieve the abstract first, then let scope and tier follow from the bytes**
rather than from the three prose records that had said so since 2026-07-20. Done: PMID 20434614
efetch, persisted at `retrieval-log/session_2026-09-12-b5b-scope-rulings/f5d94e0feaa8d48f.xml`,
`sha256 f5d94e0feaa8d48f…`. Its own structured abstract states the design — **"Case series."** — and
the sample — **"The sample of convenience included manual wheelchair (MWC; n=109), power wheelchair
(PWC; n=100), and scooter users (n=14)."** `PublicationType` carries no human-subject design tag,
and the DOI in the payload is byte-identical to the stored row's. `lower_control` derives **tier 3**.
**The row moved from tier 1 to tier 3**, fifty-four days after the anchor sweep recorded that tier 1
was wrong. It governs no determination: `specifications.governing_refs` holds REF-00973/974/979/980,
checked before the write.

**Ruling 2 — REF-00971 / REF-00972: `lower_control` on both.** `scope` discriminates on study DESIGN
control, and a device bench measurement with no instrumented human protocol is observational.
`lower_control` derives tier 3, which is the stored tier, so no tier moved and the rows simply
stopped being underivable. **This ruling also settles ruling 1's design question independently** —
REF-00784 varies passageway width in 5-cm increments exactly as the scooter pair decrements room
size, so the two arrive at `lower_control` by the same reading and not by two.

**Ruling 3 — REF-00976: retrieve the J-STAGE record.** Done:
`d170cbf86507a07b.html`, `sha256 d170cbf86507a07b…`. The abstract establishes a cross-sectional
survey of built housing stock — *"clarifying actual features of the orientation to lifetime homes in
newly built residences in Japan"*, *"Most numbers of investigated residences are not proper…"*.
Buildings are measured, not participants; no intervention. `lower_control`, tier 3 unchanged.

**Ruling 4 was not put and is still open** — retrospective ratification of the five `scope` values
B5(b) applied on 2026-09-10.

**THE WRITER THIS NEEDED DID NOT EXIST, which is why the tier sat wrong for fifty-four days.**
`tier` was reachable by no sanctioned writer: `_AMENDABLE` omits it and `correct-source` takes only
bibliographic fields from a payload. So the sole route to re-tier a source was hand SQL against a
table the CLI can reach — `CLAUDE.md` §4's coverage-bug shape. `amend-source` now takes `--tier`,
admissible **only** beside `--field scope` and **only** equal to the value the ratified ladder
derives from the new scope, written in the same statement. The original refusal is narrowed, not
removed: no path here writes a row the ladder cannot produce. Four refusal paths fault-injected
before use.

**What it unblocks, stated without overclaiming.** All 11 sources are now tier-consistent and none
carries a NULL scope, so B5a's tier gate no longer makes any of them non-anchoring — including the
three that measured corridor and passage geometry. They anchor at **T3**, not T1, so the
corridor-width cell is not thereby a `stated` determination; what changed is that the sources which
actually measured the parameter now reach the engine at all. Run the engine to find out; do not
predict the state here.

CONDITION: Any session amending `scope`, reading `adjudication_integrity`'s quarantine entry, or
planning the corridor-width cell.
ACTION: Amend scope through `db.py amend-source`, with `--tier` when and only when the ladder
derives a different tier; never by hand SQL. Read REF-00784 as T3. `adjudication_integrity` is GREEN
as of this date and stays quarantined — its promotion clause waits on OD-E, which was ruled
2026-08-31 (D-0179) and whose subject holds 0 rows, so promotion is an owner call with no mechanical
blocker left.
DATE: 2026-09-12 — owner rulings on the B5(b) escalation, executed the same day.

---



<!-- O14 references/project-standards.md:3124-3177 -->

## Owner ruling 2026-09-13 — a code value confirmed by research is upgraded; the empty circle is for code WITHOUT research backing

> **"Sometimes code standards come from T1. If a code standard is being confirmed as genuine best
> practice according to studies, then the code/regulatory input can be upgraded."**
>
> **"It is when a code/regulatory input does not have research backing that it gets the empty circle."**

**What this settles.** It was put to the owner as one of three band questions raised by the
2026-09-13 design pass: what strength a cell carries when its *finding* is T1 but its only *value*
comes from a code. The answer is the upgrade route, and it is ruled — not the two-part rendering
that was also on the table.

**WHAT IT EXTENDS, AND THE EXTENSION IS THE POINT.** `evidence-architecture.md`'s **G1** re-grains a
T4/T5 source out of NON-ANCHORING on exactly one trigger: *"its evidence basis is documented as
traceable to T1/T2 evidence, with that provenance recorded on the source record."* That is a
**genealogy** test — where the number came from. This ruling adds a second, independent route:
**confirmation** — a study finding the code's value sound, whether or not anyone can trace how the
committee reached it. The two are not the same test and the corpus already separates them:
**REF-00980** concludes *"changes to the technical requirements for ramp slope and length cannot be
recommended at this time."* It establishes nothing about ADA's provenance. Under G1 as written it
re-grains nothing. Under this ruling it upgrades the value it confirms.

**And it makes the empty circle CONDITIONAL where it was automatic.** `tier-system.md` §5 maps T6
(code-floor) to `○` flatly, and §8's band table gives `○ Weak` to "T6 (code-floor)" with a cell whose
entire basis is T4–T6 taking `○` regardless. After this ruling `○` marks the **unbacked** case
specifically: a code or regulatory input with no research behind it. A code value a study has
confirmed is no longer `○` by virtue of being a code.

**WHAT THE RULING DOES NOT SAY, recorded so nobody fills it in silently.** Three things.
(1) **Which band an upgraded value lands in** — the ruling says "upgraded", not "upgraded to ●". The
natural reading is that it takes the band of the confirming evidence, so a T1 confirmation yields
`●`; that is a reading, not the ruling, and it is the next thing to put to the owner.
(2) **Whether T4/T5 and T6 behave alike here.** The ruling says "code/regulatory input" without
distinguishing them, while existing doctrine splits them — `◐` for T4/T5 citations, `○` for T6.
(3) **What counts as confirmation.** REF-00980's non-recommendation of change is the clear case. A
study that merely *uses* a code value as its rig setting is not confirming it, and that distinction
is exactly what the `confirms` / `tested_at` edges of migration 075 exist to record.

**Mechanism, so this is executable rather than aspirational.** The 075 design gives the row-level
vocabulary: a `confirms` edge from a finding row to the code figure it confirms is the upgrade
trigger; `tested_at` is not; `insufficient` is the opposite and remains an open band question. The
engine rule that reads those edges is not yet built, so **the upgrade is ruled and unexecuted** —
which is the state an empty table should be read as, per the 2026-09-11 entry above.

CONDITION: Any session assigning a strength band to a determination whose value comes from a code or
regulatory source, or citing G1's traceability clause as the only re-graining route.
ACTION: Treat confirmation-by-study as a second re-graining route alongside documented traceability.
Read `○` as "no research backing", not as "is a code". Record the confirming relation on the row
rather than asserting the upgrade in prose. Do not assume which band an upgraded value takes — that
is unruled.
DATE: 2026-09-13 — owner ruling, quoted above.

---



<!-- O15 references/project-standards.md:3178-3220 -->

## Owner ruling 2026-09-13 — a derived figure takes a WEIGHTED AVERAGE of its inputs, not the weakest one

> **"Derived figures are a weighted average of their figures. If something has like two T1 and a
> single T4...it's probably a half circle."**

**This OVERTURNS the design pass's recommendation**, which was weakest-link: *"a derived figure
anchors at the weakest band of its inputs; if any input is a regulatory-stratum row the derived value
is code-derived (○) regardless."* Under that rule the owner's own example lands `○`. Under this
ruling it lands `◐`. The recommendation is withdrawn; it was session-authored and is not a record
this ruling has to be weighed against (rule 0).

**It extends a model that already exists.** `tier-system.md` §8, the weighted-strength anchor model
(DR-2026-07-20, owner directive), already holds that *"every tier can anchor a best-practice claim;
the strength of the claim is weighted by the tier of its evidence."* Today's ruling applies that
frame to the composite case — a figure computed from several figures — which §8 never addressed
because derived figures could not be represented at all.

**THE OPERANDS DO NOT EXIST, and that is the executable gap.** §8 assigns bands by MEMBERSHIP, not
by magnitude: T1/Co-1/T2/Co-2/T3-clinical → `●`; T4/T5 → `◐`; T3-grey/T6 → `○`. There are no numeric
tier weights anywhere in the project. **And the one column whose name promises them does not hold
them:** `weighting_profile.tier_weights` holds audience foregrounding — all five rows are shapes like
`{"foreground":["T1","CO1","conflict_notes","code_refs"],"delta":"show"}`, i.e. which tiers to surface
first for a designer as against a policymaker. A future implementer looking for the weights will find
that column and be misled. Recorded here so they are not.

**The worked example constrains the function, and the obvious implementation fails it.** Scoring the
bands `●`=3, `◐`=2, `○`=1, two T1 and one T4 average to 2.67, which rounds to `●` — not the half
circle the owner named. **Rounding DOWN yields `◐` and matches.** So the ruling's example is
satisfied by *mean of band ordinals, floored*, and is falsified by *mean, rounded to nearest*. That
is a reading, not the ruling: the owner said "probably", named no weights and no rounding, and the
choice between floor, a tier-count threshold, or genuine per-tier magnitudes is unsettled.

CONDITION: Any session assigning a band to a `figure_role='derived'` row, or implementing the band
rule in the determination engine.
ACTION: Compute from all inputs; never take the weakest. Do not read
`weighting_profile.tier_weights` as tier weights. Before implementing, put the weighting function
itself to the owner with the 2×T1 + 1×T4 = `◐` case as the acceptance test, and state which candidate
function you propose — do not pick one silently, because more than one satisfies the example and they
diverge on every other combination.
DATE: 2026-09-13 — owner ruling, quoted above.

---



<!-- O16 references/project-standards.md:3221-3258 -->

## Owner ruling 2026-09-13 — a finding that a CODE is insufficient supplies no value, and is still first-class evidence

> **"Insufficient findings don't provide anything, do they? They're insufficient. All you do is log
> you looked at them, I think"**
>
> — put back to the owner because the phrase carries two opposite readings, and confirmed as: **the
> finding supplies no VALUE, but is real evidence.** The cell stays `pending` on value; the finding
> anchors the cell in DIRECTION, remains first-class R7 harm evidence, and is rendered in the book.

**Why it was queried rather than recorded as first stated.** In the 075 vocabulary `insufficient` is
a RELATION, not a quality grade: it points from a finding row to *the baseline that finding says is
inadequate*. So an "insufficient finding" is a finding **that the code is insufficient** — not a
finding that is itself weak. Read the second way, the ruling would have discarded REF-00784's
*"Between 10% and 100% of users would not be able to maneuver in spaces that meet current
Accessibility Guidelines"* and REF-00971's *"None of the scooters tested were capable of completing
all manoeuvres within the space allowed by existing standards"* as log entries. Those are T1 and T3
findings that the built environment FAILS people, which the research contract's R7 makes first-class
evidence rather than a by-product, and which the mission — *"get people to ask the right
questions"* — points directly at. The clarification preserves them.

**What the ruling settles.** Such a finding cannot say what the right number IS, so it supplies no
value and cannot move a cell off `pending` on value. It can and does establish that the existing
value is wrong for these people, and that is rendered.

**The three band questions raised by the 2026-09-13 design pass are now all closed:** a code value
confirmed by research is upgraded and `○` marks unbacked code (entry above); a derived figure takes a
weighted average of its inputs, not the weakest (entry above, weighting function still open); and an
`insufficient` finding supplies direction, not value (this entry).

CONDITION: Any session grading a finding that a code or standard is inadequate, or implementing the
determination engine's treatment of `insufficient` edges.
ACTION: Never let such a finding supply `value_min`/`value_max`. Never discard it either — it anchors
direction at its own source's tier and is rendered. A cell whose only evidence is `insufficient`
findings is `pending` on value and states the inadequacy.
DATE: 2026-09-13 — owner ruling, queried and confirmed.

---



<!-- O17 references/project-standards.md:3259-3303 -->

## Owner ruling 2026-09-13 — grey literature that states a code's value is regulatory stratum, not independent evidence

> **"If T3-grey is the same value as T6, I think T3-grey is not T3 but T6"**

**What it is really about, and it is not the marker.** `tier-system.md` §5 maps T3-grey and T6 to the
SAME band — both `○`. So re-tiering such a source changes no marker. What it changes is the
**stratum** it sits in and, decisively, **whether it counts as an independent root**. Two `○` sources
stating the same number read as two sources converging; if one is echoing the other's code, they are
one source counted twice. That is the laundering this project already names
*convergence-not-evidence*, and it is the consequential half of this ruling.

**Machinery that already exists, so this is not built from nothing.** `v_value_independence` counts
`DISTINCT COALESCE(root_ref_id, root_id)` and admits only `root_type IN ('measurement_primary',
'participatory_finding', 'derived_calculation')` — a row recorded as `committee_assertion` or
`untraced` already corroborates nothing. `echo_of` and `root_id` carry the transmission chain, and
`references/methodology/value-genealogy-worked-example-corridor-width.md` is the worked precedent
(1800 mm's zero in-corpus roots against 2440/2400 mm's two independent roots).

**THE GAP THIS RULING FILLS.** All of that machinery tests **recorded provenance** — what an extractor
wrote down about where a figure came from. The ruling supplies a test for the case where provenance
was never recorded: **value coincidence with a code**. Grey literature overwhelmingly repeats code
values, and an unrecorded echo currently reads as independent corroboration.

**THE FALSE POSITIVE, stated because the rule is stated as an identity.** Two genuinely independent
measurements can land on the same number; a code value is often round and grey fieldwork often
reports round numbers. A T3-grey field study that independently measured 1500 mm and a code that says
1500 mm are convergence, not echo, and automatic re-tiering would erase a real corroboration — the
opposite error to the one the ruling prevents, and the harder one to notice afterwards.
**Recommended shape, for the owner to confirm or reject:** the coincidence raises a rebuttable
presumption of echo — the source sits in the regulatory stratum and contributes no independent root
UNLESS its own recorded provenance shows independent measurement (`root_type='measurement_primary'`
with a root that is not the code). That keeps the ruling's force, costs nothing when provenance is
absent, which is the common case, and does not silently delete a genuine second root.

CONDITION: Any session tiering a grey source whose value matches a code, or counting independent
roots for a parameter.
ACTION: Do not count a grey source as an independent root on value agreement alone. Check its
recorded provenance first; where none exists, treat it as regulatory stratum. Expect no marker change
— both bands are `○` — and expect the change to show up in independence counts and
`regulatory_stratum_only`, which is where it matters.
DATE: 2026-09-13 — owner ruling, quoted above. The rebuttable-presumption shape is a proposal, not
the ruling.

---



<!-- O18 references/project-standards.md:3304-3341 -->

## Owner ruling 2026-09-13 — the derived-figure weighting function: mean of band ordinals, ROUNDED DOWN

> **"yeah round down"**

Closing the function left open by the weighted-average ruling above. The band ordinals are the
weights: `●`=3, `◐`=2, `○`=1; the derived figure's band is the **floor** of the mean across its
inputs. Verified against the owner's own worked case and its neighbours:

| inputs | mean | band |
|---|---|---|
| 2×T1 + 1×T4 — **the owner's example** | 2.667 | **◐** |
| 3×T1 | 3.000 | ● |
| 2×T1 + 1×T6 | 2.333 | ◐ |
| 1×T1 + 2×T6 | 1.667 | ○ |
| 99×T1 + 1×T4 | 2.990 | ◐ |

**The property that follows from `floor`, recorded so it is a decision and not a surprise.** Only an
all-`●` input set reaches exactly 3.0, so **a single sub-`●` input caps the result below full circle
at any scale** — the last row above. The rule is therefore equivalent to: *a derived figure is fully
anchored only if every input is fully anchored.* That is consistent with the ruling it completes (the
T4 costs you the full circle), and it is the strongest consequence of rounding down rather than to
nearest.

**What "weighted" means here, stated because it was ambiguous.** The ordinals carry the weighting —
inputs are equally weighted and the tiers differ. If per-input weighting by something else was
intended (sample size, source count, directness), that is a different function and is NOT ruled.

**Note for the implementer.** `v_best_practice.strength_band` computes a two-value band today; these
are the three `●◐○` bands of `tier-system.md` §5/§8, and no numeric ordinal encoding exists anywhere
in the schema yet. It has to be introduced with the engine rule, not assumed to be present.

CONDITION: Implementing the band of a `figure_role='derived'` row.
ACTION: floor(mean(ordinal(input bands))), ordinals 3/2/1, inputs equally weighted. Test against the
five rows above; the owner's example is the acceptance case and it falsifies rounding to nearest.
DATE: 2026-09-13 — owner ruling, quoted above.

---



<!-- O19 references/project-standards.md:3342-3537 -->

## Owner ruling 2026-09-13 — the whole circulation corpus is untrusted and is cleared for a re-run

> **"I want you to clear all the recent research performed and how it went down the pipeline"**
>
> **"Basically all the circulation rows that have been produced are not able to be trusted, so we
> have to redo them all from the start"**

The second statement widened the first. "The recent research" read as batches 06 and 07; the ruling
is the whole slug. Executed as one compensating data migration
(`scripts/migrations/data_20260913040739_2026-09-13-clear-circulation-corpus.sql`, applied
2026-09-13 04:15) deleting **229 rows** — every row any stage produced under
`accessible-circulation-geometry`, reaching back through batches 04 and 05.

**The scope is the slug, not the sessions, and that distinction moved rows.** Deleting by session
stamp would have left 33 `observed_terms` that `session_2026-09-03-defect-programme` harvested from
circulation sources under its own name, and one `source_locators` row sitting in an 881-row table —
the row a re-run's R9 duplicate-DOI pre-check reads, so a stale locator for a deleted source is
exactly what makes a re-run cross-file against a `ref_id` that no longer exists.

**What was kept, and why none of it is research output.** `terms`, `term_aliases` and `slugs` are
base vocabulary minted 2026-05-09; TERM-001 `ramp gradient` and TERM-002 `corridor width` survive as
terms, while `base_parameters` — the *promotion* of those terms into the parameter layer — went, because
that promotion is research output. `research_code_leads` carries neither `ref_id` nor `slug`. The
acoustics corpus and `GAP-B01-*`/`GAP-B02-*` are out of scope. `retrieval-log/` is untouched on disk,
so a re-run verifies against the bytes the first run actually received and re-fetches nothing.
`sessions/` and `attestations/` stand as written: clearing rows is not erasing the audit trail.

**A CONSEQUENCE THE CLEAR CREATED AND DID NOT RESOLVE — read before the re-run.** Deleting the
thirteen circulation `ref_id`s dropped the global high-water mark from REF-00982 to REF-00970, because
the mark is the UNION over every `ref_id`-holding table (`dbcore.ref_id_high_water`) and only
`source_locators` still carries mintable ids. `dbcore.next_ref_id()` therefore returns **REF-00971** —
an identifier the batch-07 session record, its attestation, the retrieval-log manifests and PR #136 all
attribute to a different paper. A re-run will silently reuse REF-00971 … REF-00982 for new sources, and
`db.py`'s `_relation_quote_verified` searches *every* session's payloads with no structured `ref_id` in
the manifest, so a new REF-00971's quote can verify against the old REF-00971's bytes and read as
correct. `reference_stubs` is already in `ref_id_homes` and already carries a `RETIRED` status in its
CHECK, which makes it the obvious place to park the retired ids — but it was merged into
`source_locators` by migration 062 and has no writer, so reviving it is a decision, not a sweep.

**A second consequence, recorded not adjudicated.**
`decisions/DR-2026-08-19-research-restart-operative-instrument.md` records clause (c)'s freeze exit as
SATISFIED AND SPENT because `evidence_sources >= 1` was met, and `meta_work_freeze` was retired and
deleted on that basis. `evidence_sources` is 0 again. The DR says the freeze ended by its own terms, so
this is not a claim that it revives — but the condition that discharged it no longer holds and the gate
that could observe it no longer exists.

CONDITION: Any re-run of the `accessible-circulation-geometry` slug, or any future corpus clear.
ACTION: Settle the `ref_id` minting floor BEFORE admitting the first source, so retired identifiers are
not reissued. Derive the scope of any clear from the slug and its reachable `ref_id`s, never from
session stamps.
DATE: 2026-09-13 — owner ruling, quoted above. Recorded 2026-09-13 after an audit found the ruling
present in the migration, the session record and `governance/check-registry.yaml` but absent from this
ledger, which CLAUDE.md rule 0 requires ("Record the supersession").

---

RULE: **`AX-` may never denote an ICF code, anywhere.** Owner ruling 2026-09-13, quoted verbatim:
*"'AX-' for ICF should never ever exist anywhere."* Recorded on contact per `CLAUDE.md` rule 0.

**This answers the one question the `icf_demands` rename left open, and it answers it against the
status quo.** The 2026-08-25 RULE above renames `axes` → `icf_demands` and `axes.axis_code` →
`icf_demands.demand_code`, and the 2026-08-26 §R8 entry states that the rename "is SILENT on whether
the 17 **code values** are re-minted", that "the migration must state which", and that if they are not
re-minted then `AX-*` "stays correct live data" and belongs in the retired-vocabulary register's
`deferred:` section. It is now ruled: the values are re-minted. `AX-` is not correct live data.

**The surface, derived 2026-09-13 against the live database rather than quoted from the 2026-08-26
count, which predates the circulation clear.** 128 `AX-`-bearing values across fourteen columns:

| | |
|---|---|
| key columns | `population_axis_map.axis_code` 53 · `access_need_axis_map.axis_code` 21 · `axes.axis_code` 17 |
| free text | `terms.scope_note` 17 · `axes.falsification_condition` 8 · `access_need_icf.note` 3 · seven further columns 1 each |

Derive it, never quote it:

```
python3 - <<'PY'
import sqlite3; con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for (t,) in con.execute("select name from sqlite_master where type='table' order by name"):
    for c in con.execute(f'PRAGMA table_info("{t}")'):
        try: n = con.execute(f'select count(*) from "{t}" where "{c[1]}" GLOB "*AX-*"').fetchone()[0]
        except Exception: continue
        if n: print(f"{t}.{c[1]}: {n}")
PY
```

**WHERE THE RULING BITES HARDEST, and it is not the registry — it is four columns literally named
`icf_code`.** `specifications.icf_code`, `source_value_extractions.icf_code`,
`item_taxonomy_links.icf_code` and `icf_medical_map.icf_code` each carry a real FK into
`axes(axis_code)`, so the column called `icf_code` resolves, today, to an `AX-*` value. That is the
ruled state exactly: `AX-` denoting ICF, in the schema, four times over. Two further columns named
`icf_code` do NOT do this and must not be swept with them — `access_need_icf.icf_code` and
`population_icf_links.icf_code` (migration 080) hold real ICF codes and carry no FK into `axes`,
because there is no ICF registry to point at.

**What the ruling does NOT say, and must not be read to say.** It does not fold `icf_demands` into
`access_needs` — the 2026-08-25 RULE refuses that and its b/d ÷ e reasoning is untouched. It does not
retire the demand layer, whose rows anchor to ICF **b** and **d** codes in `icf_b_anchors` /
`icf_d_anchors`; those anchor columns are the layer's correct relationship to ICF and are not the
defect. And it does not license re-minting the 17 codes as bare ICF d-codes: an `icf_demands` row
anchors to both b and d codes, so no single d-code can stand for one, and collapsing the demand layer
into ICF would destroy the anchor relation the 2026-08-25 table sets out.

**TWO THINGS REMAIN UNDECIDED AND ARE NOT GUESSED HERE.** (1) The replacement code shape — `DM-AMB`
to match `demand_code` is the obvious reading and is still a minting decision every future row
carries. (2) Whether the four lens columns named `icf_code` are renamed to `demand_code` with the
registry, which would rename a LENS the owner ruled on 2026-08-28 (identity / ICF / access-need /
medical), or whether the ICF lens instead comes to hold real ICF codes and the demand layer becomes a
fifth thing. Those are put to the owner rather than settled by an implementer.

CONDITION: Any session writing, renaming or reasoning about the demand layer, the ICF lens, or any
column named `icf_code`; and any session about to add `AX-` to the retired-vocabulary register.
ACTION: (1) Write no new `AX-` value anywhere, under any column name. (2) Do not execute the re-mint
piecemeal — the 2026-08-25 RULE's action item 3 stands, and this ruling widens that migration rather
than replacing it. (3) When it runs, it states the new code shape and the lens-column decision
explicitly, because this ruling is what made both unavoidable. (4) The retired-vocabulary entry for
`AX-` still cannot be written in any of the register's three match modes — all require a non-`[\w-]`
character after the token, so `AX-` never matches `AX-AMB`; that is a matcher fact recorded on
2026-08-26 and unchanged by this ruling.
DATE: 2026-09-13 — owner ruling, quoted above.

---

RULE: **The ICF lens keeps its name and comes to hold real ICF codes.** Owner ruling
2026-09-13, selecting that option over renaming the lens to `demand_code`, and answering the
fork the same day's `AX-` ruling opened. Recorded on contact per `CLAUDE.md` rule 0.

**Executed the same day by migration 081.** `base_icf` is the registry, and all six columns
named `icf_code` now point at it: the four lens columns that had FK'd into `axes(axis_code)`
— `specifications`, `source_value_extractions`, `item_taxonomy_links`, `icf_medical_map` —
plus `access_need_icf` and `population_icf_links`, which already held real ICF codes and
pointed at nothing. The second pair matters as much as the first: without them `base_icf`
would be a *third* home for ICF codes rather than the one home, which is the whole point
(rule 5).

**A CORRECTION OWED TO THE OWNER, because the estimate put to them was wrong in the
direction that mattered.** The option was described as "a bigger data change — every
extraction and determination keyed on a demand code needs re-keying". It needed none. All
four lens columns hold **zero** rows: the 2026-09-13 circulation clear emptied
`specifications` and `source_value_extractions`, `item_taxonomy_links` has been unwritable
since its `item_code` FK reached into the emptied `items`, and `icf_medical_map` had never
been written. The option ruled for was the *cheapest* of the three, not the dearest. The
estimate was made from the 2026-08-26 count of 288 live cells, which predates the clear —
`CLAUDE.md` rule 7, in the one place where quoting a stale figure changed what was put to
the owner.

**What the registry holds, and what it deliberately does not.** 72 codes, seeded only from
codes this repository already held (`access_need_icf`, `population_icf_links`, and the
`axes` anchor columns) — never from a remembered classification. **29 carry a title and 43
do not**, because nothing here states them and supplying an ICF title from memory is the
2026-08-19 fabrication in a smaller field. `base_icf` refuses a title without a
`title_source`; `db.py set-icf-title --title-payload` verifies one against persisted bytes
the way `add-medical --icd11-payload` does for ICD-11. The 43 are logged as
`GAP-ICF-TITLES`, and they are a real gap on this lens: `CLAUDE.md` §6 requires working from
ICF codes **and names**.

**The demand layer is untouched and is no longer a lens.** `axes` keeps its 17 rows,
`population_axis_map` its 53 and `access_need_axis_map` its 21. The 2026-08-25 RULE's
refusal to fold the demand layer into `access_needs` stands, and its b/d ÷ e reasoning is
intact: the ICF lens now holds b and d codes directly, `access_needs` keeps its e-anchors.

**AN OPEN QUESTION THIS CREATES, recorded rather than answered.** The 2026-08-25 RULE
renames `axes` → **`icf_demands`**. Running that rename now would put `AX-` codes inside a
table whose name begins "icf", which is the state the 2026-09-13 `AX-` ruling bans. The
rename therefore cannot execute as specified, and what the demand layer should be called —
and whether it survives at all now that real ICF codes carry the lens — is owner-gated.

---

**OWNER STATEMENT, same day, recorded verbatim and NOT resolved here:**
*"access needs, ICF codes, disability identities"* — given immediately after the ruling
above.

READ AS: the three base vocabularies the pipeline keys on — `access_needs` (17 rows, ICF
**e**, what the environment must do), `base_icf` (72 rows, ICF **b**/**d**, the person's
function) and `populations` (23 rows, identity). That reading is what the work above acted
on, and it is consistent with the ruling it followed: the demand layer is not among them.

**WHAT IT WAS NOT READ TO DO, and this is flagged rather than decided.** D-0170 adopted a
**fourth** lens — medical — as a reader's choice, and D-0182 relaxed the `specifications`
CHECK to "at least one of four". Three words naming three vocabularies is not read here as
retiring a ruled lens, and no code or schema was changed on that basis. If the intent was
that the medical lens goes, it needs saying, because `specifications.medical_code`,
`base_taxonomy_medical`, `identity_medical_map`, `icf_medical_map`, `db.py add-medical` and
the blocking-adjacent `medical_lens_integrity` check all exist to serve it.

CONDITION: Any session reasoning about the lens set, the demand layer, or `base_icf`.
ACTION: (1) The ICF lens is `base_icf` and holds real ICF codes; mint with `db.py
add-icf-code`. (2) Do not re-introduce a demand code into any `icf_*` column — six FKs now
refuse it. (3) Do not treat the medical lens as retired without an owner ruling that says
so. (4) `GAP-ICF-TITLES` closes by retrieval and persisted bytes, never by recall.
DATE: 2026-09-13 — owner ruling and owner statement, both quoted above.

---



<!-- O20 references/project-standards.md:3538-3589 -->

## Owner ruling 2026-09-16 — RETIRE IN PLACE, NEVER HARD-DELETE

> **"retire in place then"**

Given in answer to the proposal `scripts/migrations/076_never_reuse_identifiers.sql` named and
declined to smuggle in: *"The single rule that would make both unnecessary is `retire in place,
never hard-delete`, for which the mechanism is already half-built (`evidence_sources.superseded_by_ref_id`,
`base_parameters.status = 'retired'`, `source_locators.status = 'RETIRED'`) … That is a doctrine
change and an owner decision, so it is named here and not smuggled in."* It is now made. Recorded on
contact per `CLAUDE.md` rule 0; the paperwork below is what the ruling CHANGES, never an argument
against it.

**WHAT IT SUPERSEDES.** 076's framing of the two floors as permanent; any future data migration that
hard-deletes rows to retract them; and `assess_cell`'s re-determination refusal keying on NOT EXISTS,
which the same comment says "could key on NOT RETIRED" under this rule — that is now the design, not
a hypothetical.

**WHAT IT DOES NOT TOUCH, stated because the boundary is easy to over-read.** `CLAUDE.md` §8's
"Code, checks, scripts, dead tables and views: delete them" stands unchanged. This ruling governs
DATA ROWS AND IDENTIFIERS, where deleting destroys provenance the project cannot reconstruct. Git
history genuinely is the archive for code, so a deleted script loses nothing; a deleted row loses
the fact that it existed. The two are different objects and §8's removal-friendly posture on
apparatus is not weakened.

**WHY IT WAS RULED, in the owner's own framing:** *"This is a recurring provenance and data
management issue."* The floors 076 built are repairs applied after a delete has already destroyed
identity. They accumulate, and they collide: batch 08 found the thirteen RETIRED tombstones being
read as live DOI claims by BOTH `research_batch_dod.py` R9a and `db.py add-source`, so the re-run
the 2026-09-13 clearing ruling ordered could not admit a single cleared source by any route — the
only remedy either offered was to cross-file a retired identifier, which is the one thing 076 exists
to prevent. Both were fixed the same day by exempting RETIRED rows; neither fix would have been
needed had the rows never left.

**AN EXECUTION CONDITION, NOT A RE-LITIGATION.** An adversarial pass on this proposal was already in
flight when the ruling landed. Its strongest line: the views (`v_best_practice` and the rest) may not
filter on status, in which case retire-in-place would keep untrusted rows on the READING SURFACE —
which would defeat the 2026-09-13 ruling's purpose rather than serve it. That does not reopen this
ruling; it is a condition of executing it correctly. **No row is retired in place until every reader
that could surface it filters on status**, and that sweep is rule 4's ("a VIEW IS a caller") applied
to this ruling.

CONDITION: Any session about to delete a data row, retract a source, clear a corpus, or design a
supersede path; and any migration that would empty a table.
ACTION: (1) Retire in place — set the status the table already carries — never hard-delete. (2)
Before the first retirement, sweep every reader that could surface a retired row and make it filter;
a view that does not is the defect. (3) Re-key `assess_cell`'s re-determination refusal on NOT
RETIRED rather than NOT EXISTS. (4) Where a row MUST genuinely leave (owner-ordered destruction,
fabricated data), that is an exception the owner rules on case by case, and it is recorded here.
DATE: 2026-09-16 — owner ruling, quoted above.

---



<!-- O21 references/project-standards.md:3590-3641 -->

## Owner statement 2026-09-16 — dose-response evidence may be reasoned to a range, AS A PROXY

> **"even if they aren't asserting a gradient, they are examining the impacts of gradients … this
> means that adjudication will be able to reason that whatever range of gradients corresponds to
> the best outcomes is the best range of gradient"**
>
> and, on being shown the limit of that inference:
>
> **"yes it's not perfect it's a proxy"**

**WHAT THIS SETTLES.** A source that measures the EFFECT of a parameter without prescribing a value
is not silent about that parameter, and judgment may reason from it toward a range. Batch 08 graded
four such sources and the engine returned `pending` with `refs=0`, which reads as "no evidence" over
two studies that measured articular discomfort rising 14→36% and pushrim force more than doubling.
That reading is wrong, and the mechanism is what makes it wrong: `assess_cell.gather_sources()`
gathers `figure_role IN ('claim','derived')` only, so a `finding` contributes nothing to a
determination however much it measured.

**WHAT IT DOES NOT SETTLE, and the limit is the owner's own word — PROXY.** The inference "best
outcomes therefore best range" has a degenerate solution on the evidence as it stands: both curves
are monotonic with no reported plateau, so "best" resolves to 0°, which is not a ramp. A ramp exists
to change level, so the design question is the MAXIMUM ACCEPTABLE gradient, and that needs a
threshold of acceptability which no admitted source supplies. Reasoning from dose-response to a
range is therefore a proxy step and must be marked as one, never recorded as though a source had
stated the value.

**THE PROJECT ALREADY HAS THE VOCABULARY FOR "PROXY" AND SHOULD USE IT HERE.**
`evidence_population_match.match_grade` carries PROXY for population-of-study vs population-served;
`source_value_extractions.value_directness` exists for how directly evidence bears on the claim and
sits at `NOT_ASSESSED` on every row because no grading rule has been ratified — which
`workplan/2026-09-10-road-to-batch-06.md` makes STOP CONDITION 4, "inventing one is a stop
condition". This statement is NOT read as ratifying a directness scale; it is read as ruling that
the proxy inference is ADMISSIBLE and must be MARKED. The scale itself is still owed.

**A LEAD THIS OPENS, recorded as a lead and not as a finding.** REF-00985 tested `0° to 4.8°`, and
`arctan(1/12) = 4.76°` — 1:12 being the ramp ceiling in ADA, AS 1428.1, BS 8300-1 and others. If
that ceiling is why 4.8° was chosen, the study measures discomfort across exactly the code-permitted
range and finds it climbing throughout, which under the 2026-09-13 ruling ("a finding that a CODE is
insufficient supplies no value, and is still first-class evidence") makes it a code-insufficiency
finding rather than a bare dose-response curve. THE ABSTRACT DOES NOT SAY THIS. It is an inference
from arithmetic and must be confirmed against the full text before it is filed as anything.

CONDITION: Any session determining a cell whose evidence measures effects rather than stating values;
any session implementing how `finding` rows reach a determination.
ACTION: (1) A determination may rest on dose-response findings, marked as a proxy, never as a stated
value. (2) `assess_cell` must be able to reach a determination from findings plus a threshold, not
only from `claim` rows — today it cannot, and that is why batch 08 reads `refs=0`. (3) The threshold
half is a code value or an equivalent criterion, and `research_code_leads` names which documents to
fetch but deliberately holds no values (2026-08-12 REFERENCE-ONLY ruling), so it must be retrieved.
(4) Do not invent a `value_directness` scale on the strength of this statement.
DATE: 2026-09-16 — owner statement, quoted above.



<!-- O22 references/project-standards.md:3642-3684 -->

## Owner ruling 2026-09-17 — PRESENT BOTH notations; never choose between ratio and percentage

> **"Present both--don't choose between ratio or percentage."**

**WHAT THIS ANSWERS.** The `DEC` gap raised the same day by the ACTION (2) engine work. A gradient is
written as a ratio (`1:12`, `1:20`) by some sources and as a percentage (`5 %`, `6 %`) by others, and
they are the same physical quantity in two notations. `parse_bound` returns `None` for a ratio by
explicit design, so `compose_value` was building the determination's interval out of the
percentage-stated rows alone — measured on parameter 3: **2 of 7 governing claims**, with five rows
dropped. Migration 086 made that visible in `value_note` instead of silent. The question it left open
was whether the engine may convert, and the answer is that the question was malformed: **the engine
does not pick a notation at all. It presents both.**

**WHAT IT SETTLES.**

1. **No notation is dropped.** A governing claim stated as a ratio contributes to the determination on
   the same footing as one stated as a percentage. The 2-of-7 composition was a defect, not a policy.
2. **No notation is privileged.** The determination does not select a "canonical" form and relegate the
   other to a note. Both are carried, and a render surface shows both.
3. **Conversion is for COMPARISON, not for replacement.** The engine must compare across notations to
   apply the most-accommodating rule at all, and `1:20 = 5 %` exactly. That comparison is arithmetic.
   What it must not do is overwrite what a source wrote with the other form.

**WHAT IT DOES NOT SETTLE, and the limit is arithmetic rather than doctrine.** Some conversions are
exact and some are not: `1:20` is exactly `5 %`, but `1:12` is `8.333…%` and no finite decimal is the
figure the source stated. So a derived notation is **marked as derived**, and where it does not
terminate it is marked as inexact as well. Presenting both does not license presenting a rounded
figure as though a source had written it — that is the 2026-08-19 shape, one column along.

**A CONSEQUENCE WORTH STATING.** Until this ruling the engine's protection against inventing figures
was to refuse cross-unit composition outright, which cost it five of seven rows on the first cell it
determined. The protection was real and the cost was invisible. Both halves of that stay true and the
remedy is not to relax the refusal but to stop treating two notations of one quantity as two units.

CONDITION: Any session composing a determination's value from governing claims stated in more than one
notation of the same quantity; any session extending `parse_bound` or `compose_value`.
ACTION: (1) Compose across notations, never within one. (2) Carry every notation the governing set
states, and mark any notation the engine derived rather than read. (3) Mark a derived notation that
does not terminate as inexact; never round it into the position of a stated figure. (4) This is a
ruling about NOTATION of one quantity, not about UNITS: millimetres and degrees remain different
units and the existing refusal to compose across them is untouched. [AMENDED for exact linear units (inches, feet, millimetres, metres) by "Owner rulings 2026-10-29 (second)" below, item 7.]
DATE: 2026-09-17 — owner ruling, quoted above.



<!-- O23 references/project-standards.md:3685-3730 -->

## Owner ruling 2026-09-18 — UK is canonical; BE, ES, HR, IT and INT admitted to the jurisdiction enum

> **"UK is canonical, add BE HR INT ES IT to the enum"**

**WHAT THIS ANSWERS.** `JurisdictionCode` declared 27 codes while the corpus held eight the enum
did not — so the declared vocabulary could not gate the column it described, and
`governance/jurisdiction-philosophy.md`'s ERROR-level "GB rejected, must be UK" rule had **no gate on
the database at all**: `validate_jurisdiction.py` globs source YAML and the standards registry and
never reads a table. It passed with 0 errors over **27 GB rows across five tables**, two of which
were written the same day.

**WHAT IT SETTLES.**

1. **UK, never GB**, confirmed. All 27 rows normalised;
   `scripts/audit/jurisdiction_db_vocabulary.py` now enforces it on the DATABASE, deriving its table
   list from the live schema and parsing the rejected spellings out of the philosophy document
   rather than carrying a copy.
2. **BE, ES, HR, IT, INT are admitted.** Each was already live in the CORPUS tables —
   `evidence_sources`, `source_value_extractions`, `search_executions`, `research_code_leads`. With
   them declared, every corpus jurisdiction value resolves, which is what makes the enum usable as a
   gate.
3. **INT is not ISO.** `ISO` means an ISO-published standard; `INT` means a work spanning
   jurisdictions without being one — REF-00994 (IPC Accessibility Guide), REF-00977 (a review
   searched across three databases). Both meta-codes, different meanings, recorded in the enum.

**WHAT IT DOES NOT SETTLE, and the boundary is deliberate.** Roughly twenty further ISO codes are
live in `lang_jur_map` — AR, AT, CL, CO, CR, CY, EC, ET, FI, GH, GT, MA, MX, PE, PH, PT, TH, TZ, UY.
That table is a language-to-jurisdiction reference map of places the project **may expand into**, the
"Phase 3 expansion" the validator warns about, not evidence it holds. They are **not** admitted here:
admitting a code silently converts a candidate jurisdiction into a declared one, and that is a scope
decision about the project's coverage rather than a vocabulary repair. The check exempts that table
and says why.

**TWO ANOMALIES SURFACED AND LEFT FOR A RULING**, in `term_aliases.jurisdiction`:
`TW` (Taiwan — a real jurisdiction, undeclared, outside the five ruled on) and `colloquial` on
TERM-027 *"place handicapé"* — **which is not a jurisdiction at all** but a register label written
into the jurisdiction column. Reported by the check, non-blocking, because `term_aliases` is base
vocabulary rather than admitted evidence and neither is this session's to decide.

CONDITION: Any session admitting a source whose jurisdiction is not already declared; any session
proposing an addition to `JurisdictionCode`.
ACTION: (1) Derive what is live before proposing a code, and name WHICH tables carry it — corpus or
reference. (2) Never write `GB`. (3) Do not admit a `lang_jur_map`-only code without a scope ruling.
(4) `TW` and `colloquial` are owed a decision.
DATE: 2026-09-18 — owner ruling, quoted above.



<!-- O24 references/project-standards.md:3731-3863 -->

## Owner ruling 2026-09-18 — EXECUTED IS `mined`; a deferral is legitimate so long as it eventually runs

> **"executed is 'mined'"**
>
> and, immediately after:
>
> **"deferred is okay so long as it runs eventually"**

Given in answer to batch 16's finding that `citation_mining.backward` and `.forward` are set to `1`
by `log_mining` **unconditionally**, including on a deferral, so the direction flags do not
distinguish a pass that ran from one that was logged. Recorded on contact per `CLAUDE.md` rule 0.

**WHAT IT SETTLES, AND IT NARROWS THE DEFECT RATHER THAN WIDENING IT.**

1. **The execution signal already exists and it is `evidence_sources.citation_mining_status`.**
   `mined` means the pass ran; `deferred` means it did not. The column is live, it is populated, and
   `log_mining` already derives it correctly (`deferred` with a reason, `mined` otherwise). Nothing
   new needs building to answer "did this source get mined".
2. **The direction columns are therefore not the home of that fact and must not be made one.**
   Batch 16's proposed remedy — split `backward`/`forward` into attempted-versus-executed pairs —
   is **refused by this ruling**: it would put one fact in a second home, which is rule 5, and the
   first home already answers it. `backward=1` says a backward pass was *logged*; the status says
   whether it *ran*. Read both.
3. **A deferral is not a defect.** Depth-1 is a hard constraint (`citation-miner` §6) and a batch
   that admits an anchor cannot mine it in the same pass. Deferring is the designed behaviour, and
   batch 16's three new deferrals are correct.

**WHAT REMAINS OWED, WHICH IS THE HALF THE RULING'S SECOND CLAUSE CREATES.** *"So long as it runs
eventually"* is an obligation, and **nothing in this repository enforces it or even measures it**.
There is no ageing on a deferred mining row, no backlog count, and no check that fails when a
deferral goes unhonoured. A deferral that is never discharged is indistinguishable from one taken
last week, and the register currently holds deferrals from batch 08 alongside batch 16's.

**AND ONE READING IS NOW WRONG RATHER THAN MERELY IMPRECISE.**
`citation_mining_completeness` counts **row presence**, so it reports deferrals as mined — measured
2026-09-18 at `10/10 T1-2 sources mined, 100.0%` repo-wide while the number of sources on
`accessible-circulation-geometry` whose backward pass had actually been executed was **3 of 13**.
Under this ruling that check is reading the wrong column: it must read `citation_mining_status`.
Derive both figures, never quote these:

**The snippet below derives BOTH quoted figures and nothing else.** The first version of it
derived neither — it printed a repo-wide tally across all tiers, so a reader told to re-derive
rather than trust got numbers that did not match the sentence above them. That is rule 7a's own
failure mode reappearing inside the remedy for it, and it is corrected here rather than excused.

```
python3 - <<'PY'
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
SLUG = 'accessible-circulation-geometry'

# FIGURE 1 -- what citation_mining_completeness reports: T1-2 sources with a mining ROW,
# over T1-2 sources in scope. It counts PRESENCE, which is the defect.
rows = con.execute("""
    select es.ref_id,
           (select count(*) from citation_mining c where c.global_ref_id = es.ref_id) has_row,
           es.citation_mining_status
    from evidence_sources es
    where es.tier in (1, 2)""").fetchall()
present = sum(1 for _, h, _ in rows if h)
print(f"as the check reports it : {present}/{len(rows)} T1-2 'mined' "
      f"= {100.0 * present / len(rows):.1f}%   <- PRESENCE, the overstatement")

# FIGURE 2 -- what actually ran on the slug: status='mined' is the execution signal.
slug_rows = con.execute("""
    select es.citation_mining_status
    from evidence_sources es
    join source_slug_links l on l.ref_id = es.ref_id
    where l.slug = ? and exists
          (select 1 from citation_mining c
            where c.global_ref_id = es.ref_id and c.slug = l.slug)""", (SLUG,)).fetchall()
executed = sum(1 for (st,) in slug_rows if st == 'mined')
print(f"as execution reports it : {executed} of {len(slug_rows)} on {SLUG}")

for st in ('mined', 'deferred', 'pending'):
    n = con.execute("select count(*) from evidence_sources "
                    "where citation_mining_status = ?", (st,)).fetchone()[0]
    print(f"  corpus-wide {st:<9}: {n}")
PY
```

CONDITION: Any session logging a mining pass, reading the mining register, or reporting mining
coverage; and any session about to propose a schema change to `citation_mining`.
ACTION: (1) `citation_mining_status` is the execution signal — read it, and do not build a second
home for it. (2) Do not split the direction columns. (3) `citation_mining_completeness` reads row
presence and must be changed to read status; until it is, treat its percentage as an overstatement
and say so wherever it is quoted. (4) The "runs eventually" obligation needs a measure — an age or
a backlog count on undischarged deferrals — and it does not exist yet. (5) A deferral is
legitimate; do not record one as a defect.
DATE: 2026-09-18 — owner ruling, quoted above.

---

RULE: A RETRACTION IS A CLAIM, AND IT IS HELD TO THE STANDARD OF THE CLAIM IT RETRACTS.
CONDITION: Whenever a session withdraws a result and offers a replacement — a corrected
  count, a re-ranking, a different instrument, a revised cause.
ACTION: Re-derive the *whole* comparison, not the part that was challenged, and name the
  instrument. Batch 17 retracted a mining yield as a screen artefact — correctly — and in
  the same paragraph asserted that the strict screen "inverts the original ranking",
  without re-deriving the anchor that founded the hypothesis. That anchor tops both
  screens. The retraction reached a gap, a session record, an attestation and a PR body
  before an adversarial pass caught it, which is the same distance the original error
  travelled. **Self-correction is not self-verifying.** A retraction published on an
  unvalidated instrument is a second claim of the same kind, and it inherits the
  credibility of the first — which is to say, none.
DATE: 2026-09-18 22:55

RULE: A YIELD IS DERIVED FROM A NAMED, VERSIONED SCREEN — NEVER FROM A REGEX TYPED INLINE.
CONDITION: Any count of "how many of these references are relevant", in a mining pass, a
  prediction, a gap, or a comparison between batches.
ACTION: Name a screen from `governance/mining-screens.yaml` and derive the figure:
  `python3 scripts/research/mining_screen.py --ref <REF-NNNNN> --compare`. Record the
  screen name and version beside any yield you keep. Adding a screen is cheap; editing one
  in place silently re-scores every yield ever recorded against its name, so add a new name
  instead. Rationale: two batches compared counts produced by two different ad-hoc regexes
  and neither said so, a pre-registered floor was scored on a screen it was not calibrated
  on, and the instrument was swapped after the results were seen. This is rule 7a applied
  to a measurement rather than a count — the number must be written as the command that
  computes it, and the command must name its instrument.
DATE: 2026-09-18 22:55

RULE: WHEN THE CLI CANNOT REACH A COLUMN, ADD THE VERB — DO NOT CLAIM THE WRITE HAPPENED.
CONDITION: A correction that requires writing a column no `db.py` subcommand exposes.
ACTION: CLAUDE.md §4 already says a table the CLI cannot reach is a coverage bug, not a
  licence to bypass. The failure mode this rule adds is the third option nobody names:
  **writing the claim without the write.** Batch 17 recorded in a committed, immutable
  migration that it had repointed two candidates off a zero-yield search. No verb could
  write `search_candidates.exec_id`, so it had not — and because the candidate-to-source
  edge lived in free-text notes, no check could contradict it. Add the verb, add the edge
  the check needs, add the check, then make the claim. `reattribute-candidate`,
  migration 088's `resolved_ref_id`, and integrity check S01 are that sequence.
DATE: 2026-09-18 22:55



<!-- O25 references/project-standards.md:3864-3924 -->

## Owner ruling 2026-09-18 — ERIC is a repository worth remembering

> **"ERIC is a valuable repository to remember"**

Given mid-batch, immediately after ERIC returned the full text of a source six batches of
DOI-keyed searching had never reached. Recorded on contact per `CLAUDE.md` rule 0.

**WHAT IT ANSWERS.** GAP-028's structural finding: *"EVERY SEARCH METHOD THIS PROJECT USES IS
DOI-KEYED OR INDEX-KEYED, so the foundation layer of its central parameter is structurally out of
reach."* That was true and it is now narrower. ERIC (the US Department of Education's Education
Resources Information Center) indexes government and institutional reports that carry **no DOI, no
PMID and no Crossref deposit**, and serves many of them as full-text PDF at a predictable URL:

    https://api.ies.ed.gov/eric/?search=<query>&format=json&rows=25     # record, gives ED number
    https://files.eric.ed.gov/fulltext/<ED-number>.pdf                  # full text, often present

**AND ONE ROUTE IN THIS ENVIRONMENT IS EXHAUSTED, NOT EMPTY.** `books.googleapis.com` returns
HTTP 429 — *"Quota exceeded for quota metric 'Queries' and limit 'Queries per day'"* — so a Google
Books query here is **not asked**, and its absence of results is not a null. Batch 18 recorded three
such 429s as *"Google Books 0"* before `author_fidelity` caught it. Treat a 429 as an unfired query.

Batch 18 used exactly that pair to retrieve HUD-PDR 397 (Steinfeld, Schroeder and Bishop 1979,
`ED184280`, 170 pp., 5.7 MB), persisted through `retrieval_log.fetch`. Derive what the corpus holds
rather than quoting this sentence:

    python3 -c "import sqlite3;con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);\
    print(list(con.execute(\"select engine,count(*) from search_executions group by 1 order by 2 desc\")))"

**WHAT IT DOES NOT SETTLE.** ERIC's scope is education and rehabilitation-adjacent research. It is
not a general grey-literature index, and a miss in ERIC is a miss in *that* index — an R14
query-shape-versus-wrong-index diagnosis still has to be made rather than assumed. Two sibling
routes went untried in batch 18 and are owed: **NTIS** for federal technical reports and **Jisc
Library Hub Discover** for UK institutional reports (which is where Walter 1971 would sit).

**AND ONE INSTRUMENT IS NOW KNOWN BAD FOR THIS PURPOSE.** `catalog.hathitrust.org` served a
Cloudflare *"Just a moment… Enable JavaScript and cookies to continue"* interstitial instead of
results, persisted in this session's retrieval log. **Nothing is established about what HathiTrust
holds**; read the artefact before scoring the retrieval.

> **CORRECTED 2026-09-19, WITHIN THE SAME SESSION, AND THE CORRECTION MATTERS MORE THAN THE
> ORIGINAL CLAIM.** The paragraph above first read *"returned HTTP 200 carrying a Cloudflare
> interstitial — a false 200, the same shape batch 17 found on JSTOR."* **The status was 403, not
> 200.** Derive it: `python3 -c "import json;[print(json.loads(l)['status'],json.loads(l)['url'])
> for l in open('retrieval-log/<session>/manifest.jsonl') if 'hathitrust' in l]"`.
>
> That is not a pedantic difference and it runs AGAINST me. A 403 is an honest refusal — the
> server says it is blocking. A 200 carrying an interstitial is a *deceptive* success, which is
> why batch 17's JSTOR finding was worth recording. **By misreading the status I upgraded a
> mundane block into the more alarming class, and reached for a precedent that did not apply.**
> The operative lesson survives and is smaller: read the body, not the status, in both
> directions. Found by `author_fidelity`, which prints every non-2xx in a session's manifest —
> a check that examines what a session actually retrieved rather than what it said it did.

CONDITION: Any session searching for a pre-1995 report, an institutional or government research
report, or any source that returned no DOI from Crossref.
ACTION: (1) Try ERIC before recording a zero-yield as genuine absence — a pre-1995 grey report
absent from PubMed and Crossref is an INDEXING fact until ERIC has been asked (R5's principle, one
index along). (2) Retrieve through `retrieval_log.fetch`, never `WebFetch`, so the payload is an
artefact (GAP-034). (3) Read the body before believing a 200.
DATE: 2026-09-18 — owner ruling, quoted above.



<!-- O26 references/project-standards.md:3925-3971 -->

## Owner ruling 2026-09-18 — 1979 work is HISTORICAL GROUNDING, not a current standard

> **"I don't think 1979 work is great for today standards but it's great for historical grounding"**

Given on contact when batch 18 surfaced Steinfeld, Schroeder and Bishop 1979 (HUD-PDR 397) and was
weighing its tier. Recorded per `CLAUDE.md` rule 0, and it **overrides the tier the ladder would
otherwise have produced on study design alone.**

**WHAT IT SETTLES, AND IT CUTS AGAINST THE ADMITTING SESSION'S OWN INCLINATION.** On
`governance/tier-system.md` §1 read mechanically, the study is a candidate for
`clinical`/`high_control` → **T1**: the parameter under design was experimentally manipulated (a
purpose-built 40-ft ramp reset from 1:12 to 1:16 to 1:20), the outcome was physiological (pulse
recovery to within ten beats of resting), and n = 124 disabled participants. That is the T1
definition on its face, and it is the reading this session was about to take.

**The ruling refuses it, and the refusal is about CURRENCY rather than about design quality.** A
determination is a statement about what to build **now**. A 1979 measurement was taken on 1979
wheelchairs, by people trained in 1979 rehabilitation practice, against 1979 expectations of what a
disabled person should have to tolerate — and the anchoring band (T1 / Co-1 / T2 / Co-2) is the band
the guidebook uses to say *this is best practice today*. Historical distance is not a defect in the
study; it is a mismatch between the study and the claim it would be made to anchor.

**HOW IT IS EXPRESSED IN THE SCHEMA.** `evidence_type='grey'`, `scope='intrinsic'` → **T3**, marker
**○**, which `tier-system.md` §1 glosses as *"Supporting evidence for best-practice claims; rarely
the sole basis"* — precisely "grounding, not standard". The study-design facts are not discarded:
they are recorded in `verification_note` and in the extractions, so a later session can see that a
high-control design was admitted at T3 **by ruling** and not by anyone mistaking its methods.

**WHAT IT DOES NOT SAY.** It does not retire the source, does not make its findings false, and does
not bar it from a determination's supporting set. It bars it from being the **anchor**. Nor is this
a general rule that old work is weak: it is a ruling about 1979 work being used to state a
present-day building parameter. Where the claim is itself historical — *what did the evidence say
when this code was written* — this source is **primary and first-class**, and that is the use batch
18 makes of it.

**AND IT LEAVES THE REAL BLOCKER EXACTLY WHERE IT WAS.** Parameter 3 × MOB stays undetermined,
determination gate 1 stays open, and C10 still refuses (GAP-020, GAP-024). This ruling means batch
18 did not move that, and the batch's own pre-registered prior P3 predicted it would not.

CONDITION: Any session admitting a source published before roughly 1990, or weighing an old but
methodologically strong study for an anchoring tier.
ACTION: (1) Age is a CURRENCY judgement, made separately from study design — do not let a strong
method carry an old source into the anchoring band. (2) Record the design facts anyway, so the T3 is
legible as a ruling rather than as a misreading. (3) Historical-provenance claims are a different
claim type, and old primary work anchors those at full strength.
DATE: 2026-09-18 — owner ruling, quoted above.



<!-- O27 references/project-standards.md:3972-4031 -->

## Owner rulings 2026-09-25 — the unreachable is given up for now; four points from batch 20's independent review

Given during research batch 20
(`sessions/session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa.md`, §8 and §0b).
Recorded on contact per `CLAUDE.md` rule 0. The first ruling is quoted. The other four were relayed
to the batch by the coordinating session, and are recorded here in that session's words rather than
as quotations.

> **"if we can't access something from anywhere then we have to give up on it for now"**

**(1) GIVE UP ON THE UNREACHABLE, FOR NOW.**
- An item to which no route exists from anywhere this project can reach is not queued for anyone.
  No interlibrary-loan, document-delivery or author-contact task is drafted for the owner.
- "For now" is a decision that can be revisited, not a finding about the item.
- Applied to REF-01002, Walter 1971 (candidate 109) and the 1957 Illinois dissertation (candidate
  110). GAP-016 is NOT-ADDRESSABLE and GAP-026 is CLOSED-DECIDED.

**(2) THE DISPOSITION IS TYPED.** "Exhausted, given up for now" gets a real, CHECK-permitted value:
`search_candidates.disposition = 'EXHAUSTED'`, added by schema migration 096.
- **It is not for an item behind a possibly transient barrier** (a bot check or a Cloudflare
  interstitial) that an ordinary browser gets past.
- Candidate 123 (Garg 2024, free to read at PMC) stays PENDING-VERIFICATION on exactly that
  distinction. That is the batch's judgment, made under this ruling.

**(3) A FACILITY AUDIT'S POPULATION GRADE DOES NOT TURN ON WHETHER ITS AUDITORS WERE DISABLED.**
- REF-01007 (Pinto 2021, a census of Brazilian primary-care facilities) is re-graded PROXY → PARTIAL,
  matching REF-01006. Whether an audit's participants were disabled is a Co-1 question, not a
  criterion of population-match directness.
- REF-01006's PARTIAL is the precedent applied, not reopened.
- **What it touches:** the harness research contract's one-line R13 summary
  (`governance/research-contract.yaml`: "Children/general-population/no-participants = PROXY") is
  what the PROXY grade followed. DR-2026-08-19's own R13 text does not name "no participants". This
  ruling supersedes the contract line as applied to a facility audit. **The contract's wording was
  not edited; whether it should change is the owner's call.**

**(4) THE VOCABULARY DOES NOT PRE-DECIDE AN OPEN SCOPE QUESTION.**
- TERM-089 (`ramp`) is narrowed to exclude the running slope of paths, walkways and trails. It no
  longer answers GAP-033's open ramp-versus-route question for it.
- **This covers TERM-089 only.** TERM-094's universalised scope note, TERM-093's foreclosure of a
  separate criterion term, and TERM-092's dangling reference are open on GAP-033.

**(5) NO PERSONAL EMAIL TO THIRD-PARTY APIs**, effective at once.
- The owner's address is not sent to Unpaywall or any similar service.
- Where an API tolerates it, omit the contact parameter. Where it requires one, stop and ask; never
  substitute a guess.
- The instances already committed in retrieval-log manifests stay as they are, because the history
  is not rewritten.

CONDITION: any session that meets an unreachable item, grades a facility audit's population match,
mints or edits a base term near an open scope question, or calls an API that asks for a contact
address.
ACTION:
1. Type an unreachable item EXHAUSTED; do not queue it, and do not draft a request for it.
2. Keep EXHAUSTED for no-route items only. A transient barrier stays PENDING-VERIFICATION with a note.
3. Grade population directness on who is served and what was measured, never on the auditors' own
   disability.
4. Leave an open scope question open in the vocabulary.
5. Send no personal email to any third-party API.
DATE: 2026-09-25 — owner rulings, as relayed above.



<!-- O28 references/project-standards.md:4032-4124 -->

## Owner rulings 2026-09-26 — `results_admitted` is raise-only after insert; a proxy provenance edge is repaired before merge

Given on PR #159 (research batch 20) and relayed by the coordinating session, so recorded here in
that session's words rather than as quotations. Recorded on contact per `CLAUDE.md` rule 0. Full
record: `sessions/session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa.md`, §0c–§0d.

**(1) `search_executions.results_admitted` IS RAISE-ONLY AFTER INSERT.**
- `log-search` sets the count from the search's own edges at insert.
- An admission edge added later to that search (`db.py link-admission`) raises the count to
  max(count, edges).
- Removing a wrong edge (`db.py unlink-admission`) lowers it by one, never below the edges that
  remain.
- **The count is never lowered to force agreement with the edges.**

The rule was first written by a session as a reconciliation of two records that disagreed. The
owner confirmed it as the answer, not a stopgap.

**What it supersedes, for post-insert writes:**
- `DR-2026-08-19` step 7's "the count must agree exactly".
- The 2026-09-02 repair's "nothing updates it thereafter" (the H05 note in
  `scripts/tests/test_db_integrity.py`, which now carries an appended pointer here).

**What it keeps:** that repair's lesson. H05 stays deleted, no parity check returns, and the
historical counts restored above their edges stay as they are. The rule's one home is
`_results_admitted_after` in `scripts/db.py`. GAP-051 is closed as decided.

**(2) A PROXY PROVENANCE EDGE IS REPAIRED, NOT MERGED.** Batch 20's two admission edges copied
candidate rows that batch 19 had filed on the nearest logged search, because the steps that
actually surfaced them were never logged. The ruling was to fix it before merge, on batch 17's
precedent (candidates 107/108):
1. log each real discovery step as a backfill search (`log-search --backfill 1`, a prior that
   states its own absence, and a `query_text` that says honestly what was done);
2. move the candidates with `reattribute-candidate`;
3. move the edges with `unlink-admission` and `link-admission`.

An ad hoc lookup is logged as what it was, not dressed as a designed query. GAP-050 records the
chain.

CONDITION: any session that writes, moves or audits an admission edge on a search that is
already logged, or finds a candidate filed on a search that did not surface it.
ACTION:
1. Never lower `results_admitted` to meet the edges; let the two verbs move it.
2. When a candidate's search is a proxy, backfill the real step and move the candidate and its
   edge. Never leave the proxy in place, and never re-describe the proxy search as the source.
DATE: 2026-09-26 — owner rulings, as relayed above.

CORRECTION — 2026-09-27. **Back-pointers for two rulings recorded retroactively; the ruling
entries themselves stand as written, per this ledger's append-not-edit practice.**

Built under `decisions/DR-2026-09-26-recurring-defect-shapes-remediation.md` §4 (RC3: "currency
lives at the superseded text"), owner nod 2026-09-27. §4.1 found that superseded text was
sometimes left with no local mark: a reader who reaches the superseded sentence by grep meets it
with nothing to say it no longer holds, and the fix is not an index but a pointer at the text
itself, anchored on quotes that occur exactly once at both ends. Relayed rulings are recorded
here per §4's OQ-4 answer (yes, with the relayed ruling quoted back).

**Seed 1.**
```
SUPERSEDES: decisions/DR-2026-08-19-research-restart-operative-instrument.md :: "the junction rows and the count must agree exactly"
  BY: references/project-standards.md :: "`search_executions.results_admitted` IS RAISE-ONLY AFTER INSERT."
```
The target sentence (DR-2026-08-19 §12.1 step 7) described `results_admitted` as bound to agree
exactly with the admission edges at every point after insert. The owner's 2026-09-26 ruling above
holds instead that the count is raise-only after insert: an admission edge added later
(`link-admission`) raises it to `max(count, edges)`, and removing one (`unlink-admission`) lowers
it by one, never below the edges that remain. The target still describes insert time correctly;
what no longer holds is "must agree exactly" as a standing invariant. A local callout, quoting the
BY text verbatim, has been appended at the target site (immediately after the superseded sentence,
before "Step 8").

**Seed 2.**
```
SUPERSEDES: scripts/tests/test_db_integrity.py :: "nothing updates it thereafter"
  BY: references/project-standards.md :: "`search_executions.results_admitted` IS RAISE-ONLY AFTER INSERT."
```
The same target as seed 1, in code. Batch 20 (2026-09-25) already appended a
"SUPERSEDED IN PART 2026-09-26 BY OWNER RULING" marker to the H05 comment there, naming this
ledger and GAP-051, but without the ruling's own words — a marker that names where to look is not
the same as one a reader can verify without leaving the file. The BY quote has now been appended
to that existing marker, verbatim.

**Why this entry and not an edit to the 2026-09-25 or 2026-09-26 entries above.** Both stand
exactly as written; they were true the day they were recorded, and adding a machine-checkable
back-pointer to what they superseded is new information, not a correction to what they say.

CONDITION: any session that changes what a `SUPERSEDES` line covers, or looks for why the two
target sites now carry a callout.
ACTION: (1) Treat the two target sites as superseded in part, per the callouts at each. (2) Do not
edit the 2026-09-25 or 2026-09-26 entries above to add these pointers retroactively — this entry
is where they live. (3) A `SUPERSEDES`/`BY` pair is verified by `supersession_backpointer_audit.py`
against the live text of both files, never by re-reading this entry.
DATE: 2026-09-27 — built per DR-2026-09-26 §4, owner nod on the DR as a whole.



<!-- O29 references/project-standards.md:4125-4182 -->

## Owner ruling 2026-09-27 — DR-2026-09-26 is RATIFIED

> **"Owner nod."**
>
> **"Build out all phases in their entirety using agonist-antagonist methodology with
> antagonist ensuring plan fidelity and adherence to code architecture and layer
> conformance. As required, use /code-review, /simplify, /layer-conformance and then a
> comprehensive adversarial critique that sweeps and propagates code implications then
> audits both top-down holistic and bottom-up granular requiring handshakes to resolve
> all issues."**
>
> Followed, same session: **"we do not have layer conformance skill; we just need a code
> architecture compliance"** — "layer conformance" is checked against CLAUDE.md's own
> Layer 0-4 model and seven-stage spine (section 3) directly, not a separate tool.

Given on PR #159 already merged, in the session that authored
`decisions/DR-2026-09-26-recurring-defect-shapes-remediation.md`'s successor build. Recorded on
contact per rule 0.

**WHAT THIS RATIFIES.** DR-2026-09-26 v2's status line moves from PROPOSED to **RATIFIED**. Its
§9 owner questions were not put to the owner one at a time; "build out all phases in their
entirety" is read as adopting each question's own **Recommended** answer, since the DR itself
frames OQ-1 through OQ-7 (OQ-2 withdrawn) as answerable that way ("yes/no against drafted text,
under an hour" is DR-2026-08-19's own precedent for exactly this kind of sitting). Recorded here
because rule 0 requires the supersession recorded, not re-litigated:

- **OQ-1** (same-model independence): require a different model where available; record and
  report where not. Not yet buildable as a refusal — reported only (DR section 1.4).
- **OQ-3** (accept RC6 latency, sign the §12.2 callout): yes. Callout appended, DR-2026-08-19 §12.2.
- **OQ-4** (relay/backfill SUPERSEDES lines): yes, relayed ruling quoted back in the PR, forward
  only plus the two specimen seeds. Built, RC3.
- **OQ-5** (retire the `decisions` table / YAML register, name the ledger the single home):
  recommended retire, **NOT executed** — no concrete migration plan exists in the DR for the two
  reader scripts (`scripts/doctrine_recheck.py`, `scripts/decision_capture.py`) that read the YAML
  register, and retiring a store without sweeping its readers is exactly rule 4's failure mode.
  Left open; this entry is itself evidence for OQ-5's premise, since it lands here rather than in
  that register.
- **OQ-6** (reword R13 / does a SUPERSEDED marker in injected text count as rewording): the
  marker does NOT count as rewording (the DR's own answer); seed 3 (R13) is **not shipped** pending
  the owner's explicit wording call. Seeds 1 and 2 shipped.
- **OQ-7** (can a non-planned discovery discharge a contract leg): R1 no, R2 yes — this is a design
  assumption baked into phase 2's writer refusals when built, not a standalone action.
- **OQ-8** (widen RC4's scope beyond the RULE's limb-(a) tables): recommended yes, **NOT built** —
  the DR's own v2 text states the mechanism as specified implements only the limb-(a) list, and no
  design exists yet for the wider scope (`connection_targets` has no session column). Left open.

**WHAT THIS DOES NOT DO.** It does not retire `data/decisions/decision_register.yaml` or the
`decisions` table (OQ-5 stays open). It does not widen `adversarial_pass_recorded`'s scope (OQ-8
stays open). It does not reword the research contract's R13 text (OQ-6's wording half stays the
owner's). Construction proceeds per DR-2026-09-26 §7's phase order.

CONDITION: any session reading DR-2026-09-26's status line, or asking whether OQ-1/3/4/5/6/7/8
were answered.
ACTION: (1) Treat the DR as RATIFIED, with the per-question dispositions above. (2) Do not
re-ask OQ-1, OQ-3, OQ-4, OQ-6 (seeds 1-2), or OQ-7 — they are answered. (3) OQ-5 and OQ-8 remain
open; do not build against either without a fresh owner answer or a concrete sweep plan.
DATE: 2026-09-27 — owner ruling, quoted above.



<!-- O30 references/project-standards.md:4183-4283 -->

## Owner ruling 2026-09-27 (second) — exec 77 executed per DR-2026-09-26 §5.2(d); further tooling on pass 1 stood down

Given in this session, after an independent read-only adjudication (Fable 5.1, dispatched with no
memory of the session that raised the question) tested whether continued work on the still-open
`adversarial_passes` pass_id=1 (subject commit `9443fdb`) was warranted, or was the meta-work
pattern `DR-2026-08-19` §2.1 names by name. Recorded on contact per rule 0.

> "Execute as ratified? Proceed all."

**(1) THE ADJUDICATION'S VERDICT STANDS.** Further tooling to force pass 1 closed is the
spurious-apparatus pattern: the 2026-08-19 RULE's own ACTION (5) forbids it outright ("a pass on
a pass is forbidden — defects in a pass are the next batch's pass's business"), and nothing
depends on pass 1 closing — `adversarial_pass_recorded` is advisory and does not even query
`adversarial_passes` when `EXAMINED`=0. Pass 1 stays OPEN. No `amend-adversarial-finding` verb is
built; the artefact-shape mismatch behind findings 9–12 (`.claude/agents/antagonist.md`'s prose
spec versus `close-adversarial-pass`'s literal single-file check) is named for the next tooling
PR, not built standalone.

**(2) EXEC 77 IS EXECUTED PER §5.2(d) AS RATIFIED.** The adjudication found the phase-2-data
migration (`9443fdb`) had not actually carried out `DR-2026-09-26` §5.2(d)'s own instruction —
exec 77's `origin` was left `planned` with `target_tier=1`/`target_evidence_type='clinical'`/
`target_scope='high_control'` still live, though §5.2(d) states plainly "exec 77 → incidental".
The prior session had declined to relabel it, because `amend-search`'s own writer refusal (added
beyond the DR's text, to protect `v_coverage_branch`'s Co-1 count) blocks `--set-origin` while any
of the three target columns is populated, and no setter could null them. Ruling: execute it.
`scripts/db.py`'s `amend_search` gained `--clear-target`, nulling all three columns together (the
refusal tests them as a group) and reading the effective post-clear state so
`--clear-target --set-origin incidental` succeeds in one call — a coverage gap fixed, not
bypassed, per CLAUDE.md's own "if you find one it cannot [reach], that is a coverage bug to fix,
not a licence to bypass." Exec 77 now carries `origin='incidental'`, `target_tier`/
`target_evidence_type`/`target_scope` NULL, and a `findings_note` trail recording both changes.
Finding 2 is disposed `OWNER-RULED` against this entry.

**(3) THE AUDIT'S BLIND SPOT IS LOGGED, NOT BUILT.** Finding 1 — `adversarial_pass_audit.py`
reports `EXAMINED: 0` over 41 real UPDATEs because `search_executions`/`search_candidates` carry
no `updated_by_session` column — is real (CLAUDE.md 5(a)'s named failure mode, inside the
mechanism ratified 2026-09-27 to end it) but is filed as **GAP-053**, not fixed now: the same
adjudication judged a standalone schema PR for it unwarranted, since nothing currently gates on
the check. The fix folds into phase 2b's tooling PR (DR-2026-09-26 §7) when that lands. Finding 1
is disposed `PROVISIONAL-DISPUTED`, pointing at GAP-053.

**(4) FINDING 7 DID NOT REPRODUCE.** 23 rows (not 24) carry a `|| RC1/RC5 phase 2-data` segment,
and each sits inside a correctly-formed `|| CORRECTED 2026-09-27:` marker — the bare `||` the
finding read as a missing marker is a nested separator, not a defect. No script or check greps for
the marker (`grep -rn CORRECTED scripts/audit governance` finds only `db.py` help-text). Disposed
`REJECTED`.

CONDITION: any session reading pass 1, exec 77's origin, GAP-053, or asking why pass 1 is still
open.
ACTION: (1) Treat exec 77 as `origin='incidental'`, executed, not merely proposed. (2) Do not
build `amend-adversarial-finding` or otherwise chase pass 1 closed as its own effort; it stays
open. (3) GAP-053 is the one record of the audit's blind spot until phase 2b; do not re-file it.
(4) `amend-search --clear-target` is now the sanctioned way to null a row's target columns before
an origin change — never hand-edit them.
DATE: 2026-09-27 — owner ruling, quoted above.

CORRECTION — 2026-09-28. **A back-pointer for GAP-053's fix, built during DR-2026-09-26 phase 2b;
the GAP-053 entry above stands as written, per this ledger's append-not-edit practice.**

`scripts/db.py`'s `reattribute_candidate` carried a comment reasoning that `search_candidates`
should never gain an `updated_at`/`updated_by_session` pair, because a reattribution's date and
author already live in the row's own `notes` narrative — adding the pair would be "a second home
for a fact the note already holds." That reasoning was sound for the purpose it addressed (a
human reader of `notes`) and is superseded here for a different purpose (a machine reader):
`adversarial_pass_audit.py` (RC4) scopes a session's subject rows by matching every column ending
`_by_session` on the 2026-08-19 RULE's named tables, and `search_candidates` carrying only
`created_by_session` made every UPDATE this writer issues invisible to that scope — GAP-053's
finding. Migration 100 (phase 2b) adds the pair; the writer now stamps it from the same
`audit(session)` call that writes the narrative note, so the two homes are written together and
cannot drift — not the shape rule 5 forbids, which is two independently-written homes of one fact.

```
SUPERSEDES: scripts/db.py :: "the column does not exist, and adding one to record a repair would be a second home for a fact the note already holds."
  BY: references/project-standards.md :: "The fix folds into phase 2b's tooling PR (DR-2026-09-26 §7) when that lands."
```

A second comment in the same file asserted the same fact for a sibling function, and is superseded
by the same ruling — reusing the BY quote, not asserting it twice (the audit's own convention: two
`SUPERSEDES` lines may cite one ruling, per DR-2026-09-26 §4.2(c)'s two seeds).

```
SUPERSEDES: scripts/db.py :: "search_candidates has no updated_* pair, so the dated, attributed line IS the audit record of the resolution (the literal RESOLVED is R15's predicate)."
  BY: references/project-standards.md :: "The fix folds into phase 2b's tooling PR (DR-2026-09-26 §7) when that lands."
```

A "SUPERSEDED IN PART" marker naming this entry and GAP-053, carrying the BY quote verbatim, has
been appended immediately after each target sentence in `scripts/db.py` — the original comments are
untouched, per the append-not-edit practice this trailer itself depends on.

CONDITION: any session reading `reattribute_candidate`'s original comment, or asking why
`search_candidates` carries `updated_at`/`updated_by_session` despite that comment's stated
objection.
ACTION: (1) Treat the objection as answered for GAP-053's specific (machine-reader) purpose, not
retracted in general — a future addition of a THIRD home for the same fact, for the same
human-narrative purpose the original comment addressed, is not licensed by this entry. (2) Do not
edit `reattribute_candidate`'s original comment; the marker beside it is where this is recorded at
the source. (3) A `SUPERSEDES`/`BY` pair is verified by `supersession_backpointer_audit.py` against
the live text of both files, never by re-reading this entry.
DATE: 2026-09-28 — built per DR-2026-09-26 §§1 and 6 (RC4/GAP-053 and RC6), during phase 2b
construction.



<!-- O31 references/project-standards.md:4284-4352 -->

## Owner ruling 2026-09-28 — jurisdiction scope: buckets 1–2 exhausted before reaching further, for any slug

**OD-2** (`decisions/DR-2026-08-19-research-restart-operative-instrument.md` §9) recorded a drafted
bucket fill order as "Ratify as drafted, noting the bucket 4/5 split is authored, not the owner's
words," but left it formally OPEN ("decisions OD-2 through OD-12 are still open; nothing gated
behind them is executed"). Batch 21 (2026-09-28) admitted Uganda — a jurisdiction in neither the
bucket scheme nor `governance/jurisdiction-philosophy.md`'s 24-canonical list — without consulting
either. The owner, live in the batch-22 orientation conversation, corrected this on contact (rule 0)
and gave a standing order:

> "Uganda ... is not a great country to hone in on." / "Please focus on the tiers 1 and 2
> countries" / "Uganda is not part of the 24 jurisdiction list" / "Standing order: do not research
> from countries other than Bucket 1 and Bucket 2 for any slug until those buckets are
> categorically exhausted."

**RULE: for every slug, research jurisdiction scope is Bucket 1 and Bucket 2 ONLY, until both are
categorically exhausted for that slug** (`workplan/2026-08-18-research-frame-proposal.md:420-424`,
membership below) — not merely for batch 22, and not merely for the ramp-gradient slug batch 21 and
22 work. "Categorically exhausted" means a search-coverage record (SEARCHED/THIN/NO-DATA, per the
per-jurisdiction tier-coverage convention `references/project-standards.md:121` already requires)
exists for every bucket-1 and bucket-2 jurisdiction against the slug's parameters, not merely that
some bucket-1/2 evidence has been found. Only once that is true for a slug may a session reach past
bucket 2 for that slug. This is narrower than OD-2's own draft (which scoped the buckets to a named
item set for scale-out) — this ruling applies the bucket-1/2 floor to every slug, and does not by
itself ratify buckets 4/5 or resolve the fill order beyond bucket 2.

**Bucket membership, derived from the one citation, never re-typed:**
`sed -n '420,424p' workplan/2026-08-18-research-frame-proposal.md` — at authoring time this reads
Bucket 1 = UN, ISO, Canada, USA, UK, Germany, Norway, Sweden, Japan, Australia; Bucket 2 = EU,
Singapore, New Zealand, Ireland, France, Spain, Portugal, Finland, Netherlands, South Korea.

**NOT RESOLVED BY THIS RULING**, named rather than silently carried forward: `workplan/2026-08-18-model-substitution-log.md`
records "buckets omit 7 of 8 Global South jurisdictions named by CANONICAL doctrine" as a conflict
raised and not resolved — Bangladesh, Egypt, Indonesia, India, Kenya, Nigeria, South Africa are all
in the 24-canonical list (`governance/jurisdiction-philosophy.md` §1.1) and in none of buckets 1–2.
This ruling does not touch that tension; it only fixes the floor (bucket 1–2 first, categorically,
per slug) that batch 21 violated. UN also names no member of `JurisdictionCode`
(`schemas/enums.py`) at all — distinct from Uganda's gap, UN is now IN the operative scope but has
no enum value; a session reaching UN-level evidence hits the same `jurisdiction_db_vocabulary`
class of block batch 21's PR #165 already carries as a waiver, and that is a tooling gap (rule 10:
fix in its own PR), not licence to admit UN-jurisdiction evidence under a different, wrong code.

CONDITION: any session selecting a jurisdiction to search for any slug, or asking why a
non-bucket-1/2 jurisdiction was reached.
ACTION: (1) Before searching outside bucket 1–2 for a slug, confirm and record a search-coverage
status for every bucket-1 and bucket-2 jurisdiction against that slug's parameters — do not infer
exhaustion from a partial pass. (2) Do not admit evidence from a jurisdiction outside buckets 1–2
for a slug that has not met that bar, batch 21's Uganda admissions being the named violation this
ruling corrects going forward (not retroactively — PR #165's existing rows are not unwound by this
ruling). (3) The Global South/canonical-24 tension is left open, not silently resolved by this
ruling's floor. (4) `UN` is in scope per this ruling but absent from `JurisdictionCode`; treat
admitting UN-sourced evidence as blocked on the same class of gap as Uganda's, not as licensed by
this ruling's wording.
DATE: 2026-09-28 — owner ruling, quoted above, given live during batch 22 orientation.

CORRECTION — same session, self-caught before any write was attempted against it. The ruling
above cites "the per-jurisdiction tier-coverage convention `references/project-standards.md:121`"
as the mechanism for recording exhaustion; `search_coverage` (the table that RULE describes) is
FROZEN (`db.py upsert-coverage` refuses on contact: "a hand-kept grid that drifted from the search
log in both directions; `workplan/search-coverage-completion-workplan.md` replaced it with the
search_executions log plus derived views"). **The live mechanism is `search_executions.jurisdiction`
plus `v_coverage_jurisdiction`/`v_coverage_language`** — a jurisdiction's status for a slug is read
off logged searches (including deferred ones, which are how a jurisdiction is marked deliberately
not searched), not written to a separate grid. ACTION (1) above is corrected to: confirm exhaustion
by querying `v_coverage_jurisdiction` (or the equivalent over `search_executions` directly) for
every bucket-1/2 jurisdiction against the slug, and closing any gap with `db.py log-search
--jurisdiction <code> ... --deferred-reason "..."` for a jurisdiction deliberately not searched, or
a real logged search otherwise. Nothing else in the ruling changes.



<!-- O32 references/project-standards.md:4353-4374 -->

## Owner ruling 2026-10-01 — the process-gap remediation plan's decisions D1–D4 approved

Given in session https://claude.ai/code/session_01MaToqCJbDoviNNLNkSpJPX, in reply to the
process-gap remediation plan for research batch 23 (PR #166), whose list of owner decisions named
D1 to D4. The plan is committed on PR #166's branch at
`scratchpad/session_2026-10-01-research-batch-23/process-gap-remediation-plan.md` and is not on main
until that PR merges; this entry is the record. Recorded on contact per rule 0.

> "approve all"

**D2**, the decision this entry exists to make findable: `JurisdictionCode` (`schemas/enums.py`)
admits `PT`, `FI` and `UN`, executing the owner ruling of 2026-09-28 above, and admits `UG` with
the comment "declared for PR #165's rows, which are not unwound; outside research scope by the
2026-09-28 ruling". D1, D3 and D4 concern PR #166's sequencing behind the tooling PR, the go-ahead
for the plan's branches, and agent edits to `.claude/settings.json`.

CONDITION: any session asking on whose authority `UG`, `PT`, `FI` or `UN` is a `JurisdictionCode`
member.
ACTION: (1) Read this entry as that authority. (2) Declaring `UG` licenses no research; the
2026-09-28 ruling, not the enum, sets research scope.
DATE: 2026-10-01 — owner approval, quoted above.



<!-- O33 references/project-standards.md:4375-4424 -->

## Owner statements 2026-10-09 — every source is scanned for every parameter; the parameter list is seeded from the existing terms; the catalogue plan, its critique and its tooling

Given in the session https://claude.ai/code/session_01DYqutJg8mWCGUQvqKzqAeM and recorded on contact per `CLAUDE.md` rule 0. Each statement is quoted verbatim beside what it answered; times are UTC. The questions are in `scratchpad/session_2026-10-09-research-batch-24-parameter-pilot/catalogue-plan-v2.md` section 2.5 and its addenda. The session record is `sessions/session_2026-10-09-research-batch-24-parameter-pilot.md`.

**The method**, stated unprompted (02:35):

> "note that while we search by slug, we scan each source for any and all applicable parameters. we may need to just prepopulate a parameters list."

and, when commissioning the critique of the catalogue plan and its rewrite (20:22), the whole message:

> "Perform Fable 5.1 read-only adversarial critique of the above. Interrogate quality, logic, sequencing and flexibility of pipeline all directions as well as all gates, reads, writes, conditionals. Ensure that all of our terms/parameters in catalogued will be leveraged in such a way where we can scrape information across any parameter if it appears in any source no matter the slug. Slugs guide our searches, but they do not guide what we derive and mine from sources! Our terms/parameter catalogue will, which means I expect harvesting across multiple terms if a source discusses multiple terms. Ensure that we can add and expand parameter catalogue as required based on new information we come across. Pass off to Opus to rewrite plan judiciously and exhaustively."

**Answers to the session's questions**, in order:

- "Is the existing `terms` registry acceptable as the seed for the parameter list?" — "1 yes" (03:08).
- "Does a `preliminary` or `skim` extraction ever govern a published cell?" — "2 ..yes? like, one pulled from another slug? should be yes, but we still tag it for follow up later" (03:08). This was ambiguous between a skimmed figure and a figure from another slug; D1 below resolved it.
- "WP12: confirm the R7 floor removal?" — "3 don't know what is" (03:08), then, after a plain-words restatement, "keep wp12 rule" (05:48). The R7 floor stays removed and R5 stays re-aimed at admitted sources.
- "populate a parameters table" (05:48), then, typed mid-turn, "we need like the 90+ cleaned parameters without values" (05:52).
- "A. The 94 existing terms. I would turn each object into its measurable quantity ... and propose the new names for your review. B. The 93 old guidebook items with the numbers stripped ..." — "A" (06:01). The session then found that parameter names may not be invented (the 2026-09-09 ruling above), so A could not be carried out as offered.
- "... why would you develop a parameter database for coverage of all accessible design terms possible by using batch 23 that came from a specific slug" (06:06). The session withdrew the batch 23 scan.
- "pull from the major codes, literature and advocacy from major countries" (queued 06:07:12, before the session's "1. slug by slug / 2. you seed it" options arrived at 06:07:27, so that choice was never answered) and, typed mid-turn, "there should be an exhaustive bibliography that is outdated but correct that has info on each jurisdiction code bodies and major groups".
- After the plan was rewritten: "D1: yes figure from source filed by another slug allowed. skimmed values are not publishable" (21:17), and then, later the same evening, "D2 yes, D3 keep the rule, D8 approve tooling".
- Immediately after, on D3: "D3 for parameter terms? it can be pulled from previous catalogues of entries for prepopulating". It qualifies "keep the rule" and is read in item 3 below.
- Asked which previous catalogues D3 meant, what guard applies to names taken from them, and whether a second branch may carry the first tooling pull request, the owner selected (from listed options, not typed): the catalogues **"Code and standards registries"** and **"Old corpus terms"** (the old Part 4 item names were offered and NOT selected); the guard **"Screen, then you approve"**; and **"Yes, second branch"**.

**What these establish**

1. **The scan contract.** Every admitted source is read against the whole parameter list, whatever slug it was filed under. Slugs plan and log searches; they do not decide what is taken from a source. One source can yield many parameters. Arguments and qualitative findings are mined as well as figures (the 2026-09-18 ruling in `sessions/session_2026-09-18-research-batch-15-t2-synthesis-threshold.md` is the root).
2. **The seed.** The parameter list is seeded from the existing terms registry. Parameters 4 to 12 (corridor width, turning circle, operating force, reverberation time, LRV contrast, door width, colour temperature, headroom clearance, ramp run length), added on this branch by commit `a8b7c11`, are kept, not reverted, and go to `main` through a pull request (D2).
3. **Names.** The 2026-09-09 rule stands for names that come out of research (D3, "keep the rule"): a name is minted only from a phrase an admitted source uses, through `db.py add-term --from-observation`, never by hand and never bearing a value. For prepopulating the parameter list the owner then permitted names "pulled from previous catalogues of entries", and selected which: the code and standards registries (`references/standards-registry.md`, `references/tier456-verified-sources.json`, `references/co1-verified-sources.json`, `references/co2-verified-sources.json`) and the terms of the pre-reset corpus (`_archived/data/corpus-pre-reset-2026-08-06.db`). The old Part 4 item names are not a permitted source. The guard is "Screen, then you approve": every candidate name is screened (no digit, comparator or min/max word, no old item code) and listed in one table, with the catalogue and the entry it came from, for the owner to approve before any is minted. Minting a name on this authority needs a route `insert_term` does not have. The session proposed that route as an addition to tooling T1 (`catalogue-plan-v2.md` Addenda 3 and 4); D8 predates it, so the owner's approval of T1 (item 5) does not cover its design, which goes to the owner on the T1 pull request. This narrows the "never by hand" clause for prepopulation only. The back-pointer grammar cannot mark the 2026-09-09 clause because it sits in this ledger (see item 6); this item is the mark.
4. **Cross-slug figures and skimmed figures (D1).** A figure taken from a source filed under another slug may be extracted and may set a published value, tagged for follow-up (the 03:08 words were not withdrawn). The owner's words are "skimmed values are not publishable". [ASSUMPTION: "skimmed" means a figure whose `extraction_method` is `skim`, and the determination engine is to leave such figures out of what sets a value. The owner named neither the column nor the engine rule; this reading is the session's, from `catalogue-plan-v2.md` Addendum 1, and stands until the owner confirms or corrects it.] Whether a figure read in full but still marked `preliminary` may set a value is NOT settled (D1c) and is not changed by this entry.
5. **Tooling.** D8 approved the first tooling pull request as `catalogue-plan-v2.md` section 4.2 items 1 to 5. It ships as its own pull request, on its own branch, and merges before this branch's pull request (`CLAUDE.md` rule 10); the second to merge takes `main`'s `data/guidebook.db` and re-runs `python3 scripts/migrate_db.py`. What T1 carries beyond those items (the catalogue minting route of item 3, and any change the session built to meet D1) was not shown to the owner before it was built, and is for the owner to accept or strike on the T1 pull request.
6. **The critique was commissioned by the owner.** The owner commissioned a read-only adversarial critique of the catalogue plan, saved verbatim in `scratchpad/session_2026-10-09-research-batch-24-parameter-pilot/catalogue-plan-critique-fable.md`. That supersedes, for that plan only, the 2026-08-19 clause that plans, critiques and handoffs are not adversarial-pass subjects. The back-pointer grammar below cannot mark that clause: it sits in this ledger, and the audit counts a target quote in the target file's raw text, where the SUPERSEDES line itself would make a second copy. This paragraph is the mark.
7. **The pilot's scope.** The batch 24 pilot in `process-gap-remediation-plan.md` section 7 is superseded in the places marked below. The pilot's scope, a judgement-stage re-read of batch 23's fourteen sources, is replaced by the scan contract above. Observation is no longer limited to phrases that carry a figure: arguments, qualitative findings and every quantity a source treats as a design quantity are observed. The pilot's budget of new parameters was exceeded on the owner's direction ("populate a parameters table", then D2 kept the nine promoted) and is superseded to that extent. **The pilot's cap on extractions (twice batch 23's) is not superseded:** no owner words address it. It budgets a pilot whose scope is replaced, so it has nothing to bind until a batch is run to the scan contract; whether any cap carries over, and whether the review unit is one source (`catalogue-plan-v2.md` section 1.1, F16, the session's own recommendation), is put to the owner.

```
SUPERSEDES: scratchpad/session_2026-10-01-research-batch-23/process-gap-remediation-plan.md :: "The pilot is a judgement-stage re-read of batch 23's 14 admitted sources."
  BY: references/project-standards.md :: "is replaced by the scan contract above"
SUPERSEDES: scratchpad/session_2026-10-01-research-batch-23/process-gap-remediation-plan.md :: "New parameters ≤ 4."
  BY: references/project-standards.md :: "is superseded to that extent"
SUPERSEDES: scratchpad/session_2026-10-01-research-batch-23/process-gap-remediation-plan.md :: "Do this for every concept phrase the source states a figure for"
  BY: references/project-standards.md :: "Observation is no longer limited to phrases that carry a figure"
```

**Not yet answered**, so nothing here approves them: D4 (exhaustion judged per parameter and jurisdiction), D5 (who reviews vocabulary in bulk), D6 (an item is one parameter), D7 (the category list), D9 (publish Release 0), D10 (read what is held before fetching), D11 (read out-of-bucket sources already held), D12 (this entry, which `CLAUDE.md` rule 0 requires regardless), D13 (the two finished batch 23 scans as test material), and whether the pilot's extraction cap carries over to the scan contract. The recommendations in `catalogue-plan-v2.md` section 10 stand unapproved. The batch 23 scan outputs are not data.

CONDITION: any session asking how a source is scanned, whether a figure from another slug may be used or a skimmed one published, on whose authority parameters 4 to 12 exist, whether a parameter name may be minted by hand, from an observed phrase, or from a registry or the pre-reset corpus, whether the pilot's scope or row budgets still bind, or whether a plan may be critiqued.
ACTION: (1) Scan every admitted source for every parameter in the catalogue; never limit a reading to the slug a source was filed under. (2) Take names from observed phrases; mint nothing by hand. For prepopulation the owner permits names from the code and standards registries and the pre-reset corpus terms (never the old Part 4 item names), screened and approved in one table before any is minted. (3) Treat a skimmed figure as not publishable; treat a cross-slug figure as allowed and tagged. (4) Build the first tooling pull request as its own pull request, on its own branch off `main`, before any bulk promotion. (5) Do not read the pilot's scope, its new-parameter budget or its figure-only step as binding. Its cap on extractions is NOT lifted: ask the owner whether it carries over to the scan contract, and treat the one-source review unit as a recommendation, not a ruling. (6) A critique of a plan needs the owner's fresh commission; this one covered the catalogue plan only.
DATE: 2026-10-09 — owner statements, quoted above.



<!-- O34 references/project-standards.md:4425-4444 -->

## Owner delegation 2026-10-14 — the simplification plan's §4 items are resolved by the assistant, including searches without a slug

Asked to design step 1.5a of `workplan/2026-10-12-simplification-workplan.md` and shown its §4 list of items waiting for the owner, the owner wrote (both absorbed mid-turn; `transcripts/harness_db856d85/main.jsonl:7802` and `:7814`):

> "design 15a for me so long as it makes sense with system"

> "§4, including the nullable-slug question.
>
> no idea what these are, but resolve them for me in a logical manner"

**What this does.** It hands every item in §4 of the plan to the assistant to resolve, on the premises already in the repository (LED-154 already delegates items presented to the owner to Fable 5.1). The resolutions, with their premises, inference and what would overturn each, are in `workplan/pipeline-state-graph/RULINGS.md` section (G); this entry does not copy them (point, do not copy). In short: the proposed rulings R1 to R42 are adopted as amended by the rehearsals; R12's language conjunct survives; the bytes pointer takes the favoured `retrievals` shape, to be rehearsed before it is built; `case_studies` and `economics_entries` are not folded; a full-read figure marked preliminary may set a value when tagged; a search may be recorded without a slug when it names a parameter or a mined source (R43); `PopulationCode` is retired (R44); the retired rule identifiers stay readable (R45); the frozen coverage verbs and the register text are deleted (R46, R47); the marker readings are fixed (R48); the five row-bearing drops of R3, the names of R14 (M4), the root key of R24 and the columns of R25 are confirmed (R49).

**What it does not do.** It executes nothing. Each step lands in its own pull request, which the owner reads before it merges; the destructive steps (1.4 and 1.5) drop only rows the entry states are reconstructible, or whose record survives in the git history of the blob. The owner can overturn any resolution by a later statement (rule 0).

**The one supersession this entry decides** (R24): the rule becomes that `source_value_extractions.root_id` references `external_root_registry` and nothing else; an in-corpus root is named by `root_ref_id`, which is how the two columns already divide. It replaces the sentence of `governance/evidence-architecture.md` (a) that let a `root_id` resolve to a `root_ref_id`. The `SUPERSEDES`/`BY` pair is **not** written here: `supersession_backpointer_audit` requires the target document to carry the pointer in the same change, so the pair, the amended sentence and the update of atom EVI-162 arrive together in the pull request that builds the key (plan step 3 judgment).

CONDITION: any session asking whether the plan's §4 items are still waiting for the owner, whether a row-bearing table may be dropped, whether a search may be recorded without a slug, what names the identity registry takes, whether `root_id` may name an in-corpus source, or whether the simplification plan may be executed.
ACTION: (1) Treat the §4 items as resolved by `RULINGS.md` section (G); do not ask the owner to re-answer them. (2) Execute the plan one step per pull request, opened last, and put each owner-merge edit in the diff of its own step. (3) Do not drop a row-bearing table except in steps 1.4 and 1.5, after `--rebuild` shows the rows are reproduced or the entry's record of survival applies. (4) The nullable-slug resolution (R43) is rehearsed before it is built. (5) The owner's override of any resolution is a later statement and wins.
DATE: 2026-10-14 — owner statements, quoted above.



<!-- O35 references/project-standards.md:4445-4458 -->

## Recording 2026-10-14 — the root registry: a `root_id` references the registry and nothing else

**What this does.** The delegation entry of 2026-10-14 decided one supersession (RULINGS R24) and left its back-pointer to the pull request that builds the key, because `supersession_backpointer_audit` requires the target document to carry the mark in the same change. That change is migration 114: `source_value_extractions.root_id` now carries a foreign key to `external_root_registry`. This entry writes the pair and nothing else. It makes no ruling.

```
SUPERSEDES: governance/evidence-architecture.md :: "a `root_id` must resolve either to a `root_ref_id` in `evidence_sources` or to a registered external-root stub"
  BY: references/project-standards.md :: "the rule becomes that `source_value_extractions.root_id` references `external_root_registry` and nothing else"
```

The sentence is overtaken in its first alternative only: an in-corpus root is named by `root_ref_id`, never by `root_id`, which is how the two columns already divided. The mark in the target says so.

CONDITION: any session asking what a `root_id` may name, or reading the "Root registry" discipline in `governance/evidence-architecture.md`.
DATE: 2026-10-14 — recorded under RULINGS R24; the superseding words are the delegation entry's, quoted at the ledger line the mark names.



<!-- O36 references/project-standards.md:4459-4467 -->

## Recording 2026-10-20 — the identity registry and its ICF map take their lens names

**What this does.** The delegation entry of 2026-10-14 listed "what names the identity registry takes" among the items the assistant resolves, and `RULINGS.md` R49(c) confirmed the names `base_taxonomy_identity`, `identity_icf_map` and the column `identity_code` for LED-127 (M4 only). Migration 115 applies them: `populations` becomes `base_taxonomy_identity`, `population_icf_links` becomes `identity_icf_map`, and `population_code` becomes `identity_code` in both. This entry makes no ruling. It records that the sentence "Confirmation pending — the rename is not applied" in the LED-127 entry (the ruling of 2026-08-28 above) is no longer true of the database, and that the confirmation is the one R49(c) records under the delegation. No `SUPERSEDES` pair is written: the sentence it would mark sits in this ledger, and `supersession_backpointer_audit` counts a target quote in the target file's raw text, where the pair itself would make a second copy (the 2026-10-09 entry, item 6, gives the same reason).

**Not done, and still the owner's.** `evidence_population_match` and its `target_population` and `study_population` columns keep their names. LED-127 names them `served_group` and `study_group` and keeps them out of the lens vocabulary; `RULINGS.md` R14 as first worded would have named the table `evidence_identity_match`. The register step LED-127 orders is executed for `population_icf_links` only (`governance/retired-vocabulary.yaml` RV-027); `populations` is an English word and fails that file's admission test 4, and `population_code` is held back for the flood that file's deferred entry records.

CONDITION: any session asking whether the identity registry has been renamed, what its key column is called, or whether LED-127's confirmation is still pending.
DATE: 2026-10-20 — recorded under RULINGS R14 and R49(c); the authority is the 2026-10-14 delegation entry above.



<!-- O37 references/project-standards.md:4468-4490 -->

## Owner statements 2026-10-21 — which findings count, who may confirm, and what a marker needs

Given in session https://claude.ai/code/session_019DBbAfKYEE5x5qvYnBRp3W, in reply to four questions put with the review of the determination's marker (migration 116, PR #200), and recorded on contact per `CLAUDE.md` rule 0. Each answer is quoted verbatim beside the question it answered.

1. Do skimmed or `absent` findings supply direction for a proxy determination? — "no. skimmed findings cue tools for a dedicated pass."
2. Can an `absent` finding confirm a code's value? — "no"
3. Does an unverified source cap the marker? — "must be verified"
4. Is one confirmed clause enough to confirm a whole code? — "no"

**How the engine reads them** (`scripts/assess/assess_cell.py`; the readings of 3 and 4 are the assistant's, marked, and stand until the owner corrects them).

- **1 and 2.** A finding row counts for direction (`gather_findings`) only if it is not skimmed and not `claim_type='absent'`, and for confirmation (`_confirmed_bands`, from `gather_confirmers`) only if it is not skimmed (the later entry below lets an `absent` row confirm). A skimmed finding is left out and *reported* (`skimmed_findings` in the report and on the summary line, naming `db.py record-scan --mode targeted`), which is the cue to a dedicated reading. This narrows the 2026-09-16 ruling that findings supply direction; it does not overturn it. [ASSUMPTION: "cue tools" means the engine's report names the tool for the owed pass; no row is written.]
- **3.** A source that is not `VERIFIED` takes the weak band for the marker, so a full marker needs every governing source verified; an unverified source still anchors a determination (D-0157). [ASSUMPTION: the owner's words say verification is required, not whether a lone unverified source caps the whole cell. The reading applied is the floor of the mean over bands with the unverified source at weak; the alternative, capping the cell at weak, is not applied.]
- **4.** A code takes its confirming study's band only if every one of its governing extraction rows is confirmed; otherwise it is weak. [ASSUMPTION: "no" means unconfirmed clauses keep the code unconfirmed.]

**Still unruled.** The function from sources to a cell's marker: the floor of the mean is the owner's for a derived figure's inputs (2026-09-13), and its use for a determination's governing sources is `RULINGS.md` R7 as amended by R49(a), not put to the owner at this level.

**Effect on the live corpus, measured on a scratch copy.** Parameter 3's proxy determination keeps its marker, but a skimmed or `absent` finding row no longer supplies direction, so its direction sources shrink and its `tier_basis` can lose "T1". Re-derive, never quote: copy the database to a scratch path and run `GUIDEBOOK_DB_PATH=<scratch> python3 scripts/assess/assess_cell.py --db <scratch> --emit-sql <out.sql> --parameter-id 3 --slug <slug> --identity MOB --session <session> --stamp <timestamp>`. The report lists the skimmed findings left out, by extraction id and source.

CONDITION: any session asking whether a skimmed or `absent` finding may supply direction or confirm a value, whether an unverified source may carry a full marker, or whether one confirmed clause confirms a code.
ACTION: (1) Count a finding only if it is neither skimmed nor `absent`; report a skimmed one as owing a dedicated reading. [AMENDED for confirmation by "Owner clarification 2026-10-21" below: an `absent` finding may confirm.] (2) Give a source that is not verified the weak band. (3) Confirm a code only when every one of its governing rows is confirmed. (4) Do not treat the readings marked ASSUMPTION as ruled.
DATE: 2026-10-21 — owner statements, quoted above.



<!-- O38 references/project-standards.md:4517-4535 -->

## Owner clarification 2026-10-21 — an absence found at the tested value confirms it

Given in session https://claude.ai/code/session_019DBbAfKYEE5x5qvYnBRp3W, in reply to the question put in plain words after the second correction, "which did you mean, A or B?" (A: the sentence "changes to the technical requirements for ramp slope and length cannot be recommended at this time" means the existing requirement held up under testing, so the study backs the code's value; B: it only says the study found no grounds to change it). Recorded on contact per `CLAUDE.md` rule 0.

> "Reading A... but the issue is that there ARE values, which are the existing ones that were tested. The "absence" of the findings is actually research support for that tested code value, so it's actually a supplemental document that supports those code values"

**What this settles.** The 2026-09-13 ruling stands: REF-00980 is a clear case of confirmation. The owner's earlier "no" to "can an `absent` finding confirm a code's value" (entry above) is read as being about a finding that says nothing about any value; an absence found *at a tested value* is support for it. This replaces the item 1 of the first correction ("until the owner says otherwise the engine counts no `absent` row"): the owner has said otherwise.

**How the engine reads it** (`_confirmed_bands` in `scripts/assess/assess_cell.py`). A `confirms` edge from an `absent` finding row confirms the code row it points at, because the edge is itself the claim and needs a row referent and a quote; an absence that examined nothing carries no such edge. A skimmed row still confirms nothing. An `absent` row still supplies no direction (a source that looked and found nothing does not say which end of a permitted range the evidence favours). [ASSUMPTION: the clarification speaks to confirmation; the direction rule of answer 1 is left as given.]

**What remains before the REF-00980 case counts, all research data and so a separate change (`CLAUDE.md` rule 10), none done here.**
1. The paper is held only as an abstract (extraction 48 is `skim`, `preliminary`); the dedicated reading that answer 1 calls for is owed.
2. Its `confirms` edge (`relation_id` 29) points at a label, "the technical requirements for ramp slope and length", not at a code row; it must be repointed (`db.py repoint-extraction-relation`) at the extraction of the requirement the study tested, which the reading will identify. An edge to a label confirms nothing.
3. Only the code rows the study tested are confirmed by it; other jurisdictions' values are not.

CONDITION: any session asking whether REF-00980 or any `absent` finding may confirm a code's value.
ACTION: (1) Let an `absent` finding confirm through an explicit `confirms` edge to a code row, once it is read in full. (2) Do not let it supply direction. (3) Do the three data steps above in a research change, not in a tooling change.
DATE: 2026-10-21 — owner statement, quoted above.



<!-- O39 references/project-standards.md:4536-4551 -->

## Owner statements 2026-10-21 (third) — an unretrievable source cannot be top tier; the edition label becomes pilot-4

Given in session https://claude.ai/code/session_019DBbAfKYEE5x5qvYnBRp3W, in reply to two questions put in plain words (should an answer resting on an unverified source read ○, or keep its band and be flagged; should the rule-edition label change), and recorded on contact per `CLAUDE.md` rule 0.

> "if we can't retrieve a study, then we can't verify it as a primary source, which means that we can't claim it as a top tier. add unverified in this context where something can't be retrieved to the empty circle alongside grey or thin"

> "pilot 4 I guess"

**1. The empty circle.** ○ now stands for grey, thin **or unverified because the source could not be retrieved**. This answers the "Owner to rule" in the second correction above: such a cell reads ○; it is not left at its band and flagged. It is stated in `governance/tier-system.md` sections 5 and 8, `governance/mission-and-epistemics.md` (the citation-discipline marker line, with atom MIS-03 re-quoted), `CLAUDE.md` section 6, and the `EvidenceMarker` and `band` docstrings [AMENDED by "Correction 2026-10-22" below, item 4: the `band` docstring was not changed]. The engine already did this: an unverified source is left out of the marker and a cell with no verified governing source is weak (`_verified` in `scripts/assess/assess_cell.py`). The blocking check C10 in `scripts/tests/test_db_integrity.py` already refuses a published (live stated or provisional) cell whose governing sources are not all verified, so such a cell cannot stand as an answer; ○ is how it reads, and why it is refused, before it is retired. The 2026-09-13 reading of ○ as "no research backing" is thereby widened to include "not retrieved": a hedge on the *source*, not a finding about the *evidence*.

**2. `RULE_VERSION` is `pilot-4`.** This answers the "Owner to decide" in the first correction above and replaces its item 4. The label marks rows written by an engine that writes a marker and applies the rules of the entries above; rows labelled `pilot-3` were written without one. The `derivation_sha` payload is unchanged from pilot-3, so K01 and K02 read both labels (checked on a scratch database holding a fresh pilot-4 row: both examined it and passed, where on the canonical database they examine nothing because no determination is live).

CONDITION: any session asking what ○ means, whether an unretrievable source may be called top tier, or what `rule_version` pilot-4 is.
ACTION: (1) Read ○ as grey, thin or unverified-because-not-retrieved. (2) Never claim a top tier for a source that could not be retrieved. (3) Write `pilot-4` on new determinations and let K01 and K02 read pilot-3 and pilot-4. [AMENDED by "Correction 2026-10-22" below, item 7: they read every version but the closed legacy set.]
DATE: 2026-10-21 — owner statements, quoted above.



<!-- O40 references/project-standards.md:4552-4575 -->

## Correction 2026-10-22 — to the entries above, found by two review passes after the third statement

Append-only, except that each superseded ACTION line above now carries a one-line mark pointing here. A `SUPERSEDES`/`BY` pair cannot be written, because the ledger is both source and target and the pair would hold the quote a second time (the reason the 2026-10-20 entry gives).

1. **Confirmation was read off the direction set, so the clarification was half built.** The clarification says an `absent` finding confirms through its `confirms` edge. `_confirmed_bands` took the confirming source's band from the sources that supply direction, and those leave out an `absent` row, so an absent-only source confirmed nothing whatever edges it carried. The engine now reads the confirming sources on their own (`gather_confirmers`), assesses them through the same gates and takes a band only from a verified one. Checked on a fixture: three T6 codes, one counted finding supplying direction and a separate absent-only study with edges to all three codes read ● (they read ○ before).

2. **Not built, and the owner's to rule: a floor claim a study confirms.** Where a study's rows are all `absent` (REF-00980 is that shape on its parameter) no finding supplies direction, so the cell is not a proxy determination. It is a regulatory-stratum-only floor claim, which migration 116's CHECK holds at ○, and a confirmation does not lift it. The 2026-09-13 ruling says a code value a study confirms is upgraded and `RULINGS.md` R39 says direction-only confirmation stays on the proxy route; neither says what determination such a cell is (it is not `regulatory_stratum_only`, and it is not a proxy). So the list in the clarification of what remains before REF-00980 counts has a fourth item: this ruling. **Owner to rule.**

3. **What `db.py` guards, corrected, and what notices the rest.** The unguarded routes listed in the first and second corrections no longer stand as listed. For a live determination `db.py` now refuses: a change by `amend-source` to any column the engine reads of a source (`dbcore.ENGINE_SOURCE_COLUMNS`, which `assess_cell` builds its SELECT from), whichever of the three junctions the determination reaches the source by (governing links, convergence, extraction links); the supersession of such a source; a change by `amend-extraction` to a column the engine reads of a row (`dbcore.ENGINE_EXTRACTION_COLUMNS`; of those `figure_role`, `comparator` and `extraction_method` are amendable); and a `confirms` edge to a governing row of a live proxy determination. Not refused, by design: a finding row added to the parameter after the answer (research goes on, and K02 reports it), a data migration, and the verification cron. Those, and any route nobody has thought of, are noticed afterwards by `assess_cell.stale_determinations`, which `derivation_handshake_integrity` runs: it re-runs the engine on each live determination of the current `RULE_VERSION` and compares the stored answer. Like K01 and K02 it examines nothing while no determination is live; `scripts/tests/test_assess_cell_pilot.py` exercises it on a fixture. Re-derive the columns the engine reads: `python3 -c "import sys; sys.path.insert(0, 'scripts'); import dbcore; print(dbcore.ENGINE_SOURCE_COLUMNS, dbcore.ENGINE_EXTRACTION_COLUMNS)"`.

4. **A claim in the third statement withdrawn.** That entry says the `EvidenceMarker` and `band` docstrings state the widened ○. `band` in `schemas/tier_derivation.py` grades by (tier, evidence_type) alone and was not changed; the rule that an unverified source earns no band is the engine's (`_verified`). Only the comment on `EvidenceMarker.WEAK` states it. The prose that restated ○ and had not moved is now swept: `governance/tier-system.md` section 8 (an unretrievable source keeps its tier and may still anchor, earns no band above ○, and is flagged unverified in place of the regulation/practice flag), `skills/evidence-auditor_SKILL.md`, `references/methodology-evidence-hierarchy-mapping.md` section 7.1, and the atoms CLM-038, EVI-047, EVI-055 and EVI-056. [ASSUMPTION: the owner's words put the unretrievable source in the empty circle; that it keeps its tier and may still anchor is the engine's behaviour since D-0157 and was not put to the owner.] `governance/grounds.md` says ○ "includes" values that codes agree on and nobody has tested; that is not exhaustive, and it is unchanged.

5. **Migration 116's header was edited after it merged** (`CLAUDE.md` rule 3). It is restored to the merged text and its corrections live here. Its sentence "the eight written before this file are all retired" was a count at the time. The ALTER fails if a live stated or provisional row exists; re-derive with `select count(*) from specifications where retired_at is null and state in ('stated', 'provisional')` (pending and not_applicable rows carry no marker and are allowed). The column's reader, which rule 8 asks to be named: render step 3.R (plan Phase 3, not built) shows it beside `has_unverified_sources`; until then only the two CHECKs, C10 and `stale_determinations` read it.

6. **Unverified inputs are flagged whether or not they anchor.** `has_unverified_sources` was set for value sources and for unverified direction anchors. An unverified Co-1 finding source is no anchor (`classify` holds it back), so it supplied no direction and raised no flag, and the cell read as a plain floor claim. The flag now covers every live finding and confirming source of an answer that rests on the regulatory stratum.

7. **K01 and K02 named the open set.** They listed the versions written under the link-set format (`pilot-3`, `pilot-4`), which the next bump would have left behind: K02 would then have examined nothing and K01 would have read new rows as legacy. They now name the closed legacy set (`pilot-2`), which is history and cannot grow.

8. **Counts removed.** The "Effect on the live corpus" paragraph of the first entry quoted counts and a command ending in "..."; it now carries the command (`CLAUDE.md` rule 7a).

CONDITION: any session asking what `db.py` guards for a live determination, whether an `absent` finding confirms when no other finding exists, which versions K01 and K02 read, or what notices a stale marker.
ACTION: (1) Treat the routes in item 3 as guarded or detected; its list replaces the lists in the first and second corrections. (2) Let an `absent` finding confirm through its edge on a proxy determination, and put item 2 to the owner before building the confirmed floor claim. (3) Read ○ per `tier-system.md` sections 5 and 8 as amended in item 4, and never claim a top band for an unretrieved source. (4) Treat the marks on the earlier ACTION lines as binding.
DATE: 2026-10-22 — recorded under the entries above; the owner's words are quoted there.



<!-- O41 references/project-standards.md:4576-4591 -->

## Owner statement 2026-10-28 — an interface to review and edit the tables, and the code it may add

Given in session https://claude.ai/code/session_01Ub36iQ3vbthbsh45LNks6j, after the orientation report of the same day, and recorded on contact per `CLAUDE.md` rule 0. The first statement is quoted from the owner's message; the second is the owner's answer to a question put with the plan.

> "I need there to be some kind of interface where I can manually review and edit the different table values/information and have it propagate accordingly. At the moment, everything in the database is opaque to me."

The question (code budget): the page needs roughly 400 to 550 new lines under `scripts/` against the standing constraint of as little code as possible (2026-10-12; restated 2026-10-23 in `workplan/2026-10-23-pipeline-resolution-workplan.md` section 1, where it is not yet in this ledger), and no deletion offsets it today. The owner's answer: "Name the exception".

**What this does.** It records a need that no plan held: the workplan has no item for a viewer or editor, and the nearest text is H-0's line in `.claude/commands/orient.md` and the question register's E12 / D5 (who reviews vocabulary in bulk), both unanswered. The plan that answers it is `scratchpad/session_2026-10-28-owner-review-interface-plan/interface-plan.md`; this entry points to it and does not restate it. No ratified text is overtaken by a pair here. Three interactions are named so a later session does not rediscover them: (1) workplan T-5 and the report's K-13 hold that a rendered page is not committed, and the interface follows that (the page is generated to `$TMPDIR` and published privately, never committed); (2) H-0 specifies the owner queue as four lines of text in `orient.md` with "no apparatus", which the page's first screen widens, so one of the two holds the queries and the other points to it; (3) `CLAUDE.md` section 8 asks a PR that raises the line total of `scripts/`, `schemas/`, `.github/` or `skills/` to name the exception, and the answer above is the owner's instruction to do that for this work.

**Readings applied, marked.** [ASSUMPTION: "edit" means a proposal that reaches the database only through the sanctioned path (scratch copy, `db.py` verb, `emit_batch_sql.py`, `emit_data_migration.py`, `migrate_db.py`), because `CLAUDE.md` rule 3 forbids a direct write; an edit made on the page changes an in-browser copy and a change set, and the assistant applies the change set through the verbs, previews it, and ships it in its own data pull request (rule 10).] [ASSUMPTION: "propagate" means two things the schema already separates: the views recompute on every read, and a determination is recomputed only by an engine re-run, which `db.py` guards for a live determination and `assess_cell.stale_determinations` detects afterwards.] If the owner meant an edit that writes immediately from the page, that is a ruling against rule 3 and is the owner's to make; this entry does not make it.

CONDITION: any session asking whether the owner has asked for an interface to review or edit the tables, whether that interface may write to the database, whether a page it generates may be committed, or whether its code needs an offset.
ACTION: (1) Build the interface as the plan in the pointed file orders it: a read-only browser and the owner's queue first, then edits as proposals. (2) Let no page write the database; apply every change through the verbs and ship it in a data pull request apart from the tooling. (3) State in each tooling pull request "no offset, N lines added" and cite this entry. (4) Do not read the answer "Name the exception" as a ruling on any other pull request's line count.
DATE: 2026-10-28 — owner statements, quoted above.



<!-- O42 references/project-standards.md:4592-4607 -->

## Owner statement 2026-10-28 (second) — decisions waiting on the owner are prompts with full context, on a phone

Given in session https://claude.ai/code/session_01Ub36iQ3vbthbsh45LNks6j, in reply to the first version of the owner's browser page, and recorded on contact per `CLAUDE.md` rule 0. Both statements are quoted from the owner's messages.

> "I'm on mobile tho"

> "waiting on me decisions need to be prompts with full context"

**What this does.** It fixes two requirements of the page recorded in "Owner statement 2026-10-28" above. First, the owner reads and answers on a phone (the stored user agent of the engine test is an Android WebView), so the page is designed for a phone screen, not adapted to one. Second, each item that waits on the owner is a prompt: a question, why it is the owner's, the full context in plain words, the options with what each one does, and a recommendation only where a source states one. The 31 decisions of the resolution report's decision sheet and the workplan's section 4 (OR-1 to OR-25 with their sub-parts, OW-1 and OW-2) are written that way in `governance/owner-browser.yaml`, each naming its source; the seven lists of database rows are shown as prompts with the whole row. An answer given on the page is saved in the page's own store; it is not a ruling until an entry in this ledger quotes it in the owner's words, as the 2026-10-28 entry above already provides.

**Readings applied, marked.** [ASSUMPTION: "decisions waiting on me" means those 31 decisions and the database rows the seven lists name; the membership of the lists is the assistant's judgment and the owner is asked to confirm it.] [ASSUMPTION: the plain-language context of each prompt is the assistant's rewriting of the sources it names and may misstate one; the owner is asked to correct any prompt that does, and the sources, not the prompts, are the record.]

CONDITION: any session asking how a decision waiting on the owner is to be put to the owner, whether the owner reads on a phone, or whether a saved answer on the page is a ruling.
ACTION: (1) Put every decision to the owner as a prompt with its full context and its options, never as a bare row or a code such as OR-n. (2) Design every owner-facing surface for a phone first. (3) Treat a saved answer as a choice, and write the ledger entry that quotes the owner's words before work that depends on it. (4) Correct a prompt that misstates its source, and say so in the commit.
DATE: 2026-10-28 — owner statements, quoted above.



<!-- O43 references/project-standards.md:4608-4650 -->

## Owner rulings 2026-10-29 — OR-1, OR-2, OR-3, OR-5 and OR-6 answered

Given in session https://claude.ai/code/session_01Ub36iQ3vbthbsh45LNks6j, in reply to prompts OR-1, OR-2, OR-3, OR-5 and OR-6 of the owner's browser page (`workplan/2026-10-23-pipeline-resolution-workplan.md` section 4; the decision sheet of the 2026-10-22 resolution report), and recorded on contact per `CLAUDE.md` rule 0 and workplan WR-3. Each answer is quoted verbatim. The answers to OR-2 and OR-3 are the option labels the prompts gave.

OR-1:

> "A parameter does not require a lens for each and every disability population or access need. Do not store table rows for parameters when there is a missing lens for a disability population or access need, i.e. for when the parameter is not relevant. In other words, I expect each and every determination to only have rows for the actual relevant lens. Ensure that all relevant codes/identification/lenses are filled out as required, i.e. a determination should never be limited to only one lens because we have different models for discussing disability (ICF, population identity, access needs)--we need to have each model filled out accordingly."

OR-2: "Branches, and an empty headline when all are conditioned"

OR-3: "Yes, reformat in place"

OR-5:

> "Co-1 figures may set a value insofar as the source is academically sound. Otherwise, they set the direction, not the number."

OR-6:

> "Stated and divergent, with a synthesis approach — We make the dispute transparent. We will provide the T1 source as the stated value, but we will note in discussion of the item that it has been disputed by the T2 source."

**What this does.** Five of the six decisions the workplan says gate building are answered; OR-8 is the one left. The readings below are the assistant's and are marked; the owner's words above are the ruling.

1. **OR-1.** Taken from the prompt's "yes": a figure reaches a determination only through the lens tags written on that figure, so D-0184 stands. The consequence the prompt gave, `pending` determinations for autistic, blind and ADHD people, the ICF code d450 and an effort need on parameter 3, is **overruled**: no row is stored for a parameter and lens the parameter is not relevant to, and none for a lens that no figure carries. The workplan's T-3 done-when sentence that expects those `pending` cells is overtaken, and so is the `not_applicable` state as a stored assertion (a cell for a lens the parameter is not relevant to is not stored), which `governance/evidence-methodology.md` section 2.5 required. [ASSUMPTION: relevance is shown by the figures that carry a lens, so a lens no figure carries has no row; the gaps table still records a missing figure for a lens that is relevant.] The ruling adds a requirement: every determination, and every figure under it, names each model that is relevant (identity, ICF code, access need, and medical when its registry is filled), never one. That raises D-0182's "ideally ties into many" from an authoring aim, which D-0182's notes say is "deliberately not mechanised", to a requirement for determinations. The CHECK stays at "at least one", the floor a CHECK can hold without refusing the single-lens rows that exist. D-0182's own aid is the means: the crossing maps suggest the codes that probably belong on the same row, and judgment confirms them, so lens tagging (D-2) fills every relevant model and not only the lens a quote names. [ASSUMPTION: "a determination should never be limited to only one lens" reads as one determination carrying the codes of every relevant model, in the way a cell already may (`assess_cell.lens_key`).] **Not settled by the ruling, put to the owner as OR-1c:** one figure holds one code per model, while a fact can concern several (for example d450 and d465).
2. **OR-2.** The prompt's recommended option, so T-2 is built as written. It narrows the 2026-07-21 most-accommodating selection to unconditioned claims only (`decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md` section 5.2; the architecture document line 122).
3. **OR-3.** Yes. Reformatting a figure's value, unit or empty setting in place, with the same digits and quote and the old text kept in notes, narrows D-0168's "a wrong claimed_value ... is a SECOND ROW" for reformatting only (`decisions/DR-2026-08-27-evidence-is-the-source-judgment-is-the-extraction.md`; `db.amend_extraction`'s first refusal). T-1 step 8 widens the amend verb and D-1 repairs the rows.
4. **OR-5.** Not the prompt's "yes" and not its "no". A Co-1 figure sets a value when its source is academically sound, and only the direction otherwise. This amends `references/methodology-evidence-hierarchy-mapping.md` section 6.4, whose "not co-primary for dimensional values" holds now only for a Co-1 source that is not academically sound, and T-4 step 3 changes from leaving every Co-1 row out of the numeric bound to leaving out those whose source is not academically sound. That section's claim that the boundary is already "mechanically expressed" stays false until T-4 builds it. The architecture document's claim-type split (line 41) is read the same way. [ASSUMPTION: "academically sound" is not a field of the database. The four Co-1 sources held on 2026-10-29 are two participatory-research journal articles and two others (a lived-experience publication and a DPO position statement), none flagged grey; re-derive with `select ref_id, co1_source_type, source_type, grey_flag from evidence_sources where evidence_type = 'co1'`. How soundness is established is put to the owner as OR-5b.]
5. **OR-6.** The prompt's recommended option, so section 3.3 of `governance/evidence-methodology.md` stands: the determination is `stated`, the convergence is `divergent`, and a synthesis approach is supplied. The owner's sentence is that approach for a T1 source against a T2 source: the T1 figure is the stated value and the discussion of the item says the T2 source disputes it. [ASSUMPTION: the approach is the owner's words, cited by a pointer to this entry and not written by the engine, which the workplan declines (K-5). It applies to claims that cannot all hold; OR-4 and OR-6b, which govern differing floors that can all be met, are still open. Whether it covers every divergence or only T1 against T2, and whether section 3.3's design range still takes in the disputing figure, is put to the owner as OR-6c.]

**What is unblocked, and what still waits.** T-2 is unblocked (OR-2), and T-1 step 8 with D-1 (OR-3). T-3 and D-2 wait on OR-1b and OR-1c; T-4 waits on OR-4, OR-5b, OR-6b and OR-6c; T-6b step 4 on OR-8.

**Marks owed, named so they are not lost.** A mark in `decisions/` needs an attestation (rule 2), so these are left to the workplan's H-0: DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md (D-0182's "ideally-many" note), DR-2026-07-21 section 5.2 (OR-2), DR-2026-08-27 (OR-3), and the architecture document lines 41 and 122. The prose that restates the four cell states and still lists `not_applicable` (`governance/evidence-architecture.md` lines 26 and 116, `governance/mission-and-epistemics.md` line 118, `CLAUDE.md` section 6) is swept in the tooling change that retires or re-scopes that state, which is a decision for the T-3 pull request.

```
SUPERSEDES: governance/evidence-methodology.md :: "A cell is `not_applicable` when the parameter genuinely has no design implication for the population."
  BY: references/project-standards.md :: "Do not store table rows for parameters when there is a missing lens for a disability population or access need"
SUPERSEDES: references/methodology-evidence-hierarchy-mapping.md :: "which require T1/T2/T3 evidence (or regulatory citation for the code minimum)"
  BY: references/project-standards.md :: "Co-1 figures may set a value insofar as the source is academically sound."
```

CONDITION: any session asking whether a determination is stored for a lens the parameter is not relevant to, whether a determination may carry one lens, whether Co-1 may set a value, how a T1 against T2 divergence is stated, whether conditional claims are shown as branches, or whether a figure may be reformatted in place.
ACTION: (1) Store no row for a parameter and lens the parameter is not relevant to, and none for a lens that no figure carries. (2) Fill every relevant model on a determination and on the figures under it; do not read the CHECK's "at least one" as the aim. (3) Build T-2 as written, and T-1 step 8 and D-1 with in-place reformatting. (4) Let a Co-1 figure set a value only when its source is academically sound, and settle how that is established (OR-5b) before T-4 step 3. (5) For a T1 against T2 divergence, state the T1 figure and note the dispute in the item's discussion, citing this entry as the synthesis approach. (6) Treat every [ASSUMPTION] above as unratified.
DATE: 2026-10-29 — owner statements, quoted above.



<!-- O44 references/project-standards.md:4651-4708 -->

## Owner rulings 2026-10-29 (second) — OR-8, OR-1b, OR-4, OR-6b, OR-7, OR-9, OR-10, OR-11a, OR-11b, OR-12a, OR-12b, OR-13, OR-14, OR-15 and OR-16 answered

Given in session https://claude.ai/code/session_01Ub36iQ3vbthbsh45LNks6j, in reply to prompts OR-8, OR-1b, OR-4, OR-6b, OR-7, OR-9, OR-10, OR-11a, OR-11b, OR-12a, OR-12b, OR-13, OR-14, OR-15 and OR-16 of the owner's browser page, after the entry above, and recorded on contact per `CLAUDE.md` rule 0 and workplan WR-3. Each answer is quoted verbatim.

OR-8: "Yes, per parameter and bucket so long as the bucket is not just jurisdiction but associated language."

OR-1b: "No, ALL reaches only an ALL determination"

OR-4: "Yes, the most accommodating value wins"

OR-6b: "No, the spread is printed in the note"

OR-7: "Yes, show it flagged — Empty circle."

OR-9: "None yet"

OR-10: "Yes, convert and show both — Round to nearest 1/4" or 5mm."

OR-11a: "Yes, require a full-scope scan"

OR-11b: "Yes, flagged for follow up."

OR-12a: "Yes, scope them out for now"

OR-12b: "Yes, flagged — With that said, I expect that the model will be using real terms that are actually in use within a jurisdiction."

OR-13: "From the codes held"

OR-14: "Yes, derive it — This derivation is what I expect the specifications pass to be doing--adjudicating, deriving and synthesizing across rows of related evidence."

OR-15: "Yes, use batch 23's material"

OR-16: "Yes, read what we hold first"

**What this does.** With these, all six decisions the workplan says gate building are answered.

1. **OR-8.** Yes: exhaustion is judged per parameter, per bucket member, with the bucket list entered once as a table (T-6b steps 4 and 5). The owner's condition is on what a bucket member is: a jurisdiction together with its associated language, never the jurisdiction alone. [ASSUMPTION: "associated language" means the pairs `lang_jur_map` already records, whose key is language by jurisdiction, so a jurisdiction with several associated languages is several bucket members, and the bucket table points at those pairs with an approval reference on each row and does not restate the languages (rule 5).] Which pairs belong to buckets 1 and 2 is not settled here: the 2026-09-28 ruling names the buckets' jurisdictions, and T-6b proposes the pairs for the owner's approval.
2. **OR-1b.** The prompt's recommended option: a figure tagged with the identity code ALL reaches only a determination whose identity is ALL. T-3's predicate gets no clause for it.
3. **OR-4.** The prompt's recommended option: within T1, Co-1, T2 and Co-2 the most accommodating value wins, whichever of them stated it. The 2026-07-21 rule as the engine extends it is unchanged, and no composition rule has to be stated. It governs differing figures that can all be met; claims that cannot all hold are OR-6's. [ASSUMPTION: OR-5 applies first, so a Co-1 figure whose source is not academically sound is out of the numeric bound before this rule picks.]
4. **OR-6b.** The prompt's recommended option: anchoring floors that differ but can all be met (the report's example is at least 900 and at least 1500) are not divergent. The spread is printed in the value note, and T-4 step 2 does not mark them divergent, so a cell with several such sources needs no synthesis approach.
5. **OR-7.** The prompt's recommended option: a determination resting only on a regulation (T6, `code_floor_only = 1`) appears in the best-practice view, flagged with the empty circle (○), the weak marker that `governance/tier-system.md` already gives a T6 code floor. T-5 step 2 drops the `code_floor_only = 0` filter from the view. Option A, as tier-system section 8 and the architecture document line 121 ratify it, is confirmed, so no ratified text changes.
6. **OR-9.** The prompt's recommended option: no search indices are named yet, so T-6 step 6 (a table of search indices) is not built and coverage is not measured by index.
7. **OR-10.** Yes: the engine composes across exact linear units (inches and feet with millimetres and metres), converts, and shows both, the converted figure rounded to the nearest quarter inch or 5 mm. This amends ACTION (4) of "Owner ruling 2026-09-17 — PRESENT BOTH notations", which kept units apart, for exact linear units (a mark is placed at that ACTION line). Its ACTION (3), never to round a derived figure into the position of a stated figure, still holds. [ASSUMPTION: the rounding is of what is shown beside the source's own figure, and the stored bound stays exact, as T-1 step 9 reads `('36','in','>=')` as the exact fraction of a millimetre. Which way a rounded minimum or maximum moves is put to the owner as OR-10b.]
8. **OR-11a.** The prompt's recommended option: an extraction marked `verified` requires a recorded full-scope `source_scans` reading that covers the row's parameter. T-1 step 10 is built, and the renderer prints the status of each row. No ratified text changes.
9. **OR-11b.** The prompt's recommended option: a figure read in full but still `preliminary` may set a published value, flagged. No engine change, and the renderer (T-5) shows the flag. [ASSUMPTION: "for follow up" asks that the flag say the figure still awaits review; it does not by itself raise a follow-up record for each figure.]
10. **OR-12a.** The prompt's recommended option: Arabic, Bengali, Hindi and Swahili, which `lang_jur_map` requires and for which the project has no aliases, are scoped out by the bucket table until buckets 1 and 2 are exhausted, so building their aliases is not research debt now. [ASSUMPTION: with OR-8's bucket member as a jurisdiction-and-language pair, their pairs are not bucket members until then.]
11. **OR-12b.** The prompt's recommended option: a model-generated alias may be used for a search if the search is flagged. The owner adds an expectation, and it is an instruction to the model: generate only terms actually in use in the jurisdiction, not word-for-word translations of English terms. That is research rule R11 (no back-translation; every alias carries its in-language source or is marked unverified) applied to model-generated aliases. [ASSUMPTION: no stricter gate is ruled, such as requiring an in-language source before the alias is used; the flag says the alias is model-generated and not yet attested by a retrieved source. `python3 scripts/audit/alias_provenance_audit.py` lists them.]
12. **OR-13.** The prompt's recommended option: the list of quantities (parameters) is seeded by an open-pass scan of the bucket 1 and 2 codes already held, not slug by slug. D-8 is built as written; it also needs D-3 for the open pass, T-6b for the buckets, and OR-17.
13. **OR-14.** Yes: a book page for an element (a ramp) is derived from a typed term pointer to the live determinations of its parameters, with one parameter as the degenerate case, and is never a container that rows are filed into. T-7 and D-6 are built. The owner's note places this derivation in the specifications pass: "adjudicating, deriving and synthesizing across rows of related evidence". [ASSUMPTION: that is an expectation of the pass, not only of the renderer. T-7 as proposed derives the page at read time from the parameters' determinations (a view and a renderer option); whether the specifications pass itself writes an element-level determination is put to the owner as OR-14b.]
14. **OR-15.** The prompt's recommended option: the inter-rater test uses held batch-23 material, one code with a step table and one T1 paper with findings. D-5 as written.
15. **OR-16.** The prompt's recommended option: sources already held, inside and outside buckets 1 and 2, are read before more are fetched. D-3 covers every source that has not been superseded.

**What is unblocked, and what still waits.** T-6b steps 4 and 5 are unblocked, and T-5 step 2 (it still needs T-2 to T-4). T-6b step 6 is not built. T-1 step 9 (OR-10) and step 10 (OR-11a) are unblocked. T-3 waits on OR-1c only. T-4 now waits on OR-5b and OR-6c.

CONDITION: any session asking what a coverage bucket member is, whether exhaustion is judged per slug or per parameter, whether an identity-ALL figure reaches the determination of a particular group, which anchoring value wins when sources differ, whether differing floors that can all be met are divergent, whether a regulation-only determination is shown, whether units of length are converted, whether `verified` needs a scan, whether an element page is derived, or what material the inter-rater test uses.
ACTION: (1) Build T-6b steps 4 and 5 with a bucket member as a jurisdiction-and-language pair that points at `lang_jur_map`. (2) Let an ALL figure reach only an ALL determination. (3) Let the most accommodating anchoring value win among differing figures that can all be met. (4) Print the spread of such figures in the value note and do not mark them divergent. (5) Show a regulation-only determination in the best-practice view, flagged ○. (6) Build no table of search indices. (7) Convert exact linear units and show both, the converted figure rounded to the nearest quarter inch or 5 mm and never in the position of a stated figure. (8) Require a full-scope scan for `verified`. (9) Let a `preliminary` figure set a value, flagged. (10) Scope Arabic, Bengali, Hindi and Swahili out until buckets 1 and 2 are exhausted. (11) Use a model-generated alias in a search only when the search is flagged, and generate only terms actually in use in the jurisdiction. (12) Seed the list of quantities from the codes held, not slug by slug. (13) Derive element pages from a typed term pointer to parameters' live determinations, never as a container (T-7, D-6). (14) Use batch 23's material for the inter-rater test (D-5). (15) Read the sources already held, every one not superseded, before fetching more (D-3). (16) Treat the [ASSUMPTION] marks above as unratified.
DATE: 2026-10-29 — owner statements, quoted above.



<!-- O45 references/project-standards.md:4709-4781 -->

## Owner rulings 2026-10-29 (third) — OR-17, OR-18, OR-19, OR-20, OR-21, OR-22, OR-23, OR-24, OW-1, OW-2, decisions D-0139, decisions D-0140, decisions D-0165, observed_terms 65, observed_terms 68, observed_terms 70, observed_terms 71 and observed_terms 73 answered

Given in session https://claude.ai/code/session_01Ub36iQ3vbthbsh45LNks6j, in reply to prompts OR-17, OR-18, OR-19, OR-20, OR-21, OR-22, OR-23, OR-24, OW-1, OW-2, decisions D-0139, decisions D-0140, decisions D-0165, observed_terms 65, observed_terms 68, observed_terms 70, observed_terms 71 and observed_terms 73 of the owner's browser page, after the entries above, and recorded on contact per `CLAUDE.md` rule 0 and workplan WR-3. Each answer is quoted verbatim.

OR-17: "Yes, bulk, with me reading the PR — Ensure that these phrases/names/aliases are all present in their prescribed jurisdiction/language. It is not acceptable for the model to generate its own phrases/names/aliases."

OR-18: "Transcripts suffice"

OR-19: "Yes, presume an echo"

OR-20: "No — We don't need to mine backwards for T4 to T6--whatever is given to us by them is what we accept as a matter of fiat. We are not interested in their history itself."

OR-21: "Yes, when it first arises"

OR-22: "Something else — This is why we use backwards citation mining and contextual clues. If we are unable to find the actual parameters/values under discussion, then the source itself has no value. If we are able to find the actual parameters/values under discussion, then the absence of findings--i.e. the lack of prescribed change to that parameter/value--is simply a confirmation of the validity of those parameters/values."

OR-23: "Confirm -- This applies only when the source is properly cited in an academic context, i.e. there is a valid academic route to the source."

OR-24: "Confirm"

OW-1: "Yes, map views to a stage — I expect the rendering to occur on the basis of whatever specification has been synthesized accordingly, and I expect the render table to be one where the specification table rows have been converted into complete prose, bibliographic information etc accordingly from the preceding tables such that it can be displayed properly on the website repository."

OW-2: "Yes, register it"

decisions D-0139: "Ratify it (active)"

decisions D-0140: "Ratify it (active)"

decisions D-0165: "Ratify it (active) — ...room acoustics is PIVOTAL for deaf and hard-of-hearing people. Room acoustics were literally developed with these persons in mind."

observed_terms 65: "It names a term we have — All it does is tell where the ramp slope is to be calculated from, i.e. the middle of the ramp. The gradient is another for the slope."

observed_terms 68: "It names something new — Barrier-free path of travel is not limited to ramps, but the entire procession throughout a building."

observed_terms 70: "It names a term we have — ramped access route = ramp. access route is about procession throughout a building"

observed_terms 71: "It names a term we have — refers to barrier-free path of travel"
[SUPERSEDED as to what observation 71 names, by "Owner rulings 2026-10-29 (fifth)" below.]

observed_terms 73: "It names a term we have — it is a ramp, and the access route refers to the barrier-free path of travel insofar as it concerns navigating a building"

**What this does.** The readings are the assistant's and are marked; the owner's words above are the ruling.

1. **OR-17.** Yes: the assistant approves vocabulary in bulk (D-4, D-8) and the owner reads the pull request. The owner's conditions are part of the ruling: every phrase, name and alias is present in its prescribed jurisdiction and language, and the model may not generate its own phrases, names or aliases. [ASSUMPTION: 'present in' means attested by a retrieved source of that jurisdiction and language, an observed phrase with its source, and each pull request that approves a phrase carries that attestation for it. This is stricter than the ruling on OR-12b, which let a flagged search use a model-supplied alias that is a real term in use. The later and stricter statement governs the vocabulary. Whether a flagged search may still use a recalled term, and what becomes of the model-generated aliases already stored (`python3 scripts/audit/alias_provenance_audit.py` counts them by language), is put to the owner as OR-17b.]
2. **OR-18.** The prompt's recommended option: the preserved transcripts, which carry the model and effort of every assistant message, are the telemetry. D-5 derives model and effort from them, and session records need no `Model:` or `Effort:` lines.
3. **OR-19.** The prompt's recommended option: a grey (T3) source that repeats a code's value is presumed to echo the code, without being re-tiered, and the presumption can be rebutted. T-8 step 3 applies it.
4. **OR-20.** The prompt's recommended option: T4 to T6 anchors are not mined backward for root tracing. What a regulation, standard or national framework states as its own requirement is accepted as given, and its history is not traced. Research contract rule R2 is unchanged and D-7 gets no mining pass. [ASSUMPTION: 'accepted as a matter of fiat' covers the figure the source states as its own rule. It does not lift the walling-off of T4 to T6 from full-strength anchoring (`CLAUDE.md` section 6), nor the requirement that the source be retrieved and verified, or read as the empty circle.]
5. **OR-21.** The prompt's recommended option: when a direction is contested, a direction is recorded for each lens, once the case first arises. The query that finds the case returns nothing today, so nothing is built now.
6. **OR-22.** Neither of the prompt's two options. A study whose rows are all absence findings confirms the value it tested, provided the actual parameters and values under discussion can be found, by backward citation mining of the study and by contextual clues. If they cannot be found, the source has no value. If they can, the lack of a prescribed change is a confirmation of the validity of those values. This answers item 2 of "Correction 2026-10-22" (what a floor claim confirmed by an all-absent study is): it is a confirmed claim, not a regulation-only floor, and it is consistent with the owner's clarification of 2026-10-21. It is not in conflict with OR-20: that rule is about tracing a regulation's own history, and this is mining the study's citations to find which values it tested. [ASSUMPTION: the confirmed floor claim takes the band of its confirming study, as `_confirmed_bands` in `scripts/assess/assess_cell.py` already gives a confirmed code, so migration 116's CHECK that holds a regulation-only cell at the empty circle must not apply to it; and a study whose tested values cannot be identified is given no role, and is flagged as such. Which marker the cell reads is put to the owner as OR-22b.]
7. **OR-23.** Confirmed, with a condition: an unretrievable source keeps its tier and may still anchor a determination, earning no band above the empty circle, only when the source is properly cited in an academic context, that is, when there is a valid academic route to it. This amends the sentence of `governance/tier-system.md` section 8 that states the rule without the condition (the mark is placed there). [ASSUMPTION: a valid academic route is what the project already records as how the existence of a source was established without retrieving it: a resolving DOI or index record, or a citing bibliography (the `verification_method` values). A source with no such route keeps no tier claim and does not anchor; the ruling does not say what becomes of those already held. As of 2026-10-29 six held sources are `UNVERIFIED`, one T1 paper with a corroborating route and no DOI, one T4 standard and four T6 codes with no DOI (`select ref_id, tier, verification_method, doi from evidence_sources where verification_status = 'UNVERIFIED'`). Whether a code or standard, which is not cited in academic literature, has a valid route through a registry citation is put to the owner as OR-23b.]
8. **OR-24.** Confirmed: 'skimmed' means `extraction_method = 'skim'`, which the ledger entry of 2026-10-09 (item 4) had marked as an assumption. The assumption is now ruled.
9. **OW-1.** Yes: a view mapped to a stage counts as a member of that stage in the walkability check, and `governance/stage-map.yaml` gains a `views:` key. The owner adds an expectation about the render stage itself: rendering is done on the basis of whatever specification has been synthesized, and the render table holds the specification rows converted into complete prose, with bibliographic information and the rest drawn from the preceding tables, so that the website repository can display it as it stands. This overtakes the workplan's note that no render table is designed and that the report says not to invent one, and it re-opens T-5, which was drafted as a view and a renderer writing to a scratch directory. [ASSUMPTION: the render table lives in the database and the site reads it, so the 2026-08-27 ruling that render surfaces are read from the database when rendered, and that no committed file is a render, still holds; rule 5 (point, do not copy) is met if each render row points at its specification and records a hash of its inputs, so that a stale row is detectable. How the prose is produced is put to the owner as OW-1b, and whether the table is stored or rebuilt as OW-1c.]
10. **OW-2.** The prompt's option: `workplan/pipeline-state-graph/walkability.py` outlives the instrument and is registered as the stage-pair gate, by one registry entry that fails when a stage pair has no path (the workplan's completion test, item 7). [ASSUMPTION: the entry is added once the views key of OW-1 has landed. Before that the pairs ending at render print NO PATH by construction, so registering it earlier would fail at once.]
11. **decisions D-0139.** Ratified: decision D-0139, which issued `architecture/schema-spec.md` as the SQL specification for the SQLite storage form, becomes active. **The reason it was held is unchanged by this ruling and stays on the record:** the decision's notes ("RATIFICATION 2026-08-04") say the document describes a database that does not exist, naming specification, population, conflict, measurement, jurisdictional_value, specialist and doctrine as tables, none of which were in the database, with only 4 of 66 live table names appearing in it at all. Ratifying it makes the document a binding decision without making it describe the schema, which the owner may wish to correct. [ASSUMPTION: the ruling is read as ratifying the decision as the B1 session's specification of record, and does not ask for the document to be brought into line with the database; say if it does.] The `decisions` table has no `db.py` verb, so its status row stays PROPOSED until one exists; the ledger is the record of the ruling meanwhile, and the missing verb is a coverage gap to be filed in a tooling pull request, never closed by a hand edit.
12. **decisions D-0140.** Ratified: decision D-0140, the Change Order proposing that the repository stay one repository with the SQLite database inside it (`governance/repo-strategy-revision-co.md`), becomes active. Its notes say adoption applies the revisions of its sections 3.1 to 3.4 to `governance/repo-strategy.md` and archives the Change Order. That follow-on edit is not made by this ruling. [ASSUMPTION: the ruling ratifies the decision, and the edit to `governance/repo-strategy.md` waits for the owner's word. The Change Order names the database as `data/db/guidebook.db` and the migration tooling as `scripts/migrate/`, which are not the live paths (`data/guidebook.db`, `scripts/migrations/`) and the first of which is a retired pointer in `governance/retired-vocabulary.yaml` (RV-008), so applying its text as written would add retired vocabulary to the live surface and must correct those paths. The `decisions` row stays PROPOSED until the table has a verb, as for D-0139.]
13. **decisions D-0165.** Ratified, and the question it deferred is answered: deaf and hard-of-hearing people belong on the room-acoustic-performance topic, because room acoustics is pivotal for them. Decision D-0165 (2026-08-22) held two questions, whether deaf and hard-of-hearing people belong on that slug and what the old item A-18's applicability set should be, pending a population-taxonomy pass, and it said the first determination on the slug was blocked until the pass ran. The finding behind it stands on its record: the project's only T1-anchored reverberation value identified so far (held as source_locators leads REF-00578 and REF-00325) concerns hearing-aid and cochlear-implant users, and the owner-signed May 2026 reasoning document names the deaf as the worst-case user. The owner's ruling supersedes the deferral's outcome ("No population is added to or removed from room-acoustic-performance") for deaf and hard-of-hearing people. [ASSUMPTION: the identity code DEAF ("Deaf and hard-of-hearing people") is the lens for them, with the ICF hearing codes (b230, d115, d310) and the access need A-NOSOUND to be tagged on the figures where relevant under the ruling on OR-1. The item layer the deferral spoke of, A-18 and its population links, no longer exists, so the block it records lapses for this question; which other groups belong on the slug is not ruled. The historical statement that room acoustics was developed with these persons in mind is the owner's, and is not checked here.] The `decisions` row stays DEFERRED until the table has a verb, as for D-0139.
14. **observed_terms 65.** Observation 65 (REF-01010, "gradient measured along the centre line") is judged to name an existing term. The assistant reads it as TERM-001, ramp gradient [ASSUMPTION: basis above]. The phrase adds a place of measurement, the middle of the ramp, and no term of its own; "gradient" is the owner's word for the slope.
15. **observed_terms 68.** Observation 68 (REF-01013, "barrier-free path of travel") is judged to name something new: the whole route of travel through a building, ramps being only part of it. The held term TERM-048, circulation route, is defined as a continuous route through a building for horizontal movement, so whether the new term differs from it is the question OT-1 puts to the owner.
16. **observed_terms 70.** Observation 70 (REF-01015, "ramped access route") is judged to name an existing term. The assistant reads it as TERM-089, ramp [ASSUMPTION: basis above]. The owner places "access route" with the whole-building route of observation 68, not with the ramp.
17. **observed_terms 71.** Observation 71 (REF-01016, "accessible route", NZS 4121:2001 definitions clause) is judged to name an existing term: the one observation 68 names as new, barrier-free path of travel. It can be adjudicated NAMES-EXISTING only after that term has been added, so it follows observation 68 in the order of work. [SUPERSEDED as to what observation 71 names, by "Owner rulings 2026-10-29 (fifth)" below.]
18. **observed_terms 73.** Observation 73 (REF-01018, "ramped access route", TGD M 2022 clause 1.1.3.4, the same phrase and locator as observation 70) is judged to name an existing term. The assistant reads it as TERM-089, ramp [ASSUMPTION: basis above], with the access route within it understood as the barrier-free path of travel of observation 68.

**What is unblocked, and what still waits.** D-4 and D-8 can proceed under OR-17's conditions (D-8 also needs D-3 and T-6b). D-5 reports model and effort from the transcripts. T-8 step 3 is unblocked (T-8 itself needs T-4). D-7 is smaller by one mining pass. The REF-00980 cell can enter the first render (S-1) once its data steps are done (the full reading, the backward mining that identifies the tested values, the repointed confirms edge) and the engine change lands. The engine change for the empty-circle rule waits on OR-23b for codes and standards. The stage-map views key and the walkability change are unblocked. T-5 waits on OW-1b and OW-1c as well as on T-2 to T-4. One registry entry, after the OW-1 change. D-0140 and D-0165 still wait. A verb for the decisions table is a coverage gap. D-0165 still waits. The first determination on room-acoustic-performance is no longer held by D-0165 for deaf and hard-of-hearing people. Tagging the held figures for that slug with DEAF, the ICF hearing codes and A-NOSOUND is research data work for its own pull request (D-2), after the lens change (T-3). Observations 65 and 70 can be adjudicated NAMES-EXISTING in a data batch. Observation 68 waits on the definition of the new term (OT-1). Observation 71 follows 68.

```
SUPERSEDES: governance/tier-system.md :: "An unretrievable source keeps its tier and may still anchor a determination (D-0157: a return pass is owed)"
  BY: references/project-standards.md :: "This applies only when the source is properly cited in an academic context, i.e. there is a valid academic route to the source."
```

CONDITION: any session asking whether the assistant may approve vocabulary in bulk and on what conditions, or whether the model may generate phrases, names or aliases; or where the model and effort of a session are recorded; or how a grey source that repeats a code's value is treated; or whether T4 to T6 sources are traced back to their origins; or whether a contested direction is recorded per lens; or what a floor claim confirmed by an all-absence study is, or what an absence-only study is worth when its tested values cannot be found; or whether an unretrievable source keeps its tier and may anchor, and on what condition; or what 'skimmed' means; or whether a view counts as a member of a stage, or what the render stage holds; or whether the walkability check is registered; or whether decision D-0139 is ratified, or why the decisions table's status was not changed; or whether decision D-0140 is ratified; or whether deaf and hard-of-hearing people belong on the room-acoustic-performance topic, or whether decision D-0165 still blocks its first determination; or adjudicating observed_terms 65, 68 or 70, or naming a term for "barrier-free path of travel", "access route" or "ramped access route".
ACTION: (1) Approve vocabulary in bulk for D-4 and D-8, with the owner reading the pull request, only where each phrase, name and alias is attested in its jurisdiction and language, and never approve a phrase the model generated. (2) Derive model and effort from the transcripts for D-5. (3) Presume a grey source that repeats a code's value to be an echo of the code, rebuttably and without re-tiering it (T-8 step 3). (4) Do not mine T4 to T6 anchors backward for root tracing; accept what the regulatory source states as given. (5) Record a direction per lens when a direction is first contested; build nothing before then. (6) Treat an absence found at an identified tested value as confirmation of that value; give a study whose tested values cannot be identified no role, and flag it; use backward citation mining and contextual clues to identify them. (7) Let an unretrievable source keep its tier and anchor, below the weak band, only when it has a valid academic route. (8) Read 'skimmed' as extraction_method = 'skim'. (9) Map views to stages in the stage map and count them in walkability (OW-1). Treat the render stage as a table of complete prose and bibliographic information built from specifications and the preceding tables, and settle how it is produced and kept (OW-1b, OW-1c) before T-5. (10) Register walkability.py as the stage-pair gate once views are mapped to stages. (11) Treat D-0139 as ratified, with its hold reason still on the record, and file the decisions-table verb as a coverage gap in a tooling pull request. (12) Treat D-0140 as ratified; apply the Change Order to governance/repo-strategy.md only on the owner's word, with its two stale paths corrected. (13) Treat deaf and hard-of-hearing people as belonging on room-acoustic-performance, and do not hold the slug's first determination on D-0165 for them. (14) Adjudicate observed_terms 65 NAMES-EXISTING pointing at TERM-001 (ramp gradient), with the rationale that the phrase only locates where the slope is taken, the middle of the ramp, and that gradient is another word for the slope [ASSUMPTION: the term meant is TERM-001, the only held term that is a ramp's slope — basis: its definition, "Slope of an accessible ramp expressed as ratio or percentage"]; observed_terms 70 NAMES-EXISTING pointing at TERM-089 (ramp), with the rationale that an access route is the route through a building and is no part of the term [ASSUMPTION: the "=" reads as the phrase's head being ramp, so TERM-089 — basis: the owner's gloss]; observed_terms 68 NAMES-NEW, after the new term's definition has your approval (OT-1). All three go through db.py adjudicate-term in a data PR, none before. (15) Observation 73 is adjudicated NAMES-EXISTING pointing at TERM-089 like observation 70, with the access-route reading in its rationale. Two observations now carry the one phrase "ramped access route" (70 and 73); any other held observation of it takes the same judgment unless you say otherwise. (16) Treat every [ASSUMPTION] mark above as unratified.
DATE: 2026-10-29 — owner statements, quoted above.



<!-- O46 references/project-standards.md:4782-4797 -->

## Owner rulings 2026-10-29 (fourth) — OT-1 answered

Given in session https://claude.ai/code/session_01Ub36iQ3vbthbsh45LNks6j, in reply to prompts OT-1 of the owner's browser page, after the entries above, and recorded on contact per `CLAUDE.md` rule 0 and workplan WR-3. Each answer is quoted verbatim.

OT-1: "Barrier-free path of travel. It is a circulation route that is specific to people in wheelchairs/mobility devices."

**What this does.** The readings are the assistant's and are marked; the owner's words above are the ruling.

1. **OT-1.** The new term for the whole route through a building (observation 68, with 71 referring to it) is named "barrier-free path of travel". The owner places it as a circulation route, in the sense of TERM-048, that is specific to people who use wheelchairs or other mobility devices. It is therefore narrower than TERM-048, whose definition names no such limit. The `terms` table has no parent column, so the relation is stated in the new term's definition and scope note, which the owner approves first (OT-2). The ruling on observation 71 puts "accessible route" under this term; the assistant has not read the NZS 4121:2001 clause beyond the quoted line, and flags that a source using "accessible route" for disabled people generally would name something wider than this term [ASSUMPTION: NZS 4121's usage is the narrow one — basis: none yet; the owner's ruling on 71 stands until a source shows otherwise]. [AMENDED as to observation 71 and the "accessible route" alias by "Owner rulings 2026-10-29 (fifth)" below.]

**What is unblocked, and what still waits.** The name of the new route term is settled. Its definition waits on OT-2, and observations 68 and 71 wait on the definition.

CONDITION: any session asking defining or adjudicating a term for the whole route through a building, or reading TERM-048 (circulation route) against "barrier-free path of travel".
ACTION: (1) Add the term, canonical name "barrier-free path of travel", only after its definition and scope note have the owner's approval (OT-2); then adjudicate observation 68 NAMES-NEW and observation 71 NAMES-EXISTING pointing at it. Its aliases are the phrases the sources use ("accessible route", "access route"), each with its in-language source, and none the model writes itself (R11, OR-17). (2) Treat every [ASSUMPTION] mark above as unratified. [AMENDED as to observation 71 and the "accessible route" alias by "Owner rulings 2026-10-29 (fifth)" below.]
DATE: 2026-10-29 — owner statements, quoted above.



<!-- O47 references/project-standards.md:4798-4813 -->

## Owner rulings 2026-10-29 (fifth) — observed_terms 71 (revised) answered

Given in session https://claude.ai/code/session_01Ub36iQ3vbthbsh45LNks6j, in reply to prompts observed_terms 71 (revised) of the owner's browser page, after the entries above, and recorded on contact per `CLAUDE.md` rule 0 and workplan WR-3. Each answer is quoted verbatim.

observed_terms 71 (revised): "good point. accessible route is not the exact same as barrier-free path of travel, ie accessible route must be able to be navigated by someone who is blind"

**What this does.** The readings are the assistant's and are marked; the owner's words above are the ruling.

1. **observed_terms 71 (revised).** The owner's ruling on observation 71 in the third entry, that "accessible route" refers to barrier-free path of travel, no longer holds. An accessible route is a different thing: it must be navigable by someone who is blind, which is not a condition the owner put on the barrier-free path of travel of OT-1 (wheelchair and mobility-device users). What the phrase names is not yet ruled, and it returns to the owner's waiting list [ASSUMPTION: the statement settles that it is not the same term, not what it is — it may name a held term, a new one, or neither]. The catalogue already holds "accessible route" as an alias of TERM-048, circulation route, written by an earlier synonym-grouping build as a retrieval aid; whether that alias stays is part of the same judgment. The draft definition in OT-2 drops "accessible route" from its source phrases.

**What is unblocked, and what still waits.** OT-2 no longer waits on a check of NZS 4121; it waits only on the owner's approval of the wording. Observation 71 waits on the owner.

CONDITION: any session asking adjudicating observation 71 or any observation of "accessible route", or defining "accessible route" or "barrier-free path of travel".
ACTION: (1) Observation 71 is not adjudicated NAMES-EXISTING pointing at barrier-free path of travel, and "accessible route" is not recorded as an alias of it. The OT-1 action in the fourth entry is amended in those two respects. Observation 71 is adjudicated only on the owner's answer to its prompt. (2) Treat every [ASSUMPTION] mark above as unratified.
DATE: 2026-10-29 — owner statements, quoted above.



<!-- O48 references/project-standards.md:4814-4868 -->

## Owner rulings 2026-10-30 — best practice, the specification page and rendering (from the ramp-slope session)

Given in the owner's local session `d9505991-620e-4974-95b2-b407384c5793` (exported as `session-export-1793395272333`, titled "Research pipeline stress test: ramp slopes"), on 2026-10-29 and 2026-10-30, after the entries above, and recorded here on the owner's instruction of 2026-10-30 to implement those decisions in the repository, per `CLAUDE.md` rule 0 and workplan WR-3. The statements were found in the session transcript and are quoted verbatim; the reconciliation against `main` is `workplan/2026-10-30-ramp-spec-pages/RENDER-DECISIONS-AND-PIPELINE.md`.

On best practice and the specification:

- "best practice = the best way to do something according to how it benefits the intended group"
- "best practice =/= most common or agreed upon. we have been through this a million times"
- "remember that our guidebook doesn't take positions. it just presents what appears to be the most accommodating/gentle best practice for anything... so unless an academic article or some professional body improves upon germany's standard, that's identified as the best practice"
- "the gentlest value is the gentlest value. the evidence is that it exists in practice. there does not need to be academic studies or anything because they are not always going to be available"
- "i don't want us to highlight the steepest slope allowed in codes read"
- "You do not need to find evidence for why 1:12 was the code floor--just accept the 1:12 as a baseline to work from. Lots of the code stuff we are dealing with is like this--there is not open available research behind it"
- "We are interested in what are best practices NOW, and that means we do not need to interrogate the history of anything but rather the current state of everything"
- "specification in book and item pages now are the same idea in that it tells you the correct way to design something"
- "the critical methodology comes from synthesis/adjudication/specifications, not from evidence collection"

On states, scope and sources:

- "...covered means that the source that has been listed in the database has been read and had information extracted from it then verified"
- "provisional means that we have to go back and review the source again to confirm information accuracy" (the owner's answer 10 reads "stage. provisional means that we have to go back and review the source again to confirm information accuracy")
- "how on earth do we have evidence outside the library? we either have evidence or we do not have evidence. our library is just what we have recorded"
- "Yes it is P1+P2+P3" and "do not include countries outside of the major identified countries for now"
- "I think the issue is not the slope of the ramp, but the lack of a rest landing." and, to the question whether to make rest-landing spacing a second headline parameter, "Yes, next session"

On rendering and the page:

- "i want it to be coming from database directly in ideal world"
- "There is an audience lens (the four audiences) and a disability lens (population, ICF, access needs)"
- "Filter the page by one of three lenses: population vs ICF code vs access need, and then when you select which lens do you see the pills pop up wit the more specific case for further filtering"
- "the filters have to precede the information"
- "for ramp gradient, i want there to also be an easy comparison master table where you just see what each jurisdiction has for the value"
- "we do not need to have rows for people where the value is just "Not set." that just means that it shouldn't be showing on the page"
- "the question beneath the title is irrelevant"
- "note: all work must comply with website accessibility standards and best practices"
- "ensure that minimalism does not come at the expense of readability/legibility especially as it pertains to accessibility practices for website navigation"
- "refer to swiss graphic design"

**What this does.** The readings are the assistant's and are marked; the owner's words above are the ruling.

1. **Best practice is the most accommodating value found, not the commonest.** The value a determination names as best practice is the gentlest or most accommodating one found in practice, in the direction recorded for the parameter (`base_parameters.accessibility_direction`; for ramp gradient, lower is better), unless a study or a professional body improves on it. It is not the modal or the agreed value, and the steepest value a code allows is not highlighted. No study is needed for a value to be named, and a T4 to T6 value is accepted as a baseline without tracing its history. [ASSUMPTION: this ruling selects which value is named; it does not change the band or the flag. Under the 2026-07-21 owner directive (Option A, `governance/tier-system.md` section 8, `governance/evidence-architecture.md` I3), a determination resting on T4 to T6 alone is already stated as weak-band (○) "best practice as currently known", flagged weak and code-derived, with the convergence-not-evidence caveat. Read together, the gentlest code value is named best practice at ○ with the flag. The ramp session's page marked such values ● and called the conflict "D-DOCT"; on this reading there is no conflict to record, the ● is not carried, and no `SUPERSEDES` line is written. If the owner means to drop the ○ band or the flag, that is a further ruling and needs a `SUPERSEDES` against `governance/tier-system.md` section 8 and `governance/mission-and-epistemics.md` section 2.]
2. **Provisional is a stage; covered means read, extracted and verified.** A reading is provisional until its source has been read again and the information confirmed. A source counts as covered only when that has happened, so a page says "read, none yet verified" while no reading is verified, and lists the jurisdictions whose sources are not yet read as not yet read. [ASSUMPTION: this matches `specifications.state` (`pending`, `provisional`, `stated`) and `has_unverified_sources`; no new field is needed.]
3. **An item page is the specification.** The book's specification and the item pages are the same thing, and it is rendered from the database. [ASSUMPTION: "database directly" is read together with owner ruling OW-1 of 2026-10-29 (third), under which the render table holds the specification rows as prose with bibliographic information drawn from the preceding tables, and with the 2026-08-27 ruling that no committed file is a render. A static generator emitting committed HTML is therefore not restored; the mechanism the ramp session built is not carried, and its requirements are.]
4. **Two lenses.** A page offers an audience lens (designer, disabled person, occupational therapist, policy maker; `governance/audience-priority.md`) and a disability lens (population, ICF code, access need). Only the disability lens was built before. Lens filtering shows its more specific options only after a lens is chosen, and the controls come before the information.
5. **Page content and form.** A master comparison table gives one row per in-scope jurisdiction, alphabetical, with the standard and its edition under the row and the detail one click from the value. Rows with no value are not shown. Evidence is listed alphabetically by first author's last name and regrouped by the chosen lens. One sans typeface, few sizes, and no decoration are the visual direction; the working requirements, with acceptance tests, are `workplan/2026-10-30-ramp-spec-pages/reports/spec-page-design-requirements-2026-10-29.md`, and the owner took the defaults for its open questions Q1 to Q7 ("Use my defaults"). [ASSUMPTION: that file is a working baseline for the renderer, not a ratified specification.]
6. **Accessibility is a precondition.** WCAG 2.2 level AA wins over aesthetics, and navigation legibility is not traded for minimalism. Compliance is never self-certified: a page is described as having passed the tests that were run, on the date and build recorded, and no third-party scan or screen-reader pass has yet been run on any page.
7. **Scope of a page.** The jurisdictions shown are the major identified countries, P1+P2+P3 of the jurisdiction ranking, current editions only. [ASSUMPTION: "P1+P2+P3" is the ranking recorded in `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` section 3.]
8. **Rest landing is the second headline parameter for ramp gradient.** The owner's hypothesis is that the rest landing, not the slope, is the problem, and the owner agreed to add landing spacing as a second headline parameter. Which value is best practice follows item 1: the shortest run between rests found. The ramp session's reading of that figure (Germany, 6 m, from a secondary source) is unverified here.
9. **Two statements are not settled and are not applied as rulings.** (a) A row with no value is not shown, and `governance/mission-and-epistemics.md` requires a pending cell to display `[BEST-PRACTICE-PENDING]` with a gap link. [ASSUMPTION: the two are met together by showing no row and stating the gap, with its link, in the page's Gaps section; no `SUPERSEDES` line is written.] (b) The question line under the title is irrelevant, and the mission document makes questions first-class data. [ASSUMPTION: "irrelevant" refers to the single question line the ramp page carried, not to the questions-led commitment; how questions appear on a specification page is left to the owner.]

**What is unblocked, and what still waits.** A renderer can be designed from items 3 to 7 once the render table of OW-1 exists; the render contract in `RENDER-DECISIONS-AND-PIPELINE.md` section 3 is the starting point. Waiting on the owner: whether the ○ band and flag stay for a gentlest-code value (item 1), the render table's storage and prose-production questions (OW-1b, OW-1c), and item 9. Waiting on a data session: the rest-landing parameter (item 8), which is research content and ships apart from tooling under `CLAUDE.md` rule 10.

CONDITION: any session asking what counts as best practice for a parameter, whether a T4 to T6 value may be named best practice, which value to highlight on a page, what "provisional" or "covered" means, how a specification or item page is rendered or what it must contain, whether the page has an audience lens, what the accessibility bar for a rendered page is, which jurisdictions a page shows, or whether rest-landing spacing is a parameter.
ACTION: (1) Name as best practice the most accommodating value found in the parameter's recorded direction, never the commonest and never by highlighting the steepest code value; keep the ○ band and the weak, code-derived flag for a determination resting on T4 to T6 alone, and do not mark such a value ●. (2) Describe a reading as provisional until a second reading of its source confirms it, and as covered only when read, extracted and verified. (3) Render a specification page from the database, not from a committed file, and take its element-to-table mapping from the render contract; do not restore a static generator. (4) Offer the audience and disability lenses, and write nothing as accessible that has not passed a recorded test. (5) Show only in-scope jurisdictions and no row without a value, stating the gap under Gaps. (6) Mint rest-landing spacing as a parameter through the sanctioned CLI in a data PR of its own, with its direction recorded from an admitted source and not hand-set. (7) Treat every [ASSUMPTION] mark above as unratified.
DATE: 2026-10-30 — owner statements of 2026-10-29 and 2026-10-30, quoted above.



<!-- O49 references/project-standards.md:4869-4883 -->

## Owner rulings 2026-10-30 (second) — the ○ band and flag for a gentlest code value

Given in this session (https://claude.ai/code/session_01Ub36iM8xPEnP9BjGKYZzbV), in reply to the open question at the end of the previous entry, and recorded on contact per `CLAUDE.md` rule 0 and workplan WR-3. The answer is quoted verbatim.

"Yes, keep the ○ band and flag"

**What this does.** The reading is the assistant's and is marked; the owner's words above are the ruling.

1. **Item 1 of the previous entry is ratified.** A determination resting on T4 to T6 alone keeps the weak-band (○) and the weak, code-derived flag with the convergence-not-evidence caveat, under `governance/tier-system.md` section 8 and `governance/evidence-architecture.md` I3, as amended 2026-07-21. The owner's best-practice statements of 2026-10-29 and 2026-10-30 decide which value is named, and do not change the band or the flag. Nothing is superseded, so no `SUPERSEDES` line is written. [ASSUMPTION: "keep" confirms the position of the previous entry's item 1 in full, including that a value of this kind is not marked ●, which the ramp-slope session's page had done.]

**What is unblocked, and what still waits.** The first of the three owner questions in the previous entry is closed. The render table's storage and prose production (OW-1b, OW-1c), and how questions appear on a specification page (item 9(b)), still wait on the owner.

CONDITION: any session asking whether a gentlest code value named as best practice carries the ○ band and the flag, or whether the ramp-slope session's ● for such a value stands.
ACTION: (1) Keep the ○ band and the weak, code-derived flag on a determination resting on T4 to T6 alone, whichever value is named; do not mark it ●. (2) The [ASSUMPTION] mark on item 1 of the previous entry is ratified by this entry; the others in that entry stay unratified.



<!-- O50 references/project-standards.md:4884-4901 -->

## Owner statement 2026-10-30 — radical transparency; present, do not claim correctness

Given in session https://claude.ai/code/session_01Ub36iMDP3HjZ4vtU4HZvDu, in reply to the five questions at the end of the first draft of the render contract for parameters 3 and 12 (`workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md`), and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim, including its lower case:

"i don't know how to resolve the questions for me at this point, but please know that i want to be as radically transparent for my audience as possible while simply PRESENTING information without claiming correctness myself"

The owner then said the questions "may mean that you need an opus antagonist adjudication round to resolve these things". That round was run (a read-only Opus critic against commit `ae692d99`); its findings are in `transcripts/harness_fcb93ff6/subagents/`, and what was repaired is in the contract's section 8.

**What this does.** It restates, in the owner's present words, the posture already ratified in `decisions/DR-2026-07-21-product-posture-thinking-tool-not-authority.md`: every determination is rendered as a figure for thought, "radically transparent about its evidence, its derivation, its disagreements, and its strength flag" and "we never adjudicate a correct path or conclusion". The critic found that DR, and `governance/held-tensions.md` T5 and its binding that no session may resolve a held tension, after the first version of this entry had missed them.

1. **Supersession.** None is claimed. The statement agrees with the ratified posture, so there is no `SUPERSEDES` pair. [ASSUMPTION: it is read as reaffirming the posture and not as retiring any of the ratified texts that use the phrase "best practice" with a marker (`governance/evidence-architecture.md` section 6, the Core Doctrine marker rule in this file, `governance/mission-and-epistemics.md`). If the owner means it to reach those, they have not said so, and that needs a decision record, not a session's reading.]
2. **The questions.** The statement is a deferral: the owner does not know how to resolve them. It does not delegate them. The assistant's positions on them are proposals in the contract's section 8, unratified, bound to nothing. The audience lens is answered by the entry above (item 4: a page offers both lenses), which the critic's finding about held tension T5 anticipated. One of the five stays with the owner: OW-1b, whether and by whom a source's sentence may be translated or rewritten.
3. **OW-1b and OW-1c** stay open on the owner's browser page until the owner answers them.

CONDITION: any session writing or reviewing the wording of a rendered page, a render record, or a template that turns a specification or an extraction into prose; any session asking whether a page may recommend, endorse or call a value correct.
ACTION: (1) Apply the ratified posture of DR-2026-07-21 as the owner's present words restate it: describe and attribute, show the derivation and the strength flag and the disagreements, never adjudicate a correct path. (2) Treat the contract's section 8 positions as the assistant's proposals, and every [ASSUMPTION] mark above as unratified.
DATE: 2026-10-30 — owner statement, quoted above.



<!-- O51 references/project-standards.md:4902-4921 -->

## Owner rulings 2026-11-06 — minimise code; no net-negative requirement

Given in this session (https://claude.ai/code/session_01Ub36iMkXnQsEwzR9oaTqn1), in three messages after the gap register for the two pipeline batches was filed and handed to an analyst, and recorded on contact per `CLAUDE.md` rule 0. Each is quoted verbatim, including its lower case:

- (question) "net negative rule? that is supposed to be reserved for minimizing code infrastructure?"
- "we want to MINIMIZE code wherever possible. we don't require a net negative because the extreme of that means we end up with no code"
- "we want the bare essentials in the most code efficient manner possible so that we are agile and lean"

**What this does.** The readings are the assistant's and are marked; the owner's words above are the ruling.

1. **The standing constraint is minimal code, not a shrinking total.** The 2026-10-12 direction (as little code as possible) stands and is sharpened to the bare essentials written as efficiently as possible. The net-negative requirement that operationalised it (a PR touching `scripts/`, `schemas/`, `.github/` or `skills/` may not raise their line total without naming the exception) is not required. [ASSUMPTION: the net-negative bullet is read as a rule about code infrastructure only, as the owner's question puts it, so it never applied to research rows, owner decisions, doctrine or prose.]
2. **What stays.** The tests of `CLAUDE.md` section 8 that need no count: before adding a check, script or table, state what wrong thing reaches the guidebook without it; nothing is added without naming what reads it. [ASSUMPTION: "wherever possible" is a standing preference weighed case by case, not a gate, so a defect that reaches the guidebook is still fixed with the smallest code that closes it.]
3. **Supersession.** The net-negative bullet of `CLAUDE.md` section 8 is rewritten in place, as that file's own rule directs (fix the sentence, put the account in the commit message). No `SUPERSEDES` pair is written for it: the audit anchors on a target quote that must still occur once, and the sentence it would quote no longer exists. The simplification plan's W3 (`workplan/2026-10-12-simplification-workplan.md`) and the "net-negative" item of the standing constraints and W1-W10 list in `workplan/2026-10-23-pipeline-resolution-workplan.md` restate the old bullet; they are plans, left as written, and this ruling governs where they differ.

**What is unblocked, and what still waits.** Nothing waits on the owner. The Opus resolution analysis of GAP-074 to GAP-096 was told of the ruling and is to classify each tooling recommendation as close-as-accepted, rule or prose, reuse, delete or new code.

CONDITION: any session writing or reviewing a PR that touches `scripts/`, `schemas/`, `.github/` or `skills/`, or asked whether a change must reduce the line total.
ACTION: (1) Do not require or claim a net-negative total. Name what the added code reads and what wrong thing reaches the guidebook without it, and name any code it replaces or makes deletable. (2) Try, in order: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. (3) Treat every [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O52 references/project-standards.md:4922-4942 -->

## Owner rulings 2026-11-06 (second) — OR-1c, the identity lens ALL, and the type of a government report

Given in this session (https://claude.ai/code/session_01Ub36iMkXnQsEwzR9oaTqn1), in reply to the first three questions of the owner-decision sheet in `scratchpad/session_2026-11-06-pipeline-batch-2/resolution-analysis-GAP-074-096.md` (section B), and recorded on contact per `CLAUDE.md` rule 0. Each answer is quoted verbatim, including its lower case:

1. OR-1c: "link table unless that is more prone to errors"
2. The lens for a clause under a disability heading: "ALL is a generic? what do you even mean? ALL implies it is just good design, not that it is accessible design in particular as it doesn't map to a particular group. I guess we can see it as a universal?"
3. The type of a government report: "if government report is academically sound then it can be t3 I think"

The owner then asked that every fix be queued for a later session, and that the work be committed, merged and closed.

**What this does.** The readings are the assistant's and are marked; the owner's words above are the ruling.

1. **OR-1c.** A link table: a figure is written once and a separate table lists the combinations of codes it concerns. The owner's condition was that the link table not be more error-prone. The assistant measured the alternative: one row per identity and ICF combination would turn the identity-tagged figure rows into many more rows each repeating the same value and quote (`python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);m=dict(c.execute('select identity_code,count(*) from identity_icf_map group by 1'));r=c.execute('select identity_code,count(*) from source_value_extractions where identity_code is not null group by 1').fetchall();print(sum(n for i,n in r),sum(n*max(1,m.get(i,1)) for i,n in r))"`; measured 2026-11-06: 212 rows become 1608 on identity and ICF alone, before access needs). The link table's own error, an orphan link row, is already caught at apply time, because `scripts/migrate_db.py` snapshots `PRAGMA foreign_key_check` before and after a migration and fails on a new violation. [ASSUMPTION: that measurement settles the owner's condition; if the owner reads it otherwise, OR-1c reopens.] The shape of the table, and what happens to the four lens columns already on a figure (a column a committed data migration inserts can never be dropped, so retire writer, then reader, then NULL forward), are the tooling PR's.
2. **The lens ALL.** `ALL` in this project is a scope marker, not a population: `governance/population-taxonomy.md` section 1.3 says it "means this specification applies to all populations", for example Universal Mode code compliance values and universal design principles, and the database describes it as "Item is not population-specific; applies to everyone". The owner reads it as a universal, good design for everyone, which names no particular group and so is not accessible design in particular. [ASSUMPTION: this is read as: a provision written as accessible design, from an accessibility code or a study of disabled people, is not tagged ALL merely because its sentence names no group; it carries the group or groups it serves, and ALL is kept for provisions that are universal good design. The owner hedged ("I guess"), so this is not a final ruling on MOB against ALL for a clause under a disability heading, and one question stands: confirm the reading.] If the reading holds, the sentence of `governance/population-taxonomy.md` section 1.3 naming "code compliance values (e.g., minimum corridor width per code)" as a typical use of ALL is overtaken; no `SUPERSEDES` pair is written because the answer is hedged. Which group a provision carries is judgment's output, filled with the link table of item 1, where one figure can carry several groups. OR-1b is unchanged: a figure tagged ALL reaches only an ALL determination.
3. **A government report.** A government report that is academically sound may be tier 3. [ASSUMPTION: "t3" is tier 3; "academically sound" is the test OR-5 already uses for a Co-1 source; the answer takes the option "stay `grey`, tier 3" and rejects reclassifying to `clinical` and a new route to tier 1.] REF-00468, REF-01005 and REF-01008 stay as filed. The line of `governance/tier-system.md` that lists `grey` as "occasionally" tier 1 for unpublished primary research is the text this answer leaves in tension; correcting it is queued as a doctrine change and not made here. Whether a given report is academically sound is judged per source and is not decided by this entry.

**What is unblocked, and what still waits.** OR-1c is answered, so the lens-routing change (T-3) and the tagging of existing rows (D-2) can be designed, as a tooling pull request first. The tier of REF-00468 is settled as filed. Waiting on the owner: the confirmation in item 2, and the five other questions of the sheet (the term for a width at a turn, sub-national instruments, adversarial pass 7, a library route for six papers and BS 8300, in-place correction of a locator).

CONDITION: any session designing the lens-routing change or filling lenses on figures (T-3, D-2), writing a lens on a figure from an accessibility code or a study of disabled people, or typing a government report.
ACTION: (1) Carry several codes of one model on a figure by a link table; do not write the figure once per combination. (2) Do not tag a provision from an accessibility code ALL because its sentence names no group; leave the tag to the lens fill and treat ALL as a universal-design marker, until the owner confirms or corrects item 2. (3) Keep `grey` government reports that are academically sound at tier 3; do not reclassify them to `clinical`. (4) Treat every [ASSUMPTION] mark above as unratified.



<!-- O53 references/project-standards.md:4943-4956 -->

## Owner instruction 2026-11-06 — retire workplan-orchestrator; /run-pipeline replaces it

Given in session https://claude.ai/code/session_01Ub36iN9Wtnk3RfPq2ogN3U and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim:

"please retire workplan orchestrator. please create a new skill in its place called /run-pipeline (which includes a variant for processing evidence and beyond without research)"

Supersession, recorded here and at the superseded text: the RULE headed "Session start protocol (GraphQL batch read: LATEST + project-standards + workplan-orchestrator …)" and the RULE "Do not re-read workplan-orchestrator_SKILL.md mid-session" are SUPERSEDED, and the two RULEs that send a reader to the deleted skill's "§Population Codes" and "§CO-0004 Part Numbering Map" are AMENDED (each carries a marker line pointing here). This is stated in prose, not in the audited `SUPERSEDES:`/`BY:` grammar, because that grammar counts its target quote in the target file's raw text, which for a ledger-internal target includes the citation line itself and so can never equal one. The skill they name no longer exists; `/session-open` and `/orient` open a session. The decisions-register copies D-0058 and D-0065 stay `ACTIVE` until a data-only PR marks them SUPERSEDED (CLAUDE.md rule 10 keeps data migrations out of a tooling PR; the SQL is written and waits for that PR).

**What this does.** `skills/workplan-orchestrator_SKILL.md` is deleted. Its risk-escalation rule (two or more escalation signals append a REVIEW gap) is **not carried**: it was unexecutable before the deletion (the signals were never defined anywhere in the repository, and `REVIEW` is not a `gaps.category` value), and the mechanisms that now exist, `add-gap`, `raise-determination-gate` and the closing adversarial pass, do the work it named. [ASSUMPTION: the owner's retirement instruction is read as not wanting it re-homed.] Its population-code table is replaced by `base_taxonomy_identity`. The dangling live references were corrected in the same change (`governance/project-instructions-v10_14.md` skill list, `governance/population-taxonomy.md`, `references/skill-registry.md`, `references/effort-guide.md`). Frozen historical records that name the skill (the armature documents, `architecture/sqlite-data-layer.md`, dated workplans and audits) are left as the record of their time.

CONDITION: any session asking which skill orchestrates a multi-stage run, or what runs at session start.
ACTION: Use `/run-pipeline` (variant `from-evidence`) for a multi-stage run and `/session-open` then `/orient` to start a session; do not look for `workplan-orchestrator`.
DATE: 2026-11-06 — owner instruction, quoted above.



<!-- O54 references/project-standards.md:4957-4974 -->

## Owner statements 2026-11-06 — the minimum code that is correct, one value per cell, more columns

Given in session https://claude.ai/code/session_01Ub36iN9Wtnk3RfPq2ogN3U and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim:

"you can add columns. another session has pointed out that there is an erroneous "net negative" rule which taken to extreme means we have no code. what I mean is for there to be the minimum code possible to perform the action correctly such that we are lean, agile and centralize data which in turn means we minimize errors and breaks and detritus"

"tables and columns must be as clearly organized as possible. we do NOT want to have data joined in cells that will cause issues further down the pipeline or have data stored in the wrong cell"

"more columns = more specificity = more flexibility imo"

Relation to the entry above ("Owner rulings 2026-11-06 — minimise code; no net-negative requirement"): that entry records the same objection to the net-negative requirement from earlier messages and rewrites `CLAUDE.md` §8 in place; nothing here supersedes it. This entry adds what it does not carry: that the standard is the minimum code that performs the action *correctly*, that data is centralised so errors, breaks and detritus are minimised, and the column and cell principles.

**What this does.** `CLAUDE.md` §8's "Minimise code" bullet carries both entries' wording (a writer that refuses what it should, a typed column in place of a convention and a test that can go red are not waste), and §4 gains the schema-shape rule. The census that shows what the rule finds on the live schema is a command, not a list: `python3 scripts/audit/joined_cells_census.py` (text columns whose values parse as JSON, or as short delimiter-joined tokens, or carry an appended `|| CORRECTED` correction; a report that exits 0 and prints `EXAMINED`). [ASSUMPTION: the owner's "another session" is the session that raised the same objection; no ruling of that session is relied on.] Migrations 119 and 120 apply the rule to what this change touched: `source_value_extractions.harm_finding` and `search_executions.absence_class` (states that were prose), and `connection_targets` with one typed foreign-key column per kind (it was one cell whose meaning depended on a prefix). The classes the census found that this change does not touch, and which want their own tooling PR and adversarial pass because the determination engine reads them: JSON lists that are the second home of a junction table (`convergence_assessment.*_sources`, `specifications.governing_refs`), JSON and delimited lists elsewhere (`search_executions.terms_used`, `citation_mining.connections_produced`, `adversarial_passes.reviewer_models` and `author_models`, `access_needs.absorbs`, `source_locators.authors` and `used_in_bpcs`, `research_code_leads.clause`), and corrections appended inside a note (`search_executions.findings_note`, `gaps.description`, the notes the amend verbs append to).

CONDITION: any session adding or changing a table or column, or asking whether a PR may add code or columns.
ACTION: (1) Judge code by whether it is the minimum that performs the action correctly, not by line count; add a column where a convention would otherwise carry a fact. (2) Put one value in each cell and each fact in the cell that names it: a foreign key where a table exists, a row per repeated value, never a list, an array or a prefixed string. (3) Before shipping a schema change, run `scripts/audit/joined_cells_census.py` and do not add a cell it would flag.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O55 references/project-standards.md:4975-5004 -->

## Owner statements 2026-11-06 — the pipeline skill's requirements

Given in session https://claude.ai/code/session_01Ub36iN9Wtnk3RfPq2ogN3U and recorded on contact per `CLAUDE.md` rule 0, as the requirements `skills/run-pipeline_SKILL.md` implements. Quoted verbatim:

"do we have a skill that manages the process of performing research then processing it throughout every stage of pipeline followed by doing an adversarial audit for accuracy, logic, sequence?"

"base > research > evidence > judgment > synthesis > specification > render

please retire workplan orchestrator. please create a new skill in its place called /run-pipeline (which includes a variant for processing evidence and beyond without research)

research: must be performed by topic across languages and jurisdictions while tracking its queries. must be able to perform citation mining. must be able to record evidence from a source that pertains to other categories/topics/parameters to maximize search efficiency, which means that every research row for a source must list all different categories/topics/parameters found within that source. this means that a research session may search by a given slug for sources, but the actual review of any source will concern every single thing relevant to accessible design as per the reference tables in base / at suggestion of Claude while ensuring that equivalencies are found to prevent duplication. all relevant bibliographic data must be recorded.

evidence stage must carefully adjudicate sources to assignrelevant populations/access needs/ICF codes properly referenced, and the evidence needs to be stored in such a manner where it can be used to inform synthesis+specifications as well as be able to be used directly by rendering.

synthesis will ensure the use of cross referential analysis for table rows to see if there are any relevant links within parameters/topics/categories (eg wheel chair swept path analyses for different wheel chairs would inform different space requirements)

specifications: must be able to review all evidence and syntheses of evidence to determine what best practice is, which explicitly means the most accommodating/gentle/dignified set of values/rationales/solutions for a given specification item within a category. the most commonly seen value/etc is NOT evidence of best practice but most common practice. must be able to understand code is a floor unless backed up directly by high value evidence, and we are more likely to see best practices coming from academic research/professional clinical guidelines/advocacy groups.

renders: must be able to process specifications to be readable for a webpage, must be able to compile all evidence in tables for comparison, must be radically transparent in approach, must ensure proper bibliographic citations, etc."

"(rendering step should refer to recent PRs that concerned the webpage display of a specification item)"

"if code documents are the only things that inform a specification, then they can be best practice...it's just going to be a weaker evidence tier"

**What this does.** It records, in the owner's words, the stage requirements the new skill follows and the audit dimensions (accuracy, logic, sequence) that migration 118 gives the adversarial pass a lens for. Nothing is superseded: the last statement agrees with the ratified position of the two 2026-10-30 entries (a determination resting on T4 to T6 alone is named at the weak band, with the code-derived flag, and never marked full). [ASSUMPTION: "evidence stage ... assign relevant populations/access needs/ICF codes" is read as the judgment stage, where `CLAUDE.md` section 6 places the lens crossing (owner, 2026-08-27); `skills/run-pipeline_SKILL.md` says so and names the cost of moving it. The owner's omission of a judgment stage from the requirement list is read as the same collapse.]

CONDITION: any session asking what the pipeline-orchestration skill must do, how each stage is to be run, or whether the adversarial pass covers sequence.
ACTION: Follow `skills/run-pipeline_SKILL.md`; change it by ledger entry, not by session preference.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O56 references/project-standards.md:5005-5032 -->

## Owner statements 2026-11-06 — the old item subjects are admitted as a basis for the base vocabulary; the base must serve every P1+P2+P3 language; Opus plans the population

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9 after a read-only review of the base tables (`scratchpad/session_2026-11-06-base-vocabulary-review/base-review.md`, PR #213), and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim; the first two arrived mid-turn.

On language and jurisdiction scope:

> "these base tables, as per our aliases and native terms and translations and multilingual and multijurisdictional requirements etc, must work across all languages that we have defined for this current edition of project (the p1+2+3, I think it's called, for the initial countries to focus on)"

On prior work:

> "we should have some work already done based upon previous editions of this project and those listed specification items"

On the question the review put (whether the 93 item subjects, value-stripped, may be admitted as a catalogue for prepopulating parameter names, overriding the 2026-10-09 exclusion):

> "great work. yes, use the 93 items with stripped values as a basis. with your criticisms in mind, have Opus plan out a strategy with which to populate the base tables and address all listed issues such that we have a truly comprehensive international project without English bias"

**What this establishes**

1. **The 93 item subjects are admitted as a basis.** This reverses, for the pre-reset `items` names only, the 2026-10-09 clause that the old Part 4 item names "are not a permitted source" (the entry "Owner statements 2026-10-09 — every source is scanned for every parameter…", item 3). The mark of that supersession is this item: the back-pointer grammar cannot mark a clause that sits in this ledger.
2. **What "basis" does not do.** It does not mint anything. The guard the owner chose on 2026-10-09 stands: "Screen, then you approve". Each candidate is screened (no digit, comparator or min/max word, no old item code, not already held) and listed in one table with the item it came from, and the owner approves that table in a further dated entry before any term is minted. [ASSUMPTION: "use … as a basis" means a source of candidate names under that guard, not an approval of the names, and not a licence to file findings into the old item containers. The deletion of the item layer (2026-09-01) stands; an item subject is a lead for a quantity, never a container.]
3. **A route is owed.** `terms.catalogue`'s CHECK already admits the pre-reset corpus file, but `_resolve_catalogue_entry` resolves it for `terms:<TERM-ID>` only. Admitting the item subjects needs a resolver and no schema change, and it ships as a tooling-only pull request before any name is minted (`CLAUDE.md` rule 10).
4. **The language scope is P1+P2+P3.** The base tables, aliases, native terms and translations must work across every language those jurisdictions require. [ASSUMPTION: the set is the one recorded in `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` section 3 (US UK AU CA DE NO SE ISO EU; FR CH NL DK FI BE IE ES IT PT; JP SG NZ KR CN), which the owner confirmed on 2026-10-30 ("Yes it is P1+P2+P3"), giving the 14 languages `lang_jur_map` pairs with them. The 2026-10-29 OR-12a scoping-out of Arabic, Bengali, Hindi and Swahili is not touched by this statement.]
5. **Opus plans.** An Opus-class planner writes a strategy to populate the base tables and to address the review's listed issues (the parameter list at ten rows, the unverified and English-biased alias layer, the English-only ICF, identity, need and room tables, the empty medical lens, the missing topics). The plan is a proposal: it approves nothing and writes no rows.

CONDITION: any session asking whether the 93 old item names may seed parameters, whether item subjects are still excluded as a source, whether the base vocabulary must cover the P1+P2+P3 languages, or who plans the population of the base tables.
ACTION: (1) Treat the pre-reset item subjects, value-stripped and with their codes removed, as a permitted source of candidate names, never as containers. (2) Mint no name from them before a tooling pull request adds the catalogue route and the owner approves the screened table in a dated entry. (3) Build base vocabulary, aliases and native terms for every P1+P2+P3 language, with in-language provenance (R11); never treat an English term translated word for word as a native term. (4) Treat every [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O57 references/project-standards.md:5033-5067 -->

## Owner statement 2026-11-06 (second) — every recommendation of the base-population plan is applied

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9, in reply to the plan `scratchpad/session_2026-11-06-base-vocabulary-review/base-population-plan.md` and its section E of twelve owner decisions, and recorded on contact per `CLAUDE.md` rule 0. The whole message:

> "apply all recommendations, carefully infer and apply all solutions from my rulings and context required for pipeline to operate, etc"

and, in a message that arrived while the first was being worked on:

> "e1 e3 e4; Appy yes"

[ASSUMPTION: "Appy" is "Apply". The second message names the three items that block the first tooling pull request, E1, E3 and E4, and says yes to each; it is read as confirming their recommended options specifically, so those three do not rest on the blanket reading below.]

**What this decides.** Each decision of the plan's section E is answered by the option the plan marked as recommended, as the plan words it. [ASSUMPTION: a blanket "apply all recommendations" is read as choosing the recommended option of every E-item other than E1, E3 and E4 (which the second message names), including the three of those the plan marks DG-NON (E5 licensing, E6 population taxonomy, E7 jurisdiction), because the owner is the one who decides those and has now decided. It is not read as approving the screened table of item subjects, the mints, the declinations or the stakes table themselves: each of those is a table the owner has not yet seen, and the 2026-10-09 guard ("Screen, then you approve") and the plan's E9 still require the owner's approval of the table before any row is written.]

| Item | Answer applied |
|---|---|
| E1 (DG-NON) | A concept first met outside English is named by the instrument's own phrase, in its own language, until an English-language instrument of a P1+P2+P3 jurisdiction is observed naming the same concept. No English gloss is typed (OR-17). |
| E2 | The four terms that carry a name no source used (TERM-090, TERM-092 and the two others the plan's D9 finds) are renamed to the observed phrase, in a research pull request, after the tooling merges. TERM-091 (parameter 12) is among the four the plan names; its rename needs the owner's quote on that parameter and is not applied here. |
| E3 | The 93 item subjects are pointed at by row number in the pre-reset database (`items:<rowid>`); no old item code appears in a live row. |
| E4 (OR-17b) | The model-generated and unrecorded aliases stay as flagged search aids, never vocabulary, and are not deleted; each becomes vocabulary only when an instrument in its language is read and the phrase is found there. |
| E5 (DG-NON, licensing) | WHO titles in other languages: store the pointer to the persisted payload only, until the licence is read from WHO's own terms. |
| E6 (DG-NON, population taxonomy) | The base may record each language community's own designation for an identity code, attested in its own Co-1 sources, beside the English name. No identity code changes; a gap stays visible. |
| E7 (DG-NON, jurisdiction) | Norwegian is split into Bokmål and Nynorsk only where an instrument is published in both; other official languages of in-scope countries stay out of scope for now. |
| E8 | Rooms are frozen until a page reads them. |
| E9 | The model proposes a `typical_stakes` for each need that lacks one, with its warrant, in one table; the owner approves that table before any row is written. |
| E10 | This edition relies on attestation from codes alone; no named native-speaker reviewer is required. |
| E11 | The language-and-jurisdiction pairs that `lang_jur_map` holds for P1+P2+P3 are approved as the bucket members of OR-8. The count is derived, not quoted. |
| E12 | The functional-axis terms and the method terms are declined as parameters, each with a reason, and kept as terms. No taxonomy change. |

**What it asks of the pipeline.** "Apply … context required for pipeline to operate" is read as: build the tooling the plan names (its T1 to T4) in a tooling-only change before any row is written (`CLAUDE.md` rule 10), keep the ledger and the instrument consistent with the answers above, and stage the research that follows. It authorises no row.

CONDITION: any session asking how a concept first met in a non-English instrument is named, whether the unattested aliases are vocabulary or may be deleted, whether item subjects are pointed at by code or by row, whether WHO titles in other languages may be stored verbatim, whether identity labels in other languages may be recorded, whether Norwegian is split, whether rooms are populated, whether the P1+P2+P3 language-and-jurisdiction pairs are approved bucket members, or whether the axis and method terms are parameters.
ACTION: (1) Name a concept first met outside English by the instrument's own phrase and language; never type an English gloss. (2) Treat the unattested aliases as flagged search aids and delete none. (3) Point at item subjects by `items:<rowid>`. (4) Store a pointer to a persisted payload, not a verbatim non-English WHO title, until the licence is read. (5) Record a community's own identity designation only when attested in its own Co-1 source; change no code. (6) Leave rooms alone. (7) Treat the P1+P2+P3 pairs as the bucket members. (8) Decline the axis and method terms as parameters with reasons, in a research change after the tooling merges. (9) Write no row from the item subjects, the stakes proposal or the renames until the owner approves the table in a dated entry. (10) Treat every [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statement, quoted above.



<!-- O58 references/project-standards.md:5068-5105 -->

## Owner statements 2026-11-06 (third) — the register is written in English first, then translated to search each language; it must not be English-biased

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9 while the RHFAC Rating Survey v4.0 and the CSA/ASC B651 listing were being catalogued, and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim; times in session order.

> "we have categories according to the kind of technique (acoustic, circulation, etc) as well as categories according to building typology and room"

> "and these cross-pollinate each other"

> "what appears in a category specification for type (eg circulation, acoustics) will appear in building typologies and rooms and vice versa"

> "you don't need French edition here"

> "what I mean is that you will build out a comprehensive register of concepts/items/terms/techniques but you have to ensure that you research them across all of our chosen jurisdictions and languages without an English bias"

> "so we are doing prep work to get this all written out in English and then we have to translate it all properly into other languages to search them too"

and, replying to the session's reading of those statements (that a translation is a flagged search seed, and the register also takes concepts from native-language readings):

> "yes"

> "we set up the base and in turn we set up the research coverage"

[ASSUMPTION: "yes" answers the session's reading in point 3 and 4 below; "we set up the base and in turn we set up the research coverage" is read as: the base register is the list the research coverage is derived from, concept by language-and-jurisdiction pair, and coverage is never kept as a second list.]

**What this establishes**

1. **Two category axes that derive from one set of rows.** A technique category (acoustic, circulation …) and a building typology or room are two views of the same criteria. Whatever sits in a technique category appears under the typologies and rooms that use it, and the reverse. Neither view is maintained beside the other (`CLAUDE.md` rules 5 and 8): both are generated from one table of tagged criteria.
2. **English first, as preparation.** The English register is the search plan, not the vocabulary. It is not definitive: the RHFAC survey is a Canadian rating instrument that scores criteria by points and states no values, and the B651 text was not obtained.
3. **Translation is for searching.** A translation of the English register is a search seed, produced to be in use in the jurisdiction and not word for word ("properly"), and recorded as model-generated and flagged, which is what OR-12b permits. It is not a term, not an alias and not evidence. It becomes vocabulary only when an instrument of that language is read and the phrase is found there (E4; OR-17; R11).
4. **The register must not end where English ends.** A concept English does not carve out cannot be reached by translating English. The register therefore also takes concepts from native-language open passes over each P1+P2+P3 instrument (OR-13; plan C.3), named by the instrument's own phrase (E1), and records, per concept and per language-and-jurisdiction pair, whether it was searched and what was found, including absence.
5. **The French RHFAC edition is not used here.** It was retrieved before this statement and is persisted in the retrieval log; nothing is drawn from it.

[ASSUMPTION: "translate it all properly" is read as OR-12b's generation of in-use, jurisdiction-specific terms for flagged searches, and not as licence to store translations as vocabulary; the owner's earlier OR-17 ("It is not acceptable for the model to generate its own phrases/names/aliases") and E4 are not read as withdrawn.]

CONDITION: any session asking whether the English register may be translated into other languages, what a translation of it is, whether it may be stored as aliases, how a concept English does not name enters the register, or how technique categories relate to building typologies and rooms.
ACTION: (1) Generate both category views, and the research coverage, from the base register and the tagged table; keep no second list. (2) Treat every translated term as a flagged model-generated search seed, never as vocabulary. (3) Promote a seed only by reading an instrument in its language and finding the phrase there. (4) Feed concepts found in native-language readings back into the register by the instrument's own phrase. (5) Treat every [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O59 references/project-standards.md:5106-5117 -->

## Owner statement 2026-11-06 (fourth) — the project may hold retrieved standards in the repository

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9, after the session had kept the CSA/ASC B651:23 PDF out of git because its legal notice says users may not "make an electronic copy", and recorded on contact per `CLAUDE.md` rule 0. The whole message:

> "oh fuck off with the "no electronic copy". we are doing a not for profit volunteer advocacy project. this is fine"

**What this decides.** The project may persist retrieved copies of standards and codes in `retrieval-log/` under research rule R10, a publisher's "no electronic copy" notice notwithstanding. The session's earlier exclusion of the B651 PDF is withdrawn and the file is committed with the other retrieval artefacts. [ASSUMPTION: this is read as a ruling on holding retrieved copies for the project's own verification, as R10 requires; it is not read as a ruling on republishing or rendering any standard's text in the book, which stays a separate question for licensing (`CLAUDE.md` section 8: licensing is the owner's).]

CONDITION: any session asking whether a retrieved standard whose legal notice restricts copying may be persisted in the repository.
ACTION: (1) Persist it in the retrieval log like any other source. (2) Do not treat a publisher's copying notice as a reason to withhold a source from verification. (3) Raise republication or rendering of such text as a separate question. (4) Treat the [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statement, quoted above.



<!-- O60 references/project-standards.md:5118-5139 -->

## Owner statement 2026-11-06 (fifth) — log where a large source was retrieved from; do not commit the file

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9, on seeing that the pull request had grown to over a hundred thousand lines because the retrieved files were committed, and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim; the first two messages preceded the third.

> "110k is...high?"

> "ohhh it's from retrieving"

> "well, we don't need to actually commit these large PDFs etc. we just need to log where we retrieved from ie the url"

and, in two further messages:

> "we don't need to be saving these PDFs in repo just tracking where they can be found for reference which is our version of persistence"

> "otherwise you're going to blow the context tokens etc. just record page number and line if need be too"

**What this decides.** For a retrieved PDF, web page or full-text extraction, the record kept in the repository is the manifest line (URL, retrieval time, status, byte count, sha256), not the file. This narrows the fourth entry of the same day, which let the project hold a standard in the repository: the project may, but need not, and for large files does not. [ASSUMPTION: "large PDFs etc." is read as PDFs, HTML pages and the text extracted from them (the `text/` folders of the terminology passes); a small structured payload such as an API response keeps the existing convention and stays committed. A source whose admission is logged against a search (`log-search --artefact`) is checked by `retrieval_log.check_artefact_link`, which looks for the artefact; where that check applies, the artefact stays committed and this entry does not reach it.] The files stay on the machine that fetched them until it is reclaimed; the URL and sha256 let any reader fetch and compare them. Persistence, in the owner's words, is tracking where a source can be found; a locator is the page number and, where needed, the line.

CONDITION: any session asking whether a retrieved PDF, page or extracted text is committed, or what the repository keeps of a retrieval.
ACTION: (1) Keep the `retrieval-log/` manifest line; do not commit large retrieved files or text extracted from them. (2) Commit an artefact that a search-execution or admission gate must find. (3) Treat the [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O61 references/project-standards.md:5140-5175 -->

## Owner statements 2026-11-06 (sixth) — a concept is an equivalence class of forms, for every term researched

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9, on reading the English-variants pass's report that a held alias ("handicapped parking") did not occur in its jurisdiction's code, and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim, in order:

> "handicapped parking is still accessible parking stall etc"

> "*also"

> "there are lots of equivalencies"

> "barrier free parking"

> "accessibility parking, disabled parking,"

> "this kind of equivalency finding is applicable for all terms researched"

> "inclusive, universal"

> "wheelchair friendly etc"

> "an elevator is a lift"

> "there is a lot of conflation in literature"

**What this decides.**
1. **The unit of the register is an equivalence class.** A concept has many surface forms per language and jurisdiction. "Accessible parking stall", "handicapped parking", "barrier free parking", "accessibility parking" and "disabled parking" name one concept, and the held instruments add "designated accessible spaces" (RHFAC 1.1) and "designated accessible parking" (CSA/ASC B651:23, clause 9.4).
2. **Non-occurrence in an instrument does not invalidate a form.** Attestation in a code establishes that form as that code's term; it does not decide which other forms are valid equivalents. A form the code does not use is "not attested by these texts", and the sources that could attest it are statutes, road-sign and signage manuals, municipal and advocacy guidance, and ordinary public usage.
3. **Every term researched gets equivalence-class discovery**, not only the first form found. Each form carries its usage type (code term, colloquial, regional variant, outdated or disfavoured, product name) and its attestation (instrument phrase with locator, another source, an owner-supplied form, or an unattested seed). A disfavoured form is recorded with a usage note and not deleted, because people still search with it.
4. **The umbrella adjective is itself a class.** "Accessible", "barrier-free", "inclusive", "universal" and "wheelchair friendly" are offered as interchangeable qualifiers of the same noun ("… parking", "… washroom", "… entrance"). [ASSUMPTION: they are equivalent as usage and unequal in scope. "Wheelchair friendly" addresses wheelchair users only, and "universal" and "inclusive" have a general-population sense outside this project, where they always mean inclusion of persons with disabilities (`CLAUDE.md` section 9). The register records each with a scope note instead of collapsing them, and a code's own umbrella word (for example Norwegian "universell utforming", German "barrierefrei", Finnish "esteetön") is the instrument's term.]
5. **Conflation is recorded, not resolved.** The literature uses one form for several concepts and several forms as though they were one (the qualifiers above; "lift" for an elevator and for a platform lift; "ramp" for a slope threshold and for a device). Equivalence is therefore judged per occurrence, by the sense the source gives the form, never by the form alone (the pilots' rule: a text match is not a sense match). Where a source conflates, the register records a conflation note with its locator and does not settle it by fiat.
6. **This does not widen what may become vocabulary.** OR-17 and E4 stand: a form enters the base as an attested alias only when a source in its language is read and the phrase is found there. An owner-supplied form is a seed marked as owner-supplied until a source attests it. [ASSUMPTION: the owner's examples are supplied in English; forms for the other languages are found by the passes, not translated from these.]

CONDITION: any session asking whether an alias that no code uses is wrong, whether one form or several names a concept, how a disfavoured or colloquial form is handled, or whether equivalence-finding applies beyond the first example.
ACTION: (1) Research every term as an equivalence class, with usage type and attestation per form. (2) Do not treat "not found in the instrument read" as a defect of a form. (3) Keep disfavoured forms with a usage note. (4) Promote a form to an attested alias only on a source's own use of it. (5) Treat the [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O62 references/project-standards.md:5176-5199 -->

## Owner statements 2026-11-06 (seventh) — the base grounds itself; base vocabulary is not verified and stored in evidence

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9, after the session had proposed admitting about a hundred instruments as `evidence_sources` so that base aliases could be attested through `observed_terms`, and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim, in order:

> "we are working on the base to create a comprehensive multilingual multijurisdictional matrix of terms/concepts that can be leveraged by research"

> "none of the work in base needs to be verified and stored in evidence."

> "base grounds itself."

> "the only thing that we need to do is ensure that our matrix works properly so that we have proper coverage across all these languages and jurisdictions"

> "so long as we can confirm that we have correct coverage, we are fine"

**What this decides.**
1. **The base is the matrix and is self-grounding.** A base cell (a concept, a language, a jurisdiction, a form) carries where it was found, in the base's own columns: the source's URL and, if need be, page and line (this extends the fifth entry of the same day: "just record page number and line if need be"). It does not point into the evidence stage, and nothing in the base waits on a source being admitted, a quote being verified in a saved file, or an observation being adjudicated.
2. **This supersedes, for base vocabulary only,** the route the 2026-10-09 ledger entry and migration 125 set up: an attested alias reached through `observed_terms` and `evidence_sources` (`db.py add-alias` requires an adjudicated observation whose quote verifies in a file saved for its source). That route stays for evidence-stage reading of a source for a parameter (the scan contract); it is no longer the way a base alias or term is grounded. [ASSUMPTION: "none of the work in base needs to be verified and stored in evidence" is read as releasing base vocabulary from the evidence stage's admission and quote-verification, not as withdrawing the rulings that a form is something a source actually uses (OR-17; E4): a form still carries the URL and locator where it was found, and a model-generated form with no source is still flagged as a search seed.]
3. **The acceptance test is confirmed coverage.** The matrix is accepted when coverage across every language and jurisdiction can be confirmed as correct, which means a coverage measure derived from the base itself (concept by language-and-jurisdiction column), not a list kept beside it. [ASSUMPTION: "correct coverage" is read as a derivable measure that distinguishes a cell that has a form, a cell searched with none found, and a cell not yet searched; the stopping rule for "proper" is derived, not a hand-set number.]
4. **Consequences left open for the owner's schema decision:** whether the base cell's source columns go on `term_aliases` or on a new matrix table; what happens to `term_aliases.observation_id` (migration 125); and how a concept first met outside English is held (`terms.canonical_en` is required). A design is being prepared (`scratchpad/session_2026-11-06-base-vocabulary-review/matrix-design/`); it approves nothing.

CONDITION: any session asking whether a base term or alias must be admitted as evidence, verified in a saved file or adjudicated before it enters the base, or where a base cell records its source.
ACTION: (1) Ground a base cell by its own source columns (URL, page, line), not by an `evidence_sources` row. (2) Do not admit sources or adjudicate observations merely to populate base vocabulary. (3) Keep using `observe-term`, `adjudicate-term` and `add-alias` where a source is being read for evidence. (4) Treat the [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statements, quoted above.



<!-- O63 references/project-standards.md:5200-5216 -->

## Owner clarification 2026-11-06 (eighth) — English labels are allowed on non-English-origin concepts; the aim is to avoid English bias, not English words

Given in session https://claude.ai/code/session_01Ub36iPbFEPovMCoes1oKx9, on reading the session's report that the 180 non-English-origin register rows carry an empty English label "because E1 forbids an English gloss", and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim:

> "you obviously can have English words for these rows."

> "we are trying to avoid english BIAS"

**What this decides.**
1. **A non-English-origin concept may carry an English descriptive label.** The session read the sixth-entry and 2026-11-06 E1 answer ("a concept first met outside English is named by the instrument's own phrase … no English gloss") as forbidding any English words on such a row. The owner's aim is bias, not vocabulary: English must not be the pivot that decides which concepts exist, what the standard form is, or how a non-English concept is described. An English word on the row is allowed.
2. **Bias is avoided by structure, not by silence.** The instrument's own phrase stays on the row as a form of the concept, in its language and jurisdiction, with its source reference. An English label on such a row is a descriptive label of ours, marked as such, and is not asserted to be a form any English-language instrument uses. No English-language form is attached to the concept until a source for an English jurisdiction is found using it. English is one column of the matrix among the others and is not read first, matched first or ranked first.
3. **This narrows how OR-17 and E1 were applied here,** where they were read as forbidding an English label on a row whose concept English instruments have not been observed naming. They still forbid presenting a model's wording as a source's term. [ASSUMPTION: "English words for these rows" is read as an English label for the concept, flagged as a descriptive label and kept apart from attested English forms; it is not read as permission to present that label as the concept's English-language name.]

CONDITION: any session asking whether a concept first met in another language may have an English label, or what avoiding English bias requires of the register and the schema.
ACTION: (1) Give a non-English-origin concept an English descriptive label, marked as ours. (2) Keep the instrument's own phrase as a form with its language, jurisdiction and source reference. (3) Attach an English-language form only on a source for an English jurisdiction. (4) Order, match and rank no column ahead of another. (5) Treat the [ASSUMPTION] mark above as unratified.
DATE: 2026-11-06 — owner statement, quoted above.
