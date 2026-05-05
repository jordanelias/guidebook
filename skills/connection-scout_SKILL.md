---
name: connection-scout
description: >
  Identify connections in the evidence base not yet reflected in the guidebook. Two modes:
  Internal (scans BPC, gap register, session outputs for cross-population overlaps and
  siloed solutions) and External (searches for published cross-references between existing
  BPC sources). Registers connections in SQLite via db.py CLI. ALWAYS use when: looking
  for cross-population connections, finding evidence overlaps, identifying siloed design
  solutions, or at edition boundaries. Trigger on: "find connections", "cross-population
  scan", "evidence connections", "what links exist".
---

**Model:** Opus 4.6 (judgment-heavy) or Sonnet 4.6 (batch detail writing)
**GitHub backend:** `jordanelias/guidebook` · `main`
**SQLite:** `data/guidebook.db` via `scripts/db.py`

---

## Schema Reference

### connections columns
`con_id, status, confidence, connection_type, filed_in, description, source_skill, opus_reviewed, session_applied, created_at, created_by_session, updated_at, updated_by_session`

### connection_targets columns
`con_id, target`
**Note:** single `target` column (not `target_type` + `target_id`). Encode type in the target string: `item:E-08`, `slug:threshold-door-hardware`, `population:MOB`.

---

## 1. Connection Registration (SQLite)

### Get next CON-ID
```bash
python3 scripts/db.py next-id connections
```
Returns JSON: `{"next_id": "CON-0248"}`

### Register new connection (direct SQL)
```sql
INSERT INTO connections
  (con_id, status, confidence, connection_type, filed_in, description,
   source_skill, opus_reviewed, created_at, created_by_session, updated_at, updated_by_session)
VALUES
  ('CON-0248', 'PENDING', 'HIGH', 'CROSS-POPULATION', 'sensory-environment',
   'A-02 RT60 evidence applies to NDV/AUT classroom acoustic parameter',
   'connection-scout', 0, '{ts}', '{session}', '{ts}', '{session}')
```

### Register connection targets (one row per target)
```sql
INSERT INTO connection_targets (con_id, target, created_at, created_by_session, updated_at, updated_by_session)
VALUES ('CON-0248', 'item:A-02', '{ts}', '{session}', '{ts}', '{session}')
```

Target format: `{type}:{identifier}` — e.g. `item:E-08`, `slug:threshold-door-hardware`, `population:MOB/UPL`

### Update connection status
```sql
UPDATE connections SET status = 'CONSUMED',
  updated_at = '{ts}', updated_by_session = '{session}'
WHERE con_id = 'CON-0248'
```

---

## 2. Scanning Protocol

### Internal mode
Sources to scan:
- BPC files: `references/bpc/{topic}/{slug}.md`
- Gap register: `python3 scripts/db.py gaps` (OPEN items only)
- Connections pending: `python3 scripts/db.py connections --status PENDING`

Procedure:
1. For each BPC slug: extract populations, specs, evidence sources
2. Cross-reference for multi-population overlapping specs
3. FDR compound scan: check both populations' BPCs for same environmental parameter
4. Gap-connection bridge: OPEN gaps may indicate missing connections

### External mode
1. For each Tier 1–2 source: check forward citations for cross-slug references
2. Use Scholar Gateway / PubMed forward citations
3. Cross-slug citation found → register as CROSS-ITEM connection

---

## 3. Querying Connections

```bash
# All pending HIGH confidence
python3 scripts/db.py connections --status PENDING --confidence HIGH

# Targeting a specific item
SELECT c.con_id, c.confidence, c.description
FROM connections c
JOIN connection_targets ct ON c.con_id = ct.con_id
WHERE ct.target LIKE 'item:E-08%' AND c.status = 'PENDING'
```

---

## 4. Connection Consumption

When item-specification-writer consumes a connection:
1. ISW applies evidence to target spec
2. ISW updates: `UPDATE connections SET status = 'CONSUMED' WHERE con_id = ?`
3. Connection reveals conflict → register in conflicts table (if it exists)

---

## 5. Rules

1. Always `next-id connections` for CON-ID — never manually increment
2. HIGH confidence → feed to item-specification-writer
3. SPECULATIVE → gap register via `db.py` (P3 priority)
4. Per-topic connection markdown files archived (Phase 1-E) — descriptions live in `connections.description`
5. Do NOT read or write `references/connection-register-active.md` (archived)
