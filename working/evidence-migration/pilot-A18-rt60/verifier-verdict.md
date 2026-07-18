# Verifier verdict — A-18 (RT60)

**Status: COMPLETE. The adversarial verifier caught real errors in the first draft; they are corrected
below and in the other pilot artifacts.** A separate, independent, guilty-until-proven agent re-queried the
canonical DB and re-retrieved the ANSI figure from the open web. This is the anti-fabrication / anti-overclaim
gate working as designed — the writer did **not** certify its own grounding.

## Per-claim verdict

| claim | verdict | note |
|---|---|---|
| C1 · DEAF/0.3 s cell exists as described | **CONFIRMED** | cell_id 9008, population_code=DEAF, stated, T1, governing_refs exact |
| C2 · the four governing refs are real, Tier-1, on-topic | **CONFIRMED — no fabrication** | Iglehart 2020/2016, Neuman 2010, Wroblewski 2012 — all VERIFIED, web-corroborated |
| C3 · ALL/0.55–0.57 s universal cell exists | **CONFIRMED** | cell_id 9009 |
| C4 · ANSI/ASA S12.60 = 0.6 s for ≤283 m³ | **CONFIRMED — but *unoccupied*, furnished** | the occupancy basis matters (see C5) |
| C5 · "build to ANSI 0.6 s → HI children at ~2× → an instance of V-01" | **OVERCLAIMED — corrected** | three errors, below |
| C6 · "the DB does not store the code threshold values" | **REFUTED — corrected** | it does (`source_value_extractions`) |

## What was wrong, and the correction (accepted in full)

1. **Code-floor values are NOT un-migrated (C6).** They live in `source_value_extractions` (8 rows for this
   slug) and `spec_value_probes` (13 PMP-walk rows), with `echo_of` provenance: ANSI 0.6 s (ALL) / **0.3 s
   (DEAF, Footnote e)**, BB93 0.6–0.8 s, DIN 0.4–0.8 s, UNI 0.5 s, AS/NZS 0.4–0.6 s. My "un-migrated
   code-floor values" gap was **false** — I checked only `evidence_sources.bpc_note`, not the dedicated
   extraction tables. Corrected everywhere.

2. **`population_code` is NOT null.** The cells carry DEAF / ALL / DEM / AUT. I read the wrong column
   (`population`, which is unused) and falsely declared a null-population gap. Corrected.

3. **ANSI does not floor hearing-impaired children at 0.6 s — it specifies 0.3 s for them (Footnote e).**
   The DB records this correctly, as an **echo of the Iglehart evidence, not an independent code root**
   (`source_value_extractions.echo_of`). So the sharp "convergence ≠ evidence" example I built — "the code
   floor is 2× laxer than the evidence for HI children" — was **wrong**: for HI children the code
   *converges with* the evidence. The real, narrower point that survives: the code's **general** minimum
   (0.6 s, typical-hearing, *unoccupied*) must not be misapplied to an HI space — but ANSI's own population
   provision already prevents that, so it is a **susceptibility if the wrong provision is applied**, not a
   code-vs-evidence conflict.

4. **Occupied vs unoccupied.** A-18 is defined for *occupied* spaces; ANSI 0.6 s is *unoccupied/furnished*.
   The DB's PMP-A18-002 walk already puts the general value on the right basis (0.55 s, Prodi 2022 occupied
   dose-response). My raw "2×" mixed bases. Corrected.

5. **"An instance of V-01" → "a susceptibility to V-01."** Minimum-compliance weaponization needs an actor
   invoking compliance to deny the target; the bare structural gap is an attack surface, not a demonstrated
   instance. Corrected in `ethics-screen.md`.

## What survives verification (real, confirmed)

- **No fabrication** anywhere in the derivation — all governing refs resolve to real, Tier-1, on-topic,
  VERIFIED papers.
- **Co-1 lived experience is genuinely absent** — all four `convergence_assessment` rows are `single_axis`
  clinical, `co1_sources=[]`; `co1_pass_count=0`. A real gap.
- **Real DB-flagged data errors** (surfaced, not invented): (a) `item_population_elaborations` elab_id=6
  mis-cites Devos 2019 as **REF-00571**, which is actually *Kotloski 2020, a genetics paper*; the real
  Devos 2019 is **REF-00735** (unlinked). (b) **Four duplicate ANSI-2010 records** — REF-00326, -00335,
  -00563, -00604 — flagged for dedup.
- The DEM (0.5 s) and AUT (0.4 s) values are **honest conjectures** — the PMP walks record strict-termination
  **FAIL by design**, labeling them as literature-informed conjectures, not Tier-1 thresholds. The
  extrapolation/thin-base admission is already done correctly in the DB.

## The meta-finding this produced

My first draft under-inventoried the schema and reported gaps that were already filled. The lesson —
folded into the plan — is **inventory the existing substrate before running the pipeline**: A-18 already
carries `source_value_extractions`, `spec_value_probes`, `convergence_assessment`, and RDC records from the
July 2026 sessions. The migration must *build on* that, not re-derive it or mis-report it as missing.
