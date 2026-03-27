# Workplan: Guidebook v10.2 — Integrated Revision

**Created:** 2026-03-26 17:00
**Supersedes:** Workplan_v10-1_Redesigned_2026-03-24-1.md
**Basis:** v10-1 Workplan + State Review 2026-03-26 (11 sessions completed since v10-1; systematic gap register, GitHub, and ecosystem audit)
**Principle:** Content determines structure. Audit before research. Research before writing. Structure once, at the end.

---

## What Changed From v10.1

| Area | v10.1 plan | v10.2 plan | Rationale |
|---|---|---|---|
| Phase 0 | 2 sessions (build 6 skills, update 10) | **1 session** — reconciliation + cleanup only. 6 skills already built. Remaining: verify 10 updates, reconcile inventories, migrate BPC/SL storage. | 11 sessions of work completed Phase 0 builds. Remaining is infrastructure cleanup, not builds. |
| Slug storage | Dual architecture: 14 flat files + 2 directory-structure slugs | **Single canonical architecture:** per-slug directory structure. Flat files migrated, then frozen. | Dual structure creates CHECK/LOG path ambiguity and reconciliation debt. One architecture. |
| `connection-scout` | Mentioned at edition boundary only | **Integrated at three points:** (1) pre-Phase 2B scan of completed BPC corpus; (2) post-Phase 2B re-scan after new research; (3) post-Phase 3 edition boundary. External mode runs twice. Skill file to be built. | 32 connections already discovered; methodology proven. Must be systematically scheduled, not ad hoc. |
| `functional-deficit-researcher` | Not in session plan | **Integrated:** runs after each `multilingual-research` COMPLETE slug with ≥2 THIN flags or thin-base population. 12 scenarios already completed for PAIN/OFS; remaining slugs scheduled. | Methodology validated: 18 NOVEL findings, 4 Tier 0 candidates from PAIN/OFS run alone. |
| Out-of-sequence research | Not acknowledged | **Acknowledged and credited.** Bathroom (COMPLETE), kitchen (PROVISIONAL), threshold-door-hardware (PARTIAL), PAIN/OFS FDR (COMPLETE), 8 targeted gap resolutions, 32 connections — all credited. Phase 2B scope reduced accordingly. | ~6 sessions of research already done. Workplan must reflect actual state, not re-plan completed work. |
| Phase 1 | 3 sessions (D1/D2/D3) | **2 sessions** (D2/D3 combined — D1 already done). | P1-D1 complete with 34 decisions recorded. Only D2 and D3 remain. |
| Gap register triage | Phase 2A Session 6 | **Moved to Phase 0** reconciliation session — 127 OPEN items need triage against Decision Register before research planning. | Triage is infrastructure, not content. Must happen before Phase 1 resumes. |
| Skill sync | Assumed `/mnt/project/` = GitHub | **Explicit sync step:** 3 skills on GitHub missing from `/mnt/project/`; `keyword-lookup` disposition required; `connection-scout` skill file to be built. | Runtime reads from `/mnt/project/`; GitHub-only skills cannot be read at execution time. |
| Working document persistence | Discovered mid-session 2026-03-26 | **Enforced:** rule in project-standards. session-consolidator verifies no uncommitted working docs before close. | Data loss risk existed prior to rule. |
| Total sessions | 24 | **22** (net -2: Phase 0 compressed 2→1; Phase 1 compressed 3→2; Phase 2A absorbed into Phase 0; Phase 2B reduced by credited research) |

---

## Current State Summary (as of 2026-03-26 17:00)

### Completed Since v10.1

| Item | Status | Session(s) |
|---|---|---|
| **Phase 0 skill builds** (6/6) | github-io, file-splitter, evidence-marker, bulk-renumber, citation-miner, sensory-coherence-checker — all on GitHub | 2026-03-25, earlier |
| **P1-D1 Decision Register** | 34 decisions (D1-01 through D1-34). Vol I + Vol II front matter + Part 8 scope. | 2026-03-25 |
| **CO-0002** (IntD elimination) | Issued. Execution pending (GAP-CO02-01). | 2026-03-25 |
| **Bathroom slug** (accessible-bathroom-and-grab-bar) | 24/24 jurisdictions COMPLETE. BPC logged. | 2026-03-26 |
| **Kitchen slug** (residential-kitchen-and-task-surfaces) | 19/24 jurisdictions PROVISIONAL (accepted gaps). BPC logged. | 2026-03-26 |
| **Threshold slug** (threshold-door-hardware) | PARTIAL — 24/24 Tier 6, 12 SEARCHED + 13 THIN, Co-1 0/24, citation mining 0. | 2026-03-26–27 |
| **PAIN/OFS slug** (pain-ofs-built-environment-design) | PARTIAL — 10/24 jurisdictions (accepted gaps). FDR COMPLETE (12/12 scenarios, 18 NOVEL, 4 Tier 0 candidates). | 2026-03-26 |
| **8 targeted gap resolutions** | B-10 seizure, DEAF RT60, sensory room, circadian lighting, Rajotte, NCSE, Guay biomechanics, NC-25 equivalence — all RESOLVED. | 2026-03-26 |
| **Connection discovery** | 32 connections (CON-0001–0032). 20 internal, 12 external. 19 HIGH, 9 MODERATE, 4 SPECULATIVE. | 2026-03-26 |
| **functional-deficit-researcher** | Built, validated, PAIN/OFS run COMPLETE. | 2026-03-26 |
| **89 project-standards rules** | Accumulated across 44 sessions. | Ongoing |

### Not Yet Done

| Item | Workplan ref | Blocking? |
|---|---|---|
| P1-D2 (Parts 4–7, item consolidation gate) | Phase 1 Session 4 | **YES — critical path** |
| P1-D3 (Parts 8–13, Appendices) | Phase 1 Session 5 | **YES — gates Phase 2B scope** |
| Pre-v4 slug triage (51 slugs) | Phase 2A | No — but gates Phase 2B efficiency |
| BPC/SL storage migration | Infrastructure | No — but creates operational risk |
| Skill inventory reconciliation | Phase 0 | No — but 3 skills unreadable at runtime |
| Gap register triage against Decision Register | Phase 2A | No — but 127 OPEN items is unwieldy |
| `connection-scout` skill file | Phase 0 | No — runs from PI definition, but should have standalone file for registry |
| `github-io` adoption across skills | Phase 0 | No — current inline approach works but wastes tokens |

