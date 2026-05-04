# CO-0007 Workplan v4
**Created:** 2026-05-03 22:40 UTC
**Model:** Opus 4.6
**Supersedes:** workplan v3 (`workplan-co0007-v3.md`)
**Authority:** Amendment 8 (`workplan-amendment-8-audit-integrated-2026-05-03.md`) + comprehensive repository audit + website ethics IA
**Status:** ADOPTED

---

## Current position (2026-05-03)

| Stage | Status | Sessions consumed |
|---|---|---|
| Stage 0 (verification + decision freeze) | ✓ COMPLETE | 9 |
| Stage A (A1-A13 foundations) | ✓ COMPLETE | ~24 |
| Stage B1 (schema design) | ✓ COMPLETE | 9 |
| **Stage B2** | **NEXT** | 0 |

**Total sessions consumed:** ~42 of 188–253 budget.
**Remaining budget:** ~146–211 sessions.

---

## What changed from v3

**From workplan v3:** Stages 0 and A are complete. B1 is complete. The comprehensive repository audit and website ethics IA identified seven structural findings (AF-1 through AF-7) that revise B2–C scope. Stage C is reorganized from entity-type migration to website-page-type migration. Budget tightened from 220–336 to 188–253 sessions (~30-80 sessions saved).

**Key structural changes:**
- B2 expanded from 4–6 to 6–8 sessions (schema reconciliation, DesignMode rename, Appendix A migration, question heading authoring added)
- B3 expanded from 3–4 to 4–5 sessions (6 new website entity types + 14 page templates)
- B4 restructured: E-08 pipeline pilot first, then 3 full tracks (6–10 sessions, was 8–12; tightened)
- Stage C reorganized by page type, not entity type (121–177 sessions, was 165–245)
- C3 combines old C3 (parameters) + old C5 items into specification page content
- C5 is now rooms (was items+rooms)
- C6 tightened to 12 conflict domains (was speculative 200–400 entries)
- C8 tightened with Appendix A pre-migrated in B2

---

## Completed stages

### Stage 0 — Verification and decision freeze · ✓ COMPLETE · 9 sessions

All 31 audit findings mapped and resolved. Three Critical pre-decisions made:
- D-03: Co-1 operational role → pre-launch solo authorship; published corpus engagement
- T-03: Co-1 tier encoding → co-primary with Tier 1
- T-04: Sparse-evidence behavior → reduced-confidence category with rendering distinction

Outputs: `governance/pre-stage-a-decisions.md`, `governance/mission-and-epistemics.md`, `co0007-quantitative-verification.md`, contamination sampling, repo strategy decision (D-0140: same repo, same branch)

### Stage A — Foundations · ✓ COMPLETE · ~24 sessions

Thirteen governance documents committed (A1-A13). Key deliverables:
- `governance/audience-priority.md`, `governance/mission-and-epistemics.md` (A1-A2)
- `governance/conceptual-model.md` (A3)
- `governance/voice-and-framing.md`, `skills/voice-style_SKILL.md` (A4)
- `governance/co1-operational.md` (A5)
- `governance/evidence-methodology.md` (A6)
- `governance/population-taxonomy.md` (A7)
- `governance/jurisdiction-philosophy.md` (A8)
- `governance/time-model.md` (A9)
- `governance/adversarial-use-framework.md` (A10)
- `governance/legal-regulatory.md` (A11)
- `governance/decision-protocol.md` (A12)
- `governance/doctrine-recheck.md` (A13)

Python-backed infrastructure co-produced: 12 Pydantic schemas in `schemas/`, 10 validators in `scripts/`, 8 converters in `scripts/convert/`, CI pipeline (`ci.yml` with 3 jobs).

### B1 — Schema design · ✓ COMPLETE · 9 sessions

**What B1 produced that gates everything downstream:**
- D-0138 ACTIVE: SQLite storage form canonical
- D-0139 ACTIVE: 19-entity SQL DDL specification operative
- D-0140 ACTIVE: repo strategy terminal (same repo, same branch)
- `architecture/storage-decision.md`: terminal-state reference
- `architecture/schema-spec.md`: the DDL blueprint B2 implements
- `governance/migration-survival.md` §7: B1 row resolved, zero reclassifications

---

## Stage B — Architecture and pilot
**Sessions:** 24–33 (was 26–40)
**Output:** Working multi-pilot demonstrating end-to-end; static site generator rendering all 14 template types from SQLite

### B2. Schema implementation + audit remediation · 6–8 sessions

#### B2.1 Schema reconciliation and DDL amendment · 1 session · Opus

