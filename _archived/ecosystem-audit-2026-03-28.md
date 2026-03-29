# Ecosystem Audit — Exhaustive Analysis
**Date:** 2026-03-28
**Scope:** PI, 41 active skills, GitHub repo structure, workflows, pipelines, token efficiency, accuracy, process integrity
**Basis:** Full read of all GitHub skill files, repo tree, project-standards.md, session history, Anthropic Agent Skills documentation

---

## 1. Architecture Assessment

### 1.1 Execution Model: Fundamental Contradiction Chain

The project-standards.md contains a **chain of contradictory rules** about where skills are sourced, each superseding the last:

| Date | Rule | Source |
|---|---|---|
| 2026-03-18 18:30 | GitHub takes precedence over /mnt/project/ | Rule ~37 |
| 2026-03-18 22:15 | GitHub is inventory only; /mnt/project/ is canonical | Rule ~48 |
| 2026-03-18 22:25 | SUPERSEDED: confirms Rule 48 overrides Rule 37 | Rule ~49 |
| 2026-03-26 19:15 | Skills NOT in /mnt/project/ must GET from GitHub | Rule ~90 |
| 2026-03-27 17:30 | ALL skills GitHub-only; Rules 37/48/49/90 superseded | Rule ~103 |

**Current PI says:** "All skills live on GitHub at `skills/{skill-name}_SKILL.md`. GET before execution. No `/mnt/project/` reads for skills."

**Problem:** The old rules are still in project-standards.md. They are marked SUPERSEDED but not deleted. Any session that loads project-standards.md encounters all five contradictory rules in sequence. The model must parse the supersession chain correctly every time. This is fragile. One misparse and the session reads skills from the wrong source.

**Fix:** Delete all superseded rules from project-standards.md. Keep only the canonical rule. Append: "All prior rules about skill file locations are void."

### 1.2 Skill Source: GitHub GET Cost

The current architecture requires a GitHub GET for every skill used in a session. Session start alone requires 3 GETs (workplan-orchestrator, session-consolidator, github-io). A typical research session adds 3-5 more (multilingual-research, research-log-manager, citation-miner, etc.).

**Token cost per GET:** Each GitHub API call returns base64 content + JSON envelope. The `urllib` + `base64.b64decode` pattern costs ~20-30 tokens of boilerplate per call, plus the full skill content. A 200-line skill is ~4,000 tokens. Session start: ~12,000 tokens just for skill loading.

**Comparison with /mnt/project/ alternative:** /mnt/project/ files load into context automatically at session start (zero explicit GET cost) but consume context window permanently. GitHub GET loads on-demand (progressive disclosure) but requires boilerplate each time.

**Assessment:** The GitHub GET model is correct for this project. Skills should only load when needed. But the boilerplate overhead can be reduced — see §5.

### 1.3 Model Tier Architecture: Dead Code

The PI still references a three-tier model routing architecture (Haiku/Sonnet/Opus) that cannot be implemented:

- **Haiku:** 14 skills list "Model: Haiku 4.5" — but Haiku cannot be invoked from a Sonnet conversation. Every "Haiku" task runs as Sonnet.
- **Opus:** 5 skills reference Opus (connection-scout, cross-population-conflict-mapper, multilingual-research synthesis, evidence-auditor judgment, content-gap-analyzer judgment) — but Opus requires a separate conversation session. The artifact proxy routes all model strings to Sonnet 4.5-20250929.
- **Sonnet:** All tasks actually execute as Sonnet 4.6 (conversation model) regardless of stated model assignment.

**Impact:** Every session that loads a "Haiku" skill and follows its model assignment instructions wastes zero tokens — the instruction is simply ignored. But it creates confusion about what quality level to expect. Skills marked "Haiku — no judgment" may actually be performing judgment-level work (as Sonnet) without the skill author's quality expectations being calibrated correctly.

**The real cost:** The fiction that Haiku tasks exist means skill authors write instructions like "structural extraction only — no content judgment" which constrains Sonnet unnecessarily. Sonnet can and should exercise judgment on structural tasks where appropriate.

---

## 2. Skill-by-Skill Analysis

### 2.1 Structural Issues

**Missing YAML frontmatter (5 skills):**
- `bibliography-compiler_SKILL.md` — NO YAML
- `connection-scout_SKILL.md` — NO YAML
- `item-specification-writer_SKILL.md` — NO YAML
- `multilingual-research_SKILL.md` — NO YAML (also has escaped markdown throughout — `\\*\\*`, `\\---`, `&#x20;` artifacts)
- `research-log-manager_SKILL.md` — NO YAML

