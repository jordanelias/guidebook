---
name: framing-checker
description: >
  Check guidebook text for social model framing regressions. ALWAYS use this skill when asked to:
  review framing, check language, audit for medical model language, check CRPD alignment, review
  disability language, or verify social model consistency. Run at every draft before publication.
  Trigger on: "check framing", "review language", "social model check", "CRPD alignment",
  "framing regression", "disability language audit", or when framing-checker is called in
  workplan-orchestrator Full Section Review workflow.
---

**Intake:** ≤500 lines only. Full document → haiku-chunker first.
**Model:** Sonnet 4.6 only — never Haiku.
**Passes:** 2. After Pass 1: ground in CRPD Article 9 + social model definition before Pass 2. No changes without external grounding.
**Output schema:** → `references/project-standards.md` (fields: claim_id, section, claim_text, framing_flag)

## Flag Categories
| Code | Flag | Examples |
|------|------|---------|
| MEDICAL_MODEL | Diagnosis as design rationale | "blind people need...", "persons with dementia require..." |
| COMPLIANCE_COST | Disability as cost | "accommodation expense", "cost of providing access" |
| PASSIVE_CENTERING | Disability as problem | "inaccessible to wheelchair users" (→ "design excludes...") |
| ACCOMMODATION_BURDEN | Disability as add-on | "special needs", "accommodating disabled people" |
| CAPABILITY_DEFICIT | Deficit language | "suffers from", "wheelchair-bound", "confined to" |
| CRPD_INCONSISTENT | Rights framing absent | access as charity/accommodation, not right (CRPD Art.9/19) |
| UNIVERSAL_EROSION | Universal design undermined | "disabled-friendly features", "special accessible route" |

Do not flag: "people who use wheelchairs" · population codes (MOB, VIS, etc.) · identity-first language (autistic, Deaf)

## Steps
1. Scan for instances of each flag category. List: exact quote · location · proposed code.
2. Confirm/reject each. Assign severity: 🔴 HIGH (published; credibility risk) · 🟡 MED (ambiguous) · 🟢 LOW (editorial). Draft reframe.
3. Pass 2: re-read CRPD Art.9 + social model definition. Confirm/upgrade/downgrade each Pass 1 flag.
4. Output:

| ID | Location | Flag | Original Text | Severity | Suggested Reframe |

Claim objects (YAML) — one per flagged item.
Summary: X flags — Y 🔴 / Z 🟡 / W 🟢 · Regression risk: HIGH/MED/LOW/CLEAN
