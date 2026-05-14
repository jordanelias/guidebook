# Authority-Implying Language Audit — V9.0

**Scan date:** 2026-03-28
**Scope:** Full guidebook (6683 lines, 553KB)
**Purpose:** Identify language that implies the guidebook has institutional authority, clinical validation, or regulatory standing it does not possess.

---

## Problem Statement

The guidebook is one team's best reading of the evidence. It has not been:
- Field-tested across building types or jurisdictions
- Peer-reviewed by a standards body
- Validated through post-occupancy evaluation at scale
- Endorsed by any professional registration authority

Language that implies otherwise creates liability risk for practitioners who rely on it and credibility risk for the project.

---

## Category 1: Self-Governing Language

The guidebook positions itself as a governing document — language appropriate for a standard or regulation, not a guidance resource.

| Line | Text | Problem | Replacement |
|---|---|---|---|
| 369 | "Where this document requires more than statutory requirements, **this document governs**." | Asserts regulatory authority over statutory codes | "Where this document recommends more than statutory requirements, the practitioner should consider the higher provision and document the rationale for the standard adopted." |
| 191 | "This document **operates above the code floor** throughout." | Positions the document as a parallel regulatory instrument | "This document **recommends provisions above the code floor** throughout." |
| 193 | "Every specification in this document **is calibrated** above code" | Implies engineering-grade validation | "Every specification in this document **is set** above code" |
| 21 | "This guidebook **operates** above the code floor throughout" | Same as L191 | Same fix — "recommends provisions above" |
| 301 | "The following tier structure **governs** source prioritisation throughout this document." | Acceptable (internal document governance) but sets a pattern | No change needed — this governs the document's own method |
| 5233 | "Where OT assessment findings conflict…the OT assessment **governs** for the individual concerned." | Acceptable — OT authority is legitimate | No change needed |
| 199 | "The **governing principle** is: design must accommodate the actual functional capacity…" | "Governing principle" implies regulatory status | "The **organising principle**" or "The **core principle**" |

**Pattern:** "governs" is used 12 times. ~4 instances assert the guidebook's authority over other instruments (problematic). ~8 instances describe internal logic or legitimate OT authority (acceptable).

---

## Category 2: Protocol / Framework Language

Terms that imply clinically validated, field-tested procedures.

| Line | Text | Problem | Replacement |
|---|---|---|---|
| 766 | "see Part 8 §8.4.4 for **resolution protocol**" | Implies validated protocol | "see Part 8 §8.4.4 for **conflict reasoning guidance**" or "**recommended resolution approach**" |
| 1008 | "### 4.6 **Decision Framework** for Sequencing Techniques" | "Framework" implies validated structure | "### 4.6 **Reasoning Sequence** for Sequencing Techniques" or "**Considerations for** Sequencing Techniques" |
| 5062 | "## 9.3 **Stage-Gated Coordination Protocol**" | "Protocol" implies validated procedure | "## 9.3 **Stage-Gated Coordination Sequence**" or "**Coordination Approach by Stage**" |
| 5331 | "## 9.7 **Coordination Protocol** Across All Specialist Consultants" | Same | "## 9.7 **Coordination Guidance** Across All Specialist Consultants" |
| 844 | "FM **protocol** for sensory environment maintenance" | FM context — "protocol" is industry-standard here | No change — FM protocols are legitimate operational documents |

**Pattern:** "protocol" appears 14 times. ~3 are self-referential (problematic). ~8 reference external protocols (Motionspot, PEEP, FM — all legitimate). ~3 are in conflict resolution contexts (should be "guidance" or "approach").

---

## Category 3: Mandatory / Non-Negotiable / Must

The guidebook cannot mandate anything. It can recommend, and it can explain consequences of not following recommendations.

| Line | Text | Problem | Replacement |
|---|---|---|---|
| 239 | "DAR…is **mandatory** at every tier without exception." | Guidebook cannot impose mandates | "DAR…**applies** at every tier." or "DAR is **recommended** at every tier; omission removes future adaptability." |
| 1262 | "They are **non-negotiable** and must appear on the stated drawing" | Same | "These provisions are **critical to access outcomes** and should appear on the stated drawing" |
| 1773 | "They are **non-negotiable** for any new or substantially refurbished building." | Same | "These provisions are **fundamental to access** for any new or substantially refurbished building." |
| 1891 | "mandatory **non-negotiable** workplace provision" | Double assertion of authority | "essential workplace provision" |
| 4838 | "**Stage sequencing is non-negotiable.**" | Same | "**Stage sequencing is critical.** Items deferred past their declared stage gate may become physically impossible or prohibitively expensive." |
| 243–245 | Tier table: "Mandatory" in every row | The tiers describe the guidebook's own structure — "mandatory" overstates | Replace with "Applies" or "Required by this guidebook's methodology" (the latter is honest about the source of the requirement) |

