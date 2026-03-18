# Guidebook Project — Ecosystem Audit & Process Reference
**Date:** 2026-03-17 17:30
**Scope:** Full skill ecosystem audit · GitHub integration review · Model selection · Evidence hierarchy alignment · Session management

---

## 1. Ecosystem Audit Findings

### 1.1 GitHub Integration — Status

| File | Location | Writer | Status |
|---|---|---|---|
| `session_log.md` | GitHub root | session-consolidator | ✓ Live |
| `gap_register.md` | GitHub root | workplan-orchestrator | ✓ Live |
| `references/project-standards.md` | GitHub | session-consolidator | ✓ Live |
| `references/search-log.md` | GitHub | research-log-manager | ✓ Live |
| `references/best-practices-compendium.md` | GitHub | research-log-manager | ✓ Live |

**Skills:** Definitions in Project Files (`/mnt/project/`). GitHub holds copies for version history only. Never read skills from GitHub at runtime.

**PAT lifecycle:** Provided once per session at conversation open. All GitHub-writing skills reference `Project Instructions §GitHub API` — the protocol is not repeated in individual skill files.

**Shared GitHub read/write protocol** is defined once in Project Instructions §GitHub API. Skills reference it by pointer. No duplication.

---

### 1.2 Skills — Relevancy Audit

| Skill | Status | Notes |
|---|---|---|
| `workplan-orchestrator` | ✓ Active | Session Start Protocol now GitHub-backed |
| `session-consolidator` | ✓ Active | Writes to GitHub; fallback to chat output |
| `haiku-chunker` | ✓ Active | Required before every full-doc analysis |
| `structure-auditor` | ✓ Active | Haiku 4.5; structural extraction only |
| `markdown-formatter` | ✓ Active | Haiku 4.5; heading/formatting correction |
| `chunk-assembler` | ✓ Active | Needed for document assembly workflow |
| `find-and-replace` | ✓ Active | 82× and 12× deferred items still open |
| `table-formatter` | ✓ Active | Required after any bulk replacement pass |
| `guidebook-auditor` | ✓ Active | Mixed Haiku/Sonnet by mode |
| `content-gap-analyzer` | ✓ Active | Feeds gap_register on GitHub |
| `framing-checker` | ✓ Active | Sonnet 4.6 only; CRPD-grounded |
| `evidence-auditor` | ✓ Active | **Evidence hierarchy updated** — see §1.3 |
| `item-consolidation-analyzer` | ✓ Active | Pre-finalisation tool |
| `version-diff` | ✓ Active | Used for v8→v8.x comparisons |
| `prose-style-checker` | ✓ Active | Run after framing-checker |
| `item-specification-writer` | ✓ Active | Core writing tool |
| `practice-note-generator` | ✓ Active | OT field tools; low-frequency use |
| `citation-verifier` | ✓ Active — PROVISIONAL | Full bibliography unavailable |
| `multilingual-research` | ✓ Active | **Model updated** — see §1.4 |
| `research-log-manager` | ✓ Active | GitHub-backed; defined in Project Instructions only |
| `literature-review-planner` | ✓ Active | Used for thesis/research planning phase |
| `economics-researcher` | ✓ Active | economics-sources.md not yet on GitHub — Tier B |
| `jurisdiction-tracker` | ✓ Active | Run once per edition |
| `cross-reference-resolver` | ✓ Active | Required after any structural change |
| `volii-validator` | ✓ Active — PROVISIONAL | Application volume unavailable |
| `supplemental-integrator` | ✓ Active | BAR integration complete; reserved for future supp volumes |
| `fix-linebreaks` | ✓ Active | DOCX-to-MD pipeline utility |
| `vol2-item-formatter` | ✓ Active | Volume 2 item output standardisation |

**No skills retired this audit.** All skills map to active guidebook work or open blockers.

---

### 1.3 Evidence Hierarchy — Corrected

The guidebook (§1.5) defines its own evidence hierarchy, distinct from the standard clinical hierarchy. All skills must use this version.

| Tier | Type | Guidebook basis |
|---|---|---|
| **1a** | OT clinical research (intervention-tested, person-environment-occupation) | §1.5 Tier 1 primary |
| **1b** | Lived experience and participatory design research (CRPD Art. 4.3) | §1.5 Co-primary Tier 1 |
| **2** | NGO and advocacy organisation best-practice guidelines (disabled community-developed) | §1.5 Tier 2 |
| **3** | Systematic reviews and meta-analyses | §1.5 Tier 3 |
| **4** | RCTs and controlled studies | §1.5 Tier 4 |
| **5** | Regulatory documents, building codes, professional standards, clinical guidelines | New — mapped from prior Tier 5 |
| **6** | Grey literature, single case reports, single-source findings | New — mapped from prior Tier 5 |

