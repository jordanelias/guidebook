# Pipeline Stress Test — "Ramp Slopes"

**Date:** 2026-10-29 · **Repo HEAD:** be7bc576 · **DB:** `data/guidebook.db`, user_version 25 (read-only; all writes on a scratch copy)
**Audit trail:** [run-log.md](run-log.md) (timestamped actions/decisions) · [evidence/](evidence/) (raw query/command output)
**Author:** Claude Sonnet 5.5 (direct, serialized, main loop — per the rate-limit lesson). Standing rule #2 means I did **not** write a synthesis value.

## 1. Bottom line

**Research can be done; it cannot yet be carried through the pipeline to a trustworthy output.** I found and verified new evidence on ramp slopes in about an hour using external tools. But the pipeline's own machinery could not safely ingest it, could not verify it beyond "exists", had no judgment engine to weigh it, had no synthesis capacity for it (1 of 82 BPCs has a reasoning doc), and its published ramp page is **wrong**, not just empty.

| Stage | Capability for this topic | Grade |
|---|---|---|
| 1 Scope / taxonomy | Resolved cleanly to item E-03 + TERM-001 (14-language aliases) + 6 gaps. Missed sub-parameters (cross-slope, landings, run length) — no items exist. | **B** |
| 2 Discovery / search | Strong *with external tools*; internally 5/47 jurisdictions searched, tier 5/6 never attempted, no way to record how a source was found. Paywalled norms (BS 8300, AS 1428.1, DIN 18040-1, ISO 21542) unreachable. | **C+** |
| 3 Collection / ingestion | Write path accepts duplicate DOIs, tier 9, `evidence_type='bogus'`, year 2099 (CI later catches the duplicate, not the tier/type). The 28 existing duplicate-DOI groups are *by design* (one ref_id per BPC, allowlisted in `test_db_integrity.py` D01) — see §8. | **D+** |
| 4 Verification | "VERIFIED" = existence only. Blind to title/DOI mismatch (REF-00387) and topical irrelevance; blocking CI passes 35/35 over these. | **D+** |
| 5 Judgment / weighting | Tables empty; no script computes a cell state or weight. | **F (unbuilt)** |
| 6 Synthesis | 1 of 82 slugs has a reasoning doc; ramp slug has none; rule-#10 gates cannot be satisfied for E-03. | **F** |
| 7 Render / presentation | `site/specs/e-03.html` shows another item's prose, wrong populations, a recycled-ID evidence row, empty jurisdiction table; generator crashes on committed DB. | **F (actively misleading)** |
| 8 Governance / audit tooling | Rich and honest, but 2 of the audit scripts crash, 1 check is vacuous, neither crash is in CI. | **C** |

## 2. What the pipeline does and decides, stage by stage

**S1 Scope.** Searched slugs/items/terms/gaps for ramp|slope|gradient. *Decision:* ramp slope = **E-03 "Ramp Gradient (≤1:20 — MS Fatigue and Temporal Accessibility)"**, bpc slug `stair-ramp-threshold-biomechanics-accessibility` (state RETRACTED-PRE-REHAB); excluded `detectable-gradient-protocol-sensory-zones` (false positive on "gradient").

**S2 Discovery.** Ran Consensus, web search, primary-source fetch, multilingual (DE, JA) searches, Crossref. *Decisions:* serialize Consensus calls after two of three parallel calls were throttled; treat web-search summaries of paywalled standards as *secondary, unverified*; verify papers by DOI→Crossref instead of trusting titles.

**S3 Collection.** Traced what the KB holds for the slug: 15 sources, all tier 3–4, only 4 actually about ramps/wheelchair propulsion/thresholds (Kim 2014, Koontz/Yang 2012, Waters 1988, Lawati 2017) — the other 11 concern stairs (6) or unrelated tasks such as sit-to-stand, grab bars, luminance contrast (5); 0 statutes, 0 Co-1/Co-2, 11 of 15 jurisdiction "INT". Tested ingestion on a scratch DB (§4).

**S4 Verification.** Crossref-checked the 4 ramp-relevant DOIs: 2 correct, **REF-00387 is two papers fused**, **REF-00388 is a backrest-height study (first author Yang) used as the basis of the 1:20 claim**. Checked primary ADA text — the YAML US row is right.

**S5 Judgment.** Checked `evidence_cell_state`, `convergence_assessment`, `source_value_extractions`: nothing for E-03. Reviewed the 8-row YAML that holds the only jurisdiction values (§5 defects).

**S6 Synthesis.** Dry-ran the 9-step rule; blocked at step 3 (paywalls) and step 5 (no T1/Co-1/T2). *Decision:* produce an evidence inventory + Opus-queue brief (§6) rather than a value.

