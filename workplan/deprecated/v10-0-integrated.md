# Workplan: Guidebook v10.0 — Integrated Revision

**Created:** 2026-03-20 23:00
**Supersedes:** Workplan_v10-0_Comprehensive_2026-03-20.md + Ecosystem_Audit_Phase0_2026-03-20.md
**Principle:** Content determines structure. Structure is applied once, at the end.

---

## Sequencing Logic

```
Phase 0  Skills/Ecosystem          Build tools before using them
Phase 1  Editorial Decisions       What stays, merges, goes — produces definitive scope
Phase 2  Gap Triage + Research     Only research what survived Phase 1
Phase 3  Writing                   Consolidate, edit, mark evidence, revise
Phase 4  Structure                 Renumber, decompose to files, resolve cross-refs — once
Phase 5  QA + Assembly             Audit, assemble, final verification
```

**Why this order:**
- Phase 1 before Phase 2: no point researching evidence for content that gets cut.
- Phase 1 before Phase 3: no point writing concise prose that later gets merged or deleted.
- Phase 3 before Phase 4: consolidations and deletions change heading counts; renumber after content is final.
- Phase 4 before Phase 5: cross-references can only be verified after numbering is stable.

---

## Directive Register

*(Unchanged from previous workplan — 41 directives, codes DIR-01 through DIR-41. See previous workplan for full table. Key additions from this revision below.)*

| Code | Source | Directive |
|---|---|---|
| DIR-42 | Author (this session) | Narrow scope: guidebook for architects and designers. Vol II content must be actionable and evidentiary. Remove cursory content. |
| DIR-43 | Author (this session) | Consolidation and deletion happen before renumbering. Structure is applied once at the end. |
| DIR-44 | Author (this session) | Gap register items in eliminated content → CLOSED-ELIMINATED, not researched. |
| DIR-45 | Author (this session) | Content that is not directly relevant to architectural/design practice → cut or move to appendix. |

---

## Phase 0: Ecosystem (Sessions 1–3)

*(Content unchanged from Ecosystem Audit. Summary only.)*

### Session 0-A: Core Infrastructure Skills
- **Build:** `github-io` (standardised commits), `file-splitter`, `evidence-marker` (●/○ system)
- **Update:** `framing-checker` (+BAR-in-Vol-I check, +marker check), `evidence-auditor` (+marker mode), `item-specification-writer` (+●/○ template, +illustration note)

### Session 0-B: Structural and Assembly Skills
- **Build:** `bulk-renumber` (context-aware §-reference rewriting)
- **Update:** `cross-reference-resolver`, `structure-auditor`, `chunk-assembler` (+manifest), `workplan-orchestrator`, `session-consolidator`, `vol2-item-formatter`

### Session 0-C: Research and Content Skills
- **Build:** `citation-miner`, `sensory-coherence-checker`
- **Update:** `citation-verifier` (+HARVEST mode for bibliography assembly)

**Phase 0 gate:** All skills built/updated. Author adds new skills to `/mnt/project/`. Verified by running each skill on a test input.

---

## Phase 1: Editorial Decisions (Sessions 4–7)

Phase 1 does not edit the document. It produces a **Decision Register** — a comprehensive list of every keep/merge/cut/move decision, which becomes the binding specification for Phases 2–5.

The Decision Register is a single document on GitHub (`workplan/v10-decision-register.md`) with one entry per section/item/subsection, each carrying a status: KEEP, MERGE (into what), CUT (reason), MOVE (to where), or CONDENSE (target word count).

### P1-D1: Volume I Editorial Pass (Session 4)

Work through every section in Volume I with the hierarchy correction directives and the scope filter: *Is this directly relevant to an architect or designer making decisions about a building?*

**Part 1 — Foundations:**

