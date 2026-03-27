# Decision Register — P1-D3: Parts 8–13 + Appendices
## Editorial Decisions — Session 3

**Session:** Phase 1 Session 3
**Date:** 2026-03-27
**Status:** DRAFT — requires author approval before any Phase 2 work begins.
**Basis:** v9.0 parts 7–14 · D1-29–D1-34 (Part 8 scope) · DEC-08–DEC-21 · Connection Register · Gap Register · Workplan v10.2 · Critique Report v9.0

---

## Pre-Analysis: v9.0 Structural Issues (Parts 8–13)

Critical numbering errors inherited from v9.0 that affect every decision below:

| Error | Location | Fix |
|---|---|---|
| Part 9 (Engineering) uses §9.x numbering correctly | — | No change needed |
| Part 10 (Consultants) uses §9.x numbering internally (wrong) | L15: "9.1 Three-Tier Hierarchy", L31: "9.2 OT" | Renumber → §10.x in Phase 4 |
| Part 11a (DAR) and Part 11b (Economics) both labelled "Part 11" | Two separate parts with same number | DAR → Part 11; Economics → Part 12; Case Studies → Part 13. Phase 4. |
| Part 12 (Case Studies) would become Part 13 | After above renumber | Confirmed |
| Economics uses §11.x; should be §12.x after renumber | Throughout | Phase 4 renumber |
| Appendix D currently = Emergency Evacuation. F-02 policy note needs Appendix D slot | Conflict | Emergency Evacuation → Appendix E; F-02 Fragrance-Free Policy → Appendix D |
| Appendix E (OT Framework) does not yet exist | D1-10 moved §1.8 content here | Create in Phase 3 |

---

## Part 8 — Cross-Population Resolution & Cross-Disciplinary Collaboration (NEW)

*Confirmed structure from D1-29–D1-34: §8.1 Purpose · §8.2 Methodology · §8.3 Priority Hierarchy · §8.4 Conflict Resolutions · §8.5 Unresolvable/Zoning · §8.6 Handoff Protocols · §8.7 Collaboration by Stage · §8.8 Worked Examples*

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D3-01 | §8.1–§8.3 | **WRITE FROM SCRATCH** — ~300 words. Purpose, methodology, priority hierarchy (population safety > population dignity > universal provision). | No source content in v9.0. Core doctrine for Part 8. |
| D3-02 | §8.4 Conflict Resolutions | **SOURCE:** §3.4 (12 entries confirmed) + connection register HIGH findings (CON-0014: B-10/DEAF strobe vs NEU/NDV seizure; CON-0017: user-control convergence; CON-0001: circulation legibility Tier 0) + item-level conflict notes scattered through Part 7. **Target: 20–25 entries.** Grouped by environmental domain: acoustic (~5), thermal (~4), visual (~3), spatial (~4), sensory/cognitive (~4), multi-domain (~3–5). | D1-32. Source is §3.4 + connections, not phantom Part E. |
| D3-03 | §8.5 Unresolvable / Zoning | **KEEP CON-0014 as primary example.** B-10 (DEAF strobe) vs NEU/NDV (seizure risk from strobe) is the paradigm case of a genuinely unresolvable cross-population conflict — resolved only by zoning and user control (H-02). Add 2–3 further examples from connection register MODERATE findings. | CON-0014 explicitly flagged as §8.5 content. |
| D3-04 | §8.6–§8.7 Handoff + Collaboration | **~50% existing content relocated from Part 10** (OT, dementia specialist, DeafSpace, sensory consultant, accessibility auditor briefs). **~50% new:** per-discipline handoff checklists; trigger points by design stage; shared vocabulary glossary per discipline. | D1-33. Part 10 becomes leaner after content moves here. |
| D3-05 | §8.8 Worked Examples | **CONFIRM DEC-14: 3 examples.** (a) Residential bathroom: MOB+PAIN thermal conflict → OT + M&E resolution. (b) Education classroom: DEAF+NDV acoustic conflict → acoustic + sensory consultant resolution. (c) Healthcare ward: DEM+VIS+OFS multi-domain → full team resolution. Covers residential/NR/healthcare and simple/moderate/complex. | D1-34. DEC-14 preliminary confirmed. |

---