---

## Structural Architecture

Unchanged from v10.1. Confirmed:

| Part | Title | Volume |
|---|---|---|
| 1 | Foundations of Accessible Design | I |
| 2 | Disability Categories | I |
| 3 | Designing for Multiple Disability Categories | I |
| 4 | Synthesis and Sequencing | II |
| 5 | Residential Application Matrices | II |
| 6 | Non-Residential Application Matrices | II |
| 7 | Item Specification Library | II |
| 8 | Cross-Population Resolution & Cross-Disciplinary Collaboration | II (NEW) |
| 9 | Engineering and Coordination | II |
| 10 | Interdisciplinary Design Team | II (reconceived) |
| 11 | Design for Adaptable Readiness — DAR | III |
| 12 | The Economics of Accessible Construction | III (intensified) |
| 13 | Case Studies and Built Evidence | III (expanded) |
| Apps | Appendices A–E, Bibliography, Glossary | III |
| Supp | Supplementary Volume: Body Sizes | — |

---

## Sequencing Logic

```
Phase 0R  Reconciliation           Clean up ecosystem, migrate storage, triage gaps (1 session)
Phase 1   Editorial Decisions      Complete Decision Register — D2 + D3 (2 sessions)
Phase 2A  Triage & Mining          Pre-v4 slug triage + case study evidence mining (1 session)
Phase 2B  Research                 Only what survived Phase 1 + new content — reduced by credited work (4 sessions)
Phase 2C  Connection + Bottom-Up   connection-scout re-scan + FDR for new COMPLETE slugs (1 session)
Phase 3   Writing                  Consolidate, edit, mark evidence, create new content (9 sessions)
Phase 4   Structure                Renumber, decompose, resolve cross-refs — once (2 sessions)
Phase 5   QA + Assembly            Audit, assemble, final verification (2 sessions)
```

**Why this order:**
- Phase 0R before everything: ecosystem must be clean before any skill operates at scale.
- Phase 1 before Phase 2: no point researching evidence for content that gets cut.
- Phase 2A before 2B: triage determines which slugs need research vs. backfill.
- Phase 2B before 2C: `connection-scout` and `functional-deficit-researcher` operate on assembled BPC outputs — they need the BPC corpus to be substantially complete.
- Phase 2C before Phase 3: connection findings and FDR findings feed `item-specification-writer`.
- Phase 3 before Phase 4: consolidations and deletions change heading counts; renumber after content is final.
- Phase 4 before Phase 5: cross-references can only be verified after numbering is stable.

---

## Phase 0R: Reconciliation (Session 1)

This session produces no content. It makes the ecosystem trustworthy for all subsequent sessions.

### 0R-1: Slug Storage Migration (~40% of session)

**Problem:** 62 slugs exist across 14 flat population files. 2 slugs use the per-slug directory structure. The slug registry lists only 2 entries. `research-log-manager` CHECK/LOG/RETRIEVE cannot resolve paths for 60 slugs.

**Fix:**
1. GET all 14 flat BPC files. For each `## {slug}` heading, extract slug content.
2. Assign each slug to a topic directory per the Topic Directory Index in the slug registry.
3. Create `references/bpc/{topic}/{slug}.md` and `references/search-log/{topic}/{slug}.md` for each slug.
4. Update `references/slug-registry.md` with all 62 rows.
5. Verify: `research-log-manager CHECK` on 5 randomly selected slugs — all must resolve.
6. Add `_archived/` prefix note to flat files — do not delete (frozen archive).

**Topic directory assignments** (extend the existing index):

| Directory | Slugs (anticipated) |
|---|---|
| `entrances-and-circulation` | threshold-door-hardware, door-width-clearance, corridor-width, ramp-gradient, step-nosing, staircase-design, lift-and-elevator, entrance-approach, parking-and-drop-off |
| `bathrooms-and-wet-areas` | accessible-bathroom-and-grab-bar, shower-bathing-geometry, grab-bar-configuration, toilet-transfer-clearance, basin-and-vanity |
| `kitchens-and-workspaces` | residential-kitchen-and-task-surfaces, sink-clearance, workspace-ergonomics, counter-height |
| `health-and-symptom-management` | pain-ofs-built-environment-design, retreat-reset-room, thermal-regulation |
| `wayfinding-and-signage` | luminance-contrast-and-pattern, tactile-indicators, signage-and-pictogram, visual-alerting-and-wayfinding-light |
| `seating-and-rest` | seating-interval, rest-points, recline-seating |
| `sensory-environment` | therapeutic-lighting-design, acoustic-environment, sensory-room-design, olfactory-environment |
| `communication-and-alerts` | hearing-loop-and-assistive-listening, visual-and-vibrotactile-alarm, intercom-and-communication |
| `controls-and-hardware` | reach-range-and-accessible-controls, door-hardware-and-ironmongery, window-operation |
| `furniture-and-fittings` | bed-and-bedroom-furniture, seating-specification, storage-and-shelving |
| `outdoor-and-landscape` | outdoor-accessible-design, playground-and-recreation |
| `population-general` | deafblind-built-environment-design, mobility-built-environment, dementia-built-environment, visual-impairment-built-environment, deaf-built-environment, neurodivergent-built-environment, mental-health-built-environment, neurological-built-environment, intellectual-disability-built-environment-design |
| `frameworks-and-methodology` | ot-built-environment-collaboration, cross-population-conflict-resolution, dar-design-adaptable-readiness, universal-design-methodology |
| `room-types` | residential-home-modification, healthcare-facility-design, education-facility-design, workplace-design, retail-and-commercial, hospitality-design, transport-and-interchange, cultural-and-assembly |

Exact slug-to-directory assignments will be confirmed during migration by reading each flat file's content.

### 0R-2: Skill Inventory Reconciliation (~20% of session)

