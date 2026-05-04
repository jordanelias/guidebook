# Session: 2026-05-03 Economics Audit + Citation Mining (Sessions 1-2)

## session_open
- **Date:** 2026-05-03
- **Model:** Opus 4.6
- **Phase:** B1 Economics audit + cross-jurisdictional research + citation mining
- **Prior session:** session_2026-05-02-b1-s9.md (B1 Phase 1 COMPLETE — schema design)

## session_close
- **Date:** 2026-05-03
- **Commits:** ~24 total across 2 chat sessions

### Session 1 (10 commits: 720e296 → 1d5fef2)
- Full audit of economics methodology doc (v1.6→v1.8)
- CMHC cost correction (6-12%, not "few hundred to few thousand")
- Throughline 1 re-tiering (E-08, E-12, G-08, kitchen → Tier 2)
- CvV ROI reframing (absolute comparison lead)
- TERRAGON commercial interest flagged
- UK Dec 2025 M4(2) 40% mandate
- NEN 9120:2025 confirmed published
- Ielegems 2019 full report retrieved (scale-dependent costs)
- Canadian institutional landscape mapped (9 provincial programmes)
- Sirmans forward-citation: hedonic gap confirmed

### Session 2 (14 commits: 7efb82a → 649b1e3 + 4 integration)
- Habinteg £27K traced to contractor estimates
- LSE "Living not Existing" 2023: M4(3) BCR 4.3-5.6:1
- DCWC cost correction (Silver AUD $3,874, not $538)
- DaltonCarter counter-analysis to CIE RIS
- Japanese 3-paper Tsuchiya-Ito chain (LTC ¥200K, 28% LTCF reduction)
- Chandola & Rouxel 2022 Lancet: curb-cut effect empirically demonstrated
- Keall NZ RCT chain: 26-31% fall reduction, 9:1 BCR at NZD $500
- Cochrane review: 21% falls reduction (6 RCTs)
- CAPABLE US: $1,300/person, ~10:1 Medicaid savings
- Dual-read thesis established (Throughline 1A)
- Spanish Law 6/2022 Cognitive Accessibility
- Swedish Fänge & Iwarsson longitudinal
- Integration: methodology v1.9, BPC files updated

### Integration commits
- db71925: methodology doc v1.9 (evidence hierarchy + Throughline 1A)
- 741b832: construction-cost-data (CCD-07 through CCD-11)
- 16fcab1: government-grant-programmes (JP/UK/NZ/US/AU/SE)
- 3377197: economics-sources (20+ verified citations)

## next_action
1. Part 11 §11.3 update with Q5 evidence (Keall, Chandola, CAPABLE, Tsuchiya-Ito)
2. §15 extraction to separate analytical document (Change Order required)
3. Cha et al. 2025 MDPI systematic review (new lead)
4. Whitehead BATH-OUT, Hollinghurst 2022 (lower priority deferred leads)
5. Ishikawa & Koike 2008 Japanese-language study (multilingual research)

## blockers
None.

## decisions
- D-0141: Throughline 1 items re-tiered (E-08, E-12, G-08, kitchen → Tier 2; D-05, accessible bedroom → Tier 1-2)
- D-0142: CvV ROI reframed with absolute comparison lead
- D-0143: CMHC primary source corrected to 6-12% per dwelling
- D-0144: Throughline 1A (dual-read thesis) established
- D-0145: Four-pillar economic case framework adopted
- D-0146: Citation mining established as continuous research practice

## key_synthesis
The economic case for accessible housing rests on four pillars ranked by evidence strength: (1) Health outcomes — 9-10:1 BCR from RCT and quasi-experimental data across NZ and US; (2) Cost-of-inaction — 5-20× retrofit penalty; (3) Construction cost when designed in — 0.4-1.9% for basic visitability; (4) Market value — no revealed-preference evidence, but dual-read thesis reframes the question. The hedonic gap is a labeling problem: accessible features are consumed as mainstream desirable features (NAHB 2024 mapping confirms 60-72% buyer preference). Cross-jurisdictional convergence across 12 jurisdictions strengthens confidence. The Chandola 2022 Lancet study provides the strongest empirical evidence for the curb-cut effect in residential housing.

### Session 3 (2 commits: audit + partition)
- Comprehensive audit of all economics/financial data files (13 files reviewed)
- Identified architecture: 3 analytical frameworks (Q/V taxonomy, four-pillar case, §15 perceptual-value crossover)
- Evidence strength assessment per pillar (health outcomes STRONG, cost-of-inaction STRONG, construction cost MODERATE-STRONG, market value WEAK)
- 11 gaps identified and ranked (critical: hedonic premium, Co-1, non-US CvV equivalent)
- Partitioned monolithic economics-research-methodology.md (v1.9, 1,624 lines) into 6 throughline-organized files
- TERRAGON commercial-interest note added
- Version footer mismatch corrected
- Original archived as v1.9-archived

### Session 3 continued (4 more commits: schema alignment + cross-refs + gap resolution)
- economics.json restructured to match unified-data-schema.md conventions
- Entity 5 expanded from 3 to 7 sub-entities (5a–5g) in schema
- 171 spec_cross_refs populated across cost_premiums, health_outcomes, throughlines
- GAP-ECON-05 (Missing Part 11 cost tables) resolved — tables exist in Part 11 v10
- ER diagram updated with new economics relationships
- part11_cost_table_map added linking 12 cost table sections to item codes
- Interactive React dashboard created (economics-dashboard.jsx)

## session_close
2026-05-04 01:10

## next_action
1. Co-1 verification pass — populate lived-experience economic perspectives (GAP-ECON-02)
2. Unverified source-name sweep (~40 pattern-matched entries) (GAP-ECON-04)
3. Part 11 §11.3 update with Q5 evidence (Keall, Chandola, CAPABLE, Tsuchiya-Ito)
4. §15 extraction to separate analytical document (Change Order required)
5. Populate spec_cross_refs on remaining cost_premium records (CP-004, CP-007, CP-008) when spec database exists

## blockers
None.

## decisions
- D-0147: Economics methodology partitioned by economic throughlines (health outcomes, cost-of-inaction, construction cost, market value) rather than by original section numbering
- D-0148: TERRAGON AG commercial-interest disclosure added to construction-cost throughline
- D-0149: Website data integration via schema-aligned JSON in references/website/data/ (not Wix)
- D-0150: Entity 5 expanded from 3 sub-entities (5a-5c) to 7 (5a-5g) with four-pillar framework
- D-0151: GAP-ECON-05 resolved — Part 11 v10 already contains the four missing cost tables
