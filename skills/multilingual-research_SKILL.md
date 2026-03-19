---
name: multilingual-research
description: >
  Conduct accessibility research across 14 languages (Chinese, Danish, Dutch, Finnish, French,
  German, Italian, Japanese, Korean, Norwegian, Portuguese, Spanish, Swedish, and English) and
  synthesize findings in English. ALWAYS use this skill when asked to: research accessibility
  topics, find international evidence, search non-English literature, conduct literature reviews,
  find international standards or guidelines, or gather evidence for accessibility guidebook
  sections. Occupational therapy is the primary lens. Trigger on: "research", "find evidence",
  "what does the literature say", "international standards", "review the evidence", "find studies on".
---

**Intake:** Focused query required. Ambiguous scope → ask one clarifying question before proceeding.
**Model:** Sonnet 4.6 with web search.
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Every source confirmed real before inclusion. Flag grey literature. Flag thin base (<3 studies). "I don't know" → gap list.**

---

## Pre-Flight: Research Log Check

Before beginning any search, call `research-log-manager CHECK`:
1. Normalise query to slug: lowercase, spaces→hyphens, `|<population-code>`.
2. If COMPLETE and <90 days → load sources → skip to Synthesize.
3. If PARTIAL → search missing languages only → update log.
4. If STALE → re-run full search.
5. NOT FOUND → proceed to Step 0.

---

## Step 0 — Native-Language Vocabulary Lookup (mandatory)

Before generating any search queries:

1. Call `keyword-lookup` with: slug, target population code(s), all 14 language codes.
2. Receive native-language terms for the target concept — these are terms of art used by practitioners, researchers, and regulators in each jurisdiction, **not** translated English.
3. Use these native terms as the primary search strings for each language. Do not substitute English translations.
4. Where a native concept has no English equivalent (e.g., German *Barrierefreiheit*, Norwegian *universell utforming*, Finnish *esteettömyys* vs *saavutettavuus*), preserve the native concept and document it in synthesis. Never flatten to the English term.

---

## Step 1 — Query Generation

Generate native-language queries for all 14 languages using terms from Step 0. Identify relevant source types per language matrix below. English query generated last, not first.

---

## Step 2 — Multi-Pass Search (order is mandatory; do not reorder)

### Pass A — Co-1 / Tier 2: Disability-Led Organisations (run first)

For each language, search the relevant disability-led organisation's publications directly using native-language terms. This pass precedes all academic database searches without exception.

**Primary Co-1 / Tier 2 targets by language:**

| Language | Organisation targets |
|---|---|
| EN | RNID, CNIB, HLAA, DeafSpace/Gallaudet, MEAction, Sense UK, NDCS, Disability Rights UK, RCOT, AOTA (2022 Position Statement), WFOT, AT2030 |
| SV | Hörselskadades Riksförbund (HRF), Dövas Riksförbund (SDR), Synskadades Riksförbund, DHB (deaf-blind SV) |
| NO | Norges Døveforbund, Norges Blindeforbund, FFO (Funksjonshemmedes Fellesorganisasjon), Ergoterapeutene, SAFO |
| DA | Danmarks Døveforbund, Dansk Blindesamfund, LEV (intellectual disability), Muskelsvindfonden |
| FI | Kuuloliitto, Näkövammaisten Liitto, Kehitysvammaliitto, Autismiliitto, Rinnekoti (deafblind) |
| FR | APF France Handicap, UNAPEI, UNISDA (Deaf France), AVH (Aveugles de France), CFHE, Autisme France |
| DE | DBSV (blind/VIS), Bundesvereinigung Lebenshilfe, Bundesverband der Gehörlosen (BDG), Bundesfachstelle Barrierefreiheit, Deutsche Gesellschaft für Ergotherapie |
| ZH | China Disabled Persons' Federation (CDPF), HK Joint Council for People with Disabilities, Deaf Association HK, Taiwan Deaf Association |
| JA | Japan Federation of the Deaf (JFD), DINF Japan, Japan Blind Union, Japanese Society of Occupational Therapy, Japan ME/CFS Association |
| NL | Dovenschap, Oogvereniging, Ergotherapie Nederland, Platform VG, Ieder(in) |
| ES | ONCE, CNSE (Confederación Estatal de Personas Sordas), CERMI, FEAPS, CONADIS (MX/AR/CO) |
| PT | FENEIS (Brazil Deaf), Fundação Dorina Nowill (VIS), APECDA (Portugal Deaf), ACAPO (Portugal blind), Movimento de Vida Independente |
| KO | Korean Deaf Association, KODDI, Korea Welfare Foundation, National Rehabilitation Centre (NRC), AutismKorea |
| IT | ENS (Ente Nazionale Sordi), UICI (blind/VIS), Fish disability federation, Fand, Autismo Italia |

