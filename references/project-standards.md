# Project Standards
<!-- Managed by session-consolidator. Append new RULE blocks at bottom. Never overwrite existing entries. -->

---

## Core Doctrine (locked)

RULE: Three-Tier Design Hierarchy governs all specifications. Tier 0 = Universal Design / Code Compliance (population-agnostic, fixed values). Tier 1 = Population-Informed Inclusive Design (ranges; median as default). Tier 2 = Person-Specific Co-Design (OT assessment resolves position within Tier 1 range). DAR mandatory at all tiers.
DATE: Established — pre-session

RULE: Universal design is co-extensive with code compliance — the floor, not an aspiration. Inclusive design is the positive aspiration.
DATE: Established — pre-session

RULE: BAR is not a main taxonomy code. Large body size is not a disability. BAR provisions belong in Supplementary Volume Supp. Part 4 only. No BAR reference, cross-reference, heading, or J-code is permitted in Volumes I–II. Delete on sight without replacement or pointer. Category J (J-01–J-05) is struck from Volume II Part 4.
DATE: Established — pre-session; consolidated 2026-03-29

RULE: Specification ranges are not expressions of uncertainty. They are the designed-in bridge between Tier 1 and Tier 2. At Tier 1 use median. At Tier 2 resolve through co-design. Never write a range without specifying which end applies at which tier.
DATE: Established — pre-session

RULE: Lived experience evidence is co-primary at Tier 3–4 where no clinical trial is feasible.
DATE: Established — pre-session

RULE: VIS, DEAF, DBL are three distinct independent population codes. VIS/DEAF as a compound code is an error. DBL ≠ VIS + DEAF. See workplan-orchestrator §Population Codes for full canonical list.
DATE: Established — pre-session; consolidated 2026-03-29

RULE: IntD (Intellectual Disability) is not a standalone population code. IntD provisions are proxied through DEM (wayfinding, cognitive simplicity) and NDV (sensory environment, Easy Read signage). No §2.12, no IntD matrix column, no IntD population code table entry. All IntD specifications carry THIN-BASE disclosure.
DATE: 2026-03-25 19:35; consolidated 2026-03-29

RULE: Biophilic Design (BIO-01–BIO-05) and Thermal Comfort (TC-01–TC-05) are in Appendices B and C respectively. Supplementary Resources A and B struck from Volume II body. No inline BIO- or TC- cross-references in Part 4 specs or room matrices. Single opening notice permitted in volume front matter.
DATE: 2026-03-18 20:10; consolidated 2026-03-29

RULE: The guidebook is a starting framework for professional judgment, not a substitute for it. Population-level specifications (Tier 0 and Tier 1) are necessary but insufficient. Part 1 must state this explicitly as a foundational principle.
DATE: 2026-03-26 16:00

RULE: Conflict resolution protocol (Part 5 and cross-synthesis escalation) operates at Tier 1 only. At Tier 2, conflict resolution is the domain of the OT and the individual through co-design. The guidebook's Tier 2 role is to equip non-OT professionals with decision frameworks and structured approaches — not prescriptive answers.
DATE: 2026-03-26 16:00

---

## Evidence Hierarchy

RULE: Evidence hierarchy is seven tiers (D-18 extension). Tier 1 = OT intervention-tested clinical research; Co-1 = lived experience / participatory design (CRPD Art. 4.3, co-primary with Tier 1); Tier 2 = NGO/DPO/advocacy guidelines; Co-2 = OT professional body CPGs (CAOT, AOTA, RCOT, COTEC, WFOT); Tier 3 = systematic reviews and meta-analyses; Tier 4 = international standards with evidence basis; Tier 5 = national beyond-code frameworks; Tier 6 = statutory codes (reference baseline only). OT body guidelines = Tier 3 with [Tier 3 — CPG] marker.
DATE: 2026-03-19 19:00; consolidated 2026-03-29

RULE: Evidence specification markers. ● (filled circle) = evidence-based specification (Tier 1–6). ○ (empty circle) = inferred from clinical reasoning or expert consensus (gap disclosed). Every specification sentence carries either ● or ○. Unmarked = error.
DATE: 2026-03-20 21:00

---

## Item Code System

RULE: Item codes use bare category prefix only (A-01, B-06, etc.). No volume-part prefix (V2-P8-, V2-PV-, etc.). Item codes are Part-independent and do not change with renumbering.
DATE: Established — pre-session; consolidated 2026-03-29

