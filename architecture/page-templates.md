# Page Template Specifications
**Created:** 2026-05-04
**Depends on:** navigation-modes.md, d0139-amendment-1.md, d0139-amendment-2.md
**Decision:** D-TMPL-001 through D-TMPL-014
**Status:** ACTIVE

---

## Overview

Each template defines: the primary query (SQLite), the section sequence with field mappings, rendering components, mode variants (if any), and ethics constraints. Templates are numbered to match navigation-modes.md §4.

Field references use `table.column` notation. Components are reusable UI elements shared across templates.

---

## Shared Components

### C-01: Evidence Marker Badge
Renders `evidence_state_record.state` as: ● stated (green) · ◐ provisional (amber) · ○ pending (grey). No "strong/weak" language (D-NAV-009).

### C-02: Population Badge Set
Renders population codes as coloured badges. Primary populations full-opacity; secondary dimmed. No ranking by count (D-NAV-006).

### C-03: Jurisdiction Cell
Three states: green (value present) · red (no requirement) · grey (not searched). Neutral colour semantics (D-NAV-010).

### C-04: Item Code Link
Renders `[A-K]-NN` as a clickable link to `/specs/[item_code]`. Shows item title on hover.

### C-05: Conflict Domain Card
Compact card showing conflict_label, population parties (A vs B), resolution status badge. Links to `/conflicts/[domain]`.

### C-06: Co-1 Badge
Dedicated badge for Co-1 (co-primary/lived experience) evidence. Always visible when present; never subordinated to academic evidence (D-NAV-011).

### C-07: Curation Status Indicator
Footer element showing `specification.curation_status`: automated · reviewed · opus_synthesized. Informational only.

### C-08: Mode Toggle
Renders in page header. Active on specification pages; inert elsewhere. Controls `<body>` class (`mode-spec` / `mode-question`).

### C-09: DAR Flag
Renders `specification.dar_relevant` as a flag icon with `dar_note` tooltip. Links to `/dar-register`.

---

## Template 1: Specification Page

**URL:** `/specs/[item_code]` or `/specs/[item_code]/[parameter]`
**Mode variants:** Yes (spec mode / question mode)
**Entity:** specification + measurement + jurisdictional_value + joins

### Primary query

```sql
SELECT s.*,
       GROUP_CONCAT(DISTINCT sp.population_code || ':' || sp.role) AS pop_roles
FROM specification s
LEFT JOIN specification_population sp ON s.spec_id = sp.spec_id
WHERE s.item_code = :item_code
GROUP BY s.spec_id;
```

### Supporting queries

```sql
-- Measurements (universal → population → person-specific)
SELECT m.* FROM measurement m
WHERE m.spec_id = :spec_id
ORDER BY CASE m.design_mode
  WHEN 'universal' THEN 1
  WHEN 'population_based' THEN 2
  WHEN 'person_specific' THEN 3 END,
  m.population_code;

-- Jurisdictional values
SELECT jv.*, j.label AS jurisdiction_label
FROM jurisdictional_value jv
LEFT JOIN jurisdiction j ON jv.jurisdiction = j.code
WHERE jv.spec_id = :spec_id
ORDER BY jv.jurisdiction;

-- Performance criteria
SELECT * FROM performance_criterion WHERE spec_id = :spec_id;
```

### Section sequence

| Order (spec) | Order (question) | Section | Fields | Component |
|---|---|---|---|---|
| 1 | — | Title bar | `s.title`, `s.item_code`, `s.parameter` | C-01 badge |
| — | 1 | Question heading | `s.question_heading` | Large accessible heading |
| — | 2 | Why it matters | `s.why_md` | Prose block |
| 2 | 3 | Value block | `measurement.*` grouped by design_mode | Three-row table (Universal / Mode P / Mode S) |
| 3 | 4 | Evidence summary | `s.evidence_summary`, `s.evidence_tier` | C-01, C-06 |
| 4 | 5 | Population applicability | `specification_population` join | C-02 badges (primary/secondary) |
| 5 | 6 | Jurisdiction matrix | `jurisdictional_value` rows | C-03 cells in grid |
| 6 | 7 | Conflict domains | `s.conflict_domains` JSON | C-05 cards |
| 7 | 8 | DAR note | `s.dar_relevant`, `s.dar_note` | C-09 flag + prose |
| 8 | 9 | Engineering | `s.structural_backing_required` | Flag + Part 8 link |
| 9 | 10 | Schedule language | `s.schedule_md` | Copyable text block |
| 10 | — | Why it matters | `s.why_md` | Prose block (end position in spec mode) |
| 11 | 11 | Cross-references | `connection_endpoint` join | C-04 links |
| 12 | 12 | Diagram | `s.diagram_svg`, `s.diagram_type` | Inline SVG |
| 13 | 13 | Metadata footer | `s.curation_status`, `s.modified_at` | C-07 |