**Additional jurisdictions — always include:**

| Jurisdiction | Organisation targets |
|---|---|
| Ireland (IE) | Centre for Excellence in Universal Design (CEUD), NDA (National Disability Authority), DeafHear Ireland, NCBI (blind/VIS), AsIAm (autism IE) |
| Singapore (SG) | SgEnable, Disabled People's Association (DPA), Singapore Association of the Deaf (SADeaf), SAVH (VIS), BCA (Building and Construction Authority) |
| South Africa (ZA) | SABS accessibility, Disabled People South Africa (DPSA), Deaf Federation of South Africa (DEAFSA) |
| India (IN) | NCPEDP, Disabled Rights Initiative, AICB (blind), National Deaf Association India |
| New Zealand (NZ) | Deaf Aotearoa, Blind Foundation NZ, Lifemark NZ, CCS Disability Action |
| Australia (AU) | Deaf Australia, Blind Citizens Australia, Summer Foundation, Centre for Universal Design Australia (CUDA) |

---

### Pass B — Native-Language Standards

Search the national standards body in each language using native-language terms. Targets:

| Language | Standards sources |
|---|---|
| EN | ADA, ADA Standards 2010, ISO 21542:2021, EN 17210:2021, AS 1428 (AU), NBC (CA), BS 8300:2018 (UK), Building Regulations Part M (IE) |
| SV | BFS/BBR (Boverket), AFS 2009:2 (workplaces) |
| NO | TEK17, Statsbygg, NS 11001-1:2018 |
| DA | DS/SBi-anvisning, Bygningsreglementet BR18 |
| FI | Accessibility Decree 241/2017, SuRaKu guidelines, RT accessibility cards |
| FR | Arrêté du 20 avril 2017, CEREMA guides, OPHQ (Quebec) |
| DE | DIN 18040-1/2/3, DIN 32984 (TWSI), DIN VDE 0828 (hearing loop) |
| ZH | GB 50763-2012, JGJ 50-2001, HK BD Code of Practice on Barrier Free Access |
| JA | Barrier-Free Law 2006/2018, MLIT guidelines, JIS T 9251, JIS C 1503 |
| NL | NEN 1814, BNA guidelines |
| ES | CTE DB SUA, UNE 41500 series, LISMI/LGDPD |
| PT | NBR 9050:2020 (BR), DL 163/2006 (PT) |
| KO | Welfare Facility Standard, BF Act 2006, KSF 3011 |
| IT | DM 236/89, DPR 503/1996, UNI EN 17210 |
| IE | Building Regulations Part M:2010, CEUD "Building for Everyone" series (10 booklets), NDA Technical Guidance |
| SG | BCA Accessibility Code 2019, Universal Design Mark (UD Mark), BCA Design for Buildability |

---

### Pass C — Academic Databases

Search in this order. Tag each result `[DB: name][LANG: XX]`.

**English academic databases (all runs):**
- OTseeker — OT intervention evidence; filtered for design (free; HIGH priority)
- PubMed — clinical/OT
- Consensus — cross-discipline
- CINAHL — allied health; OT environmental adaptation
- Scholar Gateway — built environment
- EMBASE — European biomedical (priority for European-language runs)
- SCOPUS — architecture + built environment journals
- Web of Science — use for forward citation tracking

**Language-specific academic databases:**

| Language | Databases |
|---|---|
| JA | J-STAGE (open access), CiNii |
| ZH | CNKI (Chinese academic) |
| KO | RISS (Korean academic) |
| PT | BDTD (Brazilian theses) |
| FR | OpenEdition (French social sciences) |
| DE | REHADAT (AT + workplace adaptation; free); BASE |
| Multi | BASE (Bielefeld Academic Search Engine; multi-language) |

**OT and occupational science journals (search directly when slug is OT/OS adjacent):**
- AJOT (American Journal of Occupational Therapy)
- BJOT (British Journal of Occupational Therapy)
- Scandinavian Journal of Occupational Therapy
- CJOT (Canadian Journal of Occupational Therapy)
- OTJR: Occupation, Participation and Health
- Journal of Occupational Science (OS; distinct evidence base from OT clinical)
- HERD (Health Environments Research & Design) — healthcare POE

**AT and adjacent databases (when slug involves AT-built environment interface):**
- ABLEDATA (AT database)
- OTseeker AT filter
- Rehadat-international.org

---

### Pass D — Grey Literature (always run)

For each jurisdiction, the following sources have been identified as unsearched; include in all relevant runs:

