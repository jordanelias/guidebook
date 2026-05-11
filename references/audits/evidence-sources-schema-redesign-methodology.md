# evidence_sources Schema Redesign Methodology
**Authored:** 2026-05-11  
**Status:** PROPOSED — requires adoption decision before execution  
**Scope:** `data/guidebook.db` → `evidence_sources` table + new `evidence_source_authors` table  
**Estimated effort:** Phase 1 (schema + migration script) ~10h · Phase 2 (parse + human review) ~22h · Phase 3 (tooling update) ~6h

---

## 1. Diagnosis: what is currently conflated

### 1.1 The `title` field — 10 types of data in one cell

| Content type | Count | Example |
|---|---|---|
| BPC annotation (em-dash note) | 216 | `…Ear Hear — key RT60 reference` |
| DOI inline | 110 | `…Front Psychiatry. DOI:10.3389/fpsyt.2021.727353` |
| Journal abbrev + vol/issue/pages | 92 | `…Ear Hear 40(2):381–392` |
| GREY flag | 56 | `…[GREY — full citation from search log required]` |
| PMID inline | 53 | `…PMID:27885976` |
| BPC study design note | 31 | `…CAPABLE RCT — $2,825/participant` |
| URL inline | 8 | `…https://hdl.handle.net/…` |
| Book chapter info | 2 | `…In Willard and Spackman's OT` |
| Verification note | 1 | `[Unverified title — Stark S et al. 2017]` |
| Internal file path | 1 | `references/case-study-compendium.md v10.4` |

### 1.2 The `authors` field — no normalization, no structure

Current state: one text blob per source. Problems:
- "Steinfeld, E. et al." — only one author named; rest unknown
- "Kinnealey, M., Pfeiffer, B., Miller, J., Roan, C., Shoener, R." — five authors, no structured split
- "Habinteg / CAE / RIBA" — three corporate bodies, slash-separated
- "Baum, C. et al." — truncated; full author list unknown
- No author position, no ORCID, no separation of surname from given name

**Consequence:** cannot sort by author, cannot query first author for CrossRef, cannot generate APA for multi-author sources, cannot deduplicate by authorship.

### 1.3 The `year` field — 8 value types in an untyped TEXT column

`4-digit` (611), `n.d.` (55), `ongoing` (3), `2020/pub.2022` (2), `2023-2025` (1), `annual` (1), `2020/2024` (1), `April 2017` (1).

### 1.4 The `notes` and `evidence_type` fields

`notes`: verification session logs, journal+PMID spillover, ISBN, adversarial commentary — four unrelated things in one cell.

`evidence_type`: 17 values with at least 4 case variants of the same concept. 96% NULL.

### 1.5 Fields absent entirely

Journal name, volume, issue, pages, publisher, URL, access date, ISBN, ISSN, source type, chapter title, book title, edition, standard number, report number — all absent. APA generation is impossible without them.

---

## 2. Target schema

### 2.1 Design principles

1. **One fact per column.** No column may contain two semantically distinct pieces of information.
2. **Authors normalized into a separate table.** Each author is one row. Position, name parts, and corporate/individual distinction are separate columns. The parent table holds only denormalized fast-query fields derived from the author table.
3. **Bibliographic fields are separate from project annotation fields.**
4. **Typed where possible.** `pub_year` is INTEGER. Booleans are INTEGER 0/1. Enums use CHECK constraints.
5. **APA 7th edition generatable.** Given `source_type` + relevant columns, a correct APA citation can be produced programmatically for every source type.
6. **CrossRef-queryable.** `first_author_last`, `first_author_first`, `pub_title`, `pub_year` provide unambiguous structured inputs — no parsing required.

---

### 2.2 Table 1: `evidence_source_authors` (new — normalized author table)

One row per author per source. This is the source of truth for all authorship data.