### Rendering rules
- Value block: Universal row always visible. Mode P row shows range + median with unit_display formatting. Mode S row shows `person_specific_note` text. If no measurement exists for a mode, row is omitted (not shown as empty).
- Mode S framed as "resolves to the person's own needs" not "requires specialist" (D-NAV-012).
- Jurisdiction matrix: max 14 columns visible; horizontal scroll for more. Sort by ISO code.

---

## Template 2: Population Page

**URL:** `/populations/[code]`
**Mode variants:** No
**Entity:** population + specification_population + conflict joins

### Primary query

```sql
SELECT p.* FROM population p WHERE p.code = :code;
```

### Supporting queries

```sql
-- Specifications for this population
SELECT s.item_code, s.title, s.parameter, sp.role
FROM specification_population sp
JOIN specification s ON sp.spec_id = s.spec_id
WHERE sp.population_code = :code
ORDER BY sp.role DESC, s.item_code;

-- Conflicts involving this population
SELECT DISTINCT c.* FROM conflict c
WHERE c.conflict_id IN (
  SELECT conflict_id FROM conflict
  WHERE JSON_EXTRACT(population_a, '$.codes') LIKE '%' || :code || '%'
     OR JSON_EXTRACT(population_b, '$.codes') LIKE '%' || :code || '%'
);
```

### Section sequence

| Order | Section | Fields | Component |
|---|---|---|---|
| 1 | Header | `p.label`, `p.code` | Population icon + label |
| 2 | Functional profile | `p.functional_profile` | Prose block |
| 3 | Primary barriers | `p.primary_barriers` | Tag list |
| 4 | Specification matrix | `specification_population` join | Table: primary highlighted, secondary dimmed |
| 5 | Co-1 evidence | `p.co1_status`, `p.co1_gap_note` | C-06 + status text |
| 6 | Conflict involvement | Conflict join results | C-05 cards |
| 7 | Co-occurrence | `p.co_occurrence_notes` | Prose block |
| 8 | Evidence confidence | `p.evidence_confidence` | Badge (HIGH/MODERATE/LOW) |
| 9 | BPC sources | `p.bpc_slugs` | Link list |

### Rendering rules
- No ranking of populations anywhere (D-NAV-006). Population page never compares this population to others by specification count.
- Functional profile uses capacity language (D-NAV-007).

---

## Template 3: Room Page

**URL:** `/rooms/[type]/[code]`
**Mode variants:** No
**Entity:** room + room_item + room_dar_provision + room_conflict

### Primary query

```sql
SELECT r.* FROM room r WHERE r.room_id = :code AND r.building_type = :type;
```

### Supporting queries

```sql
SELECT ri.*, rip.population_code, rip.applicability
FROM room_item ri
LEFT JOIN room_item_population rip ON ri.room_id = rip.room_id AND ri.item_code = rip.item_code
WHERE ri.room_id = :code
ORDER BY ri.item_code;

SELECT * FROM room_dar_provision WHERE room_id = :code;
SELECT * FROM room_conflict WHERE room_id = :code;
```

### Section sequence

| Order | Section | Fields |
|---|---|---|
| 1 | Header | `r.room_label`, `r.building_type`, `r.evidence_density` |
| 2 | Criticality note | `r.criticality_note` |
| 3 | Item matrix | `room_item` + `room_item_population` — grid: items × populations |
| 4 | DAR provisions | `room_dar_provision` rows |
| 5 | Conflict register | `room_conflict` rows with resolution |
| 6 | Schematic checklist | `r.schematic_checklist` — checkbox list for design review |
| 7 | Design stage sequence | Grouped by `ri.design_stage` (SD → DD → CD → RFO) |

---

## Template 4: Conflict Page

**URL:** `/conflicts/[domain]`
**Mode variants:** No
**Entity:** conflict + parties + resolution + citations

### Primary query

```sql
SELECT c.* FROM conflict c WHERE c.conflict_id = :domain;
```

### Section sequence

