---
name: volii-validator
description: >
  Validate item code cross-references in the application volume of the guidebook — confirming
  that every item code cited in Volume 1, Volume 3, or any other volume actually exists in the
  application volume item library, that declared population categories are consistent, and that
  item descriptions match across volumes. ALWAYS use this skill when asked to: validate item codes,
  check application volume cross-references, verify design specification codes, check whether a
  referenced item exists in the item library, or audit cross-reference integrity for item-coded
  specifications. Trigger on: "validate item codes", "check item references", "cross-reference audit",
  "does this item code exist", "item code check", "volii check", "item library validation".
  Operates in PROVISIONAL mode until the application volume full text is available; FULL mode when available.
---

**Model:** Sonnet 4.6
**Intake:** pre-chunked section or item code list. Full document → `haiku-chunker` Mode D first.
**Storage:** `guidebook:volii:{item-code}`

Storage entry:
```yaml
code: A-04
first_seen: "Vol I §3.2 — refers to acoustic zoning"
declared_categories: [NEU, NDV]
vol_ii_status: UNVERIFIED-PENDING|CONFIRMED|NOT_FOUND|MISMATCH
vol_ii_description: ""
last_updated: YYYY-MM-DD
```

## Modes

**PROVISIONAL** (application volume unavailable): build registry from cross-references in other volumes. Record: code · reference context · declaring section · declared categories. Mark all UNVERIFIED-PENDING. Output: `volii-registry.md`.

**FULL** (application volume available): cross-reference every cited code against the item library.
- Exists in library? → CONFIRMED / NOT_FOUND
- Description matches? → MATCH / MISMATCH
- Declared categories consistent? → CONSISTENT / INCONSISTENT

## Output
| Code | Reference Location | Declared Categories | Library Status | Notes |

Summary: X codes — Y CONFIRMED / Z NOT_FOUND / W MISMATCH / V UNVERIFIED-PENDING
Persist all entries to storage.
