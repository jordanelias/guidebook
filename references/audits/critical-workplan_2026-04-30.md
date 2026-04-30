# Critical Workplan — Path to Launch

**Companion to:** `references/audits/methodological-audit_2026-04-30.md`
**Author:** Claude (Sonnet 4.6 / interface-resolved)
**Date generated:** 2026-04-30 03:05 UTC

This workplan converts the methodological audit's findings (15 weaknesses ranked by ethical/epistemic weight) and the non-undermining fixes (one fix per weakness, traced to existing project doctrine) into a sequenced critical path to launch.

It distinguishes:
- the dependency chain that **gates** launch (cannot be skipped);
- items that can be **deferred** to post-launch without credibility cost;
- items that are **tempting to cut** but should not be;
- items that **cannot be closed** before launch and must be honestly handled instead.

Confidence: medium-high on sequencing logic; medium on session-count estimates; lower on external-response timelines.

---

## 1. Critical path

The dependency chain that gates launch.

```
G1 (path-to-impact) ──┬─→ W1 (Part 1 prose: reader address)
                      ├─→ W3 (Tier 2 visibility audit) ──→ Part 4 corrections
                      └─→ S1 (niche-depth framing in Core Doctrine)
                                                          │
W4 (artifact accessibility commitments) ──→ rendering/format work ──┤
                                                                    │
W5 (GRADE retrofit) ──┐                                             ├─→ LAUNCH
W6 (citation tagging) ─┴─→ CI green, validators pass ───────────────┤
                                                                    │
W7 (hallucination audit v2) ────────────────────────────────────────┤
                                                                    │
E1 (external methodology review) ───────────────────────────────────┘
```

**G1 is the single point of failure.** Without it, every subsequent decision is implicit. With it, decisions sort cleanly into depth-serving, reach-serving, and ethics-serving buckets.

**W5 + W6 are the longest mechanical work on the path** — ~125 GRADE specs and ~918 pending citation tags. They are parallelisable but high-volume.

**E1 (external review) can run in parallel** to W1–W7 but takes external response time the auditor cannot estimate. Start at Phase B opening.

---

## 2. Phased sequence

### 2.1 Phase A-residual

Stage A completion plus the new strategic phases needed to prevent A11–A13 from operating without strategic frame. Solo-author session estimates assume the rapid pace evident in A4–A8 close on 2026-04-29.

| Phase | Content | Sessions | Notes |
|---|---|---|---|
| **A9** | Time model (existing schedule). validate_temporal.py, version_retrofit.py. | 1–2 | Already next_action from prior session. |
| **A10** | Path-to-Impact governance (new). G1 + S1. Theory of change; niche-depth strategic framing. | 1 | Highest leverage. Without this, A11–A13 are arbitrary. |
| **A11** | Participatory-Limit governance (new). G2 stakeholder map + S2 operational handling of Co-1 participation gap (per-population sub-cohort coverage tracking; first-call commitment language; feedback channel design). | 1–2 | Reuses 2026-04-26 honesty rule infrastructure. |
| **A12** | Decision protocol (existing schedule). decision_capture.py. Fold G3 (Sen capability), G4 (ICF critique), G5 (disability justice engagement) as paragraph-level decisions captured under the new protocol. | 1–2 | Bundles three doctrinal-engagement items because they share treatment pattern. |
| **A13** | Doctrine recheck (existing schedule). doctrine_recheck.py, contamination_sampler.py. Fold G6 (Tier 2 geographic), G7 (IntD reframing), G8 (license/citation/DOI), W4 (artifact accessibility commitments) as governance commitments validated by the recheck. | 2–3 | Heavier than original scope because of folded items, but the recheck pass naturally surfaces them. |

**Phase A-residual total:** 6–10 sessions.

**Parallel rigour-debt closure during every Phase A session:** 30 min retrofit slot — 5–10 GRADE specs *or* citation-tagging chunk. Reduces W5/W6 backlog without dedicated mechanical sessions. Over 6–10 sessions: 30–100 specs / 50–500 tags closed in parallel with governance work.

### 2.2 Phase B

Writing, content, and rigour-debt closure.

| Workstream | Content | Sessions | Parallelism |
|---|---|---|---|
| **B-prose** | W1 disabled reader address; G3/G4/G5 paragraphs in Part 1; G6/G7 prose passes; S1 Core Doctrine reframe. | 4–6 | Single workstream — voice consistency demands sequential authorship. |
| **B-tier2** | W3 Tier 2 visibility audit + Part 4 prose corrections; voice-style §8.4 calibration test addition. | 3–5 | Parallel to B-prose if voice-style skill changes are committed first. |
| **B-grade** | W5 GRADE retrofit completion (Part 7/8 matrices + remaining specs). | 8–12 | Mechanical; high parallelism; chunk per-Part. |
| **B-citation** | W6 citation tagging completion to ≥95%; ORPHANED to zero. | 6–10 | Mechanical; parallel to B-grade. |
| **B-capability** | W2 capability-organised cross-cut (Appendix E or separate digest). | 4–6 | New deliverable, not a fix. Lower priority — see cut analysis §3. |

