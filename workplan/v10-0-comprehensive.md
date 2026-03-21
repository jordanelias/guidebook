# Workplan: Guidebook v10.0 Comprehensive Revision

**Created:** 2026-03-20 21:00
**Supersedes:** Workplan_v9-0_Comprehensive_2026-03-19.md
**Source documents:**
- Critique_Report_Guidebook_v9-0_2026-03-20.md (this session)
- Hierarchy_correction.md (author directives)
- Guidebook_v90_Headings_Sequential.md (current structure)
- gap_register.md (93 OPEN items, 15 P1)
- references/project-standards.md (canonical rules)
- references/best-practices-compendium.md (research state)

**Target:** Guidebook for Accessible Design v10.0
**Output architecture:** One `.md` per Part; one `.md` per Item Category; assembled master document
**GitHub path:** `parts/v10/{filename}.md`

---

## 0. Directive Register

All author directives from this session, assigned tracking codes.

| Code | Source | Directive | Phase |
|---|---|---|---|
| DIR-01 | Hierarchy correction | Renumber all Parts per corrected hierarchy (see §0.1) | P2 |
| DIR-02 | Hierarchy correction | §1.8 Evidence Frameworks → Appendix E or Glossary expansion | P3 |
| DIR-03 | Hierarchy correction | §1.9 Scope → eliminate; absorb essential content into §1.1 | P3 |
| DIR-04 | Hierarchy correction | "Working with OTs" → assign §1.3a or merge into §1.3 | P3 |
| DIR-05 | Hierarchy correction | Part 2: sort categories alphabetically by code | P3 |
| DIR-06 | Hierarchy correction | Part 2: add Item Application Table per category | P3 |
| DIR-07 | Hierarchy correction | Part 2: remove OT framework references from body; remove inline citations from core environmental needs | P3 |
| DIR-08 | Hierarchy correction | Part 2: add Item Specification Library Code Reference at head of Part 2 | P3 |
| DIR-09 | Hierarchy correction | §3.4 co-occurrence guidance → consolidate into Part 4 | P3 |
| DIR-10 | Hierarchy correction | Sort §3.4 / consolidated co-occurrence guidance alphabetically | P3 |
| DIR-11 | Hierarchy correction | Vol II: eliminate Population Codes Reference, Entry Paths I/II/III, DAR Register — Consolidated | P3 |
| DIR-12 | Hierarchy correction | Remove §5.0a Universal Residential Provisions; §6.0 Universal Non-Residential Provisions | P3 |
| DIR-13 | Hierarchy correction | Consolidate Part 4 subsections — make more concise | P3 |
| DIR-14 | Hierarchy correction | Consolidate Part 7 items where possible | P3 |
| DIR-15 | Hierarchy correction | Consolidate Part 9 (new; was Part 10) subsections | P3 |
| DIR-16 | Hierarchy correction | §11.4 (new numbering) cost tables — consider mapping to Item Spec Library categories or room-by-room; reduce subsections | P3 |
| DIR-17 | Hierarchy correction | Economics References section → move to Master Bibliography | P3 |
| DIR-18 | Hierarchy correction | Appendix labels: §A.x, §B.x, §C.x, §D.x | P2 |
| DIR-19 | Hierarchy correction | Worked examples → §4.7.1–§4.7.5 numbering | P2 |
| DIR-20 | Hierarchy correction | §4.8 subsections → §4.8.1–§4.8.5 numbering | P2 |
| DIR-21 | Hierarchy correction | Front matter: resolve duplicate H1; establish as ToC | P2 |
| DIR-22 | Author (session) | Part 8 conflict resolutions → consolidate into Part 4: Synthesis and Sequencing | P3 |
| DIR-23 | Author (session) | No BAR mentions in Volume I | P3 |
| DIR-24 | Author (session) | Quote CRPD Article 3, Article 4.3, Article 9 in Volume I (§1.7) | P1 |
| DIR-25 | Author (session) | Evidence bullet (●) vs inferred bullet (○) — note distinction at beginning of each volume | P3 |
| DIR-26 | Author (session) | Tier clarification: public unknown = Tier 0, public known disabled populations = Tier 1, residential = Tier 2 | P3 |
| DIR-27 | Author (session) | Specify provisions with clinical reasoning/expert consensus where evidence absent; disclose with ○ marker | P3 |
| DIR-28 | Author (session) | Make document more concise; consolidate sections wherever possible to increase usability | P3 |
| DIR-29 | Author (session) | Note that all items will be accompanied by diagram/drawing/illustration | P3 |
| DIR-30 | Author (session) | Each Part → separate .md file; each Category → separate .md file | P2 |
| DIR-31 | Critique report | Resolve all phantom item references (68+) | P2 |
| DIR-32 | Critique report | Remove duplicate E-06/E-07/E-08/E-09 blocks | P2 |
| DIR-33 | Critique report | Populate Master Bibliography from bibliography-v9.md | P3 |
| DIR-34 | Critique report | Fix "Developed Design" → "Design Development"; "Commissioning" → "Ready for Occupancy" | P2 |
| DIR-35 | Critique report | Fix "Part 11I §8.x" → valid section references | P2 |
| DIR-36 | Critique report | Populate Co-2 tier with CAOT, AOTA, RCOT, COTEC CPG sources | P1 |
| DIR-37 | Critique report | Reformat Appendix B/C items to match Part 7 template | P3 |
| DIR-38 | Critique report | Add EXPERT CONSENSUS / THIN-BASE disclosure to OFS and PAIN specs | P3 |
| DIR-39 | Critique report | Reorder §12.3 (new: §11.3) subsections — §11.3.4 should follow §11.3.3 | P2 |
| DIR-40 | Critique report | Resolve "MIS" population code (not defined) → correct to NDV/SENS or remove | P2 |
| DIR-41 | Critique report | Stale VI-xx references → resolve or delete | P2 |

