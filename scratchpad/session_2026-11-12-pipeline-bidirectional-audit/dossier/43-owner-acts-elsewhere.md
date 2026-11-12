# 43 — Other files that record owner acts (located, not copied)

_Generated 2026-11-12 02:24 UTC at commit 3db0a4e by build_owner_prose.py; verbatim text is copied, never paraphrased._


`.ignore` hides `sessions/`, `_archived/`, `audits/`, `versions/` from ripgrep and the Grep tool — use `grep -r` / `git grep` (CLAUDE.md §7).

Counts by top directory: `architecture` 4, `decisions` 71, `governance` 18, `references` 7, `sessions` 35, `workplan` 45

Decisions (`decisions/DR-*`) that mention owner acts, and the operative instrument's section headings:


```
# DR-2026-08-19 — The operative instrument: restart research, end the loop
## §A How to use this document
## §B Supersession table
## §C What this instrument decides, in one page
## §0 Original framing — why a Decision Record and not a plan
### The original title
## §0 Why this is a DR and not a workplan document
## §1 Decision 1 — the 93 items are LEADS, not research topics
### §1.1 The finding
### §1.2 The second vector: the determinations are still rendered
### §1.3 The decision proposed
### §1.4 The quarantine protocol — six rules
### §1.5 A consequence R1 did not price: `jurisdictional_values`
## §2 Decision 2 — the apparatus freezes until one batch lands
### §2.1 The finding
### §2.2 The decision proposed
### §2.3 Three companion changes, each one edit
### §2.4 What the freeze does not do
## §3 What this unblocks, and in what order
## §4 Acceptance — the one criterion apparatus cannot satisfy
## §5 Reversal
# AMENDMENTS — 2026-08-19, after six read-only adjudication passes
## §2.5 Freeze supersession — the clause the owner signs
## §6 The identifier stash — every DOI this project has ever held
## §7 Adversarial review — preserved as a truth-instrument, abolished as a plan-instrument
## §8 The four documents
## §9 The owner-decision batch — one sitting
## §10 Abandonment — one close-out DR
## §11 Termination — the five properties
# §12 THE RUNBOOK — run this
## §12.0 Four defects fixed first — one PR, before any research
### F3/F4 — the write path. **Ruling: session-scoped scratch DB, not `--emit-sql`.**
### F5/F6 — transactions. **The ordering that cannot break.**
### F9 — the three unproven rules
## §12.1 The batch, command by command
## §12.2 Scope
## §12.3 Acceptance
## §12.4 Failure modes, most likely first
## §12.5 What batch 2 automates
```


## Files

