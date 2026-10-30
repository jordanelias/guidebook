# Handoff: rebuild the ramp-slope and spec-page work on current `main` (written 2026-10-30)

**For a new session started from GitHub `main`.** Read this file first, then `CLAUDE.md` (rules 0-9 bind you), then `/orient`.
Everything the previous session produced is either in this folder or on the branch `ramp-spec-pages-work` (see section 2).
The owner has instructed: **"you have to rebuild it for main."** This file is the brief for that rebuild.

Rule 7a applies to this file: every count and state below was measured on 2026-10-30 against `main` at `599cf40b`.
Re-derive before relying on any of them.

---

## 1. What happened and why a rebuild is needed

A previous session ran a stress test of the pipeline on one item (E-03, ramp gradient / slope), added a research batch, a
classification layer, and built a static spec page with a generator. It worked on a local checkout whose base was
`be7bc576` (2026-06-24). `main` is 2,203 commits ahead of that base. Between the two:

- **The render apparatus was deleted** (`ea8b9635`, RULINGS R1, 2026-10-14): the owner's target is **dynamic rendering from the
  database** (LED-103, LED-104). `site/`, `specs/`, `scripts/generate/{build_site,spec_page,...}.py` no longer exist on `main`.
  The previous session's static generator (`spec_page_v3.py`) therefore must **not** be restored as-is.
- **The database was restarted.** The old working DB had 640 sources; `main`'s `data/guidebook.db` has 53 `evidence_sources`
  (max `REF-01032`), 101 `source_value_extractions`, 8 `specifications`, 10 `base_parameters`, schema version 116, tables
  `evidence_sources`, `source_value_extractions`, `specifications`, `base_parameters`, `parameter_declinations`,
  `specification_source_links`, `base_icf`, `access_needs`, `access_need_icf`, `identity_icf_map`, and others.
- **`main` already has its own ramp work**: data migration `data_20261010002423_2026-10-09-research-batch-24-parameter-pilot.sql`
  (a ramp-gradient parameter pilot citing REF-00992 (UK Approved Document M), REF-00996, REF-01002, REF-01005, REF-01008).
  **Compare before adding anything**; do not duplicate (rule 5: point, do not copy).
- The old migrations numbered `026` and `data_202610290...-030...` **collide with `main`'s migration history and must never
  be run against `main`'s database.** They are kept here only as inert `.txt` reference files.

So the previous work cannot be merged; its **content** has to be re-expressed in `main`'s schema and rules.

## 2. Where the previous work lives

| Thing | Location |
|---|---|
| This folder | `workplan/2026-10-30-ramp-spec-pages/` on `main` (after the handoff PR merges) |
| Full previous work, 7 commits, old base | branch `origin/ramp-spec-pages-work` (tip `1165366f`) |
| Raw session transcript (17.5 MB) | **not in git.** On the owner's computer only: `C:\Users\Jordan\.claude\projects\C--Github-guidebook\d9505991-620e-4974-95b2-b407384c5793.jsonl`. Copying it into the repo was blocked by the tool permission check. |

To read anything from the branch: `git fetch origin ramp-spec-pages-work` then `git show origin/ramp-spec-pages-work:<path>`.
Most useful paths there that are NOT copied into this folder: `scripts/generate/spec_page_v3.py` and `spec_page_v2.py` (the static
generator, reference for layout and accessibility decisions only), `site/specs/e-03.html` (the rendered pilot page),
`site/specs/e-08.html` (hand-built exemplar), `scripts/db/build_ramp_batch_migration.py` and `..._2_...py` (builders for the
research rows), `sessions/session_2026-10-30-spec-page-handoff.md` and the `sessions/2026-10-30-ramp-spec-pages-archive/` index.

Folder contents here:
- `reports/` : requirements and design analysis (R1-R16, owner answers in section 12), defects and persona walkthrough,
  partial accessibility record, research-batch findings (ramp), stress-test report.
- `data/E-03.json` : the hand-staged page content (16 jurisdiction readings, 16 evidence refs, values, plain-language text).
- `data/old-migrations-reference-only/*.txt` : the previous classification and research-batch SQL, as text so no runner picks them up.
- `owner-rules/` : copy of the owner's memory notes from the previous workspace (standing rules; may overlap `main`'s `CLAUDE.md`, which wins on conflict, except where a newer owner statement below says otherwise).

## 3. Owner definitions and directives (authoritative; from the owner in chat, 2026-10-29/30)