**Key changes from prior hierarchy:**
- Tiers 1a/1b reflect CRPD Art. 4.3 co-primary status of lived experience — not subordinate to clinical research on experiential outcomes
- NGO/advocacy guidelines (Tier 2) rank above systematic reviews because they encode lived experience validity
- Regulatory documents separated from grey literature: Tier 5 (codes/standards) vs Tier 6 (single-source/grey)
- Standard clinical hierarchy (RCT at top) is **not used** in this project

**Traffic-light tagging:**
- 🟢 Tiers 1a, 1b, 2 — high confidence
- 🟡 Tiers 3, 4 — moderate confidence
- 🔴 Tiers 5, 6 — low confidence; flag for upgrade or caveat

---

### 1.4 Model Selection — Extended Thinking

**When to use Sonnet 4.6 extended thinking:**

Extended thinking is appropriate when the task requires multi-step reasoning over ambiguous or conflicting evidence before reaching a conclusion — not for synthesis of clear findings.

| Task | Model | Rationale |
|---|---|---|
| Structural extraction, chunking, section mapping | Haiku 4.5 | Pattern matching; no judgment required |
| Format correction, markdown, heading fixes | Haiku 4.5 | Rule application; no judgment |
| Table repair, find-and-replace discovery | Haiku 4.5 | Extraction only |
| Framing audit, evidence stratification, citation judgment | Sonnet 4.6 | Judgment required; not multi-step reasoning |
| Prose style, item specification drafting | Sonnet 4.6 | Writing quality; not extended reasoning |
| Gap analysis, cross-reference resolution (standard) | Sonnet 4.6 | Standard synthesis |
| **Multilingual research synthesis** (≥6 languages, conflicting findings) | **Sonnet 4.6 extended** | Cross-language contradiction resolution requires holding multiple conflicting evidence streams |
| **Evidence hierarchy adjudication** (Tier 1a vs 1b conflict; lived experience vs clinical divergence) | **Sonnet 4.6 extended** | Normative reasoning over evidence conflict |
| **Complex item specification** (multiple populations, conflicting requirements, Part IV conflicts) | **Sonnet 4.6 extended** | Multi-constraint resolution |
| **Literature review planning** (systematic protocol design) | **Sonnet 4.6 extended** | Research design reasoning |
| **Version diff** (semantic regression detection) | **Sonnet 4.6 extended** | Subtle argument-level change detection |
| Session consolidation, rule extraction | Sonnet 4.6 | Pattern recognition; not extended reasoning |
| Economics research, jurisdiction tracking | Sonnet 4.6 + web | Retrieval + synthesis; not extended reasoning |

**Rule:** Use extended thinking when the task involves resolving contradiction or designing under competing constraints. Do not use for retrieval, formatting, or straightforward synthesis.

---

### 1.5 Session Cutoff — Updated Protocol

**Trigger:** 95% of conversation context OR 95% of session token budget — whichever is reached first.

**Action (mandatory):**
1. Cease any task <90% complete. Do not attempt to finish.
2. Write stage checkpoint note: what was being done, what line/section/item was reached, what remains.
3. Invoke `session-consolidator` — write full YAML block to GitHub.
4. Output to chat:
   - In-progress work product (whatever exists, clearly labelled `[DRAFT — CUT AT {stage}]`)
   - Stage note: `Stopped at: {skill} · {section/line} · Remaining: {description}`
   - YAML resumption block (also written to GitHub)
5. Instruct user: "Start a new conversation and provide your GitHub PAT. workplan-orchestrator will read the session log and resume from this point."

**Never:** silently drop in-progress work. Never summarise instead of outputting the actual draft.

---

### 1.6 Staleness Threshold

Updated to **180 days** across all references to search log staleness. Applies to `research-log-manager` CHECK and BPC entries.

---

### 1.7 Duplication Removed This Audit

| Duplication | Resolution |
|---|---|
| GitHub API protocol repeated in 3 skill files | Defined once in Project Instructions §GitHub API; skills reference by pointer |
| Workflow table in workplan-orchestrator + Project Instructions | Defined once in Project Instructions; workplan-orchestrator references by pointer |
| Evidence hierarchy defined in multilingual-research + evidence-auditor + Project Instructions | Canonical definition now in Project Instructions §Evidence Hierarchy; skills reference it |
| Session-close YAML schema in session-consolidator + workplan-orchestrator + Project Instructions | Defined once in Project Instructions §Session-Close YAML; referenced by pointer |

