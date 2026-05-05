---
name: citation-miner
description: >
  Backward and forward citation mining for confirmed Tier 1–3 sources in the guidebook
  evidence base. Runs in two modes: INLINE (triggered automatically by research skills
  when a source is confirmed) and BATCH (standalone pass over all unmined sources in a
  slug or globally). Depth-1 only — mine references of each source but never recurse
  into discovered sources within the same session. Tracks all mining in SQLite via
  db.py CLI. Produces bibliography-ready output. ALWAYS use this skill when asked to:
  mine citations, find related sources, trace citation networks, expand evidence base,
  run citation mining pass, generate bibliography. Trigger on: "citation mining",
  "mine references", "cited by", "backward citations", "forward citations",
  "expand evidence base", "bibliography", "unmined sources".
---

**Model:** Sonnet 4.6 + web search
**Connectors:** PubMed, Scholar Gateway, Consensus — activate for mining.
**SQLite:** `data/guidebook.db` via `scripts/db.py`

---

## 1. Two Modes

### INLINE mode (called from research skills)

When multilingual-research, functional-deficit-researcher, economics-researcher, or
literature-review-planner confirms a Tier 1–3 source:

1. The calling skill passes: `(slug, ref_id, author, year, title, doi)`
2. Citation-miner checks: `python3 scripts/db.py is-mined {slug} {ref_id}`
3. If already mined (both B+F) → skip, return
4. If unmined or partial → mine missing direction(s)
5. Log result: `python3 scripts/db.py log-mining {slug} {ref_id} {direction} --connections CON-XXXX --session {session}`
6. Return discovered sources to calling skill

**Depth-1 enforced:** discovered sources are RECORDED but NOT mined in the same pass.
They enter the unmined queue for the next batch run.

### BATCH mode (standalone)

When citation-miner is invoked directly:

1. Query unmined sources:
   ```sql
   SELECT es.ref_id, es.surname, es.year, es.title, es.doi, ssl.slug
   FROM evidence_sources es
   JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
   LEFT JOIN citation_mining cm ON cm.slug = ssl.slug AND cm.local_ref_id = es.ref_id
   WHERE es.evidence_tier IN (1, 2, 3)
   AND (cm.backward IS NULL OR cm.backward = 0 OR cm.forward IS NULL OR cm.forward = 0)
   ORDER BY es.evidence_tier ASC, es.year DESC
   ```
2. For each unmined source: mine backward, mine forward, log to SQLite
3. After completing all sources in a slug: update `bpc_metadata.citation_mining_complete = 1`
4. Report: total mined, new sources discovered, remaining unmined

**Depth-1 enforced:** sources discovered during batch are added to evidence_sources
but NOT mined in the same batch run. They appear in the next batch query.

---

## 2. Mining Protocol

### Backward Mining (reference list)
For each source:
1. Retrieve reference list via DOI → CrossRef, PubMed references, or Scholar Gateway
2. Filter for relevance (see §3)
3. For each relevant reference found:
   - Verify existence (PubMed/Scholar lookup)
   - Classify evidence tier per §1.5 hierarchy
   - Check if already in evidence_sources table
   - If new: add to evidence_sources + source_slug_links
   - Record discovery_method: `backward_from:{ref_id}`

### Forward Mining (cited by)
For each source:
1. Search Google Scholar "cited by" or Scholar Gateway forward citations
2. Apply recency filter: prioritise post-2015, don't exclude earlier if high-tier
3. Filter for relevance (see §3)
4. For each relevant citing paper:
   - Verify existence
   - Classify evidence tier
   - Check if already in evidence_sources
   - If new: add to evidence_sources + source_slug_links
   - Record discovery_method: `forward_from:{ref_id}`

---

## 3. Relevance Filter

**Include** if ANY:
- Same population code AND built environment element as input source
- OT clinical evidence (Tier 1) for same specification domain
- Lived experience data (Co-1) for same population
- Systematic review covering input source's topic
- Jurisdiction-specific beyond-code data not yet in evidence base

**Exclude** if ANY:
- Pure medical/clinical without built environment application
- Policy/advocacy without specification-level data
- Duplicate of existing source (check by dedup key: `lower(surname + year + first_5_title_words)`)

