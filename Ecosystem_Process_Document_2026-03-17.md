# Guidebook Review System — Process Document
**Version:** 2026-03-17  
**Scope:** Full ecosystem audit — coordination, GitHub integration, model selection, evidence hierarchy, session management

---

## 1. Ecosystem Audit Findings

### 1.1 Skills — Status After Audit

| Skill | Status | Action |
|---|---|---|
| `workplan-orchestrator` | ✅ Active | Updated this session — upload to Project Files |
| `session-consolidator` | ✅ Active | Updated this session — upload to Project Files |
| `research-log-manager` | ✅ Active | Updated this session — upload to Project Files |
| `multilingual-research` | ✅ Active | Evidence hierarchy needs update (see §3) |
| `haiku-chunker` | ✅ Active | No changes needed |
| `structure-auditor` | ✅ Active | No changes needed |
| `markdown-formatter` | ✅ Active | No changes needed |
| `guidebook-auditor` | ✅ Active | No changes needed |
| `content-gap-analyzer` | ✅ Active | No changes needed |
| `framing-checker` | ✅ Active | No changes needed |
| `evidence-auditor` | ✅ Active | Evidence hierarchy needs update (see §3) |
| `citation-verifier` | ✅ Active | No changes needed |
| `prose-style-checker` | ✅ Active | No changes needed |
| `item-specification-writer` | ✅ Active | No changes needed |
| `item-consolidation-analyzer` | ✅ Active | No changes needed |
| `vol2-item-formatter` | ✅ Active | Distinct from item-specification-writer; retained |
| `chunk-assembler` | ✅ Active | No changes needed |
| `find-and-replace` | ✅ Active | No changes needed |
| `table-formatter` | ✅ Active | No changes needed |
| `cross-reference-resolver` | ✅ Active | No changes needed |
| `volii-validator` | ✅ Active | No changes needed |
| `supplemental-integrator` | ✅ Active | No changes needed |
| `practice-note-generator` | ✅ Active | No changes needed |
| `version-diff` | ✅ Active | No changes needed |
| `literature-review-planner` | ✅ Active | Retained — used for thesis/research workstream |
| `economics-researcher` | ✅ Active | No changes needed |
| `jurisdiction-tracker` | ✅ Active | No changes needed |
| `fix-linebreaks` | 🔴 Dormant | DOCX→MD conversion phase complete. V8.8 is clean markdown. Retire from active registry; retain file for reactivation if new DOCX conversion needed. |
| `vol1-corrections-writer` | 🔴 Retired | Already marked retired. Remove from all references. |
| `vol2-revision` | 🔴 Retired | Already marked retired. Remove from all references. |

**Net active skills: 27. Retired: 2. Dormant (retained): 1.**

---

### 1.2 GitHub Integration — Gap Audit

| File | Status | Notes |
|---|---|---|
| `session_log.md` | ✅ Live | Written by session-consolidator |
| `gap_register.md` | ✅ Live | Written by workplan-orchestrator + skills |
| `references/project-standards.md` | ✅ Live | Written by session-consolidator |
| `references/search-log.md` | ✅ Live | Written by research-log-manager |
| `references/best-practices-compendium.md` | ✅ Live | Written by research-log-manager |
| `references/economics-sources.md` | ⚠️ Missing | economics-researcher references this; needs scaffolding |
| `references/ref-patterns.md` | ⚠️ Missing | cross-reference-resolver references this; needs scaffolding |
| `references/section-map.md` | ⚠️ Missing | haiku-chunker writes this; needs scaffolding |
| `references/terminology.md` | ⚠️ Missing | guidebook-auditor Mode B references this; needs scaffolding |
| `references/format-rules.md` | ⚠️ Missing | guidebook-auditor Mode A requires this; needs scaffolding |

**Action:** Scaffold five missing reference files on GitHub. Each skill that writes to these files should use the same GET→append→PUT protocol defined in §GitHub API.

---

### 1.3 Duplication Removed This Session
- GitHub API read/write protocol: was duplicated in 3 skills → now defined once in Project Instructions §GitHub API; skills reference it by pointer.
- Workflow reference table: was duplicated in workplan-orchestrator and Project Instructions → now canonical in Project Instructions; workplan-orchestrator points to it.
- Session-close YAML schema: was in 3 places → now canonical in Project Instructions.

---

## 2. Model Selection — Sonnet 4.6 vs Extended Thinking

### When to use Sonnet 4.6 (standard)
Tasks where the answer follows from applying a defined framework to available evidence. The skill provides the framework; the model applies it.

