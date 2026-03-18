# Project Standards
<!-- Managed by session-consolidator. Do not edit manually. -->
<!-- Append new RULE blocks at the bottom. Never overwrite existing entries. -->

---

## Core Doctrine (locked)

RULE: Three-Tier Design Hierarchy governs all specifications. Tier 0 = Universal Design / Code Compliance (population-agnostic, fixed values). Tier 1 = Population-Informed Inclusive Design (ranges; median as default). Tier 2 = Person-Specific Co-Design (OT assessment resolves position within Tier 1 range). DAR mandatory at all tiers.
CONDITION: All specification items.
ACTION: Every item must identify which tier it serves and apply that tier's specification standard.
DATE: Established — pre-session

RULE: Universal design is co-extensive with code compliance — the floor, not an aspiration. Inclusive design is the positive aspiration.
CONDITION: All editorial and framing decisions.
ACTION: Never frame UD as aspirational. Never frame ID as obligatory minimum.
DATE: Established — pre-session

RULE: BAR is not a main taxonomy code. Large body size is not a disability. BAR provisions belong in Supplementary Volume §IV only. Category J (J-01 through J-05) is to be struck entirely from Volume 2 Part IV. No BAR reference, cross-reference, or heading is permitted anywhere in Volumes 1–3. Delete on sight; do not relocate — items already exist in Supplementary Volume §IV.
CONDITION: Any item, cross-reference, or heading in Volumes 1–3.
ACTION: Flag and delete any BAR or J-code instance in Volumes 1–3. Do not replace with Supplementary Volume pointers.
DATE: Established — pre-session; updated 2026-03-18 20:10

RULE: Specification ranges are not expressions of uncertainty. They are the designed-in bridge between Tier 1 and Tier 2. At Tier 1 use median. At Tier 2 resolve through co-design.
CONDITION: All range specifications.
ACTION: Never write a range without specifying which end applies at which tier.
DATE: Established — pre-session

RULE: Lived experience evidence is co-primary at Tier 3–4 where no clinical trial is feasible.
CONDITION: Evidence stratification decisions.
ACTION: Do not subordinate lived experience evidence to clinical research when no RCT is feasible for the population.
DATE: Established — pre-session

RULE: VIS and DEAF are separate independent population codes — never grouped or combined. VIS = visual impairment. DEAF = Deaf/hard of hearing/hearing device users. DBL = DeafBlind — a third distinct population, not a combination of VIS + DEAF. VIS/DEAF as a compound code is an error requiring correction on sight.
CONDITION: All population code usage throughout Volumes 1–3, matrices, item specs, glossary, abbreviations.
ACTION: Replace all VIS/DEAF compound instances with standalone VIS or DEAF as appropriate. Update all matrices, glossary, and quick reference tables.
DATE: Established — pre-session; updated 2026-03-18 20:20

RULE: IntD (Intellectual Disability) is a main-body population category. It appears in Volume 1 Part II and receives full item coverage in Volume 2 matrices, residential and non-residential. All IntD specifications carry THIN-BASE disclosure: [TIER 4-5; no quantified architectural standard in any jurisdiction; March 2026].
CONDITION: Any task touching IntD population coverage.
ACTION: Treat IntD as a full main-taxonomy category. Author items in main body. Apply THIN-BASE disclosure to all IntD specifications.
DATE: 2026-03-18 20:20

RULE: Biophilic Design (BIO-01–BIO-05) and Thermal Comfort (TC-01–TC-05) are canonical in Volume 3 Appendix B and Appendix C respectively. Supplementary Resources A and B in the Volume 2 body are to be struck. No inline BIO- or TC- cross-references are permitted in Part IV item specs or room matrices. A single opening notice is permitted in volume front matter: "This guidebook includes supplementary appendices covering biophilic design (Appendix B) and thermal comfort (Appendix C)."
CONDITION: Any edit touching Volume 2 body or Part IV item specs.
ACTION: Delete Supplementary Resources A and B from Volume 2. Remove all inline BIO- and TC- cross-references. Retain opening notice only.
DATE: 2026-03-18 20:10; consolidated 2026-03-18 20:20

---

## Item Code System

RULE: V2-P4-XX is the canonical item code system. V2-PV-XX is deprecated and must not be used.
CONDITION: All item codes in all volumes.
ACTION: Replace any V2-PV-XX instance on sight.
DATE: Established — pre-session

---

## Citation and Evidence Standards

RULE: All sources must be confirmed real before inclusion. Unverified claims → [UNVERIFIED — DOI/URL required before publication].
CONDITION: All citations.
ACTION: Never silently remove unverified claims — flag them. citation-verifier defaults to PROVISIONAL mode.
DATE: Established — pre-session

RULE: G-03 cites two Levine papers — Levine 2023 (Human Factors) AND Levine 2025 (JMIR). Both required.
CONDITION: Item G-03 and room matrix R-BA-02.
ACTION: Levine 2023: doi:10.1177/00187208211059860. Levine 2025: doi:10.2196/69442. Replace any "Levine 2024" reference with both.
DATE: 2026-03-17 21:30

