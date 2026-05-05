# SQLite Migration Design — Guidebook Data Layer

**Date:** 2026-05-05  
**Version:** 3 (full rewrite — all review concerns addressed)  
**Status:** FOR IMPLEMENTATION

---

## 1. Problem

Every session loads markdown registers into context: connection index (~4K tokens), gap register (fetched whole for grepping), slug registry, search coverage. These files grow monotonically, require threshold management, and consume context budget that should go to work. Updates require GET full file → parse → modify → PUT — fragile and SHA-stale-prone.

The deeper problem: the guidebook is a relational data problem stored in a document format. The same specification (grab bar height for G-03) exists in the BPC file, Part 4 prose, Part 6 room matrix, Part 7 matrix, website spec page YAML, and generated HTML. When evidence changes, five files need updating. Inconsistency is the expected failure mode, not the exception.

---

## 2. Architecture Decision

**SQLite as the canonical store for all structured data. Everything else is a derived view.**

This is not a register migration. It is Phase 1 of a full structured-data migration across three phases:

| Phase | Scope | Delivers |
|---|---|---|
| **1 — Registers + logs** | Connections, gaps, slugs, evidence sources, citation mining, search coverage, decisions, terminology | Session-start token savings; citation mining tracking; synonym-expanded search |
| **2 — Entity data** | Items, measurements, room-item joins, population-item joins, specification values, conflict domains | Single source of truth for all specifications; room matrices become queries |
| **3 — Derived views** | Spec pages, room pages, population pages, Part 6/7 matrices, Part 4 prose injection | Multivariate presentation becomes a rendering problem, not a file-assembly problem |

Phase 1 is implemented here. Phase 2/3 are mapped in §12 so Phase 1 schema doesn't foreclose them.

---

## 3. What Migrates vs. What Stays

### → SQLite (Phase 1)

| Table(s) | Current source | Session-start savings |
|---|---|---|
| `connections`, `connection_targets` | `connections/_index.md` + per-topic files | ~4K → ~200 tokens |
| `gaps` | `gap_register.md` | ~2K → ~100 tokens |
| `slugs` | `slug-registry.md` | ~1.5K → 0 (query on demand) |
| `bpc_metadata` | BPC front-matter (scattered) | Enables completeness queries |
| `evidence_sources`, `source_slug_links` | Per-BPC REF-ID tables | Cross-slug dedup; citation mining FK |
| `citation_mining` | NEW | Born in SQLite |
| `search_coverage`, `search_languages` | Per-slug search-log metadata | Pre-LOG completeness check becomes SQL |
| `decisions` | `decision_register.yaml` | ~1K → 0 (query on demand) |
| `terms`, `term_aliases`, `term_item_links` | NEW | Synonym expansion for mining + connections |
| `db_meta` | NEW | Schema versioning via `PRAGMA user_version` |

**Total session-start savings: ~7–8K tokens → ~300 tokens.**

### → Stays as Markdown/YAML (Phase 1)

| File | Reason |
|---|---|
| `project-standards.md` | Rules prose — git diff matters |
| `sessions/session_*.md` | Narrative YAML — read linearly |
| Governance documents | Versioned prose with reasoning |
| BPC files | Research narrative — only metadata migrates |
| Per-topic connection files | **Archived** once description text migrates to `connections.description` |
| Skill files | Guidance documents |
| `schemas/` | Python code |
| `data/adversarial_use/catalog.yaml` | Small, infrequent — YAML+Pydantic adequate |
| `data/temporal/` | Complex supersedence graph — adequate for now |

### Resolved Design Questions

**Per-topic connection files:** Description text migrates to `connections.description`. Per-topic markdown files are archived — header added, updates stop, git history preserved.

**Evidence source dedup:** Application-layer dedup, not a UNIQUE constraint. Dedup key = `lower(surname + year + first_5_title_words)` for DOI-less sources. Migration script reports all collision candidates before inserting; user adjudicates. No DB-level UNIQUE on derived keys — see §8 Issue 5.

**Search log narrative:** Only status metadata (coverage per jurisdiction/language, attempt flags) migrates. Narrative search strategy text stays in per-slug markdown search-log files.

---

## 4. Schema

### 4.0 Audit Columns — Every Table, No Exceptions

```sql
created_at          TEXT NOT NULL    -- YYYY-MM-DD HH:MM UTC
created_by_session  TEXT NOT NULL    -- session filename
updated_at          TEXT NOT NULL    -- YYYY-MM-DD HH:MM UTC
updated_by_session  TEXT NOT NULL    -- session filename
```

### 4.1 db_meta — Schema Versioning

```sql
CREATE TABLE db_meta (
    key     TEXT PRIMARY KEY,
    value   TEXT NOT NULL
);

-- Seed on init:
INSERT INTO db_meta VALUES ('schema_version', '1');
INSERT INTO db_meta VALUES ('created_at', '2026-05-05 00:00');
INSERT INTO db_meta VALUES ('project', 'jordanelias/guidebook');
```

Schema version also tracked via `PRAGMA user_version = 1` — SQLite's native mechanism, atomic, requires no table read. Migration runner checks `PRAGMA user_version` first; `db_meta.schema_version` is human-readable backup.

### 4.2 connections + connection_targets

