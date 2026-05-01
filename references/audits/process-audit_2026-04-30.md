# Audit — Past Week of Work (Long-Term Project Health Lens)

**Auditor:** Claude (Opus 4.7) via session protocol bootstrap
**Audit window:** 2026-04-23 00:00 UTC → 2026-04-30 23:59 UTC (7 days)
**Method:** GitHub commit log + 20 session files (full read) + chat sweep (16 conversations) + gap_register filtered for OPEN P1
**Position:** External-to-the-week observer; not the agent that produced any of the work being audited
**Confidence:** Medium-high on commit-level findings (mechanical), medium on session-narrative findings (interpretive), low on doctrinal-correctness findings (depends on prose I haven't read)

This audit is preparatory material for governance decisions, not the decisions themselves. Sonnet's `methodological-audit_2026-04-30.md` and `critical-workplan_2026-04-30.md` (filed 2026-04-30 02:47 / 03:05 UTC) cover doctrinal correctness; this audit covers process health. Findings are scoped to the audit window and read against project-standards / session protocol / Stage A done-criteria. Do not treat this as a substitute for the Sonnet audit on doctrinal questions or for external review by disabled people, OT clinicians, or counsel.

---

## 1. Volume and shape

- **401 commits** in window across 8 unique skill prefixes: multilingual-research (89), jurisdiction-tracker (75), citation-verifier (68), session-consolidator (67), workplan-orchestrator (59), item-specification-writer (10), connection-scout (8), long tail of 12 others (≤5 each).
- **20 session files** committed in window. One giant (block1, 2,368 lines) plus 19 small (43–266 lines).
- **Authorship:** 398/401 commits attributed to `jordanelias`. Three direct Claude commits — two `Claude (Sonnet 4.6)`, one `Claude (Opus 4.7 Adaptive)` — all in `working/mobile-app-prototype-v9/` on 2026-04-30 between 02:47 and 03:12 UTC.
- **Commit cadence:** Highly clustered. By in-message timestamp: 04-23 (115), 04-24 (139), 04-25 (2), 04-26 (29), 04-27 (2), **04-28 (0)**, 04-29 (16), 04-30 (21). Two near-zero days plus one full silent day (04-28). By git push date: 04-24 saw 328 commits — a single batch flush of work authored 04-23/04-24.
- **What got shipped in the week:** Stage A — all 13 governance phases (A1 through A13) closed; Co-1 reframe; CO-0008 infrastructure pour; A3 conceptual model sign-off; A6/A7/A8/A9/A10/A11/A12/A13 governance + schemas + validators; CI integration; RC-001 stage-transition recheck; decision register seeded (106 records); CS1 + CS8 LIVE; 5 parallel commits filed (mobile-app-prototype + methodological audit); 1 deferred commit budget (A12 Sessions 3–4) explicitly flagged.

---

## 2. Strengths (long-term health positive)

These reduce future drift, increase reviewability, or buy optionality.

**S1 — Stage A completion is genuine, not declared.** The 13 governance phases each shipped a CANONICAL governance document plus validator(s). RC-001 ran the 5-pass procedure, found and resolved one cross-reference miss (`pre-stage-a-decisions.md` missing CANONICAL marker), and committed a baseline snapshot. This is harder to fake than the more common pattern of declaring stage closure on prose alone.

**S2 — Doctrinal pivots were captured, not absorbed.** Three foundational corrections happened in-window: (a) the Block 33 architectural pivot from markdown-form to structured-data form (2026-04-24/25); (b) the Co-1 governance reframe (pre-launch solo reality, 2026-04-26 03:45) corrected an inherited false premise about collaborator infrastructure; (c) the advocacy-identity / "shall be" retirement (2026-04-26 20:00) reframed specification language tier-by-tier. All three were committed as RULEs and/or Decisions; none were silently absorbed into other work.

**S3 — CI integration closed the operations/governance gap.** The 2026-04-30 ci-s1 commit added 5 missing validator invocations (validate_temporal, audit_adversarial_use, decision_capture, doctrine_recheck, contamination_sampler) to `.github/workflows/ci.yml`. Until this commit, A9–A13 governance docs all named their validators "CI-integrated" while only A6/A7/A8 were actually wired. The discrepancy was caught and closed in the same week the docs landed. `requirements.txt` pinned (`pydantic==2.13.3`, `PyYAML==6.0.3`) — no more ad-hoc per-job pip installs.

**S4 — Latent A9 bug was caught by A10 and retroactively fixed.** A9's `SupersedenceLink` had been shipping `model_dump(mode="python")` which returned enum instances unparseable by `safe_load`. A10's MisuseVector exposure surfaced the bug 12 hours later; `schemas/base.py` was patched and regression-tested across all five default-bearing schemas. The validator culture caught the latent — not the test data, not a user.

**S5 — Decision register seeded with explicit epistemic disclaimers.** 106 decisions extracted from project-standards RULEs at A12 S2; every record carries `notes: "seeded from project-standards.md §X at A12 Session 2; classification heuristic; review pending"` and placeholder `model_routing: legacy/none/none` rather than fabricated values. The seeding could have papered over its own confidence; it didn't.

**S6 — Parallel work streams didn't collide.** Five non-Stage-A commits landed during A10–A13 (3 mobile-app-prototype, 2 methodological audit). Each Stage A session that ran during this window verified non-conflict before its own commit (e.g., A12 S1 explicitly enumerated the 3 intervening commits and confirmed `schemas/enums.py` SHA unchanged). This is rare engineering hygiene under AI-agent parallelism.

**S7 — Self-auditing happened in-week.** Sonnet committed `methodological-audit_2026-04-30.md` (15 weaknesses ranked) and `critical-workplan_2026-04-30.md` (path-to-launch dependency chain) during the same week the doctrine being audited was being authored. The audit explicitly named its own recursive problem: "a project on accessible design *for* disabled people has, for the duration of this audit, been evaluated *by* a non-disabled (or status-unknown) AI system." Naming this is more valuable than not.

---

## 3. Risks and concerns (ranked by long-term project health weight)

### R1 — `[CRITICAL]` Massive supersession event creates a "kept research, retired form" overhang

Block 33 (2026-04-24/25) declared that the project's then-current form (markdown specifications + Appendix A tables + BPC `best_practice_synthesis` derived from code consensus) is the wrong long-term medium. The synthesis workplan reframes ~280+ prior commits as input data, not deliverables to patch. Stage C migration is budgeted at 140–200 sessions / 12–18 months.

**Why this matters for long-term health.** A pivot of this scale is the right call once the corpus contamination diagnosis was accepted, but it creates three durable risks: (a) the kept-research / retired-form boundary lives only in the synthesis workplan and a few session notes — not in a single canonical "what survives migration" register; (b) future contributors (or future Claude sessions) may not realise that a guidance value extracted from a retired BPC `best_practice_synthesis` is now suspect; (c) the migration estimate is an Opus session's best guess at a moment of high context — there is no second-source check on it.

**Mitigation already in place.** A6 evidence-state machine; A7 population taxonomy; advocacy-identity rule; tier-appropriate specification language. These reduce the risk of new content reproducing the contamination pattern.

**Mitigation gap.** No single document at `governance/migration-survival.md` (or similar) enumerating what from the pre-pivot corpus migrates as-is, what migrates with re-derivation, what is retired. Stage C will produce this incrementally but the register itself should exist before Stage C starts.

### R2 — `[HIGH]` First-of-kind doctrine recheck violated its own fresh-context principle

A13 §4.2 specifies that periodic rechecks run in fresh context to mitigate long-context drift. RC-001 (the first recheck, run as Stage A→B transition recheck) was performed by the same Opus session that landed A10/A11/A12-S1/A13/A12-S2. The session's own `Note on the recheck reviewer` acknowledges the partial violation and offers mitigations (mechanical passes 2.2–2.5 are context-insensitive; sample selection is deterministic-stratified; classification rationale is recorded so future rechecks can audit).

**Why this matters.** The principle exists because a session that just authored doctrine is the worst auditor of that doctrine — it has the rationale present, can rationalise weaknesses, and has narrative attachment to the choices. The "Material CLEAN drift (78% → 60%) — methodologically virtuous, not contamination" finding is exactly the kind of judgment most vulnerable to context bias. It may be correct. It is also the conclusion the authoring context most wants to be true.

**Recommendation.** Re-run RC-001 in genuinely fresh context (different conversation, different Opus session) before treating its baseline as canonical for Stage B drift detection. Do not skip this on the rationale that "the mechanical passes don't change" — the §3.2 four-state classification on the 15-sample contamination set is the classification the next stage drifts against.

### R3 — `[HIGH]` Decision register's 106 placeholders are an unrecorded promise to do work later

Every seeded record carries placeholder `model_routing: "legacy/none/none"`, conservative `delegation: "DG-NON"`, and `decided_by: "solo_author_pre_launch"`. They are operative as-seeded but require individual review (estimated 0.5–1 working session per A12 S2 close, more realistically 1–2 per ~50 records given attention drift). Three carry C3 short-rationale warnings; one carries a C6 outcome-as-rationale warning.

**Why this matters.** Project-standards now operationally points to `data/decisions/decision_register.yaml` for queryable doctrinal history. A future agent doing a "read-the-rationale-to-understand-why-this-is-the-way-it-is" lookup (the §6 discriminator) on a placeholder record gets `notes: "seeded from project-standards.md §X; classification heuristic; review pending"` — accurate but a gap.

**The gap is bounded if it ships before launch.** It becomes a long-term liability if launch ships with most records still placeholder.

### R4 — `[HIGH]` A10–A13 governance corpus written in single Opus context

Per the rc001 session note, "the recheck reviewer in this run is the same Opus session that landed A10–A13 in this conversation." A10 (adversarial-use), A11 (legal-regulatory), A12 S1 (decision-protocol), A13 (doctrine-recheck), A12 S2 (seeding + consolidator wiring) were all produced in one conversation. Total governance volume: roughly 60K+ chars of CANONICAL doctrine plus four schema files plus three new validator scripts plus the V-08 catalog cross-update.

**Why this matters.** A13 itself codifies "fresh-context decision-checking" as a B-06 mitigation precisely because long-context drift is a known pattern. The four phases that doctrinated the principle were authored without it. The tight integration is also why A10–A13 are so cleanly cross-referenced — the same context that produced one produced the others. That's a feature for cross-reference correctness and a risk for blind-spot correlation.

**Recommendation.** Treat A10–A13 governance docs as a single doctrinal block for review purposes. External review (Sonnet's E1, project-owner read, or counsel where applicable) reviewing them as one unit will catch correlated weaknesses that piece-by-piece review will not.

### R5 — `[HIGH]` Co-1 governance reframe surfaced a foundational premise error that the audit-and-resolution chain could not catch

On 2026-04-26 03:45 the project owner surfaced that Stage 0 deliverables (mission, pre-Stage-A decisions, workplan v3, v3 amendments) had been drafted on a false premise: Co-1 collaborator operational structure (DPO partnerships, collaborator panels, recruitment thread, compensation infrastructure) did not exist. The audit v2 document had diagnosed a "doctrine-vs-operations gap" on Co-1, and the Stage 0.5 resolution had tried to bridge it with operational triggers — both presupposed an operational structure to evaluate.

**Why this matters for long-term health.** The pattern named in the co0007-a1a2-i12 session — "audits can inherit and amplify a wrong premise rather than catch it" — is a structural limit on auditor-driven self-correction. The mitigation in this case was project-owner direct correction. There is no analogous mitigation when the project owner is mid-context, distracted, or absent.

**This means.** External-to-the-project review (Sonnet's E1, counsel, disabled people, OT clinicians) is not a "should-have" for credibility — it is the only structural correction available for premise-level errors. The methodological audit names this correctly.

### R6 — `[MEDIUM]` PI staleness pattern, three independent surfacings in window

(a) Start-protocol omits `references/connections/_index.md` that workplan-orchestrator skill mandates. (b) Model identity references "Sonnet 4.6 / Opus 4.6"; live model is 4.7. (c) Audit v2 referenced as input to Stage 0 but never committed to repo (turn-1 upload released between turns; never re-uploaded).

**Why this matters.** Each is individually small. The pattern is the issue: the project-instructions document evolves on a slower cadence than skill files and live infrastructure, and stale PI sections accumulate. Standing Rule notes "PI text governs where PI and skill file conflict" but the architecture already inverts this for the start-protocol section because the skill file was newer. The current PI is therefore already partially superseded by its own file architecture.

**Mitigation gap.** No PI-staleness sweep in the audit window. Each surfacing was logged to a session reconciliation table; none triggered a PI revision Change Order.

### R7 — `[MEDIUM]` Commit convention compliance ~81%

77/401 commits (19%) lack the required `[YYYY-MM-DD HH:MM]` timestamp suffix per PI commit convention. Most failures are jurisdiction-tracker `add jurisdiction_coverage [SLUG]` commits where the bracketed token holds a slug name not a timestamp; two outlier commits use a malformed `[2026-04-24 07:12M]` (the trailing `M` is unexplained). Tag-day-vs-git-day mismatch on 118/324 tagged commits (36%) — substantial deferred-push behaviour, mostly the 04-24 batch flush of 04-23 work.

**Why this matters.** Commit messages are now load-bearing — the in-message timestamp is the only easy way to reconstruct work cadence post-hoc when push dates batch (04-24 had 328 commits with timestamps spanning 04-23 06:00 through 04-24 09:15). 19% non-compliance plus malformed-tag outliers makes auditability meaningfully worse.

**Mitigation.** Pre-commit hook validating the regex pattern, or an `audit_commits.py` utility run periodically. Currently neither exists.

### R8 — `[MEDIUM]` OPEN P1 gaps unchanged through the week

`gap_register.md` shows 2 OPEN-PARTIAL P1 items at end of window: GAP-079 (Part 7/8 GRADE ratings deferred to Phase B; ~125 specs unaligned) and GAP-CITE-01 (citation tagging Step 2; 1,382 claims to populate ref_ids; Part 4 Cat A 45 TAGGED, 17 DEFERRED in Session 1 only). Both standing-decision deferred. Both touch the corpus that Block 33 reframed as input data.

**Why this matters.** The two P1 gaps are exactly the work that the Stage C migration would consume. Letting them sit OPEN through the Stage A authoring period is correct (they're not blocking governance work). But they are not making progress either, and their priority designation (P1) implies the project committed to closing them — that commitment now sits in a stage that is 12–18 months out.

**Recommendation.** Decide whether GAP-079 and GAP-CITE-01 stay P1 or get reclassified. P1 = "critical" in the schema header; sitting in a deferred stage for 12+ months is in tension with that.

### R9 — `[MEDIUM]` Five P2 jurisdictional research gaps (LRP-06–LRP-10) untouched in week

GAP-LRP-06 through GAP-LRP-10: Global South jurisdiction expansion for 5 BPC slugs (threshold-door-hardware, pain-ofs, acoustics, dementia, intellectual-disability). New jurisdictions named: IN, EG, ZA, MA, NG, MX, CO, CL, PE, KE, ID, PH. Phase 3-A through 3-E. OPEN since 2026-04-05. No commits touching these gaps in the audit window.

**Why this matters.** These gaps explicitly extend coverage into populations and regions the project's mission says it serves. They are the kind of work that, if left to the migration phase 12–18 months out, will likely be cut on scope-management grounds. The longer they sit OPEN P2, the more they look like they will be reclassified P3 or CLOSED-DELETED rather than executed.

### R10 — `[MEDIUM]` 04-28 silent day in a high-cadence week

Zero commits on 2026-04-28. 04-25 and 04-27 each show 1–2 commits. In a week of intense governance authoring (A6 → A13 in 36 hours of 04-29/04-30 wall-clock), the 04-28 silence is conspicuous. Read against the rc001 session's own concern about long-context risk, it is plausible that 04-28 was a context-reset day. There is no session file documenting the gap.

**Why this matters.** Not a problem on its own. Becomes a problem if the gap represents work done off-system that didn't make it back to the repo, or if it represents context fatigue that affected subsequent sessions. Neither is currently visible. Worth project-owner reflection rather than instrumentation.

### R11 — `[MEDIUM]` Adversarial-use validator declares its own structural blindness

A10's `audit_adversarial_use.py` is explicit: "The validator does not perform automated content scanning for misuse patterns. Most adversarial-use vectors are not mechanically detectable in prose. Pretending otherwise would create a false-confidence failure mode. The release gate is a structured human-judgment exercise; this script confirms the review has occurred and is well-recorded." Pre-launch reviewer is `solo_author_pre_launch`.

**Why this matters.** The honesty is right. The structural gap remains: a single solo reviewer pre-launch reviewing for nine misuse vectors (V-01 through V-09) — including HIGH-severity vectors V-01 minimum-compliance weaponization, V-02 exclusionary ROI, V-03 surveillance, V-05 Co-1 instrumentalization, V-08 adversarial litigation citation — is the maximum possible self-review and the minimum useful adversarial-use review. Sonnet's methodological audit reaches a similar conclusion via the recursive-problem framing.

**Recommendation.** Adversarial-use review is one of the items on Sonnet's `E1` external-review list and should be treated as not-launchable-without-it, not as a pre-launch checkbox.

### R12 — `[LOW]` Three [STRUCK] claims sit in BPC files as unsourced

Block 32 (2026-04-24 09:15) struck three Tier 3 claims as CLOSED-DELETED across 8 files: indoor vegetation cognitive benefits (Rhee 2023), Village Landais 31% psychotropic reduction (INSERM), tenji blocks as MOB hazard (Kapsalis SR). The struck markers are present; the underlying claims remain in BPC content as `[STRUCK]` annotations awaiting Opus re-sourcing.

**Why this matters.** A future content-render of these BPCs would either ship the claim with `[STRUCK]` visible (incorrect for a published guidebook) or have to silently drop the claim (loss of substance without record of why). The three claims need either re-sourcing or removal-with-rationale before any rendering.

### R13 — `[LOW]` "Claude (Opus 4.7 Adaptive)" author attribution is non-standard

One commit (`1df7bcef19`, 2026-04-30 03:12 UTC) attributed to `Claude (Opus 4.7 Adaptive)`. The "Adaptive" suffix is non-standard Anthropic model nomenclature. Two other Claude commits the same day attributed to `Claude (Sonnet 4.6)` — this is the project's expected Claude-attribution convention. The Adaptive variant either represents a custom git config on the project owner's side or a model identity confusion that propagated into commit metadata.

**Why this matters.** Minor by itself. Becomes a problem if the attribution string is parsed by any validator or skill (it would not match the model_routing regex enforced at A12). Worth disambiguating once.

### R14 — `[LOW]` Fresh-context principle applied unevenly across the week

Stage A→B fresh context recommended (A13 §4.2) but RC-001 recheck violated it. CO-0007 Stage 0 → Stage A boundary explicitly observed. A12 S2 deliberately ordered after A13 (against numerical sequence) "because A13 closes Stage A, and running it before A12 S2 surfaces real validator coverage data at A12 S2." The latter is reasonable; the inversion was logged.

The principle is treated as soft when convenient. If it is binding (per A13 §1.2 STAGE_TRANSITION trigger), it should bind RC-001. If it is advisory, the governance text should say so.

### R15 — `[LOW]` Working-session counter initialised from 0 with no session-count reconstruction

A12 S2 initialised `data/doctrine_recheck/working_session_counter.yaml` at 0, with explicit non-reconstruction of pre-A12-S2 session count. The first periodic recheck triggers at counter=25.

**Why this matters.** The 25-session cadence was set knowing the pre-A12-S2 session count was non-trivial. Resetting to 0 means the *first* periodic recheck will run after 25 working sessions of *post-Stage-A* work — almost certainly during Stage B. The project absorbed an implicit "no periodic recheck during Stage B Phase 1" decision when the counter reset. Worth confirming this was the intended behaviour.

---

## 4. Process compliance

| Rule | Status | Notes |
|---|---|---|
| Standing Rule 1 (≤500 lines per input) | ✅ enforced | Block1 chunked to handle |
| Standing Rule 2 (UTC timestamps via `date -u`) | ⚠ partial | 19% commits lack timestamp suffix |
| Standing Rule 3 (.md default; DOCX only on request) | ✅ enforced | All deliverables .md or .yaml |
| Standing Rule 4 (research-log-manager CHECK before research) | ⚠ untested | Most sessions `research_log_updated: false` (no research run); skill discipline not exercised |
| Standing Rule 5 (sources real; "I don't know" > invention; 2-fail → DELETED) | ✅ visible | 3 [STRUCK] claims executed per protocol; Tier 3 verification complete |
| Standing Rule 6 (Sonnet never determines best practice) | ⚠ ambiguous | Sonnet `methodological-audit` is methodological audit, not best-practice synthesis — borderline; Sonnet 4.6 produced doctrine-adjacent assessments |
| Standing Rule 7 (toc-editor before structural changes) | n/a | No structural-restructure session in window |
| Standing Rule 8 (connectors only when research-required) | ✅ enforced | A1-A2 iter 3 used PubMed for citation closure; otherwise dormant |
| Standing Rule 10 (quality > completion; handoff over rush) | ✅ enforced | A8 close at ~74% context; ci-s1 close after declining to invent low-grade work |
| PI start-protocol (1a/1b/2/3/4) | ✅ enforced | All 16 sampled chats opened with batch_read of LATEST + standards + orchestrator |
| Effort-guide adherence | not audited | Would require reading `references/effort-guide.md` per phase |

---

## 5. Recommendations — ordered by leverage

1. **Re-run RC-001 in genuinely fresh context** before treating the 60/20/13/7 baseline as canonical. (R2)
2. **Decide on the 106 placeholder Decision records** — schedule the rationale-review work, or accept that they ship as-seeded and document that. (R3)
3. **Treat A10–A13 governance corpus as one block for external review** rather than four. (R4)
4. **Author `governance/migration-survival.md`** before Stage B Phase 1 lands a storage form — register what survives, what re-derives, what retires. (R1)
5. **Add commit-message validator script** invoked by CI or pre-commit. (R7)
6. **Decide whether GAP-079 and GAP-CITE-01 stay P1** or get reclassified given their Stage C dependency. (R8)
7. **Sweep PI for staleness** (`_index.md` start-protocol omission; model identity 4.6 → 4.7; audit-v2 reference). One Change Order per PI revision. (R6)
8. **Resolve the three [STRUCK] BPC claims** before any rendering work begins (re-source or remove-with-rationale). (R12)
9. **Confirm working-session counter reset to 0 was intentional** — the first periodic recheck now lands deep in Stage B. (R15)
10. **Treat external review (E1 in Sonnet's critical workplan) as gating, not optional.** (R5, R11)

---

## 6. What this audit could not determine

- Whether the doctrine in A6–A13 is *correct* (vs internally consistent and well-implemented). Would require disability-studies / OT / counsel review.
- Whether the migration estimate (180–262 sessions, 12–18 months) is realistic. Depends on Stage B scope decisions not yet made.
- Whether the project owner has bandwidth for the placeholder-rationale review, the counsel engagement, the external-review thread, and Stage B Phase 1 simultaneously.
- Whether the CC BY-SA 4.0 + decline-pursuit posture is the right strategic choice. Out of scope.

These are project-owner decisions and external-review work, not audit findings.

---

## 7. Sign-off

This audit reads the past week as: **Stage A authentically complete, infrastructure honest, key pivots well-captured, decision register seeded with epistemic discipline, but the four R1–R4 risks (supersession overhang, recheck context-violation, placeholder records, single-context governance authoring) compound rather than cancel.** The risks are all addressable; none requires unwinding work already done. The leverage point for the next week is whichever fresh-context recommendation gets executed first.

Conflicts with Sonnet's methodological audit: none material — that audit covers doctrinal correctness; this covers process. Where overlap exists (recursive-problem / E1 external review), conclusions agree.

---

**End of audit.**