---

## 2. Workflow Flowchart

```
╔══════════════════════════════════════════════════════════════╗
║              SESSION START (every new conversation)          ║
╠══════════════════════════════════════════════════════════════╣
║  1. Prompt user for GitHub PAT                               ║
║  2. GET session_log.md → report last session + next action   ║
║  3. GET gap_register.md → surface OPEN P1 items              ║
║  4. GET references/project-standards.md → load rules         ║
║  5. Confirm with user before resuming                        ║
╚══════════════════════════╤═══════════════════════════════════╝
                           │
              ┌────────────▼────────────┐
              │     TASK INTAKE         │
              │  New task → select      │
              │  workflow below         │
              │  Resumed → go to        │
              │  next_action in YAML    │
              └────────────┬────────────┘
                           │
        ┌──────────────────▼──────────────────────────────────┐
        │              WORKFLOW SELECTION                       │
        ├─────────────────┬──────────────┬─────────────────────┤
        │  FULL SECTION   │    ITEM      │   STRUCTURAL /      │
        │  REVIEW         │    SPEC      │   BULK TEXT         │
        └────────┬────────┘      │       └──────────┬──────────┘
                 │               │                  │
    ┌────────────▼────────┐      │      ┌───────────▼──────────┐
    │  L1: haiku-chunker  │      │      │ structure-auditor    │
    │  → section map      │      │      │ → markdown-formatter │
    │  + chunks           │      │      │ → cross-ref-resolver │
    └────────────┬────────┘      │      │ → find-and-replace   │
                 │               │      │ → guidebook-auditor A│
    ┌────────────▼────────┐      │      └──────────────────────┘
    │  L2 PARALLEL        │      │
    │  ─────────────────  │      │      ┌──────────────────────┐
    │  structure-auditor  │      │      │  RESEARCH RETRIEVAL  │
    │  markdown-formatter │      │      │  research-log-mgr    │
    │  guidebook-auditor  │      │      │  CHECK               │
    │  content-gap-anlzr  │      │      │  ├─ COMPLETE →       │
    │  framing-checker    │      │      │  │  retrieve BPC     │
    │  evidence-auditor   │      │      │  └─ PARTIAL/STALE/   │
    └────────────┬────────┘      │      │     NOT FOUND →      │
                 │               │      │     multilingual-    │
    ┌────────────▼────────┐      │      │     research (ext.)  │
    │  L3                 │      │      │     → LOG            │
    │  research-log-mgr   │      │      └──────────────────────┘
    │  CHECK              │      │
    │  multilingual-      │      │      ┌──────────────────────┐
    │  research (ext.)    │      │      │  CITATION AUDIT      │
    │  citation-verifier  │      │      │  citation-verifier   │
    │  research-log-mgr   │      │      │  → critique-report   │
    │  LOG                │      │      │    -writer §7        │
    └────────────┬────────┘      │      └──────────────────────┘
                 │               │
    ┌────────────▼────────┐      │      ┌──────────────────────┐
    │  L4 PARALLEL        │      │      │  SESSION WRAP        │
    │  ─────────────────  │      │      │  session-consolidator│
    │  guidebook-auditor C│      │      │  → PUT session_log   │
    │  volii-validator    │      │      │  → PUT project-stds  │
    │  cross-ref-resolver │      │      │  → output YAML +     │
    └────────────┬────────┘      │      │    in-progress work  │
                 │               │      └──────────────────────┘
    ┌────────────▼────────┐      │
    │  prose-style-checker│      │
    │  critique-report-   │      │
    │  writer             │      │
    └────────────┬────────┘      │
                 │               │
    ┌────────────▼──────────────▼────────────────────────────┐
    │              95% CONTEXT/TOKEN MONITOR                  │
    │  If triggered:                                          │
    │  1. Stop current task                                   │
    │  2. Output in-progress work [DRAFT — CUT AT {stage}]   │
    │  3. session-consolidator → GitHub + YAML to chat        │
    │  4. Instruct user to start new conversation            │
    └─────────────────────────────────────────────────────────┘
```

---

## 3. Canonical Reference Tables

### Evidence Hierarchy (all skills — authoritative)