```sql
CREATE TABLE connections (
    con_id              TEXT PRIMARY KEY,
                        -- CON-NNNN (4-digit zero-padded)
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'
                        )),
    confidence          TEXT NOT NULL
                        CHECK(confidence IN ('HIGH','MODERATE','SPECULATIVE')),
    connection_type     TEXT
                        CHECK(connection_type IN (
                            'CROSS-POPULATION','CROSS-ITEM',
                            'COMPOUND-INTERACTION','METHODOLOGY'
                        )),
    filed_in            TEXT NOT NULL,
    description         TEXT,            -- migrated from per-topic files
    source_skill        TEXT,
    opus_reviewed       INTEGER NOT NULL DEFAULT 0 CHECK(opus_reviewed IN (0,1)),
    session_applied     TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

-- Junction table: one connection → many item/section targets
CREATE TABLE connection_targets (
    con_id              TEXT NOT NULL REFERENCES connections(con_id),
    target              TEXT NOT NULL,   -- item code or section ref
    PRIMARY KEY (con_id, target)
);

CREATE INDEX idx_conn_status     ON connections(status);
CREATE INDEX idx_conn_confidence ON connections(confidence);
CREATE INDEX idx_conn_filed_in   ON connections(filed_in);
CREATE INDEX idx_ct_target       ON connection_targets(target);
```

**Session-start query (PENDING connections — summary only):**
```sql
SELECT c.con_id, c.confidence,
       GROUP_CONCAT(ct.target, ', ') AS targets
FROM connections c
JOIN connection_targets ct USING (con_id)
WHERE c.status = 'PENDING'
GROUP BY c.con_id
ORDER BY c.confidence DESC
```

### 4.3 gaps

```sql
CREATE TABLE gaps (
    gap_id              TEXT PRIMARY KEY,
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'RP','SW','CR','ST','MX','CD','EC','EG'
                        )),
    priority            TEXT NOT NULL CHECK(priority IN ('P1','P2','P3')),
    status              TEXT NOT NULL
                        CHECK(status LIKE 'OPEN%' OR status LIKE 'CLOSED%'),
    skill               TEXT,
    section             TEXT,
    description         TEXT NOT NULL,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE INDEX idx_gap_priority_status ON gaps(priority, status);
```

**Session-start query:**
```sql
SELECT gap_id, section, description
FROM gaps
WHERE priority = 'P1' AND status LIKE 'OPEN%'
ORDER BY gap_id
```

### 4.4 slugs + bpc_metadata

```sql
CREATE TABLE slugs (
    slug                TEXT PRIMARY KEY,
    topic_directory     TEXT NOT NULL,
    sl_path             TEXT NOT NULL,
    bpc_path            TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN (
                            'ACTIVE','MERGED','STUB','PROVISIONAL'
                        )),
    merged_into         TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE TABLE bpc_metadata (
    slug                    TEXT PRIMARY KEY REFERENCES slugs(slug),
    population              TEXT NOT NULL,
    last_updated            TEXT,
    jurisdictions_searched  INTEGER DEFAULT 0,
    co1_pass_count          INTEGER DEFAULT 0,
    evidence_state          TEXT,
    pico_complete           INTEGER NOT NULL DEFAULT 0 CHECK(pico_complete IN (0,1)),
    search_complete         INTEGER NOT NULL DEFAULT 0 CHECK(search_complete IN (0,1)),
    bpc_complete            INTEGER NOT NULL DEFAULT 0 CHECK(bpc_complete IN (0,1)),
    citation_mining_complete INTEGER NOT NULL DEFAULT 0
                            CHECK(citation_mining_complete IN (0,1)),
    -- audit
    created_at              TEXT NOT NULL,
    created_by_session      TEXT NOT NULL,
    updated_at              TEXT NOT NULL,
    updated_by_session      TEXT NOT NULL
);
```

### 4.5 evidence_sources + source_slug_links

```sql
CREATE TABLE evidence_sources (
    ref_id              TEXT PRIMARY KEY,   -- REF-NNNNN or Co1-NN
    authors             TEXT NOT NULL,
    year                TEXT,
    title               TEXT NOT NULL,
    doi                 TEXT,              -- NOT UNIQUE at DB level; dedup is app-layer
    doi_less_key        TEXT,              -- derived dedup key for DOI-less sources
                                           -- NOT UNIQUE — collisions logged, not rejected
    pmid                TEXT,
    tier                INTEGER CHECK(tier IS NULL OR tier BETWEEN 1 AND 6),
    evidence_type       TEXT,
    jurisdiction        TEXT,
    metadata_quality    TEXT
                        CHECK(metadata_quality IN (
                            'COMPLETE','PMID-ONLY','GREY','AUTHOR-TITLE-ONLY'
                        )),
    verification_status TEXT,
    co1_provenance      TEXT,
    co1_source_type     TEXT,
    synthesis_attribution_required INTEGER CHECK(
        synthesis_attribution_required IN (0,1)
    ),
    notes               TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE TABLE source_slug_links (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (ref_id, slug)
);

CREATE INDEX idx_es_doi      ON evidence_sources(doi);
CREATE INDEX idx_es_tier     ON evidence_sources(tier);
CREATE INDEX idx_ssl_slug    ON source_slug_links(slug);
CREATE INDEX idx_ssl_ref     ON source_slug_links(ref_id);
```

**Why no UNIQUE on doi / doi_less_key:** A DB-level UNIQUE either silently rejects a legitimate new source or fails noisily without context. Application-layer dedup surfaces collision candidates to the user with enough context to adjudicate. `doi_less_key` is an index aid and reporting tool, not an integrity constraint.

### 4.6 citation_mining