### 0.1 Part Renumbering Map (Corrected Hierarchy)

| Old | New | Title | Volume |
|---|---|---|---|
| Part 1 | **Part 1** | Foundations of Accessible Design | I |
| Part 2 | **Part 2** | Disability Categories | I |
| Part 3 | **Part 3** | Designing for Multiple Disability Categories | I |
| Part 4 | **Part 4** | Synthesis, Sequencing, and Cross-Population Guidance | II |
| Part 5 | **Part 5** | Residential Application Matrices | II |
| Part 6 | **Part 6** | Non-Residential Application Matrices | II |
| Part 7 | **Part 7** | Item Specification Library | II |
| **Part 8 (old)** | **(absorbed into Part 4)** | Cross-Population Conflict Resolutions → Part 4 | — |
| Part 9 (old) | **Part 8** | Engineering and Coordination | II |
| Part 10 (old) | **Part 9** | Working with Specialist Consultants | II |
| Part 11 (old) | **Part 10** | Design for Adaptable Readiness (DAR) | III |
| Part 12 (old) | **Part 11** | The Economics of Accessible Construction | III |
| Part 13 (old) | **Part 12** | Case Studies | III |

**Section numbering rule:** Part N uses §N.x numbering. No exceptions.

---

## Phase 1: Research (Sessions 1–5)

Research must precede editing. Evidence gaps identified in critique must be filled before content is revised.

### P1-R1: CRPD Article Text Retrieval
**Skill:** web search (one-time)
**Directive:** DIR-24
**Task:** Retrieve exact CRPD Article 3 (General Principles), Article 4.3 (participation clause), and Article 9 (Accessibility) text. Prepare quoted blocks for insertion into §1.7.
**Output:** `parts/v10/research/crpd-articles.md`
**Checkpoint:** CRPD text confirmed and formatted

### P1-R2: Co-2 Tier Sources
**Skill:** multilingual-research (targeted)
**Directive:** DIR-36
**Task:** Retrieve and verify clinical practice guidelines from: CAOT (Canada), AOTA (USA), RCOT (UK), COTEC/ENOTHE (EU), WFOT (International), Ergotherapie Austria, DVE (Germany), ANFE (France). For each: title, year, scope, DOI/URL.
**Output:** `parts/v10/research/co2-sources.md`
**Checkpoint:** ≥5 CPGs confirmed with DOI

### P1-R3: PAIN Built-Environment Literature Review
**Skill:** research-log-manager CHECK → multilingual-research → research-log-manager LOG
**Directive:** Critique §1.2 (PAIN = thinnest evidence base)
**Slug:** `pain-built-environment`
**Scope:** 14 languages × 24 jurisdictions per Protocol v4
**Priority targets:** Fibromyalgia environmental triggers (temperature, vibration, surface hardness); chronic pain and flooring; CRPS environmental sensitivity; pain-specific home modifications
**Output:** `parts/v10/research/lit-PAIN-BE.md`
**Checkpoint:** BPC entry written; evidence tier range confirmed

### P1-R4: OFS Built-Environment Literature Review
**Skill:** research-log-manager CHECK → multilingual-research → research-log-manager LOG
**Directive:** Critique §1.2 (OFS = inferred from symptom profiles)
**Slug:** `ofs-built-environment`
**Scope:** 14 languages × 24 jurisdictions per Protocol v4
**Priority targets:** ME/CFS environmental triggers; POTS orthostatic environment design; MCAS chemical sensitivity and ventilation; post-COVID fatigue and building design
**Output:** `parts/v10/research/lit-OFS-BE.md`
**Checkpoint:** BPC entry written; evidence tier range confirmed