| Tier | Type | Tag | Confidence |
|---|---|---|---|
| 1a | OT clinical research — intervention-tested, person-environment-occupation | `[T1a-OT]` | 🟢 |
| 1b | Lived experience and participatory design research (CRPD Art. 4.3) | `[T1b-LE]` | 🟢 |
| 2 | NGO/advocacy organisation best-practice guidelines (community-developed) | `[T2-NGO]` | 🟢 |
| 3 | Systematic reviews and meta-analyses | `[T3-SR]` | 🟡 |
| 4 | RCTs and controlled studies | `[T4-RCT]` | 🟡 |
| 5 | Regulatory documents, building codes, professional standards | `[T5-REG]` | 🔴 |
| 6 | Grey literature, single case reports, single-source findings | `[T6-GREY]` | 🔴 |

**Lived experience evidence is co-primary (Tier 1b) — never subordinate to clinical research on experiential outcomes.**
**Regulatory documents (Tier 5) are a floor, not a ceiling.**

---

### Model Selection (authoritative)

| Task type | Model |
|---|---|
| Structural extraction, chunking, heading correction, table repair, find-and-replace discovery | Haiku 4.5 |
| Framing audit, evidence stratification, citation judgment, prose style, gap analysis, item drafting, session consolidation | Sonnet 4.6 |
| Multilingual research synthesis (≥6 languages, conflicting findings) | Sonnet 4.6 extended thinking |
| Evidence hierarchy adjudication (Tier 1a vs 1b conflict; lived experience vs clinical divergence) | Sonnet 4.6 extended thinking |
| Complex item specification (multiple populations, Part IV conflicts) | Sonnet 4.6 extended thinking |
| Literature review protocol design | Sonnet 4.6 extended thinking |
| Semantic version diff (argument-level regression detection) | Sonnet 4.6 extended thinking |

---

### GitHub State Files

| File | Managed by | Rule |
|---|---|---|
| `session_log.md` | session-consolidator | Append-only. Never overwrite closed entries. |
| `gap_register.md` | workplan-orchestrator + skills | Append OPEN. Never overwrite CLOSED. |
| `references/project-standards.md` | session-consolidator | Append-only. |
| `references/search-log.md` | research-log-manager | Overwrite slug entry on LOG. |
| `references/best-practices-compendium.md` | research-log-manager | Overwrite `## {slug}` section on LOG. |

**Always GET before PUT. Capture SHA. On 409: re-GET and retry once. On failure: output to chat.**

---

### Session Cutoff Protocol

**Trigger:** 95% conversation context OR 95% token budget.

**Output sequence:**
1. `[DRAFT — CUT AT {skill} · {section/line}]` — in-progress work product
2. Stage note: what was done, where stopped, what remains
3. YAML resumption block (written to GitHub AND output to chat)
4. User instruction to start new conversation with PAT

---

### Staleness: 180 days (search log entries)

---

## 4. Required Project File Uploads

Upload these files to replace current Project File versions:

| File | Change |
|---|---|
| `workplan-orchestrator_SKILL.md` | GitHub Session Start Protocol; workflow table by pointer |
| `session-consolidator_SKILL.md` | GitHub write protocol; fallback output |
| `research-log-manager_SKILL.md` | GitHub read/write; 180-day staleness |
| `multilingual-research_SKILL.md` | Extended thinking flag; corrected evidence hierarchy (Tiers 1a/1b/2/3/4/5/6); 14-language early-close gate preserved |
| `evidence-auditor_SKILL.md` | Corrected evidence hierarchy |

**Project Instructions** must also be updated in the Project Instructions field (not a file upload).

---

## 5. Open Items Not Addressed This Session

These require separate sessions or author input:

| Item | Priority | Status |
|---|---|---|
| `references/economics-sources.md` → GitHub | P2 | Tier B — not yet migrated |
| `references/ref-patterns.md` → GitHub | P2 | Tier B — not yet migrated |
| `references/section-map.md` → GitHub | P2 | Tier B — not yet migrated |
| Appendix A Emergency Evacuation | P1-01 | Author must supply |
| Levine et al. (2024) DOI verification | P1-06 | citation-verifier required |
| 82× "Chapter C" → "Part VIII §8.4" | Deferred | find-and-replace + manual review |
| 12× "Part VIII (case studies)" → "Part IX" | Deferred | find-and-replace |
| `sessions_3to6.md` BAR refs (~50) | Deferred | Not yet processed |
| GAP-PARTV-RANGES audit | Deferred | Do not execute without explicit instruction |