- **Best practice** = the best way to do something for the intended group. It is NOT the most common or most agreed value.
  The **gentlest / most accommodating value found in practice IS best practice**; no academic study is required. The Guidebook
  takes no positions. Do not highlight the steepest slope a code allows. (1:20 is gentler than Germany's ~1:16.7.)
- **Provisional** is a stage: the source must be re-read and the information confirmed. **Covered** = the listed source was read,
  extracted AND verified. At the time of writing, 0 readings were verified.
- **Scope of jurisdictions**: P1+P2+P3 only: US UK AU CA DE NO SE ISO EU; FR CH NL DK FI BE IE ES IT PT; JP SG NZ KR CN. Major
  identified countries only on the page.
- **Current editions only**; no history. T4-T6 values (e.g. 1:12) are accepted as baselines; do not hunt for their research.
  Tier numbering: `governance/tier-system.md` (2026-05-25).
- **Methodology**: the rigor belongs in synthesis, adjudication and specification, not evidence collection.
- **Evidence is binary**: recorded in the library or not. No "outside the library".
- **Item pages and the book's specifications are the same idea**: the correct way to design something.
- **Pages should render directly from the database** (matches R1/LED-103).
- **Two lenses**: an AUDIENCE lens (designer, disabled person, OT, policymaker) and a DISABILITY lens (population, ICF code,
  access need). Only the disability lens was built before.
- **Page design requirements** (full list in `reports/spec-page-design-requirements-2026-10-29.md`): controls above information;
  master comparison table with the standard's name as a small italic line under each row; value click opens detail; no "Not set"
  rows; jurisdictions alphabetical; evidence alphabetical by last name, grouped by lens; filters collapsed with pills only after a
  lens click; Swiss-grid look, one sans typeface, four sizes, no AI tropes; unit selector; APA references that open a popup with
  "cited on" lists; ●/○ evidence markers mandatory; WCAG 2.2 AA mandatory and wins over aesthetics; navigation legibility
  must not be sacrificed to minimalism. **Never self-certify accessibility.**
- **Owner hypothesis on E-03**: the problem is the lack of a rest landing, not the slope. The owner approved making rest-landing
  spacing a second headline parameter (best-practice value found so far: Germany 6 m, provisional, secondary source).
- **Persona questions the page must answer**: can an architect find the values; a policy writer find precedents and code bodies;
  a therapist/researcher find evidence; a person with a disability navigate the page.
- **Workflow**: PRs are allowed; the owner only objects to needless GitHub pinging (CLAUDE.md rule 9: open the PR once, last;
  unsubscribe immediately; do not poll). Commit and push only when asked.

## 4. What is worth carrying into `main`

Already in this folder as reports/data. To be re-expressed through `main`'s own mechanisms (migrations via
`scripts/emit_data_migration.py` and `scripts/migrate_db.py`; `scripts/db.py add-source`; never write the DB directly, rule 3):

1. **Research rows.** 14 library source ids appear in the old batch SQL (`REF-00738`..`REF-00751`; the studies on ramp slope, energy
   cost and ramp use, plus Sanford 1997, Rooney 2021 (abstract-level only, UNVERIFIED-1), IE TGD M 2022 and SG Code 2025). Their
   content is in the old batch SQL (`data/old-migrations-reference-only/data_20261030003751_*.txt` and `..004524_*.txt`)
   and findings in `reports/research-batch-ramp-slopes-2026-10-29__findings.md`. On `main` they need **new REF ids** from
   `add-source`, and dedupe against the 53 existing sources first. Tags in the old DB (population, ICF, access need) were all
   UNREVIEWED automated tags: do not present them as verified.
2. **Jurisdiction readings** (the 16 entries in `data/E-03.json`: preferred/max slope, landing, width, handrails, cross-slope,
   clause, standard, edition, tier, source URL). These belong as `source_value_extractions` rows linked to
   `specifications`/`base_parameters` in `main`'s schema, with locators, following `main`'s extraction conventions (check
   the 101 existing rows and the batch-24 pilot first). All are PROVISIONAL (read once, unverified).
3. **Classification vocabulary** (ICF codes, access needs). `main` already has `base_icf`, `access_needs`, `access_need_icf`,
   `identity_icf_map`. **Do not re-add the old 026 tables.** Diff the old vocabulary (in `...classification...txt`) against what
   `main` has and propose only genuine additions; the old vocabularies were authored by the previous session and never reviewed
   by the owner.
4. **Findings that bear on method**: stress-test report, defects, requirements analysis. Read before designing.
5. **Validator and audit-script repairs** done on the old base (`scripts/validate_db.py`, `scripts/audit/research_protocol_audit.py`)
   do not apply: `main` has its own check registry. Do not port them.