```sql
CREATE TABLE citation_mining (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    global_ref_id       TEXT REFERENCES evidence_sources(ref_id),
    doi                 TEXT,
    backward            INTEGER NOT NULL DEFAULT 0 CHECK(backward IN (0,1)),
    forward             INTEGER NOT NULL DEFAULT 0 CHECK(forward IN (0,1)),
    connections_produced TEXT NOT NULL DEFAULT '[]',
                        -- JSON array of CON-IDs: ["CON-0241","CON-0242"]
                        -- Array not range string — IDs may be non-contiguous
    notes               TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (slug, local_ref_id)
);

CREATE INDEX idx_cm_unmined ON citation_mining(slug, backward, forward);
```

### 4.7 search_coverage + search_languages

```sql
CREATE TABLE search_coverage (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    jurisdiction        TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN ('SEARCHED','THIN','NO-DATA','NOT-RUN')),
    co1_attempted       INTEGER NOT NULL DEFAULT 0 CHECK(co1_attempted IN (0,1)),
    tier5_attempted     INTEGER NOT NULL DEFAULT 0 CHECK(tier5_attempted IN (0,1)),
    tier6_attempted     INTEGER NOT NULL DEFAULT 0 CHECK(tier6_attempted IN (0,1)),
    notes               TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (slug, jurisdiction)
);

CREATE TABLE search_languages (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    language            TEXT NOT NULL,
    status              TEXT NOT NULL
                        CHECK(status IN ('SEARCHED','PARTIAL','NOT-RUN')),
    results_count       INTEGER NOT NULL DEFAULT 0,
    notes               TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (slug, language)
);
```

**Pre-LOG completeness check:**
```sql
SELECT COUNT(*) FROM search_coverage WHERE slug=? AND status != 'NOT-RUN';
-- Must equal 24

SELECT COUNT(*) FROM search_languages WHERE slug=? AND status != 'NOT-RUN';
-- Must equal 14
```

### 4.8 decisions

```sql
CREATE TABLE decisions (
    decision_id         TEXT PRIMARY KEY,   -- D-NNNN
    category            TEXT NOT NULL
                        CHECK(category IN (
                            'D-DOCT','D-METH','D-SCHEMA','D-OP','D-PRES'
                        )),
    delegation          TEXT NOT NULL
                        CHECK(delegation IN ('DG-NON','DG-REVIEW','DG-AUTO')),
    delegation_rationale TEXT,
    summary             TEXT NOT NULL,
    outcome             TEXT NOT NULL,
    rationale           TEXT NOT NULL,
    decision_date       TEXT NOT NULL,
    decided_by          TEXT NOT NULL,
    model_routing       TEXT NOT NULL,
    effort_level        INTEGER NOT NULL,
    status              TEXT NOT NULL DEFAULT 'ACTIVE'
                        CHECK(status IN (
                            'ACTIVE','SUPERSEDED','WITHDRAWN','PROPOSED'
                        )),
    review_status       TEXT NOT NULL,
    -- JSON arrays (SQLite has no native array type; TEXT+JSON is the standard pattern)
    supersedes          TEXT NOT NULL DEFAULT '[]',
    predecessors        TEXT NOT NULL DEFAULT '[]',
    decision_artifacts  TEXT NOT NULL DEFAULT '[]',
    alternatives_considered TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE INDEX idx_decision_status   ON decisions(status);
CREATE INDEX idx_decision_category ON decisions(category);
```

JSON arrays in TEXT columns is the accepted SQLite pattern for 1-to-many relationships that don't warrant a junction table. SQLite's `json_each()` enables querying: `SELECT * FROM decisions, json_each(supersedes) WHERE json_each.value = 'D-0050'`.

### 4.9 terms + term_aliases + term_item_links

This table set serves synonym expansion for citation mining and semantic connection discovery. The project uses domain-specific terminology that varies across jurisdictions, disciplines, and languages. "Grab bar" = "support rail" = "handrail" = "助力バー" = "barre d'appui". Without synonym expansion, citation mining misses sources that use different but equivalent terms. Without a controlled vocabulary, connection-scout pattern matching is purely lexical and misses conceptually related items.

```sql
CREATE TABLE terms (
    term_id             TEXT PRIMARY KEY,   -- TERM-NNNN
    canonical_en        TEXT NOT NULL,      -- preferred English term
    definition          TEXT,               -- brief scope note (what this term covers)
    domain              TEXT,               -- 'architectural','clinical','legal','colloquial'
    scope_note          TEXT,               -- use/don't-use guidance
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL
);

CREATE TABLE term_aliases (
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    alias               TEXT NOT NULL,
    language            TEXT NOT NULL DEFAULT 'EN',
                        -- ISO 639-1: EN, FR, DE, JA, ZH, PT, AR, KO, ES, NL, SV, FI, HI, SW
    alias_type          TEXT NOT NULL
                        CHECK(alias_type IN (
                            'SYNONYM',      -- same concept, same language
                            'TRANSLATION',  -- same concept, different language
                            'NARROWER',     -- more specific (e.g. "fold-down grab bar" < "grab bar")
                            'BROADER',      -- more general
                            'DEPRECATED',   -- old term, no longer preferred
                            'DOMAIN'        -- domain-specific variant
                        )),
    jurisdiction        TEXT,               -- if usage is jurisdiction-specific
    notes               TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (term_id, alias, language)
);

-- Many-to-many: terms ↔ items (one term applies to multiple items; one item has many terms)
CREATE TABLE term_item_links (
    term_id             TEXT NOT NULL REFERENCES terms(term_id),
    item_code           TEXT NOT NULL,      -- e.g. G-03, A-16
                                            -- FK to items table in Phase 2; unconstrained in Phase 1
    population          TEXT,               -- if term is population-specific for this item
    notes               TEXT,
    -- audit
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (term_id, item_code)
);

CREATE INDEX idx_ta_alias    ON term_aliases(alias);
CREATE INDEX idx_ta_language ON term_aliases(language);
CREATE INDEX idx_til_item    ON term_item_links(item_code);
```

