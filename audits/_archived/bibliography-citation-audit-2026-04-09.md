# Bibliography & Citation Audit
**Date:** 2026-04-09 22:42
**Scope:** Entire project — bibliography-v9.md, 91 BPC files, 7 Part 5 volume files, 2 systematic reviews
**Model:** Sonnet 4.6 (verification via PubMed + web search)

---

## 1. Executive Summary

| Metric | Value |
|---|---|
| Bibliography-v9 entries | 220 |
| Items using legacy `Key citations` | 89 |
| Items using `Sources cited` + REF-ID | 0 |
| ⚠ flagged entries | 14 |
| ❌ entries | 0 (but see §3 — 3 should be ❌) |
| Confirmed hallucinations | 2 |
| Misattributions (real paper, wrong author) | 2 |
| Ghost citations (unverifiable) | 3 |
| Sources added since bib compilation (2026-03-27) not in bibliography | ~50+ |

---

## 2. Conversion Blocker Analysis

**Why aren't BPC sources being converted into the bibliography?**

The endnote pipeline has five stages:

```
item-specification-writer (emits REF-ID + Sources cited)
  → vol2-item-formatter (validates)
    → chunk-assembler
      → bibliography-compiler (REF → superscript + endnote list)
        → cross-reference-resolver
```

**The blocker is Stage 1.** All 89 items in the active volume files (`parts/88_to_90/part05-*`) use the legacy `**Key citations:**` format — free-text inline citations with no structured metadata. The bibliography-compiler skill explicitly passes these through unchanged with a `[LEGACY-CITATION — conversion required]` flag.

Conversion requires each item to be individually revised by `item-specification-writer`, which:
1. Runs `research-log-manager RETRIEVE` for the item's BPC
2. Emits `[REF:{slug}:{NN}]` markers in body text
3. Generates a structured `#### Sources cited` table with DOI, tier, jurisdiction

This was proven to work in the dry-run (2026-03-29, item E-14). But batch conversion across 89 items has not been scheduled because:

- **Dependency chain:** Items need content revision first (voice-style pass, connection integration, FDR scenario integration). Converting citation format on items that will be rewritten wastes effort.
- **Session priorities:** Connection register migration (CO-0006), systematic reviews, FDR compound scenarios, and CRPD integration have consumed sessions since March 27.
- **No standalone path:** GAP-CR-01 correctly notes that bibliography-compiler requires upstream REF-ID markers. Without them, no compilation is possible. This is a pipeline dependency, not a bug.

**Resolution path:** Citation conversion should be bundled with the item revision pass (Phase 3 Document Assembly). When each item is revised, item-specification-writer emits the new format. After all items are revised, bibliography-compiler runs once per volume.

---

## 3. Hallucination Audit

### 3A. Confirmed hallucinations (fabricated or unlocatable)

| # | Entry | Status | Evidence |
|---|---|---|---|
| H-1 | `Latiff, A., et al. (2024). Biophilic outdoor transitional spaces for NDV populations. [EN, Co-1]` | **HALLUCINATED** | No publication by "Latiff" on this topic exists. Web search returns Aminpour et al. (UNSW, 2024) on biophilic design for neurodivergent people, and Finnigan (2024) SREF framework. Neither matches. Source appears fabricated. |
| H-2 | `MDPI Buildings. (2026). Intellectual disability and home design [forthcoming]. Buildings, 16(3), 489.` | **UNVERIFIABLE — likely hallucinated** | Already flagged ⚠. No MDPI Buildings article with this volume/issue/page exists. "Forthcoming" with specific pagination is a hallucination pattern. |
| H-3 | `PMC. (2025). [Intellectual disability home design scoping review — PMC ID not recorded].` | **GHOST CITATION** | Already flagged ⚠. No PMC ID, no author, no title. Cannot be verified. Delete. |

### 3B. Misattributions (real paper, wrong metadata)

| # | Entry as listed | Correct attribution | Error |
|---|---|---|---|
| M-1 | `Caldwell, J., et al. (2025). A calm space to reset: perceptions of sensory rooms in Australian public buildings. Archnet-IJAR.` | **Watchorn, V., Cartledge, M., Grant, C., Walker, A., & Hale, I. (2025).** DOI: 10.1108/ARCH-10-2024-0453 | Author completely wrong. "Caldwell, J." does not appear as an author. Paper is real. |
| M-2 | `Sensory Responsive Environments Framework (SREF) (2024). MDPI Land, 13(5), 636. [EN, Co-1]` | **Finnigan, K.A. (2024).** Sensory Responsive Environments: A Qualitative Study... Land, 13(5), 636. | Listed by framework name instead of author. Paper is real. |

### 3C. Other ⚠ entries requiring resolution

| # | Entry | Issue | Action |
|---|---|---|---|
| W-1 | NIHR (2023) bariatric facilities design | "specific publication not identified" — already flagged | DELETE — no standalone NIHR bariatric design publication exists |
| W-2 | Amputee Coalition (2023) home modification guide — ⚠ URL | Verify URL | Low priority — org is real |
| W-3 | Mostafa et al. (2024) ASPECTSS 2.0 — ⚠ publication details | "in Vol 2B citation register" | Locate and complete metadata |
| W-4 | NINDS (2024) POTS fact sheet — ⚠ | URL stub only | Complete with full URL |
| W-5 | Hamraie (2017) Building Access — ⚠ | Book — likely real, needs DOI/ISBN | Verify ISBN: 978-0-8166-9642-0 |
| W-6 | Imrie (2012) Disability and Rehabilitation — ⚠ | **CONFIRMED REAL** — PMID 22054109 | Upgrade to ✅, add DOI: 10.3109/09638288.2011.624250 |
| W-7 | Lee, O'Neill, Forgues (2019) grab bar positioning — ⚠ | "citation to be confirmed" | Verify or delete |
| W-8 | NIOSH (2021) stairway falls — ⚠ | URL stub | Complete URL |
| W-9 | PSSRU (2012) unit costs — ⚠ | Standard grey lit — likely real | Low priority |
| W-10 | Stannah (2024) stairlift guide — ⚠ | "Industry reference" | Accept as industry/Tier 6 or delete |
| W-11 | JOTA (2022) practice guidelines — ⚠ | Japanese source, translation | Verify via JOTA website |

