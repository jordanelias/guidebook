# Work Triage Plan — Opus Review Sessions
**Created:** 2026-03-29  
**Basis:** Ecosystem Update Plan (misc/ecosystem-update-plan-2026-03-29.md) Part 2  
**Scope:** All outputs previously attributed to Opus that were produced by Sonnet 4.5 via artifact proxy  
**Model requirement:** ALL sessions in this plan MUST be run in an Opus conversation session

---

## Verdicts Summary

| Item | Group | Verdict | Opus Session |
|---|---|---|---|
| fold-down-grab-bar-specification BPC | C | REDO | A |
| upper-limb-impairment-built-environment BPC | C | REDO | A |
| cross-population-conflict-resolutions BPC | C | REDO | A |
| CON-0050–0084 MODERATE connections (20) | F | FLAG→A | A (parallel) |
| acoustics-speech-intelligibility-disability BPC | C | FLAG | B |
| sensory-relief-space-design BPC | C | FLAG | B |
| ndv-aut-built-environment-quantified-thresholds BPC | C | FLAG | B |
| T0-03 rejection (retreat/reset room) | E | FLAG | B |
| E-14 specification logic + citation verification | D | FLAG | B |
| residential-accessible-home-case-studies synthesis | B | FLAG | C |
| Pre-passthrough escalations (grab bar, turning circle, seizure, DEAF RT60) | A | FLAG | C |
| T0 CONFIRMED candidates (B-12, E-10, E-12, E-13) | E | ACCEPT | — |
| CON-0001–0038 connections | — | ACCEPT | — |
| CON-0085–0092 external connections | — | ACCEPT | — |
| All Sonnet assembly/drafting work | — | ACCEPT | — |

---

## Opus Review Session A — Safety-Critical

**Priority:** HIGHEST — blocks Phase 3 for grab bar and toilet compartment items  
**Prerequisite:** None  
**Phase 3 items blocked until complete:** All grab bar items; all toilet compartment items involving ADA 18-inch centreline; A-04, B-05, A-09

### Brief for Opus

You are reviewing three best_practice_synthesis blocks that were produced by Sonnet 4.5 (not Opus) due to an artifact proxy routing error. Your task is to review each synthesis, confirm or revise the key findings, and output amended best_practice_synthesis sections.

**Context:** The Accessible Built Environments Guidebook evidence hierarchy:
- Tier 1: OT clinical research (intervention-tested)
- Co-1: Lived experience / participatory design (CRPD Art. 4.3)
- Tier 2: Disability-led NGO / DPO advocacy guidelines
- Higher tiers govern on conflict. Sequencing: Ideal → Best Practice → Acceptable → Minimum.

**Task 1: fold-down-grab-bar-specification**
Load BPC at `references/bpc/grab-bar/fold-down-grab-bar-specification.md`.
Key finding to verify: WHO APS-15:2022 110 kg load rating is inadequate given measured peak transfer forces of ~1.3 kN (~130 kg). GAP-OPS-02 raised.
Your task:
1. Review the biomechanical reasoning. Is the 1.3 kN figure correctly interpreted? Is the WHO standard genuinely inadequate?
2. If confirmed: what is the highest-ambition defensible load rating specification?
3. If not confirmed: revise the finding and update GAP-OPS-02 status.
Output: Amended best_practice_synthesis section. Updated GAP-OPS-02 with Opus determination and rationale.

**Task 2: upper-limb-impairment-built-environment**
Load BPC at `references/bpc/upper-limb/upper-limb-impairment-built-environment.md`.
Key finding to verify: ADA 18-inch toilet centreline is described as "the most consequential evidence-practice conflict in guidebook."
Your task:
1. Review the evidence for toilet centreline positioning for upper-limb impairment. Is the ADA 18-inch standard genuinely in conflict with clinical evidence? Is this the most consequential conflict?
2. What is the correct specification range?
3. Does this finding change any population codes for toilet compartment items?
Output: Amended best_practice_synthesis section with confirmed or revised conflict assessment and specification range.

**Task 3: cross-population-conflict-resolutions**
Load BPC at `references/bpc/cross-population/cross-population-conflict-resolutions.md`.
Key finding to verify: Items A-04, B-05, A-09 contain unsupported values. GAP-OPS-01 raised.
Your task:
1. Review each of A-04, B-05, A-09 values. Which are unsupported and require [UNSUPPORTED — citation required] markers?
2. Review OFS/MCAS chemical sensitivity conflict: is it genuinely unaddressed or has it been resolved in a later BPC entry?
3. For any value you determine is defensible: identify the supporting evidence tier and source.
Output: Amended best_practice_synthesis section. Per-item verdict for A-04, B-05, A-09 (SUPPORTED / UNSUPPORTED + rationale). Updated GAP-OPS-01.

**Parallel Task: CON-0050–0084 MODERATE connections (20 items)**
Load connection register at `references/connection-register.md`, filter to CON-0050–0084 MODERATE entries.
Review each MODERATE connection. For each: ELEVATE to HIGH (include in Phase 3 item briefing) or DOWNGRADE to LOW (stays in gap register, no Phase 3 action).
Output: Updated status for each CON-005x–CON-008x MODERATE entry.

---

## Opus Review Session B — Consequential Judgments

**Priority:** HIGH — blocks finalisation of A-02, A-08, A-13, A-16, E-14; T0-03 decision  
**Prerequisite:** Session A complete (grab bar and centreline findings may affect some of these)

### Brief for Opus

You are reviewing five outputs that required consequential judgment and were produced by Sonnet 4.5. Review each, confirm or revise, output amendments.