- `architecture/conformance-schema-findings.md`
- `architecture/meta-scripts-spec.md`
- `architecture/project-architecture-guidebook-v2.3.md`
- `architecture/sqlite-data-layer.md`
- `decisions/DR-2026-05-09-adversarial-research-protocol.md`
- `decisions/DR-2026-05-10-progressive-measurement-protocol.md`
- `decisions/DR-2026-05-13-evidence-verification-methodology.md`
- `decisions/DR-2026-05-15-migration-history-drift-repair.md`
- `decisions/DR-2026-05-18-statutory-metadata-completeness.md`
- `decisions/DR-2026-05-19-channel-2-manual-verification.md`
- `decisions/DR-2026-05-20-evidence-metadata-rehabilitation.md`
- `decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md`
- `decisions/DR-2026-05-24-best-practice-supersession-protocol.md`
- `decisions/DR-2026-05-26-gap-driven-mining-protocol.md`
- `decisions/DR-2026-05-28-b-source-value-extractions-schema.md`
- `decisions/DR-2026-05-28-c-population-junctions-governance-close.md`
- `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md`
- `decisions/DR-2026-06-10-e2g-reverification-scope.md`
- `decisions/DR-2026-06-10-synthesis-model-floor.md`
- `decisions/DR-2026-07-12-decision-tracking-naming-and-schema-doc-currency.md`
- `decisions/DR-2026-07-12-evidence-architecture-unification-impact-appendix.md`
- `decisions/DR-2026-07-12-evidence-architecture-unification.md`
- `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md`
- `decisions/DR-2026-07-12-tier3-stated-threshold.md`
- `decisions/DR-2026-07-12-versioning-and-archive-consolidation.md`
- `decisions/DR-2026-07-12-website-architecture-lock.md`
- `decisions/DR-2026-07-13-attestation-rule-identifier-registry-gap.md`
- `decisions/DR-2026-07-13-integrity-protocol-three-modes.md`
- `decisions/DR-2026-07-13-value-genealogy-and-derivation-handshake.md`
- `decisions/DR-2026-07-20-evidence-architecture-weighted-strength-reconciliation.md`
- `decisions/DR-2026-07-20-intra-category-cross-test.md`
- `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md`
- `decisions/DR-2026-07-21-held-tensions-register.md`
- `decisions/DR-2026-07-21-product-posture-thinking-tool-not-authority.md`
- `decisions/DR-2026-07-21-re-attestation-materiality-and-window.md`
- `decisions/DR-2026-07-21-tier-doctrine-source-class-consistency.md`
- `decisions/DR-2026-07-22-population-representation-reconciliation.md`
- `decisions/DR-2026-07-22-work-from-axes.md`
- `decisions/DR-2026-07-23-population-schema-replace.md`
- `decisions/DR-2026-07-24-lang-jur-map-roles.md`
- `decisions/DR-2026-07-24-search-executions-substrate.md`
- `decisions/DR-2026-07-25-controlled-vocabulary-grouping-and-provenance.md`
- `decisions/DR-2026-07-25-research-contract-mechanical-enforcement.md`
- `decisions/DR-2026-08-04-verification-status-is-a-standing-not-a-history.md`
- `decisions/DR-2026-08-06-cold-storage-search-scope.md`
- `decisions/DR-2026-08-12-migration-history-baseline.md`
- `decisions/DR-2026-08-14-status-vocabulary-ratification.md`
- `decisions/DR-2026-08-15-superseded-status-retained.md`
- `decisions/DR-2026-08-19-research-restart-operative-instrument.md`
- `decisions/DR-2026-08-24-scaffolding-is-phase-specific.md`
- `decisions/DR-2026-08-27-base-building-three-levels-items-is-not-one.md`
- `decisions/DR-2026-08-27-base-sources-is-a-target-registry.md`
- `decisions/DR-2026-08-27-concept-vocabulary-harvested-at-evidence-adjudicated-at-judgment.md`
- `decisions/DR-2026-08-27-evidence-is-the-source-judgment-is-the-extraction.md`
- `decisions/DR-2026-08-27-four-taxonomies-are-browsing-lenses.md`
- `decisions/DR-2026-08-27-naming-grammar-underscore-icf-family-singular-stage-ids.md`
- `decisions/DR-2026-08-27-relevance-is-adjudicated-at-collection.md`
- `decisions/DR-2026-08-27-seven-stage-spine-base-is-first.md`
- `decisions/DR-2026-08-31-a18-applies-to-deaf-aut-ndv-dem.md`
- `decisions/DR-2026-08-31-adversarial-subject-waiver-ratified-narrowly.md`
- `decisions/DR-2026-08-31-co1-warrant-must-name-the-co-production.md`
- `decisions/DR-2026-08-31-deaf-and-com-belong-on-room-acoustic-performance.md`
- `decisions/DR-2026-08-31-item-population-links-are-substrate-provisionally.md`
- `decisions/DR-2026-08-31-ref-00967-already-t3.md`
- `decisions/DR-2026-08-31-strike-jurisdictional-values-clause.md`
- `decisions/DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md`
- `decisions/DR-2026-09-01-rationale-ref-points-at-the-decision.md`
- `decisions/DR-2026-09-02-finish-the-render-sweep.md`
- `decisions/DR-2026-09-02-restore-research-code-leads.md`
- `decisions/DR-2026-09-02-strike-the-item-frame-pull.md`
- `decisions/DR-2026-09-11-adjudication-delegated-medical-lens-enforced.md`
- `decisions/DR-2026-09-26-recurring-defect-shapes-remediation.md`
- `decisions/PI-update-needed.md`
- `decisions/RATIFICATION-PACKAGE-2026-07-12.md`
- `decisions/RATIFICATION-RECORD-2026-07-21.md`
- `governance/check-registry.yaml`
- `governance/citation-mining-protocol-memo-2026-05-11.md`
- `governance/decision-protocol.md`
- `governance/evidence-architecture.md`
- `governance/evidence-methodology.md`
- `governance/functional-taxonomy.md`
- `governance/grounds.md`
- `governance/held-tensions.md`
- `governance/jurisdiction-philosophy.md`
- `governance/migration-survival.md`
- `governance/mission-and-epistemics.md`
- `governance/owner-browser.yaml`
- `governance/pipeline-contract.yaml`
- `governance/pipeline-operations.md`
- `governance/research-contract.yaml`
- `governance/retired-vocabulary.yaml`
- `governance/stage-map.yaml`
- `governance/tier-system.md`
- `references/methodology-evidence-hierarchy-mapping.md`
- `references/methodology/intra-category-cross-test-methodology.md`
- `references/methodology/value-genealogy-worked-example-corridor-width.md`
- `references/owner-notes/2026-08-27-architecture-note.md`
- `references/project-standards.md`
- `references/search-log/frameworks-and-methodology/manoeuvring-footprint-vs-turning-radius-methodology.md`
- `references/skill-registry.md`
- `sessions/session_2026-05-10-pass2-completion.md`
- `sessions/session_2026-05-13b-evidence-verification-methodology.md`
- `sessions/session_2026-05-15a-governance-reconciliation.md`
- `sessions/session_2026-05-17-pilot-pass-2-and-3.md`
- `sessions/session_2026-05-20-ato-rehab.md`
- `sessions/session_2026-05-23-bpc-rewrite-phase-b-closure.md`
- `sessions/session_2026-06-11-artifacts/1.4-A6-mapping-table.md`
- `sessions/session_2026-07-13-value-genealogy-mining-dossier.md`
- `sessions/session_2026-07-20-sr-meta-tier-reconciliation.md`
- `sessions/session_2026-08-12-commit-91-review-and-corridor-walk.md`
- `sessions/session_2026-08-15-owner-decisions-group-1.md`
- `sessions/session_2026-08-16-pr103-adversarial-pass.md`
- `sessions/session_2026-08-20-provenance-walk.md`
- `sessions/session_2026-08-22-record-correction-and-biblio-repair.md`
- `sessions/session_2026-08-25-rulings-incorporation-and-pipeline-sweep.md`
- `sessions/session_2026-08-27-nomenclature-reconciliation.md`
- `sessions/session_2026-09-01-lens-architecture.md`
- `sessions/session_2026-09-01-research-batch-04-accessible-circulation.md`
- `sessions/session_2026-09-02-owed-repairs.md`
- `sessions/session_2026-09-13-clear-circulation-corpus.md`
- `sessions/session_2026-09-16-research-batch-09-ramp-gradient-co1.md`
- `sessions/session_2026-09-17-notation-present-both.md`
- `sessions/session_2026-09-17-research-write-path-repair.md`
- `sessions/session_2026-09-18-research-batch-15-t2-synthesis-threshold.md`
- `sessions/session_2026-09-18-research-batch-16-backward-mining-t2-anchors.md`
- `sessions/session_2026-09-18-research-batch-17-vredenburgh-full-read-and-mining.md`
- `sessions/session_2026-09-18-research-batch-18-archive-route-ramp-threshold.md`
- `sessions/session_2026-09-20-research-batch-19-pre1990-chain-steinfeld-walter-templer.md`
- `sessions/session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa.md`
- `sessions/session_2026-09-27-repo-data-status-check-ht2rsn.md`
- `sessions/session_2026-09-28-research-batch-21-selection.md`
- `sessions/session_2026-09-28-research-batch-22-selection.md`
- `sessions/session_2026-10-01-research-batch-23.md`
- `sessions/session_2026-10-09-research-batch-24-parameter-pilot.md`
- `sessions/session_2026-11-06-pipeline-batch-2.md`
- `workplan/2026-08-05-archive-fork-execution.md`
- `workplan/2026-08-11-remediation-and-pipeline-anatomy.md`
- `workplan/2026-08-12-commit-91-adversarial-review.md`
- `workplan/2026-08-12-step-R-rename-execution-record.md`
- `workplan/2026-08-13-writer-plan.md`
- `workplan/2026-08-14-remediation-workplan.md`
- `workplan/2026-08-15-adversarial-brief-pr103.md`
- `workplan/2026-08-17-consolidated-action-plan.md`
- `workplan/2026-08-18-cull-execution-plan.md`
- `workplan/2026-08-18-handoff-next-session.md`
- `workplan/2026-08-18-model-substitution-log.md`
- `workplan/2026-08-18-research-frame-proposal.md`
- `workplan/2026-08-18-structural-census-and-cull-list.md`
- `workplan/2026-08-19-adversarial-critique-research-restart.md`
- `workplan/2026-08-20-provenance-walk-execution-plan.md`
- `workplan/2026-08-21-reasoning-doc-digestion.md`
- `workplan/2026-08-22-agonist-antagonist-execution-plan.md`
- `workplan/2026-08-22-master-execution-plan.md`
- `workplan/2026-08-24-pointer-discipline-queue.md`
- `workplan/2026-09-10-b5b-scope-owner-escalation.md`
- `workplan/2026-09-10-batch-06-runbook.md`
- `workplan/2026-09-16-infrastructure-remediation-brief.md`
- `workplan/2026-09-23-pr-audit-resolution.md`
- `workplan/2026-10-12-simplification-workplan.md`
- `workplan/2026-10-23-pipeline-resolution-workplan.md`
- `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md`
- `workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md`
- `workplan/2026-10-30-ramp-spec-pages/RENDER-DECISIONS-AND-PIPELINE.md`
- `workplan/2026-10-30-ramp-spec-pages/owner-rules/code-baselines-accepted.md`
- `workplan/2026-10-30-ramp-spec-pages/owner-rules/current-state-only.md`
- `workplan/2026-10-30-ramp-spec-pages/owner-rules/methodology-lives-in-synthesis.md`
- `workplan/2026-10-30-ramp-spec-pages/reports/spec-page-design-requirements-2026-10-29.md`
- `workplan/coverage-completion-loop-methodology-2026-07-21.md`
- `workplan/methodology-and-pipeline-enforcement-plan-2026-07-23.md`
- `workplan/pipeline-state-graph/COMPARISON.md`
- `workplan/pipeline-state-graph/CONFLICTS.md`
- `workplan/pipeline-state-graph/IDEAL-GRAPH.md`
- `workplan/pipeline-state-graph/README.md`
- `workplan/pipeline-state-graph/RULINGS.md`
- `workplan/pipeline-state-graph/STATE-GRAPH.md`
- `workplan/pipeline-state-graph/conflicts.yaml`
- `workplan/pipeline-state-graph/rehearsals/C-r7-tier-marker.md`
- `workplan/ratification-execution-register-2026-07-13.md`
- `workplan/ratification-execution-register-2026-07-21.md`
- `workplan/research-matrix-completion-execution-plan-2026-07-24.md`