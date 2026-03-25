---
name: citation-miner
description: >
  Backward and forward citation mining for confirmed Tier 1–3 sources in the guidebook
  evidence base. For every confirmed source: mine its reference list (backward) and
  Google Scholar "cited by" (forward) to discover additional relevant evidence. ALWAYS
  use this skill when asked to: mine citations, find related sources, trace citation
  networks, discover additional evidence from a known source, perform backward citation
  mining, perform forward citation mining, or expand the evidence base from existing
  references. Trigger on: "citation mining", "mine references", "cited by", "backward
  citations", "forward citations", "trace the citation network", "find related papers",
  "expand evidence base". Phase 2B skill — runs after initial multilingual-research
  retrieval.
---

**Model:** Sonnet 4.6 + web search
**Input:** Source list (author, year, title, DOI if available, tier) from multilingual-research or BPC
**Output:** New sources discovered + tier classification + BPC update data
**Connectors:** PubMed, Scholar Gateway, Consensus — activate for mining.

---

## 1. Mining Protocol

### Backward Mining (reference list)
For each input source:
1. Retrieve the source's reference list via:
   - DOI → CrossRef API or publisher page
   - PubMed → "References" section
   - Scholar Gateway → source record
2. Scan references for relevance: title contains target population code terms OR built environment terms
3. For each relevant reference found:
   - Verify it exists (PubMed/Scholar Gateway lookup)
   - Classify evidence tier per §1.5 hierarchy
   - Record: author, year, title, journal, DOI, tier, language, jurisdiction, discovery method (backward from {source})

### Forward Mining (cited by)
For each input source:
1. Search Google Scholar "cited by" or Scholar Gateway forward citations
2. Filter by relevance: title/abstract contains target population + built environment terms
3. Apply recency filter: prioritise post-2015 sources (but don't exclude earlier if highly relevant)
4. For each relevant citing paper:
   - Verify it exists
   - Classify evidence tier
   - Record as above with discovery method (forward from {source})

---

## 2. Relevance Filter

A discovered source is relevant if it meets ANY of:
- Addresses the same population code AND built environment element as the input source
- Provides OT clinical evidence (Tier 1) for the same specification domain
- Provides lived experience data (Co-1) for the same population
- Is a systematic review covering the input source's topic
- Provides jurisdiction-specific beyond-code data not yet in the BPC

A discovered source is NOT relevant if:
- Pure medical/clinical without built environment application
- Policy/advocacy without specification-level data
- Duplicate of an already-known source

---

## 3. Output Format

```markdown
## Citation Mining Report — {slug}
**Date:** YYYY-MM-DD HH:MM
**Sources mined:** [N]
**New sources discovered:** [N] (backward: [N], forward: [N])

### Backward mining
| Input source | Refs scanned | Relevant found | New to BPC |
|---|---|---|---|

### Forward mining
| Input source | Citing papers | Relevant found | New to BPC |
|---|---|---|---|

### New sources
| # | Authors | Year | Title | Journal | Lang | Jurisdiction | Tier | DOI | Discovery |
|---|---|---|---|---|---|---|---|---|---|

### Sources already known
[List of sources found that are already in the BPC — confirms network coverage]

### Mining gaps
[Languages/jurisdictions where mining produced no new results]
```

---

## 4. Integration with research-log-manager

After mining:
- New sources are added to the BPC entry for the slug under `citation_mining`:
  ```yaml
  citation_mining:
    backward: [N]
    forward: [N]
    sources_added: [N]
    sources_mined: [list of input source identifiers]
  ```
- New Tier 1–2 sources trigger re-evaluation of `best_practice_synthesis`
- Call `research-log-manager LOG` to update the search-log entry

---

## 5. Token Efficiency

- Mine ≤8 sources per run (prioritise highest-tier inputs)
- Stop forward mining at 20 citing papers per source (diminishing returns)
- If a source has >100 citing papers: filter by "cited by" sort relevance, take top 20
- Batch by slug: mine all sources for one slug before moving to next
- Checkpoint after each source: `CHECKPOINT — mined: {author year} — backward: {N} new — forward: {N} new`

---

## 6. Escalation Triggers

- Mining reveals a systematic review not previously identified → 🟡 flag for evidence-auditor (may change stratum)
- Mining reveals contradictory evidence → 🔴 flag for workplan-orchestrator (specification may need revision)
- Mining produces >10 new Tier 1–2 sources for a slug → flag as HIGH-YIELD; reassess best_practice_synthesis

---

**Preceded by:** `multilingual-research` (provides initial source list)
**Feeds into:** `research-log-manager LOG` · `evidence-auditor` (if new evidence changes strata) · `item-specification-writer` (if new evidence supports upgrades)
