<!-- SUPERSEDED 2026-05-11 -->
> **⚠ SUPERSEDED:** This workplan is replaced by `audits/bpc-rewrite-workplan-2026-05-11.md` (ADOPTED 2026-05-11 in session_2026-05-11h, per PI v10.8 standing rule #6). Jurisdiction sweep work is now §Phase C (Coverage axis expansion) and is scoped to 46 jurisdictions per PI v10.8 standing rule #9. Do not use for forward work. Preserved here as historical record. See `audits/bpc-rewrite-workplan-2026-05-11.md` §Appendix E for the full supersession map.

---

# Workplan: Jurisdiction & Code Sweep
**Created:** 2026-04-23
**Scope:** Fill jurisdiction/code gaps across standards registry, BPC, item specifications, and spec database
**Workflow:** Multilingual Research (full) + Item Specification + jurisdiction-tracker
**Effort:** 150 (cross-jurisdictional synthesis — per effort-guide.md)
**Model:** Sonnet 4.6 (search, extraction) · Opus 4.6 (best-practice synthesis only)

---

## Executive Summary

### Current State
| Asset | Jurisdictions covered | Canonical target | Gap |
|---|---|---|---|
| Standards Registry | 26 | 46 | **20 jurisdictions zero entries** (all CO-0005 Tier A/B) |
| BPC files (78 total) | Variable; ~14–16 per mature slug | 46 | **8+ jurisdictions explicitly flagged "not searched"** in jurisdiction-matrix BPC; most topic slugs have <12 jurisdictions |
| Part 4 Evidence Tables (91 items) | Dominated by UK/US/AU/DE/ISO | 46 | **~30 jurisdictions absent** from evidence basis tables |
| Spec Database JSON | batch 1 only (10/76 BPC) | 76 BPC files | `jurisdictions_supporting` / `jurisdictions_divergent` uncurated |
| Search Logs | Per-topic dirs exist | 46 per slug | Per-jurisdiction tracking completeness unknown for most slugs |

### Missing Jurisdictions (23 with ZERO standards-registry entries)
**CO-0005 Tier A (10):** IN · ZA · MX · CL · CR · ID · BD · NG · PH · EG
**CO-0005 Tier B (12):** KE · TH · CO · AR · PE · GT · EC · UY · MA · GH · TZ · ET
**Pre-CO-0005 gap (1):** BE

### Jurisdiction Tiers for Prioritisation
| Priority | Jurisdictions | Rationale |
|---|---|---|
| P1 — Core | US · UK · AU · CA · DE · NO · SE · ISO · EU | Most evidence; existing standards-registry entries; highest item-specification impact |
| P2 — Extended European | FR · CH · NL · DK · FI · BE · IE · ES · IT · PT | EN 17210 transposition states; some registry entries exist |
| P3 — Asia-Pacific | JP · SG · NZ · KR · CN | Existing registry entries but thin coverage in BPC |
| P4 — Tier A Global South | IN · ZA · MX · CL · CR · ID · BD · NG · PH · EG | Zero registry entries; CO-0005 mandate |
| P5 — Tier B Global South | KE · TH · CO · AR · PE · GT · EC · UY · MA · GH · TZ · ET | Zero registry entries; CO-0005 mandate; expect THIN/NO-DATA for most |

---

## Phase 1: Standards Registry Expansion
**Goal:** Every canonical jurisdiction has ≥1 standards-registry entry with current primary accessibility code.
**Skill:** `jurisdiction-tracker` (effort 75)
**Estimated sessions:** 4

### Phase 1A — Verify + Update Existing 26 Jurisdictions (1 session)
Status check all 80 existing entries. Some are from 2026-03-18 — nearly 5 weeks old.
Focus: entries with `status: UPDATED` or `status: SUPERSEDED` (20 entries).
Deliverable: Updated standards-registry.md with fresh `last_checked` dates.

### Phase 1B — Belgium (Pre-CO-0005 Gap) (0.5 session)
Belgium is the only original-24 jurisdiction with no entry. Has distinctive federal/regional structure (Flanders, Wallonia, Brussels).
Target standards:
- Vlaamse regelgeving toegankelijkheid (Flanders)
- Code wallon (Wallonia)
- RRU urbanisme (Brussels-Capital)

### Phase 1C — CO-0005 Tier A (10 jurisdictions) (1.5 sessions)
| Jurisdiction | Expected primary standard | Language |
|---|---|---|
| IN | MoHUA Harmonised Guidelines 2021 + RPwD Act 2023 | EN/HI |
| ZA | SANS 10400-S:2011 | EN |
| MX | NOM-233-SSA1-2003 + NMX-R-050-SCFI-2006 | ES |
| CL | DS 50/2015 (Ley 20.422) | ES |
| CR | Ley 7600 + Reglamento | ES |
| ID | Permen PUPR 14/2017 | ID |
| BD | Bangladesh National Building Code 2020 | EN/BN |
| NG | Nigerian Building Code 2006 | EN |
| PH | BP 344 (Accessibility Law) + NBC 2005 | EN |
| EG | Egyptian Building Code (accessibility chapter) | AR |

### Phase 1D — CO-0005 Tier B (12 jurisdictions) (1 session)
| Jurisdiction | Expected primary standard | Language |
|---|---|---|
| KE | Kenya Building Code 2009 | EN |
| TH | Ministerial Regulation on facilities for disabled persons 2005 | TH |
| CO | NTC 6047:2013 | ES |
| AR | Ley 24.314 + Decreto 914/97 | ES |
| PE | RNE Norma A.120 | ES |
| GT | Reglamento de Construcción (Guatemala City) | ES |
| EC | NEC-11 + Ley Orgánica de Discapacidades | ES |
| UY | Ley 18.651 + UNIT 200 | ES |
| MA | Loi 10-03 relative à l'accessibilité | FR/AR |
| GH | Ghana Building Code | EN |
| TZ | No known standalone standard | EN/SW |
| ET | Ethiopian Building Proclamation | EN/AM |

Expected outcome: Many P5 jurisdictions will return THIN or NO-DATA. Record attempt; do not block.

---

## Phase 2: BPC Jurisdiction Enrichment
**Goal:** Every BPC slug's search-log records per-jurisdiction search status for all 46 jurisdictions. BPC consensus findings updated where new jurisdiction data changes synthesis.
**Skill:** `multilingual-research` (effort 150) + `research-log-manager` (effort 75)
**Estimated sessions:** 18–24

### Phase 2A — Audit Current Per-Jurisdiction Coverage (2 sessions)
For each of the 78 BPC files:
1. `research-log-manager CHECK` → extract per-jurisdiction tier coverage record
2. Build master matrix: slug × jurisdiction → status (SEARCHED | THIN | NO-DATA | NOT-RUN)
3. Identify highest-yield gaps: slugs with <12 jurisdictions searched AND high item-specification impact

Deliverable: `references/jurisdiction-coverage-audit-2026-04.md` — machine-readable matrix.

### Phase 2B — P1 Core Jurisdiction Backfill (6–8 sessions)
Systematic pass through BPC slugs where P1 jurisdictions (US/UK/AU/CA/DE/NO/SE/ISO/EU) show NOT-RUN.
Process per session (target 4–5 slugs/session):
1. `research-log-manager CHECK` for slug
2. Load native terms from Keyword Compendium
3. Run Steps 1–3 of multilingual-research for missing P1 jurisdictions
4. `citation-miner` for any new Tier 1–3 sources
5. Pre-LOG completeness check
6. `research-log-manager LOG`
7. Flag for Opus synthesis if findings change consensus

Priority order by item-specification impact:
1. **Category A slugs** (acoustics) — `acoustics-speech-intelligibility-disability`, `room-acoustic-performance`, `deaf-acoustic-built-environment`, `deaf-classroom-reverberation-time`
2. **Category E slugs** (entrances/circulation) — `accessible-circulation-geometry`, `residential-entry-and-threshold`, `stair-ramp-threshold-biomechanics-accessibility`, `threshold-and-level-access`, `threshold-door-hardware`
3. **Category B slugs** (lighting) — `circadian-lighting-melanopic-edi`, `therapeutic-lighting-design`
4. **Category G slugs** (bathrooms) — `accessible-bathroom-and-grab-bar`, `fold-down-grab-bar-specification`
5. **Category C/D slugs** (colour/wayfinding) — `luminance-contrast-lrv-evidence-base`, `cognitive-wayfinding-design`, `wayfinding-dementia-spatial-design`
6. **Category F slugs** (sensory/thermal) — `sensory-relief-space-design`, `air-quality-voc-chemical-sensitivity-built-environment`, `thermoregulation-built-environment`
7. **Category H/K slugs** (controls/kitchens) — `reach-range-and-accessible-controls`, `residential-kitchen-and-task-surfaces`
8. **Population-general slugs** — all 12 population BPC files

### Phase 2C — P2 Extended European Backfill (4–5 sessions)
Same process for FR/CH/NL/DK/FI/BE/IE/ES/IT/PT.
Focus: EN 17210 transposition mapping — which member states have adopted EN 17210 as mandatory vs. voluntary?
Cross-check against `jurisdiction-matrix-accessibility-standards.md` "not yet searched" list.

### Phase 2D — P3 Asia-Pacific Backfill (2–3 sessions)
JP/SG/NZ/KR/CN. Existing registry entries exist but BPC coverage is thin.
Language barrier highest here — JA/KO/ZH terms from Keyword Compendium critical.

### Phase 2E — P4/P5 Global South Pass (4–6 sessions)
CO-0005 Tier A then Tier B. Expect many THIN/NO-DATA outcomes.
Special protocol:
- Record attempt even when empty
- Flag `co1-housing-research-global-south` and `sensory-space-global-south` BPC slugs as primary targets
- Cross-check `wayfinding-global-south` and `bathroom-typology-global-south` BPC slugs
- For each jurisdiction: record whether CRPD ratified + any CRPD concluding observations mentioning built environment

---

## Phase 3: Item Specification Jurisdiction Enrichment
**Goal:** Every Part 4 item's Evidence Basis table cites jurisdiction-specific codes where they diverge from best practice.
**Skill:** `item-specification-writer` (effort 125)
**Estimated sessions:** 12–15

### Phase 3A — Jurisdiction Divergence Mapping (2 sessions)
For each of the 91 items, map:
- Which jurisdictions specify a value for this parameter?
- Where do values diverge? (e.g., ramp gradient: ADA 8.3% vs DIN 6.7% vs France 5%)
- Which items have NO jurisdiction-specific values at all?

Build: `references/item-jurisdiction-divergence-matrix.md`

### Phase 3B — Category-by-Category Enrichment (10–13 sessions)
One session per category. For each item:
1. Cross-reference BPC jurisdiction data (from Phase 2 enrichment)
2. Add jurisdiction-specific code references to Evidence Basis table
3. Where values diverge: add row showing jurisdiction, standard, divergent value
4. Where jurisdiction exceeds best practice: note as potential upgrade
5. Tag each new entry with evidence marker (● for cited standard, ○ for inferred)

Session plan:
| Session | Category | Items | Est. jurisdiction refs to add |
|---|---|---|---|
| 3B-1 | A (Acoustics) | A-01 to A-17 | ~80 (many standards: BB93, DIN 18041, AS/NZS 2107) |
| 3B-2 | B (Lighting) | B-01 to B-11 | ~50 (EU EN 12464, AS 1680, DIN 5035) |
| 3B-3 | C (Colour/Contrast) | C-01 to C-06 | ~30 (BS 8300, DIN 32975, AS 1428.1) |
| 3B-4 | D (Wayfinding) | D-01 to D-11 | ~40 (PAS 6463, DIN 32984, AS 1428.4) |
| 3B-5 | E (Entrances/Circulation) | E-01 to E-15 | ~100 (highest divergence; turning radii, ramp grades, lift sizes) |
| 3B-6 | F (Sensory/Thermal) | F-01 to F-08 | ~35 (WELL Standard, ASHRAE 55, EN 16798) |
| 3B-7 | G (Bathrooms) | G-01 to G-08 | ~60 (AS 1428.1, DIN 18040-2, BS 8300-2) |
| 3B-8 | H (Controls) | H-01 to H-04 | ~25 (reach range standards differ significantly) |
| 3B-9 | I (Seating/Rest) | I-01 to I-02 | ~15 |
| 3B-10 | J (Room Types) | J-01 to J-02 | ~15 |
| 3B-11 | K (Misc) | K-01 to K-03 | ~15 |

### Phase 3C — Divergence Synthesis Notes (1–2 Opus sessions)
For items with ≥3 jurisdictions specifying different values:
- Opus synthesises which jurisdiction's approach is most evidence-informed
- Result feeds Part 5 (Building-Level Co-Occurrence Resolution) and Appendix A

---

## Phase 4: Specification Database Curation
**Goal:** `jurisdictions_supporting` and `jurisdictions_divergent` fields populated for all spec records.
**Skill:** Sonnet inline (extraction from Phase 2–3 outputs)
**Estimated sessions:** 4–6

### Phase 4A — Complete Batch Extraction (2–3 sessions)
Spec database currently has batch 1 only (10/76 BPC files). Complete extraction for remaining 66 BPC files.
Target: batches 2–4 per schema.

### Phase 4B — Jurisdiction Field Curation (2–3 sessions)
For each spec record:
1. Map `jurisdictions_supporting` from Phase 3A divergence matrix
2. Map `jurisdictions_divergent` with specific divergent values
3. Cross-validate against standards-registry entries

---

## Phase 5: Cross-Cutting Deliverables

### 5A — Appendix A Update: Jurisdiction Comparison Tables (2 sessions)
Update Appendix A with comprehensive jurisdiction comparison tables for:
- Turning radii (ISO/ANSI/CSA/DIN/AS/NCC)
- Ramp gradients (ADA/DIN/TEK17/FR/AS)
- Lift car dimensions (EN 81-70/ADA/AS 1735)
- Grab bar heights (BS 8300/DIN 18040/AS 1428.1/ADA)
- Hearing loop standards (BS 8300/ADA/IEC 60118-4)
- Contrast requirements (BS 8300/DIN 32975/AS 1428.1)
- Reach ranges (ADA/BS 8300/DIN 18040)

### 5B — Standards Supersession Tracker (1 session)
Build automated check: which Part 4 items cite a SUPERSEDED standard version?
Cross-reference Part 4 evidence tables against standards-registry `status` field.
Generate correction list.

### 5C — CRPD Ratification + Concluding Observations Map (1 session)
For all 46 jurisdictions: CRPD ratification date, concluding observations mentioning built environment/housing.
Feeds Part 1 §1.3 and Part 12.

---

## Session Sequencing

### Dependencies
```
Phase 1 (Standards Registry) ──→ Phase 2B-E (needs registry for Tier 6 lookup)
Phase 2A (Audit) ──→ Phase 2B-E (prioritises which slugs to enrich)
Phase 2B-E (BPC enrichment) ──→ Phase 3B (items need BPC jurisdiction data)
Phase 3A (Divergence mapping) ──→ Phase 3B (items need divergence matrix)
Phase 3B (Item enrichment) ──→ Phase 4B (spec-db needs item jurisdiction data)
Phase 2 + Phase 3 ──→ Phase 5A (Appendix A needs both)
```

### Recommended Execution Order
| Block | Phase | Sessions | Cumulative |
|---|---|---|---|
| 1 | 1A + 1B (verify existing + Belgium) | 1.5 | 1.5 |
| 2 | 1C (Tier A Global South registry) | 1.5 | 3 |
| 3 | 1D (Tier B Global South registry) | 1 | 4 |
| 4 | 2A (jurisdiction coverage audit) | 2 | 6 |
| 5 | 2B sessions 1–4 (P1 core backfill: Cat A/E slugs) | 4 | 10 |
| 6 | 2B sessions 5–8 (P1 core backfill: Cat B/G/C/D/F/H/K + pop-general) | 4 | 14 |
| 7 | 3A (divergence mapping) | 2 | 16 |
| 8 | 2C (P2 Extended European) | 4 | 20 |
| 9 | 2D (P3 Asia-Pacific) | 2 | 22 |
| 10 | 3B sessions 1–6 (Cat A–F item enrichment) | 6 | 28 |
| 11 | 3B sessions 7–11 (Cat G–K item enrichment) | 5 | 33 |
| 12 | 2E (P4/P5 Global South BPC) | 5 | 38 |
| 13 | 3C (Opus divergence synthesis) | 2 | 40 |
| 14 | 4A + 4B (Spec database curation) | 5 | 45 |
| 15 | 5A + 5B + 5C (Cross-cutting deliverables) | 4 | 49 |

**Total estimated sessions: 45–55**

### Parallelisation Opportunities
- Phase 1 (registry) and Phase 2A (audit) can run in same session — different skills, no dependency
- Phase 5C (CRPD map) can run alongside any Phase 2 session
- Phase 4A (spec-db extraction) can run alongside Phase 2 sessions (no shared writes)

---

## Quality Gates

### Per-Session Exit Criteria
- [ ] All search-log entries updated with per-jurisdiction status
- [ ] Standards-registry entries created for any new jurisdiction touched
- [ ] `research-log-manager LOG` completed for every slug researched
- [ ] Citation-miner run for every new Tier 1–3 source discovered
- [ ] Pre-LOG completeness check passed (46 jurisdictions, co1_pass, native aliases)
- [ ] Opus synthesis flagged where consensus finding changes

### Phase-Level Exit Criteria

**Phase 1 complete when:**
- [ ] 46/46 jurisdictions have ≥1 standards-registry entry (THIN/NO-DATA acceptable for P5)
- [ ] All existing entries have `last_checked` within 30 days

**Phase 2 complete when:**
- [ ] Jurisdiction coverage audit matrix shows SEARCHED/THIN/NO-DATA for all 78 slugs × 46 jurisdictions
- [ ] Zero NOT-RUN entries for P1/P2/P3 jurisdictions on item-specification-mapped slugs
- [ ] BPC consensus findings updated where new data changes synthesis

**Phase 3 complete when:**
- [ ] All 91 Part 4 items have ≥5 jurisdiction-specific code references in Evidence Basis tables
- [ ] All divergent values documented with jurisdiction + standard + divergent value
- [ ] Divergence synthesis notes drafted for items with ≥3 conflicting jurisdictions

**Phase 4 complete when:**
- [ ] All 76 BPC files extracted to spec-db (batches 1–4)
- [ ] `jurisdictions_supporting` and `jurisdictions_divergent` populated for all records

**Phase 5 complete when:**
- [ ] Appendix A jurisdiction comparison tables cover all 7 parameter categories
- [ ] Supersession tracker identifies all Part 4 items citing outdated standards
- [ ] CRPD map covers all 46 jurisdictions

---

## Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| P4/P5 jurisdictions have no locatable accessibility standard | Many THIN/NO-DATA outcomes | Record attempt; note CRPD ratification status as minimum |
| Language barrier for AR/HI/BN/SW/AM terms | Missed sources in non-Latin script jurisdictions | Keyword Compendium verification; flag [UNVERIFIED-TERMS] per CO-0005 |
| Standards-registry entries become stale during 49-session sweep | Outdated data in early entries | Re-verify P1 jurisdiction entries every 10 sessions |
| Opus synthesis backlog from Phase 2 BPC changes | `opus_synthesis: false` propagates to items | Batch Opus sessions between Phase 2 and Phase 3 |
| Part 4 token limit (~63K) constrains per-item enrichment | Cannot load full Part 4 for cross-item consistency | Use part04-item-index.md line ranges to load targeted chunks |
| DIN 18040 revision published mid-sweep | Supersedes current registry entry | Monitor DIN/BfB news; update registry immediately |
| project-standards.md at 96% capacity | Cannot add new rules if needed | Consolidate or archive obsolete rules before sweep begins |

---

## Relation to Existing Workplan Items

This workplan is a **new phase** (Phase C) extending the completed Phase A (BPC assembly) and Phase B (validation/CI). It operates on the Phase A frozen corpus and enriches it with jurisdiction depth.

It does NOT modify the Phase A frozen tag. All enrichment commits go to `main` HEAD, post-freeze.

It complements but does not replace:
- Step 2 citation tagging (in progress — 13% complete)
- GREY DOI resolution (~28 remaining — requires institutional access)
- B5 hallucination audit follow-up (~45 GREY pre-publication items)

---

## Metrics

Track weekly:
- Jurisdictions with ≥1 standards-registry entry: **current 26/46**
- BPC slugs with ≥24 jurisdiction statuses recorded: **current ~0/78**
- Part 4 items with ≥5 jurisdiction code refs: **current ~15/91** (estimated)
- Spec-db records with jurisdiction fields populated: **current 0/143** (batch 1 uncurated)
