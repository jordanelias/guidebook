# E-03 page: design, hierarchy, UX and navigation defects (static and data audit)

Status: SELF-AUTHORED, PESSIMISTIC BY DESIGN. Audit of `specs/e-03.html` (commit 525a2083) from its source, its data and
its script logic. A separate reviewer is doing a visual, rendered critique in the browser pane; its report is not
merged here. Every finding carries how it was established:
- CODE = read from the generator's CSS or JS; DATA = measured from `data/spec_pages/E-03.json`;
- MEASURED = measured on the rendered page earlier in this session;
- UNVERIFIED = a plausible defect that needs a rendered check.

New owner constraint applied (2026-10-30): **minimalism must not come at the expense of readability and legibility,
especially for accessibility of website navigation.** Section E tests the page against it.

## A. Breaking behaviour

| ID | Sev | Finding | Basis |
|---|---|---|---|
| A1 | Major | Evidence regrouped by a lens keeps a group heading even when a filter hides every entry under it, leaving orphan headings. `regroup()` builds headings from all entries, ignoring `.hidden`. | CODE |
| A2 | Major | The lens and filters affect only the values table and the evidence list. The jurisdiction comparison table never changes; the access-need filter only dims provisions inside the details accordion, which is closed by default. In section 2 the filter appears to do nothing. Pill counts also cover only values rows and evidence. | CODE |
| A3 | Major | Table sort has no state indicator and no `aria-sort`; its label always reads "Sort steepest first", even after it reverses; the only way back to alphabetical order is a reload; the control sits inside the column header, so the header's accessible name becomes "Maximum Sort steepest first". | CODE |
| A4 | Minor | Filter state overwrites the whole URL hash; clicking a section link replaces the hash and drops the filter state from the URL (and the back button then walks through these states). | CODE |
| A5 | Minor | The "hit" row highlight is a `box-shadow` on `<tr>`; Chrome does not paint shadows on table rows, so a filtered row may show no marker. | UNVERIFIED |
| A6 | Minor | Print: closed `details` stay closed, so evidence notes, jurisdiction details and gaps do not print. | CODE |
| A7 | Minor | With imperial units the drawing's value text (`nowrap`) follows a triangle sized to 82% of the row, which may overflow at 320 px. | UNVERIFIED |
| A8 | Trivial | Dead or orphaned CSS (`.q`, `.note`); several classes used by script have no rule. | CODE |

## B. Inconsistencies in design choices

| ID | Sev | Finding | Basis |
|---|---|---|---|
| B1 | Major | No spacing scale: 45 distinct padding and margin values, 28 distinct pixel values, 6 line heights, 14 different `gap` values. | MEASURED (CSS) |
| B2 | Major | Two content edges. Sections, controls and the drawing use a 3 / 9 split (content starts at 25%); the page title, the hero figures and their equal columns start at 0 and the second hero figure starts at 50%. The grid is not one grid. | CODE |
| B3 | Minor | Section numbers sit above the heading on desktop and inline on narrow screens. | CODE |
| B4 | Minor | Five different reading measures (66ch, 34em, 46em, 52em, unconstrained table cells). | CODE |
| B5 | Major | The same underlined-button style is used for opening a popup, sorting, clearing filters, citations and applied-filter removal; the same bold weight marks both a value and (in the top row) a label. One cue, many meanings. | CODE |
| B6 | Major | Red is the only accent and means five things: current section, open lens, pressed pill, keyboard focus, and highlighted row. Red conventionally signals error. | CODE |
| B7 | Major | The other 88 spec pages, the exemplar `specs/e-08.html` and the site index use different designs, and this page's "Cited on" and breadcrumb links lead to them. | CODE |
| B8 | Minor | The type stack starts with Helvetica Neue, which is absent on most Windows machines, so the delivered design is Arial there. | CODE |

## C. Failures in information hierarchy

| ID | Sev | Finding | Basis |
|---|---|---|---|
| C1 | Major | The same value is shown about seven times: hero, drawing, the comparison "Best practice" row (preferred and maximum), and three of the four values rows (all "1:20 or gentler"). The real differences (the qualifiers) are 13 px and muted. | DATA |
| C2 | Major | Comparison table columns are sparse: Preferred is filled for 5 of 15 jurisdictions; Between landings for 11 of 15; only 2 rows have all three. On a phone the empty cells are hidden, so the cards have different shapes. | DATA |
| C3 | Major | The evidence list shows the least informative part (the citation) and hides the most informative parts (why the source matters, tier, where it is cited) behind 16 closed accordions. | CODE |
| C4 | Major | The drawing is two triangles of the same height drawn 10 m and 8.33 m long (17% apart). The triangles imply an angle that is not to scale; a plain bar would encode length honestly. The drawing adds little beyond the hero. | DATA |
| C5 | Minor | The hero gives "Best practice found" and "Gentlest legal maximum, Germany" equal weight and equal size; their relationship is explained only in a 13 px muted note. | CODE |
| C6 | Minor | Weight alone separates a value from its row label (both 16 px); there is one cue for the most important distinction in the tables. | MEASURED |
| C7 | Minor | "Set by individual assessment" is a non-value in the Value column, mixing categories. | DATA |
| C8 | Major | Controls precede information, so the answer starts below two or three control rows: about 510 px down with the lens closed and about 740 px with a pill row open at 1280 wide. At 812x375 the hero is below the first screen. | MEASURED / UNVERIFIED (landscape) |

