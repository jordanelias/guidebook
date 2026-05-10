# Session: 2026-05-10 — BPC Audit Passes 0/1/2
**Model:** Opus 4.7 (per system context; UI-set; per `<model_identity>` not independently verifiable)
**session_close:** 2026-05-10 05:30 UTC
**next_action:** Pass 2B (5-item citation verification queue under research-log-manager CHECK/LOG protocol) → Pass 2E (file 14 gaps via `db.py add-gap`) → Pass 2A application (apply 5 remediation drafts via toc-editor + Change Order) → Pass 2C BPC body commit (`cross-population-conflict-resolutions.md`) after owner review of DEM "loop plan" reinterpretation. Order is owner's call.
**blockers:** Owner sign-off needed on (a) Pass 1D / Pass 2C cross-pop corridor resolution framing — specifically the claim that DEM "loop plan" topology evidence (Marquardt & Schmieg 2009) does not imply narrow corridor cross-section; (b) gap-categorisation for the 14 Pass 2E gaps before bulk SQLite insertion; (c) IntD BPC existence question per RULE 2026-03-25.

**github_writes:**
- `references/audits/bpc-audit-pass0-2026-05-10.md` (527 lines)
- `references/audits/bpc-audit-pass1-2026-05-10.md` (184 lines)
- `references/audits/bpc-audit-pass2-2026-05-10.md` (412 lines)

**commit_oids:**
- Pass 0: `851545adbec885` (`governance: build BPC audit Pass 0 [2026-05-10 04:41]`)
- Pass 1: `ba150fed6a7374` (`governance: build BPC audit Pass 1 [2026-05-10 04:51]`)
- Pass 2: `9d2731e58167bd` (`governance: build BPC audit Pass 2 [2026-05-10 05:11]`)

**intervening commit observed:** HEAD shifted from `ba150fe` (post-Pass-1) to `351a4f` (pre-Pass-2). An external commit landed between Pass 1 and Pass 2; my Pass 2 commit was based on the updated HEAD without conflict. Source of intervening commit not investigated this session.

---

## Audit thesis (in one sentence)

Best-practice values across the BPC corpus are systematically pulled toward code-consensus (Tier 6) defaults rather than Tier 1/Co-1/Tier 2/Co-2/Tier 3 evidence-supported maxima — the "Convergence ≠ Evidence" failure — and the corpus's own evidence base contains larger values that have been selectively un-cited.

## Methodology added this session

1. **Convergence ≠ Evidence** — formalisation of project-standards line 20. A `best_practice_synthesis` value qualifies as best practice only if Tier 1/Co-1, Tier 2/Co-2, or Tier 3 evidence supports it AND no higher-tier source recommends a more accommodating value for any reasonable in-population sub-segment. Code consensus across N jurisdictions is not best practice.
2. **Quantitative Ascending Search (QAS)** — for each numerical parameter, search incrementally higher values; accept if Tier 3 or better support exists; stop after two consecutive misses; the highest evidence-supported value is the audit's ceiling.
3. **Geometry-vs-path framing** — "turning circle" assumes an idealised pivot most wheelchairs cannot perform. Real spec is **swept envelope**, drive-system-dependent (MWD / RWD / FWD / scooter), with T-shape / multi-point alternatives. Steinfeld 2006 figures *are* empirical swept paths in defined bays — not idealised circles.
4. **STUB downstream trace** — pre-commit check that no Part 4 spec cites a BPC whose `Best-practice synthesis` section is `[STUB...]`. Drafted as Phase 2 hook proposal.
5. **`Convergence ≠ Evidence` corollary added by user mid-session:** "most cited / highest convergence ≠ best practice unless justified by Tier 1/2 source" → tightened to **Tier 3 or better** at user's instruction.

## Headline findings

### Wheelchair turning circle 180°

