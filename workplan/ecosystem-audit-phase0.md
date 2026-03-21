# Ecosystem Audit and Phase 0: Skills-First Update Plan

**Date:** 2026-03-20 22:00
**Amends:** Workplan_v10-0_Comprehensive_2026-03-20.md
**Rationale:** The original workplan placed ecosystem updates in Phase 5 (after content). This is wrong. Every downstream session depends on skills functioning correctly with v10.0 architecture. Skills-first means every subsequent session is faster, more reliable, and produces commits that don't need manual repair.

---

## 1. Commit Pipeline Audit

### Current state: fragile

GitHub commits are performed via ad-hoc inline bash/python in every skill that writes state. There is **no standardised commit skill**. Each of the following skills reinvents the GET→decode→modify→encode→PUT cycle independently:

| Skill | Commits to | Method | Error handling |
|---|---|---|---|
| session-consolidator | `sessions/`, `references/project-standards.md`, `gap_register.md` | Inline python/bash | Retry once; fallback to fenced code block |
| research-log-manager | `references/search-log.md`, `references/best-practices-compendium.md`, `references/slug-registry.md` | Inline python/bash | Single retry; no fallback specified |
| workplan-orchestrator | `gap_register.md` | Inline bash | Single retry |
| toc-editor | `references/toc.md`, `references/change-orders/` | Inline python | Single retry |
| jurisdiction-tracker | `references/standards-registry.md` | Inline | Unknown |
| (ad hoc) | Any file during session work | Inline curl/python | Variable |

**Problems:**
1. **Token waste:** Each commit operation costs ~100–200 tokens for the inline script. Across a 23-session workplan with ~5 commits per session, that's ~11,500–23,000 tokens spent on boilerplate.
2. **Inconsistent error handling:** Some skills retry once, some don't. Some fall back to fenced code blocks, some silently fail. SHA conflicts on busy sessions are unhandled.
3. **No collision detection on writes:** Two skills writing to the same file in one session (e.g., gap_register from workplan-orchestrator and session-consolidator) can produce SHA conflicts.
4. **No commit log:** There's no record of what was committed per session beyond the session YAML — which is written last and may miss earlier commits.
5. **v10.0 file architecture multiplies the problem:** Going from 1 master document to ~30 Part/Category files means 30× more commit operations.

### Fix: `github-io` skill

A single standardised skill that all other skills call for GitHub operations. Every GET/PUT/list goes through one interface with consistent retry, collision handling, and logging.

---

## 2. Skill-by-Skill Audit

### 2.1 Skills requiring update for v10.0

| Skill | What's broken/stale | Impact if not fixed | Fix complexity |
|---|---|---|---|
| **workplan-orchestrator** | Part numbering map; workflow sequences reference old Part numbers; skill registry lists retired skills | Sessions start with wrong context; workflows reference non-existent Parts | Medium — ~200 lines to revise |
| **cross-reference-resolver** | Valid item code registry doesn't include K-category; §-reference patterns don't know about new numbering; no knowledge of per-Part file architecture | Phase 4 QA produces false positives/misses real breaks | Medium — update pattern inventory and valid targets |
| **structure-auditor** | Expected heading patterns assume old numbering (§6.x in Part 5, §7.x in Part 6, §9.x in Part 10) | Flags correct v10 numbering as errors | Low — update expected patterns |
| **framing-checker** | No BAR-in-Vol-I check; no ●/○ marker awareness | Misses the two most important v10.0 framing rules | Low — add two check rules |
| **evidence-auditor** | No ●/○ verification mode; doesn't know about EXPERT CONSENSUS disclosure requirement for OFS/PAIN | Can't audit the primary v10.0 evidence quality system | Low — add marker audit mode |
| **item-specification-writer** | No ●/○ marker requirement; no "[Illustration: to be provided]" instruction; doesn't know K-category template | Every item written without markers needs a second pass | Low — add to output template |
| **vol2-item-formatter** | Doesn't know ●/○ system or new Part numbering | Formats items to old spec | Low |
| **chunk-assembler** | File list assumes single master document, not per-Part files | Assembly fails or produces wrong order | Medium — needs new file manifest system |
| **session-consolidator** | Part numbering in YAML templates; reconciliation checks reference old structure | Session close YAMLs reference non-existent Parts | Low |

