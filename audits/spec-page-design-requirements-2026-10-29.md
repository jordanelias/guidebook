# Specification page: design review, reconciliation and requirements

Status: ANALYSIS ONLY. No page was changed while writing this. Source: every statement the owner made about the
specification pages in the 2026-10-29 session (quoted in section 1), plus the reference sites and articles named.
Purpose: settle what the owner actually requires, resolve the places where the feedback pulls in opposite
directions, and state tenets and acceptance tests, so the next redesign starts from a fixed baseline instead of
another round of restyling.

## 1. The record (grouped, in the owner's words)

**Content and meaning of values**
- "I need exhaustive jurisdiction comparisons ... accordion drop-downs ... top line is the jurisdiction and the salient standard/clause/value/note, and then an expansion upon everything below."
- "A-01 ... far too vague with value of 800-1300mm. who on earth is that 800-1300mm for?" / "'ALL' is fine, but we need to have specific populations too" / "ALL is basically the same as saying it is universal" / "then we have population/code/need specific and then person specific."
- "'Mode P' is jargon for users." / "'WHY IT MATTERS' needs to have line breaks, and it should be using bullet points."
- "we do not need to have rows for people where the value is just 'Not set.' that just means that it shouldn't be showing on the page."
- "how on earth do we have evidence outside the library? we either have evidence or we do not have evidence."
- "You do not need to find evidence for why 1:12 was the code floor--just accept the 1:12 as a baseline." / "if you can't find evidence for why a T4-T6 is why it is, that is fine."
- "We are interested in what are best practices NOW ... we do not need to interrogate the history."
- "do not include countries outside of the major identified countries for now." Buckets 1 and 2: "canada usa australia japan norway etc then like italy china whatever" (the repo's P1+P2+P3 was adopted).

**Tools and interaction**
- "you should be able to select units for each page, ie metric vs imperial, % slope vs ratio slope vs degrees."
- "we also need to be able to sort page by population/ICF code/access need" (restated: filter).
- Filter by one of three lenses; "when you select which lens do you see the pills pop up with the more specific case"; "we don't want to show ALL the pills at once"; "the filters shouldn't start out expanded ... the three lens filters ... are their own row, and when you click one, there is a new row beneath that has the different pills."
- "think about how ... shopping websites make judicious uses of filters where you can filter for colours, prices, sizes ... and then the subsequent more granular items if desired."
- "for ramp gradient, i want there to also be an easy comparison master table where you just see what each jurisdiction has for the value"; "you can click on value for a popup or an anchor location or as its own subpage."
- "you don't need to show the full jurisdiction standard's name in a column ... on its own full span row below ... smaller italicized text."

**Evidence and citation**
- "all of these references 'In the library' to be in APA format with author/body and year ... clickable and pop-up the bibliographic citation and then list all pages where it has been cited under the entry."
- "evidence in the library needs to be sorted alphabetically by last name" and "ideally it is subcategorized by population group/access need/icf code (depends upon filter chosen up top)."

**Research method (shapes the page's content, not its look)**
- "our goal is to be looking at all the bucket 1+2 jurisdictions for what they do with ramps, and then ... what academic studies and professional bodies and advocacy groups recommend."
- "the critical methodology comes from synthesis/adjudication/specifications, not from evidence collection."
- "ensure that we are correctly scraping all information ... from the most recent codes and standards ... and then we move on to higher tier evidence ... across any language in any jurisdiction ... to see if there are even better approaches that go beyond those codes."

**Visual design and hierarchy**
- "I do not like how VALUES is set up ... we don't need to have so many headings and fonts and pills and stuff. this needs to be radically simplified, and we need to make a lot more use of accordions and pop-up pills."
- "think about how dimensions.com presents information ... make the actually salient information/values highly visible and easy to read without needing to spend time reading large lengths of texts."
- "too much page space" (filters/controls); "uses up too much page space."
- "sections do not cleanly separate or have breaks, section headers lack weight or real dynamic identification, too much disparity and breaking logic for font sizes and weights for hierarchy of information."
- "that needs to be way less yellow, and i really dislike the typefaces used and the size hierarchy sucks. the book-era is better for how info is organized not necessarily for style."
- "too many AI design tropes" ... "wikipedia is very good and simple, dimensions.com is very good and simple, substack is very good and simple. the idea is to make this as clearly presented and formatted as possible with information as primary." References given: UX Collective, Medium/PicsRush (not readable: HTTP 403), Bright Avenue, JSTOR (bot challenge; the saved copy is script-rendered), Wiley (403).
- On the Wikipedia-style version: "oh no that is not good at all"; "i don't want it to look like wikipedia"; "the point of wikipedia is that it is very clearly organized"; "the previous design iteration was a lot lot better but the organization of information in this one is much improved ... so far worse aesthetics, better data flow."
- "refer to swiss graphic design." "look at this example [dimensions.com single-hung windows] ... very simple, very clear."
- Review "across different formats and sizes and ratios from landscape to portrait."

## 2. What the references actually say (so the analysis rests on evidence)

- **UX Collective (read):** minimalism is a choice about priorities, not a shortage of design; keep only what helps the visitor reach the goal; one or two typefaces; a clear size difference between headings and body; neutral tones plus a single accent; generous space around key content and tighter space to group; do not use light grey on white for body text; test on phones; keep primary navigation visible.
- **Bright Avenue (read):** every element needs a reason to be there; two or three core colours plus one accent; one consistent link colour; visitors skim, so use headings, short sections, bullets, and bold or italics for key facts; keep menus short and labels specific; **do not go too minimal or clinical and do not remove content**; keep a sticky header if people need to move around.
- **Medium/PicsRush, JSTOR, Wiley:** could not be read (403 or bot challenge). The saved JSTOR file is script-rendered; its CSS names a design system and a single sans-serif, white ground, grey rules and one blue accent (#3860be). Nothing else can be claimed about these three.
- **Wikipedia, Substack (from general knowledge, not fetched here):** Wikipedia: content visible by default, a lead then an infobox of key facts, plain hairline tables, numbered references, single-pixel heading rules. Substack: one narrow reading column, large calm type, nothing at the sides.
- **dimensions.com (page seen):** a large illustration first, then plainly labelled sections ("Description", "History"), short paragraphs, one hue, one typeface. The collection page I could see is prose-led and has no value table, so what the owner values there is its **calm and clarity**, not a particular table layout. I have not seen an individual dimension page; if that is what the owner means, I need that link.
- **Swiss graphic design (principles):** modular grid, asymmetric layout, flush-left ragged-right text, one neo-grotesque sans (Helvetica or Akzidenz), hierarchy from size and weight alone, thin rules, generous space, objective content, restrained colour (often black, white and one red).

## 3. Themes

1. **Information is primary.** The reader should see the answer without reading prose or operating controls.
2. **Organisation is the thing to get right first.** The owner separates "how info is organized" (valued, book-era and the article iteration) from "style" (to be neutral and subordinate).
3. **Depth on demand.** Complete, exhaustive information must exist but sit behind accordions and popups; the top line carries only the salient figure.
4. **Meaning of every value is explicit.** Who it is for, in which tier, with which source; no jargon; no empty rows; no pseudo-evidence.
5. **Traceability and scholarship.** APA citations, popups, cited-on lists, alphabetical and lens-grouped evidence.
6. **Compact, on-demand controls.** Units and filters are essential but must not consume page space; pills appear only after a lens is chosen.
7. **One disciplined visual system.** Few sizes and weights, one typeface, near-neutral colour, strong section separation, no decoration.
8. **Fit for any screen.** Portrait to landscape, phone to wide desktop, no horizontal scroll, readable tables.
9. **Scope discipline.** Major countries only, current editions only, code values accepted as baselines.

## 4. Conflicts and how each is resolved

| # | Apparent conflict | Resolution |
|---|---|---|
| C1 | "Radically simplify ... fewer pills" vs "a lot more use of accordions and pop-up pills" | Different jobs. Primary answers are never collapsed. Accordions and popups hold depth (jurisdiction detail, basis, citation). Pills exist only as filter options, shown on demand, never as status or decoration. |
| C2 | "I don't want it to look like Wikipedia" vs "wikipedia is very good ... the point is that it is very clearly organized" | Take Wikipedia's organisation (lead, key facts, plain tables, content visible, numbered references), not its skin (blue links, grey panels, contents box, framed tables). |
| C3 | "Previous iteration ... a lot lot better" aesthetics vs "this one ... better data flow" | Combine: previous iteration's look (white, one sans, numbered sections with a heavy rule, sticky section nav, hero value) on the article iteration's information order. |
| C4 | Minimal ("too many AI tropes", "radically simplified") vs "section headers lack weight or real dynamic identification" | Minimal is not flat. Strong, consistent hierarchy is required; identification comes from position, number, rule and weight, not colour tints. Bright Avenue's warning against over-minimalism supports this. |
| C5 | Book era for organisation, Swiss/dimensions/Substack for style | Two layers: information architecture (book-era table-first, value-first) fixed first; visual skin (Swiss grid, one sans, neutral) applied second and held neutral. |
| C6 | Exhaustive comparisons vs "too much page space" and "major countries only" | Exhaustive within scope: one row per major jurisdiction (24), everything else behind the row. Countries outside scope are not shown. |
| C7 | "Far more information" vs "without needing to spend time reading large lengths of texts" | Structured fields (value, unit, when, source) over prose; first sentence only on the surface; full text one click away. |
| C8 | Shopping-style filters vs "too much page space" and "don't show all pills" | Filter facets collapsed behind three lens buttons; applied filters shown as a short removable line; counts shown; results regroup by lens. |
| C9 | Units selector required vs compact controls | Two compact controls (length, slope) plus one filter row; everything else hidden until used. |
| C10 | "Dimensions.com is very simple" vs the page seen being prose-heavy with section pill labels | The shared quality is calm clarity and a visual first. Do not copy its decoration; do copy a clear lead visual and consistent plain section labels. Open question Q3. |

## 5. Tenets (in order of precedence)

1. **Information first.** If an element does not help the reader find or trust a value, remove it.
2. **Answer within the first screen.** The Guidebook value, the common legal range and the start of the comparison are visible with no interaction, on desktop and on a phone.
3. **Organise, then style.** The information order is fixed before any visual choice, and the skin never changes the order.
4. **Salient values large, labels small, prose short.** One idea per line; first sentence on the surface.
5. **One visual system.** One sans-serif family, at most four type sizes, each role using the same size in every section, two weights, black and white plus greys, at most one accent used only for state (active, focus, hit). No decoration: no tiles, status pills, shadows, rounded boxes, gradients, tinted sections, uppercase tracked labels, icons or emoji.
6. **Structure is visible.** Sections separate with space and a rule; each heading is numbered and heavy; a nav shows where you are.
7. **Evidence is binary and traceable.** Recorded or absent. Every figure leads to a citation; every citation lists where it is used.
8. **Scope is explicit.** Major jurisdictions, current editions, T4-T6 values accepted as baselines.
9. **Responsive by structure.** Tables re-flow rather than scroll; touch targets at least 44 px.
10. **Accessible, always.** (Owner, mid-session: "all work must comply with website accessibility standards and best practices.") WCAG 2.2 level AA is the floor, with the cognitive (COGA) guidance the project already adopted in `governance/armature_v3_review.md` §6. Accessibility is a precondition for every other tenet, not a trade-off against them; where a design choice and an accessibility rule conflict, the rule wins.

## 6. Requirements with acceptance tests

**Information architecture (fixed order)**
- R1. Order: title and one-line question; hero of three figures (Guidebook value, most common legal maximum, gentlest); compact units and filter row; 1 Specification (who / value / short basis); 2 Requirements by jurisdiction (master table, then details); 3 Why it matters (bullets); 4 Evidence (APA list); 5 Gaps; 6 About this page. Test: a reader finds the Guidebook value and the 1:12 range with no scrolling at 1280x800 and 375x812.
- R2. Master table: one row per major jurisdiction; columns Preferred, Maximum (and when), Between landings; standard name, edition and verification on a small italic full-width line beneath each row; click a value for the detail popup; sortable by maximum. Test: 24 jurisdictions in scope; none outside scope appear.
- R3. Value tiers: everyone, specific group / ICF / access need, one person; each row says who it is for; rows with no value are not rendered. Test: no row contains "Not set".
- R4. No jargon and no "outside the library" language. Test: text search finds neither.

**Tools**
- R5. Two unit controls (length; slope) apply to every figure, including drawings and popups.
- R6. Filter: three lens buttons in one row; pills only after a lens is chosen and only for that lens; counts on options; applied filters as a removable line; evidence regroups by the chosen lens (population group, ICF chapter, or need).
- R7. Controls block no taller than about 100 px on desktop and landscape phone, and about 190 px on a phone, when collapsed.

**Evidence**
- R8. Evidence is an APA reference list, alphabetical by first author's last name (organisation name for corporate authors); each entry opens a popup with the full citation and the list of pages that cite it, and shows "Cited on" under the entry.
- R9. Why it matters is bullets, one or two short sentences each.

**Visual**
- R10. Type: one sans-serif family (Helvetica/Arial class; no web fonts, no monospace), four sizes with one job each in every section: 56 (36 on phones) page title; 24 section headings, headline figures, the question and dialog titles; 16 all body text, table cells, list items and controls; 13 all secondary text (qualifiers, standard names, captions, labels, table column heads). Weights 400 and 700 only. In tables the value is 16 bold, the row label 16 regular, everything secondary 13 regular. Test: computed styles show one family, at most five sizes and two weights.
- R11. Colour: white ground, black text, two greys, hairline grey rules; no yellow or cream tint anywhere; one accent for state only. Test: at most four text colours; no background tints except a light grey for hit rows.
- R12. Structure: numbered section headings with a heavy top rule and consistent spacing; a sticky nav that marks the current section; consistent hover and focus states.
- R13. Grid: a 12-column grid, flush-left text, asymmetric layout (section titles in a left rail, content in the right nine columns), collapsing to one column below about 760 px.

**Responsive and quality**
- R14. No horizontal page scroll at 375, 768, 812x375, 1024, 1280 and 1920 wide; tables restructure on narrow screens; page length budget about 6,000 px at desktop with details collapsed.
- R15. Accessibility (WCAG 2.2 AA minimum; project standard per `governance/armature_v3_review.md`; prior site audit `audits/accessibility-audit-2026-05-10.md`). Itemised in section 6a. Each item is a pass/fail test and must pass before a page is shown to the owner.

### 6a. Accessibility requirements (testable)

**Perceivable**
- A1. Text contrast at least 4.5:1 (large text 3:1); non-text UI (control borders, focus ring, chart lines) at least 3:1 (1.4.3, 1.4.11). Check light and dark schemes separately.
- A2. No information by colour alone (1.4.1): a pressed filter, active section or highlighted row also changes weight, underline or a marker; any status uses words, not only a symbol.
- A3. Reflow (1.4.10): usable at 320 CSS px with no horizontal scroll of the page; 200% and 400% zoom without loss of content (1.4.4); user text-spacing overrides do not clip (1.4.12).
- A4. Semantics (1.3.1, 1.3.2): one `h1`; headings never skip a level; data in real `<table>` with `<caption>` or an accessible name, `<th scope>`; lists are lists; reading order equals visual order. When a table is restyled for narrow screens, header association must survive (do not hide `thead` with `display:none` without supplying equivalent names).
- A5. Figures and drawings: every SVG has an accessible name and a text equivalent (a short description plus the data as a table or list); drawing text uses real text so the unit selector and zoom work.
- A6. Language (3.1.1, 3.1.2): `lang` on the page and on foreign-language strings (for example the Japanese standard title).
- A7. Honour `prefers-color-scheme`, `prefers-reduced-motion` and forced-colors (no motion is required by the design; transitions off when reduced).

**Operable**
- A8. Everything works by keyboard alone (2.1.1), no trap (2.1.2), logical focus order (2.4.3), visible focus on every control at 3:1 or better (2.4.7, 2.4.13 where applicable).
- A9. Focus not obscured (2.4.11): a sticky nav must not cover a focused element (use `scroll-padding-top` or avoid sticky).
- A10. Skip link to the main content is the first focusable element (2.4.1); descriptive page title and link text (2.4.2, 2.4.4); section nav marks the current section with `aria-current`.
- A11. Target size at least 24x24 CSS px (2.5.8); the design aims for 44 px on touch. No drag-only interaction (2.5.7).
- A12. Dialogs: native `<dialog>` with `showModal`, a visible and labelled close control, Escape closes, focus moves in on open and returns to the invoking control on close; background inert. Content that appears on hover or focus is dismissible, hoverable and persistent (1.4.13); the design uses click, not hover.
- A13. No time limits and no auto-updating content; filter changes announce the result count through a polite live region (4.1.3).

**Understandable**
- A14. Every control has a visible label and a programmatic name; unit selectors are labelled `select` elements; toggle buttons use `aria-pressed`; accordions are native `details/summary`.
- A15. Consistent navigation and consistent identification of repeated components (3.2.3, 3.2.4); no change of context on input.
- A16. Plain language (COGA): short sentences, no unexplained jargon or codes (ICF and need codes are always shown with their names), the same term for the same thing throughout; abbreviations expanded on first use; values always carry their unit and who they apply to.

**Robust**
- A17. Valid HTML; name, role and state exposed for every custom control (4.1.2); no `title`-only information; no ARIA where a native element does the job.

**Verification before sign-off**
- V1. Automated scan (axe-core and Lighthouse accessibility) with zero violations at the sizes in R14.
- V2. Keyboard-only walkthrough of every task: change units, apply and clear a filter, open and close a value popup and a citation popup, expand a jurisdiction.
- V3. Screen-reader spot check (NVDA with Firefox or Chrome; VoiceOver where available) of the master table, a popup and a filtered view.
- V4. 320 px and 400% zoom pass; forced-colors and dark-scheme pass; printed output readable.
- V5. Record results in an accessibility audit file next to this one. Findings are never self-certified as compliant; a "pass" means the specific tests above passed on the date and build recorded.

### 6b. Known accessibility defects in earlier iterations (do not repeat)
- Narrow-screen CSS hid table headers with `display:none`, breaking column-header association for screen readers (A4).
- A sticky section nav with no `scroll-padding` could obscure focused elements (A9).
- Verification was shown with filled and open circles and a tooltip (`title`) only (A2, A17).
- The Japanese standard title had no `lang` attribute (A6).
- The gradient drawing had only an `aria-label`, no text equivalent (A5).
- Dotted-underline button text for values and citations gave a weak, non-standard link affordance and relied on hover (A1, A8).
- None of the iterations has been run through an automated or screen-reader test (V1-V3).

## 7. Where each iteration stands against this

| Iteration | Strengths | Fails |
|---|---|---|
| 1. Original v2 page (own CSS, three typefaces, tiles, pills, 26 type combinations) | Content depth; units; filters; citations | R10, R11, R12; far too long; horizontal scroll at 768 |
| 2. v3 on the site stylesheet (cream, slab and mono) | Section identity; consistent with the site | Owner dislikes the typefaces and the yellow; sizes poor (R10, R11) |
| 3. Neutral version (white, one sans, numbered heavy-rule sections, sticky nav, hero) | Aesthetics the owner preferred; R10-R12 mostly met | Information order and tables less clear than iteration 4 |
| 4. Article version (Wikipedia-like organisation) | Information order, plain tables, content visible: "better data flow" | Skin: blue links, grey panels and boxes, contents box; owner rejected the look |
| 5. Swiss-grid version (built, not yet reviewed with the owner) | Fits R13 | Untested against R1-R15; not yet judged by the owner |

## 8. Decisions needed from the owner before redesign

- Q1. Typeface: is one neo-grotesque (Helvetica/Arial) the intended Swiss reference, or do you prefer another single sans (for example a system UI sans)? A serif body is off the table unless you say otherwise.
- Q2. Accent: Swiss red for state only, a dark blue, or none (black and grey only)?
- Q3. Dimensions.com: the page I saw is a prose-led collection page. Is there a specific dimension page whose value display you want to match?
- Q4. Lead graphic: do you want a drawing under the hero on every spec page (the draft drew the run needed for the same rise at each gradient from the page's own data)? It carries the data visually but needs a data-driven drawing per item.
- Q5. Sticky section nav: keep it (it gives "dynamic identification") or drop it on short pages?
- Q6. Default state of jurisdiction details and evidence notes: collapsed (shortest page) or expanded?
- Q7. Dark mode: required, or ignore for now?

## 9. Process notes (what I got wrong)

- I restyled five times without a fixed requirements baseline, so each pass answered the last remark and undid an earlier one.
- I applied the site stylesheet before checking whether the owner liked it, and treated "Wikipedia is good" as a skin rather than an organisation.
- I gave weight to references I could not read (Medium, JSTOR, Wiley) as if I had; nothing here relies on them except the saved JSTOR file's design-system facts.

## 10. Doctrine alignment (added after reading the mission and project doctrines)

Documents read: `governance/mission-and-epistemics.md` (CANONICAL), `governance/audience-priority.md` (CANONICAL),
`references/project-standards.md` Core Doctrine, `governance/tier-system.md`.

**Owner definition of best practice (stated in session, matches the Core Doctrine rule):** the Guidebook takes no
positions. Best practice is the best way to do something according to how it benefits the intended group, determined by
the evidence hierarchy, not by code consensus and not by what is most common. For a given item and group the page shows
the most accommodating value found (here the gentlest slope, 1:20, which is gentler than Germany's 1:16.7 maximum) and
whether any study or professional body improves on it. Codes are shown as the regulatory minimum for comparison.

Changes made in the page to match:
- Removed "Guidebook position", "working position", "most common legal maximum" and the steepest-slope figure (owner: do not highlight it). The hero shows the best practice found and the gentlest legal maximum.
- Evidence markers are shown on every value row (project rule: unmarked is an error): the symbol plus the words "evidence-based" or "inferred", with a legend; symbol alone is never relied on (accessibility A2).
- Wording follows the specification-language rule (the project is an advocacy project, not a standard-setting body): no "shall be" or "must"; the person tier reads "An occupational therapist's assessment determines the position within the range"; basis lines say what the standards and studies state.
- Values are marked provisional: the best-practice value rests on standards alone (tier 4 to 6), and no higher-tier study sets a value.
- Populations with no evidence stay off the table (owner instruction) but are named in the Gaps section, so the page is not silent about them.
- The page states that no lived-experience (Co-1) evidence on this item is recorded in the library (checked in the database: 0 Co-1 sources linked to the item's evidence base; the library holds 29 Co-1 sources overall, none on ramps or slopes).
- The controls (lens, filters, units) sit above all information, as the owner required. The question line under the title was removed at the owner's direction ("irrelevant"), so this page no longer carries a question at all.

**Tensions between the owner's instructions and the written doctrine (need an owner decision, not silently resolved):**
1. Evidence-state rule says a cell with sparse evidence displays `[BEST-PRACTICE-PENDING]` with a gap link. The owner said rows that are "Not set" should not show. Current handling: no table row, a plain statement in Gaps. Confirm.
2. Doctrine says tier 4 to 6 are a regulatory baseline "walled off from best-practice anchoring" and that a best-practice claim from standards alone is "in error" when it comes from convergence. The owner's rule (best practice is the most accommodating value stated by a current standard unless evidence improves on it) is implemented as a single-source gentlest value, marked evidence-based but provisional, with the basis stated. Confirm this is the intended reading and whether the marker should be inferred instead.
3. The questions-led commitment ("questions are first-class data") is not met on this page: the owner removed the question line under the title as irrelevant, and there is no "questions to ask" content for E-03 in the data (none invented). Confirm how the questions-led doctrine should appear on specification pages.
4. Audience-priority doctrine names four audiences and use-patterns; the site's exemplar `specs/e-08.html` has a "Reading as" lens that changes which sections open by default. It has not been built into this page. The three owner lenses (population, ICF code, access need) are all present. Confirm whether the audience lens is wanted here.
5. Doctrine requires within-population variability as a first-class dimension; the page shows it only through the person tier and group rows. More is possible once data exists.


Control order (owner, 2026-10-29): the Lens row comes first, then its pills when a lens is chosen, then the Units row; all controls sit above all information.