## D. Failures in user experience

| ID | Sev | Finding | Basis |
|---|---|---|---|
| D1 | Major | Every value in the comparison table is a button: roughly 40 tab stops with no way to skip them; the bold underlined text does not look like "opens a popup". | CODE |
| D2 | Minor | Popups duplicate the content of the details accordion; there are two routes to the same content, no URL for a popup, and no way to compare two jurisdictions. | CODE |
| D3 | Major | Applied filters read "MS x", "d465 x", "AN-01 x": codes without names, contradicting the plain-language rule; "Hide general (everyone) rows" is jargon and can hide the main answer. | CODE |
| D4 | Minor | Filter state persists in memory but not in the visible UI when the lens is closed, except as bare codes. | CODE |

## E. Navigation legibility (new owner constraint)

| ID | Sev | Finding | Basis |
|---|---|---|---|
| E1 | Major | All navigation is set at the smallest size and lowest emphasis: section nav 13 px, breadcrumb 13 px, inactive links `#595959`. Contrast passes (about 7:1) but legibility for low-vision users and small screens is the lowest on the page where it matters most. | MEASURED |
| E2 | Major | The section nav shows no "you are here" until a section crosses the scroll band; at page load, and in the last short section, nothing is marked current. | CODE |
| E3 | Major | The section nav is one horizontally scrolling row of six items with no scroll cue; at 320 px only about two and a half are visible. | UNVERIFIED |
| E4 | Minor | The sticky nav takes 46 px permanently: about 12% of a landscape phone's height. | MEASURED |
| E5 | Major | Disclosure cues are 13 to 16 px grey "+" and "-" glyphs at the far right of rows up to about 750 px wide; the label and the cue are far apart. | CODE |
| E6 | Minor | Links are distinguished from text only by a 1 px underline in the same colour; no visited or hover colour change, only a thicker underline. | CODE |
| E7 | Minor | One skip link (to main content); no skip past the long table, no back-to-top, no landmark for the controls. | CODE |
| E8 | Minor | Disclosures, popups, filters and sort are visually near-identical to body text; discoverability depends on knowing to try them. | CODE |

## F. Things that held up (evidence only)
- Contrast: 0 failures by my own calculation at 320, 375 and 1280 wide, light and dark.
- No horizontal page scroll at seven widths; skip link first in tab order; dialog focus handling.
- One typeface, four sizes, two weights, with the same size for the same role in every section.

## G. What would settle the UNVERIFIED items
A rendered pass at 320 px with imperial units; Chrome rendering of the filtered-row highlight; a landscape-phone first screen; and the separate visual reviewer's report.

## H. Requirement added by this audit (R16, navigation legibility)
Navigation must be at least as legible as body text: 16 px or larger, near-black on white (or the dark equivalent),
a visible current-location state at load, larger targets, disclosure and sort controls whose state is visible, and no
reliance on small grey glyphs. Minimalism may remove decoration, never legibility or state cues.

## I. Persona task walkthrough (owner's four key questions)

Method: for a concrete task per persona, what is visible at load, what needs clicks, and what is missing, from the page
source and data. Numbers are counted from `data/spec_pages/E-03.json`, the database and the generated HTML.