**Actions:**
1. `connection-scout`: Build SKILL.md file from PI §connection-scout definition. Write to `/mnt/project/` and `skills/` on GitHub.
2. `keyword-lookup`: Classify. If functionality is subsumed by `multilingual-research` native-alias lookup → retire. Add to `skills/deprecated/` on GitHub.
3. `research-log-manager`: Confirm PI inline definition is canonical. Remove stale `/mnt/project/research-log-manager_SKILL.md` (or replace with pointer to PI). No GitHub `skills/` file needed per design.
4. Verify `/mnt/project/` has current copies of: `bulk-renumber`, `citation-miner`, `sensory-coherence-checker`. If not → copy from GitHub `skills/` to working directory for runtime access. **Note:** `/mnt/project/` is read-only in this environment. For sessions requiring these skills, the skill must be read from GitHub via `github-io` GET or the PI definition must be consulted. Add a note to `project-standards.md`: "Skills not in `/mnt/project/` must be read from GitHub `skills/{name}_SKILL.md` via GET before execution."
5. Confirm all 10 skill updates from v10.1 Phase 0 are reflected in actual skill files. Spot-check: `framing-checker` (BAR-in-Vol-I check?), `evidence-auditor` (●/○ verification mode?), `cross-reference-resolver` (BPC↔Item traceability?). If any update is missing → apply.

**Gate:** Slug registry has all 62 rows. `research-log-manager CHECK` resolves 5/5 test slugs. `connection-scout` SKILL.md exists. `keyword-lookup` disposed of. Skill update spot-check passes.

### 0R-3: Gap Register Triage (~25% of session)

**Problem:** 127 OPEN items. Many may target content eliminated by the Decision Register or by CO-0002. Triage before Phase 1 resumes.

**Process:**
1. GET `gap_register.md`.
2. GET Decision Register (`workplan/v10-1-decision-register.md`).
3. For each OPEN gap:
   - Content eliminated by Decision Register or CO-0002 → CLOSED-ELIMINATED.
   - Content merged → reassign to new location.
   - Content surviving → remains OPEN.
   - RESOLVED items → verify specification language exists; if execution-ready, tag `EXEC-READY` for Phase 3 pickup.
4. Add GAP-CO2-01 resolution: Co-2 tier unpopulated (per audit §4.1) → P1 gap for Session 7 research.
5. PUT updated `gap_register.md`.

**Expected outcome:** 127 OPEN → ~70–85 OPEN (some eliminated by CO-0002 IntD removal; some merged). ~37 RESOLVED items tagged for Phase 3 execution.

### 0R-4: `github-io` Adoption Verification (~15% of session)

1. Confirm `github-io` skill works: test GET + PUT cycle on a non-critical file.
2. Check whether `session-consolidator` and `research-log-manager` are calling `github-io` or still using inline bash. If inline → note as P3 technical debt (not blocking; token waste only).
3. Verify `session-consolidator` checks for uncommitted working documents per the 2026-03-26 21:00 rule.

**Phase 0R gate:** All slug paths resolve. Gap register triaged. Skills reconciled. `github-io` verified. No infrastructure debt remains that would compromise Phase 1 or Phase 2 execution.

---

## Phase 1: Editorial Decisions (Sessions 2–3)

### P1-D2: Parts 4–7 (Session 2)

**Pre-existing:** P1-D1 complete (34 decisions, D1-01 through D1-34).

**Part 4 — Synthesis and Sequencing:**
- §4.1–§4.8: Apply per-subsection keep/merge/condense decisions per v10.1 plan.
- §4.9 (cross-population guidance): Becomes brief cross-reference pointer to Part 8 (not substantive).
- DEC-11: Worked examples — keep 5 or reduce to 3?

**Part 5 — Residential Matrices:**
- §5.0a: CUT (absorb into §5.0).
- Per-room: DEC-07 — sub-table structure (keep 6 or condense to 3?).
- Remove BAR columns from all matrices.
- Resolve phantom items per decision.

**Part 6 — Non-Residential Matrices:**
- §6.0: CUT.
- Same structural questions as Part 5.

**Part 7 — Item Specification Library:**
- Item consolidation decisions (DEC-01): approve/reject each merger candidate.
- Per-item scope filter: architectural specification or non-design content?
- I-04/I-05/I-06 (DEC-03): create as full Part 7 items, merge, or delete?
- H-05 (DEC-04): create or redirect?
- BIO/TC (DEC-06): promote to Part 7 or keep in appendix?
- F-02 Fragrance-Free (DEC-12): keep or cut?
- A-17 Upholstered Seating (DEC-13): keep or cut?

**Part 7 connection-register integration:** Review all 19 HIGH-confidence connections (CON-0001–0032). For each: does it imply a new item, a merged item, or a cross-reference addition? Feed into DEC-01 merger decisions.

**Output:** Decision Register entries for Parts 4–7.
**Checkpoint:** Author reviews and approves item consolidation list. **This is the most critical gate.**

### P1-D3: Parts 8–13 + Appendices + Supplementary (Session 3)

Per v10.1 plan — unchanged. Resolves DEC-08 through DEC-20.

**Additional input for Part 8 scope:** CON-0001 through CON-0032 findings. Connection register entries rated HIGH that identify cross-population conflicts feed directly into §8.4 content inventory. Expected: 5–8 connections supplement the existing 12 §3.4 entries, bringing §8.4 toward the 20–25 entry target.

**Additional input for Part 12 economics:** CON-0031 (environmental gerontology cost-effectiveness), CON-0032 (Clemson 2023 Cochrane fall reduction cost ratio 1:2.2–1:14.9). These strengthen the economics evidence base beyond what v10.1 anticipated.

**Output:** Complete Decision Register on GitHub. All DEC-01 through DEC-20 resolved.
**Phase 1 gate:** Decision Register approved by author. No Phase 2 work begins until approved.

---

## Phase 2A: Triage & Evidence Mining (Session 4)

### Operation 1: Pre-v4 Slug Triage (~60% of session)

Process all 51 pre-v4 slug entries. Now that slug storage migration is complete (Phase 0R), each slug has its own file and can be individually assessed.