## Part 9 — Engineering and Coordination

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D3-06 | §9.0–§9.3 | **KEEP — strong content.** Engineering Coordination Register (§9.1), Brief Templates (§9.2), Stage-Gated Protocol (§9.3) are all well-structured and largely Phase 3-ready. | No structural issues. |
| D3-07 | §9.1.4 Mechanical Engineering Items | **ADD TC-02+TC-03 combined item** per DEC-06: "Thermal Envelope and Mass — Passive Thermal Performance." Existing content references TC items by appendix; relocate substance here. | TC-02+TC-03 relocation from Appendix C. |
| D3-08 | §9.2 Brief Templates | **ADD I-04 (Ceiling Hoist) to Structural Engineer brief (§9.5).** Currently §9.5 Structural Engineer exists but has no ceiling hoist provision. Add: structural blocking specification, dead load requirement (≥200 kg/m²), and coordination with M&E for 13A spur. | I-04 is CD-CRITICAL and requires structural coordination brief. |
| D3-09 | §9.4 O&M Manual | **KEEP.** Accessibility systems O&M is underused in practice; retaining signals its importance. Minor update: add H-05 (nurse call) to systems list. | Good content, low edit burden. |
| D3-10 | §9.5 Structural Engineer | **EXPAND** — currently sparse (2 paragraphs). Add: ceiling hoist blocking protocol (see D3-08), grab bar backing specification, structural implications of zero-threshold drainage channels (G-04). | Three items in Part 7 have structural implications not yet documented in §9.5. |

---

## Part 10 — Interdisciplinary Design Team (reconceived)

*Note: Part 10 internally uses §9.x numbering — renumber to §10.x in Phase 4.*

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D3-11 | Overall scope | **RECONCEIVE.** Current Part 10 = detailed consultant briefs (OT, dementia, DeafSpace, sensory, accessibility auditor). After D3-04, §8.6–§8.7 absorbs the per-discipline handoff protocols and cross-population collaboration content. Part 10 becomes: how the IDT is assembled, governed, and sequenced — not what each consultant does in detail. | Part 8 takes the cross-population detail. Part 10 becomes team governance. |
| D3-12 | §10.1 Three-Tier Hierarchy and Consultant Appointment | **KEEP + CONDENSE** — retain appointment trigger logic; remove per-consultant detail (moves to §8.6). ~150 words max. | Trigger logic belongs here. Scope detail → §8.6. |
| D3-13 | §10.2–§10.6 Individual consultant sections | **CONDENSE to single summary table** per consultant: Role · Appointment trigger · Design stage · Relationship to Part 8. Remove extended scope descriptions (→ §8.6). | After §8.6 absorbs the detail, these sections are redundant at length. One summary table replaces 5 sections. |
| D3-14 | §10.5 OT-Architect Interface (DEC-15) | **MODERATE DETAIL.** Retain: OT assessment report format (§9.2.4 in v9.0 — brief format headings are practically useful); co-design protocol (§9.2.5 — CRPD Art. 4.3 obligation); relationship to Tier 2 design (§9.2.6). Remove: extended scope lists already in §8.6. | OT-Architect interface is the most practically important relationship. Brief format and co-design protocol are tools practitioners use directly. |
| D3-15 | §10.7 Coordination Protocol + §10.8 Disability Organisations | **KEEP BOTH** — sequencing, architect coordination responsibility, documentation, VE protection scope, and lived experience input are all valuable and don't duplicate Part 8. | Not covered by §8.6 (which focuses on cross-population conflict resolution, not team governance). |

---

## Part 11 — Design for Adaptable Readiness (DAR)

*Note: In v9.0 this is labelled Part 11 but a second "Part 11" (Economics) also exists. After Phase 4 renumber: DAR stays Part 11; Economics → Part 12.*

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D3-16 | §11.0–§11.7 | **KEEP — no structural changes.** DAR Cost Multiplier Framework, CAN/ASC 2.8, Lifetime Homes 16, Visitability 3-criterion, Aging in Place OT evidence, Nordic models, and case study evidence are all well-structured and current. | Strong content. Standards current as of January 2026 (already noted). |
| D3-17 | DAR mandatory at every tier | **ADD explicit callout box** in §11.0: "DAR provisions are mandatory at Tier 0, 1, and 2. The three-tier hierarchy does not reduce DAR requirements." | Current text is implicit. The callout makes the standing rule unambiguous. |
| D3-18 | I-04 (Ceiling Hoist) DAR entry | **ADD to §11.1 DAR Cost Multiplier Framework table**: Ceiling hoist tracking, ×20–40 retrofit multiplier, CD-CRITICAL, consistent with new Part 7 item I-04. | I-04 is the second-highest retrofit multiplier — must appear in the multiplier table. |