| Section | Hierarchy correction directive | Decision needed |
|---|---|---|
| §1.1 Definitions + Key Terms | — | KEEP but CONDENSE — definitions are essential |
| §1.2 Code-as-Floor | — | KEEP — core doctrine |
| §1.3 Designing for the Individual | — | KEEP |
| "Working with OTs" (unlabelled) | DIR-04: needs §-label or merge | MERGE into §1.3 or KEEP as §1.3.1? |
| §1.4 Universal/Inclusive Design | — | KEEP but review subsections for condensability |
| §1.4.1–§1.4.6 (6 subsections) | — | Can any merge? §1.4.1+§1.4.5 both argue UD is insufficient — merge? |
| §1.5 Evidence Hierarchy | — | KEEP — structural |
| §1.6 DAR Principle | — | KEEP |
| §1.7 CRPD Alignment | DIR-24: add CRPD quotes | KEEP + expand with Article text |
| §1.8 Evidence Frameworks | DIR-02: move to Appendix E or Glossary | MOVE to Appendix E. One-sentence cross-ref replaces section. |
| §1.9 Scope | DIR-03: eliminate | CUT — absorb essential content ("applies to...") as one sentence in §1.1 |

**Part 2 — Disability Categories:**
Per hierarchy correction: sort alphabetically, add item application tables, remove OT framework lines, remove inline citations from core needs. Plus: apply scope filter — are the "Special Considerations" paragraphs actionable for an architect, or are they clinical background?

Decision needed per category: which content is architectural specification (KEEP) vs. clinical rationale (CONDENSE or CUT)?

**Part 3 — Multiple Categories:**
§3.1–§3.3 KEEP (theory is short). §3.4 → MOVE to Part 4 (already decided, DIR-09). Co-occurrence matrix: remove BAR row/column.

**Output:** Decision Register entries for all Vol I sections.
**Checkpoint:** Vol I decisions complete. Author reviews and approves before proceeding.

### P1-D2: Volume II Editorial Pass — Part 4 + Front Matter (Session 5)

**Vol II front matter (currently before Part 4):**
- "How to Use This Volume" — KEEP (short, necessary)
- Population Codes Reference — DIR-11: CUT (redundant with Part 2)
- Entry Path I: By Design Stage — DIR-11: CUT? Or is this actionable for architects? **Decision needed:** The design stage table (SD/DD/CD/RFO) is genuinely useful. Consider: CUT the separate section but absorb the table into §4.4 Stage-by-Stage Process.
- Entry Path II: By Population — DIR-11: CUT (redundant with Part 2 item tables)
- Entry Path III: By Building Type — DIR-11: CUT? Or CONDENSE to simple pointer table?
- NOT-RETROFITTABLE table — KEEP (actionable, concise)
- DAR Register — DIR-11: CUT (redundant with Part 10 DAR content)

**Part 4 — Synthesis and Sequencing:**
DIR-13: look to consolidate. Scope filter: is each subsection actionable for an architect, or is it pedagogical scaffolding?

| Section | Assessment |
|---|---|
| §4.1 Why Synthesis Matters | Pedagogical — could be 2 paragraphs, not a full section |
| §4.2 The Layered Environment | Useful framework — KEEP but CONDENSE |
| §4.3 Four Synthesis Principles | Actionable — KEEP |
| §4.4 Stage-by-Stage Process | Highly actionable — KEEP. Absorb Entry Path I table here? |
| §4.5 Synthesis by Building Strategy | Actionable — KEEP |
| §4.6 Decision Framework for Sequencing | Actionable — KEEP. Could merge with §4.5? |
| §4.7 Worked Examples (5) | Highly actionable — KEEP. Do we need 5 or would 3 suffice? |
| §4.8 From Approach to Application | The strongest section — KEEP |
| §4.9 (new) Cross-Population Conflict Guidance | Absorbs §3.4 + old Part 8 refs — KEEP |

**Output:** Decision Register entries for all Vol II front matter + Part 4.
**Checkpoint:** Decisions complete.

### P1-D3: Volume II Editorial Pass — Parts 5–7 (Session 6)

**Part 5 — Residential Matrices:**
- §5.0a Universal Residential Provisions — DIR-12: CUT (absorb into §5.0)
- Per room matrix: are all 6 sub-tables (item table, DAR, conflict register, citations, checklist, criticality note) needed? Or can some be folded into the item table?
- Scope filter: citation additions sub-tables — these list citations "recommended but not yet in item specs." Are these actionable for architects? Or are they editorial notes that should live in the gap register?

