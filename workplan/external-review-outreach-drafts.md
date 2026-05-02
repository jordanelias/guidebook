# External Review — Outreach Drafts

**Status:** Application-ready artifact (companion to workplan/external-review-queue.md)
**Authoring:** Opus 4.7 audit-remediation-cont session 2026-05-02
**Audit basis:** audit_2026-04-30 R10 + R11 + D-0127 (this issuance)
**Application:** project owner reviews wording, fills in reviewer details, sends
**Purpose:** Reduce external-review commissioning from a research-and-draft task to a one-click send

---

## How to use this document

Each section below is a paste-ready outreach email for one reviewer batch. The drafts are templates — review wording, fill in `[BRACKETED PLACEHOLDERS]`, send via your normal email or correspondence channel.

The six batches map to the reviewer-type clusters in `workplan/external-review-queue.md` §3:

1. **Counsel batch** — disability-law counsel for V-08 + L-Q1/L-Q2/L-Q7/L-Q8 (5 items)
2. **Disability-studies batch** — V-01/V-02/V-03/V-05 + EQ-21 (5 items)
3. **Methodology reviewer (Sonnet E1)** — V-04/V-06 + EQ-18/EQ-19 + EQ-21 method review
4. **DPO / Co-1 outreach (Sonnet E2)** — DPO partner review
5. **Workflow-integration scoping (Sonnet E3)** — non-gating scoping conversations
6. **Migration-survival register external review (EQ-21)** — disability-studies + methodology reviewer cross-cut

Estimated reviewer load per batch is in `workplan/external-review-queue.md` §3.

---

## Batch 1 — Disability-law counsel

**Subject:** Request for legal review — accessibility guidebook governance documents (5 items, ~4–6 hour engagement)

**To:** `[COUNSEL_NAME]` (`[COUNSEL_FIRM]`)

---

Dear `[COUNSEL_NAME]`,

I am the author of an in-development guidebook on accessible built-environment design (`jordanelias/guidebook` on GitHub; pre-launch, solo authorship). I am writing to ask whether you would be available for a focused legal review of five governance items that are flagged as gating on counsel sign-off before the guidebook can be published.

The five items concern (a) negligent-misrepresentation exposure for the project's specification language, (b) fitness-for-purpose disclaimers, (c) jurisdictional disclaimer scope, (d) litigation-defense provisional language, and (e) an adversarial-use scenario where guidebook content might be cited in litigation against disabled people. Each item is documented in two files:

- `governance/legal-regulatory.md` §6.2 (legal questions L-Q1 through L-Q8)
- `governance/adversarial-use-framework.md` (vector V-08 — adversarial litigation citation)

Both files are public on the repo. Total page count for the legal-bearing material is ~50 pages. The questions are bounded — you don't need to review the underlying technical specifications, only the framing language and disclaimer architecture.

**Estimated engagement:** 4–6 hours of review + 1–2 hours of written response or videoconference.

**My ask:** Either a written letter addressing the five questions, or a 1-hour videoconference where I can talk through your assessment and we can agree on revision language. I will accept "the framing is fine; no revisions needed" as a valid output if that is your conclusion.

**Compensation:** I am a solo pre-launch author; the project does not yet have a budget. I can offer (a) acknowledgment in the published guidebook, (b) modest hourly compensation if your normal rate allows that, or (c) a pro bono engagement if your firm's policies support that. Happy to discuss.

**Timeline:** No fixed deadline; the guidebook publishes when it publishes. Counsel review is the binding gate, so I am pacing the rest of the work to whatever timeline works for you.

If this is not a fit for your practice, I would also welcome a referral to a disability-law colleague who handles built-environment / construction-document liability questions.

Thank you for considering this.

`[USER_NAME]`
`[USER_EMAIL]`
`[USER_PHONE_OR_AVAILABILITY]`

GitHub: github.com/jordanelias/guidebook

---

## Batch 2 — Disability studies / disability-rights advocacy

**Subject:** Request for review — adversarial-use framework for accessibility guidebook (4 items + 1 register, ~6–8 hour engagement)

**To:** `[REVIEWER_NAME]` (`[INSTITUTION]`)

---

Dear `[REVIEWER_NAME]`,

I came across your work on `[SPECIFIC_CITATION_OR_BOOK_OR_ARTICLE]` and am writing to ask whether you would consider reviewing material from a guidebook on accessible built-environment design that I am developing pre-launch.

The specific items I am asking about are not the technical specifications themselves — those have separate methodology and counsel review tracks. I'm asking about the **adversarial-use framework**: a register of ways the guidebook could be misused against disabled people, with corresponding mitigations. Five vectors in the catalogue need disability-studies or disability-rights review:

1. **V-01 Minimum-compliance weaponization** — risk that "best practice" framing gets repurposed as ceiling
2. **V-02 Exclusionary ROI** — risk that the cost-benefit material is recoded into an ROI argument that excludes high-cost-population provisions
3. **V-03 Surveillance via inferred functional needs** — risk that population-specific design analysis becomes population profiling
4. **V-05 Co-1 instrumentalization** — risk that lived-experience citation becomes consent-laundering
5. **EQ-21 Migration-survival register** — recently CANONICAL governance doc classifying which corpus content survives a planned form-pivot; checks the framing's posture toward deprecation of pre-pivot work

