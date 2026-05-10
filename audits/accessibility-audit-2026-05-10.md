# Guidebook — Accessibility & Design Audit
**[SELF-AUTHORED — bias risk] · Verified 2026-05-10 · Against: index.html, specs/e-08.html, assets/guidebook.css**

All claims in this document are backed by direct code inspection. The prior analysis is superseded where marked.

---

## Corrections to prior analysis

**WITHDRAWN — z-index collision between `.pop` and `.sectnav`:** The `.pop` divs sit at the end of the DOM, after `</main>`. At equal z-index (both 80), later DOM order wins. Popovers render above the sectnav. Not a bug.

**WITHDRAWN — "skip link lands users into sectnav":** The sectnav `<nav>` is positioned *before* `<main id="main">` in DOM order (between the subbar nav and the main element). The skip link's `href="#main"` correctly skips all navigation including the sectnav. Skip link behavior is correct.

**CONFIRMED more precisely — section reordering is inert:** No CSS anywhere consumes `var(--order-spec)` or `var(--order-q)`. No `order:` property is applied to section elements. No flex or grid container is defined for `.spec-content`. The custom properties are set on every section but never read. The mode toggle changes visual framing (title wording, body class) but sections render in source order regardless of mode.

---

## Verified issues — organized by audience impact

---

### Group A: Broken CSS variables (affects all users — visual and functional failures)

All confirmed by grep with zero `--radius:`, `--accent:`, `--ochre:`, `--wrap:` definitions in `:root`.

**A1. `--radius` undefined** *(5 occurrences)*
Used on `.compare-wrap`, `.hero-drawing`, `.hero-value-card`, `.hero-value-card::before`, `.hero-stats`. Falls back to `initial` → 0px. Those elements render with no border-radius, inconsistent with every other container in the design (which uses `10px` or `999px` directly).

**A2. `--accent` undefined** *(3 occurrences)*
```css
.sectnav-list a:focus-visible { outline: 2px solid var(--accent); }  /* line 531 */
.sitemap-list a:focus-visible  { outline: 2px solid var(--accent); }  /* line 606 */
.lens-select:focus             { outline: 2px solid var(--accent); }  /* line 1538 */
```
All three resolve to nothing. **The section-nav chips and lens dropdown have invisible focus outlines.** WCAG 2.4.7 Focus Visible failure on the two most-used interactive controls on the spec page.

**A3. `--mark-opus-*` / `--mark-src-*` self-referential** *(lines 75–81)*
```css
--mark-opus-bg: var(--mark-opus-bg);  /* resolves to nothing */
```
The markers toggle button's pressed state (lines 679–682) applies these variables for background, border, and text color. When markers are enabled, the button has no visual change. The `.src-chip` elements (⚠ opus annotations) have no background or border. Both the button affordance and the chip visibility are broken.

**A4. `--ochre` undefined**
Used in `.compare-table tbody tr.row-spread { background: color-mix(in srgb, var(--ochre) 6%, var(--paper)); }`. The jurisdiction table's spread summary row gets no highlight.

**A5. `--wrap` undefined**
Used in `.lens-bar-inner { max-width: var(--wrap); }`. The lens bar (legacy control) has no max-width constraint, but this component is not in current pages, so impact is limited.

**Fix for all:** Add to `:root`:
```css
--radius:           10px;
--accent:           var(--blue);
--ochre:            #c08a2c;
--wrap:             var(--max-w);
--mark-opus-bg:     #f8ecd4;
--mark-opus-fg:     #7a5a1a;
--mark-opus-border: #d4b47a;
--mark-src-bg:      #d8ead4;
--mark-src-fg:      #2d5a3a;
--mark-src-border:  #8ab88a;
```

---

### Group B: Unstyled structural classes (index.html — layout broken)

**B1. `.layout`, `.spec-content`, `.infobox`, `.h2-num` have no CSS rules.**

The landing page (`index.html`) uses all four:
- `.layout` wraps the article and sidebar. No CSS → no grid/flex → sidebar stacks below article as a plain block on all viewports. There is no two-column layout anywhere on the landing page.
- `.spec-content` wraps the article. No CSS.
- `.infobox` / `<aside>` wraps the quick-reference sidebar. No CSS → renders as a full-width block element.
- `.h2-num` used as section number labels (`§ 1 · Entry`, etc.). No CSS → no styling, just plain inline text.

