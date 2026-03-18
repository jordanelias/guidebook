---
name: session-consolidator
description: >
  End-of-session memory consolidation for the Accessible Built Environments Guidebook project.
  Reviews session events, extracts recurring patterns, writes YAML resumption block to session_log.md,
  and appends learned rules to references/project-standards.md. Both files are persisted to GitHub.
  ALWAYS use this skill at session end. Trigger on: "end of session", "wrap up", "consolidate
  findings", "update project knowledge", "write session close", "save progress", or when
  workplan-orchestrator session-end protocol runs.
---

**Model:** Sonnet 4.6
**All timestamps: `YYYY-MM-DD HH:MM`** — no date-only entries anywhere in output.

---

## GitHub Backend

All writes go to `jordanelias/guidebook` · branch `main`.

**PAT:** Must be present in session context. If missing, prompt user before proceeding.

**Read a file:**
```
GET https://api.github.com/repos/jordanelias/guidebook/contents/{path}
Authorization: token {PAT}
```
Decode base64 `content` field. Capture `sha` for write.

**Write a file:**
```
PUT https://api.github.com/repos/jordanelias/guidebook/contents/{path}
Authorization: token {PAT}
Body: { "message": "{commit message}", "content": "{base64-encoded}", "sha": "{current sha}" }
```
Always GET before PUT. On 409: re-GET and retry once.

**Commit message convention:**
```
session-consolidator: {ACTION} [{YYYY-MM-DD HH:MM}]
```

---

## Steps

### 1 — Review Session
Compile from current session context:
- Skills run (in order)
- New GAP-XXX items produced
- Gaps resolved this session
- Escalations triggered
- Blockers encountered
- Skill performance anomalies
- `research-log-manager` LOG calls: completed or missed

### 2 — Extract Patterns
Identify recurring signals across the session:
- Sources consistently failing verification
- Sections with recurring framing flags
- Skill failure modes
- Evidence gaps appearing across multiple sections
- Languages consistently returning NO-DATA or THIN across topics

### 3 — Assess and Write Rules
For each pattern: is it specific, actionable, and likely to recur?

If yes:
1. GET `references/project-standards.md` — capture content + SHA.
2. Append rule entry:
   ```
   RULE: {description}  CONDITION: {when}  ACTION: {what}  DATE: YYYY-MM-DD HH:MM
   ```
3. PUT updated file back with SHA.
4. Commit: `session-consolidator: append rule to project-standards [{YYYY-MM-DD HH:MM}]`

### 4 — Research Log Hygiene
If `multilingual-research` was run this session:
- Confirm `research-log-manager` LOG was called.
- If not: flag as BLOCKER in YAML. Do not silently omit.

### 5 — Write Session Close to GitHub
1. GET `session_log.md` — capture content + SHA.
2. Append the following YAML block at the bottom of the file (never overwrite existing entries):

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

3. PUT updated `session_log.md` back with SHA.
4. Commit: `session-consolidator: append session close [{YYYY-MM-DD HH:MM}]`
5. Confirm write success. If PUT fails: output YAML block to user in chat as fallback with instruction to paste into GitHub manually.

### 6 — Report to User
≤5 lines:
- Accomplishments this session
- Gaps added / resolved
- Next action (skill + file)
- Rules added
- Research log status
- GitHub write status (✓ written / ⚠ failed — see fallback above)

---

## Fallback — GitHub Write Failure

If GitHub write fails after one retry:

1. Output the complete YAML block in a fenced code block in chat.
2. Output the complete rules text (if any) in a fenced code block.
3. Instruct user:
   > "GitHub write failed. Please paste the YAML block above into `session_log.md` in your repository, and the rules text into `references/project-standards.md`. Start the next session by providing the PAT and these blocks will be re-read correctly."

Never silently drop session state. Always surface it to the user if GitHub is unavailable.