Files: `data/adversarial_use/catalog.yaml` (the catalogue) + `governance/adversarial-use-framework.md` (the framework) + `governance/migration-survival.md` (newly CANONICAL register). Public at github.com/jordanelias/guidebook. Total reading load ~40 pages.

**My ask:** review whether the mitigations are sufficient and whether the framing has any remaining risks I have missed. Written response (any length) preferred; videoconference also welcome.

**Estimated engagement:** 6–8 hours.

**Compensation:** This is a solo pre-launch project with no current budget. I can offer acknowledgment in the published guidebook, modest hourly compensation if your circumstances allow that, and (if your work has been cited in the guidebook) a citation review pass. Happy to discuss.

**Timeline:** No fixed deadline.

If this is not a fit, a referral to a disability-studies colleague who works on environmental design or design ethics would be welcome.

Thank you,

`[USER_NAME]`
`[USER_EMAIL]`

GitHub: github.com/jordanelias/guidebook

---

## Batch 3 — Methodology reviewer (research design / evidence synthesis)

**Subject:** Request for methodology review — accessibility guidebook evidence framework (Sonnet audit E1 follow-up, ~8–12 hour engagement)

**To:** `[METHODOLOGY_REVIEWER_NAME]`

---

Dear `[REVIEWER_NAME]`,

I am writing to ask if you would consider conducting a methodology review on the evidence framework of an accessibility design guidebook I am developing.

The guidebook draws evidence from peer-reviewed studies (Tier 1–2), authoritative standards (Tier 4), and lived-experience testimony (Co-1, treated as co-primary at Tier 3–4 per project doctrine). A separate Sonnet-conducted audit recommended that this framework receive external methodology review (item E1) before launch. The questions for review are:

1. **Convergence-record sufficiency** (V-04 from adversarial framework + EQ-18 in queue) — does the guidebook's convergence-tracking methodology reliably surface multi-jurisdictional or multi-tier disagreement?
2. **Evidence-tier laundering** (V-06) — are there structural ways for low-tier evidence to be cited as high-tier through chained synthesis?
3. **Decision protocol classification scheme** (EQ-18) — is the D-DOCT/D-METH/D-OP/D-SCHEMA/D-PRES taxonomy adequate for tracking governance decisions?
4. **Doctrine-recheck rubric** (EQ-19) — see the four-state contamination rubric in `governance/doctrine-recheck.md` §3.2; an internal second-eyes recheck (RC-002) found ~80% inter-reviewer agreement and queries the rubric's edge-case calibration
5. **Migration-survival register** (EQ-21) — newly CANONICAL `governance/migration-survival.md`; does the per-category disposition logic hold up under external scrutiny?

Files are at github.com/jordanelias/guidebook in the `governance/` directory and `data/doctrine_recheck/` directory.

**My ask:** I can offer this either as a single multi-question review (preferred — gives you context about the system as a whole) or as a journal-submission review of a methodology paper I would draft summarising the framework. Whichever fits your time better.

**Estimated engagement:** 8–12 hours for multi-question review; or normal manuscript-review time if journal-submission path.

**Compensation:** Pre-launch; solo author; no current budget. Acknowledgment in published guidebook + modest hourly compensation if circumstances allow + citation review pass on your work if cited.

**Timeline:** Flexible.

Thank you,

`[USER_NAME]`
`[USER_EMAIL]`

GitHub: github.com/jordanelias/guidebook

---

## Batch 4 — DPO / Co-1 outreach (single-pass review)

**Subject:** Request for review by your DPO — accessibility guidebook Co-1 protocol and population-specific provisions

**To:** `[DPO_CONTACT_NAME]` at `[DPO_NAME]`

---

Dear `[DPO_CONTACT_NAME]`,

I am the author of an in-development guidebook on accessible built-environment design that treats lived-experience evidence as co-primary at Tier 3–4 per project doctrine (rather than supplementary, as much of the existing literature does).

A separate audit of the project (Sonnet, 2026-04-30) recommended that the project actively seek DPO review (item E2) of two things:

1. **The Co-1 verification protocol** in `governance/co1-operational.md` — the operational rules for citing lived-experience sources, including the six-field schema (date, language, identifier, source URL or paper, population, citation field) and the Co-1 admissibility test
2. **Population-specific provisions** for `[POPULATION YOUR DPO REPRESENTS — e.g., IntD self-advocates / Deaf cultural community / Global South disability self-advocacy]` in the BPC corpus (`references/bpc/` directory)

The audit's particular concern is that the guidebook's posture toward DPO review has been "we will get review eventually" without specific outreach. I am writing now to make the specific outreach.

**My ask:** Either (a) a written response from a DPO-affiliated reviewer addressing whether the Co-1 protocol and the population-specific provisions are appropriate, or (b) a meeting at a time and format that works for your organisation. I will accept any of: full review, partial review of one of the two items, "this is not what we do; here is who you should ask", or "we want to be involved at a different stage". All are useful answers.

