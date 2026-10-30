# Session handoff: ramp-slope stress test, classification layer, spec page redesign (2026-10-29 to 2026-10-30)

Read this first in the next session. Memory files (`C:\Users\Jordan\.claude\projects\C--Github-guidebook\memory\`) hold the owner's standing rules; this note holds the state of the work.

## 1. What was done (commits on `main`, nothing pushed)
| Commit | Content |
|---|---|
| `9c51ec35` | Ramp-slope pipeline stress test (`audits/stress-test-ramp-slopes-2026-10-29/`); migration 026 and data migration (ICF codes, access needs, population/ICF/need tags, all UNREVIEWED); `spec_page_v2` pilot; repaired `validate_db.py` and `research_protocol_audit.py`; banner on 72 stale spec pages |
| `933e1a46` | Ramp research batch: 12 studies + Sanford 1997, Rooney 2021 (UNVERIFIED-1, abstract-level), IE TGD M 2022 and SG Code 2025 rows; first `spec_page_v3`; E-03 page; removed old `site/specs/e-03.html` |
| `525a2083` | v3 generator rebuilt (Swiss grid, accessibility pass), best-practice content, design requirements, partial accessibility audit |
| `71e70edd` | Persona fixes (parameter table, my-jurisdiction selector, clause/tier/source link, evidence details, plain-language line), fixed column widths, navigation legibility, alphabetical jurisdictions, defects audit |
| this commit | Spec pages consolidated into `site/specs/`; wording corrected to the owner's definitions; this handoff |

## 2. Owner definitions and decisions (authoritative; see memory `spec-page-requirements.md`)
- Best practice = the best way to do something for the intended group; it is NOT the most common value. The gentlest/most accommodating value found in practice IS best practice; no academic study is required. The Guidebook takes no positions.
- Provisional = the source must be re-read to confirm accuracy; it is a stage. "Covered" = listed source read, extracted and verified (currently 0 verified).
- Current editions only. T4-T6 values are accepted as given; do not hunt for their derivation.
- Scope: P1+P2+P3 jurisdictions only (US UK AU CA DE NO SE ISO EU; FR CH NL DK FI BE IE ES IT PT; JP SG NZ KR CN).
- Two lenses: audience (designer, disabled person, OT, policymaker) and disability (population, ICF code, access need). Only the disability lens is built.
- Controls sit above all information. Evidence and jurisdictions are alphabetical (bibliography by last name). No "Not set" rows. No "outside the library" evidence.
- Design: Swiss grid, one sans typeface, four sizes (13/16/24/56), black/white/grey, red for state only, accessible (WCAG 2.2 AA minimum, project standard). Minimalism must not cost navigation legibility. Pills are fine if judicious.
- Pages should render directly from the database in the ideal state.
- Tier numbering: `governance/tier-system.md` (2026-05-25) governs.

## 3. Where things are
- Generator: `scripts/generate/spec_page_v3.py` (reads `data/guidebook.db` + `data/spec_pages/<ITEM>.json`; writes `site/specs/<item>.html`). Run: `python -X utf8 scripts/generate/spec_page_v3.py E-03`. Only E-03 has a data file.
- Requirements and audits: `audits/spec-page-design-requirements-2026-10-29.md` (themes, tenets, R1-R16, doctrine alignment, owner answers section 12), `audits/spec-page-design-defects-2026-10-30.md` (defects, persona walkthrough, status J), `audits/accessibility-audit-spec-page-v3-2026-10-30.md` (what was and was not tested), `audits/research-batch-ramp-slopes-2026-10-29/findings.md`.
- Migrations: `scripts/migrations/026_classification_codes.sql` and the three `data_2026102*`/`data_2026103*` files; generators in `scripts/db/`.
- All spec pages now live in `site/specs/`; `specs/` at the root no longer exists; `index.html` links the e-08 exemplar at `site/specs/e-08.html`.

## 4. Open work, in suggested order
1. **Rest landings.** Owner hypothesis: the E-03 problem is the missing rest landing, not slope. Documents: the book spec pairs 1:20 with a 9 m max run and a 1500x1500 mm rest platform (GAP-016: unsourced); codes differ (DE 6 m; SG 6 m at 1:12 to 15 m at 1:20; UK/IE 500 mm rise per flight; US/JP/NZ about 750 mm; CA/ES about 9 m); UK/IE text says a high total rise is tiring even with rests; Hashizume 2015 shows effort rising with distance. Proposed: make rest-landing spacing a second headline parameter (hero, drawing, values table). Owner confirmed (2026-10-30): do this first in the next session.
2. **Render contract and database-direct rendering.** `source_value_extractions`, `evidence_cell_state`, `convergence_assessment` are empty; no specification/jurisdictional-value table; the page values are hand-typed in `E-03.json`. Write the render contract (page element to required data to table), add the missing schema by migration, move E-03's data in, make the generator read the DB, and add a per-item parameter schema (which direction is more accommodating, units, columns).
3. **Verify the readings.** All 15 jurisdiction readings are provisional and need a second review against the source. Not yet read: Belgium, Denmark, EU, Finland, Italy, Netherlands, Portugal, South Korea, Sweden. Blocked or missing: CN clause 3.4 (translation omits it), NZ D1/AS1 (host blocks downloads; a mirror exists), CA NBC 2025 free text, AU AS 1428.1 (paywalled), NO/SE official pages (404 on the URLs tried), UK BS 8300 (paywalled). Library rows exist for IE and SG only; none for the UK AD M source or the others.
4. **Audience lens** (e-08 "Reading as" semantics) on the v3 page.
5. **Doctrine decision record (D-DOCT)** for "gentlest value in practice is best practice" versus the mission document's tier 4-6 wall; mark the stale tier line in `references/project-standards.md` (line 17).
6. **Accessibility tests still missing:** third-party scan (axe-core or Lighthouse; loading axe from a CDN in the page was blocked, so use a local install with the owner's approval), screen reader, forced colours, 400% zoom, print, keyboard walkthrough of the new jurisdiction links.
7. **Defects still open (defects audit section J):** landscape-phone first screen; hero and title on a different left edge from section content; citations not fully APA; same value repeated; page length (about 8,100 px desktop).
8. **Other pages:** 87 old-design pages remain in `site/specs/`. Applying v3 needs steps 2 and the per-item schema.
9. **Data defects:** REF-00388 title carries a curation note (cleaned at render only); REF-00375 and REF-00078 author fields; REF-00074 URL points to the 2019 PDF; 10 of 16 evidence entries not VERIFIED; 9 lack a DOI; 224 of 640 sources untagged; ICF and access-need vocabularies (mine) unreviewed; `validate_db.py` reports C4 FAIL (31 connections with 0 targets) and C5 WARN; 1,883 rule-7 findings.
10. **Doctrine gaps on the page:** no lived-experience (Co-1) evidence for E-03 (29 Co-1 sources exist, none on ramps); questions-led commitment unmet (the owner removed the question line); within-population variability barely shown.

## 5. Practical notes
- Windows: use `python -X utf8`; Bash mangles backslashes (use the Edit/Write tools for code with backslashes); delete `data/guidebook.db-shm` and `-wal` after read-only opens.
- Testing pages: serve the repo with `python -m http.server 8765 --bind 127.0.0.1` and open it with the browser pane's `preview_start` (file:// views cannot load relative CSS; navigating the pane directly to localhost can be denied). Stop the server afterwards.
- Untracked files `_tmp_claims.txt` and `_tmp_schema.json` pre-date this work and were deliberately left uncommitted.
- Workflow: solo repo, work on `main`, commit only when asked, serialize heavy multi-agent runs.

## 6. Suggested opening for the next session
"Read `sessions/session_2026-10-30-spec-page-handoff.md` and the memory index. Start with the rest-landing headline parameter on E-03 (open item 1), then the render contract (item 2)."
