# Armature v3 — Tri-Lens Review: CRPD, UI/UX Accessibility, Usability

**Date:** 2026-04-27 20:35
**Reviewer:** Sonnet 4.6
**Scope:** Document `armature_v3.md` — pre-decision draft, person-profile armature
**Status:** Sonnet-drafted critique applying CRPD treaty text, WCAG 2.2 / COGA, and general usability principles. Best-practice synthesis claims (e.g., empirical effectiveness of specific UX patterns for cognitively disabled users) flagged for Opus session.

---

## Lens 1 — CRPD (Convention on the Rights of Persons with Disabilities)

### Strengths in current draft

- Plain-language register for disabled-person tool-user role aligns with Art 2 (communication includes plain-language) and Art 21 (access to information).
- Bottom-up entry without diagnosis aligns with Art 1 social-model orientation; the tool does not require medicalization to function.
- §3.4 distinguishes PWLE-as-evidence-source (CRPD Art 4.3) from PWLE-as-tool-user.
- Adjustability principle aligns with Art 3 (individual autonomy, freedom to make one's own choices).
- Disabled-person tool-user is a primary role, not a downstream beneficiary.
- Advocacy support and rights content surfaced for disabled-person variant aligns with Art 4 (general obligations including awareness raising).

### Gaps and issues

**1. Art 12 (Equal recognition before the law) — Capacity assumption is unaddressed.** The armature assumes the tool user has the cognitive and communicative capacity to autonomously navigate diagnosis taxonomies, 20-axis profiles, and four-dimensional scoping. For users with intellectual disability, advanced dementia, or cognitive disabilities affecting autonomous tool operation, CRPD Art 12 (as interpreted in General Comment 1, 2014) requires *supported decision-making*, not substituted. The current carer role frames usage as proxy ("what to ask for on behalf of") — this is substituted-decision-making language. CRPD-aligned framing positions the carer as a *supporter using the tool with* the disabled person, with the disabled person remaining central to the query and outputs. The interface design must accommodate two-person operation with the disabled person in the primary role even when motor or literacy barriers mean the carer is the active input mechanism. **A12 implication:** the carer role is not "proxy variant of disabled-person-as-tool-user" — it is a supported-use mode requiring distinct interaction patterns.

**2. Art 4.3 — "Nothing about us without us" is understated.** The validation gap (solo authorship) is acknowledged in §4.2 as operational reality. Under CRPD Art 4.3, *all* legislation, policies, and decisions affecting disabled persons require close consultation with disabled persons through their representative organizations. A guidebook governing built environment specifications for disabled people falls squarely within this. The current framing treats validation as a logistical limitation. CRPD treats it as a normative requirement. The armature should:
   - Explicitly identify the Art 4.3 deficit as a CRPD compliance gap, not merely an operational one.
   - State that pre-launch, the project does not yet meet Art 4.3 standards for participatory development of provisions affecting disabled people.
   - Specify what minimum participatory threshold must be met before launch (not after), even if that threshold is provisional.

**3. Art 9 (Accessibility) vs reasonable accommodation — Tier hierarchy unmapped.** The Tier 0 / 1 / 2 design hierarchy is not explicitly mapped to CRPD's foundational distinction between accessibility (Art 9, anticipatory, group-level) and reasonable accommodation (Art 5, responsive, individual-level). The mapping is implicit:
   - Tier 0 (UD/Code Compliance) ≈ Art 9 universal accessibility floor
   - Tier 1 (Population-informed inclusive design) ≈ Art 9 group-level accessibility
   - Tier 2 (OT/individual co-design) ≈ Art 5 reasonable accommodation
   
   Stating this explicitly strengthens the framework's CRPD grounding and clarifies legal/policy language for the policymaker role. **§5.2 should be amended to add this mapping.**

**4. Art 19 (Living independently and being included in the community) — Institutional design risk.** The armature's spatial scope (room type, building type) does not surface CRPD Art 19's deinstitutionalization mandate. Built environment design can perpetuate institutional patterns (shared bathrooms, restricted personal space, surveillance-oriented layouts) under the guise of "accessibility for high-support needs." The armature could inadvertently optimize for institutional contexts without flagging the CRPD obligation to enable community-based living. **Recommendation:** building-type or living-context filter should distinguish institutional vs community-based settings, and Art 19-relevant specifications (personal space, choice, control over environment) should be surfaced as cross-cutting requirements analogous to DAR.

**5. Art 5 (Non-discrimination), Art 6 (Women), Art 7 (Children) — Intersectional identity invisible.** The 20-axis system and diagnosis taxonomy address impairment dimensions but not intersecting identity dimensions:
   - Gendered specifications (menstrual hygiene facilities, breastfeeding spaces in non-residential buildings, gender-affirming bathroom design)
   - Child-specific specifications (height ranges, supervision-aware layouts, child-scaled controls, evolving capacity per Art 3.h and Art 7.3)
   - Age-related specifications beyond pediatric/adult split
   
   CRPD Arts 6 and 7 require disaggregation by gender and age. The current axis system cannot represent this. **A7 implication:** decide whether intersectional identity is a separate dimension (parallel to person profile) or integrated into the axis system. Body-size accommodation (§4.3) is a partially-related question.

**6. Art 30 (Cultural life, recreation, leisure, sport) — Underspecified scope.** Spatial scope examples list bathroom, bedroom, kitchen, corridor, entrance — predominantly residential. Cultural venues (theatres, museums), sports facilities, recreational spaces have CRPD-specific requirements (Art 30) that the current scope structure does not surface. **Recommendation:** spatial scope category list should be reviewed against CRPD Art 30 coverage at A8.

**7. Art 21 — Sign language and Deaf cultural identity vs medical-model auditory framing.** The axis system frames deafness as "auditory acuity" (full / hard of hearing / no functional hearing) and "auditory processing" (typical / APD / hearing-aid+loop dependent / CI dependent). This is medicalized. CRPD Art 2 recognizes sign languages as languages and Art 21 requires their facilitation. For a Deaf-signing user, the relevant accommodation is *linguistic*, not auditory: sign-language video content, sign-language-first communication, visual-alert systems framed as primary not compensatory. The current framing positions sign language users as having an auditory deficit. **A7 implication:** consider whether Deaf cultural/linguistic identity requires a distinct axis (or distinct top-down entry path: "Deaf — sign language user") rather than positioning within the auditory axes.

**8. Art 24, Art 27 (Education, Work) — Specific building types unaddressed.** Educational facilities and workplaces have CRPD-specific requirements (e.g., reasonable accommodation in education per Art 24.2.c; accessibility of workplaces per Art 27.1.i). Not surfaced in current spatial scope examples.

**9. Top-down workflow described as "natural" — medical-model regression risk.** §3.2 states "the natural workflow is top-down entry followed by bottom-up adjustment." This positions diagnosis-first as the default mental model. CRPD social-model orientation would frame both directions as equally primary. **Recommendation:** remove "natural workflow" framing; describe the two directions as parallel paths suited to different user contexts.

**10. Capability Approach integration — CRPD provides better operational grounding.** §5.2 acknowledges CA mapping as shallow. CRPD Art 19 is operationally clearer than abstract capability framing: each specification can be evaluated against (a) does it enable choice, (b) does it enable participation, (c) does it enable autonomy. This is testable in a way that "real freedoms to achieve valued functionings" is not. **Recommendation:** A12 should consider CRPD Art 19 operationalization as the primary framing, with CA as theoretical ground rather than the operational layer.

**11. Language: "persons with disabilities" vs "disabled people".** The treaty uses "persons with disabilities." The social-model preference in many disability rights communities (UK, Australia in particular) is "disabled people" (identity-first, framing disability as imposed by society on people with impairments). The document uses both inconsistently. The disabled-person tool-user role surfacing rights content needs to use language the user community accepts in the relevant jurisdiction. **A8/A12 implication:** language convention is jurisdiction-sensitive, not universal. The plain-language register may need locale-specific terminology.

**12. Carer role and substituted-decision-making language.** Current carer description: "what to ask for on behalf of." This is substituted-decision-making language. CRPD-aligned alternative: "what to ask for *with* and *alongside*" plus "tools for supporting the disabled person to be central to the conversation." The framing matters because UI design follows it.

---

## Lens 2 — UI/UX Accessibility

### WCAG 2.2 AA is mentioned but underspecified

§6 states WCAG 2.2 AA minimum, screen reader compatibility, switch input, captioning, plain-language toggle, no time limits. This is a baseline list, not an implementation specification. Specific WCAG 2.2 success criteria with high relevance to this tool:

- **2.4.11 Focus Not Obscured (Minimum) — AA.** Faceted query interface with overlapping panels must not obscure focus.
- **2.5.7 Dragging Movements — AA.** Any drag-based axis selection must have non-drag alternative.
- **2.5.8 Target Size (Minimum) — AA.** 24×24 px minimum; 44×44 px AAA. Affects axis-value selection on mobile.
- **3.2.6 Consistent Help — A.** Help mechanisms (definitions, glossary, tutorials) must be in consistent locations.
- **3.3.7 Redundant Entry — A.** User shouldn't re-enter axis values when adjusting query scope.
- **3.3.8 Accessible Authentication (Minimum) — AA.** If accounts/profile-saving introduced, no cognitive function tests.

### Cognitive accessibility (W3C COGA Task Force)

WCAG 2.2 cognitive coverage is acknowledged as weak by W3C COGA. The armature serves people with cognitive disabilities directly. COGA-relevant patterns:

- **Single-screen task focus.** Don't fragment query construction across multiple pages without persistent visible progress.
- **Forgiving input.** Autocorrect, fuzzy matching, plain-language synonyms in diagnosis search (already noted in §4.4).
- **Save state across navigation.** Don't lose query input on accidental browser back/forward.
- **Clear error recovery.** When axis combinations produce zero results or contradictions, surface what to change, not just "no results."
- **Consistent navigation.** Same query controls in same locations across all role surfaces.
- **Familiar metaphors over novel ones.** "Armature" itself is a novel metaphor (already flagged §1, §7 item 1) — risks failing COGA familiarity guidance.
- **Avoid jargon.** Document is rich with jargon: KFA, BPC, DAR, RFO, POE, DEM, NDV, OFS, IntD, MWI, Clarke, GMFCS, MACS, EDSS, ICF, CRPD itself. Tool users will not know these. Inline definitions, glossary, hover-explanations required.

[GAP: COGA — empirical effectiveness of specific cognitive-accessibility patterns for armature-style faceted query interfaces. Sonnet cannot synthesize evidence base; flagged for Opus session.]

### Multi-modal input

The two-direction person profile entry addresses input-path diversity at the conceptual level. Each direction must support multi-modal input:

- Voice input (mobility impairments, dyslexia)
- Switch input (limited motor control)
- Eye tracking compatibility
- Touch with adjustable target sizes
- Keyboard-only navigation (full functionality without pointer)

Not specified in current document. Website-build requirement.

### Cognitive load of axis entry

20 axes is significant cognitive load. Bottom-up entry asks the user to assess themselves (or another person) on 20 dimensions. UX patterns to reduce load:

- **Progressive disclosure.** Don't show all axes simultaneously. Cluster headers first; expand on click.
- **"Skip / unknown / not applicable" option on every axis.** Forcing answers degrades quality and excludes users uncertain about their own profile.
- **Sensible defaults aligned with bottom-up workflow.** "Typical" / "no impairment" defaults so users only modify axes that matter.
- **Cluster-based navigation.** The 6 clusters in §4 should be the primary navigation structure for bottom-up entry, not a flat 20-item list.
- **Plain-language axis descriptions.** Not "vestibular function — typical / motion-affected / severely affected" but "Balance and motion: how well do you (or the person) handle uneven surfaces, stairs, or moving environments?"
- **Examples for ambiguous axes.** "Reduced grip strength" — example: difficulty turning a doorknob, holding a coffee cup steady.

### Scope/filter complexity

Four orthogonal sub-dimensions plus role plus profile plus optional jurisdiction is a multi-faceted query. UX patterns:

- **Sensible defaults.** Most queries should work with profile + scope only; role auto-detected or remembered.
- **Most-common queries one click away.** Quick-start cards: "I'm a designer working on a bathroom for a wheelchair user." "I want to know my rights for housing accessibility."
- **Faceted search with live result counts.** Show "127 specifications matching" as filters apply.
- **Save / share query.** URL-encoded query state. Critical for collaboration use case (disabled person sharing query with their architect).
- **Query history.** Especially for designers iterating across projects.

### Output presentation — undefined

Armature defines query input but not output presentation. Key UX decisions:

- How are 50+ specifications presented for one query? List, grouped by category, filterable, searchable within results?
- How is evidence marker (●/○) communicated to screen readers? Symbols alone are inaccessible. Text equivalent required.
- How are conflict notes surfaced? Inline with each spec? Banner at top? Separate panel?
- How is Tier 2 handoff visually distinct from Tier 1? (Cannot rely on color alone — WCAG 1.4.1.)
- Tables vs cards vs lists for specs?
- Print / save / share output? Critical for designers integrating into deliverables, OTs into reports, disabled people into advocacy.

These are A3 (output schema) and website-build decisions, but the armature should flag them.

### Accessibility of evidence markers

● and ○ are visual symbols. Screen reader users hear "black circle" and "white circle" by default — meaningless. Text equivalents required: "evidence-based" and "inferred — gap disclosed." Color-only differentiation (some implementations might use green/grey) fails WCAG 1.4.1 Use of Color.

### Tool's own accessibility validation

The document mentions WCAG compliance as the validation standard. This is necessary but insufficient. A tool serving disabled people requires:

- **PWLE testing pre-launch.** Tested by disabled people across the populations the tool serves. Not just WCAG conformance audit. (Returns to CRPD Art 4.3.)
- **Accessibility statement publication.** Conformance level, known issues, contact for accessibility complaints, alternative-format request mechanism.
- **Independent accessibility audit** beyond automated tools.

Not specified.

### Language and translation

Document is English. CRPD Art 21 implies multiple-language access. International access requires:

- Language picker with locale-aware defaults
- RTL support (Arabic, Hebrew)
- Character-set support (CJK)
- Translation of axis labels, axis values, scope categories — not just chrome
- Translation review by native-speaking PWLE (more Art 4.3)

Not addressed. Significant scope question for post-Stage-A.

### Mobile-first

Many disabled users access the web primarily on mobile. Phone-screen UX for 20-axis entry, four-sub-dimension scope, role selection, results display is non-trivial. Touch target sizes (WCAG 2.5.5 / 2.5.8), one-handed operation, screen reader on small screens, switch control on mobile — all need explicit consideration.

### Error states

What happens when:
- A user enters a profile that retrieves zero specifications? (Suggests profile is contradictory or scope is over-filtered.)
- Axes contradict each other? (Not always knowable; some apparent contradictions are valid co-occurrences per §5.4.)
- A diagnosis isn't in the taxonomy? (Redirect to bottom-up entry; preserve any partial profile data.)
- Network fails mid-query? (Local-state preservation.)
- Output specifications are themselves contested or have ○ (inferred) markers exclusively? (Surface uncertainty honestly.)

Not addressed. Website-build requirement, but the armature should flag the categories.

### Identity persistence and privacy

If the tool offers profile saving:

- Privacy-by-design (local-only by default, server only with consent)
- Anonymous use without account
- Data retention transparency
- Sharing controls (share query, share results, with whom, for how long)
- GDPR / equivalent compliance

Health information is sensitive category data under GDPR Art 9. A tool collecting diagnosis or detailed functional profile data has compliance obligations. Not addressed.

### Help / inline explanation

Document is dense with terminology. Tool users need:

- Glossary
- Inline definitions on hover / tap
- "What is this?" buttons next to abstract concepts (axis, design tier, evidence marker)
- Onboarding tutorial (optional, skippable)
- Contextual help that does not interrupt task flow (per WCAG 3.2.6)

---

## Lens 3 — Usability for People (general usability beyond accessibility)

### Tool purpose comprehension

First-time users need to understand: what does this do, why use it, what will I get. The current document treats this as out of scope (it is) but the armature must flag the onboarding requirement. Different user types need different orientations:

- A designer needs: "This generates filtered specification matrices for disability-inclusive design across [scope]."
- An OT needs: "This surfaces evidence-graded environmental specifications you can use in client recommendations."
- A disabled person needs: "This helps you understand what to ask architects, OTs, and policymakers for, with explanations of why."
- A carer needs: "This helps you and the person you support identify environmental questions worth asking."
- A policymaker needs: "This maps inclusive design specifications against CRPD obligations and jurisdiction-specific compliance frameworks."

Each requires distinct entry framing.

### Trust signals

Disabled-person tool-users seeking advocacy support need to assess:

- Who made this?
- Is this authoritative or contested?
- Can I rely on this in arguments with architects / housing providers / policymakers?
- What are the known limitations?

The advocacy-not-authority disclaimer (§5.1) is correct. It must be visible in the tool, not buried. Source attribution per specification (BPC linkage) provides part of the answer; explicit "this is best practice based on [evidence tier]" framing per the 2026-04-26 specification language rule provides another part. But a meta-level "About this tool" / "Methodology" / "Limitations" page is needed.

### Recovery from wrong path

A user who started top-down ("Cerebral palsy") and realizes their child's profile differs significantly from defaults should be able to switch to bottom-up adjustment without losing context. A user who started bottom-up and realizes there's a diagnostic match should be able to apply diagnosis defaults without losing manual axis entries. Mode-switching UX is essential, not optional.

### Realistic expectation setting

Users come with specific questions ("can my mum live in this house?"). The tool returns specifications. There's a gap between specifications and what users want to know. Bridging the gap:

- Reframe specifications in user-meaningful terms ("180mm grab rail mounting height" → "the grab rail goes about [diagram] this high; this works for transfer from a standard wheelchair height").
- "Practical implication" sections that translate specs into space and function ("with these specs, the bathroom door must be a least X wide — that's wider than a standard residential door, so this likely needs a renovation if existing").
- Example use cases linking queries to outcomes.

This is closely related to the role × content-variant mechanism (§3.4) but extends beyond register to *interpretation depth*.

### Sharing and collaboration

Core use cases:
- Disabled person preparing for a meeting with their architect: "Here's my profile; here's what I want to talk about; here are the specs I want you to confirm we're meeting."
- OT preparing recommendations for a client family: shareable query state, exportable spec list with evidence markers.
- Designer working with disabled co-designer: live-shared query with both parties able to see and adjust.
- Policymaker citing the tool in policy proposals: stable URL, citable specifications with evidence sources.

Sharing isn't an add-on; it's the value-creation step for several roles. Underspecified in current document.

### Confidence calibration

Tool users need to understand when to trust output and when to push for more. The evidence marker (●/○) is a good signal. Adjacent signals required:

- "This is well-established across multiple jurisdictions and evidence tiers."
- "This is current best practice based on [tier] evidence; emerging research may revise."
- "This is contested between [framework A] and [framework B]; we present both."
- "This is inferred from clinical reasoning — empirical evidence is absent. Consider this a starting point for OT consultation."

Currently the project has the metadata to support this calibration; the armature must surface it.

### Action orientation

What does the user *do* with output?

- Designer integrates into drawings / specification documents → exportable spec lists, ideally in BIM-compatible format (long-term).
- OT integrates into client recommendations → exportable text formatted for assessment reports.
- Disabled person uses for advocacy → printable / shareable plain-language summary with rights references.
- Policymaker uses for policy drafting → citable text with full evidence trail.
- Carer uses for advocacy support → shareable summary aligned with disabled-person variant.

Outputs should be exportable in forms suited to each action. This is a website-build decision but the data model must support it.

### Cultural and linguistic appropriateness

"Plain language" for a UK disabled adult differs from "easy English" for an Australian user with intellectual disability differs from translated French. The Easy Read question raised in §7 item 21 is part of this larger problem:

- Plain-language register is not one register; it's many.
- Easy Read (formal accessibility format with image+text) is distinct from plain-language (clear writing for general audiences).
- Locale-specific plain-language differs by region (UK GOV.UK style, US plain-language standards, Australian Easy English, etc.).

A12 should treat plain-language as a multi-register concept, not a single content variant.

### Privacy and trust

Users may enter sensitive information:
- Diagnoses (sensitive health data)
- Detailed functional profiles (re-identifiable in combination)
- Location/jurisdiction (geolocation)

Privacy-by-design is required, not optional. Local-only processing where feasible. Anonymous use as default. Data retention minimization. Sharing controls explicit. GDPR Art 9 and equivalent compliance. Not addressed in current document.

### Failure modes

When the tool fails (network, server, data missing for a query), what happens? Graceful degradation matters more for users who cannot easily retry, navigate around errors, or troubleshoot.

### Meta-question — do users know what they don't know?

A disabled person preparing to advocate may not know which axes are relevant. A designer new to inclusive design may not know which scope dimensions matter for their project. The tool should help users discover relevant scope, not assume they bring it. Suggestions, recommended-next-questions, and "you might also want to consider" prompts are usability features, not nice-to-haves.

### Appeal / feedback

When the tool's output disagrees with the user's lived experience or professional judgment, there must be a feedback channel. This operationalizes CRPD Art 4.3 post-launch (consultation as continuous, not one-off). The feedback mechanism is also a quality-assurance asset — disagreement signals data gaps.

---

## Synthesis — what flows back into the armature

Some review findings affect the armature directly. Others are website-build or downstream phase decisions but should be flagged in the armature so they aren't lost.

### Should be incorporated into armature v4

1. **§5.2 mapping addition:** explicit Tier 0 / 1 / 2 mapping to CRPD Art 9 (accessibility) vs Art 5 (reasonable accommodation).
2. **§3.2 framing fix:** remove "natural workflow" language describing top-down-first; reframe as parallel directions.
3. **§3.4 carer role:** rewrite to align with CRPD Art 12 supported-decision-making, not substituted-decision-making language.
4. **§4.1 IntD note expansion:** acknowledge Art 12 capacity assumption affecting tool autonomy and supported-use mode requirement.
5. **§4.2 validation gap:** reframe solo-authorship validation gap as CRPD Art 4.3 compliance gap, not just operational reality.
6. **§5.6 (new):** add CRPD Art 19 (independent living) cross-cutting requirement, parallel to DAR.
7. **New axis or distinct entry path question (A7):** Deaf cultural/linguistic identity — auditory acuity axis is medicalized framing. Add to §7 open questions.
8. **New A7 question:** intersectional identity (gender per Art 6, age per Art 7) — separate dimension or axis-system extension. Add to §7.
9. **New A8 question:** spatial-scope coverage of CRPD Art 30 (cultural/recreational/sport venues) and Arts 24/27 (education/work building types). Add to §7.
10. **§4.4 expansion:** WCAG 2.2 AA listed; expand to specific success criteria (2.5.8, 3.2.6, 3.3.7) and add COGA-aligned cognitive-accessibility requirements.
11. **§6 expansion:** PWLE testing pre-launch as CRPD Art 4.3 operationalization, not just WCAG audit.
12. **§7 new items:** sharing/collaboration as core use case; mode-switching UX; output presentation schema; privacy-by-design.

### Belongs to website-build phase but should be flagged in armature

13. Multi-modal input support (voice, switch, eye tracking, keyboard-only).
14. Progressive disclosure of 20-axis entry.
15. Quick-start patterns / role-orientation onboarding.
16. Trust-signal architecture (about, methodology, limitations pages).
17. Output presentation patterns (cards/tables/lists; export formats; sharing).
18. Help / inline definitions / glossary system.
19. Multi-language support architecture.
20. Mobile-first responsive design.
21. Error-state and recovery patterns.
22. Privacy-by-design defaults (local-first, anonymous).
23. Feedback mechanism for tool-user dissent.

### Belongs to a phase not yet defined

24. Locale-specific plain-language registers (multiple plain-language variants per language).
25. CRPD compliance assessment as a standing project artifact (not a one-off review).
26. Cultural/linguistic validation of all content variants by relevant PWLE communities.

---

## Sonnet/Opus boundary

This review applies CRPD treaty text, WCAG/COGA framework principles, and general usability heuristics to the armature draft. Framework interpretation is appropriate for Sonnet.

Best-practice synthesis claims that need Opus session:

- Empirical effectiveness of specific cognitive-accessibility UX patterns for faceted-query interfaces in disability-inclusive design tools. [GAP: COGA empirical synthesis]
- Disabled-user testing methodologies appropriate for tools serving multiple disability populations simultaneously.
- Evidence on whether top-down vs bottom-up entry directions produce different output quality or different user satisfaction across disability populations.
- Comparative effectiveness of plain-language vs Easy Read vs symbol-supported communication for built-environment specifications.

These should be flagged for Opus synthesis at A12 (decision protocol), with output feeding the website-build specification rather than the armature itself.

---

## Critical limitation of this review

This review is conducted by Sonnet, working from the armature document and project-standards. It is not a substitute for review by:

- Disabled people across the populations the tool serves (CRPD Art 4.3 — direct, not proxied through Sonnet).
- DPOs (representative organizations).
- Practicing OTs working with disability-inclusive design.
- Architects with built-environment access expertise.
- WCAG / COGA practitioners.
- Disability rights legal experts.

The findings here should be treated as a structured first-pass identifying gaps for those reviewers to address — not as a validated CRPD compliance assessment.