RULE: NIH NIOSH storage height claim (40% strain reduction at shoulder-hip zone) — primary source not confirmed.
CONDITION: Any citation of this claim in PAIN items.
ACTION: Flag [UNVERIFIED — DOI/URL required before publication] until primary source retrieved.
DATE: 2026-03-18 10:00

RULE: If a publication blocker requires citation verification and two or more independent searches across sessions have returned no confirmed source, the item or specification value is to be deleted rather than indefinitely flagged. Deletion is the resolution. Do not accumulate unresolvable UNVERIFIED flags. Log deletion in gap_register.md as CLOSED-DELETED.
CONDITION: Any specification value carrying [UNVERIFIED] after two or more failed independent search attempts.
ACTION: Delete the specific value or claim. Retain the item structure if the remainder is evidence-supported.
DATE: 2026-03-18 19:10

---

## Specification Upgrades (rules confirmed by evidence)

RULE: E-08 corridor primary route specification is ≥1500 mm (not 1200 mm).
CONDITION: Any primary route corridor specification in public buildings.
ACTION: Upgrade to ≥1500 mm citing DIN 18040-1 + TEK17 §8-6. Note: 1200 mm acceptable for secondary residential corridors only.
DATE: 2026-03-17 21:30

RULE: C-04 LRV contrast is a split tiered table within the single item C-04. No new item code is created. Row 1: general accessible environments ≥30 LRV. Row 2: critical navigation junctions ≥40 LRV. A note is added for severe VIS users: environments serving severe VIS may require ≥65% Michelson contrast at critical junctions and signage (Dain 2022; DIN 32975 K≥0.7). Conflict resolution note cross-referencing C-04 vs C-05 to be added in Part E.
CONDITION: C-04 item specification and any item citing LRV thresholds.
ACTION: Replace single-value spec with two-row tiered table. Add severe-VIS note. Add Part E conflict note.
DATE: 2026-03-17 21:30; updated 2026-03-18 20:20

RULE: Ramp gradient for independent propulsion — evidence maximum is 6% (1:16.7), not 8.3% (1:12).
CONDITION: E-03 and all ramp gradient specifications.
ACTION: Maintain ADA 1:12 as Tier 0 code floor. State 6% (DIN 18040; TEK17) as Tier 1 evidence-supported maximum for independent propulsion. 8.3% acceptable only for short assisted rises ≤0.30 m.
DATE: 2026-03-18 10:00

RULE: Turning circle standard values serve ≤50th percentile of wheelchair users. 95th percentile power chairs require 2100 mm; scooters require 2489 mm.
CONDITION: All turning circle specifications.
ACTION: Tier 1 range: 1300 mm (indoor manual, minimum) → 2100 mm (power chair, preferred). Specify 2489 mm for scooter-inclusive environments. Cite D'Souza 2011 + CSA B651:23.
DATE: 2026-03-18 10:00

RULE: E-10 rest seating interval is 25–30 m (Tier 1 range; median 27.5 m), replacing the previous 20 m value. OFS populations additionally require reclining/tilt seating option at each station.
CONDITION: E-10 item specification and all room-matrix references to rest seating interval.
ACTION: Update E-10 to 25–30 m range with 27.5 m median. Add OFS seating-type note. Update all room matrices referencing the 20 m value.
DATE: 2026-03-18 20:20

RULE: H-04 does not include temperature specification. Temperature for OFS/PAIN populations is addressed exclusively in Thermal Comfort Appendix C. Any temperature content in H-04 is to be removed and replaced with: "For thermal environment requirements for OFS and PAIN populations, see Appendix C."
CONDITION: H-04 item specification.
ACTION: Remove temperature content from H-04. Add single cross-reference note to Appendix C.
DATE: 2026-03-18 20:20

---

## Structural Decisions

RULE: B-10 strobe VAD seizure risk is a gap across all European standards.
CONDITION: B-10 specification.
ACTION: Retain item. Flag as [SYSTEMIC GAP — no European standard specifies strobe frequency limit for VAD; UK interim guidance only].
DATE: 2026-03-17 21:30

RULE: All PAIN and OFS item specifications must carry: "Specifications for this item serving PAIN and/or OFS populations are derived from expert consensus and clinical evidence; no built-environment design research base exists for these populations in any of 14 languages searched (March 2026). [EXPERT CONSENSUS — March 2026]"
CONDITION: Any item specification serving PAIN or OFS populations.
ACTION: Apply disclosure note to all PAIN/OFS provisions including E-10, G-06, A-09, and all room matrix provisions.
DATE: 2026-03-18 18:30

RULE: DBL room matrix additions carry: [EXPERT CONSENSUS — no standard; March 2026]. IntD room matrix additions carry: [TIER 4-5; March 2026]. Both disclosures are mandatory.
CONDITION: Any DBL or IntD provision added to room matrices.
ACTION: Apply respective disclosure per item-spec-revisions-2026-03-18-18-00.md §6.
DATE: 2026-03-18 18:30

