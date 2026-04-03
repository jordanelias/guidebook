# Opus Synthesis Queue — Missing Passes
**Created:** 2026-04-03 04:07
**Reason:** Phase 3 writing executed by Sonnet without prior Opus adjudication of CON connections and cross-population conflict resolutions. This file defines all Opus work required before Phase 5 (QA + Assembly).

**Rule invoked:** project-standards.md — "Sonnet never determines best practice."

---

## Summary

| Session | Scope | Status |
|---|---|---|
| OP-A | Part 5 §5.2 conflict resolution table adjudication | PENDING |
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