These 5 skills would fail validation against the Agent Skills standard. The missing YAML is inconsistent with the other 36 skills that do have it.

**Escaped markdown corruption (1 skill):**
`multilingual-research_SKILL.md` contains pervasive escaped markdown artifacts: `\\*\\*` instead of `**`, `\\---` instead of `---`, `&#x20;` whitespace entities. This suggests it was written or edited through a system that escaped markdown. The skill is 550 lines (over the 500-line recommended limit) and the escaped characters inflate it further. The content is readable by a human but the escaping adds ~200 tokens of noise.

**Line counts vs. 500-line guidance:**
Only `multilingual-research_SKILL.md` (550 lines) exceeds 500. The next largest are `toc-editor` (269), `functional-deficit-researcher` (254), `bibliography-compiler` (252), and `item-specification-writer` (231). All are within range.

### 2.2 Stale Model References

| Skill | Claims | Reality |
|---|---|---|
| connection-scout | "Model: Opus 4" | Runs as Sonnet 4.6 |
| cross-population-conflict-mapper | "Opus 4.6 (resolution synthesis)" | Runs as Sonnet 4.6 |
| haiku-chunker | "Model: Haiku 4.5" | Runs as Sonnet 4.6 |
| fix-linebreaks | "Model: Haiku 4.5" | Runs as Sonnet 4.6 |
| structure-auditor | "Model: Haiku 4.5" | Runs as Sonnet 4.6 |
| markdown-formatter | "Model: Haiku 4.5" | Runs as Sonnet 4.6 |
| github-filing | "Model: Haiku" | Runs as Sonnet 4.6 |
| bulk-renumber | "Haiku 4.5 for pattern extraction" | Runs as Sonnet 4.6 |
| file-splitter | "Haiku 4.5 for splitting" | Runs as Sonnet 4.6 |
| table-formatter | "Haiku 4.5 (detection)" | Runs as Sonnet 4.6 |
| evidence-marker | "Sonnet 4.6" then "Haiku tag" in workflow | Inconsistent |

**14 of 41 skills claim Haiku execution. 5 claim or reference Opus. None execute as stated.**

### 2.3 Deprecated/Retired Skill References

- `workplan-orchestrator` Skill Registry lists `neufert-image-analyzer` — deprecated and in `skills/deprecated/`
- `workplan-orchestrator` Workflow table references `vol2-item-formatter` placement inconsistently (before vs. after `prose-style-checker` depending on which table)
- `keyword-lookup` is marked DEPRECATED in project-standards.md (Rule ~92) but still referenced in the multilingual-research skill's pre-run steps ("view the Keyword Compendium")
- `connection-scout` references "Opus 4" (not "Opus 4.6") — stale model name

### 2.4 PI ↔ Skill Divergence

The PI and skill files contain duplicate but divergent definitions. Key conflicts:

**Workflow sequences:**
| Source | Item Specification Workflow |
|---|---|
| PI (current) | `item-consolidation-analyzer → research-log-manager RETRIEVE → Opus best-practice synthesis → item-specification-writer → vol2-item-formatter → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator` |
| workplan-orchestrator (GitHub) | `item-consolidation-analyzer → item-specification-writer → [framing-checker · evidence-auditor] → evidence-marker → prose-style-checker → vol2-item-formatter → volii-validator` |
| workplan-orchestrator (project-knowledge) | `item-consolidation-analyzer → item-specification-writer → [framing-checker · evidence-auditor] → prose-style-checker → volii-validator → vol2-item-formatter` |

Three different orderings in three different locations. Which is canonical? The PI says "PI definition governs." But the workplan-orchestrator on GitHub was updated more recently. And the endnote-downstream-amendments document specifies yet another ordering with `bibliography-compiler` inserted.

**Document Assembly:**
| Source | Assembly Workflow |
|---|---|
| PI | `chunk-assembler → bibliography-compiler → bibliography-reconciliation → cross-reference-resolver → guidebook-auditor A` |
| workplan-orchestrator | `chunk-assembler (manifest mode) → cross-reference-resolver → guidebook-auditor A` |

The workplan-orchestrator on GitHub does not include `bibliography-compiler` in its Document Assembly workflow, despite this being added to the PI. The endnote amendments document specifies the correct pipeline but was never integrated into the workplan-orchestrator.

