---
name: connection-discovery
description: >
  Identify new cross-item, cross-population, compound-interaction, and methodology
  connections from newly available source material (BPC prose, item specifications,
  citation mining output) and log them to the SQLite connections table via db.py.
  Use this skill whenever: new citation mining has completed for a slug, a new item
  specification has been written or materially updated, a new BPC synthesis has
  been completed, or a research session has produced sources not yet scanned for
  connections. Do NOT use for auditing or validating existing connections — that is
  connection-auditor.
---

# Connection Discovery

**Model:** Opus 4.6 (multi-step synthesis across dispersed evidence required)
**Execution pattern:** Hybrid — Claude performs synthesis; output validated by db.py schema
**Output target:** SQLite `connections` table via `python3 scripts/db.py add-connection`

> **Schema note:** `connection_type` is NULL on all entries migrated from the legacy
> `.md` register. Type field is only populated on entries created by this skill going
> forward. Do not filter or sort existing data by `connection_type`.

---

## When to run

- After any citation mining session (`db.py log-mining` has just been called)
- After ISW produces a new item specification
- After a BPC synthesis is completed or materially revised
- Explicitly invoked: "run connection discovery on [slug/item]"

Do not run mid-session on material you have not yet finished processing — wait until
the source content is stable.

---

## Step 0 — Scope and dedup load

Identify the scope of the current run:

```
scope_type: slug | item | mixed
scope_id:   [slug name] | [item code, e.g. G-03] | [list]
```

Query existing connections for the specific items in scope to build a dedup list.
Do not use `--summary` (returns totals only, not CON-IDs):

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 -c "
import sqlite3, json, os
conn = sqlite3.connect(os.environ['GUIDEBOOK_DB_PATH'])
conn.row_factory = sqlite3.Row
# Replace G-03 with your target item(s) — run once per item in scope
rows = conn.execute('''
  SELECT c.con_id, c.status, c.description
  FROM connections c
  JOIN connection_targets ct ON c.con_id = ct.con_id
  WHERE ct.target LIKE \"%G-03%\"
  ORDER BY c.con_id
''').fetchall()
for r in rows:
    d = dict(r)
    print(d['con_id'], d['status'], d['description'][:80])
"
```

Cache the returned CON-IDs. Any new connection mapping to the same source + target +
connection_type as an existing entry is a duplicate — skip it.

---

## Step 1 — Read source material

Load the relevant content. Priority order:

1. **New BPC prose** — best_practice_synthesis section + evidence_gaps section
2. **Item specification** — full item text (Mode P + Mode S notes + population annotations)
3. **Citation mining results** — new sources logged since last discovery run

For BPC files, read the full synthesis section. Do not skim — connection opportunities
concentrate in evidence gaps, co-occurrence notes, and population caveats.

---

## Step 2 — Identify connections

For each substantive finding in the source material, ask:

> Does this finding imply a design relationship between two items, populations, or
> methodological principles that is not already captured in the connection register?

Four connection types to test for:

| Type | Test question |
|---|---|
| `CROSS-ITEM` | Does this evidence for item X directly affect or constrain item Y? |
| `CROSS-POPULATION` | Does this finding for population A conflict with or reinforce a finding for population B on the same physical parameter? |
| `COMPOUND-INTERACTION` | Would applying spec X and spec Y simultaneously to the same individual produce a non-additive outcome? |
| `METHODOLOGY` | Does this finding affect the guidebook's methodological framework (Part 1, Part 3, evidence hierarchy, mode definitions)? |

**Confidence assignment:**

| Level | Criteria |
|---|---|
| `HIGH` | Direct evidence links the two targets; relationship is explicit in source |
| `MODERATE` | Relationship is implied by clinical reasoning or evidence gap; not directly stated |
| `SPECULATIVE` | Plausible but no direct evidence; flag clearly |

Do not log SPECULATIVE connections unless the relationship is material enough to
warrant ISW attention in future. When in doubt, omit.

---

## Step 3 — Get next CON-ID

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py next-id connections
```

Increment sequentially for each new connection in the batch.

---

## Step 4 — Log each connection

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py add-connection \
  --con-id CON-XXXX \
  --confidence HIGH \
  --connection-type CROSS-ITEM \
  --filed-in [topic-slug] \
  --description "[one sentence: what the connection is and why it matters for ISW]" \
  --source-skill connection-discovery \
  --targets '["item:G-03", "item:E-10"]' \
  --session [session-name]
```

**`filed-in` valid values** (match existing topic slugs):
`bathrooms-and-wet-areas` · `entrances-and-circulation` · `wayfinding-and-signage` ·
`sensory-environment` · `health-and-symptom-management` · `seating-and-rest` ·
`kitchens-and-workspaces` · `controls-and-hardware` · `communication-and-alerts` ·
`cross-cutting` · `frameworks-and-methodology` · `room-types` · `population-general`

**`targets` format:** JSON array. Each entry: `"item:A-16"`, `"part:Part 3 §3.8"`,
`"bpc:mob-upper-limb"`, or `"methodology:evidence-hierarchy"`.

**Description quality bar:** Must be actionable by ISW without further lookup.
Bad: "G-03 and E-10 are related."
Good: "Roxburgh 2024 rest interval evidence (E-10) implies grab bar placement
continuity requirement along circulation routes that G-03 does not currently address."

---

## Step 5 — Batch commit

After logging all connections for the session:

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 scripts/db.py connections \
  --status PENDING --summary
```

Verify count increased as expected. Then commit the DB to GitHub via github-io
batch_commit with message:
`connection-discovery: [N] new connections [slug/item scope] [YYYY-MM-DD HH:MM]`

---

## Output summary (inline, after run)

```
Connection Discovery — [scope]
New connections logged: N
  HIGH:       N
  MODERATE:   N
  SPECULATIVE: N
Topics: [list of filed-in slugs]
Next CON-ID: CON-XXXX
Duplicates skipped: N
```
