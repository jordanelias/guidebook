# Workplan: Website Preparation — v2 (Comprehensive)
**Created:** 2026-04-09 22:30
**Revised:** 2026-04-17 (v2 — comprehensive scope review against April 4 source conversation)
**Basis:** [Interactive accessibility design resource platform](https://claude.ai/chat/94f71d00-604b-42c9-bbc2-125919587465) (2026-04-04)
**Status:** DRAFT — requires user review before execution

---

## 0. Gap Analysis: v1 → v2

The April 4 conversation specified a 13-section platform design with detailed page types, interactive tools, community layers, and technical architecture. The v1 workplan captured the data extraction pipeline but omitted or underspecified the following:

| Gap | April 4 specification | v1 coverage |
|---|---|---|
| **Functional task axis (Axis 2)** | Bottom-up navigation: functional task → specification → population. Your original request: "bottom up by functionality (toilet transfers)" | Missing entirely. No entity, no schema, no extraction. |
| **Brief Builder / Decision Engine** | 8-step interactive workflow: population selection → building type → design tier → conflict dashboard → specification list → OT appointment → export PDF + shareable URL. Implements §3.8 decision tree. | Mentioned as "prototype one interface" in Phase 3. No schema, no data preparation, no logic extraction. |
| **Engineering coordination pages** | `/engineering/[discipline]` — filtered view per engineering discipline (structural, mechanical, electrical, fire) of all specs requiring that discipline's input, grouped by design stage | Not mentioned. |
| **Jurisdiction comparison tool** | Multi-select jurisdiction dropdown; side-by-side standards table filterable by specification category | Not mentioned. |
| **Co-occurrence matrix tool** | Interactive table from Part 3 §3.3; per-cell: prevalence, worked examples, conflict count | Not mentioned. |
| **Standards entity** | Standards registry as queryable entity with currency status, jurisdiction, version, supersession tracking | Not in schema. Jurisdiction data is on spec records but no standalone standards entity. |
| **Functional task entity** | Tasks (toilet transfer, wayfinding, kitchen preparation, fire egress, seated task performance) mapped to specifications and populations | Missing entirely. |
| **Downloadable drawings** | Dimensions.com parallel — SVG/DWG detail drawings per specification | Not mentioned. |
| **OT appointment trigger tool** | Part 9 §9.2.2 logic: given population brief, does this project require OT appointment? | Not in any schema or extraction plan. |
| **Multi-audience pathways** | Primary (architects), secondary (OTs), tertiary (engineers/consultants), quaternary (disabled people, advocates, policy makers) — each with distinct entry points | Not addressed. |
| **Specific page types** | Specification canonical page, population hub, building-type hub, functional task page, engineering coordination page, standards index, case study with submission, about/methodology, legal/disclaimer/privacy/licensing, changelog | Only partially listed in content transformation. |
| **Stack recommendation** | April 4 concluded: Next.js + PostgreSQL + Directus CMS + Meilisearch. Self-hosted. | v1 listed 4 candidates and deferred. The analysis was already done. |
| **AI integration** | Claude API assistant for conversational specification lookup and decision engine guidance | Not mentioned. |
| **Supplementary populations** | CHD, LPA, EXH, BAR — include in MVP or defer? ~40 additional specifications. | Not addressed. |
| **Legal/governance content** | CC BY-SA 4.0 licensing, disclaimer (not a substitute for professional judgment), privacy (GDPR), contributor license agreement | Listed under "not covered" but April 4 specified these as Phase 2 deliverables. |
| **Changelog** | Auto-generated from database version history | Not mentioned. |
| **Update pipeline** | How new evidence flows: research → BPC → database → website. Standards currency monitoring. | Listed under "not covered" but April 4 specified ongoing post-launch cycle. |
| **Accessibility testing protocol** | axe-core CI, NVDA + VoiceOver, keyboard navigation, reduced motion, Lighthouse ≥90/≥95 | Mentioned as requirement but no protocol. |
| **Open questions** | 7 specific decisions identified: domain, V9 vs V10 content, supplementary populations, dimensioned drawings, multilingual at launch, AI integration, relationship to existing document | v1 listed only 4. |

---

## 1. Strategic Context

*(Unchanged from v1 — the April 4 conclusions about what transfers, what stops, and what continues remain correct.)*

### What transfers as-is
All BPC files (93) → evidence records. Specification database (73 records, batch 1) → specification records. Connection register (181 entries) → cross-reference relationships. Cost data (2 files) → economics records. Population profiles (Parts 1–2) → population pages. Case studies (Part 12) → case study entries. Conflict resolution matrices (Part 5) → interactive conflict resolver. Room matrices (Parts 6–7) → room-type lookup. Search logs (14 topic directories) → research transparency layer.

### What stops
Document assembly, TOC management, cross-reference resolution within prose, formatting, section renumbering, change orders for heading hierarchy.

### What continues (unchanged priority)
BPC research, FDR scenarios, connection scout, citation verification, multilingual research, Opus synthesis, economics evidence gathering.

---

## 2. Platform Architecture

### 2.1 Technology stack

The April 4 conversation completed a stack evaluation. The recommendation stands:

| Layer | Choice | Rationale |
|---|---|---|
| **Database** | PostgreSQL | Relational model matches entity relationships; JSONB for flexible fields; full-text search fallback |
| **CMS / API** | Directus (self-hosted) | Database-first; auto-generates REST + GraphQL; open-source; full data ownership; CRPD-aligned open-access philosophy argues against vendor lock-in |
| **Frontend** | Next.js (React) with SSR | WCAG compliance; SEO via server rendering; React ecosystem for D3/Recharts interactive tools; largest accessible component library ecosystem |
| **Search** | Meilisearch | Faceted filtering (population, building type, category, evidence tier, jurisdiction, conflict status, functional task, design stage); fast; self-hosted |
| **Analytics** | Plausible | Privacy-respecting; cookieless; GDPR-compliant |
| **Hosting** | Self-hosted (VPS) or Directus Cloud ($15/mo fallback) | Data sovereignty for community contributions |

### 2.2 Content architecture: Four navigation axes

The website serves four distinct audiences through four navigation axes to the same underlying data:

**Axis 1 — Top-down (Architect's workflow):** Building type → Population → Specification
"I'm designing a hospital; what do I need?"

**Axis 2 — Bottom-up (OT's workflow):** Functional task → Specification → Population
"My client can't transfer safely; what does the built environment need?"

**Axis 3 — Economic (Client/developer/policy workflow):** Cost curve → Item specification → Decision stage
"What does this cost, and what do I get?"

**Axis 4 — Evidence (Researcher/policy/advocate workflow):** Evidence tier → Specification → Jurisdiction → Citation
"What's the evidence base for this specification, and which standards require it?"

### 2.3 Eight entity types

| Entity | Source | Interface served | Target records |
|---|---|---|---|
| Specifications | Part 4 + BPC files | Specification Explorer (core) | 400–600 |
| Populations | Part 2 + BPC population files | Population Navigator | 14 |
| Room types | Parts 6–7 matrices | Room Configurator (Axis 1) | 25–30 |
| Conflicts | Part 5 + connection register | Conflict Resolver | 14+ |
| Economics | Part 11 + cost-data files | Economics Engine (Axis 3) | 50–80 |
| Case studies | Part 12 | Case Study Library | 8–12 initial |
| **Functional tasks** | Part 3 §3.5–3.12 + Part 4 item descriptions + OT frameworks | **Task Navigator (Axis 2)** | 30–50 |
| **Standards** | Standards registry + jurisdiction tracker | **Jurisdiction Comparison tool** | 100–150 |

Cross-cutting entities (unchanged from v1): Connections (181 records), Citations (normalized, deduplicated).

### 2.4 Interactive tools (five)

| Tool | Source content | Data dependencies |
|---|---|---|
| **Brief Builder** (Decision Engine) | Part 3 §3.8 decision tree + Part 5 conflicts + Part 9 §9.2.2 OT triggers | Specifications, populations, conflicts, OT appointment logic |
| **Cost Explorer** | Part 11 cost curves + cost-data files | Economics entity (premiums, multipliers, grant programmes) |
| **Conflict Matrix** | Part 5 §5.2 | Conflicts entity (12 domains, population pairs) |
| **Co-occurrence Matrix** | Part 3 §3.3 | Population pairs, prevalence data, conflict domain counts |
| **Jurisdiction Comparison** | Standards registry + jurisdiction tracker | Standards entity (side-by-side comparison) |

### 2.5 Page types (comprehensive)

| Page type | URL pattern | Content source |
|---|---|---|
| Specification detail | `/specifications/[item_code]` | Spec entity + linked populations, conflicts, case studies, standards, economics |
| Population hub | `/populations/[code]` | Population entity + all tagged specs, co-occurrence data |
| Building-type hub | `/building-types/[type]` | Room-type entity + applicable specs per population + conflict alerts |
| Functional task | `/tasks/[task_slug]` | Task entity + relevant specs + populations served |
| Room detail | `/rooms/[room_id]` | Room entity + item matrix + DAR provisions + conflict register |
| Conflict detail | `/conflicts/[conflict_id]` | Conflict entity + decision tree + worked examples |
| Case study | `/case-studies/[id]` | Case study entity + tagged specs + outcomes + financials |
| Engineering coordination | `/engineering/[discipline]` | Specs filtered by discipline input, grouped by design stage |
| Standards index | `/standards` | Standards entity, filterable by jurisdiction and category |
| Brief Builder | `/brief-builder` | Interactive tool — all entities |
| Cost Explorer | `/economics` | Economics entity + interactive chart |
| Search | `/search` | Meilisearch faceted search across all entities |
| About / Methodology | `/about/methodology` | Part 1 adapted |
| Evidence hierarchy | `/about/evidence-hierarchy` | Part 1 §1.5 |
| Three-tier hierarchy | `/about/three-tier-hierarchy` | Part 1 §1.4.3 |
| Population overview | `/about/populations` | Summary with links |
| Disclaimer | `/legal/disclaimer` | "Not a substitute for professional judgment" |
| Privacy | `/legal/privacy` | GDPR compliance |
| Licensing | `/legal/licensing` | CC BY-SA 4.0 |
| Changelog | `/changelog` | Auto-generated from database version history |

### 2.6 Community layers (three)

| Layer | Mechanism | Feeds |
|---|---|---|
| **Lived experience feedback** | Structured form per specification: "Does this work for you? What's missing?" Tagged by population, building type, geography. Moderated. | Gap register; Co-1 evidence tier |
| **Practitioner POE submissions** | Post-occupancy evaluation against case study schema. Financial data quality tier (VERIFIED/PROVISIONAL/GREY). | Case study library; economics database |
| **Jurisdiction updates** | Standards currency tracking. Practitioners flag superseded standards. | Standards registry |

Priority weighted toward disabled people's contributions — both in interface design (site meets its own specifications) and moderation policy.

---

## 3. Phased Workplan

### Phase 0: Schema Consolidation (Sonnet — 3–4 sessions)

| Task | Input | Output | Status |
|---|---|---|---|
| 0.1 Specification schema | Existing 73-record schema | Extended schema (all fields per v1 unified-data-schema.md) | **DONE** (2026-04-09) |
| 0.2 Population schema + extraction | Part 2 | `populations.json` — 11 records | **DONE** (2026-04-09) |
| 0.3 Room-type schema | Parts 6–7 matrices | `room_types.json` schema | PENDING |
| 0.4 Conflict schema + extraction | Part 5 + connection register | `conflicts.json` — 14 records | **DONE** (2026-04-09) |
| 0.5 Case study schema | Part 12 | `case_studies.json` schema | PENDING |
| 0.6 Economics schema | Part 11 + cost-data files | `economics.json` schema (3 sub-entities) | PENDING |
| **0.7 Functional task schema** | Part 3 §3.5–3.12 + Part 4 item descriptions + OT frameworks (PEOP, EHP, CMOP-E) | **`functional_tasks.json` schema mapping tasks → specs → populations** | **NEW** |
| **0.8 Standards schema** | Standards registry + jurisdiction-tracker output | **`standards.json` schema with currency, version, supersession** | **NEW** |
| **0.9 Brief Builder logic schema** | Part 3 §3.8 decision tree + Part 9 §9.2.2 OT triggers | **`brief_builder_logic.json` — decision tree nodes, OT appointment conditions, conflict detection rules** | **NEW** |
| 0.10 Cross-referential integrity check | All 0.x outputs | Unified ERD; foreign key map; integrity rules | PENDING |

### Phase 1: Data Extraction — Specifications (Sonnet — 8–12 sessions)

*(Unchanged from v1 — batches 2–5 of BPC extraction, deduplication, item-code mapping.)*

Target: ~400–600 records from all 93 BPC files. Includes new fields from extended schema: `retrofit_penalty`, `dar_relevant`, `design_stage_lock`, `engineering_disciplines`, `functional_tasks`.

**New fields to extract per specification (v2 additions):**

| Field | Source | Purpose |
|---|---|---|
| `design_stage_lock` | Part 4 retrofit notes + Part 8 | Which design stage must this be decided at? Feeds process timeline. |
| `engineering_disciplines` | Part 8 + Part 4 cross-references | Which engineering disciplines need to coordinate? Feeds engineering pages. |
| `functional_tasks` | Part 4 item descriptions + OT evidence basis | Which functional tasks does this specification serve? Feeds Axis 2. |
| `ve_risk` | Part 8 §8.3.3 VE Protection Register | Is this specification at risk of value engineering? Feeds Brief Builder warnings. |
| `ot_appointment_trigger` | Part 9 §9.2.2 | Does specifying this item require OT involvement? Boolean + conditions. |
| `drawing_available` | New field — initially all false | Whether a downloadable detail drawing exists for this specification. |

### Phase 2: Data Extraction — Other Entities (Sonnet — 10–14 sessions)

| Task | Input | Output | Sessions est. |
|---|---|---|---|
| 2.1 Population data extraction | Part 2 + population BPCs | `populations.json` — 14 records | **DONE** |
| 2.2 Room-type matrix extraction | Parts 6–7 | `room_types.json` — ~25–30 room records with item matrices | 2 |
| 2.3 Conflict extraction | Part 5 + connection register | `conflicts.json` — 14+ records with decision trees | **DONE** |
| 2.4 Case study extraction | Part 12 | `case_studies.json` — 8–12 records with tagged specs and outcomes | 1 |
| 2.5 Economics extraction | Part 11 + cost-data files | `economics.json` — premiums, multipliers, grant programmes | 1 |
| **2.6 Functional task extraction** | Part 3 §3.5–3.12 + Part 4 + OT frameworks | **`functional_tasks.json` — 30–50 task records mapped to specs and populations** | **2 (NEW)** |
| **2.7 Standards extraction** | Standards registry + jurisdiction-tracker + BPC jurisdiction data | **`standards.json` — 100–150 standards records with jurisdiction, version, currency** | **2 (NEW)** |
| **2.8 Brief Builder logic extraction** | Part 3 §3.8 + Part 5 + Part 9 §9.2.2 | **`brief_builder_logic.json` — decision tree, OT triggers, conflict detection rules** | **2 (NEW)** |
| **2.9 Engineering coordination extraction** | Part 8 + Part 4 design stage annotations | **`engineering_coordination.json` — specs per discipline per stage** | **1 (NEW)** |
| 2.10 Cross-referential integrity validation | All 2.x outputs + spec DB | Integrity report; orphaned references | 1 |

### Phase 3: Stack Setup + MVP Prototype (Opus assessment → Sonnet build — 5–8 sessions)

| Task | Description | Sessions est. |
|---|---|---|
| 3.1 Stack finalization | Confirm Next.js + Directus + PostgreSQL + Meilisearch. Document deployment architecture, CI/CD pipeline, backup strategy. | 1 (Opus) |
| 3.2 Accessibility component audit | Evaluate Radix, React Aria, HeadlessUI, Shoelace for WCAG AAA compliance. Select component library. | 1 |
| 3.3 Database schema → PostgreSQL migration | Transform JSON schemas into PostgreSQL DDL. Directus collection configuration. Migration scripts. | 2 |
| 3.4 Data import pipeline | Scripts to import all JSON data files into PostgreSQL. Validation against integrity rules. | 1 |
| 3.5 Prototype: Specification Explorer | One complete page type: `/specifications/[item_code]` with all related data, responsive, accessible. | 1–2 |
| 3.6 Accessibility testing protocol | axe-core CI integration; NVDA + VoiceOver manual protocol; keyboard navigation checklist; Lighthouse targets (Performance ≥90, Accessibility ≥95). | 1 (Opus) |

### Phase 4: Content Transformation (Sonnet — 12–18 sessions)

| Task | Description | Sessions est. |
|---|---|---|
| 4.1 Part 1 → About / Methodology / Evidence hierarchy / Three-tier hierarchy | Rewrite for web: shorter, scannable, standalone pages | 2 |
| 4.2 Part 2 → Population profile pages | Each population as standalone hub with linked specs, co-occurrence, evidence confidence | 2 |
| 4.3 Part 3 → Co-occurrence framework + Brief Builder content | Decision tree content for interactive tool; co-occurrence matrix data | 2 |
| 4.4 Part 4 → Specification detail pages | Each item spec as canonical web page with all entity links | 3–4 |
| 4.5 Part 5 → Conflict resolver content | Decision trees, worked examples, resolution strategies | 2 |
| 4.6 Parts 8–9 → Engineering coordination + Consultant appointment | Per-discipline filtered views; OT appointment logic narrative | 2 |
| 4.7 Parts 10–11 → DAR + Economics content | Calculator inputs, argument templates, cost curve narrative, grant databases | 2 |
| 4.8 Part 12 → Case study entries | Structured tagged entries with outcome data | 1 |
| **4.9 Functional task pages** | **30–50 task descriptions with spec links, OT framework connections** | **2 (NEW)** |
| **4.10 Legal / Governance pages** | **Disclaimer, privacy (GDPR), licensing (CC BY-SA 4.0), contributor agreement** | **1 (NEW)** |

### Phase 5: Community Infrastructure Design (Opus — 3–4 sessions)

| Task | Description |
|---|---|
| 5.1 Submission workflow design | Three submission types: lived-experience feedback, practitioner POE, jurisdiction update. Each with form schema, moderation pipeline, and publication rules. |
| 5.2 Evidence weighting protocol | How community contributions weighted vs clinical research. CRPD Art. 4.3 alignment. Co-1 tier integration. |
| 5.3 Professional review workflow | OT/architect/engineer submission validation. Credential verification. |
| 5.4 Moderation policy | Content moderation, abuse prevention, accessibility of moderation tools themselves. |
| 5.5 Privacy and consent framework | GDPR compliance, data handling for lived-experience contributors, anonymous contribution option, data subject rights. |
| **5.6 User role design** | **Four roles: lived_experience, practitioner, researcher, moderator. Permission matrices per role per entity.** |
| **5.7 AI integration specification** | **Claude API assistant: conversational specification lookup, decision engine guidance, evidence interpretation. Accuracy guardrails, liability framing, cost model.** |

### Phase 6: Build — MVP (Sonnet — 15–25 sessions)

| Task | Description | Sessions est. |
|---|---|---|
| 6.1 Project scaffolding | Next.js + Directus + PostgreSQL + Meilisearch deployed. CI/CD via GitHub Actions. | 2 |
| 6.2 Specification pages | Canonical page per spec with all related data. Server-rendered (ISR). | 3 |
| 6.3 Population and building-type hub pages | Population page: all tagged specs, co-occurrence, evidence. Building-type: applicable specs by population, conflict alerts. | 2 |
| 6.4 Functional task pages | Axis 2 entry: task → spec → population. | 1 |
| 6.5 Faceted search | Meilisearch integration. Facets: population, building type, category, functional task, evidence tier, jurisdiction, conflict status, design stage. Zero-results → gap submission. | 2 |
| 6.6 Static content pages | About, methodology, evidence hierarchy, legal, changelog. | 1 |
| 6.7 Engineering coordination pages | Per-discipline filtered views. | 1 |
| 6.8 Standards index + jurisdiction comparison | Filterable standards table; side-by-side comparison tool. | 1 |
| 6.9 Accessibility audit + remediation | axe-core 0 critical/serious; keyboard; screen reader; colour contrast; reduced motion. | 2 |

### Phase 7: Build — Decision Engine + Visualizations (Sonnet — 10–15 sessions)

| Task | Description | Sessions est. |
|---|---|---|
| 7.1 Brief Builder backend | Serverless function: population brief + building type + design tier → applicable specs + conflicts + OT assessment + DAR provisions. Unit tests per co-occurrence pair. | 2 |
| 7.2 Brief Builder frontend | 8-step UI: population selection → building type → tier → conflict dashboard → spec list → OT assessment → DAR → export (PDF + shareable URL). | 3–4 |
| 7.3 Cost Explorer | Interactive D3/Recharts chart. X: decision stage. Y: cost %. Spec toggle. Data quality visual. DAR multiplier. Outcome tooltips. | 2 |
| 7.4 Conflict matrix overview | 12-domain grid, colour + shape coded. Population-pair view. Click to expand. | 1 |
| 7.5 Co-occurrence matrix | Interactive table. Per-cell: prevalence, worked examples, conflict count. | 1 |
| 7.6 Jurisdiction comparison | Multi-select dropdown; side-by-side standards table; filterable by spec category. | 1 |

### Phase 8: Build — Community Layer (Sonnet — 8–12 sessions)

| Task | Description | Sessions est. |
|---|---|---|
| 8.1 User accounts | Email/password via Directus. Role assignment. Account settings + deletion. | 2 |
| 8.2 Lived experience feedback forms | Structured form per specification page. Population, building type, geography tags. Moderation queue. | 2 |
| 8.3 POE submission form | Case study schema. Financial data quality self-assessment. Moderation integration. | 2 |
| 8.4 Standards update form | Jurisdiction update submission. Currency flag. Moderation queue. | 1 |
| 8.5 Moderation workflow | Directus editorial pipeline. Status tracking. Approval → publication. | 2 |
| 8.6 Privacy implementation | Cookie consent (minimal — Plausible cookieless). GDPR rights. Anonymous option. | 1 |

### Phase 9: Case Study Expansion + Post-Launch (Sonnet — ongoing)

| Task | Description |
|---|---|
| 9.1 Case study pages | Full schema, linked specs, financial data with quality tiers, map if location data. |
| 9.2 Case study submission pipeline | Public form, moderation, publication. |
| 9.3 Annual standards review cycle | Jurisdiction-tracker equivalent for web. |
| 9.4 Evidence update pipeline | New BPC research → database → website. Change detection. |
| 9.5 Analytics review | Search queries with no results (gap detection); most-viewed specs; Brief Builder patterns. |
| 9.6 AI integration (if approved) | Claude API assistant on specification and decision engine pages. |

---

## 4. Parallel Work Streams

*(Unchanged from v1.)*

| Stream | Current state | Website relevance |
|---|---|---|
| BPC research pipeline | 93 files across 14 topics | Populates specification database |
| FDR scenarios | 45-scenario registry; 7 P1 granular queued | Generates new specifications |
| Connection scout | 181 connections; 98 PENDING | Populates cross-reference layer |
| Opus synthesis queue | Ongoing | Produces `bpc_synthesis` field content |
| Multilingual research | 14 languages × 24 jurisdictions | Populates jurisdiction data |
| Citation verification | Ongoing | Evidence integrity |
| Economics evidence | Bottom-up cost data; 7-country grant mapping | Populates economics engine |
| Systematic reviews | 5 deep-dive protocols | Strengthens evidence tier assignments |

---

## 5. Open Questions (decisions required before or during Phase 0)

| # | Question | Options | Impact |
|---|---|---|---|
| 1 | **Domain name** | User decision | Branding, SEO, all shared links |
| 2 | **V9 vs V10 content at launch** | Launch with V10-quality revised content only, or include V9 content with quality flags | Record count; gap visibility; editorial burden |
| 3 | **Supplementary populations (CHD/LPA/EXH/BAR)** | Include in MVP or defer? ~40 additional specifications | Schema complexity; extraction sessions |
| 4 | **Dimensioned drawings** | Create SVG/DWG detail drawings per specification for launch, or defer? | Significant content creation effort separate from platform build. If deferred, `drawing_available: false` throughout. |
| 5 | **Multilingual UI** | English-only at launch with multilingual evidence, or multilingual UI from day one? | i18n architecture decisions in Phase 3; translation effort |
| 6 | **AI integration** | Claude API assistant on specification/decision engine pages — build for launch or defer? | Cost ($), accuracy guardrails, liability language |
| 7 | **Relationship to existing guidebook** | Website replaces document, or document continues alongside? If replaces: URL redirects for §x.x citations? | Content maintenance; dual-format overhead |
| 8 | **Budget / hosting constraints** | Self-hosted VPS vs managed cloud. Monthly budget tolerance. | Stack finalization in Phase 3 |
| 9 | **Community features: MVP or post-launch?** | Launch with community submission or add post-MVP? | Moderation readiness; user accounts at launch |

---

## 6. Effort and Timeline Estimate (revised)

| Phase | Sessions | Model | Status |
|---|---|---|---|
| 0: Schema consolidation | 3–4 | Sonnet | **3/10 tasks DONE** |
| 1: Spec extraction | 8–12 | Sonnet | PENDING |
| 2: Entity extraction | 10–14 | Sonnet | **2/10 tasks DONE** |
| 3: Stack + prototype | 5–8 | Opus + Sonnet | PENDING |
| 4: Content transformation | 12–18 | Sonnet | PENDING |
| 5: Community design | 3–4 | Opus | PENDING |
| 6: Build MVP | 15–25 | Sonnet | PENDING |
| 7: Decision engine + viz | 10–15 | Sonnet | PENDING |
| 8: Community build | 8–12 | Sonnet | PENDING |
| 9: Case studies + post-launch | Ongoing | Sonnet | PENDING |
| **Total pre-launch** | **74–112** | | |

v1 estimated 61–96. The increase (+13–16 sessions) comes from: functional task entity (+4 sessions: schema + extraction + content + build), standards entity (+3 sessions), Brief Builder logic extraction (+2 sessions), engineering coordination (+2 sessions), legal/governance content (+1 session), expanded community design (+1 session), AI integration spec (+1 session).

---

## 7. Risk Register (updated)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Schema changes mid-extraction require re-extraction | MODERATE | HIGH | Phase 0 thorough review; version field in all records |
| WCAG AAA constrains interactive features | LOW | MODERATE | Component library audit in Phase 3.2; AT testing protocol |
| Community features introduce moderation burden | HIGH | MODERATE | Design moderation before build (Phase 5); consider launching without |
| Functional task taxonomy is subjective | MODERATE | MODERATE | Ground in OT frameworks (PEOP, EHP, CMOP-E); Opus review |
| Brief Builder logic errors produce wrong specifications | MODERATE | HIGH | Unit tests per co-occurrence pair; edge case testing; disclaimers |
| Evidence base still growing — content staleness | HIGH | MODERATE | Update pipeline design (Phase 5); `last_updated` per record |
| Scope creep from 9 phases | HIGH | HIGH | MVP scope defined below; defer Phases 7–8 if needed |
| Dimensioned drawings are a parallel workstream | MODERATE | LOW | Defer drawings; launch with `drawing_available: false` |
| AI integration liability | MODERATE | MODERATE | Frame as "not a substitute for professional judgment"; accuracy guardrails; defer if Q6 unresolved |

---

## 8. MVP Definition (revised)

**Tier 1 MVP** (achievable with static site + JSON — GitHub Pages intermediate step):
1. Specification Explorer — searchable, filterable
2. Population Navigator — population hubs with linked specs
3. About / Methodology pages
4. Faceted search

**Tier 2 MVP** (requires Next.js + Directus):
5. Room Configurator — building type → population → specification
6. Functional Task Navigator — Axis 2 bottom-up
7. Conflict Resolver — interactive decision trees
8. Standards index
9. Case study pages (read-only)
10. Engineering coordination pages

**Post-MVP:**
11. Brief Builder / Decision Engine (PDF export, shareable URL)
12. Cost Explorer (interactive chart)
13. Co-occurrence + Jurisdiction comparison tools
14. Community submission layers (lived experience, POE, standards updates)
15. AI integration
16. Dimensioned drawings

---

## 9. Immediate Next Actions

**This session:**
1. Commit revised workplan to `workplan/website-preparation.md` (replace v1)

**Next session:**
1. Phase 0.7 — functional task schema design (the largest gap in v1)
2. Phase 0.8 — standards schema design
3. Phase 0.9 — Brief Builder logic schema

**Decisions needed from user** (§5 above — 9 questions).
