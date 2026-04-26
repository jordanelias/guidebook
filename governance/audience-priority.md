# Audience Priority
**Status:** ITERATION 1 — first draft of A1-A2; not yet canonical
**Created:** 2026-04-26 03:55 UTC
**Iteration plan:** `workplan/a1-a2-iteration-plan.md`
**Operative frame:** Pre-launch solo authorship; partial-CRPD-Art-4.3-honoring at evidence level
**Companion deliverable (pending):** `governance/mission-and-epistemics.md` (canonical) — produced in iter 2

---

## Why audience priority is an operational question

Audience priority answers a recurring question in content production: *when reading needs diverge, whose needs govern?* It is not a worth-judgment about who matters more. It is an operational rule that resolves choices about content layering, navigation entry, terseness vs framing, and cross-reference structure. Without an audience-priority rule, every such choice would be made ad hoc and the guidebook would drift toward whichever audience the author imagines most clearly while drafting any given passage. With the rule, choices are accountable.

The four named audiences — designers, disabled people, occupational therapists, policymakers — are confirmed in mission-PROVISIONAL §Audiences. This document specifies their operational priority and the use-patterns within each.

---

## Primary audiences

**Primary status is granted to the audiences at the production-use endpoints of the built environment: those who produce environments and those who use them.**

### Designers (architects, interior designers)

Designers produce environments. Decisions made at programming, schematic design, design development, and construction documentation determine what the built environment is. The guidebook's most direct mechanism of effect on accessibility is changing those decisions.

**Use-patterns:**

| Pattern | Reader state | Content need |
|---|---|---|
| Information-finding | Looking up a specific value for a specific parameter for a specific population at a specific design stage | Tabulated, precise, retrievable; minimal framing in the immediate cell; cross-references to fuller treatment |
| Decision-frame | Facing a population-implicating design decision; wants to think through considerations | Narrative around the spec data; questions to ask; alternatives surfaced; trade-offs named |

These are different reading modes engaging the same underlying data. Content production must serve both modes — typically by layering (table + surrounding prose) rather than by producing two parallel artifacts.

### Disabled people (themselves)

Disabled people use environments. Their lived experience tests whether what gets built actually serves them. The guidebook's claim to evidence-based best practice is empty if it is not legible and accountable to the people whose needs it claims to specify.

**Use-patterns:**

| Pattern | Reader state | Content need |
|---|---|---|
| Information-finding | What should I expect / ask for / advocate for in a built environment shaped around my needs? What does my condition imply for specific design parameters? | Accessible specs in plain language; cross-references to advocacy use; precise enough to cite when asking for change |
| Representation-checking | Is my experience acknowledged? Is within-population variability honored, or am I subsumed under a generic label? | Narrative framing surfacing variability; explicit acknowledgment that population codes are organizing scaffolding, not descriptions of any individual; visible Co-1 evidence basis |

Representation-checking is unusual among reading modes: the reader is **testing** the document, not just reading it. The document must hold up under that test. A document that fails representation-checking is failing in its core commitment, not merely in style.

---

## Secondary audiences

**Secondary status is granted to audiences whose work shapes the conditions of others' production or use: intermediaries between code, individual assessment, and the built environment.**

### Occupational therapists

OTs operate at the individual side of the built environment — assessing how a specific person engages a specific environment, intervening through co-design at Tier 2. They have established clinical training; the guidebook supplements rather than primarily teaches them.

**Use-patterns:**

| Pattern | Reader state | Content need |
|---|---|---|
| Clinical-collaboration | Co-designing a built-environment intervention with a client; bringing population-level specifications into individual-specific assessment | Tier 1 ranges legible alongside the median, with the Tier-2-resolution path identified |
| Specialist-handoff | Communicating an OT assessment finding to a non-OT designer or builder; using the guidebook as common-ground language | Population codes and parameter labels stable enough to cite; cross-references to the matching item specification |

### Policymakers

