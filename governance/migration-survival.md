# Migration Survival Register

**Status:** CANONICAL — adopted by project owner 2026-05-02 01:37 (instruction "perform all" in audit-remediation continuation session)
**Doctrinal basis:** workplan/workplan-co0007-v3.md §Salvage matrix; governance/repo-strategy.md; project-standards 2026-04-25 best-practice rule; A6 evidence-methodology.md §Evidence-state machine; A12 decision-protocol.md §1 categories
**Audit basis:** audit_2026-04-30 R1 — Block 33 supersession created a kept-research/retired-form overhang with no canonical "what survives migration" register. This document is that register.
**Issued (PROVISIONAL):** 2026-05-01 04:30
**Adopted (CANONICAL):** 2026-05-02 01:37
**Last updated:** 2026-05-02 01:37

---

## 1. Purpose

CO-0007 Block 33 (2026-04-24/25) declared that the project's then-current form (markdown specifications + Appendix A tables + BPC `best_practice_synthesis` fields derived from code consensus) is the wrong long-term medium for several mission-load-bearing requirements. The synthesis workplan reframes ~280+ pre-pivot commits as input data, not deliverables to patch.

This created a problem the workplan acknowledged but did not fully resolve: the boundary between *kept-research* and *retired-form* was distributed across the synthesis document, the workplan, and a few session notes. No single canonical register named what crosses Stage C as-is, what re-derives, what retires.

This document is that register. It exists to:

1. **Prevent silent re-use of retired content.** A future agent (or future Claude session) reading a Block-32-struck claim from a pre-pivot BPC must be able to identify it as suspect from a single canonical lookup, not a multi-document trace.
2. **Make migration scope visible.** Stage C is currently estimated at 140–200 sessions. Without an itemised register, that estimate is not auditable. With one, it is.
3. **Expose unresolved migration questions.** Several categories sit in the "open" state (e.g., voice-style work pending A4 disposition); naming them centrally surfaces them for decision rather than leaving them dependency-implicit.

Per workplan v3 §Salvage matrix, this register expands the five-row salvage matrix into per-category detail with per-file specificity where applicable.

---

## 2. Scope and boundaries

### 2.1 What this document is

A canonical register of every artifact category in the pre-pivot corpus, classified by survival disposition, with explicit forward dependencies on Stage A/B/C decisions that can change classification.

### 2.2 What this document is not

- A migration *plan*. Stage C phases C1–C11 own that.
- A *content audit*. Each surviving artifact still requires per-item verification at migration time; this register classifies categories and flags content-level conditions, not individual files.
- A *supersession order*. Categories marked SUPERSEDED here are operationally retired but not deleted; the historical commits remain in git history and may be cited as audit trail. Deletion (if any) happens at Stage C close.

### 2.3 Adoption note

This register was issued PROVISIONAL on 2026-05-01 and adopted CANONICAL on 2026-05-02. The single-context risk that motivated the PROVISIONAL marker (audit R4 — same conversation produced both the audit recommending the register and the register itself) is mitigated by:

- Project-owner explicit adoption instruction ("perform all") rather than tacit acceptance
- The companion `references/audits/methodological-audit_2026-04-30.md` and `references/audits/critical-workplan_2026-04-30.md` (Sonnet, fresh-context) provide independent governance triangulation for the broader corpus this register classifies
- Per-row classifications carry forward dependencies (§7) that surface for re-evaluation as gating decisions land

External review of this register (per governance/decision-protocol.md DG-REVIEW pattern) remains available and is queued in `workplan/external-review-queue.md` (item EQ-21 — newly added at adoption). Adoption does not foreclose subsequent amendment.

The "Reusable conditionally" category still requires per-file contamination assessment; that work is C-stage migration scope, not pre-adoption scope.

---

## 3. Disposition categories

Five categories, derived from workplan v3 §Salvage matrix with definitional refinements:

| Disposition | Definition | Migration action |
|---|---|---|
| **SURVIVES_AS_IS** | Content can be migrated with mechanical transformation only (format change, structural re-keying). No re-derivation, no re-verification beyond schema validation. | Convert to target form per Stage C phase; no human re-review. |
| **SURVIVES_WITH_REDERIVATION** | Content's underlying data survives but the synthesis layer is retired. Re-derivation produces new synthesis from the surviving inputs. | Retain inputs; re-author synthesis at migration time using post-Stage-A doctrinal apparatus (A6 evidence-state machine; A7 taxonomy; A12 decision protocol). |
| **SURVIVES_CONDITIONALLY** | Per-instance assessment required. Some files in the category survive as-is; others survive with re-derivation; others are superseded. The disposition for each file is determined by its content state. | Assess per-file at migration time using §5 decision rules; classify each into one of the other three terminal states. |
| **SUPERSEDED** | Operationally retired. Not migrated. Historical record only. | No migration action; reference for audit only; delete at Stage C close per project-owner discretion. |
| **OPEN** | Disposition cannot be determined yet — depends on a Stage A/B/C decision not yet made. | Hold until the gating decision lands; reclassify at that point. |

Note: SUPERSEDED ≠ wrong. Many superseded artifacts captured the project's actual state at their authoring time. Supersession reflects that the form they took is being retired, not that their content was incorrect. Some superseded artifacts (e.g., audit v1) are explicitly retained as audit trail.

---

## 4. Per-category register

The 14 categories below cover every pre-pivot artifact class. Each row carries: category, disposition, count or scope, gating dependencies, and notes.

### 4.1 Research data

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| Jurisdictional values (per BPC; consensus findings tables) | SURVIVES_AS_IS | ~300 BPC consensus-finding entries across 95 BPCs | None | Already valued, sourced, and verified during Phase 2A/2B. Migration is mechanical — the values move; the synthesis prose is what gets re-derived. |
| Verified evidence sources (bibliography) | SURVIVES_AS_IS | 584 sources; 86% verified (Tier 1–6); residual 14% (84 sources) UNVERIFIED-1 | C7 disposition | The 86% verified portion crosses unchanged. The 14% UNVERIFIED-1 residual is OPEN pending project-owner decision (forward to BPC authors for re-source, or CLOSED-DELETED). |
| Multilingual coverage (concept-boundary tables; native aliases) | SURVIVES_AS_IS | 64 slugs × ~14 languages = ~900 entries | None | Per-slug concept-boundary mapping is reusable as-is in any storage form. |
| Co-1 corpus (cited lived-experience sources) | SURVIVES_AS_IS | 25 entries (per A5 Co-1 verification) | A5 forward — Co-2 admissibility | Co-1 entries are core; A5 §6.3 verification report is the authoritative count. |
| Search logs | SURVIVES_AS_IS | ~125 search-log files (Phase 2B output) | None | Audit-trail value; small storage; retain. |
| Jurisdictional standards registry | SURVIVES_AS_IS | 103 standards entries; 49 jurisdictions registered; 24 canonical coverage | A8 §3 currency management | Currency status flagged per entry; A8 governance applies. |
| 3 Block-32 [STRUCK] claims residue (Rhee 2023 indoor vegetation; INSERM Village Landais 31%; Kapsalis tenji SR) | SUPERSEDED | 3 inline `[STRUCK]` markers in pre-pivot BPCs | None — see §6 below | Block 32 (2026-04-24 09:15) struck the underlying sources per 2-failed-search rule. The claims remain marked in BPC text; migration must either re-source (deferred Opus session) or remove with rationale. |

### 4.2 Synthesis layer

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| BPC `best_practice_synthesis` fields | SURVIVES_CONDITIONALLY | 78 BPC entries (per A3 BPCMetadata count) — minus 2 MERGED | Per-file Stage C contamination assessment | Per RC-001 and RC-002 sampling: ~53–60% CLEAN, ~20–33% AMBIGUOUS, ~7% STUB, ~7% MERGED. Stage C C-stage migration does the per-file pass. CLEAN cases survive_with_rederivation (synthesis prose re-authored against post-Stage-A apparatus); AMBIGUOUS cases require evidence-state-machine re-application; STUB cases re-synthesise from the underlying research data; MERGED cases retire the redirect. |
| Part 4 item specifications (~92 items) | SUPERSEDED | 92 spec-db records as currently written | None | Workplan v3 §Salvage matrix marks Part 4 specs as superseded form. Underlying jurisdictional values (the rows in jurisdiction comparison tables) are SURVIVES_AS_IS per §4.1; the prose synthesis around them retires. |
| Appendix A tables (24 tables) | SUPERSEDED | 24 Appendix A tables as currently framed | None | Same logic as Part 4 — the data tables' underlying values survive; the framing prose retires. |
| "Shall be" specification voice | SUPERSEDED | All occurrences across Part 4, Appendix A, and BPC synthesis | A4 voice style | Per project-standards 2026-04-26 advocacy-identity rule. Tier-appropriate language replaces it at migration time. |