| Task type | Skills |
|---|---|
| Framing checks against known doctrine | framing-checker |
| Style and register audits | prose-style-checker |
| Gap analysis against known taxonomy | content-gap-analyzer |
| Item formatting and structure validation | vol2-item-formatter, item-consolidation-analyzer |
| Cross-reference discovery and repair | cross-reference-resolver, volii-validator |
| Citation existence checks | citation-verifier |
| Session management | workplan-orchestrator, session-consolidator |
| Economics evidence retrieval | economics-researcher |
| Jurisdiction standards tracking | jurisdiction-tracker |

### When to use Sonnet 4.6 Extended Thinking
Tasks requiring multi-step reasoning across ambiguous or conflicting evidence, where the correct answer is not determinable by framework application alone — the model must reason through tradeoffs.

| Task type | Skills | Rationale |
|---|---|---|
| Evidence stratification and overclaiming judgment | `evidence-auditor` | Must assess whether confidence level *matches* evidence quality — requires probabilistic reasoning across conflicting study designs |
| Cross-language synthesis with divergent findings | `multilingual-research` (synthesis step only) | Requires weighing incommensurable evidence across regulatory regimes and study traditions |
| New item specification with thin evidence base | `item-specification-writer` (when evidence tier <3) | Must reason through what can be responsibly claimed given evidence gaps |
| Systematic review protocol design | `literature-review-planner` | Requires reasoning about scope, search term adequacy, and inclusion criteria tradeoffs |
| Critique report writing on contested sections | `critique-report-writer` (contested evidence sections) | Requires holding multiple framings simultaneously and reasoning to a defensible position |

**Implementation note:** Extended thinking is not a separate model call — it is a parameter (`thinking: {type: "enabled", budget_tokens: N}`). Budget 8,000–16,000 tokens for evidence synthesis tasks; 4,000–8,000 for item specification with thin base. Standard Sonnet for everything else. Do not default to extended thinking — it has a significant token cost and is only warranted where reasoning depth materially improves output quality.

---

## 3. Evidence Hierarchy (Revised)

Aligned to guidebook doctrine: OT practice evidence and lived experience are primary.

| Tier | Type | Notes |
|---|---|---|
| **1** | OT practice evidence: systematic reviews, meta-analyses, clinical practice guidelines with OT authorship or OT population focus | Highest weight — directly practice-relevant |
| **2** | Lived experience evidence: participatory research, user studies, disability-led research, phenomenological studies | Co-primary with Tier 1 on experiential outcomes. Never subordinate to clinical research where lived experience is the subject of inquiry. |
| **3** | Controlled studies: RCTs, controlled trials, cohort studies, cross-sectional studies with disability population | |
| **4** | Expert consensus: professional standards, clinical guidelines (non-OT), Delphi studies, expert panels | |
| **5** | Regulatory and standards documents: building codes, accessibility standards, government technical guidance (ADA, ISO, DIN, etc.) | Normative, not empirical. Cite as floor/requirement, not as evidence of efficacy. |
| **6** | Grey literature and single sources: conference papers, unpublished reports, single case reports, manufacturer guidance, non-peer-reviewed documents | Flag explicitly. Use only where no higher-tier evidence exists. |

**Tagging:** Every source in every skill output must carry a tier tag: `[T1]` through `[T6]`.
**Staleness threshold:** 180 days. Entries in search-log older than 180 days → STALE on CHECK.
**Thin base:** <3 independent sources at Tier 1–4 for a given claim → flag `[THIN BASE — citation gap]`.

---

## 4. Session Cut-off Protocol

### Triggers (either condition fires the protocol)
- **Context usage hits 95%** of the conversation context window
- **Token usage hits 95%** of the session token budget

### Protocol — mandatory, no exceptions
When either trigger fires, Claude must:

1. **Stop** any task that is less than 90% complete. Do not attempt to finish it.
2. **Document in-progress state:**
   ```
   INTERRUPTED: {skill} on {file/chunk}
   Stage reached: {stage name}
   Last completed step: {step}
   Next step: {step}
   Notes: {any decisions made mid-task that affect resumption}
   ```
3. **Invoke session-consolidator** — write full session-close YAML to GitHub including the interruption record in `blockers`.
4. **Output to chat:**
   - Any in-progress work product (partial output, intermediate tables, working document) as a fenced code block or presented file
   - The interruption note above
   - Instruction: *"Start a new conversation. Provide your GitHub PAT. workplan-orchestrator will read session state and resume from the interruption point."*
