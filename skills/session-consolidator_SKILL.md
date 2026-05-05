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
> **C2 overhaul 2026-05-05:** Register queries now use SQLite instead of markdown/YAML.
> **Phase 1-C verified 2026-05-04:** Steps 1b (gaps, connections) confirmed SQLite-native. No remaining markdown register dependencies.


<!-- Updated: 2026-05-04 — Phase 1-C verification pass -->

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

**SQLite gaps table**
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

**[ARCHIVED — use SQLite connections table]**
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
- If Decision Register was updated this session: verify `SQLite decisions table (canonical per A12 §5.1; legacy workplan/v10-1-decision-register.md superseded)` reflects changes.
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

### 1c. CS8 decision capture (per A12 decision-protocol)
Run after Step 1b — before pattern extraction.

**Working-session counter.** A "working session" produces or substantively modifies project content. Sessions that only adjust skills, fix typos, or rebase commits do not count.
- GET `data/doctrine_recheck/working_session_counter.yaml`. If absent, treat counter = 0.
- If this session is a working session: increment by 1; PUT back.
- If counter % 25 == 0: include `recheck_due: PERIODIC` in session close YAML (next session's first action runs `scripts/doctrine_recheck.py`).
- If this session closed a stage transition: include `recheck_due: STAGE_TRANSITION` in session close YAML.

**Decision capture.** For each decision made this session in any of the 5 categories (D-DOCT / D-METH / D-SCHEMA / D-OP / D-PRES per A12 §1):
- Build a Decision record per A12 §3.2 (16 fields). Required: decision_id (next D-NNNN), category, delegation, summary, outcome, rationale, decision_date, decided_by, model_routing (per A12 §4.4 notation), effort_level, decision_artifacts, status=ACTIVE, review_status (NA for DG-NON/DG-AUTO; PENDING for DG-REVIEW).
- D-DOCT records require `alternatives_considered`; D-DOCT or D-METH with `delegation: DG-AUTO` (default departure) require `delegation_rationale`.
- GET `SQLite decisions table`. Append the new Decision records. Validate the register through `scripts/decision_capture.py --register-only` before writing back.
- Each new RULE appended to `references/project-standards.md` (Step 3) MUST be paired with a Decision record. The RULE's section reference appears in the Decision's `decision_artifacts`.

**Detection heuristics for "decision made this session":**
- New CANONICAL governance doc → 1 D-DOCT
- New RULE in project-standards.md → 1 record (category by content)
- New schema entity, enum, or validator behaviour → 1 D-SCHEMA
- New session_close.next_action that pivots from prior session's plan → 1 D-OP
- Voice / formatting / register conventions adopted → 1 D-PRES

If the session made no doctrinal decisions, this step is a no-op (counter increments anyway).

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
- PUT back. Commit: `session-consolidator: append rule [YYYY-MM-DD HH:MM:SS]`

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
- Timestamps in the YAML `session_close:` field: use `date -u +"%Y-%m-%d %H:%M:%S"` as canonical source. This is the single timestamp authority for all session operations.
- This is always a NEW file — never append to an existing session file.
- PUT (no SHA required for new files).
- Commit: `session-consolidator: session close [YYYY-MM-DD HH:MM:SS]`
- **Update LATEST pointer:** After writing the session file, GET `sessions/LATEST`, PUT back with content = this session's filename (e.g. `session_084.md`, no trailing newline). Commit: `session-consolidator: update LATEST [session_NNN]`.

**YAML schema:**
```yaml
session_close: YYYY-MM-DD HH:MM:SS
github_writes: []  # list of files committed this session
commit_oid: ""     # first 12 chars of batch_commit() OID — required if any GitHub writes occurred
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

**"Start a new conversation" constraint:** Only include this instruction in next_action output if (a) context is ≥85% consumed OR (b) the next task requires a materially different workflow type. Never include it for simple phase continuations, sequential task execution, or status-check follow-ons. When in doubt, omit it — the user can always start a new conversation; the overhead cost of unnecessary conversation fragmentation is higher than the cost of a long context.

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

1. Query SQLite gaps table.
2. For each item in the *prior* session's `blockers:` list: check if its associated gap ID is now CLOSED in the register. If CLOSED: do not carry forward to this session's YAML. If still OPEN: carry forward with updated context if relevant.
3. If a blocker is listed in the current session's YAML without a corresponding OPEN gap register entry: either create the gap entry or remove the blocker — never let a blocker float without a gap ID.
4. Write the validated `blockers:` list only.

**Rule:** Stale blockers cause workplan drift. Validate every close.

---

## Quarterly Skill Performance Review (CO-0006 2026-04-08)

**Trigger:** After every 10 multilingual-research LOG calls (tracked in project-standards.md under `multilingual_research_run_count`). Invoke as part of session close when count reaches a multiple of 10.

**Increment counter:** At every session close where ≥1 multilingual-research LOG was completed, increment `multilingual_research_run_count` in project-standards.md by the number of LOG calls completed this session.

### Review process

1. **Aggregate per-language yield** from search-log entries for the last 10 runs:
   - Yield = sources found / searches run, per language
   - Pull language-level `results: N` from search-log YAML across last 10 slug entries

2. **Flag underperforming languages:** yield <10% across 3+ consecutive runs = underperformance trigger

3. **For each underperforming language:** review and update multilingual-research_SKILL.md:
   - Keyword quality — are native aliases confirmed, or still UNVERIFIED?
   - Database selection — is the right database targeted for this language?
   - Concept boundary warnings — are warnings causing excessive deviation?
   - Record adaptation in `multilingual_research_adaptations` log in project-standards.md

4. **Track adaptation effectiveness:** In the following 3 runs for that language, note whether yield improved. If yield remains <10% after adaptation: flag as `[LANGUAGE-THIN-PERSISTENT]` in project-standards.md and note in gap register as P3 scope gate candidate.

### Output (append to session close YAML)
```yaml
quarterly_skill_review:
  triggered: true | false
  run_count_at_close: {N}
  languages_reviewed: [{LANG}, ...]
  adaptations_made: [{description}, ...]
  languages_flagged_persistent_thin: [{LANG}, ...]
```
