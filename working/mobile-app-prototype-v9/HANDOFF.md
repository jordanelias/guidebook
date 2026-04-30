# Handoff Workplan — Mobile App Prototype V9.0
**Created:** 2026-04-30 02:45 UTC
**Reason for handoff:** Out of context window. Resuming in fresh session.
**Last commit:** `7ce9852` — schema + architect-data for 11 specs
**Branch:** main

## What this is

The Guidebook V9.0 mobile-app prototype is a single-file React/JSX artifact for claude.ai that lets users navigate the Guidebook's populations, specifications, rooms, and master index on a phone-sized canvas. It exists as exploratory UX work — not a published deliverable. Each session has refined it: bone palette, gender-neutral typography, declarative spec titles, persistent question/spec mode toggle, click-citation popovers, master index with multi-axis filters, and now (this iteration) architect-facing data on each spec and a proposed room-synthesis schema.

The previous session got partway through v9: 11 specs received full architect data including dimensions, performance metrics, codes by jurisdiction, products, schedule language, detail items, embedded SVG diagrams, install notes, and failure patterns. The room-level synthesis was scoped but not written, and the React components to render the new fields were not yet built.

## Current state

Files in repo at `working/mobile-app-prototype-v9/`:

| File | Lines | Status |
|---|---|---|
| `README.md` | ~95 | Complete — describes design, schema, what's done, what's pending |
| `SCHEMA.txt` | 52 | Complete — field definitions for spec architect-data and room synthesis |
| `data1.js` | 46 | Complete — POPS (10), CATEGORIES (9), TIERS (3), TOPICS (11) |
| `data2.js` | 1393 | Complete for 11 specs — needs 4–10 more for visual coverage of categories |

The 11 specs covered: A-02 (Acoustic Ceiling), A-16 (Sensory Room), B-04 (Flicker-Free LED), B-10 (Visual Fire Alarm), C-04 (LRV Contrast), D-04 (Landmarks), E-01 (Accessible Lift), E-08 (Corridor Width), E-10 (Rest Seating), G-04 (Wet-Room Bathroom), H-01 (Controls Reach).

The previous session also built and committed v8 in earlier iterations (chat history, not in repo). v9 is the schema upgrade pass; the working v8 .jsx code is recoverable from chat transcript at `/mnt/transcripts/2026-04-30-02-38-27-guidebook-mobile-app-iterations.txt`.

## What's pending — in execution order

### Phase 1 — Sonnet, this session or next

**1.1 Decide whether more specs need architect data before assembly.** Current 11 cover all 9 categories and both Tier 0 and Tier 1. For an MVP demonstrating the schema, 11 is sufficient. For visual density when browsing categories, more would help. Recommend: ship MVP with 11 first, add specs incrementally.

**1.2 Build new components.** All to be added to the v9 single-file artifact. Components needed:

- `DimTable({ rows })` — renders dimensions[] as a table with columns Dim · Value · Unit · Note
- `PerfTable({ rows })` — renders performance[] as Metric · Target · Measurement
- `CodesByJurisdiction({ rows })` — groups codes by jurisdiction (AU/US/UK/EU/INTL) into collapsible sections, each row showing Reference · Clause
- `ProductsList({ items })` — bulleted manufacturer-neutral product list
- `ScheduleBlock({ text })` — monospace block with copy-to-clipboard button (handle clipboard API failure gracefully — fallback to selection)
- `DetailAccordion({ groups })` — accordion of detail[] entries, each `{ title, items[] }`
- `SvgDiagram({ svg, type })` — renders the inline SVG markup safely (use `dangerouslySetInnerHTML` since SVG is authored, not user input). Include type label (plan/section/elevation/chart) and `role="img"` with `aria-label` already in the SVG itself.
- `InstallList({ items })` — numbered installation notes
- `FailurePatterns({ items })` — bulleted failure patterns, with prefix marker