```sql
CREATE TABLE evidence_source_authors (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id) ON DELETE CASCADE,
  position            INTEGER NOT NULL,  -- 1 = first author, 2 = second, etc.

  -- Individual author
  last_name           TEXT,   -- surname / family name
  first_name          TEXT,   -- given name(s) — "Edward", "E.", "E.T."
  suffix              TEXT,   -- "Jr.", "Sr.", "III"
  orcid               TEXT,   -- ORCID iD if known (0000-0000-0000-0000 format)

  -- Corporate/institutional author
  is_corporate        INTEGER NOT NULL DEFAULT 0 CHECK(is_corporate IN (0,1)),
  corporate_name      TEXT,   -- full org name when is_corporate = 1

  -- Role
  role                TEXT NOT NULL DEFAULT 'author'
                           CHECK(role IN ('author', 'editor', 'translator',
                                          'compiler', 'director')),

  -- Audit
  created_at          TEXT,
  created_by_session  TEXT,

  UNIQUE(ref_id, position, role)
);

CREATE INDEX idx_esa_ref_id   ON evidence_source_authors(ref_id);
CREATE INDEX idx_esa_last     ON evidence_source_authors(last_name);
CREATE INDEX idx_esa_corp     ON evidence_source_authors(corporate_name);
```

**Examples of what this replaces:**

| Current `authors` value | Becomes rows in `evidence_source_authors` |
|---|---|
| `Steinfeld, E. et al.` | position=1: last=Steinfeld, first=E., is_corporate=0. No further rows (et al. — author_count_is_complete=0) |
| `Kinnealey, M., Pfeiffer, B., Miller, J., Roan, C., Shoener, R.` | 5 rows, positions 1–5, all is_corporate=0 |
| `Habinteg / CAE / RIBA` | 3 rows: position=1 corporate_name=Habinteg, position=2 corporate_name=CAE, position=3 corporate_name=RIBA |
| `CDC` | 1 row: position=1, is_corporate=1, corporate_name=CDC |
| `NDTi / NHS England` | 2 rows: position=1 corporate_name=NDTi, position=2 corporate_name=NHS England |
| `(author TBC)` | 0 rows. author_count_is_complete=0 on parent. |

---

### 2.3 Table 2: `evidence_sources` (restructured)

