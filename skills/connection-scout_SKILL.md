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

## 1. Connection Registration (SQLite)

### Get next CON-ID
```bash
python3 scripts/db.py next-id connections
```
Returns: `CON-0248` (next available)

### Register new connection
```sql
INSERT INTO connections (con_id, status, confidence, connection_type,
  filed_in, description, source_skill, opus_reviewed,
  created_at, created_by_session, updated_at, updated_by_session)
VALUES ('CON-0248', 'PENDING', 'HIGH', 'CROSS-POPULATION',
  'sensory-environment', 'A-02 RT60 evidence applies to NDV/AUT classroom acoustic',
  'connection-scout', 0, '{ts}', '{session}', '{ts}', '{session}')
```

### Register connection targets
```sql
INSERT INTO connection_targets (con_id, target_type, target_id,
  created_at, created_by_session, updated_at, updated_by_session)
VALUES ('CON-0248', 'item', 'A-02', '{ts}', '{session}', '{ts}', '{session}')
```

### Update connection status
```sql
UPDATE connections SET status = 'CONSUMED',
  updated_at = '{ts}', updated_by_session = '{session}'
WHERE con_id = 'CON-0248'
```

---

## 2. Scanning Protocol

### Internal mode
Scans existing BPC entries, OPEN gap register items, FDR findings, and session
reports for unrecognised cross-population overlaps.

**Sources to scan:**
- BPC files: `references/bpc/{topic}/{slug}.md` — all active BPC entries
- Gap register: `SELECT * FROM gaps WHERE status = 'OPEN'`
- FDR compound scenarios: `references/fdr/` files
- Connection register: `SELECT * FROM connections WHERE status = 'PENDING'`

**Scan procedure:**
1. For each BPC slug, extract: populations served, specifications involved, evidence sources
2. Cross-reference: find specs that serve multiple populations with overlapping evidence
3. Compound interaction scan: for each FDR compound scenario, check if both populations'
   BPCs address the same environmental parameter
4. Gap-connection bridge: OPEN gap items may indicate missing connections

### External mode
Searches for published cross-references between existing BPC sources.

**Procedure:**
1. For each confirmed Tier 1–2 source, check if it's cited by sources in OTHER slugs
2. Use Scholar Gateway / PubMed forward citations
3. If cross-slug citation found → register as CROSS-ITEM connection

---

## 3. Connection Detail Writing

For PENDING connections that need details, write topic-level detail to per-topic
connection files on GitHub: `references/connections/{topic}/connections.md`

Each detail entry includes:
- CON-ID, target items, populations affected
- Evidence basis (which sources support the connection)
- Recommended action (ISW upgrade, new BPC entry, conflict registration)
- Priority assessment

After writing details: update SQLite `connections.description` field.

---

## 4. Connection Consumption (ISW handoff)

When item-specification-writer consumes a connection:

1. ISW applies the connection's evidence to the target item spec
2. ISW updates SQLite: `UPDATE connections SET status = 'CONSUMED' WHERE con_id = ?`
3. If connection reveals a conflict: register in conflicts table

---

## 5. Querying Connections

### Pending connections by priority
```bash
python3 scripts/db.py gaps  # shows gap summary
```
```sql
SELECT c.con_id, c.confidence, c.description,
  GROUP_CONCAT(ct.target_id) as targets
FROM connections c
JOIN connection_targets ct ON c.con_id = ct.con_id
WHERE c.status = 'PENDING'
ORDER BY
  CASE c.confidence WHEN 'HIGH' THEN 1 WHEN 'MODERATE' THEN 2 ELSE 3 END
```

### Connection count by status
```sql
SELECT status, COUNT(*) FROM connections GROUP BY status
```

---

## 6. Rules

1. Always use `next-id connections` for CON-ID assignment — never manually increment
2. HIGH confidence connections → feed directly to item-specification-writer
3. SPECULATIVE connections → register in gap register as P3
4. Per-topic connection markdown files on GitHub are being archived (Phase 1-E) —
   description text migrates to SQLite `connections.description` column
5. Do NOT read or write the archived `references/connection-register-active.md`