## 5. Suggested plan for the rebuild session

1. Orient: `bash .claude/hooks/ensure-deps.sh`, `/orient`, read `CLAUDE.md` sections 1-3 and 7, `governance/tier-system.md`.
   Derive the current ramp footprint with `db-census`/`repo-sweep` (batch-24 pilot rows, existing ramp specification, existing
   `base_parameters` for gradient).
2. Decide with the owner the open questions in section 6 before writing rows.
3. Ingest the missing sources (dedupe, new REF ids, tags marked unreviewed) through the sanctioned CLI; one data migration.
4. Add the jurisdiction readings as `source_value_extractions` (provisional), pointing at sources by id, not copying text (rule 5).
5. Add rest-landing spacing as a second parameter if the schema allows (`base_parameters` row via migration; direction rationale
   column exists). Best-practice direction: the gentlest found.
6. Dynamic rendering: write the **render contract** (page element → required data → table) per the contract/traceability
   invariant before any HTML. Check what LED-103/LED-104 and the owner browser page (`governance` commit `838d9889`, a read-only
   phone view of every table) already provide; reuse it rather than rebuilding a generator. Port the page design requirements
   (section 3) to whatever renders from the database.
7. Gate once at the end: `scripts/preflight.sh`, then commit with `{skill}: {action} [YYYY-MM-DD HH:MM]`, open one PR, unsubscribe.
   Add `attestations/<slug>.json` if you touch `sessions/` or `decisions/` (rule 2).

## 6. Open decisions for the owner (ask once, early)

- Does dynamic rendering already exist enough to host the page (owner browser page), or is a new renderer wanted? R1 says the
  committed static apparatus was removed because it no longer ran.
- Doctrine conflict: the mission document walls off T4-T6 evidence from "best practice", while the owner now says the gentlest
  value in practice is best practice. A decision record (D-DOCT) is needed (rule 0: the live owner statement wins, record the
  supersession; naming it is on you). Also `references/project-standards.md` line ~17 carries a stale tier line (check it still exists).
- Which jurisdictions' sources to read next. Not yet read: BE, DK, EU, FI, IT, NL, PT, KR, SE. Blocked or missing: CN clause 3.4
  (translation omits it), NZ D1/AS1 (host blocks downloads; a mirror exists), CA NBC 2025 free text, AU AS 1428.1 (paywalled),
  NO and SE official pages (404 on URLs tried), UK BS 8300 (paywalled).
- Build the audience lens (four audiences) alongside the disability lens.
- No lived-experience (Co-1) evidence for ramps exists in the old library (29 Co-1 sources, none on ramps); the page must say so
  (Co-1 gap statement) until sourced.

## 7. Known defects and gaps in the previous work (do not repeat)

- Provisional and unverified readings: all 15 jurisdiction readings; 10 of 16 evidence entries not VERIFIED; 9 lack a DOI.
- Accessibility **not** established: no third-party scan (axe/Lighthouse), no screen reader, forced-colours, 400% zoom, print or
  touch tests. Own contrast/keyboard/reflow checks passed on the old page; that is not compliance.
- Page defects left open: landscape-phone first screen; hero edges vs rail; citations not fully APA; same value repeated; length.
- Data defects in the old library: REF-00388 title carried a curation note; two author fields; one URL pointed at a 2019 PDF.
  Mapping to `main`'s library may or may not carry these over: check, do not assume.
- Old DB validators reported a pre-existing C4 failure (31 connections with no targets); not necessarily true of `main`.

## 8. Practical notes (Windows / this repo)

- Use `python -X utf8`. Heredocs with complex quoting fail in Bash on Windows: write scripts with the Write tool.
- Test pages by serving over `python -m http.server` and opening with the browser pane's `preview_start` (file:// cannot load
  relative CSS); stop the server and reset the viewport afterwards.
- Use `git ls-files` / the Grep tool carefully: CLAUDE.md notes `.ignore` hides files from the Grep tool.
- Heavy multi-agent runs trip throttling and spend caps; serialize them.
- Untracked scratch files `_tmp_claims.txt`, `_tmp_schema.json` exist only in the owner's old checkout; ignore.

## 9. Suggested opening prompt

"Read `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md`, then CLAUDE.md. Rebuild the ramp-slope and E-03 work on main per section 5.
Start by deriving what main already holds for ramp gradient, then ask me the section 6 questions in one batch."
