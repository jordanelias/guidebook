# Navigation Modes — Website Architecture
**Created:** 2026-05-04
**Decision:** D-NAV-001 through D-NAV-014
**Status:** ACTIVE
**Governs:** URL routing, page template selection, mode toggle, homepage entry model

---

## 1. Homepage Entry Model — Four Doors

The homepage presents four entry points, each addressing a distinct user mental model. No door is privileged; all reach the same content through different navigation paths.

| Door | Label | Entry URL | Lands on | Mental model |
|---|---|---|---|---|
| 1 | **Design professional** | `/specs` | Specification Explorer (spec mode) | "Show me the number and the evidence" |
| 2 | **Disabled person / advocate** | `/questions` | Specification Explorer (question mode) | "Does this building work for me?" |
| 3 | **OT / allied health** | `/populations` | Population Navigator | "What does my client's population need?" |
| 4 | **Policymaker / procurer** | `/economics` | Economics Dashboard | "What does this cost and what does it save?" |

Each door sets a `mode` cookie/localStorage value that persists the user's preferred rendering until explicitly changed.

---

## 2. Navigation Modes — Spec vs Question

The guidebook renders the same specification data in two modes. Mode affects section ordering and heading language on specification pages only. All other page types render identically in both modes.

### 2.1 Spec mode (default for Door 1)

Section order on specification page: parameter → value → evidence → populations → conflicts → DAR → engineering → schedule → why it matters.

Heading language uses technical parameter names: "Corridor clear width", "Grab bar diameter".

### 2.2 Question mode (default for Door 2)

Section order on specification page: question heading → why it matters → value → evidence → populations → conflicts → DAR → engineering → schedule.

Heading language uses the question_heading field: "Can two power wheelchairs pass in this corridor?"

### 2.3 Toggle behavior

The mode toggle is a client-side CSS class on `<body>`: `mode-spec` or `mode-question`. Both section sequences exist in the DOM; CSS `order` properties control display sequence. No server round-trip required.

Persistence: `localStorage.setItem('guidebook-mode', 'spec' | 'question')`. Read on page load; default to `spec` if unset.

The toggle control appears in the page header on all pages. On non-specification pages it is visible but inert (greyed with tooltip: "Mode affects specification pages").

---

## 3. URL Routing Map

All URLs are defined here. No URL may be added without amending this document.

### 3.1 Primary entity routes

| URL pattern | Page template | Entity source | Notes |
|---|---|---|---|
| `/` | Homepage | Static | Four-door entry |
| `/specs` | Spec Explorer (list) | specification table | Filterable grid; default sort by category |
| `/specs/[item_code]` | Spec Page | specification + measurement + joins | Canonical spec URL; mode-sensitive |
| `/specs/[item_code]/[parameter]` | Spec Page (anchored) | Same | Deep-link to specific parameter within item |
| `/questions` | Question Explorer (list) | specification table (question_heading) | Same data as /specs, question-mode default |
| `/populations` | Population Navigator (list) | population table | Card grid by population code |
| `/populations/[code]` | Population Page | population + specification_population join | e.g. `/populations/MOB` |
| `/rooms` | Room Navigator (list) | room table | Split: residential / non-residential |
| `/rooms/[type]/[code]` | Room Page | room + item_matrix joins | e.g. `/rooms/residential/R-ENT` |
| `/conflicts` | Conflict Navigator (list) | conflict table | Card grid by domain |
| `/conflicts/[domain]` | Conflict Page | conflict + parties + resolution | e.g. `/conflicts/ACOUSTIC-LVL` |
| `/jurisdictions` | Master Index | jurisdictional_value table | Three-state matrix (green/red/grey) |
| `/jurisdictions/[code]` | Jurisdiction Page | jurisdictional_value filtered | e.g. `/jurisdictions/AU` |
| `/bibliography` | Bibliography (list) | evidence_source table | Filterable; Co-1 dedicated view |
| `/bibliography/[ref_id]` | Source Page | evidence_source record | Individual source detail |

### 3.2 Secondary entity routes

| URL pattern | Page template | Entity source | Notes |
|---|---|---|---|
| `/foundations` | Foundations index | doctrine table | Grouped by doctrine group |
| `/foundations/[group]/[slug]` | Doctrine Page | doctrine record | e.g. `/foundations/core/design-modes` |
| `/engineering` | Engineering index | Part 8 content | Grouped by trade |
| `/engineering/[trade]` | Engineering Trade Page | Part 8 section | e.g. `/engineering/acoustic` |
| `/economics` | Economics Dashboard | economics table | Four-pillar structure |
| `/economics/[topic]` | Economics Topic Page | economics record | e.g. `/economics/construction-cost` |
| `/case-studies` | Case Study index | case_study table | Card grid |
| `/case-studies/[slug]` | Case Study Page | case_study record | e.g. `/case-studies/south-tyrol-care-home` |
| `/throughlines` | Throughline index | throughline table | 17 entries |
| `/throughlines/[id]` | Throughline Page | throughline record | e.g. `/throughlines/T-01` |
| `/specialists` | Specialist index | specialist table | 6 roles |
| `/specialists/[role]` | Specialist Page | specialist record | e.g. `/specialists/OT` |
| `/index` | Master Specification Index | specification table | Full table view, all fields |

