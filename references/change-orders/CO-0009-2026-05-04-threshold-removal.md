# CO-0009 — Remove Markdown Register Threshold Rules
**Date:** 2026-05-04 19:20
**Status:** SIGNED OFF
**Supersedes:** Rules at lines 460–472, 561 of project-standards.md

## Rationale

Phase 1 SQLite migration (INFRA-S1, 2026-05-05) moved all structured data from markdown registers to `data/guidebook.db`. The following threshold management infrastructure is now obsolete:

1. **`scripts/check_thresholds.py`** — monitored markdown file sizes (gap_register.md at 20K, connection-register at 15K, citation-mining-register at 6K). SQLite has no token-threshold concern.
2. **Citation mining register rule** (line 561) — references `references/citation-mining-register.md` as canonical. Citation mining data is now in the `citation_mining` SQLite table. The markdown file never existed (born in SQLite per architecture decision).

## Changes

### project-standards.md

**RETIRE** the `check_thresholds.py` section (lines 460–472):
- `### scripts/check_thresholds.py` block
- Threshold table (gap_register 20K, connection-register 15K)
- Usage line

**RETIRE** citation-mining-register rule (line 561):
- Replace with: "Citation mining state is in SQLite (`citation_mining` table). Query via `python3 scripts/db.py mining`. CHECK before mining; LOG after. Skipping = protocol error."

**RETIRE** connection register read-once rule (line 258):
- Replace with: "Connection state is in SQLite. Query via `python3 scripts/db.py connections`. Do not load archived markdown connection files."

### Scripts

**`scripts/check_thresholds.py`** — archive to `_archived/`. No longer called by any skill or CI.

## Impact

No functional impact. Removes ~500 tokens of obsolete rules from project-standards.md context load.
