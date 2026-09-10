# mobile-app-prototype v9 — Handoff

**Last update:** 2026-05-02 02:28 UTC
**Status:** v9 — restructured IA, accordion-pattern, 4-domain navigation
**File:** `working/mobile-app-prototype-v9/guidebook-app.jsx` (~6,500 lines, single-file React)

---

## What's in v9 now

### Information architecture (5 top-level tabs)

1. **Doctrine** — frameworks, approaches, foundational concepts
2. **Practice** — sub-tabbed: Buildings · Specs · Populations
3. **Resources** — collaborators, organisations, methods, references
4. **Economics** — cost case, lifecycle, retrofit-vs-design-in, incentives
5. **Index** — master alphabetical index across all specs/rooms

Preface dropped from bottom nav. Still defined as `tab="preface"` route; reachable when wired (currently no entry surface). Decide next session: nav slot, header logo link, or retire.

### Accordion-everywhere pattern

Every spec, room, doctrine, resource, and economics detail page uses the **`Point`** component pattern — every dimension, performance metric, code clause (grouped by jurisdiction), product, detail group, install note, failure pattern, sequence step, interaction, clearance, related entry, key point is its own drop-down row. Each opens to show:
- Note / why / measurement
- **Relates to** (auto-extracted spec codes via regex; clickable)
- **Conflicts & trade-offs** (filtered from `related[].why` text on conflict-language keywords)
- **Evidence** (parent entry's evidence array, inherited at point level — labeled clearly)

No prose dump at the top. About-row first, expanded by default; everything else closed.

### Data scope (current placeholders)

| Domain | Entries | Status |
|---|---|---|
| Specs (ITEMS) | 11 with full architect data | unchanged from earlier v9 |
| Rooms (ROOMS_SYNTHESIS) | 14 (9 full + 5 compact) | unchanged from earlier v9 |
| Doctrine (DOCTRINE) | 10 — full author-voiced stubs | NEW |
| Resources (RESOURCES) | 7 — full author-voiced stubs | NEW |
| Economics (ECONOMICS) | 5 — every figure flagged `[UNVERIFIED]` | NEW |

Doctrine entries cover: social model, medical model, relational model, disability justice, universal design, inclusive design, visitability, co-design, cognitive accessibility, sensory design.

Resources entries cover: disability co-designers, OT, access consultant, DPOs, walking interviews, POE, Mismatch (Holmes 2018).

Economics entries cover: marginal cost design-in vs retrofit, total addressable market, bathroom cost delta, aging-in-place, funding/incentives. **All numerical claims are `[UNVERIFIED]` pending economics-research pass** — this matches the broader project's economics methodology workstream (see commits dc5e544, e226c36, 38b1490).

---

## What's NOT done

1. **Economics figures unsourced.** Every cost percentage, retrofit multiplier, prevalence stat in ECONOMICS entries is illustrative. The project's economics methodology pass (separate workstream) needs to land before these can be unflagged.
2. **Per-point evidence is heuristic.** The Point component shows the parent spec's evidence array as the evidence-base for each point. True per-point evidence requires schema extension (`evidence_refs: [...]` on each dimension/perf/code row). Schema change, not UI change. Standing Rule 7 — TOC Change Order before active-dataset migration.
3. **Conflict surfacing is keyword-filtered**, not curated. Catches "stricter / differs / exception / vs / however / tension / trade-off / inverse / opposite". May miss real conflicts whose prose doesn't use these words.
4. **Schema additions still in working/.** The 9 new spec-record fields and 6 new room-record fields from the earlier 7ce98529 commit, plus the new DOCTRINE/RESOURCES/ECONOMICS arrays added in this session — none have been migrated to the active dataset. Standing Rule 7 requires `toc-editor` Change Order first.
5. **Synthesis prose is Sonnet-authored** for prototype demonstration. `synthesis_source: "sonnet-illustrative"` annotation pattern from earlier sessions still holds. Replaceable when an Opus session does the room-syntheses pass.
6. **Dead code:** `SynthesisSection` component is no longer referenced (room synthesis is now Point-pattern); ~10 lines, harmless.

---

## Phase 2 (next session, recommended order)

1. **Doctrine expansion** — current 10 stubs cover the major frameworks. Likely additions: trauma-informed design, neurodivergent design, intersectional access, anti-ableism in practice, disability art / aesthetics. Decide group structure.
2. **Resources expansion** — current 7 stubs are minimal. Likely additions: peer-reviewed databases, jurisdictional code references, manufacturer-neutral product registries, training programs, certifying bodies (registered access consultants), conference/community lists.
3. **Economics population** — wait for economics-methodology workstream to land (per active workstream commits dc5e544 etc.), then populate ECONOMICS entries with sourced figures, remove `[UNVERIFIED]` flags.
4. **Cross-domain related linking pass** — DOCTRINE entries should auto-suggest related specs (e.g. DOC-09 cognitive accessibility → all C-category specs). Currently each entry's `related[]` is hand-curated. Could auto-extract via topic match.
5. **TOC Change Order** — formalise the 4-domain IA + new schemas + Doctrine/Resources/Economics shape. Required by Standing Rule 7 before any active-dataset migration.
6. **Preface decision** — reinstate in nav, move to header, or retire.

---

## Files in working/mobile-app-prototype-v9/

- `guidebook-app.jsx` — single-file assembly (~6,500 lines, parses clean, single default export)
- `README.md` — original architect schema reference
- `SCHEMA.txt` — schema for spec record additions
- `data1.js` — POPS, CATEGORIES, TIERS, TOPICS source (now inlined in jsx)
- `data2.js` — ITEMS source (now inlined in jsx)
- `data3-rooms.js` — ROOMS_SYNTHESIS source (now inlined in jsx)
- `HANDOFF.md` — this file

Source data files retained for reference and external inspection but the `.jsx` is now self-contained.

---

## Validation

- Babel parser: PARSE OK
- Top-level: 64 statements, 1 default export, 36 functions, 26 consts
- File size: ~360 KB
- No localStorage / sessionStorage usage (artifact-safe)
- No external dependencies beyond React core hooks

---

## Standing rules adherence in this session

- Rule 1 (>500 lines): respected — surgical edits with view ranges, never full-file context loads
- Rule 2 (UTC timestamps): all commits via `date -u`
- Rule 3 (.md default): handoff is .md
- Rule 6 (Sonnet ≠ best practice): doctrine/resource entries are settled-knowledge consolidation, not best-practice determination; economics figures flagged `[UNVERIFIED]` rather than asserted
- Rule 7 (toc-editor before structural change): NOT YET DONE — schema additions still in `working/`, no migration to active dataset attempted
- Rule 10 (no rushing): committed before final polish; opted for clean handoff over compressed completion
