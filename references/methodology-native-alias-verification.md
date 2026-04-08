# Native Alias Verification — Tracking Document
**Generated:** 2026-04-08 (Phase 1C — CO-0006)
**Basis:** Extraction across 90 search-log slug files (28 with native_aliases populated)
**Scope:** 14 base languages + 5 CO-0005 languages (AR/HI/ID/SW/BN)

---

## Executive Summary

| Issue | Count | Risk |
|---|---|---|
| INLINE-GENERATED terms (LLM output, unverified) | 14 (1 per language, same slug) | MEDIUM — single slug |
| UNTAGGED terms (no verification status recorded) | ~18 instances | MEDIUM — unknown quality |
| PARTIAL terms (boundary mismatch noted) | ZH: 14, JA: 12, KO: 12, DA: 8, FI: 8 | LOW — flagged; deviations documented |
| CO-0005 languages: ALL terms absent | AR/HI/ID/SW/BN: 28/28 MISSING | HIGH — no searches run yet |
| CLEAN terms | 14–22 per language | — verified |

**Critical finding:** All INLINE-GENERATED instances are in a single slug: `threshold-door-hardware`. This slug ran a 13-language Co-1 pass that is still outstanding. The INLINE-GENERATED status applies to search terms used in that specific pass only — not a systemic failure across all slugs.

**CO-0005 language absence** is expected: AR/HI/ID/SW/BN were added in CO-0005 (2026-04-05) and searches have not yet been run with these terms. The UNVERIFIED designation from CO-0005 applies to the keyword compendium terms themselves, not to search-log entries (none exist yet).

---

## Verification Status by Language

### Tier 1: CLEAN — no action required at this time
Terms tagged `[CLEAN]` have been used in research and produced results consistent with the concept boundary. Treat as provisionally verified until native-speaker review is scheduled.

| Language | CLEAN slugs | PARTIAL slugs | INLINE-GEN | UNTAGGED |
|---|---|---|---|---|
| Swedish (SV)  | 19 | 6 | 1 | 2 |
| Norwegian (NO)  | 20 | 6 | 1 | 1 |
| Danish (DA)  | 18 | 8 | 1 | 1 |
| Finnish (FI)  | 19 | 8 | 1 | 0 |
| French (FR) ⭐ | 19 | 6 | 1 | 2 |
| German (DE) ⭐ | 22 | 3 | 1 | 2 |
| Chinese (ZH) ⭐ | 12 | 14 | 1 | 1 |
| Japanese (JA) ⭐ | 14 | 12 | 1 | 1 |
| Dutch (NL)  | 22 | 3 | 1 | 2 |
| Spanish (ES)  | 19 | 8 | 1 | 0 |
| Portuguese (PT)  | 20 | 5 | 1 | 2 |
| Korean (KO) ⭐ | 14 | 12 | 1 | 1 |
| Italian (IT)  | 18 | 8 | 1 | 1 |
| English (EN)  | 1 | 0 | 0 | 1 |

⭐ = High-priority: national standards body publishes in this language (DE, FR, JA, ZH, KO)

---

### Tier 2: INLINE-GENERATED — remediation required

**Affected slug:** `threshold-door-hardware` — all 14 languages
**Source:** Terms generated inline (LLM) during initial search setup, before Keyword Compendium was available.
**Risk:** If terms were incorrect, the threshold-door-hardware EN pass may have missed non-EN sources. 13 non-EN Co-1 passes are already outstanding for this slug.

**Remediation process:**
1. Load Keyword Compendium, Part 3, concept group for threshold/door hardware.
2. Compare INLINE-GENERATED terms against Compendium terms for all 14 languages.
3. Where terms differ: flag search deviation; re-run language pass with correct terms.
4. Update search-log `native_aliases` entries from INLINE-GENERATED → CLEAN or PARTIAL.
5. Record in search-log: `[VERIFIED-COMPENDIUM YYYY-MM-DD]`

**Assign to:** Next `threshold-door-hardware` multilingual-research session (already scheduled — 13 non-EN Co-1 passes outstanding per session blockers).

---

### Tier 3: UNTAGGED — remediation required

Terms present but no `[CLEAN]`/`[PARTIAL]`/`[INLINE-GENERATED]` tag. Status unknown.

| Language | Slug | Term (truncated) | Action |
|---|---|---|---|
| SV | residential-accessible-home-case-studies | tillgangliga bostader fallstudier / bostadsanpassning f | Add status tag |
| SV | room-acoustic-performance | efterklangstid / rumakustik | Add status tag |
| NO | residential-accessible-home-case-studies | tilgjengelige boliger / boligtilpasning funksjonshemnin | Add status tag |
| DA | room-acoustic-performance | efterklangstid / rumakustik | Add status tag |
| FR | residential-accessible-home-case-studies | logement accessible etudes de cas / adaptation domicile | Add status tag |
| FR | room-acoustic-performance | temps de réverbération / acoustique intérieure | Add status tag |
| DE | residential-accessible-home-case-studies | barrierefreie Wohnung Fallstudien / Wohnungsanpassung B | Add status tag |
| DE | room-acoustic-performance | Nachhallzeit / Hörsamkeit | Add status tag |
| ZH | room-acoustic-performance | 混响时间 / 室内声学 | Add status tag |
| JA | residential-accessible-home-case-studies | bariafu-ri jutaku jirei kenkyu / jutaku kaishu shogaish | Add status tag |
| NL | residential-accessible-home-case-studies | toegankelijke woningen casestudies / woningaanpassing b | Add status tag |
| NL | room-acoustic-performance | nagalmtijd / ruimteakoestiek | Add status tag |
| PT | DBL | surdocego / comunicação tátil / surdo-cegueira | Add status tag |
| PT | deafblind-built-environment-design | surdocego / comunicação tátil / surdo-cegueira | Add status tag |
| KO | room-acoustic-performance | 잔향시간 | Add status tag |
| IT | room-acoustic-performance | tempo di riverberazione | Add status tag |
| EN | cross-population-case-studies | cross-population accessible design case studies | Add status tag |