**Part 6 — Non-Residential Matrices:**
- §6.0 Universal Non-Residential Provisions — DIR-12: CUT
- Same structural questions as Part 5

**Part 7 — Item Specification Library:**
DIR-14: consolidate where possible. This is the biggest editorial decision set in the workplan.

**Item consolidation candidates (from critique + inspection):**

| Candidate merge | Rationale | Decision needed |
|---|---|---|
| A-01 (Buffer Zones) + A-04 (Acoustic Zoning) | Both address acoustic gradient planning | Same concept at different scales? |
| A-06 (Fabric Panels) + A-07 (Flutter Echo) | Both treat acoustic reflection surfaces | Merge into "Acoustic Surface Treatment"? |
| A-08 (HVAC Noise) + A-09 (HVAC Vibration) | Both address HVAC acoustic performance | Same system, two specs? |
| A-10 (Counter Loop) + A-11 (Room Loop) | Same technology, different scales | Merge into "Hearing Loop Provision"? |
| B-03 (No Fluorescent) + B-04 (Flicker-Free) | Both eliminate harmful light sources | Merge into "Light Source Quality"? |
| C-05 (DEM Inverse Contrast) + C-06 (Plain Flooring) | Both address floor visual complexity for DEM | Merge into "DEM Floor Treatment"? |
| D-08 (Pictogram Signage) + D-09 (Consistent Layout) | Both address cognitive predictability | Keep separate — different trades |
| E-06 through E-09 | Duplicate block exists | Remove duplicate; keep originals |

Also: which items are not directly architectural? E.g., F-02 (Fragrance-Free Zone) is an operational policy, not a design specification. Is it in scope? A-17 (Upholstered Seating) — is this a specification or a furniture procurement note?

**Output:** Decision Register entries for all Vol II Parts 5–7 including per-item consolidation decisions.
**Checkpoint:** Author reviews and approves item consolidation list.

### P1-D4: Volume II Parts 8–9 + Volume III + Appendices (Session 7)

**Part 8 (Engineering, was Part 9):** Scope filter — all engineering coordination content is directly relevant to architects. KEEP. Look for CONDENSE opportunities.

**Part 9 (Specialist Consultants, was Part 10):** DIR-15: consolidate. Merge Role + Triggers + Scope into single subsection per consultant type.

**Part 10 (DAR, was Part 11):** KEEP — actionable cost data.

**Part 11 (Economics, was Part 12):** Scope filter — is this for architects or for policy advocates? Some §11.3 "value" content may be advocacy rather than design guidance. Decision needed: KEEP all (it supports the architect in client conversations) or CONDENSE the advocacy framing?

**Part 12 (Case Studies, was Part 13):** KEEP all 14? Or select the most relevant? Residential emphasis per author: prioritise residential case studies.

**Appendices:** Appendix E (new, from §1.8) — is it needed at all, or can evidence framework descriptions be 2-line glossary entries?

**Output:** Decision Register entries for all remaining Parts + Appendices.

**Phase 1 gate:** Complete Decision Register on GitHub. Author reviews and approves all MERGE, CUT, CONDENSE, and MOVE decisions. This is the most important gate in the workplan — everything downstream depends on it. No Phase 2 work begins until the Decision Register is approved.

---

## Phase 2: Gap Triage + Research (Sessions 8–12)

### P2-T1: Gap Register Triage (Session 8, first half)

With the Decision Register approved, process every OPEN gap register item:

| If the gap's section/item... | Then gap status becomes... |
|---|---|
| Survives (KEEP or CONDENSE) | Remains OPEN — research needed |
| Is merged into another section | OPEN but reassigned to merged target |
| Is cut (CUT) | **CLOSED-ELIMINATED** — no research needed |
| Is moved (MOVE) | Remains OPEN at new location |

**Output:** Updated `gap_register.md` on GitHub. Expected: significant reduction in OPEN items. The 93 current OPEN items may drop to 40–60 depending on how many specs are cut.

**Checkpoint:** Triage complete. Surviving OPEN items form the research list.