**Tasks:**
1. Read all five schema representations (spec-db JSON schema, unified website schema, SQL DDL, populations.json, conflicts.json)
2. For each of the 18 unified website schema display fields, resolve: SQL column vs JSON blob column vs computed at render time. Issue D-SCHEMA record.
3. Produce D-0139 Amendment 1: add the following to `architecture/schema-spec.md`:

**Specification table — 11 new fields:**
```
question_heading    TEXT            -- DC-6: question-mode heading (mandatory)
question_summary    TEXT            -- question-mode summary variant
summary             TEXT            -- spec-mode one-sentence summary
why_md              TEXT            -- "Why it matters" authored prose
schedule_md         TEXT            -- Schedule language (copyable)
diagram_svg         TEXT            -- Inline SVG content
diagram_type        TEXT            -- plan/section/elevation/isometric/chart
dar_relevant        INTEGER DEFAULT 0   -- DAR applicability flag
dar_note            TEXT            -- DAR rationale
conflict_domains    TEXT            -- JSON array of conflict domain IDs
structural_backing_required INTEGER DEFAULT 0
```

**JSON columns on specification (content atoms stored as JSON arrays/objects):**
```
failures_json       TEXT            -- JSON array of failure pattern strings
install_notes_json  TEXT            -- JSON array of installation note strings
detail_groups_json  TEXT            -- JSON array of {title, items[]} objects
pop_reasons_json    TEXT            -- JSON object keyed by PopulationCode
topics_json         TEXT            -- JSON array of topic strings
```

**3 new tables:**
- `measurement` — per design-mode-rename doc §2.3
- `jurisdictional_value` — per design-mode-rename doc §2.3
- `performance_criterion` — metric, target, measure per specification

4. Map the 26 website-preparation.md parsers to post-D-0138 pipeline roles (migration script vs rendering query vs redundant)
5. Produce schema reconciliation document: `architecture/schema-reconciliation.md`

**Output:** D-0139 Amendment 1; `architecture/schema-reconciliation.md`; D-SCHEMA records for 18-field resolution
**Model:** Opus (cross-cutting schema design)

#### B2.2 DesignMode rename + Part 8 numbering fix · 1.5 sessions · Sonnet

**Tasks:**
1. Rename `DesignTier` → `DesignMode` in `schemas/enums.py` (values: UNIVERSAL, POPULATION_BASED, PERSON_SPECIFIC)
2. Safe pattern-replace across all files:
   - `Universal Mode` → `Universal Mode` (safe — evidence tiers start at 1)
   - `Design Modes` → `Design Modes` (safe exact phrase)
   - `Mode P default:` / `Mode P median:` → `Mode P default:` / `Mode P median:` (safe)
   - `Mode S OT` / `Mode S handoff` → `Mode S OT` / `Mode S handoff` (safe)
3. Manual discrimination pass on `references/project-standards.md` + `skills/voice-style_SKILL.md` (~42 instances requiring judgment — mixed evidence/design tier usage)
4. Part 8 §9.x → §8.x renumbering (same find-and-replace session)
5. Update `references/website/schema/unified-data-schema.md`: `universal_value` → `universal_value`, `population_value` → `population_value`, `person_specific_note` → `person_specific_note`

**Scope:** ~200+ instances across 14 part files, 5 skill files, 10+ governance files. Part 4 (~57 instances) requires manual review because "Tier 1" is used for both evidence and design.
**Output:** All files updated; commit message: `find-and-replace: DesignMode rename + Part 8 renumbering`
**Model:** Sonnet (mechanical find-and-replace with discrimination)

#### B2.3 Appendix A → jurisdictional_value migration · 1 session · Sonnet

**Tasks:**
1. Parse `parts/v10/appendix-a-jurisdiction-comparison.md` — 20 tables, ~150-200 rows
2. For each row: extract `(spec_id, jurisdiction, standard_name, clause_reference, value_text, value_numeric, unit, is_code_minimum, evidence_tier)`
3. Map item codes (E-03, E-06, H-01, etc.) to SPEC-IDs via `references/spec-db-part4-reconciliation.md`
4. Produce migration script: `scripts/migrate/phase_jv_appendix_a.py`
5. Output: YAML records under `data/jurisdictional_values/` + migration verification report

**This single session produces the jurisdictional master index core data.** The 20 tables cover the most-compared parameters: ramp gradients, thresholds, corridors, lifts, reach ranges, LRV, hearing loops, alarms, grab bars, slip resistance, door force, rest seating, classroom acoustics, bathroom dimensions, TWSI.

