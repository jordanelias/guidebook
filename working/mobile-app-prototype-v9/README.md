# Mobile App Prototype — V9.0
**Status:** In progress · Sonnet (UI/data scaffold) · Opus required for synthesis content
**Last updated:** 2026-04-30 02:45 UTC

## What this is

Exploratory React/JSX mobile interface for the Guidebook V9.0. Designed for claude.ai artifact rendering — single .jsx file with inlined CSS, fonts via Google Fonts CDN.

Not currently part of the published Guidebook. Working artifact for evaluating how the document organises on a phone-sized screen and what new fields the dataset would need to support architect-facing use.

## Design state (v8 → v9)

Five-tab armature: **Preface · Buildings · Specs · People · Index**.

Persistent toggle bar at top of every screen: **Specifications | Questions** — same content, two reading voices.

Population codes render as inline citations (`MOB`, `VIS`, `DEAF`) styled like footnote markers. Tapping any code opens a click-citation popover with population description, count of relevant specs, and jump action to the population page. Popovers dismiss on outside-click or Escape, restore focus to the cite.

Click-citation popovers, accordion details, breadcrumb navigation, semantic landmarks, AAA contrast, ≥44px touch targets, `prefers-reduced-motion` honoured, focus-visible rings, `aria-current` / `aria-pressed` / `aria-expanded` throughout.

Single-color palette: deep ink (`#1A1612`) on warm bone (`#F2EBDD`). No saturation. Source Serif 4 / Inter / JetBrains Mono.

## v9 schema additions (this directory)

This iteration adds **architect-facing fields** to spec items and proposes **synthesis fields** for rooms. Schema in `SCHEMA.txt`.

### Spec architect-data fields (added)
- `dimensions[]` — `{ dim, value, unit, note }` precise dimensional callouts
- `performance[]` — `{ metric, target, measure }` performance criteria with measurement methods
- `codes[]` — `{ ref, clause, jurisdiction }` codes/standards (AU/US/UK/EU/INTL) with clause references
- `products[]` — manufacturer-neutral product types
- `schedule` — drop-in schedule language ready to paste
- `detail[]` — `{ title, items[] }` detail-item callouts grouped by topic
- `diagram` — `{ type, svg }` embedded SVG (plan / section / elevation / chart)
- `install[]` — installation notes
- `failures[]` — common failure patterns

### Room synthesis fields (proposed, not yet populated)
- `synthesis` — prose: how applicable specs integrate
- `sequence[]` — ordered design decisions with rationale
- `interactions[]` — where specs constrain each other
- `clearances[]` — room-specific clear-zone dimensions
- `failures[]` — room-level integration failure patterns
- `diagram` — room-level SVG with zone overlay

## What's in this directory

| File | Status |
|---|---|
| `SCHEMA.txt` | Field definitions — complete |
| `data1.js` | POPS, CATEGORIES, TIERS, TOPICS — complete |
| `data2.js` | 11 ITEMS with full architect data including SVG diagrams — complete |

The 11 specs cover every category and both Tier 0 and Tier 1: E-08, G-04, A-02, B-04, C-04, E-01, B-10, D-04, A-16, E-10, H-01.

## What's missing

1. **Room synthesis content** — `synthesis`, `sequence`, `interactions` fields require best-practice synthesis writing. Per Standing Rule 6, this is Opus work, not Sonnet. Priority rooms: R-BA, R-KIT, R-BED, R-LIV, NR-EDU, NR-HLT, NR-WRK (densest spec interactions).
2. **Schema TOC entry** — these field additions to spec and room records are structural. Standing Rule 7 requires `toc-editor` Change Order before merging into the active dataset.
3. **Components for new architect fields** — DimTable, PerfTable, CodesByJurisdiction, ScheduleBlock with copy button, DetailAccordion, SvgDiagram, ClearancesTable, FailurePatterns, SynthesisSection.
4. **SpecDetail rebuild** — to render all new fields in order: header → summary → body → why → dimensions table → performance table → codes by jurisdiction → products list → schedule copy block → detail accordions → diagram → install → failures → populations → where applies → related → evidence accordion → topics.
5. **RoomDetail rebuild** — leads with synthesis prose, then sequence, then interactions, then specs by category, then clearances, then failures, then diagram. Must gracefully handle missing synthesis fields until Opus populates them.
6. **Single-file assembly** — combine into one .jsx at the project working artifact location for claude.ai rendering.

## Architecture preserved from v8

- 430px shell, bone background, ink text
- Persistent ToggleBar with `role="radiogroup"` at top of shell
- Bottom nav: Preface, Buildings, Specs, People, Index
- Cite popover with `role="dialog"`, ESC dismiss, click-outside dismiss, focus restoration
- Accordion with `aria-expanded`
- All ≥44px touch targets, focus-visible 2px ink rings
- `aria-pressed` / `aria-current` / `aria-expanded` throughout
- `prefers-reduced-motion` honoured

## Provenance

Designed across multiple sessions exploring the brief: bone background, no pastels, gender-neutral typography, declarative spec titles, master index with multi-axis filters, persistent question/spec mode toggle, click-citation popovers, architect-facing data, room synthesis. See chat history for design rationale.