**Skill Registry duplications:**
The PI Skill Registry and the workplan-orchestrator Skill Registry are maintained independently. They have diverged:
- PI lists `bibliography-compiler` (Haiku) and `vol2-item-formatter` (Sonnet) — added per FIX-05
- workplan-orchestrator lists `vol2-item-formatter` (Haiku/Sonnet) but places it under "Writing and Specification"
- PI lists `citation-miner` — workplan-orchestrator does not include it in any Skill Registry table
- workplan-orchestrator lists `evidence-marker` — PI Skill Registry does not include it
- workplan-orchestrator lists skills with model assignments that don't match PI model assignments (e.g., `chunk-assembler` as "Haiku/Sonnet" vs. PI silent on model)

---

## 3. Pipeline Integrity

### 3.1 Endnote Pipeline — NOT INTEGRATED

The endnote-downstream-amendments document (2026-03-27) specifies amendments to 5 skills and the PI. Status:

| Amendment | Applied? |
|---|---|
| item-specification-writer: REF-ID markers + sources-cited | **Partially** — the GitHub skill file has the protocol, but the PI section was added separately |
| vol2-item-formatter: REF-ID validation | **Yes** — GitHub skill file includes REF-ID validation |
| chunk-assembler: pipeline note update | **NO** — GitHub skill file does not mention bibliography-compiler |
| cross-reference-resolver: endnote superscript pattern | **NO** — GitHub skill file does not include endnote superscript pattern |
| PI: Skill Registry addition | **YES** — PI includes bibliography-compiler |
| PI: Workflow Reference update | **NO** — workplan-orchestrator workflows not updated |

**Assessment:** The endnote pipeline is half-integrated. Two of four downstream skills have not been amended. If the pipeline is run as-is, `chunk-assembler` will flag REF-ID markers as broken refs, and `cross-reference-resolver` will not validate endnote superscripts. This blocks Phase 3.

### 3.2 Research Pipeline — Functional but Expensive

The research pipeline (CHECK → multilingual-research → LOG) works but has structural inefficiency:

**Token cost per slug research run:**
1. `research-log-manager CHECK`: GET slug-registry (18K file) + GET search-log file → ~5,000 tokens input
2. `multilingual-research`: 14 languages × web searches + 24 jurisdictions → varies widely; typically 15,000-40,000 tokens in web search results alone
3. `research-log-manager LOG`: GET + PUT search-log + GET + PUT BPC → ~3,000 tokens overhead

Total overhead (excluding actual research content): ~8,000 tokens per slug just for pipeline management.

**The slug-registry.md is 18,575 bytes** — loaded in full on every CHECK. It could be restructured to reduce per-lookup cost (e.g., alphabetical index with byte ranges for direct lookup), but this is a marginal optimization.

### 3.3 Session Pipeline — Functional with Known Gaps

Session start protocol requires 5 sequential GETs: LATEST → latest session file → gap_register.md → project-standards.md → (optionally) directory listings for stale file detection.

**project-standards.md is 74,026 bytes (790 lines, ~143 rules).** This is loaded in full every session. At ~18,000 tokens, it consumes a significant portion of the context window. Many rules are superseded, stale, or one-time decisions that have no ongoing relevance.

**gap_register.md is 72,540 bytes.** Also loaded in full. Most entries are CLOSED. Only OPEN items are relevant at session start. A filtered load (grep for OPEN) would save ~90% of tokens.

### 3.4 Connection Register — Oversized

**connection-register.md is 149,926 bytes (~37,000 tokens).** This file cannot be loaded into context in a single GET without consuming a massive portion of the window. The `connection-scout` skill that writes to it and the `session-consolidator` that reconciles it both need to GET this file. Neither can reasonably process it in full.

---

## 4. Data Architecture Issues

### 4.1 Append-Only Files Without Compaction

Three critical state files are append-only and growing without bound:

| File | Size | Growth Pattern |
|---|---|---|
| `gap_register.md` | 72.5 KB | Every session adds gaps; CLOSED items never removed |
| `references/project-standards.md` | 74.0 KB | Every session may add rules; superseded rules never removed |
| `references/connection-register.md` | 149.9 KB | Connection-scout adds; status changes append text |

**Projection:** At current growth rate (~5 KB/session for gap register, ~2 KB/session for project-standards), these files will exceed 100 KB within 15-20 sessions. Loading any of them will consume >25,000 tokens per GET.

