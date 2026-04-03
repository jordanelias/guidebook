# Opus Synthesis Queue — Missing Passes
**Created:** 2026-04-03 04:07
**Reason:** Phase 3 writing executed by Sonnet without prior Opus adjudication of CON connections and cross-population conflict resolutions. This file defines all Opus work required before Phase 5 (QA + Assembly).

**Rule invoked:** project-standards.md — "Sonnet never determines best practice."

---

## Summary

| Session | Scope | Status |
|---|---|---|
| OP-A | Part 5 §5.2 conflict resolution table adjudication | COMPLETE 2026-04-03 04:15 |
| OP-B | CON connection synthesis adjudication (10 substantive HIGH entries) | PENDING |
| OP-C | Part 10 DAR — BPC integration pass | PENDING |
| OP-D | Part 11 Economics — BPC integration pass | PENDING |

Switch model picker to **Opus 4.6** before each session. No programmatic escalation path exists.

---

## OP-A: Part 5 §5.2 Conflict Resolution Table Adjudication

**What Sonnet did:** Wrote Part 5 §5.2 (11-entry conflict resolution table) drawing on the cross-population-conflict-resolutions BPC (which has Opus synthesis). Resolution hierarchy, RESOLVED/PARTIAL status assignments, and evidence citations were determined by Sonnet.

**What Opus must do:** Read Part 5 §5.2 in full. For each of the 11 conflict entries:
1. Verify resolution status (RESOLVED-EVIDENCE / RESOLVED-CONSENSUS / PARTIAL) is correctly assigned given the evidence tier of the governing provision.
2. Verify the governing provision is correctly identified (safety-critical vs comfort; Tier 1 vs Tier 5).
3. Verify the strategy code (SRW / SZ / TS / PP / IEC) is correctly applied.
4. Flag any resolution where Sonnet's adjudication is incorrect or a higher-ambition resolution exists in the BPC that was not applied.
5. Verify §5.3 unresolvable conflicts — confirm the three entries are genuinely irresolvable.

**Files to read:**
- parts/v10/part05.md (full)
- references/bpc/frameworks-and-methodology/cross-population-conflict-resolutions.md
- references/bpc/health-and-symptom-management/ms-thermal-temperature-conflict-resolution.md
- references/bpc/communication-and-alerts/deaf-acoustic-built-environment.md
- references/bpc/population-general/dementia-built-environment.md
- references/bpc/population-general/neurodivergent-built-environment.md

**Output:** Corrections applied directly to parts/v10/part05.md. Commit: opus-adjudication: Part 5 §5.2 conflict resolution review [YYYY-MM-DD HH:MM]

---

## OP-B: CON Connection Synthesis Adjudication

**What Sonnet did:** Applied 69 CON connections to Part 4 as population expansions and annotations. Synthesis directions were executed by Sonnet without Opus adjudication of whether the direction was correct, complete, or conflicted with other provisions.

**What Opus must do:** For each of the 10 entries below, read the full CON entry and current Part 4 implementation, then adjudicate whether the synthesis direction was correctly executed, whether specification values are correct given BPC evidence, and whether evidence tier markers are correct.

**10 entries requiring Opus adjudication:**

| CON | Synthesis direction | Items to review |
|---|---|---|
| CON-0001 | Tier 0 circulation legibility — 5 populations | D-01, D-02 |
| CON-0002 | A-16 multi-population expansion; retire separate MH room concept | A-16 description + Applicable Groups |
| CON-0004 | New item: Adjustable Posture Seating with recline | G-08 seated-task section |
| CON-0017 | H-02 elevated to Tier 0; governs B-06/F-07/F-08 | H-02 heading and Tier 0 designation |
| CON-0019 | Environmental refuge as Tier 0; one per floor plate | A-16 + G-08 |
| CON-0039 | RT60 <= 0.3 s Tier 0 for speech-critical rooms; 0.6 s = failure boundary | A-01, A-02 |
| CON-0040 | Unified sensory environment specification matrix | F-01, A-16, D-05 |
| CON-0042 | Multi-channel alerting: every alert through all three channels | B-10, K-04 |
| CON-0046 | Zone 3 + refuge mandatory (not recommended) in healthcare/education | Part 7 NR-HLT, NR-EDU |
| CON-0047 | Evidence hierarchy methodology note in Part 7 | Part 7 §7.0 universal provisions |