**S7 Render.** Opened `parts/v10` and `site/specs/e-03.html`; attempted regeneration (crash).

## 3. Findings (severity-ranked, all verified this run unless marked)

| # | Sev | Stage | Finding | Evidence |
|---|---|---|---|---|
| R-01 | **Critical** | Render | `site/specs/e-03.html` is wrong: floor-finish "why it matters", population DEM/OFS (DB: MOB/PAIN/OFS/SCI), evidence row "REF-00460 AS 1428.1 threshold" — REF-00460 is now an Italian door standard (**ID reused with shifted meaning**), jurisdiction table empty, cites "Waters 1985" (DB: 1988). | s3, run-log S4 |
| R-02 | **Critical** | Render | `spec_page.py` queries a `specification` table absent from the committed DB → published pages are unreproducible, no recorded link to the state that produced them. | s10 |
| R-03 | High | Verification | REF-00387 (Pavol) is VERIFIED/COMPLETE/`integrity=OK` but title+year describe one paper and the DOI another (JAGS 2002 trip-strength paper). | Crossref check |
| R-04 | High *(revised, see §10)* | Collection | 1:20 rationale chain is unsupported: GAP-019 says it derives from "Koontz 2012"; REF-00388 is Yang et al. 2012 - a backrest-height trial in 36 SCI wheelchair users on level vs a single 3° slope. It shows uphill raises force but cannot derive a threshold, and does not cover cervical lesions. Still flagged OWNER-QUEUE-DISAMBIGUATE yet VERIFIED. | s6, s14 |
| R-05 | High | Collection | The source GAP-019 names as the "proper primary source" (PLOS One 2022 SR) is **already in the KB** (REF-00037 + duplicate REF-VERIFIED-003) but **not linked to the ramp slug**, and the gap misnames its author (it is Rouvier et al., not "Lalumière"). Gap OPEN since 2026-05-09 with its resolution in hand. | s7, s3 |
| R-06 | High | Judgment | The item's headline mechanism ("MS fatigue") has **zero** supporting sources in the KB. External literature exists (Rooney 2021 meta-analysis; Har-Nir 2022 — which finds perceived effort, not O2 cost, is elevated uphill in pwMS, partly contradicting the item's energy-conservation rationale). | S5 research |
| R-07 | High | Search | Direct empirical ramp-slope studies are missing: **Sanford 1997** (171 subjects, 1:8–1:20; few manual-WC users failed at 1:8 — a ready-made *named dissenter* for rule #7) and **Lenker 2016** (1:8/1:12 acceptable, 1:4 unsafe). 0 hits in KB. | s5 |
| R-08 | Medium *(downgraded; see §8)* | Collection | `db.py add-source` has no duplicate-DOI check, no CHECK on tier/evidence_type/year, no UNIQUE index; CLI cannot record discovery provenance. CI test D01 does catch a non-allowlisted duplicate, but only once `doi_resolution_outcome` is set, and its allowlist is hand-maintained. The 28 existing groups are intentional (per-BPC rows). | s9, s12 |
| R-09 | High | Governance | `validate_db.py`/`db.py validate` (dead column `doi_less_key`) and `research_protocol_audit.py` (dead column `title`) crash; not run by CI. Rule #7 has **no working enforcement**. | s8 |
| R-10 | Medium | Governance | PMP CHECK 1 is vacuous (flags only items that have probes). 88/92 items never walked; E-03's 1:20 has no walk; audit says 0. | s8 |
| R-11 | Medium | Verification | Phase-E gate: 640/640 "eligible"; ramp slug "READY" at tiers [3,4] only. Gate has no discriminating power and no relevance test. | s8 |
| R-12 | Medium | Judgment | YAML a-1_e03: NO row `value_numeric=1.0` placeholder; unit `ratio` on percent values; tier 6 on all rows though BS 8300 is T5 and ISO 21542 T4 under `tier-system.md`; BS 8300 multi-tier table (1:20/10 m, 1:15/5 m, 1:12/2 m) flattened to "max 1:12"; cites BS 8300-**1** while ramp rules sit in Part 2 (unresolved); `spec_id` null everywhere; Japan, Canada, NZ, Brazil, Italy absent. | YAML read |
| R-13 | Medium | Scope | No items for cross-slope (ADA 1:48), landings, run length/rise, handrail trigger — all part of "ramp slope" in every code; only a gradient is modelled. | S1 |
| R-14 | Medium | Governance | 177/273 connections have NULL description (162 CONSUMED); the E-03 page cites CON-0229 (NULL description, no E-03 target). | s11 |
| R-15 | Low | Tooling | Windows: cp1252 crashes any script printing item names ("≤"); `resolve_dois.py` has no argparse (`--help` launched a live run). | log S1, S6 |

## 4. Machinery stress results (scratch DB)

| Probe | Expected | Actual |
|---|---|---|
| Ingest a valid new paper (Sanford 1997) | Accepted, queued for verification | Accepted; row has no quality/verification, no authors, no provenance fields available |
| Ingest duplicate DOI | Rejected at write | **Accepted by CLI**; CI D01 flags it only if the DOI is not allowlisted *and* `doi_resolution_outcome` is set (Kim 2014's DOI is allowlisted, so my first test could not trigger CI) |
| Ingest tier 9 / bogus type / year 2099 | Rejected | **Accepted** |
| CI integrity after bad rows | Fail on bad data | 34/35 — fails only on C02 (missing outcome); tier 9 / bogus type / year 2099 never detected |
| Run validators | Pass or report | 2 crash on nonexistent columns |
| Regenerate E-03 page | Reproduce | Crash |

## 5. Ramp-slope evidence inventory (for the Opus queue — not a synthesis)

Provenance levels: **P** = primary text read; **S** = secondary web source only (not authoritative); **A** = abstract only; **X** = conflicting/unresolved.

| Jurisdiction / source | Running slope | Other | Level |
|---|---|---|---|
| US — ADA 2010 §405 | 1:12; 1:10 if rise ≤6 in; 1:8 if rise ≤3 in (limited space) | cross 1:48; rise ≤30 in/run; landing 60 in; handrails if rise >6 in | **P** (access-board.gov) |
| UK — BS 8300-2:2018 / AD M | 1:20 preferred; 1:12 absolute max | rise caps 500/333/166 mm at 1:20/1:15/1:12; going 10/5/2 m | **S** (paywalled; Part 1 vs 2 unresolved) |
| DE — DIN 18040-1 | 6 % | run ≤6 m; landing ≥1.50 m; cross-fall 0; width 1.20 m | **S** |
| JP — Barrier-Free ordinance | 1/12; 1/8 if height ≤16 cm | landing every 75 cm rise; width ≥120/90 cm; handrail if >1/12 or >16 cm | **S** (prefectural docs quoting national rule); **not in YAML** |
| AU — AS 1428.1:2021 | 1:14 for ramps >1.9 m (one source) vs 1:20 up to 15 m (another) | landings every 9 m (one source) | **X** |
| CH — SIA 500 | 6 % (12 % admissible) | — | KB title only |
| Clinical | Sanford 1997 (1:8–1:20; ADA range usable); Lenker 2016 (1:8/1:12 OK, 1:4 unsafe); Kim 2014 (in KB); Rouvier 2022 SR, 34 studies (in KB, unlinked); MS: Rooney 2021, Har-Nir 2022, Devasahayam 2019; ambulant: Liu 2023, Rasouli 2019 | | **A** |

Observation (not a synthesis): primary-verified fact is that the US legal maximum is 1:12; the guidebook's 1:20 is a design preference whose clinical derivation is currently unsupported inside the KB and for which the nearest direct empirical study (Sanford 1997) cuts the other way for wheelchair users. Under `tier-system.md` §3, convergence of T5/T6 codes on 1:12 is regulatory floor, not best-practice evidence.

## 6. Recommended next steps (ordered by value ÷ effort)

1. **Stop the misleading page**: unpublish or banner `site/specs/e-03.html`; fix the `specification`-table dependency or point the generator at real tables (R-01/02).
2. **Fix the dead audit scripts** (`doi_less_key`, `title`) and wire them into `audit.yml`; make PMP CHECK 1 flag items with *no* probes (R-09/10).
3. **Add DB constraints at the write path**: a duplicate-DOI guard in `add-source` consistent with the per-BPC design (allowlist, not UNIQUE), CHECK on tier/evidence_type/pub_year, `--derivation-chain`/`--search-query` flags on `add-source` (R-08, F-06).
4. **Repair records**: REF-00387 (fuse), REF-00388 (disambiguate), merge REF-00030/00386, REF-00037/VERIFIED-003; link Rouvier 2022 to the ramp slug and close/advance GAP-019 with correct attribution (R-03/04/05).
5. **Ingest the new literature** (Sanford 1997, Lenker 2016, MS cluster, ambulant-aid studies) via the normal pipeline with a named-dissenter entry; run a PMP walk on the 1:20 value (R-06/07/10).
6. **Fix the YAML** (NO row, units, tiers, BS 8300 structure, add JP/CA/NZ/BR/IT) and load it into `source_value_extractions` (R-12).
7. **Decide the paywall policy**: purchases (BSI, Standards Australia, DIN, ISO) for the ≈5 norms needed for ramp step 3; otherwise rule #10 forces downgrade.

## 7. Limits of this run

Journal papers were read at abstract level only; Crossref confirmed metadata, not content. Web-search summaries for DE/UK/AU/JP are secondary and partly conflicting. Only one topic item (E-03) was traced end to end; findings about tooling (R-08–R-11, R-15) are general, findings about content (R-01, R-03–R-07, R-12–R-14) are specific to ramp slopes. No commits were made; the real DB was never written. The scratch DB is in the session scratchpad and can be discarded.

## 8. Corrections made during the fix pass (2026-10-29)

- **Duplicate DOIs are not a CI blind spot.** `scripts/tests/test_db_integrity.py` D01 hard-codes an allowlist of DOIs that legitimately appear under several `ref_id`s (one per BPC), including Kim 2014 (REF-00030/00386) with a comment saying so. My first negative test reused that allowlisted DOI, so it could not trigger CI. Retest (evidence/s12) with a non-allowlisted DOI: CI fails D01 once `doi_resolution_outcome` is set, and fails C02 while it is NULL. Remaining true points: the CLI itself accepts duplicates, the allowlist is a hand-synced register, and the same paper carrying several IDs weakens traceability.
- Everything else in §3 stands, including R-03 (REF-00387), R-04, R-05, R-09, R-10.
- **R-01 is site-wide, not E-03-only.** Checking every evidence row on `site/specs/*.html` against the DB by REF id + first-author token + year: **0 of 222 agree, across 73 of 89 pages** (evidence/s13). The generated site cites REF ids from a pre-renumbering state. All 73 affected pages (E-03 plus 72 others) now carry an under-review banner (§9).

## 9. Fix pass — what changed (not committed)

| File | Change |
|---|---|
| `scripts/validate_db.py` | C5 repointed from dropped `doi_less_key` to doi/pmid/isbn/standard_number or (first_author_last, pub_year, pub_title); C3 expected version derived from highest `scripts/migrations/NNN_*.sql` (was hard-coded 5). Now runs: **C4 reports 31 connections with 0 targets** (real, pre-existing), C5 warns on 5 sources. |
| `scripts/audit/research_protocol_audit.py` | `title`→`pub_title`; honors `GUIDEBOOK_DB_PATH`; opens DB read-only; UTF-8 stdout. Now runs: **1,883 rule-#7 findings** (e.g. 615 verified sources lack `prior_expectation`/`search_queries_used`; 609 lack a population match). |
| `.github/workflows/audit.yml` | Two new steps in the `audit` job. Findings are informational; a Python traceback fails the job so the scripts cannot die silently again. Not blocking on findings because both report a real backlog. |
| `site/specs/*.html` (72 pages, same banner scoped to evidence references) | Banner inserted after `<body>`; 16 pages without checkable REF rows left untouched (unverified, not cleared). |
| `site/specs/e-03.html` | Visible "Under review — do not rely on this page" banner + provenance comment. Page content otherwise untouched (cannot be regenerated). |

## 10. Page redesign and classification layer (owner requirements)

**Owner requirements** (mid-run): exhaustive jurisdiction accordions; values per specific population; three tiers with ALL = universal; filter by population / ICF code / access need; plain-language labels; bulleted "Why it matters"; unit selector; code every evidence table.

**Built** (not committed): migration `026_classification_codes.sql` and a data migration (37 ICF codes, 14 access needs, provisional maps, 2,540 population tags, 664 ICF and 645 need rows - all UNREVIEWED); `scripts/db/build_classification_migration.py`; `scripts/generate/spec_page_v2.py`; `data/spec_pages/E-03.json`; regenerated `site/specs/e-03.html`. Applied to the real DB after a scratch apply, full rebuild comparison and CI integrity run (35/35); backup kept.

**Corrections to earlier findings:**
- A-01: the page mixed two records. Title/slug/value ("800-1300 mm", a door-handle height range) came from threshold-door-hardware; the prose and evidence were A-01's own acoustics content, correct in topic but citing stale REF ids.
- R-04: see the revised row above (Yang 2012 is an SCI slope study; it cannot set a threshold).

**Honest limits:** only 208 of 640 sources have a population "subject" tag and only 6 were assigned by reading an abstract; 224 have no tag. ICF/need vocabularies and maps are provisional. For E-03 only the US text was read from a primary source; 32 of 48 jurisdictions have no entry. Other pages (72) still show the old layout under a banner. URL-hash restore of filters, print layout and screen-reader behaviour were not tested.

**Next steps:** (1) owner review of the ICF/need vocabularies and the population maps; (2) read abstracts for the highest-value untagged sources; (3) buy/read the paywalled norms for UK, DE, AU, ISO and read SG/CN/IE/ES/FR primary texts; (4) ingest the five external studies; (5) generalise `data/spec_pages` to the other items and move it into DB tables.
