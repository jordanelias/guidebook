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

RULE: BAR is not a main taxonomy code. Large body size is not a disability. BAR provisions belong in Supplementary Volume only.
CONDITION: Any item in Volumes 1, 2, or 3.
ACTION: Any BAR-coded item found in Volume 2 main taxonomy is a doctrine violation — flag P1 and remove.
DATE: Established — pre-session

RULE: Specification ranges are not expressions of uncertainty. They are the designed-in bridge between Tier 1 and Tier 2. At Tier 1 use median. At Tier 2 resolve through co-design.
CONDITION: All range specifications.
ACTION: Never write a range without specifying which end applies at which tier.
DATE: Established — pre-session

RULE: Lived experience evidence is co-primary at Tier 3–4 where no clinical trial is feasible.
CONDITION: Evidence stratification decisions.
ACTION: Do not subordinate lived experience evidence to clinical research when no RCT is feasible for the population.
DATE: Established — pre-session

RULE: VIS/vis ≠ VIS/DEAF ≠ DBL. Three populations with minimal technical overlap.
CONDITION: All population tagging and item specification.
ACTION: Never conflate. Never merge population codes for these three groups.
DATE: Established — pre-session

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

---

## Specification Upgrades (rules confirmed by evidence)

RULE: E-08 corridor primary route specification should be ≥1500 mm, not 1200 mm.
CONDITION: Any primary route corridor specification in public buildings.
ACTION: Upgrade to ≥1500 mm citing DIN 18040-1 (primary routes in public buildings) + TEK17 §8-6 (1.4–1.8 m approach routes). Note: 1200 mm acceptable for secondary residential corridors only.
DATE: 2026-03-17 21:30

RULE: C-04 LRV ≥30 is insufficient for severe VIS users. Evidence supports ≥65% Michelson contrast.
CONDITION: C-04 specification and any item citing 30% LRV as the evidenced threshold.
ACTION: Retain 30% LRV as the code floor (Tier 0). Add ≥65% Michelson contrast as Tier 1 specification for VIS-primary environments. Cite Dain 2022 + DIN 32975 K≥0.7 for signage text.
DATE: 2026-03-17 21:30

RULE: Ramp gradient for independent propulsion — evidence maximum is 6% (1:16.7), not 8.3% (1:12).
CONDITION: E-03 and all ramp gradient specifications.
ACTION: Maintain ADA 1:12 as Tier 0 code floor. State 6% (DIN 18040; TEK17) as Tier 1 evidence-supported maximum for independent propulsion. 8.3% acceptable only for short assisted rises ≤0.30 m.
DATE: 2026-03-18 10:00

RULE: Turning circle standard values serve ≤50th percentile of wheelchair users. 95th percentile power chairs require 2100 mm; scooters require 2489 mm.
CONDITION: All turning circle specifications.
ACTION: Tier 1 range: 1300 mm (indoor manual, minimum) → 2100 mm (power chair, preferred). Specify 2489 mm for scooter-inclusive environments. Cite D'Souza 2011 + CSA B651:23.
DATE: 2026-03-18 10:00

---

## Structural Issues (active — confirmed)

RULE: BAR items J-01 through J-05 in Volume 2 main taxonomy are doctrine violations.
CONDITION: Volume 2 item list.
ACTION: Remove J-01–J-05 from main taxonomy. Relocate to Supplementary Volume with cross-reference. P1 escalation confirmed 2026-03-17.
DATE: 2026-03-17 21:30

RULE: B-10 strobe VAD seizure risk is a gap across all European standards.
CONDITION: B-10 specification.
ACTION: Retain item. Flag as [SYSTEMIC GAP — no European standard specifies strobe frequency limit for VAD; UK interim guidance only]. P1 confirmed 2026-03-17.
DATE: 2026-03-17 21:30

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
ACTION: DA, FI, ZH, JA confirmed SCOPE-GATE-CANDIDATEs for PAIN/OFS population searches. Never permanently exclude a language — only recommend moving to extended set for specific population topics.
DATE: 2026-03-18 10:00

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

RULE: Context limit approaching → complete current stage, invoke session-consolidator, instruct user to start new chat. Do not attempt to squeeze additional stages into a limited context.
CONDITION: Context approaching limit.
ACTION: Prioritise clean session close over partial additional work.
DATE: Established — pre-session