**Fix required:** Implement compaction. CLOSED gap items → archived file. Superseded rules → deleted or archived. Connection register → split into PENDING (active) and CONSUMED/CLOSED (archived).

### 4.2 Session Files — 84 and Growing

The `sessions/` directory contains 84 session files. The LATEST pointer (session_084.md) eliminates the need to list and sort the directory. But `session-consolidator` still needs to GET the prior session to validate blocker carry-forward. If session files continue to accumulate, directory listings will grow.

The sequential numbering (session_NNN.md) is correct. No action needed on naming convention.

### 4.3 Deprecated Workplan Files

`workplan/deprecated/` contains 14 files totaling ~280 KB. These are correctly filed. But `workplan/` also contains:
- `v10-4-integrated.md` (37.9 KB) — should be in deprecated/ (superseded by v10-5)
- `P1-D2-D3-co0004-remapping.md` (8.9 KB) — active reference
- `co0003-amendment-2026-03-28.md` (4.2 KB) — active reference
- `slug-triage-2026-03-28.md` (8.7 KB) — active reference
- `v10-5_2026-03-29.md` (25.2 KB) — current workplan

`v10-4-integrated.md` should be filed to deprecated/.

### 4.4 Flat BPC/SL Files — Frozen but Still Referenced

The PI says flat files (`references/bpc/{POPULATION}.md` and `references/search-log/{POPULATION}.md`) are "Retired (frozen)." But they still exist on GitHub as active files (14 population-level BPC files, 14 population-level SL files). They total ~430 KB combined.

New research uses per-slug directory entries (`references/bpc/{topic}/{slug}.md`). But the flat files are not marked as frozen within the files themselves. A new session that doesn't load the PI carefully might write to them.

---

## 5. Token Efficiency Analysis

### 5.1 Per-Session Overhead Budget

| Component | Est. Tokens | Notes |
|---|---|---|
| PI (system prompt) | ~5,500 | Current PI embedded in system prompt |
| project-standards.md GET | ~18,000 | 790 lines, 143 rules |
| gap_register.md GET | ~18,000 | Growing |
| Latest session GET | ~1,200 | Typical session file |
| workplan-orchestrator GET | ~2,800 | 201 lines |
| session-consolidator GET | ~4,500 | 178 lines |
| github-io GET | ~1,800 | 195 lines |
| **Total session start** | **~51,800** | Before any work begins |

With a 200K-token context window, session start consumes ~26% of available context. After adding a research skill (multilingual-research: ~13,000 tokens), the overhead rises to ~32%.

### 5.2 Reducible Overhead