**How this is used:**

*Citation mining expansion:* Before running a mining pass on a source, retrieve all aliases for the item's canonical terms. Search using the expanded set. A paper titled "Support rails in aged care bathrooms" matches G-03 (grab bar) via the SYNONYM alias "support rail".

*Multilingual research:* `SELECT alias FROM term_aliases WHERE term_id IN (SELECT term_id FROM term_item_links WHERE item_code = 'G-03') AND language = 'JA'` returns the Japanese search terms automatically.

*Vectorized connection discovery:* The synonym-expanded text of each item's terms can be embedded (sentence-transformers or similar) to produce a dense vector. Cosine similarity over these vectors surfaces conceptually related items that don't share exact keywords — a grab bar specification and a seating transfer specification may not share the word "grab bar" but share "transfer support", "upper limb loading", "functional reach". This is Phase 2 work; Phase 1 builds the vocabulary.

*Pattern matching in connection-scout:* The `terms` + `term_aliases` tables provide the vocabulary for semantic overlap detection without requiring embedding infrastructure. A connection between G-03 and I-03 is suggested when both items share term_ids for "transfer" and "upper limb support" — detectable by a JOIN query without any ML.

---

## 5. Python Interface — `scripts/db.py`

### 5.0 Design Principles

**CLI-first:** Invoked as `python3 scripts/db.py <command> [args]` from bash_tool. No import-path setup. All output is JSON on stdout. Errors exit non-zero with message on stderr.

**Environment-configured path:** `DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))`. Overridable in tests without touching production file. 12-factor principle #3.

**No dict mutation:** All helpers use `{**data, **audit(session)}` — never `data.update(...)`.

**Whitelist validation for identifiers:** Column names used in f-strings (upsert helpers) are validated against a declared frozenset before any SQL is constructed. Values always use parameterized queries.

**Context-managed connections:** Every connection is opened and closed in a `with connect() as conn:` block with automatic commit/rollback.

**Dry-run support:** All write commands accept `--dry-run` flag. Dry-run executes logic up to but not including `conn.commit()`, prints the SQL and parameters that would execute, exits 0 if no errors.

**Repository pattern separation:** The module has three clearly labelled sections:
- `# --- Storage layer (CRUD) ---`: `insert_*`, `update_*`, `get_by_id`, `delete_*` — no business logic
- `# --- Domain queries ---`: `get_open_gaps`, `get_unmined_sources`, `get_coverage_completeness` — business logic over stored data
- `# --- CLI ---`: `__main__` block with argparse subcommands

### 5.1 Module skeleton

```python
"""
scripts/db.py — SQLite interface for guidebook data layer.

Environment:
    GUIDEBOOK_DB_PATH   Path to database file (default: data/guidebook.db)

CLI usage:
    python3 scripts/db.py init
    python3 scripts/db.py migrate              # apply pending migrations
    python3 scripts/db.py gaps [--priority P1] [--status OPEN]
    python3 scripts/db.py connections [--status PENDING] [--confidence HIGH] [--summary]
    python3 scripts/db.py is-mined --slug SLUG --ref REF-ID
    python3 scripts/db.py log-mining --slug S --ref R --direction backward
                          --connections '["CON-0241"]' --session SESSION
                          [--dry-run]
    python3 scripts/db.py next-id connections|gaps|terms
    python3 scripts/db.py coverage --slug SLUG
    python3 scripts/db.py synonyms --item A-16 [--language JA]
    python3 scripts/db.py validate             # runs validate_db checks inline
    python3 scripts/db.py --help               # full command reference
"""

import json
import os
import sqlite3
import sys
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

# Column whitelists — validated before any f-string SQL construction
_COVERAGE_COLS = frozenset({
    "status","co1_attempted","tier5_attempted","tier6_attempted","notes"
})
_LANGUAGE_COLS = frozenset({"status","results_count","notes"})
_BPC_META_COLS = frozenset({
    "population","last_updated","jurisdictions_searched","co1_pass_count",
    "evidence_state","pico_complete","search_complete","bpc_complete",
    "citation_mining_complete"
})

@contextmanager
def connect(dry_run: bool = False):
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        if not dry_run:
            conn.commit()
        else:
            conn.rollback()   # dry-run: roll back all writes
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

def audit(session: str) -> dict:
    ts = now()
    return {
        "created_at": ts, "created_by_session": session,
        "updated_at": ts, "updated_by_session": session,
    }

def _upd(session: str) -> dict:
    return {"updated_at": now(), "updated_by_session": session}

def _validate_cols(data_keys, whitelist: frozenset, context: str):
    unknown = set(data_keys) - whitelist
    if unknown:
        raise ValueError(
            f"{context}: unknown column(s) {unknown}. "
            f"Permitted: {whitelist}"
        )
```

### 5.2 Storage layer — Connections