| Tier | Value | Source | In-corpus? |
|---|---|---|---|
| 6 (code) | 1500–1525 mm | ADA, AS, DIN, NBR, KR, BFS, NZS, GB | Yes — explicitly REJECTED in `mob_pg.md` |
| 2 (DPO) | **1500 mm** | Disability Scotland TAG (GCIL 2014) kitchens | DPO did NOT raise above code |
| 5 | 1700 mm | RHFAC CA, BS 8300 UK | Yes |
| **2 (DPO) / 5** | **1800 mm** | **IWA BPAG p.29 / BS 8300-2 Annex G** | Yes — current "best practice" |
| 5 | 1830 mm | VA Barrier-Free 2025 (bariatric) | Yes |
| 3 | 1925 mm | Steinfeld 2006 RESNA UDI 180° (open-ended) | Yes — bariatric BPC |
| **3** | **2400 mm** | **Steinfeld 2006 RESNA IDEA + BS8300 entire samples 180°** | **NO — same paper, selectively un-cited** |

### Corridor primary mixed-population

| Tier | Value | Source | In-corpus? |
|---|---|---|---|
| 6 | 1200 mm | UK Part M, DE DIN 18040 | Yes — reported without rejection language |
| 5 | 1800 mm | BS 8300, DIN 18040 (two-WC) | Yes — current "best practice" in `circ.md` |
| 2 / 3 | 1830 mm | DSDG (secondary corridors) | DEAF BPC only |
| **Co-1 / 2 / 3** | **2440 mm** | **DSDG primary + Vaughn 2018 + Cloete & Rout 2025** | DEAF BPC only — invisible from `circ.md` |
| Co-1 | 3050 mm | DSDG public exterior | DEAF BPC only |

### Substantive findings

| Code | Topic | Pass |
|---|---|---|
| F1 | Corridor width: code-consensus default mislabelled "best practice" in `circ.md` | Pass 0 §4.1 |
| F2 | Lift dimensions: same pattern, smaller magnitude (1100×1800 vs Tier 5 BS 8300 1100×2000) | Pass 0 §4.1 |
| F3 | Corridor reasoning structurally excludes DEAF and bariatric | Pass 0 §4.1 |
| F-X1 | Internal contradiction: corridor width (`circ.md` 1800 vs `deaf-spatial-design` 2440) | Pass 0 §5 |
| F-X2 | 17 BPCs use code-floor values without rejection language | Pass 0 §5 |
| F-X3 | "Aligned on best practice" linguistic conflation | Pass 0 §5 |
| F-X4 | Geometry framing failure: "turning circle" assumes pivot | Pass 0 §5 |
| F-X5 | Tier numbering inconsistency: project-standards (Tier 3 = systematic review) vs guidebook-auditor SKILL (Tier 4 = systematic review) | Pass 0 §5 |
| Pass 1A | 5 confirmed PROVISIONAL files with substantive risk (corridor, residential-entry, kitchen, reach, MOB-general) — clustered around the same code-floor pattern | Pass 1 §1A |
| Pass 1A reclassifications | 4 Pass 0 false-positive PROVISIONAL flags corrected (mental-health, pain-ofs, residential-accessible-home-case-studies, co1-housing-research-global-south) | Pass 1 §1A |
| Pass 1C | 3 STUB BPCs cited as Part 4 evidence basis: `sensory-processing-model-design-application`, `sensory-relief-space-design`, `upper-limb-impairment-built-environment` | Pass 1 §1C |
| Pass 1D / 2C | Cross-pop corridor conflict resolved via Step-0 variable disambiguation: 2440mm primary + glazed intersections satisfies DEAF + NDV/MH + DEM simultaneously | Pass 1 §1D / Pass 2 §2C |

### Independent verifications completed

- IWA BPAG Edition 4 (2020) p.29 — direct quote confirmed: "powered wheelchair which requires a 1800mm turning circle"
- IWA BPAG 2300mm value — confirmed to be **suspended sign clear headroom**, not turning circle
- Disability Scotland TAG (GCIL 2014) — turning circle = 1500mm; 2200mm is kitchen layout dimension, not turning
- Steinfeld 2006 RESNA paper — full text retrieved, contains 1925mm UDI 180°, **2400mm IDEA + BS8300 entire-sample 180°**, ~4200mm UDI 360°
- DSDG 2440mm — corroborated via Vaughn 2018, Cloete & Rout 2025, RIT InfoGuides, NEA, DesignWithDisabledPeopleNow

