# ⚠️ DEPRECATED — Do not use as audit source

`Guidebook_for_Accessible_Design_v9-0_2026-03-20.md` is a **frozen document snapshot from 2026-03-20**.

Since March 2026, specification content has been maintained in:
- **`references/specification-database.json`** — structured spec data (73 specs, updated 2026-05-04)
- **`references/bpc/`** — 81 Best Practice Compendium files with evidence tiers, population coverage, economics data (updated through 2026-05-07)
- **`data/db/guidebook.db`** — website DB with 141 specifications, measurements, populations, connections (updated continuously)

The v9 document is retained for:
- Historical reference
- Cross-reference verification (item codes, titles, structural layout)
- Text that has not yet been migrated to structured format

**Do not audit, pipeline, or generate gaps from v9 alone.** Use specification-database.json + BPC content + website DB as authoritative sources.

Added: 2026-05-08. Reason: C3 pipeline pre-pass incorrectly ran against v9 only, generating gaps already resolved in BPC content. 51 gaps closed as CLOSED-SYNC after BPC cross-reference.
