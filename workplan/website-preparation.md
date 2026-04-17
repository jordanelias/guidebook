# Workplan: Research Processing → Website Build
**Created:** 2026-04-17
**Sources:** Website-preparation v2 (comprehensive) + Build guide (April 11) + Ecosystem guide (Valoria)
**Staging:** All Claude.ai research processing completes before Claude Code begins.
**Status:** DRAFT — requires user review
**Decisions recorded:** 2026-04-17 — all BPC migration, all connections, CI yes, cancel JSON extraction

---

## 1. Staging Logic

Three documents govern this workplan:

- **Website-preparation v2** defines what the website contains: 8 entity types, 5 interactive tools, 20 page types, 3 community layers, 4 navigation axes. It specifies the data schema and content architecture.
- **Build guide** defines how it gets built: Claude Code + Next.js + PostgreSQL + Directus + Meilisearch + Vercel. 26 parsers read guidebook source files and write to database.
- **Ecosystem guide** defines enforcement patterns. In this workplan, enforcement maps to: PostgreSQL constraints (data), CI (website repo), and lightweight CI (guidebook repo).

**Two phases, one transition:**

```
PHASE A: CLAUDE.AI (guidebook repo)                      23–35 sessions
  Complete research processing →
  Fill data gaps for all 26 parsers →
  Stabilise source files →
  Guidebook repo CI →
  Gap register split

      ↓ transition: parser readiness audit passes

PHASE B: CLAUDE CODE (website repo)                       build guide S1 →
  Project scaffold → database schema → parsers →
  frontend → interactive tools → community
```

---

## 2. Parser Readiness Audit

The build guide defines 26 parsers. The v2 workplan adds source requirements for 4 new entities (functional tasks, standards, Brief Builder logic, engineering coordination). Here is every parser, its source, and the current readiness of that source.

### Tier 1 — Reference entities (no dependencies)

| Parser | Source | Exists? | Ready? | Gap |
|---|---|---|---|---|
| p01_standards | `references/standards-registry.md` (15KB) | ✓ | Needs format audit | YAML block standardisation |
| p14_glossary | `versions/current/Guidebook...v9-0...md` (glossary section) | ✓ | Needs format audit | Term/definition pair boundaries |
| p17_sensory_zones | Manual (3 records) | N/A | ✓ | Hardcoded in parser |
| p18_categories | `parts/v10/part04.md` category headers | ✓ | ✓ | 10 categories present |
| p07_resolution_strategies | `parts/v10/part03.md` §3.9 | ✓ | Needs audit | 9 strategies, formatting consistency |

### Tier 2 — Core entities

| Parser | Source | Exists? | Ready? | Gap |
|---|---|---|---|---|
| p08_populations | `parts/v10/part02.md` + BPC population files (14) | ✓ | Partial | Part 2 profiles exist; populations.json (11 records) validates. Format audit needed. |
| p11_sources | `references/bibliography-v9.md` + BPC Key sources | ✓ | **Major gap** | ~70 BPC files need Key sources migration to CO-0006 REF-ID table. **Largest Phase A task.** |
| p12_dar | `parts/v10/part10.md` §10.1 | ✓ | Likely | Table format audit |
| p19_grant_programmes | Part 11 + `references/cost-data/` (3 files) + `references/economics/` (3 files) | ✓ | Partial | Part 11 has grant data in prose; cleaner structure = fewer parser errors |

### Tier 3 — Complex entities