```sql
CREATE TABLE evidence_sources (

  -- ── IDENTITY ──────────────────────────────────────────────
  ref_id                      TEXT PRIMARY KEY,

  -- ── SOURCE TYPE ───────────────────────────────────────────
  source_type                 TEXT CHECK(source_type IN (
                                'journal_article', 'book', 'book_chapter',
                                'report', 'standard', 'thesis',
                                'website', 'conference_paper', 'guideline',
                                'grey', 'case_study', 'dataset', 'internal'
                              )),

  -- ── AUTHOR SUMMARY (denormalized from evidence_source_authors) ──
  -- Source of truth is evidence_source_authors. These are derived/cached.
  -- Regenerated by scripts/refresh_author_denorm.py whenever authors table changes.
  author_count                INTEGER,   -- total named authors; NULL = unknown
  author_count_is_complete    INTEGER DEFAULT 0 CHECK(author_count_is_complete IN (0,1)),
  first_author_last           TEXT,      -- surname of position-1 author (for CrossRef, sort)
  first_author_first          TEXT,      -- given name of position-1 author (for CrossRef)
  is_corporate_primary        INTEGER DEFAULT 0 CHECK(is_corporate_primary IN (0,1)),
  author_display              TEXT,      -- APA-format full author string for citation rendering

  -- ── PUBLICATION DATE ──────────────────────────────────────
  pub_year                    INTEGER,             -- 4-digit integer, NULL if unknown
  pub_year_note               TEXT,               -- "n.d.", "in press", "ongoing"

  -- ── TITLE ─────────────────────────────────────────────────
  pub_title                   TEXT,   -- actual title; no annotations, no journal info
  pub_subtitle                TEXT,   -- subtitle after colon
  chapter_title               TEXT,   -- chapter title for book_chapter
  original_title              TEXT,   -- non-English original (if pub_title is translated)

  -- ── JOURNAL (source_type = journal_article) ───────────────
  journal_name                TEXT,   -- full journal name
  journal_abbrev              TEXT,   -- NLM/ISO abbreviation
  volume                      TEXT,
  issue                       TEXT,   -- "3", "Suppl.1", "Pt B"
  pages_start                 TEXT,   -- "381", "e69442"
  pages_end                   TEXT,   -- "392", NULL for e-articles
  article_number              TEXT,   -- online-first article number

  -- ── BOOK / CHAPTER / REPORT ───────────────────────────────
  publisher                   TEXT,
  publisher_location          TEXT,
  edition                     TEXT,   -- "2nd", "3", "revised"
  book_title                  TEXT,   -- parent book (for book_chapter)
  series                      TEXT,
  series_number               TEXT,
  report_number               TEXT,
  institution                 TEXT,   -- issuing body for reports/theses

  -- ── STANDARD ──────────────────────────────────────────────
  standard_number             TEXT,   -- "ISO 23599:2019", "DIN 32984:2011-10"

  -- ── IDENTIFIERS ───────────────────────────────────────────
  doi                         TEXT,
  pmid                        TEXT,
  pmcid                       TEXT,
  isbn                        TEXT,
  issn                        TEXT,
  url                         TEXT,
  url_accessed                TEXT,   -- YYYY-MM-DD
  handle                      TEXT,
  local_id                    TEXT,   -- Korea Science JAKO, J-STAGE, etc.

  -- ── EVIDENCE CLASSIFICATION ───────────────────────────────
  tier                        INTEGER CHECK(tier BETWEEN 1 AND 6),
  evidence_type               TEXT CHECK(evidence_type IN (
                                'rct', 'systematic_review', 'meta_analysis',
                                'scoping_review', 'narrative_review',
                                'cohort_study', 'cross_sectional',
                                'case_series', 'primary_research',
                                'biomechanics_study', 'exercise_physiology',
                                'clinical_guideline', 'international_standard',
                                'national_standard', 'government_report',
                                'industry_guidance', 'book', 'thesis',
                                'expert_opinion', 'grey'
                              )),
  jurisdiction                TEXT,
  co1_provenance              TEXT,
  co1_source_type             TEXT,
  synthesis_attribution_required INTEGER CHECK(synthesis_attribution_required IN (0,1)),

  -- ── METADATA QUALITY & VERIFICATION ──────────────────────
  metadata_quality            TEXT CHECK(metadata_quality IN (
                                'COMPLETE', 'PARTIAL', 'GREY',
                                'AUTHOR-TITLE-ONLY', 'PMID-ONLY'
                              )),
  verification_status         TEXT CHECK(verification_status IN (
                                'VERIFIED', 'UNVERIFIED-1', 'UNVERIFIED-CLOSED',
                                'CLOSED-DELETED', 'PROBABILISTIC'
                              )),
  doi_resolution_outcome      TEXT CHECK(doi_resolution_outcome IN (
                                'RESOLVED', 'NO-MATCH', 'REVERTED'
                              )),
  doi_less_key                TEXT,

  -- ── PROJECT ANNOTATIONS (separated from bibliographic) ────
  bpc_shorthand               TEXT,   -- BPC note formerly mixed into title
  bpc_note                    TEXT,
  grey_flag                   INTEGER DEFAULT 0 CHECK(grey_flag IN (0,1)),
  grey_reason                 TEXT,
  verification_note           TEXT,   -- [UNVERIFIED], [POSSIBLE-ERROR] formerly in title
  prior_expectation           TEXT,
  search_queries_used         TEXT,
  derivation_chain            TEXT,

  -- ── FREE-FORM NOTES ───────────────────────────────────────
  notes                       TEXT,

  -- ── AUDIT ─────────────────────────────────────────────────
  created_at                  TEXT,
  created_by_session          TEXT,
  updated_at                  TEXT,
  updated_by_session          TEXT
);
```

---

## 3. APA generation rules by source_type

All APA generated from structured fields — no string parsing at render time.

**journal_article**
```
{author_display} ({pub_year_display}). {pub_title}[: {pub_subtitle}]. {journal_name}, {volume}({issue}), {pages_start}[–{pages_end}][, Article {article_number}]. https://doi.org/{doi}
```

**book**
```
{author_display} ({pub_year_display}). {pub_title}[: {pub_subtitle}] [{edition} ed.]. {publisher}.
```

