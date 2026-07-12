# Guidebook Project — Comprehensive Repository Inventory and State Analysis

**Date:** 2026-07-12
**Prepared by:** multi-agent audit (3 initial recon agents + an 11-agent deep-read pipeline over ~86 additional documents + 4 synthesis agents), assembled and reviewed by Claude Code.
**Scope:** every top-level directory in the repository; a full read of every Decision Record, active workplan document, governance document, and audit report reviewed; a full read of the ~30 most recent session logs plus all handoff documents; a structural inventory (not an exhaustive read) of the remaining ~200 archived session logs and ~440 `references/` evidence-corpus documents. See §1 for exact scope boundaries.

---

## Executive Summary

**Guidebook** (formally *Guidebook for Accessible Design* / *Guidebook — Disability-Inclusive Design*, v10) is a solo-authored (jordanelias) research and publishing project building an evidence-graded reference on disability-inclusive built-environment design. It combines a markdown "book" (`parts/`), a canonical SQLite database (`data/guidebook.db`), a large evidence corpus (`references/`, 440 files), a generated static website (`site/`, `index.html`), and an unusually extensive governance apparatus (37 governance docs, 19 Decision Records, 263 session-log files, 74 workplan documents, 26+19 audit reports).

**Top five findings:**

1. **The project runs entirely on claude.ai (chat + Code Interpreter), not Claude Code.** No `.claude/` directory, `CLAUDE.md`, or MCP config exists anywhere in the repo. The 48 `skills/*_SKILL.md` files are a bespoke, well-formed analog built for that surface — a real, low-risk migration path exists (§6).
2. **The evidence base is large but its central deliverable is empty.** 640 evidence sources and 92 items exist, but the `evidence_cell_state` table — the per-parameter × per-population "what is the best practice" determination engine that is the project's entire reason for being — has zero rows as of the most recent documents reviewed (`workplan/best-practices-assessment-system.md`, 2026-06-22).
3. **The canonical database cannot currently be rebuilt from its own migration history.** Multiple Decision Records (DR-2026-05-15, DR-2026-05-28) document out-of-band schema edits, 113 unlogged data migrations, and a from-scratch rebuild that reproduces only 7 of 39 tables — ultimately resolved by formally exempting some tables rather than fixing reproducibility.
4. **A real, recurring evidence-bias pattern has been caught and re-caught at least seven separate times** between 2026-05-08 and 2026-05-26 (fabricated citations, misattributed authors, "convergence mistaken for evidence," topic-evidence conflated with claim-evidence). Each instance produced a genuine remediation (the Adversarial Research Protocol, Progressive Measurement Probe, `reasoning_doc_citations`), but the underlying tendency — a single unsupervised model overestimating its own verification — is still active as of the most recent session logs.
5. **Planning churns hard, then appears to have stabilized.** At least nine planning documents were each declared canonical and superseded within days to weeks during April–May 2026; the project converged on a stable operative plan (`audits/bpc-rewrite-workplan-2026-05-11.md`) on 2026-05-11, and later documents build on it rather than replacing it. Execution against that plan remains incomplete.

The project's own self-audit (`audits/project-shape-audit-2026-06-22.md`) grades itself C-/C-/D/C- across mission fitness, traceability, methodology transparency, and SQLite capability adoption. This report's independent integrity assessment (§5) concurs with those grades and, in one respect, considers them generous rather than harsh.

---

## 1. Scope and Methodology

This report was produced by a multi-stage multi-agent process:

- **Recon (3 parallel agents):** a full directory/file inventory of the entire repository; a sweep of session logs, handoffs, roadmaps, and commit history; and an exhaustive search for Claude Code configuration.
- **Deep-read (11 parallel/pipelined agents):** full reads of 86 additional documents not already covered by recon — the ~30 most recent session logs (2026-05-05 through 2026-06-11), all ~40 active `workplan/` documents, all 36 remaining `governance/` documents, the 14 remaining Decision Records, and 24 audit reports (2 top-level + all 21 `audits/_archived/` reports plus `verification-coverage-catalog-2026-05-13b.md`).
- **Synthesis (4 parallel agents):** a chronological timeline, a roadmap/workplan status matrix, an independent integrity assessment, and a Claude Code migration plan, each built from the deep-read data plus recon findings.

**Explicit scope limits (per user decision):**