| Parser | Source | Exists? | Ready? | Gap |
|---|---|---|---|---|
| p09_specifications | `parts/v10/part04.md` (92 items, 86 with specs, 6 stubs) | ✓ | **Partial** | 6 stubs need completion. Spec DB (73 records from 21 slugs) needs reconciliation with Part 4. **v2 adds fields:** `design_stage_lock`, `engineering_disciplines`, `functional_tasks`, `ve_risk`, `ot_appointment_trigger`, `drawing_available` — some require enrichment of Part 4 items or cross-referencing Part 8/9 data. |
| p04_conflicts | Part 5 (39KB) + `references/conflict-matrices/` (13 files) + SYNTHESIS.md | ✓ | Good | conflicts.json (14 records) validates source. |
| p02_case_studies | `references/case-study-compendium.md` (57KB) | ✓ | Likely | Format audit |
| p10_building_types | `parts/v10/part06.md` + `part07.md` | ✓ | Partial | Some room types are scaffolds → `status: SCAFFOLD` |
| p20_functional_tasks | **Semi-manual** (Part 3 §3.5–3.12 + Part 4 descriptions + OT frameworks) | ✓ (Part 3: 42KB) | **NEW in v2** | Claude Code proposes tasks from source material. No structured extraction source exists — but Part 3 and Part 4 content is sufficient for Claude Code to derive. **No Claude.ai pre-work needed beyond ensuring Part 3 content is stable.** |

### v2 additions — new parsers needed

| Parser | Source | Exists? | Ready? | Gap |
|---|---|---|---|---|
| p_standards_ext | `references/standards-registry.md` + BPC jurisdiction data across search-log files | ✓ | Partial | Standards registry has 29 entries. v2 targets 100–150. Remaining standards exist in BPC jurisdiction coverage sections but aren't consolidated. **Phase A task: audit standards-registry completeness against BPC jurisdiction data.** |
| p_engineering | `parts/v10/part08.md` (48KB) §8.1 register table | ✓ | Likely | Existing Part 8 content maps specs to disciplines and design stages. Format audit needed. |
| p_brief_logic | `parts/v10/part03.md` §3.8 + `part05.md` + `part09.md` §9.2.2 | ✓ | Needs extraction design | Decision tree structure exists in prose. OT appointment triggers in Part 9. Claude Code can extract — but the logic needs to be verified as correct before parsing. **Phase A task: validate Part 3 §3.8 decision tree and Part 9 §9.2.2 OT trigger logic are complete and internally consistent.** |

### Tier 4 — Dependent entities

| Parser | Source | Ready? | Gap |
|---|---|---|---|
| p06_co_occurrence | `parts/v10/part03.md` §3.3 | Likely | Table format audit |
| p05_connections | `references/connections/_index.md` + per-topic files | ✓ | 181 connections, well-structured |
| p03_gaps | `gap_register.md` | **Needs split** | Split active/archive before parsing |
| p13_engineering | `parts/v10/part08.md` §8.1 | Likely | Register table format audit |
| p15_worked_examples | `parts/v10/part03.md` §3.11 + `part05.md` §5.4 | Needs audit | Narrative boundary detection |
| p16_project_rules | `references/project-standards.md` | ✓ | RULE block format consistent |

### Tier 5 — Join tables

| Parser | Depends on | Gap |
|---|---|---|
| p22_spec_populations | p09 (Applicable Groups line) | — |
| p23_spec_building_types | p10 (Parts 6–7 matrices) | — |
| p24_spec_conflicts | p04, p09 (Part 5 §5.2 table) | — |
| p25_spec_sources | p09, p11 (Key citations + BPC Key sources) | **Depends on A1 citation migration** |
| p26_spec_standards | p01, BPC jurisdiction data | — |
| p21_spec_functional_tasks | p09, p20 | Manual curation in Claude Code |

---

## 3. Gap Analysis

### Category A: Must complete (parser blockers)

