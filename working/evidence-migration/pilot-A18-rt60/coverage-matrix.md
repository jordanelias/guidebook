# Coverage matrix — `room-acoustic-performance` (pilot)

*Equity is measured by search effort + transparent yield, not parity (S6). This records what the corpus
actually holds for this slug, across jurisdiction and language, **including the empties and the mislabels**.*

## What the 32 linked sources cover

**By jurisdiction — 13 distinct (the reliable equity axis here):**

| tier band | jurisdictions represented |
|---|---|
| T1 clinical (16) | US ×11, INT ×3, UK ×1, IN ×1, IT ×1 — Anglophone-clinical dominated |
| T2 / T3 (5) | INT ×4, CA ×1 |
| T4–T6 standards (11) | US, UK ×2, JP, DA (Denmark), DE, AU/NZ, NO, FR, IT, CN — **broadly multi-jurisdictional** |

**By `lang_detected`:** 31 `en`, 1 `de`. **This tag is unreliable and understates multilingual coverage.**

## The key equity finding: language tags hide the multilingual evidence

Five of the linked standards are from non-Anglophone jurisdictions but are tagged `en`, because
`lang_detected` was produced by an automated `langdetect`/`corrected_short_text` pass run on the
**English-translated catalogue metadata**, not the source's home-language text:

| ref | jurisdiction | standard | `lang_detected` | true source language |
|---|---|---|---|---|
| REF-00572 | FR | *Guide acoustique pour personnes malentendantes* | `en` ✗ | French (title is French) |
| REF-00567 | JP | AIJES-S001-2008 | `en` ✗ | Japanese |
| REF-00575 | DA | SBi-anvisning 218 | `en` ✗ | Danish |
| REF-00564 | IT | UNI 11532-2:2020 | `en` ✗ | Italian |
| REF-00329 | DE | DIN 18041:2016 | `de` ✓ | German (correctly tagged) |

**Consequence:** the corpus-wide "~6× English" skew (measured by `lang_detected`) **overstates** Anglophone
dominance wherever non-English standards were catalogued in English — as here. For this slug, **jurisdiction
shows broad international coverage that the language tag erases.** Two honest actions follow:
1. **Trust jurisdiction over `lang_detected`** for equity accounting until the tags are re-derived from
   home-language source text (a corpus-wide hygiene item).
2. **State the limit (S3):** these non-English standards are currently read **via English metadata**, so any
   content that exists only in the original may be missed — an `inadequate` provenance on the *content*,
   even where the *bibliographic record* is fine.

## Where the base is genuinely thin or skewed (admitted)

- **Lived-experience (Co-1): absent** for this slug (`co1_pass_count=0`). Provenance-strength: `absent`.
- **Population evidence outside HI children is thin:** dementia RT60 = one T2 (provisional); autism = one T3
  (provisional). Provenance-strength: `inadequate` — stated, not dressed as settled.
- **The clinical T1 layer is US/Anglophone-concentrated** (11/16 US) — the *evidence* axis is skewed even
  though the *standards* axis is not.

## What a full 14×24 stratified search would target next (the program, not this run)

Not executed here (that is the batch work); named honestly so the empties are visible:
- **Un-migrated non-English acoustic sources already registered** (from L0): REF-00221 (JP, deafblind
  communication), REF-00218 (DE, DIN 18041 — likely renumber of REF-00329), REF-00001/REF-00031 (room
  acoustics / noise+reverberation SNR-50 at RT 0.3/0.6/0.8 s).
- **Home-language retrieval** of the FR/JP/DA/IT/NO standards' actual RT60 thresholds (the un-migrated
  code-floor values), each re-retrievable to a real record (anti-fabrication gate).
- **Non-Anglophone lived experience** of reverberant environments (DPO position papers, first-person
  accounts) — the corpus's most-skewed modality.
- **Under-represented jurisdictions** with strong barrier-free traditions absent here (e.g., KR, SE, NL
  building-acoustics standards).

Each row a full search adds will be recorded as `{language, jurisdiction, searched, found, best_tier,
has_precedent, note}` with empties kept.
