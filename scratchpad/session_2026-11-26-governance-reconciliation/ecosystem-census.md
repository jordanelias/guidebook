# Ecosystem census: documentation and instruction surface of /home/user/guidebook

Generated 2026-11-26 by a read-only sweep. Nothing in the repository was edited. Search method: `git ls-files`, `git grep` and `git log` (they see through `.ignore`). The Grep tool and ripgrep were NOT used for any completeness claim, because `.ignore` hides sessions/, audits/, references/search-log/, references/bpc/, versions/, _archived/, workplan/_superseded/ and transcripts/. Working tree was clean at the start (`git status --porcelain -- governance decisions skills .claude CLAUDE.md architecture` = 0 lines). SQLite was read through `file:data/guidebook.db?mode=ro`.

Headline figures, each with its command:
- Tracked files, whole repo: `git ls-files | wc -l` = 5138
- governance/ + decisions/ files examined for status and inbound pointers: 142 (`git ls-files governance/ decisions/ | wc -l` = 142)
- CLAUDE.md distinct tokens examined for paths: 118 (`python3 /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/claudemd.py`, line `TOTAL`)
- Retired-vocabulary active entries: 27 (`grep -c '  - id: RV-' governance/retired-vocabulary.yaml`)
- Skills: 26 flat (`git ls-files skills/ | wc -l`) + 22 under .claude/skills (`git ls-files .claude/skills | grep -c SKILL.md`)

Sections: 1 inventory; 2 CLAUDE.md pointers; 3 governance/decisions status and inbound pointers (3b flagged); 4 restatement homes; 5 retired vocabulary; 6 skills; 7 prose callers (not gated), listed separately; 8 nulls and unproven items.

## 1. Inventory of tracked non-code documents by directory
Commands: `git ls-files` per prefix, piped to `wc -l`; workplan subfolders: `git ls-files workplan/ | awk -F/ 'NF>2{print $2}' | sort | uniq -c`.

| directory | tracked files | command |
|---|---:|---|
| governance/ | 53 | `git ls-files governance/ \| wc -l` |
| decisions/ | 89 | `git ls-files decisions/ \| wc -l` |
| references/ | 360 | `git ls-files references/ \| wc -l` |
| architecture/ | 12 | `git ls-files architecture/ \| wc -l` |
| workplan/ | 323 | `git ls-files workplan/ \| wc -l` |
| working/ | 1 | `git ls-files working/ \| wc -l` |
| skills/ | 26 | `git ls-files skills/ \| wc -l` |
| sessions/ | 330 | `git ls-files sessions/ \| wc -l` |
| attestations/ | 155 | `git ls-files attestations/ \| wc -l` |
| .claude/agents/ | 3 | `git ls-files .claude/agents/ \| wc -l` |
| .claude/commands/ | 4 | `git ls-files .claude/commands/ \| wc -l` |
| .claude/skills/ | 22 | `git ls-files .claude/skills/ \| wc -l` |
| .claude/hooks/ | 2 | `git ls-files .claude/hooks/ \| wc -l` |
| references/ (top level only) | 34 | `git ls-files references/ \| awk -F/ 'NF==2' \| wc -l` |
| workplan/ top-level files | 71 | `git ls-files workplan/ \| awk -F/ 'NF==2' \| wc -l` |

workplan/ subfolders (file counts, from the command above): 2026-10-30-ramp-spec-pages 23, 2026-11-12-bidirectional-pipeline 154, _superseded 20, deprecated 16, pipeline-state-graph 39. [derived by the uniq command; these five numbers were copied from its output]

references/ top-level names: best-practices-compendium.md, bibliography-v11-draft.md, bpc-scope-review.md, case-study-compendium.md, citation-mining-register.md, citation-tagging-protocol.md, co1-verified-sources.json, co2-verified-sources.json, crpd-ratification-map.md, deep-dive-protocols.md, economics-sources.md, effort-guide.md, meta-analysis-feasibility-v2.md, methodology-evidence-hierarchy-mapping.md, methodology-native-alias-verification.md, native-alias-verification.md, parser-source-readiness.md, phase-b-handoff.md, project-standards.md, search-log.md, self-review-meta-v1.md, skill-registry.md, slug-registry.md, standards-registry.md, standards-supersession-tracker.md, theory-gap-analysis.md, throughline-analysis.md, throughline-audit-notes.md, tier1-verified-sources.json, tier2-verified-sources.json, tier3-verified-sources.json, tier456-verified-sources.json, toc.md, tooling-register.md

Sizes and first heading/Status line for governance/, decisions/, .claude/ and skills/ are in the file `inv_out.txt` (same scratchpad) and reproduced below (command: `python3 /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/inv.py`).

