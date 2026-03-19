---
name: multilingual-research
description: >
  Conduct accessibility research across 14 languages AND 24 jurisdictions using native-language
  conceptual vocabulary, Co-1/Tier 2 sources first, and companion network retrieval. Synthesises
  findings in English with best-practice judgment for each population. ALWAYS use when: researching
  accessibility topics, finding international evidence, conducting literature reviews, gathering
  evidence for guidebook sections. Trigger on: "research", "find evidence", "what does the
  literature say", "international standards", "review the evidence", "find studies on".
  CHECK before / LOG after every run.
---

**Model:** Sonnet 4.6 + web  
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API  
**Governing protocol:** Multilingual Research Protocol v4 (structural role: multilingual research protocol document in project files) — read it before executing any run.  
**Every source confirmed real before inclusion. Flag grey literature. Flag thin base (<3 studies). "I don't know" → gap list.**

---

## Coverage axes — both must be satisfied independently

This skill operates on two axes that are NOT equivalent and cannot substitute for each other:

**Axis 1 — Language (14):** SV · NO · DA · FI · FR · DE · ZH · JA · NL · ES · PT · KO · IT · EN  
**Axis 2 — Jurisdiction (24):** DE · BE · NO · FR · BR · JP · CA · CH · AU · UK · US · EU · ISO · SG · SE · DK · FI · CN · IE · NZ · KR · ES · NL · IT

A completed language pass does not satisfy jurisdiction coverage. EN covers USA, UK, Canada, Australia, Ireland, New Zealand, Singapore — each must be tracked separately. FR covers France, Belgium (FR), Switzerland (FR). DE covers Germany, Switzerland (DE). NL covers Netherlands, Belgium (NL). PT covers Brazil and Portugal. Each jurisdiction must have its own recorded status in the search-log.

---

## Pre-Run (mandatory — every run)

1. **`research-log-manager CHECK`** — normalise slug; if COMPLETE <90 days: load BPC inline and stop. If PARTIAL: identify unsearched languages AND unsearched jurisdictions; run both. If STALE/NOT FOUND: proceed.
2. **Load native terms** — `view` the Keyword Compendium (multilingual keyword reference document in project files), Part 3, for the target slug's concept group. Extract terms for all 14 languages. Do not generate translated terms from memory.
3. **Load companion networks** — `view` the Multilingual Research Protocol v4, §COMPANION NETWORKS, for the slug's population code(s). Identify organisation and scholar nodes as direct retrieval targets.
4. **Load concept boundary warnings** — from the slug's existing search-log entry or Keyword Compendium. Deviations are mandatory.
5. **Build jurisdiction work list** — list all 24 jurisdictions. For each, note: primary language, Co-1 organisations to target (Step 1), Tier 5 beyond-code sources to target (Step 2b), statutory standard to target (Step 2a). This list governs Steps 1–3 — not the language list alone.

> Steps 2–5 are `view` calls or internal planning within this skill. No separate skill call required.

---

## Search Sequence (all 14 languages AND all 24 jurisdictions must complete)

**Step 1 — Co-1 / Tier 2 pass (first; no exceptions)**

For each jurisdiction: retrieve publications from companion network organisation nodes directly using native-language terms. Do not search for organisations via general search — go to their publication pages. Record co1_attempted: true/false per jurisdiction.

Co-1 / Tier 2 targets by jurisdiction (minimum — add population-specific orgs from companion networks):