### P2-R1: CRPD Text + Co-2 Sources (Session 8, second half)
*(Only if §1.5 and §1.7 survived Phase 1 — they will.)*
- Retrieve CRPD Article 3, 4.3, 9 text
- Retrieve Co-2 tier CPG sources (CAOT, AOTA, RCOT, COTEC)
- Item consolidation analysis (from surviving item list, not full 90)
**Output:** `parts/v10/research/crpd-articles.md`, `co2-sources.md`, `item-consolidation-final.md`

### P2-R2–R5: Literature Reviews (Sessions 9–12)
**Only for populations whose specifications survived Phase 1 with OPEN evidence gaps.**

Likely survivors (these populations have the weakest evidence and the strongest case for inclusion):

| Slug | Sessions | Condition |
|---|---|---|
| `pain-built-environment` | 1 | If PAIN specs survive with ○ markers needing upgrade |
| `ofs-built-environment` | 1 | If OFS specs survive with ○ markers |
| `intd-built-environment` | 1 | If IntD provisions survive (they may be condensed significantly) |
| `residential-home-modification` | 1 | If residential primacy framing creates new evidence needs |
| `neu-built-environment` (supplement) | 0.5 | If NEU specs survive with evidence gaps |
| `mh-built-environment` | 0.5 | If NDV/MH specs survive with gaps |

**Note:** Some of these may be eliminated or reduced in scope by Phase 1 decisions. E.g., if IntD provisions are condensed to a single paragraph pointing to DEM/NDV proxies with an honest ○ disclosure, then the full IntD literature review (estimated at 1 full session) becomes a 30-minute targeted check.

**Phase 2 gate:** All surviving OPEN gaps either researched or explicitly accepted as ○-marked provisions. Research outputs committed to GitHub. BPC entries written for all new slugs.

---

## Phase 3: Writing (Sessions 13–20)

Content revision within the *current* structure (old numbering). Renumbering happens in Phase 4. Phase 3 works from the Decision Register and applies: consolidation, deletion, concision, evidence markers, CRPD quotes, alphabetical sort, and all content directives.

**Operating rule:** Every Part file is edited in place (in the current master document or working copy). The goal is to produce a **content-final** document with correct prose, correct evidence markers, correct consolidations — but still using the old heading numbers. Phase 4 does a single renumbering pass on this content-final document.

### P3-W01: Front Matter + Part 1 Foundations (Session 13)
- Apply all Phase 1 decisions for front matter and Part 1
- Add ●/○ notation guide
- Add illustration note
- Absorb §1.9 into §1.1
- Move §1.8 to Appendix E placeholder
- Merge "Working with OTs" per decision
- Insert CRPD article quotes in §1.7
- Populate Co-2 in §1.5
- Clarify Tier defaults (public=T0/T1, residential=T2)
- Remove all BAR from Vol I
- Concision pass
**Checkpoint:** Part 1 content-final

