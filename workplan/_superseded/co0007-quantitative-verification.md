# CO-0007 Quantitative Verification
**Created:** 2026-04-26 01:46 UTC
**Stage:** 0.2 (Quantitative verification)
**Resolves audit finding:** B-01 (quantitative claims unverified)
**Status:** Stage-0 deliverable; pre-adoption (workplan v3 not yet adopted per 0.9)

---

## Purpose

Workplan v3 §0.2 lists 14 quantitative claims sized into the synthesis from prior conversation state. Audit v2 §B-01 designated this High because budgets, gating decisions, and scope estimates compound across these inputs. This report verifies each against live repository state at HEAD (`7d99147da49a`, 2026-04-25 00:21:16Z).

---

## Verification table

| # | Audit claim | Live value | Match | Source of truth |
|---|---|---|---|---|
| 1 | ~280 commits | **2,259 commits** on `main` | ✗ MAJOR | GitHub API `/commits` Link header `rel="last"`. First commit `e25429977715` 2026-03-18 05:25Z; HEAD `7d99147da49a` 2026-04-25 00:21Z. ~38 days, ~59 commits/day mean velocity. |
| 2 | 78 BPC files | **78 topic-slug BPCs** in `references/bpc/<topic>/<slug>.md` | ✓ exact | Tree enumeration. Plus 14 frozen population-level + 1 thermoregulation + 1 index = 94 files under `references/bpc/`. Audit's denominator = topic-slug only. |
| 3 | 90 search-logs | **90 = 76 topic + 14 population-level**, plus 1 root pointer + 1 archived monolithic | ✓ matches if 76+14 | `references/search-log/`. The 90 figure works only if topic-slug + population-frozen are summed. |
| 4 | 92 Part 4 specs | **92 items** in `parts/v10/part04.md` | ✓ exact | Categories: A=18, B=12, C=6, D=11, E=15, F=8, G=9, H=5, I=4, K=4. |
| 5 | 73 spec-database records | **73** in `references/specification-database.json` | ✓ exact | `_meta.total_specs: 73`; `bpc_files_processed` lists 25 source slugs (Phase 2A complete). |
| 6 | 20 Appendix A tables | **20 markdown tables** (A.1–A.20) in `parts/v10/appendix-a-jurisdiction-comparison.md` | ✓ exact | Section headers list A.1 through A.20. |
| 7 | 46 jurisdictions | **49 unique country codes** in `references/standards-registry.md` (50 incl. schema example) | ~ approximate | Codes: AR, AU, BD, BE, BR, CA, CH, CL, CN, CO, CR, DE, DK, EC, EG, ES, ET, EU, FI, FR, GH, GT, ID, IE, IN, INT, ISO, IT, JP, KE, KR, MA, MX, NG, NL, NO, NZ, PE, PH, PT, SE, SG, TH, TZ, UK, UN, US, UY, ZA + schema placeholder. 112 jurisdiction-standard pairs across 49 codes. **project-standards line 118 says "24 canonical (per jurisdiction-tracker §4.7.3)"** — the 24 is the *coverage scope*, not the *registry size*. Confirms audit L-01/L-02 disambiguation gap. |
| 8 | 557 sources / 94% verified | **584 deduplicated sources / 503 verified (86%)** per `bibliography-v11-draft.md` self-meta | ✗ MAJOR | Header text: *"Compiled from 584 deduplicated sources… 81 entries carry [GREY] status (citation details unverified)."* Coverage table sums to 584. Library has *grown* (557 → 584) and verification rate has *decreased* (94% → 86%). |
| 8a | (cross-check) tier-JSON sums | Tier 1: 57 · Co-1: 25 · Tier 2: 37 · Co-2: 15 · Tier 3: 168 · Tier 4-5-6: 249. **Sum = 551** | drift | Bibliography text claims 584; tier-JSONs hold 551. **33-source drift between two stores** of the same data. Confirms audit D-02 disconnect (single-source-of-truth holds at edit but not read). |
| 9 | 189 connection register entries | **`Total connections migrated: 181`** + **`Next CON-ID: CON-0189`** in `references/connections/_index.md` | ✓ as next-ID | Status summary in `_index.md`: CONSUMED 140, CONSUMED-DEFERRED 42, PENDING 5, CONSUMED (this session) 3. Last-applied CON-IDs span CON-0001 through CON-0188; CON-0189 is next. Audit's 189 = next-ID, not entry count. |
| 10 | 13 doctrinal-divergence parameters | **13 numbered ## sections** in `references/opus-divergence-synthesis.md` | ✓ exact | Ramp Gradient, Threshold Height, Corridor Clear Width, Reach Range, LRV Contrast, Turning Space, Door Opening Force, Anti-Scald Temperature, Grab Bar Height, Slip Resistance, Rest Seating Interval, Classroom RT, Kitchen Worktop Adjustability. |
| 11 | 11 population codes | **11 disability codes + ALL aggregator** in `skills/workplan-orchestrator_SKILL.md` §Population Codes | ✓ exact | MOB, VIS, DEAF, NEU, DEM, NDV, NDV/MH, PAIN, DBL, OFS, IntD = 11. ALL is taxonomy-level aggregator. Plus supplementary codes (CHD, LPA, EXH, BAR) explicitly excluded from main taxonomy. |
| 12 | 60–80 atomic parameters | **NOT A LIVE COUNT** — concept doesn't map to existing artifact | ✗ definitional | Closest live denominators: 92 Part 4 items, 73 spec-DB records, 38 FDR scenarios, 13 doctrinal-divergence parameters. The "atomic parameter" unit is a workplan-side concept for the structured form's migration unit; it doesn't pre-exist in the corpus. **Definitional task for A3 (conceptual model), not a verification target.** |
| 13 | 55 population pairs | **C(11,2) = 55** | ✓ mathematical | 11 disability codes; pairwise = 55. |
| 14 | ~40 skill files | **45 active skill files** (42 active + 3 in `skills/deprecated/`) | ~ understated | Tree enumeration of `skills/`. Audit's "~40" rounds the right answer down. |

