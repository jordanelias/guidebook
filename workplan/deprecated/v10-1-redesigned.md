# Workplan: Guidebook v10.1 — Redesigned Comprehensive Revision

**Created:** 2026-03-24 22:00
**Supersedes:** Workplan_v10-0_Integrated_2026-03-20-1.md
**Basis:** Systematic Audit Report 2026-03-24; Critique Report v9.0 2026-03-20
**Principle:** Content determines structure. Audit before research. Research before writing. Structure once, at the end.

---

## What Changed From v10.0

| Area | v10.0 plan | v10.1 plan | Rationale |
|---|---|---|---|
| Part 8 | Absorbed §3.4 into §4.9; no dedicated Part | **New Part 8: Cross-Population Resolution & Cross-Disciplinary Collaboration** — dedicated part; expanded audience | Audit §5.2 / §4.6: cross-population content is the document's highest-value intellectual contribution; it deserves dedicated treatment, not absorption into synthesis |
| Audience scope (Part 8) | Architects + designers only | Architects + OTs + specialty consultants + engineers | User directive: novel territory requires broader disciplinary lens |
| Cross-disciplinary collaboration | Not addressed | Part 10 reconceived as **Interdisciplinary Design Team** — not just "specialist consultants to engage" but collaboration protocols, handoff frameworks, shared vocabulary | User directive: cross-disciplinary collaboration, not just architect+consultant |
| Economics | Concision pass only | **Intensified**: pro forma templates, development ROI models, insurance/liability data, cost studies by building type, value proposition frameworks | User directive: intensify economic analysis |
| Case studies | Keep or select from existing 14 | **Expand + systematically mine**: (a) mine existing 14 for Part 7 evidence upgrades; (b) source 6–10 new case studies targeting thin populations; (c) use case studies as formal evidence base | Audit §5.4: case study evidence loop; user directive: more case studies |
| Pre-v4 slug handling | Assumed CHECK would work | **Dedicated triage session**: assess all 51 pre-v4 slugs for Co-1/Tier 2 adequacy before deciding re-run vs. consume | Audit §5.1: protocol inversion means pre-v4 slugs can't be trusted without assessment |
| BPC↔Item mapping | Not planned | **New infrastructure**: bidirectional `part7_items` in BPC; `bpc_slugs` in item specs | Audit §5.5: no traceability chain currently exists |
| Slug coverage | Per-slug as needed | **Systematic coverage plan**: all 62 unique slugs assessed; backfill targets defined; jurisdiction coverage gaps closed | Audit §2.1: 88% missing jurisdiction_coverage; 100% missing best_practice_synthesis |
| Phase 0 | 3 sessions | 2 sessions (compressed by dependency-tier batching) | Token efficiency |
| Phase 1 | 4 sessions | 3 sessions (combined Vol I + Vol II front matter) | Token efficiency |
| Phase 5 | 3 sessions | 2 sessions (combined QA passes) | Token efficiency |
| Total | 25 sessions | 24 sessions | Net -1 despite expanded scope |

---

## Structural Architecture — v10.1

### Part Numbering (Final)

| Part | Title | Volume | Status |
|---|---|---|---|
| 1 | Foundations of Accessible Design | I | Revision |
| 2 | Disability Categories | I | Revision |
| 3 | Designing for Multiple Disability Categories | I | Revision |
| 4 | Synthesis and Sequencing | II | Revision |
| 5 | Residential Application Matrices | II | Revision |
| 6 | Non-Residential Application Matrices | II | Revision |
| 7 | Item Specification Library | II | Revision |
| **8** | **Cross-Population Resolution & Cross-Disciplinary Collaboration** | **II** | **NEW** |
| 9 | Engineering and Coordination | II | Was Part 9/V; revision |
| 10 | Interdisciplinary Design Team | II | Was Part 10 "Specialist Consultants"; **reconceived** |
| 11 | Design for Adaptable Readiness — DAR | III | Was Part 11/VII; revision |
| 12 | The Economics of Accessible Construction | III | Was Part 12/VIII; **intensified** |
| 13 | Case Studies and Built Evidence | III | Was Part 13/IX; **expanded** |
| Apps | Appendices A–E, Bibliography, Glossary | III | Revision |
| Supp | Supplementary Volume: Body Sizes | — | Revision |

### Part 8 — Architecture (New)

**Audience:** Architects/designers + OTs/practitioners + specialty consultants (acoustic, lighting, sensory) + engineers (structural, M&E)

**Source material:** §3.4 (12 co-occurrence entries) + Part E (9 conflict resolutions) + phantom §8.4.x stubs + individual item conflict notes scattered through Part 7

**Proposed structure:**

