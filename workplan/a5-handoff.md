# A5 Handoff — Co-1 Operational Specification
**Issued:** 2026-04-29 14:04 UTC
**Phase predecessor:** A4 Voice and framing — COMPLETE
**Phase target:** A5 — Co-1 operational specification
**Doctrinal basis:** workplan-co0007-v3 §A5 + Amendment 7 (pre-launch solo authorship reality) + governance/audience-priority.md + governance/pre-stage-a-decisions.md D-03 (revised 2026-04-26)
**Sessions estimated:** 2–3 (revised from original 5–7 per Amendment 7)
**Pattern:** Governance document only (no Python validator; no schema; recruitment thread inoperative pre-launch)

---

## 1. What A5 produces

**Primary deliverable:** `governance/co1-operational.md` — definitive specification of how Co-1 (lived experience and participatory design research) operates as a co-primary evidence tier in the guidebook, given the pre-launch solo authorship reality.

**Secondary deliverables:**
- Trigger specification for post-launch CS2 (Co-1 recruitment) and CS5 (Co-1 representation monitoring) activation conditions
- Documentation of inoperative-pre-launch status of CS2/CS5 in `references/project-standards.md`
- Updated `gap_register.md` entries for any Co-1 representation gaps surfaced during specification

**No Python work.** A5 is the second prose-only phase in Stage A (after A4). A6 returns to governance+code pattern with the evidence-state validator.

---

## 2. Why A5 is necessary

The locked Seven-Tier Evidence Hierarchy (Core Doctrine 2026-03-19, elevated 2026-04-24) places **Co-1 (Lived Experience and Participatory Design Research) as co-primary alongside Tier 1 OT clinical research**. Part 1 §1.5 of the guidebook treats Co-1 as a peer evidence tier with formal authority equal to OT research:

> "Where lived experience evidence and clinical research findings align, confidence is elevated. Where they diverge, both are presented and the divergence is noted. Participatory design processes — where disabled people are involved as co-designers, not only as research subjects — are treated as a form of evidence generation."

This is a strong commitment. It creates obligations the project does not currently have a way to honor in operational practice.

**The gap A5 closes:** the corpus of Co-1 evidence currently in the guidebook is drawn from third-party sources (Kelsey IDS, Gallaudet DeafSpace, Motionspot, APF France Handicap, CDPF, CERMI, ME Association, Patient Led Research Collaborative, etc.). It is curated by a single solo author (per D-03 revised 2026-04-26 03:45). It is not currently produced by an in-house Co-1 representative within the project. This is the operational reality the specification must describe accurately, not aspirationally.

**Why this cannot be deferred:**
1. **A6 evidence methodology depends on it.** A6 will operationalize T-04 evidence-state machine and T-03 tier+evidence_type encoding. Without an A5 specification of what Co-1 means operationally pre-launch, A6 cannot validate Co-1 evidence claims.
2. **B1 schema design references it.** The EvidenceSource entity needs to encode `co1_status` (third-party-curated vs. in-house-generated) and `co1_provenance` (which Co-1 source). A5 specifies the values these fields take.
3. **Adversarial-use review (A10) depends on it.** Misrepresentation of Co-1 status — claiming in-house Co-1 representation that does not exist — is a critical reputational and ethical risk. A5 produces the documentation that prevents this.

---

## 3. Doctrinal anchors carried forward

A5 must honor the following prior decisions without revisiting them:

| Decision | Source | Status |
|---|---|---|
| **D-03 revised** | `governance/pre-stage-a-decisions.md` 2026-04-26 03:45 | Co-1 operational role is pre-launch solo authorship; collaboration contingent post-launch. Recruitment is inoperative pre-launch. |
| **Amendment 7** | `workplan/workplan-co0007-v3-amendments.md` | Co-1 cadence is no longer a binding constraint pre-launch. Solo-only-permanent is a possible end-state. |
| **Audience canonical** | `governance/audience-priority.md` 2026-04-26 | Primary: designers, disabled people. Secondary: OTs, policymakers. Pre-launch methodological note: solo cross-checking only; no live representation. |
| **Advocacy identity** | Core Doctrine 2026-04-26 19:25 | Guidebook is advocacy, not authority. Equips with questions; does not confer competence. |
| **Tier-appropriate specification language** | Core Doctrine 2026-04-26 19:25 + voice-style §8.1 (this A4) | Specification voice locates authority appropriately. |
| **Seven-Tier Evidence Hierarchy** | Core Doctrine 2026-03-19, elevated 2026-04-24 | Tier 1 + Co-1 co-primary. Lived Experience and Participatory Design Research is its own tier with peer authority. |

---

## 4. Open questions A5 must resolve

These are the substantive judgments the A5 governance document needs to make. They are not pre-decided; A5 is where they get decided.

### Q1 — How does the guidebook represent Co-1 evidence honestly under solo authorship?

