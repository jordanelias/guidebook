<!-- GOVERNED BY PROJECT INSTRUCTIONS — execution copy only. PI definition governs on conflict. -->
<!-- C2 OVERHAUL 2026-05-05: SQLite-first data sourcing + citation mining integration -->

---
name: item-specification-writer
description: >
  Draft, revise, and audit item-level design specifications for the guidebook. SQLite-first:
  reads evidence from evidence_sources, writes spec fields to specification table, triggers
  citation mining for confirmed sources. Applies design modes, specification range doctrine,
  social model framing, and population code cross-referencing. ALWAYS use when asked to:
  write a new spec, revise an existing item, draft evidence tables, write room matrices,
  or produce structured item-level content. Trigger on: "write the item", "draft the spec",
  "revise this item", "new specification", "item spec", "ISW", "evidence upgrade".
---

**Model:** Sonnet 4.6 (judgment required for evidence and framing)
**SQLite:** `data/guidebook.db`
**GitHub backend:** `jordanelias/guidebook` · `main` (Part 4 prose files)

---

## 0. Data Sourcing (SQLite-first)

### Before writing or revising any item:

1. **Load spec record from SQLite:**
   ```sql
   SELECT * FROM specification WHERE item_code = '{code}'
   ```

2. **Load evidence sources:**
   ```sql
   SELECT es.ref_id, es.surname, es.year, es.title, es.evidence_tier, es.language
   FROM evidence_sources es
   JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
   WHERE ssl.slug IN (SELECT bpc_source_slug FROM specification WHERE item_code = '{code}')
   ORDER BY es.evidence_tier ASC
   ```

3. **Load population associations:**
   ```sql
   SELECT population_code, role FROM specification_population
   WHERE spec_id IN (SELECT spec_id FROM specification WHERE item_code = '{code}')
   ```

4. **Load connections targeting this item:**
   ```sql
   SELECT c.con_id, c.status, c.confidence, c.description
   FROM connections c
   JOIN connection_targets ct ON c.con_id = ct.con_id
   WHERE ct.target_id = '{code}' AND c.status = 'PENDING'
   ```

5. **Load BPC synthesis from GitHub:** GET `references/bpc/{topic}/{slug}.md`
   Check `bpc_metadata.citation_mining_complete` — if false, note in output.

### After writing or revising:

6. **Write spec fields to SQLite:**
   ```sql
   UPDATE specification SET
     summary = ?, evidence_summary = ?, why_md = ?, schedule_md = ?,
     question_heading = ?, dar_relevant = ?, dar_note = ?,
     retrofit_category = ?, ot_evidence_basis = ?,
     person_specific_note = ?, evidence_tier = ?,
     updated_at = ?, updated_by_session = ?
   WHERE item_code = '{code}'
   ```

7. **Write updated Part 4 prose to GitHub** (the markdown file remains canonical for prose)

8. **Trigger citation-miner inline** for any new Tier 1–3 source confirmed during the revision

---

## 1. BPC Opus-Synthesis Check

Query SQLite before writing:
```sql
SELECT citation_mining_complete FROM bpc_metadata WHERE slug = '{slug}'
```
If `citation_mining_complete = 0`: emit warning that evidence base may be incomplete.

---

## 2. Governing Principles

### Social Model (non-negotiable)
The built environment creates barriers. People are not the problem.
- CRPD Articles 9, 19, 30 govern all specification decisions.
- State the ideal built environment first. Constraints only where genuinely necessary.
- Never: "to help users with X". Always: "to remove the barrier".

### Design Modes
| Mode | Context | Specification standard |
|---|---|---|
| Universal Mode | No particular population predominant | Above code minimum, allows tailoring |
| Mode P | Identified population(s) most likely to use building | Ranges; median is population-informed default |
| Mode S | Named client/person; specific building | Co-design: OT + client resolve specific value |

### Specification Range Doctrine
Ranges are not uncertainty — they bridge Mode P and Mode S.
- Mode P: use median as population-informed default
- Mode S: position within range determined through co-design (OT + client)
- Never "between X and Y" without specifying which end at which mode

---

## 3. Item Format

```markdown
### [CODE] [Title — Descriptive Only; No Values in Heading]

**Population codes:** [code list]
**Typology:** Residential · Non-Residential · Both
**Design stage:** [SD / DD / TA / Construction / Post-occupancy]

#### Specification

● or ○ [Ideal provision — best achievable outcome first]
● or ○ [Best practice — guidebook target for new build]
● or ○ [Acceptable — where spatial/structural constraint exists]
● or ○ [Minimum — hard floor, not a target]

#### Evidence basis

| Tier | Source | Claim supported |
|---|---|---|
| [1–6] | [Author, Year] | [Specific claim] |

#### Conflict notes
[Only where this item conflicts with another population's provision]

#### Cross-references
[Internal refs to related items, evidence annex, DAR register]

#### Retrofit note
**Retrofit:** [HIGH / MODERATE / LOW penalty]
```

**Evidence markers:** ● = evidence-based (Tier 1–6 source); ○ = inferred (gap disclosed).
Non-prescriptive sentences carry no marker.

---

## 4. Population Code Rules

Apply all 11 codes. Never collapse sub-codes.
- `●` primary, `○` secondary, `—` not applicable
- Conflict → flag `⚠ CONFLICT` + apply conflict resolution rules

**Canonical:** MOB (MOB/AMB, MOB/UPL) · VIS · DEAF · NEU (NEU/PCS) · DEM · NDV (NDV/AUT, NDV/ADHD, NDV/SENS) · NDV/MH · PAIN · DBL · OFS (OFS/ME, OFS/POTS, OFS/MCAS)

---

## 5. Evidence Rules

- Every prescriptive claim carries citation or tier marker
- Unsupported: flag `[UNSUPPORTED — citation required]`
- Single-source: flag `[SINGLE SOURCE — Tier X]`
- Two sentences max in item body for rationale — extended rationale in evidence annex
- After confirming any new source: add to `evidence_sources` table + trigger citation-miner

---

## 6. Connection Consumption

When revising an item based on a PENDING connection:
1. Apply the connection's evidence to the spec
2. Update SQLite: `UPDATE connections SET status = 'CONSUMED' WHERE con_id = ?`
3. If connection reveals a new conflict: register in conflicts table
4. Log consumed connection in session report

---

## 7. Heading Rule
No values, ranges, or thresholds in item headings. Navigational label only.

## 8. No-Value Heading Rule
Sequencing: Ideal → Best Practice → Acceptable → Minimum within each item.

## 9. Escalation
- Unresolvable cross-population conflict → cross-population-conflict-mapper
- >2 evidence markers need upgrading → citation-miner batch on slug
- DAR integration needed → flag for Part 6/10 update
