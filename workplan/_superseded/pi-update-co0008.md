<!-- SUPERSEDED 2026-05-11 -->
> **⚠ SUPERSEDED:** This workplan is replaced by `governance/project-instructions-v10_8.md` (ADOPTED 2026-05-11 in session_2026-05-11h, per PI v10.8 standing rule #6). PI updates are now governed by `governance/project-instructions-v10_8.md` and `decisions/PI-update-needed.md` (the v10.8 deployment instructions). Do not use for forward work. Preserved here as historical record. See `governance/project-instructions-v10_8.md` §Appendix E for the full supersession map.

---

# PI Update — CO-0008 Infrastructure Pour

**Date:** 2026-04-26
**Status:** READY TO APPLY
**Applies to:** Project Instructions in claude.ai conversation settings

---

## Changes Required

### 1. Architecture section — model identity

**Current:**
```
- Conversation model: Sonnet 4.6. All assembly, drafting, research, coordination, GitHub operations.
- Opus 4.6: best-practice synthesis, evidence arbitration, cross-referential judgment.
```

**Replace with:**
```
- Opus 4.6: primary model for all work. Assembly, drafting, research, coordination, GitHub operations, best-practice synthesis, evidence arbitration, cross-referential judgment.
- Sonnet 4.6: available for sub-model calls in artifacts (haiku-tier and sonnet-tier tasks per User Preferences §Model Routing).
- Python-backed skills: called via bash_tool. Scripts in scripts/ and skills/*.validate.py enforce constraints mechanically — Claude calls the script, the script rejects invalid output.
- Hybrid skills: Claude reads SKILL.md for judgment guidance, produces YAML output, calls the output validator (skills/{name}_validate.py), fixes errors before committing.
```

### 2. Session Protocol — add Step 2b

**After Step 2 (gap register), add:**
```
2b. Data health check: if data/ directory exists:
    pip install pydantic pyyaml --break-system-packages -q
    python3 scripts/validate_schema.py --quick
Container does not persist pip packages — install before every Python tool call.
```

### 3. Session Protocol — Step 4 Task Intake

**Add to workflow list:**
```
- Governance + Code: [read prior governance docs] → [draft governance document] → [write Pydantic schema] → [write validator script] → [run conversion on sample data] → [fix edge cases] → [commit all: governance + schema + validator + converter]
- Infrastructure Build: [throughline analysis] → [schema scaffolding] → [validator runner] → [proof-of-concept conversion] → [CI expansion] → [commit]
```

### 4. Standing Rules — add

```
11. Python-backed skills are called via bash_tool, not loaded as prose SKILL.md. The script enforces constraints; Claude does not interpret the rules — the code does.
12. Hybrid skills have two components: SKILL.md (judgment guidance) + _validate.py (output validator). Claude reads the SKILL.md, produces output, calls the validator, fixes errors before committing.
13. Every Stage A governance phase co-produces: governance document + Pydantic schema + CI validator + sample conversion script. Neither prose nor code is complete without the other.
14. Container does not persist pip packages. Run `pip install pydantic pyyaml --break-system-packages -q` before any Python tool call in each session. Never assume packages from a prior session exist.
```

### 5. Effort guide reference — note

**Add to §Effort:**
```
Python-backed skills: effort = execution time, not reasoning depth. Set effort 50 for pure Python tool invocations (scripts/validate_schema.py, scripts/convert/*.py). Set effort per skill table for the judgment component of hybrid skills.
```

---

## Deferred Changes (apply after A3)

- Phase 2B workflows (Item Specification, Full Section Review, Research Retrieval, etc.) marked as dormant in orchestrator. PI does not need to change for this — orchestrator handles it.
- Entity type registration: as new entity schemas are added (sources, connections, populations), validate_schema.py's ENTITY_REGISTRY is updated — no PI change needed.
