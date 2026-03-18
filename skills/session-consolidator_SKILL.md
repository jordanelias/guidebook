---
name: session-consolidator
description: >
  End-of-session memory consolidation for the Accessible Built Environments Guidebook project.
  Reviews session events, extracts recurring patterns, reconciles state files against work
  performed, writes YAML session-close block to GitHub sessions/ directory, and appends
  learned rules to references/project-standards.md. ALWAYS use this skill at session end.
  Trigger on: "end of session", "wrap up", "consolidate findings", "update project
  knowledge", "write session close", "save progress", or when workplan-orchestrator
  session-end protocol runs.
---

**Model:** Sonnet 4.6
**GitHub backend:**  ·  · Protocol → Project Instructions §GitHub API
**All timestamps: **

## Steps

1. **Review session:** skills run · GAP-XXX items added/resolved · escalations · blockers · skill anomalies · research-log-manager LOG calls completed or missed.

2. **Extract patterns:** failing sources · recurring framing flags · skill failure modes · cross-section evidence gaps · languages consistently NO-DATA/THIN.

3. **Write rules to GitHub:** for each specific, actionable, recurring pattern:
   - GET  + SHA.
   - Append: 
   - PUT back. Commit: 

4. **Reconcile state files against session work** (run after Step 3 — full picture first):

   For each state file, GET current content from GitHub and verify:

   **gap_register.md**
   - Every gap described as raised this session → entry exists with correct ID, status OPEN, and today's timestamp.
   - Every gap described as resolved this session → status field updated (CLOSED / CLOSED-DELETED / CLOSED-NOTED / RESOLVED).
   - Every gap described as a known limitation → status KNOWN-LIMITATION and rationale present.
   - Discrepancy → attempt inline fix (append corrected entry or update status); if fix fails → BLOCKER.

   **references/project-standards.md**
   - Every rule described as added this session → RULE block present with matching DATE.
   - Discrepancy → append missing rule inline; if fix fails → BLOCKER.

   **references/search-log.md**
   - Every  run described this session → slug entry present,  matches session date, all 9 core language statuses recorded.
   - Discrepancy → flag as BLOCKER (cannot reconstruct search results post-hoc).

   **references/best-practices-compendium.md**
   - Every slug confirmed in search-log → BPC entry  present.
   - Discrepancy → flag as BLOCKER.

   **sessions/ directory**
   - No prior session's  is being skipped without explanation in the current session YAML.
   - No duplicate filename for the current session timestamp.

   **Reconciliation output (compact table — include in session YAML under ):**
   

5. **Research log hygiene:** if  ran and LOG was not called → flag as BLOCKER.

6. **Write session close to GitHub:**
   - Determine filename:  (use session-close timestamp, not wall-clock if session started earlier).
   - Check for collision: GET filename. If 404: proceed. If exists: append  suffix.
   - This is always a NEW file — never append to an existing session file.
   - PUT (no SHA required for new files). Commit: 

   **YAML schema:**
   

7. **Report to user (≤6 lines):** accomplishments · gaps added/resolved · rules added · reconciliation result (pass / N fixes / N blockers) · next action · GitHub write status (✓ / ⚠ fallback).

**Fallback:** if PUT fails after one retry — output YAML block and rules text as fenced code blocks. Instruct user to paste manually. Never silently drop state.
