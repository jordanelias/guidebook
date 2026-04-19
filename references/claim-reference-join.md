# Claim-to-Reference Join Table
<!-- Generated 2026-04-19 — Step 3 of citation infrastructure -->
<!-- Session 1 of Step 2 (Part 4 Category A acoustics) complete 2026-04-19 -->

**Purpose:** Traceable mapping from each specification claim in Parts 1-12 to the references that support it. Phase B parsers read this table to render footnotes on the frontend.

**Total claims enumerated:** 1382

**Overall status:**
- PENDING (untagged): 1309
- TAGGED (refs assigned): 45
- VERIFIED (confirmed): 0
- DEFERRED (non-citable: methodology, definitional, echo): 17
- ORPHANED (no supporting ref in global registry): 11

**Full machine-readable data:** `references/claim-reference-join.json`

---

## Progress by Part

| Part | Total | PENDING | TAGGED | VERIFIED | DEFERRED | ORPHANED |
|---|---|---|---|---|---|---|
| Part 1 | 7 | 7 | 0 | 0 | 0 | 0 |
| Part 2 | 83 | 83 | 0 | 0 | 0 | 0 |
| Part 3 | 42 | 42 | 0 | 0 | 0 | 0 |
| Part 4 | 558 | 485 | 45 | 0 | 17 | 11 |
| Part 5 | 79 | 79 | 0 | 0 | 0 | 0 |
| Part 6 | 115 | 115 | 0 | 0 | 0 | 0 |
| Part 7 | 111 | 111 | 0 | 0 | 0 | 0 |
| Part 8 | 116 | 116 | 0 | 0 | 0 | 0 |
| Part 9 | 10 | 10 | 0 | 0 | 0 | 0 |
| Part 10 | 23 | 23 | 0 | 0 | 0 | 0 |
| Part 11 | 191 | 191 | 0 | 0 | 0 | 0 |
| Part 12 | 47 | 47 | 0 | 0 | 0 | 0 |

---

## Session Log

### Step 2 Session 1 — Part 4 Category A (acoustics) — 2026-04-19 ✅

- **Scope:** 73 claims across A-01 to A-17
- **Results:** 45 TAGGED, 17 DEFERRED, 11 ORPHANED
- **Primary references used:** REF-00142 (Bettarello 2021), REF-00157 (PAS 6463:2022), REF-00151 (BS 8300-2:2018), REF-00218 (DIN 18041:2016), REF-00126 (ANSI S12.60), REF-00289 (IEC 60118-4), REF-00302 (ISO 2631), REF-00305 (ISO 10137), REF-00041 (Staud 2011), REF-00273 (HLAA Auracast), REF-00167 (CAOT ABI 2024)
- **ORPHANED flagged (require Phase B content review):**
  - A-04 L160 20m restorative interval — Kaplan 1989 cited but outside acoustic BPCs
  - A-09 L340 0.1 m/s RMS vibration threshold — UNVERIFIED, likely BS 6472-1:2008 (GAP-IMPL-05)
  - A-13 L516 De Hogeweyk 94% / 34% — Dutch grey lit not in global registry
  - A-16 L639 Uhthoff 30-60 min recovery + ≤16°C / ≤20°C MS cooling — Leavitt 2014, Davis 2010 cited in Part 4 but not in global registry (MS BPC has Staud 2011 only)
- **DEFERRED categories:**
  - Measurement-frequency references (500 Hz, 1000 Hz — standard methodology per ISO 3382-2)
  - Construction tolerances (3mm undercut)
  - OT evidence echo text (repeats spec values already tagged upstream)
  - Category B metadata misextracted to A-17 scope (1200mm/850mm/1500mm eye-level figures)

### Next session (Session 2): Part 4 Category B-C (lighting, surfaces) — ~100 claims

---

## Status values

| Status | Meaning |
|---|---|
| `PENDING` | Not yet tagged (default) |
| `TAGGED` | Ref IDs assigned; first pass complete |
| `VERIFIED` | Second-pass check: cited refs genuinely support claim |
| `ORPHANED` | No supporting reference found in global registry — Phase B content review required |
| `DEFERRED` | Not a citable claim (definitional, cross-ref, measurement methodology, or extractor artifact) |

---

## How to populate `ref_ids` (Step 2 instructions)

For each claim:
1. Identify which BPC file(s) cover the topic area
2. Look up the claim's source in that BPC's Key sources table
3. Find the matching global REF-ID in `global-reference-registry.md`
4. Add the REF-ID(s) to this claim's `ref_ids` field (array, multiple allowed for primary + supporting)
5. Set `status: TAGGED`
6. For cross-referenced claims or measurement methodology, set `status: DEFERRED` with a note
7. For claims citing sources not in the global registry, set `status: ORPHANED` and log the citation gap

**Priority order per claim:**
- Tier 1–2 sources cited first
- Multiple refs allowed (primary spec source + supporting clinical evidence + governing standard)

**Verification:** After tagging, a second pass can set `status: VERIFIED` for claims where the cited ref genuinely supports the stated value (not just same topic area).