**Output:** `scripts/migrate/phase_jv_appendix_a.py`; ~150-200 JV records; `/jurisdictions/master-index` MVP data
**Model:** Sonnet (structured extraction)

#### B2.4 Pydantic module authoring — 5 new modules · 2 sessions · Sonnet (Opus schema approval)

**Session 1 (Population + Conflict):**
1. `schemas/population.py` — E-11 entity. Fields: functional_profile, primary_barriers, key_parameters, conflict_domains, co_occurrence_notes, evidence_confidence, icf_codes_primary. Recursive sub-code inheritance per D-0139 §3.1.
2. `schemas/conflict.py` — E-09 entity. Fields: decision_tree, strategy_codes, governing_principle, unresolvable_residual, citations, population_a, population_b. D-0139 §3.3 base + audit-identified extensions.
3. Converters: `convert_populations.py` (from populations.json → population YAML), `convert_conflicts.py` (from conflicts.json + conflict-matrices/ → conflict YAML)
4. Validators: extend `validate_population.py`, create `validate_conflict.py`

**Session 2 (Item + FDR + specialist):**
5. `schemas/item.py` — E-08 entity per D-0139 §3.2
6. `schemas/fdr_specialist.py` — E-10 (FDR scenario) + specialist_handoff per D-0139 §3.5
7. Converters and validators for both
8. `schemas/question.py` stub — deferred to B3 per D-0139 §3.4

**Output:** 5 new Pydantic modules + converters + validators; CI extended
**Model:** Sonnet (implementation from approved schemas)

#### B2.5 Specification table field population — existing 73 records · 1 session · Sonnet

**Tasks:**
1. For the 73 existing records in `specification-database.json`, populate the 11 new fields from BPC source content:
   - `summary` — extract from BPC "Consensus finding" line
   - `question_heading` — extract from prototype ITEMS `q` field (11 items have `q` in the prototype; remaining 62 deferred to B2.7)
   - `dar_relevant` / `dar_note` — derive from Part 6 §6.10 DAR Priority Register + Part 4 HTML comments
   - `conflict_domains` — derive from `conflicts.json` specifications_involved arrays
   - `structural_backing_required` — derive from Part 8 engineering register cross-references
2. Produce: updated `specification-database.json` with new fields populated; verification report

**Output:** specification-database.json updated; field-population coverage report
**Model:** Sonnet (structured extraction from existing content)

#### B2.6 Migration tooling foundation · 1 session · Sonnet

**Tasks:**
1. Create `scripts/migrate/` directory structure per D-0139 §5.1 (13-phase outline)
2. Implement Phase 1 (slug migration) and Phase 2 (population migration) as working scripts
3. Implement Phase 3 CI gate: Co-1 completeness (all 25+ corpus entries; zero CHECK failures)
4. Implement Phase 5 CI gate: design-stage linkage verification
5. Implement Phase 8 CI gate: conflict population coverage check
6. Create `data/db/` directory with empty `guidebook.db` structure (DDL from schema-spec.md)

**Output:** `scripts/migrate/` with Phase 1-2 scripts + 3 CI gates; empty SQLite database with DDL applied
**Model:** Sonnet (tooling implementation)

#### B2.7 Question heading authoring — 91 items · 0.5 sessions · Opus

**Tasks:**
1. For each of 91 Part 4 items, author a `question_heading` — the question form of the specification title
2. Source: the prototype has 11 `q` fields already authored. Author remaining 80.
3. Quality standard: question must be answerable by yes/no from building inspection; must reference the lived experience the spec addresses; per voice-style §8.1 guidance

**Example:** E-08 "Corridor Clear Width ≥1200mm" → "Can two power wheelchairs pass each other?"

**Output:** 91 question_heading atoms added to spec-db records
**Model:** Opus (authoring — questions must be epistemically tested)

#### B2 done criteria

- [ ] D-0139 Amendment 1 applied (11 fields, 3 tables)
- [ ] Five schema representations reconciled; `architecture/schema-reconciliation.md` committed
- [ ] DesignMode rename complete across all files; zero "Universal Mode/1/2" design references remaining
- [ ] Part 8 §9.x → §8.x renumbering complete
- [ ] 5 new Pydantic modules built and CI-validated (population, item, conflict, fdr_specialist + question stub)
- [ ] Appendix A migrated to ~150-200 jurisdictional_value records
- [ ] 73 spec records updated with new fields (partial population)
- [ ] 91 question headings authored
- [ ] Migration tooling foundation: Phase 1-2 scripts + 3 CI gates + empty SQLite database
- [ ] 26 parsers mapped to post-D-0138 pipeline roles

