# Native Alias Verification Tracking Document
**Created:** 2026-04-08 · Phase 1C · CO-0006
**Basis:** Extraction from 91 search-log entries (70 with aliases, 21 without — legacy format or index files)
**Purpose:** Track verification status of native search terms across all 19 languages. Identify terms requiring native-speaker or glossary verification.

---

## Methodology

Native aliases carry one of the following flags:
| Flag | Meaning | Action required |
|---|---|---|
| `[CLEAN]` | Accepted by researcher at search time | Low priority — verify for high-priority languages |
| `[PARTIAL]` | Accepted with boundary divergence noted | Review divergence; confirm terms are still best available |
| `[INLINE-GENERATED]` | LLM-generated at search time, not reviewed | HIGH PRIORITY — verify before next search run on this slug |
| `[UNVERIFIED]` / `[UNVERIFIED-TERMS]` | CO-0005 expansion languages — explicitly unverified | Verify before removing flag |
| `[NO-FLAG]` | No flag recorded — pre-flagging convention or legacy entry | Treat as UNVERIFIED; add flag on next touch |

**Verification methods (in priority order):**
1. Published glossary or terminology list from a national standards body document (e.g., DIN 18040 terminology, AFNOR glossary) — record as `[VERIFIED-GLOSSARY]`
2. Native-speaker review by qualified professional — record as `[VERIFIED-NATIVE]`
3. Cross-checked against multiple published sources — record as `[VERIFIED-CROSS]`

---

## Status Summary by Language

| Lang | Language | Total slugs | CLEAN | PARTIAL | INLINE-GEN | NO-FLAG | UNVERIFIED | Priority |
|---|---|---|---|---|---|---|---|---|
| SV | Swedish | 69 | 19 | 6 | 1 | 43 | 0 | P2 — INLINE-GEN present |
| NO | Norwegian | 68 | 20 | 6 | 1 | 41 | 0 | P2 — INLINE-GEN present |
| DA | Danish | 67 | 19 | 8 | 1 | 39 | 0 | P2 — INLINE-GEN present |
| FI | Finnish | 67 | 19 | 8 | 1 | 39 | 0 | P2 — INLINE-GEN present |
| FR | French | 67 | 20 | 6 | 1 | 40 | 0 | P1 — national standards body |
| DE | German | 69 | 24 | 3 | 1 | 41 | 0 | P1 — national standards body |
| ZH | Chinese | 66 | 13 | 14 | 1 | 38 | 0 | P1 — national standards body |
| JA | Japanese | 67 | 14 | 12 | 1 | 40 | 0 | P1 — national standards body |
| NL | Dutch | 39 | 22 | 3 | 1 | 13 | 0 | P2 — INLINE-GEN present |
| ES | Spanish | 37 | 19 | 8 | 1 | 9 | 0 | P2 — INLINE-GEN present |
| PT | Portuguese | 37 | 22 | 5 | 1 | 9 | 0 | P2 — INLINE-GEN present |
| KO | Korean | 36 | 14 | 12 | 1 | 9 | 0 | P1 — national standards body |
| IT | Italian | 31 | 19 | 8 | 1 | 3 | 0 | P2 — INLINE-GEN present |
| EN | English | 43 | 1 | 0 | 0 | 42 | 0 | P2 — INLINE-GEN present |
| AR | Arabic | 0 | 0 | 0 | 0 | 0 | 0 | P1 — CO-0005 UNVERIFIED |
| HI | Hindi | 0 | 0 | 0 | 0 | 0 | 0 | P1 — CO-0005 UNVERIFIED |
| ID | Indonesian | 0 | 0 | 0 | 0 | 0 | 0 | P1 — CO-0005 UNVERIFIED |
| SW | Swahili | 0 | 0 | 0 | 0 | 0 | 0 | P1 — CO-0005 UNVERIFIED |
| BN | Bengali | 0 | 0 | 0 | 0 | 0 | 0 | P1 — CO-0005 UNVERIFIED |

**Note on NO-FLAG count:** Many slugs use legacy search-log format where aliases are embedded in narrative text without structured flags. These are treated as UNVERIFIED until reviewed.

---

## P1 — CO-0005 Expansion Languages (AR/HI/ID/SW/BN)

These languages were added in CO-0005 with explicit `[UNVERIFIED]` status. All retrieval using these terms must carry `[UNVERIFIED-TERMS]` until verified.

**Current state:** 0 slugs have extracted aliases for these languages — they have not yet been used in search runs. The keyword compendium contains provisional terms only.

**Action required:**
1. Before any multilingual-research run using AR/HI/ID/SW/BN: confirm provisional terms in keyword compendium against at least one published accessibility glossary in that language
2. Record verification source in keyword compendium under each language's entry
3. Update flag to `[VERIFIED-GLOSSARY]` or `[VERIFIED-NATIVE]` once confirmed

