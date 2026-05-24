# DR-2026-05-23: Pre-rehabilitation banner — cohort definition

**Status:** PROPOSED (pending owner ratification)
**Adopted by:** session_2026-05-23-bpc-rewrite-phase-b-closure (B.0 banner application)
**Sharpens:** PI v10.14 standing rule #10 final paragraph (cohort definition) — operational scope only; no PI text amendment required.

## Problem

PI standing rule #10 final paragraph defines the cohort eligible for the `SYNTHESIS VALIDITY: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner as:

> BPCs bearing `opus_synthesis: YES [OPUS-SYNTHESIS]` from the **2026-03-30 round** carry [...] banner until Phase E.2g overwrites.

Two operational issues with the literal text:

1. **"2026-03-30 round" is descriptive, not bounding.** Opus synthesis was performed in multiple rounds prior to the 2026-05-23 evidence-metadata-rehabilitation completion (HEAD `b0a4a25`). The 2026-03-29/30 round is the largest single cohort but is not the only pre-rehab synthesis batch. Survey of `references/bpc/` finds positive `[OPUS-SYNTHESIS*]` tags across at least four rounds:
   - `[OPUS-SYNTHESIS]` (bare, with `Updated: 2026-03-29 (Opus synthesis)` header) — ~65 files. The "2026-03-30 round."
   - `[OPUS-SYNTHESIS 2026-04-07]` — 14 files. April round.
   - `[OPUS-SYNTHESIS-PROVISIONAL]` — 1 file (`cross-population-conflict-resolutions`, cross-population dir).
   - `[OPUS-SYNTHESIS — CLINICAL DERIVATION]`, `[OPUS-SYNTHESIS — CLINICAL DERIVATION + ENGINEERING TRANSLATION]`, `[OPUS-SYNTHESIS — PROVISIONAL — 2-session run]` — additional ~3 file-instances.

   All four rounds used evidence carrying pre-rehabilitation AUTHOR-TITLE-ONLY metadata gaps (which the 2026-05-23 rehab session closed at 638/638 eligibility). The epistemic basis for the banner — that the synthesis cited evidence whose metadata quality could not be validated against PI rule #10's existence gate — applies identically to all four rounds.

2. **Handoff target estimate (~30 BPCs) was off by ~2.3×.** Session_2026-05-23 handoff sized B.0 at "~30 BPCs." Actual cohort under either literal or spirit reading is 65–70 files (68 unique slugs).

## Decision

The banner cohort is defined by **tag presence + pre-rehab dating**, not by the literal "2026-03-30 round" phrase:

**Eligibility criterion.** Any file under `references/bpc/` containing a positive `[OPUS-SYNTHESIS*]` tag (any variant: bare, dated, provisional, or annotated) where the synthesis date predates the evidence-metadata-rehabilitation closure (2026-05-23, commit `b0a4a25`).

**Negative exclusion.** Files where the only `opus_synthesis` declaration is `false` or `NO` (Sonnet drafts with no Opus pass) are excluded — those carry the existing REDUCED-CONFIDENCE warning from PI rule #2 instead.