**Phase B total:** 25–39 sessions if all workstreams completed; 15–22 sessions if W2 capability cross-cut is deferred to post-launch.

### 2.3 Pre-launch external — parallel to Phase B from start

External work cannot be timeboxed reliably. Start at Phase B opening; do not gate launch on full responsiveness, only on having attempted and documented.

| Item | Lead time | Notes |
|---|---|---|
| **E1** methodology review (2–3 reviewers OR journal submission) | 4–12 weeks | Outreach starts Phase B start. Single review pass; document responses. Journal route doubles as publication. |
| **E2** DPO outreach (2–3 DPOs, single-pass review) | 4–8 weeks | Targets: intellectual-disability self-advocacy (Inclusion International or local affiliate), Deaf cultural representation (WFD or national affiliate), Global South DPO (partner of UN-Habitat or IDA). |
| **E3** workflow-integration scoping | 2–4 weeks | Identify 2–3 BIM library / OT clinical-reference / code-commentary projects. No build commitment. |

### 2.4 Pre-launch checks

| Check | Owner | Trigger |
|---|---|---|
| All CI validators green | Mechanical | Every commit |
| GRADE applied to 100% of Tier 1 specifications | Audit | Pre-launch gate |
| Citation tagging ≥95%; ORPHANED count = 0 | Audit | Pre-launch gate |
| W7 hallucination audit v2 (qualitative claim attribution sample) | Single session | Pre-launch gate |
| Artifact accessibility verification on rendered output (screen-reader test, alt-text presence, plain-language version available) | Manual + tooling | Pre-launch gate |
| External review responses logged (not necessarily incorporated) | Manual | Pre-launch gate |

### 2.5 Launch artifact

Depth corpus + plain-language summary + audio of Part 1 + Easy Read summary of key principles + WCAG 2.2 AA conformant web rendering + DOI + license. English only at launch; translation roadmap stated.

### 2.6 Post-launch

| Item | Trigger |
|---|---|
| **Revision cadence** (per G8) | Quarterly minor / annual major / 24-month evidence-review pass. |
| **Co-1 collaboration outreach** | If resources materialise per 2026-04-26 rule. |
| **W2 capability cross-cut** (if deferred) | Phase 2 deliverable, 6–12 months post-launch. |
| **Sub-community Co-1 stratification** (per audit §3.2.2 fix) | Continuous; tracked in `gap_register` `subcommunity_coverage_gap`. |
| **Translation rollout** | Per priority-language schedule. |
| **Workflow integrations** | If E3 surfaces willing partners. |

---

## 3. Cut analysis

### 3.1 What can be cut without launch impact

**W2 capability-organised cross-cut.** New deliverable, not a fix. Closes a real capability-approach gap (audit §3.4) but not on the credibility-critical path. Defer to post-launch. If launch slips to accommodate it, that is the wrong trade.

**E3 workflow-integration scoping.** Outreach without build commitment. If no partners surface, launch unaffected. Defer outreach to post-launch if Phase B capacity is constrained.

**G8 partial — translation roadmap.** Stating a roadmap is required pre-launch (artifact accessibility commitment); executing it is not. Multi-language launch is a different project.

**Some sub-items in W4 artifact-accessibility.** Audio of Part 1 yes; full audio corpus no. Easy Read summary of principles yes; Easy Read of full corpus no. Braille policy statement yes; braille production no. Tier the AA commitment honestly.

### 3.2 What cannot be cut

The four launch gates (G1, W4 commitments, W5+W6, W7) and reader address (W1) are non-negotiable for credibility.

### 3.3 What might be tempting to cut but shouldn't

**E1 external methodology review.** Temptation: launch faster without it. Cost: leaves the project's largest credibility gap (audit §3.2.14) standing. Even one reviewer's documented input is structurally stronger than zero.

**Disability justice engagement (G5).** Temptation: "we cite enough frameworks already." Cost: omission signals which critique the project is unwilling to face.

**Disabled reader address (W1).** Temptation: "the document already serves disabled people." Cost: whether it does is the entire question. One paragraph in Part 1 is the lightest possible structural correction.

---

## 4. Hard launch gates

Non-negotiable preconditions. No launch until all six are green.

1. **Path-to-impact stated.** G1 + S1 in Core Doctrine.
2. **Artifact accessibility verified.** WCAG 2.2 AA conformance on rendered output; plain-language summary available; audio of Part 1 produced; Easy Read summary of key principles produced.
3. **GRADE 100% on Tier 1 specifications.** No Tier 1 spec without a GRADE rating.
4. **Citation tagging ≥95%; ORPHANED = 0.** No untraceable claims at launch.
5. **Hallucination audit v2 complete** with documented error rate and (if >5%) expanded audit on that vector.
6. **External review attempted and logged.** Not "incorporated" — attempted and documented. Refusing to attempt is the failure; non-response from reviewers is acceptable.

