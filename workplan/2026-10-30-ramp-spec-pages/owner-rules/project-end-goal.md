---
name: project-end-goal
description: "The Guidebook project's true end goal — a multi-modal site that dynamically renders policy-grade weighted evidence from one big data table."
metadata: 
  node_type: memory
  type: project
  originSessionId: d8ad22dd-b407-4f8b-b198-5ff102840966
---

The Guidebook (`C:\Github\guidebook`, SQLite-backed at `data/guidebook.db`) exists to produce a **multi-modal website** that dynamically interprets a massive table of data according to user requirements. The data must be sound for **academic viability and policy development**, so the evidence standard is extremely high AND the evidence must carry **dynamic weighting that shifts with user requirements** (not a single fixed score).

It is governed by an overarching mission statement / methodology, realized through an end-to-end pipeline:
**research → evidence collection → judgment → synthesis → collation → rendering → presentation** (stage names approximate; the principle is a transparent chain).

**Why:** This sets the audit bar. "Correct" here means fitness-for-mission, not just clean code: every pipeline stage needs rigorous, portable, transparent data management so the data can be reworked at any stage and the evidence chain stays auditable. The DB-is-source-of-truth + forward-only-migrations + reproducibility design exists to serve this transparency/portability requirement.

**How to apply:** Judge every finding against the pipeline. Ask of any component: which stage does it serve, is its data portable/transparent into the next stage, and does it preserve the dynamic-weighting + provenance needed for policy-grade output? Structural soundness (see the architecture audit) is a *prerequisite*; the higher-order question is whether the pipeline as a whole can render trustworthy, user-conditioned evidence. Relates to [[architecture-audit-2026-06-22]].