---

## Part 12 — The Economics of Accessible Construction

*Becomes Part 12 after Phase 4 renumber (was Part 11b in v9.0).*

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D3-19 | DEC-08: §12.4 Cost tables — restructure? | **KEEP STRUCTURE; UPDATE REFERENCES ONLY.** §11.4 (current numbering) cost intelligence tables are well-structured, with NC Premium + Retrofit ×NC + Decision Stage columns. No restructure needed. Phase 3 actions: (1) update B-03/04 → B-03; (2) update TC-05 ref (now F-07); (3) add I-04 ceiling hoist row to §12.4.2 Bathroom; (4) add F-06 (thermal zoning) row to §12.4.6; (5) remove TC-05 row (now F-07); (6) update F-02 reference to Appendix D policy note. | Tables are high-quality. Reference updates only — no restructure. CON-0031+CON-0032 add evidence for existing rows, not new rows. |
| D3-20 | DEC-16: Pro forma templates — which building types? | **5 building types:** Residential (standard) · Residential (supported/care) · Healthcare (acute ward) · Education (primary school) · Office/commercial. Rationale: covers the five highest-prevalence accessible design contexts. Hospitality and retail are lower-frequency and more variable. Pro formas: 1-page per type with NC Premium total, key trigger items, and decision stage gate. | DEC-16 resolved. 5 is tractable in Phase 3 economics session. 7 would be excessive. |
| D3-21 | DEC-17: ROI model — practitioner-facing or developer-facing? | **DUAL-AUDIENCE with explicit labelling.** §12.8.1 (client conversations) serves both. Add explicit sub-sections: "For OT practitioners making the case to clients" and "For developers/clients evaluating the brief." Same evidence base; different framing. | Neither audience should be excluded. The evidence (CON-0031, CON-0032 fall reduction 1:2.2–1:14.9) works for both framings. |
| D3-22 | DEC-18: Grant programmes — all 24 jurisdictions or top 8? | **Top 10 jurisdictions** by guidebook evidence coverage: UK · Canada · Australia · USA · Germany · Netherlands · Sweden · Norway · France · Singapore. Full grant inventory for these 10. Brief note for remaining 14: "Jurisdiction-specific programmes exist — consult national disability organisations." | 24 full entries would be stale within 12 months. Top 10 are where the evidence base is strongest. |
| D3-23 | CON-0031/CON-0032 integration | **ADD to §12.1.2 (What Evidence Shows):** environmental gerontology cost-effectiveness (CON-0031) and Clemson 2023 Cochrane fall reduction cost ratio 1:2.2–1:14.9 (CON-0032). These are the strongest ROI citations in the guidebook. | Workplan v10.2 flagged these explicitly as Phase 12 input. |

---

## Part 13 — Case Studies and Built Evidence

*Becomes Part 13 after Phase 4 renumber (was Part 12 in v9.0).*

| ID | Element | Decision | Rationale |
|---|---|---|---|
| D3-24 | DEC-09: Keep all 14 + expand | **CONFIRMED: Keep all 14. Expand with up to 6 new.** 14 existing studies are high quality. New studies target populations underrepresented in current 14: PAIN/OFS (0 dedicated studies), NDV/MH (0 dedicated), NEU/ABI (0 dedicated). Target 3 new studies minimum for these populations; 3 optional from cross-population or economics evidence. Total target: 17–20. | Phase 2B case study sourcing session. |
| D3-25 | DEC-19: Target populations for new case studies | **Priority populations:** (1) PAIN/OFS — no existing studies; FDR confirmed NOVEL findings available. (2) NDV/MH — no existing studies; CON-0015 TID evidence. (3) NEU/ABI — no existing studies. (4) Cross-population (MOB+DEM+NDV compound) — only 1 indirect (BC Housing HAFI). Secondary: economics-focused study showing ROI at building scale. | Populations with 0 current representation take priority. |
| D3-26 | DEC-20: Add "Evidence Contribution" field to case study template? | **YES — ADD.** Each case study should explicitly state: what new evidence it contributes to Part 7 items (item codes referenced), evidence tier of the contribution, and whether it confirms, supplements, or contradicts existing BPC entries. Aligns case studies to endnote pipeline. | Makes case studies active evidence contributors, not just illustrative examples. Enables bibliography-compiler to include them in REF pipeline. |
| D3-27 | Case study template revision | **Add fields:** Evidence Contribution (item codes + tier + confirms/supplements/contradicts) · Population codes · Building type · Country/jurisdiction · Design stage documented · Year completed. Remove: the existing "Note on Methodology" preamble (integrate into §13.0 intro). | Consistent template across all 20 studies enables cross-reference resolution. |