### 3D. PubMed-verified entries (spot check)

| Entry | PMID | Status |
|---|---|---|
| Molderings et al. (2011) J Intern Med | 21895806 | ✅ CONFIRMED |
| Levine et al. (2025) JMIR Rehab | 40694815 | ✅ CONFIRMED |
| Imrie (2012) Disabil Rehabil | 22054109 | ✅ CONFIRMED |
| Cloete & Rout (2025) Acta Structilia | — (not PubMed indexed) | ✅ CONFIRMED via AJOL |

---

## 4. Post-Compilation Source Gap

Bibliography-v9 was compiled 2026-03-27. Since then, the following research outputs have added new sources NOT yet in the bibliography:

| Source of new citations | Approx. new sources | Date |
|---|---|---|
| 5 systematic reviews (PRISMA-lite) | ~50 studies across 5 domains | 2026-04-09 |
| CRPD implementation BPC (Phase 2) | 12 sources (3 new) | 2026-04-07 |
| FDR compound scenarios (sessions 03-27–03-28) | ~15–20 OT CPG sources | 2026-03-27–28 |
| Connection register entries CON-0114–0170 | Unknown (57 connections, some cite new sources) | Pending write-back |

**Estimated total new sources not in bibliography: 50–80+**

These sources exist in BPC files and systematic review documents but have not been compiled into bibliography-v9 because:
1. Bibliography-compiler requires assembled volumes with REF-ID markers (the conversion blocker above)
2. No manual bibliography update has been run since compilation date
3. The citation-verifier HARVEST mode could extract them, but hasn't been triggered

---

## 5. Structural Issues

1. **No citation-to-item map exists.** The bibliography lists sources alphabetically by section (A–E) but does not record which items cite which sources. The bibliography-compiler is designed to produce this, but can't run yet.

2. **BPC Key sources use slug-based shorthand** (e.g., `Levine2025-JMIR · Greene2024-CJOT`) while bibliography uses APA format. No automated crosswalk exists between these two formats.

3. **Duplicate potential:** Some sources appear in multiple BPC files under slightly different shorthand slugs. The bibliography-compiler's deduplication (by DOI) would catch these, but manual compilation risks duplicates.

4. **Section classification (A–E) is informal.** The bibliography header says `A: 63 · B: 61 · C: 83 · D: 9 · E: 4` but section assignment is done by topic grouping, not by item code reference.

---

## 6. Recommended Actions

| Priority | Action | Skill | Model |
|---|---|---|---|
| P1 | Delete H-1 (Latiff), H-2 (MDPI 2026), H-3 (PMC ghost) from bibliography-v9 | Manual edit | Sonnet |
| P1 | Correct M-1 (Caldwell→Watchorn) and M-2 (SREF→Finnigan) in bibliography-v9 | Manual edit | Sonnet |
| P1 | Upgrade W-6 (Imrie) to ✅ with DOI | Manual edit | Sonnet |
| P2 | Delete W-1 (NIHR bariatric) | Manual edit | Sonnet |
| P2 | Resolve remaining 8 ⚠ entries (W-2–W-11) | citation-verifier | Sonnet |
| P2 | Run citation-verifier HARVEST on systematic reviews file to capture ~50 new verified sources | citation-verifier | Sonnet |
| P3 | Bundle citation format conversion with item revision pass during Phase 3 Document Assembly | item-specification-writer | Sonnet |
| P3 | After all items revised: run bibliography-compiler per volume | bibliography-compiler | Haiku |

---

## 7. Backfill Execution

### Immediate corrections (P1) — ready to commit

**Deletions:**
- Line ~376: Delete `MDPI Buildings. (2026). Intellectual disability...`
- Line ~393: Delete `PMC. (2025). [Intellectual disability home design...]`
- Delete `Latiff, A., et al. (2024). Biophilic outdoor transitional spaces...`

**Corrections:**
- `Caldwell, J., et al. (2025)` → `Watchorn, V., Cartledge, M., Grant, C., Walker, A., & Hale, I. (2025). "A calm space to reset": perceptions of sensory rooms in Australian public buildings. Archnet-IJAR: International Journal of Architectural Research, ahead-of-print. DOI: 10.1108/ARCH-10-2024-0453`
- `Sensory Responsive Environments Framework (SREF) (2024). MDPI Land, 13(5), 636.` → `Finnigan, K.A. (2024). Sensory Responsive Environments: A Qualitative Study on Perceived Relationships between Outdoor Built Environments and Sensory Sensitivities. Land, 13(5), 636. DOI: 10.3390/land13050636`
- `Imrie, R. (2012)` → upgrade ⚠ to ✅, add DOI: 10.3109/09638288.2011.624250, PMID: 22054109
- `NIHR (2023) bariatric` → DELETE

**Updated header counts after corrections:**
- Entries: 216 (was 220, minus 4 deletions)
- Verification: recalculate ✅/⚠ counts
