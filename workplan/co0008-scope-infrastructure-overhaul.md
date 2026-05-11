<!-- SUPERSEDED 2026-05-11 -->
> **⚠ SUPERSEDED:** This workplan is replaced by `audits/bpc-rewrite-workplan-2026-05-11.md` (ADOPTED 2026-05-11 in session_2026-05-11h, per PI v10.8 standing rule #6). CO-0008 infrastructure overhaul work is now §Phase A (Foundation), with all 12 sub-tasks (A.1 through A.12) absorbing the prior CO-0008 scope. Do not use for forward work. Preserved here as historical record. See `audits/bpc-rewrite-workplan-2026-05-11.md` §Appendix E for the full supersession map.

---

# CO-0008 Scope: Infrastructure Overhaul

**Author:** Opus 4.6
**Date:** 2026-04-26
**Status:** DRAFT — for review before workplan amendment
**Supersedes:** Draft Amendment 8 (entity-driven proposal standalone)
**Materials:** workplan v3 + amendments, skill inventory (Stage 0.3), specification-database.json, validate_bpc.py, throughline-analysis.md, current PI, current workplan-orchestrator

---

## 1. Three Layers

The infrastructure overhaul has three layers that interact:

```
┌─────────────────────────────────────────────────┐
│  ECOSYSTEM (Layer 3)                             │
│  PI · orchestrator · session protocol · CI · repo│
├─────────────────────────────────────────────────┤
│  EXECUTION (Layer 2)                             │
│  Python-backed skills · hybrid skills · prose    │
├─────────────────────────────────────────────────┤
│  DATA (Layer 1)                                  │
│  Pydantic schemas · validators · converters      │
└─────────────────────────────────────────────────┘
```

Layer 1 defines what data looks like (schemas) and how it's validated (validators).
Layer 2 defines how work produces data (skills as Python tools with validated I/O).
Layer 3 defines how sessions are organized, how work is orchestrated, and how the repo is structured.

Each layer depends on the one below it. A Python-backed skill (L2) calls a Pydantic validator (L1). The orchestrator (L3) routes work through Python-backed skills (L2). Building bottom-up ensures each layer has a stable foundation.

---

## 2. Data Layer (Layer 1)

Covered in detail in the entity-driven iteration proposal. Summary:

- **Pydantic schemas** for every entity type (specification, source, BPC metadata, population, jurisdiction, connection, item, gap, conflict, parameter)
- **Shared enumerations** encoding doctrinal decisions: EvidenceTier, EvidenceType (T-03), BestPracticeStatus (T-04), PopulationCode
- **CI validators** running on every push — schema conformance, referential integrity, evidence state machine
- **Conversion scripts** transforming current files to validated YAML under `data/`
- **Dual serialization** — YAML in Git (working format), JSON build output (website delivery)

Storage form: structured YAML in Git. Resolved by constraint analysis (solo author, GitHub workflow, 12+ year horizon). Documents the derivation that satisfies workplan B1's requirement without the 6–9 session evaluation exercise.

---

## 3. Execution Layer (Layer 2)

### 3.1 Skill classification

Every skill falls into one of three execution patterns:

**PYTHON TOOL** — mechanical processing with defined input/output schemas. Claude calls the script; the script enforces constraints. Claude does not interpret the rules — the code does.

**HYBRID** — Claude does the thinking (synthesis, writing, research judgment); the output is mechanically validated. The skill has two components: prose guidance (how to think) and a Python output validator (what the output must look like).

**PROSE ONLY** — guidance for Claude's judgment where output is not mechanically validatable. Voice, style, framing. These remain SKILL.md files.

### 3.2 Classification of current 42 active skills

| Pattern | Skills | Count |
|---|---|---|
| **PYTHON TOOL** | evidence-auditor, evidence-marker, structure-auditor, volii-validator, relational-integrity-checker, cross-reference-resolver, guidebook-auditor (validation checks), content-gap-analyzer, bibliography-compiler, bulk-renumber, sensory-coherence-checker | 11 |
| **HYBRID** | item-specification-writer, multilingual-research, citation-miner, citation-verifier, functional-deficit-researcher, connection-scout, cross-population-conflict-mapper, economics-researcher, jurisdiction-tracker, literature-review-planner, item-consolidation-analyzer, research-log-manager, practice-note-generator, critique-report-writer | 14 |
| **PROSE ONLY** | voice-style, prose-style-checker, workplan-orchestrator, session-consolidator | 4 |
| **INFRASTRUCTURE** (unchanged) | github-io, github-filing | 2 |
| **DEPRECATE** (Stage C or already) | chunk-assembler, file-splitter, find-and-replace, fix-linebreaks, markdown-formatter, table-formatter, haiku-chunker, toc-editor, supplemental-integrator, vol2-item-formatter | 10 |
| **FLAG** (resolve at C0) | prose-style-checker overlap with voice-style | 1 |

### 3.3 Python tool pattern

```python
#!/usr/bin/env python3
"""
skill_name.py — mechanically enforced skill

Input:  structured data (YAML/JSON) or file path
Output: validated data (YAML/JSON) + error report
"""
from schemas.specification import Specification
from schemas.enums import PopulationCode, EvidenceTier

def run(input_path: str, output_path: str) -> dict:
    """
    Returns: {
        "status": "pass" | "fail",
        "output_path": str | None,
        "errors": [{"field": str, "message": str, "severity": str}],
        "warnings": [...]
    }
    """
    # Load input
    # Validate against schema
    # Process
    # Validate output against schema
    # Write validated output
    # Return report
```

Claude calls this via `bash_tool`: `python3 scripts/skills/evidence_auditor.py --input data/specifications/grab-bar.yaml --output data/specifications/grab-bar.yaml`. The script rejects invalid output. Claude cannot produce invalid data through this path.

### 3.4 Hybrid skill pattern

Two files per skill:

```
skills/
├── item-specification-writer_SKILL.md    # Prose: how to think about writing specs
└── item-specification-writer_validate.py # Python: validates ISW output against schema
```

Workflow:
1. Claude reads the SKILL.md for guidance on synthesis, evidence weighting, population considerations
2. Claude produces output (YAML with prose sections)
3. Claude calls `python3 skills/item-specification-writer_validate.py --check output.yaml`
4. Validator reports pass/fail with specific field-level errors
5. Claude fixes errors before committing
6. CI re-validates on push

The prose guidance is still needed — you can't mechanically determine what "most accommodating, dignified, usable" means. But you can mechanically enforce that the output has valid population codes, evidence tier assignments, T-04 state markers, and referential integrity.

### 3.5 What this replaces in workplan v3 C2

The C2 skill inventory from Stage 0.3 lists ~33 NEW skills. Under the Python-backed execution model:

| C2 category | C2 count | Disposition under this scope |
|---|---|---|
| Validation (10 new) | 10 | **Python tools built incrementally during Stage A** — not C2. Each governance phase that defines a constraint co-produces its validator. |
| Migration tools (4 new) | 4 | **Python tools built during infrastructure session + Stage A** — not C2. Conversion scripts are the migration tools. |
| Renderers (6 new) | 6 | **Remain C2/mid-C** — rendering depends on architecture decisions in B. Cut-list (Amendment 2) already defers 3 to mid-C. |
| Co-1 interface (4 new) | 4 | **Inoperative pre-launch** — per Amendment 7. Design-only document at A5 (2–3 sessions). No Python tool needed pre-launch. |
| Research/Synthesis (4–5 new) | 5 | **Hybrid skills built during Stage A** — prose guidance + output validators. Co-1-evidence-intake folds into multilingual-research REBUILD. |
| Authoring (2 new) | 2 | **Hybrid skills** — entity-authoring is the ISW replacement with Pydantic output validation. Narrative-prose is voice-style + output formatting. |
| Project orchestration (5 new) | 5 | **Mixed** — doctrine-recheck and decision-capture become Python tools; gap-register and change-order become Python-backed data operations; supersession-checker is a Python tool. |
| Epistemic (1 new) | 1 | **Deferred** — epistemic-defense is a review process, not a Stage A deliverable. |

**Net: ~19 of 33 "NEW" C2 skills are absorbed into Stage A as co-products of governance phases. C2 retains ~14 skills (renderers, remaining synthesis tools, epistemic defense).**

### 3.6 Stage A skill build schedule

| Phase | Python tools co-produced | Hybrid skills co-produced |
|---|---|---|
| Infrastructure session | validate_schema.py, convert_spec_db.py, evidence_auditor.py (proof of concept) | — |
| A3 (Conceptual model) | validate_entities.py, validate_cross_refs.py (rewrite), convert_bpc_metadata.py, convert_connections.py | — |
| A6 (Evidence methodology) | validate_evidence_state.py, convert_sources.py | multilingual-research output validator |
| A7 (Population taxonomy) | validate_population.py | — |
| A8 (Jurisdiction philosophy) | validate_jurisdiction.py, convert_jurisdictions.py | jurisdiction-tracker output validator |
| A9 (Time model) | validate_temporal.py, version_retrofit.py | — |
| A12 (Decision protocol) | decision_capture.py | — |
| A13 (Doctrine recheck) | doctrine_recheck.py, contamination_sampler.py | — |

---

## 4. Ecosystem Layer (Layer 3)

### 4.1 Project Instructions update

Current PI references are stale:

| PI element | Current state | Required update |
|---|---|---|
| Model identity | "Conversation model: Sonnet 4.6" / "Opus 4.6: best-practice synthesis" | Opus 4.6 is the active model. Remove Sonnet-as-default framing. |
| Skill loading | "load ONLY required skills for that workflow via single batch_read" | Add: Python-backed skills are called via bash_tool, not loaded as prose. |
| Workflow references | Workflows reference Phase 2B patterns (Item Specification, Full Section Review) | Add Stage A workflows. Mark Phase 2B workflows as dormant until C-stage. |
| Session protocol | Steps 1a–4 reference current file set | Add: after Step 2, run `python3 scripts/validate_schema.py --quick` to verify data layer health. |
| Effort guide | `references/effort-guide.md` governs per-skill effort | Update effort guide for Python-backed skills (effort = execution time, not reasoning depth). |

### 4.2 Workplan-orchestrator rewrite

Current orchestrator defines workflows for Phase 2B work (Item Specification, Full Section Review, Research Retrieval, etc.). No Stage A workflow exists. The orchestrator needs:

**Stage A workflow definitions:**

| Workflow | Skill/tool sequence |
|---|---|
| **Governance + Code** | [read prior governance docs] → [draft governance document] → [write Pydantic schema] → [write validator script] → [run conversion on sample data] → [fix edge cases] → [commit all: governance + schema + validator + converter] |
| **Infrastructure Build** | [throughline analysis on spec-db] → [schema scaffolding] → [validator runner] → [proof-of-concept conversion] → [CI expansion] → [commit] |
| **Session Wrap** | session-consolidator (unchanged) |

**Dormant workflows** (activated at Stage C):

All current workflows (Item Specification, Full Section Review, etc.) marked as dormant. They'll be rebuilt when the skills they depend on are Python-backed.

**Workflow execution model change:**

Current: "load SKILL.md → Claude follows prose instructions → produce markdown output"
New: "load SKILL.md for judgment guidance → call Python tool for mechanical processing → validate output → commit"

### 4.3 Session protocol changes

Minimal. The current protocol (GraphQL batch read → session file → gap register P1 filter → task intake) is sound. Two additions:

1. **Post-Step-2:** `python3 scripts/validate_schema.py --quick` — quick health check on data layer. Catches corruption introduced between sessions.
2. **Step 4 (Task intake):** workflow selection now includes "Governance + Code" and "Infrastructure Build" as options alongside existing workflows.

### 4.4 CI pipeline expansion

Current: 3 jobs (syntax, structure, commit-msg).

Target:

| Job | What it checks | Blocking? |
|---|---|---|
| syntax | UTF-8 parseable (md, json, yaml) | Yes |
| structure | validate_bpc.py, validate_cross_refs.py, check_thresholds.py | Yes |
| commit-msg | HEAD matches `{skill-name}: {action} [YYYY-MM-DD HH:MM]` | Yes |
| **schema** (new) | validate_schema.py — all entity records in `data/` validate against Pydantic models | Yes |
| **evidence-state** (new) | validate_evidence_state.py — T-04 state machine enforcement | Yes |
| **cross-entity** (new) | validate_cross_refs.py (rewritten) — referential integrity across entity types | Yes |

New jobs are additive. Existing jobs unchanged. New jobs only trigger on files in `data/` and `schemas/` directories (path filtering in CI config).

### 4.5 Repo structure additions

```
guidebook/                          # Existing repo root
├── schemas/                        # NEW — Pydantic models
├── data/                           # NEW — validated entity YAML
├── scripts/
│   ├── validate_schema.py          # NEW — generic validator runner
│   ├── validate_evidence_state.py  # NEW — T-04 enforcement
│   ├── convert/                    # NEW — conversion scripts
│   └── review/                     # NEW — review pipeline
├── build/                          # NEW — gitignored; JSON build output for website
├── skills/                         # Existing — prose SKILL.md files
│   └── *.validate.py               # NEW — output validators for hybrid skills
├── .github/workflows/ci.yml        # MODIFIED — expanded
└── [everything else unchanged]
```

All additions are additive. No existing files moved or renamed. `references/bpc/`, `references/specification-database.json`, etc. remain as frozen archives alongside the new `data/` structured versions.

---

## 5. Consolidated Workplan Impact

This replaces the draft Amendment 8 with a comprehensive package.

### 5.1 Phase budget changes

| Phase | v3 + Amend 1–7 | This scope | Delta | Reason |
|---|---|---|---|---|
| Infrastructure session | — | **1** | +1 | Scaffolding pour |
| A3 | 5–7 | **6–8** | +1 | +schema +conversion +throughline analysis |
| A6 | 3–5 | **4–6** | +1 | +T-04 validator +source unification |
| A7 | 2–3 | **2–3** | 0 | Population schema is small |
| A8 | 2–3 | **2–3** | 0 | Jurisdiction schema is small |
| A9 | 2–3 | **2–3** | 0 | Time model metadata retrofit is small |
| A12 | 1 | **1** | 0 | Decision capture tool is small |
| A13 | 1 | **1–2** | +0.5 | Contamination sampler as Python tool |
| B1 | 6–9 | **1–2** | **-5 to -7** | Constraint-resolved; integration review |
| B2 | 4–6 | **2–3** | **-2 to -3** | Validators built in Stage A |
| C1 | 4–6 | **1–2** | **-3 to -4** | Conversion scripts built in Stage A |
| C2 | 12–16 (cut-list) | **6–10** | **-6** | 19 of 33 NEW skills absorbed into Stage A; validators already exist |
| **Net** | | | **~-14 to -12** | |

### 5.2 Project total

v3 + Amendments 1–7 total: 220–336 sessions.
After this scope: **~206–324 sessions.** Net savings ~14 sessions.

More importantly: risk redistribution. The largest risk (migration errors in C3–C9) is mitigated by tooling built and tested during Stage A rather than built under time pressure during C1–C2.

### 5.3 What stays unchanged

- Phase structure (A1–A13, B1–B7, C0–C11)
- Stage sequence (A → B → C)
- A1-A2 (closed, canonical)
- A4 (voice — prose only)
- A5 (Co-1 design — prose only, re-scoped per Amendment 7)
- A10, A11 (adversarial use, legal — prose governance)
- B3–B7 (navigation, pilot, validation, lock)
- C3–C9 (migration passes — execute with existing tools)
- C10–C11 (quality gates, maintenance lifecycle)
- Cross-stage requirements CS1–CS9

---

## 6. Implementation Sequence

### Session 0: Infrastructure pour (1 session)

**Input:** specification-database.json, throughline-analysis.md, validate_bpc.py, BPC template

**Deliverables:**
1. Programmatic throughline analysis of spec-db (parameter frequency, population co-occurrence, jurisdiction clustering) → informs schema design
2. `schemas/` scaffolding: base.py, enums.py, specification.py
3. `scripts/validate_schema.py` — generic validator runner
4. `scripts/convert/convert_spec_db.py` — converts spec-db.json to validated YAML
5. Proof of concept: one hybrid skill (evidence-auditor) with output validator
6. `.github/workflows/ci.yml` expanded with schema validation job
7. Updated PI (model identity, workflow references, Python tool calling pattern)
8. Updated workplan-orchestrator (Stage A workflows added, Phase 2B workflows marked dormant)

### Session 1: A3 with entity-driven approach (first of 6–8)

Proves the pattern: governance document + schema + validator + sample conversion, all in one session. Subsequent governance phases follow the same pattern.

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| Infrastructure session runs long (>1 session) | Time-box to scaffolding + one entity type (Specification). Remaining entity schemas follow in A3. |
| Pydantic models over-constrain future decisions | Schema versioning. Breaking changes managed by migration scripts. |
| Python tool calling adds token overhead per session | Python scripts are token-cheap to call (~20 tokens for bash_tool invocation). Net savings from replacing prose SKILL.md reads (~500–2000 tokens each). |
| CI pipeline expansion slows push cycle | Path filtering: new jobs only trigger on `data/` and `schemas/` changes. |
| Three meta-sessions before A3 content work | Two, not three. This scope document is the review. Next session: infrastructure pour + PI/orchestrator update. Then A3. |

---

## 8. Decision Required

This scope document is the review artifact. Two decisions:

1. **Adopt the three-layer approach** — data + execution + ecosystem updated together, not incrementally.
2. **Commit as CO-0008** — a Change Order, not an amendment to v3. This is a methodology change that affects how all subsequent phases execute, not a cell-level budget revision.

If adopted: next session is the infrastructure pour. Deliverables per §6.