**Revised session estimate:** 6–8 sessions. Net addition vs v3: 2 sessions for audit remediation.

---

### B3. Navigation + website entity specification · 4–5 sessions

#### B3.1 Navigation mode specification · 1 session · Opus

Per original workplan B3 scope (resolves T-02, T-05, D-01), plus:
- Define the four-door homepage entry model (architect / disabled person / OT / policymaker)
- Specify spec/question mode toggle behavior (client-side CSS class toggle, localStorage persistence)
- Specify URL routing: `/specs/[code]`, `/populations/[code]`, `/rooms/[type]/[code]`, `/conflicts/[domain]`, `/jurisdictions/[code]`, `/bibliography/[filter]`, `/foundations/[group]/[slug]`, `/engineering/[trade]`, `/economics/[topic]`, `/case-studies/[slug]`, `/throughlines/[id]`, `/specialists/[role]`, `/index`
- Specify section ordering per mode: spec mode (data-first) vs question mode (meaning-first) per IA §4.3

**Output:** `architecture/navigation-modes.md` (revised to include URL map and mode toggle spec)

#### B3.2 Website entity specification — 6 entities not in D-0139 · 2 sessions · Opus

The audit identified six entity types required by the IA that have no schema:

| Entity | URL family | Content source | Schema work |
|---|---|---|---|
| Doctrine | `/foundations/[group]/[slug]` | Prototype DOCTRINE data (10 entries) + Part 1 | Pydantic model + DDL table |
| Room | `/rooms/[type]/[code]` | Parts 6-7 + prototype ROOM_DATA | E-17 (deferred from A6) — now scoped |
| Economics entry | `/economics/[topic]` | Part 11 + `references/economics/` | Pydantic model + DDL table |
| Case study | `/case-studies/[slug]` | Part 12 (18 entries) | Pydantic model + DDL table |
| Throughline | `/throughlines/[id]` | `references/throughline-analysis.md` (17 entries) | Pydantic model + DDL table |
| Specialist consultant | `/specialists/[role]` | Part 9 (6 specialist roles) | Pydantic model + DDL table |

For each: Pydantic model, SQL DDL, converter from existing content, validator.

**Session 1:** Doctrine + Room + Specialist consultant (richest existing content)
**Session 2:** Economics entry + Case study + Throughline (thinner content; simpler schema)

Also: Question entity (E-20) per original workplan — deferred from B2 per D-0139 §3.4.

**Output:** 7 new Pydantic models (6 audit-identified + question); DDL amendments; converters; validators
**Decision:** D-SCHEMA records for each new entity

#### B3.3 Template specification · 1 session · Opus

Define the 14 page templates per IA §6.2:
- For each template: the SQLite query shape, the section sequence, the mode variants, the ethics-tested rendering rules (per IA §4)
- Spec page template with spec/question mode variants (section order changes per mode)
- Population page template with evidence-state matrix, Co-1 section, compound population notes
- Room page template with DAR section, spec sequence, interactions, clearances
- Conflict page template with decision tree, harm asymmetry, residual, compound note
- Jurisdiction page + master index template
- Bibliography page with Co-1 dedicated view
- Foundations, engineering, economics, case study, throughline, specialist templates

**Output:** `architecture/page-templates.md`

#### B3 done criteria

- [ ] Navigation modes specified including URL map and mode toggle
- [ ] 7 new entity types specified with Pydantic models and DDL
- [ ] 14 page templates defined with query shapes and rendering rules
- [ ] Question entity (E-20) specified
- [ ] Part 9 URL family (`/specialists/`) integrated into navigation spec

**Revised session estimate:** 4–5 sessions (was 3–4). Net addition: 1 session for 6 website entities.

---

### B4. Pilot construction · 6–10 sessions

#### B4.0 Pipeline pilot — E-08 Corridor Clear Width · 1 session · Sonnet

Before the three full pilot tracks, build the complete pipeline for one spec:
1. E-08 has the richest data in the prototype (5 dimensions, 2 performance criteria, 5 code references, 4 related specs, 2 population reasons, 4 failure patterns, 3 install notes, SVG diagram, schedule language)
2. Populate all SQLite tables for E-08: specification record (all fields), measurement rows, jurisdictional_value rows (from Appendix A §A.3), performance_criterion rows, connection rows, cell records for MOB and ALL populations
3. Build the static page generator for `/specs/E-08`
4. Render the spec page in both spec mode and question mode
5. Verify: every section of the IA template renders; data is correct; mode toggle works