---

## Appendices

| ID | Appendix | Decision | Rationale |
|---|---|---|---|
| D3-28 | Appendix A — Global Standards Catalogue | **KEEP — UPDATE IN PHASE 3.** jurisdiction-tracker skill runs once per edition to flag superseded standards. Run before Phase 3 Session 18. | Well-structured. Standards currency check required before assembly. |
| D3-29 | Appendix B — Biophilic Design (BIO) | **REFORMAT to Part 7 item template** per DEC-06 (already decided). Fix stale "Part 11I §8.4" references throughout. No content changes. | DEC-06 committed. |
| D3-30 | Appendix C — Thermal Comfort (TC) | **RETIRE.** TC-01→F-06; TC-04→F-04; TC-05→F-07; TC-02+TC-03→Part 9 combined. Appendix C becomes empty shell — delete. CO-0003 handles this. | DEC-06 committed. |
| D3-31 | Appendix D — Emergency Evacuation (current) | **RENUMBER → Appendix E.** F-02 Fragrance-Free Policy needs Appendix D slot (DEC-12). Emergency Evacuation content is unchanged — renumber only in Phase 4. | Slot conflict created by DEC-12 modification. |
| D3-32 | Appendix D (new) — Management and Operational Guidance | **CREATE.** First entry: F-02 Fragrance-Free Environment Policy (populations NDV, PAIN, MH, OFS/MCAS; safety-critical for anaphylactic OFS; cross-ref F-04, F-01). Template for future operational guidance entries. | DEC-12 committed. Appendix D now exists as a category. |
| D3-33 | DEC-10: Appendix E — OT Framework | **CREATE as Appendix E** (after Emergency Evacuation renumbers from D → E). Wait — this creates a collision: Emergency Evacuation renumbers to E, and OT Framework also needs to be E. **Resolution: OT Framework → Appendix F.** Emergency Evacuation stays D (no renumber needed if F-02 gets its own dedicated section within Appendix D rather than displacing it). | See revised Appendix structure below. |

### Revised Appendix Structure

| Appendix | Content | Status |
|---|---|---|
| A | Global Standards Catalogue | Existing — update |
| B | Biophilic Design (BIO-01–05) | Existing — reformat |
| ~~C~~ | ~~Thermal Comfort~~ | **RETIRED** |
| D | Management and Operational Guidance | **NEW** — F-02 policy + future entries |
| E | Emergency Evacuation | Existing — renumber from D to E |
| F | Theoretical Frameworks (OT) | **NEW** — relocated from §1.8 per D1-10 |
| Bibliography | Master Bibliography | Existing |
| Glossary | Core Concepts + Codes + Abbreviations + Frameworks | Existing |

**DEC-10 RESOLVED: Appendix F (Theoretical Frameworks).** Not merged into Glossary — the framework descriptions (~500 words) are substantive clinical background, not definitional terms.

---

## New Decision Added

| ID | Question | Resolved |
|---|---|---|
| DEC-21 | Worked examples placement: Part 4 §4.5 or Appendix F? | **Part 4 §4.5.** Worked examples are the primary pedagogical tool for applying Part 4 synthesis principles — they belong in the body, not an appendix. Appendix F is OT framework content (clinical background). No collision. |

---

## Post-D3 Structural Summary

### Part Renumbering (Phase 4)