---

## Citation and Evidence Standards

RULE: All sources must be confirmed real. Unverified claims → [UNVERIFIED — DOI/URL required before publication]. citation-verifier defaults to PROVISIONAL mode.
DATE: Established — pre-session

RULE: G-03 cites Levine 2023 (Human Factors, doi:10.1177/00187208211059860) AND Levine 2025 (JMIR, doi:10.2196/69442). Both required. Replace any "Levine 2024" with both.
DATE: 2026-03-17 21:30

RULE: 2 failed independent searches → delete the unverifiable value (CLOSED-DELETED). Do not accumulate unresolvable UNVERIFIED flags.
DATE: 2026-03-18 19:10

RULE: AOTA Home Modification Practice Guidelines: confirmed edition is Siebert, Smallfield & Stark (2014). Verify if 2023 revision exists before citing as 2023.
DATE: 2026-03-28 18:25

---

## Structural Decisions



RULE: references/toc.md on GitHub is canonical structural record. Structural changes → toc-editor → Change Order → find-and-replace + cross-reference-resolver.
DATE: 2026-03-18 19:00

---

## CO-0003 + CO-0004 Structural Rules
<!-- TRANSITIONAL — remove after CO-0004 propagation pass is complete -->

RULE: CO-0004 Volume Merge and Part renumbering. 2 Volumes: Volume I (Parts 1–9), Volume II (Parts 10–12). Supplementary unchanged. See workplan-orchestrator §CO-0004 for Part Map. CO-0004 supersedes CO-0003 structural provisions; CO-0003 terminology changes remain in full effect.
DATE: 2026-03-29 00:00

RULE: "Cross-population" retired per CO-0003. Use "co-occurring disability" (intra-individual) or "multi-population" (inter-group). Population code notation: `+` = co-occurring in one person; `/` = different people same space.
DATE: 2026-03-28 21:30

RULE: Part 5 (Building-Level Co-Occurrence Resolution) owns building-wide system conflicts. Room-level conflicts → Parts 6/7 inline annotations. Methodology → Part 3 §3.8–§3.9. Items → Part 4. Engineering → Part 8. Consultants → Part 9.
DATE: 2026-03-29 00:00

RULE: Parts 6/7 matrices include inline conflict notes. Format: "Conflict note — [code]: Items [X-NN] and [Y-NN] conflict for [POP+POP]: [description]. Resolution: Part 3 §3.9.N. See Part 5 if building-wide."
DATE: 2026-03-29 00:00

RULE: Part 9 §9.9 and §9.10 contain co-occurrence collaboration protocol and OT appointment threshold. Route there, not Part 5.
DATE: 2026-03-29 00:00

RULE: Slug names are frozen path identifiers — never renamed by CO-0003. Content adopts new terminology; paths unchanged.
DATE: 2026-03-28 21:30

RULE: Part 7 conflict entries tagged [INTRA-INDIVIDUAL], [INTER-GROUP], or [BOTH]. Intra → Tier 2 OT resolution. Inter → Tier 0/1 architectural. Both → state both pathways.
DATE: 2026-03-28 21:30

---

## Research and Evidence Pipeline

RULE: Each slug covers exactly one population. Combined slugs not permitted.
DATE: 2026-03-18 23:30

RULE: 24 jurisdictions canonical (per jurisdiction-tracker §4.7.3). Language and jurisdiction coverage are distinct axes — both satisfied independently. Per-jurisdiction tier coverage record required: status (SEARCHED|THIN|NO-DATA|NOT-RUN), co1_attempted, tier5_attempted, tier6_attempted. Pre-LOG completeness check mandatory (24 jurisdictions, co1_pass_summary, best_practice_synthesis, citation_mining, native_aliases for 14 languages) — fail = BLOCKER. BPC entry PROVISIONAL until all 24 recorded + co1_pass ≥9 languages.
DATE: 2026-03-19 19:28

RULE: Forward + backward citation mining mandatory for every confirmed Tier 1-2 source. Use citation-miner skill (inline = fallback only).
DATE: 2026-03-18 23:00; consolidated 2026-03-29

RULE: Early-close gate permanently removed. All 14 languages searched to completion on every run. Exception: IntD only — early-close active (literature confirmed absent in non-English).
DATE: 2026-03-18 23:00; updated 2026-03-18 15:00

RULE: PICO framing begins with population need and functional outcome evidence — not standard values. Standards at Step 2.
DATE: 2026-03-19 04:08