**This is the first time a complete page renders from SQLite atoms.** All downstream pilots build on this foundation.

**Output:** Working `/specs/E-08` page from SQLite; page generator MVP
**Model:** Sonnet (implementation)

#### B4.1–B4.3 Full pilot tracks · 5–9 sessions

Per original workplan (3 tracks: adequate-evidence, contested, sparse-evidence). Revised scope:
- Each pilot track now produces a complete page from the static site generator (not just "populated schema instances")
- Each pilot renders through both spec and question modes
- Each pilot includes: population page for one relevant population, room page for the pilot room, conflict page for the relevant conflict domain
- Pilot track 1 (G-04 Bathroom): also produces `/rooms/residential/bathroom` and `/populations/MOB` and `/conflicts/ACOUSTIC-LVL`

**Output:** 3 pilot tracks rendered as static pages; page generator extended to 4 template types (spec, population, room, conflict)

**Revised session estimate:** 6–10 sessions (was 8–12; tightened with E-08 pipeline pilot).

---

### B5. Rendering layer (static site generator) · 3–4 sessions

#### B5.1 Complete static site generator · 2 sessions · Sonnet

Extend the B4 page generator to all 14 template types:
- All remaining templates beyond the 4 proven in B4 (bibliography, foundations, engineering, economics, case study, throughline, specialist, jurisdiction/master-index, index, homepage)
- Homepage with four-door entry model
- Spec/question mode toggle (client-side JavaScript: toggle `data-mode` on body, localStorage persistence)
- Schedule copy-to-clipboard (client-side JavaScript)
- Accordion/details state management (CSS/semantic HTML `<details>/<summary>`)

#### B5.2 Rendering refresh policy + verification · 1–2 sessions

Per original workplan: continuous-deploy vs periodic-snapshot vs versioned-release decision.
- Round-trip rendering verification
- Cross-navigation link verification
- Evidence-state rendering verification (stated/provisional/pending badges)
- Co-1 evidence marker rendering (distinct from clinical evidence)
- Mode toggle verification across all template types

**Output:** Complete static site generator; rendering refresh policy committed
**Model:** Sonnet (implementation; Opus for refresh policy decision)

---

### B6. Pilot validation against mission · 3–4 sessions

Per original workplan scope, plus:
- Validate each pilot page against the 9 ethics findings (F-01 through F-09 in the ethics review)
- Validate question-mode rendering against DC-6 (questions-led as first-class)
- Validate population page evidence-state matrix against DC-1 (within-population variability visible)
- Validate Co-1 evidence rendering against DC-3 (co-primary visibility)
- Validate Design Mode progression rendering against DC-4/DC-5 (floor-not-aspiration)
- Validate conflict page against harm asymmetry transparency commitment
- Validate jurisdiction master index against M-04 (systematic absence visible)

**Revised session estimate:** 3–4 sessions (was 4–5). Tightened because ethics criteria are pre-specified.

---

### B7. Architecture lock · 2 sessions

No change from original workplan. Lock decisions. Re-issue synthesis per CS4. Periodic doctrine recheck per A13.

---

### Stage B done criteria

All original criteria, plus:
- [ ] DesignMode rename complete across all files
- [ ] Part 8 section numbering corrected
- [ ] Five schema representations reconciled into one canonical form (SQLite DDL + rendering queries)
- [ ] Appendix A migrated to jurisdictional_value table
- [ ] 91 question headings authored and in spec records
- [ ] 14 page templates defined, implemented, and pilot-validated
- [ ] Static site generator renders all template types from SQLite
- [ ] E-08 full pipeline test passes (complete spec page from SQLite atoms in both modes)
- [ ] Ethics review findings (F-01–F-09) validated in pilot rendering

---

## Stage C — Content migration + website content population
**Sessions:** 121–177 (was 165–245)
**Output:** Complete project in structured form; all 14 page template types rendering from SQLite atoms

Stage C is organized by **website page type** — each page requires atoms from multiple entity types simultaneously. The prior entity-type-first organization (parameters → populations → items → conflicts) is replaced.

### C0. Skill responsibility matrix · 2–3 sessions

Unchanged from original workplan.

### C1. Migration tooling completion · 3–5 sessions

Complete the 13-phase migration tooling started in B2.6. Remaining phases:
- Phase 3: evidence_source migration (531 records from global-reference-registry.md)
- Phase 4: BPC metadata migration (78 records)
- Phase 5: specification migration (extend 73 records to full corpus)
- Phase 6: cell migration (new — evidence state per spec×population)
- Phase 7: connection migration (181 records from _index.md)
- Phase 8: conflict migration (from conflicts.json + 13 conflict-matrix files)
- Phase 9-13: remaining entity types