| Optimization | Token Savings | Effort |
|---|---|---|
| Compact project-standards.md (remove superseded, deduplicate) | ~8,000 | Medium — requires careful rule-by-rule audit |
| Filter gap_register.md (OPEN only at session start) | ~15,000 | Low — change session-start protocol to grep OPEN |
| Remove stale PI sections (per FIX-04) | ~800 | Low — PI edit |
| Inline github-io patterns (don't GET — memorize the 3 functions) | ~1,800 | Low — but fragile if patterns change |
| Remove model assignment lines from skills (they're all Sonnet) | ~100 | Trivial but low impact |
| **Total recoverable** | **~25,700** | |

**Net session start after optimization:** ~26,100 tokens (~13% of context). This is a realistic and achievable target.

### 5.3 Per-Skill GET Overhead

Each skill GET via GitHub API costs:
- ~30 tokens: urllib/base64 boilerplate
- Full skill content: varies (30-550 lines)
- JSON envelope parsing: ~20 tokens

The `github-io` skill itself could be simplified: the current 195 lines include 4 function definitions (GET, PUT, APPEND, LIST), bash shorthand, collision prevention rules, and error reporting. Most sessions use only GET and WRITE. The APPEND function is rarely used standalone (session-consolidator and workplan-orchestrator have their own append logic).

---

## 6. Process Integrity Issues

### 6.1 Reconciliation Failures

Session 084's reconciliation shows `checked: false` for gap_register, project_standards, search_log, bpc, and connection_register. Only sessions is `checked: true`. This means the session closed without verifying state file integrity.

Looking at recent sessions, reconciliation is frequently incomplete. The `session-consolidator` specifies a comprehensive reconciliation protocol (7 state files checked), but in practice sessions often close without completing it — likely due to context exhaustion.

**Root cause:** The reconciliation protocol is too expensive. Checking 7 state files requires 7 GETs (each potentially 18K+ tokens). By session close (~85% context), there isn't enough room.

**Fix:** Reconciliation should be lightweight. Instead of full file GETs, maintain a session-local change log (skills run, gaps added/resolved, rules added) and validate only against that log. Full reconciliation becomes a separate, dedicated session activity run periodically.

### 6.2 Blocker Propagation

Session 084 carries 5 blockers. Several are repeated from prior sessions:
- "Endnote pipeline dry run NOT DONE" — present since at least session_2026-03-28
- "Body ↔ bibliography cross-reference audit NOT DONE" — same
- "PI changes FIX-03/04/05 still require manual system prompt edit" — from ecosystem update plan

Blockers are carried forward manually. The FIX-09 (YAML pre-commit blocker validation) is specified in the ecosystem update plan but not yet implemented in `session-consolidator`. Stale blockers accumulate.

### 6.3 Workplan Drift

The workplan has gone through 6 major versions (v10.0 through v10.5) plus 4 Change Orders. Each workplan references the prior as "superseded." But the workplan also contains the canonical workflow sequences that the PI and workplan-orchestrator reference. When the workplan changes, the PI and workplan-orchestrator are not updated in sync.

This creates three sources of truth for workflow sequences: PI, workplan-orchestrator skill, and current workplan. They have already diverged (see §2.4).

---

## 7. Accuracy and Correctness Issues

### 7.1 Evidence Tier Discrepancy

The PI defines a 6-tier + 2 co-primary evidence hierarchy. But within the PI itself, the tiers have shifted:

- PI §Evidence Hierarchy: Tier 1, Co-1, 2, Co-2, 3, 4, 5, 6
- project-standards.md Rule ~51: "Tier 5 = jurisdiction-specific regulatory documents and grey literature" — this contradicts the PI where Tier 5 = "National beyond-code frameworks" and Tier 6 = "Statutory codes"
- multilingual-research_SKILL.md: Correctly lists the 6-tier hierarchy matching the PI

Rule ~51 in project-standards.md is from 2026-03-18 22:35 and appears to be an early version of the hierarchy that was later refined. It has not been superseded. It conflicts with the canonical hierarchy.

### 7.2 Population Code "VIS/DEAF" in Skills

project-standards.md Rule ~53 states "VIS/DEAF is not a valid population code." But the `item-specification-writer` skill file contains `VIS/DEAF` in its "Canonical codes" list: "VIS/vis · **VIS/DEAF**". This is the exact error the rule was written to prevent.

### 7.3 CO-0004 Numbering Not Propagated

CO-0004 (2026-03-29) changed 13 Parts → 12 Parts and 3 Volumes → 2 Volumes. The `workplan-orchestrator` has been updated with the new Part numbering map. But:
- The PI still references the old structure in several places (Workflow Reference table, Skill Registry)
- Multiple skills reference "Part 7" (old item library), "Part 8" (old engineering), "Part VIII", "Vol 2"
- The guidebook source files in `parts/88_to_90/` use the old numbering (part00 through part14)

This is expected — CO-0004 is DRAFT awaiting author sign-off. But when it's approved, propagating the numbering change through 41 skill files and the PI will be a significant effort.

---

## 8. Agent Skills Standard Compliance

### 8.1 Native Agent Skills Assessment

Against the Anthropic Agent Skills standard (open standard, Dec 2025):

| Requirement | Project Status |
|---|---|
| YAML frontmatter (`name` + `description`) | 36/41 have it; 5 missing |
| `name`: max 64 chars, lowercase/hyphens | All conformant names are valid |
| `description`: max 1024 chars | Most descriptions exceed 1024 chars (typical: 400-600 chars in YAML, but some run to 800+) — needs measurement |
| SKILL.md under 500 lines | 40/41 conform; `multilingual-research` at 550 |
| Progressive disclosure (multi-file) | Not used — all skills are single monolithic SKILL.md files |
| Code execution integration | Not applicable — these are text-instruction skills, not code-execution skills |
| No cross-surface sync | Acknowledged in ecosystem update plan |

### 8.2 Suitability for Native Upload

The project's skills are **text-instruction-only**. They don't execute code in a container. They are injected into the conversation context as instructions. This is fundamentally different from native Agent Skills which "leverage Claude's VM environment."

The project's GET-from-GitHub pattern is functionally equivalent to progressive disclosure: skills are loaded only when needed, and only the needed skill is loaded. This is correct behavior.

**Recommendation:** Do not attempt native Agent Skills upload. The current architecture (GitHub GET on demand) is appropriate for this use case. Native upload would require:
- Refactoring all skills to fit the code-execution paradigm
- Splitting large skills into multi-file directories
- Losing the GitHub version control and collaboration model
- Managing two copies (claude.ai Settings + GitHub)

None of these provide value for this project.

---

## 9. Structural Recommendations

### 9.1 Critical (Blocks Phase 3)

1. **Complete endnote pipeline integration:** Amend `chunk-assembler` and `cross-reference-resolver` per endnote-downstream-amendments. Without this, the bibliography compilation pipeline will break.

2. **Run endnote pipeline dry run:** The PI lists this as an unresolved blocker. One item end-to-end through the full pipeline (item-specification-writer → vol2-item-formatter → chunk-assembler → bibliography-compiler → cross-reference-resolver) must pass before any batch item specification work begins.

3. **Resolve workflow sequence conflicts:** Establish ONE canonical Item Specification workflow. Update PI, workplan-orchestrator, and workplan to match. Delete conflicting versions.

### 9.2 High Priority (Before Next Research Session)

4. **Compact project-standards.md:** Remove superseded rules, deduplicate, delete one-time decisions that have no ongoing relevance. Target: <200 lines (~5,000 tokens).

5. **Filter gap_register.md at session start:** Change protocol to extract OPEN items only via grep/python, not load entire file. Target: <2,000 tokens at session start.

6. **Fix multilingual-research escaped markdown:** Re-commit with clean markdown. Also add YAML frontmatter.

7. **Add YAML frontmatter to 5 missing skills:** bibliography-compiler, connection-scout, item-specification-writer, multilingual-research, research-log-manager.

8. **Fix VIS/DEAF in item-specification-writer:** Remove from canonical codes list.

### 9.3 Medium Priority (Before Phase 3)

9. **Update all model assignments:** Replace "Model: Haiku 4.5" with "Model: Sonnet 4.6" (or remove model lines entirely). Remove behavioral constraints predicated on Haiku limitations ("no content judgment", "structural extraction only") where Sonnet judgment would improve quality.

10. **Split connection-register.md:** PENDING entries → active file. CONSUMED/CLOSED → archived file. Current 150 KB is unmanageable.

11. **Implement lightweight reconciliation:** Replace 7-file GET reconciliation with session-local change tracking.

12. **File v10-4 workplan to deprecated/.**

13. **Archive comprehensive-audit-2026-03-27.md** from Project Files (per FIX-02 in ecosystem update plan — user action required).

14. **Delete opus-passthrough.html** from Project Files (per FIX-01 — user action required).

### 9.4 Low Priority (Ongoing Maintenance)

15. **Establish single-source-of-truth for workflows:** Either the PI or the workplan-orchestrator defines workflows — not both. Recommended: workplan-orchestrator is canonical for workflow sequences; PI references it rather than duplicating.

16. **Periodic project-standards.md pruning:** After each major phase, review all rules. Delete those that have been absorbed into skill files or the PI.

17. **Flat BPC/SL files:** Add `<!-- FROZEN — new entries go to per-slug directory files -->` header to each frozen population-level file to prevent accidental writes.

---

## 10. Token Budget Summary

| Scenario | Current | After §9 Fixes |
|---|---|---|
| Session start (before work) | ~51,800 tokens | ~26,100 tokens |
| Session start + 1 research skill | ~64,800 tokens | ~39,100 tokens |
| Available for actual work (200K window) | ~135,200 tokens | ~160,900 tokens |
| **Efficiency gain** | — | **+19% usable context** |

---

## 11. Risk Register

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| Endnote pipeline breaks at chunk-assembler | HIGH | CERTAIN if unamended | Complete FIX-06 |
| Workflow sequence conflict causes incorrect skill ordering | MEDIUM | LIKELY | Single-source workflows |
| project-standards.md exceeds loadable size | MEDIUM | LIKELY (15-20 sessions) | Compaction protocol |
| connection-register.md unloadable | HIGH | CURRENT | Split file |
| CO-0004 numbering propagation creates mass of broken refs | MEDIUM | CERTAIN when approved | Pre-compute find-and-replace spec |
| Session reconciliation consistently incomplete | LOW | CURRENT | Lightweight protocol |
| Contradictory rules cause skill source confusion | LOW | POSSIBLE | Delete superseded rules |

---

*End of audit*