For each pre-v4 slug:
1. GET `references/search-log/{topic}/{slug}.md`.
2. Classify:
   - Content eliminated by Decision Register → CLOSE-ELIMINATED.
   - Existing search data covers ≥18 jurisdictions, Co-1 found incidentally → CONSUME (backfill metadata only).
   - Partial coverage, missing key jurisdictions → SUPPLEMENT (targeted pass).
   - Clearly inadequate → RE-RUN.
3. Merge any duplicate slug entries identified in audit (4 confirmed).
4. Fix pipe-suffix naming inconsistencies.
5. PUT updated files.

**Output:** Triage register — every slug classified.

### Operation 2: Case Study Evidence Mining (~25% of session)

Per v10.1 plan — unchanged. Process all 14 existing case studies. Extract quantified outcome data. Map to Part 7 items. Assess evidence tier. Produce case study evidence map.

**Output:** `workplan/case-study-evidence-map.md` on GitHub.

### Operation 3: Gap Register Post-Decision Triage (~15% of session)

With Decision Register now complete (post-Phase 1):
1. Second pass on gap register — any items newly eliminable by D2/D3 decisions.
2. Tag all EXEC-READY items with their Phase 3 session assignment.

**Output:** Updated `gap_register.md`. Expected: ~70 OPEN → ~50–60 OPEN.

---

## Phase 2B: Research (Sessions 5–8)

### Scope Reduction From Credited Work

| Planned in v10.1 | Status | v10.2 action |
|---|---|---|
| Session 7: Co-2 + CRPD + CONSUME backfill | CONSUME backfill absorbed into Phase 0R slug migration. Co-2 and CRPD text still needed. | **Session 5** — combined with remaining slug backfill |
| Session 8: PAIN + OFS + IntD lit review | PAIN/OFS slug PARTIAL + FDR COMPLETE. IntD = condensed proxy (DEC-05). | **Absorbed** — PAIN/OFS research substantially done; IntD is proxy only |
| Session 9: NDV/MH + NEU + residential + SUPPLEMENT | Unchanged. | **Session 6** |
| Session 10: Cross-population + economics | CON-0001–0032 partially satisfy cross-population evidence. Economics unchanged. | **Session 7** — reduced scope on cross-population; economics intensified |
| Session 11: Case studies + remaining slugs | Unchanged. | **Session 8** |

### Session 5: Foundations + Slug Backfill + Threshold Completion

**Co-2 Sources:**
- Retrieve CPGs from: CAOT, AOTA, RCOT (incl. Housing Adaptations Without Delay 2019), COTEC, WFOT.
- Classify, extract, log in BPC.

**CRPD Text:**
- Retrieve Articles 3, 4.3, 9 full text for §1.7 expansion.

**Slug backfill — CONSUME batch:**
- Process CONSUME-classified slugs from Phase 2A triage: add `jurisdiction_coverage`, `native_aliases`, `best_practice_synthesis`.
- All written to per-slug directory structure files.

**Threshold-door-hardware completion:**
- Co-1/DPO pass for priority jurisdictions (DREDF, Scope, PVA, AFB, DPI Japan, CDPF, EDF).
- Citation mining on 18 confirmed sources.
- Web verification of 13 THIN jurisdiction values.
- Pre-LOG completeness check → target COMPLETE or accepted PARTIAL.

**Output:** Co-2 sources, CRPD articles, backfilled slugs, threshold slug upgraded.

### Session 6: Population Research — NDV/MH + NEU + Residential + SUPPLEMENT Batch

**Slug: `mental-health-built-environment`** (P1 priority)
- Targeted pass: Co-1 from mental health advocacy organisations; therapeutic design evidence.

**Slug: `neurological-built-environment`** (P1 supplement)
- Close specific gaps (NEU/PCS provisions relying solely on PAS 6463).

**Slug: `residential-home-modification`** (P1 priority)
- OT home modification outcome studies; aging-in-place evidence by jurisdiction.

**SUPPLEMENT batch:**
- Process 5–8 SUPPLEMENT slugs from Phase 2A triage.

**Output:** Updated BPC entries; SUPPLEMENT slugs upgraded.

### Session 7: Cross-Population Evidence + Economics Deep-Dive