### 3.3 Utility routes

| URL pattern | Purpose |
|---|---|
| `/search` | Full-text search across all entities |
| `/about` | Project information, methodology, team |
| `/glossary` | Term definitions (ICF codes, population codes, evidence tiers) |
| `/changelog` | Version history per specification |
| `/dar-register` | DAR Priority Register (linked from spec pages) |

---

## 4. Page Templates — 14 Types

Each template defines the section sequence, the primary query, and the mode variant (if any).

### Template 1: Specification Page

The most complex template. Two rendering variants (spec mode / question mode).

**Primary query:**
```sql
SELECT s.*, m.*, jv.jurisdiction, jv.value_text
FROM specification s
LEFT JOIN measurement m ON s.spec_id = m.spec_id
LEFT JOIN jurisdictional_value jv ON s.spec_id = jv.spec_id
WHERE s.item_code = ?
ORDER BY m.design_mode, jv.jurisdiction;
```

**Spec mode sections (order):**
1. Title + parameter label + evidence marker
2. Value block (universal → population → person-specific, with unit display)
3. Evidence summary + full citation list
4. Population applicability (primary / secondary badges)
5. Jurisdiction matrix (green/red/grey cells)
6. Conflict domains (linked cards)
7. DAR note (if dar_relevant)
8. Engineering coordination (if structural_backing_required)
9. Schedule language (copyable text block)
10. "Why it matters" prose
11. Cross-references (linked item codes)
12. Diagram (if diagram_svg present)
13. Metadata footer (curation_status, last_updated)

**Question mode sections (order):**
1. Question heading (large, accessible)
2. "Why it matters" prose
3. Value block (same rendering)
4–13. Same as spec mode §3–12

### Template 2: Population Page

**Primary query:**
```sql
SELECT p.*, sp.spec_id, sp.role, s.item_code, s.title
FROM population p
JOIN specification_population sp ON p.code = sp.population_code
JOIN specification s ON sp.spec_id = s.spec_id
WHERE p.code = ?
ORDER BY sp.role, s.item_code;
```

**Sections:**
1. Population label + functional profile
2. Primary barriers (bullet list)
3. Specification matrix (primary specs highlighted, secondary dimmed)
4. Co-1 evidence section (if co1_status not null)
5. Conflict involvement (linked conflict cards)
6. Co-occurrence notes
7. Evidence confidence badge
8. BPC source links

### Template 3: Room Page

**Sections:**
1. Room label + building type + criticality note
2. Item matrix (population × item grid with applicability indicators)
3. DAR provisions for this room
4. Interactions and clearances
5. Room-specific conflict notes
6. Design stage sequence (SD → DD → CD → RFO)

### Template 4: Conflict Page

**Sections:**
1. Conflict label + domain
2. Population parties (A vs B, with specification summaries)
3. Decision tree (interactive, collapsible)
4. Governing principle
5. Resolution strategy (with strategy code badges)
6. Unresolvable residual (if MODE-S-ONLY)
7. Mode S trigger and mitigation
8. Specifications involved (linked)
9. Citations

### Template 5: Jurisdiction Page

**Sections:**
1. Jurisdiction name + ISO code
2. Standards list (with clause references)
3. Specification values from this jurisdiction (table)
4. Comparison with guidebook values (above/below/equal indicators)

### Template 6: Master Index

Full specification table with sortable columns: item_code, parameter, value, evidence_tier, population_count, jurisdiction_count, dar_relevant. Filterable by category (A–K).

### Template 7: Bibliography Page

**Sections:**
1. Source metadata (authors, year, journal, DOI)
2. Evidence tier assignment
3. Specifications citing this source (linked)
4. Co-1 badge (if co-primary evidence)
5. Language of source

### Template 8: Doctrine Page

**Sections:**
1. Doctrine title + group
2. Statement (authoritative prose from Part 1)
3. Implications for practice
4. Related specifications
5. Version history

### Template 9: Engineering Trade Page

**Sections:**
1. Trade name (Acoustic / Electrical / Mechanical / Structural)
2. Engineering coordination register items for this trade
3. Brief templates (copyable)
4. Stage-gated coordination protocol checkpoints

### Template 10: Economics Topic Page