For room synthesis (Phase 2 dependency, build skeletons now):
- `SynthesisSection({ prose })` — renders synthesis prose as serif body
- `SequenceList({ steps })` — ordered list with step number + focus + why
- `InteractionsList({ items })` — list of `{ specs[], note }` showing which specs constrain each other
- `ClearancesTable({ rows })` — same shape as DimTable
- `RoomFailures({ items })` — same as FailurePatterns but room-level

All components must:
- Honour `prefers-reduced-motion`
- Touch targets ≥44px
- Focus-visible 2px ink rings
- Match the existing palette (deep ink #1A1612 on bone #F2EBDD)
- Be keyboard navigable
- Use semantic HTML (table for tables, ol/ul for lists, etc.)

**1.3 Rebuild SpecDetail page.** Section order on every spec detail:

1. Crumb back to specs list + spec code
2. Header: category, full title (or question per mode), tier tag with description, counterpart in alt-form quoted box
3. **Summary** — short prose (existing `s` field)
4. **Specification in detail** — long prose (existing `body` field)
5. **Why it matters** — rationale (existing `why` field)
6. **Dimensions** — DimTable
7. **Performance criteria** — PerfTable
8. **Codes and standards** — CodesByJurisdiction
9. **Product types** — ProductsList
10. **Schedule language** — ScheduleBlock with copy
11. **Detail items** — DetailAccordion
12. **Diagram** — SvgDiagram
13. **Installation notes** — InstallList
14. **Common failures** — FailurePatterns
15. **Relevant populations** — existing list with per-population reasons
16. **Where it applies** — existing rooms-by-building grouping
17. **Related entries** — existing related list with rationale
18. **Evidence and references** — existing accordion
19. **Topics** — existing inline list

Sections render only if data present (graceful empty state for specs without architect data yet).

**1.4 Rebuild RoomDetail page.** Section order:

1. Crumb back to Buildings → building type → room name
2. Header: room name + short note
3. **Character prose** (existing room body)
4. **Design synthesis** — SynthesisSection (Phase 2 content; show "Synthesis pending Opus session" placeholder if missing)
5. **Sequence of design decisions** — SequenceList (same fallback)
6. **Critical interactions** — InteractionsList (same fallback)
7. **Stats panel** — total entries, T0 count, T1 count
8. **Critical entries callout** — Tier 0 specs that apply
9. **All entries by category** — existing inline-expandable rows
10. **Clearances** — ClearancesTable
11. **Common failures** — RoomFailures
12. **Diagram** — SvgDiagram

**1.5 Single-file assembly.** Combine into one .jsx at `/mnt/user-data/outputs/guidebook-app.jsx`. Use the v8 architecture as the base (preserves persistent toggle, master index, click-citation popovers, breadcrumbs, accordions). Verify in claude.ai artifact viewer.

**1.6 Present file via `present_files`.**

**Estimated effort:** Phase 1 is ~50k tokens of focused work. Likely 1–2 sessions depending on whether more specs are added.

### Phase 2 — Opus, separate session

**2.1 Room synthesis content** for priority rooms in this order (highest spec-interaction density first):

- **R-BA (Bathroom)** — densest integration: G-04 wet-room falls + G-03 grab bar backing + I-03 anti-scald + E-07 slip resistance + B-12 night lighting + B-10 visual alarm. Show how falls, drain, grab-bar backing, and waterproofing all coordinate in a single wall buildup before lining.
- **R-KIT (Kitchen)** — F-05 seated-task + I-02 one-handed + H-01 reach + B-04 flicker-free under cabinets + E-07 slip + C-04 contrast at controls.
- **NR-EDU (Education)** — A-02 ceiling + A-08 HVAC quiet + A-11 perimeter loop + A-13 no masking + B-03/B-04 lighting + D-02 simplicity + D-05 retreat + A-16 sensory room. Heavy acoustic + sensory integration.
- **NR-HLT (Healthcare)** — A-01 buffers + D-01 loop plan + D-03 toilet visibility + E-01 lift + G-04 bathroom + extensive overlap. The most multi-population room type.
- **R-BED (Bedroom)** — sleep-environment integration: A-08 + A-09 + A-14 + B-01 + B-11 + B-12 + H-02 + G-09. Circadian + acoustic + thermal control.
- **R-LIV, NR-WRK** — secondary priority.

Each room's `synthesis` field needs:
- 2–4 paragraphs of prose explaining how the applicable specs combine into a coherent design move (not a list — a discussion of integration)
- `sequence[]`: 4–8 ordered design decisions with rationale ("Set out floor falls before substrate" ahead of "Coordinate grab-bar backing with framing" ahead of...)
- `interactions[]`: 3–6 entries identifying where one spec's resolution constrains another (e.g., "G-04 waterproofing depth requires coordination with G-03 grab-bar backing — both behind the same wall before lining")
- `clearances[]`: room-specific clear zones tabulated
- `failures[]`: 4–8 patterns where rooms typically fail to integrate
- `diagram`: room-level SVG showing zone overlay

This is best-practice synthesis content. Per Standing Rule 6, requires Opus model. BPC entries should record `opus_synthesis: true`.

**2.2 Schema TOC entry.** Per Standing Rule 7, the new spec and room schema fields are structural changes. Submit Change Order to `toc-editor` listing the additions:

Spec record additions: `dimensions[]`, `performance[]`, `codes[]`, `products[]`, `schedule`, `detail[]`, `diagram`, `install[]`, `failures[]`.
Room record additions: `synthesis`, `sequence[]`, `interactions[]`, `clearances[]`, `failures[]`, `diagram`.

Once TOC entry approved, the schema can migrate from prototype-only (working/) into the active dataset.

### Phase 3 — Integration, future session

**3.1** Once Opus has populated room synthesis, reassemble the single-file artifact with synthesis content rendering in RoomDetail.

**3.2** Add remaining specs incrementally as architect data is authored. The schema accommodates partial population — sections render only when data is present.

**3.3** Consider whether the prototype's components and data structure should inform the published Guidebook deliverable (PDF/print) or remain a digital companion.

## Risks and constraints

- **Standing Rule 1** (never process >500 lines as single input): `data2.js` at 1393 lines is over threshold. When resuming, view in ranged chunks (e.g. lines 1–400, 401–800, 801–1200, 1200–end) rather than full read.
- **Standing Rule 6**: Sonnet must not write the room synthesis prose. Flag for Opus.
- **Standing Rule 7**: schema migration to active dataset requires Change Order via toc-editor first.
- **Persistence layer** (`<persistence_mitigation>` in user prefs): when assembling single-file artifact, send pre-flight first ("about to produce ~3000-line .jsx, OK to proceed?"), checkpoint inline at each section boundary, reference output location in next turn.
- **Token budget**: a single-file .jsx with 11 specs (each ~120 lines of architect data + SVG) plus components, plus rooms, lands at ~2500–3500 lines. Generation is heavy. Consider whether to split into multiple files at the project level, accepting the artifact-rendering tradeoff.

## How to resume

A fresh session should:

1. Run start protocol (sessions/LATEST + project-standards.md + workplan-orchestrator skill)
2. Load this workplan
3. Read `working/mobile-app-prototype-v9/README.md` and `SCHEMA.txt`
4. Decide whether to continue Phase 1 (Sonnet UI/component work) or whether the user wants to switch to Opus session for Phase 2 synthesis content first
5. If Phase 1 — view `data2.js` in chunks; build components per 1.2; assemble per 1.5
6. If Phase 2 — Opus session, work through priority rooms in order, save each room's synthesis to a new `data3-rooms.js` in the same prototype directory

The chat transcript at `/mnt/transcripts/2026-04-30-02-38-27-guidebook-mobile-app-iterations.txt` contains v8's complete .jsx (last fully-assembled state) and the design rationale for each iteration. Useful as a reference for the assembled-app state v9 needs to extend.
