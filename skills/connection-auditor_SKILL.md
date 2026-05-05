---
name: connection-auditor
description: >
  Query and validate existing connections in the SQLite connections table. Use to:
  surface PENDING connections for ISW prioritisation, audit CONSUMED-DEFERRED entries
  for resolution, validate that CONSUMED connections were properly reflected in target
  item specifications, and identify stale or low-confidence connections that should be
  retired or downgraded. Trigger on: "audit connections", "what connections are pending",
  "check consumed-deferred", "validate connection robustness", "what hasn't been applied",
  "run a connection audit", or any request to review the state of the connection register.
  Do NOT use for discovering new connections — that is connection-discovery.
---

# Connection Auditor

**Model:** Sonnet 4.6 (structured querying + validation; no open-ended synthesis)
**Execution pattern:** Python Tool (queries) + Hybrid (action recommendations)
**Input:** filter parameters (status, confidence, type, target item, topic)
**Output:** audit report with ACTION recommendations per connection

> **Schema note:** `connection_type` is NULL on all entries migrated from the legacy
> `.md` register. Type-based filtering (e.g. flagging `COMPOUND-INTERACTION`) applies
> only to entries created by connection-discovery. Do not assume NULL = untyped error.

---

## Modes

Run one or more modes per session depending on task. State which mode(s) you are running.

| Mode | Purpose | Typical trigger |
|---|---|---|
| `PENDING` | List PENDING connections; recommend ISW order | "what should ISW tackle next" |
| `DEFERRED` | Audit CONSUMED-DEFERRED; flag unresolved | "check what's been deferred" |
| `ROBUSTNESS` | Verify CONSUMED connections reflected in target items | "validate connections for G-03" |
| `FULL` | All three modes in sequence | "run a full connection audit" |

---

## Mode: PENDING

### Query

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py connections \
  --status PENDING --confidence HIGH

GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py connections \
  --status PENDING --confidence MODERATE
```

### Prioritisation output

Group by `filed_in` topic. Within each topic, sort HIGH before MODERATE.
For each connection report:

```
CON-XXXX  [confidence]  [connection_type or "untyped"]
Targets:  [target list]
Action:   ISW — [brief rationale for priority]
```

**Flag for immediate ISW:** PENDING connections where the target item code appears
in the guidebook's item specification files — meaning the item exists but the
connection was never applied. This check requires a manual GitHub file-existence
lookup; it is not derivable from the DB alone.

**Flag for Opus session:** connections with `connection_type = 'COMPOUND-INTERACTION'`
(per project-standards compound functioning rule). Note: only applies to entries
created post-migration; migrated entries have NULL type.

---

## Mode: DEFERRED

### Query

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py connections \
  --status CONSUMED-DEFERRED
```

### For each CONSUMED-DEFERRED entry, determine:

1. **Was the primary connection consumed?** If the connection was split (partial
   application in one item, remainder deferred), confirm the primary target item
   spec includes the core finding.

2. **Is the deferred portion still actionable?** The deferred target may be a Part
   not yet written (Part 10, 11, 12 are common blockers). If so: status is correctly
   deferred — note the blocking Part.

3. **Has the deferred target since been written?** Requires a manual GitHub
   file-existence check for the target Part or item. If the target now exists,
   the deferral is stale — recommend CONVERT-TO-PENDING.

### Action codes

| Code | Meaning |
|---|---|
| `NO-ACTION` | Correctly deferred; blocking Part not yet written |
| `CONVERT-TO-PENDING` | Target now exists; deferral is stale; needs ISW |
| `RETIRE` | Connection no longer valid (target item removed/restructured) |
| `ESCALATE` | Compound interaction or high-stakes gap; flag for Opus session |

---

## Mode: ROBUSTNESS

Scope: one item code or topic slug. Query all CONSUMED connections targeting that scope:

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 -c "
import sqlite3, json, os
conn = sqlite3.connect(os.environ['GUIDEBOOK_DB_PATH'])
conn.row_factory = sqlite3.Row
rows = conn.execute('''
  SELECT c.con_id, c.confidence, c.connection_type, c.description,
         group_concat(ct.target, \", \") as targets
  FROM connections c
  JOIN connection_targets ct ON c.con_id = ct.con_id
  WHERE ct.target LIKE \"%G-03%\"
    AND c.status = \"CONSUMED\"
  GROUP BY c.con_id
  ORDER BY c.con_id
''').fetchall()
print(json.dumps([dict(r) for r in rows], indent=2))
"
```

Replace `G-03` with the target item code or topic keyword. Then fetch the current
item specification from GitHub via GraphQL and read it in full.

For each CONSUMED connection, verify:

- The connection's core finding appears in the item specification (Mode P note,
  population annotation, Mode S handoff, or evidence citation)
- The evidence tier claimed in the connection is consistent with what landed in the spec
- No contradictions between the connection description and the spec text

### Action codes

| Code | Meaning |
|---|---|
| `VERIFIED` | Connection properly reflected in spec |
| `PARTIAL` | Core finding present but incomplete; flag for next ISW pass |
| `MISSING` | Connection not reflected; recommend reopening as PENDING |
| `CONTRADICTED` | Spec contradicts connection; route to evidence-auditor |

---

## Output format

```
CONNECTION AUDIT — [mode] — [scope] — [YYYY-MM-DD HH:MM]
══════════════════════════════════════════════════════════

PENDING (HIGH confidence): N
PENDING (MODERATE confidence): N
CONSUMED-DEFERRED: N
  → CONVERT-TO-PENDING: N
  → NO-ACTION (blocked): N
  → RETIRE recommended: N

ROBUSTNESS (if run):
  Verified: N   Partial: N   Missing: N   Contradicted: N

PRIORITY ISW TARGETS:
  1. CON-XXXX — [filed_in] — [one-line rationale]
  2. CON-XXXX — ...

ACTIONS REQUIRING DECISION:
  CON-XXXX: [RETIRE | ESCALATE | CONVERT] — [reason]

GAP REGISTER: [N new P2 items recommended — descriptions below]
```

---

## Post-audit actions

**CONVERT-TO-PENDING:**

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py update-connection \
  --con-id CON-XXXX --status PENDING --session [session-name]
```

**RETIRE:**

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py update-connection \
  --con-id CON-XXXX --status CLOSED --session [session-name]
```

**New gap items from audit** (category `SW` = Specification Writing):

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py add-gap \
  --category SW --priority P2 \
  --description "[description]" \
  --session [session-name]
```

Commit all DB changes after post-audit actions:
`connection-auditor: [mode] audit + [N] status updates [YYYY-MM-DD HH:MM]`
