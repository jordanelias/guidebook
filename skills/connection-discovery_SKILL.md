---
name: connection-discovery
description: >
  Identify new cross-item, cross-population, compound-interaction, and methodology
  connections from item specifications, BPC evidence, and published citation networks,
  and log them to the SQLite connections table via db.py. Three modes: spec (item
  specifications and cross-reference tables), evidence (BPC files, gap register,
  session outputs), external (forward citation search via Scholar Gateway / PubMed).
  Use this skill whenever: new citation mining has completed for a slug, a new item
  specification has been written or materially updated, a new BPC synthesis has been
  completed, or a research session has produced sources not yet scanned for connections.
  Do NOT use for auditing or validating existing connections — that is connection-auditor.
  Merged: absorbs connection-scout (D-0146, 2026-05-05). connection-scout is deprecated.
---

# Connection Discovery

**Model:** Opus 4.6 (multi-step synthesis across dispersed evidence required)
**Execution pattern:** Hybrid — Claude performs synthesis; output validated by db.py schema
**Output target:** SQLite `connections` table via `python3 scripts/db.py add-connection`

> **Schema note:** `connection_type` is NULL on all entries migrated from the legacy
> `.md` register. Type field is only populated on entries created by this skill going
> forward. Do not filter or sort existing data by `connection_type`.

---

## Modes

| Mode | Trigger | Source material |
|---|---|---|
| `--mode spec` | New or updated item specification | Item spec text + cross-reference tables |
| `--mode evidence` | New BPC synthesis, gap register update | BPC files + gap register + pending connections |
| `--mode external` | Citation mining complete for a slug | Tier 1-2 forward citations via Scholar Gateway / PubMed |

Run spec and evidence modes together for a full per-item scan. External mode is
invoked separately after citation mining completes and is scoped to the mined slug.

Default mode when not specified: `spec`.

---

## When to run

- After any citation mining session (`db.py log-mining` has just been called)
- After ISW produces a new item specification
- After a BPC synthesis is completed or materially revised
- As Step 1 and Step 2 of the item-audit-pipeline wrapper
- Explicitly invoked: "run connection discovery on [slug/item]"

Do not run mid-session on material you have not yet finished processing.

---

## Step 0 — Scope and dedup load

Identify the scope of the current run:

```
scope_type: slug | item | mixed
scope_id:   [slug name] | [item code, e.g. G-03] | [list]
mode:       spec | evidence | external
```

Query existing connections for the specific items in scope to build a dedup list:

```bash
GUIDEBOOK_DB_PATH=data/guidebook.db python3 -c "
import sqlite3, json, os
conn = sqlite3.connect(os.environ['GUIDEBOOK_DB_PATH'])
conn.row_factory = sqlite3.Row
rows = conn.execute('''
  SELECT c.con_id, c.status, c.description
  FROM connections c
  JOIN connection_targets ct ON c.con_id = ct.con_id
  WHERE ct.target LIKE \"%I-01%\"
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

## Step 1 — Read source material (mode-dependent)

### spec mode
1. Item specification — full item text (Mode P + Mode S notes + population annotations)
2. Cross-reference tables in the spec (explicit cross-refs already noted by the author)
3. Items table for applicable_groups — population scope of the item

### evidence mode
Sources in priority order:
1. BPC files for the item's populations: `references/bpc/{topic}/{slug}.md`
   Read `best_practice_synthesis` and `evidence_gaps` sections in full. Do not skim.
2. Open gaps for this item: `python3 scripts/db.py gaps --status OPEN`
3. Pending connections for this scope: `python3 scripts/db.py connections --status PENDING`

For each BPC slug: extract populations, specs, evidence sources. Cross-reference for
multi-population overlapping specs. FDR compound scan: check both populations' BPCs
for the same environmental parameter on this item.

### external mode
1. Identify Tier 1-2 sources for the slug from `evidence_sources` table
2. For each source: use Scholar Gateway forward citations and PubMed related articles
3. Cross-slug citation found: assess as CROSS-ITEM connection candidate
4. Log new source to `citation_mining` with `deferred_reason=NULL` if mined;
   set `deferred_reason='not-relevant-to-{item_code}'` if deferred

---

## Step 2 — Identify connections

For each substantive finding in the source material, ask:

> Does this finding imply a design relationship between two items, populations, or
> methodological principles not already captured in the connection register?

**Connection type taxonomy:**

| Type | Test question |
|---|---|
| `CROSS-ITEM` | Does evidence for item X directly affect or constrain item Y? |
| `CROSS-POPULATION` | Does a finding for population A conflict with or reinforce a finding for population B on the same physical parameter? |
| `COMPOUND-INTERACTION` | Would applying spec X and spec Y simultaneously to the same individual produce a non-additive outcome? |
| `METHODOLOGY` | Does this finding affect the guidebook's methodological framework? |

**Confidence assignment:**

| Level | Criteria |
|---|---|
| `HIGH` | Direct evidence links the two targets; relationship explicit in source |
| `MODERATE` | Relationship implied by clinical reasoning or evidence gap; not directly stated |
| `SPECULATIVE` | Plausible but no direct evidence |

**Non-connection findings — mandatory routing:**

Not every finding is a connection. Apply this decision tree before logging anything:

```
Is this finding a relationship between two design entities?
  YES: Is it MODERATE confidence or above?
    YES → Log as connection (Step 4)
    NO  → SPECULATIVE → log as CR gap (investigate; close-deleted if unconfirmed)
  NO: Is this a gap in evidence or scope?
    YES → Log as gap via db.py add-gap (RP | AUDT | CONF as appropriate)
    NO: Is this a population conflict?
      YES → Route to cross-population-conflict-mapper
      NO  → Discard (not actionable)
