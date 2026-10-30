---
name: leverage-full-data-capabilities
description: "Standard for the Guidebook — leverage every available data-management capability (SQLite-native + ecosystem) for clean, transparent data; don't leave integrity/transparency features switched off."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d8ad22dd-b407-4f8b-b198-5ff102840966
---

The Guidebook must leverage **every** capability available for clean and transparent data management ("as per sqlite or whatever"). Declaring integrity in DDL is not enough if enforcement is off or the feature is unused.

**Why:** The mission ([[project-end-goal]]) demands policy-grade, academically-defensible, traceable data ([[contract-traceability-invariant]]). Unused integrity/transparency capabilities are silent risk: a column that *can* hold garbage eventually will; an unenforced FK is documentation, not a guarantee.

**Baseline gap measured 2026-06-22 (committed DB):** STRICT tables 0/39 (no type safety); `evidence_sources` 88 cols with 0 NOT NULL; triggers 0 (no automated provenance/audit-trail); views 1 (derived transparent surfaces unused); generated columns 0; FTS5 0 (no full-text over an evidence/search corpus); `PRAGMA foreign_keys` defaults OFF and ~18 legacy violations are tolerated; application_id unset; JSON stored as TEXT with no `json_valid()` CHECK. WAL mode + migrations + 93 indexes + CHECK on 25/39 are the good parts already in use.

**How to apply:** When touching the data layer, prefer the strongest available mechanism: STRICT tables + NOT NULL/UNIQUE on logical keys; continuous FK enforcement (zero tolerated violations); triggers for audit-trail/updated_at/invariant enforcement; VIEWS as the transparent derived surfaces (coverage matrix, bibliography, provenance-trace) instead of hand-maintained grids; FTS5 for evidence/term search; generated columns for dedup/normalized keys; `json_valid()` CHECK on JSON columns; integrity_check + foreign_key_check as blocking CI gates; and ecosystem tools (Datasette for transparent/faceted publishing of the queryable site, sqlite-utils for clean ingestion). Kill parallel YAML stores in favor of single-source-of-truth DB + generated exports.