### Pass 2B handoff queue (5 items — citation verification needed)

1. **Steinfeld 2010, n=500** (cited in `mob_pg.md`) — likely IDeA Center book/report; verify exists, sample size, contains 2400mm or higher
2. **van der Schaaf 2013, n=23,868 across 199 wards** (mental-health BPC) — Tier 1 anchor for "private space per patient" claim
3. **Faerden 2022, Cohen's d = 2.0 patient support** (mental-health BPC) — high-effect-size claim per RULE 2026-04-09 high-risk pattern
4. **Weltens 2023, OR 5.36 overcrowding→aggression** (mental-health BPC) — exact OR value verification
5. **Avandell NJ $12,000/month vs US memory-care $7,500/month → 60% premium** (`accessibility-feature-market-value-uplift-framing.md`) — **highest fabrication risk** per RULE 2026-04-09; economics BPC was caught with 3 fabricated quantified findings 2026-04-09

### Pass 2E handoff queue (14 gaps — `db.py add-gap` calls owed)

Full list in `bpc-audit-pass2-2026-05-10.md` §"Pass 2E handoff." 7× P1, 5× P2, 1× P3. 9× AUDT, 4× EG, 1× governance/doctrine-recheck. Owner sign-off on category and priority recommended before bulk insertion.

## Pattern of bias documented (this session, building on session 2026-05-09)

The prior session's bias pattern was: "I conflated 'evidence on the topic' with 'evidence supporting the specific claim'" — owner correction rate 67%.

This session adds: **selective citation within a single source** — Steinfeld 2006 paper reports both 1925mm (UDI sub-sample, open-ended bay) and 2400mm (IDEA + BS8300 entire samples, enclosed bay); the bariatric BPC cites only the smaller value. This is a less-flagrant form of the prior bias (the citation IS supportive of the topic and the chosen number) but produces the same practical outcome — the reader doesn't see the larger-value evidence.

**Mitigation pattern this session:** every numerical claim run through QAS (search higher values; stop only when two consecutive Tier-3+ misses). Surfaced the 2400mm value the original BPC author had passed over.

**Pass 2 self-bias disclosure:** I drafted text I then proposed for the project's BPCs. The Pass 2C `cross-population-conflict-resolutions.md` body in particular hinges on reinterpreting Marquardt & Schmieg 2009 as topology-not-narrowness evidence — defensible from the abstract, but DEM-specialist review owed before it lands.

## Multilingual remediation Tier 1 — still pending

Carried forward from session 2026-05-09 next_action. Not addressed this session.

## What this audit deliberately did NOT do

- Modify any BPC, Part 4 prose, or other content file. All audit outputs in `references/audits/` only.
- File the 14 gaps in SQLite. Hand-off to Pass 2E.
- Run citation-verifier on the Pass 2B queue.
- Apply the Pass 1D / Pass 2C resolution to DEM BPC ("loop plan" reinterpretation).
- Adjudicate IntD BPC existence question.

## Recommended next-session sequence

1. **Owner review of audit findings** — 30 min reading the three audit docs; flag any framings to push back on (especially the Pass 2C DEM reinterpretation and the IntD existence question)
2. **Pass 2B citation verification** — fresh context, research-log-manager CHECK/LOG; ~1 session
3. **Pass 2E gap-filing** — bulk `db.py add-gap`; ~30 min mechanical
4. **Pass 2A application** — apply 5 remediation drafts via `toc-editor` + Change Order; ~1 session
5. **Pass 2C commit** — drafted `cross-population-conflict-resolutions.md` body to repo after DEM reinterpretation review
6. **Phase 2 hook landing** — `bpc-stub-cited-by-part4` per Pass 2D draft

Total estimated: 3–4 sessions to full audit closure.

## Audit success metric

If the next 5 sessions close all P1 gaps and all 5 PROVISIONAL files in the wheelchair-test cluster are remediated, the corpus's largest-value-evidence-supported ceilings will be visible in every relevant best-practice synthesis. The Pass 2D hook prevents regression on the STUB-citation pattern.

---

**End session.**