| # | Gap | Description | Sessions | Priority |
|---|---|---|---|---|
| A1 | **BPC Key sources migration** | ~70 BPC files: flat Key sources → CO-0006 REF-ID table. p11 and p25 depend on consistent citation structure. **Decision: all files.** | 6–8 | P1 |
| A2 | **Spec DB ↔ Part 4 reconciliation** | 73-record spec DB (parameter-level, 21 slugs) vs 92 Part 4 items. Reconciliation report for Claude Code Session D. | 2–3 | P1 |
| A3 | **Gap register split** | Active/archive. Parser p03 should read active only. | 0.5 | P1 |
| A4 | **6 stub item specs** | Complete or mark as explicit stubs with rationale. | 1–2 | P2 |
| A5 | **Standards registry completeness** | v2 targets 100–150 standards. Current: 29. Audit BPC jurisdiction_coverage sections to identify standards referenced but not in registry. Consolidate. | 1–2 | P2 |
| A6 | **Brief Builder logic validation** | Part 3 §3.8 decision tree + Part 9 §9.2.2 OT triggers: verify completeness, internal consistency, and that all population combinations produce valid outputs. | 1 | P2 |
| A7 | **v2 spec field enrichment** | Part 4 items need: `design_stage_lock` (from Part 8 cross-ref), `ve_risk` (from Part 8 §8.3.3), `ot_appointment_trigger` (from Part 9 §9.2.2). Annotate Part 4 items with this data so parsers can extract it. | 2–3 | P1 |

### Category B: Should complete (data quality)

| # | Gap | Description | Sessions | Priority |
|---|---|---|---|---|
| B1 | **96 PENDING connections — all** | Each consumed connection enriches item specs with cross-references. **Decision: all 96.** Opus-assigned (connection-scout). Consumption via ISW at effort 125. | 12–18 | P2 |
| B2 | **12 Tier 3 SRs pending BPC integration** (GAP-078) | Strongest: Rashid 2025, Quesada-Cubo 2025, Simpson 2025. | 3–4 | P2 |
| B3 | **GRADE confidence ratings** (GAP-079) | Framework designed, not applied to ~125 items. Without these, `evidence_tier: null` on parsed specs. | 3–4 | P2 |
| B4 | **Evidence density statements** (GAP-080) | Drafted for all 12 Parts. Voice-style pass then insertion. | 1 | P3 |
| B5 | **Remaining BPC audit** | 20 of 60 files unaudited for hallucinations. | 2–3 | P2 |

### Category C: Ecosystem hardening

| # | Gap | Description | Sessions | Priority |
|---|---|---|---|---|
| C1 | **Guidebook repo CI** | Syntax check (JSON/YAML parseable), register sizes, commit message format. Protects parser source files. **Decision: yes.** | 1 | P2 |
| C2 | **Session archive** | 133 session files → archive pre-April. | 0.5 | P3 |
| C3 | **Source format standardisation** | Fix formatting issues found during Block 1 audit. | 2 | P2 |

---

## 4. Phase A Schedule (Claude.ai)

All Phase A work runs in Claude.ai because it depends on the existing guidebook project ecosystem: the skill set (research-log-manager, connection-scout, item-specification-writer, evidence-auditor, multilingual-research), the session protocol, the GitHub-backed state management, and the Opus model routing for connection consumption and evidence synthesis. These tools and workflows do not exist in the Claude Code environment.

### Block 1: Cleanup + Audit (1–2 sessions)

| Task | Description |
|---|---|
| A3 | Split gap register active/archive |
| C2 | Archive old session files |
| Source format audit | Read every parser source file listed in §2. Document formatting patterns, edge cases, known issues for each. Produce **parser source readiness report** covering: standards-registry, glossary, Part 2, Part 3 (§3.3, §3.5–3.12, §3.8, §3.9, §3.11), Part 4, Part 5, Part 8 (§8.1, §8.3.3), Part 9 (§9.2.2), Part 10 (§10.1), Part 12, bibliography-v9. |
| A5 (audit only) | During source format audit: count standards referenced in BPC jurisdiction_coverage sections that aren't in standards-registry.md. Quantify the gap (29 current → target 100–150). |
| A6 | During Part 3/Part 9 audit: validate decision tree completeness and OT trigger logic. Flag any population combinations that produce no output or contradictory output. |

### Block 2: Citation Infrastructure (6–8 sessions)

| Task | Description |
|---|---|
| A1 | BPC Key sources migration. All ~70 files. Batch by topic directory (~5–8 files per session). Restructure flat Key sources lists → CO-0006 REF-ID table (REF-ID, Short-key, Authors, Year, Title, Journal/Publisher, DOI/URL, Tier, Lang, Jurisdictions). |