---

## Summary by audit-claim accuracy

| Class | Claims | Items |
|---|---|---|
| **Exact match** | 7 | 78 BPCs, 92 Part 4, 73 spec-DB, 20 Appendix A tables, 13 doctrinal divergences, 11 populations, 55 pop-pairs |
| **Acceptable approximate** | 3 | 90 search-logs (= 76 topic + 14 pop), 189 connections (= next-ID), ~40 skills (≈45) |
| **Disambiguation gap** | 1 | 46 vs. 24 jurisdictions — both correct for different denominators; not labeled |
| **Definitionally absent** | 1 | 60–80 atomic parameters (forward-looking workplan unit, not corpus unit) |
| **Material discrepancy** | 2 | 280 commits → 2,259; 557/94% sources → 584/86% sources |

---

## Material findings

### M1 · Commit count is wrong by ~8× and the figure is load-bearing

Synthesis says "approximately 280 commits"; live is 2,259. The 280 figure was used to scale "the project corpus" rhetorically (synthesis Coda) but does not appear to gate any specific budget calculation. **Implication is rhetorical, not arithmetical** — the 12–18 month estimate from synthesis was not derived from commit count. But the figure being 8× off is a credibility hit on the synthesis as a whole and is the kind of error audit B-01 was designed to catch. Workplan v3 §0.7 (synthesis re-issue) must correct.

### M2 · Bibliography library grew and verification rate decreased

Synthesis: 557 sources / 94% verified (~33 unverified). Live: 584 sources / 503 verified (~81 unverified, 14% rate). **The unverified residual approximately tripled**. Workplan v3 §C7 currently allocates 12–17 sessions for "557 sources + 6% residual disposition." The actual scope is 584 sources with 81-source residual — roughly 2.5× the disposition workload. Either C7's session estimate is too low, or the disposition criteria need tightening (e.g., expanding "deprecate as unverifiable" rather than re-verify). **Adjust C7 budget upward, or revise disposition criteria.**