| Jurisdiction | Primary Co-1 / Tier 2 targets |
|---|---|
| US | DREDF · Disability Rights Advocates · ADAPT · IL movement publications · PVA (mobility) · AFB (vision) |
| UK | Scope · Disability Rights UK · RNID · RNIB · Leonard Cheshire · Muscular Dystrophy UK · DeafBlind UK |
| CA | CADS · ARCH Disability Law · DisAbled Women's Network · BCACL · CNIB · CHHA |
| AU | Physical Disability Australia · Deaf Australia · Vision Australia · Summer Foundation · Blind Citizens Australia |
| IE | Disability Federation of Ireland · DeafHear · NCBI · Independent Living Movement Ireland |
| NZ | Disabled Persons Assembly NZ · Blind Foundation NZ · Deaf Aotearoa |
| SG | SgEnable · SADeaf · SAVH · SPD |
| DE | BAG Selbsthilfe · BVKM · Deutscher Blinden- und Sehbehindertenverband · Bundesverband der Gehörlosen |
| CH | Pro Infirmis · SZB (Schweizerischer Zentralverein für das Blindenwesen) · SGB-FSS |
| FR | APF France Handicap · CFPSAA · FNSF · UNISDA |
| BE | GRIP · Fevlado · Ligue Braille |
| NL | Ieder(in) · Dovenschap · Bartiméus · Koninklijke Visio |
| SE | Förbundet Rörelsehindrade · HRF · SDR |
| NO | Funksjonshemmedes Fellesorganisasjon · Norges Blindeforbund · Norges Døveforbund |
| DK | DH (Danske Handicaporganisationer) · Danmarks Blindesamfund · Danmarks Døveforbund |
| FI | Vammaisfoorumi · Näkövammaisliitto · Kuuloliitto |
| JP | DPI Japan · 日本障害者協議会 · 日本視覚障害者団体連合 · 全日本ろうあ連盟 |
| KR | 한국장애인단체총연합회 · 한국시각장애인연합회 · 한국농아인협회 |
| CN | 中国残疾人联合会 (CDPF) · 中国盲人协会 · 中国聋人协会 |
| BR | FENASP · ABRADEF · Movimento de Vida Independente Brasil |
| ES | CERMI · ONCE · FIAPAS · Confederación FEDER |
| PT | INR · APCB · SNRIPD |
| IT | FISH · ENS · UICI · ANFFAS |
| EU/ISO | Disability Europe / EDF · European Disability Forum (as Tier 2 supranational) |

If a jurisdiction's organisations publish nothing on this slug domain: flag THIN with reason. Do not skip — the attempt must be recorded.

**Step 2a — Statutory standards pass (Tier 6)**

For each jurisdiction, retrieve the primary statutory code. Record tier6_attempted: true per jurisdiction.

| Jurisdiction | Primary statutory standard |
|---|---|
| US | ADA 2010 Standards; ICC A117.1-2017 (note: ICC is Tier 5, not Tier 6) |
| UK | Building Regulations Part M (England); Technical Handbooks (Scotland); Technical Guidance (Wales); Part R (NI) |
| CA | NBC 2020 Part 3.8; provincial building codes (OBC, BCBC); CAN/ASC B651/B652 |
| AU | NCC 2022 Section D / Livable Housing; AS 1428.1:2021 |
| IE | Building Regulations Part M:2010; BS 8300 (adopted by reference) |
| NZ | NZS 4121:2001 (Design for access and mobility); NZBC D1 |
| SG | BCA Accessibility Code 2019 |
| DE | DIN 18040-1/2/3; Landesbauordnungen |
| CH | SIA 500:2009 (Hindernisfreies Bauen); Behindertengleichstellungsgesetz |
| FR | Arrêté du 8 décembre 2014; Code de la Construction (CCH) |
| BE | Toegankelijkheidsverordening (Flanders); Brussels COBAT Title IV; Walloon Code |
| NL | NEN 9120:2025; Besluit bouwwerken leefomgeving (Bbl) |
| SE | BBR / BFS 2024:12; ALM 2 |
| NO | TEK17; NS 11001-1:2018; NS 11005 |
| DK | BR18; DS 3028; SBi-anvisning 230 |
| FI | Accessibility Decree 241/2017; ESKEH protocol |
| JP | MLIT Barrier-Free Law; Housing Performance Indication System |
| KR | 편의증진법 시행규칙 별표1; Welfare Facilities Standard |
| CN | GB 50763-2012; GB/T 37239 |
| BR | NBR 9050:2020; ABNT NBR 16537:2024 |
| ES | CTE DB SUA; UNE 41500 series |
| PT | DL 163/2006; INR acessibilidade guides |
| IT | DM 236/89; Legge 13/1989; UNI EN 17210 |
| EU | EN 17210:2021; EAA (European Accessibility Act) transpositions |
| ISO | ISO 21542:2021; ISO 23599:2019 (tactile); ISO 9386 (lifts) |

**Step 2b — Beyond-code / Tier 5 pass**

