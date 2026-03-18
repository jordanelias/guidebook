---
name: session-consolidator
description: >
  End-of-session memory consolidation for the Accessible Built Environments Guidebook project.
  Reviews session events, extracts recurring patterns, writes YAML resumption block to session_log.md,
  and appends learned rules to references/project-standards.md — both persisted to GitHub.
  ALWAYS use this skill at session end. Trigger on: "end of session", "wrap up", "consolidate
  findings", "update project knowledge", "write session close", "save progress", or when
  workplan-orchestrator session-end protocol runs.
---

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**All timestamps: `YYYY-MM-DD HH:MM`**

---

## Steps

### 1 — Review session
Compile from context: skills run (in order) · new GAP-XXX items · gaps resolved · escalations · blockers · skill anomalies · research-log-manager LOG calls completed or missed.

### 2 — Extract patterns
Identify recurring signals: sources failing verification · framing flags by section · skill failure modes · cross-section evidence gaps · languages consistently returning NO-DATA/THIN.

### 3 — Write rules to GitHub
For each pattern that is specific, actionable, and likely to recur:
1. GET `references/project-standards.md` + SHA.
2. Append: `RULE: {description}  CONDITION: {when}  ACTION: {what}  DATE: YYYY-MM-DD HH:MM`
3. PUT back. Commit: `session-consolidator: append rule [{YYYY-MM-DD HH:MM}]`

### 4 — Research log hygiene
If `multilingual-research` ran this session and `research-log-manager` LOG was not called: flag as BLOCKER in YAML.

### 5 — Write session close to GitHub
1. GET `session_log.md` + SHA.
2. Append YAML block (never overwrite existing entries):

```yaml
---
session_close: YYYY-MM-DD HH:MM
document: "[DOC-ID]"
skills_run: []
gaps_added: []
gaps_resolved: []
escalations_triggered: 0
patterns_noted: []
rules_added: []
blockers: []
research_log_updated: true|false
next_action:
  skill: name
  input_file: filename
  parameters: {}
```

3. PUT back. Commit: `session-consolidator: append session close [{YYYY-MM-DD HH:MM}]`

### 6 — Report to user (≤5 lines)
Accomplishments · gaps added/resolved · next action · rules added · GitHub write status (✓ / ⚠ fallback)

---

## Fallback — GitHub write failure
If PUT fails after one retry: output YAML block and any rule text as fenced code blocks in chat. Instruct user to paste into `session_log.md` and `references/project-standards.md` manually. Never silently drop session state.