The guidebook currently cites Co-1 sources (Kelsey IDS, DeafSpace, etc.) with apparent equivalence to in-house Co-1 representation. Under solo authorship, this equivalence is overstated.

**Sub-questions:**
- Should Co-1 citations carry a `co1_provenance` marker distinguishing third-party-curated vs. in-house-generated? (Provisional answer: yes, per B1 schema design needs.)
- Does the guidebook's specification voice (per voice-style §8.1) need a Co-1 locator analogous to "Tier 1 evidence supports..."? (Provisional answer: yes — "Co-1 sources ([list]) document..." pattern.)
- How does the reader distinguish "consensus across multiple Co-1 sources" from "single Co-1 source citation"? (Resolves: provisional Co-1 evidence-state classification within T-04.)

### Q2 — What do CS2 and CS5 look like operationally pre-launch?

The cross-stage threads CS2 (Co-1 recruitment) and CS5 (Co-1 representation monitoring) are flagged INOPERATIVE pre-launch by Amendment 7. But the guidebook continues to make Co-1 claims and synthesize Co-1 evidence. Something is operating; it just is not recruitment.

**Sub-questions:**
- What is the pre-launch operational substitute for CS2 / CS5? (Provisional: solo curation + explicit gap acknowledgment + post-launch contingent activation.)
- What does "post-launch contingent activation" mean concretely? Specifically: what triggers activation? Who decides? On what timeline? (A5 must specify.)
- If launch never occurs (Amendment 7 acknowledges this is possible), are CS2 and CS5 permanently inoperative? Or do they convert to a different form? (A5 must specify.)

### Q3 — What does the guidebook owe Co-1 sources whose work it cites?

The guidebook draws on ~15+ Co-1 source organizations (Kelsey IDS, DeafSpace, Motionspot, APF, CDPF, CERMI, ME Association, etc.). Solo authorship means none of these organizations have endorsed the guidebook's synthesis of their work.

**Sub-questions:**
- Should the guidebook publish a Co-1 attribution and disclosure section? (Provisional: yes — likely as Part 13 appendix or front matter.)
- Should Co-1 sources be notified (pre-launch or at launch) that their work has been synthesized? (Outside A5 scope; flag for A11 legal/regulatory framework.)
- Is there an operational difference between citing a Co-1 source (one citation, attributed) and synthesizing across Co-1 sources (multi-source claim, no individual organizational endorsement)? (Provisional: yes — synthesis requires explicit multi-source labeling.)

### Q4 — How does Co-1 status interact with the Design Modes?

Tier 1 and Tier 2 design specifications use Co-1 evidence alongside OT evidence. A4 §8.1 worked examples used "Tier 3 evidence (Sanford 2010; AOTA 2018) supports..." constructions, which assumes Tier 1 OT evidence underlies the spec.

**Sub-questions:**
- When a Tier 1 specification range is supported primarily by Co-1 (not by Tier 1 OT clinical research), how is the voice located? (Provisional: "Co-1 sources document..." analog to "Tier 3 evidence supports...".)
- When Co-1 and Tier 1 OT diverge (per Part 1 §1.5 — both are presented; divergence noted), what is the voice convention for presenting both? (Provisional: "Tier 1 OT evidence supports X; Co-1 sources document Y; the Tier 1 range encompasses both.")
- Does Tier 2 (person-specific OT-assessed) override Co-1 source recommendations? Or does it integrate them? (Substantive question for A5.)

### Q5 — What is the relationship between Co-1 status and audience priority?

Audience-priority canonical: primary = designers + disabled people; secondary = OTs + policymakers.

**Sub-questions:**
- "Disabled people" as audience and "Co-1 representation" in evidence are related but distinct. Audience is who reads; Co-1 is whose lived experience the evidence draws from. A5 should specify the relationship.
- Pre-launch solo authorship: the author is one disabled person. This is not Co-1 representation; it is solo authorship by someone with lived experience. A5 must specify how to talk about this without overclaiming.

---

## 5. Methodology recommendation

A5 should be structured as **a single governance document** with the following sections:

1. **Definition** — what Co-1 is (locking in current definition from Part 1 §1.5 and the Seven-Tier Hierarchy)
2. **Pre-launch operational reality** — solo authorship + third-party-curated Co-1 sources + explicit gap acknowledgment
3. **Resolution of Q1–Q5** — the substantive judgments listed above, made explicit
4. **CS2 and CS5 trigger specification** — what activates Co-1 recruitment / representation monitoring post-launch (if launch occurs)
5. **Voice conventions** — how Co-1 evidence is named, attributed, and synthesized in guidebook prose; updated against voice-style §8.1
6. **Documentation requirements** — what every Co-1 citation in the guidebook must carry (provenance, gap-disclosure where applicable)
7. **Schema implications** — pointers to B1 (EvidenceSource entity, `co1_provenance` field) for downstream encoding