RULE: DBL is included in the Part III co-occurrence matrix (§III.3) and co-occurrence design guidance (§III.4) as a standalone population. A note at the end of §III.4 explains that DBL requirements arise from the primacy of tactility and combined sensory loss — not from the sum of VIS and DEAF provisions.
CONDITION: Part III co-occurrence matrix and guidance.
ACTION: Add DBL row/column to §III.3. Add DBL guidance to §III.4. Add explanatory note at end of §III.4.
DATE: 2026-03-18 20:20

RULE: Part I section §1.11 Scope is renumbered to §1.9. No content authored for the gap. All cross-references to §1.11 updated to §1.9.
CONDITION: Part I section numbering.
ACTION: Renumber §1.11 → §1.9. Update all cross-references throughout the document.
DATE: 2026-03-18 20:20

RULE: Part V (Engineering and Coordination) contains placeholder headings only. Each of V.1–V.5 carries: "Brief template to be provided. Engage relevant specialist consultant at [design stage]." No templates to be authored in this edition.
CONDITION: Part V content.
ACTION: Add placeholder note under each V.1–V.5 heading.
DATE: 2026-03-18 20:20

RULE: De-escalation rooms are out of scope. No item to be authored. May be noted in gap register only.
CONDITION: Any request to author a de-escalation room item.
ACTION: Decline item creation. Log as scope-exclusion if raised.
DATE: 2026-03-18 20:20

RULE: IntD-specific emergency egress is covered by the existing deferral to jurisdiction-specific building codes (Appendix D). No separate IntD egress item to be authored.
CONDITION: Any request to author IntD egress provisions.
ACTION: Refer to Appendix D deferral. No new item.
DATE: 2026-03-18 20:20

RULE: When Category J cross-references are struck from room matrices, entry paths, and reading guides, they are deleted without replacement. No pointer to Supplementary Volume §IV is added.
CONDITION: find-and-replace pass striking Category J.
ACTION: Delete all J-code cross-references. Do not replace.
DATE: 2026-03-18 20:20

---

## Research Log Standards

RULE: research-log-manager CHECK must be called before any multilingual-research run. research-log-manager LOG must be called after every run. Skipping either is an error.
CONDITION: Every multilingual-research invocation.
ACTION: No exceptions. If LOG was missed in a prior session, flag as BLOCKER in the next session-close YAML.
DATE: Established — pre-session

RULE: Staleness threshold for BPC entries is 90 days. Entries older than 90 days → STALE on CHECK. Re-run multilingual-research for any STALE entry in an active section.
CONDITION: All BPC retrieval operations.
ACTION: Compare last_searched date to current date. If >90 days: status = STALE, proceed to full re-run.
DATE: Established — pre-session

RULE: SCOPE-GATE-CANDIDATE: 3+ independent searches returning NO-DATA for the same language across different topics → append P3 item to gap_register.md.
CONDITION: research-log-manager LOG operations.
ACTION: DA, FI, ZH, JA confirmed SCOPE-GATE-CANDIDATEs for PAIN/OFS population searches. Never permanently exclude a language.
DATE: 2026-03-18 10:00

RULE: Early-close gate is SUSPENDED for all multilingual-research runs on population categories and item-level searches. All 9 core languages must be fully searched before a run closes. EXCEPTION: IntD only — early-close gate remains active; literature is confirmed absent in non-English sources.
CONDITION: Any multilingual-research run except IntD.
ACTION: Run all 9 core languages to completion. Do not close at early-close gate. Record all NO-DATA and THIN results explicitly.
DATE: 2026-03-18 15:00

---

## Session Management

RULE: Never re-run a completed stage. Consume existing outputs.
CONDITION: Session start and task intake.
ACTION: Confirm completed stages from session close YAML before beginning work.
DATE: Established — pre-session

RULE: All timestamps must include hour and minute: YYYY-MM-DD HH:MM. No date-only timestamps.
CONDITION: All outputs, file names, YAML entries.
ACTION: Enforce without exception.
DATE: Established — pre-session

RULE: Context limit approaching → complete current stage, invoke session-consolidator, instruct user to start new chat.
CONDITION: Context approaching limit.
ACTION: Prioritise clean session close over partial additional work.
DATE: Established — pre-session

RULE: Session logs are stored at sessions/session_YYYY-MM-DD-HHMM.md — one new file per session. Legacy session_log.md is deprecated as of 2026-03-18.
CONDITION: All session start and session end operations.
ACTION: workplan-orchestrator: LIST sessions/ directory, sort descending, GET most recent file. session-consolidator: CREATE new sessions/session_{YYYY-MM-DD-HHMM}.md — never append to existing. Do not read or write session_log.md.
DATE: 2026-03-18 18:30

RULE: Updated skill files are written to skills/ directory on GitHub. When a skill has both a project file and a skills/ GitHub file, the GitHub version takes precedence.
CONDITION: Any skill updated through the 2026-03-18 audit.
ACTION: Check skills/{skill-name}_SKILL.md on GitHub first. Fall back to /mnt/project/{skill-name}_SKILL.md only if not found on GitHub.
DATE: 2026-03-18 18:30