```

**SPECULATIVE rule:** SPECULATIVE findings are logged as CR gaps, not as connections.
Category CR = cross-reference gap: investigate and document if confirmed.
CONN is not a valid gap category — do not use it.

```bash
python3 scripts/db.py add-gap \
  --category CR \
  --priority P3 \
  --description "SPECULATIVE: [what the relationship might be and why it needs verification]" \
  --skill connection-discovery \
  --session {session}
```

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

**`filed-in` valid values:**
`bathrooms-and-wet-areas` · `entrances-and-circulation` · `wayfinding-and-signage` ·
`sensory-environment` · `health-and-symptom-management` · `seating-and-rest` ·
`kitchens-and-workspaces` · `controls-and-hardware` · `communication-and-alerts` ·
`cross-cutting` · `frameworks-and-methodology` · `room-types` · `population-general`

**`targets` format:** JSON array. Each entry: `"item:A-16"`, `"part:Part 3 S3.8"`,
`"bpc:mob-upper-limb"`, or `"methodology:evidence-hierarchy"`.

**`source-skill`:** always `connection-discovery` regardless of mode used.

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

Verify count increased as expected. Commit DB to GitHub:
`connection-discovery: [N] new connections [scope] [mode] [YYYY-MM-DD HH:MM]`

---

## Step 6 — Connection consumption

When item-specification-writer consumes a connection:
1. ISW applies evidence to target spec
2. Update: `python3 scripts/db.py update-connection --con-id CON-XXXX --status CONSUMED --session {session}`
3. Connection reveals conflict: route to cross-population-conflict-mapper; do not log conflict here

---

## Schema reference

### connections columns
`con_id, status, confidence, connection_type, filed_in, description, source_skill,
opus_reviewed, session_applied, created_at, created_by_session, updated_at, updated_by_session`

### connection_targets columns
`con_id, target`
Target encoding: `item:E-08` | `slug:threshold-door-hardware` | `population:MOB`

### Status values
`PENDING` to `CONSUMED` | `CONSUMED-DEFERRED` | `CLOSED`

---

## Output summary (inline, after run)

```
Connection Discovery — [scope] --mode [mode]
New connections logged: N
  HIGH:        N
  MODERATE:    N
  SPECULATIVE: 0 (logged as CR gaps)
Gaps logged (non-connection findings): N
Topics: [list of filed-in slugs]
Next CON-ID: CON-XXXX
Duplicates skipped: N
```

---

## Rules

1. Always `next-id connections` for CON-ID — never manually increment
2. HIGH confidence: feed to item-specification-writer
3. SPECULATIVE: `add-gap --category CR` — never log as a connection
4. CONN is not a valid gap category — use CR for speculative cross-reference gaps
5. Per-topic connection markdown files archived (Phase 1-E) — descriptions live in `connections.description`
6. Do NOT read or write `references/connection-register-active.md` (archived)
7. Do NOT read or write `gap_register.md` directly — use `db.py` CLI only
8. Feeds into: cross-population-conflict-mapper (conflicts), item-audit-pipeline (steps 1+2)
9. Non-connection findings always exit via `db.py add-gap` — never as SPECULATIVE connection