### P1-R5: IntD Built-Environment Literature Review
**Skill:** research-log-manager CHECK → multilingual-research → research-log-manager LOG
**Directive:** Critique §1.2 (IntD = PLACEHOLDER); gap_register GAP-S4-SYST-02
**Slug:** `intd-built-environment`
**Scope:** 14 languages × 24 jurisdictions per Protocol v4
**Priority targets:** Bundesvereinigung Lebenshilfe (DE); Vilans (NL); Plena inclusión (ES); NICE NG93 (UK); NDIS SDA intellectual disability provisions (AU); supported living design evidence
**Output:** `parts/v10/research/lit-IntD-BE.md`
**Checkpoint:** BPC entry written; PLACEHOLDER status resolved to either PARTIAL or COMPLETE

### P1-R6: NEU Evidence Strengthening
**Skill:** multilingual-research (targeted supplement to existing coverage)
**Directive:** Critique §1.2 (NEU = WEAK — relies heavily on PAS 6463)
**Slug:** `neu-built-environment` (supplement existing)
**Priority targets:** TBI environmental evidence; MS-specific built environment studies; PCS environmental sensitivity; epilepsy-specific lighting/flicker evidence
**Output:** `parts/v10/research/lit-NEU-BE-supplement.md`
**Checkpoint:** ≥3 new Tier 1–3 sources confirmed

### P1-R7: NDV/MH Evidence Strengthening
**Skill:** multilingual-research (targeted)
**Slug:** `mh-built-environment`
**Priority targets:** PTSD and built environment; trauma-informed design evidence; Dignified Design (2024) full extraction; psychiatric facility design OT literature
**Output:** `parts/v10/research/lit-MH-BE.md`
**Checkpoint:** BPC entry written

### P1-R8: Residential Focus — Home Modification Evidence
**Skill:** multilingual-research
**Directive:** Author emphasis on residential primacy ("every person lives somewhere")
**Slug:** `residential-home-modification`
**Priority targets:** OT home assessment evidence across all populations; NDIS SDA evidence; UK DFG evidence; Canadian HAFI evidence; Scandinavian boligtilpasning evidence
**Output:** `parts/v10/research/lit-residential.md`
**Checkpoint:** BPC entry written; residential-specific evidence mapped to each population code

### P1-R9: Item Consolidation Analysis
**Skill:** item-consolidation-analyzer
**Directive:** DIR-14 (consolidate items where possible)
**Task:** Review all 90 Part 7 items. Identify candidates for merger. Produce consolidation recommendations.
**Output:** `parts/v10/research/item-consolidation-recommendations.md`
**Checkpoint:** Consolidation list with author decision required per item pair

**Phase 1 gate:** All P1-R outputs committed to GitHub before Phase 2 begins.

---

## Phase 2: Structure (Sessions 6–8)

Structural changes applied to the document skeleton before content editing.

### P2-S1: File Decomposition
**Skill:** haiku-chunker (Mode B) + bash
**Directive:** DIR-30
**Task:** Split v9.0 master document into per-Part and per-Category files:

```
parts/v10/
  part01-foundations.md
  part02-disability-categories.md
  part03-multiple-categories.md
  part04-synthesis-sequencing.md           # absorbs §3.4 + old Part 8
  part05-residential-matrices.md
  part06-nonresidential-matrices.md
  part07-item-library-index.md             # index only
  categories/
    cat-A-acoustics.md
    cat-B-lighting.md
    cat-C-colour-surface.md
    cat-D-spatial-wayfinding.md
    cat-E-entry-circulation.md
    cat-F-sensory-zoning.md
    cat-G-furniture-fittings.md
    cat-H-controls-technology.md
    cat-I-upper-limb.md
    cat-K-deafblind.md
  part08-engineering.md                    # was Part 9
  part09-specialist-consultants.md         # was Part 10
  part10-dar.md                            # was Part 11
  part11-economics.md                      # was Part 12
  part12-case-studies.md                   # was Part 13
  appendix-A-standards.md
  appendix-B-biophilic.md
  appendix-C-thermal.md
  appendix-D-evacuation.md
  appendix-E-evidence-frameworks.md        # from old §1.8
  front-matter.md
  glossary.md
  bibliography.md
```

**Checkpoint:** All files created on GitHub; line counts confirmed

### P2-S2: Section Renumbering
**Skill:** find-and-replace + toc-editor
**Directives:** DIR-01, DIR-18, DIR-19, DIR-20
**Task:** Apply renumbering map (§0.1) across all Part files. Generate Change Order CO-0002.
**Sequence per file:**
1. Rename section headers
2. Update all internal §-references
3. Update all cross-references pointing into or out of the file
**Checkpoint:** toc-editor confirms no orphan references