**Files to read:**
- references/connection-register-active.md (CON-0001, 0002, 0004, 0017, 0019, 0039, 0040, 0042, 0046, 0047)
- parts/v10/part04.md (relevant item sections)
- parts/v10/part07.md (NR-HLT, NR-EDU sections)

**Output:** Corrections applied to parts/v10/part04.md and parts/v10/part07.md where implementation was incorrect or incomplete. Commit per file changed.

---

## OP-C: Part 10 DAR — BPC Integration Pass

**What Sonnet did:** Copied v9.0 Part 11 (DAR) with section renumbering only. No BPC content integrated.

**What Opus must do:** Read three DAR BPC slugs and rewrite Part 10 integrating Opus synthesis findings.

**BPC slugs:**
- references/bpc/frameworks-and-methodology/residential-dar-provisions-priority-register.md
- references/bpc/frameworks-and-methodology/visitability-residential-accessibility-minimum-standards.md
- references/bpc/frameworks-and-methodology/residential-accessible-home-case-studies.md

**Sections to update:**
- §10.1 Cost Multiplier Table — verify against BPC evidence
- §10.2 CAN/ASC 2.8:2025 — confirm current version and provisions
- §10.3 Lifetime Homes — confirm 16 criteria current
- §10.4 Visitability — update from visitability BPC Opus synthesis (jurisdiction matrix)
- §10.6 Nordic Models — update from BPC Nordic evidence
- §10.7 Case Study Evidence — integrate residential-accessible-home-case-studies BPC

**Output:** Rewritten parts/v10/part10.md. Commit: opus-writing: Part 10 DAR BPC integration [YYYY-MM-DD HH:MM]

---

## OP-D: Part 11 Economics — BPC Integration Pass

**What Sonnet did:** Copied v9.0 Part 12 (Economics) with cross-ref updates only. No BPC content integrated.

**What Opus must do:** Read three economics BPC slugs and rewrite Part 11 integrating Opus synthesis findings.

**BPC slugs:**
- references/bpc/economics/accessible-design-economics-cost-premium.md
- references/bpc/economics/government-grant-programmes-home-adaptation.md
- references/bpc/economics/case-study-economics-financial-data.md (may still be STUB — proceed with available evidence)

**Sections to update:**
- §11.1 Cost Myth — update with current BPC evidence on cost premium
- §11.2 Core Ratio — verify new construction vs retrofit ratio
- §11.4 Cost Intelligence Tables — update from jurisdiction-specific BPC data
- §11.6 Evidence Landscape — add Oslo Economics (2018) per GAP-064; integrate BPC evidence landscape
- §11.8 Client Arguments — update with grant programme evidence

**Output:** Rewritten parts/v10/part11.md. Commit: opus-writing: Part 11 Economics BPC integration [YYYY-MM-DD HH:MM]

---

## Reduced-Confidence Flags

Until all four Opus sessions are complete, the following v10 content carries reduced confidence per project-standards.md:

| File | Sections | Reason |
|---|---|---|
| parts/v10/part05.md | §5.2, §5.3 | Resolution hierarchy adjudicated by Sonnet, not Opus |
| parts/v10/part04.md | CON-0001/0002/0004/0017/0019/0039/0040/0042/0046/0047 items | Synthesis direction executed by Sonnet without Opus review |
| parts/v10/part10.md | All sections | No BPC integration — v9.0 scaffold only |
| parts/v10/part11.md | §11.1, §11.2, §11.4, §11.6, §11.8 | No BPC integration — v9.0 scaffold only |

Flags lifted when relevant Opus session commits output and marks session COMPLETE above.

---

## Session Protocol

1. Switch model picker to **Opus 4.6**.
2. Start a new conversation. Reference this file: workplan/opus-missing-passes.md.
3. Run session start protocol (GraphQL batch read: sessions/LATEST + project-standards + workplan-orchestrator).
4. Load only the files listed under that session's "Files to read".
5. Execute. Commit. Mark the session row COMPLETE with date.
6. Switch back to Sonnet 4.6 for Phase 5.

---

## OP-E: Phase 2C Connection Scout Re-Scan

**What was missed:** Session 9 (Phase 2C) was never executed. The workplan specified: connection-scout internal re-scan after D2/D3 decisions finalised + F-category coherence check (new items F-06, F-07, F-08 did not exist during Phase 2A scan) + targeted external scan for connections missed in Phase 2A.