| Jurisdiction | Source |
|---|---|
| CA | Wavefront Centre for Communication Accessibility |
| CA | CMHC Housing Design Catalogue |
| CA | CNIB Access Labs (lived experience testing) |
| UK | Centre for Accessible Environments (CAE) technical guides |
| UK | Thomas Pocklington Trust (VIS + DEM housing) |
| UK | Housing LIN |
| UK | RCOTSSH GenHOME project |
| IE | CEUD "Building for Everyone" (10 booklets — all relevant to built environment) |
| IE | NDA Technical Guidance Documents |
| SG | SgEnable built environment guidance |
| SG | BCA Universal Design resource library |
| US | isUD database (500+ evidence-based UD solutions) |
| US | IDeA Center / Wheeled Mobility Database |
| AU | Summer Foundation (younger people in aged care housing) |
| AU | Centre for Universal Design Australia (CUDA) |
| NZ | Lifetime Design NZ |
| ZA | SANS 10400 Part S (SABS) |
| IN | Harmonised Guidelines 2021 (RPwD 2016); Bureau of Indian Standards |
| Global | DbI (Deafblind International) — primary DBL Tier 2 authority |
| Global | AT2030 publications |

---

### Pass E — Forward/Backward Citation Mining (mandatory for all confirmed Tier 1–2 sources)

For every confirmed Tier 1–2 source retrieved in Passes A–D:
1. **Backward pass:** read reference list; identify any sources directly relevant to the slug that have not yet been retrieved.
2. **Forward pass:** Google Scholar "Cited by" — identify papers that have cited this source since publication; assess top 10 for relevance.
3. Log citation mining counts in BPC entry (`citation_mining` fields).

This is standard PRISMA methodology ("Identification from other methods"). It is mandatory, not optional.

---

## Step 3 — Translation and Tagging

Translate non-English findings to English. Tag: `[LANG: XX][TRANSLATED]`. Flag untranslatable concepts with parenthetical explanation in English. Preserve native concepts that have no English equivalent — document them.

---

## Step 4 — Cross-Language Evaluation

Cluster semantically equivalent findings. Do not privilege any language's framing. Flag divergent conclusions (κ ≈ 0.30 — surface all divergence, suppress nothing). Where native-language frameworks differ conceptually from English-language frameworks (e.g., Norwegian *universell utforming* as a rights-based statutory concept vs. "universal design" as a design philosophy), document the difference rather than collapsing it.

---

## Step 5 — Synthesize

**Consensus findings** (≥2 independent sources, cross-language consistent): `Finding | Sources | Tier`  
**Language-divergent findings:** `Topic | Lang A finding | Lang B finding`  
**Emerging/single-source:** `Finding | Source | Lang` (flag as preliminary)  
**Evidence gaps:** `Gap | Languages searched | Search terms used`  
**Source list:** `# | Authors | Year | Title | Journal | Lang | Tier | DOI`

---

## Post-Run: Log Updates (mandatory)

Call `research-log-manager LOG`. Log must include:
- Per-language status (SEARCHED / THIN / NO-DATA / NOT-RUN)
- Co-1 pass completion: `co1_pass: complete/partial/not-run`
- Native standards pass completion: `native_standards_pass: complete/partial/not-run`
- AT database pass (if run): `at_db_pass: complete/not-run`
- Citation mining: `citation_mining: {backward: N, forward: N, sources_added: N}`

Skipping LOG is an error.

---

## Evidence Hierarchy

Per §1.5 (Volume 1) — canonical; governs all skills and documents. Clinical pyramid is NOT the default.

| Tier | Type |
|---|---|
| 1 | OT clinical research (intervention-tested; person-environment-occupation) |
| Co-1 | Lived experience and participatory design research (CRPD Art. 4.3 — co-primary, not subordinate) |
| 2 | NGO / advocacy organisation guidelines (community-developed; lived experience embedded) |
| 3 | Systematic reviews and meta-analyses |
| 4 | International standards with evidence basis (CRPD Art. 9, ISO, EN, PAS) |
| 5 | Jurisdiction-specific regulatory documents; grey literature; single case reports |

Where sources conflict, higher-tier evidence governs regardless of jurisdiction or citation count.

---

## Token Efficiency

- Batch web searches by language family: Nordic (SV/NO/DA/FI) · West-Central European (FR/DE/NL) · Romance (ES/PT/IT) · East Asian (ZH/JA/KO) · English (EN + IE/SG/AU/NZ/ZA/IN).
- Return ≤20 sources total; prioritise by tier then cross-language diversity.
- NO-DATA or THIN after one genuine attempt: log and move on.
- Early-close gate: **REMOVED**. All 9 core languages must be searched to completion on every run. Extended languages (NL, ES, PT, KO, IT) are included as standard — this is a 14-language system.