| Section | Content | Source |
|---|---|---|
| §8.1 Purpose and Audience | Why cross-population resolution requires cross-disciplinary input; four disciplines addressed | NEW |
| §8.2 Resolution Methodology | Conflict identification → priority hierarchy → zoned resolution → DAR fallback → Tier 2 co-design override | Consolidates Part E §E.2 + §3.4 preamble |
| §8.3 Priority Hierarchy | When populations conflict, which need governs — and why | Part E §E.2, expanded with decision trees |
| §8.4 Documented Conflict Resolutions | All known conflicts with resolution guidance, grouped by environmental domain (acoustic, thermal, visual, spatial, sensory) | Part E §E.4 (9 entries) + §3.4 (12 entries) + item notes; target: 20–25 entries |
| §8.5 Unresolvable Conflicts and Zoning Strategy | Conflicts that cannot be resolved at population level; require spatial zoning or Tier 2 resolution | NEW — drawn from audit §4.6 (NEU+PAIN Uhthoff's thermal; NDV+MH ground-floor sensory retreat) |
| §8.6 Cross-Disciplinary Handoff Protocols | Per-discipline: what the architect needs from each specialist; what each specialist needs from the architect; shared vocabulary; trigger points | NEW — draws from Part 10 consultant briefs, expanded |
| §8.7 Collaboration Frameworks by Design Stage | SD → DD → CD → RFO: which disciplines are needed at each stage; what decisions lock in | NEW — draws from Part 4 stage-by-stage + Part 9 engineering briefs |
| §8.8 Worked Resolution Examples | 3–4 multi-disciplinary examples showing the full resolution chain: identify conflict → consult specialist → resolve or zone → document in DAR | NEW — populated from existing worked examples (§I.7) + new case study evidence |

### Part 10 — Reconceptualised

**Old model:** "Specialist Consultants: Who to Engage" — a list of consultant types with role/trigger/scope subsections.

**New model:** "Interdisciplinary Design Team" — collaboration-first framing.

| Section | Content |
|---|---|
| §10.1 The Case for Interdisciplinary Design | Why accessibility design fails in siloed practice; evidence from case studies |
| §10.2 Core Team Composition | Architect + OT + access consultant as permanent team; criteria for when additional specialists are needed |
| §10.3 Specialist Disciplines | Per specialist: shared vocabulary, common misconceptions, handoff checklist, escalation triggers (builds on old Part 10 but restructured for collaboration) |
| §10.4 Communication Protocols | Shared documentation standards; conflict escalation; design review structure |
| §10.5 OT-Architect Interface | The primary collaboration relationship; detailed protocol for assessment → specification → verification loop |

### Part 12 — Intensified Economics

**Additions to existing content:**

| New section/subsection | Content | Source |
|---|---|---|
| §12.X Development Pro Forma Templates | Template spreadsheets showing accessibility cost as % of total development cost for 3 building types (residential, office, healthcare); standard line items; worked examples | NEW — requires economics-researcher + web research |
| §12.X ROI Models | Return on investment calculations: avoided retrofit, reduced liability, tenant retention, insurance reduction, market premium | NEW — draws from existing §8.2 core ratio + new research |
| §12.X Value Propositions by Stakeholder | Developer, owner-occupier, tenant, insurer, government — each gets a tailored argument with quantified benefits | NEW — consolidates existing §8.3 value frameworks into actionable templates |
| §12.X Insurance and Liability | Specific data on slip/trip/fall liability costs; accessible design as risk mitigation; insurance premium evidence | NEW — requires targeted research |
| §12.X Grant Programmes and Incentives | Jurisdiction-by-jurisdiction funding sources for accessibility works (24 jurisdictions) | Expanded from existing — economics-researcher output |

### Part 13 — Expanded Case Studies

**Strategy:** Case studies serve dual purpose: (a) illustrative examples for practitioners; (b) formal evidence base for Part 7 specifications.

| Action | Detail | Count |
|---|---|---|
| Keep all existing 14 | Verified, cross-referenced, high quality | 14 |
| Mine existing for evidence upgrades | Systematically extract outcome data → cite in Part 7 items → upgrade ○ to ● where justified | ~10–15 item upgrades |
| Source new: PAIN/OFS | Zero current case studies for these populations | Target: 2–3 |
| Source new: NDV/MH | Only ASPECTSS school retrofit currently | Target: 1–2 |
| Source new: Residential (mixed-needs) | BC HAFI is only residential case study | Target: 2–3 |
| Source new: Cross-disciplinary collaboration | Projects documenting multi-specialist process | Target: 1–2 |
| Source new: Cross-population conflict resolution | Built environments where competing population needs were explicitly resolved — documented trade-offs and outcomes | Target: 2–3 |
| Source new: Co-occurring/compound disability | Multi-population environments designed for compound functional demand — synergistic provisions serving ≥2 populations simultaneously | Target: 2–3 |
| Source new: Evidence-gap deep dives | Single-population case studies targeting populations where Phase 2B research yields THIN or NO-DATA evidence — population(s) selected after Session 8–9 results | Target: 2–4 |
| **Total target** | | **25–35 case studies** |
**Case study evidence mining protocol** (new — Session 6):
1. For each of the 14 existing case studies: extract all quantified outcome data
2. Map each outcome to the Part 7 item(s) it supports
3. Assess evidence tier of each outcome (most are Tier 2–3)
4. For items currently marked ○ that gain case study evidence: upgrade to ● with citation
5. Log in BPC under relevant slug

---

## Slug Coverage Plan — Comprehensive

### Current State (from audit §2.1)

| Metric | Current | Target | Gap |
|---|---|---|---|
| Unique slugs | 62 | 62 | — |
| With `jurisdiction_coverage` block | 8 | 62 | 54 to backfill |
| With `best_practice_synthesis` | 0 | 62 | 62 to write |
| With `native_aliases` (14 lang) | 17 | 62 | 45 to backfill |
| With `citation_mining` | 20 | 62 | 42 to add |
| Pre-v4 slugs needing triage | 51 | 0 | 51 to assess |
| Duplicate slug entries | 4 | 0 | 4 to merge |
| PROVISIONAL BPC entries | 13 | ≤5 | ≥8 to upgrade |

### Triage Strategy (Session 6)

For each of the 51 pre-v4 slugs:

| Triage outcome | Criteria | Action | Est. count |
|---|---|---|---|
| **CONSUME** | Co-1 sources found incidentally; jurisdiction coverage ≥18/24; evidence adequate for specification | Add `jurisdiction_coverage` summary + `native_aliases` + `best_practice_synthesis` (backfill only; no new search) | ~20–25 |
| **SUPPLEMENT** | Partial coverage; missing Co-1 for key jurisdictions; evidence adequate but could be stronger | Targeted Co-1/Tier 2 pass for missing jurisdictions only; then backfill metadata | ~15–20 |
| **RE-RUN** | Evidence clearly inadequate; Co-1/Tier 2 not retrieved; thin or no-data for critical jurisdictions | Full multilingual-research run per v4 protocol | ~5–8 |
| **CLOSE-ELIMINATED** | Content eliminated by Phase 1 Decision Register | Close in search-log; mark CLOSED-ELIMINATED | ~3–5 |

**Token savings:** CONSUME slugs require ~50 tokens each (metadata backfill). SUPPLEMENT slugs require ~500 tokens (targeted pass). RE-RUN slugs require ~2,000 tokens. Without triage, all 51 would be RE-RUN at ~102,000 tokens. With triage, estimated ~25,000 tokens. **~75% reduction.**

### Backfill Protocol

For CONSUME and SUPPLEMENT slugs:

1. GET search-log entry
2. Add `jurisdiction_coverage` block — infer from existing search data which jurisdictions were covered
3. Add `native_aliases` — from Keyword Compendium if available, or infer from search terms used
4. Write `best_practice_synthesis` — from existing BPC content; the synthesis exists in prose but wasn't tagged per schema
5. Add `citation_mining` block — record 0 with explanation if not performed
6. PUT updated entry

### Priority Tiers for Research

| Priority | Slugs | Rationale |
|---|---|---|
| **P0 — Critical** | `pain-built-environment`, `ofs-built-environment`, `intellectual-disability-built-environment-design`, `cross-population-conflict-resolution` (NEW) | Weakest evidence × highest content value; Part 8 requires new slug |
| **P1 — High** | `mental-health-built-environment`, `neurological-built-environment` (supplement), `residential-home-modification`, `economics-accessible-construction` (NEW), `co-occurring-disability-design` (NEW) | Moderate evidence gaps; strategic importance; co-occurring slug feeds Part 8 §8.8 + Part 13 |
| **P2 — Upgrade** | All 13 PROVISIONAL BPC entries | Sufficient for specification but need jurisdiction gaps closed |
| **P3 — Backfill** | All remaining pre-v4 slugs triaged as CONSUME | Metadata only; no new search |

---

## Token Efficiency Analysis

### Gains Identified

| Source | Mechanism | Est. saving (tokens/session) |
|---|---|---|
| `github-io` skill | Eliminates ~100–200 tokens per commit × ~10 commits/session | 1,000–2,000 |
| Phase 0 compression (3→2) | Eliminates one full session overhead | ~4,000 (one-time) |
| Phase 1 compression (4→3) | Eliminates one full session overhead | ~4,000 (one-time) |
| Phase 5 compression (3→2) | Eliminates one full session overhead | ~4,000 (one-time) |
| Pre-v4 slug triage | Avoids unnecessary RE-RUN for ~40 slugs | ~75,000 (Phase 2) |
| Case study evidence mining | Upgrades 10–15 items from ○→● without new research | ~20,000 (avoids research sessions) |
| BPC↔Item mapping | Prevents duplicate research; enables targeted gap closure | ~10,000 (Phase 2–3) |
| Decision Register gate | Eliminates research/writing for CUT content | Variable; depends on scope reduction |
| Consume existing outputs | Never regenerate completed stages; reuse all v9.0 content | Standing rule; saves ~2,000/session |

### Costs of Expanded Scope

| Addition | Est. cost (sessions) |
|---|---|
| Part 8 research | 0.5 (within Phase 2) |
| Part 8 writing | 1.0 (dedicated session) |
| Economics intensification research | 0.5 (within Phase 2) |
| Economics intensification writing | 0.5 (within Phase 3) |
| Case study sourcing | 0.5 (within Phase 2) |
| Co-occurring slug research + expanded case study categories | 0.5 (within existing Session 10 + 11) |
| Part 10 reconceptualisation | 0 (absorbed into existing Part 10 writing) |
| **Net new session cost** | **~1 session** (absorbed into existing sessions where possible) |

### Net Assessment

Efficiency gains eliminate 3 sessions (Phase compression). Expanded scope adds ~1 session equivalent. Net: **24 sessions** vs. 25 in v10.0.

---

## Sequencing Logic

```
Phase 0  Ecosystem              Build tools before using them (2 sessions)
Phase 1  Editorial Decisions    What stays, merges, goes — produces Decision Register (3 sessions)
Phase 2A Triage & Mining        Pre-v4 slug triage + case study evidence mining + gap triage (1 session)
Phase 2B Research               Only research what survived Phase 1 + new Part 8/12/13 content (5 sessions)
Phase 3  Writing                Consolidate, edit, mark evidence, create new content (9 sessions)
Phase 4  Structure              Renumber, decompose, resolve cross-refs — once (2 sessions)
Phase 5  QA + Assembly          Audit, assemble, final verification (2 sessions)
```

**Why this order:**
- Phase 0 before everything: tools must exist before use.
- Phase 1 before Phase 2: no point researching evidence for content that gets cut. Decision Register is the single most important deliverable — everything downstream depends on it.
- Phase 2A before 2B: triage determines which slugs need research vs. backfill. Without triage, Phase 2B wastes tokens on adequate slugs.
- Phase 2B before Phase 3: evidence must exist before writing specifications.
- Phase 3 before Phase 4: consolidations and deletions change heading counts; renumber after content is final.
- Phase 4 before Phase 5: cross-references can only be verified after numbering is stable.
- Phase 5 last: QA on final, numbered, assembled document.

---

## Phase 0: Ecosystem (Sessions 1–2)

### Session 0-A: Core Infrastructure + Structural Skills (Session 1)

**Build (3):**
- `github-io` — standardised commit infrastructure; blocks everything downstream
- `file-splitter` — decompose master doc to per-Part files (Phase 4)
- `evidence-marker` — ●/○ classification and audit (Phase 3 + 5)

**Update (6):**
- `framing-checker` — add BAR-in-Vol-I check; add ●/○ marker awareness
- `evidence-auditor` — add ●/○ verification mode
- `item-specification-writer` — add ●/○ template; add illustration note; add K-category template
- `cross-reference-resolver` — add K-category codes; add per-Part file awareness; add BPC↔Item traceability pass
- `structure-auditor` — update heading patterns for v10.1 numbering
- `chunk-assembler` — add manifest mode for v10.1 multi-file architecture

**Gate:** All 3 builds complete. All 6 updates verified on test input. `github-io` tested with read/write cycle.

### Session 0-B: Research + Content Skills (Session 2)

**Build (3):**
- `bulk-renumber` — context-aware §-reference rewriting (Phase 4)
- `citation-miner` — backward + forward citation mining (Phase 2B)
- `sensory-coherence-checker` — sensory consistency across room matrices (Phase 5)

**Update (4):**
- `workplan-orchestrator` — update Part numbering map for v10.1 structure
- `session-consolidator` — add per-Part file awareness; add reconciliation for new state files
- `vol2-item-formatter` — add ●/○ system; update Part numbering
- `citation-verifier` — add HARVEST mode for bibliography assembly

**Reconcile skill inventory (from audit §1.1):**
- Add `vol2-item-formatter` and `toc-editor` to PI registry
- Classify `keyword-lookup`: retire or register
- Rename `workplan-orchestrator_SKILL-1.md` → `workplan-orchestrator_SKILL.md`

**Gate:** All 3 builds + 4 updates complete. Inventory reconciled. All skills tested.

---

## Phase 1: Editorial Decisions (Sessions 3–5)

Phase 1 does NOT edit the document. It produces a **Decision Register** (`workplan/v10-1-decision-register.md` on GitHub) — a comprehensive list of every keep/merge/cut/move/condense decision. This becomes the binding specification for Phases 2–5.

### P1-D1: Volume I + Volume II Front Matter (Session 3)

**Volume I (Parts 1–3):**

Scope filter: *Is this directly relevant to an architect or designer making decisions about a building?*

Part 1 — Foundations:
- §1.1–§1.7: KEEP (core doctrine). Apply CONDENSE targets per v10.0 plan.
- §1.8 Evidence Frameworks: MOVE to Appendix E.
- §1.9 Scope: CUT — absorb essential content into §1.1.
- "Working with OTs" unlabelled section: decision needed — merge into §1.3 or keep as §1.3.1.

Part 2 — Disability Categories:
- Alphabetical sort; add item application tables; remove OT framework lines.
- Per-category scope filter: architectural specification (KEEP) vs. clinical rationale (CONDENSE/CUT).
- IntD (DEC-05): full evidence review or condensed ○-marked proxy paragraph?
- ADD: DEAF → add DBL cross-reference and differentiation note.

Part 3 — Multiple Categories:
- §3.1–§3.3: KEEP. Remove BAR row/column from co-occurrence matrix.
- §3.4: MOVE to **new Part 8** (not §4.9 as in v10.0 — Part 8 is now a dedicated section).

**Volume II Front Matter:**
- "How to Use This Volume": KEEP.
- Population Codes Reference: CUT (redundant).
- Entry Path I (Design Stage): CONDENSE to table; absorb into §4.4.
- Entry Path II (Population): CUT (redundant with Part 2 item tables).
- Entry Path III (Building Type): CONDENSE to pointer table.
- NOT-RETROFITTABLE table: KEEP.
- DAR Register: CUT (redundant with Part 11).
- Item Template Reference Card: KEEP.

**Scope definition for new Part 8:**
- Confirm audience: architects + OTs + consultants + engineers.
- Confirm source material: §3.4 + Part E + §8.4.x phantoms + item conflict notes.
- Confirm structure per §8.1–§8.8 architecture above.
- Identify which new cross-disciplinary handoff content exists (from Part 10 consultant briefs) vs. must be written fresh.

**Output:** Decision Register entries for Vol I + Vol II front matter + Part 8 scope.
**Checkpoint:** Vol I + front matter decisions complete.

### P1-D2: Parts 4–7 (Session 4)

**Part 4 — Synthesis and Sequencing:**
- §4.1–§4.8: Apply per-subsection keep/merge/condense decisions per v10.0 plan.
- §4.9 (cross-population guidance): This is now a CROSS-REFERENCE to Part 8, not a substantive section. §4.9 becomes a brief pointer ("For cross-population conflict resolution, see Part 8") rather than absorbing §3.4 content.
- DEC-11: Worked examples — keep 5 or reduce to 3?

**Part 5 — Residential Matrices:**
- §5.0a: CUT (absorb into §5.0).
- Per-room: DEC-07 — sub-table structure (keep 6 or condense to 3?).
- Remove BAR columns from all matrices.
- Resolve phantom items per decision.

**Part 6 — Non-Residential Matrices:**
- §6.0: CUT.
- Same structural questions as Part 5.

**Part 7 — Item Specification Library:**
- Item consolidation decisions (DEC-01): approve/reject each merger candidate.
- Per-item scope filter: architectural specification or non-design content?
- I-04/I-05/I-06 (DEC-03): create as full Part 7 items, merge, or delete? **Recommendation from audit §5.3:** I-04 (zero-threshold drainage) and I-05 (ceiling hoist structure) are design decisions with ×20–40 cost multipliers — promote to Part 7.
- H-05 (DEC-04): create or redirect?
- BIO/TC (DEC-06): promote to Part 7 or keep in appendix?
- F-02 Fragrance-Free (DEC-12): keep or cut?
- A-17 Upholstered Seating (DEC-13): keep or cut?

**Output:** Decision Register entries for Parts 4–7.
**Checkpoint:** Author reviews and approves item consolidation list. **This is the most critical gate.**

### P1-D3: Parts 8–13 + Appendices + Supplementary (Session 5)

**Part 8 (NEW — cross-population resolution):**
- Review all source material identified in Session 3.
- Inventory all scattered conflict content: count entries, classify by domain (acoustic, thermal, visual, spatial, sensory).
- Identify gaps: which known co-occurrence pairs lack documented resolution guidance?
- Define cross-disciplinary handoff content scope: which consultant types need handoff protocols?
- DEC-14 (NEW): How many worked resolution examples for §8.8? Target: 3–4.

**Part 9 (Engineering):**
- KEEP all — directly relevant to architects.
- CONDENSE opportunities.
- Identify content that migrates to Part 8 §8.6/§8.7 (handoff protocols by design stage).

**Part 10 (reconceived as Interdisciplinary Design Team):**
- Identify content from old Part 10 that stays (consultant role descriptions).
- Define new content needed: collaboration protocols, communication standards, OT-architect interface.
- DEC-15 (NEW): How detailed should §10.5 OT-Architect Interface be? (This is core to the guidebook's value proposition.)

**Part 11 (DAR):** KEEP. Concision pass only.

**Part 12 (Economics — intensified):**
- DEC-08: Cost table restructure?
- DEC-16 (NEW): Pro forma template scope — which building types? Recommend: residential (most common), office, healthcare.
- DEC-17 (NEW): ROI model detail level — practitioner-facing summary or developer-facing full model?
- DEC-18 (NEW): Jurisdiction scope for grant programmes — all 24 or top 8?

**Part 13 (Case Studies — expanded):**
- DEC-09: Keep all 14 existing.
- DEC-19 (NEW): Target populations for new case studies (PAIN/OFS, NDV/MH, residential, conflict resolution, co-occurring/compound, evidence-gap deep dives). IntD case studies removed per directive.
- DEC-20 (NEW): Case study template — add "Evidence Contribution" field mapping outcomes to Part 7 items?

**Appendices:** Per v10.0 plan. Appendix E from §1.8.

**Supplementary Volume:** Review for consistency with main guidebook decisions. No major changes expected.

**Output:** Complete Decision Register on GitHub. All DEC-01 through DEC-20 resolved.

**Phase 1 gate:** Decision Register approved by author. No Phase 2 work begins until approved.

---

## Phase 2A: Triage & Evidence Mining (Session 6)

This session eliminates unnecessary downstream work. Three operations, each reducing the research burden.

### Operation 1: Pre-v4 Slug Triage (~60% of session)

Process all 51 pre-v4 slug entries:

1. GET search-log.
2. For each pre-v4 slug:
   - Check: is its content eliminated by Decision Register? → CLOSE-ELIMINATED.
   - Check: does existing search data cover ≥18 jurisdictions? Were Co-1 sources found incidentally? → CONSUME (backfill metadata only).
   - Check: partial coverage, missing key jurisdictions? → SUPPLEMENT (targeted pass).
   - Check: clearly inadequate? → RE-RUN.
3. Merge 4 duplicate slug entries.
4. Fix pipe-suffix naming inconsistencies.
5. PUT updated search-log.

**Output:** Triage register — every slug classified as CONSUME / SUPPLEMENT / RE-RUN / CLOSE-ELIMINATED.

### Operation 2: Case Study Evidence Mining (~25% of session)

Process all 14 existing case studies:

1. For each case study: extract all quantified outcome data (e.g., De Hogeweyk 50% lower antipsychotic rates; DSDC 30–40% agitation reduction from acoustic intervention).
2. Map each outcome to Part 7 item(s) it supports.
3. Assess evidence tier of outcome data.
4. Log evidence mapping: `Part 13 case study → Part 7 item → evidence tier → upgrade candidate (○→●)?`
5. Produce case study evidence map on GitHub.

**Output:** `workplan/case-study-evidence-map.md` — expected: 10–15 item upgrade candidates.

### Operation 3: Gap Register Triage (~15% of session)

With Decision Register approved:

1. GET gap_register.md.
2. For each OPEN gap: if section/item eliminated → CLOSED-ELIMINATED. If merged → reassign. If surviving → OPEN.
3. PUT updated gap_register.md.
4. Add P1 gap: GAP-CO2-01 (Co-2 tier unpopulated — per audit §4.1).

**Output:** Updated gap_register.md. Expected: 100 OPEN → ~50–65 OPEN.

**Checkpoint:** Triage complete. Surviving OPEN gaps + triage results define Phase 2B research scope.

---

## Phase 2B: Research (Sessions 7–11)

### Session 7: Foundations Research — Co-2 + CRPD + Slug Backfill Batch 1

**Co-2 Sources (§1.5 population):**
- Retrieve CPGs from: CAOT, AOTA, RCOT (incl. Housing Adaptations Without Delay 2019), COTEC, WFOT
- For each: classify evidence tier, extract built-environment specifications, log in BPC

**CRPD Text:**
- Retrieve Articles 3, 4.3, 9 full text for §1.7 expansion

**Slug Backfill — CONSUME batch:**
- Process ~20–25 CONSUME slugs: add `jurisdiction_coverage`, `native_aliases`, `best_practice_synthesis`
- Target: 8–10 per hour; complete full CONSUME batch in one session

**Output:** `co2-sources.md`, `crpd-articles.md`, backfilled search-log entries.

### Session 8: Population Research — PAIN + OFS + IntD

**Slug: `pain-built-environment`** (P0 priority)
- Full v4 protocol run. Focus: Co-1 sources (pain patient advocacy), Tier 5 beyond-code.
- Target: upgrade from WEAK to ADEQUATE.

**Slug: `ofs-built-environment`** (P0 priority)
- Full v4 protocol run. Focus: ME/CFS advocacy publications, POTS research.
- Target: upgrade from WEAK to at minimum ADEQUATE-PROVISIONAL.

**Slug: `intellectual-disability-built-environment-design`** (scope determined by DEC-05)
- If full review: v4 protocol run targeting Lebenshilfe (DE), Vilans (NL), Plena inclusión (ES), AAIDD (US).
- If condensed proxy: targeted check only (~30 min).

**Output:** Updated BPC entries for all three slugs.

### Session 9: Population Research — NDV/MH + NEU Supplement + Residential

**Slug: `mental-health-built-environment`** (P1 priority)
- Targeted pass: Co-1 sources from mental health advocacy organisations; therapeutic design evidence.

**Slug: `neurological-built-environment`** (P1 supplement)
- Supplement pass: close specific gaps identified in triage (NEU/PCS provisions relying solely on PAS 6463).

**Slug: `residential-home-modification`** (P1 priority)
- Residential primacy framing creates evidence needs. Target: OT home modification outcome studies; aging-in-place evidence by jurisdiction.

**SUPPLEMENT batch:**
- Process 5–8 SUPPLEMENT slugs with targeted Co-1/Tier 2 passes for missing jurisdictions.

**Output:** Updated BPC entries; SUPPLEMENT slugs upgraded.

### Session 10: Cross-Population + Economics Research

**NEW slug: `cross-population-conflict-resolution`** (P0 priority)
- Evidence for Part 8 content. Search targets:
  - Sensory environment conflict literature (VIS vs DEM lighting; DEAF vs NDV acoustic)
  - Thermal conflict literature (NEU Uhthoff's vs PAIN warmth needs)
  - Multi-disciplinary design team effectiveness evidence
  - Post-occupancy evaluation data on resolved vs unresolved conflicts
- This slug uses all 14 languages and 24 jurisdictions but with a narrow topic focus.

**NEW slug: `co-occurring-disability-design`** (P1 priority)
- Evidence for compound/synergistic design. Distinct from conflict resolution: this slug asks "what design techniques serve ≥2 populations simultaneously?" rather than "how do you resolve when populations conflict?"
- Search targets:
  - Aged care facility design for compound populations (MOB+DEM+VIS+DEAF)
  - SDA/supported living for co-occurring conditions
  - OT home modification for clients with ≥2 disability categories
  - POE data from multi-population settings
  - Rehabilitation facility design for compound functional demand
- Companion nodes: Summer Foundation, Habinteg, IDeA Center, UNSW HMC, KDA, Vilans
- 14 languages × 24 jurisdictions, narrow topic focus.

**Economics intensification research:**
- Cost study data by building type (residential, office, healthcare)
- Pro forma/development cost data: US (RSMeans), UK (BCIS), DE (TERRAGON), AU (QS databases)
- Insurance/liability reduction evidence
- Grant programme inventory: 8 priority jurisdictions (US, UK, CA, AU, DE, FR, SE, JP)
- ROI calculation methodologies for accessible design

**Output:** New BPC entry for cross-population slug. Economics research compilation.

### Session 11: Case Study Sourcing + Remaining Slug Coverage

**New case studies — targeted search:**
- PAIN/OFS: built environment adaptations with outcome data (target: 2–3)
- NDV/MH: therapeutic or trauma-informed design with outcomes (target: 1–2)
- Residential mixed-needs: home modification programmes with longitudinal data (target: 2–3)
- Cross-disciplinary collaboration: projects documenting multi-specialist process (target: 1–2)
- Cross-population conflict resolution: built projects where competing population needs were explicitly resolved — documented trade-offs, zoning decisions, outcome data (target: 2–3)
- Co-occurring/compound disability: multi-population environments designed for compound functional demand — aged care, SDA, rehabilitation — with synergistic design provisions serving ≥2 populations (target: 2–3)
- Evidence-gap deep dives: single-population case studies for populations where Sessions 8–9 research yielded THIN or NO-DATA — specific populations selected at Session 10 checkpoint (target: 2–4)

**Remaining SUPPLEMENT slugs:**
- Complete any SUPPLEMENT batch slugs not finished in Session 9.

**RE-RUN slugs:**
- Process any slugs triaged as RE-RUN (estimated 5–8). If >5 need full runs, extend into Session 12 or defer lowest-priority to PROVISIONAL.

**Output:** Case study compendium. All slug coverage complete or explicitly PROVISIONAL.

**Phase 2 gate:** All surviving OPEN gaps either researched or explicitly accepted as ○-marked. All slug entries meet minimum v4 schema. Case study evidence map complete. Economics research compiled. Decision Register updated with any scope changes.

---

## Phase 3: Writing (Sessions 12–20)

Content revision within the *current* structure (old numbering). Phase 4 renumbers. Phase 3 applies: consolidation, deletion, concision, evidence markers, new content creation.

### P3-W01: Front Matter + Part 1 (Session 12)

- Apply all Phase 1 decisions for front matter and Part 1.
- Add ●/○ notation guide; add illustration note.
- Absorb §1.9 into §1.1; move §1.8 to Appendix E placeholder.
- Merge "Working with OTs" per decision.
- Insert CRPD article quotes in §1.7.
- Populate Co-2 in §1.5 with sources from Session 7.
- Clarify Tier defaults (public = T0/T1, residential = T2).
- Strengthen residential primacy argument in §1.4.6 (per audit §5.6).
- Remove all BAR from Vol I.
- Concision pass.

**Checkpoint:** Part 1 content-final.

### P3-W02: Part 2 — Disability Categories (Session 13)

- Alphabetical sort; add item application tables; remove OT framework lines.
- Per-category: apply keep/condense decisions from Decision Register.
- Integrate Phase 2B research findings for PAIN, OFS, IntD, NDV/MH, NEU.
- Apply ●/○ markers.
- Remove BAR references; add DBL differentiation from VIS+DEAF.
- Concision pass — target: each category ≤1 page equivalent.

**Checkpoint:** Part 2 content-final.

### P3-W03: Parts 3 + 4 (Session 14)

- Part 3: remove §3.4 (**moved to Part 8**, not §4.9); remove BAR from matrix; condense.
- Part 4: apply Phase 1 consolidation decisions. §4.9 becomes a brief cross-reference pointer to Part 8 (not substantive content).
- Number worked examples; number §4.8 subsections.
- Absorb Entry Path I table into §4.4 if decided.
- Concision pass.

**Checkpoint:** Parts 3 + 4 content-final.

### P3-W04: Part 5 — Residential Matrices (Session 15)

- Apply Phase 1 room matrix decisions.
- Remove §5.0a; remove BAR columns.
- Resolve phantom items per Decision Register.
- Apply ●/○ markers. Apply case study evidence upgrades from Session 6 evidence map.
- Condense per Decision Register.

**Checkpoint:** Part 5 content-final.

### P3-W05: Part 6 — Non-Residential Matrices (Session 16)

- Same operations as Part 5.
- Remove §6.0.

**Checkpoint:** Part 6 content-final.

### P3-W06: Part 7 — Item Library Categories A–E (Session 17)

- Apply all item consolidation mergers from Decision Register.
- Delete items marked CUT.
- Apply ●/○ markers to every specification sentence.
- Apply case study evidence upgrades (○→● where evidence map justifies).
- Add "[Illustration: to be provided]" to every item.
- Add EXPERT CONSENSUS / THIN-BASE disclosures.
- Add `bpc_slugs` field to each item (BPC↔Item traceability).
- Reformat Appendix B/C items to Part 7 if promoted.
- Remove duplicate E-06/E-07/E-08/E-09 block.
- Resolve phantom item references.
- Concision pass.

**Checkpoint:** Categories A–E content-final.

### P3-W07: Part 7 — Categories F–K + BIO + TC (Session 18)

- Same operations as Session 17 for remaining categories.
- K-category: apply EXPERT CONSENSUS template; ensure honest evidence disclosure maintained.
- Promote I-04, I-05 to full Part 7 items if decided (DEC-03).

**Checkpoint:** All Part 7 categories content-final.

### P3-W08: Part 8 — Cross-Population Resolution & Collaboration (Session 19)

**This is the primary new-content session.**

§8.1 Purpose and Audience:
- Write framing: why cross-population resolution is a distinct discipline requiring multi-specialist input.
- Address each audience segment: architect (spatial resolution), OT (functional assessment), consultant (domain expertise), engineer (technical feasibility).

§8.2 Resolution Methodology:
- Consolidate from Part E §E.2 + §3.4 preamble.
- Expand into step-by-step methodology: identify conflict → classify severity → apply priority hierarchy → select resolution strategy (zoning / specification range / DAR / Tier 2 override).

§8.3 Priority Hierarchy:
- Expand from Part E §E.2 into decision tree format.
- Add tie-breaking rules for equal-priority conflicts.

§8.4 Documented Conflict Resolutions:
- Consolidate all 21+ entries (Part E 9 + §3.4 12 + item notes).
- Group by environmental domain: acoustic, thermal, visual, spatial, sensory.
- Each entry: conflict statement → populations affected → resolution → evidence tier → which specialist resolves → DAR note.
- Target: 20–25 documented resolutions.

§8.5 Unresolvable Conflicts and Zoning Strategy:
- NEU+PAIN Uhthoff's thermal (audit §4.6): irresolvable at population level; zoned thermal management.
- NDV+MH ground-floor sensory retreat requirement.
- Write 3–5 unresolvable conflict entries with zoning resolution guidance.

§8.6 Cross-Disciplinary Handoff Protocols:
- Draw from old Part 10 consultant brief templates.
- Per discipline: acoustic engineer, lighting designer, OT, M&E engineer, landscape architect.
- Each: what they need from the architect, what the architect needs from them, trigger points, shared vocabulary.

§8.7 Collaboration Frameworks by Design Stage:
- SD → DD → CD → RFO: which disciplines needed, what locks in at each stage.
- Draw from Part 4 stage-by-stage + Part 9 engineering briefs.

§8.8 Worked Resolution Examples:
- 3–4 examples showing full multi-disciplinary resolution chain.
- Draw from existing worked examples + new case study evidence.

**Checkpoint:** Part 8 content-final.

### P3-W09: Parts 9–13 + Appendices + Bibliography (Session 20)

**Part 9 (Engineering):** Concision pass. Migrate handoff content to Part 8 §8.6/§8.7 (cross-reference only; don't duplicate).

**Part 10 (Interdisciplinary Design Team):**
- Restructure from consultant list to collaboration framework.
- §10.1–§10.2: Write new framing + core team composition.
- §10.3: Restructure existing consultant role descriptions for collaboration lens.
- §10.4: Write communication protocols.
- §10.5: Write OT-Architect Interface protocol (core collaboration relationship).

**Part 11 (DAR):** Concision pass.

**Part 12 (Economics — intensified):**
- Existing content: concision pass; reorder §12.3 subsections.
- NEW: Development pro forma templates (from Session 10 research).
- NEW: ROI models section.
- NEW: Value propositions by stakeholder.
- NEW: Insurance and liability section.
- NEW: Grant programmes and incentives (8+ jurisdictions).
- Integrate case study economic outcome data.

**Part 13 (Case Studies — expanded):**
- Keep all 14 existing.
- Integrate 11–19 new case studies from Session 11 sourcing (PAIN/OFS, NDV/MH, residential, cross-disciplinary, conflict resolution, co-occurring/compound, evidence-gap deep dives).
- Add "Evidence Contribution" field to each case study: which Part 7 items this study's outcomes support.
- Add cross-references back to Part 7 item specifications.

**Appendices:**
- Appendix E: write from §1.8 content.
- Bibliography: run `citation-verifier` HARVEST mode across all Parts; assemble consolidated bibliography. Part 12 bibliography serves as template.
- Glossary: absorb framework definitions; verify all terms.
- Fix all remaining terminology per standing rules.

**Checkpoint:** All Parts content-final. Document ready for structural pass.

---

## Phase 4: Structure (Sessions 21–22)

### P4-S1: Renumbering (Session 21)

1. Generate final heading inventory from content-final document.
2. Apply Part renumbering map:
   - Parts 1–7: unchanged
   - Part 8: NEW (already numbered correctly in Phase 3)
   - Parts 9–13: verify alignment with new numbering
3. Apply section renumbering: each Part N uses §N.x.
4. Run `bulk-renumber` in dry-run → review → apply.
5. Generate Change Order CO-0002.

**Checkpoint:** All sections correctly numbered. Zero old numbering remains.

### P4-S2: File Decomposition + Cross-Reference Resolution (Session 22)

1. `file-splitter` → per-Part .md files per architecture.
2. `cross-reference-resolver` full scan including BPC↔Item traceability.
3. Fix any orphan references.
4. Update `references/toc.md`.
5. Commit all files to `parts/v10/` on GitHub.
6. Create assembly manifest.

**Phase 4 gate:** All files on GitHub. toc.md current. Zero orphan references. BPC↔Item links verified.

---

## Phase 5: QA + Assembly (Sessions 23–24)

### P5-Q1: Full Automated Audit Suite (Session 23)

- `framing-checker` — social model, BAR-in-Vol-I, CRPD alignment.
- `evidence-marker` AUDIT — 100% ●/○ coverage check.
- `structure-auditor` — heading hierarchy across all files.
- `guidebook-auditor` — format, terminology, table consistency.
- `sensory-coherence-checker` — room matrices.
- `prose-style-checker` — register, voice, concision, ≤25-word specification sentences.
- `citation-verifier` — every cited source in bibliography.
- `cross-reference-resolver` — BPC↔Item bidirectional check.
- Manual spot-check: 10 cross-references per volume.

**Output:** QA findings register. Fix all P1/P2 issues inline.

### P5-Q2: Assembly + Final (Session 24)

1. `chunk-assembler` with manifest → master document.
2. Line count and heading count verification.
3. Final commit of assembled v10.1.
4. Close all resolved gap register items.
5. Update project-standards.md.
6. Session consolidator → final YAML.
7. Produce handoff summary.

**Phase 5 gate:** Assembled v10.1 on GitHub. Gap register reconciled. All QA findings resolved or logged.

---

## Decision Points (Complete)

| ID | Question | Phase | Blocking |
|---|---|---|---|
| DEC-01 | Per-item consolidation: approve/reject each merger | P1-D2 | Yes |
| DEC-02 | Entry Path I table: absorb into §4.4 or cut? | P1-D1 | No |
| DEC-03 | I-04/I-05/I-06: create, merge, or delete? | P1-D2 | Yes |
| DEC-04 | H-05 (Nurse Call): create or redirect? | P1-D2 | No |
| DEC-05 | IntD: full review or condensed proxy? | P1-D1 | Yes — determines Phase 2B |
| DEC-06 | BIO/TC: promote to Part 7 or keep in appendix? | P1-D2 | No |
| DEC-07 | Room matrix sub-tables: keep 6 or condense to 3? | P1-D2 | No |
| DEC-08 | §12.4 Cost tables: restructure? | P1-D3 | No |
| DEC-09 | Case studies: keep all 14 + expand | P1-D3 | No |
| DEC-10 | Appendix E: separate appendix or glossary expansion? | P1-D3 | No |
| DEC-11 | Worked examples: keep 5 or reduce to 3? | P1-D1 | No |
| DEC-12 | F-02 (Fragrance-Free): keep or cut? | P1-D2 | No |
| DEC-13 | A-17 (Upholstered Seating): keep or cut? | P1-D2 | No |
| DEC-14 | Part 8 §8.8: how many worked resolution examples? | P1-D3 | No |
| DEC-15 | Part 10 §10.5 OT-Architect Interface: detail level? | P1-D3 | No |
| DEC-16 | Pro forma templates: which building types? | P1-D3 | No |
| DEC-17 | ROI model: practitioner-facing or developer-facing? | P1-D3 | No |
| DEC-18 | Grant programmes: all 24 jurisdictions or top 8? | P1-D3 | No |
| DEC-19 | Target populations for new case studies | P1-D3 | No |
| DEC-20 | Case study template: add "Evidence Contribution" field? | P1-D3 | No |

---

## Session Plan (Final)

| Session | Phase | Work |
|---|---|---|
| 1 | P0 | Build: github-io, file-splitter, evidence-marker. Update: 6 skills |
| 2 | P0 | Build: bulk-renumber, citation-miner, sensory-coherence-checker. Update: 4 skills. Reconcile inventory |
| 3 | P1 | Editorial: Vol I (Parts 1–3) + Vol II front matter + Part 8 scope |
| 4 | P1 | Editorial: Parts 4–7 — **item consolidation gate** |
| 5 | P1 | Editorial: Parts 8–13 + Appendices — **Decision Register complete** |
| 6 | P2A | Pre-v4 slug triage (51 slugs) + case study evidence mining (14 studies) + gap register triage |
| 7 | P2B | Co-2 sources + CRPD text + CONSUME slug backfill (~20–25 slugs) |
| 8 | P2B | Lit review: PAIN + OFS + IntD |
| 9 | P2B | Lit review: NDV/MH + NEU supplement + residential + SUPPLEMENT slug batch |
| 10 | P2B | Cross-population conflict evidence (Part 8) + economics deep-dive |
| 11 | P2B | Case study sourcing + remaining SUPPLEMENT/RE-RUN slugs |
| 12 | P3 | Write: Front matter + Part 1 |
| 13 | P3 | Write: Part 2 (disability categories) |
| 14 | P3 | Write: Parts 3 + 4 |
| 15 | P3 | Write: Part 5 (residential matrices) |
| 16 | P3 | Write: Part 6 (non-residential matrices) |
| 17 | P3 | Write: Part 7 Categories A–E |
| 18 | P3 | Write: Part 7 Categories F–K + BIO + TC |
| 19 | P3 | Write: Part 8 (NEW — cross-population resolution + collaboration) |
| 20 | P3 | Write: Parts 9–13 + Appendices + Bibliography + Glossary |
| 21 | P4 | Renumber (single pass, content-final document) |
| 22 | P4 | File decomposition + cross-reference resolution |
| 23 | P5 | Full QA audit suite |
| 24 | P5 | Assembly, final commit, gap register close, handoff |

**Total: 24 sessions.** Phase 1 editorial decisions remain the critical path.

---

## Audit Recommendations — Implementation Tracker

| Audit rec. | ID | Implementation | Session |
|---|---|---|---|
| Reconcile skill inventory | §1.1a–c | Session 0-B reconciliation step | 2 |
| Build 6 missing skills | §1.2a | Phase 0 | 1–2 |
| Update 10 skills | §1.3a | Phase 0 | 1–2 |
| Add P1 gap for Co-2 | §4.1a | Session 6 gap triage | 6 |
| Promote I-04/I-05 | §5.3 | DEC-03 in Session 4 | 4 |
| Protect cross-population content | §5.2 | Part 8 dedicated part | 5, 19 |
| Resolve ●/○ ambiguity | §4.2a | Session 3 notation guide decision | 3 |
| Pre-v4 slug triage | §5.1 | Dedicated Phase 2A | 6 |
| Fix duplicate slugs | §2.2a | Session 6 triage | 6 |
| Enforce slug naming | §2.2b | Session 6 triage | 6 |
| Mine case studies for evidence | §5.4 | Session 6 evidence mining | 6 |
| BPC↔Item mapping | §5.5 | `cross-reference-resolver` update + Phase 3 item writing | 1, 17–18 |
| Backfill pre-v4 slugs | §2.1 | Session 7 CONSUME batch | 7 |
| Strengthen residential primacy | §5.6 | Session 12 Part 1 writing | 12 |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase 1 scope decisions don't narrow enough → Phases 2–3 bloat | Medium | High | DEC-05 (IntD), DEC-01 (item mergers), and DEC-07 (sub-tables) are the biggest scope levers; resolve these early in Session 4 |
| Part 8 new content exceeds single session | Medium | Medium | §8.6–§8.7 draw heavily from existing Part 9/10 content; §8.4 is consolidation not creation; only §8.1, §8.5, §8.8 are genuinely new |
| Economics research finds thin pro forma data | High | Medium | Fallback: worked examples with placeholder values marked [DATA NEEDED]; flag as P2 gap for post-publication update |
| Case study sourcing for PAIN/OFS yields <3 studies | High | Medium | PAIN/OFS are genuinely under-documented in built environment literature; accept THIN-BASE with honest disclosure |
| Pre-v4 triage takes longer than allocated | Low | Low | Triage is classification, not research; 51 slugs × ~3 min each = ~2.5 hours; fits within session |
| Context limit reached mid-Part 8 writing | Medium | Medium | Part 8 §8.4 (consolidated resolutions) is the longest section; if context limit approaches, split §8.4 acoustic+thermal into one session and visual+spatial+sensory into next |
| Co-occurring/compound case study sourcing yields thin results | Medium | Medium | Co-occurring design is often documented as universal design without explicit multi-population framing; search strategy includes POE literature and aged care facility evaluations where compound populations are implicit |
| Conflict resolution case studies lack documented trade-off data | High | Medium | Most built projects don't publish conflict resolution process; target SDA, aged care, and healthcare facility evaluations where regulatory requirements forced explicit documentation |
| Evidence-gap deep dives depend on Sessions 8–9 completing first | Low | Low | If Sessions 8–9 incomplete at Session 11, defer deep dives to PROVISIONAL and note in gap register |

---

*End of Redesigned Workplan v10.1*