```python
# --- Storage layer ---

def next_con_id() -> str:
    with connect() as conn:
        row = conn.execute(
            "SELECT con_id FROM connections ORDER BY con_id DESC LIMIT 1"
        ).fetchone()
    if not row:
        return "CON-0001"
    return f"CON-{int(row['con_id'].split('-')[1]) + 1:04d}"

def insert_connection(data: dict, targets: list[str],
                      session: str, dry_run: bool = False) -> str:
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph   = ", ".join(["?"] * len(row))
        conn.execute(
            f"INSERT INTO connections ({cols}) VALUES ({ph})",
            list(row.values())
        )
        conn.executemany(
            "INSERT OR IGNORE INTO connection_targets (con_id, target) VALUES (?,?)",
            [(data["con_id"], t) for t in targets]
        )
    return data["con_id"]

def update_connection_status(con_id: str, status: str,
                             session: str, dry_run: bool = False):
    u = _upd(session)
    with connect(dry_run) as conn:
        conn.execute(
            "UPDATE connections SET status=?, session_applied=?, "
            "updated_at=?, updated_by_session=? WHERE con_id=?",
            [status, session, u["updated_at"], u["updated_by_session"], con_id]
        )
```

### 5.3 Storage layer — Gaps

```python
def next_gap_id() -> str:
    with connect() as conn:
        row = conn.execute(
            "SELECT gap_id FROM gaps "
            "WHERE gap_id GLOB 'GAP-[0-9]*' "
            "ORDER BY CAST(SUBSTR(gap_id,5) AS INTEGER) DESC LIMIT 1"
        ).fetchone()
    if not row:
        return "GAP-001"
    return f"GAP-{int(row['gap_id'].split('-')[1]) + 1:03d}"

def insert_gap(data: dict, session: str, dry_run: bool = False) -> str:
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph   = ", ".join(["?"] * len(row))
        conn.execute(f"INSERT INTO gaps ({cols}) VALUES ({ph})", list(row.values()))
    return data["gap_id"]

def close_gap(gap_id: str, status: str,
              session: str, dry_run: bool = False):
    if not status.startswith("CLOSED"):
        raise ValueError(f"status must start with CLOSED, got '{status}'")
    u = _upd(session)
    with connect(dry_run) as conn:
        conn.execute(
            "UPDATE gaps SET status=?, updated_at=?, updated_by_session=? "
            "WHERE gap_id=?",
            [status, u["updated_at"], u["updated_by_session"], gap_id]
        )

def update_gap_priority(gap_id: str, priority: str,
                        session: str, dry_run: bool = False):
    if priority not in ("P1","P2","P3"):
        raise ValueError(f"Invalid priority: {priority}")
    u = _upd(session)
    with connect(dry_run) as conn:
        conn.execute(
            "UPDATE gaps SET priority=?, updated_at=?, updated_by_session=? "
            "WHERE gap_id=?",
            [priority, u["updated_at"], u["updated_by_session"], gap_id]
        )
```

### 5.4 Storage layer — Citation Mining

```python
_VALID_DIRECTIONS = frozenset({"backward", "forward"})

def is_mined(slug: str, ref_id: str) -> dict | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT backward, forward, connections_produced "
            "FROM citation_mining WHERE slug=? AND local_ref_id=?",
            [slug, ref_id]
        ).fetchone()
    return dict(row) if row else None

def log_mining(slug: str, ref_id: str, direction: str,
               connections: list[str], session: str,
               doi: str = None, dry_run: bool = False):
    if direction not in _VALID_DIRECTIONS:
        raise ValueError(
            f"direction must be 'backward' or 'forward', got '{direction}'"
        )
    # Column name is now safe: validated against explicit set, not user input
    dir_col = direction   # 'backward' or 'forward' — both valid column names
    ts = now()

    with connect(dry_run) as conn:
        row = conn.execute(
            "SELECT backward, forward, connections_produced "
            "FROM citation_mining WHERE slug=? AND local_ref_id=?",
            [slug, ref_id]
        ).fetchone()
        if row:
            prior   = json.loads(row["connections_produced"] or "[]")
            merged  = json.dumps(list(dict.fromkeys(prior + connections)))
            # dir_col validated above — safe to interpolate
            conn.execute(
                f"UPDATE citation_mining SET {dir_col}=1, "
                "connections_produced=?, updated_at=?, updated_by_session=? "
                "WHERE slug=? AND local_ref_id=?",
                [merged, ts, session, slug, ref_id]
            )
        else:
            conn.execute(
                "INSERT INTO citation_mining "
                "(slug,local_ref_id,doi,backward,forward,"
                " connections_produced,created_at,created_by_session,"
                " updated_at,updated_by_session) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                [slug, ref_id, doi,
                 1 if direction == "backward" else 0,
                 1 if direction == "forward"  else 0,
                 json.dumps(connections), ts, session, ts, session]
            )
```

### 5.5 Storage layer — Search Coverage (with whitelist validation)