**Why it matters:** The 97 CON entries in connection-register-active.md are Phase 2A output only. The following were not in scope during Phase 2A and may have generated additional connections:
- F-06 Fragrance-Free Policy (whole-building) — new item
- F-07 Thermal Zoning — new item (CO-0003)
- F-08 Thermal Transition — new item (CO-0003)
- I-04 Ceiling Hoist — new item (CO-0004)
- H-05 Nurse Call — new item (CO-0004)
- Part 5 Building-Level Co-Occurrence Resolution — new Part (CO-0004)
- Merged Part 3 content (old Parts 3+4) — new structure

**What Opus must do:**
1. Run connection-scout internal pass: read all BPC slugs and identify connections not captured in CON-0001 through CON-0100, with specific attention to F-category coherence.
2. Check: does F-07 (Thermal Zoning) have connections to F-04 (Air Quality), F-06 (Fragrance-Free), and F-08 (Thermal Transition) that are not in the register?
3. Check: does I-04 (Ceiling Hoist) have connections to G-03 (Grab Bars), G-04 (Accessible Bathroom), and K-03 (Haptic Communication) that are not in the register?
4. Check: does H-05 (Nurse Call) have connections to K-04 (Vibrotactile Alert) and B-10 (Visual Fire Alarm) that are not in the register?
5. For any new connections identified: add to connection-register-active.md with CON-01XX numbering (continuing from CON-0100). Mark as Phase 2C source.
6. If new HIGH connections are identified that affect Part 4 item specifications already written: flag for SONNET-A pass (item-specification-writer protocol).