**Sections:**
1. Topic label + pillar assignment
2. Key findings (structured data from economics.json)
3. Source citations with study design
4. Specification links (which specs have cost data)

### Template 11: Case Study Page

**Sections:**
1. Project name + location + building type
2. Narrative summary
3. Specifications demonstrated (linked)
4. Outcomes / lessons learned
5. Images (if available)

### Template 12: Throughline Page

**Sections:**
1. Throughline ID + title
2. Description (what pattern this throughline captures)
3. Evidence instances across specifications
4. Implications for practice

### Template 13: Specialist Page

**Sections:**
1. Role title (OT, Dementia Design Specialist, etc.)
2. Scope of services by design stage
3. Appointment triggers (from Part 9)
4. Specifications requiring this specialist (linked)
5. Assessment report format guidance
6. Co-design and CRPD Article 4.3 notes (for OT)

### Template 14: Homepage

**Sections:**
1. Four-door entry cards (§1 of this document)
2. Key statistics (specification count, population count, jurisdiction count)
3. Recent updates
4. Quick search

---

## 5. Cross-Cutting Navigation Elements

### 5.1 Global navigation bar

Persistent across all pages: Specs | Populations | Rooms | Conflicts | Jurisdictions | Bibliography | More (dropdown: Foundations, Engineering, Economics, Case Studies, Throughlines, Specialists)

### 5.2 Breadcrumbs

Format: `Home > [Section] > [Entity]`. Example: `Home > Specifications > E-08 Corridor Clear Width`.

### 5.3 Related content sidebar

On entity pages, a sidebar shows: related specifications (by connection register), conflict involvement, population applicability. Collapsed by default on mobile.

### 5.4 Search

Full-text search across all entity types. Results grouped by entity type with type badges. Search indexes: specification titles + parameters + question headings, population labels + functional profiles, room labels, conflict labels, throughline titles.

---

## 6. Ethics-Tested Rendering Rules

Per the unified-data-schema ethics review, the following rendering constraints apply to all templates.

1. **No ranking by disability.** Population pages never sort populations by specification count, evidence confidence, or any metric that implies a hierarchy of disability.
2. **No deficit framing.** Population functional profiles use capacity language ("uses powered wheelchair") not deficit language ("confined to wheelchair").
3. **Conflict pages show both parties equally.** No visual hierarchy between population_a and population_b. The governing principle appears after both parties, not as a verdict.
4. **Evidence markers are descriptive, not evaluative.** ● = stated evidence, ◐ = provisional evidence, ○ = pending review. No "strong/weak" language.
5. **Jurisdiction matrix uses neutral colours.** Green = value present, red = no requirement, grey = not searched. No implication that "red" jurisdictions are inferior.
6. **Co-1 evidence gets dedicated visibility.** Co-primary (lived experience) evidence is never subordinated to academic evidence in display order.
7. **Person-specific mode (Mode S) is an expansion, not a fallback.** Language frames Mode S as "resolves to the person's own needs" not "requires specialist intervention."

---

## 7. Decision Records

| ID | Decision | Category | Delegation |
|---|---|---|---|
| D-NAV-001 | Four-door homepage entry model | D-NAV | DG-REVIEW |
| D-NAV-002 | Spec/question mode as CSS toggle, not server-side | D-NAV | DG-AUTO |
| D-NAV-003 | localStorage persistence for mode preference | D-NAV | DG-AUTO |
| D-NAV-004 | URL routing map as defined in §3 | D-NAV | DG-REVIEW |
| D-NAV-005 | 14 page templates as defined in §4 | D-NAV | DG-REVIEW |
| D-NAV-006 | No ranking by disability (ethics rule 1) | D-NAV | DG-MANDATORY |
| D-NAV-007 | No deficit framing (ethics rule 2) | D-NAV | DG-MANDATORY |
| D-NAV-008 | Conflict parties displayed equally (ethics rule 3) | D-NAV | DG-MANDATORY |
| D-NAV-009 | Evidence markers descriptive only (ethics rule 4) | D-NAV | DG-MANDATORY |
| D-NAV-010 | Jurisdiction matrix neutral colours (ethics rule 5) | D-NAV | DG-MANDATORY |
| D-NAV-011 | Co-1 evidence dedicated visibility (ethics rule 6) | D-NAV | DG-MANDATORY |
| D-NAV-012 | Mode S framed as expansion (ethics rule 7) | D-NAV | DG-MANDATORY |
| D-NAV-013 | Specialist entity routes at /specialists/ | D-NAV | DG-AUTO |
| D-NAV-014 | Question mode section reordering (why-first) | D-NAV | DG-REVIEW |

---

## Change Log

| Date | Change |
|---|---|
| 2026-05-04 | Document created. D-NAV-001 through D-NAV-014 issued. |