---

## 4. SQLite Integration

### Pre-mining check (mandatory)
```bash
python3 scripts/db.py is-mined {slug} {ref_id}
```
Returns: `{"backward": 0/1, "forward": 0/1, "connections_produced": [...]}` or null

### Post-mining log (mandatory)
```bash
python3 scripts/db.py log-mining {slug} {ref_id} backward --connections CON-0247,CON-0248 --session session_2026-05-05
python3 scripts/db.py log-mining {slug} {ref_id} forward --connections CON-0249 --session session_2026-05-05
```

### Adding new sources
New sources discovered during mining are added to evidence_sources via direct SQL
INSERT (not yet exposed as db.py subcommand — add if needed). Required fields:
- ref_id (next available in slug's REF-ID sequence)
- surname, year, title, journal
- doi (if available)
- evidence_tier
- language, jurisdiction
- discovery_method

### Slug completion check
After all sources in a slug are mined (B+F):
```sql
UPDATE bpc_metadata SET citation_mining_complete = 1,
  updated_at = '{timestamp}', updated_by_session = '{session}'
WHERE slug = '{slug}'
```

---

## 5. Bibliography Output

When asked for bibliography or when a mining pass completes, generate formatted
bibliography from evidence_sources:

```bash
python3 scripts/db.py coverage {slug}
```

For full bibliography generation, query:
```sql
SELECT es.ref_id, es.surname, es.year, es.title, es.journal, es.doi,
       es.evidence_tier, es.language, GROUP_CONCAT(ssl.slug) as slugs
FROM evidence_sources es
JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
GROUP BY es.ref_id
ORDER BY es.surname, es.year
```

Format each entry as:
```
[REF-ID] Surname, Initials (Year). Title. *Journal*, Volume(Issue), Pages. DOI: xxx
  Tier: N | Language: XX | Slugs: slug-1, slug-2
  Mining: B={status} F={status} | Discovered via: {method}
```

---

## 6. Depth-1 Rule

**This is a hard constraint.** During any single invocation (inline or batch):

- Mine the references OF the input source ✓
- Mine the citations OF the input source ✓
- Record any new sources discovered ✓
- Mine the references of discovered sources ✗ NEVER
- Mine the citations of discovered sources ✗ NEVER

Discovered sources enter the unmined queue. They will be mined in a SUBSEQUENT
invocation (next batch run or next inline trigger). This prevents citation mining
from consuming unbounded context chasing citation chains.

---

## 7. Integration with Research Skills

All research skills that confirm Tier 1–3 sources MUST invoke citation-miner
in inline mode before completing their run. The integration point is:

1. Research skill confirms source exists and assigns tier
2. Research skill calls citation-miner inline: `(slug, ref_id, author, year, title, doi)`
3. Citation-miner checks is-mined, mines if needed, logs result
4. Citation-miner returns any new sources to research skill
5. Research skill includes new sources in its LOG output

**Skills with this integration:**
- multilingual-research (Step 4: mandatory citation-miner invocation)
- functional-deficit-researcher (Step 4b: mandatory after diminishing-return gate)
- economics-researcher (Step 7: mandatory for E-1/E-2 sources)
- literature-review-planner (Section 3: during plan scoping)

---

## 8. Session Reporting

At end of any mining session, produce:

```markdown
## Citation Mining Summary — {date}
**Mode:** {inline|batch}
**Sources processed:** {N} (backward: {N}, forward: {N})
**New sources discovered:** {N}
**Connections produced:** {CON-IDs}
**Slugs completed:** {list of slugs where all sources now mined}
**Remaining unmined:** {N} sources across {N} slugs
```

Query for remaining unmined:
```sql
SELECT COUNT(*) as unmined, ssl.slug
FROM evidence_sources es
JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
LEFT JOIN citation_mining cm ON cm.slug = ssl.slug AND cm.local_ref_id = es.ref_id
WHERE es.evidence_tier IN (1, 2, 3)
AND (cm.backward IS NULL OR cm.backward = 0 OR cm.forward IS NULL OR cm.forward = 0)
GROUP BY ssl.slug
ORDER BY unmined DESC
```