### C2. Skill set rebuild · 10–14 sessions

Per original workplan, minus the skills already operational from B2-B5.

Add to skill inventory:
- `question-author` — generates question headings for new specs
- `cell-curator` — populates evidence state per (spec × population) pair
- `appendix-a-parser` — extends jurisdictional value extraction to new Appendix A entries

### C3. Specification page content — migrate all 91+ items · 25–35 sessions

The primary content migration. For each Part 4 item:

1. **Extract or author all atom fields** per the 11 new specification columns:
   - `question_heading` — if not authored in B2.7, author now
   - `summary` — extract from BPC consensus finding
   - `why_md` — author from BPC best_practice_synthesis + prototype `why` field
   - `schedule_md` — extract from Part 4 if present, or author
   - `failures_json` — extract from prototype ITEMS + Part 4 failure patterns
   - `install_notes_json` — extract from prototype ITEMS
   - `detail_groups_json` — extract from prototype ITEMS
   - `pop_reasons_json` — author per-population reasoning
   - `diagram_svg` — extract from prototype ITEMS (11 items have SVGs) or author
   - `dar_relevant` / `dar_note` — derive from Part 6 §6.10 DAR register
   - `conflict_domains` — derive from conflict entity linkages

2. **Populate measurement table** — extract from BPC best_practice_synthesis sections.

3. **Populate jurisdictional_value table** — extract from BPC "Jurisdictions confirmed" + Appendix A (partially migrated in B2.3).

4. **Populate performance_criterion table** — extract from prototype ITEMS `performance[]` arrays + Part 4 content.

5. **Populate cell records** — for each (spec × population) pair: determine evidence state (stated/provisional/pending/not_applicable) per A6 §2 evidence-state machine. Curation, not extraction.

**Pending Part 4 items (from manifest):**
- Draft F-07 (Thermal Zoning), F-08 (Thermal Transition) — new specs
- Draft I-04 (Ceiling Hoist), H-05 (Nurse Call) — new specs
- Execute C-03+C-06 merger, B-03+B-04 merger, A-17→G-02 absorption
- D2-41 PAIN/OFS audit across all items
- 36 CON-HIGH entries: annotate or apply
- BIO-01–BIO-05 reformat to Part 4 template

**Session estimate:** 25–35 sessions (was 30–40 for parameters + 30–45 for items+rooms combined). Tightened: specification entity is the primary migration unit.

### C4. Population page content — 11 populations · 12–18 sessions

For each population:
1. **Migrate Part 2 prose** to `population.functional_profile`, `population.primary_barriers`, etc.
2. **Populate `population.key_parameters`** — structured per populations.json pattern
3. **Populate `population.co_occurrence_notes`** — from Part 2 prose + FDR compound files
4. **Populate `population.icf_codes_primary`** — new ICF mapping (requires web search for ICF codes per population)
5. **Co-1 evidence section** — compile Co-1 evidence sources per population
6. **Cell state completion** — verify all (spec × this population) cell records populated from C3

**Co-1 cadence note:** Pre-launch solo authorship per D-03. Published Co-1 corpus engagement only.

### C5. Room page content — 14 rooms · 15–22 sessions

For each room type (7 residential from Part 6 + 7 non-residential from Part 7):
1. **Implement E-17 Room entity** — specified in B3.2
2. **Author `room.synthesis_md`** — from prototype ROOM_DATA (richer than Parts 6-7)
3. **Author `room.sequence_json`** — design decision sequence per room
4. **Author `room.interactions[]`** — specification interactions
5. **Author `room.clearances_json`** — room-specific dimensions
6. **Author `room.failures_json`** — room-level failure patterns
7. **Author `room.diagram_svg`** — room plans
8. **Populate spec-to-room linkages** — from Parts 6-7 matrices
9. **DAR section per room** — from Part 6 §6.10 DAR Priority Register + non-residential DAR

**Critical note:** Prototype ROOM_DATA is the richest source. Migration path: prototype ROOM_DATA → room entity records in SQLite. Parts 6-7 provide spec-to-room matrices; prototype provides synthesis prose.

### C6. Conflict page content — 12 domains · 10–15 sessions

For each of the 12 non-retired conflict domains (CORRIDOR-W retired):
1. **Migrate from `conflicts.json`** (9 domains) — decision tree, strategy codes, governing principle, population pairs, resolution status, unresolvable residual
2. **Migrate from `references/conflict-matrices/` files** (13 files, 12 domains) — analytical content
3. **Cross-link to affected specifications**
4. **Compound population notes** — from FDR compound interaction files

