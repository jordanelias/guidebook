# Multilingual & Multijurisdictional Search Remediation Plan
**Created:** 2026-05-09
**Governs:** search_languages, search_coverage, term_aliases tables in tracking DB

## Problem Statement

30/91 items (33%) carry SPECULATIVE flags. Search coverage is uneven:
- EN 59%, DE 53%, JA 40%, FR 38%, ZH 31%, KO 26% of slugs searched
- 21 slugs have no documented English search
- ZH, KO, PT coverage thin across the board
- Session-level web_search was English-only; BPC creation sessions did better but inconsistently

## Infrastructure Built

| Table | Rows | Purpose |
|---|---|---|
| terms | 20 | Core accessibility terms (EN canonical) |
| term_aliases | 284 | Translations + synonyms in 12 languages |
| term_item_links | 50 | Term → item mapping |
| search_languages | 1134 | Coverage tracking per slug × language |
| search_coverage | 1863 | Coverage tracking per slug × jurisdiction |

## Search Protocol

For each remediation search:

1. **Select slug** from priority queue (below)
2. **Load relevant terms** via `term_item_links → terms → term_aliases`
3. **Construct search queries** in target language using `term_aliases`
4. **Search** using PubMed (MeSH multilingual), Scholar Gateway, Consensus, or web_search with translated terms
5. **Log results** to `search_languages` (status: SEARCHED/PARTIAL/NOT-RUN, results_count)
6. **Log jurisdiction** to `search_coverage` (status: SEARCHED/THIN/NOT-RUN)
7. **Update evidence_sources** with any new references found
8. **Update SPECULATIVE flag** if evidence found (remove flag or add citation)

## Priority Queue

### Tier 1: SPECULATIVE items with ≥8 languages NOT-RUN ({len(tier1)} slugs)
These have the highest risk of missing contradictory or supporting evidence.

- `luminance-contrast-lrv-evidence-base` (14 langs NOT-RUN) → items: D-03
- `sensory-room-user-control` (13 langs NOT-RUN) → items: A-16, H-02
- `school-environment-autism` (12 langs NOT-RUN) → items: A-02, A-08
- `circadian-lighting-melanopic-edi` (11 langs NOT-RUN) → items: B-06, B-07, H-02
- `construction-cost-data` (11 langs NOT-RUN) → items: A-16, D-10, K-12
- `visual-fire-alarm-seizure-safety` (11 langs NOT-RUN) → items: B-10
- `accessible-design-economics-cost-premium` (9 langs NOT-RUN) → items: D-03, K-12
- `thermal-comfort-older-adults-care-settings` (8 langs NOT-RUN) → items: F-07, G-08, H-04

### Tier 2: SPECULATIVE items with <8 languages NOT-RUN (6 slugs)

- `ms-thermal-temperature-conflict-resolution` (7 langs NOT-RUN) → items: A-16, F-06, F-07
- `multilingual-evidence-convergence-non-english` (6 langs NOT-RUN) → items: D-03, D-09, D-11, E-03, E-07
- `ndv-aut-built-environment-quantified-thresholds` (6 langs NOT-RUN) → items: A-16, D-05, G-08
- `sensory-relief-space-design` (4 langs NOT-RUN) → items: A-16, F-01, F-03, H-02
- `accessible-bathroom-and-grab-bar` (3 langs NOT-RUN) → items: G-03, K-01
- `room-acoustic-performance` (2 langs NOT-RUN) → items: A-13, F-01

### Tier 3: Non-speculative with ≥10 languages NOT-RUN (29 slugs)

- `bariatric-turning-radius-built-environment` (14 langs NOT-RUN)
- `bathroom-typology-global-south` (14 langs NOT-RUN)
- `chronic-pain-built-environment` (14 langs NOT-RUN)
- `co1-housing-research-global-south` (14 langs NOT-RUN)
- `crpd-implementation-built-environment` (14 langs NOT-RUN)
- `fatigue-spectrum-built-environment` (14 langs NOT-RUN)
- `government-grant-programmes` (14 langs NOT-RUN)
- `hearing-impairment-built-environment` (14 langs NOT-RUN)
- `luminance-contrast-and-pattern` (14 langs NOT-RUN)
- `post-occupancy-evaluation-global` (14 langs NOT-RUN)

## Language Priority

| Language | NOT-RUN slugs | Search approach |
|---|---|---|
| SV | 52 | web_search (SBI/Boverket) |
| DA | 52 | web_search (BR18/SBI) |
| FI | 51 | web_search (Finnish building code) |
| ES | 51 | PubMed (MeSH ES) + web_search |
| PT | 50 | web_search (NBR standards + ABNT) |
| KO | 50 | web_search (KS standards + Korean research) |
| IT | 50 | web_search (UNI standards) |
| ZH | 46 | web_search (GB standards + Chinese research) |
| NL | 40 | web_search (NEN standards) |
| JA | 40 | PubMed (MeSH JA) + web_search (JIS/MLIT terms) |
| FR | 36 | PubMed (MeSH FR) + web_search (NF standards) |
| DE | 27 | PubMed (MeSH DE) + web_search (DIN/DGUV terms) |
| EN | 21 | PubMed + Scholar Gateway + web_search |
| NO | 16 | web_search (TEK17/Direktoratet) |

## Jurisdiction Priority

| Jurisdiction | NOT-RUN slugs | Standard body |
|---|---|---|
| ZA | 75 | SANS 10400-S |
| AT | 74 | ÖNORM B 1600 |
| IN | 72 | Harmonized Guidelines |
| CH | 70 | SIA 500 |
| IE | 69 | Part M |
| DK | 69 | BR18 |
| SG | 68 | Code on Accessibility |
| BR | 67 | NBR 9050 |
| NZ | 65 | NZS 4121 |
| KR | 63 | KS/MOLIT |
| CN | 63 | GB 50763 |
| JP | 54 | JIS/MLIT |
| ES | 51 | CTE DB SUA |
| IT | 50 | DM 236 |
| SE | 49 | Boverkets/AFS |

## Effort Estimate

| Tier | Slugs | Est. sessions | Approach |
|---|---|---|---|
| Tier 1 | 8 | 3–5 | Full multilingual search per slug using PubMed + Scholar Gateway + term_aliases |
| Tier 2 | 6 | 2–3 | Targeted search in highest-gap languages |
| Tier 3 | 29 | 2–3 | Batch search, lower priority |
| **Total** | **43** | **7–11** | |

## Done Criteria

1. All Tier 1 slugs have ≤3 languages at NOT-RUN
2. All SPECULATIVE items have at least EN + DE + JA + FR + ZH coverage
3. All search_languages entries have been updated with results_count
4. Any new evidence found has been added to evidence_sources + source_slug_links
5. SPECULATIVE flags reviewed and removed where cross-jurisdictional evidence found
