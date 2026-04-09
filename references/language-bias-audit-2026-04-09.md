# Language Bias Audit — Evidence Weighting
**Date:** 2026-04-09 22:11
**Model:** Sonnet 4.6
**Scope:** Full project — BPC files, skills, Part 1–4 body text, methodology documents
**Trigger:** User-directed audit: "there should have been no language weighting for evidence"

---

## Governing Principle (Part 1 §1.5)

> "Where sources conflict, higher-tier evidence governs regardless of jurisdiction, language, or number of citations."

This principle is correct. The audit identifies six categories where implementation deviates from it.

---

## FINDING 1 — "Languages confirming" Column Header (HIGH)

**~40+ BPC files + _template.md**

Every BPC consensus findings table uses `Languages confirming`. This framing implies a finding is established first (implicitly in English) and other languages merely "confirm" it. Evidence from each language is independent data.

**Fix:** Rename to `Languages with evidence` across all BPC files and template.

---

## FINDING 2 — Explicit "EN (primary)" Labels (HIGH)

Instances where English is explicitly labelled as primary evidence language:

- `room-acoustic-performance.md` L39: `EN (primary); IT (via UNI 11532-2)`
- `neurological-built-environment.md` L51 / `NEU.md` L56: `EN-primary evidence base for ABI wayfinding research`
- Evidence base audit L147: `EN, DE, SV primary`

**Fix:** Replace with tier-based classification. E.g. `Tier 1 (EN: Iglehart 2020); Tier 4 (IT: UNI 11532-2)`.

---

## FINDING 3 — "Non-English confirms" Framing (HIGH)

- `acoustics-speech-intelligibility-disability.md` + `ALL-ENV.md`: "Non-English language acoustic standards broadly confirm RT60 targets"

**Fix:** Replace "confirm" with "converge on" / "independently report consistent" / "also establish".

---

## FINDING 4 — Part 2 Co-1 Gap Disclosures Frame English as Default (MODERATE)

- §2.5 NEU: "Co-1 pass not run for non-EN languages"
- §2.6 DEM: "Co-1 extended pass not run for 9 languages"
- §2.10 DBL: "Co-1 evidence limited to US English-speaking Protactile community"

**Fix:** State which languages ARE completed and which ARE NOT. Not "EN done, non-EN not done" but "EN completed; DA, DE, ES, FI, FR, IT, JA, KO, NL, NO, PT, SV, ZH pending."

---

## FINDING 5 — §1.5 Source Lists EN-Dominated (MODERATE)

Primary Tier 1 sources list: CAOT, JOTA, COTEC/WFOT, AOTA, Housing Enabler, RCOT — all EN-publishing bodies.
Primary Co-1 sources: Kelsey, Gallaudet, Motionspot, ME Association — all EN.

**Fix:** Add non-EN exemplars at each tier. Already documented in multilingual-evidence-convergence BPC.

---

## FINDING 6 — EN-only Evidence Normalized Without Gap Flag (LOW-MODERATE)

- `OFS.md` L52: `evidence base is EN-only` — no gap flag or remediation plan.
- `PAIN.md` L13: same.

**Fix:** Add `[LANGUAGE GAP — EN-only. Non-EN passes pending. Confidence reduced for cross-jurisdictional applicability.]`

---

## FINDING 7 — Database Priority Note Missing (LOW)

multilingual-research skill Step 3: EN databases searched all runs; non-EN databases language-specific only.

**Fix:** Add note: "No database priority implies evidence priority. Sources carry identical tier authority regardless of indexing language."

---

## POSITIVE FINDINGS (No Remediation)

1. Part 1 §1.5 principle is language-neutral.
2. Evidence hierarchy methodology contains no language weighting.
3. Evidence-auditor flags "single-language for cross-jurisdictional claim" — language-neutral.
4. multilingual-evidence-convergence-non-english BPC documents 7 provisions where non-EN evidence is strongest.
5. multilingual-research synthesis instruction: "Group by concept cluster, not by language."
6. Part 4 body correctly foregrounds non-EN evidence where strongest (Marquardt DE, Japanese heat shock, Dutch De Hogeweyk, Danish loop garden).
7. BPC concept boundary tables track native aliases across 14 languages.

---

## REMEDIATION PLAN

| Finding | Severity | Method | Status |
|---|---|---|---|
| F1: Column header rename | HIGH | Batch find-and-replace | PENDING |
| F2: EN (primary) labels | HIGH | Manual edit (3-5 files) | PENDING |
| F3: "Non-English confirms" | HIGH | Manual edit (2-3 files) | PENDING |
| F4: Co-1 gap disclosures | MODERATE | Manual edit Part 2 | PENDING |
| F5: §1.5 source lists | MODERATE | Manual edit Part 1 | PENDING |
| F6: EN-only normalization | LOW-MOD | Manual edit + gap register | PENDING |
| F7: Database priority note | LOW | 1-line addition to skill | PENDING |