```
===  governance/
19274	governance/adversarial-use-framework.md	|H: # Adversarial-Use Framework	|S: **Status:** CANONICAL — A10 Session 1
29887	governance/armature_v3_review.md	|H: # Armature v3 — Tri-Lens Review: CRPD, UI/UX Accessibility, Usability	|S: **Status:** Sonnet-drafted critique applying CRPD treaty text, WCAG 2.2 / COGA, and general usability principles. Best-practice synthesis cl
43791	governance/armature_v4.md	|H: # Pre-Decision: Person-Profile Armature — Query Architecture for a Research-Grounded Built-Environment Design Reference	|S: **Status:** PRE-DECISION DRAFT — captured intent for Stage A formalization. NOT decision-quality. Sonnet-drafted; flagged for Opus synthesis
24287	governance/armature_v4_integration.md	|H: # Armature v4 + Resolutions — Workplan Judgment and Integration	|S: 
70351	governance/armature_v4_resolutions.md	|H: # Armature v4 — Open Question Resolution	|S: **Status:** Authoritative resolution for architectural and best-practice synthesis questions. Population-specific content decisions (naming,
18224	governance/audience-priority.md	|H: # Audience Priority	|S: **Status:** CANONICAL — locked at iter 4 cross-test pass (2026-04-26 05:29)
50303	governance/check-registry.yaml	|H: # THE ONE HOME OF THE no_floor VOCABULARY. Every `no_floor:` reason must OPEN with one of	|S: 
7003	governance/citation-mining-protocol-memo-2026-05-11.md	|H: # Citation-Mining Protocol Violation Memo	|S: **Status:** for owner review, decisions pending
45616	governance/co1-operational.md	|H: # Co-1 Operational Specification	|S: > **D-0157 amendment, 2026-08-05.** `verification_status` is a **binary standing**,
12518	governance/conceptual-model.md	|H: # A3 — Conceptual Model	|S: **Status:** SIGNED OFF 2026-04-26 · **Amended 2026-07-21** — entity codes renamed `E-##` → `ENT-##` to remove a namespace collision with `it
8878	governance/concurrent-write-architecture-proposal-2026-05-11.md	|H: # Concurrent-write architecture — proposal	|S: **Status:** Proposal — awaiting owner decision
75491	governance/context-map.yaml	|H: 	|S: 
12315	governance/decision-protocol.md	|H: # Decision Protocol	|S: **Status:** CANONICAL — A12 Session 1
3679	governance/doctrine-deltas.json	|H: 	|S: 
19772	governance/doctrine-recheck.md	|H: # Doctrine Recheck Cadence	|S: **Status:** CANONICAL — A13 Session 1
56426	governance/evidence-architecture.md	|H: # Evidence Architecture — the unified statement	|S: **Status:** CANONICAL — ratified by owner directive 2026-07-13 (see `decisions/RATIFICATION-RECORD-2026-07-13.md`); the single entry point t
52581	governance/evidence-methodology.md	|H: # Evidence Methodology	|S: > **D-0157 amendment, 2026-08-05.** `verification_status` is a **binary standing**,
33290	governance/functional-taxonomy.md	|H: # Functional Taxonomy — Two-Layer Model (Axes × Profiles)	|S: **Status: RATIFIED — owner directive "Ratify all", 2026-07-21. Doctrine OPERATIVE;
10869	governance/grounds.md	|H: # How This Project Thinks	|S: **Status: RATIFIED — owner directive "Ratify all", 2026-07-21. OPERATIVE (doctrine);
26721	governance/held-tensions.md	|H: # Held Tensions Register	|S: **Status: RATIFIED — owner directive "Ratify all", 2026-07-21. OPERATIVE (doctrine).**
9713	governance/jurisdiction-philosophy.md	|H: # Jurisdiction Philosophy	|S: **Status:** CANONICAL — A8 Session 1
29256	governance/legal-regulatory.md	|H: # Legal and Regulatory Framework	|S: **Status:** CANONICAL — A11 Session 1
7443	governance/migration-based-writes-adopted-2026-05-11.md	|H: # Migration-based DB writes — adopted	|S: **Status:** Adopted
26386	governance/migration-survival.md	|H: # Migration Survival Register	|S: **Status:** CANONICAL — adopted by project owner 2026-05-02 01:37 (instruction "perform all" in audit-remediation continuation session)
4136	governance/mining-screens.yaml	|H: # Named, versioned screens for citation-mining relevance counts.	|S: 
13886	governance/mission-PROVISIONAL.md	|H: # Mission Statement (PROVISIONAL)	|S: **Status:** PROVISIONAL — committed 2026-04-26 02:42 UTC per Stage 0.6; revised 2026-04-26 03:45 UTC per pre-launch solo correction
21224	governance/mission-and-epistemics.md	|H: # Mission and Epistemic Commitments	|S: **Status:** CANONICAL — locked at iter 4 cross-test pass (2026-04-26 05:29). Supersedes `governance/mission-PROVISIONAL.md`.
85459	governance/owner-browser.yaml	|H: # governance/owner-browser.yaml -- what the owner's browser page says about each table, and what it lists as waiting on 	|S: 
8703	governance/pi-revision-co.md	|H: # Change Order — project-instructions (PI) revision sweep	|S: **Status:** PROPOSAL — project-owner-applied; not auto-applied
27351	governance/pipeline-contract.yaml	|H: # Header follows decisions/DR-2026-07-13-pipeline-contract.md: status ACCEPTED (doctrine) on the owner's	|S: status: ACCEPTED
8443	governance/pipeline-operations.md	|H: # Pipeline operations — what each one consumes, produces, and logs	|S: **Status:** PROPOSED · **Date:** 2026-08-02 · **Scope:** definitional
11388	governance/population-taxonomy.md	|H: # Population Taxonomy	|S: **Status:** SUPERSEDED (population code set) — see banner below. Structural detail retained pending full rewrite.
7063	governance/pre-decision-multimodal-access-armature.md	|H: # Pre-Decision: Multimodal Access Armature — Website Navigation Architecture	|S: **Status:** PRE-DECISION (captures design intent for A7+ formalization)
16741	governance/pre-stage-a-decisions.md	|H: # Pre-Stage-A Doctrinal Decisions	|S: **Status:** CANONICAL — retroactively marked at A12 S2 finding RC-001 resolution (2026-04-30)
442	governance/project-instructions-v10_10.md	|H: # Project Instructions v10.10 — ARCHIVED (moved)	|S: 
442	governance/project-instructions-v10_11.md	|H: # Project Instructions v10.11 — ARCHIVED (moved)	|S: 
442	governance/project-instructions-v10_12.md	|H: # Project Instructions v10.12 — ARCHIVED (moved)	|S: 
442	governance/project-instructions-v10_13.md	|H: # Project Instructions v10.13 — ARCHIVED (moved)	|S: 
21952	governance/project-instructions-v10_14.md	|H: # Project Instructions — Accessible Built Environments Guidebook	|S: - **V10.14 (2026-05-20)** — Two changes, after which future bootstrap drift no longer requires PI bumps. (1) **Standing rule #11 sub-(a) exp
440	governance/project-instructions-v10_7.md	|H: # Project Instructions v10.7 — ARCHIVED (moved)	|S: 
440	governance/project-instructions-v10_8.md	|H: # Project Instructions v10.8 — ARCHIVED (moved)	|S: 
440	governance/project-instructions-v10_9.md	|H: # Project Instructions v10.9 — ARCHIVED (moved)	|S: 
8258	governance/repo-strategy-revision-co.md	|H: # Repo Strategy Revision — Change Order Proposal-of-Record	|S: **Status:** PROPOSED — pending project-owner application
4156	governance/repo-strategy.md	|H: # Repo Strategy — CO-0007 Stage 0.8	|S: **Status:** Decision committed
698	governance/research-contract-baseline.json	|H: 	|S: 
19986	governance/research-contract.yaml	|H: # research-contract.yaml — the single source for the research contract.	|S: # STATUS: OPERATIVE. Adopted per DR-2026-07-25-research-contract-mechanical-enforcement
57876	governance/retired-vocabulary.yaml	|H: # retired-vocabulary.yaml — tokens that are READABLE AND WRONG.	|S: # STATUS: OPERATIVE. Consumed by scripts/audit/retired_vocabulary_audit.py, which
1480	governance/schema-reference-exemptions.yaml	|H: # Exemptions for scripts/audit/schema_reference_audit.py.	|S: 
8957	governance/stage-map.yaml	|H: # governance/stage-map.yaml — which pipeline stage each table belongs to.	|S: 
16183	governance/tier-system.md	|H: # Tier system — canonical definition	|S: **Status:** OPERATIVE — 2026-05-25; amended 2026-07-20 (§8–§10 added; §3 binary rule superseded).
19784	governance/time-model.md	|H: # Time Model	|S: **Status:** CANONICAL — A9 Session 1
3307	governance/userPreferences-v6.2-deltas.md	|H: # userPreferences v6.2 — Adherence Logging Deltas	|S: **Status:** repo-side reference copy. Live deployment: paste into claude.ai project settings.
10444	governance/workplan-adoption.md	|H: # CO-0007 Workplan Adoption Decision	|S: 
===  decisions/
4332	decisions/DR-2026-05-09-adversarial-research-protocol.md	|H: # Decision Record: Adopt Adversarial Research Protocol v2	|S: **Status:** ADOPTED 2026-05-09 — owner directive: "whatever makes sense for long-term integrity and health"
7171	decisions/DR-2026-05-10-progressive-measurement-protocol.md	|H: # Decision Record: Adopt Progressive Measurement Probe (PMP) Protocol	|S: **Status:** ADOPTED 2026-05-10 — owner directive: "proceed" (session 2026-05-10c)
23845	decisions/DR-2026-05-13-evidence-verification-methodology.md	|H: # Decision Record: Evidence Verification Methodology — Existence vs. Claim	|S: **Status:** ADOPTED 2026-05-13 — owner directive: "whatever is in best interest of project long-term, do" (session 2026-05-13b, after resear
18367	decisions/DR-2026-05-15-migration-history-drift-repair.md	|H: # Decision Record: Migration-History Drift — Repair Strategy	|S: **Status:** ADOPTED — Option B (Baseline Reset). Applied 2026-05-15 by owner via commits `d5449e8f` (baseline 012), `5026e827` (`migrate_db.
8734	decisions/DR-2026-05-18-statutory-metadata-completeness.md	|H: # Decision Record: Statutory Metadata Completeness — `COMPLETE-STATUTORY`	|S: **Status:** ADOPTED 2026-05-18 — owner directive 2026-05-18 in pilot session resumption: "A" (path A — new metadata_quality value preserving
39811	decisions/DR-2026-05-19-channel-2-manual-verification.md	|H: # Decision Record: Channel-2 Manual Verification Protocol (V2-manual)	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
8680	decisions/DR-2026-05-20-evidence-metadata-rehabilitation.md	|H: # DR-2026-05-20: Evidence metadata rehabilitation — type-routed protocol with mandatory cross-check	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
17656	decisions/DR-2026-05-23-cohort-manifest.json	|H: 	|S: 
8691	decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md	|H: # DR-2026-05-23: Pre-rehabilitation banner — cohort definition	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
14318	decisions/DR-2026-05-24-best-practice-supersession-protocol.md	|H: # DR-2026-05-24 — Best-Practice Supersession Protocol	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
16730	decisions/DR-2026-05-26-gap-driven-mining-protocol.md	|H: # DR-2026-05-26 — Gap-Driven Mining Protocol	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
8660	decisions/DR-2026-05-28-b-source-value-extractions-schema.md	|H: # DR-2026-05-28-b — `source_value_extractions` schema layer	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
4105	decisions/DR-2026-05-28-c-population-junctions-governance-close.md	|H: # DR-2026-05-28-c — Population-Junctions Governance Close (value-claim tables)	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
10268	decisions/DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation.md	|H: # DR-2026-05-28 — Migration-Ledger Drift & DB Reproducibility Reconciliation	|S: **Status:** ACCEPTED — option **3a** ratified by owner 2026-06-11 (see §Ratification). Step 2 (ledger backfill) was already executed in a pr
5621	decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md	|H: # DR-2026-05-29 — Evidence-Hierarchy Reconciliation (sr_meta@T2, tier=anchor-type, T1 composition, de-OT correction)	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
3453	decisions/DR-2026-06-10-e2g-reverification-scope.md	|H: # DR-2026-06-10 — E.2g Reverification Scope (full re-synthesis; prior text is a claim inventory, not salvageable prose)	|S: **Status:** RATIFIED 2026-06-10 (owner directive: "proceed with recommendations with care", ratifying Stage 4.3 plan §9 D-4.3-B).
3328	decisions/DR-2026-06-10-synthesis-model-floor.md	|H: # DR-2026-06-10 — Synthesis Model Floor (rule #2 is a capability floor, not a brand pin)	|S: **Status:** RATIFIED 2026-06-10 (owner directive: "proceed with recommendations with care", ratifying Stage 4.3 plan §9 D-4.3-A).
3463	decisions/DR-2026-06-11-remove-colonial-role.md	|H: # DR-2026-06-11: Remove COLONIAL from the lang_jur_map role taxonomy	|S: - Status: ACCEPTED
5040	decisions/DR-2026-07-12-decision-tracking-naming-and-schema-doc-currency.md	|H: # DR-2026-07-12: Decision-tracking naming disambiguation + schema-doc currency markers	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
8484	decisions/DR-2026-07-12-evidence-architecture-unification-impact-appendix.md	|H: # Impact appendix — DR-2026-07-12 evidence-architecture unification	|S: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-REC
21893	decisions/DR-2026-07-12-evidence-architecture-unification.md	|H: # DR-2026-07-12: Evidence-architecture unification — proposed resolution	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
11490	decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md	|H: # DR-2026-07-12: `evidence_cell_state` schema reconciliation — proposed resolution (v2)	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
5408	decisions/DR-2026-07-12-tier3-stated-threshold.md	|H: # DR-2026-07-12: Tier-3-alone `stated` threshold — proposed resolution	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
12914	decisions/DR-2026-07-12-versioning-and-archive-consolidation.md	|H: # DR-2026-07-12: PI archival hygiene, register-snapshot ban, archive consolidation, and handoff convention	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
11590	decisions/DR-2026-07-12-website-architecture-lock.md	|H: # DR-2026-07-12: Website architecture lock — proposed resolution (v2)	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
8010	decisions/DR-2026-07-13-attestation-rule-identifier-registry-gap.md	|H: # DR-2026-07-13: Attestation rule-identifier registry gap — proposed resolution	|S: - Status: **RATIFIED — owner directive 2026-07-21.** Executed by a later session (`project-pipeline-overview-xfpid1`), distinct from the 202
5166	decisions/DR-2026-07-13-integrity-protocol-three-modes.md	|H: # DR-2026-07-13: Integrity protocol — three-mode implementation of the adversarial-review lessons	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
13156	decisions/DR-2026-07-13-person-mode-functional-capacity-not-population-range.md	|H: # DR-2026-07-13: Person Mode is the individual's own functional capacity — not a position on a population range	|S: - Status: **APPLIED, but BLAST RADIUS INCOMPLETE — see `DR-2026-07-14-person-mode-governance-reconciliation.md`.** This DR corrected three s
12907	decisions/DR-2026-07-13-pipeline-contract.md	|H: # DR-2026-07-13: Pipeline contract — one machine-checkable stage-gate spec for evidence work	|S: - Status: **ACCEPTED (doctrine) — owner ratification "Yes, ratify ALL recent work", 2026-07-21; owner-action precondition OUTSTANDING (stage
16641	decisions/DR-2026-07-13-value-genealogy-and-derivation-handshake.md	|H: # DR-2026-07-13: Value genealogy + the function↔population derivation handshake — proposed resolution	|S: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECOR
9098	decisions/DR-2026-07-14-person-mode-governance-reconciliation.md	|H: # DR-2026-07-14: Person Mode reconciliation — completing the governance-file sweep the prior correction under-scoped	|S: - Status: **APPLIED (governance-only pass) — owner-directed** ("Governance-only first"). Completes the canonical-governance reconciliation o
7861	decisions/DR-2026-07-20-citation-mining-methodology-corrections.md	|H: # DR-2026-07-20 — Citation-Mining Methodology Corrections	|S: **Status:** ACCEPTED (session-adopted; corrections applied directly to the skill during the same session that found them)
8097	decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md	|H: # DR-2026-07-20 — Reconcile evidence-architecture.md with the weighted-strength anchor model	|S: **Status:** SUPERSEDED-BY `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md` — owner ruled **Option A** (with direction-a
20034	decisions/DR-2026-07-20-intra-category-cross-test.md	|H: # DR-2026-07-20: The intra-category cross-test — every specification adjudicated against its category-siblings before de	|S: - Status: **ACCEPTED — owner ratification "Yes, ratify ALL recent work", 2026-07-21; forks X2 (functional-neighbourhood granularity) and X5 
8469	decisions/DR-2026-07-20-weighted-strength-anchor-model.md	|H: # DR-2026-07-20 — Weighted-strength anchor model, review-species tiering, practitioner practice-stream	|S: **Status:** OPERATIVE — 2026-07-20
4732	decisions/DR-2026-07-21-entity-code-namespace-rename.md	|H: # DR-2026-07-21 — Rename entity codes `E-##` → `ENT-##` to end the item_code collision	|S: **Status:** OPERATIVE — 2026-07-21.
14561	decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md	|H: # DR-2026-07-21 — Evidence-architecture Option A execution: weak-anchor reconciliation with the weighted-strength model	|S: **Status:** OPERATIVE — by owner directive 2026-07-21 (finding F1, Option A ratified).
6333	decisions/DR-2026-07-21-held-tensions-register.md	|H: # DR-2026-07-21 — Held-tensions register and public grounds section	|S: - Status: **ACCEPTED — owner ratification "Ratify all", 2026-07-21.** Doctrine operative (held-tensions.md, grounds.md); see `decisions/RATI
9048	decisions/DR-2026-07-21-product-posture-thinking-tool-not-authority.md	|H: # DR-2026-07-21: Product posture — the Guidebook adjudicates evidence and declines authority	|S: - Status: **RATIFIED — owner directive 2026-07-21** (merge of PR #46 + explicit owner ratification; independently reaffirmed by the "Yes, ra
13774	decisions/DR-2026-07-21-re-attestation-materiality-and-window.md	|H: # DR-2026-07-21: Re-attestation by materiality triage — discharging the doctrine-change attestation debt without launder	|S: - Status: **RATIFIED (mechanism) — owner directive 2026-07-21.** M1 (materiality triage), M3 (schema `reattestation` block — shipped PR #43)
7277	decisions/DR-2026-07-21-tier-doctrine-source-class-consistency.md	|H: # DR-2026-07-21: Tier-doctrine consistency for four source classes (+ Steinfeld DOI-error)	|S: - Status: **RATIFIED — owner directive 2026-07-21.** Surfaced by the same-DOI dedup batch
7669	decisions/DR-2026-07-21-two-layer-functional-taxonomy.md	|H: # DR-2026-07-21 — Two-layer functional taxonomy: axes × profiles	|S: - Status: **ACCEPTED — owner ratification "Ratify all", 2026-07-21.** Doctrine operative (functional-taxonomy.md v1.2 incl. §0.5); DB execut
9926	decisions/DR-2026-07-22-population-representation-reconciliation.md	|H: # DR-2026-07-22 — Population-representation reconciliation: one canonical code set across enum, DB, and the axis layer	|S: ratified-but-unimplemented sweep, using the `SUPERSEDED` status retained by D-0163.
5343	decisions/DR-2026-07-22-work-from-axes.md	|H: # DR-2026-07-22 — Work from axes; no armchair umbrellas (population-coding discipline)	|S: - Status: **ADOPTED — owner directive 2026-07-22** ("work from axes"; "ensure you find
6330	decisions/DR-2026-07-23-population-schema-replace.md	|H: # DR-2026-07-23 — Retire the disability-population code schema; replace with the Access-Taxonomy Axis-2 set	|S: - Status: **ADOPTED — owner directive 2026-07-23** ("retire existing code schema for
8965	decisions/DR-2026-07-24-lang-jur-map-roles.md	|H: # DR-2026-07-24 — `lang_jur_map` role definitions + population (PROPOSAL, owner-to-decide)	|S: - Status: **PROPOSED — DG-NON. Owner decides; this agent proposes only.** No register entry
12737	decisions/DR-2026-07-24-search-executions-substrate.md	|H: # DR-2026-07-24 — `search_executions` logged-search substrate (coverage-loop memory)	|S: - **RATIFIED — owner directive 2026-07-24 ("Ratify all").** Register D-0151 `review_status:
18490	decisions/DR-2026-07-25-controlled-vocabulary-grouping-and-provenance.md	|H: # DR-2026-07-25 — Controlled-vocabulary grouping, token-based retrieval, and alias provenance	|S: - Status: **RATIFIED — owner directive 2026-07-25 ("ratify"), per the merge-implies-ratification
13658	decisions/DR-2026-07-25-rendered-document-integrity-gate.md	|H: # DR-2026-07-25 — Rendered-document integrity gate, and four rules the E-08 audits earned	|S: - Status: ~~**PROPOSED**~~ → **RATIFIED BY MERGE — DG-REVIEW §2–§4 (above); §5 is
9165	decisions/DR-2026-07-25-research-contract-mechanical-enforcement.md	|H: # DR-2026-07-25 — The research contract: mechanical enforcement of research validity	|S: - Status: **ADOPTED — owner directive 2026-07-24/25**, verbatim: *"OUR RESEARCH IS INVALID IF IT
6154	decisions/DR-2026-08-01-research-contract-single-source.md	|H: # DR-2026-08-01 — Research contract: single source, and three divergences resolved	|S: **Status:** ACCEPTED
26665	decisions/DR-2026-08-04-verification-status-is-a-standing-not-a-history.md	|H: # DR-2026-08-04 — `verification_status` is a standing, not a history	|S: # DR-2026-08-04 — `verification_status` is a standing, not a history
7701	decisions/DR-2026-08-06-clean-room-evidence-reset.md	|H: # DR-2026-08-06 — Clean-room evidence reset: the frame stays, the corpus becomes reference	|S: **Status:** ADOPTED, 2026-08-06 · **Decided by:** owner
7856	decisions/DR-2026-08-06-cold-storage-search-scope.md	|H: # DR-2026-08-06 — Cold storage: hide frozen records from agent search, not from code	|S: - Status: **ADOPTED — owner directive 2026-08-06.** The owner asked, in their own words,
9248	decisions/DR-2026-08-12-migration-history-baseline.md	|H: # DR-2026-08-12 — Freeze and archive the migration history; compress it into a full baseline	|S: **Status:** OPERATIVE — 2026-08-12.
3947	decisions/DR-2026-08-12-specification-curator-rename.md	|H: # DR-2026-08-12 — Rename the skill `cell-curator` → `specification-curator`	|S: **Status:** OPERATIVE — 2026-08-12.
6123	decisions/DR-2026-08-12-specification-rename-and-replay-order.md	|H: # DR-2026-08-12 — Rename the (item × population) determination to `specification`, and make migration replay order faith	|S: **Status:** OPERATIVE — 2026-08-12.
13304	decisions/DR-2026-08-14-status-vocabulary-ratification.md	|H: # DR-2026-08-14 — One ratified status vocabulary for decisions and conflicts	|S: # DR-2026-08-14 — One ratified status vocabulary for decisions and conflicts
5944	decisions/DR-2026-08-14-tier-1-retirement-batch.md	|H: # DR-2026-08-14 — The Tier-1 retirement batch	|S: **Status:** OPERATIVE — 2026-08-14 (executed 2026-08-15).
4179	decisions/DR-2026-08-15-superseded-status-retained.md	|H: # DR-2026-08-15 — `SUPERSEDED` is retained as a status value	|S: # DR-2026-08-15 — `SUPERSEDED` is retained as a status value
76673	decisions/DR-2026-08-19-research-restart-operative-instrument.md	|H: # DR-2026-08-19 — The operative instrument: restart research, end the loop	|S: 
22572	decisions/DR-2026-08-24-scaffolding-is-phase-specific.md	|H: # DR-2026-08-24 — Scaffolding is phase-specific; only table data crosses a stage boundary	|S: **Status:** **RATIFIED BY MERGE 2026-08-24** — PR #114, `main` at `84912b1`, per the merge-implies-
2773	decisions/DR-2026-08-27-base-building-three-levels-items-is-not-one.md	|H: # DR-2026-08-27 — base_building holds three levels -- building type, room type, construction element -- and `items` is n	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2690	decisions/DR-2026-08-27-base-sources-is-a-target-registry.md	|H: # DR-2026-08-27 — base_sources is a registry of research TARGETS -- prompts for where to look. It is neither evidence no	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
3364	decisions/DR-2026-08-27-concept-vocabulary-harvested-at-evidence-adjudicated-at-judgment.md	|H: # DR-2026-08-27 — The concept vocabulary is harvested at evidence and adjudicated at judgment. DR-2026-08-24 §2.4 deferr	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2755	decisions/DR-2026-08-27-evidence-is-the-source-judgment-is-the-extraction.md	|H: # DR-2026-08-27 — The evidence item is the SOURCE; the judgment item is the extracted, tiered, categorised value. Eviden	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2622	decisions/DR-2026-08-27-four-taxonomies-are-browsing-lenses.md	|H: # DR-2026-08-27 — The four disability taxonomies are user-selectable browsing lenses, and the medical model is included	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2888	decisions/DR-2026-08-27-naming-grammar-underscore-icf-family-singular-stage-ids.md	|H: # DR-2026-08-27 — The naming grammar: underscore separator, `base_` prefix, parallel `base_taxonomy_*` names, the `icf_*	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2697	decisions/DR-2026-08-27-relevance-is-adjudicated-at-collection.md	|H: # DR-2026-08-27 — Relevance is an adjudication made at evidence collection, against a topic; applicability remains a syn	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
3010	decisions/DR-2026-08-27-seven-stage-spine-base-is-first.md	|H: # DR-2026-08-27 — The pipeline is SEVEN stages and `base` is the first: Base, Research, Evidence, Judgment, Synthesis, S	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2859	decisions/DR-2026-08-31-a18-applies-to-deaf-aut-ndv-dem.md	|H: # DR-2026-08-31-a18-applies-to-deaf-aut-ndv-dem — OD-C: A-18 'RT60 in Occupied Learning and Listening Spaces' applies to	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2606	decisions/DR-2026-08-31-adversarial-subject-waiver-ratified-narrowly.md	|H: # DR-2026-08-31-adversarial-subject-waiver-ratified-narrowly — OD-F: the adversarial-subject waiver is RATIFIED ONCE, NA	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
3358	decisions/DR-2026-08-31-co1-warrant-must-name-the-co-production.md	|H: # DR-2026-08-31-co1-warrant-must-name-the-co-production — OD-D: a Co-1 tier is unwarranted-pending unless co1_provenance	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2546	decisions/DR-2026-08-31-deaf-and-com-belong-on-room-acoustic-performance.md	|H: # DR-2026-08-31-deaf-and-com-belong-on-room-acoustic-performance — OD-B: deaf and hard-of-hearing people belong on room-	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
3489	decisions/DR-2026-08-31-item-population-links-are-substrate-provisionally.md	|H: # DR-2026-08-31-item-population-links-are-substrate-provisionally — OD-A: item_population_links are SUBSTRATE, provision	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2603	decisions/DR-2026-08-31-ref-00967-already-t3.md	|H: # DR-2026-08-31-ref-00967-already-t3 — OD-E: REF-00967 belongs at T3, not T1. Measured already T3 -- the ruling is satis	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2722	decisions/DR-2026-08-31-strike-jurisdictional-values-clause.md	|H: # DR-2026-08-31-strike-jurisdictional-values-clause — OD-G: strike DR §12.1 Step 10's jurisdictional_values clause, and 	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
3270	decisions/DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md	|H: # DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many — A taxonomy link may be ABSENT from a lens, MUST tie to at	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2730	decisions/DR-2026-09-01-rationale-ref-points-at-the-decision.md	|H: # DR-2026-09-01-rationale-ref-points-at-the-decision — rationale_ref points at the DECISION that authorises the edge -- 	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
5057	decisions/DR-2026-09-01-the-lens-is-a-column-not-a-traversal.md	|H: # DR-2026-09-01-the-lens-is-a-column-not-a-traversal — The lens is a COLUMN, not a traversal: one item×taxonomy link tab	|S: **Status:** **ADOPTED, REVIEW PENDING** — a `DG-REVIEW` decision taken by a session under
3113	decisions/DR-2026-09-02-finish-the-render-sweep.md	|H: # DR-2026-09-02-finish-the-render-sweep — Finish the render sweep: archive the site surfaces that publish the deleted it	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
4008	decisions/DR-2026-09-02-restore-research-code-leads.md	|H: # DR-2026-09-02-restore-research-code-leads — Restore the 83 archived code/standard leads as research_code_leads, execut	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
2950	decisions/DR-2026-09-02-strike-the-item-frame-pull.md	|H: # DR-2026-09-02-strike-the-item-frame-pull — Strike DR-2026-08-19 §12.1 step 2's item-frame query; replace it with an IC	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
3514	decisions/DR-2026-09-11-adjudication-delegated-medical-lens-enforced.md	|H: # DR-2026-09-11 — Adjudication is delegated for a named set of items, and the medical lens gets filled out	|S: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that a
107880	decisions/DR-2026-09-26-recurring-defect-shapes-remediation.md	|H: # DR-2026-09-26 (v2): Six recurring defect shapes. The pass gets a record, provenance gets an artefact, and research and	|S: > **STATUS: RATIFIED 2026-09-27** (`references/project-standards.md`, "Owner ruling 2026-09-27
11306	decisions/PI-update-needed.md	|H: # PI Deployment Queue	|S: **Pending deployment:** none on the bootstrap/rule track. Queued for the next legitimate PI bump (documentation-only, per "no PI bump unless
19177	decisions/RATIFICATION-PACKAGE-2026-07-12.md	|H: # Ratification package — 2026-07-12	|S: **Purpose:** one memo, one sitting. Every PROPOSED decision record in the repository (all **16** — RECOUNTED: status-header grep over `decis
2640	decisions/RATIFICATION-RECORD-2026-07-13.md	|H: # Ratification record — 2026-07-13	|S: - **B1–B7** the seven May-era DRs (B4 with its migration-015 status check noted as an execution item; B5 ratified rather than deferred per "
10363	decisions/RATIFICATION-RECORD-2026-07-21.md	|H: # Ratification record — 2026-07-21	|S: 
===  .claude/
6019	.claude/README.md	|H: # `.claude/` — what lives here and why	|S: 
6756	.claude/agents/antagonist.md	|H: 	|S: 
2194	.claude/agents/db-census.md	|H: 	|S: 
2177	.claude/agents/repo-sweep.md	|H: 	|S: 
3876	.claude/commands/adversarial.md	|H: 	|S: 
10338	.claude/commands/batch-done.md	|H: ## COVERAGE (read it; it does not fail)	|S: 
1754	.claude/commands/orient.md	|H: 	|S: 
3009	.claude/commands/session-open.md	|H: 	|S: 
3109	.claude/hooks/ensure-deps.sh	|H: #!/usr/bin/env bash	|S: 
20524	.claude/hooks/record-command.py	|H: #!/usr/bin/env python3	|S: 
9690	.claude/settings.json	|H: 	|S: 
5398	.claude/skills/bibliography-compiler/SKILL.md	|H: ## Schema Reference	|S: 
26534	.claude/skills/citation-miner/SKILL.md	|H: ## 0. Connector availability (read BEFORE mining)	|S: 
5642	.claude/skills/citation-verifier/SKILL.md	|H: ## Steps	|S: 
10128	.claude/skills/connection-discovery/SKILL.md	|H: # Connection Discovery	|S: 
3348	.claude/skills/content-gap-analyzer/SKILL.md	|H: ## Steps	|S: 
14319	.claude/skills/cross-population-conflict-mapper/SKILL.md	|H: ## 1. Conflict Domains	|S: cross-reference each other. Outputs a conflict matrix with resolution status
9974	.claude/skills/cross-reference-resolver/SKILL.md	|H: ## 1. Reference Pattern Inventory	|S: 
2232	.claude/skills/doctrine-recheck/SKILL.md	|H: ## 1. Automated Checks (via script)	|S: 
6796	.claude/skills/economics-researcher/SKILL.md	|H: ## Scope Boundary	|S: 
8761	.claude/skills/evidence-auditor/SKILL.md	|H: ## Evidence Strata	|S: 
7574	.claude/skills/find-and-replace/SKILL.md	|H: ## Stage 0 — Replacement Specification	|S: 
17997	.claude/skills/functional-deficit-researcher/SKILL.md	|H: ## 1. Concept	|S: 
26474	.claude/skills/gap-driven-mining/SKILL.md	|H: ## 0. Connector availability (read BEFORE mining)	|S: 
10956	.claude/skills/github-io/SKILL.md	|H: ## 1. BATCH READ — GraphQL (primary)	|S: 
2471	.claude/skills/jurisdiction-tracker/SKILL.md	|H: ## Jurisdictions in scope (§4.7.3)	|S: 
29443	.claude/skills/multilingual-research/SKILL.md	|H: ## Coverage axes — both must be satisfied independently	|S: 
7375	.claude/skills/prose-style-checker/SKILL.md	|H: ## Register Specification	|S: 
11987	.claude/skills/research-log-manager/SKILL.md	|H: ## Slug Resolution (all actions)	|S: CHECK (query slug status from SQLite + load BPC from GitHub), LOG (write search results
59172	.claude/skills/run-pipeline/SKILL.md	|H: ## 1. base — read before touching a source	|S: 
14732	.claude/skills/session-consolidator/SKILL.md	|H: ## Steps	|S: 
16279	.claude/skills/supersession-audit/SKILL.md	|H: ## 0. Connector availability (read BEFORE auditing)	|S: 
12531	.claude/skills/toc-editor/SKILL.md	|H: # toc-editor	|S: 
===  skills/
20574	skills/adversarial-research_SKILL.md	|H: # Skill: Adversarial Research Protocol	|S: status: active
5398	skills/bibliography-compiler_SKILL.md	|H: ## Schema Reference	|S: 
26534	skills/citation-miner_SKILL.md	|H: ## 0. Connector availability (read BEFORE mining)	|S: 
5642	skills/citation-verifier_SKILL.md	|H: ## Steps	|S: 
10128	skills/connection-discovery_SKILL.md	|H: # Connection Discovery	|S: 
3348	skills/content-gap-analyzer_SKILL.md	|H: ## Steps	|S: 
14319	skills/cross-population-conflict-mapper_SKILL.md	|H: ## 1. Conflict Domains	|S: cross-reference each other. Outputs a conflict matrix with resolution status
9974	skills/cross-reference-resolver_SKILL.md	|H: ## 1. Reference Pattern Inventory	|S: 
2232	skills/doctrine-recheck_SKILL.md	|H: ## 1. Automated Checks (via script)	|S: 
6796	skills/economics-researcher_SKILL.md	|H: ## Scope Boundary	|S: 
8761	skills/evidence-auditor_SKILL.md	|H: ## Evidence Strata	|S: 
15803	skills/evidence-metadata-rehabilitation_SKILL.md	|H: # Skill: Evidence Metadata Rehabilitation	|S: status: active
7574	skills/find-and-replace_SKILL.md	|H: ## Stage 0 — Replacement Specification	|S: 
17997	skills/functional-deficit-researcher_SKILL.md	|H: ## 1. Concept	|S: 
26474	skills/gap-driven-mining_SKILL.md	|H: ## 0. Connector availability (read BEFORE mining)	|S: 
10956	skills/github-io_SKILL.md	|H: ## 1. BATCH READ — GraphQL (primary)	|S: 
12450	skills/integrity-protocol_SKILL.md	|H: # SKILL: integrity-protocol — three-mode implementation of the adversarial-review lessons	|S: **Status:** ACTIVE — ratified by owner directive 2026-07-13 (`decisions/RATIFICATION-RECORD-2026-07-13.md`; DR ACCEPTED)
2471	skills/jurisdiction-tracker_SKILL.md	|H: ## Jurisdictions in scope (§4.7.3)	|S: 
29443	skills/multilingual-research_SKILL.md	|H: ## Coverage axes — both must be satisfied independently	|S: 
7375	skills/prose-style-checker_SKILL.md	|H: ## Register Specification	|S: 
11987	skills/research-log-manager_SKILL.md	|H: ## Slug Resolution (all actions)	|S: CHECK (query slug status from SQLite + load BPC from GitHub), LOG (write search results
59172	skills/run-pipeline_SKILL.md	|H: ## 1. base — read before touching a source	|S: 
14732	skills/session-consolidator_SKILL.md	|H: ## Steps	|S: 
16279	skills/supersession-audit_SKILL.md	|H: ## 0. Connector availability (read BEFORE auditing)	|S: 
12531	skills/toc-editor_SKILL.md	|H: # toc-editor	|S: 
44433	skills/voice-style_SKILL.md	|H: # Writing & Framing Skill — Guidebook for Accessible Design	|S:
```

Duplicate-skill check. Command: `cmp -s skills/<name>_SKILL.md .claude/skills/<name>/SKILL.md` for each of the 26 flat files. Result: 22 pairs byte-identical (`SAME`), 4 flat-only (adversarial-research_SKILL.md, evidence-metadata-rehabilitation_SKILL.md, integrity-protocol_SKILL.md, voice-style_SKILL.md). No `.claude/skills/<name>/` without a flat counterpart. Note the two copies carry different last-commit dates for identical bytes (see section 6).

## 2. Pointers named in CLAUDE.md
Command: `python3 /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/claudemd.py` (extracts every backticked token and bare path-shaped token from CLAUDE.md, tests existence in the working tree). Raw output saved in /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/claudemd_out.txt. 118 distinct tokens.

Basename resolution (command: `git ls-files | grep -E '(^|/)<name>$'`): check_commit_msg.py -> scripts/ci_helpers/check_commit_msg.py; ci.yml -> .github/workflows/ci.yml; research_contract_hook.py -> scripts/generate/research_contract_hook.py; run_checks.py -> scripts/run_checks.py; db.py -> scripts/db.py; ensure-deps.sh -> .claude/hooks/ensure-deps.sh; evidence-architecture.md -> governance/evidence-architecture.md; migrate_db.py -> scripts/migrate_db.py.

### 2a. Named paths that resolve to nothing in the tracked tree (BROKEN or non-path)

| CLAUDE.md line | token | finding |
|---|---|---|
| L350 | `index.html` | root index.html is NOT tracked (`git ls-files | grep -E '^index\.html$'` = 0). Exists only as `_archived/index.html`, `_archived/site/index.html`. BROKEN pointer. |
| L241 | `pipeline-map.yaml` | named as retired; only tracked copy is `_archived/governance/pipeline-map.yaml` (8 tracked files match `pipeline-map`). Intentional retirement reference, not a live path. |
| L90 | `ci.yml:257` | stale line pointer: `sed -n '257p' .github/workflows/ci.yml` is `with: {node-version: "20"}`; `check_commit_msg` is invoked at ci.yml line 274 (`grep -n check_commit_msg .github/workflows/ci.yml`). |
| L234 | `architecture/shape/pipelines/schema` | descriptive phrase in the Layer 1 ruling, not a path. |
| L236 | `tools/workflows/processes/scripts` | descriptive phrase in the Layer 2 ruling, not a path. |
| L372 | `policy/standards` | not a path: the token is the phrase "policy/standards only" in the marker legend. `git ls-files | grep -c '^policy/'` = 0. |
| L124 | `~/.claude/projects` | user-home path outside the repo. |
| L154 | `evidence/discovery-provenance` | a registry-style key name, not a file. |
| L462 | ``.md`` | a grammar fragment, not a file. |
| L421 | `/__agentproxy/status` | an endpoint, not a repo path. |
| L57-58 | `/adversarial, /batch-done, /orient, /session-open` | slash commands; they resolve to `.claude/commands/{adversarial,batch-done,orient,session-open}.md` (all 4 exist). |
| L215, L154, L408, L378 | `0/1/2, 16/640, Cloudflare/Bunny-Shield, ICF/access-need` | prose tokens, not paths. |
| L318 | `/tmp/rebuilt.db` | scratch path in a command example. |

Checked `scripts/migrations/NNN_slug.sql` (L317) and `scripts/migrations/data_*` (L117): placeholders; `git ls-files scripts/migrations | wc -l` = 280 total, `| grep -c '/data_'` = 169 data files.

### 2b. Named commands and scripts, existence
Command: `test -e <path>` and `git ls-files --error-unmatch`. Result: every named script exists — scripts/run_checks.py, scripts/db.py, scripts/preflight.sh, scripts/preserve_transcripts.py, scripts/bootstrap.sh, scripts/fix_stop_hook_loop.sh, scripts/emit_data_migration.py, scripts/migrate_db.py, scripts/research/emit_batch_sql.py, scripts/research/retrieval_log.py, scripts/audit/derived_not_curated_audit.py, scripts/audit/joined_cells_census.py, .claude/hooks/record-command.py, .claude/hooks/ensure-deps.sh, scripts/ci_helpers/check_commit_msg.py, scripts/generate/research_contract_hook.py. Flags: `grep -c -- '"--changed-from"' scripts/run_checks.py` = 5; `--list`, `--explain`, `--selftest`, `--battery`, `--kinds`, `--all` each found by the same grep pattern.

### 2c. Every CLAUDE.md token that resolves to an existing tracked path

| status | token | CLAUDE.md lines |
|---|---|---|
| EXISTS | `.claude/agents/` | L[55] |
| EXISTS | `.claude/commands/` | L[57] |
| EXISTS | `.claude/hooks/ensure-deps.sh` | L[34] |
| EXISTS | `.claude/hooks/record-command.py` | L[439] |
| EXISTS | `.claude/settings.json` | L[209] |
| EXISTS | `.claude/skills/` | L[59] |
| EXISTS | `.github/` | L[510] |
| MISSING | `.md` | L[462] |
| MISSING | `/__agentproxy/status` | L[421] |
| MISSING | `/adversarial` | L[57] |
| MISSING | `/batch-done` | L[58] |
| MISSING | `/orient` | L[57] |
| MISSING | `/session-open` | L[57] |
| MISSING | `0/1/2` | L[215] |
| MISSING | `16/640` | L[154] |
| MISSING | `Cloudflare/Bunny-Shield` | L[408] |
| MISSING | `ICF/access-need` | L[378] |
| EXISTS | `_archived/` | L[423, 451, 499, 500] |
| EXISTS | `_archived/references/part04-item-index.md` | L[458] |
| EXISTS | `architecture/` | L[159] |
| EXISTS | `architecture/project-architecture-guidebook-v2.3.md` | L[544] |
| MISSING | `architecture/shape/pipelines/schema` | L[234] |
| EXISTS | `audits/` | L[423] |
| MISSING | `check_commit_msg.py` | L[90] |
| MISSING | `ci.yml` | L[211] |
| MISSING | `ci.yml:257` | L[90] |
| EXISTS | `data/guidebook.db` | L[98, 221, 280, 285, 290, 332] |
| MISSING | `db.py` | L[214, 298] |
| EXISTS | `decisions/` | L[93] |
| EXISTS | `decisions/DR-2026-08-19-research-restart-operative-instrument.md` | L[21, 538] |
| MISSING | `ensure-deps.sh` | L[62] |
| MISSING | `evidence-architecture.md` | L[161] |
| MISSING | `evidence/discovery-provenance` | L[154] |
| EXISTS | `governance/` | L[158] |
| EXISTS | `governance/check-registry.yaml` | L[65, 195, 224, 520] |
| EXISTS | `governance/conceptual-model.md` | L[542] |
| EXISTS | `governance/decision-protocol.md` | L[543] |
| EXISTS | `governance/evidence-architecture.md` | L[541] |
| EXISTS | `governance/functional-taxonomy.md` | L[542] |
| EXISTS | `governance/mission-and-epistemics.md` | L[540] |
| EXISTS | `governance/pipeline-contract.yaml` | L[247] |
| EXISTS | `governance/tier-system.md` | L[367, 541] |
| MISSING | `index.html` | L[350] |
| MISSING | `origin/main` | L[43, 44, 49, 446, 485, 515] |
| MISSING | `pipeline-map.yaml` | L[241] |
| MISSING | `policy/standards` | L[372] |
| EXISTS | `references/` | L[159, 450] |
| EXISTS | `references/bpc/` | L[424, 451] |
| EXISTS | `references/connection-reasoning/` | L[92] |
| EXISTS | `references/project-standards.md` | L[240, 386, 392, 468, 539] |
| EXISTS | `references/search-log/` | L[424, 451] |
| MISSING | `research_contract_hook.py` | L[465] |
| MISSING | `run_checks.py` | L[163, 347, 521] |
| EXISTS | `schemas/` | L[510] |
| EXISTS | `schemas/attestation.schema.json` | L[94] |
| EXISTS | `scratchpad/CURRENT` | L[429] |
| EXISTS | `scripts/` | L[510] |
| EXISTS | `scripts/audit/derived_not_curated_audit.py` | L[191] |
| EXISTS | `scripts/audit/joined_cells_census.py` | L[310] |
| EXISTS | `scripts/bootstrap.sh` | L[469] |
| EXISTS | `scripts/db.py` | L[192, 288, 304] |
| EXISTS | `scripts/emit_data_migration.py` | L[99, 289] |
| EXISTS | `scripts/fix_stop_hook_loop.sh` | L[481] |
| EXISTS | `scripts/migrate_db.py` | L[99, 289] |
| EXISTS | `scripts/migrations` | L[515] |
| MISSING | `scripts/migrations/NNN_slug.sql` | L[317] |
| EXISTS | `scripts/preflight.sh` | L[43] |
| EXISTS | `scripts/preserve_transcripts.py` | L[122] |
| EXISTS | `scripts/research/emit_batch_sql.py` | L[289] |
| EXISTS | `scripts/research/retrieval_log.py` | L[357] |
| EXISTS | `scripts/run_checks.py` | L[35, 44, 45] |
| EXISTS | `sessions/` | L[93, 424, 425] |
| EXISTS | `sessions/LATEST` | L[430] |
| EXISTS | `skills/` | L[510] |
| MISSING | `tools/scripts` | L[234] |
| MISSING | `tools/workflows/processes/scripts` | L[236] |
| EXISTS | `transcripts/` | L[425] |
| EXISTS | `versions/` | L[424, 451] |
| EXISTS | `working/` | L[450] |
| EXISTS | `workplan/2026-09-16-infrastructure-remediation-brief.md` | L[146] |
| EXISTS | `workplan/_superseded/` | L[424] |
| MISSING | `~/.claude/projects` | L[124] |

`MISSING` rows in 2c are the tokens of 2a (non-paths, slash commands resolved in 2a, and bare basenames resolved above). Command: `python3 /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/claudemd.py`.

## 3. governance/ and decisions/: declared status and inbound pointers (142 files)
Command: `git ls-files governance/ decisions/` then for each path `git grep -l -F -- <path>`; ALL = hits excluding self, `transcripts/` and `sessions/` (the spec); LIVE-DOC = hits in CLAUDE.md, governance/, decisions/, skills/, .claude/, architecture/, schemas/, scripts/, data/, attestations/, workplan/ (excluding `_archived/`, `audits/`, `references/search-log/`, `references/bpc/`, `versions/`, `workplan/_superseded/`); SCRATCH = hits under `scratchpad/`; ARCH = hits under the archive/frozen paths. Status = first line in the first 15 lines matching `Status:|SUPERSEDED|HISTORICAL|DEPRECATED|RETIRED|ARCHIVED`.

| path | bytes | status line (first 15 lines) | ALL | LIVE-DOC | SCRATCH | ARCH |
|---|---:|---|---:|---:|---:|---:|
| decisions/DR-2026-05-09-adversarial-research-protocol.md | 4332 | L3: **Status:** ADOPTED 2026-05-09 — owner directive: "whatever makes sense for long-term integ | 19 | 4 | 10 | 4 |
| decisions/DR-2026-05-10-progressive-measurement-protocol.md | 7171 | L3: **Status:** ADOPTED 2026-05-10 — owner directive: "proceed" (session 2026-05-10c) | 10 | 1 | 5 | 3 |
| decisions/DR-2026-05-13-evidence-verification-methodology.md | 23845 | L3: **Status:** ADOPTED 2026-05-13 — owner directive: "whatever is in best interest of project  | 9 | 1 | 7 | 1 |
| decisions/DR-2026-05-15-migration-history-drift-repair.md | 18367 | L3: **Status:** ADOPTED — Option B (Baseline Reset). Applied 2026-05-15 by owner via commits `d | 10 | 0 | 10 | 0 |
| decisions/DR-2026-05-18-statutory-metadata-completeness.md | 8734 | L3: **Status:** ADOPTED 2026-05-18 — owner directive 2026-05-18 in pilot session resumption: "A | 5 | 0 | 5 | 0 |
| decisions/DR-2026-05-19-channel-2-manual-verification.md | 39811 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 10 | 1 | 9 | 0 |
| decisions/DR-2026-05-20-evidence-metadata-rehabilitation.md | 8680 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 7 | 2 | 5 | 0 |
| decisions/DR-2026-05-23-cohort-manifest.json | 17656 | NONE | 11 | 3 | 7 | 1 |
| decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md | 8691 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 9 | 3 | 6 | 0 |
| decisions/DR-2026-05-24-best-practice-supersession-protocol.md | 14318 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 30 | 6 | 23 | 0 |
| decisions/DR-2026-05-26-gap-driven-mining-protocol.md | 16730 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 22 | 4 | 17 | 0 |
| decisions/DR-2026-05-28-b-source-value-extractions-schema.md | 8660 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 5 | 1 | 4 | 0 |
| decisions/DR-2026-05-28-c-population-junctions-governance-close.md | 4105 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 4 | 1 | 3 | 0 |
| decisions/DR-2026-05-28-migration-ledger-and-reproducibility-reconciliation.md | 10268 | L3: **Status:** ACCEPTED — option **3a** ratified by owner 2026-06-11 (see §Ratification). Step | 8 | 5 | 3 | 0 |
| decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md | 5621 | L3: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 20 | 5 | 13 | 1 |
| decisions/DR-2026-06-10-e2g-reverification-scope.md | 3453 | L3: **Status:** RATIFIED 2026-06-10 (owner directive: "proceed with recommendations with care", | 9 | 2 | 7 | 0 |
| decisions/DR-2026-06-10-synthesis-model-floor.md | 3328 | L3: **Status:** RATIFIED 2026-06-10 (owner directive: "proceed with recommendations with care", | 20 | 4 | 16 | 0 |
| decisions/DR-2026-06-11-remove-colonial-role.md | 3463 | L3: - Status: ACCEPTED | 8 | 4 | 4 | 0 |
| decisions/DR-2026-07-12-decision-tracking-naming-and-schema-doc-currency.md | 5040 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 6 | 3 | 3 | 0 |
| decisions/DR-2026-07-12-evidence-architecture-unification-impact-appendix.md | 8484 | L2: **Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify | 21 | 2 | 19 | 0 |
| decisions/DR-2026-07-12-evidence-architecture-unification.md | 21893 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 40 | 10 | 28 | 1 |
| decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md | 11490 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 135 | 13 | 31 | 90 |
| decisions/DR-2026-07-12-tier3-stated-threshold.md | 5408 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 27 | 8 | 17 | 1 |
| decisions/DR-2026-07-12-versioning-and-archive-consolidation.md | 12914 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 9 | 4 | 5 | 0 |
| decisions/DR-2026-07-12-website-architecture-lock.md | 11590 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 6 | 3 | 3 | 0 |
| decisions/DR-2026-07-13-attestation-rule-identifier-registry-gap.md | 8010 | L3: - Status: **RATIFIED — owner directive 2026-07-21.** Executed by a later session (`project- | 21 | 3 | 16 | 0 |
| decisions/DR-2026-07-13-integrity-protocol-three-modes.md | 5166 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 5 | 2 | 3 | 0 |
| decisions/DR-2026-07-13-person-mode-functional-capacity-not-population-range.md | 13156 | L3: - Status: **APPLIED, but BLAST RADIUS INCOMPLETE — see `DR-2026-07-14-person-mode-governanc | 10 | 2 | 8 | 0 |
| decisions/DR-2026-07-13-pipeline-contract.md | 12907 | L3: - Status: **ACCEPTED (doctrine) — owner ratification "Yes, ratify ALL recent work", 2026-07 | 15 | 4 | 11 | 0 |
| decisions/DR-2026-07-13-value-genealogy-and-derivation-handshake.md | 16641 | L3: - Status: **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify a | 36 | 6 | 28 | 0 |
| decisions/DR-2026-07-14-person-mode-governance-reconciliation.md | 9098 | L3: - Status: **APPLIED (governance-only pass) — owner-directed** ("Governance-only first"). Co | 5 | 1 | 4 | 0 |
| decisions/DR-2026-07-20-citation-mining-methodology-corrections.md | 7861 | L3: **Status:** ACCEPTED (session-adopted; corrections applied directly to the skill during the | 2 | 0 | 2 | 0 |
| decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md | 8097 | L3: **Status:** SUPERSEDED-BY `decisions/DR-2026-07-21-evidence-architecture-option-a-execution | 32 | 3 | 29 | 0 |
| decisions/DR-2026-07-20-intra-category-cross-test.md | 20034 | L3: - Status: **ACCEPTED — owner ratification "Yes, ratify ALL recent work", 2026-07-21; forks  | 22 | 4 | 17 | 0 |
| decisions/DR-2026-07-20-weighted-strength-anchor-model.md | 8469 | L3: **Status:** OPERATIVE — 2026-07-20 | 30 | 6 | 24 | 0 |
| decisions/DR-2026-07-21-entity-code-namespace-rename.md | 4732 | L3: **Status:** OPERATIVE — 2026-07-21. | 5 | 3 | 2 | 0 |
| decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md | 14561 | L3: **Status:** OPERATIVE — by owner directive 2026-07-21 (finding F1, Option A ratified). | 58 | 11 | 47 | 0 |
| decisions/DR-2026-07-21-held-tensions-register.md | 6333 | L3: - Status: **ACCEPTED — owner ratification "Ratify all", 2026-07-21.** Doctrine operative (h | 6 | 2 | 4 | 0 |
| decisions/DR-2026-07-21-product-posture-thinking-tool-not-authority.md | 9048 | L3: - Status: **RATIFIED — owner directive 2026-07-21** (merge of PR #46 + explicit owner ratif | 35 | 8 | 27 | 0 |
| decisions/DR-2026-07-21-re-attestation-materiality-and-window.md | 13774 | L3: - Status: **RATIFIED (mechanism) — owner directive 2026-07-21.** M1 (materiality triage), M | 14 | 2 | 12 | 0 |
| decisions/DR-2026-07-21-tier-doctrine-source-class-consistency.md | 7277 | L3: - Status: **RATIFIED — owner directive 2026-07-21.** Surfaced by the same-DOI dedup batch | 10 | 4 | 6 | 0 |
| decisions/DR-2026-07-21-two-layer-functional-taxonomy.md | 7669 | L3: - Status: **ACCEPTED — owner ratification "Ratify all", 2026-07-21.** Doctrine operative (f | 5 | 3 | 2 | 0 |
| decisions/DR-2026-07-22-population-representation-reconciliation.md | 9926 | L3: - **SUPERSEDED — 2026-07-23, recorded 2026-08-15.** `DR-2026-07-23-population-schema-replac | 4 | 1 | 3 | 0 |
| decisions/DR-2026-07-22-work-from-axes.md | 5343 | L3: - Status: **ADOPTED — owner directive 2026-07-22** ("work from axes"; "ensure you find | 17 | 2 | 15 | 0 |
| decisions/DR-2026-07-23-population-schema-replace.md | 6330 | L3: - Status: **ADOPTED — owner directive 2026-07-23** ("retire existing code schema for | 16 | 6 | 10 | 0 |
| decisions/DR-2026-07-24-lang-jur-map-roles.md | 8965 | L9: - Status: **PROPOSED — DG-NON. Owner decides; this agent proposes only.** No register entry | 17 | 7 | 7 | 3 |
| decisions/DR-2026-07-24-search-executions-substrate.md | 12737 | L8: - Status: **PROPOSED — DG-REVIEW (agent decides, owner reviews before canonical).** | 11 | 4 | 4 | 3 |
| decisions/DR-2026-07-25-controlled-vocabulary-grouping-and-provenance.md | 18490 | L3: - Status: **RATIFIED — owner directive 2026-07-25 ("ratify"), per the merge-implies-ratific | 6 | 1 | 5 | 0 |
| decisions/DR-2026-07-25-rendered-document-integrity-gate.md | 13658 | L13: - Status: ~~**PROPOSED**~~ → **RATIFIED BY MERGE — DG-REVIEW §2–§4 (above); §5 is | 5 | 1 | 4 | 0 |
| decisions/DR-2026-07-25-research-contract-mechanical-enforcement.md | 9165 | L3: - Status: **ADOPTED — owner directive 2026-07-24/25**, verbatim: *"OUR RESEARCH IS INVALID  | 10 | 4 | 3 | 3 |
| decisions/DR-2026-08-01-research-contract-single-source.md | 6154 | L5: **Status:** ACCEPTED | 7 | 2 | 5 | 0 |
| decisions/DR-2026-08-04-verification-status-is-a-standing-not-a-history.md | 26665 | L3: - Status: **ADOPTED — owner directive 2026-08-04 ("ratify all, dispatch resolver").** Ratif | 22 | 5 | 12 | 5 |
| decisions/DR-2026-08-06-clean-room-evidence-reset.md | 7701 | L5: **Status:** ADOPTED, 2026-08-06 · **Decided by:** owner | 23 | 5 | 18 | 0 |
| decisions/DR-2026-08-06-cold-storage-search-scope.md | 7856 | L3: - Status: **ADOPTED — owner directive 2026-08-06.** The owner asked, in their own words, | 18 | 6 | 11 | 0 |
| decisions/DR-2026-08-12-migration-history-baseline.md | 9248 | L3: **Status:** OPERATIVE — 2026-08-12. | 8 | 3 | 3 | 2 |
| decisions/DR-2026-08-12-specification-curator-rename.md | 3947 | L3: **Status:** OPERATIVE — 2026-08-12. | 8 | 3 | 3 | 1 |
| decisions/DR-2026-08-12-specification-rename-and-replay-order.md | 6123 | L3: **Status:** OPERATIVE — 2026-08-12. | 11 | 4 | 5 | 2 |
| decisions/DR-2026-08-14-status-vocabulary-ratification.md | 13304 | L3: **Status:** OPERATIVE — 2026-08-14 (implemented 2026-08-15 by schema migration 058). | 9 | 4 | 4 | 1 |
| decisions/DR-2026-08-14-tier-1-retirement-batch.md | 5944 | L3: **Status:** OPERATIVE — 2026-08-14 (executed 2026-08-15). | 8 | 3 | 4 | 1 |
| decisions/DR-2026-08-15-superseded-status-retained.md | 4179 | L1: # DR-2026-08-15 — `SUPERSEDED` is retained as a status value | 8 | 3 | 4 | 1 |
| decisions/DR-2026-08-19-research-restart-operative-instrument.md | 76673 | NONE | 87 | 29 | 56 | 2 |
| decisions/DR-2026-08-24-scaffolding-is-phase-specific.md | 22572 | L3: **Status:** **RATIFIED BY MERGE 2026-08-24** — PR #114, `main` at `84912b1`, per the merge- | 23 | 8 | 15 | 0 |
| decisions/DR-2026-08-27-base-building-three-levels-items-is-not-one.md | 2773 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 12 | 7 | 4 | 1 |
| decisions/DR-2026-08-27-base-sources-is-a-target-registry.md | 2690 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 13 | 7 | 5 | 1 |
| decisions/DR-2026-08-27-concept-vocabulary-harvested-at-evidence-adjudicated-at-judgment.md | 3364 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 14 | 7 | 6 | 1 |
| decisions/DR-2026-08-27-evidence-is-the-source-judgment-is-the-extraction.md | 2755 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 22 | 9 | 12 | 1 |
| decisions/DR-2026-08-27-four-taxonomies-are-browsing-lenses.md | 2622 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 16 | 8 | 7 | 1 |
| decisions/DR-2026-08-27-naming-grammar-underscore-icf-family-singular-stage-ids.md | 2888 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 10 | 6 | 3 | 1 |
| decisions/DR-2026-08-27-relevance-is-adjudicated-at-collection.md | 2697 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 14 | 6 | 7 | 1 |
| decisions/DR-2026-08-27-seven-stage-spine-base-is-first.md | 3010 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 13 | 7 | 5 | 1 |
| decisions/DR-2026-08-31-a18-applies-to-deaf-aut-ndv-dem.md | 2859 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 12 | 7 | 4 | 1 |
| decisions/DR-2026-08-31-adversarial-subject-waiver-ratified-narrowly.md | 2606 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 11 | 6 | 4 | 1 |
| decisions/DR-2026-08-31-co1-warrant-must-name-the-co-production.md | 3358 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 21 | 8 | 12 | 1 |
| decisions/DR-2026-08-31-deaf-and-com-belong-on-room-acoustic-performance.md | 2546 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 12 | 7 | 4 | 1 |
| decisions/DR-2026-08-31-item-population-links-are-substrate-provisionally.md | 3489 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 11 | 6 | 4 | 1 |
| decisions/DR-2026-08-31-ref-00967-already-t3.md | 2603 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 13 | 6 | 6 | 1 |
| decisions/DR-2026-08-31-strike-jurisdictional-values-clause.md | 2722 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 14 | 6 | 7 | 1 |
| decisions/DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md | 3270 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 20 | 6 | 13 | 1 |
| decisions/DR-2026-09-01-rationale-ref-points-at-the-decision.md | 2730 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 12 | 6 | 5 | 1 |
| decisions/DR-2026-09-01-the-lens-is-a-column-not-a-traversal.md | 5057 | L3: **Status:** **ADOPTED, REVIEW PENDING** — a `DG-REVIEW` decision taken by a session under | 21 | 8 | 12 | 1 |
| decisions/DR-2026-09-02-finish-the-render-sweep.md | 3113 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 12 | 6 | 5 | 1 |
| decisions/DR-2026-09-02-restore-research-code-leads.md | 4008 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 15 | 7 | 7 | 1 |
| decisions/DR-2026-09-02-strike-the-item-frame-pull.md | 2950 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 11 | 6 | 4 | 1 |
| decisions/DR-2026-09-11-adjudication-delegated-medical-lens-enforced.md | 3514 | L3: **Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds | 13 | 5 | 8 | 0 |
| decisions/DR-2026-09-26-recurring-defect-shapes-remediation.md | 107880 | NONE | 23 | 8 | 15 | 0 |
| decisions/PI-update-needed.md | 11306 | NONE | 28 | 11 | 13 | 4 |
| decisions/RATIFICATION-PACKAGE-2026-07-12.md | 19177 | L10: > **SUPERSEDED IN PART — appended 2026-11-19, not edited.** As to excluding the code-only  | 31 | 5 | 26 | 0 |
| decisions/RATIFICATION-RECORD-2026-07-13.md | 2640 | NONE | 45 | 29 | 14 | 2 |
| decisions/RATIFICATION-RECORD-2026-07-21.md | 10363 | NONE | 28 | 10 | 17 | 1 |
| governance/adversarial-use-framework.md | 19274 | L2: **Status:** CANONICAL — A10 Session 1 | 60 | 15 | 35 | 10 |
| governance/armature_v3_review.md | 29887 | L6: **Status:** Sonnet-drafted critique applying CRPD treaty text, WCAG 2.2 / COGA, and general | 23 | 7 | 15 | 1 |
| governance/armature_v4.md | 43791 | L3: **Status:** PRE-DECISION DRAFT — captured intent for Stage A formalization. NOT decision-qu | 30 | 11 | 18 | 1 |
| governance/armature_v4_integration.md | 24287 | NONE | 15 | 1 | 14 | 0 |
| governance/armature_v4_resolutions.md | 70351 | L5: **Status:** Authoritative resolution for architectural and best-practice synthesis question | 24 | 7 | 17 | 0 |
| governance/audience-priority.md | 18224 | L2: **Status:** CANONICAL — locked at iter 4 cross-test pass (2026-04-26 05:29) | 55 | 24 | 26 | 5 |
| governance/check-registry.yaml | 50303 | NONE | 327 | 166 | 146 | 13 |
| governance/citation-mining-protocol-memo-2026-05-11.md | 7003 | L4: **Status:** for owner review, decisions pending | 17 | 0 | 13 | 4 |
| governance/co1-operational.md | 45616 | NONE | 94 | 31 | 53 | 7 |
| governance/conceptual-model.md | 12518 | L4: **Status:** SIGNED OFF 2026-04-26 · **Amended 2026-07-21** — entity codes renamed `E-##` →  | 75 | 23 | 41 | 11 |
| governance/concurrent-write-architecture-proposal-2026-05-11.md | 8878 | L5: **Status:** Proposal — awaiting owner decision | 8 | 2 | 4 | 2 |
| governance/context-map.yaml | 75491 | NONE | 162 | 69 | 91 | 2 |
| governance/decision-protocol.md | 12315 | L2: **Status:** CANONICAL — A12 Session 1 | 128 | 55 | 63 | 10 |
| governance/doctrine-deltas.json | 3679 | NONE | 45 | 17 | 28 | 0 |
| governance/doctrine-recheck.md | 19772 | L2: **Status:** CANONICAL — A13 Session 1 | 41 | 15 | 19 | 6 |
| governance/evidence-architecture.md | 56426 | L2: **Status:** CANONICAL — ratified by owner directive 2026-07-13 (see `decisions/RATIFICATION | 175 | 67 | 97 | 9 |
| governance/evidence-methodology.md | 52581 | NONE | 159 | 52 | 92 | 12 |
| governance/functional-taxonomy.md | 33290 | L3: **Status: RATIFIED — owner directive "Ratify all", 2026-07-21. Doctrine OPERATIVE; | 91 | 39 | 42 | 10 |
| governance/grounds.md | 10869 | L3: **Status: RATIFIED — owner directive "Ratify all", 2026-07-21. OPERATIVE (doctrine); | 27 | 7 | 20 | 0 |
| governance/held-tensions.md | 26721 | L3: **Status: RATIFIED — owner directive "Ratify all", 2026-07-21. OPERATIVE (doctrine).** | 57 | 20 | 36 | 1 |
| governance/jurisdiction-philosophy.md | 9713 | L2: **Status:** CANONICAL — A8 Session 1 | 134 | 38 | 85 | 7 |
| governance/legal-regulatory.md | 29256 | L2: **Status:** CANONICAL — A11 Session 1 | 45 | 15 | 22 | 8 |
| governance/migration-based-writes-adopted-2026-05-11.md | 7443 | L5: **Status:** Adopted | 14 | 4 | 6 | 4 |
| governance/migration-survival.md | 26386 | L3: **Status:** CANONICAL — adopted by project owner 2026-05-02 01:37 (instruction "perform all | 33 | 8 | 17 | 7 |
| governance/mining-screens.yaml | 4136 | NONE | 28 | 10 | 18 | 0 |
| governance/mission-PROVISIONAL.md | 13886 | L2: **Status:** PROVISIONAL — committed 2026-04-26 02:42 UTC per Stage 0.6; revised 2026-04-26  | 52 | 11 | 36 | 5 |
| governance/mission-and-epistemics.md | 21224 | L2: **Status:** CANONICAL — locked at iter 4 cross-test pass (2026-04-26 05:29). Supersedes `go | 193 | 85 | 92 | 15 |
| governance/owner-browser.yaml | 85459 | NONE | 116 | 44 | 72 | 0 |
| governance/pi-revision-co.md | 8703 | L3: **Status:** PROPOSAL — project-owner-applied; not auto-applied | 10 | 3 | 2 | 5 |
| governance/pipeline-contract.yaml | 27351 | NONE | 232 | 93 | 132 | 7 |
| governance/pipeline-operations.md | 8443 | L3: **Status:** PROPOSED · **Date:** 2026-08-02 · **Scope:** definitional | 56 | 15 | 40 | 1 |
| governance/population-taxonomy.md | 11388 | L2: **Status:** SUPERSEDED (population code set) — see banner below. Structural detail retained | 65 | 28 | 25 | 11 |
| governance/pre-decision-multimodal-access-armature.md | 7063 | L3: **Status:** PRE-DECISION (captures design intent for A7+ formalization) | 6 | 3 | 2 | 1 |
| governance/pre-stage-a-decisions.md | 16741 | L2: **Status:** CANONICAL — retroactively marked at A12 S2 finding RC-001 resolution (2026-04-3 | 49 | 19 | 23 | 7 |
| governance/project-instructions-v10_10.md | 442 | L1: # Project Instructions v10.10 — ARCHIVED (moved) | 3 | 1 | 2 | 0 |
| governance/project-instructions-v10_11.md | 442 | L1: # Project Instructions v10.11 — ARCHIVED (moved) | 4 | 2 | 2 | 0 |
| governance/project-instructions-v10_12.md | 442 | L1: # Project Instructions v10.12 — ARCHIVED (moved) | 5 | 3 | 2 | 0 |
| governance/project-instructions-v10_13.md | 442 | L1: # Project Instructions v10.13 — ARCHIVED (moved) | 4 | 2 | 2 | 0 |
| governance/project-instructions-v10_14.md | 21952 | NONE | 38 | 14 | 23 | 1 |
| governance/project-instructions-v10_7.md | 440 | L1: # Project Instructions v10.7 — ARCHIVED (moved) | 6 | 3 | 2 | 1 |
| governance/project-instructions-v10_8.md | 440 | L1: # Project Instructions v10.8 — ARCHIVED (moved) | 5 | 1 | 2 | 2 |
| governance/project-instructions-v10_9.md | 440 | L1: # Project Instructions v10.9 — ARCHIVED (moved) | 4 | 2 | 2 | 0 |
| governance/repo-strategy-revision-co.md | 8258 | L2: **Status:** PROPOSED — pending project-owner application | 15 | 7 | 4 | 4 |
| governance/repo-strategy.md | 4156 | L4: **Status:** Decision committed | 27 | 8 | 12 | 7 |
| governance/research-contract-baseline.json | 698 | NONE | 34 | 12 | 17 | 5 |
| governance/research-contract.yaml | 19986 | NONE | 152 | 51 | 99 | 2 |
| governance/retired-vocabulary.yaml | 57876 | NONE | 77 | 33 | 40 | 3 |
| governance/schema-reference-exemptions.yaml | 1480 | NONE | 22 | 4 | 18 | 0 |
| governance/stage-map.yaml | 8957 | NONE | 135 | 66 | 69 | 0 |
| governance/tier-system.md | 16183 | L3: **Status:** OPERATIVE — 2026-05-25; amended 2026-07-20 (§8–§10 added; §3 binary rule supers | 272 | 98 | 139 | 33 |
| governance/time-model.md | 19784 | L2: **Status:** CANONICAL — A9 Session 1 | 39 | 8 | 19 | 12 |
| governance/userPreferences-v6.2-deltas.md | 3307 | L3: **Status:** repo-side reference copy. Live deployment: paste into claude.ai project setting | 2 | 0 | 2 | 0 |
| governance/workplan-adoption.md | 10444 | NONE | 14 | 6 | 4 | 4 |

Zero-inbound check. Command: inline python over the inbound JSON that produced the table (counting ALL==0; the table itself is the `git grep -l -F` output). Result: 0 of 142 files have ALL==0. [NULL: governance/ + decisions/ examined (142 files), ALL==0 found nothing]. Files with LIVE-DOC==0 (5): decisions/DR-2026-05-15-migration-history-drift-repair.md, decisions/DR-2026-05-18-statutory-metadata-completeness.md, decisions/DR-2026-07-20-citation-mining-methodology-corrections.md, governance/citation-mining-protocol-memo-2026-05-11.md, governance/userPreferences-v6.2-deltas.md.

Ten fewest ALL pointers in governance/ and decisions/ (the substitute for 'zero'):

| ALL | LIVE-DOC | path |
|---:|---:|---|
| 2 | 0 | decisions/DR-2026-07-20-citation-mining-methodology-corrections.md |
| 2 | 0 | governance/userPreferences-v6.2-deltas.md |
| 3 | 1 | governance/project-instructions-v10_10.md |
| 4 | 1 | decisions/DR-2026-05-28-c-population-junctions-governance-close.md |
| 4 | 1 | decisions/DR-2026-07-22-population-representation-reconciliation.md |
| 4 | 2 | governance/project-instructions-v10_11.md |
| 4 | 2 | governance/project-instructions-v10_13.md |
| 4 | 2 | governance/project-instructions-v10_9.md |
| 5 | 0 | decisions/DR-2026-05-18-statutory-metadata-completeness.md |
| 5 | 1 | decisions/DR-2026-05-28-b-source-value-extractions-schema.md |

Ten most-pointed-at within governance/ and decisions/ (ALL). Command: sort of the table above by ALL, descending.

| ALL | LIVE-DOC | SCRATCH | path |
|---:|---:|---:|---|
| 327 | 166 | 146 | governance/check-registry.yaml |
| 272 | 98 | 139 | governance/tier-system.md |
| 232 | 93 | 132 | governance/pipeline-contract.yaml |
| 193 | 85 | 92 | governance/mission-and-epistemics.md |
| 175 | 67 | 97 | governance/evidence-architecture.md |
| 162 | 69 | 91 | governance/context-map.yaml |
| 159 | 52 | 92 | governance/evidence-methodology.md |
| 152 | 51 | 99 | governance/research-contract.yaml |
| 135 | 13 | 31 | decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md |
| 135 | 66 | 69 | governance/stage-map.yaml |

## 3b. Superseded / historical / retired files and their pointers from doctrine
Command: status line from the first 15 lines (`grep -n -E 'Status:|SUPERSEDED|HISTORICAL|DEPRECATED|RETIRED|ARCHIVED'`) and, for each such file, `git grep -l -F -- <path>` filtered to STRICT = CLAUDE.md, governance/*, skills/*, .claude/* (the set the spec names as live). Raw lists are in /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/inbound2.json.

| file | declared status | ALL | LIVE-DOC | STRICT pointers (live doctrine) |
|---|---|---:|---:|---|
| governance/population-taxonomy.md | SUPERSEDED (population code set) L2 | 65 | 28 | **governance/functional-taxonomy.md, governance/held-tensions.md** (both RATIFIED doctrine). Also prose-only in architecture/schema-spec.md, references/project-standards.md, data/guidebook.db (binary; not checked further) |
| decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md | SUPERSEDED-BY DR-2026-07-21-...option-a-execution L3 | 32 | 3 | none (0). LIVE: decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md, references/project-standards.md |
| decisions/DR-2026-07-22-population-representation-reconciliation.md | SUPERSEDED 2026-07-23 L3 | 4 | 1 | none (0) |
| decisions/RATIFICATION-PACKAGE-2026-07-12.md | SUPERSEDED IN PART (appended 2026-11-19) L10 | 31 | 5 | none (0). LIVE: decisions/DR-2026-07-12-evidence-architecture-unification.md, decisions/RATIFICATION-RECORD-2026-07-13.md, references/project-standards.md, workplan/2026-11-12-bidirectional-pipeline/tasks/T-119-ledger-unification-entry.md |
| governance/project-instructions-v10_7, _8, _9, _10, _11, _12, _13 (7 stubs) | ARCHIVED (moved) L1 | 3-6 each | 1-3 each | STRICT only governance/retired-vocabulary.yaml (a registry that names them; expected). Others: decisions/PI-update-needed.md, decisions/DR-2026-05-13-evidence-verification-methodology.md, decisions/DR-2026-07-12-versioning-and-archive-consolidation.md (prose) |

Flags that are NOT superseded documents (my first pass was too broad): governance/tier-system.md (status OPERATIVE; the regex hit its status line text "§3 binary rule superseded") and decisions/DR-2026-08-15-superseded-status-retained.md (title is about the SUPERSEDED status value). Command that produced the spurious hit: `grep -n -i superseded governance/tier-system.md | head -1`.

Files whose first 15 lines contain no status marker at all (NONE; command: the inbound2.json scan): decisions/DR-2026-05-23-cohort-manifest.json, decisions/DR-2026-08-19-research-restart-operative-instrument.md, decisions/DR-2026-09-26-recurring-defect-shapes-remediation.md, decisions/PI-update-needed.md, decisions/RATIFICATION-RECORD-2026-07-13.md, decisions/RATIFICATION-RECORD-2026-07-21.md, governance/armature_v4_integration.md, governance/check-registry.yaml, governance/co1-operational.md, governance/context-map.yaml, governance/doctrine-deltas.json, governance/evidence-methodology.md, governance/mining-screens.yaml, governance/owner-browser.yaml, governance/pipeline-contract.yaml, governance/project-instructions-v10_14.md, governance/research-contract-baseline.json, governance/research-contract.yaml, governance/retired-vocabulary.yaml, governance/schema-reference-exemptions.yaml, governance/stage-map.yaml, governance/workplan-adoption.md. [NONE count: 22 of 142]

Note: decisions/DR-2026-08-19-research-restart-operative-instrument.md (the instrument CLAUDE.md names as operative) is in that NONE set; its status is not in its first 15 lines.

## 4. Facts restated across files: definition homes (file:line)
Each row: the fact, the command that finds its restatements, the count, and the definition homes. Counts exclude `_archived/`, `audits/`, `versions/`, `workplan/_superseded/`, `references/search-log/`, `references/bpc/`, `transcripts/`, `sessions/`, `scratchpad/`, unless noted.

### 4a. Tier ladder (T1..T6, Co-1, Co-2)
Command: `git grep -n -E '(^|[^A-Za-z0-9-])(T[1-6]|Co-1|Co-2)([^A-Za-z0-9-]|$)'` restricted to the live set; lines naming four or more distinct tiers: 110 (command: the scan in /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/restate.py). Ladder-defining homes:
- governance/tier-system.md:15-22 — the ladder table (T1, Co-1, T2, Co-2, T3, T4, T5, T6); governance/tier-system.md:11 — prose statement of the ladder. Canonical per the file's own Status line (line 3).
- CLAUDE.md:367-370 — §6 restatement (bold list: T1, Co-1, T2, Co-2, T3, T4–T6).
- governance/owner-browser.yaml:107, :109 — `meaning:` strings restating tiers for the owner's browser page.
- governance/evidence-methodology.md:30 — prose. governance/evidence-architecture.md:44 — T4–T6 stratum definition.
- references/methodology-evidence-hierarchy-mapping.md:39 (stratum), :161 (marker table, which restates the ladder).
- schemas/tier_derivation.py:105 — code docstring with FULL/PARTIAL tier bands (code home; a second copy of the ladder in code).
- scripts/assess/assess_cell.py:1095, :1449, :1594 — strings and comments naming the anchoring set.
- skills/evidence-auditor_SKILL.md:45-46, :54 (the marker table restated; .claude/skills/evidence-auditor/SKILL.md is byte-identical per cmp).
- Restatements in decisions/ (15 lines, e.g. decisions/DR-2026-07-20-weighted-strength-anchor-model.md:26, decisions/DR-2026-07-12-tier3-stated-threshold.md:15) and workplan/ (37 lines) and references/project-standards.md (20 lines); counts: `git grep -n -E ...` per top directory, as in the restate scan.

### 4b. Stage spine (base -> research -> evidence -> judgment -> synthesis -> specification -> render)
Command: `git grep -n -E 'base ?(->|→) ?research'` over the live set: 14 lines (restate scan, `## stage spine line`).
- Canonical text: governance/pipeline-contract.yaml:17 (`spine:` key; CLAUDE.md §3 says this is the single home).
- Rendering checked by claude_md_spine: CLAUDE.md:245 (the SPINE line, marked do-not-hand-edit).
- Stage table: CLAUDE.md:255-261 (7 rows, `| **base** |` … `| **render** |`). Command: `git grep -n -E '\| \*\*(base|research|evidence|judgment|synthesis|specification|render)\*\*' -- . ':(exclude)_archived' ...` = 7 rows in CLAUDE.md; 1 further in workplan/2026-10-12-simplification-workplan.md.
- Prose restatements (not gated): architecture/meta-scripts-spec.md:453; references/project-standards.md:2298 (ruling text), :2341, :2387, :2848; decisions/DR-2026-08-27-seven-stage-spine-base-is-first.md:1 (title); decisions/DR-2026-08-19-research-restart-operative-instrument.md:779 (arrow form that omits `render`; stale by its own text); workplan/2026-09-10-batch-06-runbook.md:1, workplan/2026-09-10-road-to-batch-06.md:3, workplan/2026-09-16-infrastructure-remediation-brief.md:658, workplan/2026-09-18-pipeline-content-review-and-walkability.md:38, workplan/2026-10-30-ramp-spec-pages/RENDER-DECISIONS-AND-PIPELINE.md:33, workplan/pipeline-state-graph/STATE-GRAPH.md:9, workplan/pipeline-state-graph/WALKABILITY.md:26,48,166.
- Code comment: scripts/audit/claude_md_spine.py:13 (names the superseded six-stage list).

### 4c. Marker glyphs (● ◐ ○ ⚠)
Command: `git grep -c -E '●.*◐|◐.*○|○.*⚠|●.*○' -- CLAUDE.md governance skills .claude architecture scripts references/*.md decisions` = 100 lines in total (per-file counts from that command).

Legend homes, and the meanings they give to the glyphs:
| file:line | ● | ◐ | ○ | ⚠ |
|---|---|---|---|---|
| CLAUDE.md:372 | confirmed | policy/standards only | grey, thin or unverified | not defined |
| governance/tier-system.md:64-66 (and table :92-93) | confirmed evidence base | policy or standards basis only | grey literature, expert consensus, thin base | `⚠ Superseded` heading at :49 (a different meaning) |
| governance/owner-browser.yaml:111 | confirmed | policy or standards only | grey, thin, or unverified | not defined |
| skills/evidence-auditor_SKILL.md:45-46, :54 | confirmed evidence base | policy or standards basis only | line 54: ○ used as a mismatch condition | — |
| references/project-standards.md:26 (RULE line) | confirmed evidence base | policy/standards basis only | grey, expert consensus, thin base, unconfirmed | ⚠ defined at :7062 and :7078 as the grey/thin/unverified marker 'in place of the circle' |
| governance/mission-and-epistemics.md:136 | confirmed | policy/standards only | grey, thin, unverified | not defined |
| governance/armature_v4.md:35 | specification supported by direct evidence | — | — | not defined |
| governance/evidence-methodology.md:381 | 'No ● or ○ marker' (governs specifications) | — | — | — |
| architecture/navigation-modes.md:301 | stated evidence | provisional evidence | pending review | — |
| architecture/page-templates.md:23 | stated (green) | provisional (amber) | pending (grey) | — |
| architecture/page-templates.md:145 (jurisdiction matrix, facet 7) | present | — | no requirement | ◌ not searched (no ⚠) |
| architecture/schema-reconciliation.md:56 | = stated | = provisional | = pending | — |
| references/case-study-compendium.md:553 | evidence-based | mixed | expert consensus | — |
| references/parser-source-readiness.md:236 | 'Primary' (●) | — | 'Secondary' (○) | — |
| references/parser-source-readiness.md:210 | '● ◐ ○ (three-tier)' with no meanings given | | | |
| references/methodology-evidence-hierarchy-mapping.md:161 | confirmed | — | — | — |
| governance/population-taxonomy.md:9 | — | — | — | `⚠ Superseded by DR-2026-07-23` (banner) |

Glyph ⚠ carries at least three meanings across live files: grey/unverified marker (references/project-standards.md:7062, :7078), 'Superseded' banner (governance/tier-system.md:49; governance/population-taxonomy.md:9). Count: `git grep -c '⚠' -- CLAUDE.md governance skills .claude architecture` = 8 lines.

### 4d. Owner's goal sentence ("we research, we record")
Command: `git grep -n -i 'we research, we record' -- . ':(exclude)transcripts' ':(exclude)sessions' ':(exclude)scratchpad'`: CLAUDE.md:5 (verbatim, dated 2026-11-20), references/project-standards.md:8124 (quoted entry), references/project-standards.md:8194 (mention). Other homes: `git grep -l -i 'we research, we record' -- sessions | wc -l` = 0; `-- transcripts | wc -l` = 26; `-- scratchpad | wc -l` = 1.

### 4e. Write path (scratch copy -> db.py -> emit_batch_sql.py -> emit_data_migration.py -> migrate_db.py)
Command: `git grep -n -E 'scratch copy|WRITE PATH|emit_batch_sql[^|]*emit_data_migration|emit_data_migration[^|]*migrate_db' -- . ':(exclude)attestations' ':(exclude)scripts/migrations' ':(exclude)transcripts' ':(exclude)sessions' ':(exclude)scratchpad' ':(exclude)_archived' ':(exclude)workplan' ':(exclude)versions' ':(exclude)references/search-log' ':(exclude)references/bpc' ':(exclude)audits' ':(exclude)data' ':(exclude)scripts/tests'`: 23 files (the sentence-level matches are below).
- Sentence homes: CLAUDE.md:99 (`emit_data_migration.py → migrate_db.py`), CLAUDE.md:288-289 (THE WRITE PATH IS ONE SENTENCE).
- Harness/config copies: .claude/settings.json:20 (in the harness prompt string); .gitignore:28, :31, :37 (comments).
- Generated: governance/context-map.yaml:12 (generated by scripts/generate/context_map.py:256 — a code home).
- Other homes: governance/research-contract.yaml:351; governance/check-registry.yaml (no definitional line; 4 matches are scratch-copy test fixtures); architecture/meta-scripts-spec.md:498 (table row L2.7); .claude/agents/db-census.md:23; .claude/commands/adversarial.md:50; references/project-standards.md:2711; scripts/dbcore.py:23, :181; scripts/assess/assess_cell.py:12, :2260, :2548.

Note: the same sentence is restated in code strings (scripts/assess/assess_cell.py:2260, :2548) and in a harness prompt (.claude/settings.json:20). Those are the copies a prose edit to CLAUDE.md does not reach.

## 5. Retired vocabulary still present in live files
Source: `governance/retired-vocabulary.yaml` (read; 27 active entries RV-001..RV-027; `deferred:` and `rejected:` sections not counted). Global exempt_paths include `decisions/**`, `_archived/**`, `scripts/migrations/**`, `references/project-standards.md`, `attestations/**`, `sessions/**`, `transcripts/**`, `retrieval-log/**`, `governance/retired-vocabulary.yaml` and `scripts/audit/retired_vocabulary_audit.py`.
Command per token: `git grep -c -F [-w for match: identifier] -- <token> -- CLAUDE.md governance skills .claude architecture` (the RAW column), with line-level hits recorded by `git grep -n` (file `/tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/rv_hits.tsv`). SELF = hits in governance/retired-vocabulary.yaml (self-exempt). EXEMPT = hits matching the entry's own exempt_paths glob. ESCAPE = hits carrying `[RETIRED-VOCAB-OK]`. NET = remaining hits. NET is my approximation of the audit's verdict, not the audit's output; match semantics for `identifier` were approximated with `git grep -w`.

| id | match | token | RAW | SELF | EXEMPT | ESCAPE | NET |
|---|---|---|---:|---:|---:|---:|---:|
| RV-001 | identifier | `applicable_groups` | 2 | 2 | 0 | 0 | 0 |
| RV-002 | identifier | `doi_less_key` | 10 | 4 | 0 | 2 | 4 |
| RV-003 | literal | `audit.yml` | 11 | 3 | 1 | 2 | 5 |
| RV-004 | literal | `research-contract.yml` | 2 | 1 | 0 | 0 | 1 |
| RV-005 | literal | `regenerate-vetting-surface.yml` | 1 | 1 | 0 | 0 | 0 |
| RV-006 | literal | `regenerate-evidentiary-audit.yml` | 1 | 1 | 0 | 0 | 0 |
| RV-007 | literal | `regenerate-pipeline-completeness.yml` | 1 | 1 | 0 | 0 | 0 |
| RV-008 | literal | `data/db/guidebook.db` | 8 | 1 | 0 | 0 | 7 |
| RV-009 | literal | `/tmp/guidebook.db` | 2 | 2 | 0 | 0 | 0 |
| RV-010 | phrase | `physically disabled` | 4 | 2 | 2 | 0 | 0 |
| RV-011 | phrase | `energy-limiting chronic illness` | 1 | 1 | 0 | 0 | 0 |
| RV-012 | identifier | `UNVERIFIED-1` | 22 | 3 | 0 | 0 | 19 |
| RV-013 | identifier | `VERIFIED-1` | 2 | 2 | 0 | 0 | 0 |
| RV-014 | identifier | `VERIFIED-2` | 1 | 1 | 0 | 0 | 0 |
| RV-015 | identifier | `UNVERIFIED-2` | 2 | 1 | 0 | 0 | 1 |
| RV-016 | identifier | `VERIFIED-WITH-CORRECTION` | 4 | 2 | 0 | 0 | 2 |
| RV-017 | identifier | `db_meta.schema_version` | 2 | 2 | 0 | 0 | 0 |
| RV-018 | identifier | `IS-PAYWALL` | 3 | 2 | 0 | 0 | 1 |
| RV-019 | identifier | `es.authors` | 2 | 2 | 0 | 0 | 0 |
| RV-020 | identifier | `evidence_cell_state` | 2 | 1 | 0 | 0 | 1 |
| RV-021 | identifier | `cell_source_links` | 1 | 1 | 0 | 0 | 0 |
| RV-022 | literal | `RESOLUTION-PROPOSED` | 1 | 1 | 0 | 0 | 0 |
| RV-023 | literal | `MODE-S-ONLY` | 2 | 2 | 0 | 0 | 0 |
| RV-024 | literal | `UNRESOLVABLE-MODE-S` | 1 | 1 | 0 | 0 | 0 |
| RV-025 | phrase | `Mode P` | 4 | 3 | 0 | 1 | 0 |
| RV-026 | phrase | `Mode S` | 7 | 2 | 0 | 5 | 0 |
| RV-027 | literal | `population_icf_links` | 4 | 3 | 0 | 1 | 0 |
| TOTAL | | | 103 | 48 | 3 | 11 | 41 |

Entries with NET > 0 (line-level, `grep` of `rv_hits.tsv`):
- RV-002 `doi_less_key`: architecture/sqlite-data-layer.md:21:> including `authors`, `year`, `title` and `doi_less_key`; the live table has none
- RV-002 `doi_less_key`: architecture/sqlite-data-layer.md:252:    doi_less_key        TEXT,              -- derived dedup key for DOI-less sources
- RV-002 `doi_less_key`: architecture/sqlite-data-layer.md:294:**Why no UNIQUE on doi / doi_less_key:** A DB-level UNIQUE either silently rejects a legitimate new source or fails noisily without 
- RV-002 `doi_less_key`: architecture/sqlite-data-layer.md:1087:      on normalised title). Was 'neither doi nor doi_less_key'; that key was
- RV-003 `audit.yml`: governance/project-instructions-v10_14.md:11:- **V10.10 (2026-05-13)** — Conciseness pass per `<migration_and_growth>` of architecture v2.3 (PI growth target 200 lines). 
- RV-003 `audit.yml`: governance/project-instructions-v10_14.md:81:- `.github/workflows/audit.yml` — 3 blocking checks: source_slug_links duplicates, citation-mining completeness, migration re
- RV-003 `audit.yml`: governance/project-instructions-v10_14.md:170:    - `audit.yml` `attestation_schema` — JSON schema validation (Level 4 blocking).
- RV-003 `audit.yml`: governance/project-instructions-v10_14.md:171:    - `audit.yml` `attestation_evidence` — cross-reference rule-status to commit content (Level 2 → 4 after 7-day shakedown 
- RV-003 `audit.yml`: governance/project-instructions-v10_14.md:172:    - `audit.yml` `attestation_verdict` — NON-COMPLIANT count surfaced as PR comment / commit annotation; never blocking.
- RV-004 `research-contract.yml`: governance/check-registry.yaml:1063:    all three checks in this script read. Advisory, as it was in research-contract.yml.'
- RV-008 `data/db/guidebook.db`: architecture/schema-spec.md:970:- Add `data/db/guidebook.db` as the operative substrate location once adopted.
- RV-008 `data/db/guidebook.db`: architecture/schema-spec.md:972:  `data/guidebook.db`, not `data/db/guidebook.db`. The proposal line is left as
- RV-008 `data/db/guidebook.db`: governance/repo-strategy-revision-co.md:12:> at **`data/db/guidebook.db`**, and the canonical database is in fact
- RV-008 `data/db/guidebook.db`: governance/repo-strategy-revision-co.md:13:> **`data/guidebook.db`**. `data/db/guidebook.db` has never existed in this tree.
- RV-008 `data/db/guidebook.db`: governance/repo-strategy-revision-co.md:55:> The deferred B1 trigger has resolved (per D-0138 PROVISIONAL → CANONICAL on adoption). Operative storage form is SQLite (sing
- RV-008 `data/db/guidebook.db`: governance/repo-strategy-revision-co.md:62:> - **The operative SQLite database commits to `data/db/guidebook.db`.** Single binary file; treated as a generated artifact at
- RV-008 `data/db/guidebook.db`: governance/repo-strategy-revision-co.md:90:| Operative storage form | SQLite at `data/db/guidebook.db` per D-0138 |
- RV-012 `UNVERIFIED-1`: architecture/schema-spec.md:78:                   ('VERIFIED', 'UNVERIFIED-1', 'UNVERIFIED-2', 'UNAVAILABLE', 'STRUCK'))
- RV-012 `UNVERIFIED-1`: governance/co1-operational.md:13:> Where a rule below said "flag `UNVERIFIED-1` for re-search", the successor test is
- RV-012 `UNVERIFIED-1`: governance/evidence-methodology.md:13:> Where a rule below said "flag `UNVERIFIED-1` for re-search", the successor test is
- RV-012 `UNVERIFIED-1`: governance/migration-survival.md:79:| Verified evidence sources (bibliography) | SURVIVES_AS_IS | 584 sources; 86% verified (Tier 1–6); residual 14% (84 sources) UNVERIFI
- RV-012 `UNVERIFIED-1`: governance/migration-survival.md:176:| 84 UNVERIFIED-1 residual | OPEN | 84 entries | Project-owner disposition (forward to BPC authors or CLOSED-DELETED per Standing Rul
- RV-012 `UNVERIFIED-1`: governance/migration-survival.md:246:| C7 bibliography UNVERIFIED-1 disposition | 84 sources (OPEN → SURVIVES_AS_IS or SUPERSEDED per disposition) | Resolves OPEN |
- RV-012 `UNVERIFIED-1`: governance/migration-survival.md:291:- It does not pre-empt project-owner decisions on the 106 placeholder Decision records, the C7 UNVERIFIED-1 disposition, or any other
- RV-012 `UNVERIFIED-1`: governance/project-instructions-v10_14.md:114:   Phase ordering is STRICT SEQUENTIAL B before E. No BPC may be rewritten until its formally-linked sources have completed 
- RV-012 `UNVERIFIED-1`: governance/project-instructions-v10_14.md:148:10. **Evidence verification gate for synthesis.** Per DR-2026-05-13, amended per DR-2026-05-18. No BPC synthesis claim may c
- RV-012 `UNVERIFIED-1`: skills/evidence-metadata-rehabilitation_SKILL.md:132:   (Was `UNVERIFIED-1`, retired by D-0157 and migrated 2026-08-04. The "one attempt so far"
- RV-012 `UNVERIFIED-1`: skills/evidence-metadata-rehabilitation_SKILL.md:206:> `verification_status ∈ {VERIFIED, UNVERIFIED-1}`. That vocabulary was retired by
- RV-012 `UNVERIFIED-1`: skills/evidence-metadata-rehabilitation_SKILL.md:208:> **nothing** on the `UNVERIFIED-1` limb ever since.
- RV-012 `UNVERIFIED-1`: skills/evidence-metadata-rehabilitation_SKILL.md:210:> It is not a find-and-replace. `UNVERIFIED-1` mapped to `UNVERIFIED` +
- RV-012 `UNVERIFIED-1`: skills/evidence-metadata-rehabilitation_SKILL.md:218:> the gate** — sources that were eligible as `UNVERIFIED-1` are no longer. That is a
- RV-012 `UNVERIFIED-1`: skills/gap-driven-mining_SKILL.md:199:> `verification_status ∈ {VERIFIED, UNVERIFIED-1}`. That vocabulary was retired by
- RV-012 `UNVERIFIED-1`: skills/gap-driven-mining_SKILL.md:201:> **nothing** on the `UNVERIFIED-1` limb ever since.
- RV-012 `UNVERIFIED-1`: skills/gap-driven-mining_SKILL.md:203:> It is not a find-and-replace. `UNVERIFIED-1` mapped to `UNVERIFIED` +
- RV-012 `UNVERIFIED-1`: skills/gap-driven-mining_SKILL.md:211:> the gate** — sources that were eligible as `UNVERIFIED-1` are no longer. That is a
- RV-012 `UNVERIFIED-1`: skills/integrity-protocol_SKILL.md:56:- **verification/DB-state mismatch:** a migration comment claimed "verification complete" while the cited sources still sat at `UNVE
- RV-015 `UNVERIFIED-2`: architecture/schema-spec.md:78:                   ('VERIFIED', 'UNVERIFIED-1', 'UNVERIFIED-2', 'UNAVAILABLE', 'STRUCK'))
- RV-016 `VERIFIED-WITH-CORRECTION`: governance/co1-operational.md:15:> meant was "not yet exhausted". Where it said `∈ {VERIFIED, VERIFIED-WITH-CORRECTION}`,
- RV-016 `VERIFIED-WITH-CORRECTION`: governance/evidence-methodology.md:15:> meant was "not yet exhausted". Where it said `∈ {VERIFIED, VERIFIED-WITH-CORRECTION}`,
- RV-018 `IS-PAYWALL`: skills/evidence-metadata-rehabilitation_SKILL.md:126:   (Was `IS-PAYWALL`, retired by D-0157 and migrated 2026-08-04 — the paywall is the
- RV-020 `evidence_cell_state`: architecture/schema-spec.md:116:> from `evidence_cell_state` at schema version 055), and it diverges from this proposal in four

Schema check, sqlite_master (read-only URI, `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`): 229 objects examined (30 views), SQL text searched for all 27 tokens. Result: 0 hits. [NULL: sqlite_master, 229 objects examined, no retired token found].

Note: `governance/project-instructions-v10_14.md` (highest-numbered PI, which CLAUDE.md names as live) carries 5 `audit.yml` hits (RV-003; command `git grep -c 'audit.yml' -- governance/project-instructions-v10_14.md` = 5) and is NOT in the global exempt list.

## 6. Skills: last commit, and whether they name the deleted item layer
Commands: `git log -1 --format=%cs -- <path>` per skill; item-layer probe: `grep -c -E '\b[A-Z]-[0-9]{2}\b' <file>` (item codes), `grep -c -i 'items table'`, `grep -c 'item_code'`.

| path | last commit (YYYY-MM-DD) | item codes (A-10 style) | 'items table' | item_code | names deleted item layer? |
|---|---|---:|---:|---:|---|
| skills/adversarial-research_SKILL.md | 2026-11-19 | 4 | 0 | 0 | YES (item codes as content) |
| skills/bibliography-compiler_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/citation-miner_SKILL.md | 2026-11-16 | 0 | 0 | 0 | no |
| skills/citation-verifier_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/connection-discovery_SKILL.md | 2026-11-17 | 0 | 0 | 0 | no |
| skills/content-gap-analyzer_SKILL.md | 2026-10-15 | 0 | 0 | 2 | mention only (placeholder param) |
| skills/cross-population-conflict-mapper_SKILL.md | 2026-11-13 | 0 | 0 | 0 | no |
| skills/cross-reference-resolver_SKILL.md | 2026-10-15 | 3 | 0 | 0 | YES (item codes as content) |
| skills/doctrine-recheck_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/economics-researcher_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/evidence-auditor_SKILL.md | 2026-10-22 | 0 | 0 | 3 | mention only (placeholder param) |
| skills/evidence-metadata-rehabilitation_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/find-and-replace_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/functional-deficit-researcher_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/gap-driven-mining_SKILL.md | 2026-11-20 | 0 | 0 | 0 | no |
| skills/github-io_SKILL.md | 2026-11-06 | 0 | 0 | 0 | no |
| skills/integrity-protocol_SKILL.md | 2026-10-14 | 0 | 0 | 0 | no |
| skills/jurisdiction-tracker_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/multilingual-research_SKILL.md | 2026-11-15 | 0 | 0 | 0 | no |
| skills/prose-style-checker_SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| skills/research-log-manager_SKILL.md | 2026-11-18 | 0 | 0 | 0 | no |
| skills/run-pipeline_SKILL.md | 2026-11-20 | 0 | 0 | 0 | no |
| skills/session-consolidator_SKILL.md | 2026-11-06 | 0 | 0 | 0 | no |
| skills/supersession-audit_SKILL.md | 2026-10-16 | 0 | 0 | 0 | no |
| skills/toc-editor_SKILL.md | 2026-11-20 | 2 | 0 | 0 | YES (item codes as content) |
| skills/voice-style_SKILL.md | 2026-10-14 | 2 | 0 | 0 | YES (item codes as content) |
| .claude/skills/bibliography-compiler/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/citation-miner/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/citation-verifier/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/connection-discovery/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/content-gap-analyzer/SKILL.md | 2026-10-15 | 0 | 0 | 2 | mention only (placeholder param) |
| .claude/skills/cross-population-conflict-mapper/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/cross-reference-resolver/SKILL.md | 2026-10-15 | 3 | 0 | 0 | YES (item codes as content) |
| .claude/skills/doctrine-recheck/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/economics-researcher/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/evidence-auditor/SKILL.md | 2026-10-15 | 0 | 0 | 3 | mention only (placeholder param) |
| .claude/skills/find-and-replace/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/functional-deficit-researcher/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/gap-driven-mining/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/github-io/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/jurisdiction-tracker/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/multilingual-research/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/prose-style-checker/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/research-log-manager/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/run-pipeline/SKILL.md | 2026-11-06 | 0 | 0 | 0 | no |
| .claude/skills/session-consolidator/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/supersession-audit/SKILL.md | 2026-10-15 | 0 | 0 | 0 | no |
| .claude/skills/toc-editor/SKILL.md | 2026-10-15 | 2 | 0 | 0 | YES (item codes as content) |

Item-code lines (the actual content, from `grep -n -E '\b[A-Z]-[0-9]{2}\b|item_code' <file>`):
- skills/adversarial-research_SKILL.md:294, :300, :306, :312 (GAP-069 A-10; GAP-097 B-02; GAP-260 K-05; GAP-076 A-12). Counted as item codes by the probe.
- skills/cross-reference-resolver_SKILL.md:37 (`see item G-03`, `refer to A-11`, `see K-04`; the skill validates item headings).
- skills/toc-editor_SKILL.md:56, :89 (J-01 used as a live example and a RECODE rule).
- skills/voice-style_SKILL.md:109 (A-03), :252 (A-16).
- skills/content-gap-analyzer_SKILL.md:43, :53 and skills/evidence-auditor_SKILL.md:115, :124, :130 use `item_code` as a CLI placeholder (`--section [item_code ...]`), not item codes.
- .claude copies of the same skills are byte-identical (cmp SAME), so the same lines appear in .claude/skills/.

Probe result for `items table`: 0 hits in all 48 skill files (flat + .claude). Command as above.

## 7. PROSE CALLERS: not swept by any gate (listed separately, conspicuously)

Nothing in the gate suite reads these. Each is a sentence or table that restates or depends on a fact in Section 3b, 4 or 5. Each line below was located by the command named in its section.

**7a. Superseded population-taxonomy (governance/population-taxonomy.md, SUPERSEDED).** Command: `git grep -l -F -- governance/population-taxonomy.md`, excluding transcripts/ and sessions/: 65 files (ALL); prose and doctrine homes among them include governance/functional-taxonomy.md, governance/held-tensions.md (doctrine, prose), architecture/schema-spec.md (architecture prose), references/project-standards.md (rule ledger), and workplan/2026-11-12-bidirectional-pipeline/ (10 files, from the `git grep -l -F` list). Binary home: data/guidebook.db (a pointer string inside the database; not inspected further).

**7b. Retired vocabulary in live prose (NET hits from Section 5).** Command: `git grep -n -F -- <token> -- CLAUDE.md governance skills .claude architecture` with the exemptions applied (rv_hits.tsv). The NET lines are listed in Section 5 under "Entries with NET > 0". Prose-heavy examples: architecture/sqlite-data-layer.md:21, :252, :294 (doi_less_key); architecture/schema-spec.md:78 (UNVERIFIED-1, UNVERIFIED-2 in a CHECK literal); governance/migration-survival.md:79, :176, :246, :291 (UNVERIFIED-1); governance/project-instructions-v10_14.md:11, :81, :170-172 (audit.yml); governance/evidence-architecture.md:197 (table row naming "Mode P" / "Mode S"); governance/check-registry.yaml:1063 (research-contract.yml); skills/evidence-metadata-rehabilitation_SKILL.md:126, :132, :206-218 and skills/gap-driven-mining_SKILL.md:199-211 (UNVERIFIED-1 and IS-PAYWALL, historical notes in skill prose); architecture/schema-spec.md:116 (evidence_cell_state); governance/co1-operational.md:13, :15 and governance/evidence-methodology.md:13, :15 (UNVERIFIED-1, VERIFIED-WITH-CORRECTION); governance/migration-survival.md (UNVERIFIED-1 table rows, 84 residual).

**7c. Item-layer codes in skill prose.** Command: `grep -n -E '\b[A-Z]-[0-9]{2}\b' <skill>` over the 4 skills: skills/adversarial-research_SKILL.md:294-312 (4 lines), skills/cross-reference-resolver_SKILL.md:37, skills/toc-editor_SKILL.md:56, :89, skills/voice-style_SKILL.md:109, :252. Same lines in the byte-identical .claude copies, except adversarial-research (flat only). These are skill callers of the deleted layer.

**7d. Spine restatements in prose.** See Section 4b: architecture/meta-scripts-spec.md:453; decisions/DR-2026-08-19-research-restart-operative-instrument.md:779 (arrow form without `render`); 9 workplan lines; references/project-standards.md:2298-2387, :2848.

**7e. Write-path restatements in prose.** See Section 4e: CLAUDE.md:99, :288-289; architecture/meta-scripts-spec.md:498; .claude/commands/adversarial.md:50 (command doc); .claude/agents/db-census.md:23 (agent doc); references/project-standards.md:2711; governance/research-contract.yaml:351 (yaml text).

**7f. Owner goal sentence in prose.** references/project-standards.md:8124 (quoted), :8194 (mention). Command: `git grep -n -i 'we research, we record' -- references`.

**7g. Glyph legends in prose that disagree with governance/tier-system.md §5.** architecture/navigation-modes.md:301 (● stated, ◐ provisional, ○ pending review); architecture/page-templates.md:23 and :145 (● means stated, and separately ● means present); architecture/schema-reconciliation.md:56; references/case-study-compendium.md:553; references/parser-source-readiness.md:236. Command: `git grep -n -E '●.*◐|◐.*○|○.*⚠|●.*○' -- architecture references` lists them.

**7h. Tier ladder in prose.** governance/evidence-methodology.md:30; governance/evidence-architecture.md:44, :90, :120, :129; references/methodology-evidence-hierarchy-mapping.md:39, :151, :161; workplan (37 lines) and decisions (15 lines) per Section 4a.

**7i. Superseded documents still pointed at from doctrine prose.** Section 3b: governance/functional-taxonomy.md and governance/held-tensions.md point at the SUPERSEDED population-taxonomy; decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md and references/project-standards.md point at a SUPERSEDED-BY decision (superseded document: decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md).

## 8. Nulls and unproven items

- [NULL: skills/ and .claude/skills/ (48 SKILL files), `items table` — examined, nothing found]. Command: `grep -c -i 'items table' <each file>`.
- [NULL: governance/ + decisions/ (142 files), ALL==0 pointers — examined, nothing found]. Command: Section 3 table.
- [NULL: sqlite_master (229 objects, 30 views), all 27 retired tokens — examined, nothing found]. Command: `python3` read-only URI, `SELECT type,name,sql FROM sqlite_master`, substring test per token.
- [NULL: sqlite_master, `item_code` / item-layer names — not separately probed beyond the retired-token list; the item layer was dropped (CLAUDE.md §7) and its tables are not in the 229-object list].
- Unproven, not clean: the retired-vocabulary NET column is my approximation of the audit's verdict (match semantics approximated with `git grep -w`). The authoritative verdict is the audit script, which this census did not run.
- Unproven: the `scratchpad/` and `transcripts/` hits were counted only where the spec required; the scratchpad command logs are exempt by the registry and were not checked for retired tokens beyond the counts above.
- Not checked: data/guidebook.db text blobs beyond sqlite_master SQL (e.g., row values naming superseded docs). The binary pointer at data/guidebook.db for population-taxonomy.md is reported as a hit, not examined.
- Not run: `scripts/audit/retired_vocabulary_audit.py`, `run_checks.py`. Per the task, read-only census only.