For each jurisdiction, retrieve the primary beyond-code framework if one exists. Record tier5_attempted: true per jurisdiction.

| Jurisdiction | Primary Tier 5 source |
|---|---|
| US | ICC A117.1-2017; IDeA Center / Wheeled Mobility Database; Kelsey Inclusive Design Standards; ADA Best Practices Tool Kit |
| UK | BS 8300:2018; Lifetime Homes (Habinteg 2010/2024); Wheelchair Housing Design Guide 3rd ed.; RCOTSS-Housing Adaptations Without Delay 2019; Inclusive Housing Design Guide (Habinteg 2024) |
| CA | RHFAC v4.2 (Rick Hansen Foundation); CMHC Universal Design Guide; CAN/ASC 2.8:2025 (DAR standard) |
| AU | Livable Housing Design Guidelines 4th ed. (Silver/Gold); ABCB Voluntary Standard; UNSW Home Modification Clearinghouse |
| IE | CEUD Building for Everyone series (NDA) |
| NZ | Universal Design guidelines (IHC/CCS Disability Action) |
| SG | BCA Universal Design Mark; Dementia-Friendly Neighbourhood Design Guide (AIC/CLC) |
| DE | VDI 6008; nullbarriere.de guidance; KDA publications |
| CH | SIA 500 commentary; Procap design guides |
| FR | CEREMA Accessibilité guides |
| BE | Inter Handboek Toegankelijkheid (Flanders); CAWaB guide (Wallonia) |
| NL | toegankelijkbouwen.nl (NEN 9120:2025 companion) |
| SE | Boverket guidance; SPSM (Specialpedagogiska skolmyndigheten) for NDV |
| NO | Husbanken veiledere; SINTEF accessibility research |
| DK | SBi-anvisning 230; BUILD (formerly SBi) research |
| FI | Invalidiliitto ESKEH; Asumisen rahoitus- ja kehittämiskeskus (ARA) |
| JP | Housing Performance Indication System Elderly Care Grades 1-5; MLIT 建築設計標準 |
| KR | Seoul Universal Design Guidelines 2022; Ministry of Welfare design guides |
| CN | 住房城乡建设部 beyond-code guidance |
| BR | NUTAU/USP APO research; IBDD guides |
| ES | DALCO criteria; ONCE design guides |
| PT | INR Acessibilidade e Mobilidade para Todos (280-page guide) |
| IT | CNR-ICAR publications; CNAPPC guides |
| EU | EIDD Design for All principles; EDF built environment guides |
| ISO | ISO TC 173 (assistive products); ISO 21542:2021 commentary |

**Step 3 — Academic and specialist databases**

| Database | Languages | Priority |
|---|---|---|
| PubMed · OTseeker · Consensus · Scholar Gateway · CINAHL | EN | All runs |
| EMBASE · SCOPUS | EN / EU | European-language runs |
| REHADAT | DE | All DE runs; OFS/AT slugs all runs |
| J-STAGE · CiNii | JA | All JA runs |
| CNKI | ZH | All ZH runs |
| RISS | KO | All KO runs |
| BDTD | PT | All PT runs; POE slugs |
| OpenEdition | FR | All FR runs |
| BASE | multi | Multi-language synthesis |

**Step 4 — Citation mining (mandatory for every confirmed Tier 1–2 source)**  
Backward: mine reference list. Forward: Google Scholar "cited by". Log counts in BPC `citation_mining` block. Until `citation-miner` skill is built: perform inline.

**Step 5 — `research-log-manager LOG`**  
Mandatory. Skipping is an error. LOG is blocked until pre-LOG completeness check passes (see below).

---

## Pre-LOG Completeness Check (mandatory — executes before every LOG write)

`research-log-manager LOG` must verify all of the following before writing to GitHub. Any failure is a named BLOCKER — do not write; surface the specific failing condition; user must resolve or explicitly accept the gap.