---

## 5. What cannot be done before launch

Honestly named. The project owner decides whether these block launch. The audit's recommendation: handle, do not delay launch.

**Closing the Co-1 participation gap (audit §3.2.1).** Solo authorship cannot be made participatory by writing. The 2026-04-26 honesty rule is the project's handling. Launch with the gap acknowledged in front matter; flag as standing limitation; commit to first-call collaboration if resources arrive.

**Full sub-community Co-1 stratification (audit §3.2.2).** Depends on review by sub-community-led organisations that may not be reachable pre-launch. Launch with `subcommunity_coverage_gap` flags in BPC metadata; commit to closure as ongoing work.

**Tier 2 alternative mechanism for Global South (audit §3.2.6).** The project does not prescribe substitutes for OT-led Tier 2. Launch with the limit named; refuse the temptation to invent a substitute the auditor and project owner are not positioned to specify.

**Mass-architectural reach (audit §3.2.15).** The artifact serves depth, not mass-design-moment use. Launch refusing the population-scale claim. Mass reach is post-launch via influence vectors.

---

## 6. Risk register

Top 5 risks ranked by likelihood × impact.

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | **Phase B capacity insufficient for parallel rigour-debt + writing.** Solo-author bandwidth caps; one workstream dominates. | High | High | Sequence rigour-debt closure (B-grade, B-citation) ahead of new content (W2). Run mechanical work in parallel sessions. Use 30-min retrofit during Phase A-residual to reduce backlog. |
| 2 | **Tier 2 visibility audit reveals widespread prose failure.** W3 finds many specifications without vivid Tier 2 handoff. Correction is large. | Medium | High | Run W3 audit early in Phase B. If failure rate >30%, scope dedicated correction phase rather than retrofitting per-spec. |
| 3 | **Hallucination audit v2 finds qualitative-claim attribution errors.** W7 reveals a different failure pattern than the 2026-04-09 quantified-claim audit. | Medium | High | Bound first audit to 20 claims. If error rate >5%, expand to full sample on that vector. Flag findings; correct before launch. |
| 4 | **Artifact accessibility commitments cannot be fully delivered solo.** Audio production, Easy Read authoring require external skills/budget. | High | Medium | Tier commitments at G8: state intent, deliver minimum (Part 1 audio, Easy Read of principles), roadmap rest. Honest tiering protects against over-promise. |
| 5 | **External reviewers don't respond in time.** E1/E2 outreach fails to produce reviewers within Phase B window. | Medium | Medium | Start outreach at Phase B opening (4–12 weeks lead). Accept non-response as outcome; document attempts. Journal submission as alternative gate. |

---

## 7. What to do this week

If work resumes immediately:

1. **Open A10 (Path-to-Impact).** Single-session governance phase. Output: governance doc + RULE in project-standards + S1 reframe of Core Doctrine. Without this, A11+ are arbitrary.
2. **Begin E1 outreach.** Identify and contact 2–3 candidate methodology reviewers. Or draft a methodology paper for journal submission. Lead time is the constraint.
3. **Begin E2 outreach.** Identify and contact 2–3 candidate DPO reviewers. Same logic.

These three actions in week 1 unlock everything else. A10 sets the strategic frame; E1/E2 start the longest-lead-time external dependencies.

---

## 8. Cross-references to audit

Each plan item maps to one or more audit findings. The cross-reference is the traceability that prevents this workplan from accumulating items beyond what the audit warrants.

| Plan item | Audit finding | Section |
|---|---|---|
| G1 | 3.2.15 Path-to-impact | §5.1 |
| G2 | §3.3 stakeholder set | §5.1 |
| G3 | 3.2.4 Capability version | §5.1 |
| G4 | 3.2.3 ICF critique | §5.1 |
| G5 | 3.2.5 Disability justice | §5.1 |
| G6 | 3.2.6 Tier 2 geographic | §5.1 |
| G7 | 3.2.7 IntD reframing | §5.1 |
| G8 | 3.2.13, sustained-artifact concerns in §3.4 | §5.1 |
| W1 | 3.2.8 Disabled reader address | §5.2 |
| W2 | §3.4 capability-organised cross-cut | §5.2 |
| W3 | 3.2.10 Tier 2 visibility | §5.2 |
| W4 | 3.2.13 Artifact accessibility | §5.2 |
| W5 | 3.2.11 GRADE retrofit | §5.2 |
| W6 | 3.2.11 Citation tagging | §5.2 |
| W7 | 3.2.12 Hallucination audit scope | §5.2 |
| E1 | 3.2.14 External ethics gate | §5.3 |
| E2 | 3.2.1 Co-1 participation gap (partial) | §5.3 |
| E3 | §5 practical considerations / workflow integration | §5.3 |
| S1 | 3.2.15 Niche-depth framing | §5.4 |
| S2 | 3.2.1 Solo-author Co-1 gap as standing limitation | §5.4 |

---

*End of document. Sequencing is preparatory; phasing decisions belong to the project owner.*
