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
| BAR_IN_VOLUME_I | BAR reference in Volumes 1–3 | Any mention of BAR, bariatric, or large body size provisions outside Supplementary Volume. BAR is not a main-taxonomy code. |
| MARKER_FRAMING | Evidence marker misuse | ● on a sentence with no citation; ○ without gap disclosure; marker on non-prescriptive text |
| AUTHORITY_CLAIM | Guidebook asserts authority it lacks | "this document governs", "mandatory", "non-negotiable", "resolution protocol", "authoritative", "decision framework" — any language implying regulatory, institutional, or clinically validated standing |

Do not flag: "people who use wheelchairs" · population codes (MOB, VIS, etc.) · identity-first language (autistic, Deaf)

## BAR-in-Vol-I Check (v10.1 addition)

Scan all input text for:
- The string "BAR" used as a population code or category label
- "bariatric" as a design category reference (not as a clinical descriptor in evidence citations)
- "large body size" in specification or matrix contexts (acceptable in Supplementary Volume only)
- BAR row/column in any co-occurrence matrix, application matrix, or population table
- Cross-references to "Category J" or "J-01" through "J-05" in Volumes 1–3

Any match in Volume I, II, or III content → flag as BAR_IN_VOLUME_I with 🔴 HIGH severity.

## Evidence Marker Awareness (v10.1 addition)

When scanning text that contains ● or ○ markers:
- Check that ● sentences have a corresponding citation in the evidence table or inline
- Check that ○ sentences include a gap disclosure or `[Expert consensus]` note
- Flag markers on non-prescriptive text (definitions, rationale, cross-references) as MARKER_FRAMING
- Do not flag markers on non-prescriptive text (definitions, rationale, cross-references) as MARKER_FRAMING
- Do not flag the markers themselves as framing issues — they are an evidence system, not a framing choice

## Authority-Claim Check (v10.2 addition)

The guidebook is not a standard, regulation, or clinically validated protocol. Language that implies otherwise creates liability and credibility risk. Scan for:

**Self-governing language:** "this document governs" / "this guidebook governs" (when asserting authority over external instruments — acceptable when describing internal document logic); "operates above" (→ "recommends provisions above")

**Protocol/framework as self-description:** "resolution protocol" / "decision framework" / "coordination protocol" when describing the guidebook's own content (→ "reasoning guidance" / "reasoning sequence" / "coordination guidance"). Acceptable when referencing external protocols (PEEP, FM, Motionspot).

**False mandate language:** "mandatory" / "non-negotiable" / "must" when the guidebook asserts a requirement it has no authority to impose. Replace with consequence-based framing: explain *what happens* if the provision is omitted, not *that it is mandated*. Acceptable when citing external mandates (statutory, standards body).

**Authoritative source claims:** "authoritative bibliography" / "best-practice standard set by this guidebook" / "inclusive design instruments" (→ "consolidated bibliography" / "best-practice level recommended" / "inclusive design resources")

**Reframing principle:** Replace authority-asserting language with consequence-describing language. "This is mandatory" → "Omitting this removes future adaptability." Same urgency, no false authority.

Any match → flag as AUTHORITY_CLAIM. Severity: 🔴 HIGH if the text could be read as asserting regulatory or clinical authority; 🟡 MED if ambiguous; 🟢 LOW if editorial only.

## Steps
1. Scan for instances of each flag category (including BAR_IN_VOLUME_I, MARKER_FRAMING, and AUTHORITY_CLAIM). List: exact quote · location · proposed code.
2. Confirm/reject each. Assign severity: 🔴 HIGH (published; credibility risk) · 🟡 MED (ambiguous) · 🟢 LOW (editorial). Draft reframe.
3. Pass 2: re-read CRPD Art.9 + social model definition. Confirm/upgrade/downgrade each Pass 1 flag.
4. Output:

| ID | Location | Flag | Original Text | Severity | Suggested Reframe |

Claim objects (YAML) — one per flagged item.
Summary: X flags — Y 🔴 / Z 🟡 / W 🟢 · Regression risk: HIGH/MED/LOW/CLEAN