Policymakers shape codes and policy. The guidebook is evidence-grounded best practice that informs rule-making — it is not itself a code and does not aim to become one. Tier 6 codes are the floor; the guidebook specifies the evidence-based aspiration.

**Use-patterns:**

| Pattern | Reader state | Content need |
|---|---|---|
| Jurisdiction-comparison | What do other jurisdictions do for this provision? Why? | The 24/46/49 jurisdiction structure (per A8) navigable; comparable provisions surfaced |
| Rationale | What is the evidence basis for this best-practice value? | Citation chain visible; tier hierarchy applied; gap between code value and evidence-based value made explicit |

---

## Audiences by extension

The guidebook does not produce dedicated content for the following readers, but its structure makes it usable by them through one of the four core audience modes:

- **Students** (architecture, occupational therapy, disability studies) — typically read in designer-decision-frame mode or OT-clinical-collaboration mode
- **Researchers** — typically read in policymaker-rationale mode
- **Facility managers / building owners** — typically read in designer-information-finding mode
- **Builders, contractors, inspectors** — typically read in designer-information-finding mode for specific items

These uses are accommodated by extension. They do not constrain content choices independently. If an extension-by-use need cannot be served by any of the four primary/secondary use-pattern paths, that is a structural gap to log, not a tertiary-audience target to add.

---

## Conflict-resolution rules

### Within-primary conflicts

When designer-information-finding needs and disabled-person-representation-checking needs apply to the same content cell:

1. **Default: layer both.** Spec table for lookup precision; framing prose surrounding the table for representation acknowledgment. Most cells admit both.
2. **Where layering is impossible** (e.g., a single sentence in a tight prose passage): representation acknowledgment governs framing language; numeric/parameter precision governs measurement text. The two coexist within the sentence.
3. **Where the representation-check would return a "this is wrong about my experience" verdict** for a defensible disabled reader: that is a content failure overriding designer convenience. Re-draft the cell.

### Within-secondary conflicts

When OT-clinical-collaboration and policymaker-rationale needs apply to the same content cell:

1. Default: serve clinical-collaboration in the primary content body; serve rationale in cross-references to evidence base, jurisdiction matrix, and bibliography.
2. Where conflict cannot be resolved by structural placement, primary audiences govern any framing decision; secondary audiences accept the resulting structure.

### Primary vs secondary conflicts

1. Primary's needs govern direct content placement, primary navigation paths, and the language of doctrinal commitments.
2. Secondary's needs govern cross-reference structure, appendices, jurisdiction matrices, evidence-tier listings, and supplementary materials.
3. A secondary-audience need that would require restructuring primary content paths is logged as a gap, not absorbed.

### Within-audience use-pattern conflicts

When information-finding and decision-frame patterns apply to the same designer reader at the same moment, or information-finding and representation-checking apply to the same disabled-person reader:

1. **Entry path governs.** A reader entering through a specification page is in information-finding mode; a reader entering through a Part introduction or doctrinal commitment is in decision-frame or representation-checking mode.
2. **Where entry path is ambiguous, default to the more demanding pattern**: representation-checking for disabled people, decision-frame for designers. The more demanding pattern produces content that also serves the simpler pattern; the reverse is not true.

---

## What this means for content production

| Content type | Audience priority signal | Content production rule |
|---|---|---|
| Item specifications | Designer information-finding + disabled-person information-finding | Tabulated lookup-friendly parameter data; framing prose surrounding; population codes navigable |
| Population sections | Disabled-person representation-checking | Narrative-led; within-population variability surfaced; co-occurrence as norm; population code as scaffold not description |
| Conflict-resolution sections (Parts 3, 5, 7) | Designer decision-frame + OT clinical-collaboration | Decision-framework structured; questions to ask; resolution paths identified; not prescriptive answers |
| Front matter and Part introductions | Designer decision-frame + disabled-person representation-checking | Questions-led teaching mode; doctrinal commitments visible; mission language audible |
| Appendices and bibliographies | Policymaker rationale + OT specialist-handoff | Citation chains; jurisdiction matrices; tier-hierarchy listings; evidence basis retrievable |
| Cross-references | All audiences | Stable; navigable both directions; pattern consistent across Volumes I and II |

