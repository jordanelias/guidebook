# Deep-Dive Systematic Review Protocols
**Date:** 2026-04-09
**Status:** PROTOCOLS DESIGNED — execution across multiple sessions required
**Basis:** PubMed verification of BPC-cited studies + web search confirmation
**Attribution:** Study metadata retrieved from PubMed where indicated.

---

## Verified Study Registry

### Acoustics (Deep-Dive 2)

| Study | PMID | DOI | Design | Key Finding |
|---|---|---|---|---|
| Murgia et al. 2023 | 36260411 | [10.1044/2022_LSHSS-21-00181](https://doi.org/10.1044/2022_LSHSS-21-00181) | Systematic review, 23 studies | RT >0.6s prevents 100% speech perception at any SNR |
| Iglehart 2020 | 31835909 | [10.1044/2019_AJA-19-0010](https://doi.org/10.1044/2019_AJA-19-0010) | Experimental (HA children) | RT 0.3s significantly better than 0.6s and 0.9s for hearing-impaired children |
| Tardini et al. 2025 | [UNVERIFIED] | 10.1016/j.buildenv.2025.113299 | Survey of national target values | Cross-jurisdictional classroom acoustic standards |
| Mealings 2023 | [UNVERIFIED] | Not confirmed | Scoping review | Mainstream classroom acoustics |

### Grab Bars (Deep-Dive 4)

| Study | PMID | DOI | Design | Key Finding |
|---|---|---|---|---|
| Levine et al. 2023 | 34963373 | [10.1177/00187208211059860](https://doi.org/10.1177/00187208211059860) | Experimental, N=63 | Grab bar users 75.8% more likely to recover balance during bathtub transfer |
| Levine 2025 | — | 10.2196/69442 | [PubMed match inconclusive — wrong Levine returned] | Grab bar + JMIR study; needs DOI direct verification |
| Kennedy et al. 2015 | NOT FOUND | [UNVERIFIED] | Experimental | COP deviation — vertical bar preference |
| Nakamura 2009 | NOT FOUND | [UNVERIFIED] | Experimental | Hemiplegic vertical bar positioning |

### LRV Contrast (Deep-Dive 6)

| Study | PMID | DOI | Design | Key Finding |
|---|---|---|---|---|
| Brown et al. 2023 | 36314061 | [10.1080/00140139.2022.2141347](https://doi.org/10.1080/00140139.2022.2141347) | Observational, N=5824 | Step edge highlighters reduced descending gait speed (coeff −0.07, p=.010) |
| Harper et al. 2022 | Same team as Brown | Same paper | — | OR 2.87 for contrast enhancement vs control |
| Thompson 2017/2022 | [UNVERIFIED] | PMC8993136 | Computational modelling | Low-contrast nosings invisible at moderate VI levels |

### Thermoregulation (Deep-Dive 5)

| Study | PMID | DOI | Design | Key Finding |
|---|---|---|---|---|
| Griggs 2019 | [PubMed match was wrong paper] | [NEEDS DOI VERIFICATION] | Review/experimental | SCI thermoregulation — Tcore rises to 37.7°C at 23.9°C indoor |
| Hayashi & Naito 2022 | [AMBIGUOUS — 2398 results] | [NEEDS DOI VERIFICATION] | Review | SCI sweating capacity: tetraplegia ~30%, thoracic paraplegia ~57% |
| Burini 2018 | NOT FOUND | [NEEDS DOI VERIFICATION] | Review | 0.5°C core temp rise triggers MS pseudoexacerbation |
| Davis 2010 | NOT FOUND | [NEEDS DOI VERIFICATION] | — | 60-80% MS heat sensitivity prevalence |
| Flensner 2011 | NOT FOUND | [NEEDS DOI VERIFICATION] | — | MS temperature sensitivity |
| Chaseling 2022 | [AMBIGUOUS] | [NEEDS DOI VERIFICATION] | Survey | pwMS identify A/C as primary thermal strategy |

**Critical note on thermoregulation:** 4 of 6 BPC-cited studies could not be confirmed via PubMed citation lookup. These may be in non-PubMed-indexed journals, may have slightly different citation details in the BPC, or may require DOI-based lookup. **Before committing these to the guidebook bibliography, all 6 must be DOI-verified.** This is a [GAP] to log.

---

## PRISMA Search Protocols

### Protocol DD-2: Acoustic RT60/STI Thresholds

**Research question (PICO):**
- P: People with hearing loss (sensorineural, conductive, device users) in built environments
- I: Controlled reverberation time (RT60) and/or speech transmission index (STI)
- C: Standard/uncontrolled acoustic environments
- O: Speech intelligibility/perception scores

**Databases:** PubMed, Scopus, Web of Science, ASA Digital Library
**Grey literature:** ANSI/ASA S12.60, BB93 (UK), ISO 3382, IEC 60118-4
**Search terms:**
```
Cluster 1: (reverberation time OR RT60 OR "speech transmission index" OR STI)
Cluster 2: (hearing loss OR hearing impairment OR deaf OR "hard of hearing" OR "hearing aid" OR "cochlear implant")
Cluster 3: (speech intelligibility OR speech perception OR speech recognition)
Cluster 4: (classroom OR "built environment" OR indoor OR room)
Combined: C1 AND C2 AND C3
Expanded: C1 AND C3 AND C4
```
**Date range:** 2000-2026 (ANSI S12.60-2002 to present)
**Exclusion:** Non-English unless 14-language protocol activated; animal studies; lab-only without room simulation
**Quality appraisal:** SR → AMSTAR-2; RCT → PEDro; Observational → NOS
**Data extraction:** Author-Year · N · Population (HL type, device) · Setting · RT60 value · STI value · Speech recognition % · Jurisdiction · Evidence tier
**Expected yield:** 20-40 studies (based on Murgia 2023 finding 23 in elementary schools alone; expanded scope to all ages and settings)

### Protocol DD-4: Grab Bar Biomechanics

**Research question (PICO):**
- P: People with mobility impairment, older adults, wheelchair users performing bathroom transfers
- I: Grab bar configuration (height, diameter, angle, bilateral/unilateral, fixed/fold-down)
- C: No grab bar or alternative configuration
- O: Balance recovery, COP deviation, fall rate, transfer independence (FIM)

**Databases:** PubMed, CINAHL, OTseeker, PEDro
**Grey literature:** AOTA home mod CPG (Siebert et al. 2014), RCOT publications, CAOT guidelines
**Search terms:**
```
Cluster 1: (grab bar OR "grab rail" OR "support rail" OR "safety rail" OR handrail)
Cluster 2: (bathroom OR bathtub OR toilet OR shower OR "wet room")
Cluster 3: (fall OR balance OR transfer OR "center of pressure" OR COP OR biomechanics OR "functional independence")
Combined: C1 AND (C2 OR C3)
```
**Date range:** 2000-2026
**Exclusion:** Handrails on stairs (separate domain); grab bars in non-bathroom contexts
**Quality appraisal:** RCT → PEDro; Observational → NOS; Biomechanical → bespoke checklist
**Data extraction:** Author-Year · N · Population · Bar config (height mm, diameter mm, orientation, bilateral) · Setting · Outcome measure · Effect size · Jurisdiction · Evidence tier
**Expected yield:** 10-20 studies [UNVERIFIED — requires database search]

### Protocol DD-5: Thermoregulation Thresholds

**Research question (PICO):**
- P: People with thermoregulation impairment (SCI, MS, FMS, dysautonomia/OFS)
- I: Controlled ambient temperature
- C: Uncontrolled or standard indoor temperature
- O: Symptom exacerbation onset temperature, core temperature rise, functional performance change

**Databases:** PubMed, CINAHL, Cochrane Library
**Grey literature:** WHO HHGL 2018, MS Society publications, SCI rehabilitation guidelines
**Search terms:**
```
Cluster 1: (thermoregulation OR "heat sensitivity" OR "cold sensitivity" OR "thermal comfort" OR "ambient temperature")
Cluster 2: (spinal cord injury OR multiple sclerosis OR fibromyalgia OR dysautonomia OR POTS)
Cluster 3: (indoor OR housing OR "built environment" OR home OR "living environment" OR dwelling)
Combined: C1 AND C2
Expanded: C1 AND C2 AND C3
```
**Date range:** 2000-2026
**Exclusion:** Exercise thermoregulation only (no resting/indoor component); animal studies
**Quality appraisal:** RCT → PEDro; Observational → NOS; SR → AMSTAR-2
**Data extraction:** Author-Year · N · Condition (SCI level, MS type, FMS) · Ambient temp °C · Core temp response · Symptom measure · Threshold identified · Jurisdiction · Evidence tier
**Expected yield:** 15-30 studies [UNVERIFIED — BPC cites 6 directly; clinical literature likely larger]

### Protocol DD-6: LRV Contrast Empirical Review

**Research question:** What LRV differential thresholds are empirically validated for boundary/hazard detection by people with visual impairment?

**Databases:** PubMed, Scopus, Ergonomics Abstracts
**Grey literature:** CNIB 2024, UK NIHR review, US Access Board guidance, RNIB
**Search terms:**
```
Cluster 1: (luminance contrast OR LRV OR "light reflectance value" OR "visual contrast")
Cluster 2: (visual impairment OR low vision OR "visually impaired" OR ageing OR "age-related" OR dementia)
Cluster 3: (stair OR step OR edge OR boundary OR wayfinding OR hazard OR detection)
Combined: C1 AND (C2 OR C3)
```
**Date range:** 2000-2026
**Expected yield:** 8-15 studies [UNVERIFIED]

### Protocol DD-1: NDV Sensory Qualitative Meta-Synthesis

**Research question:** What sensory environment features do neurodivergent people identify as enabling or disabling in built environments?

**Method:** Thematic synthesis (Thomas & Harden 2008)
**Databases:** PubMed, CINAHL, PsycINFO, Scopus
**Grey literature:** NAS, Amaze/Architecture & Access 2025, PAS 6463 evidence review
**Search terms:**
```
Cluster 1: (autism OR autistic OR neurodivergent OR "sensory processing" OR ADHD)
Cluster 2: (built environment OR architecture OR room OR space OR building OR classroom OR home)
Cluster 3: (experience OR perspective OR perception OR "lived experience" OR qualitative)
Combined: C1 AND C2 AND C3
```
**Inclusion:** Qualitative or mixed-methods studies reporting NDV people's experiences of built environments
**Exclusion:** Clinical sensory processing assessments without built-environment context; intervention studies without participant perspectives
**Quality appraisal:** CASP Qualitative Checklist
**Data extraction:** Author-Year · N · Population (diagnosis, age) · Setting · Method · Key themes · Sensory domains addressed · Built-env features identified
**Expected yield:** 15-30 studies [UNVERIFIED]

---

## Execution Plan

### Session sequence (estimated)

| Session | Task | Deep-Dive | Model | Est. tokens |
|---|---|---|---|---|
| S+1 | PubMed systematic search DD-2 (acoustics) | 2 | Sonnet | Medium |
| S+1 | PubMed systematic search DD-4 (grab bars) | 4 | Sonnet | Medium |
| S+2 | PubMed systematic search DD-5 (thermoregulation) | 5 | Sonnet | Medium |
| S+2 | Web search DD-6 (LRV contrast) | 6 | Sonnet | Low |
| S+3 | PubMed + PsycINFO search DD-1 (NDV qualitative) | 1 | Sonnet | Medium |
| S+3 | Screen and catalogue all results | All | Sonnet | Medium |
| S+4 | Umbrella review: identify existing Tier 3 SRs across all BPCs | 7 | Sonnet | Medium |
| S+5-6 | FDR compound scenarios P1 (FDR-CMP-01, -02, -04, -06) | 5 | Opus | High |
| S+7-8 | FDR compound scenarios P1 cont'd + occupation scenarios | 5 | Opus | High |
| S+9 | Quality appraisal of DD-2 and DD-4 studies | 2, 4 | Sonnet | Medium |
| S+10 | Synthesis writing: acoustic MA + grab bar MA | 2, 4 | Sonnet | Medium |
| S+11 | Synthesis writing: thermoregulation + LRV | 5, 6 | Sonnet | Medium |
| S+12 | NDV qualitative meta-synthesis | 1 | Opus | High |
| S+13 | Realist review protocol design (external execution) | 8 | Opus | Medium |
| S+14 | GRADE-equivalent confidence ratings (disclosure) | — | Sonnet | High |
| S+15 | Evidence density statements per Part | — | Sonnet | Medium |

### GAP items to log

| GAP-ID | Priority | Description |
|---|---|---|
| GAP-DD-01 | P1 | 4 of 6 thermoregulation BPC-cited studies not confirmed via PubMed — DOI verification required before bibliography inclusion |
| GAP-DD-02 | P1 | Levine 2025 (JMIR, doi:10.2196/69442) PubMed lookup returned wrong paper — verify DOI directly |
| GAP-DD-03 | P2 | Kennedy 2015 and Nakamura 2009 (grab bar) not found in PubMed — may be in non-indexed rehabilitation journals |
| GAP-DD-04 | P2 | All deep-dive "expected yield" counts are UNVERIFIED — actual counts require database execution |

---

## Relationship to v2 Assessment

This file operationalises §5.1 of `meta-analysis-feasibility-v2.md`. The 9 ranked investments map to specific protocols above. Investment #8 (realist review) and #9 (Co-1 meta-synthesis MOB/DEAF/DEM) are protocol-design-only at this stage — execution is multi-month external research.

### What this session accomplished

1. **Self-review:** 20 flaws identified in v1; all corrected in v2
2. **Grounded assessment:** 12 canonical BPC files read; coverage matrix used; existing audits referenced
3. **Study verification:** 4 BPC-cited studies confirmed via PubMed; 6+ could not be matched (logged as GAPs)
4. **PRISMA protocols designed:** 5 deep-dives with complete search strategies
5. **Execution plan:** 15-session roadmap for completing all synthesis investments

### What requires next session

1. Commit this file + v2 assessment to GitHub
2. Execute DD-2 (acoustics) PubMed search — highest confidence, most poolable
3. Begin thermoregulation DOI verification for GAP-DD-01
4. Update gap_register.md with GAP-DD-01 through GAP-DD-04