| Question | Verdict | Why |
|---|---|---|
| 1. Can an architect or designer easily find the required values? | PARTIAL | The slope and, for 11 of 15 jurisdictions, a landing-interval figure are in the table. Everything else a ramp needs is only inside a popup or the closed details: of 15 jurisdictions, landing size is recorded for 10, width for 8, handrails for 6, cross-slope for 5, rise per flight for 5, edge protection for 3. For Switzerland, France, Norway and ISO only the slope is known. There is no parameter-by-jurisdiction table (the book's Appendix A.1 had Max Rise/Run and Handrails columns), no way to pick "my jurisdiction", and no list of what is not yet known per jurisdiction. |
| 2. Can a policy writer or legislator easily find precedents and code bodies? | PARTIAL, weak on citation | The standard name and edition are shown under every row, and read level is stated. Clause, regime (statute versus guidance) and tier exist in the data but are never rendered. Links to the official text sit inside the closed details or popup, 2 steps away, and 4 of 15 jurisdictions (Switzerland, France, Norway, ISO) have no link. Only 5 of 15 were read from a primary or official source; 6 are secondary, 3 are earlier extractions, 1 is a library title only. Nine major jurisdictions are listed only as a 13 px grey line of names. |
| 3. Can a therapist or researcher easily find evidence? | WEAK | 16 studies in an alphabetical list, each closed to its citation alone. The population, design, sample size and finding are hidden (8 of 16 notes state a sample size). 7 of 16 have a DOI and 10 of 16 are not VERIFIED, and neither is visible until the entry is opened. 14 of 16 carry a population tag but it only matters if a lens is chosen. No sort by tier or year; no study type; no link to full text unless a DOI exists. Lived-experience evidence: none recorded, stated only inside the Gaps section. |
| 4. Can a person with a disability easily navigate the page? | PARTIAL | Keyboard, focus, skip link, dialogs and live region work. But about 85 tab stops from top to bottom (31 of them table values) with a single skip link; all navigation text is 13 px; no current-section mark at load; jargon in the controls and rows ("Lens", "ICF code", "access need", "tier", "evidence-based / inferred", "Hide general rows"); no plain statement of what 1:20 means for the person ("for every 1 m of height, 20 m of ramp"); the lead sentence was removed. The doctrine names disabled people as a primary audience who need plain language, visible variability and visible lived-experience evidence; the page shows none of these directly. |

Highest-impact fixes, in order:
1. Add a parameter-by-jurisdiction table (gradient, landing size, width, handrails, cross-slope, rise per flight) with empty cells labelled "not read", and a "my jurisdiction" selector.
2. Render clause, regime and tier in the comparison table row and put the official link in the row, not behind a popup.
3. Show what each study says (population, design, n, finding) in the evidence entry's visible line; add tier and year sort.
4. Make navigation legible (R16): 16 px, dark, current section marked at load, a skip link past the table, fewer tab stops.
5. Add a plain-language line for the person reading ("what this means") and replace jargon in controls.

## J. Status after the persona and reviewer fixes (build of 2026-10-30, later)

The independent visual reviewer's report was received and merged with this audit. Verified on the rendered page
(1280, 1024, 800, 812x375, 375, 320; light and dark): no horizontal scroll, 0 contrast failures, 0 targets under 24 px,
four sizes (13/16/24/56, 36 for the hero on phones), two weights, no visible pipeline wording.

**Fixed**
- Persona gaps: a second table with landings, clear width, handrails and cross-slope per jurisdiction (empty cells say "not read"); a "my jurisdiction" selector that pins that row at the top of both tables; clause, document tier and a source link in every comparison row; population, evidence tier, DOI and verification status, and the finding visible on every evidence entry; a plain-language line; applied filters and the citation popup in plain words; reader-facing About text.
- Column widths: every table now fills the 774 px column with fixed, explicit widths; the jurisdiction column lines up across tables; "Between landings" is the widest value column. Cause found: my own `.plain` paragraph class collided with the `.plain` table class and capped all tables at 62ch. Cells wrapping to 3+ lines fell from 71 to 22 at 1280.
- Jurisdictions and the bibliography are alphabetical; the table order control cycles A-Z, steepest first, gentlest first, with `aria-sort`.
- Navigation: 16 px black; current section correct at load ("Overview"), at each section and at the bottom (position-based scroll-spy); one-row "Sections" disclosure on phones; disclosure cues at the left; skip link past the tables.
- One detail route (jurisdiction name opens its entry); the duplicate popup route was removed.
- Zero-count filter options are disabled; filtered counts appear beside the content; orphan lens headings are hidden; the pill panel is bounded to 45% of the viewport height.
- Phone cards are consistent (every card shows the same fields); landscape controls share rows; hero values are 56 px and the page title 24 px; sticky table heads; imperial values round to whole inches and keep number and unit together.
- Pipeline text removed from the reader view (About section, citation titles).

**Still open (not fixed)**
- Landscape phone (812x375): the headline figures start at 395 px, just under the 375 px fold; controls above all information is the owner's rule, so only a shorter bar can help.
- The title and hero still start at the page edge while section content starts at the rail edge (two left edges); the "12-column" grid remains a 3/9 split.
- Citation formatting is not fully APA (italics, "et al." in reference entries); the data lacks full author lists.
- The same 1:20 appears in the hero, drawing, best-practice row and three values rows.
- Page length is 8,100 px on desktop (about 15,300 on a phone), above the original 6,000 px budget because the new tables and evidence lines add content.
- Not re-tested after these changes: screen reader, forced colors, 400% zoom, print, and the keyboard walkthrough of the new jurisdiction links.
