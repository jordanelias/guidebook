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

**Model:** Sonnet-class (judgment required for evidence and framing)
**SQLite:** `data/guidebook.db`
**GitHub backend:** `jordanelias/guidebook` · `main` (Part 4 prose files)

---

## 0. Data Sourcing (SQLite-first)

> **Schema note (corrected 2026-08-02):** The `specification`, `specification_population`,
> `measurement`, and `room` tables **do not exist** in `data/guidebook.db` — verified against
> `sqlite_master`. The canonical equivalents are **`items`** (93 rows) and
> **`item_taxonomy_links`** (530 rows since migration 065 folded `item_axis_links` in;
> 372 carry the identity lens). The queries below have been repointed accordingly.
> The lens is a COLUMN since migration 065: `item_taxonomy_links` carries `identity_code`, `icf_code`, `needs_code` and `medical_code`, at least one set. Filter on the lens you mean, or an ICF-lens row arrives with a NULL population.
>
> Do **not** run `scripts/db/migrate_all.py`. It targets `data/db/guidebook.db`, a legacy path
> that does not exist; running it creates an empty database and then fails. If a query here
> returns empty, that is a finding about the data — not a signal to rebuild anything.


### Before writing or revising any item:

1. **Load the item record from SQLite:**
   ```sql
   SELECT * FROM items WHERE item_code = '{code}'
   ```

2. **Load evidence sources:**
   ```sql
   -- POINTER, NOT COPY (migration 063): author facts come from v_evidence_authors,
   -- which derives them from evidence_source_authors. The columns of the same name
   -- on evidence_sources are writer-retired tombstones and read NULL.
   SELECT es.ref_id, va.first_author_last, es.pub_year, es.pub_title, es.tier, es.language
   FROM evidence_sources es
   LEFT JOIN v_evidence_authors va ON va.ref_id = es.ref_id
   JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
   WHERE ssl.slug IN (SELECT bpc_source_slug FROM items WHERE item_code = '{code}')
   ORDER BY es.tier ASC
   ```

3. **Load population associations:**
   ```sql
   SELECT identity_code, applicability, subtype
   FROM item_taxonomy_links WHERE item_code = '{code}' AND identity_code IS NOT NULL
   ```

4. **Load connections targeting this item:**
   ```sql
   SELECT c.con_id, c.status, c.confidence, c.description
   FROM connections c
   JOIN connection_targets ct ON c.con_id = ct.con_id
   WHERE ct.target = '{code}' AND c.status = 'PENDING'
   ```

5. **Load BPC synthesis from GitHub:** GET `references/bpc/{topic}/{slug}.md`
   Check `bpc_metadata.citation_mining_complete` — if false, note in output.

### After writing or revising:

6. **Write structured fields — via migration, never a direct `UPDATE`.**

   > **Corrected 2026-08-02.** This step previously issued
   > `UPDATE specification SET summary, evidence_summary, why_md, schedule_md, …`.
   > That table does not exist, and **no table in `data/guidebook.db` carries those prose
   > fields** (checked column-by-column across all 63 tables). A direct `UPDATE` would also
   > violate the migrations-only rule.

   Prose is canonical in the markdown file — see step 7. Only these structured surfaces are
   writable, and each change ships as a migration
   (`scripts/emit_data_migration.py` → `scripts/migrate_db.py`):

   | Surface | Holds |
   |---|---|
   | `items` | `name`, `category`, `status`, `bpc_source_slug`, the `pmp_*` walk fields |
   | `item_taxonomy_links` | `identity_code`, `icf_code`, `needs_code`, `medical_code`, `applicability`, `subtype`, `rationale_ref` |
   | `specifications` | the per-(item × population) synthesis record and its `governing_refs` |

   ⚑ **Open question for the owner:** whether the spec template's prose fields should have a
   home in the schema at all, or remain file-canonical. Today they are file-canonical by
   default rather than by decision — which is part of why 79 of 87 generated spec pages
   render an empty best-practice banner.

7. **Write updated Part 4 prose to GitHub** (the markdown file remains canonical for prose)

8. **Trigger citation-miner inline** for any new Tier 1–3 source confirmed during the revision

---

## 1. BPC Opus-Synthesis Check

Query SQLite before writing:
```sql
SELECT citation_mining_complete, bpc_complete, evidence_state
FROM bpc_metadata WHERE slug = '{slug}'
```
If `citation_mining_complete = 0`: emit warning — evidence base may be incomplete.
If `bpc_complete = 0`: emit warning — BPC synthesis not finalised.
**Note:** No `opus_synthesis` column in schema — use `bpc_complete` as the synthesis gate.

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
| Population Mode | Identified population(s) most likely to use building | Ranges; median is population-informed default |
| Person Mode | Named client/person; specific building | Co-design: OT + client resolve specific value |

### Specification Range Doctrine
Ranges are not uncertainty — they bridge Population Mode and Person Mode.
- Population Mode: use median as population-informed default
- Person Mode: position within range determined through co-design (OT + client)
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

**Evidence markers — THREE, per `governance/tier-system.md` §5 (OPERATIVE):**

| Marker | Means | Licensed by |
|---|---|---|
| **●** | confirmed evidence base | T1 / Co-1 / T2 / Co-2, or T3-clinical |
| **◐** | policy or standards basis only | T4 / T5 |
| **○** | weak band — grey, expert consensus, thin, or code-consensus | T3-grey, T6, or a regulatory-stratum claim under Option A |

Every prescriptive sentence carries exactly one. Unmarked is an error.
Non-prescriptive sentences carry no marker.

> **This section used to read "● = evidence-based (Tier 1–6 source); ○ = inferred."**
> That is the retired two-marker scheme, and it is not merely out of date — it
> inverts the doctrine. Under it a T6 code-consensus claim earns a full-strength
> ●, which `tier-system.md` §3/§8 and the Option A amendment
> (DR-2026-07-21) exist specifically to forbid: **code convergence is not
> evidence.** A code-consensus claim may anchor best practice *only* at the
> flagged weak band ○ ("best practice as currently known"); rendered at ●, ◐, or
> unflagged, it is in error. `mission-and-epistemics.md` still describes the old
> scheme too — a known reconciliation drift; `tier-system.md` is operative and
> wins. Corrected 2026-08-06, found by a read-only audit of this phase.
> The marker must not exceed what the cell's `tier_basis` licenses.

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
