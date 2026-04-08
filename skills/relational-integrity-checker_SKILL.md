---
name: relational-integrity-checker
description: >
  Systematic verification that item codes, population codes, and slug names referenced across
  gap register, connection register, BPC entries, Part 4 scaffold, and application matrices
  are internally consistent. Detects orphan references, phantom references, and stale
  pre-CO-0004 codes. Run before structural migrations and as part of quarterly maintenance.
  Trigger on: "check integrity", "verify references", "orphan codes", "phantom items",
  "relational check", or before any connection register migration.
---

<!-- Created: CO-0006 2026-04-08 -->

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main`
**Canonical sources:**
- Item codes: Part 4 TOC (parts/v10/part04.md or toc.md §Part 4)
- Population codes: workplan-orchestrator_SKILL.md §Population Codes
- Slug names: `references/slug-registry.md`
**Run before:** connection register migration; BPC schema migration; any structural change touching cross-references

---

## Process

### Step 1 — Build canonical lookup tables

Load and parse:
1. `references/toc.md` → extract all canonical item codes (A-01 through K-NN). Store as `canonical_items`.
2. `skills/workplan-orchestrator_SKILL.md` §Population Codes → extract all canonical pop codes (MOB, VIS, DEAF, etc.). Store as `canonical_pops`.
3. `references/slug-registry.md` → extract all slug names. Store as `canonical_slugs`.

### Step 2 — Extract references from scope files

For each scope file below, extract all item codes, population codes, and slug names via pattern matching:

| Scope file | Extract |
|---|---|
| `gap_register.md` | Item codes (letter-digit pattern), pop codes, slug names |
| `references/connections/_index.md` | Item codes, pop codes |
| `references/connections/{topic}/connections.md` (all) | Item codes, pop codes, slug names |
| `references/bpc/{topic}/{slug}.md` (sampled or all) | Item codes, pop codes |
| Part 4 scaffold | Item codes, pop codes |

### Step 3 — Cross-reference

For each extracted reference:

**Item codes:**
- In `canonical_items` → OK
- Not in `canonical_items`, matches pre-CO-0004 pattern (e.g., bare number, old letter prefix) → STALE
- Not in `canonical_items`, no pattern match → PHANTOM

**Population codes:**
- In `canonical_pops` → OK
- Not in `canonical_pops` → PHANTOM or TYPO (flag both)

**Slug names:**
- In `canonical_slugs` → OK
- Not in `canonical_slugs` → ORPHAN-SLUG (slug referenced but not in registry)

### Step 4 — Report

```markdown
## Relational Integrity Report
**Date:** YYYY-MM-DD HH:MM
**Scope:** {files checked}

### Summary
| Category | Count |
|---|---|
| Item codes checked | N |
| OK | N |
| STALE (pre-CO-0004) | N |
| PHANTOM (undefined) | N |
| Population codes checked | N |
| OK | N |
| PHANTOM / TYPO | N |
| Slugs checked | N |
| OK | N |
| ORPHAN-SLUG | N |

### STALE item codes (pre-CO-0004)
| Code found | Location | Likely new code | Action |
|---|---|---|---|

### PHANTOM references
| Reference | Type | Location | Action |
|---|---|---|---|

### ORPHAN slugs
| Slug | Location | Action |
|---|---|---|
```

**Action values:** `UPDATE` (stale → new code known) · `INVESTIGATE` (no clear mapping) · `DELETE` (reference serves no purpose)

### Step 5 — Optional auto-fix

If user confirms: apply `UPDATE` fixes automatically via GitHub PUT. Log each fix. Do not auto-fix `INVESTIGATE` or `DELETE` — surface for manual review.

---

## Token Management

- Load scope files in batches of 5. Do not load all at once.
- For BPC entries: sample 10 randomly + any touched this session. Full pass only if explicitly requested.
- Report stale/phantom counts after each batch; commit intermediate report to GitHub if >20 issues found mid-run.

---

## Commit convention
`relational-integrity-checker: integrity report [{YYYY-MM-DD HH:MM}]`
