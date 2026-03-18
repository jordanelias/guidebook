---
name: session-consolidator
description: >
  End-of-session memory consolidation for the Accessible Built Environments Guidebook project.
  Reviews session events, reconciles state files against work performed, extracts recurring
  patterns, writes YAML session-close block to GitHub sessions/ directory, and appends learned
  rules to references/project-standards.md. ALWAYS use this skill at session end. Trigger on:
  "end of session", "wrap up", "consolidate findings", "update project knowledge", "write
  session close", "save progress", or when workplan-orchestrator session-end protocol runs.
---

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**All timestamps: `YYYY-MM-DD HH:MM`**

## Steps

### 1. Review session
Compile from conversation history:
- Skills run
- GAP-XXX items raised, resolved, or noted as limitations
- Escalations triggered
- Blockers encountered
- Skill anomalies
- `multilingual-research` LOG calls completed or missed

### 1b. Reconcile state files against session work
Run immediately after Step 1 — before extracting patterns or writing rules.

For each file below: GET current content from GitHub. Check against session work compiled in Step 1. Fix any discrepancy inline (update the file, PUT back). If a fix cannot be completed inline, flag as BLOCKER — do not silently skip.

**gap_register.md**
- Every gap described as raised this session → entry exists with correct ID, priority, status OPEN, and today's timestamp.
- Every gap described as resolved → status field is CLOSED / CLOSED-RESOLVED / CLOSED-DELETED / CLOSED-NOTED.
- Every gap described as a known limitation → status is KNOWN-LIMITATION with rationale.
- Fix: append corrected or missing entry; update status inline.

**references/project-standards.md**
- Every rule described as added this session → RULE block present with matching DATE.
- Fix: append missing rule.

**references/search-log.md**
- Every `multilingual-research` run described this session → slug entry present, `last_searched` matches session date, all searched language statuses recorded.
- Fix: cannot reconstruct search results post-hoc → flag as BLOCKER.

**references/best-practices-compendium.md**
- Every slug confirmed in search-log → BPC entry `## {slug}` present.
- Fix: cannot reconstruct BPC content post-hoc → flag as BLOCKER.

**sessions/ directory**
- No prior session's `next_action` is being skipped without explanation in the current session YAML.
- No duplicate filename for the current session timestamp.
- Fix: add explanation to `next_action` field; suffix `-b` if collision.

**Reconciliation output** — compact table, reported to user and included in session YAML:

| file | checked | discrepancies_found | fixed_inline | blockers_raised |
|---|---|---|---|---|
| gap_register | ✓ | N | N | N |
| project_standards | ✓ | N | N | N |
| search_log | ✓ | N | N | N |
| bpc | ✓ | N | N | N |
| sessions | ✓ | N | N | N |

### 2. Extract patterns
From session history and reconciliation findings:
- Failing or unreliable sources
- Recurring framing flags
- Skill failure modes
- Cross-section evidence gaps
- Languages consistently NO-DATA or THIN

### 3. Write rules to GitHub
For each specific, actionable, recurring pattern identified in Steps 1–2:
- GET `references/project-standards.md` + SHA.
- Append:
  ```
  RULE: {description}
  CONDITION: {when this applies}
  ACTION: {what to do}
  DATE: YYYY-MM-DD HH:MM
  ```
- PUT back. Commit: `session-consolidator: append rule [YYYY-MM-DD HH:MM]`

### 4. Research log hygiene
If `multilingual-research` ran and LOG was not called → flag as BLOCKER in session YAML.

### 5. Write session close to GitHub
- Determine filename: `sessions/session_{YYYY-MM-DD-HHMM}.md` using the session-close timestamp (not wall-clock if different).
- Check for collision: GET filename. If 404: proceed. If exists: append `-b` suffix.
- This is always a NEW file — never append to an existing session file.
- PUT (no SHA required for new files).
- Commit: `session-consolidator: session close [YYYY-MM-DD HH:MM]`

**YAML schema:**
```yaml
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
reconciliation:
  gap_register:     {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  project_standards: {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  search_log:       {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  bpc:              {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  sessions:         {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
next_action:
  skill: name
  session: description
  parameters: {}
```

### 6. Report to user (≤6 lines)
- Accomplishments
- Gaps added / resolved
- Rules added
- Reconciliation result: pass / N fixes applied / N blockers
- Next action
- GitHub write status (✓ / ⚠ fallback)

---

**Fallback:** if any PUT fails after one retry — output the relevant content as a fenced code block with manual paste instructions. Never silently drop state.
