# Workplan: Website Preparation
**Created:** 2026-04-09 22:30
**Basis:** [Interactive accessibility design resource platform](https://claude.ai/chat/94f71d00-604b-42c9-bbc2-125919587465) conversation (2026-04-04)
**Status:** DRAFT — requires user review before execution

---

## 1. Strategic Context

The April 4 conversation established that this project's value is better realized as an interactive web platform than a static document. The key insight: **the intellectual work (evidence synthesis, specification determination, conflict resolution) is format-independent — it transfers directly to a database-backed platform. The document-assembly work does not.**

### What transfers as-is
- All BPC files (93 files across 14 topic directories) → evidence records
- Specification database (73 records from batch 1; schema established) → specification records
- Connection register (181 entries, 83 consumed, 98 pending) → cross-reference relationships
- Cost data (2 files: US/UK/AU primary + 5-language multilingual) → economics module records
- Population profiles (Parts 1–2) → population reference pages
- Case studies (Part 12) → case study entries
- Conflict resolution matrices (Part 5) → interactive conflict resolver
- Room matrices (Parts 6–7) → room-type lookup engine
- Search logs (14 topic directories) → research transparency layer

### What stops
- Document assembly, TOC management, cross-reference resolution within prose
- Markdown formatting, line-break fixing, section renumbering
- Change orders for heading hierarchy
- Any work whose purpose is making the *document* internally consistent

### What continues (unchanged priority)
- BPC research pipeline (evidence quality drives everything)
- FDR scenarios (functional deficit research)
- Connection scout (cross-population relationship discovery)
- Citation verification
- Multilingual research
- Opus synthesis (best-practice determination)
- Economics evidence gathering

---

## 2. Platform Architecture Decision

### 2.1 Decision required: Technology stack

This workplan is **pre-stack** — it focuses on data preparation, schema design, and content structuring that is stack-independent. The stack decision should be made after this preparation work is substantially complete, because the data shape will inform the technology choice.

That said, the April 4 conversation identified these requirements that constrain the stack:

| Requirement | Implication |
|---|---|
| Interactive process charts (top-down by population, bottom-up by functionality) | Client-side interactivity; filterable data model |
| Economic argument builder | Calculation engine; parameterized cost models |
| Case study analysis with community feedback | User accounts; moderated submissions; lived-experience priority |
| Crowdsourced evidence with lived-experience priority | Authentication; role-based access; review workflow |
| WCAG AAA compliance (non-negotiable for this project) | Constrains framework/component choices |
| Multilingual content (14+ languages in evidence base) | i18n architecture; RTL support for future Arabic/Hebrew sources |
| Offline capability for field practitioners | PWA or similar; local data caching |

**Candidate stacks** (to be evaluated in Phase 3):

| Option | Strengths | Risks |
|---|---|---|
| Next.js + PostgreSQL + Prisma | SSR for accessibility; rich ecosystem; Vercel hosting | Complexity; maintenance burden |
| Astro + Starlight (docs framework) + SQLite | Simpler; content-focused; static-first with islands | Less interactive capability; may not support user accounts |
| SvelteKit + Supabase | Lightweight; excellent accessibility story; auth built in | Smaller ecosystem; fewer accessibility-tested component libraries |
| Docusaurus/MkDocs + API layer | Fastest path from existing markdown | Limited interactivity; not a real application |

**Recommendation:** Defer this decision. Phase 1–2 work is stack-agnostic.

### 2.2 Content architecture (from April 4 conversation)

The website is **not a digitized document**. It is a relational data platform with six primary interfaces:

1. **Specification Explorer** — every item spec (A-01 through K-NN) as a queryable record with evidence trails, population tags, jurisdiction data, Tier 0/1/2 ranges, and linked BPC synthesis
2. **Population Navigator** — top-down entry: select population → see all relevant specifications, room considerations, co-occurrence patterns, conflict zones
3. **Room Configurator** — select room type + building type + applicable populations → generated specification checklist with conflict flags
4. **Conflict Resolver** — interactive decision tree for cross-population conflicts (Part 5 content) with worked examples
5. **Economics Engine** — cost-premium calculator, retrofit-vs-new-build comparator, grant programme finder by jurisdiction, SROI/QALY argument builder
6. **Case Study Library** — documented accessible environments with tagged specifications, searchable by building type/population/jurisdiction, community contribution pipeline

Two cross-cutting layers:
- **Evidence Transparency** — every specification links to its BPC, search log, and source citations; evidence tier visible; language-agnostic display
- **Community Evidence** — lived experience submissions, professional feedback, moderated evidence contributions with CRPD Art. 4.3 priority weighting

---

## 3. Phased Workplan

### Phase 0: Schema Consolidation (Sonnet — 2–3 sessions)
**Goal:** Finalize the canonical data schema that all subsequent extraction targets.

| Task | Input | Output | Dependencies |
|---|---|---|---|
| 0.1 Extend specification-database-schema.md | Current 73-record schema | Comprehensive schema covering all 6 interfaces | None |
| 0.2 Design population schema | Part 2 population profiles + BPC population files | `populations.json` schema with functional-need taxonomy | None |
| 0.3 Design room-type schema | Parts 6–7 matrices | `room-types.json` schema with population × specification mapping | 0.1 |
| 0.4 Design conflict schema | Part 5 content + connection register | `conflicts.json` schema with resolution pathways and decision trees | 0.1, 0.2 |
| 0.5 Design case-study schema | Part 12 content | `case-studies.json` schema with specification tags and outcome data | 0.1 |
| 0.6 Design economics schema | Part 11 + cost-data files | `economics.json` schema with cost models, grant programmes, multipliers | 0.1 |
| 0.7 Schema review + cross-referential integrity check | All 0.x outputs | Unified ERD; foreign key map; identified normalization issues | 0.1–0.6 |

**Deliverable:** `references/website/schema/` directory with all JSON schemas + ERD documentation.

### Phase 1: Data Extraction — Specifications (Sonnet — 8–12 sessions)
**Goal:** Complete the specification database from all 93 BPC files.

| Task | Input | Output | Sessions est. |
|---|---|---|---|
| 1.1 Batch 2 extraction (next 20 BPC files) | BPC topic files | specification-database.json additions | 2 |
| 1.2 Batch 3 extraction (next 20) | BPC topic files | specification-database.json additions | 2 |
| 1.3 Batch 4 extraction (next 20) | BPC topic files | specification-database.json additions | 2 |
| 1.4 Batch 5 extraction (remaining ~23) | BPC topic files | specification-database.json additions | 2 |
| 1.5 Population BPC extraction (14 files) | BPC population files (MOB.md, VIS.md, etc.) | Population-specific specification overlays | 1 |
| 1.6 Deduplication + normalization pass | Complete spec DB | Deduplicated, cross-referenced, gaps flagged | 1 |
| 1.7 Item-code mapping pass | spec DB + Part 4 | Every record mapped to Part 4 item code (or flagged as orphan) | 1–2 |

**Deliverable:** Complete `specification-database.json` with ~400–600 records covering all BPC files.

### Phase 2: Data Extraction — Other Entities (Sonnet — 6–8 sessions)
**Goal:** Populate the remaining schemas.

| Task | Input | Output | Sessions est. |
|---|---|---|---|
| 2.1 Population data extraction | Part 2 + population BPCs | `populations.json` — 14 population records with functional-need taxonomies | 1 |
| 2.2 Room-type matrix extraction | Parts 6–7 | `room-types.json` — room × population × specification cross-reference | 2 |
| 2.3 Conflict extraction | Part 5 + connection register | `conflicts.json` — conflict scenarios with resolution pathways | 2 |
| 2.4 Case study extraction | Part 12 | `case-studies.json` — tagged case studies | 1 |
| 2.5 Economics extraction | Part 11 + cost-data files | `economics.json` — cost models, grant data, multiplier tables | 1 |
| 2.6 Cross-referential integrity validation | All 2.x outputs + spec DB | Integrity report; orphaned references; missing links | 1 |

**Deliverable:** Complete data layer in `references/website/data/`.

### Phase 3: Stack Decision + Prototype (Opus assessment → Sonnet build — 3–5 sessions)
**Goal:** Select technology stack and build a functional prototype of one interface.

| Task | Description | Model |
|---|---|---|
| 3.1 Stack evaluation | Evaluate candidate stacks against requirements (§2.1) with WCAG AAA, i18n, community features, hosting cost, maintenance burden | Opus |
| 3.2 Accessibility component audit | Evaluate accessible component libraries (Radix, React Aria, HeadlessUI, Shoelace) for WCAG AAA compliance | Sonnet + research |
| 3.3 Prototype: Specification Explorer | Build one complete interface — the Specification Explorer — as a functional prototype | Sonnet |
| 3.4 Prototype user testing plan | Design a testing protocol with screen reader, switch access, voice control, and cognitive load evaluation | Opus |

**Deliverable:** Functional prototype of one interface; stack decision documented; testing plan.

### Phase 4: Content Transformation (Sonnet — 10–15 sessions)
**Goal:** Transform guidebook prose into web-native content.

| Task | Description | Sessions est. |
|---|---|---|
| 4.1 Part 1 → About/Methodology pages | Rewrite for web (shorter, scannable, not chapter-sequential) | 2 |
| 4.2 Part 2 → Population profile pages | Each population as standalone page with linked specifications | 2 |
| 4.3 Part 3 → Co-occurrence framework | Interactive compound-population tool content | 1 |
| 4.4 Part 4 → Specification detail pages | Each item spec as a standalone record with evidence, population tags, tier ranges | 3–4 |
| 4.5 Part 5 → Conflict resolver content | Decision tree content for interactive resolver | 2 |
| 4.6 Parts 10–11 → DAR + Economics content | Calculator inputs, argument templates, grant databases | 2 |
| 4.7 Part 12 → Case study entries | Structured tagged entries | 1 |

**Deliverable:** Web-ready content in `references/website/content/` — markdown with YAML frontmatter per schema.

### Phase 5: Community Infrastructure Design (Opus — 2–3 sessions)
**Goal:** Design the community evidence contribution system.

| Task | Description |
|---|---|
| 5.1 Submission workflow design | Lived-experience submission form → moderation → evidence integration pipeline |
| 5.2 Evidence weighting protocol | How community contributions are weighted relative to clinical research (CRPD Art. 4.3 alignment) |
| 5.3 Professional review workflow | How OT/architect/engineer submissions are validated |
| 5.4 Moderation policy | Content moderation, abuse prevention, accessibility of moderation tools |
| 5.5 Privacy and consent framework | Data handling for lived-experience contributors; GDPR/privacy compliance |

**Deliverable:** Community infrastructure specification document.

### Phase 6: Build (Sonnet — ongoing)
**Goal:** Construct the website.

This phase is out of scope for this workplan. It begins after Phases 0–5 are substantially complete and produces a deployable web application. Estimated scope: 30–50 sessions depending on stack choice and feature prioritization.

---

## 4. Parallel Work Streams

The following existing work streams continue in parallel with website preparation. They are not blocked by or blocking the website workplan — they feed it.

| Stream | Current state | Website relevance |
|---|---|---|
| BPC research pipeline | 93 files across 14 topics | Direct: populates specification database |
| FDR scenarios | 45-scenario registry; 7 P1 granular scenarios queued | Direct: generates new specifications |
| Connection scout | 181 connections; 98 PENDING | Direct: populates cross-reference layer |
| Opus synthesis queue | Ongoing | Direct: produces `bpc_synthesis` field content |
| Multilingual research | 14 languages × 24 jurisdictions | Direct: populates jurisdiction data |
| Citation verification | Ongoing | Direct: evidence integrity |
| Economics evidence | Bottom-up cost data; 7-country grant mapping | Direct: populates economics engine |
| Systematic reviews | 5 deep-dive protocols established | Direct: strengthens evidence tier assignments |
| Language bias audit | Complete (2026-04-09) | Quality assurance: confirmed no language weighting in evidence |

---

## 5. What This Workplan Does NOT Cover

1. **Domain registration and hosting** — requires user decision on domain name, hosting provider, budget
2. **Visual design / branding** — requires design input beyond Claude's scope; recommend engaging a designer with accessibility expertise
3. **User authentication system** — depends on stack choice (Phase 3) and community feature scope (Phase 5)
4. **Content management system** — whether the team uses a headless CMS, git-based workflow, or direct database editing
5. **Legal** — terms of service, privacy policy, contributor license agreement, liability disclaimers
6. **Analytics** — privacy-respecting analytics choice (Plausible, Fathom, etc.)
7. **SEO and discoverability** — metadata, structured data, academic indexing
8. **Maintenance and update workflow** — how new evidence flows from research to database to website

---

## 6. Immediate Next Actions

**This session (if context permits):**
1. Commit this workplan to `workplan/website-preparation.md`
2. Create `references/website/` directory structure on GitHub

**Next session:**
1. Phase 0.1 — extend specification-database-schema.md to cover all six interfaces
2. Phase 0.2 — design population schema

**Decision needed from user:**
1. Confirm workplan direction and phasing
2. Confirm that document assembly work should stop (per April 4 conclusion)
3. Any priority reordering of the six interfaces
4. Budget/hosting preferences (informs Phase 3 stack decision)
5. Whether community features (Phase 5) are MVP or post-launch

---

## 7. Effort and Timeline Estimate

| Phase | Sessions | Model | Effort level |
|---|---|---|---|
| 0: Schema | 2–3 | Sonnet | 125 |
| 1: Spec extraction | 8–12 | Sonnet | 100 |
| 2: Other extraction | 6–8 | Sonnet | 100 |
| 3: Stack + prototype | 3–5 | Opus + Sonnet | 150 |
| 4: Content transform | 10–15 | Sonnet | 100 |
| 5: Community design | 2–3 | Opus | 150 |
| **Total pre-build** | **31–46** | | |
| 6: Build | 30–50 | Sonnet | 100–125 |
| **Total** | **61–96** | | |

Parallel research streams (BPC, FDR, connections, economics) continue throughout and are not counted above — they are already ongoing work that happens to feed the website.

---

## 8. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Schema changes mid-extraction require re-extraction | MODERATE | HIGH | Phase 0 schema review is thorough; include version field in all records |
| WCAG AAA compliance constrains interactive features | LOW | MODERATE | Audit component libraries early (Phase 3.2); test with assistive technology |
| Community features introduce moderation burden | HIGH | MODERATE | Phase 5 designs moderation before build; consider launch without community features |
| Specification database too large for client-side filtering | LOW | LOW | Pagination/server-side filtering; assess at prototype stage |
| Evidence base still growing — website content becomes stale | HIGH | MODERATE | Design update pipeline (Phase 5); version all data; show "last updated" per record |
| Scope creep from six interfaces | HIGH | HIGH | Prioritize: Specification Explorer first, then Population Navigator, then Room Configurator. Others are post-MVP. |

---

## 9. MVP Definition

If resource constraints require a reduced scope, the **minimum viable product** is:

1. **Specification Explorer** — searchable, filterable specification database with evidence trails
2. **Population Navigator** — population entry point linking to relevant specifications
3. **About/Methodology** — foundational pages explaining the framework

Everything else (Room Configurator, Conflict Resolver, Economics Engine, Case Study Library, Community Evidence) is post-MVP.

This MVP is achievable with a static site generator + JSON data files — no database, no auth, no server. It could ship as a GitHub Pages site as an intermediate step.