```python
def upsert_search_coverage(slug: str, jurisdiction: str,
                           data: dict, session: str, dry_run: bool = False):
    _validate_cols(data.keys(), _COVERAGE_COLS, "upsert_search_coverage")
    ts = now()
    with connect(dry_run) as conn:
        exists = conn.execute(
            "SELECT 1 FROM search_coverage WHERE slug=? AND jurisdiction=?",
            [slug, jurisdiction]
        ).fetchone()
        if exists:
            sets = ", ".join(f"{k}=?" for k in data)
            conn.execute(
                f"UPDATE search_coverage SET {sets}, "
                "updated_at=?, updated_by_session=? "
                "WHERE slug=? AND jurisdiction=?",
                [*data.values(), ts, session, slug, jurisdiction]
            )
        else:
            row = {"slug": slug, "jurisdiction": jurisdiction,
                   **data, **audit(session)}
            cols = ", ".join(row)
            ph   = ", ".join(["?"] * len(row))
            conn.execute(
                f"INSERT INTO search_coverage ({cols}) VALUES ({ph})",
                list(row.values())
            )

def upsert_search_language(slug: str, language: str,
                           data: dict, session: str, dry_run: bool = False):
    _validate_cols(data.keys(), _LANGUAGE_COLS, "upsert_search_language")
    # Same upsert pattern as above — omitted for brevity
    ...
```

### 5.6 Domain queries

```python
# --- Domain queries ---

def get_open_gaps(priority: str = None) -> list[dict]:
    q = "SELECT * FROM gaps WHERE status LIKE 'OPEN%'"
    params = []
    if priority:
        q += " AND priority=?"
        params.append(priority)
    q += " ORDER BY priority, gap_id"
    with connect() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]

def get_connections(status: str = None, confidence: str = None) -> list[dict]:
    q = """
        SELECT c.*, GROUP_CONCAT(ct.target, ', ') AS targets
        FROM connections c
        LEFT JOIN connection_targets ct USING (con_id)
        WHERE 1=1
    """
    params = []
    if status:
        q += " AND c.status=?"; params.append(status)
    if confidence:
        q += " AND c.confidence=?"; params.append(confidence)
    q += " GROUP BY c.con_id ORDER BY c.confidence DESC"
    with connect() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]

def get_unmined_sources(slug: str) -> list[dict]:
    with connect() as conn:
        rows = conn.execute("""
            SELECT ssl.local_ref_id,
                   es.doi, es.title,
                   COALESCE(cm.backward, 0) AS backward,
                   COALESCE(cm.forward,  0) AS forward
            FROM source_slug_links ssl
            JOIN evidence_sources es ON ssl.ref_id = es.ref_id
            LEFT JOIN citation_mining cm
                ON cm.slug=ssl.slug AND cm.local_ref_id=ssl.local_ref_id
            WHERE ssl.slug=?
              AND (COALESCE(cm.backward,0)=0 OR COALESCE(cm.forward,0)=0)
            ORDER BY ssl.local_ref_id
        """, [slug]).fetchall()
    return [dict(r) for r in rows]

def get_coverage_completeness(slug: str) -> dict:
    with connect() as conn:
        j = {r["jurisdiction"]: r["status"] for r in conn.execute(
            "SELECT jurisdiction, status FROM search_coverage WHERE slug=?",
            [slug]).fetchall()}
        l = {r["language"]: r["status"] for r in conn.execute(
            "SELECT language, status FROM search_languages WHERE slug=?",
            [slug]).fetchall()}
    return {
        "jurisdictions": j, "languages": l,
        "blockers": {
            "missing_jurisdictions": 24 - len(j),
            "not_run_jurisdictions": [k for k,v in j.items() if v == "NOT-RUN"],
            "missing_languages": 14 - len(l),
            "not_run_languages": [k for k,v in l.items() if v == "NOT-RUN"],
        }
    }

def get_synonyms(item_code: str, language: str = None) -> list[dict]:
    """Return all aliases for terms linked to an item code."""
    q = """
        SELECT t.canonical_en, ta.alias, ta.language, ta.alias_type
        FROM term_item_links til
        JOIN terms t USING (term_id)
        JOIN term_aliases ta USING (term_id)
        WHERE til.item_code=?
    """
    params = [item_code]
    if language:
        q += " AND ta.language=?"
        params.append(language)
    q += " ORDER BY ta.language, ta.alias_type, ta.alias"
    with connect() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]
```

---

## 6. Session Data Lifecycle (GitHub ↔ Container)

The container does not persist between sessions and does not clone the repository. GitHub files are accessed via API. This section specifies how the `.db` file and `scripts/db.py` move between GitHub and the container each session.

### 6.1 Session open — download

```python
# Pseudocode executed in bash_tool at session start (Step 2)

import base64, pathlib, requests

PAT = "..."
REPO = "jordanelias/guidebook"
HEADERS = {"Authorization": f"bearer {PAT}"}

def download_file(repo_path: str, local_path: str):
    r = requests.get(
        f"https://api.github.com/repos/{REPO}/contents/{repo_path}",
        headers=HEADERS
    )
    data = r.json()
    pathlib.Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(local_path).write_bytes(
        base64.b64decode(data["content"])
    )

download_file("data/guidebook.db", "/home/claude/data/guidebook.db")
download_file("scripts/db.py",     "/home/claude/scripts/db.py")
```

Or more efficiently — use the existing GraphQL read infrastructure for `db.py` (text file, readable via GraphQL), and a dedicated REST GET for the binary `.db` file.

### 6.2 During session — local operations

All SQLite operations run against the local `/home/claude/data/guidebook.db`. Zero API calls per operation. Immediately consistent. No SHA-staleness risk.

### 6.3 Session close — upload

