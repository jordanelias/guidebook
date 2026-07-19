# Research Plan — Remediating the Per-Slice Evidentiary Audit (2026-07-19)

## Context

The most recent audit, `audits/evidentiary-base-audit.md` (data as of 2026-07-19, merged today in
PR #24), scores all 82 ACTIVE research slices on six dimensions and surfaces six remediation findings
in its §6. The headline problems: best-practice **anchoring is thin** (only 23% of linked instances can
anchor a best-practice claim; **20 slices have no anchor at all**), the corpus is **73% English /
Anglophone-concentrated**, **13 slices are entirely empty**, a handful rest on **one jurisdiction**, and
a few **data-hygiene defects** (mis-filed language codes in the `jurisdiction` column, NULL jurisdictions,
orphan sources) distort the counts.

This is a *research plan*, not a code-remediation plan: most of the work is finding, verifying, tier-grading,
and ingesting real evidence to raise the weakest slices above the audit's risk thresholds — using the
**existing, proven pipeline** the project already ran for nine non-English recovery batches today, not a new
process. The intended outcome: every identified issue has an owner-visible workstream, the highest-risk
slices (no-anchor, high-salience empty) gain anchors first, and the audit is **re-run to measure the shift**
rather than asserted fixed.

**Scope decision (owner):** cover **all six findings** — a short data-hygiene prep pass first, then the four
evidence-gathering workstreams. **Ambition (owner):** a **prioritized first pass** sequenced by the audit's
own risk order, with explicit targets for the top-priority slices and the long tail queued.

---

## The pipeline to reuse (do not reinvent)

The canonical recovery loop is already written down in
`working/evidence-migration/research-handoff-non-english.md` §2 and was executed across batches 1–9 today.
Every workstream below runs this same **per-batch loop**:

1. **Identify targets** — a slice + a lead (a named instrument in `search_languages.notes`, or a fresh search
   where notes are empty/stub).
2. **Verify each source re-retrieves** via a *real* tool call (WebSearch/WebFetch for a standard/law/guideline;
   PubMed / Scholar Gateway / Consensus / bioRxiv for articles). **A source that does not re-retrieve is
   dropped, never ingested** — the anti-fabrication gate.
3. **Tier + tag** per `governance/tier-system.md`: set `tier`, `evidence_type`, `lang_detected` (from the
   *home-language* source text, not English metadata), `jurisdiction`, `standard_number`,
   `verification_status`.
4. **Dedup** against `evidence_sources` (match on DOI / `standard_number` / title) — never create a twin.
5. **Ingest** via `scripts/emit_data_migration.py` → `scripts/migrate_db.py` (never an ad-hoc `UPDATE`), and
   **link to the slug** in `source_slug_links`.
6. **Adversarial verification pass** — a separate, guilty-until-proven reviewer (fresh context, briefed to
   *refute*) re-retrieves a sample and re-derives every documentation number from the live DB, per
   `decisions/DR-2026-05-09-adversarial-research-protocol.md` and
   `decisions/DR-2026-05-13-evidence-verification-methodology.md`. This is the batch-5 discipline that has
   repeatedly caught real errors.
7. **Regenerate + record** — re-run `tools/evidentiary_audit.py` (and
   `tools/regenerate_vetting_surface.py`), update the coverage matrix / tracking docs, run
   `PRAGMA foreign_key_check` + `integrity_check`.

**Check first, then research:** `working/evidence-migration/slug-language-tracking-matrix.md` is the live
"have we touched slug X / language Y yet" table — consult it before spending effort on any slug/language.

---

## Workstreams (prioritized by the audit's own risk order)

### WS0 — Data-hygiene prep (fast, unblocks accurate measurement) · Finding 6 + §3.5

One migration, no new research; makes every downstream count honest.
- **Move the 4 mis-filed language codes** out of `evidence_sources.jurisdiction` (`DA`×1, `ZH`×3) into
  `lang_detected`, and recover each source's true jurisdiction (audit §3.3).
- **Backfill / normalize the 18 NULL-jurisdiction instances** where a real home jurisdiction exists; leave
  genuinely trans-national clinical/synthesis sources NULL but confirmed-intentional (audit §3.5).
- **Review the 24 orphan sources** in `evidence_sources` linked to no active slug — link to the right slug or
  record why they're unlinked (audit §2).
- Emit via `scripts/emit_data_migration.py`; verify with `PRAGMA foreign_key_check`; re-run the audit to
  confirm JUR/%ANG denominators shift as expected.

### WS1 — Anchor the 20 no-anchor slices (P0: sharpest risk) · Finding 1

These carry real sources but **zero best-practice anchors** (no T1/Co-1/T2/Co-2), so they cannot carry a
best-practice claim. Two sub-groups, easiest-leverage first:
- **9 supporting-only (†)** — already hold confirmed T3-clinical evidence; they need *only* an anchor
  (SR/meta-analysis, T1 primary with mechanism control, Co-1 DPO output, or Co-2 CPG). Highest ROI. Targets:
  `stair-ramp-threshold-biomechanics-accessibility`, `reach-range-and-accessible-controls`,
  `circadian-lighting-melanopic-edi`, `ecological-psychology-haptic-affordances-built-environment`,
  `wayfinding-cognitive-science-spatial-design`, `intellectual-disability-built-environment-design`,
  `floor-vibration-wheelchair-disability`, `cross-population-conflict-resolutions`,
  `thermoregulation-built-environment`.
- **11 code-floor / convergence-only (‡)** — pure T4–T6/grey; need genuine confirmed evidence, not more
  codes. Targets include `luminance-contrast-and-pattern`, `threshold-and-level-access`,
  `jurisdiction-grant-programmes-comprehensive`, `visual-alerting-and-wayfinding-light`,
  `body-sizes-supplementary-populations`, `european-accessibility-act-scope-clarification`,
  `accessible-laundry-room-design`, `government-grant-programmes-home-adaptation`,
  `therapeutic-lighting-design`, `crpd-implementation-built-environment`, `co1-housing-research-global-south`
  (full list, audit §4).

This workstream directly attacks the corpus-wide thinness: only **76 Tier-2 instances exist** — prioritize
SR/meta-analysis + DPO/professional-body standard recovery.

### WS2 — Fill or formally park the 13 empty slices (P1) · Finding 4

- **6 retracted-pending-rehab** — prior work cleared, awaiting re-derivation:
  `bariatric-turning-radius-built-environment`, `bathroom-typology-global-south`,
  `fold-down-grab-bar-specification`, `jurisdiction-matrix-accessibility-standards`,
  `multilingual-evidence-convergence-non-english`, `neurodivergent-built-environment`. Re-derive via the loop.
- **7 un-started** — `evidence_state` unset, no search run:
  `accessible-design-failures-poor-performance`, `chronic-pain-built-environment`, `economics-sources`,
  `fatigue-spectrum-built-environment`, `government-grant-programmes`, `hearing-impairment-built-environment`,
  `post-occupancy-evaluation-global`. Several are high-salience (`hearing-impairment-…`,
  `chronic-pain-…`) — run a first search pass. For any that are genuine non-priorities, **formally park**
  them (set an explicit deferred `evidence_state` in `bpc_metadata`) so they stop reading as silent gaps.

### WS3 — Convert non-English search into non-English evidence (P1) · Findings 2 & 5

Searches ran in 19 languages but the corpus stays ~73% English — the gap is *yield/recovery*, not effort.
Much of the notes-extraction recovery is done (batches 1–9); the remaining work:
- **Zero-yield-language investigation** — `ar`, `bn`, `hi`, `id`, `sw` returned nothing in every slice.
  Per `research-handoff-non-english.md` §4, diagnose which of (a) tooling reachability, (b) query
  construction (native-script terms), or (c) genuine absence applies, and **publish the finding**
  (`global-south-finding.md` already started). Where genuine absence holds, pivot to Co-1 / CRPD treaty-body
  evidence and record the absence, honestly, in the coverage matrix.
- **Under-linked productive languages** — continue slug-by-slug recovery for the 14 languages that *did*
  yield, until the coverage matrix is filled (`slug-language-tracking-matrix.md`).
- **Dilute the 14 doubly-concentrated slices** (≥90% English *and* ≥50% native-Anglophone; audit §5 list,
  e.g. `accessibility-feature-market-value-uplift-framing`, `ot-cpg-built-environment`,
  `luminance-contrast-lrv-evidence-base`, `cross-population-case-studies`). Treat as citation-risk: source a
  non-Anglophone regime where possible, and flag their global-applicability claims until diluted.

### WS4 — De-risk the 3 monojurisdictional slices (P2) · Finding 3

`thermoregulation-built-environment`, `crpd-implementation-built-environment`,
`co1-housing-research-global-south` each rest on ≤1 jurisdiction. Source a second code regime; until then,
**flag their numeric thresholds as non-transferable** in `bpc_metadata` so downstream renders don't overstate
cross-jurisdiction applicability.

---

## Execution sequence (batch queue)

Mirror the existing batch cadence — one workstream slice-cluster per batch, adversarial pass every few
batches (as batch 5 was today):

1. **Batch A (WS0):** data-hygiene migration + audit re-run to reset the baseline.
2. **Batch B–D (WS1 †):** the 9 supporting-only slices — anchor-only recovery, highest ROI.
3. **Batch E–F (WS2):** the high-salience empty slices (`hearing-impairment-…`, `chronic-pain-…`,
   `neurodivergent-…`) + park the rest.
4. **Batch G (WS1 ‡):** the 11 code-floor slices — genuine confirmed evidence.
5. **Batch H (WS3):** zero-yield-language diagnosis + doubly-concentrated dilution.
6. **Batch I (WS4):** monojurisdictional de-risking + flags.
7. **Adversarial review batch** after B–D and again after G (fresh-context refuters).

Each batch ends with `tools/evidentiary_audit.py` re-run so grade movement is visible per batch.

---

## Discipline & guardrails (non-negotiable — from the handoff §6)

- **Every ingested source re-retrievable** via a real tool call; no exceptions (non-English fabrications are
  harder to catch, so the gate is loudest there).
- **No back-translation** — never relabel an English source as another language to pad the matrix.
- **No quota parity** — equity = equal search effort + transparent yield, not equal counts.
- **Empties kept** — a searched-and-found-nothing cell is a recorded finding, not a deletion.
- **Tier by doctrine** — `governance/tier-system.md`; T4–T6 convergence is *not* a best-practice anchor.
- **Migrations only** — `emit_data_migration.py` → `migrate_db.py`; never ad-hoc SQL against `guidebook.db`.

---

## Verification (how we prove it worked, end-to-end)

- **Re-run the audit:** `python tools/evidentiary_audit.py` regenerates
  `audits/evidentiary-base-audit.{md,json,csv}` byte-deterministically from the DB. Compare grade
  distribution before/after — success = no-anchor count down, empty count down, Tier-2/anchor share up,
  English share down.
- **Integrity:** `PRAGMA foreign_key_check` + `PRAGMA integrity_check` clean after every migration; no new
  duplicate DOIs/standard-numbers.
- **Adversarial sample:** fresh-context reviewer re-retrieves a random sample of newly-ingested sources and
  re-derives documentation numbers from the live DB.
- **Vetting surface:** `python tools/regenerate_vetting_surface.py` and the dashboard
  `tools/evidentiary-audit-dashboard.html` reflect the new state.

---

## Critical files & tables

- **Audit + regen:** `audits/evidentiary-base-audit.{md,json,csv}`, `tools/evidentiary_audit.py`,
  `tools/evidentiary-audit-dashboard.html`, `tools/regenerate_vetting_surface.py`.
- **Pipeline docs:** `working/evidence-migration/research-handoff-non-english.md`,
  `working/evidence-migration/HANDOFF.md`, `working/evidence-migration/slug-language-tracking-matrix.md`,
  `working/evidence-migration/non-english-coverage-matrix.json`,
  `working/evidence-migration/global-south-finding.md`, `.../equity-dashboard.md`.
- **Tooling:** `scripts/emit_data_migration.py`, `scripts/migrate_db.py`.
- **Doctrine:** `governance/tier-system.md`, `references/project-standards.md`,
  `decisions/DR-2026-05-09-adversarial-research-protocol.md`,
  `decisions/DR-2026-05-13-evidence-verification-methodology.md`.
- **DB (`data/guidebook.db`):** `evidence_sources`, `source_slug_links`, `search_languages`,
  `search_coverage`, `bpc_metadata`, `jurisdictional_values`, `source_value_extractions`.
- **This plan (proposed home):** `workplan/evidentiary-base-research-plan-2026-07-19.md`.

---

## Known risk / open item

**Network egress is session-dependent.** Batch 9 today confirmed CrossRef / OpenAlex / Semantic Scholar and
`WebFetch` were **blocked this session** (same root-cause egress policy), while `WebSearch` worked. Before a
research batch, confirm which retrieval tools are reachable (`curl "$HTTPS_PROXY/__agentproxy/status"`); if
DOI-resolver egress is down, fall back to `WebSearch`-corroboration (the batch 6–8 standard) and defer
citation-mining rows honestly rather than fabricating or silently skipping.
