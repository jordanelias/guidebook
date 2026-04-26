# Session: 2026-04-26 CO-0008 Scope
**Model:** Opus 4.6
**Started:** 2026-04-26 ~05:30 UTC
**Closed:** 2026-04-26 06:25 UTC
**Predecessor:** session_2026-04-25-a1a2-iter4.md

---

## Task

Workplan review + infrastructure overhaul scoping. Three deliverables:

1. Workplan v3 review (logic, sequence, best practice, conversion accuracy) — 10 findings
2. Entity-driven iteration proposal (data layer) — Pydantic schemas, validators, converters
3. CO-0008 scope: three-layer infrastructure overhaul (data + execution + ecosystem)

---

## Completed

### Workplan v3 review
10 findings across four dimensions. Key: A12 positioned too late, C4 gate undefined post-Amendment 7, B1 over-scoped for constraints, no incremental release strategy, no scope reduction protocol. Overall assessment: structurally sound, gaps in solo-authorship operational detail.

### Entity-driven iteration proposal
Audited current data structures (spec-db 73 records, BPC template, verified-source JSONs, connection register, existing validators). Proposed Pydantic schemas with CI enforcement, dual serialization (YAML working / JSON delivery), conversion pipeline from current files.

### CO-0008 scope — three-layer infrastructure overhaul
- **Layer 1 (Data):** Pydantic schemas, validators, converters, CI enforcement
- **Layer 2 (Execution):** 42 skills classified — 11 Python tools, 14 hybrid, 4 prose-only, 2 infrastructure, 10 deprecate. 19 of 33 "NEW" C2 skills absorbed into Stage A.
- **Layer 3 (Ecosystem):** PI update, orchestrator rewrite for Stage A workflows, CI expansion from 3 to 6 jobs, repo structure additions.

Net budget impact: ~14 session savings. B1: 6-9 → 1-2. B2: 4-6 → 2-3. C1: 4-6 → 1-2. C2: 12-16 → 6-10.

---

## Skills run

- workplan-orchestrator (session start)

## Gaps added

None.

## Rules added

- Governance+code co-production rule (project-standards)

---

## Session YAML close block

```yaml
session_close: 2026-04-26 06:25
github_writes:
  - workplan/co0008-scope-infrastructure-overhaul.md (new)
  - references/project-standards.md (rule appended)
  - sessions/session_2026-04-26-co0008-scope.md (new)
  - sessions/LATEST (updated)
commit_oid: pending
document: CO-0008
skills_run:
  - workplan-orchestrator
gaps_added: []
gaps_resolved: []
escalations_triggered: 0
rules_added:
  - governance+code co-production (project-standards)
blockers: []
research_log_updated: false
next_action:
  skill: workplan-orchestrator
  session: >
    Infrastructure pour session. Build the scaffolding per CO-0008 §6 Session 0:
    (1) Programmatic throughline analysis of spec-db,
    (2) schemas/ scaffolding (base.py, enums.py, specification.py),
    (3) scripts/validate_schema.py,
    (4) scripts/convert/convert_spec_db.py,
    (5) Proof of concept hybrid skill (evidence-auditor with output validator),
    (6) CI expansion,
    (7) PI update (model identity, Python tool calling, Stage A workflows),
    (8) workplan-orchestrator rewrite (Stage A workflows, Phase 2B dormant).
    Read co0008-scope-infrastructure-overhaul.md at session start for full spec.
  parameters:
    co0008_status: SCOPE ADOPTED
    scope_document: workplan/co0008-scope-infrastructure-overhaul.md
    deliverables_required: 8
    next_content_phase: A3 (after infrastructure pour)
latest_updated: true
```