```python
db_bytes = pathlib.Path("/home/claude/data/guidebook.db").read_bytes()
db_b64   = base64.b64encode(db_bytes).decode()

# Get current SHA for the PUT
r = requests.get(
    f"https://api.github.com/repos/{REPO}/contents/data/guidebook.db",
    headers=HEADERS
)
sha = r.json()["sha"]

requests.put(
    f"https://api.github.com/repos/{REPO}/contents/data/guidebook.db",
    headers=HEADERS,
    json={
        "message": f"db: session close [{now()}]",
        "content": db_b64,
        "sha": sha,
        "branch": "main"
    }
)
```

**Checkpoint commits during session:** Do not accumulate all changes into a single end-of-session upload. Upload the `.db` at logical boundaries — after each migration script completes, after a citation mining batch, after a connection-scout pass. This matches the existing practice of multiple commits per session and gives fine-grained rollback targets.

### 6.4 Comparison with current markdown workflow

| | Markdown registers | SQLite |
|---|---|---|
| GET cost | Full file every modification | One binary download at session open |
| Operations during session | One API call per GET/PUT | All local — zero API calls |
| Upload cost | One PUT per file per modification | One binary upload per checkpoint |
| Rollback granularity | Per-file, per-commit | Per-checkpoint-commit |
| Cross-file consistency | Not enforced | FK constraints enforce it |

SQLite is strictly better for this workflow when checkpoint commits are used.

---

## 7. Schema Migration Strategy

**Pattern: forward-only numbered migration files.**

```
scripts/migrations/
    001_initial_schema.sql
    002_add_terms_tables.sql     # if terms added after initial deploy
    ...
```

**Migration runner (`scripts/migrate_db.py`):**

```python
"""Run pending schema migrations against guidebook.db."""

import sqlite3, os
from pathlib import Path

MIGRATIONS_DIR = Path("scripts/migrations")
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

def get_user_version(conn) -> int:
    return conn.execute("PRAGMA user_version").fetchone()[0]

def set_user_version(conn, version: int):
    conn.execute(f"PRAGMA user_version = {version}")  # PRAGMA doesn't accept ?

def run_migrations(dry_run: bool = False):
    conn = sqlite3.connect(str(DB_PATH))
    current = get_user_version(conn)
    migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))

    pending = [m for m in migrations
               if int(m.stem.split("_")[0]) > current]

    if not pending:
        print(f"Schema at version {current} — no pending migrations.")
        return

    for mig in pending:
        version = int(mig.stem.split("_")[0])
        sql = mig.read_text()
        print(f"  Applying migration {mig.name}...")
        if not dry_run:
            conn.executescript(sql)
            set_user_version(conn, version)
            conn.commit()
        else:
            print(f"  [DRY-RUN] Would apply:\n{sql[:200]}...")

    conn.close()
    print(f"Schema migrated to version {max(int(m.stem.split('_')[0]) for m in pending)}.")
```

No rollback migrations. If a migration produces bad data: revert the `.db` file via git. The migration file itself is corrected and re-run as the next numbered migration.

---

## 8. Session-Start Protocol Change

### Current (markdown)
```
1a. GraphQL batch_read: LATEST + project-standards + workplan-orchestrator
1b. GraphQL read: session file + connections/_index.md     ← 4K tokens loaded
2.  Filtered bash: grep gap_register.md for OPEN P1        ← full file fetched
```

### Proposed (SQLite)
```
1a. GraphQL batch_read: LATEST + project-standards + workplan-orchestrator
1b. GraphQL read: session file (connections index NOT loaded)
1c. Download: data/guidebook.db + scripts/db.py → /home/claude/
2a. python3 scripts/db.py gaps --priority P1
    → JSON array of OPEN P1 gaps (instant SQL query, no file parsing)
2b. python3 scripts/db.py connections --status PENDING --summary
    → { "total": 55, "HIGH": 20, "MODERATE": 30, "SPECULATIVE": 5 }
    (summary count only at session open — full list on demand)
```

---

## 9. Migration Plan

### Phase 1-A — Infrastructure (one session)

1. Write `scripts/migrations/001_initial_schema.sql` — full DDL from §4
2. Write `scripts/db.py` — full implementation of §5 with CLI
3. Write `scripts/migrate_db.py` — migration runner
4. Write `scripts/init_db.py` — runs migration 001, seeds `db_meta`, sets `PRAGMA user_version = 1`
5. `python3 scripts/init_db.py` → creates `data/guidebook.db`
6. `PRAGMA integrity_check` → confirms clean state
7. Commit: `db: init SQLite data layer [YYYY-MM-DD HH:MM]`

### Phase 1-B — Data migration (one session per script, each with --dry-run first)

| Order | Script | Source | Validation |
|---|---|---|---|
| 1 | `scripts/migrate/migrate_slugs.py` | `slug-registry.md` | Count matches registry |
| 2 | `scripts/migrate/migrate_decisions.py` | `decision_register.yaml` | JSON arrays round-trip |
| 3 | `scripts/migrate/migrate_evidence_sources.py` | Per-BPC REF-ID tables | Collision report before INSERT |
| 4 | `scripts/migrate/migrate_connections.py` | `_index.md` + per-topic files | 232 rows; 55 PENDING; all targets populated |
| 5 | `scripts/migrate/migrate_gaps.py` | `gap_register.md` | No OPEN P1 rows lost |
| 6 | `scripts/migrate/migrate_bpc_metadata.py` | BPC front-matter | Count = slug count |

Each script: `--dry-run` first → review output → `--commit` to apply → upload `.db` checkpoint commit immediately.