**Banner text** (unchanged from PI rule #10 phrasing):

```
**SYNTHESIS VALIDITY:** PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION
(See PI rule #10; cohort defined by DR-2026-05-23. Evidence cited herein
predates the 2026-05-23 metadata-quality rehabilitation. Claims requiring
Phase E.2g reverification.)
```

**DB state mirror.** Each unique slug in the cohort gets `bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB'`. Applied via timestamped data migration (forward-only, append-only) per architecture v2.3 `<data_layer_pattern>`.

## Why no PI amendment is needed

Per architecture v2.3 `<migration_and_growth>`: "PI standing rules describe rules, not state. State content — current AUTHOR-TITLE-ONLY counts, retraction banners, session-specific commentary — belongs in DRs, audit scripts, or the DB."

The cohort scope decision is operational classification (which BPCs satisfy the banner predicate), not a change to the banner mechanism, the banner removal predicate, or the eligibility gate. The rule's existing text ("from the 2026-03-30 round") is defensible as descriptive shorthand for the dominant batch; this DR refines the practical scope without contradicting the rule's predicate or mechanism.

Armature for the broader-cohort interpretation lives outside PI:

- **DR (this document)** — codifies criterion + enumeration.
- **`decisions/DR-2026-05-23-cohort-manifest.json`** — frozen enumeration at HEAD `b0a4a25`.
- **`scripts/audit/pre_rehab_banner_audit.py`** — Level 2 audit enforcing the four invariants below.
- **`bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB'`** — queryable source of truth, mirrored across 68 unique slugs.

If a future owner directive narrows the cohort (e.g., back to the literal 2026-03-30 round), the path is forward-reversible per slug via a counter-migration; no PI text changes are required to apply or to unwind.

## Cohort enumeration

Frozen at this DR's adoption: **70 files, 68 unique slugs.** Manifest stored in the migration file's leading comment block and in `decisions/DR-2026-05-23-cohort-manifest.json` (committed alongside this DR for audit replay).

Two slugs have two markdown files each (legacy flat-root + categorized copy or alternate-category copy). Both file-copies receive the banner; the DB row (one per slug) is updated once.

- `thermoregulation-built-environment` — `references/bpc/thermoregulation-built-environment.md` AND `references/bpc/health-and-symptom-management/thermoregulation-built-environment.md`.
- `cross-population-conflict-resolutions` — `references/bpc/frameworks-and-methodology/cross-population-conflict-resolutions.md` AND `references/bpc/cross-population/cross-population-conflict-resolutions.md`.

These duplicates are noted as a separate cleanup item (Phase E.2g triage); banner application does not resolve them.

## Phase E.2g overwrite

Banner removal is governed by PI rule #10 sub-rules 1/2/3 — a banner clears only when:

1. Every synthesis claim in the file is backed by either (a) a `spec_value_probes` PMP walk passing strict termination (numerical-spec claims), or (b) a `reasoning_doc_citations` row with `value_match ∈ {EXACT, WITHIN-TOLERANCE}` (jurisdiction-comparison cells), or (c) a `reasoning_doc_citations` row with `claim_match ∈ {SUPPORTED, PARTIAL}` (qualitative/definitional claims).
2. All cited `evidence_sources` rows satisfy the rule #10 existence gate (`metadata_quality ∈ {COMPLETE, COMPLETE-STATUTORY}`, `verification_status ∈ {VERIFIED, UNVERIFIED-1}`) — automatic after the 2026-05-23 rehab closure, since all 638 rows now meet it.
3. The corresponding `bpc_metadata.evidence_state` is transitioned out of `RETRACTED-PRE-REHAB` (to `REVERIFIED-PRE-E2G-PASS` or analogous; nomenclature locked when Phase E.2g protocol is authored).

Banner removal is per-file. A partial Phase E.2g pass (some claims reverified, others not) does not remove the banner.

## Audit

`scripts/audit/pre_rehab_banner_audit.py` (Level 2 — to be authored in a follow-up session; not blocking) verifies:

- Every cohort file (by current `[OPUS-SYNTHESIS*]` tag scan) carries the banner.
- Every cohort slug has `bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB'`.
- No file outside the cohort carries the banner.
- Drift between markdown banner and DB `evidence_state` is reported as `[GAP]`.

Until the audit ships, integrity is maintained by the same migration-applies-everything pattern that landed the banner (re-running the migration is idempotent on the DB side; the markdown side is idempotent by the banner-presence guard in the insertion script).

## Trade-offs

**Accepted:** Stricter banner application widens the cohort to ~70 BPCs from the ~30 the handoff sized. The trade-off is correctness over speed — applying the banner to a strictly broader cohort under-claims rather than over-claims synthesis validity, which is the conservative direction.

**Rejected alternative — apply banner only to the 14 dated April-round files.** This would leave the larger March-round cohort un-bannered, which fails the rule #10 spirit (any pre-rehab synthesis is retracted-pending-reverification).

**Rejected alternative — apply banner manually only to BPCs with explicit `Status: COMPLETE — Opus synthesis complete` line.** This catches 8 of the 70 files, misses the rest. The tag is the durable signal; Status lines drift across edits.

## Related

- PI v10.14 standing rule #10 (existence gate + sub-rules 1/2/3).
- PI rule #10 amendment queued for v10.15 in `decisions/PI-update-needed.md`.
- Architecture v2.3 `<data_layer_pattern>` — migration discipline.
- Architecture v2.3 `<migration_and_growth>` — DR adoption path.
- BPC rewrite workplan §B.0 (this is the B.0 closure mechanism).
