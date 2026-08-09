---
name: bibliography-compiler
description: >
  Generate formatted bibliography from the evidence_sources SQLite table. Produces
  full bibliography, per-slug bibliography, or per-item source lists. Replaces the
  old endnote compilation approach. ALWAYS use when asked to: compile bibliography,
  generate references, produce source list, export citations, audit source completeness.
  Trigger on: "bibliography", "compile references", "source list", "citation list",
  "reference list", "export sources".
---

**Model:** Sonnet-class
**SQLite:** `data/guidebook.db` via `scripts/db.py coverage --slug {slug}`

---

## Schema Reference

### evidence_sources columns

**Read the live schema before writing a query — do not trust a column list in
prose, including this one:**

```python
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
print([r[1] for r in con.execute("PRAGMA table_info(evidence_sources)")])
```

The list that stood here named four columns that **do not exist** — `authors`,
`year`, `title`, `doi_less_key` — and told you to "use `authors` and `tier`". Any  <!-- [RETIRED-VOCAB-OK] -->
query written from it failed. The names that matter for a bibliography:

| You want | The column is |
|---|---|
| author string | `author_display` (structured authors live in `evidence_source_authors`) |
| year | `pub_year` |
| title | `pub_title` (plus `pub_subtitle`, `chapter_title`, `book_title`) |
| journal | `journal_name`, `journal_abbrev` |
| locator | `volume`, `issue`, `pages_start`, `pages_end`, `article_number` |
| identifiers | `doi`, `pmid`, `pmcid`, `isbn`, `issn`, `handle`, `url` |

`tier` and `evidence_type` are as named and are **orthogonal** — a tier is not a
type. There is no `surname`, `journal` or `evidence_tier` column.

`doi_less_key` was a derived dedup key; it was dropped from the schema and has no  <!-- [RETIRED-VOCAB-OK] -->
successor column. Deduplicate by DOI first, then by any other stable identifier,
then by normalised title.

### source_slug_links columns
`ref_id, slug, local_ref_id`

### citation_mining columns
`slug, local_ref_id, backward, forward, connections_produced`

---

## 1. Full Bibliography

```sql
SELECT es.ref_id, es.author_display, es.pub_year, es.pub_title, es.doi, es.tier,
       es.evidence_type, es.jurisdiction, es.verification_status,
       GROUP_CONCAT(DISTINCT ssl.slug) as slugs,
       MAX(cm.backward) as cm_b, MAX(cm.forward) as cm_f
FROM evidence_sources es
LEFT JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
LEFT JOIN citation_mining cm ON cm.local_ref_id = ssl.local_ref_id AND cm.slug = ssl.slug
GROUP BY es.ref_id
ORDER BY es.first_author_last COLLATE NOCASE, es.pub_year
```

### Markdown output format
```markdown
# Bibliography — Guidebook for Accessible Design
**Generated:** {date}
**Total sources:** {N} | Tier 1: {N} Tier 2: {N} Tier 3: {N} ...

---

**{ref_id}** {authors} ({year}). {title}. {doi if available}
  Tier: {tier} | Type: {evidence_type} | Jurisdiction: {jurisdiction}
  Slugs: {slugs} | Mining: B={cm_b} F={cm_f}
```

---

## 2. Per-Slug Bibliography

```sql
SELECT es.ref_id, es.author_display, es.pub_year, es.pub_title, es.doi, es.tier
FROM evidence_sources es
JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
WHERE ssl.slug = '{slug}'
ORDER BY es.tier ASC, es.first_author_last COLLATE NOCASE
```

Use `python3 scripts/db.py coverage --slug {slug}` for coverage summary first.

---

## 3. Coverage Report

```sql
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN tier = 1 THEN 1 ELSE 0 END) as tier1,
  SUM(CASE WHEN tier = 2 THEN 1 ELSE 0 END) as tier2,
  SUM(CASE WHEN tier = 3 THEN 1 ELSE 0 END) as tier3,
  SUM(CASE WHEN doi IS NOT NULL AND doi != '' THEN 1 ELSE 0 END) as has_doi,
  -- Uppercase. SQLite `=` is case-sensitive and the column holds VERIFIED /
  -- UNVERIFIED (D-0157), so the lowercase form matched 0 of 863 rows and
  -- reported every source as unverified.
  SUM(CASE WHEN verification_status = 'VERIFIED' THEN 1 ELSE 0 END) as verified
FROM evidence_sources
```

---

## 4. Rules

1. Bibliography generated from SQLite — not from scanning markdown
2. Every source must have an evidence_sources record to appear
3. Sources without DOI are included but flagged
4. DOI verification is citation-verifier's job — not this skill
5. Output: markdown by default; BibTeX on request
