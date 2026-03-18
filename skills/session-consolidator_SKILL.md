---
name: session-consolidator
description: >
  End-of-session memory consolidation for the Accessible Built Environments Guidebook project.
  Reviews session events, extracts recurring patterns, writes YAML session-close block to GitHub
  sessions/ directory, and appends learned rules to references/project-standards.md. ALWAYS use
  this skill at session end. Trigger on: "end of session", "wrap up", "consolidate findings",
  "update project knowledge", "write session close", "save progress", or when workplan-orchestrator
  session-end protocol runs.
---

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**All timestamps: `YYYY-MM-DD HH:MM`**

## Steps

1. **Review session:** skills run · GAP-XXX items added/resolved · escalations · blockers · skill anomalies · research-log-manager LOG calls completed or missed.

2. **Extract patterns:** failing sources · recurring framing flags · skill failure modes · cross-section evidence gaps · languages consistently NO-DATA/THIN.

3. **Write rules to GitHub:** for each specific, actionable, recurring pattern:
   - GET `references/project-standards.md` + SHA.
   - Append: `RULE: {description}  CONDITION: {when}  ACTION: {what}  DATE: YYYY-MM-DD HH:MM`
   - PUT back. Commit: `session-consolidator: append rule [{YYYY-MM-DD HH:MM}]`

4. **Research log hygiene:** if `multilingual-research` ran and LOG was not called → flag as BLOCKER in YAML.

5. **Write session close to GitHub:**
   - Determine filename: `sessions/session_{YYYY-MM-DD-HHMM}.md` (use current session datetime, not now-time if session started earlier).
   - This is always a NEW file — never append to an existing session file.
   - Create the file via PUT (no SHA required for new files):

   ```yaml
   ---
   session_close: YYYY-MM-DD HH:MM
   document: "[DOC-ID]"
   skills_run: []
   gaps_added: []
   gaps_resolved: []
   escalations_triggered: 0
   escalation_detail: []
   patterns_noted: []
   rules_added: []
   blockers: []
   research_log_updated: true|false
   next_action:
     skill: name
     session: description
     parameters: {}
   ```

   - Commit: `session-consolidator: append session close [{YYYY-MM-DD HH:MM}]`

6. **Report to user (≤5 lines):** accomplishments · gaps added/resolved · next action · rules added · GitHub write status (✓ / ⚠ fallback).

**Fallback:** if PUT fails after one retry — output YAML block and rules text as fenced code blocks. Instruct user to paste manually. Never silently drop state.