### 4.3 Skill methodologies

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| Skill methodology structure (the *what each skill does* layer) | SURVIVES_AS_IS | ~45 skill files | C2 — skill rebuild | Methodology survives; output target and synthesis logic change. C2 rewrites the implementation, not the methodology. |
| Skill validators (pre-A6 paradigm) | SURVIVES_WITH_REDERIVATION | ~10 pre-A6 validators | C2 + A6 evidence-state machine | Validation paradigm reusable; specific checks rewrite to apply A6 evidence-state machine. |
| skills/voice-style_SKILL.md | OPEN | 1 skill file | A4 disposition | A4 voice phase outcome determines voice-style skill survival. Per workplan v3 §Salvage matrix this is explicitly marked OPEN. |
| Retired skills (workplan v3 §C2 cut-list) | SUPERSEDED | 10 skills marked for deprecation per CO-0008 §Layer 2 | None | Per CO-0008 scope-overhaul: 10 skills retire as part of infrastructure rebuild. |

### 4.4 Validators (post-A6 paradigm)

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| schemas/* (A3 entity classes + A6/A7/A8/A9/A10/A12/A13 extensions) | SURVIVES_AS_IS | 12 schema files; 34 enum classes; 6+ entity types | None | Authored under post-Stage-A doctrine; survives. |
| scripts/validate_*.py (A6/A7/A8/A9/A10/A12/A13 validators) | SURVIVES_AS_IS | 8 validator scripts | None | Authored under post-Stage-A doctrine; survives. |
| .github/workflows/ci.yml (post-CI-integration commit `0d9551cdbfbb`) | SURVIVES_AS_IS | 1 workflow file | None | Post-2026-04-30 ci-s1 is the canonical baseline. |

### 4.5 Connection register

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| Connection records (CON-NNNN) | SURVIVES_AS_IS | 191 connections per A3 Connection entity count | None | Cross-reference structure intact; re-rendering only. |
| `references/connections/_index.md` | SURVIVES_AS_IS | 1 index file | None | PI start-protocol references this; A12 §6.2 session-consolidator wiring depends on it. |

### 4.6 Governance corpus

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| governance/* CANONICAL docs (12+ docs from A1–A13) | SURVIVES_AS_IS | 12 CANONICAL docs as of 2026-04-30 | None | Authored under post-pivot doctrine; survives. |
| governance/mission-PROVISIONAL.md | SUPERSEDED | 1 doc | A1-A2 iter 4 close | Superseded by mission-and-epistemics.md (CANONICAL). Retain as audit trail. |
| governance/armature_v3_review.md and armature_v4*.md (4 docs) | SURVIVES_AS_IS | 4 docs | A7 → reference vs canonical | Armature documents are pre-decision artifacts feeding A7 (population taxonomy) decisions. Their status as "pre-decision" makes them durable input to A7 — they survive but their classification (reference vs canonical) depends on A7 outcome. |
| governance/pre-decision-multimodal-access-armature.md | SURVIVES_AS_IS | 1 doc | None | Pre-decision artifact; audit-trail value. |
| governance/repo-strategy.md | SURVIVES_AS_IS | 1 doc | None | Stage 0.8 deliverable; durable. |
| governance/workplan-adoption.md | SURVIVES_AS_IS | 1 doc | None | Stage 0.9 decision record. Will eventually pair with a queryable Decision record (D-NNNN) in the register; the document itself survives as the authoritative narrative. |

### 4.7 Decision register

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| `data/decisions/decision_register.yaml` records | SURVIVES_WITH_REDERIVATION | 128 records as of 2026-05-02 (106 seeded placeholder + 22 non-placeholder: D-0107 ci-integration; D-0108–D-0113 from B1 sessions 1–2; D-0114–D-0118 from audit-remediation; D-0119 from B1-S3; D-0120–D-0128 from audit-remediation continuation) | A12 placeholder review (Tier C executed 2026-05-02; Tier A/B pending) | The register structure survives. The 106 seeded placeholder records require rationale-review per audit R3 (Tier C mechanical batch handled 2026-05-02 by D-0121; Tier A/B pending project-owner sequencing per workplan/placeholder-review-triage.md). The 22 non-placeholder records have proper model_routing/delegation/rationale and are SURVIVES_AS_IS within the register. |
| `data/doctrine_recheck/recheck_*.yaml` (RC-001, RC-002 second-eyes) | SURVIVES_AS_IS | 2 recheck records | None | A13 baseline data. |
| `data/adversarial_use/catalog.yaml` (v2) | SURVIVES_AS_IS | 1 catalogue file; 9 ACTIVE vectors | A11 counsel review for V-08 | V-08 mitigation language updates pending counsel; catalog version may bump on counsel close. |

### 4.8 Workplan corpus

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| workplan/workplan-co0007-v3.md + amendments | SURVIVES_AS_IS | 2 docs | Amendment 7 close | Operative plan post-2026-04-26. |
| workplan/co0008-scope-infrastructure-overhaul.md | SURVIVES_AS_IS | 1 doc | None | Operative through Stage A; partially absorbed into Stage A schedule. |
| workplan/roadmap-2026-04-27.md | SURVIVES_AS_IS | 1 doc | None | Stage A→B navigation document. |
| workplan/co0007-stage-0_*.md (Stage 0 deliverables) | SURVIVES_AS_IS | 6 docs (0.1 grounding, 0.2 quant, 0.3 skill, 0.4 contamination, 0.5 decisions, 0.7 synthesis re-issue) | None | Verification-gate audit trail; durable. |
| workplan/co0007-synthesis-workplan-2.md (synthesis re-issue) | SURVIVES_AS_IS | 1 doc | None | Authoritative synthesis statement post-Stage-0. |
| workplan/co0007-synthesis-workplan-1.md (original synthesis) | SUPERSEDED | 1 doc | None | Superseded by v2; retain as audit trail per workplan v3 §Salvage matrix. |
| workplan/workplan-co0007-audit-1.md (or earlier) | SUPERSEDED | 1 doc | None | Per workplan v3 supersession. Retain as audit trail. |
| workplan/v10-1-decision-register.md | SUPERSEDED | 1 doc | A12 §5.1 supersession | Replaced by `data/decisions/decision_register.yaml`. Retain as audit trail. |
| workplan/critical-workplan_2026-04-30.md | OPEN | 1 doc | Project-owner adoption | Sonnet's audit-companion path-to-launch. Adoption status pending. |

### 4.9 Session corpus

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| sessions/session_*.md | SURVIVES_AS_IS | 64 session files | None | Project history; durable; auditable record of every session. |
| sessions/LATEST | SURVIVES_AS_IS | 1 pointer file | None | Operational pointer. |

### 4.10 Audits

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| references/audits/methodological-audit_2026-04-30.md (Sonnet) | SURVIVES_AS_IS | 1 doc | None | External audit on the project's own corpus; durable. |
| references/audits/critical-workplan_2026-04-30.md (Sonnet) | SURVIVES_AS_IS | 1 doc | None | Path-to-launch derived from methodological audit. |
| references/audits/process-audit_2026-04-30.md (Opus 4.7, this conversation) | SURVIVES_AS_IS | 1 doc | None | Process audit of past week's work. |
| pre-pivot audit v1 (in `workplan/`) | SUPERSEDED | 1 doc | None | Per workplan v3 supersession. Retain. |
| co0007-audit-2.md | SUPERSEDED-NOT-COMMITTED | 1 doc — never in repo | None | Referenced as Stage 0 input but the upload was released between turns; see session_2026-04-26-co0007-stage0.md note D-01-D. Operationally superseded by workplan v3. |

### 4.11 Bibliography

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| Tier 1–6 verified entries | SURVIVES_AS_IS | 500 of 584 (86%) | None | Citation-verifier passes complete through Tier 4–6 (per Block 13/14). |
| Tier 1 Co-1 entries (verification complete) | SURVIVES_AS_IS | 25 of 25 | None | Per Block 4/5 close. |
| Tier 3 entries — 18 of 20 RESOLVED, 2 UNVERIFIED-CLOSED, 3 CLOSED-DELETED | SURVIVES_AS_IS | 18 RESOLVED entries | None | Per Block 30/32 close; 3 [STRUCK] handled per §4.1. |
| 84 UNVERIFIED-1 residual | OPEN | 84 entries | Project-owner disposition (forward to BPC authors or CLOSED-DELETED per Standing Rule 5) | C7 cleanup. |

### 4.12 Spec database

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| `data/spec_db/*.yaml` jurisdictional value records | SURVIVES_AS_IS | 73 records per A3 Specification entity count | None | Per-spec jurisdictional values. The spec-db was the prototype for the structured-data form B1 will canonicalise. Records cross intact; B1 schema may extend (not retire). |

### 4.13 Gap register

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| `gap_register.md` OPEN entries | SURVIVES_WITH_REDERIVATION | 162 entries (4 P1 / 129 P2 / 29 P3 per current gap register) | Each gap's individual disposition | Gaps are ongoing project-state, not historical artifact. They cross migration with their dispositions intact; new gaps surface through migration. |
| `gap_register_archive.md` CLOSED entries | SURVIVES_AS_IS | (count not pulled) | None | Audit-trail value. |

### 4.14 PI / project-instructions

| Category | Disposition | Scope | Gating | Notes |
|---|---|---|---|---|
| project-instructions text (in claude.ai project) | SURVIVES_WITH_REDERIVATION | 1 text blob | PI sweep per audit R6 | Three stale sections identified (D-01-A `_index.md` omission; D-01-F model identity 4.6→4.7; audit-v2 reference). PI revision is project-owner-owned; the structure survives, the text revises. |
| references/effort-guide.md | SURVIVES_AS_IS | 1 doc | None | Per-skill effort routing; orthogonal to migration. |
| references/project-standards.md | SURVIVES_AS_IS | 1 doc | Periodic recheck per A13 | Append-only RULE log; structure intact. |

---

## 5. Decision rules for SURVIVES_CONDITIONALLY cases

The 78 BPC `best_practice_synthesis` fields are the largest SURVIVES_CONDITIONALLY category. Per-file disposition uses these rules at Stage C migration time:

| Per-file state | Disposition |
|---|---|
| BPC carries `Status: COMPLETE` + Opus synthesis YES + no inline `[UNVERIFIED]`/`[STRUCK]` flags + populations correctly assigned per A7 + Tier coverage adequate per A6 | SURVIVES_WITH_REDERIVATION (synthesis re-authored against post-Stage-A apparatus; underlying findings preserved) |
| BPC self-flags `Status: PROVISIONAL` or `PARTIAL` + jurisdictional coverage <50% + Co-1 absent | SURVIVES_WITH_REDERIVATION + flagged for evidence-density review at migration |
| BPC carries inline `[UNVERIFIED-QUANT]` flag (e.g., economics-cost-premium 47% claim residue) | SURVIVES_WITH_REDERIVATION + claim removal-or-resource decision required first |
| BPC marked `Status: MERGED` (CO-0006 redirect) | SUPERSEDED (redirect target is the substantive entry; retain redirect for git-history reference only) |
| BPC marked `Status: STUB` or `Opus synthesis: NO` with placeholder content | SURVIVES_WITH_REDERIVATION (re-synthesise from underlying research data which is SURVIVES_AS_IS) |
| BPC's underlying research data fails A6 evidence-state machine post-application (e.g., relies entirely on superseded sources) | SUPERSEDED |

These rules are operational at C-stage; they do not require pre-C-stage application. RC-001 + RC-002 already classified 15 of 78 BPCs against an analogous rubric; that classification informs but does not bind C-stage per-file disposition.

---

## 6. Three [STRUCK] claim residue (forward action required)

Per audit R12 and Block 32 close, three claims sit in pre-pivot BPC text as `[STRUCK]` annotations:

1. **Indoor vegetation cognitive benefits** (was Rhee 2023). Affected BPCs: ALL-ENV / biophilic-design / sensory-environment.
2. **Village Landais 31% psychotropic reduction** (was INSERM citation). Affected BPCs: dementia-built-environment-related entries.
3. **Tenji blocks as MOB hazard** (was Kapsalis SR). Affected BPCs: detectable-gradient / wayfinding.

Each requires either re-sourcing (Opus session per Block 32 note) or removal with rationale. See `workplan/struck-claim-research-attempt_2026-05-01.md` (this audit-remediation session's deliverable) for the re-source attempt.

Until each claim has a forward action recorded:

- Treat the BPCs containing `[STRUCK]` markers as SURVIVES_WITH_REDERIVATION + `flag: claim_residue_pending`.
- Block C-stage migration of the affected BPCs until the residue is resolved.

This protects against silent migration of unsourced claims into post-pivot content.

---

## 7. Forward dependencies

This register's classifications change if any of the following land:

| Decision | Affects | Direction |
|---|---|---|
| B1 storage-form selection | All "SURVIVES_AS_IS" mechanical-conversion estimates; potentially upgrades some categories to SURVIVES_WITH_REDERIVATION if B1 changes structural assumptions | Both |
| A4 voice-style disposition | skills/voice-style_SKILL.md (OPEN → terminal) | Resolves OPEN |
| A11 counsel review | data/adversarial_use/catalog.yaml v2 (catalog v2→v3 likely on counsel close) | SURVIVES_AS_IS unchanged; version bump only |
| C7 bibliography UNVERIFIED-1 disposition | 84 sources (OPEN → SURVIVES_AS_IS or SUPERSEDED per disposition) | Resolves OPEN |
| Project-owner placeholder Decision review (R3) | 106 seeded records (SURVIVES_WITH_REDERIVATION → SURVIVES_AS_IS as records receive real values) | Forward |
| Sonnet's `critical-workplan_2026-04-30.md` adoption | workplan/critical-workplan disposition (OPEN → terminal) | Resolves OPEN |
| PI revision per audit R6 | PI text (SURVIVES_WITH_REDERIVATION → SURVIVES_AS_IS post-revision) | Forward |
| Three [STRUCK] claim resolution per §6 | ~5 BPCs containing `[STRUCK]` markers (block lifted; standard SURVIVES_CONDITIONALLY rules apply) | Resolves block |

Each forward dependency carries a hook in this document; when the dependency lands, the corresponding row updates.

---

## 8. Validator hook

Migration-survival classifications are queryable via a future `scripts/validate_migration.py` (not authored in this session; spec follows). Validator checks:

| Check | What it verifies |
|---|---|
| M1 | Every file in the repo maps to exactly one §4 category |
| M2 | No file in §4 SURVIVES_AS_IS contains inline `[UNVERIFIED]` / `[STRUCK]` / `[STUB]` flags |
| M3 | Every OPEN row's gating dependency has not been resolved (else reclassify) |
| M4 | Every SUPERSEDED-but-retained file is reachable from at least one CANONICAL doc as audit trail |
| M5 | C-stage per-file BPC disposition (when run) matches §5 rules |

The validator is not in scope for this audit-remediation session. It is a follow-up if/when migration-survival is adopted CANONICAL.

---

## 9. Cross-stage thread CS-MIG

This document creates a new continuous cross-stage thread:

- **Trigger:** any commit that adds, modifies, or supersedes content in any §4 category.
- **Cadence:** review at each periodic doctrine recheck (per A13 §1.1) + at each stage transition.
- **Owner:** project owner; agent maintains the register on instruction.
- **Pairing:** every supersession event lands a Decision record (D-OP/DG-REVIEW per A12 §2) referencing the affected migration-survival row.

CS-MIG activates on this document's adoption.

---

## 10. What this register does not do

- It does not migrate anything. Stage C does that.
- It does not select B1's storage form. B1 does that.
- It does not resolve the three [STRUCK] claims. The Opus re-source session does that.
- It does not adjudicate the 78 per-file BPC dispositions. Stage C migration does that, using §5 rules.
- It does not pre-empt project-owner decisions on the 106 placeholder Decision records, the C7 UNVERIFIED-1 disposition, or any other OPEN row.

---

## 11. Status

| Field | Value |
|---|---|
| Status | CANONICAL |
| Issued (PROVISIONAL) | 2026-05-01 04:30 (session_2026-05-01-audit-remediation; Opus 4.7 single context) |
| Adopted (CANONICAL) | 2026-05-02 01:37 (session_2026-05-02-audit-remediation-cont; project-owner instruction "perform all") |
| External review | QUEUED (external-review-queue.md EQ-21) — does not block CANONICAL status; pairs with future amendment if review surfaces issues |
| Pairs with Decision | D-0120 (D-DOCT/DG-NON; CANONICAL adoption) — see decision_register.yaml |
| Supersedes | governance/migration-survival.md PROVISIONAL (commit d76471da) |

Adoption converts PROVISIONAL → CANONICAL. Adoption may include amendments to specific rows. Once CANONICAL, this document governs migration-survival classifications until the next periodic recheck or until a stage transition triggers re-evaluation.

---

## 12. Change log

| Date | Change | Commit |
|---|---|---|
| 2026-05-01 | Initial PROVISIONAL draft | d76471da748613f9f227dd1c892f4456c665d99c |
| 2026-05-02 | PROVISIONAL → CANONICAL adoption (project-owner instruction); §2.3 rewritten as adoption note; §11 status block updated; external review queued non-blocking (EQ-21); record-count §4.7 refreshed to current 128 (119 upstream incl. B1-S3 D-0119 + 9 records D-0120..D-0128 from this session) | (this commit) |

---

**End of Migration Survival Register.**
