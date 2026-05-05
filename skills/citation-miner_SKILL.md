---
name: citation-miner
description: >
  Backward and forward citation mining for confirmed Tier 1–3 sources in the guidebook
  evidence base. Runs in two modes: INLINE (triggered automatically by research skills
  when a source is confirmed) and BATCH (standalone pass over all unmined sources in a
  slug or globally). Depth-1 only — mine references of each source but never recurse
  into discovered sources within the same session. Tracks all mining in SQLite via
  db.py CLI. Produces bibliography-ready output. ALWAYS use when asked to: mine citations,
  find related sources, trace citation networks, expand evidence base, generate bibliography.
  Trigger on: "citation mining", "mine references", "cited by", "backward citations",
  "forward citations", "expand evidence base", "bibliography", "unmined sources".
---

**Model:** Sonnet 4.6 + web search
**Connectors:** PubMed, Scholar Gateway, Consensus — activate for mining.
**SQLite:** `data/guidebook.db` via `scripts/db.py`

---

## 1. Two Modes

### INLINE mode (called from research skills)

When multilingual-research, functional-deficit-researcher, economics-researcher, or
literature-review-planner confirms a Tier 1–3 source:

1. Calling skill passes: `(slug, local_ref_id, doi)`
2. Citation-miner checks:
   ```bash
   python3 scripts/db.py is-mined --slug {slug} --ref {local_ref_id}
   ```
   Returns: `{"mined": false}` or `{"backward": 0/1, "forward": 0/1, ...}`
3. If already mined (both B+F) → skip, return
4. If unmined or partial → mine missing direction(s)
5. Log result:
   ```bash
   python3 scripts/db.py log-mining \
     --slug {slug} \
     --ref {local_ref_id} \
     --direction backward \
     --connections '["CON-0247","CON-0248"]' \
     --session {session_filename} \
     --doi {doi}
   ```
   Run once per direction (backward, then forward as separate calls).
6. Return discovered sources to calling skill

**Depth-1 enforced:** discovered sources are recorded but NOT mined in the same pass.

### BATCH mode (standalone)

When citation-miner is invoked directly:

1. Query unmined sources:
   ```bash
   # All slugs, Tier 1-3:
   python3 scripts/db.py unmined --tier-max 3
   # Single slug:
   python3 scripts/db.py unmined --slug {slug} --tier-max 3
   ```
2. For each: mine backward + forward, log both directions
3. After completing all sources in a slug:
   ```bash
   python3 scripts/db.py update-bpc --slug {slug} --citation-mining-complete 1 --session {session}
   ```
4. Report: total mined, new sources discovered, remaining unmined

**Depth-1 enforced:** discovered sources added to evidence_sources but NOT mined this run.

---

## 2. Mining Protocol

### Backward Mining (reference list)
1. Retrieve reference list via DOI → CrossRef, PubMed, or Scholar Gateway
2. Filter for relevance (§3)
3. For each relevant reference:
   - Verify existence (PubMed/Scholar lookup)
   - Classify evidence tier
   - Check if already in evidence_sources (dedup by `doi_less_key`)
   - If new: INSERT into evidence_sources + source_slug_links
   - discovery_method field: `backward_from:{local_ref_id}`

### Forward Mining (cited by)
1. Scholar Gateway forward citations or Google Scholar "cited by"
2. Filter for relevance (§3)
3. For each relevant citing paper: same protocol as backward, discovery_method: `forward_from:{local_ref_id}`

---

## 3. Relevance Filter

**Include** if ANY:
- Same population + built environment element as input source
- OT clinical evidence (Tier 1) for same spec domain
- Lived experience data for same population
- Systematic review covering input topic

**Exclude** if ANY:
- Pure clinical without built environment application
- Duplicate: check `doi_less_key` = `lower(first_author_surname + year + first3_title_words)`

---

## 4. SQLite Schema Reference

### evidence_sources columns (Phase 1 schema)
`ref_id, authors, year, title, doi, doi_less_key, pmid, tier, evidence_type, jurisdiction, metadata_quality, verification_status, notes`

**Note:** `authors` (not `surname`), `tier` (not `evidence_tier`), no `language` or `journal` columns.

### source_slug_links columns
`ref_id, slug, local_ref_id`

### citation_mining columns
`slug, local_ref_id, global_ref_id, doi, backward, forward, connections_produced, notes`

### Adding new sources
```bash
python3 scripts/db.py add-source \
  --ref-id {local_ref_id} \
  --authors "{authors}" \
  --year {year} \
  --title "{title}" \
  --tier {tier} \
  --doi {doi} \
  --jurisdiction {jur} \
  --slug {slug} \
  --local-ref-id {local_ref_id} \
  --session {session}
```

---

## 5. Bibliography Output

Query for bibliography generation:
```sql
SELECT es.ref_id, es.authors, es.year, es.title, es.doi, es.tier,
       es.jurisdiction,
       GROUP_CONCAT(DISTINCT ssl.slug) as slugs,
       cm.backward, cm.forward
FROM evidence_sources es
LEFT JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
LEFT JOIN citation_mining cm ON cm.local_ref_id = ssl.local_ref_id AND cm.slug = ssl.slug
GROUP BY es.ref_id
ORDER BY es.authors COLLATE NOCASE, es.year
```

Format:
```
[{ref_id}] {authors} ({year}). {title}. DOI: {doi}
  Tier: {tier} | Jurisdiction: {jurisdiction}
  Slugs: {slugs} | Mining: B={backward} F={forward}
```

---

## 6. Depth-1 Rule (hard constraint)

Mine references OF the source ✓ · Mine citations OF the source ✓ · Record new sources ✓
Mine references of discovered sources ✗ NEVER · Mine citations of discovered sources ✗ NEVER

---

## 7. Integration with Research Skills

All research skills MUST invoke citation-miner inline for every confirmed Tier 1–3 source:
1. Research skill confirms source + assigns tier
2. Calls citation-miner inline with `(slug, local_ref_id, doi)`
3. Citation-miner: `is-mined` check → mine if needed → `log-mining`
4. Returns new sources to research skill
5. Research skill includes new sources in LOG output

---

## 8. Session Report

```markdown
## Citation Mining Summary — {date}
**Mode:** {inline|batch}
**Sources processed:** {N}
**New sources discovered:** {N}
**Connections produced:** [{CON-IDs}]
**Slugs now fully mined:** [{list}]
**Remaining unmined (Tier 1–3):**
```sql
SELECT COUNT(*), ssl.slug FROM evidence_sources es
JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
LEFT JOIN citation_mining cm ON cm.slug = ssl.slug AND cm.local_ref_id = ssl.local_ref_id
WHERE es.tier IN (1,2,3) AND (cm.local_ref_id IS NULL OR cm.backward=0 OR cm.forward=0)
GROUP BY ssl.slug ORDER BY COUNT(*) DESC
```
