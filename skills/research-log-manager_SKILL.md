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

> **C2 overhaul 2026-05-05:** All register operations use SQLite and db.py CLI.
> `slug-registry.md`, `gap_register.md`, and `citation-mining-register.md` are archived.
> All slug lookups, coverage writes, and gap filings go through db.py subcommands.

---

## Slug Resolution (all actions)

Query SQLite first:

```bash
python3 scripts/db.py coverage --slug {slug}
```

Returns: jurisdiction/language coverage counts, completeness flag.

For slug → topic_directory lookup:
```sql
SELECT slug, topic_directory, sl_path, bpc_path, status
FROM slugs WHERE slug = '{slug}'
```

**New slug:** INSERT into slugs table, create BPC + search-log files on GitHub, commit.

---

## CHECK action

1. Query coverage:
   ```bash
   python3 scripts/db.py coverage --slug {slug}
   ```
2. Query mining status:
   ```sql
   SELECT citation_mining_complete, bpc_complete, search_complete
   FROM bpc_metadata WHERE slug = '{slug}'
   ```
3. GET BPC file from GitHub: `references/bpc/{topic_directory}/{slug}.md`
4. Report to calling skill: jurisdictions searched/not searched, languages searched/not searched, evidence tier range, mining status, coverage gaps.

**New slug:** report "No prior research. Starting fresh."

---

## LOG action

After multilingual-research completes:

1. **Update search-log file on GitHub:** Append search results, new sources, coverage data.

2. **Update SQLite coverage (per jurisdiction searched):**
   ```bash
   python3 scripts/db.py upsert-coverage \
     --slug {slug} \
     --jurisdiction {jur_code} \
     --status searched \
     --co1-attempted {0|1} \
     --session {session_filename}
   ```
   Run once per jurisdiction attempted. Repeat for each.

3. **Update SQLite language coverage (per language searched):**
   ```bash
   python3 scripts/db.py upsert-language \
     --slug {slug} \
     --language {lang_code} \
     --status searched \
     --results-count {N} \
     --session {session_filename}
   ```
   Run once per language attempted.

4. **Add new evidence sources:**
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
     --session {session_filename}
   ```

5. **Update BPC file on GitHub:** Append new findings to BPC synthesis sections.

6. **Invoke citation-miner inline** for every confirmed Tier 1–3 source (per citation-miner §7).

---

## RETRIEVE action

1. GET BPC file from GitHub: `references/bpc/{topic_directory}/{slug}.md`
2. Parse: best_practice_synthesis, consensus_findings, divergent_findings, key_sources, NO-DATA flags.
3. Return structured data to item-specification-writer or calling skill.

---

## Rules

1. CHECK before / LOG after every research run — skipping = error.
2. Never read or write `references/slug-registry.md` (archived).
3. Never read or write `references/citation-mining-register.md` (archived).
4. 3+ NO-DATA for same language across topics → file gap:
   ```bash
   python3 scripts/db.py add-gap \
     --category RES \
     --priority P3 \
     --description "{language} NO-DATA across {topics}" \
     --skill research-log-manager \
     --session {session_filename}
   ```
5. Never permanently close a language — mark THIN and move on.
6. All source additions go through `db.py add-source` — no raw SQL.