- The local git clone is **shallow** (`--depth 50`; boundary commit `b529dde1`), covering only 2026-05-28 → 2026-07-06 (50 commits). Any claim about commit authorship, counts, or history before 2026-05-28 rests on session logs and Decision Records, not git itself, and cannot be independently verified against the true commit history without an unshallow fetch.
- The ~95 files in `sessions/_archive/` (2026-03-13 through 2026-03-31) and the ~440 documents in `references/` (the BPC/evidence corpus itself) were **not** individually read — they were structurally inventoried (file counts, directory purpose) but not read file-by-file. Conclusions about recurring *patterns* (evidence-bias, plan supersession, PI drift, DB non-reproducibility) are well-supported because they surface independently across dozens of unconnected documents that *were* read. Conclusions about exact *current-moment* state (e.g., today's exact open-gap count) are not reliably confirmable at this scope.
- "All conversations/chats/sessions" in this report means the git-committed `sessions/*.md` log corpus — the project's own record-keeping system. No external claude.ai chat export exists to cross-check against.
- The Claude Code ecosystem section (§6) is evaluation and recommendation only; no `.claude/` scaffolding was created as part of this task.

---

## 2. Full Repository Inventory

Root: `.gitattributes`, `.gitignore`, `index.html` (39KB, the live site's front page — "91 provisions, 661 evidence sources, 10 categories"), `requirements.txt` (exactly two pinned Python deps: `pydantic==2.13.3`, `PyYAML==6.0.3`). No `package.json`/`pyproject.toml`/`Makefile` exists. Repo size ~46M working tree, ~8.6M `.git`. Single remote (`github.com/jordanelias/guidebook`), branches `main` and the current session branch.

| Directory | Files | Size | Purpose |
|---|---|---|---|
| `references/` | 440 | 7.5M | The evidence/knowledge corpus: audit-briefs, audits, `bpc/` (Best Practice Compendium), `bpc-reasoning/`, change-orders (CO-0001–0009), conflict-matrices, connections/connection-reasoning, cost-data/economics, `fdr/` (Functional Deficit Research), methodology, search-log, systematic-reviews, plus root files (`skill-registry.md`, `specification-database.json`, `standards-registry.md`, `toc.md`, etc.) |
| `scripts/` | 311 | 9.0M | Python tooling: `audit/` (12 scripts), `ci_helpers/`, `convert/` (16 per-domain converters), `db/`, `generate/` (site generators), `migrate/`, `migrations/` (~190 SQL files, `001_initial_schema.sql`–`025_drop_colonial_role.sql` plus dated data migrations), `probes/`, `test/`, `tests/`, `bootstrap.sh` |
| `sessions/` | 263 | 3.3M | The work journal: 120 root session logs + 95 `_archive/` (back to 2026-03-13) + `artifacts/` + most-recent-session artifacts; `LATEST` pointer file; multiple `HANDOFF*.md` documents |
| `site/` | 117 | 1.7M | Generated static website (GitHub Pages): `populations/`, `rooms/` (17 pages), `specs/` (~90 pages) |
| `skills/` | 60 | 608K | 48 active `*_SKILL.md` files + `deprecated/` (12 files) — the claude.ai-Project-shaped analog to Claude Code skills (see §6) |
| `governance/` | 37 | 804K | Project doctrine, including `project-instructions-v10_7.md`–`v10_14.md` (the closest analog to CLAUDE.md) |
| `workplan/` | 74 | 1.6M | ~40 active documents + `deprecated/` (14) + `_superseded/` (14) |
| `attestations/` | 17 | 116K | Signed decision/session attestation JSON records |
| `schemas/` | 30 | 220K | Pydantic schema definitions mirroring the SQLite tables |
| `_archived/` | 53 | 1.6M | Retired content: `misc-2026/`, `research-2026/`, `working-2026/`, plus root files |
| `parts/` | 83 | 2.5M | Book chapters: `v10/` (current, 14 files), `deprecated/`, `_archived/v10-predraft-2026-04-23/`, `88_to_90/` (v9.0) |
| `audits/` | 26 | 400K | Self-audit reports, plus `_archived/` (19 more — see appendix) |
| `data/` | 30 | 5.1M | `guidebook.db` (SQLite, 4.85MB, canonical store, tracked as binary) + `adversarial_use/`, `decisions/decision_register.yaml`, `doctrine_recheck/`, `jurisdictional_values/` |
| `decisions/` | 19 | 248K | Decision Records `DR-2026-05-09` through `DR-2026-06-11`, plus `PI-update-needed.md` |
| `working/` | 7 | 588K | `mobile-app-prototype-v9/` — a React/JSX prototype marked "Complete" 2026-04-30 |
| `architecture/` | 9 | 228K | System design docs (`project-architecture-guidebook-v2.3.md`, `sqlite-data-layer.md`, `schema-spec.md`, etc.) |
| `versions/` | 3 | 1.2M | Frozen v9.0 document snapshots; `current/DEPRECATED.md` explicitly warns against using them as an audit source |
| `tools/` | 3 | 360K | Auto-generated "Spec Curation Vetting Surface" viewer + its regenerator script |
| `specs/`, `assets/`, `misc/` | 1 each | 112K/80K/44K | Single exemplar spec page; site stylesheet; one archived file |
| `.github/` | 6 | 52K | `CODEOWNERS` (single-owner `@jordanelias`) + 5 workflow files: `ci.yml`, `audit.yml`, `verify-urls.yml`, `resolve-dois.yml`, `regenerate-vetting-surface.yml` — genuinely mature CI (concurrency guards, idempotency checks, self-push retry logic) that was **deleted by the owner on 2026-06-09** (still present in the repo history/files reviewed here, but session logs confirm this action; current enforcement is agent self-checks) |

No `.claude/`, `CLAUDE.md`, `.mcp.json`, or `settings.json` exists anywhere in the repository (see §6).

---

## 3. Project Timeline and History

**Pre-2026-04-26: Legacy foundation (v9.0 and the March critique).** The earliest material visible in this audit is `audits/_archived/Critique_Report_v9-0_2026-03-20.md`, a systematic internal critique of Guidebook v9.0 (6,546 lines) that found strong philosophical architecture (Three-Tier Hierarchy, Co-1 co-primary status, Design Modes) sitting atop serious mechanical rot: 68+ phantom item cross-references, a completely empty Master Bibliography, section-numbering collisions, and duplicate item blocks. This is the project's founding self-diagnosis, and its central complaint — evidentiary ambition outrunning evidentiary plumbing — recurs almost verbatim in every later audit through `audits/project-shape-audit-2026-06-22.md`. Through April, a long series of hallucination/citation-verification audits (2026-04-06 through 2026-04-24) progressively found and fixed fabricated citations (e.g., a fabricated Mostafa 2021 DOI, an Ismail 2023 source that was actually McVeigh 2008), misattributions, and a striking finding that ~16% of nominal "Tier 1" sources were actually misclassified lower-tier evidence — undermining any prior conflict-resolution work that depended on tier status. Two duplicate, non-reconciled "Phase 2A jurisdiction audits" (2026-04 and 2026-04-24, using 46 vs 49 jurisdictions) reveal an early pattern of parallel, uncoordinated audit efforts.

**2026-04-26 to 2026-04-30: Stage A governance foundation.** Stage 0 closed (waiving the mandated "sit-with" reflection period, per `governance/workplan-adoption.md`) and Stage A began in earnest. In a single dense week, the project locked its foundational doctrine: `mission-and-epistemics.md` and `audience-priority.md` (both iter-4, 2026-04-26), replacing an earlier `mission-PROVISIONAL.md` that had described a *fictional* Co-1 "Reviewer/Drafting" collaborator structure — corrected same-day in `pre-stage-a-decisions.md`'s D-03 revision to an honest solo-authorship declaration. This is the project's first explicit self-correction of a fabricated operational claim about itself. A3 (conceptual model), A6 (evidence methodology), A7 (population taxonomy), A8 (jurisdiction philosophy), A9 (time model), A11 (legal/regulatory, still blocked on unavailable counsel review), A12 (decision protocol) and A13 (doctrine-recheck cadence) were all authored in rapid succession. Budget tracking already showed strain: `workplan/a6-handoff.md` (2026-04-29) reports Stage A projected at 37-44 sessions against a 22-32 session budget — over by 5-12 sessions, the first of many budget overruns the project would candidly self-report rather than hide.

**2026-05-01 to 2026-05-02: The B1 storage-form derivation.** An eight-session, rubric-driven process (`workplan/b1-derivation-framework.md` through `b1-comparative-scoring.md`) evaluated four storage candidates (Markdown+YAML, Relational, Graph/RDF, Hybrid) against a 30-criterion, 171-point weighted rubric. Candidate D (hybrid) was eliminated by strict dominance; Candidate B (Relational/SQLite) scored 89% and was ultimately selected over Candidate C (Graph/RDF, 91%) via a deliberate tradeoff-aware decision rather than simple highest-score selection.

**2026-05-05: The SQLite pivot.** `session_2026-05-05-infra-s1-sqlite.md` built the actual data layer (15 tables, `db.py` CLI, migrating 556 evidence sources, 245 connections, 168 gaps from markdown registers), but shipped with real column-naming defects that had to be corrected the very same day in `session_2026-05-05-c2-skill-overhaul.md` — the first of many "ship it, then immediately patch it" cycles.

**2026-05-08 to 2026-05-11: The evidence-integrity crisis and the great supersession.** This is the project's true inflection point. `session_2026-05-08-co0009-phase3.md` introduced the Adversarial Research Protocol (DR-2026-05-09) after catching four fabricated claims on first deployment, including a fabricated Chaffin et al. 2006 citation the protocol used as its *own worked example*. `session_2026-05-09-co0009-gap-verify.md` then found that 8 of 12 (67%) of a session's own gap closures needed correction under stricter scrutiny — the origin of the now-canonical finding "the protocol does NOT make Claude rigorous, it makes Claude's bias VISIBLE." Then `session_2026-05-11h` and the resulting `audits/bpc-rewrite-workplan-2026-05-11.md` delivered the crisis verdict: only 14/661 (2%) of evidence sources were VERIFIED, 567/661 were AUTHOR-TITLE-ONLY, and citation_mining sat at 0 rows despite being mandated by project rules for over a month. This triggered the single largest supersession event in the project's history: Appendix E of that workplan formally superseded roughly a dozen workplans, retracted ~30-70 prior BPC syntheses pending reverification, and became "PI v10.8" the same day — though the live claude.ai copy stayed on v10.6, opening the PI-drift pattern that recurs through `decisions/PI-update-needed.md` for months.

**2026-05-11 to 2026-05-20: Rehabilitation marathon, with real incidents.** `session_2026-05-11g` documented triple concurrent-write clobbering of the git-tracked SQLite binary by a parallel session, total DB-write loss recovered only via a hand-built replay script — leading to `governance/migration-based-writes-adopted-2026-05-11.md` adopting migration-based schema/data changes over direct writes. `session_2026-05-15a-governance-reconciliation.md` then found a genuinely serious silent data-loss event: a 2026-05-07 DB reset had silently dropped 28 connections still cited in canonical Part 10 text, requiring git-archaeology reconstruction. `session_2026-05-20-ato-rehab.md` began as a bounded pilot and, through repeated owner "Continue" directives, ballooned into an 80+ batch marathon pushing the evidence-eligible pool from 35% to 92.6%.

**2026-05-23 to 2026-06-11: Protocol layering and CI removal.** New protocol layers accumulated: the supersession-check protocol (DR-2026-05-24), gap-driven-mining (DR-2026-05-26, later found to have been built but never exercised — 0 rows), and the Progressive Measurement Probe. The tier system itself was formally reconciled (`DR-2026-05-29`) after PI v10.14, `tier-system.md`, and the live database disagreed on whether systematic reviews sat at Tier 2 or Tier 3. Most consequentially, `session_2026-06-11-stages1-2-and-4.2-4.3prep.md` confirms **the owner deleted the CI/GitHub Actions workflows on 2026-06-09**, shifting enforcement entirely to self-run verification before direct pushes to main — a governance posture change with no external backstop.

**2026-06-10 to 2026-06-22: Phase E and the honest ceiling.** `workplan/phase-e-execution-plan-v1.md` (2026-06-10) scoped re-synthesis of 68 retracted BPCs, alongside `DR-2026-06-10-synthesis-model-floor` (reinterpreting the Sonnet/Opus rule as a capability floor to permit "Claude Fable 5") and `DR-2026-06-10-e2g-reverification-scope` (mandating that re-synthesis treat old prose only as a bias-tagged claim checklist, never reusable text). The trajectory culminates in `audits/project-shape-audit-2026-06-22.md`'s blunt verdict — grades of C-, C-, D, C- — and `workplan/best-practices-assessment-system.md`, which names the empty `evidence_cell_state` table as the single unbuilt core of the entire project: a strong evidence library sitting atop a judgment layer that, as of the most recent documents, does not yet exist.

---

## 4. Roadmap and Workplan Status Matrix

| Document | Date | Claimed Scope | Current Status | Notes (planned vs. actual) |
|---|---|---|---|---|
| CO-0001–CO-0003 | pre-2026-03-28 | Earliest Change Orders establishing Part-numbering/workplan structure | unclear | Not directly recovered; referenced only as predecessors to CO-0004 |
| `P1-D2-D3-co0004-remapping.md` | 2026-03-29 | CO-0004: remap old Part numbering (3–13) to new (3–12) | completed | Purely translational; executed cleanly |
| `slug-triage-2026-03-28.md` | 2026-03-28 | Phase 2A triage of 48 placeholder BPC slugs | superseded | Later classified "Historical (pre-Stage-A)" |
| `evidence-expansion-2026-04-03.md` (CO-0005) | 2026-04-03 | 40–60 session evidence-base expansion (jurisdictions 24→46, languages 14→19) | superseded | Superseded 2026-05-11; folded into bpc-rewrite-workplan §B/C |
| `opa-adjudication.md` | 2026-04-03 | Opus adjudication of Part 5 conflict-resolution table | completed | 9/11 entries confirmed correct; contradicted-in-the-wild by opb-adjudication |
| `opb-adjudication.md` | 2026-04-03 | Adjudication of 10 CON entries | completed | Surfaced RT60/STI numeric contradictions; only 1 of 6 fixes applied immediately |
| `opg-methodology-review.md` | 2026-04-03 | Methodology review of conflict-resolution tree | completed | Found step-numbering mismatch, 2 missing resolutions |
| `opus-missing-passes.md` | 2026-04-03 | Master remediation tracker after Sonnet improperly performed Opus-reserved work | completed | Process-violation origin; all 10 passes logged complete within ~2 hours |
| `opus-synthesis-queue.md` | 2026-03-29/2026-05-08 | Track Opus-synthesis status | unclear | Cites a plan already superseded by the time it was "cleaned"; likely orphaned |
| `roadmap-2026-04-27.md` | 2026-04-27; deprecated 2026-05-08 | Full-project roadmap, 220–336 session horizon | deprecated | Own banner: superseded within days, itself then contradicted |
| workplan-co0007-v4 (referenced only) | ~2026-04/05 | Canonical workplan naming Stage A complete | superseded | Cited as canonical by 4+ documents, then superseded 2026-05-11 |
| `a1-a2-iteration-plan.md` | 2026-04-26 | Stage A1–A2 (audience/mission) | completed | Confirmed complete via a4 audit |
| `co0008-scope-infrastructure-overhaul.md` (CO-0008) | 2026-04-26 | 3-layer infra overhaul | superseded | Superseded 2026-05-11, folded into §A |
| `co0008-throughline-analysis.md` (CO-0008) | 2026-04-26 | Pydantic schema design analysis | superseded | Superseded 2026-05-11; self-reports 0/73 records Opus-synthesized |
| `a4-part01-audit-2026-04-27.md` | 2026-04-27/29 | Stage A4 voice/framing audit | completed | Internal arithmetic inconsistency (30 vs 38 reframes); spawned GAP-VOICE-01 |
| `a5-handoff.md` | 2026-04-29 | Scope Stage A5 (Co-1 operational spec) | completed | Confirmed same day; budget already over |
| `a6-handoff.md` | 2026-04-29 | Scope Stage A6 (evidence methodology) | completed (per later docs) | Self-reports Stage A over budget by 5–12 sessions |
| `b1-derivation-framework.md` | 2026-04-30 | Storage-form decision framework | completed | Self-corrects criteria count 24→30 |
| `b1-criteria-weighting.md` | 2026-05-01 | Lock weighting scheme | completed | Self-corrects 17→21 weight-2 criteria |
| `b1-candidate-a-markdown-yaml.md` | 2026-05-01 | Score Candidate A | superseded | 132/171 (77%) |
| `b1-candidate-b-relational.md` | 2026-05-02 | Score Candidate B (SQLite) | completed | 152/171 (89%) |
| `b1-candidate-c-graph.md` | 2026-05-02 | Score Candidate C (RDF/graph) | completed | 155/171 (91%), worst Operational score (33%) |
| `b1-candidate-d-hybrid.md` | 2026-05-02 | Score Candidate D (Hybrid) | superseded | Dismissed by strict dominance, 0 wins/18 ties/12 losses |
| `b1-comparative-scoring.md` | 2026-05-02 | Cross-candidate comparison | open | Actual selection (Session 8) never captured in reviewed files |
| `co0009-phase0-handoff.md` (CO-0009) | 2026-05-07 | 10 gating decisions to activate item-audit pipeline | blocked | Hard blocker: 8/10 decisions never confirmed |
| `workplan-item-audit-pipeline-co0009.md` (CO-0009) | 2026-05-05 | 8-step per-item audit pipeline | superseded | Superseded 2026-05-11 while still PROPOSED |
| `external-review-queue.md` | 2026-05-01 | Register of 21 external-review items | open | DRAFT, no paired Decision record |
| `external-review-outreach-drafts.md` | 2026-05-02 | 6 outreach email drafts | open | "Application status: PENDING" — none confirmed sent |
| `gap-p1-reclassification-recommendation.md` | 2026-05-01 | Reclassify 2 P1 gaps to P2 | open | Unadopted recommendation |
| `placeholder-review-triage.md` | 2026-05-01 | Triage 106 seeded Decision records | open | Pure recommendation, no review performed |
| `struck-claim-research-attempt_2026-05-01.md` | 2026-05-01 | Re-source 3 struck BPC claims | open | 2 of 3 rescued with weaker sources; 1 figure never located |
| `economics-audit-research-2026-05-03.md` | 2026-05-03 | Audit + expand economics evidence | open | "INTERIM"; contains a duplicated section (structural anomaly) |
| `multilingual-search-remediation.md` | 2026-05-09 | Remediate 30/91 SPECULATIVE items | superseded | Superseded 2 days later, before its own work appears to have executed |
| `research-protocol-adversarial.md` (v2) | 2026-05-09 | 5 falsifiable fields per finding | active | Subordinate to the 2026-05-11 rewrite, not superseded; later ratified as DR-2026-05-09 |
| `audits/bpc-rewrite-workplan-2026-05-11.md` | 2026-05-11 | 8-phase, ~2,200–2,300 hour rehabilitation | active | The pivotal document — still the operative umbrella plan |
| `website-preparation.md` (CO-0006) | 2026-04-17/2026-05-08 | BPC source-migration pipeline, transition criteria | superseded | Already a v3.0 excision of a stale v2.0 predecessor |
| `workplan-jurisdiction-sweep.md` | 2026-04-23 | 45–55 session jurisdiction/code coverage closure | superseded | Folded into §C, rescoped |
| `workplan-reconciliation-2026-05-08.md` | 2026-05-08 | Reconcile CO-0001–0009 | superseded | Superseded 3 days later; self-reports its own gate mechanism enforces the wrong model |
| `adherence-attestation-build-2026-05-17.md` | 2026-05-17 | Cryptographic doctrine-SHA + attestation governance | open (proposed) | Names an irreducible "compound gaming vulnerability" it cannot close |
| `progressive-measurement-protocol.md` | 2026-05-10 | PMP iterative numerical-value validation | active | Subordinate protocol, not superseded; adoption checklist partly unchecked at writing |
| `phase1b-part01-s15-expansion.md` | undated | Replace Part 1 §1.5 Evidence Hierarchy | open | Position in timeline unclear; requires voice-style pass before integration |
| `decisions/PI-update-needed.md` | ongoing | Track PI live-vs-repo drift | active | Chronic, never fully closed |
| `phase-e-execution-plan-v1.md` | 2026-06-10 | Re-synthesize 68 retracted + 13 unsynthesized BPCs | active | Blocked pending owner decisions D-4.3-A/C |
| `best-practices-assessment-system.md` | 2026-06-22 | Best-practice determination engine design | open (design only) | The single most load-bearing unbuilt piece; `evidence_cell_state` empty |
| `search-coverage-completion-workplan.md` | 2026-06-22 | Replace placeholder search-coverage grids | active | Most recently dated; most historical coverage data unrecoverable |

**Overall pattern:** In the roughly three weeks from `evidence-expansion-2026-04-03.md` through `workplan-reconciliation-2026-05-08.md`, at least nine distinct planning documents were each declared canonical only to be superseded within days to weeks — several before their own gating decisions were ever ratified. The pattern breaks on 2026-05-11: `audits/bpc-rewrite-workplan-2026-05-11.md` was issued with an explicit Appendix E supersession map covering all 54 `workplan/` files at once, and — unlike every predecessor — it has held. Later documents (`phase-e-execution-plan-v1.md`, `search-coverage-completion-workplan.md`, both building on the 2026-05-11 plan) carry no supersession banners of their own. As of the most recent dated material, the operative plan is the layered stack of the 2026-05-11 master plan plus Phase E (tactical, BPC re-synthesis) plus the search-coverage plan — but even this current stack is explicitly blocked on unresolved owner decisions and rests on the still-unbuilt `evidence_cell_state` engine: the project has converged on *which* plan is authoritative even though execution against it remains incomplete and partly stalled.

---

## 5. Integrity Assessment

**1. Data integrity.** The SQLite store (`data/guidebook.db`, `user_version=25`) has repeatedly drifted from its own migration history. DR-2026-05-15 documents 11 direct schema edits bypassing migrations, expanding `evidence_sources` from 23 to 81 columns. DR-2026-05-28 found 113 data migrations applied out-of-band and never logged, and confirmed a from-scratch rebuild cannot reproduce 165 author rows plus 2 pipeline-run rows added by a scheduled job — ultimately "resolved" by ratifying the gap as an intentional exemption rather than fixing reproducibility. The 2026-06-11 session log independently confirms the rebuild only reproduces 7 of 39 tables. Separately, a 2026-05-07 DB reset silently dropped 28 connections still cited in canonical text, requiring hand reconstruction from git history, and the DB binary was clobbered three times by a concurrent session before migration-based writes were adopted (only partially — the direct-write path is explicitly noted as still active and still vulnerable). Against this, 635/640 sources are verified at the *existence* level — but existence-verification and claim-verification are different things in this project's own vocabulary, and claim-level verification (`evidence_cell_state`, `source_value_extractions`) remains almost entirely unpopulated. This is a project whose canonical data store cannot currently be rebuilt from its own audit trail — a real, not cosmetic, data-integrity failure, candidly self-documented.

**2. Process integrity.** The headline finding — Claude systematically conflating "evidence on the topic" with "evidence supporting the specific claim," with an owner spot-check finding bias in 8 of 12 (67%) gap closures — is real, and its remediation (the Adversarial Research Protocol, later PI standing rules #7–#10) is genuine and iterated seriously. But this was not an isolated incident: independent sessions caught a fabricated "Avandell" NJ cost-premium figure, a fabricated Chaffin et al. 2006 citation used as the adversarial protocol's *own worked example*, a silent `INSERT OR IGNORE` bug that caused a false claim of "4 verified citations" against an actual DB state of 0, ~16% of nominal Tier-1 sources misclassified, and a slug marked "COMPLETE, no correction needed" overturned three hours later by a protocol-compliant redo. The pattern recurs across at least seven independent sessions (2026-05-08 through 2026-05-26), each catching a different flavor of the same failure mode — under-verification presented with unwarranted confidence. Each response is a real fix, but the recurrence indicates the underlying tendency is being repeatedly patched rather than structurally eliminated; a self-reported "three unverified pushes before a CHECK-constraint violation was caught" incident (2026-05-17) shows the discipline still lapsing well after the rules were codified.

**3. Planning integrity.** The workplan corpus shows extreme plan churn (§4). This is not obviously pathological on its own — solo research projects legitimately re-plan as facts change — but two things push it toward a genuine integrity concern: budget estimates are revised so frequently and by such large multiples (Stage A alone went from 22–32 to a self-reported 37–44 sessions) that the project's own forward projections carry little evidentiary weight; and PI live-vs-repo drift is a standing, unresolved condition, not a one-time bug — `decisions/PI-update-needed.md` exists specifically because this recurs every time the PI changes. Given the PI encodes the actual enforceable standing rules, a project whose enforcement layer is chronically out of sync with its committed doctrine has a real gap between what governance says should happen and what an agent is actually being told to do session-to-session.

**4. Governance integrity.** CODEOWNERS lists a single owner for a repo where, in the visible (shallow) commit window, 27 of 50 commits are attributed to "Claude (staged, no-push)," 12 to `github-actions[bot]`, 9 to `guidebook-agent`, and only 2 to the human owner — meaning code review, in any conventional sense, is not occurring; the project instead relies on agent self-attestation plus periodic owner spot-checks, and the CI workflows that provided the closest thing to automated review were deleted by the owner on 2026-06-09. Decision Record discipline is reasonably strong in form (numbered, dated, often explicitly self-critical) but weak in closure: numerous DRs remain PROPOSED while their content is already being executed against the live DB, and 106 of 128 decision-register records are unreviewed placeholders. On candor: the project's audits are unusually self-incriminating rather than self-serving — `project-shape-audit-2026-06-22.md` graded itself C-/C-/D/C- and named the empty `evidence_cell_state` table as the single most load-bearing gap; `best-practices-assessment-system.md` admits its own multi-agent review step was skipped for budget reasons, not rigor reasons. That candor is itself evidence of a genuinely functioning (if under-resourced) internal check — a mitigating governance signal even where the underlying substance is weak.

**5. Scope of this analysis.** This assessment rests on a shallow git clone (2026-05-28 to 2026-07-06 only) — commit-level claims are reliable only within that window. The session-log corpus is complete back to 2026-03-13, and the summaries above draw on a substantial but explicitly non-exhaustive targeted read (roughly 40 session logs, 25 workplan files, 20 governance docs, 12 decision records, and 20 archived audits out of several hundred total documents). Conclusions about *recurring patterns* are well-supported because they surface independently across many unconnected documents. Conclusions about *current, present-tense state* are not reliably confirmable without either the full git history or an exhaustive read of every remaining file — several documents already indicate live state has moved past what was reviewed here (e.g., `governance/tier-system.md`'s reference to "PI v10.14," a version not itself included in this audit's read set).

**6. Overall verdict.** This report concurs with the project's self-grades, and in one respect considers them generous rather than harsh. S3 (methodology transparency) at D is clearly correct and arguably the most defensible grade in the set — the claim-verification gap is a first-order problem for a project whose entire value proposition is evidentiary rigor. S1/S2/S4 at C- are fair: the project has real, unusual strengths (a large, multiply-cross-audited evidence corpus; a genuinely iterated methodology; unusually candid self-audits) that keep it out of D/F territory, but the DB-reproducibility failures, the chronic PI drift, the near-total absence of human code review, and the recurring evidence-bias pattern are structural, not cosmetic. Where this report pushes back on the project's own framing is subtler: the self-audits tend to treat each incident as a discrete, now-remediated event, when the deep-read pattern across ten-plus sessions shows these are recurring instances of the same two underlying failure modes — a single unsupervised model overestimating its own verification, and a solo-owner governance loop too thin to keep enforcement synchronized with intent. The remediations are real and improving, but the failure mode itself, not just its instances, is still active as of the most recent documents read.

---

## 6. Claude Code Ecosystem Gap Analysis and Migration Recommendations

### 6.1 Current state: zero Claude Code footprint, full claude.ai-Project footprint

An exhaustive search confirms there is no `.claude/` directory, no `CLAUDE.md`, no `.mcp.json`/`mcp.json`, no `settings.json`/`settings.local.json`, and no `agents/` directory anywhere in the tree. This reflects the project's actual operating model: `architecture/project-architecture-guidebook-v2.3.md` and `governance/project-instructions-v10_14.md` both state the surface explicitly as "claude.ai chat with Code Interpreter." The repo is designed, session-to-session, to be driven by a human pasting the PI into claude.ai Project Settings, then manually fetching and piping `scripts/bootstrap.sh` at session start via a "thin caller" block embedded in that PI text. The one PAT the project depends on lives only in the live claude.ai project-settings copy of the PI; the repo copy is deliberately redacted for GitHub secret-scanning.

The string "Claude Code" appears in exactly four files, and in every case it refers to a planned, not-yet-started future workstream — the Phase B website build (Next.js + PostgreSQL + Directus + Meilisearch + Vercel, 43–70 sessions), itself currently marked DEFERRED/MAY BE SUPERSEDED pending Stage B7 architecture lock. Nothing in the current, active editorial and research workflow runs under, or was designed for, Claude Code. The good news is that the claude.ai-side analogs are unusually well-formed substitutes to translate from — the PI is already organized into sections that map cleanly onto CLAUDE.md conventions, and the skill corpus already uses `name`+`description` frontmatter for the large majority of files.

### 6.2 File-level migration plan

**Root `CLAUDE.md`** should be assembled by translating `governance/project-instructions-v10_14.md` section-by-section: `<project_identity>` becomes an Identity section (with the PAT line dropped entirely — Claude Code should use `gh auth`/the ambient GitHub App credential, never an inlined PAT); `<decisions>`/`<terminology>` carry over as locked project doctrine; `<reference_files>` becomes a "Key files"/"load on demand" list; `<skills_assigned>` points at `references/skill-registry.md`; `<hooks_status>` becomes a "CI and automation" section; standing rules 1–11 carry over as a numbered list (rule #11's `[DOCTRINE: <sha>]` commit format is directly enforceable via a Claude Code hook if desired); the PI's changelog becomes CLAUDE.md's own version history.

**Skills: `skills/<name>_SKILL.md` → `.claude/skills/<name>/SKILL.md`.** All 48 active files need a folder-per-skill restructure. Of these, 43 already use compatible `name`+`description` frontmatter (a mechanical rename/move). Five require a genuine frontmatter rewrite because they use an incompatible schema (`title`/`purpose`/`status`/`enforcement` instead of `description`) and read more as governance/protocol documents than invocable skills: `adversarial-research_SKILL.md`, `evidence-metadata-rehabilitation_SKILL.md`, `progressive-measurement_SKILL.md`, `reasoning-doc-citations_SKILL.md`, `voice-style_SKILL.md`. The 12 files in `skills/deprecated/` should not migrate as live skills. `references/skill-registry.md` should remain the source of truth post-migration but needs path updates; the four named PI-placeholder skills (`bpc-curator`, `gap-register`, `bpc-writer`, `opus-synthesis`) remain intentionally absent, not a bug. CODEOWNERS currently excludes `skills/` itself from required review — this gap should close as part of migration, since live Claude Code skills executing with tool access are a materially higher-stakes surface.

**`github-filing_SKILL.md` and `github-io_SKILL.md`** are hand-rolled Python/urllib GraphQL/REST clients authenticating with a PAT — a workaround for claude.ai's lack of native git/gh access. In Claude Code this is unnecessary: both should be rewritten to shell out to `git`/`gh` via Bash directly, eliminating the embedded PAT-handling code entirely.

### 6.3 `scripts/bootstrap.sh` as a real SessionStart hook

Today, `bootstrap.sh` is fetched over the GitHub API and manually piped into a claude.ai session via a six-line "thin caller" pasted into the PI text — not automated by any harness, dependent on a human remembering to run it every session. In Claude Code this becomes a `SessionStart` hook registered in `.claude/settings.json`, invoked automatically with no manual paste step. The script's existing behavior (halting on missing critical files, querying `data/guidebook.db` for live state counters) translates directly; changes needed are (a) confirming its file/DB logic resolves against local paths rather than the GitHub API, and (b) removing the gh-or-curl dual-backend fetch logic devised for the paste-into-claude.ai workflow.

### 6.4 Relationship to the planned Phase B Claude Code website build

The Phase B website build and the ecosystem migration described here are related but not the same project, and should be sequenced deliberately: the core skills/CLAUDE.md/settings.json migration should happen **before or independently of** Phase B — it is low-risk, self-contained, and unblocks any Claude Code usage of this repo, including ordinary maintenance work that has nothing to do with the website. Gating it on Phase B (itself gated on Stage B7 architecture lock) would leave the repo unable to be operated via Claude Code for months for no good reason. Once the base migration is done, Phase B's own Claude Code sessions inherit it for free.

### 6.5 Prioritized next steps

1. Draft `.claude/settings.json` and a `SessionStart` hook wrapping `scripts/bootstrap.sh` — lowest risk, highest immediate value.
2. Draft root `CLAUDE.md` by translating `governance/project-instructions-v10_14.md` per §6.2, with the PAT line dropped rather than carried forward in any form.
3. Bulk-migrate the 43 compatible skills from `skills/<name>_SKILL.md` to `.claude/skills/<name>/SKILL.md`.
4. Rewrite frontmatter for the 5 non-conforming skill files, deciding per-file whether each becomes a real skill or a referenced governance doc instead.
5. Rewrite `github-filing` and `github-io` to drop urllib/PAT logic in favor of `git`/`gh` via Bash.
6. Add `skills/` (or its migrated successor) to CODEOWNERS alongside `references/skill-registry.md`.
7. Update `references/skill-registry.md` to reflect new paths and confirm the four placeholder skills are still intentionally absent.
8. Decide on and, if desired, restore a minimal `.github/` CI presence appropriate to a Claude-Code-operated repo, given CI was deleted 2026-06-09.
9. Only after the above is stable, revisit Phase B's Stage B7 architecture lock as its own separate effort.

---

## 7. Appendix: Deep-Read Document Log

Full-text-read documents beyond the recon phase, organized by category. Each entry is file / date / status / one-line finding.

### 7.1 Session logs (30 most recent, 2026-05-05 → 2026-06-11)

| Session | Date | Status | Key finding |
|---|---|---|---|
| `session_2026-06-11-stages1-2-and-4.2-4.3prep.md` | 2026-06-11 | blocked | Stages 1–2/4.2 complete; Stage 4.3 blocked on owner decisions; confirms CI deleted this session |
| `session_2026-05-26-gap-driven-mining-protocol-design.md` | 2026-05-26 | open | Reconstructed record of unlogged work; gap-driven-mining protocol built but 0 rows exercised |
| `session_2026-05-23-bpc-rewrite-phase-b-closure.md` | 2026-05-23–25 | completed | Retraction cohort 2.3x larger than estimated (70 vs ~30 files) |
| `session_2026-05-20-ato-rehab.md` | 2026-05-20–22 | completed | Pilot ballooned into 80+ batch marathon; eligible pool 35%→92.6% |
| `session_2026-05-19-deployment-state-reconciliation.md` | 2026-05-19–20 | completed | Fixed 4 pre-existing CI failures silent for up to 15 days |
| `session_2026-05-17-pilot-pass-2-and-3.md` | 2026-05-17–18 | open | Self-reported: 3 unverified pushes before a CHECK-constraint catch |
| `session_2026-05-15a-governance-reconciliation.md` | 2026-05-15 | completed | Discovered and repaired real data loss (28 connections silently dropped by a 2026-05-07 reset) |
| `session_2026-05-13b-evidence-verification-methodology.md` | 2026-05-13 | completed | Adopts DR-2026-05-13 three-track hybrid verification methodology |
| `session_2026-05-13a-url-verification.md` | 2026-05-13 | completed | VERIFIED sources 53%→60.7%; documents durable method lessons |
| `session_2026-05-12j-phase-b-verification.md` | 2026-05-12 | completed | VERIFIED sources 42%→53%; 5 false-positive DOI reverts restored |
| `session_2026-05-11i-workplan-consolidation.md` | 2026-05-11 | completed | Adopts BPC rewrite workplan as sole operative plan; documents PI drift (live v10.6 vs repo v10.8) |
| `session_2026-05-11h-bpc-rewrite-workplan-design.md` | 2026-05-11 | superseded | Crisis audit: 14/661 (2%) sources VERIFIED |
| `session_2026-05-11g-citation-mining.md` | 2026-05-11 | completed | citation_mining table found at 0 rows (GAP-283); triple DB clobber incident |
| `session_2026-05-10f-term-alias-expansion.md` | 2026-05-10–11 | completed | Found earlier "FULL" multilingual batch-marking was systematically unreliable |
| `session_2026-05-10f-accessibility-remediation.md` | 2026-05-10 | open | 19 WCAG fixes via static analysis only, no browser/AT testing |
| `session_2026-05-10e-slug3-adversarial.md` | 2026-05-10 | completed | PMP walk surfaces critical B-01 metric error (EML→melanopic-EDI) |
| `session_2026-05-10d-pmp-governance.md` | 2026-05-10 | completed | Rebuilds PMP protocol from a concept lost to context compaction |
| `session_2026-05-10c-protocol-redo.md` | 2026-05-10 | completed | Redo of slug 2 under adversarial protocol overturns prior "sound" verdict |
| `session_2026-05-10b-multilingual-slug2-3.md` | 2026-05-10 | superseded | "COMPLETE, no correction needed" verdict overturned 3 hours later |
| `session_2026-05-10-pass2-completion.md` | 2026-05-10 | completed | Fabrication found: NJ-specific stat mislabeled as US-wide average |
| `session_2026-05-10-multilingual-lrv.md` | 2026-05-10 | open | Begins multilingual Tier-1 remediation, long-pending since 05-08/09 |
| `session_2026-05-10-ecosystem-audit.md` | 2026-05-10 | completed | Full 19-table DB integrity audit; 701 duplicate rows removed |
| `session_2026-05-10-bpc-audit.md` | 2026-05-10 | blocked | "Convergence != Evidence" thesis; untraced external commit observed |
| `session_2026-05-10-bpc-audit-2b2c2e2a.md` | 2026-05-10 | open | Confirmed fabrication (Avandell); bad commit with empty DB blob caught and reverted |
| `session_2026-05-09-co0009-gap-verify.md` | 2026-05-09 | open | The 67% correction-rate finding; "protocol makes bias visible, not Claude rigorous" |
| `session_2026-05-08-co0009-phase3.md` | 2026-05-08 | completed | Adversarial Research Protocol adopted after catching 4 fabrications on first use |
| `session_2026-05-06-synthesis-scan.md` | 2026-05-06 | completed | Corrects a rationale attributed to a paper that doesn't support it, contradicted by clinical guidance |
| `session_2026-05-05-terragon-p2-gaps.md` | 2026-05-05 | completed | Closes 80 of 131 P2 gaps; clean close, no blockers |
| `session_2026-05-05-infra-s1-sqlite.md` | 2026-05-05 | completed | Builds the SQLite data layer; ships with schema-naming defects |
| `session_2026-05-05-c2-skill-overhaul.md` | 2026-05-05 | completed | Same-day fix of the prior session's schema-naming defects |

### 7.2 Active workplan documents (41 files)

Full summaries are incorporated into §4's status matrix. Notable cross-cutting findings not otherwise captured: `workplan/adherence-attestation-build-2026-05-17.md` names an irreducible "compound gaming vulnerability"; the B1 storage-form derivation (`b1-derivation-framework.md` through `b1-comparative-scoring.md`) is the most internally rigorous sub-process in the corpus but its final selection (Session 8) is not captured in any reviewed file; `workplan/best-practices-assessment-system.md` (2026-06-22) explicitly notes its own multi-agent panel review was skipped for budget reasons.

### 7.3 Governance documents (36 files)

Key findings not already covered in §3/§5: `governance/mission-and-epistemics.md` contains an internal contradiction (header says "CANONICAL," body says "Not yet operative"); `governance/pi-revision-co.md` (a 2026-05-01 CO) appears never to have been actually applied — the PI version it targeted still lacked the fix nine days later; `governance/population-taxonomy.md` and `governance/pre-decision-multimodal-access-armature.md` use inconsistent terminology ("impairment axes" never reconciled); `governance/legal-regulatory.md` remains explicitly blocked on counsel review that has no evidence of ever occurring; `governance/tier-system.md` references "PI v10.14 line 138" — a version not included in this audit's governance file set, confirming the PI evolved further than what was reviewed; the eight PI versions read (v10.7–v10.13, plus v10.14 read earlier in recon) show a pattern of same-week or next-day supersession, including one (v10.12) that self-admits "improperly bundling two unrelated content changes under one version label."

### 7.4 Decision Records (14 files, full detail in §5)

All 14 remaining DRs (`DR-2026-05-10` through `DR-2026-06-11-remove-colonial-role`) were read in full; findings are integrated into §3 and §5. Notable pattern: several DRs (`DR-2026-05-19`, `-20`, `-23`, `-24`, `-26`) show live DB-relevant work already executed and logged in the changelog while the DR's own status line still reads PROPOSED — a recurring "adopted-in-effect before formal ratification" pattern.

### 7.5 Audit reports (24 files)

Key cross-document findings: two independently-run "tier456 verification" reports (2026-04-23 and 2026-04-24) cover overlapping but different entry counts (264 vs 249) using different methodologies, with the discrepancy never reconciled in either file; two "Phase 2A jurisdiction audits" (2026-04 and 2026-04-24) likewise use different jurisdiction counts (46 vs 49) without cross-referencing each other; `audits/verification-coverage-catalog-2026-05-13b.md` is itself a self-critical honesty audit triggered by an owner challenge to a prior overconfident claim, finding roughly half the repository was never opened during the session it audits; `audits/accessibility-audit-2026-05-10.md` found the site's section-reordering feature is completely inert (no CSS ever reads the custom properties that would drive it).

---

## 8. Recommended Next Steps

Synthesizing §4–§6, in priority order:

1. **Resolve the core deliverable gap first.** `evidence_cell_state` is the single most load-bearing missing piece (§5, §4). Before any further evidence-collection or website work, decide whether to execute `workplan/best-practices-assessment-system.md`'s 5-phase build, and budget it honestly given the project's track record of underestimating session counts.
2. **Address DB reproducibility as a standing risk, not a closed issue.** The "job-owned tables" exemption (DR-2026-05-28) resolves the *symptom* but not the underlying risk that the canonical data store cannot be rebuilt from its audit trail. Consider whether the direct-write path (`scripts/db.py`) should be deprecated entirely now that migration-based writes exist.
3. **Decide on a durable review mechanism.** With CI deleted and human review effectively absent (2 of 50 commits), the project relies entirely on the same model's self-checks to catch its own recurring bias pattern. Even a lightweight periodic external or human spot-check cadence (already recommended internally in `session_2026-05-09-co0009-gap-verify.md` and never confirmed as followed) would materially change the integrity profile.
4. **Fix the PI drift mechanism structurally, not just track it.** `decisions/PI-update-needed.md` documents the problem but the underlying cause — a manual copy-paste step required by the claude.ai Projects model — won't go away without either process discipline or (see next item) migrating off that model.
5. **Execute the Claude Code migration (§6) as an independent, low-risk workstream.** It is fully specified in this report, does not block or depend on Phase E or the Phase B website build, and would incidentally solve the PI-drift problem (CLAUDE.md and hooks live in the repo, not in an external chat setting) as a side effect.
6. **Reconcile or formally retire orphaned planning documents** (`opus-synthesis-queue.md`, `phase1b-part01-s15-expansion.md`, several others in §4 marked "unclear") so the workplan corpus doesn't accumulate more ambiguous, never-superseded-but-never-executed artifacts.
7. **Consider an unshallow git fetch** before any future audit that needs to make commit-level integrity claims — the current shallow clone caps confidence on authorship/history claims to a 6-week window.