**Task 1: acoustics-speech-intelligibility-disability**
Load BPC at `references/bpc/acoustics/acoustics-speech-intelligibility-disability.md`.
Key finding to verify: "0.6 s is the failure boundary, not a compliant specification." This framing correction affects items A-02, A-08, A-13.
Your task: Confirm or revise this boundary framing. If confirmed, state what the best-practice specification range is (not just the failure boundary). If revised, state the correct framing.
Output: Amended best_practice_synthesis section. Confirmed or revised boundary framing with supporting evidence.

**Task 2: sensory-relief-space-design**
Load BPC at `references/bpc/sensory/sensory-relief-space-design.md`.
Key finding to verify: Toilet adjacency was identified as underclaimed; approach sequence underclaimed. Mandatory status of toilet adjacency needs Opus confirmation.
Your task: Review evidence for toilet adjacency in sensory relief spaces. Is this mandatory (Tier 1/Co-1 evidence) or recommended (Tier 4/5)? Review approach sequence — what is the highest-ambition defensible specification?
Output: Amended best_practice_synthesis section. Explicit mandatory vs. recommended status for toilet adjacency with evidence basis.

**Task 3: ndv-aut-built-environment-quantified-thresholds**
Load BPC at `references/bpc/ndv/ndv-aut-built-environment-quantified-thresholds.md`.
Key finding to verify: Evidence gap is structural; process-based design is highest-ambition specification under thin evidence.
Your task: Review the evidence base. Is process-based design genuinely the highest-ambition specification, or does sufficient Tier 1/Co-1 evidence exist to support quantified thresholds? If process-based: what does process-based design look like as an actionable specification for architects?
Output: Amended best_practice_synthesis section. Confirmed or revised highest-ambition specification with evidence basis.

**Task 4: T0-03 Retreat/Reset Room rejection**
Load the T0 candidate assessment from the session record (session_2026-03-28-1715.md or session_2026-03-28-1830.md).
Key finding to verify: Retreat/reset room rejected from T0 status because sound attenuation provisions conflict with DEAF emergency communication access.
Your task: Is this conflict irresolvable, or can a provision structure preserve T0 status while meeting DEAF emergency requirements (e.g., visual alarm integration, tactile alerts, DEAF-aware room design)?
Output: Confirmed rejection with rationale, OR revised T0 candidate status with required provision modifications.

**Task 5: E-14 Entrance Rest Seating — specification confirmation**
Load item draft at `parts/v10/E-14-entrance-rest-seating.md` (or equivalent committed path).
Load BPC at `references/bpc/seating/seating-entrance.md`.
Key finding to verify: Dimensional corrections applied (440–480mm seat height, 1200mm alcove, recline mandatory Tier 1 OFS/PAIN). REF:seating-entrance:02 removed (hallucination). Three remaining citations need verification.
Your task: Review specification logic against BPC Key sources. Confirm specification is Phase 3-ready, or flag specific revisions. Note the three remaining citations — are they real and correctly attributed?
Output: E-14 verdict: PHASE-3-READY or REVISE with specific changes. Citation status for remaining three references.

---

## Opus Review Session C — Framework Synthesis

**Priority:** MEDIUM — required before Part 13 writing; pre-passthrough escalations should resolve before any affected item enters Phase 3  
**Prerequisite:** Sessions A and B complete

### Brief for Opus

You are reviewing two categories of earlier synthesis work. Review and confirm or revise.

**Task 1: residential-accessible-home-case-studies governing principles**
Load BPC at `references/bpc/residential/residential-accessible-home-case-studies.md`.
Review the 8 governing principles extracted from case study synthesis.
Your task: Confirm all 8 are accurate and appropriate for structuring Part 13 case study selection. Revise any that are overclaimed, underclaimed, or not supported by the evidence in the BPC.
Output: Confirmed or revised governing principles list with rationale for any changes.

**Task 2: Pre-passthrough escalation determinations**
Review the following in-session Sonnet escalation outputs from sessions 2026-03-17 through 2026-03-20:
- G-03 grab bar type conflict (session 2026-03-17 or nearest)
- Circulation geometry / turning circle
- A-08/A-13 acoustic conflict
- B-10 seizure safety provisions
- Sensory room provisions
- Circadian lighting

For each: load the relevant BPC entry. Review the escalation determination. Confirm or revise.
Output: Per-item verdict (CONFIRMED / REVISED with changes). If revised: updated best_practice_synthesis section for affected BPC.

---

## Phase 3 Gate

Phase 3 writing cannot begin on the following items until the specified session is complete:

| Item(s) | Blocking session |
|---|---|
| All grab bar items | Session A (Task 1) |
| All toilet compartment items with ADA 18-inch centreline | Session A (Task 2) |
| A-04, B-05, A-09 | Session A (Task 3) |
| A-02, A-08, A-13 | Session B (Task 1) |
| A-16 | Session B (Task 2) |
| E-14 | Session B (Task 5) |
| Part 13 (case studies) | Session C (Task 1) |
| G-03, circulation items | Session C (Task 2) |

All other items may proceed to Phase 3 with standard evidence-auditor review.

---

## What Does Not Need Redoing

| Item | Reason |
|---|---|
| All Sonnet assembly / drafting / formatting | Correctly attributed throughout |
| CON-0001–0038 connections | In-session Sonnet work; appropriate model |
| CON-0085–0092 external connections | Correctly attributed to Sonnet + web search |
| INTRA/INTER/BOTH tagging | Appropriate Sonnet task |
| Gap register entries from synthesis sessions | Gaps are real even if model attribution was wrong |
| REF:seating-entrance:02 deletion | Correct regardless of model |
| T0 CONFIRMED candidates (B-12, E-10, E-12, E-13) | Actioned; reverting would cause more disruption than benefit |
| CON-0050–0084 HIGH connections (14) | Confirmed across multiple evidence streams; accept |

---

*End of work triage plan*