### 2.2 Skills that are fine as-is

| Skill | Why no change needed |
|---|---|
| haiku-chunker | Operates on any document; no structural assumptions |
| find-and-replace | Generic text substitution; no structural assumptions |
| fix-linebreaks | Line-level processing; no structural assumptions |
| table-formatter | Table-level processing; no structural assumptions |
| markdown-formatter | Heading-level only; patterns are generic |
| content-gap-analyzer | Population-level analysis; will pick up alphabetical sort naturally |
| prose-style-checker | Style rules are structural-agnostic |
| citation-verifier | Source-level; no Part numbering dependency |
| multilingual-research | Research protocol; no Part numbering dependency |
| research-log-manager | GitHub state files; no Part numbering dependency |
| literature-review-planner | Protocol design; no Part dependency |
| economics-researcher | Research; no Part dependency |
| jurisdiction-tracker | Standards tracking; no Part dependency |
| supplemental-integrator | Supp vol processing; independent |
| critique-report-writer | Report generation; adapts to input |
| practice-note-generator | Output-focused; no structural dependency |
| version-diff | Comparison tool; no structural assumptions |
| item-consolidation-analyzer | Item-level analysis; no structural dependency |
| keyword-lookup | Lookup utility |

### 2.3 New skills needed — with downstream benefit analysis