### P2-S3: Structural Deletions and Moves
**Skill:** find-and-replace
**Directives:** DIR-02, DIR-03, DIR-09, DIR-11, DIR-12, DIR-17, DIR-22
**Tasks:**
- Move §1.8 Evidence Frameworks → appendix-E-evidence-frameworks.md
- Delete §1.9 Scope (absorb "applies to" list into §1.1 as one sentence)
- Move §3.4 co-occurrence guidance → part04 new §4.9 "Cross-Population Conflict Guidance"
- Absorb all §8.4.x conflict resolution references → §4.9.x subsections
- Delete: Population Codes Reference, Entry Paths I/II/III, DAR Register from Vol II front matter
- Delete: §5.0a Universal Residential Provisions, §6.0 Universal Non-Residential Provisions
- Move Economics References section → bibliography.md
**Checkpoint:** Deleted content verified absent; moved content verified present in new location

### P2-S4: Phantom Reference Resolution
**Skill:** cross-reference-resolver + find-and-replace
**Directives:** DIR-31, DIR-32, DIR-35, DIR-40, DIR-41
**Tasks:**
- Remove duplicate E-06/E-07/E-08/E-09 block
- For each phantom item (I-04, I-05, I-06, J-01–J-05, H-05, VI-xx): decision table:
  - If content exists elsewhere → redirect reference
  - If content should exist → create stub with [PLACEHOLDER]
  - If content is stale → delete reference
- Fix all "Part 11I §8.x" → corrected §10.x (new DAR numbering) or §4.9.x (conflict guidance)
- Fix "MIS" → "NDV/SENS" or delete
- Fix all VI-xx → correct current item code or delete
**Checkpoint:** cross-reference-resolver confirms zero orphan references

### P2-S5: Terminology Corrections
**Skill:** find-and-replace
**Directives:** DIR-34, DIR-39
**Tasks:**
- "Developed Design" → "Design Development" (all occurrences)
- "Commissioning" → "Ready for Occupancy" (all design stage references)
- "COMM" stage abbreviation → "RFO"
- Reorder §11.3 (new numbering) subsections to 11.3.1, 11.3.2, 11.3.3, 11.3.4
**Checkpoint:** grep confirms zero remaining instances of old terms

**Phase 2 gate:** All structural changes committed. `references/toc.md` updated. Change Order CO-0002 filed.

---

## Phase 3: Content Editing (Sessions 9–20)

Content revision within the new structure. Each Part is its own work unit.

### P3-C01: Front Matter
**File:** `front-matter.md`
**Directives:** DIR-21, DIR-25, DIR-29
**Tasks:**
1. Consolidate to single H1 + ToC
2. Add evidence notation guide: ● = evidence-based specification; ○ = inferred from clinical reasoning / expert consensus (evidence gap disclosed)
3. Add note: "All items in the Item Specification Library are designed to be accompanied by a technical diagram, drawing, or illustration. Where illustrations are not yet provided, the specification text is self-sufficient."
4. Update item counts, category list, Part numbering to v10.0
**Output:** `parts/v10/front-matter.md`
**Checkpoint:** Front matter complete

### P3-C02: Part 1 — Foundations
**File:** `part01-foundations.md`
**Directives:** DIR-02, DIR-03, DIR-04, DIR-23, DIR-24, DIR-26, DIR-36
**Tasks:**
1. Merge "Working with OTs" into §1.3 (give it subsection §1.3.1 or integrate prose)
2. Eliminate §1.9 Scope (one-sentence summary absorbed into §1.1)
3. §1.5 Evidence Hierarchy: populate Co-2 with CAOT, AOTA, RCOT, COTEC CPG sources from P1-R2
4. §1.7 CRPD Alignment: insert quoted text of Article 3 (principles), Article 4.3 (participation), Article 9 (accessibility) from P1-R1
5. §1.4.3 Three-Tier Hierarchy: clarify — public building unknown population = Tier 0; public building known disabled populations = Tier 1; residential home = Tier 2
6. Remove all BAR mentions from Volume I text (DIR-23)
7. §1.4.6 Application to Residential Design: strengthen with residential primacy framing — "every person lives somewhere; every residence should be able to tailor itself to the people who live there"
8. Cross-reference §1.8 → "See Appendix E: Evidence Frameworks" (one sentence)
9. Apply ●/○ evidence markers to any prescriptive claim in Part 1
10. Concision pass: target 15% word reduction
**Output:** `parts/v10/part01-foundations.md`
**Checkpoint:** Part 1 complete; no BAR; CRPD quoted; Co-2 populated