**Verification targets by language:**
| Lang | Primary terminology sources to check |
|---|---|
| AR | مواصفات إمكانية الوصول — Saudi SBC, Egyptian standard ECP 306, CRPD Arabic text terminology |
| HI | भारतीय अभिगम्यता मानक — Harmonised Guidelines 2021 (MoHUA Hindi version), Rights of PwD Act 2016 Hindi text |
| ID | SNI 03-1746-2000 Indonesian terminology; Peraturan PUPR 14/2017 glossary |
| SW | Tanzania/Kenya national building code accessibility provisions; CRPD Swahili ratification text |
| BN | BNBC 2020 Bengali terminology; Bangladesh national standards |

---

## P1 — High-Priority Languages (DE/FR/JA/ZH/KO)

These languages have national standards bodies publishing accessibility terminology. Terms should be verified against those documents before the next search run.

### FR — French
**Verification source:** Arrêté du 8 décembre 2014 glossary; CEREMA accessibility guide terminology; NF P98-351
**INLINE-GENERATED slugs (1):** threshold-door-hardware
**PARTIAL slugs (6):** MOB, OFS, reach-range-and-accessible-controls, cross-population-case-studies, ofs-built-environment, mobility-built-environment
**NO-FLAG slugs (40):** treat as unverified; add flag on next touch
**Verification status:** `[UNVERIFIED]` — pending glossary check

### ZH — Chinese
**Verification source:** GB 50763-2012 terminology section; GB/T 37239 glossary; CDPF standard terminology list
**INLINE-GENERATED slugs (1):** threshold-door-hardware
**PARTIAL slugs (14):** ALL-ROOMS, DBL, DEAF, OFS, accessible-bathroom-and-grab-bar, deaf-spatial-design, reach-range-and-accessible-controls, residential-entry-and-threshold, threshold-and-level-access, cross-population-case-studies…
**NO-FLAG slugs (38):** treat as unverified; add flag on next touch
**Verification status:** `[UNVERIFIED]` — pending glossary check

### JA — Japanese
**Verification source:** MLIT 建築設計標準 2021 glossary; JIS X 8341 terminology; Housing Performance Indication System
**INLINE-GENERATED slugs (1):** threshold-door-hardware
**PARTIAL slugs (12):** DBL, DEAF, MOB, OFS, deaf-spatial-design, reach-range-and-accessible-controls, cross-population-case-studies, ofs-built-environment, pain-ofs-built-environment-design, deafblind-built-environment-design…
**NO-FLAG slugs (40):** treat as unverified; add flag on next touch
**Verification status:** `[UNVERIFIED]` — pending glossary check

### DE — German
**Verification source:** DIN 18040-1/2/3 terminology section; VDI 6008 glossary; nullbarriere.de standard term list
**INLINE-GENERATED slugs (1):** threshold-door-hardware
**PARTIAL slugs (3):** OFS, cross-population-case-studies, ofs-built-environment
**NO-FLAG slugs (41):** treat as unverified; add flag on next touch
**Verification status:** `[UNVERIFIED]` — pending glossary check

### KO — Korean
**Verification source:** 편의증진법 시행규칙 terminology; KS F 1952 accessibility terms; Seoul UD Guidelines 2022 glossary
**INLINE-GENERATED slugs (1):** threshold-door-hardware
**PARTIAL slugs (12):** DBL, DEAF, OFS, deaf-spatial-design, reach-range-and-accessible-controls, residential-entry-and-threshold, threshold-and-level-access, cross-population-case-studies, residential-accessible-home-case-studies, ofs-built-environment…
**NO-FLAG slugs (9):** treat as unverified; add flag on next touch
**Verification status:** `[UNVERIFIED]` — pending glossary check

---

## P2/P3 — Remaining 14 Languages

All original 14 languages have at least one `[INLINE-GENERATED]` slug (the threshold-door-hardware slug, which used inline generation for all languages). Otherwise the majority of terms are flagged `[CLEAN]` or `[PARTIAL]`.

**Recommended action:**
- On next touch of any slug with `[INLINE-GENERATED]` terms: replace with terms from keyword compendium (if compendium entry exists and is sourced) or flag for native review
- `[NO-FLAG]` entries: add `[CLEAN]` flag if terms appear reasonable, or `[INLINE-GENERATED]` if generation history is uncertain. Add flag during next LOG write.
- No mass-update required — first-touch migration applies

---

## Verification Protocol (Standing)

When a new search run is about to begin for any slug:
1. CHECK native_aliases in existing search-log entry
2. For any `[INLINE-GENERATED]` or `[NO-FLAG]` terms: consult keyword compendium Part 3 for this concept group
3. If compendium entry is sourced from a published glossary: use compendium term, record `[VERIFIED-GLOSSARY]`
4. If compendium entry is also INLINE-GENERATED: flag the search as carrying `[UNVERIFIED-TERMS]` and note in search-log
5. Update alias flag in search-log after run: `[CLEAN]` → `[VERIFIED-GLOSSARY]` or leave as `[CLEAN]` if no better source found

**Keyword compendium location:** multilingual keyword reference document (project files)

---

## Tracking Log

| Date | Language | Slug | Old flag | New flag | Verification source | Verified by |
|---|---|---|---|---|---|---|
| 2026-04-08 | ALL | — | — | — | Phase 1C extraction — baseline established | Sonnet 4.6 |

*Update this table as verifications are completed.*