### C7. Evidence base and bibliography · 12–17 sessions

1. Migrate 531 entries from global-reference-registry.md to evidence_source SQLite table
2. DOI verification pass — prioritize 56 COMPLETE entries, then 64 GREY entries. 395 AUTHOR-TITLE-ONLY: verify what can be verified; flag remainder with research-gap marker.
3. Co-1 source tagging — all Co-1 sources have `evidence_type = 'co1'` and six required Co-1 fields populated
4. GAP-CITE-01 resolution — 918 pending citation tags in Parts 5-12; cross-reference to REF-IDs during migration

### C8. Jurisdiction content · 6–10 sessions

1. **Complete jurisdictional_value table** — B2.3 produces ~150-200 from Appendix A. Remaining: extract from BPC files for 53 unprocessed BPC files.
2. **Jurisdiction page content** — for each of the 24 canonical jurisdictions: compile all code values, standards, and gaps.
3. **Master index rendering** — the SQL view over specification + jurisdictional_value. Three cell states (value present, no requirement, not searched) per IA §4.6.
4. **Standards registry migration** — 80 entries from `references/standards-registry.md` into structured standards entity

### C9. Cross-cutting prose + foundations content · 18–25 sessions · Opus

The largest content authoring block. All Opus-required.

**Part 1 revision:**
1. Add ICF, PEO/PEOP, Capability Approach, Kawa as four meta-theoretical framework entries
2. Expand DAR section (§1.6) from 6 lines to production depth
3. Design Mode rename applied (done in B2.2)
4. Co-1 co-primary claim explicitly surfaced in §1.5 Evidence Hierarchy

**Foundations entity content (NEW):**
5. Author doctrine entries: Social Model, Medical Model, Relational Model, Disability Justice, Universal Design, Inclusive Design, Visitability, Co-design, Cognitive Accessibility, Sensory Accessibility
6. Author framework entries: ICF, PEO/PEOP, Capability Approach, Kawa

**Part 10 (DAR) expansion:**
7. Expand from 135 lines scaffold to production depth. Visitability (§10.4) treatment needs expansion. Cost multiplier data integration with Part 11 economics.

**Part 9 integration:**
8. Map Part 9 content to `/specialists/` URL family

**Parts 5, 11, 12 content expansion:**
9. Part 5: complete §5.1-§5.3 (currently DRAFT)
10. Part 11: expand economics tables with cost-data research content
11. Part 12: deepen 18 case studies to sufficient depth or consolidate to overview page

**Throughline content:**
12. Create throughline entity records from `references/throughline-analysis.md` (17 entries — T-01 through T-11, M-01 through M-06)
13. Cross-link each throughline to relevant specs, conflicts, populations, bibliography entries

**Supplementary volume recovery:**
14. Locate and integrate CHD/LPA/EXH/BAR supplementary content (CO-0004 relocated from Part 4 Category J; file status unknown)

### C10. Quality gates and validation · 5–8 sessions

All original validators plus:
- DesignMode terminology check (zero "Universal Mode/1/2" design refs remaining)
- Question heading coverage (91/91 specs have question_heading populated)
- Cell record coverage (all spec × population pairs have cell state assigned)
- Jurisdictional value coverage (top 6 jurisdictions have values for all 91+ specs)
- Co-1 source tagging completeness (all Co-1 sources have evidence_type='co1' and 6 required fields)
- Evidence-state rendering verification (every population page shows stated/provisional/pending per spec)
- Mode toggle verification (every spec page renders correctly in both modes)
- Ethics review F-01–F-09 compliance check across all rendered pages

### C11. Maintenance lifecycle · 3–5 sessions

Unchanged from original workplan.

### Stage C done criteria

All original criteria, plus:
- [ ] All 14 page template types render from SQLite atoms
- [ ] 91+ spec pages render in both spec and question modes
- [ ] 11 population pages render with evidence-state matrices and Co-1 sections
- [ ] 14 room pages render with synthesis prose, DAR sections, and spec sequences
- [ ] 12 conflict pages render with decision trees and harm asymmetry documentation
- [ ] Master index renders with three cell states (value/gap/not-searched)
- [ ] Bibliography renders with Co-1 dedicated page
- [ ] Foundations pages render with disability models and theoretical frameworks
- [ ] Engineering pages render with correct §8.x numbering
- [ ] Economics pages render with verified cost data
- [ ] Throughline pages render with cross-linked specs and connections
- [ ] Specialist consultant pages render from Part 9 content
- [ ] DesignMode terminology used throughout — zero "Universal Mode/1/2" design refs
- [ ] Cell records populated for all spec × population pairs