| Order | Section | Fields | Component |
|---|---|---|---|
| 1 | Header | `c.conflict_label`, `c.domain` | — |
| 2 | Population A | `c.population_a.codes`, `c.population_a.specification` | C-02 badges |
| 3 | Population B | `c.population_b.codes`, `c.population_b.specification` | C-02 badges |
| 4 | Decision tree | `c.decision_tree` | Interactive collapsible tree |
| 5 | Governing principle | `c.governing_principle` | Callout block |
| 6 | Resolution | `c.resolution.strategy_codes`, `c.resolution.description` | Strategy badges + prose |
| 7 | Unresolvable residual | `c.unresolvable_residual` (if MODE-S-ONLY) | Warning block |
| 8 | Mode S trigger | `c.mode_s_trigger`, `c.mitigation` | Trigger + mitigation prose |
| 9 | Specifications | `c.specifications_involved` | C-04 links |
| 10 | Citations | `c.citations` | Reference list |

### Rendering rules
- Parties displayed with equal visual weight (D-NAV-008). No visual hierarchy between A and B. Side-by-side layout on desktop; stacked equally on mobile.

---

## Template 5: Jurisdiction Page

**URL:** `/jurisdictions/[code]`
**Mode variants:** No

### Primary query

```sql
SELECT jv.*, s.item_code, s.title, s.parameter
FROM jurisdictional_value jv
JOIN specification s ON jv.spec_id = s.spec_id
WHERE jv.jurisdiction = :code
ORDER BY s.item_code;
```

### Section sequence

| Order | Section |
|---|---|
| 1 | Jurisdiction name + ISO code + flag |
| 2 | Standards referenced (grouped by `jv.standard_name`) |
| 3 | Value table: item_code, parameter, jurisdiction value, guidebook value, comparison indicator |

---

## Template 6: Master Index

**URL:** `/index`
**Mode variants:** No

### Primary query

```sql
SELECT s.item_code, s.parameter, s.title, s.evidence_tier,
       COUNT(DISTINCT sp.population_code) AS pop_count,
       COUNT(DISTINCT jv.jurisdiction) AS jur_count,
       s.dar_relevant
FROM specification s
LEFT JOIN specification_population sp ON s.spec_id = sp.spec_id
LEFT JOIN jurisdictional_value jv ON s.spec_id = jv.spec_id
WHERE s.status = 'active'
GROUP BY s.spec_id
ORDER BY s.item_code;
```

### Rendering
Full-width sortable table. Column headers clickable for sort. Category filter (A–K tabs). Search box filters by title/parameter.

---

## Template 7: Bibliography Page

**URL:** `/bibliography/[ref_id]`
**Mode variants:** No

### Section sequence

| Order | Section |
|---|---|
| 1 | Source metadata (authors, year, title, journal, DOI link) |
| 2 | Evidence tier badge |
| 3 | Co-1 badge (if co-primary) — always above academic tier (D-NAV-011) |
| 4 | Specifications citing this source (C-04 links) |
| 5 | Language of source |

---

## Template 8: Doctrine Page

**URL:** `/foundations/[group]/[slug]`
**Mode variants:** No

### Primary query

```sql
SELECT d.* FROM doctrine d WHERE d.slug = :slug;

SELECT ds.item_code FROM doctrine_specification ds
WHERE ds.doctrine_id = :doctrine_id;
```

### Section sequence

| Order | Section |
|---|---|
| 1 | Title + group badge (core/evidence/ethics/frameworks) |
| 2 | Statement (authoritative prose) |
| 3 | Implications for practice |
| 4 | Related specifications (C-04 links) |
| 5 | Part section reference |

---

## Template 9: Engineering Trade Page

**URL:** `/engineering/[trade]`
**Mode variants:** No

### Section sequence

| Order | Section |
|---|---|
| 1 | Trade name (Acoustic / Electrical / Mechanical / Structural) |
| 2 | Engineering coordination register items for this trade |
| 3 | Brief template (copyable text block) |
| 4 | Stage-gated coordination protocol: SD gate → DD gate → CD gate → RFO gate |

### Data source
Part 8 content (§8.1 register, §8.2 briefs, §8.3 protocol). Served as static markdown rendered to HTML. No dedicated SQL table; content from `parts/v10/part08.md` sections.

---

## Template 10: Economics Topic Page

**URL:** `/economics/[topic]`
**Mode variants:** No

### Primary query

```sql
SELECT * FROM economics_entry
WHERE pillar = :pillar
ORDER BY evidence_tier, year DESC;
```

### Section sequence

| Order | Section |
|---|---|
| 1 | Topic label + pillar badge (health/inaction/construction/market) |
| 2 | Key findings table (source, jurisdiction, finding, BCR if available) |
| 3 | Study design details (expandable per entry) |
| 4 | Specification links (which items have cost data) |

---

