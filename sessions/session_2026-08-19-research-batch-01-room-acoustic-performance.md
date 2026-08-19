# session_2026-08-19-research-batch-01-room-acoustic-performance

**Purpose.** DR-2026-08-19 §3 step 4 — the first research batch after the restart, on
`room-acoustic-performance`, under the §1.4 quarantine and the R1–R15 contract. This is the
session the §4 acceptance criterion was written for.

**This IS a research session.** Both `sessions/LATEST` and `sessions/LATEST-RESEARCH` are moved
to it. `evidence_sources` went 0 → 5, so **the §2.2 freeze lifted by its own terms** — no repeal,
no ceremony, exactly as §11 property 1 specified.

**Scope held at §12.2 minimum viable**, deliberately: 9 searches, 77 screened, 5 admissions,
3 candidates, 12 population matches, 5 mining rows. The step-7 enrichment was hand-written this
time and a failed batch of 30 remediates far worse than one of 5.

---

## 1. The owner's two interventions, and what each changed

**(a) "AX???? we declared using ICF codes with name."** My step-2 frame pull printed bare
`axis_code` values and counts. Corrected, the frame reads:

| Axis | ICF anchors | Mechanism | Items |
|---|---|---|---|
| AX-AUD Auditory access & alerting | b230; d310, d115 | speech access, alert receipt | 13 |
| AX-SPR Sensory-load | b156, b140; d230, d160 | stimulus intensity, unpredictability, trigger exposure | 9 |
| AX-PAI Pain-load | b280; d410, d450, d640 | impact, vibration, pressure, cold | 2 |
| AX-VIS-N Non-visual information | b210; d460 | legible without vision | 1 |

**Four of my first five searches were framed on AX-AUD alone.** The ICF anchors are what made the
second mechanism visible: AX-SPR is a different question (b156 perceptual / b140 attention) that
speech-intelligibility queries cannot reach. exec 6 opened that seam and produced two of the five
admissions. Had the frame been pulled as declared, this would have been visible before searching
rather than after.

**(b) "requirement-class first."** Ruled after I put the choice. It decided what I screened *for*:
what KIND of requirement each axis imposes, before any number. §5 below is why it mattered.

## 2. What was admitted

| ref_id | Source | Tier / type | Axis |
|---|---|---|---|
| REF-00965 | Rosas-Pérez et al. 2025, *Applied Acoustics* | T1 **co1** | AX-AUD + AX-SPR |
| REF-00966 | MacLennan et al. 2023, *Autism in Adulthood* | T1 **co1** | AX-SPR |
| REF-00967 | Bagheri et al. 2024, *Building and Environment* | T1 clinical | AX-SPR |
| REF-00607 | Tsironis et al. 2024, *Trends in Hearing* | T2 sr_meta | AX-AUD |
| REF-00968 | Wright et al. 2026, *Cogent Social Sciences* | T1 **co1** | AX-SPR |

**R1 was satisfied first and genuinely**: 4 Co-1-targeted searches, 3 Co-1 sources admitted, 0 waivers.

**Population grading is honest, not decorative**: 12 rows, of which only **3 EXACT** — 4 PARTIAL,
3 PROXY, 2 MISMATCH. The T2 anchor is PROXY against every population this slug serves, because its
population-of-study is normal-hearing listeners.

## 3. Three defects in the instrument, found by running it

1. **The runbook's ref_id example is a trap.** §12.1 mints `REF-00001`. The stash occupies
   `REF-00002`–`REF-00964`, so `REF-00001` happens to be free and the example WORKS — while the
   next four ids a session would reach for are all taken by unrelated papers. The trap stays
   hidden until the second admission, then silently conflates sources. Minted above the
   high-water mark instead (REF-00965+).
2. **§6 is not optional, and it is already load-bearing.** Tsironis's DOI was already held as
   **REF-00607** (`recovered_from corpus-pre-reset-2026-08-06`). The R9 gate queries
   `evidence_sources` only and **passed it clean**. I promoted the lead rather than minting a
   twin — but only because I checked the stash by hand. Every one of the **9 REF-ids cited by the
   predecessor reasoning doc is likewise in the stash and absent from `evidence_sources`.**
3. **R2 and RULE 124 are different obligations.** R2's floor is `admissions//4`; the blocking
   `citation_mining_session` gate demands a row per confirmed T1–T2 source. The batch met the
   first and failed the second. Both now satisfied — five real Crossref chases, not deferrals.

## 4. A regression I caused, and fixed forward