### P3-C03: Part 2 — Disability Categories
**File:** `part02-disability-categories.md`
**Directives:** DIR-05, DIR-06, DIR-07, DIR-08, DIR-23, DIR-25, DIR-27
**Tasks:**
1. Add Item Specification Library Code Reference table at head of Part 2 (all category codes A–K with descriptions)
2. Sort population categories alphabetically by code: DBL, DEAF, DEM, IntD, MOB, NDV, NDV/MH, NEU, OFS, PAIN, UPL, VIS
3. Renumber: §2.1 DBL, §2.2 DEAF, §2.3 DEM, §2.4 IntD, §2.5 MOB, §2.6 NDV, §2.7 NDV/MH, §2.8 NEU, §2.9 OFS, §2.10 PAIN, §2.11 UPL, §2.12 VIS
4. Per category: add Item Application Table (which Part 7 items apply, ●/○ coding)
5. Per category: remove "OT Framework:" line from body
6. Per category: remove inline citations from "Core environmental needs" (citations live in Part 7 items and Bibliography)
7. Remove all BAR mentions or redirects from Part 2
8. IntD: integrate P1-R5 findings; upgrade from PLACEHOLDER if evidence permits; apply ○ markers to inferred provisions
9. PAIN: integrate P1-R3 findings; apply ○ markers where evidence is inferred
10. OFS: integrate P1-R4 findings; apply ○ markers; add EXPERT CONSENSUS disclosures per DIR-38
11. Apply ●/○ markers to all core environmental needs lists
12. Concision pass: target 20% word reduction (removing duplicated content that lives in Part 7)
**Output:** `parts/v10/part02-disability-categories.md`
**Checkpoint:** Part 2 complete; alphabetically sorted; item tables added; no OT framework refs; no inline citations in core needs

### P3-C04: Part 3 — Multiple Categories
**File:** `part03-multiple-categories.md`
**Directives:** DIR-09, DIR-10, DIR-23
**Tasks:**
1. Remove §3.4 (moved to Part 4 §4.9)
2. Remove BAR from co-occurrence matrix
3. Keep §3.1–§3.3 intact; this Part becomes shorter and more focused on theory
4. Co-occurrence matrix: remove BAR row and column
5. Concision pass
**Output:** `parts/v10/part03-multiple-categories.md`
**Checkpoint:** Part 3 complete; §3.4 absent; no BAR

### P3-C05: Part 4 — Synthesis, Sequencing, and Cross-Population Guidance
**File:** `part04-synthesis-sequencing.md`
**Directives:** DIR-09, DIR-10, DIR-13, DIR-19, DIR-20, DIR-22
**Tasks:**
1. Absorb former §3.4 co-occurrence guidance as new §4.9
2. Absorb all scattered Part 8 §8.4.x conflict resolutions into §4.9 subsections
3. Sort §4.9 co-occurrence entries alphabetically (DEM+OFS, MH+OFS, MH+PAIN, MOB+DEM, MOB+NEU, MOB+OFS, MOB+PAIN, NDV+MH, NEU+MH, NEU+OFS, NEU+PAIN, VIS+DBL)
4. Number worked examples §4.7.1–§4.7.5
5. Number §4.8 subsections §4.8.1–§4.8.5
6. Consolidate §4.1–§4.3 if overlap permits (target: merge §4.1 into §4.2 if "why synthesis matters" is restated in "the layered environment")
7. Remove BAR from worked examples
8. Concision pass: target 15% reduction
**Output:** `parts/v10/part04-synthesis-sequencing.md`
**Checkpoint:** Part 4 complete; all conflict content consolidated; alphabetically sorted

### P3-C06: Part 5 — Residential Matrices
**File:** `part05-residential-matrices.md`
**Directives:** DIR-12, DIR-23, DIR-25, DIR-31
**Tasks:**
1. Remove §5.0a Universal Residential Provisions (content absorbed into §5.0 How to Read)
2. Renumber sections §5.0–§5.10
3. R-BATH not R-BA-05 → R-BA-01 (per hierarchy correction: §5.5 R-BATH)
4. Remove BAR column from all matrices; redirect to Supp Vol footnote
5. Resolve phantom items in matrix tables (I-04 → G-04?; I-05 → create or remove; J-xx → remove)
6. Apply ●/○ markers to IntD and OFS matrix entries
7. Strengthen residential framing per author emphasis
8. Integrate P1-R8 residential evidence where it improves matrix specifications
**Output:** `parts/v10/part05-residential-matrices.md`
**Checkpoint:** Part 5 complete; no BAR; no phantom items; §5.x numbering

### P3-C07: Part 6 — Non-Residential Matrices
**File:** `part06-nonresidential-matrices.md`
**Directives:** DIR-12, DIR-23, DIR-25, DIR-31
**Tasks:**
1. Remove §6.0 Universal Non-Residential Provisions
2. Renumber §6.1–§6.7
3. Remove BAR column from all matrices
4. Resolve phantom items
5. Apply ●/○ markers
**Output:** `parts/v10/part06-nonresidential-matrices.md`
**Checkpoint:** Part 6 complete; §6.x numbering

