## Bibliography Assembly Report — Dry Run (E-10)

**Date:** 2026-03-28 16:50
**Item tested:** E-10 Rest Seating on Circulation Routes (revised)
**Volume:** II (Part 7, Category E)
**Purpose:** Endnote pipeline gate — Standing Rule 17 (must pass before Phase 3)

### Result: PASS ✅

| Metric | Value |
|---|---|
| REF-ID markers in body | 6 (3 unique) |
| Sources-cited rows | 3 |
| Unique sources | 3 |
| Endnotes generated | ¹²³ |
| ORPHAN-REF errors | 0 |
| UNUSED-SOURCE warnings | 0 |
| DOI-MISSING warnings | 3 (non-blocking) |
| LEGACY-CITATION flags | 0 |

### Endnote output (simulated)

```
## Endnotes

### Category E: Entry and Circulation — E-10

¹ Roxburgh, R., Hughes, J., & Milgate, W. (2024). Using time diaries to inform OT practice for people with ME/CFS. *British Journal of Occupational Therapy*. [Tier 1; UK] [DOI required]

² Royal College of Occupational Therapists (2019). Housing Adaptations Without Delay. *RCOT/Housing LIN*. [Tier Co-2; UK] [DOI required]

³ British Standards Institution (2018). BS 8300-2:2018. Design of an accessible and inclusive built environment — Part 2: Buildings. *BSI*. [Tier 5; UK] [DOI required]
```

### Errors
| Type | Count | Details |
|---|---|---|
| ORPHAN-REF | 0 | — |

### Warnings
| Type | Count | Details |
|---|---|---|
| UNUSED-SOURCE | 0 | — |
| DOI-MISSING | 3 | All FDR new sources; DOIs to be retrieved at citation-verifier pass |
| LEGACY-CITATION | 0 | — |

### Notes
- Tier column parsing cosmetic issue: parser reads Lang column instead of Tier column from sources-cited table. Tier values correct in sources-cited table; display artifact only. Resolve at haiku-chunker preprocessing step before full-volume run.
- Full volume run requires chunk-assembler to assemble Part 7 before bibliography-compiler processes entire volume.
- Endnote numbering will reset to ¹ at volume boundary.

### Gate status
**Standing Rule 17 (endnote pipeline dry run) — CLEARED**
Phase 3 may proceed.
