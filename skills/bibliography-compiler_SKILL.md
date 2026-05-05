---
name: bibliography-compiler
description: >
  Generate formatted bibliography from the evidence_sources SQLite table. Produces
  full bibliography, per-slug bibliography, per-population bibliography, or per-item
  source lists. Replaces the old endnote compilation approach (which assembled from
  per-item sources-cited tables in monolithic documents). ALWAYS use when asked to:
  compile bibliography, generate references, produce source list, export citations,
  check bibliography coverage, or audit source completeness. Trigger on: "bibliography",
  "compile references", "source list", "citation list", "reference list", "export sources".
---

**Model:** Sonnet 4.6
**SQLite:** `data/guidebook.db` via `scripts/db.py`

---

## 1. Full Bibliography

Query all evidence sources with their slug associations:

```sql
SELECT es.ref_id, es.surname, es.year, es.title, es.journal, es.doi,
       es.evidence_tier, es.language, es.jurisdiction,
       GROUP_CONCAT(DISTINCT ssl.slug) as slugs,
       cm.backward as cm_backward, cm.forward as cm_forward
FROM evidence_sources es
LEFT JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
LEFT JOIN citation_mining cm ON cm.local_ref_id = es.ref_id AND cm.slug = ssl.slug
GROUP BY es.ref_id
ORDER BY es.surname COLLATE NOCASE, es.year
```

### Output format (markdown)
```markdown
# Bibliography — Guidebook for Accessible Design
**Generated:** {date}
**Total sources:** {count}
**Tier distribution:** Tier 1: {n}, Tier 2: {n}, Tier 3: {n}, Tier 4: {n}, Tier 5: {n}, Tier 6: {n}, Co-1: {n}
**Citation mining:** {n} mined (B+F), {n} partial, {n} unmined

---

## A

**{ref_id}** {Surname}, {Initials} ({Year}). {Title}. *{Journal}*. {DOI if available}
- Tier: {N} | Language: {XX} | Jurisdiction: {JUR}
- Slugs: {slug-1}, {slug-2}
- Mining: B={✓/—} F={✓/—}

...
```

---

## 2. Per-Slug Bibliography

```sql
SELECT es.ref_id, es.surname, es.year, es.title, es.journal, es.doi,
       es.evidence_tier, es.language
FROM evidence_sources es
JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
WHERE ssl.slug = '{slug}'
ORDER BY es.evidence_tier ASC, es.surname COLLATE NOCASE
```

---

## 3. Per-Item Source List

For a specific Part 4 item code, find all sources via slug linkage:

```sql
SELECT DISTINCT es.ref_id, es.surname, es.year, es.title, es.evidence_tier
FROM evidence_sources es
JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
JOIN slugs s ON ssl.slug = s.slug
WHERE s.slug IN (
  SELECT bpc_source_slug FROM specification WHERE item_code = '{item_code}'
)
ORDER BY es.evidence_tier ASC, es.surname
```

---

## 4. Coverage Report

```sql
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN evidence_tier = 1 THEN 1 ELSE 0 END) as tier1,
  SUM(CASE WHEN evidence_tier = 2 THEN 1 ELSE 0 END) as tier2,
  SUM(CASE WHEN evidence_tier = 3 THEN 1 ELSE 0 END) as tier3,
  SUM(CASE WHEN doi IS NOT NULL AND doi != '' THEN 1 ELSE 0 END) as has_doi,
  SUM(CASE WHEN doi IS NULL OR doi = '' THEN 1 ELSE 0 END) as no_doi
FROM evidence_sources
```

---

## 5. Rules

1. Bibliography is generated from SQLite, not from scanning markdown files
2. Every source in the bibliography MUST have an evidence_sources record
3. Sources without DOI are flagged but included — DOI verification is citation-verifier's job
4. Co-1 sources are rendered with `[Co-1]` tag before the entry
5. Output is markdown by default; can produce BibTeX on request
6. Per-item source lists are used by item-specification-writer for the "Key Citations" section
