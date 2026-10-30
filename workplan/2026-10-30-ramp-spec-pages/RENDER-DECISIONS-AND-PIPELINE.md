# Render decisions from the 2026-10-29/30 ramp session, reconciled against `main`

Written 2026-10-30. **Source:** `session-export-1793395272333.zip` (owner's Windows session `d9505991-…`, titled "Research pipeline stress test: ramp slopes"; its two transcript files are byte-identical). **Reconciled against:** `main` at `cea708e`.

**Scope (owner, 2026-10-30):** only the decisions made about rendering, and how each bears on the pipeline. Not the research rows, the classification vocabularies or the static generator; the first two are already in this folder as inert reference, and the third is not to be restored (RULINGS R1).

**Status (updated after implementation, same day):** the owner's statements are now recorded in `references/project-standards.md`, "Owner rulings 2026-10-30 — best practice, the specification page and rendering" (cited below as *ledger 2026-10-30*, with its item number). The state column is revised accordingly. Three claims in the first version of this file were wrong and are corrected in section 7.

**Reading rule.** The export was produced on a checkout based on `be7bc576`, 2,203 commits behind `main`. Every "the database is empty / the table does not exist" statement in it described that old database and is **not** a statement about `main`. Counts here are commands (CLAUDE.md rule 7a); re-run them.

```
python3 - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
print(c.execute('pragma user_version').fetchone())
for t in ('specifications','source_value_extractions','specification_source_links','base_parameters','evidence_sources'):
    print(t, c.execute(f'select count(*) from {t}').fetchone()[0])
print(c.execute('select accessibility_direction, count(*) from base_parameters group by 1').fetchall())
PY
```

---

## 1. Verdict

1. **The owner's rendering decisions were on `main` only as handoff text** (`HANDOFF.md` §3 and `reports/spec-page-design-requirements-2026-10-29.md` §§1–12), which no future session is directed to read. They are now a ledger entry with a CONDITION/ACTION pair, which is the repository's binding form (CLAUDE.md rule 0).
2. **What is not on `main`:** (a) the mapping from each rendered element to the pipeline stage that must supply it, and to a `main` table where one exists (§3 below); (b) the session's own list of concerns and confusions about generalising the pilot page (§5); (c) the export's reading of what the pilot *implies for earlier stages* (§4).
3. **Two of the export's blockers are gone on `main`.** The export found no per-parameter direction of "more accommodating" and no table able to hold jurisdiction readings. `main` has `base_parameters.accessibility_direction`, and `source_value_extractions` carries `jurisdiction`, a value, a unit and `loc_*` locator columns. Whether they are *populated enough* is the open question, not whether they exist (§3).
4. **One export decision conflicts with `main`'s ruling and is not carried:** a committed static generator emitting committed HTML. RULINGS R1 (owner-quoted LED-103/LED-104: "the entire pipeline is dynamic rendering on site", "do not rely on artifacts for rendering the site") deleted that class of apparatus, and owner ruling OW-1 (2026-10-29, third) then specified a **render table** in the database holding specification rows as prose. The export's *requirements* survive; its *mechanism* does not.
5. **The "doctrine conflict" the export called D-DOCT is largely already resolved on `main`.** See section 7, correction 1.

## 2. Decisions about rendering, by pipeline stage

Spine: `base -> research -> evidence -> judgment -> synthesis -> specification -> render` (`governance/pipeline-contract.yaml`). "On main" = already recorded in the repository in a form that binds; "Handoff only" = recorded in this folder but not yet in any binding record; "Conflicts" = see the note.

| # | Decision (owner unless marked) | Stage it binds | State against `main` |
|---|---|---|---|
| D1 | Pages render directly from the database; the page is one view plus one renderer | render | **On main**: RULINGS R1, refined by OW-1 (render table in the database; ledger 2026-10-29 third, item 9). Export agrees; ledger 2026-10-30 item 3. Renderer still **NOT-BUILT** (STATE-GRAPH P-K, CAPABILITIES C4.6) |
| D2 | Item pages and the book's specifications are the same idea: *the correct way to design something* | specification → render | Ledger 2026-10-30, item 3 |
| D3 | **Best practice = what benefits the intended group most; the gentlest/most accommodating value found in practice is best practice; no academic study required; the Guidebook takes no positions; never highlight the steepest value a code allows** | specification | Ledger 2026-10-30, item 1. **Not a conflict on the reading recorded there:** Option A (2026-07-21) already states a T4–T6-only determination as weak-band (○) "best practice as currently known", flagged. The owner's statements decide *which value* is named; the band and flag are unchanged. No `SUPERSEDES` line written. **Owner confirmed the reading** (ledger 2026-10-30 second: "Yes, keep the ○ band and flag") |
| D4 | Code values (T4–T6) are accepted as baselines; do not hunt for the research behind them; current editions only, no history | research, evidence | Ledger 2026-10-30, item 1. Consistent with OR-20 (2026-10-29) and with `main`'s `code_floor_only` / `regulatory_stratum_only` flags |
| D5 | Evidence is binary: recorded in the library or not; no "outside the library" language | evidence → render | Ledger 2026-10-30, items 2 and 9 (wording only; no new check) |
| D6 | **"Provisional" is a stage** (source must be re-read and the information confirmed). **"Covered"** = source listed, read, extracted *and verified*. Page says "read, none yet verified" until that is true | judgment → render | Ledger 2026-10-30, item 2. Matches `main`'s `specifications.state` (`pending`/`provisional`/`stated`) and `has_unverified_sources` |
| D7 | Value tiers: **universal / population-ICF-need-specific / person-specific**; "ALL" means universal; each value row says whom it is for; rows with no value are not rendered | specification → render | Tiers: `specifications.design_scale`. Rows: ledger 2026-10-30, item 9(a), **read as compatible** with the pending-cell doctrine (no row; gap stated under Gaps); owner to confirm |
| D8 | Two lenses: an **audience** lens (designer, disabled person, OT, policymaker) and a **disability** lens (population, ICF code, access need) | render (presentation) | Ledger 2026-10-30, item 4. Audience lens has doctrine (`governance/audience-priority.md`) but no data and has not been built |
| D9 | Lens filtering: three lens buttons, pills only after a lens is chosen, results regroup by the chosen lens; controls above all information; units control below the lens row | render | Ledger 2026-10-30, items 4 and 5 (presentation; no pipeline effect) |
| D10 | Master comparison table: one row per in-scope jurisdiction, alphabetical; standard name, edition, tier, read level on a small full-width line; value click opens detail; sortable | render, fed by evidence | Ledger 2026-10-30, item 5 |
| D11 | Jurisdiction scope for pages = P1+P2+P3 only (US UK AU CA DE NO SE ISO EU; FR CH NL DK FI BE IE ES IT PT; JP SG NZ KR CN); "buckets 1 and 2" was read as P1+P2+P3 | research → render | Ledger 2026-10-30, item 7 |
| D12 | Unit selector on every page (metric/imperial; % / ratio / degrees); unit tokens converted client-side | render | Presentation only; needs a per-parameter unit family (§3, E9). Not in the ledger entry: the owner's statement is in the working requirements only |
| D13 | Evidence list: APA, alphabetical by first author's last name (organisation name for corporate), grouped by the active lens; each entry opens a popup with the full citation and a *cited on* list | evidence → render | Ledger 2026-10-30, item 5 |
| D14 | ●/○ markers mandatory on every specification value; "unmarked is an error" | specification → render | **On main**: CLAUDE.md §6, `specifications.marker`. **Resolved by tier-system §8 / Option A:** a determination resting on T4–T6 alone takes ○ at determination level (◐ only for an individual T4/T5 citation in an anchored cell). The export's ● is not carried (ledger 2026-10-30, item 1) |
| D15 | A page states its Co-1 (lived-experience) position explicitly; for ramp gradient, none recorded | evidence → render | On main as doctrine (CLAUDE.md §6). The page-level statement is Handoff only |
| D16 | Accessibility: WCAG 2.2 AA is a precondition and wins over aesthetics; navigation legibility is never traded for minimalism; **never self-certify** compliance | render | Ledger 2026-10-30, item 6 (requirements A1–A17, V1–V5, R16 in the working file). Nothing on `main` checks it: no render surface exists to check |
| D17 | Visual system: one sans typeface, four sizes, two weights, white/black/grey, one state-only accent, Swiss grid, no decoration. *Content organisation is fixed first; style is applied second and held neutral* | render (presentation) | Ledger 2026-10-30, item 5, as a working baseline. The earlier site stylesheet it rejects (cream/slab/mono) is gone with the site; `main` has no design system to conflict with |
| D18 | Owner hypothesis: for E-03 the problem is the **lack of a rest landing**, not the slope; add landing spacing as a second headline parameter (shortest run between rests found = Germany 6 m, secondary source, provisional) | research → specification → render | Ledger 2026-10-30, item 8 (hypothesis and "yes"); the parameter itself is a data PR not yet made. Export's research is unverified here (§6) |
| D19 | The question line under a page title is irrelevant and was removed | render | Ledger 2026-10-30, item 9(b), **read as not repealing** the questions-led doctrine; left to the owner |
| D20 | Methodology lives in synthesis/adjudication/specification, not in evidence collection | judgment → specification | Ledger 2026-10-30, item 1 (`owner-rules/methodology-lives-in-synthesis.md` is the memory note) |

## 3. Render contract against `main`'s schema

The export's closing proposal was a **render contract** mapping each page element to the data it needs (existing table / missing table / manual), before any HTML. None was written. This is a first pass from `PRAGMA table_info`, not a built or tested contract. **[ASSUMPTION: column semantics read from names and the CHECK clauses seen, not from writer code.]**

| # | Page element | Supplying stage | Where it is on `main` | Status |
|---|---|---|---|---|
| E1 | Headline best-practice value (+ unit) | specification | `specifications.value_min/value_max/value_unit`; direction from `base_parameters.accessibility_direction` | Columns exist. Direction is NULL for most parameters (derive with the command above); gradient has a direction and `provisional` rows |
| E2 | ●/◐/○ marker | specification | `specifications.marker` | Exists; D14 unresolved |
| E3 | Value tier (universal / group / person) | specification | `specifications.design_scale` | Exists |
| E4 | Whom a value is for (lens) | judgment → specification | `identity_code`, `icf_code`, `needs_code`, `medical_code` on both `specifications` and `source_value_extractions` | Exists. Vocabularies: `base_taxonomy_identity`, `base_icf`, `access_needs`, `access_need_icf`. **Do not re-add the export's `population_icf_map` / `source_*_tags` tables** (HANDOFF §4.3) |
| E5 | Jurisdiction master table (value, clause, edition, source link) | evidence | `source_value_extractions.jurisdiction`, `claimed_value/unit`, `loc_*`, `ref_id` → `evidence_sources.standard_number/edition/url/tier/verification_status/code_currency_status` | Exists. Gradient rows cover many jurisdictions; **read level and "verified" per row** must come from `extraction_status` and `verification_*`, not a hand label |
| E6 | Per-jurisdiction secondary parameters (landing, width, handrails, cross-slope) | evidence | Needs a `base_parameters` row each, then extractions | **Missing as parameters** unless minted; only the gradient parameter has extractions |
| E7 | Rest-landing spacing as a second headline | research → specification | As E6; direction rationale lives in `base_parameters.direction_rationale` | Missing; needs owner confirmation of D18, then a migration |
| E8 | Evidence list, APA, cited-on | evidence | `evidence_sources` bibliographic columns; cited-on from `specification_source_links.ref_id` and `source_value_extractions.ref_id` | Exists; no page-level "cited on" view found |
| E9 | Units (slope %, ratio, degrees; length) | render | `value_unit` per row | A unit *family* per parameter is not recorded as far as the columns read show. **[UNVERIFIED]** whether a vocabulary exists |
| E10 | Evidence regrouped by lens | evidence | Only through extractions' lens columns | **Gap:** a source with no extraction has no lens. The export's healthy-volunteer studies would vanish under population filtering (its concern 9) |
| E11 | Gaps section; Co-1 statement | research / evidence | `gaps`; `evidence_sources.co1_provenance` | Exists; statement must be derived, not typed |
| E12 | "Why it matters" bullets; plain-language line | synthesis | No table found | **Not yet built.** OW-1 (2026-10-29, third) rules that a render table in the database holds specification rows as complete prose with bibliographic information drawn from the preceding tables; OW-1b (how the prose is produced) and OW-1c (stored or rebuilt) are unanswered. OPI-229's Opus floor attaches to the prose (RULINGS R22) |
| E13 | Read-only "state of every table" browser | all | `scripts/generate/owner_browser_build.py`, `governance/owner-browser.yaml` | **Exists, committed, and is the only renderer on main.** Not a spec page; HANDOFF §6 asks whether it can host one |
| E14 | Audience lens ("reading as…") | render | `governance/audience-priority.md` only | Presentation + doctrine; no data |

Contract invariant that governs all of it (owner memory, `owner-rules/contract-traceability-invariant.md`): every hand-off at every boundary is *verifiable and traceable*. The export's pilot violated it in two ways that the contract above must prevent: values typed by hand into a JSON file with no database record (concern 5), and the same fact held in two places (concern 6; CLAUDE.md rule 5).

## 4. What the render target demands of earlier stages

The export's own inference, restated against `main`'s stages. A rendered page must show, per jurisdiction: value, clause, edition, tier, read level, source link; per group: value and marker; per source: population, design, sample size, finding; and gaps, Co-1 status, a plain line. That implies:

| Stage | Must output for the page |
|---|---|
| research | Which in-scope jurisdictions were searched and which were not (so the page can say "not yet read" without inventing it); the Co-1 search outcome |
| evidence | One extraction per reading with a locator (`loc_*`), the standard's edition and currency, and a verification state that distinguishes *read* from *verified* (D6) |
| judgment | Population/ICF/need attribution per extraction, as adjudicated terms, not keyword tags (the export's tags were all `UNREVIEWED`) |
| synthesis | The direction rationale per parameter and the prose behind "why it matters" |
| specification | A value, `design_scale`, `marker`, `state`, and a derivation that cites the extractions (D3 decides what a code-only floor may claim) |
| render | Reads the above through one view; derives every count, label and statement at read time; holds no copy |

## 5. Concerns and confusions the session raised, with their state on `main`

The export's assistant listed 23 concerns and 10 confusions after the pilot, before the owner answered the confusions. Dispositions below; **C = concern, Q = confusion** in the export's numbering.

| Item | Substance | State |
|---|---|---|
| C1–C4 | Generator hard-codes ramp logic; no per-item direction; units cover slope and length only; E-03-specific scope and 500 mm rise assumption | Moot as code (generator not carried). Per-item direction is now `accessibility_direction`; unit families open (E9) |
| C5, C6 | Values typed into JSON; two copies of each fact | Prevented by rule 5 and by D1; the E-03.json in this folder is reference data only |
| C7 | 20 older `data/jurisdictional_values/*.yaml` files of unclear status | Moot: `data/jurisdictional_values/` does not exist on `main` |
| C8, C9 | Classification tags provisional and unreviewed; untagged sources drop out of population filters | Carried as E4 and E10 |
| C10 | Doctrine requires a pending cell to display `[BEST-PRACTICE-PENDING]` with a gap link; owner says no `Not set` rows | Read as compatible: no row, gap stated under Gaps with its link (ledger 2026-10-30, item 9(a)). The doctrine text is unchanged; owner to confirm |
| C11 | Standards (T4–T6) cannot anchor best practice vs owner's gentlest-value rule | Largely resolved by Option A (2026-07-21); see section 7, correction 1 and ledger 2026-10-30, item 1. Closed: the owner confirmed the ○ band and flag stay (ledger 2026-10-30 second) |
| C12 | Questions-led doctrine not met once the question line was removed | Read as not repealed (ledger 2026-10-30, item 9(b)); how questions appear on a specification page is the owner's |
| C13, C14 | Audience lens not built; within-population variability barely shown | Open (D8; `audience-priority.md`) |
| C15, C16 | Two design systems; requirements written for one page, no shared template | Open; the shared template is the render contract plus one renderer |
| C17–C20 | Accessibility untested; page length; landscape-phone first screen; APA and edge alignment | Not carried (page not carried); the requirements carry (D16) |
| C21–C23 | Restyled six times without a baseline; both audits self-authored; "verified" claims from the session's own checks | Lesson recorded in requirements §9. No third-party scan exists |
| Q1 | Best practice with trade-offs: a gentler ramp is longer and more tiring; who decides between conflicting groups or parameters? | **Open.** Doctrine has a conflict-mapping rule the session did not apply |
| Q2 | Which tier numbering governs | Answered by the session: `governance/tier-system.md` (2026-05-25, operative). The older line in `references/project-standards.md` is stale |
| Q3 | Where pages live and what is deployed | Moot: neither `site/` nor `specs/` exists on `main` |
| Q4 | "Lens" means two things | Answered: two lenses (D8) |
| Q5 | "Buckets 1 and 2" = P1+P2+P3 | Answered (D11) |
| Q6 | What "covered" means | Answered (D6) |
| Q7 | Database or curated JSON | Answered: database (D1) |
| Q8 | Specification in the book vs item pages | Answered (D2). How they relate to the generated `parts/` files is **[UNVERIFIED]** on `main` |
| Q9 | Single-source gentlest value as "evidence-based" | Answered as D3; marker unresolved (D14) |
| Q10 | Provisional as a permanent state or a stage | Answered: a stage (D6) |

## 6. Not carried, and caveats

- **Not carried:** the static generators (`spec_page_v2.py`, `spec_page_v3.py`), the rendered `site/specs/*.html`, migration `026_classification_codes.sql` and its data migration (the numbering collides with `main`'s history), and the repairs to `validate_db.py` / `research_protocol_audit.py` (`main` has its own check registry).
- **Stress-test grades** (scope B, discovery C+, collection D+, verification D+, judgment F, synthesis F, render F) describe the old base. They are not a description of `main`.
- **Rest-landing figures** (Germany 6 m; Singapore 6 m at 1:12 to 15 m at 1:20; UK 500 mm of rise per flight; US/JP/NZ about 750 mm) and the claim that the book spec's 9 m run is unsourced (GAP-016) are the export's readings of secondary sources. **[UNVERIFIED]** here; I did not open the PDFs in the export.
- **The export holds more than this folder.** It also contains the browser screenshots, four fetched PDFs and a subagent transcript, none of which were needed for these decisions and none of which were copied into the repository.
- **Not done:** no decision record. The owner confirmed the reading in ledger 2026-10-30 item 1, so there is no supersession to record and no DR or attestation is needed. Were that ever reversed, a `SUPERSEDES` line is required against `governance/tier-system.md` §8 and `governance/mission-and-epistemics.md` §2.
- **Not done, by design:** the rest-landing parameter (D18) is a data migration; CLAUDE.md rule 10 requires it in a PR apart from tooling and documents. No edit was made to `governance/pipeline-contract.yaml`: a render criterion with `check: null` would be unread apparatus (rule 8), and the ledger's CONDITION/ACTION is what a future session reads.

## 7. Corrections to the first version of this file

1. **[CORRECTION: "D3 conflicts with the mission document and tier-system §5/§8" — changed to "largely already resolved on `main`".]** The first version took the export's handoff at its word. `governance/tier-system.md` §8 and `governance/mission-and-epistemics.md` §2 were amended on 2026-07-21 (owner directive, Option A) so that a T4–T6-only determination is stated as weak-band (○) "best practice as currently known", always flagged weak and code-derived. I did not find a "wall" sentence in the mission document; its section 2 title is "code consensus anchors it only at the weak band". What remained between the owner's statements and `main` was the marker and flag, not the right to name the gentlest code value best practice; the owner has since confirmed the ○ band and flag stay (ledger 2026-10-30 second).
2. **[CORRECTION: D14 "unresolved" — changed to resolved.]** Tier-system §8 sets ○ at determination level for a T4–T6-only basis. The export's ● contradicted `main`.
3. **[CORRECTION: E12 "no table found" — changed to "not yet built, but ruled".]** OW-1 (2026-10-29, third) rules a render table. I cited only R1 and missed OW-1, which is in the same ledger.
4. **[CORRECTION: C7 "unverified" — changed to moot** (`data/jurisdictional_values/` is absent on `main`).]
