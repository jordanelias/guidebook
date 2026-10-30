# Accessibility test record: spec page generator v3, page E-03

Status: SELF-AUTHORED, PARTIAL. This records what was actually tested on `specs/e-03.html` as built by
`scripts/generate/spec_page_v3.py`, against the testable items in
`audits/spec-page-design-requirements-2026-10-29.md` section 6a. It is not a compliance certificate. No third-party
scanner (axe-core, Lighthouse, pa11y) and no screen reader has been run (see "Not tested").

Method: the page was served from a local web server and driven in the Claude desktop app's browser pane. Checks were
scripts I wrote and ran against the live DOM, plus real key presses for the keyboard test. An attempt to load axe-core
from a public CDN into the page was blocked by the permission system, and I did not work around that.

## Passed (build of 2026-10-30)

| Item | Result |
|---|---|
| A1 text contrast (own calculation of computed colours, light and dark) | 0 failures at 320, 375, 1280 wide and in the dark scheme; text colours used: 2 |
| A3 reflow | no horizontal page scroll at 320, 375, 732, 812x375, 1024, 1280, 1920 wide |
| A4 semantics | one h1; no skipped heading levels; every table has a caption and scoped headers; tables carry explicit ARIA roles so the narrow-screen layout keeps header association (column headers are visually hidden, not removed) |
| A5 drawing | the drawing's labels and values are real HTML text; the triangles are decorative (`aria-hidden`); the figure has a caption |
| A6 language | `lang="en"` on the page; Japanese and Chinese text runs are wrapped in `lang="ja"` / `lang="zh"` (checked: none without) |
| A8 keyboard | skip link is the first focusable element and shows a visible focus ring; Enter on a value button opens the dialog; focus moves into the dialog and stays inside it; Escape closes it; focus returns to the opening button |
| A10 | skip link present; section nav uses `aria-current`; `scroll-padding-top` set under the sticky nav (A9) |
| A11 target size | no interactive element under 24 px; the measured minimum height for buttons and selects is 32 px, 44 px on narrow screens |
| A12 dialogs | native `<dialog>` with `showModal`; `aria-labelledby` points at an existing heading when open |
| A13 live region | filter changes and table sorting are announced through a polite live region (verified the text is set) |
| A14 labels | 0 controls without an accessible name; unit selects are labelled; lens buttons use `aria-expanded`/`aria-controls`; filter options use `aria-pressed` |
| Duplicate IDs, broken ID references | none |
| Type system | one family, four sizes (13, 16, 24 and a 56 or 36 title), weights 400 and 700; every section uses the same sizes for the same roles |

## Defects found and fixed during testing
- Sort button under 24 px high: given a 32 px minimum height.
- Dialog `aria-labelledby` pointed at headings that did not exist until opened: now set on open.
- Dialog focus landed on an unnamed scroll container: focus now goes to the dialog heading; the scroll region is named.
- Drawing text shrank to about 5 px on a phone (whole SVG scaled): figure rebuilt with HTML text.
- Page length 9,100 px at desktop (budget about 6,000): evidence notes, gaps and per-jurisdiction details collapsed by default; now about 6,030 px.

## Not tested (do not assume these pass)
- A third-party automated scan (axe-core, Lighthouse, pa11y): blocked or not installed.
- Any screen reader (NVDA, JAWS, VoiceOver) on the table, popups, filters and figure.
- Forced-colors mode (rules written, not exercised) and Windows high contrast.
- 400% browser zoom and user text-spacing overrides (the 320 px width check is a proxy for reflow only).
- Print output.
- Touch behaviour on real devices.
- The actual font that renders: the stack is Helvetica Neue, Helvetica, Arial, Liberation Sans, so Windows machines show Arial.

## Next step before the page is shown as accessible
Run an automated scan and a screen-reader pass (V1 and V3) and record the results here; leave this file's status as
PARTIAL until both exist.