This is not just a visual issue. The sidebar contains status information ("Active · drafting", "WCAG 2.2 AA · audited 2026-05", conformance claims) that is structurally orphaned. Users who rely on source order and structure (screen readers, reading modes, print) encounter it after the entire article, with no visual or structural cue that it's supplementary.

**Fix:** Define the layout. Minimum:
```css
.layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 48px;
  align-items: start;
}
@media (max-width: 800px) {
  .layout { grid-template-columns: 1fr; }
}
.infobox {
  position: sticky;
  top: 24px;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  border-radius: 10px;
  padding: 20px;
}
.infobox-head {
  font-family: var(--font-mono);
  font-size: var(--fs-xs);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 14px;
  font-weight: 600;
}
.h2-num {
  font-family: var(--font-mono);
  font-size: var(--fs-xs);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  display: block;
  margin-bottom: 6px;
}
```

---

### Group C: Contrast failures (sight — WCAG 1.4.3)

Measured against WCAG AA: 4.5:1 for normal text, 3:1 for large text (18px+ regular or 14px+ bold).

| Color pair | Ratio | Use | Verdict |
|---|---|---|---|
| `--muted-2` (#948a7c) on `--paper-2` | 2.71:1 | Breadcrumb separator `›` | Decorative; acceptable |
| `--sec-6` / `--ochre` (#c08a2c) on `--paper-3` | 2.86:1 | `.r-tag` text on evidence tier rows | **FAIL** — small text |
| `--pop-vis` (#b88a2c) on `--paper-3` | 2.95:1 | `.r-tag` on VIS population row | **FAIL** — small text |
| `--ev-provis` (#c08a2c) on `--paper-3` | 2.86:1 | `.r-tag` on provisional evidence row | **FAIL** — small text |
| `--pop-pain` (#b85b1b) on `--paper-3` | 4.35:1 | `.r-tag` on PAIN row | **FAIL** — 4.5 needed |
| `--warn` (#b8521b) on `--warn-soft` | 3.78:1 | "✗ does not comply" verdict badge | Passes AA-large; fails small |
| `--blue` (#2a6fdb) on `--paper` | 4.24:1 | Links at body text size | **FAIL** — needs 4.5 |
| tier-5 ochre (#c08a2c) on near-paper | 2.75:1 | Tier chip text | **FAIL** |

The ochre/amber family is the systemic problem. The color conveys "provisional / editorial" meaning and is used in multiple places as small text, but its contrast against the warm paper background is consistently below 3:1. Strengthening it to approximately `#7a5a00` yields 4.6:1 without losing the amber hue.

The blue link color at body size is a borderline AA fail (4.24 vs 4.5 required). Since links are underlined (the CSS adds `border-bottom` on hover but not by default), the underline decoration partially compensates per WCAG 1.4.1, but the color-only distinction of linked text from non-linked text in paragraphs remains. Add `text-decoration: underline` to non-hover link state, or darken blue to `#1f5ab0` (6.8:1).

---

### Group D: Section reordering is inert (all users — spec/question mode doesn't work)

Confirmed: no CSS reads `var(--order-spec)` or `var(--order-q)`. The `<article class="spec-content">` and its child `<section>` elements have no `display:flex`/`grid` + `order:` applied.

In question mode, the body gets `class="mode-question"`. This:
- Changes which title `<h1>` span is visible ✓
- Changes which `h1.title-spec`/`h1.title-question` on index.html is visible ✓
- Does nothing to section render order ✗

Section `§2 · Why it matters` has `--order-spec:11; --order-q:1` — intended to be the last section in spec mode but the first in question mode. It renders second in both modes (its source position).

**Fix:**
```css
.spec-content {
  display: flex;
  flex-direction: column;
}
body.mode-spec .section   { order: var(--order-spec); }
body.mode-question .section { order: var(--order-q); }
```

---

### Group E: Keyboard and ARIA failures (sight — screen readers, keyboard-only)

**E1. Popover focus management**
When a citation trigger or cross-ref trigger is clicked, the popover appears via `data-open="true"` but focus stays on the trigger. No `.focus()` call exists in the JS. Screen reader users receive no notification of the popover's appearance.

Additionally: popovers lack `role="dialog"`, `aria-labelledby`, and focus trap. There is no way for a screen reader user to discover the popover opened, navigate into it, or close it with Escape (Escape is implemented for popovers but not announced).

**Fix minimum:** On popover open, move focus to the popover container; add `role="dialog"` and `aria-labelledby="pop-head-id"`. On close, return focus to trigger.

**E2. Lens menu: ARIA role/keyboard mismatch**
The lens dropdown uses `role="menu"` with `role="menuitemradio"` children. The ARIA menu pattern requires arrow-key navigation between items, Home/End to jump, and Tab to exit the menu. Current JS has no ArrowUp/ArrowDown handlers. Users Tab through all four options sequentially — correct behavior for a `radiogroup`, not a `menu`.

Additionally: Escape key is implemented for popovers but NOT for the `<details>` lens menu. Pressing Escape while the lens menu is open does nothing.

**Fix:** Either implement ARIA menu keyboard pattern (arrow keys, Home/End, automatic focus management), or change roles to `role="radiogroup"` on the container and `role="radio"` on each button. The latter is simpler and more honest.

**E3. `aria-hidden="true"` not updated on mode switch (spec page)**
`specs/e-08.html` line 111:
```html
<span class="title-question" aria-hidden="true">Can two power wheelchairs…</span>
```
The `setMode()` function toggles body classes. CSS in `mode-question` makes `.title-question` visible. But the `aria-hidden="true"` attribute is never removed. In question mode, the question title is visually visible but AT-invisible. Screen reader users in question mode still only hear the spec-mode title.

**Fix:** In `setMode()`:
```js
document.querySelector('.title-spec').setAttribute('aria-hidden', mode === 'question' ? 'true' : 'false');
document.querySelector('.title-question').setAttribute('aria-hidden', mode === 'question' ? 'false' : 'true');
```

**E4. Subbar `aria-label="Breadcrumb"` is inaccurate (spec page)**
The `<nav class="subbar" aria-label="Breadcrumb">` contains two children: the `<ol class="crumbs">` breadcrumb AND the mode toggle `<div>`. Labelling the nav as "Breadcrumb" misrepresents its contents to AT. Screen reader users navigating by landmark will encounter it as the breadcrumb nav, not finding the mode toggle until they explore inside.

**Fix:** Change to `aria-label="Page navigation"` or `aria-label="Breadcrumb and reading mode"`.

**E5. Compare-scroll has no keyboard scrollability**
`.compare-scroll { overflow-x: auto }` on the jurisdictions table. The container has no `tabindex="0"`, so keyboard users cannot focus the scroll container to scroll it. They can Tab to individual table cells, and the browser *may* auto-scroll, but horizontal scrolling of the container is not guaranteed. On narrow viewports, the right-side jurisdictions may be unreachable via keyboard.

**Fix:** Add `tabindex="0"` to `.compare-scroll` when the table overflows.

**E6. `aria-live` on static empty-state content (§9)**
```html
<div class="empty-state" role="status" aria-live="polite">
```
This content is rendered at page load and never changes dynamically. `aria-live` on static content may cause screen readers to announce it unexpectedly on load. `role="status"` implies the content will change.

**Fix:** Remove `role="status"` and `aria-live="polite"`. Plain `<div>` with an `<h3>` heading is sufficient; the heading provides the necessary structure for AT navigation.

---

### Group F: Missing ARIA and semantic problems

**F1. Dead links — landing page (executive dysfunction / cognitive load)**

14 `href="#"` or `href="#anchor"` links on `index.html` go nowhere:
- Primary nav: Populations, Rooms, Conflicts, Jurisdictions, Bibliography (`href="#"` anchors with no matching element)
- About nav item links to `#about` which exists, so that one is fine
- Door 3 links to `#populations`, Door 4 to `#economics` — no matching elements
- "Recently modified" list: 4 of 5 entries link to `href="#"`
- Infobox: "data/guidebook.db" links to `#`
- Three architecture xref links to `#`
- A-02 link in popover footer: `href="#"`

For users with executive dysfunction, a dead link is not just annoying — it breaks the spatial model of the site ("I can go to populations from here"). After encountering dead links in navigation, users cannot trust the nav structure and must rely entirely on working memory.

**Fix:** Replace dead nav links with either working links or non-link text. Distinguish "not yet built" from "an error" — a `<span>` with `title="Coming soon"` styled like muted text is better than a link that goes nowhere.

**F2. `data-door` attributes missing on landing page**

CSS defines distinct door colors via `[data-door="1"]` through `[data-door="4"]`. The HTML `<a class="door">` elements have no `data-door` attribute. All four doors render with the default `var(--ink)` stripe — no color differentiation. The CSS is ready for this feature; the HTML never activates it.

**Fix:** Add `data-door="1"` through `data-door="4"` to the four `.door` elements.

**F3. Jurisdiction checkbox labels — country codes only**

```html
<label class="juris-pick"><input type="checkbox" data-juris="NO">NO</label>
```

"NO" is a valid abbreviation but ambiguous to AT ("no" vs "Norway"). "DE" reads as a word, not a country. Labels are technically accessible (the `<label>` wraps the input), but screen reader users hear "DE checkbox" and must know that DE = Germany.

**Fix:** Use `aria-label` or visible full names: `<label aria-label="Germany"><input...><span>DE</span></label>`.

---

### Group G: Touch targets (motor impairments — WCAG 2.5.8)

| Element | Effective size | Issue |
|---|---|---|
| Citation trigger `[1]` | ~22×20px | Fails 24px AA minimum |
| Mode toggle buttons | ~22×24px | Fails 24px AA minimum |
| Copy button (`pre` block) | ~22×22px | Fails |
| SVG hotspot circles (`r=10`) | 20×20px | Fails; these are tappable `role="button"` elements |
| `ex-preset` buttons | ~24×24px | Borderline |

SVG hotspots are the most significant: they are keyboard-accessible (`tabindex="0"`, `role="button"`) but their 20×20px touch target is too small for motor-impaired users to tap reliably.

**Fix:** Increase citation trigger padding to `padding: 3px 8px; min-height: 28px`. For SVG hotspots, add an invisible larger hit area:
```svg
<circle r="18" fill="transparent" pointer-events="all"/>  <!-- hit area -->
<circle class="hot" r="10" .../>  <!-- visual only -->
```
Or increase the visible radius to 14px.

---

### Group H: Reduced-motion gap (sight — vestibular / photosensitive)

The CSS correctly applies:
```css
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
```

But the interactive corridor-width explorer (§4) animates SVG elements by directly mutating attributes via JS (`setAttribute('y', ...)`, `setAttribute('transform', ...)`). These are not CSS transitions — the `prefers-reduced-motion` CSS rule has no effect on them. On every slider drag, the corridor walls, zone rectangle, chairs, and dimension strings animate.

**Fix:** Check the media query in JS before updating:
```js
var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// In update(): if prefersReducedMotion, skip SVG attribute animation; jump directly to final state.
```
Or, simplify: remove the live SVG mutation and only update the readout cells (width, separation, cost, verdict) when reduced motion is active.

---

### Group I: Print styles incomplete

```css
@media print {
  .masthead, .subbar, .skip, .colophon { display: none; }
}
```

Missing: `.sectnav` is not in the hide list. Since sectnav is outside `<main>` (between the subbar and main), it will print: a sticky-positioned nav showing "§ 0 · Top of page" above the article. Also missing: the popover library divs at the bottom of the DOM would print as empty invisible boxes (they're `display:none` until opened — OK), but the empty space they'd occupy if opened is not addressed.

**Fix:** Add `.sectnav` to print hide list. Also consider `details.row[open] > .r-body { display: block !important; }` is already in print styles (good) but `details.row:not([open]) > .r-body` could be force-opened too to ensure full content prints.

---

### Group J: Duplicate CSS blocks

**J1. Two `.masthead` and `.masthead-inner` blocks**

Block 1 (line 157): `padding: 18px 28px 14px`, `align-items: baseline`, nav `gap: 18px`
Block 2 (line 345): `padding: 18px 28px`, `align-items: center`, nav `gap: 22px`

Block 2 overrides Block 1 for all properties. The nav on both pages gets `gap: 22px`, `align-items: center`. Block 1 is dead code — its distinct values are never applied. The separate nav styles in Block 1 (14px font, 18px gap, different hover) are all overridden by Block 2 (14px font, 22px gap, `color: var(--ink)` on hover).

**Fix:** Delete Block 1 (`lines 157–209` up to the next comment block). Block 2 is complete.

---

### Group K: Cognitive-load and organizational issues

**K1. Accordion default state — all rows closed**
All sections start with every `<details>` closed. Users with executive dysfunction must actively expand each row to see any content. The lens system partially addresses this for a subset of rows. Recommendation: default the first row in each section to `open` unconditionally.

**K2. No "expand all" affordance**
No control exists to open all rows at once. Power users and users who want to read linearly must click every row individually. Adding a small `expand all / collapse all` toggle per section would serve sequential readers.

**K3. No "back to contents" link mid-page**
The sitemap is an excellent orientation tool at page top. Mid-page, the sectnav chips provide a flat numbered list but no return to the descriptive sitemap. A `↑ Contents` link as the first item in the sectnav chip list would give one-click access to the sitemap's descriptions from anywhere.

**K4. Dual view customization systems**
The spec/question mode toggle and the audience lens menu operate independently and affect different things. New users must understand both systems to optimize their view. Consider surfacing a one-line description of the current lens directly in the UI (e.g., below the sectnav: "Reading as: Designer / architect — Drawing & Values sections open").

---

## Summary table

| ID | Issue | WCAG | Severity | Effort |
|---|---|---|---|---|
| A2 | `--accent` undefined → invisible focus on sectnav/sitemap/lens | 2.4.7 | **Critical** | 5 min |
| A3 | `--mark-opus-*` self-referential → markers feature non-functional | — | **Critical** | 5 min |
| A1,A4 | `--radius`, `--ochre` undefined | — | High | 5 min |
| B1 | `.layout`, `.infobox`, `.h2-num` have no CSS → layout broken | — | **Critical** | 1 hr |
| D | Section reordering inert → spec/question mode doesn't reorder | — | **Critical** | 15 min |
| E3 | `aria-hidden` not updated on mode switch | 4.1.2 | High | 5 min |
| C | Ochre/amber contrast failures across multiple r-tag texts | 1.4.3 | High | 30 min |
| F1 | 14 dead links on landing page | — | High | 30 min |
| E1 | Popover: no focus management, no dialog role | 4.1.2, 2.1.1 | High | 1 hr |
| E2 | Lens menu: ARIA menu role without keyboard pattern | 4.1.2 | High | 1 hr |
| E4 | Subbar aria-label misleads about content | 4.1.2 | Medium | 2 min |
| E5 | Compare-scroll not keyboard-scrollable | 2.1.1 | Medium | 10 min |
| E6 | `aria-live` on static empty-state | 4.1.3 | Medium | 2 min |
| F2 | `data-door` attributes missing → color coding inert | — | Medium | 2 min |
| F3 | Jurisdiction checkboxes use country codes only | 4.1.2 | Medium | 10 min |
| G | Touch targets below 24px (citations, mode toggle, SVG hotspots) | 2.5.8 | Medium | 30 min |
| H | JS animations don't respect prefers-reduced-motion | 2.3.3 | Medium | 30 min |
| I | Print: sectnav not hidden | — | Low | 2 min |
| J1 | Duplicate masthead CSS → dead code | — | Low | 5 min |
| K1–K4 | Cognitive load: closed accordions, no expand-all, no back-to-contents | — | Medium | Design decisions |

**Total verified WCAG failures:** 8 (A2, E1, E2, E3, E4, E5, E6, C)
**Critical non-WCAG bugs:** 3 (A3, B1, D)
**Highest-leverage single fix:** Add the six CSS variable definitions (A1–A5) — fixes invisible focus, broken markers, and visual inconsistencies in ~5 minutes.

---

*Audit methodology: static code analysis of all three files. No browser rendering, no AT testing, no user testing. AT behavior is inferred from ARIA spec and established patterns. Rendering and interaction issues require browser-level verification to confirm.*