### P3-C08: Part 7 — Item Specification Library (per-Category files)
**Files:** `categories/cat-{X}-{name}.md` (10 files)
**Directives:** DIR-14, DIR-25, DIR-27, DIR-29, DIR-37, DIR-38
**Tasks per category:**
1. Apply item consolidation decisions from P1-R9
2. Apply ●/○ evidence markers to every specification
3. Add EXPERT CONSENSUS / THIN-BASE disclosures where missing (OFS, PAIN items)
4. Add note per item: "[Illustration: to be provided]"
5. Verify all cross-references point to valid items in new numbering
6. Appendix B items (BIO-01–BIO-05): reformat to match Part 7 template (structured fields, not paragraph)
7. Appendix C items (TC-01–TC-05): reformat to match Part 7 template
8. Fix "Part 11I §8.x" references in BIO/TC items → correct new section numbers
9. Concision pass per item: one claim per sentence; ≤25 words per spec sentence

**Category-specific tasks:**
- **Cat-A Acoustics:** Review A-10b naming (should this be A-10.1 or A-11 with renumber?)
- **Cat-E Entry/Circulation:** Remove duplicate E-06/E-07/E-08/E-09 block
- **Cat-I Upper Limb:** Decide on I-04/I-05/I-06 — create or redirect
- **Cat-K DeafBlind:** Integrate any new Co-1 evidence from P1 research

**Output:** 10 category files + `part07-item-library-index.md` (master index with item code, title, category, applicable groups, evidence tier)
**Checkpoint:** All categories complete; zero phantom items; all items have ●/○ markers

### P3-C09: Part 8 — Engineering (was Part 9)
**File:** `part08-engineering.md`
**Directives:** DIR-01
**Tasks:**
1. Renumber §9.x → §8.x throughout
2. Update all cross-references
3. Concision pass
**Output:** `parts/v10/part08-engineering.md`
**Checkpoint:** Part 8 complete; §8.x numbering

### P3-C10: Part 9 — Specialist Consultants (was Part 10)
**File:** `part09-specialist-consultants.md`
**Directives:** DIR-01, DIR-15
**Tasks:**
1. Renumber §9.x (old Part 10) → §9.x (new Part 9) — note collision: old Part 9 Engineering also used §9.x. New Engineering is §8.x, so §9.x is now free for Specialist Consultants.
2. Consolidate specialist consultant subsections: for each consultant type (DEM, DeafSpace, Sensory, Accessibility Auditor), merge Role + Appointment Triggers + Scope into single subsection (not three sub-subsections each)
3. Update cross-references
4. Concision pass
**Output:** `parts/v10/part09-specialist-consultants.md`
**Checkpoint:** Part 9 complete; consolidated; §9.x numbering

### P3-C11: Part 10 — DAR (was Part 11)
**File:** `part10-dar.md`
**Directives:** DIR-01
**Tasks:**
1. Renumber §11.x → §10.x
2. Update cross-references
3. Concision pass
**Output:** `parts/v10/part10-dar.md`
**Checkpoint:** Part 10 complete; §10.x numbering

### P3-C12: Part 11 — Economics (was Part 12)
**File:** `part11-economics.md`
**Directives:** DIR-01, DIR-16, DIR-17, DIR-39
**Tasks:**
1. Renumber §12.x → §11.x
2. Reorder §11.3 subsections: 11.3.1 Functional → 11.3.2 Lifecycle → 11.3.3 Market → 11.3.4 Social/Systemic
3. §11.4 Cost Intelligence Tables: evaluate mapping to Item Spec Library categories (A–K) instead of current topic grouping. Author decision required.
4. Move References section → bibliography.md
5. Update all cross-references
6. Concision pass
**Output:** `parts/v10/part11-economics.md`
**Checkpoint:** Part 11 complete; §11.x numbering; references moved

### P3-C13: Part 12 — Case Studies (was Part 13)
**File:** `part12-case-studies.md`
**Directives:** DIR-01
**Tasks:**
1. Renumber §12.xx → §12.xx (numbering stays §12 but now belongs to this Part, no collision)
2. Renumber: §12.01–§12.14
3. Update cross-references
**Output:** `parts/v10/part12-case-studies.md`
**Checkpoint:** Part 12 complete; §12.x numbering; no collision with Economics