| Skill | Purpose | Sessions that benefit | Token savings estimate | Priority |
|---|---|---|---|---|
| **github-io** | Standardised GitHub GET/PUT/list/commit with retry, collision handling, base64, commit logging | ALL 23 sessions | ~15,000 tokens total (eliminating inline scripts) | **P0 — build first** |
| **bulk-renumber** | Takes a renumbering map (old §X.Y → new §Z.W) and applies it across all references in a file. Safer than find-and-replace for §-references because it understands context (won't rename §12.3 inside a URL or citation). | Sessions 7–8 (Phase 2 renumbering) + all Phase 3 cross-ref updates | ~2 sessions saved (renumbering is the highest-error-risk task) | **P0** |
| **evidence-marker** | Applies ●/○ markers to specifications; audits for completeness. Two modes: APPLY (classify each spec as evidence-based or inferred, insert marker) and AUDIT (scan for unmarked specs). | Sessions 10–15 (every Phase 3 content edit) + Session 21 (QA) | ~1 session saved + prevents rework from missed markers | **P0** |
| **file-splitter** | Splits a master document into per-Part/per-Category files at heading boundaries. Inverse of chunk-assembler. | Session 6 (Phase 2 decomposition) | ~0.5 sessions saved | **P0** |
| **citation-miner** | Backward + forward citation mining from confirmed Tier 1–2 sources. Deferred since v9.0. | Sessions 2–5 (all Phase 1 research) | Improves research quality; doesn't save sessions but produces better evidence | **P1** |
| **sensory-coherence-checker** | Checks a room specification set for sensory conflicts between items (e.g., acoustic treatment vs. wayfinding texture; lighting for VIS vs. NDV). Operationalises §4.3 Principle 2 that the critique flagged as described-but-not-operationalised (GAP-CR-16). | Sessions 12–13 (residential/non-residential matrices) + becomes a publication-quality QA tool | Fills a genuine content gap in the guidebook; also produces a practitioner tool | **P1** |
| **illustration-tracker** | Manages "[Illustration: to be provided]" placeholders. Simple registry: item code, illustration status (PENDING/DRAFTED/FINAL), description of required illustration. | Session 14–15 (Category files) onward | Prevents placeholder drift; low cost to build | **P2** |

---

## 3. Guidebook Content Areas That Need a Skill

| Content gap | Current state | Skill solution |
|---|---|---|
| **Sensory coherence audit** (GAP-CR-16) | §4.3 Principle 2 described but no tool | `sensory-coherence-checker` — produces a room-level conflict matrix that practitioners can use. Becomes both a QA skill AND a guidebook deliverable (include the method in §4.3 as a practitioner tool). |
| **POE protocol** (GAP-CR-19) | Part 12 presents case studies but no POE methodology | Extend `practice-note-generator` with a POE template mode — generates a post-occupancy evaluation checklist tied to the item codes used in the design. |
| **Bibliography population** | Master Bibliography is empty (12 lines) | Extend `citation-verifier` with a HARVEST mode — scan all Part files, extract every citation string, deduplicate, format to bibliography standard, output assembled bibliography. Currently citation-verifier only checks; it doesn't aggregate. |
| **Per-Part commit management** | Going from 1 file to ~30 files multiplies commit complexity | `github-io` handles this, but `chunk-assembler` also needs a manifest system that knows which files exist and their order. |

---

## 4. Revised Phase Sequence

The workplan must be resequenced:

```
Phase 0: Ecosystem (Sessions 1–2)     ← NEW: was Phase 5
Phase 1: Research (Sessions 3–7)       ← shifted +2
Phase 2: Structure (Sessions 8–10)     ← shifted +2
Phase 3: Content (Sessions 11–22)      ← shifted +2
Phase 4: QA + Assembly (Sessions 23–25) ← shifted +2
```

**Why Phase 0 first:**
- Every Phase 1 research session uses `research-log-manager` and `multilingual-research` — both commit to GitHub. `github-io` makes these commits reliable.
- Every Phase 2 structural task uses `find-and-replace`, `cross-reference-resolver`, and `toc-editor` — all need updated Part numbering knowledge.
- Every Phase 3 content edit uses `item-specification-writer`, `framing-checker`, `evidence-auditor` — all need ●/○ system awareness.
- Building `bulk-renumber` before Phase 2 prevents the highest-risk task (renumbering) from being done manually.
- Building `evidence-marker` before Phase 3 means markers are applied correctly the first time, not audited and repaired afterward.

---

## 5. Phase 0 Session Plan

### Session 0-A: Core Infrastructure Skills (est. 1 session)

**Build:**

1. **`github-io`** — Standardised GitHub operations skill
   - Actions: GET (file or directory), PUT (create or update), DELETE
   - Features: automatic base64 encode/decode; SHA management; single retry on 409; commit message convention enforcement; collision detection (two writes to same file in one session → warn); commit log (append to session working file)
   - Interface: all other skills call `github-io` by name for any GitHub operation instead of inline bash
   - Test: GET `references/project-standards.md`, append a test line, PUT back, verify

2. **`file-splitter`** — Document decomposition skill
   - Input: master document path + splitting rules (heading level and/or heading text patterns)
   - Output: N files at specified output paths
   - Features: preserves heading hierarchy within each output file; optionally adds front matter (file name, source, date) to each; logs split manifest
   - Test: split a 100-line test document at H2 boundaries

3. **`evidence-marker`** — ●/○ evidence classification and audit skill
   - Mode CLASSIFY: takes a specification text block; classifies each prescriptive sentence as ● (evidence-based, citation present or Tier identified) or ○ (inferred/expert consensus, no direct evidence); outputs marked text
   - Mode AUDIT: scans a file for all specification sentences; flags any without ● or ○ marker; produces coverage report
   - Rules: Tier 1–6 citations → ●; "EXPERT CONSENSUS" → ○; "inferred from" / "clinically reasoned" → ○; PLACEHOLDER → ○; no citation and no disclosure → FLAG
   - Test: run on 3 sample items from Cat-A

**Update:**

4. **`framing-checker`** — Add two new check rules:
   - CHECK-BAR-VOL1: flag any "BAR" mention in files identified as Volume I (Parts 1–3)
   - CHECK-EVIDENCE-MARKERS: flag specification sentences without ●/○ markers

5. **`evidence-auditor`** — Add ●/○ verification mode:
   - New mode: MARKER-AUDIT — delegates to `evidence-marker` AUDIT mode; aggregates results across multiple files

6. **`item-specification-writer`** — Add to output template:
   - Every specification line must carry ● or ○ prefix
   - Every item must include `**[Illustration: to be provided]**` after Cross-reference line
   - K-category template awareness

### Session 0-B: Structural and Assembly Skills (est. 1 session)

**Build:**

7. **`bulk-renumber`** — Section reference renumbering skill
   - Input: renumbering map (YAML: `{old: "§11.4", new: "§10.4"}` etc.) + target file(s)
   - Process: for each map entry, find all occurrences of old reference in context-aware mode (skip URLs, citation strings, code blocks); replace with new; log each replacement
   - Safety: dry-run mode (report what would change without changing); confirmation mode (present changes, require user approval before write)
   - Context-aware patterns: `§X.Y`, `Part X`, `§X.Y.Z`, `Part X §X.Y`
   - Test: apply to a 50-line test file with known references

**Update:**

8. **`cross-reference-resolver`** — Update for v10.0:
   - Add K-category item codes (K-01 through K-04) to valid item registry
   - Add per-Part file architecture awareness (references can cross file boundaries)
   - Update expected §-numbering patterns per v10.0 renumbering map
   - Remove expectation of §6.x in Part 5, §7.x in Part 6, §9.x in Part 10
   - Add: §5.x for Part 5, §6.x for Part 6, §8.x for Part 8 (Engineering), §9.x for Part 9 (Consultants)

9. **`structure-auditor`** — Update expected heading patterns:
   - Part 5 sections: §5.0–§5.10
   - Part 6 sections: §6.1–§6.7
   - Part 8 (Engineering): §8.x
   - Part 9 (Consultants): §9.x
   - Part 10 (DAR): §10.x
   - Part 11 (Economics): §11.x
   - Part 12 (Case Studies): §12.x

10. **`chunk-assembler`** — Add file manifest system:
    - Input: manifest file listing all Part/Category files in assembly order
    - Process: concatenate in order; verify no duplicate headings; verify heading hierarchy continuity across file boundaries
    - Manifest location: `parts/v10/assembly-manifest.md`

11. **`workplan-orchestrator`** — Update:
    - Part numbering map in workflow sequences
    - Skill registry: add new skills (github-io, file-splitter, evidence-marker, bulk-renumber, sensory-coherence-checker); remove retired skills; update triggers
    - Workflow table: add new workflows (Per-Part Edit, Evidence Marker Pass, Bulk Renumber)

12. **`session-consolidator`** — Update:
    - YAML template Part references to v10.0 numbering
    - Reconciliation check list: add per-Part file verification
    - Add commit log reconciliation (verify all intended GitHub writes completed)

13. **`vol2-item-formatter`** — Update:
    - Add ●/○ marker awareness
    - Add illustration note insertion

### Session 0-C: Research and Content Skills (can overlap with Phase 1 start)

**Build:**

14. **`citation-miner`** — Backward + forward citation mining
    - Input: confirmed source (DOI or title + year)
    - Backward: extract reference list; classify each by tier; flag any that are new to BPC
    - Forward: Google Scholar "cited by" search; retrieve citing sources; classify by tier
    - Output: `citation_mining` block for research-log-manager LOG
    - Saves inline mining work in every Phase 1 research session

15. **`sensory-coherence-checker`** — Room-level sensory conflict audit
    - Input: room matrix (list of items with population applicability) OR single room specification
    - Process: for each item pair, check for sensory conflicts using conflict knowledge base (acoustic vs. tactile; lighting for VIS vs. NDV; temperature for NEU vs. PAIN; etc.)
    - Output: conflict matrix per room; each conflict linked to §4.9 resolution if one exists; unresolved conflicts flagged for gap register
    - Also produces: practitioner-facing sensory coherence checklist (can be included in guidebook §4.3 as an operational tool — resolves GAP-CR-16)

**Update:**

16. **`citation-verifier`** — Add HARVEST mode:
    - Scan all Part files
    - Extract every citation string (author-year, standard reference, DOI)
    - Deduplicate
    - Output: assembled bibliography draft for `bibliography.md`
    - This resolves the empty Master Bibliography problem (GAP-CR-01) during Phase 3

---

## 6. Commit Guarantee Protocol

With `github-io` built, every session follows this commit protocol:

1. **Start of session:** `github-io GET` all files that will be modified (load SHAs)
2. **During session:** all writes go through `github-io PUT` with retry
3. **End of session:** `github-io` produces a commit log:
   ```
   COMMITS [YYYY-MM-DD HH:MM]:
   ✓ parts/v10/part01-foundations.md — updated — sha: abc123
   ✓ gap_register.md — appended GAP-CR-21 — sha: def456
   ✗ references/search-log.md — FAILED (409 conflict) — MANUAL PASTE REQUIRED
   ```
4. **Session-consolidator** includes the commit log in the session YAML
5. **Next session:** workplan-orchestrator checks previous session's commit log for any ✗ entries and resolves before proceeding

This guarantees:
- Every commit is logged
- No silent failures
- Failed commits are surfaced and resolved in the next session
- The 30-file v10.0 architecture doesn't multiply commit failures silently

---

## 7. Updated Session Estimate

| Phase | Sessions | Content |
|---|---|---|
| **Phase 0** | 2–3 | Build 4 new skills; update 9 existing skills |
| **Phase 1** | 5 | Research (PAIN, OFS, IntD, NEU, NDV/MH, residential, CRPD, Co-2, item consolidation) |
| **Phase 2** | 3 | File decomposition, renumbering, structural moves, phantom refs |
| **Phase 3** | 12 | Content editing (14 work units across all Parts + Categories) |
| **Phase 4** | 3 | QA + assembly |
| **Total** | **25** | (+2 from original 23, but with higher reliability and lower rework) |

The 2 extra sessions in Phase 0 are recovered by:
- ~1 session saved from `bulk-renumber` preventing manual renumbering errors
- ~0.5 sessions saved from `evidence-marker` preventing marker audit rework
- ~0.5 sessions saved from `github-io` eliminating inline commit scripts and preventing silent failures
- Reduced debugging in Phase 4 QA (fewer issues to find because skills caught them during Phase 3)

---

## 8. Decision Required

Before Phase 0 begins, author should confirm:

| Decision | Options | Recommendation |
|---|---|---|
| `github-io` scope | Minimal (GET/PUT only) vs. full (GET/PUT/DELETE/list/commit-log) | Full — the marginal build cost is low and DELETE will be needed for deprecated files |
| `sensory-coherence-checker` timing | Build in Phase 0 (Session 0-C) vs. defer to Phase 3 | Phase 0 — it produces a practitioner tool that becomes guidebook content in §4.3, and it improves Phase 3 matrix editing quality |
| `citation-miner` timing | Build in Phase 0 vs. defer | Phase 0 Session 0-C — improves every Phase 1 research session |
| Skill storage | Continue `/mnt/project/` (read-only) + GitHub `skills/` (reference) vs. migrate canonical to GitHub `skills/` and read from there | Keep current — `/mnt/project/` is the runtime location; GitHub `skills/` is human reference. But new skills built in Phase 0 must be added to `/mnt/project/` by the author after each build session. |

---

*End of Ecosystem Audit*