**Citation mining seeding:** CON-0222–0239 predate the DB. Do not retroactively reconstruct — the specific local_ref_ids that were mined were not recorded. `citation_mining` table starts empty. Future mining passes will either: (a) find those CON-IDs already exist and not insert duplicates, or (b) re-mine the same sources and produce redundant connections that are caught at INSERT via the existing Pydantic dedup check. Both outcomes are acceptable.

**Terms table seeding:** Seed in a dedicated session after Phase 1-B completes. Start with high-value item clusters (grab bars, corridor geometry, lighting, acoustic) where synonym expansion will immediately benefit ongoing citation mining.

### Phase 1-C — Operational switchover

- Update `workplan-orchestrator_SKILL.md`: replace GraphQL connection index load with SQLite query; replace grep-based gap filter with `python3 scripts/db.py gaps --priority P1`
- Update `session-consolidator_SKILL.md`: write register changes via db.py CLI, checkpoint-upload after each batch
- Update `connection-scout_SKILL.md`: `next_con_id()` via CLI; INSERT via CLI; check `is_mined()` before mining
- Update `gap_register` write protocol in project-standards: deprecated for new entries; all new gaps via `insert_gap`

### Phase 1-D — CI migration

- Update `validate_cross_refs.py`: query `guidebook.db` for CON-IDs instead of parsing `_index.md`
- Update `check_thresholds.py`: **remove** threshold checks for `gap_register.md` and `connections/_index.md`; **retain** check for `project-standards.md` (still markdown)
- Add `scripts/validate_db.py` per §10

### Phase 1-E — Archive

- Add `data/guidebook.db binary` to `.gitattributes`
- `data/guidebook.db` must **not** be in `.gitignore`
- Freeze markdown registers: add `<!-- ARCHIVED YYYY-MM-DD — source of truth is data/guidebook.db -->` header; stop updating
- File CO-0009: remove threshold rules in `project-standards.md` for migrated files

---

## 10. validate_db.py Spec

```
Checks:
  C1  PRAGMA integrity_check → must return 'ok'
  C2  PRAGMA foreign_key_check → must return 0 rows
  C3  PRAGMA user_version → must match expected version constant in script
  C4  connections with 0 rows in connection_targets → must be 0 (every connection needs ≥1 target)
  C5  evidence_sources with neither doi nor doi_less_key → WARNING (incomplete dedup data)
  C6  citation_mining rows with backward=1 AND forward=1 AND connections_produced='[]'
      → INFO only (mining completed, nothing found — valid outcome)
  C7  source_slug_links.local_ref_id not present in citation_mining for same slug
      → INFO: count of unmined sources per slug
  C8  gaps with status LIKE 'OPEN%' AND priority NOT IN ('P1','P2','P3') → ERROR
  C9  term_item_links.item_code not in items table (Phase 2: enforce FK; Phase 1: INFO only)

Exit codes:
  0  all checks pass (including INFO)
  1  error (C1–C4, C8)
  2  warning only (C5)
```

---

## 11. Pydantic Integration

No schema changes required. Add bridge methods to `GuidebookEntity`:

```python
@classmethod
def from_row(cls, row) -> "GuidebookEntity":
    """Load from sqlite3.Row or dict."""
    return cls.model_validate(dict(row))

def to_row(self) -> dict:
    """Serialize for SQLite INSERT, excluding None values."""
    return self.model_dump(mode="json", exclude_none=True)
```

The flow for reads:
```python
rows = get_connections(status="PENDING")
entities = [Connection.from_row(r) for r in rows]   # validates on read
```

YAML methods (`from_yaml`, `to_yaml`) remain for entities that stay in YAML.

---

## 12. Phase 2/3 Roadmap (Anticipated — Not Implemented in Phase 1)

Phase 1 schema is designed to anticipate Phase 2 without requiring changes to existing tables. The following tables will be added in Phase 2:

```
items           -- item code, title, category, DAR flag
specifications  -- one row per item+mode+population combination
measurements    -- numeric values per specification
room_items      -- junction: room × item (populates Part 6/7 matrices)
spec_populations-- junction: specification × population
spec_evidence   -- junction: specification × evidence_source
conflict_domains-- the 12 environmental parameter conflict domains
```

Phase 3 converts all generators to read from SQLite:

```
generate_spec_page(item_code)    →  queries items + specifications + measurements + spec_evidence
generate_room_matrix(room_code)  →  queries room_items + specifications + measurements
generate_population_page(pop)    →  queries spec_populations + items + measurements
generate_part4_section(item)     →  queries full evidence chain for prose injection
```

**What Phase 1 leaves ready for Phase 2:**
- `source_slug_links` → `spec_evidence` FK ready (ref_id is the shared key)
- `connection_targets.target` → `items.item_code` FK ready (same code format)
- `term_item_links.item_code` → `items.item_code` FK ready (noted as Phase 1 unconstrained; Phase 2 enforces)
- `bpc_metadata` → extends to include Phase 2 population-specific fields without schema change

---

## 13. Git Considerations

- Binary file: diffs show "Binary files differ" — acceptable for solo project; session YAML records logical changes
- `data/guidebook.db binary` in `.gitattributes` — prevents spurious line-ending transforms
- Do **not** add to `.gitignore`
- Checkpoint commits during session give rollback granularity matching current markdown practice
- Size projection: all Phase 1 data well under 2MB; Phase 2 entity data adds ~5MB maximum
- Alternative considered and rejected: nightly `sqlite3 guidebook.db .dump > guidebook.sql` — adds session discipline overhead that doesn't reliably exist in this workflow
