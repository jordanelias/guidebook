# A-02 · Acoustic Ceiling Panels (NRC ≥ 0.85) in Occupied Spaces
**Complete best-practice provision — both halves: performance target + design technique.**
Category A (room acoustic performance) · slug `room-acoustic-performance` · pilot: technique-layer, 2026-07-16.
Status: WORK IN PROGRESS — held behind the PROVISIONAL banner; evidence-graded, not published as authority.
Adversarially reviewed 2026-07-16 (APPLY-WITH-FIXES): STI conflict disclosed, low-frequency physics corrected, paywalled-standard marker downgraded, single-site caveat restored.

---

## The question a designer arrives with
"The ceiling is the biggest hard surface in the room and it's smearing speech into reverberation. Panels are the obvious fix — how do I do it so it actually helps, and doesn't quietly make listening *worse*?"

That last clause is the whole point of this record. The naive technique (hang the highest-NRC tile you can buy) is a documented way to *degrade* intelligibility. Best practice is not the number; it is the number **plus** how you achieve it.

---

## 1 · Performance target — REQUIRED (but one figure is contested)

| Metric | Target | Status | Basis |
|---|---|---|---|
| **NRC** (panel) | ≥ 0.85 | ◐ industry-consensus | `PMP-A02-001` empirical ceiling 0.935 → NRC ~0.90 to meet ANSI/ASA S12.60 RT-adaptability. This is engineering guidance (e.g. Armstrong) on hitting the RT target; the standard's own text was **not** opened (REF-00335 paywalled). |
| **STI** (listener position) | **CONTESTED** | ⚠ unresolved | The room's real performance criterion is STI *at the seat*, not room-average — but its value is disputed: this corpus carries a flat **STI ≥ 0.5** and a two-tier **≥ 0.60 general / ≥ 0.75 DEAF-CI** in different files. Flagged Q24, pending Phase E.2g adjudication; the source BPC is `PRE-REHABILITATION — RETRACTED`. Do not treat either figure as settled. |
| **absorption spectrum** | broadband, per-octave 250 Hz–4 kHz | required qualifier | The single NRC number hides spectral skew (§4). Specify per-octave, not just NRC. |