1. **Jurisdiction coverage complete** — all 24 jurisdictions present in `jurisdiction_coverage` block with a recorded status (SEARCHED · THIN · NO-DATA · NOT-RUN). Missing jurisdiction = BLOCKER.
2. **Co-1 attempted** — `co1_attempted: true` for at least 12 of 24 jurisdictions. Fewer than 12 = BLOCKER. The 12 minimum is a floor; full coverage is the target.
3. **Tier 5 attempted** — `tier5_attempted: true` for at least 16 of 24 jurisdictions. Fewer than 16 = BLOCKER.
4. **`best_practice_synthesis` populated** — non-empty `best_practice_synthesis` field in BPC entry. Empty = BLOCKER.
5. **`native_aliases` populated** — all 14 languages present. Any missing = BLOCKER.
6. **`citation_mining` recorded** — backward and forward counts present. May be 0 if no Tier 1/2 sources found, but the field must be present with an explanation if 0.
7. **`co1_pass_summary` populated** — at least one language listed as complete. All `not-run` = BLOCKER.

If all checks pass → write LOG entry with status determined by coverage:
- All 24 jurisdictions SEARCHED + all blockers clear → COMPLETE
- Any jurisdiction NOT-RUN or any blocker accepted by user → PARTIAL (with specific gaps named)
- Explicitly mark BPC as PROVISIONAL if any P1 gaps remain unresolved.

---

## PICO Framing

Begin with population need and functional outcome evidence — not standard values.

1. What does best-practice evidence show is optimal for this population?
2. What do standards require as minimum?
3. What is the gap?
4. What is the design synthesis?

Never anchor search on a standard value then seek confirming evidence.

---

## Mid-Session Checkpointing

After each completed step:
```
CHECKPOINT [YYYY-MM-DD HH:MM] — slug: {slug} — step: {step} — languages complete: {list} — jurisdictions complete: {list} — sources found: {N}
```
Checkpoints must name both languages complete and jurisdictions complete as separate counts.

---

## Synthesis

Group findings by concept cluster, not by language or jurisdiction. For each cluster:

**Best-practice judgment (mandatory — complete before LOG):**
- Most inclusive provision: what most fully removes the barrier for this population?
- Most targeted provision: what gives greatest dignity, specificity, functional accommodation?
- Conflict resolution: what maximises inclusion for the most constrained user?
- Record in BPC `best_practice_synthesis`.

**Concept boundary handling:** Where a warning applies, synthesis for that language opens with the boundary note before findings. Distinguish: (a) genuine empirical divergence; (b) boundary mismatch; (c) regulatory context difference.

**Untranslatable concepts:** Name in native language; explain; do not flatten to English.

**Output format:**

**Consensus findings:** `Finding | Languages confirming | Jurisdictions confirming | Tier`  
**Divergent findings:** `Topic | Lang/Jurisdiction A | Lang/Jurisdiction B | Cause`  
**NO-DATA / THIN:** `Jurisdiction | Language | Reason | Co-1 attempted? | Tier 5 attempted?`  
**Citation mining:** `Source | Direction | New sources added`  
**Source list:** `# | Authors | Year | Title | Journal | Lang | Jurisdiction | Tier | DOI`

---

## Evidence Hierarchy
Per §1.5 (Volume 1) — canonical; governs all skills and documents.

| Tier | Type |
|---|---|
| 1 | OT clinical research — intervention-tested; person-environment-occupation |
| Co-1 | Lived experience and participatory design (CRPD Art. 4.3) — co-primary with Tier 1 |
| 2 | Disability-led NGO / DPO / advocacy guidelines |
| Co-2 | OT clinical practice guidelines |
| 3 | Systematic reviews and meta-analyses |
| 4 | International standards with evidence basis |
| 5 | National beyond-code frameworks |
| 6 | Statutory codes — reference baseline only |

Co-1 and Tier 1 are co-primary in authority. Search order: Co-1/Tier 2 first (Step 1), then Tier 5 (Step 2b), then Tier 6 (Step 2a), then Tier 3/1 (Step 3). This order is non-negotiable.

---

## Token Rules
- Batch web searches by language family (Batch A: SV/NO/DA/FI · Batch B: FR/DE/NL · Batch C: ES/PT/IT · Batch D: ZH/JA/KO).
- EN-jurisdiction pass (US/UK/CA/AU/IE/NZ/SG) runs as Batch E.
- Return ≤16 sources total per slug; prioritise by tier then cross-jurisdiction diversity.
- NO-DATA or THIN after one genuine attempt per jurisdiction: log and move on.
- Checkpoints: 1–2 lines, naming both language and jurisdiction counts.
