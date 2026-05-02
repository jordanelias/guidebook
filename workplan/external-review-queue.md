# External Review Queue

**Status:** Decision-support document
**Authoring:** Opus 4.7 audit-remediation session 2026-05-01
**Audit basis:** audit_2026-04-30 R10 (treat A10–A13 governance corpus as one block for external review) + R11 (treat external review as gating per Sonnet's E1, not optional). Cross-reference: Sonnet's `references/audits/critical-workplan_2026-04-30.md` §2.3 E1/E2/E3.
**Recommendation type:** vector→reviewer mapping; the project owner commissions reviews.

---

## 1. Purpose

The audit's R10 finding flagged that A10 (adversarial-use), A11 (legal-regulatory), A12 (decision-protocol), and A13 (doctrine-recheck) all received same-conversation Opus drafting + same-conversation Opus self-review, no fresh-context external pass, and form a tightly cross-referenced governance bloc. R11 found that Sonnet's audit-companion already lists three external work items (E1/E2/E3) that do not have explicit reviewer-mapping in the project's records.

This document combines both: a single queryable register of (a) which items need external eyes, (b) what kind of reviewer for each, (c) how items can be batched to reduce reviewer load, (d) what the project commits to do with the responses.

---

## 2. Item inventory

| Item ID | Source | Description | Severity | Reviewer type |
|---|---|---|---|---|
| EQ-01 | A10 / catalog v2 | Adversarial-use vector V-01 (Minimum-compliance weaponization) — review mitigations for sufficiency | HIGH | Disability studies / disability rights advocacy |
| EQ-02 | A10 / catalog v2 | V-02 (Exclusionary ROI) — review CRPD-grounded counter-framing | HIGH | Disability studies + economist with disability-law focus |
| EQ-03 | A10 / catalog v2 | V-03 (Surveillance via inferred functional needs) — review A7 §3.4 framing | HIGH | Disability studies + privacy/surveillance scholar |
| EQ-04 | A10 / catalog v2 | V-04 (Selective citation) — review A6 §3.2 convergence-record sufficiency | MEDIUM | Methodology reviewer (E1 below) |
| EQ-05 | A10 / catalog v2 | V-05 (Co-1 instrumentalization) — review A5 verification protocol | HIGH | Disability studies (Co-1) |
| EQ-06 | A10 / catalog v2 | V-06 (Evidence-tier laundering) — review tier-validator coverage | MEDIUM | Methodology reviewer (E1) |
| EQ-07 | A10 / catalog v2 | V-07 (Anti-DAR deferral) — pending Part 10 draft; flagged for re-review at v10.x | MEDIUM | Defer to Part 10 close |
| EQ-08 | A10 / catalog v2 | V-08 (Adversarial litigation citation) — counsel review of §3.3 disclaimer | HIGH | Disability-law counsel (mandatory per A11 §6) |
| EQ-09 | A10 / catalog v2 | V-09 (Population-proxy denial) — IntD proxy decision adversarial-use review | MEDIUM | Self-advocacy DPO (Inclusion International or local affiliate) |
| EQ-10 | Sonnet E1 | Methodology review (2-3 reviewers OR journal submission) | gating | Methodology reviewer (research design / evidence synthesis) |
| EQ-11 | Sonnet E2 | DPO outreach (single-pass review) | gating | DPO partner — IntD self-advocacy, Deaf cultural, Global South |
| EQ-12 | Sonnet E3 | Workflow-integration scoping | non-gating | BIM / OT / code-commentary integrator (no commitment) |
| EQ-13 | A11 / legal-regulatory.md §6.2 | L-Q1 (negligent-misrepresentation exposure) | HIGH | Disability-law counsel |
| EQ-14 | A11 / legal-regulatory.md §6.2 | L-Q2 (fitness-for-purpose disclaimer wording) | HIGH | Disability-law counsel |
| EQ-15 | A11 / legal-regulatory.md §6.2 | L-Q3 (CC-BY licensing of best-practice synthesis) | MEDIUM | Counsel + IP/licensing expert |
| EQ-16 | A11 / legal-regulatory.md §6.2 | L-Q7 (jurisdictional disclaimer scope) | HIGH | Disability-law counsel |
| EQ-17 | A11 / legal-regulatory.md §6.2 | L-Q8 (litigation-defense provisional language) | HIGH | Disability-law counsel |
| EQ-18 | A12 / decision-protocol §1 | Categories (D-DOCT/D-METH/D-OP/D-SCHEMA/D-PRES) classification scheme — external review of taxonomy choices | LOW | Methodology reviewer (E1) |
| EQ-19 | A13 / doctrine-recheck §3.2 | Four-state contamination rubric (CLEAN/AMBIGUOUS/STUB/MERGED) — external review of rubric clarity | LOW | Methodology reviewer (E1) — see RC-002 finding RC-002-001 |
| EQ-20 | Audit / R12 | Three [STRUCK] claim residue — re-source attempt or removal-with-rationale | non-review | Internal Opus session (per Block 32 protocol) — not external review |
| EQ-21 | Audit / R1 + R4 + D-0120 | governance/migration-survival.md (CANONICAL 2026-05-02) — single-context governance authored alongside its recommending audit; external review queued non-blocking per D-0120 adoption framing | MEDIUM | Methodology reviewer (E1) + disability-studies reviewer (cross-cut); see workplan/external-review-outreach-drafts.md Batch 6 |

---

## 3. Reviewer-type mapping

Five reviewer profiles are needed. Items can be batched within profile to reduce reviewer load:

### 3.1 Disability-law counsel (combined batch)

**Items:** EQ-08, EQ-13, EQ-14, EQ-15 (joint w/ IP), EQ-16, EQ-17 (= 6 items)
**Materials to provide:**
- governance/legal-regulatory.md (full)
- governance/adversarial-use-framework.md §1.5 + §2.5 (V-08-related)
- data/adversarial_use/catalog.yaml v2 vector V-08 entry
- The five A11 §6.2 questions L-Q1, L-Q2, L-Q3, L-Q7, L-Q8

**Single review pass; targeted questions to bound effort.**
**Outcome:** counsel response document → A11 §7.1 cleared/cleared-with-notes status update + V-08 transition.

### 3.2 Disability studies / disability rights scholar (combined batch)

**Items:** EQ-01, EQ-02 (joint w/ economist), EQ-03 (joint w/ privacy), EQ-05 (= 4 items, with optional 2 additional reviewers for joint topics)
**Materials:**
- governance/mission-and-epistemics.md
- governance/adversarial-use-framework.md
- governance/co1-operational.md
- A7 §3.3, §3.4 from population-taxonomy.md
- catalog v2 vectors V-01, V-02, V-03, V-05

**Outcome:** mitigation-strengthening recommendations OR vector-status changes (CLEARED → ESCALATED if mitigation gap surfaced).

### 3.3 Methodology reviewer (combined batch — E1)

**Items:** EQ-04, EQ-06, EQ-10, EQ-18, EQ-19 (= 5 items in single review)
**Profile:** research design + evidence synthesis methodology (e.g., Cochrane systematic-review methodologist, evidence-based design researcher).
**Materials:**
- governance/evidence-methodology.md (full)
- governance/co1-operational.md (full)
- governance/decision-protocol.md (A12)
- governance/doctrine-recheck.md (A13) + RC-001/RC-002 records
- A6 evidence-state machine + A6 validators
- 2-3 sample BPCs covering CLEAN/AMBIGUOUS dispositions

**This is Sonnet's E1 — the most extensive single-reviewer ask. Can be split between two reviewers if one is unavailable for the full batch.**

### 3.4 DPO partner — IntD self-advocacy (single-pass)

**Items:** EQ-09, EQ-11 (partial — IntD slice)
**Profile:** Inclusion International or national affiliate (e.g., Inclusion Canada, Inclusion Europe, People First).
**Materials:**
- IntD coverage map (DEM + NDV proxy decision; A7 §1.1)
- BPCs covering NEU + DEM proxy positions
- catalog v2 vector V-09

**Single review pass; specific question: is the proxy decision adequate or should IntD be promoted to a primary code with own BPCs?**

### 3.5 DPO partner — Deaf cultural representation (single-pass)

**Items:** EQ-11 (partial — Deaf slice)
**Profile:** WFD or national affiliate.
**Materials:**
- DEAF BPCs (assistive-listening, visual-alerting, deafblind-overlap)
- A7 DEAF code + DBL deaf-blind code
- governance/co1-operational.md §Co-1 corpus

### 3.6 DPO partner — Global South representation (single-pass)

**Items:** EQ-11 (partial — Global South slice)
**Profile:** UN-Habitat or IDA partner.
**Materials:**
- Jurisdiction-philosophy.md + jurisdiction coverage matrix (24 jurisdictions present; 5+ Global South gaps)
- A8 §3 jurisdictional currency framework

---

## 4. Batching rationale

The 20 items above could in principle generate up to 20 separate review requests. Batching reduces this to 5-7 reviewer engagements:

- 1 counsel batch (EQ-08, 13, 14, 15, 16, 17) — single firm, single retainer
- 1 disability-studies batch (EQ-01, 02, 03, 05) — single reviewer or co-reviewer pair
- 1 methodology batch (EQ-04, 06, 10, 18, 19) — Sonnet's E1 + audit/R10 governance batch combined
- 1 IntD DPO batch (EQ-09, 11-IntD) — single DPO
- 1 Deaf DPO batch (EQ-11-Deaf) — single DPO
- 1 Global South DPO batch (EQ-11-GS) — single DPO
- (EQ-12 BIM/OT/code-commentary) — scoping, not review; deferrable

This is **6 review engagements**, not 20. Per Sonnet's E1/E2 lead-time estimates (4-12 weeks E1, 4-8 weeks E2), the engagements run in parallel from Phase B start.

---

## 5. Audit R10 specific recommendation

R10 said: "treat A10–A13 governance corpus as one block for external review rather than four." This document operationalises that by:

- Combining all A10/A11/A12/A13-derived items (EQ-01..EQ-09, EQ-13..EQ-19 = 16 items) into 3 reviewer batches (counsel + disability-studies + methodology) rather than 16 separate reviews.
- The methodology batch (EQ-04, 06, 18, 19) gets the cross-A12/A13 view that single-document review would miss.
- Single review pass per batch (no iteration loop) per Sonnet's E1 framing.

The cross-document review is what catches inconsistencies between A10 mitigations and A12 delegation classifications, between A11 disclaimer wording and A13 recheck triggers — none of which were checked in same-conversation drafting.

---

## 6. Audit R11 specific recommendation

R11 said: "Treat external review (E1) as gating, not optional." Sonnet's critical-workplan §2.3 already frames E1/E2/E3 as parallel-to-Phase-B; the gating question is what counts as "having attempted." This document recommends:

- **Gating-on-attempt:** outreach made, materials sent, deadline communicated, response logged (or non-response logged after deadline + 2 weeks).
- **Gating-on-incorporation:** response received, incorporation decisions made (incorporate / acknowledge / reject with rationale), changes captured in commit log.
- **NOT gating-on-favorable-response:** the project does not require external endorsement to launch; it requires having tried and documented.

This matches Sonnet's "do not gate launch on full responsiveness, only on having attempted and documented" framing. R11's stronger "gating, not optional" framing is honored as: outreach is mandatory (gating-on-attempt); favorable response is not (gating-on-favorable-response is not adopted).

---

## 7. What this document does not do

- It does not commission any review. Reviewer recruitment is project-owner work.
- It does not name specific reviewers. Naming is project-owner choice (and confidentiality may apply).
- It does not commit a budget. Reviewer fees and DPO honoraria are out of scope.
- It does not produce review materials. Material packaging happens at engagement time.
- It does not pre-empt response handling. Each reviewer's response gets a Decision record at incorporation.

---

## 8. Status

| Field | Value |
|---|---|
| Status | DRAFT — recommendation only |
| Adoption | OPTIONAL — batching is recommendation, not requirement |
| Pairs with Decision | none until adopted |
| Author | opus_4.7_session_2026-05-01_audit-remediation |

End of external-review queue.