### P3-W02: Part 2 Disability Categories (Session 14)
- Apply alphabetical sort
- Apply per-category decisions (what stays, what's condensed)
- Add item application tables
- Remove OT framework lines
- Remove inline citations from core needs
- Integrate research findings for categories with surviving gaps
- Apply ●/○ markers
- Remove BAR
- Concision pass — target: each category ≤1 page equivalent (definition, core needs with markers, item application table, population-specific notes)
**Checkpoint:** Part 2 content-final

### P3-W03: Part 3 + Part 4 (Session 15)
- Part 3: remove §3.4 (moved to Part 4); remove BAR from matrix; condense
- Part 4: absorb §3.4 as §4.9; absorb all §8.4.x conflict resolutions; sort §4.9 alphabetically; apply Phase 1 consolidation decisions (merge subsections per Decision Register); number worked examples; number §4.8 subsections; absorb Entry Path I table into §4.4 if decided
- Concision pass on Part 4 — the largest editing task
**Checkpoint:** Parts 3+4 content-final

### P3-W04: Part 5 Residential Matrices (Session 16)
- Apply Phase 1 room matrix decisions
- Remove §5.0a content (absorb into §5.0)
- Remove BAR columns
- Resolve phantom items per Decision Register
- Apply ●/○ markers to matrix entries
- Condense: remove citation addition sub-tables if decided in P1-D3; fold conflict registers into item notes where simple
- Strengthen residential framing
**Checkpoint:** Part 5 content-final

### P3-W05: Part 6 Non-Residential Matrices (Session 17)
- Same operations as Part 5
- Remove §6.0
**Checkpoint:** Part 6 content-final

### P3-W06–W07: Part 7 Item Library — Categories (Sessions 18–19)
- Apply all item consolidation mergers from Decision Register
- Delete items marked CUT
- Apply ●/○ markers to every specification sentence
- Add "[Illustration: to be provided]" to every item
- Add EXPERT CONSENSUS / THIN-BASE disclosures where needed
- Reformat Appendix B/C items to Part 7 template (they become Part 7 items or stay in appendix per Decision Register)
- Fix "Part 11I" references
- Remove duplicate E-06/E-07/E-08/E-09 block
- Resolve all phantom item references (I-04, I-05, I-06, J-xx, H-05, VI-xx)
- Concision pass per item
- Session 18: Categories A–E
- Session 19: Categories F–K + BIO + TC
**Checkpoint:** All categories content-final

### P3-W08: Parts 8–9 + Volume III + Appendices (Session 20)
- Part 8 (Engineering): apply consolidation decisions; concision
- Part 9 (Consultants): merge Role+Triggers+Scope per consultant; concision
- Part 10 (DAR): concision pass
- Part 11 (Economics): reorder §12.3 subsections; apply cost table restructure if decided; concision
- Part 12 (Case Studies): apply selection decisions if any
- Appendix E: write from old §1.8 content
- Bibliography: run `citation-verifier` HARVEST mode across all Parts; assemble bibliography
- Glossary: absorb framework definitions; verify all terms used in document
- Fix all remaining terminology ("Developed Design" → "Design Development", "Commissioning" → "Ready for Occupancy", "MIS" → "NDV/SENS")
**Checkpoint:** All Parts content-final. Document is ready for structural pass.

---

## Phase 4: Structure (Sessions 21–22)

The entire document is now content-final. Heading counts are stable. This is the single point at which renumbering, file decomposition, and cross-reference resolution happen.

### P4-S1: Renumbering (Session 21)

1. Generate the final heading inventory from the content-final document
2. Apply the Part renumbering map (old Part 9→8, 10→9, 11→10, 12→11, 13→12)
3. Apply section renumbering: each Part N uses §N.x
4. Use `bulk-renumber` skill with the complete renumbering map
5. Run in dry-run mode first; review changes; then apply
6. Generate Change Order CO-0002

**Checkpoint:** All sections correctly numbered. Zero old numbering remains.

### P4-S2: File Decomposition + Cross-Reference Resolution (Session 22)

1. Use `file-splitter` to decompose into per-Part and per-Category .md files per the file architecture
2. Use `cross-reference-resolver` to scan all files for orphan references
3. Fix any cross-reference breaks (there should be very few since renumbering was done on the assembled document)
4. Update `references/toc.md` from final heading structure
5. Commit all files to `parts/v10/` on GitHub
6. Create `parts/v10/assembly-manifest.md`

**Phase 4 gate:** All files on GitHub. toc.md current. Zero orphan references. Assembly manifest complete.

---

## Phase 5: QA + Assembly (Sessions 23–25)

### P5-Q1: Automated Audits (Session 23)
- `framing-checker` full pass (social model, BAR-in-Vol-I, CRPD)
- `evidence-marker` AUDIT mode (100% ●/○ coverage check)
- `structure-auditor` (heading hierarchy across all files)
- `guidebook-auditor` (format, terminology, table consistency)
- `sensory-coherence-checker` on all room matrices

### P5-Q2: Prose + Citation QA (Session 24)
- `prose-style-checker` full pass
- `citation-verifier` against bibliography (provisional — check that every cited source appears in bibliography)
- Manual spot-check of 10 cross-references per volume

### P5-Q3: Assembly + Final (Session 25)
- `chunk-assembler` with manifest → master document
- Line count and heading count verification
- Final commit of assembled v10.0
- Session consolidator → final session YAML
- Update gap register (close all resolved items)
- Update project-standards.md with any new rules from Phase 3–5
- Produce handoff summary

---

## Decision Points (Updated)

| ID | Question | Phase | Blocking |
|---|---|---|---|
| **DEC-01** | Per-item consolidation: approve/reject each merger in Decision Register | P1-D3 | Yes — blocks Phase 3 |
| **DEC-02** | Entry Path I table: absorb into §4.4, or cut entirely? | P1-D2 | No |
| **DEC-03** | I-04/I-05/I-06: create, merge, or delete? | P1-D3 | Yes — blocks Phase 3 |
| **DEC-04** | H-05 (Nurse Call): create or redirect? | P1-D3 | No |
| **DEC-05** | IntD: full evidence review or condensed ○-marked proxy paragraph? | P1-D1 | Yes — determines Phase 2 research scope |
| **DEC-06** | BIO/TC items: promote to Part 7 main library or keep in appendices? | P1-D3 | No |
| **DEC-07** | Room matrix sub-tables: keep all 6 or condense to 3 (item table, DAR, checklist)? | P1-D3 | No |
| **DEC-08** | §11.4 Cost tables: map to item categories, room types, or keep current? | P1-D4 | No |
| **DEC-09** | Case studies: keep all 14 or select? | P1-D4 | No |
| **DEC-10** | Appendix E (Evidence Frameworks): separate appendix or glossary expansion? | P1-D4 | No |
| **DEC-11** | Worked examples: keep 5 or reduce to 3? | P1-D2 | No |
| **DEC-12** | F-02 (Fragrance-Free): design spec or operational policy? Keep or cut? | P1-D3 | No |
| **DEC-13** | A-17 (Upholstered Seating): design spec or procurement note? | P1-D3 | No |

---

## Session Plan (Final)

| Session | Phase | Work |
|---|---|---|
| 1 | P0 | Build: github-io, file-splitter, evidence-marker. Update: framing-checker, evidence-auditor, item-spec-writer |
| 2 | P0 | Build: bulk-renumber. Update: cross-ref-resolver, structure-auditor, chunk-assembler, workplan-orchestrator, session-consolidator, vol2-item-formatter |
| 3 | P0 | Build: citation-miner, sensory-coherence-checker. Update: citation-verifier (+HARVEST) |
| 4 | P1 | Editorial decisions: Vol I (Parts 1–3) |
| 5 | P1 | Editorial decisions: Vol II front matter + Part 4 |
| 6 | P1 | Editorial decisions: Parts 5–7 (matrices + item library) — **author approval gate** |
| 7 | P1 | Editorial decisions: Parts 8–9, Vol III, Appendices — **Decision Register complete** |
| 8 | P2 | Gap triage (CLOSE-ELIMINATED) + CRPD text + Co-2 sources + item consolidation analysis |
| 9 | P2 | Lit review: PAIN (if surviving gaps) |
| 10 | P2 | Lit review: OFS (if surviving gaps) |
| 11 | P2 | Lit review: IntD (scope determined by P1-D1 DEC-05) |
| 12 | P2 | Lit review: residential + NEU supplement + NDV/MH (combined) |
| 13 | P3 | Write: Front matter + Part 1 |
| 14 | P3 | Write: Part 2 (disability categories) |
| 15 | P3 | Write: Parts 3 + 4 (multiple categories + synthesis) |
| 16 | P3 | Write: Part 5 (residential matrices) |
| 17 | P3 | Write: Part 6 (non-residential) |
| 18 | P3 | Write: Part 7 Categories A–E |
| 19 | P3 | Write: Part 7 Categories F–K + BIO + TC |
| 20 | P3 | Write: Parts 8–12 + Appendices + Bibliography + Glossary |
| 21 | P4 | Renumber (single pass, content-final document) |
| 22 | P4 | File decomposition + cross-reference resolution |
| 23 | P5 | QA: framing, evidence markers, structure, sensory coherence |
| 24 | P5 | QA: prose, citations, spot-checks |
| 25 | P5 | Assembly, final commit, gap register close, handoff |

**Total: 25 sessions.** Phase 1 editorial decisions are the critical path — everything downstream depends on them.

---

*End of Integrated Workplan v10.0*