### Block 3: Specification Completeness (5–8 sessions)

| Task | Description |
|---|---|
| A4 | Complete 6 stub item specs in Part 4. |
| A7 | Enrich Part 4 items with v2 fields: annotate each item with `design_stage_lock` (from Part 8 design stage register), `ve_risk` (from Part 8 §8.3.3 VE Protection Register), `ot_appointment_trigger` (from Part 9 §9.2.2). Format as parseable annotations (HTML comments or structured field blocks within each item). |
| A2 | Reconcile spec DB (73 records) against Part 4 (92 items). Produce reconciliation report: items without BPC coverage, spec DB records without Part 4 mapping, field-level discrepancies. Document for Claude Code Session D. |
| A5 (execution) | Consolidate BPC jurisdiction standards into standards-registry.md. Add missing entries with jurisdiction, version, status, source_url. Target: registry contains every standard referenced anywhere in BPC files. |
| B3 (partial) | Apply GRADE-equivalent confidence ratings to highest-priority items (Categories A, E, G). Partial coverage acceptable — unrated specs get `evidence_tier: null`. |

### Block 4: Evidence Quality + Connection Consumption (12–18 sessions)

| Task | Description |
|---|---|
| B1 | Consume all 96 PENDING connections. Opus connection-scout sessions to write cross-references into Part 4 items and connection register. Alternating with Block 2 sessions (different file targets — parallelisable). |
| B5 | Complete BPC hallucination audit (remaining ~20 files). |
| B2 | Integrate highest-priority Tier 3 SRs into BPC files: Rashid 2025 (NDV), Quesada-Cubo 2025 (IntD housing), Simpson 2025 (school acoustics/autism). |
| B4 | Evidence density statements: voice-style pass, insert at Part openings. |

### Block 5: Ecosystem Hardening (1–2 sessions)

| Task | Description |
|---|---|
| C1 | Guidebook repo CI: `.github/workflows/ci.yml` with syntax-check + register-size thresholds + commit message format. Enable branch protection after green. |
| C3 | Fix formatting issues found in Block 1 audit. |
| Final readiness audit | Re-run parser source readiness report. Confirm every source file in §2 is parser-ready. Verify transition criteria (§5). |

---

## 5. Transition Criteria (Phase A → Phase B)

Claude Code begins (build guide S1) when:

1. **A1 complete:** ≥90% of BPC files have CO-0006 Key sources tables.
2. **A2 complete:** Spec DB ↔ Part 4 reconciliation report exists.
3. **A3 complete:** Gap register split into active/archive.
4. **A4 complete:** All 92 Part 4 items have quantified specs (no stubs).
5. **A5 complete:** Standards registry contains ≥80% of standards referenced in BPC files.
6. **A6 complete:** Part 3 §3.8 decision tree and Part 9 §9.2.2 OT triggers validated.
7. **A7 complete:** Part 4 items annotated with design_stage_lock, ve_risk, ot_appointment_trigger.
8. **Parser readiness audit passes:** Every source file documented with formatting patterns and edge cases.
9. **No P1 OPEN gaps that block parser source quality.**

10. **B1 complete:** All 96 PENDING connections consumed.
11. **B2 complete:** Priority Tier 3 SRs integrated into BPC files.
12. **B3 complete:** GRADE confidence ratings applied to priority categories (A, E, G).
13. **B5 complete:** BPC hallucination audit complete (all 60 files).

All Phase A work — Category A, B, and C — must complete before Phase B begins. No early-start exceptions. Blocks 2 and 4 run in parallel with each other (different file targets), but both must finish before transition.

---

## 6. Phase B: Claude Code Build

Phase B follows the build guide sequentially. The v2 workplan's Phases 3–8 map to the build guide as follows:

| v2 Phase | Build guide section | Sessions | Notes |
|---|---|---|---|
| 3: Stack + prototype | S1–S5, Phase 1.1–1.2 | 3–5 | Stack confirmed (Next.js + PostgreSQL + Directus + Meilisearch). Schema → PostgreSQL DDL. Directus connection. |
| 1+2: Data extraction | Phase 1.3–1.7 | 8–15 | 26 parsers. Tiered. Cross-entity validation (§1.7). **Parsers read from guidebook repo; data quality reflects Phase A work.** |
| — | Phase 1.8 | 0.5 | Meilisearch sync. |
| 6: Build MVP | Phase 2.0–2.6 | 15–25 | Design system → base layout → spec pages → all page types → explorer → search → accessibility audit. **v2 additions:** functional task pages, engineering coordination pages, standards index. |
| 7: Decision engine + viz | Phase 3.1–3.6 | 10–15 | Brief Builder backend + frontend, Cost Explorer, conflict/co-occurrence/jurisdiction tools. |
| 8: Community | Phase 4.1–4.4 | 8–12 | User accounts, feedback forms, moderation, privacy. |

### v2 entities mapped to build guide parsers

The build guide's parser list needs 4 additions for v2 entities:

| New parser | Source | Build guide phase | Notes |
|---|---|---|---|
| p_functional_tasks | Part 3 §3.5–3.12 + Part 4 descriptions + OT frameworks | Phase 1.5 (Tier 3) | Semi-manual. Claude Code proposes ~30–50 tasks, user reviews. |
| p_standards_ext | standards-registry.md + BPC jurisdiction sections | Phase 1.4 (Tier 2) | After Phase A enriches the registry. |
| p_engineering | Part 8 §8.1 register table | Phase 1.5 (Tier 3) | Maps specs → disciplines → design stages. |
| p_brief_logic | Part 3 §3.8 + Part 5 + Part 9 §9.2.2 | Phase 1.5 (Tier 3) | Decision tree nodes + OT trigger conditions. After Phase A validates the logic. |

### v2 page types mapped to build guide phases

| v2 page type | Build guide phase | Notes |
|---|---|---|
| Functional task pages (`/tasks/[slug]`) | Phase 2.3 Session D | New — task → spec → population (Axis 2) |
| Engineering coordination (`/engineering/[discipline]`) | Phase 2.5 | In build guide |
| Standards index + jurisdiction comparison (`/standards`) | Phase 2.5 | In build guide; v2 expands to side-by-side comparison tool |
| Brief Builder (`/brief-builder`) | Phase 3.1–3.2 | In build guide; v2 specifies 8-step flow |
| Co-occurrence matrix | Phase 3.5 | In build guide |
| Jurisdiction comparison tool | Phase 3.5 | In build guide; v2 specifies multi-select side-by-side |
| Legal/governance pages | Phase 2.5 | v2 adds: disclaimer, privacy, licensing, contributor agreement |
| Changelog (`/changelog`) | Phase 2.5 | v2 adds: auto-generated from database version history |

---

## 7. Enforcement Architecture

### Guidebook repo (Phase A — Claude.ai)

| Mechanism | What it enforces | Source pattern |
|---|---|---|
| Lightweight CI (Block 5, C1) | JSON/YAML syntax, register sizes, commit message format | Ecosystem guide §5 (adapted — no hooks.py, just CI) |
| Existing session protocol | Session LATEST, YAML logs, consolidator reconciliation | Current ecosystem (unchanged) |
| Existing skill ecosystem | Research-log-manager CHECK/LOG, connection-scout, ISW | Current ecosystem (unchanged) |

### Website repo (Phase B — Claude Code)

| Mechanism | What it enforces | Source pattern |
|---|---|---|
| PostgreSQL constraints (CHECK, FK, NOT NULL, ENUM) | Data validity at insert time | Ecosystem guide "code enforces, prose suggests" |
| Parser test suites + §1.7 cross-entity validation | Referential integrity across all entities | Ecosystem guide §11 (propagation tracking) |
| CI: axe-core + Lighthouse + type checking + unit tests | Accessibility, performance, code quality | Build guide §2.6 + ecosystem guide §5 (external ground truth) |
| Git pre-commit hooks | Commit message format, linting | Ecosystem guide §8 (commit protocol) |
| Database version history | Change tracking, changelog generation | v2 requirement |