---

## Cross-stage requirements

These operate continuously:

**CS1. Doctrine-recheck cadence.** Per A13. Every 25 working sessions or stage transition. LIVE from A13 close.

**CS2. Co-1 recruitment thread.** Per A5/D-03: pre-launch INOPERATIVE. Published corpus engagement only. Activates post-launch contingent on launch + resources + co-designed recruitment specification.

**CS3. Versioning continuity.** Per A9. Time model live from C1. All entities carry version metadata.

**CS4. Document re-issue cadence.** Synthesis re-issued after Stage 0 (done); after Stage A complete (done); after B7 lock.

**CS5. Co-1 representation monitoring.** Pre-launch: corpus-representation monitoring (per-population, per-domain, per-jurisdiction Co-1 source inventories with gap-flagging).

**CS6. Standards monitoring.** Per safeguards S29. Active from B7 onward.

**CS7. Salvage re-evaluation.** Per safeguards S25. At each stage transition.

**CS8. Decision capture.** Per A12. Every decision point produces written rationale. CS8 LIVE from A12 close.

**CS9. Adversarial-use review.** Per A10. Pre-public-release gate; periodic review during Stage C.

---

## Budget arithmetic

| Phase | Sessions (revised) | Status |
|---|---|---|
| Stage 0 | 9 | ✓ COMPLETE |
| Stage A (A1-A13) | 24 | ✓ COMPLETE |
| B1 | 9 | ✓ COMPLETE |
| **B2** | **6–8** | NEXT |
| **B3** | **4–5** | |
| **B4** | **6–10** | |
| **B5** | **3–4** | |
| B6 | 3–4 | |
| B7 | 2 | |
| **Stage B total** | **24–33** | |
| C0 | 2–3 | |
| C1 | 3–5 | |
| C2 | 10–14 | |
| **C3** | **25–35** | |
| **C4** | **12–18** | |
| **C5** | **15–22** | |
| **C6** | **10–15** | |
| C7 | 12–17 | |
| **C8** | **6–10** | |
| **C9** | **18–25** | |
| C10 | 5–8 | |
| C11 | 3–5 | |
| **Stage C total** | **121–177** | |
| **Project total** | **188–253** | |
| **Consumed** | **42** | |
| **Remaining** | **146–211** | |

**Budget reduction from v3:** ~30-80 sessions saved through:
- Combined parameter+item migration (C3 replaces old C3+C5-items)
- Explicit room migration (C5) scoped more tightly than old C5's "92 items + room set"
- Conflict migration (C6) scoped to 12 domains not speculative "200-400 entries"
- Jurisdiction migration (C8) tightened with Appendix A pre-migrated in B2
- B4 tightened with E-08 pipeline pilot

---

## What this workplan does NOT do

- Does not re-open D-0138, D-0139, or D-0140 decisions
- Does not amend the Stage 0 or Stage A completion status
- Does not change the Co-1 operational posture (D-03: pre-launch solo authorship)
- Does not commit to a website technology stack (Next.js + PostgreSQL + Directus + Meilisearch per website-preparation.md is a Stage C / Claude Code decision, not a B2 decision)
- Does not build the search engine, CMS, user accounts, or community features
- Does not commit to a specific launch date or launch decision
- Does not modify cross-stage threads (CS1-CS9)
- Does not re-budget clock time (per Amendment 7: re-budget when working rhythm establishes)

---

## Finding-resolution map (v3 audit findings — all resolved)

All 31 findings from audit v2 were resolved during Stage 0 and Stage A. The finding-resolution map is retained in `workplan-co0007-v3.md` for archival reference. No outstanding findings.

---

## Decision inventory (updated)

Decisions 1–20 from v3 are all RESOLVED (made during Stage 0 and A). Active and upcoming decisions:

| # | Phase | Decision | Status |
|---|---|---|---|
| 21 | B1 | Storage form → SQLite (D-0138) | ✓ RESOLVED |
| 22 | B2.1 | 18-field display resolution (D-SCHEMA records) | PENDING |
| 23 | B3.2 | 6 new entity type schemas (D-SCHEMA records) | PENDING |
| 24 | B5.2 | Rendering refresh policy | PENDING |
| — | B6 | Architecture lock vs. iterate | PENDING |
| — | C11 | Maintenance lifecycle approval | PENDING |

All decisions are captured per A12 protocol in `data/decisions/decision_register.yaml`.