### P3-C14: Appendices and Back Matter
**Files:** `appendix-{A|B|C|D|E}.md`, `glossary.md`, `bibliography.md`
**Directives:** DIR-02, DIR-18, DIR-33, DIR-37
**Tasks:**
1. Appendix A: relabel subsections §A.1–§A.5
2. Appendix B: relabel §B.1–§B.5; reformat items to Part 7 template
3. Appendix C: relabel §C.1–§C.5; reformat items to Part 7 template
4. Appendix D: relabel if needed
5. Appendix E (new): Evidence Frameworks (content from old §1.8)
6. Glossary: absorb any framework definitions from old §1.8 not included in Appendix E
7. Bibliography: populate from bibliography-v9.md project file; absorb Economics references; structure by language group
**Output:** 7 files
**Checkpoint:** All appendices complete; bibliography populated

**Phase 3 gate:** All Part files committed. All directives resolved. All cross-references verified.

---

## Phase 4: Quality Assurance (Sessions 21–23)

### P4-Q1: Cross-Reference Audit
**Skill:** cross-reference-resolver
**Task:** Scan all Part files for every §-reference and item code reference. Verify each resolves to a valid target.
**Output:** `parts/v10/qa/xref-audit.md`
**Checkpoint:** Zero orphan references

### P4-Q2: Framing Check
**Skill:** framing-checker
**Task:** Full social model framing check across all Part files. Verify no BAR in Volume I. Verify CRPD alignment.
**Output:** `parts/v10/qa/framing-audit.md`
**Checkpoint:** Zero regressions

### P4-Q3: Evidence Marker Audit
**Skill:** evidence-auditor (extended to check ●/○ system)
**Task:** Verify every prescriptive specification carries either ● (evidence-based) or ○ (inferred/expert consensus). Flag any unmarked claims.
**Output:** `parts/v10/qa/evidence-marker-audit.md`
**Checkpoint:** 100% specification marker coverage

### P4-Q4: Prose Style Check
**Skill:** prose-style-checker
**Task:** Verify ≤25-word specification sentences; soft imperative subjunctive voice; concision targets met.
**Output:** `parts/v10/qa/prose-audit.md`
**Checkpoint:** Style pass complete

### P4-Q5: Structure Audit
**Skill:** structure-auditor + guidebook-auditor
**Task:** Verify heading hierarchy, numbering sequence, table formatting, and markdown consistency across all files.
**Output:** `parts/v10/qa/structure-audit.md`
**Checkpoint:** Zero structural issues

### P4-Q6: Document Assembly
**Skill:** chunk-assembler
**Task:** Concatenate all Part files into `Guidebook_for_Accessible_Design_v10-0_{date}.md`
**Output:** `versions/current/Guidebook_for_Accessible_Design_v10-0.md`
**Checkpoint:** Master document assembled; line count and heading count confirmed

---

## Phase 5: Ecosystem Update

### P5-E1: Skill Audit and Updates

| Skill | Status | Required update |
|---|---|---|
| workplan-orchestrator | Active | Update Part numbering map; update workflow sequences |
| haiku-chunker | Active | No change |
| find-and-replace | Active | No change |
| toc-editor | Active | Update toc.md schema to v10 Part numbering |
| structure-auditor | Active | Update expected numbering rules |
| markdown-formatter | Active | No change |
| cross-reference-resolver | Active | Update valid item code registry for v10 |
| guidebook-auditor | Active | Update expected section patterns |
| content-gap-analyzer | Active | Update population code order (alphabetical) |
| framing-checker | Active | Add BAR-in-Vol-I check; add ●/○ marker check |
| evidence-auditor | Active | Add ●/○ marker verification mode |
| item-consolidation-analyzer | Active | No change |
| item-specification-writer | Active | Add ●/○ marker requirement; add "[Illustration: to be provided]" |
| prose-style-checker | Active | No change |
| citation-verifier | Active (provisional) | No change until bibliography complete |
| multilingual-research | Active | No change |
| research-log-manager | Active (inline) | No change |
| session-consolidator | Active | Update Part numbering in YAML schema |
| chunk-assembler | Active | Update file list for v10 architecture |
| vol2-item-formatter | Active | Update to match ●/○ system |
| table-formatter | Active | No change |
| supplemental-integrator | Active | No change |
| critique-report-writer | Active | No change |
| practice-note-generator | Active | No change |
| version-diff | Active | No change |
| jurisdiction-tracker | Active | No change |
| literature-review-planner | Active | No change |
| economics-researcher | Active | No change |
| fix-linebreaks | Active | No change |
| keyword-lookup | Active | No change |

**Skills requiring update:** 9 of 29
**Skills to build:** citation-miner (P2 — deferred from v9.0)
**Skills to retire:** None

### P5-E2: GitHub State File Updates