## Template 11: Case Study Page

**URL:** `/case-studies/[slug]`
**Mode variants:** No

### Primary query

```sql
SELECT cs.* FROM case_study cs WHERE cs.slug = :slug;

SELECT csp.population_code FROM case_study_population csp
WHERE csp.case_study_id = :id;

SELECT css.item_code FROM case_study_specification css
WHERE css.case_study_id = :id;
```

### Section sequence

| Order | Section |
|---|---|
| 1 | Title + location + year + architect |
| 2 | Building type + setting |
| 3 | Primary populations (C-02 badges) |
| 4 | Design strategies (prose + C-04 spec links) |
| 5 | Verified outcomes (metric, value, source, tier badge) |
| 6 | Cost data (with quality badge: VERIFIED/PROVISIONAL/GREY) |
| 7 | Limitations |

---

## Template 12: Throughline Page

**URL:** `/throughlines/[id]`
**Mode variants:** No

### Primary query

```sql
SELECT t.* FROM throughline t WHERE t.throughline_id = :id;

SELECT ts.item_code, ts.description
FROM throughline_specification ts
WHERE ts.throughline_id = :id;
```

### Section sequence

| Order | Section |
|---|---|
| 1 | Throughline ID + title |
| 2 | Description (what pattern this captures) |
| 3 | Evidence instances (specification × description table) |
| 4 | Implications for practice |

---

## Template 13: Specialist Page

**URL:** `/specialists/[role]`
**Mode variants:** No

### Primary query

```sql
SELECT sp.* FROM specialist sp WHERE sp.role = :role;

SELECT st.trigger_text FROM specialist_trigger st
WHERE st.specialist_id = :id;

SELECT ss.stage, ss.scope_text FROM specialist_stage_scope ss
WHERE ss.specialist_id = :id ORDER BY
  CASE ss.stage WHEN 'SD' THEN 1 WHEN 'DD' THEN 2 WHEN 'CD' THEN 3 WHEN 'RFO' THEN 4 END;

SELECT ssp.item_code FROM specialist_specification ssp
WHERE ssp.specialist_id = :id;
```

### Section sequence

| Order | Section |
|---|---|
| 1 | Role label + role description |
| 2 | Appointment triggers (checklist) |
| 3 | Scope by design stage (SD → DD → CD → RFO table) |
| 4 | Specifications requiring this specialist (C-04 links) |
| 5 | Assessment report format (copyable template) |
| 6 | Co-design / CRPD 4.3 notes (if applicable) |
| 7 | Guidebook relationship |

---

## Template 14: Homepage

**URL:** `/`
**Mode variants:** No

### Section sequence

| Order | Section | Content |
|---|---|---|
| 1 | Four-door entry | Cards per navigation-modes.md §1 |
| 2 | Key statistics | `SELECT COUNT(*) FROM specification WHERE status='active'`, population count, jurisdiction count |
| 3 | Recent updates | `SELECT * FROM specification ORDER BY modified_at DESC LIMIT 5` |
| 4 | Quick search | Search input targeting `/search` |

---

## Decision Records

| ID | Decision | Category |
|---|---|---|
| D-TMPL-001 | Specification page dual-mode rendering via CSS order | DG-REVIEW |
| D-TMPL-002 | Value block omits empty design modes (no empty rows) | DG-AUTO |
| D-TMPL-003 | Population page no cross-population comparison | DG-MANDATORY |
| D-TMPL-004 | Conflict page equal-weight party display | DG-MANDATORY |
| D-TMPL-005 | Jurisdiction matrix max 14 visible columns | DG-AUTO |
| D-TMPL-006 | Master index sortable + filterable by category | DG-AUTO |
| D-TMPL-007 | Bibliography Co-1 badge above academic tier | DG-MANDATORY |
| D-TMPL-008 | Engineering pages served as rendered markdown | DG-AUTO |
| D-TMPL-009 | Economics four-pillar dashboard structure | DG-REVIEW |
| D-TMPL-010 | Case study cost quality badges (VERIFIED/PROVISIONAL/GREY) | DG-AUTO |
| D-TMPL-011 | Throughline instances as specification × description table | DG-AUTO |
| D-TMPL-012 | Specialist scope by design stage table | DG-AUTO |
| D-TMPL-013 | Homepage four-door cards with statistics | DG-REVIEW |
| D-TMPL-014 | Shared component library (C-01 through C-09) | DG-REVIEW |

---

## Change Log

| Date | Change |
|---|---|
| 2026-05-04 | Document created. 14 templates + 9 shared components + 14 D-TMPL decisions. |