**Estimated session 1:** Sections 1–3 (definition + reality + Q1/Q2/Q5 resolution).
**Estimated session 2:** Sections 4–7 (triggers + voice + documentation + schema pointers).
**Possible session 3:** if Q3 (Co-1 source attribution / disclosure) requires more depth or external research.

---

## 6. Doctrinal risk: what A5 must NOT do

- **MUST NOT** claim Co-1 representation that does not exist. The guidebook is solo-authored. Saying otherwise — even by implication — is the highest-priority adversarial-use risk.
- **MUST NOT** retroactively revise the Co-1 co-primary tier status. The Seven-Tier Hierarchy is locked. A5 specifies how Co-1 operates, not whether it is a tier.
- **MUST NOT** commit to Co-1 recruitment timeline pre-launch. Amendment 7 deferred this. CS2 specifies post-launch contingent activation only.
- **MUST NOT** treat third-party-curated Co-1 evidence as a deficiency to be fixed in A5. The evidence is real and authoritative within its scope; the operational gap is in-house representation, not evidence quality.
- **MUST NOT** scope-creep into A11 (legal and regulatory framework) — Co-1 source notification protocols and licensing questions belong there, not here.
- **MUST NOT** scope-creep into B1 (schema design) — A5 produces pointers to schema needs, not the schema itself.

---

## 7. Reading list for A5 Session 1

Mandatory reads (full file unless noted):
1. `governance/audience-priority.md` — audience canonical, with pre-launch methodological note
2. `governance/pre-stage-a-decisions.md` — D-03 revised text
3. `workplan/workplan-co0007-v3-amendments.md` — Amendment 7 in full
4. `governance/mission-and-epistemics.md` — Co-1 doctrinal grounding
5. `governance/conceptual-model.md` — EvidenceSource entity (A3 sign-off)
6. `parts/v10/part01.md` §1.5 evidence hierarchy (just reframed in A4 — current state authoritative)
7. `references/project-standards.md` — current cross-stage thread definitions

Reference reads (headers + relevant sections):
8. `skills/voice-style_SKILL.md` §8.1 — tier-appropriate construction; will inform Co-1 voice convention
9. `workplan/a4-part01-audit-2026-04-27.md` — A4 final state for context
10. `gap_register.md` — surface any open Co-1-representation gaps that should be addressed

External research reads (only if Q3 requires depth):
- CRPD Article 4.3 — co-design obligation text
- Kelsey IDS, Motionspot, APF France Handicap operational documents (Co-1 source examples)
- ME Association / Patient Led Research Collaborative — patient-led research methodology

---

## 8. Cross-stage continuity threads

A5 affects these cross-stage threads:

| Thread | Change at A5 |
|---|---|
| **CS2** Co-1 recruitment | Trigger spec produced; remains INOPERATIVE pre-launch |
| **CS5** Co-1 representation monitoring | Trigger spec produced; remains INOPERATIVE pre-launch |
| **CS8** Decision capture | A5 substantive decisions captured per protocol (note: CS8 doesn't go LIVE until A12, so capture format is provisional) |
| **CS4** Re-issue cadence | A5 closure does not trigger a synthesis re-issue; that triggers at end of Stage A and at B7 lock |

A5 does not affect these threads:
- CS1 (doctrine recheck) — activates at A13
- CS3 (versioning) — activates at A9 spec, C1 LIVE
- CS6 (standards monitoring) — activates at B7
- CS7 (salvage re-evaluation) — activates at stage transitions
- CS9 (adversarial-use review) — activates at A10

---

## 9. Stage A budget impact

Original v3 budget for A5: 5–7 sessions.
Amendment 7 revision: 2–3 sessions (recruitment thread inoperative; less to write).
Stage A total budget post-Amendment 7: 22–32 sessions.

**A5 entering with: ~14 sessions used (Stage 0 9 + A1-A2 ~3 + A3 ~7 + A4 3 = ~14) + A5 (2–3) = ~16–17. On track.**

After A5: A6 (3–5), A7 (2–3), A8 (2–3), A9 (2–3), A10 (1–2), A11 (1–2 + counsel external), A12 (1), A13 (1) = ~13–20 more sessions to Stage A complete.

Stage A done estimated total: ~30–37 sessions, within or near the 22–32 budget upper bound.

---

## 10. Entry condition for A5 Session 1

Before starting A5 Session 1, the user should:

1. ✓ Apply PI updates from `workplan/pi-update-co0008.md` if not yet applied (Opus 4.7 as primary model; Standing Rules 11–14)
2. ✓ Confirm Amendment 7 is the operative pre-launch reality (no recruitment activity)
3. ✓ Confirm A4 closure (this audit closes A4)
4. Decide whether A5 starts in current conversation or fresh context

A5 Session 1 will load this handoff document + the 7 mandatory reads above as its input. Estimated context load: ~80–120k tokens of input before drafting begins. Comfortable in 1M window.

---

**End of A5 handoff.**
