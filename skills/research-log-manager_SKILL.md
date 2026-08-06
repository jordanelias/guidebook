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

**Model:** Sonnet-class (mechanical) · Opus-class or above (if BPC synthesis judgment needed)
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

2. **Log every search you ran — one row per query, verbatim (R8):**
   ```bash
   python3 scripts/db.py log-search \
     --slug {slug} \
     --language {lang_code} \
     --jurisdiction {jur_code} \        # omit if the search was not jurisdiction-scoped
     --query-text '{the query, exactly as fired}' \
     --terms-used '["alias1","MeSH term","alias2"]' \   # JSON array — the column is json_valid-checked
     --engine {pubmed|crossref|web|...} \
     --depth-method {scoping|systematic} \             # only two; a citation chase is --mining-direction
     --target-tier {1..6} --target-evidence-type {co1|clinical|code|...} \
     --results-found {N} --results-screened {N} --results-admitted {N} \
     --admitted-ref-id REF-NNNNN \      # repeatable; writes the admission junction too
     --session {session_filename}
   ```
   Once per query. **Keep the empties** — a zero-yield search with a well-formed
   query is a completed unit of work and evidence about the world (R8, R14).
   Never delete one, never backfill one silently.

3. **A search you deliberately did NOT run is also a row:**
   ```bash
   python3 scripts/db.py log-search \
     --slug {slug} --language {lang_code} \
     --query-text 'n/a' --engine {engine} --depth-method scoping \
     --deferred-reason 'why — e.g. no controlled vocabulary for AR (0 aliases); \
                        a query would be back-translation, forbidden by R11' \
     --session {session_filename}
   ```
   `deferred_reason` is what makes **"not looked for"** different from
   **"nothing found"**. That distinction is the thing the whole pipeline exists
   to preserve; a missing row erases it.

   > **`upsert-coverage` and `upsert-language` are gone.** `search_coverage` and
   > `search_languages` were hand-kept grids that drifted from the search log in
   > both directions — 634 cells claimed SEARCHED against 15 with a matching
   > logged search, while 31 logged searches landed on cells the grid called
   > NOT-RUN. They are frozen as historical artifacts; coverage is now DERIVED
   > from the log via `v_coverage_jurisdiction` / `v_coverage_language`, so it
   > cannot claim more than was logged. Read it with
   > `python3 scripts/db.py coverage --slug {slug}`.

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

6. **Invoke citation-miner inline — MANDATORY for every confirmed Tier 1–2 source.** Failure to invoke is a protocol violation (GAP-283).

   For each new evidence_sources row with `tier IN (1, 2)`:

   > Tier 3 is **not** mandatory. This said "ALSO for Tier 3 unless explicitly
   > deferred", which `governance/research-contract.yaml` R2 corrected on
   > 2026-08-01: the operative RULE says "every confirmed Tier 1-2 source", and
   > the wider reading "had been obliging work on a tier band the rule ledger
   > does not require — a real cost silently imposed on every session." Mine T3
   > when it is worth mining, not because a skill said you must.

   a. Check mining status:
   ```bash
   python3 scripts/db.py is-mined --slug {slug} --ref {local_ref_id}
   ```

   b. If `mined: false`, invoke citation-miner skill (INLINE mode) with `(slug, local_ref_id, doi)`. Citation-miner will perform backward + forward mining per its own protocol and write a citation_mining row.

   c. If citation-miner cannot complete a direction (e.g., Scholar Gateway unavailable), it will write `deferred_reason` — that is acceptable. A citation_mining row MUST exist; only the direction may be deferred.

7. **Verify LOG completeness before session-close.** Run the audit script:
   ```bash
   python3 scripts/audit/citation_mining_completeness.py --session {session_filename}
   ```
   The script reports any Tier 1–2 source added in this session that lacks a citation_mining row. A nonzero count is a session-close blocker. To clear: either mine the source or write a citation_mining row with `deferred_reason` and the explicit DEFERRED-* marker.

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
     --category RP \
     --priority P3 \
     --description "{language} NO-DATA across {topics}" \
     --skill research-log-manager \
     --session {session_filename}
   ```
   *(Note: category is `RP` — `RES` was deprecated when the gaps schema CHECK constraint was tightened to RP/SW/CR/ST/MX/CD/EC/EG/CI/DEC/CONF/AUDT.)*
5. Never permanently close a language — mark THIN and move on.
6. All source additions go through `db.py add-source` — no raw SQL.
7. LOG completeness verification (step 7 above) is MANDATORY before session-close. Surfaces GAP-283-class protocol violations early.