5. **Do not summarise at length.** The YAML block on GitHub is the handoff. The chat output is the safety copy.

### Tasks that may be abandoned at cut-off (not resumed)
- Single-stage tasks where the output is fully presentable at their current state
- Checkpoints and audit logs (already written to GitHub)

### Tasks that must resume from interruption point
- Any multi-stage workflow where a later stage depends on an earlier stage's output
- Any GitHub write that was initiated but not confirmed

---

## 5. Workflow Flowchart

```
NEW CONVERSATION
      │
      ▼
┌─────────────────────────────────┐
│  workplan-orchestrator          │
│  SESSION START PROTOCOL         │
│  1. GET session_log → report    │
│  2. GET gap_register → P1 items │
│  3. GET project-standards       │
│  4. Confirm PAT                 │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
RESUME            NEW TASK
    │                 │
    ▼                 ▼
Confirm next    Select workflow
action from     (see table below)
YAML → execute  Confirm in ≤3 lines
                → execute
             │
             ▼
    ┌─────────────────┐
    │  CONTEXT/TOKEN  │◄── Monitor throughout
    │  ≥95% used?     │
    └────┬───────┬────┘
         │NO     │YES
         ▼       ▼
    Continue   CUT-OFF PROTOCOL
    task       (§4 above)
         │
         ▼
    Task complete?
         │
    ┌────┴────┐
    │YES      │NO (more stages)
    ▼         ▼
SESSION    Next stage
WRAP       (loop back)
    │
    ▼
session-consolidator
1. Review session
2. Extract patterns
3. Write rules → GitHub
4. Check research log hygiene
5. Write session YAML → GitHub
6. Report to user ≤5 lines
```

### Workflow Selection Table

| User intent | Workflow | Key skills |
|---|---|---|
| Review a section | Full Section Review | haiku-chunker → [L2 parallel] → [L3 research] → [L4 validation] → prose-style-checker → critique-report-writer |
| Write/revise a spec item | Item Specification | item-consolidation-analyzer → item-specification-writer → [framing · evidence] → prose-style-checker → volii-validator |
| Fix structure/headings | Structural Change | structure-auditor → markdown-formatter → cross-reference-resolver → find-and-replace → guidebook-auditor A |
| Mass text substitution | Bulk Text Change | find-and-replace (all 6 stages) |
| Check citations | Citation Audit | citation-verifier → critique-report-writer §7 |
| Find coverage gaps | Evidence Gap | content-gap-analyzer → research-log-manager CHECK → multilingual-research → LOG → gap list |
| Format/heading check only | Format Check | structure-auditor → markdown-formatter → guidebook-auditor A+B |
| Language/framing check | Framing + Style | framing-checker → prose-style-checker |
| Add new chapter | New Chapter | content-gap-analyzer → research-log-manager CHECK → multilingual-research → LOG → citation-verifier → item-specification-writer |
| Look up prior research | Research Retrieval | research-log-manager CHECK → if COMPLETE: retrieve BPC · else: multilingual-research → LOG |
| Compare two versions | Version Comparison | version-diff on aligned chunks |
| Add supplementary volume | Supplementary Volume | supplemental-integrator → [find-and-replace · volii-validator · cross-reference-resolver] → guidebook-auditor A |
| Assemble final document | Document Assembly | chunk-assembler → cross-reference-resolver → guidebook-auditor A |
| End session | Session Wrap | session-consolidator |

---

## 6. Actions Required

### Immediate (this session)
| # | Action | Who |
|---|---|---|
| 1 | Upload `workplan-orchestrator_SKILL.md` to Project Files | Jordan |
| 2 | Upload `session-consolidator_SKILL.md` to Project Files | Jordan |
| 3 | Upload `research-log-manager_SKILL.md` to Project Files | Jordan |
| 4 | Replace Project Instructions with updated version | Jordan |
| 5 | Scaffold 5 missing GitHub reference files | Claude (next task) |
| 6 | Update evidence hierarchy in `multilingual-research_SKILL.md` and `evidence-auditor_SKILL.md` | Claude (next task) |

### Deferred
| # | Action | Priority |
|---|---|---|
| 7 | Mark `fix-linebreaks` as dormant in Project Files (add header note, keep file) | P3 |
| 8 | Remove `vol1-corrections-writer` and `vol2-revision` references everywhere | P2 |
| 9 | Add extended thinking parameter guidance to `evidence-auditor`, `multilingual-research` (synthesis step), `item-specification-writer` | P2 |