**Files to read:**
- references/connection-register-active.md (full — to avoid duplicating existing entries)
- references/bpc/index.md (slug inventory)
- All F-category BPC slugs: sensory-environment/* and health-and-symptom-management/ms-thermal*
- references/bpc/population-general/deafblind-built-environment-design.md (for I-04/K-series connections)
- workplan/v10-5_2026-03-29.md §Phase 2C for original session scope

**Output:** Updated connection-register-active.md with any new CON entries. Commit: opus-connection-scout: Phase 2C re-scan [YYYY-MM-DD HH:MM]

---

## OP-F: FDR — Functional Deficit Research for Phase 2B Slugs

**What was missed:** FDR (functional-deficit-researcher skill, Opus 4.6) was run only for PAIN/OFS (12 scenarios, COMPLETE). The workplan specified FDR for all newly COMPLETE slugs from Phase 2B Sessions 5-8. Five slugs became COMPLETE during Phase 2B without an FDR pass:
- ndv-aut-built-environment-quantified-thresholds
- intellectual-disability-built-environment-design
- ms-thermal-temperature-conflict-resolution
- ofs-built-environment
- thermal-comfort-older-adults-care-settings

**What FDR does:** Generates novel built-environment findings from clinical functional deficit evidence — identifying design implications that the standard built-environment research literature does not contain. Outputs feed Part 4 item specifications as additional evidence points.

**What Opus must do:** For each of the five slugs above, run the FDR protocol:
1. Read the full BPC slug including Opus synthesis.
2. Identify functional deficits described in the clinical evidence that have direct built-environment design implications not yet captured in the BPC.
3. For each novel finding: state the functional deficit, the architectural implication, the evidence source, and the evidence tier.
4. Append findings to the relevant BPC file under a new section: "### FDR findings (Phase 2C pass)"
5. Flag any FDR finding that conflicts with or extends a Part 4 item already written — route to SONNET-A for item-specification-writer update.

**Files to read (one slug per sub-session — 5 sub-sessions total):**
- references/bpc/population-general/ndv-aut-built-environment-quantified-thresholds.md
- references/bpc/population-general/intellectual-disability-built-environment-design.md
- references/bpc/health-and-symptom-management/ms-thermal-temperature-conflict-resolution.md
- references/bpc/health-and-symptom-management/ofs-built-environment.md
- references/bpc/health-and-symptom-management/thermal-comfort-older-adults-care-settings.md

**Output:** Each BPC file updated with FDR findings section. Commit per file: opus-fdr: [slug] Phase 2C [YYYY-MM-DD HH:MM]. Flag any Part 4 items requiring update for SONNET-A.

---

## OP-G: Part 3 §3.8 and §3.9 — Novel Methodology Review

**What was missed:** Part 3 §3.8 (Resolution Decision Tree) and §3.9 (Resolution Strategies Menu) are flagged as GAP-P8-01 and GAP-P8-02 in the workplan: "original practitioner methodology — guidebook contribution" with no peer-reviewed taxonomy. These were written by Sonnet directly from CO-0004 content descriptions without Opus synthesis or review.

**Why it matters:** §3.8 and §3.9 are the methodological core of the guidebook's co-occurrence framework — the content the guidebook is contributing to the field. If the decision tree logic or the strategy taxonomy is incorrect, incomplete, or contradicted by existing frameworks, the entire Part 3 methodology is compromised.

**What Opus must do:**
1. Read Part 3 §3.8 and §3.9 in full.
2. Check §3.8 decision tree against: (a) the cross-population-conflict-resolutions BPC resolution hierarchy; (b) the 11 resolved conflicts in Part 5 §5.2 — does applying §3.8 to each conflict produce the same resolution as Part 5? If not, one of them is wrong.
3. Check §3.9 strategy menu (IEC/SZ/TS/DAR/SRW/PP/T0/OT-REF): are these the correct and complete set of strategies given the evidence base? Is the ordering correct (which strategy should be attempted first)?
4. Check §3.7 decision framework against §3.8 — are they internally consistent? §3.7 has 6 steps; §3.8 is a tree version of the same logic. Any divergence is an error.
5. Check §3.11 worked examples — does applying §3.8 to each worked example produce the design decisions stated? If not, either the example or the tree is wrong.
6. Check Part 5 §5.4 worked examples — same consistency check against §3.8/3.9.

**Files to read:**
- parts/v10/part03.md §3.7, §3.8, §3.9, §3.11 (full text)
- parts/v10/part05.md §5.2, §5.3, §5.4 (full text)
- references/bpc/frameworks-and-methodology/cross-population-conflict-resolutions.md

**Output:** Corrections applied to parts/v10/part03.md where decision tree logic, strategy menu, or worked examples are inconsistent. Commit: opus-adjudication: Part 3 §3.8-3.9 methodology review [YYYY-MM-DD HH:MM]

---

## OP-H: Part 12 Case Studies — BPC Integration

**What was missed:** Part 12 is the v9.0 scaffold only (14 case studies from v9.0). The following were not integrated:
- references/case-study-compendium.md (skeleton created Phase 2A, Session 4)
- references/bpc/frameworks-and-methodology/cross-population-case-studies.md (ACTIVE slug with Opus synthesis)
- references/bpc/frameworks-and-methodology/accessible-design-failures-poor-performance.md (STUB — Phase 2B Session 8; may still be stub)

**What Opus must do:**
1. Read cross-population-case-studies BPC — identify any case studies not in current Part 12 that should be added.
2. Read case-study-compendium.md — identify any entries not yet in Part 12.
3. If accessible-design-failures-poor-performance is no longer a stub: integrate failure cases into Part 12 (the workplan specifies failure evidence for §12 methodology note and §5.5 unresolvable conflicts).
4. Review the 14 existing case studies in Part 12 — verify §12.3 subsection ordering fix (GAP-CR-10/D3-19): confirm case study sequence reflects evidence quality, not chronological order.
5. Assess whether any existing case studies require updating given cross-population evidence (e.g. De Hogeweyk is DEM-primary — does the cross-population BPC add anything?).

**Files to read:**
- parts/v10/part12.md (full)
- references/case-study-compendium.md
- references/bpc/frameworks-and-methodology/cross-population-case-studies.md
- references/bpc/frameworks-and-methodology/accessible-design-failures-poor-performance.md

**Output:** Updated parts/v10/part12.md with new/revised case studies. Commit: opus-writing: Part 12 case studies BPC integration [YYYY-MM-DD HH:MM]

---

## SONNET-A: New Items — item-specification-writer Protocol Pass

**What was missed:** New items written this phase (F-07, F-08, I-04, G-08 seated-task additions, E-15) were written inline without the item-specification-writer protocol. Required passes not run:
- REF-ID markers not assigned (bibliography-compiler cannot process these items)
- sources-cited tables not created per item
- vol2-item-formatter validation not run
- framing-checker pass not run
- evidence-auditor pass not run

**Dependency:** Run AFTER OP-B (CON adjudication may change specification content) and AFTER OP-E/OP-F (new FDR findings may affect item specs).

**Scope:** Apply item-specification-writer protocol to:
- F-07 Thermal Zoning
- F-08 Thermal Transition
- I-04 Ceiling Hoist
- G-08 seated-task additions (new content only — not the wardrobe spec from working/item-specs-final which already has REF-IDs)
- E-15 Changing Places Facility (was written in 88_to_90 — needs protocol pass on v10 version)
- H-05 Nurse Call (CO-0004 new item — check whether it has a full spec in part04.md or only a placeholder)
- Any additional items flagged by OP-E or OP-F

**Protocol per item:**
1. Read relevant BPC slug(s) for evidence basis.
2. Write or revise specification with REF-ID markers in body text.
3. Write sources-cited table (REF-ID | Authors | Year | Title | Journal/Publisher | Tier | Lang | Jurisdiction).
4. Run framing-checker on item text.
5. Run evidence-auditor on evidence tier markers.
6. Run vol2-item-formatter validation (REF-ID integrity).

**Output:** Updated parts/v10/part04.md with protocol-compliant items. Commit: item-specification-writer: [item code] protocol pass [YYYY-MM-DD HH:MM]

---

## SONNET-B: Part 2 Co-1 Evidence Gap Markers

**What was missed:** Part 2 was rewritten from BPC Opus synthesis outputs. BPC files note Co-1 passes were PARTIAL for most populations — lived experience and participatory design sources not fully retrieved. Part 2 makes claims in several population sections that rest on Tier 3-5 evidence where Co-1 evidence exists but was not retrieved.

**Dependency:** Can run independently; does not require Opus sessions first.

**What Sonnet must do:**
1. Read Part 2 in full.
2. For each population section, identify claims where the BPC notes Co-1 as NOT RETRIEVED or PARTIAL.
3. Add inline marker after each such claim: [Co-1 NOT RETRIEVED — lived experience evidence for this provision not confirmed; see BPC {slug} for retrieval status]
4. This does not change the specification — it flags the evidence gap for future Co-1 research.

**Populations with confirmed Co-1 gaps (from BPC files):**
- MOB: KR Co-1 not retrieved; BR Co-1 not retrieved
- VIS: Co-1 pass PARTIAL — RNIB HQ user trials confirmed; others not retrieved
- NEU: Co-1 pass not run for non-EN languages
- DEM: Co-1 extended pass not run for 9 languages
- NDV: Co-1 PARTIAL — ZH/NL/FI/IT no data
- PAIN: Co-1 7/14 languages not attempted
- DBL: Co-1 PARTIAL — Protactile community only
- OFS: Co-1 structural gap — no design-specific Co-1 in any jurisdiction
- IntD: Co-1 attempted 14 languages; all thin or no data

**Output:** Updated parts/v10/part02.md with Co-1 gap markers. Commit: sonnet-audit: Part 2 Co-1 evidence gap markers [YYYY-MM-DD HH:MM]

---

## Updated Summary Table

| Session | Scope | Model | Status |
|---|---|---|---|
| OP-A | Part 5 §5.2 conflict resolution adjudication | Opus | PENDING |
| OP-B | CON connection synthesis adjudication (10 HIGH entries) | Opus | PENDING |
| OP-C | Part 10 DAR — BPC integration | Opus | PENDING |
| OP-D | Part 11 Economics — BPC integration | Opus | PENDING |
| OP-E | Phase 2C connection-scout re-scan | Opus | COMPLETE 2026-04-03 05:27 |
| OP-F | FDR for 5 Phase 2B slugs | Opus | COMPLETE 2026-04-03 05:27 |
| OP-G | Part 3 §3.8/3.9 methodology review | Opus | PENDING |
| OP-H | Part 12 case studies — BPC integration | Opus | PENDING |
| SONNET-A | New items — item-specification-writer protocol pass | Sonnet | PENDING (after OP-B, OP-E, OP-F) |
| SONNET-B | Part 2 Co-1 evidence gap markers | Sonnet | PENDING |

**Recommended execution order:**
1. OP-E (connection scout) — may generate new CON entries affecting all subsequent work
2. OP-F (FDR) — may generate new item spec requirements for SONNET-A
3. OP-G (Part 3 methodology) — independent; can run in parallel with OP-E/F
4. OP-A, OP-B (adjudication passes) — after OP-E to include any new connections
5. OP-C, OP-D, OP-H (BPC integration writing) — independent of each other; can run in parallel
6. SONNET-A (item-specification-writer) — after OP-B, OP-E, OP-F
7. SONNET-B (Part 2 Co-1 markers) — independent; run anytime
8. Phase 5 (cross-reference-resolver + assembly) — after all above