**The correction that makes this honest:** NRC ≥ 0.85 is **necessary but not sufficient** (the project's own GAP-RAP-01: the bare "NRC ≥ 0.85 = primary treatment" claim is *underclaimed* — correct but incomplete). STI at the listener position is the criterion in principle; its *value* is unresolved in this corpus and must not be asserted as settled.

## 2 · The design technique — how you ACHIEVE it

**Ceiling absorption is the primary acoustic treatment** — it is the largest available surface and the most consistent recommendation across BB93 (UK), ANSI/ASA (US) and DIN 18041 (DE). But "primary" is not "sufficient on its own." Best practice is four moves, not one:

1. **Absorb broadband, not just treble.** The failure Amlani & Russo measured came from panels whose absorption was *high-frequency-dominant* — they soaked up the consonant band while leaving lower frequencies live, so aggregate NRC rose while consonant contrast fell. The primary lever for broadband (not treble-skewed) absorption is **panel thickness and the air-gap / plenum depth behind it** — a thicker panel, or one spaced off the deck, reaches lower frequencies; material chemistry (mineral fibre vs glass wool) is a *secondary* refinement, not the main dial. Specify the **absorption spectrum per octave 250 Hz–4 kHz**, not just the single NRC.
2. **Design to the seat, not the room.** Amlani & Russo's degradation was worst *beyond the critical distance* — verify STI/absorption at representative listener positions, especially far seats, not a room average that hides spatial loss.
3. **Pair the ceiling with first-reflection wall treatment** (A-06 fabric panels) where speech targets are tight; the ceiling alone leaves lateral reflections.
4. **Complement, don't substitute for, personal systems.** In high-RT rooms a ceiling sound-field underperforms a personal/desktop FM (Iglehart 2004; Anderson & Goldstein 2004) — treatment and assistive listening are complementary, not alternatives.

## 3 · Products — manufacturer-neutral

| Product type | Typical NRC (varies by thickness/mounting) | Low-frequency note | Use |
|---|---|---|---|
| Glass-wool / fibreglass tile | 0.85–0.95 | reaches lower frequencies at adequate thickness/air-gap | general speech-critical absorber |
| Mineral-fibre lay-in tile | 0.55–0.70 std; high-NRC lines to ~0.90 | thinner lines skew treble → the Amlani-Russo risk; add thickness/air-gap | acceptable with spectrum verified |
| Rock-wool / mineral-wool | ≥ 0.85 at thickness | broadband when thick | good absorber |
| Hybrid mineral + soft-fibre | to ~0.90 (+ CAC ≥ 40) | broadband + blocking | where sound *isolation* also needed |
| Wood-wool / wood-fibre | 0.60–0.80 | mid-dominant, aesthetic | supplement / feature, not primary |

*Coverage & mounting:* the **dominant low-frequency lever is thickness + plenum/air-gap depth** — a ~25 mm tile tight to the deck is treble-skewed; ~50 mm and/or a deep plenum reaches lower frequencies. Size coverage to hit the room's RT60/STI target, not a fixed percentage.

## 4 · Failure modes — the ones that actually happen

- **NRC-compliant but STI-degrading.** High-frequency-dominant panels (thin, treble-skewed) can bring a room into ANSI RT compliance while *decreasing* speech-signal transmission and *increasing* listening effort — word-recognition and digit-recall both fell in Amlani & Russo's Grade-3 classroom (STI decrease measured qualitatively). **This is the headline failure this record exists to prevent.**
- **Room-average blindness.** A single room-average passes while distant seats fail; spatial/spectral degradation hides behind the single number.
- **Substitution error.** Panels *instead of* personal FM in a high-RT room — the ceiling system underperforms the desktop one (Iglehart 2004).
- **Over-damping.** Pushing RT very low can reduce hearing-aid directional-microphone utility (Wu & Bentler 2012) — more absorption is not monotonically better, so chase the room's RT/STI target, not the panel's headline NRC.

## 5 · Functional-capacity mapping — one technique, four routes

The technique serves a single functional capacity — *maintaining auditory signal clarity under reverberation* — that appears across disability groups through different routes:

| Population | Why absorptive ceiling serves them | Population-specific note |
|---|---|---|
| **Deaf / HoH** (device users) | devices amplify reflected energy along with direct speech; cutting reverberation restores the direct-to-reverberant ratio | complement with FM/SFA; avoid over-damping (directional utility) |
| **Autism / NDV** | broadband absorption suppresses flutter echo, reflective peaks and sudden-onset reverberant energy that drive sensory load | pair with *no sound masking* (A-13) and gradient zoning |
| **Dementia** | reverberant complexity raises cognitive load → agitation; acoustic calm is a therapeutic target | one **single-site** POE reported ~40 % agitation reduction post ceiling install (Lyngby-Taarbæk, T2) — compelling but not replicated |
| **Post-concussion / phono-sensitive** | lowers the reverberant noise floor | absent from acoustic standards — **THIN-BASE** |

## 6 · Evidence & honesty trail

- **Verified at source (this session):** Amlani & Russo 2016 (T1, PMID 27885976; DB REF-00580, VERIFIED) — high-frequency-dominant panels reduced speech-signal transmission and raised listening effort, worst beyond critical distance, despite meeting ANSI RT. (The record is *more* faithful than the source BPC's own text, which mis-states this as panels "improving STI.")
- **In-project, cited (section-level re-read pending):** Wu & Bentler 2012 (T1, over-damping vs HA directional), Iglehart 2004 (T1, desktop > ceiling SFA in high RT), Anderson & Goldstein 2004 (T1, ceiling SFA no benefit vs HA at RT 1.1 s), Lyngby-Taarbæk POE (T2, DEM, single-site).
- **Performance target:** `PMP-A02-001` NRC → ~0.90 (walk clean); ANSI/ASA S12.60 (T4) — **standard text not opened (paywalled REF-00335)**; the 0.90 figure is industry consensus, not a verified clause.
- **The physics correction (this review):** low-frequency absorption is governed primarily by thickness + air-gap, not fibre chemistry — the earlier draft over-weighted material and over-attributed the fix to Amlani & Russo. Corrected.
- **Grade:** the *bare* "NRC ≥ 0.85 = primary treatment" claim is **provisional / underclaimed**. The *refined* technique (broadband absorption via thickness/air-gap + per-octave spectrum + seat-position verification + complement personal systems) is evidence-**informed** best practice, anchored on the T1 counter-finding that disciplines it — held provisional pending the Q24 STI adjudication and reverification of the retracted source BPC.

## 7 · Trade-offs & cross-references
- **NRC (means) vs STI (criterion)** — the core tension; resolved by specifying the absorption spectrum + STI at position, *not* by maximizing NRC.
- **Ceiling absorption vs HA directional utility** — do not over-damp (Wu & Bentler).
- **A-06** fabric wall panels — first-reflection complement.
- **A-05** carpet — alternative absorption, trades against VIS-navigation contrast + infection control.
- **A-13** no sound masking — contraindicated for NDV/DEM; do not "cover" residual reverberation with masking.
