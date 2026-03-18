---
name: multilingual-research
description: >
  Conduct accessibility research across 14 languages (Chinese, Danish, Dutch, Finnish, French,
  German, Italian, Japanese, Korean, Norwegian, Portuguese, Spanish, Swedish, and English) and
  synthesize findings in English. ALWAYS use this skill when asked to: research accessibility
  topics, find international evidence, search non-English literature, conduct literature reviews,
  find international standards or guidelines, or gather evidence for accessibility guidebook sections.
  Occupational therapy is the primary lens. Trigger on: "research", "find evidence", "what does
  the literature say", "international standards", "review the evidence", "find studies on".
---

**Intake:** Focused query required. Ambiguous scope → ask one clarifying question before proceeding.
**Model:** Sonnet 4.6 with web search.
**Sources/journals:** → `references/project-standards.md`
**Every source confirmed real before inclusion. Flag grey literature. Flag thin base (<3 studies). "I don't know" → gap list.**

---

## Pre-Flight: Project Files First

Before any web search, consult project files in this order:

1. Normalise the query to a slug (e.g. `grab-bar-height|MOB`).
2. Call `research-log-manager` CHECK with the slug.
3. Act on the result:
   - `COMPLETE` — load the BPC section from `best-practices-compendium.md`. Skip to Step 6 (Synthesize) using stored findings. Do not run web search.
   - `PARTIAL` — load available BPC section. Proceed to Steps 1–5 for missing languages only. Merge new findings with stored findings at Step 6.
   - `STALE` — load available BPC section for context. Run full search (all 14 languages). Replace stale entry at LOG.
   - `NOT FOUND` — proceed to Step 1 below. Full search required.

**No web search is to be initiated until project files have been consulted and a `NOT FOUND` or `STALE` result returned.**

---

## Steps

### Step 1 — Query Generation
Generate English query + native-language queries for all 14 languages. Identify relevant source types per language matrix (Step 3).

### Step 2 — Academic Databases (English only)
Search PubMed (clinical/OT), Consensus (cross-discipline), and Scholar Gateway (built environment) **in English only**. Tag all results `[DB: PubMed|Consensus|SG][LANG: EN]`.

> Rationale: PubMed and Consensus index predominantly English-language literature. Searching in other languages on these platforms produces unreliable or null results. Non-English academic literature is captured via web search in Step 3.

### Step 3 — Web Search: All 14 Languages (mandatory)

Search every language in the matrix below. Every language **must** be searched before the run is considered complete. Do not stop early because English sources appear sufficient.

| Language | Primary sources / corpora |
|----------|--------------------------|
| English | ADA, AustralianStandards, ISO, WHO, NICE, AOTA, CAOT |
| French | CEREMA, ANPIHM, OPHQ (Quebec), Ergothérapie France, Belgian AWIPH |
| Dutch | NEN, BNA, Ergotherapie Nederland, Flemish Agentschap |
| Danish | DS/SBi, Bygningsreglementet (BR18), Servicestyrelsen |
| German | DIN 18040, BMAS, Bundesfachstelle Barrierefreiheit, DVSE |
| Spanish | ONCE, DAE-España, CONADIS (MX/AR/CO), IMSERSO |
| Portuguese | NBR 9050 (BR), DL 163/2006 (PT), Associação Portuguesa de Ergoterapia |
| Chinese | GB 50763, JGJ 50, MCA China, HK BD Code of Practice |
| Japanese | MLIT barrier-free law (改正バリアフリー法), DINF Japan, National Institute on Disability |
| Korean | Welfare Facilities Standard (장애물 없는), KODDI, KS B ISO |
| Swedish | BFS/BBR, Boverket, Scandinavian J Occupational Therapy, Hjälpmedelsinstitutet |
| Norwegian | TEK17, Statsbygg, SINTEF, Ergoterapeutene |
| Finnish | Accessibility Decree 241/2017, THL, STAKES, Valteri |
| Italian | DM 236/89, Linee guida CNAPPC, CNR-ITIA |

### Step 4 — Translation and Tagging
Translate non-English findings to English. Tag `[LANG: XX][TRANSLATED]`. Flag untranslatable regulatory concepts with a parenthetical explanation.

### Step 5 — Cross-Language Evaluation
Cluster semantically equivalent findings. Flag divergent conclusions (expected; κ ≈ 0.30 — surface all divergence, suppress nothing).

### Step 6 — Synthesize

**Consensus findings** (≥2 independent sources, cross-language consistent): `Finding | Sources | Tier`
**Language-divergent findings:** `Topic | Lang A finding | Lang B finding`
**Emerging/single-source** (flag as preliminary): `Finding | Source | Lang`
**Evidence gaps:** `Gap | Languages searched | Search terms`
**Source list:** `# | Authors | Year | Title | Journal | Lang | Tier | DOI`

---

## Post-Run: Log Updates (mandatory)

After completing synthesis, call `research-log-manager LOG`. All writes to `search-log.md` and `best-practices-compendium.md` are handled by `research-log-manager` via GitHub API — do not write directly.

---

## Evidence Hierarchy
Apply the following tiers consistently. Tag every source.

| Tier | Type |
|------|------|
| 1 | Systematic review or meta-analysis |
| 2 | RCT or controlled study |
| 3 | Cohort, cross-sectional, or case-control study |
| 4 | Expert consensus, clinical guideline, professional standard |
| 5 | Grey literature, regulatory document, single case report |

Lived experience evidence is co-primary at Tier 3–4 where no clinical trial is feasible. Do not subordinate lived experience to clinical research on experiential outcomes.

---

## Token Efficiency Rules
- Batch web searches by language family (Nordic · Romance · Asian · English) for parallelism.
- Do not stop early based on source count. All 14 languages must be searched.
- Return up to 20 sources total; prioritise by tier then cross-language diversity.
- If a language produces only NO-DATA or THIN results after a genuine search attempt, log it and move on — do not expand search time on that language beyond one attempt per slug.
- Apply CMOP-E/MOHO/PEOP framing where relevant.
