---
name: content-gap-analyzer
description: >
  Analyze accessibility guidebook sections for content gaps against a comprehensive evidence taxonomy
  covering all disability and neurological populations. ALWAYS use this skill when asked to: find
  content gaps, check population coverage, identify missing topics, review what's missing, assess
  completeness of coverage, check if neurodivergent users are addressed, or conduct systematic
  content reviews. Trigger on: "what's missing", "coverage gaps", "content review", "are we
  covering", "systematic review", "completeness check".
---

**Intake:** ≤500 lines only. Full document → haiku-chunker first.
**Model:** Sonnet 4.6
**Population codes:** → `references/project-standards.md` (do not substitute or collapse)
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API

## Steps
1. **Inventory:** List all sections/topics in scope; tag with declared Part II category codes.
2. **Coverage map:** For each section × each Part II code: ✅ addressed with evidence + criteria · ⚠️ mentioned, no evidence · ❌ absent · N/A
3. **Evidence type check:** Design criteria present? · Evidence cited? · OT rationale? · Lived experience? · Part III co-occurrences?
4. **Vol II item audit** (when Vol II in scope):
   - Extract item codes → record declared categories → audit against full taxonomy
   - Flag: category that *should* be affected but absent (e.g. tactile indicator: VIS only → missing DEM, NDV/MH)
   - Flag: missing cross-references; unaddressed Part III co-occurrences; no evidence tier
   - Add columns: `Item Code | Declared Categories | Missing Categories | Missing Cross-refs | Evidence Tier`
5. **Thematic review:** Flag cross-section absences — wayfinding (cognitive/visual/NDV) · rest/recovery (fatigue) · sensory env · thermal (Uhthoff) · emergency egress (all codes) · maintenance accessibility
6. **Output:**
   - Population coverage heatmap (sections × Part II codes)
   - Priority gaps (HIGH): `[Section] | [Code] | [Gap] | [Suggested source]`
   - Secondary gaps (MED)
   - Thematic gaps
   - Research tasks for multilingual-research: `Topic | Search terms | Languages | Source types`
   - Gap YAML per item → append to `gap_register.md` on GitHub (GET + append + PUT per Project Instructions §GitHub API):
     ```yaml
     id: GAP-XXX
     type: evidence|framing|citation|format|code|cross-ref
     section: "..."
     description: "[one sentence — what is missing and why it matters]"
     priority: P1|P2|P3
     status: OPEN
     skill_responsible: content-gap-analyzer
     date: YYYY-MM-DD HH:MM
     ```
     Or in compact register format: `GAP-XXX | P{1|2|3} | OPEN | content-gap-analyzer | {section} | {description} | {YYYY-MM-DD HH:MM}`