| v9.0 label | v10 label | Notes |
|---|---|---|
| Part 8 | Part 8 (new) | Cross-Population Resolution — written from scratch |
| Part 9 | Part 9 | Engineering — keep; §9.5 expanded |
| Part 10 | Part 10 | Consultants — reconceived; §9.x → §10.x renumber |
| Part 11 (DAR) | Part 11 | DAR — keep; minor additions |
| Part 11 (Economics) | Part 12 | Economics — keep; reference updates + pro formas |
| Part 12 (Case Studies) | Part 13 | Case studies — keep + expand |
| Bibliography + Glossary | Vol III back matter | Keep |
| Appendix A | Appendix A | Keep + update |
| Appendix B | Appendix B | Reformat |
| Appendix C | ~~RETIRED~~ | — |
| Appendix D (Evac) | Appendix E | Renumber |
| — | Appendix D (new) | Management + Operational Guidance |
| — | Appendix F (new) | OT Theoretical Frameworks |

### Writing Scope Assessment (Parts 8–13)

| Part | New writing | Relocation | Edit only |
|---|---|---|---|
| Part 8 | §8.1–8.3 (~300w), §8.4 expansions (~8 new entries), §8.8 (3 examples) | §8.4 (from §3.4), §8.6–8.7 (from Part 10) | — |
| Part 9 | §9.5 expansion, TC-02+TC-03 item in §9.1.4 | — | Reference updates |
| Part 10 | — | §8.6 absorbs detail | Condense to table format |
| Part 11 DAR | DAR callout box, I-04 row | — | None |
| Part 12 Economics | CON-0031+32 paragraphs, 5 pro formas, ROI dual-audience framing, top-10 grants | — | Reference updates in §12.4 |
| Part 13 Case Studies | 3–6 new studies, Evidence Contribution field in all 20 | — | Template standardisation |
| Appendices | Appendix D (new), Appendix F (new) | Appendix B reformat, Appendix E renumber | Appendix A update |

---

## Decisions Resolved (P1-D3)

| ID | Decision | Status |
|---|---|---|
| DEC-08 | §12.4 Cost tables — restructure? | RESOLVED (D3-19: keep structure; reference updates only) |
| DEC-09 | Case studies — keep all 14 + expand | RESOLVED (D3-24: keep 14 + up to 6 new; target 17–20) |
| DEC-10 | Appendix E — separate appendix or glossary expansion? | RESOLVED (D3-33: Appendix F, not E; not merged into glossary) |
| DEC-14 | Part 8 §8.8 worked examples count | RESOLVED (D3-05: 3 examples confirmed) |
| DEC-15 | Part 10 §10.5 OT-Architect Interface detail level | RESOLVED (D3-14: moderate detail; retain brief format + co-design protocol) |
| DEC-16 | Pro forma templates — which building types? | RESOLVED (D3-20: 5 types) |
| DEC-17 | ROI model — practitioner or developer facing? | RESOLVED (D3-21: dual-audience with explicit labelling) |
| DEC-18 | Grant programmes — all 24 or top 8? | RESOLVED (D3-22: top 10) |
| DEC-19 | Target populations for new case studies | RESOLVED (D3-25: PAIN/OFS · NDV/MH · NEU/ABI priority) |
| DEC-20 | Case study template — add Evidence Contribution field? | RESOLVED (D3-26: YES) |
| DEC-21 | Worked examples placement — Part 4 §4.5 or Appendix F? | RESOLVED: Part 4 §4.5 |

---

## Cumulative Totals (D1 + D2 + D3)

| Metric | Value |
|---|---|
| Total decisions resolved | 96 (D1: 34 + D2: 40 + D3: 22) |
| Pending author approval | DEC-08 through DEC-21 (this register) |
| Parts with structural changes | 8, 10, 11b/12, 12/13 |
| Parts with reference updates only | 9, 11a/11 |
| New appendices | D (Management), F (OT Frameworks) |
| Retired appendices | C (Thermal Comfort) |
| Renumbered appendices | D (Evac) → E |
| New writing sessions required | Part 8 (+1 session); Economics pro formas (+partial session); Case study expansion (Phase 2B Session 8) |
| Phase 1 gate | Decision Register complete — **all DEC-01 through DEC-21 resolved pending author approval** |

*End of P1-D3 Decision Register Draft*
