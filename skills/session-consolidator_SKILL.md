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
**GitHub backend:** `jordanelias/guidebook` · `main` · All GitHub operations use `github-io` patterns.
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

**Scope: session-local change log only.** Check only files touched or referenced in THIS session (skills run, gaps added/resolved, rules added, connections consumed). Do not re-read all state files from scratch — that is a periodic dedicated activity, not a per-session task.

For each file below that was modified or referenced this session: GET current content from GitHub. Check against session work compiled in Step 1. Fix any discrepancy inline (update the file, PUT back). If a fix cannot be completed inline, flag as BLOCKER — do not silently skip.

**gap_register.md**
- Every gap described as raised this session → entry exists with correct ID, priority, status OPEN, and today's timestamp.
- Every gap described as resolved → status field is CLOSED / CLOSED-RESOLVED / CLOSED-DELETED / CLOSED-NOTED.
- Every gap described as a known limitation → status is KNOWN-LIMITATION with rationale.
- Fix: append corrected or missing entry; update status inline.

**references/project-standards.md**
- Every rule described as added this session → RULE block present with matching DATE.
- Fix: append missing rule.

**references/search-log/{topic}/{slug}.md** (per-slug files)
- Every `multilingual-research` run described this session → per-slug search-log file present, `last_searched` matches session date.
- Fix: cannot reconstruct search results post-hoc → flag as BLOCKER.

**references/bpc/{topic}/{slug}.md** (per-slug files)
- Every slug confirmed in search-log → BPC entry present.
- Fix: cannot reconstruct BPC content post-hoc → flag as BLOCKER.

**references/connection-register-active.md**
- Every connection described as CONSUMED this session → status updated from PENDING to CONSUMED with today's timestamp and item reference.
- Every new connection identified this session by `connection-scout` → PENDING entry present with correct priority and population codes.
- Every connection described as DEFERRED or SUPERSEDED → status field reflects that state.
- Fix: update status inline; append missing entries. Cannot reconstruct scout output post-hoc → flag as BLOCKER.

**Project Instructions**
- Compare session decisions (new rules, structural changes, skill updates, population code changes) against PI content.
- If PI is stale → flag as BLOCKER with specific section(s) requiring update. Do not auto-edit PI — flag for author action.

**sessions/ directory**
- No prior session's `next_action` is being skipped without explanation in the current session YAML.
- No duplicate filename for the current session timestamp.
- Fix: add explanation to `next_action` field; suffix `-b` if collision.

**parts/v10/ directory** (v10.1 addition)
- If any per-Part files were edited this session: verify manifest line/heading counts still match. Deviation → 🟡 WARNING (manifest needs update).
- If new Part files were created: verify manifest includes them.
- If file-splitter ran: verify manifest exists and is complete.

**workplan/ directory** (v10.1 addition)
- If Decision Register was updated this session: verify `workplan/v10-1-decision-register.md` reflects changes.
- If Change Orders were issued: verify `references/change-orders/` contains the CO file.
- For each watched directory (`workplan/`, `versions/current/`): GET listing. If >1 non-directory file outside the directory's `deprecated/` subdirectory, and a new file was committed to that directory this session: invoke `github-filing` on that directory before writing session YAML. Report result in reconciliation block.

**Reconciliation output** — compact table, reported to user and included in session YAML:

| file | checked | discrepancies_found | fixed_inline | blockers_raised |
|---|---|---|---|---|
| gap_register | ✓ | N | N | N |
| project_standards | ✓ | N | N | N |
| search_log | ✓ | N | N | N |
| bpc | ✓ | N | N | N |
| connection_register | ✓ | N | N | N |
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

#### 5a. Concurrent session isolation (pre-write — always runs first)

Each session is an independent record. Session files are never merged, shared, or overwritten.

1. **Fresh read:** GET `sessions/LATEST` from GitHub now — do not use the value cached at session start.
2. **Capture fresh `_head_oid`** from this read. Use it as `expectedHeadOid` for all subsequent commits. Discard the session-start OID.
3. **If LATEST has changed since session start** (another session closed while this one ran):
   a. Note the concurrent session filename — log it in this session's YAML under `concurrent_sessions`.
   b. Do **not** attempt to read, merge, or reconcile the concurrent session's content.
   c. Proceed to write this session's file unconditionally. Session records are independent.
   d. **LATEST update:** attempt to update `sessions/LATEST` to this session's filename. If `expectedHeadOid` conflict on that commit (another session also updating LATEST): leave LATEST as-is. Log `latest_updated: false` in this session's YAML. Session file is still written and valid.
4. **If LATEST is unchanged:** proceed normally. Update LATEST after writing session file.

**At next session open:** Session Protocol Step 1b reads LATEST. If `latest_updated: false` appears in that session's YAML, or if the LATEST file predates the most recent session file by timestamp: read the last 3 session files to surface all active threads and report them to the user before task intake.

**On `expectedHeadOid` conflict on the session file write itself:** re-fetch head OID and retry once. If second attempt fails: output session YAML as fenced code block with manual paste instructions — never drop state.

- **Filename:** GET `sessions/LATEST`. Parse the number from the current value (e.g. `session_083.md` → 83). Next file = zero-padded three-digit increment: `session_084.md`. If LATEST contains a legacy timestamp filename, treat the count of all `session_` files in the directory as N; next = N+1.
- Check for collision: GET the new filename. If 404: proceed. If exists: increment again.
- Timestamps in the YAML `session_close:` field: use `date -u +"%Y-%m-%d %H:%M"` as canonical source. This is the single timestamp authority for all session operations.
- This is always a NEW file — never append to an existing session file.
- PUT (no SHA required for new files).
- Commit: `session-consolidator: session close [YYYY-MM-DD HH:MM]`
- **Update LATEST pointer:** After writing the session file, GET `sessions/LATEST`, PUT back with content = this session's filename (e.g. `session_084.md`, no trailing newline). Commit: `session-consolidator: update LATEST [session_NNN]`.

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
  gap_register:        {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  project_standards:   {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  search_log:          {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  bpc:                 {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  connection_register: {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  sessions:            {checked: true, discrepancies: 0, fixed: 0, blockers: 0}
  project_instructions: {checked: true, stale_sections: 0, blockers: 0}
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


### Pre-Close: Uncommitted Working Document Check

Before writing the session YAML, verify no working documents are uncommitted:

1. Check for any files created during the session in `/home/claude` or referenced as working documents.
2. If any working document has content not yet committed to GitHub: commit it now, or log it explicitly in `blockers:` with the filename.
3. The `reconciliation.sessions` block must include `{checked: true}` only if this check passes.

**Rule:** No session closes with uncommitted working documents. Data loss prevention.

### Pre-Close: YAML Blocker Validation

Before writing the session YAML, validate the `blockers:` list against the gap register:

1. GET `gap_register.md`.
2. For each item in the *prior* session's `blockers:` list: check if its associated gap ID is now CLOSED in the register. If CLOSED: do not carry forward to this session's YAML. If still OPEN: carry forward with updated context if relevant.
3. If a blocker is listed in the current session's YAML without a corresponding OPEN gap register entry: either create the gap entry or remove the blocker — never let a blocker float without a gap ID.
4. Write the validated `blockers:` list only.

**Rule:** Stale blockers cause workplan drift. Validate every close.

