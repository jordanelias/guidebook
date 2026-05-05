---
name: research-log-manager
description: >
  SQLite-backed search log and Best Practices Compendium (BPC) manager. Three actions:
  CHECK (query slug status from SQLite + load BPC from GitHub), LOG (write search results
  to search-log file + update SQLite coverage), RETRIEVE (load BPC for item-specification-writer).
  Uses per-slug topic-directory architecture. ALWAYS use before and after every
  multilingual-research run. Trigger on: "CHECK slug", "LOG results", "RETRIEVE BPC",
  "search status", "what do we know about", or any research workflow start/end.
---

**Model:** Sonnet 4.6 (mechanical) or Opus 4.6 (if BPC synthesis judgment needed)
**GitHub backend:** `jordanelias/guidebook` · `main`
**SQLite:** `data/guidebook.db` via `scripts/db.py`

---

## Slug Resolution (all actions)

Query SQLite first, then resolve GitHub paths:

```bash
python3 scripts/db.py synonyms {slug_candidate}
```

If the slug exists in the `slugs` table: use canonical slug name and `topic_directory`.
If not found: check `terms` table for alias match, then `slugs` for the canonical form.

**New slug:** INSERT into slugs table, create both SL and BPC files on GitHub, commit.

```bash
# Check if slug exists
python3 scripts/db.py coverage {slug}
```

Derive paths:
- Search log: `references/search-log/{topic_directory}/{slug}.md`
- BPC: `references/bpc/{topic_directory}/{slug}.md`

---

## CHECK action

1. Query SQLite for slug status:
   ```bash
   python3 scripts/db.py coverage {slug}
   ```
   Returns: jurisdiction coverage, language coverage, evidence tier range, mining status

2. If slug exists: GET BPC file from GitHub for current synthesis content
3. Report to calling skill:
   - Jurisdictions searched / not searched
   - Languages searched / not searched
   - Evidence tier range (highest → lowest)
   - Citation mining complete? (from `bpc_metadata.citation_mining_complete`)
   - Search coverage gaps

**If slug is NEW:** report "No prior research. Starting fresh."

---

## LOG action

After multilingual-research completes:

1. **Update search-log file on GitHub:** Append search results, new sources, coverage data
2. **Update SQLite coverage:**
   ```bash
   # upsert-coverage has no CLI subcommand — call directly:
   python3 -c "import sys; sys.path.insert(0, 'scripts'); from db import upsert_search_coverage; upsert_search_coverage('
     --languages "EN,FR" --tiers "1,3,5" --session {session}
   ```
3. **Add new evidence sources to SQLite:**
   ```sql
   INSERT INTO evidence_sources (ref_id, surname, year, title, journal, doi,
     evidence_tier, language, jurisdiction, discovery_method,
     created_at, created_by_session, updated_at, updated_by_session)
   VALUES (...)
   ```
   ```sql
   INSERT INTO source_slug_links (ref_id, slug, role,
     created_at, created_by_session, updated_at, updated_by_session)
   VALUES (...)
   ```
4. **Update BPC file on GitHub:** Append new findings to BPC synthesis sections
5. **Invoke citation-miner inline** for every confirmed Tier 1–3 source (per §7 of citation-miner skill)

**Threshold management:** Search-log files on GitHub have no token limit — they grow freely.
SQLite coverage data replaces the need to parse search-log headers at session start.

---

## RETRIEVE action

1. GET BPC file from GitHub: `references/bpc/{topic_directory}/{slug}.md`
2. Parse: best_practice_synthesis, consensus_findings, divergent_findings, key_sources, NO-DATA
3. Return structured data to item-specification-writer or calling skill

---

## Slug Registry Migration

The markdown `references/slug-registry.md` is archived. Slug data now lives in SQLite:

```sql
SELECT slug, topic_directory, status, evidence_state, pico_complete,
       search_complete, bpc_complete, citation_mining_complete
FROM slugs
WHERE status = 'ACTIVE'
```

Do NOT read or write `slug-registry.md`. All slug operations go through SQLite.

---

## BPC Front-Matter

BPC files retain their GitHub markdown format. The front-matter metadata is also
mirrored in `bpc_metadata` SQLite table. When updating a BPC file:
1. Update the markdown file on GitHub (canonical content)
2. Update `bpc_metadata` in SQLite (queryable status)

---

## Rules

1. CHECK before / LOG after every research run — skipping = error
2. research-log-manager CHECK triggers before citation-miner batch — ensures slug context
3. 3+ NO-DATA for same language across topics → file gap register entry via SQLite:
   ```bash
   python3 scripts/db.py add-gap --category RES --priority P3 --description "..." --session {session}
   ```
4. Never permanently close a language — mark THIN and move on
5. All source additions go through evidence_sources table — no standalone markdown source lists