| File | Update |
|---|---|
| `references/toc.md` | Full regeneration from v10 hierarchy |
| `gap_register.md` | Close all resolved gaps; append new gaps from workplan |
| `references/project-standards.md` | Append: Part renumbering rule; ●/○ marker rule; alphabetical sort rule; residential Tier 2 default rule; no-BAR-in-Vol-I rule; CRPD quotation rule |
| `references/search-log.md` | New entries from P1-R3 through P1-R8 |
| `references/best-practices-compendium.md` | New BPC entries from Phase 1 research |
| `references/slug-registry.md` | New slugs: pain-built-environment, ofs-built-environment, intd-built-environment, mh-built-environment, residential-home-modification |

### P5-E3: Project Instructions Update

The following PI sections require amendment after v10.0 completion:

| Section | Change |
|---|---|
| Population Codes table | Reflect alphabetical ordering |
| Three-Tier Design Hierarchy | Add residential Tier 2 default |
| Standing Rules §15 | Already correct (DD, RFO) |
| Skill Registry | Update Part numbers in trigger descriptions |
| Workflow Reference | Update skill sequences for new Part numbering |
| Deferred Production Items | Clear resolved items; add new deferrals |

---

## Session Plan

| Session | Phase | Work units | Est. tokens |
|---|---|---|---|
| **1** | P1 | R1 (CRPD), R2 (Co-2), R9 (item consolidation) | Medium |
| **2** | P1 | R3 (PAIN lit review) | High |
| **3** | P1 | R4 (OFS lit review) | High |
| **4** | P1 | R5 (IntD lit review) | High |
| **5** | P1 | R6 (NEU supplement), R7 (NDV/MH), R8 (residential) | High |
| **6** | P2 | S1 (file decomposition) | Medium |
| **7** | P2 | S2 (renumbering), S3 (structural moves) | High |
| **8** | P2 | S4 (phantom refs), S5 (terminology) | Medium |
| **9** | P3 | C01 (front matter), C02 (Part 1) | Medium |
| **10** | P3 | C03 (Part 2 — largest content edit) | High |
| **11** | P3 | C04 (Part 3), C05 (Part 4) | High |
| **12** | P3 | C06 (Part 5 — residential matrices) | High |
| **13** | P3 | C07 (Part 6), C08 start (Cat A, B) | High |
| **14** | P3 | C08 continued (Cat C, D, E) | High |
| **15** | P3 | C08 continued (Cat F, G, H, I, K) | High |
| **16** | P3 | C09 (Part 8 Engineering), C10 (Part 9 Consultants) | Medium |
| **17** | P3 | C11 (Part 10 DAR), C12 (Part 11 Economics) | Medium |
| **18** | P3 | C13 (Part 12 Case Studies), C14 (Appendices) | Medium |
| **19** | P3 | C14 continued (Glossary, Bibliography) | Medium |
| **20** | P4 | Q1 (xref audit), Q2 (framing) | Medium |
| **21** | P4 | Q3 (evidence markers), Q4 (prose) | Medium |
| **22** | P4 | Q5 (structure), Q6 (assembly) | Medium |
| **23** | P5 | E1 (skill updates), E2 (GitHub state), E3 (PI update) | Medium |

**Total estimated sessions:** 23
**Critical path:** Phase 1 research must complete before Phase 3 content editing begins. Phase 2 structure can run in parallel with Phase 1 after Session 5.

---

## Checkpoint Protocol

Each session ends with:
1. `CHECKPOINT [YYYY-MM-DD HH:MM] — phase: {P} — unit: {code} — status: {DONE|PARTIAL|BLOCKED}`
2. All completed files committed to GitHub
3. Session-consolidator YAML written to `sessions/`
4. Handoff summary for next session

Each Phase gate requires:
- All work units in the phase marked DONE or explicitly deferred with author approval
- All outputs committed to GitHub
- gap_register updated
- toc.md updated (Phase 2+)

---

## Decision Points Requiring Author Input

| ID | Question | Phase | Blocking |
|---|---|---|---|
| DEC-01 | Item consolidation: approve/reject each merger recommendation from P1-R9 | P3-C08 | Yes |
| DEC-02 | §11.4 Cost Intelligence Tables: map to Item categories (A–K) or keep current topic grouping? | P3-C12 | No (can proceed with current and restructure later) |
| DEC-03 | I-04/I-05/I-06: create as new items, merge into existing items, or delete references? | P2-S4 | Yes |
| DEC-04 | H-05 (Nurse Call): create as new item or redirect to K-04? | P2-S4 | No |
| DEC-05 | IntD evidence review (P1-R5): if evidence remains THIN, proceed with ○-marked proxy provisions or remove IntD from matrices? | P3-C03 | Yes |
| DEC-06 | BIO/TC items: remain in Appendices B/C or promote into Part 7 main library? | P3-C08 | No |
| DEC-07 | A-10b (Hydrotherapy RT60): renumber to A-18 or keep as A-10b? | P3-C08 | No |

---

*End of Workplan*
