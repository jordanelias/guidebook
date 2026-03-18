# Skill Ecosystem Reference
**Project:** Guidebook for Accessible Design
**Last updated:** 2026-03-17 17:00
**Skills:** 29 registered · 3 retired

---

## Architecture

### Two-layer design
| Layer | What lives here | Access pattern |
|---|---|---|
| **Project Files** (`/mnt/project/`) | Skill definitions (29 `.md` files) | Auto-injected into context — no API call needed |
| **GitHub** (`jordanelias/guidebook`) | Persistent state (5 files + 5 reference files) | GET before read · GET+PUT for write · PAT required |

### Why this split
Skills are read frequently and benefit from auto-injection. State files need to persist across sessions and benefit from git history. Putting state on GitHub and skills in Project Files gives the lowest token overhead for the most common operation (skill execution) while ensuring session continuity.

---

## Session Flow

### Every new conversation
1. `workplan-orchestrator` runs **Session Start Protocol** (mandatory, cannot skip):
   - GET `session_log.md` → surface last session + next action
   - GET `gap_register.md` → surface open P1 items
   - GET `references/project-standards.md` → load rules into context
2. User confirms before any work resumes
3. Task intake → workflow selection → execution

### Session end
1. `session-consolidator` runs:
   - Extracts patterns → appends rules to `project-standards.md` (PUT)
   - Appends YAML block to `session_log.md` (PUT)
2. Fallback: if GitHub write fails, outputs YAML in chat for manual paste

---

## GitHub State Files

| File | Writer | Reader | Purpose |
|---|---|---|---|
| `session_log.md` | session-consolidator | workplan-orchestrator | Rolling YAML resumption blocks |
| `gap_register.md` | workplan-orchestrator + contributing skills | workplan-orchestrator | Typed gap register — append only |
| `references/project-standards.md` | session-consolidator | workplan-orchestrator + all skills | Canonical rules |
| `references/search-log.md` | research-log-manager | research-log-manager | Per-topic search coverage index |
| `references/best-practices-compendium.md` | research-log-manager | research-log-manager | Synthesised BPC entries per slug |
| `references/section-map.md` | haiku-chunker · guidebook-auditor | all analysis skills | Document structure map |
| `references/terminology.md` | guidebook-auditor (Mode B) | guidebook-auditor | Deprecated/flagged term register |
| `references/economics-sources.md` | economics-researcher | economics-researcher | Verified funding + cost data |
| `references/ref-patterns.md` | cross-reference-resolver | cross-reference-resolver | Cross-reference pattern registry |
| `references/format-rules.md` | author | guidebook-auditor (Mode A) | Format rules — must be populated before Mode A |

---

## Skill Registry

### Orchestration
| Skill | Model | Role | GitHub writes |
|---|---|---|---|
| `workplan-orchestrator` | — | Session start · workflow routing · gap register | `gap_register.md` |
| `session-consolidator` | Sonnet 4.6 | Session end · YAML handoff | `session_log.md` · `project-standards.md` |

### Document Processing
| Skill | Model | Role | GitHub writes |
|---|---|---|---|
| `haiku-chunker` | Haiku 4.5 | Chunk docs >500 lines · build section map | `references/section-map.md` |
| `structure-auditor` | Haiku 4.5 | Heading hierarchy · structural violations | `gap_register.md` (escalation) |
| `markdown-formatter` | Haiku 4.5 | Heading levels · markdown consistency | — |
| `chunk-assembler` | Haiku/Sonnet | Reassemble chunks in section-map order | — |
| `find-and-replace` | Haiku/Sonnet | Bulk text substitution with classification | `gap_register.md` |
| `table-formatter` | Haiku 4.5 | Table repair and standardisation | — |
| `fix-linebreaks` | Haiku 4.5 | Join broken prose lines from DOCX conversion | — |

### Content Analysis
| Skill | Model | Role | GitHub writes |
|---|---|---|---|
| `guidebook-auditor` | Haiku (A/C/E) · Sonnet (B/D) | Format · consistency · structure | `section-map.md` · `terminology.md` |
| `content-gap-analyzer` | Sonnet 4.6 | Population and topic coverage gaps | `gap_register.md` |
| `framing-checker` | Sonnet 4.6 | Social model framing · CRPD alignment | — |
| `evidence-auditor` | Sonnet 4.6 | Evidence stratification · overclaiming | — |
| `item-consolidation-analyzer` | Sonnet 4.6 | Merge/split/scope items | — |
| `version-diff` | Sonnet 4.6 | Semantic diff between versions | — |