### M3 · Bibliography ↔ tier-JSON drift

Bibliography text claims 584 sources. Six tier-JSON files sum to 551. 33-source gap. The bibliography is generated from BPC `key sources` tables; tier-JSONs were curated separately. The drift is a real instance of audit D-02 (single-source-of-truth at edit but not read time). **Reconciliation is itself a C7 task** — adds scope but does not require new tooling.

### M4 · "Atomic parameter" is not a corpus unit

The "60–80 atomic parameters" figure is workplan terminology for the migration unit in the future structured form. It has no live denominator. The closest existing units (92 Part 4 items, 73 spec-DB records, 13 divergence parameters) bracket the audit's 60–80 range, suggesting the audit guessed reasonably — but the definition has to be made in A3, not pre-counted. **No correction needed; flag for A3.**

### M5 · Jurisdiction count disambiguation

Standards registry holds 49 unique codes (112 jurisdiction-standard pairs). project-standards rule cites "24 canonical." Audit cites 46. All three are right for different denominators (registry size, coverage scope, prior synthesis estimate). **No correction needed; flag for 0.7 synthesis re-issue to define the denominators clearly.**

---

## Updated scope-relevant figures for downstream stages

These figures, corrected, are the inputs Stage A/B/C should use:

| Variable | Use this figure | Used in |
|---|---|---|
| Repo commit count | 2,259 (as of HEAD 2026-04-25 00:21Z) | Status reporting only; not budget input |
| BPC topic-slug files | 78 | Stage 0.4 contamination sampling (N=15 from 78); C3 migration scope |
| BPC frozen population-level files | 14 | Independent migration track in C3/C4 |
| Search-logs (topic) | 76 | C3/C7 alignment |
| Part 4 items | 92 | C5 (items and rooms migration) |
| Spec-DB records | 73 (Phase 2A complete; Phase 2B+ not started) | C2 migration tooling input; C7 alignment |
| Appendix A tables | 20 | C8 (jurisdiction migration) |
| Jurisdictions in registry | 49 codes / 112 pairs | C8 budget input (revise upward from 46) |
| Bibliography sources | 584 (503 verified + 81 unverified) | C7 budget input (revise upward from 557) |
| Connection register | 188 entries (next CON-0189) | C0 cross-cutting reference |
| Doctrinal-divergence parameters | 13 | A6 evidence methodology input |
| Population codes (disability) | 11 | A7 + B4 multi-pilot scoping |
| Population pairs | 55 | C6 conflict combinatorial (audit estimated 200–400 actual entries from 55 pairs × ~60 parameters) |
| Active skills | 42 | 0.3 inventory + C2 rebuild |

---

## Items that could not be verified in this session

- **Cross-walk between bibliography text and tier-JSON files** to enumerate the exact 33-source drift. Reconciliation work, deferred to C7 or its own sub-task.
- **Phase 2B/2C/2D progress on spec-DB.** The `_meta` field shows Phase 2A complete; whether Phase 2B has progressed since 2026-04-08 was not checked.

---

## What this report does not do

- **Does not commit corrections.** Workplan v3 §0.7 (synthesis re-issue) is the formal commit point.
- **Does not adjust budgets.** C7, C8 budget revisions per M2 / M5 are a Stage 0.7 task, not 0.2.
- **Does not modify the gap register.** No new gap entries.
- **Does not adopt or reject workplan v3.** That is 0.9.

---

## Coda

Two of fourteen quantitative claims have material errors (commit count, bibliography stats). Eleven match exactly or acceptably. One is definitionally absent and one is a labeling gap rather than a numeric error. The synthesis's quantitative grounding is **mostly accurate, with two corrections needed before the synthesis is re-issued in 0.7**. Neither error invalidates Stage 0's procedural plan; both invalidate downstream budget arithmetic if uncorrected.