**Cross-population conflict resolution slug:**
- Review existing CON-0001–0032 findings. Identify evidence gaps not yet covered.
- Targeted search for: sensory environment conflict POE data; multi-disciplinary design team effectiveness evidence; thermal conflict resolution evidence (Uhthoff's vs PAIN warmth).
- Reduced scope: internal connection discovery already provides substantial evidence base for Part 8 §8.4.

**Economics intensification research:**
- Cost study data by building type (residential, office, healthcare).
- Pro forma/development cost data: US (RSMeans), UK (BCIS), DE (TERRAGON), AU (QS databases).
- Insurance/liability reduction evidence.
- Grant programme inventory: 8 priority jurisdictions (scope per DEC-18).
- ROI calculation methodologies — incorporate CON-0031/0032 findings (Clemson 2023 Cochrane, environmental gerontology cost data).

**Output:** Cross-population BPC entry. Economics research compilation.

### Session 8: Case Study Sourcing + Remaining Slugs

**New case studies — targeted search:**
- PAIN/OFS: built environment adaptations with outcome data (target: 2–3).
- IntD: purpose-built or adapted environments (target: 1–2).
- NDV/MH: therapeutic or trauma-informed design with outcomes (target: 1–2).
- Residential mixed-needs: home modification programmes with longitudinal data (target: 2–3).
- Cross-disciplinary collaboration: projects documenting multi-specialist process (target: 1–2).

**Remaining SUPPLEMENT/RE-RUN slugs:**
- Complete any slugs not finished in Sessions 5–6.
- If >5 need full runs, defer lowest-priority to PROVISIONAL.

**Output:** Case study compendium. All slug coverage complete or explicitly PROVISIONAL.

**Phase 2B gate:** All surviving OPEN gaps either researched or explicitly accepted as ○-marked. All slug entries meet minimum v4 schema in per-slug directory files. Case study evidence map complete. Economics research compiled. Decision Register updated with any scope changes.

---

## Phase 2C: Connection Discovery + Bottom-Up Research (Session 9)

This phase is new in v10.2. It runs after Phase 2B because both `connection-scout` and `functional-deficit-researcher` operate on assembled BPC outputs — they need the corpus to be substantially complete.

### 2C-1: `connection-scout` Internal Re-Scan (~40% of session)

**Why re-scan:** Phases 2A–2B added new BPC content (SUPPLEMENT/RE-RUN slug upgrades, economics data, case study evidence, threshold completion). The original internal scan (CON-0001–0020) operated on the pre-Phase-2B corpus. New connections may exist.

**Process:**
1. GET all BPC entries via slug registry.
2. GET connection register (CON-0001–0032).
3. Run `connection-scout` internal mode — skip population pairs already covered in CON-0001–0020. Focus on: newly completed slugs, economics evidence, case study outcomes, FDR Tier 0 candidates.
4. Expected: 5–10 new connections (diminishing returns from broad scan; targeted by new content).

### 2C-2: `connection-scout` External Targeted Scan (~20% of session)

**Scope:** Not a broad field sweep (already done in CON-0021–0032). Targeted at specific evidence gaps identified during Phase 2B:
- POE methodology for accessible design (per CON-0031 — only 2 validated tools exist).
- Trauma-informed design spatial evidence (per CON-0024 — convergence opportunity).
- Any gap register items marked REVIEW or KNOWN-LIMITATION that external literature might resolve.

**Expected:** 3–5 new connections.

### 2C-3: `functional-deficit-researcher` for Newly COMPLETE Slugs (~40% of session)

**Trigger:** Any slug that reached COMPLETE in Phase 2B with ≥2 THIN flags or thin-base populations.

**Candidate slugs:**
- `mental-health-built-environment` (if COMPLETE after Session 6)
- `neurological-built-environment` (if COMPLETE after Session 6)
- `cross-population-conflict-resolution` (if COMPLETE after Session 7)
- Any SUPPLEMENT slug that revealed thin evidence during backfill.

**Process per slug:**
1. Select ≤12 functional scenarios (ICF-d codes × functional constraint → environment context).
2. Run FDR search sequence (OT intervention DBs → practice guidelines → AT databases → cross-language check).
3. Categorize: CONFIRMS, REFINES, NOVEL, CONTRADICTS, NEW.
4. Flag ≥3-code convergences as TIER-0-CANDIDATE.
5. Update BPC `### Bottom-up findings` and search-log `functional_deficit_pass` block.

**Cap:** ≤24 scenarios total in this session (2 slugs × 12 scenarios, or 3 slugs × 8 scenarios).

**Output:** Updated connection register. Updated BPC entries with FDR findings. Gap register updated with Tier 0 candidates and SPECULATIVE connections.

**Phase 2C gate:** Connection register current (all Phase 2B content scanned). FDR complete for all COMPLETE slugs with thin evidence. HIGH-confidence connections briefed into item-specification-writer input queue.

---

## Phase 3: Writing (Sessions 10–18)

Content revision within the *current* structure (old numbering). Phase 4 renumbers. Phase 3 applies: consolidation, deletion, concision, evidence markers, new content creation.

All 37+ EXEC-READY gap resolutions are consumed during Phase 3 writing — assigned to their relevant session below.

### P3-W01: Front Matter + Part 1 (Session 10)

Per v10.1 plan. Additional inputs:
- Co-2 sources from Session 5.
- CRPD article text from Session 5.
- CON-0027 (environmental gerontology — Lawton docility-proactivity continuum) for theoretical framing in §1.4.
- EXEC-READY gaps: GAP-CR-05 (ToC mismatch), GAP-CR-08 (DD terminology), GAP-CR-09 (RFO terminology).

**Checkpoint:** Part 1 content-final.

### P3-W02: Part 2 — Disability Categories (Session 11)

Per v10.1 plan. Additional inputs:
- FDR findings for population-specific categories.
- Connection register findings identifying cross-population provisions.
- CO-0002 execution: delete IntD standalone section; replace with condensed ○-marked proxy paragraph under DEM/NDV with [TIER 4-5] tag.
- EXEC-READY gaps: GAP-DBL-BE-01 (THIN-BASE disclosure on all DBL items), GAP-DBL-BE-02 (Protactile/co-presence paragraph).

**Checkpoint:** Part 2 content-final.

### P3-W03: Parts 3 + 4 (Session 12)

Per v10.1 plan. Additional input:
- GAP-CR-14 (Co-2 tier populated from Session 5 research).
- GAP-CR-16 (sensory coherence practitioner tool — from connection register CON-0002).

**Checkpoint:** Parts 3 + 4 content-final.

### P3-W04: Part 5 — Residential Matrices (Session 13)

Per v10.1 plan. Additional inputs:
- GAP-S4-R01 through R09 (DBL/IntD room-level gaps — Phase 3 insertion pass).
- FDR Tier 0 candidates (universal reach zone 380–1220 mm; rest seating on circulation routes).
- Case study evidence upgrades from Phase 2A evidence map.
- GAP-CO02-01 execution: delete IntD column from residential matrices.

**Checkpoint:** Part 5 content-final.

### P3-W05: Part 6 — Non-Residential Matrices (Session 14)

Per v10.1 plan. Additional inputs:
- GAP-S4-N01 through N07 (DBL/IntD non-residential gaps).
- GAP-CO02-01 execution: delete IntD column from non-residential matrices.

**Checkpoint:** Part 6 content-final.

### P3-W06: Part 7 — Item Library Categories A–E (Session 15)

Per v10.1 plan. Additional inputs:
- EXEC-READY specification resolutions: GAP-STEP5-01 (B-10 seizure), GAP-RAP-06 (DEAF RT60), GAP-SRS-01 (A-16 user control), GAP-034 (B-01 circadian), GAP-RAP-03 (A-08 NC-25 equivalence), GAP-059 (CHD-10 Rajotte), GAP-060 (A-16 NCSE), GAP-063 (G-03/G-04 Guay biomechanics).
- Connection register HIGH findings: CON-0001 (Tier 0 circulation legibility), CON-0002 (sensory relief room), CON-0003 (thermal comfort), CON-0007 (grab bar universal), CON-0010 (loop circulation DEM/NEU/NDV), CON-0011 (DBL hearing loop), CON-0014 (bedroom privacy/refuge), CON-0017–0019 (additional internal connections).
- External connections: CON-0021–0024 (TID validation, prospect-refuge, sensory taxonomy).
- FDR novel spatial parameters (PAIN/OFS: counter heights, storage zones, seating intervals, temperature ranges).
- Add `bpc_slugs` field to each item (BPC↔Item traceability).

**Checkpoint:** Categories A–E content-final.

### P3-W07: Part 7 — Categories F–K + BIO + TC (Session 16)

Per v10.1 plan. Additional inputs from FDR and connection register as applicable.

**Checkpoint:** All Part 7 categories content-final.

### P3-W08: Part 8 — Cross-Population Resolution & Collaboration (Session 17)

Per v10.1 plan. **Primary new-content session.**

Additional inputs — substantially richer than v10.1 anticipated:
- Connection register: 19 HIGH-confidence connections provide evidence base for §8.4. Expected: 15–20 entries have direct cross-population conflict or resolution implications.
- CON-0020 (DEAF glazed junction four-way conflict) → §8.5 unresolvable conflict.
- CON-0024 (trauma-informed design) → §8.1 theoretical framing.
- CON-0026 (SAE/SBI validation of three-tier approach) → §8.2 methodology grounding.
- FDR PAIN/OFS thermal conflict finding → §8.5 thermal zoning.
- FDR Tier 0 candidates → §8.2 resolution methodology (Tier 0 as resolution strategy for multi-population convergence).

§8.4 target now achievable: 12 from §3.4 + 5–8 from connection register + 3–5 from item conflict notes = 20–25 documented resolutions.

**Checkpoint:** Part 8 content-final.

### P3-W09: Parts 9–13 + Appendices + Bibliography (Session 18)

Per v10.1 plan. Additional inputs:
- Economics: CON-0031 (cost-effectiveness evidence), CON-0032 (Clemson Cochrane), Session 7 economics research.
- Case studies: Session 8 sourced case studies + evidence contribution fields.
- Part 10 reconceptualisation: CON-0028 (inclusive POE tools) feeds §10.4 (communication protocols should include POE stage).
- Bibliography: run `citation-verifier` HARVEST mode. Resolves GAP-CR-01 (empty bibliography).

**Checkpoint:** All Parts content-final. Document ready for structural pass.

---

## Phase 4: Structure (Sessions 19–20)

### P4-S1: Renumbering (Session 19)

Per v10.1 plan. Resolves GAP-CR-02 (section numbering collisions).

1. Generate final heading inventory from content-final document.
2. Apply Part renumbering map.
3. Run `bulk-renumber` in dry-run → review → apply.
4. Execute deferred production items: 82× "Chapter C" → "Part VIII §8.4"; 12× "Part VIII (case studies)" → "Part IX".
5. Generate Change Order CO-0003.

**Checkpoint:** All sections correctly numbered. Zero old numbering remains.

### P4-S2: File Decomposition + Cross-Reference Resolution (Session 20)

Per v10.1 plan. Resolves GAP-CR-03 (phantom cross-references), GAP-CR-04 (duplicate headings), GAP-CR-05 (ToC mismatch).

1. `file-splitter` → per-Part .md files.
2. `cross-reference-resolver` full scan including BPC↔Item traceability.
3. Fix orphan references (68+ phantom items).
4. Remove duplicate E-06/E-07/E-08/E-09 blocks.
5. Update `references/toc.md`.
6. Commit all files to GitHub.
7. Create assembly manifest.

**Phase 4 gate:** All files on GitHub. toc.md current. Zero orphan references. BPC↔Item links verified.

---

## Phase 5: QA + Assembly (Sessions 21–22)

### P5-Q1: Full Automated Audit Suite + Edition-Boundary Connection Scan (Session 21)

**QA audit (per v10.1):**
- `framing-checker` — social model, BAR-in-Vol-I, CRPD alignment.
- `evidence-marker` AUDIT — 100% ●/○ coverage check.
- `structure-auditor` — heading hierarchy across all files.
- `guidebook-auditor` — format, terminology, table consistency.
- `sensory-coherence-checker` — room matrices.
- `prose-style-checker` — register, voice, concision, ≤25-word specification sentences.
- `citation-verifier` — every cited source in bibliography.
- `cross-reference-resolver` — BPC↔Item bidirectional check.
- Manual spot-check: 10 cross-references per volume.

**Edition-boundary connection scan:**
- `connection-scout` internal mode — final scan on assembled, numbered document. Targets: any connections created by Phase 3 writing or Phase 4 restructuring that didn't exist in the pre-writing corpus. This is the PI-mandated edition-boundary run.
- `connection-scout` external mode — brief targeted scan for any literature published since Phase 2C (if >30 days have elapsed).
- New connections rated HIGH → P1 errata for v10.2a patch. MODERATE/SPECULATIVE → gap register for v11.

**Output:** QA findings register. Fix all P1/P2 issues inline. Connection register updated with edition-boundary findings.

### P5-Q2: Assembly + Final (Session 22)

1. `chunk-assembler` with manifest → master document.
2. Line count and heading count verification.
3. Final commit of assembled v10.2.
4. Close all resolved gap register items.
5. Update `project-standards.md`.
6. Final gap register reconciliation: all OPEN items carry a disposition (deferred to v11, accepted KNOWN-LIMITATION, or assigned to post-publication errata).
7. `session-consolidator` → final YAML.
8. Produce handoff summary.

**Phase 5 gate:** Assembled v10.2 on GitHub. Gap register reconciled. All QA findings resolved or logged. Connection register current. All state files reconciled.

---

## Integration Points: connection-scout and functional-deficit-researcher

### connection-scout Schedule

| Phase | Mode | Input corpus | Expected yield | Session |
|---|---|---|---|---|
| Pre-Phase 2B (already done) | Internal | Pre-Phase-2B BPC (14 population files) | 20 connections (done: CON-0001–0020) | Completed 2026-03-26 |
| Pre-Phase 2B (already done) | External | Current literature | 12 connections (done: CON-0021–0032) | Completed 2026-03-26 |
| Phase 2C | Internal | Post-Phase-2B BPC (upgraded slugs, new economics/case study data) | 5–10 new connections | Session 9 |
| Phase 2C | External | Targeted: POE, TID spatial evidence, KNOWN-LIMITATION resolution | 3–5 new connections | Session 9 |
| Phase 5 (edition boundary) | Internal | Assembled, numbered v10.2 document | 3–8 connections (created by writing/restructuring) | Session 21 |
| Phase 5 (edition boundary) | External | Literature published since Phase 2C | 0–5 connections (brief scan) | Session 21 |

**Disposition workflow:**
- HIGH → `item-specification-writer` briefing (Phase 3) or P1 errata (Phase 5).
- MODERATE → P2 gap register item.
- SPECULATIVE → P3 gap register item.

### functional-deficit-researcher Schedule

| Phase | Target slug(s) | Trigger | Scenarios | Session |
|---|---|---|---|---|
| Already done | pain-ofs-built-environment-design | Thin-base population | 12/12 COMPLETE (18 NOVEL, 4 Tier 0) | Completed 2026-03-26 |
| Phase 2C | mental-health-built-environment | ≥2 THIN flags expected | ≤12 | Session 9 |
| Phase 2C | neurological-built-environment | NEU/PCS thin provisions | ≤12 | Session 9 |
| Phase 2C | cross-population-conflict-resolution | New slug, thin by definition | ≤8 | Session 9 |
| Phase 3 (on demand) | Any item with `item-specification-writer` evidence gap | Triggered by writing | ≤6 per instance | Sessions 15–18 |

**Integration with `item-specification-writer`:**
- FDR NOVEL findings → add to item's evidence table with Tier classification.
- FDR REFINES findings → update specification value within item.
- FDR CONTRADICTS findings → route to `evidence-auditor` before inclusion.
- FDR TIER-0-CANDIDATE findings → propose for Tier 0 universal specification in Part 1/Part 8.
- FDR cross-pop findings → route to `connection-scout` for register.

---

## Decision Points (Complete — inherited from v10.1)

| ID | Question | Phase | Blocking | Status |
|---|---|---|---|---|
| DEC-01 | Per-item consolidation: approve/reject each merger | P1-D2 | Yes | PENDING — Session 2 |
| DEC-02 | Entry Path I table: absorb into §4.4 or cut? | P1-D1 | No | RESOLVED (D1-24: condense + move to §4.4) |
| DEC-03 | I-04/I-05/I-06: create, merge, or delete? | P1-D2 | Yes | PENDING — Session 2 |
| DEC-04 | H-05 (Nurse Call): create or redirect? | P1-D2 | No | PENDING — Session 2 |
| DEC-05 | IntD: full review or condensed proxy? | P1-D1 | Yes | RESOLVED (D1-17: condensed proxy) |
| DEC-06 | BIO/TC: promote to Part 7 or keep in appendix? | P1-D2 | No | PENDING — Session 2 |
| DEC-07 | Room matrix sub-tables: keep 6 or condense to 3? | P1-D2 | No | PENDING — Session 2 |
| DEC-08 | §12.4 Cost tables: restructure? | P1-D3 | No | PENDING — Session 3 |
| DEC-09 | Case studies: keep all 14 + expand | P1-D3 | No | PENDING — Session 3 |
| DEC-10 | Appendix E: separate appendix or glossary expansion? | P1-D3 | No | PENDING — Session 3 |
| DEC-11 | Worked examples: keep 5 or reduce to 3? | P1-D2 | No | PENDING — Session 2 |
| DEC-12 | F-02 (Fragrance-Free): keep or cut? | P1-D2 | No | PENDING — Session 2 |
| DEC-13 | A-17 (Upholstered Seating): keep or cut? | P1-D2 | No | PENDING — Session 2 |
| DEC-14 | Part 8 §8.8: how many worked resolution examples? | P1-D3 | No | PRELIMINARY (3 — D1-34) |
| DEC-15 | Part 10 §10.5 OT-Architect Interface: detail level? | P1-D3 | No | PENDING — Session 3 |
| DEC-16 | Pro forma templates: which building types? | P1-D3 | No | PENDING — Session 3 |
| DEC-17 | ROI model: practitioner-facing or developer-facing? | P1-D3 | No | PENDING — Session 3 |
| DEC-18 | Grant programmes: all 24 jurisdictions or top 8? | P1-D3 | No | PENDING — Session 3 |
| DEC-19 | Target populations for new case studies | P1-D3 | No | PENDING — Session 3 |
| DEC-20 | Case study template: add "Evidence Contribution" field? | P1-D3 | No | PENDING — Session 3 |

---

## Session Plan (Final)

| Session | Phase | Work |
|---|---|---|
| 1 | 0R | Reconciliation: slug migration, skill inventory, gap triage, github-io verification |
| 2 | P1 | Editorial: Parts 4–7 — **item consolidation gate** |
| 3 | P1 | Editorial: Parts 8–13 + Appendices — **Decision Register complete** |
| 4 | P2A | Pre-v4 slug triage (51 slugs) + case study evidence mining (14 studies) + post-decision gap triage |
| 5 | P2B | Foundations: Co-2 + CRPD + CONSUME backfill + threshold completion |
| 6 | P2B | Population: NDV/MH + NEU supplement + residential + SUPPLEMENT batch |
| 7 | P2B | Cross-population conflict evidence + economics deep-dive |
| 8 | P2B | Case study sourcing + remaining SUPPLEMENT/RE-RUN slugs |
| 9 | P2C | connection-scout re-scan (internal + targeted external) + FDR for newly COMPLETE slugs |
| 10 | P3 | Write: Front matter + Part 1 |
| 11 | P3 | Write: Part 2 (disability categories) + CO-0002 execution |
| 12 | P3 | Write: Parts 3 + 4 |
| 13 | P3 | Write: Part 5 (residential matrices) |
| 14 | P3 | Write: Part 6 (non-residential matrices) |
| 15 | P3 | Write: Part 7 Categories A–E |
| 16 | P3 | Write: Part 7 Categories F–K + BIO + TC |
| 17 | P3 | Write: Part 8 (NEW — cross-population resolution + collaboration) |
| 18 | P3 | Write: Parts 9–13 + Appendices + Bibliography + Glossary |
| 19 | P4 | Renumber (single pass, content-final document) |
| 20 | P4 | File decomposition + cross-reference resolution |
| 21 | P5 | Full QA audit suite + edition-boundary connection scan |
| 22 | P5 | Assembly, final commit, gap register close, handoff |

**Total: 22 sessions.** Phase 1 editorial decisions remain the critical path.

---

## Audit Recommendations — Implementation Tracker (Updated)

| Audit rec. | ID | Implementation | Session | Status |
|---|---|---|---|---|
| Reconcile skill inventory | §1.1a–c | Phase 0R reconciliation | 1 | PENDING |
| Build 6 missing skills | §1.2a | Phase 0 | — | **DONE** (all 6 built) |
| Update 10 skills | §1.3a | Phase 0 + Phase 0R verification | 1 | PARTIAL — verify in 0R |
| Add P1 gap for Co-2 | §4.1a | Phase 0R gap triage | 1 | PENDING |
| Promote I-04/I-05 | §5.3 | DEC-03 in P1-D2 | 2 | PENDING |
| Protect cross-population content | §5.2 | Part 8 dedicated part | 3, 17 | Part 8 scope confirmed (D1-29–34) |
| Resolve ●/○ ambiguity | §4.2a | P1-D2 notation guide decision | 2 | PENDING |
| Pre-v4 slug triage | §5.1 | Phase 2A | 4 | PENDING |
| Fix duplicate slugs | §2.2a | Phase 0R slug migration | 1 | PENDING |
| Enforce slug naming | §2.2b | Phase 0R slug migration | 1 | PENDING |
| Mine case studies for evidence | §5.4 | Phase 2A evidence mining | 4 | PENDING |
| BPC↔Item mapping | §5.5 | Phase 3 item writing | 15–16 | PENDING |
| Backfill pre-v4 slugs | §2.1 | Phase 0R migration + Phase 2B CONSUME | 1, 5 | PARTIAL (migration Phase 0R; metadata Phase 2B) |
| Strengthen residential primacy | §5.6 | Phase 3 Part 1 writing | 10 | PENDING |
| Migrate BPC/SL storage | (new) | Phase 0R | 1 | PENDING |
| Build connection-scout SKILL.md | (new) | Phase 0R | 1 | PENDING |
| Dispose keyword-lookup | (new) | Phase 0R | 1 | PENDING |
| Verify working doc persistence | (new) | Phase 0R | 1 | Rule exists; verify enforcement |

---

## Risk Register (Updated)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase 1 scope decisions don't narrow enough → Phases 2–3 bloat | Medium | High | DEC-01 (item mergers) and DEC-07 (sub-tables) are the biggest scope levers; resolve early in Session 2 |
| Slug migration creates path resolution errors | Low | Medium | Test 5 slugs after migration; flat files frozen (not deleted) as fallback |
| Part 8 new content exceeds single session | Medium | Medium | §8.4 now has richer input from connection register (15–20 entries); reduces novel writing. §8.6–§8.7 draw from existing Part 9/10 content |
| Economics research finds thin pro forma data | High | Medium | Fallback: worked examples with placeholder values marked [DATA NEEDED] |
| Case study sourcing for PAIN/OFS yields <3 studies | High | Medium | PAIN/OFS are genuinely under-documented; accept THIN-BASE with honest disclosure |
| FDR runs yield diminishing returns for non-PAIN populations | Medium | Low | Cap at 12 scenarios per slug; diminishing-return gate (3 consecutive no-yield → stop) |
| Connection register exceeds 50 entries → information overload | Medium | Low | Only HIGH-confidence findings feed Phase 3 writing. MODERATE/SPECULATIVE → gap register only. |
| `/mnt/project/` cannot be updated (read-only) | Certain | Medium | Rule: skills not in `/mnt/project/` must be read from GitHub via GET before execution. PI definitions govern. |

---

## Token Efficiency Analysis

### Gains vs v10.1

| Source | Mechanism | Saving |
|---|---|---|
| Phase 0 compression (2→1) | Builds already done; reconciliation only | ~4,000 tokens (one session) |
| Phase 1 compression (3→2) | P1-D1 already complete | ~4,000 tokens (one session) |
| Phase 2B compression (5→4) | PAIN/OFS + bathroom + kitchen + threshold + 8 gap resolutions already done | ~8,000 tokens |
| Credited connection discovery | 32 connections already feed Part 8 + item writing — no re-discovery needed | ~6,000 tokens |
| Credited FDR PAIN/OFS | 18 NOVEL findings already in BPC — no re-research needed | ~3,000 tokens |
| Slug storage migration | Eliminates per-CHECK path ambiguity and dual-architecture maintenance | ~500 tokens/session × 22 sessions = ~11,000 tokens |

### Costs of v10.2 Additions

| Addition | Cost (sessions) |
|---|---|
| Phase 2C (connection + FDR) | 1.0 (new dedicated session) |
| Phase 0R slug migration | 0.4 (within reconciliation session) |
| Edition-boundary connection scan | 0.3 (within QA session) |
| **Net new** | **~1.0 session equivalent** |

### Net Assessment

v10.1: 24 sessions. v10.2: 22 sessions. Net saving: 2 sessions despite expanded connection-scout and FDR integration. Saving comes from crediting completed work rather than re-planning it.

---

## Unresolved Blockers (Inherited)

| Blocker | Status | Action |
|---|---|---|
| Full bibliography | NOT AVAILABLE | citation-verifier in provisional mode; resolved by Phase 3 Session 18 HARVEST |
| Application volume full text | NOT AVAILABLE | volii-validator in provisional mode |

## Deferred Production Items (Inherited)

- 82× "Chapter C" → "Part VIII §8.4" (Phase 4 Session 19)
- 12× "Part VIII (case studies)" → "Part IX" (Phase 4 Session 19)

---

*End of Workplan v10.2*