---

## Open questions for iteration 2+

The following are deferred to subsequent A1-A2 iterations or to later phases:

1. **Volume-specific audience priority weighting.** Should Volume I (conceptual) emphasize representation-checking and decision-frame more than Volume II (item-level), which leans toward information-finding? Defer to iter 2 against mission-and-epistemics first draft.
2. **Audience priority under tight design timeline.** When a designer reader is in genuine time pressure, the layered-content rule may produce a content density they cannot navigate. Should there be a "fast lane" navigation mode? Routes to B3 (navigation mode specification), not A1-A2 — but A1-A2 audience-priority decisions constrain B3 design space.
3. **Use-pattern → navigation-mode mapping.** The four primary use-patterns plus four secondary use-patterns suggest navigation modes. B3 is the phase that decides this. A1-A2 supplies the audience-priority constraint; B3 supplies the navigation specification.
4. **Public-facing version of audience priority.** Should there be a one-paragraph version of this document for the guidebook front matter? Defer to iter 5 (optional public-facing pass).
5. **Citation gap.** The audience-priority structure is not yet supported by citations to design-pedagogy or accessibility-practice literature. Iter 3 closes the citation gap.
6. **Tertiary-by-extension acknowledgment.** Should the front matter explicitly name extension users (students, researchers, facility managers, builders, inspectors), or leave them unnamed? Either is defensible. Decide in iter 4 cross-test pass.

---

## Cross-references

- Iteration plan: `workplan/a1-a2-iteration-plan.md`
- Mission input: `governance/mission-PROVISIONAL.md` §Audiences (revised 2026-04-26 03:45)
- D-03 revised: `governance/pre-stage-a-decisions.md` (Co-1 evidence engagement only pre-launch)
- Project standards: `references/project-standards.md` (RULE 2026-04-26 03:45 — pre-launch solo)
- Workplan v3 §A1-A2: `workplan/workplan-co0007-v3.md` lines 146–160
- Amendment 7: `workplan/workplan-co0007-v3-amendments.md` (A5 re-scoped; no Co-1 collaborator review at iteration boundaries)
- Audit v2 §T-05 (use-patterns within audiences): the audit document is not in repo; T-05 framing is incorporated through this document's use-pattern structure

---

## What this file does not do

- **Does not commit canonical audience priority.** Canonical is achieved at iter 4 cross-test pass. This is iter 1.
- **Does not articulate the mission.** Mission articulation is iter 2 against this audience-priority baseline.
- **Does not specify navigation modes.** B3 does that. A1-A2 supplies the audience-priority constraint that B3 must respect.
- **Does not commit citations.** Iter 3 cites the audience-priority and use-pattern claims against design-pedagogy and accessibility-practice literature.
- **Does not specify content production templates.** That is C2 (skill-build) work. The "What this means for content production" table specifies the audience-priority signals; templates instantiate them.
- **Does not assume Co-1 review.** Per Amendment 7 / revised D-03, A1-A2 is solo authorship. Iteration acceptance tests are solo cross-checking against committed mission language.

---

## Status

ITERATION 1. Marked draft. Not canonical.

| Field | Value |
|---|---|
| Created | 2026-04-26 03:55 UTC |
| Iteration | 1 of 4–6 (per `workplan/a1-a2-iteration-plan.md`) |
| Author | Project owner (solo, pre-launch) |
| Acceptance test for canonical | Iter 4 cross-test pass against `governance/mission-and-epistemics.md` (canonical, produced iter 2-3) |
| Doctrinal anchor | `references/project-standards.md` Core Doctrine + 2026-04-26 03:45 RULE |
| Operational frame | Pre-launch solo synthesis from published Co-1 corpus |
