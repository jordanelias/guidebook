# D/E-grade remediation + coverage extension — executable plan (2026-07-21)

**Status:** Active workplan. Prepared after the intensive week-audit + adversarial review (2026-07-21),
under the ratified product posture (`DR-2026-07-21-product-posture-thinking-tool-not-authority`):
the machinery **adjudicates the evidence** to surface the best-supported figure at a stated strength;
the end product presents figures for thought and never adjudicates the reader's conclusion. All work
below runs the **existing verify-each-source-re-retrieves pipeline**
(`working/evidence-migration/research-handoff-non-english.md` §2) — no new process. Migrations only
(`emit_data_migration.py` → `migrate_db.py`); every ingested source re-retrievable via a real tool call;
empties kept as findings; tier by `governance/tier-system.md`.

**Anti-displacement note (posture consequence #2, now in force):** this is adjudication-unblocking work,
so it is *permitted* under the freeze. Governance/attestation cycles that do not unblock an adjudication
slug wait.

---

## Part A — D/E-grade remediation, prioritized by what actually moves each slice

The audit's own diagnostics show the D/E pain is **overwhelmingly linguistic/jurisdictional breadth, not
tier** — and a large share is **already-searched hits that were never linked** (the cheapest, zero-
fabrication work). Tiers below are by remediation *type*, not just score.

### P1 — Identity-contradiction fixes (all 3 E-grade). Highest priority: a globally-scoped slug with zero global evidence is the sharpest credibility risk under a transparency posture.
| slice | grade | contradiction | fix |
|---|---|---|---|
| `co1-housing-research-global-south` | E 28.5 | 100% EN, INT-only, partial-band — global-south slug, **0 non-English sources** | link the corpus's real global-south rows (BR, ID, TH, MY…) + 2–3 genuine global-south housing instruments + 1 full-band anchor |
| `crpd-implementation-built-environment` | E 32.5 | INT:5 only, monojurisdictional, partial-band — treaty slug, no state-party diversity | 3–4 state-party jurisdictions + disability-studies Art.9 implementation evidence (full-band) |
| `residential-dar-provisions-priority-register` | E 33.0 | Anglo-only (UK/CA/INT), standards-heavy | non-Anglo DAR regimes + evidence beyond the register text |

### P2 — Cheap, high-ROI: full-band already, dragged only by language/anglo, where search yield already exists → relink already-verified rows, lowest fabrication risk. **Run this batch first.**
- `ofs-built-environment` (D 49.8) — full-band, **13 language-hits, 0 non-English linked** → relink.
- `luminance-contrast-lrv-evidence-base` (D 48.7) — full-band, 9 hits, 0 linked; sibling `luminance-contrast-and-pattern` is **100% non-English (13/13)** → borrow/relink from sibling (same topic, already verified).
- `accessible-laundry-room-design` (D 47.0) — partial-band, **14 language-hits** → link them (moves language + anglo), then seek 1 full-band anchor.
- `ot-cpg-built-environment` (D 49.6) — full-band but **2 DISPUTED sources** → replace them (also clears part of the 10-DISPUTED debt).

### P3 — Genuine full-strength evidence needed (real tier-lift research).
- `therapeutic-lighting-design` (D 43.4) — partial-band; full-band clinical exists via sibling `circadian-lighting-melanopic-edi` → anchor/borrow.
- `thermoregulation-built-environment` (D 44.1) — full-band but **monojurisdictional (INT:5)** → source a 2nd jurisdiction.
- `accessible-design-failures-poor-performance` (D 45.8) — full-band; needs non-EN/anglo balance (and is generative — see Part B).

### P4 — Accept as honest ◐ partial / genuine constraint. Flag, do NOT force full-band (posture-consistent).
- `government-grant-programmes-home-adaptation` (D 46.3) & `european-accessibility-act-scope-clarification` (D 45.4) — inherently policy/legal-instrument; full-band *clinical* evidence is a category error. Render standards-basis, flagged. Low grade is honest.
- `bariatric-turning-radius` (D 49.0) — documented genuine absence of non-English bariatric standards; accept Anglo-concentration transparently, flag applicability.
- `cross-population-case-studies` / `-conflict-resolutions` / `case-study-economics-financial-data` (D 44–48) — cross-cutting **meta-slices**; EN-concentration partly inherent (they aggregate the corpus). Lowest priority; flag global applicability.

---

## Part B — Coverage extension: missing regions/areas + the logic to keep finding them

### Verified regional gaps (checked against the corpus; Brazil NBR 9050 IS present — not a gap)
- **South Africa** — essentially absent (one `INT/ZA` row); SANS 10400-S is a major standard.
- **Philippines** — absent; BP 344 is a foundational SEA accessibility law.
- **Latin America beyond BR/CL** — Mexico, Argentina (Ley 24.314), Colombia — none present.
- **Francophone Africa, Pakistan/Sri Lanka/Nepal** — none.
- **Structural:** the "global-south" slugs are *hollow* — the corpus HAS global-south jurisdictions
  (BR, ID, TH, MY, EG, SA, NG, GH, BD) but they are **under-linked** to the global-south-labelled slugs.
  Extending global-south coverage is partly a **linking** problem, not only a search problem.

### Candidate technique gaps (verify against the item registry before creating slugs — flagged, not asserted)
Areas of refuge / accessible means of egress (visual-fire-alarm is *alerting* only); Changing Places /
adult-changing + ceiling hoist (distinct from bathroom/grab-bar); accessible parking / passenger drop-off /
exterior approach route (entry-threshold is the building edge, not the site); vertical circulation —
lifts / platform lifts / evacuation lifts (circulation-geometry is horizontal); slip-resistance /
floor-finish specification.

### The extension logic — a repeatable gap-finder (tied to adjudication: you can only adjudicate a "best" across the space you enumerate; unenumerated cells are silent omissions the transparency posture must surface as "we have not examined X")
1. **Population × Function/Room × Technique-class matrix.** Enumerate the 11 population codes × building
   functions × technique classes; empty cells are candidate slugs. Makes omissions visible.
2. **Instrument table-of-contents mining.** Walk each major (esp. under-covered-region) accessibility
   code's ToC; any technique-heading present in the code but absent from the slug set is a candidate
   (this surfaces Changing Places (BS 8300), areas of refuge (IBC/ADA), TGSI (AS 1428.4 / JIS)).
3. **Failure→technique inversion.** `accessible-design-failures-poor-performance` is a generative seed —
   each documented failure implies a technique that should have a slug.
4. **Co-1 / DPO lived-experience surfacing.** DPO literature names techniques the code-first view misses
   (DeafSpace, sensory rooms entered this way).
5. **Region×technique replication requirement.** Give every technique slug an explicit target of
   ≥N jurisdictions across ≥M regions; the hollow global-south slugs prove the current set asserts global
   scope without global evidence. Make the scope claim carry its evidentiary backing.

---

## Execution sequence (batch cadence; audit re-run each batch; adversarial pass every few batches)
1. **Batch 1 (P2 relinks)** — within-corpus relinks of already-verified rows; zero fabrication surface. Re-run `tools/evidentiary_audit.py`; expect language/anglo components to rise on ofs / luminance-lrv / laundry.
2. **Batch 2 (P1 global-south identity)** — the 3 E-grade slices; link hollow global-south rows + source real instruments; adversarial pass (fresh-context refuter) after.
3. **Batch 3 (P3 tier-lift)** — full-band anchors for therapeutic-lighting / thermoregulation.
4. **Batch 4 (DISPUTED cleanup)** — replace the 10 DISPUTED instances (ot-cpg's 2 first).
5. **Batch 5 (coverage extension)** — ToC-mine SA / Philippines / LatAm; run the Part-B matrix gap-finder; create verified candidate slugs.
6. **P4 slices** — render honestly at ◐ partial / flagged; no forced full-band.

**Discipline (non-negotiable):** every ingested source re-retrievable via a real tool call; no
back-translation; no quota parity (equity = equal search effort + transparent yield); empties kept;
migrations only; adversarial verification per `DR-2026-05-09` / `DR-2026-05-13`.