RULE: Standards registry: BCA Accessibility Code 2025 (SG), NEN 9120:2025 (NL), BFS 2024:12 / ALM 2 (SE) are current editions. Prior editions superseded.
DATE: 2026-03-26 16:30

---

## Endnote and Source Pipeline

RULE: Evidence Priority: BPC best_practice_synthesis governs as primary evidence basis. Raw search results supplement but never override. Contradictions → evidence-auditor.
DATE: 2026-03-27 14:00

RULE: Source Propagation: Every cited source → in-text [REF:{slug}:{NN}] marker → bibliography-compiler → superscript endnote + volume-end endnote list. No source without endnote; no endnote without citation.
DATE: 2026-03-27 14:00; consolidated 2026-03-29

RULE: PROVISIONAL-REF pattern — assign REF-ID positions only after BPC Key sources updated. Never emit final text with provisional positions.
DATE: 2026-03-28 18:25

---

## Session and Process Management

RULE: Flat BPC/SL files frozen — 15 population-level flat files are frozen archives. New research creates per-slug directory entries.
DATE: 2026-03-27 15:45

---

## Functional Deficit Research

RULE: FDR CONTRADICTS resolution — do not delete original BPC claim. Append [CONTRADICTED BY FDR]. Route to evidence-auditor for adjudication.
DATE: 2026-03-27 15:45

RULE: PubMed MeSH "dressing" → "bandages" conflict. Skip PubMed Step 1 for d540/ADL/bedroom scenarios. Go direct to Step 2 (OT practice guidelines).
DATE: 2026-03-28 09:00

---

## Specification Process Rules

RULE: item-specification-writer uses 'shall be' constructions. Always run prose-style-checker before vol2-item-formatter.
DATE: 2026-03-28 18:25

RULE: "Adjustable" is not a universal conflict resolution. Document operability per population. Flag populations who cannot self-adjust. Route to Tier 2 if ambient parameter irreconcilable.
DATE: 2026-03-28 23:45

RULE: Cross-population conflicts searched by CONFLICT DOMAIN (12 environmental parameter conflicts), not by population pair. Aged care POEs richest evidence source.
DATE: 2026-03-28 23:45

RULE: Population-specific design guideline sets developed independently and do not cross-reference conflict points. Check cross-population-conflict-mapper §1 before finalising any single-population spec in shared spaces.
DATE: 2026-03-28 23:45

RULE: Tier 0 rejection test — provisions creating emergency communication isolation incompatible with Tier 0 for DEAF. Check DEAF population before assigning Tier 0 to acoustic isolation specs.
DATE: 2026-03-28 18:25

RULE: Acoustic panel NRC is not standalone performance criterion. STI is correct criterion. STI ≥ 0.60 (general) / STI ≥ 0.75 (DEAF/CI). NRC is means, not end.
DATE: 2026-03-27 12:20

---

## Case Studies

RULE: Case study deduplication requires checking name variants, date variants, building vs programme level. Programme-level entries (CAPABLE, DFG, BATH-OUT) use programme-level format.
DATE: 2026-03-27 22:10; consolidated 2026-03-29


RULE: Part 4 holds sole specification authority for all performance targets. Anything distinctly spatial is architectural; engineers support execution. Part 8 is a coordination register mapping architect-specified targets to engineering briefs for delivery — not a parallel specification. Where Part 8 currently restates Part 4 values, replace with cross-reference. Where values contradict, Part 4 governs. Performance targets (RT60, STI, NC, STC, melanopic EDI, MERV, etc.) are architect specifications derived from population evidence; engineers design systems to achieve them.
DATE: 2026-03-30 03:42

RULE: Every Part 4 specification using "adjustable", "individual control", or "user-operated" must include a population operability note: (1) populations who can self-adjust, (2) populations requiring carer/staff operation, (3) default setting when no individual present with harm-asymmetry rationale. "Adjustable" is not a universal conflict resolution — per conflict-matrices SYNTHESIS.
DATE: 2026-03-30 03:42

RULE: Every Part 4 specification with a range (where the range reflects individual variation, not jurisdictional difference) carries a Tier 2 handoff flag: "Tier 1 default: [median]. Tier 2: OT assessment resolves position within range based on [functional parameter]." Ranges are the designed-in bridge between Tier 1 and Tier 2 — restatement of existing project-standards rule with explicit format requirement.
DATE: 2026-03-30 03:42
