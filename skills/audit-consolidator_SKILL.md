---
name: audit-consolidator
description: >
  Collects all findings from an item audit pipeline run and produces a structured
  research brief at references/audit-briefs/{item_code}_brief.md. Queries tracking DB
  by item_code for gaps, conflicts, connections, and deferred citations; organises them
  into two action tables (research actions and authoring corrections) plus connection
  and citation sections. Updates item_audit_runs status to COMPLETE. Pure collation —
  no synthesis. Runs as Step 8 of item-audit-pipeline wrapper, or standalone after
  all audit steps are complete for an item. Trigger on: "consolidate the audit",
  "produce the brief", "audit-consolidator".
  Decision: D-0149, 2026-05-05.
---

# Audit Consolidator

**Model:** Sonnet 4.6 · effort 75 · extract (pure collation — no synthesis)
**Intake:** item_code + session (required) · run_id (from item_audit_runs)
**Output:** references/audit-briefs/{item_code}_brief.md committed to GitHub
**Side effect:** item_audit_runs status → COMPLETE; brief_path populated

---

## Step 1 — Load findings from tracking DB

```python
import sqlite3, json
conn = sqlite3.connect('data/guidebook.db')
conn.row_factory = sqlite3.Row
ITEM = '{item_code}'

# Gaps for this item (all open, all sessions — not filtered by session)
gaps = conn.execute(
    "SELECT * FROM gaps WHERE section=? AND status LIKE 'OPEN%' ORDER BY priority, category",
    (ITEM,)
).fetchall()

# Conflicts for this item
conflicts = conn.execute(
    "SELECT * FROM conflicts WHERE item_code=? ORDER BY status, domain",
    (ITEM,)
).fetchall()

# Connections referencing this item
connections = conn.execute("""
    SELECT c.con_id, c.confidence, c.connection_type, c.description, c.status
    FROM connections c
    JOIN connection_targets ct ON c.con_id = ct.con_id
    WHERE ct.target LIKE ? AND c.status='PENDING'
    ORDER BY c.confidence DESC, c.con_id
""", (f'%{ITEM}%',)).fetchall()

# Deferred citations
deferred_citations = conn.execute(
    "SELECT slug, local_ref_id, deferred_reason, created_by_session FROM citation_mining "
    "WHERE deferred_reason IS NOT NULL ORDER BY created_by_session",
).fetchall()

# Audit run record
run = conn.execute(
    "SELECT * FROM item_audit_runs WHERE item_code=? ORDER BY created_at DESC LIMIT 1",
    (ITEM,)
).fetchone()
```

---

## Step 2 — Validate gap_id integrity (compensating FK check)

For each conflict with a gap_id set, verify the gap exists and is OPEN:

```python
for c in conflicts:
    if c['gap_id']:
        gap = conn.execute(
            "SELECT gap_id, status FROM gaps WHERE gap_id=?", (c['gap_id'],)
        ).fetchone()
        if not gap:
            orphan = f"[DATA-INTEGRITY: {c['conflict_id']} references deleted gap {c['gap_id']}]"
            # Add to brief header warnings
        elif 'CLOSED' in gap['status']:
            orphan = f"[DATA-INTEGRITY: {c['conflict_id']} references closed gap {c['gap_id']} — review]"
```

---

## Step 3 — Categorise gaps for brief

Routing by category:

**Research Actions** (require research or resolution evidence):
- RP → functional-deficit-researcher or multilingual-research
- EC → economics-researcher
- EG → evidence-auditor → FDR
- CONF → cross-population-conflict-mapper (resolution evidence run)
- MX → multilingual-research

**Authoring Corrections** (require ISW authoring correction):
- AUDT → item-specification-writer
- SW → item-specification-writer
- CR → connection-discovery → ISW cross-reference
- CD → item-specification-writer

**Infrastructure** (not routed to ISW or research):
- CI → technical
- DEC → workplan-orchestrator
- ST → structure-auditor

---

## Step 4 — Produce brief (markdown)

Write to `references/audit-briefs/{item_code}_brief.md`:

```markdown
# Audit Brief — {item_code}: {item_name}
**Date:** {YYYY-MM-DD HH:MM} UTC
**Run ID:** {run_id}
**Pipeline steps complete:** {steps_complete as comma-separated list}
**Steps started but not complete (mid-step failures):** {incomplete if any, else "None"}

{DATA-INTEGRITY warnings if any}

---

## Research Actions

Items requiring research, conflict resolution, or evidence retrieval.

| Gap ID | Category | Priority | Skill | Description |
|---|---|---|---|---|
| GAP-NNN | RP | P2 | functional-deficit-researcher | ... |

## Authoring Corrections

Items requiring ISW authoring correction or cross-reference addition.

| Gap ID | Category | Priority | Skill | Description |
|---|---|---|---|---|
| GAP-NNN | AUDT | P2 | item-specification-writer | ... |

---

## Active Conflicts

| Conflict ID | Domain | Pop A | Pop B | Status | Gap ID |
|---|---|---|---|---|---|
| CONF-NNNN | | | | UNRESOLVED | GAP-NNN |

*(No conflicts logged for this item)* if empty.

---

## Pending Connections

New connections awaiting ISW integration.

| CON-ID | Confidence | Type | Description |
|---|---|---|---|
| CON-NNNN | HIGH | CROSS-ITEM | ... |

*(No pending connections)* if empty.

---

## Deferred Citations

Sources encountered during audit deferred for future mining sessions.

| Source slug | Local ref | Deferred reason | Session |
|---|---|---|---|

*(No deferred citations)* if empty.

---

## Summary

**Gaps logged:** N total (P1: N · P2: N · P3: N)
**Research actions:** N gaps
**Authoring corrections:** N gaps
**Conflicts:** N (resolved: N · unresolved: N)
**Pending connections:** N
**Deferred citations:** N
**Economics-researcher trigger:** YES (P2 EC gap present) / NO
**FDR trigger:** YES (RP gap with FDR-TRIGGER scenario) / NO
```

---

## Step 5 — Commit brief to GitHub

```bash
# Get SHA of existing brief if it exists (may be updating a prior brief)
BRIEF_PATH="references/audit-briefs/{item_code}_brief.md"

# Commit via GitHub API (PUT to contents endpoint)
# Message format:
# audit-consolidator: {item_code} brief {YYYY-MM-DD HH:MM}
```

---

## Step 6 — Update item_audit_runs

```bash
python3 scripts/db.py update-audit-run \
  --run-id {run_id} \
  --session {session} \
  --status COMPLETE \
  --brief-path "references/audit-briefs/{item_code}_brief.md"
```

---

## Rules

1. Brief location: always `references/audit-briefs/{item_code}_brief.md`
2. Prior briefs from earlier sessions are preserved — do not overwrite; append new run
   as a dated section if brief already exists for this item
3. DATA-INTEGRITY warnings appear in the brief header — never silently omitted
4. All OPEN gaps for the item are included — not filtered by session
   (prior sessions' gaps are part of the current picture)
5. CONFIRMED_STRATUM and UNDERCLAIMED evidence-auditor findings are not logged to DB
   and will not appear in the brief — this is by design
6. Steps in steps_started but not steps_complete are flagged in the brief header
   as mid-step failures — not silently ignored
7. Feeds into: item-audit-pipeline (step 8); ISW (via brief); economics-researcher and FDR (via brief)