**book_chapter**
```
{author_display} ({pub_year_display}). {chapter_title}. In {editors_display} (Ed[s].), {book_title} (pp. {pages_start}–{pages_end}). {publisher}. [https://doi.org/{doi}]
```

**report**
```
{author_display} ({pub_year_display}). {pub_title} [{report_number}]. {institution}. {url}
```

**standard**
```
{corporate_name of position-1 author}. ({pub_year_display}). {standard_number}: {pub_title}. {publisher}.
```

**`author_display` generation (from evidence_source_authors):**
- ≤2 authors: `Last, F., & Last, F.`
- 3–20 authors: `Last, F., Last, F., … & Last, F.` (APA 7: all authors up to 20)
- >20 authors: `Last, F., Last, F., [first 19] … Last, F.` (ellipsis + final author)
- 1 corporate: `Corporate Name`
- Multiple corporates: `Name1 & Name2` / `Name1, Name2, & Name3`

---

## 4. Field-by-field migration rules

### 4.1 `authors` → `evidence_source_authors` rows

Parse pipeline:
1. If contains `(author TBC)`, `(internal)`, `(E\d+`: zero rows, `author_count_is_complete = 0`
2. Split on ` et al.` — if found, flag `author_count_is_complete = 0`, parse only named portion
3. Split on ` & ` or `; ` or `, ` (with care for "Last, F." patterns)
4. For each token: if matches `^[A-ZÀ-Ö][a-z]+(,\s*[A-Z\.]+)?$` → individual; else → corporate
5. Parse individual: `last_name` = before comma, `first_name` = after comma
6. Assign `position` = 1, 2, 3…

**Known ambiguous cases requiring human review:**
- `Kinnealey, M., Pfeiffer, B., Miller, J., Roan, C., Shoener, R.` — comma-separated last+initial pairs, parser must not split at commas within a name
- `Finitzo-Hieber, T. & Tillman, T.W.` — hyphenated surnames
- Non-Latin authors (`한국시각장애인연합회`, `筑波大学`) — corporate=1, full string as corporate_name
- `Levine D et al.` — no comma after surname; `last=Levine`, `first=D`

### 4.2 `title` → structured fields

Strip in order, recording each extraction:
1. `verification_note` ← `r'\[(UNVERIFIED|POSSIBLE.ERROR|GAP:|Unverified)[^\]]*\]'`
2. `grey_flag`, `grey_reason` ← `r'\[GREY[^—]*—([^\]]+)\]'`
3. DOI ← `r'(?:DOI[:\s]+|doi\.org/)(10\.\S+?)[\s\.\]]'` → validate, write to `doi`
4. PMID ← `r'PMID[:\s]+(\d+)'` → write to `pmid`
5. Journal citation block ← `r'\.?\s*([A-Z][A-Za-z &]+)\s+(\d+)\(([^)]+)\)[:\s]+([\d–\-]+)'`
   → `journal_abbrev`, `volume`, `issue`, `pages_start/end`
6. Book chapter ← `r'\bIn\b.*(?:Ed[s]?\.|Eds\.|\(Ed)'` → `book_title`, parse editor into author rows with `role='editor'`
7. URL ← `r'https?://\S+'` → `url`
8. BPC annotation ← leading `[BPC shorthand] —` pattern before main title
9. `pub_title` ← what remains after all above are stripped; trim trailing punctuation

### 4.3 `year` → `pub_year` + `pub_year_note`

| Input | pub_year | pub_year_note |
|---|---|---|
| `2024` | 2024 | NULL |
| `n.d.` / `n.d` | NULL | `n.d.` |
| `ongoing` | NULL | `ongoing` |
| `2020/pub.2022` | 2022 | `2020/pub.2022` |
| `April 2017` | 2017 | `April 2017` |
| `2023-2025` | 2023 | `2023-2025` |
| `annual` | NULL | `annual` |

### 4.4 `source_type` inference

| Condition | source_type |
|---|---|
| `standard_number` extractable OR tier ≥ 4 AND title matches ISO/DIN/BS/EN/ANSI pattern | `standard` |
| title contains `In [Name] (Ed` or `In Willard` | `book_chapter` |
| `journal_abbrev` extractable | `journal_article` |
| title/notes contains `thesis`, `dissertation` | `thesis` |
| `grey_flag = 1` | `grey` |
| `authors = '(internal)'` | `internal` |
| `url` present, no journal/publisher | `website` |
| unresolved | `report` + flag for human review |