The ecosystem guide's `hooks.py` / bootstrap / session token / token threshold patterns are **not implemented**. They solve Claude.ai container-reset and context-window problems that don't exist in the Claude Code development model. Enforcement comes from the database schema (structural validity), test suites (relational integrity), and CI (accessibility + quality).

---

## 8. Session Estimates

### Phase A (Claude.ai)

| Block | Sessions | Model | Dependency |
|---|---|---|---|
| Block 1: Cleanup + audit | 1–2 | Sonnet | Start immediately |
| Block 2: Citation migration | 6–8 | Sonnet | After Block 1 scopes the work |
| Block 3: Spec completeness | 5–8 | Sonnet + Opus (B3) | After Block 1 |
| Block 4: Evidence + connections | 12–18 | Opus (connections) + Sonnet | Parallel with Block 2 |
| Block 5: Ecosystem hardening | 1–2 | Sonnet | After Blocks 2–4 |
| **Phase A total** | **25–38** | | |

### Phase B (Claude Code)

| Phase | Sessions | Source |
|---|---|---|
| Setup + scaffold | 2–3 | Build guide S1–S5 |
| Database + parsers | 8–15 | Build guide Phase 1 |
| Frontend MVP | 15–25 | Build guide Phase 2 + v2 additions |
| Decision engine + viz | 10–15 | Build guide Phase 3 + v2 tools |
| Community | 8–12 | Build guide Phase 4 |
| **Phase B total** | **43–70** | |

**Combined total: 68–108 sessions.** v2 estimated 74–112 for the equivalent scope. The difference: Phase A subsumes v2 Phases 0–2 (schema + extraction are now handled by parsers, not Claude.ai JSON extraction). Phase B is more efficient because parsers replace manual extraction.

---

## 9. v2 Open Questions (decisions still needed)

| # | Question | Options | When needed |
|---|---|---|---|
| 1 | Domain name | User decision | Before Phase B (Vercel custom domain) |
| 2 | V9 vs V10 content at launch | V10-quality only, or V9 with quality flags | Before Phase B parsers (determines source files) |
| 3 | Supplementary populations (CHD/LPA/EXH/BAR) | Include in MVP (~40 additional specs) or defer | Before Phase B Phase 1.5 |
| 4 | Dimensioned drawings | Create SVG/DWG per spec or defer (`drawing_available: false`) | Before Phase B Phase 2 |
| 5 | Multilingual UI | English only at launch (multilingual evidence preserved) or multilingual UI | Before Phase B Phase 2 (i18n architecture) |
| 6 | AI integration | Claude API assistant on spec/decision engine pages — build or defer | Before Phase B Phase 7 |
| 7 | Website replaces or supplements document | URL redirects for §x.x citations? | Before Phase B launch |
| 8 | Budget / hosting | Self-hosted VPS vs managed cloud. Monthly budget tolerance. | Before Phase B S1 |
| 9 | Community features: MVP or post-launch | Launch with submission forms or add later | Before Phase B Phase 8 |

---

## 10. Cancelled Work

| Item | Reason |
|---|---|
| v1 website-preparation.md Phases 0.3, 0.5, 0.6 (room types, case studies, economics JSON extraction) | Parsers read markdown source, not JSON. JSON extraction is redundant. |
| Ecosystem workplan `hooks.py` / bootstrap / session tokens for website repo | Claude Code doesn't have container-reset or context-window problems. Database constraints + CI replace these. |
| Ecosystem workplan two-repo data promotion pipeline | Parsers read directly from guidebook repo clone. No repo-to-repo JSON promotion needed. |
| v1 website-preparation.md Phase 1 (spec extraction batches 2–5 to JSON) | Parsers handle extraction from BPC files → database. No intermediate JSON step. |