**Remediation:** For each UNTAGGED entry, determine source of term:
- If loaded from Keyword Compendium → tag `[CLEAN]`
- If generated inline without Compendium check → tag `[INLINE-GENERATED]`; add to INLINE-GEN remediation queue
- If from published glossary → tag `[VERIFIED-GLOSSARY source]`

**Assign to:** research-log-manager LOG operator — apply correct tag on next touch of each affected slug.

---

### Tier 4: PARTIAL — monitored, no immediate action

PARTIAL terms are documented concept boundary mismatches — the native term covers a broader or narrower concept than the English slug. These are the expected and handled case. Deviations are recorded in `concept_boundary_warnings`.

**High PARTIAL counts (ZH: 14, JA: 12, KO: 12):** Reflects genuine conceptual differences in East Asian accessibility discourse, not search failures. Evidence retrieved via PARTIAL terms is valid; concept boundary notes in BPC entries document the deviation.

**Action:** None — these are working as intended. Review only if a BPC entry shows NO-DATA for ZH/JA/KO with PARTIAL-tagged terms, which would indicate the boundary deviation caused missed retrieval.

---

## CO-0005 Languages — Pre-Search Verification Required

AR, HI, ID, SW, BN have no search-log entries because no searches have been run yet. CO-0005 marked all five as UNVERIFIED. Terms must be verified before first search pass.

| Language | CO-0005 status | Verification path | Priority |
|---|---|---|---|
| AR (Arabic) | UNVERIFIED | Native-speaker review or published Arabic accessibility glossary (e.g., ESCWA standards) | High — IN, EG, MA searches pending |
| HI (Hindi) | UNVERIFIED | Native-speaker review or MoHUA Harmonised Guidelines Hindi version | High — IN searches pending |
| ID (Indonesian) | UNVERIFIED | Native-speaker review or SNI standard bilingual editions | Medium — ID searches pending |
| SW (Swahili) | UNVERIFIED | Native-speaker review — no known published accessibility glossary | Low — KE/TZ searches pending |
| BN (Bengali) | UNVERIFIED | Native-speaker review or BNBC 2020 Bengali edition | Medium — BD searches pending |

**Verification method options (ranked):**
1. Published bilingual standard (e.g., MoHUA Hindi, BNBC Bengali) → tag `[VERIFIED-STANDARD]`
2. Native-speaker review by OT or disability professional → tag `[VERIFIED-NATIVE]`
3. DPO publication check — does the jurisdiction's primary DPO publish in this language? Retrieve and confirm terms → tag `[VERIFIED-CO1]`
4. If none available: retain `[UNVERIFIED]`; flag all retrieval `[UNVERIFIED-TERMS]`

**External task:** Native-speaker verification cannot be completed by Sonnet or Opus. Flag as external dependency. Assign to project lead for procurement.

---

## Verification Protocol (ongoing)

### At research time (multilingual-research mandate — CO-0006)
Every alias recorded in a search-log `native_aliases` block must carry one of:
- `[CLEAN]` — from Keyword Compendium or prior verified search
- `[PARTIAL — {reason}]` — documented boundary mismatch; deviation recorded
- `[INLINE-GENERATED]` — LLM-generated; remediation required
- `[VERIFIED-{method} {YYYY-MM-DD}]` — formally verified; method stated
- `[UNVERIFIED]` — CO-0005 expansion languages only; pending verification

No alias may be written without a status tag. UNTAGGED = error; research-log-manager LOG will BLOCKER.

### Verification tracking
This document is the tracking record. Update the tables below when verification events occur.

#### Completed verifications
| Date | Language | Slug | Old status | New status | Method |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

#### Outstanding external requests
| Date requested | Language | Contact | Method | ETA |
|---|---|---|---|---|
| 2026-04-08 | AR, HI, ID, SW, BN | Project lead | Native speaker / published standard | TBD |

---

## Integration with research-log-manager

From CO-0006, research-log-manager LOG action validates:
- All `native_aliases` entries have a status tag (missing tag = BLOCKER)
- INLINE-GENERATED tags trigger a warning (not a BLOCKER; researcher must confirm acceptable)
- UNVERIFIED tags (CO-0005 languages) are accepted with a `[UNVERIFIED-TERMS]` flag propagated to all retrieved sources