**Compensation:** This is a pre-launch solo project with no current budget. I can offer acknowledgment, modest compensation for any reviewer time if circumstances allow, and a clear understanding that if your DPO would like to be co-listed as a reviewing organisation that contribution will be recorded as such.

**Timeline:** No fixed deadline.

Files: github.com/jordanelias/guidebook (public). The two specific files are `governance/co1-operational.md` and the population-specific BPC files in `references/bpc/`. I am happy to send a curated reading-list of the most relevant ~30 pages if that helps.

Thank you for considering this.

`[USER_NAME]`
`[USER_EMAIL]`

---

## Batch 5 — Workflow-integration scoping (non-gating)

**Subject:** Quick scoping question — accessibility guidebook integration with `[BIM/CODE-COMMENTARY/OT-DELIVERY]` workflows

**To:** `[INTEGRATOR_CONTACT]`

---

Dear `[CONTACT_NAME]`,

I am developing an accessibility design guidebook (pre-launch; github.com/jordanelias/guidebook) that aims to be useful to designers, code commentators, and OT clinicians at the design stage rather than only at compliance-check stage.

A Sonnet audit of the project (2026-04-30) flagged that the guidebook's integration points with downstream tooling — BIM workflows, code-commentary databases, and OT clinical-delivery handoff — have not been scoped in a way that supports adoption. This item (E3 in the audit) is non-gating; the guidebook can launch without it. But scoping it now lets me make small adjustments early rather than expensive ones after publication.

**My ask:** A 30–60 minute scoping conversation (no commitment; not asking you to integrate, just to talk about what integration would need to look like). Your perspective on what data structure, format, or interface a `[BIM tool / code-commentary system / OT delivery workflow]` would need to consume the guidebook content as a useful input.

**Compensation:** This is a scoping conversation, not a paid engagement. If it leads to actual integration work later, that conversation would be separate.

**Timeline:** Whenever fits your schedule in the next 1–3 months.

Thank you,

`[USER_NAME]`
`[USER_EMAIL]`

---

## Batch 6 — Migration-survival register external review (EQ-21)

**Subject:** Brief review request — migration-survival classification register for accessibility guidebook (~3–5 hour engagement)

**To:** `[REVIEWER_NAME]` (best fit: methodology reviewer or disability-studies reviewer with archival/research-method background)

---

Dear `[REVIEWER_NAME]`,

I am writing to ask if you would do a brief review of one specific governance document in an accessibility guidebook I am developing (`jordanelias/guidebook`). The document was issued PROVISIONAL on 2026-05-01 by an Opus 4.7 session and adopted CANONICAL on 2026-05-02. The audit that recommended the document was conducted in the same conversation that authored it (a single-context risk that the project flags openly). External review is the structural counterweight.

The document is `governance/migration-survival.md` (314 lines). It classifies every artifact category in the project's pre-pivot corpus into one of five dispositions (SURVIVES_AS_IS / SURVIVES_WITH_REDERIVATION / SURVIVES_CONDITIONALLY / SUPERSEDED / OPEN) ahead of a planned form-pivot from prose-form deliverables to structured-data deliverables. The questions for review are:

1. Is the per-category classification logic internally consistent?
2. Is the §5 per-file decision rules table appropriate for the SURVIVES_CONDITIONALLY case (78 BPC `best_practice_synthesis` fields)?
3. Does the §6 [STRUCK] claim residue block adequately protect against silent migration of unsourced claims?
4. Is the §9 cross-stage thread CS-MIG operationalisation reasonable?

**Estimated engagement:** 3–5 hours.

**Compensation:** Pre-launch solo project; modest if circumstances allow; acknowledgment in published guidebook.

**Timeline:** No fixed deadline.

This is a much smaller ask than a full methodology review; if you'd like to start with a 30-minute call about whether the document seems coherent at a high level before committing to the deeper review, that would also work.

Thank you,

`[USER_NAME]`
`[USER_EMAIL]`

GitHub: github.com/jordanelias/guidebook (file path: governance/migration-survival.md)

---

## Application checklist

For each batch you commission:

- [ ] Identify candidate reviewer(s) — academic profiles, prior contact, or referral
- [ ] Fill bracketed placeholders in the corresponding draft
- [ ] Send via your normal channel (email, professional contact)
- [ ] Track responses in a separate (project-owner-maintained) tracking document; not in repo unless you choose to
- [ ] After response received, add a follow-up Decision record (D-NEXT) recording reviewer, response, and any guidebook revisions arising

---

## What this document does not do

- Identify specific reviewers (project-owner network selection)
- Send any emails (drafts only; project owner sends)
- Negotiate compensation (project owner workflow)
- Track responses (project owner workflow)

---

## Status

| Field | Value |
|---|---|
| Status | APPLICATION-READY |
| Pairs with Decision | D-0127 |
| Application owner | project owner |
| Application status | PENDING |

End of outreach drafts.