The batch took `test_db_integrity` **72/72 → 67/72**: I1, C03, C08, G02 all failed because
`db.py add-source` cannot write `first_author_last`, `evidence_source_authors`,
`verification_disposition` or `citation_mining_status` — the `_ES_COLS` whitelist §12.0 names.
Two compensating migrations restored **72/72**. Data migrations are immutable; nothing was edited.

## 5. The finding — requirement class, not level

Steps 1–11 were completed before `references/bpc-reasoning/room-acoustic-performance.md` was
opened, per §1.4 rule 5. On release, the comparison:

**Converges.** The predecessor states no Tier-1 quantified RT60 threshold exists for NDV/AUT. My
batch reached the same conclusion blind and by a different route: the controlled seam remediates
the *listener* (auditory training, cochlear implants), not the *room*, and the one on-parameter T2
review studies normal-hearing listeners. Two independent paths, same absence.

**Diverges, and this is the substantive result.** The predecessor's parameter header asserts an
accessibility direction: *"LOWER is more inclusive — less reverberation = better speech
intelligibility for hearing-impaired, lower sensory load for NDV/AUT, less agitation trigger for
DEM."* The Co-1 evidence admitted this batch contests that for **two** of those three populations:

- **NDV/AUT** — Wright 2026 (REF-00968): themes *Acoustical Control as Cognitive Safety* and
  *Restoration is Not Silence*; imposed silence was experienced as emotionally taxing, and
  predictability plus personal control ranked **above level**. Rosas-Pérez 2025 (REF-00965):
  *"Agency is crucial."*
- **DEM** — the lived-experience literature centres sound as social resource and meaning, and
  explicitly resists *"narrow conceptualisations of sound as unwanted noise that must be reduced."*
  (Logged at exec 2; off-parameter for admission here, and a finding in its own right.)

So the predecessor answers a question of **level** where the Co-1 evidence poses a question of
**class**: for the sensory-load axis the requirement looks like *control and predictability*, not
*a lower number*. A value-first batch would have screened for thresholds and never surfaced this.
That is the requirement-class-first ruling earning itself on its first use.

**No determination is authored here.** This session admits evidence and records the contest.
Writing `best_practice_synthesis` sits at the Opus floor behind the B-before-E gate and is not
this batch's work.

## 6. Recorded absences, not silences

- **SCI × room acoustics, Co-1**: 20 results, **zero** addressing the intersection — the engine
  returned both literatures separately. R14 diagnosis: not query-shape failure, not wrong index,
  **genuine absence**. SCI carries 1 item on this slug and has no lived-experience base for it.
- **AX-PAI**: deliberately not searched. Its mechanism is impact/vibration/pressure — structure-borne,
  not airborne. Searching it under this slug would have imported the wrong mechanism. Reasoned
  deferral under R6, not a coverage gap.
- **R8/R14 passed without a subject.** No search returned `results_found=0` this batch. The SCI
  search returned 20 rows, none on target, and I recorded it as 20/20/0 rather than dressing it as
  a zero-yield to give those two rules something to chew on. Disclosed rather than manufactured.
- **DIN 18041** is located and on-topic (its 2016 revision was prompted by accessibility
  requirements) but every number reaching me came from secondary commentary. `[UNVERIFIED-QUANT]`;
  no value recorded. The `jurisdictional_values` backfill §12.2 anticipated did not happen, because
  R3 forbids it without a clause.

## 7. Method proposal, recorded not executed

The owner proposed deriving required design values and then researching products/solutions that
achieve them. Endorsed with the ordering amended to **requirement-class → value → solution**, for
the reason §5 demonstrates. Two constraints recorded: product and manufacturer data is not
evidence at full strength (test-lab data against a standard is regulatory stratum, weak band ○
only), and a single "required value" collapses the three Design Modes. No apparatus was built for
this — `specifications` is the values home and there is no solutions table; creating one was
frozen at the time and remains an owner decision.

## 8. State at close

`user_version` 60 unchanged. Three data migrations applied (one batch, two compensating). DoD
COMPLIANT exit 0 with non-zero subjects on every rule that has one. `citation_mining_completeness`
CLEAN, Examined 5. `test_db_integrity` 72/72. Rebuild reproduces every table count.

**OD-2 through OD-12 remain open.** Nothing gated behind them was executed. OD-5 (the §6 stash
widening) is now the highest-value open decision: this batch demonstrated the gate is blind to
835 held identifiers, and that the predecessor's entire citation set sits in that blind spot.
