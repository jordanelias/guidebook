# Mobile App Prototype — V9.0
**Status:** Complete · Single-file React/JSX artifact assembled and validated
**Last updated:** 2026-04-30 03:05 UTC
**Model:** Opus 4.7 Adaptive

## What this is

Production-ready React/JSX mobile interface for the Guidebook V9.0. Designed for claude.ai artifact rendering — single .jsx file with inlined data, components, and CSS. Renders directly without external dependencies beyond React and Google Fonts CDN.

## Files

| File | Lines | Purpose |
|---|---|---|
| `guidebook-app.jsx` | 5273 | Final single-file artifact |
| `SCHEMA.txt` | 52 | Field definitions for spec architect-data and room synthesis |
| `data1.js` | 46 | Working data: POPS, CATEGORIES, TIERS, TOPICS |
| `data2.js` | 1393 | Working data: 11 ITEMS with full architect data |
| `data3-rooms.js` | 945 | Working data: 14 ROOMS_SYNTHESIS records |
| `README.md` | this file | Documentation |
| `HANDOFF.md` | (superseded) | Earlier handoff plan; v9 now complete |

## What's in the artifact

### Five tabs
1. **Preface** — hero + how-to-read + tier explanation + entry points
2. **Buildings** — 14 rooms across Residential / Non-Residential
3. **Specs** — 11 specifications by category with mode toggle
4. **People** — 10 populations with relevant entries
5. **Index** — Master index with multi-axis filters and free-text search

### 11 specifications with architect data
A-02, A-16, B-04, B-10, C-04, D-04, E-01, E-08, E-10, G-04, H-01

Each carries: dimensions table, performance table with measurement methods, codes by jurisdiction with clauses, manufacturer-neutral products, drop-in schedule language with copy-to-clipboard, detail item accordions, embedded SVG diagram, install notes, failure patterns, per-population rationale, applicable rooms by building, related entries with rationale, evidence accordion, topic tags.

### 14 rooms with synthesis content
Priority (R-BA, R-KIT, R-BED, R-LIV, R-HAL, R-ENT, NR-EDU, NR-HLT, NR-WRK) include synthesis prose, sequence, interactions, clearances, failures, and SVG diagram. Compact (R-LAU, NR-RET, NR-CUL, NR-HOS, NR-TRP) include synthesis without diagram.

Each carries: design synthesis prose, sequence of design decisions, critical interactions (cross-linking specs), stats panel, critical Tier 0 callout, all entries grouped by category with inline expansion, clearances table, common failure patterns, schematic plan diagram.

### Persistent toggle
"Specifications | Questions" at top of every screen. `role="radiogroup"`. Same content, two reading voices.

### Click-citation popovers
Population codes throughout text are tappable. Popover shows population description, relevant spec count, and jump action. ESC dismiss, click-outside dismiss, focus restoration.

## Accessibility

- Bone (#F2EBDD) on ink (#1A1612): 14.8:1 contrast (AAA exceeds 7:1)
- Touch targets ≥44 px
- Focus-visible 2 px ink rings on every interactive element
- `aria-current`, `aria-pressed`, `aria-expanded`, `aria-haspopup`, `role="dialog"`, `role="radiogroup"` throughout
- `prefers-reduced-motion` honoured
- Semantic HTML throughout
- Keyboard navigable — Tab, ESC, Enter/Space
- No hover-dependent functionality
- Descriptive `aria-label` on every diagram, cite, and form control

## Validation

- Parsed with `@babel/parser` (sourceType: module, plugins: jsx) — clean parse, 45 top-level statements
- Single default export
- All 7 data structures defined exactly once
- All 27 components defined and reachable

## How to render

Drop `guidebook-app.jsx` into a claude.ai artifact (type: `application/vnd.ant.react`). Or import as a React component into any React 18+ project.

## Provenance

V9 extends V8 (recoverable from chat transcript) by adding architect-facing fields to spec records and synthesis fields to room records. V8 architecture (persistent toggle, master index, click-citation popovers, breadcrumbs, accordions) preserved unchanged. V9 additions described in `SCHEMA.txt` and demonstrated for 11 specs and 14 rooms in this artifact. Schema designed across multiple sessions; final assembly authored by Opus 4.7 Adaptive 2026-04-29 to 2026-04-30. Spec architect-data references AS 1428.1:2021, AS/NZS 2107:2016, ADA 2010, ISO 21542:2021, BS 8300, IEEE 1789-2015, AS 4428.16, AS 4586, AS 3740, and related standards.