### Writing and Specification
| Skill | Model | Role | GitHub writes |
|---|---|---|---|
| `prose-style-checker` | Sonnet 4.6 | Register · concision · voice | — |
| `item-specification-writer` | Sonnet 4.6 | Draft and revise specifications | — |
| `vol2-item-formatter` | Sonnet 4.6 | Format and validate Vol 2 item blocks | — |
| `practice-note-generator` | Sonnet 4.6 | OT practitioner field tools | — |

### Research and Verification
| Skill | Model | Role | GitHub writes |
|---|---|---|---|
| `citation-verifier` | Sonnet 4.6 | Citation audit · hallucination screen | — |
| `multilingual-research` | Sonnet 4.6 + web | 14-language search · delegates writes to research-log-manager | via research-log-manager |
| `research-log-manager` | Sonnet 4.6 | CHECK · LOG · RETRIEVE for search-log + BPC | `search-log.md` · `BPC.md` |
| `literature-review-planner` | Sonnet 4.6 + web | Systematic review protocol · PRISMA | — |
| `economics-researcher` | Sonnet 4.6 + web | Economics evidence · funding programmes | `economics-sources.md` |
| `jurisdiction-tracker` | Sonnet 4.6 + web | Standards currency by jurisdiction | — |

### Reference Management
| Skill | Model | Role | GitHub writes |
|---|---|---|---|
| `cross-reference-resolver` | Haiku/Sonnet | Audit and repair internal cross-references | `ref-patterns.md` |
| `volii-validator` | Haiku/Sonnet | Item code validation | — |
| `supplemental-integrator` | Haiku/Sonnet | Integrate supplementary volumes | — |

### Reporting
| Skill | Model | Role | GitHub writes |
|---|---|---|---|
| `critique-report-writer` | Sonnet 4.6 | Formal critique and review reports | — |

**Retired:** `vol1-corrections-writer` · `vol2-revision`

---

## Workflow Reference

| Workflow | Skill sequence |
|---|---|
| **Full Section Review** | haiku-chunker → [structure-auditor · markdown-formatter · guidebook-auditor · content-gap-analyzer · framing-checker · evidence-auditor] → [research-log-manager CHECK · multilingual-research · citation-verifier · research-log-manager LOG] → [guidebook-auditor C · volii-validator · cross-reference-resolver] → prose-style-checker → critique-report-writer |
| **Item Specification** | item-consolidation-analyzer → item-specification-writer → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator |
| **Structural Change** | structure-auditor → markdown-formatter → cross-reference-resolver → find-and-replace → guidebook-auditor A |
| **Bulk Text Change** | find-and-replace (all six stages) |
| **Citation Audit** | citation-verifier → critique-report-writer §7 |
| **Evidence Gap** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → gap list |
| **Format Check** | structure-auditor → markdown-formatter → guidebook-auditor A+B |
| **Framing + Style** | framing-checker → prose-style-checker |
| **New Chapter** | content-gap-analyzer → research-log-manager CHECK → multilingual-research → research-log-manager LOG → citation-verifier → item-specification-writer → evidence brief |
| **Research Retrieval** | research-log-manager CHECK → if COMPLETE: retrieve BPC · if PARTIAL/STALE/NOT FOUND: multilingual-research → LOG |
| **Version Comparison** | version-diff on two aligned chunks |
| **Supplementary Volume** | supplemental-integrator → [find-and-replace · volii-validator · cross-reference-resolver] → guidebook-auditor A |
| **Document Assembly** | chunk-assembler → cross-reference-resolver → guidebook-auditor A |
| **Session Wrap** | session-consolidator |

**Parallel rule:** L2 and L4 agents run independently. No L2/L4 agent takes another's output as input within the same level.

---

## Key Design Principles

1. No file names in skill body — references belong in session-log YAML or workplan
2. No completed-task references — past decisions belong in `project-standards.md` or `gap_register.md`
3. No version-locked language — use structural roles
4. One skill, one process — audit and correction are separate skills
5. BAR is not a main-taxonomy code — no skill routes BAR items to Volume 2
6. All timestamps: `YYYY-MM-DD HH:MM`
7. Skills live in Project Files — GitHub holds state only. Update skills by uploading to Project Files.

---

## Skill Update Process

When a skill is amended:
1. Produce updated `.md` file (outputs directory)
2. Push copy to GitHub (version history)
3. Upload to Project Files to replace old version — **this is what Claude runs from**

Skills on GitHub are version history only. Project Files are authoritative for execution.