### 4.5 `evidence_type` normalization

| Current variants | Normalized value |
|---|---|
| `SYSTEMATIC_REVIEW`, `systematic_review`, `systematic_review_meta_analysis` | `systematic_review` or `meta_analysis` (check title) |
| `CLINICAL_STUDY`, `primary-research`, `primary_study` | `primary_research` |
| `INTERNATIONAL_STANDARD` | `international_standard` |
| `BIOMECHANICS_STUDY` | `biomechanics_study` |
| `EXERCISE_PHYSIOLOGY_STUDY` | `exercise_physiology` |
| `GOVERNMENT_REPORT` | `government_report` |
| `INDUSTRY_GUIDANCE` | `industry_guidance` |

---

## 5. `metadata_quality = COMPLETE` definition (revised)

After migration, COMPLETE requires all of:
- `pub_title` populated
- `pub_year` OR `pub_year_note` populated
- `source_type` populated
- At least one identifier: `doi` OR `url` OR `handle` OR `local_id` OR `isbn`
- At least one of: `journal_name` (articles), `publisher` (books/reports), `standard_number` (standards), `institution` (reports)
- `author_count_is_complete = 1` OR `is_corporate_primary = 1` with `corporate_name` set

---

## 6. Downstream changes

| Component | Change |
|---|---|
| `scripts/resolve_dois.py` | Query `first_author_last`, `first_author_first`, `pub_title`, `pub_year` — no parsing needed |
| `scripts/generate_apa.py` (new) | APA formatter by source_type; joins `evidence_source_authors` |
| `scripts/refresh_author_denorm.py` (new) | Regenerates `first_author_last`, `first_author_first`, `author_display`, `is_corporate_primary` from author table |
| `scripts/validate_bpc.py` | Update column references |
| Bootstrap status block | Add `source_type` coverage; revise COMPLETE definition |
| All audit scripts | Update column names |
| `source_slug_links` | `ref_id` FK unchanged |
| `citation_mining` | `global_ref_id` unchanged |
| `evidence_population_match` | `ref_id` unchanged |

---

## 7. Execution plan

**Phase 1 — Schema + migration script (~10h)**
1. `scripts/migrate_evidence_sources_v2.py` — creates new tables, migrates 675 rows, outputs review CSV with confidence scores and flagged ambiguous parses
2. `scripts/generate_apa.py` — APA formatter, test against all rows
3. `scripts/refresh_author_denorm.py` — denorm updater
4. Updated `scripts/resolve_dois.py`

**Phase 2 — Human review (~22h)**
1. Review flagged ambiguous rows (~100 title parses, ~60 author parses)
2. Manual entry for non-Latin titles/authors (~40 rows)
3. Spot-check APA output for 50 rows across all source types
4. Resolve `author_count_is_complete = 0` entries where full author list is needed for APA

**Phase 3 — Cutover (~6h)**
```sql
ALTER TABLE evidence_sources RENAME TO evidence_sources_v1_legacy;
-- run migration → creates evidence_sources + evidence_source_authors
```
Update all downstream scripts. Commit with `data_migrations` entry.

---

## 8. What this unblocks

| Blocker | Resolution |
|---|---|
| CrossRef false positives | Queries `first_author_last + pub_title + pub_year` — exact structured inputs |
| APA generation impossible | Fully automated for all source types via `generate_apa.py` |
| 518 AUTHOR-TITLE-ONLY rows | ~280 resolvable to COMPLETE by extracting structured fields from existing title strings |
| `evidence_type` 96% null | Inferred from `source_type` + tier; enum enforced |
| Author deduplication | Exact match on `last_name + first_name + pub_year` |
| et al. truncation | `author_count_is_complete` flag — system knows what it doesn't know |
| Multi-corporate authorship | Each org is its own row with `position` ordering |
| Phase B.7 verification scope | `source_type = standard` rows auto-classified; reduces manual scope by ~80 rows |
