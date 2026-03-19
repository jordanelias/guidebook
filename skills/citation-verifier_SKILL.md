---
name: citation-verifier
description: >
  Verify citations, evidence claims, and source credibility for accessibility and built environment
  documents. ALWAYS use this skill when asked to audit citations, check references, verify evidence,
  flag hallucinated sources, confirm source credibility, or perform any evidence quality review.
  Trigger on: "check citations", "verify sources", "audit references", "is this claim supported",
  "evidence review", "citation audit". Essential for any accessibility guidebook review workflow.
---

**Intake:** ≤500 lines only. Full document → haiku-chunker first.
**Model:** Sonnet 4.6
**Never assume a source exists. Confirm via tool lookup or mark UNVERIFIED.**
**Sources/journals:** → `references/project-standards.md`
**Output schema:** → `references/project-standards.md` (fields: claim_id, section, claim_text, source, claim_type, confidence, citation_status)
**SelfCheck:** HIGH-confidence citations → assess twice with different framing; divergence = UNCERTAIN_REVIEW

## Steps
1. Extract all citations, implicit claims, standards refs, statistical claims → `[claim_id | text | citation | type]`
2. Classify each: type (empirical/standard/guideline/expert-opinion/anecdotal) · priority (HIGH/MED/LOW) · verifiability (tool-searchable/standards-lookup/unknown)
3. Verify:
   - Peer-reviewed → PubMed → Consensus → Scholar Gateway (max 3 tools/citation)
   - Standards → ISO, IEC, AODA, ADA, NBC, AS 1428, BS 8300, EN 17210, WCAG, UN CRPD
   - Statistical claims → trace to primary source; flag secondary-only
   - Implicit claims → flag for manual review + suggested search terms
4. Output:

**A. Verified Citations Table**
| ID | Claim | Source | Status | Notes |

Status codes: CONFIRMED · MISMATCH · UNNUMBERED · UNRESOLVABLE · UNVERIFIED · NOT_FOUND

**B. Information Gaps:** claim text · suggested replacement · search terms · severity (foundational/supporting/contextual)

**C. Claim objects (YAML)** — one per flagged item per schema

## Connectors
PubMed, Consensus, Scholar Gateway — activate for verification only.