**Pattern:** "mandatory" appears 22 times. ~8 refer to external mandates (Norwegian standard, statutory requirements — legitimate). ~14 are the guidebook asserting its own mandates (problematic). "Non-negotiable" appears 6 times, all self-asserted.

**Note on "must":** 82 occurrences. Many are legitimate technical constraints ("must be visible from ≥5 m"). The problematic ones are where "must" enforces a guidebook-internal rule as though it were externally binding. A systematic must→should pass would be overkill; the fix is to address the framing *around* "must" (i.e., making clear the guidebook recommends, not mandates).

---

## Category 4: Authoritative Source Claims

| Line | Text | Problem | Replacement |
|---|---|---|---|
| 6269 | "This is the **authoritative bibliography** for the Guidebook." | Claims authority the document hasn't earned externally | "This is the **consolidated bibliography** for the Guidebook." or "**reference bibliography**" |
| 293 | "both are below the **best-practice standard set by this guidebook**" | Asserts the guidebook defines a standard | "both are below the **best-practice level recommended in this guidebook**" |

---

## Category 5: Inclusive Design Instruments

| Line | Text | Problem | Replacement |
|---|---|---|---|
| 235 | "All specifications…in this document are **inclusive design instruments**" | "Instruments" implies validated tools with measured efficacy | "All specifications…in this document are **inclusive design resources**" or "**evidence-informed design guidance**" |

---

## Category 6: Categorical / Absolute Intervention Language

| Line | Text | Problem | Replacement |
|---|---|---|---|
| 2438 | "This item implements a **categorical** EHP 'prevent' intervention." | "Categorical" is accurate to EHP terminology here | No change — this describes the EHP strategy type, not the guidebook's authority |
| 2634 | "this item implements a **categorical prevent** intervention" | Same — EHP terminology | No change |

---

## Category 7: Design Discipline Framing

| Line | Text | Problem | Replacement |
|---|---|---|---|
| 913 | "Items are treated as a compliance list rather than as a **design discipline**." | Implies the guidebook constitutes a discipline | "Items are treated as a compliance list rather than as **an integrated design approach**." |
| 931 | "The design stage column in Part 7 is not a suggested timeline — **it is a constraint**." | Asserts binding constraint | "The design stage column in Part 7 is a **critical consideration** — items not decided at the indicated stage risk becoming physically impossible or prohibitively expensive to incorporate later." |

---

## Summary of Required Changes

| Category | Instances Found | Problematic | Action Required |
|---|---|---|---|
| Self-governing language | 12 | 4 | Reframe to "recommends" / "organising principle" |
| Protocol/framework | 14 | ~6 | Replace with "guidance" / "reasoning sequence" / "approach" |
| Mandatory/non-negotiable | 28 | ~20 | Replace with consequence-based framing |
| Authoritative claims | 2 | 2 | Replace "authoritative" / "standard set by" |
| Instruments | 2 | 1 | Replace with "resources" / "guidance" |
| Categorical | 2 | 0 | No action (legitimate EHP terminology) |
| Design discipline | 2 | 2 | Reframe |

**Total problematic instances: ~35**

---

## Recommended Global Reframing Principle

Replace **authority-asserting** language with **consequence-describing** language throughout.

Instead of: "This is mandatory / non-negotiable / required / the document governs"
Use: "This is recommended because [consequence of omission]. The evidence supporting this recommendation is [tier]."

This approach:
1. Preserves the urgency (practitioners still understand the stakes)
2. Removes the false authority claim
3. Aligns with the stated position that the guidebook is "a framework for professional judgment, not a substitute"
4. Lets the evidence do the persuading, not the framing

---

## Proposed Preamble Addition (Volume 1, before §1.1)

> **Status of this document.** This guidebook assembles the best available evidence from occupational therapy clinical research, lived experience, and international standards to inform design decisions for accessible built environments. It is not a standard, a regulation, or a clinically validated protocol. It has not been field-tested across building types or jurisdictions. Where it uses terms like "should," "recommended," or "critical," these reflect the strength of the underlying evidence, not a claim of regulatory or institutional authority. Practitioners are expected to exercise professional judgment, consult applicable statutory requirements, and engage directly with occupational therapists and disabled people in making design decisions. The guidebook supports that process; it does not replace it.

---

## Gap Register Entry

**ID:** GAP-LANG-001
**Type:** FRAMING
**Priority:** P1
**Description:** Authority-implying language throughout V9.0 (~35 instances across 7 categories). Requires systematic replacement with consequence-based framing before any external distribution.
**Status:** OPEN
